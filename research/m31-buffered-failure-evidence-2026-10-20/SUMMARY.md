# A shortlist worth testing, but no speed result

20 October 2026. Computational research only.

We tried to make repeated airflow calculations cheaper by remembering which drones might affect each other. Think of keeping a shopping list instead of searching the whole shop again. The list could be reused while drones moved within conservative limits; airflow and forces were still recalculated from each current state. Reusing neighbor lists is an established idea, not our invention.

The corrected test passed all 12 small comparisons against the existing baseline. For the 1,000-drone input, the candidate completed six prescribed states, then the seventh was rejected because some interactions entered a near-field region unsupported by the current model. The eighth state was not evaluated. These were prescribed test positions, not a time-integrated Boids flock.

The rejection recorded 186 source-to-receiver-rotor classifications. That is not a count of drones, collisions or observed physical failures. No 1,000-drone baseline query ran, and no measured timing comparison completed. We therefore have no large-case equality result, no speedup result, and no successful qualification of this candidate. We cannot infer that real flocks cannot fly from this artificial test.

There were two stopped scientific attempts. The first made 18 calls and stopped because our test harness incorrectly expected success for an intentionally wide input that both implementations rejected. A separately reviewed correction changed only that expected outcome. The second made 31 calls, passed the 12 controls, and stopped on the large-input near-field refusal. Both records are retained. We did not reduce the movement after seeing the failure.

A separate saved-data audit checked the 49 recorded calls, input associations and preserved outputs. Its success means the failure evidence was checked; it does not mean the model was validated. The updated [Three.js view](viewer/) shows all eight saved input states and distinguishes completed, refused and unevaluated states. It runs no aerodynamic solver. Desktop and mobile checks passed after a separately recorded correction to the display-test selector; the original failed check remains saved.

The practical next question is whether useful three-dimensional Boids motion can stay inside the current model's computational admission rules. That requires a new prospective study, with fixed initial conditions, motion rules and failure criteria. Passing those rules would establish computational usability only. Physical airflow accuracy, flight safety and novelty remain unestablished. No such new study has been launched here.

Evidence: [saved audit](results/audit.json), [corrected failure review](../m31-buffered-candidates-corrected-2026-10-20/review/FAILURE-REVIEW.md), [claim ledger](RESULT-CLAIMS.md), [display checks](UI-QA.md), [verified antecedents](LITERATURE.md), [restart](RESTART-RESULT.md).
