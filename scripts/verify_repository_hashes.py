"""Verify manifest hashes against committed Git bytes, independent of checkout EOLs."""
import argparse
import hashlib
import pathlib
import subprocess


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--revision", default="HEAD", help="Git revision; use INDEX for staged files")
    args = parser.parse_args()
    repo = pathlib.Path(__file__).resolve().parents[1]
    prefix = ":" if args.revision == "INDEX" else args.revision + ":"
    manifest = subprocess.check_output(["git", "show", prefix + "SHA256SUMS.txt"], cwd=repo).decode("utf-8")
    failures = []
    count = 0
    for line in manifest.splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        expected, name = line.split("  ", 1)
        path = name.replace("\\", "/")
        data = subprocess.check_output(["git", "show", prefix + path], cwd=repo)
        if hashlib.sha256(data).hexdigest() != expected:
            failures.append(path)
        count += 1
    if failures:
        raise SystemExit("HASH MISMATCH: " + ", ".join(failures))
    print(f"VERIFIED {count} Git files against SHA256SUMS.txt ({args.revision})")


if __name__ == "__main__":
    main()
