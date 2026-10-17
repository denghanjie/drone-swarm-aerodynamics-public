# Postrun saved-evidence audit

The saved renewal evidence is internally consistent and bound to source commit
`ea2c963ea9a3e9af1eecaaeefe3739bf0082d0d5`. This was a bounded read-only
postrun audit: no scientific module import, reference recomputation, analyzer
or checker rerun, replacement input, or modification of frozen/result files.

All 61 manifest pins match both current bytes and the exact source commit.
The manifest itself matches its committed Git blob and saved publication
digest; the pinned Python binary also matches. The publication record documents
an exact-commit HTTPS verification before launch; this audit did not repeat
that network fetch. Both attempt records name the same source commit/manifest,
report 61 verified pins, completion, exit 0 and no first failure, and match the
exact bytes and SHA-256 of their respective saved outputs.

The checker is passed with no failure. Its 19 input pins exactly bind the
analyzer output plus all six input/reference/baseline-r0 triples; all 18 prior
files also occur in the frozen manifest. The records contain nine passing
analyzer fixtures, 19 passing independent-checker fixtures and 14 corruption
rejections in their intended registered families. These are saved execution
records, not newly executed controls.

All six ordered states remain present, with 1,536 rows, 4,608 tier records,
9,216 tree selections and 96,768 planned nonself rotor/source pairs. Row/tier/
tree counts and each state/tier aggregate were reconciled from saved analyzer
rows with both saved summaries. Pair count is the complete fixed-domain count
and agrees with the checker's reported validated count; this postrun audit did
not repeat its full pair-interval validation. Every positive denominator is
nonzero. All 18 ceiling hurdles and all 36 tree hurdles are false.

| State | Positive denominator | Ceiling = feasible, 1e-8 | 1e-4 | 1e-2 | Widest-tier percent | T8 / T2 at 1e-2 |
|---|---:|---:|---:|---:|---:|---:|
| run-a-t0 | 389 | 0 | 0 | 5 | 1.285% | 0 / 0 |
| run-a-t5 | 252 | 0 | 2 | 8 | 3.175% | 0 / 0 |
| run-a-t10 | 192 | 0 | 2 | 6 | 3.125% | 0 / 0 |
| run-b-t0 | 394 | 0 | 1 | 9 | 2.284% | 0 / 0 |
| run-b-t5 | 256 | 0 | 1 | 7 | 2.734% | 0 / 0 |
| run-b-t10 | 163 | 0 | 3 | 12 | 7.362% | 0 / 2 |

Ceiling and upper-endpoint feasible-singleton counts coincide in every state
and tier. T8 covers zero positive terms at every tier. T2 also covers zero
except run-b-t10 at 1e-2: one group in one row, four source members including
two positive terms, with 16,126 visits versus the usual 16,128. All T8 totals
are 3,840 visits per state/tier. Exact ratios, full summaries and the lone
selected-group record are retained in the accompanying audit JSON.

The strongest permitted interpretation is that every one of these six exposed
states has an optimistic positive-term omission ceiling below 10%, even at the
widest fixed coefficient-mass proxy tier. Thus the registered all-six 10%
continuation target is excluded under this specific per-row budget policy.
This establishes neither physical impossibility nor a general limit on
approximation, alternative budgets/trees, different states, load accuracy or
runtime savings. The two dependent trajectories are not fresh confirmatory
flight data, and the oracle has already paid scalar-reference costs.

Recorded analyzer/checker wall stages are 1.1145491246134043 and
1.3391624996438622 seconds; observed peak RSS values are 91,340,800 and
86,081,536 bytes. These satisfy the renewal's post-output 512 MiB acceptance
gate, which is not an enforced memory ceiling and excludes final attempt-report
overhead. These stage observations are not simulator performance comparisons
or strict whole-process timing claims. The original failed RLIMIT_DATA
allocation and first failure remain preserved among the verified manifest pins.
