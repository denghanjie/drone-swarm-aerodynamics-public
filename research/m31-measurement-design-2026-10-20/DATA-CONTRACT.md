# Required experimental record — schema proposal, no data supplied

Keep raw/reconstructed observations distinct. Any future release must identify its license, version, immutable file hashes and processing source. Field names below specify required information, not actual observations or a runnable importer.

| Record | Required information |
|---|---|
| Acquisition | experiment/run/acquisition IDs; timestamp; independent rerun definition; exposure/pulse separation and sampling cadence; plane-order schedule; averaging interval |
| Geometry | rotor centers/radii/axes; airframe pose/trajectory; laboratory/body frame and handedness; origin and independently registered reference axis; physical l definition; site coordinates in m and registration uncertainty |
| Operation | thrust and whether total/per-rotor, density, RPM/control state, ambient flow, walls and other boundaries; before/after reference checks |
| Observation | directly measured signed Vx,Vy,Vz in m/s; effective spatial support/interrogation region; raw and processed signal references; missing/nonfinite/masked status with reason |
| Uncertainty | component error covariance, coordinate/pose uncertainty, shared calibration nuisance variables and their covariance, temporal correlation and between-run variability; estimation method/coverage assumptions; distinguish flow variability from measurement error |
| Processing | calibration target/mapping and reference-velocity evidence, timing and signs, stereo cross-talk, filtering/interpolation/masks, reconstruction constraints, order of transform/averaging and software/version/source |
| Model freeze | exact model source/constants/domain, independent input measurement/scaling evidence, status of inherited gain, output component basis and units; no target-fitted corrections |
| Test freeze | primary 48 sites and all-site coverage rule, secondary comparisons, independent practical margins, interval/multiplicity method, replication/precision rationale and bounded execution protocol |

Store shared error sources once with explicit relationships rather than pretending each site has independent calibration. A table of per-site standard errors alone is insufficient for shared-error contrasts. Do not fabricate raw images, calibration certificates, covariance or experiment IDs to make this schema appear complete.
