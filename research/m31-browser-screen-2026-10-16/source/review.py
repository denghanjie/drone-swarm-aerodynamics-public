#!/usr/bin/env python3
"""Independent saved-only browser L/F audit. Source preparation is not run permission.

The supervised official review imports only pinned independent Python sources.
No browser/candidate/generator module is imported or evaluated by this checker.
"""
import argparse
import gzip
import hashlib
import importlib.metadata
import importlib.util
import json
import math
import os
import platform
import re
import resource
import statistics
import sys
import time
from pathlib import Path

CASES=[('n1000-s261701-t5',1000,261701),('n5000-s261702-t5',5000,261702),('n5000-s261703-t5',5000,261703)]
PROCESS_IDS=['p0','p1','p2']
COOPERATIVE_SECONDS=595
RSS_CAP=1610612736
ROOT_SCHEMA='m31-browser-screen-v1'
ANALYSIS_SCHEMA='m31-browser-screen-independent-analysis-v1'
INHERITED_SHA='09660f29649d2e33da4a87d051936f10e612d28bf4001f98380e5a3d79a97279'
REFERENCE_SHA='4b21e84674d0007e23641622aec52724bced4791fcca3c1b97d48189c21f6aeb'

# No scientific import is performed during source preparation. The official
# supervisor must verify publication/source/runtime identities before launching.
helper_path=Path(__file__).with_name('inherited-center-review.py')
if hashlib.sha256(helper_path.read_bytes()).hexdigest()!=INHERITED_SHA:
    raise RuntimeError('inherited independent helper pin mismatch')
if hashlib.sha256(Path(__file__).with_name('numeric-reference.py').read_bytes()).hexdigest()!=REFERENCE_SHA:
    raise RuntimeError('inherited independent reference pin mismatch')
_spec=importlib.util.spec_from_file_location('browser_pinned_independent_helpers',helper_path)
H=importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(H)
np=H.np
require=H.require
load_json=H.load_json
finite=H.finite

class Audit(H.Audit):
    """Per-process path scope; one campaign deadline and namespaced check ledger."""
    def __init__(self,package,campaign=None,process_id=None):
        super().__init__(package)
        self.campaign=campaign if campaign is not None else self
        self.process_id=process_id
        self.top=campaign.top if campaign is not None else package
        self.root=self.top.parent.parent
        if campaign is not None:
            self.started=campaign.started
            self.checks=campaign.checks
            self.errors=campaign.errors
        else:
            self.processes=[]
            self.cross_process=[]
            self.config={}
            self.runtime={}
            self.closures={}
    def guard(self):
        require(time.monotonic()-self.started<COOPERATIVE_SECONDS,'browser reviewer595-second cooperative cap')
        rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        if sys.platform!='darwin':rss*=1024
        require(rss<=RSS_CAP,'browser reviewer1.5GiB RSS cap')
    def check(self,ok,name,details=None):
        return super().check(ok,(self.process_id+'.' if self.process_id else '')+name,details)
    def path(self,base,relative):
        p=super().path(base,relative)
        require(not (base/relative).is_symlink(),'artifact symlink forbidden')
        return p

def shared_generation(audit):
    evidence=load_json(audit.path(audit.top,'results/generation-evidence.json'))
    audit.check(evidence.get('kind')=='fresh-browser-screen-input-generation' and evidence.get('complete') is True,'generation.complete-kind')
    audit.check(evidence.get('runtimeIdentityVerified') is True,'generation.runtime-identity-reported')
    index=load_json(audit.path(audit.top,'inputs/index.json'))
    audit.pin(audit.top,evidence['inputIndex'],'generation.input-index-pin')
    audit.check(evidence['inputIndex'].get('path')=='inputs/index.json','generation.input-index-path')
    H.compare_fields(audit,index,dict(kind='fresh-airflow-off-boids-states',shape=['vehicle',17],dtype='float64le'),'generation.input-index-contract')
    entries=index['cases'];summaries=evidence.get('generation',[])
    require([(x.get('id'),x.get('n'),x.get('seed')) for x in entries]==CASES,'fixed three shared generated inputs')
    audit.check([x.get('id') for x in summaries]==[x[0] for x in CASES],'generation.fixed-summary-order')
    for entry in entries:
        audit.guard();ident,n,seed=entry['id'],entry['n'],entry['seed']
        audit.check(entry.get('t')==5,'generation.'+ident+'.fixed-final-time')
        state=H.read_array(audit,entry,'<f8',17*n,ident+'.shared-input').reshape(n,17)
        require(entry.get('path')=='inputs/'+ident+'.f64' and entry.get('generationPath')=='generation/'+ident+'.json','shared generation paths')
        gen=load_json(audit.path(audit.top,entry['generationPath']))
        summary=next(x for x in summaries if x.get('id')==ident)
        audit.pin(audit.top,summary['pin'],ident+'.generation-summary')
        audit.pin(audit.top,entry['generationPin'],ident+'.generation-index-pin')
        audit.exact(entry['generationPin'],summary['pin'],ident+'.shared-generation-pin-agreement')
        audit.check(summary['pin'].get('path')==entry['generationPath'],'generation.'+ident+'.summary-path')
        audit.check(gen.get('id')==ident and gen.get('n')==n and gen.get('seed')==seed and gen.get('complete') is True and gen.get('initialMatches') is True,ident+'.generation-identity-complete')
        audit.check(summary.get('complete') is True and summary.get('generationMs')==gen.get('generationMs'),ident+'.generation-summary-match')
        H.compare_fields(audit,gen['config'],dict(seed=seed,count=n,mode='boids',dt=.0025,duration=5,search='grid',filter='wall-priority',course='factory-v1',airflow='off',observation='ideal'),ident+'.generator-config')
        audit.check(gen['metrics'].get('end')==5 and gen['metrics'].get('stopReason') is None and gen['metrics'].get('failure') is None,ident+'.generation-completed')
        initial=H.read_array(audit,gen['initial'],'<f8',17*n,ident+'.initial').reshape(n,17)
        final=H.read_array(audit,gen['final'],'<f8',17*n,ident+'.final').reshape(n,17)
        audit.check(state.tobytes()==final.tobytes(),ident+'.unaltered-shared-final-input')
        audit.check(np.all(np.isfinite(initial)) and np.all(np.isfinite(final)),ident+'.finite-complete17-states')
        poses=H.read_array(audit,gen['poses'],'<f8',26*(1+7*n),ident+'.poses').reshape(26,1+7*n)
        audit.check(gen['poses'].get('frames')==26 and gen['poses'].get('width')==1+7*n and np.all(np.isfinite(poses)),ident+'.26-finite-poses')
        frames=gen['frames'];require(len(frames)==26,'exact26framepins')
        for frame_index,pin in enumerate(frames):
            frame=H.read_array(audit,pin,'<f8',1+7*n,ident+'.frame.'+str(frame_index))
            audit.check(pin.get('t')==poses[frame_index,0] and frame.tobytes()==poses[frame_index].tobytes(),ident+'.frame-concatenation.'+str(frame_index))
        audit.numeric(poses[:,0],np.arange(26)/5,ident+'.pose-times',1e-12,0.)
        for index,source in [(0,initial),(-1,final)]:
            wanted=np.concatenate((source[:,:3],source[:,6:10]),axis=1)
            audit.check(poses[index,1:].tobytes()==wanted.tobytes(),ident+'.pose-endpoint.'+str(index))
        audit.exact(gen.get('recording'),dict(cadence=.2,streamed=True),ident+'.recording-cadence')
        audit.numeric([s['t'] for s in gen['samples']],np.arange(51)/10,ident+'.unchanged-metric-sample-times',1e-12,0.)
        audit.check(finite(gen.get('generationMs')) and gen['generationMs']>=0,ident+'.separate-generation-cost')
        state.flags.writeable=False
        audit.generation.append(dict(id=ident,n=n,seed=seed,state=state,entry=entry,generationMs=gen['generationMs']))
    audit.resources['generationEvidence']=dict(path='results/generation-evidence.json',sha256=audit.digest(audit.top/'results/generation-evidence.json'))
    return entries

