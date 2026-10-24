"""Single-use administrative public-byte recovery; never imports scientific code."""
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path, PurePosixPath
from urllib.parse import quote
import argparse
import datetime
import hashlib
import json
import os
import re
import selectors
import signal
import sys
import subprocess
import threading
import time

ROOT = Path(__file__).resolve().parents[2]
REL = 'research/m31-native-factor-reuse-2026-10-23'
BASE = 'research/publication-receipts/m31-native-factor-reuse-source-public-review-2026-10-23'
REC = BASE + '-recovery-v2'
COMMIT = '7e6ab5b1d3bb819a7a17178c9a5636bde49ca6f2'
REPO = 'denghanjie/drone-swarm-aerodynamics-public'
BOUNDS = {'maxConcurrentTransfers': 2, 'attemptsPerFile': 2,
          'connectSeconds': 10, 'secondsPerAttempt': 90, 'overallSeconds': 900,
          'secondsPerLocalOperation': 45, 'localOperationCapturedBytes': 2097152,
          'aggregateCapturedPublicBytes': 536870912, 'maxPublicRequests': 16}
START = time.monotonic()
MUTEX = threading.Lock()
STOP = threading.Event()
EVENTS = []
CAPTURED = REQUESTS = 0
JOURNAL_READY = False
ROUTES = {}
JOURNAL = ROOT / (REC + '-events.jsonl')
ENV = {k: v for k, v in os.environ.items() if k not in ('GH_DEBUG', 'DEBUG', 'GIT_EXTERNAL_DIFF', 'GIT_DIFF_OPTS', 'GIT_PAGER')}
ENV.update(GIT_NO_REPLACE_OBJECTS='1', GIT_TERMINAL_PROMPT='0',
           GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL='/dev/null',
           GH_PROMPT_DISABLED='1', GH_NO_UPDATE_NOTIFIER='1', GH_NO_EXTENSION_UPDATE_NOTIFIER='1')


class BudgetFailure(Exception):
    pass


class AttemptTimeout(Exception):
    pass


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def require(condition, detail):
    if not condition:
        raise ValueError(detail)


def identity(raw):
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def same(a, b):
    return all(a[k] == b[k] for k in ('bytes', 'sha256'))


def remaining():
    left = BOUNDS['overallSeconds'] - (time.monotonic() - START)
    if left <= 0:
        STOP.set()
        raise BudgetFailure('overall-900-second-limit')
    return left


def safe_path(relative):
    p = PurePosixPath(relative)
    require(not p.is_absolute() and p.as_posix() == relative and '..' not in p.parts,
            'unsafe-relative-path')
    full = ROOT / relative
    require(full.is_file() and not full.is_symlink(), 'ordinary-file-required:' + relative)
    require(all(not (ROOT / parent).is_symlink() for parent in p.parents), 'symlinked-parent')
    require(full.resolve().is_relative_to(ROOT), 'path-outside-repository')
    return full


def unique(items):
    out = {}
    for k, v in items:
        require(k not in out, 'duplicate-administrative-key')
        out[k] = v
    return out


def invalid_constant(value):
    raise ValueError('nonfinite-administrative-json:' + value)


def parse_admin(raw):
    return json.loads(raw, object_pairs_hook=unique, parse_constant=invalid_constant)


def read_pinned(pin, decode=False):
    raw = bounded_read(pin['file'])
    require(same(pin, identity(raw)), 'administrative-pin-mismatch:' + pin['file'])
    return parse_admin(raw) if decode else raw


def record(event):
    with MUTEX:
        numbered = {'event': len(EVENTS) + 1, **event}
        if JOURNAL_READY:
            with JOURNAL.open('a', encoding='utf8') as stream:
                stream.write(json.dumps(numbered, separators=(',', ':')) + '\n')
                stream.flush()
                os.fsync(stream.fileno())
        EVENTS.append(numbered)
    return numbered


def error_view(error):
    return {'errorType': type(error).__name__,
            'detail': str(error).replace(str(ROOT), '[repository]')[:1200]}


def allocation_state():
    absent = []
    for phase in ('producer', 'audit', 'finalize', 'ui'):
        for name in (phase + '-supervisor-launch.lock', phase + '-supervisor.json',
                     'results' if phase == 'producer' else phase):
            relative = REL + '/' + name
            require(not os.path.lexists(ROOT / relative), 'allocation-already-started:' + relative)
            absent.append(relative)
    relative = REL + '/viewer/pins.json'
    require(not os.path.lexists(ROOT / relative), 'finalizer-already-started')
    return {'checkedAtUtc': now(), 'allUnstarted': True, 'absentPaths': absent + [relative]}


