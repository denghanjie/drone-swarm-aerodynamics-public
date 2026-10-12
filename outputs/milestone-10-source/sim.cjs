'use strict';
const F=require('../step02c-source/physics.cjs');
const {Scheduler}=require('../milestone-07-source/scheduler.cjs');
const {Scheduler:CautiousScheduler}=require('../milestone-04-source/scheduler.cjs');
const {steer,PARAMETERS}=require('./boids.cjs');
const R=.075, SAFE=.20, HORIZON=60, CONTROL=.01;
const clamp=(x,a,b)=>Math.max(a,Math.min(b,x));
function rng(seed){let x=seed>>>0;return()=>{x=(1664525*x+1013904223)>>>0;return x/4294967296;};}
function swept(a,b,c,d){const r=a.map((v,k)=>v-c[k]),v=b.map((x,k)=>x-a[k]-d[k]+c[k]),vv=v.reduce((s,x)=>s+x*x,0),t=vv?clamp(-r.reduce((s,x,k)=>s+x*v[k],0)/vv,0,1):0;return Math.hypot(...r.map((x,k)=>x+t*v[k]));}
function run({width=1.2,spacing=.6,speed=.5,seed=1,dt=.01,duration=HORIZON,record=false,count=50,controller='flow',profile='ideal'}={}){
 if(!['flow','scheduled','reactive','boids','goal-only'].includes(controller))throw Error('Unsupported controller');
 if(![.6,1.2,2.4].includes(width)||![.3,.6].includes(spacing)||![.25,.5].includes(speed)||![.01,.005,.0025].includes(dt))throw Error('Unsupported configuration');
 const observer=new Observer(profile,seed,count);
 const random=rng(seed),states=Array.from({length:count},(_,i)=>[-1.2-Math.floor(i/5)*spacing,(i%5-2)*spacing+(random()-.5)*.01,1.2+(random()-.5)*.01,0,0,0,0,0,0,1,0,0,0,...Array(4).fill(F.P.m*F.P.g/4)]),initial=states.map(s=>s.slice(0,3));
 // Five ordered approach lanes contract to the gate. This is a deliberately simple local-steering baseline.
 const scheduler=controller==='flow'?new Scheduler({width,spacing,speed,initial}):controller==='scheduled'?new CautiousScheduler({width,spacing,speed,initial}):null;
 const ys=states.map((_,i)=>(i%5-2)*Math.min(spacing,(width-2*R-.08)/4));
 let controls=states.map(s=>F.control(s,{vx:0,vy:0,z:1.2,yaw:0},2.25)),frames=[],diagnostics=[],crossings=Array(count).fill(null),invalid=new Set(),near=new Set(),contact=new Set(),minSep=Infinity,sat=0,err2=0,errN=0,stopped=null,stopTime=null,maxTilt=0;
 const sample=t=>{frames.push([+t.toFixed(6),...states.flatMap(s=>[...s.slice(0,3),...s.slice(6,10)].map(x=>+x.toFixed(6)))]);if(controller==='boids'||controller==='goal-only'){const i=Math.min(12,count-1),cmd=steer(i,states,{width,speed,mode:controller});diagnostics.push({t:+t.toFixed(6),selected:i,...cmd});}};
 if(record)sample(0);
 const steps=Math.round(duration/dt),interval=Math.round(CONTROL/dt),save=Math.round(.1/dt);
 for(let n=0;n<steps;n++){
  const t=n*dt;
  if(n%interval===0){
   const observed=observer.sample(states);
   if(scheduler)scheduler.update(observed,t);
   controls=states.map((s,i)=>{
    let vx,vy,refY=ys[i];
    if(controller==='boids'||controller==='goal-only'){const cmd=steer(i,observed,{width,speed,mode:controller});vx=cmd.vx;vy=cmd.vy;refY=cmd.refY;}else if(scheduler){const cmd=scheduler.command(i,observed[i]);vx=cmd.vx;vy=cmd.vy;refY=cmd.refY;}else{
    vx=speed;vy=clamp(1.2*(ys[i]-s[1]),-speed,speed);
    // Complete lateral alignment before entering the opening; no invisible wall force.
    if(s[0]>-.65&&s[0]<0&&Math.abs(s[1]-ys[i])>.035)vx=0;
    for(let j=0;j<count;j++){if(i===j)continue;const q=states[j],dx=s[0]-q[0],dy=s[1]-q[1],dz=s[2]-q[2],d=Math.hypot(dx,dy,dz);if(d<.48){const force=1.8*Math.max(0,(.30-d)/.30);vx+=force*dx/Math.max(d,.001);vy+=force*dy/Math.max(d,.001);if(q[0]>s[0]&&Math.abs(dy)<SAFE&&q[0]-s[0]<.45)vx=Math.min(vx,speed*clamp((q[0]-s[0]-SAFE)/.25,0,1));}}
    }
    const norm=Math.hypot(vx,vy);if(norm>speed){vx*=speed/norm;vy*=speed/norm;}
    err2+=(s[1]-refY)**2+(s[2]-1.2)**2;errN++;
    return F.control(s,{vx,vy,z:1.2,yaw:0},2.25);
   });
  }
  const old=states.map(s=>s.slice(0,3));
  for(let i=0;i<count;i++){states[i]=F.integrate(states[i],controls[i].u,dt);if(controls[i].saturated)sat+=dt;const s=states[i];maxTilt=Math.max(maxTilt,...F.euler(s.slice(6,10)).slice(0,2).map(Math.abs));if(!s.every(Number.isFinite)||s[2]<R||s[2]>3||Math.hypot(...s.slice(10,13))>30){stopped='vehicle model limit';}
   if(old[i][0]<0&&s[0]>=0){const f=-old[i][0]/(s[0]-old[i][0]),y=old[i][1]+f*(s[1]-old[i][1]),z=old[i][2]+f*(s[2]-old[i][2]);if(Math.abs(y)<=width/2-R&&z>=.6+R&&z<=1.8-R){if(crossings[i]===null)crossings[i]=t+f*dt;}else invalid.add(i);}
  }
  for(let i=0;i<count;i++)for(let j=i+1;j<count;j++){const d=swept(old[i],states[i].slice(0,3),old[j],states[j].slice(0,3));minSep=Math.min(minSep,d);if(d<SAFE)near.add(i+','+j);if(d<2*R){contact.add(i+','+j);stopped='contact envelope reached';}}
  if(stopped){stopTime=(n+1)*dt;if(record)sample(stopTime);break;}
  if(record&&(n+1)%save===0)sample((n+1)*dt);
 }
 const end=stopTime??duration,valid=crossings.filter(x=>x!==null).length;
 return {config:{width,spacing,speed,seed,dt,count,duration,controller,profile},observation:observer.description(),metrics:{validCrossings:valid,completionFraction:valid/count,fullHorizonThroughput:valid/duration,minSeparation:minSep,closePairs:near.size,contactPairs:contact.size,invalidCrossingDrones:invalid.size,motorSaturationFraction:sat/(count*end),lateralAltitudeTrackingRMS:Math.sqrt(err2/errN),maxTiltDeg:maxTilt*180/Math.PI,stopReason:stopped,simulatedSeconds:end,fullHorizonCompleted:!stopped},crossings,initial,...(scheduler?{schedule:scheduler.events,capacity:scheduler.capacity}:{}),final:states.map(s=>s.slice(0,3)),...(record?{frames,diagnostics}:{} )};
}
const PROFILES={ideal:{bias:0,delay:0},bias:{bias:.02,delay:0},delay:{bias:0,delay:.10},combined:{bias:.02,delay:.10},stress:{bias:.05,delay:.25}};
class Observer {
 constructor(profile,seed,count){if(!PROFILES[profile])throw Error('Unknown observation profile');this.p=PROFILES[profile];this.ticks=Math.round(this.p.delay/CONTROL);this.history=[];const random=rng((seed^0x9e3779b9)>>>0);this.offsets=Array.from({length:count},()=>[(2*random()-1)*this.p.bias,(2*random()-1)*this.p.bias]);}
 sample(states){this.history.push(states.map(s=>s.slice()));if(this.history.length>this.ticks+1)this.history.shift();return this.history[0].map((s,i)=>{const o=s.slice();o[0]+=this.offsets[i][0];o[1]+=this.offsets[i][1];return o;});}
 description(){return {biasBoundPerAxis:this.p.bias,navigationDelaySeconds:this.p.delay,offsets:this.offsets,scope:'Delayed navigation state; fixed x/y bias. Low-level control and safety measurements use current true state. Initial scheduler map is exact.'};}
}
module.exports={run,swept,R,SAFE,Observer,PROFILES};
if(require.main===module){const out=run(JSON.parse(process.argv[2]||'{}'));console.log(JSON.stringify(out));}
