import {loadEvidence, FILES, byteAt, hexByte, wordHex, region} from './evidence.js';

const $ = id => document.getElementById(id);
const set = (id, value) => { $(id).textContent = String(value); };
const element = (tag, text, className) => { const item = document.createElement(tag); if (text !== undefined) item.textContent = text; if (className) item.className = className; return item; };
const display = value => value === null || value === undefined ? 'unavailable' : typeof value === 'object' ? JSON.stringify(value) : String(value);
const flag = value => value === true ? 'reported true' : value === false ? 'reported false' : 'unavailable';
let model = null, scene = null, selected = 0, comparison = 'returned-file';

function comparisonTitle(pair) {
  if (!pair.available) return 'Unavailable';
  if (pair.exact128) return '128 / 128 bytes equal';
  return pair.equal + ' / 128 bytes equal';
}
function comparisonDetail(pair) {
  if (!pair.available) return 'Both actual inputs are required. Missing bytes are never supplied from the reference.';
  return pair.differentOrMissing + ' different or missing fixture bytes. Input lengths: ' + pair.leftBytes + ' and ' + pair.rightBytes + ' bytes.' +
    (pair.unexpectedLength ? ' At least one input has an unexpected length; exact fixture equality is false.' : ' Both inputs contain the complete 128-byte fixture.');
}
function chooseWord(index) {
  if (!model || !Number.isInteger(index) || index < 0 || index >= 32) return;
  selected = index; const offset = index * 4, pair = model.pairs[comparison];
  set('word-region', region(index).toUpperCase() + (region(index) === 'active' ? ' · COMPUTE TARGET' : ' · SENTINEL PADDING'));
  set('word-title', 'Word ' + String(index).padStart(2, '0') + ' · byte offsets ' + offset + '–' + (offset + 3));
  $('byte-rows').replaceChildren();
  for (let byte = offset; byte < offset + 4; byte++) {
    const row = element('tr');
    for (const value of [String(byte), hexByte(byteAt(model.returned, byte)), hexByte(byteAt(model.received, byte)), hexByte(byteAt(model.expected, byte))]) row.append(element('td', value));
    const state = pair.states[byte]; row.append(element('td', {match: 'equal', mismatch: 'different / missing', unknown: 'unavailable'}[state], 'state-' + state));
    $('byte-rows').append(row);
  }
  set('word-values', 'Little-endian u32 · returned ' + wordHex(model.returned, index) + ' · saved ' + wordHex(model.received, index) + ' · expected ' + wordHex(model.expected, index));
  [...$('words').children].forEach((button, word) => button.setAttribute('aria-pressed', String(word === index)));
  scene?.update(pair.states, index); document.body.dataset.word = String(index);
}
function selectComparison(value) {
  if (!model || !Object.hasOwn(model.pairs, value)) return;
  comparison = value; const pair = model.pairs[value];
  set('comparison-detail', pair.name + ': ' + comparisonTitle(pair) + '. ' + comparisonDetail(pair));
  [...$('words').children].forEach((button, word) => {
    [...button.querySelectorAll('i')].forEach((dot, index) => { dot.className = pair.states[word * 4 + index]; });
  });
  chooseWord(selected); document.body.dataset.comparison = value;
}
function showEvent(index) {
  if (!model || !Number.isInteger(index) || index < 0 || index >= model.events.length) return;
  $('event').value = String(index); set('event-record', JSON.stringify(model.events[index], null, 2));
  $('previous').disabled = index === 0; $('next').disabled = index === model.events.length - 1;
  document.body.dataset.event = String(index);
}
function addBoundary(title, role, paragraphs, projection) {
  const card = element('article', undefined, 'boundary'); card.append(element('h3', title));
  card.append(element('p', FILES[role] + (model.records.has(role) ? ' · digest-bound record' : ' · unavailable'), 'source'));
  for (const paragraph of paragraphs) card.append(element('p', paragraph));
  if (model.records.has(role)) {
    const details = element('details'); details.append(element('summary', 'Inspect retained fields'), element('pre', JSON.stringify(projection ?? model.records.get(role), null, 2))); card.append(details);
  }
  $('boundaries').append(card);
}
function renderBoundaries() {
  $('boundaries').replaceChildren();
  const get = role => model.records.get(role) ?? {};
  const page = get('returned'), host = get('host'), capture = get('captureExecution'), report = get('reviewReport'), supervisor = get('reviewSupervisor'), external = get('reviewExecution'), disposition = get('disposition');
  const groups = Array.isArray(report.groups) ? report.groups : [];
  const passed = groups.filter(group => group?.pass === true).length;
  set('host-status', model.records.has('host') ? display(host.status) : 'Unavailable');
  set('transfer-status', comparisonTitle(model.pairs['returned-file']));
  set('review-status', model.records.has('reviewReport') ? passed + ' / ' + groups.length + ' groups reported passed' : 'Unavailable');
  addBoundary('1 · Page self-report', 'returned', [
    'Page status: ' + display(page.status) + '. Last work stage: ' + display(page.lastWorkStage) + '.',
    'Mapping, copying, unmapping, destruction and device-loss fields describe page observations. This viewer does not independently reobserve those GPU events.'
  ], {kind: page.kind, fixtureId: page.fixtureId, phaseEvidenceKind: page.phaseEvidenceKind, status: page.status, lastWorkStage: page.lastWorkStage, counts: page.counts, observation: page.observation, failures: page.failures});
  addBoundary('2 · Host return and persistence', 'host', [
    'Return received: ' + flag(host.returned?.received) + '. Closed persistence: ' + flag(host.persistence?.closed) + '. Local observation complete: ' + flag(host.localObservationComplete) + '.',
    'A local complete observation or exit zero can accompany page failure or wrong bytes. Browser-close return is a separate observation from process closure.'
  ], {status: host.status, evaluation: host.evaluation, returned: host.returned, persistence: host.persistence, timing: host.timing, browserCloseReturned: host.browserCloseReturned, localObservationComplete: host.localObservationComplete, errors: host.errors, cleanupErrors: host.cleanupErrors, protocolDeviations: host.protocolDeviations});
  addBoundary('3 · External capture completion', 'captureExecution', [
    'Tool session completed: ' + flag(capture.toolSessionCompleted) + '. Recorded capture exit: ' + display(capture.actualCaptureExitCode) + '. Full elapsed: ' + display(capture.actualFullElapsedSeconds) + ' s.',
    'This is the retained external completion receipt. The viewer does not reobserve historical processes; page cleanup cannot stand in for this receipt.'
  ]);
  addBoundary('4 · Independent saved-file report', 'reviewReport', [
    model.records.has('reviewReport') ? passed + ' of ' + groups.length + ' evidence groups report pass. Record-integrity candidate: ' + flag(report.recordIntegrityCandidate) + '.' : 'No saved-file report is bound.',
    'The reviewer’s byte facts remain separate from page self-report. Its self-verified flag is ' + flag(report.recordIntegrityVerified) + '; external completion is still a distinct record.'
  ], {recordIntegrityCandidate: report.recordIntegrityCandidate, recordIntegrityVerified: report.recordIntegrityVerified, qualified: report.qualified, finding: report.finding, groups: report.groups, errors: report.errors, gpuExecutionIndependentlyAttested: report.gpuExecutionIndependentlyAttested, processClosureIndependentlyReobserved: report.processClosureIndependentlyReobserved});
  addBoundary('5 · Review supervisor', 'reviewSupervisor', [
    model.records.has('reviewSupervisor') ? 'An actual supervisor receipt is bound; inspect its recorded child exit and bounded completion observations.' : 'The supervisor receipt is unavailable.',
    'The reviewer has a 30-second limit inside a 35-second supervisor bound. The supervisor’s own receipt does not replace the caller’s observed completion.'
  ], supervisor);
  addBoundary('6 · External review completion', 'reviewExecution', [
    'Tool session completed: ' + flag(external.toolSessionCompleted) + '. Recorded supervisor exit: ' + display(external.actualSupervisorExitCode) + '. Full elapsed: ' + display(external.actualFullElapsedSeconds) + ' s.',
    'The retained checker-exit projection is ' + display(external.actualCheckerExitCode) + '. It is distinct from the supervisor exit and does not promote matching bytes to an overall result.'
  ]);
  addBoundary('7 · Root terminal disposition', 'disposition', [
    'Root’s byte-readback verification within this fixture: ' + flag(disposition.byteReadbackVerifiedWithinFixture) + '. Scientific qualification: ' + flag(disposition.scientificQualified) + '.',
    display(disposition.scope), display(disposition.processClosureScope)
  ]);
  set('interpretation', disposition.byteReadbackVerifiedWithinFixture === true
    ? 'The root disposition reports byte-readback verification within this fixed fixture. The displayed comparisons use actual bound return and file bytes; page phases and external completion retain the separate evidence scopes shown above.'
    : 'The root disposition does not report verified byte readback within this fixture. Inspect the bound failures, missing artifacts and separate completion records for the retained outcome.');
}
function renderFailures() {
  $('failures').replaceChildren(); const messages = [...model.issues];
  for (const role of ['host', 'returned', 'captureExecution', 'reviewReport', 'reviewSupervisor', 'reviewExecution']) {
    if (!model.records.has(role)) messages.push(FILES[role] + ' has no available decoded record.');
  }
  const fields = [['budget', 'errors'], ['capture', 'errors'], ['returned', 'failures'], ['host', 'errors'], ['host', 'cleanupErrors'], ['host', 'protocolDeviations'], ['reviewReport', 'errors']];
  for (const [role, field] of fields) {
    const entries = model.records.get(role)?.[field];
    if (Array.isArray(entries)) for (const entry of entries) messages.push(FILES[role] + ' · ' + field + ': ' + display(entry));
  }
  const groups = model.records.get('reviewReport')?.groups;
  if (Array.isArray(groups)) for (const group of groups) if (group?.pass !== true) messages.push('Saved review group did not pass: ' + display(group?.group));
  const rejection = model.records.get('rejectedReturn');
  if (rejection) messages.push('Rejected-return projection: ' + display(rejection.errorCode) + '. Original rejected object retained: ' + flag(rejection.originalRetained) + '.');
  for (const pair of Object.values(model.pairs)) if (pair.available && !pair.exact128) messages.push(pair.name + ': ' + comparisonDetail(pair));
  if (!messages.length) messages.push('No failure entries were found in the selected bound fields. That absence is not an independent successful-trial determination.');
  for (const message of messages) $('failures').append(element('li', message));
}
function renderData() {
  $('words').replaceChildren();
  for (let index = 0; index < 32; index++) {
    const button = element('button', undefined, 'word ' + region(index)); button.type = 'button'; button.setAttribute('aria-pressed', 'false');
    button.setAttribute('aria-label', 'Word ' + index + ', ' + region(index) + ', byte offsets ' + (index * 4) + ' to ' + (index * 4 + 3));
    button.append(element('span', 'Word ' + String(index).padStart(2, '0')), element('small', region(index)));
    const dots = element('span', undefined, 'dots'); dots.setAttribute('aria-hidden', 'true'); for (let byte = 0; byte < 4; byte++) dots.append(element('i')); button.append(dots);
    button.addEventListener('click', () => chooseWord(index)); $('words').append(button);
  }
  $('comparison-cards').replaceChildren();
  for (const pair of Object.values(model.pairs)) {
    const card = element('article', undefined, 'comparison-card'); card.append(element('h3', pair.name), element('strong', comparisonTitle(pair), pair.available ? pair.exact128 ? 'state-match' : 'state-mismatch' : 'state-unknown'), element('p', comparisonDetail(pair))); $('comparison-cards').append(card);
  }
  renderBoundaries(); renderFailures();
  $('event').replaceChildren();
  if (model.events.length) {
    model.events.forEach((event, index) => { const option = element('option', (index + 1) + ' · ' + display(event.kind ?? event.event ?? event.type)); option.value = String(index); $('event').append(option); });
    $('event').disabled = false; showEvent(0);
  } else { $('event').append(element('option', 'No saved events bound')); set('event-record', 'Unavailable'); }
  $('receipts').replaceChildren();
  for (const file of [model.manifest, ...model.files]) {
    const receipt = element('div', undefined, 'receipt'); const link = element('a', file.path); link.href = file.path;
    receipt.append(link, document.createTextNode(' · ' + file.bytes + ' bytes'), element('code', 'SHA-256 ' + file.sha256)); $('receipts').append(receipt);
  }
  $('comparison').disabled = false; selectComparison(comparison);
  set('binding-status', 'All declared file digests match');
  set('status', 'Bound to actual terminal trial records. Byte colors describe the selected comparison; each record keeps its own evidence scope.');
  document.body.dataset.ready = 'true'; document.body.dataset.binding = 'verified';
}

