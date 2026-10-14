#!/usr/bin/env python3
"""Independent AUDIT-C1 benchmark receipt verifier. Never imports audit/model code.
Prepared for frozen execution; it must not be invoked before execution release.
"""
from __future__ import annotations
import hashlib
import json
import math
from pathlib import Path
import statistics

ORDERS={840131:['BC','CB','CB','BC','BC','CB','CB','BC'],840137:['CB','BC','BC','CB','CB','BC','BC','CB']}
OBS={'W-ENDPOINT':257,'W-STAGE-FIXTURE':161}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def finite_nonnegative(value):
    return isinstance(value,(int,float)) and not isinstance(value,bool) and math.isfinite(value) and value>=0


def expected_slots():
    return [(w,s,b,'B' if v=='B' else 'C1') for w in OBS for s in ORDERS for b,order in enumerate(ORDERS[s]) for v in order]


def median_range(values):
    return {'median':statistics.median(values),'minimum':min(values),'maximum':max(values),'all':values}


def validate_receipt(receipt, job, freeze_sha):
    require(receipt.get('schema')=='audit-c1-job/v1','Incorrect child receipt schema')
    require(receipt.get('status')=='passed','Incomplete child cannot enter ratios')
    require(receipt.get('jobId')==job['id'],'Job identity mismatch')
    require(receipt.get('freezeSha256')==freeze_sha,'Freeze identity mismatch')
    b=receipt.get('benchmark',{})
    for field in ('workload','seed','block','variant'):
        require(b.get(field)==job[field],'Benchmark '+field+' mismatch')
    require(b.get('consumedOutsideTimedRegion') is True,'Semantic results not consumed outside timed region')
    require(b.get('finishInsideTimedRegion') is True,'Finish/output materialization excluded from audit time')
    require(b.get('warmupIsolated') is True,'Warmup must use independent audit instance/ID')
    require(b.get('extraInstrumentedPasses')==0,'Unfrozen instrumented passes')
    warm=b.get('warmup',[])
    timed=b.get('timedPasses',[])
    require(isinstance(warm,list) and len(warm)==1,'Exactly one actual warmup required')
    require(isinstance(timed,list) and len(timed)==2,'Exactly two actual measured passes required')
    dig=b.get('expectedSemanticDigest')
    require(isinstance(dig,str) and len(dig)==64,'Missing correctness-derived semantic digest')
    identities=[]
    for index,p in enumerate(warm+timed):
        require(p.get('complete') is True,'Partial pass excluded')
        require(p.get('observations')==OBS[job['workload']],'Actual observation count mismatch')
        require(p.get('pairSamples')==OBS[job['workload']]*960,'Actual pair count mismatch')
        require(p.get('pairMarginValues')==OBS[job['workload']]*960*8,'All pair margins must be consumed')
        require(p.get('semanticDigest')==dig,'Semantic output digest differs from correctness anchor')
        require(p.get('consumed') is True,'Pass output not consumed')
        require(finite_nonnegative(p.get('wallSeconds')) and finite_nonnegative(p.get('cpuSeconds')),'Invalid per-pass time')
        require(isinstance(p.get('logicalId'),str),'Pass logical ID missing')
        identities.append(p['logicalId'])
    require(len(set(identities))==3,'Warmup/timed passes share logical audit IDs')
    aggregate=b.get('aggregate',{})
    # Integers in receipt are authoritative so harmless conversion summation does
    # not create a tolerance in the exact-output scientific contract.
    for key in ('wallSeconds','cpuSeconds'):
        require(finite_nonnegative(aggregate.get(key)) and aggregate[key]>0,'Nonpositive aggregate time')
        require(aggregate[key]==sum(p[key] for p in timed),'Aggregate '+key+' must sum exactly two measured passes')
    counts=receipt.get('counts',{})
    require(counts.get('warmupPasses')==1 and counts.get('measuredPasses')==2,'Configured counts cannot substitute for actual completed counts')
    require(counts.get('warmupObservations')==OBS[job['workload']],'Warmup observation ledger mismatch')
    require(counts.get('measuredObservations')==2*OBS[job['workload']],'Measured observation ledger mismatch')
    require(counts.get('totalObservations')==3*OBS[job['workload']],'Total observation ledger mismatch')
    rss=receipt.get('resourceUsage',{}).get('maxRssBytes')
    require(finite_nonnegative(rss) and rss>0 and rss<=512*1024*1024,'Missing/excessive max RSS')
    return b


