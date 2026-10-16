'use strict';
// SOURCE PREPARATION ONLY. Do not invoke before the parent freezes and admits
// source, runtime, resources, and the one supervised generation allocation.
// Only Node built-ins are loaded before the runtime-identity gate below.
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const os = require('node:os');

const start = performance.now();
const fixedCases = [
  {id: 'n1000-s261701-t5', n: 1000, seed: 261701, t: 5},
  {id: 'n5000-s261702-t5', n: 5000, seed: 261702, t: 5},
  {id: 'n5000-s261703-t5', n: 5000, seed: 261703, t: 5}
];
const fixedGeneration = {
  duration: 5, dt: 0.0025, mode: 'boids', search: 'grid',
  filter: 'wall-priority', record: true, frameEvery: 0.2,
  factoryVariant: 'wide', expectedCourse: 'factory-v1',
  airflow: 'off', observation: 'ideal'
};
const limits = {
  generationWallSeconds: 900,
  generationCooperativeSeconds: 895,
  rssBytes: 1610612736,
  generationBytes: 67108864,
  normalGenerationBytes: 62914560
};
const ownedResultNames = [
  'generation-child-invocation.lock', 'generation-evidence.json',
  'generation-failure.json', 'generation-partial-evidence.json'
];
const sha = b => crypto.createHash('sha256').update(b).digest('hex');
const bytes = x => Buffer.from(x.buffer, x.byteOffset, x.byteLength);
const stateBuffer = states => bytes(Float64Array.from(states.flat()));
const token = x => Object.is(x, -0) ? '-0' : String(x);
let packageRoot = null;
let lockOwned = false;
let maxRSS = 0;
let progress = {phase: 'invocation-gate'};
const evidence = {
  kind: 'fresh-browser-screen-input-generation',
  complete: false,
  runtimeIdentityVerified: false,
  generation: [],
  inputIndex: null
};

function assert(value, label) {
  if (!value) throw Error('checkpoint: ' + label);
}

function exact(a, b) {
  if (Object.is(a, b)) return true;
  if (!a || !b || typeof a !== 'object' || typeof b !== 'object' ||
      Array.isArray(a) !== Array.isArray(b)) return false;
  const ka = Object.keys(a), kb = Object.keys(b);
  return ka.length === kb.length &&
    ka.every(k => Object.hasOwn(b, k) && exact(a[k], b[k]));
}

function encode(value) {
  if (typeof value === 'number' &&
      (!Number.isFinite(value) || Object.is(value, -0))) return token(value);
  if (Array.isArray(value)) return value.map(encode);
  if (value && typeof value === 'object') {
    return Object.fromEntries(Object.entries(value).map(([k, v]) => [k, encode(v)]));
  }
  return value;
}

function guard() {
  maxRSS = Math.max(maxRSS, process.memoryUsage().rss);
  assert(maxRSS <= limits.rssBytes, 'RSS guard exceeded');
  assert(performance.now() - start <= limits.generationCooperativeSeconds * 1000,
    'internal wall guard exceeded');
}

function directoryBytes(directory) {
  if (!fs.existsSync(directory)) return 0;
  const stat = fs.lstatSync(directory);
  assert(stat.isDirectory(), 'owned output directory must be a real directory');
  let total = 0;
  for (const entry of fs.readdirSync(directory, {withFileTypes: true})) {
    const child = path.join(directory, entry.name);
    const childStat = fs.lstatSync(child);
    assert(childStat.isFile(), 'unexpected non-file in owned output directory');
    total += childStat.size;
  }
  return total;
}

function generationBytes() {
  let total = directoryBytes(path.join(packageRoot, 'inputs')) +
    directoryBytes(path.join(packageRoot, 'generation'));
  for (const name of ownedResultNames) {
    const file = path.join(packageRoot, 'results', name);
    if (!fs.existsSync(file)) continue;
    const stat = fs.lstatSync(file);
    assert(stat.isFile(), 'owned result must be a regular file');
    total += stat.size;
  }
  return total;
}

function write(relative, data, emergency = false) {
  if (!emergency) guard();
  const buffer = typeof data === 'string' ? Buffer.from(data) : data;
  const cap = emergency ? limits.generationBytes : limits.normalGenerationBytes;
  assert(generationBytes() + buffer.length <= cap, 'generation output guard exceeded');
  fs.writeFileSync(path.join(packageRoot, relative), buffer, {flag: 'wx'});
  return {path: relative, bytes: buffer.length, sha256: sha(buffer)};
}

