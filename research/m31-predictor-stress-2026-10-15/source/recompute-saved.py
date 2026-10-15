"""Portable saved-record verifier: python3 m31-predictor-recompute.py REPOSITORY.

Reads retained files only. Does not import or evaluate the field, receiver, cases,
dynamics, or benchmark. Every invocation archives its checker and output under
/tmp/m31-predictor-verifier-runs before updating /tmp/m31-predictor-review.json.
"""
import hashlib
import json
import math
import statistics
import sys
import time
from collections import Counter
from pathlib import Path

START = time.perf_counter()
if len(sys.argv) != 2:
    raise SystemExit('Usage: python3 m31-predictor-recompute.py REPOSITORY')
REPO = Path(sys.argv[1]).resolve()
BASE = REPO / 'research/m31-predictor-stress-2026-10-15'
OUT = Path('/tmp/m31-predictor-review.json')
RUN = Path('/tmp/m31-predictor-verifier-runs') / str(time.time_ns())
RUN.mkdir(parents=True)
SCRIPT = Path(__file__).read_bytes()
(RUN / 'checker.py').write_bytes(SCRIPT)
if OUT.exists():
    (RUN / 'prior-review-preserved.json').write_bytes(OUT.read_bytes())

def read(path):
    return json.loads(path.read_text())

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

C = read(BASE / 'config.json')
R = read(BASE / 'results/result.json')
F = read(BASE / 'freeze.json')
B = read(BASE / 'results/budget.json')
categories = Counter()
failures = []

def check(ok, category, context=None):
    categories[category] += 1
    if not ok:
        failures.append({'check': category, 'context': context})

def near(x, y):
    return math.isclose(x, y, rel_tol=3e-14, abs_tol=1e-27)

def finite(values):
    return all(isinstance(x, (int, float)) and math.isfinite(x) for x in values)

review = {
    'scope': 'Independent saved-record arithmetic verification only; no field, receiver, case/pose, dynamics, refinement, timing, or experiment rerun.',
    'method': {
        'script': 'm31-predictor-recompute.py',
        'scriptSha256': hashlib.sha256(SCRIPT).hexdigest(),
        'invocationArchive': str(RUN),
        'prediction': 'Exact binary64 equality, matching source ratio-first arithmetic; only saved actual refresh winds enter history.',
        'rms': 'Event-split squared-error trapezoids; independent math.fsum accumulation plus source-order sequential sum cross-check.',
        'oracle': 'Direct comparison of every saved all-vehicle production/independent rotor wind and saved receiver0 loads.',
        'timing': 'Saved timing records only; exact primary-load checksum, call counts, order, min/median/max.',
        'comparisonScope': 'Matched hold5 suite rule is prospective. Hold2.5 comparisons and source-pitch startup decomposition are descriptive saved-record checks.'
    },
    'sourceCommit': R['sourceCommit'], 'sourceHashes': [], 'rawHashes': [],
    'cases': [], 'samplingFailures': [], 'targetExceedances': [],
    'predictorTargetExceedanceRecords': [], 'predictorVsHold2p5ms': [],
    'metricDiscrepancy': {'peak': 0.0, 'rmsFsum': 0.0, 'rmsSequential': 0.0}
}
expected_commit = '661bb14c99521ef2b1d3350600e202b4fb44d5b9'
check(R['sourceCommit'] == expected_commit, 'source commit')
S = read(BASE / 'raw/started.json')
check(S['sourceCommit'] == expected_commit and S['config'] == C, 'started source/config')
check(R == read(BASE / 'raw/result.json') and R['config'] == C, 'published/raw/config equality')
check(C['primaryStride'] == 2 and C['fineStride'] == 1 and C['finalTick'] == 4000, 'fixed grids')
check(C['cases'] == [s['id'] for s in R['cases']] and len(C['cases']) == 6, 'all six case order')
check(C['variants'] == ['instant', 'hold-10ms', 'hold-5ms', 'hold-2.5ms', 'predict-5ms'], 'fixed method order')
for item in F['files']:
    p = REPO / item['path']
    h = sha(p)
    matched = h == item['sha256'] and p.stat().st_size == item['bytes']
    check(matched, 'frozen file', item['path'])
    review['sourceHashes'].append({'path': item['path'], 'sha256': h, 'bytes': p.stat().st_size, 'matches': matched})
