# Prospective claims

| Claim | Status before execution | Challenge |
|---|---|---|
| Effective rotor loads replace nominal axial force/moment without double counting. | Source-reviewed implementation hypothesis. | Synthetic single-rotor impulses; independent saved derivative checks. |
| The small fixed-command feedback trajectories are numerically resolved at declared tolerances. | Untested. | Three fixed timestep levels, all common endpoints, exact retained failures. |
| The same adapter works with local3D Boids and time-varying nominal commands. | Untested conditional exploratory question. | Only run if all primary gates pass; retain any domain/contact/numerical failures. |
| The aerodynamic law represents real drone interactions. | Unresolved. | Needs compatible independent physical measurements; this experiment cannot establish it. |
| A5000-drone browser accuracy–computation contribution is established. | Unresolved. | This small Node diagnostic supplies neither browser timing nor physical validation nor novelty. |

Mathematical consistency, finite-domain behavior, numerical resolution, and physical accuracy are different claims. Time refinements are correlated evaluations of a single designed initial condition, not independent physical trials.
