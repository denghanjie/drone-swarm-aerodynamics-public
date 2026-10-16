import { loadEvidence } from './data.js';

const $ = id => document.getElementById(id);
const MODES = {
  bothFades: { label: 'Both fades · implemented profile', speed: 'bothFadesMps', j: 'JBothFadesN', color: '#126f79' },
  radialOnly: { label: 'Radial fade only', speed: 'radialOnlyMps', j: 'JRadialOnlyN', color: '#7767aa' },
  untruncated: { label: 'Untruncated profile', speed: 'untruncatedMps', j: 'JUntruncatedN', color: '#b36c21' },
};
const CASE_LABELS = { off: 'All source motors off', 'quarter-hover': 'Quarter-hover total', hover: 'Hover total', 'twice-hover': 'Twice-hover total', 'unequal-same-total': 'Unequal rotors · hover total' };
const fmt = n => n === 0 ? '0' : Number(n.toPrecision(8)).toString();
const say = (id, text) => { $(id).textContent = text; };
function option(value, label) { const el = document.createElement('option'); el.value = value; el.textContent = label; return el; }
function row(values, className = '') {
  const tr = document.createElement('tr'); tr.className = className;
  values.forEach(value => { const td = document.createElement('td'); td.textContent = typeof value === 'number' ? fmt(value) : value; if (typeof value === 'number') td.title = String(value); tr.append(td); });
  return tr;
}
function svgEl(name, attributes = {}, text) {
  const el = document.createElementNS('http://www.w3.org/2000/svg', name);
  Object.entries(attributes).forEach(([key, value]) => el.setAttribute(key, value));
  if (text !== undefined) el.textContent = text;
  return el;
}
function drawPlot(plane) {
  const svg = $('profile-plot');
  svg.replaceChildren(svgEl('title', { id: 'plot-title' }, `Saved radial profiles at s = ${plane.downstreamM} m`), svgEl('desc', { id: 'plot-desc' }, 'Three lines connect only the 41 saved radius and speed values. Exact saved values are available in the selected-plane table below. No profile formula is evaluated.'));
  const box = { left: 43, top: 14, width: 298, height: 154 };
  const maxR = plane.profile[plane.profile.length - 1].radiusM;
  const maxU = Math.max(...plane.profile.map(p => p.untruncatedMps), Number.EPSILON);
  const x = value => box.left + value / maxR * box.width;
  const y = value => box.top + box.height - value / maxU * box.height;
  for (let k = 0; k <= 2; k++) {
    const u = maxU * k / 2, r = maxR * k / 2;
    svg.append(svgEl('line', { x1: box.left, y1: y(u), x2: box.left + box.width, y2: y(u), class: 'grid' }));
    svg.append(svgEl('text', { x: box.left - 7, y: y(u) + 3, 'text-anchor': 'end' }, Number(u.toPrecision(3)).toString()));
    svg.append(svgEl('text', { x: x(r), y: box.top + box.height + 16, 'text-anchor': 'middle' }, Number(r.toPrecision(3)).toString()));
  }
  svg.append(svgEl('text', { x: box.left, y: 9 }, 'm/s'), svgEl('text', { x: box.left + box.width, y: 204, 'text-anchor': 'end' }, 'radius r / m'));
  for (const key of ['untruncated', 'radialOnly', 'bothFades']) {
    const mode = MODES[key];
    const d = plane.profile.map((point, i) => `${i ? 'L' : 'M'}${x(point.radiusM)},${y(point[mode.speed])}`).join(' ');
    svg.append(svgEl('path', { d, class: 'plot-line', stroke: mode.color, 'stroke-dasharray': key === 'radialOnly' ? '6 4' : key === 'untruncated' ? '2 4' : 'none' }));
  }
}

