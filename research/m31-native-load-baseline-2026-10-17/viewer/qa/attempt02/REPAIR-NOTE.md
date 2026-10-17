# Authorized harness-only repair

Attempt 01 remains failed and unchanged. Attempt 02 retains the same complete fixed schedule and the same 240 s outer / 32 MiB output limits. No data, projection, viewer or scientific source changes are made.

The only functional repair changes the three `#exact-record` reads from `innerText()` to `textContent()`: the JSON field-address check and both rejection-state checks. All other `innerText()` reads were inspected; they read visible headers, cards, captions or status labels, not closed details content. The QA attempt identifier changes from 1 to 2. `QA-HARNESS-DIFF.patch` records the exact source differences.
