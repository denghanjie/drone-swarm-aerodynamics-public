"""Single first projected N1000 state: conditional native equivalence and arithmetic.
No native producer, initializer, controller or reference routine is executed here.
"""
from pathlib import Path
from fractions import Fraction
import hashlib
import importlib.util
import json
import math
import struct
import sys

PACKAGE = 'research/m31-native-tree-state1000-2026-10-17'
CASE, N, SEED = 'tree-t0-n1000-a', 1000, 2026101741
ORDER = ('F','H0','H')


def bootstrap(root, expected, commit):
    raw = (root/PACKAGE/'source-manifest.json').read_bytes()
    if hashlib.sha256(raw).hexdigest() != expected: raise ValueError('bootstrap-manifest')
    manifest = json.loads(raw); path = PACKAGE+'/source/support.py'
    pins = [p for p in manifest['files'] if p['path'] == path]
    source = (root/path).read_bytes()
    if len(pins) != 1 or len(source) != pins[0]['bytes'] or hashlib.sha256(source).hexdigest() != pins[0]['sha256']:
        raise ValueError('bootstrap-support-pin')
    spec = importlib.util.spec_from_file_location('_state1000_support',root/path)
    support = importlib.util.module_from_spec(spec); spec.loader.exec_module(support)
    return support,support.preflight(root,expected,commit,'check')


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
           and body['sources'] == bundle['sources'] and len(body['sources']) == 19
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
        PACKAGE+'/source/layout.cjs',
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
            k:timing[k] for k in ('queryWallMs','encodeWallMs','semanticCompareWallMs','layoutEncodeWallMs','layoutRoundtripWallMs')}, 'native-audit-timing-binding')
        for key in ('queryWallMs','encodeWallMs','semanticCompareWallMs','layoutEncodeWallMs','layoutRoundtripWallMs','appendWallMs','serializationMilliseconds','transferMilliseconds','persistMilliseconds'):
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


def stage_arithmetic(s,ctx,audit,stage,loaded_h):
    rows = stage['records']; n = len(stage['nativeInput']['drones'])
    audit.need(stage['schema'] == 'm31-tree-browser-stage-v1' and [r['id'] for r in rows] == list(range(n)), 'stage-stable-ids')
    audit.need(stage['nativeInput'] == {'drones':[{'id':r['id'],'state':r['stateWords']} for r in rows]}, 'stage-native-input-consumption')
    audit.need(stage['rawBeforeProjection'] == {'drones':[{'id':r['id'],'state':r['rawStateWords']} for r in rows]}
               and stage['commandsBeforeEvaluation'] == [r['commandsWords'] for r in rows], 'stage-before-after-binding')
    for row,load in zip(rows,loaded_h['loads']):
        s.guard(ctx)
        audit.need(row['id'] == load['id'] and row['consumed'] == {
            'rotorWords':load['rotor'],'collectiveWord':load['collective'],
            'worldForceWords':load['worldForce'],'worldMomentWords':load['worldMoment']}, 'actual-H-delivered-word-consumption')
        audit.derivative(row)
    audit.counts['stages'] += 1
    return {'derivativeRows':n,'derivativeWords':17*n,'referenceCalls':0}


