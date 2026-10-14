'use strict';
// Post-baseline adversarial extension: expose many-weak-source accumulation and
// greedy-order symmetry breaking; not tuning data and not a performance run.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const X=require('./fixtures.cjs'),O=require('./oracle.cjs'),{comparison}=require('./checks.cjs');
const candidatePath=path.resolve(__dirname,'../src/pruned-aero.cjs'),C=require(candidatePath);
const hash=()=>crypto.createHash('sha256').update(fs.readFileSync(candidatePath)).digest('hex');
function main(){const sourceHash=hash(),records=[];
  for(const down of [2.1,2.4,2.45])for(const radialFactor of [2.85,3]){
    const states=[X.state(),...Array.from({length:24},(_,i)=>X.state([radialFactor*X.half(down)*Math.cos(2*Math.PI*i/24),radialFactor*X.half(down)*Math.sin(2*Math.PI*i/24),1+down]))];
    const reference=O.fields(states),candidate=C.fields(states,{epsilon:.04});
    const singleSources=states.slice(1).map(s=>O.fields([states[0],s]).winds[0]);
    const maxSingleContribution=Math.max(...singleSources.flat());
    const exactLoad=C.loads(states[0],reference.winds[0]),candidateLoad=C.loads(states[0],candidate.winds[0]);
    const boundCompliance=reference.winds.every((row,i)=>row.every((u,k)=>u-candidate.winds[i][k]>=-1e-12&&u-candidate.winds[i][k]<=candidate.omittedBounds[i]+1e-12));
    records.push({config:{down,radialFactor,sourceCount:24,epsilon:.04},states,reference,candidate,singleSources,maxSingleContribution,
      allSingleContributionsBelowEpsilon:maxSingleContribution<.04,aggregateMaxInflow:reference.maximumInflow,
      boundCompliance,comparison:comparison(states,reference,candidate),receiverLoads:{exact:exactLoad,candidate:candidateLoad}});
  }
  const result={utc:new Date().toISOString(),sourceHash,sourceStable:sourceHash===hash(),scope:'Constructed post-baseline stress extension, settings chosen after seeing which initial fixtures activated omission. Candidate and thresholds remain frozen. No performance claim.',records};
  fs.writeFileSync(path.join(__dirname,'raw/accumulation_probe.json'),JSON.stringify(result,null,2));
  console.log(JSON.stringify(records.map(r=>({config:r.config,maxSingle:r.maxSingleContribution,aggregateMax:r.aggregateMaxInflow,omittedPairs:r.candidate.omittedPairs,omittedBound:r.candidate.omittedBounds[0],boundCompliance:r.boundCompliance,comparison:r.comparison,receiverLoads:r.receiverLoads})),null,2));
}
if(require.main===module)main();
