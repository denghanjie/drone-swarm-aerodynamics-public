# Receiver browser experiment: final static disposition

Date: 2026-10-16. Repository: <REPOSITORY_ROOT>. Campaign: research/m31-browser-receiver-2026-10-16.

**Disposition: bounded static approval for the reviewed source design, conditional on the prospective freeze/publication/pin verification and all declared runtime/saved-review gates. No claim of numerical success, browser support, execution success or unconditional OS containment is made.** The four original execution/evidence gaps and the detached-browser supervision blocker have been addressed in the identified snapshot. No additional blocking source issue was found within this receiver-only, single-attempt scope.

This review used source/dependency/protocol text reads and file hashes only. No scientific module import, shader parsing/compilation, browser/GPU launch, dispatch, root/field/geometry calculation, input-matrix interpretation, benchmark or saved checker execution occurred. No repository files were modified by this reviewer. Earlier reviews remain preserved at /tmp/m31-browser-receiver-static-review.md, /tmp/m31-browser-receiver-static-followup.md and /tmp/m31-browser-receiver-detached-process-review.md.

## Containment repair assessment

1. experiment.cjs requires process-registry.cjs before requiring Playwright. The registry wraps child_process.spawn with the same original arguments and return value. The pinned Playwright coreBundle browser path calls that API with command, argument array and options, so the hook sees the actual detached Chrome creation. The coreBundle used to establish this behavior is now included in runtime pins.
2. The supervisor creates an unpredictable private temporary registry before launching Node and passes its absolute path through the environment. The wrapper synchronously appends the PID, detached flag, executable and existing unique --user-data-dir argument before returning the ChildProcess. Append failure attempts immediate child/group termination and throws. The driver requires a registered detached Chrome entry with a profile argument before creating the page or invoking any shader/GPU action.
3. The supervisor includes its Node group and all registered detached groups in final cleanup, including after ordinary leader exit. This corrects the earlier assumption that Chrome belongs to Node's group. It first tests group existence, then obtains the live leader command with /bin/ps -ww and a 150 ms bound. A surviving group is signaled only after matching the exact executable plus the unique Chrome profile argument, or the known Node invocation. Missing leaders, unreadable/mismatched identities and errors are unqualified, with no signal to an unidentified group. The -ww option avoids truncating Chrome's long arguments before the ownership token.
4. Group absence is polled with at most twenty 50 ms sleeps. Registry read/parse and private audit errors prevent qualification and are retained in the terminal ledger. The supervisor reserves 1.5 seconds from the 180-second wall allowance for cleanup and rejects elapsed time at or above the cap. GPU shutdown and browser close are separately attempted under 2-second and 5-second bounds, and either cleanup failure rejects qualification.
5. This remains ordinary bounded process supervision, not an atomic process container. The spawn-return-to-registry-append interval can be interrupted before registration; no scientific GPU work can be reached through that interval because registration/assertion precedes page/GPU initialization. The live-identity-check-to-kill interval is also non-atomic. An unidentifiable surviving group is deliberately not killed and causes failure. The protocol now states these limits. They must remain visible in any claims; do not describe every possible OS failure as guaranteed contained.
6. The ownership check is an appropriate practical protection for this short, serial, one-attempt campaign. It avoids treating a historical numeric PID alone as unconditional kill authority. It is not a security boundary against hostile same-user tampering with process arguments or the private registry. No such adversarial scope is claimed or needed here.

## Evidence and arithmetic assessment retained from prior static reviews

- The shader rejects exceptional raw u32 exponent patterns and nonzero padding before float interpretation; admitted positive alpha has the frozen 2^-120 lower bound. The fixed Newton expression, 12-update cap, original threshold and zero-input identity remain unchanged. Current positive-input metadata additionally requires alpha > 0, and a cap record requires both 12 iterations and a final step at or above the f32 threshold.
- The browser checks actual device limits as well as adapter limits. Unsupported capability terminates without fallback or retry. Device-loss and uncaptured-error state are separate from compilation/pipeline responses.
- Readback words are copied/unmapped and returned separately from the pending error-scope result. The driver persists raw words/readback metadata before awaiting finishReceiverBatch. This complete two-phase operation retains one 30-second deadline; a later API rejection/hang cannot erase a raw file already written.
- Initialization phase/adapter/compiler state is cached and recovered through a bounded failure metadata read; unavailable browser evidence is explicitly labeled. Frozen local HTML, module and shader bytes are supplied through Playwright routes, and served-source identities are retained. This removes reliance on unchecked localhost server content.
- R64 reuses all 24,000 saved I roots; only 32 scalar R roots are new. Q64 uses decoded operands and A64 uses returned shader alpha. The total is 48,096 new roots with 4,617,216 reserved bisection slots. Four dispatches reserve 24,032 valid roots plus five invalid guards and 288,384 Newton updates. Field and integration counts remain zero.
- Total rotor, A-root X/residual and Q-parameter power gates match the protocol. Old 1e-12 N rotor outcomes, original-model power and representation/division/iteration/multiplication attribution remain separately visible. Stop codes do not certify accuracy. The new 1e-7 N allocation does not imply old precision, physical adequacy or full-flock qualification.

## Conditions on downstream qualification

The final source/config/schema/protocol/runtime/input freeze must match this design and be independently verified before the sole invocation. Any source changes require checking their effect on this disposition. Runtime outcome must combine the scientific result with the supervisor ledger: a zero process exit alone is insufficient, and pass=true in the driver's result cannot override a timeout, incomplete registry, unconfirmed ownership/absence, cleanup error or exceeded wall/raw/operation cap. Unsupported or partial evidence never qualifies the full suite.

The separate saved-only checker is still unexecuted. Its later single supervised invocation must inspect the actual retained records and hashes, not infer success from this source review. No scientific or review budget is reopened by this static disposition.

## Final reviewed source identities

| File | Bytes | SHA256 |
|---|---:|---|
| source/process-registry.cjs | 1539 | `cd6ceca7bc85b5de340cbd61996642f53bd7affc56654427a3c921c926ed3152` |
| source/run-once.py | 6317 | `0bd0e190892cce5d7934dab0760bdc320cdbc6292664ea9138040d2558e925cf` |
| source/experiment.cjs | 17755 | `f49aa4ac2e533a83987354818266ccb6810f5f6061aba7f41660d9fdf3dba045` |
| source/browser.js | 5559 | `1476e9984454cad29f989d015355d2f41164ff2906b9aad3817abc1382435483` |
| source/receiver.wgsl | 3318 | `dc64e23b3905d635f0d1de4d56233c2380455e89c2f50ee5a59c67baca6f1555` |
| source/reference.cjs | 796 | `4628e2a3a4d843868810bea070153fe22798cfe3e73fd483492ca329558d497d` |
| source/browser.html | 293 | `30821edc65a0ac3d8ee739b7342897142aecf4be1ec3b55a29361f5ac7f04834` |
| config.json | 2312 | `2d89e2cecc048a9427555818507079eb1410836ca38bc04961e867d89b6c29ce` |
| schema.json | 1218 | `9a8d8d440360c3c19f48a28eea5e58cc9535e47e947bc850994db1477747964b` |
| PROTOCOL.md | 13579 | `dc7e1afd8932a0c0af815553c4173377a47ec77b1ba94ddf8ce66dea797e235b` |
| runtime-provenance.json | 1423 | `499b92433a9cf249c026b3f9c7d1edf5d03328c089ad90a6dc04095892f727ae` |
| constant-encoding.json | 6372 | `a3cab7f30b4490308464d1016bbe19539a8d197fb77076860f523c484c54005e` |
