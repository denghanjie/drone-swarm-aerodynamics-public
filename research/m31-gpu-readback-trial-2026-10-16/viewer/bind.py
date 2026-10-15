"""Future presentation binding of closed actual records. Source preparation only.

This adapter does not import or invoke the diagnostic, GPU page or saved checker.
It must be installed in the new trial's viewer/ directory before explicit use.
"""
from pathlib import Path
import hashlib
import json
import os
import stat
import sys

CAMPAIGN = 'm31-gpu-readback-trial-2026-10-16'
CAP = 8388608
FILES = {
    'expected': 'expected.bin',
    'returned': 'raw/returned.json',
    'received': 'raw/received.bin',
    'rejectedReturn': 'raw/rejected-return.json',
    'trace': 'raw/trace.public.ndjson',
    'host': 'results/result.json',
    'relay': 'results/wrapper.json',
    'budget': 'results/budget.json',
    'capture': 'results/capture.json',
    'captureExecution': 'publication/capture-execution.json',
    'captureOutput': 'publication/capture-output.json',
    'observerOutput': 'publication/observer-output.json',
    'reviewReport': 'review/results/report.json',
    'reviewSummary': 'review/results/summary.json',
    'reviewManifest': 'review/evidence-manifest.json',
    'reviewSupervisor': 'publication/review-supervisor.json',
    'reviewOutput': 'publication/review-output.json',
    'reviewExecution': 'publication/review-execution.json',
    'disposition': 'publication/FINAL-DISPOSITION.json',
    'freeze': 'freeze.json',
}


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def read_regular(base, relative, remaining):
    path = base / relative
    cursor = base
    for part in Path(relative).parts:
        cursor /= part
        require(not cursor.is_symlink(), 'Symlink evidence is not admitted')
    require(path.resolve().is_relative_to(base), 'Evidence must remain in the trial directory')
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    try:
        before = os.fstat(fd)
        require(stat.S_ISREG(before.st_mode) and 0 <= before.st_size <= remaining, 'Regular evidence file within aggregate cap required')
        chunks = []
        total = 0
        while True:
            chunk = os.read(fd, min(65536, before.st_size + 1 - total))
            if not chunk:
                break
            total += len(chunk)
            require(total <= before.st_size, 'Evidence grew during read')
            chunks.append(chunk)
        after = os.fstat(fd)
        require((before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns, before.st_ctime_ns) ==
                (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns, after.st_ctime_ns) and total == before.st_size,
                'Evidence changed during read')
        return b''.join(chunks)
    finally:
        os.close(fd)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def encode(value):
    return (json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + '\n').encode('utf-8')


def main():
    require(len(sys.argv) == 2 and Path(sys.argv[1]).is_absolute(), 'One absolute closed trial directory required')
    base = Path(sys.argv[1]).resolve()
    require(base.name == CAMPAIGN, 'This adapter is scoped to the new GPU-readback trial')
    viewer = base / 'viewer'
    require(viewer.resolve() == viewer and Path(__file__).resolve().parent == viewer, 'Install the source in the new trial viewer directory first')
    require(not (viewer / 'evidence.json').exists() and not (viewer / 'binding.json').exists(), 'Binding outputs are exclusive and must not already exist')
    disposition_bytes = read_regular(base, FILES['disposition'], 65536)
    disposition = json.loads(disposition_bytes)
    require(type(disposition) is dict and disposition.get('diagnosticTerminal') is True and
            disposition.get('savedReviewTerminal') is True and disposition.get('scientificQualified') is False,
            'Actual root disposition must mark both stages closed and scientific qualification false')
    require(type(disposition.get('byteReadbackVerifiedWithinFixture')) is bool,
            'Root disposition must explicitly retain its scoped verification result')
    descriptors = []
    total = 0
    for role, relative in FILES.items():
        path = base / relative
        require(not path.is_symlink(), 'Symlink evidence is not admitted')
        if not path.exists():
            continue
        data = read_regular(base, relative, CAP - total)
        if role == 'disposition':
            require(data == disposition_bytes, 'Terminal disposition changed during binding')
        total += len(data)
        descriptors.append({'role': role, 'path': '../' + relative, 'bytes': len(data), 'sha256': digest(data)})
    artifact = {'schema': 'm31-gpu-readback-view-v1', 'campaign': CAMPAIGN,
                'fixtureId': 'm31-u32-readback-128-v1', 'files': descriptors}
    encoded = encode(artifact)
    binding = encode({'schema': 'm31-gpu-readback-view-binding-v1', 'path': './evidence.json',
                      'bytes': len(encoded), 'sha256': digest(encoded)})
    require(len(encoded) <= 32768 and len(binding) <= 16384, 'Bounded presentation manifest')
    with (viewer / 'evidence.json').open('xb') as handle:
        require(handle.write(encoded) == len(encoded), 'Complete evidence-manifest write')
    with (viewer / 'binding.json').open('xb') as handle:
        require(handle.write(binding) == len(binding), 'Complete binding write')
    print(json.dumps({'kind': 'gpu-readback-view-binding-created', 'actualFiles': len(descriptors),
                      'actualBackingBytes': total, 'evidenceBytes': len(encoded), 'evidenceSHA256': digest(encoded),
                      'diagnosticInvoked': False, 'savedReviewInvoked': False,
                      'outcomeDerivedByAdapter': False}))


if __name__ == '__main__':
    main()
