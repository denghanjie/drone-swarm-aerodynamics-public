import {createScene} from './scene.js';

const $ = id => document.getElementById(id);
const CHANNELS = ['rotor', 'force', 'moment'];
const LABELS = {rotor: 'Rotor load · mg/4', force: 'Collective force · mg', moment: 'Body moment · mgR'};
const EXPECTED = Object.freeze({
  config: '../config.json',
  events: '../results/events.jsonl',
  summary: '../results/summary.json',
  independentReview: '../results/independent-review.json',
  candidateRun: '../results/candidate-run.json',
  reviewRun: '../results/review-run.json',
  source: '../../m31-ratio-reuse-2026-10-16/results/boids16-reuse10ms-0.00125.json'
});
const SOURCE_PATH = 'research/m31-ratio-reuse-2026-10-16/results/boids16-reuse10ms-0.00125.json';
const state = {verified: false, frame: 0, mode: 'predict', metric: 'rotor', timer: null, scene: null, data: null};

function require(ok, message) { if (!ok) throw new Error(message); }
function sameSaved(a, b) {
  if (a === b) return true;
  if (!a || !b || typeof a !== 'object' || typeof b !== 'object') return false;
  const keys = Object.keys(a);
  return keys.length === Object.keys(b).length && keys.every(k => Object.hasOwn(b, k) && sameSaved(a[k], b[k]));
}
function finite(x) { return typeof x === 'number' && Number.isFinite(x); }
function nonnegative(x) { return finite(x) && x >= 0; }
function vector(v, n, predicate = finite) { return Array.isArray(v) && v.length === n && v.every(predicate); }
function matrix(v, n, m, predicate = finite) { return Array.isArray(v) && v.length === n && v.every(row => vector(row, m, predicate)); }
function format(value) {
  if (value === null || value === undefined) return 'Not scored';
  if (!finite(value)) return 'Unavailable';
  return value === 0 ? '0' : value < 0.0001 ? value.toExponential(3) : value.toPrecision(5);
}
function location(value) {
  if (!value) return 'No complete location';
  const parts = [];
  if (Number.isInteger(value.event)) parts.push('event ' + value.event);
  if (Number.isInteger(value.drone)) parts.push('drone ' + value.drone);
  if (Number.isInteger(value.rotor)) parts.push('rotor ' + value.rotor);
  return parts.join(' · ');
}
function cell(text, className = '') {
  const node = document.createElement('td');
  node.textContent = text;
  node.className = className;
  return node;
}
function numberCell(value, where = null) {
  const node = cell(format(value));
  if (where) {
    const small = document.createElement('span');
    small.className = 'location';
    small.textContent = location(where);
    node.append(small);
  }
  return node;
}
function booleanStatus(node, value, labels = ['Passed', 'Failed']) {
  node.textContent = value === true ? labels[0] : value === false ? labels[1] : 'Unresolved';
  node.className = value === true ? 'pass' : value === false ? 'fail' : 'unresolved';
}
function readField(record, name) {
  // Deliberately only a direct field: pending reviewer schema cannot fall back optimistically.
  return typeof name === 'string' && Object.hasOwn(record, name) ? record[name] : undefined;
}

