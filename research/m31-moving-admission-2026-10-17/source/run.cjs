'use strict';
// Sole supervised allocation. Development validation is syntax-only: do not import this file.
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const origin = process.hrtime.bigint();
const MiB = 1024 * 1024;
const packageRoot = path.resolve(process.argv[2] || '.');
const root = path.resolve(packageRoot, '../..');
const packageRelative = path.relative(root, packageRoot).split(path.sep).join('/');
const resultRoot = path.join(packageRoot, 'results');
const generatorEntry = 'outputs/milestone-31-source/sim.cjs';
const generatorFiles = [generatorEntry, 'outputs/milestone-31-source/grid.cjs',
  'outputs/milestone-31-source/geometry.cjs', 'outputs/milestone-31-source/factory.cjs',
  'outputs/milestone-31-source/factory-wide.cjs', 'outputs/milestone-31-source/wall-filter.cjs',
  'outputs/step02c-source/physics.cjs'];
const scientificFiles = ['methods.cjs', 'adapter.cjs', 'canonical.cjs', 'rational.cjs',
  'interval.cjs', 'boxes.cjs', 'tree.cjs', 'pair-prepared.cjs', 'loads.cjs',
  'zero-filter.cjs', 'binary64-interval.cjs', 'spec.json'];
const sourceFiles = [...scientificFiles, 'run.cjs', 'config.json']
  .map(p => packageRelative + '/source/' + p).concat(generatorFiles);
const scheduledIds = ['run-a-t0', 'run-a-t5', 'run-a-t10', 'run-b-t0', 'run-b-t5', 'run-b-t10'];
const sha = bytes => crypto.createHash('sha256').update(bytes).digest('hex');
const assert = (condition, message) => { if (!condition) throw Error(message); };
const json = p => JSON.parse(fs.readFileSync(p, 'utf8'));
const relative = p => path.relative(root, p).split(path.sep).join('/');
const same = (a, b) => encode(a) === encode(b);

// This general record encoder deliberately does not reuse the integer-only input encoder.
function encode(value) {
  if (value === null) return 'null';
  if (typeof value === 'string' || typeof value === 'boolean') return JSON.stringify(value);
  if (typeof value === 'number') {
    assert(Number.isFinite(value) && !Object.is(value, -0), 'Unencoded diagnostic number');
    return JSON.stringify(value);
  }
  if (Array.isArray(value)) {
    assert(Object.keys(value).length === value.length && Object.keys(value).every((k, i) => k === String(i)), 'Sparse record array');
    return '[' + value.map(encode).join(',') + ']';
  }
  assert(value && typeof value === 'object' && [Object.prototype, null].includes(Object.getPrototypeOf(value)), 'Non-JSON record value');
  return '{' + Object.keys(value).sort().map(k => JSON.stringify(k) + ':' + encode(value[k])).join(',') + '}';
}
function diagnostic(value) {
  if (value === undefined) return {undefined: true};
  if (typeof value === 'number') {
    if (Object.is(value, -0)) return {negativeZero: true};
    if (!Number.isFinite(value)) return {nonfinite: Number.isNaN(value) ? 'nan' : value > 0 ? '+infinity' : '-infinity'};
    return value;
  }
  if (value === null || typeof value === 'string' || typeof value === 'boolean') return value;
  if (Array.isArray(value)) return value.map(diagnostic);
  assert(value && Object.getPrototypeOf(value) === Object.prototype, 'Non-JSON simulator diagnostic');
  return Object.fromEntries(Object.entries(value).map(([k, v]) => [k, diagnostic(v)]));
}
function errorValue(error) {
  let message = String(error && error.message || error).slice(0, 4096);
  for (const [prefix, label] of [[packageRoot, 'PACKAGE'], [root, 'REPOSITORY'], [process.execPath, 'NODE_EXECUTABLE']]) message = message.split(prefix).join(label);
  return {name: String(error && error.name || 'Error').slice(0, 128), message};
}
function fsyncDirectory(directory) {
  const fd = fs.openSync(directory, 'r');
  try { fs.fsyncSync(fd); } finally { fs.closeSync(fd); }
}
function checkRegular(p) {
  assert(fs.lstatSync(p).isFile(), 'Pinned path is not a regular file: ' + relative(p));
  assert(fs.realpathSync(p) === path.resolve(p), 'Pinned path crosses a symlink: ' + relative(p));
}
function pin(p) {
  checkRegular(p);
  const bytes = fs.readFileSync(p);
  return {path: relative(p), bytes: bytes.length, sha256: sha(bytes)};
}

