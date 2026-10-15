# Quantization-gate decision

2026-10-15 UTC. Decision: make a narrow prospective amendment; do not report the frozen gate as passed. No marker values, predictions or residuals were inspected for this decision.

Reviewed PLAN.md SHA256 c2ca80c01e18deb314e7a2425c747b49c13cdb3469d1a25c88720f9fe8a1a497 requires confirmation of coordinate decimal quantization <=0.001 SVG unit. A short decimal can be an exact published coordinate or a rounded export. Trailing zeros do not identify the historical exporter resolution. Newly rounding an analysis coordinate to 0.001 proves only the newly introduced rounding bound; it cannot verify the original gate.

Preserve the current collection attempt as stopped before data-marker extraction, with this gate unverified. This is a protocol limitation, not a negative physical result. Keep the frozen plan unchanged and separately adopt a short amendment before resuming collection. No outcome-driven selection has occurred, so a documented before-data amendment remains scientifically defensible.

Recommended replacement: treat published SVG decimal strings as exact rational coordinates; propagate the verified transform chain; independently verify floating arithmetic error <=1e-6 SVG unit and the two-parse agreement gate. Retain the same source hash, series, windows, shared calibration and fixed nominal parameters. Prefer no extra quantization. If rounding is deliberately retained, freeze one rule and account for its <=0.0005 SVG-unit shift before collection, without claiming this bounds pre-export values.

Describe +/-0.01 SVG unit as a preselected graphical sensitivity envelope around published coordinates. It does not bound historical export rounding, author symbol placement or experimental uncertainty. All remain unknown. Independent extraction review and separate root model-evaluation release still apply.
