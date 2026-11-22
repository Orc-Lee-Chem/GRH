import Lean
open Lean

unsafe def main (args : List String) : IO UInt32 := do
  let some listFile := args.head? | IO.eprintln "usage: DumpEdges LIST OUT"; return 1
  let some outFile := (args.drop 1).head? | IO.eprintln "usage: DumpEdges LIST OUT"; return 1
  let contents ← IO.FS.readFile listFile
  let lines := contents.splitOn "\n" |>.map String.trim |>.filter (fun s => !s.isEmpty)
  let out ← IO.FS.Handle.mk outFile .write
  let mut files := 0
  let mut edges := 0
  for f in lines do
    if !f.endsWith ".olean" then continue
    try
      let (data, region) ← readModuleData f
      files := files + 1
      for ci in data.constants do
        match ci.value? (allowOpaque := true) with
        | some v =>
          let cs := v.getUsedConstants
          if cs.size > 0 then
            let parts := cs.toList.map (fun c => c.toString)
            out.putStrLn s!"{ci.name}\t{f}\t{String.intercalate "," parts}"
            edges := edges + 1
        | none => pure ()
      CompactedRegion.free region
    catch _ => pure ()
    if files % 10000 == 0 then
      IO.println s!"files={files} edges={edges}"
  out.flush
  IO.println s!"DONE files={files} edges={edges}"
  return 0
