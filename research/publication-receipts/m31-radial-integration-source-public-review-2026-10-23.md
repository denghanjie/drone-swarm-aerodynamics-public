# Independent public source verification — radial integration

Passed on 2026-10-23T01:23:32.074725+00:00. All four prospective allocations were unstarted at both checks.

- Source commit: `b68ab63f598755e8801b2be55ce5cdef101dd821`.
- Manifest: `research/m31-radial-integration-2026-10-23/source-manifest.json`; 20,900 bytes; SHA-256 `03086d126ff14783fa228b127843759505e3ccc6de80bcad269330608e976683`.
- All 79 pins plus manifest match local bytes and source-commit Git blobs.
- All 50 input pins also match their declared origin-commit Git blobs.
- Fresh HTTPS: 80 exact reads (manifest, 29 source files, 50 inputs), 224,542,223 bytes. All six selected-archive transport parts were fully downloaded and checked. No input public proof was reused.
- 290 successful identity operations; 0 failed attempts, preserved individually in the JSON receipt.

Public input reads use each manifest descriptor’s originCommit; source files and manifest use the source commit. HTTPS-only transfers required status 200, exact length and SHA-256, with at most three attempts and a 45-second transfer timeout per attempt. At most four public transfers ran concurrently. Each transfer was capped at its pinned file size.

The archive parts and other scientific evidence were opaque bytes. No archive decompression, source/module import, native query, diagnostic, numerical audit, reaggregation or browser/UI allocation ran. This receipt establishes publication identity and an unstarted gate, not scientific validity or universal runtime equivalence.

## Coverage inventory

