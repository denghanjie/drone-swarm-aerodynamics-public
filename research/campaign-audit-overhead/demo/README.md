# Record-linked diagnostic viewer

This lightweight page embeds the existing, unmodified Three.js trajectory viewer and links diagnostic records beside it. It does not duplicate the large historical records or generate new flight paths. `evidence.json` currently reports that experiments are not released; replace it with links to actual saved outcomes only after they exist and are independently reviewed.

For the local isolated workspace, serve the workspace root with `python3 -m http.server 8000`, then open `/research-audit-optimization/demo/`. For a downloaded public repository, serve its root and open `/research/campaign-audit-overhead/demo/`. The published checkpoint must include the previous joint-stage campaign and its `implementation/demo/records.json`.

This requires an ordinary HTTP server because the reused renderer fetches local JSON/modules. Do not open the modular page directly as a `file:` URL. The earlier self-contained HTML is a separate offline attachment. No server was started or browser launched while creating this scaffold.

Existing flight paths remain explicitly historical. Dense audit inputs and synthetic stage packets are identified in experiment records, not replaced by the display's resampled poses. Rendering has not been browser-verified.