def process_analysis(audit):
    """No pooled gate. A complete process supplies three separate six-pair tables."""
    out=dict(processId=audit.process_id,complete=False,cases=[],performanceRulePass=None,practicalRulePass=None)
    if len(audit.calls)!=42:return out
    primary=[]
    for ident,n,seed in CASES:
        rows=[r for r in audit.calls if r['id']==ident and not r['warmup']]
        grouped={(r['block'],r['method']):r for r in rows}
        require(len(grouped)==12,'six paired blocks per case')
        case=dict(id=ident,n=n,seed=seed,methods={},pairs={},practicalRulePass=None)
        all_phases=sorted(set().union(*(r['phasesMs'] for r in rows)))
        for method in 'LF':
            selected=[grouped[b,method] for b in range(6)]
            actual_phases=sorted(set().union(*(r['phasesMs'] for r in selected)))
            summaries={}
            for key,values in [('totalMs',[r['totalMs'] for r in selected])]+[(p,[r['phasesMs'][p] for r in selected]) for p in actual_phases]:
                summaries[key]=dict(values=values,median=statistics.median(values),min=min(values),max=max(values))
            summaries['screenCounts']=[r['screen'] for r in selected]
            summaries['actualPhaseNames']=actual_phases
            case['methods'][method]=summaries
        ratios=[grouped[b,'F']['totalMs']/grouped[b,'L']['totalMs'] for b in range(6)]
        differences=[grouped[b,'F']['totalMs']-grouped[b,'L']['totalMs'] for b in range(6)]
        median=statistics.median(ratios);wins=sum(r<1 for r in ratios)
        case['pairs']['F/L']=dict(blocks=list(range(6)),ratios=ratios,differencesMs=differences,medianPairedRatio=median,strictWins=wins,
            pairedTotalsMs=[dict(block=b,L=grouped[b,'L']['totalMs'],F=grouped[b,'F']['totalMs']) for b in range(6)],
            matchedPhaseDifferenceSumsMs={p:sum(grouped[b,'F']['phasesMs'].get(p,0.)-grouped[b,'L']['phasesMs'].get(p,0.) for b in range(6)) for p in all_phases},
            phaseDifferenceConvention='Absent phases contribute structural zero only to differences; absent method phase series are omitted.')
        case['gates']=dict(requiredPrimaryCase=n==5000,medianPairedRatioAtMost090=median<=.90,atLeast5StrictWins=wins>=5,
            complete42CallProcess=True,independentNumericalAudit=True,sharedGeneration=True,processClosure=True,crossProcessExactEquality=None,reviewSupervisorClosure=None)
        case['performanceRulePass']=median<=.90 and wins>=5
        if n==5000:primary.append(case['performanceRulePass'])
        out['cases'].append(case)
    out.update(complete=True,performanceRulePass=len(primary)==2 and all(primary))
    return out

def saved_process(audit,process_id):
    pa=Audit(audit.top/'runs'/process_id,audit,process_id);before=len(audit.errors)
    complete=False;summary=dict(processId=process_id,complete=False,cases=[],performanceRulePass=None,practicalRulePass=None)
    try:
        pa.evidence=load_json(pa.path(pa.package,'results/evidence.json'))
        process_provenance(pa)
        require(len(audit.errors)==before,'process browser provenance failed')
        pa.check(len(pa.evidence.get('qualification',[]))==6,'qualification.six-builds-and-solves')
        H.controls_review(pa);H.ownership_review(pa)
        require(len(audit.errors)==before,'process controls/ownership failed')
        for item in audit.generation:browser_independent_case(pa,item)
        pa.check(len(pa.frames)==3 and all(frame.get('complete') and frame.get('pass') for frame in pa.frames),'qualification.three-complete-independent-cases')
        require(len(audit.errors)==before,'process qualification failed')
        H.timing_review(pa,[x[0] for x in CASES]);pa.guard()
        require(len(audit.errors)==before,'process timing evidence failed')
        summary=process_analysis(pa);complete=True
    except Exception as error:
        pa.error('process-review-error',error)
        raise
    finally:
        summary.update(complete=complete,controls=pa.controls,qualification=pa.frames,validatedTimingRecords=len(pa.calls),
                       independentAuditPass=complete and len(audit.errors)==before,errors=audit.errors[before:])
        audit.processes.append(summary)
        # Do not retain three processes' large matrices/solution objects at once.
        pa.qualified.clear();pa.evidence.clear();pa.calls.clear()
    return summary

def compare_binary(audit,left,right,name,expected_bytes=None,compressed=False):
    """Complete streaming byte equality; hashes never replace comparison."""
    opener=gzip.open if compressed else open
    total=bad=0;first=None
    with opener(left,'rb') as lf,opener(right,'rb') as rf:
        while True:
            audit.guard();a=lf.read(1<<20);b=rf.read(1<<20)
            if not a and not b:break
            if len(a)!=len(b):
                bad+=abs(len(a)-len(b))
                if first is None:first=total+min(len(a),len(b))
            size=min(len(a),len(b))
            if a[:size]!=b[:size]:
                mismatch=np.flatnonzero(np.frombuffer(a[:size],dtype=np.uint8)!=np.frombuffer(b[:size],dtype=np.uint8))
                bad+=int(mismatch.size)
                if first is None:first=total+int(mismatch[0])
            total+=max(len(a),len(b))
            if expected_bytes is not None:require(total<=expected_bytes,'decompressed crossprocess symbol exceeds fixed shape')
    audit.check(bad==0 and (expected_bytes is None or total==expected_bytes),name,dict(comparedBytes=total,differingBytes=bad,firstDifferingByte=first,expectedBytes=expected_bytes))
    return bad==0 and (expected_bytes is None or total==expected_bytes)

def compare_values(audit,left,right,name):
    """Full recursively typed value comparison, preserving binary64 and -0 tokens."""
    missing=object();stack=[('$',left,right)];bad=leaves=0;first=[]
    while stack:
        audit.guard();path,a,b=stack.pop()
        if isinstance(a,dict) and isinstance(b,dict):
            for key in sorted(set(a)|set(b),reverse=True):stack.append((path+'.'+key,a.get(key,missing),b.get(key,missing)))
            continue
        if isinstance(a,list) and isinstance(b,list):
            for i in range(max(len(a),len(b))-1,-1,-1):stack.append((path+'['+str(i)+']',a[i] if i<len(a) else missing,b[i] if i<len(b) else missing))
            continue
        leaves+=1
        equal=a is not missing and b is not missing and H.canonical(a)==H.canonical(b)
        if not equal:
            bad+=1
            if len(first)<8:
                def atom(value):
                    if value is missing:return {'absent':True}
                    if isinstance(value,(dict,list)):return {'type':type(value).__name__,'length':len(value)}
                    return value
                first.append(dict(path=path,reference=atom(a),actual=atom(b)))
    audit.check(bad==0,name,dict(comparedLeaves=leaves,differingLeaves=bad,firstDifferences=first))
    return bad==0

def cross_process_review(audit):
    """Every saved scientific array/value is required equal to p0, separately p1/p2."""
    baseline=audit.top/'runs/p0'
    for process_id in PROCESS_IDS[1:]:
        root=audit.top/'runs'/process_id;before=len(audit.errors);name='cross.p0-vs-'+process_id
        for spec in H.expected_controls():
            ident=spec['id'];rel='results/control-'+ident+'.json'
            left=load_json(audit.path(baseline,rel));right=load_json(audit.path(root,rel))
            compare_values(audit,left,right,name+'.control.'+ident+'.all-scientific-values')
        left=load_json(audit.path(baseline,'results/ownership.json'));right=load_json(audit.path(root,'results/ownership.json'))
        for key in ('sequence','extraBuilds','retained','retainedInputBeforeTokens','retainedInputAfterTokens','retainedInputBeforeSha256','retainedInputAfterSha256','inputUnchanged','returnedStorageDisjoint','pass'):
            compare_values(audit,left[key],right[key],name+'.ownership.'+key)
        for ident,n,_ in CASES:
            for method in 'LF':
                rel='results/'+ident+'-'+method+'.json';left=load_json(audit.path(baseline,rel));right=load_json(audit.path(root,rel))
                keys=('id','label','n','input','admission','graph','certificate','symbolCounts','geometryWork','ordinaryLmax','assemblyStats','screen','solutions','matrixHash','solutionHash')
                compare_values(audit,{k:left[k] for k in keys},{k:right[k] for k in keys},name+'.'+ident+'.'+method+'.complete-scientific-metadata-and-solutions')
                for key in ('offsets','sources','K','a'):
                    lp=audit.pin(baseline,left['artifacts'][key],name+'.'+ident+'.'+method+'.reference-'+key)
                    rp=audit.pin(root,right['artifacts'][key],name+'.'+ident+'.'+method+'.actual-'+key)
                    compare_binary(audit,lp,rp,name+'.'+ident+'.'+method+'.all-'+key,expected_bytes=left['artifacts'][key]['bytes'])
                lp=audit.pin(baseline,left['artifacts']['symbols'],name+'.'+ident+'.'+method+'.reference-symbols')
                rp=audit.pin(root,right['artifacts']['symbols'],name+'.'+ident+'.'+method+'.actual-symbols')
                compare_binary(audit,lp,rp,name+'.'+ident+'.'+method+'.every-symbol',expected_bytes=4*n*n,compressed=True)
                rel='results/qualification-'+ident+'-'+method+'.json'
                lq=load_json(audit.path(baseline,rel));rq=load_json(audit.path(root,rel))
                compare_values(audit,{k:v for k,v in lq.items() if k not in ('qualificationComputeMs','persistence')},
                    {k:v for k,v in rq.items() if k not in ('qualificationComputeMs','persistence')},name+'.'+ident+'.'+method+'.qualification-scientific-values')
        for sequence in range(42):
            rel=f'results/call-{sequence:03d}.json';left=load_json(audit.path(baseline,rel));right=load_json(audit.path(root,rel))
            # Clock readings and the hashes of their raw serialization vary by process.
            omit={'totalMs','phasesMs','raw'}
            compare_values(audit,{k:v for k,v in left.items() if k not in omit},{k:v for k,v in right.items() if k not in omit},name+'.timing.'+str(sequence)+'.all-saved-nonclock-values')
        lr=audit.closures['p0']['pageResult']['sourceReceipt'];rr=audit.closures[process_id]['pageResult']['sourceReceipt']
        compare_values(audit,lr,rr,name+'.complete-source-and-adapter-receipt')
        audit.cross_process.append(dict(referenceProcess='p0',actualProcess=process_id,complete=True,**{'pass':len(audit.errors)==before},errors=audit.errors[before:]))


