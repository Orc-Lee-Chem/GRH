# What the “vacuous objects” actually are

Date: 2026-11-22

## 1. `anyGeometry`

Source: `src/Development/AbelianVarietyTheory/Definitions/AutomorphicMembership/OverIx.lean:19`

```lean
abbrev GeoP : Type 1 := ∀ D : D7, Formalism.L2.Pj.Core D → DivX D → Prop

def anyGeometry : GeoP := fun _ _ _ => True
```

`GeoP` is a predicate saying “this point/divisor has a geometry”. `anyGeometry` makes that
predicate `True` for every `D`, every core, every divisor.

**Interpretation:** there is no geometric object here at all. It is the universal “yes” predicate.
It is not a known curve, variety, or geometric theorem.

## 2. `geoDegenerate`

Source: `src/Formalism/LocalToGlobal/LatticeGeometry/Inhabited.lean:241`

```lean
@[reducible] def geoDegenerate (F : Type) [Field F] [NumberField F] [StarRing F]
    (Tau : Type) [Fintype Tau] : DV.Geo F where
  Var := ℕ
  dim := fun N => Formalism.DegreeFormula.dimFl Tau N
  Fn := fun _ => F
  ...
  Eff := fun _ _ => True
  H0 := fun _ _ => ⊤
  ...
  KY := fun _ => 0
  Cl := fun _ => PUnit
  ...
  nef := fun _ _ => True
  big := fun _ _ => True
  bpf := fun _ _ _ => True
  phiBir := fun _ _ _ => True
  phiNoContr := fun _ _ _ _ => True
  vanishOn := fun _ _ _ _ => True
  ...
  pts := fun _ _ => PUnit
  vol := fun _ _ => 0
  ...
```

This is an instance of the `DV.Geo` interface with:

- “variety” `Var := ℕ` (just a type, not an algebraic variety);
- every effective divisor allowed (`Eff := True`);
- `H0 := ⊤`;
- class group `Cl := PUnit` (trivial);
- all divisors nef/big/bpf, all vanishing conditions true;
- no points (`pts := PUnit`) and volume `0`.

**Interpretation:** it is a **toy model** satisfying the interface by making every geometric
predicate true and every invariant zero. It is not a known curve or surface. In ordinary
mathematics, “every divisor is big” and “volume = 0” are not a consistent nondegenerate geometry;
this is a deliberately degenerate model.

## 3. `divXFl`

Source: `src/Formalism/LocalToGlobal/LatticeGeometry/Inhabited.lean:829`

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

`divXFl` is a `DivX` (divisor/curve data) whose:

- geometry is `geoDegenerate`;
- curve moduli `CurveM` is `PUnit` (a point);
- degree `degM` is `0`;
- the map `iMj` is the zero map.

**Interpretation:** it is a **degenerate divisor object** with no genuine curve, degree zero, and
zero cycle class. It is not a known curve/divisor. It is an interface filler.

## 4. `UnusedSlot72` and `siegel_eisenstein_simple_pole`

Source:
`src/Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/LocalTypeDictionary/DiscreteSpectrumResidualClassification.lean:7`

```lean
abbrev GlobalTheory.Published.UnusedSlot72 : Prop := True
```

Source:
`src/Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/ThirdPlaceSeries/EveryCharacterOfLiteratureOfVWin.lean:505`

```lean
theorem UpperTheory.LiteratureTheorems.siegel_eisenstein_simple_pole
    (O : OpenLiteratureStatements) : GlobalTheory.Published.UnusedSlot72 :=
  trivial
```

**Interpretation:** this is not the known theorem “Siegel Eisenstein series has a simple pole”.
It is the proposition `True`, proved by `trivial`. The name is a label for an empty slot.

## 5. `exists_divT` / `divEx_prov`

Source:
`src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/TupPinsOfMuIsW.lean`

`exists_divT` constructs a witness and verifies several conditions. `divEx_prov` calls it
through `StepW.of_all`; `trivial` solves only one component. Their statements mention
`anyGeometry`, but the whole proofs are not `rfl`/`trivial`.

**Interpretation:** these are not known existence theorems for divisors; they are immediate
consequences of the degenerate definitions.

## 6. What is actually a known theorem?

The 60-field `UnitaryGroupThirdPlaceHypotheses` contains names that do correspond to known
mathematics:

- Chebotarev density;
- Jacquet–Shalika;
- Harish-Chandra / Casselman–Wallach;
- Bernstein–Zelevinsky finiteness;
- Deligne–Ribet;
- global Artin reciprocity;
- Bhatt–Scholze crystalline lattices;
- de Rham / potentially semistable.

But:

- the formal statements may be stronger than the textbook versions;
- `CaraianiLocalGlobalDual` and `GaloisRepOfPolarizedPairLit` are **not** standard theorems in
  this full generality; they are encoded as the strong `Row0b`;
- the geometric inputs are `anyGeometry`/`geoDegenerate`/`divXFl`, which are not known objects;
- `UnusedSlot72` is not a theorem at all.

So the correct statement is:

> Some cited names are known theorems, but the **objects they are applied to** are synthetic
> degenerate models. The result is a valid Lean proof of a vacuous/weakened variant, not a proof
> of GRH.

## 7. Can we “restore” the intended objects?

We can read the interfaces (`DV.Geo`, `DivX`, `GeoP`) and see what a non-vacuous instance would
need: an actual curve/variety, a genuine class group, nonzero volume, a real curve moduli space,
and a nonzero cycle map. The archive does not provide these; it provides `PUnit`, `True`, `0`,
and `⊤`.

If one replaced `geoDegenerate`/`divXFl`/`anyGeometry` with genuine objects, the proofs that
currently go through `trivial`, `rfl`, `Submodule.mem_top`, and `PUnit` would no longer work. That
is exactly the sense in which the proof is hollow.

## 8. Historical bottom line (retracted)

The earlier “this proves a formally weakened statement, not GRH” conclusion is retracted.
See `../../CONCLUSIONS.md` for the current verdict: the final theorem is the standard Mathlib
RH statement; the degenerate objects are a faithfulness concern, not a demonstrated formal gap.

Files:
- `E:\GRH-Lean-Check\GRH_literature_statements.md`
- `E:\GRH-Lean-Check\GRH_Lean_proof_term_findings.md`
