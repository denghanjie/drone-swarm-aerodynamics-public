# AUDIT-C1 terminal schedule diagnosis

Status: terminal integrity failure; no retry, resume, source correction or new campaign authorized or performed.

## Finding

The frozen supervisor has one wrong schedule literal. At `robustness-review/supervise.py:32`, `ORDERS[840137][6]` is `CB`. The prescribed order is `BC`.

- `PLAN.md:110` gives seed 840131 as BC, CB, CB, BC, BC, CB, CB, BC and requires the opposite order for seed 840137.
- `PROTOCOL.json:94–103` therefore specifies CB, BC, BC, CB, CB, BC, BC, CB for 840137.
- All 64 performance rows in `implementation/config/jobs.json` exactly match that protocol.
- `robustness-review/validate_cost_receipts.py:12,25–26,80–83` independently specifies and requires the same correct order.
- The supervisor instead uses CB, BC, BC, CB, CB, BC, **CB**, CB for 840137. Its seed has three BC and five CB block orders, rather than four of each, and block 6 is no longer opposite seed 840131.

One reversed pair is repeated in both workloads, causing exactly four slot mismatches. These are zero-based performance slots:

| Slot | Workload | Seed / block | Configured and prescribed | Supervisor expects |
|---|---|---|---|---|
| 28 | W-ENDPOINT | 840137 / 6 | B | C1 |
| 29 | W-ENDPOINT | 840137 / 6 | C1 | B |
| 60 | W-STAGE-FIXTURE | 840137 / 6 | B | C1 |
| 61 | W-STAGE-FIXTURE | 840137 / 6 | C1 | B |

The corresponding job definitions begin at `jobs.json:359,367,615,623`. Their full job-list indices are 46, 47, 78 and 79, respectively, because 18 correctness jobs precede performance.

The small-first scheduling amendment did not cause this mismatch. Its before/after performance rows are byte-equivalent as parsed JSON; only correctness ordering changed.

## What actually ran

`WINDOW-STARTED.json` records 2026-10-14T04:53:51Z and retryAllowed=false. `SUPERVISOR.json` records integrity_blocked with the exact error “Performance jobs must match all 64 prescribed serial slots, zero-based blocks.”

The supervisor created its one-shot marker before calling verify_release (`supervise.py:454–473`). The jobs check raised at lines 142–143, during line 264, before the child loop, full frozen-file check, runtime check, correctness gate or cost validator. No child was started or reaped. All 82 configured jobs, plus the separate gate, were unrun.

The empty `unrunJobIds` field is an initialization artifact, not a complete pending-work inventory: self.rows starts as [] at line 176 and the assignment `self.rows = verify_jobs(self.jobs)` never completes. The referenced durable checkpoint was never written.

The supervisor records 0.040667349 s wall and 0.039228 s process-tree CPU before its final receipt; FINAL-ACCOUNTING records 0.048071681 s wall and 0.046627 s CPU before its own write. These are explicitly before-write accounting values. There is no equivalence, speedup or resource-completion evidence. The prior reference remains unqualified.

## Why static acceptance missed it

The retained acceptance claims did not establish consistency across every schedule consumer:

1. Earlier resource checks claim benchmarkOrderMatchesProtocol and all64OrderedSlotsMatch. Those are consistent with the actual jobs and protocol but insufficient to establish what the supervisor expects.
2. Final semantic review004 and final resource checks explicitly establish that all 64 performance jobs were unchanged across the correctness-only reorder (`STATIC-REVIEW-004.json:458–465`, `STATIC-CHECKS-FINAL.json:125–163`).
3. Final resource decision nevertheless asserts allOrderedSlotsVerified=true (`DECISION.json:220`). That broad assurance conflicts with the frozen supervisor literal.
4. The supervisor and validator received AST syntax checks without import (`STATIC-CHECKS-FINAL.json:79–95`). Syntax validity and hash agreement preserve an erroneous literal; they cannot establish agreement between consumers.
5. Prepared `test_receipt_rules.py` imports only validate_receipt. It has no cross-schedule or supervisor verify_jobs regression test, and its fixtures were not executed.

The directly evidenced failure is a missing cross-consumer acceptance check. Exact historical commands that produced the boolean schedule claims are not retained here, so this report does not invent which human or script made the oversight.

The supervisor, jobs and cost validator match their frozen byte identities. This is a frozen inconsistency, not evidence of post-freeze source drift. The companion JSON records all inspected evidence identities and verifies 16 relevant entries against FREEZE.json.

## Proposed future amendment, not adopted

Preserve this attempt's marker, freeze, release, sources and receipts unchanged. A proposed correction applies only to a separately authorized prospective revision:

1. Correct the supervisor's seed-840137 block-6 order from CB to BC. Do not alter the prescribed protocol/jobs/cost-validator order to accommodate the typo.
2. Require explicit comparison of all 64 ordered slots across protocol, jobs, actual production supervisor expected_performance_slots and cost-validator expected_slots. Record comparison scope, pins, schedule hashes and an empty mismatch list.
3. Add an isolated metadata-only regression harness that evaluates the actual production helpers without supervisor startup, model imports, children or an attempt marker. Verify acceptance of the prescribed jobs and rejection of a synthetically reversed pair, missing/extra/duplicate slots, wrong seed/block/variant, and invalid phase order. Also assert zero-based blocks 0–7, integer seeds, complementary seed orders, and four BC/four CB blocks per seed. These tests are proposed and were not run.
4. Retain an independent protocol oracle so a shared wrong constant cannot make every component agree incorrectly. A source-only AST/literal cross-check can be part of pre-release review without numerical execution.
5. Perform metadata preflight before consuming any future one-shot marker and recheck within runtime. Improve future preflight-failure receipts to distinguish loaded from validated jobs and report the actual unrun configuration. Never reset this failed attempt's marker.
6. Any future numerical execution requires separately approved protocol, independent review, a new source/config freeze and explicit release. This diagnosis creates none.

## Evidence preservation

Only new files in `postrun-diagnosis/` were written. Existing evidence was read as text/JSON or parsed as Python AST; no study module, supervisor, gate, fixture, child or benchmark was imported or executed. All 21 evidence files retained the same byte count and SHA-256 across diagnosis generation.

See `SCHEDULE-DIAGNOSIS.json` for exact order arrays, mismatch tuples, full terminal receipts, source hashes and frozen-identity comparisons.

