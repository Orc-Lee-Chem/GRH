import Main
open Lean

/-!
Tier-1 check for the GRH Lean archive.

Run from a project where `Main.olean` exists (community cache or a full build):

    lake env lean Check.lean > check.out 2>&1

It prints the axioms of the five headline theorems and the direct constants
used by the proof term of `riemannHypothesis`.  A `#print` fallback is included
because the meta API can differ between Lean versions.
-/

#check @riemannHypothesis
#print axioms riemannHypothesis
#print axioms riemannZeta_eq_zero_re
#print axioms LFunction_ne_zero_of_half_lt_re
#print axioms LFunction_eq_zero_re
#print axioms LFunction_eq_zero_re_of_isPrimitive

/- Direct constants in the proof term (Lean 4.33/4.34 API). -/
#eval do
  let env ← getEnv
  let some ci := env.find? `riemannHypothesis
    | throwError "riemannHypothesis not found"
  let some v := ci.value? (allowOpaque := true)
    | throwError "riemannHypothesis has no value"
  let cs := v.getUsedConstants
  IO.println s!"direct constants: {cs.size}"
  for c in cs do
    IO.println s!"  {c}"
  IO.println "--- suspects ---"
  let suspects : List Name := [
    `geoDegenerate, `divXFl, `anyGeometry,
    `GlobalTheory.Published.UnusedSlot72,
    `UpperTheory.LiteratureTheorems.siegel_eisenstein_simple_pole,
    `exists_divT, `divEx_prov
  ]
  for s in suspects do
    if cs.contains s then IO.println s!"  DIRECT HIT: {s}"
  IO.println "done"

/- Fallback: print the proof term and grep the suspect names. -/
set_option pp.proofs true in
set_option pp.all true in
#print riemannHypothesis

