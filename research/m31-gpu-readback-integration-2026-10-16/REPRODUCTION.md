# Reproducing static preparation checks

No operational invocation is allocated. Do not run capture-transport.py,observe-transport.py,run-once.py,host-worker.cjs or the full saved-evidence checker. No browser,GPU,diagnostic or experiment-result review was executed during this checkpoint.

Safe pure check from repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s research/m31-gpu-readback-integration-2026-10-16/source -p test_admission.py -v
```

The Python admission suite completed4test methods, including malformed inputs and window boundaries. AST parsing of the5initialPython source files succeeded without importing operational entrypoints. Host checks: six Node syntax checks and25inert cases are recorded in STATIC-CHECKS.json and PURE-TEST-RESULTS.txt. The corresponding safe command is `node research/m31-gpu-readback-integration-2026-10-16/source/host-logic.test.cjs`; it imports only pure logic/validator, reads bounded local source text and uses an injected in-memory writer. Independent checker pure-test commands/results are recorded under review/:37pure/scratch cases passed. Its safe primitive test script is `review/test_review_primitives.py`; read it before using its output-path argument. It never invokes the full saved-file checker. Final combined static parsing covered9Python files with0errors. Use the documented installed Node/Python versions; no package installation is needed.

Source identity is provided by manifest.json. Each path is repository-relative; compare actual length andSHA256. Historical preparation's30pins must remain unchanged. Exact public source checkpoint identity is recorded after push in a separate publication receipt. A publication inventory proves saved-byte identity; it does not prove runtime outcomes.

Privacy: public package contains only synthetic fixtures,source,source-check results,and concise specification receipts. Cached primary HTML,private runtime paths/process metadata/nonces/traces and chat attachments are not included. No operational data or runtime provenance is fabricated.