LOCAL_READ = """import sys
with open(sys.argv[1], 'rb') as f:
 for block in iter(lambda: f.read(65536), b''):
  sys.stdout.buffer.write(block)
"""
LOCAL_HASH = """import hashlib,json,sys
n=0;h=hashlib.sha256();g=hashlib.sha1(b'blob '+sys.argv[2].encode()+bytes([0]))
with open(sys.argv[1],'rb') as f:
 for b in iter(lambda:f.read(1048576),b''):
  n+=len(b);h.update(b);g.update(b)
print(json.dumps({'bytes':n,'sha256':h.hexdigest(),'gitBlobSha1':g.hexdigest()}))
"""


def bounded_local(command, operation, path, log=True):
    begin = time.monotonic()
    duration = min(BOUNDS['secondsPerLocalOperation'], remaining())
    intent = record({'operation': operation, 'stage': 'local-intent', 'path': path,
                     'secondsLimit': duration, 'passed': None}) if log else {'event': None}
    out = bytearray(); err = bytearray(); child = None; code = None; error = None
    selector = selectors.DefaultSelector()
    try:
        child = subprocess.Popen(command, cwd=ROOT, env=ENV, stdin=subprocess.DEVNULL,
                                 stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True)
        for stream, label in ((child.stdout, 'stdout'), (child.stderr, 'stderr')):
            os.set_blocking(stream.fileno(), False)
            selector.register(stream, selectors.EVENT_READ, label)
        while selector.get_map():
            left = duration - (time.monotonic() - begin)
            if left <= 0:
                remaining()
                raise AttemptTimeout('local-operation-45-second-limit')
            for key, _ in selector.select(min(left, .2)):
                cap = BOUNDS['localOperationCapturedBytes'] - len(out) - len(err)
                require(cap > 0, 'local-operation-capture-limit')
                data = os.read(key.fileobj.fileno(), min(65536, cap))
                if not data:
                    selector.unregister(key.fileobj)
                else:
                    (out if key.data == 'stdout' else err).extend(data)
        code = child.wait(timeout=max(.001, duration - (time.monotonic() - begin)))
        require(code == 0, 'local-operation-nonzero')
    except BaseException as exc:
        error = exc
        if child is not None:
            if child.poll() is None:
                os.killpg(child.pid, signal.SIGKILL)
            child.wait(timeout=2); code = child.returncode
    finally:
        selector.close()
        if child is not None:
            child.stdout.close(); child.stderr.close()
    event = {'operation': operation, 'stage': 'local-result', 'path': path,
             'intentEvent': intent['event'], 'passed': error is None, 'returncode': code,
             'capturedStdout': identity(bytes(out)), 'capturedStderr': identity(bytes(err)),
             'stderrText': bytes(err).decode('utf8', 'replace').replace(str(ROOT), '[repository]')[:1000],
             'wallSeconds': time.monotonic() - begin}
    if error is not None:
        event.update(error_view(error))
    if log:
        record(event)
    if error is not None:
        raise error
    return bytes(out)


def bounded_read(relative):
    path = safe_path(relative)
    return bounded_local([sys.executable, '-c', LOCAL_READ, str(path)],
                         'administrative-byte-read', relative)


def local_identity(pin):
    begin = time.monotonic()
    path = safe_path(pin['path'])
    raw = bounded_local([sys.executable, '-c', LOCAL_HASH, str(path), str(pin['bytes'])],
                        'opaque-hash-subprocess', pin['path'])
    got = parse_admin(raw)
    require(same(pin, got), 'local-byte-identity-mismatch:' + pin['path'])
    if pin.get('gitBlobOid'):
        require(got['gitBlobSha1'] == pin['gitBlobOid'], 'declared-blob-mismatch')
    return {'operation': 'local', 'path': pin['path'], 'passed': True, **got,
            'wallSeconds': time.monotonic() - begin}


def tree_identity(pin, local, commit, operation):
    begin = time.monotonic()
    raw = bounded_local(['/usr/bin/git', 'ls-tree', '--full-tree', '-z', commit, '--', pin['path']],
                        'git-tree-metadata-subprocess', pin['path'])
    entries = raw.split(b'\0')
    require(len(entries) == 2 and entries[-1] == b'', 'one-exact-tree-entry-required')
    meta, path = entries[0].split(b'\t', 1)
    mode, kind, oid = meta.decode('ascii').split(' ')
    require(path == pin['path'].encode() and kind == 'blob' and mode in ('100644', '100755'),
            'exact-ordinary-tree-blob-required')
    require(oid == local['gitBlobSha1'] == pin['gitBlobOid'], 'tree-blob-identity-mismatch')
    return record({'operation': operation, 'path': pin['path'], 'commit': commit,
                   'passed': True, 'bytes': pin['bytes'], 'sha256': pin['sha256'],
                   'gitBlobSha1': oid, 'gitTreeMode': mode,
                   'localIdentityEvent': local['event'], 'treeMetadata': identity(raw),
                   'wallSeconds': time.monotonic() - begin,
                   'binding': 'Fresh exact tree metadata plus fresh local SHA256 and Git blob SHA1; no blob extraction.'})


