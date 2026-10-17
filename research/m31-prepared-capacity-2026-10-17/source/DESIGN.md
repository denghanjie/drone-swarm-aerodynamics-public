# Prepared-reference capacity pilot: source design

This source-only driver proposes one fixed, three-case allocation. It does not
authorize execution. The parent owns protocol, source freeze, public receipt and
launch; the independent reviewer inspects this source before launch. No old
scientific source, input or result is edited. This document and `run.py` are the
only files authored by this implementation task. No commit is made by this task.

## Exact allocation and inherited recipe

The fixed order is `fresh-a-t5` (64 drones), `dense-180-filter-cost` (180), then
`sparse-180-filter-cost` (180). Each gets exactly one
`prepared-reference.regenerate_scene` invocation, with standard-library cProfile
enabled around that invocation. There are no unprofiled repeats, no new input
generation, no new full-oracle calls, no native/browser run and no rerun of any
control. A failure stops the remaining scientific calls and is preserved as an
incomplete negative allocation; it does not grant a replacement allocation.
The prescribed suffix counts are exactly 7,408 / 34,707 / 3,340 and positive
counts 228 / 3,056 / 0. Total suffix calls must be 45,455 and logical pairs
273,888. The 60,000 ceiling does not replace these exact expected counts.

The 24-case prepared-reference qualification and its passing saved-evidence
audit are prerequisites, including their manifest membership. The new manifest
must contain all members of that earlier source manifest, all 24 saved result
pins, the exact prepared index, saved-audit result, audit-source manifest and
audit source. The three new calls do not replace or recalculate those controls.
The predecessor result manifest and its separate public receipt are pinned and
must match commit `1ce0f3bff31ae5c296fd7ab711bcc5949bf297bd`, manifest SHA256
`3bb348f971327ec84b0e942968a3872397f30e70edf8c24171fdb0cc86071418`, its complete
pin count and successful committed/remote byte verification.

The driver imports only the already qualified frozen pair, semantic, tree and
prepared modules after source/publication/runtime/prerequisite gates. Their
four expected SHA256 values are hardcoded in `MODULE_PINS` and must agree with
the new verified source manifest. It additionally requires the filter-cost
pair/semantic source hashes to equal the reused fresh-transfer source hashes.
The complete non-scene settings of the saved filter-cost spec and reused spec
must be identical. Explicit checks preserve `maxDrones=180`, `leafCapacity=8`,
`referenceCoefficientBits=192`, `referenceSourceBits=192`,
`referenceRootBisections=128` and producer `fractionBits=96`. The frozen tree
retains its own checks, including the unchanged 2,000,000 positive-term cap.

Fresh-a uses its saved raw-word input encoding. The 180-drone cases use the
original decimal states from the saved filter-cost spec, preserving the
original preparation route. No rounded output is recycled as a decimal input.
The emitted full raw-word input must exactly equal the saved producer scene,
including order, and the stable-ID maps are also checked explicitly.

## Preserved evidence and exact comparisons

`wire` is a literal source-text copy of the prior prepared driver's function.
Every completed call emits the complete input/prepared/global decision/tree,
all residual scalar statuses and branches, all positive 192-bit rational
coefficient intervals, every root and signed-load interval, and compact exact
coverage evidence. The complete record and complete profile are written in
exclusive-create mode before any outcome comparison or counter assertion.
An exception therefore does not discard an already returned scientific record
or overwrite an earlier result. If a call itself raises, no complete target
was returned; the partial cProfile data, event start and allocation failure are
retained where the hard closure and byte budgets permit.

Fresh-a must be structurally identical to its complete saved prepared wire.
This includes all coefficient endpoints, roots, signed loads, coverage and
branches. For each 180-drone case, the required comparisons are:

1. Exact scene identity and saved raw-input digest binding; exact raw-word list
   and stable-ID raw map equality with the saved producer scene.
2. Exact stable-ID prepared-word map equality with both the saved `hierarchy`
   and `filtered` producer methods.
3. Exact stable-ID equality of every root and every signed rotor, collective,
   force and moment box with the saved `independentReference`. These saved
   independent records explicitly declare 192-bit coefficient/source arithmetic
   and 128 root bisections. Equality compares the canonical rational wire, with
   no floating conversion or tolerance.
   Both producer methods must retain their certified/admitted result. Their
   schema has candidate rows but no saved solve traversal order, so a direct
   saved-order comparison is explicitly marked unavailable.
4. Exact positive-support identity against both saved producer methods.
   Producer receiver/source array indices are translated through the complete
   saved stable-ID list. Duplicate support keys or nonpositive entries in an
   admitted producer method fail. The saved 96-bit coefficient maps must also
   be exactly equal between those two producer methods.
5. Each new 192-bit positive interval must be contained in the corresponding
   saved 96-bit producer interval by exact `Fraction` inequalities, with no
   tolerance. The old independent record contains no pair-coefficient table,
   so independent-192 pair equality is explicitly marked unavailable. This
   containment check is not described as that unavailable comparison.

