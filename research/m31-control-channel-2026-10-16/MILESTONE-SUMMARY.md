# What changed at this checkpoint

**We now have one successfully tested way to save a small piece of browser-produced evidence.** The browser returned 3,840 synthetic bytes through its automation connection. The host saved the actual returned bytes, and a separate checker read the closed file and found an exact match.

This matters because missing saved output had prevented us from judging earlier numerical work. It gives us a candidate path for collecting future evidence. It does not recover the missing earlier output or explain its cause.

The test used ordinary browser memory. We still need to establish whether a GPU buffer can be copied, released and transferred correctly, and what the chosen transfer method costs for realistic output sizes. The small successful trial gives no failure-rate estimate or large-swarm speed claim. The aerodynamic model still needs compatible physical measurements.

One preregistered trial completed. The independent saved-record review passed five groups with zero errors. The records include the actual return, saved binary, trace, source/runtime bindings, resource observations and actual tool completion. Private ownership records remain private. No browser permission or security setting was changed.

The [Three.js milestone](http://127.0.0.1:8876/research/m31-control-channel-2026-10-16/viewer/) lets you follow five observed stages and inspect the actual events. It is clearly labeled as an engineering evidence diagram. The source, test and review are preserved; neither invocation will be repeated in this evidence directory.
