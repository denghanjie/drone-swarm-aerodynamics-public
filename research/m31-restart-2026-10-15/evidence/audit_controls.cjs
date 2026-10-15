'use strict';
// Read-only local calculations. Usage: node audit_controls.cjs PUBLIC_REPOSITORY.
// Writes audit-controls.json beside this script. Does not run S.run or original audits.
const fs=require('fs'),path=require('path'),crypto=require('crypto');
if(process.argv.length!==3){console.error('Usage: node audit_controls.cjs PUBLIC_REPOSITORY');process.exit(2);}
const repo=path.resolve(process.argv[2]);
if(!fs.existsSync(path.join(repo,'outputs/milestone-31-protocol.json'))){console.error('PUBLIC_REPOSITORY must contain outputs/milestone-31-protocol.json');process.exit(2);}
const dir=path.join(repo,'outputs/milestone-31-source');
const read=p=>JSON.parse(fs.readFileSync(p));
const F=require(path.join(repo,'outputs/step02c-source/physics.cjs'));
const G=require(path.join(dir,'geometry.cjs'));
const protocol=read(path.join(repo,'outputs/milestone-31-protocol.json'));
const output={method:{command:'node audit_controls.cjs PUBLIC_REPOSITORY',
 contact:'Replay only the affected independent rigid body from its recorded preceding-control state, with its frozen command, for two primary steps; check all boxes from the trial-specific saved geometry.',
 order:'Re-evaluate one preserved 20 s full-state checkpoint per 1000-drone geometry. Reverse neighbor IDs while holding every state, route, geometry, gain, and filter fixed; compare requested velocities. This reverses both floating-point social summation order and sequential pair projection order, so it does not isolate them. This is a post-hoc controller sensitivity probe, not a mission or an accepted variant.',
 scope:'Per invocation: six RK4 integration steps; no full swarm simulation. Reusing frozen functions tests consistency and local sensitivity, not independent physical correctness.',
 runtime:process.version,
 exactOrderOperation:'For every drone i=0..999, forward IDs are Grid.neighbors(i, 1.8), sorted ascending by frozen Grid.candidates; reverse IDs are ids.slice().reverse(). Both full ID lists and per-drone output residuals are retained.',
 inferenceLimit:'Neighbor reversal is a new exploratory same-state calculation. It is not preregistered confirmation, not improved accuracy, and not an identified cause of the saved timestep divergence.'},inputHashes:[],contacts:[],neighborOrderProbes:[]};
function recordHash(p){const rel=path.relative(repo,p);if(!output.inputHashes.some(x=>x.path===rel))output.inputHashes.push({path:rel,sha256:crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex')});}
for(const name of ['sim.cjs','grid.cjs','geometry.cjs','factory.cjs','factory-wide.cjs','wall-filter.cjs'])recordHash(path.join(dir,name));
recordHash(path.join(repo,'outputs/step02c-source/physics.cjs'));
for(const j of protocol.jobs){
 const r=read(path.join(dir,j.id+'.json'));if(!r.metrics.failure)continue;
 recordHash(path.join(dir,j.id+'.json'));recordHash(path.join(dir,'factory-'+j.course+'.json'));
 const a=r.lastControl.affected[0],v=a.velocity,rs=a.state;
 const c=F.control(rs,{vx:v[0],vy:v[1],z:rs[2]+(2.5*v[2]+1.5*rs[5])/6,yaw:Math.atan2(v[1],v[0])},2.25);
 const geom=read(path.join(dir,'factory-'+j.course+'.json'));
 let state=rs.slice();const steps=Math.round((r.metrics.end-r.lastControl.t)/j.dt),segments=[];
 for(let k=0;k<steps;k++){
  const before=state;state=F.integrate(state,c.u,j.dt);
  const hits=geom.boxes.map(b=>({id:b.id,clearance:G.segmentBoxDistance(before.slice(0,3),state.slice(0,3),b)-.075})).filter(b=>b.clearance<0);
  segments.push({step:k+1,endTime:r.lastControl.t+(k+1)*j.dt,hits});
 }
 const walls=a.walls.map(w=>{const n=w.n.slice(0,3),dot=x=>x.slice(0,3).reduce((z,v,k)=>z+v*n[k],0);return {obstacle:w.obstacle,requiredOutwardVelocity:w.lower,requestedOutwardVelocity:dot(a.velocity),actualOutwardVelocity:dot(rs.slice(3,6)),commandDeficit:Math.max(0,w.lower-dot(a.velocity)),adverseTrackingDifference:dot(a.velocity)-dot(rs.slice(3,6))};});
 output.contacts.push({trial:j.id,controlExactlyReproduced:JSON.stringify(c)===JSON.stringify(a.actuator),
  finalStateExactlyReproduced:JSON.stringify(state)===JSON.stringify(r.final[a.drone]),
  contactIdentityAndClearanceExactlyReproduced:JSON.stringify(segments.at(-1).hits)===JSON.stringify(r.metrics.failure.hits),
  steps,segments,walls,motorTargetMinusLaggedThrustNorm_N:Math.hypot(...c.u.map((u,i)=>u-rs[13+i]))});
}
for(const [seed,variant] of [[2001,'wide'],[2002,'narrow']]){
 process.env.FLOCK_FACTORY_VARIANT=variant;
 for(const name of ['sim.cjs','factory.cjs'])delete require.cache[require.resolve(path.join(dir,name))];
 const S=require(path.join(dir,'sim.cjs')),{Grid}=require(path.join(dir,'grid.cjs'));
 const checkpoint='checkpoint-heldout-'+seed+'-1000-'+variant+'-wall-priority-0.0025-20.json';
 recordHash(path.join(dir,checkpoint));
 const cp=read(path.join(dir,checkpoint)),states=cp.states,grid=new Grid(states,S.P.neighbor);
 for(const filter of ['baseline','wall-priority']){
  let differences=[],details=[];
  for(let i=0;i<states.length;i++){
   const ids=grid.neighbors(i,S.P.neighbor);let a,b;
   S.steer(i,states,ids,'boids',filter,d=>a=d);
   S.steer(i,states,ids.slice().reverse(),'boids',filter,d=>b=d);
   const d=Math.hypot(...a.velocity.map((v,k)=>v-b.velocity[k]));differences.push(d);
   details.push({drone:i,forwardNeighborIDs:ids,reverseNeighborIDs:ids.slice().reverse(),difference_mps:d,forward:a.velocity,reversed:b.velocity,forwardWallResidual:a.wallResidual,reversedWallResidual:b.wallResidual,forwardPairResidual:a.pairResidual,reversedPairResidual:b.pairResidual});
  }
  differences.sort((a,b)=>a-b);details.sort((a,b)=>b.difference_mps-a.difference_mps);
  output.neighborOrderProbes.push({checkpoint,filter,count:states.length,time:cp.t,maximum_mps:differences.at(-1),
   median_mps:(differences[499]+differences[500])/2,p95_mps:differences[949],fractionAbove1cmPerSecond:differences.filter(x=>x>.01).length/differences.length,top5:details.slice(0,5),allDrones:details});
 }
}
fs.writeFileSync(path.join(__dirname,'audit-controls.json'),JSON.stringify(output,null,2)+'\n');
console.log(JSON.stringify({contacts:output.contacts,neighborOrderProbes:output.neighborOrderProbes.map(({top5,allDrones,...x})=>x)},null,2));