let config, configBytes, manifestBytes, manifestPath, manifest, receipt, attempt, runtime;
let identity, sourceSha256, constants = null, M, A, C, simulator;
let journalFd = null, journalBytes = 0, scientificBytes = 0, eventSequence = 0;
let methodCalls = 0, generationRuns = 0, stage = 'initialization';
const controls = [], generations = [], generationRecords = [];
const scheduled = scheduledIds.map((id, i) => ({id, runId: i < 3 ? 'run-a' : 'run-b', t: [0, 5, 10][i % 3],
  status: 'not-generated', reason: 'kernel-not-completed', generationSha256: null, inputSha256: null, record: null}));

function verifyManifest() {
  assert(same(pin(manifestPath), {path: relative(manifestPath), bytes: manifestBytes.length, sha256: sha(manifestBytes)}), 'Source manifest changed');
  for (const entry of manifest.files) {
    assert(same(pin(path.join(root, entry.path)), entry), 'Source pin mismatch: ' + entry.path);
  }
  const executable = pin(process.execPath);
  assert(executable.sha256 === runtime.executableSha256, 'Runtime executable changed');
  assert(same(json(path.join(packageRoot, 'source-publication.json')), receipt), 'Publication receipt changed');
  assert(same(json(path.join(resultRoot, 'kernel-attempt.json')), attempt), 'Supervisor attempt changed');
}
function preflight() {
  assert(process.argv.length === 3 && packageRoot === path.resolve(__dirname, '..'), 'Exactly this package root is required');
  assert(packageRelative === 'research/m31-moving-admission-2026-10-17', 'Wrong package allocation');
  assert(process.env.RESEARCH_SUPERVISION_STAGE === 'kernel', 'Kernel supervision required');
  assert(!process.env.NODE_OPTIONS && !process.env.NODE_PATH, 'Node preloads/search overrides are forbidden');
  configBytes = fs.readFileSync(path.join(__dirname, 'config.json'));
  config = JSON.parse(configBytes);
  assert(config.id === 'm31-moving-admission-v1' && config.method === 'filtered', 'Wrong frozen method/config');
  assert(same(config.cases, [{id: 'run-a', seed: 26171001}, {id: 'run-b', seed: 26171002}]), 'Wrong fixed cases');
  assert(same(config.scheduledTimes, [0, 5, 10]), 'Wrong fixed schedule');
  assert(same(config.generation, {count: 64, duration: 10, dt: 0.0025, mode: 'boids', search: 'grid', filter: 'wall-priority', record: true, frameEvery: 0.2, factoryVariant: 'wide', airflow: 'off', observation: 'ideal'}), 'Wrong generation configuration');
  assert(same(config.controls.map(c => c.id), ['positive', 'distant-zero', 'raw-force', 'order-incompatible']), 'Wrong fixed controls');
  for (const [key, expected] of Object.entries({kernelSeconds: 600, rssBytes: 1024 * MiB, kernelOutputBytes: 192 * MiB,
    sceneBytes: 32 * MiB, generationBytesPerRun: 8 * MiB, indexBytes: 2 * MiB, journalBytes: 4 * MiB})) assert(config.limits[key] === expected, 'Wrong resource cap: ' + key);
  assert(config.launchCutoffUtc === '2026-10-16T23:00:00Z' && Date.now() < Date.parse(config.launchCutoffUtc), 'Launch cutoff reached');
  manifestPath = path.resolve(process.env.RESEARCH_SOURCE_MANIFEST_PATH || '');
  assert(manifestPath.startsWith(root + path.sep), 'Manifest must belong to repository');
  checkRegular(manifestPath);
  manifestBytes = fs.readFileSync(manifestPath);
  assert(/^[0-9a-f]{64}$/.test(process.env.RESEARCH_EXPECTED_MANIFEST_SHA256 || '') && sha(manifestBytes) === process.env.RESEARCH_EXPECTED_MANIFEST_SHA256, 'Manifest environment pin mismatch');
  manifest = JSON.parse(manifestBytes);
  assert(Array.isArray(manifest.files) && manifest.files.length > 0, 'Manifest files required');
  const paths = new Set();
  for (const entry of manifest.files) {
    assert(same(Object.keys(entry).sort(), ['bytes', 'path', 'sha256']), 'Invalid manifest pin shape');
    assert(typeof entry.path === 'string' && entry.path !== '' && !path.isAbsolute(entry.path) && !entry.path.includes('\\') && entry.path.split('/').every(p => p && p !== '.' && p !== '..'), 'Invalid manifest path');
    assert(Number.isSafeInteger(entry.bytes) && entry.bytes >= 0 && /^[0-9a-f]{64}$/.test(entry.sha256), 'Invalid manifest pin');
    assert(!paths.has(entry.path), 'Duplicate manifest path'); paths.add(entry.path);
  }
  for (const p of [...sourceFiles, ...['PROTOCOL.md', 'RECORD-CONTRACT.md', 'runtime-pins.json', 'source/result-contract.json', 'source/supervise.py', 'source/guardian.py', 'source/check.py'].map(p => packageRelative + '/' + p)]) assert(paths.has(p), 'Missing required source pin: ' + p);
  const commit = process.env.RESEARCH_SOURCE_COMMIT || '';
  assert(/^[0-9a-f]{40}$/.test(commit), 'Source commit pin required');
  receipt = json(path.join(packageRoot, 'source-publication.json'));
  assert(receipt.remoteBytesEqualLocal === true && receipt.committedBytesEqualLocal === true && receipt.commit === commit && receipt.manifestSha256 === sha(manifestBytes) && receipt.manifestBytes === manifestBytes.length && receipt.manifestPath === relative(manifestPath) && receipt.verifiedFilePins === manifest.files.length, 'Publication receipt mismatch');
  const verified = Date.parse(receipt.verifiedUtc);
  attempt = json(path.join(resultRoot, 'kernel-attempt.json'));
  assert(attempt.stage === 'kernel' && attempt.sourceCommit === commit && attempt.sourceManifestSha256 === sha(manifestBytes) && attempt.configSha256 === sha(configBytes) && attempt.launchCutoffUtc === config.launchCutoffUtc && attempt.allocation === 'sole attempt; existence prevents retry', 'Permanent supervisor attempt mismatch');
  const started = Date.parse(attempt.startedUtc);
  assert(Number.isFinite(verified) && Number.isFinite(started) && verified <= started && started <= Date.now() && started < Date.parse(config.launchCutoffUtc), 'Invalid publication/attempt chronology');
  const executable = pin(process.execPath), runtimePins = json(path.join(packageRoot, 'runtime-pins.json'));
  assert(executable.bytes === runtimePins.node.bytes && executable.sha256 === runtimePins.node.sha256, 'Runtime binary pin mismatch');
  runtime = {node: process.version, platform: process.platform, arch: process.arch, executableSha256: executable.sha256};
  sourceSha256 = Object.fromEntries(sourceFiles.map(p => [p, manifest.files.find(e => e.path === p).sha256]));
  identity = {configId: config.id, configSha256: sha(configBytes), sourceManifestSha256: sha(manifestBytes), sourceCommit: commit, runtime};
  verifyManifest();
  for (const name of ['index.json', 'kernel-journal.jsonl', 'controls', 'scenes', 'generation']) assert(!fs.existsSync(path.join(resultRoot, name)), 'Runner output already exists: ' + name);
  for (const name of ['controls', 'scenes', 'generation']) fs.mkdirSync(path.join(resultRoot, name));
  journalFd = fs.openSync(path.join(resultRoot, 'kernel-journal.jsonl'), 'wx', 0o600);
  fs.fsyncSync(journalFd); fsyncDirectory(resultRoot);
}
function boundary() {
  assert(process.hrtime.bigint() - origin < BigInt(config.limits.kernelSeconds) * 1000000000n, 'Kernel time budget exceeded');
  assert(process.memoryUsage().rss <= config.limits.rssBytes, 'Kernel RSS budget exceeded');
}
function save(name, value, cap, failure = false) {
  if (!failure) boundary();
  const bytes = Buffer.from(encode(value) + '\n', 'utf8');
  assert(bytes.length <= cap, 'File size budget exceeded: ' + name);
  // Leave index and journal reserves available until completion/failure preservation.
  const reserve = name === 'index.json' ? 0 : config.limits.indexBytes;
  assert(scientificBytes + bytes.length + reserve + (config.limits.journalBytes - journalBytes) <= config.limits.kernelOutputBytes, 'Kernel output budget exceeded');
  const file = path.join(resultRoot, name), fd = fs.openSync(file, 'wx', 0o600);
  try { fs.writeFileSync(fd, bytes); fs.fsyncSync(fd); } finally { fs.closeSync(fd); }
  fsyncDirectory(path.dirname(file)); scientificBytes += bytes.length;
  return {path: relative(file), bytes: bytes.length, sha256: sha(bytes)};
}
function event(type, payload) {
  const line = Buffer.from(encode({schema: 'm31-moving-admission-journal-v1', sequence: eventSequence + 1, type, payload}) + '\n', 'utf8');
  assert(line.length <= 64 * 1024 && journalBytes + line.length <= config.limits.journalBytes, 'Journal budget exceeded');
  assert(scientificBytes + line.length <= config.limits.kernelOutputBytes, 'Kernel output budget exceeded');
  fs.writeFileSync(journalFd, line); fs.fsyncSync(journalFd);
  eventSequence++; journalBytes += line.length; scientificBytes += line.length;
}
function capture(states) {
  assert(Array.isArray(states) && states.length === config.generation.count, 'Invalid full-state callback count');
  return Object.freeze({drones: Object.freeze(states.map((state, id) => {
    assert(Array.isArray(state) && state.length === 17 && state.every(x => typeof x === 'number'), 'Invalid full-state callback layout');
    return Object.freeze({id, state: Object.freeze(state.map(A.bits))});
  }))});
}
const projection = input => input.drones.flatMap(d => [...d.state.slice(0, 3), ...d.state.slice(6, 10)]);
const inputHash = (id, input) => C.sha(C.encode({domain: 'm31-moving-admission/input/v1', id, input}));
function evaluate(id, kind, input, captureInfo) {
  boundary();
  const sequence = methodCalls + 1, inputSha256 = inputHash(id, input);
  event('method-start', {id, kind, sequence, inputSha256, capture: captureInfo});
  methodCalls++;
  let method = null, error = null;
  const phases = [], start = process.hrtime.bigint();
  try {
    method = M.method(input, 'filtered', name => {
      assert(name === ['prepared', 'spatial', 'assembled'][phases.length], 'Unexpected method phase sequence');
      phases.push({name, offsetNs: String(process.hrtime.bigint() - start)});
    });
  } catch (caught) { error = errorValue(caught); }
  const end = process.hrtime.bigint();
  const call = {sequence, startNs: String(start - origin), endNs: String(end - origin), totalNs: String(end - start), phases};
  const record = {id, kind, input, method, error};
  const saved = save((kind === 'control' ? 'controls/' : 'scenes/') + id + '.json', record, config.limits.sceneBytes, !!error);
  const descriptor = {id, kind, ...saved, inputSha256, capture: captureInfo, call};
  event('method-complete', descriptor);
  return {descriptor, error};
}
function optionsFor(item) {
  const g = config.generation;
  return {seed: item.seed, count: g.count, duration: g.duration, dt: g.dt, mode: g.mode,
    search: g.search, filter: g.filter, record: g.record, frameEvery: g.frameEvery};
}
function generate(item) {
  boundary();
  const generatorOptions = optionsFor(item);
  event('generation-start', {id: item.id, seed: item.seed, generatorOptions});
  generationRuns++;
  const frames = [], callbacks = [], slots = config.scheduledTimes.map(t => ({t, status: 'not-reached', input: null, reason: 'generator-error'}));
  let terminal = null, initial = null, final = null, runSummary = null, error = null;
  try {
    const returned = simulator.run({...generatorOptions,
      frameSink(frame) {
        boundary();
        assert(Array.isArray(frame) && frame.length === 1 + 7 * config.generation.count && frame.every(v => typeof v === 'number'), 'Invalid streamed frame');
        const t = frame[0];
        assert(Number.isFinite(t) && t >= 0 && t <= config.generation.duration && (frames.length === 0 ? t === 0 : t > frames.at(-1).t), 'Invalid frame chronology');
        assert(frames.length < 52, 'Too many streamed frames');
        frames.push(Object.freeze({t, words: Object.freeze(frame.slice(1).map(A.bits))}));
      },
      progress(metadata, states) {
        // The native values are copied to immutable words before any later simulator mutation.
        const input = capture(states);
        boundary();
        const {t, stopReason} = metadata;
        assert(Number.isFinite(t) && t >= 0 && t <= config.generation.duration && (callbacks.length === 0 ? t === 0 : t > callbacks.at(-1).t), 'Invalid progress chronology');
        assert(stopReason === null || (typeof stopReason === 'string' && stopReason.length > 0), 'Invalid stop reason');
        assert(frames.at(-1)?.t === t && same(projection(input), frames.at(-1).words), 'Progress and pose words differ');
        const slot = slots.find(s => s.t === t);
        if (slot) {
          assert(slot.status === 'not-reached', 'Duplicate scheduled callback');
          Object.assign(slot, {status: 'reached', input, reason: null});
        } else {
          assert(stopReason !== null && terminal === null, 'Unexpected unscheduled progress callback');
          terminal = {t, input, reason: stopReason};
        }
        callbacks.push(diagnostic(metadata));
        assert(callbacks.length <= 4, 'Too many progress callbacks');
      }
    });
    initial = capture(returned.initial); final = capture(returned.final);
    const {initial: ignoredInitial, final: ignoredFinal, frames: ignoredFrames, ...summary} = returned;
    assert(ignoredFrames === undefined, 'Simulator returned duplicate unstreamed frames');
    runSummary = diagnostic(summary);
    assert(same(initial, slots[0].input), 'Returned initial differs from captured slot0');
    const end = Number(returned.metrics.end.toFixed(6)), stopReason = returned.metrics.stopReason;
    assert(stopReason === null || (typeof stopReason === 'string' && stopReason.length > 0), 'Invalid terminal summary');
    assert(end >= 0 && end <= config.generation.duration && (stopReason !== null || end === config.generation.duration), 'Incomplete simulator return without stop reason');
    assert(frames.at(-1)?.t === end && same(projection(final), frames.at(-1).words), 'Final state and terminal frame differ');
    const lastInput = terminal?.input || [...slots].reverse().find(s => s.status === 'reached')?.input;
    assert(callbacks.at(-1)?.t === end && same(final, lastInput), 'Returned final differs from terminal full capture');
    assert(callbacks.at(-1).stopReason === stopReason, 'Terminal callback reason mismatch');
    const expectedTimes = [];
    for (let i = 0; i <= 50; i++) { const t = Number((i * config.generation.frameEvery).toFixed(6)); if (t <= end) expectedTimes.push(t); }
    if (expectedTimes.at(-1) !== end) expectedTimes.push(end);
    assert(same(frames.map(f => f.t), expectedTimes), 'Incomplete pose cadence');
    for (const slot of slots) {
      assert((slot.t <= end) === (slot.status === 'reached'), 'Incomplete scheduled callback capture');
      if (slot.status === 'not-reached') { assert(stopReason !== null, 'Missing slot without simulator stop'); slot.reason = stopReason; }
    }
    if (terminal) assert(terminal.t === end && terminal.reason === stopReason, 'Invalid off-schedule terminal capture');
    assert(same(returned.config, {filter: generatorOptions.filter, seed: item.seed, count: generatorOptions.count, mode: generatorOptions.mode, dt: generatorOptions.dt, duration: generatorOptions.duration, search: generatorOptions.search, course: 'factory-v1', airflow: 'off', observation: 'ideal'}), 'Generator returned configuration mismatch');
    assert(same(returned.recording, {cadence: config.generation.frameEvery, streamed: true}), 'Generator recording configuration mismatch');
  } catch (caught) {
    error = errorValue(caught); initial = null; final = null; runSummary = null;
    for (const slot of slots) if (slot.status === 'not-reached') slot.reason = 'generator-error';
  }
  const record = {schema: 'm31-moving-admission-generation-v1', ...identity, id: item.id, seed: item.seed,
    requested: config.generation, generatorOptions,
    generatorSource: {entry: generatorEntry, environment: {FLOCK_FACTORY_VARIANT: 'wide'}, sha256: Object.fromEntries(generatorFiles.map(p => [p, sourceSha256[p]]))},
    initial, final, frames, slots, terminal, callbacks, runSummary, error};
  const saved = save('generation/' + item.id + '.json', record, config.limits.generationBytesPerRun, !!error);
  const descriptor = {id: item.id, ...saved, seed: item.seed, status: error ? 'error' : 'completed', frameCount: frames.length,
    reachedTimes: slots.filter(s => s.status === 'reached').map(s => s.t), missingTimes: slots.filter(s => s.status === 'not-reached').map(s => s.t), error};
  generations.push(descriptor); generationRecords.push(record);
  for (const slot of slots) {
    const entry = scheduled.find(s => s.runId === item.id && s.t === slot.t);
    Object.assign(entry, {status: slot.status === 'reached' ? 'reached-not-evaluated' : 'not-reached',
      reason: slot.status === 'reached' ? 'query-pending' : slot.reason,
      generationSha256: saved.sha256, inputSha256: slot.input ? inputHash(entry.id, slot.input) : null});
  }
  event('generation-complete', descriptor);
  if (error) throw Object.assign(Error(error.message), {name: error.name});
}
function completion(status) {
  return {status, stage, methodCalls, generationRuns,
    reachedScheduled: scheduled.filter(s => ['reached-not-evaluated', 'evaluated', 'error'].includes(s.status)).length,
    missingScheduled: scheduled.filter(s => s.status === 'not-reached').length};
}
function indexValue(status, error) {
  return {schema: 'm31-moving-admission-index-v1', ...identity, sourceSha256, constants,
    controls, generations, scheduled, completion: completion(status), error};
}

