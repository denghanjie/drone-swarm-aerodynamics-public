M31 omission-ablation saved-evidence review — final memo

The sole saved-only review passed 1,594,583 checks with zero failures, no observed scientific gate violations and no partial tails. The saved report records scientificStatus="completed", scientificQualificationCompleted=true and performanceQualified=true. The experiment completed its numerical/control qualification; its prespecified incremental performance criterion H1 was unmet on both fresh inputs, while the descriptive zero-screen-package criterion H2 was met on both. A negative H1 result is a completed result, not a failed scientific invocation.

This memo is based on the saved review JSON, its archived launch/runtime files, and the preparation memo. The draft README and claim ledger were also read for interpretation. No reviewer or scientific code was rerun, imported or modified. No raw scientific calculation, geometry, root solution, input generation, integration or benchmark was performed. Scalar maxima below are reductions of the review's already-reconstructed case summaries.

The frozen scientific source is b6aafb006bbc406deb95f7defcebde6801eaa7f5. Freeze SHA-256 is ccd1695ca48fefd85225c830fd1a93fbbd6bfbde4e1fcaffd1e0532a9c799ec0, with all 34 direct file pins matched. The saved reviewer source SHA-256 is 83bc57c83c6befa63d92278e09d181ee5655dc7f5ac48118df1f9e45fc41ca29. Canonical /tmp/m31-ablation-saved-review.json contains 131,197 bytes, SHA-256 a09c5d46c54e7610b635d506ec8c3ccfc42c98610ff3269aff16dcb78980746d, and is byte-identical to its archived review.json.

The independent launch archive is /tmp/m31-ablation-verifier-launches/1792084001107270000; the checker archive is /tmp/m31-ablation-verifier-runs/1792084001138159000. The launch preserves original checker/memo, exact arguments, stdout, stderr and runtime. The checker archive preserves its own source, arguments, original scientific start/result/budget, review, logs and runtime. Exit code was 0, stderr empty, and no timeout occurred. Internal review time before output was 1.727721708 seconds; time through review/logs was 1.731856708 seconds; external launch wall time was 1.7938165 seconds. The 55-second internal alarm and 59-second external timeout were within the separate 60-second allowance. There were no corrections or reruns.

The campaign's 26 completed case summaries cover 24 exposed fixtures and two fresh same-family lattices. Twenty-two cases produced accepted complete numerical outputs; four fixtures produced the required five-method domain rejections: farStart--1e-12, nearRadius--1e-12, centerInferenceInvalid and tiltRejected. The nearRadius-0 agreement fixture was accepted. The saved-data review reconciles domain decisions and retained witnesses; it does not reconstruct the geometric domain predicate.

All 202 attempted calls and 72 timing records/validation records were accounted for. The exact independently reconstructed shape vector is 25,994,070 independent-center slots, 519,880,140 combined C/Z bound slots, 4,263,017,400 rotor-visit slots, 985,040 rotor receiver-law/root-call slots and zero integration steps. The receiverCalls field reserves four rotor slots per vehicle per attempted query, including early rejections; it is not a count of bisection iterations or independently observed actual instructions. The saved scientific assertion count is 34,017,127 and was retained as runtime evidence, not independently replayed.

The scientific supervisor records one invocation, exit 0, external wall time 59.989628333 seconds, and no cap-triggered stop. The budget was terminal when reviewed. Raw evidence comprises 254 files and 22,074,354 bytes. The saved review reconciles all listed file sizes/hashes and the complete raw inventory. The terminal raw/result.json is separately inventoried because it cannot appear in its own embedded file list: 176,059 bytes, SHA-256 54ffdc78fbea1bc206adf8c0d0572c225f940172d61ba4ac71900671ba7056fd. Raw and published result objects agree. The scientific run and saved review are distinct budgeted invocations; neither timing is substituted for the measured query series.

The retained coverage is 6,052 input state rows, 30,220 scientific output rows, 6,044 C decision rows, 6,044 Z shadow decision rows and 6,044 independent audit rows. The reviewer checked state layout/finiteness/placeholders/motors, all 17-value output schemas, signed body wrench arithmetic, saved root residual/bracket/normalization and power identities, full B/M/Z versus independent I gates, C source/aggregate load budgets, mask encoding/digest/padding/self/order, exact declared nextUp accumulation, source identities and counters. It checked C/Z observable shadow equality and Z actual-versus-shadow work identities, plus the retained Z/M bitwise diagnostic.

