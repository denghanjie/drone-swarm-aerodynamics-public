'use strict';
const fs=require('fs'),path=require('path'),crypto=require('crypto');
const {source}=require('./source.cjs'),M=require('./pruned-aero.cjs');
const B=source('outputs/milestone-31-source/sim.cjs'),{Grid}=source('outputs/milestone-31-source/grid.cjs'),G=source('outputs/milestone-31-source/geometry.cjs');
const config=require('../configs/campaign.json'),F=M.F;
function run({seed=3391,count=16,duration=1,dt=.0025,aeroDt=.01,epsilon=0,mode='coupled'}={}){
  if(count>16||duration>1)throw Error('Initial closed-loop diagnostic limited to 16 drones and 1 second');
  if(![.0025,.00125].includes(dt)||![.01,.005].includes(aeroDt)||Math.abs(aeroDt/dt-Math.round(aeroDt/dt))>1e-10)throw Error('Unsupported diagnostic cadence');
  const started=performance.now();let states=B.initial(seed,count),controls,winds=states.map(()=>[0,0,0,0]),omittedBounds=states.map(()=>0),frames=[],stop=null,end=0,heldTime=0,updates=0,omissions=0,maxInflow=0;
  const initial=states.map(s=>s.slice());
  const save=t=>{frames.push({t,states:states.map(s=>s.slice()),heldFieldTime:updates?heldTime:null,fieldStatus:updates?'successfully computed held field':'uninitialized; zero placeholder',winds:winds.map(x=>x.slice()),omittedBounds:omittedBounds.slice()});};
  for(let step=0;step<Math.round(duration/dt);step++){
    const t=step*dt;
    if(step%Math.round(aeroDt/dt)===0){
      try{const field=mode==='off'?{winds:states.map(()=>[0,0,0,0]),omittedBounds:states.map(()=>0),omittedPairs:0,maximumInflow:0}:M.fields(states,{epsilon});winds=field.winds;omittedBounds=field.omittedBounds;heldTime=t;updates++;omissions+=field.omittedPairs;maxInflow=Math.max(maxInflow,field.maximumInflow);}
      catch(e){stop={type:e.constructor.name,message:e.message,detail:e.detail,t};if(!frames.length||frames.at(-1).t!==t)save(t);break;}
    }
    if(step%Math.round(B.P.controlDt/dt)===0){
      const grid=new Grid(states,B.P.neighbor);
      controls=states.map((s,i)=>{const v=B.steer(i,states,grid.neighbors(i,B.P.neighbor),'boids','wall-priority');return F.control(s,{vx:v[0],vy:v[1],z:s[2]+(2.5*v[2]+1.5*s[5])/6,yaw:Math.atan2(v[1],v[0])},2.25);});
    }
    if(step%Math.round(.02/dt)===0)save(t);
    const previous=states;
    states=states.map((s,i)=>M.integrate(s,controls[i].u,dt,winds[i],mode==='off'?'off':'sum-rotor'));end=(step+1)*dt;
    for(let i=0;i<count;i++){
      if(!states[i].every(Number.isFinite)||states[i][2]<B.P.bodyRadius){stop={type:'vehicle model limit',drone:i,t:end};break;}
      const hits=B.obstacleContacts(previous[i],states[i]);if(hits.length){stop={type:'obstacle contact envelope',drone:i,hits,t:end};break;}
    }
    if(!stop)for(const [i,j] of B.contactCandidates(previous,states)){const d=G.segmentPair(previous[i],states[i],previous[j],states[j]);if(d<2*B.P.bodyRadius){stop={type:'drone contact envelope',pair:[i,j],distance:d,t:end};break;}}
    if(stop){save(end);break;}
    if(performance.now()-started>50000){stop={type:'wall-time cap',t:end};save(end);break;}
  }
  if(!frames.length||Math.abs(frames.at(-1).t-end)>1e-10)save(end);
  return {config:{seed,count,duration,dt,aeroDt,controlDt:B.P.controlDt,epsilon,mode,controller:'unchanged milestone31 local 3D Boids + wall-priority; shared broad route, no individual scripted trajectories'},sourceHash:crypto.createHash('sha256').update(fs.readFileSync(path.join(__dirname,'pruned-aero.cjs'))).digest('hex'),initial,frames,final:states,metrics:{end,stop,updates,omissions,maxInflow,...B.measure(states)},wallSeconds:(performance.now()-started)/1000,claim:'Short closed-loop numerical diagnostic only; no physical validation or safe-flight/trajectory-convergence claim'};
}
function compare(a,b){const amap=new Map(a.frames.map(f=>[f.t.toFixed(6),f]));let maxPosition=0,maxQuaternionDistance=0,common=0;for(const f of b.frames){const g=amap.get(f.t.toFixed(6));if(!g)continue;common++;for(let i=0;i<f.states.length;i++){maxPosition=Math.max(maxPosition,Math.hypot(...[0,1,2].map(k=>f.states[i][k]-g.states[i][k])));maxQuaternionDistance=Math.max(maxQuaternionDistance,Math.hypot(...[6,7,8,9].map(k=>f.states[i][k]-g.states[i][k])));}}const bothComplete=!a.metrics.stop&&!b.metrics.stop&&Math.abs(a.metrics.end-a.config.duration)<1e-10&&Math.abs(b.metrics.end-b.config.duration)<1e-10;return {commonFrames:common,maxPositionM:maxPosition,maxQuaternionDistance,bothComplete,statusAgrees:a.metrics.stop?.type===b.metrics.stop?.type,positionScreenPassed:common>0&&bothComplete&&maxPosition<=.01,scope:'Common saved timestamps only; local 1-second window; censored members cannot pass'};}
if(require.main===module){
  const out=path.join(__dirname,'../results/boids');fs.mkdirSync(out,{recursive:true});const records=[];
  const jobs=config.closedLoop.seeds.flatMap(seed=>[{seed,epsilon:0,label:'exact'},{seed,epsilon:.04,label:'pruned'},{seed,epsilon:0,mode:'off',label:'off'}]);
  jobs.push({seed:3391,epsilon:0,dt:.00125,label:'physics-refined'},{seed:3391,epsilon:0,aeroDt:.005,label:'refresh-refined'});
  for(const job of jobs){const {label,...cfg}=job,record=run(cfg),id=`${job.seed}-${label}`;fs.writeFileSync(path.join(out,id+'.json'),JSON.stringify(record));records.push({id,...record});console.log(JSON.stringify({id,end:record.metrics.end,stop:record.metrics.stop,omissions:record.metrics.omissions,wallSeconds:record.wallSeconds}));}
  const comparisons=[];for(const seed of config.closedLoop.seeds){const exact=records.find(r=>r.id===`${seed}-exact`);for(const r of records.filter(r=>r.id.startsWith(`${seed}-`)&&r!==exact))comparisons.push({a:exact.id,b:r.id,...compare(exact,r)});}
  fs.writeFileSync(path.join(out,'index.json'),JSON.stringify({records:records.map(({id,config,metrics,wallSeconds})=>({id,file:id+'.json',config,metrics,wallSeconds})),comparisons},null,2));
}
module.exports={run,compare};
