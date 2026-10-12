/* Original exploratory coupling; published wake + assumed constant ideal induced power.
   UMD module. Browser dependencies: Drone3D and WakeModel. */
(function(root){'use strict';
const D=typeof module!=='undefined'?require('./physics.cjs'):root.Drone3D;
const W=typeof module!=='undefined'?require('../step03a-source/wake.cjs'):root.WakeModel;
const {P,rotors,rotate,control,euler}=D;
const A=Math.PI*.023**2,rho=1.225,l=2*P.a; // illustrative 23 mm rotor radius; l is adjacent rotor spacing
function inducedPower(f,U=0){return f*(U/2+Math.sqrt(U*U/4+f/(2*rho*A)));}
function effectiveThrust(nominal,U){if(nominal<0||!Number.isFinite(nominal)||U<0||!Number.isFinite(U))throw Error('Invalid rotor input');if(nominal===0||U===0)return nominal;const power=inducedPower(nominal);let lo=0,hi=nominal;for(let i=0;i<40;i++){const mid=(lo+hi)/2;if(inducedPower(mid,U)>power)hi=mid;else lo=mid;}return (lo+hi)/2;}
function loads(y,{gap,offset,enabled}){
 const q=y.slice(6,10),axis=rotate(q,[0,0,1]),source=[offset,0,1+gap],nominal=y.slice(13,17),winds=[];
 const f=rotors.map(([x,yR],i)=>{const delta=rotate(q,[x,yR,0]),p=delta.map((v,k)=>v+y[k]),s=source[2]-p[2],r=Math.hypot(p[0]-source[0],p[1]);
 if(!enabled){winds.push(0);return nominal[i];}
 const w=W.hoverWake({downstream:s,radial:r,mass:P.m,propRadius:.023,motorDistance:l,rho});
 if(w.speedMS===null)throw Error('Rotor entered the unmodeled near field');
 const U=w.speedMS*Math.max(0,axis[2]);winds.push(U);return effectiveThrust(Math.max(0,nominal[i]),U);
 });return {f,winds};
}
function derivative(y,u,config){const {f}=loads(y,config),effective=y.slice();effective.splice(13,4,...f);const d=D.derivative(effective,u);if(config.model==='force-only'){const nominalTorque=D.wrench(y.slice(13)).t,effectiveTorque=D.wrench(f).t;for(let i=0;i<3;i++)d[10+i]+=(nominalTorque[i]-effectiveTorque[i])/P.I[i];}for(let i=0;i<4;i++)d[13+i]=(u[i]-y[13+i])/P.motorTau;return d;}
function integrate(y,u,h,config){const next=(d,a)=>y.map((v,i)=>v+a*d[i]),a=derivative(y,u,config),b=derivative(next(a,h/2),u,config),c=derivative(next(b,h/2),u,config),d=derivative(next(c,h),u,config),out=y.map((v,i)=>v+h*(a[i]+2*b[i]+2*c[i]+d[i])/6);const n=Math.hypot(...out.slice(6,10));for(let i=6;i<10;i++)out[i]/=n;return out;}
class Simulation{
 constructor({gap=.45,offset=0,enabled=true,model='rotor',controller='position',ratio=2.25,dt=.005,gains={kp:1,kv:2.5,ka:100,kw:20}}={}){if(!['position','velocity'].includes(controller))throw Error('Invalid controller');if(!['rotor','force-only'].includes(model))throw Error('Invalid model');if(![gap,offset,ratio,dt].every(Number.isFinite)||gap<.25||gap>.8||Math.abs(offset)>.2||ratio<1.1||ratio>2.25||dt<=0||Math.abs(.01/dt-Math.round(.01/dt))>1e-8)throw Error('Invalid configuration');if(!['kp','kv','ka','kw'].every(k=>Number.isFinite(gains[k])&&gains[k]>0))throw Error('Invalid gains');this.gains={...gains};Object.assign(this,{gap,offset,enabled,model,controller,ratio,dt,scenario:'hover',n:0,t:0,satTime:0,stopped:null});this.y=[0,0,1,0,0,0,0,0,0,1,0,0,0,...Array(4).fill(P.m*P.g/4)];this.c=this.command();this.history=[this.sample()];}
 reference(){let vx=0,vy=0;if(this.controller==='position'){vx=-this.gains.kp*this.y[0];vy=-this.gains.kp*this.y[1];const speed=Math.hypot(vx,vy);if(speed>.5){vx*=.5/speed;vy*=.5/speed;}}return {vx,vy,z:1,yaw:0};}
 command(){return control(this.y,this.reference(),this.ratio,this.gains);}
 sample(){const {f,winds}=loads(this.y,this),e=euler(this.y.slice(6,10));return {t:this.t,x:this.y[0],y:this.y[1],z:this.y[2],vx:this.y[3],vy:this.y[4],vz:this.y[5],qx:this.y[6],qy:this.y[7],qz:this.y[8],qw:this.y[9],roll:e[0],pitch:e[1],yaw:e[2],f1:f[0],f2:f[1],f3:f[2],f4:f[3],nominal1:this.y[13],nominal2:this.y[14],nominal3:this.y[15],nominal4:this.y[16],wind1:winds[0],wind2:winds[1],wind3:winds[2],wind4:winds[3],thrust:f.reduce((a,b)=>a+b,0),nominalThrust:this.y.slice(13).reduce((a,b)=>a+b,0),targetVx:this.reference().vx,targetVy:this.reference().vy,targetZ:1,targetYaw:0,saturated:this.c.saturated,model:this.model,controller:this.controller,phase:!this.enabled?'No interaction':this.model==='rotor'?'Uneven rotor loads':'Total force only'};}
 step(){if(this.stopped||this.t>=P.duration-1e-9)return false;if(this.n%Math.round(.01/this.dt)===0)this.c=this.command();let next;try{next=integrate(this.y,this.c.u,this.dt,this);}catch(e){this.stopped=e.message;return false;}
 if(!next.every(Number.isFinite)){this.stopped='Nonfinite state';return false;}
 if(rotate(next.slice(6,10),[0,0,1])[2]<Math.cos(Math.PI/9)){this.stopped='Tilt exceeded the 20° exploratory limit';return false;}
 this.y=next;if(this.c.saturated)this.satTime+=this.dt;this.n++;this.t=this.n*this.dt;this.history.push(this.sample());return true;}
 run(){while(this.step());return this;}
 metrics(){return {maxAltitudeLoss:1-Math.min(...this.history.map(s=>s.z)),finalAltitude:this.y[2],maxPitchDeg:Math.max(...this.history.map(s=>Math.abs(s.pitch)))*180/Math.PI,finalX:this.y[0],saturationFraction:this.t?this.satTime/this.t:0,stopped:this.stopped};}
}
const api={...D,Simulation,effectiveThrust,inducedPower,loads,pairDerivative:derivative,pairIntegrate:integrate,geometry:{rotorRadius:.023,motorDistance:l,rho}};if(typeof module!=='undefined')module.exports=api;else root.DroneControllers=api;
})(typeof globalThis!=='undefined'?globalThis:this);
