"""Execute only two frozen AST fragments against deterministic in-memory mocks.

The original observer module is never imported or executed. No process API,
browser, GPU, network, clock or private historical evidence is used.
"""

import ast
import copy
import hashlib
import json
from pathlib import Path
import sys
from types import SimpleNamespace

sys.dont_write_bytecode = True

SOURCE_RELATIVE = "research/m31-gpu-readback-trial-2026-10-16/source/observe-transport.py"
SOURCE_SHA256 = "aacb3daa611f7f3893b27ebf0b6bed0ff2a434d7042d1d10f429e833cf31069e"
PREREG_SHA256 = "83f8c43a152c60a65c2a10cb9f22b91363cad2472025685b3a5303bd05278cf7"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def encoded(value):
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()


def read_small(path, cap=65536):
    if not path.is_file() or path.is_symlink() or path.stat().st_size > cap:
        raise ValueError("Expected bounded regular source/metadata file")
    data = path.read_bytes()
    if len(data) > cap:
        raise ValueError("Source/metadata size changed")
    return data


def extract(repo, output):
    prereg_bytes = read_small(output / "PREREGISTERED-CASES.json")
    if digest(prereg_bytes) != PREREG_SHA256:
        raise ValueError("Prespecified synthetic semantics changed")
    prereg = json.loads(prereg_bytes)
    source_bytes = read_small(repo / SOURCE_RELATIVE)
    if digest(source_bytes) != SOURCE_SHA256:
        raise ValueError("Frozen observer source changed")
    freeze_bytes = read_small(repo / "research/m31-gpu-readback-trial-2026-10-16/freeze.json")
    if digest(freeze_bytes) != prereg["originalSource"]["freezeSHA256"]:
        raise ValueError("Frozen inventory changed")
    source_pin = next(pin for pin in json.loads(freeze_bytes)["files"] if pin["path"] == SOURCE_RELATIVE)
    if source_pin["bytes"] != len(source_bytes) or source_pin["sha256"] != SOURCE_SHA256:
        raise ValueError("Source not bound by original freeze")
    source = source_bytes.decode("utf-8")
    tree = ast.parse(source, filename=SOURCE_RELATIVE)
    samples = [node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "sample"]
    closures = [node for node in tree.body if isinstance(node, ast.Assign)
                and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name)
                and node.targets[0].id == "closure_complete"]
    if len(samples) != 1 or len(closures) != 1:
        raise ValueError("Expected exactly one source fragment of each kind")
    sample = samples[0]
    closure = closures[0].value
    sample_source = (ast.get_source_segment(source, sample) + "\n").encode()
    closure_source = (ast.get_source_segment(source, closure) + "\n").encode()
    (output / "sample.extracted.py").write_bytes(sample_source)
    (output / "closure.extracted.txt").write_bytes(closure_source)
    provenance = {
        "kind": "frozen-observer-ast-extraction-provenance",
        "sourcePath": SOURCE_RELATIVE,
        "sourceBytes": len(source_bytes),
        "sourceSHA256": SOURCE_SHA256,
        "freezeSHA256": digest(freeze_bytes),
        "preregistrationSHA256": PREREG_SHA256,
        "originalModuleImported": False,
        "originalModuleBodyExecuted": False,
        "fragments": [
            {"name": "sample", "nodeKind": "FunctionDef", "startLine": sample.lineno,
             "endLine": sample.end_lineno, "sourceSHA256": digest(sample_source),
             "astSHA256": digest(ast.dump(sample, include_attributes=False).encode())},
            {"name": "closure_complete RHS", "nodeKind": type(closure).__name__,
             "startLine": closure.lineno, "endLine": closure.end_lineno,
             "sourceSHA256": digest(closure_source),
             "astSHA256": digest(ast.dump(closure, include_attributes=False).encode())},
        ],
        "mockBoundary": "registry_entries, process_table, inspect_groups, require, os.getpid, CAPTURE_PID, HELPERS, RSS_CAP and report are synthetic. No original helper executes.",
        "caseSemanticsBeforeExecution": prereg["cases"],
    }
    (output / "EXTRACTION-PROVENANCE.json").write_bytes(encoded(provenance))
    return sample, closure


def synthetic_table(detached_pid):
    def row(pid, ppid, pgid):
        return {"pid": pid, "ppid": ppid, "pgid": pgid,
                "rss": 4096, "observerProbe": False}
    return {
        10: row(10, 1, 10),
        20: row(20, 10, 10),
        100: row(100, 20, 100),
        101: row(101, 100, 100),
        detached_pid: row(detached_pid, 101, detached_pid),
    }


def run_sample_case(sample_ast, case_id, initial_registry, late_registration, detached_pid):
    registry_store = set(initial_registry)
    admitted = set()
    order = []
    fixture = synthetic_table(detached_pid)
    report = {"rssSamples": 0, "peakObservedOwnedRSSBytes": 0}

    def registry_entries():
        order.append("registry-read")
        admitted.update(registry_store)

    def process_table():
        if late_registration:
            registry_store.add(200)
            order.append("synthetic-registration-after-read")
        order.append("process-snapshot")
        return copy.deepcopy(fixture)

    def inspect_groups(table):
        order.append("inspect-admitted-groups")
        return {100} | admitted

    def require(condition, reason):
        if not condition:
            raise RuntimeError(reason)

    namespace = {
        "__builtins__": {"all": all, "sum": sum, "max": max, "len": len},
        "registry_entries": registry_entries,
        "process_table": process_table,
        "inspect_groups": inspect_groups,
        "require": require,
        "os": SimpleNamespace(getpid=lambda: 20),
        "CAPTURE_PID": 10,
        "HELPERS": [],
        "RSS_CAP": 2147483648,
        "report": report,
    }
    # Define only the extracted function; no original imports or module body.
    module = ast.Module(body=[copy.deepcopy(sample_ast)], type_ignores=[])
    exec(compile(module, "<frozen-sample-fragment>", "exec"), namespace)
    error_type = error_reason = None
    returned = None
    try:
        returned = namespace["sample"]()
    except RuntimeError as error:
        error_type, error_reason = type(error).__name__, str(error)
    return {
        "id": case_id,
        "syntheticCallOrder": order,
        "registryBeforeRead": sorted(initial_registry),
        "registryAfterSnapshot": sorted(registry_store),
        "admittedGroupsForThisCall": sorted({100} | admitted),
        "errorType": error_type,
        "errorReason": error_reason,
        "returnedOriginalSyntheticTable": returned == fixture,
        "rssSamples": report["rssSamples"],
        "peakObservedOwnedRSSBytes": report["peakObservedOwnedRSSBytes"],
    }


