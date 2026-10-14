// Postrun-only adaptation of ../demo/app.js. No model or benchmark is invoked.
const get = id => document.getElementById(id);
const localLayout = location.pathname.includes('/research-audit-optimization/');
const priorBase = new URL(localLayout ? '../../research-next/' : '../../campaign-joint-stage-reference/', location.href);
get('replay').src = new URL('implementation/demo/index.html', priorBase).href;
get('prior-report').href = new URL('MILESTONE.md', priorBase).href;
const sameOrigin = path => {
  const url = new URL(path, location.href);
  if (url.origin !== location.origin) throw new Error('Evidence links must stay in this served repository');
  return url;
};
try {
  const response = await fetch('./evidence.json', {cache: 'no-store'});
  if (!response.ok) throw new Error(`Evidence unavailable (${response.status})`);
  const record = await response.json();
  if (record.schema !== 'audit-c1-terminal-postrun-evidence/v1') throw new Error('Unrecognized evidence schema');
  for (const [id, key] of [['status','statusLabel'],['summary','summary'],['reason','reason'],['correctness','correctnessLabel'],['speed','speedLabel'],['verification','displayVerification']]) get(id).textContent = record[key];
  const links = record.records.map(item => {
    const li = document.createElement('li'), a = document.createElement('a');
    a.href = sameOrigin(item.path).href;
    a.textContent = item.label;
    li.append(a, document.createTextNode(` — ${item.description}`));
    return li;
  });
  get('records').replaceChildren(...links);
  if (!globalThis.crypto?.subtle) throw new Error('Browser SHA-256 is unavailable. Read the linked original receipts; no in-browser identity check was made.');
  const receipts = [];
  for (const source of record.sourceIdentities) {
    const response = await fetch(sameOrigin(source.path), {cache: 'no-store'});
    if (!response.ok) throw new Error(`Receipt unavailable (${response.status}): ${source.path}`);
    const bytes = await response.arrayBuffer();
    const digest = await crypto.subtle.digest('SHA-256', bytes);
    const hash = Array.from(new Uint8Array(digest), n => n.toString(16).padStart(2, '0')).join('');
    if (bytes.byteLength !== source.bytes || hash !== source.sha256) throw new Error(`Receipt identity mismatch: ${source.path}`);
    receipts.push(JSON.parse(new TextDecoder().decode(bytes)));
  }
  const [start, terminal, accounting] = receipts;
  if (receipts.length !== 3 || start.schema !== 'audit-c1-window-start/v1' || terminal.schema !== 'audit-c1-supervisor/v1' || accounting.schema !== 'audit-c1-final-accounting/v1' || terminal.status !== 'integrity_blocked' || terminal.completedJobIds.length !== 0 || start.retryAllowed !== false) throw new Error('Unexpected terminal receipt contents');
  get('started').textContent = start.startedAtUtc;
  get('terminal').textContent = terminal.status;
  get('reason').textContent = terminal.reason;
  get('completed').textContent = String(terminal.completedJobIds.length);
  get('retry').textContent = String(start.retryAllowed);
  get('wall').textContent = `${accounting.wallSecondsBeforeWrite} s`;
  get('cpu').textContent = `${accounting.processTreeCpuSecondsBeforeWrite} s`;
  get('receipt-status').textContent = 'All three original receipt byte lengths and SHA-256 identities match the saved postrun evidence. This identity check is not a numerical validation.';
} catch (error) {
  get('receipt-status').textContent = `Receipt display not verified: ${error.message}`;
}
