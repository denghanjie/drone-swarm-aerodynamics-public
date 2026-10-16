# Independent saved-data acceptance

Accepted as a bounded numerical and descriptive source-accounting audit. All 46 checks passed in one authorized independent review. Frozen source commit `b515ac7a0b146ebf337431fb492d145d9a43c619`, freeze SHA-256 `e343f288205b27e0996a6141db6af20ea4ab2f5be2ab5e0eb3ca5b6cd287eca3`, source pins and committed source blobs agree.

- All five source motor arrays and twenty saved field records were checked, including every policy field. All records are identical and positive: 2.5241780354649195 m/s. This is the current static model's motor-insensitivity, not measured shutdown behavior.
- Four saved quadrature levels and their convergence records agree with the analytic normalization. Independent Decimal arithmetic gives untruncated J/(mg) = 0.71677251025819184. A separately written four-point Gauss-Legendre check, using 16 and 32 panels on the fade interval and an analytic inner disk, gives radial retention 0.9713664384367813. Its radial integral differs from the saved final Simpson result by 3.069766663088558e-14. This review used 192 new quadrature evaluations and did not rerun the author routine.
- All ten planes and 410 profile points were checked: 1,230 velocity values and 2,050 numeric profile fields. Maximum profile discrepancy was 8.881784197001252e-16. Both fades, zero fields at and beyond 2.5 m, and nominal radial cutoff labels are consistent.
- Independent printed-number arithmetic gives squared-frequency ratio 1.3467459228776101 and flow-load ratio 1.3641025641025641, with relative difference -0.01272385352957153. Last-digit sensitivity endpoints agree. The printed component sum 9.22 N and separately reported total 9.21 N remain distinct.

The saved worker and tool receipts report successful completion. The tool wall field (0.045202917 s) is smaller than the driver interval (0.154138292 s); both are retained without reconciling their scopes. This is not nested stopwatch verification or a performance result.

J is a squared scalar-profile proxy, not measured thrust or a complete momentum balance. The paper geometry convention remains unresolved. Wolf's arithmetic is a descriptive reproduction of already-seen printed values, with no inferential acceptance threshold; its primary article was not independently reopened. No new physical measurements, calibration or flight qualification follow.

The independent review stayed below its 30 s CPU and 2 MiB output limits. No original audit import, source witness rerun, original runner invocation, browser/GPU activity or process-table observation occurred. The review plan was fixed after inspecting the author's saved results and is not a held-out confirmation. Raw checks, the exact review script and their inventory accompany this note.