function json(relative, object, emergency = false) {
  return write(relative, JSON.stringify(encode(object)) + '\n', emergency);
}

function stateShape(states, count) {
  return Array.isArray(states) && states.length === count && states.every(
    row => Array.isArray(row) && row.length === 17 && row.every(Number.isFinite));
}

function memory() {
  return {
    sampledPeakRSSBytes: maxRSS,
    processResourceUsage: process.resourceUsage(),
    platformMaxRSSUnits: 'Node maxRSS in kilobytes; sampled RSS in bytes'
  };
}

try {
  assert(process.argv.length === 3, 'argument shape: generate.cjs PACKAGE_ROOT');
  packageRoot = fs.realpathSync(path.resolve(process.argv[2]));
  const resultsPath = path.join(packageRoot, 'results');
  fs.mkdirSync(resultsPath, {recursive: true});
  assert(fs.lstatSync(resultsPath).isDirectory(), 'results must be a real directory');

  // The exclusive lock is never deleted. A second invocation must not alter
  // either a completed result or the first invocation's failure evidence.
  for (const name of ownedResultNames) {
    assert(!fs.existsSync(path.join(resultsPath, name)), 'generation invocation already exists');
  }
  fs.writeFileSync(path.join(resultsPath, 'generation-child-invocation.lock'),
    'single frozen generation invocation; do not replace or retry\n', {flag: 'wx'});
  lockOwned = true;
  for (const dir of ['inputs', 'generation']) {
    const target = path.join(packageRoot, dir);
    fs.mkdirSync(target, {recursive: true});
    assert(fs.lstatSync(target).isDirectory() && fs.readdirSync(target).length === 0,
      'generation output directories must be empty');
  }

  progress = {phase: 'config-and-runtime-gate'};
  guard();
  const configBytes = fs.readFileSync(path.join(packageRoot, 'config.json'));
  const runtimeBytes = fs.readFileSync(path.join(packageRoot, 'runtime.json'));
  const config = JSON.parse(configBytes);
  const runtime = JSON.parse(runtimeBytes);
  assert(config.schema === 'm31-browser-screen-v1', 'frozen configuration schema');
  assert(exact(config.cases, fixedCases), 'fixed generation cases');
  assert(exact(config.generation, fixedGeneration), 'fixed generation configuration');
  for (const [key, value] of Object.entries(limits)) {
    assert(config.limits?.[key] === value, 'fixed generation limit ' + key);
  }
  assert(os.endianness() === 'LE', 'little endian runtime required');
  assert(!process.env.NODE_OPTIONS && process.execArgv.length === 0,
    'runtime options forbidden');
  const nodeBytes = fs.readFileSync(fs.realpathSync(process.execPath));
  assert(nodeBytes.length === runtime.node.bytes && sha(nodeBytes) === runtime.node.sha256 &&
    process.version === runtime.node.version, 'Node runtime identity');
  assert(os.arch() === runtime.architecture && os.platform() === runtime.platform,
    'platform identity');
  guard();
  evidence.runtimeIdentityVerified = true;
  evidence.configurationSha256 = sha(configBytes);
  evidence.runtimeMetadataSha256 = sha(runtimeBytes);
  evidence.runtime = {
    platform: os.platform(), architecture: os.arch(), node: process.version,
    v8: process.versions.v8, nodeExecutableSha256: runtime.node.sha256,
    nodeOptionsEmpty: true, executionFlagCount: 0
  };
  evidence.limits = {...limits};

  // The parent supervisor separately verifies the frozen complete source
  // manifest and publication receipt. This local runtime gate precedes the
  // first scientific import; it does not replace that parent source gate.
  progress = {phase: 'simulator-import'};
  process.env.FLOCK_FACTORY_VARIANT = config.generation.factoryVariant;
  const simulatorPath = path.resolve(packageRoot, '../../outputs/milestone-31-source/sim.cjs');
  const sim = require(simulatorPath);
  const index = {kind: 'fresh-airflow-off-boids-states', shape: ['vehicle', 17],
    dtype: 'float64le', cases: []};

  // Extracted from the completed center-screen generation block. Simulation
  // source, initial-state construction, solver/control order and metric cadence
  // are unchanged. Only fixed seeds, duration and supported pose cadence differ.
  for (const info of config.cases) {
    progress = {phase: 'generation', id: info.id};
    guard();
    const framePins = [], frames = [], g0 = performance.now();
    let initialPin = null;
    const run = sim.run({
      seed: info.seed, count: info.n,
      ...Object.fromEntries(['duration', 'dt', 'mode', 'search', 'filter', 'record',
        'frameEvery'].map(k => [k, config.generation[k]])),
      frameSink(frame) {
        guard();
        const arr = Float64Array.from(frame);
        const pin = write(`generation/${info.id}-frame-${String(frames.length).padStart(3, '0')}.f64`,
          bytes(arr));
        frames.push(arr);
        framePins.push({...pin, t: frame[0]});
        progress = {phase: 'generation', id: info.id, frameCount: frames.length,
          time: frame[0], initial: initialPin, frames: framePins};
      },
      progress(state, states) {
        guard();
        if (state.t === 0 && !initialPin) {
          initialPin = write(`generation/${info.id}-initial.f64`, stateBuffer(states));
          progress.initial = initialPin;
        }
      }
    });
    const generationMs = performance.now() - g0;
    guard();
    const finalPin = write(`inputs/${info.id}.f64`, stateBuffer(run.final));
    const posesPin = write(`generation/${info.id}-poses.f64`, Buffer.concat(frames.map(bytes)));
    const initialMatches = Boolean(initialPin &&
      sha(stateBuffer(run.initial)) === initialPin.sha256);
    const expectedConfig = {
      filter: config.generation.filter, seed: info.seed, count: info.n,
      mode: config.generation.mode, dt: config.generation.dt, duration: info.t,
      search: config.generation.search, course: config.generation.expectedCourse,
      airflow: 'off', observation: 'ideal'
    };
    const expectedTimes = Array.from({length: 26}, (_, i) => i / 5);
    const finalPose = Float64Array.from([info.t,
      ...run.final.flatMap(s => [...s.slice(0, 3), ...s.slice(6, 10)])]);
    const finiteStateShape = stateShape(run.initial, info.n) && stateShape(run.final, info.n);
    const complete = initialMatches && finiteStateShape && exact(run.config, expectedConfig) &&
      run.metrics.end === info.t && run.metrics.stopReason === null && run.metrics.failure === null &&
      exact(run.recording, {cadence: 0.2, streamed: true}) && frames.length === 26 &&
      frames.every((f, i) => f[0] === expectedTimes[i] && f.length === 1 + 7 * info.n &&
        f.every(Number.isFinite)) && bytes(frames.at(-1)).equals(bytes(finalPose));
    const {initial, final, ...rest} = run;
    const record = {
      id: info.id, n: info.n, seed: info.seed, ...rest,
      initial: initialPin, final: finalPin, frames: framePins,
      poses: {...posesPin, frames: frames.length, width: 1 + 7 * info.n},
      generationMs, initialMatches, finiteStateShape, complete
    };
    const meta = json(`generation/${info.id}.json`, record);
    evidence.generation.push({id: info.id, pin: meta, complete, generationMs});
    index.cases.push({...info, ...finalPin, generationPath: meta.path, generationPin: meta});
    assert(complete, 'generation completion mismatch');
  }

  assert(evidence.generation.length === 3 && evidence.generation.every(x => x.complete),
    'completed generation schedule mismatch');
  progress = {phase: 'generation-publication'};
  guard();
  evidence.inputIndex = json('inputs/index.json', index);
  evidence.memory = memory();
  evidence.newGenerationBytesBeforeEvidence = generationBytes();
  evidence.complete = true;
  json('results/generation-evidence.json', evidence);
  console.log(JSON.stringify({complete: true, generation: evidence.generation.length,
    inputIndex: evidence.inputIndex.path}));
} catch (error) {
  evidence.complete = false;
  const message = typeof error.message === 'string' && error.message.startsWith('checkpoint: ')
    ? error.message : 'unexpected generation exception';
  const failure = {message, exceptionClass: error.constructor?.name ?? 'Error',
    progress, completedGeneration: evidence.generation.length};
  // An unowned/repeated invocation never writes into the earlier invocation.
  if (lockOwned) {
    evidence.failure = failure;
    evidence.memory = memory();
    for (const [relative, object] of [
      ['results/generation-failure.json', failure],
      ['results/generation-partial-evidence.json', evidence],
      ['results/generation-evidence.json', evidence]
    ]) {
      try { json(relative, object, true); }
      catch { console.error('generation failure evidence write failed'); }
    }
  }
  process.exitCode = 1;
  console.log(JSON.stringify(encode(failure)));
}
