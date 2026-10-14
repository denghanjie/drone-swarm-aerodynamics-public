'use strict';
const fs=require('fs'),path=require('path'),crypto=require('crypto'),assert=require('assert/strict'),zlib=require('zlib');
const M=require('./pruned-aero.cjs'),S=require('./scenarios.cjs'),config=require('../configs/campaign.json');
const output=path.join(__dirname,'../results');
const norm=x=>Math.hypot(...x),diff=(a,b)=>a.map((x,i)=>x-b[i]);
const quantile=(a,p)=>{const b=a.slice().sort((x,y)=>x-y);return b[Math.min(b.length-1,Math.floor(p*b.length))]||0;};
function sha(file){return crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex');}
function snapshotComparison(states,epsilon,full,original){
  const candidate=M.fields(states,{epsilon}),rows=[];
  let referenceError=0;
  for(let i=0;i<states.length;i++){
    const truth=M.loads(states[i],full.winds[i]),approx=M.loads(states[i],candidate.winds[i]);
    const bounds=M.loadBounds(states[i],candidate.winds[i],candidate.omittedBounds[i]);
    const inflowError=diff(full.winds[i],candidate.winds[i]),forceError=norm(diff(truth.force,approx.force)),momentError=norm(diff(truth.moment,approx.moment));
    if(original)referenceError=Math.max(referenceError,...diff(original.winds[i],full.winds[i]).map(Math.abs));
    assert(inflowError.every(e=>e>=-1e-12&&e<=candidate.omittedBounds[i]+1e-12),'accumulated inflow bound');
    assert(forceError<=bounds.force+1e-12&&momentError<=bounds.moment+1e-13,'force and moment response bound');
    assert(forceError<=config.forceToleranceWeightFraction*M.F.P.m*M.F.P.g,'frozen force criterion');
    assert(momentError<=config.momentToleranceWeightArmFraction*M.F.P.m*M.F.P.g*M.F.P.a,'frozen moment criterion');
    rows.push({receiver:i,fullWind:full.winds[i],candidateWind:candidate.winds[i],inflowError,omittedBound:candidate.omittedBounds[i],fullLoads:truth,candidateLoads:approx,forceError,momentError,bounds});
  }
  assert(referenceError<=1e-12,'original source equivalence');
  return {epsilon,referenceError,counters:candidate.counters,rows};
}
function correctness({quick=false}={}){
  const started=performance.now(),sourceHash=sha(path.join(__dirname,'pruned-aero.cjs'));
  const rawFile=quick?'accuracy-smoke.jsonl':'accuracy-raw.jsonl.gz';
  const stream=fs.openSync(path.join(output,rawFile),'w');
  // Concatenated gzip members retain every raw JSONL record while bounding disk
  // growth. Python gzip and standard gzip -dc read all members normally.
  const writeRecord=record=>{const line=JSON.stringify(record)+'\n';fs.writeSync(stream,quick?line:zlib.gzipSync(line,{level:1}));};
  const errors=[],failures=[],totals={snapshots:0,receiverComparisons:0,omittedPairs:0,maxReferenceError:0,maxInflowError:0,maxForceError:0,maxMomentError:0};
  const seeds=quick?[3391]:[...config.developmentSeeds,...config.heldoutSeeds],counts=quick?[16,50]:config.counts,times=quick?[0,.5,1]:Array.from({length:101},(_,i)=>i/100);
  for(const seed of seeds)for(const count of counts)for(const family of config.families)for(const t of times){
    const caseConfig={seed,count,family,t},states=S.cloud(caseConfig);
    try{
      const full=M.fields(states),original=M.A.fields(states,'sum-rotor');
      for(const epsilon of config.epsilonsMS){
        const result=snapshotComparison(states,epsilon,full,original);
        writeRecord({config:caseConfig,...result});
        totals.omittedPairs+=result.counters.omittedPairs;totals.maxReferenceError=Math.max(totals.maxReferenceError,result.referenceError);
        for(const row of result.rows){totals.receiverComparisons++;totals.maxInflowError=Math.max(totals.maxInflowError,...row.inflowError);totals.maxForceError=Math.max(totals.maxForceError,row.forceError);totals.maxMomentError=Math.max(totals.maxMomentError,row.momentError);errors.push([row.forceError,row.momentError]);}
      }
      totals.snapshots++;
    }catch(e){failures.push({config:caseConfig,name:e.constructor.name,message:e.message,detail:e.detail,states});writeRecord({config:caseConfig,failure:failures.at(-1)});if(!(e instanceof M.DomainError)){fs.closeSync(stream);throw e;}}
    if(performance.now()-started>180000)throw Error('Correctness wall cap exceeded');
  }
  fs.closeSync(stream);
  const report={sourceHash,rawFile,scope:'same prescribed states; all four rotors; exact model-relative bounds; no physical validation',quick,config,totals,force:{p95:quantile(errors.map(x=>x[0]),.95),rms:Math.sqrt(errors.reduce((s,x)=>s+x[0]**2,0)/Math.max(1,errors.length))},moment:{p95:quantile(errors.map(x=>x[1]),.95),rms:Math.sqrt(errors.reduce((s,x)=>s+x[1]**2,0)/Math.max(1,errors.length))},failures,wallSeconds:(performance.now()-started)/1000,passed:failures.length===0,sourceUnchanged:sourceHash===sha(path.join(__dirname,'pruned-aero.cjs'))};
  fs.writeFileSync(path.join(output,quick?'accuracy-smoke-summary.json':'accuracy-summary.json'),JSON.stringify(report,null,2));return report;
}

let sink=0;
function evalBatch(variant,frames,cycles){
  const start=performance.now();
  for(let i=0;i<cycles;i++){const states=frames[i%frames.length];const result=variant==='legacy'?M.A.fields(states,'sum-rotor'):M.fields(states,{epsilon:variant});sink+=result.maximumInflow;}
  return performance.now()-start;
}
function bootstrapRatios(pairs,seed=701){const random=S.rng(seed),ratios=[];for(let b=0;b<5000;b++){const sample=[];for(let i=0;i<pairs.length;i++)sample.push(pairs[Math.floor(random()*pairs.length)]);ratios.push(quantile(sample,.5));}return [quantile(ratios,.025),quantile(ratios,.975)];}
function timing(){
  const started=performance.now(),sourceHash=sha(path.join(__dirname,'pruned-aero.cjs')),rows=[];
  const variants=['legacy',0,...config.epsilonsMS];
  for(const count of [100,200])for(const family of config.families)for(const seed of config.heldoutSeeds){
    const frames=Array.from({length:10},(_,i)=>S.cloud({count,family,seed,t:i/10}));
    // Validate every exact input frame before timing; fields/load validation is excluded from timed scope.
    for(const states of frames){const full=M.fields(states),original=M.A.fields(states,'sum-rotor');for(const epsilon of config.epsilonsMS)snapshotComparison(states,epsilon,full,original);}
    for(let w=0;w<2;w++)for(const v of variants)evalBatch(v,frames,frames.length);
    const pilot=evalBatch(0,frames,10),cycles=Math.max(10,Math.min(1000,Math.ceil(50/Math.max(pilot,1)*10)));
    const reps=[];
    for(let rep=0;rep<config.timingRepetitions;rep++){
      const order=variants.map((_,k)=>variants[(k+rep)%variants.length]);if(rep%2)order.reverse();
      const ms={};for(const v of order)ms[String(v)]=evalBatch(v,frames,cycles);
      reps.push({rep,order,cycles,ms});
    }
    const summary=config.epsilonsMS.map(epsilon=>{const ratios=reps.map(r=>r.ms[String(epsilon)]/r.ms['0']);return {epsilon,medianRatio:quantile(ratios,.5),pairedBootstrap95:bootstrapRatios(ratios),ratios,qualified:quantile(ratios,.5)<=.9&&bootstrapRatios(ratios)[1]<1};});
    const row={count,family,seed,inputStateHashes:frames.map(s=>crypto.createHash('sha256').update(JSON.stringify(s)).digest('hex')),reps,summary};rows.push(row);
    fs.writeFileSync(path.join(output,'timing-partial.json'),JSON.stringify({sourceHash,rows},null,2));
    if(performance.now()-started>270000)throw Error('Initial timing lease wall cap exceeded');
  }
  const report={sourceHash,sourceUnchanged:sourceHash===sha(path.join(__dirname,'pruned-aero.cjs')),scope:'Node CPU fields() wall time including state validation, axes/rotor preparation, broad phase, bounds, retained kernels, result allocation; excludes receiver loads, integrator, rendering and serialization',budgetVsExactMeaning:'Zero and positive budgets perform identical bounds and exact-zero culling; legacy reports same-equation optimization separately',rows,wallSeconds:(performance.now()-started)/1000,sinkIsFinite:Number.isFinite(sink),physicalAccuracyClaim:false};
  fs.writeFileSync(path.join(output,'timing.json'),JSON.stringify(report,null,2));return report;
}
if(require.main===module){fs.mkdirSync(output,{recursive:true});const mode=process.argv[2];let report;if(mode==='smoke')report=correctness({quick:true});else if(mode==='accuracy')report=correctness();else if(mode==='timing')report=timing();else throw Error('Use smoke, accuracy, or timing');console.log(JSON.stringify({mode,wallSeconds:report.wallSeconds,totals:report.totals,failures:report.failures?.length,rows:report.rows?.length,sourceUnchanged:report.sourceUnchanged}));}
module.exports={snapshotComparison,correctness,timing};
