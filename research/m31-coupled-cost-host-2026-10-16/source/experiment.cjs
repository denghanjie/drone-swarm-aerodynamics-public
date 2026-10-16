'use strict';
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto'),zlib=require('node:zlib'),os=require('node:os'),cp=require('node:child_process');
const kernel=require('./kernel.cjs');
const p=path.resolve(process.argv[2]),prior=path.resolve(p,'../m31-swarm-coupling-transfer-2026-10-16'),start=performance.now();
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
const bytes=x=>Buffer.from(x.buffer,x.byteOffset,x.byteLength);
let outputBytes=0,progress={},maxRSS=0;
function guard(){maxRSS=Math.max(maxRSS,process.memoryUsage().rss);if(maxRSS>1.5*1024**3)throw Error('RSS guard exceeded');if(performance.now()-start>295000)throw Error('internal wall guard exceeded');}
function write(rel,b,emergency=false){if(typeof b==='string')b=Buffer.from(b);if(outputBytes+b.length>(emergency?128:124)*1024**2)throw Error('output guard exceeded');fs.writeFileSync(path.join(p,rel),b,{flag:'wx'});outputBytes+=b.length;return {path:rel,bytes:b.length,sha256:sha(b)};}
const json=(rel,o)=>write(rel,JSON.stringify(o)+'\n');
function assert(v,label){if(!v)throw Error(label);}
function numeric(a,b,atol,rtol){assert(a.length===b.length,'array length mismatch');let maxAbs=0,maxRel=0,bad=0,firstMismatch=null;for(let i=0;i<a.length;i++){const d=Math.abs(a[i]-b[i]);maxAbs=Math.max(maxAbs,d);maxRel=Math.max(maxRel,d/Math.max(Math.abs(b[i]),Number.MIN_VALUE));if(!Number.isFinite(a[i])||!Number.isFinite(b[i])||d>atol+rtol*Math.abs(b[i])){bad++;if(!firstMismatch)firstMismatch={index:i,actual:a[i],reference:b[i]};}}return {length:a.length,maxAbs,maxRel,bad,firstMismatch,pass:bad===0};}
const exact=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
function solutionValues(s){return [...s.y,...s.rotors.flatMap(a=>a.flatMap(r=>[r.alpha,r.x,r.T])),...s.residualMap.y,...s.residualMap.rotors.flatMap(a=>a.flatMap(r=>[r.alpha,r.x,r.T]))];}
function solHash(s){return sha(JSON.stringify({values:solutionValues(s),work:s.work,residualWork:s.residualWork,residualLog:s.residualLog,sourceReceiverMismatch:s.sourceReceiverMismatch,iterations:s.iterations??1,converged:s.converged??true,lastChange:s.lastChange??null}));}
function matrixHash(q){const h=crypto.createHash('sha256');for(const a of [q.offsets,q.src,q.kv,q.aa])h.update(bytes(a));h.update(JSON.stringify({input:q.input,admission:q.admission,graph:q.graph,symbolCounts:q.symbolCounts,ordinaryLmax:q.ordinaryLmax}));return h.digest('hex');}
function solveCompare(s,ref){const values=numeric(solutionValues(s),solutionValues(ref),0,1e-9),work=exact(s.work,ref.work)&&exact(s.residualWork,ref.residualWork),termination=(s.iterations??1)===(ref.iterations??1)&&(s.converged??true)===(ref.converged??true),residual=Number.isFinite(s.residualLog)&&s.residualLog<=1e-9&&Number.isFinite(s.sourceReceiverMismatch)&&s.sourceReceiverMismatch<=2e-9;return {values,work,termination,residual,pass:values.pass&&work&&termination&&residual};}
function readTyped(rel,Type){const b=fs.readFileSync(path.join(prior,rel));return new Type(b.buffer.slice(b.byteOffset,b.byteOffset+b.byteLength));}
function readReference(info){const r=JSON.parse(fs.readFileSync(path.join(prior,'results',info.id+'.json'),'utf8'));r.symbolBytes=zlib.gunzipSync(fs.readFileSync(path.join(prior,r.symbols.path)));r.offsetArray=readTyped(r.csr.offsets.path,Uint32Array);r.sourceArray=readTyped(r.csr.sources.path,Uint32Array);r.KArray=readTyped(r.csr.K.path,Float64Array);return r;}
function qualifyCompare(q,sols,r){const symbols=q.symbols.equals(r.symbolBytes),offsets=bytes(q.offsets).equals(bytes(r.offsetArray)),sources=bytes(q.src).equals(bytes(r.sourceArray)),K=numeric(q.kv,r.KArray,2e-12,2e-12),input=exact(q.input,r.input),admission=exact(q.admission,r.admission),graph=exact(q.diagnosticGraph,r.graph),counts=exact(q.symbolCounts,r.symbolCounts),L=q.ordinaryLmax===r.ordinaryLmax,geometry=['centerEligiblePairs','centerGuardRejectedPairs','pairCalls','positiveRotorTerms'].every(k=>q.geometryWork[k]===r.geometryWork[k]);const direct=solveCompare(sols.O,r.solutions.direct),picard=solveCompare(sols.P,r.solutions.picard),trace=numeric(sols.P.iterates.flat(),r.solutions.picard.iterates.flat(),0,1e-9),lastChange=sols.P.lastChange===r.solutions.picard.lastChange;return {trace,lastChange,symbols,offsets,sources,K,input,admission,graph,counts,L,geometry,direct,picard,pass:symbols&&offsets&&sources&&K.pass&&input&&admission&&graph&&counts&&L&&geometry&&direct.pass&&picard.pass&&trace.pass&&lastChange};}
function persist(id,label,q,sols){
 const t0=performance.now(),gz=zlib.gzipSync(q.symbols,{level:6});assert(gz.length<=64*1024**2,'compressed symbol guard exceeded');const t1=performance.now(),base=`results/${id}-${label}`,artifacts={symbols:write(base+'-symbols.u8.gz',gz)};
 artifacts.symbols.rawSha256=sha(q.symbols);artifacts.symbols.rawBytes=q.symbols.length;
 for(const [k,v] of Object.entries({offsets:q.offsets,sources:q.src,K:q.kv,a:q.aa}))artifacts[k]=write(base+'-'+k+'.bin',bytes(v));
 const doc={id,label,n:q.n,input:q.input,admission:q.admission,graph:q.diagnosticGraph,certificate:q.certificate,symbolCounts:q.symbolCounts,geometryWork:q.geometryWork,ordinaryLmax:q.ordinaryLmax,artifacts,solutions:sols,matrixHash:matrixHash(q),solutionHashes:{O:solHash(sols.O),P:solHash(sols.P)}};
 const meta=json(base+'.json',doc),end=performance.now();return {meta,compressionMs:t1-t0,hashSerializeBufferedWriteMs:end-t1,totalPersistenceMs:end-t0,fsync:false};
}
function nextUp(x){if(x===0)return Number.MIN_VALUE;const b=Buffer.alloc(8);b.writeDoubleLE(x);let u=b.readBigUInt64LE();u+=x>0?1n:-1n;b.writeBigUInt64LE(u);return b.readDoubleLE();}
const nextDown=x=>-nextUp(-x);
function controls(){
 const out=[],add=(id,positions,grid)=>out.push({id,positions,expectedGrid:grid});
 for(const x of [0,-6])for(const [name,fn] of [['below',nextDown],['exact',x=>x],['above',nextUp]])add(`radius-${x}-${name}`,[[x,0,0],[fn(x+3),0,0]],true);
 for(const [axis,name,fn] of [[0,'below',nextDown],[1,'exact',x=>x],[2,'above',nextUp]]){const rotate=v=>v.map((_,k)=>v[(k-axis+3)%3]);add(`cell-${name}`,[[0,0,0],rotate([fn(4),.25,.5]),rotate([4,0,1])],true);}
 add('signed-zero',[[-0,0,0],[0,-0,0]],true);
 const coarse=[[0,0,0],[1,.25,.5],[4,1,2]];add('coarse-origin',coarse,true);add('coarse-translated',coarse.map(a=>a.map(x=>x+2**40)),true);
 add('dense-16',Array.from({length:16},(_,i)=>[i*.05,0,.45*(i%3)]),true);
 add('span-256',[[0,0,0],[256,0,0]],true);add('span-nextUp256',[[0,0,0],[nextUp(256),0,0]],false);
 add('far-invalid258',[[0,0,0],[258,0,0]],false);add('nonfinite-nan',[[0,0,0],[NaN,0,0]],false);add('nonfinite-infinity',[[0,0,0],[Infinity,0,0]],false);add('overflow-span',[[-Number.MAX_VALUE,0,0],[Number.MAX_VALUE,0,0]],false);
 add('near-field',[[0,0,0],[0,0,.02]],true);add('duplicates',[[1,1,1],[1,1,1]],true);
 return out;
}
function environment(){const cores=os.cpus(),read=(cmd,args)=>{try{return cp.execFileSync(cmd,args,{encoding:'utf8',timeout:3000}).trim();}catch{return null;}};const power=read('/usr/bin/pmset',['-g']);return {cpuModel:cores[0]?.model??null,logicalCores:cores.length,physicalCores:Number(read('/usr/sbin/sysctl',['-n','hw.physicalcpu']))||null,installedRAMBytes:os.totalmem(),architecture:os.arch(),platform:os.platform(),kernel:os.release(),node:process.version,v8:process.versions.v8,nodeExecutableSha256:sha(fs.readFileSync(process.execPath)),nodeOptionsEmpty:!process.env.NODE_OPTIONS,executionFlagCount:process.execArgv.length,executionFlags:process.execArgv.every(x=>/^--[a-z-]+$/.test(x))?process.execArgv:[],clock:'performance.now monotonic milliseconds',loadAverage:os.loadavg(),lowPowerMode:power?.match(/lowpowermode\s+(\d+)/)?.[1]??null,powerSource:read('/usr/bin/pmset',['-g','batt'])?.match(/Now drawing from '([^']+)'/)?.[1]??null,threads:'one JS worker; runtime helper threads unspecified',pidOmitted:true};}
const evidence={kind:'fixed-pose-coupled-cost',constants:kernel.constants,complete:false,controls:[],qualification:[],cache:[],timings:[],readings:[],environmentStart:environment()};
function recordTiming(workload,id,method,block,warmup,call,qualified){
 progress={phase:'timing',workload,id,method,block,warmup};guard();const result=call();
 const rec={sequence:evidence.timings.length,workload,id,method,block,warmup,totalMs:result.totalMs,phasesMs:result.phasesMs,checksum:result.check,geometryWork:result.q.geometryWork,certificate:result.q.certificate,work:result.s.work,residualWork:result.s.residualWork,iterations:result.s.iterations??1,converged:result.s.converged??true,lastChange:result.s.lastChange??null,residualLog:result.s.residualLog,sourceReceiverMismatch:result.s.sourceReceiverMismatch};
 // Duration is persisted before validation. A failure retains its timed observation.
 progress.currentTiming=rec;rec.raw=json(`results/call-${String(rec.sequence).padStart(3,'0')}-raw.json`,rec);
 evidence.timings.push(rec);
 const matrix=numeric(result.q.kv,qualified.q.kv,0,0),aa=numeric(result.q.aa,qualified.q.aa,0,0),offsets=bytes(result.q.offsets).equals(bytes(qualified.q.offsets)),sources=bytes(result.q.src).equals(bytes(qualified.q.src)),solution=solveCompare(result.s,qualified.s),mh=matrixHash(result.q),sh=solHash(result.s);
 const repeatGeometry=workload==='cached'||exact(result.q.geometryWork,qualified.q.geometryWork),certificate=exact(result.q.certificate,qualified.q.certificate),checksum=result.check===kernel.checksum(qualified.q,qualified.s);
 rec.validation={matrix,aa,offsets,sources,solution,repeatGeometry,certificate,checksum,matrixHash:mh,solutionHash:sh,hashesMatch:mh===qualified.matrixHash&&sh===qualified.solutionHash,pass:matrix.pass&&aa.pass&&offsets&&sources&&solution.pass&&repeatGeometry&&certificate&&checksum&&mh===qualified.matrixHash&&sh===qualified.solutionHash};
 json(`results/call-${String(rec.sequence).padStart(3,'0')}.json`,rec);
 if(!rec.validation.pass){json('results/repeat-failure-solution.json',{sequence:rec.sequence,solution:result.s,matrixComparison:rec.validation});throw Error('repeat output mismatch');}
}
try{
 assert(os.endianness()==='LE','little endian runtime required');assert(!process.env.NODE_OPTIONS&&process.execArgv.length===0,'runtime options forbidden');
 for(const ctl of controls()){
  progress={phase:'control',id:ctl.id};guard();const states=ctl.positions.map(v=>[...v,0,0,0,0,0,0,1,0,0,0,...Array(4).fill(kernel.constants.mg/4)]),a=kernel.build(states,'all',true,guard),b=kernel.build(states,'grid',true,guard),support=bytes(a.offsets).equals(bytes(b.offsets))&&bytes(a.src).equals(bytes(b.src)),K=numeric(a.kv,b.kv,0,0);
  const recount=q=>{const counts=Array(12).fill(0);for(const v of q.symbols)counts[v]++;return exact(counts,q.symbolCounts);};
  const rec={id:ctl.id,n:states.length,expectedGrid:ctl.expectedGrid,positionTokens:ctl.positions.map(a=>a.map(x=>Object.is(x,-0)?'-0':String(x))),all:{certificate:a.certificate,symbols:[...a.symbols],symbolCounts:a.symbolCounts,admission:a.admission,graph:kernel.fullGraph(a),geometryWork:a.geometryWork,offsets:[...a.offsets],sources:[...a.src],K:[...a.kv]},grid:{certificate:b.certificate,symbols:[...b.symbols],symbolCounts:b.symbolCounts,admission:b.admission,graph:kernel.fullGraph(b),geometryWork:b.geometryWork,offsets:[...b.offsets],sources:[...b.src],K:[...b.kv]},pass:recount(a)&&recount(b)&&a.symbols.equals(b.symbols)&&support&&K.pass&&exact(a.admission,b.admission)&&exact(kernel.fullGraph(a),kernel.fullGraph(b))&&b.certificate.useGrid===ctl.expectedGrid};
  evidence.controls.push(rec);json(`results/control-${ctl.id}.json`,rec);assert(rec.pass,'control mismatch');
 }
 const index=JSON.parse(fs.readFileSync(path.join(prior,'inputs/index.json'),'utf8')),cases=[];
 for(const info of index.cases){
  progress={phase:'qualification',id:info.id};guard();const t0=performance.now(),raw=fs.readFileSync(path.join(prior,info.path));assert(raw.length===info.n*17*8&&sha(raw)===info.sha256,'input pin mismatch');const states=Array.from({length:info.n},(_,i)=>Array.from({length:17},(_,k)=>raw.readDoubleLE((i*17+k)*8))),t1=performance.now(),ref=readReference(info),t2=performance.now();evidence.readings.push({id:info.id,inputReadDecodeMs:t1-t0,referenceLoadMs:t2-t1,inputSha256:sha(raw)});
  const item={...info,states,builders:{}};
  for(const label of ['all','grid']){
   const t=performance.now(),q=kernel.build(states,label,true,guard),order=kernel.schedule(q),sols={};
   for(const method of ['O','P']){sols[method]=kernel.solve(q,method,order,true,guard);Object.assign(sols[method],kernel.residual(q,sols[method],guard));}
   q.diagnosticGraph=kernel.fullGraph(q);const qualificationComputeMs=performance.now()-t,comparison=qualifyCompare(q,sols,ref),saved=persist(info.id,label,q,sols),rec={id:info.id,label,qualificationComputeMs,comparison,persistence:saved,matrixHash:matrixHash(q),solutionHashes:{O:solHash(sols.O),P:solHash(sols.P)}};evidence.qualification.push(rec);json(`results/qualification-${info.id}-${label}.json`,rec);assert(comparison.pass,'qualification reference mismatch');
   q.symbols=null;item.builders[label]={q,order,sols,matrixHash:rec.matrixHash,solutionHashes:rec.solutionHashes};
  }
  const t=performance.now(),cache=item.builders.grid,typedResidentBytes=cache.q.offsets.byteLength+cache.q.src.byteLength+cache.q.kv.byteLength+cache.q.aa.byteLength;
  // Uses the same qualified matrix; no extra build or solve. JS object storage is unspecified.
  assert(matrixHash(cache.q)===cache.matrixHash,'cache preparation mismatch');item.cache=cache;evidence.cache.push({id:info.id,origin:'qualified grid matrix and qualified schedule',validationMs:performance.now()-t,buildCostReportedInQualification:true,typedCSRBytes:typedResidentBytes,nominalAndS0ScalarCount:info.n*5,orderLength:cache.order.length,otherResidentState:'full decoded states, geometry, graph and reference solutions retained; JS object/Map overhead unmeasured'});cases.push(item);
 }
 const perms=['ABC','BCA','CAB','CBA','ACB','BAC'];
 function full(item,label,block,warmup){const b=item.builders[label==='A'?'all':'grid'],m=label==='C'?'P':'O';recordTiming('full',item.id,label,block,warmup,()=>kernel.query(item.states,label,guard),{q:b.q,s:b.sols[m],matrixHash:b.matrixHash,solutionHash:b.solutionHashes[m]});}
 for(const item of cases)for(const label of 'ABC')full(item,label,-1,true);
 for(let block=0;block<6;block++)for(let j=0;j<4;j++){const caseIndex=(j+block)%4,item=cases[caseIndex];for(const label of perms[(block+caseIndex)%6])full(item,label,block,false);}
 function cache(item,m,block,warmup){const b=item.cache;recordTiming('cached',item.id,m,block,warmup,()=>kernel.cached(b.q,m,b.order,guard),{q:b.q,s:b.sols[m],matrixHash:b.matrixHash,solutionHash:b.solutionHashes[m]});}
 for(const item of cases)for(const m of 'OP')cache(item,m,-1,true);
 for(let block=0;block<6;block++)for(let j=0;j<4;j++){const item=cases[(j+block)%4];for(const m of block%2?'PO':'OP')cache(item,m,block,false);}
 const ids=cases.map(x=>x.id),expected=[];const addExpected=(workload,id,method,block,warmup)=>expected.push({workload,id,method,block,warmup});for(const id of ids)for(const m of 'ABC')addExpected('full',id,m,-1,true);for(let b=0;b<6;b++)for(let j=0;j<4;j++){const c=(j+b)%4;for(const m of perms[(b+c)%6])addExpected('full',ids[c],m,b,false);}for(const id of ids)for(const m of 'OP')addExpected('cached',id,m,-1,true);for(let b=0;b<6;b++)for(let j=0;j<4;j++)for(const m of b%2?'PO':'OP')addExpected('cached',ids[(j+b)%4],m,b,false);assert(evidence.controls.length===21&&evidence.qualification.length===8&&evidence.timings.length===140&&evidence.timings.every((r,i)=>exact({workload:r.workload,id:r.id,method:r.method,block:r.block,warmup:r.warmup},expected[i])),'completed schedule mismatch');
 evidence.complete=true;evidence.environmentEnd=environment();evidence.memory={sampledPeakRSSBytes:maxRSS,processResourceUsage:process.resourceUsage(),platformMaxRSSUnits:'Node maxRSS in kilobytes; separate sampled RSS in bytes'};evidence.newScientificBytesBeforeEvidence=outputBytes;json('results/evidence.json',evidence);
 console.log(JSON.stringify({complete:true,controls:evidence.controls.length,qualifications:evidence.qualification.length,timingCalls:evidence.timings.length}));
}catch(e){
 evidence.complete=false;const allowed=['RSS guard exceeded','internal wall guard exceeded','output guard exceeded','input pin mismatch','positive coefficient guard exceeded','compressed symbol guard exceeded','control mismatch','qualification reference mismatch','repeat output mismatch','Picard nonconvergence','solve domain rejected','candidate order/uniqueness failure','invalid alpha','cache preparation mismatch','completed schedule mismatch','runtime options forbidden'];
 const error={message:allowed.includes(e.message)?e.message:'unexpected execution exception',exceptionClass:e.constructor.name,progress,completedControls:evidence.controls.length,completedQualifications:evidence.qualification.length,completedTimings:evidence.timings.length};write('results/failure.json',JSON.stringify(error)+'\n',true);write('results/partial-evidence.json',JSON.stringify(evidence)+'\n',true);process.exitCode=1;console.log(JSON.stringify(error));
}
