"""One-use, data-only admission audit; third-party content is never executed."""
from pathlib import Path
import base64
import csv
import datetime as dt
import hashlib
import io
import json
import math
import signal
import statistics
import sys
import time
import urllib.request

FILES = [
    ('cf50_04.csv', 'c051cf74a9ae9eeedb17594466b5a95ddaecbfb0', 4826012),
    ('cf51_04.csv', '2041927f90fbde571d778997437c00badc9b626d', 4789240),
    ('cf50_05.csv', '9ceeae04af8b9da281be65b172bd992deb3cb425', 4885916),
    ('cf51_05.csv', '136780f868e09ab29ac1a0311d96c4ecc0639c93', 4797542),
]
HEADER = 'time[ms],x[m],y[m],z[m],vx[m/s],vy[m/s],vz[m/s],ax[m/s^2],ay[m/s^2],az[m/s^2],qx,qy,qz,qw,u1[N],u2[N],u3[N],u4[N],u1[PWM],u2[PWM],u3[PWM],u4[PWM],Vbat[V],thrust_des[g],torquex[Nm],torquey[Nm],torquez[Nm],wx[rad/s],wy[rad/s],wz[rad/s]'
SCALES = [('header_ms', 1000), ('preprocessing_us', 1000000)]

def utc():
    return dt.datetime.now(dt.timezone.utc).isoformat()

def write_new(path, obj):
    data = (json.dumps(obj, indent=2, allow_nan=False) + '\n').encode()
    assert len(data) < 1024 * 1024
    with path.open('xb') as f:
        f.write(data)

def identity(data):
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}

def preserve(root):
    p = root / 'research/m31-native-fresh-transfer-2026-10-17/result-manifest.json'
    data = p.read_bytes()
    assert hashlib.sha256(data).hexdigest() == '5b2188c33904b612a56056050c6b575404e0c9df539fd75c0bff84d2dee39a89'
    m = json.loads(data)
    assert len(m['files']) == 547
    for x in m['files']:
        b = (root / x['path']).read_bytes()
        assert identity(b) == {k: x[k] for k in ('bytes', 'sha256')}, x['path']
    return 547

def describe(data, progress=None):
    progress = {} if progress is None else progress
    progress['structuralEligible'] = False
    progress['physicalLabelAdmitted'] = False
    text = data.decode('utf-8')
    lines = text.splitlines()
    progress['schemaMatches'] = bool(lines) and lines[0].lstrip('# ').strip() == HEADER
    assert progress['schemaMatches'], 'schema mismatch'
    rows = []
    for row in csv.reader(lines[1:]):
        progress['parsingDataRow'] = len(rows) + 1
        rows.append([float(x) for x in row])
    progress.pop('parsingDataRow', None)
    progress['rows'] = len(rows)
    progress['observedColumnCounts'] = sorted(set(len(r) for r in rows))
    assert len(rows) >= 2 and all(len(r) == 30 for r in rows), 'shape'
    finite = sum(math.isfinite(x) for r in rows for x in r)
    progress['finiteValues'] = finite
    progress['nonfiniteValues'] = 30 * len(rows) - finite
    assert finite == 30 * len(rows), 'nonfinite data: no implicit cleanup'
    times = [r[0] for r in rows]
    intervals = [b-a for a,b in zip(times,times[1:])]
    positive = all(x > 0 for x in intervals)
    norms = [math.sqrt(math.fsum(x*x for x in r[10:14])) for r in rows]
    pwm = [x for r in rows for x in r[18:22]]
    quat_error = max(abs(x-1) for x in norms)
    scale_results = {}
    for label, divisor in SCALES:
        squared = []
        for a,b,delta in zip(rows,rows[1:],intervals):
            if delta > 0:
                for i in range(3):
                    e = (b[1+i]-a[1+i])/(delta/divisor)-(a[4+i]+b[4+i])/2
                    squared.append(e*e)
        scale_results[label] = {
            'durationSeconds': (times[-1]-times[0])/divisor,
            'medianIntervalSeconds': statistics.median(intervals)/divisor,
            'positionVelocityComponentRmseMps': math.sqrt(math.fsum(squared)/len(squared)) if squared else None,
            'comparedComponents': len(squared),
        }
    return {
        'rows': len(rows), 'columns': 30, 'finiteValues': finite,
        'rawTimeStart': times[0], 'rawTimeEnd': times[-1],
        'rawIntervals': {'min':min(intervals),'median':statistics.median(intervals),'max':max(intervals),'nonpositive':sum(x<=0 for x in intervals)},
        'timeScales': scale_results,
        'quaternionNorm': {'min':min(norms),'max':max(norms),'maxAbsError':quat_error},
        'pwmRange': [min(pwm),max(pwm)],
        'batteryRangeV': [min(r[22] for r in rows),max(r[22] for r in rows)],
        'accelerationRanges': [[min(r[i] for r in rows),max(r[i] for r in rows)] for i in range(7,10)],
        'firmwareForceRanges': [[min(r[i] for r in rows),max(r[i] for r in rows)] for i in range(14,18)],
        'structuralEligible': positive and min(pwm)>=0 and max(pwm)<=1 and quat_error<=.01,
        'physicalLabelAdmitted': False,
    }

