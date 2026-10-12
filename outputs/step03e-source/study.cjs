// Run: node outputs/step03e-source/study.cjs
const fs=require('fs'),path=require('path'),D=require('./pair.cjs');
const out=path.join(__dirname,'..');
const original={kp:1,kv:2.5,ka:100,kw:20};
// Frozen design: one training geometry; 27 candidates; no held-out tuning.
const training={gap:.45,offset:.06,ratio:2.25};
const grid=[];for(const kp of [.5,1,2])for(const kv of [1,2.5,4])for(const kw of [20,30,40])grid.push({kp,kv,ka:100,kw});
function metrics(s,end=s.t){const h=s.history.filter(p=>p.t<=end+1e-9),rms=f=>Math.sqrt(h.reduce((a,p)=>a+f(p)**2,0)/h.length);const m={end,ownEnd:s.t,stopped:s.stopped,horizontalRMS:rms(p=>Math.hypot(p.x,p.y)),altitudeRMS:rms(p=>p.z-1),speedRMS:rms(p=>Math.hypot(p.vx,p.vy,p.vz)),tiltRMS:rms(p=>Math.acos(Math.min(1,1-2*(p.qx*p.qx+p.qy*p.qy)))*180/Math.PI),peakHorizontal:Math.max(...h.map(p=>Math.hypot(p.x,p.y))),peakPitch:Math.max(...h.map(p=>Math.abs(p.pitch)))*180/Math.PI};m.score=m.horizontalRMS/.1+m.altitudeRMS/.2+m.speedRMS/.5+m.tiltRMS/10;return m;}
const trials=grid.map(gains=>({gains,...metrics(new D.Simulation({...training,gains}).run())}));
const eligible=trials.filter(t=>!t.stopped&&t.end===16).sort((a,b)=>a.score-b.score);if(!eligible.length)throw Error('No completed candidate');const chosen=eligible[0].gains;
const heldout=[{gap:.25,offset:.04,ratio:2.25},{gap:.45,offset:.12,ratio:2.25},{gap:.8,offset:.06,ratio:2.25},{gap:.8,offset:.2,ratio:2.25},{gap:.45,offset:0,ratio:2.25},{gap:.45,offset:.06,ratio:1.1}];
const tests=[training,...heldout].map((config,i)=>{const runs=[];for(const [name,gains] of [['original',original],['chosen',chosen]])for(const model of ['rotor','force-only'])runs.push({name,model,s:new D.Simulation({...config,gains,model}).run()});const end=Math.min(...runs.map(r=>r.s.t));return {split:i?'held-out':'training',config,end,runs:runs.map(r=>({name:r.name,model:r.model,...metrics(r.s,end)}))};});
fs.writeFileSync(path.join(out,'step-03e-study.json'),JSON.stringify({design:{training,grid,heldout,score:'horizontalRMS/0.1 + altitudeRMS/0.2 + speedRMS/0.5 + tiltRMS/10deg; only complete 16s candidates eligible',selection:'lowest training score; held-out cases never used for selection'},original,chosen,trials,tests},null,2));
console.log(JSON.stringify({chosen,training:tests[0],heldout:tests.slice(1)},null,2));
