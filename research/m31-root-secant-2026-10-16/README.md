# Can a straight-line forecast improve the saved rotor loads?

Holding the old rotor-load ratios for10ms failed the preceding experiment. This checkpoint tests one small alternative: extend the trend between the two most recent actual ratios. At startup there is only one old value, so the rule must hold it. We include that first interval and every later endpoint.

The input flight has already happened in simulation. We keep its exact poses, motor states and freshly computed reference loads, and compare the two approximations at those same states. This makes the question clear: how much load error does the specified forecast make? It does not yet tell us how a flock driven by that forecast would fly.

Before running, the protocol, code, input and independent checker are frozen and published. The complete result, including invalid predictions or failures, will be retained. There is one candidate invocation and one audit, with no tuning or retries. Read PROTOCOL.md and config.json for the precise scope; source/ contains the auditable arithmetic and supervisor. New results will be accompanied by an exact-pose Three.js diagnostic and a plain-language milestone summary.

This is a development test of an established prediction idea on a different coupled model. Physical accuracy, useful error-triggering, novel contribution and efficient5000-drone flight remain unresolved.
