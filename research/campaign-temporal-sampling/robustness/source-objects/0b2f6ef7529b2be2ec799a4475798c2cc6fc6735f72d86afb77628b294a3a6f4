'use strict';
// External watchdog. The worker is strictly serial, but its synchronous loops
// cannot block this process. hrtime monotonic deadlines are shared host-wide.
const {fork}=require('child_process'),path=require('path'),fs=require('fs');
const {ROOT,load,save,retainedBytes}=require('./io.cjs');
const {validateFreeze}=require('./campaign.cjs');
try{validateFreeze();}catch(e){save('results/failures/preflight-validation.json',{phase:'source/config/plan freeze validation',type:e.constructor.name,message:e.message,detail:e.detail||null,numericalJobsStarted:false},{emergency:true});throw e;}
if(process.argv.length>2)throw Error('Only the original frozen campaign window is available; no numerical restart or separate audit allowance');
const record='results/supervisor.json';
if(fs.existsSync(path.join(ROOT,record)))throw Error('Do not restart or reset this execution budget');
const start=process.hrtime.bigint(),totalDeadline=start+300000000000n,startedAt=new Date().toISOString();
save(record,{status:'starting',mode:'original bounded campaign',startedAt,startMonotonicNs:String(start),totalDeadlineMonotonicNs:String(totalDeadline),totalLimitSeconds:300,jobLimitSeconds:45,restartsPermitted:false});
const child=fork(path.join(__dirname,'campaign.cjs'),[],{cwd:ROOT,env:{...process.env,TEMPORAL_SUPERVISED:'1',TEMPORAL_TOTAL_DEADLINE_NS:String(totalDeadline)},stdio:['ignore','pipe','pipe','ipc']});
let job=null,jobTimer=null,killed=null,stdout='',stderr='';
child.stdout.on('data',x=>{stdout+=x;process.stdout.write(x);});child.stderr.on('data',x=>{stderr+=x;process.stderr.write(x);});
function remainingMs(deadline){return Math.max(0,Number(deadline-process.hrtime.bigint())/1e6);}
function kill(reason){if(killed)return;killed={reason,job,at:new Date().toISOString(),elapsedWallMs:Number(process.hrtime.bigint()-start)/1e6};child.kill('SIGKILL');}
const totalTimer=setTimeout(()=>kill('hard total 300-second watchdog'),remainingMs(totalDeadline));
child.on('message',m=>{if(m.type==='job-start'){clearTimeout(jobTimer);job={id:m.id,startMonotonicNs:m.startMonotonicNs,deadlineMonotonicNs:m.deadlineMonotonicNs};const deadline=BigInt(m.deadlineMonotonicNs);if(deadline-BigInt(m.startMonotonicNs)>45000000000n)return kill('invalid oversized job deadline');jobTimer=setTimeout(()=>kill('hard per-job 45-second watchdog'),remainingMs(deadline));}else if(m.type==='job-end'){if(job?.id!==m.id)return kill('job lifecycle mismatch');if(process.hrtime.bigint()>BigInt(job.deadlineMonotonicNs))return kill('job exceeded 45-second deadline before completion acknowledgement');clearTimeout(jobTimer);job=null;}});
child.on('error',e=>{stderr+='\nFork/runtime error: '+e.message;kill('child-process launch or transport failure');});
child.on('close',(code,signal)=>{clearTimeout(jobTimer);if(process.hrtime.bigint()>totalDeadline-1000000000n&&!killed)killed={reason:'Insufficient hard-budget headroom for final serialization',job,at:new Date().toISOString()};let checkpoint=null;try{checkpoint=load('results/last-checkpoint.json');}catch{}const result={status:killed?'watchdog-stopped':code===0?'finished':'worker-stopped',mode:'original bounded campaign',code,signal,killed,startedAt,startMonotonicNs:String(start),totalDeadlineMonotonicNs:String(totalDeadline),elapsedWallMs:Number(process.hrtime.bigint()-start)/1e6,logicalUncompressedRetainedBytes:retainedBytes(),stdout,stderr,postInterruptionEmergencyLoggingIsCleanup:!!killed};
 if(killed)save('results/failures/watchdog.json',{...result,exactStoppedState:false,stoppedStateUnavailable:true,lastDurableCheckpoint:checkpoint,warning:'The checkpoint is older evidence, not the exact state at interruption. No interrupted member can qualify.'},{emergency:true});
 save(record,result,{emergency:true});if(process.hrtime.bigint()>totalDeadline&&!killed){killed={reason:'Final accounting/serialization exceeded total hard budget'};result.status='watchdog-stopped';result.killed=killed;result.postInterruptionEmergencyLoggingIsCleanup=true;save(record,result,{emergency:true});save('results/failures/finalization.json',{exactStoppedState:false,numericalWorkerAlreadyExited:true,reason:killed.reason},{emergency:true});}
 save('results/execution-validity.json',{uninterruptedSuccessfulExecution:!killed&&code===0,qualifiedResultsMayBeConsidered:!killed&&code===0,referenceQualificationStillRequiresBothSeedsAndAllGates:true,reason:killed?.reason||(code===0?'worker completed without watchdog interruption':'worker stopped; inspect exact failure evidence')},{emergency:true});clearTimeout(totalTimer);if(killed||code!==0)process.exitCode=1;
});
