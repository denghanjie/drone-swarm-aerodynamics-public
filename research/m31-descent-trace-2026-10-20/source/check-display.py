import common as C
import json
try:
 C.LIMIT=150;C.gate()
 for phase in ['extract','audit','finalize']:
  s=C.load(C.BASE/(phase+'-supervisor.json'));assert s['returncode']==0 and s['allocationWallPassed'] and s['outputCapPassed'] and not s.get('timeout')
 for folder in ['results','audit','finalize']:assert not (C.BASE/folder/'failure.json').exists()
 assert C.load(C.BASE/'finalize/report.json')['passed']
 a=C.load(C.BASE/'audit/report.json');assert a['passed'] and a['samples']==1924
 pins=C.load(C.BASE/'viewer/pins.json')
 for p in pins.values():C.checked(C.ROOT/p['file'],p)
 assert pins['data']['sha256']==a['viewPin']['sha256'] and pins['data']['bytes']==a['viewPin']['bytes']
 print(json.dumps({'passed':True,'readEvents':C.EVENTS}))
except Exception as e:
 print(json.dumps({'passed':False,'error':str(e).replace(str(C.ROOT),'[repository]'),'type':type(e).__name__,'readEvents':C.EVENTS}));raise
