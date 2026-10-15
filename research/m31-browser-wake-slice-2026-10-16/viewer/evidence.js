// Saved-byte display only. No host model, shader or numerical gate is executed.
export const IDS = Object.freeze([27, 445, 4500, 988]);
export const N = 5000;
export const STATUS = ['unwritten', 'malformed', 'domain invalid', 'early zero', 'evaluated zero', 'positive profile', 'arithmetic invalid'];
export const POLICY = ['self / outside center', 'downstream ≤ 0', 'downstream cutoff', 'near domain invalid', 'near policy skip', 'radial cutoff', 'zero projection', 'positive projection'];
export const FIELDS = ['Center distance', 'Downstream', 'Radial', 'Half width', 'Axis dot', 'Projection', 'Normalized downstream', 'Xi', 'Normalized speed', 'Downstream fade', 'Radial fade', 'Term'];
export const STATUS_COLORS = ['#667788', '#ff667a', '#c88ae6', '#365a78', '#a9c5d6', '#f2b763', '#ff667a'];
export const ordinal = (selection, source, rotor) => (selection * N + source) * 4 + rotor;
const buffers = new Map();
const text = new TextDecoder();
const finite = value => Number.isFinite(value) ? value : null;
export async function checked(spec) {
  if (!spec || typeof spec.url !== 'string' || !Number.isSafeInteger(spec.bytes) || spec.bytes < 0 || !/^[a-f0-9]{64}$/.test(spec.sha256)) throw Error('Invalid evidence descriptor');
  const url = new URL(spec.url, location.href);
  if (url.origin !== location.origin || !['http:', 'https:'].includes(url.protocol)) throw Error('Evidence URL must remain on the published host');
  const key = `${url.href}:${spec.sha256}`;
  if (!buffers.has(key)) buffers.set(key, (async () => {
    const response = await fetch(url, {cache: 'no-store'});
    if (!response.ok) throw Error(`Evidence unavailable: ${spec.label || spec.url}`);
    const bytes = await response.arrayBuffer();
    const hash = Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256', bytes)), x => x.toString(16).padStart(2, '0')).join('');
    if (bytes.byteLength !== spec.bytes || hash !== spec.sha256) throw Error(`Evidence checksum mismatch: ${spec.label || spec.url}`);
    return bytes;
  })());
  return buffers.get(key);
}
export async function checkedJSON(spec) { return JSON.parse(text.decode(await checked(spec))); }
function view(bytes, expected, name) {
  if (bytes.byteLength !== expected) throw Error(`Saved array shape mismatch: ${name}`);
  return new DataView(bytes);
}
function floatArray(bytes, count, name) {
  const values = new Float64Array(count), data = view(bytes, count * 8, name);
  for (let i = 0; i < count; i++) values[i] = data.getFloat64(i * 8, true);
  return values;
}
function samePin(a, b) { return a?.bytes === b?.bytes && a?.sha256 === b?.sha256; }
function verifyReview(meta, review, closure, result, budget) {
  if (meta.reviewContract?.version !== 1 || meta.reviewContract?.bound !== true) throw Error('Independent saved-review contract is not yet bound');
  if (closure.terminal !== true || closure.active !== false || closure.qualifiedReviewClosure !== true) throw Error('Independent saved-review external closure is not qualified');
  if (review.terminal !== true || review.reviewPass !== true) throw Error('Independent saved review has not verified evidence integrity');
  if (!['consistent-recorded-negative', 'consistent-full-pass', 'consistent-incomplete'].includes(review.status)) throw Error('Independent review has no displayable terminal disposition');
  if (review.sourceCommit !== result.sourceCommit || review.freezeSha256 !== meta.files.freeze.sha256) throw Error('Independent review source/freeze identity mismatch');
  if (review.inputIndexSha256 !== meta.reviewContract.inputIndexSha256 || review.checkerSha256 !== meta.reviewContract.checkerSha256) throw Error('Independent review input/checker identity mismatch');
  if (result.terminal !== true || budget.terminal !== true || budget.active !== false) throw Error('Scientific attempt is not terminal');
  // Deliberately do not require fullSuiteQualified/result.pass: a faithfully
  // recorded numerical failure remains valid evidence for the viewer.
}
export async function loadEvidence() {
  const response = await fetch('data.json', {cache: 'no-store'});
  if (!response.ok) throw Error('Viewer manifest unavailable');
  const meta = await response.json();
  if (meta.schemaVersion !== 1 || meta.receiverIds?.join(',') !== IDS.join(',') || meta.nSources !== N) throw Error('Viewer schema/cohort mismatch');
  if (meta.reviewContract?.bound !== true) throw Error('Independent saved-review binding is pending; scientific data remain locked');
  const [review, closure, result, budget, freeze, selection] = await Promise.all(['review', 'reviewClosure', 'result', 'budget', 'freeze', 'selection'].map(key => checkedJSON(meta.files[key])));
  verifyReview(meta, review, closure, result, budget);
  if (result.config?.receiverIds?.join(',') !== IDS.join(',') || selection.selected?.map(x => x.receiverId).join(',') !== IDS.join(',')) throw Error('Saved cohort identity mismatch');
  const sourcePin = freeze.files?.find(item => item.path === meta.files.poses.repoPath);
  if (!samePin(sourcePin, meta.files.poses)) throw Error('Original pose bytes are not bound by the frozen inputs');
  for (const descriptor of Object.values(meta.files)) {
    if (!descriptor?.rawName) continue;
    const original = result.files?.find(item => item.name === descriptor.rawName);
    if (!samePin(original, descriptor)) throw Error(`Original result index mismatch: ${descriptor.rawName}`);
  }
  const loaded = new Map();
  await Promise.all(Object.entries(meta.files).map(async ([key, spec]) => loaded.set(key, await checked(spec))));
  const json = key => loaded.has(key) ? JSON.parse(text.decode(loaded.get(key))) : null;
  const data = {meta, review, closure, result, budget, freeze, selection, reports: {}, references: {}, gpu: null, serial: null, preparedOffsets: null};
  data.poses = floatArray(loaded.get('poses'), N * 17, 'poses');
  for (let i = 0; i < N; i++) for (const k of [0, 1, 2, 6, 7, 8, 9]) {
    if (!Number.isFinite(data.poses[17 * i + k])) throw Error('Non-finite saved display pose');
  }
  for (const stage of ['R', 'Q', 'controls', 'terms', 'serial']) data.reports[stage] = json(`${stage}Report`);
  for (const label of ['R', 'Q']) {
    const descriptor = meta.references[label];
    if (!descriptor) continue;
    const ref = {};
    for (const [key, [bytes, name]] of Object.entries({metadata: [80000 * 32, 'metadata'], scalars: [80000 * 96, 'scalars'], terms: [80000 * 8, 'terms'], sums: [128, 'sums'], validity: [16, 'validity']})) {
      const fileKey = descriptor[key];
      ref[key] = fileKey && loaded.has(fileKey) ? view(loaded.get(fileKey), bytes, `${label} ${name}`) : null;
    }
    ref.counts = descriptor.counts ? json(descriptor.counts) : null;
    data.references[label] = ref;
  }
  if (loaded.has('gpuTerms')) data.gpu = view(loaded.get('gpuTerms'), 6400000, 'GPU terms');
  if (loaded.has('gpuSerial')) data.serial = view(loaded.get('gpuSerial'), 512, 'GPU serial output');
  if (loaded.has('originalOffsets')) data.preparedOffsets = floatArray(loaded.get('originalOffsets'), 64, 'original offsets');
  return data;
}
export function record(data, stage, selection, source, rotor) {
  const n = ordinal(selection, source, rotor), gpu = stage === 'T', ref = data.references[stage], metadata = gpu ? data.gpu : ref?.metadata;
  if (!metadata) return null;
  const base = n * (gpu ? 80 : 32), words = Array.from({length: 8}, (_, k) => metadata.getUint32(base + 4 * k, true));
  const [slot, receiverID, sourceID, rotorID, status, code, mask, flags] = words;
  const identityValid = slot === n && receiverID === IDS[selection] && sourceID === source && rotorID === rotor;
  const scalars = Array.from({length: 12}, (_, k) => {
    if (!(mask & (1 << k))) return null;
    if (gpu) return finite(metadata.getFloat32(base + 32 + 4 * k, true));
    if (k === 11 && ref.terms) return finite(ref.terms.getFloat64(n * 8, true));
    return ref.scalars ? finite(ref.scalars.getFloat64(n * 96 + k * 8, true)) : null;
  });
  const termValid = identityValid && [3, 4, 5].includes(status) && !!(mask & 2048) && scalars[11] !== null && scalars[11] >= 0;
  return {ordinal: n, receiverID, sourceID, rotor: rotorID, status, code, mask, flags, scalars, identityValid, termValid, term: termValid ? scalars[11] : null};
}
export function modes(data) {
  const options = [];
  for (const stage of ['T', 'Q', 'R']) {
    if (stage === 'T' ? data.gpu : data.references[stage]?.metadata) {
      options.push({id: `contribution-${stage}`, label: `${stage} · saved contribution`, kind: 'contribution', stage});
      options.push({id: `status-${stage}`, label: `${stage} · saved record status`, kind: 'status', stage});
    }
  }
  for (const [a, b] of [['T', 'R'], ['T', 'Q'], ['Q', 'R']]) {
    if ((a === 'T' ? data.gpu : data.references[a]?.terms) && data.references[b]?.terms) options.push({id: `error-${a}${b}`, label: `|${a} − ${b}| · saved term difference`, kind: 'error', a, b, stage: a});
  }
  return options;
}
export function metric(data, mode, selection, source, rotor) {
  const a = record(data, mode.stage, selection, source, rotor);
  if (mode.kind === 'status') return {value: a?.status ?? null, record: a};
  if (mode.kind === 'contribution') return {value: a?.term ?? null, record: a};
  const b = record(data, mode.b, selection, source, rotor);
  return {value: a?.term !== null && a?.term !== undefined && b?.term !== null && b?.term !== undefined ? Math.abs(a.term - b.term) : null, record: a};
}
export function savedSum(data, stage, index) {
  if (stage === 'T') {
    if (!data.serial) return {value: null, label: 'Not dispatched'};
    const b = index * 32, status = data.serial.getUint32(b + 12, true), valid = data.serial.getUint32(b + 16, true), count = data.serial.getUint32(b + 20, true);
    const value = status === 2 && (valid & 1) ? finite(data.serial.getFloat32(b + 24, true)) : null;
    return {value, label: status === 2 && value !== null ? `Complete · ${count} terms` : status === 0 ? 'Unwritten' : `Invalid · ${count} accepted prefix terms`};
  }
  const ref = data.references[stage];
  if (!ref?.sums) return {value: null, label: 'Unavailable'};
  const valid = ref.validity?.getUint8(index) === 1, value = finite(ref.sums.getFloat64(index * 8, true));
  return {value, label: valid ? 'Complete' : 'Partial / not qualified', valid};
}
export const certificate = item => Number.isFinite(item?.approximateDisplay) ? item.approximateDisplay : null;