def campaign_analysis(audit,completed):
    passed=completed and not audit.errors and len(audit.processes)==3 and len(audit.cross_process)==2
    out=dict(schema=ANALYSIS_SCHEMA,independentAuditPass=passed,performanceRulePass=None,practicalRulePass=None,
        requiresReviewSupervisorClosure=True,scope='Three serial fresh processes of one pinned Chrome build on three shared newly generated frozen states; fixed warmed-query regime.',
        processes=audit.processes,crossProcess=audit.cross_process,caseProcessSpread=[],primaryCells=[],
        inference='All six primary case-by-process cells must pass. No pooled rescue, population confidence interval, cold-start, live-flight or cross-browser inference.')
    if not passed:return out
    for process in audit.processes:
        for case in process['cases']:
            case['gates']['crossProcessExactEquality']=True
            if case['n']==5000:
                out['primaryCells'].append(dict(processId=process['processId'],id=case['id'],medianPairedRatio=case['pairs']['F/L']['medianPairedRatio'],strictWins=case['pairs']['F/L']['strictWins'],performanceRulePass=case['performanceRulePass']))
    for ident,n,seed in CASES:
        cells=[next(c for c in process['cases'] if c['id']==ident) for process in audit.processes]
        medians=[c['pairs']['F/L']['medianPairedRatio'] for c in cells]
        out['caseProcessSpread'].append(dict(id=ident,n=n,seed=seed,processIds=PROCESS_IDS,processMedianPairedRatios=medians,min=min(medians),max=max(medians),range=max(medians)-min(medians),medianAcrossProcesses=statistics.median(medians),descriptiveOnly=True))
    out['performanceRulePass']=len(out['primaryCells'])==6 and all(cell['performanceRulePass'] for cell in out['primaryCells'])
    return out

# The inherited fresh-case audit, with truthful browser persistence.fsync=True.
def browser_independent_case(audit,item):
    ident,n,states=item['id'],item['n'],item['state'];before=len(audit.errors);bs={}
    for method in 'LF':
        doc=load_json(audit.path(audit.package,'results/'+ident+'-'+method+'.json'))
        audit.check(doc.get('id')==ident and doc.get('label')==method and doc.get('n')==n,ident+'.'+method+'.identity')
        bs[method]=H.bundle(audit,doc,ident+'.'+method);audit.qualified[(ident,method)]=bs[method]
    streams={method:gzip.open(bs[method]['symbolPath'],'rb') for method in 'LF'}
    hashes={method:hashlib.sha256() for method in 'LF'}
    def reader(i):
        rows=[]
        for method in 'LF':
            block=streams[method].read(4*n);require(len(block)==4*n,'truncated symbol artifact');hashes[method].update(block)
            rows.append(np.frombuffer(block,dtype=np.uint8).reshape(n,4))
        return rows
    try:
        model=H.independent_model(audit,states,bs['L'],bs['F'],ident,reader)
        for method in 'LF':
            audit.check(streams[method].read(1)==b'',ident+'.'+method+'.symbols-no-trailing')
            audit.check(hashes[method].hexdigest()==bs[method]['doc']['artifacts']['symbols']['rawSha256'],ident+'.'+method+'.raw-symbol-hash')
    finally:
        for stream in streams.values():stream.close()
    for key in ('solutions','matrixHash','solutionHash'):audit.exact(bs['L']['doc'][key],bs['F']['doc'][key],ident+'.exact-'+key)
    require(model['admission']['admitted'] and model['graph']['descendingEligible'],'fresh target solve-domain rejected')
    require(len(audit.errors)==before,'fresh independent geometry/equality failed before solve')
    residual=H.independent_solution(audit,bs['L']['doc']['solutions']['O'],states,model['g'],model['c'],model['off'],model['src'],model['a'],model['graph'],ident)
    for method in 'LF':
        b=bs[method];sol=b['doc']['solutions']['O'];values,*_=H.rotor_values(sol,n)
        require(np.all(np.isfinite(values)),'nonfinite saved solution')
        b['checksum']=H.saved_checksum(sol,b['k']);b['valuesLength']=len(values);b['stateHash']=item['entry']['sha256']
        selected=[r for r in audit.evidence.get('qualification',[]) if r.get('id')==ident and r.get('label')==method]
        require(len(selected)==1,'qualification identity multiplicity')
        rec=selected[0]
        audit.exact(rec,load_json(audit.path(audit.package,'results/qualification-'+ident+'-'+method+'.json')),ident+'.'+method+'.qualification-copy')
        audit.pin(audit.package,rec['persistence']['meta'],ident+'.'+method+'.qualified-meta')
        audit.check(rec['persistence']['meta']['path']=='results/'+ident+'-'+method+'.json',ident+'.'+method+'.meta-path')
        audit.check(rec.get('matrixHash')==b['doc']['matrixHash'] and rec.get('solutionHash')==b['doc']['solutionHash'],ident+'.'+method+'.qualification-fingerprints')
        H.comparison_report(audit,rec['comparison'],b,ident+'.'+method+'.qualification-comparison',True)
        H.mutation(audit,{**rec,'inputUnchanged':rec['comparison'].get('inputUnchanged')},states,ident+'.'+method+'.qualification-mutation')
        if method=='F':H.verify_omission_report(audit,rec['omissionAudit'],states,model['omitted'],ident+'.qualification')
        else:audit.check(rec.get('omissionAudit') is None,ident+'.L.no-screen-report')
        audit.check(rec.get('pass') is True,ident+'.'+method+'.qualification-pass')
        audit.check(finite(rec.get('qualificationComputeMs')) and rec['qualificationComputeMs']>=0 and finite(rec['persistence'].get('totalPersistenceMs')) and rec['persistence']['totalPersistenceMs']>=0,ident+'.'+method+'.separate-untimed-cost')
        H.compare_fields(audit,rec['persistence'],dict(fsync=True,directoryFsync=True,durableExclusiveCollector=True,fsyncScope='file content and parent directory after exclusive link/unlink publication'),ident+'.'+method+'.durable-exclusive-persistence')
    audit.frames.append(dict(id=ident,n=n,complete=True,symbolEntries=4*n*n,omittedOrderedPairs=model['omitted'],omittedRotorSymbolsChecked=4*model['omitted'],coefficientMaxAbs=model['maxError'],independentResidualLog=residual,**{'pass':len(audit.errors)==before}))


FIXED_LIMITS=dict(candidateWallSeconds=3000,candidateCooperativeSeconds=895,reviewWallSeconds=600,reviewCooperativeSeconds=595,
    rssBytes=1610612736,positiveTerms=2000000,normalScientificBytes=536870912,scientificBytes=553648128,
    compressedSymbolsBytesPerBundle=67108864,supervisorLogsBytes=16777216,scientificDirectoryBytes=2147483648,
    generationWallSeconds=900,generationCooperativeSeconds=895,generationBytes=67108864,normalGenerationBytes=62914560,
    controllerRSSBytes=536870912,browserTreeRSSBytes=2147483648,administrativeReserveBytes=16777216,reviewBytes=134217728,allocatedTotalSeconds=4500)
SCIENTIFIC_PINS={
    'kernel.cjs':'efc87f4c0f9d1a5a9b754d9d334ce295227a0cb01ce6980e4818313dd35d3bc8',
    'lean-anchor.cjs':'1b57d90d1ce1a45fe3e7f637cae57325861bfc37c907de4d4c6f9e1a79f1af96',
    'anchor-kernel.cjs':'c2ab29e4f53341706582d52149df96cd93323d3943ac145f288fbbae4de71a8a',
    'reference-excerpt.cjs':'ec71562d17db5b30497e2953adc75019c424c19a44e45b22fcbb3a4482096d1e',
    'controls.cjs':'bf54381ee7f4dab8fbb19e48ada7e11c0f6d129cec1bcd21e5ce5075fc91f1ba',
    'inherited-center-review.py':INHERITED_SHA,'numeric-reference.py':REFERENCE_SHA}

