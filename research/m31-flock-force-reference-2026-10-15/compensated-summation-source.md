# Verified provenance: Neumaier compensated summation

Verified 15 October 2026. This note is for freezing the provenance of an arithmetic diagnostic before the static full-flock checkpoint. No scientific computation, model execution, contact or paid access was performed.

## Publication and access

**Arnold Neumaier (1974), “Rundungsfehleranalyse einiger Verfahren zur Summation endlicher Summen,” Zeitschrift für Angewandte Mathematik und Mechanik (ZAMM), 54(1), 39–51. DOI: [10.1002/zamm.19740540106](https://doi.org/10.1002/zamm.19740540106).**

The [publisher record](https://onlinelibrary.wiley.com/doi/abs/10.1002/zamm.19740540106) verifies title, A. Neumaier, year, journal, volume, issue, pages and DOI. The author's [publication list, entry N1](https://arnold-neumaier.at/publist.html) independently identifies the article and links its [public scan](https://arnold-neumaier.at/scan/01.pdf).

The current author-hosted scan returned HTTP 200, `application/pdf`, 1,094,943 bytes; 13 pages. SHA-256: `ecdf42add97c73f1d858d2987d701f9560073dc310a149a230c6d3af11348d38`. Temporary local copy: `/tmp/m31-neumaier-1974.pdf`. It has no extractable text; rendered pages were read visually. The older university URL `https://www.mat.univie.ac.at/~neum/scan/01.pdf` returned HTTP 404. Full text was obtained from the author, so no fallback secondary citation is needed. The source PDF was not added to the repository.

## Algorithm actually read

Printed p. 40 (PDF page 2), §2 IV, equation **(IV,1)**, presents the improved Kahan–Babuška procedure. In modern variable names, preserving its grouping:

```text
s = 0
c = 0
for each input x, in the declared order:
    t = s + x
    if abs(s) >= abs(x):
        c = c + (x + (s - t))
    else:
        c = c + (s + (x - t))
    s = t
return s + c
```

Each operation is a floating-point operation; the correction is accumulated separately and added at the end. This is the magnitude-branch method commonly called Neumaier compensated summation, not the different Kahan feedback recurrence.

Printed p. 45 (PDF page 7), §6, explicitly conditions its analysis on assumptions 1–5. Equations **(IV,8)–(IV,10)** retain both final rounding error and a weighted sum of residual errors. The paper therefore supplies error analysis, not an assertion that this recurrence always produces the exact sum or the correctly rounded exact sum.

## Meaning for the proposed checkpoint

These are application limits, not additional results attributed to the paper:

- Use this published method alongside an independently implemented ordinary sum of the same nonnegative contribution terms, with input order and binary64 evaluation specified. Preserve parentheses and branch behavior; do not algebraically simplify the residual expression.
- Report the ordinary-versus-compensated discrepancy as an **observed arithmetic diagnostic**. That discrepancy is not a certified upper bound on either result's error. Agreement does not rule out shared mistakes in geometry, contribution evaluation or enumeration.
- Nonnegative terms avoid cancellation in their exact sum; this does not eliminate floating-point rounding, overflow/underflow or errors already present in each computed term. Check finite outputs and keep those concerns separate from summation.
- Neither result is an exact-arithmetic oracle, an interval enclosure, a formal rounding certificate, physical ground truth, or evidence that a truncated spatial approximation is accurate. A correctly rounded claim would require additional verified machinery and assumptions that this checkpoint has not established.
- This is established numerical-analysis prior art. Using it adds an arithmetic cross-check, not a new aerodynamic or summation method. No result or tolerance is inferred before running the separately frozen checkpoint.

Suggested report wording: “We computed both ordinary and Neumaier-compensated positive sums at fixed states to diagnose sensitivity to floating-point accumulation. Their discrepancy is observational; no certified rounding or physical-accuracy claim follows.”
