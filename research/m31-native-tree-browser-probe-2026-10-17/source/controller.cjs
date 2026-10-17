"use strict";
// Explicit single supervised qualification only. No scientific Node imports.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto'),os=require('node:os'),cp=require('node:child_process');
const PACKAGE='research/m31-native-tree-browser-probe-2026-10-17';
const [rootArg,expectedManifest,sourceCommit]=process.argv.slice(2),root=path.resolve(rootArg||'.'),pkg=path.join(root,PACKAGE),resultDir=path.join(pkg,'results');
const FILE_CAP=32*1024*1024,RECORD_CAP=2*1024*1024;
const need=(v,c)=>{if(!v)throw Error(c);},sha=b=>crypto.createHash('sha256').update(b).digest('hex'),pause=ms=>new Promise(r=>setTimeout(r,ms));
let store,transportHost,manifest,supervision,science,runtime,context,browserRoot,journalFd,timer,closed=false,launched=0,gated=false,saved=false,timedOut=false,stage='source-gate',rootExit=null,rootClose=null,rootError=null,journalBytes=0,journalSequence=0,closePromise=null;
let absoluteDeadline=0;const started=performance.now(),protectedPins=[];
const result={schema:'m31-native-tree-browser-probe-browser-v1',sourceManifestSha256:expectedManifest,sourceCommit,complete:false,errors:[],counts:{},inputs:{},servedPins:[],runtimeIdentityVerified:false,inputsAndSourcesPreserved:false,browserClosed:false,browserRootExitConfirmed:false,browserRootCloseConfirmed:false,allHelpersExitClaim:false,memoryLimitClaim:false};
function safePath(base,relative){need(typeof relative==='string'&&relative&&!path.isAbsolute(relative)&&!relative.split('/').includes('..'),'relative-path');const f=path.resolve(base,relative);need(fs.realpathSync(f).startsWith(fs.realpathSync(base)+path.sep),'path-outside-base');return f;}
function identity(file){const h=crypto.createHash('sha256'),b=Buffer.alloc(1024*1024),fd=fs.openSync(file,'r');let bytes=0;try{for(;;){const n=fs.readSync(fd,b,0,b.length,null);if(!n)break;bytes+=n;h.update(b.subarray(0,n));if(absoluteDeadline)guard();}}finally{fs.closeSync(fd);}return {bytes,sha256:h.digest('hex')};}
function verify(file,pin,code){need(pin&&Number.isSafeInteger(pin.bytes)&&/^[a-f0-9]{64}$/.test(pin.sha256),code+'-pin');const got=identity(file);need(got.bytes===pin.bytes&&got.sha256===pin.sha256,code);return got;}
function pinned(relative){const pin=manifest.files.find(x=>x.path===relative);need(pin,'unlisted-source');verify(safePath(root,relative),pin,'pinned-file');return pin;}
function readPinned(relative){const p=pinned(relative);need(p.bytes<=FILE_CAP,'pinned-read-cap');return fs.readFileSync(safePath(root,relative));}
function jsonPinned(relative){return JSON.parse(readPinned(relative).toString('utf8'));}
function load(file){need(fs.statSync(file).size<=FILE_CAP,'json-cap');return JSON.parse(fs.readFileSync(file,'utf8'));}
function guard(){need(!timedOut&&performance.now()<absoluteDeadline&&(!supervision||Date.now()<Date.parse(supervision.launchCutoffUtc)),'controller-deadline');}
function authorization(){need(supervision.executionAllowed===true&&supervision.authorization&&Number.isFinite(Date.parse(supervision.launchCutoffUtc))&&Date.now()<Date.parse(supervision.launchCutoffUtc),'execution-not-authorized');}
function create(file,bytes){need(bytes.length<=FILE_CAP,'output-file-cap');if(store&&!timedOut)store.budget(bytes.length);const fd=fs.openSync(file,'wx',0o600);try{fs.writeFileSync(fd,bytes);fs.fsyncSync(fd);}finally{fs.closeSync(fd);}const dd=fs.openSync(path.dirname(file),'r');try{fs.fsyncSync(dd);}finally{fs.closeSync(dd);}}
function append(kind,descriptor,metrics={}){
 guard();transportHost.validateDescriptor(descriptor);need(journalFd!==undefined&&typeof kind==='string'&&/^[a-z][a-z0-9-]{0,50}$/.test(kind),'journal-record');
 need(descriptor?.schema==='m31-lossless-record-v1'&&Array.isArray(descriptor.fields)&&descriptor.fields.length<=128&&descriptor.binaryBytes<=96*1024**2&&descriptor.jsonBytes<=256*1024**2&&descriptor.elements<=16000000,'transport-descriptor');
 let binaryBytes=0,elements=1;const keys=new Set();
 for(const f of descriptor.fields){need(typeof f.key==='string'&&!keys.has(f.key)&&f.stream?.schema==='m31-value-stream-v1','transport-field');keys.add(f.key);let length=0;
  for(let i=0;i<f.stream.chunks.length;i++){const pin=f.stream.chunks[i];need(i===f.stream.chunks.length-1||pin.bytes===1048576,'fixed-shard-boundary');length+=store.get(pin).length;}
  need(length===f.stream.binaryBytes,'stream-length');binaryBytes+=length;elements+=1+f.stream.elements;
 }
 need(binaryBytes===descriptor.binaryBytes&&elements===descriptor.elements,'descriptor-totals');
 for(const key of ['serializationMilliseconds','transferMilliseconds','persistMilliseconds'])need(Number.isFinite(metrics[key])&&metrics[key]>=0,'transport-timing');
 need(journalSequence<4096,'journal-record-count');const start=performance.now(),recordPin=store.record('records',String(journalSequence).padStart(4,'0')+'-'+kind,descriptor);
 const entry={sequence:journalSequence,kind,recordPin,...metrics},bytes=Buffer.from(JSON.stringify(entry)+'\n');
 need(bytes.length<=RECORD_CAP&&journalBytes+bytes.length<=RECORD_CAP,'journal-byte-cap');store.budget(bytes.length);
 fs.writeFileSync(journalFd,bytes);fs.fsyncSync(journalFd);journalBytes+=bytes.length;journalSequence++;
 result.counts[kind]=(result.counts[kind]||0)+1;
 if(kind==='failure'||kind==='driver-failure')result.errors.push({phase:stage,code:'driver-failure-record',sequence:entry.sequence});
 return {durable:true,sequence:entry.sequence,recordPin,persistMilliseconds:performance.now()-start};
}

