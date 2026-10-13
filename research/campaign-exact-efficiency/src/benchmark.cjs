'use strict';
const fs=require('fs'),os=require('os'),path=require('path');
const {M,config,evaluator,sha,sourceHash,save,median,bootstrap,root}=require('./common.cjs'),S=require('./scenarios.cjs');
let sink=0;
function payload(fn,states,scope,index){
 if(scope==='receiver')return states.map((s,i)=>M.loads(s,fn[index].winds[i]));
 const result=fn(states);return scope==='field'?result.winds:{winds:result.winds,loads:states.map((s,i)=>M.loads(s,result.winds[i]))};
}
function batch(fn,frames,calls,scope,expected=null){
 const outputs=[],t=performance.now();for(let c=0;c<calls;c++)outputs.push(payload(fn,frames[c%frames.length],scope,c%frames.length));
 const ms=performance.now()-t,hashes=outputs.map(x=>sha(JSON.stringify(x)));
 if(expected&&hashes.some((h,i)=>h!==expected[i%frames.length]))throw Error('Timed complete-output checksum mismatch');
 sink+=ms;return {ms,outputHash:sha(JSON.stringify(hashes)),checksumPassed:expected?true:null};
}
function run({seed=4301,count=50,family='sparse',stage='development'}={}){
 const started=performance.now(),memoryBefore=process.memoryUsage(),loadBefore=os.loadavg(),hash=sourceHash(),frames=config.times.map(t=>S.cloud({seed,count,family,t})),inputHash=sha(JSON.stringify(frames));
 const fixture=`${seed}-${count}-${family}`;save(`results/fixtures/${fixture}.json`,{seed,count,family,times:config.times,frames,inputHash});
 const evaluators=Object.fromEntries(config.variants.map(v=>[v,evaluator(v)])),setupMs={};
 for(const v of config.variants){const t=performance.now();evaluator(v);setupMs[v]=performance.now()-t;}
 // Per-case warmup is equal across variants and independent of sample results.
 for(let w=0;w<3;w++)for(const v of config.variants)batch(evaluators[v],frames,3,'field');
 const pilot=batch(evaluators['previous-zero'],frames,3,'field'),calls=Math.max(3,Math.min(config.maxCallsPerBatch,Math.ceil(config.targetBatchMs/Math.max(pilot.ms,0.01)*3)));
 const repetitions=stage==='development'?config.developmentRepetitions:config.heldoutRepetitions,rows=[];
 const frozenFields=frames.map(evaluators.legacy),expected={};
 for(const scope of ['field','receiver','field+receiver']){expected[scope]={};for(const v of config.variants)expected[scope][v]=frames.map((s,i)=>sha(JSON.stringify(payload(scope==='receiver'?frozenFields:evaluators[v],s,scope,i))));}
 for(const scope of ['field','receiver','field+receiver'])for(let rep=0;rep<repetitions;rep++){
  let order=config.variants.map((_,i)=>config.variants[(i+rep)%config.variants.length]);if(rep%2)order=order.reverse();
  const ms={},checksums={};for(const v of order){try{const b=batch(scope==='receiver'?frozenFields:evaluators[v],frames,calls,scope,expected[scope][v]);ms[v]=b.ms;checksums[v]={outputHash:b.outputHash,passed:b.checksumPassed};if(performance.now()-started>55000)throw Error('55-second per-job wall cap');}catch(e){save(`results/timing/failure-${stage}-${fixture}.json`,{config:{seed,count,family,stage},sourceHash:hash,rows,current:{scope,rep,order,calls,ms,checksums},failure:{name:e.constructor.name,message:e.message},memory:process.memoryUsage()});throw e;}}
  rows.push({scope,rep,order,calls,ms,checksums});save(`results/timing/partial-${stage}-${fixture}.json`,{config:{seed,count,family,stage},sourceHash:hash,rows});
 }
 const summaries=[];
 for(const scope of ['field','receiver','field+receiver'])for(const variant of config.variants)for(const reference of ['legacy','previous-zero']){
  if(variant===reference)continue;const selected=rows.filter(r=>r.scope===scope),ratios=selected.map(r=>r.ms[variant]/r.ms[reference]),ci=bootstrap(ratios);
  summaries.push({scope,variant,reference,medianRatio:median(ratios),bootstrap95:ci,medianMsPerCall:median(selected.map(r=>r.ms[variant]/r.calls)),qualified:median(ratios)<=.9&&ci[1]<1});
 }
 const result={config:{seed,count,family,stage},sourceHash:hash,sourceUnchanged:hash===sourceHash(),inputHash,inputHashAfter:sha(JSON.stringify(frames)),inputUnchanged:inputHash===sha(JSON.stringify(frames)),memory:{before:memoryBefore,after:process.memoryUsage()},processObservation:{pid:process.pid,loadBefore,loadAfter:os.loadavg()},inputFile:`fixtures/${fixture}.json`,times:config.times,setupMs,warmupCallsPerVariant:9,pilot:{variant:'previous-zero',calls:3,ms:pilot.ms},calls,repetitions,rows,summaries,wallSeconds:(performance.now()-started)/1000,finiteSink:Number.isFinite(sink),runtime:{node:process.version,platform:process.platform,arch:process.arch,cpuModel:os.cpus()[0]?.model,cpuCount:os.cpus().length},scope:'Serial CPU wall time. Field includes validation, refreshed geometry, grid, kernels and owned output. Receiver is an identical-code noise control using saved legacy fields. Checksum processing is excluded; temporary output retention is included. Combined performs fields and all rotor loads. No browser/GPU/physical fidelity claim.'};
 save(`results/timing/${stage}-${fixture}.json`,result);return result;
}
if(require.main===module){const r=run(JSON.parse(process.argv[2]||'{}'));console.log(JSON.stringify({config:r.config,wallSeconds:r.wallSeconds,summaries:r.summaries.filter(s=>s.scope==='field'&&s.reference==='previous-zero')}));}
module.exports={run};
