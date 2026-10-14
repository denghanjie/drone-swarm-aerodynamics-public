'use strict';
/* Deferred actual-runner clock fixture. Dynamics, controller, field, geometry,
 * recording and branch audit are replaced by explicit synthetic stubs. No
 * Boids equations or source initial conditions execute. */
if(process.env.JOINT_REFERENCE_WINDOW_ACTIVE!=='1')throw Error('Coordinator-authorized numerical window required');
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),vm=require('node:vm'),crypto=require('node:crypto');
const filename=path.resolve(__dirname,'../implementation/src/run.cjs'),tests=[];
function test(name,fn){try{fn();tests.push({name,passed:true});}catch(e){tests.push({name,passed:false,error:{name:e.name,message:e.message,stack:e.stack}});}}
function runner(kind){
 const log={steps:[],controllerTicks:[],fieldCalls:0},moduleObject={exports:{}};
 const Y=Array.from({length:16},(_,i)=>{const s=Array(17).fill(0);s[0]=2*i;s[2]=2;s[9]=1;return s;});
 const field=states=>{log.fieldCalls++;return {winds:states.map(()=>[0,0,0,0]),counters:{evaluatedRotorKernels:0,candidates:0},maximumInflow:0};};
 const B={P:{bodyRadius:.075},initial:()=>Y.map(s=>s.slice()),obstacleContacts:()=>[],contactCandidates:()=>[],course:{boxes:[]}};
 const controller=(states,tick)=>{log.controllerTicks.push(tick);const commands=states.map(()=>Array(4).fill(tick+1));return {commands,event:{tick,commands}};};
 const bytes=rows=>Buffer.from(JSON.stringify(rows)),sha=buffer=>crypto.createHash('sha256').update(buffer).digest('hex');
 class Audit{constructor(){this.samples=0;}observe(states,location){this.samples++;return {states,raw:states,location,pairs:[],signatureSha256:'0'.repeat(64)};}compare(){}checkStep(){}finish(){return {samples:this.samples};}}
 const M={createEvaluator:()=>field,integrate(s,c){if(s[0]===0)log.steps.push({command:c[0]});return s.slice();}};
 function jointStep(states,commands,h,hooks){log.steps.push({command:commands[0][0]});for(let stage=1;stage<=4;stage++){const fraction=[0,.5,.5,1][stage-1],raw=states.map(s=>s.slice()),geometry=states.map(s=>s.slice()),data={raw,geometry,commands,stage,fraction};hooks.beforeStage(data);const result=hooks.field(geometry),derivatives=states.map(()=>Array(17).fill(0));for(let i=0;i<16;i++){hooks.beforeDerivative?.({drone:i,stage});hooks.afterDerivative?.({drone:i,stage});}hooks.afterStage({...data,result,derivatives});}hooks.onProjection({raw:states,accepted:states,projectionSizes:states.map(()=>0)});return states.map(s=>s.slice());}
 const IO={sha,rawBytes:bytes,writeRaw(relative,rows,metadata){return {path:relative,shape:[rows.length,metadata.count,17],bytes:rows.length*metadata.count*17*8};},save(){},atomicWrite(){}};
 const requireFake=id=>id==='crypto'?crypto:id==='./exact-aero.cjs'?M:id==='./source.cjs'?{source:()=>({boxDistance:()=>({distance:10}),segmentPair:()=>10})}:id==='./controller.cjs'?{B,controller}:id==='./joint-step.cjs'?{jointStep}:id==='./branch-audit.cjs'?{BranchAudit:Audit}:id==='./io.cjs'?IO:id==='./controller-record.cjs'?{writeControllers:()=>({})}:(()=>{throw Error('Unexpected dependency '+id);})();
 vm.runInNewContext(fs.readFileSync(filename,'utf8'),{module:moduleObject,exports:moduleObject.exports,require:requireFake,Buffer,performance,process,console},{filename});
 const row={arm:'synthetic-clock-'+kind,kind,stepTicks:32,...(kind==='held'?{airTicks:32}:{})},out=moduleObject.exports.run(999,row,{budgetCheck(){},checkpoint(){}});
 return {out,log};
}
for(const kind of ['joint','held'])test(`actual ${kind} runner uses old command through boundary and has no terminal discrete update`,()=>{
 const {out,log}=runner(kind);assert.equal(out.result.complete,true);assert.equal(out.result.endTick,51200);assert.equal(log.steps.length,1600);assert.equal(log.controllerTicks.length,100);
 assert.equal(log.controllerTicks[0],0);assert.equal(log.controllerTicks.at(-1),50688);assert.ok(!log.controllerTicks.includes(51200));
 assert.equal(log.steps[15].command,1);assert.equal(log.steps[16].command,513);assert.equal(log.steps.at(-1).command,50689);
 assert.equal(out.common.length,1601);assert.equal(out.result.work.controllerUpdates,100);
 if(kind==='held'){assert.equal(out.result.work.fieldUpdates,1600);assert.equal(out.result.heldTick,51168);assert.equal(out.result.fieldEvents.count,1600);}else assert.equal(log.fieldCalls,6400);
});
const report={schema:'independent-actual-runner-clock-fixtures/v1',kind:'actual run.cjs scheduler with synthetic stubs; no genuine Boids trajectories',tests,passed:tests.every(t=>t.passed)};process.stdout.write(JSON.stringify(report)+'\n');if(!report.passed)process.exitCode=1;
