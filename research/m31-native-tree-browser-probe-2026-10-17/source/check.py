"""Complete saved browser proof, stage binding and four64 exact-load audit.

No producer is imported. The frozen saved-word arithmetic/coverage checkers are
hash-verified helpers. All 44,256 primary drone-stage derivatives are checked.
"""
from pathlib import Path
from fractions import Fraction
import hashlib
import importlib.util
import json
import math
import struct
import sys

PACKAGE = 'research/m31-native-tree-browser-probe-2026-10-17'
ORDERS = (('F','H0','H'), ('H0','H','F'), ('H','F','H0'), ('H','H0','F'), ('H0','F','H'), ('F','H','H0'))
CASES = (('tree-t0-n64-a',64,26171731,(0,1,2,3)),
         ('tree-t0-n1000-a',1000,26171732,(4,5,0,1)),
         ('tree-t0-n5000-a',5000,26171733,(0,1,2,3)),
         ('tree-t0-n5000-b',5000,26171734,(4,5,0,1)))


def bootstrap(root, expected, commit):
    raw = (root / PACKAGE / 'source-manifest.json').read_bytes()
    if hashlib.sha256(raw).hexdigest() != expected:
        raise ValueError('bootstrap-manifest')
    manifest = json.loads(raw)
    path = PACKAGE + '/source/reference.py'
    pin = next(p for p in manifest['files'] if p['path'] == path)
    source = (root / path).read_bytes()
    if len(source) != pin['bytes'] or hashlib.sha256(source).hexdigest() != pin['sha256']:
        raise ValueError('bootstrap-support-pin')
    spec = importlib.util.spec_from_file_location('_probe_reference_support', root / path)
    support = importlib.util.module_from_spec(spec); spec.loader.exec_module(support)
    return support, support.preflight(root, expected, commit, 'check')


def exact_equal(a, b):
    if a is b:
        return True
    if type(a) is not type(b):
        return False
    if isinstance(a, dict):
        return a.keys() == b.keys() and all(exact_equal(a[k], b[k]) for k in a)
    if isinstance(a, list):
        return len(a) == len(b) and all(exact_equal(x,y) for x,y in zip(a,b))
    if isinstance(a, float):
        return struct.pack('>d',a) == struct.pack('>d',b)
    return a == b


def clean_native(value):
    return {k:v for k,v in value.items() if k not in ('recordMeta','auditTiming')}


def comparable(value):
    out = {k:v for k,v in value.items() if k not in ('recordMeta','auditTiming','method','tree','timing')}
    d = out.get('diagnostics')
    if d is not None:
        d = dict(d); d.pop('buildPhasesMs',None); out['diagnostics'] = d
        if d.get('geometryWork') is not None:
            d['geometryWork'] = {k:v for k,v in d['geometryWork'].items() if k != 'gatheredNonselfCandidates'}
        if d.get('screen') is not None:
            d['screen'] = {k:v for k,v in d['screen'].items() if k not in ('orderedPairVisits','componentTests')}
    return out


def elapsed(s, value):
    s.need(type(value) in (int,float) and math.isfinite(value) and value >= 0, 'finite-nonnegative-timing')
    return Fraction(value)


def timings(s, value, names):
    s.fields(value,names,'common-timing-fields')
    for name in names: elapsed(s,value[name])


