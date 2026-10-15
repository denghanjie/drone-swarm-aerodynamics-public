# Kiran RSS 2025 physical-validation target: follow-up audit

Audit date: 15 October 2026; public metadata/landing-page checks performed approximately 15:21–15:23 UTC. Scope: public metadata, paper and sensor documentation, plus read-only inspection of M28 source. No raw observations were saved, no model was run, and no author contact, payment or challenge bypass was attempted.

**Decision:** a real, publicly registered experimental dataset has been verified, but a usable, measurement-matched quantitative validation target for the unchanged 27 g M28 model has **not yet been secured**. The obstacles are specific: Brown serves a human-verification page to this client; DataCite does not supply file/schema/reuse metadata; force/moment calibration and exported conventions remain unverified; and the published geometry and actuation differ from M28. This is not evidence that no public dataset exists.

## Access and reuse evidence

| Checked resource | Observed response | What it establishes |
|---|---|---|
| [DataCite DOI API](https://api.datacite.org/dois/10.26300/64d4-wa17) | HTTP 200; JSON; 2,904 bytes | DOI `10.26300/64d4-wa17`, title *Force, Moment, and Velocity Dataset for Quadrotor Downwash*, creators Anoop Kiran, Nora Ayanian, Kenneth Breuer, publisher Brown University, year 2025, resource type Dataset. |
| [Brown landing page](https://repository.library.brown.edu/studio/item/bdr:rnnfmt6u/) | HTTP 200; HTML; 1,669 bytes; title “Verification required”; human-verification/Cloudflare Turnstile page | The registered URL responds, but this response contains no dataset file manifest or observations. HTTP 200 is not successful data acquisition. |
| [RSS publication page](https://www.roboticsproceedings.org/rss21/p102.html) and [paper HTML](https://arxiv.org/html/2507.09463v1) | Publication identity and experimental methods available | *Influence of Static and Dynamic Downwash Interactions on Multi-Quadrotor Systems*, RSS 2025, DOI `10.15607/RSS.2025.XXI.102`. |

The DataCite record has empty `rightsList`, `descriptions`, `sizes`, `formats`, `relatedIdentifiers` and `dates`; `contentUrl` and `version` are null. Empty rights metadata does **not** establish that the dataset is unlicensed or unavailable for reuse: a license could exist on the inaccessible landing page or in its files. The paper is CC BY 4.0, which does not by itself license the dataset.

**Filenames, extensions, file formats, sizes, checksums, columns, row structure, sample timestamps, repetition identifiers and raw units are unverified.** Do not label these files CSV or MAT without inspecting a manifest. No dataset download URL was established. The web reader also could not access the DOI/API/landing resource; the successful direct metadata request above provides the current access evidence. No alternative undocumented endpoint was used to bypass verification.

## What the experiment measures

The paper's §II-A describes two Crazyflies attached to ATI Nano17 six-axis force/torque transducers on an x–z translation system with 100 μm positioning accuracy. Both receive a tethered **4 V DC supply at commanded hover PWM**. Nominal rotation is approximately 320 Hz, but the authors explicitly distinguish constant voltage from constant rotational frequency. Neither “constant RPM” nor a flight controller restoring hover is an equivalent actuation condition. The exact numerical PWM setting, propeller identification and complete motor configuration were not established from the inspected text.

Force/torque sampling is 20 kHz for 30 seconds per case with three repetitions. The PIV and force measurements are separate experiment sets. PIV uses a plane through the two front rotor centers, 1,000 image pairs over approximately 70 seconds; it cannot automatically be compared with a body-center radial velocity cut. These descriptions establish experimental design, not the contents of a retrieved data file. [Paper, §II](https://arxiv.org/html/2507.09463v1)

For static loads, §III-A gives weight **W ≈ 0.265 N** and center-to-motor radial arm **l = 32.5 mm**. Thrust is normalized by W and pitch moment M_y by Wl. Thus Wl ≈ 0.0086125 N·m (8.6125 N·mm), an arithmetic normalization derived from the reported approximate scales. It is not a new measurement. The raw sensor/export units, pitch sign, sensor-to-body transformation, exact moment reference point and tare/bias procedure remain unverified. Net thrust must also be distinguished from an incremental interaction load; any subtraction requires a matched isolated baseline and compatible signs. [Paper, §III-A](https://arxiv.org/html/2507.09463v1)

Do not fit to the isolated percentage statement at separation 4l: the body reports thrust at about 65% of nominal while the conclusion describes a 65–70% reduction. That textual inconsistency needs resolution from actual observations, not a guessed correction.

## Sensor uncertainty: identified instrument, unresolved load accuracy

The paper reports a PIV velocity uncertainty of 0.6 mm/s from its displacement-error calculation. This is **not** force or moment uncertainty. Text searches for calibration and tare did not establish a force/torque calibration matrix, sensor serial/calibration range, calibration certificate, uncertainty budget, drift or cross-talk correction.

The [ATI Nano17 manufacturer page](https://www.ati-ia.com/products/ft/ft_models.aspx?id=Nano17) lists several calibration ranges. SI-12-0.12 has Fxy/Fz ranges of 12/17 N and torque range 120 N·mm, with nominal resolutions 1/320 N and 1/64 N·mm. SI-25-0.25 and SI-50-0.5 have different ranges and coarser resolutions. The site says resolution depends on the system/calibration/filtering and directs customers to obtain accuracy information separately. Its traceability statements do not identify the calibration used in this experiment.

**Catalog resolution is not experimental measurement accuracy.** Do not use the finest catalog resolution as this study's error bar or invent a numerical acceptance tolerance. Repeat variability, if eventually recovered, also would not capture all systematic calibration error.

## Compatibility with M28

Direct source inspection confirms the existing model configuration:

- `outputs/milestone-28-source/aero.cjs:3–4` imports `outputs/step02c-source/physics.cjs` and sets rotor radius 23 mm.
- `outputs/step02c-source/physics.cjs:3–4` sets mass 0.027 kg and rotor coordinates (±0.028, ±0.028) m. Its radial arm is therefore 39.598 mm, approximately **21.8% larger** than the experiment's 32.5 mm. Opposite-motor spacing is 79.196 mm; it must not be confused with radial arm length or adjacent-motor spacing.
- `outputs/step02c-source/physics.cjs:17–18` defines motor states as thrusts and makes them follow thrust commands with a 0.04 s time constant. M28 retains this motor-state update in `aero.cjs:18`.
- `aero.cjs:8–9` supplies an ideal constant-induced-power receiver response; it is not a calibrated voltage/PWM–RPM–load response. Its wake strength is based on isolated hover weight, not a self-consistent solution of each source rotor's current effective thrust.

Matching approximately 27 g mass is insufficient. Rescaling only separation by l cannot establish similarity of different rotor geometry, rotor size or electrical/motor response. A defensible comparison requires an explicitly separate, documented measurement-matched vehicle/setup configuration and justified actuation/receiver response. Preserve the existing M28 identity; do not silently replace its constants and call the result validation of unchanged M28. The experiment's rigid support and moment convention also need matching.

## Independent holdout and permitted next step

The reported three repetitions could support repeatability estimates once run identifiers are available. They do not establish an independent holdout: random rows from the same 30-second recording are correlated, and the accessible metadata provides no split. A prospective split should reserve complete separation/offset/configuration cases (and relevant repetitions) before fitting. Static versus dynamic cases may be a useful separate generalization test only after their setup and file identities are verified. Parameters fitted to these same observations or paper curves cannot then be described as independently validated on them.

The present evidence supports a **paper-level qualitative and dimensional compatibility check**, not a numerical force/moment validation score. To advance, obtain accessible versioned files and reuse terms, a manifest/schema, geometry and actuation metadata, calibration/convention information and matched isolated baselines. Then freeze case-level holdouts and implement a separately identified measurement-matched comparison. Report errors in N, N·m and m/s with documented uncertainty before adding normalized scores. Pair-interaction data would still not validate arbitrary multi-vehicle wake overlap, turbulent fluctuations or 5,000-drone flight.
