'use strict';
const fs=require('fs'),path=require('path'),crypto=require('crypto'),assert=require('assert/strict');
const root=path.resolve(__dirname,'../../..'),out=path.resolve(__dirname,'../results'),evidence=path.resolve(process.argv[2]||root);
const artifact=path.join(out,'order-probe.json');if(fs.existsSync(artifact))throw Error('Refuse to replace an existing order-probe result');
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
const result={scope:'Preregistered development diagnostic on previously exposed states. No trajectories. Separate social accumulation and pair-constraint iteration; no claim that natural runtime order changed.',runtime:process.version,inputHashes:[],cases:[]};
function hashed(rel){const p=path.join(evidence,rel),raw=fs.readFileSync(p);result.inputHashes.push({path:rel,sha256:sha(raw)});return JSON.parse(raw);}
for(const [seed,course] of [[2001,'wide'],[2002,'narrow']]){
 process.env.FLOCK_FACTORY_VARIANT=course;
 for(const p of ['outputs/milestone-31-source/sim.cjs','outputs/milestone-31-source/factory.cjs','research/m31-diagnosis-2026-10-15/source/controller.cjs']){const key=require.resolve(path.join(root,p));delete require.cache[key];}
 const S=require(path.join(root,'outputs/milestone-31-source/sim.cjs')),{steer}=require('./controller.cjs'),{Grid}=require(path.join(root,'outputs/milestone-31-source/grid.cjs'));
 const rel=`outputs/milestone-31-source/checkpoint-heldout-${seed}-1000-${course}-wall-priority-0.0025-20.json`,cp=hashed(rel),states=cp.states,before=sha(JSON.stringify(states)),grid=new Grid(states,S.P.neighbor),rows=[];
 for(let i=0;i<states.length;i++){
  const ids=grid.neighbors(i,S.P.neighbor);let original,natural,pairs,social;
  const frozen=S.steer(i,states,ids,'boids','wall-priority',d=>original=d);
  const adapted=steer(i,states,ids,'boids','wall-priority',d=>natural=d);
  assert.deepEqual(adapted,frozen);for(const key of Object.keys(original))assert.deepEqual(natural[key],original[key]);
  steer(i,states,ids,'boids','wall-priority',d=>pairs=d,{reversePairs:true});
  steer(i,states,ids,'boids','wall-priority',d=>social=d,{reverseSocial:true});
  const compact=d=>({velocity:d.velocity,preferred:d.preferred,beforeWall:d.beforeWall,wallResidual:d.wallResidual,pairResidual:d.pairResidual,iterations:d.iterations,converged:d.converged,pairIDs:d.pairs.map(p=>p.neighbor)});
  rows.push({i,position:states[i].slice(0,3),neighborIDs:ids,natural:compact(natural),reversePairs:compact(pairs),reverseSocial:compact(social),pairDifference:Math.hypot(...pairs.velocity.map((x,k)=>x-natural.velocity[k])),socialDifference:Math.hypot(...social.velocity.map((x,k)=>x-natural.velocity[k]))});
 }
 assert.equal(before,sha(JSON.stringify(states)));
 function summary(key){const a=rows.map(x=>x[key]).sort((a,b)=>a-b);return {maximum:a.at(-1),median:(a[499]+a[500])/2,p95:a[949],countAbove001:a.filter(x=>x>.01).length,worstDrone:rows.reduce((a,b)=>a[key]>=b[key]?a:b).i};}
 result.cases.push({seed,course,t:cp.t,count:states.length,naturalExactlyMatchesFrozen:true,inputStateUnmodified:true,pairSummary:summary('pairDifference'),socialSummary:summary('socialDifference'),rows});
}
fs.mkdirSync(out,{recursive:true});fs.writeFileSync(artifact,JSON.stringify(result,null,2)+'\n',{flag:'wx'});
console.log(JSON.stringify(result.cases.map(({rows,...c})=>c)));
