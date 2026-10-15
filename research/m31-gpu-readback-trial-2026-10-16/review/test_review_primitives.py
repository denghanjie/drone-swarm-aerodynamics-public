"""Pure predicates and disposable bounded-read fixtures; never checker main."""

import copy
import datetime
import json
from pathlib import Path
import sys
import tempfile

sys.dont_write_bytecode = True
from byte_primitives import compare_byte_evidence, expected_bytes
from review_primitives import (COUNTS, LAYOUT, LIMITS, OBS_BOOL, OBS_LENGTH, STAGES, admit_review,
                               json_bytes, read_bounded, strict_equal, validate_page_claims)


def page_fixture(candidate=True):
    observation = {key: False for key in OBS_BOOL}
    observation.update({key: None for key in OBS_LENGTH})
    observation.update(adapterAvailable=None, isFallbackAdapter='unavailable', compilationErrors=0,
                       compilationWarnings=0, compilationInfos=0, mapStateAtCopy=None, ownedIndependent=None,
                       rangeDetached=None, lossBeforeDestroySnapshot='not-observed', deviceLostReason='not-observed',
                       uncapturedErrorKinds=[], scopes=[{'filter':f,'state':'unpushed','errorKind':None}
                                                       for f in ['out-of-memory','internal','validation']])
    stages = ['entered','work-failed','cleanup-started','return-envelope-ready']
    if candidate:
        observation.update({key: True for key in ['limitsAdmitted','unmapSucceeded','storageDestroyed','readbackDestroyed',
                                                'deviceDestroyAttempted','deviceDestroySucceeded','expectedDestroyLossObserved']})
        observation.update(adapterAvailable=True, isFallbackAdapter=False, mapStateAtCopy='mapped', ownedIndependent=True,
                           rangeDetached=True, deviceLostReason='destroyed', mappedByteLengthBeforeUnmap=128,
                           mappedByteLengthAfterUnmap=0, ownedByteLengthBeforeRelease=128, ownedByteLengthAfterRelease=128)
        for scope in observation['scopes']:
            scope['state'] = 'popped'
        stages = STAGES
    return {'version':1,'kind':'synthetic-gpu-readback-envelope','fixtureId':'m31-u32-readback-128-v1',
            'phaseEvidenceKind':'page-self-report','requiresIndependentPersistenceReview':True,'scientificQualified':False,
            'historicalFailureExplained':False,'performanceClaim':False,'layout':dict(LAYOUT),
            'context':{'originLabel':'page-origin','isSecureContext':True,'webgpuSupported':candidate},
            'status':'candidate-readback' if candidate else 'failed','values':list(expected_bytes()) if candidate else None,
            'returnedByteLength':128 if candidate else 0,'events':[{'sequence':i+1,'stage':stage,'browserMilliseconds':i+1}
                                                               for i,stage in enumerate(stages)],
            'failures':[] if candidate else ['webgpu-unavailable'],'eventOverflow':False,'failureOverflow':False,
            'counts':{key:1 if candidate else 0 for key in COUNTS},'observation':observation,
            'lastWorkStage':'owned-copy-made' if candidate else 'entered','browserElapsedMilliseconds':100}