function finalize(){if(saved||!gated)return;result.browserClosed=closed;result.browserRootExitConfirmed=rootExit!==null;result.browserRootCloseConfirmed=rootClose!==null;result.browserRoot={exit:rootExit,close:rootClose,error:rootError,scope:'Specific spawned Chrome root only; no every-helper exit guarantee'};result.transport=store?store.stats():null;result.preIndexElapsedMs=performance.now()-started;result.controllerProcessLifetimePeakRssBytes=process.resourceUsage().maxRSS*1024;result.peakRssScope='Node process lifetime maxRSS only; not Chrome renderer/tree aggregate or OS memory cap';result.complete=Boolean(result.scheduleReturned&&!timedOut&&result.runtimeIdentityVerified&&result.inputsAndSourcesPreserved&&closed&&launched===1&&rootError===null&&rootExit?.code===0&&rootExit.signal===null&&rootClose?.code===0&&rootClose.signal===null&&result.errors.length===0);if(journalFd!==undefined){fs.fsyncSync(journalFd);fs.closeSync(journalFd);journalFd=undefined;const f=path.join(resultDir,'browser-journal.jsonl');result.journal={path:PACKAGE+'/results/browser-journal.jsonl',...identityWithoutGuard(f),records:journalSequence};}create(path.join(resultDir,'browser.json'),Buffer.from(JSON.stringify(result)+'\n'));saved=true;}
function identityWithoutGuard(file){const h=crypto.createHash('sha256'),fd=fs.openSync(file,'r'),buffer=Buffer.alloc(1024*1024);let bytes=0;try{for(;;){const n=fs.readSync(fd,buffer,0,buffer.length,null);if(!n)break;bytes+=n;h.update(buffer.subarray(0,n));}}finally{fs.closeSync(fd);}return {bytes,sha256:h.digest('hex')};}
async function closeBrowser(){if(!context||closed)return;if(closePromise)return closePromise;closePromise=(async()=>{await Promise.race([context.close(),pause(3000).then(()=>{throw Error('browser-close-timeout');})]);for(let i=0;i<20&&(rootExit===null||rootClose===null);i++)await pause(100);need(browserRoot&&rootError===null&&rootExit?.code===0&&rootExit.signal===null&&rootClose?.code===0&&rootClose.signal===null,'browser-root-close-unconfirmed');closed=true;})();return closePromise;}
async function main(){
 need(process.argv.length===5&&/^[a-f0-9]{64}$/.test(expectedManifest)&&/^[a-f0-9]{40}$/.test(sourceCommit),'arguments');
 supervision=load(path.join(pkg,'config.json'));authorization();
 need(process.env.RESEARCH_EXECUTION_CONTEXT==='tool-require-escalated'&&!process.env.NODE_OPTIONS&&!process.env.NODE_PATH&&process.execArgv.length===0,'dispatch-context');
 const attemptPath=path.join(resultDir,'run-attempt.json'),attempt=load(attemptPath),token=process.env.RESEARCH_RUN_TOKEN;
 need(process.env.RESEARCH_STAGE==='browser'&&typeof token==='string'&&attempt.status==='running'&&attempt.stages?.browser?.status==='started'&&attempt.runTokenSha256===sha(token)&&attempt.sourceCommit===sourceCommit&&attempt.sourceManifestSha256===expectedManifest,'supervisor-binding');
 need(process.env.RESEARCH_CHILD_BUDGET_MILLISECONDS==='120000','browser-budget');absoluteDeadline=started+110000;guard(); // Local Node clock only; outer Python independently enforces120s. Ten seconds remain for controller/root closure and handoff.
 const manifestPath=path.join(pkg,'source-manifest.json'),manifestBytes=fs.readFileSync(manifestPath);need(sha(manifestBytes)===expectedManifest,'manifest-sha');manifest=JSON.parse(manifestBytes);need(Array.isArray(manifest.files)&&new Set(manifest.files.map(p=>p.path)).size===manifest.files.length,'manifest-paths');
 for(const pin of manifest.files)verify(safePath(root,pin.path),pin,'manifest-file');
 for(const rel of ['config.json','runtime.json','source/controller.cjs','source/browser.js','source/browser.html','source/science-config.json','source/source-bundle.json','source/browser-bundle.js','source/transport.cjs','source/transport-store.cjs'])pinned(PACKAGE+'/'+rel);
 supervision=jsonPinned(PACKAGE+'/config.json');authorization();
 const publicationPath=path.join(pkg,'source-publication.json'),publication=load(publicationPath);need(publication.commit===sourceCommit&&publication.manifestSha256===expectedManifest&&publication.manifestPath===PACKAGE+'/source-manifest.json'&&publication.manifestBytes===manifestBytes.length&&publication.verifiedFilePins===manifest.files.length&&publication.remoteBytesEqualLocal===true&&publication.committedBytesEqualLocal===true&&Date.parse(publication.verifiedUtc)<=Date.parse(attempt.startedUtc),'source-publication');
 for(const f of [manifestPath,publicationPath,attemptPath])protectedPins.push({file:f,...identity(f)});
 need(attempt.stages?.['saved-validation']?.status==='completed','saved-validation-required');const savedValidationPath=path.join(resultDir,'saved-validation.json'),savedValidation=load(savedValidationPath);verify(savedValidationPath,attempt.stages['saved-validation'].output,'saved-validation-output');need(savedValidation.complete===true&&savedValidation.passed===true&&savedValidation.sourceCommit===sourceCommit&&savedValidation.sourceManifestSha256===expectedManifest,'saved-validation-pass');protectedPins.push({file:savedValidationPath,...identity(savedValidationPath)});result.savedValidation={path:PACKAGE+'/results/saved-validation.json',...identity(savedValidationPath)};
 science=jsonPinned(PACKAGE+'/source/science-config.json');runtime=jsonPinned(PACKAGE+'/runtime.json');
 result.scienceConfig=pinned(PACKAGE+'/source/science-config.json');
 const bundle=jsonPinned(PACKAGE+'/source/source-bundle.json');need(bundle.path===PACKAGE+'/source/browser-bundle.js'&&Array.isArray(bundle.sources),'bundle-schema');const bundlePin=pinned(bundle.path),bundleBytes=readPinned(bundle.path);need(bundle.bytes===bundlePin.bytes&&bundle.sha256===bundlePin.sha256,'bundle-binding');let previousEnd=0;
 for(const source of bundle.sources){const original=readPinned(source.path);need(Number.isSafeInteger(source.offset)&&source.offset>=previousEnd&&source.bytes===original.length&&sha(original)===source.sha256&&bundleBytes.subarray(source.offset,source.offset+source.bytes).equals(original),'source-slice-binding');previousEnd=source.offset+source.bytes;}
 need(!fs.existsSync(path.join(resultDir,'browser.json'))&&!fs.existsSync(path.join(resultDir,'browser-journal.jsonl')),'single-use-output');
 journalFd=fs.openSync(path.join(resultDir,'browser-journal.jsonl'),'wx',0o600);gated=true;
 const timerMs=absoluteDeadline-performance.now();need(timerMs>0&&timerMs<120000,'controller-budget');
 timer=setTimeout(async()=>{timedOut=true;try{append('failure',{phase:stage,code:'controller-deadline'});}catch(_){}try{await closeBrowser();}catch(_){result.errors.push({phase:'close',code:'deadline-close-failure'});}try{finalize();}catch(_){}process.exit(2);},timerMs);
 stage='runtime-gate';
  verify(fs.realpathSync(process.execPath), runtime.node, 'node-runtime');
  need(process.version === runtime.node.version && os.arch() === runtime.architecture && os.platform() === runtime.platform && os.endianness() === 'LE', 'runtime-version');
  const modules = process.env.RESEARCH_NODE_MODULES, chrome = process.env.RESEARCH_CHROME_CONTENTS,
    profile = process.env.RESEARCH_BROWSER_PROFILE, privateDir = process.env.RESEARCH_PRIVATE_LOG_DIR;
  need([modules, chrome, profile, privateDir].every(x => typeof x === 'string' && path.isAbsolute(x)), 'runtime-environment-paths');
  need(!path.resolve(profile).startsWith(root + path.sep) && !fs.existsSync(profile), 'fresh-private-profile');
  need(!path.resolve(privateDir).startsWith(root + path.sep) && fs.statSync(privateDir).isDirectory(), 'private-log-directory');
  transportHost=require(safePath(root,PACKAGE+'/source/transport.cjs'));const {createStore}=require(safePath(root,PACKAGE+'/source/transport-store.cjs'));store=createStore(root,fs.realpathSync(privateDir),guard);
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
    try { create(path.join(privateDir, 'browser-process.json'), Buffer.from(JSON.stringify({pid: child.pid, command, args,
      detachedRequested: options?.detached === true, detachedApplied: false}) + '\n')); }
    catch (error) { try { child.kill('SIGKILL'); } catch (_) {} throw error; }
    result.browserLaunch = {count: launched, profileCount: 1, profileIdentitySha256: sha(profile), detachedApplied: false,
      argumentCount: args.length};
    return child;
  };
  stage = 'browser-launch';
  try {
    const {chromium} = require(path.join(modules, 'playwright'));
    need(Date.now() < Date.parse(supervision.launchCutoffUtc), 'browser-launch-cutoff');
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

 const origin='http://localhost:8876',allowed=new Map();
 for(const rel of ['source/browser.html','source/browser.js','source/browser-bundle.js']){const p=pinned(PACKAGE+'/'+rel);allowed.set('/'+p.path,p);}
 await context.route('**/*',async route=>{const u=new URL(route.request().url()),pin=allowed.get(u.pathname);if(u.origin!==origin||u.search||!pin||route.request().method()!=='GET'){result.errors.push({phase:stage,code:'unlisted-browser-request'});await route.abort();return;}try{const f=safePath(root,pin.path);verify(f,pin,'served-pin');const bytes=fs.readFileSync(f);need(bytes.length===pin.bytes&&sha(bytes)===pin.sha256,'served-byte-identity');result.servedPins.push(pin);await route.fulfill({status:200,contentType:pin.path.endsWith('.html')?'text/html':'application/javascript',body:bytes});}catch(_){result.errors.push({phase:stage,code:'served-source-changed'});await route.abort();}});
 await page.exposeBinding('__storeTreeShard',(_source,packet)=>{guard();need(packet&&Number.isInteger(packet.bytes)&&packet.bytes>0&&packet.bytes<=1048576&&typeof packet.base64==='string'&&packet.base64.length<=1398104&&/^[a-f0-9]{64}$/.test(packet.sha256),'shard-packet');const bytes=Buffer.from(packet.base64,'base64');need(bytes.length===packet.bytes&&bytes.toString('base64')===packet.base64&&sha(bytes)===packet.sha256,'shard-packet-identity');const start=performance.now(),pin=store.put(bytes);return {pin,persistMilliseconds:performance.now()-start};});
 await page.exposeBinding('__appendTreeRecord',(_source,kind,descriptor,metrics)=>append(kind,descriptor,metrics));
 authorization();guard();await page.goto(origin+'/'+PACKAGE+'/source/browser.html',{waitUntil:'load'});await page.waitForFunction(()=>typeof window.runNativeTreeProbe==='function');
 stage='coupled-driver';guard();
 const done=await page.evaluate(payload=>window.runNativeTreeProbe(payload),{config:science,bundle,provenance:{scienceConfig:result.scienceConfig,sourceManifestSha256:expectedManifest,sourceCommit},authorization:{executionAllowed:true,runTokenSha256:attempt.runTokenSha256,launchCutoffUtc:supervision.launchCutoffUtc},remainingMs:Math.max(1,absoluteDeadline-performance.now()-1000)});
 need(done?.complete===true,'driver-incomplete');result.scheduleReturned=true;result.driverReturn=done;
 stage='preservation';guard();for(const pin of manifest.files)verify(safePath(root,pin.path),pin,'postrun-source');for(const p of protectedPins)verify(p.file,p,'protected-file');for(const p of Object.values(result.inputs))verify(safePath(root,p.path),p,'stage-input-preserved');result.inputsAndSourcesPreserved=true;
}
main().catch(error=>{const body={phase:stage,code:/^[a-z0-9-]{1,100}$/.test(error.message||'')?error.message:'controller-exception',errorClass:error.constructor?.name||'Error'};if(gated){try{append('failure',body);}catch(_){result.errors.push(body);}}process.stderr.write(String(error.stack||error)+'\n');process.exitCode=1;}).finally(async()=>{if(timedOut||!gated)return;try{await closeBrowser();}catch(_){result.errors.push({phase:'close',code:'browser-close-failure'});}try{finalize();}catch(_){process.stderr.write('finalization-failure\n');process.exitCode=1;}clearTimeout(timer);if(!result.complete)process.exitCode=1;});