def startup_source(s,ctx,body):
    bundle = s.decode(s.read_pin(ctx['root'],ctx['pins'][PACKAGE+'/source/source-bundle.json']))
    bundle_pin = {k:bundle[k] for k in ('path','bytes','sha256')}
    s.need(body['bundle'] == bundle_pin == ctx['pins'][PACKAGE+'/source/browser-bundle.js']
           and body['sources'] == bundle['sources'] and len(body['sources']) == 18
           and body['verifiedBeforeFactoryExecution'] is True and body['nativeArithmetic'] is True,
           'browser-executed-source-binding')
    raw = s.read_pin(ctx['root'],bundle_pin); previous = 0
    for source in body['sources']:
        pin = {k:source[k] for k in ('path','bytes','sha256')}
        s.need(pin == ctx['pins'][source['path']] and source['id'] == './'+source['path'], 'browser-factory-source-pin')
        offset = s.integer(source['offset'],previous,len(raw),'browser-source-offset')
        original = s.read_pin(ctx['root'],pin)
        s.need(raw[offset:offset+source['bytes']] == original,'browser-bundle-exact-source-slice')
        previous = offset+source['bytes']
    fresh = 'research/m31-native-fresh-transfer-2026-10-17/source/'
    expected = [PACKAGE+'/source/transport.cjs',PACKAGE+'/source/browser-driver.cjs',PACKAGE+'/source/browser-adapter.cjs',
        fresh+'vendor/generation/step02c-source/physics.cjs']
    expected += [fresh+'vendor/generation/milestone-31-source/'+name+'.cjs'
                 for name in ('sim','grid','geometry','factory','factory-wide','wall-filter')]
    expected += [fresh+'native-load.cjs']+[fresh+'vendor/'+name+'.cjs'
                 for name in ('kernel','anchor-kernel','reference-excerpt','lean-anchor')]
    expected += [PACKAGE+'/source/'+name+'.cjs' for name in ('native-tree','tree','compact-codec')]
    s.need(set(expected) == {p['path'] for p in body['sources']},'complete-factory-allowlist')
    s.need(body['localFactoryProcessShim'] == {'module':'./'+fresh+'vendor/generation/milestone-31-source/factory.cjs',
                                             'env':{'FLOCK_FACTORY_VARIANT':'wide'}},'local-factory-shim')
    controls = body['adapterControls']
    groups = (('zero-allocation',4),('one-fill',2),('fresh-storage',4),('float64-le',6),('float64-special',6),
              ('uint64-le',9),('offset-rejection',14),('value-rejection',4),('allocation-rejection',7))
    s.need(controls['schema'] == 'm31-browser-buffer-controls-v1' and controls['pass'] is True
           and controls['beforeScientificFactories'] is True
           and controls['expectedGroups'] == controls['executedGroups'] == len(controls['groups']) == 9
           and controls['expectedChecks'] == controls['executedChecks'] == 56
           and controls['groupIds'] == [name for name,count in groups], 'fixed56-buffer-controls')
    for group,(name,count) in zip(controls['groups'],groups):
        s.need(group['id'] == name and group['expectedChecks'] == len(group['checks']) == count
               and group['errorClass'] is None and group['pass'] is True
               and len({c['id'] for c in group['checks']}) == count
               and all(type(c['id']) is str and c['id'] and c['pass'] is True for c in group['checks']),
               'fixed56-buffer-control-assertions')
    return ['./'+path for path in expected]


def controller(audit, record, initial):
    audit.need(record['schema'] == 'm31-coupled-controller-v1' and record['arm'] == 'coupled'
               and record['stepIndex'] == record['controlIndex'] == 0
               and audit.d(record['relativeTimeWord']) == audit.d(record['originalTimeWord']) == 0,
               'one-initial-controller')
    rows = record['records']; ids = [r['id'] for r in initial['drones']]
    audit.need([{'id':r['id'],'state':r['stateWords']} for r in rows] == initial['drones'], 'actual-controller-input')
    commands = []
    for row in rows:
        state = audit.vec(row['stateWords'],17,'controller-state')
        neighbors = row['neighborIds']
        audit.need(type(neighbors) is list and neighbors == sorted(set(neighbors))
                   and all(type(i) is int and 0 <= i < len(ids) and i != row['id'] for i in neighbors),
                   'saved-controller-neighbor-shape')
        velocity = audit.vec(row['desiredVelocityWords'],3,'desired-velocity')
        target = row['target']
        audit.need(audit.d(target['vxWord']) == velocity[0] and audit.d(target['vyWord']) == velocity[1], 'target-velocity-binding')
        want_z = audit.r(state[2]+audit.r(audit.r(audit.r(Fraction(5,2)*velocity[2])+audit.r(Fraction(3,2)*state[5]))/6))
        audit.need(audit.d(target['zWord']) == want_z, 'target-z-arithmetic')
        audit.d(target['yawWord']); audit.vec(row['desiredQuaternionWords'],4,'desired-quaternion')
        values = audit.vec(row['commandsWords'],4,'controller-command')
        maximum = audit.r(audit.r(audit.r(Fraction(9,4)*audit.m)*audit.g)/4)
        audit.need(all(0 <= v <= maximum for v in values) and type(row['saturated']) is bool, 'controller-clamp-domain')
        commands.append(row['commandsWords'])
    return commands


