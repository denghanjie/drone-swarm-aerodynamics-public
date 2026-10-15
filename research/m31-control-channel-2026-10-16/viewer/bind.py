"""Presentation adapter for terminal saved evidence only; no operational imports."""
from pathlib import Path
import json,hashlib
b=Path(__file__).resolve().parents[1];v=b/'viewer'
def load(n):return json.loads((b/n).read_text())
def descriptor(n):
 data=(b/n).read_bytes();return {'path':'../'+n,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
r=load('results/result.json');review=load('review/results/report.json');d=load('publication/FINAL-DISPOSITION.json')
assert r['terminal'] and review['terminal'] and d['diagnosticTerminal'] and d['savedReviewTerminal']
assert r['kind']=='synthetic-control-channel-diagnostic' and not r['scientificSuccess']
events=[json.loads(line) for line in (b/'raw/trace.public.ndjson').read_text().splitlines()]
def refs(kind):return [{'file':'raw/trace.public.ndjson','event':e['id'],'kind':kind} for e in events if e['kind']==kind]
def state(value):return 'yes' if value else 'no' if r['localObservationComplete'] else 'unknown'
ret=r['returned'];persist=r['persistence'];verified=d['scopedPublicRecordIntegrityVerified'];success=d['narrowEngineeringObservationSupported']
stages=[
 {'name':'Page payload','observed':state(ret['validationPassed']), 'detail':'The returned, validated envelope reports array-ready from the frozen page function. Its page-generated values are retained. There is no separate browser-phase event if the call does not return.', 'evidenceRefs':[{'file':'raw/returned.json','field':'constructionPhase / values'}]},
 {'name':'API return','observed':state(ret['received']), 'detail':f"One payload-bearing evaluate call was observed. Return received: {ret['received']}. No application payload HTTP request was observed. The host interval includes several kinds of work and is not a benchmark.", 'evidenceRefs':refs('control-evaluate-started')+refs('control-evaluate-returned')+refs('control-evaluate-error')},
 {'name':'Valid bytes','observed':state(ret['validationPassed']), 'detail':f"Strict representation validation passed: {ret['validationPassed']}. Actual returned bytes: {ret['bytes']}. The saved JSON represents decoded values, not protocol wire bytes.", 'evidenceRefs':refs('control-envelope-validated')+[{'file':'results/result.json','field':'returned'}]},
 {'name':'Closed file','observed':state(persist['complete'] and persist['equalsReturned']), 'detail':f"Exclusive file written and closed: {persist['complete']}. Bytes written: {persist['writtenBytes']}. The file matches the actual return: {persist['equalsReturned']}. Matching expected fixture bytes is checked separately.", 'evidenceRefs':refs('persistence-started')+refs('persistence-write')+refs('persistence-completed')},
 {'name':'Independent check','observed':'yes' if verified and review['transferSuccess'] else 'no' if verified else 'unknown', 'detail':f"Saved-public-evidence review: {sum(g['pass'] for g in review['groups'])}/{len(review['groups'])} groups passed. Independent post-closure exact-byte comparison passed: {review['transferSuccess']}. Actual external review exit is retained; private trace transformation was not independently reconstructed.", 'evidenceRefs':[{'file':'review/results/report.json','field':'byteEvidence / groups'},{'file':'publication/review-execution.json','field':'actualCheckerExitCode'},{'file':'publication/FINAL-DISPOSITION.json','field':'scopedPublicRecordIntegrityVerified'}]}
]
names=['results/result.json','raw/trace.public.ndjson','raw/returned.json','raw/received.bin','results/wrapper.json','results/budget.json','results/capture.json','publication/capture-execution.json','publication/capture-output.json','publication/observer-output.json','review/results/report.json','review/results/summary.json','review/evidence-manifest.json','publication/review-execution.json','publication/review-output.json','publication/FINAL-DISPOSITION.json','payload.json','payload.bin','freeze.json']
names=[n for n in names if (b/n).exists()]
artifact={'schema':'m31-transport-view-v1','sourceCommit':r['sourceCommit'],'sourceFreezeSHA256':r['sourceFreezeSHA256'],'summary':{'outcome':'Exact small-payload transfer observed once' if success else 'Narrow transfer not established','review':'Independent saved-byte review passed' if verified else 'Review incomplete or failed','status':'Bound to actual terminal records and external completion. Ordinary heap only; no GPU or flight computation.','interpretation':'This single 3,840-byte payload returned through the existing automation connection and was saved exactly, with an independent post-closure comparison. It supports this small engineering path; it does not validate GPU lifetime, large-transfer cost, general reliability or aerodynamics.' if success else 'Inspect the saved records for the observed boundary. No positive transfer conclusion is established.'},'stages':stages,'events':events,'files':[descriptor(n) for n in names]}
data=(json.dumps(artifact,indent=2,ensure_ascii=False)+'\n').encode()
with (v/'evidence.json').open('xb') as f:f.write(data)
with (v/'binding.json').open('x') as f:json.dump({'path':'./evidence.json','bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()},f,indent=2);f.write('\n')
print(json.dumps({'events':len(events),'stages':len(stages),'backingFiles':len(names),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}))
