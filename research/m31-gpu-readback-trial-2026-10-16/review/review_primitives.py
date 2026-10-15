"""Pure record predicates and bounded regular-file reads; no operational imports."""

import datetime
import hashlib
import json
import math
import os
from pathlib import Path
import re
import stat

from byte_primitives import decode_byte_values

FIXTURE_ID = 'm31-u32-readback-128-v1'
LIMITS = {'wallSeconds':60,'workerSeconds':40,'evaluateSeconds':12,'cleanupSeconds':58,
          'combinedBytes':8388608,'ownedRSSBytes':2147483648,'traceEvents':2048}
LAYOUT = dict(wordBytes=4, wordCount=32, byteLength=128, prefixWords=4, activeWords=17,
              suffixWords=11, workgroupSize=8, dispatchGroups=3, launchedInvocations=24, endianness='little')
COUNTS = ['adapterRequests','deviceRequests','initializationWrites','pipelineCreations','dispatchEncodes',
          'copyEncodes','submissions','mapRequests','ownedCopies','returnConversions']
STAGES = ['entered','adapter-requested','adapter-available','adapter-kind-observed','device-requested','device-available',
          'limits-admitted','scope-pushed','scope-pushed','scope-pushed','buffers-created','sentinels-queued','shader-created',
          'compilation-observed','pipeline-requested','pipeline-created','dispatch-encoded','readback-copy-encoded','submitted',
          'map-requested','mapped','owned-copy-made','cleanup-started','unmap-returned','mapped-range-after-unmap',
          'storage-destroy-returned','readback-destroy-returned','scope-popped','scope-popped','scope-popped',
          'device-destroy-intent','device-destroy-returned','expected-destroy-loss','owned-copy-after-release',
          'owned-values-created','return-envelope-ready']
EXTRA_STAGES = ['uncaptured-error','unexpected-device-loss','work-failed']
FAILURES = ['work-deadline','cleanup-deadline','insecure-context','webgpu-unavailable','adapter-timeout','adapter-unavailable',
            'fallback-adapter-rejected','fallback-status-unavailable','device-timeout','unexpected-device-loss','limits-unavailable',
            'compilation-timeout','compilation-message-cap','shader-compilation-error','pipeline-timeout','pipeline-error-validation',
            'pipeline-error-internal','pipeline-error-other','map-timeout','map-state-mismatch','mapped-byte-length','owned-copy-shape',
            'api-operation-rejected','unmap-rejected','mapped-range-not-detached','mapped-range-observation-failed','storage-destroy-rejected',
            'readback-destroy-rejected','error-scope-nonempty','scope-pop-rejected','device-destroy-rejected','destroy-loss-unobserved',
            'return-conversion-failed','uncaptured-error-observed','evidence-cap']
OBS_BOOL = ['limitsAdmitted','unmapSucceeded','storageDestroyed','readbackDestroyed','deviceDestroyAttempted','deviceDestroySucceeded',
            'unexpectedDeviceLoss','expectedDestroyLossObserved','uncapturedErrorOverflow','pendingAdapterRequest','pendingDeviceRequest',
            'pendingMapRequest','pendingWork','cleanupDeadlineExceeded']
OBS_LENGTH = ['mappedByteLengthBeforeUnmap','mappedByteLengthAfterUnmap','ownedByteLengthBeforeRelease','ownedByteLengthAfterRelease']
OBS_KEYS = ['adapterAvailable','isFallbackAdapter','compilationErrors','compilationWarnings','compilationInfos','mapStateAtCopy',
            'ownedIndependent','rangeDetached','lossBeforeDestroySnapshot','deviceLostReason','uncapturedErrorKinds','scopes'] + OBS_BOOL + OBS_LENGTH
TOP_KEYS = ['version','kind','fixtureId','phaseEvidenceKind','requiresIndependentPersistenceReview','scientificQualified',
            'historicalFailureExplained','performanceClaim','layout','context','status','values','returnedByteLength','events',
            'failures','eventOverflow','failureOverflow','counts','observation','lastWorkStage','browserElapsedMilliseconds']


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def integer(value, maximum, minimum=0):
    return type(value) is int and minimum <= value <= maximum


