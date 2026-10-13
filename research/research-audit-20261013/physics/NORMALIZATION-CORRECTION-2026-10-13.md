# Normalization correction before experiment execution

Checked 2026-10-13. No experiment or figure digitization was executed. The proposed `5 < z/l < 6.5` profile-falsification screen is withdrawn: it is outside the model's declared far-field domain under a well-supported interpretation of the paper's geometry.

## Evidence and reconciliation

[Kiran et al., arXiv v1](https://arxiv.org/html/2507.09463v1#S3.SS1), III-A, describes l = 32.5 mm as the horizontal center-to-motor distance. That prose alone does not distinguish a planar radial distance from its side-view x-projection. On inspected PDF page 3, Fig. 3 draws l along x from the centerline to the visible motor. Page 4, Fig. 4 shows the X-layout and a PIV plane through the front rotor pair. III-A also associates lateral displacement 2l with left/right rotor alignment. [III-B1](https://arxiv.org/html/2507.09463v1#S3.SS2.SSS1) equates z/l = 6.5 with approximately 2.3 motor-to-motor distances.

Let D denote the opposite-motor distance used by [Bauersfeld Fig. 2 and Eq. (8)](https://arxiv.org/html/2403.13321v3#S3.F2), avoiding the different meanings of l in the two papers.

Two geometric readings must be distinguished:

- Radial-arm reading: rotor centers have radius l, so D = 2l. Then z/l = 6.5 gives z/D = 3.25, inconsistent with the stated approximately 2.3 conversion.
- Projected-half-side reading: rotor centers are (±l, ±l), so the arm radius is √2 l and D = 2√2 l. Then 6.5/(2√2) = 2.2981, matching the conversion. The rotor-alignment description is consistent too.

The second reading reconciles the figures and arithmetic and is better supported. This is an interpretation of the published diagram/text, not independent validation of the physical vehicle dimensions. The prose remains ambiguous; the audit must not present 32.5 mm as a definitively verified radial arm length. Raw geometry/calibration metadata or explicit author clarification would close that ambiguity.

## Consequence for the proposed screen

The inherited model starts at z/D = 2.5. Its lower bound in paper coordinates is therefore:

- z/l = 5 under the radial-arm reading;
- z/l = 5√2 = 7.0710678119 under the projected-half-side reading.

The originally selected interval, 5 < z/l < 6.5, does not satisfy both mappings and is entirely below the latter bound. There is no eligible point in the original window under the conservative applicability gate. A near-field shape disagreement there cannot be called an in-domain falsification of this model.

The screen is stopped at the applicability gate, with no scientific outcome or experiment ID. We will not move the window after inspecting curves to preserve a desired rejection. Any later physical comparison must be a newly frozen protocol, mapping coordinates and PIV plane explicitly and requiring every selected location to be inside the domain under every unresolved mapping, including extraction uncertainty. The present audit does not initiate that replacement.

## Correction to previous audit statements

My previous audit treated 32.5 mm as an established radial arm length and proposed the five-to-six-and-a-half interval. That interpretation was insufficiently checked and is superseded. The previous comparison of the repository's radial arm 39.6 mm with a supposed physical radial arm 32.5 mm is also withdrawn. Under the better-supported projected reading, compare coordinate half-widths 28 mm and 32.5 mm, or radial arms about 39.60 mm and 45.96 mm, respectively. The second vehicle dimensions remain inferred, not independently measured here.

The literal numerical l scale still exists in the paper, but physical geometry, moment arms and measurement-plane offsets must not be silently equated with it. This also strengthens the input gate for the deferred raw static-force proposal.

## Retained evidence

- Consulted Kiran PDF SHA-256: `791db3db03f1c3b00198cab068a6709944bc137850596639f8de88da844fb3ce`.
- Consulted Bauersfeld PDF SHA-256: `81987dfd1cf2980270defd9447a9e5fb6c1586eab77b75b730de127c932d373c`.
- Original proposal and metadata files remain in the local pre-correction history. A clearly labeled [superseded proposal](PROSPECTIVE-PHYSICS-SCREEN.superseded-2026-10-13.md) preserves the full proposed procedure for review.
- Bibliography, ledger, access notes and distribution manifest are updated with this correction. No frozen numerical source or campaign records changed.
- The publisher PDF was located, but its web screenshot extraction failed. The visual checks above used the already-hashed arXiv PDF; no claim of publisher-PDF byte equivalence is added.
