"""Six prespecified inert boundary cases against the separately authored pure helper."""

import ast
from dataclasses import fields
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True


def digest(data):
    return hashlib.sha256(data).hexdigest()


def rejected(action, error_type):
    try:
        action()
    except error_type as error:
        return {"rejected": True, "errorType": type(error).__name__}
    return {"rejected": False, "errorType": None}


def main():
    if len(sys.argv) != 2:
        raise ValueError("Supply the standalone pure-helper directory")
    output = Path(__file__).resolve().parent
    author = Path(sys.argv[1]).resolve()
    plan_bytes = (output / "HELPER-REVIEW-PLAN.json").read_bytes()
    plan = json.loads(plan_bytes)
    helper_bytes = (author / "reconcile.py").read_bytes()
    contract_bytes = (author / "CONTRACT.md").read_bytes()
    assert digest(helper_bytes) == plan["helperSHA256"]
    assert digest(contract_bytes) == plan["contractSHA256"]
    tree = ast.parse(helper_bytes, filename="reconcile.py")
    imports = sorted((node.module, tuple(alias.name for alias in node.names))
                     for node in tree.body if isinstance(node, ast.ImportFrom))
    assert imports == [("__future__", ("annotations",)), ("dataclasses", ("dataclass",))]
    assert not any(isinstance(node, ast.Import) for node in ast.walk(tree))
    assert not any(isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) for node in ast.walk(tree))
    spec = importlib.util.spec_from_file_location("independently_reviewed_pure_reconcile", author / "reconcile.py")
    helper = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = helper
    spec.loader.exec_module(helper)  # Only this source-pinned pure helper; never the observer.
    Row, Snapshot, Coverage = helper.Row, helper.Snapshot, helper.ValidatedCoverage
    reconcile = helper.reconcile
    coverage = lambda snapshot, *groups: Coverage(snapshot, frozenset(groups))
    snapshot = Snapshot("synthetic-frame-1", (Row(100, 1, 100), Row(200, 100, 200)))
    outcomes = []

    altered = Snapshot("synthetic-frame-1", (Row(100, 1, 100), Row(200, 1, 200)))
    result = rejected(lambda: reconcile(coverage(snapshot, 100), coverage(altered, 100, 200), ()), ValueError)
    outcomes.append({"id": "same_label_different_snapshot", **result, "expectedMet": result["rejected"]})

    result = rejected(lambda: Snapshot("duplicate", (Row(100, 1, 100), Row(100, 200, 200))), ValueError)
    outcomes.append({"id": "duplicate_pid_conflicting_rows", **result, "expectedMet": result["rejected"]})

    result = rejected(lambda: Snapshot("forged-row", ({"pid": 100, "ppid": 1, "pgid": 100},)), TypeError)
    outcomes.append({"id": "fabricated_row_representation", **result, "expectedMet": result["rejected"]})

    fabricated = reconcile(coverage(snapshot, 100), coverage(snapshot, 100, 200), ())
    pids = [item.row.pid for item in fabricated.covered_after_refresh]
    fields_exposed = [field.name for field in fields(fabricated)]
    outcomes.append({
        "id": "fabricated_well_typed_coverage_boundary",
        "coveredAfterCallerAssertion": pids,
        "closureGateWithAssertedKnownClosure": fabricated.closure_permitted(True),
        "ownershipIndependentlyAuthenticated": False,
        "expectedMet": pids == [200] and fabricated.ledger == () and fabricated.closure_permitted(True),
        "interpretation": "Acceptance is conditional on a truthful caller assertion. This demonstrates the documented authentication boundary, not a valid operational admission or signaling authorization.",
    })

    first = reconcile(coverage(snapshot, 100), None, ())
    later = Snapshot("synthetic-frame-2", snapshot.rows)
    retained = reconcile(coverage(later, 100, 200), coverage(later, 100, 200), first.ledger)
    reset = reconcile(coverage(later, 100, 200), coverage(later, 100, 200), ())
    outcomes.append({
        "id": "permanent_taint_and_ledger_threading_boundary",
        "correctlyThreadedLedgerPreserved": retained.ledger == first.ledger,
        "correctThreadClosureGate": retained.closure_permitted(True),
        "deliberateContractViolationEmptyLedgerGate": reset.closure_permitted(True),
        "expectedMet": retained.ledger == first.ledger and not retained.closure_permitted(True)
                       and reset.ledger == () and reset.closure_permitted(True),
        "interpretation": "The helper never clears supplied taint. A stateless function cannot detect callers discarding prior history; the required entire-ledger threading and durable persistence obligations remain external.",
    })

    ancestry = reconcile(coverage(snapshot, 100), coverage(snapshot, 100), ())
    unadmitted = [item.row.pid for item in ancestry.still_unadmitted]
    no_signal_api = fields_exposed == ["covered_after_refresh", "still_unadmitted", "ledger", "refresh_available"]
    outcomes.append({
        "id": "ancestry_only_does_not_admit",
        "stillUnadmittedPIDs": unadmitted,
        "closureGate": ancestry.closure_permitted(True),
        "resultFields": fields_exposed,
        "noSignalAPIInReviewedSource": no_signal_api,
        "expectedMet": unadmitted == [200] and not ancestry.closure_permitted(True) and no_signal_api,
    })

    assert len(outcomes) == plan["plannedCaseExecutions"] == 6
    assert [case["id"] for case in outcomes] == [case["id"] for case in plan["cases"]]
    author_receipt = json.loads((author / "static-check-receipt.json").read_bytes())
    prior_count = author_receipt["total_test_case_executions_across_development_runs"]
    assert prior_count == 44
    report = {
        "kind": "independent-pure-reconciliation-helper-review",
        "helperSHA256": digest(helper_bytes), "contractSHA256": digest(contract_bytes),
        "prespecifiedPlanSHA256": digest(plan_bytes),
        "caseExecutions": 6,
        "casesMeetingExpected": sum(case["expectedMet"] for case in outcomes),
        "outcomes": outcomes,
        "sourceImports": [module + "." + ",".join(names) for module, names in imports],
        "authorReportedCaseExecutions": prior_count,
        "independentFrozenSourceCaseExecutions": 4,
        "checkpointCaseExecutionsReportedTotal": prior_count + 4 + 6,
        "caseLimit": 100,
        "materialDefectWithinDocumentedPureContractFound": False,
        "notImplementedOrTestedHere": plan["notImplementedOrTestedHere"],
        "dataclassValidationScope": "Row/container types, integer shapes and duplicate PID rejection only. These checks do not validate registry parsing, registry append-only history or full process ownership evidence.",
        "callerObligations": [
            "Authenticate exact owned-group coverage for the same retained snapshot; well-typed data is not proof.",
            "Carry and durably retain the entire ledger; never reset or truncate it after initialization.",
            "Keep failed refresh, incomplete registry and any other known-group closure conditions independently fail-closed.",
            "Provide no signaling authority through these observations; any future operations need separate fresh ownership evidence and authorization.",
        ],
        "legacyModuleImports": 0, "realProcessOperations": 0, "browserInvocations": 0, "gpuInvocations": 0,
        "historicalDiagnosisEstablished": False,
        "scope": "Pure helper source review and six deterministic synthetic boundary cases only; no operational integration, source modification or historical diagnosis.",
    }
    (output / "HELPER-REVIEW.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(json.dumps({key: report[key] for key in ["kind", "caseExecutions", "casesMeetingExpected", "checkpointCaseExecutionsReportedTotal", "materialDefectWithinDocumentedPureContractFound"]}, sort_keys=True))
    return 0 if all(case["expectedMet"] for case in outcomes) else 1


if __name__ == "__main__":
    raise SystemExit(main())
