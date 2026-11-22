# GRH Lean minimal source-level audit

Root: `C:\Users\OrcLeeChem\Documents\deepseek-harness\default-workspace\rhfull`

This is a **source-level** audit: `git grep HEAD` over all blobs. It does not build Lean
and does not inspect the compiled proof term.

## Suspect definitions

| Name | Definition site | References | In headline chain files? |
|---|---|---:|---|
| `anyGeometry` | `src/Development/AbelianVarietyTheory/Definitions/AutomorphicMembership/OverIx.lean:19` | 118 | yes: src/Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/ThirdPlaceSeries/HypothesesNonemptyOfUnramifiedExponents.lean, src/Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/ThirdPlaceSeries/SiegelEisensteinSecondTermHypotheses.lean |
| `geoDegenerate` | `src/Formalism/LocalToGlobal/LatticeGeometry/Inhabited.lean:241` | 11 | no |
| `divXFl` | `src/Formalism/LocalToGlobal/LatticeGeometry/Inhabited.lean:829` | 10 | no |
| `UnusedSlot72` | `src/Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/LocalTypeDictionary/DiscreteSpectrumResidualClassification.lean:7` | 12 | yes: src/Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/ThirdPlaceSeries/EveryCharacterOfLiteratureOfVWin.lean |
| `siegel_eisenstein_simple_pole` | `src/Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/ThirdPlaceSeries/EveryCharacterOfLiteratureOfVWin.lean:505` | 2 | yes: src/Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/ThirdPlaceSeries/EveryCharacterOfLiteratureOfVWin.lean |
| `exists_divT` | `src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/TupPinsOfMuIsW.lean:178` | 2 | no |
| `divEx_prov` | `src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/TupPinsOfMuIsW.lean:204` | 2 | no |

## Real counterparts

| Name | Definition site | References | In headline chain files? |
|---|---|---:|---|
| `geoOf` | `src/Development/AbelianVarietyTheory/Definitions/AutomorphicMembership/OverIx.lean:16` | 16 | no |
| `geoTrue` | `src/Development/AbelianVarietyTheory/Definitions/AutomorphicMembership/GeometrySectionsEqRiemannRoch.lean:21` | 19 | no |
| `IsGeoOf` | `src/Development/AbelianVarietyTheory/Definitions/AutomorphicMembership/LargeFor.lean:78` | 6 | no |
| `HasTrueSurf` | `src/Development/AbelianVarietyTheory/Definitions/AutomorphicMembership/SecondChernDegreeVanishesTrueSurfaces.lean:346` | 7 | no |
| `divXStd` | `src/Formalism/LocalRingCardinality/SpanPowerMembership/NZRowD.lean:14` | 5 | no |
| `levelRecordDivisor` | `src/Formalism/LocalRingCardinality/SpanPowerMembership/NZRowF.lean:171` | 7 | no |
| `fin_X` | `src/Formalism/LocalRingCardinality/SpanPowerMembership/NZRowZ.lean:57` | 8 | no |
| `SiegelEisensteinSimplePole` | `"src/Development/AbelianVarietyTheory/PublishedTheorems/SiegelWeil\342\202\202/SiegelEisensteinSimplePoleOfDoublingMethod.lean":14` | 14 | no |

## Direct references of selected suspects

### `anyGeometry`

