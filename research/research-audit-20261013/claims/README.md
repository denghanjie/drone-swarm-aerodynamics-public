# Claim–evidence ledger

Start with [AUDIT.md](AUDIT.md). The authoritative structured claim inventory is [claims.json](claims.json). Numerical calculations, source identities and raw-input hashes are in [audit-results.json](audit-results.json).

## Reproduce the audit

Run `node audit-records.cjs CAMPAIGN_DIRECTORY REPOSITORY_DIRECTORY` with the complete saved campaign evidence and its unchanged upstream repository sources. This reads files and recalculates statistics; it never runs a simulation or benchmark. It writes `audit-results.json` beside the checker. Then run `python build-ledger.py` to regenerate the ledger and summary.

Campaign links are branch-based and paired with input hashes. A release may replace the branch with its complete publication commit without changing the scientific evidence or recalculated results. The first published checkpoint should not be assumed to contain every later record.

Historical mission claims are identified but explicitly unaudited. A successful saved-record audit does not establish physical validity, general performance, or mathematical correctness for every possible input.
