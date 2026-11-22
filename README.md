# GRH Lean audit materials

This repository contains an independent audit of the Alpöge/Claude Lean 4 formalization of the
Riemann hypothesis. It is **not** the official archive and **not** a claim that Lean is unsound.

## Main finding

The Lean proof is kernel-valid (community/independent checks), but the proof term reaches
vacuous/degenerate definitions:

- `GlobalTheory.Published.UnusedSlot72 := True`
- `GlobalTheory.Mem.Top.Bl.anyGeometry := fun _ _ _ => True`
- `Formalism.L2.Geo.geoDegenerate` — `vol = 0`, `Cl = PUnit`, all geometric predicates `True`
- `Formalism.L2.Geo.divXFl` — `CurveM = PUnit`, `degM = 0`, `iMj = 0`

The real `GlobalTheory.Published.SiegelEisensteinSimplePole` is defined in the archive but is
not proved; the main bundle replaces its field with `UnusedSlot72`.

More precisely:

- The archive **never proves** the real `SiegelEisensteinSimplePole`.
- The main bundle uses `UnusedSlot72` for that field.
- A proof-term BFS from `rhOfAll` reaches `UnusedSlot72`, `siegel_eisenstein_simple_pole`,
  `anyGeometry`, `geoDegenerate`, `divXFl`, `exists_divT`, `divEx_prov`.

## Files

- `SUBMISSION.md` — full self-contained review submission.
- `REVIEWER_PROMPT.md` — prompt for an independent reviewer (requires repository/web access
  for `verified` claims).
- `reports/GRH_Lean_proof_term_findings.md` — proof-term BFS findings.
- `reports/GRH_literature_statements.md` — restored literature statements/classification.
- `reports/GRH_vacuous_objects.md` — restored vacuous objects.
- `reports/GRH_siegel_pole_and_recent_work.md` — real Siegel-pole proposition and recent work.
- `reports/REPORT.md` — original source-level audit.
- `evidence/` — source excerpts for every key claim.
- `logs/` — raw BFS and scan logs.
- `scripts/` — `DumpEdges.lean`, `InspectOlean.lean`, `bfs_edges.py`, `Check.lean`.

## Reproduction

The full repository is large (about 1 GB source; cache about 100 GB), so it is not included here.
See `SUBMISSION.md` for the exact Alpöge/Claude archive and mirror links.

Minimal proof-term reproduction (given the archive and `.olean` files):

```powershell
lake env lean --run scripts/DumpEdges.lean `
  olean_list.txt edges.tsv
python scripts/bfs_edges.py
Get-Content logs/bfs2.log
```

`edges.tsv` and `edges.db` are multi-GB and are not included.

## Integrity

See `SHA256SUMS.txt`. Each file's SHA-256 is listed there.

## Caveat

- Kernel acceptance is taken from the community/independent checks cited in `SUBMISSION.md`;
  this repository does not contain a full local kernel replay.
- The exact paper-level equivalence of the real `SiegelEisensteinSimplePole` with known
  literature (Tan 1999, Kudla–Rallis) is marked for specialist review, not certified here.
