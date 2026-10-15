'use strict';
// Inert scientific worker until invoked by the one-shot external supervisor.
// This source is not permission to rerun a terminal campaign.
const fs=require('fs'),path=require('path'),crypto=require('crypto'),http=require('http');
const registry=require('./process-registry.cjs'),{chromium}=require('playwright');
const base=path.resolve(__dirname,'..'),repo=path.resolve(base,'../..'),raw=path.join(base,'raw');
const cfg=JSON.parse(fs.readFileSync(path.join(base,'config.json'))),limit=cfg.limits,start=performance.now();
const source=process.env.RESEARCH_SOURCE_COMMIT,sha=b=>crypto.createHash('sha256').update(b).digest('hex');
let browser,page,sink,rawBytes=0,checks=0,context='start',activeSinkWrites=0;
const faults=[],privateErrors=[],counts={},sinkReservations=new Map(),sinkSockets=new Set();
const out={sourceCommit:source,scope:cfg.scope,cases:[],counts,qualified:false,terminal:false};
function clean(s){return String(s).split('\n')[0].replace(/\/(?:Users|private|var|tmp|Volumes|Applications|Library|opt|usr|System)\/[^\s"'<>]*/g,'[local-path]').replace(/http:\/\/127\.0\.0\.1:\d+\/evidence\/[^\s"'<>]*/g,'[private-local-sink]').replace(/--user-data-dir=\S+/g,'[private-profile]').replace(/\b(?:pid|PID|pgid)\s*[=:]\s*\d+/g,'[private-process]').slice(0,512);}
function publicValue(v){if(typeof v==='string')return clean(v);if(Array.isArray(v))return v.map(publicValue);if(v&&typeof v==='object')return Object.fromEntries(Object.entries(v).map(([k,x])=>[k,publicValue(x)]));return v;}
function assert(ok,message,detail){checks++;if(!ok){const e=Error(message);e.detail=detail;throw e;}}
function guard(){assert(performance.now()-start<1000*limit.cooperativeWallSeconds,'Cooperative science wall cap');assert(faults.length===0,'Browser or evidence sink failure',faults.slice(0,16));}
function charge(name,n=1){guard();assert(Number.isSafeInteger(n)&&n>=0,'Counter shape');assert(name in cfg.workLimits,'Unreserved work counter '+name);counts[name]=(counts[name]??0)+n;assert(counts[name]<=cfg.workLimits[name],'Work cap '+name,{actual:counts[name],cap:cfg.workLimits[name]});}
function bytes(x){if(Buffer.isBuffer(x))return x;if(x instanceof ArrayBuffer)return Buffer.from(x);if(ArrayBuffer.isView(x))return Buffer.from(x.buffer,x.byteOffset,x.byteLength);throw Error('Typed binary evidence required');}
function write(name,value,reserve=false){
 assert(/^[A-Za-z0-9][A-Za-z0-9._-]*$/.test(name),'Evidence filename');const b=typeof value==='object'&&!Buffer.isBuffer(value)&&!ArrayBuffer.isView(value)&&!(value instanceof ArrayBuffer)?Buffer.from(JSON.stringify(value,null,2)+'\n'):bytes(value);
 assert(rawBytes+b.length<=limit.rawBytes-(reserve?0:limit.failureReserveBytes),'Raw evidence cap');fs.writeFileSync(path.join(raw,name),b,{flag:'wx'});rawBytes+=b.length;return {name,bytes:b.length,sha256:sha(b)};
}
async function deadline(p,ms,label){let timer;try{return await Promise.race([p,new Promise((_,reject)=>{timer=setTimeout(()=>reject(Error(label+' deadline')),ms);})]);}finally{clearTimeout(timer);}}
function preserveError(label,e){privateErrors.push({label,name:e?.name,message:e?.message??String(e),stack:e?.stack,detail:e?.detail});}
async function openSink(){
 const token=crypto.randomBytes(24).toString('hex'); // Private transport nonce; never used for numerical inputs.
 sink=http.createServer((req,res)=>{
  const headers={'Access-Control-Allow-Origin':'http://127.0.0.1:8876','Access-Control-Allow-Methods':'POST, OPTIONS','Access-Control-Allow-Headers':'Content-Type','Cache-Control':'no-store'};
  if(req.method==='OPTIONS'){res.writeHead(204,headers);res.end();return;}
  const reservation=sinkReservations.get(req.url);
  if(req.method!=='POST'||!reservation||reservation.started){res.writeHead(409,headers);res.end();return;}
  reservation.started=true;activeSinkWrites++;
  const target=path.join(raw,reservation.name);let fd,received=0,closed=false,failed=false;const hash=crypto.createHash('sha256');
  const finish=()=>{if(closed)return;closed=true;activeSinkWrites--;if(fd!==undefined){fs.closeSync(fd);fd=undefined;}};
  const fail=e=>{if(failed)return;failed=true;preserveError('binary-sink',e);faults.push('Evidence sink write failed');reservation.errorType=e.name;reservation.bytes=received;finish();if(!res.headersSent)res.writeHead(500,headers);res.end(JSON.stringify({complete:false,bytes:received}));req.destroy();};
  try{assert(Number(req.headers['content-length'])===reservation.size,'Sink declared byte shape');assert(rawBytes+reservation.size<=limit.rawBytes-limit.failureReserveBytes,'Sink raw reservation cap');fd=fs.openSync(target,'wx');}
  catch(e){fail(e);return;}
  req.on('data',chunk=>{if(failed)return;try{assert(received+chunk.length<=reservation.size,'Sink excess bytes');assert(rawBytes+chunk.length<=limit.rawBytes-limit.failureReserveBytes,'Sink byte cap');let offset=0;while(offset<chunk.length){const n=fs.writeSync(fd,chunk,offset,chunk.length-offset);assert(n>0,'Sink zero-length successful write');hash.update(chunk.subarray(offset,offset+n));offset+=n;received+=n;rawBytes+=n;}}catch(e){fail(e);}});
  req.on('end',()=>{if(failed)return;try{assert(received===reservation.size,'Sink truncated body');finish();reservation.complete=true;reservation.bytes=received;reservation.sha256=hash.digest('hex');res.writeHead(200,{...headers,'Content-Type':'application/json'});res.end(JSON.stringify({complete:true,bytes:received,sha256:reservation.sha256}));}catch(e){fail(e);}});
  req.on('error',fail);req.on('aborted',()=>fail(Error('Sink request aborted')));
 });
 sink.on('connection',socket=>{sinkSockets.add(socket);socket.on('close',()=>sinkSockets.delete(socket));});
 await new Promise((resolve,reject)=>{sink.once('error',reject);sink.listen(0,'127.0.0.1',resolve);});
 const port=sink.address().port;
 return (key,name,size)=>{
  const file=key+'-gpu-'+name+'.u32',urlPath='/evidence/'+token+'/'+file;
  assert(!sinkReservations.has(urlPath),'Unique binary sink');sinkReservations.set(urlPath,{name:file,size,started:false,complete:false});
  return {sinkURL:'http://127.0.0.1:'+port+urlPath,reservation:sinkReservations.get(urlPath)};
 };
}
async function runBatch(key,entry,count,inputBuffers,outputShapes,reserveSink){
 guard();context='GPU '+key;charge('gpuDispatches');charge('gpuActiveInvocations',count);charge('gpuLaunchedInvocations',64*Math.ceil(count/64));
 const reservations=[],input={key,entry,count,groups:Math.ceil(count/64),timeoutMs:limit.gpuBatchTimeoutMilliseconds,
  inputs:inputBuffers.map(([binding,name,b])=>({binding,name,base64:bytes(b).toString('base64')})),
  outputs:outputShapes.map(([binding,name,size])=>{const s=reserveSink(key,name,size);reservations.push(s.reservation);return {binding,name,size,sinkURL:s.sinkURL};})};
 const result=await deadline(page.evaluate(input=>window.runBodyBatch(input),input),limit.gpuBatchTimeoutMilliseconds+5000,'Complete GPU batch');
 write(key+'-gpu-api.json',publicValue(result)); // No transport addresses enter this report.
 for(const r of reservations)assert(r.complete&&r.bytes===r.size,'Complete persisted raw readback',{name:r.name,complete:r.complete,bytes:r.bytes,expected:r.size});
 assert(!result.error&&!result.validation&&!result.health.loss&&!result.health.uncaptured&&result.dispatch.completed,'GPU API gate',result);
 assert(result.after.liveBufferBytes===0&&result.allocated.every(x=>x.destroyed),'Batch release before API snapshot',result);
 assert(result.dispatch.entry===entry&&result.dispatch.count===count&&result.dispatch.groups===input.groups,'Dispatch identity');guard();
 return Object.fromEntries(outputShapes.map(([,name],i)=>[name,fs.readFileSync(path.join(raw,reservations[i].name))]));
}
function savePrepared(key,p,constantWords){
 assert(bytes(p.originalStates).equals(fs.readFileSync(path.join(raw,key+'-originalStates.f64'))),'Prepared original-state identity');
 for(const name of ['candidatePrepared','referencePrepared','decodedPrepared'])write(key+'-'+name+'.f64',bytes(p[name]));
 for(const [name,b]of Object.entries(p.packed))write(key+'-packed-'+name+'.u32',bytes(b));
 write(key+'-packed-constants.u32',bytes(constantWords));write(key+'-admission.json',p.admission);
}
function saveReference(key,r){if(r.policy)write(key+'-policy.u16',bytes(r.policy));write(key+'-output.bin',bytes(r.output));write(key+'-status.json',{status:r.status,completed:r.completed,counters:r.counters,failure:r.failure??null});}
function savePartial(key,error){if(error.partial){try{if(error.partial.buffers){for(const [name,b]of Object.entries(error.partial.buffers))if(b)write(key+'-partial-'+name+'.bin',bytes(b),true);write(key+'-partial-status.json',publicValue({kind:error.partial.kind,metadata:error.partial.metadata}),true);}else saveReference(key+'-partial',error.partial);}catch(e){preserveError('partial-evidence',e);}}}
(async()=>{
 assert(/^[a-f0-9]{40}$/.test(source??''),'Published source identity required');assert(Date.now()<Date.parse(cfg.stopNewLaunchUTC),'Overnight launch cutoff');
 fs.mkdirSync(raw,{recursive:true});assert(fs.readdirSync(raw).length===0,'No prior raw evidence');
 const freezeBytes=fs.readFileSync(path.join(base,'freeze.json')),freeze=JSON.parse(freezeBytes);
 assert(process.env.RESEARCH_REMOTE_VERIFIED_FREEZE===sha(freezeBytes),'Independent remote freeze receipt required');
 for(const p of freeze.files){const f=path.resolve(repo,p.path);assert(f.startsWith(repo+path.sep),'Contained freeze pin');const b=fs.readFileSync(f);assert(b.length===p.bytes&&sha(b)===p.sha256,'Frozen source mismatch',{path:p.path});}
 const runtime=JSON.parse(fs.readFileSync(path.join(base,'runtime-provenance.json'))),pw=path.dirname(require.resolve('playwright/package.json')),core=path.dirname(require.resolve('playwright-core/package.json'));
 for(const [i,f]of [process.execPath,path.join(pw,'package.json'),path.join(pw,'index.js'),path.join(core,'package.json'),path.join(core,'index.js'),path.join(core,'lib/coreBundle.js')].entries()){const b=fs.readFileSync(f),p=runtime.pins[i];assert(b.length===p.bytes&&sha(b)===p.sha256,'Runtime entry mismatch',{label:p.label});}
 write('started.json',{sourceCommit:source,freezeSha256:sha(freezeBytes),scope:cfg.scope,config:cfg,node:process.version,platform:process.platform,architecture:process.arch,runtimePinsVerified:runtime.pins});
 const h=require('./host.cjs'),generator=require('./generator.cjs');
 charge('constantSetups');const C=h.createConfig();write('scientific-constants-and-gates.json',C);
 context='fixed controls construction';charge('controlBuilds');let controls;try{controls=h.buildControls(C,{guard,charge});}catch(e){savePartial('controls-build',e);throw e;} // No reference solves in construction.
 write('control-metadata.json',{pairs:{count:controls.pairs.count,expected:controls.pairs.expected},roots:{count:controls.roots.count,definitions:controls.roots.definitions}});write('control-host-only-spec.json',controls.hostOnly);
 for(const name of ['pairs','roots']){write('controls-'+name+'-input.u32',bytes(controls[name].input));write('controls-'+name+'-original.f64',bytes(controls[name].original));}
 // Explicitly reserved reference work; controls assessment itself never solves roots.
 charge('controlReferenceCalls');let controlReferences;try{controlReferences=h.runControlsReference(controls,C,{guard,charge});}catch(e){savePartial('controls-reference',e);throw e;}
 write('controls-reference-pairs.json',controlReferences.pairs);
 for(const name of ['R','Q'])write('controls-reference-'+name+'-roots.bin',bytes(controlReferences.roots[name]));
 write('controls-reference-status.json',{completed:controlReferences.completed,pass:controlReferences.pass,status:controlReferences.status,counters:controlReferences.counters,failure:controlReferences.failure??null});
 assert(controlReferences.completed&&controlReferences.pass,'Control reference completion/quality',controlReferences.failure);
 charge('hostOnlyCalls');let hostOnly;try{hostOnly=h.runHostOnlyControls(controls,C,{guard,charge});}catch(e){savePartial('controls-host-only',e);throw e;}write('controls-host-only-result.json',hostOnly);assert(hostOnly.completed&&hostOnly.pass,'Host admission/decoder control premise',hostOnly);
 context='browser initialization';browser=await chromium.launch({channel:'chrome',headless:true,timeout:15000});assert(registry.hasRegisteredBrowser(),'Registered browser ownership');
 out.browserVersion=await browser.version();assert(out.browserVersion===runtime.chromeBundleVersion,'Frozen browser version');write('process-registration-summary.json',registry.summary());
 page=await browser.newPage();page.setDefaultTimeout(15000);page.on('pageerror',e=>faults.push(clean(e.message)));page.on('console',m=>{if(m.type()==='error')faults.push(clean(m.text()));});
 const url='http://127.0.0.1:8876/research/m31-body-load-2026-10-16/source/',served=[];
 for(const [name,type]of [['browser.html','text/html'],['browser.js','application/javascript'],['body.wgsl','text/plain']]){
  const b=fs.readFileSync(path.join(__dirname,name));await page.route(url+name,route=>{served.push({name,bytes:b.length,sha256:sha(b)});return route.fulfill({status:200,contentType:type,body:b});});
 }
 write('served-source-contract.json',{method:'Exact frozen local bytes supplied through Playwright routes',files:['browser.html','browser.js','body.wgsl'].map(name=>{const b=fs.readFileSync(path.join(__dirname,name));return {name,bytes:b.length,sha256:sha(b)};})});
 const reserveSink=await openSink();await page.goto(url+'browser.html');await page.waitForFunction(()=>window.bodyRunnerReady===true);
 const capability=await deadline(page.evaluate(()=>window.initializeBody()),20000,'GPU initialization');
 if(capability.shader){assert(sha(Buffer.from(capability.shader))===sha(fs.readFileSync(path.join(__dirname,'body.wgsl'))),'Served shader identity');delete capability.shader;}
 write('capability.json',{browserVersion:out.browserVersion,...capability});out.capability=capability;
 assert(capability.supported&&capability.compiled&&!capability.validation&&!capability.loss&&!capability.uncaptured,'GPU admission/compilation',capability);
 const controlGPU={};
 for(const kind of ['pairs','roots']){
  const count=kind==='pairs'?15:146,constants=Uint32Array.from(C.packedConstants);constants[20]=count;
  write('controls-'+kind+'-constants.u32',bytes(constants));
  controlGPU[kind]=await runBatch('controls-'+kind,kind==='pairs'?'controlPairs':'controlRoots',count,[[0,'constants',constants],[6,'controls',controls[kind].input]],[[7,'output',256*count]],reserveSink);
 }
 // Handoff control roots are a separate reserved numerical call after raw GPU persistence.
 charge('controlHandoffCalls');let controlH;try{controlH=h.runControlHandoff(controlGPU.roots.output,controls,C,{guard,charge});}catch(e){savePartial('controls-handoff',e);throw e;}
 write('controls-handoff-output.bin',bytes(controlH.output));write('controls-handoff-status.json',{completed:controlH.completed,pass:controlH.pass,status:controlH.status,counters:controlH.counters,failure:controlH.failure??null});
 assert(controlH.completed&&controlH.pass,'Control handoff completion/quality',controlH.failure);
 charge('controlAssessments');try{out.controls=h.assessControls({controls,references:controlReferences,GPU:{pairs:controlGPU.pairs.output,roots:controlGPU.roots.output},H:controlH,hostOnly},C,{guard,charge});}catch(e){savePartial('controls-assessment',e);throw e;}write('control-assessment.json',out.controls);assert(out.controls.pass,'Shared control gate',out.controls);
 for(const familyID of [1,2,3,4]){
  const key='family-'+familyID;context=key+' input generation';charge('freshFamilyGenerations');
  let generated;try{generated=generator.generateFamily(familyID,{guard,charge});}catch(e){savePartial(key,e);throw e;}write(key+'-generator-audit.json',generated.audit);
  write(key+'-originalStates.f64',Float64Array.from(generated.states.flat()));
  for(const name of ['permutation','inversePermutation','designatedReceiverIds','designatedSourceIds','coreFlags','permutationDigests'])if(generated[name])write(key+'-'+name+'.bin',bytes(generated[name]));
  charge('preparations');let p;try{p=h.prepare(generated.states,C,{guard,charge});}catch(e){savePartial(key,e);throw e;}const constants=Uint32Array.from(C.packedConstants);constants[20]=p.N;savePrepared(key,p,constants);
  const local={familyID,key,N:p.N,qualified:false};out.cases.push(local);
  charge('referenceCalls');charge('reservedReferencePairs',p.N*p.N);let R;
  try{R=h.runReference(p,'R',C,{guard,charge});}catch(e){savePartial(key+'-R',e);throw e;}saveReference(key+'-R',R);assert(R.completed,'Original reference completion',R.failure);
  charge('referenceCalls');charge('reservedReferencePairs',p.N*p.N);let Q;
  try{Q=h.runReference(p,'Q',C,{guard,charge});}catch(e){savePartial(key+'-Q',e);throw e;}saveReference(key+'-Q',Q);assert(Q.completed,'Decoded reference completion',Q.failure);
  charge('inputAssessments');local.stimulus=h.assessStimulus({generated,prepared:p,R,Q},C,{guard,charge});write(key+'-stimulus.json',local.stimulus);assert(local.stimulus.pass,'Input/exposure/reference-quality premise',local.stimulus);
  charge('reservedGpuPairs',p.N*p.N);
  const GPU=await runBatch(key,'mainBody',p.N,[[0,'constants',constants],[1,'nodes',p.packed.nodes],[2,'offsets',p.packed.offsets],[3,'motors',p.packed.motors]],[[4,'policy',4*p.N*p.N],[5,'output',256*p.N]],reserveSink);
  charge('handoffCalls');let H;try{H=h.runHandoff(GPU.output,p,C,{guard,charge});}catch(e){savePartial(key+'-H',e);throw e;}saveReference(key+'-H',H);assert(H.completed,'Actual-handoff reference completion',H.failure);
  charge('mainAssessments');try{local.assessment=h.assess({prepared:p,R,Q,GPU,H,designatedReceiverIds:generated.designatedReceiverIds},C,{guard,charge});}catch(e){savePartial(key+'-assessment',e);throw e;}write(key+'-assessment.json',local.assessment);
  assert(local.assessment.integrityPass,'Main evidence/validity premise',local.assessment);local.qualified=local.assessment.pass;
  // A numerical policy/output discrepancy is retained; remaining independently
  // reserved families still execute. Invalid/incomplete evidence terminates.
  local.status=local.qualified?'qualified':'completed-numerical-failure';write(key+'-disposition.json',local);
 }
 const health=await page.evaluate(()=>window.bodyHealth());write('final-gpu-health.json',health);assert(!health.loss&&!health.uncaptured&&health.costs.liveBufferBytes===0,'Final GPU health');
 out.costs=health.costs;out.servedSources=served;
 for(const [name,value]of Object.entries(cfg.expectedGPUCosts))assert(health.costs[name]===value,'Complete GPU cost ledger '+name,{expected:value,observed:health.costs[name]});
 out.qualified=out.cases.length===4&&out.cases.every(x=>x.qualified);out.invocationComplete=true;out.status='completed-feasibility-comparison';out.decision=out.qualified?'finite-body-load-feasibility-supported-pending-review':'required-feasibility-gates-not-met';
})().catch(async e=>{
 preserveError(context,e);out.status='failed';out.error=publicValue({name:e.name,message:e.message,detail:e.detail});out.context=context;out.qualified=false;process.exitCode=1;
 if(page){try{write('browser-failure-evidence.json',publicValue(await deadline(page.evaluate(()=>({initialization:window.bodyInitializationEvidence??null,dispatch:window.lastBodyDispatch??null,health:window.bodyHealth?.()??null})),1000,'Failure evidence')),true);}catch(x){preserveError('failure-evidence',x);}}
}).finally(async()=>{
 const cleanup=[];
 if(page){try{out.gpuShutdown=await deadline(page.evaluate(()=>window.shutdownBody?.()),1500,'GPU shutdown');}catch(e){preserveError('GPU-cleanup',e);cleanup.push(clean(e.message));}}
 if(browser){try{await deadline(browser.close(),3000,'Browser close');}catch(e){preserveError('browser-cleanup',e);cleanup.push(clean(e.message));}}
 if(sink){try{for(const socket of sinkSockets)socket.destroy();await deadline(new Promise(resolve=>sink.close(resolve)),1000,'Evidence sink close');}catch(e){preserveError('sink-cleanup',e);cleanup.push(clean(e.message));}}
 out.sinkClosure={activeWrites:activeSinkWrites,reservations:[...sinkReservations.values()].map(x=>({...x})),closed:!sink?.listening};
 if(activeSinkWrites!==0)cleanup.push('Evidence sink write still active');
 if(cleanup.length){out.cleanupErrors=cleanup;out.qualified=false;out.status='failed-cleanup';process.exitCode=1;}
 if(privateErrors.length){try{const b=Buffer.from(JSON.stringify(privateErrors,null,2)+'\n');fs.writeFileSync(process.env.RESEARCH_PROCESS_REGISTRY+'.errors.json',b,{flag:'wx'});out.privateErrorReceipt={bytes:b.length,sha256:sha(b),disclosure:'Full exceptions retained privately; public first-line errors redact local paths, profiles, transport nonce and process identities.'};}catch(e){out.privateErrorReceipt={written:false,errorType:e.name};}}
 out.checks=checks;out.elapsedSeconds=(performance.now()-start)/1000;out.terminal=true;
 out.files=fs.existsSync(raw)?fs.readdirSync(raw).sort().map(name=>{const b=fs.readFileSync(path.join(raw,name));return {name,bytes:b.length,sha256:sha(b)};}):[];
 try{write('result.json',out,true);fs.writeFileSync(path.join(base,'results/result.json'),JSON.stringify(out,null,2)+'\n',{flag:'wx'});}catch(e){process.exitCode=1;console.error('Terminal evidence write failed: '+clean(e.message));}
 console.log(JSON.stringify({status:out.status,qualified:out.qualified,decision:out.decision,error:out.error,counts,elapsedSeconds:out.elapsedSeconds,rawBytes}));
});
