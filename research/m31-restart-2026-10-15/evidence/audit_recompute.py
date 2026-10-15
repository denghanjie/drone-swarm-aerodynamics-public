"""Read-only M31 evidence audit. Usage: python3 audit_recompute.py PUBLIC_REPOSITORY.

Uses only the standard library; writes audit-data.json beside this script.
Does not import or run any simulation, report, or original audit script.
"""
import array
import bisect
import hashlib
import json
import math
from pathlib import Path
import statistics
import sys

if len(sys.argv) != 2:
    raise SystemExit('Usage: python3 audit_recompute.py PUBLIC_REPOSITORY')
repo = Path(sys.argv[1]).resolve()
if not (repo/'outputs/milestone-31-protocol.json').is_file():
    raise SystemExit('PUBLIC_REPOSITORY must contain outputs/milestone-31-protocol.json')
out = Path(__file__).resolve().parent
src = repo / 'outputs/milestone-31-source'
read = lambda p: json.loads(p.read_text())
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
protocol = read(repo / 'outputs/milestone-31-protocol.json')
data = {'auditSchema': 1, 'scope': 'Independent read-only first-checkpoint audit; no solver campaigns.',
        'method': {'script': 'audit_recompute.py', 'language': 'Python 3 standard library',
                   'reproduce': 'python3 audit_recompute.py PUBLIC_REPOSITORY',
                   'pythonVersion': sys.version.split()[0], 'scriptSha256': sha(Path(__file__)),
                   'positionMetric': 'Euclidean distance between equal-ID xyz at identical binary saved times; no interpolation.',
                   'replayLayout': 'Float64LE: time, then per drone [x,y,z,qx,qy,qz,qw]. Quaternion is xyzw.',
                   'replayLayoutSources': ['outputs/milestone-31-source/sim.cjs:41','outputs/step02c-source/physics.cjs:1','outputs/step02c-source/physics.cjs:17'],
                   'quantile': 'Nearest rank ceil(p*n), except median uses statistics.median.',
                   'postHoc': 'All new ensemble, finish-time, and normalized diagnostics are descriptive; they do not replace the frozen 1 cm test.'},
        'sourceHashChecks': [], 'rawFileHashes': [], 'trials': [], 'matchedInitialConditions': [],
        'trajectoryComparisons': [], 'checkpointChecks': [], 'figureDataChecks': []}

for rel, expected in protocol['sourceHashes'].items():
    p = src / rel
    actual = sha(p)
    data['sourceHashChecks'].append({'path': str(p.resolve().relative_to(repo)), 'expected': expected,
                                    'actual': actual, 'matches': expected == actual})
data['wallFilterMatchesM30Bytes'] = (src/'wall-filter.cjs').read_bytes() == (repo/'outputs/milestone-30-source/wall-filter.cjs').read_bytes()

runs, poses = {}, {}
def quantiles(xs):
    if not xs: return None
    x = sorted(xs)
    return {'minimum': x[0], 'p10': x[math.ceil(.1*len(x))-1], 'median': statistics.median(x),
            'p90': x[math.ceil(.9*len(x))-1], 'p95': x[math.ceil(.95*len(x))-1], 'maximum': x[-1]}

