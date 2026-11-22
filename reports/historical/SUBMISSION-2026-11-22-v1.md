> **CORRECTION (2026-11-22):** An independent review found real errors in the earlier submission and showed that the earlier "final theorem is vacuous / does not prove GRH" conclusion was too strong. See [CORRECTION.md](CORRECTION.md). The formal proof of the standard `RiemannHypothesis` stands; the degenerate definitions are an internal/faithfulness issue, not by themselves a formal-validity disproof.
# Submission for independent review: the Alpöge/Claude GRH Lean archive

**Purpose of this file.** I am asking a reviewer (GPT or a human) to check the claims below
against the Lean source and the proof-term evidence. This is not a claim that Lean is unsound.
The claim is narrower: **the main proof term reaches vacuous definitions, and the real
Siegel–Eisenstein simple-pole proposition is never proved in the archive.**

Date: 2026-11-22
Archive: Levent Alpöge / Claude, Lean 4 formalization of GRH, announced 2026-11-20.
Lean: 4.33.1. Mathlib: `0df444a360eaa60ab8c11dca51a86af692955474`.

---

## Reviewer instructions (read before judging)

**Do not rely only on the excerpts below.** Open the original archive and verify the paths
yourself. If you cannot access the repository or the web, say so explicitly and mark the
affected claims as “source excerpt only, not independently checked”.

Original material:

- Full mirror: <https://github.com/CocoSgt/riemann-hypothesis-lean>
- Comparator copy: <https://github.com/leanprover-community/riemann-hypothesis>
- Alpöge archive parts: <https://alpo.ge/lean.tar.gz.part01> … `.part14`
  (the Hexagon guide reports SHA-256 of the joined archive
  `9631b4f020199e580ba86178cb56c6e9b09f690c2369a80dc4334aa93f49c7fc`; this is
  guide-reported, not independently recomputed here)
- Source copy audited here: commit `7cbf7a0c32fca1badf05931879a37c3f8a2b03b4`

Minimum verification commands:

```bash
git clone https://github.com/CocoSgt/riemann-hypothesis-lean
cd riemann-hypothesis-lean
git checkout 7cbf7a0c32fca1badf05931879a37c3f8a2b03b4

# 1. literal True slot
grep -RIn "UnusedSlot72" src
grep -RIn "siegelEisensteinSimplePole" src

# 2. real definition
sed -n '1,40p' \
  src/Development/AbelianVarietyTheory/PublishedTheorems/SiegelWeil₂/SiegelEisensteinSimplePoleOfDoublingMethod.lean

# 3. all occurrences of the real name
grep -RIn "SiegelEisensteinSimplePole" src

# 4. exact-conclusion search
grep -RInE "theorem .*: *GlobalTheory\\.Published\\.SiegelEisensteinSimplePole|theorem .*: *Published\\.SiegelEisensteinSimplePole" src
```

Web/literature searches to run independently:

- `"SiegelEisensteinSimplePole"`
- `"UnusedSlot72" Lean`
- `Siegel Eisenstein series simple pole U(n,n)`
- `Tan Poles of Siegel Eisenstein Series on U(n,n)`
- `Kudla Rallis doubling method Siegel Eisenstein pole`
- `openai/math quasi Riemann hypothesis`
- `OpenAI 722 mathematics quasi-Riemann`

For the mathematical comparison, check at least:

- V. Tan, *Poles of Siegel Eisenstein Series on U(n,n)*, Canad. J. Math. 51 (1999).
- Kudla–Rallis / doubling method (Kudla’s Park City notes).
- Gan–Qiu–Takeda, regularized Siegel–Weil formula.

Required output format:

| Claim | Source/location | Independently verified? | Verdict |
|---|---|---|---|

For each of the seven claims in §0, mark `verified`, `refuted`, or `unresolved`. In
particular, do not accept “the real proposition is unproved” from this file alone: run the
exact-conclusion search and inspect every occurrence of `SiegelEisensteinSimplePole`.

---


## 0. Claims to verify

1. `GlobalTheory.Published.UnusedSlot72` is defined as `True`.
2. The field `siegelEisensteinSimplePole` in the main hypothesis bundle has type
   `UnusedSlot72`, not the real Siegel-pole proposition.
3. The real proposition `GlobalTheory.Published.SiegelEisensteinSimplePole` is defined in the
   archive but **no theorem proves it**; it occurs only as a hypothesis/field and in
   conditional theorems.
