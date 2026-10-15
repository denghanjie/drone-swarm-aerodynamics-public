'use strict';
// Research driver. Reading/checking this file does not import the model.
const fs=require('fs'),path=require('path'),crypto=require('crypto');
const start=performance.now(),cpu0=process.cpuUsage(),ROOT=__dirname,WS=path.dirname(ROOT),FEAS=path.join(WS,'research-public-reference-feasibility');
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
const read=p=>JSON.parse(fs.readFileSync(p,'utf8'));
const bytes=p=>{if(!fs.existsSync(p))return 0;return fs.readdirSync(p,{withFileTypes:true}).reduce((n,e)=>{const q=path.join(p,e.name);return n+(e.isDirectory()?bytes(q):fs.lstatSync(q).size);},0);};
const phase=process.argv[2],config=read(path.join(ROOT,'config.json')),P=config.phases[phase];
if(!P||process.env.REFERENCE_SUPERVISED!==phase)throw Error('Released supervisor required');
const release=read(path.join(ROOT,`RELEASE-${phase}.json`)),freezePath=path.join(ROOT,'FREEZE.json'),freeze=read(freezePath);
if(release.status!=='RELEASED'||release.phase!==phase||release.freezeSha256!==sha(fs.readFileSync(freezePath))||!Number.isSafeInteger(release.globalRemainingBytes)||release.globalRemainingBytes<P.outputCap+config.supervisorReserve)throw Error('Invalid release');
function verifyFreeze(){for(const f of freeze.files){const p=path.resolve(WS,f.path);if(!p.startsWith(WS+path.sep)||sha(fs.readFileSync(p))!==f.sha256)throw Error('Frozen source changed: '+f.path);}}
verifyFreeze();
if(phase==='extension'){const q=path.join(ROOT,'results-qualification/summary.json'),s=read(q),rp=path.join(ROOT,'execution-qualification-receipt.json'),r=read(rp);if(s.status!=='COMPLETE'||s.eligibleForExtension!==true||sha(fs.readFileSync(q))!==release.qualificationSummarySha256||r.returncode!==0||r.reason!==null||r.timedout||sha(fs.readFileSync(rp))!==release.qualificationReceiptSha256)throw Error('Qualification prerequisite');}
if(!fs.existsSync(path.join(ROOT,`execution-${phase}-started.json`)))throw Error('Missing supervisor start');
if(bytes(ROOT)+bytes(FEAS)+P.outputCap+config.supervisorReserve>config.combinedBytes)throw Error('Insufficient combined byte allowance');
const OUT=path.join(ROOT,`results-${phase}`);fs.mkdirSync(OUT); // Exclusive one-attempt directory.
const completed=[],comparisons=[],gates=[],sourceBodies=new Map();let active=null,current={phase:'initialization'},witnessCount=0,emergency=false,compatibility=null;
function resource(){const c=process.cpuUsage(cpu0);return {wallSeconds:(performance.now()-start)/1000,cpuSeconds:(c.user+c.system)/1e6,rssBytes:process.memoryUsage().rss};}
function budget(){const r=resource();if(r.wallSeconds>P.cooperativeSeconds||r.cpuSeconds>P.cooperativeSeconds)throw Object.assign(Error('Cooperative resource stop'),{detail:r});}
function write(name,b){if(!Buffer.isBuffer(b))b=Buffer.from(b);const f=path.join(OUT,name),tmp=f+'.partial';if(!f.startsWith(OUT+path.sep))throw Error('Output path');const cap=P.outputCap-(emergency?0:config.phaseFailureReserve);if(bytes(OUT)+b.length>cap||bytes(ROOT)+bytes(FEAS)+b.length>config.combinedBytes-config.supervisorReserve)throw Error('Retained byte stop');fs.mkdirSync(path.dirname(f),{recursive:true});const fd=fs.openSync(tmp,'wx');try{fs.writeFileSync(fd,b);fs.fsyncSync(fd);}finally{fs.closeSync(fd);}fs.renameSync(tmp,f);return {path:name,bytes:b.length,sha256:sha(b)};}
function save(name,v){return write(name,JSON.stringify(v,(_k,x)=>typeof x==='number'&&!Number.isFinite(x)?{nonfinite:String(x)}:x)+'\n');}
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
let M,C,J,G,B,compare,gate,keys,makeMonitor;const initials=new Map(),baselineChecked=new Set();
function run(seed,kind,h,air,end=P.endTick,compat=false){
 const id=`s${seed}-${kind}${h}${air?'-a'+air:''}`,monitor=makeMonitor(M,B,G),field=M.createEvaluator({variant:'lean'});
 let Y=initials.get(seed).map(s=>s.slice()),winds=null,heldTick=null,commands=null,tick=0,last;
 const d={id,seed,kind,h,air,endTick:end,complete:false,common:[],controls:[],diag:[],referenceRows:[],tick:0,work:{steps:0,derivatives:0,productionFields:0,auxiliaryFields:0,baselineFields:0,controllers:0,contributions:0,candidates:0,nonzeroFields:0,maxInflow:0},monitor:monitor.x,lag:{maxInflowGap:0,maxForceGap:0,maxRollPitchGap:0,maxAgeTicks:0},initialSha256:sha(raw(Y))};active=d;
 function production(geometry){d.work.productionFields++;const f=field(geometry);d.work.contributions+=f.counters.contributions;d.work.candidates+=f.counters.candidates;d.work.nonzeroFields+=+(f.maximumInflow>0);d.work.maxInflow=Math.max(d.work.maxInflow,f.maximumInflow);
  if(config.seeds.includes(seed)&&!baselineChecked.has(seed)){const b=M.A.fields(geometry,'sum-rotor');d.work.baselineFields++;if(!raw(f.winds).equals(raw(b.winds)))throw Error('Lean/production arithmetic mismatch');baselineChecked.add(seed);}return f;
 }
 function record(){if(tick%128===0)d.common.push(Y.flat());if(kind==='J'&&h===32&&tick%512===0)d.referenceRows.push(Y.flat());}
 function diagnostic(){if(compat)return;d.work.auxiliaryFields++;const fresh=field(Y).winds,incoming=kind==='H'?winds:fresh,age=kind==='H'?tick-heldTick:0,loads=Y.map((s,i)=>M.loads(s,incoming[i]));
  for(let i=0;i<16;i++){const freshLoad=M.loads(Y[i],fresh[i]);for(let r=0;r<4;r++)d.lag.maxInflowGap=Math.max(d.lag.maxInflowGap,Math.abs(incoming[i][r]-fresh[i][r]));d.lag.maxForceGap=Math.max(d.lag.maxForceGap,Math.hypot(...loads[i].force.map((v,k)=>v-freshLoad.force[k])));d.lag.maxRollPitchGap=Math.max(d.lag.maxRollPitchGap,Math.hypot(...loads[i].moment.slice(0,2).map((v,k)=>v-freshLoad.moment[k])));}
  d.lag.maxAgeTicks=Math.max(d.lag.maxAgeTicks,age);d.diag.push({tick,fresh,incoming,age,loads});monitor.clearance(Y);
 }
 current={phase:'initial endpoint',id,state:Y};last=monitor.sample(Y,{tick,role:'endpoint'});record();
 while(tick<end){budget();if(end%h||512%h||128%h||(kind==='H'&&air%h))throw Error('Tick alignment');
  current={phase:'events',id,tick,state:Y,commands,winds};
  if(kind==='H'&&tick%air===0){winds=production(Y).winds;heldTick=tick;}
  if(tick%512===0){const before=raw(Y),c=C.controller(Y,tick);if(!before.equals(raw(Y)))throw Error('Controller input mutation');monitor.controls(c);commands=c.commands;d.controls.push({tick,commands,signature:c.event.branchSignatureSha256});d.work.controllers++;}
  if(tick===0)diagnostic();
  const old=Y,input=raw(Y),u=raw(commands),samples=[last],trial=[];current={phase:'physics',id,tick,state:Y,commands,winds,trial};
  if(kind==='J')Y=J.jointStep(Y,commands,h*config.tickSeconds,{field:production,
   beforeStage:q=>{current={phase:'joint stage',id,tick:tick+q.fraction*h,stage:q.stage,state:old,raw:q.raw,geometry:q.geometry,commands,trial};trial.push({raw:q.raw,geometry:q.geometry});samples.push(monitor.sample(q.geometry,{tick:tick+q.fraction*h,role:'stage',stage:q.stage}));for(const s of q.raw)monitor.x.maxRawNormDefect=Math.max(monitor.x.maxRawNormDefect,Math.abs(Math.hypot(...s.slice(6,10))-1));},
   beforeDerivative:()=>{},afterDerivative:()=>{d.work.derivatives++;},
   onProjection:q=>{for(const v of q.projectionSizes)monitor.x.maxProjection=Math.max(monitor.x.maxProjection,v);}});
  else Y=Y.map((s,i)=>{current.vehicle=i;const y=M.integrate(s,commands[i],h*config.tickSeconds,winds[i],'sum-rotor');d.work.derivatives+=4;return y;});
  if(!input.equals(raw(old))||!u.equals(raw(commands)))throw Error('Step input mutation');
  tick+=h;d.tick=tick;d.work.steps++;current={phase:'accepted endpoint',id,tick,state:Y,previous:old,commands,winds,trial};monitor.safe(old,Y);last=monitor.sample(Y,{tick,role:'endpoint'});samples.push(last);monitor.jump(samples);record();if(tick%512===0)diagnostic();if(d.work.steps%128===0)progress('RUNNING');
 }
 const expectedFields=kind==='J'?4*end/h:end/air;
 if(d.work.steps!==end/h||d.work.derivatives!==4*16*end/h||d.work.productionFields!==expectedFields||d.work.controllers!==end/512||d.common.length!==end/128+1||(!compat&&d.diag.length!==end/512+1))throw Error('Work/coverage mismatch');
 d.complete=true;d.finalSha256=sha(raw(Y));
 if(kind==='J'&&h===32){const artifact=write(`reference/s${seed}.f64`,raw(d.referenceRows));d.reference={...artifact,shape:[d.referenceRows.length,16,17],cadenceTicks:512,encoding:'little-endian Float64'};}
 const report={id,seed,kind,h,air,endTick:end,complete:true,initialSha256:d.initialSha256,finalSha256:d.finalSha256,work:d.work,exposure:d.monitor,lag:d.lag,reference:d.reference??null,scope:'Own-state closed-loop public model; numerical only'};
 save(`runs/${id}.json`,report);completed.push(report);progress('RUNNING');verifySources();active=null;return d;
}
function comparison(a,b){const c=compare(a,b,witness);const f=save(`comparisons/${a.id}--${b.id}.json`,c);comparisons.push({a:c.a,b:c.b,file:f,maximum:c.maximum});return c;}
function stopGate(name,result){gates.push({name,...result});save('gates.json',gates);if(!result.passed)throw Object.assign(Error(name),{gateStop:true,detail:result});}
function compactFailure(e){
 const matrices=[],seen=new Set(),meta=[];function add(label,a){if(!Array.isArray(a)||!a.length||!Array.isArray(a[0])||seen.has(a))return;seen.add(a);if(a.some(r=>!Array.isArray(r)||r.some(x=>typeof x!=='number')))return;const b=raw(a);if(matrices.reduce((n,x)=>n+x.length,0)+b.length>28000)return;meta.push({label,offset:matrices.reduce((n,x)=>n+x.length,0),shape:a.map(r=>r.length),bytes:b.length});matrices.push(b);}
 for(const k of ['state','previous','raw','geometry','commands','winds'])add(k,current[k]);for(const [i,t]of (current.trial||[]).entries()){add('trial'+i+'raw',t.raw);add('trial'+i+'geometry',t.geometry);}for(const k of ['raw','geometry','commands','field','derivatives'])add('error.'+k,e.stageEvidence?.[k]);add('endpoint.raw',e.endpointEvidence?.raw);
 const artifact=matrices.length?write('failure-state.f64',Buffer.concat(matrices)):null;let detail=e.detail??null;if(Buffer.byteLength(JSON.stringify(detail))>2500)detail={omitted:'Oversized detail; bounded state evidence retained'};
 save('failure.json',{status:e.gateStop?'GATE_STOP':'STOPPED',message:e.message,detail,current:{phase:current.phase,id:current.id,tick:current.tick,stage:current.stage,vehicle:current.vehicle},active:active?{id:active.id,tick:active.tick,work:active.work}:null,artifact,matrices:meta,exactFailedIntegratorState:!!(e.stageEvidence?.raw||e.endpointEvidence?.raw),retainedStateMeaning:'Exact joint raw stage/projection input when identified; otherwise last available input/accepted sample, not a hidden failure stage',heldInternalStageUnavailable:current.phase==='physics'&&active?.kind==='H',completed:completed.map(r=>r.id),resources:resource()});
}
let status='STOPPED',eligible=false;
try{
 save('started.json',{phase,freezeSha256:release.freezeSha256,config,claim:'Numerical self-consistency only; not physical truth or recovery of R8'});
 ({M,C,J,G}=loadClosure());B=C.B;({compare,gate,keys}=require('./compare.cjs'));makeMonitor=require('./monitor.cjs');
 for(const seed of [4301,...config.seeds])initials.set(seed,B.initial(seed,16));
 const closure=read(path.join(FEAS,'CLOSURE.json')),cp=path.resolve(WS,closure.compatibility_input.path),cb=fs.readFileSync(cp);if(sha(cb)!==closure.compatibility_input.sha256)throw Error('Public compatibility data identity');
 if(!raw(initials.get(4301)).equals(cb.subarray(0,2176)))throw Error('Public initial-state compatibility mismatch');
 const cr=run(4301,'H',128,512,512,true),prefix=raw(cr.common);if(!prefix.equals(cb.subarray(0,prefix.length)))throw Error('Public four-step compatibility mismatch');compatibility={passed:true,records:5,bytes:prefix.length,sha256:sha(prefix),referenceSha256:closure.compatibility_input.sha256};save('compatibility.json',compatibility);
 const refs=new Map(),jointUncertainty=new Map();
 for(const seed of config.seeds){const js=config.jointSteps.map(h=>run(seed,'J',h,null));const coarse=comparison(js[0],js[1]),fine=comparison(js[1],js[2]);stopGate('joint-convergence-'+seed,gate(fine,config.smallCaps,coarse,config.floors,config.jointReduction));stopGate('joint-airflow-exposure-'+seed,{passed:js.every(d=>d.work.nonzeroFields>0),nonzeroFields:js.map(d=>d.work.nonzeroFields)});refs.set(seed,js[2]);jointUncertainty.set(seed,fine);}
 // Both seeds have passed Gate A before any held matrix arm starts.
 for(const seed of config.seeds){const errors=[],physics=[];for(const air of config.airTicks){const hs=config.heldSteps.map(h=>run(seed,'H',h,air)),p=comparison(hs[0],hs[1]);stopGate(`held-physics-${seed}-${air}`,gate(p,config.smallCaps));physics.push(p);errors.push(comparison(hs[1],refs.get(seed)));}
  for(let j=1;j<errors.length;j++)stopGate(`hold-reduction-${seed}-${config.airTicks[j]}`,gate(errors[j],config.outerCaps,errors[j-1],config.floors,config.holdReduction));
  stopGate('finest-cross-family-'+seed,gate(errors.at(-1),config.outerCaps));
  const rows=errors.flatMap((e,j)=>keys.map(k=>{const signal=e.maximum[k],uncertainty=Math.max(physics[j].maximum[k],jointUncertainty.get(seed).maximum[k]),belowFloor=signal<=config.floors[k];return {airTicks:config.airTicks[j],key:k,signal,uncertainty,belowFloor,passed:belowFloor?uncertainty<=config.floors[k]:uncertainty<=config.uncertaintyFraction*signal};}));stopGate('resolved-airflow-attribution-'+seed,{passed:rows.every(r=>r.passed),rows});
 }
 verifyFreeze();verifySources();budget();status='COMPLETE';eligible=true;
}catch(e){emergency=true;try{compactFailure(e);}catch(writeError){try{save('failure-minimal.json',{message:e.message,retentionError:writeError.message,current:{phase:current.phase,id:current.id,tick:current.tick},resources:resource()});}catch(_){process.stderr.write('Failure receipt could not be persisted\n');}}status=e.gateStop?'GATE_STOP':'STOPPED';process.exitCode=2;}
finally{
 emergency=true;try{verifyFreeze();verifySources();}catch(e){status='SOURCE_CHANGED';eligible=false;process.exitCode=2;}
 try{const expected=config.seeds.flatMap(seed=>[...config.jointSteps.map(h=>`s${seed}-J${h}`),...config.airTicks.flatMap(a=>config.heldSteps.map(h=>`s${seed}-H${h}-a${a}`))]);const summary={status,eligibleForExtension:phase==='qualification'&&status==='COMPLETE'&&eligible,phase,endTick:P.endTick,compatibility,completed:completed.map(r=>r.id),skipped:expected.filter(id=>!completed.some(r=>r.id===id)),comparisons,gates:gates.map(g=>({name:g.name,passed:g.passed})),resources:resource(),retainedBytesBeforeSummary:bytes(OUT),referenceFiles:completed.filter(r=>r.reference).map(r=>r.reference),claim:'Case/horizon-specific numerical agreement only. Incoming-held field sampled before refresh; no physical accuracy, speedup, R8 or historical reference qualification.'};save('summary.json',summary);progress(status);process.stdout.write(JSON.stringify({status,completed:completed.length,phase,resources:resource()})+'\n');}catch(e){process.stderr.write('Terminal output failure: '+e.message+'\n');process.exitCode=3;}
}
