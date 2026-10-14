'use strict';
const {source}=require('./source.cjs'),M=require('./exact-aero.cjs'),{sha}=require('./io.cjs');
const B=source('outputs/milestone-31-source/sim.cjs'),{Grid}=source('outputs/milestone-31-source/grid.cjs');
function controller(states,tick){
 const grid=new Grid(states,B.P.neighbor),rows=[];
 const controls=states.map((s,i)=>{
  const neighbors=grid.neighbors(i,B.P.neighbor);let diagnostic;
  const v=B.steer(i,states,neighbors,'boids','wall-priority',d=>{diagnostic=d;});
  const reference={vx:v[0],vy:v[1],z:s[2]+(2.5*v[2]+1.5*s[5])/6,yaw:Math.atan2(v[1],v[0])};
  const c=M.F.control(s,reference,2.25),err=M.F.qmul([-s[6],-s[7],-s[8],s[9]],c.qd);
  const az=M.F.P.g+Math.max(-4,Math.min(5,6*(reference.z-s[2])-4*s[5]));
  const tiltExcess=Math.hypot(2.5*(v[0]-s[3]),2.5*(v[1]-s[4]))-az*Math.tan(M.F.P.tiltMax);
  const max=2.25*M.F.P.m*M.F.P.g/4;
  const signature={neighbors,walls:diagnostic.walls.map(x=>x.obstacle),pairs:diagnostic.pairs.map(x=>x.neighbor),torqueErrorSign:err[3]<0?-1:1,tiltClipped:tiltExcess>0,motorBounds:c.u.map(x=>x===0?-1:x===max?1:0),wallRepairIterations:diagnostic.iterations,wallRepairConverged:diagnostic.converged,speedAtLimit:Math.hypot(...v)>=B.P.maxSpeed-1e-12};
  rows.push({drone:i,signature,steeringSpeed:Math.hypot(...v),desiredHorizontalSpeedNorm:Math.hypot(v[0],v[1]),torqueErrorScalar:err[3],tiltExcess,saturated:c.saturated,commands:c.u,...diagnostic});
  return c;
 });
 const commands=controls.map(c=>c.u);
 return {controls,commands,event:{tick,type:'controller',commands,commandsSha256:sha(JSON.stringify(commands)),branchSignatureSha256:sha(JSON.stringify(rows.map(r=>r.signature))),rows}};
}
module.exports={controller,B};
