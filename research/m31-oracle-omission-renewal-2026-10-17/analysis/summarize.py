"""Saved-only descriptive counts; no imports of scientific or analysis methods."""
from pathlib import Path
import hashlib,json
p=Path(__file__).resolve().parents[1]
c=json.loads((p/'results/check.json').read_text());a=json.loads((p/'results/analyze.json').read_text())
assert c['passed'] is True and c['firstFailure'] is None
rows=[]
for s in c['outcomes']:
 for q in s['summary']:
  n=s['positiveTerms']
  rows.append({'state':s['id'],'tier':q['tier'],'positiveTerms':n,'optimisticCeiling':q['optimisticCeiling'],'singletonFeasible':q['singletonFeasible'],'ceilingPercent':100*q['optimisticCeiling']/n if n else None,'T8PositiveCovered':q['trees']['T8']['positiveCovered'],'T2PositiveCovered':q['trees']['T2']['positiveCovered'],'ceilingBelowTenPercent':n>0 and 10*q['optimisticCeiling']<n})
all_equal=all(t['ceilingCount']==t['singletonFeasibleCount'] for s in a['states'] for r in s['rows'] for t in r['tiers'])
summary={'schema':'m31-oracle-descriptive-summary-v1','sourceCommit':'ea2c963ea9a3e9af1eecaaeefe3739bf0082d0d5','scope':'Exact saved counts plus descriptive percentages; six dependent states, no population estimate or timing comparison','sourcePins':[{'file':f,'sha256':hashlib.sha256((p/'results'/f).read_bytes()).hexdigest()} for f in ['analyze.json','check.json']],'rows':rows,'all4608LowerAndUpperPrefixCountsEqual':all_equal,'everyStateBelowTenPercentEvenAtStressTier':all(q['ceilingBelowTenPercent'] for q in rows if q['tier']=='1e-2'),'decision':'Stop this fixed tau/16 coefficient-mass omission policy; investigate direct final-load error before a practical grouping solver. No load tolerance or speed claim.'}
with (p/'analysis/summary.json').open('x') as f:json.dump(summary,f,indent=2);f.write('\n')
print(json.dumps({k:summary[k] for k in ['all4608LowerAndUpperPrefixCountsEqual','everyStateBelowTenPercentEvenAtStressTier']}))
