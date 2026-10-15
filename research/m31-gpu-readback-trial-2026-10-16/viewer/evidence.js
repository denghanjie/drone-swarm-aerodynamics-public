// Presentation-only adapter. No diagnostic or saved-review code is imported.
export const CAMPAIGN = 'm31-gpu-readback-trial-2026-10-16';
export const FIXTURE = 'm31-u32-readback-128-v1';
export const EXPECTED_SHA256 = 'ba507e3ef0ad8991b3e84530f89fa51501e9c6fd274157d519ef10cb8aded951';
const CAP = 8388608;
export const FILES = Object.freeze({
  expected: 'expected.bin',
  returned: 'raw/returned.json',
  received: 'raw/received.bin',
  rejectedReturn: 'raw/rejected-return.json',
  trace: 'raw/trace.public.ndjson',
  host: 'results/result.json',
  relay: 'results/wrapper.json',
  budget: 'results/budget.json',
  capture: 'results/capture.json',
  captureExecution: 'publication/capture-execution.json',
  captureOutput: 'publication/capture-output.json',
  observerOutput: 'publication/observer-output.json',
  reviewReport: 'review/results/report.json',
  reviewSummary: 'review/results/summary.json',
  reviewManifest: 'review/evidence-manifest.json',
  reviewSupervisor: 'publication/review-supervisor.json',
  reviewOutput: 'publication/review-output.json',
  reviewExecution: 'publication/review-execution.json',
  disposition: 'publication/FINAL-DISPOSITION.json',
  freeze: 'freeze.json',
});

function require(condition, message) { if (!condition) throw new Error(message); }
const object = value => value !== null && typeof value === 'object' && !Array.isArray(value);
export const sha256 = async bytes => Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256', bytes)), n => n.toString(16).padStart(2, '0')).join('');
const decode = bytes => new TextDecoder('utf-8', {fatal: true}).decode(bytes);
const json = bytes => JSON.parse(decode(bytes));

async function readBounded(url, cap, signal, allowMissing = false) {
  const response = await fetch(url, {cache: 'no-store', signal, credentials: 'same-origin', redirect: 'error'});
  if (allowMissing && response.status === 404) return null;
  require(response.ok, 'A declared evidence file is unavailable.');
  const declared = response.headers.get('content-length');
  if (declared !== null) require(/^\d+$/.test(declared) && Number(declared) <= cap, 'Evidence response exceeds its size bound.');
  require(response.body, 'Evidence response has no readable body.');
  const reader = response.body.getReader();
  const chunks = []; let length = 0;
  try {
    for (;;) {
      const part = await reader.read();
      if (part.done) break;
      length += part.value.byteLength;
      require(length <= cap, 'Evidence response exceeds its size bound.');
      chunks.push(part.value);
    }
  } catch (error) { await reader.cancel().catch(() => {}); throw error; }
  finally { reader.releaseLock(); }
  const bytes = new Uint8Array(length); let offset = 0;
  for (const chunk of chunks) { bytes.set(chunk, offset); offset += chunk.byteLength; }
  return bytes;
}

async function bound(descriptor, expectedPath, cap, signal) {
  require(object(descriptor) && descriptor.path === expectedPath, 'Unexpected evidence path.');
  require(Number.isSafeInteger(descriptor.bytes) && descriptor.bytes >= 0 && descriptor.bytes <= cap &&
    typeof descriptor.sha256 === 'string' && /^[a-f0-9]{64}$/.test(descriptor.sha256), 'Invalid evidence descriptor.');
  const url = new URL(expectedPath, location.href);
  require(url.origin === location.origin, 'Evidence must stay on this origin.');
  const bytes = await readBounded(url.href, descriptor.bytes, signal);
  require(bytes.byteLength === descriptor.bytes && await sha256(bytes) === descriptor.sha256, 'A saved file does not match its bound length or SHA-256.');
  return bytes;
}

