# Reproduction and evidence inspection

This original campaign is closed. Do not rerun the driver, remove started/lock files, change a budget or use another job ID. A future independent reproduction needs its own declared protocol and budget, preserving this evidence.

Historical scientific invocation (record only):

```
RESEARCH_SOURCE_COMMIT=4717d9b5bb3d82fe2b3d75ea26801de201d124b6 python3 research/m31-zero-screen-2026-10-16/source/run-step.py --id sole-zero-screen --timeout 300 -- node research/m31-zero-screen-2026-10-16/source/experiment.cjs
```

RuntimeNode24.19.0, Python3.9.6 supervisor, AppleM4/Darwin25.5.0arm64. Read PROTOCOL.md/config.json/schema.json/freeze.json for exact methods, seed shapes, gates, dependencies, accounting and retained-evidence limits. Original40pins remain unchanged. The external source commit and freeze bytes were independently verified before generation/execution.

Float64LE files have17columns as schema.json. E/L packed2bitmasks:0self/outside,1screenedzero,2near-domainfallback,3remainingretained. Zcode3is shadow-selectedbutactuallyretained; map3to2for actual mask comparison. E/Lcode2is also retained. Independent audit code vectors have4Nbytes perreceiver. Zero-returnclasses1,2,4,5;code6projection-zeroevaluation;code0/3cannotcertifyeligiblezero;code7mayroundtozeroandrequiresanexplicitexceptionwhenclaimedzero. Successful full term vectors and timed matrices are absent.

Saved review original checker SHA25696c324e62ef554c98ff599f49d338b6830d2a23f6c1e292782f0438bb49e4b67 was executed exactly once under59sexternal/55sinternal guards, within separate60sallowance. Results and original/public transformation hashes are preserved under results/. No scientific module, geometry, generation, root solving or timing repeat occurred in that review.

Serve repository root with a local static server; open research/m31-zero-screen-2026-10-16/viewer/. It verifies saved result, poses, E/Lloads and both decisionfiles, then validates selected decompressed masks. It displays saved values only. source/build-viewer-data.py reproduces metadata by hashing existing files; it does not evaluate physics. BrowserQA is separately recorded and does not count as a scientific timing benchmark.
