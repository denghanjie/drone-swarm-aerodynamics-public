# Exact spatial-neighbor baseline: source-only planning audit

2026-10-16. Recommendation: compare the complete all-pairs coupled query with one
conservative uniform-grid implementation that preserves the current guarded
pair contract. Use a sufficient whole-scene bounding-box certificate before
omitting far center pairs, and retain a complete all-pairs fallback. Charge the
certificate, grid build, candidate sorting, CSR/graph construction, root solves
and residuals to the complete-query cost. No target positions, pair values,
timings, model execution or new numerical fixtures were evaluated for this note.

## Inspected source and established method

The historical `outputs/milestone-26-source/grid.cjs` is a Map of integer-cell
string keys to source-ID arrays. Insertion visits IDs in ascending order.
`candidates` gathers all cells intersecting an axis-aligned radius box and then
numerically sorts all gathered IDs. `neighbors` removes self and retains the
strict predicate `Math.hypot(...) < r`. Its default cell size is 1.8 m;
`outputs/milestone-28-source/aero.cjs` explicitly instantiates it at 1.5 m. [S1,S2]

This supplies a real implementation baseline, not a new algorithm. It does not
contain the current center-invalid guards, a safe-coordinate/grid-index
certificate, explicit floating-boundary padding, or fixed-occupancy overflow
handling. Its existing equality evidence on earlier workloads is useful history,
not proof for every later guarded contract. Do not call its `neighbors` directly
and assign symbol 1 to every unvisited pair under the new contract.

Uniform-grid neighbor enumeration is established prior work. Green, *Particle
Simulation using CUDA*, revision 1.3, May 10, 2010, printed pp. 4–7, describes
uniform grids and atomic/sorting constructions. The repository's verified ledger
and access log record actual primary-source reading of those pages. The atomic
example's fixed-capacity clamping must not be copied as a complete dense-cell
policy. This note relies on that previously verified reading; it did not retrieve
or reread the PDF. [L1,L2] CPU grid indexing, source-ID sorting, conservative
enumeration and fallback are engineering adaptations of known methods. Neither
algorithmic originality nor CUDA/WebGPU performance follows.

## Preserve the exact center and rotor contract

For each nonself directed pair, the canonical order is:

1. Form `dx = p_j.x - p_i.x`, and similarly dy,dz, from the original stored world
   coordinates, and evaluate the original `Math.hypot(dx,dy,dz)`.
2. If the norm is nonfinite, greater than 512, or any absolute coordinate
   difference is greater than 257, classify all four rotor entries as symbol 11.
3. Only then classify center distance >= 3 as symbol 1. Strictly smaller center
   distance invokes the unchanged pairTerm four times with
   `centerAlreadyEligible=true`.

Self stays symbol 1. Inside the retained center neighborhood all displacement,
downstream, radial, near-field, projection and speed guards remain unchanged.
In particular, none of the rotor-level guards is discharged by a center box.
The candidate source IDs must ascend before four-row coefficient accumulation;
cell traversal order is not an acceptable replacement. [S3]

The problem with an unconditional radius grid is semantic, not just numerical:
a far pair with a coordinate difference over 257 is symbol 11, even though its
distance exceeds 3. Omitting it as symbol 1 erases an admission failure.

## Sufficient bounding-box certificate and explicit fallback

In a prospective implementation, scan all positions once to obtain finite
per-axis minima m and maxima M. Form the binary64 spans `s = M - m`. Admit the
grid fast path only if every position and span is finite, every span is
nonnegative, and each span is <= 256 m. Record the extrema, spans and decision.
This is a sufficient numerical domain check, not a newly imposed physical
admission rule or a claim about the selected snapshots.

For any original pair, monotonic correctly rounded subtraction bounds its
rounded coordinate differences by the rounded extreme span. Thus each is at
most 256, below the 257 guard. The exact Euclidean bound on those rounded
components is `sqrt(3)*256`, and `3*256^2 < 512^2`, with ample numerical margin.
All center norms are finite and below 512 under the intended binary64 norm
semantics. No guard threshold is accepted at an ulp-sized margin. The grid may
therefore omit far pairs only on this certified path. The source's unchanged
center calculation is still used for every gathered candidate.

