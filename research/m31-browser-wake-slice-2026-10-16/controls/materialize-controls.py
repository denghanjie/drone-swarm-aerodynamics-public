"""Static literal encoding only: no geometry, wake, root or shader evaluation."""
import hashlib
import json
import pathlib
import struct

ROOT = pathlib.Path(__file__).resolve().parent
UNSET = 0xffffffff

def encoded(value):
    return struct.unpack('<I', struct.pack('<f', value))[0]

def control(index, name, kind, scalars=None, self_flag=0, source=None,
            receiver=None, source_axis=None, receiver_axis=None, offset=None,
            mutations=None, status=3, code=0, validity=2048, routing=16,
            term='zero-valid'):
    words = [0] * 32
    words[0:4] = [index, kind, self_flag, 0]
    if scalars is not None:
        for slot, value in zip(range(4, 12), scalars):
            words[slot] = encoded(value)
    for start, values in [(12, source), (16, receiver), (20, source_axis),
                          (24, receiver_axis), (28, offset)]:
        if values is not None:
            for component, value in enumerate(values):
                words[start + component] = encoded(value)
    for slot, value in mutations or []:
        words[slot] = value
    return {'id': index, 'name': name, 'kind': kind, 'words': words,
            'expected': {'ordinal': index, 'receiverID': 0,
                         'sourceID': 0 if self_flag else 1, 'rotor': 0,
                         'status': status, 'policyCode': code,
                         'validityMask': validity, 'routingFlags': routing,
                         'termAssertion': term}}

# Scalar tuple: centerNorm, down, radial, halfWidth, axisDot,
#               normalizedDown, xi, radialRatio.
# These are explicit synthetic stage interfaces, not pose reconstructions.
rows = [
    control(0, 'self-before-outside-and-near', 0,
            [4, .1, 0, .125, 0, 4, 0, 0], self_flag=1, routing=17),
    control(1, 'outside-before-near-and-projection', 0,
            [3, .1, 0, .125, 0, 4, 0, 0], validity=2049, routing=18),
    control(2, 'down-zero-before-near', 0,
            [0, 0, 0, .125, 0, 4, 0, 0], code=1, validity=2051),
    control(3, 'down-cutoff-before-near-and-projection', 0,
            [0, 2.5, 0, .125, 0, 4, 0, 0], code=2, validity=2051),
    control(4, 'near-invalid-before-zero-projection', 0,
            [0, .0625, 0, .125, 0, 4, 0, 0], status=2, code=3,
            validity=7, term='zero-placeholder-not-valid'),
    control(5, 'near-invalid-before-radial-cutoff', 0,
            [0, .0625, .1, .015625, 1, 4, 0, 0], status=2, code=3,
            validity=7, term='zero-placeholder-not-valid'),
    control(6, 'near-radius-equality-skips', 0,
            [0, .0625, .15, .125, 1, 4, 0, 0], code=4, validity=2055),
    control(7, 'radial-cutoff-before-zero-projection', 0,
            [0, 1, .5, .125, 0, 4, 0, 0], code=5, validity=2127),
    control(8, 'profile-with-zero-projection', 0,
            [0, 1, 0, .125, 0, 4, 0, 0], status=4, code=6, validity=4095),
    control(9, 'profile-with-negative-projection', 0,
            [0, 1, 0, .125, -1, 4, 0, 0], status=4, code=6, validity=4095),
    control(10, 'profile-positive-sign-only', 0,
            [0, 1, 0, .125, 1, 4, 0, 0], status=5, code=7,
            validity=4095, term='finite-strictly-positive'),
    control(11, 'profile-valid-zero-radial-fade-endpoint', 0,
            [0, 1, .125, .125, 1, 4, 1, 3], status=4, code=7,
            validity=4095, routing=24),
    control(12, 'full-prepared-near-domain-rejection', 1,
            source=[0, 0, .0625], receiver=[0, 0, 0],
            source_axis=[0, 0, 1], receiver_axis=[0, 0, 1],
            offset=[0, 0, 0], status=2, code=3, validity=7,
            routing=48, term='zero-placeholder-not-valid'),
    control(13, 'raw-nan-before-float-reinterpretation', 1,
            source=[0, 0, .0625], receiver=[0, 0, 0],
            source_axis=[0, 0, 1], receiver_axis=[0, 0, 1],
            offset=[0, 0, 0], mutations=[(12, 0x7fc00000)],
            status=1, code=UNSET, validity=0, routing=48,
            term='zero-placeholder-not-valid'),
    control(14, 'nonzero-padding-rejected', 0,
            [0, 1, 0, .125, 1, 4, 0, 0], mutations=[(3, 1)],
            status=1, code=UNSET, validity=0, routing=16,
            term='zero-placeholder-not-valid'),
    control(15, 'full-prepared-outside-center-zero', 1,
            source=[4, 0, 0], receiver=[0, 0, 0],
            source_axis=[0, 0, 1], receiver_axis=[0, 0, 1],
            offset=[0, 0, 0], status=3, code=0,
            validity=2049, routing=50),
]

payload = b''.join(struct.pack('<32I', *row['words']) for row in rows)
record = {'status': 'STATIC_LITERAL_MATERIALIZATION_ONLY',
          'recordCount': 16, 'inputStrideBytes': 128,
          'outputStrideBytes': 80,
          'inputSha256': hashlib.sha256(payload).hexdigest(),
          'scope': 'Shared policy/profile helper controls; only records12and15'
                   ' exercise complete finite prepared geometry. Record13 is a'
                   ' raw-input guard. Scalar records are synthetic interfaces.'
                   ' No control wake/geometry/root value was evaluated here.',
          'numericalExpectation': 'Exact identities, statuses, codes, flags and'
                                  ' valid-zero/invalid-placeholder/positive sign'
                                  ' only; no positive term magnitude claim.',
          'controls': rows}
(ROOT / 'controls.u32').write_bytes(payload)
(ROOT / 'controls.json').write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps({'bytes': len(payload), 'sha256': record['inputSha256'],
                  'records': len(rows)}))
