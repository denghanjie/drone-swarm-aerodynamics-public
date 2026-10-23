'use strict';

// Source-only draft. Loading/executing this module requires the parent's
// separately frozen source approval and execution allocation.
const K = require('./candidate-kernel.cjs');
const MAX_N = 5000;
const POSITIVE_TERM_CAP = 2000000;
const RESIDUAL_LOG_LIMIT = 1e-9;
const SOURCE_RECEIVER_LIMIT = 2e-9;
const {mg, arm, radius, rho, A, R, c} = K.constants;
const CONSTANTS = Object.freeze({mg, arm, radius, rho, A, R,
  D: c.D, decay: c.decay, spread: c.spread, origin: c.origin,
  minDown: c.minDown, neighbor: c.neighbor, nearRad: c.nearRad,
  downFade: c.downFade, downCut: c.downCut, radFade: c.radFade,
  radCut: c.radCut, induced: c.induced, kappa: c.sqrt2minus1});

class Refusal extends Error {
  constructor(status, reason) { super(reason); this.status = status; this.reason = reason; }
}
function need(ok, status, reason) { if (!ok) throw new Refusal(status, reason); }
function finite(value) { return typeof value === 'number' && Number.isFinite(value); }
function positive(value) { return finite(value) && value > 0; }
function dataProperty(object, name) {
  const property = Object.getOwnPropertyDescriptor(object, name);
  need(property && Object.hasOwn(property, 'value'), 'input-refused', 'accessor-or-missing-property');
  return property.value;
}
function record(object, names) {
  need(object !== null && typeof object === 'object' && !Array.isArray(object),
    'input-refused', 'record-shape');
  const prototype = Object.getPrototypeOf(object);
  need(prototype === Object.prototype || prototype === null, 'input-refused', 'record-prototype');
  const keys = Reflect.ownKeys(object);
  need(keys.length === names.length && names.every(name => keys.includes(name)),
    'input-refused', 'record-fields');
  for (const name of names) dataProperty(object, name);
}
function dense(array, expected, limit) {
  need(Array.isArray(array) && Object.getPrototypeOf(array) === Array.prototype,
    'input-refused', 'array-type');
  const length = dataProperty(array, 'length');
  need(Number.isSafeInteger(length) && length >= 0,
    'input-refused', 'array-length');
  if (limit !== undefined) need(length <= limit, 'resource-failure', 'drone-count-limit');
  if (expected !== undefined) need(length === expected, 'input-refused', 'array-length');
  need(Reflect.ownKeys(array).length === length + 1, 'input-refused', 'array-extra-or-missing-property');
  for (let i = 0; i < length; i++) dataProperty(array, String(i));
  return length;
}
function captureInput(input, poll) {
  record(input, ['drones']);
  const drones = dataProperty(input, 'drones');
  const n = dense(drones, undefined, MAX_N);
  need(n > 0, 'input-refused', 'empty-input');
  const copied = [], seen = new Set();
  for (let i = 0; i < n; i++) {
    poll();
    const item = dataProperty(drones, String(i)); record(item, ['id', 'state']);
    const id = dataProperty(item, 'id'), state = dataProperty(item, 'state');
    need(Number.isSafeInteger(id) && id >= 0 && !Object.is(id, -0),
      'input-refused', 'id-domain');
    need(!seen.has(id), 'input-refused', 'duplicate-id'); seen.add(id);
    dense(state, 17);
    const owned = new Array(17);
    for (let k = 0; k < 17; k++) {
      const value = dataProperty(state, String(k));
      need(finite(value), 'input-refused', 'raw-nonfinite'); owned[k] = value;
    }
    let total = 0;
    for (let r = 0; r < 4; r++) {
      const force = owned[13 + r];
      need(force > 0, 'input-refused', 'nominal-nonpositive'); total += force;
      const denominator = force / (2 * rho * A), nu = Math.sqrt(denominator);
      need(positive(denominator) && positive(nu), 'numerical-failure', 'normalizer-range');
    }
    need(positive(total), 'numerical-failure', 'nominal-total-range');
    const beta = Math.sqrt(total / mg);
    need(positive(beta), 'numerical-failure', 'source-scale-range');
    copied.push({id, state: owned});
  }
  copied.sort((a, b) => a.id - b.id);
  return copied;
}
function validateBuild(q, n, poll) {
  need(q.n === n && q.S0.length === n && q.nominal.length === n,
    'internal-failure', 'builder-shape');
  need(q.offsets.length === 4 * n + 1 && q.src.length === q.kv.length &&
    q.aa !== null && q.aa.length === q.kv.length,
    'internal-failure', 'coefficient-shape');
  need(q.kv.length <= POSITIVE_TERM_CAP, 'resource-failure', 'positive-term-limit');
  need(q.offsets[0] === 0 && q.offsets[4 * n] === q.kv.length,
    'internal-failure', 'coefficient-offsets');
  for (let i = 0; i < n; i++) {
    need(positive(q.S0[i]), 'numerical-failure', 'prepared-total-range');
    need(q.nominal[i].length === 4 && q.nominal[i].every(positive),
      'numerical-failure', 'prepared-force-range');
  }
  for (let row = 0; row < 4 * n; row++) {
    poll();
    const start = q.offsets[row], end = q.offsets[row + 1];
    need(start <= end && end <= q.kv.length, 'internal-failure', 'coefficient-offsets');
    let previous = -1;
    for (let z = start; z < end; z++) {
      const source = q.src[z];
      need(source < n && source !== Math.floor(row / 4) && source > previous,
        'internal-failure', 'source-order'); previous = source;
      need(positive(q.kv[z]) && positive(q.aa[z]),
        'numerical-failure', 'coefficient-range');
    }
  }
  need(q.admission.admitted, 'domain-refused', 'native-admission');
  need(q.graph.descendingEligible, 'domain-refused', 'native-graph-order');
}
function validateMap(value, q, label, poll) {
  const n = q.n;
  need(value.y.length === n && value.rotors.length === n,
    'internal-failure', label + '-shape');
  for (let i = 0; i < n; i++) {
    poll();
    need(positive(value.y[i]) && value.y[i] <= 1,
      'numerical-failure', label + '-y-range');
    need(value.rotors[i].length === 4, 'internal-failure', label + '-rotor-shape');
    for (let r = 0; r < 4; r++) {
      const rotor = value.rotors[i][r];
      need(finite(rotor.alpha) && rotor.alpha >= 0,
        'numerical-failure', label + '-alpha-range');
      need(positive(rotor.x) && rotor.x <= 1,
        'numerical-failure', label + '-x-range');
      need(positive(rotor.T) && rotor.T <= q.nominal[i][r],
        'numerical-failure', label + '-force-range');
    }
  }
}
function cross(a, b) {
  return [a[1] * b[2] - a[2] * b[1],
    a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]];
}
function prepareEvidence(raw, q, poll) {
  const prepared = [];
  for (let i = 0; i < raw.length; i++) {
    poll();
    const id = raw[i].id, base = 28 * i;
    const center = Array.from(q.p.subarray(base, base + 3));
    const axis = Array.from(q.p.subarray(base + 4, base + 7));
    const offsets = [], points = [], nu = [];
    for (let r = 0; r < 4; r++) {
      const start = base + 8 + 4 * r;
      const offset = Array.from(q.p.subarray(start, start + 3)); offsets.push(offset);
      points.push(center.map((value, k) => value + offset[k]));
      nu.push(Math.sqrt(q.nominal[i][r] / (2 * rho * A)));
    }
    prepared.push({id, center, axis, offsets, points, forces: q.nominal[i].slice(),
      nativeTotal: q.S0[i], nativeBeta: Math.sqrt(q.S0[i] / mg), nativeNu: nu});
  }
  return prepared;
}
function materializeLoads(raw, prepared, solution, poll) {
  const loads = [], solved = [];
  for (let i = 0; i < raw.length; i++) {
    poll();
    const {id, center, axis, offsets, points, nativeNu} = prepared[i];
    const rotor = []; let collective = 0; const worldMoment = [0, 0, 0];
    for (let r = 0; r < 4; r++) {
      // T is the actual native product produced by the unchanged nodeMap.
      const force = solution.rotors[i][r].T; rotor.push(force); collective += force;
      const lever = cross(offsets[r], axis);
      for (let k = 0; k < 3; k++) worldMoment[k] += lever[k] * force;
    }
    const worldForce = axis.map(value => value * collective);
    need([...center, ...axis, ...offsets.flat(), ...points.flat()].every(finite),
      'numerical-failure', 'prepared-geometry-range');
    need(nativeNu.every(positive) && positive(collective) &&
      [...rotor, ...worldForce, ...worldMoment].every(finite),
      'numerical-failure', 'delivered-load-range');
    loads.push({id, rotor, collective, worldForce, worldMoment});
    solved.push({id, y: solution.y[i], rotors: solution.rotors[i]});
  }
  return {loads, solution: solved};
}
function consumeLoads(loads, poll) {
  // Consume every delivered output word without a floating sum that could
  // overflow on otherwise finite loads. This is a checksum, not an audit hash.
  const scratch = new DataView(new ArrayBuffer(8));
  let hash = 2166136261, loadWords = 0, identityWords = 0;
  const status = 'native-success';
  for (let i = 0; i < status.length; i++) hash = Math.imul(hash ^ status.charCodeAt(i), 16777619) >>> 0;
  function word(value) {
    scratch.setFloat64(0, value, false);
    hash = Math.imul(hash ^ scratch.getUint32(0, false), 16777619) >>> 0;
    hash = Math.imul(hash ^ scratch.getUint32(4, false), 16777619) >>> 0;
  }
  for (const load of loads) {
    poll();
    // Every safe-integer ID has an exact binary64 encoding. Mix it before its
    // associated load words so changing the ID association changes this input.
    word(load.id); identityWords++;
    const values = [...load.rotor, load.collective, ...load.worldForce, ...load.worldMoment];
    for (const value of values) {
      word(value); loadWords++;
    }
  }
  return {kind: 'native-load-id-status-fnv32', status, loadWords, identityWords,
    statusCharacters: status.length, value: hash};
}
function query(input, method = 'F', guard = () => {}) {
  const begin = performance.now(), phasesMs = {}; let phaseStart = begin;
  let raw = null, q = null, prepared = null, solution = null, output = null, stage = 'input';
  function phase(name) { const now = performance.now(); phasesMs[name] = now - phaseStart; phaseStart = now; }
  function poll() {
    try { guard(); } catch (_) { throw new Refusal('resource-failure', 'cooperative-guard'); }
  }
  const base = {schema: 'm31-native-load-result-v1',
    model: 'ordinary-binary64-full-contribution', method: typeof method === 'string' ? method : null,
    status: null, reason: null, constants: CONSTANTS};
  try {
    need(method === 'F' || method === 'L', 'input-refused', 'method');
    need(typeof guard === 'function', 'input-refused', 'guard-type'); poll();
    raw = captureInput(input, poll); phase('input'); stage = 'build';
    const states = raw.map(item => item.state);
    q = K.build(states, method === 'F' ? 'screen' : 'lean', false, poll);
    prepared = prepareEvidence(raw, q, poll);
    validateBuild(q, raw.length, poll); phase('buildAndAdmission'); stage = 'schedule';
    const order = K.schedule(q); phase('schedule'); stage = 'solve';
    solution = K.solve(q, 'O', order, false, poll); validateMap(solution, q, 'solution', poll);
    phase('solve'); stage = 'residual';
    const residual = K.residual(q, solution, poll);
    validateMap(residual.residualMap, q, 'residual', poll);
    need(finite(residual.residualLog) && residual.residualLog >= 0 &&
      finite(residual.sourceReceiverMismatch) && residual.sourceReceiverMismatch >= 0,
      'numerical-failure', 'residual-range');
    need(residual.residualLog <= RESIDUAL_LOG_LIMIT &&
      residual.sourceReceiverMismatch <= SOURCE_RECEIVER_LIMIT,
      'numerical-failure', 'residual-limit');
    phase('residual'); stage = 'loads';
    const delivered = materializeLoads(raw, prepared, solution, poll); phase('loads');
    stage = 'consumption'; const consumption = consumeLoads(delivered.loads, poll); phase('consumption');
    output = {...base, status: 'native-success', raw, ids: raw.map(item => item.id),
      prepared, ...delivered, coefficients: {offsets: q.offsets, sourceIndices: q.src, K: q.kv, a: q.aa},
      diagnostics: {admission: q.admission, input: q.input, graph: q.graph,
        symbolCounts: q.symbolCounts, screen: q.screen ?? null,
        geometryWork: q.geometryWork, buildPhasesMs: q.phasesMs,
        ordinaryLmax: q.ordinaryLmax, scheduleIndices: order,
        solveWork: solution.work, residualWork: residual.residualWork,
        residualLog: residual.residualLog, sourceReceiverMismatch: residual.sourceReceiverMismatch},
      consumption};
  } catch (error) {
    let status = 'internal-failure', reason = 'unexpected-exception';
    if (error instanceof Refusal) { status = error.status; reason = error.reason; }
    else if (error instanceof Error && error.message === 'positive coefficient guard exceeded') {
      status = 'resource-failure'; reason = 'positive-term-limit';
    } else if (error instanceof Error && error.message === 'invalid alpha') {
      status = 'numerical-failure'; reason = 'native-alpha-range';
    } else if (error instanceof RangeError) { status = 'resource-failure'; reason = 'native-range-error'; }
    output = {...base, status, reason, stage, raw, prepared,
      coefficients: q ? {offsets: q.offsets, sourceIndices: q.src, K: q.kv, a: q.aa} : null,
      ids: raw ? raw.map(item => item.id) : null,
      diagnostics: q ? {admission: q.admission, input: q.input, graph: q.graph,
        symbolCounts: q.symbolCounts, screen: q.screen ?? null, geometryWork: q.geometryWork} : null};
  }
  // This timestamp follows final result assembly and all required output work.
  const end = performance.now();
  phasesMs.finalization = end - phaseStart;
  output.timing = {clock: 'performance.now', totalMs: end - begin, phasesMs,
    boundary: 'raw current input through validation, copying, canonical ID order, native build/admission, ordered solve, residual, four loads, evidence fields and complete load-word/ID/status consumption'};
  return output;
}

