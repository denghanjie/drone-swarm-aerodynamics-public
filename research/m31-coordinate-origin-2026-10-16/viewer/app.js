import {N, STATUS, POLICY, FIELDS, STATUS_COLORS, PendingEvidence, loadEvidence, loadOrigin, record, modes, metric, savedSum, certificate} from './evidence.js';
const $ = id => document.getElementById(id);
const controls = ['origin', 'arm', 'receiver', 'rotor', 'source', 'color', 'whole', 'focus', 'largest', 'links', 'recenter', 'vector'];
const number = value => value == null || !Number.isFinite(value) ? 'Unavailable' : Object.is(value, -0) ? '−0' : value === 0 ? '0' : Math.abs(value) < .001 ? value.toExponential(7) : value.toPrecision(10);
const approx = value => number(certificate(value));
const statusName = item => item ? `${STATUS[item.status] ?? `Unknown status ${item.status}`}${item.identityValid ? '' : ' · identity mismatch'}` : 'Not retained';
const tint = hex => [1, 3, 5].map(index => parseInt(hex.slice(index, index + 2), 16) / 255);
const cold = tint('#4394cc'), hot = tint('#f49b41'), missing = tint('#667788');
let data, frame, scene, options = [], mode, origin = 0, arm = 'A', selection = 0, rotor = 0, source = 0, loading = false;
const cell = () => data.reports.cells.find(item => item.origin === origin && item.arm === arm);
const setControls = disabled => controls.forEach(id => {$(id).disabled = disabled;});
function row(values, choose, label) {
  const tr = document.createElement('tr');
  for (const value of values) {const td = document.createElement('td');td.textContent = String(value);tr.append(td);}
  if (choose) {
    tr.tabIndex = 0;tr.setAttribute('aria-label', label);tr.addEventListener('click', () => {if (!loading) choose();});
    tr.addEventListener('keydown', event => {if (!loading && (event.key === 'Enter' || event.key === ' ')) {event.preventDefault();choose();}});
  }
  return tr;
}
function sumRow(values, index) {
  const tr = row(values, () => {selection = Math.floor(index / 4);rotor = index % 4;$('receiver').value = String(selection);$('rotor').value = String(rotor);update();scene?.fit('focused');}, `Inspect receiver ${data.meta.receiverIds[Math.floor(index / 4)]}, rotor ${index % 4}`);
  tr.dataset.index = String(index);return tr;
}
function listItem(label, value) {const dt = document.createElement('dt'), dd = document.createElement('dd');dt.textContent = label;dd.textContent = value;return [dt, dd];}
function chooseLargest() {
  let best = -Infinity, chosen = null;
  for (let id = 0; id < N; id++) {const entry = metric(frame, mode, selection, id, rotor), value = mode.kind === 'status' ? entry.record?.term : entry.value;if (value != null && value > best) {best = value;chosen = id;}}
  if (chosen !== null) {source = chosen;$('source').value = String(source);}
  else $('pair-note').textContent = 'No valid retained value exists in this color slice. The inspected source is unchanged.';
}
function updateInspector() {
  const stages = ['R', 'Q0', 'Q1', `T:${arm}`], records = stages.map(stage => record(frame, stage, selection, source, rotor));
  const chosen = record(frame, mode.stage, selection, source, rotor);
  $('pair-title').textContent = `Source ${source} → receiver ${frame.receiverIds[selection]}`;
  $('pair-note').textContent = `Origin ${origin} · arm ${arm} · rotor ${rotor} · source-major slot ${(selection * N + source) * 4 + rotor}. The white dashed link identifies this pair, including zero and unavailable records.`;
  $('pair-summary').replaceChildren(...[
    ...listItem('Color metric', mode.label),
    ...listItem('Shown value', mode.kind === 'status' ? statusName(chosen) : `${number(metric(frame, mode, selection, source, rotor).value)} m/s`),
    ...listItem('Policy', chosen ? POLICY[chosen.code] ?? (chosen.code === 0xffffffff ? 'Not classified' : `Unknown ${chosen.code}`) : 'Unavailable'),
    ...listItem('Validity mask', chosen ? `0x${chosen.mask.toString(16).padStart(5, '0')}` : 'Unavailable'),
    ...listItem('Routing flags', chosen ? `0x${chosen.flags.toString(16)}` : 'Unavailable'),
    ...listItem('Identity', chosen ? chosen.identityValid ? 'Matches saved slot' : 'Invalid / unwritten identity' : 'Unavailable')
  ]);
  $('pair-table').replaceChildren(...records.map((entry, index) => row([stages[index], number(entry?.term), statusName(entry)])));
  $('stage-fields').replaceChildren(...FIELDS.map((label, k) => {
    const tr = row([label, ...records.map(entry => number(entry?.scalars[k]))]);
    records.forEach((entry, i) => {tr.children[i + 1].title = entry ? `${entry.reached[k] ? 'Reached' : 'Unreached'} · raw bits ${entry.scalarBits[k] ?? 'unavailable'} · ${statusName(entry)}` : 'No saved record';});return tr;
  }));
  updateVectors();
}
function updateVectors() {
  const stages = ['R', 'Q0', 'Q1', 'T:A', 'T:B', 'T:C'], records = stages.map(stage => record(frame, stage, selection, source, rotor)), start = $('vector').value === 'center' ? 12 : 15;
  const difference = (a, b) => a != null && b != null ? number(a - b) : 'Unavailable';
  const rows = [row(['Record status', ...records.map(statusName), 'Display difference', 'Display difference'])];
  for (let axis = 0; axis < 3; axis++) {
    const values = records.map(entry => entry?.scalars[start + axis] ?? null), tr = row([['x', 'y', 'z'][axis], ...values.map(number), difference(values[4], values[3]), difference(values[5], values[4])]);
    records.forEach((entry, i) => {tr.children[i + 1].title = entry ? `${entry.reached[start + axis] ? 'Reached' : 'Unreached'} · raw bits ${entry.scalarBits[start + axis] ?? 'unavailable'} · ${statusName(entry)}` : 'No saved record';});rows.push(tr);
  }
  $('vector-table').replaceChildren(...rows);
  $('vector-note').textContent = 'Each component requires its reached bit and matching record identity. Reached values can survive an invalid later stage; the record status stays visible. B − A and C − B are display-only subtraction of these saved components. Hover a value for its original bits; unavailable components are never reconstructed.';
}
function updateLegend(maximum, positives, unavailable) {
  $('legend').replaceChildren(document.createTextNode('Cyan: receiver / saved rotor offset · White: inspected source. '));
  if (mode.kind === 'status') STATUS.forEach((name, index) => {const entry = document.createElement('span'), swatch = document.createElement('i');swatch.className = 'swatch';swatch.style.background = STATUS_COLORS[index];entry.append(swatch, document.createTextNode(name));$('legend').append(entry);});
  else {const gradient = document.createElement('i');gradient.className = 'gradient';$('legend').append(gradient, document.createTextNode(`0 → ${number(maximum)} m/s, current slice maximum. Gray: unavailable. `));}
  const counts = document.createElement('div');counts.textContent = `${positives} valid positive ${mode.stage} terms · ${unavailable} unavailable color values. Focus and links use those positive saved terms.`;$('legend').append(counts);
}
function update() {
  if (!frame || !mode) return;
  const rows = Array.from({length: N}, (_, id) => metric(frame, mode, selection, id, rotor));
  let maximum = 0;for (const entry of rows) if (entry.value != null && entry.value > maximum) maximum = entry.value;
  const colors = new Float32Array(N * 3), positiveIDs = [];
  rows.forEach((entry, id) => {
    const fraction = maximum > 0 ? Math.max(0, Math.min(1, entry.value / maximum)) : 0;
    colors.set(entry.value == null ? missing : mode.kind === 'status' ? tint(STATUS_COLORS[entry.value] ?? '#ff667a') : cold.map((channel, i) => channel + fraction * (hot[i] - channel)), id * 3);
    if (entry.record?.termValid && entry.record.term > 0) positiveIDs.push(id);
  });
  const offsetIndex = (selection * 4 + rotor) * 4, rawOffset = frame.preparedOffsets?.slice(offsetIndex, offsetIndex + 3), offset = rawOffset && Array.from(rawOffset).every(Number.isFinite) ? Array.from(rawOffset) : null;
  scene?.show({colors, receiver: frame.receiverIds[selection], source, offset, positiveIDs, showLinks: $('links').checked});
  updateInspector();updateLegend(maximum, positiveIDs.length, rows.filter(entry => entry.value == null).length);
  for (const id of ['sum-table', 'gate-table']) for (const tr of $(id).children) tr.classList.toggle('selected', Number(tr.dataset.index) === selection * 4 + rotor);
  document.body.dataset.origin = String(origin);document.body.dataset.arm = arm;document.body.dataset.receiver = String(frame.receiverIds[selection]);document.body.dataset.rotor = String(rotor);document.body.dataset.source = String(source);document.body.dataset.color = mode.id;
}
function renderCells() {
  $('cell-table').replaceChildren(...data.reports.cells.map(item => {
    const tr = row([`Origin ${item.origin} / ${item.arm}`, item.matchedReference, item.status, item.availability.terms.label, item.availability.serial.label, item.qualificationLabel], () => {origin = item.origin;arm = item.arm;$('origin').value = String(origin);$('arm').value = arm;activate().catch(fail);}, `Inspect origin ${item.origin}, arm ${item.arm}`);
    tr.classList.toggle('selected', item.origin === origin && item.arm === arm);tr.children[2].className = item.statusKind === 'failed' ? 'fail' : item.statusKind === 'qualified' ? 'pass' : 'missing';return tr;
  }));
  const chosen = cell();$('coverage').textContent = `Origin ${origin} / ${arm} · ${chosen.status}`;$('cell-note').textContent = chosen.note;$('cell-note').dataset.kind = chosen.statusKind;$('matched-reference').textContent = `${chosen.matchedReference} for arm ${arm}`;
}
function renderSums() {
  const chosen = cell(), sums = [], gates = [];
  for (let index = 0; index < 16; index++) {
    const label = `${data.meta.receiverIds[Math.floor(index / 4)]} / ${index % 4}`, entry = chosen.rows?.find(item => item.index === index), serial = savedSum(frame, `T:${arm}`, index, chosen.availability.serial.label);
    const ordinary = ['R', 'Q0', 'Q1'].map(stage => {const value = savedSum(frame, stage, index);return value.valid ? number(value.value) : value.rawValue != null ? `${value.label} · raw ${number(value.rawValue)}` : value.label;});
    sums.push(sumRow([label, ...ordinary, entry?.exactTermSum ? `${approx(entry.exactTermSum)}${entry.termSumLabel ? ` · ${entry.termSumLabel}` : ''}` : 'Unavailable', number(serial.value), serial.label], index));
    const tr = sumRow([label, approx(entry?.l1QR), approx(entry?.l1TQ), approx(entry?.l1TR), approx(entry?.termPlusAllowance), approx(entry?.reductionError), approx(entry?.allowance), approx(entry?.combined), approx(entry?.epsilon), entry?.gateLabel ?? 'Not assessed'], index);
    tr.lastChild.className = entry?.gatePass === false ? 'fail' : entry?.gatePass === true ? 'pass' : 'missing';gates.push(tr);
  }
  $('sum-table').replaceChildren(...sums);$('gate-table').replaceChildren(...gates);
}
function renderContrasts() {
  const rows = [];
  for (const contrast of data.reports.vectorContrasts ?? []) {
    if (!contrast.available) {rows.push(row([`Origin ${contrast.origin} / ${contrast.comparison}`, contrast.label, 'Unavailable', 'Unavailable', 'Unavailable', 'Unavailable']));continue;}
    for (const field of contrast.fields) rows.push(row([`Origin ${contrast.origin} / ${contrast.comparison}`, FIELDS[field.scalarIndex] ?? String(field.scalarIndex), field.compared, field.rawWordDifferences, number(field.maxAbsoluteDifference), field.maxWitness]));
  }
  $('vector-contrast-table').replaceChildren(...rows);
}
function renderEvidence() {
  $('evidence-list').replaceChildren(...Object.entries(data.meta.files).map(([key, spec]) => {const entry = document.createElement('div'), link = document.createElement('a'), hash = document.createElement('code');entry.className = 'evidence-row';link.href = spec.url;link.textContent = spec.label || key;hash.textContent = `${spec.bytes.toLocaleString('en-US')} bytes · SHA-256 ${spec.sha256}`;entry.append(link, hash);return entry;}));
}
function refreshModes() {
  const previous = mode?.id.replace(/T:[ABC]/g, `T:${arm}`);options = modes(arm);
  $('color').replaceChildren(...options.map(item => {const option = document.createElement('option');option.value = item.id;option.textContent = item.label;return option;}));
  mode = options.find(item => item.id === previous) ?? options[0];$('color').value = mode.id;
}
async function activate() {
  loading = true;setControls(true);document.body.dataset.ready = 'false';
  $('cell-note').textContent = `Checking retained bytes for origin ${origin}, arm ${arm}…`;
  frame = await loadOrigin(data, origin);refreshModes();renderCells();renderSums();
  $('display-frame').textContent = $('recenter').checked ? `Drawing coordinates subtract [${frame.origin.join(', ')}]. All displayed numbers and scientific records retain their original coordinates.` : 'Absolute saved coordinates. Recenter changes only drawing coordinates and camera framing.';
  if (frame.poses) {
    if (scene) scene.setFrame(frame, $('recenter').checked);
    else {const {createScene} = await import('./scene.js');scene = createScene($('scene'), frame, id => {source = id;$('source').value = String(id);update();});scene.setFrame(frame, $('recenter').checked);}
  } else {scene?.dispose();scene = null;const text = document.createElement('p');text.className = 'scene-placeholder';text.textContent = 'No original saved poses retained for this origin. The scene is unavailable.';$('scene').replaceChildren(text);}
  update();scene?.fit('focused');loading = false;setControls(false);
  for (const id of ['whole', 'focus', 'links', 'recenter']) $(id).disabled = !scene;
  document.body.dataset.ready = 'true';
}
function fail(error) {
  loading = false;setControls(true);scene?.dispose();scene = null;document.body.dataset.ready = 'false';
  const pending = error instanceof PendingEvidence;document.body.dataset.integrity = pending ? 'pending' : 'failed';
  $('integrity').textContent = pending ? 'Awaiting review binding' : 'Evidence not unlocked';$('status').textContent = error.message;
  if (!pending) {const text = document.createElement('p');text.className = 'scene-placeholder';text.textContent = 'Scene locked because required evidence could not be verified.';$('scene').replaceChildren(text);}
}
$('origin').addEventListener('change', () => {origin = Number($('origin').value);activate().catch(fail);});
$('arm').addEventListener('change', () => {arm = $('arm').value;activate().catch(fail);});
$('receiver').addEventListener('change', () => {selection = Number($('receiver').value);update();scene?.fit('focused');});
$('rotor').addEventListener('change', () => {rotor = Number($('rotor').value);update();scene?.fit('focused');});
$('source').addEventListener('change', () => {source = Math.max(0, Math.min(N - 1, Math.round(Number($('source').value) || 0)));$('source').value = String(source);update();});
$('color').addEventListener('change', () => {mode = options.find(item => item.id === $('color').value);update();});
$('vector').addEventListener('change', updateVectors);$('links').addEventListener('change', update);
$('recenter').addEventListener('change', () => {scene?.setFrame(frame, $('recenter').checked);scene?.fit();$('display-frame').textContent = $('recenter').checked ? `Drawing coordinates subtract [${frame.origin.join(', ')}]. All displayed numbers and scientific records retain their original coordinates.` : 'Absolute saved coordinates. Recenter changes only drawing coordinates and camera framing.';});
$('whole').addEventListener('click', () => scene?.fit('whole'));$('focus').addEventListener('click', () => scene?.fit('focused'));
$('largest').addEventListener('click', () => {chooseLargest();update();scene?.fit('focused');});
window.addEventListener('pagehide', () => scene?.dispose(), {once: true});
(async () => {
  data = await loadEvidence();const campaign = data.reports.campaign;
  $('integrity').textContent = data.verification.reviewPassed ? 'Independent saved review passed' : 'Review FAILED · records unqualified';$('outcome').textContent = campaign.outcomeLabel;$('status').textContent = data.verification.reviewNotice + ' ' + campaign.summary;
  $('provenance-note').textContent = `Source ${campaign.sourceCommit}. Byte identities are bound. The independent review is terminal and failed; its two control-stage bookkeeping findings remain preserved. Numerical outcomes below are recorded driver results, not fully qualified conclusions.`;
  document.body.dataset.integrity = data.verification.reviewPassed ? 'verified' : 'recorded-unqualified';document.body.dataset.outcome = campaign.qualified === true ? 'passed' : campaign.qualified === false ? 'failed' : 'incomplete';
  $('receiver').replaceChildren(...data.meta.receiverIds.map((id, index) => {const option = document.createElement('option');option.value = String(index);option.textContent = String(id);return option;}));
  const initial = data.meta.initialSelection;
  if (initial) {
    if (![0, 1].includes(initial.origin) || !['A', 'B', 'C'].includes(initial.arm) || !Number.isInteger(initial.selection) || initial.selection < 0 || initial.selection > 3 || !Number.isInteger(initial.rotor) || initial.rotor < 0 || initial.rotor > 3 || !Number.isInteger(initial.source) || initial.source < 0 || initial.source >= N) throw Error('Invalid initial display selection');
    origin = initial.origin;arm = initial.arm;selection = initial.selection;rotor = initial.rotor;source = initial.source;
    mode = modes(arm).find(item => item.id === initial.color);
  }
  $('origin').value = String(origin);$('arm').value = arm;$('receiver').value = String(selection);$('rotor').value = String(rotor);$('source').value = String(source);
  renderEvidence();renderContrasts();await activate();
})().catch(fail);
