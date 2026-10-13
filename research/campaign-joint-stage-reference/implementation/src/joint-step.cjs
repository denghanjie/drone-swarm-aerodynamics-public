'use strict';
// A synchronized full-state RK4 step. Does not update discrete commands.
const M = require('./exact-aero.cjs');
function geometryCopy(states) {
  return states.map((s, drone) => {
    if (s.length !== 17 || !s.every(Number.isFinite)) throw Object.assign(new Error('Invalid raw stage state'), {detail:{drone}});
    const n = Math.hypot(...s.slice(6, 10));
    if (!(n > 0) || !Number.isFinite(n)) throw Object.assign(new Error('Invalid stage quaternion norm'), {detail:{drone,n}});
    const copy = s.slice();
    for (let k = 6; k < 10; k++) copy[k] /= n;
    return copy;
  });
}
function synchronizedRK4(states, h, evaluateStage, project = x => x) {
  const next = (derivatives, scale) => states.map((s,i) => s.map((v,k) => v + scale * derivatives[i][k]));
  const k1 = evaluateStage(states, 1, 0);
  const k2 = evaluateStage(next(k1,h/2), 2, .5);
  const k3 = evaluateStage(next(k2,h/2), 3, .5);
  const k4 = evaluateStage(next(k3,h), 4, 1);
  return project(states.map((s,i) => s.map((v,k) => v + h*(k1[i][k]+2*k2[i][k]+2*k3[i][k]+k4[i][k])/6)));
}
function endpointNormalize(states) {
  return states.map((s,drone) => {
    const n = Math.hypot(...s.slice(6,10));
    if (!(n > 0) || !Number.isFinite(n)) throw Object.assign(new Error('Invalid endpoint quaternion norm'),{detail:{drone,n}});
    const out=s.slice(); for(let k=6;k<10;k++)out[k]/=n; return out;
  });
}
function jointStep(states, commands, h, {field=M.createEvaluator({variant:'lean'}), beforeStage=()=>{}, afterStage=()=>{}, onProjection=()=>{},beforeDerivative=()=>{},afterDerivative=()=>{}}={}) {
  return synchronizedRK4(states,h,(raw,stage,fraction)=>{
    let geometry=null, result=null, derivatives=null,failingDrone=null;
    try {
      geometry=geometryCopy(raw);
      beforeStage({raw,geometry,commands,stage,fraction});
      result=field(geometry); // One complete swarm field before any derivative.
      derivatives=[];raw.forEach((s,i)=>{failingDrone=i;beforeDerivative({stage,drone:i});const d=M.A.derivative(s,commands[i],result.winds[i],'sum-rotor');derivatives.push(d);afterDerivative({stage,drone:i});failingDrone=null;});
      if(derivatives.some(row=>!row.every(Number.isFinite)))throw Error('Nonfinite joint-stage derivative');
      afterStage({raw,geometry,commands,stage,fraction,result,derivatives});
      return derivatives;
    } catch(error) {
      error.stageEvidence={stage,fraction,raw,geometry,commands,field:result?.winds||null,derivatives,failingDrone,guard:{name:error.constructor.name,message:error.message,detail:error.detail||null}};
      throw error;
    }
  },raw=>{
    try { const accepted=endpointNormalize(raw);
    onProjection({raw,accepted,quaternionNormDefects:raw.map(s=>Math.hypot(...s.slice(6,10))-1),projectionSizes:raw.map((s,i)=>Math.hypot(...s.slice(6,10).map((v,k)=>v-accepted[i][6+k])))});
    return accepted; } catch(error){error.endpointEvidence={raw,rawCombinedEndpoint:raw,commands,guard:{name:error.constructor.name,message:error.message,detail:error.detail||null}};throw error;}
  });
}
module.exports={geometryCopy,synchronizedRK4,endpointNormalize,jointStep};
