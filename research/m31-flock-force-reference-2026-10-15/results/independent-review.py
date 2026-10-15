"""One authorized saved-evidence review; never import/execute campaign science.

Usage (only after explicit authorization):
  python3 m31-force-saved-review.py REPOSITORY --authorized-after-science
The caller must also retain an external launch record and impose <=59 seconds.
Preparation of this file is not authorization to execute it.
"""
import base64
import contextlib
import hashlib
import json
import math
import signal
import struct
import sys
import time
import traceback
import zlib
from collections import Counter
from pathlib import Path

SOURCE_COMMIT = '89c3b14e6d59f2446d257bd106e3af4bbcb029c6'
FREEZE_SHA = 'c6c6c91dbde3e342da355474d60f5bd2b81316c8c31cefe4a87777fa21c5456a'
METADATA_SHA = 'f69cae28818dd0802863b512af96a448ffcd3aa7aa8824f528b4ed59032d613c'
BINARY_SHA = 'c9918697fc61576a9c0454cda354a8d66f42b0b6e21e082cdbf12054b372c927'
DOMAIN_RESULT_SHA = '7e8cf6d53fe4a94c7c6faaf1bc1af36dfd1f30da6b519680c3a82d84ab2f5584'
DOMAIN_MANIFEST_SHA = 'd6589044982631ba85fcf325c3c14f3752a827f0ce6b4fb96fd21e3f061edf4b'
CAMPAIGN = 'research/m31-flock-force-reference-2026-10-15'
DOMAIN = 'research/m31-flock-domain-2026-10-15'
ROTOR_COLUMNS = ['U_primary_mps','U_independent_mps','U_compensated_mps','f_primary_N','f_independent_N','x_primary','x_independent','alpha_primary','alpha_independent','residual_primary','residual_independent','bracket_lower','bracket_upper','bisection_iterations','power_primary_W','power_independent_W']
VEHICLE_COLUMNS = ['T_primary_N','T_independent_N','mx_primary_Nm','my_primary_Nm','mz_primary_Nm','mx_independent_Nm','my_independent_Nm','mz_independent_Nm','Fx_primary_N','Fy_primary_N','Fz_primary_N','Fx_independent_N','Fy_independent_N','Fz_independent_N','deltaFx_primary_N','deltaFy_primary_N','deltaFz_primary_N','deltaFx_independent_N','deltaFy_independent_N','deltaFz_independent_N','deltaT_primary_N','deltaT_independent_N','worldMx_primary_Nm','worldMy_primary_Nm','worldMz_primary_Nm','worldMx_independent_Nm','worldMy_independent_Nm','worldMz_independent_Nm','axisX_primary','axisY_primary','axisZ_primary','axisX_independent','axisY_independent','axisZ_independent','quaternion_norm_error']
METRICS = ['inflow','compensated','rotorThrust','bodyThrust','roll','pitch','worldForce','worldForceChange','worldMoment','rootResidualPrimary','rootResidualIndependent','powerResidualPrimary','powerResidualIndependent']
# These are checker arithmetic tolerances, never additions to scientific gates.
ARITH_ABS = 2e-16
ARITH_REL = 8e-15
RESIDUAL_ARITH_ABS = 4e-15
SUMMARY_REL = 5e-13
START = time.perf_counter()
RUN = Path('/tmp/m31-force-verifier-runs') / str(time.time_ns())
RUN.mkdir(parents=True, exist_ok=False)
SCRIPT = Path(__file__).read_bytes()
(RUN / 'checker.py').write_bytes(SCRIPT)
COUNTS = Counter()
FAILURES = []
FAILED_COUNT = 0
CURRENT = {'phase': 'startup'}
REPORT = {
    'scope': 'One saved-data-only review of the complete static prescribed-input campaign. No geometry regeneration, quaternion rotation, field evaluation, root solving, integration, fixture, or science execution.',
    'method': {
        'script': 'm31-force-saved-review.py', 'scriptSha256': hashlib.sha256(SCRIPT).hexdigest(),
        'invocationArchive': str(RUN), 'sourceCommit': SOURCE_COMMIT,
        'wallAllowanceSeconds': 60, 'internalAlarmSeconds': 55,
        'checkerArithmeticTolerance': {'absolute': ARITH_ABS, 'relative': ARITH_REL, 'cubicResidualReconstructionAbsolute': RESIDUAL_ARITH_ABS, 'summaryRelative': SUMMARY_REL, 'summaryAbsoluteMaximumAndRMS': 1e-30, 'summaryAbsoluteSumSquares': 1e-55},
        'toleranceSeparation': 'Every frozen scientific comparison is rechecked without adding checker arithmetic tolerance. Checker tolerances apply only to independently recomputed scalar formulas, saved-axis relations, and summary arithmetic.',
        'powerBaseline': 'Select the first retained exact-zero-inflow/exact-nominal-thrust rotor power for each implementation; verify all such baseline records and the scalar nominal-power formula. This retained baseline reproduces original power-discrepancy statistics without accidental bit-equality demands on a Python square root. Also recheck each power identity against the independently computed nominal power with the unchanged scientific gate.',
        'statistics': 'Sequential sum of squares, first maximizing index, all zeros retained; nearest-rank q50/q95 over every primary vehicle.',
        'codeCoverage': 'Inflate every pinned prior complete 4N-byte vector; check both hashes, all eight counts, eligibility groups, self slots and current metadata. Derive the exact early-break contributor-code inspection count using saved bytes only.'
    },
    'sourceHashes': [], 'rawHashes': [], 'snapshots': [],
    'limitations': [
        'The current force campaign retains code hashes, not a duplicate code vector. Every prior vector is fully decoded and matches both prior/current digests; the independent field classification itself is not regenerated.',
        'No world rotor positions are saved in the new binary records. Saved axis discrepancies can be recomputed, but the reported maximum geometry discrepancy also includes unsaved rotor coordinates and is checked only as retained runtime evidence within its frozen gate.',
        'World force and force change are cross-checked against saved axes. A single saved thrust axis does not determine roll about that axis, so world-moment rotation cannot be independently reconstructed; retained components, their cross-implementation gates and their orthogonality to the saved axis are checked.',
        'Quaternion norm defects and domain predicates are retained evidence tied to pinned prior rows; they are not recalculated from pose quaternions.',
        'Operation counters are recorded execution evidence reconciled against complete saved coverage; this review does not independently instrument the original execution.',
        'Binary64 root residuals and brackets are diagnostics, not formally rounded interval certificates. No roots are solved in this review.',
        'Passing is only finite static arithmetic qualification of prescribed inputs on selected historical poses. It is not physical validation, reconstructed historical motor loads, trajectory convergence, temporal/spatial approximation acceptance, or a speed claim.'
    ]
}