async function bound(key, pin) {
  require(pin && pin.url === EXPECTED[key], 'Unexpected or missing artifact path: ' + key);
  require(Number.isSafeInteger(pin.bytes) && pin.bytes > 0 && /^[a-f0-9]{64}$/.test(pin.sha256), 'Unfinalized artifact pin: ' + key);
  require(pin.format === (key === 'events' ? 'jsonl' : 'json'), 'Unknown artifact format: ' + key);
  const url = new URL(pin.url, import.meta.url);
  require(url.origin === locationOrigin(), 'Artifact must remain on this origin');
  const response = await fetch(url, {cache: 'no-store'});
  require(response.ok, 'Missing artifact: ' + key);
  const bytes = await response.arrayBuffer();
  require(bytes.byteLength === pin.bytes, 'Byte-length mismatch: ' + key);
  require(globalThis.crypto?.subtle, 'SHA-256 verification is unavailable');
  const sha = Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256', bytes)), value => value.toString(16).padStart(2, '0')).join('');
  require(sha === pin.sha256, 'SHA-256 mismatch: ' + key);
  const text = new TextDecoder('utf-8', {fatal: true}).decode(bytes);
  if (pin.format === 'jsonl') {
    const lines = text.trimEnd().split('\n');
    require(lines.length > 0 && lines.every(line => line.trim()), 'Blank or empty event record');
    return lines.map(line => JSON.parse(line));
  }
  return JSON.parse(text);
}
function locationOrigin() { return new URL(import.meta.url).origin; }

function validateError(error, label) {
  if (error === null) return;
  require(error && matrix(error.rotor, 16, 4, nonnegative) && vector(error.force, 16, nonnegative) && vector(error.moment, 16, nonnegative), 'Saved error shape: ' + label);
  for (const channel of CHANNELS) {
    require(nonnegative(error.maxima?.[channel]), 'Missing saved maximum: ' + label);
    require(Number.isInteger(error.argmax?.[channel]?.drone) && error.argmax[channel].drone >= 0 && error.argmax[channel].drone < 16, 'Invalid saved error location');
  }
}
function validateSummaryGroup(group, count, primary = false) {
  require(group?.targets === count && Number.isInteger(group.scoredEvents) && Number.isInteger(group.invalidRoots), 'Summary population mismatch');
  for (const mode of ['predict', 'hold']) {
    require(typeof group.modes?.[mode]?.complete === 'boolean', 'Missing summary coverage');
    for (const channel of CHANNELS) {
      for (const key of ['maxima', 'finiteDiagnosticMaxima']) {
        const value = group.modes[mode][key]?.[channel];
        require(value === null || nonnegative(value), 'Missing saved summary maximum');
      }
    }
  }
  if (primary) {
    require(typeof group.pass === 'boolean', 'Missing primary decision');
    for (const channel of CHANNELS) {
      const gate = group.gates?.[channel];
      require(gate?.tolerance === 0.001 && typeof gate.absolute === 'boolean' && typeof gate.noWorseThanHold === 'boolean', 'Missing saved primary gate');
    }
  }
}
function validateData(data, binding) {
  const {config, events, summary, source} = data;
  require(config.kind === 'causal-saved-joint-root-secant' && config.n === 16 && config.events === 201 && config.targets === 200, 'Unsupported study configuration');
  require(CHANNELS.every(key => config.thresholds?.[key] === 0.001), 'Unexpected declared screens');
  require(config.input?.path === SOURCE_PATH && config.input.bytes === binding.artifacts.source.bytes && config.input.sha256 === binding.artifacts.source.sha256, 'Configuration/input pin disagreement');
  require(summary.kind === config.kind && summary.input?.path === config.input.path && summary.input.bytes === config.input.bytes && summary.input.sha256 === config.input.sha256, 'Summary/input pin disagreement');
  require(summary.complete === true && summary.inputAdmission === true && typeof summary.scientificPass === 'boolean' && typeof summary.decision === 'string', 'Saved experiment incomplete or unadmitted');
  require(summary.scientificPass === summary.primary?.pass, 'Inconsistent saved result decision');
  require(source.complete === true && source.failure === null && source.id === 'boids16-reuse10ms-0.00125' && source.mode === 'reuse10ms', 'Original recording identity is incomplete');
  require(Array.isArray(source.events) && source.events.length === 201 && Array.isArray(events) && events.length === 200, 'Event coverage is incomplete');
  source.events.forEach((event, index) => {
    require(event.index === index && finite(event.t) && event.t === Math.round(index * 0.01 * 1e6) / 1e6 && event.status === 'completed', 'Original event ordering mismatch');
    require(matrix(event.states, 16, 17), 'Original saved pose shape mismatch');
  });
  events.forEach((event, offset) => {
    const index = offset + 1;
    require(event.index === index && event.t === source.events[index].t, 'Target/source event mismatch');
    require(event.method === (index === 1 ? 'cold-start-hold' : 'secant'), 'Unexpected saved startup policy');
    require(typeof event.validRoots === 'boolean' && Array.isArray(event.invalidRoots), 'Missing saved domain status');
    require(event.scoreStatus === 'scored' || event.scoreStatus === 'unscored', 'Missing saved scoring status');
    require(event.errors && Object.hasOwn(event.errors, 'predict') && Object.hasOwn(event.errors, 'hold'), 'Missing saved errors');
    require(event.errors.hold !== null, 'Missing held-comparator diagnostic');
    validateError(event.errors.predict, 'prediction event ' + index);
    validateError(event.errors.hold, 'hold event ' + index);
    for (const invalid of event.invalidRoots) {
      require(Number.isInteger(invalid.drone) && invalid.drone >= 0 && invalid.drone < 16 && Number.isInteger(invalid.rotor) && invalid.rotor >= 0 && invalid.rotor < 4 && typeof invalid.reason === 'string', 'Malformed invalid-root record');
    }
  });
  validateSummaryGroup(summary.primary, 200, true);
  validateSummaryGroup(summary.secondarySecantOnly, 199);
}

