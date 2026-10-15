# Milestone 31 restart: what the overnight work established

**We have useful component evidence and preserved failures, but no defensible breakthrough yet.** The goal remains 5,000 drones with local 3D flocking, credible flight dynamics and mutual airflow at a measured browser cost. No completed experiment establishes that combination.

## The findings in plain language

| Question | What the evidence says | Meaning for our next decision |
|---|---|---|
| Does skipping small airflow contributions provide a useful extra speedup? | In the [omission ablation](../m31-omission-ablation-2026-10-16/README.md), loads stayed within the chosen numerical limits, but the required extra speed benefit failed on both fresh inputs. Most measured savings belonged to the package that discards exact zeros. | Do not claim approximation itself caused the large package speedup. |
| Can simpler zero checks make it fast enough? | The [exact-zero campaign](../m31-zero-screen-2026-10-16/README.md) preserved saved forces bit for bit. Neither simplification met the preset usefulness rule at both sizes. The fastest reported 5,000-source CPU median was about 1.06 seconds per static query. | Fewer arithmetic operations did not imply a proportionate wall-time gain. This was not a full flight or browser benchmark. |
| Can the browser GPU calculate the rotor response accurately? | The [receiver component](../m31-browser-receiver-2026-10-16/README.md) passed its new 1e-7 N allocation for 24,032 valid inputs, with maximum error about 8.56e-9 N. The older 1e-12 N comparison failed for 24,022 inputs. | One finite component works at its declared engineering tolerance. It does not validate the whole pipeline or real physics. |
| Can the GPU calculate the wake accurately enough? | The [wake slice](../m31-browser-wake-slice-2026-10-16/README.md) exceeded its declared term-error budget for one of 16 receiving rotors, so addition was not run. The [coordinate diagnostic](../m31-coordinate-origin-2026-10-16/README.md) selected no candidate across both origins; its saved review also retained a bookkeeping failure. | Input representation and arithmetic remain issues. These strict component failures do not prove the complete force-output targets are impossible. |
| Do complete GPU body loads meet the application targets? | The [first body attempt](../m31-body-load-2026-10-16/README.md) stopped at runtime admission. This [distinct replication](README.md) passed admission but failed to save its first GPU control output. No main body-load family ran. | This question is still unanswered. A failed measurement transfer is not a numerical result. |
| Do these equations predict real drones? | The [physical source-contract review](../m31-source-contract-planning-2026-10-16/README.md) found an uncalibrated link between motor behavior and source wake. Compatible independent thrust, flow and receiver-response observations remain missing. | Implementation agreement cannot close the physical-validation gap. |

These are finite experiments on explicitly described inputs and hardware. Technical timing repetitions are not independent swarms, and a large number of scalar checks is not a sample of real flights. Each linked report preserves its source freeze, raw records, uncertainty limits, failed gates and separate review outcome.

The latest saved-record audit also failed: its metadata comparison wrongly expected an extra browser-version field in both objects. That mistake was missed during source review. The failure and uncompleted checks are retained; a static explanation is not a substitute for a passing audit. See [the review disposition](INDEPENDENT-SAVED-REVIEW.md).

## Where this leaves the original eight steps

The [eight-step roadmap](../../outputs/research-roadmap.md) remains the organizing framework. Historical Milestone 31 supplies genuine local 3D Boids with shared map guidance and 34 solids. Its airflow was off, and all original 1 cm individual-path refinement checks failed. Those failures remain visible.

The present work advances **provisional Step 6**, testing the calculations we might accelerate. Steps 1–4 still need compatible physical references; Step 7 lacks a qualified complete coupled browser simulation; Step 8 lacks a defensible accuracy–cost contribution and novelty case. A good replay is useful for inspection but does not complete those steps.

## What should happen next

Preserve and publish this terminal failure and its failed saved-record review. Do not restart any closed invocation or launch an automatic third runtime campaign. The new [Three.js view](viewer/) makes the saved CPU controls, missing GPU data and failed review explicit and links the historical flock's saved-pose audit.

The next numerical proposal should first isolate the evidence-transfer boundary with a tiny, known, non-scientific payload under a separately reviewed plan. Only after reliable persistence is observed should a future fresh complete-body query be considered. That is a proposed sequence, not an allocated or executed third campaign, and it does not reopen this one.

The next physical proposal is already documented: test a fixed mean-wake shape scaled by independently measured thrust against locked symmetric and unequal-motor conditions. The verified literature motivates that test, but currently available records do not supply the necessary compatible measurements. The source/receiver model must remain provisional.

No routine approval is needed to archive evidence or prepare a prospective plan within the research mandate. New work must respect the recorded allocation boundaries, the original 07:00 Shanghai launch cutoff, available resources and the requirement for genuine evidence. No paid service, installation, author contact or paper submission was used.
