from collections import deque
import hashlib
import json
import pathlib

ROOT = pathlib.Path(__file__).parent
TARGETS = ["GlobalTheory.Published.UnusedSlot72", "UpperTheory.LiteratureTheorems.siegel_eisenstein_simple_pole", "GlobalTheory.Mem.Top.Bl.anyGeometry", "Formalism.L2.Geo.geoDegenerate", "Formalism.L2.Geo.divXFl", "GlobalTheory.Mem.Top.DivRec.exists_divT", "GlobalTheory.Mem.Top.DivRec.divEx_prov"]

def main():
    constants = {}
    for line in (ROOT / "inspect.jsonl").read_text(encoding="utf-8").splitlines():
        row = json.loads(line)
        constants[row["constant"]["name"]] = row
    start = "rhOfAll"
    parents = {start: None}
    queue = deque([start])
    while queue:
        node = queue.popleft()
        for dependency in constants.get(node, {}).get("constant", {}).get("valueConstants", []):
            if dependency not in parents:
                parents[dependency] = node
                queue.append(dependency)
    paths = {}
    for target in TARGETS:
        if target not in parents:
            paths[target] = None
            continue
        path = []
        node = target
        while node is not None:
            path.append(node)
            node = parents[node]
        paths[target] = list(reversed(path))
    focused = {name: constants[name] for name in [*TARGETS, "riemannHypothesis", "ResidueKilled.dm_of_two"] if name in constants}
    result = {"source": "fresh local extraction of 32 selectively downloaded cache modules; not a local kernel replay", "constant_count": len(constants), "reachable_names_in_partial_graph": len(parents), "paths": paths, "focused": focused}
    (ROOT / "local_findings.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print("LOCALLY_REPRODUCED_TARGET_PATHS", sum(path is not None for path in paths.values()), "OF", len(TARGETS))
    for name, row in focused.items():
        record = row["constant"]
        print("CONSTANT", name, "TYPE", record["typeSketch"])
        if name == "ResidueKilled.dm_of_two":
            print("LAMBDA_USAGE", json.dumps(record["lambdaUsage"], ensure_ascii=False))
    print("DIRECT_MAIN_VALUE", constants["riemannHypothesis"]["constant"]["valueConstants"])
    if any(path is None for path in paths.values()):
        raise SystemExit(2)

if __name__ == "__main__":
    main()