def validate_original(protocol):
    original = read_pinned(protocol['originalFailure'], True)
    journal_raw = read_pinned(protocol['originalJournal'])
    journal = [parse_admin(line) for line in journal_raw.splitlines()]
    manifest = read_pinned(protocol['manifest'], True)
    read_pinned(protocol['originalProtocol'])
    read_pinned(protocol['originalHelper'])
    read_pinned(protocol['frozenPublicProcedure'])
    require(original['passed'] is False and original['phase'] == 'source' and
            original['commit'] == COMMIT, 'original-must-remain-failed')
    require(original['events'] == journal and [e['event'] for e in journal] == list(range(1, len(journal) + 1)),
            'original-journal-mismatch')
    require(original['eventJournal'] == protocol['originalJournal'], 'original-journal-pin-mismatch')
    require(original['helper'] == protocol['originalHelper'] and
            original['protocol'] == protocol['originalProtocol'], 'original-procedure-pin-mismatch')
    require(original['manifestPath'] == protocol['manifest']['file'] and
            original['manifestBytes'] == protocol['manifest']['bytes'] and
            original['manifestSha256'] == protocol['manifest']['sha256'], 'original-manifest-pin-mismatch')
    require(original['allAllocationsUnstartedAtStartAndEnd'] is True and
            all(original['allocationChecks'][x]['allUnstarted'] is True for x in ('start', 'end')),
            'original-allocation-state')
    require(original['inputPublicProofsReused'] == 0 and original['freshPublicReads'] == 67 and
            original['freshInputPublicPins'] == 27 and original['verifiedFilePins'] == 66,
            'original-counts-mismatch')
    pins = manifest['files']
    by_path = {p['path']: p for p in pins}
    require(len(by_path) == len(pins) == 74 and sum(p.get('kind') == 'input' for p in pins) == 35 and
            sum(p['bytes'] for p in pins if p.get('kind') == 'input') == 209531895, 'manifest-counts')
    events = {e['event']: e for e in journal}
    proofs = original['fileProofs']
    require(len(proofs) == 66 and [p['descriptor'] for p in proofs] == original['files'], 'original-proof-count')
    successful = set()
    for proof in proofs:
        d = proof['descriptor']
        require(d == by_path[d['path']] and d['path'] not in successful, 'original-descriptor-mismatch')
        successful.add(d['path'])
        chain = [events[n] for n in proof['events']]
        is_input = d.get('kind') == 'input'
        expected = ['local', 'source-commit'] + (['input-origin-commit'] if is_input else [])
        require(len(chain) == len(expected) + 1 and [x['operation'] for x in chain[:-1]] == expected,
                'original-chain-shape')
        require(all(x['passed'] is True and x['path'] == d['path'] for x in chain), 'original-chain-state')
        require(all(same(d, x) for x in chain[:-1]) and chain[1]['commit'] == COMMIT,
                'original-local-tree-binding')
        require(chain[0]['gitBlobSha1'] == chain[1]['gitBlobSha1'] and
                chain[1]['localIdentityEvent'] == chain[0]['event'], 'original-source-blob-binding')
        if is_input:
            require(chain[2]['commit'] == d['originCommit'] and
                    chain[0]['gitBlobSha1'] == chain[2]['gitBlobSha1'] == d['gitBlobOid'] and
                    chain[2]['localIdentityEvent'] == chain[0]['event'], 'original-input-origin-binding')
        remote = chain[-1]
        require(remote['operation'] == 'public-contents-api' and remote['authenticated'] is True and
                remote['httpStatus'] == 200 and remote['returncode'] == 0 and same(d, remote['publicIdentity']) and
                same(d, remote['responseBody']) and remote['commitBinding'] == COMMIT and
                remote['gitBlobSha1'] == chain[0]['gitBlobSha1'], 'original-public-identity')
        require(remote['endpoint'] == 'https://api.github.com/repos/' + REPO + '/contents/' +
                quote(d['path'], safe='/') + '?ref=' + COMMIT, 'original-exact-public-endpoint')
    mp = {'path': protocol['manifest']['file'], **{k: protocol['manifest'][k] for k in ('bytes', 'sha256')}}
    mchain = [events[n] for n in (1, 2, 4)]
    require(all(x['passed'] is True and x['path'] == mp['path'] for x in mchain) and
            all(same(mp, x) for x in mchain[:2]) and same(mp, mchain[2]['publicIdentity']) and
            same(mp, mchain[2]['responseBody']) and mchain[1]['commit'] == COMMIT and
            mchain[0]['gitBlobSha1'] == mchain[1]['gitBlobSha1'] and
            mchain[1]['localIdentityEvent'] == 1 and mchain[2]['operation'] == 'public-contents-api' and
            mchain[2]['httpStatus'] == 200 and mchain[2]['authenticated'] is True and
            mchain[2]['commitBinding'] == COMMIT and mchain[2]['returncode'] == 0 and
            mchain[2]['endpoint'] == 'https://api.github.com/repos/' + REPO + '/contents/' + mp['path'] + '?ref=' + COMMIT,
            'original-manifest-public-binding')
    metadata = events[3]
    require(metadata == original['repositoryMetadata'] and metadata['passed'] is True and
            metadata['operation'] == 'repository-public-metadata' and metadata['authenticated'] is True and
            metadata['httpStatus'] == 200 and metadata['returncode'] == 0 and
            metadata['endpoint'] == 'https://api.github.com/repos/' + REPO and
            metadata['repositoryMetadata'] == {'full_name': REPO, 'private': False, 'visibility': 'public',
                                               'html_url': 'https://github.com/' + REPO}, 'original-public-repository')
    missing = [p for p in pins if p['path'] not in successful]
    require(missing == protocol['missingFiles'] and len(missing) == 8 and
            all(p['kind'] == 'input' for p in missing) and sum(p['bytes'] for p in missing) == 207305212,
            'exact-eight-missing-inputs-required')
    failures = [e for e in journal if e['passed'] is False]
    require(failures == original['failedAttempts'] and len(failures) == 24 and
            sum(e['errorType'] == 'AttemptTimeout' for e in failures) == 22 and
            sum('CANCEL; received from peer' in e.get('stderrText', '') for e in failures) == 2,
            'original-failure-history')
    require({e['path'] for e in failures} == {p['path'] for p in missing} and
            all(sorted(e['attempt'] for e in failures if e['path'] == p['path']) == [1, 2, 3] for p in missing),
            'original-attempt-history')
    return original, pins, missing, mp