function showSavedReview(data, binding) {
  const review = data.independentReview;
  const fields = binding.reviewFields;
  const passed = readField(review, fields?.pass);
  const complete = readField(review, fields?.complete);
  const reviewOkay = passed === true && complete === true;
  booleanStatus($('review-status'), reviewOkay ? true : passed === false ? false : undefined);
  if (complete === false && passed !== false) $('review-status').textContent = 'Incomplete';
  $('review-detail').textContent = 'Saved pass: ' + String(passed ?? 'missing') + ' · complete: ' + String(complete ?? 'missing') + '. This is an audit, not a physical experiment.';
  for (const [key, id] of [['candidateRun', 'candidate-status'], ['reviewRun', 'review-run-status']]) {
    const run = data[key];
    const okay = run.supervisorSuccess === true && run.closed === true && run.returncode === 0;
    const failed = run.supervisorSuccess === false || run.closed === false || (Number.isInteger(run.returncode) && run.returncode !== 0);
    booleanStatus($(id), okay ? true : failed ? false : undefined, ['closed / successful', 'failed / incomplete']);
    $(id).title = 'supervisorSuccess=' + String(run.supervisorSuccess ?? 'missing') + '; closed=' + String(run.closed ?? 'missing') + '; returncode=' + String(run.returncode ?? 'missing');
  }
  $('audit-detail').textContent = 'Independent review: ' + fields?.pass + '=' + String(passed ?? 'missing') + ', ' + fields?.complete + '=' + String(complete ?? 'missing') + '. Candidate and reviewer supervisor closures are checked separately.';
  return reviewOkay && data.candidateRun.supervisorSuccess === true && data.candidateRun.closed === true && data.candidateRun.returncode === 0 && data.reviewRun.supervisorSuccess === true && data.reviewRun.closed === true && data.reviewRun.returncode === 0;
}

