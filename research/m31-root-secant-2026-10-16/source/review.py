#!/usr/bin/env python3
"""Independent saved-root secant audit; never imports a scientific solver."""
import hashlib
import json
import math
import pathlib
import resource
import sys
import time

try:
    import numpy as np
except Exception as error:
    print('audit dependency unavailable: '+type(error).__name__,file=sys.stderr)
    sys.exit(2)

INPUT_PIN = dict(path='research/m31-ratio-reuse-2026-10-16/results/boids16-reuse10ms-0.00125.json',bytes=15814425,
    sha256='ca0a19b3fe2c9f17ec9f89dcd0fda19a649912033fd4809882da9d7a4cfc7e07')
PROVENANCE_PINS = [
    dict(path='research/m31-ratio-reuse-2026-10-16/results/independent-review.json',bytes=27348,sha256='e88cc48df67113deb75c5fdc670991eb145031e8a15d24530f4d52c4f5b13816'),
    dict(path='research/m31-ratio-reuse-2026-10-16/results/review-run.json',bytes=3542,sha256='038344ce3a678b3d473e59e52c387d73837a699da807b663d87b5ce99b64093a'),
    dict(path='research/m31-ratio-reuse-2026-10-16/result-manifest.json',bytes=28439,sha256='b7b9b4d05f137120cb471780950d953eb906a3be389e595cb890f7d1aa0af4ae'),
    dict(path='research/publication-receipts/m31-ratio-reuse-result-2026-10-16.json',bytes=550,sha256='62498b8dbecfd6daf4b216b9c099a2a158cd85aec9aa85236f31afccb2869ab5')]
MASS,GRAVITY,ARM = .027,9.81,.028
MG = MASS*GRAVITY
HOVER = MG/4
RADIUS = math.sqrt(2)*ARM
CORNERS = np.array([[ARM,ARM],[-ARM,ARM],[-ARM,-ARM],[ARM,-ARM]])
RESULTS_CAP,PACKAGE_CAP,CLOSURE_RESERVE = 10*1024**2,16*1024**2,128*1024


class EvidenceError(Exception):
    pass


class Audit:
    def __init__(self):
        self.start = time.monotonic()
        self.checks = 0
        self.failures = []

    def guard(self):
        if time.monotonic()-self.start > 55:
            raise EvidenceError('audit cooperative wall cap')
        rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        if sys.platform != 'darwin':
            rss *= 1024
        if rss > 512*1024**2:
            raise EvidenceError('audit RSS cap')

    def check(self, value, label):
        self.checks += 1
        if not bool(value):
            self.failures.append(label)

    def require(self, value, label):
        self.check(value,label)
        if not value:
            raise EvidenceError(label)

    def close(self, actual, expected, label, atol=1e-11, rtol=1e-10):
        a,b = np.asarray(actual,dtype=float),np.asarray(expected,dtype=float)
        valid = a.shape == b.shape and np.all(np.isfinite(a)) and np.all(np.isfinite(b))
        self.check(valid and np.all(np.abs(a-b) <= atol+rtol*np.abs(b)),label)


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda:stream.read(1024*1024),b''):
            h.update(block)
    return h.hexdigest()


def child(root,relative):
    p = pathlib.Path(relative)
    if p.is_absolute() or '..' in p.parts:
        raise EvidenceError('unsafe artifact path')
    full = (root/p).resolve()
    if not full.is_relative_to(root.resolve()):
        raise EvidenceError('artifact escapes root')
    return full


def read(path):
    if path.stat().st_size > 32*1024**2:
        raise EvidenceError('oversized input artifact')
    return json.loads(path.read_text(),parse_constant=lambda _:(_ for _ in ()).throw(EvidenceError('nonfinite JSON literal')))


def verify_pin(audit,root,pin,label):
    path = child(root,pin['path'])
    audit.require(path.is_file(),label+'.present')
    audit.require(path.stat().st_size == pin['bytes'] and digest(path) == pin['sha256'],label+'.exact-pin')
    return path


def rotate_rows(q, vectors):
    cross = 2*np.cross(q[:,:3],vectors)
    return vectors+q[:,3,None]*cross+np.cross(q[:,:3],cross)


def secant_prediction(history, target_time):
    """Causal API accepts prior times/roots and target time only."""
    if not history:
        raise EvidenceError('prediction requires prior root')
    last_t,last_x = history[-1]
    if not math.isfinite(target_time) or target_time <= last_t:
        raise EvidenceError('invalid target time')
    if len(history) == 1:
        return np.array(last_x,dtype=float,copy=True)
    previous_t,previous_x = history[-2]
    if not previous_t < last_t:
        raise EvidenceError('nonincreasing predecessor times')
    scale = (target_time-last_t)/(last_t-previous_t)
    return np.asarray(last_x,dtype=float)+scale*(np.asarray(last_x,dtype=float)-np.asarray(previous_x,dtype=float))


