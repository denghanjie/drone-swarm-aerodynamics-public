'use strict';
const fs=require('fs'),path=require('path'),os=require('os'),assert=require('assert/strict');
const root=path.resolve(__dirname,'../../..');
process.env.FLOCK_FACTORY_VARIANT='narrow';
const S=require(path.join(root,'outputs/milestone-31-source/sim.cjs')),F=require(path.join(root,'outputs/step02c-source/physics.cjs')),{Grid}=require(path.join(root,'outputs/milestone-31-source/grid.cjs')),G=require(path.join(root,'outputs/milestone-31-source/geometry.cjs')),{steer}=require('./controller.cjs');
assert.equal(os.endianness(),'LE','Binary writers require a little-endian runtime');
const TICKS_PER_SECOND=1600,CONTROL_TICKS=16;
const clone=x=>JSON.parse(JSON.stringify(x));
function writeJSON(p,x){fs.writeFileSync(p+'.tmp',JSON.stringify(x)+'\n');fs.renameSync(p+'.tmp',p);}
class Stream{
 constructor(file,width){this.file=file;this.width=width;this.frames=0;this.fd=fs.openSync(file,'wx');}
 add(values){assert.equal(values.length,this.width);const a=Float64Array.from(values),b=Buffer.from(a.buffer);let offset=0;while(offset<b.length)offset+=fs.writeSync(this.fd,b,offset,b.length-offset);this.frames++;}
 close(){fs.closeSync(this.fd);}
 meta(){return {file:path.basename(this.file),valuesPerFrame:this.width,frames:this.frames,bytes:this.frames*this.width*8,type:'Float64LE'};}
}
function loadStart(evidence,name){
 const id=name==='A'?'heldout-2002-1000-narrow-wall-priority-0.0025':'refinement-2002-1000-narrow-wall-priority-0.00125';
 const dir=path.join(evidence,'outputs/milestone-31-source'),cp=JSON.parse(fs.readFileSync(path.join(dir,'checkpoint-'+id+'-20.json'))),mission=JSON.parse(fs.readFileSync(path.join(dir,id+'.json')));
 assert.equal(cp.t,20);assert.equal(cp.states.length,1000);assert(cp.states.every(s=>s.length===17&&s.every(Number.isFinite)));
 const crossings=mission.crossings.map(t=>t!==null&&t<=cp.t?t:null);assert.equal(crossings.filter(t=>t!==null).length,cp.passed);
 return {states:cp.states,timeTick:32000,controls:null,lastControl:null,crossings,stop:null,saturationSeconds:0};
}
function fnv(ids){let h=2166136261;for(const id of ids){h=Math.imul(h^id,16777619)>>>0;}return h;}
const diagnosticFields=['preferredX','preferredY','preferredZ','beforeWallX','beforeWallY','beforeWallZ','requestedX','requestedY','requestedZ','actualX','actualY','actualZ','beforeWallResidual','wallResidual','pairResidual','repairIterations','repairConverged','socialCount','pairCount','wallCount','socialHash32','pairHash32','saturated','trackingErrorNorm'];
function segment({context,dt,duration,instrument=true,replay=null,intervention=null,onControl=null,onSample=null}){
 const c=clone(context),n=c.states.length,units=Math.round(dt*TICKS_PER_SECOND),steps=Math.round(duration/dt),startTick=c.timeTick;
 assert.equal(units/TICKS_PER_SECOND,dt);assert.equal(CONTROL_TICKS%units,0);assert.equal(steps*units/TICKS_PER_SECOND,duration);assert(!c.stop);
 const phase={control:0,physics:0,safety:0,io:0,measurement:0},commands=[],samples=[];
 function sampled(){const at=performance.now();const science=S.measure(c.states);phase.measurement+=performance.now()-at;const t=c.timeTick/TICKS_PER_SECOND;const rec={t,passed:c.crossings.filter(x=>x!==null).length,...science};samples.push(rec);const io=performance.now();onSample?.(c,rec);phase.io+=performance.now()-io;}
 sampled();
 for(let step=0;step<steps;step++){
  const tick=c.timeTick;
  if(tick%CONTROL_TICKS===0){
   const at=performance.now(),grid=replay?null:new Grid(c.states,S.P.neighbor),rows=[],details=[];
   if(replay){const k=(tick-32000)/CONTROL_TICKS;assert(Number.isInteger(k)&&k>=0&&k<replay.frames);c.controls=c.states.map((s,i)=>({u:Array.from(replay.values.subarray((k*n+i)*4,(k*n+i+1)*4)),saturated:null,qd:null}));}
   else c.controls=c.states.map((s,i)=>{
    const ids=grid.neighbors(i,S.P.neighbor);let d;
    const options=step===0&&intervention?{pairOverride:intervention}:{};
    const v=instrument?steer(i,c.states,ids,'boids','wall-priority',x=>d=x,options):S.steer(i,c.states,ids,'boids','wall-priority',x=>d=x);
    const control=F.control(s,{vx:v[0],vy:v[1],z:s[2]+(2.5*v[2]+1.5*s[5])/6,yaw:Math.atan2(v[1],v[0])},2.25);
    details.push({drone:i,state:s,velocity:v,...d,actuator:control});
    if(instrument)rows.push(...d.preferred,...d.beforeWall,...d.velocity,...d.actual,d.beforeWallResidual,d.wallResidual,d.pairResidual,d.iterations,d.converged?1:0,ids.length,d.pairs.length,d.walls.length,fnv(ids),fnv(d.pairs.map(x=>x.neighbor)),control.saturated?1:0,Math.hypot(...v.map((x,k)=>x-s[k+3])));
    return control;
   });
   c.lastControl={timeTick:tick,states:c.states,details};phase.control+=performance.now()-at;
   const u=c.controls.flatMap(x=>x.u);commands.push({timeTick:tick,u});
   const io=performance.now();onControl?.(c,rows,u);phase.io+=performance.now()-io;
  }
  assert(c.controls&&c.controls.length===n);
  const old=c.states,at=performance.now();c.states=c.states.map((s,i)=>{if(c.controls[i].saturated)c.saturationSeconds+=dt;return F.integrate(s,c.controls[i].u,dt);});phase.physics+=performance.now()-at;
  c.timeTick+=units;const st=performance.now();
  // Preserve frozen per-drone traversal and event-detection order; no interpolated event time.
  for(let i=0;i<n;i++){
   const s=c.states[i];if(!s.every(Number.isFinite)||s[2]<S.P.bodyRadius){c.stop={reason:'vehicle model limit',drone:i};break;}
   const hits=S.obstacleContacts(old[i],s);if(hits.length){c.stop={reason:'obstacle contact envelope',drone:i,hits};break;}
   if(c.crossings[i]===null&&old[i][0]<S.course.finish&&s[0]>=S.course.finish)c.crossings[i]=c.timeTick/TICKS_PER_SECOND;
  }
  if(!c.stop)for(const [i,j] of S.contactCandidates(old,c.states)){const distance=G.segmentPair(old[i],c.states[i],old[j],c.states[j]);if(distance<2*S.P.bodyRadius){c.stop={reason:'drone contact envelope',pair:[i,j],distance};break;}}
  if(c.stop){const ids=c.stop.pair||[c.stop.drone];c.stop={...c.stop,lastSafeTick:c.timeTick-units,detectedTick:c.timeTick,lastControlTick:c.lastControl.timeTick,affected:ids.map(i=>({i,precedingState:old[i],detectedState:c.states[i],lastControlState:c.lastControl.states[i],heldActuator:c.controls[i],diagnostic:c.lastControl.details.find(x=>x.drone===i)||null}))};}
  phase.safety+=performance.now()-st;
  if((c.timeTick-startTick)%160===0||c.stop||step===steps-1)sampled();
  if(c.stop)break;
 }
 return {context:c,commands,samples,phase};
}
function runJob(job,evidence,out){
 fs.mkdirSync(out,{recursive:true});const started=performance.now(),context=job.context||loadStart(evidence,job.start),n=context.states.length;
 const streams={states:new Stream(path.join(out,job.id+'-states.f64'),1+17*n),commands:new Stream(path.join(out,job.id+'-commands.f64'),1+4*n)};
 if(job.precontrol)streams.precontrol=new Stream(path.join(out,job.id+'-precontrol.f64'),1+17*n);
 if(job.instrument!==false&&!job.replay)streams.diagnostics=new Stream(path.join(out,job.id+'-diagnostics.f64'),1+diagnosticFields.length*n);
 let replay=null;
 if(job.replay){const b=fs.readFileSync(path.join(out,job.replay+'-commands.f64')),x=new Float64Array(b.buffer,b.byteOffset,b.length/8),stride=1+4*n,frames=x.length/stride;assert(Number.isInteger(frames));const values=new Float64Array(frames*4*n);for(let k=0;k<frames;k++){assert.equal(x[k*stride],32000+k*16);values.set(x.subarray(k*stride+1,(k+1)*stride),k*4*n);}replay={values,frames};}
 const index=()=>writeJSON(path.join(out,job.id+'-index.json'),{id:job.id,complete:false,streams:Object.fromEntries(Object.entries(streams).map(([k,v])=>[k,v.meta()])),diagnosticFields,timestamp:'integer ticks, 1600 ticks per second'});
 let result;
 try{result=segment({context,dt:job.dt,duration:job.duration,instrument:job.instrument!==false,replay,intervention:job.intervention,onSample:c=>{streams.states.add([c.timeTick,...c.states.flat()]);index();},onControl:(c,rows,u)=>{streams.precontrol?.add([c.timeTick,...c.states.flat()]);streams.commands.add([c.timeTick,...u]);streams.diagnostics?.add([c.timeTick,...rows]);index();}});}
 finally{for(const s of Object.values(streams))s.close();}
 const meta={id:job.id,dt:job.dt,duration:job.duration,start:job.start||'local pre-control state',startTick:context.timeTick,endTick:result.context.timeTick,complete:result.context.timeTick===context.timeTick+Math.round(job.duration*1600)&&!result.context.stop,stop:result.context.stop,samples:result.samples,phaseMilliseconds:result.phase,elapsedWallSeconds:(performance.now()-started)/1000,streams:Object.fromEntries(Object.entries(streams).map(([k,v])=>[k,v.meta()])),diagnosticFields,timestamp:'integer ticks, 1600 ticks per second',externalAerodynamicForce:[0,0,0],saturationSeconds:job.replay?null:result.context.saturationSeconds,crossings:result.context.crossings};
 writeJSON(path.join(out,job.id+'-final-context.json'),result.context);writeJSON(path.join(out,job.id+'-index.json'),meta);return meta;
}
module.exports={S,F,Grid,steer,loadStart,segment,runJob,clone,diagnosticFields};
