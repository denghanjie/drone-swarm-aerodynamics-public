#!/usr/bin/env python3
"""Independent saved-result checker. Authoring this file does not run it.

Only the Python standard library is used. No implementation module is imported,
and no process or network operation is performed. The external supervisor owns
the prospective wall/RSS limits. All fixture generation happens inside main at
the single separately authorized execution, never while importing this module.
"""

import argparse
from collections import Counter
import copy
from fractions import Fraction
import hashlib
import json
from math import isqrt
from pathlib import Path, PurePosixPath
import re
import sys


MAX_INPUT_BYTES = 16 * 1024 * 1024
MAX_MANIFEST_BYTES = 1024 * 1024
MAX_SPEC_BYTES = 65536
MAX_SOURCE_BYTES = 16 * 1024 * 1024
MAX_SOURCE_TOTAL = 64 * 1024 * 1024
MAX_SOURCE_FILES = 256
MAX_ERRORS = 32
EXPECTED_RECORDS = 1488
STATUSES = ("ok", "invalid-nonfinite", "unresolved-domain", "unresolved-range",
            "unresolved-iteration", "unresolved-sqrt-check", "invalid-bits",
            "invalid-interval")


class CheckError(Exception):
    """An intentionally public-safe validation failure."""


def require(condition, code):
    if not condition:
        raise CheckError(code)


def canonical_integer(value):
    require(isinstance(value, str) and len(value) <= 128,
            "endpoint-string-shape")
    require(re.fullmatch(r"0|-?[1-9][0-9]*", value) is not None,
            "endpoint-string-syntax")
    return int(value)


def pairs_without_duplicates(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, "duplicate-json-key")
        result[key] = value
    return result


def reject_json_constant(_value):
    raise CheckError("nonfinite-json-number")


def same_json(left, right):
    """Structural equality without Python's True == 1 or 1.0 == 1 aliases."""
    if type(left) is not type(right):
        return False
    if isinstance(left, dict):
        return set(left) == set(right) and all(same_json(left[k], right[k]) for k in left)
    if isinstance(left, list):
        return len(left) == len(right) and all(same_json(a, b) for a, b in zip(left, right))
    return left == right


def load_json(path, limit):
    require(path.is_file(), "required-file-missing")
    require(path.stat().st_size <= limit, "input-file-budget")
    with path.open("rb") as handle:
        data = handle.read(limit + 1)
    require(len(data) <= limit, "input-file-budget")
    try:
        return json.loads(data, object_pairs_hook=pairs_without_duplicates,
                          parse_constant=reject_json_constant)
    except (UnicodeError, ValueError, RecursionError):
        raise CheckError("invalid-json") from None


def relative_name(path, root):
    try:
        relative = path.resolve(strict=True).relative_to(root)
    except (OSError, ValueError):
        raise CheckError("input-path-outside-root-or-missing") from None
    require(relative.parts and not any(p in (".", "..") for p in relative.parts),
            "invalid-relative-path")
    return relative.as_posix()


def file_sha256(path, limit=MAX_SOURCE_BYTES):
    h = hashlib.sha256()
    total = 0
    with path.open("rb") as handle:
        while True:
            block = handle.read(65536)
            if not block:
                break
            total += len(block)
            require(total <= limit, "source-file-budget")
            h.update(block)
    return total, h.hexdigest()