def root_domain(roots):
    roots = np.asarray(roots,dtype=float)
    invalid = []
    for drone,rotor in np.ndindex(roots.shape):
        value = float(roots[drone,rotor])
        if not math.isfinite(value):
            tag = 'nan' if math.isnan(value) else 'positive-infinity' if value > 0 else 'negative-infinity'
            invalid.append(dict(drone=drone,rotor=rotor,reason=tag,value=None))
        elif value <= 0:
            invalid.append(dict(drone=drone,rotor=rotor,reason='nonpositive',value=value))
        elif value > 1:
            invalid.append(dict(drone=drone,rotor=rotor,reason='above-one',value=value))
    return invalid


def safe_roots(roots):
    return [[float(x) if math.isfinite(float(x)) else None for x in row] for row in roots]


def load_fields(states,roots):
    states,roots = np.asarray(states,dtype=float),np.asarray(roots,dtype=float)
    thrust = states[:,13:17]*roots
    delta = thrust-states[:,13:17]
    body_force = np.column_stack((np.zeros(len(states)),np.zeros(len(states)),np.sum(delta,axis=1)))
    force = rotate_rows(states[:,6:10],body_force)
    torque = np.column_stack((delta @ CORNERS[:,1],-delta @ CORNERS[:,0],np.zeros(len(states))))
    return dict(forces=thrust,delta=delta,worldForce=force,bodyTorque=torque)


def load_errors(actual,oracle):
    rotor = np.abs(actual['forces']-oracle['forces'])/HOVER
    force = np.linalg.norm(actual['worldForce']-oracle['worldForce'],axis=1)/MG
    moment = np.linalg.norm(actual['bodyTorque']-oracle['bodyTorque'],axis=1)/(MG*RADIUS)
    return dict(rotor=rotor,force=force,moment=moment)


def fields_finite(fields):
    return all(np.all(np.isfinite(value)) for value in fields.values())


def synthetic_controls(audit):
    """Independent formulas checked once in the official audit, never pre-run."""
    controls = []
    def check(name,actual,expected):
        before = len(audit.failures)
        audit.close(actual,expected,'synthetic.'+name,1e-14,0)
        controls.append(dict(id=name,pass_=len(audit.failures) == before))
    check('cold-start-hold',secant_prediction([(0,[[.2,.4,.6,1.]])],.01),[[.2,.4,.6,1.]])
    check('constant-roots',secant_prediction([(0,[[.5]*4]),(.01,[[.5]*4])],.02),[[.5]*4])
    check('nonuniform-linear-time',secant_prediction([(0,[[.2]*4]),(.1,[[.4]*4])],.3),[[.8]*4])
    boundary = np.array([[0.,1.,-.1,1.1],[math.nan,math.inf,-math.inf,.5]])
    invalid = root_domain(boundary)
    expected_invalid = [dict(drone=i,rotor=j,value=v,reason=r) for i,j,v,r in [
        (0,0,0.,'nonpositive'),(0,2,-.1,'nonpositive'),(0,3,1.1,'above-one'),
        (1,0,None,'nan'),(1,1,None,'positive-infinity'),(1,2,None,'negative-infinity')]]
    valid = invalid == expected_invalid
    audit.check(valid,'synthetic.invalid-domain-coverage')
    controls.append(dict(id='invalid-domain-coverage',pass_=valid))
    encoded = safe_roots(boundary)
    expected_safe = [[0.,1.,-.1,1.1],[None,None,None,.5]]
    valid = encoded == expected_safe and [x['reason'] for x in invalid[-3:]] == ['nan','positive-infinity','negative-infinity']
    audit.check(valid,'synthetic.nonfinite-json-safety')
    json.dumps(dict(roots=encoded,invalid=invalid),allow_nan=False)
    controls.append(dict(id='nonfinite-json-safety',pass_=valid))
    state = np.array([[0.,0.,4.,0.,0.,0.,0.,0.,0.,1.,0.,0.,0.,HOVER,HOVER,HOVER,HOVER]])
    check('identity-root-zero-force',load_fields(state,np.ones((1,4)))['worldForce'],[[0.,0.,0.]])
    delta = -.2*HOVER
    signs = [(1,-1),(1,1),(-1,1),(-1,-1)]
    for rotor,(sx,sy) in enumerate(signs):
        roots = np.ones((1,4)); roots[0,rotor] = .8
        fields = load_fields(state,roots)
        check('rotor-'+str(rotor)+'-force',fields['worldForce'],[[0.,0.,delta]])
        check('rotor-'+str(rotor)+'-moment',fields['bodyTorque'],[[sx*ARM*delta,sy*ARM*delta,0.]])
    return [{('pass' if k == 'pass_' else k):v for k,v in row.items()} for row in controls]


