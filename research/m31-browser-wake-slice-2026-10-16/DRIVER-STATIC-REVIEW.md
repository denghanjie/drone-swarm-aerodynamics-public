# Wake-slice driver and supervision — provisional independent static review

Disposition: no full launch clearance. This review covers the draft driver/browser/supervisor and declared GPU interface; final host, WGSL, protocol, schema, freeze, publication, and prospective saved-review preparation remain outstanding. Only static text reads, comparisons, file hashes, and declared-size arithmetic were performed. No module import, model evaluation, browser/shader execution, checker, or prior-budget reuse occurred.

## Reviewed draft identities

Repository-relative campaign: `research/m31-browser-wake-slice-2026-10-16/`.

| File | SHA-256 |
|---|---|
| `source/browser.js` | `602ecea171206b5f26f752817b1bec933665a9cb8d7c089e071fa8ff26bfb2f6` |
| `source/experiment.cjs` | `5c7ffb132773f89825956f9846ae9cf1a3dd824be5d844c993422b5484e40ce5` |
| `source/run-once.py` | `33243fb882a0d8735cbe5eca0fefeb2c1cef5f8cebcb941d040e412bde6069d1` |
| `source/process-registry.cjs` | `cd6ceca7bc85b5de340cbd61996642f53bd7affc56654427a3c921c926ed3152` |
| `config.json` | `85476f0aa1784706345b9d9f1ad6da8e9fb197392561fd4a96ec2642ead5398c` |
| `SUPERVISION.md` | `1aa51b20b61c5a326b2941e4a005ffa1fca4dd574982db7c03313f8e47161a18` |
| `KERNEL-CONTRACT.md` | `ac4245fb4848d229a29f1464628bf618285d65a0542e30c9fa3c6f1e9fd9f961` |
| `controls/controls.json` | `55035545e61ca16d0c112b45e278ae94e4cb31fb7940bc8dd567cd9f95796219` |

These drafts are evolving. Any changed bytes require a targeted follow-up; hashes here do not freeze or authorize them.

## Launch-blocking finding

**B1 — Cache known adapter evidence before awaiting device creation.** In `browser.js:13–20`, adapter metadata is assembled locally, but `wakeInitializationEvidence` remains `{phase:'request-adapter'}` until `requestDevice()` and the actual device-limit check have completed. A rejected or stalled device request therefore loses already available adapter evidence and reports the wrong last phase. Before the await, cache `{phase:'request-device',adapter:meta}`; update the cache when actual device limits become available. This is an evidence-preservation repair, not an invitation to retry device creation. The parent was notified during review.

## Required final-contract completions

These are incomplete prospective declarations, not claims that an unseen host/kernel implementation is wrong.

1. **Count launched lanes separately from active slots.** The browser submits 1,250×64 term lanes, 1×64 control lanes, and 1×64 reduction lanes: 80,128 launched invocations, 80,032 active output slots, and 96 padding lanes (48 controls +48 reductions). Configuration counters currently reserve only active slots. Declare padding and early-return semantics in the final operation ledger, together with the API's control helper-path reservations. Do not label active slots as all launched invocations. Three pipeline creations, one preparation/upload stage, three dispatch/readback/error-scope stages, and final health/cleanup calls must also be distinguished from scientific term counts.
2. **Specify all resident typed arrays, device buffers, and serialization copies.** The eight permanent GPU buffers sum to 6,564,176 bytes. The largest additional readback is 6,400,000 bytes, so their maximum simultaneous declared GPU-buffer capacity is 12,964,176 bytes before runtime overhead. Host/browser base64 strings, mapped copies, decoded arrays, reference arrays, assessor state, terminal JSON, and transient hashes need separate accounting once the host/schema is final. The 64 MiB cap is raw evidence, including a 4 MiB failure reserve; it is not a hard host/Chrome/OS memory cap.
3. **Verify every host API/schema and exact-dyadic gate after assembly.** `savePrepared`, `saveReference`, and the four assessors are presently assumed interfaces. The decisive gates now required are exact-dyadic `Σ|Q_j−R_j| + 1e-12 <= eps` and `Σ|T_j−R_j| + |S−ΣExact(T_j)| + 1e-12 <= eps`, where `eps=3*originalInduced*1e-7/f0` is the specified binary64 engineering value. Preserve term-level T−Q and signed attribution as diagnostics; do not replace exact saved-operand arithmetic with an ordinary float64 sum. Big integer evidence must have a frozen JSON-safe encoding. R reproduction, code/status completeness, and the reference allowance still need source-level verification.
4. **Require the complete terminal qualification conjunction.** An unsupported adapter deliberately yields `out.pass=false` but currently leaves Node exit status zero (`experiment.cjs:49`); the supervisor reports process closure independently. Final qualification must require the driver's successful scientific result, external no-timeout/under-cap/cleanup result, exact data coverage, and the sole saved review. Supervisor exit zero or `status:'closed'` alone is not numerical qualification. This is acceptable if explicit in the final protocol/reviewer.

