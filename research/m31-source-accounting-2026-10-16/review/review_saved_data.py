"""One authorized saved-data review; never imports or invokes audit source."""
import hashlib
import json
import math
import resource
import subprocess
import sys
import time
from decimal import Decimal, getcontext
from pathlib import Path

resource.setrlimit(resource.RLIMIT_CPU, (30, 30))
ROOT = Path(sys.argv[1])
HERE = Path(__file__).resolve().parent
BASE = ROOT / 'research/m31-source-accounting-2026-10-16'
COMMIT = 'b515ac7a0b146ebf337431fb492d145d9a43c619'
FREEZE = 'e343f288205b27e0996a6141db6af20ea4ab2f5be2ab5e0eb3ca5b6cd287eca3'
cpu_start = time.process_time()
getcontext().prec = 70
D = Decimal
checks = []
report = {'kind': 'independent-saved-source-accounting-review', 'sourceCommit': COMMIT,
          'freezeSHA256': FREEZE, 'sourceWitnessReruns': 0,
          'originalRunnerInvocations': 0, 'browserOrGPUInvocations': 0,
          'originalAuditImports': 0, 'checks': checks}

def check(name, condition, details=None):
    item = {'name': name, 'pass': bool(condition)}
    if details is not None:
        item['details'] = details
    checks.append(item)

def close(actual, expected, tolerance=1e-12):
    return math.isfinite(float(actual)) and abs(float(actual)-float(expected)) <= tolerance

def load(name):
    return json.loads((BASE / 'results' / name).read_text())

def sha(data):
    return hashlib.sha256(data).hexdigest()

