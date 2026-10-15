'use strict';
// New ordinary-heap control-channel diagnostic. No HTTP payload sink or scientific code.
const START=performance.now();
const fs=require('fs'),path=require('path'),crypto=require('crypto');
const registry=require('./process-registry.cjs');
const {validateEnvelope}=require('./validation.cjs');
const base=path.resolve(__dirname,'..'),repo=path.resolve(base,'../..');
const raw=path.join(base,'raw'),results=path.join(base,'results');
const privateDir=path.dirname(process.env.RESEARCH_PROCESS_REGISTRY);
const SHA='b92773fc3edb949a8a0d6e4a2f60ef2020ee2bd5bf6f8299c1448142a6cd3404';
const pageBase='http://127.0.0.1:8876/research/m31-control-channel-2026-10-16/source/';
const EVENT_CAP=2048,EVENT_BYTES=8192,RAW_TRACE_CAP=3*1024*1024,PUBLIC_TRACE_CAP=2*1024*1024;
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
const check=(ok,message)=>{if(!ok)throw Error(message);};
let browser,page,rawFD,publicFD,expectedFixture,receivedBuffer,phase='admission',substantiveStopped=false;
let hardTimer,workTimer,traceClosed=false,eventCount=0,attemptedEvents=0,rawTraceBytes=0,publicTraceBytes=0;
let droppedEvents=0,truncatedEvents=0,observerExceptions=0,callbackErrors=0,unexpectedRedirects=0,unexpectedApplicationRequests=0;
const requests=new WeakMap(),cdpIDs=new Map(),listeners=[];
let requestCount=0,cdpCount=0;
const ready={playwright:false,cdpNetwork:false,cdpAudits:false,routes:false};
const out={version:1,kind:'synthetic-control-channel-diagnostic',sourceCommit:process.env.RESEARCH_SOURCE_COMMIT,
 sourceFreezeSHA256:null,terminal:false,scope:'One ordinary-heap value returned through the existing automation channel',
 qualified:false,scientificSuccess:false,explainsHistoricalFailure:false,retryPermitted:false,
 browserLaunches:0,evaluateCalls:0,applicationFetchCalls:0,observerReadyEvent:null,browserVersion:null,browserContext:null,
 expected:{bytes:3840,sha256:SHA},errors:[],cleanupErrors:[],protocolDeviations:[],
 evaluation:{settled:false,timedOut:false,deadlineExceeded:false,errorName:null,hostMilliseconds:null},
 returned:{received:false,validationPassed:false,validationError:null,json:null,rejectionProjection:null,bytes:null,sha256:null,exact:false},
 persistence:{attempted:false,opened:false,closed:false,complete:false,writtenBytes:0,writeCalls:0,
   exists:false,bytes:null,sha256:null,exact:false,equalsReturned:false},
 timing:{hostValidationMilliseconds:null,hostPersistenceMilliseconds:null,browserConstructionMilliseconds:null},
 browserClosed:false};
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
  if (value === pageBase + 'browser.js') return 'fixture-script';
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
  if(d.transferID === 'channel-1')p.transferID='channel-1';
  if ('headers' in d) p.headers = publicHeaders(d.headers);
  if ('sha256' in d) p.sha256 = /^[a-f0-9]{64}$/.test(d.sha256) ? d.sha256 : null;
  return p;
}
function record(kind, data = {}) {
  if (traceClosed) { observerExceptions++; return null; }
  if (attemptedEvents >= EVENT_CAP) { droppedEvents++; return null; }
  attemptedEvents++;
  try {
    if (kind.startsWith('control-') || kind.startsWith('persistence-')) data.transferID='channel-1';
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
function guard() { check(!substantiveStopped&&performance.now() - START < 34000, 'Worker substantive deadline'); }
function fileReceipt(filename) {if(!fs.existsSync(filename))return null;const b=fs.readFileSync(filename);return {bytes:b.length,sha256:sha(b)};}
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
  const fd=fs.openSync(path.join(raw,name),'wx');
  try {let offset=0;while(offset<data.length){guard();const n=fs.writeSync(fd,data,offset,data.length-offset);check(n>0,'Returned JSON zero write');offset+=n;}}
  finally{fs.closeSync(fd);}
  return {bytes:data.length,sha256:sha(data)};
}
function persistActualBytes(bytes) {
  guard();check(bytes.length===3840,'Validated received byte length');out.persistence.attempted=true;
  record('persistence-started',{bytes:bytes.length,sha256:sha(bytes)});
  const started=performance.now();let fd;
  try {
    guard();fd=fs.openSync(path.join(raw,'received.bin'),'wx');out.persistence.opened=true;
    while(out.persistence.writtenBytes<bytes.length){guard();
      const n=fs.writeSync(fd,bytes,out.persistence.writtenBytes,bytes.length-out.persistence.writtenBytes);
      check(n>0,'Received binary zero write');out.persistence.writtenBytes+=n;out.persistence.writeCalls++;
      record('persistence-write',{writtenBytes:out.persistence.writtenBytes,writeCalls:out.persistence.writeCalls});
    }
  } finally {
    if(fd!==undefined){fs.closeSync(fd);out.persistence.closed=true;}
    out.timing.hostPersistenceMilliseconds=performance.now()-started;
  }
  out.persistence.complete=out.persistence.closed&&out.persistence.writtenBytes===bytes.length;
  record('persistence-completed',{complete:out.persistence.complete,bytes:out.persistence.writtenBytes,sha256:sha(bytes)});
}
async function main() {
  fs.mkdirSync(raw,{recursive:true});check(fs.readdirSync(raw).length===0,'Fresh raw directory');
  rawFD=fs.openSync(path.join(privateDir,'trace.private.ndjson'),'wx');publicFD=fs.openSync(path.join(raw,'trace.public.ndjson'),'wx');
  check(/^[a-f0-9]{40}$/.test(out.sourceCommit||''),'Published source identity');
  check(Date.now()<Date.parse('2026-10-15T23:00:00Z'),'Original new-launch cutoff');
  const freezeBytes=fs.readFileSync(path.join(base,'freeze.json'));out.sourceFreezeSHA256=sha(freezeBytes);
  check(out.sourceFreezeSHA256===process.env.RESEARCH_REMOTE_VERIFIED_FREEZE,'Verified freeze');
  for(const pin of JSON.parse(freezeBytes).files){const f=path.resolve(repo,pin.path);check(f.startsWith(repo+path.sep),'Contained source pin');
    const b=fs.readFileSync(f);check(b.length===pin.bytes&&sha(b)===pin.sha256,'Frozen source bytes');}
  expectedFixture=fs.readFileSync(path.join(base,'payload.bin'));check(expectedFixture.length===3840&&sha(expectedFixture)===SHA,'Frozen synthetic fixture');
  const runtime=JSON.parse(fs.readFileSync(path.join(base,'runtime-provenance.json')));
  const pw=path.dirname(require.resolve('playwright/package.json')),core=path.dirname(require.resolve('playwright-core/package.json'));
  const runtimeFiles=[process.execPath,path.join(pw,'package.json'),path.join(pw,'index.js'),path.join(core,'package.json'),path.join(core,'index.js'),path.join(core,'lib/coreBundle.js')];
  check(runtime.pins.length===6,'Runtime entry pin count');runtimeFiles.forEach((f,i)=>pinFile(f,runtime.pins[i]));
  const executable=process.env.RESEARCH_CHROME_EXECUTABLE;runtimePins(runtime,executable);out.runtimePinsBefore=true;
  const {chromium}=require('playwright');phase='browser-launch';out.browserLaunches++;
  browser=await chromium.launch({channel:'chrome',executablePath:executable,headless:true,timeout:15000});
  check(registry.hasRegisteredBrowser(),'Registered browser');out.browserVersion=await browser.version();
  check(out.browserVersion==='155.0.8059.80','Browser version');runtimePins(runtime,executable);out.runtimePinsAfter=true;
  page=await browser.newPage();page.setDefaultTimeout(15000);armPage();await armCDP();
  for(const [name,type]of [['browser.html','text/html'],['browser.js','application/javascript']]){
    const bytes=fs.readFileSync(path.join(__dirname,name));await page.route(pageBase+name,route=>route.fulfill({status:200,contentType:type,body:bytes}));
  }ready.routes=true;
  out.observerReadyEvent=record('observers-ready');check(out.observerReadyEvent,'Observer readiness retained');
  phase='navigation';await page.goto(pageBase+'browser.html');
  check(droppedEvents===0&&truncatedEvents===0&&observerExceptions===0&&callbackErrors===0,'Pre-evaluate trace health');
  phase='evaluate-started';guard();
  check(out.evaluateCalls===0&&Object.values(ready).every(Boolean),'Sole observed payload evaluation');
  check(record('control-evaluate-started')!==null,'Retained evaluate boundary');
  const evaluationStart=performance.now();let actual;
  try {
    out.evaluateCalls++;
    actual=await bounded(page.evaluate(()=>window.runControlChannelPayload()),10000,'ControlEvaluateDeadline');
    out.evaluation.settled=true;out.returned.received=true;phase='evaluate-returned';
    record('control-evaluate-returned',{callMilliseconds:performance.now()-evaluationStart});
  } catch(error) {
    out.evaluation.timedOut=error.message==='ControlEvaluateDeadline';
    out.evaluation.settled=!out.evaluation.timedOut;out.evaluation.errorName=safeWord(error.name);
    record('control-evaluate-error',{errorName:error.name,errorMessage:error.message});
    phase=out.evaluation.timedOut?'evaluate-timeout':'evaluate-rejected';
    if(out.evaluation.timedOut)out.protocolDeviations.push('evaluate-timeout-not-cancellation');
    if(performance.now()-evaluationStart>=10000){out.evaluation.deadlineExceeded=true;out.protocolDeviations.push('evaluate-deadline-overrun');}
    return; // Never persist or make another extraction after failed/expired evaluate.
  } finally {out.evaluation.hostMilliseconds=performance.now()-evaluationStart;}
  if(out.evaluation.hostMilliseconds>=10000){out.evaluation.deadlineExceeded=true;out.protocolDeviations.push('evaluate-deadline-overrun');phase='evaluate-deadline-overrun';return;}
  guard();phase='validate-returned-envelope';const validationStart=performance.now();let validated;
  try {validated=validateEnvelope(actual);out.returned.validationPassed=true;}
  catch(error){out.returned.validationError=safeWord(error.code||error.name);
    // Deliberately retain no unvalidated arbitrary strings or nested values publicly.
    const projection={kind:'rejected-decoded-return-projection',errorCode:out.returned.validationError,
      rootType:actual===null?'null':typeof actual,rootIsArray:Array.isArray(actual),originalRetained:false};
    out.returned.rejectionProjection=writeReturnedJSON(Buffer.from(JSON.stringify(projection)+'\n'),'rejected-return.json');
    throw error;}
  finally{out.timing.hostValidationMilliseconds=performance.now()-validationStart;}
  guard();
  phase='retain-returned-envelope';
  out.returned.json=writeReturnedJSON(Buffer.from(validated.json,'utf8'));
  // Validation above rejects holes, coercible values, floats, nulls and overflows.
  guard();phase='convert-returned-values';
  receivedBuffer=Buffer.from(actual.values);
  out.returned.bytes=receivedBuffer.length;out.returned.sha256=sha(receivedBuffer);out.returned.exact=receivedBuffer.equals(expectedFixture);
  out.browserContext={originLabel:actual.origin==='http://127.0.0.1:8876'?'page-origin':'opaque-null',isSecureContext:actual.isSecureContext};
  if(actual.origin!=='http://127.0.0.1:8876')out.protocolDeviations.push('effective-origin-mismatch');
  out.timing.browserConstructionMilliseconds=actual.browserConstructionMilliseconds;
  record('control-envelope-validated',{valid:true,jsonBytes:validated.jsonBytes,bytes:receivedBuffer.length,sha256:out.returned.sha256,exact:out.returned.exact});
  phase='persist-returned-bytes';persistActualBytes(receivedBuffer);phase='persistence-returned';
}
async function cleanup() {
  if(browser){try{await bounded(browser.close(),3000,'Browser close deadline');out.browserClosed=true;}
    catch(error){out.cleanupErrors.push({stage:'browser-close',type:safeWord(error.name)});}}
  else out.browserClosed=out.browserLaunches===0;
  const received=path.join(raw,'received.bin');
  if(fs.existsSync(received)){const b=fs.readFileSync(received);out.persistence.exists=true;out.persistence.bytes=b.length;out.persistence.sha256=sha(b);
    out.persistence.exact=expectedFixture?b.equals(expectedFixture):false;out.persistence.equalsReturned=receivedBuffer?b.equals(receivedBuffer):false;}
  if(unexpectedApplicationRequests>0)out.protocolDeviations.push('unexpected-application-network-request');
  record('cleanup-finished',{complete:out.cleanupErrors.length===0&&out.browserClosed});
  out.lastPhase=phase;
  for(const {emitter,name,listener}of listeners)emitter.removeListener(name,listener);
  traceClosed=true;for(const fd of [rawFD,publicFD])if(fd!==undefined)fs.closeSync(fd);
  out.instrumentation={ready,eventCount,attemptedEvents,eventCap:EVENT_CAP,droppedEvents,truncatedEvents,observerExceptions,callbackErrors,
    collectionBeforeEvaluate:out.evaluateCalls===0||out.observerReadyEvent!==null,captureClosedAfterCleanup:true,
    unexpectedRedirectObservations:unexpectedRedirects,unexpectedApplicationRequestObservations:unexpectedApplicationRequests,
    complete:Object.values(ready).every(Boolean)&&droppedEvents===0&&truncatedEvents===0&&observerExceptions===0&&callbackErrors===0&&unexpectedRedirects===0&&unexpectedApplicationRequests===0,
    clock:'worker-monotonic-receipt',browserClock:'browser-performance-independent',crossClockOrderingClaimed:false};
  out.trace={public:fileReceipt(path.join(raw,'trace.public.ndjson')),private:fileReceipt(path.join(privateDir,'trace.private.ndjson'))};
  const complete=out.instrumentation.complete&&out.cleanupErrors.length===0&&out.errors.length===0&&out.protocolDeviations.length===0&&out.browserClosed&&out.evaluation.settled;
  out.localObservationComplete=complete;
  out.status=!complete?'incomplete':!out.returned.received?'control-return-failed':
    out.persistence.complete&&out.persistence.equalsReturned?(out.persistence.exact?'synthetic-control-transfer-complete':'received-content-mismatch'):'persistence-failed';
  out.terminal=true;out.elapsedSeconds=(performance.now()-START)/1000;check(out.elapsedSeconds<40,'Worker including cleanup limit');
  const data=Buffer.from(JSON.stringify(out,null,2)+'\n');check(data.length<=65536,'Result byte cap');
  const fd=fs.openSync(path.join(results,'result.json'),'wx');try{check(fs.writeSync(fd,data)===data.length,'Complete worker result');}finally{fs.closeSync(fd);}
  const summary=Buffer.from(JSON.stringify({kind:'synthetic-control-channel-worker-summary',status:out.status,terminal:true,qualified:false,resultBytes:data.length,resultSHA256:sha(data)})+'\n');
  check(fs.writeSync(1,summary)===summary.length,'Complete worker summary');process.exitCode=complete?0:1;
}
hardTimer=setTimeout(()=>process.exit(124),40000);
workTimer=setTimeout(()=>{substantiveStopped=true;fail(Error('Worker substantive deadline'),'deadline');if(page)page.close().catch(()=>{});},34000);
main().catch(error=>fail(error,phase)).finally(async()=>{clearTimeout(workTimer);try{await cleanup();}catch(error){process.exitCode=1;
  try{fs.writeSync(2,Buffer.from(JSON.stringify({kind:'worker-finalization-failed',type:safeWord(error.name)})+'\n'));}catch(_){}}
  finally{hardTimer.unref();}});