def verify_manifest(manifest_path, root, spec_path, contract_path):
    manifest = load_json(manifest_path, MAX_MANIFEST_BYTES)
    require(isinstance(manifest, dict), "manifest-object-required")
    files = manifest.get("files")
    require(isinstance(files, list) and 1 <= len(files) <= MAX_SOURCE_FILES,
            "manifest-file-count")
    seen = set()
    verified = []
    total = 0
    for item in files:
        require(isinstance(item, dict), "manifest-record-object")
        name = item.get("path")
        require(isinstance(name, str) and len(name) <= 512 and "\\" not in name,
                "manifest-path-shape")
        parts = PurePosixPath(name)
        require(not parts.is_absolute() and str(parts) == name and
                all(part not in (".", "..") for part in parts.parts),
                "manifest-path-not-relative")
        require(name not in seen, "duplicate-manifest-path")
        seen.add(name)
        size = item.get("bytes")
        expected_sha = item.get("sha256")
        require(type(size) is int and 0 <= size <= MAX_SOURCE_BYTES,
                "manifest-size-shape")
        require(isinstance(expected_sha, str) and
                re.fullmatch(r"[0-9a-f]{64}", expected_sha) is not None,
                "manifest-hash-shape")
        source_path = root / name
        require(relative_name(source_path, root) == name,
                "manifest-noncanonical-file-path")
        actual_size, actual_sha = file_sha256(source_path)
        total += actual_size
        require(total <= MAX_SOURCE_TOTAL, "source-total-budget")
        require(actual_size == size and actual_sha == expected_sha,
                "source-manifest-pin-mismatch")
        verified.append({"path": name, "bytes": size, "sha256": actual_sha})
    require(relative_name(spec_path, root) in seen, "spec-not-source-pinned")
    require(relative_name(contract_path, root) in seen,
            "result-contract-not-source-pinned")
    require(relative_name(Path(__file__), root) in seen,
            "checker-not-source-pinned")
    return verified


def parse_lattice_token(token, scale, maximum):
    require(isinstance(token, str) and len(token) <= 64,
            "invalid-interval-token")
    if re.fullmatch(r"0|-?[1-9][0-9]*", token):
        return int(token)
    match = re.fullmatch(r"(-?)([1-9][0-9]*)?([SM])(?:(/)([1-9][0-9]*)|([+-])([0-9]+))?",
                         token)
    require(match is not None, "unsupported-interval-token")
    sign, multiplier, symbol, divide, denominator, adjustment, amount = match.groups()
    value = (scale if symbol == "S" else maximum) * int(multiplier or "1")
    if sign:
        value = -value
    if divide:
        divisor = int(denominator)
        require(value % divisor == 0, "noninteger-interval-token")
        value //= divisor
    if adjustment:
        value += int(amount) * (1 if adjustment == "+" else -1)
    return value


def regenerate_inputs(spec):
    """Independent stream consumption; no runner-supplied fixture is trusted."""
    require(isinstance(spec, dict), "spec-object-required")
    approved = {
        "id": "m31-fixed96-primitives-v1", "fractionBits": 96,
        "maxEndpointPower": 352, "modulusPower": 64,
        "generatedBits": 128, "generatedIntervals": 128,
        "pairs": 256, "expectedRecords": EXPECTED_RECORDS,
        "generatedPairs": 208,
        "seedHex": "6a09e667f3bcc909", "multiplier": "6364136223846793005",
        "increment": "1442695040888963407",
        "intervalRule": "After all generatedBits draws, each interval consumes three LCG draws: a=(next mod 2^40)-2^39, b likewise; shift=next mod 310. Endpoints are sorted(a,b)*2^shift. All endpoints fit within +/-2^352. No rejection resampling.",
        "pairRule": "48 explicitPairs first. After all interval draws, each of 208 generated pairs consumes two draws; each index is (next >> 32) modulo totalIntervalCount. Each pair is used for add, sub, mul, div in that order. High bits avoid the former forced left-even/right-odd parity; no statistical independence claim.",
        "order": "All 160 fromBits cases first; then square and sqrt for each of 152 intervals; then add/sub/mul/div for each of 256 pairs.",
    }
    require(all(type(spec.get(k)) is type(v) and spec[k] == v
                for k, v in approved.items()), "spec-allocation-changed")
    explicit_bits = spec.get("explicitBits")
    explicit_intervals = spec.get("explicitIntervals")
    require(isinstance(explicit_bits, list) and len(explicit_bits) == 32,
            "explicit-bits-count")
    require(all(isinstance(v, str) and re.fullmatch(r"[0-9a-f]{16}", v)
                for v in explicit_bits), "explicit-bits-shape")
    require(isinstance(explicit_intervals, list) and len(explicit_intervals) == 24,
            "explicit-intervals-count")
    scale = 1 << spec["fractionBits"]
    maximum = 1 << spec["maxEndpointPower"]
    state = int(spec["seedHex"], 16)
    modulus = 1 << spec["modulusPower"]
    multiplier = int(spec["multiplier"])
    increment = int(spec["increment"])

    def draw():
        nonlocal state
        state = (state * multiplier + increment) % modulus
        return state

    bits = list(explicit_bits)
    for _ in range(spec["generatedBits"]):
        bits.append(format(draw(), "016x"))
    intervals = []
    for row in explicit_intervals:
        require(isinstance(row, list) and len(row) == 2,
                "explicit-interval-shape")
        lo, hi = (parse_lattice_token(v, scale, maximum) for v in row)
        require(-maximum <= lo <= hi <= maximum, "explicit-interval-range")
        intervals.append((lo, hi))
    for _ in range(spec["generatedIntervals"]):
        first = (draw() % (1 << 40)) - (1 << 39)
        second = (draw() % (1 << 40)) - (1 << 39)
        factor = 1 << (draw() % 310)
        lo, hi = sorted((first * factor, second * factor))
        require(-maximum <= lo <= hi <= maximum, "generated-interval-range")
        intervals.append((lo, hi))
    explicit_pairs = spec.get("explicitPairs")
    require(isinstance(explicit_pairs, list) and len(explicit_pairs) == 48,
            "explicit-pairs-count")
    pairs = []
    for pair in explicit_pairs:
        require(isinstance(pair, list) and len(pair) == 2 and
                all(type(v) is int and 0 <= v < len(intervals) for v in pair),
                "explicit-pair-index")
        pairs.append(tuple(pair))
    for _ in range(spec["generatedPairs"]):
        pairs.append(((draw() >> 32) % len(intervals),
                      (draw() >> 32) % len(intervals)))
    require(len(pairs) == spec["pairs"], "total-pairs-count")
    return scale, maximum, bits, intervals, pairs