def sha(data):
    return hashlib.sha256(data).hexdigest()

def read(path):
    return json.loads(path.read_text())

def finite(values):
    return all(isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v) for v in values)

def check(ok, category, context=None):
    global FAILED_COUNT
    COUNTS[category] += 1
    if not ok:
        FAILED_COUNT += 1
        if len(FAILURES) < 300:
            FAILURES.append({'check': category, 'context': CURRENT if context is None else context})

def must(ok, category, context=None):
    check(ok, category, context)
    if not ok:
        raise ValueError('Cannot continue safely: ' + category)

def close(a, b, absolute=ARITH_ABS, relative=ARITH_REL):
    return finite([a, b]) and abs(a-b) <= absolute + relative*max(abs(a), abs(b))

def gate(a, b, absolute, relative=0):
    return finite([a, b]) and abs(a-b) <= absolute + relative*max(abs(a), abs(b))

def power(thrust, inflow, area):
    return thrust*(inflow/2 + math.sqrt(inflow*inflow/4 + thrust/(2*1.225*area)))

def statistic():
    return {'count': 0, 'sumSquares': 0.0, 'maximum': 0.0, 'maximumAt': None}

def add(stat, value, at):
    stat['count'] += 1
    stat['sumSquares'] += value*value
    if stat['maximumAt'] is None or value > stat['maximum']:
        stat['maximum'], stat['maximumAt'] = value, at

def distribution(values):
    values = sorted(values)
    n = len(values)
    return {'count': n, 'minimum': values[0], 'q50': values[math.ceil(.5*n)-1], 'q95': values[math.ceil(.95*n)-1], 'maximum': values[-1]}

def alarm(signum, frame):
    raise TimeoutError('Saved-data reviewer reached its 55-second internal wall limit')

