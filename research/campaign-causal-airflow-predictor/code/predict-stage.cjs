'use strict';
// Causal supply only: no model import, wake evaluation or filesystem access.
function scalar(current, previous, alpha) {
  if (!Number.isFinite(current) || current < 0 || (previous !== null && (!Number.isFinite(previous) || previous < 0)) || !Number.isFinite(alpha) || alpha < 0 || alpha > 1) throw Error('Invalid predictor input');
  const raw = previous === null ? current : current + alpha * (current - previous);
  if (!Number.isFinite(raw)) throw Error('Nonfinite predictor output');
  return {raw, value: Math.max(0, raw)};
}
function createHistory(kind, period) {
  if (!['H','P'].includes(kind) || !Number.isSafeInteger(period) || period <= 0) throw Error('Invalid supply configuration');
  let current = null, previous = null, tick = null;
  const make = () => ({vectors:0, scalars:0, startupHoldVectors:0, clampedScalars:0, clampedVectors:0, affectedRotorIds:[], affectedRefreshTicks:[], minimumRaw:null, mostNegative:null, zeroWindVehicleVectors:0, nonzeroWindVehicleVectors:0});
  const stats = {stage:make(), diagnostic:make()}, affected = {stage:new Set(), diagnostic:new Set()}, intervals = {stage:new Set(), diagnostic:new Set()};
  function accept(winds, t) {
    if (!Number.isSafeInteger(t) || (tick === null ? t !== 0 : t !== tick + period) || !Array.isArray(winds) || !winds.length || winds.some(r=>!Array.isArray(r)||r.length!==4||r.some(x=>!Number.isFinite(x)||x<0))) throw Error('Invalid scheduled history');
    if(current && winds.length !== current.length) throw Error('History shape changed');
    previous = current; current = winds.map(r=>r.slice()); tick = t;
  }
  function supply(t, role, location={}) {
    if (!current || !Object.hasOwn(stats,role)) throw Error('Uninitialized supply');
    const alpha = (t-tick)/period, s=stats[role];
    if(!Number.isFinite(alpha)||alpha<0||alpha>1) throw Error('Stage outside current refresh interval');
    let clamped=false; s.vectors++; if(kind==='P'&&previous===null)s.startupHoldVectors++;
    const winds=current.map((row,i)=>row.map((u,r)=>{
      const q=scalar(u,kind==='P'&&previous!==null?previous[i][r]:null,alpha);s.scalars++;
      if(s.minimumRaw===null||q.raw<s.minimumRaw)s.minimumRaw=q.raw;
      if(q.raw<0){s.clampedScalars++;clamped=true;affected[role].add(4*i+r);intervals[role].add(tick);if(s.mostNegative===null||q.raw<s.mostNegative.raw)s.mostNegative={raw:q.raw,tick:t,receiver:i,rotor:r,alpha,current:u,previous:previous?.[i][r]??null,refreshTick:tick,...location};}
      return q.value;
    }));
    for(const row of winds)row.every(x=>x===0)?s.zeroWindVehicleVectors++:s.nonzeroWindVehicleVectors++;
    s.clampedVectors+=+clamped;s.affectedRefreshTicks=Array.from(intervals[role]).sort((a,b)=>a-b);s.affectedRotorIds=Array.from(affected[role]).sort((a,b)=>a-b);
    return winds;
  }
  return {accept,supply,stats,get tick(){return tick;},snapshot:()=>({current,previous,tick})};
}
module.exports={scalar,createHistory};