All 31,398 retained positive-envelope-selected receiver–source tuples were inspected as four saved rotor terms and a saved source bound. Of these, 15,404 had at least one positive realized term and 15,994 had four zero terms, across all accepted fixtures and fresh inputs. The selected support-code tally was 27,125. The saved 28,690,232 exact-zero term inspections are runtime assertions with coverage reconciled from the masks; their complete term vectors are not retained. A positive source envelope therefore must not be described as proof that a nonzero wake contribution was removed. Counts refer to directed receiver–source selections, not distinct source vehicles.

On the fresh cases, Z and M are bitwise identical across the saved output matrices: zero differing components out of 17,000 and 85,000 respectively. B, M and Z satisfy the fixed full-reference gates against independent I. C satisfies all reconstructable per-source, aggregate and load-target gates. Across the 22 accepted numerical cases, the maximum C discrepancies are:

| Quantity | Largest saved discrepancy | Fixed target | Case |
| --- | ---: | ---: | --- |
| Body thrust | 0.000135753501473046 N | 0.0013243500000000002 N | fresh5000 |
| Roll moment | 0.000002809915842182792 N·m | 0.000010488316895441329 N·m | fresh5000 |
| Pitch moment | 0.0000037467002556263265 N·m | 0.000010488316895441329 N·m | fresh5000 |

The largest inflow discrepancy is 0.02652329975489387, the largest single-rotor discrepancy is 0.00009985207554676079 N, and the largest used-capacity fraction is 0.999998394967478. These are finite-case observations. Near exhaustion of the selected omission capacity is compatible with the retained load gates, and does not establish a universal safety margin.

The actual/shadow count distinction is substantive:

| Input | Exact-zero pair culls | C positive-envelope selections | C actual retained pairs | Z actual retained pairs | C rotor visits | Z rotor visits |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| fresh1000 | 683,632 | 4,931 | 18,203 | 23,134 | 72,812 | 92,536 |
| fresh5000 | 6,488,884 | 26,463 | 99,167 | 125,630 | 396,668 | 502,520 |

Both fresh cases have zero near-fallback counts. Z's actual positive omissions are zero. Its extra work for C-selected pairs is 19,724 / 105,852 rotor visits and 4,316 / 22,805 profile evaluations. Z's shadow selected bounds/B/masks and shared counters agree with C, while those selected terms are physically retained by Z. The shadow B is not an actual Z approximation budget.

The primary cost result uses paired blocks, as frozen prospectively:

| Input | Median paired C/Z | C strictly faster | H1 rule | Outcome |
| --- | ---: | ---: | --- | --- |
| fresh1000 | 1.0038152438668204 | 3 / 8 | Median ≤ 0.95 and at least 7 wins | Unmet |
| fresh5000 | 0.9934533749073577 | 5 / 8 | Median ≤ 0.95 and at least 7 wins | Unmet |

Each ratio pairs C and Z within the same technical block; the even median averages sorted positions four and five. The result supports the statement that positive-bound omission did not supply the predefined useful incremental improvement under these complete implementations and two inputs. It does not establish zero benefit, equivalence, universal harm, or statistical significance. In particular, positive sum-time savings can coexist with unmet H1.

The secondary H2 decomposition uses the sums of the same eight measured durations. All values below are seconds except the share:

| Input | Sum M | Sum Z | Sum C | Net M−C | Zero-package M−Z | Positive-omission Z−C | Zero-package share |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| fresh1000 | 0.8631941670000001 | 0.7009633329999999 | 0.683472915 | 0.1797212520000001 | 0.16223083400000016 | 0.017490417999999952 | 0.90268030182652 |
| fresh5000 | 10.645251166000001 | 8.891523542000002 | 8.747766456999999 | 1.8974847090000022 | 1.7537276239999997 | 0.1437570850000025 | 0.9242380798547967 |

Both net savings are positive and both zero-package shares exceed 0.5, so H2 is met on both inputs. The reconstructed additive identity residual is zero in each case. This is a descriptive decomposition for these implementations and inputs. M−Z includes exact-zero screening together with bound construction, shadow selection, masks and reporting costs. C/Z also includes Z's reporting overhead and any resulting receiver-law workload difference. Neither number is pure exactTerm instruction cost or the performance of a lean zero-only implementation.

For context, marginal measured query medians and ranges were:

