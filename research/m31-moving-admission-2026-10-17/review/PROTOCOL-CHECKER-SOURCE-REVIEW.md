# Independent protocol and checker source review

Reviewer: m31_verified_literature. Stage: source preparation only. Decision: no blocking source-consistency finding for the pins below. This is an independent review of the protocol/checker, not independent approval of the supervisor that this reviewer authored. The separate supervisor reviewer reported no blocking containment mismatch; its own review record remains authoritative for that assessment.

The initial complete checker source and result contract were read, followed by the same-buffer artifact pinning delta and the final shared journal decoder delta. The final exact runtime-literal delta was then read: the report must say v24.19.0/darwin/arm64 as well as match the pinned executable digest; the literal comes from parent prior receipt evidence, with no new runtime probe. Final PROTOCOL.md, RECORD-CONTRACT.md, configuration and prospective decisions were reconciled. The cumulative inventory is11of20 inherited/adapted content paths, conservatively charging the new adapted checker and contract. Earlier reading records remain intact.

## Pinned source

| File within package | Bytes | SHA256 |
| --- | ---: | --- |
| `source/check.py` | 68149 | `084f4f45aa353f7a7d8adc5c4a78eae4b09ee83fb2119741b01a317225d3fa69` |
| `source/result-contract.json` | 9872 | `f9dea13a77a04a2a974caf5ffec06125b6fcb506eb23e9d34266fe2494e8a7c3` |
| `source/config.json` | 5362 | `0a6b876edb63f13ce17ac81f996dea741e93abe72bdb28b7c6649626ffab278e` |
| `PROTOCOL.md` | 7032 | `5ff0215d326f5e4625824421f218b7f5a30c4d6d7f649936b31954a144caa045` |
| `RECORD-CONTRACT.md` | 10345 | `921231b8dcc9a9d7342cfe113edce75334bba39ebd7de13615efdd86f56173b6` |
| `source/semantic-reference.py` | 39634 | `ee77aab09109d3fba898555dacc4509312813caae4116bb3e1063efd88e3ad2c` |
| `source/pair-reference.py` | 44757 | `845f52cf350a09d2043934dff3e797a7b7416f4ef5c64beb716104bcd74f38f0` |
| `source/supervise.py` | 26727 | `8d23c224fd0f976552fd266ea5dac13e9fc9c7566d8694f7c23f14fab57eec27` |
| `source/guardian.py` | 2276 | `10341c52ab32fa8ff80c3909d578a7d368a3b2bcea59e78af7e8aa8f29c619f0` |
| `runtime-pins.json` | 248 | `842b2522133ed499f4706e071b09f3d100c5f4ed3f41d0fd135736c4dc191087` |

## Protocol challenge

The intended question is finite moving-state admission of the unchanged filtered model over six scheduled full states. The protocol preserves actual17-word flight states, with no flattening of attitudes or replacement thrusts. It separates uncoupled flight generation from posthoc aerodynamic evaluation. The exact two seeds,64drones,10seconds,0/5/10second full-state schedule and0.2second pose cadence are source-fixed. Four fixed controls precede the two generation recordings, and both recordings must be complete before any generated-state method call. A stopped generator leaves explicit missing scheduled states in the denominator of6. No substituted state, reseed or retry is authorized.

The positive mixed-leaf control has three drones; the other controls have two. This change from the earlier planning shorthand is explicit and prospective. Intended witnesses have not been numerically tested. Their absence fails the registered corruption controls rather than allowing a replacement recipe. The fixed ordering control exercises the chosen ordering refusal; it does not, by itself, demonstrate a graph cycle.

The final protocol, contract and implementation agree on the stricter nontriviality gate: each run separately needs positive edges at two scheduled times, a post-initial prepared horizontal-axis squared norm greater than1e-6, relative position change versus drone0 greater than0.001m in each coordinate, and a changed resolved positive-edge set relative to that run's initial set. Witnesses for the coordinates may differ. These are design thresholds with no population or physical-validity meaning. Ambiguous or absent witnesses make this transfer test uninformative.

## Checker source challenge

1. **Wire format and provenance.** Index, generation and method artifacts are decoded under sorted-key, compact-layout, duplicate-key, ASCII and numeric-shape gates. Scientific records use raw binary64 words and exact canonical-line checking. Diagnostic decimals are parsed without Python float reserialization. The final decoder is shared by journal lines. Index/generation/method hashes are made from the same buffers that are parsed, and all evidence pins are reread after validation. The journal reconstructs the exact fixed event order, including both generation completions before generated queries, and checks the final index pin. Source maps, runtime identity, supervisor environment and both permanent attempts are bound.

