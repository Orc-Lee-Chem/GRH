"""Read-only source and public-receipt audit; never execute repository code."""
import concurrent.futures
import datetime
import hashlib
import json
import pathlib
import re
import subprocess
import requests

ROOT = pathlib.Path(__file__).parent
OUT = ROOT / "trust-audit"
SOURCE = ROOT.parents[1] / "upstream-rh"
PIN = "7cbf7a0c32fca1badf05931879a37c3f8a2b03b4"
MATHLIB_PIN = "0df444a360eaa60ab8c11dca51a86af692955474"
URLS = {
    "mit_index.html": "https://math.mit.edu/~drew/grh/",
    "mit_audit.log": "https://math.mit.edu/~drew/grh/audit.log",
    "con-leche-compare.log": "https://math.mit.edu/~drew/grh/con-leche-compare.log",
    "con-ron-compare.log": "https://math.mit.edu/~drew/grh/con-ron-compare.log",
    "nanoda.log": "https://math.mit.edu/~drew/grh/nanoda.log",
    "comparator.json": "https://math.mit.edu/~drew/grh/comparator.json",
    "sandbox-build.sh": "https://math.mit.edu/~drew/grh/sandbox-build.sh",
    "sandbox-timeline.txt": "https://math.mit.edu/~drew/grh/sandbox-timeline.txt",
    "SHA256SUMS": "https://math.mit.edu/~drew/grh/SHA256SUMS",
    "mathlib_RiemannZeta.lean": f"https://raw.githubusercontent.com/leanprover-community/mathlib4/{MATHLIB_PIN}/Mathlib/NumberTheory/LSeries/RiemannZeta.lean",
    "mathlib_DirichletContinuation.lean": f"https://raw.githubusercontent.com/leanprover-community/mathlib4/{MATHLIB_PIN}/Mathlib/NumberTheory/LSeries/DirichletContinuation.lean",
    "mathlib_DirichletBasic.lean": f"https://raw.githubusercontent.com/leanprover-community/mathlib4/{MATHLIB_PIN}/Mathlib/NumberTheory/DirichletCharacter/Basic.lean",
    "lean_Environment.lean": "https://raw.githubusercontent.com/leanprover/lean4/819816b2e0a3bf405af45ae5c7af2491d8f5bee6/src/Lean/Environment.lean",
    "author_publications.html": "https://philpeople.org/profiles/jenny-lorraine-nielsen/publications?iframe=true&order=added",
    "paper_latest": "https://philarchive.org/archive/NIEIOT-2v14",
    "paper_www": "https://www.philarchive.org/archive/NIEIOT-2v14",
    "paper_download": "https://philarchive.org/archive/NIEIOT-2v14?download=1",
}
PATTERNS = {
    "axioms_sorry": r"\b(?:axiom|sorry|sorryAx|admit)\b",
    "native_evaluation": r"\b(?:native_decide|bv_decide)\b|\bdecide\s+\+native\b|Lean\.(?:trustCompiler|ofReduceBool|ofReduceNat)",
    "unsafe_ffi": r"\b(?:unsafe|implemented_by|extern)\b",
    "metaprogramming": r"\b(?:initialize|builtin_initialize|elab_rules|macro_rules|macro|elab|syntax|run_tac|run_elab|addDecl|setEnv|modifyEnv|skipKernelTC)\b|#eval|Lean\.Environment",
    "critical_definitions": r"^\s*(?:(?:noncomputable|private|protected|unsafe)\s+)*(?:def|abbrev|opaque|axiom|theorem|inductive|structure)\s+(?:_root_\.)?(?:RiemannHypothesis|riemannZeta|DirichletCharacter|Real|Complex|Nat)(?:\s|\.|:|\{|\(|$)",
    "options": r"^\s*set_option\b",
}

def fetch(item):
    name, url = item
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    try:
        response = requests.get(url, timeout=30, headers={"User-Agent": "Mozilla/5.0"})
        row = {"url": url, "retrieved_utc": started, "status": response.status_code,
               "final_url": response.url, "bytes": len(response.content),
               "sha256": hashlib.sha256(response.content).hexdigest()}
        if len(response.content) > 8 * 1024 * 1024:
            raise RuntimeError("Response exceeds small-file budget")
        if response.ok:
            (OUT / name).write_bytes(response.content)
            if response.content.startswith(b"%PDF"):
                from pypdf import PdfReader
                pdf = OUT / (name + ".pdf")
                pdf.write_bytes(response.content)
                reader = PdfReader(pdf)
                pdf.with_suffix(".txt").write_text("\n\n".join(f"PAGE {i+1}\n{p.extract_text()}" for i, p in enumerate(reader.pages)), encoding="utf-8")
                row["pdf_pages"] = len(reader.pages)
        return name, row
    except Exception as exc:
        return name, {"url": url, "retrieved_utc": started, "error": str(exc)}

def main():
    OUT.mkdir(exist_ok=True)
    identity = subprocess.run(["git", "rev-parse", "HEAD"], cwd=SOURCE, capture_output=True, text=True, check=True).stdout.strip()
    assert identity == PIN, identity
    status = subprocess.run(["git", "status", "--porcelain"], cwd=SOURCE, capture_output=True, text=True, check=True).stdout
    assert not status, status
    if (OUT / "http_receipts.json").exists():
        receipts = json.loads((OUT / "http_receipts.json").read_text(encoding="utf-8"))
    else:
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
            receipts = dict(pool.map(fetch, URLS.items()))
        (OUT / "http_receipts.json").write_text(json.dumps(receipts, ensure_ascii=False, indent=2), encoding="utf-8")
    matches = {}
    for category, pattern in PATTERNS.items():
        command = ["git", "grep", "--threads=2", "-n", "-z", "-P", "-e", pattern, "HEAD", "--", "src/*.lean"]
        result = subprocess.run(command, cwd=SOURCE, capture_output=True, text=True, encoding="utf-8")
        if result.returncode not in (0, 1):
            raise RuntimeError(result.stderr)
        records = []
        for line in result.stdout.splitlines():
            location, number, content = line.split("\0", 2)
            records.append({"path": location.removeprefix("HEAD:"), "line": int(number), "text": content})
        (OUT / (category + ".json")).write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
        matches[category] = {"line_count": len(records), "file_count": len({r['path'] for r in records}), "pattern": pattern, "command": command}
        print("SCANNED", category, len(records), "lines", flush=True)
    files = subprocess.run(["git", "ls-files", "--", "src/*.lean", "src/**/*.lean"], cwd=SOURCE, capture_output=True, text=True, encoding="utf-8", check=True).stdout.splitlines()
    assert len(files) == 175187, len(files)
    reserved = [p for p in files if re.match(r"src/(Mathlib|Init|Lean|Std|Lake)(/|\.lean$)", p)]
    summary = {"source_commit": identity, "source_clean": not bool(status), "lean_file_count": len(files), "reserved_module_paths": reserved, "lexical_scans": matches,
               "warning": "Lexical scans include comments and strings; zero hits are not a proof of semantic absence. Public receipts are external evidence, not local full kernel replay."}
    (OUT / "source_scan.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    print("HTTP", json.dumps({n: {k:v for k,v in r.items() if k in ('status','error','pdf_pages','bytes')} for n,r in receipts.items()}, ensure_ascii=False))

if __name__ == "__main__":
    main()
