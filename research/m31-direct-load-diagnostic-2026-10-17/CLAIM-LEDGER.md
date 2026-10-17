# Claim–evidence ledger

All numerical claims are conditional on the supplied prepared-word model and six exposed snapshots, not real flight measurements. Source commit ee342fe5cdd824cbd68e4c1c85bae9f83bf688bf; [source manifest](source-manifest.json); [raw proposals](results/analyze.json); [independent check](results/check.json); [saved analysis](analysis/summary.json). Reference interval widths are retained; no population confidence estimate is claimed for dependent reused snapshots.

| Claim | Status within scope | Evidence and limit |
|---|---|---|
| Full native control reproduces strict normalized load accuracy | Supported on all six | Full A and B pass all categories at1e-8; does not certify historical JS bit equivalence |
| Fixed weakest-tenth deletion preserves strict accuracy | Contradicted on all six | Omission A is definite-fail at1e-8 in every state |
| Fixed weakest-tenth deletion preserves stress-tier accuracy in every state | Contradicted | A0 and B0 definitely fail1e-2; four other states pass. No pooled average overrides these failures |
| The certificate alone explains all omission rejection | Contradicted | Direct load errors fail even stress at both starting states |
| The existing certificate can reject a directly verified stress-tier accurate candidate | Supported on two states | A5 and B5 direct A passes while B/C are not-certified; this is certificate insufficiency, not observed force error |
| Discarding omitted lower bounds necessarily loosens this certificate | Contradicted on this panel | All 1,536 B/C local factors and root boxes, all six global K and error intervals agree exactly; contraction intervals need not agree |
| The prospective tL*U>=1 condition explains every equal row | Not established and unnecessary | Condition counts217,221,232,213,218,224 of256, respectively; all256 local factors per state agree. Condition is sufficient only |
| The procedure passes independent saved-data verification | Supported by checker and independent postrun audit |29 fixtures,13 intended corruption failures; counts and file bindings retained. Validity does not imply scientific success |
| Runtime saving, browser/5000-drone feasibility, online Q-current, physical validity or novelty | Unresolved/not tested | Oracle coefficients already paid; no practical selector, new flight, hardware data or relevant new-prior-art comparison |

Decision: retain accepted exact baseline, close this fixed deletion route, do not tune its mask/fraction in this allocation. Future approximations need a new protocol and fresh confirmation after development; these data remain exposed. No physical tolerance was adopted or relaxed.
