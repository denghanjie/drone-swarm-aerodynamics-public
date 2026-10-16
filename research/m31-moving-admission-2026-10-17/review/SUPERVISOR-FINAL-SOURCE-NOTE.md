# Supervisor source pin finalization

The initial adaptation note and inventory are preserved. Before freeze, the parent identified a chronology edge: publication.verifiedUtc can contain microseconds while the old attempt.startedUtc string truncated to seconds. A launch in the same second could falsely fail the runner's receipt-before-attempt gate after consuming the permanent attempt. The sole source change from the initial adaptation note is `datetime.now(timezone.utc).isoformat()` for startedUtc. No run was attempted to diagnose or validate this source correction.

The independent evidence-audit reviewer reports a full static reading of the supervisor and guardian plus the exact final timestamp delta, with no blocking containment mismatch. This author's note records the final source identities; it does not substitute for that independent review or the later public-source gate.

Final source pins:

- source/supervise.py: 26727 bytes, SHA-256 `8d23c224fd0f976552fd266ea5dac13e9fc9c7566d8694f7c23f14fab57eec27`.
- source/guardian.py: 2276 bytes, SHA-256 `10341c52ab32fa8ff80c3909d578a7d368a3b2bcea59e78af7e8aa8f29c619f0`.
- runtime-pins.json: 248 bytes, SHA-256 `842b2522133ed499f4706e071b09f3d100c5f4ed3f41d0fd135736c4dc191087`.

Final inventory: SUPERVISOR-FINAL-READING.json, 3076 bytes, SHA-256 `90aec8b381dbd08c28d94b84790510abd9cbc91d533f221da42b37cae8a19085`. Fresh inherited-content count remains4/20. All prior source-only limits, resource bounds, isolated-mode requirement, cutoff and no-retry obligations remain unchanged. No execution is authorized by this note.
