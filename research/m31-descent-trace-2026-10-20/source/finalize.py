import common as C
B=C.BASE
assert (B/'finalize-supervisor-launch.lock').exists()
(B/'finalize').mkdir()
try:
 C.gate();a=C.load(B/'audit/report.json');assert a['passed'] and a['samples']==1924
 for phase in ['extract','audit']:
  s=C.load(B/(phase+'-supervisor.json'));assert s['returncode']==0 and s['allocationWallPassed'] and s['outputCapPassed'] and not s.get('timeout')
 assert not (B/'results/failure.json').exists() and not (B/'audit/failure.json').exists()
 pins={}
 for key,rel in [('audit','audit/report.json'),('data','results/view-data.json'),('extract','extract-supervisor.json'),('auditSupervisor','audit-supervisor.json')]:
  raw=(B/rel).read_bytes();pins[key]={'file':B.relative_to(C.ROOT).as_posix()+'/'+rel,'bytes':len(raw),'sha256':C.sha(raw)}
 assert pins['data']['sha256']==a['viewPin']['sha256'] and pins['data']['bytes']==a['viewPin']['bytes']
 assert C.write(B/'viewer/pins.json',pins)['bytes']<=65536
 C.gate();C.write(B/'finalize/report.json',{'passed':True,'readEvents':C.EVENTS})
except Exception as e:
 C.write(B/'finalize/failure.json',{'type':type(e).__name__,'error':str(e).replace(str(C.ROOT),'[repository]'),'readEvents':C.EVENTS});raise
