# FINAL REVIEW PROMPT — copy this to GPT

You are an independent reviewer of a Lean 4 formalization. Your job is **not** to agree with
me. Your job is to verify or refute the claims in `GRH_Lean_audit_submission.md` against the
original repository and the mathematical literature.

## Rules

1. **Do not use my excerpts as independent evidence.** Open the original repository or raw
   files and quote the actual source line.
2. If you have no browser/repository/terminal tool, say so at the start. Mark claims that
   depend on repository access as `unresolved (no repository access)`. Do not pretend to have
   checked them.
3. A claim is `verified` only if you give: URL or commit, file path, line number, and the
   exact quoted source (or exact command output). Otherwise it is `unresolved`.
4. Do not mark “there is no proof” merely because one search failed. Distinguish:
   - “not found in this public archive after a full exact-conclusion search”;
   - “no proof exists anywhere”.
5. Distinguish **Lean kernel validity** from **mathematical non-vacuity**. A proof can be
   kernel-valid and still prove a vacuous statement.
6. Do not claim the real Siegel-pole proposition is “known” without comparing the exact Lean
   statement to a cited theorem. If unsure, mark `unresolved`.

## Material

- Submission: `GRH_Lean_audit_submission.md` (claims + source excerpts + BFS paths)
- Repository mirror: <https://github.com/CocoSgt/riemann-hypothesis-lean>
- Comparator copy: <https://github.com/leanprover-community/riemann-hypothesis>
- Alpöge archive: <https://alpo.ge/lean.tar.gz.part01> … `.part14`
- Source commit audited: `7cbf7a0c32fca1badf05931879a37c3f8a2b03b4`

If you can clone:

```bash
git clone https://github.com/CocoSgt/riemann-hypothesis-lean
cd riemann-hypothesis-lean
git checkout 7cbf7a0c32fca1badf05931879a37c3f8a2b03b4
```

If you cannot clone, use GitHub’s code search or raw URLs and say which method you used.

## Tasks

### A. Open the actual source

Verify these files and quote the relevant lines:

1. `src/Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/LocalTypeDictionary/DiscreteSpectrumResidualClassification.lean`
2. `src/Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/ThirdPlaceSeries/BernsteinUnitaryProductIrreducible.lean`
3. `src/Development/AutomorphicArithmetic/ThetaCorrespondence/ThetaPairLifts/ThirdPlaceSeries/EveryCharacterOfLiteratureOfVWin.lean`
4. `src/Development/AbelianVarietyTheory/PublishedTheorems/SiegelWeil₂/SiegelEisensteinSimplePoleOfDoublingMethod.lean`
5. `src/Development/AbelianVarietyTheory/PublishedTheorems/SiegelWeil₂/EisPoleLEZeroOfLt.lean`
6. `src/Formalism/LocalToGlobal/LatticeGeometry/Inhabited.lean`
7. `src/Development/AbelianVarietyTheory/Definitions/AutomorphicMembership/OverIx.lean`
8. `src/Development/AbelianVarietyTheory/Proofs/IwasawaDecomposition/TupPinsOfMuIsW.lean`

### B. Check the vacuous definitions

For each, quote the definition and state whether it is a genuine object or a placeholder:

- `GlobalTheory.Published.UnusedSlot72`
- `GlobalTheory.Mem.Top.Bl.anyGeometry`
- `Formalism.L2.Geo.geoDegenerate`
- `Formalism.L2.Geo.divXFl`
- `GlobalTheory.Mem.Top.DivRec.exists_divT`
- `GlobalTheory.Mem.Top.DivRec.divEx_prov`

### C. Check the real Siegel-pole proposition

1. Quote the real `def GlobalTheory.Published.SiegelEisensteinSimplePole`.
2. Parse it in ordinary mathematical language:
   - what are `D`, `V`, `a`, `μ`, `b`, `φ`, `s₀`;
   - what does `EisPoleLE ... 1` assert;
   - at what point is the pole.
3. Run an exact-conclusion search over **all** `.lean` files:

```bash
grep -RIn "SiegelEisensteinSimplePole" src
grep -RInE "theorem .*:.*SiegelEisensteinSimplePole" src
```

4. Inspect every occurrence. State whether any unconditional theorem has conclusion
   `SiegelEisensteinSimplePole`.
5. Check `EisPoleLEZeroOfLt.lean`: does it prove the full order-1 statement, or only an
   order-0 statement for `2 * rank < b`?
6. Check whether the main bundle field is typed as the real proposition or as `UnusedSlot72`.

### D. Check proof-term reachability

The submission claims a BFS over `.olean` value edges reaches these constants from `rhOfAll`:

`UnusedSlot72`, `siegel_eisenstein_simple_pole`, `anyGeometry`, `geoDegenerate`, `divXFl`,
`exists_divT`, `divEx_prov`.

Use the supplied `bfs2.log` as evidence, or reproduce with `DumpEdges.lean` / `bfs_edges.py`.
State whether the paths support:

- “the constant is present in the transitive proof term”, and
- “the final theorem needs a proof of it as an argument/field” (if you can determine that).

Do not overstate: presence in a structure value is not the same as being projected by the final
theorem. Say which claim is supported and which is not.

### E. Search the literature

Run web searches for:

- `"SiegelEisensteinSimplePole"`
- `"UnusedSlot72" Lean`
- `Siegel Eisenstein series simple pole U(n,n)`
- `Tan, Poles of Siegel Eisenstein Series on U(n,n)`
- `Kudla Rallis doubling method Siegel Eisenstein pole`
- `Gan Qiu Takeda regularized Siegel-Weil`

Check at least:

- V. Tan, *Poles of Siegel Eisenstein Series on U(n,n)*, Canad. J. Math. 51 (1999).
- Kudla–Rallis / doubling method (Kudla’s Park City notes).
- Gan–Qiu–Takeda, regularized Siegel–Weil formula.

Question: is the exact Lean `SiegelEisensteinSimplePole` a known theorem, a specialization of a
known theorem, a stronger statement, or unresolved? Give citations and explain.

### F. Check OpenAI and recent work

Search:

- `openai/math`
- `OpenAI quasi Riemann hypothesis`
- `OpenAI 722 mathematics`
- `SiegelEisensteinSimplePole OpenAI`
- `Siegel Eisenstein simple pole Lean`

Questions:

1. Does OpenAI’s 2026 `openai/math` release prove this exact proposition?
2. Does it fill `UnusedSlot72`?
3. Is its quasi-RH result the same as GRH or this Siegel-pole statement?
4. Does any other recent public work prove the real proposition, or does the Alpöge/Claude
   archive remain the only relevant formalization?

### G. Final verdict

Answer separately:

1. Is the archive kernel-valid? (Cite independent reports; do not infer from my summary.)
2. Is the formal theorem non-vacuous?
3. Is the real `SiegelEisensteinSimplePole` proved in the public archive?
4. Is the main proof term dependent on the vacuous definitions?
5. Does any recent work (OpenAI or other) cover the missing proposition?
6. If the real proposition is not proved, what would need to be added for a genuine GRH proof?

## Required output

Start with:

```text
Tools used: ...
Repository access: yes/no
Web access: yes/no
Commit/archive verified: ...
```

Then:

| Claim | Evidence (URL/commit/path/line/quote) | Verified? | Verdict |
|---|---|---|---|

Then:

```text
What I could not verify:
...
```

Do not write “verified” without a URL/commit + path + line + quote. If you cannot access the
repository, mark the repository-dependent claims `unresolved` and still answer what can be
answered from the literature/web.
