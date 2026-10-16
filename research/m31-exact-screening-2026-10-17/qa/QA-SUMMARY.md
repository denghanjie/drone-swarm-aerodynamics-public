# Display QA

The static Three.js hierarchy diagnostic passed45checks on the second and final display allocation. The flow was: open saved checkpoint → select scene/receiver/rotor → inspect updated group and proof counts → orbit the camera. Desktop1440×1050 and mobile390×844 were checked with installed Playwright and Chrome155.0.8059.80. Browser plugin not available; no installation was performed. Localhost8876 remained the target.

| Check | Result |
|---|---|
| Intended URL/title and meaningful content | Passed |
| Three.js canvas and18scene controls | Passed |
| Scene, receiver, rotor and orbit changes | Passed |
| Fallback state/no tree, invalid prepared geometry | Passed |
| Static scope, cost caveat and historical airflow-off disclosure | Passed |
| All linked evidence targets | Passed |
| Mobile page width and visible layout | Passed |
| Console errors/warnings and framework overlays | None observed |
| Corrupted binding/model/raw records hide claims | Passed |
| Saved desktop/mobile screenshots | Visually inspected |

Attempt01 stopped at30checks in1.203s because the test used selectOption('2'): the second displayed rotor has label2 but internal value1, so Playwright selected that earlier label match while the assertion expected value2. The failure screenshot shows label2; no browser errors/warnings occurred. The original QA script and full viewer snapshot are retained under attempt-01/source-snapshot/. Only the test was corrected to selectOption({value:'2'}); viewer source and scientific records were unchanged. This is a harness correction, not a repaired scientific allocation.

Attempt02 completed45checks in2.533s with zero errors/warnings. Receiver1 and rotor value2 (displayed rotor3) were exercised, followed by orbit and mobile scene selection. Screenshots show teal zero-proof boxes, amber scanned leaves and the selected rotor marker. Sparse scenes have small drone markers; zoom remains available. This is geometry/proof inspection, not dynamic simulation validation.

Both display allocations are closed. No scientific kernel was imported or executed by either. New browser engines, other device sizes, live coupled trajectories and5,000-drone aerodynamic execution remain untested. The user-visible tab was queued through Open in Codex.