**If the certificate fails, do the original complete directed-center loop.**
Do not conclude that the snapshot itself is invalid from certificate failure:
the box condition is deliberately sufficient, not necessary. Do not select a
replacement snapshot, loosen the box after seeing the result, or call a failed
certificate an acceleration success. Preserve fallback status and its full cost.
Nonfinite positions never enter binning. A false certificate due to an arithmetic
or safe-index check likewise selects the fallback, with its cause recorded.

A more general per-block validity certificate could avoid some fallback work,
but it changes the baseline and proof burden. It should not be added reactively
to rescue this first fixed comparison.

## Conservative floating-boundary enumeration

Use local coordinates **only to index cells**: `u_i = fl(p_i - m)`. On the
certified path these lie in [0,256]. Keep original positions unchanged for all
actual center and rotor arithmetic. In particular, do not replace
`source - (receiver + rotorOffset)` with a regrouped translated expression.

A simple prespecified baseline uses dyadic cell width h = 4 m and stores source
j at `floor(u_j/h)` on each axis. Division by four avoids the extra rounding of
a non-dyadic cell width; cell indices are small safe integers. For receiver i,
enumerate the inclusive integer rectangle

```text
lo[k] = floor((u_i[k] - 3)/4) - 1
hi[k] = floor((u_i[k] + 3)/4) + 1
```

The extra full cell on each side is a conservative coverage halo. At these
bounded local magnitudes, subtraction/addition rounding is many orders of
magnitude smaller than a 4 m cell. A truly near source that is moved across a
query-box/cell boundary by rounding can change the relevant floor by at most
one cell, which the halo covers. A conservative binary64 bookkeeping bound on
the small number of local transform/query operations is below 2^-40 m; the
padding is a cell, not that tiny bound. It intentionally gathers false positives.
There are at most five queried indices per axis (125 cells), and stored cell
indices lie between 0 and 64. An alternative 27-cell design may be possible, but
is unnecessary for this conservative baseline and should not be chosen after
observing target timing.

Gather each occupied cell once. Each source belongs to one cell, so source IDs
are unique. Numerically sort the gathered IDs ascending, skip self, then apply
the exact original guard and `Math.hypot < 3` predicate. The halo changes only
which pairs get examined; it never changes the 3 m support or the final branch
comparison. Do not substitute squared distance, add a radius epsilon, remove
the original guard, or change arithmetic signs/grouping as part of this arm.

This reasoning assumes the intended IEEE binary64 arithmetic and ordinary
finite norm semantics; ECMAScript Math.hypot is not an outward-rounded interval
primitive. Therefore qualify the implementation prospectively against the actual
all-pairs runtime predicate, including cell boundaries and distance boundaries,
and retain any mismatch as failure. This note is not an executed coverage test
or a formal proof of a particular JavaScript engine's math library.

Suggested future qualification cases, to freeze before execution: exact and
adjacent representable values around 3 m; exact cell boundaries and either side;
negative and signed-zero coordinates; common large translations with small
extent; duplicate centers; near-field rejection inside the neighborhood; dense
single-cell occupancy; spans at 256 and immediately outside; coordinate-difference
guard witnesses above 257; nonfinite and overflowing spans forcing fallback.
No such fixture is run by this planning task.

## Construction, ordering, storage and whole-query costs

Let C_i be the gathered candidate count, B the directed center-eligible count,
M the positive rotor coefficient count, and E the unique vehicle-edge count.
None has been measured here. An exact finite-radius model may still be dense:
C_i can be N, B can be N(N-1), and four-rotor work can remain quadratic.

