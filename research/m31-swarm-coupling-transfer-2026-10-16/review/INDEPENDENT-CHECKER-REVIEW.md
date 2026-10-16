# Independent swarm saved-record checker: source review

Prepared prospectively on 2026-10-16. This checker has only been read and parsed
with Python's AST parser. It has not been imported or executed, no numerical
fixtures have been evaluated, and no selected target states have been read here.
The coordinator controls the frozen source publication, remote manifest check,
exclusive invocation lock, and separately authorized once-only reviewer run.

Interface after freeze:

```text
python source/independent-check.py PACKAGE_PATH OUTPUT_JSON
```

The Python/NumPy implementation does not import or invoke candidate JavaScript.
It reconstructs quaternion axes and historical rotor offsets from the saved
17-component input rows without normalization or force replacement. It evaluates
the entire receiver/source/rotor symbol census in receiver-sized chunks, including
all rejected snapshots. Every symbol is compared exactly; every positive sparse
support row and coefficient is compared, with the frozen 2e-12 absolute plus
2e-12 relative coefficient tolerance. Compression/decoded hashes, binary shapes,
sizes, encodings, fixed case selection, completed case copies, and declared
geometry work are checked. The original historical JSON remains outside the
package: original identity/hash/size metadata is checked against the prospective
extractor's fixed published pins, while
the separately frozen extractor and manifest provide original provenance.

Independent input, nominal-force, near-field, invalid-term, scaled-cap,
ordinary-Lmax and graph records are reconstructed. Invalid nominal forces never
enter the square-root/division scaling path; unavailable scaled diagnostics stay
null. Geometry census continues. The graph is deduplicated per receiver; the
height-descending/id-tie order must be topological. Strict height violations are
reported separately. Root dependency depth is zero. The numerical tilt count is
not treated as an exact-real theorem certificate.

Only admitted and topologically eligible snapshots with successful preceding case
comparisons and an existing saved solution enter the load solver. A missing
required solution still fails the audit. The
review uses a distinct hyperbolic positive-cubic root formula, a descending solve
with normalized original nominal-force weights, and independently reconstructed
coefficients. Every saved Picard update, final generating rotor record, and
separate residual map is checked. All returned forces and source amplitudes are
compared to the independent descending result with 1e-9 relative tolerance.
Stopping, iteration caps, root closures, the specified 56 bisection-loop work per
numerically positive alpha, positive-term multiplications, residuals and source/receiver
consistency are audited. Saved work counters are checked for consistency with the
specified algorithm; an output record alone cannot prove internal loop execution.

Output contains `pass`, `checkCount`, `passedChecks`, `errors`, per-case `cases`,
individual `checks`, elapsed time and `reviewMethod`. A scientifically rejected
snapshot may pass the record audit when the complete rejection census agrees;
that does not turn it into an admitted solve. Exceptions preserve prior completed
comparisons and a failed case record. Output creation is exclusive. The checker
has cooperative 230-second and 1.5-GiB RSS guards; the runner's external 240-second
wall limit is authoritative. Candidate artifact byte/term caps are checked:
255 MiB for normal science and 256 MiB including failure records. Only the known
supervisor/reviewer bookkeeping names and the current review output are excluded;
unexpected other result payloads count against the science allocation. Exception
messages redact the local package root. Relative comparisons retain their maximum
observed relative error when finite. Under the prospective diagnostic convention,
nonfinite scalar error/tilt maxima, scaled-cap maxima and ordinary bounds encode
as null while admission failure/counts remain explicit. This convention does not
apply to K, a, alpha, source amplitudes or rotor solution values: those must remain
finite, and nonfinite a is rejected before the independent load solve begins.

Residual numerical limits: independently expressed floating arithmetic can differ
from JavaScript at hard geometric boundaries. Exact-symbol differences remain
failures; no epsilon reclassification or target-driven adjustment is allowed.
The review is a numerical consistency check of a frozen-pose, assumed-power load
contract on historical airflow-off states. It is not outward-rounded arithmetic,
new held-out evidence, coupled-flight validation, physical validation, or a timing
or scaling benchmark. No target execution or follow-up campaign is authorized by
this source review alone.
