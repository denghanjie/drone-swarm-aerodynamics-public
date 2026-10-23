# Independent public source verification — radial diagnostic

Passed on 2026-10-23T00:53:01.222551+00:00. This is an identity receipt, not a numerical result or allocation launch.

- Source commit: `d1a9d8d04974f54f52889f348f3194b7f152fcfb`.
- Manifest: `research/m31-radial-certificate-2026-10-23/source-manifest.json`; 11192 bytes; SHA-256 `2e7b6e06d675d29a1b20a7a5f20dd88753ef207a574c194a1407609a12f1bb76`.
- All 46 file pins verified: 31 source and 15 input pins, including the complete three-file Three.js module closure.
- Fresh public reads: 47 (manifest plus all pins), 11,561,453 verified bytes. No previous remote verification was reused.
- All 46 files and the manifest match local working-tree and source-commit Git bytes. Each of the 15 input files additionally matches its declared origin-commit Git blob.
- 156 successful identity operations; 0 failed attempts. Every attempt is retained in the JSON receipt.

Public source files were read at the source commit; input files were freshly read at their declared immutable origin commits. All were independently matched by byte length and SHA-256. HTTPS reads required status 200, allowed at most three attempts, and were bounded to 45 seconds per transfer and each expected file size. Local/Git object checks and downloaded bytes were compared without interpreting or executing research source or saved-state data.

No diagnostic, control, audit, browser, model, timing experiment, saved-state reaggregation, archive read or decompression occurred. All four allocation output directories and supervisor launch locks were absent at both start and completion. Runtime/source conformance and universal cache correctness remain unproved. No old evidence was changed.

The JSON receipt contains every operation, URL, commit, observed identity and anomaly. Receipt files are additive publication records outside the source freeze.

## Verified pin inventory

