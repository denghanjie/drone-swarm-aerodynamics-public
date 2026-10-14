'use strict';
const fs=require('fs'),path=require('path');
const {ROOT,load,save,sha,fileSha,sourceManifest,readSeries,retainedBytes}=require('./io.cjs');
const {run,persist,compare,Q}=require('./coupled.cjs');
const {replayDriver}=require('./replay.cjs');
const KEYS=['positionM','velocityMps','attitudeRad','angularVelocityRadps'];
function referenceGate(coarse,fine,thresholds,floors,reduction){const rows=KEYS.map(key=>({key,coarse:coarse.maximum[key],fine:fine.maximum[key],limit:thresholds[key],floor:floors[key],magnitudePassed:fine.maximum[key]<=thresholds[key],reductionPassed:fine.maximum[key]<=Math.max(floors[key],reduction*coarse.maximum[key])}));return {passed:rows.every(x=>x.magnitudePassed&&x.reductionPassed),rows,reduction,coarse,fine};}
function diskSize(dir){let size=0;if(!fs.existsSync(dir))return size;for(const f of fs.readdirSync(dir)){const p=path.join(dir,f),s=fs.statSync(p);size+=s.isDirectory()?diskSize(p):s.size;}return size;}
function validateFreeze(){const cfg=load('configs/campaign.json'),freeze=load('FREEZE.json');if(cfg.status!=='FROZEN_AUTHORIZED'||freeze.status!=='FROZEN_AUTHORIZED')throw Error('Parent freeze required before any campaign cases');if(fileSha(path.join(ROOT,'src/exact-aero.cjs'))!==cfg.exactSourceSha256)throw Error('Frozen evaluator changed');if(sha(JSON.stringify(sourceManifest()))!==freeze.sourceManifestSha256)throw Error('Source/config changed since freeze');if(fileSha(path.join(ROOT,'PLAN.md'))!==freeze.planSha256)throw Error('Plan changed since freeze');return {cfg,freeze};}
function main(){
 if(process.env.TEMPORAL_SUPERVISED!=='1'||!process.send)throw Error('Run through src/supervise.cjs so hard watchdogs cannot be bypassed');
 const {cfg,freeze}=validateFreeze();if(fs.existsSync(path.join(ROOT,'results/campaign.json')))throw Error('Existing campaign results: refuse unregistered rerun');
 if(process.env.FLOCK_FACTORY_VARIANT&&process.env.FLOCK_FACTORY_VARIANT!=='wide')throw Error('Unfrozen factory variant');
 const started=performance.now(),cpu0=process.cpuUsage(),store=new Map(),runs=[],gates={physics:[],air:[]},replays=[],coupled=[];
 let status='running',phase='compatibility',failure=null,storageUncompressed=0,jobStarted=performance.now(),jobId=null,jobDeadline=null;
 const totalDeadline=BigInt(process.env.TEMPORAL_TOTAL_DEADLINE_NS);
 function beginJob(id){jobId=id;jobStarted=performance.now();const at=process.hrtime.bigint();jobDeadline=at+45000000000n;process.send({type:'job-start',id,startMonotonicNs:String(at),deadlineMonotonicNs:String(jobDeadline)});}
 function endJob(){budgetCheck();process.send({type:'job-end',id:jobId});jobId=null;jobDeadline=null;}
 function budgetCheck(){const now=process.hrtime.bigint();if(now>totalDeadline-2000000000n)throw Error('Campaign cooperative wall-time cap');if(jobDeadline&&now>jobDeadline-1000000000n)throw Error('Per-job cooperative wall-time cap');const cpu=process.cpuUsage(cpu0);if((cpu.user+cpu.system)>cfg.maxCpuSeconds*1e6)throw Error('Campaign CPU cap');}
 function checkpoint(){const cpu=process.cpuUsage(cpu0);save('results/campaign.json',{status,phase,failure,freeze,config:cfg,runIds:runs.map(x=>x.runId),gates,replayRunIds:replays.map(x=>x.runId),coupledComparisons:coupled,resources:{elapsedWallMs:performance.now()-started,cpuMs:(cpu.user+cpu.system)/1000,rawUncompressedBytes:storageUncompressed,allCampaignLogicalUncompressedBytes:retainedBytes(),retainedDiskBytes:diskSize(path.join(ROOT,'results')),maxRssKiB:process.resourceUsage().maxRSS},claim:'Numerical screens conditional on unchanged physically unvalidated model. No physical validation, full mission, GPU or hardware-throughput claim.'},{emergency:status==='stopped'});}
 function execute(seed,p,a,{compatibility=false}={}){beginJob(`coupled-s${seed}-p${p}-a${a}`);budgetCheck();const data=run({seed,count:cfg.count,duration:cfg.duration,physicsDt:p*Q,airDt:a*Q,dense:!compatibility&&p===1&&a===4,compatibility,budgetCheck});const r=persist(data);storageUncompressed+=(r.commonStates?.uncompressedBytes||0)+(r.denseStates?.uncompressedBytes||0);runs.push(r);store.set(r.runId,data);checkpoint();if(!r.complete)throw Object.assign(Error('Coupled run stopped'),{detail:{runId:r.runId,stop:r.stop}});if(r.work.controllerUpdates!==100||r.work.physicsSteps!==6400/p||r.work.fieldUpdates!==6400/a||r.heldTick!==6400-a)throw Error('Unexpected event/work counts');endJob();return data;}
 const get=(s,p,a)=>store.get(`s${s}-p${p}-a${a}`);
 function conditionalReplay(){phase+=' / conditional-fixed-path';for(const seed of cfg.seeds){const driver=get(seed,1,4);if(!driver?.result.complete)continue;beginJob(`conditional-replay-s${seed}`);const r=replayDriver(driver.result,cfg,{budgetCheck,referenceQualified:false});replays.push(r);storageUncompressed+=r.freshFields.uncompressedBytes;checkpoint();endJob();}beginJob('conditional-classification-output');save('results/cadence-screens.json',{referenceQualified:false,cadenceScreens:cfg.airCadences.map(airDt=>({airDt,qualified:false,cadence_qualified:false,status:'unqualified; no cadence classification'})),reason:'reference_failed; only already complete valid dense drivers were replayed.'});checkpoint();endJob();require('./evaluate.cjs').reconstruct();}
 try{
  const preflight=execute(4301,16,64,{compatibility:true}),expected='fabdd3452577cfdc3cb948ecd12b90c93fc74ee8673129a9737ca2d3e1265ef7';
  save('results/compatibility.json',{passed:preflight.result.terminalStateWindSha256===expected,expectedTerminalStateWindSha256:expected,actualTerminalStateWindSha256:preflight.result.terminalStateWindSha256,sourceRecord:'prior exact campaign results/pipeline.json; selected lean; seed4301; N16; T1s; p2.5ms; air10ms',work:preflight.result.work,heldTick:preflight.result.heldTick});
  if(preflight.result.terminalStateWindSha256!==expected)throw Error('Production compatibility checksum failed');
  phase='physics-reference';for(const seed of cfg.seeds)for(const p of [4,2,1])execute(seed,p,4);
  beginJob('physics-reference-analysis');for(const seed of cfg.seeds)gates.physics.push({seed,...referenceGate(compare(get(seed,4,4),get(seed,2,4)),compare(get(seed,2,4),get(seed,1,4)),cfg.gates.physics,cfg.gates.comparisonFloors,1)});
  checkpoint();endJob();if(!gates.physics.every(x=>x.passed)){status='reference-not-established';phase='physics-screen-failed';checkpoint();conditionalReplay();return;}
  phase='airflow-reference';for(const seed of cfg.seeds)for(const a of [8,16])execute(seed,1,a);
  beginJob('air-reference-analysis');for(const seed of cfg.seeds)gates.air.push({seed,...referenceGate(compare(get(seed,1,16),get(seed,1,8)),compare(get(seed,1,8),get(seed,1,4)),cfg.gates.airReference,cfg.gates.comparisonFloors,cfg.gates.airReferenceReduction)});
  checkpoint();endJob();if(!gates.air.every(x=>x.passed)){status='reference-not-established';phase='airflow-screen-failed';checkpoint();conditionalReplay();return;}
  phase='coarser-airflow';for(const seed of cfg.seeds)for(const a of [32,64])execute(seed,1,a);
  beginJob('ancillary-coupled-comparisons');for(const seed of cfg.seeds)for(const a of [4,8,16,32,64]){const comparison=compare(get(seed,1,a),get(seed,1,4));coupled.push({seed,airDt:a*Q,...comparison,descriptiveScreens:KEYS.map(key=>({key,value:comparison.maximum[key],threshold:cfg.gates.airReference[key],passed:comparison.maximum[key]<=cfg.gates.airReference[key]}))});}checkpoint();endJob();
  phase='fixed-path-replay';for(const seed of cfg.seeds){beginJob(`replay-s${seed}`);const r=replayDriver(get(seed,1,4).result,cfg,{budgetCheck});replays.push(r);storageUncompressed+=r.freshFields.uncompressedBytes;checkpoint();endJob();}
  beginJob('cadence-classification-output');
  const cadenceScreens=cfg.airCadences.map(airDt=>({airDt,qualified:replays.every(r=>r.rows.find(x=>x.airDt===airDt)?.qualifiedConditionalOnReference),perSeed:replays.map((r,i)=>({seed:cfg.seeds[i],quadraturePassed:r.rows.find(x=>x.airDt===airDt).quadrature.passed,errorScreen:r.rows.find(x=>x.airDt===airDt).errorScreen,excitation:r.excitation}))}));save('results/cadence-screens.json',{referenceQualified:true,cadenceScreens,scope:'Both seeds separately required; two N16 1s cases only'});
  checkpoint();endJob();require('./evaluate.cjs').reconstruct();beginJob('final-completion');status='complete';phase='complete';checkpoint();endJob();
 }catch(e){status='stopped';failure={phase,type:e.constructor.name,message:e.message,detail:e.detail||null};save('results/failures/campaign.json',failure);checkpoint();process.exitCode=1;}
 console.log(JSON.stringify({status,phase,failure,runCount:runs.length,wallMs:performance.now()-started}));
}
module.exports={referenceGate,validateFreeze,main};
if(require.main===module)main();