| Kind | Public commit | Repository path | Bytes | SHA-256 |
| --- | --- | --- | ---: | --- |
| source | `b68ab63f598755e8801b2be55ce5cdef101dd821` | `outputs/step02b-source/vendor/OrbitControls.js` | 38703 | `b97879c748170baadeb3fb84cea1ffdf4674e283dc06042f34e2acb95a76042c` |
| source | `b68ab63f598755e8801b2be55ce5cdef101dd821` | `outputs/step02b-source/vendor/three.core.js` | 1403455 | `eb077d2417f61d3e6d9264c317cabc4ea35769ed6b0ab533067292a550784c20` |
| source | `b68ab63f598755e8801b2be55ce5cdef101dd821` | `outputs/step02b-source/vendor/three.module.js` | 603113 | `c8211c69345d2e9949dc7a8ac969380497aa0600a5a8ac6a459c8cd02dd9cb8a` |
| input | `0461153a7d6f75cb6e8564850b77e8b6f04cebb2` | `research/m31-buffered-candidates-2026-10-20/LITERATURE.md` | 4331 | `9a514f8e340a5d4146c08d21603c4ef1a29c512e5b44dae78496309a9db52076` |
| input | `0461153a7d6f75cb6e8564850b77e8b6f04cebb2` | `research/m31-buffered-candidates-2026-10-20/source/candidate-cache.cjs` | 6457 | `9b38064690c2ae5b505cae936d574e3355bcc613b3f69fda8b89ed50732f96ad` |
| input | `0461153a7d6f75cb6e8564850b77e8b6f04cebb2` | `research/m31-buffered-candidates-2026-10-20/source/candidate-kernel.cjs` | 17265 | `4fea99f4e61bff3c5eb54a0090e50b48e41d4cdf7cff5cdc770a37366f321b19` |
| input | `0461153a7d6f75cb6e8564850b77e8b6f04cebb2` | `research/m31-buffered-candidates-2026-10-20/source/candidate.cjs` | 16381 | `2e11acb60ad7ab447bc137e6ade56c24ef2b383444db7d46643648bd83cd807b` |
| input | `0461153a7d6f75cb6e8564850b77e8b6f04cebb2` | `research/m31-buffered-motion-2026-10-22/ALLOCATION-CLOSURE.json` | 1870 | `a5f38347cb14b7a590120ae2cdc325cfe2f879ae5413a299a886f6a2e9247c52` |
| input | `0461153a7d6f75cb6e8564850b77e8b6f04cebb2` | `research/m31-buffered-motion-2026-10-22/PROTOCOL.md` | 8164 | `5faff49bca309d4db1e26923130b2eac46f670b3865685edf760bf7a8b472918` |
| input | `0461153a7d6f75cb6e8564850b77e8b6f04cebb2` | `research/m31-buffered-motion-2026-10-22/audit-supervisor.json` | 220 | `9d8843d7aa587b2c1618e2e651caf51fa2994b9c3a43cca280c8821dfa2a16bb` |
| input | `0461153a7d6f75cb6e8564850b77e8b6f04cebb2` | `research/m31-buffered-motion-2026-10-22/audit/audit.json` | 457439 | `ef6e8876a3b102ceea2f5e6cdefc2d6d07fe0c65d64846320df22f8fafb26ab2` |
| input | `0461153a7d6f75cb6e8564850b77e8b6f04cebb2` | `research/m31-buffered-motion-2026-10-22/audit/exit.json` | 57 | `6c7aa6223a83cdf98490e16e9143942f7394a4102f178e9323799bcf28e71e85` |
| input | `0461153a7d6f75cb6e8564850b77e8b6f04cebb2` | `research/m31-buffered-motion-2026-10-22/config.json` | 1257 | `08e792b0b7a28413f61a09d4ad5be700f918807c4e9b328396059daead195f3a` |
| input | `0461153a7d6f75cb6e8564850b77e8b6f04cebb2` | `research/m31-buffered-motion-2026-10-22/extract-supervisor.json` | 222 | `86ef8f194cbad2c7bc48629f0aede3b1900b19965cd78254075231fb39285b16` |
| input | `0461153a7d6f75cb6e8564850b77e8b6f04cebb2` | `research/m31-buffered-motion-2026-10-22/extract/exit.json` | 73 | `ca62f6abd2af4cd5967bf08f0e8978e3366fb7d4f5afdf8341763a9d0c6ce3bb` |
| input | `0461153a7d6f75cb6e8564850b77e8b6f04cebb2` | `research/m31-buffered-motion-2026-10-22/extract/index.json` | 18790 | `c7c144f40a0f4fb807e6f045becdc622ae7e643bcf154c01ecd3904544b68cac` |
| input | `0461153a7d6f75cb6e8564850b77e8b6f04cebb2` | `research/m31-buffered-motion-2026-10-22/producer-supervisor.json` | 222 | `30673a820eb2a6b9c3aa894a4f4446e3b100c7ce3079ba2c7806b52609a08217` |
| input | `0461153a7d6f75cb6e8564850b77e8b6f04cebb2` | `research/m31-buffered-motion-2026-10-22/result-manifest.json` | 545123 | `440d2ac225f1587359cfa96af5d27b9a9b37d962ce25d75701c4fc195d753025` |
| input | `0461153a7d6f75cb6e8564850b77e8b6f04cebb2` | `research/m31-buffered-motion-2026-10-22/results/summary.json` | 1046 | `7b2838198ec5529ec536ea0ace474535fa97f5ba52dd7d50ff5460ea304dbfa2` |
| input | `0461153a7d6f75cb6e8564850b77e8b6f04cebb2` | `research/m31-buffered-motion-2026-10-22/review/RESULT-REVIEW.md` | 12906 | `f59f9c54192634673d2b62aa5337ced6a17ce3f2dd245e424c2320f00e67e6ed` |
| input | `0461153a7d6f75cb6e8564850b77e8b6f04cebb2` | `research/m31-buffered-motion-2026-10-22/transport/index.json` | 1099 | `15da8e04cbed8cf2ceb6a214dead7f4c5b01b62896b0121e6a4ea2ae3ee367d7` |
| input | `0461153a7d6f75cb6e8564850b77e8b6f04cebb2` | `research/m31-buffered-motion-2026-10-22/transport/selected.jsonl.gz.part000` | 33554432 | `079b27f80012b61a5b7da88d23604c617b290cc60c98b73c62d3f00cf2b75793` |
| input | `0461153a7d6f75cb6e8564850b77e8b6f04cebb2` | `research/m31-buffered-motion-2026-10-22/transport/selected.jsonl.gz.part001` | 33554432 | `32dc050281d8822ddb5b94710b68fac5fb7ad70eeab13a24bdb369038164ce81` |
| input | `0461153a7d6f75cb6e8564850b77e8b6f04cebb2` | `research/m31-buffered-motion-2026-10-22/transport/selected.jsonl.gz.part002` | 33554432 | `b4ca4865ac09c54597ede4d608841d445a5ea7164799614978b5c1777627b268` |
| input | `0461153a7d6f75cb6e8564850b77e8b6f04cebb2` | `research/m31-buffered-motion-2026-10-22/transport/selected.jsonl.gz.part003` | 33554432 | `e44877bab0936c31aab556a39a0151855ec316d13ce6c233db9ceae5ec9fdc86` |
| input | `0461153a7d6f75cb6e8564850b77e8b6f04cebb2` | `research/m31-buffered-motion-2026-10-22/transport/selected.jsonl.gz.part004` | 33554432 | `36cbf56cc311de3a453254c0637cd213d047a47dafe5a8c0f01d6a35685838f4` |
| input | `0461153a7d6f75cb6e8564850b77e8b6f04cebb2` | `research/m31-buffered-motion-2026-10-22/transport/selected.jsonl.gz.part005` | 27090335 | `0039ca2e5736e067d4d68040f56cbd6b4413a6c393c1d3973d6ce5def656da4f` |
| input | `0461153a7d6f75cb6e8564850b77e8b6f04cebb2` | `research/m31-native-fresh-transfer-2026-10-17/source/native-load.cjs` | 16262 | `b4699a8025e27dcd34e9a206e0330a2c08d7caa61e934ec203d142876e1430f1` |
| input | `0461153a7d6f75cb6e8564850b77e8b6f04cebb2` | `research/m31-native-fresh-transfer-2026-10-17/source/vendor/anchor-kernel.cjs` | 11828 | `c2ab29e4f53341706582d52149df96cd93323d3943ac145f288fbbae4de71a8a` |
| input | `0461153a7d6f75cb6e8564850b77e8b6f04cebb2` | `research/m31-native-fresh-transfer-2026-10-17/source/vendor/kernel.cjs` | 16676 | `efc87f4c0f9d1a5a9b754d9d334ce295227a0cb01ce6980e4818313dd35d3bc8` |
| input | `0461153a7d6f75cb6e8564850b77e8b6f04cebb2` | `research/m31-native-fresh-transfer-2026-10-17/source/vendor/lean-anchor.cjs` | 14840 | `1b57d90d1ce1a45fe3e7f637cae57325861bfc37c907de4d4c6f9e1a79f1af96` |
| input | `0461153a7d6f75cb6e8564850b77e8b6f04cebb2` | `research/m31-native-fresh-transfer-2026-10-17/source/vendor/reference-excerpt.cjs` | 2731 | `ec71562d17db5b30497e2953adc75019c424c19a44e45b22fcbb3a4482096d1e` |
| input | `a38234d150bcdecb50e3c4615e07dc8703039397` | `research/m31-neighbor-density-2026-10-23/results/stages.jsonl` | 9063908 | `8098f5d2478b9a7f7184ed34f5df41199b565f969e9691ad9099ee6f3e48c1c3` |
| input | `a38234d150bcdecb50e3c4615e07dc8703039397` | `research/m31-neighbor-density-2026-10-23/results/summary.json` | 16311 | `f786d6424102ce501e021531dadb94d9a66938870572045362dc85a290c06644` |
| input | `afddaf6b191cc577cf82ad4fa43e1bbd77a9d43d` | `research/m31-radial-certificate-2026-10-23/ALLOCATION-CLOSURE.json` | 1908 | `a08ec06ff49e7ce717d321372496f5038e8fb7c40558d017346a3d0174b53f2a` |
| input | `afddaf6b191cc577cf82ad4fa43e1bbd77a9d43d` | `research/m31-radial-certificate-2026-10-23/LITERATURE.md` | 7429 | `144ee6e8b0f8d3871280381321b67fdf6065bac875e41fdea1465761498d5c85` |
| input | `afddaf6b191cc577cf82ad4fa43e1bbd77a9d43d` | `research/m31-radial-certificate-2026-10-23/RESEARCH-ACQUISITION.md` | 5767 | `042b32c71a318631dce699c03800d5f0e072fce2a6ccef2b7a9bbaea99ab59c5` |
| input | `afddaf6b191cc577cf82ad4fa43e1bbd77a9d43d` | `research/m31-radial-certificate-2026-10-23/audit-supervisor.json` | 218 | `221f527bda016802f974827280f5234a42d859a5020b60c4a25f1a0387d8495d` |
| input | `afddaf6b191cc577cf82ad4fa43e1bbd77a9d43d` | `research/m31-radial-certificate-2026-10-23/audit/audit.json` | 374934 | `0e085738758087baa96aa827f3cab97bc5072a75eb539b76fb150edf2b02abf4` |
| input | `afddaf6b191cc577cf82ad4fa43e1bbd77a9d43d` | `research/m31-radial-certificate-2026-10-23/audit/exit.json` | 71 | `0dc630e8ba58c0ab4462758601182663e0c5207953356d1cae56daa2d6a04165` |
| input | `afddaf6b191cc577cf82ad4fa43e1bbd77a9d43d` | `research/m31-radial-certificate-2026-10-23/producer-supervisor.json` | 219 | `e4ec61dbdc1e5621fd9657fdf028e4fb61c89cb8771b78d18101d7b5c765147d` |
| input | `afddaf6b191cc577cf82ad4fa43e1bbd77a9d43d` | `research/m31-radial-certificate-2026-10-23/result-manifest.json` | 23297 | `c3825a3e6886ecdff8ebfa521484f6b21704091966bbd82271d9225b70566514` |
| input | `afddaf6b191cc577cf82ad4fa43e1bbd77a9d43d` | `research/m31-radial-certificate-2026-10-23/results/classes.bin` | 7741440 | `9015cf8f843f2aa5d7bd1afd869840e31df6ff1d23b197f96cc03c101fb2f755` |
| input | `afddaf6b191cc577cf82ad4fa43e1bbd77a9d43d` | `research/m31-radial-certificate-2026-10-23/results/omitted.bin` | 7741440 | `73fcb247e763fc5ec45c24bf146814f8a5ce3233de157caf8783318a7189e765` |
| input | `afddaf6b191cc577cf82ad4fa43e1bbd77a9d43d` | `research/m31-radial-certificate-2026-10-23/results/stages.jsonl` | 778310 | `506e6fb0b8a805e0e20fcddea46f7c9725150132cabbaca1068446fdb889e2ee` |
| input | `afddaf6b191cc577cf82ad4fa43e1bbd77a9d43d` | `research/m31-radial-certificate-2026-10-23/results/summary.json` | 647 | `c68db400b4ef05867b690fea0d8b6cdb6433e8bcb439857f53f8d472ada3369f` |
| input | `afddaf6b191cc577cf82ad4fa43e1bbd77a9d43d` | `research/m31-radial-certificate-2026-10-23/results/witnesses.jsonl` | 236864 | `de2c59bc50ef8d05f68e123e906b63000acad25b19268efc9d1efe410d709604` |
| input | `afddaf6b191cc577cf82ad4fa43e1bbd77a9d43d` | `research/m31-radial-certificate-2026-10-23/review/CONDITIONAL-LEMMA.md` | 9989 | `941d6b231e0f6cd5fef3c0968847c888828c278af2c22076860a61a025db2ea1` |
| input | `afddaf6b191cc577cf82ad4fa43e1bbd77a9d43d` | `research/m31-radial-certificate-2026-10-23/review/RESULT-REVIEW.md` | 17020 | `67214deed136ee4ed03476e912602331c5784e9165a630aa1adfd7d85d9b0ac7` |
| source | `b68ab63f598755e8801b2be55ce5cdef101dd821` | `research/m31-radial-integration-2026-10-23/CLAIMS.md` | 1505 | `e5a64fc7c236b984ed3294568ef2a03c240c016915695432bd2d5f6675588fdd` |
| source | `b68ab63f598755e8801b2be55ce5cdef101dd821` | `research/m31-radial-integration-2026-10-23/LITERATURE.md` | 2095 | `81eaf547215f93e2c94e16f29b7cff5c0910ff17d2f08977a5389ba2d60fa364` |
| source | `b68ab63f598755e8801b2be55ce5cdef101dd821` | `research/m31-radial-integration-2026-10-23/PRIVACY-SOURCE.json` | 265 | `26535e275dea175561ee74fe62a6a9b863a016f8381b3f8a33a6f57f509a7229` |
| source | `b68ab63f598755e8801b2be55ce5cdef101dd821` | `research/m31-radial-integration-2026-10-23/PRIVACY.md` | 822 | `bfdf0472d1e7f7dffe86b95abefcf973dcbe7096f788829dbfd571632bc472cd` |
| source | `b68ab63f598755e8801b2be55ce5cdef101dd821` | `research/m31-radial-integration-2026-10-23/PROTOCOL.md` | 7097 | `ff1396b8c056140a75d275252fb2e181382b27bcbb021b00ff40f713ee8a022b` |
| source | `b68ab63f598755e8801b2be55ce5cdef101dd821` | `research/m31-radial-integration-2026-10-23/RESTART.md` | 1188 | `fd93458cb4809b400750496a11b1736fb3a554a0d28fc941245a8e9df23729e6` |
| source | `b68ab63f598755e8801b2be55ce5cdef101dd821` | `research/m31-radial-integration-2026-10-23/SCHEMA.md` | 6355 | `d96c953fbc2ab793cc7e05b6498791587ffda87429ec56ccb0d22eb5190d5e27` |
| source | `b68ab63f598755e8801b2be55ce5cdef101dd821` | `research/m31-radial-integration-2026-10-23/SOURCE-CHANGES.md` | 2402 | `04de28fb29def520bb436e8ace689c4d76fd4a27fcac9d48aed11db58487e717` |
| source | `b68ab63f598755e8801b2be55ce5cdef101dd821` | `research/m31-radial-integration-2026-10-23/config.json` | 1833 | `fac7c77a199514db6521864ea8eff718ed58a160587ac78f67223e9aff349da2` |
| source | `b68ab63f598755e8801b2be55ce5cdef101dd821` | `research/m31-radial-integration-2026-10-23/input-pins.json` | 14566 | `b126e19c660b9f171a0ccbd0789391ae8fbc45abb44f6dcc406c7f6ff2f48cb0` |
| source | `b68ab63f598755e8801b2be55ce5cdef101dd821` | `research/m31-radial-integration-2026-10-23/review/AUDIT-DESIGN.md` | 16480 | `0225575a0683cf19e3c63780e58496795395887809eb64e0d71a5a0f7e6ce020` |
| source | `b68ab63f598755e8801b2be55ce5cdef101dd821` | `research/m31-radial-integration-2026-10-23/review/PROTOCOL-REVIEW.md` | 15071 | `220db404a4d88cf235f9ffd52866220f04e37349f57864538a58885c126c702d` |
| source | `b68ab63f598755e8801b2be55ce5cdef101dd821` | `research/m31-radial-integration-2026-10-23/runtime.json` | 855 | `66de2ba49b9465c74de0a3a9da4a9aca19f30005cdccd78d3307f5ea41b3d035` |
| source | `b68ab63f598755e8801b2be55ce5cdef101dd821` | `research/m31-radial-integration-2026-10-23/source/audit.py` | 69713 | `a349b5e5a9c640fc8c5d6111377f47d2801e07f95e6a88039bc54a13fb36f56a` |
| source | `b68ab63f598755e8801b2be55ce5cdef101dd821` | `research/m31-radial-integration-2026-10-23/source/candidate-cache.cjs` | 6909 | `b4e4a63d359e1e326edf834501ffb4db3780db62c1c1c9fc4a1a708933a0b146` |
| source | `b68ab63f598755e8801b2be55ce5cdef101dd821` | `research/m31-radial-integration-2026-10-23/source/candidate-kernel.cjs` | 17265 | `4fea99f4e61bff3c5eb54a0090e50b48e41d4cdf7cff5cdc770a37366f321b19` |
| source | `b68ab63f598755e8801b2be55ce5cdef101dd821` | `research/m31-radial-integration-2026-10-23/source/candidate.cjs` | 16381 | `2e11acb60ad7ab447bc137e6ade56c24ef2b383444db7d46643648bd83cd807b` |
| source | `b68ab63f598755e8801b2be55ce5cdef101dd821` | `research/m31-radial-integration-2026-10-23/source/common.cjs` | 2413 | `1b0dd668be9065422b7d852347ac3f8c7bb07ca0686c3ab3c7a9f5070e221019` |
| source | `b68ab63f598755e8801b2be55ce5cdef101dd821` | `research/m31-radial-integration-2026-10-23/source/common.py` | 4258 | `54da09f029d5c62f4a9fd042adc42f5372ccb9164c6a7ee1bf771ebf1af643ed` |
| source | `b68ab63f598755e8801b2be55ce5cdef101dd821` | `research/m31-radial-integration-2026-10-23/source/finalize.py` | 1563 | `34bb732308060791d1946d066019fce56ae99e4e09b89233c0e9ec3a70057273` |
| source | `b68ab63f598755e8801b2be55ce5cdef101dd821` | `research/m31-radial-integration-2026-10-23/source/launch.py` | 888 | `394a1447fb3e571e19110e31d8ddb59806eeab80d836b2b53e780472fc9a41ce` |
| source | `b68ab63f598755e8801b2be55ce5cdef101dd821` | `research/m31-radial-integration-2026-10-23/source/run.cjs` | 8361 | `92f92f3b699f209000e9456bca77e9517f2f0aa5db4519c11c61f3ffc7ce6622` |
| source | `b68ab63f598755e8801b2be55ce5cdef101dd821` | `research/m31-radial-integration-2026-10-23/source/supervise.py` | 3072 | `99fe23d838f894018a924566716c61ba6c41c2aa08c54392e1119474f93f1190` |
| source | `b68ab63f598755e8801b2be55ce5cdef101dd821` | `research/m31-radial-integration-2026-10-23/source/ui.cjs` | 10274 | `9c049078dd5f672ac5cdc73824b037ecbed1ad66ed4d2ca9472d92a3da5d75a5` |
| source | `b68ab63f598755e8801b2be55ce5cdef101dd821` | `research/m31-radial-integration-2026-10-23/viewer/app.js` | 8202 | `1829c19fb04092bdb7140f00f9a13b6da151dbaf6745b6ff3840fd965f6ab137` |
| source | `b68ab63f598755e8801b2be55ce5cdef101dd821` | `research/m31-radial-integration-2026-10-23/viewer/index.html` | 5322 | `cd1e06feefc67ecbb537aac801b5df37d2d7321d8630e5cc166f4f17a7319d98` |
| input | `88832eb2a95dba88d1a077e8d814f6174f0725d7` | `research/publication-receipts/m31-buffered-motion-result-2026-10-22.json` | 3090 | `c026b172b3b237280d50097692bae595f372f1b284fecce0082a445ab2fe8c25` |
| input | `88832eb2a95dba88d1a077e8d814f6174f0725d7` | `research/publication-receipts/m31-radial-certificate-result-2026-10-23.json` | 3730 | `48a91e2190c9ea49ceb7f313fc99072c28b23edd40bd49491a13eaa16628b00d` |
| input | `88832eb2a95dba88d1a077e8d814f6174f0725d7` | `research/publication-receipts/m31-radial-certificate-result-public-review-2026-10-23.json` | 186241 | `4cd3312c6d5798762a4b55368680867f46f65f0856d870a43a3390b6e96011dc` |
| input | `88832eb2a95dba88d1a077e8d814f6174f0725d7` | `research/publication-receipts/m31-radial-certificate-result-public-review-2026-10-23.md` | 20310 | `21d43fb03c180f93cbee27e5d336dd3215eed83b1495a94d8187c3d524995999` |