def native_stage(s, ctx, a, compact, stage, natives, pins, n, order):
    s.need(stage['methodOrder'] == list(order) and list(natives) == list(order) and stage['nativeCalls'] == 3
           and stage['semanticAgreement'] is True and stage['status'] == 'completed' and stage['reason'] is None,
           'complete-three-arm-stage')
    s.need([r['method'] for r in stage['nativeRefs']] == list(order)
           and [r['recordPin'] for r in stage['nativeRefs']] == [pins[m] for m in order], 'actual-native-reference-binding')
    s.need([t['method'] for t in stage['queryTimings']] == list(order), 'query-timing-order')
    digest = s.sha(s.canonical(stage['nativeInput']))
    for index, method in enumerate(order):
        body = natives[method]
        s.need(body['recordMeta'] == {'caseId':stage['caseId'],'stageId':stage['stageId'],
                                     'queryOrderIndex':index,'inputUnchanged':True}, 'native-query-identity-preservation')
        s.need(body['method'] == method and body['caseId'] == stage['stageId']
               and body['semanticInputSha256'] == body['inlineInputCanonicalSha256'] == digest
               and body['status'] == 'native-success' and body['reason'] is None, 'native-input-success-binding')
        timing = stage['queryTimings'][index]
        s.need(timing['queryOrderIndex'] == index and body['auditTiming'] == {
            k:timing[k] for k in ('queryWallMs','encodeWallMs','semanticCompareWallMs')}, 'native-audit-timing-binding')
        for key in ('queryWallMs','encodeWallMs','semanticCompareWallMs','appendWallMs','serializationMilliseconds','transferMilliseconds','persistMilliseconds'):
            elapsed(s,timing[key])
    s.need(exact_equal(comparable(natives['F']),comparable(natives['H0']))
           and exact_equal(comparable(natives['F']),comparable(natives['H'])), 'complete-native-word-equality')
    f = natives['F']; raw = a.raw_binding(f,stage['nativeInput'])
    s.need(raw is not None and len(raw) == n and f['ids'] == list(range(n)), 'fixed-canonical-native-count')
    a.csr(f,n); a.consumption(f)
    s.need(f['diagnostics']['admission']['admitted'] is True
           and f['diagnostics']['admission']['reasons'] == []
           and f['diagnostics']['graph']['descendingEligible'] is True, 'native-success-admission')
    for field,limit in (('residualLog',1e-9),('sourceReceiverMismatch',2e-9)):
        s.need(elapsed(s,f['diagnostics'][field]) <= Fraction(limit), 'unchanged-residual-gate')
    p = compact.prepare(a,raw)
    stats = {'F': {'pairs':n*(n-1),'omitted':0,'culls':0}}
    s.need(f.get('tree') is None, 'unchanged-F-no-tree')
    for method in ('H0','H'):
        stats[method] = compact.certificate(a,natives[method].get('tree'),raw,method,p,poll=lambda:s.guard(ctx))
    for method in ('F','H0','H'):
        d = natives[method]['diagnostics']; work,screen = d['geometryWork'],d['screen']
        s.need(screen['eligible'] is p['eligible'] and screen['fallback'] is (not p['eligible']), 'independent-screen-eligibility')
        s.need(work['logicalDirectedPairs'] == n*(n-1)
               and work['gatheredNonselfCandidates'] == stats[method]['pairs']
               and work['certifiedSkippedPairs'] == n*(n-1)-work['directedCenterTests']
               and screen['orderedPairVisits'] == stats[method]['pairs']
               and screen['componentTests'] == (stats[method]['pairs'] if p['eligible'] else 0), 'exact-work-diagnostic-binding')
    return stats


