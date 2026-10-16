# Qualification supervisor source review

This is source preparation for a separate exposed-corpus validator qualification. It does not report qualification success, a new trajectory, new scientific observations or an amended old result. The old moving-admission gate remains failed. No qualification driver or scientific module was imported or executed while preparing these files.

## Authored files and inherited trust

The new `source/supervise.py` and `source/guardian.py` adapt the previous allocation's retained-guardian lifecycle and resource-accounting structure. The new scope has one Python qualification child, a distinct attempt marker, a fresh output directory, a reduced closed output set, new source/publication gates and explicit old source/result identities. It does not reuse the old stage marker or old output destinations. The new runtime-pins.json keeps only the active Python executable's inherited pin; Node is not launched.

Reviewed supervisor: 29,640 bytes, SHA256 `91d79f3b025ee75d036f37628af9424ec61f3e3e9abf2d891e6495fe33306b70`. Guardian: 2,470 bytes, SHA256 `9363f141731075f502c7ea63308b93fa4a14ad1819a9bc7bb6b06c5956f88a52`. Runtime pins: 126 bytes, SHA256 `806e6dfee974d35f04828496fb0e3afb9b4603e275d2f75987b4245203203349`. Subsequent review corrections require a fresh pin before freeze.

The inherited supervisor/guardian's source and historical manifest/receipt envelopes were read, not executed. The unchanged numerical checker, reference helpers, simulator and force backend were not imported by this author. This source review relies on the parent and independent driver review for the driver's numerical semantics and the restriction against calling the old main entry point.

## Preflight and immutability

Before launch, the supervisor requires the exact prospective config, 21 declared negative controls, ten fixed reference IDs, Python isolated mode and disabled bytecode. Loader injection is refused, and child preload/search environment overrides are cleared. The active Python executable is checked against the exact byte/SHA256 pin.

The source chain is separated into three commits: historical source, historical published results, and the new publicly verified qualification source. The new manifest and HEAD must agree with the new publication receipt. The entire historical source closure of 53 pins and historical result closure of 128 pins are rehashed as opaque bytes and compared with their respective committed blobs before and after the child. The old manifests, old result receipt, old failed-check flags and old checker-source hash are also retained. The new publication cannot precede the old corpus's verification receipt. No remote check is invented: exact HTTPS verification is supplied by the parent's saved receipt, while this supervisor verifies current/committed bytes.

The attempt file is exclusive, fsynced and immutable through finalization. No child starts until all gates pass and the attempt exists. Any existing result or private-log artifact blocks the allocation. The chosen private directory is outside the repository; result paths are under the new package only. All old source/result files remain inputs and postrun mutations fail qualification.

## Resource and lifecycle checks

Only qualification.json and the ten fixed reference files are scientific outputs. All eleven are required for success, with a 64 MiB total cap, 2 MiB report cap and 32 MiB per-reference cap. Metadata and both public/private logs share 16 MiB; aggregate80MiB. Unknown outputs, symlinks, unexpected subdirectories and private log entries fail the stage. The supervisor's own final report is limited to 64 KiB and reserved in final accounting.

Supervisor wall limit is 600s, guardian limit 610s, and sampled group RSS limit 1 GiB. Launch cutoff is checked by supervisor and guardian immediately before their child launch. The guardian retains group identity until the supervisor observes the scientific child absent and releases it. Unexpected descendants, group residuals, guardian failure, broken parent connection or resource errors prevent qualification. The supervisor signals only while the owned guardian remains alive and requires final group absence. Source/runtime, attempt and old-corpus checks run again after child closure, and their time is included in the reported supervised duration.

These are reviewed-process containment checks, not proof of continuous peak memory bounds or hostile process isolation. Finalization failure is itself failure and leaves an exclusive terminal-error marker when possible. The existence of a report is insufficient: exit codes, immutable identities, resource bounds, required outputs and closed group must all agree.

## Driver agreement and result scope

The agreed CLI uses Python `-I -B` and explicit config, new manifest, new report and repository-root arguments. The supervisor supplies new and historical identity environment bindings, documented exactly in SUPERVISOR-INTERFACE.md. It owns the attempt and lifecycle files; the driver owns only the new scientific outputs.

A successful qualification report must carry all six top-level new/prior provenance fields matching the attempt, plus `passed:true` and `exposedCorpusQualificationPassed:true`. It must preserve `historicalOriginalPassed:false`, `historicalOriginalAdvancement:false` and `transferAuthorized:false`. Thus even a newly qualified exposed-corpus validator cannot rewrite the original failed experiment or authorize transfer. A false result exits nonzero and consumes the attempt.

The source interface was coordinated with the independent driver author before freeze. Parent and literature reviewer independently inspected the full supervisor/guardian source. The only noted interface corrections were the driver's six top-level provenance fields and a documentation command that initially omitted `-B`; these are source-only corrections, not responses to qualification output. A targeted final source read confirms that the driver now emits the exact six top-level provenance fields from its gated new/prior identities, retains the three historical/transfer false flags, and returns exit 0 only when its passed flag is true. The new machine contract declares the same fields, fixed output set and resource bounds. This is an interface check, not a second numerical implementation review; the inspected driver/contract pins and limited reading scope appear in SUPERVISOR-READING.json.

## Permitted validation and reading inventory

Both new Python files passed `ast.parse` under pinned Python `-I -B`. Their module bodies were not executed or imported; no supervisor preflight, child launch, helper import, scientific probe or numerical evaluation occurred. No old package file was edited.

SUPERVISOR-READING.json records hashes and scopes. Six historical content files were read; the newly derived Python-only runtime pin is conservatively counted as a seventh inherited-content item, within the fresh 20-file cap. New prospective config/protocol/reproduction/interface material is listed separately. Manifest member files were not opened for semantic content in this stage. Earlier source/audit allocations and their read caps remain closed.
