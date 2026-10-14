#!/usr/bin/env python3
"""Recovery tooling written after artifact loss; never execute the supplied HTML/JS.
Extract JSON literals with Python's strict decoder; retain each literal verbatim.
Decode embedded text/module strings as UTF-8 without newline changes.
"""
from pathlib import Path
import hashlib, json, posixpath, re
from datetime import datetime, timezone

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
SOURCE=ROOT/'attached-viewer/temporal-airflow-evidence(1).html'
EXPECTED='622ad9c80779dfef9434b92fc18cbc5d57c7b85a340e76a0a42dc0c2e0b54115'
raw=SOURCE.read_bytes()
sha=lambda b:hashlib.sha256(b).hexdigest()
gitsha=lambda b:hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
assert sha(raw)==EXPECTED, 'Attachment identity mismatch'
s=raw.decode('utf-8')
def strict_obj(pairs):
    out={}
    for k,v in pairs:
        if k in out: raise ValueError('Duplicate JSON key: '+k)
        out[k]=v
    return out
D=json.JSONDecoder(object_pairs_hook=strict_obj,parse_constant=lambda x:(_ for _ in ()).throw(ValueError(x)))
def ws(i):
    while i<len(s) and s[i] in ' \r\n\t':i+=1
    return i
def entries(start):
    """Return full object, its end, and value spans without executing content."""
    obj,end=D.raw_decode(s,start)
    assert isinstance(obj,dict) and s[start]=='{'
    out=[];i=ws(start+1)
    while s[i]!='}':
        key,j=D.raw_decode(s,i); assert isinstance(key,str)
        j=ws(j);assert s[j]==':';a=ws(j+1)
        value,b=D.raw_decode(s,a);out.append((key,value,a,b));i=ws(b)
        if s[i]==',':i=ws(i+1)
        else:assert s[i]=='}'
    assert i+1==end and list(obj)==[x[0] for x in out]
    return obj,end,out
marker='const sources='
assert s.count(marker)==1
start=s.index(marker)+len(marker)
maps={};spans={};allentries={}
for index,name in enumerate(('sources','data','texts')):
    if index:
        marker=','+name+'='
        assert s[start:start+len(marker)]==marker
        start+=len(marker)
    maps[name],end,allentries[name]=entries(start)
    spans[name]=(start,end);start=end
assert s[start:start+2]==';\n'
assert {k:len(v) for k,v in maps.items()}=={'sources':4,'data':30,'texts':5}

def write(relative,body):
    p=HERE/relative;p.parent.mkdir(parents=True,exist_ok=True)
    if p.exists():assert p.read_bytes()==body, f'Refusing different overwrite: {p}'
    else:p.write_bytes(body)
    assert p.read_bytes()==body
    return {'path':relative,'bytes':len(body),'sha256':sha(body)}

tree=json.loads((ROOT/'github/campaign-tree.json').read_text())
prefix='research/campaign-temporal-sampling/implementation/'
tree_by_path={e['path']:e for e in tree['tree'] if e['type']=='blob'}
originals=ROOT/'github/recovered'
files=[];unique={}
for name in maps:
    a,b=spans[name]
    meta=write('literal-maps/'+name+'.json',s[a:b].encode('utf-8'))
    meta.update({'sourceUtf8ByteStart':len(s[:a].encode('utf-8')),'sourceUtf8ByteEndExclusive':len(s[:b].encode('utf-8'))})
    spans[name]=meta
    for key,value,a,b in allentries[name]:
        rel=posixpath.normpath(posixpath.join('demo',key))
        assert not rel.startswith('../') and not rel.startswith('/')
        body=s[a:b].encode('utf-8') if name=='data' else value.encode('utf-8')
        rec=write('recovered/'+rel,body)
        if rec['path'] in unique:assert unique[rec['path']]==rec['sha256']
        unique[rec['path']]=rec['sha256']
        rec.update({'embeddedMap':name,'embeddedKey':key,
          'recoveryMethod':'verbatim JSON value literal; reconstructed file representation, original file whitespace/encoding not claimed' if name=='data' else 'exact decoded JSON string, UTF-8, no added newline',
          'sourceValueUtf8ByteStart':len(s[:a].encode('utf-8')),'sourceValueUtf8ByteEndExclusive':len(s[:b].encode('utf-8')),
          'originalFileBytesVerified':False})
        if name=='data':assert D.decode(body.decode())==value
        else:assert body.decode()==value
        original=tree_by_path.get(prefix+rel)
        if original:
            rec['priorUploadedGitBlobSha1']=original['sha']
            rec['originalFileBytesVerified']=gitsha(body)==original['sha']
            rec['matchesPriorUploadedFileBytes']=rec['originalFileBytesVerified']
            local=originals/(prefix+rel)
            if local.exists() and name=='data':
                rec['matchesPriorUploadedJsonSemantics']=D.decode(local.read_text())==value
        files.append(rec)

