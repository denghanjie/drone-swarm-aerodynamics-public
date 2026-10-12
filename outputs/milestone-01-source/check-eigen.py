from pathlib import Path
import json
p=Path(__file__).resolve().parent;exec((p/'eigen.py').read_text().split('root=')[0])
root=p.parent;rows=json.loads((root/'milestone-01-sensitivity-matrices.json').read_text());checks=[]
for r in rows:
    a=eigen(r['halfDifference'])[0]['magnitude'];b=eigen(r['halfStep'])[0]['magnitude'];change=max(abs(a-r['originalRadius']),abs(b-r['originalRadius']))
    assert change<1e-6 and (a>1)==(b>1)==(r['originalRadius']>1)
    checks.append({'gains':r['name'],'momentScale':r['momentScale'],'original':r['originalRadius'],'halfDifference':a,'halfStep':b,'maxChange':change})
v=json.loads((root/'milestone-01-verification.json').read_text());v['checks'].append({'name':'Boundary stability classifications survive numerical refinement','passed':True,'detail':checks});(root/'milestone-01-verification.json').write_text(json.dumps(v,indent=2));print(str(sum(c['passed'] for c in v['checks']))+' numerical checks passed; 1 trajectory-convergence limitation retained; maximum eigenvalue radius change:',max(r['maxChange'] for r in checks))
