# Logs

- `bfs2.log` — fresh BFS run from `rhOfAll`, generated from a new SQLite database built from
  `edges.tsv`. Its first line is `source tsv=edges.tsv db=edges_fresh.db`; it does not use an
  existing database.
- `dump_edges.log` — `DumpEdges.lean` progress from the original run.
- `scanmany3.log` — direct-use scan of the `.olean` set.
- `inspect_eigen.log`, `inspect_mainconcl2.log` — source-level chain inspections.

`edges.tsv` and `edges.db` are multi-GB and are not committed. See `../scripts/README.md` for
reproduction.