# The IO writer returns the exact sidecar object that coupled.persist stores in
# denseStates. Copy those existing nested objects verbatim, never derive fields.
nested=[]
for key,value,a,b in allentries['data']:
    if '/runs/' not in key:continue
    assert value['commonStates']==maps['data']['../'+value['commonStates']['path']+'.json']
    if 'denseStates' not in value:continue
    _,_,props=entries(a)
    prop=next(p for p in props if p[0]=='denseStates');_,v,aa,bb=prop
    rec=write('recovered/'+v['path']+'.json',s[aa:bb].encode('utf-8'))
    rec.update({'embeddedMap':'data','embeddedKey':key,'jsonPointer':'/denseStates',
       'recoveryMethod':'verbatim nested JSON sidecar object; reconstructed standalone file representation',
       'originalFileBytesVerified':False,'semanticIdentityBasis':'src/io.cjs:22-23 returns saved sidecar object; src/coupled.cjs:51 stores it as denseStates',
       'sourceValueUtf8ByteStart':len(s[:aa].encode('utf-8')),'sourceValueUtf8ByteEndExclusive':len(s[:bb].encode('utf-8'))})
    assert D.decode((HERE/rec['path']).read_text())==v
    nested.append(rec)

c=maps['data']['../results/campaign.json'];m=maps['data']['../results/matrix-status.json'];sc=maps['data']['../results/cadence-screens.json'];sup=maps['data']['../results/supervisor.json'];viewer=maps['data']['./records.json']
assert c['status']==viewer['status']=='reference-not-established'
assert c['gates']==viewer['gates']
assert [x['passed'] for x in c['gates']['physics']]==[True,True]
assert [x['passed'] for x in c['gates']['air']]==[False,False]
assert all([r['key'] for r in x['rows'] if not r['magnitudePassed']]==['velocityMps','attitudeRad','angularVelocityRadps'] for x in c['gates']['air'])
assert all(r['reductionPassed'] for x in c['gates']['air'] for r in x['rows'])
assert sc['referenceQualified'] is False and len(sc['cadenceScreens'])==5
assert all(x['qualified'] is False and x['cadence_qualified'] is False for x in sc['cadenceScreens'])
assert m['freshCompleted']==10 and m['freshSkipped']==4 and m['cadenceQualification']=='none'
assert sum(r['status']=='completed' for r in m['rows'])==10
assert sum(r['status']=='skipped_by_failed_airflow_reference_gate' for r in m['rows'])==4
assert len(c['runIds'])==11 and len(viewer['runs'])==10 and len(viewer['replay'])==2
assert all(x['referenceQualified'] is False and len(x['rows'])==5 and all(y['qualified'] is False and y['quadraturePassed'] for y in x['rows']) for x in viewer['replay'])
assert sup['elapsedWallMs']==51135.539888 and sup['code']==0 and sup['killed'] is None
assert '51.136 s' in maps['texts']['../REPORT.md']
assert len([k for k in maps['data'] if '/runs/' in k])==10
assert all(v['complete'] and v['stop'] is None for k,v in maps['data'].items() if '/runs/' in k)
assert sha(maps['texts']['../PLAN.md'].encode())==maps['data']['../FREEZE.json']['planSha256']

checks={'description':'Recovery-time checks of existing records only; no simulation, field evaluation, gate recomputation from arrays, or regenerated numerical evidence.',
 'status':'passed','physicsGates':[{'seed':x['seed'],'passed':x['passed']} for x in c['gates']['physics']],
 'airflowGates':[{'seed':x['seed'],'passed':x['passed'],'failedAbsoluteCaps':[r['key'] for r in x['rows'] if not r['magnitudePassed']],'allReductionChecksPassed':all(r['reductionPassed'] for r in x['rows'])} for x in c['gates']['air']],
 'referenceQualified':False,'qualifiedCadenceCount':0,'attemptedCoupledRunCount':len(c['runIds']),'freshCompleted':m['freshCompleted'],'freshSkipped':m['freshSkipped'],'compatibilityPreflights':1,
 'conditionalReplayDriverCount':len(viewer['replay']),'conditionalQuadratureRowsPassed':10,'supervisedElapsedWallMs':sup['elapsedWallMs'],'supervisedElapsedWallSecondsRounded3dp':'51.136',
 'workerCheckpointElapsedWallMs':c['resources']['elapsedWallMs'],'exitCode':sup['code'],'watchdogKilled':sup['killed'],
 'tenStandaloneCommonSidecarsMatchNestedObjects':True,'frozenPlanSha256Matches':True,
 'executionValidityIsNotReferenceQualification':True,'note':'The 51.136 s value is the external supervised window. Instrumented per-run loop timings exclude later serialization and are not process CPU times.'}

