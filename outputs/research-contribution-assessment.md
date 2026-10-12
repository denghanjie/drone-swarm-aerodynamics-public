# Contribution assessment — 12 October 2026

## Current position

This is a reproducible simulation benchmark and a record of failure mechanisms. It is not yet evidence of a new flocking algorithm or validated aerodynamic accuracy. A visually convincing group is a useful demonstration, but does not establish either claim.

## Closely related work checked

|Prior work|Relevant established capability|Implication for this project|
|---|---|---|
|[Vásárhelyi et al., 2018, author project page](https://vasarhelyi.github.io/drone-project-site/scirob2018.html)|Distributed flocking with obstacle handling, optimized parameters, real flights with30 drones and simulation at1,000.|Local flocking, obstacles and a thousand simulated agents cannot by themselves be our novelty. Virtual GPS obstacles in that work are not interchangeable with our synthetic solid factory.|
|[Neural-Swarm2, 2021](https://arxiv.org/abs/2012.05457v2)|Learned aerodynamic residuals integrated with heterogeneous swarm planning and tracking control.|Accounting for downwash in a swarm is established. Our local emergent-motion task differs from assigned trajectory tracking, but that distinction alone does not establish superiority.|
|[Gielis et al., 2023](https://arxiv.org/abs/2312.03488v1)|Measured aggregate interactions, nonlinear aggregation and learned comparison against simpler linear models.|Linear addition and root-sum-square must remain assumptions. Our comparison cannot decide their accuracy without aggregate reference data.|
|[Bauersfeld et al., 2024](https://arxiv.org/abs/2403.13321v3)|A normalized mean far-wake model and a controller application.|The wake equation is reused prior work. Correct normalization is necessary; it is not an original contribution.|

This is a focused prior-art check, not an exhaustive literature search or proof that no similar benchmark exists. We have not reproduced those systems under matched conditions, and must not claim to outperform them.

## Potential research contribution

A useful question is: **Which simplifications preserve mission outcomes and force predictions, at what computational cost, and where do they fail?** The benchmark can contribute an inspectable experimental method: the same genuine local3D flock, solid geometry, matched starting states, separately varied force/moment assumptions, timestep checks and preserved counterexamples.

To turn that into a strong research result, we need independent force/wake observations matched to the vehicle and actuator conditions, externally comparable baselines, error estimates on held-out configurations, and computation measurements under controlled conditions. The current protocol provides groundwork and negative evidence; it does not yet provide the accuracy axis of an accuracy-versus-cost result.

## What the present evidence can answer

- Can we build and run local3D drone flocks in a complex synthetic environment? Yes, within the stated model and tested small-count missions.
- Does this navigation controller remain safe just because smaller flocks complete? No. The retained1,000- and5,000-drone wall contacts are concrete counterexamples, repeated against the same drone/wall at smaller timesteps.
- Does a smooth Three.js replay mean real-time simulation? No. Recorded rendering and actual integration costs are separately measured.
- Do different assumed aerodynamic loads cause different simulated trajectories? Yes, in the completed corrected matched study: all five primary airflow-off cases finish, while all15 active-airflow cases stop early. A separate airflow-update sensitivity check fails, so this does not establish converged aerodynamic trajectories. The adjacent-motor version is retained as an implementation error.
- Are those loads physically accurate? Unestablished. Numerical consistency cannot answer that.

## Decision

Use the bounded benchmark and its cost comparison as groundwork. Preserve failures instead of indefinitely tuning the controller until it looks successful. The next substantial scientific investment should be independent physical evidence and matched external baselines. Additional visual complexity alone has diminishing research value.
