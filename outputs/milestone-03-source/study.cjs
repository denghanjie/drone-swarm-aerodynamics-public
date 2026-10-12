'use strict';
const fs=require('fs'),path=require('path'),{run,swept}=require('./sim.cjs');
const dir=path.resolve(__dirname,'..'),results=[];
for(const width of [.6,1.2,2.4])for(const spacing of [.3,.6])for(const speed of [.25,.5]){
 for(let seed=1;seed<=10;seed++)results.push(run({width,spacing,speed,seed}));
 console.log('Completed',width,spacing,speed);
}
fs.writeFileSync(path.join(dir,'milestone-03-study.json'),JSON.stringify({description:'120 seeded runs; five-lane local steering baseline; aerodynamic interactions disabled',results},null,2));
const demos=[.6,1.2,2.4].map(width=>run({width,spacing:.6,speed:.5,seed:1,record:true}));
fs.writeFileSync(path.join(__dirname,'demo.json'),JSON.stringify(demos));
const refinements=[.6,1.2,2.4].map(width=>{const a=results.find(r=>r.config.width===width&&r.config.spacing===.6&&r.config.speed===.5&&r.config.seed===1),b=run({...a.config,dt:.005}),c=run({...a.config,dt:.0025});return {width,coarse:a.metrics,half:b.metrics,quarter:c.metrics,halfVsQuarterFinalPositionMax:Math.max(...b.final.map((p,i)=>Math.hypot(...p.map((v,k)=>v-c.final[i][k])))),coarseVsHalfFinalPositionMax:Math.max(...a.final.map((p,i)=>Math.hypot(...p.map((v,k)=>v-b.final[i][k]))))};});
const checks=[{name:'Swept separation detects between-frame head-on contact',passed:swept([-1,0,0],[1,0,0],[1,0,0],[-1,0,0])===0},{name:'Swept separation detects parallel separated motion',passed:Math.abs(swept([0,0,0],[1,0,0],[0,1,0],[1,1,0])-1)<1e-12},{name:'Every planned configuration and seed retained, including failures',passed:results.length===120},{name:'All output metrics finite or explicitly null',passed:results.every(r=>Object.values(r.metrics).every(x=>typeof x!=='number'||Number.isFinite(x)))},{name:'Replay frames include all 50 vehicles and end at reported stop',passed:demos.every(r=>r.frames.every(f=>f.length===351)&&Math.abs(r.frames.at(-1)[0]-r.metrics.simulatedSeconds)<1e-5)},{name:'Unique valid crossings agree with per-drone event record',passed:results.every(r=>r.crossings.filter(x=>x!==null).length===r.metrics.validCrossings)},{name:'Halving step size twice preserves exemplar outcome, stop time within 0.05 s, and positions within 1 cm',passed:refinements.every(r=>r.coarse.validCrossings===r.half.validCrossings&&r.half.validCrossings===r.quarter.validCrossings&&r.coarse.stopReason===r.quarter.stopReason&&Math.abs(r.coarse.simulatedSeconds-r.quarter.simulatedSeconds)<.05&&r.halfVsQuarterFinalPositionMax<.01&&r.coarseVsHalfFinalPositionMax<.01)}];
fs.writeFileSync(path.join(dir,'milestone-03-verification.json'),JSON.stringify({checks,refinements,scope:'Numerical checks of engineering pilot, not physical validation. Refinement covers three displayed exemplars only.'},null,2));
const cols=['width','spacing','speed','seed','validCrossings','minSeparation','closePairs','contactPairs','invalidCrossingDrones','simulatedSeconds','stopReason'];
fs.writeFileSync(path.join(dir,'milestone-03-study.csv'),cols.join(',')+'\n'+results.map(r=>cols.map(k=>({...r.config,...r.metrics})[k]??'').join(',')).join('\n'));
console.log(JSON.stringify({checks,refinements},null,2));
