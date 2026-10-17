"""UI-only retained owned process-group leader; no research imports."""
from pathlib import Path
import json,os,select,signal,subprocess,sys,time
private=Path(os.environ['RESEARCH_QA_PRIVATE'])
child=subprocess.Popen([os.environ['RESEARCH_NODE'],sys.argv[1]])
recorded=False
while True:
    code=child.poll()
    if code is not None and not recorded:
        with (private/'exit.tmp').open('x') as f:json.dump({'exitCode':code},f);f.flush();os.fsync(f.fileno())
        (private/'exit.tmp').rename(private/'exit.json');recorded=True
    ready,_,_=select.select([sys.stdin.buffer],[],[],.1)
    if ready:
        command=os.read(sys.stdin.fileno(),1)
        if command==b'R' and recorded:break
        os.killpg(os.getpgrp(),signal.SIGKILL)
    if time.monotonic_ns()>=int(os.environ['RESEARCH_QA_DEADLINE_NS']):os.killpg(os.getpgrp(),signal.SIGKILL)
sys.exit(0)
