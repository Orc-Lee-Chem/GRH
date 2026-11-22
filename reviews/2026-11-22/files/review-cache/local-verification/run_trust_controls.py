import json
import pathlib
import subprocess
import time
import psutil

ROOT = pathlib.Path(__file__).parent
OUT = ROOT / "trust-audit"

def run(filename):
    command = [str(ROOT / "toolchain" / "bin" / "lean.exe"), "-j1", "-M1536", filename]
    start = time.monotonic()
    peak = 0
    with (OUT / (filename + ".log")).open("wb") as log:
        process = subprocess.Popen(command, cwd=ROOT, stdout=log, stderr=subprocess.STDOUT)
        monitor = psutil.Process(process.pid)
        while process.poll() is None:
            try:
                peak = max(peak, monitor.memory_info().rss)
            except psutil.NoSuchProcess:
                pass
            if peak > 2100 * 1024**2 or time.monotonic() - start > 90:
                process.kill()
                raise RuntimeError("Control exceeded resource budget")
            time.sleep(0.05)
        code = process.wait()
    text = (OUT / (filename + ".log")).read_text(encoding="utf-8")
    print(filename, "EXIT", code)
    print(text)
    return {"command": command, "exit_code": code, "seconds": round(time.monotonic()-start,3), "peak_rss_bytes": peak, "output": text}

def main():
    OUT.mkdir(exist_ok=True)
    valid = run("TrustControls.lean")
    assert valid["exit_code"] == 0
    assert "'TrustControls.extraAxiom' depends on axioms: [missingFact]" in valid["output"]
    assert "'TrustControls.incomplete' depends on axioms: [sorryAx]" in valid["output"]
    assert "'TrustControls.Shadowed.fakeRH' does not depend on any axioms" in valid["output"]
    invalid = run("RejectWrongGoal.lean")
    assert invalid["exit_code"] != 0 and "Type mismatch" in invalid["output"]
    receipt = {"all_controls_passed": True, "acceptance_controls": valid, "wrong_goal_rejected": invalid,
               "scope": "Tests of local checking distinctions on isolated examples; no new RH kernel replay."}
    (OUT / "controls_receipt.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=2), encoding="utf-8")
    print("TRUST_CONTROLS=PASS")

if __name__ == "__main__":
    main()
