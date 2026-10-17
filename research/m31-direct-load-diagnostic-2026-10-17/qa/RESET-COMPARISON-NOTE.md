# Reset screenshot comparison correction

Attempt 01 completed all 36 state/candidate/tier combinations and 12 overview category/tier projections, then failed the SHA-256 equality comparison between the initial and reset canvas PNGs. The attempt remains unchanged and failed; no viewer file was repaired.

Both screenshots were opened and visually inspected. A read-only PNG decoder found 942 changed pixels out of 424,842, all on the single top boundary row (`x=0..941`, `y=0`) of the 942 × 451 element screenshot. Maximum channel difference was 15. All 422,060 pixels inside a one-pixel border were exactly identical, with zero channel difference. The scene framing and content were restored; the screenshot boundary varied after scrolling to the reset control.

The next attempt retains full-image pixel-difference statistics and requires exact decoded equality in the canvas interior, excluding the one-pixel screenshot clipping boundary. Orbit and zoom must still change rendered screenshots. This corrects a screenshot comparison artifact; it does not relax any pose, link, status, interval, GPU-upload or draw-count assertion. `png-diff.cjs` reads screenshots only and never edits them.

All 159 frozen pins and four accepted results were preserved in attempt 01. The scientific files, built data and viewer source remain unchanged.