def stage_arithmetic(s,ctx,audit,stage,loaded_h,target=None):
    rows = stage['records']; n = len(stage['nativeInput']['drones'])
    audit.need(stage['schema'] == 'm31-tree-browser-stage-v1' and [r['id'] for r in rows] == list(range(n)), 'stage-stable-ids')
    audit.need(stage['nativeInput'] == {'drones':[{'id':r['id'],'state':r['stateWords']} for r in rows]}, 'stage-native-input-consumption')
    audit.need(stage['rawBeforeProjection'] == {'drones':[{'id':r['id'],'state':r['rawStateWords']} for r in rows]}
               and stage['commandsBeforeEvaluation'] == [r['commandsWords'] for r in rows], 'stage-before-after-binding')
    native_report = None
    if target is not None:
        derived = dict(stage['native'],inputFileSha256=target['inputFileSha256'])
        native_report = audit.a.audit_evidence(derived,target,'F')
        audit.need(native_report['qualified'], 'four-exact-load-category-gates')
        audit.counts['nativeReferences'] += 1
    frame_max = Fraction(0)
    for row,load in zip(rows,loaded_h['loads']):
        s.guard(ctx)
        audit.need(row['id'] == load['id'] and row['consumed'] == {
            'rotorWords':load['rotor'],'collectiveWord':load['collective'],
            'worldForceWords':load['worldForce'],'worldMomentWords':load['worldMoment']}, 'actual-H-delivered-word-consumption')
        audit.derivative(row)
        if target is not None:
            bound = audit.frame_bound(row,target['loads'][row['id']],audit.d(target['constants']['R']))
            frame_max = max(frame_max,audit.a.rat(bound['bodyReference']['u']))
    audit.counts['stages'] += 1
    return {'nativeReference':native_report,'bodyMomentMaxSquaredNormalizedUpper':audit.a.encoded(frame_max)}


