const assert=require('node:assert/strict');
const fs=require('node:fs');
const {P,Simulation,integrate}=require('./physics.cjs');
const checks=[];
function check(name,fn){fn();checks.push({name,pass:true});}
check('Hover equilibrium for 12 seconds',()=>{const s=new Simulation({scenario:'hover'}).run();assert(Math.abs(s.y[1]-1)<1e-10);assert(Math.abs(s.y[0])<1e-10);});
check('Free fall agrees with z=z0-gt²/2',()=>{let y=[0,10,0,0,0,0,0,0];for(let i=0;i<200;i++)y=integrate(y,[0,0],.005);assert(Math.abs(y[1]-(10-P.g/2))<1e-9);assert(Math.abs(y[3]+P.g)<1e-9);});
check('Fixed tilt gives expected horizontal and vertical acceleration',()=>{const th=.2,T=P.m*P.g/Math.cos(th);let y=[0,1,0,0,th,0,T/2,T/2];for(let i=0;i<100;i++)y=integrate(y,[T/2,T/2],.005);assert(Math.abs(y[2]-P.g*Math.tan(th)*.5)<1e-9);assert(Math.abs(y[1]-1)<1e-9);});
check('Motor step agrees with first-order exponential response',()=>{let y=[0,1,0,0,0,0,0,0];for(let i=0;i<20;i++)y=integrate(y,[.1,.1],.001);assert(Math.abs(y[6]-.1*(1-Math.exp(-.02/P.motorTau)))<1e-9);});
check('Differential thrust has expected angular acceleration',()=>{const y=[0,1,0,0,0,0,.15,.1],out=integrate(y,[.15,.1],.001);assert(Math.abs(out[5]-.001*P.lever*.05/P.I)<1e-9);});
const runs={};for(const scenario of ['hover','move','climb'])for(const ratio of [2.25,1.1]){const s=new Simulation({scenario,ratio}).run();runs[`${scenario}-${ratio}`]=s.metrics();check(`${scenario}, ratio ${ratio}: finite states and thrust bounds`,()=>{for(const h of s.history){assert(Object.values(h).filter(v=>typeof v==='number').every(Number.isFinite));assert(h.left>=-1e-10&&h.right>=-1e-10);assert(h.thrust<=ratio*P.m*P.g+1e-10);}});}
check('Move accelerates and then brakes',()=>{const s=new Simulation().run();const at=t=>s.history[Math.round(t/s.dt)];assert(at(5).vx>.45);assert(at(6.3).theta<0);assert(Math.abs(at(12).vx)<.01);assert(s.metrics().maxAltitudeError<.03);});
check('Reduced thrust causes saturation in climb',()=>{assert(runs['climb-1.1'].saturationFraction>.05);assert(runs['climb-1.1'].saturationFraction>runs['climb-2.25'].saturationFraction);});
const convergence=[];
for(const scenario of ['move','climb'])for(const ratio of [2.25,1.1]){
 const a=new Simulation({scenario,ratio,dt:.005}).run(),b=new Simulation({scenario,ratio,dt:.0025}).run(),c=new Simulation({scenario,ratio,dt:.00125}).run();
 let maxPositionDelta=0,maxSpeedDelta=0,maxAngleDelta=0;
 for(let i=0;i<a.history.length;i++){let u=a.history[i],v=c.history[i*4];maxPositionDelta=Math.max(maxPositionDelta,Math.hypot(u.x-v.x,u.z-v.z));maxSpeedDelta=Math.max(maxSpeedDelta,Math.hypot(u.vx-v.vx,u.vz-v.vz));maxAngleDelta=Math.max(maxAngleDelta,Math.abs(u.theta-v.theta));}
 const result={scenario,ratio,maxPositionDelta,maxSpeedDelta,maxAngleDelta,finalX:[a.y[0],b.y[0],c.y[0]]};convergence.push(result);
 check(`Timestep convergence ${scenario} ${ratio}`,()=>{assert(maxPositionDelta<.001);assert(maxSpeedDelta<.001);assert(maxAngleDelta<.001);});
}
const report={scope:'Planar numerical verification; no physical validation',parameters:P,checks,runs,convergence};
fs.writeFileSync(require('node:path').join(__dirname,'../step-02-verification.json'),JSON.stringify(report,null,2));
const s=new Simulation().run(),keys=Object.keys(s.history[0]);fs.writeFileSync(require('node:path').join(__dirname,'../step-02-move-brake.csv'),keys.join(',')+'\n'+s.history.map(r=>keys.map(k=>r[k]).join(',')).join('\n'));
console.log(JSON.stringify(report,null,2));
