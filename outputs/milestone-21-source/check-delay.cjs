const fs=require('fs'),assert=require('assert/strict'),S=require('./sim.cjs'),R=require('../milestone-19-source/sim.cjs');
const config={seed:1100,count:6,duration:2,dt:.0025,mode:'interior',scenario:'tight',record:false};
const a=S.run(config),b=R.run(config);assert.deepEqual(a.final,b.final);assert.deepEqual(a.samples,b.samples);assert.deepEqual(a.metrics,b.metrics);
const c=S.run({...config,observationDelay:.1});assert.notDeepEqual(c.final,a.final);assert(c.final.flat().every(Number.isFinite));assert.throws(()=>S.run({...config,observationDelay:.015}));
// At100ms delay the first ten steering snapshots are held at the initial state.
// Full small-run equality against an independently scheduled reference loop is checked below.
const F=require('../step02c-source/physics.cjs'),states0=R.initial(1100,6).map(s=>{s[0]-=6;return s;}),startCommands=states0.map((_,i)=>R.steer(i,states0,0,'interior','tight').velocity);let states=states0;
for(let n=0;n<40;n++){if(n%4===0)var u=states.map((s,i)=>{const v=startCommands[i];return F.control(s,{vx:v[0],vy:v[1],z:s[2]+(2.5*v[2]+1.5*s[5])/6,yaw:Math.atan2(v[1],v[0])},2.25).u});states=states.map((s,i)=>F.integrate(s,u[i],.0025));}
const d=S.run({...config,duration:.1,observationDelay:.1});assert.deepEqual(d.final,states);
fs.writeFileSync(require('path').join(__dirname,'../milestone-21-delay-checks.json'),JSON.stringify({checks:['Zero delay equals original full states, samples and metrics exactly for6 drones/2s','100ms delay changes a finite trajectory','Non-grid delay rejected','First100ms exactly matches independent fixed-observation integration'].map(name=>({name,passed:true}))},null,2));console.log('4 delay checks passed');
