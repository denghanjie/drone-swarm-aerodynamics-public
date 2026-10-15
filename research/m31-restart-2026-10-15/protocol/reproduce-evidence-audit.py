#!/usr/bin/env python3
"""Recompare existing M31/M32 records. No simulator is imported or executed.

Usage: python3 reproduce-evidence-audit.py --source-root /path/to/repository \
    --output /path/to/owned-output/read-only-evidence-audit.json
"""
import argparse
import array
import hashlib
import json
import math
from pathlib import Path
import sys


def read_doubles(path):
    raw = path.read_bytes()
    if len(raw) % 8:
        raise ValueError(f'Invalid Float64 byte count: {path.name}')
    values = array.array('d')
    values.frombytes(raw)
    if sys.byteorder != 'little':
        values.byteswap()
    return values


def compare(root, first, second, count, width):
    a, b = read_doubles(root / first), read_doubles(root / second)
    stride = 1 + width * count
    if len(a) % stride or len(b) % stride:
        raise ValueError('Frame length does not match declared count and width')
    times_a = {round(a[k], 9): k for k in range(0, len(a), stride)}
    times_b = {round(b[k], 9): k for k in range(0, len(b), stride)}
    if len(times_a) != len(a) // stride or len(times_b) != len(b) // stride:
        raise ValueError('Duplicate time keys')
    common = sorted(set(times_a) & set(times_b))
    if not common:
        raise ValueError('No common saved times')
    maximum, first_exceedance, maximum_at = 0.0, None, None
    max_time_discrepancy = max(abs(a[times_a[t]] - b[times_b[t]]) for t in common)
    for time in common:
        ka, kb = times_a[time] + 1, times_b[time] + 1
        for drone in range(count):
            ia, ib = ka + drone * width, kb + drone * width
            error = math.sqrt(sum((a[ia + j] - b[ib + j]) ** 2 for j in range(3)))
            if not math.isfinite(error):
                raise ValueError('Nonfinite position difference')
            if error > maximum:
                maximum, maximum_at = error, {'t': time, 'drone': drone}
            if first_exceedance is None and error >= 0.01:
                first_exceedance = time
    return {
        'a': first, 'b': second, 'count': count, 'commonFrames': len(common),
        'firstTime': common[0], 'lastTime': common[-1],
        'maximumPositionDifference_m': maximum, 'maximumAt': maximum_at,
        'firstSavedTimeAtOrAbove1cm': first_exceedance,
        'maxPairedTimestampDiscrepancy_s': max_time_discrepancy,
        'rawPairedTimestampsExactlyEqual': max_time_discrepancy == 0.0,
        'comparisonTimeMode': 'raw timestamps exactly equal' if max_time_discrepancy == 0.0 else 'rounded-key matched; raw timestamps differ; not an exact-common-time comparison',
    }


def audit(root):
    checks = []
    protocol = json.loads((root / 'outputs/milestone-31-protocol.json').read_text())
    for name, expected in protocol['sourceHashes'].items():
        path = (root / 'outputs/milestone-31-source' / name).resolve()
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        checks.append({'file': str(path.relative_to(root)), 'expected': expected,
                       'actual': actual, 'match': actual == expected})
    for filename in ['milestone-32-protocol.json', 'milestone-32-checkpoint-protocol.json']:
        protocol = json.loads((root / 'outputs' / filename).read_text())
        for category, base in [('sourceHashes', root / 'outputs/milestone-32-source'),
                               ('inputHashes', root / 'outputs')]:
            for name, expected in protocol.get(category, {}).items():
                path = (base / name).resolve()
                actual = hashlib.sha256(path.read_bytes()).hexdigest()
                checks.append({'file': str(path.relative_to(root)), 'expected': expected,
                               'actual': actual, 'match': actual == expected})
    m31 = []
    for count, seed, course in [(1000, 2001, 'wide'), (1000, 2002, 'narrow'),
                                (5000, 2001, 'wide')]:
        first = f'outputs/milestone-31-source/heldout-{seed}-{count}-{course}-wall-priority-0.0025.f64'
        kind = 'window-refinement' if count == 5000 else 'refinement'
        second = f'outputs/milestone-31-source/{kind}-{seed}-{count}-{course}-wall-priority-0.00125.f64'
        m31.append(compare(root, first, second, count, 7))
    m32 = []
    for first, second in [('closed-0.0025', 'closed-0.00125'),
                          ('closed-0.00125', 'closed-0.000625'),
                          ('closed-0.0025', 'replayed-0.00125'),
                          ('replayed-0.00125', 'replayed-0.000625'),
                          ('closed-0.0025', 'fine-start-0.0025')]:
        m32.append(compare(root, f'outputs/milestone-32-source/{first}-positions.f64',
                           f'outputs/milestone-32-source/{second}-positions.f64', 1000, 3))
    return {
        'scope': 'Read-only audit of existing artifact hashes and saved-time-key binary position comparisons; raw paired timestamp equality and maximum discrepancy are explicitly checked per comparison; no simulator imports, solver runs or frozen-source edits in this script. Hashes validate consistency with protocols, not physical accuracy or independent replication.',
        'sourceRoot': 'PUBLIC_REPOSITORY',
        'sourceRootRedaction': 'Metadata-only replacement of the original machine-specific absolute path and normalization of relative artifact path spelling; input bytes, hash values and numerical comparison values are unchanged.',
        'reproductionScript': 'reproduce-evidence-audit.py',
        'runtime': {'pythonVersion': sys.version.split()[0], 'byteOrder': sys.byteorder},
        'timeMatching': 'Match saved timestamp keys rounded to 9 decimal places; reject duplicate/colliding keys; no interpolation. Compare every raw paired timestamp explicitly and report its maximum discrepancy. Exact-common-time language is valid only for records with rawPairedTimestampsExactlyEqual=true.',
        'checkpointScopeNote': 'The wider checkpoint executed no new full-swarm trajectory campaign. A separate evidence audit performed six single-drone RK4 contact-replay consistency steps; this script performs none.',
        'sourceHashChecks': checks,
        'm31RecomputedComparisons': m31,
        'm32RecomputedComparisons': m32,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-root', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    root, output = args.source_root.resolve(), args.output.resolve()
    if output == root or root in output.parents:
        parser.error('--output must be outside the source repository to preserve frozen artifacts')
    record = audit(root)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(record, indent=2) + '\n')
    print(json.dumps({'hashChecks': len(record['sourceHashChecks']),
                      'allHashesMatch': all(x['match'] for x in record['sourceHashChecks']),
                      'm31Comparisons': len(record['m31RecomputedComparisons']),
                      'm32Comparisons': len(record['m32RecomputedComparisons'])}))


if __name__ == '__main__':
    main()
