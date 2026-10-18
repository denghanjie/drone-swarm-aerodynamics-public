# Saved-result protocol review

Reviewer: `/root/m31_protocol_challenge`. Evidence inspected 2026-10-18T12:10:39Z.

## Disposition and decision adherence

**Accept the recorded decision: stop pursuing the current H implementation on this saved N1000 workload.** The registered keep gate failed clearly, while the saved correctness analysis passed. This does not reject all tree methods, other implementations, other sizes or other states.

The protocol required the median of all 24 paired H/F query-time ratios to be at most 0.90, at least 20 strict H < F wins, and all 116 correctness checks to pass. The saved analysis reports:

| Registered quantity | Saved result | Required |
|---|---:|---:|
| Median paired H/F | 2.2822220357956775 | <= 0.90 |
| Strict H wins | 0 of 24 | >= 20 of 24 |
| Correctness | 116 checked, passed | All 116 pass |
| Keep gate | false | All conditions pass |

The raw query rows show H slower than F in every measured block. Their saved paired ratios range from approximately 1.5878 to 2.7205. The central two sorted ratios are 2.279891282165096 and 2.2845527894262587, consistent with the reported even-sample median. The decision uses paired ratios, not a ratio of the two arm medians. There is no tie to count as a win. No trimming, alternative threshold or diagnostic-query substitution is needed or justified.

Calls 1–16 are the four warm blocks; calls 17–112 are all 24 measured blocks; calls 113–116 are the final F/H/HC/H0 instrumented diagnostics. The raw records follow the registered four-order Williams cycle, with each measured arm in each position six times. The warm and diagnostic records remain present and do not enter the primary statistic. The saved result therefore supports the stated negative performance decision under the prospective rule.

This review used saved JSON/text, metadata and file hashes only. The reviewer inspected all 116 raw query records' schedule, query times and declared correctness fields, the 24 reported pairs, all four raw diagnostic records, relevant frozen timer/analysis source, and the saved publication/closure receipts. **No experiment, codec, scientific producer, analysis script or checker was rerun.** Full semantic-byte validation remains the result of the one separately executed independent analysis, whose source and output were inspected; this review does not claim a second independent runtime validation.

## Timing scope

The measured cost begins before fresh hexadecimal state decoding and ends after the complete native query and submitted-input immutability comparison. It includes native validation/copy/order, geometry/tree work, admission, solve, residual, loads and consumption. The label should therefore be “complete query cost including input restoration and immutability checking,” or an equivalently explicit description. Native internal time is secondary.

The saved arm summaries, rounded for reporting, are:

| Arm | Primary median, ms | Primary interquartile interval, ms | Native median, ms |
|---|---:|---:|---:|
| F, screened scan | 36.85 | 35.875–45.925 | 34.20 |
| H, capture disabled | 85.15 | 84.225–85.950 | 82.65 |
| HC, capture enabled | 90.10 | 89.500–90.925 | 87.55 |
| H0, no omission | 106.35 | 104.875–107.550 | 103.80 |

Encoding, semantic normalization/comparison, transfer and persistence occur outside the primary timer. They are retained separately and must not be silently added to, or described as included in, these query medians. Persistence is already included in `transferAndPersistMs`; adding it again would double count it. Separate medians are not additive decompositions of a median total. These measurements do not include rendering or establish interactive frame rate, complete application latency or flight/control-loop throughput.

The measured paired HC/H median is 1.0577742764216473: approximately 5.78% higher query time with capture enabled in this run. That is a comparison of complete queries under the two options, not an isolated witness-allocation microbenchmark. H already has capture disabled and still loses every F pair, so disabling witness capture alone does not rescue the tested implementation. HC's reported encoding median of 29.45 ms versus H's 23.90 ms is outside the primary timer and cannot explain away the primary H/F loss.

H0/F has a median paired ratio of 2.8786157666216834. Omitting groups improves the tree variant relative to its no-omission counterpart in these observations, but the resulting H still costs more than F. F already uses cheap component screening; this is not a comparison against a deliberately naive full rotor scan.

## Diagnostic attribution

The repeated, uninstrumented `buildAndAdmission` medians are 27.10 ms for F, 75.90 ms for H, 80.90 ms for HC and 97.10 ms for H0. The solve and residual medians are similar across arms. This localizes the principal observed difference to geometry/build/admission work rather than demonstrating a slower solve.

The four final instrumented records contain the following observations:

| Arm | Query ms | Wrapped tree build ms | Combined gather ms | Build/gather calls |
|---|---:|---:|---:|---:|
| F | 51.3 | 0 | 0 | 0 / 0 |
| H | 93.1 | approximately 0.6 | approximately 49.7 | 1 / 1000 |
| HC | 91.4 | approximately 0.6 | approximately 54.4 | 1 / 1000 |
| H0 | 105.1 | approximately 0.6 | approximately 65.2 | 1 / 1000 |

The gather wrapper combines traversal, candidate handling/sorting and capture where enabled. There is one instrumented query per arm, in a fixed final order, and wrapper/timer overhead is present. These observations support a gather-related cost hypothesis; they do not partition exact costs among traversal, sorting, capture, allocation or garbage collection. They must not be treated as repeated component benchmarks or used to subtract an exact causal overhead from the primary medians. In particular, HC's one diagnostic total happens to be lower than H's even though the 24 measured HC/H pairs show a higher median; the primary comparison must retain precedence.

