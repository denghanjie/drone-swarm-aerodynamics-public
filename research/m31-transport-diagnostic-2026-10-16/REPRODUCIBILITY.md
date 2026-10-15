# Source, environment and reproduction boundary

The sole diagnostic entry point is `source/capture-transport.py`. It owns one external observer, one relay/Node invocation and at most one explicitly identified headless Chrome lifecycle. The seven source files are self-contained transport/lifecycle code; none imports a scientific module or reads prior raw data. The retained lifecycle design derives from the preceding campaign, with a newly reviewed resource envelope. The protocol and source freeze govern execution, not this explanatory file alone.

Environment: Darwin arm64, Python 3.9.6, Node 24.19.0, Playwright 1.62.1 and Chrome 155.0.8059.80. `runtime-provenance.json` retains partial executable/package inventory hashes. It does not pin every OS, browser resource or driver file. No dependency installation, browser downgrade, security flag or permission change is part of this diagnostic.

Before the one permitted launch, the coordinator must publish the exact source freeze, independently retrieve it, reconcile its bytes and every local pin, and supply the source commit and verified freeze hash through `RESEARCH_SOURCE_COMMIT` and `RESEARCH_REMOTE_VERIFIED_FREEZE`. Supply the installed Node path, `NODE_PATH` and explicit `RESEARCH_CHROME_EXECUTABLE` privately. Public records omit installation paths. The existing localhost origin is preserved; no server restart is required because the fixture is route-fulfilled from frozen bytes.

Command shape, shown without machine paths:

```text
python3 source/capture-transport.py <absolute-pinned-node-executable>
```

The root retains the actual tool completion, complete caller summary and observer summary separately under `publication/`. Tool wall observation includes command/tool latency and any completion polling; it is a conservative full-completion observation, not a transport performance measure. The saved reviewer consumes only this new diagnostic's fixed evidence manifest.

Existing launch locks are permanent. After terminal execution, never repeat an entry point, change source, fill omitted stages or reuse this output directory. An intentional independent replication requires its own prospective decision, isolated evidence area and runtime admission. Retaining commands and code does not assert portability or authorize retries of this record.

Full private traces and process registries remain private. Public trace transformations are specified in `SCHEMA.md`; public-file checksums refer to the transformed bytes. Byte verification and event consistency do not prove complete browser-event delivery, original failure causality, numerical correctness or physical validity.
