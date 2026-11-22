# Restored literature statements in the GRH Lean archive

Date: 2026-11-22

## 1. What is actually assumed, and what is proved

`UpperTheory.LiteratureTheorems.OpenLiteratureStatements` is **not** a list of 60 unproved
theorems. It is a 3-field `Prop` structure:

```lean
structure UpperTheory.LiteratureTheorems.OpenLiteratureStatements : Prop where
  caraianiLocalGlobalDual : UpperTheory.One.M.Row
  localLanglandsExists : UpperTheory.Zero.LLC.RecTExists
  galoisRepOfPolarizedPairLit : UpperTheory.One.M.Row
```

Source:
`src/Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/ThirdPlaceSeries/EveryCharacterOfLiteratureOfVWin.lean:215`

`UpperTheory.One.M.Row` is:

```lean
def UpperTheory.One.M.Row : Prop :=
  UpperTheory.GalStar.Row0b fun h rc => UpperTheory.Zero.LLC.IsRecT h rc
```

Source:
`src/Development/AutomorphicArithmetic/Foundations/UnitarySphericalFixing/SatakeParameters/RecT.lean:6`

So the two `Row` fields are the same substantial `Row0b` statement, not two independent
assumptions. `MainConclusion` constructs the structure with the explicit `h : Row0b` and the
proved `recTExists`; it is not an unchecked axiom.

## 2. What is `Row0b`?

`Row0b` is a genuine quantified proposition about CM fields, Hecke characters, cuspidal
representations, Galois representations, Hodge–Tate weights and local conditions:

```lean
def Row0b (Rc : ...) : Prop :=
  ∀ (E : Type) [Field E] [NumberField E] [IsCMField E]
    (l : ℕ) [Fact l.Prime] (ψ : Qbar l ≃* ℂ) (a : ℕ), 1 ≤ a →
    ∀ (π : CuspSub E a) (χ : HChar (maximalRealSubfield E)),
      (CG.mk π).IsRegAlg →
      GlobalTheory.ContraPair.PolarizedPair π χ →
      ∃ (r : G E ℂ → GL (Fin a) (Qbar l)) (wt : ℕ)
        (HT : (E →* Qbar l) → Multiset ℕ),
        PropsB Rc π ψ r wt HT
```

Source:
`src/Development/AutomorphicArithmetic/Foundations/GaloisRepresentations/TypeConditions/WeightsConjBis.lean:69`

This is not `True`. It is a strong existence statement. Whether it is a known theorem in this
generality is a separate mathematical question; the Lean proof of it goes through
`galoisRepresentations_of_thetaLift`, `GeoOne`, and `TLiftK`.

## 3. The 60 fields of `UnitaryGroupThirdPlaceHypotheses`

`GlobalTheory.Fc.S0.UnitaryGroupThirdPlaceHypotheses` is the 60-field structure used by
`published_results_eigen`. Its fields are **propositions** such as:

```lean
clozelCohomological : GlobalTheory.Published.ClozelCohomological
greenCuspidal : GlobalTheory.Published.GreenCuspidal
chebotarevDegreeOne : GlobalTheory.Published.ChebotarevDegreeOne
jacquetShalika : GlobalTheory.Published.JacquetShalika
harishChandraFinite : GlobalTheory.Published.HarishChandraFinite
casselmanWallach : GlobalTheory.Published.CasselmanWallach
bernsteinZelevinskyFiniteness : GlobalTheory.Published.BernsteinZelevinskyFiniteness
globalArtinReciprocity : GlobalTheory.Published.GlobalArtinReciprocity
bhattScholzeCrystallineLattices : GlobalTheory.Published.BhattScholzeCrystallineLattices
siegelEisensteinSimplePole : GlobalTheory.Published.UnusedSlot72
nLink : GlobalTheory.NLink.Hypotheses
toHypothesesX : GlobalTheory.NRows.GeometricGaloisRepCompatibility
```

Source:
`src/Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/ThirdPlaceSeries/BernsteinUnitaryProductIrreducible.lean:22`

`published_results_eigen` **constructs** this structure from the 3-field `O`, using one
`..._of_literature O` theorem per field. Those `..._of_literature` theorems are Lean theorems, not
axioms; most of them simply call a corresponding `..._holds` theorem.

## 4. Known vs unknown: first-pass classification

| Field / statement | Status |
|---|---|
| `ChebotarevDegreeOne` | known: Chebotarev density theorem |
| `JacquetShalika` | known: Jacquet–Shalika |
| `HarishChandraFinite`, `CasselmanWallach` | known |
| `BernsteinZelevinskyFiniteness` | known |
| `GlobalArtinReciprocity` | known |
| `BhattScholzeCrystallineLattices` | known (Bhatt–Scholze) |
| `DeRhamPotSemistable` | known (potentially semistable) |
| `CaraianiLocalGlobalDual`, `GaloisRepOfPolarizedPairLit` | **not standard in this full generality**; encoded as `Row0b`, a strong existence statement |
| `LocalGlobalAboveL` | conditional/partial; not a general theorem as stated |
| `SiegelEisensteinSimplePole` | **vacuous**: its type is `UnusedSlot72 := True`, proved by `trivial` |
| `LitN`, `ToHypothesesX`, `NLink` | strong/conditional; not known as stated |
| `MemberHodgeHyp...` | constructed from local inputs; not a classical theorem |

The names are suggestive, but the formal statements are not automatically identical to the
textbook theorems. A paper-level comparison would require checking each `Published.*` definition,
not just the theorem name.

## 5. The decisive problem

Even if every named field were a known theorem, the final proof still instantiates the geometric
layer with:

```lean
GlobalTheory.Mem.Top.Bl.anyGeometry := fun _ _ _ => True
Formalism.L2.Geo.geoDegenerate       -- geometric fields True, vol=0, H0=⊤
Formalism.L2.Geo.divXFl              -- iMj=0, degM=0, CurveM=PUnit
GlobalTheory.Published.UnusedSlot72  -- True
```

The proof-term BFS confirms all of these are reachable from `rhOfAll`:

```text
rhOfAll -> ... -> nonempty_hyps_definite_side_of_closed_bound
        -> anyGeometry
        -> ... -> member_hodgeHyp... -> UnusedSlot72
        -> published_results_eigen -> siegel_eisenstein_simple_pole
        -> ... -> divEx_prov -> exists_divT -> geoOver_stages
        -> divXFl -> geoDegenerate
```

Therefore:

- the cited literature theorems are **not** simply assumed without Lean checking;
- but the formal objects they are applied to are **vacuous**;
- The earlier “vacuous/weakened” conclusion is retracted; see current CONCLUSIONS.md.

## 6. Files

- `src/Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/ThirdPlaceSeries/EveryCharacterOfLiteratureOfVWin.lean`
- `src/Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/ThirdPlaceSeries/BernsteinUnitaryProductIrreducible.lean`
- `src/Development/AutomorphicArithmetic/Foundations/GaloisRepresentations/TypeConditions/WeightsConjBis.lean`
- `src/Formalism/LocalToGlobal/LatticeGeometry/Inhabited.lean`
- `src/Development/AbelianVarietyTheory/Definitions/AutomorphicMembership/OverIx.lean`
- `src/Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/LocalTypeDictionary/DiscreteSpectrumResidualClassification.lean`
