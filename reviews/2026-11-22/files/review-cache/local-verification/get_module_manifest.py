import gzip
import hashlib
import json
import pathlib
import requests
import concurrent.futures

ROOT = pathlib.Path(__file__).parent
REV = "e50d09817ad81469f737e8f637561e6ccf86c670"
EXPECTED = "292caa386a620d935cfc736b56fcceaab9fe7073086693b62e899c1ee4725f04"

def main():
    url = f"https://rh-cache.taucetiproject.org/bootstrap/{REV}/modules.jsonl.gz"
    head = requests.head(url, timeout=30)
    head.raise_for_status()
    size = int(head.headers["Content-Length"])
    ranges = [(start, min(start + 262144, size)) for start in range(0, size, 262144)]
    def fetch_chunk(pair):
        start, end = pair
        for attempt in range(3):
            try:
                response = requests.get(url, headers={"Range": f"bytes={start}-{end-1}"}, timeout=30)
                if response.status_code != 206 or len(response.content) != end - start:
                    raise RuntimeError(f"Bad response for range {pair}: {response.status_code}")
                return response.content
            except Exception:
                if attempt == 2:
                    raise
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        content = b"".join(executor.map(fetch_chunk, ranges))
    print("MANIFEST_BYTES", len(content))
    digest = hashlib.sha256(content).hexdigest()
    if digest != EXPECTED:
        raise RuntimeError(f"Manifest SHA mismatch: {digest}")
    (ROOT / "modules.jsonl.gz").write_bytes(content)
    data = gzip.decompress(content)
    (ROOT / "modules.jsonl").write_bytes(data)
    print("SHA256", digest)
    print(data[:2200].decode("utf-8"))
    settings = requests.get("https://raw.githubusercontent.com/leanprover-community/riemann-hypothesis/main/scripts/restore-cache.py", timeout=30)
    settings.raise_for_status()
    (ROOT / "upstream-restore-cache.py").write_bytes(settings.content)

if __name__ == "__main__":
    main()
