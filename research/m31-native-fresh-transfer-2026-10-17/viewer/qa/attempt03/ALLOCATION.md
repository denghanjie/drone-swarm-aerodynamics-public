# Explicit parent authorization: focused attempt 03

The parent reviewed the minimal harness diff and authorized exactly one focused attempt 03. Accepted source inventory SHA-256: `558ab850310ba326bdca61a3d4b1f57217b53161905a51d23b37b3abb753344e`. Accepted protocol SHA-256: `4e6361cca9ca393b643a04fbf21c6d3288cdf1bebf34a922e830ccb54c72c6e5`.

The allocation is 120 seconds outer wall and 16 MiB aggregate attempt artifacts, with the reviewed 95-second work deadline and owned-child cleanup. Dispatch uses explicit escalation and the frozen installed runtime. No scientific import or call, viewer edit, source rebinding, republication or automatic retry is authorized. Attempt 02 remains failed and unchanged; all earlier evidence is preserved.

Use the existing localhost:8876 server without changing it, a fresh owned Chrome root/profile, and the `fresh-attempt03` environment guard. Successful cleanup requires graceful Browser.close, root exit and close code 0 with null signals, reaping, and profile removal. This file records authorization before launch; the execution receipts record the actual outcome. Parent screenshot inspection remains separate from automated verification.