function renderTables(data) {
  const {primary, secondarySecantOnly: secondary} = data.summary;
  $('primary-rows').replaceChildren();
  $('secondary-rows').replaceChildren();
  $('finite-rows').replaceChildren();
  const startup = data.events[0];
  for (const channel of CHANNELS) {
    const row = document.createElement('tr');
    const gate = primary.gates[channel];
    row.append(cell(LABELS[channel]), numberCell(primary.modes.predict.maxima[channel], primary.modes.predict.argmax?.[channel]), numberCell(primary.modes.hold.maxima[channel], primary.modes.hold.argmax?.[channel]), cell(format(gate.tolerance)), cell(gate.absolute ? 'Pass' : 'Miss', gate.absolute ? 'gate-pass' : 'gate-fail'), cell(gate.noWorseThanHold ? 'Pass' : 'Miss', gate.noWorseThanHold ? 'gate-pass' : 'gate-fail'));
    $('primary-rows').append(row);
    const other = document.createElement('tr');
    other.append(cell(LABELS[channel]), numberCell(startup.errors.predict?.maxima[channel] ?? null), numberCell(secondary.modes.predict.maxima[channel]), numberCell(secondary.modes.hold.maxima[channel]));
    $('secondary-rows').append(other);
    const diagnostic = document.createElement('tr');
    diagnostic.append(cell(LABELS[channel]), numberCell(primary.modes.predict.finiteDiagnosticMaxima[channel]), numberCell(primary.modes.hold.finiteDiagnosticMaxima[channel]));
    $('finite-rows').append(diagnostic);
  }
  $('finite-diagnostics').hidden = primary.modes.predict.complete && primary.modes.hold.complete;
  $('primary-note').textContent = primary.invalidRoots > 0 ? 'The saved summary records ' + primary.invalidRoots + ' invalid predicted roots across ' + primary.invalidEvents + ' events. Finite maxima remain invalid-domain diagnostics; they cannot override this rejection.' : 'Primary maxima include every target. The complete-set decision is separate from individual gate results.';
  $('secondary-note').textContent = 'Secondary diagnostic coverage: ' + secondary.scoredEvents + ' / 199 scored; ' + secondary.invalidRoots + ' invalid predicted roots. These finite diagnostics do not qualify invalid predictions. No secondary pass is defined. Mandatory cold start remains in the 200-event primary result.';
  $('event-rows').replaceChildren();
  for (const event of data.events) {
    const row = document.createElement('tr');
    row.dataset.event = String(event.index);
    if (!event.validRoots) row.classList.add('invalid-event');
    const first = cell('');
    const button = document.createElement('button');
    button.textContent = event.index + ' · ' + event.t.toFixed(2) + ' s';
    button.disabled = true;
    button.dataset.control = '';
    button.dataset.event = String(event.index);
    button.addEventListener('click', () => { if (!state.verified) return; pause(); show(event.index); $('scene-heading').scrollIntoView({block: 'start', behavior: 'auto'}); });
    first.append(button);
    row.append(first, cell(event.index === 1 ? 'Cold-start hold' : 'Secant'));
    for (const channel of CHANNELS) for (const mode of ['predict', 'hold']) row.append(numberCell(event.errors[mode]?.maxima[channel] ?? null));
    row.append(cell(event.validRoots ? 'Valid roots' : event.invalidRoots.length + ' invalid', event.validRoots ? '' : 'gate-fail'));
    $('event-rows').append(row);
  }
}