raw_files = sorted((BASE / 'raw').iterdir())
expected_names = {'started.json', 'result.json'}
expected_names.update(cid + suffix for cid in C['cases'] for suffix in ['.ndjson', '-accuracy.json'])
expected_names.update(f'timing-{p}-{ci}-{j}.json' for p in range(6) for ci in range(6) for j in range(5))
check({p.name for p in raw_files} == expected_names, 'complete raw file inventory')
for p in raw_files:
    review['rawHashes'].append({'path': str(p.relative_to(REPO)), 'bytes': p.stat().st_size, 'sha256': sha(p)})
weight = .027 * 9.81
motor_distance = 2 * math.sqrt(2) * .028
budgets = [C['forceBudgetMgFraction'] * weight] + [C['momentBudgetMgDFraction'] * weight * motor_distance] * 2
check(budgets == R['budgets'], 'numerical target arithmetic')
duration = C['finalTick'] * C['tickSeconds']
observables = ['thrust', 'roll', 'pitch']
checksums = {}
refresh_counts = {}
science_fields = 0
oracle_fields = 0
oracle_scalar_count = 0
windows = {
    'cold-start-inflow': [(0, 20), (20, 40)],
    'smooth-fast-reversal': [(960, 1040), (1960, 2040), (2960, 3040)]
}
source_pitch_detail = None

