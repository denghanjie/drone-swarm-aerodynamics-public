# Single-PIV provenance admission — bounded documentary check

19 October 2026. **Full dimensional/calibrated-component-to-release chain: NOT ADMITTED.** This bounded search obtained no genuinely new preprocessing source that ties the pinned released `u_piv` and `v_piv` variables to dimensional calibrated components. The useful new observation is a current check of the primary manuscript's revision metadata. Repository/registry access failures limit this conclusion: it is not a finding that the missing documentation does not exist, nor evidence that the released values are wrong.

Only this scratch note was written. No archive or raw-data retrieval, payload inspection, model/data calculation, installation, author contact or access-challenge bypass occurred. No publisher full text is reproduced here.

## Existing baseline read first — not new evidence

The following retained ledgers were read before the remote check:

- `research/m31-airflow-scale-transfer-2026-10-19/review/NORMALIZATION-SOURCE.md`
- `research/m31-crossstream-test-2026-10-19/review/GEOMETRY-AND-CONTINUITY.md`
- `research/m31-physical-test-2026-10-19/review/GEOMETRY-CORRECTION.md`
- `research/m31-physical-test-2026-10-19/review/LITERATURE-REVIEW.md`

They already establish a documented common nominal Ui convention for single-PIV u/v, the direct plotting of prepared variables, missing single-PIV conversion/calibration/stitching history, the README's 5 May 2026 update, and the inability to transfer a separate multi-vehicle magnitude script's denominator to these components. They also already distinguish original projected half-spacing 32.5 mm from later radial-arm material and do not establish raw-record identity across papers. None of those conclusions is relabeled a new finding here. Neither archive nor old paper full text was reopened for a fresh normalization claim.

The target release remains the previously pinned archive SHA-256 `b495b7a224b3c1db9f15efd5a15815c586e4e11ea29d4df6edcbc25bf50554fa`. No new primary record encountered in this pass supplied that checksum, a matching release version, or an explicit processing lineage for its single-PIV variables.

## Newly checked primary metadata

### Current manuscript revision record — limited affirmative evidence

Verified readable URL: [arXiv record 2507.09463](https://arxiv.org/abs/2507.09463).

The current primary record displays one submission-history entry, v1 dated 13 July 2025, and identifies the RSS 2025 publication and related proceedings DOI. The displayed record lists PDF/HTML/TeX access and generic code/data discovery toggles; it does not display an identified author preprocessing repository, archive version history or component-calibration supplement. I did not follow generic third-party finder toggles or download source files.

**New versus old:** this is a fresh check that the currently displayed revision history exposes no later manuscript version; the existence/content of the v1 paper is old evidence. This check provides no trace from dimensional components through normalization into the current Brown release, and it cannot establish whether separate repository files were updated.

### Newly surfaced earlier publication — discovery lead only

Publisher-indexed URL: [AIAA DOI 10.2514/6.2024-4145](https://doi.org/10.2514/6.2024-4145).

The search returned the publisher's record for *Downwash Dynamics: Impact of Separation on Forces, Moments, and Velocities for Dense Quadrotor Flight*, with Anoop Kiran, Narek Harutyunyan, Nora Ayanian and Kenneth Breuer. Opening the DOI returned HTTP 403. Thus the title/DOI were surfaced as a primary-publisher discovery lead, but this pass did not inspect its supplements or verify a release correspondence. It is not admitted as a calibration or exact-release source. I did not use the separately returned ResearchGate full-text excerpt as replacement provenance.

## Repository/registry attempts — access status, not negative content evidence

| Attempted primary URL | Outcome | What remains unverified |
|---|---|---|
| [DataCite API DOI record](https://api.datacite.org/dois/10.26300/64d4-wa17) | Web connector reported inaccessible | Deposit/update history, version and related-identifier fields |
| [Brown item record](https://repository.library.brown.edu/studio/item/bdr:rnnfmt6u/) | Web connector reported inaccessible | Current release metadata, linked revisions, supplements and checksums |
| Same Brown item via ordinary in-app browser | Browser unavailable before a tab was created | No page content obtained; no access challenge attempted |
| [DataCite Commons record](https://commons.datacite.org/doi.org/10.26300/64d4-wa17) | Web connector reported inaccessible | DOI metadata and links to versions/supplements |

These attempts do not supersede the prior successful Brown landing-page observation in the old ledger. They also do not verify whether its current contents have changed. No archive link was followed.

## Search and page budget

All four allocated search queries were used exactly once:

1. `"10.26300/64d4-wa17" version calibration`
2. `"Anoop Kiran" "u_piv" OR "RSS_2025_data" GitHub`
3. `"Anoop Kiran" Brown downwash data code`
4. `site:repository.library.brown.edu "Aerodynamic Interaction Dataset" OR "rnnfmt6u"`

The results included the already-known RSS and later merging-jets papers, institutional background, the AIAA precursor and unrelated coauthored simulation code. No returned result supplied an author calibration/export pipeline explicitly tied to `u_piv`, `v_piv` or the pinned release. This is a bounded discovery result, not an exhaustive claim about all author repositories.

The six primary-page/record-open attempts were DataCite API, Brown via web, Brown via unavailable in-app browser, DataCite Commons, current arXiv revision metadata and the AIAA DOI. The failed browser binding is conservatively counted against the six-attempt limit even though it created no page. No additional search, page open or archive/source download was performed after reaching that limit.

## Exact-release and full-chain disposition

No newly inspected primary source establishes the required correspondence between a dimensional/calibrated component dataset, its physical sign/coordinate transform, section assembly/masking history, the exact Ui construction applied to both components, and a named/versioned export matching this archive. Current arXiv metadata does not fill those links; the AIAA precursor cannot be equated with the later release on authorship or subject alone; inaccessible metadata cannot be treated as evidence of absent links.

Accordingly, retain the previous distinction between a documented nominal convention and unverified actual preprocessing. No conjectural scale factor, sign reversal, geometry remapping, dataset-version identity or correction is admitted. No current model coefficient, score or saved result changes. Reopening admission would require an accessible primary processing/calibration record explicitly associated with the exact single-PIV release, rather than another plot or general experimental-method description.
