# MODERA selective-access attempt

**The archive index remains uninspected.** One bounded Python URL-open attempt ended with `URLError: EOF occurred in violation of protocol (_ssl.c:1129)`. No HTTP status was recorded and the application read no response-body bytes. This does not establish that the server rejected ranges, that the archive is unavailable, or which network component caused the failure. The planned second range was never attempted. No archive member, scientific measurement, or complete archive was acquired.

The pre-acquisition plan and exact executed source are retained beside `acquisition.json`. The external command returned exit 0 because the script catches and records failures; its result status is `incomplete`, not success. Actual tool execution wall observation was 0.376657167 seconds. No request or worker remains active. Do not rerun this bounded attempt or silently replace its outcome. A future acquisition must separately specify its client, unchanged access controls, caps, provenance and failure handling.

This was ancillary data-access work following the public dataset review, not a substantial scientific milestone. The [latest Three.js evidence view](http://127.0.0.1:8876/research/m31-control-channel-2026-10-16/viewer/) remains bound to its completed control-channel experiment; it does not display this failed metadata acquisition as physical data.

## What to inspect once actual force files become available

The [provider's archived description](../m31-followup-planning-2026-10-16/datasets/zenodo-17457069-projection.json), `metadata.description`, documents motor order and balance axes, and describes seven force CSVs at seven vehicle angles. These are provider descriptions, not internally verified schemas. In particular, the balance x-axis points toward the microphones: it points forward at vehicle angle 0 degrees and rearward at 180 degrees. Its z-axis points upward along positive thrust.

Do not pool horizontal force and moment components across angles before verifying the angle sign, frame transformation and moment reference point. For a verified orthogonal frame rotation R, vector components transform as F_body = R F_balance. Moments at the same physical point transform similarly; changing the reference point additionally requires the corresponding lever-arm cross force. This is a coordinate identity, not an empirical finding about these files. The seven angle acquisitions may be useful for consistency checks, but their independence, calibration, repeatability and boundary effects remain unverified.

The next useful acquisition target remains the seven force files' actual headers, units, data rows, timestamps/averaging, motor settings, calibration and uncertainty. Spatial airflow and matching nanoquad hardware remain separate evidence gaps. No model fit or physical-validity conclusion is supported here.

## Provenance and publication scope

Universitat Politècnica de València, *UAV digital model and experimental tests* (2025-10-27), Zenodo v1, DOI [10.5281/zenodo.17457069](https://doi.org/10.5281/zenodo.17457069). Source metadata and license were verified in the preceding published dataset review. The dataset declares CC BY-SA 4.0 and the provider's research/education notice is preserved there. No new dataset payload is redistributed in this package.

Public artifacts contain only the plan, acquisition code, scoped failure record and this interpretation. The source URL is public; no credentials, personal paths, profiles or machine identifiers are included. The manifest inventories actual saved bytes. It does not establish physical truth or archive integrity.
