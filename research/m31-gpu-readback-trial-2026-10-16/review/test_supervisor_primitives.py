"""Pure handcrafted binding/byte-cap tests; no supervisor/checker import or process."""
import ast
import copy
import datetime
import json
from pathlib import Path
import unittest
import sys
sys.dont_write_bytecode = True
from review_primitives import admit_review
from supervisor_primitives import bounded_piece, bind_checker, digest, total_bytes, CHECKER_LOCK

GROUPS = ['frozen_source_and_allocation','final_public_manifest','actual_bytes_and_reported_page_phases',
          'external_lifecycle_projections','resource_and_output_accounting']


def encode(value):
    return (json.dumps(value, sort_keys=True)+'\n').encode()


def handcrafted(candidate=True):
    report = {'kind':'saved-gpu-readback-public-evidence-review','terminal':True,'active':False,
        'recordIntegrityCandidate':candidate,'recordIntegrityVerified':False,'qualified':False,
        'requiresExternalReviewExit0AndCompleteFinalSummary':True,'gpuExecutionIndependentlyAttested':False,
        'processClosureIndependentlyReobserved':False,'retryPermitted':False,
        'groups':[{'group':name,'pass':candidate or i>0} for i,name in enumerate(GROUPS)],
        'errors':[] if candidate else [{'group':GROUPS[0],'type':'ValueError','reason':'handcrafted unit-test rejection'}],
        'finding':{'hostOutcome':'candidate-byte-transfer-recorded','actualByteFacts':{'all_bytes_match':True},'pageCandidateBySelfReport':True},
        'wallCapSeconds':30,'workStopSeconds':25,'finalStopSeconds':29,'reviewArtifactBytes':0,
        'accountedDiagnosticAndLaterPublicReviewBytes':100000 if candidate else None}
    return report


def bound_bytes(report):
    for _ in range(20):
        data = encode(report)
        finding = report.get('finding')
        summary = {'kind':'saved-gpu-readback-review-summary','reportBytes':len(data),'reportSHA256':digest(data),
            'recordIntegrityCandidate':report['recordIntegrityCandidate'],'recordIntegrityVerified':False,'qualified':False,
            'requiresExternalReviewExit0AndCompleteFinalSummary':True,'hostOutcome':finding['hostOutcome'] if finding else None,
            'actualBytesMatch':finding['actualByteFacts']['all_bytes_match'] if finding and finding['actualByteFacts'] else None,
            'pageCandidateBySelfReport':finding['pageCandidateBySelfReport'] if finding else None,
            'gpuExecutionIndependentlyAttested':False,'groupsPassed':sum(row['pass'] for row in report['groups']),
            'groupsTotal':len(report['groups']),'errors':len(report['errors']),
            'accountedDiagnosticAndLaterPublicReviewBytes':report['accountedDiagnosticAndLaterPublicReviewBytes']}
        stdout = encode(summary)
        own = len(CHECKER_LOCK)+len(data)+len(stdout)
        if report['reviewArtifactBytes'] == own:
            return stdout, data
        report['reviewArtifactBytes'] = own
    raise AssertionError('handcrafted own-size convergence')


