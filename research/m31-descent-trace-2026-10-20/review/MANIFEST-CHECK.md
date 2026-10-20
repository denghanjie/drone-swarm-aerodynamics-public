# Pre-execution manifest verification

The existing protocol reviewer independently checked all 129 local pins, totaling 2,422,390,558 bytes. Coverage included all 14 reviewed candidate files, the protocol review, all 75 existing journal parts, required prior publication metadata and closures, both replay datasets/audits, Three.js dependencies, explanatory source and literature provenance. All candidate hashes were unchanged; selected parts match their respective public result manifests. The reviewer performed no allocation execution and wrote no files during this check.

The source manifest is 27,609 bytes, SHA-256 e9daac500d5b3539eda4bbf12628b4fc7a51f5da3234c9336a66cef5c475da83. Its exact bytes match source commit 94ed4a45862a928a3b003afa64d30f6bc35d021c. The parent separately compared every local pinned file to its committed blob and retrieved the exact-commit public manifest with TLS verification; it matched at 2026-10-20T14:37:19.113064+00:00. The receipt is source-publication.json. No byte-read anomaly was reported by that public verification pass. The receipt verifies a separately retrieved public manifest, not a complete re-download of the raw journals.

Extraction was launched only after both checks passed. Source remains immutable and earlier allocations remain closed.
