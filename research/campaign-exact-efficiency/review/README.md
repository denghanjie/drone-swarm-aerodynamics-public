# Independent numerical review records

The pre-run plan review and amended-source code review document the exactness, support-envelope, domain-order and ownership requirements. The intentionally extreme-coordinate two-state record preserves the v0 false-zero failure; the amended result explicitly rejects that out-of-scope coordinate. These are software stress probes, not plausible flight data or physical validation.

From this campaign directory:

```sh
node review/large-translation-probe.cjs source-versions/exact-aero-v0.cjs.txt src/exact-aero.cjs
node review/large-translation-probe.cjs src/exact-aero.cjs
node review/targeted-guards.cjs src/exact-aero.cjs
```

The inherited huge-coordinate grid timeout is additionally recorded under `robustness/raw/independent-checks.json` in the `malformedAPI` outcomes; the bounded reproduction is in `robustness/checks.cjs`. Do not run the legacy enormous-coordinate case without a subprocess timeout.
