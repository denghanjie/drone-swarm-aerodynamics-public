const get = id => document.getElementById(id);
const localLayout = location.pathname.includes('/research-audit-optimization/');
const priorBase = new URL(localLayout ? '../../research-next/' : '../../campaign-joint-stage-reference/', location.href);
get('replay').src = new URL('implementation/demo/index.html', priorBase).href;
get('prior-report').href = new URL('MILESTONE.md', priorBase).href;
try {
  const response = await fetch('./evidence.json', {cache: 'no-store'});
  if (!response.ok) throw new Error(`Evidence link record unavailable (${response.status})`);
  const record = await response.json();
  if (record.schema !== 'audit-overhead-display-evidence/v1') throw new Error('Unrecognized evidence record');
  get('status').textContent = record.statusLabel;
  get('summary').textContent = record.summary;
  get('correctness').textContent = record.correctnessLabel;
  get('verification').textContent = record.displayVerification;
  for (const item of record.records) {
    const link = new URL(item.path, location.href);
    if (link.origin !== location.origin) throw new Error('Evidence links must remain in this served repository');
    const li = document.createElement('li'), a = document.createElement('a');
    a.href = link.href;
    a.textContent = item.label;
    li.append(a, document.createTextNode(` — ${item.description}`));
    get('records').append(li);
  }
} catch (error) {
  get('status').textContent = 'Diagnostic evidence unavailable';
  get('summary').textContent = error.message;
}