for job in protocol['jobs']:
    rid = job['id']; r = read(src / (rid+'.json')); runs[rid] = r; n = job['count']
    f = array.array('d'); f.frombytes((src / r['replay']['file']).read_bytes())
    if sys.byteorder != 'little': f.byteswap()
    width = 1 + 7*n; nf = len(f)//width
    frames = {f[k*width]: memoryview(f)[k*width+1:(k+1)*width] for k in range(nf)}
    poses[rid] = frames
    def endpoint_exact(t, states):
        return list(frames[t]) == [x for s in states for x in s[:3]+s[6:10]]
    crossings = [x for x in r['crossings'] if x is not None]
    minima = {key: min(s[col] for s in r['samples']) for key,col in [
        ('minimumConnectedFraction','largestFraction'), ('minimumSampledSeparation','minimumSeparationCappedAtRadius'),
        ('minimumSampledObstacleClearance','minimumObstacleClearance')]}
    row = {'id':rid, 'job':job, 'passedRecounted':len(crossings), 'end':r['metrics']['end'],
           'stop':r['metrics']['stopReason'], 'failure':r['metrics']['failure'], 'finishTimeQuantiles_s':quantiles(crossings),
           'allFinishTime_s':max(crossings) if len(crossings)==n else None,
           'stateAndFrameChecks': {'binarySizeMatches':len(f)==width*r['replay']['frames'],
             'frameCount':nf, 'firstFrame':min(frames), 'lastFrame':max(frames),
             'allPosesFinite':all(math.isfinite(x) for x in f),
             'allEndpointsFiniteAnd17D':all(len(s)==17 and all(math.isfinite(x) for x in s) for s in r['initial']+r['final']),
             'initialPoseExactlyMatches':endpoint_exact(min(frames),r['initial']),
             'finalPoseExactlyMatches':endpoint_exact(max(frames),r['final']),
             'passedMatches':len(crossings)==r['metrics']['passed'],
             'sampleMinimaMatch':all(minima[k]==r['metrics'][k] for k in minima),
             'controlUpdateCountMatches':r['diagnostics']['updates']==n*math.ceil(r['metrics']['end']/.01-1e-8)},
           'sampleMinimaRecomputed':minima,
           'sampledPairSurfaceGap_m':minima['minimumSampledSeparation']-.15,
           'sampledPairMarginShortfall_m':max(0,.38-minima['minimumSampledSeparation']),
           'initialExtents_m':[[min(s[k] for s in r['initial']),max(s[k] for s in r['initial'])] for k in range(3)],
           'initialMeanNeighborCount':r['samples'][0]['meanNeighborCount'],
           'initialCenter_m':r['samples'][0]['center'],
           'diagnostics':r['diagnostics'],
           'wallViolationUpdateFraction':r['diagnostics']['wallViolationsAfter']/r['diagnostics']['updates'],
           'pairViolationUpdateFraction':r['diagnostics']['pairViolationsAfter']/r['diagnostics']['updates'],
           'samplesBelowFullyConnected':[{'t':s['t'],'fraction':s['largestFraction']} for s in r['samples'] if s['largestFraction']<1]}
    data['trials'].append(row)
    for p in [src/(rid+'.json'),src/r['replay']['file']]:
        data['rawFileHashes'].append({'path':str(p.relative_to(repo)),'bytes':p.stat().st_size,'sha256':sha(p)})
    for t in [20,60,120,180]:
        p = src/f'checkpoint-{rid}-{t}.json'
        if p.exists():
            cp = read(p)
            data['checkpointChecks'].append({'trial':rid,'t':t,'poseExactlyMatchesBinary':endpoint_exact(t,cp['states']),
             'crossingCountMatches':cp['passed']==sum(x is not None and x<=t for x in r['crossings']),
             'fullFinalStateMatches':cp['states']==r['final'] if t==r['metrics']['end'] else None})

for seed,n,course in [(2001,1000,'wide'),(2002,1000,'narrow'),(2001,5000,'wide')]:
    ids = [f'heldout-{seed}-{n}-{course}-{fil}-0.0025' for fil in ['baseline','wall-priority']]
    data['matchedInitialConditions'].append({'trials':ids,'exactlyEqual':runs[ids[0]]['initial']==runs[ids[1]]['initial']})

