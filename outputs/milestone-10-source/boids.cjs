'use strict';
// Local Boids steering only. No IDs, rows, lane assignments, phase state or reservations.
// Shared map/goal is environmental information. Only neighbors inside radius affect steering.
const PARAMETERS=Object.freeze({neighborRadius:1.25,separationRadius:.65,separationWeight:.75,alignmentWeight:.55,cohesionWeight:.16,goalWeight:.42,edgeMargin:.13});
const cap=(x,lo,hi)=>Math.max(lo,Math.min(hi,x));
function steer(i,states,{width=1.2,speed=.5,mode='boids'}={}){
 const s=states[i],p=PARAMETERS,sep=[0,0],align=[0,0],cohesion=[0,0];let neighbors=0;
 for(let j=0;j<states.length;j++){if(i===j)continue;const q=states[j],dx=s[0]-q[0],dy=s[1]-q[1],dz=s[2]-q[2],d=Math.hypot(dx,dy,dz);if(d>=p.neighborRadius)continue;neighbors++;align[0]+=q[3];align[1]+=q[4];cohesion[0]+=q[0]-s[0];cohesion[1]+=q[1]-s[1];if(d<p.separationRadius&&d>1e-8){const strength=p.separationWeight*(1/d-1/p.separationRadius);sep[0]+=strength*dx/d;sep[1]+=strength*dy/d;}}
 if(neighbors){for(let k=0;k<2;k++){align[k]=p.alignmentWeight*(align[k]/neighbors-s[3+k]);cohesion[k]=p.cohesionWeight*cohesion[k]/neighbors;}}
 // Each drone aims at its nearest interior gate point, then keeps traveling beyond it.
 // This is continuous goal/obstacle steering, not an assigned lane or a crossing reservation.
 const edge=width/2-p.edgeMargin,ty=s[0]<.35?cap(s[1],-edge,edge):s[1],dx=s[0]<.35?Math.max(.3,-s[0]+.3):1,dy=ty-s[1],norm=Math.hypot(dx,dy),goal=[p.goalWeight*dx/norm,p.goalWeight*dy/norm];
 // Local map lookahead: brake forward motion when the predicted gate intercept is outside the clearance.
 const tau=cap(-s[0]/Math.max(.15,s[3]),0,1.5),predY=s[1]+tau*s[4],outside=Math.max(0,Math.abs(predY)-edge);
 const obstacle=[0,0];if(s[0]<0&&s[0]>-1.2&&outside>0){obstacle[0]=-p.goalWeight*Math.min(1,outside/.15)*Math.max(0,1+(s[0]+.25)/1.2);obstacle[1]=-.8*Math.sign(predY)*outside;}
 const social=mode==='goal-only'?[0,0]:[sep[0]+align[0]+cohesion[0],sep[1]+align[1]+cohesion[1]];
 let vx=goal[0]+obstacle[0]+social[0],vy=goal[1]+obstacle[1]+social[1];const n=Math.hypot(vx,vy);if(n>speed){vx*=speed/n;vy*=speed/n;}
 return {vx,vy,refY:ty,neighbors,terms:{separation:mode==='goal-only'?[0,0]:sep,alignment:mode==='goal-only'?[0,0]:align,cohesion:mode==='goal-only'?[0,0]:cohesion,goal,obstacle}};
}
module.exports={steer,PARAMETERS};
