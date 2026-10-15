'use strict';
// Event-stress driver derived from the frozen causal screen. No imports occur on syntax checking.
const fs=require('fs'),path=require('path'),crypto=require('crypto');
const start=performance.now(),cpu0=process.cpuUsage(),ROOT=__dirname,WS=path.dirname(ROOT),FEAS=path.join(WS,'research-public-reference-feasibility');
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
const read=p=>JSON.parse(fs.readFileSync(p,'utf8'));
const bytes=p=>{if(!fs.existsSync(p))return 0;return fs.readdirSync(p,{withFileTypes:true}).reduce((n,e)=>{const q=path.join(p,e.name);return n+(e.isDirectory()?bytes(q):fs.lstatSync(q).size);},0);};
const phase=process.argv[2],config=read(path.join(ROOT,'config.json')),P=config.phases[phase];
if(!P||process.env.EVENT_STRESS_SUPERVISED!==phase)throw Error('Released supervisor required');
const release=read(path.join(ROOT,`RELEASE-${phase}.json`)),freezePath=path.join(ROOT,'FREEZE.json'),freeze=read(freezePath);
if(release.status!=='RELEASED'||release.phase!==phase||release.freezeSha256!==sha(fs.readFileSync(freezePath))||!Number.isSafeInteger(release.globalRemainingBytes)||release.globalRemainingBytes<P.outputCap+config.supervisorReserve)throw Error('Invalid release');
function verifyFreeze(){for(const f of freeze.files){const p=path.resolve(WS,f.path);if(!p.startsWith(WS+path.sep)||sha(fs.readFileSync(p))!==f.sha256)throw Error('Frozen source changed: '+f.path);}}
verifyFreeze();
if(!fs.existsSync(path.join(ROOT,`execution-${phase}-started.json`)))throw Error('Missing supervisor start');
if(bytes(ROOT)+P.outputCap+config.supervisorReserve>config.combinedBytes)throw Error('Insufficient combined byte allowance');
const OUT=path.join(ROOT,`results-${phase}`);fs.mkdirSync(OUT); // Exclusive one-attempt directory.
const completed=[],comparisons=[],gates=[],sourceBodies=new Map();let active=null,current={phase:'initialization'},witnessCount=0,emergency=false,compatibility=null,compatibilityWork=null,integratorContext=null;
function resource(){const c=process.cpuUsage(cpu0);return {wallSeconds:(performance.now()-start)/1000,cpuSeconds:(c.user+c.system)/1e6,rssBytes:process.memoryUsage().rss};}
function budget(){const r=resource();if(r.wallSeconds>P.cooperativeSeconds||r.cpuSeconds>P.cooperativeSeconds)throw Object.assign(Error('Cooperative resource stop'),{detail:r});}
function write(name,b){if(!Buffer.isBuffer(b))b=Buffer.from(b);const f=path.join(OUT,name),tmp=f+'.partial';if(!f.startsWith(OUT+path.sep))throw Error('Output path');const cap=P.outputCap-(emergency?0:config.phaseFailureReserve);if(bytes(OUT)+b.length>cap||bytes(ROOT)+b.length>config.combinedBytes-config.supervisorReserve)throw Error('Retained byte stop');fs.mkdirSync(path.dirname(f),{recursive:true});const fd=fs.openSync(tmp,'wx');try{fs.writeFileSync(fd,b);fs.fsyncSync(fd);}finally{fs.closeSync(fd);}fs.renameSync(tmp,f);return {path:name,bytes:b.length,sha256:sha(b)};}
function save(name,v){return write(name,JSON.stringify(v,(_k,x)=>typeof x==='number'&&!Number.isFinite(x)?{nonfinite:String(x)}:x)+'\n');}
function saveBounded(name,v,cap){const b=JSON.stringify(v,(_k,x)=>typeof x==='number'&&!Number.isFinite(x)?{nonfinite:String(x)}:x)+'\n';if(Buffer.byteLength(b)>cap)throw Error('Bounded receipt overflow: '+name);return write(name,b);}
function raw(rows){const b=Buffer.alloc(rows.reduce((n,r)=>n+r.length*8,0));let k=0;for(const r of rows)for(const v of r){b.writeDoubleLE(v,k);k+=8;}return b;}
function progress(status){save('progress.json',{status,current:{id:active?.id??null,tick:active?.tick??null,phase:current.phase},completed:completed.map(r=>r.id),validReferenceFiles:completed.filter(r=>r.reference).map(r=>r.reference),exactInternalState:false,meaning:'Last durable progress; partial step state is not claimed',resources:resource()});}
function witness(rows){const f=write(`witnesses/${witnessCount++}.f64`,raw(rows));return {...f,shape:rows.map(r=>r.length),encoding:'little-endian Float64'};}
function verifySources(){for(const [filename,b]of sourceBodies)if(sha(fs.readFileSync(filename))!==sha(b))throw Error('Public source mutation');}
// Hash-checked in-memory CommonJS filesystem. Original source text is unchanged.
function loadClosure(){
 const closure=read(path.join(FEAS,'CLOSURE.json')),virtual=path.join(ROOT,'virtual/implementation'),map=new Map(),cache=new Map();
 for(const f of closure.functional_files){const p=path.resolve(WS,f.local_bytes_path),b=fs.readFileSync(p);if(b.length!==f.bytes||sha(b)!==f.sha256)throw Error('Closure identity');sourceBodies.set(p,b);const suffix=f.required_path.split('/implementation/')[1];if(!suffix)throw Error('Closure path');map.set(path.join(virtual,suffix),b.toString('utf8'));}
 function load(filename){if(cache.has(filename))return cache.get(filename).exports;const body=map.get(filename);if(body===undefined)throw Error('Unlisted module: '+filename);const m={exports:{}};cache.set(filename,m);
  const req=id=>{if(['fs','path','crypto'].includes(id))return require(id);if(!id.startsWith('.')&&!path.isAbsolute(id))throw Error('Unlisted dependency');return load(path.resolve(path.dirname(filename),id));};
  new Function('exports','require','module','__filename','__dirname',body)(m.exports,req,m,filename,path.dirname(filename));return m.exports;
 }
 process.env.FLOCK_FACTORY_VARIANT='wide';return {M:load(path.join(virtual,'src/exact-aero.cjs')),C:load(path.join(virtual,'src/controller.cjs')),J:load(path.join(virtual,'src/joint-step.cjs')),G:load(path.join(virtual,'snapshot/outputs/milestone-31-source/geometry.cjs')),closure};
}
let M,C,J,G,B,compare,gate,keys,makeMonitor,createHistory,scalar,makeObserver;let initialIdentity=null;const initials=new Map(),baselineChecked=new Set();
function run(seed,kind,h){
 const end=P.endTick,air=kind==='J'?null:config.airTicks,id=`s${seed}-${kind}${h}${air?'-a'+air:''}`;
 const monitor=makeMonitor(M,B,G),observer=makeObserver(M),field=M.createEvaluator({variant:'lean'}),history=kind==='J'?null:createHistory(kind,air);
 let Y=initials.get(seed).map(s=>s.slice()),commands=null,tick=0,last,stageTick=null;
 const historyEvidence=()=>{const q=history?.snapshot();return q?{historyCurrent:q.current,historyPrevious:q.previous,historyTick:q.tick}:{};};
 integratorContext=null;current={phase:'arm admission',id,tick:0,state:Y};
 if(h*config.tickSeconds/M.F.P.motorTau>1/16||Y.some(r=>r.slice(13).some(v=>v<0)))throw Error('Motor positivity step domain');
 const counter=()=>({fields:0,candidates:0,guardRotorChecks:0,supportTests:0,exactZeroPairs:0,evaluatedRotorKernels:0,contributions:0});
 const d={id,seed,kind,h,air,endTick:end,complete:false,common:[],controls:[],diag:[],referenceRows:[],tick:0,work:{steps:0,derivatives:0,productionFields:0,auxiliaryFields:0,baselineFields:0,productionAttempts:0,auxiliaryAttempts:0,baselineAttempts:0,controllerAttempts:0,controllerSuccessfulReturns:0,controllers:0,stageCallbacks:0,nonzeroFields:0,maxInflow:0,production:counter(),diagnostic:counter()},monitor:monitor.x,eventExposure:observer.x,predictor:history?.stats??null,stageExposure:{minimumRawNominalMotor:null,minimumRawMotorWitness:null,zeroWindVehicleStages:0,nonzeroWindVehicleStages:0},lag:{maxInflowGap:0,maxForceGap:0,maxRollPitchGap:0,maxAgeTicks:0},initialSha256:sha(raw(Y))};active=d;
 function evaluate(geometry,role){
  d.work[role==='production'?'productionAttempts':'auxiliaryAttempts']++;
  const f=field(geometry),c=d.work[role];c.fields++;for(const k of Object.keys(c))if(k!=='fields')c[k]+=f.counters[k];
  if(role==='production'){
   d.work.productionFields++;d.work.nonzeroFields+=+(f.maximumInflow>0);d.work.maxInflow=Math.max(d.work.maxInflow,f.maximumInflow);
   if(!baselineChecked.has(seed)){const before=raw(geometry);d.work.baselineAttempts++;const b=M.A.fields(geometry,'sum-rotor');d.work.baselineFields++;if(!before.equals(raw(geometry))||!raw(f.winds).equals(raw(b.winds)))throw Error('Lean/production arithmetic or mutation mismatch');baselineChecked.add(seed);}
  }else d.work.auxiliaryFields++;
  return f;
 }
 function record(){if(tick%config.commonTicks===0)d.common.push(Y.flat());if(kind==='J'&&h===32&&tick%config.controlTicks===0)d.referenceRows.push(Y.flat());}
 function diagnostic(){
  const before=raw(Y),snap=history?JSON.stringify(history.snapshot()):null,fresh=evaluate(Y,'diagnostic').winds;
  const incoming=history?history.supply(tick,'diagnostic',{phase:'incoming diagnostic'}):fresh,age=history?tick-history.tick:0,loads=Y.map((s,i)=>M.loads(s,incoming[i]));
  for(let i=0;i<config.count;i++){const f=M.loads(Y[i],fresh[i]);for(let r=0;r<4;r++)d.lag.maxInflowGap=Math.max(d.lag.maxInflowGap,Math.abs(incoming[i][r]-fresh[i][r]));d.lag.maxForceGap=Math.max(d.lag.maxForceGap,Math.hypot(...loads[i].force.map((v,k)=>v-f.force[k])));d.lag.maxRollPitchGap=Math.max(d.lag.maxRollPitchGap,Math.hypot(...loads[i].moment.slice(0,2).map((v,k)=>v-f.moment[k])));}
  if(!before.equals(raw(Y))||(history&&snap!==JSON.stringify(history.snapshot())))throw Error('Diagnostic mutated state/history');
  d.lag.maxAgeTicks=Math.max(d.lag.maxAgeTicks,age);d.diag.push({tick,fresh,incoming,age,loads});monitor.clearance(Y);
 }
 current={phase:'initial endpoint',id,state:Y};last=monitor.sample(Y,{tick,role:'endpoint'});observer.sample(Y,{tick,role:'endpoint'},last);record();
 while(tick<end){
  budget();if(end%h||config.controlTicks%h||config.commonTicks%h||(air&&air%h))throw Error('Tick alignment');
  current={phase:'events',id,tick,state:Y,commands,...historyEvidence()};
  if(history&&tick%air===0){const before=raw(Y);history.accept(evaluate(Y,'production').winds,tick);if(!before.equals(raw(Y)))throw Error('Scheduled field mutated state');}
  if(tick%config.controlTicks===0){const before=raw(Y);d.work.controllerAttempts++;const c=C.controller(Y,tick);d.work.controllerSuccessfulReturns++;if(!before.equals(raw(Y)))throw Error('Controller input mutation');monitor.controls(c);observer.controls(c,Y);commands=c.commands;if(commands.some(r=>r.length!==4||r.some(v=>!Number.isFinite(v)||v<0)))throw Error('Nonnegative commands required');d.controls.push({tick,commands,signature:c.event.branchSignatureSha256});d.work.controllers++;}
  if(tick===0)diagnostic(); // Initial approximate field exists; no fictitious incoming history.
  const old=Y,input=raw(Y),u=raw(commands),histBefore=history?JSON.stringify(history.snapshot()):null,samples=[last],trial=[];
  current={phase:'physics',id,tick,state:Y,commands,...historyEvidence(),trial};integratorContext={kind:'jointStep',id,startTick:tick,hTicks:h,returned:false};
  Y=J.jointStep(Y,commands,h*config.tickSeconds,{
   beforeStage:q=>{
    stageTick=tick+q.fraction*h;current={phase:'RK stage',id,tick:stageTick,stage:q.stage,state:old,raw:q.raw,geometry:q.geometry,commands,...historyEvidence(),trial};
    trial.push({raw:q.raw,geometry:q.geometry});const location={tick:stageTick,role:'stage',stage:q.stage},sample=monitor.sample(q.geometry,location);samples.push(sample);observer.sample(q.geometry,location,sample);
    for(let i=0;i<q.raw.length;i++){const s=q.raw[i];monitor.x.maxRawNormDefect=Math.max(monitor.x.maxRawNormDefect,Math.abs(Math.hypot(...s.slice(6,10))-1));if(s.slice(13).some(v=>v<0))throw Error('Negative raw-stage nominal motor');for(let r=0;r<4;r++)if(d.stageExposure.minimumRawNominalMotor===null||s[13+r]<d.stageExposure.minimumRawNominalMotor){d.stageExposure.minimumRawNominalMotor=s[13+r];d.stageExposure.minimumRawMotorWitness={tick:stageTick,stage:q.stage,receiver:i,rotor:r};}}
   },
   field:geometry=>{
    d.work.stageCallbacks++;if(stageTick===null)throw Error('Missing stage clock');
    const result=history?{winds:history.supply(stageTick,'stage',{stage:current.stage})}:evaluate(geometry,'production');stageTick=null;
    for(const row of result.winds)row.every(x=>x===0)?d.stageExposure.zeroWindVehicleStages++:d.stageExposure.nonzeroWindVehicleStages++;
    return result;
   },afterDerivative:()=>{d.work.derivatives++;},
   onProjection:q=>{for(const v of q.projectionSizes)monitor.x.maxProjection=Math.max(monitor.x.maxProjection,v);}
  });
  integratorContext.returned=true;
  if(!input.equals(raw(old))||!u.equals(raw(commands))||(history&&histBefore!==JSON.stringify(history.snapshot())))throw Error('Step input/history mutation');
  tick+=h;d.tick=tick;d.work.steps++;current={phase:'accepted endpoint',id,tick,state:Y,previous:old,commands,...historyEvidence(),trial};monitor.safe(old,Y);last=monitor.sample(Y,{tick,role:'endpoint'});samples.push(last);monitor.jump(samples);observer.sample(Y,{tick,role:'endpoint'},last);record();if(tick%config.controlTicks===0)diagnostic();if(d.work.steps%128===0)progress('RUNNING');
 }
 const expectedFields=kind==='J'?4*end/h:end/air;
 if(d.work.productionAttempts!==d.work.productionFields||d.work.auxiliaryAttempts!==d.work.auxiliaryFields||d.work.baselineAttempts!==d.work.baselineFields||d.work.steps!==end/h||d.work.derivatives!==4*config.count*end/h||d.work.stageCallbacks!==4*end/h||d.work.productionFields!==expectedFields||d.work.production.fields!==expectedFields||d.work.auxiliaryFields!==end/config.controlTicks+1||d.work.diagnostic.fields!==d.work.auxiliaryFields||d.work.controllerAttempts!==d.work.controllerSuccessfulReturns||d.work.controllerSuccessfulReturns!==d.work.controllers||d.work.controllers!==end/config.controlTicks||d.common.length!==end/config.commonTicks+1||d.diag.length!==end/config.controlTicks+1)throw Error('Work/coverage mismatch');
 if(history&&(history.stats.stage.vectors!==4*end/h||history.stats.diagnostic.vectors!==end/config.controlTicks+1||history.tick!==end-air||history.stats.stage.startupHoldVectors!==(kind==='P'?4*air/h:0)))throw Error('History coverage mismatch');
 if(observer.x.work.samples!==1+5*end/h||observer.x.work.pairVisits!==(1+5*end/h)*config.count*(config.count-1)*4||observer.x.work.endpointSamples!==1+end/h||observer.x.work.controllerCalls!==end/config.controlTicks||observer.x.work.controllerRows!==config.count*end/config.controlTicks)throw Error('Observer coverage mismatch');
 d.complete=true;d.finalSha256=sha(raw(Y));
 if(kind==='J'&&h===32){const artifact=write(`reference/s${seed}.f64`,raw(d.referenceRows));d.reference={...artifact,shape:[d.referenceRows.length,config.count,17],cadenceTicks:config.controlTicks,encoding:'little-endian Float64'};}
 const report={id,seed,kind,h,air,endTick:end,complete:true,initialSha256:d.initialSha256,finalSha256:d.finalSha256,work:d.work,exposure:d.monitor,eventExposure:d.eventExposure,stageExposure:d.stageExposure,predictor:d.predictor,lag:d.lag,reference:d.reference??null,evaluationCountMeaning:'Attempts include the failing invocation; field and kernel counters describe successful evaluator returns only',scope:'Own-state public model; matched scheduled fields, not total runtime equivalence'};
 save(`runs/${id}.json`,report);completed.push(report);progress('RUNNING');verifySources();active=null;return d;
}
function compatibilityCheck(){
 compatibilityWork={fieldAttempts:0,fieldSuccessfulReturns:0,controllerAttempts:0,controllerSuccessfulReturns:0};
 const closure=read(path.join(FEAS,'CLOSURE.json')),cp=path.resolve(WS,closure.compatibility_input.path),cb=fs.readFileSync(cp);
 if(sha(cb)!==closure.compatibility_input.sha256)throw Error('Public compatibility input identity');
 const initial=B.initial(4301,config.count);if(128*config.tickSeconds/M.F.P.motorTau>1/16||initial.some(r=>r.slice(13).some(v=>v<0)))throw Error('Compatibility motor domain');if(!raw(initial).equals(cb.subarray(0,2176)))throw Error('Public initial compatibility');
 current={phase:'compatibility field',id:'s4301-compatibility',tick:0,state:initial};
 const field=M.createEvaluator({variant:'lean'}),before=raw(initial);compatibilityWork.fieldAttempts++;const winds=field(initial).winds;compatibilityWork.fieldSuccessfulReturns++;compatibilityWork.controllerAttempts++;const c=C.controller(initial,0);compatibilityWork.controllerSuccessfulReturns++;const commands=c.commands;
 if(!before.equals(raw(initial)))throw Error('Compatibility inputs mutated');
 const fixture={records:5,fieldEvaluations:1,controllerCalls:1,steps:8,derivatives:512,scalarChecks:12,zeroWindVehicles:winds.filter(r=>r.every(x=>x===0)).length,nonzeroWindVehicles:winds.filter(r=>r.some(x=>x!==0)).length,minimumRawNominalMotor:null,worstWrapperDifference:null};
 if(commands.some(r=>r.length!==4||r.some(v=>!Number.isFinite(v)||v<0)))throw Error('Compatibility command domain');
 const paths=[];
 for(const kind of ['legacy','stage']){
  let Y=initial.map(r=>r.slice()),rows=[Y.flat()];const monitor=makeMonitor(M,B,G);let last=monitor.sample(Y,{tick:0,role:'endpoint'});monitor.controls(c);
  for(let step=0;step<4;step++){
   budget();const old=Y,input=raw(Y),u=raw(commands),w=raw(winds),samples=[last];current={phase:'compatibility '+kind,tick:step*128,state:Y,commands,winds};integratorContext={kind,id:'s4301-compatibility',startTick:step*128,hTicks:128,returned:false};
   if(kind==='legacy')Y=Y.map((s,i)=>M.integrate(s,commands[i],128*config.tickSeconds,winds[i],'sum-rotor'));
   else Y=J.jointStep(Y,commands,128*config.tickSeconds,{field:()=>({winds}),beforeStage:q=>{current={phase:'compatibility stage',tick:(step+q.fraction)*128,stage:q.stage,raw:q.raw,geometry:q.geometry,state:old,commands,winds};samples.push(monitor.sample(q.geometry,{tick:(step+q.fraction)*128,role:'stage'}));for(const s of q.raw)for(const f of s.slice(13)){if(f<0)throw Error('Compatibility raw motor domain');if(fixture.minimumRawNominalMotor===null||f<fixture.minimumRawNominalMotor)fixture.minimumRawNominalMotor=f;}}});
   integratorContext.returned=true;
   if(!input.equals(raw(old))||!u.equals(raw(commands))||!w.equals(raw(winds)))throw Error('Compatibility mutation');monitor.safe(old,Y);last=monitor.sample(Y,{tick:(step+1)*128,role:'endpoint'});samples.push(last);monitor.jump(samples);rows.push(Y.flat());
  }
  paths.push(rows);
 }
 const legacy=raw(paths[0]),staged=raw(paths[1]);if(!legacy.equals(cb.subarray(0,legacy.length)))throw Error('Public four-step compatibility mismatch');
 let maximum=0,worst=null;for(let t=0;t<5;t++)for(let k=0;k<272;k++){const v=Math.abs(paths[0][t][k]-paths[1][t][k]);if(!Number.isFinite(v))throw Error('Nonfinite wrapper comparison');if(v>maximum){maximum=v;worst={tick:t*128,drone:Math.floor(k/17),component:k%17,legacy:paths[0][t][k],stage:paths[1][t][k]};}}
 const scalarRows=[];for(const [name,prev,cur,expected]of [['constant',2,2,[2,2,2]],['affine',1,2,[2,2.5,3]],['declining',3,1,[1,0,0]],['startup',null,2,[2,2,2]]])for(const [i,a]of [0,.5,1].entries()){const r=scalar(cur,prev,a);if(r.value!==expected[i]||(name==='declining'&&r.raw!==[1,0,-1][i]))throw Error('Predictor scalar fixture');scalarRows.push({name,alpha:a,...r});}
 compatibility={...fixture,work:compatibilityWork,passed:maximum<=config.compatibilityTolerance,legacyBitEqual:true,wrapperBitEqual:legacy.equals(staged),maximumWrapperComponentDifference:maximum,worstWrapperDifference:worst,wrapperTolerance:config.compatibilityTolerance,fixtureOnly:true,legacySha256:sha(legacy),stageSha256:sha(staged),referenceSha256:closure.compatibility_input.sha256,scalarRows};
 save('compatibility.json',compatibility);if(!compatibility.passed)throw Error('Stage wrapper compatibility tolerance');
}

