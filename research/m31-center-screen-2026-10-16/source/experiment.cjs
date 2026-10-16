'use strict';
// SOURCE PREPARATION ONLY. Scientific imports are behind the frozen runtime gate.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto'),zlib=require('node:zlib'),os=require('node:os'),cp=require('node:child_process');
const p=path.resolve(process.argv[2]),start=performance.now(),config=JSON.parse(fs.readFileSync(path.join(p,'config.json'),'utf8'));
const runtime=JSON.parse(fs.readFileSync(path.join(p,'runtime.json'),'utf8'));
const sha=b=>crypto.createHash('sha256').update(b).digest('hex'),bytes=x=>Buffer.from(x.buffer,x.byteOffset,x.byteLength),mode={L:'lean',F:'screen'};
let kernel,sim,controlModule,outputBytes=0,progress={phase:'runtime-gate'},maxRSS=0;
for(const dir of ['results','inputs','generation'])fs.mkdirSync(path.join(p,dir),{recursive:true});
const token=x=>Object.is(x,-0)?'-0':String(x);
function encode(x){if(typeof x==='number'&&(!Number.isFinite(x)||Object.is(x,-0)))return token(x);if(Array.isArray(x))return x.map(encode);if(x&&typeof x==='object')return Object.fromEntries(Object.entries(x).map(([k,v])=>[k,encode(v)]));return x;}
function clone(x){if(Array.isArray(x))return x.map(clone);if(x&&typeof x==='object')return Object.fromEntries(Object.entries(x).map(([k,v])=>[k,clone(v)]));return x;}
function exact(a,b){if(Object.is(a,b))return true;if(!a||!b||typeof a!=='object'||typeof b!=='object'||Array.isArray(a)!==Array.isArray(b))return false;const ka=Object.keys(a),kb=Object.keys(b);return ka.length===kb.length&&ka.every(k=>Object.hasOwn(b,k)&&exact(a[k],b[k]));}
function assert(v,label){if(!v)throw Error('checkpoint: '+label);}
function guard(){maxRSS=Math.max(maxRSS,process.memoryUsage().rss);assert(maxRSS<=config.limits.rssBytes,'RSS guard exceeded');assert(performance.now()-start<=config.limits.candidateCooperativeSeconds*1000,'internal wall guard exceeded');}
function write(rel,b,emergency=false){if(typeof b==='string')b=Buffer.from(b);assert(outputBytes+b.length<=(emergency?config.limits.scientificBytes:config.limits.normalScientificBytes),'output guard exceeded');fs.writeFileSync(path.join(p,rel),b,{flag:'wx'});outputBytes+=b.length;return {path:rel,bytes:b.length,sha256:sha(b)};}
const json=(rel,o,emergency=false)=>write(rel,JSON.stringify(encode(o))+'\n',emergency);
const statesFor=positions=>positions.map(v=>[...v,0,0,0,0,0,0,1,0,0,0,...Array(4).fill(kernel.constants.mg/4)]);
const stateBuffer=states=>bytes(Float64Array.from(states.flat()));
function numeric(a,b){
 if(a===null||b===null)return {length:0,bad:a===b?0:1,pass:a===b,firstMismatch:a===b?null:{nullMismatch:true}};
 if(a.length!==b.length)return {length:a.length,bad:1,pass:false,firstMismatch:{lengthA:a.length,lengthB:b.length}};
 let maxAbs=0,maxRel=0,bad=0,nonfinitePairs=0,firstMismatch=null;
 for(let i=0;i<a.length;i++){if(Number.isFinite(a[i])&&Number.isFinite(b[i])){const d=Math.abs(a[i]-b[i]);maxAbs=Math.max(maxAbs,d);maxRel=Math.max(maxRel,d/Math.max(Math.abs(b[i]),Number.MIN_VALUE));}else nonfinitePairs++;if(!Object.is(a[i],b[i])){bad++;if(firstMismatch===null)firstMismatch={index:i,actual:token(a[i]),reference:token(b[i])};}}
 return {length:a.length,maxAbs,maxRel,nonfinitePairs,bad,firstMismatch,pass:bad===0};
}
function literal(q){return clone({n:q.n,symbols:q.symbols?[...q.symbols]:null,offsets:[...q.offsets],sources:[...q.src],K:[...q.kv],a:q.aa?[...q.aa]:null,input:q.input,admission:q.admission,graph:kernel.fullGraph(q),certificate:q.certificate,symbolCounts:q.symbolCounts,geometryWork:q.geometryWork,ordinaryLmax:q.ordinaryLmax,assemblyStats:q.assemblyStats??null,screen:q.screen??null});}
function modelGeometry(q){const {directedCenterTests,certifiedSkippedPairs,...rest}=q.geometryWork;return rest;}
function comparableAssembly(q){if(!q.assemblyStats)return null;const {commonSymbolBytes,...rest}=q.assemblyStats;return rest;}
function solutionValues(s){return [...s.y,...s.rotors.flatMap(a=>a.flatMap(r=>[r.alpha,r.x,r.T])),...s.residualMap.y,...s.residualMap.rotors.flatMap(a=>a.flatMap(r=>[r.alpha,r.x,r.T]))];}
function solutionRecord(s){return {values:solutionValues(s),work:s.work,residualWork:s.residualWork,residualLog:s.residualLog,sourceReceiverMismatch:s.sourceReceiverMismatch,iterations:s.iterations??1,converged:s.converged??true,lastChange:s.lastChange??null};}
const solHash=s=>sha(JSON.stringify(encode(solutionRecord(s))));
function matrixHash(q){const h=crypto.createHash('sha256');for(const a of [q.offsets,q.src,q.kv,q.aa])if(a)h.update(bytes(a));h.update(JSON.stringify(encode({input:q.input,admission:q.admission,graph:kernel.fullGraph(q),symbolCounts:q.symbolCounts,ordinaryLmax:q.ordinaryLmax})));return h.digest('hex');}
function solveCompare(s,ref){if(s===null||ref===null)return {pass:s===ref,notSolved:true};const values=numeric(solutionValues(s),solutionValues(ref)),work=exact(s.work,ref.work)&&exact(s.residualWork,ref.residualWork),termination=(s.iterations??1)===(ref.iterations??1)&&(s.converged??true)===(ref.converged??true)&&Object.is(s.lastChange??null,ref.lastChange??null),residual=Number.isFinite(s.residualLog)&&s.residualLog<=1e-9&&Number.isFinite(s.sourceReceiverMismatch)&&s.sourceReceiverMismatch<=2e-9,exactResidual=Object.is(s.residualLog,ref.residualLog)&&Object.is(s.sourceReceiverMismatch,ref.sourceReceiverMismatch),completeSolution=exact(s,ref);return {values,work,termination,residual,exactResidual,completeSolution,pass:values.pass&&work&&termination&&residual&&exactResidual&&completeSolution};}
function compare(q,s,ref,withSymbols,ownMethod=false){
 const c={symbols:!withSymbols||(q.symbols!==null&&ref.q.symbols!==null&&q.symbols.equals(ref.q.symbols)),offsets:bytes(q.offsets).equals(bytes(ref.q.offsets)),sources:bytes(q.src).equals(bytes(ref.q.src)),K:numeric(q.kv,ref.q.kv),a:numeric(q.aa,ref.q.aa),prepared:bytes(q.p).equals(bytes(ref.q.p))&&exact(q.nominal,ref.q.nominal)&&exact(q.S0,ref.q.S0),input:exact(q.input,ref.q.input),admission:exact(q.admission,ref.q.admission),graph:exact(kernel.fullGraph(q),kernel.fullGraph(ref.q)),dependencies:exact(q.deps,ref.q.deps),certificate:exact(q.certificate,ref.q.certificate),symbolCounts:exact(q.symbolCounts,ref.q.symbolCounts),modelGeometry:exact(modelGeometry(q),modelGeometry(ref.q)),ordinaryLmax:Object.is(q.ordinaryLmax,ref.q.ordinaryLmax),assembly:exact(comparableAssembly(q),comparableAssembly(ref.q)),symbolAllocation:q.assemblyStats.commonSymbolBytes===(withSymbols?q.n*q.n*4:0),solution:solveCompare(s,ref.s)};
 if(ownMethod){c.screen=exact(q.screen??null,ref.q.screen??null);c.allGeometryWork=exact(q.geometryWork,ref.q.geometryWork);}
 c.pass=Object.values(c).every(v=>typeof v==='boolean'?v:v.pass);return c;
}
function omissionAudit(states,L,F){
 const n=states.length,screen=F.screen,rec={eligible:screen.eligible,orderedPairs:0,omittedPairs:0,checkedRotorSymbols:0,exactOutsideSymbols:true,firstMismatch:null};
 assert(L.symbols&&F.symbols,'omission tensor missing');
 for(let i=0;i<n;i++){guard();for(let j=0;j<n;j++){if(i===j)continue;rec.orderedPairs++;const dx=states[j][0]-states[i][0],dy=states[j][1]-states[i][1],dz=states[j][2]-states[i][2];if(!screen.eligible||Math.max(Math.abs(dx),Math.abs(dy),Math.abs(dz))<config.screen.componentThreshold)continue;rec.omittedPairs++;for(let r=0;r<4;r++){rec.checkedRotorSymbols++;const at=4*(i*n+j)+r;if(L.symbols[at]!==1||F.symbols[at]!==1){rec.exactOutsideSymbols=false;if(rec.firstMismatch===null)rec.firstMismatch={receiver:i,source:j,rotor:r,L:L.symbols[at],F:F.symbols[at]};}}}}
 rec.screenCounts=rec.orderedPairs===screen.orderedPairVisits&&rec.omittedPairs===screen.skippedCenterNormCalls&&screen.actualCenterNormCalls===rec.orderedPairs-rec.omittedPairs&&screen.componentTests===(screen.eligible?rec.orderedPairs:0);
 rec.pass=rec.exactOutsideSymbols&&rec.screenCounts;return rec;
}
function persist(id,label,q,s){
 const t0=performance.now(),base=`results/${id}-${label}`,artifacts={};
 if(q.symbols){const gz=zlib.gzipSync(q.symbols,{level:6});assert(gz.length<=config.limits.compressedSymbolsBytesPerBundle,'compressed symbol guard exceeded');artifacts.symbols={...write(base+'-symbols.u8.gz',gz),rawSha256:sha(q.symbols),rawBytes:q.symbols.length};}
 for(const [k,v] of Object.entries({offsets:q.offsets,sources:q.src,K:q.kv,a:q.aa}))if(v)artifacts[k]=write(base+'-'+k+'.bin',bytes(v));
 const doc={id,label,n:q.n,input:q.input,admission:q.admission,graph:kernel.fullGraph(q),certificate:q.certificate,symbolCounts:q.symbolCounts,geometryWork:q.geometryWork,ordinaryLmax:q.ordinaryLmax,assemblyStats:q.assemblyStats??null,screen:q.screen??null,artifacts,solutions:{O:s},matrixHash:matrixHash(q),solutionHash:s?solHash(s):null};
 const meta=json(base+'.json',doc);return {meta,totalPersistenceMs:performance.now()-t0,fsync:false};
}
function environment(){const cores=os.cpus(),read=(cmd,args)=>{try{return cp.execFileSync(cmd,args,{encoding:'utf8',timeout:3000}).trim();}catch{return null;}};const power=read('/usr/bin/pmset',['-g']);return {cpuModel:cores[0]?.model??null,logicalCores:cores.length,physicalCores:Number(read('/usr/sbin/sysctl',['-n','hw.physicalcpu']))||null,installedRAMBytes:os.totalmem(),architecture:os.arch(),platform:os.platform(),kernel:os.release(),node:process.version,v8:process.versions.v8,nodeExecutableSha256:runtime.node.sha256,nodeOptionsEmpty:!process.env.NODE_OPTIONS,executionFlagCount:process.execArgv.length,clock:'performance.now monotonic milliseconds',loadAverage:os.loadavg(),lowPowerMode:power?.match(/lowpowermode\s+(\d+)/)?.[1]??null,powerSource:read('/usr/bin/pmset',['-g','batt'])?.match(/Now drawing from '([^']+)'/)?.[1]??null,threads:'one JS worker; runtime helper threads unspecified',pidOmitted:true};}
const evidence={kind:'fresh-boids-center-screen',constants:null,complete:false,controls:[],ownership:null,generation:[],qualification:[],timings:[],environmentStart:null};
function recordTiming(item,method,block,warmup){
 const sequence=evidence.timings.length;progress={phase:'timing',id:item.id,method,block,warmup,sequence};guard();let result;const attemptStart=performance.now();
 try{result=kernel.query(item.states,method,guard);}catch(e){json(`results/call-${String(sequence).padStart(3,'0')}-raw.json`,{sequence,id:item.id,method,block,warmup,status:'query-threw',observedElapsedMs:performance.now()-attemptStart},true);throw e;}
 const qualified=item.builders[method],rec={sequence,workload:'full',id:item.id,method,block,warmup,status:'returned',totalMs:result.totalMs,phasesMs:result.phasesMs,checksum:result.check,geometryWork:result.q.geometryWork,screen:result.q.screen??null,certificate:result.q.certificate,work:result.s.work,residualWork:result.s.residualWork,iterations:result.s.iterations??1,converged:result.s.converged??true,lastChange:result.s.lastChange??null,residualLog:result.s.residualLog,sourceReceiverMismatch:result.s.sourceReceiverMismatch,assemblyStats:result.q.assemblyStats??null};
 progress.currentTiming=clone(rec);rec.raw=json(`results/call-${String(sequence).padStart(3,'0')}-raw.json`,rec);evidence.timings.push(rec);
 const comparison=compare(result.q,result.s,qualified,false,true),mh=matrixHash(result.q),sh=solHash(result.s),checksum=Object.is(result.check,kernel.checksum(qualified.q,qualified.s)),inputUnchanged=item.inputBytes.equals(stateBuffer(item.states));
 const finiteTiming=Number.isFinite(rec.totalMs)&&rec.totalMs>0&&Object.values(rec.phasesMs).every(Number.isFinite);
 rec.validation={...comparison,inputUnchanged,inputBeforeSha256:sha(item.inputBytes),inputAfterSha256:sha(stateBuffer(item.states)),checksum,finiteTiming,matrixHash:mh,solutionHash:sh,hashesMatch:mh===qualified.matrixHash&&sh===qualified.solutionHash,pass:comparison.pass&&inputUnchanged&&checksum&&finiteTiming&&mh===qualified.matrixHash&&sh===qualified.solutionHash};
 json(`results/call-${String(sequence).padStart(3,'0')}.json`,rec);
 if(!rec.validation.pass){persist(item.id,'repeat-failure-'+sequence,result.q,result.s);throw Error('checkpoint: repeat output mismatch');}
}
try{
 assert(process.argv.length===3,'argument shape');assert(os.endianness()==='LE','little endian runtime required');assert(!process.env.NODE_OPTIONS&&process.execArgv.length===0,'runtime options forbidden');
 const nodeBytes=fs.readFileSync(fs.realpathSync(process.execPath));assert(nodeBytes.length===runtime.node.bytes&&sha(nodeBytes)===runtime.node.sha256&&process.version===runtime.node.version,'Node runtime identity');assert(os.arch()===runtime.architecture&&os.platform()===runtime.platform,'platform identity');
 assert(config.schema==='m31-center-screen-v1'&&exact(config.methods,['L','F'])&&exact(config.permutations,['LF','FL'])&&config.blocks===6&&config.warmupCalls===6&&config.measuredCalls===36&&config.totalCalls===42,'frozen schedule');
 assert(config.controls===48&&Array.isArray(config.controlIds)&&config.controlIds.length===48&&config.ownershipExtraBuilds===6&&config.qualificationBuilds===6&&config.qualificationSolves===6,'frozen control counts');
 assert(config.controlSolvePolicy==='untimed solve+residual iff admitted and descendingEligible; otherwise explicit no-solve reason','frozen control solve policy');
 process.env.FLOCK_FACTORY_VARIANT=config.generation.factoryVariant;
 kernel=require('./kernel.cjs');sim=require('../../../outputs/milestone-31-source/sim.cjs');controlModule=require('./controls.cjs');
 evidence.constants=kernel.constants;evidence.environmentStart=environment();
 assert(exact(controlModule.controlIds,config.controlIds),'exported literal control IDs');const fixedControls=controlModule.controls();assert(exact(fixedControls.map(c=>c.id),config.controlIds),'literal control IDs');
 let retained=null;
 for(const ctl of fixedControls){
  progress={phase:'control',id:ctl.id};guard();const states=statesFor(ctl.positions);
  for(const patch of ctl.statePatches??[]){assert(Number.isInteger(patch.vehicle)&&patch.vehicle>=0&&patch.vehicle<states.length&&Number.isInteger(patch.index)&&patch.index>=0&&patch.index<17,'control patch');states[patch.vehicle][patch.index]=patch.value;}
  const before=stateBuffer(states),beforeTokens=states.map(a=>a.map(token)),built={},solutions={L:null,F:null},mutationChecks={build:{},solve:{L:null,F:null}};for(const label of config.methods){built[label]=kernel.build(states,mode[label],true,guard);mutationChecks.build[label]=before.equals(stateBuffer(states));}
  const buildComparison=compare(built.F,null,{q:built.L,s:null},true),audit=omissionAudit(states,built.L,built.F);
  const rec={id:ctl.id,n:states.length,inputBeforeTokens:beforeTokens,stateTokens:states.map(a=>a.map(token)),positionTokens:ctl.positions.map(a=>a.map(token)),statePatches:(ctl.statePatches??[]).map(x=>({...x,value:token(x.value)})),expectedScreenEligible:ctl.expectedScreenEligible,expectedFallbackReason:ctl.expectedFallbackReason,solvePolicy:'admitted-and-descending-only',noSolveReason:null,L:literal(built.L),F:literal(built.F),solutions,comparison:buildComparison,omissionAudit:audit,mutationChecks};
  rec.screenExpectation=Object.is(built.F.screen.eligible,ctl.expectedScreenEligible)&&Object.is(built.F.screen.fallbackReason,ctl.expectedFallbackReason);
  if(buildComparison.pass&&built.L.admission.admitted&&built.L.graph.descendingEligible){for(const label of config.methods){const q=built[label],s=kernel.solve(q,'O',kernel.schedule(q),false,guard);Object.assign(s,kernel.residual(q,s,guard));solutions[label]=s;mutationChecks.solve[label]=before.equals(stateBuffer(states));}}else rec.noSolveReason=!buildComparison.pass?'model-mismatch':!built.L.admission.admitted?'admission':'ordering';
  rec.solutionComparison=solveCompare(solutions.F,solutions.L);rec.stateTokens=states.map(a=>a.map(token));rec.inputBeforeSha256=sha(before);rec.inputAfterSha256=sha(stateBuffer(states));rec.inputUnchanged=before.equals(stateBuffer(states))&&Object.values(mutationChecks.build).every(x=>x===true)&&Object.values(mutationChecks.solve).every(x=>x===null||x===true);rec.pass=buildComparison.pass&&audit.pass&&rec.screenExpectation&&rec.solutionComparison.pass&&rec.inputUnchanged;
  const saved=json(`results/control-${ctl.id}.json`,rec);evidence.controls.push({id:ctl.id,pass:rec.pass,pin:saved,solved:solutions.L!==null});assert(rec.pass,'control mismatch');
  if(ctl.id==='planes-66')retained={states,before,beforeTokens,built,literals:{L:rec.L,F:rec.F}};
 }
 assert(evidence.controls.length===config.controls&&retained,'control schedule mismatch');
 progress={phase:'ownership'};const extraBuilds=[],seen=[],seenArrays=[];let disjoint=true,unchanged=true;
 function checkStorage(q){for(const a of [q.p,q.offsets,q.src,q.kv,q.aa,q.symbols].filter(Boolean)){disjoint&&=a.byteOffset===0&&a.byteLength===a.buffer.byteLength&&!seen.some(b=>b.buffer===a.buffer);seen.push(a);}for(const a of [q.S0,...q.nominal,...q.deps,...(q.screen?[q.screen.min,q.screen.max,q.screen.spans]:[])]){disjoint&&=!seenArrays.includes(a)&&!q.states.some(b=>a===b);seenArrays.push(a);}}
 for(const q of Object.values(retained.built))checkStorage(q);
 assert(exact(controlModule.ownershipSequence,['L:sparse2','F:sparse2','L:planes62','F:planes62','L:fallback258','F:fallback258'])&&exact(controlModule.ownershipSequence,config.ownershipSequence)&&controlModule.ownershipSequence.length===config.ownershipExtraBuilds,'ownership schedule');
 for(const spec of controlModule.ownershipSequence){const [label,which]=spec.split(':'),positions=which==='sparse2'?[[0,0,0],[4,0,0]]:which==='fallback258'?[[0,0,0],[258,0,0]]:Array.from({length:62},(_,i)=>[0,0,i<31?0:.6]),states=statesFor(positions),before=stateBuffer(states),beforeTokens=states.map(a=>a.map(token)),q=kernel.build(states,mode[label],true,guard);checkStorage(q);const inputUnchanged=before.equals(stateBuffer(states));unchanged&&=inputUnchanged;extraBuilds.push({label,id:which,n:states.length,inputBeforeTokens:beforeTokens,stateTokens:states.map(a=>a.map(token)),inputBeforeSha256:sha(before),inputAfterSha256:sha(stateBuffer(states)),inputUnchanged,positionTokens:positions.map(a=>a.map(token)),bundle:literal(q)});}
 unchanged&&=retained.before.equals(stateBuffer(retained.states));const ownership={sequence:controlModule.ownershipSequence,extraBuilds,retained:{L:{before:retained.literals.L,after:literal(retained.built.L)},F:{before:retained.literals.F,after:literal(retained.built.F)}},retainedInputBeforeTokens:retained.beforeTokens,retainedInputAfterTokens:retained.states.map(a=>a.map(token)),retainedInputBeforeSha256:sha(retained.before),retainedInputAfterSha256:sha(stateBuffer(retained.states)),inputUnchanged:unchanged,returnedStorageDisjoint:disjoint};
 ownership.pass=unchanged&&disjoint&&exact(ownership.retained.L.before,ownership.retained.L.after)&&exact(ownership.retained.F.before,ownership.retained.F.after);evidence.ownership=json('results/ownership.json',ownership);assert(ownership.pass,'ownership control mismatch');retained=null;
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
   progress={phase:'qualification',id:item.id,label};guard();const t=performance.now(),q=kernel.build(item.states,mode[label],true,guard);
   q.diagnosticGraph=kernel.fullGraph(q);
   if(!q.admission.admitted||!q.graph.descendingEligible){persist(item.id,label,q,null);throw Error('checkpoint: qualification domain rejected');}
   const s=kernel.solve(q,'O',kernel.schedule(q),false,guard);Object.assign(s,kernel.residual(q,s,guard));
   const qualificationComputeMs=performance.now()-t,saved=persist(item.id,label,q,s),qualified={q,s,matrixHash:matrixHash(q),solutionHash:solHash(s)};
   item.builders[label]=qualified;const comparison=compare(q,s,item.builders.L,true);
   comparison.inputUnchanged=item.inputBytes.equals(stateBuffer(item.states));comparison.pass&&=comparison.inputUnchanged;
   const audit=label==='F'?omissionAudit(item.states,item.builders.L.q,q):null;
   const record={id:item.id,label,qualificationComputeMs,persistence:saved,comparison,omissionAudit:audit,inputBeforeSha256:sha(item.inputBytes),inputAfterSha256:sha(stateBuffer(item.states)),matrixHash:qualified.matrixHash,solutionHash:qualified.solutionHash};
   record.pass=comparison.pass&&(!audit||audit.pass);evidence.qualification.push(record);
   json(`results/qualification-${item.id}-${label}.json`,record);assert(record.pass,'qualification anchor mismatch');
  }
  // Both complete tensors were persisted and element-compared before release.
  for(const label of config.methods)item.builders[label].q.symbols=null;
 }
 for(const item of cases)for(const method of config.methods)recordTiming(item,method,-1,true);
 for(let block=0;block<config.blocks;block++)for(let j=0;j<cases.length;j++){const c=(j+block)%cases.length,item=cases[c];for(const method of config.permutations[(block+c)%2])recordTiming(item,method,block,false);}
 assert(evidence.qualification.length===config.qualificationBuilds&&evidence.timings.length===config.totalCalls&&evidence.timings.filter(x=>x.warmup).length===config.warmupCalls&&evidence.timings.filter(x=>!x.warmup).length===config.measuredCalls&&evidence.generation.length===3,'completed schedule mismatch');
 evidence.complete=true;evidence.environmentEnd=environment();evidence.memory={sampledPeakRSSBytes:maxRSS,processResourceUsage:process.resourceUsage(),platformMaxRSSUnits:'Node maxRSS in kilobytes; separate sampled RSS in bytes'};
 evidence.newScientificBytesBeforeEvidence=outputBytes;evidence.controlSolvePolicy='admitted-and-descending-only';evidence.actualControlSolves=2*evidence.controls.filter(x=>x.solved).length;
 json('results/evidence.json',evidence);
 console.log(JSON.stringify({complete:true,controls:evidence.controls.length,generation:evidence.generation.length,qualifications:evidence.qualification.length,timingCalls:evidence.timings.length}));
}catch(e){
 evidence.complete=false;
 const known=['positive coefficient guard exceeded','candidate order/uniqueness failure','invalid alpha','solve domain rejected'];
 const message=e.message?.startsWith('checkpoint: ')?e.message:known.includes(e.message)?e.message:'unexpected execution exception';
 const failure={message,exceptionClass:e.constructor.name,progress,completedControls:evidence.controls.length,completedGeneration:evidence.generation.length,completedQualifications:evidence.qualification.length,completedTimings:evidence.timings.length};
 try{json('results/failure.json',failure,true);}catch{console.error('failure evidence write failed');}
 try{json('results/partial-evidence.json',evidence,true);}catch{console.error('partial evidence write failed');}
 process.exitCode=1;console.log(JSON.stringify(encode(failure)));
}
