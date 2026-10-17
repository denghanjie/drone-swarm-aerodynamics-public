# Camera fit after attempt 01 visual review

The original attempt's desktop view was clear, but the mobile final B view partly clipped the swarm. Its camera had been fitted to the initial pose. The parent requested a narrow framing correction and a separately approved focused QA attempt.

Before editing, the exact original `app.js`, `scene.js`, `index.html`, `style.css`, `binding.json`, and `SOURCE-PINS.json` were copied into `qa/attempt01/original-viewer-source/`, with byte pins in `PRESERVATION.json`. Attempt 01 receipts and screenshots remain unchanged.

Only `app.js` and `scene.js` change the viewer behavior. The app computes a display envelope from the selected run's complete saved trajectory and selected method's saved final force endpoints at the chosen scale. The scene pads it by 0.23 m to cover enlarged drone glyphs and arrow heads, encloses it in a sphere, and chooses the camera distance using the narrower horizontal/vertical field of view plus 12% margin. This supports a portrait or landscape viewport without clipping. The camera fits on run/method/scale change and resize; frame updates do not reset it. Reset returns to this full-run fit. Actual positions, quaternions, load words, forces and scale formulas are unchanged.

The scene exposes its actual camera projection and view matrices for the focused frustum checks. The QA computes homogeneous projections independently and checks padded centers and endpoints. This is display verification only, not a scientific calculation or new result.

Focused attempt 02 is prepared under `qa/attempt02/` with a 120-second outer limit and requires explicit parent authorization before launch. No second browser has been launched during this repair preparation.