function encodeEvidence(result) {
  // Explicitly outside query timing. No reference/oracle input is accepted.
  const scratch = new DataView(new ArrayBuffer(8));
  function word(value) {
    if (typeof value !== 'number') throw new TypeError('word requires number');
    scratch.setFloat64(0, value, false);
    return scratch.getUint32(0, false).toString(16).padStart(8, '0') +
      scratch.getUint32(4, false).toString(16).padStart(8, '0');
  }
  const vector = values => Array.from(values, word);
  function safe(value) {
    if (typeof value === 'number') return Number.isFinite(value) ? value : {nonfiniteWord: word(value)};
    if (Array.isArray(value)) return value.map(safe);
    if (value !== null && typeof value === 'object') return Object.fromEntries(Object.entries(value).map(([key, item]) => [key, safe(item)]));
    return value;
  }
  const out = {schema: 'm31-native-load-evidence-v1', model: result.model,
    status: result.status, reason: result.reason, method: result.method, ids: result.ids,
    constants: Object.fromEntries(Object.entries(result.constants).map(([key, value]) => [key, word(value)])),
    raw: result.raw ? result.raw.map(item => ({id: item.id, state: vector(item.state)})) : null,
    diagnostics: safe(result.diagnostics), timing: safe(result.timing)};
  out.prepared = result.prepared ? result.prepared.map(item => ({id: item.id, center: vector(item.center),
    axis: vector(item.axis), offsets: item.offsets.map(vector), points: item.points.map(vector),
    forces: vector(item.forces), nativeTotal: word(item.nativeTotal),
    nativeBeta: word(item.nativeBeta), nativeNu: vector(item.nativeNu)})) : null;
  out.coefficients = result.coefficients ? {offsets: Array.from(result.coefficients.offsets),
    sourceIndices: Array.from(result.coefficients.sourceIndices),
    K: vector(result.coefficients.K), a: result.coefficients.a ? vector(result.coefficients.a) : null} : null;
  if (result.status !== 'native-success') { out.stage = result.stage; return out; }
  out.solution = result.solution.map(item => ({id: item.id, y: word(item.y),
    rotors: item.rotors.map(rotor => ({alpha: word(rotor.alpha), x: word(rotor.x), T: word(rotor.T)}))}));
  out.loads = result.loads.map(item => ({id: item.id, rotor: vector(item.rotor),
    collective: word(item.collective), worldForce: vector(item.worldForce), worldMoment: vector(item.worldMoment)}));
  out.consumption = result.consumption;
  return out;
}

module.exports = {query, encodeEvidence, limits: Object.freeze({maxN: MAX_N,
  positiveTermCap: POSITIVE_TERM_CAP, residualLogLimit: RESIDUAL_LOG_LIMIT,
  sourceReceiverLimit: SOURCE_RECEIVER_LIMIT})};
