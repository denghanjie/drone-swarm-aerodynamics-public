# Milestone 8 — WebGPU mechanics agreement

The browser executed a real WGSL compute kernel on the reported GPU adapter (hardware identity withheld). All four sizes met the predeclared CPU/GPU component tolerances. These checks validate a port of the equations, not physical flight accuracy.

| Vehicles | CPU median (ms) | GPU + transfer median (ms) | Maximum position-component discrepancy |
|---:|---:|---:|---:|
| 50 | 11.80 | 0.50 | 0.0015 mm |
| 200 | 41.10 | 0.50 | 0.0018 mm |
| 1000 | 202.80 | 1.10 | 0.0051 mm |
| 5000 | 1000.50 | 1.20 | 0.0106 mm |

The task is 50 RK4 steps (0.5 simulated seconds at 10 ms) for independently evolving rigid bodies under fixed motor commands. Initial states and commands are identically rounded to Float32 before both paths. CPU arithmetic then uses JavaScript doubles; GPU uses Float32. This explicitly tests motor lag, quaternion attitude integration, gyroscopic terms, thrust and torque. There are no wakes, collisions or navigation.

Timing uses one warm-up and three repeats per size. GPU timing includes upload, dispatch, synchronization and readback, but excludes buffer allocation/compilation. CPU timing is the original allocation-heavy reference, not an optimized competitive implementation. GPU executes 50 steps per dispatch with fixed commands, so it avoids the per-control-step readbacks a closed-loop CPU controller needs. Values below a millisecond are sensitive to browser timer granularity. The timing advantage must not be presented as complete swarm acceleration, or as a comparison with other simulators.

Density is fixed at 0.6 m cubic-lattice spacing; volume increases with count. The 3D view uses actual initial/final states and explicitly labeled endpoint interpolation, not time-resolved flight trajectories. Browser metadata, raw repeats and endpoints are preserved in the result JSON. Device identifiers not exposed by the browser are left blank.

Next: measure the closed-loop navigation pipeline with control, transfers and separation checks included. This answers whether the component gain survives the rest of the workload. Original Steps 3–4 still lack matched physical interaction data.

[3D benchmark](milestone-08-compute.html) · [Frozen protocol](milestone-08-protocol.json) · [Raw browser results](milestone-08-browser-results.json) · [WGSL source](milestone-08-source/kernel.wgsl)

To rerun and save browser results, launch `python3 outputs/milestone-08-source/server.py` from the workspace and open port 8875. The receiver binds only to loopback; subsequent results receive unique filenames. The original run is preserved.

Measurement revision: the first run allowed the visualization animation loop to remain active. A second run explicitly paused rendering to isolate compute timing. Both are retained; this report uses the second run. Numerical agreement passed in both. The initial record is [preserved here](milestone-08-browser-results-initial.json).