async function main() {
  const { result, witness, receipts } = await loadEvidence();
  document.body.dataset.binding = 'verified';
  $('verified-content').hidden = false;
  say('status', 'Both saved evidence files passed byte-count and SHA-256 verification. This viewer displays recorded values only.');
  say('summary-ratio', fmt(result.untruncatedJOverWeight));
  say('summary-witness', witness.sourceIndependentInTheseCases ? 'No direct response' : 'Recorded response differs');
  say('summary-witness-calls', `${witness.calls} saved calls across ${witness.cases.length} source motor states.`);
  say('summary-retention', `${(100 * result.radialSquaredProfileRetention).toFixed(4)}%`);
  say('summary-gate', result.numericalGatePass ? 'Recorded pass' : 'Recorded failure');
  say('summary-convergence', `512→1024 radial integral difference: ${fmt(result.convergence512To1024.radialFadedAbsoluteDifference)}.`);
  say('record-count', `${result.planes.length} planes · ${result.planes[0].profile.length} saved radial points each`);
  const colorMax = Math.max(...result.planes.flatMap(p => p.profile.map(point => point.untruncatedMps)));
  say('color-scale', `Saved scalar speed: 0 to ${fmt(colorMax)} m/s. Fixed scale across modes.`);
  result.planes.forEach((p, i) => $('plane').append(option(String(i), `s = ${p.downstreamM} m${p.fadedFieldIdenticallyZero ? ' · both-fades empty' : ''}`)));
  $('plane').value = '1'; // The recorded 0.6 m plane also matches the witness's fixed downstream separation.
  witness.cases.forEach((c, i) => $('witness').append(option(String(i), `${CASE_LABELS[c.id] || c.id} (${c.id})`)));
  const hoverIndex = witness.cases.findIndex(c => c.id === 'hover');
  $('witness').value = String(hoverIndex < 0 ? 0 : hoverIndex);
  const planeBody = $('plane-table').querySelector('tbody');
  result.planes.forEach(p => planeBody.append(row([p.downstreamM, p.halfWidthM, p.nominalRadialCutoffM, p.JUntruncatedN, p.JRadialOnlyN, p.JBothFadesN, p.fadedFieldIdenticallyZero ? 'Yes' : 'No'])));
  const witnessBody = $('witness-table').querySelector('tbody');
  witness.cases.forEach((c, i) => c.fields.forEach((f, k) => {
    const tr = row([c.id, String(k + 1), String(f.term), String(f.symbol), f.down, f.radial, f.projection, f.center, String(f.validity), String(f.stage)]);
    tr.dataset.caseIndex = String(i); witnessBody.append(tr);
  }));
  receipts.forEach(pin => {
    const item = document.createElement('div'); item.className = 'receipt';
    const name = document.createElement('span'); name.textContent = `${pin.path} · ${pin.bytes} bytes`;
    const hash = document.createElement('code'); hash.textContent = `SHA-256 ${pin.sha256}`;
    item.append(name, hash); $('receipts').append(item);
  });
  let scene = null;
  function updatePlane() {
    const index = Number($('plane').value), modeKey = $('mode').value;
    const plane = result.planes[index], mode = MODES[modeKey];
    say('plane-title', `s = ${plane.downstreamM} m`);
    say('mode-name', mode.label); say('plane-j', fmt(plane[mode.j]));
    say('plane-width', fmt(plane.halfWidthM)); say('plane-cutoff', fmt(plane.nominalRadialCutoffM));
    say('plane-fade', fmt(plane.downstreamFade)); say('plane-ratio', fmt(plane.JBothOverNominalWeight));
    const empty = modeKey === 'bothFades' && plane.fadedFieldIdenticallyZero;
    $('plane-state').dataset.empty = String(empty);
    say('plane-state', empty ? 'The saved both-fades field is identically zero. The nominal 3b scale is not a nonzero-support radius here.' : modeKey === 'untruncated' ? 'Untruncated reference, displayed only over the saved radial samples through r/b = 4.' : modeKey === 'radialOnly' ? 'Radial-fade reference. The downstream fade is excluded from this selected mode.' : 'Both saved fades are included. This remains an unprojected field-plane profile.');
    const tbody = $('profile-table').querySelector('tbody');
    tbody.replaceChildren(...plane.profile.map(p => row([p.xi, p.radiusM, p.untruncatedMps, p.radialOnlyMps, p.bothFadesMps])));
    [...planeBody.rows].forEach((tr, i) => tr.classList.toggle('selected', i === index));
    drawPlot(plane);
    scene?.setState(index, modeKey, mode.label);
  }
  function updateWitness() {
    const index = Number($('witness').value), c = witness.cases[index];
    say('witness-total', String(c.sourceTotalNominalN));
    say('witness-motors', c.sourceNominalRotorsN.map(String).join(' · '));
    say('witness-inflows', c.fields.map(f => String(f.term)).join(' · '));
    say('witness-calls', String(witness.calls));
    say('witness-stimulus', witness.stimulusAdmitted ? 'Recorded true' : 'Recorded false');
    say('witness-outcome', witness.sourceIndependentInTheseCases ? 'Saved assertion: source-independent in these five cases.' : 'Saved assertion: source independence failed in these cases.');
    say('witness-scope', witness.scope);
    say('witness-json', JSON.stringify(c, null, 2));
    [...witnessBody.rows].forEach(tr => tr.classList.toggle('selected', Number(tr.dataset.caseIndex) === index));
    // Deliberately no scene update: source motor state is not a profile amplitude control.
  }
  $('plane').addEventListener('change', updatePlane); $('mode').addEventListener('change', updatePlane);
  $('witness').addEventListener('change', updateWitness);
  updatePlane(); updateWitness();
  try {
    const { createProfileScene } = await import('./scene.js');
    scene = createProfileScene($('scene'), result.planes, result.constants.D, colorMax);
    $('reset-camera').disabled = false;
    $('reset-camera').addEventListener('click', () => scene.reset());
    updatePlane();
  } catch (error) {
    $('scene').replaceChildren();
    const message = document.createElement('p'); message.className = 'scene-fallback';
    message.textContent = `The 3D view is unavailable: ${error.message}. Verified profile plots and numeric tables remain available.`;
    $('scene').append(message);
  }
}
main().catch(error => {
  document.body.dataset.binding = 'failed'; $('verified-content').hidden = true;
  say('status', `Evidence display stopped: ${error.message}. No fallback or invented values are displayed. Use the protocol and evidence links above.`);
});
