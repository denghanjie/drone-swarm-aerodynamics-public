# Receiver supervision: detached browser process finding

Static review only, 2026-10-16. No browser/process launch, module import, shader compilation, scientific evaluation or repository edit.

The revised browser/driver snapshot (experiment.cjs SHA256 54bd55081251017624ef67617383f8faeadee7ad17bbe36c80ad2e192c8ea217; browser.js bc1bb85d7da74e2506158ede9a2abb67b026582e3e95d4b549ecb1f7f5e19098; run-once.py 4c4a7ae18589740b047f1bcd0142fa8b8c5a9c5f8156df5c52a3a353d82f290f) addresses the four earlier local-code failure paths with two-phase raw persistence, cached failure evidence, deterministic source routes, independent cleanup attempts, and unconditional final Node-group cleanup. It still cannot claim complete browser containment because the installed dependency detaches the browser.

Dependency inspected by text read:
<NODE_MODULES>/playwright-core/lib/coreBundle.js
Package version: 1.62.1
Bundle size: 3,425,603 bytes
Bundle SHA256: 9393fa79e1c67c74edc26b610d65a4f7ed73d345a762465cc88340a33a2454ac

Relevant source lines:
- 8898: async function launchProcess(options).
- 8902–8903: the source comments explicitly say detached:true on non-Windows makes the child leader of a new process group for kill(-pid).
- 8905: detached: process.platform !== "win32".
- 8911: childProcess.spawn(options.command, options.args || [], spawnOptions).
- 8995: the dependency's own forced cleanup uses process.kill(-spawnedProcess.pid, "SIGKILL").
- 39543–39555: BrowserType launches the prepared browser executable/arguments through this launchProcess helper, with pipe stdio. This is the relevant browser-launch path, not merely an unrelated helper occurrence.

Consequently, os.killpg(NodeLeaderPID, SIGKILL) does not include Chromium's independently created group. Normal browser.close can terminate the browser; the authoritative hard watchdog cannot assume that method runs when Node is killed or stuck. This remains a launch blocker for the promised containment contract.

A public-API route is chromium.launchServer with the existing channel/headless policy, a loopback-only control listener, and synchronous registration of browserServer.process().pid before any connect/page/GPU action. The supervisor must kill and confirm absence of both the Node group and the registered browser group. BrowserServer.close/kill must be used for owned browser cleanup; closing a connected client alone is insufficient as a process-lifetime argument.

The installed BrowserServer implementation supports the proposed ownership registration: coreBundle lines 56864–56868 define process() as browser.options.browserProcess.process, close() as browserProcess.close(), and kill() as browserProcess.kill(). The launchServer return is after browser startup and control-listener startup, so the implementation also needs a bounded pre-registration launch-failure cleanup story. A narrow spawn-time ownership registry or supervisor-owned descendant discovery can cover that interval. Registration must never be used to select unrelated user browser processes.

Pin the inspected bundle or otherwise explicitly bind the process-control dependency used by the final supervisor argument. The current runtime-provenance record candidly pins executable/package entries only; those entry hashes alone do not establish an unchanged internal spawn/kill implementation.

The original /tmp/m31-browser-receiver-static-review.md and first full /tmp/m31-browser-receiver-static-followup.md remain unchanged. This note does not clear launch or spend any scientific/saved-review budget.