def scientific_files(audit):
    listing=[]
    for directory in ('inputs','generation','results','runs'):
        for path in (audit.top/directory).rglob('*'):
            if path.is_file():
                require(not path.is_symlink() and path.resolve().is_relative_to(audit.top),'scientific path symlink/escape')
                listing.append(path)
    return sorted(listing)

def verify_pin_inventory(audit,pins,name):
    require(isinstance(pins,list),'artifact inventory must be list')
    paths=set();total=0
    for index,pin in enumerate(pins):
        require(isinstance(pin,dict) and pin.get('path') not in paths,'duplicate/malformed artifact pin')
        audit.pin(audit.top,pin,name+'.'+str(index));paths.add(pin['path']);total+=pin['bytes']
    return paths,total

def stage_closure(audit,kind,cap,manifest_sha,source_commit):
    rec=load_json(audit.path(audit.top,'results/'+kind+'-run.json'))
    audit.check(rec.get('kind')==kind and rec.get('sourceCommit')==source_commit and rec.get('sourceManifestSha256')==manifest_sha,kind+'.source-identity')
    audit.check(rec.get('sourceReceiptSha256')==audit.digest(audit.top/'source-publication.json'),kind+'.publication-receipt-pin')
    for key in ('closed','childGroupAbsent','ownedGroupAbsent','supervisorSuccess','runtimeIdentityVerified','protectedInputsUnchanged','candidateOutputsUnchanged'):
        audit.check(rec.get(key) is True,kind+'.'+key)
    audit.check(rec.get('returncode')==0 and rec.get('survivingOwnedProcessCount')==0,kind+'.actual-successful-owned-process-closure')
    audit.check(rec.get('monitorErrors')==[] and rec.get('signals')==[] and isinstance(rec.get('exitRaces'),list),kind+'.monitor-and-cleanup-outcomes')
    audit.check(not any(rec.get(k) for k in ('exception','cleanupError','finalizationError','finalWallCapExceeded','finalStorageCapExceeded')),kind+'.no-terminal-failure')
    audit.check(rec.get('wallCapSeconds')==cap and finite(rec.get('elapsedSeconds')) and 0<=rec['elapsedSeconds']<=cap,kind+'.wall-cap')
    audit.check(type(rec.get('rssSamples')) is int and rec['rssSamples']>0 and rec.get('sampleIntervalSeconds')==.1 and finite(rec.get('sampledPeakRSSBytes')) and rec['sampledPeakRSSBytes']>0,kind+'.actual-positive-RSS-samples')
    if kind=='candidate':
        audit.check(rec.get('rssCapBytes') is None and rec.get('controllerRSSCapBytes')==FIXED_LIMITS['controllerRSSBytes'] and rec.get('browserTreeRSSCapBytes')==FIXED_LIMITS['browserTreeRSSBytes'],kind+'.declared-split-RSS-caps')
        audit.check(finite(rec.get('browserTreePeakRSSBytes')) and 0<rec['browserTreePeakRSSBytes']<=FIXED_LIMITS['browserTreeRSSBytes'],kind+'.whole-owned-browser-tree-RSS')
        audit.check(finite(rec.get('controllerPeakRSSBytes')) and 0<rec['controllerPeakRSSBytes']<=FIXED_LIMITS['controllerRSSBytes'],kind+'.controller-RSS')
        audit.check(rec['sampledPeakRSSBytes']>=max(rec['browserTreePeakRSSBytes'],rec['controllerPeakRSSBytes']),kind+'.sampled-sum-accounting')
        audit.check(rec.get('generationSupervisorSuccess') is True,kind+'.generation-predecessor-success')
    else:audit.check(rec.get('rssCapBytes')==RSS_CAP and rec['sampledPeakRSSBytes']<=RSS_CAP,kind+'.full-stage-RSS')
    audit.exact(rec.get('runtime'),audit.runtime,kind+'.pinned-runtime-record')
    paths,total=verify_pin_inventory(audit,rec.get('artifacts'),kind+'.closed-artifacts')
    audit.check(total==rec.get('scientificBytesBeforeClosure'),kind+'.closed-inventory-byte-accounting')
    audit.check(total+(audit.top/'results'/f'{kind}-run.json').stat().st_size<=FIXED_LIMITS['scientificDirectoryBytes'],kind+'.closed-directory-cap')
    logs=sum(pin['bytes'] for pin in rec['artifacts'] if pin['path'].endswith(('-stdout.txt','-stderr.txt')))
    audit.check(logs==rec.get('logBytes') and logs<=FIXED_LIMITS['supervisorLogsBytes'],kind+'.closed-log-accounting-cap')
    lock=audit.path(audit.top,'results/'+kind+'-invocation.lock');audit.check(lock.stat().st_size>0,kind+'.consumed-exclusive-allocation')
    audit.closures[kind]=rec
    return rec,paths

def browser_environment(audit,env,name):
    require(isinstance(env,dict),'browser host environment absent')
    audit.check(env.get('architecture')==audit.runtime['architecture'] and env.get('platform')==audit.runtime['platform'],name+'.platform')
    audit.check(env.get('headless') is True and env.get('renderingDuringTiming') is False and env.get('clock')=='performance.now monotonic milliseconds',name+'.declared-browser-timing-regime')
    audit.check(isinstance(env.get('cpuModel'),str) and type(env.get('logicalCores')) is int and env['logicalCores']>0 and finite(env.get('installedRAMBytes')) and env['installedRAMBytes']>0,name+'.host-hardware')
    load=env.get('loadAverage');audit.check(isinstance(load,list) and len(load)==3 and all(finite(x) and x>=0 for x in load),name+'.host-load')