| Input | Method | Median seconds | Range seconds |
| --- | --- | ---: | --- |
| fresh1000 | B | 0.1471927505 | 0.145614583–0.154433333 |
| fresh1000 | M | 0.10631556249999999 | 0.104252041–0.113914625 |
| fresh1000 | Z | 0.0851892915 | 0.084001291–0.096280458 |
| fresh1000 | C | 0.084883354 | 0.083877750–0.087385041 |
| fresh5000 | B | 1.7309875835 | 1.703813209–1.742296375 |
| fresh5000 | M | 1.322117896 | 1.306173833–1.398923916 |
| fresh5000 | Z | 1.0873589585 | 1.066173542–1.206751208 |
| fresh5000 | C | 1.0800915624999998 | 1.065919958–1.199513458 |

Those marginal medians are not substituted for paired H1 ratios or the additive H2 sum-time decomposition. One warmup per method/case was excluded as prescribed. Eight technical blocks on two fixed lattices are not independent swarm samples or confidence intervals, and the balancing does not remove all shared-machine, JIT, garbage-collection, thermal or order effects.

Checker scalar-reconstruction tolerances were absolute 2e-16 and relative 8e-15, with 4e-15 for reconstructed cubic residuals and absolute 1e-30 / relative 5e-13 for tiny full-comparison maxima. They were not added to scientific acceptance thresholds. nextUp accumulation was reconstructed as its declared binary64 operation. Saved root diagnostics and engineering numerical allowances are not formal interval certificates.

The conclusion is limited by the retained evidence. No pose generation, quaternion norm, rotation, geometry, field or domain predicate was reconstructed. World axes are absent from new output rows, so the saved world-vector discrepancies were checked without deriving their rotations. Frozen C does not expose fallback source IDs or retained-positive bound values; their equality remains static source reasoning, not an observed offline equality gate. Complete all-source independent terms/code vectors and successful timed output/decision matrices are absent. Their saved checksums, counters, selected terms and validation assertions can be reconciled, but every timed component and every runtime zero assertion cannot be independently replayed. These limits do not license a rerun.

The draft README and claims ledger were checked against the report. The inspected README SHA-256 was 34bf1a6e5c66d3700aee6e2c545a84fa7cda6e3ca3059447fd8f1d21da256606 and claims.md SHA-256 was d60e5f407e6f9ea1e3a2b3da6bfda4a74936c7bbae8cb280e04fb6f662390143. Their central H1/H2 interpretation, distinction between paired and marginal medians, numerical error scales and bitwise Z/M statement agree with the saved report. Two wording refinements were sent to the coordinator before publication: headline attribution should name the zero-screening package and these two inputs; selection counts should name receiver–source pairs, rather than distinct sources. The pending saved-review sentence can now cite this completed pass. Per-case positive-realized subcounts are not separately exposed in the review summary; the checker did verify the underlying per-receiver counts, and this memo uses its retained global totals. No additional scientific interpretation blocker was identified in those drafts.

This establishes finite static numerical/control consistency and a measured implementation cost-fidelity result. It supplies no physical-model validation, flight safety, trajectory qualification, universal real-time performance, population generalization or novelty conclusion. Viewer QA, hardware-identification verification and result-checkpoint publication are outside this saved-review memo's verification scope.

The original preparation memo is preserved below verbatim as 6,132 UTF-8 bytes, SHA-256 b4511b50004458a02da88d23290fca94aa42905732a35c0a75ba95be1f9b5d13. Its execution-withheld language records preparation-time status and is not the current result. The original preparation file and launch copy remain unchanged.

Appendix — verbatim preparation memo begins below.

Prepared M31 ablation saved-data review — execution withheld

Prepared reviewer: /tmp/m31-ablation-saved-review.py. The sole scientific source is b6aafb006bbc406deb95f7defcebde6801eaa7f5, with freeze SHA-256 ccd1695ca48fefd85225c830fd1a93fbbd6bfbde4e1fcaffd1e0532a9c799ec0 and 34 direct pins. Both identities must also be supplied explicitly by the coordinator on the command line; the reviewer does not accept raw self-reported identities as its only provenance check.

The checker has not been executed or imported. Preparation used source/file reads, text construction, hashes and Python AST parsing only. No case generation, scientific JavaScript import, geometry, quaternion norm/rotation, field, root solution, integration or timing repeat occurred. No repository file was edited. The original challenge and all static-review notes remain unchanged.

