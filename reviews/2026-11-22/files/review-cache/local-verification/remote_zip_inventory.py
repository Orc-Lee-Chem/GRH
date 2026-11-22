import io
import json
import pathlib
import requests
import zipfile

ROOT = pathlib.Path(__file__).parent

class RemoteZip(io.RawIOBase):
    def __init__(self, url, size):
        self.url = url
        self.size = size
        self.position = 0
        self.transferred = 0
        self.session = requests.Session()
        self.cached = []

    def seekable(self):
        return True

    def readable(self):
        return True

    def tell(self):
        return self.position

    def seek(self, offset, whence=0):
        self.position = offset if whence == 0 else self.position + offset if whence == 1 else self.size + offset
        return self.position

    def read(self, count=-1):
        if count < 0:
            count = self.size - self.position
        count = min(count, self.size - self.position)
        if count <= 0:
            return b""
        start = self.position
        end = start + count
        for lo, data in self.cached:
            if lo <= start and end <= lo + len(data):
                self.position = end
                return data[start-lo:end-lo]
        # Fetch adjacent bytes too, but never silently download the whole release.
        fetch_start = max(0, start - 128)
        fetch_end = min(self.size, max(end, fetch_start + 131072))
        response = self.session.get(self.url, headers={"Range": f"bytes={fetch_start}-{fetch_end-1}"}, timeout=60, stream=True)
        if response.status_code != 206:
            response.close()
            raise RuntimeError(f"Range request was not honoured: HTTP {response.status_code}")
        content_range = response.headers.get("Content-Range", "")
        if not content_range.startswith(f"bytes {fetch_start}-"):
            response.close()
            raise RuntimeError(f"Unexpected Content-Range: {content_range}")
        data = response.content
        self.url = response.url
        self.transferred += len(data)
        self.cached.append((fetch_start, data))
        if len(self.cached) > 12:
            self.cached.pop(0)
        self.position = end
        return data[start-fetch_start:end-fetch_start]

def main():
    release = json.loads((ROOT / "lean-release.json").read_text(encoding="utf-8"))
    asset = next(a for a in release["assets"] if a["name"] == "lean-4.33.1-windows.zip")
    remote = RemoteZip(asset["browser_download_url"] + "?download=1", asset["size"])
    with zipfile.ZipFile(remote) as archive:
        entries = [{"name": i.filename, "compressed": i.compress_size, "bytes": i.file_size} for i in archive.infolist()]
    (ROOT / "lean-zip-inventory.json").write_text(json.dumps(entries, indent=2), encoding="utf-8")
    print("ZIP_INDEX_NETWORK_BYTES", remote.transferred)
    for entry in entries:
        name = entry["name"]
        if name.endswith(".dll") or name.endswith("/lean.exe") or name.endswith("/Init.olean") or name.endswith("/Lean.olean"):
            print(entry)
    print("TOTAL_ENTRIES", len(entries))

if __name__ == "__main__":
    main()