2. **Independent raw preparation.** The checker imports only the two explicitly pinned independent helper buffers after source verification. It never imports the candidate or simulator. RawWordHelper changes only the helper argument's literal interface to parse_bits for captured17-word states; the unchanged helper functions retain their original globals. Fresh source inspection confirms regenerate_scene uses this argument for raw inputs, while constant/operation-graph calculations keep the inherited decimal-literal semantics. This is a narrow adapter, not a rewrite of helper arithmetic.

3. **Coverage, zero filtering and refusals.** When global preparation is valid, reconstruction covers every logical nonself rotor/source pair. The wrapper validates fast-zero membership, ordering, branch and work counters against the full independent oracle before passing a shallow metadata projection to the inherited hierarchy validator. Global preparation refusal has filterPrepared equal to0. Canonical, independently validated model refusals can pass record integrity, but cannot advance admission. Reference-undecidable and unvalidated numerical refusal/status gaps fail integrity and retain distinct causes. Global preparation refusal does not claim pair or graph evaluation.

4. **Graph conclusions.** Graph status is resolved only if every pair is zero or positive. Vehicle edges are source-to-receiver, duplicates collapsed. The checker separately computes a rank/order witness and a DFS cycle witness. It distinguishes cyclic, acyclic but incompatible with the chosen order, compatible, and unknown cases. Therefore an ordering refusal cannot silently become a cycle claim.

5. **Controls and witnesses.** All20fixed mutation recipes require the intended semantic/provenance error family plus a saved bounded witness. Scientific mutation witnesses are selected only from the fixed positive/refusal controls, with no generated-frame fallback. Missing required witnesses are explicit failed controls. Mutation validation reaches the intended core checks before unrelated generic digest comparisons. Disposable method clones are handled one at a time.

6. **Denominators and advancement.** The checker reports reached, independently verified, admitted and certified counts separately. Known refusals may be verified while not admitted; missing slots are retained as not reached. Conditional load validation has its own admitted denominator. Advancement requires integrity, all four fixed and all20mutation controls, all six reached and independently verified, all six certified under every unchanged normalized1e-8load tolerance, and both runs informative. A successful checker exit means its integrity decision, not automatic scientific advancement.

7. **Saved outputs and containment interfaces.** Generation validation binds exact IDs/seeds/options/source, callback and frame order, capture/pose correspondence, initial/final full states and early-stop reasons. Selected unchanged simulator source confirms the0.1second sample grid,0.2second requested pose cadence,5second full progress cadence and off-schedule terminal handling. The wide factory's exported course label is factory-v1, matching the checker. References are written for fixed controls and actually reached scheduled states only. Closed file sets and kernel/checker/output budgets match the adopted wire contract. Runtime feasibility remains untested and is guarded by the separate supervisor.

## Reused trust and limitations

The unchanged semantic-reference and pair-reference hashes match the previously reviewed helper sources. This review freshly checked the raw-word adaptation, refusal/graph interfaces and validator entry points, but did not repeat a complete proof of every inherited numerical routine. It relies on prior reviewed helper algebra and on the pinned unchanged model/simulator implementation. It checks saved trajectory provenance; it does not independently regenerate or prove the trajectory dynamics.

The source was syntax-parsed and hashed only. No scientific module was imported; no control, generator, candidate, reference, checker, supervisor or guardian was run. There was no fixture creation, runtime probe, browser run, installation, new literature retrieval or commit. No older allocation was reopened. The static review provides no evidence that the small fixed witnesses, resource caps or generated admission gates will succeed.

A finite informative pass would establish eligibility for the next fresh portability/oracle experiment on this prescribed schedule. It would not establish continuous-time or all-intermediate-state admission,5000-drone scale, real-time speed, aerodynamic feedback in these trajectories, physical truth or emergence. The parent still owns complete freeze, public publication, exact source verification, launch eligibility before the fixed cutoff and all later result claims. Any scientific source or decision change after these pins requires renewed review of the change before launch.

The cumulative evidence inventory is `review/PROTOCOL-CHECKER-SOURCE-READING.json`; earlier supervisor notes are preserved separately. This source review does not open or extend a numerical allocation.