- `src/Development/AbelianVarietyTheory/Definitions/AutomorphicMembership/GKeyFin.lean:22` — `prmR (NEa hL (GlobalTheory.HeightCounting.Up.NEl hL cDep) A) SExt.none (geoCl anyGeometry)`
- `src/Development/AbelianVarietyTheory/Definitions/AutomorphicMembership/MultW.lean:45` — `prmR (GlobalTheory.HeightCounting.Up.NEl hL cDep) SExt.none (geoCl anyGeometry)`
- `src/Development/AbelianVarietyTheory/Definitions/AutomorphicMembership/NotLamAreShift.lean:153` — `∃ l, Nonempty (OAt anyGeometry t ((GlobalTheory.ShFam.Pad.SurfSt.of X).put (setLam X l))) := by`
- `src/Development/AbelianVarietyTheory/Definitions/AutomorphicMembership/OverIx.lean:19` — `def anyGeometry : GeoP := fun _ _ _ => True`
- `src/Development/AbelianVarietyTheory/Definitions/AutomorphicMembership/ParMem.lean:137` — `@[reducible] def prm0 (hL : GlobalTheory.Published.LocalLanglandsGL) : Prm hL := prmR (NEb hL) SExt.none (geoCl anyGeometry)`
- `src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/LinkedBundleConstructionExists.lean:28` — `MemberE (prmR (NEa hL (GlobalTheory.HeightCounting.Up.NEo hL cDep) A) SExt.none (geoCl anyGeometry)).s ∧`
- `src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/LinkedBundleConstructionExists.lean:29` — `ExBL KPx (IsBuiltE (prmR (NEa hL (GlobalTheory.HeightCounting.Up.NEo hL cDep) A) SExt.none (geoCl anyGeometry)).s)`
- `src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/LinkedBundleConstructionExists.lean:30` — `(IsGoodE (prmR (NEa hL (GlobalTheory.HeightCounting.Up.NEo hL cDep) A) SExt.none (geoCl anyGeometry)).s)`
- `src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/LinkedBundleConstructionExists.lean:31` — `(IsLinked (prmR (NEa hL (GlobalTheory.HeightCounting.Up.NEo hL cDep) A) SExt.none (geoCl anyGeometry))) := by`
- `src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/LinkedBundleConstructionExists.lean:51` — `P.greenCuspidal hL (GlobalTheory.HeightCounting.Up.NEo hL cDep) SExt.none (geoCl anyGeometry)`
- `src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/LinkedBundleConstructionExists.lean:56` — `(GlobalTheory.T.movable_geometric hL cDep anyGeometry)⟩`
- `src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/LinkedBundleConstructionExistsStatement.lean:12` — `theorem _root_.GlobalTheory.T.linked_bundle_construction_exists : S0.HypothesesUE → S0.RowRat → ∀ (hL : GlobalTheory.Published.LocalLanglandsGL) (cDep : ℝ) (A : GroupRetwisting.AtP), EvLgG A → StandardLattice.SiegelMa...`
- `src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/NonemptyHypsOfPublishedUE.lean:30` — `theorem nonempty_hyps_of_classicalTheoremsUE : S0.HypothesesUE → S0.RowRat → ∀ (hL : GlobalTheory.Published.LocalLanglandsGL) (cDep : ℝ) (A : GroupRetwisting.AtP), EvLgG A → RL.At (prm1 hL cDep) (fun Q L => R1.Predica...`
- `src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/NonemptyHypsOfPublishedUE.lean:38` — `have hmono := GlobalTheory.Glob.open_and_linked_of_stronger_extension hL (GlobalTheory.HeightCounting.Up.NEl hL cDep) (NEa hL (GlobalTheory.HeightCounting.Up.NEo hL cDep) A) SExt.none (geoCl anyGeometry)`
- `src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/NonemptyHypsOfPublishedUE.lean:41` — `have hN' : RL.At (prmR (NEa hL (GlobalTheory.HeightCounting.Up.NEo hL cDep) A) SExt.none (geoCl anyGeometry)) (fun Q L => R1.PredicateAtBundlePoints Q L S0.NL) :=`
- `src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/OpenFirstParametersOfPublishedUE.lean:31` — `have hPA := GlobalTheory.T.entry_hPA_at_parameters hL (GlobalTheory.HeightCounting.Up.NEl hL cDep) SExt.none (geoCl anyGeometry)`
- `src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/OpenFirstParametersOfPublishedUE.lean:32` — `have hDc := GlobalTheory.T.entry_point_g_at_parameters hL (GlobalTheory.HeightCounting.Up.NEl hL cDep) SExt.none (geoCl anyGeometry)`
- `src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/OpenFirstParametersOfPublishedUE.lean:34` — `P.discreteSeriesExists P.harishChandraFinite P.cuspRapidDecay hL _ SExt.none (geoCl anyGeometry) hNE`
- `src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/OpenFirstParametersOfPublishedUE.lean:36` — `P.casselmanWallach P.harishChandraFinite P.cuspRapidDecay hL _ SExt.none (geoCl anyGeometry) hPA hDc hTie`
- `src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/OpenFirstParametersOfPublishedUE.lean:40` — `hL (GlobalTheory.HeightCounting.Up.NEl hL cDep) SExt.none (geoCl anyGeometry)`
- `src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/OpenFirstParametersOfPublishedUE.lean:42` — `P.discreteSeriesCover P.harishChandraModules P.casselmanWallach hL _ SExt.none (geoCl anyGeometry) hB hMi.1`
- `src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/OpenFirstParametersOfPublishedUE.lean:46` — `P.zelevinskyPolynomialRing P.geometricLemma P.greenCuspidal hL (GlobalTheory.HeightCounting.Up.NEl hL cDep) SExt.none (geoCl anyGeometry)`
- `src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/OpenFirstParametersOfPublishedUE.lean:51` — `hL _ SExt.none (geoCl anyGeometry) hLam`
- `src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/OpenFirstParametersOfPublishedUE.lean:53` — `P.depthZeroInertia hL (GlobalTheory.HeightCounting.Up.NEl hL cDep) SExt.none (geoCl anyGeometry) hNE`
- `src/Development/AbelianVarietyTheory/Proofs/DivisorProofs/OpenFirstParametersOfPublishedUE.lean:55` — `P.depthZeroInertia hL _ SExt.none (geoCl anyGeometry) hNE hGood.1`
- ... (93 more)

