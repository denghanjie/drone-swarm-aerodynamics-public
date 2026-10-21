from pathlib import Path
import json,hashlib,subprocess,os,sys
if sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE'):raise RuntimeError('optimized-Python-not-permitted')
B=Path(__file__).resolve().parent.parent
assert (B/'finalize-supervisor-launch.lock').exists();(B/'finalize').mkdir()
sha=lambda b:hashlib.sha256(b).hexdigest()
def write(p,x):
 with p.open('x') as f:json.dump(x,f,indent=2);f.write('\n')
gates=[]
def gate():
 code="const C=require(process.argv[1]);let passed=false,error=null;try{C.gate();passed=true;}catch(e){error=String(e.message).replaceAll(C.root,'[repository]');process.exitCode=1;}finally{console.log(JSON.stringify({passed,error,readEvents:C.events}));}"
 r=subprocess.run([os.environ['M31_NODE'],'-e',code,str(B/'source/gate.cjs')],capture_output=True,text=True)
 try:record=json.loads(r.stdout)
 except Exception:record={'passed':False,'error':'gate-output-unavailable','returncode':r.returncode}
 gates.append(record)
 (B/'finalize/gates.json').write_text(json.dumps(gates,indent=2)+'\n')
 assert r.returncode==0 and record['passed']
try:
 gate()
 for phase in ['producer','audit']:
  s=json.loads((B/(phase+'-supervisor.json')).read_text());assert s['returncode']==0 and s['allocationWallPassed'] and s['outputCapPassed'] and not s.get('timeout')
 a=json.loads((B/'audit/audit.json').read_text());assert a['passed']
 for p in ['results/exit.json','audit/exit.json']:
  e=json.loads((B/p).read_text());assert e['exitCode']==0 and e['closed']
 assert not (B/'audit/failure.json').exists() and not (B/'results/failure.json').exists()
 ix=json.loads((B/'results/index.json').read_text());assert ix['complete'] and not ix.get('failure')
 pins={}
 for key,rel in [('audit','audit/audit.json'),('data','audit/viewer-data.json'),('producer','producer-supervisor.json'),('auditSupervisor','audit-supervisor.json')]:
  raw=(B/rel).read_bytes();pins[key]={'file':rel,'bytes':len(raw),'sha256':sha(raw)}
 assert pins['data']['sha256']==a['viewerPin']['sha256'] and pins['data']['bytes']==a['viewerPin']['bytes']
 write(B/'viewer/pins.json',pins);assert (B/'viewer/pins.json').stat().st_size<=65536
 gate()
 write(B/'finalize/report.json',{'passed':True})
except Exception as e:
 write(B/'finalize/failure.json',{'type':type(e).__name__,'error':str(e).replace(str(B.parent.parent),'[repository]').replace(os.environ.get('M31_NODE','__unset__'),'[node runtime]')});raise
