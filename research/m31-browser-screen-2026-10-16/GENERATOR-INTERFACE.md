# Generator interface — source only

Integrate `generate.cjs` as `research/m31-browser-screen-2026-10-16/source/generate.cjs`. A future admitted parent supervisor invokes the pinned Node executable with script and one argument, the package root. Do not invoke during source preparation.

The package must have `config.json` using the fields in `config-fragment.json`, plus a frozen `runtime.json` with `platform`, `architecture`, and `node.{version,bytes,sha256}`. Other top-level configuration and limit fields may serve the parent/browser/reviewer. The complete `generation` object and `cases` must exactly match the fragment. The generator verifies its own Node executable bytes/hash/version, platform, architecture, little endian encoding, and absence of Node options before importing `outputs/milestone-31-source/sim.cjs`. The parent must independently validate the complete source manifest/publication before invocation.

`inputs/` and `generation/` must be empty at invocation. `results/` may contain parent supervision files. The generator exclusively creates `results/generation-child-invocation.lock`, never deletes it, and refuses a second invocation. Every payload write uses `wx`; no existing file is replaced.

Outputs use package-root-relative paths, compatible with the old generation records:

- `inputs/index.json`: `{kind:'fresh-airflow-off-boids-states',shape:['vehicle',17],dtype:'float64le',cases:[...]}`. Each case retains `id,n,seed,t,path,bytes,sha256,generationPath`.
- `inputs/<id>.f64`: final `n × 17` row-major state, binary64 little endian.
- `generation/<id>-initial.f64`: initial `n × 17` state.
- `generation/<id>-frame-000.f64` through `-frame-025.f64`: each `[t, ...n × (x,y,z,qx,qy,qz,qw)]` with width `1+7n`.
- `generation/<id>-poses.f64`: byte concatenation of the 26 frame files.
- `generation/<id>.json`: legacy run record excluding raw initial/final arrays, replacing them with pins; includes `id,n,seed,config,metrics,samples,recording,initial,final,frames,poses,generationMs,initialMatches,complete` and other unchanged simulator metadata. The extra `finiteStateShape` boolean records output-shape/finite checks. `recording` is exactly `{cadence:0.2,streamed:true}`. Metric samples remain the original 0.1 s sequence.
- `results/generation-evidence.json`: exclusive terminal generator record with kind `fresh-browser-screen-input-generation`, `complete`, `runtimeIdentityVerified`, `generation:[{id,pin,complete,generationMs}]`, `inputIndex`, runtime/config identities, limits, memory, and `newGenerationBytesBeforeEvidence` on success. It cannot certify its own supervisor closure.

On an exception, the current case's already-written initial/frame/final artifacts remain. If the simulator returned an incomplete case, its generation record is saved with `complete:false` before failure. No subsequent case runs. `inputs/index.json` is created only after all three cases complete. For an owned invocation, the catch path conditionally writes `results/generation-failure.json`, `results/generation-partial-evidence.json`, and terminal `results/generation-evidence.json` with `complete:false`; each is exclusive and each write attempt is independent. Repeated/unowned invocations never alter earlier records. Unknown exception messages are redacted to avoid local path leakage; supervisor logs/closure remain the external evidence of abrupt termination.

The 64 MiB cap counts every file in `inputs/` and `generation/` plus the four generator-owned result names (including lock and failure records). Normal output is capped at 60 MiB. Directory entries must be regular files; output accounting re-stats files so a partially written file is not silently omitted. Parent supervisor records/logs have their own allocation and are not counted as generator-owned output. Ordinary RSS/time guards are cooperative; the parent must enforce hard external lifecycle/budget termination. No cleanup deletes evidence and no failure authorizes a retry.