reported_comparisons = read(repo/'outputs/milestone-31-comparisons.json')
for ref in reported_comparisons:
    a,b = ref['coarse'],ref['fine']; ra,rb=runs[a],runs[b]; n=ra['config']['count']
    common=sorted(set(poses[a])&set(poses[b])); profile=[]; maxima=[]
    for t in common:
        pa,pb = poses[a][t],poses[b][t]
        err=[math.dist(pa[7*i:7*i+3],pb[7*i:7*i+3]) for i in range(n)]
        maximum=max(err); who=err.index(maximum); es=sorted(err)
        center_dist=math.sqrt(sum((sum(pa[7*i+k]-pb[7*i+k] for i in range(n))/n)**2 for k in range(3)))
        profile.append({'t':t,'maximum':maximum,'maxDrone':who,'median':statistics.median(es),
                        'p95NearestRank':es[math.ceil(.95*n)-1],'rms':math.sqrt(sum(v*v for v in err)/n),
                        'centerDifference':center_dist,'fractionAbove1cm':sum(v>=.01 for v in err)/n})
    peak=max(profile,key=lambda row:row['maximum'])
    rrow={'coarse':a,'fine':b,'initialExactlyEqual':ra['initial']==rb['initial'],
          'commonSavedTimeCount':len(common),'commonTimeEnd':common[-1],
          'peak':peak,'firstSavedThresholdTimes_s':{str(th):next((p['t'] for p in profile if p['maximum']>=th),None) for th in [1e-6,1e-4,.01,.1,1,10]},
          'profile':profile,'maximumCenterDifference_m':max(p['centerDifference'] for p in profile),
          'reportedProfileMaxAbsoluteDiscrepancy':max(abs(p[key]-q[key]) for p,q in zip(profile,ref['positionDifferenceAtSavedTimes']) for key in ['maximum','median','p95NearestRank']),
          'reportedMaximumMatches':peak['maximum']==ref['maximumSynchronizedPositionDifference'],
          'frozen1cmCriterionPass':peak['maximum']<.01}
    sa={s['t']:s for s in ra['samples']};sb={s['t']:s for s in rb['samples']}; st=sorted(sa.keys()&sb.keys())
    rrow['sampledEnsembleMaxDifferences']={k:max(abs(sa[t][k]-sb[t][k]) for t in st) for k in ['passed','order','largestFraction','rmsRadius','minimumSeparationCappedAtRadius','minimumObstacleClearance']}
    ca,cb=ra['crossings'],rb['crossings']
    if all(t is not None for t in ca+cb):
        absd=[abs(x-y) for x,y in zip(ca,cb)]; xa,xb=sorted(ca),sorted(cb)
        times=sorted(set(ca+cb)); ecdf=max((abs(bisect.bisect_right(xa,t)-bisect.bisect_right(xb,t))/n,t) for t in times)
        rrow['finishTimeComparison']={'individualAbsoluteDifference_s':quantiles(absd),
          'allFinishTimes_s':[max(ca),max(cb)], 'allFinishDifference_s':max(cb)-max(ca),
          'medianFinishDifference_s':statistics.median(cb)-statistics.median(ca),
          'quantileDifferences_s':{str(p):xb[math.ceil(p*n)-1]-xa[math.ceil(p*n)-1] for p in [.1,.5,.9,.95,1]},
          'maxCumulativeFinishFractionDifference':ecdf[0], 'timeOfMaximum_s':ecdf[1],
          'wasserstein1OfFinishDistributions_s':sum(abs(x-y) for x,y in zip(xa,xb))/n,
          'fractionIndividualsMoreThan1sDifferent':sum(x>1 for x in absd)/n}
    else:rrow['finishTimeComparison']=None
    data['trajectoryComparisons'].append(rrow)

cp=read(src/'checkpoint-development-1501-5000-wide-wall-priority-0.0025-20.json')
old=read(src/protocol['developmentCheckpointReference'])
data['development20sFullStateExactlyMatchesM30']=cp['states']==old['final']

fig=read(repo/'outputs/milestone-31-figure-sources.json')
for f in fig['sources']:
    r=runs[f['file'][:-5]]
    plotted=dict(count=r['config']['count'],seed=r['config']['seed'],course=r['job']['course'],filter=r['config']['filter'],crossings=r['crossings'],end=r['metrics']['end'],stop=r['metrics']['stopReason'])
    h=hashlib.sha256(json.dumps(plotted,sort_keys=True,allow_nan=False).encode()).hexdigest()
    data['figureDataChecks'].append({'file':f['file'],'crossingsExactlyMatch':f['crossings']==r['crossings'],'plottedDataHashMatches':h==f['plottedDataSha256']})

export={r['path']:r for r in read(repo/'docs/public-export-changes.json')['changes']}
manifest=read(repo/'outputs/archive-before-full-priority-missions/research-manifest.json')
historical=[e for e in manifest['files'] if '-source/' in e['path']]
diffs=[]
# Bound this checkpoint to M31 and its dependencies. The 793-file archive is a
# historical record, not an assertion that every public byte must equal a private
# pre-export manifest. Check only declared historical sanitization mappings here.
for e in historical:
    rel='outputs/'+e['path']; mapped=export.get(rel)
    if mapped:
        actual=sha(repo/rel)
        diffs.append({'path':rel,'expectedHistoricalSha256':e['sha256'],'actual':actual,
                      'differsFromHistoricalBytes':actual!=e['sha256'],
                      'explainedBySanitizedExport':mapped['originalSha256']==e['sha256'] and mapped['publicSha256']==actual})
data['historicalSourcePreservationRecheck']={'historicalEntries':len(historical),
 'full793FileRehashPerformed':False, 'scope':'Checked declared sanitized historical source records only; prior 793-pass audit is preserved history, not a fresh public byte-equality result.',
 'filesChecked':len(diffs),'differences':diffs,'allCheckedDifferencesExplainedByPublicSanitization':all(d['explainedBySanitizedExport'] for d in diffs)}