def browser_provenance(audit,manifest_sha,source_commit):
    """Explicit browser contract; never invokes inherited Node provenance."""
    candidate=audit.closures['candidate'];phase=candidate.get('phaseClosures')
    require(isinstance(phase,list) and [x.get('path') for x in phase]==['runs/'+p+'/closure.json' for p in PROCESS_IDS],'exact three externally inventoried process closures')
    profiles=[];baseline_args=None;baseline_version=None;baseline_page=None
    expected_sources=['source/browser.html','source/browser-bundle.js','source/browser.js','source/source-bundle.json']
    shared_paths={str(p.relative_to(audit.top)) for d in ('inputs','generation') for p in (audit.top/d).rglob('*') if p.is_file()}
    for slot,process_id in enumerate(PROCESS_IDS):
        audit.guard();name='browser.'+process_id;pin=phase[slot]
        audit.pin(audit.top,pin,name+'.external-closure-pin')
        rec=load_json(audit.path(audit.top,pin['path']))
        audit.check(rec.get('processId')==process_id and rec.get('slot')==slot,name+'.fixed-slot')
        for key in ('attempted','complete','scientificScheduleComplete','closureConfirmed','runtimeIdentityVerified','browserClosed','allOwnedBrowserProcessesAbsent','inputsVerified'):
            audit.check(rec.get(key) is True,name+'.'+key)
        audit.check(rec.get('sourceCommit')==source_commit and rec.get('sourceManifestSha256')==manifest_sha,name+'.source-identity')
        audit.check(rec.get('processRegistryCount')==1 and rec.get('transportPending') is False and rec.get('errors')==[],name+'.single-launch-clean-transport')
        audit.check(finite(rec.get('elapsedSeconds')) and 0<rec['elapsedSeconds']<=900,name+'.slot-wall-cap')
        observation=rec.get('supervisorObservation',{})
        H.compare_fields(audit,observation,dict(processId=process_id,allOwnedBrowserProcessesAbsent=True,monitorHealthy=True),name+'.external-live-barrier')
        audit.check(type(observation.get('consecutiveEmptySamples')) is int and observation['consecutiveEmptySamples']>=2 and type(observation.get('samples')) is int and observation['samples']>0 and type(observation.get('observedBrowserProcessCount')) is int and observation['observedBrowserProcessCount']>0,name+'.external-actual-browser-observations')
        for key,cap in [('peakBrowserRSSBytes',FIXED_LIMITS['browserTreeRSSBytes']),('peakControllerRSSBytes',FIXED_LIMITS['controllerRSSBytes'])]:
            audit.check(finite(observation.get(key)) and 0<observation[key]<=cap,name+'.'+key)
        audit.check(H.valid_sha(rec.get('profileIdentitySha256')),name+'.private-profile-identity-hash');profiles.append(rec.get('profileIdentitySha256'))
        args=rec.get('launchArguments');require(isinstance(args,list) and all(isinstance(x,str) for x in args),'declared sanitized browser argument vector')
        audit.check(args.count('--user-data-dir=<private-fresh-profile>')==1 and not any(x.startswith('--js-flags') for x in args),name+'.fresh-profile-and-no-custom-JIT-flags')
        if baseline_args is None:baseline_args=args
        else:audit.exact(args,baseline_args,name+'.stable-launch-arguments')
        version=rec.get('browserRuntime');require(isinstance(version,dict),'running Browser.getVersion record')
        audit.check(rec.get('browserVersion')==audit.runtime['chrome']['version'] and version.get('product')=='Chrome/'+audit.runtime['chrome']['version'],name+'.actual-pinned-Chrome-build')
        audit.check(all(isinstance(version.get(k),str) and version[k] for k in ('protocolVersion','revision','userAgent','jsVersion')),name+'.actual-browser-engine-identity')
        if baseline_version is None:baseline_version=version
        else:audit.exact(version,baseline_version,name+'.same-running-browser-build-and-engine')
        page=rec.get('pageEnvironment');require(isinstance(page,dict),'actual page environment absent')
        audit.check(page.get('visibilityState') in ('visible','hidden') and type(page.get('crossOriginIsolated')) is bool and type(page.get('hardwareConcurrency')) is int and page['hardwareConcurrency']>0 and isinstance(page.get('userAgent'),str),name+'.actual-page-environment')
        if baseline_page is None:baseline_page=page
        else:audit.exact(page,baseline_page,name+'.same-page-environment')
        browser_environment(audit,rec.get('environmentStart'),name+'.start');browser_environment(audit,rec.get('environmentEnd'),name+'.end')
        for key in ('cpuModel','architecture','platform','logicalCores','installedRAMBytes','headless','renderingDuringTiming','clock'):
            audit.exact(rec['environmentStart'][key],rec['environmentEnd'][key],name+'.stable-'+key)
        source_pins=rec.get('sourceServedPins');require(isinstance(source_pins,list) and [x.get('path') for x in source_pins]==expected_sources,'fixed browser served source list')
        verify_pin_inventory(audit,source_pins,name+'.served-source-pins')
        requests=rec.get('servedRequests');require(isinstance(requests,list),'served request inventory')
        requested=set()
        for index,request in enumerate(requests):
            require(request.get('path') in set(expected_sources)|shared_paths,'browser request outside frozen source/shared-data list')
            audit.pin(audit.top,request,name+'.served-request.'+str(index));requested.add(request['path'])
        required_requests=set(expected_sources)-{'source/source-bundle.json'}
        required_requests|=shared_paths-{'inputs/index.json'}
        audit.check(required_requests<=requested,name+'.all-runtime-sources-and-shared-generation-data-served')
        result_files=[p for p in (audit.top/'runs'/process_id/'results').rglob('*') if p.is_file()]
        actual_bytes=sum(p.stat().st_size for p in result_files)
        audit.check(type(rec.get('artifactBytes')) is int and rec['artifactBytes']==actual_bytes and actual_bytes<=FIXED_LIMITS['normalScientificBytes'],name+'.normal-output-byte-accounting-cap')
        audit.check(actual_bytes<=FIXED_LIMITS['scientificBytes'] and not any(p.name.endswith('.partial') for p in result_files),name+'.total-reserve-cap-and-no-incomplete-artifacts')
        lock=load_json(audit.path(audit.top,'runs/'+process_id+'/invocation.lock'))
        audit.exact(lock,dict(processId=process_id,slot=slot,consumed=True),name+'.consumed-single-slot-lock')
        audit.check(rec.get('pageResult',{}).get('complete') is True,name+'.page-complete-reported')
        audit.closures[process_id]=rec
    audit.check(len(set(profiles))==3,'browser.three-distinct-profile-identities')
    campaign=load_json(audit.path(audit.top,'results/campaign.json'))
    H.compare_fields(audit,campaign,dict(complete=True,attempted=PROCESS_IDS,notAttempted=[],scientificCallsAddedOutsidePage=0),'browser.campaign')
    require([x.get('path') for x in campaign['sourcePins']]==expected_sources,'campaign served source names')
    verify_pin_inventory(audit,campaign['sourcePins'],'browser.campaign-source-pins')
    paths,_=verify_pin_inventory(audit,campaign['sharedPins'],'browser.campaign-shared-pins')
    audit.check(paths==shared_paths,'browser.shared-input-generation-inventory-complete')


def provenance_resources(audit):
    """Custom browser/schema gate. Missing/changed fields fail closed, never default."""
    cfg=load_json(audit.path(audit.top,'config.json'));audit.config=cfg
    audit.check([(x.get('id'),x.get('n'),x.get('seed')) for x in cfg.get('cases',[])]==CASES and all(x.get('t')==5 for x in cfg['cases']),'config.fixed-three-new5s-inputs')
    H.compare_fields(audit,cfg,dict(schema=ROOT_SCHEMA,methods=['L','F'],permutations=['LF','FL'],processes=PROCESS_IDS,blocks=6,controls=48,ownershipExtraBuilds=6,qualificationBuilds=6,qualificationSolves=6,warmupCalls=6,measuredCalls=36,totalCalls=42,
        ownershipSequence=H.OWNERSHIP,controlIds=[s['id'] for s in H.expected_controls()],controlSolvePolicy='untimed solve+residual iff admitted and descendingEligible; otherwise explicit no-solve reason'),'config')
    audit.exact(cfg['limits'],FIXED_LIMITS,'config.fixed-stage-and-aggregate-resource-limits')
    H.compare_fields(audit,cfg['generation'],dict(duration=5,dt=.0025,mode='boids',search='grid',filter='wall-priority',record=True,frameEvery=.2,factoryVariant='wide',expectedCourse='factory-v1',airflow='off',observation='ideal'),'config.unchanged-generator-supported26-frame-recording')
    audit.exact(cfg['screen'],dict(spanLimit=256,componentThreshold=4,runtimeGeneralEquivalenceProven=False),'config.unchanged-screen')
    H.compare_fields(audit,cfg['primary'],dict(ratio='F/L',maximumMedianPairedRatio=.9,minimumStrictWins=5,requiredCases=[x[0] for x in CASES if x[1]==5000]),'config.primary-per-process')
    H.compare_fields(audit,cfg['browser'],dict(headless=True,channel='chrome',launchTimeoutMs=20000,closeTimeoutMs=20000,slotWallSeconds=900,chunkBytes=4194304,timer='performance.now',renderingDuringTiming=False,detachedChrome=False),'config.browser')
    mf=audit.path(audit.top,'source-manifest.json');manifest=load_json(mf);manifest_sha=audit.digest(mf)
    source_pins=manifest.get('files');require(isinstance(source_pins,list) and source_pins,'complete frozen source manifest absent')
    seen=set()
    for index,pin in enumerate(source_pins):
        require(pin.get('path') not in seen,'duplicate source pin');seen.add(pin['path']);audit.pin(audit.root,pin,'source.'+str(index))
    prefix=str(audit.top.relative_to(audit.root));required_sources={str(p.relative_to(audit.root)) for p in (audit.top/'source').iterdir() if p.is_file() and p.suffix in ('.py','.cjs','.js','.html','.json')}
    required_sources|={prefix+'/'+name for name in ('config.json','runtime.json')}
    required_sources.add('outputs/milestone-31-source/sim.cjs')
    audit.check(required_sources<=seen,'source.all-local-runtime-generator-wrapper-checker-files-pinned')
    for name,sha in SCIENTIFIC_PINS.items():audit.check(audit.digest(audit.top/'source'/name)==sha,'source.unchanged-'+name)
    receipt=load_json(audit.path(audit.top,'source-publication.json'));source_commit=receipt.get('commit')
    audit.check(isinstance(source_commit,str) and re.fullmatch('[0-9a-f]{40}',source_commit) is not None and receipt.get('manifestSha256')==manifest_sha and receipt.get('remoteManifestMatchesLocal') is True and receipt.get('localAndCommittedPinsMatch') is True,'source.independent-publication-receipt')
    runtime=load_json(audit.path(audit.top,'runtime.json'));audit.runtime=runtime
    audit.check(runtime.get('kind')=='prospective-browser-screen-runtime-identity' and sys.platform==runtime.get('platform') and platform.machine()==runtime.get('architecture'),'runtime.actual-reviewer-platform')
    audit.check(sys.version==runtime['python']['version'] and sys.flags.optimize==runtime['flags']['pythonOptimize']==0,'runtime.actual-reviewer-python-version-flags')
    py=Path(sys.executable).resolve();audit.check(py.stat().st_size==runtime['python']['bytes'] and audit.digest(py)==runtime['python']['sha256'],'runtime.actual-reviewer-binary')
    dist=importlib.metadata.distribution('numpy');record=dist.read_text('RECORD')
    audit.check(np.__version__==dist.version==runtime['numpy']['version'] and record is not None and hashlib.sha256(record.encode('utf-8')).hexdigest()==runtime['numpy']['distributionRecordSha256'],'runtime.actual-independent-numpy')
    audit.check(runtime['flags'].get('nodeOptionsEmpty') is True and runtime['flags'].get('nodeExecArgvEmpty') is True,'runtime.declared-controller-generator-flags')
    audit.check(runtime['chrome'].get('version')==cfg['browser']['runtimeVersion']=='155.0.8059.80','runtime.fixed-Chrome-build')
    for group,key in [('chrome','appRelativePath'),('playwright','moduleRelativePath')]:
        pins=runtime[group].get('files');require(isinstance(pins,list) and pins,'runtime component pins absent')
        audit.check(len({pin.get(key) for pin in pins})==len(pins) and all(isinstance(pin.get(key),str) and type(pin.get('bytes')) is int and pin['bytes']>0 and H.valid_sha(pin.get('sha256')) for pin in pins),'runtime.'+group+'.component-pin-schema')
    audit.check({'launcher','framework','Info.plist'}<={pin.get('label') for pin in runtime['chrome']['files']},'runtime.Chrome-main-components-pinned')
    generation,generation_paths=stage_closure(audit,'generation',900,manifest_sha,source_commit)
    candidate,candidate_paths=stage_closure(audit,'candidate',3000,manifest_sha,source_commit)
    audit.check(generation.get('phaseClosures')==[],'generation.no-browser-process-slots')
    generation_expected={str(f.relative_to(audit.top)) for d in ('inputs','generation') for f in (audit.top/d).rglob('*') if f.is_file()}
    generation_expected|={'results/'+name for name in ('generation-child-invocation.lock','generation-evidence.json','generation-invocation.lock','generation-stdout.txt','generation-stderr.txt')}
    audit.check(generation_paths==generation_expected,'generation.complete-successful-closed-artifact-inventory')
    audit.check(generation_paths<=candidate_paths,'candidate.preserves-all-generation-artifacts')
    current_files=scientific_files(audit)
    expected_candidate_paths={str(path.relative_to(audit.top)) for path in current_files if not (path.parent==audit.top/'results' and (path.name.startswith('review-') or path.name in ('candidate-run.json','independent-review.json','analysis.json','qualification.json')))}
    audit.check(candidate_paths==expected_candidate_paths,'candidate.complete-closed-artifact-inventory')
    browser_provenance(audit,manifest_sha,source_commit)
    bytes_total=sum(path.stat().st_size for path in current_files)
    logs=sum(path.stat().st_size for path in current_files if path.name.endswith(('-stdout.txt','-stderr.txt')))
    audit.check(bytes_total<=FIXED_LIMITS['scientificDirectoryBytes']-FIXED_LIMITS['administrativeReserveBytes'] and logs<=FIXED_LIMITS['supervisorLogsBytes'],'review.current-total-with-administrative-reserve-and-logs')
    generation_data=sum(p.stat().st_size for d in ('inputs','generation') for p in (audit.top/d).rglob('*') if p.is_file())
    generation_evidence=audit.top/'results/generation-evidence.json'
    generation_child_lock=audit.path(audit.top,'results/generation-child-invocation.lock')
    audit.check(generation_child_lock.read_text()=='single frozen generation invocation; do not replace or retry\n','generation.consumed-child-allocation')
    generation_data+=generation_evidence.stat().st_size+generation_child_lock.stat().st_size
    audit.check(generation_data<=FIXED_LIMITS['normalGenerationBytes'],'generation.normal-output-cap')
    ge=load_json(generation_evidence)
    audit.check(ge.get('newGenerationBytesBeforeEvidence')==generation_data-generation_evidence.stat().st_size,'generation.output-byte-accounting')
    prior_seconds=generation['elapsedSeconds']+candidate['elapsedSeconds']
    audit.check(prior_seconds<FIXED_LIMITS['allocatedTotalSeconds'],'review.remaining-positive-campaign-time')
    lock=audit.path(audit.top,'results/review-invocation.lock');audit.check(lock.stat().st_size>0,'review.sole-invocation-consumed')
    audit.resources.update(sourceCommit=source_commit,sourceManifestSha256=manifest_sha,generationExternalElapsedSeconds=generation['elapsedSeconds'],candidateExternalElapsedSeconds=candidate['elapsedSeconds'],priorStageElapsedSeconds=prior_seconds,
        reviewExternalCapSeconds=600,reviewCooperativeCapSeconds=595,reviewRssCapBytes=RSS_CAP,candidateBrowserTreePeakRSSBytes=candidate['browserTreePeakRSSBytes'],candidateControllerPeakRSSBytes=candidate['controllerPeakRSSBytes'],
        directoryBytesBeforeReview=bytes_total,logsBytesBeforeReview=logs,actualReviewSupervisorClosure=None,
        rssInterpretation='Candidate cap applies separately to sampled browser-tree sum and controller; candidate total sum is not constrained by the ordinary1.5GiB stage cap.')