def main(root,expected,commit):
    s,ctx = bootstrap(root,expected,commit)
    result = {'schema':'m31-tree-browser-check-v1','sourceCommit':commit,'sourceManifestSha256':expected,
              'complete':False,'passed':False,'engineeringPassed':False,'stages':[],'cases':[],'controls':[],'errors':[]}
    try:
        saved = s.completed_output(ctx,'saved-validation')
        s.need(saved['complete'] is True and saved['passed'] is True and saved['sourceCommit'] == commit
               and saved['sourceManifestSha256'] == expected, 'pre-exposure-saved-qualification')
        a = s.module(ctx,'tree_check'); old = s.module(ctx,'stage_check'); compact = s.local_module(ctx,'compact-check.py')
        audit = old.StageAudit(s,ctx); resolver = compact.Resolver(s,ctx)
        browser,journal = s.closed_browser(ctx); audit.browser = browser
        references = s.completed_output(ctx,'reference')
        s.need(references['schema'] == 'm31-tree-browser-reference-v1'
               and references['complete'] is True and references['qualified'] is True and references['passed'] is True
               and references['sourceCommit'] == commit and references['sourceManifestSha256'] == expected
               and references['attempted'] == references['completed'] == len(references['records']) == 4
               and references['logicalPairs'] == 64512 and references['suffixCalls'] <= 64512, 'four64-reference-index')
        refmap = {r['stageId']:r for r in references['records']}
        s.need(list(refmap) == ['tree-t0-n64-a-step0-k%d'%k for k in range(1,5)], 'exact-reference-stage-ids')
        expected_kinds = ['source','factories']+['wiring-control']*12
        for _ in CASES:
            expected_kinds += ['initial','controller'] + (['native']*3+['stage'])*4 + ['step','safety','case-summary']
        expected_kinds += ['driver-summary']
        s.need([r['kind'] for r in journal] == expected_kinds, 'complete-ordered-record-coverage')
        wiring, current, pending, pending_pins, stage_records = [], None, {}, {}, []
        case_index, stage_index, total_native, suffix_calls = -1,0,0,0
        observed_pins, timing_rows, driver_events, case_summaries, pending_events = [], [], [], [], {}
        expected_factories = None
        for event in journal:
            s.guard(ctx)
            kind,pin = event['kind'],event['recordPin']; body = resolver.record(pin)
            observed_pins.append(pin)
            for field in ('serializationMilliseconds','transferMilliseconds','persistMilliseconds'):
                elapsed(s,event[field])
            if kind == 'source':
                expected_factories = startup_source(s,ctx,body); continue
            if kind == 'factories':
                s.need(body == {'ids':expected_factories,'globalProcessModified':False,'globalBufferModified':False},
                       'actual-factory-execution-order')
                continue
            if kind != 'driver-summary': driver_events.append((event,body.get('caseId'),body.get('stageId') or body.get('recordMeta',{}).get('stageId')))
            if kind == 'wiring-control':
                wiring.append({'kind':kind,'body':body}); continue
            if kind == 'initial':
                case_index += 1; identifier,n,seed,order_indices = CASES[case_index]
                s.need(body['schema'] == 'm31-tree-browser-initial-v1' and body['caseId'] == identifier
                       and body['n'] == n and body['seed'] == seed
                       and body['originalTimeWord'] == body['relativeTimeWord'] == a.ZERO,
                       'fixed-fresh-t0-initial')
                s.need([r['id'] for r in body['input']['drones']] == list(range(n)), 'initial-id-count')
                for row in body['input']['drones']:
                    s.need(all(a.finite(w) for w in a.words(row['state'],17,'initial-state')), 'initial-finite')
                current = {'id':identifier,'n':n,'initial':body['input'],'commands':None,'step':None,
                           'initializationWallMs':body['initializationWallMs'],
                           'querySums':{m:Fraction(0) for m in ('F','H0','H')},'pairs':{m:0 for m in ('F','H0','H')}}
                elapsed(s,body['initializationWallMs']); elapsed(s,body['inputEvidenceWallMs'])
                stage_records = []; stage_index = 0; resolver.clear()
            elif kind == 'controller':
                s.need(body['caseId'] == current['id'], 'controller-case-binding')
                current['commands'] = controller(audit,body,current['initial'])
                elapsed(s,body['controllerWallMs']); current['controllerWallMs'] = body['controllerWallMs']
            elif kind == 'native':
                method = body['method']
                s.need(method not in pending, 'duplicate-native-arm')
                pending[method] = body; pending_pins[method] = pin; total_native += 1
                pending_events[method] = event
            elif kind == 'stage':
                stage_index += 1
                identifier,n,seed,order_indices = CASES[case_index]
                s.need(body['caseId'] == identifier and body['stageId'] == identifier+'-step0-k'+str(stage_index)
                       and body['stepIndex'] == 0 and body['stageIndex'] == stage_index
                       and body['arm'] == 'coupled' and body['dtWord'] == a.rounded_word(Fraction('0.0025'))
                       and body['originalTimeWord'] == body['relativeTimeWord'], 'fixed-stage-grid')
                stats = native_stage(s,ctx,a,compact,body,pending,pending_pins,n,ORDERS[order_indices[stage_index-1]])
                timings(s,body['commonTiming'],('projectionWallMs','inputEvidenceWallMs','bindingAndDerivativeWallMs'))
                for item in body['queryTimings']:
                    prior = pending_events[item['method']]
                    s.need(item['serializationMilliseconds'] == prior['serializationMilliseconds']
                           and item['transferMilliseconds'] >= prior['transferMilliseconds']
                           and item['persistMilliseconds'] >= prior['persistMilliseconds'], 'query-journal-timing-binding')
                body['_recordPin'] = pin; body['native'] = clean_native(pending['F'])
                target = None
                if n == 64:
                    ref = refmap[body['stageId']]
                    s.need(ref['inputBinding'] == pin, 'reference-actual-stage-shards')
                    record = s.decode(s.read_pin(root,ref['reference']))
                    ctx['protectedPins'].append(ref['reference'])
                    s.need(record['inputSha256'] == ref['inputSha256'], 'reference-input-digest')
                    target,coverage = audit.target(body,record,references['constants'])
                    suffix_calls += coverage['scalarPairs']
                arithmetic = stage_arithmetic(s,ctx,audit,body,pending['H'],target)
                for t in body['queryTimings']:
                    current['querySums'][t['method']] += elapsed(s,t['queryWallMs'])
                for method in current['pairs']:
                    current['pairs'][method] += stats[method]['pairs']
                report = {'stageId':body['stageId'],'caseId':identifier,'work':stats,
                          'methodOrder':body['methodOrder'],'queryTimings':body['queryTimings'],
                          'commonTiming':body['commonTiming'],**arithmetic}
                result['stages'].append(report); timing_rows.append(report)
                body.pop('native'); body.pop('_recordPin')
                stage_records.append(body); pending = {}; pending_pins = {}; pending_events = {}; resolver.clear()
            elif kind == 'step':
                s.need(body['schema'] == 'm31-tree-browser-step-v1' and body['caseId'] == current['id']
                       and body['stepId'] == current['id']+'-step0'
                       and stage_index == 4 and body['originalTimeWord'] == body['relativeTimeWord'], 'complete-single-step')
                timings(s,body['commonTiming'],('rkCombinationWallMs','endpointProjectionWallMs','endpointEvidenceWallMs'))
                view = dict(body,schema='m31-coupled-step-v1')
                start = [{'id':r['id'],'stateWords':r['state']} for r in current['initial']['drones']]
                audit.step(view,stage_records,start,current['commands'])
                current['step'] = body
            elif kind == 'safety':
                s.need(body['schema'] == 'm31-coupled-safety-v1' and body['caseId'] == current['id']
                       and body['arm'] == 'coupled' and body['stepIndex'] == 0
                       and body['issues'] == [] and body['pass'] is True, 'saved-safety-status')
                elapsed(s,body['safetyWallMs']); current['safetyWallMs'] = body['safetyWallMs']
            elif kind == 'case-summary':
                s.need(body['schema'] == 'm31-tree-browser-case-summary-v1' and body['caseId'] == current['id']
                       and body['n'] == current['n'] and body['complete'] is True and body['completedSteps'] == 1
                       and body['final'] == {'drones':[{'id':r['id'],'state':r['stateWords']} for r in current['step']['final']]},
                       'case-final-actual-step-binding')
                for field in ('initializationWallMs','controllerWallMs','safetyWallMs'):
                    s.need(body[field] == current[field], 'case-common-timing-binding'); elapsed(s,body[field])
                elapsed(s,body['diagnosticCaseWallMs'])
                case_summaries.append({k:body[k] for k in ('caseId','n','complete','completedSteps',
                    'initializationWallMs','controllerWallMs','safetyWallMs','diagnosticCaseWallMs')})
                sums = current['querySums']; s.need(sums['F'] > 0, 'positive-F-query-duration')
                lower = current['pairs']['H'] < current['pairs']['F']; cost = sums['H'] <= Fraction(4,5)*sums['F']
                result['cases'].append({'caseId':current['id'],'n':current['n'],
                    'querySumsMs':{m:float(v) for m,v in sums.items()},'HtoFRatio':float(sums['H']/sums['F']),
                    'gatheredNonselfCandidates':current['pairs'],'fewerCandidates':lower,'costGate':cost,
                    'engineeringGate':lower and cost,'classification':'pass' if lower and cost else 'no-omissions' if not lower else 'overhead-dominated',
                    'initializationWallMs':body['initializationWallMs'],'controllerWallMs':body['controllerWallMs'],
                    'safetyWallMs':body['safetyWallMs'],'diagnosticCaseWallMs':body['diagnosticCaseWallMs'],
                    'stepCommonTiming':current['step']['commonTiming']})
                current = None; stage_records = []; resolver.clear()
            elif kind == 'driver-summary':
                s.need(body['schema'] == 'm31-tree-browser-driver-summary-v1' and body['complete'] is True and body['exactCounts'] is True
                       and body['counts'] == ctx['science']['expectedRuntimeCounts'], 'complete-driver-counts')
                s.need(len(body['stageTimings']) == 16 and len(body['cases']) == 4, 'driver-summary-size')
                s.need(body['cases'] == case_summaries and len(body['appendTimings']) == len(driver_events), 'driver-case-append-coverage')
                elapsed(s,body['wiringWallMs'])
                for item,(prior,case_id,stage_id) in zip(body['appendTimings'],driver_events):
                    s.need(item['recordPin'] == prior['recordPin'] and item['kind'] == prior['kind']
                           and item['caseId'] == case_id and item['stageId'] == stage_id
                           and item['serializationMilliseconds'] == prior['serializationMilliseconds']
                           and item['transferMilliseconds'] >= prior['transferMilliseconds']
                           and item['persistMilliseconds'] >= prior['persistMilliseconds'], 'driver-append-journal-binding')
                    for field in ('appendWallMs','serializationMilliseconds','transferMilliseconds','persistMilliseconds'):
                        elapsed(s,item[field])
                for recorded,checked in zip(body['stageTimings'],timing_rows):
                    s.need(recorded['caseId'] == checked['caseId'] and recorded['stageId'] == checked['stageId']
                           and recorded['status'] == 'completed' and recorded['methodOrder'] == checked['methodOrder']
                           and recorded['queryTimings'] == checked['queryTimings']
                           and recorded['commonTiming'] == checked['commonTiming'], 'driver-timing-bindings')
                result['diagnosticBrowserWallMs'] = body['diagnosticBrowserWallMs']
                elapsed(s,result['diagnosticBrowserWallMs'])
        s.need(case_index == 3 and total_native == 48 and len(result['stages']) == 16
               and suffix_calls == references['suffixCalls'], 'full-primary-reference-counts')
        result['controls'] = old.wiring_checks(audit,wiring)
        result['arithmeticFixtures'] = audit.a.arithmetic_fixtures()
        s.need(all(r['passed'] for r in result['controls']+result['arithmeticFixtures']), 'fixed-arithmetic-wiring-controls')
        s.need(audit.counts['stages'] == 16 and audit.counts['steps'] == 4
               and audit.counts['nativeReferences'] == 4 and audit.counts['droneStages'] == 44262
               and audit.counts['derivativeWords'] == 752454, 'full-derivative-audit-counts')
        result['counts'] = dict(audit.counts)
        result['controllerScope'] = 'Byte-pinned controller provenance, exact saved state/ID/command/elementary-target binding; no new independent neighbor membership or transcendental steering reconstruction.'
        result['zeroSignPolicy'] = 'Literal state/ID/load words remain exact; inherited rational derivative checks identify both zero signs numerically.'
        result['engineeringPassed'] = all(c['engineeringGate'] for c in result['cases'] if c['n'] == 5000)
        resolver.verify_preserved(); result['complete'] = result['passed'] = True
    except Exception as error:
        result['errors'].append(s.public_error(error))
    ctx['closing'] = True
    s.verify_sources(ctx); result['sourcesPreserved'] = True
    s.write(ctx,'check.json',result)
    return 0 if result['passed'] else 1


if __name__ == '__main__':
    if len(sys.argv) != 4:
        raise SystemExit('usage: check.py ROOT SHA COMMIT')
    raise SystemExit(main(Path(sys.argv[1]).resolve(),sys.argv[2],sys.argv[3]))
