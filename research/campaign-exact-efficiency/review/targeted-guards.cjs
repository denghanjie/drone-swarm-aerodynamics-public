'use strict';
// Focused review probes; independent broad all-pairs coverage is a separate file.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto'),assert=require('node:assert/strict');
const file=path.resolve(process.argv[2]),E=require(file);
const hash=()=>crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex');const before=hash();
const pose=(x,y,z,q=[0,0,0,1])=>[x,y,z,0,0,0,...q,0,0,0,...Array(4).fill(E.F.P.m*E.F.P.g/4)];
const cases=[];const add=(id,states,expectedDomain=false)=>cases.push({id,states,expectedDomain});
const d=.45/(3*E.W.parameters.spread)+E.W.parameters.origin*E.P.motorDistance;
for(const sign of [-1,1])for(const norm of [1-8e-11,1+8e-11]){
 const q=[0,0,Math.sin(Math.PI/8)*norm,Math.cos(Math.PI/8)*norm];
 add(`coordinate_limit_yaw45_sign${sign}_q${norm}`,[pose(0,sign*999999,1,q),pose(0,sign*999999+.5,1+d)]);
}
add('rotor_before_source_near_domain_tie',[pose(0,0,1),pose(-.16,.028,1.1),pose(.16,.028,1.1)],true);
add('near_domain_at_coordinate_limit',[pose(999999,999999,1),pose(999999.16,999999.028,1.1)],true);
add('cutoff_inside_at_coordinate_limit',[pose(999999,999999,1),pose(999999,999999,3.5-1e-9)]);
add('cutoff_equal_at_coordinate_limit',[pose(999999,999999,1),pose(999999,999999,3.5)]);
const outcome=f=>{try{return {ok:true,result:f()}}catch(e){return {ok:false,type:e.constructor.name,message:e.message,detail:e.detail}}};
const results=[];
for(const c of cases){const baseline=outcome(()=>E.A.fields(c.states,'sum-rotor')),methods={};assert.equal(baseline.ok,!c.expectedDomain);
 for(const variant of E.variants){const z=outcome(()=>E.fields(c.states,{variant}));assert.equal(z.ok,baseline.ok,c.id);if(z.ok){assert.deepEqual(z.result.winds,baseline.result.winds,c.id);assert.equal(z.result.maximumInflow,baseline.result.maximumInflow,c.id);}else {assert.deepEqual(z.detail,baseline.detail,c.id);assert.equal(z.type,baseline.type,c.id);}methods[variant]=z;}
 results.push({...c,baseline,methods,passed:true});
}
assert.equal(results.find(x=>x.id==='rotor_before_source_near_domain_tie').baseline.detail.source,2);
assert.equal(hash(),before);
console.log(JSON.stringify({sourceSHA256:before,sourceStable:true,scope:'Eight tiny numerical and guard-order probes; not timing or physical validation',passed:results.length,results},null,2));
