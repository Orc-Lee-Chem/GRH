import Lean.Environment
import Lean.Data.Json

open Lean

def jsonStr (s : String) : Json := Json.str s
def jsonNames (names : Array Name) : Json := Id.run do
  let mut out := #[]
  for name in names do
    out := out.push (jsonStr name.toString)
  return Json.arr out

partial def exprSketch (e : Expr) (fuel : Nat := 5) : String :=
  if fuel == 0 then "..." else
  match e with
  | .const n _ => n.toString
  | .bvar n => "#" ++ toString n
  | .sort _ => "Sort"
  | .app f a => "(" ++ exprSketch f (fuel-1) ++ " " ++ exprSketch a (fuel-1) ++ ")"
  | .lam n t b _ => "(fun " ++ n.toString ++ " : " ++ exprSketch t (fuel-1) ++ " => " ++ exprSketch b (fuel-1) ++ ")"
  | .forallE n t b _ => "(forall " ++ n.toString ++ " : " ++ exprSketch t (fuel-1) ++ ", " ++ exprSketch b (fuel-1) ++ ")"
  | .letE n _ v b _ => "(let " ++ n.toString ++ " := " ++ exprSketch v (fuel-1) ++ "; " ++ exprSketch b (fuel-1) ++ ")"
  | .mdata _ b => exprSketch b fuel
  | .proj n i b => "(" ++ n.toString ++ "." ++ toString i ++ " " ++ exprSketch b (fuel-1) ++ ")"
  | _ => "other"

partial def usesBound (e : Expr) (index : Nat := 0) : Bool :=
  match e with
  | .bvar n => n == index
  | .app f a => usesBound f index || usesBound a index
  | .lam _ t b _ | .forallE _ t b _ => usesBound t index || usesBound b (index + 1)
  | .letE _ t v b _ => usesBound t index || usesBound v index || usesBound b (index + 1)
  | .mdata _ b | .proj _ _ b => usesBound b index
  | _ => false

partial def lambdaUsage (e : Expr) : Array Json :=
  match e with
  | .lam n t b _ =>
    #[Json.mkObj [("binder", jsonStr n.toString), ("type", jsonStr (exprSketch t 3)),
      ("usedInBody", Json.bool (usesBound b))]] ++ lambdaUsage b
  | .mdata _ b => lambdaUsage b
  | _ => #[]

def inspectConst (ci : ConstantInfo) : Json :=
  let value := ci.value? (allowOpaque := true)
  let valueNames := value.map Expr.getUsedConstants |>.getD #[]
  let focused := ci.name.toString.endsWith "dm_of_two" || ci.name.toString.endsWith "UnusedSlot72" ||
    ci.name.toString.endsWith "anyGeometry" || ci.name.toString == "riemannHypothesis" ||
    ci.name.toString.endsWith "height_bound_of_component_bounds"
  let usage := if focused then value.map lambdaUsage |>.getD #[] else #[]
  Json.mkObj [("name", jsonStr ci.name.toString),
    ("typeSketch", jsonStr (exprSketch ci.type)),
    ("valueSketch", jsonStr (value.map (exprSketch · 4) |>.getD "none")),
    ("typeConstants", jsonNames ci.type.getUsedConstants),
    ("valueConstants", jsonNames valueNames),
    ("lambdaUsage", Json.arr usage)]

unsafe def main (args : List String) : IO UInt32 := do
  let some manifest := args.head? | (← IO.getStderr).putStrLn "usage: InspectSelected MODULE_PATH_LIST OUTPUT"; return 1
  let some (output : String) := (args.drop 1).head? | (← IO.getStderr).putStrLn "output path required"; return 1
  let files := (← IO.FS.readFile manifest).splitOn "\n" |>.map String.trimAscii |>.map String.Slice.toString |>.filter (! ·.isEmpty)
  let out ← IO.FS.Handle.mk output .write
  let mut scanned := 0
  let mut constants := 0
  for file in files do
    let (data, region) ← readModuleData file
    for ci in data.constants do
      out.putStrLn (Json.mkObj [("file", jsonStr file), ("constant", inspectConst ci)]).compress
      constants := constants + 1
    CompactedRegion.free region
    scanned := scanned + 1
  out.flush
  (← IO.getStdout).putStrLn s!"SCANNED_MODULES={scanned} CONSTANTS={constants}"
  return 0
