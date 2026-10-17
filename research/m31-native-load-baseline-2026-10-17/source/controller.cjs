'use strict';
// Retained qualification only. Explicit post-publication invocation is required.
const fs = require('node:fs'), path = require('node:path'), crypto = require('node:crypto');
const os = require('node:os'), cp = require('node:child_process');
const PACKAGE = 'research/m31-native-load-baseline-2026-10-17';
const CASES = ['run-a-t0', 'run-a-t5', 'run-a-t10', 'run-b-t0', 'run-b-t5', 'run-b-t10'];
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
let context, journalFd, journalBytes = 0, journalSequence = 0, saved = false, timedOut = false;
let manifest, config, runtime, timer, launched = 0, closed = false, stage = 'source-gate';
const started = performance.now();
const result = {schema: 'm31-native-browser-qualification-v1', sourceManifestSha256: expectedManifest,
  sourceCommit, complete: false, scope: 'Retained qualification; diagnostic call durations only; no benchmark or oracle input.',
  controls: {adapter: null, inherited: {expectedCount: 48, records: [], passed: false}, ownership: null,
    wrapper: {expectedCount: null, records: [], passed: false}, ownershipBuilds: []}, calls: [], targetAttempts: [], errors: [], sourceReceipt: null,
  runtimeIdentityVerified: false, inputsAndSourcesPreserved: false, browserClosed: false};
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
  else if (kind === 'failure') result.errors.push(body);
  return {sequence: entry.sequence, bytes: bytes.length, sha256: sha(bytes), durable: true};
}
function finalize() {
  if (saved) return;
  result.browserClosed = closed;
  result.elapsedMs = performance.now() - started;
  result.controls.inherited.passed = result.controls.inherited.records.length === 48 && result.controls.inherited.records.every(r => r.pass === true);
  result.controls.wrapper.passed = result.controls.wrapper.records.length === result.controls.wrapper.expectedCount && result.controls.wrapper.records.every(r => r.pass === true);
  result.completedTargetCalls = result.calls.length;
  result.expectedTargetCalls = 12;
  result.unattempted = CASES.flatMap((caseId, i) => (i % 2 ? ['L', 'F'] : ['F', 'L']).map(method => ({caseId, method})))
    .filter(item => !result.targetAttempts.some(call => call.caseId === item.caseId && call.method === item.method));
  result.unfinishedTargetAttempts = result.targetAttempts.filter(item => !result.calls.some(call => call.caseId === item.caseId && call.method === item.method));
  result.complete = Boolean(result.scheduleReturned && !timedOut && result.runtimeIdentityVerified &&
    result.inputsAndSourcesPreserved && closed && launched === 1 && result.errors.length === 0 &&
    result.controls.adapter?.pass && result.controls.inherited.passed && result.controls.ownership?.pass &&
    result.controls.wrapper.passed && result.calls.length === 12);
  if (journalFd !== undefined) { fs.fsyncSync(journalFd); fs.closeSync(journalFd); journalFd = undefined;
    result.journal = {path: PACKAGE + '/results/browser-journal.jsonl', ...fileIdentity(path.join(resultDir, 'browser-journal.jsonl')), records: journalSequence}; }
  durableCreate(path.join(resultDir, 'browser.json'), Buffer.from(JSON.stringify(result) + '\n')); saved = true;
}
async function closeBrowser() {
  if (!context || closed) return;
  await Promise.race([context.close(), pause(3000).then(() => { throw Error('browser-close-timeout'); })]); closed = true;
}
async function main() {
  need(process.argv.length === 5 && /^[a-f0-9]{64}$/.test(expectedManifest) && /^[a-f0-9]{40}$/.test(sourceCommit), 'arguments');
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
  config = jsonPinned(PACKAGE + '/config.json'); runtime = jsonPinned(PACKAGE + '/runtime.json');
  need(config.schema === 'm31-native-load-qualification-config-v1' && config.cases.length === 6 &&
    config.cases.every((c, i) => c.id === CASES[i] && c.n === 64 && same(c.methods, i % 2 ? ['L', 'F'] : ['F', 'L'])), 'fixed-target-schedule');
  need(config.controls.inheritedIds.length === 48 && same(config.controls.ownershipSequence, OWNERSHIP) &&
    config.controls.wrapper.length > 0 && config.controls.wrapper.length <= 24, 'fixed-controls');
  need(new Set(config.controls.wrapper.map(x => x.id)).size === config.controls.wrapper.length, 'wrapper-control-ids');
  result.controls.wrapper.expectedCount = config.controls.wrapper.length;
  for (const c of config.cases) need(same(c.input, pinned(c.input.path)) && /^[a-f0-9]{64}$/.test(c.semanticInputSha256), 'case-input-pin');
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
    try { durableCreate(path.join(privateDir, 'browser-process.json'), Buffer.from(JSON.stringify({pid: child.pid, command, args,
      detachedRequested: options?.detached === true, detachedApplied: false}) + '\n')); }
    catch (error) { try { child.kill('SIGKILL'); } catch (_) {} throw error; }
    result.browserLaunch = {count: launched, profileCount: 1, profileIdentitySha256: sha(profile), detachedApplied: false,
      arguments: args.map(arg => arg.startsWith('--user-data-dir=') ? '--user-data-dir=[PRIVATE_PROFILE]' : arg)};
    return child;
  };
  const {chromium} = require(path.join(modules, 'playwright'));
  stage = 'browser-launch';
  context = await chromium.launchPersistentContext(profile, {channel: 'chrome', executablePath: launcher, headless: true,
    timeout: 15000, args: ['--disable-background-networking'], viewport: {width: 800, height: 600}, serviceWorkers: 'block'});
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
  for (const c of config.cases) allowed.set('/' + c.input.path, c.input);
  result.servedPins = [];
  await context.route('**/*', async route => {
    const u = new URL(route.request().url()), pin = allowed.get(u.pathname);
    if (u.origin !== origin || u.search || !pin || route.request().method() !== 'GET') {
      result.errors.push({phase: stage, code: 'unlisted-browser-request'}); await route.abort(); return;
    }
    try { const bytes = readPinned(pin.path); result.servedPins.push(pin);
      await route.fulfill({status: 200, contentType: pin.path.endsWith('.html') ? 'text/html' : pin.path.endsWith('.js') ? 'application/javascript' : 'application/json', body: bytes}); }
    catch (_) { result.errors.push({phase: stage, code: 'changed-served-file'}); await route.abort(); }
  });
  await page.exposeBinding('__appendNativeRecord', (_source, kind, body) => append(kind, body));
  await page.goto(origin + '/' + PACKAGE + '/source/browser.html', {waitUntil: 'load'});
  await page.waitForFunction(() => typeof window.runNativeQualification === 'function');
  stage = 'controls-and-targets';
  const done = await page.evaluate(async payload => window.runNativeQualification(payload), {config, bundle});
  need(done?.complete === true && done.targetCalls === 12, 'browser-schedule-incomplete'); result.scheduleReturned = true;
  stage = 'preservation';
  for (const pin of manifest.files) verify(safePath(root, pin.path), pin, 'postrun-source-input');
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
