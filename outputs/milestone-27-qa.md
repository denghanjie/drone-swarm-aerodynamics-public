# Milestone 27 QA — in progress

Seven aerodynamic implementation checks pass, including the constant-power identity and moment accounting. Airflow-off reproduces the earlier states, metrics and scientific samples exactly on the fixed development case. All three active variants ran the two-second development smoke test with finite states and nonzero inflow. Forced domain exits at 0, 0.1 and 0.13 s preserve exact terminal frames and unique sample timestamps. These are software checks, not empirical validation.

The 25-job protocol was frozen before fresh seed1601/1602 mission outcomes. Near-field/tilt exits remain separate from contact envelopes. Full mission comparisons, streamed-artifact checks and browser QA are pending.


**Source audit correction:** The passing regression against the earlier pair model inherited its adjacent-motor normalization error. These checks did not validate the source geometry. Milestone28 replaces that regression with an explicit opposite-motor geometry/analytic-profile check. Milestone27 is a retained implementation-error record; its airflow-off branch is unaffected.

An incremental binary/source audit passed41 checks across8 completed cases. The browser was tested on the50-drone seed1601 wide rotor-moment contact: correct outcome, terminal time11.9275s, drone29 and partition-0-below. The revised page displays the normalization-error banner, contact timeline and red marker through solids. Screenshot `milestone-27-error-record.png` records this. No errors/warnings were reported by the browser log query. Final cases and refinements remain pending.

The matched-start/full-state audit now passes129 checks across16 completed cases: exact common initial states across aerodynamic variants, finite17-state endpoints and unit endpoint quaternions are included. Additional event-identity comparisons are kept separate from the frozen numerical criteria. Browser QA of seed1602/wide/RSS verified the amber model-domain marker, drone4, the explicit20-degree thrust-axis limit, and identical displayed terminal/total times11.39s. The page remains visibly marked as the wrong-normalization record.

The original study is now terminal after the verified mapping error:20 completed primary cases, five uncompleted refinement/cadence cases. The162-check final error-record audit accounts for every prescribed case and preserves partial files. This is not a25-case study-completion or numerical-refinement claim. The corrected25-case study28 is running.
