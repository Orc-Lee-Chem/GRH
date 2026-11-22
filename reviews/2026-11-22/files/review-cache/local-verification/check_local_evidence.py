import hashlib
import json
import pathlib
import subprocess
import time
import psutil

ROOT = pathlib.Path(__file__).parent
REPO = ROOT.parent.parent / "upstream-rh"
PIN = "7cbf7a0c32fca1badf05931879a37c3f8a2b03b4"
BASELINE = "e50d09817ad81469f737e8f637561e6ccf86c670"

def git(*args):
    return subprocess.check_output(["git", "-c", "core.quotePath=false", "-C", str(REPO), *args])

def main():
    diff = git("diff", "--name-status", PIN, BASELINE, "--", "src").decode("utf-8")
    if diff.strip() != "A\tsrc/Challenge.lean":
        raise RuntimeError("Cache baseline modifies the audited project source")
    (ROOT / "baseline-source-diff.txt").write_text(diff, encoding="utf-8")
    slot_path = "project/.lake/build/lib/lean/Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/LocalTypeDictionary/DiscreteSpectrumResidualClassification.olean"
    command = [str(ROOT / "toolchain/bin/lean.exe"), "-j1", "-M1024", "--run", "ReplaySlot.lean", slot_path]
    started = time.monotonic()
    peak = 0
    with (ROOT / "kernel-slot.log").open("wb") as log:
        process = subprocess.Popen(command, cwd=ROOT, stdout=log, stderr=subprocess.STDOUT)
        monitored = psutil.Process(process.pid)
        while process.poll() is None:
            try:
                peak = max(peak, monitored.memory_info().rss)
            except psutil.NoSuchProcess:
                pass
            time.sleep(0.05)
        code = process.wait()
    text = (ROOT / "kernel-slot.log").read_text(encoding="utf-8")
    expected = ["ORIGINAL_SLOT_KERNEL_REPLAY=PASS", "TRUE_INTRO_HAS_ORIGINAL_SLOT_TYPE=PASS", "MALFORMED_FALSE_PROOF_REJECTED=PASS"]
    if code or any(line not in text for line in expected):
        raise RuntimeError("Kernel control failed")
    excerpts = {}
    queries = {
        "height_formula": ("src/Development/AbelianVarietyTheory/Definitions/GlobalTwisting/SetUnipotentTranslate.lean", [(25, 31), (379, 406)]),
        "height_estimates": ("src/Formalism/SharpRestriction/Divisibility/SlopeExcess/HeightBoundOfComponentBounds.lean", [(136, 152)]),
        "vacuous_geometry_closure": ("src/Development/AbelianVarietyTheory/Definitions/AutomorphicMembership/NotGeoClFalse.lean", [(21, 28)]),
        "empty_lattice_witness": ("src/Formalism/LocalRingCardinality/SpanPowerMembership/NZRowD.lean", [(14, 39)]),
        "divisor_witnesses": ("src/Formalism/LocalToGlobal/LatticeGeometry/Inhabited.lean", [(694, 703), (829, 861)]),
    }
    for label, (path, ranges) in queries.items():
        lines = git("show", PIN + ":" + path).decode("utf-8").splitlines()
        excerpts[label] = {"path": path, "commit": PIN, "url": "https://github.com/CocoSgt/riemann-hypothesis-lean/blob/" + PIN + "/" + path,
            "ranges": [{"start": a, "end": b, "text": "\n".join(f"{i+1}: {lines[i]}" for i in range(a-1, min(b,len(lines))))} for a,b in ranges]}
    record = {"kernel_command": command, "kernel_exit_code": code, "kernel_seconds": time.monotonic() - started, "kernel_peak_rss_bytes": peak,
        "kernel_output": text, "baseline_source_diff": diff, "source_excerpts": excerpts}
    (ROOT / "additional_checks.json").write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
    print(text)
    print("BASELINE_SOURCE_DIFF", diff.strip())
    print("SLOT_CHECK_SECONDS", record["kernel_seconds"], "PEAK_RSS_BYTES", peak)

if __name__ == "__main__":
    main()