function pause() {
  if (state.timer !== null) clearInterval(state.timer);
  state.timer = null;
  $('play').textContent = 'Play events';
  document.body.dataset.playing = 'false';
}
function show(index) {
  if (!state.verified || !Number.isInteger(index) || index < 0 || index > 200) return;
  state.frame = index;
  const source = state.data.source.events[index];
  const event = index ? state.data.events[index - 1] : null;
  const errors = event?.errors[state.mode] ?? null;
  state.scene.frame(index, errors, state.metric, state.mode === 'predict' ? event?.invalidRoots ?? [] : [], index === 0);
  $('frame').value = String(index);
  $('time').textContent = source.t.toFixed(2) + ' s';
  const method = index === 0 ? 'History initialization' : index === 1 ? 'Cold start · included' : index === 200 ? 'Terminal audit · included' : 'Positive target';
  $('event-label').textContent = 'Event ' + index + ' / 200 · ' + method;
  $('scene').setAttribute('aria-label', 'Exact saved poses at ' + source.t.toFixed(2) + ' seconds. ' + (state.mode === 'predict' ? 'Secant prediction' : 'Last-value hold') + ', ' + LABELS[state.metric] + '.');
  for (const channel of CHANNELS) {
    $('event-' + channel).textContent = errors ? format(errors.maxima[channel]) : 'Not scored';
    $('event-' + channel + '-location').textContent = errors ? location(errors.argmax[channel]) : index ? 'No computable saved value' : 'Initialization only';
  }
  $('event-note').textContent = index === 0 ? 't = 0 supplies fresh history. It has no target error; gray is not a zero-error claim.' : 'Saved ' + (state.mode === 'predict' ? 'prediction' : 'hold') + ' maxima at this same state. Predictor method: ' + event.method + '; saved scoring status: ' + event.scoreStatus + (event.scoreReason ? ' (' + event.scoreReason + ')' : '') + '. No new loads are computed here.';
  const invalids = event?.invalidRoots ?? [];
  $('invalid-note').hidden = invalids.length === 0;
  if (invalids.length) {
    const descriptions = invalids.slice(0, 8).map(v => 'drone ' + v.drone + ', rotor ' + v.rotor + ': ' + v.reason + (v.value === null ? '' : ' (' + format(v.value) + ')'));
    $('invalid-note').textContent = 'Invalid predictions at this event: ' + invalids.length + '. ' + descriptions.join('; ') + (invalids.length > 8 ? '; further entries are retained in the event record.' : '.') + (state.mode === 'hold' ? ' Hold colors describe the valid comparator; the prediction remains rejected.' : ' Magenta overrides error color for the affected rotor and drone body.');
  }
  $('color-explanation').textContent = state.metric === 'rotor' ? 'Each ring uses its saved rotor error. The body uses the largest of that drone’s four saved error values; this is a display mapping, not a new score.' : 'Each drone and its four rotor rings use its saved ' + (state.metric === 'force' ? 'collective-force' : 'body-moment') + ' vector-norm error. Colors saturate at five times the 0.001 screen.';
  for (const row of $('event-rows').children) row.setAttribute('aria-current', String(Number(row.dataset.event) === index));
  $('previous').disabled = index === 0;
  $('next').disabled = index === 200;
  document.body.dataset.event = String(index);
  document.body.dataset.mode = state.mode;
  document.body.dataset.metric = state.metric;
}
function wireControls() {
  $('scene').addEventListener('scene-failure', event => fail(new Error(event.detail)));
  for (const mode of ['predict', 'hold']) $('mode-' + mode).addEventListener('click', () => {
    if (!state.verified) return;
    state.mode = mode;
    for (const other of ['predict', 'hold']) $('mode-' + other).setAttribute('aria-pressed', String(other === mode));
    show(state.frame);
  });
  $('metric').addEventListener('change', () => { if (!state.verified) return; state.metric = $('metric').value; show(state.frame); });
  $('frame').addEventListener('input', () => { pause(); show(Number($('frame').value)); });
  $('previous').addEventListener('click', () => { pause(); show(state.frame - 1); });
  $('next').addEventListener('click', () => { pause(); show(state.frame + 1); });
  $('play').addEventListener('click', () => {
    if (!state.verified) return;
    if (state.timer !== null) { pause(); return; }
    if (state.frame === 200) show(0);
    $('play').textContent = 'Pause events';
    document.body.dataset.playing = 'true';
    state.timer = setInterval(() => { show(state.frame + 1); if (state.frame === 200) pause(); }, 40);
  });
  $('reset').addEventListener('click', () => { if (state.verified) state.scene.reset(); });
  $('size').addEventListener('change', () => { if (state.verified) state.scene.size(Number($('size').value)); });
  document.addEventListener('visibilitychange', () => { if (document.hidden) pause(); });
}