## Positive static findings

- **Original term-buffer identity is preserved by the browser wrapper.** `prepareWake` creates `buffers.terms` once, with STORAGE|COPY_SRC. The terms and reduction bind groups both bind that object. Readback copies it into a separate MAP_READ buffer, which alone is destroyed. There is no term reupload or intervening wrapper write, and the stage machine permits controls → terms → reduction only. The final WGSL still must be checked for unintended mutations; a retained handle alone cannot prove shader behavior.
- **Raw results precede dependent API qualification.** `dispatchWake` copies mapped words, initiates (but does not await) `popErrorScope`, and returns the raw base64 payload. The driver writes the raw file and readback metadata before calling `finishWakeBatch`. Raw bytes, validation, device loss, and uncaptured errors are checked under the single outer 10-second batch deadline. Failure leaves a saved prefix when transfer/persistence completed.
- **The browser starts no computation on page load.** Three static entry-point pipelines are created in initialization; preparation allocates declared-size buffers and uploads only inputs; each wrapper call submits exactly one dispatch. Reduction consumes the existing storage object. No warmup, fallback, repeat, root, or field pass appears in these files.
- **Exact source delivery is explicit.** Playwright fulfills frozen HTML, JS, and WGSL bytes. The driver retains delivery metadata and verifies the returned shader text hash. Runtime claims are correctly limited to the pinned executable/package entries plus browser version, rather than a complete transitive browser hash inventory.
- **Failure and cleanup sequencing is bounded.** Failure-evidence retrieval is limited to one second. GPU shutdown has its own one-second deadline; browser close is still attempted afterward with its three-second deadline. The external 60-second supervisor remains authoritative when JavaScript blocks. A cooperative guard is a scheduled check, not instantaneous preemption; wall overruns must remain failures.
- **Detached-process supervision is retained.** Static comparison shows `run-once.py` differs from the previously reviewed receiver supervisor only in its campaign docstring and registry prefix; `process-registry.cjs` is byte-identical. The registry is installed before Playwright, browser registration is asserted before GPU work, and final cleanup checks detached groups even after normal Node exit. Surviving groups require the executable/profile or Node invocation fingerprint; unconfirmed ownership fails closed. The documentation correctly discloses race intervals, missing hard containment, and that active kill/ownership paths have not been failure-injected.

## Suggestions, not current launch blockers

- In the pipeline-creation rejection branch (`browser.js:25`), retain the outstanding validation-scope result if obtainable within the already frozen initialization deadline. The current branch fails closed and saves the exception/compiler messages, but leaves the scope uncollected. Also include uncaptured-error metadata in that failure return.
- Parent `Promise.race` deadlines do not cancel the underlying browser RPC. Document that a timed-out batch may still return and persist a late completed prefix while bounded failure retrieval/cleanup is in progress; it cannot authorize the next dispatch. The final saved reviewer should classify such evidence under the failed attempt, never a successful stage solely because raw bytes exist.
- A direct assertion that the readback sidecar's declared group/count/output-byte fields match the frozen kind would improve local diagnostics. The fixed wrapper already supplies those values; the final saved review must nevertheless verify them.

## Checklist corrigenda and scope clarification

The initial `isolated initial prospective checklist` inherited a 65-character receiver-manifest transcription. The correct prior receiver manifest SHA-256 is `7d91e41da4b873cc4b3ffba188ac111871b10554d68a17d4eec57847a320be2d` (64 hexadecimal characters; 140 pins). The parent has retained the initial artifact and disclosed its corrected preparation copy. Also, nominal yaw is not tested in this wake-only scope; no loads are evaluated. Neither the wake tolerance nor raw-byte capacity should be presented as a load-validation result or full process-memory limit.

Fixed selection now received: receiver IDs `[27,445,4500,988]`, four rotors each, source-major index `((selectionIndex*5000+sourceID)*4+rotor)`, selection SHA-256 `00bfae2e0d0cc8cfc811556ea549fe69399d45882693b760f612e15f8daa125f`. These are exposed rows chosen by the saved-data rule, not holdouts. The weakest zero-inflow row remains in the slice.

Final review remains pending after B1 is repaired and the complete host/kernel/protocol/schema/freeze set is supplied. No scientific or saved-review invocation is authorized by this memo.
