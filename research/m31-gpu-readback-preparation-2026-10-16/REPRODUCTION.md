# Reproduce preparation only

The delivered checks used the installed Node.js 24.19.0 and Python 3.9.6. No dependency installation, browser, GPU operation or network request was needed. The exact check records are `source/STATIC-CHECKS.json`, `source/pure-test-results.txt`, `review/STATIC-PREPARATION.json` and `review/PURE-TEST-RESULTS.json`.

Use a scratch copy of this preparation package if repeating the pure checks; preserve the published records. From that scratch package root:

```sh
node --check source/gpu-readback-page.js
node --check source/validation.cjs
node --check source/generate-fixture.cjs
node --check source/validation.test.cjs
node source/validation.test.cjs
python3 review/test_pure_bytes.py
```

The Node tests read page/shader source as text, import the pure validator/reference code, and use handcrafted envelopes. They do not evaluate the browser page or compile WGSL. The Python tests use only independent deterministic reference/byte code and write a new pure-test report in the scratch copy. Neither command reads an actual saved GPU output or establishes physical accuracy.

The producer's independent BigInt/manual-byte expectation and the reviewer's Python/modular-arithmetic/little-endian expectation agree on full fixture bytes: SHA256 `ba507e3ef0ad8991b3e84530f89fa51501e9c6fd274157d519ef10cb8aded951`. Initial sentinel bytes agree at SHA256 `944fbd39dc3fa2a2b8c9a2eef1c9c02b812911f4831b22c6c4e17cfe6a770e3a`. An expected fixture is not output evidence.

There is deliberately no operational launch command here: no integrated host/supervisor or full saved-file checker has been delivered or admitted, and no new launch window or execution budget exists. Finish the gates in NEXT.md before creating a separately allocated test.
