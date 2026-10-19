from pathlib import Path
import subprocess,os,json,time
base=Path(__file__).resolve().parent.parent
start=time.monotonic()
with (base/'supervisor-launch.lock').open('x') as f:f.write('One attempt; 210 second cap.\n')
try:
 r=subprocess.run([os.environ['M31_NODE'],str(base/'source/run.cjs')],timeout=210,capture_output=True,text=True)
 report={'returncode':r.returncode,'stdout':r.stdout.replace(str(base.parent.parent),'[repository]')[-2000:],'stderr':r.stderr.replace(str(base.parent.parent),'[repository]')[-2000:],'wallSeconds':time.monotonic()-start}
except subprocess.TimeoutExpired:report={'timeout':True,'wallSeconds':time.monotonic()-start}
with (base/'supervisor.json').open('x') as f:json.dump(report,f,indent=2)
print(json.dumps(report))