for ci, cid in enumerate(C['cases']):
    saved = R['cases'][ci]
    accuracy = read(BASE / 'raw' / (cid + '-accuracy.json'))
    check(accuracy == {k: v for k, v in saved.items() if k != 'timingSummary'}, 'accuracy/result equality', cid)
    with (BASE / 'raw' / (cid + '.ndjson')).open() as handle:
        rows = [json.loads(line) for line in handle]
    check([r['tick'] for r in rows] == list(range(C['finalTick'] + 1)), 'complete ordered fine ticks', cid)
    vehicle_count = [2, 2, 2, 2, 3, 4][ci]
    oracle_max = {'wind': 0.0, 'loads': [0.0] * 3}
    inflow_range = [math.inf, -math.inf]
    for row in rows:
        tick = row['tick']
        ctx = [cid, tick]
        check(len(row['states']) == vehicle_count and all(len(s) == 17 and finite(s) for s in row['states']), 'saved state shape/finiteness', ctx)
        check(all(s[13:] == [weight / 4] * 4 for s in row['states']), 'saved constant nominal thrust', ctx)
        check([v['id'] for v in row['values']] == C['variants'], 'row variant order', ctx)
        check(len(row['referenceAllWinds']) == len(row['independentAllWinds']) == vehicle_count, 'all-vehicle oracle shape', ctx)
        for vi in range(vehicle_count):
            a, b = row['referenceAllWinds'][vi], row['independentAllWinds'][vi]
            check(len(a) == len(b) == 4 and finite(a + b), 'oracle rotor shape/finiteness', ctx + [vi])
            for k, (x, y) in enumerate(zip(a, b)):
                delta = abs(x - y)
                oracle_max['wind'] = max(oracle_max['wind'], delta)
                oracle_scalar_count += 1
                check(delta <= C['arithmeticAgreementTolerance'], 'every saved oracle wind', ctx + [vi, k, delta])
        instant = row['values'][0]
        check(instant['winds'] == row['referenceAllWinds'][0], 'instant/reference linkage', ctx)
        for k, (x, y) in enumerate(zip(instant['loads'], row['independentReceiverLoads'])):
            delta = abs(x - y)
            oracle_max['loads'][k] = max(oracle_max['loads'][k], delta)
            oracle_scalar_count += 1
            check(math.isfinite(x) and math.isfinite(y) and delta <= C['arithmeticAgreementTolerance'], 'every saved oracle receiver load', ctx + [k, delta])
        inflow_range[0] = min(inflow_range[0], *instant['winds'])
        inflow_range[1] = max(inflow_range[1], *instant['winds'])
        for value in row['values']:
            for side in [value] + ([value['left']] if value['left'] is not None else []):
                check(len(side['winds']) == 4 and len(side['loads']) == 3 and finite(side['winds'] + side['loads']) and all(w >= 0 for w in side['winds']), 'treatment and left finite/nonnegative wind', ctx + [value['id']])
    check(oracle_max == saved['oracleMaximumDifference'], 'oracle maxima', cid)
    check(inflow_range == saved['receiverInflowRange'] and saved['vehicleCount'] == vehicle_count, 'inflow range and vehicle count', cid)
    case_review = {'id': cid, 'oracleMaximumDifference': oracle_max, 'receiverInflowRange': inflow_range, 'metrics': [], 'reportingWindows': [], 'targetPassingMethods': []}
    checksums[cid] = {}
    refresh_counts[cid] = {}
    for mi, mid in enumerate(C['variants']):
        saved_metric = saved['metrics'][mi]
        check(saved_metric['id'] == mid, 'metric method order', [cid, mid])
        events = [r['tick'] for r in rows if r['values'][mi]['refresh']]
        period = 1 if mid == 'instant' else C['periodTicks'][mid]
        check(events == list(range(0, C['finalTick'] + 1, period)), 'exact refresh schedule', [cid, mid])
        refresh_counts[cid][mid] = len(events)
        if mid != 'instant':
            check(all(t % C['primaryStride'] == 0 for t in events), 'refreshes on both grids', [cid, mid])
        last = prior = None
        for row in rows:
            tick = row['tick']
            v = row['values'][mi]
            ref = row['values'][0]
            ctx = [cid, mid, tick]
            if mid == 'instant':
                check(v['left'] is None and v['refresh'], 'instant refresh/no left', ctx)
                continue
            check((v['left'] is not None) == (v['refresh'] and tick > 0), 'left-limit event accounting', ctx)
            if v['left'] is not None:
                latest = rows[last]['values'][0]['winds']
                predicted = latest if mid != 'predict-5ms' or prior is None else [max(0, u + (u - p) * ((tick - last) / (last - prior))) for u, p in zip(latest, rows[prior]['values'][0]['winds'])]
                check(predicted == v['left']['winds'], 'exact causal old left wind', ctx)
                if mid != 'predict-5ms' or prior is None:
                    check(v['left']['loads'] == rows[last]['values'][0]['loads'], 'old hold left load', ctx)
            if v['refresh']:
                check(v['winds'] == ref['winds'] and v['loads'] == ref['loads'], 'actual refresh matches reference', ctx)
                prior, last = last, tick
            latest = rows[last]['values'][0]['winds']
            predicted = latest if mid != 'predict-5ms' or prior is None else [max(0, u + (u - p) * ((tick - last) / (last - prior))) for u, p in zip(latest, rows[prior]['values'][0]['winds'])]
            check(predicted == v['winds'], 'exact causal sample wind', ctx)
            if mid != 'predict-5ms' or prior is None:
                check(v['loads'] == rows[last]['values'][0]['loads'], 'constant held or startup load', ctx)
        comp = {'id': mid}
        for grid_name, stride in [('primary', C['primaryStride']), ('refined', C['fineStride'])]:
            summary = []
            for k, observable in enumerate(observables):
                peak = 0.0
                worst_tick, worst_side = 0, 'sample'
                areas = []
                integral = 0.0
                exceedances = 0
                for tick in range(0, C['finalTick'] + 1, stride):
                    row = rows[tick]
                    v = row['values'][mi]
                    reference = row['values'][0]['loads'][k]
                    sides = [('sample', v)] + ([('left', v['left'])] if v['left'] is not None else [])
                    for side, data in sides:
                        err = data['loads'][k] - reference
                        if abs(err) > peak:
                            peak, worst_tick, worst_side = abs(err), tick, side
                        if abs(err) > budgets[k] + C['arithmeticAgreementTolerance']:
                            exceedances += 1
                            if grid_name == 'refined' and mid == 'predict-5ms':
                                review['predictorTargetExceedanceRecords'].append({'case': cid, 'tick': tick, 'timeSeconds': tick * C['tickSeconds'], 'side': side, 'observable': observable, 'signedError': err, 'budget': budgets[k]})
                    if tick:
                        old = rows[tick - stride]
                        e0 = old['values'][mi]['loads'][k] - old['values'][0]['loads'][k]
                        e1 = (v['left'] if v['left'] is not None else v)['loads'][k] - reference
                        area = (e0 * e0 + e1 * e1) * .5 * stride * C['tickSeconds']
                        integral += area
                        areas.append(area)
                rms = math.sqrt(math.fsum(areas) / duration)
                sequential_rms = math.sqrt(integral / duration)
                m = {'observable': observable, 'peak': peak, 'rms': rms, 'worstTick': worst_tick, 'worstSide': worst_side, 'budget': budgets[k], 'peakWithinBudget': peak <= budgets[k] + C['arithmeticAgreementTolerance'], 'queryExceedances': exceedances}
                old = saved_metric[grid_name][k]
                check({key: val for key, val in m.items() if key != 'rms'} == {key: val for key, val in old.items() if key != 'rms'}, 'exact peak/location/target/exceedance metrics', [cid, mid, grid_name, observable])
                check(sequential_rms == old['rms'], 'source-order RMS exact', [cid, mid, grid_name, observable])
                check(near(rms, old['rms']), 'independent fsum RMS agreement', [cid, mid, grid_name, observable])
                for key, delta in [('peak', abs(peak - old['peak'])), ('rmsFsum', abs(rms - old['rms'])), ('rmsSequential', abs(sequential_rms - old['rms']))]:
                    review['metricDiscrepancy'][key] = max(review['metricDiscrepancy'][key], delta)
                if grid_name == 'refined' and not m['peakWithinBudget']:
                    review['targetExceedances'].append({'case': cid, 'method': mid, **m})
                summary.append(m)
            comp[grid_name] = summary
        comp['sampling'] = []
        for k, observable in enumerate(observables):
            floor = C['momentSamplingFloor'] if k else C['forceSamplingFloor']
            item = {'observable': observable}
            for metric in ['peak', 'rms']:
                p, q = comp['primary'][k][metric], comp['refined'][k][metric]
                difference = abs(p - q)
                threshold = max(C['samplingRelativeTolerance'] * q, floor)
                item[metric + 'Difference'] = difference
                item[metric + 'Stable'] = difference <= threshold
                check(item[metric + 'Stable'] == saved_metric['sampling'][k][metric + 'Stable'], 'sampling classification', [cid, mid, observable, metric])
                if not item[metric + 'Stable']:
                    review['samplingFailures'].append({'case': cid, 'method': mid, 'observable': observable, 'metric': metric, 'difference': difference, 'threshold': threshold})
            comp['sampling'].append(item)
        if all(m['peakWithinBudget'] for m in comp['refined']) and all(m['peakStable'] for m in comp['sampling']):
            case_review['targetPassingMethods'].append(mid)
        case_review['metrics'].append(comp)
        checksum = 0.0
        for tick in range(0, C['finalTick'] + 1, C['primaryStride']):
            x = rows[tick]['values'][mi]['loads']
            checksum += (x[0] + x[1]) + x[2]
        checksums[cid][mid] = checksum
        check(checksum == saved['expectedPrimaryChecksums'][mid], 'saved primary checksum exact', [cid, mid])
    expected_windows = windows.get(cid, [])
    check([(w['startTick'], w['endTick']) for w in saved['reportingWindows']] == expected_windows, 'prospective window ranges', cid)
    for old_window in saved['reportingWindows']:
        new_window = {k: v for k, v in old_window.items() if k != 'methods'}
        new_window['methods'] = []
        for mi, mid in enumerate(C['variants']):
            load_min, load_max = [math.inf] * 3, [-math.inf] * 3
            wind_min, wind_max = math.inf, -math.inf
            for tick in range(old_window['startTick'], old_window['endTick'] + 1):
                v, ref = rows[tick]['values'][mi], rows[tick]['values'][0]
                for side in [v] + ([v['left']] if v['left'] is not None else []):
                    for k in range(3):
                        e = side['loads'][k] - ref['loads'][k]
                        load_min[k], load_max[k] = min(load_min[k], e), max(load_max[k], e)
                    for k in range(4):
                        e = side['winds'][k] - ref['winds'][k]
                        wind_min, wind_max = min(wind_min, e), max(wind_max, e)
            new_window['methods'].append({'id': mid, 'signedLoadMin': load_min, 'signedLoadMax': load_max, 'signedWindMin': wind_min, 'signedWindMax': wind_max})
        check(new_window == old_window, 'exact signed window extrema', [cid, old_window['label']])
        case_review['reportingWindows'].append(new_window)
    fields = 2 * len(rows) + sum(refresh_counts[cid][mid] for mid in C['variants'] if mid != 'instant')
    science_fields += fields
    oracle_fields += len(rows)
    check(fields == saved['scienceFieldCalls'] == 8906 and saved['oracleCalls'] == len(rows), 'per-case science/oracle count', cid)
    if cid == 'fixed-position-source-pitch':
        records = []
        for row in rows:
            tick = row['tick']
            v, ref = row['values'][4], row['values'][0]
            for side, value in [('sample', v)] + ([('left', v['left'])] if v['left'] is not None else []):
                err = value['loads'][0] - ref['loads'][0]
                records.append({'tick': tick, 'timeSeconds': tick * C['tickSeconds'], 'side': side, 'signedThrustErrorN': err, 'absoluteThrustErrorN': abs(err), 'initialHoldInterval': tick < 20 or (tick == 20 and side == 'left')})
        initial = [r for r in records if r['initialHoldInterval']]
        later = [r for r in records if not r['initialHoldInterval']]
        exceed = [r for r in records if r['absoluteThrustErrorN'] > budgets[0] + C['arithmeticAgreementTolerance']]
        source_pitch_detail = {'scope': 'Descriptive decomposition of saved samples only; no new sampling.', 'initialHoldPeak': max(initial, key=lambda x: x['absoluteThrustErrorN']), 'afterInitialHoldPeak': max(later, key=lambda x: x['absoluteThrustErrorN']), 'exceedanceCount': len(exceed), 'allExceedancesInInitialHold': all(r['initialHoldInterval'] for r in exceed), 'firstExceedance': exceed[0] if exceed else None, 'lastExceedance': exceed[-1] if exceed else None}
    review['cases'].append(case_review)

