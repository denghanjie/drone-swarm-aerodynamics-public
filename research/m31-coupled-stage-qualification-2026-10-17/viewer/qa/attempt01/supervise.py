"""UI-only owned-process guard. No scientific imports."""
import os,signal,subprocess,time,json
from pathlib import Path
start=time.monotonic();out=Path(__file__).resolve().parent
if (out/'attempt.json').exists():raise SystemExit('single-use UI attempt')
with (out/'attempt.json').open('x') as f:json.dump({'status':'started','scientificCalls':0,'wallLimitSeconds':90},f)
p=None;result={'status':'failed','scientificCalls':0}
try:
    p=subprocess.Popen([os.environ['RESEARCH_NODE'],str(out/'run.cjs')],start_new_session=True)
    code=p.wait(timeout=max(.01,90-(time.monotonic()-start)))
    result.update(status='completed' if code==0 else 'failed',exitCode=code,childReaped=True)
except subprocess.TimeoutExpired:
    os.killpg(p.pid,signal.SIGKILL);p.wait(timeout=4)
    result.update(reason='UI timeout',childReaped=True)
finally:
    result['wallSeconds']=time.monotonic()-start
    with (out/'supervision.json').open('x') as f:json.dump(result,f,indent=2);f.write('\n')
raise SystemExit(0 if result['status']=='completed' else 1)
