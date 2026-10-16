# Viewer static review supplement

Source-only review of the presentation fixes in `research/m31-browser-screen-2026-10-16/viewer/derive.py` and `viewer/app.js`. No scientific code, reviewer, browser or presentation derivation was executed by this reviewer; no frozen file was edited. This supplements the retained initial static review.

The three previous findings are corrected in the inspected source:

- `app.js:81` now stops replay, hides content and clears the result-bearing headline/lead on failure, including a late selected-pose/load failure.
- `derive.py:31–43` and `app.js:27–37` require the complete seal-input set, match its bytes/hash pins, reject duplicate sealed inventory paths, bind evidence and generation/pose/load records to the sealed review-run inventory, and bind configuration to the frozen source manifest.
- `app.js:23`, `:38–49` enforce exact ordered case/process coverage; `derive.py:44` requires p0,p1,p2. The final `derive.py:48–50` guard rejects missing qualified generation metadata instead of silently omitting a case. The parent reports successful regeneration with the same displayed result after this last guard; no additional rendered run is claimed for it.

One narrow presentation guard remains: `app.js:48` and `:69` check a load pin only if it exists. A qualified display object can therefore retain a `y` array while omitting `loadPin`, bypassing its comparison with the saved load record. An inventory-valid same-N load from another case can likewise pass without validating its case identity. Current `derive.py` emits the correct p0/L path for every case, so this is an incomplete rejection guard, not an observed incorrect display. Before unconditional clearance, require qualified cases to carry `loadProcess:'p0'`, exact path `runs/p0/results/{case-id}-L.json`, and N load values; compare the loaded record's id/n/label as well as its y array. This needs only a presentation patch/check and no scientific rerun.

The parent reports rendered QA attempt02 passed 90 groups, including all 9 process-cell labels, all 78 saved frames / 858,000 rendered coordinate components, altered-seal analysis, duplicate cases/processes, and late pose failure clearing the header. That rendered result belongs to the parent; this supplement is static source review. The app/scene/HTML tested by that attempt are the versions pinned below; the final derive guard was added afterward.

| Repository-relative path | Bytes | SHA256 |
|---|---:|---|
| `research/m31-browser-screen-2026-10-16/viewer/derive.py` |6472|`62af7fd292a46243ffb442566b745e3fedf924d14ebdce1ffd18d830bf3a40ff`|
| `research/m31-browser-screen-2026-10-16/viewer/app.js` |10635|`fbe45c4085186768f3ec4a53304546282c4175b7c0d7de47964ed299926e531d`|
| `research/m31-browser-screen-2026-10-16/viewer/scene.js` |3875|`58718dc7452be35c1c3ba0a179b3f9398305e81dceb117466219b269b4ee88e7`|
| `research/m31-browser-screen-2026-10-16/viewer/index.html` |5217|`9bade1050d1343f09831b799f96bc9c0ac73441d6af6a69a0efdcbf7a566f528`|
| `research/m31-browser-screen-2026-10-16/viewer/display.json` |191487|`d888807ad31c2709a4e6b53999e409f2155e6d00c97d9a26eb7efa1d41837842`|
| `research/m31-browser-screen-2026-10-16/viewer/binding.json` |2801|`d140df47b076474e75a55689ae3ea88c028b150e660007d143aea7983d8f17ba`|
