/* Original 6-DOF rigid-body simulator. World/body +z up, quaternion [x,y,z,w]. */
(function(root){'use strict';
const P=Object.freeze({m:.027,g:9.81,I:[1.4e-5,1.4e-5,2.17e-5],a:.028,kf:3.16e-10,km:7.94e-12,motorTau:.04,controlDt:.01,tiltMax:Math.PI/12,duration:16});
const rotors=[[P.a,P.a,1],[-P.a,P.a,-1],[-P.a,-P.a,1],[P.a,-P.a,-1]];
const clamp=(x,a,b)=>Math.max(a,Math.min(b,x)),add=(a,b)=>a.map((x,i)=>x+b[i]),scale=(a,k)=>a.map(x=>x*k),dot=(a,b)=>a.reduce((s,x,i)=>s+x*b[i],0),cross=(a,b)=>[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]],norm=a=>Math.hypot(...a),unit=a=>scale(a,1/norm(a));
function qmul(a,b){const v=add(add(scale(b.slice(0,3),a[3]),scale(a.slice(0,3),b[3])),cross(a,b));return [...v,a[3]*b[3]-dot(a.slice(0,3),b.slice(0,3))];}
function rotate(q,v){const t=scale(cross(q,v),2);return add(v,add(scale(t,q[3]),cross(q,t)));}
function quaternionFromBasis(x,y,z){const m=[x[0],y[0],z[0],x[1],y[1],z[1],x[2],y[2],z[2]],tr=m[0]+m[4]+m[8];let q;
 if(tr>0){const s=Math.sqrt(tr+1)*2;q=[(m[7]-m[5])/s,(m[2]-m[6])/s,(m[3]-m[1])/s,s/4];}
 else if(m[0]>m[4]&&m[0]>m[8]){const s=Math.sqrt(1+m[0]-m[4]-m[8])*2;q=[s/4,(m[1]+m[3])/s,(m[2]+m[6])/s,(m[7]-m[5])/s];}
 else if(m[4]>m[8]){const s=Math.sqrt(1+m[4]-m[0]-m[8])*2;q=[(m[1]+m[3])/s,s/4,(m[5]+m[7])/s,(m[2]-m[6])/s];}
 else{const s=Math.sqrt(1+m[8]-m[0]-m[4])*2;q=[(m[2]+m[6])/s,(m[5]+m[7])/s,s/4,(m[3]-m[1])/s];}return unit(q);
}
function euler(q){const [x,y,z,w]=q;return [Math.atan2(2*(w*x+y*z),1-2*(x*x+y*y)),Math.asin(clamp(2*(w*y-z*x),-1,1)),Math.atan2(2*(w*z+x*y),1-2*(y*y+z*z))];}
function wrench(f){let T=0,t=[0,0,0];f.forEach((v,i)=>{const [x,y,s]=rotors[i];T+=v;t[0]+=y*v;t[1]-=x*v;t[2]+=s*P.km/P.kf*v;});return {T,t};}
function mix(T,t,ratio){const k=P.km/P.kf,raw=rotors.map(([x,y,s])=>T/4+y*t[0]/(4*P.a**2)-x*t[1]/(4*P.a**2)+s*t[2]/(4*k)),max=ratio*P.m*P.g/4;return {u:raw.map(f=>clamp(f,0,max)),saturated:raw.some(f=>f<0||f>max)};}
// State p[0:3], v[3:6], q[6:10], body omega[10:13], motor thrusts[13:17].
function derivative(y,u){const q=y.slice(6,10),w=y.slice(10,13),{T,t}=wrench(y.slice(13)),F=rotate(q,[0,0,T/P.m]),gyro=cross(w,w.map((v,i)=>v*P.I[i])),dq=scale(qmul(q,[...w,0]),.5);return [...y.slice(3,6),F[0],F[1],F[2]-P.g,...dq,...t.map((v,i)=>(v-gyro[i])/P.I[i]),...u.map((v,i)=>(v-y[13+i])/P.motorTau)];}
function integrate(y,u,h){const next=(k,s)=>y.map((v,i)=>v+s*k[i]),k1=derivative(y,u),k2=derivative(next(k1,h/2),u),k3=derivative(next(k2,h/2),u),k4=derivative(next(k3,h),u);const out=y.map((v,i)=>v+h*(k1[i]+2*k2[i]+2*k3[i]+k4[i])/6),q=unit(out.slice(6,10));out.splice(6,4,...q);return out;}
function target(t,scenario){let vx=0,vy=0,z=1,yaw=0,phase='Hover';
 if(scenario==='move'){if(t>=2&&t<6){vx=.5;phase='Move along X';}else if(t>=6)phase='Brake and hold';}
 if(scenario==='climb'&&t>=2){z=3;phase='Climb request';}
 if(scenario==='yaw'&&t>=2){yaw=Math.PI/2;phase='Turn 90°';}
 if(scenario==='flight'){if(t>=2&&t<5){vx=.5;phase='Move along X';}else if(t>=5&&t<8){vy=.5;phase='Move along Y';}else if(t>=8){z=1.8;phase=t<11?'Climb and brake':'Turn 90°';if(t>=11)yaw=Math.PI/2;}}
 return {vx,vy,z,yaw,phase};}
function control(y,r,ratio){const a=[2.5*(r.vx-y[3]),2.5*(r.vy-y[4]),P.g+clamp(6*(r.z-y[2])-4*y[5],-4,5)];const xy=Math.hypot(a[0],a[1]),limit=a[2]*Math.tan(P.tiltMax);if(xy>limit){a[0]*=limit/xy;a[1]*=limit/xy;}
 const bz=unit(a),heading=[Math.cos(r.yaw),Math.sin(r.yaw),0],by=unit(cross(bz,heading)),bx=cross(by,bz),qd=quaternionFromBasis(bx,by,bz),q=y.slice(6,10),err=qmul([-q[0],-q[1],-q[2],q[3]],qd),sign=err[3]<0?-1:1,w=y.slice(10,13),gyro=cross(w,w.map((v,i)=>v*P.I[i]));
 const torque=w.map((v,i)=>P.I[i]*(100*2*sign*err[i]-20*v)+gyro[i]);
 const axis=rotate(q,[0,0,1]),T=P.m*a[2]/Math.max(.5,axis[2]);return {...mix(T,torque,ratio),qd};}
class Simulation{constructor({scenario='flight',ratio=2.25,dt=.005}={}){if(!['flight','move','climb','hover','yaw'].includes(scenario)||ratio<1.1||ratio>2.25||dt<=0||Math.abs(P.controlDt/dt-Math.round(P.controlDt/dt))>1e-8)throw Error('Invalid configuration');this.scenario=scenario;this.ratio=ratio;this.dt=dt;this.n=0;this.t=0;this.y=[0,0,1,0,0,0,0,0,0,1,0,0,0,...Array(4).fill(P.m*P.g/4)];this.c=control(this.y,target(0,scenario),ratio);this.satTime=0;this.history=[this.sample()];}
 sample(){const r=target(this.t,this.scenario),e=euler(this.y.slice(6,10));return {t:this.t,x:this.y[0],y:this.y[1],z:this.y[2],vx:this.y[3],vy:this.y[4],vz:this.y[5],qx:this.y[6],qy:this.y[7],qz:this.y[8],qw:this.y[9],roll:e[0],pitch:e[1],yaw:e[2],wx:this.y[10],wy:this.y[11],wz:this.y[12],f1:this.y[13],f2:this.y[14],f3:this.y[15],f4:this.y[16],thrust:this.y.slice(13).reduce((a,b)=>a+b,0),targetVx:r.vx,targetVy:r.vy,targetZ:r.z,targetYaw:r.yaw,phase:r.phase,saturated:this.c.saturated};}
 step(){if(this.t>=P.duration-1e-9)return false;if(this.n%Math.round(P.controlDt/this.dt)===0)this.c=control(this.y,target(this.t,this.scenario),this.ratio);if(this.c.saturated)this.satTime+=this.dt;this.y=integrate(this.y,this.c.u,this.dt);this.n++;this.t=this.n*this.dt;this.history.push(this.sample());return true;}
 run(){while(this.step());return this;}
 metrics(){const h=this.history;return {finalPosition:this.y.slice(0,3),finalSpeed:norm(this.y.slice(3,6)),finalEulerDeg:euler(this.y.slice(6,10)).map(x=>x*180/Math.PI),maxThrustWeight:Math.max(...h.map(s=>s.thrust/(P.m*P.g))),saturationFraction:this.satTime/P.duration,maxQuaternionNormError:Math.max(...h.map(s=>Math.abs(Math.hypot(s.qx,s.qy,s.qz,s.qw)-1)))};}
}
const api={P,rotors,Simulation,derivative,integrate,control,mix,wrench,target,qmul,rotate,euler,quaternionFromBasis};if(typeof module!=='undefined')module.exports=api;else root.Drone3D=api;
})(typeof globalThis!=='undefined'?globalThis:this);
