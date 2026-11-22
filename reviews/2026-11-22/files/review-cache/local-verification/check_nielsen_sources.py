import collections
import hashlib
import json
import pathlib
import re
import subprocess

ROOT = pathlib.Path(__file__).parent
OUT = ROOT / "trust-audit"
SOURCE = ROOT.parents[1] / "upstream-rh"
NAMES = ["geoOf_surf", "secondChernDegree_vanishes_trueSurfaces", "degCh2_eq_zero", "geoTied", "formsTieX", "degree_value_of_determinant", "anyGeometry", "GeoCl", "degHH_def", "every_character_of_green_v_win", "zero_free_all_of_green_v_win", "zeroFreeAll_of_topG", "nonempty_hyps_definite_side_of_closed_bound", "forall_goal_of_shape_of_hyps", "shape_closed_link_n_of_green", "closed_linkDIVt_of_closed_bridge_kernel", "zeroFreeOn_of_tiedWin_cyc"]

def git(*args):
    result = subprocess.run(["git", *args], cwd=SOURCE, capture_output=True, encoding="utf-8", text=True)
    if result.returncode not in (0,1):
        raise RuntimeError(result.stderr)
    return result.stdout

def main():
    pattern = r"\b(?:" + "|".join(NAMES) + r")\b"
    raw = git("grep", "--threads=2", "-n", "-z", "-P", "-e", pattern, "HEAD", "--", "src/*.lean")
    records = []
    for line in raw.splitlines():
        path, number, text = line.split("\0",2)
        records.append({"path":path.removeprefix("HEAD:"),"line":int(number),"text":text})
    (OUT / "paper_source_occurrences.json").write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding="utf-8")
    summary = {}
    for name in NAMES:
        hits = [r for r in records if re.search(r"\b"+name+r"\b",r["text"])]
        summary[name] = {"occurrences":sum(len(re.findall(r"\b"+name+r"\b",r["text"])) for r in hits),"lines":len(hits),"files":len({r['path'] for r in hits})}
        print(name,summary[name])
    source_diff = git("diff", "--name-status", "7cbf7a0c32fca1badf05931879a37c3f8a2b03b4", "712a6aef8fe265fb6f3a5fa1f3101a017aec8fe9", "--", "src")
    (OUT / "paper-source-diff.txt").write_text(source_diff,encoding="utf-8")
    print("PAPER_SOURCE_DIFF",repr(source_diff))
    ranges = {
        "src/Formalism/SharpRestriction/Divisibility/PlaceRankTwoOne.lean": [(95,98),(123,146),(349,356)],
        "src/Formalism/LocalToGlobal/LatticeGeometry/Inhabited.lean": [(241,306),(829,861)],
        "src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/TupPinsOfMuIsW.lean": [(155,166),(178,213)],
        "src/Development/AbelianVarietyTheory/Definitions/GlobalTwisting/SetUnipotentTranslate.lean": [(25,31),(379,401)],
        "src/Formalism/LocalRingCardinality/KernelPlaceMeanBound.lean": [(20,29)],
        "src/Formalism/SharpRestriction/Divisibility/SlopeExcess/HeightBoundOfComponentBounds.lean": [(136,150)],
        "src/Formalism/LocalToGlobal/Divisibility/RecBridge.lean": [(120,141)],
    }
    excerpts=[]
    for path, spans in ranges.items():
        text=git("show","HEAD:"+path)
        lines=text.splitlines()
        excerpts.append({"path":path,"sha256_lf":hashlib.sha256(text.encode()).hexdigest(),"ranges":[{"start":a,"end":b,"text":"\n".join(f"{i}: {lines[i-1]}" for i in range(a,b+1))} for a,b in spans]})
    (OUT / "paper_source_excerpts.json").write_text(json.dumps(excerpts,ensure_ascii=False,indent=2),encoding="utf-8")
    (OUT / "paper_source_counts.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding="utf-8")
    goals=set(NAMES[9:])
    modules=[]
    for row in records:
        for name in goals:
            if re.search(r"\b(?:theorem|def|abbrev)\s+(?:[\w.]+\.)?"+name+r"\b",row["text"]):
                modules.append(row["path"].removeprefix("src/").removesuffix(".lean").replace("/","."))
    (OUT / "paper_route_modules.json").write_text(json.dumps(sorted(set(modules)),indent=2),encoding="utf-8")
    print("PAPER_ROUTE_MODULES",len(set(modules)))

if __name__=="__main__":
    main()