async function main() {
  wireControls();
  const response = await fetch(new URL('./binding.json', import.meta.url), {cache: 'no-store'});
  require(response.ok, 'Missing viewer binding');
  const binding = await response.json();
  require(binding.schema === 'm31-root-secant-viewer-v1', 'Unknown viewer binding schema');
  if (binding.ready !== true) {
    $('status').textContent = 'Result binding is not finalized. No preview data is loaded; every event control remains locked.';
    return;
  }
  require(binding.artifacts && Object.keys(binding.artifacts).length === Object.keys(EXPECTED).length, 'Incomplete artifact binding map');
  $('status').textContent = 'Verifying saved records and the referenced original trajectory by byte length and SHA-256…';
  const entries = await Promise.all(Object.keys(EXPECTED).map(async key => [key, await bound(key, binding.artifacts[key])]));
  const data = Object.fromEntries(entries);
  booleanStatus($('pin-status'), true, ['verified', 'mismatch']);
  const audited = showSavedReview(data, binding);
  $('pins').replaceChildren();
  for (const key of Object.keys(EXPECTED)) {
    const pin = binding.artifacts[key], item = document.createElement('li');
    item.textContent = key + ' · ' + pin.url + ' · ' + pin.bytes.toLocaleString('en-US') + ' bytes · SHA-256 ' + pin.sha256;
    $('pins').append(item);
  }
  require(audited, 'Saved review or supervisor closure is missing, failed, or incomplete. Results remain unqualified.');
  require(data.independentReview.kind === 'independent-saved-root-secant-review' && Array.isArray(data.independentReview.failures) && data.independentReview.failures.length === 0, 'Independent review contract or failure list is unresolved');
  require(data.independentReview.scientificPass === data.summary.scientificPass && data.independentReview.decision === data.summary.decision, 'Independent review and summary scientific result disagree');
  require(sameSaved(data.independentReview.primary, data.summary.primary) && sameSaved(data.independentReview.secondarySecantOnly, data.summary.secondarySecantOnly), 'Independent review and displayed result tables disagree');
  validateData(data, binding);
  state.data = data;
  state.scene = createScene($('scene'));
  state.scene.load(data.source.events, 16);
  state.scene.size(Number($('size').value));
  renderTables(data);
  const summary = data.summary, primary = summary.primary;
  $('decision').textContent = summary.scientificPass ? 'Passed endpoint screen' : 'Prediction rejected';
  $('decision').className = summary.scientificPass ? 'pass' : 'fail';
  $('decision-detail').textContent = summary.scientificPass ? 'The saved endpoints meet the declared screen.' : 'The largest errors were smaller, but all three still exceeded the limits.';
  $('coverage').textContent = primary.scoredEvents + ' / ' + primary.targets;
  $('coverage-detail').textContent = primary.invalidRoots + ' invalid predicted roots in ' + primary.invalidEvents + ' events. Scored coverage includes finite invalid-domain diagnostics. Startup and terminal audit remain included.';
  state.verified = true;
  for (const control of document.querySelectorAll('[data-control]')) control.disabled = false;
  $('scene-placeholder').hidden = true;
  document.body.dataset.binding = 'verified';
  document.body.dataset.decision = summary.decision;
  $('status').textContent = 'All seven data artifacts verified. Both supervised invocations and the independent saved-data review passed. Scientific result: ' + summary.decision + '.';
  show(0);
}
function fail(error) {
  state.verified = false;
  pause();
  for (const control of document.querySelectorAll('[data-control]')) control.disabled = true;
  document.body.dataset.binding = 'failed';
  $('status').className = 'status error';
  $('status').textContent = 'Display stopped: ' + error.message;
  $('decision').textContent = 'Unresolved';
  $('decision').className = 'unresolved';
  $('decision-detail').textContent = 'Evidence or audit verification did not qualify this display.';
  $('scene-placeholder').hidden = false;
}
main().catch(fail);