def main():
    freeze_data = (BASE / 'freeze.json').read_bytes()
    freeze = json.loads(freeze_data)
    check('expected_freeze_hash', sha(freeze_data) == FREEZE)
    blobs = {'research/m31-source-accounting-2026-10-16/freeze.json': freeze_data}
    pin_details = []
    for pin in freeze['files']:
        data = (ROOT / pin['path']).read_bytes()
        ok = len(data) == pin['bytes'] and sha(data) == pin['sha256']
        pin_details.append({'path': pin['path'], 'pass': ok, 'sha256': sha(data)})
        blobs[pin['path']] = data
    check('all_freeze_file_pins', all(p['pass'] for p in pin_details), pin_details)
    prior = json.loads((HERE / 'SOURCE-PINS.json').read_text())
    prior_checks = []
    for pin in prior['files']:
        data = (ROOT / pin['path']).read_bytes()
        prior_checks.append(len(data) == pin['bytes'] and sha(data) == pin['sha256'])
    historical = prior['historicalSource']
    historical_data = (ROOT / historical['path']).read_bytes()
    check('preexecution_review_pins_unchanged', all(prior_checks))
    check('historical_source_pin_unchanged', sha(historical_data) == historical['sha256'])
    blobs[historical['path']] = historical_data
    requests = ''.join(COMMIT + ':' + path + '\n' for path in blobs).encode()
    git = subprocess.run(['git', 'cat-file', '--batch'], cwd=str(ROOT), input=requests,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=5)
    cursor = 0
    committed = []
    for path, expected in blobs.items():
        end = git.stdout.index(b'\n', cursor)
        header = git.stdout[cursor:end].split()
        cursor = end+1
        if len(header) != 3 or header[1] != b'blob':
            raise ValueError('Missing committed source blob: ' + path)
        size = int(header[2])
        actual = git.stdout[cursor:cursor+size]
        cursor += size+1
        committed.append({'path': path, 'matches': actual == expected})
    check('files_match_frozen_git_commit', git.returncode == 0 and all(x['matches'] for x in committed), committed)

    inputs = []
    for path in sorted((BASE/'results').iterdir()):
        if path.is_file():
            data = path.read_bytes()
            inputs.append({'path': 'results/'+path.name, 'bytes': len(data), 'sha256': sha(data)})
    report['savedInputInventory'] = inputs
    check('author_result_output_under_two_mib', sum(x['bytes'] for x in inputs) < 2*1024*1024)
    started, execution, tool = load('started.json'), load('execution.json'), load('tool-completion.json')
    check('recorded_source_commit_and_freeze', started['sourceCommit'] == COMMIT and started['freezeSHA256'] == FREEZE)
    check('saved_success_and_bounded_driver', execution['workerExitCode'] == 0 and not execution['timeout'] and not execution['cleanupIncomplete'] and execution['pipeCaptureComplete'] and execution['externalWorkerSeconds'] < 30 and execution['within30SecondCeiling'])
    check('tool_completed_without_remaining_session', tool['toolExitCode'] == 0 and tool['toolSessionRemaining'] is False)
    check('saved_driver_pipe_sizes', execution['stdoutBytes'] == (BASE/'results/driver-stdout.txt').stat().st_size and execution['stderrBytes'] == (BASE/'results/driver-stderr.txt').stat().st_size)
    report['timing'] = {'toolWallSeconds': tool['toolReportedWallSeconds'],
                        'driverSeconds': execution['externalWorkerSeconds'],
                        'toolWallSmallerThanDriver': tool['toolReportedWallSeconds'] < execution['externalWorkerSeconds'],
                        'nestedStopwatchVerification': False, 'performanceResult': False,
                        'interpretation': 'Retained scopes are not reconciled; numerical completion and recorded driver bound only.'}

    result, witness = load('result.json'), load('witness-stdout.json')
    check('recorded_runtime_versions', started['pythonVersion'] == '3.9.6' and witness['nodeVersion'] == 'v24.19.0')
    weight = D('.027')*D('9.81')
    motor_arrays = [[D(0)]*4, [weight/16]*4, [weight/4]*4, [weight/2]*4,
                    [D('.4')*weight,D('.1')*weight,D('.4')*weight,D('.1')*weight]]
    ids = ['off','quarter-hover','hover','twice-hover','unequal-same-total']
    cases = witness['cases']
    check('five_recorded_cases_and_twenty_fields', [x['id'] for x in cases] == ids and witness['calls'] == 20 and len(cases) == 5 and sum(len(x['fields']) for x in cases) == 20 and all(len(x['fields']) == 4 for x in cases))
    check('five_source_arrays_and_totals', all(all(close(x,y,1e-15) for x,y in zip(case['sourceNominalRotorsN'], expected)) and len(case['sourceNominalRotorsN']) == 4 and close(case['sourceTotalNominalN'], sum(expected),1e-15) for case,expected in zip(cases,motor_arrays)))
    fields = [f for case in cases for f in case['fields']]
    expected_keys = {'symbol','term','down','radial','projection','center','validity','stage'}
    check('all_fields_and_policies_exactly_equal', all(f == fields[0] and set(f) == expected_keys for f in fields))
    check('positive_admitted_static_stimulus', all(f['term'] > 0 and math.isfinite(f['term']) and f['symbol'] == 8 and f['validity'] == 31 and f['stage'] == 0 and f['projection'] == 1 and f['down'] == .6 and f['center'] == .6 for f in fields) and witness['stimulusAdmitted'] and witness['sourceIndependentInTheseCases'])
    report['witness'] = {'savedFieldRecordCount': len(fields), 'savedDistinctTerms': sorted(set(f['term'] for f in fields)), 'allSourceArraysVerified': True,
                         'interpretation': 'Static current-model motor-insensitivity; not measured shutdown behavior.'}

    a_dec = D(2).sqrt()-1
    diameter_dec = 2*D(2).sqrt()*D('.028')
    k_dec = (D('10.11')*D('.07668'))**2*(diameter_dec/D('.023'))**2/(24*a_dec)
    a = float(a_dec)
    integral_exact = 1/(6*a_dec)
    check('analytic_normalization', close(result['untruncatedJOverWeight'], k_dec))
    constants = result['constants']
    expected_constants = {'a':a_dec,'C':D('10.11'),'S':D('.07668'),'origin':D('-5.817'),'D':diameter_dec,'rotorRadius':D('.023'),'rho':D('1.225'),'mass':D('.027'),'g':D('9.81'),'nominalWeightN':weight}
    check('prescribed_constants', all(close(constants[key], value) for key,value in expected_constants.items()))

    # Independent quadrature: analytic [0,2] plus composite four-point Gauss
    # on [2,3], with expanded radial fade. No author Simpson routine is used.
    small = math.sqrt((3-2*math.sqrt(6/5))/7)
    large = math.sqrt((3+2*math.sqrt(6/5))/7)
    small_w = (18+math.sqrt(30))/36
    large_w = (18-math.sqrt(30))/36
    nodes = [(-large,large_w),(-small,small_w),(small,small_w),(large,large_w)]
    core = float(integral_exact)*(1-(1+4*a)**-3)
    gauss = []
    for panels in [16,32]:
        pieces = []
        half = 1/(2*panels)
        for panel in range(panels):
            center = 2+(panel+.5)/panels
            for node, node_weight in nodes:
                x = center+half*node
                pieces.append(half*node_weight*x*(3-x)**4*(2*x-3)**2/(1+a*x*x)**4)
        gauss.append({'panelsOnTwoToThree':panels,'evaluationCount':4*panels,'radialIntegral':core+math.fsum(pieces)})
    independent_radial = gauss[-1]['radialIntegral']
    independent_retention = independent_radial/float(integral_exact)
    check('independent_gauss_level_agreement', abs(gauss[1]['radialIntegral']-gauss[0]['radialIntegral']) <= 1e-12)
    q = result['quadrature']
    check('four_saved_quadrature_resolutions', [x['subdivisionsPerUnitInterval'] for x in q] == [128,256,512,1024])
    residuals = []
    for row in q:
        residuals.append({'subdivisionsPerUnitInterval':row['subdivisionsPerUnitInterval'],
                          'untruncatedMinusIndependentAnalytic':row['untruncatedIntegral']-float(integral_exact),
                          'radialMinusIndependentGauss':row['radialFadedIntegral']-independent_radial})
        check('saved_quadrature_record_'+str(row['subdivisionsPerUnitInterval']), close(row['analyticIntegral'],integral_exact) and close(row['absoluteError'],abs(row['untruncatedIntegral']-row['analyticIntegral']),1e-16) and close(row['retention'],row['radialFadedIntegral']/row['analyticIntegral']))
    final_error = abs(q[-1]['untruncatedIntegral']-float(integral_exact))
    full_delta = abs(q[-1]['untruncatedIntegral']-q[-2]['untruncatedIntegral'])
    radial_delta = abs(q[-1]['radialFadedIntegral']-q[-2]['radialFadedIntegral'])
    saved_delta = result['convergence512To1024']
    check('declared_quadrature_gates', final_error <= 1e-9 and full_delta <= 1e-9 and radial_delta <= 1e-9 and close(saved_delta['untruncatedAbsoluteDifference'],full_delta,1e-16) and close(saved_delta['radialFadedAbsoluteDifference'],radial_delta,1e-16))
    check('final_radial_matches_independent_gauss', abs(q[-1]['radialFadedIntegral']-independent_radial) <= 1e-9 and close(result['radialSquaredProfileRetention'],independent_retention,1e-9))
    report['independentQuadrature'] = {'method':'analytic inner disk plus composite four-point Gauss-Legendre on xi 2 to 3', 'levels':gauss,
        'analyticIntegralDecimal':str(integral_exact),'normalizationDecimal':str(k_dec),'independentRetention':independent_retention,
        'authorMinusIndependentRadial':q[-1]['radialFadedIntegral']-independent_radial,'savedLevelResiduals':residuals,
        'finiteCheckOnly':True,'rigorousIntervalEnclosure':False}

    planes = result['planes']
    stations = [.25,.6,1,1.5,2,2.1,2.25,2.4,2.5,3]
    check('ten_saved_planes', [p['downstreamM'] for p in planes] == stations and len(planes) == 10)
    check('four_hundred_ten_profile_points', all(len(p['profile']) == 41 for p in planes) and sum(len(p['profile']) for p in planes) == 410)
    uh = math.sqrt(float(weight)/(8*1.225*math.pi*.023**2))
    check('hover_velocity_constant',close(constants['UH'],uh))
    k = float(k_dec)
    force_proxy = float(weight)*k
    diameter = float(diameter_dec)
    plane_diffs = []
    profile_max = 0.0
    profile_failures = 0
    for plane in planes:
        s = plane['downstreamM']
        length = s+5.817*diameter
        b = .07668*length
        uc = 10.11*uh*diameter/length
        reverse = max(0.0,min(1.0,(2.5-s)/.5))
        down_fade = reverse*reverse*(3-2*reverse)
        radial_proxy = force_proxy*independent_retention
        expected = {'halfWidthM':b,'nominalRadialCutoffM':3*b,'centerlineUntruncatedMps':uc,'downstreamFade':down_fade,'JUntruncatedN':force_proxy,'JRadialOnlyN':radial_proxy,'JBothFadesN':radial_proxy*down_fade**2,'JBothOverNominalWeight':k*independent_retention*down_fade**2}
        maximum = max(abs(plane[name]-value) for name,value in expected.items())
        plane_diffs.append({'downstreamM':s,'maximumAbsoluteScalarDifference':maximum})
        check('plane_'+str(s),maximum <= 1e-10 and plane['fadedFieldIdenticallyZero'] == (s >= 2.5))
        for index, point in enumerate(plane['profile']):
            x = index/10
            radial_fade = 1.0 if x <= 2 else (0.0 if x >= 3 else (3-x)**2*(2*x-3))
            speed = uc/(1+a*x*x)**2
            exp = {'xi':x,'radiusM':x*b,'untruncatedMps':speed,'radialOnlyMps':speed*radial_fade,'bothFadesMps':speed*radial_fade*down_fade}
            diff = max(abs(point[name]-value) for name,value in exp.items())
            profile_max = max(profile_max,diff)
            profile_failures += diff > 1e-11
    check('all_profile_point_values',profile_failures == 0)
    invariance = max(abs(p['JUntruncatedN']/float(weight)-result['untruncatedJOverWeight']) for p in planes)
    check('saved_plane_invariance',invariance <= 1e-12 and close(result['planeRatioMaxDifference'],invariance,1e-16))
    report['planeAndProfileReview'] = {'planeResiduals':plane_diffs,'profilePointsChecked':410,'velocityValuesChecked':1230,'allNumericProfileFieldsChecked':2050,'maximumAbsoluteProfileDifference':profile_max}

    published = result['publishedComparison']
    ratio_speed = (D(94)/D(81))**2
    ratio_load = D('5.32')/D('3.90')
    recomputed = {'recomputedSquaredFrequencyRatio':ratio_speed,'recomputedFlowRatio':ratio_load,
                  'signedRatioDifference':ratio_speed-ratio_load,'relativeRatioDifference':ratio_speed/ratio_load-1,
                  'printedFrontBackSumN':D('5.32')+D('3.90')}
    check('published_ratio_arithmetic',all(close(published[key],value) for key,value in recomputed.items()))
    printed = {'frontFrequencyHz':94,'backFrequencyHz':81,'frontFlowMomentumN':5.32,'backFlowMomentumN':3.90,'totalFlowMomentumN':9.21,'weightProxyN':8.98,'authorReportedForceRatio':1.366,'authorReportedSquaredFrequencyRatio':1.347}
    check('printed_published_inputs_preserved',all(published[key] == value for key,value in printed.items()))
    bounds_speed = [(D('93.5')/D('81.5'))**2,(D('94.5')/D('80.5'))**2]
    bounds_load = [D('5.315')/D('3.905'),D('5.325')/D('3.895')]
    check('last_digit_rounding_ranges',all(close(x,y) for x,y in zip(published['squaredFrequencyRoundingRange'],bounds_speed)) and all(close(x,y) for x,y in zip(published['flowRatioRoundingRange'],bounds_load)))
    check('stated_interpretation_limits',not published['roundingRangesAreMeasurementUncertainty'] and not published['physicalValidationEstablished'] and result['fieldPlaneExcludesReceiverCenterGate'] and result['JIsMeasuredThrust'] is False and result['newPhysicalMeasurements'] == 0)
    report['publishedIndependentDecimalArithmetic'] = {key:str(value) for key,value in recomputed.items()}
    report['publishedIndependentDecimalArithmetic']['squaredFrequencyRoundingRange'] = [str(x) for x in bounds_speed]
    report['publishedIndependentDecimalArithmetic']['flowRatioRoundingRange'] = [str(x) for x in bounds_load]
    check('author_gate_flag_consistent',result['numericalGatePass'] is True)