def verify(repo):
    global CURRENT
    base, prior_base = repo / CAMPAIGN, repo / DOMAIN
    c, schema = read(base / 'config.json'), read(base / 'schema.json')
    result_bytes = (base / 'results/result.json').read_bytes()
    r = json.loads(result_bytes)
    started = read(base / 'raw/started.json')
    budget_bytes = (base / 'results/budget.json').read_bytes()
    budget = json.loads(budget_bytes)
    (RUN / 'scientific-result-original.json').write_bytes(result_bytes)
    (RUN / 'scientific-budget-original.json').write_bytes(budget_bytes)
    (RUN / 'scientific-started-original.json').write_bytes((base / 'raw/started.json').read_bytes())
    freeze_bytes = (base / 'freeze.json').read_bytes()
    freeze = json.loads(freeze_bytes)
    must(sha(freeze_bytes) == FREEZE_SHA and len(freeze['files']) == 22, 'pinned 22-file freeze')
    REPORT['freezeSha256'] = sha(freeze_bytes)
    check(r['sourceCommit'] == started['sourceCommit'] == SOURCE_COMMIT, 'frozen source commit')
    check(r == read(base / 'raw/result.json') and r['config'] == started['config'] == c and r['schema'] == started['schema'] == schema, 'published/raw/start/config/schema equality')
    check(r['status'] == 'complete static full-flock equation qualification', 'complete qualification status')
    check(c['times'] == [0,20,30,60] and c['caseIndices'] == [0,1,2] and c['variantIndex'] == 0 and c['expectedCounts'] == [1000,1000,5000], 'frozen complete selection')
    check(c['inputCommit'] == '07e5165fa56f2f23bab24562b278dda1c82ed05e' and c['historicalBase'] == 'c591ce2b195fa01b895d4ba881a44a4b92fdd703' and c['domainResultCommit'] == '770c2e77867b039e20ff5082e9299298aebc5642', 'pinned historical provenance')
    must(c['mode'] == 'sum-rotor' and c['nominalRotorThrustN'] == .0662175, 'prescribed mode and motor input')
    expected_gates = {'unitQuaternionTolerance':1e-10,'geometryAgreementTolerance':1e-12,'inflowTolerance':{'absolute':1e-11,'relative':1e-12},'rotorThrustToleranceN':1e-12,'bodyThrustToleranceN':5e-12,'bodyMomentToleranceNm':2e-13,'worldForceToleranceN':1e-11,'worldMomentToleranceNm':1e-12,'rootResidualTolerance':1e-12,'rootBracketWidthTolerance':2e-15,'idealPowerTolerance':{'absolute':1e-14,'relative':1e-12}}
    must(all(c[k] == v for k,v in expected_gates.items()), 'unchanged frozen scientific gates')
    must(schema['type'] == 'Float64LE' and schema['rotorColumns'] == ROTOR_COLUMNS and schema['vehicleColumns'] == VEHICLE_COLUMNS and schema['rotorRowOrder'] == 'receiver ascending then rotor0..3' and schema['vehicleRowOrder'] == 'receiver ascending', 'exact saved binary schema')
    for item in freeze['files']:
        CURRENT = {'phase':'frozen-file', 'path':item['path']}
        payload = (repo / item['path']).read_bytes()
        matched = len(payload) == item['bytes'] and sha(payload) == item['sha256']
        check(matched, 'frozen file bytes/hash', item['path'])
        REPORT['sourceHashes'].append({'path':item['path'],'bytes':len(payload),'sha256':sha(payload),'matches':matched})
    CURRENT = {'phase':'pinned-inputs-and-domain'}
    metadata_bytes = (repo / c['inputMetadata']).read_bytes()
    binary = (repo / c['inputBinary']).read_bytes()
    metadata = json.loads(metadata_bytes)
    must(sha(metadata_bytes) == c['expectedMetadataSha256'] == METADATA_SHA, 'pinned input metadata hash')
    must(sha(binary) == c['expectedBinarySha256'] == metadata['binarySha256'] == BINARY_SHA and len(binary) == c['expectedBinaryBytes'] == metadata['binaryBytes'] == 3360000, 'pinned binary hash and size')
    must(metadata['schema'] == 'm31-audit-saved-poses-v1' and metadata['dataType'] == 'Float64LE' and metadata['valuesPerDrone'] == 7 and metadata['quaternionOrder'] == 'x,y,z,w' and metadata['offsetUnits'] == 'Float64 values' and metadata['positionUnits'] == 'm', 'input pose schema')
    domain_bytes, manifest_bytes = (repo / c['domainResult']).read_bytes(), (repo / c['domainManifest']).read_bytes()
    must(sha(domain_bytes) == c['domainResultSha256'] == DOMAIN_RESULT_SHA and sha(manifest_bytes) == c['domainManifestSha256'] == DOMAIN_MANIFEST_SHA, 'pinned prior domain result/manifest')
    domain, manifest = json.loads(domain_bytes), json.loads(manifest_bytes)
    check(domain['sourceCommit'] == manifest['sourceCommit'] == 'e23e053dfe31ce98163b7e0b6d1a28d849d7e9f3', 'prior domain scientific source')
    pins = {item['path']:item for item in manifest['files']}
    offsets = [[0,14000,28000,42000],[70000,84000,98000,112000],[140000,210000,280000,350000]]
    identities = [('wide',2001,1000,'heldout-2001-1000-wide-wall-priority-0.0025'),('narrow',2002,1000,'heldout-2002-1000-narrow-wall-priority-0.0025'),('wide',2001,5000,'heldout-2001-5000-wide-wall-priority-0.0025')]
    ids = [f'case-{ci}-t-{t}' for ci in range(3) for t in c['times']]
    must([s['id'] for s in r['snapshots']] == ids and [s['id'] for s in domain['snapshots']] == ids, '12 exact case-major snapshots')
    expected_files = {'started.json','result.json'} | {sid+suffix for sid in ids for suffix in ['-rotors.f64','-vehicles.f64','-receivers.ndjson','-summary.json']}
    raw_files = sorted((base / 'raw').iterdir())
    must(all(p.is_file() for p in raw_files) and {p.name for p in raw_files} == expected_files, 'complete exact 50-file raw inventory')
    raw_size = 0
    for path in raw_files:
        payload = path.read_bytes()
        raw_size += len(payload)
        REPORT['rawHashes'].append({'path':str(path.relative_to(repo)),'bytes':len(payload),'sha256':sha(payload)})
    f0, mg, arm = c['nominalRotorThrustN'], 4*c['nominalRotorThrustN'], .028
    area_p, area_o = math.pi*.023**2, math.pi*.023*.023
    nominal_formula = [power(f0,0,area_p),power(f0,0,area_o)]
    retained_nominal, nominal_sources = [None,None], [None,None]
    # Read saved scalars only, to recover both exact baseline values used by JS.
    for sid in ids:
        payload = (base / 'raw' / (sid+'-rotors.f64')).read_bytes()
        must(len(payload) % 128 == 0, 'baseline search complete rotor rows', sid)
        for ri,row in enumerate(struct.iter_unpack('<16d',payload)):
            for impl in range(2):
                if retained_nominal[impl] is None and row[impl] == 0 and row[3+impl] == f0:
                    retained_nominal[impl] = row[14+impl]
                    nominal_sources[impl] = {'snapshot':sid,'receiver':ri//4,'rotor':ri%4}
            if None not in retained_nominal:
                break
        if None not in retained_nominal:
            break
    must(None not in retained_nominal and finite(retained_nominal), 'retained zero-inflow nominal power baselines')
    check(all(close(a,b) for a,b in zip(retained_nominal,nominal_formula)), 'nominal ideal-power scalar reconstruction')
    check(gate(*retained_nominal,c['idealPowerTolerance']['absolute'],c['idealPowerTolerance']['relative']), 'nominal power cross-implementation scientific gate')
    REPORT['nominalPower'] = {'retainedPrimaryW':retained_nominal[0],'retainedIndependentW':retained_nominal[1],'formulaPrimaryW':nominal_formula[0],'formulaIndependentW':nominal_formula[1],'baselineSources':nominal_sources}
    totals = Counter()
    counts_all = [0]*8
    eligibility_table = bytes([0]+[1]*255)
    tilt_threshold = math.cos(20*math.pi/180)
    for si,saved in enumerate(r['snapshots']):
        ci,ti = divmod(si,4)
        t, sid = c['times'][ti], ids[si]
        course,seed,n,original_id = identities[ci]
        mc,ds = metadata['cases'][ci],domain['snapshots'][si]
        CURRENT = {'phase':'snapshot-integrity','snapshot':sid}
        check((mc['course'],mc['seed'],mc['count'],mc['ids'][0]) == identities[ci], 'pinned case identity')
        selected = [s for s in mc['samples'] if s['t'] == t]
        must(len(selected) == 1 and selected[0]['offsets'][0] == offsets[ci][ti], 'exact selected time and primary offset')
        offset = offsets[ci][ti]
        begin,end = offset*8,(offset+7*n)*8
        must(0 <= begin < end <= len(binary), 'selected pose byte bounds')
        pose_bytes = binary[begin:end]
        check(len(pose_bytes) == n*56 and sha(pose_bytes) == saved['inputPoseSha256'] == ds['inputPoseSha256'] and saved['binaryOffsetValues'] == ds['binaryOffsetValues'] == offset, 'selected pose bytes/hash/offset')
        check(saved['caseIndex'] == ci and saved['time'] == t and saved['count'] == n and saved['originalId'] == original_id and saved['completeReceivers'] == n, 'snapshot identities and completed coverage')
        check(saved == read(base / 'raw' / (sid+'-summary.json')), 'raw/published snapshot equality')
        check(ds['modelDomainPass'] and not ds['tiltIds'] and not ds['unitAssumptionIds'] and not ds['nearReceiverIds'], 'pinned prior implemented-domain pass')
        for i,pose in enumerate(struct.iter_unpack('<7d',pose_bytes)):
            check(finite(pose), 'saved pose finite decoding only', [sid,i])
        prior_bytes = (prior_base / 'raw' / (sid+'.ndjson')).read_bytes()
        prior_pin = pins['raw/'+sid+'.ndjson']
        must(len(prior_bytes) == prior_pin['bytes'] and sha(prior_bytes) == prior_pin['sha256'] == saved['priorRowsSha256'], 'pinned complete prior receiver rows')
        prior_rows = prior_bytes.splitlines()
        payloads = {}
        expected_names = [sid+'-'+suffix for suffix in ['rotors.f64','vehicles.f64','receivers.ndjson']]
        must([item['name'] for item in saved['files']] == expected_names, 'exact per-snapshot file order')
        for item in saved['files']:
            data = (base / 'raw' / item['name']).read_bytes()
            must(len(data) == item['bytes'] and sha(data) == item['sha256'], 'snapshot binary/metadata hash and size', [sid,item['name']])
            payloads[item['name']] = data
        rotor_bytes,vehicle_bytes,receiver_bytes = [payloads[name] for name in expected_names]
        must(len(rotor_bytes) == n*4*16*8 and len(vehicle_bytes) == n*35*8, 'complete binary row bytes')
        receiver_rows = receiver_bytes.splitlines()
        must(len(prior_rows) == len(receiver_rows) == n, 'all prior/current metadata rows')
        rotors = list(struct.iter_unpack('<16d',rotor_bytes))
        vehicles = list(struct.iter_unpack('<35d',vehicle_bytes))
        stats = {key:statistic() for key in METRICS}
        loss,roll,pitch = [],[],[]
        counts, eligible, centers, contributions, inspections, root_iterations = [0]*8,0,0,0,0,0
        axis_difference, maximum_primary, maximum_independent = 0.0,0.0,0.0
        no_contributor_rotors = zero_primary_rotors = zero_independent_rotors = 0
        for i in range(n):
            CURRENT = {'phase':'receiver-saved-evidence','snapshot':sid,'receiver':i}
            prior,row = json.loads(prior_rows[i]),json.loads(receiver_rows[i])
            must(prior['receiver'] == row['receiver'] == i, 'ordered complete receiver identities')
            packed = base64.b64decode(prior['codesDeflateBase64'],validate=True)
            inflator = zlib.decompressobj()
            codes = inflator.decompress(packed,4*n+1)
            must(len(codes) == 4*n and inflator.eof and not inflator.unconsumed_tail and not inflator.unused_data, 'complete strict prior code vector')
            digest = sha(codes)
            check(digest == prior['productionCodesSha256'] == prior['independentCodesSha256'] == row['codeSha256'] == row['priorProductionCodeSha256'] == row['priorIndependentCodeSha256'], 'current and prior full-vector digests')
            histogram = [codes.count(bytes([k])) for k in range(8)]
            must(sum(histogram) == 4*n, 'only declared code values')
            check(histogram == row['counts'] == prior['counts'], 'complete per-receiver code counts')
            check(codes[4*i:4*i+4] == b'\0'*4, 'self source code slots')
            mask = codes[0::4].translate(eligibility_table)
            check(all(codes[k::4].translate(eligibility_table) == mask for k in [1,2,3]), 'all four rotor eligibility groups')
            row_eligible = mask.count(b'\1')
            check(row_eligible == row['eligible'] == prior['eligible'] and histogram[0] == 4*(n-row_eligible), 'eligible/outside exact accounting')
            check(row['centerChecks'] == prior['oracleCentrePairs'] == n-1 and row['contributions'] == histogram[6]+histogram[7], 'per-receiver center and support accounting')
            check(not prior['tiltViolation'] and not prior['nearInvalidEvents'] and histogram[3] == 0 and finite(prior['axis']) and finite([prior['quaternionNormError']]) and 0 <= prior['quaternionNormError'] <= c['unitQuaternionTolerance'], 'retained prior domain constraints')
            counts = [a+b for a,b in zip(counts,histogram)]
            eligible += row_eligible
            centers += n-1
            contributions += histogram[6]+histogram[7]
            thrusts_p, thrusts_o = [],[]
            for k in range(4):
                CURRENT = {'phase':'rotor-saved-scalars','snapshot':sid,'receiver':i,'rotor':k}
                a = rotors[4*i+k]
                must(finite(a), 'all 16 rotor scalars finite')
                u,v,comp,f,g,x,y,alpha,beta,rp,ro,lo,hi,iterations,pp,po = a
                check(u >= 0 and v >= 0 and comp >= 0, 'scientific nonnegative inflows')
                check(0 <= f <= f0 and 0 <= g <= f0, 'scientific effective thrust bounds')
                check(gate(u,v,c['inflowTolerance']['absolute'],c['inflowTolerance']['relative']) and gate(v,comp,c['inflowTolerance']['absolute'],c['inflowTolerance']['relative']), 'scientific inflow and compensated gates')
                check(gate(f,g,c['rotorThrustToleranceN']), 'scientific rotor thrust gate')
                lane = codes[k::4]
                first6,first7 = lane.find(b'\6'),lane.find(b'\7')
                present = [pos for pos in [first6,first7] if pos >= 0]
                inspections += min(present)+1 if present else n
                if not present:
                    no_contributor_rotors += 1
                    check(u == v == comp == 0, 'scientific exact no-contributor zero inflow')
                if u == 0:
                    zero_primary_rotors += 1
                    check(f == f0 and x == 1 and alpha == 0 and rp == 0, 'scientific primary zero-inflow response')
                    check(pp == retained_nominal[0], 'same retained primary nominal power baseline')
                if v == 0:
                    zero_independent_rotors += 1
                    check(g == f0 and y == 1 and beta == 0 and ro == 0 and lo == hi == 1 and iterations == 0, 'scientific independent zero-inflow response')
                    check(po == retained_nominal[1], 'same retained independent nominal power baseline')
                check(0 <= x <= 1 and 0 <= y <= 1 and alpha >= 0 and beta >= 0, 'normalized saved root and alpha ranges')
                check(close(x,f/f0) and close(g,f0*y), 'normalized thrust scalar reconstruction')
                alpha_check = u/math.sqrt(f0/(2*1.225*math.pi*.023**2))
                beta_check = v/math.sqrt(f0/(2*1.225*area_o))
                check(close(alpha,alpha_check) and close(beta,beta_check), 'own-inflow alpha scalar reconstruction')
                residual_p,residual_o = x*x*x+alpha*x-1,y*y*y+beta*y-1
                check(close(rp,residual_p,RESIDUAL_ARITH_ABS) and close(ro,residual_o,RESIDUAL_ARITH_ABS), 'saved cubic residual scalar reconstruction')
                check(abs(rp) <= c['rootResidualTolerance'] and abs(ro) <= c['rootResidualTolerance'], 'scientific saved cubic residual gates')
                check(abs(residual_p) <= c['rootResidualTolerance'] and abs(residual_o) <= c['rootResidualTolerance'], 'scientific independently recomputed cubic residual gates')
                check(0 <= lo <= y <= hi <= 1 and hi-lo <= c['rootBracketWidthTolerance'] and iterations.is_integer() and 0 <= iterations <= 96, 'scientific independent bracket and iteration gate')
                rlo,rhi = lo*lo*lo+beta*lo-1,hi*hi*hi+beta*hi-1
                check(rlo <= RESIDUAL_ARITH_ABS and rhi >= -RESIDUAL_ARITH_ABS, 'rounded saved bracket endpoint residual consistency')
                check(close(pp,power(f,u,area_p)) and close(po,power(g,v,area_o)), 'ideal-power saved scalar reconstruction')
                for impl,pw in enumerate([pp,po]):
                    check(gate(pw,retained_nominal[impl],c['idealPowerTolerance']['absolute'],c['idealPowerTolerance']['relative']), 'scientific ideal-power gate against retained nominal')
                    check(gate(pw,nominal_formula[impl],c['idealPowerTolerance']['absolute'],c['idealPowerTolerance']['relative']), 'scientific ideal-power gate against formula nominal')
                root_iterations += int(iterations)
                maximum_primary,maximum_independent = max(maximum_primary,u),max(maximum_independent,v)
                at = {'receiver':i,'rotor':k}
                for key,value in [('inflow',abs(u-v)),('compensated',abs(v-comp)),('rotorThrust',abs(f-g)),('rootResidualPrimary',abs(rp)),('rootResidualIndependent',abs(ro)),('powerResidualPrimary',abs(pp-retained_nominal[0])),('powerResidualIndependent',abs(po-retained_nominal[1]))]:
                    add(stats[key],value,at)
                thrusts_p.append(f)
                thrusts_o.append(g)
            CURRENT = {'phase':'vehicle-saved-scalars','snapshot':sid,'receiver':i}
            b = vehicles[i]
            must(finite(b), 'all 35 vehicle scalars finite')
            total_p,mx_p,my_p = 0.0,0.0,0.0
            for f,(rx,ry) in zip(thrusts_p,[(arm,arm),(-arm,arm),(-arm,-arm),(arm,-arm)]):
                total_p += f
                mx_p += ry*f
                my_p -= rx*f
            f1,f2,f3,f4 = thrusts_o
            total_o,mx_o,my_o = f1+f2+f3+f4,arm*(f1+f2-f3-f4),arm*(-f1+f2+f3-f4)
            check(all(close(a,z) for a,z in [(b[0],total_p),(b[1],total_o),(b[2],mx_p),(b[3],my_p),(b[5],mx_o),(b[6],my_o)]), 'independent saved-rotor wrench arithmetic')
            check(b[4] == b[7] == 0, 'scientific nominal yaw zero convention')
            check(gate(b[0],b[1],c['bodyThrustToleranceN']) and all(gate(b[2+k],b[5+k],c['bodyMomentToleranceNm']) for k in range(3)), 'scientific body thrust and moment gates')
            check(close(b[20],b[0]-mg) and close(b[21],b[1]-mg), 'saved deltaT arithmetic')
            check(0 <= b[34] <= c['unitQuaternionTolerance'] and close(b[34],prior['quaternionNormError']), 'saved quaternion norm defect and prior agreement')
            check(b[30] >= tilt_threshold and b[33] >= tilt_threshold and prior['axis'][2] >= tilt_threshold, 'retained-axis tilt predicate agreement')
            for k in range(3):
                axis_difference = max(axis_difference,abs(b[28+k]-b[31+k]))
                check(gate(b[28+k],b[31+k],c['geometryAgreementTolerance']) and close(b[28+k],prior['axis'][k]), 'saved primary/independent/prior axis agreement')
                check(gate(b[8+k],b[11+k],c['worldForceToleranceN']) and gate(b[14+k],b[17+k],c['worldForceToleranceN']), 'scientific world force and force-change gates')
                check(gate(b[22+k],b[25+k],c['worldMomentToleranceNm']), 'scientific world moment gates')
                check(close(b[8+k],b[0]*b[28+k]) and close(b[11+k],b[1]*b[31+k]), 'world force relation using saved axes only')
                check(close(b[14+k],b[8+k]-mg*b[28+k]) and close(b[17+k],b[11+k]-mg*b[31+k]), 'world force-change relation using saved axes only')
                at = {'receiver':i,'component':k}
                add(stats['worldForce'],abs(b[8+k]-b[11+k]),at)
                add(stats['worldForceChange'],abs(b[14+k]-b[17+k]),at)
                add(stats['worldMoment'],abs(b[22+k]-b[25+k]),at)
            check(close(sum(b[22+k]*b[28+k] for k in range(3)),0) and close(sum(b[25+k]*b[31+k] for k in range(3)),0), 'saved world moment orthogonal to saved thrust axis')
            for key,value in [('bodyThrust',abs(b[0]-b[1])),('roll',abs(b[2]-b[5])),('pitch',abs(b[3]-b[6]))]:
                add(stats[key],value,{'receiver':i})
            loss.append(mg-b[0]);roll.append(abs(b[2]));pitch.append(abs(b[3]))
        CURRENT = {'phase':'snapshot-summary-arithmetic','snapshot':sid}
        check(counts == ds['counts'] and eligible == ds['eligiblePairs'] and sum(counts) == 4*n*n and centers == n*(n-1), 'snapshot complete prior counts and center coverage')
        check(saved['primaryField'] == {'maximumInflow':maximum_primary,'candidates':eligible,'contributions':contributions}, 'complete primary field summary')
        check(saved['independentField'] == {'maximumInflow':maximum_independent,'candidates':eligible,'contributions':contributions,'centerChecks':centers,'rotorVisits':4*eligible}, 'complete independent field summary')
        check(gate(maximum_primary,maximum_independent,c['inflowTolerance']['absolute'],c['inflowTolerance']['relative']), 'scientific maximum inflow gate')
        check(finite([saved['maxGeometryDifference']]) and axis_difference <= saved['maxGeometryDifference'] <= c['geometryAgreementTolerance'], 'retained runtime geometry maximum bounds saved-axis difference')
        check(saved['independentRootIterations'] == root_iterations, 'complete root iteration sum')
        must(set(saved['metrics']) == set(METRICS), 'complete 13-metric inventory')
        for key,stat in stats.items():
            stat['rms'] = math.sqrt(stat['sumSquares']/stat['count'])
            reported = saved['metrics'][key]
            check(reported['count'] == stat['count'] and reported['maximumAt'] == stat['maximumAt'], 'metric denominator and first maximizing index', [sid,key])
            check(close(reported['maximum'],stat['maximum'],1e-30,SUMMARY_REL) and close(reported['sumSquares'],stat['sumSquares'],1e-55,SUMMARY_REL) and close(reported['rms'],stat['rms'],1e-30,SUMMARY_REL), 'metric max/sumSquares/RMS arithmetic', [sid,key])
        distributions = {'thrustLossN':distribution(loss),'absoluteRollNm':distribution(roll),'absolutePitchNm':distribution(pitch)}
        must(set(saved['prescribedLoadDistributions']) == set(distributions), 'all prescribed-load distributions')
        for key,d in distributions.items():
            recorded = saved['prescribedLoadDistributions'][key]
            check(recorded['count'] == n and all(close(recorded[k],d[k],1e-30,SUMMARY_REL) for k in ['minimum','q50','q95','maximum']), 'all-vehicle nearest-rank distributions with zeros', [sid,key])
        check(saved['qualificationPass'] is True, 'retained completed qualification decision')
        totals.update({'snapshots':1,'poses':n,'rotors':4*n,'selectedPoseBytes':n*56,'rotorBinaryBytes':len(rotor_bytes),'vehicleBinaryBytes':len(vehicle_bytes),'metadataRows':n,'inflatedCodeBytes':4*n*n,'eligiblePairs':eligible,'centerChecks':centers,'contributionsPerImplementation':contributions,'combinedRotorVisits':8*eligible,'contributorCodeInspections':inspections,'independentRootIterations':root_iterations,'noContributorRotors':no_contributor_rotors,'zeroPrimaryRotors':zero_primary_rotors,'zeroIndependentRotors':zero_independent_rotors})
        counts_all = [a+b for a,b in zip(counts_all,counts)]
        REPORT['snapshots'].append({'id':sid,'count':n,'binaryOffsetValues':offset,'inputPoseSha256':sha(pose_bytes),'priorRowsSha256':sha(prior_bytes),'counts':counts,'eligiblePairs':eligible,'centerChecks':centers,'contributionsPerImplementation':contributions,'contributorCodeInspections':inspections,'noContributorRotors':no_contributor_rotors,'zeroPrimaryRotors':zero_primary_rotors,'zeroIndependentRotors':zero_independent_rotors,'maximumSavedAxisDifference':axis_difference,'reportedRuntimeMaximumGeometryDifference':saved['maxGeometryDifference'],'independentRootIterations':root_iterations,'metrics':stats,'prescribedLoadDistributions':distributions,'reportedQualificationPass':saved['qualificationPass']})
    CURRENT = {'phase':'whole-campaign-accounting'}
    check(totals['snapshots'] == 12 and totals['poses'] == totals['metadataRows'] == schema['vehicleRows'] == 28000 and totals['rotors'] == schema['rotorRows'] == 112000 and totals['selectedPoseBytes'] == 1568000, 'exact complete 12-snapshot coverage')
    check(totals['rotorBinaryBytes'] == schema['expectedRotorBytes'] == 14336000 and totals['vehicleBinaryBytes'] == schema['expectedVehicleBytes'] == 7840000 and totals['rotorBinaryBytes']+totals['vehicleBinaryBytes'] == schema['binaryTotalBytes'] == 22176000, 'exact complete binary coverage')
    check(totals['inflatedCodeBytes'] == sum(counts_all) == 432000000 and counts_all == [394485760,18759351,408755,0,2373850,15480749,0,491535], 'complete 432-million-byte prior vector coverage')
    check(totals['eligiblePairs'] == 9378560 and totals['centerChecks'] == r['oracleCentrePairs'] == 107972000, 'all eligible pairs and direct center checks')
    check(totals['contributionsPerImplementation'] == 491535 and totals['combinedRotorVisits'] == r['productionRotorVisits']+r['independentRotorVisits'] == 75028480 and r['productionRotorVisits'] == r['independentRotorVisits'] == 37514240, 'all support evaluations and eligible rotor visits')
    check(r['contributorCodeInspections'] == totals['contributorCodeInspections'] <= c['contributorCodeInspectionCap'] == 432000000, 'actual early-breaking saved-code inspections')
    check(r['fieldCalls'] == c['fieldCallCap'] == 24 and r['productionFieldCalls'] == r['independentFieldCalls'] == 12 and r['productionReceiverCalls'] == r['independentReceiverCalls'] == 112000 and r['productionReceiverCalls']+r['independentReceiverCalls'] == c['receiverCallCap'] == 224000, 'exact field and receiver call counts')
    check(r['integrationSteps'] == c['integrationStepCap'] == 0, 'zero integration accounting')
    check(r['oracleCentrePairs'] <= c['oracleCentrePairCap'] == 110000000 and totals['combinedRotorVisits'] <= c['rotorVisitCap'] == 864000000, 'frozen operation caps')
    check(c['rawByteCap'] == budget['rawByteCap'] == 64*1024*1024 and c['failureReserveBytes'] == 2*1024*1024 and raw_size <= c['rawByteCap']-c['failureReserveBytes'], 'raw cap and retained failure reserve')
    must(len(budget['entries']) == 1, 'one supervised scientific invocation')
    entry = budget['entries'][0]
    check(entry['completeProcess'] and entry['exitCode'] == 0 and entry['stop'] is None and budget['active'] is None and not budget['requiresFailureReview'], 'successful fully reaped scientific invocation')
    check(raw_size == entry['rawBytesAfter'], 'raw bytes match supervisor')
    check(c['wallCapSeconds'] == budget['wallCapSeconds'] == 300 and finite([entry['wallSeconds'],r['elapsedSeconds']]) and 0 < r['elapsedSeconds'] <= entry['wallSeconds'] < 300, 'scientific elapsed and fixed wall cap')
    check(finite([entry['childCPUSeconds'],entry['cumulativeChildMaxRSSPlatformUnits']]) and entry['childCPUSeconds'] >= 0 and entry['cumulativeChildMaxRSSPlatformUnits'] > 0, 'recorded CPU/RSS diagnostics without acceptance cap')
    REPORT['accounting'] = {**dict(totals),'counts':counts_all,'rawFiles':len(raw_files),'rawBytes':raw_size,'fieldCalls':r['fieldCalls'],'productionReceiverCalls':r['productionReceiverCalls'],'independentReceiverCalls':r['independentReceiverCalls'],'integrationSteps':0,'supervisorWallSeconds':entry['wallSeconds'],'driverElapsedSeconds':r['elapsedSeconds'],'scientificBudgetTerminalAtReview':budget['terminal'],'executionDiagnostics':entry}
    REPORT['outcome'] = {'snapshotsWithReportedQualificationPass':sum(s['reportedQualificationPass'] for s in REPORT['snapshots']),'noContributorRotorRecords':totals['noContributorRotors'],'nearPolicySkippedCode4Tuples':counts_all[4],'scope':'Complete retained static prescribed-load equation comparison only; earlier trajectory and temporal-reference failures remain unresolved.'}

exit_code = 0
with (RUN / 'stdout.txt').open('w') as stdout, (RUN / 'stderr.txt').open('w') as stderr:
    with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
        signal.signal(signal.SIGALRM,alarm)
        signal.setitimer(signal.ITIMER_REAL,55)
        try:
            if len(sys.argv) != 3 or sys.argv[2] != '--authorized-after-science':
                raise ValueError('Execution requires prior authorization and usage: python3 m31-force-saved-review.py REPOSITORY --authorized-after-science')
            verify(Path(sys.argv[1]).resolve())
        except BaseException as exc:
            exit_code = 1
            REPORT['exception'] = {'type':type(exc).__name__,'message':str(exc),'context':CURRENT}
            traceback.print_exc()
        finally:
            signal.setitimer(signal.ITIMER_REAL,0)
        REPORT['checkCount'] = sum(COUNTS.values())
        REPORT['checkCategories'] = dict(COUNTS)
        REPORT['failedCheckCount'] = FAILED_COUNT
        REPORT['failedChecks'] = FAILURES
        REPORT['failureListLimit'] = 300
        REPORT['passed'] = exit_code == 0 and FAILED_COUNT == 0
        if not REPORT['passed']:
            exit_code = 1
        REPORT['verificationWallSecondsBeforeOutput'] = time.perf_counter()-START
        canonical = Path('/tmp/m31-force-saved-review.json')
        REPORT['canonicalOutputPreservedIfAlreadyPresent'] = canonical.exists()
        serialized = json.dumps(REPORT,indent=2,allow_nan=False)+'\n'
        (RUN / 'review.json').write_text(serialized)
        try:
            with canonical.open('x') as handle:
                handle.write(serialized)
        except FileExistsError:
            pass
        print(json.dumps({'passed':REPORT['passed'],'checks':REPORT['checkCount'],'failedCheckCount':FAILED_COUNT,'failedChecks':FAILURES,'exception':REPORT.get('exception'),'outcome':REPORT.get('outcome'),'accounting':REPORT.get('accounting'),'invocationArchive':str(RUN)},indent=2))
runtime = {'wallSecondsThroughReviewAndLogs':time.perf_counter()-START,'authorizedWallAllowanceSeconds':60,'internalAlarmSeconds':55,'exitCode':exit_code,'passed':REPORT['passed'],'checkCount':REPORT['checkCount'],'checkerSha256':sha(SCRIPT),'invocationArchive':str(RUN)}
(RUN / 'runtime.json').write_text(json.dumps(runtime,indent=2)+'\n')
print((RUN / 'stdout.txt').read_text(),end='')
if (RUN / 'stderr.txt').stat().st_size:
    print((RUN / 'stderr.txt').read_text(),end='',file=sys.stderr)
print(json.dumps({'runtime':runtime}))
raise SystemExit(exit_code)
