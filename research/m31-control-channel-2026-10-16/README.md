# M31: a small evidence transfer succeeded

**The browser returned the 3,840-byte synthetic payload through its existing automation connection, and an independent post-closure check found the saved file exactly correct.** This supports that one small engineering path. It does not validate GPU output, large transfers or the drone physics.

The trial used the [published source commit](https://github.com/denghanjie/drone-swarm-aerodynamics-public/commit/4edf40a7cbfa2d41414dc8a8a6ff0718d0fa5671), independently verified before invocation. The same source freeze included the separate saved-evidence checker. One trial and one saved review are terminal; the review passed all five groups with zero errors. All older failed attempts remain unchanged.

- [Plain-language milestone summary](MILESTONE-SUMMARY.md)
- [Visible Three.js evidence diagram](http://127.0.0.1:8876/research/m31-control-channel-2026-10-16/viewer/)
- [Observed results and limits](OBSERVATIONS.md)
- [Frozen protocol](PROTOCOL.md) and [source contract](SOURCE-CONTRACT.md)
- [Independent report](review/results/report.json) and [external disposition](publication/FINAL-DISPOSITION.json)
- [Claim–evidence ledger](claims.json) and [source ledger](SOURCES.json)
- [Restart and next question](POSTRUN-RESTART.md)
- [Presentation QA](viewer/VISUAL-QA-NOTES.md) and [privacy review](PRIVACY-REVIEW.md)

The viewer binds 21 actual events and 19 backing files before rendering. It is an engineering diagram and links the earlier genuine local 3D Boids replay with airflow off. It does not depict a new flight or aerodynamic result.

The long-term target remains a defensible accuracy–computation result for 5,000 drones with local 3D Boids and physically meaningful mutual aerodynamics. No publishable contribution or fully validated coupled simulation has yet been established.
