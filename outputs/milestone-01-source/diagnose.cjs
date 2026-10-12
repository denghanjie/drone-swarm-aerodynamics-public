const fs=require('fs'),path=require('path'),D=require('./pair.cjs'),N=require('./numerics.cjs');
const out=path.join(__dirname,'..'),prior=JSON.parse(fs.readFileSync(path.join(out,'step-03e-study.json')));
// Fixed diagnostic design: both existing gains, actuator lags 10/20/40/80ms,
// moment scaling 0 to 1 in increments .025. Force loss remains unchanged.
const settings={gap:.45,offset:.06,ratio:2.25};const records=[];
for(const [name,gains] of [['original',prior.original],['selected',prior.chosen]])for(const motorTau of [.01,.02,.04,.08]){
 let last;
 for(let j=0;j<=40;j++){
 const momentScale=j/40,c={...settings,motorTau,momentScale},row={name,gains,...c};
 try{let x;try{x=N.root(c,gains,last);}catch{const y=new D.Simulation({...c,gains}).y;y[0]=.06;y[2]=.75;x=N.root(c,gains,N.pack(y));}last=x;const y=N.unpack(x),s=new D.Simulation({...c,gains});s.y=y;
 row.equilibrium=y;row.saturated=s.command().saturated;row.residual=Math.max(...D.pairDerivative(y,s.command().u,s).map(Math.abs));row.matrix=N.jac(z=>N.map(z,c,gains),x);
 }catch(e){row.failure=e.message;}
 records.push(row);
 }
}
fs.writeFileSync(path.join(out,'milestone-01-diagnostic-matrices.json'),JSON.stringify(records));
console.log('equilibria:',records.length,'failures:',records.filter(r=>r.failure).length);
// Long horizon checks on fixed settings; do not reinterpret short stable-looking runs as settling.
const flights=[];
for(const [name,gains] of [['original',prior.original],['selected',prior.chosen]])for(const motorTau of [.01,.04,.08])for(const momentScale of [0,.25,.5,1]){
 const c={...settings,gains,motorTau,momentScale};const sim=new D.Simulation(c).run();const h=sim.history,rms=(a,f)=>Math.sqrt(a.reduce((sum,p)=>sum+f(p)**2,0)/a.length),tail=h.filter(p=>p.t>=12);
 flights.push({name,...c,end:sim.t,stop:sim.stopped,positionRMS:rms(h,p=>Math.hypot(p.x,p.y)),peakTilt:Math.max(...h.map(p=>Math.acos(Math.min(1,1-2*(p.qx*p.qx+p.qy*p.qy)))))*180/Math.PI,tailSpeed:tail.length?rms(tail,p=>Math.hypot(p.vx,p.vy,p.vz)):null});
}
fs.writeFileSync(path.join(out,'milestone-01-flights.json'),JSON.stringify(flights,null,2));
