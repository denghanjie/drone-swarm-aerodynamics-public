"""Pure bounded GPU-readback byte reference; no I/O or operational imports."""

import hashlib
import struct

U32_MODULUS = 1 << 32
WORD_COUNT = 32
BYTE_COUNT = WORD_COUNT * 4
PREFIX_WORDS = 4
ACTIVE_WORDS = 17
SUFFIX_WORDS = WORD_COUNT - PREFIX_WORDS - ACTIVE_WORDS
WORKGROUP_SIZE = 8
WORKGROUP_COUNT = 3
FIXTURE_ID = 'm31-u32-readback-128-v1'


def initial_words():
    return tuple(0xD15EA5E5 ^ ((j * 0x01010101) % U32_MODULUS)
                 for j in range(WORD_COUNT))


def expected_words():
    words = list(initial_words())
    for i in range(ACTIVE_WORDS):
        product_remainder = divmod(0x9E3779B9 * (i + 1), U32_MODULUS)[1]
        xor_value = product_remainder ^ 0xA5A5A5A5
        words[PREFIX_WORDS + i] = (xor_value + 0x7F4A7C15) % U32_MODULUS
    return tuple(words)


def initial_bytes():
    return struct.pack('<32I', *initial_words())


def expected_bytes():
    return struct.pack('<32I', *expected_words())


def decode_byte_values(values):
    if type(values) is not list or len(values) != BYTE_COUNT:
        raise ValueError('Expected exactly 128 returned byte values')
    if any(type(value) is not int or not 0 <= value <= 255 for value in values):
        raise ValueError('Returned values must be integer bytes; no coercion')
    return bytes(values)


def _bounded_bytes(value):
    # One extra byte allows a bounded reader to detect trailing content.
    if type(value) is not bytes or len(value) > BYTE_COUNT + 1:
        raise ValueError('Evidence must be at most 129 actual bytes')
    return value


def _regions_match(value, expected):
    if len(value) != BYTE_COUNT:
        return {'active': False, 'padding': False}
    start = PREFIX_WORDS * 4
    end = (PREFIX_WORDS + ACTIVE_WORDS) * 4
    return {'active': value[start:end] == expected[start:end],
            'padding': value[:start] == expected[:start] and value[end:] == expected[end:]}


def compare_byte_evidence(returned_values, actual_persisted_bytes):
    """Byte facts only. Does not read files or accept producer phase assertions."""
    returned = decode_byte_values(returned_values)
    persisted = _bounded_bytes(actual_persisted_bytes)
    expected = expected_bytes()
    returned_regions = _regions_match(returned, expected)
    persisted_regions = _regions_match(persisted, expected)
    return {
        'scope': 'byte-comparison-only',
        'expected_bytes': BYTE_COUNT,
        'persisted_bytes': len(persisted),
        'persisted_length_exact': len(persisted) == BYTE_COUNT,
        'returned_sha256': hashlib.sha256(returned).hexdigest(),
        'persisted_sha256': hashlib.sha256(persisted).hexdigest(),
        'expected_sha256': hashlib.sha256(expected).hexdigest(),
        'returned_equals_persisted': returned == persisted,
        'returned_equals_expected': returned == expected,
        'persisted_equals_expected': persisted == expected,
        'returned_active_matches': returned_regions['active'],
        'returned_padding_matches': returned_regions['padding'],
        'persisted_active_matches': persisted_regions['active'],
        'persisted_padding_matches': persisted_regions['padding'],
        'all_bytes_match': returned == persisted == expected,
    }


def receipt_matches_actual(receipt, actual_bytes):
    """Check a size/hash projection against actual bounded bytes, never itself."""
    actual = _bounded_bytes(actual_bytes)
    return (type(receipt) is dict and set(receipt) == {'bytes', 'sha256'}
            and type(receipt['bytes']) is int and receipt['bytes'] == len(actual)
            and type(receipt['sha256']) is str
            and receipt['sha256'] == hashlib.sha256(actual).hexdigest())
