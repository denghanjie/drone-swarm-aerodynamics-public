# Can we calculate the airflow less often?

The previous experiment showed that airflow-induced turning matters in this simulated flock. This experiment keeps both the pushing and turning effects, but reuses their rotor-load ratios for 10 milliseconds at a time. It asks how much that shortcut changes the predictions.

Before the run, we fix one 16-drone case, three integration resolutions and explicit error limits. We keep the loads just BEFORE each refresh so recalculation cannot hide the shortcut's error. A separate checker reconstructs saved calculations. A successful run and an accurate shortcut are different outcomes.

Read PROTOCOL.md for the frozen plan, config.json for numerical settings, CLAIM-LITERATURE-LEDGER.md for scientific scope, REPRODUCE.md for execution and SOURCE-RESTART.md for allocation state. Results and a paired Three.js recorded replay are added only after the run. Physical validity, a novel contribution and efficient 5,000-drone browser simulation remain unresolved.