def run():
    cases = []
    def checked(name, condition):
        assert condition, name
        cases.append({'case':name,'pass':True})
    def rejected(name, operation):
        try:
            operation()
        except (ValueError, OSError):
            checked(name, True)
        else:
            checked(name, False)

    now = datetime.datetime(2020,1,1,0,1,tzinfo=datetime.timezone.utc)
    config = {'version':1,'scope':'synthetic-gpu-readback-host','limits':dict(LIMITS),'executionAllocated':True,'notBeforeUTC':'2020-01-01T00:00:00Z','stopNewLaunchUTC':'2020-01-01T00:02:00Z',
              'reviewNotBeforeUTC':'2020-01-01T00:00:30Z','reviewStopNewLaunchUTC':'2020-01-01T00:03:00Z'}
    checked('pure_hypothetical_allocated_window', admit_review(config, now)['review_start'] <= now)
    for name, changes in [('disabled',{'executionAllocated':False}), ('truthy_integer_not_allocation',{'executionAllocated':1}),
                          ('null_launch_window',{'notBeforeUTC':None}), ('null_review_window',{'reviewStopNewLaunchUTC':None}),
                          ('invalid_calendar_date',{'notBeforeUTC':'2020-02-30T00:00:00Z'}),
                          ('non_UTC_offset',{'notBeforeUTC':'2020-01-01T00:00:00+00:00'}),
                          ('fractional_config_window',{'notBeforeUTC':'2020-01-01T00:00:00.000Z'}),
                          ('wrong_config_identity',{'scope':'historical-campaign'}),
                          ('changed_resource_bound',{'limits':{**LIMITS,'evaluateSeconds':10}}),
                          ('reversed_review_window',{'reviewNotBeforeUTC':'2020-01-01T00:04:00Z'})]:
        value = {**config, **changes}
        rejected('admission_' + name, lambda value=value: admit_review(value, now))
    rejected('admission_at_exclusive_stop', lambda: admit_review(config, datetime.datetime(2020,1,1,0,3,tzinfo=datetime.timezone.utc)))

    candidate = page_fixture()
    claim = validate_page_claims(candidate)
    checked('candidate_claim_is_consistent_but_not_GPU_attestation', claim['candidateByPageSelfReport']
            and claim['gpuExecutionIndependentlyAttested'] is False)
    failed = validate_page_claims(page_fixture(False))
    checked('honest_failed_page_without_bytes', failed['status'] == 'failed' and failed['values'] is None)
    failed_bytes = page_fixture(); failed_bytes['status']='failed'; failed_bytes['failures']=['error-scope-nonempty']
    failed_bytes['observation']['scopes'][0]['errorKind']='validation'
    claim = validate_page_claims(failed_bytes)
    checked('matching_bytes_do_not_promote_failed_page', not claim['candidateByPageSelfReport']
            and compare_byte_evidence(claim['values'], expected_bytes())['all_bytes_match'])
    wrong = page_fixture(); wrong['values'][16] ^= 1
    claim = validate_page_claims(wrong)
    checked('page_candidate_does_not_imply_expected_bytes', claim['candidateByPageSelfReport']
            and not compare_byte_evidence(claim['values'], bytes(claim['values']))['all_bytes_match'])
    false_phase = page_fixture(); false_phase['observation']['deviceDestroySucceeded']=False
    rejected('candidate_missing_destroy_claim', lambda: validate_page_claims(false_phase))
    false_count = page_fixture(); false_count['counts']['submissions']=0
    rejected('phase_count_contradiction', lambda: validate_page_claims(false_count))
    boolean_length = page_fixture(); boolean_length['values'][0]=True
    rejected('boolean_byte_rejected', lambda: validate_page_claims(boolean_length))
    missing_padding = page_fixture(); missing_padding['values']=missing_padding['values'][16:84]
    rejected('active_only_return_rejected', lambda: validate_page_claims(missing_padding))
    forged_claim = page_fixture()
    checked('forged_cpu_candidate_does_not_attest_device', validate_page_claims(forged_claim)['gpuExecutionIndependentlyAttested'] is False)
    checked('nested_boolean_cannot_replace_integer_projection', not strict_equal({'counts':{'submissions':True}}, {'counts':{'submissions':1}}))

    rejected('duplicate_JSON_keys', lambda: json_bytes(b'{"a":1,"a":2}',128))
    rejected('nonfinite_JSON', lambda: json_bytes(b'{"a":NaN}',128))
    rejected('negative_zero_JSON_integer', lambda: json_bytes(b'{"a":-0}',128))
    rejected('negative_zero_JSON_float', lambda: json_bytes(b'{"a":-0.0}',128))
    rejected('overflow_JSON_float', lambda: json_bytes(b'{"a":1e999}',128))
    rejected('oversized_JSON', lambda: json_bytes(b'{}',1))

    with tempfile.TemporaryDirectory(prefix='gpu-review-inert-') as directory:
        root = Path(directory).resolve()
        expected = expected_bytes(); (root/'actual.bin').write_bytes(expected)
        checked('scratch_reread_actual_bytes', read_bounded(root,'actual.bin',128) == expected)
        wrong_bytes = bytearray(expected); wrong_bytes[0] ^= 1; (root/'actual.bin').write_bytes(wrong_bytes)
        actual = read_bounded(root,'actual.bin',128)
        facts = compare_byte_evidence(list(wrong_bytes), actual)
        checked('scratch_wrong_bytes_consistent_failed_fixture', facts['returned_equals_persisted']
                and not facts['all_bytes_match'] and not facts['persisted_padding_matches'])
        (root/'extra.bin').write_bytes(expected+b'\0')
        rejected('scratch_trailing_byte_cap', lambda: read_bounded(root,'extra.bin',128))
        (root/'link.bin').symlink_to(root/'actual.bin')
        rejected('scratch_symlink', lambda: read_bounded(root,'link.bin',128))
        (root/'folder').mkdir()
        rejected('scratch_directory', lambda: read_bounded(root,'folder',128))
        rejected('scratch_parent_traversal', lambda: read_bounded(root,'../actual.bin',128))
        rejected('scratch_absolute_path', lambda: read_bounded(root,str(root/'actual.bin'),128))
        # Admission test reads configuration only; it never calls a runtime reader.
        marker = root/'runtime-marker'; marker.write_bytes(b'unchanged')
        before = marker.stat().st_mtime_ns
        rejected('disabled_admission_preserves_scratch_runtime_marker', lambda: admit_review({**config,'executionAllocated':False},now))
        checked('scratch_runtime_marker_untouched', marker.read_bytes()==b'unchanged' and marker.stat().st_mtime_ns==before)

    return {'kind':'static-gpu-saved-review-primitive-tests','full_checker_main_called':False,
            'browser_gpu_network_or_operational_source_executed':False,'actual_campaign_evidence_read':False,
            'scratch_file_reads_only':True,'passed':len(cases),'failed':0,'cases':cases}


if __name__ == '__main__':
    result = run()
    Path(__file__).with_name('PURE-TEST-RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'passed':result['passed'],'failed':result['failed']}))
