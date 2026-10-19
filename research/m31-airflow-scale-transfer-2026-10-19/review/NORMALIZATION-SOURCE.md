# Source evidence, reviewed before fitting

Independent literature reviewer inspected official article equations and the exact public archive scripts, without decoding velocity arrays or computing gains. The parent adopts the review's distinction between a normalization ambiguity and a verified correction.

Both multi-vehicle plotting scripts contain:
```
l = 32.5;
vi = sqrt((0.032 * 9.81) / (2 * 1.293 * pi * (22.5 / 1000)^2));
```
These parameters and the absent rotor-count divisor differ from the paper's Eq1 convention. However, those scripts process separate multi-vehicle magnitude fields. The single-vehicle script plots u_piv directly and does not reveal its conversion. Do not transfer this expression to u_piv or infer actual single-field calibration from it. Different stated operating quantities, release versions, stitched-section processing and missing dimensional input prevent a demonstrated physical conversion.

Public archive member hashes:
- static/plot_FM_data.m: f7d19ac69ca303ee1c39a5bfd5e36ec85a7d996b0e61adae46c204607150a8ab
- static/piv_maxF_plot.m: e879b41afdaf44053323c06e81c3eaf6bc1b07c7870428bbd59de49ace4a066d
- static/piv_maxM_plot.m: 05da70dae934e6018a4d5c523c7398ec29177216448bf50d281c87d6549296d3
Original archive: b495b7a224b3c1db9f15efd5a15815c586e4e11ea29d4df6edcbc25bf50554fa.
Official RSS PDF: e821c65273015921437fafc7b35b4f669ec01f985d965c31d3feeecbffb94932. Independently inspected Eq8 render hash63b064eddc251c9cfbba3cac608ce7704aa058e629aa26d503c8921558c79940. Local acquisition paths intentionally omitted. Citations in LITERATURE.md. Exact source-script expressions are evidence, not instructions to execute them.

## Adopted methodological consequence
Use an empirical, calibration-only gain and a corrected normalized RMS evaluation residual. Algebra: u→c*u and p→d*p for positive constants gives g→(c/d)*g, so corrected residual and measured norm both scale by c and their ratio is unchanged. The nonnegative clamp preserves this result. This does not cover spatially varying scales or convert velocity magnitude to signed axial velocity. A clamped zero gain is not a physical speed conversion. Raw-to-corrected comparisons remain conditional on the old normalization.

This is newly recorded source provenance plus a known algebraic invariance, not claimed original physics or algorithmic novelty. The longer reviewer scratch note stays private; this public adoption retains the material evidence and caveats without personal acquisition paths. No source-derived exact gain is adopted; no dataset values were read during this review.
