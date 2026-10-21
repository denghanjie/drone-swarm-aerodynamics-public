 'use strict';
const start=performance.now(),fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const C=require('./gate.cjs'),{base,root,load}=C,out=path.join(base,'results');
assert.ok(fs.existsSync(path.join(base,'producer-supervisor-launch.lock')));fs.mkdirSync(out);
const config=load(path.join(base,'config.json'));let bytes=0,totalNativeCalls=0,lastStage=null,totalStages=0,journal=null,sequence=0,currentCase=null;
const index={schema:'m31-vertical-memory-v1',complete:false,config,cases:[],totalNativeCalls:0,totalStages:0};
function guard(){if(performance.now()-start>config.maxWallSeconds*1000)throw Error('global-wall-budget');if(bytes>config.maxOutputBytes-1048576)throw Error('global-output-budget');}
function append(kind,body){guard();journal.append({sequence,kind,body});sequence++;if(kind==='stage'){lastStage=body;totalStages++;assert.ok(totalStages<=config.maxStages);}return Promise.resolve();}
(async()=>{try{
const pub=C.gate();index.sourceCommit=pub.commit;const runtime=load(path.join(base,'runtime.json'));C.checked(process.execPath,{bytes:runtime.nodeBytes,sha256:runtime.nodeSha256});assert.equal(process.execArgv.length,0);assert.ok(!process.env.NODE_OPTIONS);assert.ok(!process.env.NODE_PATH);assert.ok(!process.env.FLOCK_FACTORY_VARIANT||process.env.FLOCK_FACTORY_VARIANT==='wide');process.env.FLOCK_FACTORY_VARIANT='wide';
fs.writeFileSync(path.join(out,'launch.json'),JSON.stringify({sourceCommit:pub.commit,startedUtc:new Date().toISOString(),node:process.version})+'\n',{flag:'wx'});bytes=fs.statSync(path.join(out,'launch.json')).size;
const {Journal}=require('../../m31-boids-continuation-2026-10-20/source/journal.cjs');
const storage=load(path.join(root,'research/m31-boids-continuation-2026-10-20/storage/qualification.json')),ss=load(path.join(root,'research/m31-boids-continuation-2026-10-20/storage-supervisor.json'));assert.ok(storage.passed&&storage.closed);assert.equal(ss.returncode,0);assert.ok(ss.allocationWallPassed&&ss.outputCapPassed&&!ss.timeout);
const A=require('../../m31-coupled-stage-qualification-2026-10-17/source/adapter.cjs'),F=require('../../m31-native-fresh-transfer-2026-10-17/source/vendor/generation/step02c-source/physics.cjs'),S=require('../../m31-native-fresh-transfer-2026-10-17/source/vendor/generation/milestone-31-source/sim.cjs'),M=require('./motion.cjs');
const native=require('../../m31-native-fresh-transfer-2026-10-17/source/native-load.cjs');
const checkedNative={encodeEvidence:native.encodeEvidence,query(input,method,g){guard();assert.equal(method,'F');assert.ok(totalNativeCalls<config.maxNativeCalls);totalNativeCalls++;return native.query(input,method,g);}};
const adapter=A.createAdapter({physics:F,native:checkedNative});
assert.equal(S.course.id,'factory-v1');assert.equal(S.P.controlDt,.01);assert.equal(F.P.controlDt,.01);
for(const c of config.cases){currentCase=c.caseId;let drones=S.initial(c.seed,config.n).map((state,id)=>({id,state})),memory=M.initialMemory(config.n),whole={...c,segments:[],completedSteps:0,attemptedStages:0};
 for(const seg of config.segments){sequence=0;lastStage=null;const file=c.caseId+'-s'+seg.segment+'.jsonl.gz';journal=new Journal(out,file,{guard,charge(n){guard();if(bytes+n>config.maxOutputBytes-1048576)throw Error('global-output-budget');bytes+=n;},maxRecordBytes:config.maxRecordBytes});
  memory=M.memoryWords(memory).map(x=>({id:x.id,integral:A.number(x.integralWord),previousError:A.number(x.previousErrorWord),updates:x.updates}));
  drones=A.inputWords(drones).drones.map(x=>({id:x.id,state:x.state.map(A.number)}));
  await append('initial',{caseId:c.caseId,segment:seg.segment,timeOrigin:seg.timeOrigin,input:A.inputWords(drones),controllerMemory:M.memoryWords(memory)});
  let commands=null,completedSteps=0,status='completed',reason=null,refusal=null,terminationIssues=[];const before=totalStages,steps=Math.round(seg.duration/c.dt);
  try{for(let stepIndex=0;stepIndex<steps;stepIndex++){guard();if(stepIndex%c.stepsPerControl===0){const update=M.control(drones,'coupled',stepIndex,{integration:{dt:c.dt,stepsPerControl:c.stepsPerControl,timeOrigin:seg.timeOrigin}},memory);commands=update.commands;await append('controller',update.record);}
   const old=A.copyDrones(drones);drones=await adapter.step({drones,commands,arm:'coupled',stepIndex,dt:c.dt,timeOrigin:seg.timeOrigin,append,guard});completedSteps++;
   const issues=M.safety(old,drones);await append('safety',{stepIndex,issues,pass:issues.length===0});if(issues.length){terminationIssues=issues;status='stopped';reason='endpoint-contact-or-vehicle-limit';break;}
  }
  }catch(e){const n=lastStage?.native;if(e.message==='native-non-success'&&lastStage.status==='failed'&&n&&['domain-refused','input-refused','numerical-failure'].includes(n.status)){status='stopped';reason='native-refusal';refusal={status:n.status,reason:n.reason,stage:n.stage,admission:n.diagnostics?.admission??null,stepIndex:lastStage.stepIndex,stageIndex:lastStage.stageIndex,relativeTimeWord:lastStage.relativeTimeWord};}else throw e;}
  const end={caseId:c.caseId,segment:seg.segment,timeOrigin:seg.timeOrigin,completedSteps,attemptedStages:totalStages-before,status,reason,refusal,lastTime:completedSteps*c.dt,finalInput:A.inputWords(drones),controllerMemory:M.memoryWords(memory),terminationIssues};await append('case-end',end);const identity=journal.finish();assert.equal(identity.records,sequence);journal=null;whole.segments.push({...end,journal:identity});whole.completedSteps+=completedSteps;whole.attemptedStages+=end.attemptedStages;Object.assign(whole,{status,reason,refusal,controllerMemory:end.controllerMemory,lastTime:seg.timeOrigin+end.lastTime,finalInput:end.finalInput,terminationIssues});if(status==='stopped')break;
 }
 index.cases.push(whole);currentCase=null;
}
index.complete=true;
}catch(e){index.failure={caseId:currentCase,message:String(e.message).replaceAll(root,'[repository]'),acknowledgedRecords:sequence,pendingRawBytes:journal?.blockSize??0};process.exitCode=1;}finally{
 if(journal!==null)journal.closeIncomplete();try{guard();C.gate();guard();}catch(e){index.complete=false;index.failure={caseId:currentCase,message:String(e.message).replaceAll(root,'[repository]'),phase:'final-source-and-budget-check'};process.exitCode=1;}
 index.totalNativeCalls=totalNativeCalls;index.totalStages=totalStages;index.wallSeconds=(performance.now()-start)/1000;index.outputBytesBeforeIndex=bytes;index.readEvents=C.events;index.timingIsNotBenchmark=true;fs.writeFileSync(path.join(out,'index.json'),JSON.stringify(index)+'\n',{flag:'wx'});fs.writeFileSync(path.join(out,'exit.json'),JSON.stringify({exitCode:process.exitCode||0,wallSeconds:(performance.now()-start)/1000,closed:true})+'\n',{flag:'wx'});guard();}})();
