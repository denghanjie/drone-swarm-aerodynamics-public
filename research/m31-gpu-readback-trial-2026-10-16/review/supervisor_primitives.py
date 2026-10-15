"""Pure bounded policy and receipt binding; no subprocess or operational import."""
import hashlib
from review_primitives import json_bytes, require, strict_equal

PIPE_CAP = 16384
INNER_SECONDS = 30
SOFT_SECONDS = 31
REAP_SECONDS = 33
HARD_SECONDS = 35
LOCK = b'One external saved GPU-readback review reserved. Permanent; no retry.\n'
CHECKER_LOCK = b'One saved GPU-readback review reserved. Permanent; no retry.\n'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def bounded_piece(data, retained_total, cap=PIPE_CAP):
    require(type(data) is bytes and type(retained_total) is int and 0 <= retained_total <= cap, 'Invalid capture input')
    keep = data[:max(0, cap-retained_total)]
    return keep, len(data)-len(keep)


def bind_checker(stdout, saved_summary, report_bytes, checker_lock):
    require(type(stdout) is bytes and 0 < len(stdout) <= 4096 and stdout.endswith(b'\n')
            and len(stdout.splitlines()) == 1, 'Complete single checker summary required')
    require(stdout == saved_summary and checker_lock == CHECKER_LOCK, 'Exact child summary and review lock required')
    summary = json_bytes(stdout, 4096)
    report = json_bytes(report_bytes, 65536)
    expected_summary_keys = {'kind','reportBytes','reportSHA256','recordIntegrityCandidate','recordIntegrityVerified','qualified',
        'requiresExternalReviewExit0AndCompleteFinalSummary','hostOutcome','actualBytesMatch','pageCandidateBySelfReport',
        'gpuExecutionIndependentlyAttested','groupsPassed','groupsTotal','errors','accountedDiagnosticAndLaterPublicReviewBytes'}
    require(type(summary) is dict and set(summary) == expected_summary_keys and type(report) is dict, 'Exact safe checker summary fields')
    require(summary.get('kind') == 'saved-gpu-readback-review-summary'
            and report.get('kind') == 'saved-gpu-readback-public-evidence-review', 'Checker output identity')
    require(type(summary.get('reportBytes')) is int and summary['reportBytes'] == len(report_bytes)
            and summary.get('reportSHA256') == digest(report_bytes), 'Actual report byte binding')
    for item in [summary, report]:
        require(item.get('recordIntegrityVerified') is False and item.get('qualified') is False
                and item.get('requiresExternalReviewExit0AndCompleteFinalSummary') is True
                and item.get('gpuExecutionIndependentlyAttested') is False, 'Checker claim boundary')
    require(report.get('terminal') is True and report.get('active') is False and report.get('retryPermitted') is False
            and report.get('processClosureIndependentlyReobserved') is False, 'Checker terminal boundary')
    require(type(report.get('recordIntegrityCandidate')) is bool
            and summary.get('recordIntegrityCandidate') is report['recordIntegrityCandidate'], 'Candidate projection')
    groups = report.get('groups'); errors = report.get('errors')
    require(type(groups) is list and len(groups) <= 5 and all(type(row) is dict and type(row.get('pass')) is bool for row in groups)
            and type(errors) is list and len(errors) <= 6, 'Bounded checker groups/errors')
    require(type(summary.get('groupsPassed')) is int and summary['groupsPassed'] == sum(row['pass'] for row in groups)
            and type(summary.get('groupsTotal')) is int and summary['groupsTotal'] == len(groups)
            and type(summary.get('errors')) is int and summary['errors'] == len(errors), 'Checker group projection')
    expected_groups = ['frozen_source_and_allocation','final_public_manifest','actual_bytes_and_reported_page_phases',
                       'external_lifecycle_projections','resource_and_output_accounting']
    require([row.get('group') for row in groups] == expected_groups[:len(groups)]
            and all(set(row) == {'group','pass'} for row in groups), 'Unique ordered checker groups')
    require(report['recordIntegrityCandidate'] is (len(groups) == 5 and all(row['pass'] for row in groups) and not errors),
            'Candidate equals complete checker group conjunction')
    finding = report.get('finding')
    require(finding is None or type(finding) is dict, 'Bounded finding projection')
    outcome = finding.get('hostOutcome') if finding else None
    facts = finding.get('actualByteFacts') if finding else None
    require(facts is None or type(facts) is dict and type(facts.get('all_bytes_match')) is bool, 'Boolean byte finding')
    matched = facts['all_bytes_match'] if facts else None
    page_candidate = finding.get('pageCandidateBySelfReport') if finding else None
    require(outcome in [None,'evaluate-rejected','envelope-rejected','page-failed-without-bytes','page-failed-with-bytes',
                        'valid-byte-mismatch','candidate-byte-transfer-recorded']
            and (page_candidate is None or type(page_candidate) is bool), 'Safe finding categories')
    require(strict_equal(summary.get('hostOutcome'), outcome) and strict_equal(summary.get('actualBytesMatch'), matched)
            and strict_equal(summary.get('pageCandidateBySelfReport'), page_candidate), 'Exact visible finding projections')
    require(report.get('wallCapSeconds') == 30 and report.get('workStopSeconds') == 25 and report.get('finalStopSeconds') == 29,
            'Unchanged inner checker limits')
    own = len(CHECKER_LOCK)+len(report_bytes)+len(stdout)
    require(type(report.get('reviewArtifactBytes')) is int and report['reviewArtifactBytes'] == own, 'Checker own artifact equation')
    base = report.get('accountedDiagnosticAndLaterPublicReviewBytes')
    require(strict_equal(base, summary.get('accountedDiagnosticAndLaterPublicReviewBytes')),
            'Checker base accounting projection')
    if report['recordIntegrityCandidate']:
        require(type(base) is int, 'Candidate requires established complete accounting base')
    if base is not None:
        require(type(base) is int and own+len(stdout) <= base <= 8388608
                and any(row.get('group') == 'resource_and_output_accounting' and row['pass'] for row in groups), 'Established checker accounting base')
    return {'recordIntegrityCandidate':report['recordIntegrityCandidate'], 'reportBytes':len(report_bytes),
            'reportSHA256':digest(report_bytes), 'summaryBytes':len(stdout), 'summarySHA256':digest(stdout),
            'accountedBaseBytes':base}


def total_bytes(base, private_stderr, supervisor_lock, public_checker_summary, receipt, supervisor_summary):
    """Base already includes exactly one child stdout copy: retained private stdout."""
    values = [private_stderr, supervisor_lock, public_checker_summary, receipt, supervisor_summary]
    require(all(type(n) is int and n >= 0 for n in values), 'Integer additional byte counts')
    require(base is None or type(base) is int and 0 <= base <= 8388608, 'Bounded established base')
    return None if base is None else base+sum(values)
