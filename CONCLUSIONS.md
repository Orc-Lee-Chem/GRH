# Conclusions

Date: 2026-11-22

## Scope

The archive's stated target is the Riemann zeta function and Dirichlet L-functions (the GRH
range used here). This is not a claim about GRH for arbitrary global or automorphic
L-functions.

## Verdict

**The formal proof is very likely correct. The earlier “vacuous / does not prove GRH”
conclusion was too strong and is retracted.**

`src/Main.lean` proves the standard Mathlib statement:

```lean
theorem riemannHypothesis : RiemannHypothesis := rhOfAll
```

Independent kernel/comparator records report that this statement and proof are accepted, with
only `propext`, `Classical.choice`, `Quot.sound`. We found no `sorry`, extra axiom,
`native_decide`, or `implemented_by` in the audited source. On the available evidence, this is a
formal proof of the standard RH statement, not a proof of a local `True` placeholder.

## What we found

### Degenerate internal definitions

- `GlobalTheory.Published.UnusedSlot72 := True`
  (`DiscreteSpectrumResidualClassification.lean:7`)
- The main bundle's `siegelEisensteinSimplePole` field has type `UnusedSlot72`
  (`BernsteinUnitaryProductIrreducible.lean:74`), and its proof is `trivial`
  (`EveryCharacterOfLiteratureOfVWin.lean:505`).
- `anyGeometry := fun _ _ _ => True`
  (`OverIx.lean:19`).
- `geoDegenerate` has `vol = 0`, `Cl = PUnit`, and many `True` fields
  (`Inhabited.lean:241`).
- `divXFl` has `CurveM = PUnit`, `degM = 0`, `iMj = 0`
  (`Inhabited.lean:829`).

These are real facts. The question is whether they **invalidate the final theorem**. We have not
shown that they do.

### The real Siegel pole

The real

```lean
def GlobalTheory.Published.SiegelEisensteinSimplePole : Prop := ...
```

is defined in
`SiegelEisensteinSimplePoleOfDoublingMethod.lean:14`.

An exact-name source search found no **explicit unconditional theorem** with this conclusion.
It occurs as a hypothesis/field and in conditional theorems. This is a search result: it does
not prove that no equivalent or indirect derivation exists.

### Is it load-bearing?

A proof-term BFS from `rhOfAll` reaches `UnusedSlot72`, `siegel_eisenstein_simple_pole`,
`anyGeometry`, `geoDegenerate`, `divXFl`, `exists_divT`, `divEx_prov`. That is **syntactic
reachability**, not semantic necessity.

Counterexample to “reachable = necessary”: `ResidueKilled.dm_of_two` has type
`... → True → DM` and its proof is `intro hC hS _ D ...`; the `True` argument is ignored.
So at least one path does not need the real Siegel-pole proposition.

## What we believe

- **Formal validity:** high confidence. The final statement is the standard Mathlib RH statement,
  and independent checks support kernel acceptance. We do not claim a local full replay.
- **Mathematical faithfulness:** still open. The degenerate definitions and the absence of an explicit unconditional proof of the named
  Siegel proposition in the fixed archive are a quality/explanation concern. They do not, by themselves, show the
  final theorem is false or that the standard statement is not established.
- **The real `SiegelEisensteinSimplePole`:** in the fixed public archive, an exact-name search
  found no explicit unconditional theorem; this is a search-scope result, not a claim that no
  proof exists. Its exact role and literature equivalence remain for specialist review.
- **Recent work:** OpenAI’s 2026 quasi-RH work is a different result (zero-free region /
  Landau–Siegel), not this Siegel-pole statement. No public evidence was found that it fills this
  slot.

## One-sentence summary

> We audited the archive, found degenerate internal definitions and no explicit
> unconditional Siegel-pole proof in the fixed archive, but did not find evidence that these invalidate the final standard RH
> theorem. Our best judgment is that the formal proof is very likely correct; the remaining
> issue is faithfulness/explanatory quality, not a demonstrated formal gap.

## Where to look

- `SUBMISSION.md` — precise reviewer brief.
- `REVIEWER_PROMPT.md` — independent review prompt.
- `reviews/2026-11-22/CONCLUSIONS.md` — follow-up local checks and Nielsen PDF review.
- `reports/historical/` — earlier, stronger claims, retained for transparency.
- `evidence/` — source excerpts.
- `logs/` — BFS/scan logs.
