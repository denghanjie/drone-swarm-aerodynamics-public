'use strict';
// Independent, prescribed-state fixtures. They do not replace genuine Boids.
const path = require('node:path');
const SOURCE = require('../src/source.cjs').root;
const F = require(path.join(SOURCE,'outputs/step02c-source/physics.cjs'));
const C = {sourceCommit:'c591ce2b195fa01b895d4ba881a44a4b92fdd703', seed:628731, weight:F.P.m*F.P.g,
  axialCutoff:2.5, axialFade:2, radialCutoff:3, radialFade:2,
  motorDistance:2*Math.SQRT2*F.P.a, spread:.07668, origin:-5.817, decay:10.11,
  minDownstream:2.5, maxTilt:20, nearFieldRadius:.15, rotorRadius:.023, rho:1.225};
const quat=(roll=0,pitch=0,yaw=0)=>F.qmul(F.qmul([0,0,Math.sin(yaw*Math.PI/360),Math.cos(yaw*Math.PI/360)],
  [0,Math.sin(pitch*Math.PI/360),0,Math.cos(pitch*Math.PI/360)]),[Math.sin(roll*Math.PI/360),0,0,Math.cos(roll*Math.PI/360)]);
const state=(p=[0,0,1],q=quat())=>[...p,0,0,0,...q,0,0,0,...Array(4).fill(C.weight/4)];
const half=down=>C.spread*(down-C.origin*C.motorDistance);
const rng=seed=>()=>((seed=(1664525*seed+1013904223)>>>0)/4294967296);
function lattice(n,spacing,seed=C.seed,tilt=0){
  const random=rng(seed),side=Math.ceil(Math.cbrt(n));
  return Array.from({length:n},(_,i)=>state([(i%side)*spacing+(.5-random())*spacing*.025,
    (Math.floor(i/side)%side)*spacing+(.5-random())*spacing*.025,
    1+Math.floor(i/(side*side))*spacing+(.5-random())*spacing*.025],quat(0,tilt*(random()*2-1),random()*360)));
}
function fixtures(){
  const out=[];const add=(id,states,tags=[],extra={})=>out.push({id,states,tags,...extra});
  add('empty',[],['zero']); add('isolated',[state()],['zero']);
  add('equal_height_square',[-1,1].flatMap(x=>[-1,1].map(y=>state([x,y,1]))),['zero','symmetric']);
  for(const d of [.2,.4,.75,1.5,2,2.5-1e-9,2.5,2.5+1e-9])add(`vertical_${d}`,[state([0,0,1]),state([0,0,1+d])],['vertical','axial-boundary']);
  for(const r of [2,3])for(const eps of [-1e-9,0,1e-9]){
    const d=1.3,x=r*half(d)+F.P.a+eps;
    add(`radial_${r}_${eps}`,[state([0,0,1]),state([x,F.P.a,1+d])],['asymmetric','radial-boundary']);
  }
  for(const deg of [0,10,19.999,20,20.001])for(const sign of [-1,1]){
    const q=quat(0,sign*deg,37),axis=F.rotate(q,[0,0,1]);
    add(`tilt_${sign*deg}`,[state([0,0,1],quat(0,-sign*Math.min(deg,19),-13)),
      state([axis[0],axis[1],1+axis[2]],q)],['tilted'],{expectedDomainFailure:deg>20});
  }
  for(const n of [8,24,64]){
    const d=1.75,r=2.7*half(d);
    add(`many_weak_${n}`,[state(),...Array.from({length:n},(_,i)=>{
      const a=2*Math.PI*i/n;return state([r*Math.cos(a),r*Math.sin(a),1+d]);})],
      ['many-weak','same-height-emitters',...(n>=24?['deliberately-overlapping-software-stress']:[])]);
  }
  add('near_domain',[state(),state([.16,0,1.1])],['near-domain','aggressive-pruning-guard'],{expectedDomainFailure:true});
  add('near_domain_exact_plane',[state(),state([0,0,1])],['zero','coincident-model-stress']);
  for(const n of [8,27,64])for(const spacing of [.35,1,4])add(`lattice_N${n}_spacing${spacing}`,lattice(n,spacing),['density-by-N'],{seed:C.seed,spacing});
  // Same occupied cube size, increasing N: unlike the fixed-spacing cases above.
  for(const n of [8,27,64])add(`fixed_volume_N${n}`,lattice(n,2/(Math.ceil(Math.cbrt(n))-1)),['fixed-volume'],{seed:C.seed,extent:2});
  return out;
}
module.exports={C,F,SOURCE,quat,state,half,rng,lattice,fixtures};
