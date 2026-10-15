import {IDS, N, STATUS, POLICY, FIELDS, STATUS_COLORS, loadEvidence, record, modes, metric, savedSum, certificate} from './evidence.js';
const $ = id => document.getElementById(id);
const controlIDs = ['receiver', 'rotor', 'source', 'color', 'whole', 'focus', 'largest', 'links'];
let data, options, scene, selection = 3, rotor = 3, source = 0, mode;
const number = value => value === null || value === undefined || !Number.isFinite(value) ? 'Unavailable' : value === 0 ? '0' : Math.abs(value) < .001 ? value.toExponential(6) : value.toPrecision(9);
const approx = value => number(certificate(value));
const statusName = item => item ? STATUS[item.status] ?? `Unknown status ${item.status}` : 'Not recorded';
function row(values, index) {
  const tr = document.createElement('tr');
  for (const value of values) {const td = document.createElement('td');td.textContent = String(value);tr.append(td);}
  if (index !== undefined) {tr.dataset.index = String(index);tr.tabIndex = 0;tr.setAttribute('aria-label', `Inspect receiver ${IDS[Math.floor(index / 4)]}, rotor ${index % 4}`);const choose = () => {selection = Math.floor(index / 4);rotor = index % 4;$('receiver').value = String(selection);$('rotor').value = String(rotor);chooseLargest();update();scene.fit('focused');};tr.addEventListener('click', choose);tr.addEventListener('keydown', event => {if (event.key === 'Enter' || event.key === ' ') {event.preventDefault();choose();}});}
  return tr;
}
function listItem(label, value) {const dt = document.createElement('dt'),dd = document.createElement('dd');dt.textContent = label;dd.textContent = value;return [dt, dd];}
function rgba(hex) {return [1,3,5].map(index => parseInt(hex.slice(index, index + 2), 16) / 255);}
const cold = rgba('#4394cc'), hot = rgba('#f49b41'), missing = rgba('#667788');
function heat(value, maximum) {const t = maximum > 0 ? Math.max(0, Math.min(1, value / maximum)) : 0;return cold.map((channel, index) => channel + t * (hot[index] - channel));}
function metricRows() {return Array.from({length: N}, (_, id) => metric(data, mode, selection, id, rotor));}
function chooseLargest() {
  let best = -1, chosen = 0;
  for (let id = 0; id < N; id++) {const entry = metric(data, mode, selection, id, rotor),value = mode.kind === 'status' ? entry.record?.term : entry.value;if (value !== null && value !== undefined && value > best) {best = value;chosen = id;}}
  source = chosen;$('source').value = String(source);
}
function updateInspector() {
  const records = ['R', 'Q', 'T'].map(stage => record(data, stage, selection, source, rotor));
  $('pair-title').textContent = `Source ${source} → receiver ${IDS[selection]}`;
  $('pair-note').textContent = `Rotor ${rotor} · source-major slot ${(selection * N + source) * 4 + rotor}. White dashed link marks this selection, including valid zeros or unavailable records.`;
  const chosen = records[['R', 'Q', 'T'].indexOf(mode.stage)];
  $('pair-summary').replaceChildren(...[
    ...listItem('Color metric', mode.label),
    ...listItem('Shown value', mode.kind === 'status' ? statusName(chosen) : `${number(metric(data, mode, selection, source, rotor).value)} m/s`),
    ...listItem('Policy', chosen ? POLICY[chosen.code] ?? (chosen.code === 0xffffffff ? 'Not classified' : `Unknown ${chosen.code}`) : 'Unavailable'),
    ...listItem('Validity mask', chosen ? `0x${chosen.mask.toString(16).padStart(3, '0')}` : 'Unavailable'),
    ...listItem('Routing flags', chosen ? `0x${chosen.flags.toString(16)}` : 'Unavailable'),
    ...listItem('Identity', chosen ? chosen.identityValid ? 'Matches slot' : 'Invalid / unwritten identity' : 'Unavailable')
  ]);
  $('pair-table').replaceChildren(...records.map((item, index) => row([['R', 'Q', 'T'][index], item?.termValid ? number(item.term) : 'Unavailable', statusName(item)])));
  $('stage-fields').replaceChildren(...FIELDS.map((label, index) => row([label, ...records.map(item => number(item?.scalars[index]))])));
}
function updateLegend(maximum, positiveCount, missingCount) {
  $('legend').replaceChildren();
  const marker = document.createElement('span');marker.textContent = 'Cyan: receiver / rotor · White: inspected source. ';$('legend').append(marker);
  if (mode.kind === 'status') {
    STATUS.forEach((name, index) => {const entry = document.createElement('span'),swatch = document.createElement('i');swatch.className = 'swatch';swatch.style.background = STATUS_COLORS[index];entry.append(swatch,document.createTextNode(name));$('legend').append(entry);});
  } else {
    const gradient = document.createElement('i');gradient.className = 'gradient';$('legend').append(gradient,document.createTextNode(`0 → ${number(maximum)} m/s, current slice maximum. Gray: unavailable. `));
  }
  const counts = document.createElement('div');counts.textContent = `${positiveCount} valid positive ${mode.stage} source terms for this rotor · ${missingCount} unavailable color values. Links show those stored positive terms.`;$('legend').append(counts);
}
function update() {
  if (!data || !scene) return;
  const rows = metricRows(), numeric = rows.filter(entry => entry.value !== null).map(entry => entry.value),maximum = mode.kind === 'status' ? 1 : numeric.length ? Math.max(...numeric) : 0;
  const colors = new Float32Array(N * 3), positiveIDs = [];
  rows.forEach((entry, id) => {
    const tint = entry.value === null ? missing : mode.kind === 'status' ? rgba(STATUS_COLORS[entry.value] ?? '#ff667a') : heat(entry.value, maximum);
    colors.set(tint, id * 3);if (entry.record?.termValid && entry.record.term > 0) positiveIDs.push(id);
  });
  const offsetIndex = (selection * 4 + rotor) * 4;
  const offset = data.preparedOffsets ? Array.from(data.preparedOffsets.slice(offsetIndex, offsetIndex + 3)) : null;
  scene.show({colors, receiver: IDS[selection], source, offset, positiveIDs, showLinks: $('links').checked});
  updateInspector();updateLegend(maximum, positiveIDs.length, rows.filter(entry => entry.value === null).length);
  for (const id of ['sum-table', 'gate-table']) for (const tr of $(id).children) tr.classList.toggle('selected', Number(tr.dataset.index) === selection * 4 + rotor);
  document.body.dataset.receiver = String(IDS[selection]);document.body.dataset.rotor = String(rotor);document.body.dataset.source = String(source);document.body.dataset.color = mode.id;
}
function renderDisposition() {
  const {result, review, budget, reports} = data;
  const numerical = review.fullSuiteQualified === true && result.pass === true;
  $('integrity').textContent = 'Independent saved review verified';
  $('outcome').textContent = numerical ? 'Complete diagnostic passed' : result.status === 'unsupported' ? 'Unsupported environment' : reports.terms?.pass === false ? 'Term-error gate failed' : 'Incomplete / failed attempt';
  $('coverage').textContent = data.gpu ? '80,000 GPU slots retained' : 'No GPU term buffer retained';
  document.body.dataset.integrity = 'verified';document.body.dataset.outcome = numerical ? 'passed' : 'failed';
  const failed = reports.terms?.rotors?.filter(item => item.pass === false) ?? [];
  const failureDescription = failed.length ? failed.map(item => `receiver ${item.receiverID}, rotor ${item.rotor}`).join('; ') : 'an earlier stage';
  $('status').textContent = numerical ? 'Saved integrity and all declared scientific gates passed for this fixed slice. This is a numerical component result.' : `Verified saved evidence records a terminal ${result.status ?? 'incomplete'} attempt. ${reports.terms?.pass === false ? `The conservative term gate failed at ${failureDescription}. ` : ''}${data.serial ? 'Retained serial records are shown with their own status.' : 'Serial reduction was not dispatched; no serial sum or final combined gate is available.'}`;
  $('terminal-note').textContent = `Scientific source ${result.sourceCommit}. Supervisor terminal: ${budget.terminal === true ? 'yes' : 'no'}; timeout: ${budget.timeout === true ? 'yes' : 'no'}; owned-process cleanup: ${budget.processGroupCleanup?.confirmedAbsent === true ? 'confirmed' : 'not confirmed'}. No wall-time value is presented as performance evidence.`;
  const stages = [
    ['R', 'Original reference', !!data.references.R?.metadata, data.references.R?.counts?.complete, 'Saved original inputs and binary64 terms'],
    ['Q', 'Packed-input reference', !!data.references.Q?.metadata, data.references.Q?.counts?.complete, 'Decoded packed inputs, binary64 evaluation'],
    ['controls', 'Shared GPU controls', !!data.meta.files.gpuControls, !!reports.controls, '16 frozen policy/profile controls'],
    ['terms', 'Materialized GPU terms', !!data.gpu, reports.terms?.completeTermCoverage, '80,000 source-major slots; no reduction inferred'],
    ['serial', 'Serial GPU reduction', !!data.serial, !!data.serial && reports.serial?.pass === true, 'Must use the original retained GPU term buffer']
  ];
  $('stage-table').replaceChildren(...stages.map(([key, title, present, complete, note]) => {
    const report = reports[key], exposure = review.exposure?.[key], available = present ? complete ? 'Complete retained output' : 'Retained output; partial / unqualified' : 'Not present / not reached';
    const assessment = report ? report.pass === true ? 'Passed' : `Failed · ${report.errorCount ?? '?'} finding(s)` : 'Not assessed';
    const tr = row([title, available, assessment, note]);tr.children[2].className = report ? report.pass ? 'pass' : 'fail' : 'missing';
    if (exposure && exposure.present !== present) throw Error(`Review/viewer stage availability mismatch: ${key}`);
    return tr;
  }));
}
function renderSums() {
  const sumRows = [], gateRows = [], reports = data.reports;
  const threshold = reports.serial?.threshold ?? reports.terms?.threshold ?? reports.Q?.threshold;
  for (let index = 0; index < 16; index++) {
    const label = `${IDS[Math.floor(index / 4)]} / ${index % 4}`, r = savedSum(data, 'R', index), q = savedSum(data, 'Q', index), s = savedSum(data, 'T', index);
    const t = reports.terms?.rotors?.find(item => item.index === index), serial = reports.serial?.rotors?.find(item => item.index === index), packing = reports.Q?.rotors?.find(item => item.index === index);
    const sumText = entry => entry.value === null ? entry.label : `${number(entry.value)}${entry.valid === false ? ' · partial' : ''}`;
    sumRows.push(row([label,sumText(r),sumText(q),t?.qualifiedTermCount === 5000 ? approx(t.exactStoredTermSum) : t ? 'Partial / unqualified' : 'Unavailable',number(s.value),s.label],index));
    const disposition = serial ? serial.pass ? 'Final passed' : 'Final FAILED' : t ? `${t.pass ? 'Term passed' : 'Term FAILED'} · final unavailable` : packing ? `${packing.pass ? 'Packing passed' : 'Packing FAILED'} · later unavailable` : 'Not assessed';
    const tr = row([label,approx(t?.l1QR ?? packing?.l1QR),approx(t?.l1TQ),approx(t?.l1TR),approx(t?.l1PlusAllowance),approx(serial?.absoluteReductionError),approx(threshold?.referenceSumAllowance),approx(serial?.combinedConservativeError),approx(threshold?.epsilon),disposition],index);
    tr.lastChild.className = disposition.includes('FAILED') ? 'fail' : serial?.pass ? 'pass' : 'partial';gateRows.push(tr);
  }
  $('sum-table').replaceChildren(...sumRows);$('gate-table').replaceChildren(...gateRows);
}
function renderEvidence() {
  $('evidence-list').replaceChildren(...Object.entries(data.meta.files).map(([key, spec]) => {
    const entry = document.createElement('div'),link = document.createElement('a'),hash = document.createElement('code');entry.className = 'evidence-row';link.href = spec.url;link.textContent = spec.label || key;hash.textContent = `${spec.bytes.toLocaleString('en-US')} bytes · SHA-256 ${spec.sha256}`;entry.append(link,hash);return entry;
  }));
}
function fail(error) {
  console.error(error);document.body.dataset.ready = 'false';document.body.dataset.integrity = 'failed';
  $('integrity').textContent = 'Evidence not unlocked';$('status').textContent = error.message;controlIDs.forEach(id => {$(id).disabled = true;});
}
$('receiver').addEventListener('change', () => {selection = Number($('receiver').value);chooseLargest();update();scene.fit('focused');});
$('rotor').addEventListener('change', () => {rotor = Number($('rotor').value);chooseLargest();update();scene.fit('focused');});
$('source').addEventListener('change', () => {source = Math.max(0, Math.min(N - 1, Math.round(Number($('source').value) || 0)));$('source').value = String(source);update();});
$('color').addEventListener('change', () => {mode = options.find(item => item.id === $('color').value);update();});
$('links').addEventListener('change', update);$('whole').addEventListener('click', () => scene.fit('whole'));$('focus').addEventListener('click', () => scene.fit('focused'));
$('largest').addEventListener('click', () => {chooseLargest();update();scene.fit('focused');});
(async () => {
  data = await loadEvidence();options = modes(data);if (!options.length) throw Error('Reviewed attempt retained no source-term records to inspect');
  renderDisposition();renderSums();renderEvidence();
  for (const item of options) {const option = document.createElement('option');option.value = item.id;option.textContent = item.label;$('color').append(option);}
  mode = options.find(item => item.id === 'error-TR') ?? options[0];$('color').value = mode.id;$('receiver').value = '3';$('rotor').value = '3';chooseLargest();
  const {createScene} = await import('./scene.js');scene = createScene($('scene'), data.poses, id => {source = id;$('source').value = String(source);update();});
  update();scene.fit('focused');controlIDs.forEach(id => {$(id).disabled = false;});document.body.dataset.ready = 'true';
})().catch(fail);
