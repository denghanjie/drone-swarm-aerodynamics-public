// Read saved bytes only. Never import a generator, host model, shader or checker.
import {ADAPTER_READY, verifyPublishedEvidence, projectPublishedReports} from './adapter.js';
export const N = 5000;
export const ARMS = Object.freeze(['A', 'B', 'C']);
export const STAGES = Object.freeze(['R', 'Q0', 'Q1']);
export const STATUS = ['unwritten', 'malformed', 'domain invalid', 'early zero', 'evaluated zero', 'positive profile', 'arithmetic invalid'];
export const POLICY = ['self / outside center', 'downstream ≤ 0', 'downstream cutoff', 'near domain invalid', 'near policy skip', 'radial cutoff', 'zero projection', 'positive projection'];
export const FIELDS = ['Center distance', 'Downstream', 'Radial', 'Half width', 'Axis dot', 'Projection', 'Normalized downstream', 'Xi', 'Normalized speed', 'Downstream fade', 'Radial fade', 'Term', 'Center Δx', 'Center Δy', 'Center Δz', 'Rotor Δx', 'Rotor Δy', 'Rotor Δz'];
export const STATUS_COLORS = ['#667788', '#ff667a', '#c88ae6', '#365a78', '#a9c5d6', '#f2b763', '#ff667a'];
export const ordinal = (selection, source, rotor) => (selection * N + source) * 4 + rotor;
export const certificate = value => Number.isFinite(value?.approximateDisplay) ? value.approximateDisplay : null;
const decoder = new TextDecoder('utf-8', {fatal: true});
const finite = value => Number.isFinite(value) ? value : null;
const pinMatches = (a, b) => a?.bytes === b?.bytes && a?.sha256 === b?.sha256;
const bytesCache = new Map();
export class PendingEvidence extends Error {}
export function evidenceURL(spec) {
  if (!spec || typeof spec.url !== 'string' || !Number.isSafeInteger(spec.bytes) || spec.bytes < 0 || !/^[a-f0-9]{64}$/.test(spec.sha256)) throw Error('Invalid evidence descriptor');
  const url = new URL(spec.url, location.href);
  if (!['http:', 'https:'].includes(url.protocol) || url.origin !== location.origin || url.username || url.password) throw Error('Evidence must use a public same-origin HTTP URL');
  return url;
}
export async function checked(spec) {
  const url = evidenceURL(spec), key = `${url.href}:${spec.sha256}`;
  if (!bytesCache.has(key)) bytesCache.set(key, (async () => {
    const response = await fetch(url, {cache: 'no-store', redirect: 'error'});
    if (!response.ok) throw Error(`Required saved evidence unavailable: ${spec.label || spec.url}`);
    const bytes = await response.arrayBuffer();
    if (bytes.byteLength !== spec.bytes) throw Error(`Evidence length mismatch: ${spec.label || spec.url}`);
    const hash = Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256', bytes)), x => x.toString(16).padStart(2, '0')).join('');
    if (hash !== spec.sha256) throw Error(`Evidence checksum mismatch: ${spec.label || spec.url}`);
    return bytes;
  })());
  return bytesCache.get(key);
}
export async function checkedJSON(spec) { return JSON.parse(decoder.decode(await checked(spec))); }
function view(bytes, length, name) {
  if (!bytes || bytes.byteLength !== length) throw Error(`Saved array shape mismatch: ${name}`);
  return new DataView(bytes);
}
function floatArray(bytes, count, name) {
  const source = view(bytes, count * 8, name), target = new Float64Array(count);
  for (let i = 0; i < count; i++) target[i] = source.getFloat64(i * 8, true);
  return target;
}
function validateManifest(meta) {
  if (meta.schemaVersion !== 1 || meta.nSources !== N || meta.receiverIds?.length !== 4 || new Set(meta.receiverIds).size !== 4 || meta.receiverIds.some(id => !Number.isInteger(id) || id < 0 || id >= N)) throw Error('Saved viewer schema/cohort mismatch');
  if (meta.origins?.length !== 2 || meta.origins.some((origin, i) => origin.id !== i || origin.offset?.length !== 3 || origin.offset.some(x => !Number.isFinite(x)))) throw Error('Saved origin descriptors mismatch');
  if (meta.cells?.length !== 6) throw Error('Manifest must preserve all six declared cells');
  for (let origin = 0; origin < 2; origin++) for (const arm of ARMS) {
    if (meta.cells.filter(cell => cell.origin === origin && cell.arm === arm).length !== 1) throw Error('Duplicated or missing origin/arm cell');
  }
  for (const spec of Object.values(meta.files)) evidenceURL(spec);
}
export async function loadEvidence() {
  const response = await fetch('data.json', {cache: 'no-store', redirect: 'error'});
  if (!response.ok) throw Error('Viewer manifest unavailable');
  const meta = await response.json();
  // The shipped skeleton must stop here: no anchors, arrays or scene import.
  if (!['bound-terminal-evidence', 'bound-unqualified-records'].includes(meta.bindingState) || meta.reviewContract?.bound !== true || ADAPTER_READY !== true) throw new PendingEvidence('Awaiting this campaign’s terminal result, source freeze and independent-review closure. No scientific data are loaded.');
  validateManifest(meta);
  const anchors = ['freeze', 'result', 'budget', 'review', 'reviewClosure', 'reviewInputIndex', 'reviewPrepared'];
  const documents = Object.fromEntries(await Promise.all(anchors.map(async key => [key, await checkedJSON(meta.files[key])])));
  const verification = await verifyPublishedEvidence({meta, documents});
  if (verification?.byteBindingsVerified !== true) throw Error('Saved evidence byte bindings are not verified');
  // Original raw/source indexes are checked independently of the report projection.
  for (const [key, spec] of Object.entries(meta.files)) {
    if (spec.rawName && !pinMatches(documents.result.files?.find(file => file.name === spec.rawName), spec)) throw Error(`Original raw index mismatch: ${key}`);
    if (spec.repoPath && !pinMatches(documents.freeze.files?.find(file => file.path === spec.repoPath), spec)) throw Error(`Source freeze mismatch: ${key}`);
    if (!pinMatches(verification.boundFiles?.[key], spec)) throw Error(`Review/source binding absent: ${key}`);
  }
  for (const [key, spec] of Object.entries(meta.files)) {
    if (spec.format === 'json' && !Object.hasOwn(documents, key)) documents[key] = await checkedJSON(spec);
    else if (spec.format === 'text') await checked(spec);
  }
  const reports = await projectPublishedReports({meta, documents, verification});
  if (!reports?.campaign || !Array.isArray(reports.cells) || reports.cells.length !== 6) throw Error('Incomplete saved-report mapping');
  for (const cell of meta.cells) {
    const mapped = reports.cells.filter(item => item.origin === cell.origin && item.arm === cell.arm);
    if (mapped.length !== 1 || mapped[0].matchedReference !== (cell.arm === 'C' ? 'Q1' : 'Q0')) throw Error('Saved cell/reference mapping mismatch');
    for (const stage of ['terms', 'serial']) {
      const availability = mapped[0].availability?.[stage];
      if (!availability || typeof availability.retained !== 'boolean' || typeof availability.label !== 'string' || availability.retained !== Boolean(cell[stage])) throw Error(`Saved stage availability mismatch: o${cell.origin}-${cell.arm}/${stage}`);
    }
  }
  const evidence = {meta, documents, reports, verification, originCache: new Map()};
  // Actual generated IDs must agree with the hash-bound manifest and reviewed config.
  const ids = view(await checked(meta.files[meta.receiverIdsFile]), 16, 'generated receiver IDs');
  if (meta.receiverIds.some((id, i) => ids.getUint32(i * 4, true) !== id)) throw Error('Generated receiver ID array mismatch');
  return evidence;
}
export async function loadOrigin(evidence, originID) {
  if (!evidence.originCache.has(originID)) evidence.originCache.set(originID, (async () => {
    const spec = evidence.meta.origins.find(origin => origin.id === originID);
    if (!spec) throw Error('Unknown saved origin');
    const load = key => key == null ? Promise.resolve(null) : checked(evidence.meta.files[key]);
    const frame = {id: originID, origin: spec.offset.slice(), receiverIds: evidence.meta.receiverIds, poses: null, preparedOffsets: null, references: {}, cells: {}};
    if (spec.poses) {
      frame.poses = floatArray(await load(spec.poses), N * 17, 'original saved poses');
      for (let id = 0; id < N; id++) for (const k of [0, 1, 2, 6, 7, 8, 9]) if (!Number.isFinite(frame.poses[17 * id + k])) throw Error('Non-finite saved display pose');
    }
    if (spec.preparedOffsets) frame.preparedOffsets = floatArray(await load(spec.preparedOffsets), 64, 'prepared original offsets');
    for (const stage of STAGES) {
      const refSpec = spec.references?.[stage];
      if (!refSpec) continue;
      const ref = {};
      for (const [field, length] of Object.entries({metadata: 80000 * 32, scalars: 80000 * 144, terms: 80000 * 8, sums: 128, compensatedSums: 128, validity: 16})) {
        ref[field] = refSpec[field] ? view(await load(refSpec[field]), length, `${stage}/${field}`) : null;
      }
      ref.counts = refSpec.counts ? evidence.documents[refSpec.counts] : null;
      frame.references[stage] = ref;
    }
    for (const arm of ARMS) {
      const cell = evidence.meta.cells.find(item => item.origin === originID && item.arm === arm);
      frame.cells[arm] = {gpu: cell.terms ? view(await load(cell.terms), 80000 * 104, `${arm}/terms`) : null, serial: cell.serial ? view(await load(cell.serial), 512, `${arm}/serial`) : null};
    }
    return frame;
  })());
  return evidence.originCache.get(originID);
}
export function record(frame, stage, selection, source, rotor, details = true) {
  if (!Number.isInteger(selection) || selection < 0 || selection > 3 || !Number.isInteger(source) || source < 0 || source >= N || !Number.isInteger(rotor) || rotor < 0 || rotor > 3) throw Error('Record selection outside saved array');
  const n = ordinal(selection, source, rotor), gpu = stage.startsWith('T:'), ref = frame.references[stage], metadata = gpu ? frame.cells[stage.slice(2)]?.gpu : ref?.metadata;
  if (!metadata) return null;
  const base = n * (gpu ? 104 : 32), words = Array.from({length: 8}, (_, k) => metadata.getUint32(base + 4 * k, true));
  const [slot, receiverID, sourceID, rotorID, status, code, mask, flags] = words;
  const identityValid = slot === n && receiverID === frame.receiverIds[selection] && sourceID === source && rotorID === rotor;
  const reached = Array.from({length: 18}, (_, k) => Boolean(mask & (1 << k)));
  const scalarBits = details ? Array.from({length: 18}, (_, k) => gpu ? `0x${metadata.getUint32(base + 32 + 4 * k, true).toString(16).padStart(8, '0')}` : k === 11 && ref?.terms ? `0x${ref.terms.getBigUint64(n * 8, true).toString(16).padStart(16, '0')}` : ref?.scalars ? `0x${ref.scalars.getBigUint64(n * 144 + k * 8, true).toString(16).padStart(16, '0')}` : null) : [];
  const scalars = Array.from({length: 18}, (_, k) => {
    if ((!details && k !== 11) || !identityValid || !reached[k]) return null;
    if (gpu) return finite(metadata.getFloat32(base + 32 + 4 * k, true));
    if (k === 11 && ref.terms) return finite(ref.terms.getFloat64(n * 8, true));
    return ref.scalars ? finite(ref.scalars.getFloat64(n * 144 + k * 8, true)) : null;
  });
  const termValid = identityValid && [3, 4, 5].includes(status) && reached[11] && scalars[11] !== null && scalars[11] >= 0;
  return {ordinal: n, receiverID, sourceID, rotor: rotorID, status, code, mask, flags, scalars, scalarBits, reached, identityValid, termValid, term: termValid ? scalars[11] : null};
}
export function modes(arm) {
  const options = [];
  for (const stage of [`T:${arm}`, ...STAGES]) {
    options.push({id: `contribution-${stage}`, label: `${stage} · saved contribution`, kind: 'contribution', stage});
    options.push({id: `status-${stage}`, label: `${stage} · saved record status`, kind: 'status', stage});
  }
  for (const [a, b] of [[`T:${arm}`, 'R'], [`T:${arm}`, arm === 'C' ? 'Q1' : 'Q0'], ['Q1', 'Q0']]) options.push({id: `error-${a}-${b}`, label: `|${a} − ${b}| · saved term difference`, kind: 'error', stage: a, b});
  return options;
}
export function metric(frame, mode, selection, source, rotor) {
  const a = record(frame, mode.stage, selection, source, rotor, false);
  if (mode.kind === 'status') return {value: a?.status ?? null, record: a};
  if (mode.kind === 'contribution') return {value: a?.term ?? null, record: a};
  const b = record(frame, mode.b, selection, source, rotor, false);
  return {value: a?.term != null && b?.term != null ? Math.abs(a.term - b.term) : null, record: a};
}
export function savedSum(frame, stage, index, absentLabel = 'Not retained') {
  if (!Number.isInteger(index) || index < 0 || index >= 16) throw Error('Sum row outside saved array');
  if (stage.startsWith('T:')) {
    const serial = frame.cells[stage.slice(2)]?.serial;
    if (!serial) return {value: null, label: absentLabel, valid: false};
    const base = index * 32, words = Array.from({length: 8}, (_, k) => serial.getUint32(base + 4 * k, true));
    const [selection, receiver, rotor, status, mask, count, sumBits, firstBadSlot] = words;
    const identityValid = selection === Math.floor(index / 4) && receiver === frame.receiverIds[selection] && rotor === index % 4;
    const valid = identityValid && status === 2 && mask === 1 && count === N && firstBadSlot === 0xffffffff;
    const value = valid ? finite(serial.getFloat32(base + 24, true)) : null;
    return {value, valid: valid && value !== null, sumBits, firstBadSlot, label: !identityValid ? 'Invalid record identity' : status === 0 ? 'Unwritten' : valid && value !== null ? `Complete · ${count} terms` : `Invalid · ${count} accepted prefix terms`};
  }
  const ref = frame.references[stage];
  if (!ref?.sums || !ref.validity) return {value: null, label: 'Not retained', valid: false};
  const valid = ref.validity.getUint8(index) === 1, value = finite(ref.sums.getFloat64(index * 8, true));
  return {value: valid ? value : null, rawValue: value, valid: valid && value !== null, label: valid && value !== null ? 'Complete' : 'Partial / not qualified'};
}