| Kind | Path | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| source | `outputs/step02b-source/vendor/OrbitControls.js` | 38703 | `b97879c748170baadeb3fb84cea1ffdf4674e283dc06042f34e2acb95a76042c` |
| source | `outputs/step02b-source/vendor/three.core.js` | 1403455 | `eb077d2417f61d3e6d9264c317cabc4ea35769ed6b0ab533067292a550784c20` |
| source | `outputs/step02b-source/vendor/three.module.js` | 603113 | `c8211c69345d2e9949dc7a8ac969380497aa0600a5a8ac6a459c8cd02dd9cb8a` |
| input | `research/m31-native-fresh-transfer-2026-10-17/source/vendor/anchor-kernel.cjs` | 11828 | `c2ab29e4f53341706582d52149df96cd93323d3943ac145f288fbbae4de71a8a` |
| input | `research/m31-native-fresh-transfer-2026-10-17/source/vendor/kernel.cjs` | 16676 | `efc87f4c0f9d1a5a9b754d9d334ce295227a0cb01ce6980e4818313dd35d3bc8` |
| input | `research/m31-neighbor-density-2026-10-23/LITERATURE.md` | 7635 | `4f810c7f26682b74211b2b2deeddeaa7a3c8eef8d67a5afb1834953c11123881` |
| input | `research/m31-neighbor-density-2026-10-23/RESULT-CLAIMS.md` | 3734 | `1aca0c6edde293c20771f38a13afe4acb16e6bcc321cdb41842f9ed274e88bfe` |
| input | `research/m31-neighbor-density-2026-10-23/audit-supervisor.json` | 217 | `ef2984b8c51e33956e04e20b9204ff1f04c0db69823c8742e1f4dbb4a3d7f4d7` |
| input | `research/m31-neighbor-density-2026-10-23/audit/audit.json` | 27023 | `4c3b9dac6426d8e7c029795f3190a402f1e7ba9a21d3f9771b644e5f9a65b052` |
| input | `research/m31-neighbor-density-2026-10-23/audit/exit.json` | 77 | `19df4f54accc282b5c81fadada0a65780c9feacaec6b4ad0d6436476babec45e` |
| input | `research/m31-neighbor-density-2026-10-23/producer-supervisor.json` | 224 | `ac48660ef321c243e2a718e765823ecdf092b79d84ba2356b8599c37692ec9bf` |
| input | `research/m31-neighbor-density-2026-10-23/result-manifest.json` | 19976 | `acb61c176bcf87250a7658b2675d00fd8af4104a0504da5c1fb80bebdf56a5cb` |
| input | `research/m31-neighbor-density-2026-10-23/results/stages.jsonl` | 9063908 | `8098f5d2478b9a7f7184ed34f5df41199b565f969e9691ad9099ee6f3e48c1c3` |
| input | `research/m31-neighbor-density-2026-10-23/results/summary.json` | 16311 | `f786d6424102ce501e021531dadb94d9a66938870572045362dc85a290c06644` |
| input | `research/m31-neighbor-density-2026-10-23/review/RESULT-REVIEW.md` | 14411 | `f1cbc0b98907d66db4a2814ae694411e554520306174569529e350083a678fa7` |
| source | `research/m31-radial-certificate-2026-10-23/CLAIMS.md` | 2099 | `7b5b1cf78c11c2a5adf659f35b047b4eb00192f521c03f08ce00a9b51fb00d25` |
| source | `research/m31-radial-certificate-2026-10-23/EXECUTION-PROTOCOL.md` | 6354 | `2fb330b0357f1c5fa8c1f4fee1794a4f85a1fc3c8283b38c66630ea841eb6d80` |
| source | `research/m31-radial-certificate-2026-10-23/LITERATURE.md` | 7429 | `144ee6e8b0f8d3871280381321b67fdf6065bac875e41fdea1465761498d5c85` |
| source | `research/m31-radial-certificate-2026-10-23/PARENT-ACQUISITION.json` | 922 | `1f825f1ba585d19dcd0977b36eb6d3788b5c89f7cd5d0da149092271a2993b21` |
| source | `research/m31-radial-certificate-2026-10-23/PRIVACY.md` | 947 | `b4734e92615e56cf07134cf6d7182cf32c178c39612458f7890de6dacd311e70` |
| source | `research/m31-radial-certificate-2026-10-23/PROOF-PLAN.md` | 2804 | `86947109564eed27ffc4ddf1c33c878633a9133acc26cfe0359e948848ad6bc8` |
| source | `research/m31-radial-certificate-2026-10-23/RESEARCH-ACQUISITION.md` | 5767 | `042b32c71a318631dce699c03800d5f0e072fce2a6ccef2b7a9bbaea99ab59c5` |
| source | `research/m31-radial-certificate-2026-10-23/RESTART.md` | 1273 | `82b0b563e0456d5550b130751c8f8f04284bba7ba6ba4770a9de94a506d24f50` |
| source | `research/m31-radial-certificate-2026-10-23/SCHEMA.md` | 6713 | `f9e7b0cfc06bd19e8dd2ea988af897ca3c6e8dd6713f70385a0ea255e9788b32` |
| source | `research/m31-radial-certificate-2026-10-23/config.json` | 767 | `15c91f54c715ffb2eca2fb192ed78a7fb08fbfbd10a66847cbca54db2c5e786a` |
| source | `research/m31-radial-certificate-2026-10-23/input-pins.json` | 4377 | `4bede05495769f94b4ddcdf46ca977adc34c7256d2adc3c4c8974b66e957fba3` |
| source | `research/m31-radial-certificate-2026-10-23/node-release-SHASUMS256.txt` | 2967 | `be0629ee2bcd8e40bb856abdd3407f0762101b76bd60a36b8867f637733631c0` |
| source | `research/m31-radial-certificate-2026-10-23/review/AUDIT-DESIGN.md` | 12153 | `31fcd0a73a5d943cbe4ee32ef12c8c51fc243da282cce4cd3e1334bb575f18ff` |
| source | `research/m31-radial-certificate-2026-10-23/review/CONDITIONAL-LEMMA.md` | 9989 | `941d6b231e0f6cd5fef3c0968847c888828c278af2c22076860a61a025db2ea1` |
| source | `research/m31-radial-certificate-2026-10-23/review/PREPARATION-OBSERVATION.md` | 1426 | `787468ad165691ec96ff9abbcee779e2dd40a1abbf3e22bcb7348757410a9d2c` |
| source | `research/m31-radial-certificate-2026-10-23/review/PROTOCOL-REVIEW.md` | 14858 | `0f96d75be72e3675e909590b08b8ab348f6c35ff7ed7df8c2bb3c4511a5429b6` |
| source | `research/m31-radial-certificate-2026-10-23/review/STATIC-CHALLENGE.md` | 10500 | `70a1fd76ed80d808a3cd177ac6d7fc3f897bcb7862a2458197baf37fb9c5c542` |
| source | `research/m31-radial-certificate-2026-10-23/runtime.json` | 851 | `29e4afc02aab80de03d61cbc9dad39f8289983b3c7372506cc2986d0b2e68aed` |
| source | `research/m31-radial-certificate-2026-10-23/source/audit.py` | 45976 | `4f1b83d760be6ecaef9189902d3bf3ac83a6c53e3372c16cb63379a7410d43cc` |
| source | `research/m31-radial-certificate-2026-10-23/source/candidate.cjs` | 1938 | `cd5aa426d4ed45dc169fe6cd1047555db989744f4c80b4204ea602ccc7dfaee7` |
| source | `research/m31-radial-certificate-2026-10-23/source/common.py` | 4258 | `54da09f029d5c62f4a9fd042adc42f5372ccb9164c6a7ee1bf771ebf1af643ed` |
| source | `research/m31-radial-certificate-2026-10-23/source/diagnose.cjs` | 8461 | `01537a1cdc3b81835b44a52c8258c307f2bac40636d1f509e4890da0e68eef50` |
| source | `research/m31-radial-certificate-2026-10-23/source/finalize.py` | 1516 | `499aaa0919be50002645a245eac714ef48bc84bbe08064b73d8c19c96407a6f9` |
| source | `research/m31-radial-certificate-2026-10-23/source/launch.py` | 893 | `e8bb9bee0edf1fa372275864228d345594b032b0667dade0167d4f0edb19ef43` |
| source | `research/m31-radial-certificate-2026-10-23/source/supervise.py` | 3077 | `276627f0badc2f18e7ca1e5fc37ebdb46d111a6f55985b0baceee13fea98af59` |
| source | `research/m31-radial-certificate-2026-10-23/source/ui.cjs` | 9102 | `a8a431116a1b6fe44e908664e7fecb6ba95b470c148b2c16013fb91da412a9a7` |
| source | `research/m31-radial-certificate-2026-10-23/viewer/app.js` | 8162 | `2ecd9d93c59f125c9938e026f970bba8d089554f824771e15d72742960ef5e1d` |
| source | `research/m31-radial-certificate-2026-10-23/viewer/index.html` | 5182 | `4a959437eec8702bd6952637001ac04208018418a37eac92a7c3319223a6de29` |
| input | `research/publication-receipts/m31-neighbor-density-result-2026-10-23.json` | 3552 | `37da10a634b812b5952aa900e1dc62900f360c1778651b89f99a01deae1fd396` |
| input | `research/publication-receipts/m31-neighbor-density-result-public-review-2026-10-23.json` | 131375 | `abf5fe51778853ed8963f5569696de3a8446de8ac2e5a10a852f2aeeaa289d76` |
| input | `research/publication-receipts/m31-neighbor-density-result-public-review-2026-10-23.md` | 7282 | `1d20038864e3a69a4f2b527a4a937226dc2aa6f4fe6ba01b8e3f2ab732fc7c14` |
