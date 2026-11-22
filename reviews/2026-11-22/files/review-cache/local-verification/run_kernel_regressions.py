"""Run reviewed official structural soundness regressions, without repository imports."""
import hashlib
import json
import pathlib
import subprocess
import time
import psutil

ROOT = pathlib.Path(__file__).parent
OUT = ROOT / "trust-audit"
REG = OUT / "regressions"

def main():
    sources = json.loads((REG / "sources.json").read_text(encoding="utf-8"))
    previous_path = OUT / "regression_receipts.json"
    previous = {r["file"]:r for r in json.loads(previous_path.read_text(encoding="utf-8"))} if previous_path.exists() else {}
    receipts = []
    for source in sources:
        path = REG / source["file"]
        assert hashlib.sha256(path.read_bytes()).hexdigest() == source["sha256"]
        assert "#guard_msgs in" in path.read_text(encoding="utf-8")
        old = previous.get(source["file"])
        if old and old["sha256"] == source["sha256"] and old["exit_code"] == 0:
            receipts.append(old)
            print(path.name, "PREVIOUS_PASS", flush=True)
            continue
        command = [str(ROOT / "toolchain" / "bin" / "lean.exe"), "-j1", "-M1536", "--tstack=400000", str(path)]
        start = time.monotonic()
        peak = 0
        with (REG / (path.name + ".log")).open("wb") as log:
            process = subprocess.Popen(command, cwd=REG, stdout=log, stderr=subprocess.STDOUT)
            monitor = psutil.Process(process.pid)
            while process.poll() is None:
                try:
                    peak = max(peak, monitor.memory_info().rss)
                except psutil.NoSuchProcess:
                    pass
                if peak > 2100 * 1024**2 or time.monotonic() - start > 90:
                    process.kill()
                    raise RuntimeError(f"Regression resource budget exceeded: {path.name}")
                time.sleep(0.05)
            code = process.wait()
        output = (REG / (path.name + ".log")).read_text(encoding="utf-8")
        row = dict(source, command=command, exit_code=code, seconds=round(time.monotonic()-start,3), peak_rss_bytes=peak, output=output)
        receipts.append(row)
        print(path.name, "EXIT", code, "PEAK_MIB", round(peak/1024**2,2), output, flush=True)
        (OUT / "regression_receipts.json").write_text(json.dumps(receipts, ensure_ascii=False, indent=2), encoding="utf-8")
        if code:
            raise SystemExit(code)
    print("OFFICIAL_STRUCTURAL_SOUNDNESS_REGRESSIONS=PASS", len(receipts), flush=True)

if __name__ == "__main__":
    main()
