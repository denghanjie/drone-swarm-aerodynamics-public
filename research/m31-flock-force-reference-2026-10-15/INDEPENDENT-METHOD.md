# Independent full-flock static field implementation

Prepared source: `m31-flock-force-independent.cjs`.

SHA-256: `4e1e31c00184f3dc82db8c040f5ba79313c724881d30b7c1581ddb26488270ee`.

Size: 15,787 bytes. Starting reviewed independent source SHA-256: `e0445be31ec647c8ddfb79533d4866dc8133e99ba5f25061bf393aab6bc58baf`.

This implementation follows the selected reference-only design in `/tmp/m31-flock-force-design.md`. Preparation involved source reads, text edits, byte comparisons, and hashing only. The JavaScript module was not imported, executed, syntax-run, or evaluated; no fixture, pose, geometry, field, root, force, integration, or timing calculation was performed. No repository file was edited. Execution requires the new campaign's own reviewed source freeze.

## What changed and what stayed identical

Only the field API/implementation and descriptive provenance/header were extended. Static byte comparisons confirmed that the complete source suffix beginning at `receiverSolution`—including `effectiveThrust`, `idealPower`, `rotorWrench`, `receiverWrench`, `loads`, and exports—is unchanged. `rotate`, `fade`, `normalizedWake`, physical constants, mode constants, input validation, `DomainError`, and the dot-product helper are also byte-identical to the reviewed source.

The module imports nothing. Explicit matrix rotation, direct deterministic source enumeration, independent factored fades/wake arithmetic, numerical bisection brackets, ideal-power identity, and nominal-yaw preservation retain their established semantics and limitations. The inherited bracket collapse on a rounded zero polynomial residual remains a numerical diagnostic, not a certified root enclosure.

## API contract

`fields(states, 'sum-rotor', {onReceiver, guard})` accepts the original 17-number finite state layout. This new field extension intentionally supports **only `sum-rotor`**. Other field modes throw, even though the inherited mode list and scalar/load helpers retain their original compatibility semantics. No center-sample field is implemented.

Returned fields are:

- `winds`: ordinary independent inflows, array of N four-element arrays.
- `compensatedWinds`: simultaneous Neumaier totals in the same shape.
- `maximumInflow`: maximum of the **ordinary** inflows, including zeros.
- `candidates`: total eligible ordered source-center pairs.
- `contributions`: total retained-support source/receiving-rotor terms, including zero-projection code6 terms.
- `centerChecks`: every nonself source-center check, N(N−1) on complete return.
- `rotorVisits`: eligible source/receiving-rotor geometry visits, four per eligible center pair on complete return.

Both hooks are optional synchronous functions. If supplied with a non-function type, they are rejected before field work. Hook errors propagate unchanged; the caller owns comparison, persistence, and stopping policy. No promise/asynchronous callback contract is provided.

`guard(context)` is called at each receiver's start, before its all-source scan, and after that receiver's four rotor sums have completed, before `onReceiver`. Its context is exactly `{receiver, centerChecks, rotorVisits, candidates, contributions}`, with **cumulative counts for the current field call**. The pre-loop finite/tilt preparation is not separately guarded; the caller's external supervisor governs that work. These are receiver-boundary checks, not live per-instruction limits.

`onReceiver(record)` is called once after a complete receiver, in ascending receiver order. Its record contains:

- `receiver` index.
- `codes`, a complete `Uint8Array(4*N)` indexed `4*source+receivingRotor`.
- `counts`, a plain eight-element code-count array summing to 4N, including self/outside-center zeros.
- `axis`, a copied three-element receiver axis.
- `worldrotors`, four copied three-element world rotor centers.
- `winds` and `compensatedWinds`, copied four-element arrays.
- `centerChecks` and `rotorVisits`, **per-receiver** counts, N−1 and 4×eligible on completion.
- `eligible`, that receiver's number of eligible source centers.
- `contributions`, that receiver's retained-support terms, equal to counts[6]+counts[7].

The copied axis/wind/world-rotor arrays prevent callback mutation of those arrays from corrupting subsequent field computation or returned inflows. Code/count buffers belong to that completed receiver and are not reused. Input states must remain unchanged during the call. The callback may compare/write evidence, but the field module never calls any receiver root or load helper while dispatching it.

## One field pass, complete codes, preserved branch order

Source IDs are enumerated directly in ascending order for every receiver. The strict center-distance<3 m test occurs once per nonself source. Eligible IDs remain ascending, and each receiving rotor sums source terms in that same order. Receiver rotor positions are computed once each and reused for their classification and wake term; there is no separate domain-geometry pass.

Every eligible source/rotor visit increments the visit counter before evaluating its branch. The complete byte vector preserves the domain codes: 0=self/outside center, 1=down≤0, 2=down≥2.5 m, 3=near-invalid, 4=near-skipped, 5=far radial cutoff, 6=retained geometry with zero projection, 7=retained positive projection. Near-wake checks precede far radial support and projection, and the original strict/non-strict inequalities remain unchanged. Complete vectors/counts are suitable for comparison to the pinned saved-domain evidence.

Code3 throws immediately, as the actual field model requires. The `DomainError.detail` retains receiver/source/rotor, code, downstream/radial values, both 17-state inputs, receiver rotor point, source axis, cumulative work counters, local receiver counters, eligible count, and explicitly partial receiver code counts. The offending rotor visit and all center checks already performed are counted. No callback claims that incomplete receiver as complete.

The original global axis-Z tilt gate runs before any pair work. A tilt `DomainError` retains the offending receiver/drone, its axis/state, null source/rotor (no pair exists at that gate), and zero pair/rotor/contribution counters. No quaternion is normalized or repaired.

## Ordinary and Neumaier inflows

For each retained code6/7 term, the inherited binary64 wake term `speed` is evaluated once. The ordinary running sum uses the exact same ascending-source addition as before. For old sum s, term x, and rounded t=s+x, the simultaneous correction accumulates `(s−t)+x` when |s|≥|x|, otherwise `(x−t)+s`; the ordinary sum becomes t. The compensated output is s+correction. The ordinary output remains the declared comparator; no result-dependent choice between sums is implemented. No-contributor sums remain exact zero. Code6 still evaluates/counts its zero-projection term, matching the production contribution counter.

The driver should call exported `receiverSolution` exactly once per receiving rotor, then assemble wrenches from the returned thrusts. Calling inherited `receiverWrench` or `loads` in addition would solve roots again; those helpers remain exported for compatibility, but the selected driver must not use them to duplicate its counted root work. The module itself performs zero receiver solves during `fields`.

## Interpretation

The planned pinned domain counts imply 107,972,000 independent center checks and 37,514,240 independent eligible rotor visits across the twelve snapshots; these are expectations from saved evidence, not measurements produced by this unexecuted module. The independent direct scan and production Grid do different work. No timing ratio, center-approximation result, continuous-flight claim, novelty, physical validity, or force-error acceptance is established here.