function main() {
  preflight();
  try {
    // All scientific imports occur only after source/runtime/publication/attempt gates.
    M = require('./methods.cjs'); A = require('./adapter.cjs'); C = require('./canonical.cjs');
    process.env.FLOCK_FACTORY_VARIANT = 'wide';
    simulator = require(path.join(root, generatorEntry));
    const allowed = new Set(sourceFiles.filter(p => !p.endsWith('/config.json')).map(p => path.join(root, p)));
    for (const loaded of Object.keys(require.cache)) assert(allowed.has(loaded), 'Unexpected imported module: ' + relative(loaded));
    constants = A.constantBits;
    event('run-start', {...identity, sourceSha256, constants});
    for (let i = 0; i < config.controls.length; i++) {
      const control = config.controls[i]; stage = 'control:' + control.id;
      const out = evaluate(control.id, 'control', M.makeInput(control), {type: 'control', controlIndex: i});
      controls.push(out.descriptor);
      if (out.error) throw Object.assign(Error(out.error.message), {name: out.error.name});
    }
    for (const item of config.cases) { stage = 'generation:' + item.id; generate(item); }
    stage = 'generated-queries';
    assert(generations.length === 2 && generations.every(d => d.status === 'completed'), 'Generation barrier incomplete');
    event('generations-ready', {ids: generations.map(d => d.id), sha256: generations.map(d => d.sha256)});
    for (const entry of scheduled) {
      stage = 'scheduled:' + entry.id;
      if (entry.status === 'not-reached') { event('slot-not-reached', entry); continue; }
      assert(entry.status === 'reached-not-evaluated', 'Unexpected scheduled state');
      const generation = generationRecords.find(g => g.id === entry.runId), slotIndex = generation.slots.findIndex(s => s.t === entry.t);
      const out = evaluate(entry.id, 'scheduled', generation.slots[slotIndex].input,
        {type: 'generation-slot', runId: entry.runId, generationSha256: entry.generationSha256, slotIndex, t: entry.t});
      Object.assign(entry, {status: out.error ? 'error' : 'evaluated', reason: out.error ? 'method-error' : null, record: out.descriptor});
      if (out.error) throw Object.assign(Error(out.error.message), {name: out.error.name});
    }
    boundary(); verifyManifest();
    stage = 'complete';
    const index = indexValue('complete', null), saved = save('index.json', index, config.limits.indexBytes);
    event('run-complete', {...saved, completion: index.completion});
  } catch (caught) {
    const error = errorValue(caught); let saved = null;
    try { if (!fs.existsSync(path.join(resultRoot, 'index.json'))) saved = save('index.json', indexValue('failed', error), config.limits.indexBytes, true); } catch (preservationError) {
      process.stderr.write('Failure index preservation failed: ' + encode(errorValue(preservationError)) + '\n');
    }
    try { event('run-failed', {error, index: saved, completion: completion('failed')}); } catch (preservationError) {
      process.stderr.write('Failure journal preservation failed: ' + encode(errorValue(preservationError)) + '\n');
    }
    process.stderr.write(encode(error) + '\n'); process.exitCode = 1;
  } finally {
    if (journalFd !== null) { fs.fsyncSync(journalFd); fs.closeSync(journalFd); journalFd = null; }
  }
}
try { main(); } catch (error) { process.stderr.write(encode(errorValue(error)) + '\n'); process.exitCode = 1; }
