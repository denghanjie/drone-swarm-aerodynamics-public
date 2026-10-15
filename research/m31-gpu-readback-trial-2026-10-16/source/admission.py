"""Pure admission logic plus bounded config-only reader. No operational imports."""
import datetime
import json
import re
import stat

LIMITS = {'wallSeconds': 60, 'workerSeconds': 40, 'evaluateSeconds': 12,
          'cleanupSeconds': 58, 'combinedBytes': 8388608,
          'ownedRSSBytes': 2147483648, 'traceEvents': 2048}


def admit(config, phase, now):
    """Validate an explicit future allocation. No authorization is inferred."""
    if type(config) is not dict or config.get('executionAllocated') is not True:
        raise ValueError('No execution allocation')
    if type(config.get('version')) is not int or config['version'] != 1 or config.get('scope') != 'synthetic-gpu-readback-host':
        raise ValueError('Config identity required')
    if phase not in ('launch', 'review'):
        raise ValueError('Unknown phase')
    if type(config.get('limits')) is not dict or config['limits'] != LIMITS:
        raise ValueError('Exact proposed limits required')
    if any(type(config['limits'][key]) is not int for key in LIMITS):
        raise ValueError('Integer limits required')
    values = []
    for key in ('notBeforeUTC', 'stopNewLaunchUTC', 'reviewNotBeforeUTC', 'reviewStopNewLaunchUTC'):
        value = config.get(key)
        if type(value) is not str or not re.fullmatch(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z', value):
            raise ValueError('Explicit whole-second UTC windows required')
        values.append(datetime.datetime.strptime(value, '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=datetime.timezone.utc))
    if not values[0] < values[1] or not values[2] < values[3]:
        raise ValueError('Windows must have positive duration')
    if not isinstance(now, datetime.datetime) or now.tzinfo is None or now.utcoffset() != datetime.timedelta(0):
        raise ValueError('UTC admission clock required')
    start, end = values[:2] if phase == 'launch' else values[2:]
    if not start <= now < end:
        raise ValueError('Outside allocated window')
    return True


def admit_file(path, phase):
    """Read configuration only; no experiment artifact or process is touched."""
    info = path.lstat()
    if not stat.S_ISREG(info.st_mode) or info.st_size > 16384:
        raise ValueError('Bounded regular config required')
    with path.open('rb') as handle:
        data = handle.read(16385)
    if len(data) > 16384:
        raise ValueError('Config growth cap')
    config = json.loads(data)
    admit(config, phase, datetime.datetime.now(datetime.timezone.utc))
    return config
