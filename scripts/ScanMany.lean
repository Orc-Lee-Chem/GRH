import Lean
open Lean

def targets : List Name := [
  `geoDegenerate, `divXFl, `anyGeometry,
  `GlobalTheory.Published.UnusedSlot72,
  `UpperTheory.LiteratureTheorems.siegel_eisenstein_simple_pole,
  `exists_divT, `divEx_prov
]

unsafe def main (args : List String) : IO UInt32 := do
  let some listFile := args.head? | IO.eprintln "usage: ScanMany LIST"; return 1
  let contents ← IO.FS.readFile listFile
  let lines := contents.splitOn "\n" |>.map String.trim |>.filter (fun s => !s.isEmpty)
  let mut files := 0
  let mut hits := 0
  let mut errors := 0
  for f in lines do
    if !f.endsWith ".olean" then continue
    try
      let (data, region) ← readModuleData f
      files := files + 1
      for ci in data.constants do
        let mut cs := ci.type.getUsedConstants
        match ci.value? (allowOpaque := true) with
        | some v => cs := cs ++ v.getUsedConstants
        | none => pure ()
        for c in cs do
          for t in targets do
            if c == t || c.toString.endsWith t.toString then
              IO.println s!"HIT {ci.name} uses {c} in {f}"
              hits := hits + 1
      CompactedRegion.free region
    catch _ => errors := errors + 1
  IO.println s!"scanned={files} errors={errors} hits={hits}"
  return 0
