import Lean
open Lean

def targets : List String := [
  "Formalism.L2.Geo.geoDegenerate",
  "Formalism.L2.Geo.divXFl",
  "GlobalTheory.Mem.Top.Bl.anyGeometry",
  "GlobalTheory.Published.UnusedSlot72",
  "UpperTheory.LiteratureTheorems.siegel_eisenstein_simple_pole",
  "GlobalTheory.Mem.Top.DivRec.exists_divT",
  "GlobalTheory.Mem.Top.DivRec.divEx_prov"
]

unsafe def main (args : List String) : IO UInt32 := do
  let some listFile := args.head? | IO.eprintln "usage: IndexBFS LIST"; return 1
  let contents ← IO.FS.readFile listFile
  let lines := contents.splitOn "\n" |>.map String.trim |>.filter (fun s => !s.isEmpty)
  let mut index : Std.HashMap String String := {}
  let mut files := 0
  let mut constants := 0
  for f in lines do
    if !f.endsWith ".olean" then continue
    try
      let (data, region) ← readModuleData f
      files := files + 1
      for ci in data.constants do
        constants := constants + 1
        index := index.insert ci.name.toString f
      CompactedRegion.free region
    catch _ => pure ()
    if files % 10000 == 0 then
      IO.println s!"indexed files={files} constants={constants}"
  IO.println s!"INDEX files={files} constants={constants} index={index.size}"
  let mut seen : Std.HashSet String := {}
  let mut todo : Array String := #["rhOfAll"]
  let mut visited := 0
  let mut unread := 0
  let mut reached : Array String := #[]
  while todo.size > 0 && visited < 300000 do
    let n := todo.back!
    todo := todo.pop
    if seen.contains n then continue
    seen := seen.insert n
    match index.get? n with
    | none => pure ()
    | some file =>
      visited := visited + 1
      try
        let (data, region) ← readModuleData file
        let some ci := data.constants.find? (fun c => c.name.toString == n) | continue
        let some v := ci.value? (allowOpaque := true) | continue
        for c in v.getUsedConstants do
          let s := c.toString
          for t in targets do
            if s == t || s.endsWith t then
              reached := reached.push s!"REACHED {n} -> {s} in {file}"
          if !seen.contains s then todo := todo.push s
        CompactedRegion.free region
      catch _ => unread := unread + 1
  IO.println s!"BFS visited={visited} seen={seen.size} unread={unread} reached={reached.size}"
  for r in reached[:100] do
    IO.println r
  return 0