def reconstruct_layout(s,ctx,layout,value):
    """Decode columns independently; then run the frozen structural comparator.

    This validates representation only. The reconstructed object must separately
    pass the raw-state-derived full compact certificate before any qualification.
    """
    s.fields(value,('schema','base','receiverIds','cullOffsets','cullCodes','cullDifferences','leavesRefs','gathered'),
             'layout-fields')
    s.need(value['schema'] == 'm31-tree-witness-columns-v1' and type(value['base']) is dict
           and value['base'].get('n') == N and 'receivers' not in value['base'],'layout-fixed-base')
    for key in ('receiverIds','cullOffsets','cullCodes','cullDifferences','leavesRefs','gathered'):
        s.need(type(value[key]) is list,'layout-column-array')
    s.need(len(value['receiverIds']) == len(value['leavesRefs']) == len(value['gathered']) == N
           and len(value['cullOffsets']) == N+1,'layout-fixed-receivers')
    offsets,codes,differences = value['cullOffsets'],value['cullCodes'],value['cullDifferences']
    s.need(len(codes) == len(differences) and offsets[0] == 0 and offsets[-1] == len(codes),'layout-offset-endpoints')
    prior = 0
    for offset in offsets:
        s.integer(offset,0,len(codes),'layout-offset-range'); s.need(offset >= prior,'layout-offset-order'); prior = offset
    tree = dict(value['base'],receivers=[])
    for i in range(N):
        s.guard(ctx); actual,_ = layout.new_sequence(value['gathered'][i],N)
        gathered = None
        if actual is not None:
            runs = []
            for index in actual:
                if runs and runs[-2]+runs[-1] == index: runs[-1] += 1
                else: runs.extend((index,1))
            gathered = {'kind':'runs','data':runs} if len(runs) < len(actual) else {'kind':'literal','data':actual}
        culls = []
        for at in range(offsets[i],offsets[i+1]):
            code = s.integer(codes[at],0,0xffffffff,'layout-cull-code'); node,which = divmod(code,6)
            culls.append({'node':node,'axis':which//2,'side':'min-ge4' if which%2 == 0 else 'max-le-neg4',
                          'difference':differences[at]})
        tree['receivers'].append({'receiver':value['receiverIds'][i],'culled':culls,
                                 'leavesRef':value['leavesRefs'][i],'gathered':gathered})
    report = layout.compare_tree(tree,value,poll=lambda:s.guard(ctx))
    return tree,{'layoutQualified':True,'scope':'Representation reconstruction before independent certificate',**report}


def prior_layout(s,ctx):
    path = 'research/m31-tree-witness-layout-2026-10-17/results/check.json'
    pin = ctx['pins'][path]
    s.need(pin['sha256'] == '0ee78af6bcf73fb28a181c9a8f8c00d43c90887c2c69ae9894f12a37d61e903c','qualified-layout-pin')
    report = s.decode(s.read_pin(ctx['root'],pin))
    s.need(report['schema'] == 'm31-tree-witness-layout-check-v1'
           and report['complete'] is True and report['passed'] is True and report['layoutQualified'] is True
           and report['scientificValidated'] is False and report['storageTargetPassed'] is True
           and report['recordCount'] == len(report['records']) == 156 and report['errors'] == []
           and len(report['controls']) == 17 and [r['sourceSequence'] for r in report['targets']] == [60,63],
           'qualified-layout-prerequisite')
    return pin


def retained_prerequisites(s,ctx,saved):
    s.need(saved['schema'] == 'm31-state1000-retained-validation-v1' and saved['scientificCalls'] == 0
           and saved['errors'] == [] and [p['id'] for p in saved['prerequisites']] == ['coupled64','native-tree42','saved-layout156']
           and all(p['retainedPass'] is True and p['rerun'] is False for p in saved['prerequisites']),
           'retained-prerequisite-status-and-scope')
    for item in saved['prerequisites']:
        for key in ('checkPin','attemptPin','resultManifestPin'):
            pin = item[key]; s.need(ctx['pins'][pin['path']] == pin,'retained-prerequisite-pin'); s.read_pin(ctx['root'],pin)
    coupled_pin = saved['prerequisites'][0]['checkPin']
    s.need(coupled_pin['path'] == 'research/m31-coupled-stage-qualification-2026-10-17/results/check.json'
           and coupled_pin['bytes'] == 218691
           and coupled_pin['sha256'] == 'bff01040bddc1c7ee8bd4d27b07d1594f4dbeffc36a07ee1f727a3d7e594f33e',
           'prior-coupled64-exact-pin')
    coupled = s.decode(s.read_pin(ctx['root'],coupled_pin))
    s.need(coupled['schema'] == 'm31-coupled-stage-check-v1' and coupled['complete'] is True
           and coupled['passed'] is True and coupled['errors'] == [] and coupled['counts']['nativeReferences'] == 32
           and len(coupled['corruptions']) == 10 and all(c['passed'] for c in coupled['corruptions']),
           'prior-coupled64-retained-control')
    admission_pin = saved['storageAdmissionPin']
    s.need(ctx['pins'][admission_pin['path']] == admission_pin,'storage-admission-source-pin')
    admission = s.decode(s.read_pin(ctx['root'],admission_pin))
    s.need(admission['admitted'] is True and admission['scope'] == 'cold-complete-success-evidence-no-sharing'
           and type(admission['evidenceUpperBoundBytes']) is int
           and 0 < admission['evidenceUpperBoundBytes'] <= 160*1024**2,'registered-whole-evidence-admission')
    return coupled_pin