def plain(value):
    if isinstance(value,np.ndarray):
        return plain(value.tolist())
    if isinstance(value,dict):
        return {k:plain(v) for k,v in value.items()}
    if isinstance(value,(list,tuple)):
        return [plain(v) for v in value]
    if isinstance(value,(float,np.floating)):
        return float(value) if math.isfinite(value) else None
    if isinstance(value,np.integer):
        return int(value)
    return value


def compare_tree(audit,actual,expected,label):
    expected = plain(expected)
    if isinstance(expected,dict):
        audit.require(isinstance(actual,dict) and set(actual) == set(expected),label+'.keys')
        for key,want in expected.items():
            compare_tree(audit,actual[key],want,label+'.'+key)
    elif isinstance(expected,list):
        audit.require(isinstance(actual,list) and len(actual) == len(expected),label+'.length')
        for i,(value,want) in enumerate(zip(actual,expected)):
            compare_tree(audit,value,want,label+'.'+str(i))
    elif isinstance(expected,float):
        audit.require(isinstance(actual,(int,float)) and not isinstance(actual,bool),label+'.number')
        audit.close(actual,expected,label)
    else:
        audit.check(actual == expected and (not isinstance(expected,bool) or isinstance(actual,bool)),label)


def load_record(fields):
    return dict(forces=fields['forces'].tolist(),corrections=[dict(delta=d.tolist(),force=f.tolist(),torque=t.tolist())
        for d,f,t in zip(fields['delta'],fields['worldForce'],fields['bodyTorque'])])


def checked_errors(audit,saved,actual,oracle,label):
    expected = load_errors(actual,oracle)
    audit.require(fields_finite(expected),label+'.independently-computable')
    audit.require(isinstance(saved,dict) and set(saved) == {'rotor','force','moment','maxima','argmax'},label+'.keys')
    maxima,argmax,arrays = {},{},{}
    for metric,values in expected.items():
        audit.close(saved[metric],values,label+'.'+metric)
        # Max/first-tie reduction uses independently validated retained scalars.
        # This preserves the declared binary64 comparison estimand across implementations.
        array = np.asarray(saved[metric],dtype=float)
        audit.require(array.shape == values.shape and np.all(np.isfinite(array)),label+'.retained-'+metric+'-shape')
        flat = int(np.argmax(array))
        if metric == 'rotor':
            drone,rotor = divmod(flat,4)
            location = dict(drone=drone,rotor=rotor)
        else:
            location = dict(drone=flat,rotor=None)
        maxima[metric],argmax[metric],arrays[metric] = float(array.flat[flat]),location,array.tolist()
    audit.check(saved['maxima'] == maxima and saved['argmax'] == argmax,label+'.exact-first-tie-reduction')
    independent_maxima = {metric:float(np.max(values)) for metric,values in expected.items()}
    return dict(**arrays,maxima=maxima,argmax=argmax),independent_maxima


def frozen_config(audit,cfg):
    audit.require(cfg['kind'] == 'causal-saved-joint-root-secant','frozen-kind')
    audit.require(cfg['input'] == INPUT_PIN and cfg['provenance'] == PROVENANCE_PINS,'immutable-input-ancestry-pins')
    audit.require(cfg['events'] == 201 and cfg['targets'] == 200 and cfg['n'] == 16 and cfg['dt'] == .00125 and cfg['refreshDt'] == .01 and cfg['duration'] == 2,'frozen-population')
    audit.require(cfg['mass'] == MASS and cfg['gravity'] == GRAVITY and cfg['armCoordinate'] == ARM,'frozen-physical-constants')
    audit.require(cfg['rootDomain'] == 'finite and 0 < x <= 1' and cfg['thresholds'] == dict(rotor=.001,force=.001,moment=.001),'frozen-domain-thresholds')
    audit.require(cfg['agreementAtol'] == 1e-11 and cfg['agreementRtol'] == 1e-10 and cfg['residualLimit'] == 1e-9 and cfg['sourceReceiverLimit'] == 2e-9,'frozen-agreement-residuals')
    audit.require(cfg['limits'] == dict(wallSeconds=60,cooperativeSeconds=55,rssBytes=536870912,resultsBytes=RESULTS_CAP,candidateResultsBytes=6291456,logsBytes=1048576,closureReserveBytes=CLOSURE_RESERVE,packageBytes=PACKAGE_CAP),'frozen-resource-limits')
    audit.require(cfg['geometryAdmission'] == 'inherited prior audited geometry; new checks of saved metadata and root/load correspondence only','inherited-geometry-scope')


