import concurrent.futures
import hashlib
import json
import pathlib
import requests
import subprocess

ROOT = pathlib.Path(__file__).parent
MODULES = {
    "Main", "Statements", "Supplements.Kernels.MainTheorems", "Supplements.Kernels.MainTheoremsAll",
    "Development.AutomorphicArithmetic.CharacterBoxes.MainConclusion",
    "Development.AutomorphicArithmetic.ThetaCorrespondence.ThetaPairLifts.LocalTypeDictionary.DiscreteSpectrumResidualClassification",
    "Development.AutomorphicArithmetic.ThetaCorrespondence.ThetaPairLifts.LocalTypeDictionary.DoublingMethodOfEisensteinFacts",
    "Development.AutomorphicArithmetic.ThetaCorrespondence.ThetaPairLifts.LocalTypeDictionary.MemberHodgeHypOfLocalInputsRationalWeights",
    "Development.AutomorphicArithmetic.ThetaCorrespondence.ThetaPairLifts.ThirdPlaceSeries.BernsteinUnitaryProductIrreducible",
    "Development.AutomorphicArithmetic.ThetaCorrespondence.ThetaPairLifts.ThirdPlaceSeries.EveryCharacterOfLiteratureOfVWin",
    "Development.AutomorphicArithmetic.ThetaCorrespondence.ThetaPairLifts.ThirdPlaceSeries.MemberBundlesLargeUnramifiedExponents",
    "Development.AbelianVarietyTheory.Definitions.AutomorphicMembership.OverIx",
    "Development.AbelianVarietyTheory.Definitions.AutomorphicMembership.NotGeoClFalse",
    "Development.AbelianVarietyTheory.Definitions.AutomorphicMembership.SecondChernDegreeVanishesTrueSurfaces",
    "Development.AbelianVarietyTheory.Definitions.GlobalTwisting.SetUnipotentTranslate",
    "Development.AbelianVarietyTheory.Proofs.GlobalInterpolation.RealTiedSetDiv",
    "Development.AbelianVarietyTheory.Proofs.IwasawaDecomposition.TupPinsOfMuIsW",
    "Development.AbelianVarietyTheory.Proofs.IwasawaDecomposition.DivisionGeometryScalarsTransferSetDivision",
    "Development.WeilBound.RepresentationTheoryGL.EisensteinResidues.AnisotropicGlobalForms.DmOfHyp",
    "Formalism.LocalToGlobal.LatticeGeometry.Inhabited",
    "Formalism.LocalToGlobal.LatticeGeometry.GeoTiedP",
    "Formalism.LocalRingCardinality.SpanPowerMembership.NZRowD",
    "Formalism.LocalRingCardinality.KernelPlaceMeanBound",
    "Formalism.SharpRestriction.Divisibility.SlopeExcess.HeightBoundOfComponentBounds",
    "Formalism.SharpRestriction.Divisibility.SlopeExcess.ConstRankBaseLePolyFourth",
    "Formalism.LocalToGlobal.Divisibility.RecBridge",
    "Formalism.LocalToGlobal.Divisibility.RecBridgeMkF",
}

def main():
    global MODULES
    extended = ROOT / "bfs_path_modules.json"
    if extended.exists():
        MODULES = set(json.loads(extended.read_text(encoding="utf-8")))
    selected = []
    with (ROOT / "modules.jsonl").open(encoding="utf-8") as stream:
        next(stream)
        for line in stream:
            record = json.loads(line)
            if record[0] in MODULES:
                selected.append(record)
    if {r[0] for r in selected} != MODULES:
        raise RuntimeError("Missing module records")
    cache = ROOT / "artifacts"
    cache.mkdir(exist_ok=True)
    def fetch(row):
        module, dep_hash, artifact, expected = row
        path = cache / artifact
        url = f"https://rh-cache.taucetiproject.org/artifacts/leanprover-community/riemann-hypothesis/{artifact[:-5]}.art"
        if not path.exists():
            response = requests.get(url, timeout=45)
            response.raise_for_status()
            if len(response.content) > 32 * 1024 * 1024:
                raise RuntimeError("Single archive exceeds the targeted-download budget")
            if hashlib.sha256(response.content).hexdigest() != expected:
                raise RuntimeError("Archive checksum mismatch")
            path.write_bytes(response.content)
        elif hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise RuntimeError("Local archive checksum mismatch")
        return {"module": module, "hash": dep_hash, "archive": artifact, "sha256": expected, "bytes": path.stat().st_size, "url": url}
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        records = list(executor.map(fetch, selected))
    (ROOT / "selected_oleans.json").write_text(json.dumps(records, indent=2), encoding="utf-8")
    jobs = []
    for record in records:
        relative = pathlib.Path(*record["module"].split("."))
        bases = [str(ROOT / "project" / ".lake" / "build" / suffix / relative.parent) for suffix in ("lib/lean", "ir")]
        for base in bases:
            pathlib.Path(base).mkdir(parents=True, exist_ok=True)
        jobs.append({"file": str(cache / record["archive"]), "hash": record["hash"], "base": bases})
    result = subprocess.run([str(ROOT / "toolchain" / "bin" / "leantar.exe"), "--jobs", "2", "-f", "-x", "-j", "-"], input=json.dumps(jobs), text=True, capture_output=True)
    print("DECOMPRESS_EXIT", result.returncode, result.stdout, result.stderr)
    result.check_returncode()
    print("SELECTED_MODULES", len(records), "COMPRESSED_BYTES", sum(r["bytes"] for r in records))

if __name__ == "__main__":
    main()
