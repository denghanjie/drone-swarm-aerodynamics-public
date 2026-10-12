'use strict';
// Execute only in the exclusive serial timing slot.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto'),os=require('node:os');
const {performance}=require('node:perf_hooks');
const X=require('./fixtures.cjs'),{comparison}=require('./checks.cjs');
const cfg=require('./timing_config.json');
const file=path.resolve(__dirname,'../src/pruned-aero.cjs');
const hash=p=>crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const startHash=hash(file),C=require(file),A=C.A;
const quantile=(xs,p)=>{const s=[...xs].sort((a,b)=>a-b),n=(s.length-1)*p,l=Math.floor(n);return s[l]+(s[Math.ceil(n)]-s[l])*(n-l);};
const stats=xs=>({median:quantile(xs,.5),q25:quantile(xs,.25),q75:quantile(xs,.75),min:Math.min(...xs),max:Math.max(...xs)});
const shuffle=(xs,r)=>{const a=[...xs];for(let i=a.length-1;i>0;i--){const j=Math.floor(r()*(i+1));[a[i],a[j]]=[a[j],a[i]];}return a;};
const funcs={legacy:s=>A.fields(s,'sum-rotor'),exact:s=>C.fields(s,{epsilon:0}),'epsilon_0.01':s=>C.fields(s,{epsilon:.01}),'epsilon_0.04':s=>C.fields(s,{epsilon:.04})};
const checksum=r=>r.winds.reduce((v,row,i)=>v+row.reduce((a,u,k)=>a+(i+1)*(k+1)*u,0),0);
function boot(xs){const random=X.rng(77352),med=[];for(let j=0;j<2000;j++)med.push(quantile(Array.from({length:xs.length},()=>xs[Math.floor(random()*xs.length)]),.5));return [quantile(med,.025),quantile(med,.975)];}
function main(){
  if(!process.argv.includes('--serial-slot'))throw Error('Exclusive serial timing slot is required; this script is not a functional smoke test.');
  const started=Date.now(),random=X.rng(cfg.order_seed),rows=[],fixtureRecords=[],checks=[];
  let serial=0;for(const scenario of cfg.scenarios){
    const states=X.lattice(scenario.n,scenario.spacing,cfg.seed),reference=funcs.exact(states);fixtureRecords.push({...scenario,states});
    const expected={};for(const name of cfg.methods){const out=funcs[name](states);expected[name]=checksum(out);const check=comparison(states,reference,out);
      if(!check.finiteAndShape||!check.approximationTolerancePass)throw Error('Correctness failed for '+scenario.id+'/'+name);
      checks.push({scenario:scenario.id,method:name,comparison:check,candidates:out.candidates,counters:out.counters||null,checksum:expected[name]});}
    for(const name of shuffle(cfg.methods,random))for(let i=0;i<cfg.warmup_evaluations_per_method;i++)funcs[name](states);
    for(let repetition=0;repetition<cfg.repetitions;repetition++)for(const name of shuffle(cfg.methods,random)){
      const before=process.memoryUsage(),t0=performance.now();let sum=0,last;
      for(let i=0;i<scenario.evaluations_per_repetition;i++){last=funcs[name](states);sum+=checksum(last);}
      const elapsed=performance.now()-t0,after=process.memoryUsage();
      if(!Number.isFinite(sum)||Math.abs(sum-expected[name]*scenario.evaluations_per_repetition)>1e-8*Math.max(1,Math.abs(sum)))throw Error('Nonfinite or nondeterministic checksum');
      rows.push({serial:serial++,scenario:scenario.id,repetition,method:name,evaluations:scenario.evaluations_per_repetition,elapsedMs:elapsed,perFieldMs:elapsed/scenario.evaluations_per_repetition,checksum:sum,before,after});
      if(Date.now()-started>115000)throw Error('Time budget reached');
    }
  }
  const summaries=cfg.scenarios.map(s=>({scenario:s.id,n:s.n,spacing:s.spacing,methods:Object.fromEntries(cfg.methods.map(m=>{
    const own=rows.filter(r=>r.scenario===s.id&&r.method===m),exact=rows.filter(r=>r.scenario===s.id&&r.method==='exact');
    const ratios=own.map(r=>r.perFieldMs/exact.find(x=>x.repetition===r.repetition).perFieldMs),interval=boot(ratios),ratioMedian=quantile(ratios,.5);
    return [m,{...stats(own.map(x=>x.perFieldMs)),pairedRatioMedian:ratioMedian,pairedRatio95Bootstrap:interval,provisionalSpeedGate:ratioMedian<=.9&&interval[1]<1}];}))}));
  const endHash=hash(file),result={utc:new Date().toISOString(),config:cfg,sourceHashStart:startHash,sourceHashEnd:endHash,sourceStable:startHash===endHash,
    node:process.version,platform:process.platform,arch:process.arch,cpuModels:[...new Set(os.cpus().map(x=>x.model))],cpuCount:os.cpus().length,
    loadAverage:os.loadavg(),resourceUsage:process.resourceUsage(),totalElapsedMs:Date.now()-started,checks,rows,summaries};
  fs.writeFileSync(path.join(__dirname,'raw/timing_fixtures.json'),JSON.stringify(fixtureRecords));
  fs.writeFileSync(path.join(__dirname,'raw/independent_timing.json'),JSON.stringify(result,null,2));
  console.log(JSON.stringify({sourceStable:result.sourceStable,totalElapsedMs:result.totalElapsedMs,summaries},null,2));
  if(!result.sourceStable)process.exitCode=2;
}
if(require.main===module)main();
