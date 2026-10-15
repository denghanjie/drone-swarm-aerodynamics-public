# Coordinate-origin diagnostic: no candidate

The recorded comparison selected **no candidate**. A, B and C qualified at origin `[0, 0, 0]`. On the paired copy at `[64, -32, 16]`, ordinary single-precision positions failed the interface gate, so A and B were skipped. C's high/low positions recovered the original coordinates and passed the decoded-input gate, but its GPU terms failed the unchanged error gate. Its translated serial reduction was therefore not dispatched.

In plain language: moving the same positions to a different coordinate origin exposed a precision weakness. Keeping extra position digits did not qualify the tested GPU implementation. The reason is not yet established.

**No broader confirmation was earned or run.** The frozen decision rule requires an arm to qualify at both origins. Lower error in some rows cannot replace the missing or failed required cells.

**Independent review completed but failed its aggregate integrity gate.** It recorded two final-control bookkeeping mismatches. Static source inspection identifies a checker lifecycle-assumption error; the saved API record matches the frozen source. The immutable failed report and exit code remain unchanged, with no retry or waiver. Read the [disposition](INDEPENDENT-SAVED-REVIEW.md), [exact report](results/independent-review.json) and [external closure](results/saved-review/runtime.json). The observations below retain their recorded status; no complete independent qualification is claimed.

[Open the saved-evidence viewer](viewer/) · [Original terminal result](results/result.json) · [Claims](claims.md) · [Inspection guide](REPRODUCIBILITY.md)

## The recorded six cells

| Origin | Arm | Required interface | Saved outcome | Serial output |
|---|---|---|---|---|
| `[0, 0, 0]` | A | Q0 passed | Qualified | Retained; combined gate passed |
| `[0, 0, 0]` | B | Q0 passed | Qualified | Retained; combined gate passed |
| `[0, 0, 0]` | C | Q1 passed | Qualified | Retained; combined gate passed |
| `[64, -32, 16]` | A | Q0 failed | Skipped by interface gate | Not dispatched |
| `[64, -32, 16]` | B | Q0 failed | Skipped by interface gate | Not dispatched |
| `[64, -32, 16]` | C | Q1 passed | Term gate failed | Not dispatched |

The translated [Q0 report](raw/o1-Q0-assessment.json) and [C term report](raw/o1-C-terms-assessment.json) each record 12 numerical L1-gate findings. [Q1 passed](raw/o1-Q1-assessment.json). Original R consistency, literal controls, the declared precision stimulus and useful positive exposure passed in the driver reports. No missing GPU cell is a measured zero or a counterfactual result.

## What was compared

One fresh synthetic scene contains 5,000 sources and four selected receivers—IDs 749, 500, 2250 and 4750—with four rotors each. The two origins, three arms and receiver observations share that scene and are dependent. This is not a 5,000-receiver flight simulation. The upper receiver's zero rows remain visible.

- **R:** existing host reference arithmetic on the original prepared binary64 inputs, at the matching origin. Its internal consistency does not make it an exact physical oracle or an independent replication against prior data for this fresh scene.
- **Q0:** the same host arithmetic on decoded A/B packed positions, axes, offsets and constants. **Q1** changes only positions to the binary64 sum of C's saved high/low words.
- **T:** actual retained GPU terms. A forms an absolute rotor point; B uses local-first subtraction with A's identical packed inputs; C adds high/low positions to B's structure. **S** is the optional serial sum of that same retained T buffer.

The frozen allowance is `1.8270441835956964e-5 m/s`, with `1e-12 m/s` reference allowance. Saved exact dyadic certificates decide the interface, term and combined gates; displayed decimals do not. Returned local vectors make arithmetic differences observable, but do not prove compiler reassociation or explain the earlier receiver-988 failure.

The run retained 185 raw files totaling 129,695,212 bytes. Recorded work was 10 dispatches, 320,000 GPU term slots and 48 serial output records. C adds 80,000 bytes to the 5,000-node position buffer. These are accounting facts, not a speed result; no physical-validity, portability or novelty claim follows.

## Evidence and scope

The exact [source publication](https://github.com/denghanjie/drone-swarm-aerodynamics-public/tree/ccafbd9b9fd3a3cdd7ffacb5fb360ee5f3dc1abc/research/m31-coordinate-origin-2026-10-16) is bound by [freeze.json](freeze.json). Retain the [prospective protocol](PROTOCOL.md), [literal controls](controls/controls.json), [raw outputs](raw/), [supervisor closure](results/budget.json), [review contract](REVIEW-CONTRACT.md), and [literature/result ledger](RESULT-LITERATURE-LEDGER.md). The protocol's prospective wording records its pre-exposure state.

The viewer displays saved numerical evidence. The [original M31 Boids replay](../../outputs/milestone-31-lab.html) is a separate historical demonstration with airflow off. Further scientific work requires a separately authorized, independently frozen question; this negative result does not reopen any closed budget.

The component allowance is much stricter than earlier body-output targets. [The separate budget audit](next-question/WHOLE-OBSERVABLE-BUDGET-AUDIT.md) explains why this failure does not establish that useful complete-query force accuracy is impossible. Those older targets are analyst-selected numerical requirements, not measured physical tolerances.
