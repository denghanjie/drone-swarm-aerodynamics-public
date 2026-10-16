'use strict';
// No scientific import occurs outside the one frozen candidate invocation.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto'),zlib=require('node:zlib'),os=require('node:os'),cp=require('node:child_process');
const p=path.resolve(process.argv[2]),start=performance.now(),config=JSON.parse(fs.readFileSync(path.join(p,'config.json'),'utf8'));
process.env.FLOCK_FACTORY_VARIANT=config.generation.factoryVariant;
const kernel=require('./kernel.cjs'),sim=require('../../../outputs/milestone-31-source/sim.cjs'),{controls,ownershipSequence}=require('./controls.cjs');
const sha=b=>crypto.createHash('sha256').update(b).digest('hex'),bytes=x=>Buffer.from(x.buffer,x.byteOffset,x.byteLength),exact=(a,b)=>JSON.stringify(a)===JSON.stringify(b),mode={A:'all',L:'lean',T:'typed'};
let outputBytes=0,progress={},maxRSS=0;
for(const dir of ['results','inputs','generation'])fs.mkdirSync(path.join(p,dir),{recursive:true});
function guard(){maxRSS=Math.max(maxRSS,process.memoryUsage().rss);if(maxRSS>config.limits.rssBytes)throw Error('RSS guard exceeded');if(performance.now()-start>config.limits.candidateCooperativeSeconds*1000)throw Error('internal wall guard exceeded');}
function write(rel,b,emergency=false){if(typeof b==='string')b=Buffer.from(b);if(outputBytes+b.length>(emergency?config.limits.scientificBytes:config.limits.normalScientificBytes))throw Error('output guard exceeded');fs.writeFileSync(path.join(p,rel),b,{flag:'wx'});outputBytes+=b.length;return {path:rel,bytes:b.length,sha256:sha(b)};}
const json=(rel,o,emergency=false)=>write(rel,JSON.stringify(o)+'\n',emergency);
function assert(v,label){if(!v)throw Error(label);}
const token=x=>Object.is(x,-0)?'-0':String(x);
const statesFor=positions=>positions.map(v=>[...v,0,0,0,0,0,0,1,0,0,0,...Array(4).fill(kernel.constants.mg/4)]);
const stateBuffer=states=>bytes(Float64Array.from(states.flat()));
function numeric(a,b){if(a===null||b===null)return {length:0,maxAbs:0,maxRel:0,bad:a===b?0:1,pass:a===b,firstMismatch:a===b?null:{nullMismatch:true}};if(a.length!==b.length)return {length:a.length,maxAbs:null,maxRel:null,bad:1,pass:false,firstMismatch:{lengthA:a.length,lengthB:b.length}};let maxAbs=0,maxRel=0,bad=0,firstMismatch=null;for(let i=0;i<a.length;i++){const d=Math.abs(a[i]-b[i]);maxAbs=Math.max(maxAbs,d);maxRel=Math.max(maxRel,d/Math.max(Math.abs(b[i]),Number.MIN_VALUE));if(!Number.isFinite(a[i])||!Number.isFinite(b[i])||!Object.is(a[i],b[i])){bad++;if(!firstMismatch)firstMismatch={index:i,actual:a[i],reference:b[i]};}}return {length:a.length,maxAbs,maxRel,bad,firstMismatch,pass:bad===0};}
function literal(q){return {symbols:[...q.symbols],offsets:[...q.offsets],sources:[...q.src],K:[...q.kv],a:q.aa?[...q.aa]:null,input:q.input,admission:q.admission,graph:kernel.fullGraph(q),certificate:q.certificate,symbolCounts:q.symbolCounts,geometryWork:q.geometryWork,ordinaryLmax:q.ordinaryLmax,assemblyStats:q.assemblyStats??null};}
function canonical(l){const {assemblyStats,...rest}=l;return rest;}
function solutionValues(s){return [...s.y,...s.rotors.flatMap(a=>a.flatMap(r=>[r.alpha,r.x,r.T])),...s.residualMap.y,...s.residualMap.rotors.flatMap(a=>a.flatMap(r=>[r.alpha,r.x,r.T]))];}
function solHash(s){return sha(JSON.stringify({values:solutionValues(s),work:s.work,residualWork:s.residualWork,residualLog:s.residualLog,sourceReceiverMismatch:s.sourceReceiverMismatch,iterations:s.iterations??1,converged:s.converged??true,lastChange:s.lastChange??null}));}
function matrixHash(q){const h=crypto.createHash('sha256');for(const a of [q.offsets,q.src,q.kv,q.aa])if(a)h.update(bytes(a));h.update(JSON.stringify({input:q.input,admission:q.admission,graph:q.graph,symbolCounts:q.symbolCounts,ordinaryLmax:q.ordinaryLmax}));return h.digest('hex');}
function solveCompare(s,ref){const values=numeric(solutionValues(s),solutionValues(ref)),work=exact(s.work,ref.work)&&exact(s.residualWork,ref.residualWork),termination=(s.iterations??1)===(ref.iterations??1)&&(s.converged??true)===(ref.converged??true),residual=Number.isFinite(s.residualLog)&&s.residualLog<=1e-9&&Number.isFinite(s.sourceReceiverMismatch)&&s.sourceReceiverMismatch<=2e-9,exactResidual=Object.is(s.residualLog,ref.residualLog)&&Object.is(s.sourceReceiverMismatch,ref.sourceReceiverMismatch);return {values,work,termination,residual,exactResidual,pass:values.pass&&work&&termination&&residual&&exactResidual};}
function compare(q,s,ref,withSymbols){
 const c={symbols:!withSymbols||q.symbols.equals(ref.q.symbols),offsets:bytes(q.offsets).equals(bytes(ref.q.offsets)),sources:bytes(q.src).equals(bytes(ref.q.src)),K:numeric(q.kv,ref.q.kv),a:numeric(q.aa,ref.q.aa),input:exact(q.input,ref.q.input),admission:exact(q.admission,ref.q.admission),graph:exact(kernel.fullGraph(q),kernel.fullGraph(ref.q)),certificate:exact(q.certificate,ref.q.certificate),symbolCounts:exact(q.symbolCounts,ref.q.symbolCounts),geometryWork:exact(q.geometryWork,ref.q.geometryWork),ordinaryLmax:Object.is(q.ordinaryLmax,ref.q.ordinaryLmax),solution:solveCompare(s,ref.s)};
 c.pass=Object.values(c).every(v=>typeof v==='boolean'?v:v.pass);return c;
}
function persist(id,label,q,s){
 const t0=performance.now(),base=`results/${id}-${label}`,artifacts={};
 if(q.symbols){const gz=zlib.gzipSync(q.symbols,{level:6});assert(gz.length<=config.limits.compressedSymbolsBytesPerBundle,'compressed symbol guard exceeded');artifacts.symbols={...write(base+'-symbols.u8.gz',gz),rawSha256:sha(q.symbols),rawBytes:q.symbols.length};}
 for(const [k,v] of Object.entries({offsets:q.offsets,sources:q.src,K:q.kv,a:q.aa}))if(v)artifacts[k]=write(base+'-'+k+'.bin',bytes(v));
 const doc={id,label,n:q.n,input:q.input,admission:q.admission,graph:kernel.fullGraph(q),certificate:q.certificate,symbolCounts:q.symbolCounts,geometryWork:q.geometryWork,ordinaryLmax:q.ordinaryLmax,assemblyStats:q.assemblyStats??null,artifacts,solutions:{O:s},matrixHash:matrixHash(q),solutionHash:s?solHash(s):null};
 const meta=json(base+'.json',doc);return {meta,totalPersistenceMs:performance.now()-t0,fsync:false};
}
function environment(){const cores=os.cpus(),read=(cmd,args)=>{try{return cp.execFileSync(cmd,args,{encoding:'utf8',timeout:3000}).trim();}catch{return null;}};const power=read('/usr/bin/pmset',['-g']);return {cpuModel:cores[0]?.model??null,logicalCores:cores.length,physicalCores:Number(read('/usr/sbin/sysctl',['-n','hw.physicalcpu']))||null,installedRAMBytes:os.totalmem(),architecture:os.arch(),platform:os.platform(),kernel:os.release(),node:process.version,v8:process.versions.v8,nodeExecutableSha256:sha(fs.readFileSync(process.execPath)),nodeOptionsEmpty:!process.env.NODE_OPTIONS,executionFlagCount:process.execArgv.length,executionFlags:process.execArgv.every(x=>/^--[a-z-]+$/.test(x))?process.execArgv:[],clock:'performance.now monotonic milliseconds',loadAverage:os.loadavg(),lowPowerMode:power?.match(/lowpowermode\s+(\d+)/)?.[1]??null,powerSource:read('/usr/bin/pmset',['-g','batt'])?.match(/Now drawing from '([^']+)'/)?.[1]??null,threads:'one JS worker; runtime helper threads unspecified',pidOmitted:true};}
const evidence={kind:'fresh-boids-typed-assembly',constants:kernel.constants,complete:false,controls:[],ownership:null,generation:[],qualification:[],timings:[],environmentStart:environment()};
function recordTiming(item,method,block,warmup){
 progress={phase:'timing',id:item.id,method,block,warmup};guard();const result=kernel.query(item.states,method,guard),qualified=item.builders[method];
 const rec={sequence:evidence.timings.length,workload:'full',id:item.id,method,block,warmup,totalMs:result.totalMs,phasesMs:result.phasesMs,checksum:result.check,geometryWork:result.q.geometryWork,certificate:result.q.certificate,work:result.s.work,residualWork:result.s.residualWork,iterations:result.s.iterations??1,converged:result.s.converged??true,lastChange:result.s.lastChange??null,residualLog:result.s.residualLog,sourceReceiverMismatch:result.s.sourceReceiverMismatch,assemblyStats:result.q.assemblyStats??null};
 progress.currentTiming=rec;const raw=json(`results/call-${String(rec.sequence).padStart(3,'0')}-raw.json`,rec);rec.raw=raw;evidence.timings.push(rec);
 const comparison=compare(result.q,result.s,qualified,false),mh=matrixHash(result.q),sh=solHash(result.s),checksum=result.check===kernel.checksum(qualified.q,qualified.s);
 const inputUnchanged=item.inputBytes.equals(stateBuffer(item.states));
 rec.validation={...comparison,inputUnchanged,checksum,matrixHash:mh,solutionHash:sh,hashesMatch:mh===qualified.matrixHash&&sh===qualified.solutionHash,pass:comparison.pass&&inputUnchanged&&checksum&&mh===qualified.matrixHash&&sh===qualified.solutionHash};
 json(`results/call-${String(rec.sequence).padStart(3,'0')}.json`,rec);
 if(!rec.validation.pass){persist(item.id,'repeat-failure-'+rec.sequence,result.q,result.s);throw Error('repeat output mismatch');}
}
try{
 assert(os.endianness()==='LE','little endian runtime required');assert(!process.env.NODE_OPTIONS&&process.execArgv.length===0,'runtime options forbidden');
 let retained=null;
 for(const ctl of controls()){
  progress={phase:'control',id:ctl.id};guard();const states=statesFor(ctl.positions),before=stateBuffer(states),built={};
  for(const label of config.methods)built[label]=kernel.build(states,mode[label],true,guard);
  const rec={id:ctl.id,n:states.length,stateTokens:states.map(a=>a.map(token)),positionTokens:ctl.positions.map(a=>a.map(token)),A:literal(built.A),L:literal(built.L),T:literal(built.T)};
  rec.pass=exact(canonical(rec.A),canonical(rec.L))&&exact(canonical(rec.A),canonical(rec.T))&&before.equals(stateBuffer(states));
  if(ctl.id.startsWith('planes-')){rec.expectedPositiveTerms=4*(states.length/2)**2;rec.pass&&=built.A.kv.length===rec.expectedPositiveTerms&&built.T.assemblyStats.chunkCount===Math.ceil(rec.expectedPositiveTerms/4096);}
  const saved=json(`results/control-${ctl.id}.json`,rec);evidence.controls.push({id:ctl.id,pass:rec.pass,pin:saved});assert(rec.pass,'control mismatch');
  if(ctl.id==='planes-66')retained={states,before,built:{L:built.L,T:built.T},literals:{L:rec.L,T:rec.T}};
 }
 assert(evidence.controls.length===config.controls&&retained,'control schedule mismatch');
 progress={phase:'ownership'};const extraBuilds=[],seen=[];let disjoint=true,unchanged=true;
 function checkStorage(q){for(const a of [q.offsets,q.src,q.kv,q.aa,q.symbols]){disjoint&&=a.byteOffset===0&&a.byteLength===a.buffer.byteLength&&!seen.some(b=>b.buffer===a.buffer);seen.push(a);}}
 for(const q of Object.values(retained.built))checkStorage(q);
 for(const spec of ownershipSequence){const [label,which]=spec.split(':'),positions=which==='sparse2'?[[0,0,0],[4,0,0]]:Array.from({length:62},(_,i)=>[0,0,i<31?0:.6]),states=statesFor(positions),before=stateBuffer(states),q=kernel.build(states,mode[label],true,guard);checkStorage(q);unchanged&&=before.equals(stateBuffer(states));extraBuilds.push({label,id:which,n:states.length,stateTokens:states.map(a=>a.map(token)),positionTokens:positions.map(a=>a.map(token)),bundle:literal(q)});}
 unchanged&&=retained.before.equals(stateBuffer(retained.states));const ownership={sequence:ownershipSequence,extraBuilds,retained:{L:{before:retained.literals.L,after:literal(retained.built.L)},T:{before:retained.literals.T,after:literal(retained.built.T)}},inputUnchanged:unchanged,returnedStorageDisjoint:disjoint};
 ownership.pass=unchanged&&disjoint&&exact(ownership.retained.L.before,ownership.retained.L.after)&&exact(ownership.retained.T.before,ownership.retained.T.after);evidence.ownership=json('results/ownership.json',ownership);assert(ownership.pass,'ownership control mismatch');retained=null;
 const index={kind:'fresh-airflow-off-boids-states',shape:['vehicle',17],dtype:'float64le',cases:[]},cases=[];
 for(const info of config.cases){
  progress={phase:'generation',id:info.id};guard();const framePins=[],frames=[],g0=performance.now();let initialPin=null;
  const run=sim.run({seed:info.seed,count:info.n,...Object.fromEntries(['duration','dt','mode','search','filter','record','frameEvery'].map(k=>[k,config.generation[k]])),frameSink(frame){guard();const arr=Float64Array.from(frame),pin=write(`generation/${info.id}-frame-${String(frames.length).padStart(3,'0')}.f64`,bytes(arr));frames.push(arr);framePins.push({...pin,t:frame[0]});progress={phase:'generation',id:info.id,frameCount:frames.length,time:frame[0],frames:framePins};},progress(state,states){guard();if(state.t===0&&!initialPin)initialPin=write(`generation/${info.id}-initial.f64`,stateBuffer(states));}});
  const generationMs=performance.now()-g0,finalPin=write(`inputs/${info.id}.f64`,stateBuffer(run.final)),posesPin=write(`generation/${info.id}-poses.f64`,Buffer.concat(frames.map(bytes))),initialMatches=initialPin&&sha(stateBuffer(run.initial))===initialPin.sha256;
  const expectedConfig={filter:config.generation.filter,seed:info.seed,count:info.n,mode:config.generation.mode,dt:config.generation.dt,duration:info.t,search:config.generation.search,course:config.generation.expectedCourse,airflow:'off',observation:'ideal'},expectedTimes=Array.from({length:21},(_,i)=>i/10),finalPose=Float64Array.from([info.t,...run.final.flatMap(s=>[...s.slice(0,3),...s.slice(6,10)])]);
  const complete=initialMatches&&exact(run.config,expectedConfig)&&run.metrics.end===info.t&&run.metrics.stopReason===null&&run.metrics.failure===null&&exact(run.recording,{cadence:.1,streamed:true})&&frames.length===21&&frames.every((f,i)=>f[0]===expectedTimes[i]&&f.length===1+7*info.n)&&bytes(frames.at(-1)).equals(bytes(finalPose));
  const {initial,final,...rest}=run,record={id:info.id,n:info.n,seed:info.seed,...rest,initial:initialPin,final:finalPin,frames:framePins,poses:{...posesPin,frames:frames.length,width:1+7*info.n},generationMs,initialMatches,complete},meta=json(`generation/${info.id}.json`,record);evidence.generation.push({id:info.id,pin:meta,complete,generationMs});
  index.cases.push({...info,...finalPin,generationPath:meta.path});cases.push({...info,states:run.final,inputBytes:stateBuffer(run.final),builders:{}});assert(complete,'generation completion mismatch');
 }
 json('inputs/index.json',index);
 for(const item of cases){
  for(const label of config.methods){
   progress={phase:'qualification',id:item.id,label};guard();const t=performance.now(),q=kernel.build(item.states,mode[label],true,guard);q.diagnosticGraph=kernel.fullGraph(q);
   // Save a rejected domain before any solve. No alternative method is allowed.
   if(!q.admission.admitted||!q.graph.descendingEligible){persist(item.id,label,q,null);throw Error('qualification domain rejected');}
   const s=kernel.solve(q,'O',kernel.schedule(q),false,guard);Object.assign(s,kernel.residual(q,s,guard));const qualificationComputeMs=performance.now()-t,saved=persist(item.id,label,q,s),qualified={q,s,matrixHash:matrixHash(q),solutionHash:solHash(s)};
   item.builders[label]=qualified;const comparison=compare(q,s,item.builders.A,true);comparison.inputUnchanged=item.inputBytes.equals(stateBuffer(item.states));comparison.pass&&=comparison.inputUnchanged;const record={id:item.id,label,qualificationComputeMs,persistence:saved,comparison,matrixHash:qualified.matrixHash,solutionHash:qualified.solutionHash};evidence.qualification.push(record);json(`results/qualification-${item.id}-${label}.json`,record);assert(comparison.pass,'qualification anchor mismatch');
   if(label!=='A')q.symbols=null;
  }
  item.builders.A.q.symbols=null;
 }
 for(const item of cases)for(const method of config.methods)recordTiming(item,method,-1,true);
 for(let block=0;block<config.blocks;block++)for(let j=0;j<cases.length;j++){const c=(j+block)%cases.length,item=cases[c];for(const method of config.permutations[(block+c)%6])recordTiming(item,method,block,false);}
 assert(evidence.qualification.length===config.qualificationBuilds&&evidence.timings.length===config.totalCalls&&evidence.generation.length===3,'completed schedule mismatch');
 evidence.complete=true;evidence.environmentEnd=environment();evidence.memory={sampledPeakRSSBytes:maxRSS,processResourceUsage:process.resourceUsage(),platformMaxRSSUnits:'Node maxRSS in kilobytes; separate sampled RSS in bytes'};evidence.newScientificBytesBeforeEvidence=outputBytes;json('results/evidence.json',evidence);
 console.log(JSON.stringify({complete:true,controls:evidence.controls.length,generation:evidence.generation.length,qualifications:evidence.qualification.length,timingCalls:evidence.timings.length}));
}catch(e){
 evidence.complete=false;const allowed=['RSS guard exceeded','internal wall guard exceeded','output guard exceeded','positive coefficient guard exceeded','compressed symbol guard exceeded','control mismatch','control schedule mismatch','ownership control mismatch','generation completion mismatch','qualification domain rejected','qualification anchor mismatch','repeat output mismatch','solve domain rejected','candidate order/uniqueness failure','typed row capacity invariant failure','invalid alpha','completed schedule mismatch','runtime options forbidden','little endian runtime required'];
 const error={message:allowed.includes(e.message)?e.message:'unexpected execution exception',exceptionClass:e.constructor.name,progress,completedControls:evidence.controls.length,completedGeneration:evidence.generation.length,completedQualifications:evidence.qualification.length,completedTimings:evidence.timings.length};json('results/failure.json',error,true);json('results/partial-evidence.json',evidence,true);process.exitCode=1;console.log(JSON.stringify(error));
}
