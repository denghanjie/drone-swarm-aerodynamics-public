# What does our source wake actually represent?

This checkpoint audits the source model before further optimization. It asks whether changing the source motors changes the computed field, how much of a stated profile its cutoffs remove, and what a small published asymmetric-rotor comparison can legitimately tell us.

The [protocol](PROTOCOL.md) separates a numerical implementation witness, mathematical profile accounting and descriptive reproduction of published numbers. None is a physical validation of our 27 g vehicle. The [derivation](literature/DERIVATION.md) and [source ledger](literature/LEDGER.md) explain why a squared-speed integral must not automatically be called measured thrust. We will not tune the model to force that integral to equal vehicle weight.

The scientific sources were published and frozen before the single new CPU invocation at commit `b515ac7a0b146ebf337431fb492d145d9a43c619`. Previous GPU/browser campaigns remain terminal and unchanged. The original eight-step research structure is retained: this is work on Steps 2–4, the physical-model/reference requirements that must support later approximation and scaling claims.

The completed witness gave exactly **2.5241780354649195 m/s in all 20 calls**, despite five different source motor arrays. This confirms direct motor-state insensitivity in the extracted field function at the fixed tested geometry. It does not describe a physical motor shutdown. The radial fade retains **97.13664384% of a squared-speed proxy**; downstream fading removes the remaining field by 2.5 m. The proxy is not measured thrust. No coefficient was tuned and no replacement source law was validated.

The producer's numerical gates passed. An independent saved-data review passed **46/46 checks**, including a different quadrature method, all 410 profile samples and the published-number arithmetic. This review inspected existing results and is not a blind physical confirmation. Timing scopes remain unreconciled and support no performance claim.

The [plain-language summary](MILESTONE-SUMMARY.md), [claim ledger](CLAIM-EVIDENCE-LEDGER.md), [raw result](results/result.json), [motor-state witness](results/witness-stdout.json), [independent review](review/SAVED-DATA-ACCEPTANCE.md) and [reproduction instructions](REPRODUCE.md) preserve the complete scope. The [Three.js view](viewer/) displays the saved profiles in 3D and links the historical local Boids replay. It is an interactive static evidence view, not a new fluid or flock simulation. The final display check passed 99 checks; both preceding failed attempts remain in [QA records](QA-REPORT.md).

**Next decision:** define a source actuation/flow relationship with a suitable measurement reference before using motor responsiveness to claim physical mutual coupling. The two inspected articles did not establish a compatible reusable raw dataset. A prescribed-hover source remains usable as an explicitly limited numerical benchmark. Physical validation, the complete 5,000-drone target and a publication-worthy contribution remain unresolved.

Source and result bytes are recorded in `freeze.json` and `manifest.json`; public sanitization is documented in `PRIVACY-REVIEW.md`. Result publication is verified separately by the receipt in `../publication-receipts/m31-source-accounting-2026-10-16.json` once available.