# Inventory only what is documented by preserved references and stored records.
missing=[
 ('implementation/results/replay/s840131-p1-a4.json','full original replay record','REPORT.md conditional-record link; campaign replayRunIds; viewer has only selected summaries/traces'),
 ('implementation/results/replay/s840137-p1-a4.json','full original replay record','REPORT.md conditional-record link; campaign replayRunIds; viewer has only selected summaries/traces'),
 ('implementation/results/runs/s4301-p16-a64.json','full compatibility coupled-run record','campaign.runIds and matrix-status.compatibilityRun; compatibility summary survives'),
 ('implementation/results/raw/s4301-p16-a64.states.f64.gz.json','compatibility common-state sidecar','RAW-RETENTION-MANIFEST files'),
 ('implementation/results/replay/s840131-p1-a4.fresh-inflow.f64.gz.json','fresh-inflow sidecar','RAW-RETENTION-MANIFEST files; partial identity/shape metadata survives there'),
 ('implementation/results/replay/s840137-p1-a4.fresh-inflow.f64.gz.json','fresh-inflow sidecar','RAW-RETENTION-MANIFEST files; partial identity/shape metadata survives there'),
 ('implementation/results/recomputed/reference-gates.json','original recomputed gate records','frozen src/evaluate.cjs:11 writes this alongside verification.json; original gate summaries survive in campaign.json'),
 ('implementation/results/last-checkpoint.json','original last durable execution checkpoint','frozen src/coupled.cjs:19 and src/replay.cjs:11 save checkpoint objects; none embedded'),
 ('implementation/results/recomputed/verification.json','original independent raw-reconstruction receipt','REPORT.md link'),
 ('implementation/results/invocation.json','original invocation record','REPORT.md link'),
 ('implementation/viewer-qa/browser-check.json','original browser-check failure receipt','REPORT.md link'),
 ('coordination/CLAIM-EVIDENCE-LEDGER.md','final publication ledger','README.md link'),
 ('coordination/dense-transport-parts.json','original dense transport manifest','README.md link'),
 ('coordination/packaging/reconstruct_dense.py','original dense reconstruction utility','README.md command'),
 ('implementation/publication-history/pre-label-correction/','original prior-label artifact history','README.md names directory but individual original filenames are not established')]
missing_rows=[]
for path,kind,basis in missing:
    assert 'research/campaign-temporal-sampling/'+path not in tree_by_path
    missing_rows.append({'campaignRelativePath':path,'kind':kind,'evidence':basis,'status':'not present in attachment or recovered uploaded tree; not recreated'})

manifest={'schema':'embedded-evidence-recovery/v1','createdAt':'2026-10-13T23:22:06Z','timestampSource':'clock.curr_time; recovery metadata assembly','createdDuringRecovery':True,
 'scope':'Post-loss recovery metadata, not an original campaign result or original audit. Read-only parsing/hash checks only; no remote writes or simulations.',
 'immutableSource':{'path':str(SOURCE.relative_to(ROOT.parent)),'bytes':len(raw),'sha256':sha(raw),'matchesProvidedOriginalSha256':True,'unchangedAfterExtraction':sha(SOURCE.read_bytes())==EXPECTED},
 'mapping':'Embedded relative URLs are resolved against implementation/demo/; recovered/ is the implementation directory. JSON file outputs retain exact original literal slices from the attachment, but do not claim byte identity with the lost pretty-printed original files.',
 'counts':{'moduleStringEntries':4,'directJsonRecords':30,'textStringEntries':5,'uniqueTextFiles':4,'directUniqueOutputFiles':len(unique),'additionalNestedDenseSidecars':len(nested)},
 'literalMaps':spans,'additionalRecoveryEvidence':['JSON-FORMAT-RECONSTRUCTION.json','REMOTE-BLOB-VERIFICATION.json'],'files':files,'nestedRecoveredSidecars':nested,
 'limitations':['Full original replay records are absent; viewer-selected summaries and traces are not substitutes.',
 'Two dense sidecar objects survive nested in full fresh-run records and are extracted separately with explicit provenance.',
 'The compatibility and two inflow sidecars are absent as full objects. Retention-manifest entries provide partial metadata only.',
 'The final REPORT.md is preserved as embedded text, including its historical retention claims; those claims describe the prior archive and must not be mistaken for current recovery completeness.',
 'Unknown later review, ledger, packaging, and QA filenames cannot be comprehensively inventoried from this attachment.',
 'References to missing files were not rewritten and no absent numerical evidence was generated.',
 'Raw binary payloads are not embedded; they are separately represented by uploaded tree 62e8d56e6500228cc536f6966d921697ec0bc3ad and outside this extraction.'],
 'knownMissing':missing_rows,'checks':checks,
 'existingSourceTree':{'treeSha':tree['sha'],'localRoot':'../github/recovered','reviewFilesAlreadyRecovered':[e['path'] for e in tree['tree'] if e['type']=='blob' and '/review/' in e['path']],
 'robustnessReportsAlreadyRecovered':[e['path'] for e in tree['tree'] if e['type']=='blob' and '/robustness/' in e['path'] and e['path'].endswith('.md')]}}
# Metadata is new. It can be deterministically refreshed except for the timestamp.
(HERE/'RECOVERY-MANIFEST.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
(HERE/'VERIFICATION.json').write_text(json.dumps(checks,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
assert sha(SOURCE.read_bytes())==EXPECTED
print(json.dumps({'status':'ok','counts':manifest['counts'],'knownMissingCount':len(missing_rows),'manifest':str(HERE/'RECOVERY-MANIFEST.json'),'checks':checks},indent=2))
