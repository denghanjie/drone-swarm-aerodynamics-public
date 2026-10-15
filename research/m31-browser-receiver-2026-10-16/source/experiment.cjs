'use strict';
const fs=require('fs'),path=require('path'),crypto=require('crypto'),processRegistry=require('./process-registry.cjs');
const {chromium}=require('playwright');
const base=path.resolve(__dirname,'..'),repo=path.resolve(base,'../..'),raw=path.join(base,'raw'),cfg=JSON.parse(fs.readFileSync(path.join(base,'config.json'))),limit=cfg.limits,start=performance.now();
const source=process.env.RESEARCH_SOURCE_COMMIT,sha=b=>crypto.createHash('sha256').update(b).digest('hex');
let browser,page,rawBytes=0,records=[],context={},checks=0;
const counts={dispatches:0,gpuValidRoots:0,gpuInvalidGuards:0,gpuIterationReservation:0,hostBisectionRoots:0,hostIterationReservation:0,actualHostIterations:0,fieldEvaluations:0,integrationSteps:0};
const output={sourceCommit:source,scope:cfg.scope,config:cfg,counts,batches:[]};
async function deadline(promise,ms,label){let timer;try{return await Promise.race([promise,new Promise((_,reject)=>{timer=setTimeout(()=>reject(Error(label+' timeout')),ms);})]);}finally{clearTimeout(timer);}}
function guard(){if(performance.now()-start>=1000*limit.cooperativeWallSeconds)throw Error('Cooperative scientific timeout');}
function assert(ok,message,detail){checks++;if(!ok){const e=Error(message);e.detail=detail;throw e;}}
function write(name,bytes,failure=false){if(!Buffer.isBuffer(bytes))bytes=Buffer.from(JSON.stringify(bytes,null,2)+'\n');const cap=limit.rawBytes-(failure?0:limit.failureReserveBytes);if(rawBytes+bytes.length>cap)throw Error('Raw evidence cap');fs.writeFileSync(path.join(raw,name),bytes,{flag:'wx'});rawBytes+=bytes.length;records.push({name,bytes:bytes.length,sha256:sha(bytes)});}
function append(name,bytes){if(rawBytes+bytes.length>limit.rawBytes-limit.failureReserveBytes)throw Error('Raw evidence cap');fs.appendFileSync(path.join(raw,name),bytes);rawBytes+=bytes.length;}
const f64=values=>{const b=Buffer.alloc(values.length*8);values.forEach((v,i)=>b.writeDoubleLE(v,8*i));return b;},u32=values=>{const b=Buffer.alloc(values.length*4);values.forEach((v,i)=>b.writeUInt32LE(v>>>0,4*i));return b;};
function f32Bits(x){const b=Buffer.alloc(4);b.writeFloatLE(x);return b.readUInt32LE();}
function decodeF32(bits){const b=Buffer.alloc(4);b.writeUInt32LE(bits>>>0);return b.readFloatLE();}
function charge(name,n){counts[name]+=n;assert(counts[name]<=limit[name],'Operation cap: '+name,{actual:counts[name],cap:limit[name]});}
let solveAlpha,powerRatio,F0,VI,FQ,VQ;
function root(alpha){charge('hostBisectionRoots',1);charge('hostIterationReservation',96);const r=solveAlpha(alpha);counts.actualHostIterations+=r.iterations;assert(Number.isFinite(r.x)&&r.lo<=r.x&&r.x<=r.hi&&r.lo>=0&&r.hi<=1&&r.hi-r.lo<=cfg.gates.referenceBracketWidth&&Math.abs(r.residual)<=cfg.gates.referenceResidualAbsolute,'Independent root qualification',r);return r;}
function compareRecord(reference,g,q,a,summary,index){
 const [U,f0,vi,rx,rf,rlo,rhi,rit]=reference,[alpha,x,f,residual,iterations,stop,step,reserved]=g;
 assert(g.every(Number.isFinite),'Nonfinite GPU record',{index,g});
 assert(Number.isInteger(iterations)&&iterations>=0&&iterations<=12&&[0,1,2].includes(stop)&&reserved===0&&step>=0,'GPU record metadata',{index,g});
 assert(alpha>=0&&x>0&&x<=1&&f>=0&&f<=FQ,'GPU root/force range',{index,g});
 const UQ=Math.fround(U);
 if(UQ===0)assert(alpha===0&&x===1&&f32Bits(f)===f32Bits(FQ)&&iterations===0&&stop===0&&step===0&&residual===0,'GPU zero-input identity',{index,g});
 else {assert(alpha>0&&iterations>=1&&stop!==0,'Positive-input iteration metadata',{index,g});if(stop===2)assert(iterations===12&&step>=Math.fround(1e-15),'Iteration-cap record',{index,g});if(stop===1)assert(step<Math.fround(1e-15),'Threshold-stop record',{index,g});}
 const telescoping=(q.f-rf)+(a.f-q.f)+(FQ*x-a.f)+(f-FQ*x);assert(Math.abs(telescoping-(f-rf))<=1e-15,'Signed error decomposition identity',{index,telescoping,total:f-rf});
 const errors={rootOriginalX:Math.abs(x-rx),rootRepresentedX:Math.abs(x-q.x),originalCubicAtReturnedX:Math.abs(x*x*x+(U/vi)*x-1),representedCubicAtReturnedX:Math.abs(x*x*x+q.alpha*x-1),rotorTotal:Math.abs(f-rf),inputRepresentation:Math.abs(q.f-rf),shaderVersusRepresented:Math.abs(f-q.f),alphaDivision:Math.abs(alpha-q.alpha),alphaForceEffect:Math.abs(a.f-q.f),rootX:Math.abs(x-a.x),rootForceEffect:Math.abs(FQ*(x-a.x)),finalMultiplication:Math.abs(f-FQ*x),hostResidual:Math.abs(x*x*x+alpha*x-1),shaderResidual:Math.abs(residual),representedPower:Math.abs(powerRatio(f,FQ,UQ/VQ)-1),originalPower:Math.abs(f*(U/2+Math.sqrt(U*U/4+f/(2*1.225*output.constants.area)))/(F0*VI)-1)};
 for(const [k,v]of Object.entries(errors)){assert(Number.isFinite(v),'Finite error diagnostic',{index,k,v});if(v>summary.maxima[k].value)summary.maxima[k]={value:v,index};}
 summary.oldPrecisionFailures+=errors.rotorTotal>cfg.gates.originalRotorDiagnosticN?1:0;
 summary.stops[String(stop)]++;if(stop===1&&step===0)summary.exactZeroStepStops++;if(stop===2)summary.iterationCapRecords++;
 const passed=errors.rotorTotal<=cfg.gates.rotorTotalAbsoluteN&&errors.rootX<=cfg.gates.rootXAbsolute&&errors.hostResidual<=cfg.gates.hostResidualAbsolute&&errors.representedPower<=cfg.gates.representedPowerRatioAbsolute;
 if(!passed){summary.gateFailures++;if(summary.firstFailure===null)summary.firstFailure={index,reference,g,q,a,errors};}
}
async function gpuBatch(id,bits){
 return deadline((async()=>{
  const returned=await page.evaluate(async({bits,timeout})=>window.dispatchReceiver(bits,timeout),{bits,timeout:limit.gpuBatchTimeoutMilliseconds});
  write(id+'-gpu.u32',u32(returned.bits));write(id+'-readback.json',{returnedCount:returned.count,words:returned.bits.length,dispatch:returned.dispatch});
  const api=await page.evaluate(()=>window.finishReceiverBatch());write(id+'-api.json',api);assert(!api.validation&&!api.loss&&!api.uncaptured,'GPU batch API qualification',api);return returned;
 })(),limit.gpuBatchTimeoutMilliseconds,'Complete GPU batch');
}
async function validBatch(id,reference){
 guard();context={batch:id,phase:'packing',records:reference.length};const n=reference.length,bits=[];
 for(let i=0;i<n;i++){
  const [U,f0,vi,x,f,lo,hi,it]=reference[i];assert(reference[i].every(Number.isFinite),'Finite original reference',{id,i});
  assert(U>=0&&U<=128&&f0===F0&&vi===VI&&lo>=0&&lo<=x&&x<=hi&&hi<=1&&hi-lo<=cfg.gates.referenceBracketWidth&&Number.isInteger(it)&&it>=0&&it<=96,'Original reference domain/bracket',{id,i,reference:reference[i]});
  assert(Math.abs(x*x*x+(U/vi)*x-1)<=1e-12&&Math.abs(f-F0*x)<=1e-14,'Original reference equation',{id,i});
  const UQ=Math.fround(U);assert(Number.isFinite(UQ)&&UQ>=0&&UQ<=128&&(U===0?UQ===0:UQ>0&&UQ/VQ>=2**-120),'Represented input admission',{id,i,U,UQ});
  bits.push(f32Bits(UQ),f32Bits(FQ),f32Bits(VQ),0);
 }
 if(fs.existsSync(path.join(raw,id+'-original.f64')))assert(fs.readFileSync(path.join(raw,id+'-original.f64')).equals(f64(reference.flat())),'Original reference stream equality');else write(id+'-original.f64',f64(reference.flat()));write(id+'-packed.u32',u32(bits));
 charge('dispatches',1);charge('gpuValidRoots',n);charge('gpuIterationReservation',12*n);context.phase='GPU dispatch/readback';
 const returned=await gpuBatch(id,bits);
 assert(returned.count===n&&returned.bits.length===n*8,'GPU complete byte coverage',{id,n,count:returned.count,words:returned.bits.length});
 write(id+'-Q.f64',Buffer.alloc(0));write(id+'-A.f64',Buffer.alloc(0));const floats=returned.bits.map(decodeF32),names=['rootOriginalX','rootRepresentedX','originalCubicAtReturnedX','representedCubicAtReturnedX','rotorTotal','inputRepresentation','shaderVersusRepresented','alphaDivision','alphaForceEffect','rootX','rootForceEffect','finalMultiplication','hostResidual','shaderResidual','representedPower','originalPower'];
 const summary={id,n,pass:false,maxima:Object.fromEntries(names.map(k=>[k,{value:0,index:0}])),stops:{'0':0,'1':0,'2':0},exactZeroStepStops:0,iterationCapRecords:0,oldPrecisionFailures:0,gateFailures:0,firstFailure:null};
 context.phase='Scheduled Q64/A64 independent roots';
 for(let i=0;i<n;i++){
  if(i%128===0)guard();const g=floats.slice(8*i,8*i+8);assert(g.every(Number.isFinite)&&g[0]>=0&&g[5]!==3,'GPU returned admitted root',{id,index:i,g});
  context.record=i;context.reference='Q';const q=root(Math.fround(reference[i][0])/VQ);q.f=FQ*q.x;context.latestReference=q;append(id+'-Q.f64',f64([q.alpha,q.x,q.f,q.lo,q.hi,q.iterations]));context.reference='A';const a=root(g[0]);a.f=FQ*a.x;context.latestReference=a;append(id+'-A.f64',f64([a.alpha,a.x,a.f,a.lo,a.hi,a.iterations]));
  compareRecord(reference[i],g,q,a,summary,i);
 }
 summary.distinctOriginalInflows=new Set(reference.map(r=>r[0])).size;summary.distinctPackedInflows=new Set(reference.map(r=>f32Bits(r[0]))).size;summary.pass=summary.gateFailures===0;write(id+'-summary.json',summary);output.batches.push(summary);
 assert(summary.pass,'Prespecified receiver engineering gate unmet',summary.firstFailure);
}
async function invalidBatch(){
 const nominal=f32Bits(FQ),induced=f32Bits(VQ),one=f32Bits(1),bits=[f32Bits(-1),nominal,induced,0,0x7fc00000,nominal,induced,0,0x7f800000,nominal,induced,0,one,nominal,0,0,one,f32Bits(-1),induced,0];
 context={batch:'invalid5',phase:'GPU guarded controls'};write('invalid5-packed.u32',u32(bits));charge('dispatches',1);charge('gpuInvalidGuards',5);
 const r=await gpuBatch('invalid5',bits);assert(r.count===5&&r.bits.length===40,'Guard output coverage');
 const values=r.bits.map(decodeF32);for(let i=0;i<5;i++)assert(values.slice(8*i,8*i+8).every((x,k)=>x===(k===5?3:0)),'Expected invalid sentinel',{index:i,values:values.slice(8*i,8*i+8)});
 const summary={id:'invalid5',n:5,pass:true,meaning:'Expected input guard rejection; sentinel is not a force estimate'};write('invalid5-summary.json',summary);output.batches.push(summary);
}
(async()=>{
 assert(typeof source==='string'&&/^[0-9a-f]{40}$/.test(source),'Published source identity required');assert(Date.now()<Date.parse(cfg.stopNewLaunchUTC),'Overnight launch cutoff');
 fs.mkdirSync(raw,{recursive:true});assert(fs.readdirSync(raw).length===0,'No previous scientific evidence allowed');
 const freezeBytes=fs.readFileSync(path.join(base,'freeze.json')),freeze=JSON.parse(freezeBytes);
 for(const pin of freeze.files){const file=path.resolve(repo,pin.path);assert(file.startsWith(repo+path.sep),'Contained freeze path');const bytes=fs.readFileSync(file);assert(bytes.length===pin.bytes&&sha(bytes)===pin.sha256,'Frozen file mismatch',{path:pin.path});}
 const runtime=JSON.parse(fs.readFileSync(path.join(base,'runtime-provenance.json'))),pwRoot=path.dirname(require.resolve('playwright/package.json')),coreRoot=path.dirname(require.resolve('playwright-core/package.json')),runtimeFiles=[process.execPath,path.join(pwRoot,'package.json'),path.join(pwRoot,'index.js'),path.join(coreRoot,'package.json'),path.join(coreRoot,'index.js'),path.join(coreRoot,'lib/coreBundle.js')];for(let i=0;i<runtimeFiles.length;i++){const b=fs.readFileSync(runtimeFiles[i]),pin=runtime.pins[i];assert(b.length===pin.bytes&&sha(b)===pin.sha256,'Runtime entry pin mismatch',{label:pin.label});}
 write('started.json',{sourceCommit:source,freezeSha256:sha(freezeBytes),config:cfg,node:process.version,platform:process.platform,architecture:process.arch,invocations:1,runtimePinsVerified:runtime.pins});
 ({solveAlpha,powerRatio}=require('./reference.cjs'));F0=.027*9.81/4;const area=Math.PI*.023*.023;VI=Math.sqrt(F0/(2*1.225*area));FQ=Math.fround(F0);VQ=Math.fround(VI);
 const encoding=JSON.parse(fs.readFileSync(path.join(base,'constant-encoding.json')));assert(encoding.f0.binary64LEHex===f64([F0]).toString('hex')&&encoding.vi.binary64LEHex===f64([VI]).toString('hex')&&encoding.f0.binary32Bits===f32Bits(FQ)&&encoding.vi.binary32Bits===f32Bits(VQ)&&cfg.scalarInflows.every((u,i)=>encoding.scalarInflows[i].binary64LEHex===f64([u]).toString('hex')),'Frozen constant/literal bit encodings');assert(FQ>=.01&&FQ<=.1&&VQ>=1&&VQ<=10,'Fixed constants admission');output.constants={F0,VI,FQ,VQ,originalF0Hex:f64([F0]).toString('hex'),originalVIHex:f64([VI]).toString('hex'),packedF0Bits:f32Bits(FQ),packedVIBits:f32Bits(VQ),rho:1.225,area,meaning:'vi is precomputed on host then separately rounded; GPU square root and parameter construction excluded'};write('constants.json',output.constants);
 browser=await chromium.launch({channel:'chrome',headless:true,timeout:20000});assert(processRegistry.hasRegisteredBrowser(),'Browser process was not registered before GPU work');write('process-registration-summary.json',processRegistry.summary());page=await browser.newPage();page.setDefaultTimeout(20000);const faults=[];page.on('pageerror',e=>faults.push(String(e.message)));page.on('console',m=>{if(m.type()==='error')faults.push(m.text());});output.browserVersion=await browser.version();assert(output.browserVersion===runtime.chromeBundleVersion,'Frozen Chrome version changed',{actual:output.browserVersion,expected:runtime.chromeBundleVersion});
 const runnerURL='http://127.0.0.1:8876/research/m31-browser-receiver-2026-10-16/source/',servedSources=[];for(const [name,type]of [['browser.html','text/html'],['browser.js','application/javascript'],['receiver.wgsl','text/plain']]){const bytes=fs.readFileSync(path.join(__dirname,name));await page.route(runnerURL+name,async route=>{servedSources.push({name,bytes:bytes.length,sha256:sha(bytes)});await route.fulfill({status:200,contentType:type,body:bytes});});}write('served-source-contract.json',{files:['browser.html','browser.js','receiver.wgsl'].map(name=>{const b=fs.readFileSync(path.join(__dirname,name));return {name,bytes:b.length,sha256:sha(b)};}),method:'Playwright fulfills exact frozen bytes; no runtime runner from an unchecked server response'});output.servedSources=servedSources;await page.goto(runnerURL+'browser.html');await page.waitForFunction(()=>window.receiverRunnerReady===true);context={phase:'capability/compile'};
 const cap=await deadline(page.evaluate(()=>window.initializeReceiver()),30000,'Complete GPU initialization');
 if(cap.shader){assert(sha(Buffer.from(cap.shader))===sha(fs.readFileSync(path.join(__dirname,'receiver.wgsl'))),'Served shader source hash');delete cap.shader;}
 output.capability=cap;write('capability.json',{browserVersion:output.browserVersion,...cap});
 if(!cap.supported){output.status='unsupported';output.pass=false;return;}
 assert(cap.compiled,'Shader compilation or pipeline validation failed',cap);assert(faults.length===0,'Browser runtime errors',faults);
 const scalar=[];write('scalar32-original.f64',Buffer.alloc(0));for(const U of cfg.scalarInflows){context={batch:'scalar32',phase:'R64',record:scalar.length};const r=root(U/VI),row=[U,F0,VI,r.x,F0*r.x,r.lo,r.hi,r.iterations];append('scalar32-original.f64',f64(row));scalar.push(row);}await validBatch('scalar32',scalar);await invalidBatch();
 for(const c of cfg.savedCases){
  guard();context={batch:c.id,phase:'read prior reference'};const dir=path.join(repo,cfg.sourceReferenceDirectory,'raw'),bytes=fs.readFileSync(path.join(dir,c.id+'-I.f64')),audit=fs.readFileSync(path.join(dir,c.id+'-source-audit.ndjson'),'utf8').trim().split('\n').map(JSON.parse);assert(bytes.length===c.n*17*8&&audit.length===c.n,'Reference matrix/audit coverage',c);
  const rr=[];for(let i=0;i<c.n;i++){assert(audit[i].receiver===i&&audit[i].solutions.length===4,'Original root audit order',{case:c.id,i});for(let k=0;k<4;k++){const U=bytes.readDoubleLE(8*(17*i+k)),f=bytes.readDoubleLE(8*(17*i+4+k)),r=audit[i].solutions[k];assert(f===r.thrust,'Original matrix/audit thrust equality',{case:c.id,i,k});rr.push([U,F0,VI,r.x,f,r.bracket[0],r.bracket[1],r.iterations]);}}
  await validBatch(c.id,rr);
 }
 assert(counts.dispatches===4&&counts.gpuValidRoots===24032&&counts.gpuInvalidGuards===5&&counts.hostBisectionRoots===48096,'Complete scheduled accounting',counts);assert(faults.length===0,'Browser runtime errors',faults);
 const health=await page.evaluate(()=>window.receiverHealth());write('final-gpu-health.json',health);assert(!health.loss&&!health.uncaptured,'Final GPU health',health);output.status='completed';output.pass=true;
})().catch(async e=>{if(page){try{const browserEvidence=await deadline(page.evaluate(()=>({initialization:window.receiverInitializationEvidence??null,dispatch:window.lastDispatchEvidence??null,health:window.receiverHealth?.()??null})),1000,'Failure metadata read');write('browser-failure-evidence.json',browserEvidence,true);}catch(captureError){output.browserFailureEvidenceUnavailable=captureError.message;}}process.exitCode=1;output.status='failed';output.pass=false;output.error={message:e.message,detail:e.detail??null,context};}).finally(async()=>{
 const cleanupErrors=[];if(page){try{await deadline(page.evaluate(()=>window.shutdownReceiver()),2000,'GPU cleanup');}catch(e){cleanupErrors.push(e.message);}}if(browser){try{await deadline(browser.close(),5000,'Browser cleanup');}catch(e){cleanupErrors.push(e.message);}}if(cleanupErrors.length){output.cleanupErrors=cleanupErrors;process.exitCode=1;output.pass=false;if(output.status==='completed')output.status='failed';}
 output.checks=checks;output.counts=counts;output.elapsedSeconds=(performance.now()-start)/1000;output.files=fs.existsSync(raw)?fs.readdirSync(raw).sort().map(name=>{const b=fs.readFileSync(path.join(raw,name));return {name,bytes:b.length,sha256:sha(b)};}):[];output.terminal=true;
 try{write('result.json',output,true);fs.mkdirSync(path.join(base,'results'),{recursive:true});fs.writeFileSync(path.join(base,'results/result.json'),JSON.stringify(output,null,2)+'\n',{flag:'wx'});}catch(e){process.exitCode=1;console.error('Terminal evidence write failed: '+e.message);}
 console.log(JSON.stringify({status:output.status,pass:output.pass,error:output.error,counts,elapsedSeconds:output.elapsedSeconds,rawBytes}));
});