def inherited_provenance(audit,repository,cfg):
    paths = [verify_pin(audit,repository,pin,'ancestry-'+str(i)) for i,pin in enumerate([INPUT_PIN]+PROVENANCE_PINS)]
    report,closure,manifest,receipt = [read(path) for path in paths[1:]]
    audit.require(report['kind'] == 'independent-saved-ratio-reuse-review' and report['complete'] is True and report['pass'] is True and report['failures'] == [],'prior-independent-audit-success')
    audit.require(report['allocationPass'] is True and report['reuseExecuted'] is True,'prior-numerical-allocation-success')
    audit.require(closure['kind'] == 'review' and closure['returncode'] == 0 and closure['supervisor_success'] is True,'prior-external-review-success')
    audit.require(not any(closure.get(k) for k in ['exception_class','terminated_for','cleanup_exception_class','monitorErrors']) and closure['rssSamples'] > 0 and closure['rssSampleErrors'] == 0,'prior-external-clean-monitor')
    audit.require(report['sourceCommit'] == closure['source_commit'] == manifest['sourceCommit'] and report['sourceManifestSHA256'] == closure['source_manifest_sha256'],'prior-source-ancestry')
    audit.require(manifest['pathBase'] == 'repository root' and manifest['independentSavedReview'] == 'pass' and manifest['scientificAllocations'] == 'closed; no reruns','prior-manifest-status')
    manifest_pins = {p['path']:p for p in manifest['files']}
    audit.require(len(manifest_pins) == len(manifest['files']),'prior-manifest-unique-paths')
    for pin in [INPUT_PIN]+PROVENANCE_PINS[:2]:
        audit.require(manifest_pins.get(pin['path']) == pin,'prior-manifest-pin-'+pin['path'])
    closure_pins = {p['path']:p for p in closure['artifacts']}
    old_prefix = 'research/m31-ratio-reuse-2026-10-16/'
    for pin in [INPUT_PIN,PROVENANCE_PINS[0]]:
        local = dict(pin,path=pin['path'][len(old_prefix):])
        audit.require(closure_pins.get(local['path']) == local,'prior-closure-pin-'+local['path'])
    audit.require(receipt['kind'] == 'independent-GitHub-connector-result-verification' and receipt['manifestSha256'] == PROVENANCE_PINS[2]['sha256'] and receipt['manifestBytes'] == PROVENANCE_PINS[2]['bytes'],'prior-publication-manifest-identity')
    audit.require(receipt['remoteManifestMatchesLocal'] is True and receipt['localAndCommittedPinsMatch'] is True and receipt['independentSavedReview'] == 'pass','prior-publication-success')
    audit.require(receipt['pinsVerified'] == len(manifest['files']) and receipt['pinnedBytes'] == sum(p['bytes'] for p in manifest['files']),'prior-publication-pin-counts')
    return paths[0],dict(geometry='inherited; no geometry or root solve executed by this audit',sourceCommit=report['sourceCommit'],resultCommit=receipt['commit'],resultManifestSHA256=PROVENANCE_PINS[2]['sha256'])


def check_cached_info(audit,info,index,t,at,label):
    audit.require(info['evaluation'] == 'cached-ratio' and info['cacheIndex'] == index and info['cacheTime'] == t,label+'.cache-source')
    audit.close(info['cacheAge'],at-t,label+'.cache-age',1e-12,0)
    audit.require(all(info[k] is None for k in ['edges','positiveTerms','residual','sourceReceiverMismatch','symbolCounts','admitted','descendingEligible']),label+'.no-current-closure-claim')


def admit_event(audit,event,index,cfg,previous):
    audit.guard()
    failures_before = len(audit.failures)
    label = 'input-event-'+str(index)
    t = round(index*.01,6)
    audit.require(event['index'] == index and event['t'] == t and event['status'] == 'completed' and event['role'] == ('terminal-audit' if index == 200 else 'propagation-refresh'),label+'.identity')
    audit.require(event['oldCacheIndex'] == (index-1 if index else None),label+'.predecessor')
    states,commands = np.asarray(event['states'],dtype=float),np.asarray(event['commands'],dtype=float)
    audit.require(states.shape == (16,17) and commands.shape == (16,4) and np.all(np.isfinite(states)) and np.all(np.isfinite(commands)),label+'.state-command-finite-shapes')
    audit.require(np.all(states[:,13:17] > 0) and np.all(np.isfinite(np.sum(states[:,13:17],axis=1))),label+'.nominal-motor-domain')
    audit.require(np.all(np.abs(np.linalg.norm(states[:,6:10],axis=1)-1) <= 1e-12),label+'.unit-quaternion')
    audit.require(np.all(commands >= 0) and np.all(commands <= 2.25*HOVER+1e-12),label+'.command-range')
    instant = event['instantaneous']
    info = instant['info']
    audit.require(info['evaluation'] == 'instantaneous' and info['admitted'] is True and info['descendingEligible'] is True and all(info[k] is None for k in ['cacheIndex','cacheTime','cacheAge']),label+'.fresh-admission')
    audit.require(math.isfinite(info['residual']) and 0 <= info['residual'] <= cfg['residualLimit'] and math.isfinite(info['sourceReceiverMismatch']) and 0 <= info['sourceReceiverMismatch'] <= cfg['sourceReceiverLimit'],label+'.fresh-residual-metadata')
    roots = np.asarray([[v['x'] for v in row] for row in instant['witness']['rotors']],dtype=float)
    audit.require(roots.shape == (16,4) and not root_domain(roots),label+'.fresh-root-domain')
    audit.require(event['cache'] == dict(index=index,t=t,ratios=roots.tolist()),label+'.direct-witness-cache-identity')
    fresh = load_fields(states,roots)
    audit.require(fields_finite(fresh),label+'.finite-fresh-loads')
    expected = load_record(fresh)
    for side in ['instantaneous','right']:
        compare_tree(audit,event[side]['forces'],expected['forces'],label+'.'+side+'.forces')
        for key in ['corrections','modeledCorrections']:
            compare_tree(audit,event[side][key],expected['corrections'],label+'.'+side+'.'+key)
    check_cached_info(audit,event['right']['info'],index,t,t,label+'.right')
    audit.require(event['right']['witness'] is None,label+'.right-no-geometry')
    if index:
        audit.require(previous is not None and isinstance(event['left'],dict),label+'.left-present')
        held = load_fields(states,previous)
        audit.require(fields_finite(held),label+'.finite-held-loads')
        held_record = load_record(held)
        compare_tree(audit,event['left']['forces'],held_record['forces'],label+'.left.forces')
        for key in ['corrections','modeledCorrections']:
            compare_tree(audit,event['left'][key],held_record['corrections'],label+'.left.'+key)
        check_cached_info(audit,event['left']['info'],index-1,round((index-1)*.01,6),t,label+'.left')
        audit.require(event['left']['witness'] is None,label+'.left-no-geometry')
    else:
        audit.require(event['left'] is None and event['error'] is None,label+'.cold-start-no-left')
    audit.require(len(audit.failures) == failures_before,label+'.all-input-correspondences-admitted')
    return roots,states,fresh