| Stage | Work and storage to include |
|---|---|
| Input preparation | Decode/copy as required by the estimand; finite checks, bounding-box scan, geometry/quaternion/rotor preparation; no free reuse of earlier scientific outputs. |
| Grid build | N local-coordinate transforms, cell keys and insertions; Map/bucket metadata and all N stored source IDs; temporary arrays and allocation costs. No cell occupancy clamp or top-k truncation. |
| Query enumeration | Up to 125 cell lookups per receiver, gathered-ID copies, self checks; scratch memory O(max C_i) if streamed receiver by receiver. Charge string-key construction if the implementation uses it. |
| Ordering | Numeric gather-sort cost roughly sum C_i log C_i and its allocation cost. Buckets have ascending IDs already, so a bounded-way merge is a possible later established alternative, not a free change to the first arm. |
| Exact center filter | Actual guarded Math.hypot calls for gathered nonself candidates; certificate implies skipped far pairs cannot be invalid. Fallback incurs the complete directed census. |
| Retained geometry | Exactly four pairTerm calls per eligible directed center; unchanged branch behavior, K, per-rotor source order and rejection counts. |
| Sparse assembly | Offsets, source IDs, K and reconstructed a; growth buffers/copies, unique dependency recovery, rank/order/depth checks. Typical typed CSR payload: 4(4N+1)+12M bytes before a and graph storage. |
| Coupled solution | Direct solve, required Picard comparator, all four roots, every update, separate final maps/residuals and convergence/work records; same stopping/root algorithms in both geometry arms. |
| Output/evidence | All required checksums/consumption, retained results, serialization/compression and writes according to the declared estimand; benchmark and audit storage kept distinct. |

If full `[N,N,4]` symbol tensors remain required, their initialization/emission
and raw storage remain O(N^2), even when most entries are implicit symbol 1 in
the traversal. A streamed compressor can reduce peak resident memory, but cannot
be silently counted as zero work. If the new campaign instead permits a sparse
or implicit-default classification representation, freeze that changed output
contract and independently reconstruct equivalence; it does not retroactively
alter the previous campaign.

Likewise, reporting `directedCenterTests=N*(N-1)` after skipping most actual
distance calls would confuse logical coverage with executed work. Record
logical directed pairs, box-certified skipped pairs, gathered candidates,
actual center-distance calls, eligible centers and pairTerm calls separately.
Report box/total classification coverage and the fallback reason. Do not infer
elapsed savings from a reduced Math.hypot count.

For a cold complete frozen-pose query, rebuild the grid, geometry, CSR and graph
within each measured query. A solve-only reuse measurement answers a separate
question: retain and charge the setup once, report resident bytes, and explicitly
state any amortization count. Reusing fixed K/CSR over Picard iterations within
one query is natural; borrowing the previous campaign's saved K/CSR outside the
timed query is not a complete-query baseline. Pose updates, cache invalidation,
control/integration, rendering, GPU transfers and synchronization remain outside
any claim unless separately included and measured.

The historical Map grid and the conservative guarded grid differ in cell size,
binning frame and halo, so describe the new arm accurately. It is a conservative
adaptation, not an instruction-identical rerun of historical Grid.neighbors.
No favorable timing or asymptotic density assumption has been established.

## Sources, exact inspected bytes, and limits

Working-tree HEAD observed during this source audit:
`455d14f4eba6cda4252847c0f4ffdb75b6028b7d`. File hashes, not assumptions about a
moving branch, identify the inspected material:

- **S1:** `outputs/milestone-26-source/grid.cjs`, lines 2–6; SHA256
  `f06010781770b64432935e5d825bcd1405b154b735ac4d0d654f145600cea302`.
- **S2:** `outputs/milestone-28-source/aero.cjs`, lines 10–16; SHA256
  `710b0a8f0df62208e3385ac9b8288240b379fe9248a1a645251a77c533f24a62`.
- **S3:** `research/m31-swarm-coupling-transfer-2026-10-16/source/reference-excerpt.cjs`,
  especially lines 5–14; SHA256
  `ec71562d17db5b30497e2953adc75019c424c19a44e45b22fcbb3a4482096d1e`.
- **L1:** `research/m31-restart-2026-10-15/literature/annotated-ledger.md`, C2 row
  and C2 findings; SHA256
  `c54fe9b943c76e2d146289ea6a655d1bec52b334ff72a0d4d59880f1e2cf0b37`.
- **L2:** same literature directory, `source-access-log.md`, C2 successful-text
  row and scope limitations; SHA256
  `d26d6fe7ea805831a9d3fbd1106e2f3f5e0b4f02fe926ba333752164afdd3377`.
- **Previously verified primary source:** Simon Green, *Particle Simulation using
  CUDA*, revision 1.3, May 10, 2010, printed pp. 4–7:
  <https://developer.download.nvidia.com/assets/cuda/files/particles.pdf>.

Also read current source/report context in the closed exact-zero campaign; it
does not supply a timing prediction for coupled-load queries. No new external
source, literature novelty conclusion, benchmark permission, target computation
or follow-up experiment is allocated by this note.
