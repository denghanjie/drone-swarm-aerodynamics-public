'use strict';
/* INDEPENDENT DEFERRED FIXTURES. Do not execute before coordinator freeze.
 * A frozen supervisor must set JOINT_REFERENCE_WINDOW_ACTIVE=1 and charge this
 * process, all writes and its retained report to the same campaign window.
 * node --check is allowed before that window; it does not execute this file.
 */
if (process.env.JOINT_REFERENCE_WINDOW_ACTIVE !== '1') {
  throw new Error('Numerical fixtures require the coordinator-authorized shared campaign window');
}
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const crypto = require('node:crypto');
const root = path.resolve(__dirname, '../implementation');
const results = [];
function test(name, fn) {
  try { fn(); results.push({name, passed:true}); }
  catch (error) { results.push({name, passed:false, error:{name:error.name,message:error.message,stack:error.stack}}); }
}
function loadJoint(model) {
  const filename=path.join(root,'src/joint-step.cjs'), module={exports:{}};
  const context={module,exports:module.exports,require(id){assert.equal(id,'./exact-aero.cjs');return model;},console,Buffer};
  vm.runInNewContext(fs.readFileSync(filename,'utf8'),context,{filename});
  return module.exports;
}
const copy = x => JSON.parse(JSON.stringify(x));
const sha = x => crypto.createHash('sha256').update(x).digest('hex');
function state(x=0, qw=1) { const s=Array(17).fill(0);s[0]=x;s[2]=2;s[9]=qw;return s; }
function near(actual,expected,tol=1e-13) {assert.ok(Math.abs(actual-expected)<=tol,`${actual} != ${expected}`);}
function same(actual,expected) {assert.equal(JSON.stringify(actual),JSON.stringify(expected));}
function frozenRows(rows) {for(const row of rows)Object.freeze(row);return Object.freeze(rows);}
const J=loadJoint({});

test('full-swarm coupled RK4 stages use one simultaneous state',()=>{
  const y=frozenRows([[1],[2]]), seen=[];
  const out=J.synchronizedRK4(y,.2,(s,stage,fraction)=>{
    seen.push({state:copy(s),stage,fraction});return [[s[1][0]],[s[0][0]]];
  });
  same(seen.map(x=>[x.stage,x.fraction]),[[1,0],[2,.5],[3,.5],[4,1]]);
  [[1,2],[1.2,2.1],[1.21,2.12],[1.424,2.242]].forEach((row,i)=>row.forEach((v,j)=>near(seen[i].state[j][0],v)));
  near(out[0][0],1+.2*(2+2*2.1+2*2.12+2.242)/6);
  near(out[1][0],2+.2*(1+2*1.2+2*1.21+1.424)/6);
  same(y,[[1],[2]]);
});

test('geometry normalization is a disjoint copy and preserves all nonquaternion entries',()=>{
  const original=frozenRows([state(3,2),state(9,.5)]), before=copy(original), g=J.geometryCopy(original);
  assert.notEqual(g,original);
  g.forEach((s,i)=>{assert.notEqual(s,original[i]);near(Math.hypot(...s.slice(6,10)),1);for(let k=0;k<17;k++)if(k<6||k>9)assert.equal(s[k],original[i][k]);});
  g[0][0]=99;same(original,before);
});

test('geometry guards reject zero and nonfinite quaternions or other invalid entries',()=>{
  for(const bad of [state(0,0),state(0,Infinity),state(0,NaN),state(Infinity,1),state().slice(0,16)]){
    assert.throws(()=>J.geometryCopy([bad]));
  }
});

test('endpoint normalization copies raw endpoint and normalizes each drone',()=>{
  const raw=frozenRows([state(1,2),state(4,.25)]), out=J.endpointNormalize(raw);
  assert.notEqual(out,raw);out.forEach((s,i)=>{assert.notEqual(s,raw[i]);assert.equal(s[9],1);assert.equal(s[0],raw[i][0]);});
  assert.equal(raw[0][9],2);assert.equal(raw[1][9],.25);
});

test('joint step computes complete field before derivatives and passes raw stage state',()=>{
  const log=[], command=frozenRows([[11,12,13,14],[21,22,23,24]]), initial=frozenRows([state(1,2),state(2,.5)]), before=copy(initial);
  const model={A:{derivative(raw,c,wind,mode){
    log.push(['derivative',raw[0],raw[9],c[0],wind[0],mode]);
    const d=Array(17).fill(0);d[0]=wind[0];return d;
  }}};
  const K=loadJoint(model);
  let fieldCalls=0;
  const out=K.jointStep(initial,command,.2,{field(geometry){
    fieldCalls++;log.push(['field',...geometry.map(s=>s[0])]);
    geometry.forEach(s=>near(Math.hypot(...s.slice(6,10)),1));
    return {winds:[[geometry[1][0],0,0,0],[geometry[0][0],0,0,0]]};
  }});
  assert.equal(fieldCalls,4);assert.equal(log.length,12);
  for(let k=0;k<4;k++){
    assert.equal(log[3*k][0],'field');assert.equal(log[3*k+1][0],'derivative');assert.equal(log[3*k+2][0],'derivative');
    assert.equal(log[3*k+1][2],2);assert.equal(log[3*k+2][2],.5);
    assert.equal(log[3*k+1][3],11);assert.equal(log[3*k+2][3],21);
    assert.equal(log[3*k+1][5],'sum-rotor');assert.equal(log[3*k+2][5],'sum-rotor');
  }
  out.forEach(s=>near(s[9],1));same(initial,before);
});

