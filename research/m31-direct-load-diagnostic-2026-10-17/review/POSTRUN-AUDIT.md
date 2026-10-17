# Direct-load diagnostic: postrun saved-evidence audit

The saved records support the checker's decision,
`fixed-route-stress-accuracy-definite-failure`. Record validity passed; the fixed
omission proposal did not achieve the registered accuracy goal. No scientific
module was imported, no native solver/reference was rerun, and no existing file
was changed in this audit.

## Binding and completeness

All 159 manifest pins match current bytes and exact source commit
`ee342fe5cdd824cbd68e4c1c85bae9f83bf688bf`. The manifest SHA-256 is
`93d26849dcd0a86d18b254f8eb5babc3d13e0f46d08efc92dfc2bc5cef79635b`.
The committed manifest blob, saved prelaunch publication receipt and runtime
binary also match. The receipt records a successful exact-commit HTTPS check
before launch; this audit verified its bindings without another network fetch.

Both attempts identify this source/manifest, report 159 verified pins,
completed status, exit 0 and null first failure, and bind the exact output size
and digest. Analyze is 5,452,100 bytes with SHA-256
`8b2cee37458583fbf4b78f343134f2805221f211209ba13d53208a42eaa8624b`;
check is 45,680 bytes with SHA-256
`18caa7a9d1153adead64e3f5741dc15225d5e1fa1dd1f5b17e0c6f817046fe35`.
All 15 checker input pins match: config, constants index, analyze output and
six input/reference pairs; the 14 preexisting inputs are manifest-pinned.

The saved run reports 15 producer fixtures, 29 independent checker fixtures and
13 intended corruption rejections, all successful. All six states, 12 proposals,
3,072 candidate rotors, 96,768 reference pairs, 12 A audits, 12 B audits, six C
audits, 4,608 certificate rows and 1,536 omission-diagnostic rows are retained.
Saved producer/checker summaries agree. Exact rational comparisons of their
error intervals reproduce every category and overall tier status. This audit
did not repeat candidate generation or the full independent interval audit.

## Fixed-proposal result

Every full control passes A at the strict 1e-8 tier; its B certificate also
passes. Every omitted proposal definitely fails A at 1e-8 and 1e-4. At the
1e-2 stress tier, run-a-t0 and run-b-t0 definitely fail all four A categories;
the other four states pass A. Only run-a-t10 and run-b-t10 pass B/C at stress.
In run-a-t5 and run-b-t5, the stress certificate obstacle is rotor error; the
other three certificate categories pass. A certificate `not-certified` status
does not assert actual inaccuracy.

| State | Deleted / positive | Omitted A: 1e-8 / 1e-4 / 1e-2 | Omitted B=C at 1e-2 |
|---|---:|---|---|
| run-a-t0 | 39 / 389 | definite-fail / definite-fail / definite-fail | not-certified |
| run-a-t5 | 26 / 252 | definite-fail / definite-fail / pass | not-certified |
| run-a-t10 | 20 / 192 | definite-fail / definite-fail / pass | pass |
| run-b-t0 | 40 / 394 | definite-fail / definite-fail / definite-fail | not-certified |
| run-b-t5 | 26 / 256 | definite-fail / definite-fail / pass | not-certified |
| run-b-t10 | 17 / 163 | definite-fail / definite-fail / pass | pass |

The mask sizes equal ceil(P/10). These are conditional normalized model-load
comparisons, not physical experiments. The two stress failures stop this fixed
selection/solver route under the prospective rule. They do not disprove every
approximation and do not authorize same-allocation mask/fraction/schedule tuning.
No looser pass overrides the failed strict all-six goal.

## Prospective B/C equality analysis

The table uses only already-emitted rows and the predeclared sufficient
condition tL*U>=1, with tL=C.p.lower and U=C.p.upper. Every state preserves the
256-row denominator. Exact local-factor maxima were reconciled with saved K.

| State | Equal k / 256 | Equal roots / 256 | Equal K | tL U >= 1: yes / no | Strictly wider C contractions |
|---|---:|---:|---|---:|---:|
| run-a-t0 | 256 | 256 | true | 217 / 39 | 34 |
| run-a-t5 | 256 | 256 | true | 221 / 35 | 24 |
| run-a-t10 | 256 | 256 | true | 232 / 24 | 18 |
| run-b-t0 | 256 | 256 | true | 213 / 43 | 33 |
| run-b-t5 | 256 | 256 | true | 218 / 38 | 22 |
| run-b-t10 | 256 | 256 | true | 224 / 32 | 15 |

B/C global factors agree in 6/6 states, maximum-error intervals in 6/6, and tier decisions in 6/6.
Equal factors/roots do not imply equal contraction intervals, nor that the
sufficient condition is necessary. Rows outside that condition can still have
equal B/C factors, including rows whose defects are unchanged. This outcome
shows insensitivity of this k/K certificate to discarded omitted lower bounds
for these candidates; it does not show that upper-only omission introduces no
uncertainty. The accompanying JSON retains exact summaries, condition counts,
strict/tied reciprocal-branch counts and observed evidence pins.

## Operational and claim limits

The analyze/check recorded wall stages are 0.8622413333505392 and
1.2566333757713437 seconds; observed peak RSS is 88,178,688 and 104,071,168
bytes. These meet the registered stage/output and post-output RSS acceptance
conditions. RSS is observed, not an enforced memory ceiling; final attempt
serialization overhead is excluded. These are diagnostic execution figures,
not simulator speedups or strict whole-process timings.

The states are reused dependent snapshots; oracle coefficient/reference work
was already paid for. No claim of fresh holdout confirmation, general physical
impossibility, physical 1% accuracy, online Q-current certification, useful
5,000-drone runtime or novelty follows. All frozen and result bytes were
rehashed unchanged before creating these two new review files.
