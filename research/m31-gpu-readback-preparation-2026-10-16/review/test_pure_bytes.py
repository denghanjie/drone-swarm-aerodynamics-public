"""Inert fixtures only; no browser, GPU, network, worker or full-checker import."""

import hashlib
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
from byte_primitives import (ACTIVE_WORDS, BYTE_COUNT, PREFIX_WORDS, U32_MODULUS,
                             compare_byte_evidence, decode_byte_values, expected_bytes,
                             expected_words, initial_bytes, initial_words, receipt_matches_actual)


def run():
    tests = []

    def checked(name, condition):
        assert condition, name
        tests.append({'case': name, 'pass': True})

    expected = expected_bytes()
    # A second arithmetic route uses repeated modular addition, not multiplication.
    independently_derived = list(initial_words())
    accumulator = 0
    for i in range(ACTIVE_WORDS):
        accumulator = (accumulator + 0x9E3779B9) & 0xFFFFFFFF
        independently_derived[PREFIX_WORDS + i] = ((accumulator ^ 0xA5A5A5A5) + 0x7F4A7C15) & 0xFFFFFFFF
    checked('independent_repeated_addition_reference', tuple(independently_derived) == expected_words())
    # Independent encoding uses byte extraction rather than struct/native arrays.
    manual_le = bytes((word >> shift) & 255 for word in independently_derived for shift in [0, 8, 16, 24])
    checked('explicit_little_endian_encoding', expected == manual_le)
    checked('all_active_words_differ_from_initial_sentinels', all(expected_words()[j] != initial_words()[j]
            for j in range(PREFIX_WORDS, PREFIX_WORDS + ACTIVE_WORDS)))
    checked('exact_expected_fixture', compare_byte_evidence(list(expected), expected)['all_bytes_match'])

    unchanged = initial_bytes()
    result = compare_byte_evidence(list(unchanged), unchanged)
    checked('missing_dispatch_fixture_is_consistent_but_not_positive', result['returned_equals_persisted']
            and not result['all_bytes_match'] and not result['returned_active_matches'] and result['returned_padding_matches'])

    reversed_words = b''.join(expected[i:i+4][::-1] for i in range(0, BYTE_COUNT, 4))
    result = compare_byte_evidence(list(reversed_words), reversed_words)
    checked('reversed_word_endianness_rejected', result['returned_equals_persisted'] and not result['all_bytes_match']
            and not result['returned_active_matches'] and not result['returned_padding_matches'])

    bad_active = bytearray(expected); bad_active[PREFIX_WORDS * 4 + 7] ^= 1
    result = compare_byte_evidence(list(bad_active), bytes(bad_active))
    checked('one_active_byte_corruption', result['returned_equals_persisted'] and not result['returned_active_matches']
            and result['returned_padding_matches'] and not result['all_bytes_match'])
    bad_padding = bytearray(expected); bad_padding[0] ^= 1
    result = compare_byte_evidence(list(bad_padding), bytes(bad_padding))
    checked('one_prefix_padding_byte_corruption', result['returned_active_matches'] and not result['returned_padding_matches']
            and not result['all_bytes_match'])
    bad_suffix = bytearray(expected); bad_suffix[-1] ^= 1
    checked('last_suffix_padding_byte_corruption', not compare_byte_evidence(list(bad_suffix), bytes(bad_suffix))['returned_padding_matches'])

    for name, persisted in [('short_file', expected[:-1]), ('empty_file', b''), ('trailing_file_byte', expected + b'\0')]:
        result = compare_byte_evidence(list(expected), persisted)
        checked(name, not result['persisted_length_exact'] and not result['returned_equals_persisted'] and not result['all_bytes_match'])
    try:
        compare_byte_evidence(list(expected), expected + b'\0\0')
    except ValueError:
        checked('oversized_evidence_rejected_before_comparison', True)
    else:
        checked('oversized_evidence_rejected_before_comparison', False)

    result = compare_byte_evidence(list(bad_active), expected)
    checked('substituting_expected_file_for_wrong_return_breaks_identity', result['persisted_equals_expected']
            and not result['returned_equals_persisted'] and not result['all_bytes_match'])
    actual_receipt = {'bytes': BYTE_COUNT, 'sha256': hashlib.sha256(bytes(bad_active)).hexdigest()}
    forged_receipt = {'bytes': BYTE_COUNT, 'sha256': hashlib.sha256(expected).hexdigest()}
    checked('honest_wrong_byte_receipt_matches_actual', receipt_matches_actual(actual_receipt, bytes(bad_active)))
    checked('expected_digest_cannot_replace_actual_bytes', not receipt_matches_actual(forged_receipt, bytes(bad_active)))
    checked('boolean_receipt_size_is_rejected', not receipt_matches_actual({'bytes': True, 'sha256': hashlib.sha256(b'\0').hexdigest()}, b'\0'))

    malformed = {'short_array': list(expected[:-1]), 'trailing_array': list(expected) + [0], 'object': {}, 'null': None}
    for name, bad in [('boolean', True), ('float', 1.0), ('negative_zero', -0.0), ('nan', float('nan')),
                      ('infinity', float('inf')), ('string', '1'), ('negative', -1), ('overflow', 256), ('nested', [1])]:
        values = list(expected); values[0] = bad; malformed[name] = values
    for name, values in malformed.items():
        try:
            decode_byte_values(values)
        except ValueError:
            checked('malformed_' + name, True)
        else:
            checked('malformed_' + name, False)

    # Deliberately CPU-created bytes pass byte comparison; this proves no GPU attestation.
    forged_phase_claims = {'gpuExecuted': True, 'copiedWhileMapped': True, 'unmappedBeforeReturn': True, 'destroyedBeforeReturn': True}
    false_phase_claims = {key: False for key in forged_phase_claims}
    independent_result = compare_byte_evidence(list(expected), expected)
    checked('CPU_generated_expected_bytes_can_match_without_GPU_evidence', independent_result['all_bytes_match'])
    checked('producer_phase_claims_are_not_byte_evidence_inputs', forged_phase_claims != false_phase_claims
            and not any(key in independent_result for key in forged_phase_claims)
            and independent_result['scope'] == 'byte-comparison-only')

    # Language-level ownership illustration only, not a WebGPU unmap test.
    mutable_mapping = bytearray(expected)
    alias = memoryview(mutable_mapping)
    owned_copy = bytes(alias)
    alias.release()
    mutable_mapping[:] = bytes(BYTE_COUNT)
    checked('ordinary_owned_copy_survives_original_mutation', owned_copy == expected and bytes(mutable_mapping) != expected)

    return {'kind': 'static-gpu-readback-pure-byte-tests', 'operational_sources_imported': False,
            'browser_gpu_network_operations': False, 'full_checker_executed': False,
            'cases': tests, 'passed': len(tests), 'failed': 0}


if __name__ == '__main__':
    report = run()
    Path(__file__).with_name('PURE-TEST-RESULTS.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'passed': report['passed'], 'failed': report['failed']}))
