# Reproduction scripts

These scripts regenerate the proof-term graph used in the audit. They are not a Lean proof
replay; they read `.olean` files.

## 1. Generate `olean_list.txt`

PowerShell (from the directory containing the extracted project):

```powershell
$files = Get-ChildItem '.\\.lake\\build\\lib\\lean' -Recurse -File -Filter '*.olean' |
  ForEach-Object { $_.FullName }
[System.IO.File]::WriteAllLines(
  (Join-Path (Get-Location) 'olean_list.txt'),
  $files,
  [System.Text.UTF8Encoding]::new($false)
)
```

Or, in Python:

```python
from pathlib import Path
root = Path(r".lake/build/lib/lean")
Path("olean_list.txt").write_text(
    "\n".join(str(p) for p in root.rglob("*.olean")) + "\n",
    encoding="utf-8",
)
```

## 2. Dump declaration-reference records

From a project with Lean 4.33.1 and the `.olean` files:

```powershell
lake env lean --run scripts/DumpEdges.lean `
  olean_list.txt edges.tsv
```

Each `edges.tsv` line is:

```text
declaration-name <TAB> .olean-file <TAB> comma-separated constants used in its value
```

This is **one record per declaration**, not a literal graph edge count.

## 3. Build the SQLite graph and run BFS

`bfs_edges.py` accepts two environment variables:

- `GRH_EDGES_TSV` — default `edges.tsv` next to the repository
- `GRH_EDGES_DB` — default `edges.db` next to the repository

To force a fresh build (do not reuse an old database):

```powershell
$env:GRH_EDGES_TSV = "E:\\path\\edges.tsv"
$env:GRH_EDGES_DB  = "E:\\path\\edges_fresh.db"
python scripts/bfs_edges.py *> logs/bfs2.log
```

The first line should be:

```text
source tsv=edges.tsv db=edges_fresh.db
```

`edges.tsv` and `edges.db` are multi-GB and are not committed. The repository's `logs/bfs2.log`
was generated from a fresh database; the old "using existing db" line is not part of the current
log.

## 4. Inspect a single `.olean`

```powershell
lake env lean --run scripts/InspectOlean.lean `
  path\\to\\Module.olean Constant.Name
```

## 5. Check the final theorem (optional)

`scripts/Check.lean` imports `Main` and prints axioms / direct constants. It requires a complete
project cache or a full build; see the main README for limits.
