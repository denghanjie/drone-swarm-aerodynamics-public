/* Original planar mechanics model. SI units. See step-02-results.md for scope. */
(function(root){
'use strict';
const P=Object.freeze({m:0.027,g:9.81,I:1.4e-5,lever:0.028,motorTau:0.04,tiltMax:Math.PI/12,controlDt:0.01,duration:12});
const clamp=(x,a,b)=>Math.max(a,Math.min(b,x));
// State: x,z,vx,vz,theta,omega,left-group thrust,right-group thrust.
// Positive theta tilts thrust toward +x; left group's upward force gives +theta.
function derivative(y,u,p=P){
 const T=y[6]+y[7];
 return [y[2],y[3],T*Math.sin(y[4])/p.m,T*Math.cos(y[4])/p.m-p.g,y[5],p.lever*(y[6]-y[7])/p.I,(u[0]-y[6])/p.motorTau,(u[1]-y[7])/p.motorTau];
}
function integrate(y,u,h,p=P){
 const add=(a,b,k)=>a.map((v,i)=>v+k*b[i]);
 const k1=derivative(y,u,p),k2=derivative(add(y,k1,h/2),u,p),k3=derivative(add(y,k2,h/2),u,p),k4=derivative(add(y,k3,h),u,p);
 return y.map((v,i)=>v+h*(k1[i]+2*k2[i]+2*k3[i]+k4[i])/6);
}
function target(t,scenario){
 if(scenario==='climb')return {vx:0,z:t<2?1:3,phase:t<2?'Hover':'Climb request'};
 if(scenario==='hover')return {vx:0,z:1,phase:'Hover'};
 return {vx:t>=2&&t<6?0.5:0,z:1,phase:t<2?'Hover':t<6?'Move right':t<9?'Brake':'Hold speed at zero'};
}
function control(y,r,ratio,p=P){
 const ax=clamp(2.5*(r.vx-y[2]),-3,3),az=clamp(6*(r.z-y[1])-4*y[3],-4,5);
 const desiredTheta=clamp(Math.atan2(ax,p.g+az),-p.tiltMax,p.tiltMax);
 const total=p.m*(p.g+az)/Math.max(0.5,Math.cos(y[4]));
 const torque=p.I*(100*(desiredTheta-y[4])-20*y[5]);
 const raw=[total/2+torque/(2*p.lever),total/2-torque/(2*p.lever)];
 const maxGroup=ratio*p.m*p.g/2;
 return {u:raw.map(v=>clamp(v,0,maxGroup)),saturated:raw.some(v=>v<0||v>maxGroup),desiredTheta};
}
class Simulation{
 constructor({scenario='move',ratio=2.25,dt=0.005}={}){
  if(!['move','hover','climb'].includes(scenario)||ratio<1||ratio>2.25||dt<=0||Math.abs(P.controlDt/dt-Math.round(P.controlDt/dt))>1e-9)throw Error('Invalid simulation configuration');
  this.scenario=scenario;this.ratio=ratio;this.dt=dt;this.n=0;this.t=0;this.y=[0,1,0,0,0,0,P.m*P.g/2,P.m*P.g/2];this.c=control(this.y,target(0,scenario),ratio);this.satTime=0;this.history=[this.sample()];
 }
 sample(){const r=target(this.t,this.scenario);return {t:this.t,x:this.y[0],z:this.y[1],vx:this.y[2],vz:this.y[3],theta:this.y[4],omega:this.y[5],thrust:this.y[6]+this.y[7],left:this.y[6],right:this.y[7],targetVx:r.vx,targetZ:r.z,phase:r.phase,saturated:this.c.saturated};}
 step(){if(this.t>=P.duration-1e-9)return false;
  if(this.n%Math.round(P.controlDt/this.dt)===0)this.c=control(this.y,target(this.t,this.scenario),this.ratio);
  if(this.c.saturated)this.satTime+=this.dt;
  this.y=integrate(this.y,this.c.u,this.dt);this.n++;this.t=this.n*this.dt;this.history.push(this.sample());return true;
 }
 run(){while(this.step());return this;}
 metrics(){const h=this.history;return {finalX:this.y[0],finalZ:this.y[1],finalVx:this.y[2],maxAltitudeError:Math.max(...h.map(s=>Math.abs(s.z-s.targetZ))),maxTiltDeg:Math.max(...h.map(s=>Math.abs(s.theta)*180/Math.PI)),maxThrustWeight:Math.max(...h.map(s=>s.thrust/(P.m*P.g))),saturationFraction:this.satTime/P.duration};}
}
const api={P,Simulation,target,control,derivative,integrate};if(typeof module!=='undefined')module.exports=api;else root.DronePhysics=api;
})(typeof globalThis!=='undefined'?globalThis:this);
