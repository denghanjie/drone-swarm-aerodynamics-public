"""One metadata-only final seal after actual scientific stage closure.

Reads saved Boolean decisions and hashes; never imports or recomputes science.
"""
from pathlib import Path
import hashlib,json,sys,time
p=Path(__file__).resolve().parent.parent;repo=p.parent.parent;out=p/'results';start=time.monotonic()
with (out/'qualification-seal.lock').open('x') as f:f.write('One metadata seal consumed. No repeat.\n')
r=dict(kind='terminal-browser-screen-qualification',sealSuccess=False,evidenceQualified=False,practicalRulePass=False,failureReasons=[],sourceFilesVerified=0,artifactPinsVerified=0,numericalReanalysis=False,scientificInvocationsAdded=0,inputs={})
def check(ok,msg):
    if not ok:raise ValueError(msg)
def guard():check(time.monotonic()-start<=20,'metadata-wall-cap')
def digest(f):
    h=hashlib.sha256()
    with f.open('rb') as s:
        for b in iter(lambda:s.read(1048576),b''):guard();h.update(b)
    return h.hexdigest()
def safe(base,name):
    x=Path(name);check(not x.is_absolute() and '..' not in x.parts,'nonrelative-pin');f=base/x
    check(f.is_file() and not f.is_symlink() and f.resolve().is_relative_to(base.resolve()),'missing-or-escaping-pin');return f
def verify(base,x):
    f=safe(base,x['path']);check(f.stat().st_size==x['bytes'] and digest(f)==x['sha256'],'artifact-pin-mismatch')
def load(name):
    f=safe(p,name);check(f.stat().st_size<=64*2**20,'metadata-size');r['inputs'][name]={'bytes':f.stat().st_size,'sha256':digest(f)}
    return json.loads(f.read_text(),parse_constant=lambda _:(_ for _ in ()).throw(ValueError('nonfinite-metadata')))
