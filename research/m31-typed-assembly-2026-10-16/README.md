# A fair test of typed interaction storage

Question: can changing how we store airflow interactions save meaningful work after both implementations already use the same lean arithmetic?

A retains the previous all-pairs calculation. L simplifies the arithmetic and uses ordinary arrays and Sets. T shares L's arithmetic but stores coefficients through fixed typed rows/chunks and builds already-ordered dependencies. T/L is the primary comparison. All compute the same complete frozen-pose coupled load, including construction and residual checks.

Three new, predetermined two-second flights supply poses: 1,000 drones once and 5,000 drones twice. They use the original local separation/alignment/cohesion Boids, broad shared route, avoidance and rigid-body dynamics with airflow off. These short flights test input relevance and computation; they cannot validate long-flight success, mutual-aerodynamic flight or physical reality.

Before timing, literal boundary/ownership controls and complete same-runtime outputs must agree. A separate Python/NumPy program recomputes every A interaction and uses a different cubic-root formula. It then checks all saved L/T outputs and the timing records. Neither agent agreement nor exact numerical agreement establishes physical validity.

The fixed engineering requirement is at least a10% median paired improvement over L, with5/6strict wins, on EACH5000case, and no median paired regression to A. Two independent seeds and six repeats within one process cannot support a population claim. Failure ends this storage-variant line; no chunk-size or seed sweep follows.

Before execution, status is hypothesis. Read PROTOCOL.md, SCHEMA.md and config.json for exact bounds; source-manifest.json freezes sources/dependencies. SOURCE-RESTART.md records one-shot execution. Result files, a plain-language milestone, ledgers and a Three.js saved replay will follow the frozen experiment or its preserved failure. The broader publication and live-browser goals remain open.
