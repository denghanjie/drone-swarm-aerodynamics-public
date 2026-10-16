'use strict';
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const p=path.resolve(process.argv[2]),config=JSON.parse(fs.readFileSync(path.join(p,'config.json'))),A=require('./adapter.cjs'),F=require('../../../outputs/step02c-source/physics.cjs');
process.env.FLOCK_FACTORY_VARIANT='wide';
const S=require('../../../outputs/milestone-31-source/sim.cjs'),{Grid}=require('../../../outputs/milestone-31-source/grid.cjs'),G=require('../../../outputs/milestone-31-source/geometry.cjs');
const began=performance.now();let written=0,peakRSS=0,active=null;
fs.mkdirSync(path.join(p,'results'),{recursive:true});
function guard(){peakRSS=Math.max(peakRSS,process.memoryUsage().rss);if(peakRSS>config.limits.rssBytes)throw Error('RSS guard exceeded');if(performance.now()-began>config.limits.candidateCooperativeSeconds*1000)throw Error('wall guard exceeded');}
function save(name,data,emergency=false){const b=Buffer.from(JSON.stringify(data)+'\n');if(written+b.length>config.limits.evidenceBytes-(emergency?0:8*1024**2))throw Error('evidence cap exceeded');fs.writeFileSync(path.join(p,'results',name),b,{flag:'wx'});written+=b.length;return {path:'results/'+name,bytes:b.length,sha256:crypto.createHash('sha256').update(b).digest('hex')};}
let initial=null;
function control(states){const grid=new Grid(states,S.P.neighbor);return states.map((s,i)=>{const ids=grid.neighbors(i,S.P.neighbor),v=S.steer(i,states,ids,'boids','wall-priority');return {...F.control(s,{vx:v[0],vy:v[1],z:s[2]+(2.5*v[2]+1.5*s[5])/6,yaw:Math.atan2(v[1],v[0])},2.25),neighbors:ids,desired:v};});}
function safety(old,states){let minimum=Infinity;for(let i=0;i<states.length;i++){if(!states[i].every(Number.isFinite)||states[i][2]<S.P.bodyRadius)return {problem:{kind:'vehicle model limit',drone:i},minimum:null};const hits=S.obstacleContacts(old[i],states[i]);if(hits.length)return {problem:{kind:'obstacle contact envelope',drone:i,hits},minimum:null};}for(let i=0;i<states.length;i++)for(let j=i+1;j<states.length;j++){const d=G.segmentPair(old[i],states[i],old[j],states[j]);minimum=Math.min(minimum,d);if(d<2*S.P.bodyRadius)return {problem:{kind:'drone contact envelope',pair:[i,j],distance:d},minimum};}return {problem:null,minimum};}
function run(mode,h){
 const c=config.cases[0],id=c.id+'-'+mode+'-'+String(h),start=performance.now();if(initial===null)initial=S.initial(c.seed,c.n);
 let states=initial.map(s=>s.slice()),controls=control(states),t=0,cache=null,stageCalls=0,endpointAttempts=0,saturatedUpdates=0,jointAttempts=0,cachedAttempts=0,refreshAttempts=0,propagationRefreshAttempts=0,terminalAuditAttempts=0;
 const rec={id,case:c.id,mode,dt:h,minimumSweptSeparation:null,initial:states.map(s=>s.slice()),complete:false,samples:[],stages:[],stepWitnesses:[],controls:[],events:[],failure:null,counts:{}};active=rec;
 function refresh(){
  const index=rec.events.length,at=+t.toFixed(6),role=at<c.duration?'propagation-refresh':'terminal-audit',commands=controls.map(x=>x.u),record={index,t:at,role,status:'started',states:states.map(s=>s.slice()),commands,oldCacheIndex:cache?.index??null,left:null,instantaneous:null,cache:null,right:null,error:null,postError:null};
  rec.events.push(record);refreshAttempts++;if(role==='propagation-refresh')propagationRefreshAttempts++;else terminalAuditAttempts++;
  try{if(cache){cachedAttempts++;record.left=A.cached(states,commands,cache,at,guard,config);}jointAttempts++;record.instantaneous=A.full(states,commands,guard,config);cache=A.makeCache(record.instantaneous,index,at);record.cache=cache;cachedAttempts++;record.right=A.cached(states,commands,cache,at,guard,config);record.error=A.loadError(record.left,record.instantaneous);record.postError=A.loadError(record.right,record.instantaneous);record.status='completed';return record;}
  catch(e){record.status='rejected';record.reason=e.message;e.event={index,t:at,role,states:record.states,commands,oldCacheIndex:record.oldCacheIndex};throw e;}
 }
 function sample(event=null){endpointAttempts++;let e;if(mode==='coupled'){jointAttempts++;e=A.full(states,controls.map(x=>x.u),guard,config);}else{if(!event||event.status!=='completed')throw Error('sample event unavailable');e=t===0?event.right:event.left;}
  rec.samples.push({t:+t.toFixed(6),states:states.map(s=>s.slice()),commands:controls.map(x=>x.u),forces:e.forces,modeledCorrections:e.modeledCorrections,corrections:e.corrections,derivatives:e.derivatives,info:e.info,witness:e.witness,group:S.measure(states),eventIndex:event?.index??null,sampleSide:mode==='coupled'?'instantaneous':t===0?'right':'left'});
 }
 try{
  sample(mode==='reuse10ms'?refresh():null);
  const totalSteps=Math.round(c.duration/h),refreshSteps=Math.round(config.refreshDt/h),sampleSteps=Math.round(config.sampleDt/h);
  for(let k=0;k<totalSteps;k++){
   guard();if(k%Math.round(config.controlDt/h)===0){controls=control(states);saturatedUpdates+=controls.filter(x=>x.saturated).length;rec.controls.push({t:+(k*h).toFixed(6),values:controls});}
   const old=states,capture=k===0||k===totalSteps-1;
   const beforeStage=s=>{stageCalls++;if(s.evaluationAttempted){if(mode==='coupled')jointAttempts++;else cachedAttempts++;}rec.stages.push(s);};
   states=A.step(states,controls.map(x=>x.u),mode,cache,h,k*h,guard,config,beforeStage,capture);
   if(capture)rec.stepWitnesses.push({step:k,t:k*h,h,initial:old,final:states,commands:controls.map(x=>x.u),cacheIndex:cache?.index??null});
   t=(k+1)*h;const check=safety(old,states);if(check.minimum!==null)rec.minimumSweptSeparation=Math.min(rec.minimumSweptSeparation??Infinity,check.minimum);if(check.problem){rec.failure={...check.problem,t,old,states};break;}
   const event=mode==='reuse10ms'&&(k+1)%refreshSteps===0?refresh():null;
   if((k+1)%sampleSteps===0)sample(event);
  }
  rec.complete=!rec.failure&&Math.abs(t-c.duration)<1e-10;
 }catch(e){rec.failure={kind:e.message,t,lastAcceptedStates:states,stage:e.stage??null,event:e.event??null,detail:e.detail??null};if(['RSS guard exceeded','wall guard exceeded','evidence cap exceeded'].includes(e.message))throw e;}finally{
 rec.counts={integrationStageAttempts:stageCalls,endpointAttempts,jointQueryAttempts:jointAttempts,cachedApplicationAttempts:cachedAttempts,refreshEventAttempts:refreshAttempts,propagationRefreshAttempts,terminalAuditAttempts,saturatedControllerUpdates:saturatedUpdates};
 rec.elapsedMs=performance.now()-start;rec.final=states;rec.end=t;}
 rec.pin=save(id+'.json',rec);return rec;
}
const output={kind:config.kind,complete:false,trials:[],convergence:[],referenceAgreement:[],comparisons:[],eventErrors:[],descriptive:[],reuseExecuted:false,environment:{node:process.version,arch:process.arch,platform:process.platform},limitations:['same exposed seed; numerical approximation test','cached ratios do not satisfy current joint closure between refreshes','current geometry/admission not evaluated at ordinary cached stages','positive saved load samples use pre-refresh left side','call reduction is not measured speedup','no physical, stability, novelty or 5000-drone validation']};
function record(mode){const rs=[];for(const h of config.timesteps){const r=run(mode,h);rs.push(r);output.trials.push({id:r.id,complete:r.complete,pin:r.pin,failure:r.failure?.kind??null});}output.convergence.push({case:'boids16',mode,...A.convergence(...rs,config)});return rs;}
function summarizeEvents(r){const maxima={rotor:0,force:0,moment:0},postMaxima={rotor:0,force:0,moment:0};for(const e of r.events){if(e.error)for(const k of Object.keys(maxima))maxima[k]=Math.max(maxima[k],e.error[k]);if(e.postError)for(const k of Object.keys(maxima))postMaxima[k]=Math.max(postMaxima[k],e.postError[k]);}const gates=Object.fromEntries(Object.entries(config.eventErrorTolerances).map(([k,tolerance])=>[k,{maximum:maxima[k],tolerance,pass:r.complete&&maxima[k]<=tolerance}]));return {id:r.id,dt:r.dt,positiveEvents:r.events.filter(e=>e.t>0&&e.status==='completed').length,maxima,postMaxima,postRefreshPass:r.complete&&Object.values(postMaxima).every(x=>x<=config.identityTolerance),gates,pass:r.complete&&Object.values(gates).every(x=>x.pass)};}
try{
 const {controls}=require('./controls.cjs');output.adapterControls=controls(config);save('adapter-controls.json',output.adapterControls);if(!output.adapterControls.pass)throw Error('adapter controls failed');
 const full=record('coupled');
 for(const r of full){const pin=config.references.find(x=>x.dt===r.dt),raw=fs.readFileSync(path.resolve(p,'../..',pin.path));if(raw.length!==pin.bytes||crypto.createHash('sha256').update(raw).digest('hex')!==pin.sha256)throw Error('reference pin mismatch');const ref=JSON.parse(raw),fields=['t','states','commands','forces','modeledCorrections','corrections','derivatives','witness','group'],mismatches=[];if(r.samples.length!==ref.samples.length)mismatches.push('sample count');for(let k=0;k<Math.min(r.samples.length,ref.samples.length);k++)for(const f of fields)if(JSON.stringify(r.samples[k][f])!==JSON.stringify(ref.samples[k][f]))mismatches.push(k+':'+f);output.referenceAgreement.push({id:r.id,reference:pin.path,sha256:pin.sha256,fields,samples:r.samples.length,mismatches,pass:r.complete&&ref.complete&&mismatches.length===0});}
 output.primaryPass=full.every(x=>x.complete)&&output.referenceAgreement.every(x=>x.pass)&&output.convergence.every(x=>x.pass);
 const byMode={coupled:full};
 if(output.primaryPass){output.reuseExecuted=true;const reuse=record('reuse10ms');byMode.reuse10ms=reuse;
  output.comparisons=reuse.map((r,i)=>{const maximumSampled=A.discrepancy(full[i],r),gates=Object.fromEntries(Object.entries(config.approximationTolerances).map(([k,tolerance])=>[k,{maximum:maximumSampled?.[k]??null,tolerance,pass:!!maximumSampled&&maximumSampled[k]<=tolerance}]));return {dt:r.dt,left:'coupled',right:'reuse10ms',maximumSampled,gates,pass:Object.values(gates).every(x=>x.pass)};});
  output.eventErrors=reuse.map(summarizeEvents);
 }
 for(const rs of Object.values(byMode))for(const r of rs){const stages=r.stages.filter(x=>x.status==='completed');output.descriptive.push({id:r.id,mode:r.mode,dt:r.dt,maxRecordedStageTiltDegrees:stages.length?Math.max(...stages.map(x=>x.maxTiltDegrees)):null,finalCentroid:[0,1,2].map(k=>r.final.reduce((v,s)=>v+s[k],0)/r.final.length),minimumSweptSeparation:r.minimumSweptSeparation,counts:r.counts});}
 output.allocationPass=output.primaryPass&&output.reuseExecuted&&output.trials.every(x=>x.complete)&&output.convergence.every(x=>x.pass)&&output.eventErrors.every(x=>x.postRefreshPass);
 output.approximationPass=output.allocationPass&&output.comparisons.every(x=>x.pass)&&output.eventErrors.every(x=>x.pass);
 output.decision=output.approximationPass?'eligible-for-larger-test':output.allocationPass?'missed-declared-targets':'incomplete-diagnostic';
 output.totalJointQueryAttempts=output.descriptive.reduce((s,x)=>s+x.counts.jointQueryAttempts,0);
 output.complete=true;output.peakRSSBytes=peakRSS;output.elapsedMs=performance.now()-began;save('analysis.json',output);console.log(JSON.stringify({complete:true,primaryPass:output.primaryPass,allocationPass:output.allocationPass,approximationPass:output.approximationPass,decision:output.decision,trials:output.trials.length,totalJointQueryAttempts:output.totalJointQueryAttempts}));
}catch(e){output.failure={kind:e.message,activeCase:active?.id??null};save('partial-analysis.json',output,true);if(active){try{save('interrupted-trial.json',active,true);}catch(retention){save('interrupted-trial-summary.json',{id:active.id,initial:active.initial,failure:active.failure,counts:active.counts,end:active.end??null,lastSamples:active.samples.slice(-2),lastStages:active.stages.slice(-4),lastEvents:active.events.slice(-2),totalSamples:active.samples.length,totalStageRecords:active.stages.length,totalEventRecords:active.events.length,retention:'Full active record exceeds reserved evidence capacity; compact prefix/failure record only.'},true);}}console.log(JSON.stringify(output.failure));process.exitCode=1;}