function comparison(a,b){const c=compare(a,b,witness);const f=save(`comparisons/${a.id}--${b.id}.json`,c);comparisons.push({a:c.a,b:c.b,file:f,maximum:c.maximum});return c;}
function stopGate(name,result){gates.push({name,...result});save('gates.json',gates);if(!result.passed)throw Object.assign(Error(name),{referenceStop:true,detail:result});}
function compactFailure(e){
 const matrices=[],seen=new Map(),meta=[];let matrixBytes=0;
 function add(label,a,required=false){
  if(!Array.isArray(a)||!a.length||!Array.isArray(a[0]))return null;if(seen.has(a))return {matrix:seen.get(a)};
  if(a.some(r=>!Array.isArray(r)||r.some(x=>typeof x!=='number')))return null;const b=raw(a);
  if(matrixBytes+b.length>20000){if(required)throw Error('Required failure matrix overflow');return null;}
  const index=meta.length;meta.push({label,offset:matrixBytes,shape:a.map(r=>r.length),bytes:b.length,sha256:sha(b),finite:a.every(r=>r.every(Number.isFinite))});seen.set(a,index);matrices.push(b);matrixBytes+=b.length;return {matrix:index};
 }
 // Exact source-provided failure state always precedes optional context.
 for(const k of ['raw','geometry','commands','field','derivatives'])add('error.'+k,e.stageEvidence?.[k],true);add('endpoint.raw',e.endpointEvidence?.raw,true);
 let finiteJumpWitness=null;
 if(e.message==='Unresolved sampled finite-jump risk'&&integratorContext?.kind==='jointStep'&&current.previous&&current.trial?.length===4&&Number.isInteger(e.detail?.pairIndex)){
  const n=current.state.length,k=e.detail.pairIndex,i=Math.floor(k/(4*(n-1))),r=Math.floor((k%(4*(n-1)))/(n-1)),slot=k%(n-1),j=slot>=i?slot+1:slot;
  const samples=[current.previous,...(current.trial||[]).map(q=>q.geometry),current.state];
  if(i<0||i>=n||r<0||r>=4||j>=n||samples.length!==6||samples.some(Y=>!Y?.[i]||!Y?.[j]))throw Error('Missing decisive jump samples');
  finiteJumpWitness={pairIndex:k,receiver:i,rotor:r,source:j,states:add('finiteJump.receiverSourceBySample',samples.flatMap(Y=>[Y[i],Y[j]]),true),samples:[{role:'previous endpoint',tick:integratorContext.startTick},...[0,.5,.5,1].map((fraction,k)=>({role:'normalized stage',stage:k+1,fraction,tick:integratorContext.startTick+fraction*integratorContext.hTicks})),{role:'accepted endpoint',tick:current.tick}],meaning:'Two rows per sample: receiver then source; same ordered pair used by the original conservative guard'};
 }
 // For post-step/observer/controller failures, preserve the accepted input,
 // previous endpoint and actual supply history before optional trial tapes.
 if(!e.stageEvidence)for(const k of ['state','previous','commands','winds','historyCurrent','historyPrevious'])add(k,current[k],true);
 function packTuple(label,q){if(q===null)return null;const {receiverState,sourceState,...other}=q;if([receiverState,sourceState].some(s=>s.length!==17||!s.every(Number.isFinite)))throw Error('Nonfinite observer state');return {...other,states:add(label+'.receiverSource',[receiverState,sourceState],true),stateRowOrder:['receiver','source']};}
 function packWall(label,q){if(q===null)return null;const {state,actual,velocity,commands,walls,...other}=q;if([state,...walls.map(w=>[...w.n,w.lower])].some(s=>!s.every(Number.isFinite)))throw Error('Nonfinite observer wall geometry');return {...other,stateVectors:add(label+'.stateActualVelocityCommands',[state,actual,velocity,commands],true),stateVectorRowOrder:['state','actual','velocity','commands'],wallObstacleIds:walls.map(w=>w.obstacle),wallConstraints:walls.length?add(label+'.wallNormalsAndLower',walls.map(w=>[...w.n,w.lower]),true):null,wallConstraintColumns:['nx','ny','nz','lower']};}
 let eventExposure=null;
 if(active){const v=active.eventExposure;eventExposure={work:v.work,nearestFarStart:packTuple('observer.nearestFarStart',v.nearestFarStart),nearestJumpAnnulus:packTuple('observer.nearestJumpAnnulus',v.nearestJumpAnnulus),wallCounts:Object.fromEntries(Object.entries(v.walls).filter(([_k,z])=>typeof z==='number')),firstListedWall:packWall('observer.firstListedWall',v.walls.firstListed),firstWallResponse:packWall('observer.firstWallResponse',v.walls.firstResponse),support:Object.fromEntries(Object.entries(v.support).map(([k,z])=>[k,{...z,first:z.first?{...z.first,previous:packTuple('observer.'+k+'.previous',z.first.previous),current:packTuple('observer.'+k+'.current',z.first.current)}:null}])),arrayStorage:'Numeric witness arrays use matrix indices into this failure artifact; no quantization',incompleteArmWitnessPolicy:'Both nearest joint tuples and observed first wall/support witnesses retained; later worst-wall bodies omitted for failure reserve'};}
 for(const k of ['raw','geometry','state','previous','commands','winds','historyCurrent','historyPrevious'])add(k,current[k]);for(const [i,t]of (current.trial||[]).entries()){add('trial'+i+'raw',t.raw);add('trial'+i+'geometry',t.geometry);}
 const artifact=matrices.length?write('failure-state.f64',Buffer.concat(matrices)):null;let detail=e.detail??null;if(Buffer.byteLength(JSON.stringify(detail))>2500)detail={omitted:'Oversized detail; bounded state evidence retained'};
 saveBounded('failure.json',{status:e.referenceStop?'REFERENCE_UNQUALIFIED':'STOPPED',message:e.message,detail,integratorContext,authoritativeIntegratorFailure:e.stageEvidence?{kind:'stage',stage:e.stageEvidence.stage,fraction:e.stageEvidence.fraction,tick:integratorContext?integratorContext.startTick+e.stageEvidence.fraction*integratorContext.hTicks:null,failingDrone:e.stageEvidence.failingDrone,guard:{name:e.stageEvidence.guard.name,message:e.stageEvidence.guard.message,detailReference:'detail'}}:e.endpointEvidence?{kind:'endpoint projection',tick:integratorContext?integratorContext.startTick+integratorContext.hTicks:null,guard:{name:e.endpointEvidence.guard.name,message:e.endpointEvidence.guard.message,detailReference:'detail'}}:null,currentCallbackContextMayPrecedeFailure:!!e.stageEvidence,current:{phase:current.phase,id:current.id,tick:current.tick,stage:current.stage,vehicle:current.vehicle,historyTick:current.historyTick},finiteJumpWitness,compatibilityWork,active:active?{id:active.id,tick:active.tick,work:active.work,eventExposure}:null,artifact,matrices:meta,encoding:'little-endian IEEE754 binary64; raw failing NaN/Infinity preserved; finite flag is per matrix',exactFailedIntegratorState:!!(e.stageEvidence?.raw||e.endpointEvidence?.raw),retainedStateMeaning:'Exact synchronized raw stage/projection input when identified; otherwise last available input/accepted sample, not a hidden legacy failure stage',legacyInternalStageUnavailable:current.phase==='compatibility legacy',completed:completed.map(r=>r.id),resources:resource()},16500);
}
function saveGate(name,result){gates.push({name,...result});save('gates.json',gates);return result.passed;}
let status='STOPPED',decision='NOT_EVALUATED',efficacy=null,attribution=null,workTotals=null,eventQualification=null;
try{
 save('started.json',{experimentId:config.experimentId,phase,freezeSha256:release.freezeSha256,config,claim:'Numerical mechanism only; equal field counts are not equal total work'});
 ({M,C,J,G}=loadClosure());B=C.B;
 ({compare,gate,keys}=require('../research-public-reference-campaign/compare.cjs'));
 makeMonitor=require('../research-public-reference-campaign/monitor.cjs');({createHistory,scalar}=require('../research-causal-airflow-predictor/predict-stage.cjs'));
 makeObserver=require('./observe-events.cjs');
 compatibilityCheck();
 for(const seed of config.seeds){const base=B.initial(seed,config.count),identity=sha(raw(base));if(identity!==config.untranslatedInitialSha256)throw Error('Untranslated initial identity mismatch');const shifted=base.map(s=>s.map((v,k)=>k===0?v+config.translation[0]:v));initialIdentity={seed,untranslatedSha256:identity,translatedSha256:sha(raw(shifted)),translation:config.translation,nonPositionComponentsUnchanged:base.every((s,i)=>s.slice(3).every((v,k)=>Object.is(v,shifted[i][k+3])))};if(!initialIdentity.nonPositionComponentsUnchanged)throw Error('Translation altered other state');save('initial-identity.json',initialIdentity);initials.set(seed,shifted);}
 const refs=new Map(),jointNoise=new Map();
 for(const seed of config.seeds){
  const js=config.jointSteps.map(h=>run(seed,'J',h)),coarse=comparison(js[0],js[1]),fine=comparison(js[1],js[2]);
  stopGate('joint-convergence-'+seed,gate(fine,config.smallCaps,coarse,config.floors,config.jointReduction));
  stopGate('joint-airflow-exposure-'+seed,{passed:js.every(d=>d.work.nonzeroFields>0),nonzeroFields:js.map(d=>d.work.nonzeroFields)});
  refs.set(seed,js[2]);jointNoise.set(seed,fine);
 }
 // The single developmental case qualified; collect all approximation arms before scoring their errors.
 const arms=new Map();for(const seed of config.seeds)for(const kind of ['H','P'])for(const h of config.approxSteps)arms.set(`${seed}-${kind}-${h}`,run(seed,kind,h));
 const effects=[],noiseRows=[],physicsGates=[],countGates=[],exposureGates=[];
 for(const seed of config.seeds){
  const errors={},physics={};for(const kind of ['H','P']){
   const coarse=arms.get(`${seed}-${kind}-16`),fine=arms.get(`${seed}-${kind}-8`);physics[kind]=comparison(coarse,fine);errors[kind]=comparison(fine,refs.get(seed));
   const q=gate(physics[kind],config.smallCaps);physicsGates.push(q.passed);saveGate(`physical-h-${seed}-${kind}`,q);
   const exposure={passed:coarse.work.nonzeroFields>0&&fine.work.nonzeroFields>0,nonzeroFields:[coarse.work.nonzeroFields,fine.work.nonzeroFields]};exposureGates.push(exposure.passed);saveGate(`airflow-exposure-${seed}-${kind}`,exposure);
   for(const k of keys){const signal=errors[kind].maximum[k],uncertainty=Math.max(jointNoise.get(seed).maximum[k],physics[kind].maximum[k]),belowFloor=signal<=config.floors[k];noiseRows.push({seed,kind,key:k,signal,uncertainty,belowFloor,passed:belowFloor?uncertainty<=config.floors[k]:uncertainty<=config.uncertaintyFraction*signal});}
  }
  comparison(arms.get(`${seed}-P-8`),arms.get(`${seed}-H-8`));
  for(const h of config.approxSteps){const a=arms.get(`${seed}-H-${h}`),b=arms.get(`${seed}-P-${h}`),rows=['steps','derivatives','productionFields','auxiliaryFields','productionAttempts','auxiliaryAttempts','controllerAttempts','controllerSuccessfulReturns','controllers','stageCallbacks'].map(k=>({key:k,zoh:a.work[k],predictor:b.work[k],passed:a.work[k]===b.work[k]}));const q={passed:rows.every(r=>r.passed),rows,excludedFromEquality:'kernel/pair visits, predictor arithmetic and runtime may differ'};countGates.push(q.passed);saveGate(`matched-counts-${seed}-${h}`,q);}
  for(const k of keys){const zoh=errors.H.maximum[k],predictor=errors.P.maximum[k],baselineAboveFloor=zoh>config.floors[k];effects.push({seed,key:k,zoh,predictor,ratio:zoh===0?null:predictor/zoh,baselineAboveFloor,baselineWithinOuter:zoh<=config.outerCaps[k],predictorWithinOuter:predictor<=config.outerCaps[k],relativeTarget:baselineAboveFloor?config.improvementFraction*zoh:config.floors[k],passed:predictor<=config.outerCaps[k]&&predictor<=(baselineAboveFloor?config.improvementFraction*zoh:config.floors[k]),meaning:baselineAboveFloor?'fourfold target':'below-floor cell; no fourfold claim'});}
 }
 const expected={steps:11000,derivatives:704000,productionFields:7200,auxiliaryFields:357,baselineFields:1,productionAttempts:7200,auxiliaryAttempts:357,baselineAttempts:1,controllerAttempts:350,controllerSuccessfulReturns:350,controllers:350,stageCallbacks:44000};
 workTotals=Object.fromEntries(Object.keys(expected).map(k=>[k,completed.reduce((s,r)=>s+r.work[k],0)]));
 const workGate={passed:completed.length===7&&Object.keys(expected).every(k=>workTotals[k]===expected[k]),expected,observed:workTotals,compatibilityAdditional:{steps:8,derivatives:512,productionFields:1,controllerAttempts:1,controllerSuccessfulReturns:1,controllers:1,scalarChecks:12}};
 saveGate('scientific-total-work',workGate);if(!workGate.passed||countGates.some(x=>!x))throw Error('Work-count integrity failure');
 attribution={passed:physicsGates.every(Boolean)&&noiseRows.every(r=>r.passed),rows:noiseRows};saveGate('resolved-numerical-attribution',attribution);
 const informativeSeeds=config.seeds.map(seed=>({seed,informative:effects.some(r=>r.seed===seed&&r.baselineAboveFloor)}));
 efficacy={passed:effects.every(r=>r.passed),rows:effects,informativeSeeds};saveGate('candidate-target',efficacy);
 if(exposureGates.some(x=>!x))decision='INCONCLUSIVE';
 else if(!attribution.passed)decision='NUMERICALLY_UNRESOLVED';
 else if(informativeSeeds.some(r=>!r.informative))decision='INCONCLUSIVE';
 else decision=efficacy.passed?'CANDIDATE_PROMISING_FOR_SEPARATE_REVIEW':'CANDIDATE_TARGET_FAILED';
 const required=[refs.get(config.seeds[0]),arms.get(`${config.seeds[0]}-H-8`),arms.get(`${config.seeds[0]}-P-8`)];
 const eventRows=required.map(d=>({id:d.id,wallResponseCount:d.eventExposure.walls.responseCount,radialTransitions:d.eventExposure.support.radial.count,axialTransitions:d.eventExposure.support.axial.count,passed:d.eventExposure.walls.responseCount>0&&(d.eventExposure.support.radial.count+d.eventExposure.support.axial.count)>0}));
 eventQualification={passed:eventRows.every(r=>r.passed),rows:eventRows,appliesOnlyAfterNumericalQualification:decision==='CANDIDATE_PROMISING_FOR_SEPARATE_REVIEW',meaning:'Strict sampled wall response plus eligible accepted-endpoint C1 transition in each required arm; no continuous event localization'};saveGate('event-exposure',eventQualification);
 if(decision==='CANDIDATE_PROMISING_FOR_SEPARATE_REVIEW'&&!eventQualification.passed)decision='EVENT_EXPOSURE_INSUFFICIENT';
 verifyFreeze();verifySources();budget();status='COMPLETE';
}catch(e){
 emergency=true;try{compactFailure(e);}catch(writeError){try{save('failure-minimal.json',{message:e.message,retentionError:writeError.message,current:{phase:current.phase,id:current.id,tick:current.tick},resources:resource()});}catch(_){process.stderr.write('Failure receipt could not be persisted\n');}}
 status=e.referenceStop?'REFERENCE_UNQUALIFIED':'STOPPED';decision='NOT_EVALUATED';process.exitCode=2;
}finally{
 emergency=true;try{verifyFreeze();verifySources();}catch(e){status='SOURCE_CHANGED';decision='NOT_EVALUATED';process.exitCode=2;}
 const expected=config.seeds.flatMap(seed=>[...config.jointSteps.map(h=>`s${seed}-J${h}`),...['H','P'].flatMap(k=>config.approxSteps.map(h=>`s${seed}-${k}${h}-a${config.airTicks}`))]);
 try{if(status!=='COMPLETE')saveBounded('summary.json',{experimentId:config.experimentId,status,decision,phase,endTick:P.endTick,freezeSha256:release.freezeSha256,completed:completed.map(r=>r.id),skipped:expected.filter(id=>!completed.some(r=>r.id===id)),referenceFiles:completed.filter(r=>r.reference).map(r=>r.reference),comparisonFiles:comparisons.map(c=>c.file.path),compatibilityFile:compatibility?'compatibility.json':null,gatesFile:gates.length?'gates.json':null,failureFile:fs.existsSync(path.join(OUT,'failure.json'))?'failure.json':'failure-minimal.json',scope:'Compact failure summary; completed run metrics, paired comparisons and witnesses remain in their existing files. No candidate qualification.'},1500);else save('summary.json',{experimentId:config.experimentId,status,decision,eligibleForSeparateReview:status==='COMPLETE'&&decision==='CANDIDATE_PROMISING_FOR_SEPARATE_REVIEW',phase,endTick:P.endTick,compatibility,completed:completed.map(r=>r.id),skipped:expected.filter(id=>!completed.some(r=>r.id===id)),comparisons,gates:gates.map(g=>({name:g.name,passed:g.passed})),efficacy,attribution,eventQualification,initialIdentity,workTotals,observerTotals:completed.reduce((out,r)=>{for(const [k,v]of Object.entries(r.eventExposure.work))out[k]=(out[k]||0)+v;return out;},{}),resources:resource(),retainedBytesBeforeSummary:bytes(OUT),referenceFiles:completed.filter(r=>r.reference).map(r=>r.reference),claim:'Developmentally selected translated case; genuine own-state public Boids. Case/horizon-specific numerical mechanism only, sampled exposure not continuous safety; earlier outcomes unchanged, no physical accuracy/order/speedup/novelty or automatic extension.'});}catch(e){process.stderr.write('Summary retention failure: '+e.message+'\n');process.exitCode=3;}
 try{progress(status);}catch(e){process.stderr.write('Progress retention failure: '+e.message+'\n');process.exitCode=3;}
 process.stdout.write(JSON.stringify({experimentId:config.experimentId,status,decision,completed:completed.length,resources:resource()})+'\n');
}
