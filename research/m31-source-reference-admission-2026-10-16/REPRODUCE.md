# Reproduce this bounded audit

Use Python 3 with existing pdfplumber 0.11.9 and pypdf 6.10.0 (see actual extractor metadata for installed versions). No new dependency was installed. Analysis itself uses the standard library only. Run from the repository root. Acquire the exact versioned PDF yourself from https://arxiv.org/pdf/2403.13321v3 into a private directory and verify the checksum recorded in OFFBOARD-ACQUISITION.json. The PDF is not redistributed here.

```sh
python3 research/m31-source-reference-admission-2026-10-16/extract_profiles.py PRIVATE_PDF_PATH PRIVATE_EXTRACTED_JSON
python3 research/m31-source-reference-admission-2026-10-16/independent/extract_pypdf.py PRIVATE_PDF_PATH PRIVATE_NEW_OUTPUT_DIRECTORY
python3 research/m31-source-reference-admission-2026-10-16/analyze_profiles.py --test
python3 research/m31-source-reference-admission-2026-10-16/analyze_profiles.py --input research/m31-source-reference-admission-2026-10-16/visible-profiles.json --output PRIVATE_NEW_RESULT_JSON
```

The independent extractor writes a clearly named private full-path file: do not publish it. The analysis refuses to overwrite its output. It records the current Git commit; scientific values should match the saved result even when run at a later packaging commit. Compare numerical fields separately from source provenance. No timing or live-simulation claim is made.

No data is sampled randomly; graphical vertices are not statistical replicates. The two extractor outputs differ only at floating-point roundoff, not physical uncertainty. See PROFILE-PROTOCOL.md for the immutable domain, metrics, limitations and stopping rules.