def candidate_controls(audit,package):
    saved = read(package/'results/controls.json')
    expected = [
        dict(id='startup',roots=[[.5,.75,1.,.1]],scale=None,invalidRoots=[]),
        dict(id='constant',roots=[[.5,.75,1.,.1]],scale=1.,invalidRoots=[]),
        dict(id='linear',roots=[[.35,.45,.55,.65]],scale=.5,invalidRoots=[]),
        dict(id='overshoot',roots=[[1.1]],scale=1.,invalidRoots=[dict(drone=0,rotor=0,value=1.1,reason='above-one')]),
        dict(id='serialization',roots=[[None,None,None,0.,1.1]],scale=None,
             invalidRoots=[dict(drone=0,rotor=i,value=v,reason=r) for i,(v,r) in enumerate([
                (None,'nan'),(None,'positive-infinity'),(None,'negative-infinity'),(0.,'nonpositive'),(1.1,'above-one')])])]
    compare_tree(audit,saved,expected,'candidate-synthetic-controls')
    return expected


def current_provenance(audit,package):
    cfg = read(package/'config.json')
    closure = read(package/'results/candidate-run.json')
    audit.require(closure['kind'] == 'candidate' and closure['closed'] is True and closure['supervisorSuccess'] is True and closure['returncode'] == 0,'candidate-external-success')
    audit.require(closure['childGroupAbsent'] is True and closure['protectedInputsUnchanged'] is True and closure['candidateOutputsUnchanged'] is True,'candidate-protected-state')
    audit.require(not any(closure.get(k) for k in ['exception','cleanupError','finalizationError','monitorErrors','signals','finalStorageCapExceeded']),'candidate-no-external-failure')
    audit.require(closure['wallCapSeconds'] == 60 and closure['rssCapBytes'] == 512*1024**2 and closure['performanceMeasurement'] is False and closure['inheritedInputCopied'] is False,'candidate-bound-scope')
    audit.require(closure['rssSamples'] > 0 and isinstance(closure['sampledPeakRSSBytes'],(int,float)) and 0 < closure['sampledPeakRSSBytes'] <= 512*1024**2,'candidate-rss-observations')
    audit.require(math.isfinite(closure['elapsedSeconds']) and 0 <= closure['elapsedSeconds'] <= 60,'candidate-wall-bound')
    audit.require(closure['logBytes'] <= 1024**2,'candidate-log-bound')
    manifest_path = package/'source-manifest.json'
    audit.require(digest(manifest_path) == closure['sourceManifestSha256'],'new-source-manifest-identity')
    manifest = read(manifest_path)
    repository = package.parent.parent
    pins = manifest['files']
    indexed = {p['path']:p for p in pins}
    audit.require(len(indexed) == len(pins),'new-source-unique-pins')
    for pin in pins:
        audit.guard()
        verify_pin(audit,repository,pin,'frozen-source.'+pin['path'])
    for pin in [INPUT_PIN]+PROVENANCE_PINS:
        audit.require(indexed.get(pin['path']) == pin,'new-source-input-ancestry-pin')
    prefix = package.relative_to(repository).as_posix()+'/'
    for name in ['config.json','PROTOCOL.md','source/candidate.py','source/review.py','source/run.py']:
        audit.require(prefix+name in indexed,'new-source-required-'+name)
    audit.require(not child(repository,INPUT_PIN['path']).is_relative_to(package),'inherited-input-external-reference')
    artifacts = closure['artifacts']
    audit.require(len({p['path'] for p in artifacts}) == len(artifacts),'candidate-artifact-unique-pins')
    for pin in artifacts:
        verify_pin(audit,package,pin,'candidate-artifact.'+pin['path'])
    artifact_names = {p['path'] for p in artifacts}
    for name in ['controls.json','prediction-trace.jsonl','events.jsonl','summary.json','candidate-invocation.lock','candidate-stdout.txt','candidate-stderr.txt']:
        audit.require('results/'+name in artifact_names,'candidate-required-'+name)
    audit.require(sum(p['bytes'] for p in artifacts) == closure['resultsBytesBeforeClosure'],'candidate-artifact-byte-accounting')
    audit.require(closure['resultsBytesBeforeClosure']+(package/'results/candidate-run.json').stat().st_size <= cfg['limits']['candidateResultsBytes'] and closure['packageBytesBeforeClosure']+(package/'results/candidate-run.json').stat().st_size <= PACKAGE_CAP,'candidate-final-storage-accounting')
    return closure


