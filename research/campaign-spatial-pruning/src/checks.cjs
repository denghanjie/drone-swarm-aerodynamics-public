'use strict';
const fs=require('fs'),assert=require('assert/strict'),path=require('path');
const M=require('./pruned-aero.cjs'),S=require('./scenarios.cjs');
const out=path.join(__dirname,'../results'),checks=[];
const norm=x=>Math.hypot(...x),difference=(a,b)=>a.map((x,i)=>x-b[i]);
function compare(states,epsilon){
  const original=M.A.fields(states,'sum-rotor'),full=M.fields(states),candidate=M.fields(states,{epsilon});
  let maxLegacy=0,maxInflow=0,maxForce=0,maxMoment=0;
  for(let i=0;i<states.length;i++){
    const truth=M.loads(states[i],full.winds[i]),approx=M.loads(states[i],candidate.winds[i]);
    const bounds=M.loadBounds(states[i],candidate.winds[i],candidate.omittedBounds[i]);
    for(let r=0;r<4;r++){
      maxLegacy=Math.max(maxLegacy,Math.abs(original.winds[i][r]-full.winds[i][r]));
      const error=full.winds[i][r]-candidate.winds[i][r];maxInflow=Math.max(maxInflow,error);
      assert(error>=-1e-12&&error<=candidate.omittedBounds[i]+1e-12,'inflow bound');
    }
    const ef=norm(difference(truth.force,approx.force)),em=norm(difference(truth.moment,approx.moment));
    assert(ef<=bounds.force+1e-12&&em<=bounds.moment+1e-13,'load bounds');
    assert(bounds.force<=bounds.lipschitzForce+1e-12,'response derivative bound');
    maxForce=Math.max(maxForce,ef);maxMoment=Math.max(maxMoment,em);
  }
  assert(maxLegacy<=1e-12,'reference equivalence');
  assert(maxForce<=.005*M.F.P.m*M.F.P.g,'force gate');
  assert(maxMoment<=.0075*M.F.P.m*M.F.P.g*M.F.P.a,'moment gate');
  return {maxLegacy,maxInflow,maxForce,maxMoment,omittedPairs:candidate.omittedPairs,exactZeroPairs:candidate.exactZeroPairs};
}
for(const fixture of S.fixtures()){
  checks.push({name:fixture.name,...compare(fixture.states,.04),pass:true});
}
for(const [name,states] of [
 ['near-domain',[S.pose(0,0,1),S.pose(0,0,1.1)]],
 ['tilt-domain',[S.pose(0,0,1),S.pose(0,0,2,21*Math.PI/180)]]
]){
  for(const epsilon of [0,.04,100]) assert.throws(()=>M.fields(states,{epsilon}),M.DomainError);
  assert.throws(()=>M.A.fields(states,'sum-rotor'),M.DomainError);
  checks.push({name,pass:true});
}
const invalid=S.pose(0,0,1);invalid[2]=NaN;
assert.throws(()=>M.fields([invalid]),M.InputError);checks.push({name:'nonfinite-hardened-input',pass:true,legacyEquivalenceClaim:false});
fs.mkdirSync(out,{recursive:true});fs.writeFileSync(path.join(out,'tiny-checks.json'),JSON.stringify({scope:'tiny deterministic correctness checks; no timing claims',checks},null,2));
console.log(JSON.stringify({passed:checks.length,checks},null,2));
module.exports={compare};
