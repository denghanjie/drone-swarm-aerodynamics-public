"""One work/check attempt; no scientific imports. Disabled until reviewed/published."""
import time
START = time.monotonic()
from pathlib import Path
import datetime, hashlib, json, os, resource, secrets, subprocess, sys

PACKAGE = Path(__file__).resolve().parents[1]
ROOT = PACKAGE.parents[1]
NAME = 'research/m31-native-tree-design-2026-10-17'
STAGES = ('work', 'check')
FILE_CAP, TOTAL_CAP, REPORT_CAP = 32*1024**2, 128*1024**2, 1024**2
TOTAL_SECONDS, OVERHEAD_SECONDS = 180, 15
DEADLINE = START + TOTAL_SECONDS
UTC_CUTOFF = None

def need(value, code):
    if not value: raise ValueError(code)

def guard():
    need(time.monotonic() < DEADLINE and (UTC_CUTOFF is None or datetime.datetime.now(datetime.timezone.utc) < UTC_CUTOFF), 'total-wall-deadline')
def utc(): return datetime.datetime.now(datetime.timezone.utc).isoformat()

def identity(file):
    h, size = hashlib.sha256(), 0
    with file.open('rb') as stream:
        for block in iter(lambda: stream.read(1024*1024), b''):
            guard(); h.update(block); size += len(block)
    return {'bytes':size, 'sha256':h.hexdigest()}

def load(file):
    need(file.stat().st_size <= FILE_CAP, 'json-byte-cap')
    return json.loads(file.read_bytes())

def safe(relative):
    need(isinstance(relative,str) and relative and not Path(relative).is_absolute() and '..' not in Path(relative).parts, 'relative-source-path')
    file = ROOT/relative
    need(file.resolve() == file and file.is_file() and file.is_relative_to(ROOT), 'source-location')
    return file

def verify(pin):
    need(identity(safe(pin['path'])) == {key:pin[key] for key in ('bytes','sha256')}, 'pin-identity')

def durable(file, value, first=False):
    raw = (json.dumps(value,allow_nan=False,separators=(',',':'))+'\n').encode()
    need(len(raw) <= REPORT_CAP, 'attempt-byte-cap')
    temporary = file if first else file.with_name(file.name+'.tmp')
    with temporary.open('xb') as stream:
        stream.write(raw); stream.flush(); os.fsync(stream.fileno())
    if not first: os.replace(temporary,file)
    fd = os.open(file.parent,os.O_RDONLY)
    try: os.fsync(fd)
    finally: os.close(fd)

def authorize(config):
    need(config['schema'] == 'm31-native-tree-supervision-v1' and config['executionAllowed'] is True, 'execution-not-authorized')
    a = config['authorization']
    need(isinstance(a,dict) and set(a) == {'id','approvedUtc','reviewedSourceManifestSha256'} and isinstance(a['id'],str) and 1 <= len(a['id']) <= 128, 'authorization-incomplete')
    draft = a['reviewedSourceManifestSha256']
    need(isinstance(draft,str) and len(draft) == 64 and all(c in '0123456789abcdef' for c in draft), 'reviewed-draft-pin')
    cutoff = datetime.datetime.fromisoformat(config['launchCutoffUtc'])
    approved = datetime.datetime.fromisoformat(a['approvedUtc'])
    now = datetime.datetime.now(datetime.timezone.utc)
    need(cutoff.tzinfo is not None and approved.tzinfo is not None and approved <= now < cutoff, 'authorization-window')
    return cutoff

def usage(bases):
    total = 0
    for base in bases:
        if base is None or not base.exists(): continue
        for file in base.rglob('*'):
            guard(); st = file.lstat(); need(not file.is_symlink(), 'output-symlink')
            if not file.is_dir():
                need(file.is_file() and st.st_size <= FILE_CAP, 'per-file-byte-cap')
                total += st.st_size
    # Both the final report and its temporary replacement fit inside the cap.
    need(total+2*REPORT_CAP <= TOTAL_CAP, 'combined-output-log-scratch-cap')
    return total