comparisons = []
for case in review['cases']:
    methods = {m['id']: m for m in case['metrics']}
    p, h, short = methods['predict-5ms'], methods['hold-5ms'], methods['hold-2.5ms']
    for k, observable in enumerate(observables):
        floor = C['momentSamplingFloor'] if k else C['forceSamplingFloor']
        entry = {'case': case['id'], 'observable': observable, 'floor': floor}
        short_entry = {'case': case['id'], 'observable': observable, 'floor': floor}
        for metric in ['peak', 'rms']:
            pv, hv, sv = p['refined'][k][metric], h['refined'][k][metric], short['refined'][k][metric]
            entry[metric + 'NoWorse'] = pv <= hv + floor
            entry[metric + 'StrictlyBetter'] = pv < hv - floor
            entry[metric + 'ScreensPass'] = p['sampling'][k][metric + 'Stable'] and h['sampling'][k][metric + 'Stable']
            short_entry[metric] = {'predictor': pv, 'hold2p5ms': sv, 'difference': pv - sv, 'predictorVsHold2p5ms': pv / sv if sv else None, 'comparison': 'better' if pv < sv - floor else 'worse' if pv > sv + floor else 'within-floor', 'bothSamplingScreensPass': p['sampling'][k][metric + 'Stable'] and short['sampling'][k][metric + 'Stable']}
        comparisons.append(entry)
        review['predictorVsHold2p5ms'].append(short_entry)
