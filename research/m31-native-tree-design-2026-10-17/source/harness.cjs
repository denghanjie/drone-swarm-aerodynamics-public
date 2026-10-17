"use strict";
// One supervised kernel qualification. Scientific modules load only after the gates.
const fs = require('node:fs'), path = require('node:path'), crypto = require('node:crypto'), os = require('node:os');
const START = performance.now(), NAME = 'research/m31-native-tree-design-2026-10-17';
const ORIGINAL = 'research/m31-native-fresh-transfer-2026-10-17/source';
const [rootArg, expected, commit] = process.argv.slice(2);
const root = path.resolve(rootArg || '.'), pkg = path.join(root, NAME), results = path.join(pkg, 'results');
const FILE_CAP = 32 * 1024 ** 2, TOTAL_CAP = 128 * 1024 ** 2, WORK_MS = 120000;
const METHODS = ['F', 'H0', 'H'];
const CLOSURE = [NAME+'/source/harness.cjs', NAME+'/source/native-load.cjs', NAME+'/source/kernel.cjs', NAME+'/source/tree.cjs',
  ORIGINAL+'/native-load.cjs', ...['kernel.cjs','anchor-kernel.cjs','lean-anchor.cjs','reference-excerpt.cjs'].map(f => ORIGINAL+'/vendor/'+f)];
const need = (value, code) => { if (!value) throw Error(code); };
const sha = bytes => crypto.createHash('sha256').update(bytes).digest('hex');
let config, manifest, journal, journalBytes = 0, privateDirectory, gated = false, phase = 'authorization', saved = false;
let localDeadline = START + WORK_MS - 5000; // Local clock; five seconds remain within the outer work allocation for handoff.
const protectedPins = [], emitted = [];
const result = {schema:'m31-native-tree-work-v1', sourceManifestSha256:expected, sourceCommit:commit,
  startedUtc:new Date().toISOString(), complete:false, status:'incomplete', reason:null, cases:[], evidenceFiles:[],
  runtimeIdentityVerified:false, inputsAndSourcesPreserved:false, executionRetries:0,
  scope:'Fixed small controls and one exposed saved64 regression; no trajectory, capacity, timing or physical-validity qualification'};
