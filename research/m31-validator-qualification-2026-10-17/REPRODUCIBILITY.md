# Reproduction boundary

The official allocation is single-use and launch-time bounded. Read PROTOCOL.md, source/config.json, source/result-contract.json and SOURCE-DECISION.md before invocation. The complete new source must first be committed, pushed and independently retrieved at that exact public commit; source-publication.json records verification. The old public source/result chains are distinct immutable inputs, never rewritten with the new commit identity.

Use the pinned Python executable in isolated mode and a new private raw-log directory:

```sh
export RESEARCH_PRIVATE_RUN_DIR=/tmp/new-private-validator-qualification-run
/absolute/path/to/pinned/python3 -I -B research/m31-validator-qualification-2026-10-17/source/supervise.py qualification
```

No Node runtime or additional runtime-path environment variable is required. The private log path is execution metadata and is not published. Keep HEAD at the independently verified new source commit until closure. An existing attempt marker permanently prevents another official run. The wrapper owns resource containment and child-group closure. No direct driver call bypasses the publication, provenance or attempt checks. The official launch cutoff is 2026-10-16T23:00:00Z; third-party reproductions require a separately declared allocation and provenance review rather than deleting markers or changing this historic source.

After closure, inspect results/qualification.json and its referenced independent outputs, lifecycle reports and saved-evidence reviews. The report concerns previously exposed input states. The old passed=false/advancement=false outcome remains permanently visible. The new Three.js page replays the existing pose records; no animation is numerical evidence of new flight, feedback or compute rate. Scientific and display verification are separate allocations, each with their own saved outcomes.