$('comparison').addEventListener('change', () => selectComparison($('comparison').value));
$('event').addEventListener('change', () => showEvent(Number($('event').value)));
$('previous').addEventListener('click', () => showEvent(Number($('event').value) - 1));
$('next').addEventListener('click', () => showEvent(Number($('event').value) + 1));
$('reset').addEventListener('click', () => { scene?.reset(); document.body.dataset.camera = 'reset'; });
window.addEventListener('pagehide', () => scene?.dispose(), {once: true});

try {
  model = await loadEvidence();
  if (model) {
    renderData();
    try {
      const {createByteScene} = await import('./scene.js'); scene = createByteScene($('scene'), chooseWord);
      scene.update(model.pairs[comparison].states, selected); $('reset').disabled = false;
      set('scene-status', '128 byte cells · four per word. Base strips mark prefix, active region and suffix. Drag to orbit; choose a word to inspect all three inputs.');
    } catch {
      $('scene').replaceChildren(element('p', '3D view unavailable · use the word selector and byte table', 'scene-placeholder'));
      set('scene-status', 'The 3D renderer is unavailable. The bound records, comparisons and accessible byte table remain available.');
      document.body.dataset.renderer = 'unavailable';
    }
  }
} catch (error) {
  model = null; scene?.dispose(); document.body.dataset.ready = 'false'; document.body.dataset.binding = 'failed';
  for (const id of ['comparison', 'event', 'previous', 'next', 'reset']) $(id).disabled = true;
  for (const id of ['words', 'boundaries', 'comparison-cards', 'receipts']) $(id).replaceChildren();
  $('event').replaceChildren(element('option', 'No verified events bound'));
  $('failures').replaceChildren(element('li', 'Evidence binding is unavailable or invalid. No trial conclusion is displayed.'));
  const row = element('tr'), cell = element('td', 'No verified byte data is displayed.'); cell.colSpan = 5; row.append(cell); $('byte-rows').replaceChildren(row);
  set('word-region', 'NO WORD SELECTED'); set('word-title', 'Byte details unavailable'); set('word-values', 'Unavailable'); set('comparison-detail', 'Comparison unavailable.'); set('event-record', 'Unavailable');
  set('binding-status', 'Binding unavailable or invalid'); set('host-status', 'Unavailable'); set('transfer-status', 'Unavailable'); set('review-status', 'Unavailable');
  set('status', error?.name === 'AbortError' ? 'Evidence loading exceeded its time bound. No result is displayed.' : 'No result is displayed. ' + (error?.message || 'Evidence loading failed.'));
  set('interpretation', 'No trial conclusion is available. A missing or invalid binding cannot supply a result.');
  $('scene').replaceChildren(element('p', 'Evidence unavailable', 'scene-placeholder'));
}
