# Enablement protocol review

Conclusion: **no blocker found in the enablement delta**. The reviewed change enables the already-reviewed single N1000 state protocol for the newly approved two-hour window. It does not change scientific scope, source implementation, budgets, controls, record structure or acceptance criteria. The enabled execution manifest and exact public-source verification remain required before the single launch.

This review was performed by `m31_protocol_challenge` using read-only Git object inspection, text reads, file hashes and JSON/time metadata comparisons. No project source was imported or executed. No initializer, controller, query, codec, checker, browser, bundle builder or scientific calculation was run. The only reviewer-created file is this report. Earlier source/results and the published disabled checkpoint were not changed.

## Published baseline and exact delta

The comparison baseline is commit `75a761f9503334cefe57eab20fa84e5cbf569a12`, titled “Prepare disabled complete N1000 native-state checkpoint with independent review.” Its `draft-manifest.json` SHA-256 is `6de7defdbe1a5e84ac99f471fe80e3b9c2ca6a88fcca0faa6f2af38d78774468`.

The local draft manifest is byte-identical to that commit. All **1,597** manifest pins were rehashed against their actual local bytes. The historical canonical-config pin was checked against `disabled-draft-config.json`, because that archived file preserves the old canonical config exactly. All pins matched. Separately, all **51 other published package files**, excluding only canonical `config.json`, were compared byte-for-byte with their Git objects at the baseline commit and matched. This includes scientific and supervisor/checker source, packaged bundle and its source index, science/runtime/prerequisite metadata, storage proof/admission and original review artifacts.

The canonical config changes three executable authorization keys and one descriptive scope field:

| Key | Disabled draft | Enabled config |
| --- | --- | --- |
| executionAllowed | false | true |
| authorization | null | Explicit renewal ID, approval time and reviewed draft-manifest hash |
| launchCutoffUtc | null | 2026-10-17T07:15:28+00:00 |
| scope | Disabled source-only draft description | Enabled single-attempt allocation following explicit human renewal |

No other config value differs. In particular, the two-stage order, source paths, exact completion assertions, browser-root closure requirements, preflight, timing limits and byte budgets are unchanged. The final scope wording was reread after the parent updated it to describe the enabled single-attempt allocation; this is a descriptive change only. The science-config status remains the historical string `source-only-disabled-draft` to preserve exact reviewed science and storage-proof pins. Canonical config, rather than that descriptive science status, is the actual execution gate; the new execution protocol documents the transition.

`disabled-draft-config.json` is byte-identical to canonical config at the baseline commit: **1,773 bytes**, SHA-256 `6deae4af1afd09735041d4280f94824c4ef26f14e3f92628ebc951e9a9dbe0c1`. Enabled canonical `config.json` is **2,049 bytes**, SHA-256 `53f85429d2a289ef2767ad7dd526fdac58f3bf2e69caa1c2bb6821b988ba4d96`.

## Approval and fixed window

The parent reported the direct human reply “Allow a new two-hour execution window.” The new authorization record repeats that answer and binds it to one bounded N1000 test, evidence inspection and outcome publication. The record honestly identifies its timestamp basis as the first tool-clock observation after that reply, rather than claiming a separately observed message timestamp.

Canonical config, `EXECUTION-AUTHORIZATION.json` and `EXECUTION-PROTOCOL.md` agree on:

- Approval/start basis: **2026-10-17 05:15:28 UTC**, or **13:15:28 Asia/Shanghai**.
- Fixed cutoff: **2026-10-17 07:15:28 UTC**, or **15:15:28 Asia/Shanghai**.
- Exact difference: **7,200 seconds**.
- Reviewed disabled commit and manifest: the baseline identities above.
- Single scientific attempt, zero scientific retries, unchanged scientific scope and no resumption of expired overnight automation.

