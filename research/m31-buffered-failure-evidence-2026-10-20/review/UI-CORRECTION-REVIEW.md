# Independent review of the separate display correction

20 October 2026. Read-only review of the failed display receipt and minimal successor source diff. No native/scientific query, export, browser or UI test was executed in this review. The existing viewer, exported evidence and previous source/results are unchanged.

The saved export closed successfully: exit code 0 and 0.309758958 seconds. The first UI allocation closed unsuccessfully with supervisor return code 1 after 9.631168166 seconds. Its QA report has `passed: false`, records the initial page/limitation-label check, and reports an eight-second timeout waiting for `canvas[data-stage="1"][data-points="1000"]`. The loop necessarily passed its stage-0 checks before reaching that wait. It did not complete the eight-state check or capture the planned screenshots. No additional JavaScript/HTTP error is recorded before the timeout; this is not evidence that all later display checks would pass.

The source diagnosis is consistent with that record. The viewer generates zero-based option values and one-based labels. A string selection can match either a value or a label; string `"1"` is therefore ambiguous between the first option's label and the second option's value. The successor uses `selectOption({value:String(s)})` in the eight-stage loop and `selectOption({value:'6'})` for the later refused-state selection. Both sites now name the intended value explicitly. The viewer itself is not changed to accommodate the test.

The complete runner diff is limited to those two selection calls, a fresh `ui-v2/` result directory, and use of the dedicated `display-manifest.json` / `display-publication.json` gate. The new supervisor invokes `ui-v2.cjs` and has separate permanent launch-lock and receipt paths. It retains the 100-second external process-group limit and cleanup; the runner retains the 90-second internal limit, single browser launch and all existing assertions. There is no export or scientific module invocation.

This is suitable for one separately reviewed and publicly verified display-only attempt. It does not reopen the failed UI allocation or permit a repeat of either native attempt or the export. The dedicated display freeze must pin the new runner, supervisor, this review, UI-CORRECTION.md, unchanged viewer/rendering dependencies, exact exported data/audit/exit and viewer pins, and the old failed UI QA/supervisor receipts. Public verification must identify the full display-source commit before launch. The original failed QA record remains part of the final history.

All prior display obligations remain: exact saved Float32 position buffers and statuses for eight states, explicit unevaluated-state and no-comparison/no-speed labels, orbit/reset, desktop/mobile screenshots and overflow checks, error monitoring and corrupted-data refusal. Export admission still requires a passing audit, successful export exit within 30 seconds, no failure file and at most 10 MiB of export payload. Source review cannot establish screenshot quality or a passing UI result; the new bounded execution and subsequent image inspection remain pending.

The scientific interpretation is unchanged: twelve small corrected control pairs matched, six large candidate-only warmup states succeeded, stage 6 was refused and stage 7 was not evaluated. There is no large baseline comparison or speed result, no collision count, no physical-safety finding and no candidate qualification. Repairing the UI selector does not change those limits.

No remaining static blocker was found in the narrow correction. Source identities and the preserved failed receipts are listed below; this review does not embed its own hash.

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| UI-CORRECTION.md | 1036 | f7bafec04b24c1432ca0e1d24d984ca366678ded8a3ef71a386c3cc0961f9742 |
| source/ui-v2.cjs | 5692 | 2fb03ee6c7144f8c99cf2eb19b9d76fe98cb7e47779ef4845d29254c3e734014 |
| source/ui-v2-supervise.py | 1207 | 602a8574880ec7a409a6a1ef648d2b367912329dfd49f60a30cccfc0555aef9e |
| ui/qa.json | 371 | 053a9b231bac90fe89cb3b246d231dee580fc585a6875bffd624333c0603521a |
| ui-supervisor.json | 83 | 86f4dbdd24bbb5a20b5f5d03f1a01cb58c403afc67f9f47532c4328b184b200e |
| results/exit.json | 102 | bb79d4f3014637489e6981348cc1315464950e4f63a205d03dd3f5ee013affd6 |

The supervisor was parsed for syntax only; the runner was read and compared as source. No execution result is implied.
