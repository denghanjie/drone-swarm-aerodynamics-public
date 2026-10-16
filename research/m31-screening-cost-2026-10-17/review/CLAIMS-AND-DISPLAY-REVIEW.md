# Saved claims and display source review

Date: 2026-10-17. Reviewer: `m31_verified_literature`.

## Disposition

**Accepted for claims and display source, with no blocking finding.** This review covers the saved milestone summary and viewer source snapshot below. It does not accept a finalized display binding or browser QA: `app.js` still contains `PENDING_BINDING_SHA`, and `index.html` starts with `data-binding="pending"`. The final binding and the separately bounded display QA remain required closeout gates.

The latest summary explicitly describes dense and sparse upright cubic lattices, identity orientations, and the admitted ordered positive-interaction subdomain. It correctly excludes general tilted or cyclic swarm qualification. No frozen scientific file was edited, imported, or executed. No kernel, checker, control, fixture, capacity probe, or scientific rerun occurred in this review.

## Claims checked against saved evidence

Using only saved integer nanosecond durations and Python `Fraction` arithmetic, I independently recomputed each method median, the median of four complete/hierarchy paired ratios, and the ratio of method medians. The milestone table rounds all values correctly to three decimals. All 24 measured ratios exceed one; all four pairs, including the smaller sparse-216 ratio, remain represented.

| Scene | Complete median s | Hierarchy median s | Median paired ratio | Ratio of medians |
|---|---:|---:|---:|---:|
| dense-cube-64 | 0.756738187 | 0.494196751 | 1.520564176 | 1.531248813 |
| dense-cube-125 | 4.721246563 | 3.316698000 | 1.395529713 | 1.423477978 |
| dense-cube-216 | 14.275431479 | 8.760861729 | 1.634310077 | 1.629455175 |
| sparse-cube-64 | 0.371483583 | 0.100792729 | 3.667053954 | 3.685618865 |
| sparse-cube-125 | 1.548142750 | 0.422430166 | 3.593705378 | 3.664848945 |
| sparse-cube-216 | 4.769618646 | 0.597513833 | 7.878908219 | 7.982440537 |

The dense-216 hierarchy median is **8.760861729 seconds**, correctly reported as **8.761 seconds**. Its separate arithmetic mean total is **8.8440418125 seconds**. The mean assembly stage is **8.656215958 seconds**, preparation **0.0929086775 seconds**, spatial **0.00248754175 seconds**, and admission/solve/certificate **0.09242963525 seconds**. Stage means sum exactly to the mean total. The summary correctly labels these as means and attributes the bottleneck to the combined traversal/scalar/assembly stage rather than claiming to isolate a primitive or GC cost.

All 60 saved trials comprise 12 warmups and 48 measured trials. Each scene has one warmup per method and four measured pairs in AB, BA, BA, AB order. Every saved trial scientific/common digest equals its method's fixed representative; the two methods share the same common digest per scene. This checks the saved digest relations, not recomputation of the scientific payload.

The saved audit records all six scenes admitted, qualified and passing; zero baseline errors; 527,776 independent pair outcomes and 1,055,552 validated method outcomes; all 15 controls executed, rejected and reporting their intended core failure. All qualification, tolerance, scientific, digest, timing, source-unchanged and input-unchanged flags are true. Claims in the summary reflect these saved results.

The method timing boundary includes validation/preparation, spatial work, pair assembly and certified loads. Summary/viewer descriptions disclose the excluded input-text conversion, final serialization/hashing, disk writes, rendering and startup overhead. These are method timings, not application frame times or independently remeasured clocks.

## Provenance and supervision

Source commit: `7d3c94410aaece78a151c13b7192c3a40ecb60d0`. The actual manifest bytes match `49643595936ffa7da8cab2ec8b992299db679e8365b10e2ee53ec403099bf87b` and 30,166 bytes. The saved source-publication receipt reports exact-commit HTTPS/TLS retrieval, local/committed/remote equality and 144 verified source pins. This review did not repeat remote retrieval or rehash all 144 source files.

