# Milestone 9 — complete-loop computational scaling

The current hybrid design is faster than real time at 1,000 vehicles in this short queue workload, and slower than real time at 5,000. GPU acceleration does not eliminate CPU control, serialization, synchronization and neighbor-check costs. At 50 vehicles, CPU-only is faster.

| Drones | CPU full loop ms | GPU-assisted loop ms | GPU real-time factor | Max CPU/GPU position difference |
|---:|---:|---:|---:|---:|
| 50 | 33.5 | 54.2 | 18.45 | 0.0025 mm |
| 200 | 123.3 | 86.0 | 11.63 | 0.0025 mm |
| 1000 | 594.3 | 284.4 | 3.52 | 0.0040 mm |
| 5000 | 2969.9 | 1334.6 | 0.75 | 0.0110 mm |

Each value is the median of three one-second runs at 100 Hz, after a 10-step warmup at 50 drones for each backend. Timings sum the per-step wall intervals, include GPU upload/readback and safety checks, and exclude deliberate UI yields, initial allocation and rendering. They describe computation capacity, not observed end-to-end interactive FPS. CPU and GPU pairs use the same Float32-quantized initial conditions and the unchanged clearance scheduler with ideal state information. Body mechanics is RK4; control remains on CPU. All four comparisons meet the 1 mm final-position tolerance and match measured passage/stop/close-pair counts.

The five-column planar queue retains 0.6 m spacing as its length grows to approximately 600 m. Only the first second is simulated: no group has yet completed its passage. These results do not demonstrate that 5,000 drones navigate a narrow opening, handle complex terrain or respond to wakes. Most vehicles are waiting, so the timings do not characterize a dense, actively interacting crowd. Spatial hashing can degrade towards quadratic work in dense cells.

The swept-segment neighbor search inserts expanded segment bounding boxes into all intersected cells and checks each candidate pair once. It was compared against exhaustive all-pairs checks in 100 deterministic random configurations, including long sweeps, plus an explicit crossing with disjoint endpoints. All 101 checks passed. It measures threshold violations, not global nearest-neighbor distance. Additional browser-to-Node and frame integrity checks are saved separately.

For 5,000 drones, median component times per simulated second were about 475 ms control, 462 ms mechanics/transfers and 401 ms checking/measurement. Component medians are taken independently and need not sum exactly to the median total. Improving the integrator alone is insufficient; moving control and the spatial grid onto the GPU and keeping states resident is the obvious engineering experiment, not a result already demonstrated.

Separate instanced Three.js rendering tests used 5 warmups and 30 timed frames per size, with camera fitted to the full queue, interpolated positions, simplified body orientation and synchronous WebGL completion. Median display costs were 50: 0.30 ms, 200: 0.30 ms, 1000: 0.40 ms, 5000: 0.80 ms. Small bodies in a long queue are a light pixel workload; these values do not predict detailed, close-up rendering or total FPS with physics. Raw repeats and viewport are retained. The measured compute and display timings must not simply be added and called a verified real-time integrated application.

[3D scaling viewer](milestone-09-scaling.html) · [Loop measurements and recorded trajectories](milestone-09-browser-results.json) · [Rendering measurements](milestone-09-render-results.json) · [Protocol](milestone-09-protocol.json) · [Neighbor checks](milestone-09-neighbor-verification.json) · [Other verification](milestone-09-verification.json)

Reproduce via the same loopback server described in milestone 8, then use “Run scaling study” and “Measure rendering”. Results are appended under unique receiver filenames. `milestone-09-browser-results.json` is the pinned selected run. Original receiver records remain available for traceability.
