# Milestone 32 browser and delivery QA

The existing research tab was reloaded with the new Three.js milestone. Verified in the Codex browser at its natural 615 × 977 viewport; no viewport override or mobile-device emulation was used.

- Visually inspected the flock wake envelopes, arrows, colored drone rotors and two-drone scene. Corrected a canvas CSS sizing issue during development; the final canvas fits its panel.
- Source inspection caught and corrected a rotor-order mismatch in the visual before delivery. The builder now exports the original physics rotor coordinates; the viewer uses that exact order for the corresponding four inflows. Drone enlargement is explicitly disclosed.
- Default force-coupled snapshot at 4 seconds shows peak inflow 2.49 m/s, 35/50 affected drones and 0/50 finished.
- Two-drone view at 0.8 m gap, directly underneath, shows mean inflow 2.24 m/s and hypothetical lift loss 18.3%. Moving 0.6 m sideways changes both to zero under the model's radial truncation. At 0.1 m gap directly underneath, the UI explicitly reports unsupported near wake.
- All four recorded outcome controls match original records: force coupling stops at 13.2375 s (display 13.238), linear rotor coupling at 7.770 s, RSS rotor coupling at 8.915 s, and off reaches 180 s with 50/50 complete. The off scene emits no wake envelopes or cues.
- Snapshot playback advances from the beginning and stops at the recorded outcome. Scrubbing returns to the chosen saved frame. Wake, link and animated-direction toggles were disabled together; the screenshot showed only the drones and environment. Re-enabling restores the airflow view. Camera reset works.
- The numerical table displays all four new comparisons. The follow-up text displays 4.85 cm divergence from differing inherited states at the same step. Earlier failed full-trajectory checks remain labeled unresolved.
- No horizontal overflow at the natural viewport. Final browser error/warning log is empty.
- Saved contextual screenshots: `milestone-32-flock.png` and `milestone-32-pair.png`.

The browser displays precomputed fields and recorded flock snapshots. It does not execute the large-flock research integrator or calibrated CFD. No browser frame-rate benchmark, wide-screen emulation, physical validation or safety certification is claimed.