def assertions(value, expected):
    for dotted,wanted in expected.items():
        found = value
        for part in dotted.split('.'): found = found[part]
        need(type(found) is type(wanted) and found == wanted, 'completion-assertion:'+dotted)

def limits(seconds):
    def apply():
        resource.setrlimit(resource.RLIMIT_CPU,(seconds,seconds+1))
        resource.setrlimit(resource.RLIMIT_FSIZE,(FILE_CAP,FILE_CAP))
    return apply

def preserved(pins, protected, prior):
    for pin in pins: verify(pin)
    for relative,pin in {**protected,**prior}.items():
        need(identity(safe(relative)) == pin, 'prior-artifact-preserved')

def snapshot(results, attempt_path):
    found = {}
    for file in results.rglob('*'):
        need(not file.is_symlink(), 'result-symlink')
        if file.is_file() and file != attempt_path:
            found[str(file.relative_to(ROOT))] = identity(file)
    return found

def failure(error):
    message = str(error)
    code = message if message.replace('-','').replace(':','').isalnum() and len(message) <= 120 else 'supervision-failure'
    return {'type':type(error).__name__, 'code':code}

def main(expected, commit):
    global DEADLINE, UTC_CUTOFF
    need(PACKAGE == ROOT/NAME and len(expected) == 64 and len(commit) == 40 and all(c in '0123456789abcdef' for c in expected+commit), 'arguments')
    # Sole entry: disabled config stops before any output, marker or child spawn.
    config = load(PACKAGE/'config.json'); cutoff = authorize(config)
    UTC_CUTOFF = cutoff
    remaining = (cutoff-datetime.datetime.now(datetime.timezone.utc)).total_seconds()
    need(remaining >= TOTAL_SECONDS, 'full-reservation-unavailable')
    DEADLINE = min(DEADLINE,time.monotonic()+remaining)
    need(config['stageOrder'] == list(STAGES), 'stage-order')
    need(config['limits'] == {'perFileBytes':FILE_CAP,'combinedOutputLogScratchBytes':TOTAL_CAP,'totalWallSeconds':180,'closureAndOverheadSeconds':15,'pollSeconds':0.1,'finalizationByteAllowance':2*REPORT_CAP}, 'limits')
    need([config['stages'][stage]['childWallSeconds'] for stage in STAGES] == [120,45], 'stage-allocations')
    need(sys.platform == 'darwin' and os.environ.get('RESEARCH_EXECUTION_CONTEXT') == 'tool-require-escalated', 'dispatch-context')
    need(not os.environ.get('NODE_OPTIONS') and not os.environ.get('NODE_PATH') and sys.flags.isolated == 1 and sys.flags.dont_write_bytecode == 1 and sys.flags.optimize == 0, 'runtime-flags')
    results = PACKAGE/'results'; need(not results.exists(), 'single-use-results-no-retry'); results.mkdir()
    attempt_path = results/'run-attempt.json'; token = secrets.token_hex(32)
    attempt = {'schema':'m31-native-tree-attempt-v1','sourceManifestSha256':expected,'sourceCommit':commit,
        'runTokenSha256':hashlib.sha256(token.encode()).hexdigest(),'startedUtc':utc(),'status':'running',
        'stageOrder':list(STAGES),'stages':{},'firstFailure':None,'memoryLimitClaim':False,'executionRetries':0}
    durable(attempt_path,attempt,True)
    pins, protected, prior = [], {}, {}
    private = process = child_start = active_record = None
    child_total, code = 0.0, 1
    try:
        mf = PACKAGE/'source-manifest.json'; mid = identity(mf); need(mid['sha256'] == expected, 'manifest-sha')
        manifest = load(mf); pins = manifest['files']; by_path = {p['path']:p for p in pins}
        need(len(by_path) == len(pins), 'duplicate-pins')
        for pin in pins: verify(pin)
        required = ['config.json','runtime.json','source/run.py','source/harness.cjs','source/check.py','source/cases.json',
                    'source/native-load.cjs','source/kernel.cjs','source/tree.cjs']
        for relative in required: need(NAME+'/'+relative in by_path, 'supervisor-source-closure')
        need(load(PACKAGE/'config.json') == config, 'config-preservation')
        old = 'research/m31-native-fresh-transfer-2026-10-17/source/'
        for relative in ['native-load.cjs','vendor/kernel.cjs','vendor/anchor-kernel.cjs','vendor/lean-anchor.cjs','vendor/reference-excerpt.cjs']:
            need(old+relative in by_path, 'original-F-source-closure')
        runtime = load(PACKAGE/'runtime.json')
        for kind,exe in [('python',Path(sys.executable).resolve()),('node',Path(os.environ['RESEARCH_NODE']).resolve())]:
            expected_runtime = {key:manifest['runtime'][kind][key] for key in ('bytes','sha256')}
            need(identity(exe) == expected_runtime and {key:runtime[kind][key] for key in ('bytes','sha256')} == expected_runtime, 'runtime-'+kind)
        need(runtime['platform'] == sys.platform and runtime['architecture'] == os.uname().machine and runtime['python']['version'] == sys.version, 'runtime-platform-version')
        publication_file = PACKAGE/'source-publication.json'; publication = load(publication_file)
        need(publication['commit'] == commit and publication['manifestSha256'] == expected and publication['manifestPath'] == NAME+'/source-manifest.json' and
             publication['manifestBytes'] == mid['bytes'] and publication['verifiedFilePins'] == len(pins) and publication['remoteBytesEqualLocal'] is True and
             publication['committedBytesEqualLocal'] is True and datetime.datetime.fromisoformat(publication['verifiedUtc']) <= datetime.datetime.fromisoformat(attempt['startedUtc']), 'publication-binding')
        protected = {NAME+'/source-manifest.json':mid,NAME+'/source-publication.json':identity(publication_file)}
        candidate = Path(os.environ['RESEARCH_PRIVATE_LOG_DIR'])
        need(candidate.is_absolute() and candidate.resolve() == candidate and not candidate.is_relative_to(ROOT) and not candidate.exists(), 'fresh-private-directory')
        candidate.mkdir(parents=True,exist_ok=False); private = candidate
        attempt['privateDirectoryIdentitySha256'] = hashlib.sha256(str(private).encode()).hexdigest()
        attempt['verifiedPins'] = len(pins)
        for stage in STAGES:
            guard(); authorize(config); need(time.monotonic()-START-child_total < OVERHEAD_SECONDS, 'shared-overhead-deadline')
            preserved(pins,protected,prior)
            entry = config['stages'][stage]
            expected_source = NAME+'/source/'+('harness.cjs' if stage == 'work' else 'check.py')
            need(entry['source'] == expected_source and entry['runtime'] == ('node' if stage == 'work' else 'python'), 'stage-source-runtime')
            output = results/(stage+'.json'); need(not output.exists(), 'exclusive-stage-output')
            record = {'status':'started','startedUtc':utc(),'childWallLimitSeconds':entry['childWallSeconds']}
            attempt['stages'][stage] = record; active_record = record; durable(attempt_path,attempt)
            env = dict(os.environ)
            # Python checker uses this host's monotonic clock. Node receives only
            # a duration and starts its own performance.now() deadline.
            child_start = time.monotonic(); child_deadline = min(DEADLINE,child_start+entry['childWallSeconds'])
            env.update(RESEARCH_STAGE=stage,RESEARCH_RUN_TOKEN=token,RESEARCH_CHILD_BUDGET_MILLISECONDS=str(entry['childWallSeconds']*1000),
                RESEARCH_CHILD_DEADLINE_MONOTONIC_NS=str(int(child_deadline*1e9)),RESEARCH_TOTAL_DEADLINE_MONOTONIC_NS=str(int(DEADLINE*1e9)))
            exe = str(Path(sys.executable).resolve()) if stage == 'check' else os.environ['RESEARCH_NODE']
            command = [exe]+(['-I','-B'] if stage == 'check' else [])+[str(ROOT/entry['source']),str(ROOT),expected,commit]
            log_path = private/(stage+'.log'); authorize(config); guard()
            with log_path.open('xb') as log:
                process = subprocess.Popen(command,cwd=ROOT,stdin=subprocess.DEVNULL,stdout=log,stderr=subprocess.STDOUT,env=env,preexec_fn=limits(entry['childWallSeconds']))
                while True:
                    guard(); need(time.monotonic() < child_deadline, 'child-wall-deadline'); usage([results,private])
                    child_code = process.poll()
                    if child_code is not None: break
                    time.sleep(min(.1,max(0,child_deadline-time.monotonic())))
                process.wait(); process = None
            elapsed = time.monotonic()-child_start; child_total += elapsed; child_start = None
            record.update(finishedUtc=utc(),wallSeconds=elapsed,exitCode=child_code)
            need(elapsed <= entry['childWallSeconds'], 'stage-allocation-exceeded')
            need(child_code == 0, 'child-exit-'+stage)
            value = load(output); assertions(value,entry['completionAssertions'])
            need(value['sourceCommit'] == commit and value['sourceManifestSha256'] == expected, 'stage-source-binding')
            # Reverify earlier artifacts BEFORE replacing the snapshot. A stage
            # cannot change prior bytes and have the new snapshot bless them.
            preserved(pins,protected,prior); prior = snapshot(results,attempt_path)
            record.update(status='completed',output=identity(output),privateLog=dict(identity(log_path),published=False))
            durable(attempt_path,attempt)
        code = 0
    except Exception as error:
        attempt['firstFailure'] = failure(error)
        if active_record is not None and active_record['status'] == 'started': active_record['status'] = 'failed'
    finally:
        if process is not None:
            try:
                if process.poll() is None: process.kill()
                process.wait(timeout=min(2,max(.01,DEADLINE-time.monotonic())))
                attempt['failedOwnedChildReaped'] = True
            except Exception as error: attempt['cleanupFailure'] = failure(error); code = 1
        if child_start is not None:
            elapsed = time.monotonic()-child_start; child_total += elapsed
            if active_record is not None: active_record.update(status='failed',finishedUtc=utc(),wallSeconds=elapsed)
        try:
            preserved(pins,protected,prior)
            attempt['preservationPassed'] = bool(pins and protected)
            attempt['retainedOutputs'] = snapshot(results,attempt_path)
            if private is not None:
                attempt['privateLogs'] = {stage:dict(identity(private/(stage+'.log')),published=False)
                    for stage in STAGES if (private/(stage+'.log')).is_file()}
            attempt['outputLogScratchBytes'] = usage([results,private])
            need(time.monotonic()-START-child_total <= OVERHEAD_SECONDS, 'shared-overhead-deadline'); guard()
        except Exception as error: attempt['finalizationFailure'] = failure(error); code = 1
        attempt.update(status='completed' if code == 0 and attempt.get('preservationPassed') else 'failed',finishedUtc=utc(),
            preFinalReportWallSeconds=time.monotonic()-START,stageWallSeconds=child_total,overheadAndClosureSeconds=time.monotonic()-START-child_total,
            supervisorProcessLifetimePeakRssBytes=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
            peakRssScope='macOS ru_maxrss bytes for supervisor process lifetime only; no stage, child-tree aggregate or OS memory ceiling claim',
            supervisorExitVerified=False,
            timingScope='Entry through pre-final-report timestamp. Final fsync and interpreter exit occur later; post-write deadline checked, no exact process-exit duration claim. Caller must also observe this supervisor exit code')
        durable(attempt_path,attempt)
        need(time.monotonic() <= DEADLINE and datetime.datetime.now(datetime.timezone.utc) <= cutoff, 'post-report-total-deadline')
    return 0 if attempt['status'] == 'completed' else 1

if __name__ == '__main__':
    need(len(sys.argv) == 3, 'usage-run.py-MANIFEST_SHA-SOURCE_COMMIT')
    raise SystemExit(main(*sys.argv[1:]))
