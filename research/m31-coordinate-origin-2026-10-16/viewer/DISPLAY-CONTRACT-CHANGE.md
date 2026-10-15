# Post-review display contract v2

The initial viewer required a passed independent integrity review before displaying arrays. The sole review completed but failed two API lifecycle bookkeeping checks; source/JSON inspection identifies an incorrect checker expectation. Its immutable report, failure and terminal budget are preserved.

This UI-only change allows a clearly marked **unqualified recorded-evidence view**. It never changes scientific acceptance, rewrites review artifacts, waives discrepancies, or runs additional scientific arithmetic. The viewer checks exact file lengths/hashes, source/raw/index bindings, report-to-external-closure identity, terminal process/resource closure and recorded cohort/stage availability. It returns `byteBindingsVerified:true` separately from `integrityVerified:false` and `reviewPassed:false`. The page must say “Review FAILED · records unqualified” and retain that status throughout inspection. It must not say independent verification passed.

Corrupt/missing/contradictory evidence stays locked. A terminal failed review is displayed only under the explicit `bound-unqualified-records`/`terminal-review-failed` contract. The review cannot be forged into a pass by changing its visible boolean. Decisions and values are copied from saved reports/words; only display differences, colors and drawing transforms are calculated. Missing origin1A/B terms and origin1C serial remain absent.

The original prebinding viewer is retained under `../results/viewer-prebinding/`; the old static checks describe that historical source only. Final UI QA independently exercises the actual final implementation and negative-state protections. UI QA does not constitute a second scientific evidence review.