def validate_recovery_history_and_routes(protocol, missing):
    global ROUTES
    old = read_pinned(protocol['priorRecoveryFailure'], True)
    journal = [parse_admin(x) for x in read_pinned(protocol['priorRecoveryJournal']).splitlines()]
    require(old['passed'] is False and old['closed'] is True and old['events'] == journal and
            old['publicRequests'] == 16 and old['verifiedFilePins'] == 0 and
            old['aggregateCapturedPublicBytes'] == 3424392 and old['closureErrors'] == [] and
            old['allAllocationsUnstartedAtStartAndEnd'] is True, 'prior-recovery-remains-closed-failed')
    require(old['eventJournal'] == protocol['priorRecoveryJournal'] and
            old['helper'] == protocol['priorRecoveryHelper'] and old['protocol'] == protocol['priorRecoveryProtocol'],
            'prior-recovery-procedure-pins')
    require([e['event'] for e in journal] == list(range(1, len(journal) + 1)), 'prior-recovery-event-numbering')
    failures = [e for e in journal if e.get('stage') == 'attempt-end']
    require(failures == old['failedAttempts'] and len(failures) == 16 and
            all(e['passed'] is False for e in failures), 'prior-sixteen-failures')
    for key in ('priorRecoveryHelper', 'priorRecoveryProtocol', 'priorRecoveryClosureReview'):
        read_pinned(protocol[key])
    plan = read_pinned(protocol['failedHandoffPlan'], True)
    require(plan['closed'] is True and plan['passed'] is False and plan['networkCalls'] == 0,
            'failed-handoff-plan-remains-closed')
    read_pinned(protocol['historicalRadialReceipt'])
    read_pinned(protocol['historicalPhaseReceipt'])
    routes = protocol['retrievals']
    require([r['descriptor'] for r in routes] == missing, 'exact-eight-retrieval-descriptors')
    for route in routes:
        pin = route['descriptor']; path = pin['path']; ref = route['retrievalCommit']
        if '/transport/selected.jsonl.gz.part' in path:
            expected_ref = '0461153a7d6f75cb6e8564850b77e8b6f04cebb2'
            expected_operation = 'public-raw-cdn'
            expected_receipt = protocol['historicalRadialReceipt']
        elif path == 'research/m31-neighbor-density-2026-10-23/results/stages.jsonl':
            expected_ref = 'a38234d150bcdecb50e3c4615e07dc8703039397'
            expected_operation = 'public-raw-cdn'
            expected_receipt = protocol['historicalRadialReceipt']
        else:
            require(path == 'research/m31-radial-integration-2026-10-23/audit/audit.json', 'exact-eighth-path')
            expected_ref = 'e99ce65cd6bbafa705e412ddd58c3058a9251eab'
            expected_operation = 'public-contents-api'
            expected_receipt = protocol['historicalPhaseReceipt']
        require(ref == expected_ref and route['operation'] == expected_operation and
                route['historicalReceipt'] == expected_receipt, 'reviewed-immutable-transport-selection')
        old_receipt = read_pinned(expected_receipt, True)
        matches = [e for e in old_receipt['events'] if e['event'] == route['historicalEvent']]
        require(len(matches) == 1, 'one-historical-route-event')
        event = matches[0]
        require(event['passed'] is True and event['path'] == path and event['httpStatus'] == 200,
                'historical-route-success')
        if route['operation'] == 'public-raw-cdn':
            endpoint = 'https://raw.githubusercontent.com/' + REPO + '/' + ref + '/' + quote(path, safe='/')
            require(event['operation'] == 'public' and event['commit'] == ref and event['url'] == endpoint and
                    same(pin, event), 'historical-cdn-route-pin')
        else:
            endpoint = 'https://api.github.com/repos/' + REPO + '/contents/' + quote(path, safe='/') + '?ref=' + ref
            require(event['operation'] == 'public-contents-api' and event['authenticated'] is True and
                    event['endpoint'] == endpoint and same(pin, event['responseBody']), 'historical-api-route-pin')
        require(route['endpoint'] == endpoint, 'prospective-immutable-endpoint')
    ROUTES = {r['descriptor']['path']: r for r in routes}