All three calls must be admitted, must retain full logical-pair coverage, and
must show exactly one preparation and validation per drone, two operand
lookups per suffix call, and zero pair preparations. The shared suffix budget
is incremented by the unchanged prepared adapter immediately before each
suffix call. Its hard allocation limit is 60,000, shared across all three
calls. No producer filter is imported or used for scientific decisions.

## Profile, outer wall phases and memory interpretation

Each call uses a new `cProfile.Profile` with the standard default timer. The
profiler is enabled only for the one `regenerate_scene` invocation and disabled
in a `finally` block. All cProfile function records and all caller edges are
serialized to JSON; there is no top-N truncation. Each record preserves the
primitive/total call counts, own time, cumulative time and raw pstats caller
tuple fields. Function IDs link caller edges without combining records that
happen to share a basename. Repository source filenames are repository-relative;
absolute runtime/library filenames are reduced to basenames. Private absolute
paths are not emitted. Cumulative values overlap and must not be summed as
disjoint stages. Profiler overhead is retained; no subtraction or calibration
run is performed.
The CPython cProfile source defines caller tuples in the order total calls,
primitive calls, own seconds, cumulative seconds; the JSON preserves that
order explicitly, distinct from the function-row tuple's first two fields.

Separate outer monotonic wall measurements cover module/constant setup, input
and baseline loading, each profiled regenerate call, profile serialization and
writing, full reference serialization and writing, exact saved comparison and
accounting, and closure verification. These are observed phases of this fixed
ordered pilot, not an estimate of unprofiled production performance. The
allocation's outer wall also includes administrative overhead not assigned to
a phase. The saved `wallSeconds` observation ends after closure verification,
before final index serialization and stdout; it is explicitly not a completed
process wall measurement. No old and new timing ratio is used for a speed claim.

Memory fields use macOS `resource.getrusage(resource.RUSAGE_SELF).ru_maxrss`, in
bytes. The runtime gate requires `sys.platform == 'darwin'` to keep that unit
unambiguous. Before-case, after-call, after-case and final readings are process-
lifetime peaks; they are not a per-stage allocation, per-scene isolated peak,
memory delta or enforced OS limit. Prior input loading, earlier cases,
serialization and closure may contribute to the final peak.
The final RSS observation is sampled through closure before final index
serialization; the record does not claim a later process-exit measurement.

## Gates, hard budgets and separate pilot hurdle

The new source manifest identity is supplied on the command line. The pinned
Python executable bytes, SHA256, complete version string, isolated mode and
disabled bytecode writing must match. The parent-written source-publication
receipt must identify the same commit/manifest, successful remote and committed
byte verification, and all manifest pins. The receipt's timezone-aware UTC
timestamp must precede launch and reserve at least 600 seconds before
2026-10-17 03:00 UTC. The same 600-second reservation is checked before and after
source/prerequisite verification. No scientific module is imported beforehand.

The allocation is single-use: an existing `STARTED.json` or results directory
blocks launch. Scientific work has a 540-second signal/poll limit. Closure has
at most 60 additional seconds, never beyond 600 total seconds. Final closure
rechecks all source pins, every saved evidence file and the event journal.
One absolute closure deadline is created before partial-profile preservation
when regeneration raises, or on normal entry to outer closure. Outer closure
reuses that deadline and cannot grant a second 60 seconds. The closure signal
repeats after expiry so catching its exception cannot leave preservation with
no active timer. A timeout can prevent even a final index write; retained
STARTED, journal, records and profiles remain the partial allocation evidence.
Failure clears complete/qualified flags. Per-file output is limited to 32 MiB;
aggregate newly generated evidence, including STARTED and journal, is limited
to 256 MiB. Existing files are never overwritten. Containment here is the
in-process signal and polling mechanism only; no external process guardian or
hard OS memory containment is implemented or claimed.

Accuracy qualification is separate from the observed practical capacity hurdle.
The hurdle requires all three exact comparisons to complete, each profiled
regenerate wall time to be at most 60 seconds, and final process-lifetime peak
RSS to be at most 1 GiB (1,073,741,824 bytes). This is an observed pilot hurdle,
not an OS memory cap or a production speed guarantee. Exceeding the hurdle
does not erase exact scientific equality or trigger a rerun. The index has
three explicit outcomes:

- `accuracy-unqualified-or-incomplete`;
- `accuracy-qualified-capacity-hurdle-failed`;
- `accuracy-qualified-capacity-hurdle-passed`.

`qualified` is the accuracy flag for compatibility with earlier records;
`accuracyQualified`, `capacityHurdlePassed` and `outcome` make the distinction
explicit. Exit zero means complete accuracy qualification; the separate hurdle
must be read from its explicit field. Physical validation, 5,000-drone strict
qualification, coupled flight, novelty and a performance claim remain false.

## Source-only validation

The implementation task parses the new Python source with `ast`, compares the
literal `wire` function text with the qualified prior driver, and inspects
saved JSON schemas and source text. It does not import this driver, any
scientific module, or execute any scene. The reviewer and parent must review
the frozen final bytes and manifest before a separately authorized launch.
