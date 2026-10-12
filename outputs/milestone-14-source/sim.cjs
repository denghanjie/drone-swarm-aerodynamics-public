'use strict';
const F=require('../step02c-source/physics.cjs'),{swept}=require('../milestone-10-source/sim.cjs');
const PARAM=Object.freeze({radius:1.8,separationRadius:.85,separation:1.5,alignment:2,cohesion:.22,cruise:.65,maxSpeed:.9,steeringHorizon:.4});
const COURSES=Object.freeze({
 slalom:{name:'Three obstacles, changing height',finish:10,spheres:[{center:[-1,-.5,3.8],radius:1},{center:[3,.7,4.8],radius:1.1},{center:[7,-.6,3.5],radius:.9}],route:[[-1,-1.5,5.8],[3,-1.5,6.5],[7,1.7,5.3],[11,0,4.5]]},
 staggered:{name:'Two staggered 3 m openings',finish:6.2,gates:[{center:[0,-1,3.5],width:3},{center:[5,1,5],width:3}]},
 tight:{name:'Two staggered 1.8 m openings',finish:6.2,gates:[{center:[0,-1,3.5],width:1.8},{center:[5,1,5],width:1.8}]}
});
const norm=a=>Math.hypot(...a),cap=(x,l,h)=>Math.max(l,Math.min(h,x));
function rng(seed){let x=seed>>>0;return()=>((x=(1664525*x+1013904223)>>>0)/4294967296);}
function initial(seed,count){const r=rng(seed),states=[];while(states.length<count){const p=[(r()-.5)*4.6,(r()-.5)*4.6,4+(r()-.5)*4.6];if(norm([p[0],p[1],p[2]-4])>2.3||states.some(s=>norm(p.map((x,k)=>x-s[k]))<.55))continue;let v=[r()-.5,r()-.5,r()-.5],n=norm(v);v=v.map(x=>x/n*.35);const yaw=Math.atan2(v[1],v[0]);states.push([...p,...v,0,0,Math.sin(yaw/2),Math.cos(yaw/2),0,0,0,...Array(4).fill(F.P.m*F.P.g/4)]);}return states;}
function steer(i,states,t,mode='boids',scenario='slalom'){
 const s=states[i],v=s.slice(3,6),n=norm(v),a=v.map(x=>1.2*(PARAM.cruise-n)*x/Math.max(n,.01)),sep=[0,0,0],align=[0,0,0],coh=[0,0,0];let neighbors=0;
 for(let j=0;j<states.length;j++){if(i===j)continue;const q=states[j],delta=q.slice(0,3).map((x,k)=>x-s[k]),d=norm(delta);if(d>=PARAM.radius)continue;neighbors++;for(let k=0;k<3;k++){align[k]+=q[3+k];coh[k]+=delta[k];if(d<PARAM.separationRadius&&d>1e-9)sep[k]-=PARAM.separation*(1/d-1/PARAM.separationRadius)*delta[k]/d;}}
 if(mode==='separation-only')for(let k=0;k<3;k++)a[k]+=sep[k];
 if(mode==='boids'||mode==='priority')for(let k=0;k<3;k++)a[k]+=sep[k]+(neighbors?PARAM.alignment*(align[k]/neighbors-v[k])+PARAM.cohesion*coh[k]/neighbors:0);
 // All drones share a known map and route preference; nobody assigns individual trajectories.
 const course=COURSES[scenario];let desired=[.55,0,0];
 if(course.spheres){
  const target=course.route.find(p=>s[0]<p[0])||[s[0]+3,0,4.5];
  desired=[.55,cap(.7*(target[1]-s[1]),-.55,.55),cap(.7*(target[2]-s[2]),-.55,.55)];
  for(const o of course.spheres){const delta=s.slice(0,3).map((v,k)=>v-o.center[k]),d=norm(delta),clear=d-o.radius-.075;
   if(clear<1.2){const closing=Math.max(0,-v.reduce((z,x,k)=>z+x*delta[k]/Math.max(d,1e-9),0));for(let k=0;k<3;k++)a[k]+=(2*Math.max(0,1.2-clear)+2*closing)*delta[k]/Math.max(d,1e-9);}}
 }else{
  const gate=course.gates.find(g=>s[0]<g.center[0]+.4);
  if(gate){const x=s[0]-gate.center[0],y=s[1]-gate.center[1],z=s[2]-gate.center[2],edge=gate.width/2-.25;
   const ey=cap(y,-edge,edge)-y,ez=cap(z,-edge,edge)-z;
   desired[1]=cap(ey,-.6,.6);desired[2]=cap(ez,-.6,.6);
   if(x>-2)desired[0]*=cap(1-Math.hypot(ey,ez)/.4,0,1);
   if(x<0&&x>-1.2&&Math.min(gate.width/2-Math.abs(y),gate.width/2-Math.abs(z))<.3)a[0]-=2*(1.2+x)+2*Math.max(0,v[0]);
  }
 }
 for(let k=0;k<3;k++)a[k]+=1.3*(desired[k]-v[k]);
 if(s[2]<1.5)a[2]+=3*(1.5-s[2])+2*Math.max(0,-v[2]);
 const cmd=v.map((x,k)=>x+PARAM.steeringHorizon*a[k]),speed=norm(cmd),base=cmd.map(x=>x*Math.min(1,PARAM.maxSpeed/Math.max(speed,1e-9))),filtered=mode==='priority'?clearanceFilter(s,base,scenario):base;return {velocity:filtered,base,changed:norm(filtered.map((v,k)=>v-base[k]))>1e-9,neighbors};
}
// Local velocity-command filter. Uses this drone's state and the known map only.
// This heuristic is not a formal barrier certificate for the lagged rigid-body plant.
const FILTER=Object.freeze({margin:.25,lookahead:1.2,approach:1.8,exit:.5});
function clearanceFilter(s,base,scenario){const out=base.slice(),course=COURSES[scenario];
 if(course.gates)for(const g of course.gates){const x=s[0]-g.center[0],edge=g.width/2-FILTER.margin;
  if(x<-FILTER.approach||x>FILTER.exit)continue;
  let unsafe=false;const arrival=Math.min(2,Math.max(.3,-x/Math.max(.15,s[3])));
  for(const k of [1,2]){const q=s[k]-g.center[k];out[k]=cap(out[k],-(edge+q)/FILTER.lookahead,(edge-q)/FILTER.lookahead);if(Math.abs(q+arrival*s[3+k])>edge||Math.abs(q)>edge)unsafe=true;}
  if(x<0&&unsafe)out[0]=Math.min(out[0],Math.max(0,-x-.35)/FILTER.lookahead);
 }
 if(course.spheres)for(const o of course.spheres){const d=s.slice(0,3).map((v,k)=>v-o.center[k]),n=norm(d),normal=d.map(v=>v/Math.max(n,1e-9)),clear=n-o.radius-.075;if(clear>1.2)continue;const radial=out.reduce((a,v,k)=>a+v*normal[k],0),lower=-(clear-.25)/FILTER.lookahead;if(radial<lower)for(let k=0;k<3;k++)out[k]+=(lower-radial)*normal[k];}
 const speed=norm(out);return out.map(v=>v*Math.min(1,PARAM.maxSpeed/Math.max(speed,1e-9)));
}
function measures(states){const count=states.length,center=[0,1,2].map(k=>states.reduce((a,s)=>a+s[k],0)/count),vs=states.map(s=>s.slice(3,6)),speeds=vs.map(norm),mean=speeds.reduce((a,x)=>a+x,0)/count;const order=norm([0,1,2].map(k=>vs.reduce((a,v,i)=>a+v[k]/Math.max(speeds[i],1e-9),0)/count));let visited=new Set(),largest=0;for(let i=0;i<count;i++){if(visited.has(i))continue;let q=[i],size=0;visited.add(i);while(q.length){const j=q.pop();size++;for(let k=0;k<count;k++)if(!visited.has(k)&&norm(states[j].slice(0,3).map((v,d)=>v-states[k][d]))<PARAM.radius){visited.add(k);q.push(k);}}largest=Math.max(largest,size);}return {order,largestFraction:largest/count,meanSpeed:mean,radius:Math.sqrt(states.reduce((a,s)=>a+norm(s.slice(0,3).map((v,k)=>v-center[k]))**2,0)/count),heightSpan:Math.max(...states.map(s=>s[2]))-Math.min(...states.map(s=>s[2])),center};}
function run({seed=1,count=50,mode='boids',dt=.005,duration=60,record=true,scenario='slalom'}={}){
 let states=initial(seed,count).map(s=>{s[0]-=6;return s;}),start=states.map(s=>s.slice()),frames=[],samples=[],controls,minimum=Infinity,stopReason=null,maxTilt=0,saturated=0,obstacleMinimum=Infinity,crossings=Array(count).fill(null),filterActive=0,commandCount=0,lastCommands=[],failure=null;
 function sample(t){samples.push({t,passed:crossings.filter(x=>x!==null).length,...measures(states)});if(record)frames.push([t,...states.flatMap(s=>[...s.slice(0,3),...s.slice(6,10)])]);}sample(0);
 let end=0;for(let step=0;step<Math.round(duration/dt);step++){let t=step*dt;if(step%Math.round(.01/dt)===0)controls=states.map((s,i)=>{const command=steer(i,states,t,mode,scenario);lastCommands[i]=command;commandCount++;if(command.changed)filterActive++;const v=command.velocity;
 // Algebraic setpoint conversion gives vertical acceleration 2.5*(requestedVz-currentVz), before the existing controller clamps.
 return F.control(s,{vx:v[0],vy:v[1],z:s[2]+(2.5*v[2]+1.5*s[5])/6,yaw:Math.atan2(v[1],v[0])},2.25);});
 const old=states;states=states.map((s,i)=>{if(controls[i].saturated)saturated+=dt;return F.integrate(s,controls[i].u,dt);});end=(step+1)*dt;
 for(let i=0;i<count;i++){const s=states[i];const clearance=obstacleClearance(old[i].slice(0,3),s.slice(0,3),scenario);obstacleMinimum=Math.min(obstacleMinimum,clearance);if(clearance<0)stopReason='obstacle contact envelope';if(old[i][0]<COURSES[scenario].finish&&s[0]>=COURSES[scenario].finish&&crossings[i]===null)crossings[i]=end;maxTilt=Math.max(maxTilt,...F.euler(s.slice(6,10)).slice(0,2).map(Math.abs));if(!s.every(Number.isFinite)||s[2]<.075)stopReason='vehicle model limit';for(let j=i+1;j<count;j++){const d=swept(old[i].slice(0,3),s.slice(0,3),old[j].slice(0,3),states[j].slice(0,3));minimum=Math.min(minimum,d);if(d<.15)stopReason='contact envelope reached';}}
 if(stopReason)failure={t:end,reason:stopReason,states:states.map(s=>s.slice()),commands:lastCommands};
 if(stopReason||((step+1)%Math.round(.1/dt)===0))sample(+end.toFixed(6));if(stopReason)break;
 }
 return {config:{seed,count,mode,dt,duration,scenario},initial:start,final:states,crossings,failure,metrics:{filterActiveFraction:filterActive/commandCount,obstacleMinimum,passed:crossings.filter(x=>x!==null).length,minimum,stopReason,end,maxTiltDegrees:maxTilt*180/Math.PI,saturationFraction:saturated/(count*end),initial:samples[0],final:samples.at(-1)},samples,...(record?{frames}:{})};
}
// Exact minimum distance of a straight segment to each half-plane of the aperture wall.
function halfDistance(a,b,k,sign,edge){const x=a[0],dx=b[0]-x,h=edge-sign*a[k],dh=-sign*(b[k]-a[k]);let cuts=[0,1];if(dh&&-h/dh>0&&-h/dh<1)cuts.push(-h/dh);cuts.sort((a,b)=>a-b);let best=Infinity;for(let i=0;i<cuts.length-1;i++){const l=cuts[i],r=cuts[i+1],active=h+dh*(l+r)/2>0,H=active?h:0,D=active?dh:0,t=cap(-(x*dx+H*D)/(dx*dx+D*D||1),l,r);best=Math.min(best,Math.hypot(x+dx*t,Math.max(0,h+dh*t)));}return best;}
function obstacleClearance(a,b,scenario){const course=COURSES[scenario];if(course.spheres)return Math.min(...course.spheres.map(o=>swept(a,b,o.center,o.center)-o.radius-.075));return Math.min(...course.gates.map(g=>{const aa=a.map((v,k)=>v-g.center[k]),bb=b.map((v,k)=>v-g.center[k]);return Math.min(...[1,2].flatMap(k=>[-1,1].map(sign=>halfDistance(aa,bb,k,sign,g.width/2))))-.075;}));}
module.exports={run,steer,PARAM,initial,measures,obstacleClearance,COURSES,clearanceFilter,FILTER};if(require.main===module)console.log(JSON.stringify(run(JSON.parse(process.argv[2]||'{}'))));
