# Three.js evidence-view verification

The single frozen browser allocation passed all six check groups in ui/qa.json. It checked all 1,920 rendered Float32 position buffers against the audited saved stages, timestamps/statuses, all twelve clip rows, exact decision/cost/coverage text, selection/playback/slider/orbit/reset, desktop/mobile layout and rejection of altered evidence. No unexpected browser errors were recorded.

The parent visually inspected ui/desktop.png and ui/mobile.png. Both show the 3D point flock, controls, full decision text, the inherited refused trial at 3.62 seconds and the saved 4,032-entry candidate list. The flock is rendered as small points; users can orbit and zoom. The refusal is visibly identified as a trial, not a completed flight step. The table and copy remain readable without page overflow on mobile. These screenshots inspect rendering only and are not physical validation.

The frozen viewer was not changed after the test. All five scientific/display allocations passed within their original limits; no rerun was used.
