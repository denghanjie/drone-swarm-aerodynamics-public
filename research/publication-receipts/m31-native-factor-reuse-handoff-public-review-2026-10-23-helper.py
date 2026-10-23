"""Seven bounded read-only handoff-publication checks; never a source gate."""
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
import subprocess
import time

ROOT = Path(__file__).resolve().parents[2]
BASE = 'research/publication-receipts/m31-native-factor-reuse-handoff-public-review-2026-10-23'
REL = 'research/m31-native-factor-reuse-2026-10-23'
REPO = 'denghanjie/drone-swarm-aerodynamics-public'
BRANCH = 'codex/m31-audit-2026-10-15'
PARENT = '7e6ab5b1d3bb819a7a17178c9a5636bde49ca6f2'
LIMITS = {'maxRequests': 7, 'attemptsPerRequest': 1, 'maxConcurrentRequests': 1,
          'secondsPerRequest': 20, 'overallSeconds': 180, 'aggregateCapturedBytes': 8388608}
ENV = {k: v for k, v in os.environ.items() if k not in ('GH_DEBUG', 'DEBUG')}
ENV.update(GH_PROMPT_DISABLED='1', GH_NO_UPDATE_NOTIFIER='1', GH_NO_EXTENSION_UPDATE_NOTIFIER='1')


def need(condition, message):
    if not condition:
        raise ValueError(message)


def bid(raw):
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def parse(raw):
    def pairs(items):
        out = {}
        for key, value in items:
            need(key not in out, 'duplicate-administrative-key')
            out[key] = value
        return out
    def nonfinite(value):
        raise ValueError('nonfinite-administrative-json:' + value)
    return json.loads(raw, object_pairs_hook=pairs, parse_constant=nonfinite)


def checked(pin):
    name = pin['file']
    p = PurePosixPath(name)
    need(not p.is_absolute() and p.as_posix() == name and '..' not in p.parts, 'safe-relative-path')
    full = ROOT / name
    need(full.is_file() and not full.is_symlink() and full.resolve().is_relative_to(ROOT), 'ordinary-file')
    need(all(not (ROOT / parent).is_symlink() for parent in p.parents), 'ordinary-parents')
    raw = full.read_bytes()
    need(bid(raw) == {k: pin[k] for k in ('bytes', 'sha256')}, 'pinned-local-bytes:' + name)
    return raw


def clean(value):
    value = str(value).replace(str(ROOT), '[repository]')
    value = re.sub(r'gh[pousr]_[A-Za-z0-9_]+|github_pat_[A-Za-z0-9_]+', '[redacted-token]', value)
    return re.sub(r'(?i)(authorization:\s*(?:bearer|basic)\s+)\S+', r'\1[redacted]', value)[:1200]


def error_view(error):
    return {'errorType': type(error).__name__, 'detail': clean(error)}


def allocation_check():
    absent = []
    for phase in ('producer', 'audit', 'finalize', 'ui'):
        absent.extend(REL + '/' + x for x in
                      (phase + '-supervisor-launch.lock', phase + '-supervisor.json',
                       'results' if phase == 'producer' else phase))
    absent.append(REL + '/viewer/pins.json')
    need(all(not os.path.lexists(ROOT / p) for p in absent), 'scientific-allocations-must-remain-unstarted')
    return {'allUnstarted': True, 'absentPaths': absent}


