import Lean
open Lean

unsafe def main (args : List String) : IO UInt32 := do
  let some f := args.head? | IO.eprintln "usage: InspectOlean FILE [CONST...]"; return 1
  let (data, _) ← readModuleData f
  IO.println s!"module: {f}"
  IO.println s!"constants: {data.constants.size}"
  if args.length == 1 then
    for c in data.constants do
      IO.println s!"  {c.name}"
  for n in args.drop 1 do
    let name := n.toName
    match data.constants.find? (fun c => c.name == name) with
    | none => IO.println s!"NOT FOUND {name}"
    | some ci =>
      IO.println s!"CONST {name}"
      match ci.value? (allowOpaque := true) with
      | none => IO.println "  (no value)"
      | some v =>
        let cs := v.getUsedConstants
        IO.println s!"  used constants: {cs.size}"
        for c in cs do
          IO.println s!"  {c}"
  return 0