def read_jsonl(audit,path,label):
    audit.require(path.stat().st_size <= RESULTS_CAP,label+'.size')
    lines = path.read_text().splitlines()
    audit.require(len(lines) == 200 and all(line.strip() for line in lines),label+'.fixed-coverage')
    return [json.loads(line,parse_constant=lambda _:(_ for _ in ()).throw(EvidenceError('nonfinite JSON literal'))) for line in lines]


def summarize(rows,cfg,primary):
    output = dict(targets=len(rows),scoredEvents=sum(r['scoreStatus'] == 'scored' for r in rows),
        invalidEvents=sum(not r['validRoots'] for r in rows),invalidRoots=sum(len(r['invalidRoots']) for r in rows),modes={})
    for mode in ['predict','hold']:
        available = [r for r in rows if r['errors'][mode] is not None]
        maxima,locations = {},{}
        for metric in ['rotor','force','moment']:
            if available:
                values = [r['errors'][mode]['maxima'][metric] for r in available]
                row = available[int(np.argmax(values))]
                maxima[metric] = row['errors'][mode]['maxima'][metric]
                locations[metric] = dict(event=row['index'],t=row['t'],**row['errors'][mode]['argmax'][metric])
            else:
                maxima[metric],locations[metric] = None,None
        complete = len(available) == len(rows)
        output['modes'][mode] = dict(complete=complete,maxima=maxima if complete else {k:None for k in maxima},finiteDiagnosticMaxima=maxima,argmax=locations)
    output['paired'] = [dict(event=r['index'],t=r['t'],validRoots=r['validRoots'],
        predict=None if r['errors']['predict'] is None else r['errors']['predict']['maxima'],
        hold=None if r['errors']['hold'] is None else r['errors']['hold']['maxima']) for r in rows]
    output['comparisons'] = {}
    for metric in ['rotor','force','moment']:
        counts = dict(better=0,equal=0,worse=0)
        for row in rows:
            if row['errors']['predict'] is None or row['errors']['hold'] is None:
                continue
            a,b = (row['errors'][mode]['maxima'][metric] for mode in ['predict','hold'])
            counts['better' if a < b else 'worse' if a > b else 'equal'] += 1
        output['comparisons'][metric] = counts
    output['gates'] = {}
    for metric,tolerance in cfg['thresholds'].items():
        a,b = output['modes']['predict'],output['modes']['hold']
        output['gates'][metric] = dict(tolerance=tolerance,
            absolute=a['complete'] and a['maxima'][metric] <= tolerance,
            noWorseThanHold=a['complete'] and b['complete'] and a['maxima'][metric] <= b['maxima'][metric])
    if primary:
        output['pass'] = (len(rows) == 200 and output['scoredEvents'] == 200 and output['invalidRoots'] == 0
            and all(g['absolute'] and g['noWorseThanHold'] for g in output['gates'].values()))
    return output


