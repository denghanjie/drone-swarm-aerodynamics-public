"""Saved JSON arithmetic and byte-integrity audit only; no scientific imports."""
import hashlib
import json
import math
import pathlib
import statistics
import sys

P = pathlib.Path(sys.argv[1])
OUT = pathlib.Path(sys.argv[2])
OUT.mkdir(parents=True, exist_ok=True)
checks = []
def check(name, passed):
    checks.append({'name': name, 'pass': bool(passed)})
def read(path):
    return json.loads((P / path).read_text())
def pin(path):
    b = (P / path).read_bytes()
    return {'path': path, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
def stats(values):
    return {'median': statistics.median(values), 'min': min(values), 'max': max(values)}

cfg = read('config.json')
e = read('results/evidence.json')
a = read('results/analysis.json')
review = read('results/independent-review.json')
runs = {kind: read('results/' + kind + '-run.json') for kind in ['candidate', 'review']}
ts = e['timings']
caseids = [c['id'] for c in cfg['cases']]
methods = cfg['methods']
phases = ['input', 'index', 'geometry', 'admission', 'setup', 'solve', 'residual', 'checksum', 'remainder']

check('candidate complete', e['complete'])
for key, count in [('controls',24),('generation',3),('qualification',9),('timings',63)]:
    check('count ' + key, len(e[key]) == count)
check('controls all pass', all(x['pass'] for x in e['controls']))
check('generations all complete', all(x['complete'] for x in e['generation']))
check('qualifications all pass and input unchanged', all(x['comparison']['pass'] and x['comparison']['inputUnchanged'] for x in e['qualification']))
check('independent reviewer complete/pass', review['complete'] and review['pass'])
check('independent checks exact count', review['checkCount'] == len(review['checks']) == 16239)
check('independent checks all pass and no errors', all(x['pass'] for x in review['checks']) and review['errors'] == [])
check('review covers all timings', review['coverage']['validatedTimingRecords'] == 63)

expected_schedule = [(cid,m,-1,True) for cid in caseids for m in methods]
for block in range(6):
    for j in range(3):
        c = (j + block) % 3
        expected_schedule.extend((caseids[c],m,block,False) for m in cfg['permutations'][(block+c)%6])
check('full frozen schedule exact', [(t['id'],t['method'],t['block'],t['warmup']) for t in ts] == expected_schedule)
check('sequence contiguous', [t['sequence'] for t in ts] == list(range(63)))
check('warmup and measured counts', sum(t['warmup'] for t in ts) == 9 and sum(not t['warmup'] for t in ts) == 54)
check('all durations finite positive', all(math.isfinite(t['totalMs']) and t['totalMs'] > 0 for t in ts))
check('all validations pass', all(t['validation']['pass'] and t['validation']['inputUnchanged'] and t['validation']['hashesMatch'] for t in ts))
phase_errors = []
for t in ts:
    name = f"call-{t['sequence']:03}"
    raw = read(t['raw']['path'])
    check(name + ' raw pin', pin(t['raw']['path']) == t['raw'])
    check(name + ' raw exact record retained', raw == {k:v for k,v in t.items() if k not in ['raw','validation']})
    check(name + ' validated file exact record retained', read('results/' + name + '.json') == t)
    check(name + ' phase schema and finite', list(t['phasesMs']) == phases and all(math.isfinite(x) and x >= 0 for x in t['phasesMs'].values()))
    phase_errors.append(abs(sum(t['phasesMs'].values()) - t['totalMs']))
check('phase sums exact', max(phase_errors) == 0)
check('all raw timing files exactly accounted', sorted(x.name for x in (P/'results').glob('call-*-raw.json')) == [f'call-{i:03}-raw.json' for i in range(63)])
check('no failure evidence file', not (P/'results/failure.json').exists() and not (P/'results/partial-evidence.json').exists())

recomputed = {'scope': a['scope'], 'cases': []}
extras = []
for cid in caseids:
    measured = [t for t in ts if t['id'] == cid and not t['warmup']]
    case = {'id': cid, 'methods': {}, 'pairs': {}}
    detail = {'id': cid, 'methods': {}, 'assembly': {}}
    for m in methods:
        records = [t for t in measured if t['method'] == m]
        check(cid + '/' + m + ' blocks', [t['block'] for t in records] == list(range(6)))
        case['methods'][m] = {'totalMs': stats([t['totalMs'] for t in records]), **{phase:stats([t['phasesMs'][phase] for t in records]) for phase in phases}}
        detail['methods'][m] = {'allMeasuredMs': [t['totalMs'] for t in records], 'allSequences': [t['sequence'] for t in records], 'geometrySharePerCall': stats([t['phasesMs']['geometry']/t['totalMs'] for t in records]), 'measuredSumMs':sum(t['totalMs'] for t in records)}
        if m != 'A':
            check(cid+'/'+m+' assembly invariant across warmup/measured', all(t['assemblyStats'] == records[0]['assemblyStats'] for t in ts if t['id']==cid and t['method']==m))
            detail['assembly'][m] = records[0]['assemblyStats']
    for ratio, numerator, denominator in [('T/L','T','L'),('L/A','L','A'),('T/A','T','A')]:
        left = [next(t for t in measured if t['block']==b and t['method']==numerator) for b in range(6)]
        right = [next(t for t in measured if t['block']==b and t['method']==denominator) for b in range(6)]
        ratios = [x['totalMs']/y['totalMs'] for x,y in zip(left,right)]
        diffs = [x['totalMs']-y['totalMs'] for x,y in zip(left,right)]
        case['pairs'][ratio] = {'ratios':ratios,'differencesMs':diffs,'medianPairedRatio':statistics.median(ratios),'strictWins':sum(x<1 for x in ratios),'matchedPhaseDifferenceSumsMs':{phase:sum(x['phasesMs'][phase]-y['phasesMs'][phase] for x,y in zip(left,right)) for phase in phases}}
    if cid in cfg['primary']['requiredCases']:
        tl,ta = case['pairs']['T/L'],case['pairs']['T/A']
        criteria = {'medianTOverLAtMostPoint9':tl['medianPairedRatio'] <= cfg['primary']['maximumMedianPairedRatio'], 'atLeastFiveStrictWins':tl['strictWins'] >= cfg['primary']['minimumStrictWins'], 'medianTOverAAtMostOne':ta['medianPairedRatio'] <= cfg['primary']['maximumAnchorMedianPairedRatio']}
        case['practicalRulePass'] = all(criteria.values())
        detail['decisionComponents'] = criteria
    recomputed['cases'].append(case)
    extras.append(detail)
recomputed['practicalRulePass'] = all(x['practicalRulePass'] for x in recomputed['cases'] if x['id'] in cfg['primary']['requiredCases'])
check('all saved analysis arithmetic exact match', recomputed == a)
check('independent reviewer timing arithmetic exact match', recomputed == review['timing'])

resources = {}
for kind, run in runs.items():
    check(kind+' supervisor success', run['supervisor_success'] and run['returncode']==0 and not run['monitorErrors'] and run['rssSampleErrors']==0 and not run.get('exception_class') and not run.get('terminated_for'))
    check(kind+' positive monitoring coverage', run['rssSamples']>0 and run['externalSampledPeakRSSKiB']>0)
    check(kind+' wall within cap', run['supervisor_elapsed_seconds']<=run['wall_cap_seconds'])
    check(kind+' external RSS within cap', run['externalSampledPeakRSSKiB']*1024<=run['rss_cap_bytes'])
    check(kind+' directory within cap', run['finalScientificDirectoryBytes'] + (P/('results/'+kind+'-run.json')).stat().st_size <= cfg['limits']['scientificDirectoryBytes'])
    check(kind+' logs within cap', run['finalSupervisorLogBytes']<=cfg['limits']['supervisorLogsBytes'])
    check(kind+' artifact paths unique', len({x['path'] for x in run['artifacts']})==len(run['artifacts']))
    check(kind+' artifact sizes account final directory', sum(x['bytes'] for x in run['artifacts'])==run['finalScientificDirectoryBytes'])
    check(kind+' all frozen artifact byte pins still match', all(pin(x['path'])==x for x in run['artifacts']))
    check(kind+' logs account final log bytes', sum(x['bytes'] for x in run['artifacts'] if x['path'].endswith(('-stdout.txt','-stderr.txt')))==run['finalSupervisorLogBytes'])
    resources[kind] = {k:v for k,v in run.items() if k!='artifacts'}
    resources[kind]['artifactCount'] = len(run['artifacts'])
    resources[kind]['aggregateIncludingOwnRecordBytes'] = run['finalScientificDirectoryBytes']+(P/('results/'+kind+'-run.json')).stat().st_size
check('candidate/reviewer same source identity', runs['candidate']['source_commit']==runs['review']['source_commit'] and runs['candidate']['source_manifest_sha256']==runs['review']['source_manifest_sha256'])
check('source manifest SHA agrees run records', pin('source-manifest.json')['sha256']==runs['candidate']['source_manifest_sha256'])
candidate_scientific_bytes = e['newScientificBytesBeforeEvidence'] + (P/'results/evidence.json').stat().st_size
check('candidate scientific writer count agrees reviewer', candidate_scientific_bytes==review['resources']['scientificBytes']==review['resources']['normalScientificBytes'])
check('candidate scientific writer within normal cap', candidate_scientific_bytes<=cfg['limits']['normalScientificBytes'])
check('candidate sampled RSS and Node maxRSS below cap', e['memory']['sampledPeakRSSBytes']<=cfg['limits']['rssBytes'] and e['memory']['processResourceUsage']['maxRSS']*1024<=cfg['limits']['rssBytes'])
allfiles = [x for folder in ['results','inputs','generation'] for x in (P/folder).rglob('*') if x.is_file()]
current_bytes = sum(x.stat().st_size for x in allfiles)
check('current aggregate exact review snapshot plus review record', current_bytes==resources['review']['aggregateIncludingOwnRecordBytes'])
check('current aggregate within cap', current_bytes<=cfg['limits']['scientificDirectoryBytes'])
resources['candidateScientificBytes'] = candidate_scientific_bytes
resources['currentAggregateBytes'] = current_bytes
resources['currentArtifactCount'] = len(allfiles)
resources['internalMemory'] = e['memory']
resources['reviewReportedResources'] = review['resources']
resources['generationTotalMs'] = sum(x['generationMs'] for x in e['generation'])
resources['qualificationComputeTotalMs'] = sum(x['qualificationComputeMs'] for x in e['qualification'])
resources['allQueryTotalMs'] = sum(x['totalMs'] for x in ts)
resources['measuredQueryTotalMs'] = sum(x['totalMs'] for x in ts if not x['warmup'])

largest = sorted((t for t in ts if not t['warmup']),key=lambda x:x['totalMs'],reverse=True)[:9]
result = {'kind':'independent-saved-record-arithmetic-interpretation-audit','scope':'stdlib JSON arithmetic, stored byte/hash consistency and interpretation; no simulator/geometry/solver/query imports or reruns','complete':True,'pass':all(x['pass'] for x in checks),'checkCount':len(checks),'checks':checks,'sourceCommit':runs['candidate']['source_commit'],'sourceManifestSHA256':runs['candidate']['source_manifest_sha256'],'inputPins':[pin(path) for path in ['config.json','PROTOCOL.md','SCHEMA.md','source-manifest.json','results/evidence.json','results/analysis.json','results/independent-review.json','results/candidate-run.json','results/review-run.json']], 'recomputedAnalysis':recomputed,'details':extras,'largestMeasuredCalls':[{'id':t['id'],'method':t['method'],'block':t['block'],'sequence':t['sequence'],'totalMs':t['totalMs'],'phasesMs':t['phasesMs'],'raw':t['raw']} for t in largest], 'maxPhaseSumErrorMs':max(phase_errors),'resources':resources,'environment':{'start':e['environmentStart'],'end':e['environmentEnd']},'independentNumericalReviewSummary':{'complete':review['complete'],'pass':review['pass'],'checkCount':review['checkCount'],'errors':review['errors'],'qualification':review['qualification']}}
(OUT/'ARITHMETIC.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'pass':result['pass'],'checks':len(checks),'failed':[x for x in checks if not x['pass']],'cases':[{'id':c['id'],'mediansMs':{m:c['methods'][m]['totalMs']['median'] for m in methods},'pairs':{k:{'median':v['medianPairedRatio'],'wins':v['strictWins']} for k,v in c['pairs'].items()},'rulePass':c.get('practicalRulePass')} for c in recomputed['cases']],'resources':{k:resources[k] for k in ['candidateScientificBytes','currentAggregateBytes','currentArtifactCount','generationTotalMs','qualificationComputeTotalMs','allQueryTotalMs','measuredQueryTotalMs']},'topMeasured':[{'id':t['id'],'method':t['method'],'block':t['block'],'sequence':t['sequence'],'ms':t['totalMs']} for t in largest]},indent=2))
