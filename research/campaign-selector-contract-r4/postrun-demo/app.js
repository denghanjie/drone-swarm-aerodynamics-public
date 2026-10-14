// Sanitized R4 result display only. No original raw checkpoints or inventories are fetched.
const el = id => document.getElementById(id);
const EVIDENCE_SHA256 = '4587e822242ccf202817285906fcc0add458bbc32787e60926992f95acad67d1';
const sameOrigin = path => {
  const url = new URL(path, location.href);
  if (url.origin !== location.origin) throw new Error('The sanitized evidence must stay on the same origin.');
  return url;
};
const localLayout = location.pathname.includes('/research-selector-contract-r4/');
const publicLayout = location.pathname.includes('/campaign-selector-contract-r4/');
const historicalPath = localLayout
  ? '../../research-next/postrun-display/joint-stages-partial-offline.html'
  : '../../campaign-joint-stage-reference/postrun-display/joint-stages-partial-offline.html';
el('load-replay').disabled = !(localLayout || publicLayout);
if (!localLayout && !publicLayout) el('replay-status').textContent = 'Repository layout unrecognized; historical replay not loaded.';
el('load-replay').addEventListener('click', () => {
  el('replay').src = sameOrigin(historicalPath).href;
  el('replay').hidden = false;
  el('close-replay').hidden = false;
  el('load-replay').hidden = true;
  el('replay-status').textContent = 'Historical viewer requested. These saved paths predate R4; no new trajectory is generated.';
});
el('close-replay').addEventListener('click', () => {
  el('replay').src = 'about:blank';
  el('replay').hidden = true;
  el('close-replay').hidden = true;
  el('load-replay').hidden = false;
  el('replay-status').textContent = 'Historical replay closed.';
});
try {
  const response = await fetch(sameOrigin('../postrun-report/EVIDENCE.json'), {cache:'no-store'});
  if (!response.ok) throw new Error(`Sanitized record unavailable (${response.status}).`);
  const bytes = await response.arrayBuffer();
  if (!globalThis.crypto?.subtle) throw new Error('SHA-256 is unavailable here; read the linked sanitized record directly.');
  const sha = Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256', bytes)), n => n.toString(16).padStart(2,'0')).join('');
  if (sha !== EVIDENCE_SHA256) throw new Error('Sanitized record identity differs from this prepared display.');
  const record = JSON.parse(new TextDecoder().decode(bytes));
  if (record.schema !== 'selector-contract-r4-sanitized-postrun-summary/v1' || record.isOriginalReceipt !== false || record.terminal.status !== 'incomplete_or_blocked' || record.coverage.completedCases !== 8 || record.coverage.interruptedCases !== 1 || record.coverage.unreachedCases !== 91 || record.lastDurableContext.ninthCaseReceiptPresent !== false) throw new Error('Unexpected R4 partial outcome.');
  el('evidence-status').textContent = 'The sanitized derivative matches this prepared display SHA-256. This verifies presentation identity only. Raw checkpoints and private inventories were not fetched, and no contract test or scientific gate was rerun.';
} catch (error) {
  el('evidence-status').textContent = `Sanitized display record not verified in this browser: ${error.message}`;
}
