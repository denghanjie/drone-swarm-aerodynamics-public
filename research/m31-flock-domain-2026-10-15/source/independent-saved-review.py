"""Saved-evidence verifier; no geometry, field, model, or integration evaluation.

Usage: python3 m31-domain-saved-review.py REPOSITORY
One invocation archives source/result/stdout/stderr/runtime in a unique /tmp
directory. Internal alarm is 55 seconds, within the authorized 60-second wall
allowance. Never import or execute the campaign's JavaScript sources.
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

START = time.perf_counter()
RUN = Path('/tmp/m31-domain-verifier-runs') / str(time.time_ns())
RUN.mkdir(parents=True, exist_ok=False)
SCRIPT = Path(__file__).read_bytes()
(RUN / 'checker.py').write_bytes(SCRIPT)
COUNTS = Counter()
FAILURES = []
CURRENT = {'phase': 'startup'}
REPORT = {
    'scope': 'Independent saved-evidence verification only; no geometry, rotations, pair distances/projections, fields, case evaluation, or integration rerun.',
    'method': {
        'script': 'm31-domain-saved-review.py',
        'scriptSha256': hashlib.sha256(SCRIPT).hexdigest(),
        'invocationArchive': str(RUN),
        'wallAllowanceSeconds': 60,
        'internalAlarmSeconds': 55,
        'vectorVerification': 'Strict base64/zlib decode of every complete 4N-byte vector; SHA-256 against both saved digests; full code histogram and four-rotor eligibility-mask checks.',
        'inputVerification': 'Pinned file hashes, exact primary offsets and byte-slice hashes; only decode existing seven-number records for finiteness, without quaternion norms or rotations.',
        'scalarVerification': 'Aggregate saved scalars and compare retained predicate signs to their saved codes; no coordinates or distances are regenerated.'
    },
    'sourceHashes': [], 'rawHashes': [], 'snapshots': [],
    'limitations': [
        'Only the production code vector is retained. Its complete inflated bytes are checked against both saved hashes; the independent vector is not regenerated.',
        'Independent axes, rotor coordinates, tilt predicates, and near-event coordinates are not retained separately. Their runtime comparisons and geometryMaximumDifference cannot be independently recomputed from saved geometry without rerunning geometry, which is prohibited.',
        'Code4 identities are fully recovered from the vectors; their geometry coordinates were intentionally omitted and are not reconstructed.',
        'The verifier aggregates saved quaternion norm errors and tilt angles; it does not recompute them from pose quaternions. Tilt booleans are checked against the retained axis-Z scalar.',
        'Closest-boundary summaries are minima of retained row minima. Their signs/labels agree with saved codes, but geometry is not reexamined to prove those were the closest predicates.',
        'Historical full trajectory streams are referenced by pinned metadata hashes and are not restored. Exact compact-file and selected-slice integrity are checked.',
        'A finite saved-time implemented-domain pass is not physical validation, a continuous-flight claim, numerical-reference acceptance, or authorization to evaluate aerodynamic fields.'
    ]
}

def check(ok, category, context=None):
    COUNTS[category] += 1
    if not ok:
        FAILURES.append({'check': category, 'context': context})

def must(ok, category, context=None):
    check(ok, category, context)
    if not ok:
        raise ValueError('Cannot continue safely: ' + category)

def read(p):
    return json.loads(p.read_text())

def sha(data):
    return hashlib.sha256(data).hexdigest()

def finite(values):
    return all(isinstance(v, (int, float)) and math.isfinite(v) for v in values)

def locations(data, code):
    needle = bytes([code])
    at = data.find(needle)
    while at >= 0:
        yield at
        at = data.find(needle, at + 1)

def alarm(signum, frame):
    raise TimeoutError('Saved-evidence verifier reached its 55-second internal wall limit')

def verify(repo):
    global CURRENT
    base = repo / 'research/m31-flock-domain-2026-10-15'
    c = read(base / 'config.json')
    r = read(base / 'results/result.json')
    freeze = read(base / 'freeze.json')
    budget = read(base / 'results/budget.json')
    source_commit = 'e23e053dfe31ce98163b7e0b6d1a28d849d7e9f3'
    REPORT['sourceCommit'] = r['sourceCommit']
    REPORT['freezeSha256'] = sha((base / 'freeze.json').read_bytes())
    check(r['sourceCommit'] == source_commit, 'frozen source commit')
    check(r == read(base / 'raw/result.json') and r['config'] == c, 'published/raw/config equality')
    started = read(base / 'raw/started.json')
    check(started['sourceCommit'] == source_commit and started['config'] == c and started['aerodynamicFieldCalls'] == started['integrationSteps'] == 0, 'started source/config/zero execution counters')
    check(r['status'] == 'complete saved-flock model-domain audit', 'complete result status')
    check(c['times'] == [0, 20, 30, 60] and c['caseIndices'] == [0, 1, 2] and c['variantIndex'] == 0 and c['expectedCounts'] == [1000, 1000, 5000], 'frozen complete selection')
    check(c['inputCommit'] == '07e5165fa56f2f23bab24562b278dda1c82ed05e' and c['historicalBase'] == 'c591ce2b195fa01b895d4ba881a44a4b92fdd703', 'pinned historical provenance')
    for item in freeze['files']:
        CURRENT = {'phase': 'frozen-file', 'path': item['path']}
        data = (repo / item['path']).read_bytes()
        matched = len(data) == item['bytes'] and sha(data) == item['sha256']
        check(matched, 'frozen file hash/bytes', item['path'])
        REPORT['sourceHashes'].append({'path': item['path'], 'bytes': len(data), 'sha256': sha(data), 'matches': matched})
    CURRENT = {'phase': 'pinned-inputs'}
    meta_bytes = (repo / c['inputMetadata']).read_bytes()
    binary = (repo / c['inputBinary']).read_bytes()
    meta = json.loads(meta_bytes)
    must(sha(meta_bytes) == c['expectedMetadataSha256'] == r['inputMetadataSha256'] == 'f69cae28818dd0802863b512af96a448ffcd3aa7aa8824f528b4ed59032d613c', 'pinned metadata hash')
    must(sha(binary) == c['expectedBinarySha256'] == meta['binarySha256'] == r['inputBinarySha256'] == 'c9918697fc61576a9c0454cda354a8d66f42b0b6e21e082cdbf12054b372c927', 'pinned binary hash')
    must(len(binary) == c['expectedBinaryBytes'] == meta['binaryBytes'] == 3360000, 'pinned binary size')
    check(meta['schema'] == 'm31-audit-saved-poses-v1' and meta['dataType'] == 'Float64LE' and meta['valuesPerDrone'] == 7 and meta['quaternionOrder'] == 'x,y,z,w' and meta['offsetUnits'] == 'Float64 values' and meta['positionUnits'] == 'm', 'input layout metadata')
    offset_table = [[0, 14000, 28000, 42000], [70000, 84000, 98000, 112000], [140000, 210000, 280000, 350000]]
    identities = [('wide', 2001, 1000, 'heldout-2001-1000-wide-wall-priority-0.0025'), ('narrow', 2002, 1000, 'heldout-2002-1000-narrow-wall-priority-0.0025'), ('wide', 2001, 5000, 'heldout-2001-5000-wide-wall-priority-0.0025')]
    expected_ids = [f'case-{ci}-t-{t}' for ci in range(3) for t in c['times']]
    must([s['id'] for s in r['snapshots']] == expected_ids, 'exact 12 case-major snapshots')
    expected_files = {'started.json', 'result.json'} | {sid + suffix for sid in expected_ids for suffix in ['.ndjson', '-summary.json']}
    raw_files = sorted((base / 'raw').iterdir())
    check({p.name for p in raw_files} == expected_files, 'complete raw inventory')
    raw_size = 0
    for p in raw_files:
        data = p.read_bytes()
        raw_size += len(data)
        REPORT['rawHashes'].append({'path': str(p.relative_to(repo)), 'bytes': len(data), 'sha256': sha(data)})
    total_counts = [0] * 8
    total_poses = total_center_checks = total_rotor_classifications = 0
    total_slice_bytes = total_inflated_bytes = total_eligible = 0
    tilt_threshold = math.cos(20 * math.pi / 180)
    eligibility_table = bytes([0] + [1] * 255)
    allowed_labels = {'centre-radius', 'down-zero', 'down-cutoff', 'near-downstream', 'near-radius', 'radial-cutoff', 'axis-projection'}
    down_min = 2.5 * (2 * math.sqrt(2) * .028)
    for si, saved in enumerate(r['snapshots']):
        ci, ti = divmod(si, 4)
        t = c['times'][ti]
        sid = expected_ids[si]
        mc = meta['cases'][ci]
        course, seed, n, original_id = identities[ci]
        CURRENT = {'phase': 'snapshot-integrity', 'snapshot': sid}
        check((mc['course'], mc['seed'], mc['count'], mc['ids'][0]) == identities[ci], 'pinned case identity', sid)
        selected = [s for s in mc['samples'] if s['t'] == t]
        must(len(selected) == 1, 'unique exact saved time', sid)
        offset = selected[0]['offsets'][0]
        must(offset == offset_table[ci][ti], 'pinned primary value offset', sid)
        length = n * 7 * 8
        begin, end = offset * 8, (offset + n * 7) * 8
        must(0 <= begin < end <= len(binary) and end - begin == length, 'selected slice bounds/length', sid)
        payload = binary[begin:end]
        check(saved['inputPoseSha256'] == sha(payload) and saved['inputPoseBytes'] == length and saved['binaryOffsetValues'] == offset, 'saved pose slice hash/bytes/offset', sid)
        check(saved['caseIndex'] == ci and saved['time'] == t and saved['count'] == n and saved['course'] == course and saved['seed'] == seed and saved['originalId'] == original_id, 'snapshot provenance', sid)
        check(saved == read(base / 'raw' / (sid + '-summary.json')), 'raw/published snapshot equality', sid)
        decoded_count = 0
        for vi, pose in enumerate(struct.iter_unpack('<7d', payload)):
            check(finite(pose), 'existing pose finite decoding only', [sid, vi])
            decoded_count += 1
        check(decoded_count == n, 'complete pose records', sid)
        total_poses += n
        total_slice_bytes += length
        counts = [0] * 8
        tilt_ids, unit_ids, near_receivers, skipped_receivers = [], [], [], []
        near_sources, skipped_sources = set(), set()
        max_tilt = max_norm = 0.0
        minimum = {'margin': None, 'receiver': None, 'event': None}
        min_value = math.inf
        near_boundaries = eligible_pairs = snapshot_centers = invalid_tuples = skipped_tuples = 0
        receiver_count = 0
        with (base / 'raw' / (sid + '.ndjson')).open() as handle:
            for i, line in enumerate(handle):
                CURRENT = {'phase': 'saved-receiver-vector', 'snapshot': sid, 'receiver': i}
                row = json.loads(line)
                must(i < n and row['receiver'] == i, 'complete ordered receiver', [sid, i])
                packed = base64.b64decode(row['codesDeflateBase64'], validate=True)
                inflator = zlib.decompressobj()
                codes = inflator.decompress(packed, 4 * n + 1)
                must(len(codes) == 4 * n and inflator.eof and not inflator.unconsumed_tail and not inflator.unused_data, 'complete exact-length zlib vector', [sid, i])
                digest = sha(codes)
                check(digest == row['productionCodesSha256'] == row['independentCodesSha256'], 'both retained full-vector hashes', [sid, i])
                histogram = [codes.count(bytes([code])) for code in range(8)]
                must(sum(histogram) == len(codes), 'only declared codes zero through seven', [sid, i])
                check(histogram == row['counts'], 'exact per-receiver code counts', [sid, i])
                check(codes[4*i:4*i+4] == b'\x00' * 4, 'self rotor entries are zero', [sid, i])
                mask = codes[0::4].translate(eligibility_table)
                check(all(codes[k::4].translate(eligibility_table) == mask for k in [1, 2, 3]), 'complete four-rotor source eligibility groups', [sid, i])
                eligible = mask.count(b'\x01')
                check(eligible == row['eligible'] and histogram[0] == 4 * (n - eligible) and sum(histogram[1:]) == 4 * eligible, 'eligible/outside accounting', [sid, i])
                check(row['oracleCentrePairs'] == n - 1, 'every independent nonself center accounted', [sid, i])
                snapshot_centers += row['oracleCentrePairs']
                eligible_pairs += eligible
                total_rotor_classifications += 8 * eligible
                total_inflated_bytes += len(codes)
                for k in range(8):
                    counts[k] += histogram[k]
                invalid_positions = list(locations(codes, 3))
                identities_saved = [(e['source'], e['rotor'], e['code']) for e in row['nearInvalidEvents']]
                check(identities_saved == [(pos // 4, pos % 4, 3) for pos in invalid_positions], 'all ordered near-invalid identities', [sid, i])
                check(len(invalid_positions) == histogram[3], 'near-invalid event count', [sid, i])
                if invalid_positions:
                    near_receivers.append(i)
                for pos in invalid_positions:
                    near_sources.add(pos // 4)
                for e in row['nearInvalidEvents']:
                    check(finite([e['down'], e['radial']]) and 0 < e['down'] < down_min and 0 <= e['radial'] < .15, 'saved near-invalid scalar inequalities', [sid, i, e['source'], e['rotor']])
                if histogram[4]:
                    skipped_receivers.append(i)
                found_skipped = 0
                for pos in locations(codes, 4):
                    skipped_sources.add(pos // 4)
                    found_skipped += 1
                check(found_skipped == histogram[4], 'all near-skipped vector identities recoverable', [sid, i])
                invalid_tuples += len(invalid_positions)
                skipped_tuples += found_skipped
                check(len(row['axis']) == 3 and finite(row['axis']), 'saved axis finite', [sid, i])
                check(row['tiltViolation'] == (row['axis'][2] < tilt_threshold), 'tilt predicate from saved axis only', [sid, i])
                check(finite([row['tiltDegrees'], row['quaternionNormError']]) and 0 <= row['tiltDegrees'] <= 180 and row['quaternionNormError'] >= 0, 'saved tilt/norm scalar range', [sid, i])
                if row['tiltViolation']:
                    tilt_ids.append(i)
                if row['quaternionNormError'] > c['unitQuaternionTolerance']:
                    unit_ids.append(i)
                max_tilt = max(max_tilt, row['tiltDegrees'])
                max_norm = max(max_norm, row['quaternionNormError'])
                boundary = row['minimumBoundary']
                if boundary['margin'] is None:
                    check(boundary['event'] is None and eligible == 0, 'null boundary means no inspected pair', [sid, i])
                else:
                    gap, event = boundary['margin'], boundary['event']
                    must(event is not None and event['label'] in allowed_labels and 0 <= event['source'] < n and event['source'] != i, 'boundary identity and label', [sid, i])
                    check(finite([gap, event['signed']]) and gap == abs(event['signed']), 'boundary absolute/sign arithmetic', [sid, i])
                    source = event['source']
                    rotor = event['rotor']
                    label = event['label']
                    signed = event['signed']
                    if label == 'centre-radius':
                        check(rotor is None and mask[source] == 1 and signed < 0, 'saved center-boundary predicate identity/sign', [sid, i])
                    else:
                        must(isinstance(rotor, int) and 0 <= rotor < 4, 'boundary rotor identity', [sid, i])
                        code = codes[4 * source + rotor]
                        conditions = {
                            'down-zero': 1 <= code <= 7 and ((signed <= 0) == (code == 1)),
                            'down-cutoff': 1 <= code <= 7 and ((signed >= 0) == (code == 2)),
                            'near-downstream': 3 <= code <= 7 and ((signed < 0) == (code in [3, 4])),
                            'near-radius': code in [3, 4] and ((signed < 0) == (code == 3)),
                            'radial-cutoff': code in [5, 6, 7] and ((signed >= 0) == (code == 5)),
                            'axis-projection': code in [6, 7] and ((signed <= 0) == (code == 6))
                        }
                        check(conditions[label], 'saved boundary branch reached and sign consistent', [sid, i, label, code])
                    if gap < min_value:
                        min_value = gap
                        minimum = {'margin': gap, 'event': event, 'receiver': i}
                    if gap <= c['boundaryReportingTolerance']:
                        near_boundaries += 1
                receiver_count += 1
        must(receiver_count == n, 'all receiver rows retained', sid)
        check(sum(counts) == 4 * n * n and counts[0] >= 4 * n, 'snapshot vector coverage including self', sid)
        check(saved['counts'] == counts and saved['selfRotorEntries'] == 4 * n and saved['outsideCenterRotorEntries'] == counts[0] - 4 * n and saved['eligiblePairs'] == eligible_pairs, 'snapshot counts/self/outside/eligible exact', sid)
        check(saved['tiltIds'] == tilt_ids and saved['unitAssumptionIds'] == unit_ids and saved['nearReceiverIds'] == near_receivers and saved['nearSourceIds'] == sorted(near_sources) and saved['skippedReceiverIds'] == skipped_receivers, 'all source/receiver/tilt/unit identity sets', sid)
        check(saved['maximumTiltDegrees'] == max_tilt and saved['maximumQuaternionNormError'] == max_norm and saved['nearBoundaryReceivers'] == near_boundaries and saved['minimumBoundary'] == minimum, 'saved scalar extrema/boundary aggregation', sid)
        check(math.isfinite(saved['geometryMaximumDifference']) and 0 <= saved['geometryMaximumDifference'] <= c['geometryAgreementTolerance'], 'reported runtime geometry discrepancy within frozen tolerance', sid)
        domain_pass = not tilt_ids and not near_receivers and not unit_ids
        check(saved['modelDomainPass'] == domain_pass, 'implemented-domain decision from complete retained evidence', sid)
        check(snapshot_centers == n * (n - 1), 'snapshot independent center-count arithmetic', sid)
        total_center_checks += snapshot_centers
        total_eligible += eligible_pairs
        total_counts = [a + b for a, b in zip(total_counts, counts)]
        REPORT['snapshots'].append({
            'id': sid, 'caseIndex': ci, 'time': t, 'count': n,
            'inputPoseBytes': length, 'inputPoseSha256': sha(payload), 'binaryOffsetValues': offset,
            'counts': counts, 'selfRotorEntries': 4 * n, 'outsideCenterRotorEntries': counts[0] - 4 * n,
            'eligiblePairs': eligible_pairs, 'oracleCentrePairs': snapshot_centers,
            'nearInvalidTuples': invalid_tuples, 'nearSkippedTuples': skipped_tuples,
            'nearReceiverIds': near_receivers, 'nearSourceIds': sorted(near_sources),
            'skippedReceiverIds': skipped_receivers, 'skippedSourceIds': sorted(skipped_sources),
            'tiltIds': tilt_ids, 'unitAssumptionIds': unit_ids,
            'maximumTiltDegrees': max_tilt, 'maximumQuaternionNormError': max_norm,
            'reportedGeometryMaximumDifference': saved['geometryMaximumDifference'],
            'nearBoundaryReceivers': near_boundaries, 'minimumBoundary': minimum,
            'modelDomainPass': domain_pass
        })
    check(total_poses == 28000 and len(REPORT['snapshots']) == 12 and total_slice_bytes == 1568000, 'exact 12 snapshots/28000 poses/selected bytes')
    check(total_center_checks == r['oracleCentrePairs'] == 107972000, 'all independent center checks')
    check(total_rotor_classifications == r['rotorClassifications'] == 8 * total_eligible == 75028480, 'combined eligible rotor classification accounting')
    check(total_inflated_bytes == sum(total_counts) == 432000000 and total_counts[0] - 4 * total_poses + sum(total_counts[1:]) == 4 * total_center_checks, 'complete inflated code coverage and nonself split')
    check(r['aerodynamicFieldCalls'] == r['integrationSteps'] == c['aerodynamicFieldCallCap'] == c['integrationStepCap'] == 0, 'zero field/integration saved accounting')
    check(c['oracleCentrePairCap'] == 110000000 and total_center_checks <= c['oracleCentrePairCap'] and c['rotorClassificationCap'] == 864000000 and total_rotor_classifications <= c['rotorClassificationCap'], 'frozen operation caps')
    check(c['rawByteCap'] == budget['rawByteCap'] == 64 * 1024 * 1024 and c['failureReserveBytes'] == 1024 * 1024 and raw_size < c['rawByteCap'] - c['failureReserveBytes'], 'raw cap and failure reserve')
    check(len(budget['entries']) == 1 and budget['entries'][0]['completeProcess'] and budget['entries'][0]['exitCode'] == 0 and budget['entries'][0]['stop'] is None and budget['active'] is None and not budget['requiresFailureReview'], 'single completed supervised invocation')
    entry = budget['entries'][0]
    check(raw_size == entry['rawBytesAfter'] == 40076924, 'raw bytes exact')
    check(c['wallCapSeconds'] == budget['wallCapSeconds'] == 300 and 0 < entry['wallSeconds'] < c['wallCapSeconds'] and entry['wallSeconds'] == 12.109875667, 'supervised elapsed/cap')
    REPORT['accounting'] = {'snapshots': len(REPORT['snapshots']), 'savedPoses': total_poses, 'selectedPoseBytes': total_slice_bytes, 'inflatedCodeBytes': total_inflated_bytes, 'rawFiles': len(raw_files), 'rawBytes': raw_size, 'oracleCentrePairs': total_center_checks, 'combinedEligibleRotorClassifications': total_rotor_classifications, 'eligibleOrderedPairs': total_eligible, 'selfRotorEntries': 4 * total_poses, 'outsideCenterRotorEntries': total_counts[0] - 4 * total_poses, 'counts': total_counts, 'aerodynamicFieldCalls': 0, 'integrationSteps': 0, 'supervisorWallSeconds': entry['wallSeconds'], 'driverElapsedSeconds': r['elapsedSeconds'], 'budgetTerminalAtReview': budget['terminal']}
    REPORT['outcome'] = {'modelDomainPassingSnapshots': sum(s['modelDomainPass'] for s in REPORT['snapshots']), 'nearInvalidRotorSourceTuples': total_counts[3], 'nearSkippedRotorSourceTuples': total_counts[4], 'tiltViolationPoseRecords': sum(len(s['tiltIds']) for s in REPORT['snapshots']), 'unitAssumptionViolationPoseRecords': sum(len(s['unitAssumptionIds']) for s in REPORT['snapshots']), 'scope': 'Exact saved primary snapshots, all saved vehicles; no continuous-time or physical claim.'}

exit_code = 0
with (RUN / 'stdout.txt').open('w') as stdout, (RUN / 'stderr.txt').open('w') as stderr:
    with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
        signal.signal(signal.SIGALRM, alarm)
        signal.setitimer(signal.ITIMER_REAL, 55)
        try:
            if len(sys.argv) != 2:
                raise ValueError('Usage: python3 m31-domain-saved-review.py REPOSITORY')
            verify(Path(sys.argv[1]).resolve())
        except BaseException as exc:
            exit_code = 1
            REPORT['exception'] = {'type': type(exc).__name__, 'message': str(exc), 'context': CURRENT}
            traceback.print_exc()
        finally:
            signal.setitimer(signal.ITIMER_REAL, 0)
        REPORT['checkCount'] = sum(COUNTS.values())
        REPORT['checkCategories'] = dict(COUNTS)
        REPORT['failedChecks'] = FAILURES
        REPORT['passed'] = exit_code == 0 and not FAILURES
        if not REPORT['passed']:
            exit_code = 1
        REPORT['verificationWallSecondsBeforeOutput'] = time.perf_counter() - START
        serialized = json.dumps(REPORT, indent=2, allow_nan=False) + '\n'
        (RUN / 'review.json').write_text(serialized)
        canonical = Path('/tmp/m31-domain-saved-review.json')
        try:
            with canonical.open('x') as handle:
                handle.write(serialized)
        except FileExistsError:
            REPORT['canonicalOutputNote'] = 'Existing canonical review was preserved; this invocation result is in its unique archive.'
        print(json.dumps({'passed': REPORT['passed'], 'checks': REPORT['checkCount'], 'failedChecks': FAILURES, 'exception': REPORT.get('exception'), 'outcome': REPORT.get('outcome'), 'accounting': REPORT.get('accounting'), 'invocationArchive': str(RUN)}, indent=2))
runtime = {'wallSecondsThroughReviewAndLogs': time.perf_counter() - START, 'authorizedWallAllowanceSeconds': 60, 'internalAlarmSeconds': 55, 'exitCode': exit_code, 'passed': REPORT['passed'], 'checkCount': REPORT['checkCount'], 'checkerSha256': sha(SCRIPT), 'invocationArchive': str(RUN)}
(RUN / 'runtime.json').write_text(json.dumps(runtime, indent=2) + '\n')
print((RUN / 'stdout.txt').read_text(), end='')
if (RUN / 'stderr.txt').stat().st_size:
    print((RUN / 'stderr.txt').read_text(), end='', file=sys.stderr)
print(json.dumps({'runtime': runtime}))
raise SystemExit(exit_code)
