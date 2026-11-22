import gzip
import pathlib

root = pathlib.Path(__file__).parent / "files/review-cache/local-verification"
for source in sorted(root.rglob("*.gz")):
    target = source.with_suffix("")
    data = gzip.decompress(source.read_bytes())
    if target.exists() and target.read_bytes() != data:
        raise RuntimeError(f"Refusing to overwrite a different file: {target}")
    target.write_bytes(data)
    print(target.relative_to(root), len(data))
