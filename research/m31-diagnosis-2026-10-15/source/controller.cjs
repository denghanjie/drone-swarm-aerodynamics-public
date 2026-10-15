'use strict';
// Minimal, explicit adaptation of the frozen M31 steer function.
// Natural mode must reproduce the frozen function exactly before intervention results count.
const path=require('path');
const root=path.resolve(__dirname,'../../..');
const S=require(path.join(root,'outputs/milestone-31-source/sim.cjs'));
const G=require(path.join(root,'outputs/milestone-31-source/geometry.cjs'));
const {repair,residual}=require(path.join(root,'outputs/milestone-31-source/wall-filter.cjs'));
const P=S.P,course=S.course,routeTarget=S.routeTarget;
const norm=a=>Math.hypot(...a),cap=(x,l,h)=>Math.max(l,Math.min(h,x)),smooth=(a,b,x)=>{const t=cap((x-a)/(b-a),0,1);return t*t*(3-2*t)},limit=v=>{const n=norm(v);return v.map(x=>x*Math.min(1,P.maxSpeed/Math.max(n,1e-12)))};
function steer(i,states,ids,mode='boids',filter='baseline',diagnostic=null,options={}){
 const socialIds=options.reverseSocial?ids.slice().reverse():ids;
 let pairIds=options.reversePairs?ids.slice().reverse():ids;
 const override=options.pairOverride?.i===i?options.pairOverride:null;
 if(override?.include&&!pairIds.includes(override.j))pairIds=[...pairIds,override.j].sort((a,b)=>a-b);
 const s=states[i],v=s.slice(3,6),speed=norm(v),a=v.map(x=>1.2*(P.cruise-speed)*x/Math.max(speed,.01)),sep=[0,0,0],social=[0,0,0];let weight=0;
 for(const j of socialIds){const q=states[j],dvec=q.slice(0,3).map((x,k)=>x-s[k]),d=norm(dvec),w=1-smooth(P.fade,P.neighbor,d);weight+=w;for(let k=0;k<3;k++){social[k]+=w*(P.alignment*(q[3+k]-v[k])+P.cohesion*dvec[k]);if(d<P.separationRadius&&d>1e-9)sep[k]-=P.separation*(1/d-1/P.separationRadius)*dvec[k]/d;}}
 if(mode!=='goal-only')for(let k=0;k<3;k++)a[k]+=sep[k];if(mode==='boids')for(let k=0;k<3;k++)a[k]+=social[k]/Math.max(1,weight);
 const target=routeTarget(s[0]+.8),errors=[target[1]-s[1],target[2]-s[2]],outside=errors.map(e=>Math.sign(e)*Math.max(0,Math.abs(e)-.55)),desired=[P.forward,cap(.8*outside[0],-.6,.6),cap(.8*outside[1],-.6,.6)];
 desired[0]*=1/(1+.15*(outside[0]**2+outside[1]**2));
 for(let k=0;k<3;k++)a[k]+=1.3*(desired[k]-v[k]);let out=limit(v.map((x,k)=>x+P.steeringHorizon*a[k]));
 const preferred=out.slice();
 const constraints=[];for(const box of course.boxes){const reach=1.6+P.bodyRadius+1e-10;if(s[0]<box.min[0]-reach||s[0]>box.max[0]+reach||s[1]<box.min[1]-reach||s[1]>box.max[1]+reach||s[2]<box.min[2]-reach||s[2]>box.max[2]+reach)continue;const q=G.boxDistance(s,box),clear=q.distance-P.bodyRadius;if(clear<1.6)constraints.push({obstacle:box.id,n:q.normal,lower:-(clear-P.margin)/P.filterHorizon});}
 const walls=constraints.slice();
 for(const j of pairIds){const q=states[j],delta=s.slice(0,3).map((x,k)=>x-q[k]),d=norm(delta);const include=override?.j===j?override.include:d<1.5;if(include&&d>1e-9){const n=delta.map(x=>x/d);constraints.push({neighbor:j,n,lower:q.slice(3,6).reduce((z,x,k)=>z+x*n[k],0)-(d-P.pairMargin)/P.filterHorizon});}}
 for(let it=0;it<P.iterations;it++){for(const c of constraints){const radial=out.reduce((z,x,k)=>z+x*c.n[k],0);if(radial<c.lower)out=out.map((x,k)=>x+(c.lower-radial)*c.n[k]);}out=limit(out);}
 const before=out.slice(),repaired=filter==='wall-priority'?repair(out,walls,P.maxSpeed):null;
 if(repaired)out=repaired.velocity;
 if(diagnostic)diagnostic({velocity:out.slice(),actual:v,walls,pairs:constraints.slice(walls.length),beforeWallResidual:residual(before,walls,P.maxSpeed),wallResidual:residual(out,walls,P.maxSpeed),pairResidual:residual(out,constraints.slice(walls.length),P.maxSpeed),iterations:repaired?.iterations||0,converged:repaired?.converged??null,preferred,beforeWall:before});
 return out;
}
module.exports={steer};
