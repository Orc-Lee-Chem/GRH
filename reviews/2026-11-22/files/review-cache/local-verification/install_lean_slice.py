import concurrent.futures
import hashlib
import json
import pathlib
import struct
import time
import zipfile
import zlib
import requests
import argparse
import threading
from remote_zip_inventory import RemoteZip

ROOT = pathlib.Path(__file__).parent
DEST = ROOT / "toolchain"
PREFIX = "lean-4.33.1-windows/"
MODE = "public"
IR_MODULES = set()

def wanted(name):
    if MODE == "ir":
        return any(name in {PREFIX + "lib/lean/" + module.replace(".", "/") + suffix for suffix in (".ir", ".ir.sig")} for module in IR_MODULES)
    if MODE in {"server", "private"}:
        core = name.removeprefix(PREFIX + "lib/lean/")
        return name.startswith(PREFIX + "lib/lean/") and core.split("/")[0].split(".")[0] in {"Init", "Lean", "Std"} and name.endswith(".olean." + MODE)
    if name in {PREFIX + "bin/" + file for file in ["lean.exe", "leanchecker.exe", "leantar.exe", "libc++.dll", "libInit_shared.dll", "libleanshared.dll", "libleanshared_1.dll", "libleanshared_2.dll", "zlib1.dll"]}:
        return True
    core = name.removeprefix(PREFIX + "lib/lean/")
    return name.startswith(PREFIX + "lib/lean/") and core.split("/")[0].split(".")[0] in {"Init", "Lean", "Std"} and name.endswith(".olean")

def main():
    global MODE, IR_MODULES
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["public", "server", "private", "ir"], default="public")
    parser.add_argument("--module", action="append", default=[])
    args = parser.parse_args()
    MODE = args.mode
    IR_MODULES = set(args.module)
    if MODE == "ir" and not IR_MODULES:
        raise RuntimeError("IR mode requires explicit modules")
    started = time.monotonic()
    release = json.loads((ROOT / "lean-release.json").read_text(encoding="utf-8"))
    asset = next(a for a in release["assets"] if a["name"] == "lean-4.33.1-windows.zip")
    remote = RemoteZip(asset["browser_download_url"] + "?download=1", asset["size"])
    with zipfile.ZipFile(remote) as archive:
        infos = [info for info in archive.infolist() if wanted(info.filename)]
    records = [{"name": i.filename, "offset": i.header_offset, "compressed": i.compress_size, "bytes": i.file_size, "crc": i.CRC, "method": i.compress_type} for i in infos]
    groups = []
    for entry in sorted(records, key=lambda x: x["offset"]):
        # Leave room for local filename/extra data and optional trailing descriptor.
        end = entry["offset"] + entry["compressed"] + len(entry["name"].encode()) + 4096
        if groups and entry["offset"] - groups[-1]["end"] < 16384 and end - groups[-1]["start"] < 4 * 1024 * 1024:
            groups[-1]["end"] = max(groups[-1]["end"], end)
            groups[-1]["entries"].append(entry)
        else:
            groups.append({"start": entry["offset"], "end": end, "entries": [entry]})
    estimate = sum(g["end"] - g["start"] for g in groups)
    limit = (15 if MODE == "ir" else 450 if MODE == "private" else 240) * 1024 * 1024
    if estimate > limit:
        raise RuntimeError(f"Selective download would exceed its byte budget: {estimate}")
    DEST.mkdir(exist_ok=True)
    print(f"SELECTED files={len(records)} groups={len(groups)} network_estimate={estimate} disk_bytes={sum(r['bytes'] for r in records)}", flush=True)
    thread_state = threading.local()
    def extract_group(group):
        pending = [e for e in group["entries"] if not (DEST / e["name"].removeprefix(PREFIX)).exists()]
        if not pending:
            return 0
        if not hasattr(thread_state, "session"):
            thread_state.session = requests.Session()
        for attempt in range(4):
            try:
                response = thread_state.session.get(remote.url, headers={"Range": f"bytes={group['start']}-{group['end']-1}"}, timeout=30, stream=True)
                if response.status_code != 206:
                    response.close()
                    raise RuntimeError(f"Range status {response.status_code}")
                data = response.content
                expected = f"bytes {group['start']}-"
                if not response.headers.get("Content-Range", "").startswith(expected):
                    raise RuntimeError("Unexpected range returned")
                break
            except Exception:
                if attempt == 3:
                    raise
        for entry in pending:
            pos = entry["offset"] - group["start"]
            header = struct.unpack_from("<4s5H3I2H", data, pos)
            if header[0] != b"PK\x03\x04":
                raise RuntimeError("Bad local ZIP header")
            data_start = pos + 30 + header[-2] + header[-1]
            compressed = data[data_start:data_start + entry["compressed"]]
            content = zlib.decompress(compressed, -15) if entry["method"] == 8 else compressed
            if len(content) != entry["bytes"] or zlib.crc32(content) & 0xffffffff != entry["crc"]:
                raise RuntimeError(f"ZIP CRC/size mismatch: {entry['name']}")
            path = DEST / entry["name"].removeprefix(PREFIX)
            if not path.resolve().is_relative_to(DEST.resolve()):
                raise RuntimeError("Unsafe extraction path")
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)
            entry["sha256"] = hashlib.sha256(content).hexdigest()
        return len(data)
    transferred = remote.transferred
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(extract_group, group) for group in groups]
        for index, future in enumerate(concurrent.futures.as_completed(futures), 1):
            transferred += future.result()
            if index % 100 == 0:
                print(f"PROGRESS groups={index}/{len(groups)} network_bytes={transferred}", flush=True)
    receipt = {"release_url": asset["browser_download_url"], "network_bytes": transferred, "seconds": time.monotonic() - started, "files": records}
    for record in records:
        record["sha256"] = hashlib.sha256((DEST / record["name"].removeprefix(PREFIX)).read_bytes()).hexdigest()
    (ROOT / f"lean-slice-{MODE}-receipt.json").write_text(json.dumps(receipt, indent=2), encoding="utf-8")
    print(f"DONE network_bytes={transferred} seconds={receipt['seconds']:.2f}", flush=True)

if __name__ == "__main__":
    main()