4. In the proof term of `rhOfAll`, the following constants are reachable:
   `UnusedSlot72`, `siegel_eisenstein_simple_pole`, `anyGeometry`, `geoDegenerate`, `divXFl`,
   `exists_divT`, `divEx_prov`.
5. `anyGeometry` is `fun _ _ _ => True`; `geoDegenerate` is a degenerate `DV.Geo` with
   `vol=0`, `Cl=PUnit`, all geometric predicates `True`; `divXFl` is a `DivX` with
   `CurveM=PUnit`, `degM=0`, `iMj=0`.
6. `OpenLiteratureStatements` is a 3-field structure, not a set of 60 unchecked axioms; most
   literature fields are Lean theorems. The problem is the vacuous objects, not “Lean assumed
   the cited theorems”.
7. OpenAI’s 2026 `openai/math` release (quasi-Riemann hypothesis / Landau–Siegel zero) does
   not prove this Siegel–Eisenstein pole statement. The Alpöge/Claude archive is a different
   work.

---

## 1. Environment and method

- Project: `E:\rh`
- Lean: `C:\Users\OrcLeeChem\.elan\toolchains\leanprover--lean4---v4.33.1`
- Project cache: 175,178 modules restored; 9 missing modules compiled from source.
- The machine has **16.6 GB physical RAM** (not 32 GB). A full `lake build Main` reached
  65,926/65,960 and OOM’d. Therefore I did **not** complete a local `#print axioms` on `Main`.
- Instead I read the `.olean` files directly with `Lean.readModuleData`, dumped value edges,
  and ran BFS from `rhOfAll`:
  - 175,179 `.olean` files scanned
  - 1,919,524 value edges
  - 1,309,474 constants reachable from `rhOfAll`
  - all seven target constants reached

This is a **proof-term dependency graph**, not source-level grep. It does not itself typecheck
the proof; kernel acceptance is taken from the community/independent verification (see §7).

---

## 2. The `True` slot: exact source

### 2.1 `UnusedSlot72`

`src/Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/LocalTypeDictionary/DiscreteSpectrumResidualClassification.lean:7`

```lean
abbrev GlobalTheory.Published.UnusedSlot72 : Prop := True
```

### 2.2 The main bundle uses it

`src/Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/ThirdPlaceSeries/BernsteinUnitaryProductIrreducible.lean:74`

```lean
siegelEisensteinSimplePole : _root_.GlobalTheory.Published.UnusedSlot72
```

### 2.3 The proof of the slot

`src/Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/ThirdPlaceSeries/EveryCharacterOfLiteratureOfVWin.lean:505`

```lean
theorem UpperTheory.LiteratureTheorems.siegel_eisenstein_simple_pole
    (O : _root_.UpperTheory.LiteratureTheorems.OpenLiteratureStatements) :
    GlobalTheory.Published.UnusedSlot72 :=
  trivial
```

`published_results_eigen` (same file, line 666) fills the 60-field structure and at line 718
assigns:

```lean
siegelEisensteinSimplePole :=
  (_root_.UpperTheory.LiteratureTheorems.siegel_eisenstein_simple_pole O)
```

So the “Siegel pole” field is proved by `trivial`.

---

## 3. The real Siegel-pole proposition is defined but not proved

### 3.1 Real definition

`src/Development/AbelianVarietyTheory/PublishedTheorems/SiegelWeil₂/SiegelEisensteinSimplePoleOfDoublingMethod.lean:14`

```lean
def GlobalTheory.Published.SiegelEisensteinSimplePole : Prop :=
  ∀ (D : D7) (V : HSp D), 0 < V.rank →
  ∀ a : GL (Fin V.rank) (AE D), IsMaj V a →
  HasIwasawa D.sp.cm.sig (dblSp V).gram (Khat V a) →
  ∀ (μ : (AE D)ˣ → Circle) (b : ℕ),
    IsHeckeChar D μ → ResEta D μ b →
    ∀ (s₀ : ℂ) (φ : GA D (dblSp V) → ℂ),
      φ ∈ degPS V a μ s₀ →
      V.rank < b →
      EisPoleLE V (flat V a φ s₀) (((b : ℂ) - V.rank) / 2) 1
```

In words: for every global CM datum and Hermitian space `V` of positive rank, every
majorizable `a`, Iwasawa condition, Hecke character `μ` with `ResEta D μ b`, and every
`φ ∈ degPS V a μ s₀`, if `b > rank V`, then the Siegel Eisenstein series attached to
`flat V a φ s₀` has a pole of order at most 1 at `(b - rank V)/2`.

