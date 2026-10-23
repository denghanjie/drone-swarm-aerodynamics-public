from common import *
out=Output('finalize','finalize');code=0
try:
 gate(False)
 for phase in ('producer','audit'):prior(phase)
 a=load(BASE/'audit/audit.json');assert a['passed'] and a['stages']==1920 and a['nativeCalls']==0
 for phase in ('results','audit'):
  e=load(BASE/phase/'exit.json');assert e['closed'] and e['exitCode']==0 and not (BASE/phase/'failure.json').exists()
 def pin(rel):
  raw=(BASE/rel).read_bytes();return {'file':rel,'bytes':len(raw),'sha256':sha(raw)}
 refs={'data':'../m31-neighbor-density-2026-10-23/results/stages.jsonl','priorSummary':'../m31-neighbor-density-2026-10-23/results/summary.json','diagnostic':'results/stages.jsonl','summary':'results/summary.json','audit':'audit/audit.json','producer':'producer-supervisor.json','auditor':'audit-supervisor.json'}
 pins={k:pin(v) for k,v in refs.items()};expected={p['file']:p for p in a['filePins']}
 for key in ('diagnostic','summary'):assert pins[key]==expected[pins[key]['file']]
 for key in ('data','priorSummary'):
  p=PINS[str((BASE/refs[key]).resolve().relative_to(ROOT))];assert pins[key]['bytes']==p['bytes'] and pins[key]['sha256']==p['sha256']
 raw=canonical(pins)
 with (BASE/'viewer/pins.json').open('xb') as f:assert f.write(raw)==len(raw)
 out.save('report.json',{'passed':True,'closed':True,'pins':pins,'readEvents':EVENTS})
except Exception as e:
 code=1;out.failed=True;out.save('failure.json',{'type':type(e).__name__,'message':str(e).replace(str(ROOT),'[repository]')[:1000]})
finally:out.close(code)
sys.exit(code)
