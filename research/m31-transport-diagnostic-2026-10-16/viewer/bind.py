"""Bind already saved diagnostic records for presentation; never executes a runner."""
from pathlib import Path
import hashlib,json
BASE=Path(__file__).resolve().parents[1]
VIEW=BASE/'viewer'
def load(name):
    return json.loads((BASE/name).read_bytes())
def descriptor(name):
    b=(BASE/name).read_bytes()
    return {'path':'../'+name,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
worker=load('results/result.json')
review=load('review/results/review.json')
execution=load('publication/capture-execution.json')
review_execution=load('publication/review-execution.json')
events=[json.loads(line) for line in (BASE/'raw/trace.public.ndjson').read_bytes().splitlines()]
assert worker['kind']=='synthetic-transport-diagnostic' and worker['terminal'] is True
assert review['kind']=='new-transport-public-saved-review'
assert events and all(x['sequence']==i+1 for i,x in enumerate(events))
assert worker['scientificSuccess'] is False and worker['explainsHistoricalFailure'] is False
def refs(kind):
    return [{'file':'raw/trace.public.ndjson','event':e['id'],'kind':kind} for e in events if e['kind']==kind]
healthy=worker['instrumentation']['complete']
browser=worker['browserResult']
def state(yes):
    return 'yes' if yes else 'no' if healthy and browser is not None else 'unknown'
stages=[
 {'name':'Known payload','observed':'yes' if refs('browser-payload-ready') else 'unknown',
  'detail':'The fixed fixture is 3,840 synthetic bytes. A browser payload-ready event records allocation; exact persistence is checked separately.',
  'evidenceRefs':refs('browser-payload-ready')+[{'file':'payload.json','field':'length / sha256'}]},
 {'name':'Fetch attempt','observed':'yes' if refs('browser-fetch-start') else 'unknown',
  'detail':f"The browser recorded {worker['fetchCalls']} pre-fetch reservation marker(s). This is an attempt boundary, not proof that an HTTP request reached the server.",
  'evidenceRefs':refs('browser-fetch-start')+[{'file':'results/result.json','field':'browserResult.attempted'}]},
 {'name':'Sink acceptance','observed':state(worker['sink']['started']),
  'detail':f"Actual server entries: {worker['sink']['postCount']} POST and {worker['sink']['optionsCount']} OPTIONS. Matching upload reservation accepted: {worker['sink']['started']}. Receipt of any request and acceptance of the matching POST are different stages.",
  'evidenceRefs':refs('sink-request')+refs('sink-post-started')+[{'file':'results/result.json','field':'sink'}]},
 {'name':'Exact file','observed':state(worker['persistence']['exact']),
  'detail':f"Saved file present: {worker['persistence']['exists']}. Retained bytes: {worker['persistence']['bytes'] if worker['persistence']['exists'] else 'none'}. Exact match to the frozen fixture: {worker['persistence']['exact']}. Review status above determines whether the independent saved-record check completed.",
  'evidenceRefs':[{'file':'results/result.json','field':'persistence'},{'file':'review/results/review.json','field':'exactSyntheticBytesPersisted'}]+refs('sink-persisted')},
 {'name':'Acknowledgement','observed':state(bool(browser and browser['acknowledged'])),
  'detail':f"Browser accepted the completion, length and hash receipt: {browser['acknowledged'] if browser else 'unknown'}. A server response-finish event alone does not establish that acknowledgement.",
  'evidenceRefs':refs('browser-receipt-matched')+refs('browser-fetch-error')+[{'file':'results/result.json','field':'browserResult'}]}
]
review_ok=(review.get('completed') is True and review.get('candidatePublicEvidenceVerified') is True
           and review_execution['toolSessionCompleted'] is True and review_execution['actualCheckerExitCode']==0
           and review_execution['actualFullElapsedSeconds']<30)
capture_ok=(execution['toolSessionCompleted'] is True and execution['actualCaptureExitCode']==0
            and execution['actualFullElapsedSeconds']<60)
labels={'synthetic-transfer-complete':'Synthetic transfer completed once',
        'exact-persistence-acknowledgement-failed':'File saved; acknowledgement failed',
        'sink-accepted-incomplete':'Upload accepted; persistence incomplete',
        'transfer-failed-before-sink-acceptance':'Transfer failed before upload acceptance',
        'incomplete':'Diagnostic incomplete'}
outcome=labels[worker['status']] if capture_ok else 'Diagnostic lacks complete external closure'
browser_blocks=[e for e in events if e['kind']=='cdp-loading-failed' and e['data'].get('corsError')=='LocalNetworkAccessPermissionDenied']
interpretation=('The exact synthetic payload reached the file and the browser accepted its receipt in this one recorded attempt.'
                if worker['status']=='synthetic-transfer-complete' and capture_ok else
                'The saved records locate the observed boundary for this single synthetic attempt. Inspect the trace for what the browser and server actually reported; the historical GPU failure remains unexplained.')
if browser_blocks and worker['status']=='transfer-failed-before-sink-acceptance' and capture_ok:
    interpretation='Chrome reported LocalNetworkAccessPermissionDenied for this synthetic request. The sink recorded one socket connection but no HTTP request, and no payload file was saved. This identifies a browser-reported boundary in this trial; it does not establish the historical GPU failure cause.'
    stages[1]['detail'] += ' The later browser failure event reports LocalNetworkAccessPermissionDenied.'
    stages[1]['evidenceRefs'] += refs('cdp-loading-failed')
names=['results/result.json','raw/trace.public.ndjson','results/budget.json','results/capture.json',
       'publication/capture-execution.json','publication/capture-output.json','publication/observer-output.json',
       'review/results/review.json','publication/review-execution.json','publication/review-output.json','payload.json','payload.bin']
if worker['persistence']['exists']: names.append('raw/received.bin')
artifact={'schema':'m31-transport-view-v1','sourceCommit':worker['sourceCommit'],
          'sourceFreezeSHA256':worker['sourceFreezeSHA256'],
          'summary':{'outcome':outcome,'review':'Public saved-record review passed' if review_ok else 'Saved-record review unverified or failed',
                     'status':'Bound to actual terminal records. Private raw traces were not independently reviewed by the saved-public-evidence checker.',
                     'interpretation':interpretation},'stages':stages,'events':events,'files':[descriptor(n) for n in names]}
data=(json.dumps(artifact,indent=2,ensure_ascii=False)+'\n').encode()
with (VIEW/'evidence.json').open('xb') as f: f.write(data)
binding={'path':'./evidence.json','bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
with (VIEW/'binding.json').open('x') as f: json.dump(binding,f,indent=2);f.write('\n')
print(json.dumps({'kind':'presentation-binding','bytes':len(data),'sha256':binding['sha256'],'events':len(events),'stages':len(stages)}))
