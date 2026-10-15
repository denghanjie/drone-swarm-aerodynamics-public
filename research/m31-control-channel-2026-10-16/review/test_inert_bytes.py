"""Exercise only pure byte predicates; never import any diagnostic/checker."""

import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
from byte_evidence import byte_array, compare_bytes


def main():
    # A local inert 4-byte fixture keeps the malformed cases readable.
    fixture = bytes([19, 92, 165, 238])
    malformed = {
        "object_instead_of_array": {"0": 19},
        "null": None,
        "short_array": [19, 92, 165],
        "long_array": [19, 92, 165, 238, 55],
        "boolean_is_not_integer": [True, 92, 165, 238],
        "integral_float_is_not_json_integer": [19.0, 92, 165, 238],
        "negative_zero_is_not_integer_byte": [-0.0, 92, 165, 238],
        "nan_is_not_integer_byte": [float('nan'), 92, 165, 238],
        "infinity_is_not_integer_byte": [float('inf'), 92, 165, 238],
        "string_is_not_integer": ["19", 92, 165, 238],
        "negative_byte": [-1, 92, 165, 238],
        "overflow_byte": [256, 92, 165, 238],
        "nested_array": [[19], 92, 165, 238],
    }
    outcomes = []
    for name, value in malformed.items():
        rejected = False
        try:
            byte_array(value, len(fixture))
        except ValueError:
            rejected = True
        assert rejected, name
        outcomes.append({"case": name, "pass": True})
    correct = compare_bytes(list(fixture), fixture, fixture)
    assert correct["persisted_matches_returned"]
    assert correct["returned_matches_fixture"]
    assert correct["persisted_matches_fixture"]
    outcomes.append({"case": "correct_array_and_file", "pass": True})
    wrong = bytes([20, 92, 165, 238])
    consistent_failure = compare_bytes(list(wrong), wrong, fixture)
    assert consistent_failure["persisted_matches_returned"]
    assert not consistent_failure["returned_matches_fixture"]
    assert not consistent_failure["persisted_matches_fixture"]
    outcomes.append({"case": "wrong_valid_bytes_are_consistent_failed_transfer", "pass": True})
    tampered = compare_bytes(list(fixture), wrong, fixture)
    assert not tampered["persisted_matches_returned"]
    assert tampered["returned_matches_fixture"]
    assert not tampered["persisted_matches_fixture"]
    outcomes.append({"case": "changed_persisted_file_breaks_evidence_agreement", "pass": True})
    # Full expected length uses synthetic bytes only, with no campaign read.
    synthetic = bytes((73 * i + 19) % 256 for i in range(3840))
    assert byte_array(list(synthetic)) == synthetic
    outcomes.append({"case": "full_length_inert_synthetic_array", "pass": True})
    report = {"kind": "inert-byte-predicate-tests", "operational_sources_imported": False,
              "actual_campaign_evidence_read": False, "cases": outcomes,
              "passed": len(outcomes), "failed": 0}
    Path(__file__).with_name("INERT-BYTE-RESULTS.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"passed": len(outcomes), "failed": 0}))


if __name__ == "__main__":
    main()
