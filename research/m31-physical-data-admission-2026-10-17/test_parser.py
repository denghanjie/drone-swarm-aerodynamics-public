"""Synthetic parser-only checks; no measured files/network/model calls."""
from pathlib import Path
import hashlib
import json
import runpy
import sys

p = Path(__file__).resolve().parent
m = runpy.run_path(str(p/'audit.py'))
r = [0.0]*30
r[13] = 1
r[4] = 1
r[18:22] = [.5]*4
r[22] = 4
s = r.copy()
s[0] = 1e6
s[1] = 1
def make(rows):
    return ('# '+m['HEADER']+'\n'+'\n'.join(','.join(str(x) for x in row) for row in rows)+'\n').encode()
a = m['describe'](make([r,s]))
assert a['structuralEligible']
assert a['timeScales']['preprocessing_us']['positionVelocityComponentRmseMps'] == 0
assert a['timeScales']['header_ms']['positionVelocityComponentRmseMps'] > .5
s2 = s.copy()
s2[13] = 2
assert not m['describe'](make([r,s2]))['structuralEligible']
s3 = s.copy()
s3[0] = 0
assert not m['describe'](make([r,s3]))['structuralEligible']
s4 = s.copy()
s4[1] = float('nan')
progress = {}
try:
    m['describe'](make([r,s4]), progress=progress)
    raise RuntimeError('missed nonfinite')
except AssertionError:
    assert progress['rows'] == 2 and progress['nonfiniteValues'] == 1
    assert progress['finiteValues'] == 59 and not progress['structuralEligible']
progress = {}
try:
    m['describe'](make([r,s]).replace(b'time[ms]',b'time[sec]'), progress=progress)
    raise RuntimeError('missed schema')
except AssertionError:
    assert not progress['schemaMatches'] and not progress['structuralEligible']
out = {'scope':'synthetic parser fixtures; no measured data', 'passed':5,
       'checks':['exact constant velocity with two fixed units','nonunit quaternion flagged','duplicate time flagged','nonfinite refusal retains counts','schema refusal retains witness'],
       'auditSha256':hashlib.sha256((p/'audit.py').read_bytes()).hexdigest()}
with Path(sys.argv[1]).open('x') as f:
    json.dump(out,f,indent=2)
    f.write('\n')
print(json.dumps(out))
