'use strict';
const start=performance.now();
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto'),zlib=require('node:zlib'),assert=require('node:assert/strict');
const base=path.resolve(__dirname,'..'),root=path.resolve(base,'../..'),out=path.join(base,'results');
const sha=b=>crypto.createHash('sha256').update(b).digest('hex'),load=p=>JSON.parse(fs.readFileSync(p));
const manifestBytes=fs.readFileSync(path.join(base,'source-manifest.json')),manifest=JSON.parse(manifestBytes),pub=load(path.join(base,'source-publication.json'));
assert.equal(pub.manifestSha256,sha(manifestBytes));assert.equal(pub.remoteBytesEqualLocal,true);assert.equal(pub.committedBytesEqualLocal,true);assert.equal(pub.verifiedFilePins,manifest.files.length);
for(const p of manifest.files){const b=fs.readFileSync(path.join(root,p.path));assert.equal(b.length,p.bytes);assert.equal(sha(b),p.sha256,p.path);}
const runtime=load(path.join(base,'runtime.json')),executable=fs.readFileSync(process.execPath);assert.equal(executable.length,runtime.nodeBytes);assert.equal(sha(executable),runtime.nodeSha256);assert.equal(process.execArgv.length,0);assert.ok(!process.env.NODE_OPTIONS);assert.ok(!process.env.NODE_PATH);assert.ok(!process.env.FLOCK_FACTORY_VARIANT||process.env.FLOCK_FACTORY_VARIANT==='wide');process.env.FLOCK_FACTORY_VARIANT='wide';
assert.ok(fs.existsSync(path.join(base,'native-supervisor-launch.lock')));fs.mkdirSync(out);fs.writeFileSync(path.join(out,'launch.json'),JSON.stringify({sourceCommit:pub.commit,startedUtc:new Date().toISOString(),node:process.version,versions:process.versions})+'\n',{flag:'wx'});
const config=load(path.join(base,'config.json'));
const storage=load(path.join(base,'storage/qualification.json')),storageSupervisor=load(path.join(base,'storage-supervisor.json'));assert.equal(storage.passed,true);assert.equal(storage.closed,true);assert.equal(storageSupervisor.returncode,0);assert.equal(storageSupervisor.allocationWallPassed,true);assert.equal(storageSupervisor.outputCapPassed,true);assert.ok(storageSupervisor.wallSeconds<=20);assert.ok(!storageSupervisor.timeout);
const priorBase=path.join(root,'research/m31-boids-admission-2026-10-20'),priorIndex=load(path.join(priorBase,'results/index.json'));
const priorManifestBytes=fs.readFileSync(path.join(priorBase,'result-manifest.json')),priorManifest=JSON.parse(priorManifestBytes),priorReceipt=load(path.join(root,'research/publication-receipts/m31-boids-admission-result-2026-10-20.json'));
assert.equal(priorReceipt.commit,'637c25294f162bea39970d12df0206f25dead889');assert.equal(priorReceipt.manifestSha256,sha(priorManifestBytes));assert.equal(priorReceipt.remoteBytesEqualLocal,true);assert.equal(priorReceipt.committedBytesEqualLocal,true);
for(const name of ['results/index.json','audit/audit.json','ALLOCATION-CLOSURE.json','results/exit.json','audit/exit.json','native-supervisor.json','audit-supervisor.json']){const pin=priorManifest.files.find(x=>x.path==='research/m31-boids-admission-2026-10-20/'+name),raw=fs.readFileSync(path.join(priorBase,name));assert.ok(pin);assert.equal(raw.length,pin.bytes);assert.equal(sha(raw),pin.sha256);}
assert.equal(load(path.join(priorBase,'audit/audit.json')).passed,true);assert.equal(priorIndex.complete,true);
const priorClosure=load(path.join(priorBase,'ALLOCATION-CLOSURE.json'));for(const key of ['native','audit','display','archive']){assert.equal(priorClosure[key].status,'closed-passed');assert.equal(priorClosure[key].attempts,1);}
for(const [phase,limit] of [['native',360],['audit',180]]){const sup=load(path.join(priorBase,phase+'-supervisor.json')),ex=load(path.join(priorBase,phase==='native'?'results/exit.json':'audit/exit.json'));assert.equal(sup.returncode,0);assert.equal(sup.allocationWallPassed,true);assert.ok(!sup.timeout);assert.ok(sup.wallSeconds<=limit);assert.equal(ex.exitCode,0);assert.equal(ex.closed,true);assert.ok(ex.wallSeconds<=limit);}
const {Journal}=require('./journal.cjs');let bytes=fs.statSync(path.join(out,'launch.json')).size,totalNativeCalls=0,totalStages=0,journal=null,sequence=0,currentCase=null,lastStage=null;
const index={schema:'m31-boids-continuation-index-v1',complete:false,config,cases:[],totalNativeCalls:0,sourceCommit:pub.commit};
function guard(){if(performance.now()-start>config.maxWallSeconds*1000)throw Error('global-wall-budget');if(bytes>config.maxOutputBytes-1048576)throw Error('global-output-budget');}
function append(kind,body){guard();journal.append({sequence,kind,body});sequence++;if(kind==='stage'){lastStage=body;totalStages++;}return Promise.resolve();}
// No model, initializer or controller module is imported before the public gate.
const A=require('../../m31-coupled-stage-qualification-2026-10-17/source/adapter.cjs');
const F=require('../../m31-native-fresh-transfer-2026-10-17/source/vendor/generation/step02c-source/physics.cjs');
const S=require('../../m31-native-fresh-transfer-2026-10-17/source/vendor/generation/milestone-31-source/sim.cjs');
const native=require('../../m31-native-fresh-transfer-2026-10-17/source/native-load.cjs');
const M=require('./motion.cjs');
const checkedNative={encodeEvidence:native.encodeEvidence,query(input,method,g){guard();assert.equal(method,'F');assert.ok(totalNativeCalls<config.maxNativeCalls);totalNativeCalls++;return native.query(input,method,g);}};
const adapter=A.createAdapter({physics:F,native:checkedNative});
async function runCase(c){
 currentCase=c.caseId;sequence=0;lastStage=null;const file=c.caseId+'.jsonl.gz';journal=new Journal(out,file,{guard,charge(n){guard();if(bytes+n>config.maxOutputBytes-1048576)throw Error('global-output-budget');bytes+=n;},maxRecordBytes:config.maxRecordBytes});
 const prior=priorIndex.cases.find(x=>x.caseId===c.caseId);assert.ok(prior);assert.equal(prior.status,'completed');assert.equal(prior.lastTime,1);
 let drones=prior.finalInput.drones.map(({id,state})=>({id,state:state.map(A.number)})),commands=null,completedSteps=0,attemptedStages=0,status='completed',reason=null,refusal=null;
 await append('initial',{caseId:c.caseId,input:A.inputWords(drones)});
 try{
  for(let stepIndex=0;stepIndex<c.steps;stepIndex++){
   guard();
   if(stepIndex%c.stepsPerControl===0){const update=M.control(drones,'coupled',stepIndex,{integration:{dt:c.dt,stepsPerControl:c.stepsPerControl,timeOrigin:config.timeOrigin}});commands=update.commands;await append('controller',update.record);}
   const old=A.copyDrones(drones),before=totalStages;let next;
   try{next=await adapter.step({drones,commands,arm:'coupled',stepIndex,dt:c.dt,timeOrigin:config.timeOrigin,append,guard});}finally{attemptedStages+=totalStages-before;}
   drones=next;completedSteps++;
   const issues=M.safety(old,drones);await append('safety',{stepIndex,issues,pass:issues.length===0});if(issues.length){status='stopped';reason='endpoint-contact-or-vehicle-limit';break;}
  }
 }catch(e){
  // Resource, persistence and unexpected implementation failures end the entire
  // allocation. Only a saved, structured native refusal ends this case alone.
  const n=lastStage?.native;
  if(e.message==='native-non-success'&&lastStage.status==='failed'&&n&&['domain-refused','input-refused','numerical-failure'].includes(n.status)){
   status='stopped';reason='native-refusal';refusal={status:n.status,reason:n.reason,stage:n.stage,admission:n.diagnostics?.admission??null,stepIndex:lastStage.stepIndex,stageIndex:lastStage.stageIndex,relativeTimeWord:lastStage.relativeTimeWord};
  }else throw e;
 }
 const end={caseId:c.caseId,completedSteps,attemptedStages,status,reason,refusal,lastTime:completedSteps*c.dt,finalInput:A.inputWords(drones)};await append('case-end',end);const identity=journal.finish();assert.equal(identity.records,sequence);journal=null;index.cases.push({...end,journal:identity});currentCase=null;
}
(async()=>{try{assert.equal(S.course.id,'factory-v1');assert.equal(S.P.controlDt,.01);assert.equal(F.P.controlDt,.01);for(const c of config.cases)await runCase(c);index.complete=true;}catch(e){index.failure={caseId:currentCase,message:String(e.message).replaceAll(root,'[repository]'),acknowledgedRecords:sequence,pendingRawBytes:journal?.blockSize??0};process.exitCode=1;}finally{if(journal!==null){journal.closeIncomplete();}try{guard();for(const p of manifest.files){assert.equal(sha(fs.readFileSync(path.join(root,p.path))),p.sha256,p.path);}guard();}catch(e){index.complete=false;index.failure={caseId:currentCase,message:String(e.message).replaceAll(root,'[repository]'),phase:'final-source-and-budget-check'};process.exitCode=1;}index.totalNativeCalls=totalNativeCalls;index.totalStages=totalStages;index.wallSeconds=(performance.now()-start)/1000;index.outputBytesBeforeIndex=bytes;index.nativeTimingIsNotBenchmark=true;fs.writeFileSync(path.join(out,'index.json'),JSON.stringify(index)+'\n',{flag:'wx'});fs.writeFileSync(path.join(out,'exit.json'),JSON.stringify({exitCode:process.exitCode||0,wallSeconds:(performance.now()-start)/1000,closed:true})+'\n',{flag:'wx'});guard();}})();
