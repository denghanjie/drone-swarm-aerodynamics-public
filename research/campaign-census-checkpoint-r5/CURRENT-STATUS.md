# R5: all 21 prescribed decisions matched

The coordinator accepted **the fixed census/checkpoint protocol only**: 21/21 expected outcomes, comprising 10 accepts and 11 intended control errors. There were no unexpected outcomes, no unrun cases, and no retry. Expected control errors include the legacy enumerate-then-stat race reproduction; they are successful test outcomes, not unexplained failures.

The result supports conservative accounting for the two exact registered checkpoint slots under the tested trusted-writer conditions. It does not establish a general atomic filesystem snapshot, arbitrary-writer safety, R4 integration/completion, numerical accuracy, speedup, or physical validity.

The original child and parent records still say their acceptance was pending. They were preserved. The later [sanitized acceptance/evidence](postrun-report/EVIDENCE.json) reports the separate coordinator decision and its original-record hash.

- [Milestone and limitations](postrun-report/MILESTONE.md)
- [Actual-record-linked Three.js display](postrun-demo/index.html)
- [Original child result](results/attempt-001/result.json) and [original parent observation](results/attempt-001/PARENT-OBSERVATION.json)
- [Selected census implementation](implementation/census.py) and [authored literal oracle](implementation/oracle.json)

The display reuses earlier, unqualified trajectories. No R5 flight was generated. Historical P1 stops at 0.9915625 s; the saved display reaches 0.990 s and then holds. Animation is not a physics or correctness test. The selected public evidence omits driver/configuration/fixtures and is incomplete for full reproduction. Inventory approval remains separate.
