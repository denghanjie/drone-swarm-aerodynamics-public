'use strict';
// STATIC PREPARATION: new GPU readback host. Disabled config rejects before runtime access.
const START=performance.now();
const fs=require('fs'),path=require('path'),crypto=require('crypto');
const {admitExecution,prepareDecodedEnvelope,emptyWriteReceipt,writeExclusive,classify,LIMITS}=require('./host-logic.cjs');
let registry,config,privateDir;
const base=path.resolve(__dirname,'..'),repo=path.resolve(base,'../..');
const raw=path.join(base,'raw'),results=path.join(base,'results');
const SHA='ba507e3ef0ad8991b3e84530f89fa51501e9c6fd274157d519ef10cb8aded951';
const pageBase='http://127.0.0.1:8876/'+path.relative(repo,__dirname).split(path.sep).join('/')+'/';
const EVENT_CAP=2048,EVENT_BYTES=8192,RAW_TRACE_CAP=3*1024*1024,PUBLIC_TRACE_CAP=2*1024*1024;
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
const check=(ok,message)=>{if(!ok)throw Error(message);};
let browser,page,rawFD,publicFD,expectedFixture,receivedBuffer,phase='admission',substantiveStopped=false;
let hardTimer,workTimer,traceClosed=false,eventCount=0,attemptedEvents=0,rawTraceBytes=0,publicTraceBytes=0;
let droppedEvents=0,truncatedEvents=0,observerExceptions=0,callbackErrors=0,unexpectedRedirects=0,unexpectedApplicationRequests=0,unexpectedRouteRequests=0;
const requests=new WeakMap(),cdpIDs=new Map(),listeners=[];
let requestCount=0,cdpCount=0;
const ready={playwright:false,cdpNetwork:false,cdpAudits:false,routes:false};
const out={version:1,kind:'synthetic-gpu-readback-diagnostic',fixtureId:'m31-u32-readback-128-v1',sourceCommit:process.env.RESEARCH_SOURCE_COMMIT||null,
 sourceFreezeSHA256:null,terminal:false,executionAllocated:false,scope:'One actual mapped GPU copy returned as owned ordinary bytes',
 qualified:false,scientificSuccess:false,explainsHistoricalFailure:false,performanceClaim:false,retryPermitted:false,
 independentPersistenceVerified:false,externalCompletionRequired:true,
 browserLaunches:0,evaluateCalls:0,applicationFetchCalls:0,observerReadyEvent:null,browserVersion:null,browserContext:null,
 runtimePinsBefore:false,runtimePinsAfter:false,expected:{bytes:128,sha256:SHA},errors:[],cleanupErrors:[],protocolDeviations:[],
 evaluation:{settled:false,timedOut:false,deadlineExceeded:false,errorName:null,hostMilliseconds:null,limitMilliseconds:12000},
 returned:{received:false,validationPassed:false,validationError:null,json:null,rejectionProjection:null,bytes:null,sha256:null,exact:null,
   pageStatus:null,pageFailureCodes:[],candidateByPageSelfReport:false},pageReport:null,
 persistence:{...emptyWriteReceipt(),exists:false,bytes:null,sha256:null,exact:null,equalsReturned:null},
 timing:{hostValidationMilliseconds:null,hostPersistenceMilliseconds:null,browserElapsedMilliseconds:null},
 browserCloseAttempted:false,browserCloseReturned:false,browserClosed:false};
