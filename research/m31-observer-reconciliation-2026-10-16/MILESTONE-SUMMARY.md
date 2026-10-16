# Observer source checkpoint

The old monitor can reject a registered browser if registration becomes visible between its registry read and its process snapshot. Four deterministic source cases demonstrate this possibility and show that the same error also occurs for a truly unregistered descendant. They do **not** identify the cause of the historical failed run.

The old cleanup expression can report success without resolving that descendant. We retained this limitation rather than claiming that a process survived or that every process was closed.

A small, pure helper now classifies one retained snapshot using coverage supplied before and after one registry refresh. Anything still unadmitted is retained permanently for that invocation and prevents a complete observed-process closure claim. The caller must validate ownership and preserve the ledger. The helper neither inspects nor controls processes, and it is not integrated into an operational observer.

This is an ancillary software checkpoint. It supplies no new GPU result, drone trajectory, physical validation or speed measurement. The latest visible [Three.js evidence view](../m31-gpu-readback-trial-2026-10-16/viewer/) still shows the actual terminal trial failure. The next scientific priority is the source-strength contract: a powered wake must respond to the source's actual operating condition. More GPU arithmetic would not by itself repair that physics gap.

Read [the claim ledger](CLAIM-EVIDENCE-LEDGER.md), [helper contract](helper/CONTRACT.md), [exact old-source witnesses](frozen-witness/README.md), and [restart instructions](RESTART.md). Earlier trials and their failures remain unchanged.