function guard() {
  need(performance.now() < localDeadline && (!config || Date.now() < Date.parse(config.launchCutoffUtc)), 'work-deadline');
}
function safe(relative) {
  need(typeof relative === 'string' && relative && !path.isAbsolute(relative) && !relative.split('/').includes('..'), 'relative-source-path');
  const file = path.resolve(root, relative);
  need(fs.realpathSync(file) === file && file.startsWith(root+path.sep) && fs.statSync(file).isFile(), 'source-location');
  return file;
}
function identity(file, bounded = true) {
  const h = crypto.createHash('sha256'), buffer = Buffer.alloc(1024*1024), fd = fs.openSync(file, 'r');
  let bytes = 0;
  try { for (;;) { if (bounded) guard(); const n = fs.readSync(fd, buffer, 0, buffer.length, null); if (!n) break; bytes += n; h.update(buffer.subarray(0,n)); } }
  finally { fs.closeSync(fd); }
  return {bytes, sha256:h.digest('hex')};
}
function verify(file, pin) {
  need(pin && Number.isSafeInteger(pin.bytes) && /^[a-f0-9]{64}$/.test(pin.sha256), 'pin-shape');
  const got = identity(file); need(got.bytes === pin.bytes && got.sha256 === pin.sha256, 'pin-identity'); return got;
}
function load(file) { need(fs.statSync(file).size <= FILE_CAP, 'json-byte-cap'); return JSON.parse(fs.readFileSync(file,'utf8')); }
function pin(relative) { const p = manifest.files.find(p => p.path === relative); need(p, 'unlisted-source'); verify(safe(relative),p); return p; }
function loadPinned(relative) { pin(relative); return load(safe(relative)); }
function authorize() {
  const a = config.authorization;
  need(config.schema === 'm31-native-tree-supervision-v1' && config.executionAllowed === true && a &&
    typeof a.id === 'string' && a.id.length > 0 && /^[a-f0-9]{64}$/.test(a.reviewedSourceManifestSha256) &&
    Date.parse(a.approvedUtc) <= Date.now() && Date.now() < Date.parse(config.launchCutoffUtc), 'execution-not-authorized');
}
function syncDirectory(directory) { const fd = fs.openSync(directory,'r'); try { fs.fsyncSync(fd); } finally { fs.closeSync(fd); } }
function diskUsage() {
  let total = 0;
  function visit(directory) {
    for (const entry of fs.readdirSync(directory,{withFileTypes:true})) {
      const file = path.join(directory,entry.name); need(!entry.isSymbolicLink(), 'output-symlink');
      if (entry.isDirectory()) visit(file);
      else { const st = fs.lstatSync(file); need(st.isFile() && st.size <= FILE_CAP, 'output-file-cap'); total += st.size; }
    }
  }
  visit(results); visit(privateDirectory); return total;
}
function create(file, value) {
  const bytes = Buffer.from(JSON.stringify(value)+'\n'); need(bytes.length <= FILE_CAP, 'output-file-cap');
  need(diskUsage()+bytes.length+2*1024**2 <= TOTAL_CAP, 'work-output-cap');
  const fd = fs.openSync(file,'wx',0o600); try { fs.writeFileSync(fd,bytes); fs.fsyncSync(fd); } finally { fs.closeSync(fd); }
  syncDirectory(path.dirname(file)); const p = {path:path.relative(root,file),bytes:bytes.length,sha256:sha(bytes)}; emitted.push(p); return p;
}
function append(row) {
  guard(); const bytes = Buffer.from(JSON.stringify(row)+'\n'); need(journalBytes+bytes.length <= FILE_CAP, 'journal-file-cap');
  need(diskUsage()+bytes.length+2*1024**2 <= TOTAL_CAP, 'work-output-cap');
  fs.writeFileSync(journal,bytes); fs.fsyncSync(journal); journalBytes += bytes.length;
}
function decode(word) { need(typeof word === 'string' && /^[a-f0-9]{16}$/.test(word), 'binary64-word'); return Buffer.from(word,'hex').readDoubleBE(0); }
function decodeInput(words) {
  need(words && Array.isArray(words.drones) && words.drones.length > 0 && words.drones.length <= 64, 'qualification-input-count');
  return {drones:words.drones.map(d => {
    need(d && Array.isArray(d.state) && d.state.length === 17, 'word-state-shape');
    const out = {state:d.state.map(decode)}; if (Object.hasOwn(d,'id')) out.id = d.id; return out;
  })};
}
function same(a,b) {
  if (Object.is(a,b)) return true;
  if (!a || !b || typeof a !== 'object' || typeof b !== 'object' || Object.getPrototypeOf(a) !== Object.getPrototypeOf(b)) return false;
  const ka = Reflect.ownKeys(a), kb = Reflect.ownKeys(b);
  return ka.length === kb.length && ka.every(k => {
    const da = Object.getOwnPropertyDescriptor(a,k), db = Object.getOwnPropertyDescriptor(b,k);
    return db && Object.hasOwn(da,'value') && Object.hasOwn(db,'value') && da.writable === db.writable &&
      da.enumerable === db.enumerable && da.configurable === db.configurable && same(da.value,db.value);
  });
}
function expand(spec, plan) {
  if (spec.kind === 'saved') {
    const p = pin(spec.input.path); need(p.bytes === spec.input.bytes && p.sha256 === spec.input.sha256 && spec.exposedRegression === true, 'saved-input-pin');
    return loadPinned(spec.input.path);
  }
  let descriptors = spec.drones;
  if (spec.kind === 'boundary') {
    const recipe = plan.boundaryRecipe; need(Number.isInteger(spec.axis) && spec.axis >= 0 && spec.axis < 3, 'boundary-axis');
    const origin = Array(3).fill(recipe.otherCoordinateWord), center = origin.slice(); center[spec.axis] = spec.sourceWord;
    descriptors = [{id:recipe.receiverId,centerWords:origin}, {id:recipe.sourceFirstId,repeat:recipe.sourceCount,centerWords:center}];
  } else need(spec.kind === 'inline', 'case-kind');
  const drones = [];
  for (const d of descriptors) {
    const count = d.repeat === undefined ? 1 : d.repeat, step = d.idStep === undefined ? 1 : d.idStep;
    need(Number.isInteger(count) && count > 0 && count <= 64 && Number.isSafeInteger(step), 'inline-repeat');
    need(Array.isArray(d.centerWords) && d.centerWords.length === 3, 'inline-center');
    for (let i=0; i<count; i++) {
      const state = plan.baseStateWords.slice(); d.centerWords.forEach((word,j) => { state[j] = word; });
      for (const [index,word] of Object.entries(d.stateOverrides || {})) {
        need(/^(0|[1-9][0-9]*)$/.test(index) && Number(index) < 17, 'state-override-index'); state[Number(index)] = word;
      }
      const drone = {state}; if (!d.omitId) drone.id = d.id+i*step; drones.push(drone);
    }
  }
  return {drones};
}
function verifyProtected() {
  for (const p of manifest.files) verify(safe(p.path),p);
  for (const p of protectedPins) verify(p.file,p);
  for (const p of emitted) verify(safe(p.path),p);
}
function main() {
  need(process.argv.length === 5 && /^[a-f0-9]{64}$/.test(expected) && /^[a-f0-9]{40}$/.test(commit) && fs.realpathSync(root) === root, 'arguments');
  config = load(path.join(pkg,'config.json')); authorize();
  need(process.platform === 'darwin' && process.env.RESEARCH_EXECUTION_CONTEXT === 'tool-require-escalated' && !process.env.NODE_OPTIONS && !process.env.NODE_PATH && process.execArgv.length === 0, 'dispatch-context');
  need(process.env.RESEARCH_CHILD_BUDGET_MILLISECONDS === String(WORK_MS) && process.env.RESEARCH_STAGE === 'work', 'work-budget'); guard();
  const attemptFile = path.join(results,'run-attempt.json'), attempt = load(attemptFile), token = process.env.RESEARCH_RUN_TOKEN;
  need(typeof token === 'string' && /^[a-f0-9]{64}$/.test(token) && attempt.status === 'running' && attempt.stages?.work?.status === 'started' &&
    attempt.sourceCommit === commit && attempt.sourceManifestSha256 === expected && attempt.runTokenSha256 === sha(token), 'supervisor-binding');
  const manifestFile = path.join(pkg,'source-manifest.json'), mId = identity(manifestFile); need(mId.sha256 === expected, 'manifest-sha');
  manifest = load(manifestFile); need(Array.isArray(manifest.files) && new Set(manifest.files.map(p => p.path)).size === manifest.files.length, 'manifest-paths');
  for (const p of manifest.files) verify(safe(p.path),p);
  for (const relative of [...CLOSURE,NAME+'/config.json',NAME+'/runtime.json',NAME+'/source/cases.json']) pin(relative);
  config = loadPinned(NAME+'/config.json'); authorize();
  const publicationFile = path.join(pkg,'source-publication.json'), publication = load(publicationFile);
  need(publication.commit === commit && publication.manifestSha256 === expected && publication.manifestPath === NAME+'/source-manifest.json' &&
    publication.manifestBytes === mId.bytes && publication.verifiedFilePins === manifest.files.length && publication.remoteBytesEqualLocal === true &&
    publication.committedBytesEqualLocal === true && Date.parse(publication.verifiedUtc) <= Date.parse(attempt.startedUtc), 'source-publication');
  for (const file of [manifestFile,publicationFile,attemptFile]) protectedPins.push({file,...identity(file)});
  const runtime = loadPinned(NAME+'/runtime.json'); verify(fs.realpathSync(process.execPath),runtime.node);
  need(runtime.node.bytes === manifest.runtime.node.bytes && runtime.node.sha256 === manifest.runtime.node.sha256 &&
    process.version === runtime.node.version && os.platform() === runtime.platform && os.arch() === runtime.architecture && os.endianness() === 'LE', 'runtime-identity');
  result.runtimeIdentityVerified = true;
  privateDirectory = process.env.RESEARCH_PRIVATE_LOG_DIR;
  need(typeof privateDirectory === 'string' && path.isAbsolute(privateDirectory) && fs.realpathSync(privateDirectory) === privateDirectory &&
    !privateDirectory.startsWith(root+path.sep) && privateDirectory !== root && fs.statSync(privateDirectory).isDirectory() &&
    attempt.privateDirectoryIdentitySha256 === sha(privateDirectory), 'private-directory-binding');
  const plan = loadPinned(NAME+'/source/cases.json'); need(plan.schema === 'm31-native-tree-cases-v1' && plan.baseStateWords.length === 17 &&
    plan.cases.length === 42 && new Set(plan.cases.map(c => c.id)).size === plan.cases.length &&
    plan.cases.filter(c => c.kind === 'saved').length === 1, 'fixed-case-plan');
  need(!fs.existsSync(path.join(results,'work.json')) && !fs.existsSync(path.join(results,'work.jsonl')) && !fs.existsSync(path.join(results,'evidence')), 'single-use-work-output');
  fs.mkdirSync(path.join(results,'evidence')); journal = fs.openSync(path.join(results,'work.jsonl'),'wx',0o600); syncDirectory(results); gated = true;
  phase = 'scientific-import'; guard(); authorize();
  const F = require(safe(ORIGINAL+'/native-load.cjs')), H = require(safe(NAME+'/source/native-load.cjs'));
  for (const file of Object.keys(require.cache)) need(CLOSURE.includes(path.relative(root,file)), 'import-outside-pinned-closure');
  phase = 'fixed-cases';
  for (let index=0; index<plan.cases.length; index++) {
    guard(); const spec = plan.cases[index]; need(/^[a-z0-9-]{1,80}$/.test(spec.id), 'case-id');
    const words = expand(spec,plan), row = {id:spec.id,input:words,methods:{},inputUnchanged:{}};
    for (const method of METHODS) {
      guard(); const input = decodeInput(words), original = decodeInput(words), api = method === 'F' ? F : H;
      result.activeCase = {index,id:spec.id,method};
      const value = method === 'F' ? api.query(input,'F',guard) : api.query(input,method,guard,{treeEvidence:true});
      row.inputUnchanged[method] = same(input,original);
      const evidence = api.encodeEvidence(value);
      const file = path.join(results,'evidence',String(index).padStart(3,'0')+'-'+spec.id+'-'+method+'.json');
      const p = create(file,evidence); result.evidenceFiles.push({caseId:spec.id,method,...p}); row.methods[method] = evidence;
      need(row.inputUnchanged[method], 'producer-input-mutation'); guard();
    }
    append(row); result.cases.push(row);
  }
  delete result.activeCase; phase = 'preservation'; verifyProtected(); result.inputsAndSourcesPreserved = true;
  result.complete = true; result.status = 'completed';
}
function finalize() {
  if (!gated || saved) return;
  if (journal !== undefined) { fs.fsyncSync(journal); fs.closeSync(journal); journal = undefined; }
  result.journal = {path:NAME+'/results/work.jsonl',...identity(path.join(results,'work.jsonl'),false),records:result.cases.length};
  result.completedUtc = new Date().toISOString(); result.preFinalReportWallMilliseconds = performance.now()-START;
  result.processLifetimePeakRssBytes = process.resourceUsage().maxRSS*1024;
  result.peakRssScope = 'Node process lifetime maxRSS converted from KiB; no OS memory ceiling or stage-isolated allocation claim';
  result.timingScope = 'Entry through pre-final-report timestamp; final durable write and exit occur later within outer work/total supervision';
  create(path.join(results,'work.json'),result); saved = true;
  need(performance.now()-START < WORK_MS && Date.now() < Date.parse(config.launchCutoffUtc), 'post-report-work-deadline');
}
try { main(); }
catch (error) {
  result.complete = false; result.status = 'failed'; result.reason = {phase,code:/^[a-z0-9-]{1,100}$/.test(error.message||'') ? error.message : 'work-exception',errorClass:error.constructor?.name||'Error'};
  process.stderr.write(String(error.stack||error)+'\n'); process.exitCode = 1;
}
finally { try { finalize(); } catch (error) { process.stderr.write('work-finalization-failure\n'); process.exitCode = 1; } }
