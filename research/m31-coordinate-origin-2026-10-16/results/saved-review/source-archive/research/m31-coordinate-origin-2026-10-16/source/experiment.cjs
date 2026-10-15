'use strict';
// All fresh geometry, reference arithmetic and GPU work belong to one supervised invocation.
const fs=require('fs'),path=require('path'),crypto=require('crypto'),registry=require('./process-registry.cjs');
const {chromium}=require('playwright');
const base=path.resolve(__dirname,'..'),repo=path.resolve(base,'../..'),raw=path.join(base,'raw'),cfg=JSON.parse(fs.readFileSync(path.join(base,'config.json'))),limit=cfg.limits,start=performance.now();
const sha=b=>crypto.createHash('sha256').update(b).digest('hex'),source=process.env.RESEARCH_SOURCE_COMMIT;
let browser,page,rawBytes=0,checks=0,context={},counts={},out={sourceCommit:source,scope:cfg.scope,config:cfg,cells:[],counts};const faults=[];
const privateExceptions=[];
function publicText(value){return String(value).split('\n')[0].replace(/\/(?:Users|private|var|tmp|Volumes|Applications|Library|opt|usr|System)\/[^\s"'<>]*/g,'[local-path]').replace(/--user-data-dir=\S+/g,'[private-profile]').replace(/playwright[_-][a-z_]+profile[-_][A-Za-z0-9_-]+/g,'[private-profile]').replace(/\b(?:pid|PID|pgid)\s*[=:]\s*\d+/g,'[private-process]').slice(0,512);}
function publicValue(v){if(typeof v==='string')return publicText(v);if(Array.isArray(v))return v.map(publicValue);if(v&&typeof v==='object')return Object.fromEntries(Object.entries(v).map(([k,x])=>[k,publicValue(x)]));return v;}
function preservePrivateError(phase,e){privateExceptions.push({phase,name:e?.name??null,message:e?.message??String(e),stack:e?.stack??null,detail:e?.detail??null});}

function assert(ok,message,detail){checks++;if(!ok){const e=Error(message);e.detail=detail;throw e;}}
function guard(){if(performance.now()-start>=1000*limit.cooperativeWallSeconds)throw Error('Cooperative wall cap');if(faults.length)throw Object.assign(Error('Shared browser error'),{detail:faults.slice(0,32)});}
function charge(name,amount=1){guard();assert(Number.isSafeInteger(amount)&&amount>=0,'Counter increment');assert(name in limit,'Unknown counter '+name);counts[name]=(counts[name]??0)+amount;assert(counts[name]<=limit[name],'Operation cap '+name,{actual:counts[name],cap:limit[name]});}
function write(name,data,failure=false){const bytes=Buffer.isBuffer(data)?data:Buffer.from(JSON.stringify(data,null,2)+'\n');assert(rawBytes+bytes.length<=limit.rawBytes-(failure?0:limit.failureReserveBytes),'Evidence byte cap');fs.writeFileSync(path.join(raw,name),bytes,{flag:'wx'});rawBytes+=bytes.length;}
async function deadline(promise,ms,label){let timer;try{return await Promise.race([promise,new Promise((_,reject)=>{timer=setTimeout(()=>reject(Error(label+' timeout')),ms);})]);}finally{clearTimeout(timer);}}
function assess(stage,kind,fn){
 guard();charge('assessmentCalls:'+kind);const reserved=cfg.assessmentReservations[kind];assert(reserved,'Known assessment kind');
 for(const [name,n]of Object.entries(reserved)){const key='assessmentReserved:'+name;counts[key]=(counts[key]??0)+n;assert(counts[key]<=cfg.assessmentLimits[name],'Assessment reservation cap '+name);}
 const result=fn();write(stage+'-assessment.json',result);
 for(const [name,n]of Object.entries(result.counts??{})){assert(name in reserved&&Number.isSafeInteger(n)&&n>=0&&n<=reserved[name],'Assessment actual cap '+name,{stage,n});const key='assessmentActual:'+name;counts[key]=(counts[key]??0)+n;assert(counts[key]<=cfg.assessmentLimits[name],'Aggregate assessment cap '+name);}
 if(['referenceContrast','gpuContrast'].includes(kind))assert(result.integrityPass,'Saved contrast integrity',result);guard();return result;
}
async function dispatch(kind,arm,origin=null){
 guard();const prefix=kind==='controls'?'controls-'+arm:'o'+origin+'-'+arm+'-'+kind;context={phase:'GPU '+prefix};
 const slots={controls:20,terms:80000,reduce:16}[kind],bytesExpected={controls:2080,terms:8320000,reduce:512}[kind],groups=kind==='terms'?1250:1;
 charge('dispatches');charge('gpuLaunchedInvocations',groups*64);charge('gpuPaddingInvocations',groups*64-slots);if(kind==='reduce')charge('gpuSumReadReservation',80000);charge({controls:'gpuControlSlots',terms:'gpuPairSlots',reduce:'gpuSumSlots'}[kind],slots);
 return deadline((async()=>{const r=await page.evaluate(async({kind,arm,ms})=>window.dispatchCoordinate(kind,arm,ms),{kind,arm,ms:limit.gpuBatchTimeoutMilliseconds});
 const bytes=Buffer.from(r.base64,'base64');write(prefix+'-gpu.u32',bytes);write(prefix+'-readback.json',{bytes:r.bytes,dispatch:r.dispatch,costs:r.costs});
 const api=await page.evaluate(()=>window.finishCoordinateBatch());write(prefix+'-api.json',api);guard();assert(!api.validation&&!api.loss&&!api.uncaptured,'GPU API qualification',api);
 assert(bytes.length===bytesExpected&&r.bytes===bytes.length,'GPU byte coverage');assert(r.dispatch.submitted&&r.dispatch.kind===kind&&r.dispatch.arm===arm&&r.dispatch.cell===(kind==='controls'?null:'o'+origin+'-'+arm)&&r.dispatch.count===slots&&r.dispatch.groups===groups&&r.dispatch.outputBytes===bytes.length,'GPU dispatch accounting',r.dispatch);return bytes;
 })(),limit.gpuBatchTimeoutMilliseconds,'Complete GPU '+prefix);
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
 const h=require('./host.cjs');context={phase:'fresh seed release and exact integer geometry construction'};charge('freshGeneratorCalls');const generated=h.generateFresh(source,charge);
 write('generated-receiver-ids.u32',h.encodeU32(generated.receiverIds));write('generator-audit.json',generated.audit);out.generator=generated.audit;assert(generated.receiverIds.join(',')===cfg.receiverIds.join(','),'Output-independent receiver rule');
 for(const key of ['canonicalNumerators','translatedNumerators','angleTicks'])write('generated-'+key+'.i32',h.encodeI32(generated[key]));
 for(const key of ['angles','translationResiduals'])write('generated-'+key+'.f64',h.encodeF64(generated[key]));
 for(let o=0;o<2;o++)write('o'+o+'-states.f64',h.encodeF64(generated.statesByOrigin[o].flat()));
 const C=h.makeOriginalConstants();out.constants=C;write('original-constants.json',C);
 const encoding=JSON.parse(fs.readFileSync(path.join(base,'constants/constant-encodings.json')));
 for(const e of encoding.entries.filter(x=>x.index<14))assert(h.encodeF64([C[e.name]]).toString('hex')===e.float64LEHex,'Original constant identity '+e.name);
 for(const [key,e]of Object.entries(encoding.extra))assert(h.encodeF64([C[key]]).toString('hex')===e.float64LEHex,'Original allocation identity '+key);
 assert(C.referenceSumAllowance===cfg.gates.referenceAllowanceMps&&C.epsilonWake===cfg.gates.epsilonWakeMps&&cfg.gates.wakeForceAllocationN===1e-7,'Frozen allocation configuration');
 context={phase:'prepare original attitude geometry once'};charge('originalPreparationCalls');const P0=h.prepareOriginal(generated.statesByOrigin[0],cfg.receiverIds,C,charge);charge('translationPreparationCalls');const prepared=[P0,h.translatePrepared(P0,generated.statesByOrigin[1],C,charge)];
 const packed=[],refs=[],gates=[];
 for(let o=0;o<2;o++){
  const prefix='o'+o;context={phase:prefix+' prepare and pack'};savePrepared(prefix+'-R-prepared',prepared[o],h);assert(h.encodeF64(prepared[o].constants).equals(fs.readFileSync(path.join(base,'constants/frozen-original-constants.f64'))),'Original constant bytes');
  charge('packingCalls');const p=h.packPrepared(prepared[o],C,charge);packed.push(p);savePrepared(prefix+'-Q0-prepared',p.Q0,h);savePrepared(prefix+'-Q1-prepared',p.Q1,h);write(prefix+'-packing-audit.json',p.audit);write(prefix+'-packed-constants.json',p.constants);
  write(prefix+'-positionPackingResiduals.f64',h.encodeF64(p.positionPackingResiduals));write(prefix+'-reconstructionResiduals.f64',h.encodeF64(p.reconstructionResiduals));
  for(const label of ['AB','C'])for(const key of ['nodes','offsets','ids','constants'])write(prefix+'-packed'+label+'-'+key+'.u32',h.encodeU32(p['packed'+label][key]));
  assert(h.encodeU32(p.packedAB.constants).equals(fs.readFileSync(path.join(base,'constants/frozen-packed-constants.u32'))),'Packed constant identity');
  for(const key of ['constants','offsets','ids'])assert(h.encodeU32(p.packedAB[key]).equals(h.encodeU32(p.packedC[key])),'Only position representation differs '+key);
  charge('hostReferencePasses');const R=h.evaluateSelected(prepared[o],C,'R',charge);saveReference(prefix+'-R',R,h);const rg=assess(prefix+'-R','R',()=>h.assessR(R,C));assert(rg.integrityPass&&rg.numericalPass&&rg.pass,'Original reference shared premise',rg);
  const useful=assess(prefix+'-usefulness','usefulness',()=>h.assessUsefulness(R,C));assert(useful.integrityPass,'Usefulness evidence integrity',useful);
  charge('hostReferencePasses');const Q0=h.evaluateSelected(p.Q0,p.constants,'Q0',charge);saveReference(prefix+'-Q0',Q0,h);const q0=assess(prefix+'-Q0','Q',()=>h.assessQ(R,Q0,C));assert(q0.integrityPass,'Q0 reference integrity',q0);
  charge('hostReferencePasses');const Q1=h.evaluateSelected(p.Q1,p.constants,'Q1',charge);saveReference(prefix+'-Q1',Q1,h);const q1=assess(prefix+'-Q1','Q',()=>h.assessQ(R,Q1,C));assert(q1.integrityPass,'Q1 reference integrity',q1);
  assess(prefix+'-Q1-Q0','referenceContrast',()=>h.compareReferences(Q0,Q1,C,prefix+'-Q1-minus-Q0'));
  refs.push({R,Q0,Q1});gates.push({R:rg,Q0:q0,Q1:q1,usefulness:useful,packing:p.audit});
 }
 out.references=gates;assess('R-origin-contrast','referenceContrast',()=>h.compareReferences(refs[0].R,refs[1].R,C,'R-translated-minus-canonical'));
 // The host's saved audit establishes the preregistered precision stimulus; no geometry is regenerated.
 const stimulus={canonicalPackingExact:Array.from(packed[0].positionPackingResiduals).every(x=>x===0),translatedPackingLoss:Array.from(packed[1].positionPackingResiduals).some(x=>x!==0),bothReconstructionsExact:packed.every(p=>Array.from(p.reconstructionResiduals).every(x=>x===0)),translationExact:Array.from(generated.translationResiduals).every(x=>x===0)};
 write('stimulus.json',stimulus);out.stimulus=stimulus;out.useful=gates.every(g=>g.usefulness.pass)&&Object.values(stimulus).every(Boolean);
 if(!out.useful){out.status='completed-uninformative-stimulus';out.pass=false;out.invocationComplete=true;out.candidate=null;return;}
 guard();context={phase:'browser launch'};browser=await chromium.launch({channel:'chrome',headless:true,timeout:15000});assert(registry.hasRegisteredBrowser(),'Browser ownership registration');write('process-registration-summary.json',registry.summary());out.browserVersion=await browser.version();assert(out.browserVersion===runtime.chromeBundleVersion,'Frozen browser version');
 page=await browser.newPage();page.setDefaultTimeout(15000);page.on('pageerror',e=>faults.push(e.message));page.on('console',m=>{if(m.type()==='error')faults.push(m.text());});
 const url='http://127.0.0.1:8876/research/m31-coordinate-origin-2026-10-16/source/',served=[];
 for(const [name,type]of [['browser.html','text/html'],['browser.js','application/javascript'],['coordinate.wgsl','text/plain']]){const b=fs.readFileSync(path.join(__dirname,name));await page.route(url+name,route=>{served.push({name,bytes:b.length,sha256:sha(b)});return route.fulfill({status:200,contentType:type,body:b});});}
 write('served-source-contract.json',{files:['browser.html','browser.js','coordinate.wgsl'].map(name=>{const b=fs.readFileSync(path.join(__dirname,name));return {name,bytes:b.length,sha256:sha(b)};}),method:'Exact frozen local bytes fulfilled by Playwright; no unchecked server runner'});out.servedSources=served;
 await page.goto(url+'browser.html');await page.waitForFunction(()=>window.coordinateRunnerReady===true);context={phase:'GPU initialization'};
 const cap=await deadline(page.evaluate(()=>window.initializeCoordinate()),15000,'GPU initialization');if(cap.shader){assert(sha(Buffer.from(cap.shader))===sha(fs.readFileSync(path.join(__dirname,'coordinate.wgsl'))),'Served shader identity');delete cap.shader;}out.capability=cap;write('capability.json',{browserVersion:out.browserVersion,...cap});
 if(!cap.supported){out.status='unsupported';out.pass=false;return;}assert(cap.compiled&&!cap.validation&&!cap.loss&&!cap.uncaptured,'GPU compilation/API gate',cap);assert(faults.length===0,'Browser errors',faults);
 const controlBytes=fs.readFileSync(path.join(base,'controls/controls.u32')),controlSpec=JSON.parse(fs.readFileSync(path.join(base,'controls/controls.json')));write('packed-controls.u32',controlBytes);
 const prep=await deadline(page.evaluate(input=>window.prepareCoordinateControls(input),{constants:h.encodeU32(packed[0].packedAB.constants).toString('base64'),controls:controlBytes.toString('base64')}),10000,'Control buffer prepare');write('GPU-controls-buffer-contract.json',prep);assert(!prep.validation&&!prep.loss&&!prep.uncaptured,'GPU control preparation gate',prep);
 out.controls={};for(const arm of ['A','B','C']){const bytes=await dispatch('controls',arm);out.controls[arm]=assess('controls-'+arm,'controls',()=>h.assessControls(bytes,controlSpec,arm));assert(out.controls[arm].pass,'Composite control shared premise',out.controls[arm]);}
 const retained=[{},{}];
 for(let o=0;o<2;o++)for(const arm of ['A','B','C']){
  const cellOut={origin:o,arm,key:'o'+o+'-'+arm,reference:arm==='C'?'Q1':'Q0'};out.cells.push(cellOut);const p=packed[o],q=refs[o][cellOut.reference],qg=gates[o][cellOut.reference];
  if(!qg.pass){cellOut.status='skipped-interface-gate';cellOut.qualified=false;write(cellOut.key+'-disposition.json',cellOut);continue;}
  const input={arm,origin:o};for(const key of ['nodes','offsets','ids'])input[key]=h.encodeU32((arm==='C'?p.packedC:p.packedAB)[key]).toString('base64');
  guard();charge('gpuCellPreparations');const prep=await deadline(page.evaluate(input=>window.prepareCoordinateCell(input),input),10000,'GPU cell prepare');write(cellOut.key+'-buffer-contract.json',prep);guard();assert(!prep.validation&&!prep.loss&&!prep.uncaptured,'GPU cell preparation gate',prep);
  const terms=await dispatch('terms',arm,o);retained[o][arm]=terms;cellOut.terms=assess(cellOut.key+'-terms','terms',()=>h.assessGpuTerms(refs[o].R,q,terms,C,cfg.receiverIds));assert(cellOut.terms.integrityPass,'GPU term record integrity',cellOut.terms);
  if(cellOut.terms.pass){const sums=await dispatch('reduce',arm,o);cellOut.serial=assess(cellOut.key+'-serial','serial',()=>h.assessSerial(cellOut.terms,sums,C,cfg.receiverIds));assert(cellOut.serial.integrityPass,'GPU reduction record integrity',cellOut.serial);cellOut.qualified=cellOut.serial.pass;cellOut.status=cellOut.qualified?'qualified':'failed-combined-error';}
  else{cellOut.status='failed-term-gate';cellOut.qualified=false;cellOut.serial=null;}
  cellOut.release=await page.evaluate(()=>window.finishCoordinateCell());write(cellOut.key+'-disposition.json',cellOut);guard();
 }
 for(let o=0;o<2;o++)for(const [left,right]of [['A','B'],['B','C']])if(retained[o][left]&&retained[o][right])assess('o'+o+'-'+right+'-'+left+'-vectors','gpuContrast',()=>h.compareGpuVectors(retained[o][left],retained[o][right],'o'+o+'-'+right+'-minus-'+left));
 const health=await page.evaluate(()=>window.coordinateHealth());write('final-gpu-health.json',health);out.costs=health.costs;assert(!health.loss&&!health.uncaptured&&faults.length===0,'Final browser/GPU health',{health,faults});
 const executed=out.cells.filter(c=>c.release),readback=(counts.gpuControlSlots??0)*104+(counts.gpuPairSlots??0)*104+(counts.gpuSumSlots??0)*32;
 const cellNodes=executed.reduce((n,c)=>n+(c.arm==='C'?240000:160000),0),cellCount=executed.length;
 const expectedCosts={pipelineCreations:7,bufferCreations:3+5*cellCount+counts.dispatches,allocatedBytes:5344+cellNodes+cellCount*(256+16+8320000+512)+readback,uploadedBytes:3264+cellNodes+cellCount*272,clearedBytes:6240,readbackBytes:readback,dispatches:counts.dispatches,activeOutputSlots:(counts.gpuControlSlots??0)+(counts.gpuPairSlots??0)+(counts.gpuSumSlots??0),launchedInvocations:counts.gpuLaunchedInvocations,liveBufferBytes:64,peakLiveBufferBytes:Math.max(7424,...executed.map(c=>16640848+(c.arm==='C'?240000:160000)))};
 const gpuLedger=JSON.parse(fs.readFileSync(path.join(base,'BYTE-ACCOUNTING.json'))).GPU;
 const maxima={pipelineCreations:'pipelineCreations',bufferCreations:'maximumBufferCreations',allocatedBytes:'maximumCumulativeAllocatedBytes',uploadedBytes:'maximumCumulativeUploadedBytes',readbackBytes:'maximumCumulativeReadbackBytes',clearedBytes:'maximumClearedControlOutputBytes',peakLiveBufferBytes:'maximumLiveBufferBytes'};
 out.costReconciliation={expected:expectedCosts,observed:health.costs,cellCount};write('cost-reconciliation.json',out.costReconciliation);
 for(const [key,value]of Object.entries(expectedCosts))assert(health.costs[key]===value,'Exact executed GPU cost '+key,{expected:value,actual:health.costs[key]});
 for(const [key,capKey]of Object.entries(maxima))assert(health.costs[key]<=gpuLedger[capKey],'GPU resource ceiling '+key);
 assert(counts.gpuPaddingInvocations===expectedCosts.launchedInvocations-expectedCosts.activeOutputSlots,'Padding cost reconciliation');
 const qualified={};for(const arm of ['A','B','C'])qualified[arm]=[0,1].every(origin=>out.cells.some(c=>c.arm===arm&&c.origin===origin&&c.qualified===true));
 out.qualifiedArms=qualified;out.candidate=qualified.A?null:qualified.B?'B':qualified.C?'C':null;
 out.decision=qualified.A?'baseline-already-qualifies':out.candidate?'candidate-earns-separate-fresh-confirmation':'no-candidate';
 out.status='completed-numerical-comparison';out.pass=Object.values(qualified).every(Boolean);out.invocationComplete=true;
})().catch(async e=>{preservePrivateError('primary',e);if(page){try{write('browser-failure-evidence.json',await deadline(page.evaluate(()=>({initialization:window.coordinateInitializationEvidence??null,dispatch:window.lastCoordinateDispatch??null,health:window.coordinateHealth?.()??null})),1000,'Failure evidence'),true);}catch(f){preservePrivateError('failure-evidence',f);out.browserFailureEvidenceUnavailable=publicText(f.message);}}process.exitCode=1;out.status='failed-shared-premise-or-infrastructure';out.pass=false;out.candidate=null;out.error={name:e.name??'Error',message:publicText(e.message),detail:publicValue(e.detail??null),context};}).finally(async()=>{
 const cleanup=[];if(page){try{await deadline(page.evaluate(()=>window.shutdownCoordinate()),1000,'GPU cleanup');}catch(e){preservePrivateError('cleanup',e);cleanup.push(publicText(e.message));}}if(browser){try{await deadline(browser.close(),3000,'Browser cleanup');}catch(e){preservePrivateError('cleanup',e);cleanup.push(publicText(e.message));}}
 if(cleanup.length){out.cleanupErrors=cleanup;out.pass=false;out.candidate=null;process.exitCode=1;out.status='failed-cleanup';}
 if(privateExceptions.length){try{const b=Buffer.from(JSON.stringify(privateExceptions,null,2)+'\n');fs.writeFileSync(process.env.RESEARCH_PROCESS_REGISTRY+'.errors.json',b,{flag:'wx'});out.privateErrorReceipt={bytes:b.length,sha256:sha(b),disclosure:'Full local exception strings retained privately; public messages limited to first line with local paths/profiles/process IDs redacted.'};}catch(e){out.privateErrorReceipt={written:false,errorType:e.name};}}
 out.checks=checks;out.counts=counts;out.elapsedSeconds=(performance.now()-start)/1000;out.terminal=true;out.files=fs.existsSync(raw)?fs.readdirSync(raw).sort().map(name=>{const b=fs.readFileSync(path.join(raw,name));return {name,bytes:b.length,sha256:sha(b)};}):[];
 try{write('result.json',out,true);fs.writeFileSync(path.join(base,'results/result.json'),JSON.stringify(out,null,2)+'\n',{flag:'wx'});}catch(e){process.exitCode=1;console.error('Terminal evidence write failed: '+publicText(e.message));}
 console.log(JSON.stringify({status:out.status,pass:out.pass,candidate:out.candidate,decision:out.decision,error:out.error,counts,elapsedSeconds:out.elapsedSeconds,rawBytes}));
});
