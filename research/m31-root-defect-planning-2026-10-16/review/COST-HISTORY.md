# Root-defect proposal: bounded history and cost screen

Source-only independent review, 2026-10-16. This note inspects exactly **eight distinct local content files**, including the two planning documents. It performs no scientific execution, imports, calculations, target-array reads, rescoring, benchmark, external retrieval or numerical allocation. Repeated reads and filename discovery do not add content sources. All previous allocations remain closed.

## Finding and recommendation

The proposed polynomial-defect enclosure for **arbitrary candidate rotor roots**, followed by signed body-load interval propagation, is not explicitly implemented or reported as tested in the bounded inspected history. The earlier global log-space contraction and force-error reasoning are already present and must remain credited as inherited. This is a bounded source finding, not an exhaustive repository search, a literature novelty claim, or an independent endorsement of the new mathematical derivation.

Requiring the complete **current** coefficient set leaves the measured large-query construction problem unresolved. I recommend current-geometry/coefficient work as the next performance priority. A separately frozen endpoint certificate qualification could still advance correctness knowledge: it could test whether an implemented enclosure is valid and useful for a finite set of arbitrary candidates. That would be supporting error-control work, not evidence that the 5,000-drone real-time objective has advanced computationally. It should not displace the construction-cost question or be framed as a demonstrated cheap monitor.

## Exact inspected inventory

| # | Repository-relative path | Evidence used |
|---|---|---|
| 1 | `research/m31-root-defect-planning-2026-10-16/PROSPECTIVE-SCOPE.md` | Current desk-only scope and cost restrictions; lines 5–13. |
| 2 | `research/m31-root-defect-planning-2026-10-16/DERIVATION-DRAFT.md` | Proposed arbitrary-root enclosure, body-load propagation and unimplemented arithmetic conditions; lines 15–70. |
| 3 | `research/m31-coupled-solve-2026-10-16/review/CONTRACT-CHALLENGE.md` | Existing exact fixed-coefficient contraction and recomputed-root force guarantees; sections beginning at lines 71 and 103. |
| 4 | `research/m31-coupled-cost-host-2026-10-16/MILESTONE-SUMMARY.md` | Published complete-query and cached-phase findings; lines 16–20. |
| 5 | `research/m31-coupled-cost-host-2026-10-16/source/kernel.cjs` | Full source read; geometry/scaling at lines 49–83, cubic evaluation at line 9, map/residual at lines 87–106, query/cached boundaries at lines 110–111. |
| 6 | `research/m31-typed-assembly-2026-10-16/MILESTONE-SUMMARY.md` | Published complete-query scope, timings and negative storage result; lines 5–13 and 23. |
| 7 | `research/m31-typed-assembly-2026-10-16/source/kernel.cjs` | Full source read; current preparation/assembly/scaling at lines 14–29 and 76–196; delegated solve/residual and complete-query wrapper at lines 199–209. |
| 8 | `research/m31-root-secant-2026-10-16/NEXT-QUESTION.md` | Closed prior allocation and requirement that a new monitor connect to actual load error and include its own cost; lines 3–9. |

No linked raw evidence, analysis arrays, imported helper, anchor source or additional summary was opened. In particular, the typed kernel's `anchor-kernel.cjs` dependency was not separately inspected; this note does not claim its byte identity with another file.

## What already exists, and what is distinct

The coupled-solve challenge already establishes the global `1/2` contraction of the exact fixed-coefficient map in log coordinates. It gives `D <= 2 (computed_r_log + eta_logF)` when map-evaluation error is certified. It also derives the `1`-Lipschitz log-root relation and a multiplicative bound for forces **recomputed** from provisional source amplitudes. Its final per-rotor paragraph explicitly cautions that a cubic residual alone is not automatically a force or log-error bound and requires inner-root error control. The draft must not present these inherited results as newly established.

