# Next test: avoid unnecessary distance calculations

The current code calculates an exact-runtime center distance even for drones far outside its interaction neighborhood. We identified a small change that may skip many of those calculations using current coordinate differences. It keeps current positions, motor commands, interactions and the same ordering.

We will test the change against the unchanged implementation on fixed controls and newly generated 3D Boids states. Every pair classification, coefficient and solved load must agree on the tested inputs before timing can support a performance claim. This is an ordinary optimization; its benefit has not been measured.

The source review did not establish a guarantee for every JavaScript runtime or possible input. One reviewer accidentally read a historical results file, which is recorded rather than hidden. The constants remain those proposed before that exposure, and the new experiment will preserve this limitation.

This desk decision creates no new numerical result. The [root-secant Three.js replay](../m31-root-secant-2026-10-16/viewer/) remains the latest completed numerical view until the separately frozen experiment finishes.
