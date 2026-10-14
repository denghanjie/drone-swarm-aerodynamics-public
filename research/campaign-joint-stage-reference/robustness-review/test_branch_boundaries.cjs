'use strict';
/* Deferred synthetic boundary fixtures. No source trajectories evaluated. */
if(process.env.JOINT_REFERENCE_WINDOW_ACTIVE!=='1')throw Error('Coordinator-authorized numerical window required');
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),vm=require('node:vm'),crypto=require('node:crypto');
const filename=path.resolve(__dirname,'../implementation/src/branch-audit.cjs'),moduleObject={exports:{}};
const M={P:{radialCutoff:3,motorDistance:1,nearFieldRadius:.5},W:{parameters:{spread:.1,minDownstream:2,origin:0}},farStart:2};
vm.runInNewContext(fs.readFileSync(filename,'utf8'),{module:moduleObject,exports:moduleObject.exports,Buffer,require(id){if(id==='fs')return fs;if(id==='path')return path;if(id==='crypto')return crypto;if(id==='./exact-aero.cjs')return M;if(id==='./io.cjs')return {sha:b=>crypto.createHash('sha256').update(b).digest('hex')};throw Error('Unexpected dependency');}},{filename});
const {jumpRisk,BranchAudit,outerAtFar}=moduleObject.exports,tests=[];
function test(name,fn){try{fn();tests.push({name,passed:true});}catch(e){tests.push({name,passed:false,error:{name:e.name,message:e.message}});}}
function sample(down,radial,role='endpoint',tick=0,stage){return {pairs:[{down,radial,receiver:0,rotor:0,source:1}],states:[[down,radial]],raw:[[down,radial,99]],location:{role,tick,stage},signatureSha256:'0'.repeat(64)};}

test('near-radius equality belongs to possible valid-annulus jump risk',()=>{
 assert.equal(jumpRisk([sample(1.9,M.P.nearFieldRadius),sample(2.1,M.P.nearFieldRadius)]).length,1);
});
test('outer-support equality is excluded by half-open valid-annulus interval',()=>{
 assert.equal(jumpRisk([sample(1.9,outerAtFar),sample(2.1,outerAtFar)]).length,0);
});
test('farStart equality is conservatively included',()=>{
 assert.equal(jumpRisk([sample(2,.55),sample(2.1,.55)]).length,1);
});
test('below-near-radius and one-sided-downstream sampled ranges do not flag annulus',()=>{
 assert.equal(jumpRisk([sample(1.9,.49),sample(2.1,.49)]).length,0);
 assert.equal(jumpRisk([sample(2.1,.55),sample(2.2,.55)]).length,0);
});
test('equal-time RK trial straddle is distinct from endpoint bracket',()=>{
 const a=sample(2.1,.55,'endpoint',0),k2=sample(1.9,.55,'stage',4,2),k3=sample(2.2,.55,'stage',4,3),k4=sample(2.1,.55,'stage',8,4),b=sample(2.1,.55,'endpoint',8);
 const audit=new BranchAudit('synthetic',{persist:false});let caught;
 try{audit.checkStep([a,k2,k3,k4,b]);}catch(e){caught=e;}
 assert.ok(caught);assert.equal(caught.unresolvedJump,true);assert.equal(caught.detail.endpointBracketFlag,false);assert.equal(caught.detail.fullTrialFlag,true);
 assert.equal(caught.detail.samples[1].location.tick,caught.detail.samples[2].location.tick);
 assert.equal(caught.detail.samples[1].location.stage,2);assert.equal(caught.detail.samples[2].location.stage,3);
 assert.ok(caught.detail.samples.every(s=>s.raw));assert.match(caught.detail.meaning,/possible crossing|no event localization/i);
});
test('endpoint-only evidence never claims an RK trial flag',()=>{
 const audit=new BranchAudit('synthetic-endpoints',{persist:false});let caught;
 try{audit.checkStep([sample(1.9,.55,'endpoint',0),sample(2.1,.55,'endpoint',8)]);}catch(e){caught=e;}
 assert.ok(caught);assert.equal(caught.detail.endpointBracketFlag,true);assert.equal(caught.detail.fullTrialFlag,false);
});
const report={schema:'independent-branch-boundary-fixtures/v1',kind:'synthetic geometry ranges, no genuine Boids trajectory',tests,passed:tests.every(t=>t.passed)};process.stdout.write(JSON.stringify(report)+'\n');if(!report.passed)process.exitCode=1;