suite = {'comparisons': comparisons, 'allTestedPeaksImproved': all(x['peakNoWorse'] and x['peakScreensPass'] for x in comparisons) and any(x['peakStrictlyBetter'] for x in comparisons), 'allTestedRmsImproved': all(x['rmsNoWorse'] and x['rmsScreensPass'] for x in comparisons) and any(x['rmsStrictlyBetter'] for x in comparisons), 'scope': R['suiteDecision']['scope']}
check(suite == R['suiteDecision'] and len(comparisons) == 18, 'all 18 prospective suite decisions')
review['suiteDecision'] = suite
review['suiteStrictImprovementCounts'] = {m: sum(x[m + 'StrictlyBetter'] for x in comparisons) for m in ['peak', 'rms']}
review['predictorVsHold2p5msCounts'] = {m: dict(Counter(x[m]['comparison'] for x in review['predictorVsHold2p5ms'])) for m in ['peak', 'rms']}
review['sourcePitchPredictorStartup'] = source_pitch_detail

timings = []
for pass_id in range(6):
    for ci in range(6):
        for j in range(5):
            t = read(BASE / 'raw' / f'timing-{pass_id}-{ci}-{j}.json')
            cid, mid = C['cases'][(ci + pass_id) % 6], C['variants'][(j + pass_id) % 5]
            fields = 2001 if mid == 'instant' else refresh_counts[cid][mid]
            check(t['case'] == cid and t['id'] == mid and t['pass'] == pass_id and t['warmup'] == (pass_id == 0), 'timing order/identity/warmup', [pass_id, ci, j])
            check(t['fieldCalls'] == fields and t['checksum'] == checksums[cid][mid], 'timing exact count/checksum', [pass_id, ci, j])
            check(math.isfinite(t['totalMs']) and t['totalMs'] > 0, 'timing finite/positive', [pass_id, ci, j])
            timings.append(t)
