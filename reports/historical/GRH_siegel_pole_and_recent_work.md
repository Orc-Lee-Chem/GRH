# The real Siegel–Eisenstein simple-pole proposition, and recent AI work

Date: 2026-11-22

## 1. The archive already contains the real proposition

At
`src/Development/AbelianVarietyTheory/PublishedTheorems/SiegelWeil₂/SiegelEisensteinSimplePoleOfDoublingMethod.lean`
there is a **non-vacuous** definition:

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

In words:

> For every global CM datum `D` and Hermitian space `V` of positive rank, for every
> majorizable `a`, Iwasawa condition, Hecke character `μ` with `ResEta D μ b`, and every
> `φ` in the degree space `degPS V a μ s₀`, if `b > rank V`, then the Siegel Eisenstein
> series attached to the flat section `flat V a φ s₀` has a pole of order at most 1 at
> `(b - rank V)/2`.

This is the statement named by the field `siegelEisensteinSimplePole`. It is not `True`.

## 2. The main bundle replaces it with `True`

At
`src/Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/ThirdPlaceSeries/BernsteinUnitaryProductIrreducible.lean:74`
the field is:

```lean
siegelEisensteinSimplePole : GlobalTheory.Published.UnusedSlot72
```

and

```lean
abbrev GlobalTheory.Published.UnusedSlot72 : Prop := True
```

So the real proposition is replaced by `True` exactly at the point where the main
`UnitaryGroupThirdPlaceHypotheses` is assembled. The proof of the slot is `trivial`.

## 3. Is the real proposition proved in the archive?

No. A search for a theorem whose **conclusion** is `SiegelEisensteinSimplePole` finds only:

- fields of hypothesis structures (`GeneralHyps`, `BhattScholzeCrystallineLattices`, etc.);
- conditional theorems of the form `SiegelEisensteinSimplePole → ...`;
- `simplePole_iff`, which **assumes** `Published.SiegelEisensteinSimplePole` and proves an
  equivalent form;
- `eisPoleLEZeroOfLt`, which proves order 0 for `2 * rank < b`, not order 1 for the full range.

There is no unconditional theorem `... : Published.SiegelEisensteinSimplePole`.

So the archive either:

1. treats the real proposition as an unproved hypothesis, or
2. replaces it by `True` in the main bundle.

Both are incompatible with “the main theorem is an unconditional proof of GRH”.

## 4. Is the real proposition a known theorem?

There is a substantial literature on poles of Siegel Eisenstein series:

- V. Tan, *Poles of Siegel Eisenstein Series on U(n,n)*, Canad. J. Math. 51 (1999):
  the normalized Siegel Eisenstein series on `U(n,n)` has **at most simple poles** at
  integers or half-integers in a certain strip.
- Kudla–Rallis / the doubling method: meromorphic continuation and pole control for
  Siegel Eisenstein series; this is the method named in the file `...OfDoublingMethod`.
- Gan–Qiu–Takeda, regularized Siegel–Weil formula and second-term identities: pole
  structure in the regularized setting.

So the *shape* of the statement is known mathematics, and the exact formal statement may be
a specialization of known results. But I cannot certify the exact Lean statement as a
published theorem without a paper-level comparison of every definition (`EisPoleLE`,
`flat`, `degPS`, `IsMaj`, `HasIwasawa`, `ResEta`) with the literature. The archive itself
does not prove it.

## 5. OpenAI’s 2026 work does not cover this

The OpenAI `openai/math` release (722 manuscripts, 372 families) includes:

- a “quasi-Riemann hypothesis”: zero-free region `Re(s) > 7/8` for Dirichlet L-functions;
- exclusion of Landau–Siegel zeros;
- many other results.

That is analytic number theory about zero-free regions and Landau–Siegel zeros. It is **not**
the representation-theoretic statement “Siegel Eisenstein series has a simple pole” and it
does **not** prove GRH. I found no paper in the public `openai/math` material that proves
`SiegelEisensteinSimplePole` or fills `UnusedSlot72`.

The Alpöge/Claude archive we audited is a different recent work (November 2026), not the
OpenAI release. Its Lean proof is independently kernel-checked, but the Hexagon reader’s
guide explicitly notes:

> “One field of the first bundle, `siegelEisensteinSimplePole`, is named after the simple
> pole of the Siegel Eisenstein series but has type `UnusedSlot72`, which is `True`, so it
> asserts nothing.”

That is an independent confirmation of the empty slot.

## 6. What would a genuine proof need?

1. Prove the real `SiegelEisensteinSimplePole` (or a known theorem equivalent to it) in Lean.
2. Replace `UnusedSlot72` by that proposition in the main bundle.
3. Replace `anyGeometry`, `geoDegenerate`, `divXFl` by nondegenerate geometric objects
   (or prove the geometry layer unconditionally).
4. Re-run the proof-term dependency check to confirm the final theorem uses the real
   propositions, not `True`/`PUnit`/`0`.

Until then, the archive is a valid Lean proof of a **vacuous/weakened** statement, not a
proof of GRH.

## References

- Alpöge/Claude Lean archive: <https://alpo.ge/lean.tar.gz.part01>
- Hexagon reader’s guide: <https://hexagonmath.org/2611.00799v1>
- Nielsen, *The Invalidity of the Alpoge Proposed Proof of the Riemann Hypothesis*:
  <https://philarchive.org/rec/NIEIOT-2>
- V. Tan, *Poles of Siegel Eisenstein Series on U(n,n)*:
  <https://www.cambridge.org/core/journals/canadian-journal-of-mathematics/article/poles-of-siegel-eisenstein-series-on-un-n/27F8B3E634321A156A2225A7CC2E5598>
- Kudla, Park City lectures (doubling method):
  <https://www.math.utoronto.ca/skudla/kyoto.pdf>
- OpenAI `math` repository: <https://github.com/openai/math>
- OpenAI quasi-RH coverage:
  <https://eu.36kr.com/en/p/4015128916676736>