def validate_all(root, jobs, supervised, freeze_sha):
    root=Path(root).resolve()
    rows=[r for r in jobs if r['phase']=='performance']
    slots=[(r.get('workload'),r.get('seed'),r.get('block'),r.get('variant')) for r in rows]
    require(slots==expected_slots(),'Incomplete/misordered 64 serial benchmark children')
    parents={r['jobId']:r for r in supervised}
    configured=json.loads((root/'implementation/config/jobs.json').read_text())
    gate_relative=configured.get('correctnessGate',{}).get('receipt')
    require(isinstance(gate_relative,str) and bool(gate_relative) and not Path(gate_relative).is_absolute(),
            'Missing/nonrelative configured correctness-gate receipt')
    require('..' not in Path(gate_relative).parts,'Parent traversal in correctness-gate receipt')
    gate_path=root/gate_relative
    require(gate_path.resolve().is_relative_to(root) and gate_path.resolve()==gate_path and
            not gate_path.is_symlink() and gate_path.is_file(),
            'Correctness-gate receipt escapes study, is missing, or uses a symlink')
    gate=json.loads(gate_path.read_text())
    require(gate.get('status')=='passed' and gate.get('freezeSha256')==freeze_sha,'Independent correctness gate did not pass for this freeze')
    anchors=gate.get('benchmarkSemanticDigests',{})
    records={}
    actual_observations=0
    actual_measured=0
    for job in rows:
        p=root/'implementation/results/receipts'/f"{job['id']}.json"
        receipt=json.loads(p.read_text())
        b=validate_receipt(receipt,job,freeze_sha)
        require(b['expectedSemanticDigest']==anchors.get(job['workload']+':'+str(job['seed'])),'Benchmark digest lacks independent correctness anchor')
        require(job['id'] in parents and parents[job['id']]['status']=='passed','Missing independent supervisor completion')
        pr=parents[job['id']]
        require(pr.get('receiptSha256')==hashlib.sha256(p.read_bytes()).hexdigest(),'Receipt changed after supervisor completion')
        require(pr['wait4']['exitCode']==0,'Nonzero exit benchmark excluded')
        require(pr['wait4']['maxRssBytes']<=512*1024*1024,'Independent exited-child maximum RSS fails cap')
        records[(job['workload'],job['seed'],job['block'],job['variant'])]=(receipt,pr)
        actual_observations+=receipt['counts']['totalObservations']
        actual_measured+=receipt['counts']['measuredObservations']
    require(actual_observations==40128 and actual_measured==26752,'Whole-window actual count mismatch')
    groups=[]
    too_short=False
    accept=True
    for workload in OBS:
        for seed in ORDERS:
            wall=[];cpu=[];pairs=[];rss_b=[];rss_c=[]
            for block in range(8):
                br,bp=records[(workload,seed,block,'B')]
                cr,cp=records[(workload,seed,block,'C1')]
                b=br['benchmark'];c=cr['benchmark']
                require(b['expectedSemanticDigest']==c['expectedSemanticDigest'],'Paired semantic digest mismatch')
                wb=b['aggregate']['wallSeconds'];wc=c['aggregate']['wallSeconds']
                cb=b['aggregate']['cpuSeconds'];cc=c['aggregate']['cpuSeconds']
                require(wb>0 and cb>0,'Zero baseline time invalidates cost ratio')
                wall.append(wc/wb);cpu.append(cc/cb)
                too_short |= wb<.100
                # Independently observed wait4 RSS, not self-reported data.
                rss_b.append(bp['wait4']['maxRssBytes']);rss_c.append(cp['wait4']['maxRssBytes'])
                pairs.append({'block':block,'order':ORDERS[seed][block],
                    'baselineJobId':br['jobId'],'candidateJobId':cr['jobId'],
                    'baselineTimedWallSeconds':wb,'candidateTimedWallSeconds':wc,
                    'baselineTimedCpuSeconds':cb,'candidateTimedCpuSeconds':cc,
                    'wallRatio':wall[-1],'cpuRatio':cpu[-1],
                    'baselineJobWallSeconds':bp['parentWallSeconds'],'candidateJobWallSeconds':cp['parentWallSeconds'],
                    'baselineJobCpuSeconds':bp['parentObservedCpuSeconds'],'candidateJobCpuSeconds':cp['parentObservedCpuSeconds'],
                    'baselineMaxRssBytes':rss_b[-1],'candidateMaxRssBytes':rss_c[-1],
                    'baselineReceipt':'implementation/results/receipts/'+br['jobId']+'.json',
                    'candidateReceipt':'implementation/results/receipts/'+cr['jobId']+'.json',
                    'baselineWarmup':{k:b['warmup'][0][k] for k in ('wallSeconds','cpuSeconds')},
                    'candidateWarmup':{k:c['warmup'][0][k] for k in ('wallSeconds','cpuSeconds')},
                    'baselineTimedPasses':[{k:p[k] for k in ('wallSeconds','cpuSeconds')} for p in b['timedPasses']],
                    'candidateTimedPasses':[{k:p[k] for k in ('wallSeconds','cpuSeconds')} for p in c['timedPasses']]})
            rb=statistics.median(rss_b);rc=statistics.median(rss_c)
            rss_ok=rc-rb<=max(.1*rb,16*1024*1024)
            primary=workload=='W-ENDPOINT'
            speed_ok=(statistics.median(wall)<=.80 and sum(x<1 for x in wall)>=7 and statistics.median(cpu)<=.85) if primary else (statistics.median(wall)<=1.05 and statistics.median(cpu)<=1.05)
            accept &= speed_ok and rss_ok
            groups.append({'workload':workload,'seed':seed,'wallRatios':median_range(wall),
                'cpuRatios':median_range(cpu),'blocksWithWallRatioBelowOne':sum(x<1 for x in wall),
                'baselineMedianMaxRssBytes':rb,'candidateMedianMaxRssBytes':rc,
                'rssAcceptancePassed':rss_ok,'speedAcceptancePassed':speed_ok,'pairs':pairs})
    status='correct_cost_inconclusive' if too_short else 'equivalent_faster_on_prescribed_replays' if accept else 'correct_but_no_useful_speedup'
    return {'schema':'audit-c1-independent-cost-validation/v1','status':status,
        'freezeSha256':freeze_sha,'freshChildren':64,'actualWarmupPasses':64,
        'actualMeasuredPasses':128,'actualObservationsIncludingWarmup':actual_observations,
        'actualMeasuredObservations':actual_measured,'baselineTooShort':too_short,
        'groups':groups,'outliersRemoved':0,'retries':0,'steadyStateEstablished':False,
        'measurementScope':'Fixed-one-warmup-conditioned serial audit replay; finish included; output consumption outside timed passes; all jobs fully charged.',
        'allocationOrGcShareMeasured':False,'safetyBucketAttribution':'The historical 35.093140530 s safety/diagnostics bucket includes other work. No audit-only fraction or end-to-end speedup is inferred.',
        'oldReferenceQualified':False,'realRkStagesReplayed':False,
        'interpretationLimit':'Exactness only on prescribed finite inputs and fixtures; single-host ratios are descriptive. No full-trajectory, physical-validation, browser, GPU, fleet-scale or universal-value claim.'}
