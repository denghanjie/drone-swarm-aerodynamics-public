# Independent public verification — display recovery source and evidence

Passed on 2026-10-23T01:00:29.528580+00:00. Recovery remained unstarted throughout this identity acquisition.

- Recovery commit: `f3101031a85b09e080214ebe4b838495d7017e83`.
- Manifest: `research/m31-radial-certificate-2026-10-23/display-recovery-manifest.json`; 18603 bytes; SHA-256 `c1721dd434aa3c6d0c461e9c3169fa0f15759bde4d3e893dcbf41ff909a8ee9e`.
- All 82 file pins plus the manifest freshly match local bytes and recovery-commit Git blobs.
- Fresh HTTPS reads: 68 (manifest plus all 67 non-input files), 81,188,846 bytes. This includes the complete 61,931,520-byte `results/norms.bin`, classes/omissions, successful audit/finalizer records, original failed UI evidence and recovery source.
- The 15 unchanged input public/origin-Git verifications were explicitly reused from `research/publication-receipts/m31-radial-certificate-source-public-review-2026-10-23.json` (79,183 bytes; SHA-256 `aefa55537cc43d03cbc70eb8defffba4d0aa44bd9ff5a26f67c3e1b4a374285c`). Every input descriptor and origin matches that receipt, and all inputs were freshly checked locally and in the recovery commit.
- 235 fresh successful identity operations plus 15 explicit reuse validations; 0 failed attempts.

Each fresh HTTPS transfer required status 200, permitted at most three attempts, and was bounded to 45 seconds and the pinned file size. The JSON receipt records every operation and the precise prior events reused for inputs. The earlier receipt itself is also freshly downloaded and hash-checked as one of this recovery manifest’s non-input pins.

Source files and raw numerical evidence were treated as opaque bytes. No diagnostic, control, audit, model, browser, norm, certificate, saved-state reaggregation or archive decompression ran. The original UI failure remains unchanged. This receipt establishes publication identity, not numerical validity or a runtime-general theorem.

## Coverage inventory