current=read(repo/'outputs/research-manifest.json')
entries=[e for e in current['files'] if e['path'].startswith('milestone-31') or e['path']=='step02c-source/physics.cjs']
data['publicManifestCheck']={'selectedEntriesChecked':len(entries),'mismatches':[e['path'] for e in entries if not (repo/'outputs'/e['path']).exists() or sha(repo/'outputs'/e['path'])!=e['sha256']]}
if (out/'audit-controls.json').exists():
    controls=read(out/'audit-controls.json')
    data['localControllerCalculations']={'file':'audit-controls.json','sha256':sha(out/'audit-controls.json'),
     'script':'audit_controls.cjs','scriptSha256':sha(out/'audit_controls.cjs'),'method':controls['method'],
     'contactReplayChecks':[{k:v for k,v in row.items() if k in ['trial','controlExactlyReproduced','finalStateExactlyReproduced','contactIdentityAndClearanceExactlyReproduced','steps']} for row in controls['contacts']],
     'neighborOrderProbeSummaries':[{k:v for k,v in row.items() if k not in ['top5','allDrones']} for row in controls['neighborOrderProbes']]}
data['claimEvidence']=[
 {'id':'M31-C1','claim':'Candidate completes prescribed primary cases; fresh matched baselines stop at obstacles.',
  'classification':'direct raw-record accounting plus small contact-state replay','assessment':'supported in saved model',
  'evidence':['trials','matchedInitialConditions','localControllerCalculations.contactReplayChecks'],
  'limit':'Whole-run no-contact status was not independently recomputed at every physics substep.'},
 {'id':'M31-C2','claim':'ID-matched paths meet the frozen 1 cm refinement criterion.',
  'classification':'independent calculation from raw binary poses','assessment':'rejected in all three comparisons',
  'evidence':['trajectoryComparisons'],'limit':'Two step sizes and one-second poses give discrepancies, not convergence order or between-frame bounds.'},
 {'id':'M31-C3','claim':'Aggregate passage is less sensitive than ID histories for the two 1000-drone pairs.',
  'classification':'new post-hoc descriptive calculation','assessment':'observed in these pairs',
  'evidence':['trajectoryComparisons.finishTimeComparison'],'limit':'Not a preregistered alternative success criterion; does not erase M31-C2.'},
 {'id':'M31-C4','claim':'The implemented controller has same-state neighbor-order sensitivity.',
  'classification':'new exploratory controlled calculation','assessment':'observed',
  'evidence':['localControllerCalculations.neighborOrderProbeSummaries','audit-controls.json'],
  'limit':'Artificial reversal changes both floating-point social accumulation and pair projection order. It does not prove causation of timestep divergence or improved accuracy.'},
 {'id':'M31-C5','claim':'Boids alone causes factory passage.',
  'classification':'source inspection and design analysis','assessment':'not identified',
  'evidence':['outputs/milestone-31-source/sim.cjs:11','outputs/milestone-31-source/sim.cjs:13','outputs/milestone-31-source/factory-wide.cjs:9'],
  'limit':'Every M31 run includes shared route guidance, separation, alignment, cohesion, and the pair filter.'},
 {'id':'M31-C6','claim':'M31 validates aerodynamic interactions or physical flight safety.',
  'classification':'actual dependency inspection','assessment':'unsupported',
  'evidence':['outputs/step02c-source/physics.cjs:18','outputs/milestone-31-source/sim.cjs:44'],
  'limit':'External force defaults to zero; no measured interaction model or tracking/clearance error bounds.'},
 {'id':'M31-C7','claim':'Frozen M31 scientific dependency hashes match current public bytes.',
  'classification':'SHA-256 read-only checks','assessment':'supported',
  'evidence':['sourceHashChecks','publicManifestCheck','historicalSourcePreservationRecheck'],
  'limit':'Internal hash consistency is not external preregistration proof. Historical metadata sanitization is mapped; a full 793-file archival rehash was not completed.'}
]
(out/'audit-data.json').write_text(json.dumps(data,indent=2,allow_nan=False)+'\n')
print(json.dumps({'trials':len(data['trials']),'sourceHashesMatch':all(s['matches'] for s in data['sourceHashChecks']),
  'historicalSourceMismatches':len(diffs),'publicManifestMismatches':data['publicManifestCheck']['mismatches'],
  'comparisonPeaks':[{k:v for k,v in r.items() if k in ['fine','peak','finishTimeComparison','maximumCenterDifference_m','reportedMaximumMatches','reportedProfileMaxAbsoluteDiscrepancy']} for r in data['trajectoryComparisons']]},indent=2))
