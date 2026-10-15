# Initial viewer QA failure, retained

The first38-case UI matrix reached its console-health assertion with one `Decision mask checksum mismatch` error. The scientific experiment and raw hashes were unaffected. Static inspection found a UI race: a pending selection decompressed the old case's mask but checked its length against the new current case's vehicle count. The selected mask's own SHA remained tied to its saved row. Fix: pass the captured case count into mask verification; the existing selection-generation token then discards stale completions. No hash check was disabled. A full UI rerun is required after this display-only correction.

Pre-fix viewer source SHA256: f4828d1a2a35e089faa13d9388ecd888eaa22d9951ba83ab61a49df78e83d83f
Original source retained locally at /tmp/m31-omission-app-before-race-fix.js. No scientific source/raw file changed.
