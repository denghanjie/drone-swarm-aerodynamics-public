# Evidence locations

All repository locations are pinned to commit `934a1ab92c458cad99c9278a5cb63bf68af6e56c`. Only the README, LICENSE, two YAMLs and structural API manifests were read; no claim is made to have inspected every data record.

| Finding | Source location |
|---|---|
| Instrumented flying mass 40.85 g; stock configuration 27 g | [README, Overview, line 48](https://github.com/syediu/nanobench/blob/934a1ab92c458cad99c9278a5cb63bf68af6e56c/README.md#L48). Current [paper v2](https://arxiv.org/html/2603.09908v2), §III-A Hardware Platform, explicitly agrees and describes 46 mm diameter propellers. |
| CSVs have offline alignment and interpolation onto a 100 Hz Vicon timebase | [README, Time Synchronization, line 135](https://github.com/syediu/nanobench/blob/934a1ab92c458cad99c9278a5cb63bf68af6e56c/README.md#L135); paper v2 §III-B Data Acquisition Pipeline and §III-C Time Synchronization. Nominal log rates are not raw sample rates. |
| Battery voltage is forward-filled | [README, CSV Column Reference, line 160](https://github.com/syediu/nanobench/blob/934a1ab92c458cad99c9278a5cb63bf68af6e56c/README.md#L160). |
| EKF uses Vicon pose updates | [README, CSV Column Reference note, line 162](https://github.com/syediu/nanobench/blob/934a1ab92c458cad99c9278a5cb63bf68af6e56c/README.md#L162); paper v2 §III-B, Vicon path. Agreement between this aided estimator and Vicon cannot establish independent estimator validation. |
| BSD license explicitly includes data | [README, License, line 383](https://github.com/syediu/nanobench/blob/934a1ab92c458cad99c9278a5cb63bf68af6e56c/README.md#L383), plus the preserved LICENSE. |
| Per-stream raw sample counts and battery endpoints | Included A1b and C4 metadata YAMLs; each exactly matches its public Git blob ID. These two examples do not establish all metadata quality. |
| 107 CSV / 107 YAML / 87 distinct CSV blob IDs | `nanobench-pinned-manifest.json`, directory-scoped; cross-checked against `nanobench-tree-projection.json`. Complete repository tree includes 152 CSV entries, including benchmark data and result tables. This does not resolve the advertised recording count. |

The current paper is **v2, revised 16 September 2026**, not the earlier v1 examined during discovery. Its §III-A and the pinned README agree on instrumented mass; no current paper-versus-README mass disagreement is claimed. Paper §IV-A and the README advertise 172 recordings.

Zenodo dataset licenses and file sizes/checksums come from the exact record APIs identified in the two projections. Their descriptions are preserved, including MODERA's use notice. The air-duct hardware and sensor calibration identifier come from *Flying in air ducts*, Methods → Drone / Force measurements; its article license is separate from the dataset license.
