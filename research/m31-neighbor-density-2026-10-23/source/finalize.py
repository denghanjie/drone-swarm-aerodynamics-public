from common import *
import traceback
out=Output('finalize','finalize');code=0
try:
 gate(False)
 for p in ('producer','audit'):prior(p)
 for p in ('results','audit'):
  e=load(BASE/p/'exit.json');assert e['closed'] and e['exitCode']==0 and not (BASE/p/'failure.json').exists()
 a=load(BASE/'audit/audit.json');assert a['passed'] and a['stages']==1920 and a['nativeCalls']==0
 def pin(rel):
  raw=(BASE/rel).read_bytes();return {'file':rel,'bytes':len(raw),'sha256':sha(raw)}
 pins={k:pin(rel) for k,rel in {'data':'results/stages.jsonl','summary':'results/summary.json','audit':'audit/audit.json','producer':'producer-supervisor.json','auditor':'audit-supervisor.json'}.items()}
 expected={p['file']:p for p in a['filePins']}
 for rel in ('results/stages.jsonl','results/summary.json'):assert pin(rel)==expected[rel]
 raw=canonical(pins);assert len(raw)<65536
 with (BASE/'viewer/pins.json').open('xb') as f:assert f.write(raw)==len(raw)
 out.save('report.json',{'passed':True,'closed':True,'pins':pins,'readEvents':EVENTS})
except Exception as e:
 code=1;out.failed=True;out.save('failure.json',{'type':type(e).__name__,'message':str(e).replace(str(ROOT),'[repository]')[:1000]})
finally:out.close(code)
sys.exit(code)
