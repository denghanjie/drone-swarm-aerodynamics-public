# Milestone 25 verification

## Numerical artifacts

All 13 frozen runs completed: one post-hoc 200-drone refinement and 12 short timing runs. All numerical source hashes match the frozen protocol. Removing the initialization timing assignment restores the milestone24 simulator byte-for-byte. The finer audit uses identical initial states. Three timing repetitions per count have exactly identical final states and scientific metrics; timings vary as expected. Five exact replay endpoints match saved final positions and quaternions. All 13 checks in `milestone-25-artifact-checks.json` passed.

The 1.016 mm fine-step agreement is numerical evidence for one 200-drone case, not measured physics validation. The 1,000/5,000 runs cover two seconds near the initial cloud; they do not establish full mission performance.

## Browser measurements and checks

The four rendering measurements followed `milestone-25-render-protocol.json` after the numerical study ended. Each used 30 warmup plus 240 measured frames at 1280×800 and pixel ratio 2, trails off, fixed overview, with the document reporting visibility `visible`. Raw results are in `milestone-25-rendering.json`. All four median frame intervals were about 16.7 ms. At 5,000, median scene-update CPU time was 5.4 ms and median render-submission CPU time was 0.4 ms; GPU execution time is not measured. This is a single session-specific sample per count, not a broad browser performance guarantee.

All five trial selectors loaded. Outcome values matched 200/200 at 120 seconds for the audit and 0/N at 2 seconds for timing windows; contact buttons remained disabled. Records: `milestone-25-ui-outcomes.json`. Play/restart advanced the 5,000-drone replay, and overview/close-up views rendered its volumetric group. No browser errors or warnings were captured. One initial wait for the first rendering measurement timed out before the 270-frame process finished; the same live measurement completed and its result was collected without restarting it.

Desktop 1280×800 and mobile 390×844 screenshots were inspected. Mobile document width equaled viewport width (390 px), with no horizontal overflow. Temporary viewport override was reset. Screenshots: `milestone-25-overview.png`, `milestone-25-desktop.png`, `milestone-25-mobile.png`.

The viewer uses saved exact positions/quaternions and visual interpolation. Its clocks, timing-window labels and mission limitations are explicit. Replay speed must not be treated as physics speed.
