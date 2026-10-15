# Source access log

Access date: **2026-10-15**. Log checkpoint: **13:26:51 UTC** (21:26:51 Asia/Shanghai), read from the clock tool. Entries below were observed during the same retrieval session before that checkpoint. Per-request timestamps were not exposed by the web reader; the checkpoint is not presented as each request's exact time. Method: web search and primary-page/PDF text retrieval through `search_service.web_run`.

No full papers, screenshots or datasets were saved into this directory. Bibliographic metadata and short paraphrases only are retained. A web response marked PDF/HTML is not, by itself, counted as a completed reading or dataset acquisition.

| Work / purpose | URL accessed | Observed access and use | Limitation |
|---|---|---|---|
| A1 publication | https://www.roboticsproceedings.org/rss21/p102.html | RSS title, authors, year, DOI and official BibTeX read. | Proceedings PDF body not compared with arXiv. |
| A1 text | https://arxiv.org/html/2507.09463v1 | Relevant full-text methods, static/dynamic results and limitations read. | Figures were represented by captions/text; numerical image digitization not performed. |
| A1 dataset | https://doi.org/10.26300/64d4-wa17 | Reader returned internal error. | No raw data, schema or reuse terms obtained. Earlier local challenge-page report was context, not re-established here. |
| A2 metadata | https://arxiv.org/abs/2403.13321 | Authors, v1/v2/v3 dates and title read. | Record's RA-L 2024 label differs from later author-lab year. |
| A2 text | https://arxiv.org/html/2403.13321v3 | Relevant full-text normalization, vehicle table, far field and control sections read. | Not a data/code reproduction. |
| A2 PDF | https://arxiv.org/pdf/2403.13321v3 | Title page, accepted-manuscript label and extracted text inspected. | No visual verification of geometric arrows; do not infer diagonal versus edge geometry solely from text extraction. |
| A2 author listing | https://rpg.ifi.uzh.ch/publications.html | Entry lists RA-L 2025 and an earlier “around a Quadrotor” title. | Lab listing also spells Koen Mueller; bibliography follows the version-read PDF's Koen Muller. |
| A2 journal DOI attempt | https://doi.org/10.1109/LRA.2024.3518835 | Reader failed. Candidate identifier surfaced in search. | Not independently confirmed through an accessed primary record; omitted from BibTeX. |
| A2 attempted author subpage | https://lbfd.github.io/publication/2024-downwash/ | Inaccessible. | No claim derived. |
| A3 metadata | https://arxiv.org/abs/2312.03488 | Authors, title, 2023 preprint and ISER presentation note read. | Preprint date is not proceedings publication date. |
| A3 text | https://arxiv.org/html/2312.03488v1 | Relevant full-text model, powered receiver setup and results read. | No raw observations or trained model downloaded. |
| A3 publication | https://link.springer.com/chapter/10.1007/978-3-031-63596-0_35 | Publisher metadata, abstract and citation read: 6 Aug 2024, pp. 393–404, volume 30. | Chapter body is subscription content; technical reading used arXiv. |
| A3 publisher navigation | https://link.springer.com/book/10.1007/978-3-031-63596-0?page=3 | Table of contents located the chapter and authors. | Navigation only. |
| A4 metadata | https://authors.library.caltech.edu/records/psxc9-vps89 | Authors, DOI, journal issue/pages and online/current-version dates read. | Repository labels its attached manuscript “Submitted.” |
| A4 preprint | https://arxiv.org/abs/2012.05457 | Title and author record accessed. | Content reading uses pinned v2 below. |
| A4 text | https://arxiv.org/html/2012.05457v2 | Relevant full-text equations, architecture, stability assumptions and practical training scope read. | Proofs and every flight result were not audited; code not run. |
| F1 citation | https://www.red3d.com/cwr/papers/1987/boids.html | Author citation/abstract page accessed; exact citation also returned by primary-domain search. | A later repeat request failed. |
| F1 explanatory primary page | https://www.red3d.com/cwr/boids/ | Opening rules, neighborhood, obstacle/goal and complexity discussion actually read. | Author explanation is distinct from the 1987 paper body. |
| F1 original paper attempts | https://www.red3d.com/cwr/papers/1987/SIGGRAPH87.pdf | Initial response identified a 13-page PDF, but section opens/finds timed out; screenshot responses supplied markers without usable image content. | **Not counted as full-text read.** |
| F1 alternate/DOI attempts | https://red3d.com/cwr/papers/1987/SIGGRAPH87.pdf ; https://doi.org/10.1145/37401.37406 ; https://dl.acm.org/doi/10.1145/37401.37406 | Inaccessible/internal error. | DOI excluded from BibTeX; stable author URL retained. |
| F2 author context | https://vasarhelyi.github.io/drone-project-site/scirob2018.html | Project page accessed to locate the work. | Technical claims rely on PDF below. |
| F2 full text and metadata | https://research.vu.nl/ws/files/118802354/Optimized_flocking_of_autonomous_drones_in_confined_environments.pdf | Institutional cover and relevant version-of-record text read. | Original article page numbers differ by one from PDF indexes because of repository cover; supplement not read. |
| C1 full text | https://developer.nvidia.com/gpugems/gpugems3/part-v-physics-simulation/chapter-31-fast-n-body-simulation-cuda | Online chapter, authors, tiling, timing context and hierarchy sections read. | Old CUDA hardware; not a WebGPU benchmark. |
| C1 publication date | https://www.informit.com/store/gpu-gems-3-9780321515261 | Publisher page read: 2 Aug 2007 publication, 2008 copyright. | No DOI required for this book chapter. |
| C1 book-navigation attempt | https://developer.nvidia.com/gpugems/gpugems3 | Redirected to contributors; searched for date. | Not used to establish publication date. |
| C2 original URL attempt | https://developer.download.nvidia.com/compute/DevZone/C/html_x64/5_Simulations/particles/doc/particles.pdf | Timeout. | No content read from this URL. |
| C2 successful text | https://developer.download.nvidia.com/assets/cuda/files/particles.pdf | Cover, revision history and relevant printed pp. 4–7 read. | Historical sample clamping should not be copied as a valid dense-neighbor policy. |

## Search and correction-check scope

Discovery included exact identifiers/titles for A1–A4; quadrotor receiver/downwash models; original Boids; confined flocking; CUDA all-pairs and uniform-grid approaches. Search results from aggregators, ResearchGate, blogs and social sites were discovery leads only, not technical evidence. Other papers surfaced but were not incorporated into this bounded map; this is not a search for every 2026 publication.

Four exact-title queries with **“correction erratum”** were run for A1–A4. No identifiable formal correction notice appeared in the returned results. This is a limited search outcome, **not confirmation that no corrections or retractions exist**. Publisher/institutional records and available preprint version information were inspected; a Crossmark/Crossref or complete journal issue audit was not performed. No targeted formal-correction search was conducted for F1, F2, C1 or C2.

The A1 percentage inconsistency is our observation of two passages in v1, not a publisher-issued erratum. Date differences for A2–A4 and C1 are recorded as version/publication distinctions. The local wake-length correction in earlier research notes was not silently promoted to an independent figure remeasurement here.
