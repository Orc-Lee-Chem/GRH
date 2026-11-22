import Lean
open Lean

def targets : List Name := [
  `geoDegenerate, `divXFl, `anyGeometry,
  `GlobalTheory.Published.UnusedSlot72,
  `UpperTheory.LiteratureTheorems.siegel_eisenstein_simple_pole,
  `exists_divT, `divEx_prov
]

unsafe def main (args : List String) : IO UInt32 := do
  let some f := args.head? | IO.eprintln "usage: ScanModule FILE"; return 1
  let (data, _) ← readModuleData f
  IO.println s!"module {f}: {data.constants.size} constants"
  let mut hits := 0
  for ci in data.constants do
    let mut cs := ci.type.getUsedConstants
    match ci.value? (allowOpaque := true) with
    | some v => cs := cs ++ v.getUsedConstants
    | none => pure ()
    for c in cs do
      for t in targets do
        if c == t || c.toString.endsWith t.toString then
          IO.println s!"  HIT {ci.name} uses {c}"
          hits := hits + 1
  IO.println s!"hits={hits}"
  return 0