ADAPTER_GROUPS=[
 ('zero-allocation',['length-8','uint8array-instance','all-zero','empty-supported']),
 ('one-fill',['length-7','all-one']),
 ('fresh-storage',['distinct-buffers','dedicated-views','mutation-isolated','methods-own-nonenumerable']),
 ('float64-le',['one-write-return8','one-bytes','one-read','negative-zero-write-return16','negative-zero-bytes','negative-zero-read']),
 ('float64-special',['nan-return8','nan-roundtrip','positive-infinity-return8','positive-infinity-roundtrip','negative-infinity-return8','negative-infinity-roundtrip']),
 ('uint64-le',['zero-return8','zero-bytes','zero-read','pattern-return16','pattern-bytes','pattern-read','maximum-return24','maximum-bytes','maximum-read']),
 ('offset-rejection',['read-f64-negative','read-f64-fractional','read-f64-overrun','write-f64-negative','write-f64-fractional','write-f64-overrun','read-u64-negative','read-u64-fractional','read-u64-overrun','write-u64-negative','write-u64-fractional','write-u64-overrun','empty-read-f64','empty-read-u64']),
 ('value-rejection',['uint64-negative','uint64-overflow','uint64-number','float64-string']),
 ('allocation-rejection',['negative-size','fractional-size','nan-size','infinite-size','over-limit-size','unsupported-fill2','string-fill'])]
SOURCE_IDS=['./reference-excerpt.cjs','./anchor-kernel.cjs','./lean-anchor.cjs','./kernel.cjs','./controls.cjs']
FACTORY_IDS=['./kernel.cjs','./anchor-kernel.cjs','./reference-excerpt.cjs','./lean-anchor.cjs','./controls.cjs']
ACCOUNTING_TIMES=['sourceLoadMs','inputFetchDecodeMs','artifactEncodingMs','base64EncodingMs','hashMs','gzipMs','transportAckMs','eventLoopYieldMs']
ACCOUNTING_COUNTS=['hashBytes','hashCalls','gzipInputBytes','gzipOutputBytes','eventLoopYields']
ACCOUNTING_NOTES='Query timers exclude loader, controls, qualification, input generation/transfer/decode, comparisons, encoding, hashes, gzip, transport, durable persistence and event-loop turns. Inclusive phase totals overlap detailed counters; do not sum them as disjoint components.'

def source_bundle_review(audit):
    spec=load_json(audit.path(audit.top,'source/source-bundle.json'))
    require(spec.get('path')=='/source/browser-bundle.js','fixed source bundle path')
    raw=audit.pin(audit.top,{**spec,'path':'source/browser-bundle.js'},'browser.source-bundle').read_bytes()
    require(len(raw)<=1<<20,'source bundle byte cap')
    sources=spec.get('sources');require(isinstance(sources,list) and [x.get('id') for x in sources]==SOURCE_IDS,'five fixed scientific module slices')
    previous=0
    for source in sources:
        at,size=source.get('offset'),source.get('bytes');name=source['id'][2:]
        require(type(at) is int and type(size) is int and size>0 and previous<=at and at+size<=len(raw),'source slice bounded ordered nonoverlap')
        payload=raw[at:at+size];original=audit.path(audit.top,'source/'+name).read_bytes()
        audit.check(payload==original and hashlib.sha256(payload).hexdigest()==source.get('sha256')==SCIENTIFIC_PINS[name],'browser.source-slice.'+name)
        previous=at+size
    adapter=load_json(audit.path(audit.top,'source/adapter-controls-spec.json'))
    H.compare_fields(audit,adapter,dict(schema='m31-browser-buffer-controls-v1',expectedGroups=9,expectedChecks=56,groupIds=[x[0] for x in ADAPTER_GROUPS],expectedFactoryExecutionIds=FACTORY_IDS),'browser.adapter-source-spec')
    audit.exact(adapter.get('groups'),[dict(id=ident,expectedChecks=len(checks),checkIds=checks) for ident,checks in ADAPTER_GROUPS],'browser.adapter-fixed-ordered56-source-spec')
    audit.source_bundle=spec