def run_closure_case(closure_ast):
    report = {
        "wrapperReaped": True, "wrapperGroupAbsent": True,
        "wrapperPipeCaptureComplete": True, "registryComplete": True,
        "cleanupErrorObserved": False, "rssProbeErrors": 1,
        "errors": [{"phase": "work", "reason": "Unregistered detached descendant"}],
    }
    browsers = {"synthetic-known-browser": {"absent": True}}
    compiled = compile(ast.Expression(body=copy.deepcopy(closure_ast)), "<frozen-closure-fragment>", "eval")
    worlds = []
    for offender_present in (True, False):
        namespace = {
            "__builtins__": {"all": all}, "report": copy.deepcopy(report),
            "BROWSERS": copy.deepcopy(browsers), "HELPERS": [],
            "UNLINKED_OFFENDER_PRESENT": offender_present,
        }
        result = eval(compiled, namespace)
        worlds.append({"unlinkedOffenderPresentInSyntheticWorld": offender_present,
                       "frozenClosurePredicate": result})
    names = sorted({node.id for node in ast.walk(closure_ast) if isinstance(node, ast.Name)})
    return {
        "id": "missing_offender_linkage_at_closure",
        "worlds": worlds,
        "expressionNames": names,
        "unlinkedOffenderStatusIsReadByExpression": "UNLINKED_OFFENDER_PRESENT" in names,
        "priorWorkErrorPresentInBothWorlds": True,
        "knownCleanupInputsIdentical": True,
        "limitation": "World status is an intentionally unconsulted synthetic variable, not a claim about a historical process. The expression cannot distinguish these two worlds.",
    }


def main():
    if len(sys.argv) != 2:
        raise ValueError("Supply the repository directory for bounded frozen-source reads")
    output = Path(__file__).resolve().parent
    repo = Path(sys.argv[1]).resolve()
    sample, closure = extract(repo, output)
    late = run_sample_case(sample, "late_browser_registration", [], True, 200)
    ready = run_sample_case(sample, "same_browser_already_registered", [200], False, 200)
    unregistered = run_sample_case(sample, "truly_unregistered_descendant", [], False, 300)
    gap = run_closure_case(closure)
    error = "Unregistered detached descendant"
    late["matchesPreregisteredExpected"] = (
        late["errorType"] == "RuntimeError" and late["errorReason"] == error
        and late["registryAfterSnapshot"] == [200] and late["admittedGroupsForThisCall"] == [100]
        and late["rssSamples"] == 1 and late["peakObservedOwnedRSSBytes"] == 20480)
    ready["matchesPreregisteredExpected"] = (
        ready["errorType"] is None and ready["returnedOriginalSyntheticTable"]
        and ready["admittedGroupsForThisCall"] == [100, 200]
        and ready["rssSamples"] == 1 and ready["peakObservedOwnedRSSBytes"] == 20480)
    unregistered["matchesPreregisteredExpected"] = (
        unregistered["errorType"] == "RuntimeError" and unregistered["errorReason"] == error
        and unregistered["registryAfterSnapshot"] == []
        and unregistered["admittedGroupsForThisCall"] == [100]
        and unregistered["rssSamples"] == 1 and unregistered["peakObservedOwnedRSSBytes"] == 20480)
    gap["matchesPreregisteredExpected"] = (
        all(world["frozenClosurePredicate"] is True for world in gap["worlds"])
        and gap["unlinkedOffenderStatusIsReadByExpression"] is False)
    outcomes = [late, ready, unregistered, gap]
    result = {
        "kind": "frozen-observer-deterministic-synthetic-outcomes",
        "preregistrationSHA256": PREREG_SHA256,
        "sourceSHA256": SOURCE_SHA256,
        "casesRun": len(outcomes),
        "casesMatchingPreregisteredExpected": sum(row["matchesPreregisteredExpected"] for row in outcomes),
        "outcomes": outcomes,
        "originalModuleImports": 0,
        "originalModuleInvocations": 0,
        "realProcessProbes": 0,
        "browserInvocations": 0,
        "gpuInvocations": 0,
        "historicalDiagnosisEstablished": False,
        "scope": "Possible behavior of exact frozen AST fragments under fixed documented mocks; not a historical reproduction or operational cleanup verification.",
    }
    (output / "SYNTHETIC-OUTCOMES.json").write_bytes(encoded(result))
    print(json.dumps({key: result[key] for key in ["kind", "casesRun", "casesMatchingPreregisteredExpected", "sourceSHA256", "preregistrationSHA256", "historicalDiagnosisEstablished"]}, sort_keys=True))
    return 0 if all(row["matchesPreregisteredExpected"] for row in outcomes) else 1


if __name__ == "__main__":
    raise SystemExit(main())
