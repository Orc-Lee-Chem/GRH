# Reviewer brief: GRH Lean audit

Date: 2026-11-22

## Purpose

This repository records an independent audit of the Alpöge/Claude Lean 4 formalization of the
Riemann hypothesis. The goal is to state precisely:

1. what formal result is claimed,
2. what we verified,
3. what degenerate internal definitions we found,
4. whether those findings invalidate the final theorem,
5. what remains uncertain.

**Current verdict:** the formal proof is very likely correct. We found degenerate internal
definitions and no explicit proof of the named real Siegel-pole proposition, but we have not
shown that these invalidate the final standard RH theorem. Our earlier “the final theorem is
vacuous” conclusion is retracted.

## The final statement

`src/Main.lean:4`:

```lean
theorem riemannHypothesis : RiemannHypothesis := rhOfAll
```

`RiemannHypothesis` is Mathlib’s standard RH statement, not a local `True` definition.
Independent kernel/comparator records report acceptance with only `propext`,
`Classical.choice`, `Quot.sound`.

## What we checked

- **Source scan:** all 175,187 Lean modules; no `sorry`, extra axiom, `native_decide`,
  `implemented_by`, `opaque`/`constant` abuse in the audited source.
- **Proof-term graph:** 175,179 `.olean` files; 1,919,524 value edges; BFS from `rhOfAll` reaches
  1,309,474 constants. This is a reachability graph, not a semantic necessity proof.
- **Definitions:** inspected `UnusedSlot72`, `anyGeometry`, `geoDegenerate`, `divXFl`,
  `exists_divT`, `divEx_prov`.
- **Real Siegel pole:** inspected
  `SiegelEisensteinSimplePoleOfDoublingMethod.lean` and
  `EisPoleLEZeroOfLt.lean`; ran exact-name source search.
- **Independent checks:** reviewed the public Lean community/comparator/kernel records
  (Sutherland audit, `con-leche`, `con-ron`, statement matching).
- **Literature:** Tan 1999, Kudla–Rallis/doubling method, Gan–Qiu–Takeda.
- **Recent work:** OpenAI `openai/math` quasi-RH release; it is a different analytic result.

## Findings

### 1. Degenerate definitions are real

- `GlobalTheory.Published.UnusedSlot72 := True`
  (`src/.../DiscreteSpectrumResidualClassification.lean:7`)
- The main bundle field `siegelEisensteinSimplePole` has type `UnusedSlot72`
  (`src/.../BernsteinUnitaryProductIrreducible.lean:74`); its proof is `trivial`
  (`src/.../EveryCharacterOfLiteratureOfVWin.lean:505`).
- `anyGeometry := fun _ _ _ => True` (`src/.../OverIx.lean:19`).
- `geoDegenerate`: `vol = 0`, `Cl = PUnit`, many fields `True`
  (`src/.../Inhabited.lean:241`).
- `divXFl`: `CurveM = PUnit`, `degM = 0`, `iMj = 0`
  (`src/.../Inhabited.lean:829`).

### 2. The real Siegel pole is not explicitly proved

The real `GlobalTheory.Published.SiegelEisensteinSimplePole` is defined at
`src/.../SiegelEisensteinSimplePoleOfDoublingMethod.lean:14`.

An exact-name search found no explicit unconditional theorem with that conclusion; it occurs as
a hypothesis/field and in conditional theorems. This is not a proof that no indirect proof
exists.

### 3. Reachability is not necessity

BFS from `rhOfAll` reaches the degenerate constants. But at least one path explicitly ignores a
`True` argument:

`src/.../DmOfHyp.lean`:

```lean
theorem dm_of_two : ... → True → DM := by
  intro hC hS _ D ...
```

The `_` ignores `True`. Therefore, the presence of `UnusedSlot72` in the proof term does not by
itself show that the real Siegel-pole theorem is a necessary missing premise.

## Our assessment

- **Formal validity:** high confidence. Standard RH statement; no `sorry`/axiom; independent
  kernel/comparator records support acceptance. We did not perform a local full kernel replay.
- **Faithfulness/explanatory quality:** open. Degenerate internal definitions are a real
  quality concern; their semantic role is not fully established.
- **The real Siegel pole:** unproved as an explicit named theorem in the public archive; exact
  literature equivalence remains a specialist question.
- **OpenAI quasi-RH:** different result; no evidence it covers this proposition.

## What would change our mind

- A proof that the degenerate objects are semantically required by the final theorem (not just
  syntactically reachable).
- An explicit or indirect proof of the real `SiegelEisensteinSimplePole`, or a paper-level
  equivalence to a known theorem.
- A formal defect in the final statement or kernel acceptance record.
- Evidence that `Main.lean`’s `RiemannHypothesis` is not the standard Mathlib statement.

## Review questions

1. Is `RiemannHypothesis` in `Main.lean` the standard Mathlib statement?
2. Are the degenerate definitions as quoted?
3. Is there an explicit unconditional proof of the real `SiegelEisensteinSimplePole` in the
   public archive?
4. Does `dm_of_two` ignore `True` as quoted?
5. Does any recent work (OpenAI or other) prove this exact Siegel-pole proposition?
6. Is the final theorem formally valid, and is the remaining issue only faithfulness?

## Reproduction

See `REVIEWER_PROMPT.md` and `reviews/2026-11-22/README.md`. The full source/cache are not
included (about 1 GB source, about 100 GB cache). Artifacts in this repo:

- `evidence/` — source excerpts.
- `logs/` — BFS/scan logs.
- `scripts/` — `DumpEdges.lean`, `InspectOlean.lean`, `bfs_edges.py`, `Check.lean`.
- `reviews/2026-11-22/` — follow-up local checks and Nielsen PDF review.

## Historical material

Earlier, more alarmist reports are retained under `reports/historical/`. They are superseded by
`CONCLUSIONS.md` and this brief. The `CORRECTION.md` at the top level records the retraction.
