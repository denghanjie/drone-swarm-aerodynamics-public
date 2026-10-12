from pathlib import Path
import hashlib,json,re
root=Path(__file__).resolve().parent.parent
src=root/'milestone-24-source'
p=json.loads((root/'milestone-24-protocol.json').read_text())
checks=[]
def check(name,ok):
 checks.append({'check':name,'passed':bool(ok)})
 if not ok: raise AssertionError(name)
check('Frozen numerical sources unchanged',all(hashlib.sha256((src/f).read_bytes()).hexdigest()==h for f,h in p['sourceHashes'].items()))
runs=[json.loads((src/f'run-{j["seed"]}-{j["count"]}-{j["mode"]}-{j["dt"]}.json').read_text()) for j in p['jobs']]
check('All 16 prescribed configurations exactly once',len(runs)==16 and len({(r['config']['seed'],r['config']['count'],r['config']['mode'],r['config']['dt']) for r in runs})==16 and all(all(r['config'][k]==j[k] for k in ['seed','count','mode','dt','duration']) for j,r in zip(p['jobs'],runs)))
check('Matched initial states for all paired cases',all(a['initial']==b['initial'] for a in runs for b in runs if (a['config']['seed'],a['config']['count'])==(b['config']['seed'],b['config']['count'])))
index=json.loads((src/'index.json').read_text())
check('12 primary replay entries resolve',len(index)==12 and all((src/e['file']).exists() for e in index))
for e in index:
 r=json.loads((src/e['file']).read_text()); last=r['frames'][-1]; expected=[r['metrics']['end']]+[v for s in r['final'] for v in s[:3]+s[6:10]]
 check(e['file']+' final frame and displayed metrics match',last==expected and e['metrics']==r['metrics'])
check('Main page matches milestone viewer',(root/'research-results.html').read_bytes()==(root/'milestone-24-lab.html').read_bytes())
for name in ['milestone-24-lab.html','milestone-24-report.md']:
 text=(root/name).read_text(); links=re.findall(r'href="([^"]+)"',text) if name.endswith('html') else re.findall(r'\]\(([^)]+)\)',text)
 check(name+' local links exist',all((root/l.split('#')[0]).exists() for l in links if not l.startswith(('http','#'))))
(root/'milestone-24-artifact-checks.json').write_text(json.dumps(checks,indent=2))
print(json.dumps({'checks':len(checks),'passed':sum(x['passed'] for x in checks)}))