### 3.2 No theorem proves it

Search command:

```powershell
git -C E:\rh grep -n ': *GlobalTheory.Published.SiegelEisensteinSimplePole\|: *Published.SiegelEisensteinSimplePole\|: *SiegelEisensteinSimplePole' -- 'src/**/*.lean'
```

Results:

- fields in `GeneralHyps.lean`, `BhattScholzeCrystallineLattices.lean`,
  `DiscreteSeriesCoefficientsCuspidal.lean`, `HypothesisBundleConversions.lean`;
- `simplePole_iff` in `EisPoleLEZeroOfLt.lean:46` — proves an **equivalence**; its forward direction assumes `Published.SiegelEisensteinSimplePole`;
- `eisRegularAt_one` in `EisPoleLEZeroOfLt.lean:58` — assumes it as a hypothesis;
- conditional theorems `SiegelEisensteinSimplePole → ...`;
- no unconditional theorem with conclusion `Published.SiegelEisensteinSimplePole`.

`eisPoleLEZeroOfLt` proves only `EisPoleLE ... 0` for `2 * rank < b` (order 0), not the
order-1 statement for the full range `rank < b`.

**Claim: the archive never proves the real Siegel-pole proposition.**

---

## 4. Proof-term reachability: the `True` slot is in the headline proof

Method: `DumpEdges.lean` reads every `.olean`, dumps each constant's value edges to
`edges.tsv`; `bfs_edges.py` builds an SQLite graph (`edges.db`) and BFS from `rhOfAll`.
Raw log: `bfs2.log`.

Result:

```text
done visited 1309474 seen 1309474
targets:
  Formalism.L2.Geo.divXFl
  Formalism.L2.Geo.geoDegenerate
  GlobalTheory.Mem.Top.Bl.anyGeometry
  GlobalTheory.Mem.Top.DivRec.divEx_prov
  GlobalTheory.Mem.Top.DivRec.exists_divT
  GlobalTheory.Published.UnusedSlot72
  UpperTheory.LiteratureTheorems.siegel_eisenstein_simple_pole
```

Shortest paths:

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

```text
... -> UpperTheory.LiteratureTheorems.every_character_of_literature_of_vWin
 -> UpperTheory.LiteratureTheorems.published_results_eigen
 -> UpperTheory.LiteratureTheorems.siegel_eisenstein_simple_pole
```

```text
... -> nonempty_hyps_definite_side_of_closed_bound
 -> GlobalTheory.Fc.S0.StageU.hypotheses_nonempty_of_unramified_exponents_alt
 -> GlobalTheory.T.large_unramified_exponent_bundles_exist_alt
 -> GlobalTheory.Fc.StageOneU.member_bundles_large_unramified_exponents_alt
 -> GlobalTheory.T.compatibleSystem_member_rationalWeights
 -> GlobalTheory.Mem.member_hodgeHyp_of_localInputs_rationalWeights
 -> GlobalTheory.Published.UnusedSlot72
```

```text
... -> nonempty_hyps_definite_side_of_closed_bound
 -> ... -> GlobalTheory.Mem.Top.Closing.divEx_geoCl
 -> GlobalTheory.Mem.Top.DivRec.divEx_of_ox
 -> GlobalTheory.Mem.Top.DivRec.divEx_prov
 -> GlobalTheory.Mem.Top.DivRec.exists_divT
 -> GlobalTheory.Mem.Top.DivRec.geoOver_stages
 -> Formalism.L2.Geo.divXFl
 -> Formalism.L2.Geo.geoDegenerate
```

---

## 5. The other vacuous objects

### 5.1 `anyGeometry`

`src/Development/AbelianVarietyTheory/Definitions/AutomorphicMembership/OverIx.lean:19`

```lean
abbrev GeoP : Type 1 := ∀ D : D7, Formalism.L2.Pj.Core D → DivX D → Prop
def anyGeometry : GeoP := fun _ _ _ => True
```

No geometric object; the predicate is always true.

### 5.2 `geoDegenerate`

`src/Formalism/LocalToGlobal/LatticeGeometry/Inhabited.lean:241`

Key fields:

