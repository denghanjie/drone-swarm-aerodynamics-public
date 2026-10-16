# Result claims and limits

| Statement | Evidence / disposition |
|---|---|
| All 1,488 declared primitive records matched | Observed in the one independent checker execution; zero baseline errors; exact IDs/order/inputs/statuses/endpoints and successful inclusions checked |
| Successful enclosing intervals | 1,032 records; not 1,488 successful numeric outputs |
| Correct declared unsuccessful arithmetic outcomes | 215 domain, 236 range, 5 nonfinite; all retained, none dropped |
| Deliberate faults were detected | Six probes in five categories rejected by the same core validator; one wrong bound specifically failed inclusion |
| Journal completeness | 1,488 journal rows and completion marker matched final records |
| General inclusion of the primitive formulas | Separately source-reviewed conditional argument, not inferred from finite testing and not a machine-checked engine proof |
| Input mutation was impossible in all APIs | Not established; source freezes ordinary interval objects and runner checks before/after observable inputs; hostile objects and hidden/transient side effects are outside scope |
| Malformed-input and emergency failures empirically covered | Not established; malformed serialized inputs and internal iteration/check fault paths were outside the frozen suite |
| Browser-runtime qualification / practical swarm speed | Not tested; Node v24.19.0, V8 13.6.233.17-node.51 on darwin arm64; independent checker CPython 3.12.14 |
| Complete aerodynamic/load certificate | Not implemented by these seven primitives |
| Agreement with legacy rounded query | Not established; exact-real M-current track remains distinct |
| Physical validity, safety or novelty | Not established; no new physical evidence or priority search |

Supervised kernel wall was 0.7840024177 s and checker wall 0.6027210830 s, within their separate 120 s caps. These are supervision/accounting observations, not a per-interaction benchmark or speed comparison. Sampled process-group RSS maxima were 72,744,960 and 54,657,024 bytes; sampled peaks do not bound every transient. Actual maximum sampling-request gaps were about 0.0882 and 0.0827 s. Both groups were observed absent at closure. The recorded executable hashes do not pin loaded system libraries.

The source gate used direct HTTPS exact-commit GitHub content after two connector transport failures; the independently downloaded manifest exactly matched local committed bytes. Those transport failures occurred before any numerical attempt and are preserved in source-publication.json. Neither scientific allocation was retried. Earlier L/F timings and their dense-symbol correction remain unchanged.