test('each failing RK stage retains exact raw geometry commands and original guard',()=>{
  for(let failAt=1;failAt<=4;failAt++){
    const model={A:{derivative(raw){const d=Array(17).fill(0);d[0]=1;return d;}}}, K=loadJoint(model);
    const initial=frozenRows([state(1,2),state(4,.5)]), commands=frozenRows([[1,2,3,4],[5,6,7,8]]);
    let stage=0,caught;
    const guard=Object.assign(new Error('injected exact guard'),{detail:{receiver:1,rotor:2,source:0}});
    try {K.jointStep(initial,commands,.2,{field(geometry){if(++stage===failAt)throw guard;return {winds:geometry.map(()=>[0,0,0,0])};}});}
    catch(e){caught=e;}
    assert.equal(caught,guard);assert.equal(caught.stageEvidence.stage,failAt);assert.equal(caught.stageEvidence.commands,commands);
    assert.equal(caught.stageEvidence.field,null);same(caught.stageEvidence.guard.detail,{receiver:1,rotor:2,source:0});
    const raw=caught.stageEvidence.raw, geometry=caught.stageEvidence.geometry;
    assert.equal(raw[0][9],2);assert.equal(geometry[0][9],1);assert.notEqual(raw[0],geometry[0]);
    near(raw[0][0],1+[0,.1,.1,.2][failAt-1]);
  }
});

test('geometry rejection retains raw input even before geometry exists',()=>{
  const raw=[state(0,0)], commands=[[1,2,3,4]], K=loadJoint({A:{derivative(){throw Error('unreachable');}}});
  let caught;try{K.jointStep(raw,commands,.1,{field(){throw Error('unreachable');}});}catch(e){caught=e;}
  assert.ok(caught);assert.equal(caught.stageEvidence.raw,raw);assert.equal(caught.stageEvidence.geometry,null);assert.equal(caught.stageEvidence.commands,commands);assert.equal(caught.stageEvidence.stage,1);
});

test('nonfinite derivative is rejected and retains available field and derivative',()=>{
  const K=loadJoint({A:{derivative(){const d=Array(17).fill(0);d[0]=NaN;return d;}}}), winds=[[.5,0,0,0]];
  let caught;try{K.jointStep([state()],[[1,2,3,4]],.1,{field(){return {winds};}});}catch(e){caught=e;}
  assert.ok(caught);assert.equal(caught.stageEvidence.field,winds);assert.ok(Number.isNaN(caught.stageEvidence.derivatives[0][0]));
});

test('failed endpoint projection retains the actual combined endpoint rather than k4',()=>{
  let call=0;const derivatives=[1,-4,1,-1];
  const K=loadJoint({A:{derivative(){const d=Array(17).fill(0);d[9]=derivatives[call++];return d;}}});
  const commands=[[1,2,3,4]];let caught;
  try{K.jointStep([state()],commands,1,{field(){return {winds:[[0,0,0,0]]};}});}catch(e){caught=e;}
  assert.equal(call,4);assert.ok(caught);assert.ok(caught.endpointEvidence);
  assert.equal(caught.endpointEvidence.rawCombinedEndpoint[0][9],0);assert.equal(caught.endpointEvidence.commands,commands);
  assert.ok(caught.endpointEvidence.guard);assert.equal(caught.stageEvidence,undefined);
});

/* This tests exact clock arithmetic independently of physical trajectories.
 * Campaign scheduler integration must additionally be checked in its own API.
 */
test('prescribed steps and their stage clocks are integer and event-aligned',()=>{
  const T=51200,control=512,common=32;
  for(const step of [32,16,8,4,2]){
    assert.equal(T%step,0);assert.equal(control%step,0);assert.equal(common%step,0);
    const controlTicks=[],refreshTicks=[];
    for(let tick=0;tick<T;tick+=step){
      for(const f of [0,.5,.5,1])assert.ok(Number.isInteger(tick+f*step));
      if(tick%control===0)controlTicks.push(tick);
      if(tick%step===0)refreshTicks.push(tick);
    }
    assert.equal(controlTicks.length,100);assert.equal(controlTicks.at(-1),50688);assert.ok(!controlTicks.includes(T));assert.ok(!refreshTicks.includes(T));
  }
});

/* Retained only as one small machine-readable fixture record. This stream is
 * captured by the supervisor. It must not be represented as a Boids run.
 */
const report={schema:'independent-joint-robustness-fixtures/v1',kind:'tiny synthetic fixtures, no genuine Boids trajectory',sourceSha256:sha(fs.readFileSync(path.join(root,'src/joint-step.cjs'))),tests:results,passed:results.every(x=>x.passed)};
process.stdout.write(JSON.stringify(report)+'\n');
if(!report.passed)process.exitCode=1;
