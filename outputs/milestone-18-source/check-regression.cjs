const fs=require('fs'),path=require('path'),assert=require('assert/strict'),old=require('../milestone-17-source/sim.cjs'),current=require('./sim.cjs');
const cases=JSON.parse(fs.readFileSync(path.resolve(__dirname,'../milestone-16-study.json')));let compared=0;
for(const r of cases)for(const states of [r.initial,r.final])for(const scenario of ['tight','staggered','slalom'])for(let i=0;i<states.length;i++){
 assert.deepEqual(current.steer(i,states,0,'steering-only',scenario),old.steer(i,states,0,'steering-only',scenario));compared++;
 if(scenario==='slalom')assert.deepEqual(current.steer(i,states,0,'interior',scenario),old.steer(i,states,0,'steering-only',scenario));
}
fs.writeFileSync(path.resolve(__dirname,'../milestone-18-regression.json'),JSON.stringify({passed:true,compared,description:'Exact baseline-command regression on development initial/final state fixtures, all3 geometries. Interior mode also identical to baseline on sphere geometry. This is a command-level regression, not a new full-trajectory sphere trial.'},null,2));
console.log('baseline command comparisons:',compared);
