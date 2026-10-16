'use strict';
const Base=require('../../m31-force-ablation-2026-10-16/source/adapter.cjs');
const F=require('../../../outputs/step02c-source/physics.cjs');
const mg=F.P.m*F.P.g,R=Math.SQRT2*F.P.a;
function full(states,commands,guard,config){
 const e=Base.evaluate(states,commands,'coupled',guard,config);
 e.info={...e.info,evaluation:'instantaneous',cacheIndex:null,cacheTime:null,cacheAge:null};
 return e;
}
function makeCache(e,index,t){
 return Object.freeze({index,t,ratios:Object.freeze(e.witness.rotors.map(row=>Object.freeze(row.map(r=>r.x))))});
}
function cached(states,commands,cache,t,guard,config){
 guard();
 if(!cache||!Number.isInteger(cache.index)||cache.index<0||!Number.isFinite(cache.t)||!Number.isFinite(t)||!Array.isArray(cache.ratios)||cache.ratios.length!==states.length)throw Error('missing cache');
 const age=t-cache.t;
 if(age < -1e-12 || age>config.refreshDt+1e-12)throw Error('cache age outside interval');
 if(!states.every(s=>s.length===17&&s.every(Number.isFinite)&&Math.abs(Math.hypot(...s.slice(6,10))-1)<=1e-10&&s.slice(13,17).every(x=>x>0)&&Number.isFinite(s.slice(13,17).reduce((a,b)=>a+b,0)))||commands.length!==states.length||!commands.every(u=>u.length===4&&u.every(Number.isFinite)))throw Error('cached stage input rejected');
 if(!cache.ratios.every(row=>row.length===4&&row.every(x=>Number.isFinite(x)&&x>0&&x<=1)))throw Error('invalid ratio cache');
 const forces=states.map((s,i)=>cache.ratios[i].map((x,r)=>s[13+r]*x));
 const corrections=states.map((s,i)=>Base.correction(s,forces[i]));
 const derivatives=states.map((s,i)=>{const d=F.derivative(s,commands[i]);for(let k=0;k<3;k++){d[3+k]+=corrections[i].force[k]/F.P.m;d[10+k]+=corrections[i].torque[k]/F.P.I[k];}return d;});
 if(!forces.flat().every(Number.isFinite)||!derivatives.flat().every(Number.isFinite))throw Error('nonfinite cached derivative');
 const info={evaluation:'cached-ratio',cacheIndex:cache.index,cacheTime:cache.t,cacheAge:age,edges:null,positiveTerms:null,residual:null,sourceReceiverMismatch:null,symbolCounts:null,admitted:null,descendingEligible:null,minRatio:Math.min(...cache.ratios.flat()),maxTiltDegrees:Math.max(...states.map(s=>Math.acos(Math.max(-1,Math.min(1,F.rotate(s.slice(6,10),[0,0,1])[2])))*180/Math.PI)),modeledTorqueMax:Math.max(...corrections.map(c=>Math.hypot(...c.torque))),appliedTorqueMax:Math.max(...corrections.map(c=>Math.hypot(...c.torque)))};
 return {forces,modeledCorrections:corrections,corrections,derivatives,info,witness:null};
}
function step(states,commands,mode,cache,h,t,guard,config,recordStage,capture=false){
 const stage=(raw,s,at)=>{let z=null,evaluationAttempted=false;try{z=Base.project(raw);evaluationAttempted=true;const e=mode==='coupled'?full(z,commands,guard,config):cached(z,commands,cache,at,guard,config);recordStage({t:at,stage:s,status:'completed',evaluationAttempted,rawQuaternionNormMaxError:Math.max(...raw.map(x=>Math.abs(Math.hypot(...x.slice(6,10))-1))),...e.info,...(capture?{witness:{states:z,derivatives:e.derivatives,forces:e.forces,modeledCorrections:e.modeledCorrections,corrections:e.corrections,commands}}:{})});return e.derivatives;}catch(e){recordStage({t:at,stage:s,status:'rejected',evaluationAttempted,reason:e.message});e.stage={t:at,stage:s,states:z??raw,commands,cacheIndex:cache?.index??null,detail:e.detail??null};throw e;}};
 if(!['coupled','reuse10ms'].includes(mode))throw Error('unknown propagation mode');
 const add=(k,a)=>states.map((s,i)=>s.map((v,j)=>v+a*k[i][j]));
 const k1=stage(states,1,t),k2=stage(add(k1,h/2),2,t+h/2),k3=stage(add(k2,h/2),3,t+h/2),k4=stage(add(k3,h),4,t+h);
 const rawFinal=states.map((s,i)=>s.map((v,j)=>v+h*(k1[i][j]+2*k2[i][j]+2*k3[i][j]+k4[i][j])/6));
 try{return Base.project(rawFinal);}catch(e){e.stage={t:t+h,stage:'final-projection',states:rawFinal,acceptedStart:states,commands,cacheIndex:cache?.index??null};throw e;}
}
function loadError(a,b){if(!a||!b)return null;let rotor=0,force=0,moment=0;for(let i=0;i<a.forces.length;i++){for(let r=0;r<4;r++)rotor=Math.max(rotor,Math.abs(a.forces[i][r]-b.forces[i][r])/Base.nominalHover);force=Math.max(force,Math.hypot(...a.corrections[i].force.map((x,k)=>x-b.corrections[i].force[k]))/mg);moment=Math.max(moment,Math.hypot(...a.corrections[i].torque.map((x,k)=>x-b.corrections[i].torque[k]))/(mg*R));}return {rotor,force,moment};}
module.exports={...Base,full,cached,makeCache,step,loadError,mg,R};
