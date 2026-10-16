# Frozen protocol hash correction

Source-only addendum, 2026-10-16, before dispatch. This corrects the protocol identity in the earlier focused `REVIEW.md`; it does not modify the frozen package or authorize an additional allocation. No supervisor, diagnostic, candidate, checker or scientific workload was executed.

The earlier review quoted the protocol draft SHA-256 `76ab49e4b7af3b91e6424c4f98554bb636718ce522b37aae94daf3f6351076a2`. That value must not be used as the published protocol identity.

The actual frozen `research/m31-coupled-cost-host-2026-10-16/PROTOCOL.md` at commit `a459802be0b46beac72f35568a60533215f8f784` has SHA-256 **`b2177a26c6b5d7f152f1131559b705ab91fcc58a89e3933d15cc22deaab0f4c6`**. I reread the complete current protocol, hashed it, and directly compared its local bytes with that Git commit; they match. The frozen manifest records the same protocol hash and 11,098 bytes. The local source-manifest digest is `f88099916c1a26fe999fb9a0d998d4e048c486e3d27916541762fa0b93b2284f`, matching the coordinator's independently verified remote digest. Remote retrieval itself was performed by the coordinator, not this review.

The final prose makes the reviewed monitoring rule more precise: monitoring failure stops a confirmed live child; when a failed RSS attempt is followed by `proc.poll()` confirming exit, the failed attempt is recorded in `monitorExitRaces` and the child is reaped without another helper attempt. It explicitly does not infer why the helper failed. Child-success, evidence and cap checks remain authoritative. This wording agrees with the previously reviewed implementation and narrows the interpretation appropriately.

The inherited 8,869-byte scientific protocol block was also compared directly with the original protocol at commit `4fdcc83fe870c110679a72666029d4cbc987e22c` and is byte-identical. The final replacement protocol retains the same fixed exposed inputs, 21 controls, eight qualification builds/16 solves, 84 full/56 cached calls, numerical tolerances and comparison criterion; one new 300-second candidate and one new 60-second saved-review allocation; and approved-host dispatch for both. All earlier allocations remain closed. No substantive scope mismatch or new source blocker was found.

The supervisor is unchanged from the reviewed version: SHA-256 `e9a085abc9544292f5312ce148ab6fcda60146dbb754b11be87d9b762b824e26`. The earlier numerical-source identity findings and limitations remain applicable. Read this addendum with the original review; preserve both rather than rewriting the already frozen review evidence.
