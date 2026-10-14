'use strict';
const crypto=require('crypto');
const M=require('./exact-aero.cjs'),{source}=require('./source.cjs');
const B=source('outputs/milestone-31-source/sim.cjs'),{Grid}=source('outputs/milestone-31-source/grid.cjs'),G=source('outputs/milestone-31-source/geometry.cjs');
const {sha,save,writeSeries}=require('./io.cjs');
const Q=1/6400;
const fields=['px','py','pz','vx','vy','vz','qx','qy','qz','qw','wx','wy','wz','nominal_f0','nominal_f1','nominal_f2','nominal_f3'];
function ticks(t){const n=Math.round(t/Q);if(Math.abs(t-n*Q)>1e-12||n<1)throw Error('Non-integral positive schedule');return n;}
function run({seed,count=16,duration=1,physicsDt,airDt,dense=false,compatibility=false,budgetCheck=()=>{}}){
 const stepTicks=ticks(physicsDt),airTicks=ticks(airDt),controlTicks=ticks(B.P.controlDt),endTick=ticks(duration),recordTicks=compatibility?stepTicks:4;
 if(count!==16||duration!==1||[airTicks,controlTicks,endTick,recordTicks].some(x=>x%stepTicks))throw Error('Unsupported bounded schedule');
 const runId=`s${seed}-p${stepTicks}-a${airTicks}`,started=performance.now(),cpuStart=process.cpuUsage(),evaluate=M.createEvaluator({variant:'lean'});
 const timing={field:0,controller:0,physics:0,safety:0,recording:0},work={physicsSteps:0,rk4DerivativeCalls:0,fieldUpdates:0,controllerUpdates:0,rotorKernels:0,candidatePairs:0,safetySteps:0};
 let states=B.initial(seed,count),winds=states.map(()=>[0,0,0,0]),controls,heldTick=null,tick=0,stop=null,minMotor=Infinity,maxMotor=-Infinity,minPairClearance=Infinity,minObstacleClearance=Infinity,maxInflow=0,peakRss=process.memoryUsage().rss;
 const initial=states.map(s=>s.slice()),common=[],driver=[],events=[],hash=crypto.createHash('sha256'),inputHash=crypto.createHash('sha256');
 for(const s of states){for(const f of s.slice(13,17)){minMotor=Math.min(minMotor,f);maxMotor=Math.max(maxMotor,f);}for(const box of B.course.boxes)minObstacleClearance=Math.min(minObstacleClearance,G.boxDistance(s,box).distance-B.P.bodyRadius);}
 for(let i=0;i<count;i++)for(let j=i+1;j<count;j++)minPairClearance=Math.min(minPairClearance,Math.hypot(...[0,1,2].map(k=>states[i][k]-states[j][k]))-2*B.P.bodyRadius);
 function record(){const at=performance.now(),flat=states.flat();const b=Buffer.alloc(flat.length*8);flat.forEach((x,k)=>b.writeDoubleLE(x,k*8));hash.update(b);if(tick%recordTicks===0)common.push(flat);if(dense)driver.push(flat);timing.recording+=performance.now()-at;}
 function checkpoint(phase){save('results/last-checkpoint.json',{runId,phase,tick,time:tick*Q,heldTick,state:states,heldWinds:winds,commands:controls?.map(c=>c.u)||null,exactStoppedState:false,meaning:'Last durable checkpoint only unless a separate exact failure record supersedes it'});}
 function fail(e,phase){stop={runId,phase,type:e.constructor.name,message:e.message,detail:e.detail||null,tick,time:tick*Q,heldTick,state:states.map(s=>s.slice()),heldWinds:winds.map(w=>w.slice()),attemptedFieldInputs:phase==='field'?states.map(s=>s.slice()):null,exactStoppedState:true};save(`results/failures/${runId}.json`,stop);}
 record();
 checkpoint('initialized-before-first-field');
 while(tick<endTick){
  try{budgetCheck();if(performance.now()-started>45000)throw Error('Per-job 45-second wall cap');}catch(e){fail(e,'budget');break;}
  if(tick%airTicks===0){const at=performance.now();try{const f=evaluate(states);winds=f.winds;heldTick=tick;maxInflow=Math.max(maxInflow,f.maximumInflow);work.fieldUpdates++;work.rotorKernels+=f.counters.evaluatedRotorKernels;work.candidatePairs+=f.counters.candidates;events.push({tick,type:'field',heldTick,heldWindsSha256:sha(JSON.stringify(winds)),inputStateSha256:sha(JSON.stringify(states)),maximumInflow:f.maximumInflow,contributions:f.counters.contributions});}catch(e){fail(e,'field');}timing.field+=performance.now()-at;if(stop)break;}
  if(tick%controlTicks===0){const at=performance.now(),grid=new Grid(states,B.P.neighbor);controls=states.map((s,i)=>{const v=B.steer(i,states,grid.neighbors(i,B.P.neighbor),'boids','wall-priority');return M.F.control(s,{vx:v[0],vy:v[1],z:s[2]+(2.5*v[2]+1.5*s[5])/6,yaw:Math.atan2(v[1],v[0])},2.25);});work.controllerUpdates++;events.push({tick,type:'controller',heldTick,commandsSha256:sha(JSON.stringify(controls.map(c=>c.u)))});timing.controller+=performance.now()-at;}
  const ht=performance.now();inputHash.update(JSON.stringify([tick,heldTick,states,winds,controls.map(c=>c.u)]));timing.recording+=performance.now()-ht;
  const old=states,at=performance.now();try{states=states.map((s,i)=>M.integrate(s,controls[i].u,physicsDt,winds[i],'sum-rotor'));work.physicsSteps++;work.rk4DerivativeCalls+=4*count;tick+=stepTicks;}catch(e){fail(e,'physics');}timing.physics+=performance.now()-at;if(stop)break;
  const st=performance.now();try{for(let i=0;i<count;i++){
   const s=states[i];if(!s.every(Number.isFinite))throw Object.assign(Error('Nonfinite state'),{detail:{drone:i}});
   if(Math.abs(Math.hypot(...s.slice(6,10))-1)>1e-10)throw Object.assign(Error('Invalid quaternion'),{detail:{drone:i}});
   if(s[2]<B.P.bodyRadius)throw Object.assign(Error('Vehicle model limit'),{detail:{drone:i}});
   for(const f of s.slice(13,17)){minMotor=Math.min(minMotor,f);maxMotor=Math.max(maxMotor,f);if(f<0)throw Object.assign(Error('Negative endpoint nominal thrust'),{detail:{drone:i,value:f}});}
   const hits=B.obstacleContacts(old[i],s);if(hits.length)throw Object.assign(Error('Obstacle contact envelope'),{detail:{drone:i,hits}});
   for(const box of B.course.boxes)minObstacleClearance=Math.min(minObstacleClearance,G.boxDistance(s,box).distance-B.P.bodyRadius);
  }
  // Frozen production broad-phase and ordering determine authoritative stops.
  for(const [i,j] of B.contactCandidates(old,states)){const d=G.segmentPair(old[i],states[i],old[j],states[j]);if(d<2*B.P.bodyRadius)throw Object.assign(Error('Drone contact envelope'),{detail:{pair:[i,j],distance:d}});}
  // Additional all-pair diagnostic cannot change accepted dynamics or stop order.
  for(let i=0;i<count;i++)for(let j=i+1;j<count;j++){const d=G.segmentPair(old[i],states[i],old[j],states[j]);minPairClearance=Math.min(minPairClearance,d-2*B.P.bodyRadius);}
  work.safetySteps++;
  }catch(e){fail(e,'safety');}timing.safety+=performance.now()-st;
  record();if(work.physicsSteps%100===0){peakRss=Math.max(peakRss,process.memoryUsage().rss);checkpoint('post-step');}if(stop)break;
 }
 const cpu=process.cpuUsage(cpuStart);timing.total=performance.now()-started;timing.cpuMs=(cpu.user+cpu.system)/1000;
 const complete=!stop&&tick===endTick,terminalStateWindSha256=sha(JSON.stringify([states,winds]));
 checkpoint('terminal-or-stopped');
 const result={runId,config:{seed,count,duration,physicsDt,airDt,stepTicks,airTicks,controlTicks,commonRecordTicks:recordTicks,baseTickSeconds:Q,dense,compatibility,controller:'unchanged local 3D Boids / wall-priority',fieldVariant:'lean'},complete,endTick:tick,endTime:tick*Q,stop,initial,final:states,finalWinds:winds,heldTick,terminalStateWindSha256,stateStreamSha256:hash.digest('hex'),integrationInputStreamSha256:inputHash.digest('hex'),integrationInputHashEncoding:'Concatenated JSON.stringify([tick,heldTick,full17States,heldScalarInflows,heldCommands]) before every integration step; no terminal refresh.',eventHashEncoding:'SHA256(JSON.stringify(actual nested input/output arrays))',work,timing,metrics:{minMotor,maxMotor,minPairClearance,minObstacleClearance,maxInflow},memory:{sampledPeakRssBytes:peakRss,processMaxRssKiB:process.resourceUsage().maxRSS,scope:'RSS is cumulative process high-water; sampled RSS per run includes retained inputs and JS GC. Not attributable allocation or GPU memory.'},events,claim:'Conditional numerical model study; no physical, full-mission or safe-flight validation'};
 return {result,common,driver};
}
function persist({result,common,driver}){const id=result.runId,count=result.config.count;if(common.length)result.commonStates=writeSeries(`results/raw/${id}.states.f64.gz`,common,{count,stride:17,kind:'full17 common endpoints',dt:result.config.commonRecordTicks*Q,runId:id,fields});if(driver.length)result.denseStates=writeSeries(`results/raw/${id}.dense.f64.gz`,driver,{count,stride:17,kind:'full17 dense physics endpoints',dt:result.config.physicsDt,runId:id,fields});save(`results/runs/${id}.json`,result);return result;}
function compare(a,b){
 if(a.result.endTick!==b.result.endTick||!a.result.complete||!b.result.complete)throw Error('Cannot compare incomplete or mismatched work');
 if(a.common.length!==b.common.length)throw Error('Common record count mismatch');
 for(const data of [a,b])for(const row of data.common)if(row.length!==17*data.result.config.count||!row.every(Number.isFinite))throw Error('Invalid full17 common record');
 const maximum={positionM:0,velocityMps:0,attitudeRad:0,angularVelocityRadps:0,nominalMotorN:0},worst={};
 function set(key,value,n,i){if(value>maximum[key]){maximum[key]=value;worst[key]={record:n,tick:n*4,time:n*4*Q,drone:i};}}
 for(let n=0;n<a.common.length;n++)for(let i=0;i<a.result.config.count;i++){const x=a.common[n],y=b.common[n],o=17*i;for(const [key,k] of [['positionM',0],['velocityMps',3],['angularVelocityRadps',10]])set(key,Math.hypot(...[0,1,2].map(j=>x[o+k+j]-y[o+k+j])),n,i);let d=0,nx=0,ny=0;for(let k=6;k<10;k++){d+=x[o+k]*y[o+k];nx+=x[o+k]**2;ny+=y[o+k]**2;}set('attitudeRad',2*Math.acos(Math.min(1,Math.abs(d/Math.sqrt(nx*ny)))),n,i);for(let r=13;r<17;r++)set('nominalMotorN',Math.abs(x[o+r]-y[o+r]),n,i);}
 return {a:a.result.runId,b:b.result.runId,records:a.common.length,maximum,worst};
}
module.exports={Q,ticks,fields,run,persist,compare};
