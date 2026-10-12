# Sanitized public-release audit — 12 October 2026

The public payload is a separate sanitized export. The original repository remains private; its history and release asset are excluded. This decision follows a publication review requiring removal of local paths and saved machine/runtime metadata before public access.

## Removed

- Machine-specific absolute workspace and executable paths, replaced by relative locations or commands available through PATH.
- Saved user-agent strings and GPU adapter identity.
- Saved CPU, OS, architecture and runtime-version specifications, including duplicate copies in summaries, reports and historical records.
- Saved host load and process/host memory metadata.

Thirty research files were changed for these reasons; see [the exact file and hash inventory](public-export-changes.json). The top-level output manifest is separately regenerated and labeled for the sanitized snapshot. Research values, binary trajectories, model parameters, recorded failures and all 3D demonstrations are retained. Historical checksums describe the original private evidence where a listed file was sanitized.

## Review scope

The original and public payloads were searched with ignored data explicitly included, covering common credential/private-key/bearer-token signatures, credential-related fields, home paths, email patterns, unique device-identifier fields and URLs. Matches were reviewed in context. No stored credentials were identified. Public library challenge code has a public site key and a token variable, not a saved session token. Vendor-library references to credentials are API documentation.

All 75 image artifacts were visually reviewed as contact sheets. They show research interfaces and plots, without personal chats, account screens or unrelated desktop content. Image metadata was inspected. The generated design image retains standard C2PA generation provenance and public certificates. The one PDF contains the scientific passage plot, generic Matplotlib metadata and no embedded attachments. Local OCR was also used to look for machine-identifying text in screenshots.

All 306 release files (161 JSON and 145 Float64 files) are drawn from the sanitized tree. Binary trajectories preserve their original hashes and are aligned to 8-byte values. The original private archive was verified against its local source before export; the public archive is rebuilt from the sanitized files with new hashes. Packaging resets tar ownership names, numeric IDs and timestamps. Exact public size and checksums are in the bundle manifest.

The public repository starts from a new commit containing only this export. Its author uses the owner's GitHub no-reply email. No original private Git objects, local scratch files, chat attachments, authentication files or dependency environments are included.

## Limits

No sensitive information was identified in the sanitized payload using these checks. This practical review cannot guarantee detection of every possible secret and does not cover future updates. Withholding machine specifications limits hardware-specific performance comparisons. Publication does not establish physical validity, novelty, flight safety or real-time WebGPU performance. No open-source license has been selected for original project material.