The inspected host kernel makes the distinction concrete. `residual(q, solution)` calls `map(q, solution.y, ...)` to construct `residualMap`. `nodeMap` forms each sparse `alpha` and calls `root(alpha, ...)`, which performs bisection. The returned residual is the log distance between `solution.y` and the new map state, plus a source/receiver mismatch. It does not form a polynomial defect of `solution.rotors` or an arbitrary external rotor vector. Changing only stored candidate rotor values would not make this routine check those values. The cubic polynomial comparison inside `root` is part of root solving, not the proposed arbitrary-root/body-load certificate.

The typed kernel introduces storage and assembly variants and delegates solver/residual calls to its anchor. No polynomial-defect enclosure or signed body-load interval propagation is implemented in that inspected file. Its published milestone reports coefficient/load equivalence and residual checks, not qualification of the new enclosure.

The proposed additional bridge is therefore specific: construct source amplitudes from the candidate roots and current motors; evaluate the candidate polynomial with current coefficients; translate that defect through the inherited contraction/root sensitivity into intervals for the arbitrary candidate's rotor errors; then propagate signed thrust intervals to body force and moments. The draft states that no such reference or candidate has been implemented or run. The earlier proof already supplies substantial ingredients, so this is a proposed derived certificate, not evidence of a new contraction theorem or a literature contribution.

## Published cost evidence and its limits

The host milestone reports that geometry construction occupied **96.3–97.6% of aggregate B time on its 5,000-drone states**. B is that experiment's grid/ordered complete-query implementation. The reported phase includes candidate enumeration, sorting, exact pair evaluation and sparse assembly; it does not isolate an internal operation. The same summary reports grid/ordered complete queries of **621–1,023 ms**, direct all-pairs diagnostic queries of **517–587 ms**, and cached ordered solve plus residual of **17.77–18.29 ms**. Cached timings exclude matrix construction, schedule creation and changing poses. These are published aggregate statements, not newly calculated values.

The host source places candidate/pair classification and sparse coefficient assembly in construction, scales coefficients from current nominal motors, then performs solve and residual work. The proposed root-free check removes neither the obligation to obtain current admitted coefficients nor the sparse weighted source pass. Avoiding cubic root calls is an algebraic distinction; its timing benefit and interval-arithmetic cost are unmeasured here.

The later typed milestone reports that every query includes fresh construction, scaling, ordering, solve, residual checks and output consumption. Its two 5,000-drone L medians are **476.51 ms** and **473.71 ms**; T medians are **478.96 ms** and **476.92 ms**. It concludes that typed storage added no qualifying improvement beyond lean ordinary storage and that queries still took roughly half a second, excluding flight, steering, rendering and transport. Its source still prepares current poses, enumerates directed candidates, classifies current rotor interactions, assembles coefficients and scales them before delegated solving/checking.

The host B phase percentage must **not** be transferred to L or T. The inspected typed summary gives no corresponding phase percentage, and this review does not estimate one. Nor does this review infer a new maximum speedup, an arithmetic-based runtime bound, or a time for a prospective certificate. The public evidence establishes an unresolved current-construction burden and an unresolved real-time objective; it does not establish exactly how much a new implementation could save.

## What a subsequent checkpoint could legitimately answer

A narrowly allocated endpoint certificate test could answer whether a carefully implemented outward enclosure contains the modeled current rotor/body-load error, how often it is informative under predeclared thresholds, and what its complete current-coefficient evaluation costs. It would need an independent reference and explicit treatment of current motors, support/admission, numerical invalidity and floating arithmetic. Passing it would establish neither stale-geometry safety, intermediate-time control, controlled-trajectory accuracy, physical validation nor real-time flight.

For the computational goal, prioritize a distinct, justified treatment of current geometry/coefficient evaluation. If reuse or incremental updates are proposed, their ownership, support changes, admission and approximation error need their own argument and qualification. The existing certificate cannot make an old matrix current by assumption. The root-secant `NEXT-QUESTION.md` supports this separation: a new error indicator needs a new causal definition and bounded protocol, and its cost must accompany its load-error guarantee. This recommendation creates no execution allocation and reopens no prior experiment.
