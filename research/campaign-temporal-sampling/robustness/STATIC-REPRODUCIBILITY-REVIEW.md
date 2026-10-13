# Prospective harness falsification and reproducibility review

Review began after the protocol was adopted and before any numerical fixture or campaign case was executed. This document is a source review, not a passing test report. Numerical authorization remains with the parent.

## Already present and worth preserving

- Replay evaluates the same endpoint state with four sampled-and-held rotor scalars.
- Every interval uses its old hold at both endpoints. Event left limits and the terminal old hold enter peaks and trapezoids.
- Body torque difference is rotated using each endpoint quaternion before world angular impulse.
- Reference gates implement the adopted absolute caps and comparison floors separately.
- The coupled loop ends before a terminal field/controller refresh.
- Dense states and fields have explicit binary shape/order metadata and compressed/uncompressed SHA256.
- Source loading uses a pinned snapshot, whose relative dependencies are enumerable.

## Blocking requirements found in the initial source

These were sent to implementation and reference review immediately. They remain findings against the initial inspected source, not assertions about the final amended harness.

1. Quadrature initially compared terminal vectors and scalar prefix maxima, rather than vector differences at every common coarse prefix. Equal maxima can hide a different vector path.
2. Diagnostic field rejection initially lacked run identity, previous production held-field timestamp, and explicit attempted inputs. Rejection between refreshes or at T must stop the driver and retain its state.
3. Excitation labels initially used an absolute inflow-range threshold, instead of the adopted loaded fraction, normalized inflow range and separate force/torque amplitudes.
4. Storage initially counted selected raw arrays after writing. Hard pre-write logical accounting, failure reserve, all artifact classes and external wall supervision are required.
5. `screen()` initially returned `passed=false` but an empty failure list for a NaN metric. Nonfinite metrics must be retained as failures.
6. `readSeries()` initially trusted shape metadata after verifying payload bytes. A smaller shape could silently truncate a valid payload. Validate positive integral dimensions and product(shape)*8 against payload length.

## Fixture construction

`test-harness.cjs` uses isolated module loading for synthetic replay arrays and mocks all coupled dynamics/controller/field functions when testing orchestration. It never invokes the campaign CLI or generates another genuine Boids trajectory. Real scalar-load tests use a few explicitly constructed states. Scalar ramps have closed-form one-sided-trapezoid expectations; rotating-torque fixtures have analytic vector expectations. Binary tests write only tiny files inside this directory.

Each authorized attempt writes a new timestamped folder with exact command, runtime, campaign configuration, source hashes, all passing/failing check names, and separate failure details. Later passing attempts do not overwrite earlier failures. Source hashes are compared before and after each run to flag a moving implementation.

## Reproducibility conditions before interpretation

- Freeze final plan, configuration, harness, full model source graph and Node/platform metadata before compatibility.
- Preserve failed checks and every real campaign outcome, including stopped work and watchdog-only checkpoints.
- Rebuild metrics from raw retained full17 arrays; do not substitute screenshots or high-level summaries.
- Count this review, robustness artifacts, coordination files and any retained duplicate distributions under the same 150 MB logical campaign cap. The implementation's local ledger alone cannot account for sibling directories unless extended or given a reserved external allowance.
- A passed synthetic fixture establishes a narrow software property. It does not establish reference convergence, wake-model validity, flight safety, or large-swarm performance.