class OpaqueResponse:
    def __init__(self, pin):
        self.stdout_hash = hashlib.sha256()
        self.body_hash = hashlib.sha256()
        self.blob_hash = hashlib.sha1(('blob ' + str(pin['bytes']) + '\0').encode())
        self.stdout_bytes = self.body_bytes = self.header_bytes = 0
        self.pending = bytearray()
        self.headers_complete = False
        self.status = None
        self.safe_headers = {}

    def feed(self, data):
        self.stdout_hash.update(data)
        self.stdout_bytes += len(data)
        if not self.headers_complete:
            self.pending.extend(data)
            while not self.headers_complete:
                end = self.pending.find(b'\r\n\r\n')
                if end < 0:
                    require(self.header_bytes + len(self.pending) <= 65536, 'response-headers-too-large')
                    return
                header = bytes(self.pending[:end + 4])
                del self.pending[:end + 4]
                self.header_bytes += len(header)
                require(self.header_bytes <= 65536, 'response-headers-too-large')
                match = re.match(rb'HTTP/[^\s]+ ([0-9]{3})[^\r\n]*\r\n', header)
                require(match is not None, 'invalid-http-status-line')
                self.status = int(match.group(1))
                if 100 <= self.status < 200:
                    continue
                self.headers_complete = True
                for line in header[match.end():].decode('latin1').splitlines():
                    if ':' in line:
                        key, value = line.split(':', 1)
                        if key.lower() in ('content-type', 'content-length', 'content-encoding', 'etag',
                                          'x-github-request-id', 'x-cache', 'via', 'age'):
                            self.safe_headers[key.lower()] = value.strip()[:500]
                data = bytes(self.pending)
                self.pending.clear()
        self.body_bytes += len(data)
        self.body_hash.update(data)
        self.blob_hash.update(data)

    def snapshot(self):
        return {'capturedStdout': {'bytes': self.stdout_bytes, 'sha256': self.stdout_hash.hexdigest()},
                'httpStatus': self.status, 'httpHeadersComplete': self.headers_complete,
                'responseBody': {'bytes': self.body_bytes, 'sha256': self.body_hash.hexdigest()},
                'responseGitBlobSha1': self.blob_hash.hexdigest(), 'safeResponseHeaders': self.safe_headers}


