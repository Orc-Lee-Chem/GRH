# GRH Lean audit: what we did and what we believe

**Status (2026-11-22):** We believe, with high confidence, that the Alpöge/Claude archive is a
**formal proof of the standard Mathlib `RiemannHypothesis` statement**. We found degenerate
internal definitions and, in the fixed archive, no explicit unconditional proof of the named Siegel-pole proposition, but we have **not** shown
that they invalidate the final theorem. The earlier “the final theorem is vacuous / GRH is not
proved” conclusion was too strong and has been retracted.

---

## 中文摘要

- **我们做了什么：** 对 Alpöge/Claude 的 Lean 4 GRH archive 做了源码审计、证明项依赖图分析、
  独立 kernel/comparator 记录核对，以及 Siegel 极点文献和 OpenAI 近期工作的检索。
- **我们的判断：** 最终定理是标准 Mathlib `RiemannHypothesis`，不是本地 `True` 命题；没有发现
  `sorry`、额外公理或 kernel 漏洞；独立检查支持它通过。**这份形式证明大概率是对的。**
- **我们发现的瑕疵：** 内部有 `UnusedSlot72 := True`、`anyGeometry := True`、退化的
  `geoDegenerate`/`divXFl`；真正的 `SiegelEisensteinSimplePole` 只有定义，没有找到显式无条件证明。
- **但这些瑕疵目前不足以推翻最终定理：** 它们是否语义上“承重”尚未建立；至少
  `ResidueKilled.dm_of_two` 会直接忽略 `True` 参数。更准确地说，这是**忠实性/解释性**问题，
  不是“形式证明无效”的证据。

---

## Scope

This audit covers the archive's stated target: the Riemann zeta function and Dirichlet
L-functions (the GRH range used here). It does not claim a formalization of GRH for arbitrary
global or automorphic L-functions.

## Bottom line

1. `src/Main.lean` proves the actual Mathlib statement:

   ```lean
   theorem riemannHypothesis : RiemannHypothesis := rhOfAll
   ```

2. The archive has no `sorry`, `axiom`, `native_decide`, `implemented_by` or extra axiom in the
   audited source; independent kernel/comparator records report acceptance with only
   `propext`, `Classical.choice`, `Quot.sound`.

3. The proof term does contain degenerate/internal definitions:
   - `GlobalTheory.Published.UnusedSlot72 := True`
   - `GlobalTheory.Mem.Top.Bl.anyGeometry := fun _ _ _ => True`
   - `Formalism.L2.Geo.geoDegenerate` — `vol = 0`, `Cl = PUnit`, many fields `True`
   - `Formalism.L2.Geo.divXFl` — `CurveM = PUnit`, `degM = 0`, `iMj = 0`

4. The real `GlobalTheory.Published.SiegelEisensteinSimplePole` is defined in the archive, but an
   exact-name source search found no explicit unconditional theorem proving it. This is a
   **search result**, not a proof that no indirect/equivariant proof exists.

5. These findings are not enough to show the final theorem is vacuous. The path through
   `dm_of_two` accepts a `True` argument and ignores it; reachability in a proof term is not the
   same as semantic necessity.

## What we did

- **Source audit:** checked all 175,187 Lean modules for `sorry`, `axiom`, `native_decide`,
  `implemented_by`, `opaque`, `constant`, and the final statement.
- **Proof-term graph:** read 175,179 `.olean` files, dumped 1,919,524 declaration-reference-list records (one record per declaration; each record lists the constants used in its value), and ran BFS
  from `rhOfAll`. The graph reaches 1,309,474 constants, including the degenerate definitions
  above.
- **Independent records:** reviewed the public Lean community / comparator / kernel receipts
  (Sutherland audit, `con-leche`, `con-ron`, community statement matching).
- **Literature search:** checked Tan (1999), Kudla–Rallis/doubling method, Gan–Qiu–Takeda for
  the real Siegel-pole statement.
- **Recent work:** checked OpenAI’s 2026 `openai/math` quasi-RH release; it is a different
  analytic-number-theory result (zero-free region / Landau–Siegel), not this Siegel-pole
  proposition.
- **Local targeted checks:** the follow-up package contains control tests, cache-archive checks,
  and proof-reference extractions; it does **not** contain a full local RH replay.

## What remains uncertain

- How to interpret the degenerate objects in branches other than `dm_of_two`; semantic
  dependence is a faithfulness question, not a validity criterion.
- Whether the real `SiegelEisensteinSimplePole` has an indirect proof or exactly matches a
  published theorem.
- Whether the formalization is a faithful/explanatory rendering of the intended mathematics.
- Full independent kernel replay on this machine; we rely on the cited external checks.

## Repository map

- `CONCLUSIONS.md` — concise verdict and evidence map (start here).
- `SUBMISSION.md` — reviewer brief with exact paths and claims.
- `REVIEWER_PROMPT.md` — prompt for an independent GPT/human review.
- `reviews/2026-11-22/` — follow-up local checks, Nielsen PDF review, receipts, ZIP.
- `evidence/` — source excerpts for the key definitions.
- `logs/` — BFS and scan logs.
- `scripts/` — `DumpEdges.lean`, `InspectOlean.lean`, `bfs_edges.py`, `Check.lean`,
  `verify_repository_hashes.py`.
- `reports/historical/` — earlier, more alarmist reports, kept for transparency but superseded.

## Verify

```powershell
python scripts/verify_repository_hashes.py
```

The full source archive and cache are not included (about 1 GB source, about 100 GB cache).
See `SUBMISSION.md` for archive links and reproduction commands.