```lean
Var := ℕ
Eff := fun _ _ => True
H0 := fun _ _ => ⊤
Cl := fun _ => PUnit
nef := fun _ _ => True
big := fun _ _ => True
bpf := fun _ _ _ => True
phiBir := fun _ _ _ => True
phiNoContr := fun _ _ _ _ => True
vanishOn := fun _ _ _ _ => True
pts := fun _ _ => PUnit
vol := fun _ _ => 0
```

It is a toy `DV.Geo`: “variety” is just `ℂ`, all divisors are effective/nef/big, the class
group is trivial, volume is zero.

### 5.3 `divXFl`

`src/Formalism/LocalToGlobal/LatticeGeometry/Inhabited.lean:829`

```lean
def divXFl : DivX D :=
  { X0 with
    geo := geoDegenerate D.what₂.LL D.what₂.Tau
    ...
    CurveM := fun _ _ _ _ _ _ => PUnit
    degM := fun _ _ _ _ _ _ _ _ => 0
    iMj := fun j _ => (0 : (X0.MjH j).V →ₗ[D.what₂.LL] D.what₂.LL)
    iMj_mem := fun _ _ _ => Submodule.mem_top }
```

Curve moduli is a point, degree is zero, cycle map is zero.

### 5.4 `exists_divT` / `divEx_prov`

`src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/TupPinsOfMuIsW.lean:178,204`

```lean
`exists_divT` constructs a witness and verifies several conditions. `divEx_prov` calls it
through `StepW.of_all`; `trivial` solves only one component. Their statements mention
`anyGeometry`, but the whole proofs are not `rfl`/`trivial`.

---

## 6. What is actually assumed (important correction)

`OpenLiteratureStatements` is a **3-field** structure:

`src/Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/ThirdPlaceSeries/EveryCharacterOfLiteratureOfVWin.lean:215`

```lean
structure UpperTheory.LiteratureTheorems.OpenLiteratureStatements : Prop where
  caraianiLocalGlobalDual : UpperTheory.One.M.Row
  localLanglandsExists : UpperTheory.Zero.LLC.RecTExists
  galoisRepOfPolarizedPairLit : UpperTheory.One.M.Row
```

`UpperTheory.One.M.Row` is:

`src/Development/AutomorphicArithmetic/Foundations/UnitarySphericalFixing/SatakeParameters/RecT.lean:6`

```lean
def UpperTheory.One.M.Row : Prop :=
  UpperTheory.GalStar.Row0b fun h rc => UpperTheory.Zero.LLC.IsRecT h rc
```

`MainConclusion.lean:7-14` constructs it with the explicit `h : Row0b` and the proved
`recTExists`:

```lean
theorem UpperTheory.FinalTheorems.everyCharacter_of_row
    (h : UpperTheory.GalStar.Row0b ...) : UpperTheory.EveryCharacter :=
  UpperTheory.LiteratureTheorems.every_character_of_literature_of_vWin
    ⟨h, UpperTheory.Zero.LLC.recTExists, h⟩ (UpperTheory.One.vwin_of_row h)

theorem UpperTheory.FinalTheorems.everyCharacter : UpperTheory.EveryCharacter :=
  UpperTheory.FinalTheorems.everyCharacter_of_row
    UpperTheory.Gal.Int.galoisLocalGlobalStrong_recParameter
