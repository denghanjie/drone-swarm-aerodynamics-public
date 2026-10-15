# Bounded archive-index inspection

This is a data-access and metadata inspection, not a scientific trial or model validation. It follows the published MODERA recommendation in `m31-followup-planning-2026-10-16/NEXT-DECISION.md`. No old experiment is reopened.

Before looking at archive contents: request only the last 65,557 bytes of the provider's 2,512,858,162-byte ZIP. Require HTTP 206 and the exact Content-Range; otherwise close without reading a response body. Parse an ordinary ZIP end record. If needed, permit one further exact range of at most 1 MiB for its central directory. Maximum two HTTP requests, no redirects/retries, 45-second process deadline, no request starting at or after 23:00 UTC on 2026-10-15. No member decompression, file extraction, fitting or whole-archive download.

Record selected nonpersonal response headers, actual range bytes, checksums, central-directory names and declared sizes. Index consistency is not full-archive integrity: the provider MD5 cannot be checked without the complete archive. Fail closed on unsupported ZIP64, multidisk, inconsistent bounds or structure. Preserve failure and do not automatically substitute another acquisition.

Source: Universitat Politècnica de València, *UAV digital model and experimental tests*, Zenodo record v1, 2025-10-27, DOI https://doi.org/10.5281/zenodo.17457069 . Prior verified record declares CC BY-SA 4.0; provider research/education notice is preserved in the preceding dataset review. Internal data schema, uncertainty and hardware compatibility remain unknown. Any published archive-derived material retains this attribution and license. Scientific observations cannot be inferred from filenames alone.
