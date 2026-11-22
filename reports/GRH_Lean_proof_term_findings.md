# GRH Lean proof-term audit — final

Date: 2026-11-22

## Verdict

**Not a Lean soundness bug. A vacuous formalization.**

The archive is kernel-valid Lean: the source scan found no `sorry`, `admit`, `axiom`,
`native_decide`, `implemented_by` or extra axiom; the community check reports only
`propext`, `Classical.choice`, `Quot.sound`. But the proof term of `rhOfAll` reaches every one of
the suspect placeholder definitions. In particular, a structure field typed as `True` is used in the
headline proof, and `anyGeometry` / `geoDegenerate` / `divXFl` are on explicit proof-term paths from
`rhOfAll`.

So the theorem proved is **a vacuous/weakened variant**, not a non-vacuous formalization of GRH.

## Method: proof-term graph, no imports

I could not load `Main.olean` locally: this machine has 16.6 GB RAM (not 32 GB), and a full
`lake build Main` reached 65,926/65,960 then OOM. Instead I read the `.olean` files directly with
`Lean.readModuleData`, dumped every constant's value edges, and ran a BFS from `rhOfAll`.

- 175,179 `.olean` files scanned
- 1,919,524 value edges
- 1,309,474 constants reachable from `rhOfAll`
- every suspect reached

This bypasses imports and corrupt `.olean` files and gives the **actual transitive proof-term
dependency graph**, not source-level guesses.

## Exact reachability paths

Shortest path to `anyGeometry`:

```text
rhOfAll
 -> allChi
 -> UpperTheory.FinalTheorems.everyCharacter
 -> UpperTheory.FinalTheorems.everyCharacter_of_row
 -> UpperTheory.LiteratureTheorems.every_character_of_literature_of_vWin
 -> UpperTheory.Lit.every_character_of_theta_integrals_local_matching
 -> UpperTheory.Lit.nonempty_hyps_definite_side_of_closed_bound
 -> GlobalTheory.Mem.Top.Bl.anyGeometry
```

Path to `UnusedSlot72` (the `True` slot):

```text
... -> every_character_of_literature_of_vWin
 -> every_character_of_theta_integrals_local_matching
 -> nonempty_hyps_definite_side_of_closed_bound
 -> GlobalTheory.Fc.S0.StageU.hypotheses_nonempty_of_unramified_exponents_alt
 -> GlobalTheory.T.large_unramified_exponent_bundles_exist_alt
 -> GlobalTheory.Fc.StageOneU.member_bundles_large_unramified_exponents_alt
 -> GlobalTheory.T.compatibleSystem_member_rationalWeights
 -> GlobalTheory.Mem.member_hodgeHyp_of_localInputs_rationalWeights
 -> GlobalTheory.Published.UnusedSlot72
```

Path to `siegel_eisenstein_simple_pole`:

```text
... -> every_character_of_literature_of_vWin
 -> UpperTheory.LiteratureTheorems.published_results_eigen
 -> UpperTheory.LiteratureTheorems.siegel_eisenstein_simple_pole
```

Path to `divXFl` / `geoDegenerate`:

```text
... -> nonempty_hyps_definite_side_of_closed_bound
 -> GlobalTheory.Fc.S0.StageU.hypotheses_nonempty_of_unramified_exponents_alt
 -> ... -> GlobalTheory.Mem.Top.Closing.divEx_geoCl
 -> GlobalTheory.Mem.Top.DivRec.divEx_of_ox
 -> GlobalTheory.Mem.Top.DivRec.divEx_prov
 -> GlobalTheory.Mem.Top.DivRec.exists_divT
 -> GlobalTheory.Mem.Top.DivRec.geoOver_stages
 -> Formalism.L2.Geo.divXFl
 -> Formalism.L2.Geo.geoDegenerate
```

`exists_divT` and `divEx_prov` are on that same path.

## The vacuous definitions

| Constant | Definition | Role in proof term |
|---|---|---|
| `GlobalTheory.Published.UnusedSlot72` | `True` | reached via `member_hodgeHyp...`; also field `siegelEisensteinSimplePole` |
| `UpperTheory.LiteratureTheorems.siegel_eisenstein_simple_pole` | proof by `trivial` | reached via `published_results_eigen` |
| `GlobalTheory.Mem.Top.Bl.anyGeometry` | `fun _ _ _ => True` | reached directly via `nonempty_hyps_definite_side_of_closed_bound` |
| `Formalism.L2.Geo.geoDegenerate` | geometric fields `True`; `vol=0`; `H0=⊤` | reached via `divXFl` |
| `Formalism.L2.Geo.divXFl` | `iMj=0`, `degM=0`, `CurveM=PUnit`, `geo=geoDegenerate` | reached via `geoOver_stages` |
| `GlobalTheory.Mem.Top.DivRec.exists_divT` / `divEx_prov` | `rfl` / `trivial`; statements use `anyGeometry` | reached via `divEx_of_ox` / `geoOver_stages` |

## What is and is not established

- **Established:** the proof term that Lean checks for `rhOfAll` transitively contains these
  placeholder definitions. This is stronger than "the names appear in imports".
- **Established:** the formal theorem named `RiemannHypothesis` is proved in Lean without
  `sorry`/extra axioms (community certification + source scan).
- **Not established:** that the intended mathematical objects (geometry, Siegel pole, etc.) are
  non-vacuous. They are not: the formalization replaces them with `True`/zero placeholders.
- **Therefore:** this is not a proof of GRH in the ordinary mathematical sense. It is a proof of a
  formally weakened statement whose key geometric hypotheses are vacuous.

## Local environment

- Lean 4.33.1:
  `C:\Users\OrcLeeChem\.elan\toolchains\leanprover--lean4---v4.33.1`
- Project: `E:\rh`
- Cache restored: 175,178 modules / 99.3 GB
- 9 modules missing from cache compiled from source
- Full `Main` build OOM at 16.6 GB physical RAM; proof-term graph used instead
- Artifacts:
  - `E:\GRH-Lean-Check\edges.tsv` (3.47 GB, 1,919,524 edges)
  - `E:\GRH-Lean-Check\edges.db` (SQLite graph)
  - `E:\GRH-Lean-Check\bfs2.log` (paths)
  - `E:\rh\DumpEdges.lean`, `E:\rh\IndexBFS.lean`, `E:\rh\InspectOlean.lean`