def strict_independent_summary(rows,cfg):
    """Qualification uses reconstructed errors, never tolerance-accepted saved scalars."""
    output = dict(targets=len(rows),scoredEvents=sum(r['predict'] is not None for r in rows),
        invalidRoots=sum(r['invalidRootCount'] for r in rows),modes={})
    for mode in ['predict','hold']:
        available = [r[mode] for r in rows if r[mode] is not None]
        finite = {k:max((r[k] for r in available),default=None) for k in cfg['thresholds']}
        complete = len(available) == len(rows)
        output['modes'][mode] = dict(complete=complete,maxima=finite if complete else {k:None for k in finite},finiteDiagnosticMaxima=finite)
    output['gates'] = {}
    a,b = output['modes']['predict'],output['modes']['hold']
    for metric,tolerance in cfg['thresholds'].items():
        output['gates'][metric] = dict(tolerance=tolerance,
            absolute=a['complete'] and a['maxima'][metric] <= tolerance,
            noWorseThanHold=a['complete'] and b['complete'] and a['maxima'][metric] <= b['maxima'][metric])
    output['pass'] = len(rows) == 200 and output['scoredEvents'] == 200 and output['invalidRoots'] == 0 and all(g['absolute'] and g['noWorseThanHold'] for g in output['gates'].values())
    return output


def run(audit,package):
    cfg = read(package/'config.json')
    frozen_config(audit,cfg)
    candidate_closure = current_provenance(audit,package)
    raw_path,ancestry = inherited_provenance(audit,package.parent.parent,cfg)
    independent_controls = synthetic_controls(audit)
    candidate_controls(audit,package)
    source = read(raw_path)
    audit.require(source['id'] == 'boids16-reuse10ms-0.00125' and source['case'] == 'boids16' and source['mode'] == 'reuse10ms' and source['dt'] == .00125 and source['end'] == 2 and source['complete'] is True and source['failure'] is None,'completed-exact-input-identity')
    audit.require(len(source['events']) == 201,'input-event-count')
    audit.require(source['events'][0]['states'] == source['initial'] and source['events'][-1]['states'] == source['final'],'input-initial-final-identity')
    audit.require(source['counts']['refreshEventAttempts'] == 201 and source['counts']['propagationRefreshAttempts'] == 200 and source['counts']['terminalAuditAttempts'] == 1,'input-event-role-counts')
    trace = read_jsonl(audit,package/'results/prediction-trace.jsonl','prediction-trace')
    saved_rows = read_jsonl(audit,package/'results/events.jsonl','scored-events')
    root0,_,_ = admit_event(audit,source['events'][0],0,cfg,None)
    history = [(0.,root0)]
    rows,invalid_locations,independent_rows = [],[],[]
    for index in range(1,201):
        audit.guard()
        t = round(index*.01,6)
        # Prediction and its trace check precede access to the current oracle below.
        prediction = secant_prediction(history,t)
        predecessors = [0] if index == 1 else [index-2,index-1]
        scale = None if index == 1 else (t-history[-1][0])/(history[-1][0]-history[-2][0])
        label = 'target-'+str(index)
        expected_trace = dict(index=index,t=t,predecessorIds=predecessors,scale=scale,predictedRoots=safe_roots(prediction))
        compare_tree(audit,trace[index-1],expected_trace,label+'.causal-trace')
        roots,states,fresh = admit_event(audit,source['events'][index],index,cfg,history[-1][1])
        held = load_fields(states,history[-1][1])
        saved = saved_rows[index-1]
        invalid = root_domain(prediction)
        invalid_locations.extend(dict(event=index,t=t,**item) for item in invalid)
        expected = dict(index=index,t=t,predecessorIds=predecessors,method='cold-start-hold' if index == 1 else 'secant',
            scale=scale,predictedRoots=safe_roots(prediction),holdRoots=history[-1][1].tolist(),oracleRoots=roots.tolist(),
            validRoots=not invalid,invalidRoots=invalid,scoreStatus='scored',scoreReason=None,
            loads=dict(predict=None,hold=load_record(held),fresh=load_record(fresh)),errors=dict(predict=None,hold=None))
        expected['errors']['hold'],independent_hold = checked_errors(audit,saved['errors']['hold'],held,fresh,label+'.hold-errors')
        independent_predict = None
        if np.all(np.isfinite(prediction)):
            predicted_fields = load_fields(states,prediction)
            predicted_errors = load_errors(predicted_fields,fresh)
            if fields_finite(predicted_fields) and fields_finite(predicted_errors):
                expected['loads']['predict'] = load_record(predicted_fields)
                expected['errors']['predict'],independent_predict = checked_errors(audit,saved['errors']['predict'],predicted_fields,fresh,label+'.predict-errors')
            else:
                expected['scoreStatus'],expected['scoreReason'] = 'unscored','uncomputable-error'
        else:
            expected['scoreStatus'],expected['scoreReason'] = 'unscored','nonfinite-predicted-root'
        compare_tree(audit,saved,expected,label+'.full-record')
        rows.append(expected)
        independent_rows.append(dict(event=index,t=t,invalidRootCount=len(invalid),predict=independent_predict,hold=independent_hold))
        history = (history+[(t,roots)])[-2:]
    primary,secondary = summarize(rows,cfg,True),summarize(rows[1:],cfg,False)
    strict = strict_independent_summary(independent_rows,cfg)
    summary = read(package/'results/summary.json')
    elapsed = summary['elapsedSeconds']
    audit.require(isinstance(elapsed,(int,float)) and math.isfinite(elapsed) and 0 <= elapsed <= 55,'candidate-cooperative-time-record')
    decision = 'passed-endpoint-screen' if primary['pass'] else 'rejected-fixed-secant'
    expected_summary = dict(kind=cfg['kind'],input=INPUT_PIN,inheritedGeometry=True,inputAdmission=True,complete=True,
        primary=primary,secondarySecantOnly=secondary,scientificPass=primary['pass'],decision=decision,
        elapsedSeconds=elapsed,performanceMeasurement=False)
    compare_tree(audit,summary,expected_summary,'complete-summary')
    for metric in cfg['thresholds']:
        for gate in ['absolute','noWorseThanHold']:
            audit.check(summary['primary']['gates'][metric][gate] is strict['gates'][metric][gate],
                'strict-independent-gate.'+metric+'.'+gate)
    audit.check(summary['primary']['pass'] is strict['pass'] and summary['scientificPass'] is strict['pass'],'strict-independent-scientific-qualification')
    audit.require(primary['targets'] == 200 and secondary['targets'] == 199 and len(primary['paired']) == 200 and primary['paired'][0]['event'] == 1 and primary['paired'][-1]['event'] == 200,'mandatory-primary-secondary-coverage')
    return dict(inputAdmission=True,input=INPUT_PIN,inheritedGeometry=ancestry,completeTargets=200,
        primary=primary,secondarySecantOnly=secondary,independentPrimaryStrict=strict,
        independentEventMaxima=independent_rows,scientificPass=strict['pass'],candidateScientificPass=summary['scientificPass'],
        decision='passed-endpoint-screen' if strict['pass'] else 'rejected-fixed-secant',
        invalidRootLocations=invalid_locations,independentSyntheticControls=independent_controls,
        candidateSyntheticFixturesChecked=5,newSourceCommit=candidate_closure['sourceCommit'],newSourceManifestSha256=candidate_closure['sourceManifestSha256'],
        candidateExternalElapsedSeconds=candidate_closure['elapsedSeconds'],candidateSampledPeakRSSBytes=candidate_closure['sampledPeakRSSBytes'])