def source_receipt(audit,receipt,name):
    require(isinstance(receipt,dict),'same-process source receipt absent')
    spec=audit.campaign.source_bundle
    H.compare_fields(audit,receipt,dict(verifiedBeforeFactoryExecution=True,nativeArithmetic=True,
        bufferCompatibility='local Uint8Array allocation; zero/one fill; LE float64 and uint64 DataView methods; no global Buffer or native prototype changes',factoryExecutionIds=FACTORY_IDS),name)
    audit.exact(receipt.get('bundle'),{k:spec[k] for k in ('path','bytes','sha256')},name+'.bundle')
    audit.exact(receipt.get('sources'),spec['sources'],name+'.complete-source-slices')
    ctl=receipt.get('adapterControls');require(isinstance(ctl,dict),'fixed adapter control receipt absent')
    H.compare_fields(audit,ctl,dict(schema='m31-browser-buffer-controls-v1',expectedGroups=9,expectedChecks=56,executedGroups=9,executedChecks=56,beforeScientificFactories=True,groupIds=[x[0] for x in ADAPTER_GROUPS],**{'pass':True}),name+'.adapter')
    groups=ctl.get('groups');require(isinstance(groups,list) and len(groups)==9,'nine adapter groups')
    for group,(ident,checks) in zip(groups,ADAPTER_GROUPS):
        H.compare_fields(audit,group,dict(id=ident,expectedChecks=len(checks),errorClass=None,**{'pass':True}),name+'.adapter.'+ident)
        audit.exact(group.get('checks'),[dict(id=check,**{'pass':True}) for check in checks],name+'.adapter.'+ident+'.every-fixed-check')


def page_environment(audit,env,closure,name):
    require(isinstance(env,dict),'page environment absent')
    page=closure['pageEnvironment']
    H.compare_fields(audit,env,dict(browserProcessId=audit.process_id,pageUserAgent=page['userAgent'],hardwareConcurrency=page['hardwareConcurrency'],visibility=page['visibilityState'],documentHidden=page['visibilityState']=='hidden',crossOriginIsolated=page['crossOriginIsolated'],isSecureContext=True,clock='native window.performance.now monotonic milliseconds',threads='one page main JavaScript thread; browser helper threads/processes externally observed',renderingDuringMatchedTimings=False,queryTimerScope='unchanged kernel.query totalMs/phasesMs',rssScope='no page RSS claim; owned Chrome-tree sampled RSS is the external supervisor responsibility'),name)
    audit.check(isinstance(env.get('platform'),str) and bool(env['platform']) and isinstance(env.get('language'),str) and bool(env['language']),name+'.navigator-metadata')
    audit.check(env.get('deviceMemoryGiB') is None or (finite(env['deviceMemoryGiB']) and env['deviceMemoryGiB']>0),name+'.optional-device-memory')
    audit.check(finite(env.get('performanceTimeOrigin')) and env['performanceTimeOrigin']>0,name+'.time-origin')
    clock=env.get('clockSample');require(isinstance(clock,dict),'fixed page clock metadata absent')
    H.compare_fields(audit,clock,dict(reads=128,method='fixed 128 metadata reads; no clock calibration loop'),name+'.clock-sample')
    audit.check(clock.get('minObservedPositiveDeltaMs') is None or (finite(clock['minObservedPositiveDeltaMs']) and clock['minObservedPositiveDeltaMs']>0),name+'.clock-positive-delta-or-unobserved')
    external=env.get('externalRuntimeEvidence');require(isinstance(external,dict),'host runtime evidence absent')
    for key in ('browserVersion','browserRuntime','launchArguments','profileIdentitySha256'):
        audit.exact(external.get(key),closure[key],name+'.host-'+key)
    browser_environment(audit.campaign,external.get('environment'),audit.process_id+'.'+name+'.host-environment')
    for key in ('cpuModel','architecture','platform','logicalCores','installedRAMBytes','headless','renderingDuringTiming','clock'):
        audit.exact(external['environment'].get(key),closure['environmentStart'][key],name+'.host-hardware-'+key)
    source_receipt(audit,env.get('sourceLoad'),name+'.source-load')


def stage_accounting(audit,value,name,files):
    require(isinstance(value,dict),'browser stage accounting absent')
    for key in ACCOUNTING_TIMES:audit.check(finite(value.get(key)) and value[key]>=0,name+'.'+key)
    for key in ACCOUNTING_COUNTS:audit.check(type(value.get(key)) is int and value[key]>=0,name+'.'+key)
    audit.check(value.get('notes')==ACCOUNTING_NOTES,name+'.explicit-query-exclusions-and-overlap')
    audit.check(value.get('eventLoopYields')==45,name+'.42-pretiming-plus3-postinput-turns')
    audit.check(value.get('gzipInputBytes')==2*sum(4*n*n for _,n,_ in CASES),name+'.all6-full-symbol-compression-inputs')
    audit.check(value.get('gzipOutputBytes')==sum(p.stat().st_size for p in files if p.name.endswith('-symbols.u8.gz')),name+'.all6-compressed-output-bytes')