review['timing'] = []
for case in R['cases']:
    cid = case['id']
    out = {'case': cid, 'methods': []}
    for mid in C['variants']:
        all_passes = [t for t in timings if t['case'] == cid and t['id'] == mid]
        selected = [t for t in all_passes if not t['warmup']]
        check(len(all_passes) == 6 and len(selected) == 5 and {t['pass'] for t in selected} == set(range(1, 6)), 'six total/five recorded passes', [cid, mid])
        values = [t['totalMs'] for t in selected]
        stats = {'minimum': min(values), 'median': statistics.median(values), 'maximum': max(values)}
        old = next(t for t in case['timingSummary'] if t['id'] == mid)
        check(stats == old['totalMs'] and all(t['fieldCalls'] == old['fieldCalls'] for t in all_passes), 'timing summary exact', [cid, mid])
        out['methods'].append({'id': mid, 'totalMs': stats, 'recordedMs': values, 'fieldCalls': old['fieldCalls'], 'checksum': checksums[cid][mid]})
    mm = {m['id']: m for m in out['methods']}
    p = mm['predict-5ms']['totalMs']
    out['predictorComparisons'] = {}
    for mid in ['hold-5ms', 'hold-2.5ms']:
        h = mm[mid]['totalMs']
        out['predictorComparisons'][mid] = {'medianRatio': p['median'] / h['median'], 'predictorRangeStrictlyLower': p['maximum'] < h['minimum'], 'predictorRangeStrictlyHigher': p['minimum'] > h['maximum'], 'rangesOverlap': max(p['minimum'], h['minimum']) <= min(p['maximum'], h['maximum'])}
    review['timing'].append(out)