def finite(value, maximum):
    return (type(value) in (int, float) and math.isfinite(value) and 0 <= value <= maximum
            and not (type(value) is float and value == 0 and math.copysign(1, value) < 0))


def exact_keys(value, keys, reason):
    require(type(value) is dict and set(value) == set(keys), reason)


def strict_equal(left, right):
    """JSON value equality without Python's boolean/integer conflation."""
    if type(left) is not type(right):
        return False
    if type(left) is dict:
        return left.keys() == right.keys() and all(strict_equal(left[k],right[k]) for k in left)
    if type(left) is list:
        return len(left) == len(right) and all(strict_equal(a,b) for a,b in zip(left,right))
    return left == right


def json_bytes(data, cap):
    require(type(data) is bytes and len(data) <= cap, 'Bounded JSON bytes required')
    def pairs(items):
        out = {}
        for key, value in items:
            require(key not in out, 'Duplicate JSON key')
            out[key] = value
        return out
    def no_constant(_):
        raise ValueError('Non-finite JSON token')
    def parse_int(value):
        require(value != '-0', 'Negative-zero JSON integer')
        return int(value)
    def parse_float(value):
        parsed = float(value)
        require(math.isfinite(parsed) and not (parsed == 0 and math.copysign(1,parsed) < 0), 'Non-finite or negative-zero JSON float')
        return parsed
    return json.loads(data, object_pairs_hook=pairs, parse_constant=no_constant, parse_int=parse_int, parse_float=parse_float)


