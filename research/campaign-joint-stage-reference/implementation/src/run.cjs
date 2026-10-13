'use strict';
const crypto=require('crypto');
const M=require('./exact-aero.cjs'),{source}=require('./source.cjs'),{B,controller}=require('./controller.cjs');
const G=source('outputs/milestone-31-source/geometry.cjs');
const {jointStep}=require('./joint-step.cjs'),{BranchAudit}=require('./branch-audit.cjs');
const {sha,rawBytes,writeRaw,save,atomicWrite}=require('./io.cjs'),{writeControllers}=require('./controller-record.cjs');
const Q=1/51200;
function run(seed,row,{budgetCheck=()=>{},checkpoint=()=>{}}={}){
 const recordTicks=row.arm==='compatibility'?row.stepTicks:32;
 const id=`s${seed}-${row.arm}`,start=performance.now(),cpu0=process.cpuUsage(),field=M.createEvaluator({variant:'lean'}),audit=new BranchAudit(id),common=[],dense=[],events=[],controlEvents=[];
 const timing={field:0,controller:0,rkArithmetic:0,safetyDiagnostics:0,recordingHash:0};
 const work={physicsSteps:0,rk4DerivativeCalls:0,fieldUpdates:0,controllerUpdates:0,rotorKernels:0,candidatePairs:0,safetySteps:0,jointStageFields:0,acceptedEndpointAudits:0,productionRefreshAuditAliases:0,fieldAttempts:0,derivativeAttempts:0,heldIntegratorAttempts:0,heldIntegratorCompleted:0,heldDerivativeAttemptUpperBound:0};
 let Y=B.initial(seed,16),winds=Y.map(()=>[0,0,0,0]),commands=null,tick=0,heldTick=null,stop=null,current=null,endpoint=null,projectionMaximum=0,normDefectMaximum=0,projectionWorst=null,normDefectWorst=null;
 let minPairClearance=Infinity,minObstacleClearance=Infinity,maxInflow=0,minMotor=Infinity,maxMotor=-Infinity;
 const initial=Y.map(s=>s.slice()),inputHash=crypto.createHash('sha256'),stateHash=crypto.createHash('sha256'),stageHash=crypto.createHash('sha256');
 function timed(key,fn){const at=performance.now();try{return fn();}finally{timing[key]+=performance.now()-at;}}
 function record(){timed('recordingHash',()=>{const flat=Y.flat();stateHash.update(rawBytes(Y));if(tick%recordTicks===0)common.push(flat);if(row.dense)dense.push(flat);});}
 function fieldCounters(f){work.rotorKernels+=f.counters.evaluatedRotorKernels;work.candidatePairs+=f.counters.candidates;maxInflow=Math.max(maxInflow,f.maximumInflow);}
 function inspectEndpoint(){work.acceptedEndpointAudits++;return timed('safetyDiagnostics',()=>audit.observe(Y,{tick,time:tick*Q,role:'endpoint'},{comparePrevious:row.kind!=='joint'}));}
 function safe(old){for(let i=0;i<16;i++){const s=Y[i];if(!s.every(Number.isFinite)||Math.abs(Math.hypot(...s.slice(6,10))-1)>1e-10||s[2]<B.P.bodyRadius)throw Object.assign(Error('Endpoint model limit'),{detail:{drone:i}});for(const f of s.slice(13,17)){minMotor=Math.min(minMotor,f);maxMotor=Math.max(maxMotor,f);if(f<0)throw Error('Negative nominal endpoint motor thrust');}const hits=B.obstacleContacts(old[i],s);if(hits.length)throw Object.assign(Error('Obstacle contact envelope'),{detail:{drone:i,hits}});for(const box of B.course.boxes)minObstacleClearance=Math.min(minObstacleClearance,G.boxDistance(s,box).distance-B.P.bodyRadius);}
  for(const [i,j]of B.contactCandidates(old,Y)){const distance=G.segmentPair(old[i],Y[i],old[j],Y[j]);if(distance<2*B.P.bodyRadius)throw Object.assign(Error('Drone contact envelope'),{detail:{pair:[i,j],distance}});}
  for(let i=0;i<16;i++)for(let j=i+1;j<16;j++)minPairClearance=Math.min(minPairClearance,G.segmentPair(old[i],Y[i],old[j],Y[j])-2*B.P.bodyRadius);work.safetySteps++;
 }
 try{
  current={phase:'initial-endpoint',tick,state:Y};endpoint=inspectEndpoint();record();
  while(tick<51200){
   budgetCheck();if([51200,512,recordTicks].some(period=>period%row.stepTicks)||(row.kind==='held'&&row.airTicks%row.stepTicks))throw Error('Misaligned frozen schedule');
   if(row.kind==='held'&&tick%row.airTicks===0){current={phase:'production-field',tick,state:Y,commands};work.fieldAttempts++;const f=timed('field',()=>field(Y));winds=f.winds;heldTick=tick;fieldCounters(f);work.fieldUpdates++;work.productionRefreshAuditAliases++;events.push({tick,type:'field',heldTick,inputStateSha256:sha(JSON.stringify(Y)),heldWindsSha256:sha(JSON.stringify(winds)),auditObservation:audit.samples-1,auditSignatureSha256:endpoint.signatureSha256});}
   if(tick%512===0){current={phase:'controller',tick,state:Y,commands};const c=timed('controller',()=>controller(Y,tick));commands=c.commands;controlEvents.push(c.event);work.controllerUpdates++;}
   timed('recordingHash',()=>inputHash.update(JSON.stringify([tick,heldTick,Y,winds,commands])));
   const old=Y,previousEndpoint=endpoint,stepSamples=[];
   current={phase:'physics',tick,state:Y,commands,heldWinds:winds};
   if(row.kind==='joint'){
    const before=performance.now();let nested=0;
    Y=jointStep(Y,commands,row.stepTicks*Q,{
     beforeDerivative:()=>{work.derivativeAttempts++;},afterDerivative:()=>{work.rk4DerivativeCalls++;},
     field:geometry=>{work.fieldAttempts++;const at=performance.now();const f=timed('field',()=>field(geometry));nested+=performance.now()-at;fieldCounters(f);work.jointStageFields++;return f;},
     beforeStage:data=>{current={phase:'joint-stage',tick:tick+data.fraction*row.stepTicks,stage:data.stage,state:data.raw,geometry:data.geometry,commands};const at=performance.now();const s=timed('safetyDiagnostics',()=>audit.observe(data.geometry,{tick:tick+data.fraction*row.stepTicks,time:(tick+data.fraction*row.stepTicks)*Q,role:'stage',stage:data.stage},{comparePrevious:false,raw:data.raw}));nested+=performance.now()-at;stepSamples.push(s);data.raw.forEach((s,drone)=>{const value=Math.abs(Math.hypot(...s.slice(6,10))-1);if(value>normDefectMaximum){normDefectMaximum=value;normDefectWorst={tick:tick+data.fraction*row.stepTicks,stage:data.stage,drone,value};}});},
     afterStage:data=>{const at=performance.now();timed('recordingHash',()=>stageHash.update(JSON.stringify([tick,data.stage,data.raw,data.geometry,commands,data.result.winds,data.derivatives])));nested+=performance.now()-at;},
     onProjection:data=>{data.projectionSizes.forEach((value,drone)=>{if(value>projectionMaximum){projectionMaximum=value;projectionWorst={tick:tick+row.stepTicks,drone,value};}});}
    });timing.rkArithmetic+=performance.now()-before-nested;
   }else Y=timed('rkArithmetic',()=>Y.map((s,i)=>{current.vehicle=i;work.heldIntegratorAttempts++;work.heldDerivativeAttemptUpperBound+=4;const out=M.integrate(s,commands[i],row.stepTicks*Q,winds[i],'sum-rotor');work.rk4DerivativeCalls+=4;work.heldIntegratorCompleted++;return out;}));
   tick+=row.stepTicks;work.physicsSteps++;current={phase:'accepted-endpoint',tick,state:Y,commands,heldWinds:winds};
   timed('safetyDiagnostics',()=>safe(old));endpoint=inspectEndpoint();
   timed('safetyDiagnostics',()=>{
    if(row.kind==='joint'){audit.compare(previousEndpoint,endpoint);for(let k=1;k<stepSamples.length;k++)audit.compare(stepSamples[k-1],stepSamples[k]);audit.compare(stepSamples.at(-1),endpoint);audit.checkStep([previousEndpoint,...stepSamples,endpoint]);}
    else audit.checkStep([previousEndpoint,endpoint]);
   });
   record();if(work.physicsSteps%128===0)checkpoint({runId:id,...current,exactStoppedState:false,meaning:'Last durable checkpoint only'});
  }
 }catch(e){stop={runId:id,...current,...(e.stageEvidence?{phase:'joint-stage',tick:tick+e.stageEvidence.fraction*row.stepTicks,stage:e.stageEvidence.stage,state:e.stageEvidence.raw,geometry:e.stageEvidence.geometry}:{}),...(e.endpointEvidence?{phase:'endpoint-projection',state:e.endpointEvidence.rawCombinedEndpoint}:{}),type:e.constructor.name,message:e.message,detail:e.detail||null,stageEvidence:e.stageEvidence||null,endpointEvidence:e.endpointEvidence||null,exactStoppedState:!(row.kind==='held'&&current?.phase==='physics'),exactIntegratorInput:row.kind==='held'&&current?.phase==='physics',internalFailingStageUnavailable:row.kind==='held'&&current?.phase==='physics'};save(`results/failures/${id}.json`,stop);}
 const cpu=process.cpuUsage(cpu0),complete=!stop&&tick===51200;
 const fieldBuffer=Buffer.concat(events.map(e=>Buffer.from(e.heldWindsSha256,'hex')));atomicWrite(`results/fields/${id}.bin`,fieldBuffer);const fieldEvents={path:`results/fields/${id}.bin`,bytes:fieldBuffer.length,sha256:sha(fieldBuffer),count:events.length,encoding:'32 raw SHA256 bytes of JSON.stringify(held rotor winds) per production refresh',tickSchedule:'k*airTicks, k=0..count-1; no terminal refresh',auditAlias:'Accepted endpoint observation at index tick/stepTicks. Exact same state bytes; hash in audit signature stream.',firstInputStateSha256:events[0]?.inputStateSha256||null,lastInputStateSha256:events.at(-1)?.inputStateSha256||null};
 const result={runId:id,config:{seed,...row,count:16,duration:1,physicsDt:row.stepTicks*Q,airDt:row.airTicks?row.airTicks*Q:null,baseTickSeconds:Q,controlTicks:512,commonTicks:recordTicks},complete,endTick:tick,stop,initial,final:Y,finalWinds:row.kind==='held'?winds:null,heldTick,terminalStateWindSha256:row.kind==='held'?sha(JSON.stringify([Y,winds])):null,terminalFieldMeaning:row.kind==='joint'?'No accepted endpoint field value claimed; final stage is a trial geometry and held wind is inapplicable':'Final production-held scalar inflows; no terminal refresh',stateStreamSha256:stateHash.digest('hex'),integrationInputStreamSha256:inputHash.digest('hex'),jointStageStreamSha256:stageHash.digest('hex'),stageHashEncoding:'Concatenated JSON.stringify([stepStartTick,stage,rawStage,geometryCopy,commands,field,derivatives])',work,timing:{...timing,total:performance.now()-start,cpuMs:(cpu.user+cpu.system)/1000},metrics:{minPairClearance,minObstacleClearance,maxInflow,minMotor,maxMotor,projectionMaximum,normDefectMaximum,projectionWorst,normDefectWorst},fieldEvents,audit:audit.finish(),controllers:writeControllers(id,controlEvents),signatureSchedule:row.kind==='joint'?'Initial accepted endpoint; each step stage1,stage2,stage3,stage4,accepted endpoint. Partial prefix length is audit.samples.':'Initial accepted endpoint then each accepted endpoint; production refresh aliases the same index; no terminal refresh.',claim:'Genuine local 3D Boids on own evolving state; physically unvalidated model'};
 // J3 common rows are views into its dense artifact, not a duplicate raw file.
 if(row.dense){result.denseStates=writeRaw(`results/raw/${id}.dense.f64`,dense,{count:16,runId:id,dt:row.stepTicks*Q,baseTickSeconds:Q,cadenceTicks:row.stepTicks});result.commonView={source:result.denseStates.path,stride:32/row.stepTicks};}
 else if(common.length)result.commonStates=writeRaw(`results/raw/${id}.common.f64`,common,{count:16,runId:id,dt:recordTicks*Q,baseTickSeconds:Q,cadenceTicks:recordTicks});
 const allCpu=process.cpuUsage(cpu0);result.timing.totalBeforeFinalRunRecordWrite=performance.now()-start;result.timing.cpuMsBeforeFinalRunRecordWrite=(allCpu.user+allCpu.system)/1000;result.timing.totalScope='total/cpuMs cover numerical loop only; totalBeforeFinalRunRecordWrite includes artifact serialization; scheduler job timing includes final record serialization';save(`results/runs/${id}.json`,result);return {result,common,dense,controlEvents};
}
module.exports={run,Q};