### `geoDegenerate`

- `src/Formalism/LocalToGlobal/LatticeGeometry/GeoTiedP.lean:154` — `ShimFam D (geoDegenerate D.what₂.LL D.what₂.Tau) PUnit where`
- `src/Formalism/LocalToGlobal/LatticeGeometry/Inhabited.lean:241` — `@[reducible] def geoDegenerate (F : Type) [Field F] [NumberField F] [StarRing F] (Tau : Type) [Fintype Tau] : DV.Geo F where`
- `src/Formalism/LocalToGlobal/LatticeGeometry/Inhabited.lean:310` — `(((geoDegenerate F Tau).inter N (fun _ => lam) : ℤ) : ℝ) =`
- `src/Formalism/LocalToGlobal/LatticeGeometry/Inhabited.lean:390` — `def algDegenerate (N : ℕ) : AlgPkg (geoDegenerate D.what₂.LL D.what₂.Tau) D.what₂.Tau N PUnit where`
- `src/Formalism/LocalToGlobal/LatticeGeometry/Inhabited.lean:397` — `degA := fun _ L => ((geoDegenerate D.what₂.LL D.what₂.Tau).inter N (fun _ => L) : ℝ)`
- `src/Formalism/LocalToGlobal/LatticeGeometry/Inhabited.lean:405` — `ShimU D (geoDegenerate D.what₂.LL D.what₂.Tau) jC ng1 w where`
- `src/Formalism/LocalToGlobal/LatticeGeometry/Inhabited.lean:414` — `show (((geoDegenerate D.what₂.LL D.what₂.Tau).inter w.N (fun _ => la) : ℤ) : ℝ) = 1 * _`
- `src/Formalism/LocalToGlobal/LatticeGeometry/Inhabited.lean:483` — `(NW : ℕ → ℕ) (algW : ∀ j, AlgPkg (geoDegenerate D.what₂.LL D.what₂.Tau) D.what₂.Tau (NW j) PUnit.{1})`
- `src/Formalism/LocalToGlobal/LatticeGeometry/Inhabited.lean:485` — `FormsPkg D (geoDegenerate D.what₂.LL D.what₂.Tau) NW (fun _ => PUnit.{1}) algW PtY where`
- `src/Formalism/LocalToGlobal/LatticeGeometry/Inhabited.lean:567` — `ShimFam D (geoDegenerate D.what₂.LL D.what₂.Tau) PUnit where`
- `src/Formalism/LocalToGlobal/LatticeGeometry/Inhabited.lean:831` — `geo := geoDegenerate D.what₂.LL D.what₂.Tau`