def utc_timestamp(value):
    require(type(value) is str and re.fullmatch(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z', value) is not None,
            'Strict explicit UTC timestamp required')
    try:
        parsed = datetime.datetime.fromisoformat(value[:-1] + '+00:00')
    except (ValueError, TypeError):
        raise ValueError('Invalid UTC timestamp') from None
    require(parsed.utcoffset() == datetime.timedelta(0), 'UTC timestamp offset')
    return parsed


def admit_review(config, now):
    """Read no files. Refuse allocation/window gaps before any runtime access."""
    require(type(config) is dict and config.get('executionAllocated') is True, 'Execution is not allocated')
    require(type(config.get('version')) is int and config['version'] == 1 and config.get('scope') == 'synthetic-gpu-readback-host', 'Config identity')
    exact_keys(config.get('limits'), LIMITS, 'Exact seven proposed limits')
    require(all(type(config['limits'][k]) is int and config['limits'][k] == v for k,v in LIMITS.items()), 'Fixed integer resource bounds')
    require(type(now) is datetime.datetime and now.tzinfo is not None and now.utcoffset() == datetime.timedelta(0), 'UTC review admission time')
    start = utc_timestamp(config.get('notBeforeUTC'))
    stop = utc_timestamp(config.get('stopNewLaunchUTC'))
    review_start = utc_timestamp(config.get('reviewNotBeforeUTC'))
    review_stop = utc_timestamp(config.get('reviewStopNewLaunchUTC'))
    require(start < stop and review_start < review_stop, 'Nonempty allocated windows required')
    require(review_start <= now < review_stop, 'Outside allocated saved-review window')
    return {'diagnostic_start': start, 'diagnostic_stop': stop, 'review_start': review_start, 'review_stop': review_stop}


def read_bounded(root, relative, cap):
    """Read one regular contained file, bounded before and during the read."""
    require(type(cap) is int and 0 <= cap <= 33554432, 'Bounded read cap')
    root = Path(root)
    require(root.is_absolute() and root.resolve() == root, 'Canonical absolute evidence root')
    require(type(relative) is str, 'Text evidence path')
    rel = Path(relative)
    require(not rel.is_absolute() and '..' not in rel.parts and str(rel) == relative, 'Contained normalized evidence path')
    target = root / rel
    require(target.resolve() == target, 'No evidence symlink traversal')
    fd = os.open(target, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK)
    try:
        before = os.fstat(fd)
        require(stat.S_ISREG(before.st_mode) and before.st_size <= cap, 'Bounded regular evidence file')
        pieces = []
        remaining = cap + 1
        while remaining:
            part = os.read(fd, min(65536, remaining))
            if not part:
                break
            pieces.append(part)
            remaining -= len(part)
        data = b''.join(pieces)
        after = os.fstat(fd)
        require(len(data) <= cap and len(data) == before.st_size == after.st_size
                and before.st_mtime_ns == after.st_mtime_ns and before.st_ctime_ns == after.st_ctime_ns,
                'Stable exact bounded read')
        return data
    finally:
        os.close(fd)


def validate_page_claims(v):
    """Independently check bounded report consistency; never attest GPU phases."""
    exact_keys(v, TOP_KEYS, 'Page envelope keys')
    require(type(v['version']) is int and v['version'] == 1 and v['kind'] == 'synthetic-gpu-readback-envelope'
            and v['fixtureId'] == FIXTURE_ID, 'Page envelope identity')
    require(v['phaseEvidenceKind'] == 'page-self-report' and v['requiresIndependentPersistenceReview'] is True
            and v['scientificQualified'] is False and v['historicalFailureExplained'] is False and v['performanceClaim'] is False,
            'Page claim boundary')
    exact_keys(v['layout'], LAYOUT, 'Page layout keys')
    require(all(type(v['layout'][key]) is type(expected) and v['layout'][key] == expected for key, expected in LAYOUT.items()), 'Fixed page layout')
    exact_keys(v['context'], ['originLabel','isSecureContext','webgpuSupported'], 'Page context keys')
    require(v['context']['originLabel'] in ['page-origin','opaque-null','other-origin']
            and type(v['context']['isSecureContext']) is bool and type(v['context']['webgpuSupported']) is bool, 'Page context shape')
    require(v['status'] in ['candidate-readback','failed'] and type(v['eventOverflow']) is bool and type(v['failureOverflow']) is bool, 'Page status and overflow flags')
    if v['values'] is None:
        require(type(v['returnedByteLength']) is int and v['returnedByteLength'] == 0, 'No-byte page length')
    else:
        decode_byte_values(v['values'])
        require(type(v['returnedByteLength']) is int and v['returnedByteLength'] == 128, 'Page byte count')
    require(type(v['failures']) is list and len(v['failures']) <= 16 and all(code in FAILURES for code in v['failures']), 'Bounded page failure codes')
    exact_keys(v['counts'], COUNTS, 'Page operation count keys')
    counts = [v['counts'][key] for key in COUNTS]
    require(all(integer(n, 1) for n in counts) and counts == sorted(counts, reverse=True)
            and counts[-1] == (0 if v['values'] is None else 1), 'Page single-operation count relationships')
    o = v['observation']; exact_keys(o, OBS_KEYS, 'Page observation keys')
    require(o['adapterAvailable'] is None or type(o['adapterAvailable']) is bool, 'Adapter availability shape')
    require(type(o['isFallbackAdapter']) is bool or o['isFallbackAdapter'] == 'unavailable', 'Fallback observation shape')
    require(all(type(o[key]) is bool for key in OBS_BOOL), 'Boolean page observations')
    require(all(o[key] is None or integer(o[key], 4096) for key in OBS_LENGTH), 'Bounded page length observations')
    require(all(o[key] is None or type(o[key]) is bool for key in ['ownedIndependent','rangeDetached']), 'Ownership flag shape')
    require(o['mapStateAtCopy'] in [None,'mapped','unmapped','pending','other'], 'Map state shape')
    require(all(o[key] in ['not-observed','destroyed','unknown','other'] for key in ['lossBeforeDestroySnapshot','deviceLostReason']), 'Loss observation enums')
    comp = [o[key] for key in ['compilationErrors','compilationWarnings','compilationInfos']]
    require(all(integer(n, 64) for n in comp) and sum(comp) <= 64, 'Compilation observation cap')
    require(type(o['uncapturedErrorKinds']) is list and len(o['uncapturedErrorKinds']) <= 8
            and all(kind in ['validation','out-of-memory','internal','other'] for kind in o['uncapturedErrorKinds']), 'Uncaptured error cap')
    require(type(o['scopes']) is list and len(o['scopes']) == 3, 'Three error scopes')
    for scope, filter_name in zip(o['scopes'], ['out-of-memory','internal','validation']):
        exact_keys(scope, ['filter','state','errorKind'], 'Scope keys')
        require(scope['filter'] == filter_name and scope['state'] in ['unpushed','pushed','popped','unresolved']
                and scope['errorKind'] in [None,'validation','out-of-memory','internal','other']
                and (scope['state'] == 'popped' or scope['errorKind'] is None), 'Scope state consistency')
    require(v['lastWorkStage'] in ['entered','adapter-requested','device-requested','buffers-created','shader-created',
                                  'pipeline-requested','submitted','map-requested','mapped','owned-copy-made']
            and finite(v['browserElapsedMilliseconds'], 60000), 'Page stage and time bounds')
    events = v['events']; require(type(events) is list and 1 <= len(events) <= 64, 'Page event cap')
    stages = []; prior_time = 0; cursor = 0
    for index, event in enumerate(events, 1):
        exact_keys(event, ['sequence','stage','browserMilliseconds'], 'Page event keys')
        require(type(event['sequence']) is int and event['sequence'] == index and event['stage'] in STAGES + EXTRA_STAGES,
                'Page event identity')
        require(finite(event['browserMilliseconds'], v['browserElapsedMilliseconds']) and event['browserMilliseconds'] >= prior_time, 'Page clock ordering')
        prior_time = event['browserMilliseconds']; stage = event['stage']; stages.append(stage)
        if stage not in EXTRA_STAGES:
            require(stage in STAGES[cursor:], 'Page phase subsequence')
            cursor = STAGES.index(stage, cursor) + 1
    require(stages[0] == 'entered' and (v['eventOverflow'] or stages[-1] == 'return-envelope-ready'), 'Page report boundaries')
    require(not v['eventOverflow'] or len(events) == 64, 'Page event-overflow accounting')
    require(not v['failureOverflow'] or len(v['failures']) == 16, 'Page failure-overflow accounting')
    require(not o['uncapturedErrorOverflow'] or len(o['uncapturedErrorKinds']) == 8, 'Page uncaptured-overflow accounting')
    if not v['eventOverflow']:
        operation_stages = ['adapter-requested','device-requested','sentinels-queued','pipeline-requested','dispatch-encoded',
                            'readback-copy-encoded','submitted','map-requested','owned-copy-made','owned-values-created']
        require(all(v['counts'][key] == stages.count(stage) for key, stage in zip(COUNTS, operation_stages)), 'Page counts versus reported events')
        require(stages.count('scope-pushed') == sum(s['state'] != 'unpushed' for s in o['scopes'])
                and stages.count('scope-popped') == sum(s['state'] == 'popped' for s in o['scopes'])
                and 'cleanup-started' in stages and stages.count('work-failed') <= 1, 'Page cleanup/scope event relationships')
        for key, stage in [('limitsAdmitted','limits-admitted'),('unmapSucceeded','unmap-returned'),('storageDestroyed','storage-destroy-returned'),
                           ('readbackDestroyed','readback-destroy-returned'),('deviceDestroyAttempted','device-destroy-intent'),
                           ('deviceDestroySucceeded','device-destroy-returned'),('expectedDestroyLossObserved','expected-destroy-loss'),
                           ('unexpectedDeviceLoss','unexpected-device-loss')]:
            require(o[key] == (stage in stages), 'Page observed flag versus reported event')
    require(not v['counts']['deviceRequests'] or (o['adapterAvailable'] is True and o['isFallbackAdapter'] is False), 'Nonfallback device admission report')
    require(not v['counts']['initializationWrites'] or o['limitsAdmitted'], 'Reported limits precede initialization')
    require(not o['deviceDestroySucceeded'] or o['deviceDestroyAttempted'], 'Reported device destruction attempt')
    require(o['lossBeforeDestroySnapshot'] == 'not-observed' or o['unexpectedDeviceLoss'], 'Pre-destroy loss cannot be expected')
    require(not o['expectedDestroyLossObserved'] or (o['deviceDestroyAttempted'] and o['deviceLostReason'] == 'destroyed'
            and not o['unexpectedDeviceLoss'] and o['lossBeforeDestroySnapshot'] == 'not-observed'), 'Expected-loss report consistency')
    require(not o['unexpectedDeviceLoss'] or 'unexpected-device-loss' in v['failures'] or v['failureOverflow'], 'Unexpected-loss failure evidence')
    require(o['rangeDetached'] is None or (o['mappedByteLengthAfterUnmap'] is not None
            and o['rangeDetached'] == (o['mappedByteLengthAfterUnmap'] == 0)), 'Reported detachment consistency')
    require(not v['counts']['ownedCopies'] or (o['ownedIndependent'] is True and o['ownedByteLengthBeforeRelease'] == 128
            and o['mappedByteLengthBeforeUnmap'] == 128 and o['mapStateAtCopy'] == 'mapped'), 'Reported mapped copy shape')
    require(v['values'] is None or (o['unmapSucceeded'] and o['storageDestroyed'] and o['readbackDestroyed']
            and o['deviceDestroySucceeded'] and o['ownedByteLengthAfterRelease'] == 128), 'Reported release precedes values')
    require(not o['pendingAdapterRequest'] or (v['counts']['adapterRequests'] == 1 and o['adapterAvailable'] is None), 'Pending adapter report')
    require(not o['pendingDeviceRequest'] or (v['counts']['deviceRequests'] == 1 and not o['deviceDestroyAttempted']), 'Pending device report')
    require(not o['pendingMapRequest'] or (v['counts']['mapRequests'] == 1 and v['counts']['ownedCopies'] == 0), 'Pending map report')
    require(not o['pendingWork'] or (v['counts']['initializationWrites'] == 1 and v['counts']['dispatchEncodes'] == 0), 'Pending work report')
    if v['status'] == 'candidate-readback':
        require(v['context'] == {'originLabel':'page-origin','isSecureContext':True,'webgpuSupported':True}
                and v['values'] is not None and v['failures'] == [] and not v['eventOverflow'] and not v['failureOverflow'], 'Candidate context/failures')
        require(counts == [1] * len(COUNTS) and stages == STAGES and o['adapterAvailable'] is True and o['isFallbackAdapter'] is False
                and o['limitsAdmitted'] and o['compilationErrors'] == 0, 'Candidate operation/event report')
        require([o[key] for key in OBS_LENGTH] == [128,0,128,128] and o['ownedIndependent'] is True and o['rangeDetached'] is True, 'Candidate ownership report')
        require(all(o[key] for key in ['unmapSucceeded','storageDestroyed','readbackDestroyed','deviceDestroyAttempted','deviceDestroySucceeded',
                                       'expectedDestroyLossObserved']) and o['lossBeforeDestroySnapshot'] == 'not-observed'
                and o['deviceLostReason'] == 'destroyed' and not o['unexpectedDeviceLoss'], 'Candidate cleanup/loss report')
        require(all(s['state'] == 'popped' and s['errorKind'] is None for s in o['scopes']) and not o['uncapturedErrorKinds']
                and not any(o[key] for key in ['uncapturedErrorOverflow','pendingAdapterRequest','pendingDeviceRequest','pendingMapRequest','pendingWork','cleanupDeadlineExceeded'])
                and v['lastWorkStage'] == 'owned-copy-made' and v['browserElapsedMilliseconds'] < 10000, 'Candidate unresolved evidence')
    else:
        require(bool(v['failures']) or v['failureOverflow'] or v['eventOverflow'], 'Failed page report requires bounded reason')
    return {'status':v['status'], 'values':v['values'], 'candidateByPageSelfReport':v['status'] == 'candidate-readback',
            'failureCodes':v['failures'], 'phaseEvidenceKind':'page-self-report', 'gpuExecutionIndependentlyAttested':False}