def bits_to_fraction(bits):
    word = int(bits, 16)
    exponent = (word >> 52) & 2047
    significand = word & ((1 << 52) - 1)
    if exponent == 2047:
        return None
    if exponent == 0:
        value = Fraction(significand, 1 << 1074)
    else:
        significand += 1 << 52
        power = exponent - 1075
        value = (Fraction(significand << power) if power >= 0
                 else Fraction(significand, 1 << -power))
    return -value if word >> 63 else value


def floor_fraction(value):
    return value.numerator // value.denominator


def ceil_fraction(value):
    return -((-value.numerator) // value.denominator)


def exact_image(operation, operands, scale):
    """Return status, rational image, and optional sqrt squared-image bounds."""
    if operation == "fromBits":
        exact = bits_to_fraction(operands)
        return (("invalid-nonfinite", None, None) if exact is None
                else ("ok", (exact, exact), None))
    a = tuple(Fraction(v, scale) for v in operands[0])
    if operation == "sqrt":
        if a[0] < 0:
            return "unresolved-domain", None, None
        return "ok", None, a
    if operation == "square":
        lower = Fraction(0) if a[0] <= 0 <= a[1] else min(a[0] ** 2, a[1] ** 2)
        return "ok", (lower, max(a[0] ** 2, a[1] ** 2)), None
    b = tuple(Fraction(v, scale) for v in operands[1])
    if operation == "add":
        image = (a[0] + b[0], a[1] + b[1])
    elif operation == "sub":
        image = (a[0] - b[1], a[1] - b[0])
    elif operation == "mul":
        corners = [x * y for x in a for y in b]
        image = (min(corners), max(corners))
    elif operation == "div":
        if b[0] <= 0 <= b[1]:
            return "unresolved-domain", None, None
        corners = [x / y for x in a for y in b]
        image = (min(corners), max(corners))
    else:
        raise CheckError("undeclared-operation")
    return "ok", image, None


def expected_result(operation, operands, scale, maximum):
    status, rational_image, square_image = exact_image(operation, operands, scale)
    if status != "ok":
        return {"status": status, "image": None, "squareImage": None}
    if square_image is not None:
        low_squared = square_image[0] * scale * scale
        high_squared = square_image[1] * scale * scale
        lo = isqrt(floor_fraction(low_squared))
        hi_floor = isqrt(floor_fraction(high_squared))
        hi = hi_floor if hi_floor * hi_floor == high_squared else hi_floor + 1
    else:
        lo = floor_fraction(rational_image[0] * scale)
        hi = ceil_fraction(rational_image[1] * scale)
    if lo < -maximum or hi > maximum:
        return {"status": "unresolved-range", "image": rational_image,
                "squareImage": square_image}
    return {"status": "ok", "lo": lo, "hi": hi,
            "image": rational_image, "squareImage": square_image}


def read_contract(contract_path):
    contract = load_json(contract_path, MAX_SPEC_BYTES)
    require(isinstance(contract, dict), "result-contract-object-required")
    required_lists = {
        "documentFields": ["schema", "specId", "runtime", "sourceSha256", "records"],
        "runtimeFields": ["node", "v8", "platform", "arch"],
        "sourceSha256Keys": ["interval.cjs", "spec.json", "run.cjs"],
        "recordFields": ["id", "op", "input", "result", "inputUnchanged"],
        "operations": ["fromBits", "square", "sqrt", "add", "sub", "mul", "div"],
    }
    require(contract.get("documentSchema") == "m31-fixed96-result-v1",
            "result-contract-schema-changed")
    require(all(contract.get(k) == v for k, v in required_lists.items()),
            "result-contract-fields-changed")
    require(isinstance(contract.get("statuses"), dict) and
            set(contract["statuses"]) == set(STATUSES) - {"ok"},
            "result-contract-statuses-changed")
    require(contract.get("successResult") == {
        "status": "ok", "interval": {"l": "decimal integer string",
                                     "u": "decimal integer string"}},
        "result-contract-success-shape-changed")
    return contract


def make_expected_cases(spec):
    scale, maximum, bits, intervals, pairs = regenerate_inputs(spec)
    cases = []

    def append(case_id, operation, operands, serialized_input):
        cases.append({"id": case_id, "op": operation, "input": serialized_input,
                      "expected": expected_result(operation, operands, scale, maximum)})

    def serialized_interval(interval):
        return {"l": str(interval[0]), "u": str(interval[1])}

    for index, pattern in enumerate(bits):
        append("bits-" + str(index), "fromBits", pattern, [pattern])
    for index, interval in enumerate(intervals):
        for operation in ("square", "sqrt"):
            append(operation + "-" + str(index), operation, (interval,),
                   [serialized_interval(interval)])
    for index, (left, right) in enumerate(pairs):
        operands = (intervals[left], intervals[right])
        for operation in ("add", "sub", "mul", "div"):
            append(operation + "-" + str(index), operation, operands,
                   [serialized_interval(v) for v in operands])
    require(len(cases) == EXPECTED_RECORDS, "regenerated-record-count")
    require(len({case["id"] for case in cases}) == len(cases),
            "regenerated-id-collision")
    return scale, maximum, cases


class Findings:
    def __init__(self):
        self.total = 0
        self.errors = []

    def add(self, code, index=None):
        self.total += 1
        if len(self.errors) < MAX_ERRORS:
            self.errors.append(code if index is None else code + ":row=" + str(index))

    def check(self, condition, code, index=None):
        if not condition:
            self.add(code, index)


def validate_core(document, spec, contract, cases, scale, maximum, source_hashes):
    """Same document/numerical validator for baseline and every fault probe.

    Journal comparison intentionally lives elsewhere, so a faulty mathematical
    result cannot be 'detected' merely because a second copy was not mutated.
    """
    findings = Findings()
    observed = Counter({status: 0 for status in STATUSES})
    expected_counts = Counter({status: 0 for status in STATUSES})
    expected_counts.update(case["expected"]["status"] for case in cases)
    records = []
    if not isinstance(document, dict):
        findings.add("result-document-not-object")
    else:
        findings.check(set(document) == set(contract["documentFields"]),
                       "result-document-fields")
        findings.check(document.get("schema") == contract["documentSchema"],
                       "result-schema")
        findings.check(document.get("specId") == spec["id"], "result-spec-id")
        runtime = document.get("runtime")
        findings.check(isinstance(runtime, dict) and
                       set(runtime) == set(contract["runtimeFields"]) and
                       all(isinstance(v, str) and 1 <= len(v) <= 256
                           for v in runtime.values()), "runtime-fields")
        findings.check(document.get("sourceSha256") == source_hashes,
                       "result-source-hashes")
        raw_records = document.get("records")
        if not isinstance(raw_records, list):
            findings.add("records-not-array")
        elif len(raw_records) > 2000:
            findings.add("records-over-validation-budget")
        else:
            records = raw_records
    findings.check(len(records) == len(cases), "record-count")
    seen_ids = set()
    for index, row in enumerate(records):
        if not isinstance(row, dict):
            findings.add("record-not-object", index)
            continue
        findings.check(set(row) == set(contract["recordFields"]), "record-fields", index)
        case_id = row.get("id")
        if not isinstance(case_id, str) or len(case_id) > 64:
            findings.add("record-id-shape", index)
        elif case_id in seen_ids:
            findings.add("duplicate-record-id", index)
        else:
            seen_ids.add(case_id)
        findings.check(row.get("inputUnchanged") is True, "input-mutated-or-unconfirmed", index)
        result = row.get("result")
        status = result.get("status") if isinstance(result, dict) else None
        observed[status if isinstance(status, str) and status in STATUSES
                 else "_invalidStatus"] += 1
        if index >= len(cases):
            findings.add("unexpected-extra-record", index)
            continue
        case = cases[index]
        expected = case["expected"]
        findings.check(case_id == case["id"], "record-id-or-order", index)
        findings.check(row.get("op") == case["op"], "record-operation", index)
        findings.check(row.get("input") == case["input"], "record-input", index)
        findings.check(status == expected["status"], "result-status", index)
        if not isinstance(result, dict):
            findings.add("result-not-object", index)
            continue
        if expected["status"] != "ok":
            findings.check(set(result) == {"status"}, "failure-result-fields", index)
            continue
        findings.check(set(result) == {"status", "interval"}, "success-result-fields", index)
        interval = result.get("interval")
        if not isinstance(interval, dict) or set(interval) != {"l", "u"}:
            findings.add("result-interval-fields", index)
            continue
        try:
            lo = canonical_integer(interval["l"])
            hi = canonical_integer(interval["u"])
        except CheckError as error:
            findings.add(str(error), index)
            continue
        findings.check(-maximum <= lo <= hi <= maximum, "result-interval-order-or-range", index)
        findings.check(lo == expected["lo"] and hi == expected["hi"],
                       "not-exact-outward-endpoints", index)
        low_real, high_real = Fraction(lo, scale), Fraction(hi, scale)
        if expected["squareImage"] is not None:
            source_low, source_high = expected["squareImage"]
            findings.check(lo >= 0 and hi >= 0 and low_real ** 2 <= source_low
                           and high_real ** 2 >= source_high,
                           "sqrt-inclusion-failed", index)
        else:
            image_low, image_high = expected["image"]
            findings.check(low_real <= image_low and image_high <= high_real,
                           "rational-inclusion-failed", index)
    return {"passed": findings.total == 0, "totalRecords": len(records),
            "expectedStatusCounts": dict(expected_counts),
            "observedStatusCounts": dict(observed),
            "errorCount": findings.total, "errors": findings.errors}


def validate_journal(journal_path, document, spec):
    require(journal_path.is_file(), "journal-missing")
    require(journal_path.stat().st_size <= MAX_INPUT_BYTES, "journal-file-budget")
    with journal_path.open("rb") as handle:
        raw = handle.read(MAX_INPUT_BYTES + 1)
    require(len(raw) <= MAX_INPUT_BYTES, "journal-file-budget")
    lines = raw.splitlines()
    require(len(lines) == EXPECTED_RECORDS + 2, "journal-line-count")
    decoded = []
    for line in lines:
        try:
            decoded.append(json.loads(line, object_pairs_hook=pairs_without_duplicates,
                                      parse_constant=reject_json_constant))
        except (UnicodeError, ValueError, RecursionError):
            raise CheckError("journal-invalid-json") from None
    require(same_json(decoded[0], {"kind": "header", "schema": "m31-fixed96-journal-v1",
                                  "specId": spec["id"]}), "journal-header")
    require(same_json(decoded[-1], {"kind": "complete", "records": EXPECTED_RECORDS}),
            "journal-completion")
    require(isinstance(document, dict) and isinstance(document.get("records"), list)
            and len(document["records"]) == EXPECTED_RECORDS,
            "journal-final-record-count")
    for index, (entry, row) in enumerate(zip(decoded[1:-1], document["records"])):
        require(same_json(entry, {"kind": "record", "row": row}),
                "journal-final-row-mismatch:row=" + str(index))
    return {"passed": True, "rows": EXPECTED_RECORDS,
            "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}


def fault_controls(document, core_validator):
    """Five categories, six concrete probes; originals remain untouched."""
    controls = []

    def probe(mutated):
        checked = core_validator(mutated)
        return {"rejected": not checked["passed"],
                "errorCount": checked["errorCount"], "errors": checked["errors"]}

    def add(name, description, mutations):
        probes = []
        for label, mutation in mutations:
            clone = copy.deepcopy(document)
            mutation(clone)
            result = probe(clone)
            result["name"] = label
            probes.append(result)
        controls.append({"name": name, "description": description,
                         "executed": True,
                         "passed": all(result["rejected"] for result in probes),
                         "probes": probes})

    subnormal_index = next((index for index, row in enumerate(document["records"])
                            if row["op"] == "fromBits" and
                            row["input"] == ["0000000000000001"]), None)
    require(subnormal_index is not None, "fault-control-case-missing")
    require(document["records"][subnormal_index]["result"] == {
        "status": "ok", "interval": {"l": "0", "u": "1"}},
        "fault-control-case-not-qualified")

    def narrow_subnormal(clone):
        clone["records"][subnormal_index]["result"]["interval"]["l"] = "1"

    def wrong_status(clone):
        clone["records"][0]["result"] = {"status": "unresolved-domain"}

    def missing_record(clone):
        clone["records"].pop()

    def duplicate_record(clone):
        clone["records"][1] = copy.deepcopy(clone["records"][0])

    def reorder_records(clone):
        clone["records"][0], clone["records"][1] = clone["records"][1], clone["records"][0]

    def altered_input(clone):
        clone["records"][0]["input"] = ["0000000000000001"]

    add("wrong-endpoint", "Narrow the positive minimum-subnormal conversion from [0,1] to [1,1]; ordered but excludes its exact value.",
        [("narrow-lower-endpoint", narrow_subnormal)])
    add("wrong-status", "Claim unresolved-domain for the exact zero conversion.",
        [("zero-conversion-domain", wrong_status)])
    add("missing-case", "Remove the final required record.", [("remove-final", missing_record)])
    add("duplicate-or-reordered-case", "Separately duplicate one case and exchange the first two cases.",
        [("duplicate", duplicate_record), ("reorder", reorder_records)])
    add("altered-input", "Change the first zero input to the minimum positive subnormal while retaining the zero output.",
        [("change-input-bits", altered_input)])
    return controls


class PublicArgumentParser(argparse.ArgumentParser):
    def error(self, _message):
        raise CheckError("invalid-command-line")


def main(argv=None):
    parser = PublicArgumentParser(description="Independent fixed96 saved-result checker")
    for name in ("spec", "input", "manifest", "output", "root"):
        parser.add_argument("--" + name, required=True)
    try:
        args = parser.parse_args(argv)
    except CheckError:
        print('{"passed":false,"error":"invalid-command-line"}', file=sys.stderr)
        return 2
    report = {
        "schema": "m31-fixed96-independent-check-v1", "passed": False,
        "checkerRuntime": {
            "pythonVersion": ".".join(str(v) for v in sys.version_info[:3]),
            "implementation": sys.implementation.name,
        },
        "scope": "saved-result primitive qualification; no swarm, native-equivalence or performance conclusion",
        "totalRecords": 0, "expectedRecords": EXPECTED_RECORDS,
        "faultControls": [], "expectedStatusCounts": {},
        "observedStatusCounts": {}, "errors": [],
    }
    output_allowed = False
    try:
        root = Path(args.root).resolve(strict=True)
        require(root.is_dir(), "root-not-directory")
        spec_path = Path(args.spec)
        input_path = Path(args.input)
        manifest_path = Path(args.manifest)
        contract_path = spec_path.parent / "result-contract.json"
        output_path = Path(args.output)
        try:
            output_parent = output_path.parent.resolve(strict=True)
            output_parent.relative_to(root)
        except (OSError, ValueError):
            raise CheckError("output-parent-outside-root-or-missing") from None
        output_allowed = True
        for path in (spec_path, input_path, manifest_path, contract_path):
            relative_name(path, root)
        verified = verify_manifest(manifest_path, root, spec_path, contract_path)
        indexed = {item["path"]: item for item in verified}
        contract = read_contract(contract_path)
        spec = load_json(spec_path, MAX_SPEC_BYTES)
        scale, maximum, cases = make_expected_cases(spec)
        source_hashes = {}
        for name in contract["sourceSha256Keys"]:
            relative = relative_name(spec_path.parent / name, root)
            require(relative in indexed, "runner-source-not-manifest-pinned")
            source_hashes[name] = indexed[relative]["sha256"]
        document = load_json(input_path, MAX_INPUT_BYTES)

        def validator(candidate):
            return validate_core(candidate, spec, contract, cases, scale, maximum, source_hashes)

        baseline = validator(document)
        report.update({key: baseline[key] for key in (
            "totalRecords", "expectedStatusCounts", "observedStatusCounts", "errors")})
        report["baselineErrorCount"] = baseline["errorCount"]
        report["baselinePassed"] = baseline["passed"]
        report["sourceManifest"] = {
            "path": relative_name(manifest_path, root),
            "sha256": file_sha256(manifest_path, MAX_MANIFEST_BYTES)[1]}
        report["verifiedSources"] = verified
        report["input"] = {"path": relative_name(input_path, root),
                           "sha256": file_sha256(input_path, MAX_INPUT_BYTES)[1]}
        journal_path = Path(str(input_path) + ".jsonl")
        try:
            relative_name(journal_path, root)
            report["journal"] = validate_journal(journal_path, document, spec)
            report["journal"]["path"] = relative_name(journal_path, root)
        except CheckError as error:
            report["journal"] = {"passed": False, "errors": [str(error)]}
            report["errors"].append(str(error))
        if baseline["passed"]:
            report["faultControls"] = fault_controls(document, validator)
        else:
            report["errors"].append("fault-controls-not-run-on-invalid-baseline")
        controls = report["faultControls"]
        controls_passed = len(controls) == 5 and all(control["executed"] and
                                                    control["passed"] for control in controls)
        if not controls_passed:
            report["errors"].append("fault-controls-incomplete-or-ineffective")
        report["passed"] = baseline["passed"] and report["journal"]["passed"] and controls_passed
    except CheckError as error:
        report["errors"].append(str(error))
    except Exception as error:
        # Do not serialize exception messages: OS errors may contain host paths.
        report["errors"].append("checker-exception:" + type(error).__name__)
    report["errors"] = report["errors"][:MAX_ERRORS]
    payload = (json.dumps(report, indent=2, sort_keys=True) + "\n").encode("utf-8")
    try:
        require(output_allowed, "output-path-not-qualified")
        require(len(payload) <= MAX_INPUT_BYTES, "report-output-budget")
        with Path(args.output).open("xb") as handle:
            handle.write(payload)
    except Exception:
        print('{"passed":false,"error":"exclusive-report-write-failed"}', file=sys.stderr)
        return 2
    print(json.dumps({"passed": report["passed"], "totalRecords": report["totalRecords"],
                      "faultControlCategories": len(report["faultControls"])}))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