The current timing index, journal and independent audit byte lengths and SHA-256 values match the supervision/audit pins. Both supervision reports agree on the source identity. All six scientific shard pins and all six independent-reference pins were checked against current file bytes; those shard/reference files were hashed only, not numerically recomputed.

- Timing index: 71,826 bytes; `9281a8026b0f68b5041b9d0e1e41e6fe4ee7dae66685dde09149a7615c7e6fff`.
- Journal: 76,840 bytes; `894093168ec26ed806bb201e7596cc89fb0dd3e9747d61e3dc58219df668d4ff`.
- Independent audit: 49,704 bytes; `e1999213ce853dfa9d807cd792881f197ea1e43f22d184355513ccd555d7d4e8`.

Kernel supervision records success and closure at 202.45597512461245 seconds, 2,515 RSS samples and 304,594,944 bytes peak sampled group RSS. Checker supervision records success and closure at 165.53534462489188 seconds, 1,988 samples and 199,229,440 bytes peak sampled group RSS. Both report absent child groups, rechecked source/runtime identity and no termination reason. The summary correctly separates these whole-process supervision metrics from benchmark method durations.

## Viewer source review

The source loads saved records and verifies byte pins, the binding identity, source/manifest links, supervision closure and per-scene links before enabling the display. The final binding hash is intentionally pending. Qualification and diagnostic/unqualified states are distinct. Rounded duration and ratio displays retain exact records as the source of truth; current duration formatting uses seconds for values at least one second and milliseconds otherwise. Stage values are explicitly arithmetic means across four measured trials, while the main table uses medians. Each selected scene shows every paired duration, order and ratio.

`group-scene.js` decodes saved geometry, displays nominal-relative predicted certified thrust, selected-rotor positive links, and saved hierarchy terminal boxes. Teal zero-proof and amber scanned-leaf meanings are explained; padded boxes and enlarged markers are disclosed. Orbit/render updates animate the camera, not drone dynamics. No scientific kernel is imported or run by the viewer source. Existing linked vendor/historical viewer contents were not reread.

The summary and page keep the static Node/hardware/scene scope, the at-most-216-drone limit, JIT/GC/cache/thermal/host limitations, and the timer trust boundary visible. They make no established novelty, physical validation, real-time browser or coupled 5,000-drone trajectory claim. The historical moving 5,000-drone Boids link explicitly identifies airflow as off. Suggested next-stage acceleration remains a hypothesis requiring its own prospective design and bounded experiment.

## Reviewed display snapshot

| File | Bytes | SHA-256 |
|---|---:|---|
| MILESTONE-SUMMARY.md | 5270 | `b81fd20424e0e27362962577da138d44beea2b913bd09481099911753da24901` |
| viewer/index.html | 5581 | `7e2b823a71f167353c74bbecfde48dba3d60d3ba78d9cb5a893186e5a436d7eb` |
| viewer/app.js | 6897 | `5f63da85001dfd3bb48dc8902fce36f53d6b0ef1387948abf525654cd5edfde5` |
| viewer/group-scene.js | 6175 | `b32a70f112d2a9accc82141d3a4e3db4865c946d14c896993f83f3242a7e5b62` |

Any later substantive display edit requires a corresponding source-diff review. Insertion of the final binding hash, binding-file creation and browser QA must be recorded separately. No screenshot, event-handler, WebGL rendering, resource-loading or final binding success is claimed by this source-only review.

## Reading and limits

The companion `CLAIMS-AND-DISPLAY-READING.json` preserves the exact inherited inventory and pins this review plus the current-cycle inputs. The inherited distinct-path count remains **13 / 16**; no additional inherited file content was read. All newly reviewed scientific results and display files belong to this cycle. Only saved arithmetic, JSON parsing, byte hashing and source reading were performed.
