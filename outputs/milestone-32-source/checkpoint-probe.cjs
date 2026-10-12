'use strict';
// Post-hoc numerical diagnosis, NOT a fresh mission evaluation.
const fs=require('fs'),path=require('path');
process.env.FLOCK_FACTORY_VARIANT='narrow';
const S=require('../milestone-31-source/sim.cjs'),F=require('../step02c-source/physics.cjs'),{Grid}=require('../milestone-31-source/grid.cjs'),G=require('../milestone-31-source/geometry.cjs');
const dir=__dirname,checkpoint=JSON.parse(fs.readFileSync(path.join(dir,'../milestone-31-source/checkpoint-refinement-2002-1000-narrow-wall-priority-0.00125-20.json')));
const protocol=JSON.parse(fs.readFileSync(path.join(dir,'../milestone-32-checkpoint-protocol.json'))),N=checkpoint.states.length;
const save=(n,x)=>fs.writeFileSync(path.join(dir,n),JSON.stringify(x));
function binary(n,values){const b=Buffer.allocUnsafe(values.length*8);values.forEach((x,i)=>b.writeDoubleLE(x,i*8));fs.writeFileSync(path.join(dir,n),b);}
function readBinary(n){const b=fs.readFileSync(path.join(dir,n));return Float64Array.from({length:b.length/8},(_,i)=>b.readDoubleLE(i*8));}
function run(job){
 let states=checkpoint.states.map(s=>s.slice()),controls=null,commands=[],poses=[],trace=[],stop=null;
 const held=job.feedback==='replayed'?readBinary('closed-0.0025-commands.f64'):null,dt=job.dt,steps=Math.round(10/dt),stride=Math.round(.01/dt),sampleStride=Math.round(.1/dt),started=performance.now();
 function sample(step){poses.push(20+step*dt,...states.flatMap(s=>s.slice(0,3)));}
 sample(0);
 for(let step=0;step<steps;step++){
  if(step%stride===0){const tick=step/stride;
   if(held){controls=states.map((s,i)=>Array.from(held.subarray((tick*N+i)*4,(tick*N+i+1)*4)));}
   else{const grid=new Grid(states,S.P.neighbor);let pairCount=0,wallCount=0,maxPair=0,maxWall=0,caps=0;
    controls=states.map((s,i)=>{const v=S.steer(i,states,grid.neighbors(i,S.P.neighbor),'boids','wall-priority',d=>{pairCount+=d.pairs.length;wallCount+=d.walls.length;maxPair=Math.max(maxPair,d.pairResidual);maxWall=Math.max(maxWall,d.wallResidual);caps+=d.converged===false;});return F.control(s,{vx:v[0],vy:v[1],z:s[2]+(2.5*v[2]+1.5*s[5])/6,yaw:Math.atan2(v[1],v[0])},2.25).u;});
    trace.push({t:20+tick*.01,pairCount,wallCount,maxPair,maxWall,caps});
   }
   if(job.feedback==='closed')commands.push(...controls.flat());
  }
  const old=states;states=states.map((s,i)=>F.integrate(s,controls[i],dt));
  for(let i=0;i<N;i++){if(!states[i].every(Number.isFinite)||states[i][2]<S.P.bodyRadius){stop={reason:'vehicle model limit',drone:i};break;}const hits=S.obstacleContacts(old[i],states[i]);if(hits.length){stop={reason:'obstacle contact envelope',drone:i,hits};break;}}
  if(!stop)for(const [i,j] of S.contactCandidates(old,states)){const d=G.segmentPair(old[i],states[i],old[j],states[j]);if(d<2*S.P.bodyRadius){stop={reason:'drone contact envelope',pair:[i,j],distance:d};break;}}
  if((step+1)%sampleStride===0||stop)sample(step+1);
  if((step+1)%Math.round(1/dt)===0){save('progress.json',{job,t:20+(step+1)*dt,wallSeconds:(performance.now()-started)/1000});console.log(job.id,20+(step+1)*dt);}
  if(stop){stop.t=20+(step+1)*dt;break;}
 }
 binary(job.id+'-positions.f64',poses);if(job.feedback==='closed')binary(job.id+'-commands.f64',commands);
 const record={job,checkpointTime:20,checkpointIdentical:true,controlDt:.01,sampleDt:.1,frames:poses.length/(1+3*N),count:N,stop,final:states,trace,wallSeconds:(performance.now()-started)/1000,finalMeasures:S.measure(states)};save(job.id+'.json',record);console.log('DONE',job.id,record.wallSeconds);
}
function compare(a,b){const x=readBinary(a+'-positions.f64'),y=readBinary(b+'-positions.f64'),stride=1+N*3,frames=Math.min(x.length,y.length)/stride,profile=[];let maximum=0,firstExceedance=null;
 for(let f=0;f<frames;f++){const errors=[];for(let i=0;i<N;i++){const k=f*stride+1+i*3;errors.push(Math.hypot(x[k]-y[k],x[k+1]-y[k+1],x[k+2]-y[k+2]));}errors.sort((a,b)=>a-b);const max=errors.at(-1);maximum=Math.max(maximum,max);if(firstExceedance===null&&max>.01)firstExceedance=x[f*stride];profile.push({t:x[f*stride],max,median:errors[Math.floor(N/2)],p95:errors[Math.floor(.95*N)]});}
 return {a,b,maximum,firstExceedance,profile};
}
for(const job of protocol.diagnostic.jobs)run(job);
