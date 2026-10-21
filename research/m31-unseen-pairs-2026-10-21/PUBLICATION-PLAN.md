# Lossless evidence publication

Preserve all 51 new compressed parts (1566172290 bytes), each at most 32 MiB. After independent result review and privacy checks, freeze every result identity and upload unchanged raw parts in Git transport batches at most 384 MiB, then publish the complete result manifest and documents. Transport batching neither reruns nor recompresses evidence.

Bind each new raw part to identical producer/auditor descriptors and the replay export to its auditor hash before result freezing. Retain bounded read anomalies. Verify all committed/local pins and independently retrieve the exact public result manifest. Publish its receipt and verify that receipt publicly. Intermediate archive commits alone are not a completed publication. Repair transport only if needed; all numerical/audit/display allocations remain closed.