def capture_public(route, pin):
    global CAPTURED
    duration = min(BOUNDS['secondsPerAttempt'], remaining())
    begin = time.monotonic()
    response = OpaqueResponse(pin)
    err_hash = hashlib.sha256()
    err_bytes = 0
    err_preview = bytearray()
    failure = None
    process = None
    code = None
    selector = selectors.DefaultSelector()
    if route['operation'] == 'public-raw-cdn':
        command = ['/usr/bin/curl', '--disable', '--silent', '--show-error', '--include',
                   '--suppress-connect-headers', '--proto', '=https', '--max-redirs', '0',
                   '--connect-timeout', '10', '--max-time', '90', '--retry', '0', '--proxy', '',
                   '--header', 'Accept-Encoding: identity', '--url', route['endpoint']]
    else:
        endpoint = route['endpoint'].removeprefix('https://api.github.com/')
        command = ['/opt/homebrew/bin/gh', 'api', '--hostname', 'github.com', '--method', 'GET', '--include',
                   '-H', 'Accept: application/vnd.github.raw+json', '-H', 'X-GitHub-Api-Version: 2022-11-28', endpoint]

    try:
        require(not STOP.is_set(), 'recovery-stopped')
        process = subprocess.Popen(command, cwd=ROOT, env=ENV, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE, start_new_session=True)
        for stream, label in ((process.stdout, 'stdout'), (process.stderr, 'stderr')):
            os.set_blocking(stream.fileno(), False)
            selector.register(stream, selectors.EVENT_READ, label)
        while selector.get_map():
            left = duration - (time.monotonic() - begin)
            if left <= 0:
                remaining()
                raise AttemptTimeout('public-attempt-90-second-limit')
            if STOP.is_set():
                raise BudgetFailure('recovery-stopped')
            for key, _ in selector.select(min(left, .2)):
                with MUTEX:
                    available = BOUNDS['aggregateCapturedPublicBytes'] - CAPTURED
                    if available <= 0:
                        raise BudgetFailure('aggregate-captured-536870912-byte-limit')
                    data = os.read(key.fileobj.fileno(), min(65536, available))
                    CAPTURED += len(data)
                if not data:
                    selector.unregister(key.fileobj)
                elif key.data == 'stdout':
                    response.feed(data)
                else:
                    err_bytes += len(data)
                    err_hash.update(data)
                    err_preview.extend(data[:max(0, 2000 - len(err_preview))])
        code = process.wait(timeout=max(.001, duration - (time.monotonic() - begin)))
    except BaseException as error:
        failure = error
        if isinstance(error, BudgetFailure):
            STOP.set()
        if process is not None:
            if process.poll() is None:
                os.killpg(process.pid, signal.SIGKILL)
            process.wait(timeout=2)
            code = process.returncode
    finally:
        selector.close()
        if process is not None:
            process.stdout.close()
            process.stderr.close()
    stderr_text = err_preview.decode('utf8', 'replace').replace(str(ROOT), '[repository]')
    stderr_text = re.sub(r'gh[pousr]_[A-Za-z0-9_]+|github_pat_[A-Za-z0-9_]+', '[redacted-token]', stderr_text)
    stderr_text = re.sub(r'(?i)(authorization:\s*(?:bearer|basic)\s+)\S+', r'\1[redacted]', stderr_text)
    return {**response.snapshot(), 'returncode': code,
            'capturedStderr': {'bytes': err_bytes, 'sha256': err_hash.hexdigest()},
            'stderrText': stderr_text[:1000], 'wallSeconds': time.monotonic() - begin}, failure


def recover_one(pin):
    global REQUESTS
    local = record(local_identity(pin))
    source = tree_identity(pin, local, COMMIT, 'source-commit')
    origin = tree_identity(pin, local, pin['originCommit'], 'input-origin-commit')
    route = ROUTES[pin['path']]
    retrieval = tree_identity(pin, local, route['retrievalCommit'], 'retrieval-commit')
    for attempt in range(1, BOUNDS['attemptsPerFile'] + 1):
        remaining()
        if STOP.is_set():
            raise BudgetFailure('recovery-stopped')
        with MUTEX:
            require(REQUESTS < BOUNDS['maxPublicRequests'], 'public-request-limit')
            REQUESTS += 1
            request_number = REQUESTS
        event = {'operation': route['operation'], 'path': pin['path'], 'attempt': attempt,
                 'publicRequest': request_number, 'endpoint': route['endpoint'],
                 'authenticated': route['operation'] == 'public-contents-api',
                 'sourceCommitBinding': COMMIT, 'retrievalCommit': route['retrievalCommit'],
                 'originCommit': pin['originCommit'], 'gitBlobSha1': pin['gitBlobOid'],
                 'transport': ('TLS-verified unauthenticated curl; protocol negotiation; no redirects/proxy/curlrc'
                               if route['operation'] == 'public-raw-cdn' else 'Authenticated public GitHub Contents API raw body'),
                 'freshPublicRead': True, 'historicalPublicProofReused': False}
        started = record({**event, 'stage': 'attempt-start', 'passed': None, 'startedAtUtc': now()})
        capture, failure = capture_public(route, pin)
        event.update(capture)
        event['startEvent'] = started['event']
        event['stage'] = 'attempt-end'
        try:
            if failure is not None:
                raise failure
            require(capture['returncode'] == 0, 'public-transfer-nonzero-exit')
            require(capture['httpHeadersComplete'] is True and capture['httpStatus'] == 200,
                    'missing-or-non-200-http-status')
            require(same(pin, capture['responseBody']), 'public-byte-identity-mismatch')
            require(capture['responseGitBlobSha1'] == pin['gitBlobOid'], 'public-git-blob-mismatch')
            public = record({**event, 'passed': True, 'publicIdentity': capture['responseBody']})
            print(json.dumps({'recovered': pin['path'], 'attempt': attempt,
                              'bytes': pin['bytes']}), flush=True)
            return {'descriptor': pin, 'events': [x['event'] for x in (local, source, origin, retrieval, public)]}
        except BaseException as error:
            record({**event, 'passed': False, **error_view(error)})
            if isinstance(error, BudgetFailure):
                raise
    raise RuntimeError('two-public-attempts-exhausted:' + pin['path'])


