'use strict';
const assert=require('assert/strict');
const {M,config,evaluator,sha,sourceHash,save}=require('./common.cjs'),S=require('./scenarios.cjs');
function compare(states){
 const base=evaluator('legacy')(states),rows=[];
 for(const variant of config.variants.filter(v=>v!=='legacy')){
  const result=evaluator(variant)(states);let inflow=0,force=0,moment=0,bitwise=true;
  for(let i=0;i<states.length;i++){
   for(let r=0;r<4;r++){assert(Number.isFinite(result.winds[i][r]));inflow=Math.max(inflow,Math.abs(base.winds[i][r]-result.winds[i][r]));bitwise=bitwise&&Object.is(base.winds[i][r],result.winds[i][r]);}
   const a=M.loads(states[i],base.winds[i]),b=M.loads(states[i],result.winds[i]);
   force=Math.max(force,Math.hypot(...a.force.map((x,k)=>x-b.force[k])));moment=Math.max(moment,Math.hypot(...a.moment.map((x,k)=>x-b.moment[k])));
  }
  assert(inflow<=config.inflowAbsoluteTolerance&&force<=config.forceAbsoluteTolerance&&moment<=config.momentAbsoluteTolerance,'equivalence gate');
  rows.push({variant,inflow,force,moment,bitwise,counters:result.counters||result});
 }
 return rows;
}
function run(stage='tiny'){
 const cases=stage==='tiny'?S.fixtures():config[stage==='development'?'developmentSeeds':'heldoutSeeds'].flatMap(seed=>config.correctnessCounts.flatMap(count=>config.families.flatMap(family=>config.times.map(t=>({name:`${seed}-${count}-${family}-${t}`,config:{seed,count,family,t},states:S.cloud({seed,count,family,t})})))));
 const rows=[],failures=[];
 for(const c of cases){try{const metrics=compare(c.states);rows.push({name:c.name,config:c.config,stateHash:sha(JSON.stringify(c.states)),metrics});}catch(e){failures.push({...c,error:{name:e.constructor.name,message:e.message,detail:e.detail}});break;}}
 const report={stage,sourceHash:sourceHash(),cases:rows.length,rows,failures,passed:!failures.length};save(`results/checks-${stage}.json`,report);return report;
}
if(require.main===module){const r=run(process.argv[2]||'tiny');console.log(JSON.stringify({stage:r.stage,passed:r.passed,cases:r.cases,failures:r.failures.length,sourceHash:r.sourceHash}));if(!r.passed)process.exitCode=1;}
module.exports={compare,run};
