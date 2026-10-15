"""Read-only saved-record verifier. Usage: python3 m31-cadence-recompute.py REPO.
No fields, receiver-law calls, dynamics, trajectories, or experimental reruns.
Writes only /tmp/m31-cadence-review.json. All references in output are portable.
"""
import hashlib
import json
import math
from pathlib import Path
import statistics
import sys
import time

started=time.perf_counter()
if len(sys.argv)!=2:
    raise SystemExit('Usage: python3 m31-cadence-recompute.py REPOSITORY')
repo=Path(sys.argv[1]).resolve()
base=repo/'research/m31-airflow-cadence-2026-10-15'
read=lambda p:json.loads(p.read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
C=read(base/'config.json'); result=read(base/'results/result.json')
accuracy=read(base/'raw/accuracy.json'); freeze=read(base/'freeze.json')
budget=read(base/'results/budget.json'); raw_started=read(base/'raw/started.json')
checks=[]
def check(condition,name): checks.append({'check':name,'passed':bool(condition)})
def close(a,b): return math.isclose(a,b,rel_tol=2e-14,abs_tol=1e-28)
review={'scope':'Saved-record arithmetic and source-semantics audit only; no field/dynamics/experiment execution.',
 'method':{'script':'m31-cadence-recompute.py','scriptSha256':sha(Path(__file__)),
  'rms':'sqrt(math.fsum(error^2)/uniform sample count); equal weights; refresh-left records excluded.',
  'maximum':'Uniform samples plus every saved old-hold refresh-left record, including terminal events. Earliest saved candidate wins a tie.',
  'checksum':'Sequential binary64 accumulation of (thrust+roll)+pitch at even ticks, matching the stated checksum estimand.',
  'limits':'Production field values and oracle fixture outcomes are not regenerated. Timing records are arithmetic-checked, not rerun or independently benchmarked.'},
 'sourceCommit':result['sourceCommit'],'paths':[],'timing':[],'sourceHashChecks':[],
 'samplingFailures':[],'rawHashes':[]}
expected_commit='fd857ed1f5a4662ff98635e1998b53944b98738a'
check(result['sourceCommit']==raw_started['sourceCommit']==expected_commit,'saved source commit')
check(C==result['config']==raw_started['config'],'recorded configuration equality')
check(read(base/'raw/result.json')==result,'raw and published result equality')
for e in freeze['files']:
    p=repo/e['path']; actual=sha(p)
    ok=actual==e['sha256'] and p.stat().st_size==e['bytes']
    review['sourceHashChecks'].append({'path':e['path'],'sha256':actual,'matches':ok})
    check(ok,'frozen source '+e['path'])

timing=[]
for p in sorted((base/'raw').glob('timing-pass-*.json')):
    timing.extend(read(p))
check(len(timing)==48,'48 timing rows: warmup plus five passes, two paths, four variants')
for p in sorted((base/'raw').glob('*.json')):
    review['rawHashes'].append({'path':str(p.relative_to(repo)),'bytes':p.stat().st_size,'sha256':sha(p)})

largest_rms_delta=0.0; max_mismatch=0.0
weight=.027*9.81; motor_distance=2*math.sqrt(2)*.028
for path_index,path in enumerate(C['paths']):
    pid=path['id']; raw=read(base/'raw'/f'{pid}.json'); rows=raw['rows']
    saved=next(x for x in result['metrics'] if x['id']==pid)
    check(raw['path']==path and raw['tickSeconds']==C['tickSeconds'],'raw path/config '+pid)
    check([r['tick'] for r in rows]==list(range(C['finalTick']+1)),'complete ordered ticks '+pid)
    check(len(rows)==saved['rows']==2001,'row count '+pid)
    check(all([v['period'] for v in r['values']]==C['refreshTicks'] for r in rows),'variant order '+pid)
    row_values=[{v['period']:v for v in r['values']} for r in rows]
    for row,values in zip(rows,row_values):
        t=row['tick']; expected_position=[x+v*t*C['tickSeconds'] for x,v in zip(path['receiverInitial'],path['receiverVelocity'])]
        check(row['position']==expected_position,'prescribed position '+pid+' tick '+str(t))
        due=[p for p in C['refreshTicks'] if p and t>0 and t%p==0]
        check([x['period'] for x in row['left']]==due,'refresh-left accounting '+pid+' tick '+str(t))
        for p in C['refreshTicks']:
            ref=row_values[t//p*p][0] if p else values[0]
            check(values[p]['winds']==ref['winds'] and values[p]['wrench']==ref['wrench'],
                  'stored hold equals saved last-refresh reference '+pid+' tick '+str(t)+' period '+str(p))
        for left in row['left']:
            ref=row_values[t-left['period']][0]
            check(left['winds']==ref['winds'] and left['wrench']==ref['wrench'],
                  'left uses previous hold '+pid+' tick '+str(t)+' period '+str(left['period']))
    out={'id':pid,'metrics':[],'sampling':[]}
    summaries={}
    for name,stride in [('primary',C['primaryQueryTicks']),('refined',C['refinedQueryTicks'])]:
        summaries[name]={}
        for p in C['refreshTicks']:
            measurements=[]
            for k,observable in enumerate(['thrust','roll','pitch']):
                uniform=[]; candidates=[]; left_count=0
                for row,values in zip(rows,row_values):
                    reference=values[0]['wrench'][k]
                    if row['tick']%stride==0:
                        e=abs(values[p]['wrench'][k]-reference)
                        uniform.append(e);candidates.append((e,row['tick'],'sample'))
                    for left in row['left']:
                        if left['period']==p:
                            candidates.append((abs(left['wrench'][k]-reference),row['tick'],'refresh-left'));left_count+=1
                peak=max(candidates,key=lambda x:x[0]); rms=math.sqrt(math.fsum(e*e for e in uniform)/len(uniform))
                scale=weight*(motor_distance if k else 1)
                m={'name':observable,'periodTicks':p,'refreshMs':p*C['tickSeconds']*1000,'grid':name,
                   'max':peak[0],'rms':rms,'worstTick':peak[1],'worstSide':peak[2],
                   'uniformCount':len(uniform),'leftCount':left_count,
                   'maxNormalized':peak[0]/scale,'rmsNormalized':rms/scale}
                reported=next(x for x in saved[name] if x['period']==p)['observables'][k]
                largest_rms_delta=max(largest_rms_delta,abs(rms-reported['rms']))
                max_mismatch=max(max_mismatch,abs(peak[0]-reported['max']))
                check(close(rms,reported['rms']) and peak[0]==reported['max'],'max/RMS '+pid+' '+name+' '+str(p)+' '+observable)
                check((peak[1],peak[2],len(uniform),left_count)==(reported['worstTick'],reported['worstSide'],reported['rmsSamples'],reported['refreshLeftSamplesForMaximum']),
                      'peak identity/counts '+pid+' '+name+' '+str(p)+' '+observable)
                check(close(m['maxNormalized'],reported['maxNormalized']) and close(m['rmsNormalized'],reported['rmsNormalized']),
                      'normalized metrics '+pid+' '+name+' '+str(p)+' '+observable)
                measurements.append(m);out['metrics'].append(m)
            summaries[name][p]=measurements
    for p in C['refreshTicks']:
        for k,observable in enumerate(['thrust','roll','pitch']):
            a=summaries['primary'][p][k];b=summaries['refined'][p][k]
            floor=C['samplingAbsoluteFloorMomentNm'] if k else C['samplingAbsoluteFloorForceN']
            entry={'periodTicks':p,'refreshMs':p*C['tickSeconds']*1000,'observable':observable}
            for quantity in ['max','rms']:
                delta=abs(a[quantity]-b[quantity]); threshold=max(C['samplingRelativeTolerance']*b[quantity],floor)
                entry[quantity+'Difference']=delta;entry[quantity+'Threshold']=threshold;entry[quantity+'Stable']=delta<=threshold
                if not entry[quantity+'Stable']:review['samplingFailures'].append({'path':pid,'refreshMs':entry['refreshMs'],'observable':observable,'quantity':quantity,'difference':delta,'threshold':threshold,'relativeDifference':delta/b[quantity]})
            original=next(x for x in saved['sampling'] if x['period']==p)['checks'][k]
            check(entry['maxStable']==original['maxStable'] and entry['rmsStable']==original['rmsStable'],'sampling decision '+pid+' '+str(p)+' '+observable)
            out['sampling'].append(entry)
    review['paths'].append(out)
    for p in C['refreshTicks']:
        checksum=0.0
        for row,values in zip(rows,row_values):
            if row['tick']%C['primaryQueryTicks']==0:
                w=values[p]['wrench'];checksum+=(w[0]+w[1])+w[2]
        query_ticks=range(0,C['finalTick']+1,C['primaryQueryTicks'])
        expected_calls=len({t//p*p if p else t for t in query_ticks})
        selected=[r for r in timing if r['path']==pid and r['period']==p]
        check(len(selected)==6 and {r['pass'] for r in selected}==set(range(6)),'timing passes '+pid+' '+str(p))
        check(all(r['checksum']==checksum and r['fieldCalls']==expected_calls and r['warmup']==(r['pass']==0) for r in selected),'checksum/calls '+pid+' '+str(p))
        check(all(all(math.isfinite(r[k]) and r[k]>=0 for k in ['totalMs','fieldMs','receiverMs']) and r['totalMs']+1e-9>=r['fieldMs']+r['receiverMs'] for r in selected),'finite contained timings '+pid+' '+str(p))
        summary=next(x for x in result['timingSummary'] if x['path']==pid and x['period']==p)
        recalculated={'path':pid,'periodTicks':p,'fieldCalls':expected_calls,'checksum':checksum}
        for k in ['totalMs','fieldMs','receiverMs']:
            vals=[r[k] for r in selected if not r['warmup']]
            stats={'median':statistics.median(vals),'minimum':min(vals),'maximum':max(vals)}
            check(stats==summary[k],'timing summary '+pid+' '+str(p)+' '+k)
            recalculated[k]=stats
        review['timing'].append(recalculated)
    for pass_id in range(6):
        one=[r for r in timing if r['path']==pid and r['pass']==pass_id]
        expected=[C['refreshTicks'][(j+pass_id+path_index)%4] for j in range(4)]
        check([r['period'] for r in one]==expected,'rotating timing order '+pid+' '+str(pass_id))

timed_calls=sum(r['fieldCalls'] for r in timing)
# Source-inspected fixture accounting: 31 verify() calls (two evaluators each),
# plus 4 deliberate domain-error field calls = 33 production + 33 oracle.
fixture_each=33; refined_each=len(C['paths'])*(C['finalTick']+1)
held_calls=len(C['paths'])*sum(C['finalTick']//p+1 for p in C['refreshTicks'] if p)
expected_oracle=fixture_each+refined_each; expected_production=fixture_each+refined_each+held_calls+timed_calls
check(result['fieldCalls']==expected_oracle+expected_production==freeze['expectedFieldCalls'],'total field calls from saved timing plus static loop counts')
check(result['productionCalls']==expected_production and result['oracleCalls']==expected_oracle,'production/oracle counts')
check(accuracy['fieldCallsBeforeTimings']+timed_calls==result['fieldCalls'],'accuracy/timing total reconciliation')
check(accuracy['metrics']==result['metrics'],'accuracy/result metrics equality')
raw_bytes=sum(p.stat().st_size for p in (base/'raw').iterdir())
check(raw_bytes==budget['entries'][0]['rawBytesAfter']==3184006,'raw byte accounting')
check(result['physicalValidation'] is False and result['noveltyEstablished'] is False and result['operationalCadenceQualified'] is False,'no physical/novelty/cadence acceptance claims')
review['accounting']={'rawBytes':raw_bytes,'fieldCalls':result['fieldCalls'],'timingFieldCalls':timed_calls,
 'expectedProduction':expected_production,'expectedOracle':expected_oracle,
 'recordedPilotSupervisorWallSeconds':budget['entries'][0]['wallSeconds'],
 'recordedExperimentElapsedSeconds':result['elapsedSeconds']}
review['largestRMSAbsoluteDifferenceFromPublished']=largest_rms_delta
review['largestMaximumAbsoluteDifferenceFromPublished']=max_mismatch
review['semanticFindings']=[
 'All held fields correspond to the exact saved floor-refresh pose; 2.5 ms refresh events are not rounded to the 1 ms primary query grid.',
 'Maximum error includes old-hold refresh-left values at every event, including the terminal event; uniform RMS deliberately excludes event-only records.',
 'Timing uses one warmup plus five technical repeats with rotated variant order; field calls include time zero and terminal refresh. Checksum uses receiver thrust+roll+pitch only, not all state components.',
 'Timed totals exclude file persistence, independent oracle, controller, ODE integration, contact checks, rendering, and GPU operations. Saved wall measurements are not independently validated here.',
 'These are prescribed moving positions evaluated through a quasi-static field and receiver map. They are not physically actuated trajectories, physical unsteady-wake validation, or operational cadence acceptance.',
 'Five-millisecond RMS sampling screens fail thrust and pitch in both fixtures; maximum screens pass. The failure follows the stated criterion and must remain unresolved without another authorized protocol.',
 'The production/oracle tolerance result is only read as a saved outcome; this verifier does not reevaluate either field implementation.'
]
review['checkCount']=len(checks);review['failedChecks']=[x for x in checks if not x['passed']]
review['passed']=not review['failedChecks']
review['verifierWallSecondsBeforeOutput']=time.perf_counter()-started
destination=Path('/tmp/m31-cadence-review.json')
destination.write_text(json.dumps(review,indent=2,allow_nan=False)+'\n')
print(json.dumps({'passed':review['passed'],'checks':review['checkCount'],
 'failedChecks':review['failedChecks'],'samplingFailures':review['samplingFailures'],
 'rmsDelta':largest_rms_delta,'maxDelta':max_mismatch,
 'verifierWallSecondsIncludingOutput':time.perf_counter()-started},indent=2))