const safeWord = x => typeof x === 'string' && /^[A-Za-z][A-Za-z0-9_. -]{0,159}$/.test(x) && !/[a-f0-9]{24}/i.test(x) ? x : null;
const safeNumber = x => typeof x === 'number' && Number.isFinite(x) ? x : null;
const headers = h => {
  const result = {};
  const allow = new Set(['origin','content-type','content-length','access-control-request-method','access-control-request-headers',
    'access-control-request-private-network','access-control-allow-origin','access-control-allow-methods',
    'access-control-allow-headers','access-control-allow-private-network','cache-control']);
  for (const [key, value] of Object.entries(h || {})) {
    const k = key.toLowerCase(); if (allow.has(k)) {const v=String(value);if(v.length>512)truncatedEvents++;result[k]=v.slice(0,512);}
  }
  return result;
};
function urlLabel(value) {
  if (value === pageBase + 'browser.html') return 'fixture-html';
  if (value === pageBase + 'gpu-readback-page.js') return 'fixture-script';
  if (typeof value === 'string' && value.startsWith('http://127.0.0.1:8876/')) return 'other-page-origin';
  return 'other';
}
function publicHeaders(h) {
  const a = headers(h);
  for (const k of ['origin', 'access-control-allow-origin']) if (k in a)
    a[k] = a[k] === 'http://127.0.0.1:8876' ? 'page-origin' : a[k] === '*' ? '*' : a[k] === 'null' ? 'opaque-null' : 'other-origin';
  for (const [k,v] of Object.entries(a)) {
    if (['origin','access-control-allow-origin'].includes(k)) continue;
    const known = k === 'content-length' ? /^\d{1,8}$/.test(v) : k === 'content-type' ?
      ['application/octet-stream','application/json','text/html','application/javascript'].includes(v) :
      k === 'cache-control' ? ['no-store','no-cache','max-age=0'].includes(v) :
      k.includes('private-network') ? ['true','false'].includes(v) :
      /^(?:(?:POST|OPTIONS|GET|HEAD|Content-Type|content-type)(?:, ?)?)+$/.test(v);
    if(!known)a[k]='other-header-value';
  }
  return a;
}
function publicData(d) {
  const p = {};
  for (const k of ['requestID','connectionID','cdpID','relatedCDPID','method','resourceType','errorName','errorCode','blockedReason','corsError',
    'issueCode','initiatorType','initiatorIPAddressSpace','resourceIPAddressSpace','localNetworkAccessRequestPolicy','type','reason','stage'])
    if (k in d && d[k] !== undefined) p[k] = safeWord(d[k]);
  if (d.errorText !== undefined) p.errorText = /^net::ERR_[A-Z0-9_]+$/.test(d.errorText) ? d.errorText : 'other-error-text';
  if (d.failedParameter !== undefined) p.failedParameterObserved = true;
  if (d.initiatorOrigin !== undefined) p.initiatorOriginLabel = d.initiatorOrigin === 'http://127.0.0.1:8876' ? 'page-origin' : d.initiatorOrigin === 'null' ? 'opaque-null' : 'other-origin';
  if (d.origin !== undefined) p.originLabel = d.origin === 'http://127.0.0.1:8876' ? 'page-origin' : d.origin === 'null' ? 'opaque-null' : 'other-origin';
  for (const k of ['bytes','jsonBytes','receivedBytes','writtenBytes','writeCalls','status','browserMilliseconds','encodedDataLength','callMilliseconds','validationMilliseconds','persistenceMilliseconds'])
    if (k in d) p[k] = safeNumber(d[k]);
  for (const k of ['match','started','complete','valid','exact','equalsReturned','ok','canceled','hasExtraInfo','ipProtectionUsed','initiatorIsSecureContext','isSecureContext','isWarning','auditReplayPossible','redirected'])
    if (k in d && d[k] !== undefined) p[k] = typeof d[k] === 'boolean' ? d[k] : null;
  if ('url' in d && d.url !== undefined) p.urlLabel = urlLabel(d.url);
  if(d.transferID === 'gpu-readback-1')p.transferID='gpu-readback-1';
  if ('headers' in d) p.headers = publicHeaders(d.headers);
  if ('sha256' in d) p.sha256 = /^[a-f0-9]{64}$/.test(d.sha256) ? d.sha256 : null;
  return p;
}
function record(kind, data = {}) {
  if (traceClosed||rawFD===undefined||publicFD===undefined) { observerExceptions++; return null; }
  if (attemptedEvents >= EVENT_CAP) { droppedEvents++; return null; }
  attemptedEvents++;
  try {
    if (kind.startsWith('gpu-host-') || kind.startsWith('persistence-')) data.transferID='gpu-readback-1';
    const envelope = {version: 1, id: 'e' + (eventCount + 1), sequence: eventCount + 1,
      clock: 'worker-monotonic-receipt', milliseconds: performance.now() - START, kind};
    let rawData = data;
    if (Buffer.byteLength(JSON.stringify(data)) > EVENT_BYTES - 512) {
      truncatedEvents++; rawData = {truncated: true, originalBytes: Buffer.byteLength(JSON.stringify(data))};
    }
    const r = Buffer.from(JSON.stringify({...envelope, data: rawData}) + '\n');
    const p = Buffer.from(JSON.stringify({...envelope, data: publicData(rawData)}) + '\n');
    if (rawTraceBytes + r.length > RAW_TRACE_CAP || publicTraceBytes + p.length > PUBLIC_TRACE_CAP) { droppedEvents++; return null; }
    const rw = fs.writeSync(rawFD, r); rawTraceBytes += rw;
    check(rw === r.length, 'Complete private trace write');
    const pw = fs.writeSync(publicFD, p); publicTraceBytes += pw;
    check(pw === p.length, 'Complete public trace write');
    eventCount++;
    return envelope.id;
  } catch (_) { observerExceptions++; return null; }
}
function on(emitter, name, fn) {
  const listener = (...args) => { try { fn(...args); } catch (error) {
    callbackErrors++; record('observer-callback-error', {type: error.name});
  }};
  emitter.on(name, listener); listeners.push({emitter,name,listener});
}
function fail(error, stage) {
  out.errors.push({stage, type: safeWord(error.name)});
  record('worker-error', {stage, errorName: error.name, errorMessage: error.message});
}
async function bounded(promise, ms, label) {
  let timer;
  try { return await Promise.race([promise, new Promise((_, reject) => {timer = setTimeout(() => reject(Error(label)), ms);})]); }
  finally { clearTimeout(timer); }
}
function guard(needed=0) { check(!substantiveStopped&&performance.now()-START+needed<34000,'Worker substantive deadline'); }
function readBoundedFile(filename,cap){const fd=fs.openSync(filename,fs.constants.O_RDONLY|fs.constants.O_NOFOLLOW);try{const st=fs.fstatSync(fd);check(st.isFile()&&st.size<=cap,'Bounded regular file');const data=Buffer.alloc(st.size);let at=0;while(at<data.length){const n=fs.readSync(fd,data,at,data.length-at,at);check(n>0,'Truncated bounded file');at+=n;}const tail=Buffer.alloc(1);check(fs.readSync(fd,tail,0,1,at)===0,'Grown bounded file');return data;}finally{fs.closeSync(fd);}}
function fileReceipt(filename,cap=3*1024*1024) {if(!fs.existsSync(filename))return null;const b=readBoundedFile(filename,cap);return {bytes:b.length,sha256:sha(b)};}
function pinFile(filename, pin) {
  guard(); const info = fs.statSync(filename); check(info.isFile() && info.size === pin.bytes, 'Runtime pin length');
  const fd = fs.openSync(filename, 'r'), h = crypto.createHash('sha256'), chunk = Buffer.alloc(1048576);
  try { let at = 0; while (at < info.size) { guard(); const n = fs.readSync(fd, chunk, 0, Math.min(chunk.length, info.size - at), at);
    check(n > 0, 'Runtime truncated'); h.update(chunk.subarray(0,n)); at += n; }
    check(fs.readSync(fd, chunk, 0, 1, info.size) === 0 && h.digest('hex') === pin.sha256, 'Runtime pin digest');
  } finally { fs.closeSync(fd); }
}
function runtimePins(runtime, executable) {
  check(path.isAbsolute(executable) && fs.realpathSync(executable) === executable, 'Explicit resolved Chrome executable');
  check(path.basename(executable) === 'Google Chrome' && path.basename(path.dirname(executable)) === 'MacOS', 'Chrome layout');
  const contents = path.resolve(path.dirname(executable), '..');
  check(fs.realpathSync(path.join(contents, 'Frameworks/Google Chrome Framework.framework/Versions/Current')) ===
    path.join(contents, 'Frameworks/Google Chrome Framework.framework/Versions', '155.0.8059.80'), 'Chrome Current version');
  check(runtime.chromeBundleVersion === '155.0.8059.80' && runtime.playwrightVersion === '1.62.1' && runtime.chromePins.length === 6, 'Pinned versions');
  for (const pin of runtime.chromePins) { const f = path.resolve(contents, pin.relativeToContents);
    check(f.startsWith(contents + path.sep) && fs.realpathSync(f).startsWith(contents + path.sep), 'Contained runtime pin'); pinFile(f, pin); }
}
function armPage() {
  const requestID = request => {if(!requests.has(request)) requests.set(request,'pw-'+(++requestCount));return requests.get(request);};
  on(page,'request',request=>{if(request.redirectedFrom())unexpectedRedirects++;
    if(['fetch','xhr'].includes(request.resourceType()) || request.method()==='POST')unexpectedApplicationRequests++;
    record('pw-request',{requestID:requestID(request),url:request.url(),method:request.method(),resourceType:request.resourceType(),headers:headers(request.headers()),redirected:!!request.redirectedFrom()});});
  on(page,'response',response=>record('pw-response',{requestID:requestID(response.request()),url:response.url(),status:response.status(),headers:headers(response.headers())}));
  on(page,'requestfailed',request=>record('pw-request-failed',{requestID:requestID(request),url:request.url(),errorText:request.failure()?.errorText}));
  on(page,'console',message=>record('page-console',{type:message.type(),text:message.text()}));
  on(page,'pageerror',error=>record('page-error',{errorName:error.name,errorMessage:error.message}));
  on(page,'crash',()=>{callbackErrors++;record('page-crash');}); on(page,'close',()=>record('page-close'));
  ready.playwright=true;
}
async function armCDP() {
  const cdp=await page.context().newCDPSession(page);
  const id = value => {if(!cdpIDs.has(value))cdpIDs.set(value,'cdp-'+(++cdpCount));return cdpIDs.get(value);};
  on(cdp,'Network.requestWillBeSent',e=>{if(e.redirectResponse)unexpectedRedirects++;
    record('cdp-request',{cdpID:id(e.requestId),url:e.request.url,method:e.request.method,headers:headers(e.request.headers),resourceType:e.type,
      redirected:!!e.redirectResponse,redirectResponse:e.redirectResponse?{url:e.redirectResponse.url,status:e.redirectResponse.status,headers:headers(e.redirectResponse.headers)}:undefined,
      cdpMonotonicSeconds:e.timestamp,cdpWallTimeSeconds:e.wallTime,initiatorType:e.initiator?.type,relatedCDPID:e.initiator?.requestId?id(e.initiator.requestId):undefined});});
  on(cdp,'Network.requestWillBeSentExtraInfo',e=>record('cdp-request-extra',{cdpID:id(e.requestId),headers:headers(e.headers),
    initiatorIsSecureContext:e.clientSecurityState?.initiatorIsSecureContext,initiatorIPAddressSpace:e.clientSecurityState?.initiatorIPAddressSpace,
    localNetworkAccessRequestPolicy:e.clientSecurityState?.localNetworkAccessRequestPolicy}));
  on(cdp,'Network.responseReceived',e=>record('cdp-response',{cdpID:id(e.requestId),url:e.response.url,status:e.response.status,headers:headers(e.response.headers),hasExtraInfo:e.hasExtraInfo,
    cdpMonotonicSeconds:e.timestamp,remoteIPAddress:e.response.remoteIPAddress,remotePort:e.response.remotePort}));
  on(cdp,'Network.responseReceivedExtraInfo',e=>record('cdp-response-extra',{cdpID:id(e.requestId),status:e.statusCode,headers:headers(e.headers),resourceIPAddressSpace:e.resourceIPAddressSpace,ipProtectionUsed:e.ipProtectionUsed}));
  on(cdp,'Network.loadingFinished',e=>record('cdp-loading-finished',{cdpID:id(e.requestId),encodedDataLength:e.encodedDataLength}));
  on(cdp,'Network.loadingFailed',e=>record('cdp-loading-failed',{cdpID:id(e.requestId),errorText:e.errorText,blockedReason:e.blockedReason,
    corsError:e.corsErrorStatus?.corsError,failedParameter:e.corsErrorStatus?.failedParameter,canceled:e.canceled,resourceType:e.type}));
  on(cdp,'Audits.issueAdded',e=>{const cors=e.issue.details?.corsIssueDetails, pna=e.issue.details?.genericIssueDetails;
    record('cdp-audit-issue',{issueCode:e.issue.code,cdpID:cors?.request?.requestId?id(cors.request.requestId):undefined,
      url:cors?.request?.url,corsError:cors?.corsErrorStatus?.corsError,failedParameter:cors?.corsErrorStatus?.failedParameter,
      resourceIPAddressSpace:cors?.resourceIPAddressSpace,initiatorIPAddressSpace:cors?.clientSecurityState?.initiatorIPAddressSpace,
      localNetworkAccessRequestPolicy:cors?.clientSecurityState?.localNetworkAccessRequestPolicy,
      initiatorIsSecureContext:cors?.clientSecurityState?.initiatorIsSecureContext,isWarning:cors?.isWarning,
      initiatorOrigin:cors?.initiatorOrigin,genericErrorType:pna?.errorType,
      auditReplayPossible:true});});
  await cdp.send('Network.enable');ready.cdpNetwork=true;
  await cdp.send('Audits.enable');ready.cdpAudits=true;
}
function writeReturnedJSON(data,name='returned.json') {
  guard();check(['returned.json','rejected-return.json'].includes(name),'Fixed return artifact');
  check(data.length<=32768,'Returned JSON retained cap');
  const receipt={...emptyWriteReceipt(),bytes:null,sha256:null};
  out.returned[name==='returned.json'?'json':'rejectionProjection']=receipt;
  writeExclusive(fs,path.join(raw,name),data,receipt,guard);
  receipt.bytes=data.length;receipt.sha256=sha(data);
  return receipt;
}
function persistActualBytes(bytes) {
  guard();check(bytes.length===128,'Validated received byte length');
  record('persistence-started',{bytes:bytes.length,sha256:sha(bytes)});
  const started=performance.now();
  try{writeExclusive(fs,path.join(raw,'received.bin'),bytes,out.persistence,guard,receipt=>record('persistence-write',{writtenBytes:receipt.writtenBytes,writeCalls:receipt.writeCalls}));}
  finally{out.timing.hostPersistenceMilliseconds=performance.now()-started;}
  record('persistence-completed',{complete:out.persistence.complete,bytes:out.persistence.writtenBytes,sha256:sha(bytes)});
}
async function main() {
  // entry() has already rejected disabled/null-window config before runtime artifacts/imports.
  guard();check(/^[a-f0-9]{40}$/.test(out.sourceCommit||''),'Published source identity');
  check(typeof process.env.RESEARCH_PROCESS_REGISTRY==='string'&&path.isAbsolute(process.env.RESEARCH_PROCESS_REGISTRY),'External private registry required');
  privateDir=path.dirname(process.env.RESEARCH_PROCESS_REGISTRY);
  check(!path.resolve(privateDir).startsWith(repo+path.sep),'Private trace must be outside publication tree');
  registry=require('./process-registry.cjs');
  fs.mkdirSync(raw,{recursive:true});check(fs.readdirSync(raw).length===0,'Fresh raw directory');fs.mkdirSync(results,{recursive:true});
  rawFD=fs.openSync(path.join(privateDir,'trace.private.ndjson'),'wx',0o600);publicFD=fs.openSync(path.join(raw,'trace.public.ndjson'),'wx');
  const freezeBytes=readBoundedFile(path.join(base,'freeze.json'),1048576);out.sourceFreezeSHA256=sha(freezeBytes);
  check(out.sourceFreezeSHA256===process.env.RESEARCH_REMOTE_VERIFIED_FREEZE,'Verified freeze');
  for(const pin of JSON.parse(freezeBytes).files){const f=path.resolve(repo,pin.path);check(f.startsWith(repo+path.sep),'Contained source pin');
    check(!path.isAbsolute(pin.path)&&!pin.path.split('/').includes('..'),'Relative source pin');const b=readBoundedFile(f,1048576);check(b.length===pin.bytes&&sha(b)===pin.sha256,'Frozen source bytes');}
  expectedFixture=readBoundedFile(path.join(base,'expected.bin'),128);check(expectedFixture.length===128&&sha(expectedFixture)===SHA,'Frozen synthetic fixture');
  const runtime=JSON.parse(readBoundedFile(path.join(base,'runtime-provenance.json'),1048576));
  const pw=path.dirname(require.resolve('playwright/package.json')),core=path.dirname(require.resolve('playwright-core/package.json'));
  const runtimeFiles=[process.execPath,path.join(pw,'package.json'),path.join(pw,'index.js'),path.join(core,'package.json'),path.join(core,'index.js'),path.join(core,'lib/coreBundle.js')];
  check(runtime.pins.length===6,'Runtime entry pin count');runtimeFiles.forEach((f,i)=>pinFile(f,runtime.pins[i]));
  const executable=process.env.RESEARCH_CHROME_EXECUTABLE;runtimePins(runtime,executable);out.runtimePinsBefore=true;
  const {chromium}=require('playwright');phase='browser-launch';
  guard();check(admitExecution(config,Date.now()).ok,'Fresh launch window');check(out.browserLaunches===0,'Sole browser launch');
  check(record('browser-launch-intent')!==null,'Retained browser boundary');guard();out.browserLaunches++;
  browser=await chromium.launch({channel:'chrome',executablePath:executable,headless:true,timeout:15000});
  guard();check(registry.hasRegisteredBrowser(),'Registered browser');const browserVersion=await browser.version();
  check(browserVersion==='155.0.8059.80','Browser version');out.browserVersion=browserVersion;runtimePins(runtime,executable);out.runtimePinsAfter=true;
  page=await browser.newPage();page.setDefaultTimeout(15000);armPage();await armCDP();
  const routed=new Map([['browser.html','text/html'],['gpu-readback-page.js','application/javascript']].map(([name,type])=>[pageBase+name,{type,bytes:readBoundedFile(path.join(__dirname,name),65536)}]));
  await page.route('**/*',route=>{const fixture=routed.get(route.request().url());if(fixture&&route.request().method()==='GET')return route.fulfill({status:200,contentType:fixture.type,body:fixture.bytes});
    unexpectedRouteRequests++;record('unexpected-route-blocked',{url:route.request().url(),method:route.request().method()});return route.abort('blockedbyclient');});ready.routes=true;
  out.observerReadyEvent=record('observers-ready');check(out.observerReadyEvent,'Observer readiness retained');
  phase='navigation';await page.goto(pageBase+'browser.html');
  check(droppedEvents===0&&truncatedEvents===0&&observerExceptions===0&&callbackErrors===0,'Pre-evaluate trace health');
  phase='evaluate-started';guard();
  check(out.evaluateCalls===0&&Object.values(ready).every(Boolean),'Sole observed payload evaluation');
  guard(12000);check(admitExecution(config,Date.now()).ok,'Fresh payload window');
  check(record('gpu-host-evaluate-started')!==null,'Retained evaluate boundary');
  guard(12000);check(admitExecution(config,Date.now()).ok,'Fresh payload window');
  const evaluationStart=performance.now();let actual;
  try {
    out.evaluateCalls++;
    actual=await bounded(page.evaluate(()=>window.runSyntheticGPUReadback()),12000,'GPUHostEvaluateDeadline');
    out.evaluation.settled=true;out.returned.received=true;phase='evaluate-returned';
    record('gpu-host-evaluate-returned',{callMilliseconds:performance.now()-evaluationStart});
  } catch(error) {
    out.evaluation.timedOut=error.message==='GPUHostEvaluateDeadline';
    out.evaluation.settled=!out.evaluation.timedOut;out.evaluation.errorName=safeWord(error.name);
    record('gpu-host-evaluate-error',{errorName:error.name,errorMessage:error.message});
    phase=out.evaluation.timedOut?'evaluate-timeout':'evaluate-rejected';
    if(out.evaluation.timedOut)out.protocolDeviations.push('evaluate-timeout-not-cancellation');
    if(performance.now()-evaluationStart>=12000){out.evaluation.deadlineExceeded=true;out.protocolDeviations.push('evaluate-deadline-overrun');}
    return; // Never persist or make another extraction after failed/expired evaluate.
  } finally {out.evaluation.hostMilliseconds=performance.now()-evaluationStart;}
  if(out.evaluation.hostMilliseconds>=12000){out.evaluation.deadlineExceeded=true;out.protocolDeviations.push('evaluate-deadline-overrun');phase='evaluate-deadline-overrun';return;}
  guard();phase='validate-returned-envelope';const validationStart=performance.now();let validated;
  try{validated=prepareDecodedEnvelope(actual);}
  finally{out.timing.hostValidationMilliseconds=performance.now()-validationStart;}
  if(!validated.ok){out.returned.validationError=validated.validationError;
    writeReturnedJSON(Buffer.from(JSON.stringify(validated.projection)+'\n'),'rejected-return.json');
    phase='envelope-rejected';record('gpu-host-envelope-rejected',{valid:false,errorCode:validated.validationError});return;}
  out.returned.validationPassed=true;out.returned.pageStatus=validated.pageStatus;out.returned.pageFailureCodes=validated.pageFailureCodes;
  out.returned.candidateByPageSelfReport=validated.candidateByPageSelfReport;out.pageReport=validated.pageReport;
  out.browserContext={...actual.context};out.timing.browserElapsedMilliseconds=actual.browserElapsedMilliseconds;
  guard();phase='retain-returned-envelope';writeReturnedJSON(Buffer.from(validated.json,'utf8'));
  if(validated.byteValues===null){phase='page-failed-without-bytes';record('gpu-host-envelope-without-bytes',{valid:true});return;}
  // Only validator-returned checked actual bytes are coerced. Expected bytes are comparison-only.
  guard();phase='convert-returned-values';receivedBuffer=Buffer.from(validated.byteValues);
  check(receivedBuffer.length===128,'Checked returned byte length');out.returned.bytes=receivedBuffer.length;out.returned.sha256=sha(receivedBuffer);out.returned.exact=receivedBuffer.equals(expectedFixture);
  record('gpu-host-envelope-validated',{valid:true,jsonBytes:Buffer.byteLength(validated.json),bytes:receivedBuffer.length,sha256:out.returned.sha256,exact:out.returned.exact});
  phase='persist-returned-bytes';persistActualBytes(receivedBuffer);phase='persistence-returned';
}