export async function loadEvidence() {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), 15000);
  try {
    const initial = await readBounded(new URL('./binding.json', location.href).href, 16384, controller.signal, true);
    if (initial === null) return null;
    const binding = json(initial);
    require(binding.schema === 'm31-gpu-readback-view-binding-v1', 'Unsupported viewer binding.');
    const artifactBytes = await bound(binding, './evidence.json', 32768, controller.signal);
    const artifact = json(artifactBytes);
    require(object(artifact) && artifact.schema === 'm31-gpu-readback-view-v1' && artifact.campaign === CAMPAIGN &&
      artifact.fixtureId === FIXTURE && Array.isArray(artifact.files) && artifact.files.length > 0 &&
      artifact.files.length <= Object.keys(FILES).length, 'Unexpected viewer evidence manifest.');
    const byRole = new Map(); let total = 0;
    // Validate every descriptor and aggregate bound before reading payloads.
    for (const file of artifact.files) {
      require(object(file) && Object.hasOwn(FILES, file.role) && !byRole.has(file.role), 'Unknown or repeated evidence role.');
      require(file.path === '../' + FILES[file.role] && Number.isSafeInteger(file.bytes) && file.bytes >= 0, 'Invalid evidence descriptor.');
      total += file.bytes; require(total <= CAP, 'Aggregate evidence size exceeds 8 MiB.');
      byRole.set(file.role, file);
    }
    require(byRole.has('disposition'), 'Terminal disposition is required for a recorded trial view.');
    const bytes = new Map(); const records = new Map(); const issues = [];
    for (const [role, file] of byRole) {
      const data = await bound(file, '../' + FILES[role], CAP, controller.signal);
      bytes.set(role, data);
      if (!['expected', 'received', 'trace'].includes(role)) {
        try {
          const record = json(data); require(object(record), 'An evidence record is not an object.'); records.set(role, record);
        } catch (error) {
          if (role === 'disposition') throw error;
          issues.push(FILES[role] + ' is digest-bound but cannot be decoded as a JSON object. Its fields are unavailable; the raw file remains linked.');
        }
      }
    }
    if (bytes.has('expected')) require(bytes.get('expected').length === 128 && await sha256(bytes.get('expected')) === EXPECTED_SHA256, 'Expected reference does not match the pinned 128-byte fixture.');
    const disposition = records.get('disposition');
    require(disposition.diagnosticTerminal === true && disposition.savedReviewTerminal === true && disposition.scientificQualified === false,
      'The root disposition does not mark both allocated stages closed.');
    const model = buildModel(bytes, records, issues);
    return {...model, files: artifact.files, manifest: {path: './evidence.json', bytes: artifactBytes.length, sha256: await sha256(artifactBytes)}};
  } finally { clearTimeout(timer); }
}

export function region(index) { return index < 4 ? 'prefix' : index < 21 ? 'active' : 'suffix'; }
export function byteAt(bytes, index) { return bytes !== null && index < bytes.length ? bytes[index] : null; }
export function hexByte(value) { return value === null ? '—' : value.toString(16).padStart(2, '0'); }
export function wordHex(bytes, index) {
  if (bytes === null || bytes.length < index * 4 + 4) return 'unavailable';
  return '0x' + new DataView(bytes.buffer, bytes.byteOffset + index * 4, 4).getUint32(0, true).toString(16).padStart(8, '0');
}

export function compare(left, right) {
  const available = left !== null && right !== null;
  const states = Array.from({length: 128}, (_, index) => {
    if (!available) return 'unknown';
    const a = byteAt(left, index), b = byteAt(right, index);
    return a !== null && b !== null && a === b ? 'match' : 'mismatch';
  });
  const equal = states.filter(value => value === 'match').length;
  return {available, states, equal: available ? equal : null, differentOrMissing: available ? 128 - equal : null,
    leftBytes: left?.length ?? null, rightBytes: right?.length ?? null,
    exact128: available && left.length === 128 && right.length === 128 && equal === 128,
    unexpectedLength: available && (left.length !== 128 || right.length !== 128)};
}

function buildModel(bytes, records, issues) {
  const page = records.get('returned') ?? null;
  let returned = null;
  if (page) {
    if (page.kind !== 'synthetic-gpu-readback-envelope' || page.fixtureId !== FIXTURE || page.phaseEvidenceKind !== 'page-self-report') {
      issues.push('The retained return does not identify the expected page-report envelope. Returned values are unavailable to this view.');
    } else if (page.values !== null) {
      if (Array.isArray(page.values) && page.values.length <= CAP && page.values.every(value => Number.isInteger(value) && !Object.is(value, -0) && value >= 0 && value <= 255)) returned = Uint8Array.from(page.values);
      else issues.push('The retained return has invalid byte values. No coercion or expected-byte substitution was performed.');
    }
  }
  const received = bytes.get('received') ?? null;
  const expected = bytes.get('expected') ?? null;
  const pairs = {
    'returned-file': {name: 'Returned ↔ saved', left: returned, right: received},
    'file-expected': {name: 'Saved ↔ expected', left: received, right: expected},
    'returned-expected': {name: 'Returned ↔ expected', left: returned, right: expected},
  };
  for (const pair of Object.values(pairs)) Object.assign(pair, compare(pair.left, pair.right));
  for (const [name, value] of [['Returned values', returned], ['Saved file', received], ['Expected reference', expected]]) {
    if (value === null) issues.push(name + ' unavailable.');
    else if (value.length !== 128) issues.push(name + ' has ' + value.length + ' bytes; the fixture requires 128. The layout displays offsets 0–127 only.');
  }
  let events = [];
  if (bytes.has('trace')) {
    try {
      const lines = decode(bytes.get('trace')).split('\n').filter(line => line.trim());
      require(lines.length <= 2048, 'Saved trace exceeds the declared event cap.');
      events = lines.map(line => { const item = JSON.parse(line); require(object(item), 'Invalid saved trace item.'); return item; });
    } catch {
      events = [];
      issues.push('The digest-bound saved trace is malformed or exceeds the event cap. Event inspection is unavailable; no replacement events were created.');
    }
  }
  return {records, returned, received, expected, pairs, issues, events};
}