def write_new_json(path, value):
    with path.open('x', encoding='utf8') as stream:
        json.dump(value, stream, indent=2, allow_nan=False)
        stream.write('\n')


def main():
    global JOURNAL_READY
    parser = argparse.ArgumentParser()
    parser.add_argument('--protocol-sha256', required=True)
    args = parser.parse_args()
    require(re.fullmatch('[0-9a-f]{64}', args.protocol_sha256) is not None, 'protocol-digest-required')
    protocol_path = REC + '-protocol.json'
    raw = bounded_read(protocol_path)
    require(identity(raw)['sha256'] == args.protocol_sha256, 'prospective-protocol-mismatch')
    protocol = parse_admin(raw)
    require(protocol['bounds'] == BOUNDS and protocol['commit'] == COMMIT and
            protocol['repository'] == REPO and protocol['recoveryBytes'] == 207305212,
            'prospective-scope-mismatch')
    require(protocol['helper']['file'] == REC + '-helper.py', 'exact-helper-path')
    read_pinned(protocol['helper'])
    for suffix in ('.json', '-failure.json', '-initialization-failure.json', '-events.jsonl', '-launch.lock'):
        require(not os.path.lexists(ROOT / (REC + suffix)), 'single-use-output-exists:' + suffix)
    with (ROOT / (REC + '-launch.lock')).open('x') as stream:
        stream.write(json.dumps({'startedAtUtc': now(), 'protocolSha256': args.protocol_sha256}) + '\n')
    with JOURNAL.open('x', encoding='utf8') as stream:
        for event in EVENTS:
            stream.write(json.dumps(event, separators=(',', ':')) + '\n')
    JOURNAL_READY = True
    errors = []
    closure_errors = []
    allocations = {}
    proofs = []
    pins = []
    missing = []
    manifest_pin = None
    original = None
    end_identities = []
    try:
        allocations['start'] = allocation_state()
        original, pins, missing, manifest_pin = validate_original(protocol)
        validate_recovery_history_and_routes(protocol, missing)
        with ThreadPoolExecutor(max_workers=BOUNDS['maxConcurrentTransfers']) as pool:
            futures = {pool.submit(recover_one, pin): pin for pin in missing}
            for future in as_completed(futures):
                try:
                    proofs.append(future.result())
                except BaseException as error:
                    errors.append({'path': futures[future]['path'], **error_view(error)})
        require(len(proofs) == 8 and not errors, 'recovery-incomplete')
    except BaseException as error:
        errors.append(error_view(error))
    finally:
        STOP.set()
        try:
            allocations['end'] = allocation_state()
        except BaseException as error:
            closure_errors.append({'check': 'allocation-state-end', **error_view(error)})
        try:
            for key in ('helper', 'originalFailure', 'originalJournal', 'manifest',
                        'originalProtocol', 'originalHelper', 'frozenPublicProcedure',
                        'priorRecoveryFailure', 'priorRecoveryJournal', 'priorRecoveryProtocol',
                        'priorRecoveryHelper', 'priorRecoveryClosureReview', 'failedHandoffPlan',
                        'historicalRadialReceipt', 'historicalPhaseReceipt'):
                read_pinned(protocol[key])
            require(same(identity(bounded_read(protocol_path)), identity(raw)), 'protocol-changed')
        except BaseException as error:
            closure_errors.append({'check': 'administrative-identities-end', **error_view(error)})
        try:
            require(bool(pins) and manifest_pin is not None, 'manifest-not-established')
            for pin in pins + [manifest_pin]:
                end_identities.append(record({**local_identity(pin), 'operation': 'local-end'}))
        except BaseException as error:
            closure_errors.append({'check': 'frozen-local-identities-end', **error_view(error)})
    if time.monotonic() - START > BOUNDS['overallSeconds']:
        closure_errors.append({'check': 'overall-wall-cap', 'detail': '900-second-limit-exceeded'})
    passed = len(proofs) == 8 and not errors and not closure_errors
    ordered_proofs = sorted(proofs, key=lambda x: x['descriptor']['path'])
    try:
        journal_bytes = bounded_local([sys.executable, '-c', LOCAL_READ, str(JOURNAL)],
                                      'generated-journal-final-read', REC + '-events.jsonl', log=False)
        journal_pin = {'file': REC + '-events.jsonl', **identity(journal_bytes)}
    except BaseException as error:
        closure_errors.append({'check': 'journal-final-identity', **error_view(error)})
        journal_pin = {'file': REC + '-events.jsonl', 'identityUnavailable': True}
        passed = False
    request_events = [e for e in EVENTS if e.get('stage') == 'attempt-end']
    final_wall_seconds = time.monotonic() - START
    if final_wall_seconds > BOUNDS['overallSeconds']:
        closure_errors.append({'check': 'final-overall-wall-cap', 'detail': '900-second-limit-exceeded'})
        passed = False
    receipt = {
        'schema': 'm31-native-factor-reuse-administrative-immutable-ref-recovery-v2',
        'phase': 'source-recovery', 'passed': passed, 'closed': True, 'commit': COMMIT,
        'checkedAtUtc': now(), 'protocol': {'file': protocol_path, **identity(raw)},
        'helper': protocol['helper'], 'originalFailure': protocol['originalFailure'],
        'originalJournal': protocol['originalJournal'], 'originalProtocol': protocol['originalProtocol'],
        'originalHelper': protocol['originalHelper'], 'manifest': protocol['manifest'],
        'bounds': BOUNDS, 'originalAcquisitionPassed': False, 'originalFailedAttemptsPreserved': 24,
        'priorRecoveryFailure': protocol['priorRecoveryFailure'], 'priorRecoveryJournal': protocol['priorRecoveryJournal'],
        'priorRecoveryFailedAttemptsPreserved': 16, 'totalPriorFailedPublicAttemptsPreserved': 40,
        'failedHandoffPlan': protocol['failedHandoffPlan'], 'retrievals': protocol['retrievals'],
        'originalFailureBreakdown': {'attemptTimeouts': 22, 'ghNonzeroCancelledStreams': 2},
        'retainedOriginalFileProofsValidated': 66 if original else 0,
        'retainedOriginalManifestProofValidated': original is not None,
        'retainedPublicRepositoryMetadataValidated': original is not None,
        'recoveryFilePins': len(missing), 'recoveryBytes': sum(p['bytes'] for p in missing),
        'verifiedFilePins': len(proofs), 'freshSuccessfulPublicReads': sum(e['passed'] is True for e in request_events),
        'publicRequests': REQUESTS, 'aggregateCapturedPublicBytes': CAPTURED,
        'failedAttempts': [e for e in request_events if e['passed'] is False],
        'files': [p['descriptor'] for p in ordered_proofs], 'fileProofs': ordered_proofs,
        'eventJournal': journal_pin, 'events': EVENTS, 'allocationChecks': allocations,
        'allAllocationsUnstartedAtStartAndEnd': all(allocations.get(x, {}).get('allUnstarted') is True for x in ('start', 'end')),
        'frozenLocalIdentitiesRecheckedAtEnd': len(end_identities), 'errors': errors,
        'closureErrors': closure_errors, 'wallSeconds': final_wall_seconds,
        'publicRoutes': {'public-raw-cdn': 7, 'public-contents-api': 1},
        'authentication': 'Seven unauthenticated raw-CDN bodies and one authenticated public Contents API body; historical immutable transport refs independently bound to current source/origin blob identities.',
        'priorCheckpointPublicProofsReused': 0, 'allocationLaunched': False,
        'nativeQueries': 0, 'auditExecuted': False, 'uiLaunched': False,
        'archiveDecompressed': False, 'imageRendered': False, 'savedStateReaggregated': False,
        'rawEvidenceTreatedAsOpaqueBytes': True,
        'verificationScope': 'Eight newly downloaded exact input bodies at reviewed historical immutable transport refs. Fresh local SHA256/Git blob SHA1 and fresh current source, declared origin and retrieval-ref tree bindings required. Historical successful receipts guide endpoint choice only; no historical public proof reused. All40 prior failures and failed handoff plan remain unchanged. Local byte reads and Git metadata are deadline-enforced subprocesses. No model/control/auditor execution, archive decoding or scientific-log parsing.'}
    output = REC + ('.json' if passed else '-failure.json')
    write_new_json(ROOT / output, receipt)
    print(json.dumps({'passed': passed, 'closed': True, 'receipt': output,
                      'verifiedFilePins': len(proofs), 'publicRequests': REQUESTS,
                      'aggregateCapturedPublicBytes': CAPTURED, 'errors': errors,
                      'closureErrors': closure_errors, 'wallSeconds': receipt['wallSeconds']}), flush=True)
    return 0 if passed else 1


if __name__ == '__main__':
    try:
        status = main()
    except BaseException as error:
        output = ROOT / (REC + '-initialization-failure.json')
        if not output.exists():
            write_new_json(output, {'schema': 'm31-administrative-recovery-initialization-failure-v1',
                                   'closed': True, 'passed': False, 'error': error_view(error),
                                   'events': EVENTS, 'publicRequests': REQUESTS,
                                   'wallSeconds': time.monotonic() - START, 'scientificExecution': False})
        raise
    raise SystemExit(status)