Preparation began before the coordinator's reported scientific completion. Before this memo was finalized, the coordinator reported exit0, 26 completed cases, 202 calls, H1 unmet and H2 met. Those are coordinator reports, not results independently verified by this preparation. No new raw scientific result or timing file was opened to tune the checker. Its performance rules and numerical gates follow the frozen protocol; scalar reconstruction allowances are inherited from the preceding saved-only review.

Coverage includes every frozen hash/size and required transitive dependency pin; provenance/config/schema equality; complete raw inventory and embedded listed hashes; raw/published terminal equality; exact 17-value state/output layouts; finite saved state placeholders/motors without regenerating poses; saved signed body-wrench, root residual/bracket/normalization and power identities; B/M/Z full-reference gates and maxima; C's original capacity/load-budget/source-term gates; mask length/hash/padding/self/order/count decoding; exact declared nextUp accumulation; C/Z shadow mask/selected-bound/B/count equality; Z actual/shadow/selected rotor and profile counter identities; actual versus positive-envelope selected-term counts and support-code identities; Z/M bitwise differences from saved doubles; attempted-call prefixes and all six shape totals; domain rejection witnesses; timing/validation stream prefixes, query/correctness checksums and counters; eight paired blocks, H1 and H2 arithmetic and performance-artifact equality.

The exact completed reservation is 202 calls, 25,994,070 independent-center slots, 519,880,140 C/Z bound slots, 4,263,017,400 rotor-visit slots, 985,040 rotor receiver-law/root slots, and zero integrations. receiverCalls means 4N reserved rotor slots per attempted query, including early rejects. Runtime logical-check counts and unavailable actual instructions are recorded evidence, not replayed counts.

Checker reconstruction allowances are absolute2e-16/relative8e-15; independent cubic-residual reconstruction absolute4e-15; tiny full-comparison maxima absolute1e-30/relative5e-13. They are never added to frozen scientific gates. nextUp uses integer stepping of the stored binary64 representation. Root verification evaluates saved scalar polynomial/power identities only and does not solve a root.

Evidence integrity and scientific qualification are separate. Accepted completed cases must satisfy the reconstructable saved gates. A failed or incomplete campaign can have internally consistent evidence without becoming scientifically qualified. The reviewer inventories partial tails and available completed prefixes. A failure-reserve fallback is marked evidenceIncomplete; discarded diagnostic content cannot be recovered from its saved hash. A missing/empty started record has no scientific qualification. A failed H1 or H2 performance criterion is a legitimate complete negative result when scientific qualification passes.

Limits remain explicit. No saved geometry or world rotation is regenerated. C does not retain all fallback IDs or unselected-positive bound values. Shared zero assertions and full-code hashes are retained runtime evidence; successful audits do not contain all-source term doubles or full code vectors. Successful timed matrices and timed decision masks are not saved, so the reviewer reconciles their checksums/counters and separate validation assertions instead of claiming independently replayed pointwise comparisons. The support-code tally for selected sources is a saved-data diagnostic. C/Z includes Z reporting overhead and changed downstream receiver work; M/Z includes the zero-screen package's bounds/selection/masks. Positive envelopes do not imply strictly positive realized terms. Two same-family inputs and eight technical blocks support no population, physical, flight, trajectory, real-time or novelty claim.

The coordinator must make the sole separately authorized launch under an external timeout of at most59seconds within the60second allowance. Before launch, create a unique /tmp/m31-ablation-verifier-launches/<time_ns>/ directory and preserve exact invocation arguments, original checker and this memo; retain exclusive stdout/stderr/runtime files even if Python fails to start. The checker installs a55second alarm and creates /tmp/m31-ablation-verifier-runs/<time_ns>/ with checker, arguments, original scientific start/result/budget, stdout/stderr/traceback, review JSON and runtime. Canonical /tmp/m31-ablation-saved-review.json is created exclusively, never overwritten.

Exact planned invocation:

```
python3 /tmp/m31-ablation-saved-review.py \
  <REPOSITORY_ROOT> \
  --source-commit b6aafb006bbc406deb95f7defcebde6801eaa7f5 \
  --freeze-sha256 ccd1695ca48fefd85225c830fd1a93fbbd6bfbde4e1fcaffd1e0532a9c799ec0 \
  --authorized-after-science
```

No independent trial invocation is authorized. Preserve every original result, error and runtime. Any correction or rerun after the sole launch requires a separately recorded justification and authorization; do not silently edit or retry. After the coordinator launches, a final memo may interpret the saved report and append this preparation memo verbatim.