The raw diagnostic work counts give H and HC 627,164 gathered nonself candidates, compared with 999,000 for F and H0: 371,836 fewer candidate entries, approximately 37.22%. All four diagnostic records still report the same 487,242 directed center tests, 149,834 center-eligible pairs, 599,336 `pairCalls` and 9,012 positive rotor terms. Thus the candidate reduction is not a measured reduction in those counted downstream operations relative to the already screened F. It is inappropriate to translate a 37.22% candidate reduction into a 37.22% speedup or equivalent reduction in expensive rotor work.

New tree-witness bodies were not retained or independently checked for each query. HC measures their in-query production cost. Previously saved complete witness evidence remains separate and immutable.

## Correctness, completion and claim limits

Every raw query record declares `native-success`, unchanged submitted input, browser semantic equality and host equality, and pins the same 2,554,203-byte actual semantic blob. The saved independent analysis reports all 116 complete scientific projections byte-equal to the saved F expectation after the registered normalization/exclusions. Its source rereads the actual referenced bytes and checks their hashes, lengths and equality. The actual canonical blob digest is `baee267d0d463ff059f8e61575c8a60f395d9713f9ac8a8a8325875f7c8408d7`. The exported `expected.json` has a trailing newline and a different whole-file digest; the analyzed canonical bytes use the documented stripped representation. This distinction is not a scientific discrepancy.

The saved source-publication receipt identifies commit `94ecec03c1260b7e63f5bbb1dce8345e1b2373b7`, 67 verified file pins and exact public-manifest byte equality at 12:08:57Z. The attempt began at 12:09:18Z, after that receipt and before the registered cutoff. This review reads that saved receipt; it does not perform a fresh remote verification.

The supervisor reports exit 0, no failure reason, approximately 21.01 seconds, public bytes 5,681,636 and private bytes 8,786,725 at its check, finishing 12:09:39Z. The browser record reports exactly one launch, 116 rows, completed/context closed, and root exit and root close both `{code:0, signal:null}`. The external exit receipt reports exit 0; the analysis exit receipt reports exit 0 in approximately 0.157 seconds with no stderr. These are within the registered time and disk limits. They do not establish exit of every OS helper or a hard memory bound. Later report/UI files are outside the supervisor's recorded package size.

The equality result is a bridge to one previously checked saved F result on one projected N1000 state. It is not new physical validation, a high-precision reference, a controller/derivative validation, trajectory evidence or a novelty claim. The timings come from repeated warmed queries in one headless Chrome 155.0.8059.80 process on darwin arm64, launched using Node v24.19.0. The repeated timings are not independent population samples; no confidence or generalization claim follows from them. There is no basis to infer an asymptotic crossover or behavior at other sizes, states, browsers or machines.

The defensible conclusion is: **for this saved 1,000-drone state and this recorded runtime, the current tree implementation preserved the selected scientific output but failed its prospective cost gate; stop this implementation/workload line.** Any future materially different algorithm or workload requires its own registered allocation. The separately allocated saved-result UI step does not enlarge this scientific conclusion.

## Reviewed evidence pins

Paths are relative to `research/m31-cost-decision-2026-10-18`. Hashing is an evidence identity operation, not a checker rerun.

| Path | Bytes | SHA256 |
|---|---:|---|
| `PROTOCOL.md` | 7581 | `23722fbf799ea52972a17b1d35d41913d47864fb2dd41171e3c8131ca529ee27` |
| `source-manifest.json` | 14953 | `1a3fcbcf8c486cdfc34d02d7b3348c2d0f9574431f8fe509c9e65a0c72ef47fa` |
| `source-publication.json` | 856 | `24626e8cfa8411218d4e52dcbe141ab2982fb4341bd5624fe27b1926ee23ec13` |
| `results/analysis.json` | 18882 | `a70864cda28798c32074f46579578917bf819dd42069d6be9ae17daece56d556` |
| `ANALYSIS-EXIT.json` | 263 | `3cf7cebeed79ffd9f729867f5d467265a550ee42ac83e31d8759daaa29fa80d8` |
| `EXTERNAL-EXIT.json` | 161 | `4d181ba8a3fbe3b1665b94eedb37b236d880fd205ed153c754e4c4b022543c2b` |
| `results/attempt.json` | 120 | `352f4abbfa329dabcbf72850f44534586e9c8c9e7449825275d97a38d397ccd3` |
| `results/environment.json` | 532 | `12d9fbd33d4919784b90a01d00df01618caa239588ee193557e1d56b9355dc01` |
| `results/browser-exit.json` | 193 | `3c77c3da15f0ce67bb3a3ca61d58a4262a17d2ed651fabe639a93e8f1fbd7dac` |
| `results/browser-summary.json` | 3587 | `d92086e19a2ffb366b8dafb508911491e178b8799452c531dfb3a95db3a80546` |
| `results/supervisor.json` | 248 | `11182ca2825b0021d87bfdf8a6aab993d6876c34279c37e70c68fb624388f7e7` |
| `results/semantic-baee267d0d463ff059f8e61575c8a60f395d9713f9ac8a8a8325875f7c8408d7.json` | 2554203 | `baee267d0d463ff059f8e61575c8a60f395d9713f9ac8a8a8325875f7c8408d7` |

For a compact identity of the raw row sets, concatenate the unmodified file bytes in lexical filename order, with no added separator. `results/query-001.json` through `query-116.json` total 119,361 bytes and yield SHA256 `babb9181c38e4d9335c702e9bacdd56f80f8803057c29271fe93538527bb8d73`. The 116 corresponding `transfer-*.json` files total 9,365 bytes and yield SHA256 `56f501f0fb5b036f55094b374ca86404fbf99dcf0ad962f83deb63e7076cfda2`.

No result-protocol blocker was found. Reporting must preserve the timing, diagnostic and claim limitations above. This reviewer wrote only this result-review file during this result-review task.
