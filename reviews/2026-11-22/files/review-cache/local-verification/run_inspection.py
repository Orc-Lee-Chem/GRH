import json
import os
import pathlib
import subprocess
import time
import psutil

ROOT = pathlib.Path(__file__).parent

def main():
    records = json.loads((ROOT / "selected_oleans.json").read_text(encoding="utf-8"))
    paths = [ROOT / "project" / ".lake" / "build" / "lib" / "lean" / (r["module"].replace(".", "/") + ".olean") for r in records]
    (ROOT / "olean-list.txt").write_text("\n".join(str(p) for p in paths) + "\n", encoding="utf-8")
    command = [str(ROOT / "toolchain" / "bin" / "lean.exe"), "-j1", "-M2048", "--tstack=400000", "--run", "InspectSelected.lean", "olean-list.txt", "inspect.jsonl"]
    env = dict(os.environ)
    env["LEAN_ABORT_ON_PANIC"] = "1"
    started = time.monotonic()
    peak = 0
    with (ROOT / "inspection.stdout.log").open("wb") as stdout, (ROOT / "inspection.stderr.log").open("wb") as stderr:
        process = subprocess.Popen(command, cwd=ROOT, env=env, stdout=stdout, stderr=stderr)
        monitored = psutil.Process(process.pid)
        while process.poll() is None:
            try:
                peak = max(peak, monitored.memory_info().rss)
            except psutil.NoSuchProcess:
                pass
            if peak > 2600 * 1024 * 1024 or time.monotonic() - started > 180:
                process.kill()
                raise RuntimeError("Local inspection exceeded its resource limit")
            time.sleep(0.1)
        code = process.wait()
    receipt = {"command": command, "exit_code": code, "seconds": time.monotonic() - started, "peak_rss_bytes": peak}
    (ROOT / "inspection-receipt.json").write_text(json.dumps(receipt, indent=2), encoding="utf-8")
    print(json.dumps(receipt, indent=2))
    print((ROOT / "inspection.stdout.log").read_text(encoding="utf-8"))
    print((ROOT / "inspection.stderr.log").read_text(encoding="utf-8"))
    if code:
        raise SystemExit(code)

if __name__ == "__main__":
    main()
