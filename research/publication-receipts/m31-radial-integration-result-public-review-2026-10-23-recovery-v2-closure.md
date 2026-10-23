# Recovery v2 closure and bookkeeping correction

V2 remains closed and failed. It stopped because the administrative verifier returned an event dictionary without its journal event number, causing KeyError during result-list assembly. This was a bookkeeping error, not a transport or byte-identity failure. The original v2 receipt, Markdown and journal remain unchanged.

The journal establishes successful authenticated public-repository metadata (event 1) and two complete local/result-Git/API file identities (API events 6 and 7), totaling 311,893 bytes. The conservative recoveredFileCount=0 field in the original receipt reflects the failed assembly step. Event-derived verified coverage is two files; 38 files totaling 5,256,772 bytes remain. The JSON clarification contains exact descriptors and event references. There were no failed HTTP attempts.

The helper launch explicitly requested require_escalated and was permitted, returning a running session that subsequently exited 1 because of the bookkeeping error. All four allocations stayed closed, 29 source pins stayed unchanged, and prior records/manifest were preserved.

The administrative helper correction returns the numbered dictionary from record(event). An isolated mocked test of those administrative functions confirms the event number reaches the caller and the journal; it made no network request and executed no scientific source. No acquisition has been rerun, and no passing composite has been written.