def main(root,expected,commit):
    s,ctx = bootstrap(root,expected,commit)
    result = {'schema':'m31-native-tree-state1000-check-v1','sourceCommit':commit,'sourceManifestSha256':expected,
              'complete':False,'passed':False,'conditionalNativeQualified':False,'highPrecisionAccuracyValidated':False,
              'controllerFullyRecomputed':False,'rkEndpointValidated':False,'freshReferenceCalls':0,
              'stages':[],'controls':[],'errors':[],
              'scope':'One source-bound seeded first projected N1000 state: full F/H0/H saved-word equivalence, exact tree omission coverage and delivered-load derivative arithmetic. No new high-precision accuracy or complete-controller claim.'}
    try:
        saved = s.completed_output(ctx,'saved-validation')
        s.need(saved['complete'] is True and saved['passed'] is True and saved['sourceCommit'] == commit
               and saved['sourceManifestSha256'] == expected,'pre-exposure-saved-prerequisites')
        result['priorCoupled64QualificationPin'] = retained_prerequisites(s,ctx,saved)
        result['priorLayoutQualificationPin'] = prior_layout(s,ctx)
        a,old,compact,layout = [s.module(ctx,name) for name in ('tree_check','stage_check','compact','layout')]
        audit = old.StageAudit(s,ctx); resolver = compact.Resolver(s,ctx)
        browser,journal = s.closed_browser(ctx)
        kinds = ['source','factories']+['wiring-control']*12+['initial','controller']+['native']*3+['stage','case-summary','driver-summary']
        s.need(len(journal) == 22 and [r['kind'] for r in journal] == kinds,'single-state-exact-journal')
        expected_counts = {'coupledStages':1,'coupledCompleted':1,'primaryNativeCalls':3,'steps':0,
                           'controllers':1,'initials':1,'safetyChecks':0,'wiringControls':12}
        s.need(ctx['science']['cases'] == [{'caseId':CASE,'n':N,'seed':SEED,'methodOrders':[list(ORDER)]}]
               and exact_equal(ctx['science']['expectedRuntimeCounts'],expected_counts)
               and ctx['science']['integration']['dt'] == ctx['science']['integration']['duration'] == ctx['science']['integration']['steps'] == 0,
               'frozen-one-state-science')
        natives,pins,events,layout_reports = {},{},{},{}
        wiring,driver_events = [],[]; initial = commands = stage_body = case_summary = None
        expected_factories = None
        for event in journal:
            s.guard(ctx); kind,pin = event['kind'],event['recordPin']; body = resolver.record(pin)
            for key in ('serializationMilliseconds','transferMilliseconds','persistMilliseconds'): elapsed(s,event[key])
            if kind == 'source':
                expected_factories = startup_source(s,ctx,body); continue
            if kind == 'factories':
                s.need(body == {'ids':expected_factories,'globalProcessModified':False,'globalBufferModified':False},
                       'actual-factory-execution-order'); continue
            if kind != 'driver-summary':
                driver_events.append((event,body.get('caseId'),body.get('stageId') or body.get('recordMeta',{}).get('stageId')))
            if kind == 'wiring-control':
                wiring.append({'kind':kind,'body':body})
            elif kind == 'initial':
                s.need(body['schema'] == 'm31-tree-browser-initial-v1' and body['caseId'] == CASE
                       and body['n'] == N and body['seed'] == SEED
                       and body['originalTimeWord'] == body['relativeTimeWord'] == a.ZERO,'fixed-fresh-t0-initial')
                initial = body
                s.need([r['id'] for r in body['input']['drones']] == list(range(N)),'initial-id-count')
                for row in body['input']['drones']:
                    s.need(all(a.finite(w) for w in a.words(row['state'],17,'initial-state')),'initial-finite')
                elapsed(s,body['initializationWallMs']); elapsed(s,body['inputEvidenceWallMs'])
            elif kind == 'controller':
                s.need(initial is not None and body['caseId'] == CASE,'controller-case-binding')
                commands = controller(audit,body,initial['input'])
                controller_ms = body['controllerWallMs']; elapsed(s,controller_ms)
            elif kind == 'native':
                method = body['method']; s.need(method == ORDER[len(natives)] and method not in natives,'exact-native-call-order')
                if method in ('H0','H'):
                    body['tree'],layout_reports[method] = reconstruct_layout(s,ctx,layout,body['tree'])
                else: s.need('tree' not in body,'F-tree-absent')
                natives[method],pins[method],events[method] = body,pin,event
            elif kind == 'stage':
                s.integer(body['stepIndex'],0,0,'stage-step-index'); s.integer(body['stageIndex'],1,1,'stage-index')
                s.need(body['caseId'] == CASE and body['stageId'] == CASE+'-step0-k1'
                       and body['stepIndex'] == 0 and body['stageIndex'] == 1 and body['arm'] == 'coupled'
                       and body['dtWord'] == body['originalTimeWord'] == body['relativeTimeWord'] == a.ZERO,'fixed-t0-stage-grid')
                s.need(exact_equal(body['rawBeforeProjection'],initial['input'])
                       and exact_equal(body['commandsBeforeEvaluation'],commands),'initial-command-first-stage-binding')
                stats = native_stage(s,ctx,a,compact,body,natives,pins,N,ORDER)
                timings(s,body['commonTiming'],('projectionWallMs','inputEvidenceWallMs','bindingAndDerivativeWallMs'))
                for timing in body['queryTimings']:
                    prior = events[timing['method']]
                    s.need(timing['serializationMilliseconds'] == prior['serializationMilliseconds']
                           and timing['transferMilliseconds'] >= prior['transferMilliseconds']
                           and timing['persistMilliseconds'] >= prior['persistMilliseconds'],'query-journal-timing-binding')
                    if timing['method'] == 'F':
                        s.need(timing['layoutEncodeWallMs'] == timing['layoutRoundtripWallMs'] == 0,'F-no-layout-work')
                arithmetic = stage_arithmetic(s,ctx,audit,body,natives['H'])
                s.need(audit.counts == {'stages':1,'droneStages':1000,'derivativeWords':17000,
                                      'projections':1000,'nativeReferences':0,'steps':0},'all-primary-derivatives')
                result['primaryCounts'] = dict(audit.counts)
                result['stages'].append({'stageId':body['stageId'],'caseId':CASE,'n':N,'stagePin':pin,
                    'nativePins':dict(pins),'work':stats,'layoutReconstruction':layout_reports,'methodOrder':body['methodOrder'],
                    'queryTimings':body['queryTimings'],'commonTiming':body['commonTiming'],**arithmetic})
                stage_body = body
            elif kind == 'case-summary':
                s.need(body['schema'] == 'm31-tree-browser-case-summary-v1' and body['caseId'] == CASE and body['n'] == N
                       and body['complete'] is True and body['completedSteps'] == 0 and body['completedStates'] == 1
                       and body['stageId'] == CASE+'-step0-k1' and body['derivativeRecords'] == N
                       and body['initializationWallMs'] == initial['initializationWallMs']
                       and body['controllerWallMs'] == controller_ms,'single-state-case-summary')
                s.need('final' not in body,'no-invented-endpoint'); elapsed(s,body['diagnosticCaseWallMs']); case_summary = body
            elif kind == 'driver-summary':
                s.need(body['schema'] == 'm31-tree-browser-driver-summary-v1' and body['complete'] is True
                       and body['exactCounts'] is True and exact_equal(body['counts'],expected_counts)
                       and len(body['stageTimings']) == len(body['cases']) == 1,'single-state-driver-counts')
                expected_case = {k:case_summary[k] for k in ('caseId','n','complete','completedSteps','completedStates','stageId',
                    'derivativeRecords','initializationWallMs','controllerWallMs','diagnosticCaseWallMs')}
                s.need(body['cases'] == [expected_case] and len(body['appendTimings']) == len(driver_events),'driver-case-append-coverage')
                for item,(prior,case_id,stage_id) in zip(body['appendTimings'],driver_events):
                    s.need(item['recordPin'] == prior['recordPin'] and item['kind'] == prior['kind']
                           and item['caseId'] == case_id and item['stageId'] == stage_id
                           and item['serializationMilliseconds'] == prior['serializationMilliseconds']
                           and item['transferMilliseconds'] >= prior['transferMilliseconds']
                           and item['persistMilliseconds'] >= prior['persistMilliseconds'],'driver-append-journal-binding')
                    for key in ('appendWallMs','serializationMilliseconds','transferMilliseconds','persistMilliseconds'): elapsed(s,item[key])
                timing = body['stageTimings'][0]
                s.need(timing['caseId'] == CASE and timing['stageId'] == CASE+'-step0-k1' and timing['status'] == 'completed'
                       and timing['methodOrder'] == list(ORDER) and timing['queryTimings'] == stage_body['queryTimings']
                       and timing['commonTiming'] == stage_body['commonTiming'],'driver-stage-timing-binding')
                elapsed(s,body['wiringWallMs']); elapsed(s,body['diagnosticBrowserWallMs'])
                result['diagnosticBrowserWallMs'] = body['diagnosticBrowserWallMs']
            resolver.clear()
        s.need(stage_body is not None and len(natives) == 3 and len(result['stages']) == 1,'single-complete-primary-state')
        result['controls'] = old.wiring_checks(audit,wiring)
        result['arithmeticFixtures'] = audit.a.arithmetic_fixtures()
        s.need(len(result['controls']) == 12 and len(result['arithmeticFixtures']) == 14
               and all(r['passed'] for r in result['controls']+result['arithmeticFixtures']),'fixed-arithmetic-wiring-controls')
        s.need(audit.counts == {'stages':1,'droneStages':1006,'derivativeWords':17102,
                              'projections':1006,'nativeReferences':0,'steps':0},'primary-plus-fixed-control-counts')
        result['countsIncludingWiringFixtures'] = dict(audit.counts)
        evidence_files = [p for part in ('records','shards') for p in (ctx['package']/'results'/part).rglob('*') if p.is_file()]
        s.need({p.relative_to(root).as_posix() for p in evidence_files} == set(resolver.seen),'exact-new-evidence-closure')
        resolver.verify_preserved()
        result['controllerScope'] = 'Pinned unchanged controller/neighbor-search source and full saved state/ID/command/elementary-target binding; no independent neighbor membership, Boids steering, desired quaternion or command-law reconstruction.'
        result['zeroSignPolicy'] = 'Literal state/ID/load words compare exactly; inherited rational derivative checks identify both zero signs numerically.'
        result['accuracyScope'] = 'Prior pinned coupled64 control only. No fresh high-precision reference, coefficient-accuracy or load-error conclusion at N1000.'
        result['complete'] = result['passed'] = result['conditionalNativeQualified'] = True
    except Exception as error:
        result['errors'].append(s.public_error(error))
    ctx['closing'] = True
    s.verify_sources(ctx); result['sourcesPreserved'] = True
    s.write(ctx,'check.json',result)
    return 0 if result['passed'] else 1


if __name__ == '__main__':
    if len(sys.argv) != 4: raise SystemExit('usage: check.py ROOT SHA COMMIT')
    raise SystemExit(main(Path(sys.argv[1]).resolve(),sys.argv[2],sys.argv[3]))