def directory_bytes(path):
    return sum(p.stat().st_size for p in path.rglob('*') if p.is_file())


def main():
    audit = Audit()
    np.seterr(all='ignore')
    if len(sys.argv) != 2:
        print('review requires one package argument',file=sys.stderr)
        return 2
    package = pathlib.Path(sys.argv[1]).resolve()
    output_path = package/'results/independent-review.json'
    result = dict(kind='independent-saved-root-secant-review',complete=False,
        method='independent NumPy causal-root/current-load/error reconstruction; no solver import or trajectory evaluation',
        limits=['Geometry and root-solver correctness are inherited from pinned successful prior evidence, not recomputed.',
                'Causality is checked from prior-only independent reconstruction plus the frozen flushed-trace source ordering; JSON loading itself is not hidden-data protection.',
                'Every per-drone error is independently checked; retained scalar reductions preserve exact argmax/tie identity, while scientific gates are separately recomputed strictly from independent errors.',
                'All 200 positive endpoints include cold start and terminal audit; 199 secant-only endpoints have no separate qualification.',
                'Domain-invalid finite predictions retain diagnostics; invalid roots or incomplete scoring reject scientific qualification.',
                'This exposed fixed-trajectory endpoint diagnostic does not establish intermediate-time accuracy, feedback-predictor stability, speedup, physical validity or novelty.'])
    try:
        with output_path.open('x',encoding='utf8') as output:
            try:
                result.update(run(audit,package))
                audit.guard()
                result['complete'] = True
            except Exception as error:
                audit.check(False,'audit-error.'+type(error).__name__)
                print('independent saved audit stopped: '+type(error).__name__,file=sys.stderr)
            result.update(pass_=result['complete'] and not audit.failures,checks=audit.checks,failures=audit.failures,elapsedSeconds=time.monotonic()-audit.start)
            result['pass'] = result.pop('pass_')
            encoded = json.dumps(plain(result),allow_nan=False,indent=2)+'\n'
            results_bytes,package_bytes = directory_bytes(package/'results'),directory_bytes(package)
            size = len(encoded.encode())
            if results_bytes+size > RESULTS_CAP-CLOSURE_RESERVE or package_bytes+size > PACKAGE_CAP-CLOSURE_RESERVE:
                raise EvidenceError('review output would consume reserved closure capacity')
            output.write(encoded)
        print(json.dumps(dict(complete=result['complete'],auditPass=result['pass'],scientificPass=result.get('scientificPass'),checks=audit.checks)))
        return 0 if result['pass'] else 1
    except Exception as error:
        print('independent audit output stopped: '+type(error).__name__,file=sys.stderr)
        return 1


if __name__ == '__main__':
    if sys.flags.optimize:
        raise RuntimeError('Nonoptimized Python required')
    sys.exit(main())
