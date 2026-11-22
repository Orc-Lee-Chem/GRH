# Correction after independent review

Date: 2026-11-22

An independent review (GPT, with repository access and web search) checked the submission in this
repository. It found several real errors in my earlier write-up and, more importantly, showed
that my final conclusion was too strong.

## Retracted conclusion

I previously wrote that the archive “does not prove GRH” and that the final theorem is
“vacuous”. **I retract that conclusion.**

The final theorem is:

`src/Main.lean:4`

```lean
theorem riemannHypothesis : RiemannHypothesis := rhOfAll
```

`RiemannHypothesis` is Mathlib’s actual Riemann Hypothesis statement, not a local `True`
placeholder. Independent comparator/kernel checks report that the theorem statement and proof
are accepted. On the evidence available, the archive is a **formal proof of the standard RH
statement**, assuming the kernel/checker results are correct.

## What remains correct

- `GlobalTheory.Published.UnusedSlot72` is `True`
  (`DiscreteSpectrumResidualClassification.lean:7`).
- The main bundle field `siegelEisensteinSimplePole` has type `UnusedSlot72`
  (`BernsteinUnitaryProductIrreducible.lean:74`), and its proof is `trivial`
  (`EveryCharacterOfLiteratureOfVWin.lean:505`).
- The real `GlobalTheory.Published.SiegelEisensteinSimplePole` is defined
  (`SiegelEisensteinSimplePoleOfDoublingMethod.lean:14`) but I found no explicit unconditional
  theorem proving it; this is a search result, not a proof that no indirect proof exists.
- `anyGeometry` is `fun _ _ _ => True`; `geoDegenerate` and `divXFl` have degenerate fields
  (`Cl = PUnit`, `vol = 0`, `CurveM = PUnit`, `degM = 0`, `iMj = 0`).
- A proof-term BFS from `rhOfAll` reaches those constants.

## What the review corrected

1. **`exists_divT` and `divEx_prov` are not “just `rfl`/`trivial`.”** Their proofs construct
   objects and call other theorems; my summary was wrong.
2. **`simplePole_iff` is an equivalence theorem**, not merely “assumes the real proposition”.
   My wording was wrong.
3. **BFS reachability is not semantic load-bearing.** A constant can occur in a proof term
   without being needed for the final result. In particular:
   `ResidueKilled.dm_of_two` has type `... → True → DM` and its proof is
   `intro hC hS _ D ...`, so it **ignores** the `True` argument.
   This undercuts my claim that the missing real Siegel-pole proof is a necessary gap.
4. **Comparator/kernel logs do not prove non-vacuity by themselves**, but they do verify the
   final statement/proof. The decisive point is that `Main.lean` states the actual
   `RiemannHypothesis`; the internal degenerate definitions do not by themselves change the
   final theorem’s statement.

## Corrected verdict

- **Formal Lean proof:** stands; no `sorry`/`axiom`/`native_decide`/`implemented_by` was found;
  independent checks report kernel acceptance. The archive is a formal proof of the standard RH
  statement, not a proof of a different `True`-theorem.
- **Degenerate definitions:** real, but they are internal scaffolding. I have **not** shown that
  the final theorem is semantically vacuous; the review’s point that `True` can be ignored is
  valid.
- **Real `SiegelEisensteinSimplePole`:** explicitly unproved in the public archive as far as my
  search goes, but **not shown to be necessary** for the final theorem.
- **Open question:** whether the proof is a faithful/explanatory formalization of the intended
  mathematics, and whether the degenerate objects are load-bearing in other branches. This is a
  quality/faithfulness question, not a formal-validity claim.

I am keeping the original reports for transparency, but this correction supersedes their
“hollow/not GRH” conclusion.
