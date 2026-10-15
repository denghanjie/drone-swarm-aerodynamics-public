# Reproduction and evidence access

The original scientific and saved-review attempts are single-use. Preserve their locks, budgets and raw files. Do not rerun them in place. Independent reproduction, if separately authorized later, must use a fresh checkout/output directory and remain distinguishable from this historical attempt; it cannot repair or overwrite its outcome.

The exact executed scientific source is commit `4f2ead30ce48e4845ceefc105f9796ce468d907e`. Its freeze pins 51 source/protocol/review/input/provenance files. The private publication receipt records independently fetched GitHub commit/freeze bytes and their local reconciliation. The result manifest records actual published artifacts and transformations.

The historical invocation used Python 3.9.6 to run `source/run-once.py`, passing the pinned Node24 executable and `source/experiment.cjs`. `NODE_PATH` selected installed Playwright1.62.1; `RESEARCH_SOURCE_COMMIT` identified the source commit. Full command structure is in `results/launch-provenance.json`; local runtime/root paths are replaced by documented placeholders. The supervisor supplied a private process registry automatically. No full inherited environment dump is published.

Read `schema.json` before decoding data. Binary files use little-endian storage. Original rows contain eight binary64 values; GPU rows preserve eight returned binary32 words; Q/A reference rows contain six binary64 values. For the large inputs, record index equals four times drone ID plus rotor ID. Original saved I roots were reused; new references comprise only 32 scalar R roots and all Q/A roots. The independent checker performs no new root solves or GPU dispatches.

To view saved evidence, serve the repository root with an ordinary local static HTTP server and open `research/m31-browser-receiver-2026-10-16/viewer/`. The current local server is already on port8876. The viewer uses the existing local Three.js distribution and checksum-checked recorded inputs. No scientific experiment runs on page load. The historical Boids replay is `outputs/milestone-31-lab.html` and remains clearly separate.

The viewer data-packaging script only hashes/links saved files. Its QA is a UI/value-display check, not a second scientific verification or a performance test. Published independent-checker and QA copies disclose any removed local paths; original exact bytes, arguments and logs remain private.
