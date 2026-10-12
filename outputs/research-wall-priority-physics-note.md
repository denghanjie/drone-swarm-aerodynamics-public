# Why the wall margin helps — and what it does not prove

The controller asks each drone to slow down before its body reaches a wall. The wall-priority correction prevents another movement request from undoing that instruction. That can improve the calculation without changing the flock’s social rules.

The important physical distinction is between **requested velocity** and **actual velocity**. A quadrotor must tilt, change rotor thrust and respond through motor lag. It cannot instantly acquire the requested velocity. A mathematically valid velocity request alone therefore does not establish collision-free flight.

## A conditional calculation

Let `c` be surface-to-wall clearance: distance from the drone’s center to a static solid, minus the 0.075 m body radius. Let `n` point away from the wall. In the ideal continuous-time interpretation, the current request obeys

`n · v_requested ≥ −(c − 0.3) / 1.2`.

The margin is 0.3 m and the response horizon is 1.2 s. If the actual outward velocity differs from that request by at most an adverse amount `ε`, then

`dc/dt ≥ −c/1.2 + 0.3/1.2 − ε`.

For a constant verified bound `ε ≤ 0.25 m/s`, that inequality points away from penetration at `c = 0`. More explicitly, with initial clearance `c₀`,

`c(t) ≥ (0.3 − 1.2 ε) + (c₀ − 0.3 + 1.2 ε) exp(−t/1.2)`.

If both `c₀` and `0.3 − 1.2 ε` are nonnegative, the lower bound stays nonnegative. This is a conditional comparison argument for an ideal continuously enforced wall constraint, not a safety theorem for the implemented simulator or a physical drone.

## What is missing from that condition

We have not established a uniform tracking-error bound of 0.25 m/s. The implementation updates at 100 Hz, holds commands between updates, and uses the normal and clearance from the last update. Changes in normal direction, sampled updates, sensing errors, motor limits and disturbances need explicit bounds before applying the continuous-time inequality. Finite solver residuals also consume the available margin.

Drone–drone separation requires a separate argument involving relative motion. Giving walls final priority can violate the pair requests. A successful wall correction therefore says nothing automatic about pair safety or passage capacity. A drone can avoid a wall yet wait in a queue, or contact another drone later.

The full-mission trials check what happens in the specific numerical cases. Their pre-contact records identify whether a final requested velocity violated a constraint and what the actual velocity and motor commands were. Numerical refinement checks consistency of the calculation; independent flight measurements are still needed for physical accuracy.

This note derives the inequality from the implemented margin and horizon. It adds no new controller or gain and is not used to tune the frozen milestone 31 trials.
