# Display-only repair after attempt01

Attempt01 failed in6.785seconds before any display checks completed: OrbitControls imports the bare module name `three`, but the new HTML omitted its required import map. A favicon request also returned404. Added the local Three.js import mapping and an empty data favicon. Corrected the QA readiness timeout argument placement to use its intended25-second limit; total display deadline remains60seconds.

Original viewer/QA sources and failed screenshot/report remain in attempt-01-source/ and attempt-01/. Scientific source, results, references, controls and acceptance rules are unchanged. The second and final display allocation is justified solely by these concrete presentation/harness corrections; it never executes the scientific model. No third display allocation is authorized.
