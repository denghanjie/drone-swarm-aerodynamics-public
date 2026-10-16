"""Retained owned group leader with parent-pipe loss containment.

No scientific logic. Parent releases only after child exit and group inspection.
The leader kills its own group on parent-pipe EOF. SIGKILL of this guardian or
host suspension remains outside this ordinary userspace containment guarantee.
"""
import json, os, pathlib, select, signal, subprocess, sys, time
private=pathlib.Path(os.environ['RESEARCH_SUPERVISOR_DIR'])
child=subprocess.Popen(sys.argv[1:])
(private/'child.tmp').write_text(json.dumps({'pid':child.pid,'group':os.getpgrp()}))
(private/'child.tmp').rename(private/'child.json')
recorded=False
while True:
    code=child.poll()
    if code is not None and not recorded:
        with (private/'exit.tmp').open('x') as f:json.dump({'returncode':code},f)
        (private/'exit.tmp').rename(private/'exit.json')
        recorded=True
    ready,_,_=select.select([sys.stdin.buffer],[],[],.1)
    if ready:
        b=os.read(sys.stdin.fileno(),1)
        if b==b'R' and recorded:break
        os.killpg(os.getpgrp(),signal.SIGKILL)
sys.exit(0)
