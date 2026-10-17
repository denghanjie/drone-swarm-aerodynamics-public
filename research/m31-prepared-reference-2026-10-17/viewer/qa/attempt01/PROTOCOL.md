# One prepared-reference UI validation

The parent explicitly allocated UI QA after the new scientific terminal result
passed and its source/publication gate closed. This is UI-only validation of saved
evidence. No scientific imports, oracle, native-load query, trajectory generation
or model fitting. Browser plugin is unavailable; use the installed pinned
Playwright and Chrome runtime. Screenshots and receipts are requested checkpoint
artifacts, not a separate HTML report.

Flow under test: load the new prepared-reference viewer -> choose saved flock,
receiver and rotor -> actual saved positions, zero/scalar/positive membership and
preparation reuse counters render -> toggle boxes, orbit and reset.

One attempt: 95-second work deadline, 120-second outer total and 16 MiB aggregate
artifacts. Exactly four pages: main, changed saved-record response, missing result
response, and a deliberately failed result with consistent test response hashes.
The last fixture rewrites only that page's returned binding hash literal/binding
and index bytes; it leaves all disk source/results unchanged and tests the
qualification gate after valid hash checks. The missing-index fixture intentionally
produces one explained HTTP404 console error. No other page errors, console
warnings or request failures are accepted.

Use 1440x1050 desktop and 390x844 mobile viewports. Select both 64-drone cases,
receiver indices0/63 and all four rotors in both viewports:32 fixed selections.
Compare all64 uploaded positions, zero/scalar/positive membership, box count and
selected-scene reuse counters to saved records. Check all24 result rows and actual
aggregate counters. Test box visibility, orbit/reset, invalid selection, corrupt
record, missing result, and failed qualification. Capture and inspect desktop and
mobile screenshots and check page overflow, identity, content and console health.

Use the existing `http://127.0.0.1:8876` server without restart. Requests stay in the
pinned local viewer/evidence/dependency closure. Own one fresh Chrome root/private
profile and close it gracefully; verify direct exit/close/reaping/profile removal.
Forced root cleanup fails QA. No process-group signals or hard memory containment
claim. The supervisor owns only its Node child. The frozen fresh-transfer runtime
pins identify Python, Node, Chrome and Playwright. Freeze viewer SOURCE-PINS before
launch and verify all scientific/source/bound viewer files before and afterwards.

Launch must leave120 seconds before03:00UTC17October2026. Preserve all failed
outputs. The parent allows at most two UI attempts, with a second only after a
concrete UI diagnosis and a separately written repair protocol; no scientific
source or evidence may be changed.