```

So the 60-field bundle is constructed, not assumed. Most named fields correspond to Lean
theorems. The problem is the **objects**, not unchecked citation.

---

## 7. Known mathematics and recent work

### 7.1 The real statement is a known *type* of theorem

- V. Tan, *Poles of Siegel Eisenstein Series on U(n,n)*, Canad. J. Math. 51 (1999):
  normalized Siegel Eisenstein series on `U(n,n)` has at most simple poles at integers or
  half-integers in a certain strip.
  <https://www.cambridge.org/core/journals/canadian-journal-of-mathematics/article/poles-of-siegel-eisenstein-series-on-un-n/27F8B3E634321A156A2225A7CC2E5598>
- Kudla–Rallis / doubling method: meromorphic continuation and pole control.
  <https://www.math.utoronto.ca/skudla/kyoto.pdf>
- Gan–Qiu–Takeda: regularized Siegel–Weil formula and second-term identities.

The archive’s exact formal statement may be a specialization of these results, but **it is not
proved in the archive**, and I have not verified a paper-level equivalence of every definition
(`EisPoleLE`, `flat`, `degPS`, `IsMaj`, `HasIwasawa`, `ResEta`). That is a task for a specialist.

### 7.2 OpenAI’s 2026 `openai/math`

OpenAI released 722 manuscripts (372 families) in October 2026. The headline number-theory
result is the **quasi-Riemann hypothesis**: zero-free region `Re(s) > 7/8` for Dirichlet
L-functions and exclusion of Landau–Siegel zeros. It is not full GRH and not the
representation-theoretic Siegel–Eisenstein simple-pole statement.

- <https://github.com/openai/math>
- <https://eu.36kr.com/en/p/4015128916676736>

I found no public evidence in `openai/math` that it proves `SiegelEisensteinSimplePole` or fills
`UnusedSlot72`.

### 7.3 Alpöge/Claude archive

This is the archive audited here, not the OpenAI release. Independent Lean community checks
report that the archive compiles and is accepted by Lean’s kernel and independent kernels
(Sutherland / Lean Zulip, per the Hexagon guide).

The Hexagon reader’s guide independently states:

> “One field of the first bundle, `siegelEisensteinSimplePole`, is named after the simple pole
> of the Siegel Eisenstein series but has type `UnusedSlot72`, which is `True`, so it asserts
> nothing.”

- <https://hexagonmath.org/2611.00799v1>
- Nielsen, *The Invalidity of the Alpoge Proposed Proof of the Riemann Hypothesis*:
  <https://philarchive.org/rec/NIEIOT-2>

These are independent observations (the Hexagon guide is AI-generated, not peer-reviewed; the
Nielsen preprint is not peer-reviewed). They agree with the source-level finding.

---

## 8. Verdict

- **Formal Lean proof:** valid; no `sorry`/`axiom`/`native_decide`/`implemented_by` was found;
  the kernel accepts the archive (community/independent checks).
- **Mathematical content:** the proof term reaches `UnusedSlot72=True`,
  `anyGeometry=True`, `geoDegenerate`, `divXFl`, `exists_divT`, `divEx_prov`.
- **The real `SiegelEisensteinSimplePole`:** in the fixed archive, no explicit unconditional
  theorem was found; this is a search-scope result.
- **Historical conclusion (retracted):** the earlier “vacuous/weakened” conclusion is withdrawn;
  see `../../CONCLUSIONS.md`.

---

## 9. Limitations of this submission

- I did not complete a local `#print axioms` on `Main` (16.6 GB RAM; cache corruption); I rely
  on the community/independent kernel checks for kernel acceptance, and on the `.olean` graph
  for dependency reachability.
- The `.olean` graph is a value-edge graph; it does not typecheck. It is evidence of
  reachability, not a replacement for the kernel.
- The exact paper-level equivalence of the real `SiegelEisensteinSimplePole` with Tan/Kudla–
  Rallis statements is not certified here; a specialist should check it.
- The Hexagon guide and Nielsen preprint are not peer-reviewed.

---

## 10. Reproduction commands

```powershell
# 1. Build/restore cache (already done here)
cd E:\rh
lake exe cache get

# 2. Dump value edges from all .olean files
lake env lean --run DumpEdges.lean `
  E:\GRH-Lean-Check\olean_list.txt `
  E:\GRH-Lean-Check\edges.tsv

# 3. Build SQLite graph and BFS
python bfs_edges.py

# 4. Read the raw paths
Get-Content E:\GRH-Lean-Check\bfs2.log
```

Artifacts in the submission zip:

- `SUBMISSION.md` (this file)
- `evidence/OverIx.lean`, `evidence/Inhabited.lean`,
  `evidence/DiscreteSpectrumResidualClassification.lean`,
  `evidence/BernsteinUnitaryProductIrreducible.lean`,
  `evidence/EveryCharacterOfLiteratureOfVWin.lean`,
  `evidence/SiegelEisensteinSimplePoleOfDoublingMethod.lean`,
  `evidence/EisPoleLEZeroOfLt.lean`,
  `evidence/MainConclusion.lean`,
  `evidence/MainTheorems.lean`,
  `evidence/RecT.lean`,
  `evidence/WeightsConjBis.lean`,
  `evidence/TupPinsOfMuIsW.lean`
- `bfs2.log`, `scanmany3.log`, `dump_edges.log`
- `DumpEdges.lean`, `bfs_edges.py`, `InspectOlean.lean`
- `GRH_Lean_proof_term_findings.md`, `GRH_literature_statements.md`,
  `GRH_vacuous_objects.md`, `GRH_siegel_pole_and_recent_work.md`

Not included because they are multi-GB: `edges.tsv` (3.47 GB), `edges.db` (4.08 GB).
