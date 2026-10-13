const assert=require('assert'),fs=require('fs'),{repair,residual}=require('./wall-filter.cjs');let checks=0;
function near(a,b,tol=1e-8){assert(Math.hypot(...a.map((x,k)=>x-b[k]))<tol);checks++;}
near(repair([-.5,.2,0],[{n:[1,0,0],lower:.1}]).velocity,[.1,.2,0]);
near(repair([2,0,0],[]).velocity,[.9,0,0]);
const corner=[{n:[1,0,0],lower:.2},{n:[0,1,0],lower:.3}];near(repair([-.5,-.2,0],corner).velocity,[.2,.3,0]);
near(repair([1,1,0],[{n:[1,0,0],lower:.8}]).velocity,[.8,Math.sqrt(.81-.64),0],1e-7);
assert(!repair([0,0,0],[{n:[1,0,0],lower:1}]).converged);checks++;
const A=require('../milestone-26-source/sim.cjs'),B=require('./sim.cjs');
for(const count of [50,1000,5000]){const opts={count,seed:1501,dt:.0025,duration:.1,record:false};const a=A.run(opts),b=B.run(opts);assert.deepStrictEqual(a.final,b.final);assert.deepStrictEqual(a.metrics,b.metrics);checks+=2;}
near(repair([-.5,.2,0],[{n:[1,0,0,...Array(14).fill(0)],lower:.1}]).velocity,[.1,.2,0]);
for(const count of [50,1000,5000]){const c=B.run({count,seed:1501,dt:.0025,duration:.1,record:false,filter:'wall-priority'});assert(c.final.flat().every(Number.isFinite));assert(Number.isFinite(c.diagnostics.maxWallAfter));assert.strictEqual(c.metrics.stopReason,null);checks+=3;}
fs.writeFileSync(__dirname+'/../milestone-30-checks.json',JSON.stringify({checks,passed:true,scope:'Analytic wall/speed projections, infeasible cap case, exact baseline endpoints and metrics at 50/1000/5000 over 0.1s'},null,2));console.log({checks,passed:true});
