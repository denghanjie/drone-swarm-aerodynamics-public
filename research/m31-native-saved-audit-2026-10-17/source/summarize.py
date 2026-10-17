from pathlib import Path
from fractions import Fraction
import json,hashlib
root=Path.cwd();p=root/'research/m31-native-saved-audit-2026-10-17'
source=p/'results/check.json';r=json.loads(source.read_bytes());old=root/'research/m31-native-load-baseline-2026-10-17/results/browser.json';b=json.loads(old.read_bytes())
def q(x):return Fraction(int(x['n']),int(x['d']))
cats=('rotor','collective','worldForce','worldMoment');rows=[]
for call in r['calls']:
 rows.append({'caseId':call['caseId'],'method':call['method'],'qualified':call['qualified'],'positiveTerms':call['support']['nativePositiveCount'],'errorUpperDisplay':{k:float(q(call['errors'][k]['normalizedError']['u'])) for k in cats},'allExactSquaredUpperPass':all(q(call['errors'][k]['normalizedSquaredError']['u'])<=Fraction(1,10**16) for k in cats)})
summary={'schema':'m31-native-saved-summary-v1','scope':'Projection of saved checker records only; decimal bounds are display approximations, decisions use exact rationals in check.json.','checkSha256':hashlib.sha256(source.read_bytes()).hexdigest(),'browserSha256':hashlib.sha256(old.read_bytes()).hexdigest(),'originalSupervisorStatus':'failed','separateSavedAuditDecision':r['decision'],'qualifiedCalls':r['qualifiedTargetCalls'],'all48ExactCategoryUpperChecksPass':all(x['allExactSquaredUpperPass'] for x in rows),'rows':rows,'maxErrorUpperDisplay':{k:max(x['errorUpperDisplay'][k] for x in rows) for k in cats},'fixtureCount':len(r['arithmeticFixtures']),'corruptionCount':len(r['corruptionChecks']),'newBrowserCallsDuringAudit':0,'performanceClaim':False,'physicalValidationClaim':False}
with (p/'results/summary.json').open('x') as f:json.dump(summary,f,indent=2);f.write('\n')
print(json.dumps(summary,indent=2))
