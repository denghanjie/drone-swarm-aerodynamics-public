"""Run only inside an explicitly granted five-minute serial measurement window."""
import argparse,json,pathlib,subprocess,time
p=argparse.ArgumentParser();p.add_argument('--serial-lease',action='store_true',required=True);args=p.parse_args()
root=pathlib.Path(__file__).parent;start=time.monotonic();jobs=[]
for seed in [628791,628792]:
 for count in [100,200]:
  for family in ['sparse','dense','tilted']:jobs.append(dict(seed=seed,count=count,family=family,mode='field'))
for count in [1,100]:jobs.append(dict(seed=628791,count=count,family='zero',mode='field'))
jobs.append(dict(seed=628791,count=16,family='boids',mode='pipeline'))
ledger={'frozenHash':'6111d7a70a7ca60ed7404889042e4f0ad61c852794289fc6f5e95d67070c9189','selected':'lean','jobs':[],'complete':False}
try:
 for job in jobs:
  if time.monotonic()-start>230:raise RuntimeError('Remaining lease cannot safely fit a bounded job')
  config={**job,'selected':'lean','frozenHash':ledger['frozenHash']};at=time.monotonic()
  r=subprocess.run(['timeout','60s','node',str(root/'timing.cjs'),'--serial-lease','--config='+json.dumps(config,separators=(',',':'))],capture_output=True,text=True,timeout=65)
  entry={'config':config,'exit':r.returncode,'wallSeconds':time.monotonic()-at,'stdout':r.stdout,'stderr':r.stderr};ledger['jobs'].append(entry);ledger['wallSeconds']=time.monotonic()-start
  (root/'raw/independent-batch-ledger.json').write_text(json.dumps(ledger,indent=2))
  print(json.dumps({'config':job,'exit':r.returncode,'wallSeconds':entry['wallSeconds']}),flush=True)
  if r.returncode:raise RuntimeError('Job failed; partial result retained and batch stopped')
 ledger['complete']=True
except Exception as e:
 ledger['failure']={'type':type(e).__name__,'message':str(e)};raise
finally:
 ledger['wallSeconds']=time.monotonic()-start;(root/'raw/independent-batch-ledger.json').write_text(json.dumps(ledger,indent=2))
