"""External60s limit for each of the two preallocated commands; no retry."""
import json,os,pathlib,subprocess,sys,time
base=pathlib.Path(__file__).resolve().parents[1]
mode=sys.argv[1]
assert mode in ['evaluate','audit','ui']
folder=base/'results';folder.mkdir(exist_ok=True)
with (folder/(mode+'-supervisor.lock')).open('x') as f:f.write('one invocation\n')
t=time.monotonic()
try:
    cmd=[os.environ['M31_NODE'],str(base/'source/ui.cjs')] if mode=='ui' else [sys.executable,'-I','-B',str(base/'source'/ (mode+'.py'))]
    p=subprocess.run(cmd,cwd=base,timeout=60,capture_output=True)
    result={'mode':mode,'exitCode':p.returncode,'elapsedSeconds':time.monotonic()-t,'timeout':False}
    (folder/(mode+'-stdout.txt')).write_bytes(p.stdout);(folder/(mode+'-stderr.txt')).write_bytes(p.stderr)
except subprocess.TimeoutExpired as e:
    result={'mode':mode,'exitCode':None,'elapsedSeconds':time.monotonic()-t,'timeout':True}
    (folder/(mode+'-stdout.txt')).write_bytes(e.stdout or b'');(folder/(mode+'-stderr.txt')).write_bytes(e.stderr or b'')
(folder/(mode+'-supervisor.json')).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
sys.exit(0 if result['exitCode']==0 else 1)