try:
    main()
except Exception as error:
    report['exception'] = {'type':type(error).__name__,'message':str(error)}
    check('review_completed_without_exception',False)
report['cpuSecondsForAllocationOnly'] = time.process_time()-cpu_start
check('independent_review_cpu_under_thirty_seconds',report['cpuSecondsForAllocationOnly'] < 30)
report['allChecksPass'] = all(c['pass'] for c in checks)
report['checkCount'] = len(checks)
report['limits'] = ['One authorized saved-data review, no source witness rerun.',
    'Positive identical source fields describe the implemented static model, not measured shutdown.',
    'J is a squared scalar-profile proxy, not true thrust or a full momentum balance.',
    'Independent quadrature is a finite check, not a rigorous error enclosure.',
    'Published arithmetic is descriptive and based on already-seen printed values; primary article not independently reopened.',
    'Tool and driver timing scopes remain unreconciled; no performance result.',
    'No browser, GPU, controller, original campaign, or process-table observation.']
output = (json.dumps(report,indent=2,sort_keys=True,allow_nan=False)+'\n').encode()
if len(output) >= 2*1024*1024:
    raise ValueError('Independent review output exceeds allocation')
with (HERE/'SAVED-DATA-RAW-CHECKS.json').open('xb') as stream:
    stream.write(output)
print(json.dumps({'allChecksPass':report['allChecksPass'],'checkCount':len(checks),'outputBytes':len(output),'sourceWitnessReruns':0,'independentGaussEvaluationCount':192,'cpuSecondsForAllocationOnly':report['cpuSecondsForAllocationOnly']}))
raise SystemExit(0 if report['allChecksPass'] else 1)
