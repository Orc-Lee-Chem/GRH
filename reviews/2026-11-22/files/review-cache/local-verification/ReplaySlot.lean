import Lean.Environment

open Lean

unsafe def main (args : List String) : IO UInt32 := do
  let stdout ← IO.getStdout
  let some path := args.head? | stdout.putStrLn "module file required"; return 1
  initSearchPath (← findSysroot)
  let env ← importModules #[{ module := `Init }] {}
  let (data, region) ← readModuleData path
  let target := `GlobalTheory.Published.UnusedSlot72
  let some (.defnInfo original) := data.constants.find? (fun ci => ci.name == target)
    | stdout.putStrLn "original slot definition missing"; return 1
  let checked ← match env.toKernelEnv.addDeclCore 0 10000 (.defnDecl original) none with
    | .ok checked => pure checked
    | .error _ => stdout.putStrLn "ORIGINAL_SLOT_KERNEL_REPLAY=FAIL"; return 1
  stdout.putStrLn "ORIGINAL_SLOT_KERNEL_REPLAY=PASS"
  let positive : Declaration := .thmDecl {
    name := `LocalVerification.actualSlotProof
    levelParams := []
    type := mkConst target
    value := mkConst `True.intro
  }
  match checked.addDeclCore 0 10000 positive none with
  | .ok _ => stdout.putStrLn "TRUE_INTRO_HAS_ORIGINAL_SLOT_TYPE=PASS"
  | .error _ => stdout.putStrLn "TRUE_INTRO_HAS_ORIGINAL_SLOT_TYPE=FAIL"; return 1
  let negative : Declaration := .thmDecl {
    name := `LocalVerification.invalidFalseProof
    levelParams := []
    type := mkConst `False
    value := mkConst `True.intro
  }
  match checked.addDeclCore 0 10000 negative none with
  | .error _ => stdout.putStrLn "MALFORMED_FALSE_PROOF_REJECTED=PASS"
  | .ok _ => stdout.putStrLn "MALFORMED_FALSE_PROOF_REJECTED=FAIL"; return 1
  CompactedRegion.free region
  return 0
