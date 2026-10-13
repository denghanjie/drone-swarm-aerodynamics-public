'use strict';
const fs=require('fs'),crypto=require('crypto');
const {M,config,evaluator,sourceHash,save,median,bootstrap}=require('./common.cjs');
const {source}=require('./source.cjs');
const B=source('outputs/milestone-31-source/sim.cjs'),{Grid}=source('outputs/milestone-31-source/grid.cjs'),G=source('outputs/milestone-31-source/geometry.cjs');
function run({seed=4391,count=16,duration=1,dt=.0025,aeroDt=.01,variant='lean',record=true}={}){
 if(![16,50].includes(count)||!Number.isFinite(duration)||duration>3||duration<=0)throw Error('Bounded run only N16/50, <=3s');
 if(![.0025,.00125].includes(dt)||![.01,.005].includes(aeroDt)||[aeroDt,B.P.controlDt,config.closedLoop.frameDt,duration].some(t=>Math.abs(t/dt-Math.round(t/dt))>1e-9))throw Error('Unsupported cadence or non-integral schedule');
 const started=performance.now(),evaluate=evaluator(variant),timing={field:0,controller:0,physics:0,safety:0,recording:0};
 let states=B.initial(seed,count),controls,winds=states.map(()=>[0,0,0,0]),frames=[],stop=null,end=0,heldTime=null,updates=0,maxInflow=0;
 const initial=states.map(s=>s.slice()),hash=crypto.createHash('sha256');
 const saveFrame=t=>{const at=performance.now();if(record)frames.push({t,pose:states.map(s=>[...s.slice(0,3),...s.slice(6,10)]),winds:winds.map(w=>w.slice()),heldFieldTime:heldTime});timing.recording+=performance.now()-at;};
 for(let step=0;step<Math.round(duration/dt);step++){
  const t=step*dt;
  if(step%Math.round(aeroDt/dt)===0){const at=performance.now();try{const f=evaluate(states);winds=f.winds;heldTime=t;updates++;maxInflow=Math.max(maxInflow,f.maximumInflow);}catch(e){stop={type:e.constructor.name,message:e.message,detail:e.detail,t};timing.field+=performance.now()-at;saveFrame(t);break;}timing.field+=performance.now()-at;}
  if(step%Math.round(B.P.controlDt/dt)===0){const at=performance.now(),grid=new Grid(states,B.P.neighbor);controls=states.map((s,i)=>{const v=B.steer(i,states,grid.neighbors(i,B.P.neighbor),'boids','wall-priority');return M.F.control(s,{vx:v[0],vy:v[1],z:s[2]+(2.5*v[2]+1.5*s[5])/6,yaw:Math.atan2(v[1],v[0])},2.25);});timing.controller+=performance.now()-at;}
  if(record){const at=performance.now();hash.update(JSON.stringify([t,states,winds]));timing.recording+=performance.now()-at;}
  if(step%Math.round(config.closedLoop.frameDt/dt)===0)saveFrame(t);
  const previous=states,at=performance.now();states=states.map((s,i)=>M.integrate(s,controls[i].u,dt,winds[i],'sum-rotor'));end=(step+1)*dt;timing.physics+=performance.now()-at;
  const check=performance.now();for(let i=0;i<count;i++){
   if(!states[i].every(Number.isFinite)||states[i][2]<B.P.bodyRadius){stop={type:'vehicle model limit',drone:i,t:end};break;}
   const hits=B.obstacleContacts(previous[i],states[i]);if(hits.length){stop={type:'obstacle contact envelope',drone:i,hits,t:end};break;}
  }
  if(!stop)for(const [i,j] of B.contactCandidates(previous,states)){const d=G.segmentPair(previous[i],states[i],previous[j],states[j]);if(d<2*B.P.bodyRadius){stop={type:'drone contact envelope',pair:[i,j],distance:d,t:end};break;}}
  timing.safety+=performance.now()-check;
  if(stop){saveFrame(end);break;}
  if(performance.now()-started>50000){stop={type:'wall-time cap',t:end};saveFrame(end);break;}
 }
 if(!frames.length||Math.abs(frames.at(-1).t-end)>1e-10)saveFrame(end);
 if(record)hash.update(JSON.stringify([end,states,winds]));
 timing.total=performance.now()-started;
 const complete=!stop&&Math.abs(end-duration)<1e-12;
 return {config:{seed,count,duration,dt,aeroDt,controlDt:B.P.controlDt,frameDt:config.closedLoop.frameDt,variant,record,controller:'unchanged milestone31 local 3D Boids and wall-priority, shared broad route'},sourceHash:sourceHash(),initial,final:states,frames,stateStreamHash:record?hash.digest('hex'):null,metrics:{end,stop,complete,updates,maxInflow,...(record?B.measure(states):{})},timing,claim:'Short genuine Boids numerical replay; no physical validation, full-mission, convergence, GPU or safe-flight claim'};
}
function compare(a,b){let maxPositionM=0,maxPose=0,common=0;const map=new Map(a.frames.map(f=>[f.t.toFixed(6),f]));for(const f of b.frames){const g=map.get(f.t.toFixed(6));if(!g)continue;common++;for(let i=0;i<f.pose.length;i++){maxPositionM=Math.max(maxPositionM,Math.hypot(...[0,1,2].map(k=>f.pose[i][k]-g.pose[i][k])));maxPose=Math.max(maxPose,...f.pose[i].map((x,k)=>Math.abs(x-g.pose[i][k])));}}const complete=a.metrics.complete&&b.metrics.complete;return {common,maxPositionM,maxPose,complete,stateStreamIdentical:a.stateStreamHash===b.stateStreamHash,passed:complete&&common>0&&maxPositionM<=config.closedLoop.equivalencePositionTolerance};}
function pipeline({selected='lean'}={}){
 const variants=['legacy','previous-zero',selected],rows=[];
 for(const v of variants){const r=run({seed:4301,variant:v,record:false});if(!r.metrics.complete)throw Error('Warmup incomplete; cannot compare wall time');}
 for(let rep=0;rep<7;rep++){
  let order=variants.map((_,i)=>variants[(i+rep)%variants.length]);if(rep%2)order.reverse();const results={};
  for(const v of order){const r=run({seed:4301,variant:v,record:false});results[v]={metrics:r.metrics,timing:r.timing};save('results/pipeline-partial.json',{selected,rows,current:{rep,order,results}});if(!r.metrics.complete)throw Error('Fixed-work member incomplete; no speed comparison');}
  rows.push({rep,order,results});
 }
 const summaries=['legacy','previous-zero'].map(reference=>{const ratios=rows.map(r=>r.results[selected].timing.total/r.results[reference].timing.total);return {reference,selected,medianRatio:median(ratios),bootstrap95:bootstrap(ratios),scope:'Total fixed-work 400-step N16 Boids CPU time, recording disabled, all members complete'};});
 const result={selected,sourceHash:sourceHash(),seed:4301,count:16,duration:1,warmupsPerVariant:1,repetitions:7,rows,summaries};save('results/pipeline.json',result);return result;
}
if(require.main===module){if(process.argv[2]==='pipeline'){const r=pipeline(JSON.parse(process.argv[3]||'{}'));console.log(JSON.stringify(r.summaries));}else{const cfg=JSON.parse(process.argv[2]||'{}'),r=run(cfg),id=`${r.config.seed}-${r.config.count}-${r.config.variant}-${r.config.dt}-${r.config.aeroDt}`;save(`results/boids/${id}.json`,r);console.log(JSON.stringify({id,metrics:r.metrics,timing:r.timing}));}}
module.exports={run,compare,pipeline};
