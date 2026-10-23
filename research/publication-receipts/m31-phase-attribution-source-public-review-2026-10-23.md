# Independent public source verification — phase attribution

Passed. All source and immutable input pins plus the manifest were freshly checked against local/source-Git/public bytes. Every one of the 29 inputs also received a fresh origin-Git read. No prior public proof was reused.

- Source commit: `e99ce65cd6bbafa705e412ddd58c3058a9251eab`.
- Manifest: 13793 bytes; SHA-256 `3ecea50f0e96a49187a22ae8950ce37fd4b17d131832b9fa591b46d548e57bcd`.
- Verified file pins: 54.
- Fresh public reads including manifest: 55; 97948888 body bytes.
- Route: existing-gh authenticated GitHub Contents API raw response at exact commit, after public repository visibility verification. This is not unauthenticated raw-CDN evidence.
- At most two concurrent transfers, three attempts per identity, 45 seconds per attempt, 900 seconds overall, 512 MiB aggregate captured public bytes.
- Failed attempts: 0, individually retained in JSON/journal.
- All four prospective allocations remained unstarted at start/end. No model/analysis/audit/UI execution, native query, archive decoding or reaggregation occurred.

## Coverage

| Path | Kind | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| `outputs/step02b-source/vendor/OrbitControls.js` | source | 38703 | `b97879c748170baadeb3fb84cea1ffdf4674e283dc06042f34e2acb95a76042c` |
| `outputs/step02b-source/vendor/three.core.js` | source | 1403455 | `eb077d2417f61d3e6d9264c317cabc4ea35769ed6b0ab533067292a550784c20` |
| `outputs/step02b-source/vendor/three.module.js` | source | 603113 | `c8211c69345d2e9949dc7a8ac969380497aa0600a5a8ac6a459c8cd02dd9cb8a` |
| `research/m31-cost-decision-2026-10-18/SUMMARY.md` | input | 4917 | `78d29c0c353425fa77c95735464f7aade68c4bd92301496de9cb7dab97a18f72` |
| `research/m31-native-fresh-transfer-2026-10-17/source/native-load.cjs` | input | 16262 | `b4699a8025e27dcd34e9a206e0330a2c08d7caa61e934ec203d142876e1430f1` |
| `research/m31-native-fresh-transfer-2026-10-17/source/vendor/kernel.cjs` | input | 16676 | `efc87f4c0f9d1a5a9b754d9d334ce295227a0cb01ce6980e4818313dd35d3bc8` |
| `research/m31-neighbor-density-2026-10-23/results/stages.jsonl` | input | 9063908 | `8098f5d2478b9a7f7184ed34f5df41199b565f969e9691ad9099ee6f3e48c1c3` |
| `research/m31-neighbor-density-2026-10-23/results/summary.json` | input | 16311 | `f786d6424102ce501e021531dadb94d9a66938870572045362dc85a290c06644` |
| `research/m31-phase-attribution-2026-10-23/CLAIMS.md` | source | 932 | `a9b18363b80efd8d9079c0385d54778de05b996d319f08cc84a16f7fb8bdc315` |
| `research/m31-phase-attribution-2026-10-23/LITERATURE.md` | source | 1313 | `d20754ce2756d6a95f89d6a0010e32448bd14520c38e2735d4cbedbfdd37305a` |
| `research/m31-phase-attribution-2026-10-23/PRIVACY-SOURCE.json` | source | 280 | `d4b344bdbe5e058e44e3d4690692958cb3e0a1e7ec288e1e095cf7f8fb772aac` |
| `research/m31-phase-attribution-2026-10-23/PRIVACY.md` | source | 584 | `998d417b3e6cfe7f3e36cbfc9dbc2c7c363e2f54ed2407d9faaa239578573848` |
| `research/m31-phase-attribution-2026-10-23/PROTOCOL.md` | source | 7633 | `122dce362b1b80ccd57bd974219add82e3a1dd08b25c76e6b92ed5240f4ef763` |
| `research/m31-phase-attribution-2026-10-23/RESTART.md` | source | 1120 | `597df1c386507b64766b69366b663add48e34c38984a708813d3a862963c82a6` |
| `research/m31-phase-attribution-2026-10-23/SCHEMA.md` | source | 2530 | `e6cdb308ddb93966638a3b9ab4516f322c9b82daeea53cb3eb5dc8adefc77d26` |
| `research/m31-phase-attribution-2026-10-23/SOURCE-CHANGES.md` | source | 1386 | `b4c8d8e8f4f3f2ebda2cd6ccebd05dda924dcd912f2dc2e1782b882597b68012` |
| `research/m31-phase-attribution-2026-10-23/config.json` | source | 1327 | `583215257483814146cfdcfe4d66ec0b60f6b9b3630887ecea54632734da714f` |
| `research/m31-phase-attribution-2026-10-23/input-pins.json` | source | 8428 | `f937a6027edfccac7f7359f5654f561c54540136b7c32e4e6b115cdb808a9479` |
| `research/m31-phase-attribution-2026-10-23/review/AUDIT-DESIGN.md` | source | 12709 | `f10b1ea21958b689dd12685ee02083cf0af133d1e56342b2f02a8b79460970d4` |
| `research/m31-phase-attribution-2026-10-23/review/PROTOCOL-REVIEW.md` | source | 15322 | `d0ffa2ae577dfd512d345971dcc1a0847abe417f3aef6f3b6dde70d0c4af91fb` |
| `research/m31-phase-attribution-2026-10-23/runtime.json` | source | 760 | `4d8d7e591084f681559a694a11a41f858d4b4392c32fc7a0839c54dba40705c4` |
| `research/m31-phase-attribution-2026-10-23/source/analyze.py` | source | 7977 | `13527d4dce9688d2a030fa0791b42bbaaa8458699d02548b2cf219b1958b481f` |
| `research/m31-phase-attribution-2026-10-23/source/audit.py` | source | 38330 | `ff4b7c1d852395c9c771c573f96b7cbc67b2d383f2ceb54c9f8bed23e16013f7` |
| `research/m31-phase-attribution-2026-10-23/source/common.py` | source | 4258 | `54da09f029d5c62f4a9fd042adc42f5372ccb9164c6a7ee1bf771ebf1af643ed` |
| `research/m31-phase-attribution-2026-10-23/source/finalize.py` | source | 1563 | `34bb732308060791d1946d066019fce56ae99e4e09b89233c0e9ec3a70057273` |
| `research/m31-phase-attribution-2026-10-23/source/launch.py` | source | 896 | `e7c432425102a92602648e419ed424a546b3d10c843d02f1405b90af5414c6a0` |
| `research/m31-phase-attribution-2026-10-23/source/supervise.py` | source | 3067 | `7f4584bdb2b11da905ecb8d5c270edbeb3b648eb5c9efd03a173f62bb34cf5de` |
| `research/m31-phase-attribution-2026-10-23/source/ui.cjs` | source | 12210 | `c80280ac0e37600d6fc4f0aef9f8b4404ba2fb152dc178926685bd564a08ed0f` |
| `research/m31-phase-attribution-2026-10-23/viewer/app.js` | source | 9694 | `85a6a87e1a5e57ba07ff172017885ba4c5c04386159687687477388a677d58ed` |
| `research/m31-phase-attribution-2026-10-23/viewer/index.html` | source | 4853 | `113606cc8698081dc9d3d01f75cf139f19e55ab9e1b3fbdd47c85717cdc91591` |
| `research/m31-radial-integration-2026-10-23/ALLOCATION-CLOSURE.json` | input | 1649 | `7971c6356755efe398cf2c111d2350c8ab59c572cbd89106c6e6162d0fa6f94b` |
| `research/m31-radial-integration-2026-10-23/LITERATURE.md` | input | 2095 | `81eaf547215f93e2c94e16f29b7cff5c0910ff17d2f08977a5389ba2d60fa364` |
| `research/m31-radial-integration-2026-10-23/RESULT-CLAIMS.md` | input | 3286 | `2a8f7e5fec5cd796ef1b0eaf212463174621fb04bac1c410ef0a87640dfe12b8` |
| `research/m31-radial-integration-2026-10-23/SUMMARY.md` | input | 4123 | `d5a4f9a06e959059d269625a1086b8d414a3a6ccc12f81c2d357e6827e6c8997` |
| `research/m31-radial-integration-2026-10-23/audit-supervisor.json` | input | 219 | `06167b312205359920357bdbe721c6207f118b14247ee88da0cf5bb9baed2892` |
| `research/m31-radial-integration-2026-10-23/audit/audit.json` | input | 3378809 | `59ab04097ac11731e3f978b164c32f3db863a1a3be218e5e55fbb80ddff28017` |
| `research/m31-radial-integration-2026-10-23/audit/exit.json` | input | 57 | `bd80502ee0fb3715f722ac1c4318e8581125cc17061d4e27b8d531d74fb41854` |
| `research/m31-radial-integration-2026-10-23/finalize-supervisor.json` | input | 218 | `48b34afce1ac231416e450a39c13ddf66d7152f4c57b544ea43e7bd047e26dcc` |
| `research/m31-radial-integration-2026-10-23/producer-supervisor.json` | input | 227 | `8b2a8db1e61d05265c0cccf9af8662b19fe2e4af54a370b4c022ccef3a6456e7` |
| `research/m31-radial-integration-2026-10-23/result-manifest.json` | input | 537067 | `7b0871190878f7d034677beb0f23b9f995871dbdda3fdee0935cf80cb8bc2b34` |
| `research/m31-radial-integration-2026-10-23/results/exit.json` | input | 112 | `07d80be868c3191a6717bad97e20011873ba8e595c04cdba3472fab1d23fb960` |
| `research/m31-radial-integration-2026-10-23/results/groups.jsonl` | input | 46447 | `42da5ad44e2548d7f2b9f9a7c3bed3a6855f8ff8db803893437389c6e477caee` |
| `research/m31-radial-integration-2026-10-23/results/queries.jsonl` | input | 80821976 | `6bef92fdf32ec06aae01ebcb4e0bbdd3cd6a0f72e26ead46c95b782acbe9df73` |
| `research/m31-radial-integration-2026-10-23/results/summary.json` | input | 1178 | `33f5133576cbf775292f1c28e87c2d73f8dbb0810c0fd2991a43e4138d5186f8` |
| `research/m31-radial-integration-2026-10-23/review/RESULT-REVIEW.md` | input | 15673 | `7c7cc8b59b05109134a921928049d74fed1c05549ccb1d422f5d29cf97638d32` |
| `research/m31-radial-integration-2026-10-23/source-manifest.json` | input | 20900 | `03086d126ff14783fa228b127843759505e3ccc6de80bcad269330608e976683` |
| `research/m31-radial-integration-2026-10-23/source-publication.json` | input | 855 | `765ca0a6472b4f142fa3da45b9c23a539669bec8950b5418863b92c17ec0b12e` |
| `research/m31-radial-integration-2026-10-23/source/candidate-cache.cjs` | input | 6909 | `b4e4a63d359e1e326edf834501ffb4db3780db62c1c1c9fc4a1a708933a0b146` |
| `research/m31-radial-integration-2026-10-23/source/candidate-kernel.cjs` | input | 17265 | `4fea99f4e61bff3c5eb54a0090e50b48e41d4cdf7cff5cdc770a37366f321b19` |
| `research/m31-radial-integration-2026-10-23/source/candidate.cjs` | input | 16381 | `2e11acb60ad7ab447bc137e6ade56c24ef2b383444db7d46643648bd83cd807b` |
| `research/m31-radial-integration-2026-10-23/source/run.cjs` | input | 8361 | `92f92f3b699f209000e9456bca77e9517f2f0aa5db4519c11c61f3ffc7ce6622` |
| `research/m31-radial-integration-2026-10-23/ui-supervisor.json` | input | 224 | `3ca237caaf440bc7c9f0fcbf8dc6afffd68607c3f4db6ff221eaa24794d110f0` |
| `research/publication-receipts/m31-radial-integration-result-2026-10-23.json` | input | 11808 | `e1ea07eb2ac6211ca09787c88f5ff4c68bac99681de5ae7b2697df522822077e` |
| `research/publication-receipts/m31-radial-integration-result-public-review-2026-10-23.json` | input | 1738739 | `a5a59a1efa77e82b1b3096929fdbcc872068592b7d79e7056be7916d1e309209` |
