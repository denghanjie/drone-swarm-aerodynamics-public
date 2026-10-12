const D=require('./pair.cjs'),fs=require('fs'),path=require('path'),out=path.join(__dirname,'..');
const gains={kp:1,kv:2.5,ka:100,kw:20},results=[];
// Fixed exploratory grid. Two held sources, one responding receiver. No learned aggregate model or empirical fit.
for(const initialX of [0,.001])for(const gap of [.25,.45,.8])for(const spacing of [.12,.24,.4])for(const offset of [0,.06]){
 const run=c=>{const s=new D.Simulation(c);s.y[0]=initialX;s.c=s.command();s.history=[s.sample()];return s.run();};
 const sources=[[offset-spacing/2,0,1+gap],[offset+spacing/2,0,1+gap]],config={gap,offset,sources,gains},a=run({...config,aggregation:'airflow'}),b=run({...config,aggregation:'deficits'}),end=Math.min(a.t,b.t),row={initialX,gap,spacing,offset,sources,end};
 for(const [label,run] of [['airflow',a],['deficits',b]]){const h=run.history.filter(p=>p.t<=end+1e-9),rms=f=>Math.sqrt(h.reduce((s,p)=>s+f(p)**2,0)/h.length);row[label]={ownEnd:run.t,stop:run.stopped,initialThrustWeight:h[0].thrust/(D.P.m*D.P.g),horizontalRMS:rms(p=>Math.hypot(p.x,p.y)),altitudeRMS:rms(p=>p.z-1),finalAltitude:h.at(-1).z};}
 results.push(row);
}
fs.writeFileSync(path.join(out,'milestone-01-group-study.json'),JSON.stringify(results,null,2));
console.log(JSON.stringify(results.filter(r=>r.gap===.45&&r.offset===.06),null,2));
