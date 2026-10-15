'use strict';
// All scientific preparation/evaluation is inside the sole supervised invocation.
const fs=require('fs'),path=require('path'),crypto=require('crypto'),registry=require('./process-registry.cjs');
const {chromium}=require('playwright');
const base=path.resolve(__dirname,'..'),repo=path.resolve(base,'../..'),raw=path.join(base,'raw'),cfg=JSON.parse(fs.readFileSync(path.join(base,'config.json'))),limit=cfg.limits,start=performance.now();
const sha=b=>crypto.createHash('sha256').update(b).digest('hex'),source=process.env.RESEARCH_SOURCE_COMMIT;
let browser,page,rawBytes=0,checks=0,context={},counts={dispatches:0,gpuControlSlots:0,gpuPairSlots:0,gpuSumSlots:0,roots:0,integrationSteps:0},out={sourceCommit:source,scope:cfg.scope,config:cfg,counts};
const faults=[];
function assert(ok,message,detail){checks++;if(!ok){const e=Error(message);e.detail=detail;throw e;}}
function guard(){if(performance.now()-start>=1000*limit.cooperativeWallSeconds)throw Error('Cooperative wall cap');}
function charge(name,amount=1){guard();assert(Number.isSafeInteger(amount)&&amount>=0,'Counter increment');assert(name in limit,'Unknown counter '+name);counts[name]=(counts[name]??0)+amount;assert(counts[name]<=limit[name],'Operation cap '+name,{actual:counts[name],cap:limit[name]});}
function write(name,data,failure=false){const bytes=Buffer.isBuffer(data)?data:Buffer.from(JSON.stringify(data,null,2)+'\n');assert(rawBytes+bytes.length<=limit.rawBytes-(failure?0:limit.failureReserveBytes),'Evidence byte cap');fs.writeFileSync(path.join(raw,name),bytes,{flag:'wx'});rawBytes+=bytes.length;}
async function deadline(promise,ms,label){let timer;try{return await Promise.race([promise,new Promise((_,reject)=>{timer=setTimeout(()=>reject(Error(label+' timeout')),ms);})]);}finally{clearTimeout(timer);}}
function assess(stage,fn){
 guard();const reserved=cfg.assessmentReservations[stage];assert(reserved,'Known assessment stage');
 for(const [name,n]of Object.entries(reserved)){const key='assessmentReserved:'+name;counts[key]=(counts[key]??0)+n;assert(counts[key]<=cfg.assessmentLimits[name],'Assessment reservation cap '+name);}
 const result=fn();write(stage+'-assessment.json',result);
 for(const [name,n]of Object.entries(result.counts??{})){assert(name in reserved&&Number.isSafeInteger(n)&&n>=0&&n<=reserved[name],'Assessment actual cap '+name,{stage,n});const key='assessmentActual:'+name;counts[key]=(counts[key]??0)+n;assert(counts[key]<=cfg.assessmentLimits[name],'Aggregate assessment cap '+name);}
 guard();return result;
}
async function dispatch(kind){
 guard();context={phase:'GPU '+kind};charge('dispatches',1);charge('gpuLaunchedInvocations',kind==='terms'?80000:64);charge('gpuPaddingInvocations',kind==='terms'?0:48);if(kind==='reduce')charge('gpuSumReadReservation',80000);charge({controls:'gpuControlSlots',terms:'gpuPairSlots',reduce:'gpuSumSlots'}[kind],{controls:16,terms:80000,reduce:16}[kind]);
 return deadline((async()=>{const r=await page.evaluate(async({kind,ms})=>window.dispatchWake(kind,ms),{kind,ms:limit.gpuBatchTimeoutMilliseconds});
 const bytes=Buffer.from(r.base64,'base64');write(kind+'-gpu.u32',bytes);write(kind+'-readback.json',{bytes:r.bytes,dispatch:r.dispatch});
 const api=await page.evaluate(()=>window.finishWakeBatch());write(kind+'-api.json',api);assert(!api.validation&&!api.loss&&!api.uncaptured,'GPU API qualification',api);
 assert(bytes.length===({controls:1280,terms:6400000,reduce:512}[kind])&&r.bytes===bytes.length,'GPU byte coverage');assert(r.dispatch.submitted&&r.dispatch.kind===kind&&r.dispatch.count===({controls:16,terms:80000,reduce:16}[kind])&&r.dispatch.groups===(kind==='terms'?1250:1)&&r.dispatch.outputBytes===bytes.length,'GPU dispatch accounting',r.dispatch);return bytes;
 })(),limit.gpuBatchTimeoutMilliseconds,'Complete GPU '+kind);
}
function savePrepared(label,p,h){write(label+'-nodes.f64',h.encodeF64(p.nodes));write(label+'-offsets.f64',h.encodeF64(p.offsets));write(label+'-axis-metrics.f64',h.encodeF64(p.axisMetrics));write(label+'-constants.f64',h.encodeF64(p.constants));write(label+'-ids.u32',h.encodeU32(p.ids));}
function saveReference(label,r,h){for(const k of ['scalars','terms','ordinarySums','compensatedSums'])write(label+'-'+k+'.f64',h.encodeF64(r[k]));write(label+'-metadata.u32',h.encodeU32(r.metadata));write(label+'-codes.u8',Buffer.from(r.codes));write(label+'-sumValidity.u8',Buffer.from(r.sumValidity));write(label+'-counts.json',{complete:r.complete,counts:r.counts,failure:r.failure??null});}
(async()=>{
 assert(typeof source==='string'&&/^[a-f0-9]{40}$/.test(source),'Published source identity required');assert(Date.now()<Date.parse(cfg.stopNewLaunchUTC),'Overnight launch cutoff');
 fs.mkdirSync(raw,{recursive:true});assert(fs.readdirSync(raw).length===0,'No earlier scientific output allowed');
 const freezeBytes=fs.readFileSync(path.join(base,'freeze.json')),freeze=JSON.parse(freezeBytes);
 for(const pin of freeze.files){const file=path.resolve(repo,pin.path);assert(file.startsWith(repo+path.sep),'Contained source path');const b=fs.readFileSync(file);assert(b.length===pin.bytes&&sha(b)===pin.sha256,'Frozen input/source mismatch',{path:pin.path});}
 const runtime=JSON.parse(fs.readFileSync(path.join(base,'runtime-provenance.json'))),pw=path.dirname(require.resolve('playwright/package.json')),core=path.dirname(require.resolve('playwright-core/package.json'));
 for(const [i,file]of [process.execPath,path.join(pw,'package.json'),path.join(pw,'index.js'),path.join(core,'package.json'),path.join(core,'index.js'),path.join(core,'lib/coreBundle.js')].entries()){const b=fs.readFileSync(file),p=runtime.pins[i];assert(b.length===p.bytes&&sha(b)===p.sha256,'Frozen runtime entry mismatch',{label:p.label});}
 write('started.json',{sourceCommit:source,freezeSha256:sha(freezeBytes),config:cfg,node:process.version,platform:process.platform,architecture:process.arch,runtimePinsVerified:runtime.pins});
 const h=require('./host.cjs'),selection=JSON.parse(fs.readFileSync(path.join(base,'selection/selection.json')));assert(sha(fs.readFileSync(path.join(base,'selection/selection.json')))===cfg.selectionSha256,'Selection identity');assert(selection.selected.map(x=>x.receiverId).join(',')===cfg.receiverIds.join(','),'Receiver IDs fixed');
 context={phase:'decode original states'};const originalStateBytes=fs.readFileSync(path.join(repo,cfg.sourceReferenceDirectory,'raw',cfg.sourceCase+'-states.f64'));const stateValues=h.decodeF64(originalStateBytes);assert(stateValues.length===5000*17,'Original state shape');const states=Array.from({length:5000},(_,i)=>Array.from(stateValues.slice(17*i,17*i+17)));
 const C=h.makeOriginalConstants();out.constants=C;write('original-constants.json',C);
 const encoding=JSON.parse(fs.readFileSync(path.join(base,'constants/constant-encodings.json')));
 for(const e of encoding.entries.filter(x=>x.index<14))assert(h.encodeF64([C[e.name]]).toString('hex')===e.float64LEHex,'Original constant identity '+e.name);
 for(const [key,e]of Object.entries(encoding.extra))assert(h.encodeF64([C[key]]).toString('hex')===e.float64LEHex,'Original allocation identity '+key);
 assert(C.referenceSumAllowance===cfg.gates.referenceAllowanceMps&&cfg.gates.wakeForceAllocationN===1e-7,'Frozen allocation configuration');
 context={phase:'prepare original axes and offsets'};const P=h.prepareOriginal(states,cfg.receiverIds,C,charge);savePrepared('R-prepared',P,h);assert(h.encodeF64(P.constants).equals(fs.readFileSync(path.join(base,'constants/frozen-original-constants.f64'))),'Prepared original constant bytes');write('selected-ids.u32',h.encodeU32(P.ids));
 context={phase:'pack prepared geometry'};const packed=h.packPrepared(P,C,charge);savePrepared('Q-prepared',packed.prepared,h);write('Q-constants.json',packed.constants);assert(h.encodeU32(packed.packed.constants).equals(fs.readFileSync(path.join(base,'constants/frozen-packed-constants.u32'))),'Packed constant words');
 for(const k of ['nodes','offsets','ids','constants'])write('packed-'+k+'.u32',h.encodeU32(packed.packed[k]));
 context={phase:'selected R reference'};const R=h.evaluateSelected(P,C,'R',charge);saveReference('R',R,h);
 const savedCodes=Buffer.concat(selection.selected.map(x=>fs.readFileSync(path.join(base,'selection',x.savedCodePath)))),savedSums=h.decodeF64(Buffer.concat(selection.selected.map(x=>fs.readFileSync(path.join(base,'selection',x.savedSumsPath)))));
 out.R=assess('R',()=>h.assessR(R,savedCodes,savedSums,C));assert(out.R.pass,'Original R reproduction gate',out.R);
 context={phase:'selected Q reference'};const Q=h.evaluateSelected(packed.prepared,packed.constants,'Q',charge);saveReference('Q',Q,h);out.Q=assess('Q',()=>h.assessQ(R,Q,C));assert(out.Q.pass,'Packed interface gate',out.Q);
 guard();context={phase:'browser launch'};browser=await chromium.launch({channel:'chrome',headless:true,timeout:15000});assert(registry.hasRegisteredBrowser(),'Browser ownership registration');write('process-registration-summary.json',registry.summary());out.browserVersion=await browser.version();assert(out.browserVersion===runtime.chromeBundleVersion,'Frozen browser version');
 page=await browser.newPage();page.setDefaultTimeout(15000);page.on('pageerror',e=>faults.push(e.message));page.on('console',m=>{if(m.type()==='error')faults.push(m.text());});
 const url='http://127.0.0.1:8876/research/m31-browser-wake-slice-2026-10-16/source/',served=[];
 for(const [name,type]of [['browser.html','text/html'],['browser.js','application/javascript'],['wake.wgsl','text/plain']]){const b=fs.readFileSync(path.join(__dirname,name));await page.route(url+name,route=>{served.push({name,bytes:b.length,sha256:sha(b)});return route.fulfill({status:200,contentType:type,body:b});});}
 write('served-source-contract.json',{files:['browser.html','browser.js','wake.wgsl'].map(name=>{const b=fs.readFileSync(path.join(__dirname,name));return {name,bytes:b.length,sha256:sha(b)};}),method:'Exact frozen local bytes fulfilled by Playwright; no unchecked server runner'});out.servedSources=served;
 await page.goto(url+'browser.html');await page.waitForFunction(()=>window.wakeRunnerReady===true);context={phase:'GPU initialization'};
 const cap=await deadline(page.evaluate(()=>window.initializeWake()),15000,'GPU initialization');if(cap.shader){assert(sha(Buffer.from(cap.shader))===sha(fs.readFileSync(path.join(__dirname,'wake.wgsl'))),'Served shader identity');delete cap.shader;}out.capability=cap;write('capability.json',{browserVersion:out.browserVersion,...cap});
 if(!cap.supported){out.status='unsupported';out.pass=false;return;}assert(cap.compiled&&!cap.validation&&!cap.loss&&!cap.uncaptured,'GPU compilation/API gate',cap);assert(faults.length===0,'Browser errors',faults);
 const controlBytes=fs.readFileSync(path.join(base,'controls/controls.u32')),inputs={};for(const k of ['nodes','offsets','ids','constants'])inputs[k]=h.encodeU32(packed.packed[k]).toString('base64');inputs.controls=controlBytes.toString('base64');write('packed-controls.u32',controlBytes);
 const prep=await deadline(page.evaluate(input=>window.prepareWake(input),inputs),10000,'GPU buffer prepare');write('GPU-buffer-contract.json',prep);assert(!prep.validation&&!prep.loss&&!prep.uncaptured,'GPU preparation gate',prep);
 const controls=await dispatch('controls');out.controls=assess('controls',()=>h.assessControls(controls,JSON.parse(fs.readFileSync(path.join(base,'controls/controls.json')))));assert(out.controls.pass,'Composite policy control gate',out.controls);
 const terms=await dispatch('terms');context={phase:'saved GPU term attribution'};out.terms=assess('terms',()=>h.assessGpuTerms(R,Q,terms,C,cfg.receiverIds));assert(out.terms.pass,'GPU term qualification',out.terms);
 const sums=await dispatch('reduce');context={phase:'saved serial-sum attribution'};out.serial=assess('serial',()=>h.assessSerial(out.terms,sums,C,cfg.receiverIds));assert(out.serial.pass,'Conservative combined error gate',out.serial);
 const health=await page.evaluate(()=>window.wakeHealth());write('final-gpu-health.json',health);assert(!health.loss&&!health.uncaptured&&faults.length===0,'Final browser/GPU health',{health,faults});assert(counts.dispatches===3&&counts.gpuPairSlots===80000&&counts.gpuControlSlots===16&&counts.gpuSumSlots===16,'Complete GPU reservations');
 out.status='completed';out.pass=true;
})().catch(async e=>{if(page){try{write('browser-failure-evidence.json',await deadline(page.evaluate(()=>({initialization:window.wakeInitializationEvidence??null,dispatch:window.lastWakeDispatch??null,health:window.wakeHealth?.()??null})),1000,'Failure evidence'),true);}catch(f){out.browserFailureEvidenceUnavailable=f.message;}}process.exitCode=1;out.status='failed';out.pass=false;out.error={message:e.message,detail:e.detail??null,context};}).finally(async()=>{
 const cleanup=[];if(page){try{await deadline(page.evaluate(()=>window.shutdownWake()),1000,'GPU cleanup');}catch(e){cleanup.push(e.message);}}if(browser){try{await deadline(browser.close(),3000,'Browser cleanup');}catch(e){cleanup.push(e.message);}}
 if(cleanup.length){out.cleanupErrors=cleanup;out.pass=false;process.exitCode=1;if(out.status==='completed')out.status='failed';}
 out.checks=checks;out.counts=counts;out.elapsedSeconds=(performance.now()-start)/1000;out.terminal=true;out.files=fs.existsSync(raw)?fs.readdirSync(raw).sort().map(name=>{const b=fs.readFileSync(path.join(raw,name));return {name,bytes:b.length,sha256:sha(b)};}):[];
 try{write('result.json',out,true);fs.writeFileSync(path.join(base,'results/result.json'),JSON.stringify(out,null,2)+'\n',{flag:'wx'});}catch(e){process.exitCode=1;console.error('Terminal evidence write failed: '+e.message);}
 console.log(JSON.stringify({status:out.status,pass:out.pass,error:out.error,counts,elapsedSeconds:out.elapsedSeconds,rawBytes}));
});