### `divXFl`

- `src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/TupPinsOfMuIsW.lean:164` — `refine ⟨divXFl D jc X₀, fun _ _ => True, ⟨divXFl D jc X₀, (divXFl D jc X₀).iMj, (divXFl D jc X₀).iMj_mem, rfl⟩,`
- `src/Formalism/LocalToGlobal/LatticeGeometry/GeoTiedP.lean:183` — `⟨divXFl D jc X0, famFlJ D jc KO eO kL kL_eO, fun p _ => Equiv.refl _, fun _ _ _ => Equiv.refl _,`
- `src/Formalism/LocalToGlobal/LatticeGeometry/Inhabited.lean:829` — `def divXFl : DivX D :=`
- `src/Formalism/LocalToGlobal/LatticeGeometry/Inhabited.lean:868` — `theorem tiedX_fl : TiedX (jC := jC) (ng := ng1) (divXFl D jC X0) (fun _ => Finset.univ.image D.host.g)`
- `src/Formalism/LocalToGlobal/LatticeGeometry/Inhabited.lean:902` — `theorem prov_divXFl_nonempty : Nonempty (IntegralModelsLocalData.Prov D (divXFl D jC X0)) := by`
- `src/Formalism/LocalToGlobal/LatticeGeometry/Inhabited.lean:907` — `refine ⟨settingVarietiesOverData (divXFl D jC X0) I dat hI (fun w => shimUFl D jC w) (fun S κ hS => ?_)⟩`
- `src/Formalism/LocalToGlobal/LatticeGeometry/Inhabited.lean:908` — `let w := (shimuraDatumOfSetting (divXFl D jC X0) S κ hS).1`
- `src/Formalism/LocalToGlobal/LatticeGeometry/Inhabited.lean:909` — `have hw : w.Indef := (shimuraDatumOfSetting (divXFl D jC X0) S κ hS).2`
- `src/Formalism/LocalToGlobal/LatticeGeometry/Inhabited.lean:916` — `have e : (divXFl D jC X0).shv S κ = (divXFl D jC X0).shv (dat i).S (dat i).κ :=`
- `src/Formalism/LocalToGlobal/LatticeGeometry/Inhabited.lean:919` — `exact ⟨tieOf (divXFl D jC X0) _ (prime_of_mem_image D) _ (tiedX_fl D jC X0).shv`

### `UnusedSlot72`