timing_fields = sum(t['fieldCalls'] for t in timings)
raw_bytes = sum(p.stat().st_size for p in raw_files)
check(science_fields == 53436 and timing_fields == 104580 and science_fields + timing_fields == R['fieldCalls'] == 158016, 'total field accounting including oracle')
check(oracle_fields == R['oracleCalls'] == 24006, 'total oracle accounting')
check(raw_bytes == 41337905 == B['entries'][0]['rawBytesAfter'], 'raw byte accounting')
check(C['rawByteCap'] == B['rawByteCap'] == 128 * 1024 * 1024 and C['failureReserveBytes'] == 1024 * 1024 and raw_bytes < C['rawByteCap'] - C['failureReserveBytes'], 'raw cap and reserved failure allowance')
check(len(B['entries']) == 1 and B['entries'][0]['completeProcess'] and B['entries'][0]['exitCode'] == 0 and B['entries'][0]['stop'] is None, 'single successful supervisor invocation')
check(B['entries'][0]['wallSeconds'] == 3.2304365 and B['entries'][0]['wallSeconds'] < C['wallCapSeconds'] and R['fieldCalls'] < C['fieldCallCap'], 'observed wall/call caps')
check(not R['noveltyEstablished'] and not R['physicalValidation'], 'restricted conclusion flags')
review['accounting'] = {'rawBytes': raw_bytes, 'rawFiles': len(raw_files), 'savedFineInputs': oracle_fields, 'savedOracleScalarComparisons': oracle_scalar_count, 'scienceFieldCalls': science_fields, 'timingFieldCalls': timing_fields, 'totalFieldCalls': R['fieldCalls'], 'includedOracleCalls': oracle_fields, 'boundCalls': 0, 'timingRecords': len(timings), 'supervisorWallSeconds': B['entries'][0]['wallSeconds'], 'driverElapsedSeconds': R['elapsedSeconds'], 'budgetTerminalAtReview': B['terminal']}
review['limitations'] = [
    'The matched hold5 suite decision is restricted to these six selected model-input cases; it is not physical validation or a universal predictor advantage.',
    'A suite-relative improvement does not imply passing numerical targets. Source-pitch predictor target failure must remain visible.',
    'Hold2.5 comparisons are descriptive; preserve any peak/RMS losses and report recorded timing with errors.',
    'Event-split RMS is a different, prospectively declared estimand; earlier uniform-RMS failures remain failed.',
    'Exact timing checksums verify the accumulated saved primary loads, not a collision-proof per-query identity proof.',
    'This verifier does not reevaluate the physical/model meaning of saved loads or the analytic case functions.',
    'Technical timing ranges are not confidence intervals. The separate all-pairs static domain audit and frozen source define scope.'
]
review['checkCount'] = sum(categories.values())
review['checkCategories'] = dict(categories)
review['failedChecks'] = failures
review['passed'] = not failures
review['verificationWallSecondsBeforeOutput'] = time.perf_counter() - START
serialized = json.dumps(review, indent=2, allow_nan=False) + '\n'
(RUN / 'review.json').write_text(serialized)
OUT.write_text(serialized)
summary = {'passed': review['passed'], 'checks': review['checkCount'], 'failedChecks': failures, 'samplingFailures': review['samplingFailures'], 'metricDiscrepancy': review['metricDiscrepancy'], 'suiteStrictImprovementCounts': review['suiteStrictImprovementCounts'], 'predictorVsHold2p5msCounts': review['predictorVsHold2p5msCounts'], 'sourcePitchPredictorStartup': source_pitch_detail, 'accounting': review['accounting'], 'invocationArchive': str(RUN), 'verificationWallSecondsThroughReviewWrites': time.perf_counter() - START}
stdout = json.dumps(summary, indent=2, allow_nan=False) + '\n'
(RUN / 'stdout.json').write_text(stdout)
print(stdout, end='')
