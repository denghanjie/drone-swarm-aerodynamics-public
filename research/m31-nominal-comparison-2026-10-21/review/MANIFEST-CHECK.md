# Independent source-manifest coverage check

21 October 2026. Package: `research/m31-nominal-comparison-2026-10-21`.

**Disposition: PASS for local manifest identity, reviewed-source preservation and dependency/input coverage.** This completes the independent manifest condition in `review/PROTOCOL-REVIEW.md`. Exact-public source verification and its publication receipt are separate launch prerequisites; this reviewer did not perform that network verification. No allocation outcome is asserted.

This note is an authorized result-only review artifact outside the frozen source manifest. No frozen source, prior result, failure, lock or receipt was edited. The check used byte/hash verification, static dependency inspection and metadata comparison only. No scientific module, initializer, controller, simulation, native query, journal decompression or trajectory analysis, audit, finalizer or browser was executed.

## Frozen identity

| Item | Independently checked value |
| --- | --- |
| Manifest | `research/m31-nominal-comparison-2026-10-21/source-manifest.json` |
| Schema | `m31-nominal-comparison-source-v1` |
| Unique file pins | 67 |
| Total pinned file bytes | 159,554,495 |
| Manifest bytes | 13,583 |
| Manifest SHA-256 | `9e4b37c33ad679c9d1b035a238f7a042226a09667815ba1b3d42ab07ef271bab` |
| Matching source commit | `f90d17f2b3cad19752f538040efc36893c64c3fc` |

All 67 pinned files match their recorded lengths and SHA-256 values. Paths are safe repository-relative paths, unique and free of symlink traversal. The manifest's exact saved bytes match the manifest in the stated Git commit. This local object comparison is not evidence that a remote endpoint serves those bytes.

All 17 candidate identities recorded in the prospective review remain unchanged. The review itself is pinned unchanged at 16,036 bytes, SHA-256 `584ec2f959a227904e99397440954db8685bf4f606f410a82a67413cd0718e2c`. The final independent auditor and contract are included at their reviewed identities: `source/audit.py`, 59,287 bytes, SHA-256 `9db7b2f7d77d2af5ca8d99a9e22f0964e553b92040bdeb4800ca2e4774206301`; `AUDIT-CONTRACT.md`, 16,594 bytes, SHA-256 `beee6819534419a82eb36d51a797899500708f4a920236cc4ef666152f37629f`.

## Input and provenance coverage

- The four original `.part000` inputs match both the descent input descriptors and the original public result manifest, with offset zero. They were verified as complete compressed byte inputs, without decompression or record analysis.
- Required original and continuation indexes, audits, replay exports, exits, supervisors, closure files, result manifests and publication receipts are present. Their identities are bound to the prior public manifests and receipts inspected during this check.
- The continuation storage qualification, its supervisor and the inherited Journal source are included and match their prior public identities.
- The descent input descriptor is bound to the published descent result manifest and receipt.
- `OrbitControls.js`, `three.module.js` and `three.core.js` match the prior public vendor pins.
- `PRIVACY-SOURCE.md` is included and consistent with the source-only scope. This does not replace privacy review of later generated logs, screenshots or results.

The reused original result manifest remains the 100-pin manifest at SHA-256 `a8fe6543894d1e5ddf3165d2b250304ef2d8c462f4e37f236b781312e02b974b`; the continuation result manifest remains the 157-pin manifest at SHA-256 `90edf4045db10a216daa287763928ea4fa6a73997d6050b65783c64d25df2a81`. Reuse of their prior audits is preserved as an explicit trust boundary, not a new audit of those trajectories.

## Producer dependency closure and runtime

Static traversal of literal CommonJS dependencies from the new producer reaches the following 12 files. All are manifest-covered; the ten inherited files are unchanged and bound to prior public manifests. No native solver module appears in this producer dependency closure.

```text
research/m31-boids-continuation-2026-10-20/source/journal.cjs
research/m31-boids-continuation-2026-10-20/source/motion.cjs
research/m31-coupled-stage-qualification-2026-10-17/source/adapter.cjs
research/m31-native-fresh-transfer-2026-10-17/source/vendor/generation/milestone-31-source/factory-wide.cjs
research/m31-native-fresh-transfer-2026-10-17/source/vendor/generation/milestone-31-source/factory.cjs
research/m31-native-fresh-transfer-2026-10-17/source/vendor/generation/milestone-31-source/geometry.cjs
research/m31-native-fresh-transfer-2026-10-17/source/vendor/generation/milestone-31-source/grid.cjs
research/m31-native-fresh-transfer-2026-10-17/source/vendor/generation/milestone-31-source/sim.cjs
research/m31-native-fresh-transfer-2026-10-17/source/vendor/generation/milestone-31-source/wall-filter.cjs
research/m31-native-fresh-transfer-2026-10-17/source/vendor/generation/step02c-source/physics.cjs
research/m31-nominal-comparison-2026-10-21/source/gate.cjs
research/m31-nominal-comparison-2026-10-21/source/run.cjs
```

The existing Node executable's bytes match both prior runtime metadata identities: 121,304,480 bytes, SHA-256 `d0c6c74401e6a544bb4d4b2a9ded9c43298d4e6dcd5ebac4dd010c4c81774105`. This was a byte check, not a scientific execution. Runtime metadata and browser/system dependency disclosures remain subject to the limits in `SOURCE-REUSE.md`; no hermetic operating-system or browser closure is claimed.

The source acceptance remains conditional on the separate exact-public source receipt before launch. After any authorized allocation, saved-result review, phase-closure checks, privacy/display inspection and exact-public result verification remain required. This check supplies no permission to rerun or reopen an allocation.
