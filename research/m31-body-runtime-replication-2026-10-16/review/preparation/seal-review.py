"""One byte-only review freeze write. No reviewer, scientific or runtime execution."""
import time
START = time.monotonic()
import os, signal
def expired(signum, frame):
    os._exit(124)
signal.signal(signal.SIGALRM, expired)
signal.setitimer(signal.ITIMER_REAL, max(.001, START + 15 - time.monotonic()))

import sys, json, hashlib, stat
from pathlib import Path

BASE = Path(__file__).resolve().parents[2]
REPO = BASE.parents[1]
SOURCE = 'f12d8c836e7b991ec33e6de662d00ed05dcce33e'
FREEZE = 'c0c6b2fda84567a76025b2e5f06832cbc1dd5811c23a246df5623f46baf8f8a9'
MANIFEST_SHA = '7ce34e3266c70e95fd715ec30fa95527cd749e9c7ce258ea1492f0d6b717e3e4'
REVIEW_FILES = ['review/IMPLEMENTATION.md', 'review/STATIC-CHALLENGE.md',
                'review/observe-review.py', 'review/source/check-records.py',
                'review/capture-review.py', 'review/preparation/seal-review.py']

def require(ok, code):
    if not ok:
        raise RuntimeError(code)

def read(root, relative, cap=16777216):
    p = Path(relative)
    require(not p.is_absolute() and all(x not in ['', '.', '..'] for x in relative.split('/')), 'contained-input')
    target = root / p
    require(target.resolve() == target and stat.S_ISREG(target.lstat().st_mode)
            and target.stat().st_size <= cap, 'bounded-regular-input')
    with target.open('rb') as handle:
        data = handle.read(cap + 1)
    require(len(data) <= cap, 'input-growth-cap')
    return data

def digest(data):
    return hashlib.sha256(data).hexdigest()

def pin(root, relative):
    data = read(root, relative)
    return {'path': relative, 'bytes': len(data), 'sha256': digest(data)}

def check_pins(root, pins):
    require(isinstance(pins, list) and len(pins) <= 256
            and len({p['path'] for p in pins}) == len(pins), 'unique-pin-list')
    for expected in pins:
        require(pin(root, expected['path']) == expected, 'immutable-byte-pin')

def inventory(folder):
    directory = BASE / folder
    require(directory.is_dir() and not directory.is_symlink(), 'regular-inventory-directory')
    entries = []
    for item in directory.iterdir():
        require(len(entries) < 256 and stat.S_ISREG(item.lstat().st_mode), 'bounded-flat-inventory')
        entries.append(item.name)
    return sorted(entries)

def private_guard(manifest):
    locator = Path(os.environ['M31_RUNTIME_REVIEW_PRIVATE_LOCATIONS'])
    require(locator.is_absolute() and stat.S_ISREG(locator.lstat().st_mode)
            and locator.stat().st_size <= 16384, 'bounded-private-locator')
    with locator.open('rb') as handle:
        data = handle.read(16385)
    require(len(data) <= 16384 and digest(data) == manifest['privateLocatorSHA256'], 'private-locator-pin')
    groups = json.loads(data)
    require(len(groups) == len(manifest['privateGroups']) == 2, 'private-group-count')
    for actual, expected in zip(groups, manifest['privateGroups']):
        require(actual['files'] == expected['files'], 'private-inventory-pin')
        root = Path(actual['path'])
        require(root.is_absolute() and root.is_dir() and not root.is_symlink(), 'private-regular-directory')
        root = root.resolve()
        entries = []
        for item in root.iterdir():
            require(len(entries) < 16 and stat.S_ISREG(item.lstat().st_mode), 'bounded-private-inventory')
            entries.append(item.name)
        require(sorted(entries) == sorted(p['name'] for p in expected['files']), 'exact-private-inventory')
        for item in expected['files']:
            data = read(root, item['name'], 65536)
            require(len(data) == item['bytes'] and digest(data) == item['sha256'], 'private-byte-pin')

def unused_review():
    require(not (BASE / 'review/review-freeze.json').exists()
            and not (BASE / 'review/capture-review.lock').exists(), 'existing-freeze-or-capture-lock')
    results = BASE / 'review/results'
    require(not results.exists() or (results.is_dir() and not results.is_symlink()
            and not list(results.iterdir())), 'existing-review-output-or-lock')

