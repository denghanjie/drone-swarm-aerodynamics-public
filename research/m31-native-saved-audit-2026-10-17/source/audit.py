"""Source-only draft: future isolated child for unchanged saved native-load audit."""
from pathlib import Path
import datetime
import hashlib
import importlib.util
import json
import os
import sys

NAME = 'research/m31-native-saved-audit-2026-10-17'
OLD = 'research/m31-native-load-baseline-2026-10-17'
FILE_LIMIT = 32 * 1024 * 1024


def need(value, code):
    if not value:
        raise ValueError(code)


def identity(path):
    digest, size = hashlib.sha256(), 0
    with path.open('rb') as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b''):
            digest.update(block)
            size += len(block)
    return {'bytes': size, 'sha256': digest.hexdigest()}


def verify(root, pin):
    path = (root / pin['path']).resolve()
    need(not Path(pin['path']).is_absolute() and path.is_relative_to(root), 'pin-path')
    need(identity(path) == {k: pin[k] for k in ('bytes', 'sha256')}, 'pin:' + pin['path'])
    return path


def read_json(path):
    need(path.stat().st_size <= FILE_LIMIT, 'json-size')
    return json.loads(path.read_bytes())


def write_exclusive(path, value):
    data = (json.dumps(value, allow_nan=False, separators=(',', ':')) + '\n').encode()
    need(len(data) <= FILE_LIMIT, 'audit-output-size')
    with path.open('xb') as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())


def main(root, expected_manifest, commit):
    package = root / NAME
    need(Path(__file__).resolve() == package / 'source/audit.py', 'audit-script-location')
    need(os.environ.get('RESEARCH_EXECUTION_CONTEXT') == 'tool-require-escalated', 'dispatch-attestation')
    manifest_path = package / 'source-manifest.json'
    need(identity(manifest_path)['sha256'] == expected_manifest, 'audit-manifest-sha')
    manifest = read_json(manifest_path)
    pins = {pin['path']: pin for pin in manifest['files']}
    need(len(pins) == len(manifest['files']), 'duplicate-source-pin')
    for pin in pins.values():
        verify(root, pin)
    need(NAME + '/config.json' in pins and NAME + '/source/audit.py' in pins, 'child-source-closure')
    config = read_json(package / 'config.json')
    need(config['schema'] == 'm31-native-saved-audit-config-v1', 'config-schema')
    runtime = config['runtime']['python']
    need(identity(Path(sys.executable).resolve()) == {k: runtime[k] for k in ('bytes', 'sha256')}
         and manifest['runtime']['python'] == runtime, 'python-runtime')
    for key in ('originalManifest', 'originalPublication', 'originalChecker',
                'originalBrowserOutput', 'originalFailedAttempt', 'originalJournal'):
        pin = config[key]
        need(pins.get(pin['path']) == pin, 'frozen-original-pin:' + key)
        verify(root, pin)
    original_manifest = read_json(root / config['originalManifest']['path'])
    for pin in original_manifest['files']:
        need(pins.get(pin['path']) == pin, 'original-full-closure-binding')
        verify(root, pin)
    checker_pin = config['originalChecker']
    need(any(pin == checker_pin for pin in original_manifest['files']), 'original-checker-manifest-binding')
    for relative in config['originalMustRemainAbsent']:
        need(not (root / relative).exists(), 'original-checker-artifact-already-present')
    old_attempt = read_json(root / config['originalFailedAttempt']['path'])
    need(old_attempt['status'] == 'failed' and old_attempt['exitCode'] == 1
         and old_attempt['childExitCode'] == 0 and old_attempt['cleanupError'] is True
         and old_attempt['firstFailure']['type'] == 'PermissionError'
         and old_attempt['sourceCommit'] == config['originalSourceCommit']
         and old_attempt['sourceManifestSha256'] == config['originalManifest']['sha256'],
         'original-failed-stage-binding')
    need(datetime.datetime.now(datetime.timezone.utc) < datetime.datetime.fromisoformat(config['launchCutoffUtc']),
         'checker-import-cutoff')
    checker_path = verify(root, checker_pin)
    need(checker_path == root / OLD / 'source/check.py', 'original-checker-absolute-path')
    spec = importlib.util.spec_from_file_location('_m31_original_frozen_native_checker', checker_path)
    need(spec is not None and spec.loader is not None, 'original-checker-loader')
    module = importlib.util.module_from_spec(spec)
    # Executes the unchanged frozen file with its own original __file__. Its
    # __main__ block does not run. No constants, globals or paths are patched.
    spec.loader.exec_module(module)
    report = module.main(root, config['originalManifest']['sha256'], config['originalSourceCommit'])
    need(isinstance(report, dict) and report.get('schema') == 'm31-native-load-check-v1'
         and report.get('qualificationScope') == 'retained-six-state native-load accuracy in the recorded named Chrome only',
         'unchanged-checker-report-contract')
    need('savedEvidenceAudit' not in report, 'metadata-field-collision')
    fixture_ok = ([row['id'] for row in report['arithmeticFixtures']] == config['expectedArithmeticFixtureIds']
                  and all(row['passed'] is True for row in report['arithmeticFixtures']))
    corruption_ok = ([row['id'] for row in report['corruptionChecks']] == config['expectedCorruptionIds']
                     and all(row['passed'] is True for row in report['corruptionChecks']))
    audit_metadata = {
        'schema': 'm31-native-saved-evidence-audit-provenance-v1',
        'auditSourceCommit': commit, 'auditSourceManifestSha256': expected_manifest,
        'originalSourceCommit': config['originalSourceCommit'],
        'originalSourceManifest': config['originalManifest'],
        'originalChecker': checker_pin, 'originalBrowserOutput': config['originalBrowserOutput'],
        'originalFailedAttempt': config['originalFailedAttempt'], 'originalJournal': config['originalJournal'],
        'originalSupervisorStatus': 'failed', 'originalSupervisorFailure': old_attempt['firstFailure'],
        'originalSupervisorRepaired': False, 'originalCheckerMainUsedUnchanged': True,
        'auditScope': config['qualificationScope'], 'fixtureAssertionsPassed': fixture_ok,
        'corruptionAssertionsPassed': corruption_ok,
        'launchCleanupComplianceClaim': False, 'newBrowserCalls': 0,
        'performanceClaim': False, 'onlineCertificationClaim': False}
    # Keep every original report field, schema and qualificationScope unchanged;
    # the only addition is a separate wrapper-provenance metadata field.
    result = dict(report)
    result['savedEvidenceAudit'] = audit_metadata
    write_exclusive(package / 'results/check.json', result)
    need(report['passed'] is True and fixture_ok and corruption_ok, 'checker-fixture-corruption-integrity')
    need(report['decision'] in ('qualified', 'unqualified'), 'checker-decision')
    return {'passed': report['passed'], 'decision': report['decision'],
            'originalSupervisorStatus': 'failed', 'auditScope': config['qualificationScope']}


if __name__ == '__main__':
    try:
        need(len(sys.argv) == 4, 'usage: audit.py ROOT AUDIT_MANIFEST_SHA AUDIT_SOURCE_COMMIT')
        result = main(Path(sys.argv[1]).resolve(), sys.argv[2], sys.argv[3])
        print(json.dumps(result, allow_nan=False))
    except Exception as error:
        print(json.dumps({'auditChildPassed': False, 'errorClass': type(error).__name__,
                          'reason': str(error)[:512]}))
        raise SystemExit(1)