async function cleanup() {
  if(browser){out.browserCloseAttempted=true;try{await bounded(browser.close(),3000,'Browser close deadline');out.browserCloseReturned=true;out.browserClosed=true;}
    catch(error){out.cleanupErrors.push({stage:'browser-close',type:safeWord(error.name)});}}
  else out.browserClosed=out.browserLaunches===0;
  const received=path.join(raw,'received.bin');
  if(fs.existsSync(received)){out.persistence.exists=true;try{const b=readBoundedFile(received,128);out.persistence.bytes=b.length;out.persistence.sha256=sha(b);
    out.persistence.exact=expectedFixture?b.equals(expectedFixture):false;out.persistence.equalsReturned=receivedBuffer?b.equals(receivedBuffer):false;}
    catch(error){out.cleanupErrors.push({stage:'closed-file-read',type:safeWord(error.name)});}}
  if(unexpectedApplicationRequests>0)out.protocolDeviations.push('unexpected-application-network-request');
  if(unexpectedRouteRequests>0)out.protocolDeviations.push('unexpected-route-request');
  record('cleanup-finished',{complete:out.cleanupErrors.length===0&&out.browserClosed});out.lastPhase=phase;
  for(const {emitter,name,listener}of listeners)emitter.removeListener(name,listener);
  traceClosed=true;const traceCloses={private:false,public:false};
  for(const [key,fd]of [['private',rawFD],['public',publicFD]])if(fd!==undefined){try{fs.closeSync(fd);traceCloses[key]=true;}catch(error){out.cleanupErrors.push({stage:key+'-trace-close',type:safeWord(error.name)});}}
  out.instrumentation={ready,eventCount,attemptedEvents,eventCap:EVENT_CAP,droppedEvents,truncatedEvents,observerExceptions,callbackErrors,
    collectionBeforeEvaluate:out.evaluateCalls===0||out.observerReadyEvent!==null,captureClosedAfterCleanup:traceCloses.private&&traceCloses.public,traceCloses,
    unexpectedRedirectObservations:unexpectedRedirects,unexpectedApplicationRequestObservations:unexpectedApplicationRequests,unexpectedRouteRequests,
    complete:Object.values(ready).every(Boolean)&&traceCloses.private&&traceCloses.public&&droppedEvents===0&&truncatedEvents===0&&observerExceptions===0&&callbackErrors===0&&unexpectedRedirects===0&&unexpectedApplicationRequests===0&&unexpectedRouteRequests===0,
    clock:'worker-monotonic-receipt',browserClock:'browser-performance-independent',crossClockOrderingClaimed:false};
  out.trace={public:fileReceipt(path.join(raw,'trace.public.ndjson')),private:privateDir?fileReceipt(path.join(privateDir,'trace.private.ndjson')):null};
  out.localObservationComplete=out.browserLaunches===1&&out.evaluateCalls===1&&out.instrumentation.complete&&out.cleanupErrors.length===0&&out.errors.length===0&&out.protocolDeviations.length===0&&out.browserClosed&&out.evaluation.settled&&!out.evaluation.timedOut&&!out.evaluation.deadlineExceeded;
  out.status=classify(out);out.terminal=true;out.elapsedSeconds=(performance.now()-START)/1000;check(out.elapsedSeconds<40,'Worker including cleanup limit');
  const data=Buffer.from(JSON.stringify(out,null,2)+'\n');check(data.length<=65536,'Result byte cap');
  const resultWrite=emptyWriteReceipt();writeExclusive(fs,path.join(results,'result.json'),data,resultWrite,()=>check(performance.now()-START<40000,'Finalization deadline'));
  const summary=Buffer.from(JSON.stringify({kind:'synthetic-gpu-readback-worker-summary',status:out.status,terminal:true,qualified:false,externalCompletionRequired:true,resultBytes:data.length,resultSHA256:sha(data),resultWriteClosed:resultWrite.closed})+'\n');
  check(fs.writeSync(1,summary)===summary.length,'Complete worker summary');process.exitCode=out.localObservationComplete?0:1;
}
async function entry(){
  // Configuration is the sole file read permitted before disabled/window rejection.
  config=JSON.parse(readBoundedFile(path.join(base,'config.json'),16384));
  const admission=admitExecution(config,Date.now());check(admission.ok,admission.code);out.executionAllocated=true;
  hardTimer=setTimeout(()=>process.exit(124),Math.max(0,40000-(performance.now()-START)));
  workTimer=setTimeout(()=>{substantiveStopped=true;fail(Error('Worker substantive deadline'),'deadline');if(page)page.close().catch(()=>{});},Math.max(0,34000-(performance.now()-START)));
  try{await main();}catch(error){fail(error,phase);}finally{clearTimeout(workTimer);try{await cleanup();}catch(error){process.exitCode=1;
    try{fs.writeSync(2,Buffer.from(JSON.stringify({kind:'worker-finalization-failed',type:safeWord(error.name)})+'\n'));}catch(_){}}
    finally{hardTimer.unref();}}
}
if(require.main===module)entry().catch(error=>{process.exitCode=1;try{fs.writeSync(2,Buffer.from(JSON.stringify({kind:'gpu-host-admission-rejected',code:/^[a-z-]{1,80}$/.test(error.message)?error.message:'admission-error'})+'\n'));}catch(_){}});