class PureSupervisorTests(unittest.TestCase):
    def test_disabled_config_gate(self):
        config = json.loads((Path(__file__).parents[1]/'config.json').read_text())
        with self.assertRaises(ValueError):
            admit_review(config, datetime.datetime.now(datetime.timezone.utc))

    def test_complete_binding(self):
        stdout, report = bound_bytes(handcrafted())
        r = bind_checker(stdout, stdout, report, CHECKER_LOCK)
        self.assertTrue(r['recordIntegrityCandidate'])
        self.assertEqual(r['reportSHA256'], digest(report))

    def test_failed_report_is_bound_without_promotion(self):
        stdout, report = bound_bytes(handcrafted(False))
        self.assertFalse(bind_checker(stdout, stdout, report, CHECKER_LOCK)['recordIntegrityCandidate'])

    def test_candidate_without_accounting_base_rejected(self):
        candidate = handcrafted(); candidate['accountedDiagnosticAndLaterPublicReviewBytes'] = None
        stdout, data = bound_bytes(candidate)
        with self.assertRaises(ValueError):
            bind_checker(stdout, stdout, data, CHECKER_LOCK)

    def test_partial_stdout_rejected(self):
        stdout, report = bound_bytes(handcrafted())
        with self.assertRaises(ValueError):
            bind_checker(stdout[:-1], stdout, report, CHECKER_LOCK)

    def test_extra_stdout_line_rejected(self):
        stdout, report = bound_bytes(handcrafted())
        with self.assertRaises(ValueError):
            bind_checker(stdout+b'\n', stdout, report, CHECKER_LOCK)

    def test_report_mutation_rejected(self):
        stdout, report = bound_bytes(handcrafted())
        with self.assertRaises(ValueError):
            bind_checker(stdout, stdout, report+b' ', CHECKER_LOCK)

    def test_saved_summary_mismatch_rejected(self):
        stdout, report = bound_bytes(handcrafted())
        with self.assertRaises(ValueError):
            bind_checker(stdout, stdout+b' ', report, CHECKER_LOCK)

    def test_claimed_candidate_with_no_groups_rejected(self):
        report = handcrafted(); report['groups'] = []
        stdout, data = bound_bytes(report)
        with self.assertRaises(ValueError):
            bind_checker(stdout, stdout, data, CHECKER_LOCK)

    def test_duplicate_group_rejected(self):
        report = handcrafted(); report['groups'][1]['group'] = report['groups'][0]['group']
        stdout, data = bound_bytes(report)
        with self.assertRaises(ValueError):
            bind_checker(stdout, stdout, data, CHECKER_LOCK)

    def test_false_candidate_with_all_groups_pass_rejected(self):
        report = handcrafted(); report['recordIntegrityCandidate'] = False
        stdout, data = bound_bytes(report)
        with self.assertRaises(ValueError):
            bind_checker(stdout, stdout, data, CHECKER_LOCK)

    def test_visible_outcome_projection_rejected(self):
        stdout, data = bound_bytes(handcrafted())
        for field,value in [('hostOutcome','valid-byte-mismatch'),('actualBytesMatch',False),('pageCandidateBySelfReport',False)]:
            summary = json.loads(stdout); summary[field] = value; altered = encode(summary)
            with self.assertRaises(ValueError):
                bind_checker(altered, altered, data, CHECKER_LOCK)

    def test_boolean_numeric_projection_rejected(self):
        stdout, data = bound_bytes(handcrafted()); summary = json.loads(stdout); summary['actualBytesMatch'] = 1
        altered = encode(summary)
        with self.assertRaises(ValueError):
            bind_checker(altered, altered, data, CHECKER_LOCK)

    def test_extra_public_summary_field_rejected(self):
        stdout, data = bound_bytes(handcrafted()); summary = json.loads(stdout); summary['privatePath'] = 'do-not-copy'
        altered = encode(summary)
        with self.assertRaises(ValueError):
            bind_checker(altered, altered, data, CHECKER_LOCK)

    def test_none_finding_projection(self):
        report = handcrafted(False); report['finding'] = None
        stdout, data = bound_bytes(report)
        self.assertFalse(bind_checker(stdout, stdout, data, CHECKER_LOCK)['recordIntegrityCandidate'])

    def test_bounded_piece_retains_actual_prefix(self):
        self.assertEqual(bounded_piece(b'abcde', 16382), (b'ab',3))
        self.assertEqual(bounded_piece(b'ab',16384), (b'',2))

    def test_pipe_budget_is_combined(self):
        first, _ = bounded_piece(b'a'*10000,0)
        second, dropped = bounded_piece(b'b'*10000,len(first))
        self.assertEqual(len(first)+len(second),16384); self.assertEqual(dropped,3616)

    def test_accounting_does_not_double_count_child_stdout(self):
        self.assertEqual(total_bytes(1000,2,3,4,5,6),1020)
        self.assertIsNone(total_bytes(None,2,3,4,5,6))
        with self.assertRaises(ValueError):
            total_bytes(1000,True,3,4,5,6)

    def test_supervisor_ast_only(self):
        tree = ast.parse(Path(__file__).with_name('supervise_saved_review.py').read_text())
        calls = [n for n in ast.walk(tree) if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute)
                 and isinstance(n.func.value,ast.Name) and n.func.value.id == 'subprocess' and n.func.attr == 'Popen']
        self.assertEqual(len(calls),1)
        imports = [n for n in ast.walk(tree) if isinstance(n,ast.ImportFrom)]
        self.assertFalse(any(n.module == 'check_saved_files' for n in imports))


if __name__ == '__main__':
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(PureSupervisorTests))
    print(json.dumps({'kind':'pure-supervisor-helper-tests','testsRun':result.testsRun,'failures':len(result.failures),
        'errors':len(result.errors),'checkerInvocations':0,'supervisorInvocations':0,'browserInvocations':0,'gpuInvocations':0}))
    raise SystemExit(0 if result.wasSuccessful() else 1)
