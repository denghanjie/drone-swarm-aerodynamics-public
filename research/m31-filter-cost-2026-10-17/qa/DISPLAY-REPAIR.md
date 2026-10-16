# Display-only repair after attempt 01

Attempt 01 closed after 1.983 seconds: 15 checks passed and the 16th assertion, receiver79/rotor3, failed. No browser errors or warnings were recorded. Original viewer/QA sources, screenshot and full failed report remain in their attempt directories.

The harness passed rotor indices as bare strings to Playwright selectOption. The displayed rotor labels are one-based, while option values are zero-based. Installed Playwright source shows that a bare string matches either value or label; a request for `3` can match label3/value2 before value3/label4. The saved failure does not retain the actual selected value, so this is a source-supported harness diagnosis, not an observed value trace. Change all selectors to explicit `{value: ...}` to remove the ambiguity while preserving the same assertions and scene/rotor allocation.

Independent presentation review also requested clearer timing language. The HTML now says complete method-call cost, names included/excluded work, and explains why median paired ratios differ from dividing the two median columns. No scientific source, data, acceptance rule, display geometry or evidence binding changed.

The second and final display-only allocation is justified by this concrete harness correction. Its 60-second budget and intended checks remain unchanged. No third display run is permitted. Library source identity supporting the diagnosis is saved in REPAIR-EVIDENCE.json; no additional browser or scientific probe was used for diagnosis.