class Review:
    def __init__(self, protocol_pin):
        self.started = time.monotonic()
        self.protocol_pin = protocol_pin
        self.protocol_raw = checked(protocol_pin)
        self.protocol = parse(self.protocol_raw)
        p = self.protocol
        need(p['schema'] == 'm31-native-factor-reuse-seven-read-handoff-publication-protocol-v1' and
             p['reviewed'] is True and p['bounds'] == LIMITS, 'reviewed-exact-protocol')
        need(p['repository'] == REPO and p['branch'] == BRANCH and p['parent'] == PARENT,
             'fixed-repository-branch-source-parent')
        need(re.fullmatch('[0-9a-f]{40}', p['commit']) and re.fullmatch('[0-9a-f]{40}', p['tree']),
             'exact-commit-and-tree')
        need(p['helper']['file'] == BASE + '-helper.py', 'exact-helper-path')
        checked(p['helper'])
        publication = parse(checked(p['apiPublication']))
        need(publication['passed'] is True and publication['closed'] is True and
             publication['commit'] == p['commit'] and publication['tree'] == p['tree'] and
             publication['publicationContext']['kind'] == 'handoff', 'successful-exact-handoff-publication')
        expected = ['repository', 'commit', 'root-tree', 'branch', 'summary', 'closure', 'manifest']
        need([r['name'] for r in p['reads']] == expected, 'exact-seven-read-names')
        prefixes = 'repos/' + REPO
        endpoints = [prefixes, prefixes + '/git/commits/' + p['commit'],
                     prefixes + '/git/trees/' + p['tree'], prefixes + '/git/ref/heads/' + BRANCH]
        required = [p['summary'], p['closure'], p['manifest']]
        expected_names = ['research/publication-receipts/m31-native-factor-reuse-handoff-2026-10-23-' + s
                          for s in ('SUMMARY.md', 'CLOSURE.json', 'manifest.json')]
        need([x['file'] for x in required] == expected_names, 'exact-three-small-handoff-files')
        endpoints += [prefixes + '/contents/' + quote(pin['file'], safe='/') + '?ref=' + p['commit']
                      for pin in required]
        need([r['endpoint'] for r in p['reads']] == endpoints, 'exact-seven-read-endpoints')
        need(all(r['accept'] == ('application/vnd.github+json' if i < 4 else 'application/vnd.github.raw+json')
                 for i, r in enumerate(p['reads'])), 'exact-read-representations')
        for pin in required:
            need(pin['bytes'] <= 131072, 'small-handoff-file-limit')
            checked(pin)
        for suffix in ('.json', '-failure.json', '-events.jsonl', '-launch.lock'):
            need(not os.path.lexists(ROOT / (BASE + suffix)), 'single-use-publication-check')
        with (ROOT / (BASE + '-launch.lock')).open('x') as out:
            out.write(json.dumps({'protocol': protocol_pin, 'purpose': 'seven read-only handoff checks'}) + '\n')
        self.journal = ROOT / (BASE + '-events.jsonl')
        self.journal.touch(exist_ok=False)
        self.events = []
        self.requests = 0
        self.captured = 0

    def record(self, event):
        numbered = {'event': len(self.events) + 1, **event}
        with self.journal.open('a') as out:
            out.write(json.dumps(numbered, separators=(',', ':')) + '\n')
            out.flush()
            os.fsync(out.fileno())
        self.events.append(numbered)
        return numbered

    def remaining(self):
        left = LIMITS['overallSeconds'] - (time.monotonic() - self.started)
        need(left > 0, 'overall-180-second-limit')
        return left

    def capture(self, request):
        duration = min(LIMITS['secondsPerRequest'], self.remaining())
        begin = time.monotonic()
        out = bytearray()
        err = bytearray()
        child = None
        failure = None
        code = None
        selector = selectors.DefaultSelector()
        try:
            child = subprocess.Popen(['/opt/homebrew/bin/gh', 'api', '--hostname', 'github.com',
                                      '--method', 'GET', '--include', '-H', 'Accept: ' + request['accept'],
                                      '-H', 'X-GitHub-Api-Version: 2022-11-28', request['endpoint']],
                                     cwd=ROOT, env=ENV, stdin=subprocess.DEVNULL,
                                     stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True)
            for stream, label in ((child.stdout, 'stdout'), (child.stderr, 'stderr')):
                os.set_blocking(stream.fileno(), False)
                selector.register(stream, selectors.EVENT_READ, label)
            while selector.get_map():
                left = duration - (time.monotonic() - begin)
                need(left > 0, 'request-20-second-limit')
                for key, _ in selector.select(min(left, .2)):
                    available = LIMITS['aggregateCapturedBytes'] - self.captured
                    need(available > 0, 'aggregate-captured-8388608-byte-limit')
                    data = os.read(key.fileobj.fileno(), min(65536, available))
                    self.captured += len(data)
                    if not data:
                        selector.unregister(key.fileobj)
                    else:
                        (out if key.data == 'stdout' else err).extend(data)
            code = child.wait(timeout=max(.001, duration - (time.monotonic() - begin)))
        except BaseException as error:
            failure = error
            if child is not None:
                if child.poll() is None:
                    os.killpg(child.pid, signal.SIGKILL)
                child.wait(timeout=2)
                code = child.returncode
        finally:
            selector.close()
            if child is not None:
                child.stdout.close()
                child.stderr.close()
        return bytes(out), bytes(err), code, failure, time.monotonic() - begin

    def verify_response(self, name, body):
        p = self.protocol
        if name in ('summary', 'closure', 'manifest'):
            need(bid(body) == {k: p[name][k] for k in ('bytes', 'sha256')}, 'fresh-public-handoff-file-bytes')
            if name == 'closure':
                value = parse(body)
                need(value['scientificResultExists'] is False and value['independentSourceGatePassed'] is False and
                     all(x == 'UNSTARTED' for x in value['allocations'].values()), 'honest-handoff-closure')
            return {'file': p[name]['file'], 'publicIdentity': bid(body)}
        value = parse(body)
        if name == 'repository':
            need(value['full_name'] == REPO and value['private'] is False and value['visibility'] == 'public',
                 'exact-public-repository')
            return {k: value[k] for k in ('full_name', 'private', 'visibility', 'html_url')}
        if name == 'commit':
            need(value['sha'] == p['commit'] and value['tree']['sha'] == p['tree'] and
                 [x['sha'] for x in value['parents']] == [PARENT], 'exact-public-commit-parent-tree')
            return {'commit': value['sha'], 'tree': value['tree']['sha'], 'parents': [PARENT]}
        if name == 'branch':
            need(value['ref'] == 'refs/heads/' + BRANCH and value['object']['type'] == 'commit' and
                 value['object']['sha'] == p['commit'], 'exact-public-branch-head')
            return {'ref': value['ref'], 'commit': value['object']['sha']}
        need(name == 'root-tree' and value['sha'] == p['tree'] and value['truncated'] is False,
             'complete-public-root-tree')
        entries = value['tree']
        names = [x['path'] for x in entries]
        need(len(names) == len(set(names)) and all('/' not in x and x not in ('', '.', '..') for x in names),
             'ordinary-root-tree-entry-names')
        raw = bytearray()
        for entry in sorted(entries, key=lambda x: x['path'].encode() + (b'/' if x['type'] == 'tree' else b'')):
            mode = entry['mode']
            need(mode in ('040000', '100644', '100755', '120000', '160000') and
                 entry['type'] == {'040000': 'tree', '160000': 'commit'}.get(mode, 'blob') and
                 re.fullmatch('[0-9a-f]{40}', entry['sha']), 'root-tree-entry-mode-type-oid')
            raw.extend(mode.lstrip('0').encode() + b' ' + entry['path'].encode() + b'\0' + bytes.fromhex(entry['sha']))
        oid = hashlib.sha1(b'tree ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
        need(oid == p['tree'], 'public-root-tree-reconstructed-oid')
        return {'tree': oid, 'rootEntries': len(entries), 'reconstructedFromPublicMetadata': True}

    def run(self):
        error = None
        closure_errors = []
        allocation = {}
        proofs = []
        try:
            allocation['start'] = allocation_check()
            for request in self.protocol['reads']:
                need(self.requests < LIMITS['maxRequests'], 'seven-read-limit')
                self.requests += 1
                event = {'request': self.requests, 'name': request['name'], 'attempt': 1,
                         'method': 'GET', 'endpoint': 'https://api.github.com/' + request['endpoint'],
                         'accept': request['accept'], 'authenticated': True}
                started = self.record({**event, 'stage': 'request-intent'})
                raw, err, code, failure, elapsed = self.capture(request)
                result = {**event, 'stage': 'request-result', 'intentEvent': started['event'],
                          'capturedStdout': bid(raw), 'capturedStderr': bid(err), 'returncode': code,
                          'stderrText': clean(err.decode('utf8', 'replace')), 'wallSeconds': elapsed}
                match = re.match(rb'HTTP/[^\s]+\s+(\d{3})[^\r\n]*\r?\n', raw)
                if match:
                    result['httpStatus'] = int(match.group(1))
                try:
                    if failure is not None:
                        raise failure
                    need(code == 0 and result.get('httpStatus') == 200, 'http200-and-gh-success-required')
                    split = re.search(rb'\r?\n\r?\n', raw)
                    need(split is not None and split.end() <= 65536, 'bounded-http-header')
                    body = raw[split.end():]
                    result['responseBody'] = bid(body)
                    result['proof'] = self.verify_response(request['name'], body)
                    proofs.append(self.record({**result, 'passed': True}))
                except BaseException as failure:
                    self.record({**result, 'passed': False, **error_view(failure)})
                    raise
        except BaseException as failure:
            error = error_view(failure)
        finally:
            try:
                allocation['end'] = allocation_check()
            except BaseException as failure:
                closure_errors.append({'check': 'allocations', **error_view(failure)})
            try:
                need(checked(self.protocol_pin) == self.protocol_raw, 'protocol-unchanged')
                for key in ('helper', 'apiPublication', 'summary', 'closure', 'manifest'):
                    checked(self.protocol[key])
            except BaseException as failure:
                closure_errors.append({'check': 'local-administrative-identities', **error_view(failure)})
        elapsed = time.monotonic() - self.started
        passed = len(proofs) == 7 and error is None and not closure_errors and elapsed <= LIMITS['overallSeconds']
        receipt = {'schema': 'm31-native-factor-reuse-independent-handoff-publication-review-v1',
                   'phase': 'handoff-publication', 'passed': passed, 'closed': True,
                   'checkedAtUtc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
                   'commit': self.protocol['commit'], 'tree': self.protocol['tree'], 'parent': PARENT,
                   'protocol': self.protocol_pin, 'helper': self.protocol['helper'],
                   'apiPublication': self.protocol['apiPublication'], 'bounds': LIMITS,
                   'requests': self.requests, 'aggregateCapturedBytes': self.captured, 'wallSeconds': elapsed,
                   'events': self.events, 'successfulChecks': len(proofs), 'error': error,
                   'closureErrors': closure_errors, 'allocationChecks': allocation,
                   'eventJournal': {'file': BASE + '-events.jsonl', **bid(self.journal.read_bytes())},
                   'sourceGatePassed': False, 'scientificResultExists': False,
                   'sourceInputReacquisitionRequests': 0, 'scientificOrUiAllocationLaunched': False,
                   'archiveDecompressed': False, 'qualification': 'Verifies only the public administrative handoff commit/tree/ref and three small handoff files. Original source gate and missing-input recovery remain failed; no scientific claim or source clearance follows.'}
        output = ROOT / (BASE + ('.json' if passed else '-failure.json'))
        with output.open('x') as out:
            json.dump(receipt, out, indent=2, allow_nan=False)
            out.write('\n')
        print(json.dumps({'passed': passed, 'closed': True, 'receipt': output.relative_to(ROOT).as_posix(),
                          'requests': self.requests, 'successfulChecks': len(proofs),
                          'capturedBytes': self.captured, 'wallSeconds': elapsed,
                          'error': error, 'closureErrors': closure_errors}), flush=True)
        return 0 if passed else 1


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--protocol-sha256', required=True)
    args = parser.parse_args()
    need(re.fullmatch('[0-9a-f]{64}', args.protocol_sha256), 'protocol-digest-required')
    path = BASE + '-protocol.json'
    raw = (ROOT / path).read_bytes()
    need(bid(raw)['sha256'] == args.protocol_sha256, 'exact-reviewed-protocol-hash')
    return Review({'file': path, **bid(raw)}).run()


if __name__ == '__main__':
    raise SystemExit(main())
