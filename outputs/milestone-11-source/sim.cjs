'use strict';
const F=require('../step02c-source/physics.cjs'),{swept}=require('../milestone-10-source/sim.cjs');
const PARAM=Object.freeze({radius:1.8,separationRadius:.85,separation:1.5,alignment:2,cohesion:.22,cruise:.65,maxSpeed:.9,steeringHorizon:.4});
const norm=a=>Math.hypot(...a),cap=(x,l,h)=>Math.max(l,Math.min(h,x));
function rng(seed){let x=seed>>>0;return()=>((x=(1664525*x+1013904223)>>>0)/4294967296);}
function initial(seed,count){const r=rng(seed),states=[];while(states.length<count){const p=[(r()-.5)*4.6,(r()-.5)*4.6,4+(r()-.5)*4.6];if(norm([p[0],p[1],p[2]-4])>2.3||states.some(s=>norm(p.map((x,k)=>x-s[k]))<.55))continue;let v=[r()-.5,r()-.5,r()-.5],n=norm(v);v=v.map(x=>x/n*.35);const yaw=Math.atan2(v[1],v[0]);states.push([...p,...v,0,0,Math.sin(yaw/2),Math.cos(yaw/2),0,0,0,...Array(4).fill(F.P.m*F.P.g/4)]);}return states;}
function steer(i,states,t,mode='boids'){
 const s=states[i],v=s.slice(3,6),n=norm(v),a=v.map(x=>1.2*(PARAM.cruise-n)*x/Math.max(n,.01)),sep=[0,0,0],align=[0,0,0],coh=[0,0,0];let neighbors=0;
 for(let j=0;j<states.length;j++){if(i===j)continue;const q=states[j],delta=q.slice(0,3).map((x,k)=>x-s[k]),d=norm(delta);if(d>=PARAM.radius)continue;neighbors++;for(let k=0;k<3;k++){align[k]+=q[3+k];coh[k]+=delta[k];if(d<PARAM.separationRadius&&d>1e-9)sep[k]-=PARAM.separation*(1/d-1/PARAM.separationRadius)*delta[k]/d;}}
 if(mode==='separation-only')for(let k=0;k<3;k++)a[k]+=sep[k];
 if(mode==='boids')for(let k=0;k<3;k++)a[k]+=sep[k]+(neighbors?PARAM.alignment*(align[k]/neighbors-v[k])+PARAM.cohesion*coh[k]/neighbors:0);
 // Soft environmental limits are shared by both modes, never reposition states.
 for(let k=0;k<3;k++){const lo=k===2?2:-8,hi=k===2?7:8;if(s[k]<lo)a[k]+=2*(lo-s[k])+1.5*Math.max(0,-v[k]);if(s[k]>hi)a[k]-=2*(s[k]-hi)+1.5*Math.max(0,v[k]);}
 // A local steering cue reaches only a fixed spatial region, not all drones or an assigned leader.
 if(t>=15&&t<18&&s[0]>0){a[1]+=.3;a[2]+=.2;}
 const cmd=v.map((x,k)=>x+PARAM.steeringHorizon*a[k]),speed=norm(cmd);return {velocity:cmd.map(x=>x*Math.min(1,PARAM.maxSpeed/Math.max(speed,1e-9))),neighbors};
}
function measures(states){const count=states.length,center=[0,1,2].map(k=>states.reduce((a,s)=>a+s[k],0)/count),vs=states.map(s=>s.slice(3,6)),speeds=vs.map(norm),mean=speeds.reduce((a,x)=>a+x,0)/count;const order=norm([0,1,2].map(k=>vs.reduce((a,v,i)=>a+v[k]/Math.max(speeds[i],1e-9),0)/count));let visited=new Set(),largest=0;for(let i=0;i<count;i++){if(visited.has(i))continue;let q=[i],size=0;visited.add(i);while(q.length){const j=q.pop();size++;for(let k=0;k<count;k++)if(!visited.has(k)&&norm(states[j].slice(0,3).map((v,d)=>v-states[k][d]))<PARAM.radius){visited.add(k);q.push(k);}}largest=Math.max(largest,size);}return {order,largestFraction:largest/count,meanSpeed:mean,radius:Math.sqrt(states.reduce((a,s)=>a+norm(s.slice(0,3).map((v,k)=>v-center[k]))**2,0)/count),heightSpan:Math.max(...states.map(s=>s[2]))-Math.min(...states.map(s=>s[2])),center};}
function run({seed=1,count=50,mode='boids',dt=.005,duration=30,record=true}={}){
 let states=initial(seed,count),start=states.map(s=>s.slice()),frames=[],samples=[],controls,minimum=Infinity,stopReason=null,maxTilt=0,saturated=0;
 function sample(t){samples.push({t,...measures(states)});if(record)frames.push([t,...states.flatMap(s=>[...s.slice(0,3),...s.slice(6,10)])]);}sample(0);
 let end=0;for(let step=0;step<Math.round(duration/dt);step++){let t=step*dt;if(step%Math.round(.01/dt)===0)controls=states.map((s,i)=>{const v=steer(i,states,t,mode).velocity;
 // Algebraic setpoint conversion gives vertical acceleration 2.5*(requestedVz-currentVz), before the existing controller clamps.
 return F.control(s,{vx:v[0],vy:v[1],z:s[2]+(2.5*v[2]+1.5*s[5])/6,yaw:Math.atan2(v[1],v[0])},2.25);});
 const old=states;states=states.map((s,i)=>{if(controls[i].saturated)saturated+=dt;return F.integrate(s,controls[i].u,dt);});end=(step+1)*dt;
 for(let i=0;i<count;i++){const s=states[i];maxTilt=Math.max(maxTilt,...F.euler(s.slice(6,10)).slice(0,2).map(Math.abs));if(!s.every(Number.isFinite)||s[2]<.075)stopReason='vehicle model limit';for(let j=i+1;j<count;j++){const d=swept(old[i].slice(0,3),s.slice(0,3),old[j].slice(0,3),states[j].slice(0,3));minimum=Math.min(minimum,d);if(d<.15)stopReason='contact envelope reached';}}
 if(stopReason||((step+1)%Math.round(.1/dt)===0))sample(+end.toFixed(6));if(stopReason)break;
 }
 return {config:{seed,count,mode,dt,duration},initial:start,final:states,metrics:{minimum,stopReason,end,maxTiltDegrees:maxTilt*180/Math.PI,saturationFraction:saturated/(count*end),initial:samples[0],final:samples.at(-1)},samples,...(record?{frames}:{})};
}
module.exports={run,steer,PARAM,initial,measures};if(require.main===module)console.log(JSON.stringify(run(JSON.parse(process.argv[2]||'{}'))));
