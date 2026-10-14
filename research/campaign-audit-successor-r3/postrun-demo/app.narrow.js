// Results-only presentation. No model, benchmark, inventory, or release is loaded.
const el = id => document.getElementById(id);
const sameOrigin = path => {
  const url = new URL(path, location.href);
  if (url.origin !== location.origin) throw new Error('Selected evidence must remain on the same origin.');
  return url;
};
const local = location.pathname.includes('/research-audit-successor-r3/');
const published = location.pathname.includes('/campaign-audit-successor-r3/');
if (local || published) {
  const historicalPath = local
    ? '../../research-next/postrun-display/joint-stages-partial-offline.html'
    : '../../campaign-joint-stage-reference/postrun-display/joint-stages-partial-offline.html';
  el('load-replay').disabled = false;
  el('load-replay').addEventListener('click', () => {
    el('replay').src = sameOrigin(historicalPath).href;
    el('replay').hidden = false;
    el('close-replay').hidden = false;
    el('load-replay').hidden = true;
    el('replay-status').textContent = 'Historical viewer requested. Its recorded paths and partial P1 hold are display-only, with no new R3 trajectories.';
  });
  el('close-replay').addEventListener('click', () => {
    el('replay').src = 'about:blank';
    el('replay').hidden = true;
    el('close-replay').hidden = true;
    el('load-replay').hidden = false;
    el('replay-status').textContent = 'Historical replay closed.';
  });
} else el('replay-status').textContent = 'Repository layout unrecognized; no historical viewer loaded.';
try {
  const reply = await fetch(sameOrigin('./evidence.narrow.json'), {cache:'no-store'});
  if (!reply.ok) throw new Error(`Selected-record manifest unavailable (${reply.status}).`);
  const manifest = await reply.json();
  if (manifest.schema !== 'audit-c1-r3-results-only-display/v1' || manifest.records.length !== 5) throw new Error('Unexpected results-only manifest.');
  const expected = {
    start:'../robustness-review/results/WINDOW-STARTED.json',
    accounting:'../robustness-review/results/FINAL-ACCOUNTING.json',
    synthetic:'../implementation/results/receipts/synthetic.json',
    saved:'../implementation/results/receipts/saved-json-states.json',
    checkpoint:'../robustness-review/results/last-durable-checkpoint.json'
  };
  if (new Set(manifest.records.map(x => x.id)).size !== 5 || manifest.records.some(x => expected[x.id] !== x.path)) throw new Error('Selected record set exceeds the results-only scope.');
  if (!globalThis.crypto?.subtle) throw new Error('SHA-256 is unavailable in this browser; original selected records remain linked above.');
  const records = {};
  for (const source of manifest.records) {
    const response = await fetch(sameOrigin(source.path), {cache:'no-store'});
    if (!response.ok) throw new Error(`Selected record unavailable (${response.status}).`);
    const bytes = await response.arrayBuffer();
    const hash = Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256', bytes)), x => x.toString(16).padStart(2,'0')).join('');
    if (bytes.byteLength !== source.bytes || hash !== source.sha256) throw new Error(`Selected-record identity mismatch: ${source.id}`);
    records[source.id] = JSON.parse(new TextDecoder().decode(bytes));
  }
  if (records.start.retryAllowed !== false || records.synthetic.status !== 'passed' || records.synthetic.cases.length !== 81 || records.saved.status !== 'integrity_blocked' || records.saved.failure.message !== manifest.failureReason || records.saved.counts.exactSampleComparisons !== 20 || records.saved.counts.savedSignatureAnchors !== 19 || records.checkpoint.completedJobIds.length !== 1 || records.checkpoint.completedJobIds[0] !== 'synthetic') throw new Error('Selected records differ from the reported partial outcome.');
  el('record-check').textContent = 'All five selected original record byte lengths and SHA-256 hashes match this display. That checks record identity only, not full correctness, benchmark performance, physical validity, or complete reproducibility.';
} catch (error) {
  el('record-check').textContent = `Selected records not verified in this browser: ${error.message}`;
}
