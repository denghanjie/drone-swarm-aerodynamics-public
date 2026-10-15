# Prospective neighborhood-ratio screen

NOT ADOPTED, 2026-10-15. No collection or predictions until root adoption and independent review. New observation protocol after a failed pilot, not a passed nearest-marker test.

## Frozen change and evidence

The pilot stopped at target 11 on overlapping distance bounds, before ratios or predictions. Preserve evidence-freeze.json (SHA256 fd0c462a38aa82589492472dc881ede6fe43bc1ff9f0eb34566af577922f70bd).

Reuse the certified pilot target-8 anchor without rereading. Replace the four remaining single-marker targets by neighborhoods at 11,14,17,20, each +/-0.75 in z/l. The estimand changes to one anchor and four marker sets.

## Inclusion without forced uniqueness

Include EVERY centerline marker whose coordinate interval intersects a neighborhood, including touching endpoints. Record identities/actual coordinates. Flag partial eligibility and retain FULL intervals without clipping. The target-11 competitor crossing 11.75 must be retained. Do not filter by nearestness or model agreement. If none lies wholly within a window, retain a possible empty-set outcome.

Record series identity and orange/purple overlap. Use orange centerline pixels only; hidden orange markers stop collection. Never substitute purple maxima or the dashed fit, even where the paper says curves merge. No anchor optimization. Stop for unreadable identity, missing calibration, nonpositive anchor lower bound, negative response lower bound, or any selected interval crossing the exact 2.5lambda model floor. Preserve such failures, not replacements.

## Collection and freeze

Reuse the figure/provenance, frozen calibration and pixel bounds from pilot PLAN f3407c35e2840151b3fcade06f21d569cb4185d324851bc2dd6340782e0a82a0. No recalibration or reduced bounds. Reuse completed reads; obtain two reads per new marker in one pass without predictions.

Freeze decisions, flags, coordinates, bounds and hashes. Max 15 markers including anchor; stop on excess or a marker in multiple neighborhoods.

## Conditional evaluation and limits

After extraction review, use unchanged kernel, nominal lambda=2sqrt(2), eta=1, pilot monotonicity proof and ratio bounds. At most 45 scalar calls: center/endpoints per marker.

Report each candidate's coordinate-matched ratio difference interval, then union/hull these paired residual intervals per neighborhood. Never pool observed/model ratios across coordinates or choose the best-fitting candidate. Retain shared anchor/calibration dependence; hull overlap is not joint agreement, a confidence interval or independent replication.

Unknown experimental/plane uncertainty remains. Conditional shape only; no amplitude validation or statistical pass/fail.

## Budget and stopping

Cap: 1,000,000 retained bytes including referenced evidence; one collection and one evaluation pass. No paid compute, installation, repository data, public figure redistribution or new experiments. Stop after report or failed gate.
