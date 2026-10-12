# Evidence milestone — model decision

## Decision

Proceed to the first 50-drone **navigation baseline without aerodynamic interactions**. This can establish that the route, avoidance, controller, timing and measurements work. It cannot establish real swarm safety or downwash-sensitive throughput.

Keep the current interaction model for explicitly labeled sensitivity experiments. Do not replace it with an existing simulator's downwash formula merely because that formula is published in code. No candidate reviewed here has earned a matched physical-validation claim for our configuration. Steps 3–4 remain open as evidence gates; Step 5 may begin as an engineering pilot.

## Evidence checked

**Bauersfeld et al.** supplies a far-field mean-airflow model, not a calibrated fixed-command rotor-force law for our 27 g vehicle. Its tested vehicles span 230 g–6.3 kg. We retain the published wake equation as a candidate, with vehicle transfer and the exact length convention still requiring reconciliation. Our existing implementation uses a 56 mm adjacent-motor spacing; this audit did not establish that it matches the paper's diagram. No silent geometry correction was made. [Paper, Sections III, IV-B and VI](https://arxiv.org/html/2403.13321v3)

**Kiran, Ayanian and Breuer** provides closer-scale experimental evidence. The experiment holds the supply at 4 V with a hover PWM command; this differs from our constant ideal-induced-power assumption. Section III-A reports remaining thrust of 95–98% beyond a normalized vertical separation of 19; its stated 32.5 mm scale implies 0.6175 m. This is a textual summary, not a table of independent samples or an uncertainty interval. Inconsistent nearest-separation wording is excluded. The linked raw dataset was not retrieved: the DOI failed through the current web tool, with a human-verification page encountered in earlier work. We did not bypass it. [Paper](https://arxiv.org/html/2507.09463v1) · [Dataset DOI](https://doi.org/10.26300/64d4-wa17)

**Gielis et al.** compares measured multi-neighbor forces with additive and learned aggregation. It supports testing aggregation rather than assuming it. We did not locate a complete executable model/data package with established reuse terms in this focused search. The paper's results therefore inform our experimental design, but cannot serve as a numerical ground-truth oracle in this project. [Aggregate study](https://arxiv.org/html/2312.03488v1)

**Neural-Swarm repository.** The inspected README refers to additional Box-hosted data. A complete anonymous download, model provenance and applicable reuse terms were not established here. No training or reproduction is claimed. This does not establish that suitable data are unavailable elsewhere. [Repository](https://github.com/aerorobotics/neural-swarm)

## A concrete compatibility screen

We evaluated two equations at fixed, level hover motor states, with a source centered directly above the receiver. These are equation outputs, not free-flight results:

| Vertical gap | Current hypothetical rotor model: remaining lift | Pinned simulator equation: remaining net support |
|---|---:|---:|
| 0.65 m | 84.6% | 32.2% |
| 0.80 m | 85.9% | 55.3% |
| 1.00 m | 87.5% | 71.4% |

The paper's 95–98% textual range makes automatic calibration claims inappropriate. **This is not a measured prediction-error calculation:** vehicle geometry, motor operating conditions, and force accounting are not matched. We neither fit to the range nor manufacture individual data points from it. The screen flags incompatibility in our attempted transfer; it does not disprove the published airflow model or establish the error of the source simulator in its intended setting.

For the hypothetical model we query the existing wake/rotor function at the nominal 27 g geometry and still-air hover motor states. At 1.0 m and 1.1 m we evaluate only the stationary load function; the earlier flight UI's 0.8 m configuration cap is not extended. Its force change is incorporated through rotor thrust, once.

For the simulator reference, we independently transcribed the scalar expression at commit `7ebad1ecabd28a7000add2d05f888aa2e837c2cc`:

```
alpha = 2267.18 × (0.0231348 / (4 × gap))²
beta = 0.16 × gap − 0.11
loss = alpha × exp[−0.5 × (horizontal_distance / beta)²]
```

The upstream positional condition requires positive gap and horizontal distance below 10 m. It applies the downward force in the recipient link frame. Our screen is restricted to level vehicles and does not reproduce full PyBullet dynamics. “Remaining support” here means `(mg − loss)/mg` at nominal hover thrust, using our `g = 9.81`; it is not a rotor-efficiency measurement. The pinned implementation uses `g = 9.8` for its own gravity parameter.

The width beta vanishes at 0.6875 m. At the centerline the expression divides zero by zero; near that gap, off-axis behavior is highly sensitive. Negative beta also needs physical interpretation even though its square yields a finite equation value. Our audit reports near-zero width as **unknown**, not zero disturbance, and does not repair or silently smooth the source law. This is a mathematical finding about the inspected code/coefficients, not a claim about all releases of the simulator. [Pinned implementation, `_downwash`](https://github.com/learnsyslab/gym-pybullet-drones/blob/7ebad1ecabd28a7000add2d05f888aa2e837c2cc/gym_pybullet_drones/envs/BaseAviary.py#L743) · [Pinned coefficients](https://github.com/learnsyslab/gym-pybullet-drones/blob/7ebad1ecabd28a7000add2d05f888aa2e837c2cc/gym_pybullet_drones/assets/cf2x.urdf)

## What is ready, and what is not

Ready: a mechanics implementation, reproducible interaction hypotheses, documented numerical limitations, an audited reference equation, and a concrete navigation-baseline specification.

Not ready: measured force/moment accuracy, a validated aggregate model, real-flight safety claims, GPU scaling claims, or an established novelty claim.

There is no reason to tune the controller until an assumed model merely looks stable. We can now test the navigation machinery separately. Later, add supported interaction models and measure how much they change the same task. If evidence remains inaccessible, frame the final project as an explicitly conditional simulation/sensitivity study rather than a physically validated swarm predictor.

## Reproducibility and verification

`milestone-02-source/audit.cjs` generates 21 stationary comparisons, a CSV, and six numerical checks. It uses the existing local mechanics/wake implementation and directly recorded pinned coefficients. Checks cover the analytic centerline formula, zero-width handling, positional exclusions, regression, finite outputs and preservation of the distinction between a published range and individual measurements. These are software checks, not six physical-validation tests.

Run from the workspace root:

```sh
node outputs/milestone-02-source/audit.cjs
```

Outputs: `milestone-02-audit.json`, `milestone-02-audit.csv`, and `milestone-02-verification.json`. The executable decision record is `milestone-02-model-decision.json`. No old simulation or result is overwritten. Public paper/source access was intermittent; source claims above are grounded in retrieved web text and pinned local parameter files, not incomplete shell downloads.

## Next milestone under the original eight steps

Build the approximately 50-drone virtual-gate pilot using the original Step 1 settings, fixed seeds, identical navigation/control settings, full-horizon crossing counts and swept separation checks. Start with no interaction. Verify timing, completion, collisions and motor limits before interpreting any comparison with an uncertain aerodynamic model. Details remain in [the roadmap](research-roadmap.md) and the model-decision JSON.
