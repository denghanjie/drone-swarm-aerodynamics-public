# Presentation contract

This is a Three.js diagram of saved transport evidence. Box positions, size, connecting line and camera are display aids; they are not measured drone positions or packet trajectories. No flight, aerodynamic or transport experiment runs in this viewer. WebGL renders the diagram only.

The browser first checks the exact bytes of `evidence.json` against `binding.json`, then every listed supporting file. This is a consistency check against the supplied binding, not external authentication. Failure clears the scene and disables result controls. The generated evidence artifact retains the source paths and record references used for each stage, full recorded event order, diagnostic disposition and review status. Missing stages stay unknown or explicitly incomplete; no missing output is synthesized.

The static binder is prepared only after terminal evidence and review. The public result manifest pins both raw/derived files and presentation source. QA covers desktop/mobile, every stage, first/last events, camera and keyboard controls, exact displayed records and intentional data corruption/recovery. No screenshot or viewer elapsed time establishes simulation performance.