try:
    check(len(sys.argv)==3 and sys.flags.optimize==0,'metadata-arguments');source_sha,commit=sys.argv[1:];r.update(sourceCommit=commit,sourceManifestSha256=source_sha)
    manifest=load('source-manifest.json');check(r['inputs']['source-manifest.json']['sha256']==source_sha,'source-manifest-identity')
    for pin in manifest['files']:verify(repo,pin);r['sourceFilesVerified']+=1
    receipt=load('source-publication.json');check(receipt.get('commit')==commit and receipt.get('manifestSha256')==source_sha and receipt.get('remoteManifestMatchesLocal') is True and receipt.get('localAndCommittedPinsMatch') is True,'source-publication-receipt')
    gates={};elapsed=0
    for kind,cap in [('generation',900),('candidate',3000),('review',600)]:
        rec=load('results/'+kind+'-run.json');check(rec.get('sourceCommit')==commit and rec.get('sourceManifestSha256')==source_sha and rec.get('kind')==kind,'supervisor-identity')
        check(rec.get('closed') is True and rec.get('childGroupAbsent') is True and rec.get('ownedGroupAbsent') is True,'science-not-terminal')
        check(isinstance(rec.get('artifacts'),list),'artifact-list')
        paths=[x.get('path') for x in rec['artifacts']];check(len(paths)==len(set(paths)),'duplicate-artifact-pin')
        required={'inputs/index.json','results/generation-evidence.json','results/generation-child-invocation.lock'}
        if kind in ('candidate','review'):required|={'results/generation-run.json',*(f'runs/p{s}/closure.json' for s in range(3))}
        if kind=='review':required|={'results/candidate-run.json','results/independent-review.json','results/analysis.json'}
        check(required<=set(paths),'incomplete-supervisor-artifact-chain')
        check(rec.get('sourceReceiptSha256')==r['inputs']['source-publication.json']['sha256'],'stage-source-receipt-identity')
        for pin in rec['artifacts']:verify(p,pin);r['artifactPinsVerified']+=1
        ms=rec.get('elapsedSeconds',-1);elapsed+=ms
        memory=(0<rec.get('controllerPeakRSSBytes',0)<=512*2**20 and 0<rec.get('browserTreePeakRSSBytes',0)<=2*2**30 if kind=='candidate' else 0<rec.get('sampledPeakRSSBytes',0)<=1536*2**20)
        gates[kind+'ClosureQualified']=bool(rec.get('supervisorSuccess') is True and rec.get('returncode')==0 and rec.get('runtimeIdentityVerified') is True and rec.get('protectedInputsUnchanged') is True and rec.get('candidateOutputsUnchanged') is True and rec.get('rssSamples',0)>0 and memory and 0<=ms<=cap and 0<=rec.get('logBytes',-1)<=16*2**20 and not any(rec.get(k) for k in ['signals','monitorErrors','exception','cleanupError','finalizationError','finalWallCapExceeded','finalStorageCapExceeded']))
    r['supervisedScienceElapsedSeconds']=elapsed;gates['allocatedTotalWithin4500Seconds']=0<=elapsed<=4500
    for slot in range(3):
        rec=load(f'runs/p{slot}/closure.json');gates[f'p{slot}ClosureQualified']=bool(rec.get('processId')==f'p{slot}' and rec.get('slot')==slot and rec.get('complete') is True and rec.get('scientificScheduleComplete') is True and rec.get('closureConfirmed') is True and rec.get('allOwnedBrowserProcessesAbsent') is True and rec.get('browserClosed') is True and rec.get('runtimeIdentityVerified') is True and rec.get('inputsVerified') is True and rec.get('transportPending') is False and rec.get('errors')==[] and rec.get('sourceCommit')==commit and rec.get('sourceManifestSha256')==source_sha and 0<=rec.get('elapsedSeconds',-1)<=900)
    audit=load('results/independent-review.json');analysis=load('results/analysis.json')
    check(analysis.get('practicalRulePass') is None and analysis.get('requiresReviewSupervisorClosure') is True,'premature-analysis-qualification')
    check(analysis.get('performanceRulePass') is None or type(analysis.get('performanceRulePass')) is bool,'performance-boolean')
    gates['independentReviewPassed']=audit.get('pass') is True and audit.get('complete') is True and analysis.get('independentAuditPass') is True
    gates['performanceRuleAvailable']=type(analysis.get('performanceRulePass')) is bool
    r['gates']=gates;r['evidenceQualified']=all(gates.values());r['performanceRulePass']=analysis.get('performanceRulePass');r['practicalRulePass']=r['evidenceQualified'] and analysis['performanceRulePass'];r['failureReasons']=[k for k,v in gates.items() if not v]
    r['decision']='qualified-finite-chrome-center-screen' if r['practicalRulePass'] else 'rejected-fixed-browser-practical-rule' if r['evidenceQualified'] else 'unqualified-evidence';r['sealSuccess']=True
except Exception as exc:
    r['failureReasons'].append(str(exc) if type(exc) is ValueError else 'metadata-exception-'+type(exc).__name__);r['decision']='unqualified-metadata-seal'
r['elapsedSeconds']=time.monotonic()-start
if r['elapsedSeconds']>20:r.update(sealSuccess=False,evidenceQualified=False,practicalRulePass=False,decision='unqualified-metadata-seal');r['failureReasons'].append('metadata-final-wall-cap')
total=sum(f.stat().st_size for d in ['results','inputs','generation','runs'] for f in (p/d).rglob('*') if f.is_file());r['scientificBytesBeforeSealOutput']=total
while True:
    r['elapsedSeconds']=time.monotonic()-start
    if r['elapsedSeconds']>20 and 'metadata-final-wall-cap' not in r['failureReasons']:
        r.update(sealSuccess=False,evidenceQualified=False,practicalRulePass=False,decision='unqualified-metadata-seal');r['failureReasons'].append('metadata-final-wall-cap')
    payload=(json.dumps(r,indent=2,allow_nan=False)+'\n').encode();fits=len(payload)+(out/'qualification-seal.lock').stat().st_size<=2**20 and total+len(payload)<=2*2**30
    if fits or 'metadata-final-storage-cap' in r['failureReasons']:break
    r.update(sealSuccess=False,evidenceQualified=False,practicalRulePass=False,decision='unqualified-metadata-seal');r['failureReasons'].append('metadata-final-storage-cap')
with (out/'qualification.json').open('xb') as f:f.write(payload)
print(json.dumps({k:r[k] for k in ['sealSuccess','evidenceQualified','practicalRulePass','decision','failureReasons']}))
sys.exit(0 if r['sealSuccess'] else 1)
