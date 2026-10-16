# Required dependency pin closure addendum

Independent source review found that hashing every listed manifest entry does not ensure an imported dependency was listed. Before source freeze, the supervisor was corrected to require the five external baseline paths `research/m31-screening-cost-2026-10-17/source/{adapter.cjs,rational.cjs,pair-prepared.cjs,interval.cjs,spec.json}` explicitly, in addition to checking their current bytes through manifest.files.

The parent subsequently confirmed the checker will use a local `source/semantic-reference.py` with only Python standard-library dependencies beyond it. This helper is now an explicitly required local manifest path. The eventual checker import closure still requires source review; its declaration is not treated as proof of future content.

Both earlier new-cycle supervisor versions are preserved in prefreeze/supervise-before-external-pin-review.py and prefreeze/supervise-before-checker-helper-pin.py. The current source parses successfully via AST only; nothing was imported or executed. The independent containment reviewer has been sent the current hash and both changes. The original supervisor adaptation reading record is a historical snapshot; this addendum and its companion reading record supersede its authored-source pins.

All numeric limits, file names, guardian lifecycle and private/public log accounting remain as described in SUPERVISOR-ADAPTATION.md. Inherited reads remain 4 / 12.
