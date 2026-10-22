# Buffered neighbor lists on recorded flock motion — prospective protocol

22 October 2026. Computational only. This study tests implementation equivalence and measured query cost, not physical accuracy, flight safety, novelty or large-population speed. No model, controller, skin width or trajectory is tuned. The candidate is the unchanged 20 October buffered source-ID implementation; baseline is the unchanged fresh F implementation.

## Question and exposed evidence

Does retaining conservative possible-neighbor lists save complete native-query time on short recorded N64 flock-motion windows, while preserving all scientific outputs and the previously observed near-field refusal? Reuse is established prior art. The original buffered attempt stopped after18calls at a small control with an incorrect success expectation, before reaching N1000. A separate corrected31call attempt passed twelve small control pairs, then reached a near-field refusal on the seventh N1000synthetic state before obtaining a paired speed comparison. The earlier tree alternative was slower on its tested workload. These histories are retained, not rerun.

The four fine-step paths in `m31-paired-resolution-2026-10-21/results/index.json` are already exposed. In its case order choose global attempted-stage ordinals 0–159, 4000–4159, and the last160. Thus starts are 0,4000,5632 for first-original and 0,4000,7840 for each other path: twelve160stage windows,1920 unique selected inputs. The known near-field refusal is last stage of window2. Selection is targeted, not random/held-out. A window is about0.1simulation seconds. These are RK trial-stage inputs, not completed endpoints: equal and sometimes nonmonotonic timestamps and distinct k2/k3 states are retained.

## Execution and comparisons

Extract once from all93 exact-hash compressed parts. Each part is verified before first decode; verify concatenated compressed/raw identity and record counts. Selected envelopes preserve full journal objects, raw-line byte length/SHA/uncompressed offset, case/segment/ordinal bindings. Extraction never imports a scientific module. Failure closes extraction and blocks replay. Three identity-read attempts maximum before parsing; each failed read retained. These are transport reads, never numerical retries.

Replay in rep order -1(warmup),0..7(measured), window0..11, all160 stages in order. Method order F,C when `(rep+window+10)%2==0`, C,F otherwise. Candidate cache resets at every window/repetition. F has no cache; time its symmetric empty reset boundary. Exactly34560query calls maximum:3840warmup+30720measured. Call unchanged F/C.query(input,'F',guard). No model integration, additional controls, synthetic query, tuning, outlier deletion, extra repetition or forced garbage collection. Closed older allocations stay closed.

Compare freshly encoded F and C with the saved encoded native evidence on EVERY call, by complete canonical byte equality and hash. Validate method F before exclusion; auditor separately checks archived provenance. Exact excluded paths only: method; timing; diagnostics.buildPhasesMs; diagnostics.geometryWork.gatheredNonselfCandidates; diagnostics.screen.orderedPairVisits; diagnostics.screen.componentTests; top-level caseId; semanticInputSha256; inlineInputCanonicalSha256. Sort object keys, recursively encode numeric values as binary64 big-endian16hex words, retain strings and signed-zero words. Retain all other diagnostics, IDs, raw/prepared states, coefficients, admission/refusal, solution, loads and consumption. Input words before/after must match. Matching known refusal is expected; added, missing or changed refusal fails correctness. All18 repeated refused calls remain included.

## Timing and decision

Primary timer includes fresh input copying, full query/result construction and all list checks/builds/rebuilds; add measured reset cost per method/window. Encoding, reference comparison, witnesses and disk persistence are outside primary timer and recorded separately; their allocations/GC effects may still influence this single-process instrumented runtime. This is not full application throughput. No isolated hardware benchmark or statistical population claim.

Each group retains resetMs, sumQueryMs summed from0, totalMs accumulated from resetMs, admitted/refused sums and counts. For each measured repetition sum12window totalMs per method, then ratio C/F. Primary cost gate: median of these eight aggregate ratios<=0.90 and at least7/8 strict C<F wins. Per-window eight ratios are descriptive. No significance test. Primary cost includes terminal refusal; admitted-prefix and refused-call times also reported separately.

Correctness is required throughout. Independent audit reconstructs candidate boxes/ordered rows, all counters, containment and current omitted-pair screen coverage. Store every candidate witness losslessly with explicit binary64 box words. Qualification also requires actual reuse and at least one motion-triggered box-exit rebuild across the measured workload. Cold builds alone do not qualify. Missing rebuild coverage means qualification/keep gate unsatisfied; do not lengthen windows after seeing outcomes. Full keep gate = correctness AND cost gate AND coverage gate. Passing supports only further study of this sampled chopped-window workload; failure rejects no broader algorithm family.

## Bounded allocations and source gate

Freeze all code/protocol/config/review/runtime/required-source pins, publish, independently verify public source before extraction. Old raw pins rely on their independently verified public result checkpoint plus local exact hash before use. Extraction index dynamically binds selected output before replay; auditor independently rescan-binds selected source records. No new source change is permitted after freeze. All five allocation locks are single-use, sequential, no overlap. Internal guards plus external supervisor wall/output limits:

|Allocation|Wall cap|Output cap|
|---|---:|---:|
|Extraction|1200s|768MiB|
|Native replay|1800s|768MiB|
|Independent audit|1800s|256MiB|
|Display packaging|120s|2MiB|
|Browser check|150s|16MiB|

Native replay reserves2MiB for closure. Complete semantic bodies and cache witnesses are content-addressed with byte-verified deduplication; per-call rows retain exclusions, timings, identities and cache stats. Selected raw records are losslessly gzip compressed. A cap breach closes unsuccessfully, never drops evidence or silently enlarges a budget. Approximate static expectation:1920distinct semantic bodies (rather than34560full duplicates),1920selected records,34560small query rows, deduplicated cache witnesses. Output caps are hard ceilings, not guaranteed capacity. Single failed allocation preserved; no automatic scientific rerun.

UI uses saved audited positions only, offers12windows and discrete RK-stage playback, marks refusal and sample gaps, and reports measured costs/coverage and limitations. No fresh model queries in browser. Audit/UI failure blocks a qualified result; code/display corrections need separate allocations. Privacy review, raw results, manifest, independent result review, public publication receipts and restart instructions complete the milestone.

Pre-freeze review clarifications: runtime-binary hashing occurs inside the supervised process group, so a blocked identity read is bounded by the same allocation. Node preload/search environment variables are removed before launch; only the UI receives the bundled sibling node_modules path. The supervisor starts termination two seconds before the stated wall cap, polling at one-second intervals; a termination or late closure is failure. Compressed extraction writes (including trailers) are charged before each underlying write, with2MiB closure reserve. Packaging accounts its additional viewer/pins.json (at most64KiB) within its2MiB budget. The per-call encodePersistMs covers encoding/comparison/witness/CAS preparation through the pre-journal timestamp; the row's own append is outside that timer. comparisonMs is also explicit. This instrumented experiment cannot estimate uninstrumented application throughput.
