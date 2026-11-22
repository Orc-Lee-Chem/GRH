import os, sqlite3, sys
from collections import deque

tsv = r"E:\GRH-Lean-Check\edges.tsv"
db = r"E:\GRH-Lean-Check\edges.db"
targets = {
    "Formalism.L2.Geo.geoDegenerate",
    "Formalism.L2.Geo.divXFl",
    "GlobalTheory.Mem.Top.Bl.anyGeometry",
    "GlobalTheory.Published.UnusedSlot72",
    "UpperTheory.LiteratureTheorems.siegel_eisenstein_simple_pole",
    "GlobalTheory.Mem.Top.DivRec.exists_divT",
    "GlobalTheory.Mem.Top.DivRec.divEx_prov",
}

if not os.path.exists(db):
    con = sqlite3.connect(db)
    con.execute("PRAGMA journal_mode=OFF")
    con.execute("PRAGMA synchronous=OFF")
    con.execute("CREATE TABLE nodes (name TEXT PRIMARY KEY, used TEXT)")
    n = 0
    with open(tsv, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            parts = line.rstrip("\n").split("\t", 2)
            if len(parts) != 3:
                continue
            name, _file, used = parts
            con.execute("INSERT OR REPLACE INTO nodes VALUES (?,?)", (name, used))
            n += 1
            if n % 200000 == 0:
                print("loaded", n, flush=True)
    con.commit()
    print("loaded total", n, flush=True)
else:
    con = sqlite3.connect(db)
    print("using existing db", flush=True)

start = "rhOfAll"
seen = {start}
parent = {start: None}
q = deque([start])
found = {}
visited = 0
while q and visited < 2000000:
    n = q.popleft()
    visited += 1
    if n in targets:
        found[n] = n
        print("TARGET", n, flush=True)
        # keep going to find others
    row = con.execute("SELECT used FROM nodes WHERE name=?", (n,)).fetchone()
    if not row:
        continue
    for m in row[0].split(","):
        if not m or m in seen:
            continue
        seen.add(m)
        parent[m] = n
        q.append(m)
        if m in targets:
            print("TARGET", m, flush=True)
    if visited % 50000 == 0:
        print("visited", visited, "seen", len(seen), "queue", len(q), flush=True)

print("done visited", visited, "seen", len(seen), "targets", sorted(found), flush=True)
for t in sorted(found):
    path = []
    x = t
    while x is not None:
        path.append(x)
        x = parent.get(x)
    path.reverse()
    print("PATH", " -> ".join(path), flush=True)

