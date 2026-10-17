'use strict';
// Fresh transfer only. Explicit post-publication invocation is required.
const fs = require('node:fs'), path = require('node:path'), crypto = require('node:crypto');
const os = require('node:os'), cp = require('node:child_process');
const PACKAGE = 'research/m31-native-fresh-transfer-2026-10-17';
const CASES = ['fresh-a-t5', 'fresh-b-t5'];
const MOVING = ['positive', 'distant-zero', 'raw-force', 'order-incompatible'];
const OWNERSHIP = ['L:sparse2', 'F:sparse2', 'L:planes62', 'F:planes62', 'L:fallback258', 'F:fallback258'];
const SOURCE_IDS = ['./vendor/reference-excerpt.cjs', './vendor/anchor-kernel.cjs', './vendor/lean-anchor.cjs', './vendor/kernel.cjs', './vendor/controls.cjs', './native-load.cjs', './native-controls.cjs'];
const FILE_CAP = 32 * 1024 * 1024, JOURNAL_CAP = 24 * 1024 * 1024, RECORD_CAP = 2 * 1024 * 1024;
const sha = bytes => crypto.createHash('sha256').update(bytes).digest('hex');
const need = (value, label) => { if (!value) throw Error(label); };
const same = (a, b) => JSON.stringify(a) === JSON.stringify(b);
const pause = ms => new Promise(resolve => setTimeout(resolve, ms));
const [rootArgument, expectedManifest, sourceCommit] = process.argv.slice(2);
const root = path.resolve(rootArgument || '.');
const pkg = path.join(root, PACKAGE), resultDir = path.join(pkg, 'results');
let context, browserRoot, journalFd, journalBytes = 0, journalSequence = 0, saved = false, timedOut = false;
let manifest, config, science, runtime, timer, launched = 0, closed = false, stage = 'source-gate';
let rootExit = null, rootClose = null, rootError = null;
const evidencePins = new Map();
const started = performance.now();
const result = {schema: 'm31-native-browser-qualification-v1', sourceManifestSha256: expectedManifest,
  sourceCommit, complete: false, scope: 'Two prospective fresh states; diagnostic call durations only; no benchmark or oracle input.',
  controls: {adapter: null, inherited: {expectedCount: 48, records: [], passed: false}, ownership: null,
    wrapper: {expectedCount: null, records: [], passed: false}, ownershipBuilds: []}, calls: [], targetAttempts: [], movingControlCalls: [], movingControlAttempts: [], errors: [], sourceReceipt: null,
  runtimeIdentityVerified: false, inputsAndSourcesPreserved: false, browserClosed: false,
  browserRootExitConfirmed: false, browserRootCloseConfirmed: false};
