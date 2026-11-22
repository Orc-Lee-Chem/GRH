import collections
import concurrent.futures
import hashlib
import json
import pathlib
import subprocess
import time
import psutil
import requests

ROOT = pathlib.Path(__file__).parent
OUT = ROOT / "trust-audit"

def main():
    modules = set(json.loads((OUT / "paper_route_modules.json").read_text()))
    old = {r["module"]:r for r in json.loads((ROOT / "selected_oleans.json").read_text())}
    selected=[]
    for line in (ROOT / "modules.jsonl").read_text().splitlines()[1:]:
        row=json.loads(line)
        if row[0] in modules-old.keys(): selected.append(row)
    assert {r[0] for r in selected} == modules-old.keys()
    def fetch(row):
        module, dep_hash, artifact, expected = row
        path=ROOT/"artifacts"/artifact
        url=f"https://rh-cache.taucetiproject.org/artifacts/leanprover-community/riemann-hypothesis/{artifact[:-5]}.art"
        if not path.exists():
            r=requests.get(url,timeout=30); r.raise_for_status()
            assert len(r.content)<8*1024**2
            assert hashlib.sha256(r.content).hexdigest()==expected
            path.write_bytes(r.content)
        assert hashlib.sha256(path.read_bytes()).hexdigest()==expected
        return {"module":module,"hash":dep_hash,"archive":artifact,"sha256":expected,"bytes":path.stat().st_size,"url":url}
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool: new=list(pool.map(fetch,selected))
    assert sum(r['bytes'] for r in new)<16*1024**2
    jobs=[]
    for r in new:
        relative=pathlib.Path(*r['module'].split('.'))
        bases=[str(OUT/"paper-project"/suffix/relative.parent) for suffix in ['lib/lean','ir']]
        for base in bases: pathlib.Path(base).mkdir(parents=True,exist_ok=True)
        jobs.append({"file":str(ROOT/"artifacts"/r['archive']),"hash":r['hash'],"base":bases})
    if jobs:
        result=subprocess.run([str(ROOT/"toolchain/bin/leantar.exe"),"--jobs","2","-f","-x","-j","-"],input=json.dumps(jobs),text=True,capture_output=True)
        result.check_returncode()
    (OUT/"paper-selected.json").write_text(json.dumps(new,indent=2),encoding="utf-8")
    files=[ROOT/"project/.lake/build/lib/lean"/(n.replace('.','/')+'.olean') for n in old]
    files.extend(OUT/"paper-project/lib/lean"/(r['module'].replace('.','/')+'.olean') for r in new)
    (OUT/"paper-olean-list.txt").write_text('\n'.join(map(str,files))+'\n',encoding='utf-8')
    command=[str(ROOT/"toolchain/bin/lean.exe"),"-j1","-M1536","--tstack=400000","--run","InspectSelected.lean",str(OUT/"paper-olean-list.txt"),str(OUT/"paper-inspect.jsonl")]
    start=time.monotonic(); peak=0
    with (OUT/"paper-inspection.log").open('wb') as log:
        process=subprocess.Popen(command,cwd=ROOT,stdout=log,stderr=subprocess.STDOUT)
        monitor=psutil.Process(process.pid)
        while process.poll() is None:
            try: peak=max(peak,monitor.memory_info().rss)
            except psutil.NoSuchProcess: pass
            if peak>2100*1024**2 or time.monotonic()-start>90:
                process.kill(); raise RuntimeError('Paper inspection exceeded resource budget')
            time.sleep(.05)
        assert process.wait()==0,(OUT/"paper-inspection.log").read_text(encoding='utf-8')
    constants={}
    for line in (OUT/"paper-inspect.jsonl").read_text(encoding='utf-8').splitlines():
        c=json.loads(line)['constant']; constants[c['name']]=c
    targets=['every_character_of_green_v_win','zero_free_all_of_green_v_win','zeroFreeAll_of_topG','nonempty_hyps_definite_side_of_closed_bound','forall_goal_of_shape_of_hyps','shape_closed_link_n_of_green','closed_linkDIVt_of_closed_bridge_kernel','zeroFreeOn_of_tiedWin_cyc']
    parent={'riemannHypothesis':None}; queue=collections.deque(parent)
    while queue:
        name=queue.popleft()
        for dep in constants.get(name,{}).get('valueConstants',[]):
            if dep not in parent: parent[dep]=name;queue.append(dep)
    paths={}; details={}
    for short in targets:
        found=[n for n in constants if n.endswith('.'+short) or n==short]
        assert len(found)==1,(short,found)
        name=found[0]; assert name in parent,name
        path=[]; node=name
        while node is not None: path.append(node); node=parent[node]
        paths[name]=path[::-1];details[name]=constants[name]
    receipt={'new_modules':len(new),'new_compressed_bytes':sum(r['bytes'] for r in new),'total_modules':len(files),'constants':len(constants),'seconds':round(time.monotonic()-start,3),'peak_rss_bytes':peak,'command':command,'paths':paths,'details':details,'scope':'Fresh cached-value extraction, not a full local kernel replay; positive paths do not establish necessity.'}
    (OUT/"paper_route_receipt.json").write_text(json.dumps(receipt,ensure_ascii=False,indent=2),encoding='utf-8')
    print('PAPER_ROUTE_PATHS',len(paths),'OF',len(targets),'NEW_MODULES',len(new),'BYTES',sum(r['bytes'] for r in new),'PEAK_MIB',round(peak/1024**2,2))
    for name,path in paths.items(): print(name,' <- '.join(path[::-1]))

if __name__=='__main__':main()
