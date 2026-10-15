# Public-payload review

Reviewed the additive `research/m31-restart-2026-10-15/` payload before publication. The inherited public repository and private originals were not republished or edited by this checkpoint.

- Scientific inputs came from the existing sanitized public repository and its checksum-verified release assets. Drone states and factory geometry are synthetic simulation data, not real flight locations or personal records.
- No user attachments, private conversation text, credentials, browser profiles, raw tool logs, local environment dumps, hostnames or hardware identifiers are included. Runtime versions are retained for reproducibility.
- A machine-specific source-root field in the secondary audit was replaced with `PUBLIC_REPOSITORY`; relative artifact paths were normalized. The transformation is declared in that record and `provenance.json`. Input bytes, hashes and computed scientific values were preserved.
- Pattern checks of all new text files found no private home/temporary-user paths, recognized GitHub/AWS token patterns, bearer credentials or private-key blocks. Scientific JSON and scripts were also reviewed for unnecessary identity metadata. Pattern scans are a screening aid, not a universal guarantee against every possible secret format.
- Literature files retain bibliographic facts, stable links and original paraphrases. No third-party full papers, figures or raw measurement datasets were copied. Three.js and OrbitControls remain under the repository's existing vendor notices.
- Browser screenshots show only the local research page and synthetic results, with no browser toolbar or account UI. The viewer loads its scientific assets and vendor code locally.
- Only this new directory is to be staged. Preserve newer remote main and all historical failures; use an additive `codex/` research branch and a normal push.

The exact reviewed files are enumerated by `manifest.json`; the Git commit pins the manifest itself. The verified remote commit URL is recorded in the delivery message and local publication receipt after push.
