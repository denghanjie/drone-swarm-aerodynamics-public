'use strict';
if(process.env.FLOCK_FACTORY_VARIANT&&process.env.FLOCK_FACTORY_VARIANT!=='wide')throw Error('Unfrozen factory variant');
const fs=require('fs'),path=require('path');
const {ROOT,load,save,retainedBytes}=require('./io.cjs'),{validateFreeze}=require('./freeze.cjs');
function main(){
 if(process.env.JOINT_SUPERVISED!=='1'||!process.send)throw Error('Numerical jobs require supervisor');
 const freeze=validateFreeze(),config=load('configs/campaign.json'),started=performance.now(),cpu0=process.cpuUsage(),deadline=BigInt(process.env.JOINT_TOTAL_DEADLINE_NS);
 const {fixtures}=require('../tests/fixtures.cjs'),{preflight,readInput}=require('./preflight.cjs'),{run}=require('./run.cjs'),{compare,gate,compareControllers,skippedRows,keys}=require('./compare.cjs'),{B}=require('./controller.cjs');
 if(B.course.id!=='factory-v1')throw Error('Wrong frozen course');
 const data=new Map(),attempted=[],jobs=[],gates=[],comparisons=[],controllers=[],preflights=[];let phase='fixtures',failure=null,status='running',jobDeadline=null;
 function budgetCheck(){const now=process.hrtime.bigint();if(now>deadline-2000000000n)throw Error('Total cooperative wall cap');if(jobDeadline&&now>jobDeadline-1000000000n)throw Error('Per-job cooperative wall cap');const cpu=process.cpuUsage(cpu0);if(cpu.user+cpu.system>config.maxCpuSeconds*1e6)throw Error('CPU cap');}
 const checkpoint=record=>save('results/last-checkpoint.json',record);
 function job(id,fn){budgetCheck();const start=process.hrtime.bigint(),cpu=process.cpuUsage();jobDeadline=start+BigInt(config.maxJobSeconds)*1000000000n;process.send({type:'job-start',id,startMonotonicNs:String(start),deadlineMonotonicNs:String(jobDeadline)});try{return fn();}finally{const used=process.cpuUsage(cpu),r={id,wallMs:Number(process.hrtime.bigint()-start)/1e6,cpuMs:(used.user+used.system)/1000,includesSerialization:true};jobs.push(r);process.send({type:'job-end',id,...r});jobDeadline=null;budgetCheck();}}
 function snapshot(){const cpu=process.cpuUsage(cpu0);save('results/campaign.json',{status,phase,failure,freeze,config,runIds:attempted,jobs,preflights:preflights.map(r=>({id:r.id,passed:r.passed,visitedEndpoints:r.visitedEndpoints})),gates,comparisons,controllerComparisons:controllers,matrix:skippedRows(config,attempted,failure?.message||'not yet reached'),resources:{wallMs:performance.now()-started,cpuMs:(cpu.user+cpu.system)/1000,retainedBytes:retainedBytes()},provisionalAllScientificGatesPassed:status==='complete'&&gates.every(g=>g.passed),requiresSupervisorValidity:true,claim:'Bounded cross-checked numerical reference only if every gate passed on both prescribed seeds; never physical truth'},{emergency:status==='stopped'});}
 function execute(seed,arm){const row=config.rows.find(r=>r.arm===arm);attempted.push(`s${seed}-${arm}`);const d=job(`s${seed}-${arm}`,()=>run(seed,row,{budgetCheck,checkpoint}));data.set(d.result.runId,d);snapshot();if(!d.result.complete)throw Object.assign(Error('Coupled run stopped'),{detail:d.result.stop});return d;}
 const get=(seed,arm)=>data.get(`s${seed}-${arm}`);
 function cmp(a,b){const c=compare(a,b);comparisons.push(c);controllers.push(compareControllers(a,b));return c;}
 function keepGate(name,seed,g){gates.push({name,seed,...g});if(!g.passed)throw Object.assign(Error(`${name} failed`),{detail:{seed,gate:g}});}
 try{
  job('implementation-fixtures',()=>fixtures({budgetCheck}));
  for(const name of ['test_joint_robustness.cjs','test_io_faults.cjs','test_branch_boundaries.cjs','test_watchdog_contract.cjs','test_runner_clock.cjs'])job('independent-'+name,()=>{const r=require('child_process').spawnSync(process.execPath,[path.resolve(ROOT,'../robustness-review',name)],{env:{...process.env,JOINT_REFERENCE_WINDOW_ACTIVE:'1'},encoding:'utf8',timeout:44000,maxBuffer:1000000});save(`results/fixtures/${name}.json`,{name,status:r.status,signal:r.signal,error:r.error?String(r.error):null,stdout:r.stdout,stderr:r.stderr});if(r.status!==0||r.signal||r.error)throw Error('Independent fixture failed: '+name);});
  phase='saved-path-preflight';for(const seed of config.seeds){const p=job(`preflight-s${seed}`,()=>preflight(seed,{budgetCheck,checkpoint}));preflights.push(p);snapshot();if(!p.passed)throw Object.assign(Error('Saved-path preflight blocked'),{detail:p.stop});}
  phase='compatibility';const compatibility=job('compatibility',()=>run(config.compatibility.seed,config.compatibility,{budgetCheck,checkpoint}));const r=compatibility.result,expected=config.compatibility;const passed=r.complete&&r.terminalStateWindSha256===expected.terminalStateWindSha256&&Object.entries(expected.work).every(([k,v])=>r.work[k]===v)&&r.heldTick===50688;save('results/compatibility.json',{passed,expected,actual:{complete:r.complete,terminalStateWindSha256:r.terminalStateWindSha256,work:r.work,heldTick:r.heldTick}});if(!passed)throw Error('Historical compatibility failed');
  phase='joint-reference';for(const seed of config.seeds)for(const arm of ['J1','J2','J3'])execute(seed,arm);
  job('joint-gates',()=>{for(const seed of config.seeds)keepGate('joint self-consistency',seed,gate(cmp(get(seed,'J2'),get(seed,'J3')),config.smallCaps,{coarse:cmp(get(seed,'J1'),get(seed,'J2')),floors:config.floors,reduction:config.jointReduction}));});
  phase='held-physics';for(const seed of config.seeds)for(const arm of ['H4','P1'])execute(seed,arm);
  job('physics-gates',()=>{for(const seed of config.seeds)keepGate('held physics',seed,gate(cmp(get(seed,'H4'),get(seed,'P1')),config.smallCaps));});
  phase='held-refinement';for(const seed of config.seeds)for(const arm of ['H1','H2','H3'])execute(seed,arm);
  job('bridge-and-cross-family-gates',()=>{for(const seed of config.seeds){
   const old=readInput(seed),common=[];for(let n=0;n<6401;n+=4)common.push(old.raw.row(n));const historical={result:{...old.run,endTick:51200,originalGrid:{endTick:old.run.endTick,config:old.run.config},config:{...old.run.config,seed,count:16,commonTicks:32,baseTickSeconds:1/51200}},common,controlEvents:preflights.find(p=>p.seed===seed).controlEvents};
   // Preflight separately checks every historical command against exact source.
   const bridge=compare(get(seed,'H1'),historical);comparisons.push(bridge);controllers.push(compareControllers(get(seed,'H1'),historical));keepGate('historical bridge',seed,gate(bridge,config.smallCaps));
   const errors=['H1','H2','H3','H4'].map(arm=>cmp(get(seed,arm),get(seed,'J3')));
   keepGate('finest cross-family caps',seed,gate(errors[3],config.originalCaps));
   for(let k=1;k<4;k++){const rows=keys.map(key=>({key,coarse:errors[k-1].maximum[key],fine:errors[k].maximum[key],limit:Math.max(config.floors[key],config.crossFamilyReduction*errors[k-1].maximum[key])}));keepGate(`cross-family reduction ${k}`,seed,{passed:rows.every(r=>r.fine<=r.limit),rows});}
  }});
  status='complete';phase='finished';snapshot();budgetCheck();
 }catch(e){status='stopped';failure={type:e.constructor.name,message:e.message,detail:e.detail||null,phase};save('results/failures/campaign.json',failure);snapshot();process.exitCode=1;}
}
if(require.main===module)main();module.exports={main};