- `src/Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/LocalTypeDictionary/BernsteinUnitaryProductIrreducibleBis.lean:198` — `siegelEisensteinSimplePole : _root_.GlobalTheory.Published.UnusedSlot72`
- `src/Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/LocalTypeDictionary/BernsteinUnitaryProductIrreducibleTer.lean:64` — `siegelEisensteinSimplePole : _root_.GlobalTheory.Published.UnusedSlot72`
- `src/Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/LocalTypeDictionary/DiscreteSpectrumResidualClassification.lean:7` — `abbrev GlobalTheory.Published.UnusedSlot72 : Prop := True`
- `src/Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/LocalTypeDictionary/DoublingMethodOfEisensteinFacts.lean:7` — `theorem _root_.GlobalTheory.T.doubling_zeta_of_eisenstein_facts : GlobalTheory.Published.CuspRapidDecay → GlobalTheory.Published.SiegelEisensteinContinuation → _root_.GlobalTheory.Published.UnusedSlot72 → _root_.Globa...`
- `src/Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/LocalTypeDictionary/GeometricLemma.lean:73` — `siegelEisensteinSimplePole : _root_.GlobalTheory.Published.UnusedSlot72`
- `src/Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/LocalTypeDictionary/MemberHodgeHypOfLocalInputsRationalWeights.lean:12` — `theorem member_hodgeHyp_of_localInputs_rationalWeights : _root_.GlobalTheory.Mem.LiteralAutomorphy.MemberHypotheses → GlobalTheory.Published.HarishChandraModules → GlobalTheory.Published.DiscreteSeriesCover → GlobalTh...`
- `src/Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/LocalTypeDictionary/MemberHodgeHypOfLocalInputsRationalWeights.lean:22` — `theorem _root_.GlobalTheory.T.compatibleSystem_member_rationalWeights : _root_.GlobalTheory.Mem.LiteralAutomorphy.MemberHypotheses → GlobalTheory.Published.HarishChandraModules → GlobalTheory.Published.DiscreteSeriesC...`
- `src/Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/LocalTypeDictionary/TwistedSiegelWeilIdentityOfFormula.lean:13` — `GlobalTheory.Published.SiegelEisensteinContinuation → _root_.GlobalTheory.Published.UnusedSlot72 →`
- `src/Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/LocalTypeDictionary/TwistedSiegelWeilIdentityOfFormula.lean:25` — `theorem _root_.GlobalTheory.T.twisted_siegel_weil_identity : GlobalTheory.Hk3.HoweUnram → GlobalTheory.Published.CuspRapidDecay → GlobalTheory.Published.HarishChandraFinite → GlobalTheory.Published.HarishChandraModule...`
- `src/Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/LocalTypeDictionary/TwistedSiegelWeilIdentityOfSiegelWeilFormula.lean:12` — `GlobalTheory.Published.SiegelEisensteinContinuation → _root_.GlobalTheory.Published.UnusedSlot72 →`
- `src/Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/ThirdPlaceSeries/BernsteinUnitaryProductIrreducible.lean:74` — `siegelEisensteinSimplePole : _root_.GlobalTheory.Published.UnusedSlot72`
- `src/Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/ThirdPlaceSeries/EveryCharacterOfLiteratureOfVWin.lean:505` — `theorem UpperTheory.LiteratureTheorems.siegel_eisenstein_simple_pole (O : _root_.UpperTheory.LiteratureTheorems.OpenLiteratureStatements) : GlobalTheory.Published.UnusedSlot72 :=`

### `siegel_eisenstein_simple_pole`

- `src/Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/ThirdPlaceSeries/EveryCharacterOfLiteratureOfVWin.lean:505` — `theorem UpperTheory.LiteratureTheorems.siegel_eisenstein_simple_pole (O : _root_.UpperTheory.LiteratureTheorems.OpenLiteratureStatements) : GlobalTheory.Published.UnusedSlot72 :=`
- `src/Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/ThirdPlaceSeries/EveryCharacterOfLiteratureOfVWin.lean:718` — `siegelEisensteinSimplePole := (_root_.UpperTheory.LiteratureTheorems.siegel_eisenstein_simple_pole O)`

### `exists_divT`

- `src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/TupPinsOfMuIsW.lean:178` — `theorem exists_divT {𝒮 : Slots} {K : Ctx} (w : ColW B f T) (pin : ColPin w) (Z : w.Lt) (l : Lv4 𝒮 K w Z) :`
- `src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/TupPinsOfMuIsW.lean:206` — `let ⟨Y, h1, h2, h3, h4⟩ := exists_divT w hpin.some Z l`

### `divEx_prov`

- `src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/TupPinsOfMuIsW.lean:204` — `theorem divEx_prov (𝒮 : Slots) (hOx : 𝒮.Ox = OX anyGeometry) : DivEx 𝒮 :=`
- `src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/TupPinsOfMuIsW.lean:213` — `fun _ _ _ 𝒮 hOx => divEx_prov 𝒮 hOx`

## What this shows

- The suspect definitions exist and are `True`/`Empty`/degenerate in the source.
- The real counterparts exist, but the headline chain files do not textually reference them.
- The headline chain files do reference `anyGeometry` / `siegel_eisenstein_simple_pole`,
  but not `geoDegenerate`/`divXFl` directly; those are referenced by their consumers
  (`exists_divT`, `divEx_prov`, `divEx_geoCl`, `memberE_closing`).

## What this does NOT show

- It does not show whether the suspects occur in the **compiled proof term** of
  `riemannHypothesis`; that requires a build/export + constant census.
- It does not show whether they are load-bearing; that requires ablation/replacement
  with the real counterparts.