def transport_accounting(audit,value,name,files):
    require(isinstance(value,dict),'browser transport accounting absent')
    H.compare_fields(audit,value,dict(chunkBytes=3145728,maxBase64Characters=4194304,maxInFlight=1,durableExclusiveAckRequired=True),name)
    expected=dict(acknowledgedBytes=sum(p.stat().st_size for p in files),acknowledgedChunks=sum(max(1,(p.stat().st_size+3145727)//3145728) for p in files),completedArtifacts=len(files))
    for key,wanted in expected.items():audit.check(type(value.get(key)) is int and value[key]==wanted,name+'.'+key)


def process_provenance(audit):
    evidence=audit.evidence;campaign=audit.campaign;closure=campaign.closures[audit.process_id]
    H.compare_fields(audit,evidence,dict(kind='fresh-boids-center-screen',runtimeKind='actual-chrome-javascript',browserProcessId=audit.process_id,complete=True),'evidence.actual-browser-identity')
    c=H.constants();nested={k:v for k,v in c.items() if k not in ('mg','arm','radius','rho','area')}
    H.compare_fields(audit,evidence.get('constants'),dict(mg=c['mg'],arm=c['arm'],radius=c['radius'],rho=c['rho'],A=c['area'],R=c['D']/2,c=nested),'evidence.independent-constants')
    audit.exact(evidence.get('memory'),dict(pageRSSMeasured=False,externalOwnedChromeRSSRequired=True),'evidence.no-page-RSS-substitution')
    listed=evidence.get('generation');require(isinstance(listed,list) and len(listed)==3,'three external-generation bindings')
    for rec,item in zip(listed,campaign.generation):
        entry=item['entry']
        audit.exact(rec,dict(id=item['id'],pin=entry['generationPin'],complete=True,generationMs=item['generationMs'],externalGeneration=True,finalPin={k:entry[k] for k in ('path','bytes','sha256')},generationEvidenceVerified=True),'evidence.shared-generation.'+item['id'])
    for stage in ('Start','End'):page_environment(audit,evidence.get('environment'+stage),closure,'page.environment'+stage)
    audit.exact(evidence['environmentStart'],evidence['environmentEnd'],'page.stable-complete-environment-and-source-receipt')
    execution=closure.get('executionConfigJSON');require(isinstance(execution,str) and 0<len(execution.encode('utf-8'))<=131072,'bounded host execution-config serialization')
    digest=hashlib.sha256(execution.encode('utf-8')).hexdigest()
    audit.check(digest==closure.get('executionConfigSha256')==evidence.get('executionConfigSha256'),'evidence.exact-host-page-execution-config-digest')
    expected={**campaign.config,'browserProcessId':audit.process_id,'runtimeEvidence':{key:closure[key] for key in ('browserVersion','browserRuntime','launchArguments','profileIdentitySha256')},'sourceBundle':campaign.source_bundle}
    expected['runtimeEvidence']['environment']=closure['environmentStart']
    audit.exact(json.loads(execution),expected,'evidence.every-frozen-execution-config-field')
    index=load_json(audit.path(campaign.top,'inputs/index.json'))
    # This index has only integer JSON numbers, strings, lists and objects.
    def integer_json(value):
        if isinstance(value,dict):return all(isinstance(k,str) and integer_json(v) for k,v in value.items())
        if isinstance(value,list):return all(integer_json(v) for v in value)
        return value is None or isinstance(value,(str,bool)) or type(value) is int
    require(integer_json(index),'input index must have integer-only JSON numeric fields')
    index_digest=hashlib.sha256(json.dumps(index,ensure_ascii=False,separators=(',',':'),allow_nan=False).encode('utf-8')).hexdigest()
    audit.check(evidence.get('inputIndexSha256')==index_digest,'evidence.exact-shared-index-serialization-digest')
    audit.check(evidence.get('manifestHashScope')=='SHA-256 UTF-8 JSON.stringify(encode(object)), no trailing newline; controller separately retains original index file pin.','evidence.explicit-serialization-scope')
    result=closure.get('pageResult');require(isinstance(result,dict),'host-retained page completion absent')
    H.compare_fields(audit,result,dict(complete=True,browserProcessId=audit.process_id,controls=48,generation=3,qualifications=6,timingCalls=42),'page.completion-fixed-counts')
    audit.pin(audit.package,result['evidencePin'],'page.completed-evidence-pin')
    audit.check(result['evidencePin'].get('path')=='results/evidence.json','page.completed-evidence-path')
    source_receipt(audit,result.get('sourceReceipt'),'page.completion-source-receipt')
    audit.exact(result['sourceReceipt'],evidence['environmentStart']['sourceLoad'],'page.same-completed-source-receipt')
    audit.check(finite(evidence.get('wallMsBeforeEvidence')) and finite(result.get('elapsedMs')) and 0<=evidence['wallMsBeforeEvidence']<=result['elapsedMs']<=895000 and result['elapsedMs']<=1000*closure['elapsedSeconds'],'page.cooperative-and-external-wall-accounting')
    entries=list((audit.package/'results').iterdir())
    audit.check(all(p.is_file() and not p.is_symlink() for p in entries),'page.results-directory-flat-regular-files-only')
    files=sorted(p for p in entries if p.is_file())
    expected_paths={'evidence.json','ownership.json'}
    expected_paths|={'control-'+x['id']+'.json' for x in H.expected_controls()}
    expected_paths|={f'call-{i:03d}{suffix}.json' for i in range(42) for suffix in ('','-raw')}
    for ident,_,_ in CASES:
        for method in 'LF':
            stem=ident+'-'+method
            expected_paths|={stem+'.json','qualification-'+stem+'.json',stem+'-symbols.u8.gz'}
            expected_paths|={stem+'-'+key+'.bin' for key in ('offsets','sources','K','a')}
    audit.check({p.name for p in files}==expected_paths and len(files)==176,'page.exact176-scientific-artifact-inventory')
    for p in files:audit.check(not p.is_symlink() and p.stat().st_size<=((16 if p.suffix=='.json' else 64 if p.name.endswith('.gz') else 128)<<20),'page.artifact-cap.'+p.name)
    before=[p for p in files if p.name!='evidence.json'];before_bytes=sum(p.stat().st_size for p in before);after_bytes=sum(p.stat().st_size for p in files)
    audit.check(evidence.get('newScientificBytesBeforeEvidence')==before_bytes and result.get('outputBytes')==after_bytes==closure['artifactBytes'],'page.complete-pre-post-evidence-byte-accounting')
    accounting=result.get('accountingAtCompletion');require(isinstance(accounting,dict),'completion accounting absent')
    transport_accounting(audit,evidence.get('transport'),'transport.before-evidence',before)
    transport_accounting(audit,accounting.get('transport'),'transport.completed',files)
    stage_accounting(audit,evidence.get('stageAccounting'),'accounting.before-evidence',files)
    stage_accounting(audit,accounting.get('stageAccounting'),'accounting.completed',files)
    start,end=evidence['stageAccounting'],accounting['stageAccounting']
    for key in ACCOUNTING_TIMES+ACCOUNTING_COUNTS:audit.check(end[key]>=start[key],'accounting.monotone.'+key)
    for key in ('sourceLoadMs','inputFetchDecodeMs','gzipMs','gzipInputBytes','gzipOutputBytes','eventLoopYieldMs','eventLoopYields'):
        audit.exact(start[key],end[key],'accounting.unchanged-final-save.'+key)
    audit.check(end['hashCalls']==start['hashCalls']+1 and end['hashBytes']==start['hashBytes']+result['evidencePin']['bytes'],'accounting.one-final-evidence-hash')


def output_bytes(audit,path,obj):
    payload=(json.dumps(H.safe_json(obj),allow_nan=False,indent=2)+'\n').encode('utf-8')
    require(len(payload)<=FIXED_LIMITS['reviewBytes'],'single review output cap')
    current=sum(p.stat().st_size for p in scientific_files(audit))
    initial=audit.resources.get('directoryBytesBeforeReview',current)
    require(current+len(payload)-initial<=FIXED_LIMITS['reviewBytes'],'combined review output cap')
    require(current+len(payload)<=FIXED_LIMITS['scientificDirectoryBytes']-FIXED_LIMITS['administrativeReserveBytes'],'review output preserves external closure reserve')
    with path.open('xb') as stream:stream.write(payload);stream.flush();os.fsync(stream.fileno())
    return dict(path=str(path.relative_to(audit.top)),bytes=len(payload),sha256=hashlib.sha256(payload).hexdigest())


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('package',type=Path);parser.add_argument('output',type=Path)
    args=parser.parse_args();package=args.package.resolve();out=args.output.resolve()
    require(package.is_dir() and out==package/'results/independent-review.json','fixed reviewer output required')
    require(not out.exists() and not (package/'results/analysis.json').exists(),'review outputs must be exclusive')
    audit=Audit(package);completed=False
    try:
        audit.resources['directoryBytesBeforeReview']=sum(p.stat().st_size for p in scientific_files(audit))
        provenance_resources(audit);source_bundle_review(audit)
        require(not audit.errors,'browser closure source provenance resource gate failed')
        shared_generation(audit)
        require(not audit.errors,'shared generation gate failed')
        for process_id in PROCESS_IDS:saved_process(audit,process_id)
        require(not audit.errors,'all three complete independent process gates required')
        cross_process_review(audit);audit.guard();completed=True
    except Exception as error:audit.error('review-error',error)
    result=campaign_analysis(audit,completed)
    if not result['independentAuditPass']:result['reason']='incomplete-or-failed-independent-browser-audit'
    analysis_pin=output_bytes(audit,package/'results/analysis.json',result)
    report=dict(schema='m31-browser-screen-independent-review-v1',kind='independent-fresh-browser-screen-review',complete=completed,**{'pass':completed and not audit.errors},
        independentAuditPass=result['independentAuditPass'],performanceRulePass=result['performanceRulePass'],practicalRulePass=None,requiresReviewSupervisorClosure=True,
        checkCount=len(audit.checks),errors=audit.errors,checks=audit.checks,
        generation=[dict(id=x['id'],n=x['n'],seed=x['seed']) for x in audit.generation],processes=audit.processes,crossProcess=audit.cross_process,
        coverage=dict(expectedProcesses=3,completedProcesses=sum(p['complete'] for p in audit.processes),expectedControlsPerProcess=48,expectedOwnershipBuildsPerProcess=6,expectedQualificationsPerProcess=6,expectedTimingsPerProcess=42,validatedTimingRecords=sum(p['validatedTimingRecords'] for p in audit.processes),expectedTotalTimingRecords=126,expectedPrimaryCells=6,expectedAdapterChecksPerProcess=56),
        analysis=analysis_pin,resources=audit.resources,reviewElapsedSeconds=time.monotonic()-audit.started,
        limitations=[
            'Finite evidence for three serial fresh processes of one pinned Chrome build, the fixed 48 controls and three shared newly generated saved states; no universal Math.hypot or unseen-state equivalence proof.',
            'Independent NumPy geometry and analytic roots retain inherited exact symbol requirements and numerical tolerances; no adaptive relaxation.',
            'Full saved control, ownership, qualification arrays and solutions are independently checked; all saved scientific values and gzip-decoded symbols are completely compared across p0/p1 and p0/p2. Clock readings, persistence durations and compressed gzip bytes are not equality targets.',
            'Every timed transient array is compared within its browser process to qualification arrays, but transient arrays are not all retained. The checker verifies all saved comparisons and nonclock values and cannot independently reconstruct unsaved timed arrays.',
            'Adapter checks cover 56 fixed assertions and their source-defined expectations, not all Node Buffer APIs or NaN payload bits. Their page results are receipts; the saved checker does not reexecute browser APIs.',
            'RSS measurements are sampled external owned-process sums, not a peak-memory guarantee. Browser helper threads and processes remain inside the declared sampled ownership scope.',
            'Three process median spreads are descriptive only. Each of six N5000 process-by-case cells must separately satisfy median F/L <=0.90 and at least five strict wins; no pooled rescue or process-population confidence claim.',
            'Short synthetic airflow-off Boids generation and frozen warmed queries do not establish aerodynamic validity, coupled flight, cold-start cost, rendering cost, cross-browser portability or novelty.',
            'The positive-term cap throw remains source-reviewed rather than exercised with a new giant fixture.',
            'The child cannot observe its own terminal supervisor closure. practicalRulePass remains null; an independent external seal must validate publication, all stage closures, post-review pins, combined elapsed <=4500s and final storage before any practical pass.',
            'The previously disclosed result-bearing arithmetic-file exposure remains; this is not an unexposed design process.'])
    audit.guard();output_bytes(audit,out,report)
    print(json.dumps(dict(**{'pass':report['pass']},complete=completed,checks=len(audit.checks),errors=len(audit.errors),performanceRulePass=result['performanceRulePass'],practicalRulePass=None,requiresReviewSupervisorClosure=True)))
    return 0 if report['pass'] else 1

if __name__=='__main__':raise SystemExit(main())