def main():
    root, private, original = map(Path, sys.argv[1:4])
    package = Path(__file__).resolve().parent
    assert dt.datetime.now(dt.timezone.utc) < dt.datetime(2026,10,17,3,tzinfo=dt.timezone.utc), 'launch cutoff'
    assert not private.exists(), 'private attempt directory must be new'
    assert not (package/'attempt.json').exists() and not (package/'results.json').exists()
    write_new(package/'STARTED.json', {'utc':utc(),'source':identity(Path(__file__).read_bytes()),'scope':'one data admission attempt; no physical scoring'})
    start = time.monotonic()
    def timeout(signum, frame):
        raise TimeoutError('600 second audit cap')
    signal.signal(signal.SIGALRM, timeout)
    signal.alarm(600)
    attempt = {'startedUtc':utc(),'status':'running','newScientificSimulationCalls':0,'modelScores':0}
    results = {'schema':'m31-physical-data-admission-v1','files':{},'pairs':{},'physicalEvidenceAdmitted':False}
    try:
        attempt['protectedBefore'] = preserve(root)
        private.mkdir()
        for name, blob, size in FILES:
            attempt['activeFile'] = name
            attempt['phase'] = 'acquire-and-verify'
            record = {'gitBlob':blob, 'declaredBytes':size, 'structuralEligible':False, 'physicalLabelAdmitted':False}
            results['files'][name] = record
            if name == 'cf50_04.csv':
                data = original.read_bytes()
                transport = 'verified prior private copy'
            else:
                url = 'https://api.github.com/repos/aerorobotics/neural-swarm/git/blobs/'+blob
                with urllib.request.urlopen(url, timeout=30) as response:
                    body = response.read(7*1024*1024+1)
                assert len(body)<=7*1024*1024, 'response cap'
                obj = json.loads(body)
                assert obj['sha']==blob and obj['encoding']=='base64'
                data = base64.b64decode(obj['content'])
                transport = 'HTTPS GitHub immutable blob; verified TLS'
            assert len(data)==size
            assert hashlib.sha1(b'blob '+str(size).encode()+b'\0'+data).hexdigest()==blob, 'Git identity'
            with (private/name).open('xb') as f:
                f.write(data)
            assert sum(f.stat().st_size for f in private.iterdir() if f.is_file())<=32*1024*1024
            record.update({**identity(data),'transport':transport})
            attempt['phase'] = 'describe-complete-file'
            record.update(describe(data, progress=record))
            write_new(private/(name+'.audit.json'), record)
        attempt.pop('activeFile', None)
        attempt['phase'] = 'pair-clock-descriptors'
        for run in ['04','05']:
            a,b = [results['files']['cf'+vehicle+'_'+run+'.csv'] for vehicle in ['50','51']]
            ordered = all(x['rawIntervals']['nonpositive'] == 0 for x in [a,b])
            raw_overlap=max(0,min(a['rawTimeEnd'],b['rawTimeEnd'])-max(a['rawTimeStart'],b['rawTimeStart']))
            results['pairs'][run] = {
                'rawStartDifferenceCf51MinusCf50':b['rawTimeStart']-a['rawTimeStart'],
                'clockDescriptorsEligible':ordered,
                'rawClockOverlap':{label:raw_overlap/divisor if ordered else None for label,divisor in SCALES},
                'independentlyRezeroedOverlap':{label:min(a['timeScales'][label]['durationSeconds'],b['timeScales'][label]['durationSeconds']) if ordered else None for label,divisor in SCALES},
                'synchronizationEstablished':False,
            }
        results['allStructurallyEligible']=all(x['structuralEligible'] for x in results['files'].values())
        write_new(package/'results.json', results)
        attempt['status']='completed'
        attempt['result']=identity((package/'results.json').read_bytes())
    except BaseException as e:
        attempt['status']='failed'
        attempt['errorType']=type(e).__name__
        if isinstance(e, AssertionError) and str(e) in ['schema mismatch', 'shape', 'nonfinite data: no implicit cleanup', 'response cap', 'Git identity']:
            attempt['reason']=str(e)
        # Omit exception strings that could contain private paths or network metadata.
        write_new(package/'partial-results.json',results)
    finally:
        try:
            if time.monotonic()-start >= 600:
                raise TimeoutError('audit deadline already reached')
            attempt['protectedAfter']=preserve(root)
        except BaseException:
            attempt['status']='failed'
            attempt['preservationFailure']=True
        attempt['wallSeconds']=time.monotonic()-start
        attempt['completedUtc']=utc()
        attempt['privateBytes']=sum(f.stat().st_size for f in private.iterdir() if f.is_file()) if private.exists() else 0
        write_new(package/'attempt.json',attempt)
        signal.alarm(0)
    print(json.dumps(attempt))
    return 0 if attempt['status']=='completed' else 1

if __name__ == '__main__':
    raise SystemExit(main())