| Public coverage | Path | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| Fresh recovery-commit read | `outputs/step02b-source/vendor/OrbitControls.js` | 38703 | `b97879c748170baadeb3fb84cea1ffdf4674e283dc06042f34e2acb95a76042c` |
| Fresh recovery-commit read | `outputs/step02b-source/vendor/three.core.js` | 1403455 | `eb077d2417f61d3e6d9264c317cabc4ea35769ed6b0ab533067292a550784c20` |
| Fresh recovery-commit read | `outputs/step02b-source/vendor/three.module.js` | 603113 | `c8211c69345d2e9949dc7a8ac969380497aa0600a5a8ac6a459c8cd02dd9cb8a` |
| Prior input receipt | `research/m31-native-fresh-transfer-2026-10-17/source/vendor/anchor-kernel.cjs` | 11828 | `c2ab29e4f53341706582d52149df96cd93323d3943ac145f288fbbae4de71a8a` |
| Prior input receipt | `research/m31-native-fresh-transfer-2026-10-17/source/vendor/kernel.cjs` | 16676 | `efc87f4c0f9d1a5a9b754d9d334ce295227a0cb01ce6980e4818313dd35d3bc8` |
| Prior input receipt | `research/m31-neighbor-density-2026-10-23/LITERATURE.md` | 7635 | `4f810c7f26682b74211b2b2deeddeaa7a3c8eef8d67a5afb1834953c11123881` |
| Prior input receipt | `research/m31-neighbor-density-2026-10-23/RESULT-CLAIMS.md` | 3734 | `1aca0c6edde293c20771f38a13afe4acb16e6bcc321cdb41842f9ed274e88bfe` |
| Prior input receipt | `research/m31-neighbor-density-2026-10-23/audit-supervisor.json` | 217 | `ef2984b8c51e33956e04e20b9204ff1f04c0db69823c8742e1f4dbb4a3d7f4d7` |
| Prior input receipt | `research/m31-neighbor-density-2026-10-23/audit/audit.json` | 27023 | `4c3b9dac6426d8e7c029795f3190a402f1e7ba9a21d3f9771b644e5f9a65b052` |
| Prior input receipt | `research/m31-neighbor-density-2026-10-23/audit/exit.json` | 77 | `19df4f54accc282b5c81fadada0a65780c9feacaec6b4ad0d6436476babec45e` |
| Prior input receipt | `research/m31-neighbor-density-2026-10-23/producer-supervisor.json` | 224 | `ac48660ef321c243e2a718e765823ecdf092b79d84ba2356b8599c37692ec9bf` |
| Prior input receipt | `research/m31-neighbor-density-2026-10-23/result-manifest.json` | 19976 | `acb61c176bcf87250a7658b2675d00fd8af4104a0504da5c1fb80bebdf56a5cb` |
| Prior input receipt | `research/m31-neighbor-density-2026-10-23/results/stages.jsonl` | 9063908 | `8098f5d2478b9a7f7184ed34f5df41199b565f969e9691ad9099ee6f3e48c1c3` |
| Prior input receipt | `research/m31-neighbor-density-2026-10-23/results/summary.json` | 16311 | `f786d6424102ce501e021531dadb94d9a66938870572045362dc85a290c06644` |
| Prior input receipt | `research/m31-neighbor-density-2026-10-23/review/RESULT-REVIEW.md` | 14411 | `f1cbc0b98907d66db4a2814ae694411e554520306174569529e350083a678fa7` |
| Fresh recovery-commit read | `research/m31-radial-certificate-2026-10-23/CLAIMS.md` | 2099 | `7b5b1cf78c11c2a5adf659f35b047b4eb00192f521c03f08ce00a9b51fb00d25` |
| Fresh recovery-commit read | `research/m31-radial-certificate-2026-10-23/DISPLAY-RECOVERY-PROTOCOL.md` | 2760 | `2f9d07b7421b4a241859cedfa3dec2c3cf0edbf6f98df91efb6fe8634280febf` |
| Fresh recovery-commit read | `research/m31-radial-certificate-2026-10-23/EXECUTION-PROTOCOL.md` | 6354 | `2fb330b0357f1c5fa8c1f4fee1794a4f85a1fc3c8283b38c66630ea841eb6d80` |
| Fresh recovery-commit read | `research/m31-radial-certificate-2026-10-23/LITERATURE.md` | 7429 | `144ee6e8b0f8d3871280381321b67fdf6065bac875e41fdea1465761498d5c85` |
| Fresh recovery-commit read | `research/m31-radial-certificate-2026-10-23/PARENT-ACQUISITION.json` | 922 | `1f825f1ba585d19dcd0977b36eb6d3788b5c89f7cd5d0da149092271a2993b21` |
| Fresh recovery-commit read | `research/m31-radial-certificate-2026-10-23/PRIVACY.md` | 947 | `b4734e92615e56cf07134cf6d7182cf32c178c39612458f7890de6dacd311e70` |
| Fresh recovery-commit read | `research/m31-radial-certificate-2026-10-23/PROOF-PLAN.md` | 2804 | `86947109564eed27ffc4ddf1c33c878633a9133acc26cfe0359e948848ad6bc8` |
| Fresh recovery-commit read | `research/m31-radial-certificate-2026-10-23/RESEARCH-ACQUISITION.md` | 5767 | `042b32c71a318631dce699c03800d5f0e072fce2a6ccef2b7a9bbaea99ab59c5` |
| Fresh recovery-commit read | `research/m31-radial-certificate-2026-10-23/RESTART.md` | 1273 | `82b0b563e0456d5550b130751c8f8f04284bba7ba6ba4770a9de94a506d24f50` |
| Fresh recovery-commit read | `research/m31-radial-certificate-2026-10-23/SCHEMA.md` | 6713 | `f9e7b0cfc06bd19e8dd2ea988af897ca3c6e8dd6713f70385a0ea255e9788b32` |
| Fresh recovery-commit read | `research/m31-radial-certificate-2026-10-23/audit-supervisor-launch.lock` | 23 | `582728fcc60fc12fd7abcdaf58c67141dc65f2e824a859e4ec0c68c6587f124e` |
| Fresh recovery-commit read | `research/m31-radial-certificate-2026-10-23/audit-supervisor.json` | 218 | `221f527bda016802f974827280f5234a42d859a5020b60c4a25f1a0387d8495d` |
| Fresh recovery-commit read | `research/m31-radial-certificate-2026-10-23/audit/audit.json` | 374934 | `0e085738758087baa96aa827f3cab97bc5072a75eb539b76fb150edf2b02abf4` |
| Fresh recovery-commit read | `research/m31-radial-certificate-2026-10-23/audit/exit.json` | 71 | `0dc630e8ba58c0ab4462758601182663e0c5207953356d1cae56daa2d6a04165` |
| Fresh recovery-commit read | `research/m31-radial-certificate-2026-10-23/audit/launch.json` | 149 | `59d8a837a67de1fcd06a0d9073b13fed3f53498173b1472552a2c60940f11901` |
| Fresh recovery-commit read | `research/m31-radial-certificate-2026-10-23/config.json` | 767 | `15c91f54c715ffb2eca2fb192ed78a7fb08fbfbd10a66847cbca54db2c5e786a` |
| Fresh recovery-commit read | `research/m31-radial-certificate-2026-10-23/finalize-supervisor-launch.lock` | 23 | `582728fcc60fc12fd7abcdaf58c67141dc65f2e824a859e4ec0c68c6587f124e` |
| Fresh recovery-commit read | `research/m31-radial-certificate-2026-10-23/finalize-supervisor.json` | 215 | `f399d66b83e49334ebbe5150706ed7c78305070d52fb1d42a7cfd68cd373c437` |
| Fresh recovery-commit read | `research/m31-radial-certificate-2026-10-23/finalize/exit.json` | 80 | `bf9fe7aeea6c8cdc1778443c001dbbf0cd5f86c3791859e8163182ab51c9aaa9` |
| Fresh recovery-commit read | `research/m31-radial-certificate-2026-10-23/finalize/launch.json` | 35 | `d6a3c710566bfb86df53bebfd525ecd9739127e450242708f0b1467a7ccfe9fd` |
| Fresh recovery-commit read | `research/m31-radial-certificate-2026-10-23/finalize/report.json` | 1052 | `6bab728f81002e4bda739b5de4c45bccca6282708095f0bb63a5e1ddd3ed1590` |
| Fresh recovery-commit read | `research/m31-radial-certificate-2026-10-23/input-pins.json` | 4377 | `4bede05495769f94b4ddcdf46ca977adc34c7256d2adc3c4c8974b66e957fba3` |
| Fresh recovery-commit read | `research/m31-radial-certificate-2026-10-23/node-release-SHASUMS256.txt` | 2967 | `be0629ee2bcd8e40bb856abdd3407f0762101b76bd60a36b8867f637733631c0` |
| Fresh recovery-commit read | `research/m31-radial-certificate-2026-10-23/producer-supervisor-launch.lock` | 23 | `582728fcc60fc12fd7abcdaf58c67141dc65f2e824a859e4ec0c68c6587f124e` |
| Fresh recovery-commit read | `research/m31-radial-certificate-2026-10-23/producer-supervisor.json` | 219 | `e4ec61dbdc1e5621fd9657fdf028e4fb61c89cb8771b78d18101d7b5c765147d` |
| Fresh recovery-commit read | `research/m31-radial-certificate-2026-10-23/results/classes.bin` | 7741440 | `9015cf8f843f2aa5d7bd1afd869840e31df6ff1d23b197f96cc03c101fb2f755` |
| Fresh recovery-commit read | `research/m31-radial-certificate-2026-10-23/results/controls-partial.jsonl` | 4378 | `2433c984b884a472775c256d4cae5d55dd5be39ec51a7120826ab306412f650d` |
| Fresh recovery-commit read | `research/m31-radial-certificate-2026-10-23/results/controls.json` | 4380 | `968dd518ed9cbcea3cc365b30c787a983199e2140f47e6125b6bcc5df142b82d` |
| Fresh recovery-commit read | `research/m31-radial-certificate-2026-10-23/results/exit.json` | 151 | `0a82e7caa7b132d1930693dd074a8993ea0531e11ea205bbb6198b67a68dc067` |
| Fresh recovery-commit read | `research/m31-radial-certificate-2026-10-23/results/input-binding.json` | 418 | `85c777f51a6eb2ad57efb0a760b2f090e95c243a1fe75e112826ae85e29de92e` |
| Fresh recovery-commit read | `research/m31-radial-certificate-2026-10-23/results/launch.json` | 35 | `a5751b9bbf42ca9f994a749ca9d34ca16f0163594faf647d2f6030b4f05510ea` |
| Fresh recovery-commit read | `research/m31-radial-certificate-2026-10-23/results/norms.bin` | 61931520 | `afa4a940b4839062753f8105718dce8e14eac26d2cacc6d0120606c37d68436f` |
| Fresh recovery-commit read | `research/m31-radial-certificate-2026-10-23/results/omitted.bin` | 7741440 | `73fcb247e763fc5ec45c24bf146814f8a5ce3233de157caf8783318a7189e765` |
| Fresh recovery-commit read | `research/m31-radial-certificate-2026-10-23/results/stages.jsonl` | 778310 | `506e6fb0b8a805e0e20fcddea46f7c9725150132cabbaca1068446fdb889e2ee` |
| Fresh recovery-commit read | `research/m31-radial-certificate-2026-10-23/results/summary.json` | 647 | `c68db400b4ef05867b690fea0d8b6cdb6433e8bcb439857f53f8d472ada3369f` |
| Fresh recovery-commit read | `research/m31-radial-certificate-2026-10-23/results/witnesses.jsonl` | 236864 | `de2c59bc50ef8d05f68e123e906b63000acad25b19268efc9d1efe410d709604` |
| Fresh recovery-commit read | `research/m31-radial-certificate-2026-10-23/review/AUDIT-DESIGN.md` | 12153 | `31fcd0a73a5d943cbe4ee32ef12c8c51fc243da282cce4cd3e1334bb575f18ff` |
| Fresh recovery-commit read | `research/m31-radial-certificate-2026-10-23/review/CONDITIONAL-LEMMA.md` | 9989 | `941d6b231e0f6cd5fef3c0968847c888828c278af2c22076860a61a025db2ea1` |
| Fresh recovery-commit read | `research/m31-radial-certificate-2026-10-23/review/DISPLAY-RECOVERY-REVIEW.md` | 8340 | `502dbdf69f25ce2121eb9a2bc7383e45b7f0629e6bc5c02d3ff3d5129b96d40e` |
| Fresh recovery-commit read | `research/m31-radial-certificate-2026-10-23/review/PREPARATION-OBSERVATION.md` | 1426 | `787468ad165691ec96ff9abbcee779e2dd40a1abbf3e22bcb7348757410a9d2c` |
| Fresh recovery-commit read | `research/m31-radial-certificate-2026-10-23/review/PROTOCOL-REVIEW.md` | 14858 | `0f96d75be72e3675e909590b08b8ab348f6c35ff7ed7df8c2bb3c4511a5429b6` |
| Fresh recovery-commit read | `research/m31-radial-certificate-2026-10-23/review/STATIC-CHALLENGE.md` | 10500 | `70a1fd76ed80d808a3cd177ac6d7fc3f897bcb7862a2458197baf37fb9c5c542` |
| Fresh recovery-commit read | `research/m31-radial-certificate-2026-10-23/runtime.json` | 851 | `29e4afc02aab80de03d61cbc9dad39f8289983b3c7372506cc2986d0b2e68aed` |
| Fresh recovery-commit read | `research/m31-radial-certificate-2026-10-23/source-manifest.json` | 11192 | `2e7b6e06d675d29a1b20a7a5f20dd88753ef207a574c194a1407609a12f1bb76` |
| Fresh recovery-commit read | `research/m31-radial-certificate-2026-10-23/source-publication.json` | 850 | `491cb973f2396bc7def9de955bc97ada75f3d331c0a7e59b4179d00266f7a276` |
| Fresh recovery-commit read | `research/m31-radial-certificate-2026-10-23/source/audit.py` | 45976 | `4f1b83d760be6ecaef9189902d3bf3ac83a6c53e3372c16cb63379a7410d43cc` |
| Fresh recovery-commit read | `research/m31-radial-certificate-2026-10-23/source/candidate.cjs` | 1938 | `cd5aa426d4ed45dc169fe6cd1047555db989744f4c80b4204ea602ccc7dfaee7` |
| Fresh recovery-commit read | `research/m31-radial-certificate-2026-10-23/source/common.py` | 4258 | `54da09f029d5c62f4a9fd042adc42f5372ccb9164c6a7ee1bf771ebf1af643ed` |
| Fresh recovery-commit read | `research/m31-radial-certificate-2026-10-23/source/diagnose.cjs` | 8461 | `01537a1cdc3b81835b44a52c8258c307f2bac40636d1f509e4890da0e68eef50` |
| Fresh recovery-commit read | `research/m31-radial-certificate-2026-10-23/source/finalize.py` | 1516 | `499aaa0919be50002645a245eac714ef48bc84bbe08064b73d8c19c96407a6f9` |
| Fresh recovery-commit read | `research/m31-radial-certificate-2026-10-23/source/launch.py` | 893 | `e8bb9bee0edf1fa372275864228d345594b032b0667dade0167d4f0edb19ef43` |
| Fresh recovery-commit read | `research/m31-radial-certificate-2026-10-23/source/supervise-ui-recovery.py` | 4215 | `d34e0dec2d1b3f1a1475401675c82d23cc4b9be15fe0b4f82c55f48030b2f271` |
| Fresh recovery-commit read | `research/m31-radial-certificate-2026-10-23/source/supervise.py` | 3077 | `276627f0badc2f18e7ca1e5fc37ebdb46d111a6f55985b0baceee13fea98af59` |
| Fresh recovery-commit read | `research/m31-radial-certificate-2026-10-23/source/ui-recovery.cjs` | 10202 | `0616ee480da93f1c67ddad33ff4be723280278d86409197feb15885d2c715fee` |
| Fresh recovery-commit read | `research/m31-radial-certificate-2026-10-23/source/ui.cjs` | 9102 | `a8a431116a1b6fe44e908664e7fecb6ba95b470c148b2c16013fb91da412a9a7` |
| Fresh recovery-commit read | `research/m31-radial-certificate-2026-10-23/ui-supervisor-launch.lock` | 23 | `582728fcc60fc12fd7abcdaf58c67141dc65f2e824a859e4ec0c68c6587f124e` |
| Fresh recovery-commit read | `research/m31-radial-certificate-2026-10-23/ui-supervisor.json` | 210 | `fe24597418c6d659d482736a31f17c63d8e5d0685f81f4f97978036887d40592` |
| Fresh recovery-commit read | `research/m31-radial-certificate-2026-10-23/ui/launch.lock` | 29 | `d9c0d0e4584a948ac9fa9f68d3180488fbcbb741e18fc188af9031d8c4d674a8` |
| Fresh recovery-commit read | `research/m31-radial-certificate-2026-10-23/ui/qa.json` | 552 | `c5075140eb7bf67dfd096ee8c9c81c67b8ac8d6f361ddbffd8c1831148aeb3a3` |
| Fresh recovery-commit read | `research/m31-radial-certificate-2026-10-23/viewer/app.js` | 8162 | `2ecd9d93c59f125c9938e026f970bba8d089554f824771e15d72742960ef5e1d` |
| Fresh recovery-commit read | `research/m31-radial-certificate-2026-10-23/viewer/index.html` | 5182 | `4a959437eec8702bd6952637001ac04208018418a37eac92a7c3319223a6de29` |
| Fresh recovery-commit read | `research/m31-radial-certificate-2026-10-23/viewer/pins.json` | 999 | `abfb7e0be721bd4243a2cb41b0cbd0c1f2afee51594fbdfbe7728b9f23200b17` |
| Prior input receipt | `research/publication-receipts/m31-neighbor-density-result-2026-10-23.json` | 3552 | `37da10a634b812b5952aa900e1dc62900f360c1778651b89f99a01deae1fd396` |
| Prior input receipt | `research/publication-receipts/m31-neighbor-density-result-public-review-2026-10-23.json` | 131375 | `abf5fe51778853ed8963f5569696de3a8446de8ac2e5a10a852f2aeeaa289d76` |
| Prior input receipt | `research/publication-receipts/m31-neighbor-density-result-public-review-2026-10-23.md` | 7282 | `1d20038864e3a69a4f2b527a4a937226dc2aa6f4fe6ba01b8e3f2ab732fc7c14` |
| Fresh recovery-commit read | `research/publication-receipts/m31-radial-certificate-source-public-review-2026-10-23.json` | 79183 | `aefa55537cc43d03cbc70eb8defffba4d0aa44bd9ff5a26f67c3e1b4a374285c` |
| Fresh recovery-commit read | `research/publication-receipts/m31-radial-certificate-source-public-review-2026-10-23.md` | 9031 | `adb1a4b20006dbeaae8382f2f1dfb4d38c7aa7579986ea1f040dbab88b885a82` |