The authorization object has exactly the three fields expected by the unchanged supervisor: `id`, `approvedUtc` and `reviewedSourceManifestSha256`. Its ID is nonempty, its timezone-aware timestamps are ordered and the reviewed manifest hash matches actual archived manifest bytes. The supervisor's unchanged full-reservation test requires at least 360 seconds remaining before creating an attempt. Therefore the two-hour authorization does not turn into a two-hour scientific allocation; the latest nominal start for a full 360-second reservation would be 07:09:28 UTC, subject to all earlier gates and setup time.

## Unchanged scientific and resource contract

The preserved science config still specifies exactly one N=1000 case `tree-t0-n1000-a`, seed **2026101741**, unchanged initialization at t0, one projection, fixed native order **F, H0, H**, and one whole-swarm derivative. Duration/dt/integration step count remain zero. There is no RK continuation, endpoint, safety continuation or fresh high-precision reference.

The unchanged success contract remains exactly **22 ordered journal records**, three primary native calls, one primary derivative stage covering 1000 rows, twelve fixed wiring controls, separate tiny checker arithmetic fixtures, and the qualified full tree layout with exact reconstruction. Full original native non-tree evidence remains required. No sampling, reduced evidence, extra seeded case, adaptive rescue or codec substitution was introduced.

Resource allocations remain 360 seconds total: browser 120, checker 180, setup/closure 60, with the separately bounded 15-second metadata prerequisite validation charged to overhead. Output limits remain 32 MiB per general file, 256 MiB combined, 160 MiB evidence, 64 MiB private, 30 MiB other public output and 2 MiB finalization reservation. The existing admitted complete-success storage proof and its limitations are unchanged. Neither that proof nor this enablement review guarantees complete capture of arbitrary malformed failure bodies.

The unchanged supervisor requires an absent results directory, exclusive initial attempt creation and exclusive stage outputs. A scientific attempt consumes this single-use path even if it fails. The new protocol explicitly requires preserving raw/partial output and an externally observed exit, and says a source defect after exposure does not authorize another run. Prospective allocations are required for any later saved-evidence inspection or UI-only viewer check; such work is separate from scientific reruns.

## Required prelaunch closure and review limits

At the metadata observation **2026-10-17T05:16:25.034725+00:00**, `results/`, `source-manifest.json` and `source-publication.json` were all absent. This is consistent with preparation before exposure. No current-run result exists or is claimed by this review.

The historical disabled draft manifest must remain historical: its original config pin does not match the enabled canonical config by design. The parent must assemble a new enabled source manifest that pins the actual canonical enabled config, authorization/protocol records, archived disabled config, enablement reviews, original unchanged implementation/dependencies and required retained closure. It must then publish and verify the exact enabled commit/manifest and every pinned byte before launching. The unchanged supervisor, validator, controller and checker bind the supplied execution-manifest SHA and source commit to the live attempt and publication receipt.

This review confirms the local enablement delta and historical byte preservation. It does not claim that the enabled manifest has been assembled, the enabled source has been published, remote equality has passed, runtime behavior has been tested, or the scientific calculation has succeeded. Those remain explicit subsequent gates. It introduces no additional approval requirement beyond the human renewal already supplied.

## Enablement artifact pins

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| `config.json` | 2049 | `53f85429d2a289ef2767ad7dd526fdac58f3bf2e69caa1c2bb6821b988ba4d96` |
| `disabled-draft-config.json` | 1773 | `6deae4af1afd09735041d4280f94824c4ef26f14e3f92628ebc951e9a9dbe0c1` |
| `draft-manifest.json` | 395925 | `6de7defdbe1a5e84ac99f471fe80e3b9c2ca6a88fcca0faa6f2af38d78774468` |
| `EXECUTION-AUTHORIZATION.json` | 925 | `a043801bf2c16d37bdda0d781fb21bfaf5b941ae8d9eef8a033fb2622039ba63` |
| `EXECUTION-PROTOCOL.md` | 1712 | `98b762497e7b9dfa0f42e1c21a8a9db00b326f2b61b3330b34de6bdfb4eec1d0` |

Review closed UTC: 2026-10-17T05:17:18.541306+00:00.