try:
    require(len(sys.argv) == 1, 'fixed-byte-seal-command')
    unused_review()
    with (BASE / 'review/preparation/sole-seal.lock').open('xb') as handle:
        data = b'One byte-only review seal reserved. Preserve on failure; no overwrite.\n'
        require(handle.write(data) == len(data), 'complete-seal-lock')
    fb = read(BASE, 'freeze.json', 1048576)
    require(digest(fb) == FREEZE, 'original-science-freeze')
    frozen = json.loads(fb)
    mb = read(BASE, 'review/science-manifest.json', 1048576)
    require(digest(mb) == MANIFEST_SHA, 'reviewed-science-manifest')
    manifest = json.loads(mb)
    require(manifest['kind'] == 'sealed-terminal-failed-runtime-science' and manifest['sourceCommit'] == SOURCE
            and manifest['sourceFreezeSHA256'] == FREEZE and manifest['scientificStatus'] == 'failed'
            and manifest['scientificQualified'] is False and manifest['decisionVerified'] is False
            and manifest['sourceFiles'] == frozen['files'] and len(frozen['files']) == 57, 'fixed-terminal-scope')
    check_pins(REPO, frozen['files'])
    check_pins(BASE, manifest['terminalFiles'])
    require(len(manifest['terminalFiles']) == 32, 'exact-terminal-pin-count')
    for folder, count in [('raw', 22), ('results', 7), ('publication', 2)]:
        expected = sorted(p['path'].split('/', 1)[1] for p in manifest['terminalFiles'] if p['path'].startswith(folder + '/'))
        require(len(expected) == count and inventory(folder) == expected, 'exact-terminal-inventory')
    private_guard(manifest)
    budget, capture, publication = [json.loads(read(BASE, p, 65536)) for p in
            ['results/budget.json', 'results/capture.json', 'publication/science-capture-execution.json']]
    require(budget['terminal'] is True and budget['active'] is False and budget['processClosureComplete'] is True
            and budget['outputAccountingComplete'] is True and capture['terminal'] is True
            and capture['actualObserverExitCode'] == 1 and capture['observerReaped'] is True
            and publication['actualCaptureExitCode'] == 1 and publication['toolSessionCompleted'] is True,
            'terminal-failed-science-precondition')
    review_pins = [pin(BASE, path) for path in sorted(REVIEW_FILES)]
    require(all(0 < p['bytes'] <= 1048576 for p in review_pins), 'nonempty-review-source-read-caps')
    record = {'kind': 'frozen-saved-failure-record-review', 'sourceCommit': SOURCE,
              'sourceFreezeSHA256': FREEZE, 'invocations': 1, 'wallSeconds': 120,
              'outputByteCap': 33554432, 'scienceManifest': pin(BASE, 'review/science-manifest.json'),
              'files': review_pins,
              'scope': 'One saved failed-record integrity review. No scientific or runtime execution; qualification and decision verification remain false.',
              'preparation': 'Byte-only sealer is itself pinned. Its preparation lock is outside runtime results; all scientific evidence remains immutable.'}
    # Recheck immutable inputs and the exact source set immediately before write.
    check_pins(REPO, frozen['files'])
    check_pins(BASE, manifest['terminalFiles'])
    private_guard(manifest)
    check_pins(BASE, review_pins)
    require(read(BASE, 'freeze.json') == fb and read(BASE, 'review/science-manifest.json') == mb, 'immutable-freezes-and-manifest')
    unused_review()
    encoded = (json.dumps(record, indent=2) + '\n').encode()
    require(len(encoded) <= 16384, 'review-freeze-size-cap')
    with (BASE / 'review/review-freeze.json').open('xb') as handle:
        require(handle.write(encoded) == len(encoded), 'complete-exclusive-freeze')
    summary = (json.dumps({'kind': 'byte-only-review-freeze-created', 'bytes': len(encoded),
                           'sha256': digest(encoded), 'sourcePins': len(review_pins),
                           'reviewExecuted': False, 'scientificExecuted': False}) + '\n').encode()
    if os.write(sys.stdout.fileno(), summary) != len(summary):
        os._exit(125)
except BaseException as error:
    message = (json.dumps({'kind': 'byte-only-review-seal-failed', 'type': type(error).__name__,
                           'code': str(error) if type(error) is RuntimeError else 'seal-operation-failed',
                           'retryPermitted': False, 'preserveAllPartialFiles': True}) + '\n').encode()
    if os.write(sys.stdout.fileno(), message) != len(message):
        os._exit(125)
    raise SystemExit(1)