function safePath(base, relative) {
  need(typeof relative === 'string' && relative.length > 0 && !path.isAbsolute(relative) && !relative.split('/').includes('..'), 'relative-path');
  const full = path.resolve(base, relative), real = fs.realpathSync(full);
  need(real.startsWith(fs.realpathSync(base) + path.sep), 'path-outside-root');
  return full;
}
function fileIdentity(file) {
  const h = crypto.createHash('sha256'), buffer = Buffer.alloc(1024 * 1024), fd = fs.openSync(file, 'r');
  let bytes = 0;
  try { for (;;) { const n = fs.readSync(fd, buffer, 0, buffer.length, null); if (!n) break; bytes += n; h.update(buffer.subarray(0, n)); } }
  finally { fs.closeSync(fd); }
  return {bytes, sha256: h.digest('hex')};
}
function verify(file, pin, code) {
  need(pin && Number.isSafeInteger(pin.bytes) && pin.bytes >= 0 && /^[a-f0-9]{64}$/.test(pin.sha256), code + '-pin');
  const got = fileIdentity(file); need(got.bytes === pin.bytes && got.sha256 === pin.sha256, code); return got;
}
function pinned(relative) {
  const pin = manifest.files.find(item => item.path === relative); need(pin, 'unlisted-source');
  verify(safePath(root, relative), pin, 'pinned-file'); return pin;
}
function readPinned(relative) {
  pinned(relative); return fs.readFileSync(safePath(root, relative));
}
function jsonPinned(relative) { return JSON.parse(readPinned(relative).toString('utf8')); }
function samePin(a, b) { return a && b && a.path === b.path && a.bytes === b.bytes && a.sha256 === b.sha256; }
function bindEvidence(relative, expected = null) {
  need(typeof relative === 'string' && relative.startsWith(PACKAGE + '/results/'), 'fresh-result-path');
  const file = safePath(root, relative), pin = {path: relative, ...fileIdentity(file)};
  need(pin.bytes > 0 && pin.bytes <= FILE_CAP && (!expected || samePin(pin, expected)), 'fresh-result-pin');
  if (evidencePins.has(relative)) need(samePin(pin, evidencePins.get(relative)), 'fresh-result-changed');
  evidencePins.set(relative, pin); return pin;
}
function readEvidence(relative, expected = null) {
  const pin = bindEvidence(relative, expected);
  const bytes = fs.readFileSync(safePath(root, relative));
  need(bytes.length === pin.bytes && sha(bytes) === pin.sha256, 'fresh-result-read');
  return {value: JSON.parse(bytes.toString('utf8')), pin};
}
function completedStage(name) {
  const attempt = readEvidence(PACKAGE + '/results/' + name + '-attempt.json');
  const output = readEvidence(PACKAGE + '/results/' + name + '.json');
  const a = attempt.value, value = output.value;
  need(a.schema === 'm31-native-fresh-attempt-v1' && a.stage === name && a.status === 'completed' &&
    a.exitCode === 0 && a.childExitCode === 0 && a.childReaped === true && a.preservationPassed === true &&
    a.sourceCommit === sourceCommit && a.sourceManifestSha256 === expectedManifest &&
    a.outputBytes === output.pin.bytes && a.outputSha256 === output.pin.sha256, 'completed-' + name + '-stage');
  need(value.sourceCommit === sourceCommit && value.sourceManifestSha256 === expectedManifest, 'fresh-stage-source');
  return {value, pin: output.pin, attempt: attempt.pin};
}
function bindFreshInputs() {
  const generated = completedStage('generation'), referenced = completedStage('reference');
  const g = generated.value, r = referenced.value;
  need(g.schema === 'm31-native-fresh-generation-v1' && g.complete === true && g.inputsAndSourcesPreserved === true &&
    r.schema === 'm31-native-fresh-reference-index-v1' && r.complete === true && r.qualified === true && r.inputsAndSourcesPreserved === true &&
    samePin(r.generationIndex, generated.pin), 'fresh-prerequisite-indexes');
  need(g.slots.length === 2 && g.controls.length === 4 && r.targets.length === 2 && r.controls.length === 4, 'fresh-prerequisite-denominator');
  bindEvidence(g.journal.path, g.journal);
  const targetRows = [], controlRows = [];
  function novelty(value) {
    return value && value.passed === true && value.comparedCount === 6 && Array.isArray(value.matches) && value.matches.length === 0 &&
      /^[a-f0-9]{64}$/.test(value.rawContentSha256) && Array.isArray(value.retained) && value.retained.length === 6 &&
      value.retained.every((row, i) => row.id === science.retainedInputs[i].id && samePin(row.input, science.retainedInputs[i].input) &&
        row.rawContentSha256 === science.retainedInputs[i].rawContentSha256);
  }
  function association(row, reference, n) {
    need(reference.id === row.id && reference.n === n && samePin(reference.input, row.input) &&
      reference.semanticInputSha256 === row.semanticInputSha256 && reference.qualified === true &&
      /^[a-f0-9]{64}$/.test(row.semanticInputSha256), 'fresh-reference-input-association');
    need(row.input.path === PACKAGE + '/results/inputs/' + row.id + '.json', 'fresh-input-path');
    bindEvidence(row.input.path, row.input); bindEvidence(reference.reference.path, reference.reference);
  }
  for (let i = 0; i < 2; i++) {
    const row = g.slots[i], fixed = science.slots[i], reference = r.targets[i];
    need(row.id === fixed.id && row.seed === fixed.seed && row.t === 5 && row.n === 64 && same(row.methods, fixed.methods) &&
      row.status === 'captured' && row.motion?.passed === true && row.motion.stateChanged === true &&
      row.motion.relativeGeometryChanged === true, 'fresh-captured-slot');
    need(novelty(row.novelAgainstRetained) && novelty(reference.novelAgainstRetained) &&
      row.novelAgainstRetained.rawContentSha256 === reference.novelAgainstRetained.rawContentSha256, 'fresh-distinct-from-six-retained');
    association(row, reference, 64); bindEvidence(row.generation.path, row.generation);
    need(reference.referenceStatus === 'admitted' && reference.branch === 'loads' && reference.graphStatus === 'acyclic-compatible' && Number.isSafeInteger(reference.positiveRotorPairs) &&
      reference.positiveRotorPairs > 0, 'fresh-admitted-coupled-target');
    targetRows.push({id: row.id, n: 64, methods: row.methods, input: row.input, semanticInputSha256: row.semanticInputSha256});
  }
  for (let i = 0; i < 4; i++) {
    const row = g.controls[i], fixed = science.movingControls[i], reference = r.controls[i];
    const native = science.expectedNative[i], expected = science.expectedReference[i];
    need(row.id === MOVING[i] && row.id === fixed.id && row.n === fixed.drones.length && same(row.methods, ['F', 'L']) &&
      row.expectedNative.status === native.status && row.expectedNative.reason === native.reason &&
      row.expectedReference.status === expected.status && row.expectedReference.branch === expected.branch, 'fixed-moving-control');
    association(row, reference, row.n);
    need(reference.referenceStatus === expected.status && reference.branch === expected.branch, 'moving-reference-expectation');
    controlRows.push({id: row.id, n: row.n, methods: ['F', 'L'], input: row.input,
      semanticInputSha256: row.semanticInputSha256, expectedNative: native});
  }
  result.generationIndex = generated.pin; result.referenceIndex = referenced.pin;
  result.generationAttempt = generated.attempt; result.referenceAttempt = referenced.attempt;
  // No reference values, coefficients, solutions or control literals reach the native page payload.
  config.cases = targetRows; config.movingControls = controlRows;
}
function durableCreate(file, bytes) {
  need(bytes.length <= FILE_CAP, 'output-file-cap'); const fd = fs.openSync(file, 'wx', 0o600);
  try { fs.writeFileSync(fd, bytes); fs.fsyncSync(fd); } finally { fs.closeSync(fd); }
  const dir = fs.openSync(path.dirname(file), 'r'); try { fs.fsyncSync(dir); } finally { fs.closeSync(dir); }
}
function append(kind, body) {
  need(journalFd !== undefined, 'journal-unavailable');
  const entry = {sequence: journalSequence, kind, body};
  const bytes = Buffer.from(JSON.stringify(entry) + '\n');
  need(bytes.length <= RECORD_CAP && journalBytes + bytes.length <= JOURNAL_CAP, 'journal-cap');
  fs.writeFileSync(journalFd, bytes); fs.fsyncSync(journalFd); journalBytes += bytes.length; journalSequence++;
  if (kind === 'source') { result.sourceReceipt = body; result.controls.adapter = body.adapterControls; }
  else if (kind === 'inherited-control') result.controls.inherited.records.push(body);
  else if (kind === 'ownership') result.controls.ownership = body;
  else if (kind === 'ownership-build') result.controls.ownershipBuilds.push(body);
  else if (kind === 'wrapper-control') result.controls.wrapper.records.push(body);
  else if (kind === 'target') result.calls.push(body);
  else if (kind === 'intent' && body.phase === 'target') result.targetAttempts.push(body);
  else if (kind === 'moving-control') result.movingControlCalls.push(body);
  else if (kind === 'intent' && body.phase === 'moving-control') result.movingControlAttempts.push(body);
  else if (kind === 'failure') result.errors.push(body);
  return {sequence: entry.sequence, bytes: bytes.length, sha256: sha(bytes), durable: true};
}
function finalize() {
  if (saved) return;
  result.browserClosed = closed;
  result.browserRootExitConfirmed = rootExit !== null;
  result.browserRootCloseConfirmed = rootClose !== null;
  result.browserRoot = {exit: rootExit, close: rootClose, error: rootError,
    scope: 'Specific spawned Chrome root only; no every-helper-exit or hard-containment claim'};
  result.elapsedMs = performance.now() - started;
  result.controls.inherited.passed = result.controls.inherited.records.length === 48 && result.controls.inherited.records.every(r => r.pass === true);
  result.controls.wrapper.passed = result.controls.wrapper.records.length === result.controls.wrapper.expectedCount && result.controls.wrapper.records.every(r => r.pass === true);
  result.completedTargetCalls = result.calls.length;
  result.expectedTargetCalls = 4;
  result.completedMovingControlCalls = result.movingControlCalls.length;
  result.expectedMovingControlCalls = 8;
  result.unattemptedMovingControls = MOVING.flatMap(caseId => ['F', 'L'].map(method => ({caseId, method})))
    .filter(item => !result.movingControlAttempts.some(call => call.caseId === item.caseId && call.method === item.method));
  result.unfinishedMovingControlAttempts = result.movingControlAttempts.filter(item => !result.movingControlCalls.some(call => call.caseId === item.caseId && call.method === item.method));
  result.unattempted = CASES.flatMap((caseId, i) => (i % 2 ? ['L', 'F'] : ['F', 'L']).map(method => ({caseId, method})))
    .filter(item => !result.targetAttempts.some(call => call.caseId === item.caseId && call.method === item.method));
  result.unfinishedTargetAttempts = result.targetAttempts.filter(item => !result.calls.some(call => call.caseId === item.caseId && call.method === item.method));
  result.complete = Boolean(result.scheduleReturned && !timedOut && result.runtimeIdentityVerified &&
    result.inputsAndSourcesPreserved && closed && launched === 1 && rootError === null &&
    rootExit?.code === 0 && rootExit.signal === null && rootClose?.code === 0 && rootClose.signal === null && result.errors.length === 0 &&
    result.controls.adapter?.pass && result.controls.inherited.passed && result.controls.ownership?.pass &&
    result.controls.wrapper.passed && result.calls.length === 4 && result.movingControlCalls.length === 8 &&
    result.movingControlCalls.every(call => call.pass === true));
  if (journalFd !== undefined) { fs.fsyncSync(journalFd); fs.closeSync(journalFd); journalFd = undefined;
    result.journal = {path: PACKAGE + '/results/browser-journal.jsonl', ...fileIdentity(path.join(resultDir, 'browser-journal.jsonl')), records: journalSequence}; }
  durableCreate(path.join(resultDir, 'browser.json'), Buffer.from(JSON.stringify(result) + '\n')); saved = true;
}
async function closeBrowser() {
  if (!context || closed) return;
  await Promise.race([context.close(), pause(3000).then(() => { throw Error('browser-close-timeout'); })]);
  for (let i = 0; i < 20 && (rootExit === null || rootClose === null); i++) await pause(100);
  need(browserRoot && rootError === null && rootExit?.code === 0 && rootExit.signal === null &&
    rootClose?.code === 0 && rootClose.signal === null, 'browser-root-close-unconfirmed');
  closed = true;
}
async function main() {
  need(process.argv.length === 5 && /^[a-f0-9]{64}$/.test(expectedManifest) && /^[a-f0-9]{40}$/.test(sourceCommit), 'arguments');
  need(process.env.RESEARCH_EXECUTION_CONTEXT === 'tool-require-escalated', 'dispatch-attestation');
  need(!process.env.NODE_OPTIONS && process.execArgv.length === 0, 'node-options');
  need(!fs.existsSync(path.join(resultDir, 'browser.json')) && !fs.existsSync(path.join(resultDir, 'browser-journal.jsonl')), 'single-use-output');
  fs.mkdirSync(resultDir, {recursive: true});
  journalFd = fs.openSync(path.join(resultDir, 'browser-journal.jsonl'), 'wx', 0o600);
  const journalDirectory = fs.openSync(resultDir, 'r'); try { fs.fsyncSync(journalDirectory); } finally { fs.closeSync(journalDirectory); }
  timer = setTimeout(async () => {
    timedOut = true;
    try { append('failure', {phase: stage, code: 'controller-90-second-deadline'}); } catch (_) {}
    try { await closeBrowser(); } catch (_) { result.errors.push({phase: 'close', code: 'deadline-close-failure'}); }
    try { finalize(); } catch (_) {} process.exit(2);
  }, 90000);
  const manifestBytes = fs.readFileSync(path.join(pkg, 'source-manifest.json'));
  need(sha(manifestBytes) === expectedManifest, 'source-manifest-sha'); manifest = JSON.parse(manifestBytes);
  need(Array.isArray(manifest.files) && new Set(manifest.files.map(p => p.path)).size === manifest.files.length, 'manifest-paths');
  for (const pin of manifest.files) verify(safePath(root, pin.path), pin, 'manifest-file');
  const publication = JSON.parse(fs.readFileSync(path.join(pkg, 'source-publication.json')));
  need(publication.commit === sourceCommit && publication.manifestSha256 === expectedManifest &&
    publication.manifestBytes === manifestBytes.length && publication.verifiedFilePins === manifest.files.length &&
    publication.remoteBytesEqualLocal === true && publication.committedBytesEqualLocal === true, 'source-publication');
  config = jsonPinned(PACKAGE + '/source/browser-config.json'); runtime = jsonPinned(PACKAGE + '/runtime.json');
  science = jsonPinned(PACKAGE + '/source/science-config.json');
  need(config.schema === 'm31-native-fresh-browser-config-v1' && science.schema === 'm31-native-fresh-science-config-v1' &&
    science.slots.length === 2 && science.slots.every((c, i) => c.id === CASES[i] && c.n === 64 && c.t === 5 &&
      c.seed === 26171711 + i && same(c.methods, i % 2 ? ['L', 'F'] : ['F', 'L'])) &&
    science.movingControls.length === 4 && same(science.movingControls.map(c => c.id), MOVING) &&
    science.expectedNative.length === 4 && science.expectedReference.length === 4, 'fixed-target-schedule');
  const retainedIds = ['run-a', 'run-b'].flatMap(run => [0, 5, 10].map(t => run + '-t' + t));
  need(science.retainedInputs?.length === 6 && science.retainedInputs.every((row, i) => row.id === retainedIds[i] &&
    /^[a-f0-9]{64}$/.test(row.rawContentSha256) && samePin(row.input, pinned(row.input.path))), 'six-retained-novelty-input-pins');
  need(Number.isFinite(Date.parse(science.launchCutoffUtc)) && Date.now() < Date.parse(science.launchCutoffUtc), 'browser-launch-cutoff');
  need(config.controls.inheritedIds.length === 48 && same(config.controls.ownershipSequence, OWNERSHIP) &&
    config.controls.wrapper.length === 24, 'fixed-controls');
  need(new Set(config.controls.wrapper.map(x => x.id)).size === config.controls.wrapper.length, 'wrapper-control-ids');
  result.controls.wrapper.expectedCount = config.controls.wrapper.length;
  stage = 'fresh-prerequisite-gates'; bindFreshInputs();
  const bundle = jsonPinned(PACKAGE + '/source/source-bundle.json');
  need(bundle.path === PACKAGE + '/source/browser-bundle.js' && same(bundle.sources.map(s => s.id), SOURCE_IDS), 'bundle-schema');
  const bundlePin = pinned(bundle.path), bundleBytes = readPinned(bundle.path);
  need(bundle.bytes === bundlePin.bytes && bundle.sha256 === bundlePin.sha256, 'bundle-manifest-binding');
  let previousEnd = 0;
  for (const source of bundle.sources) {
    const original = readPinned(source.path);
    need(source.path === PACKAGE + '/source/' + source.id.slice(2) && Number.isSafeInteger(source.offset) && source.offset >= previousEnd &&
      source.bytes === original.length && sha(original) === source.sha256 &&
      bundleBytes.subarray(source.offset, source.offset + source.bytes).equals(original), 'source-slice-binding');
    previousEnd = source.offset + source.bytes;
  }
  stage = 'runtime-gate';
  verify(fs.realpathSync(process.execPath), runtime.node, 'node-runtime');
  need(process.version === runtime.node.version && os.arch() === runtime.architecture && os.platform() === runtime.platform && os.endianness() === 'LE', 'runtime-version');
  const modules = process.env.RESEARCH_NODE_MODULES, chrome = process.env.RESEARCH_CHROME_CONTENTS,
    profile = process.env.RESEARCH_BROWSER_PROFILE, privateDir = process.env.RESEARCH_PRIVATE_LOG_DIR;
  need([modules, chrome, profile, privateDir].every(x => typeof x === 'string' && path.isAbsolute(x)), 'runtime-environment-paths');
  need(!path.resolve(profile).startsWith(root + path.sep) && !fs.existsSync(profile), 'fresh-private-profile');
  need(!path.resolve(privateDir).startsWith(root + path.sep) && fs.statSync(privateDir).isDirectory(), 'private-log-directory');
  for (const pin of runtime.chrome.files) verify(safePath(chrome, pin.appRelativePath), pin, 'chrome-runtime-file');
  for (const pin of runtime.playwright.files) verify(safePath(modules, pin.moduleRelativePath), pin, 'playwright-runtime-file');
  need(JSON.parse(fs.readFileSync(path.join(modules, 'playwright/package.json'))).version === runtime.playwright.version, 'playwright-version');
  const launcherPin = runtime.chrome.files.find(p => p.label === 'launcher'); need(launcherPin, 'chrome-launcher-pin');
  const launcher = safePath(chrome, launcherPin.appRelativePath), originalSpawn = cp.spawn;
  // Playwright's detached request is overridden so the external supervisor owns this Chrome group.
  cp.spawn = function(command, args, options) {
    need(launched === 0 && typeof command === 'string' && fs.realpathSync(command) === fs.realpathSync(launcher), 'one-pinned-browser-spawn');
    verify(command, launcherPin, 'launch-binary');
    need(args.filter(x => x.startsWith('--user-data-dir=')).length === 1 && args.includes('--user-data-dir=' + profile), 'one-pinned-profile');
    const child = originalSpawn.call(this, command, args, {...options, detached: false}); launched++;
    // Capture this specific root before the patched spawn returns to Playwright.
    // Node emits these asynchronously, so listeners are installed before launch can resolve.
    browserRoot = child;
    child.once('error', error => { rootError = {errorClass: error.constructor?.name || 'Error'}; });
    child.once('exit', (code, signal) => { rootExit = {code, signal}; });
    child.once('close', (code, signal) => { rootClose = {code, signal}; });
    try { durableCreate(path.join(privateDir, 'browser-process.json'), Buffer.from(JSON.stringify({pid: child.pid, command, args,
      detachedRequested: options?.detached === true, detachedApplied: false}) + '\n')); }
    catch (error) { try { child.kill('SIGKILL'); } catch (_) {} throw error; }
    result.browserLaunch = {count: launched, profileCount: 1, profileIdentitySha256: sha(profile), detachedApplied: false,
      arguments: args.map(arg => arg.startsWith('--user-data-dir=') ? '--user-data-dir=[PRIVATE_PROFILE]' : arg)};
    return child;
  };
  stage = 'browser-launch';
  try {
    const {chromium} = require(path.join(modules, 'playwright'));
    need(Date.now() < Date.parse(science.launchCutoffUtc), 'browser-launch-cutoff');
    context = await chromium.launchPersistentContext(profile, {channel: 'chrome', executablePath: launcher, headless: true,
      timeout: 15000, args: ['--disable-background-networking'], viewport: {width: 800, height: 600}, serviceWorkers: 'block'});
  } finally { cp.spawn = originalSpawn; }
  need(launched === 1 && context.pages().length === 1, 'one-browser-page');
  const page = context.pages()[0]; page.setDefaultTimeout(10000);
  const cdp = await context.newCDPSession(page), browserVersion = await cdp.send('Browser.getVersion');
  need(browserVersion.product === 'Chrome/' + runtime.chrome.version, 'named-chrome-version');
  result.browser = {product: browserVersion.product, version: runtime.chrome.version, protocolVersion: browserVersion.protocolVersion,
    revision: browserVersion.revision, userAgent: browserVersion.userAgent, jsVersion: browserVersion.jsVersion, headless: true};
  result.runtime = {node: runtime.node, playwright: {version: runtime.playwright.version}, platform: os.platform(), architecture: os.arch(),
    chromeFilesVerified: runtime.chrome.files.length, playwrightFilesVerified: runtime.playwright.files.length,
    cpuModel: os.cpus()[0]?.model, logicalCores: os.cpus().length, installedRAMBytes: os.totalmem()};
  result.runtimeIdentityVerified = true;
  page.on('pageerror', () => result.errors.push({phase: stage, code: 'page-error'}));
  page.on('console', message => { if (message.type() === 'error') result.errors.push({phase: stage, code: 'console-error'}); });
  const origin = 'http://localhost:8876', allowed = new Map();
  for (const relative of ['source/browser.html', 'source/browser.js', 'source/browser-bundle.js']) {
    const p = pinned(PACKAGE + '/' + relative); allowed.set('/' + p.path, p);
  }
  for (const c of [...config.movingControls, ...config.cases]) allowed.set('/' + c.input.path, c.input);
  result.servedPins = [];
  await context.route('**/*', async route => {
    const u = new URL(route.request().url()), pin = allowed.get(u.pathname);
    if (u.origin !== origin || u.search || !pin || route.request().method() !== 'GET') {
      result.errors.push({phase: stage, code: 'unlisted-browser-request'}); await route.abort(); return;
    }
    try { const file = safePath(root, pin.path); verify(file, pin, 'served-source-or-input');
      const bytes = fs.readFileSync(file); need(bytes.length === pin.bytes && sha(bytes) === pin.sha256, 'served-byte-identity'); result.servedPins.push(pin);
      await route.fulfill({status: 200, contentType: pin.path.endsWith('.html') ? 'text/html' : pin.path.endsWith('.js') ? 'application/javascript' : 'application/json', body: bytes}); }
    catch (_) { result.errors.push({phase: stage, code: 'changed-served-file'}); await route.abort(); }
  });
  await page.exposeBinding('__appendNativeRecord', (_source, kind, body) => append(kind, body));
  await page.goto(origin + '/' + PACKAGE + '/source/browser.html', {waitUntil: 'load'});
  await page.waitForFunction(() => typeof window.runNativeQualification === 'function');
  stage = 'controls-and-targets';
  const done = await page.evaluate(async payload => window.runNativeQualification(payload), {config, bundle});
  need(done?.complete === true && done.targetCalls === 4 && done.movingControlCalls === 8, 'browser-schedule-incomplete'); result.scheduleReturned = true;
  stage = 'preservation';
  for (const pin of manifest.files) verify(safePath(root, pin.path), pin, 'postrun-source-input');
  for (const pin of evidencePins.values()) verify(safePath(root, pin.path), pin, 'postrun-fresh-evidence');
  result.prerequisitePins = [...evidencePins.values()];
  result.inputsAndSourcesPreserved = true;
}
main().catch(error => {
  const code = /^[a-z0-9-]{1,100}$/.test(error.message || '') ? error.message : 'controller-exception';
  const body = {phase: stage, code, errorClass: error.constructor?.name || 'Error'};
  try { append('failure', body); } catch (_) { result.errors.push(body); }
  // The supervisor retains this operational log privately; public evidence gets only the code.
  process.stderr.write(String(error.stack || error) + '\n');
}).finally(async () => {
  if (timedOut) return;
  try { await closeBrowser(); } catch (_) { result.errors.push({phase: 'close', code: 'browser-close-failure'}); }
  try { finalize(); } catch (error) { process.stderr.write('finalization-failure\n'); process.exitCode = 1; }
  clearTimeout(timer); if (!result.complete) process.exitCode = 1;
});
