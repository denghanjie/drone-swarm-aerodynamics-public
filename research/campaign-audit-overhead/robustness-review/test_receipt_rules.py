"""Deterministic synthetic receipt-validator fixtures. NOT measured benchmark data.
Prepared but not run before root's explicit source/input/config execution release.
"""
import copy
import unittest
from validate_cost_receipts import validate_receipt


def fixture():
    job={'id':'fixture-job','workload':'W-ENDPOINT','seed':840131,'block':0,'variant':'B'}
    digest='a'*64
    def p(name):
        return {'complete':True,'observations':257,'pairSamples':246720,
                'pairMarginValues':1973760,'semanticDigest':digest,'consumed':True,
                'logicalId':name,'wallSeconds':0.25,'cpuSeconds':0.125}
    r={'schema':'audit-c1-job/v1','status':'passed','jobId':job['id'],'freezeSha256':'f'*64,
       'counts':{'warmupPasses':1,'measuredPasses':2,'warmupObservations':257,
                 'measuredObservations':514,'totalObservations':771},
       'resourceUsage':{'maxRssBytes':67108864},
       'benchmark':{**{k:job[k] for k in ('workload','seed','block','variant')},
          'consumedOutsideTimedRegion':True,'finishInsideTimedRegion':True,
          'warmupIsolated':True,'extraInstrumentedPasses':0,
          'expectedSemanticDigest':digest,'warmup':[p('warmup')],
          'timedPasses':[p('timed-0'),p('timed-1')],
          'aggregate':{'wallSeconds':0.5,'cpuSeconds':0.25}}}
    return job,r


class ReceiptRules(unittest.TestCase):
    def test_valid_synthetic_fixture(self):
        job,r=fixture();validate_receipt(r,job,'f'*64)

    def reject(self, change):
        job,r=fixture();change(r)
        with self.assertRaises(ValueError):
            validate_receipt(r,job,'f'*64)

    def test_drop_measured_pass(self):
        self.reject(lambda r:r['benchmark']['timedPasses'].pop())
    def test_add_unplanned_pass(self):
        self.reject(lambda r:r['benchmark']['timedPasses'].append(copy.deepcopy(r['benchmark']['timedPasses'][0])))
    def test_include_warmup_in_aggregate(self):
        self.reject(lambda r:r['benchmark']['aggregate'].update(wallSeconds=0.75))
    def test_reuse_warmup_identity(self):
        self.reject(lambda r:r['benchmark']['timedPasses'][0].update(logicalId='warmup'))
    def test_config_count_with_incomplete_actual_work(self):
        self.reject(lambda r:r['benchmark']['timedPasses'][1].update(observations=256))
    def test_missing_pair(self):
        self.reject(lambda r:r['benchmark']['timedPasses'][1].update(pairSamples=246719))
    def test_missing_margin(self):
        self.reject(lambda r:r['benchmark']['timedPasses'][1].update(pairMarginValues=1973759))
    def test_wrong_semantic_digest(self):
        self.reject(lambda r:r['benchmark']['timedPasses'][1].update(semanticDigest='b'*64))
    def test_unconsumed_result(self):
        self.reject(lambda r:r['benchmark']['timedPasses'][1].update(consumed=False))
    def test_failed_child(self):
        self.reject(lambda r:r.update(status='resource_limited'))
    def test_finish_excluded(self):
        self.reject(lambda r:r['benchmark'].update(finishInsideTimedRegion=False))
    def test_extra_instrumented_pass(self):
        self.reject(lambda r:r['benchmark'].update(extraInstrumentedPasses=1))
    def test_negative_cpu(self):
        self.reject(lambda r:r['benchmark']['timedPasses'][0].update(cpuSeconds=-1))
    def test_missing_maxrss(self):
        self.reject(lambda r:r.update(resourceUsage={}))
    def test_wrong_frozen_source(self):
        self.reject(lambda r:r.update(freezeSha256='e'*64))

if __name__=='__main__':
    unittest.main()
