# GWS transfer: final interpretation scrutiny

2026-10-16. This review used only the public `PROTOCOL.md` and
`results/aggregate.json` in `research/m31-gws-receiver-transfer-2026-10-16`.
The aggregate records source commit
`ffec6dccee9def5acc473cd907417d09533bc636`.
No raw target or private row evidence was read, no prediction or comparison was
recomputed, and no new source was acquired. This is interpretation scrutiny, not
independent arithmetic certification. The note contains only public aggregate
information and prospective scientific reasoning.

## Verdict and recommended wording

The proposed conclusion is supported within its stated descriptive scope.
“Does not reproduce exactly” is accurate but less informative than reporting the
declared discrepancy and its conditioning explicitly:

> In this exposed GWS run, the transferred ideal-power law plus the nominal-RPM
> baseline bridge gives an RMS CT discrepancy of 0.03195, or 0.519 times its static
> baseline CT, across all 14 reported conditions. The predeclared secondary
> summary for the nine reported-positive-thrust conditions is 0.01269 in CT,
> or 0.206 times baseline CT. Discrepancy is therefore not confined to the five
> reported nonpositive-thrust conditions. It persists for each of the three
> specified baseline choices. These are descriptive coefficient discrepancies,
> without a statistical rejection or practical-adequacy verdict.

These values are rounded from the saved aggregate, not newly calculated here.
The secondary result complements the full-run primary result; it must not replace
the primary headline or erase the five nonpositive rows.

## Interpretive limits that matter

- **Baseline normalization:** RMS/C0 is a fraction of static baseline CT, not
  mean pointwise percentage error, thrust error in newtons, a force uncertainty
  estimate or a flight-performance error. The full and secondary RMS average
  different sets and counts; their difference is not an additive decomposition
  of error attributable to nonpositive rows.
- **Three specified substitutions:** the positive-thrust secondary RMS/C0 values
  are approximately 0.2061 for the interpolated baseline, 0.2059 for the lower
  anchor and 0.2130 for the higher anchor. This supports persistence under these
  choices, not robustness to a quantified distribution of baseline uncertainty.
  Changing C0 changes predictions and the reporting denominator. Preserve
  absolute CT discrepancies alongside normalized ones and do not rank candidate
  baselines by the normalized score alone.
- **Conditioned secondary:** membership is determined by reported CT > 0 and was
  declared before scoring the exposed run. It is a descriptive subgroup, not a
  new holdout or proof of a physically validated operating regime. Sign
  uncertainty near zero is not quantified here.
- **Representable branch:** the five reported nonpositive conditions are retained
  in the primary result. Their incompatibility with a positive-root prediction
  is a known representational limitation of this full-run transfer. It does not
  independently falsify the equation under its original ideal-power condition.
- **Direction:** the aggregate's signed mean discrepancies are positive under
  the declared prediction-minus-report sign, so “overpredicts on average in this
  comparison” is supported. The aggregate does not establish that every row is
  overpredicted; avoid that stronger statement without row-level scrutiny.
- **Control and scope:** neither the residuals nor their persistence demonstrate
  that fixed RPM maintains ideal actuator-disk power. The data cannot isolate
  equation error from the nominal-RPM bridge, specimen association, baseline
  mismatch or measurement effects. Small root residuals establish numerical
  reconstruction, not physical accuracy. No novelty, direct 46 mm/nanoquad
  validation, transient response, nonuniform-wake response or swarm result follows.

## One next scientifically informative decision

**Close this exposed transfer as development evidence and prioritize a defined
physical control-to-f0 bridge for the intended receiver before another validation
score.** Do not spend the next experiment tuning this run's baseline or inventing
a shaft-power efficiency that improves its fit.

The next finite physical question should be the frozen receiver law **plus an
explicit fixed-command bridge**: for one identified rotor/drive and one documented
real command c, establish its zero-external-inflow baseline independently, freeze
`f0 = T0(c)`, and compare direct steady thrust at two predeclared nonzero imposed
axial inflows while holding that same command. The actual control and geometry
must be specified; radius alone does not identify the propeller/drive. Neither
fixed RPM nor fixed shaft power may silently stand in for this declared bridge.

This is a small zero-plus-two-inflow design. The minimum independent target is
measured thrust with known external inflow, a matched baseline, documented control
and adequate measurement uncertainty. RPM, torque, voltage and current are useful
diagnostics if available; a comprehensive power/drive dataset is not required
before the combined hypothesis can be tested. RPM may change under the fixed
command. Do not control P* using the measured target thrust or recalibrate f0 at
each inflow, because either would defeat the independent transfer question.

Prefer an independent compatible reference selected before target inspection.
If the necessary bridge/evidence cannot be admitted, leave the current receiver
physically unqualified rather than promote this GWS comparison into its place.
Any discrepancy in that next experiment would still initially challenge the law
and bridge together; extra diagnostics would be needed to attribute the cause.

This decision does not authorize acquisition or execution. Source mapping,
receiver moments and nonuniform wake reception, aggregation, temporal dynamics,
local control and measured browser/WebGPU costs remain separate parts of the full
5,000-drone accuracy/computation objective.
