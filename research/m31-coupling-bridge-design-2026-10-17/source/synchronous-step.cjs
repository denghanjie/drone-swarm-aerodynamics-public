'use strict';
// UNADOPTED draft alternative; prefer extending the prior motion-feedback adapter.
// Retained for design provenance only; not an executable experiment allocation.
// UNEXECUTED source candidate, not connected to any frozen experiment.
const D = require('./derivative.cjs');
function need(ok, code) { if (!ok) throw new Error(code); }
function cloneRows(rows) { return rows.map(row => ({id: row.id, state: row.state.slice()})); }
function frozenInput(rows) {
  return Object.freeze({drones: Object.freeze(rows.map(row => Object.freeze({
    id: row.id, state: Object.freeze(row.state.slice())}))) });
}
function step(rows, commands, h, query, recordStage) {
  need(Array.isArray(rows) && rows.length > 0 && rows.length <= 180, 'swarm-count');
  need([.0025, .00125, .000625].includes(h), 'step-size');
  need(typeof query === 'function' && typeof recordStage === 'function', 'callbacks-required');
  const ids = rows.map(row => row.id);
  need(ids.every((id,i) => Number.isSafeInteger(id) && id >= 0 && id <= 65535 &&
    (i === 0 || id > ids[i-1])), 'ordered-stable-ids');
  need(Array.isArray(commands) && commands.length === rows.length, 'commands-count');
  const held = commands.map((row,i) => {
    need(row.id === ids[i] && Array.isArray(row.u) && row.u.length === 4 &&
      row.u.every(x => Number.isFinite(x) && x >= 0), 'command-binding');
    return row.u.slice();
  });
  const base = cloneRows(rows);
  function stage(rawRows, ordinal) {
    // Construct EVERY projected drone before the one full-swarm query.
    const projected = rawRows.map(row => ({id: row.id, state: D.projectState(row.state)}));
    const immutable = frozenInput(projected), result = query(immutable);
    if (!result || result.status !== 'native-success') {
      recordStage({ordinal, rawStage: cloneRows(rawRows), projected: cloneRows(projected),
        native: result ?? null, status: 'native-refused', consumed: false});
      throw new Error('native-stage-refused');
    }
    need(Array.isArray(result.raw) && result.raw.length === rows.length &&
      Array.isArray(result.loads) && result.loads.length === rows.length, 'native-result-shape');
    for (let i=0; i<rows.length; i++) {
      need(result.raw[i].id === ids[i] && result.loads[i].id === ids[i], 'native-id-binding');
      need(Array.isArray(result.raw[i].state) && result.raw[i].state.length === 17 &&
        result.raw[i].state.every((x,k) => Object.is(x,projected[i].state[k])), 'native-state-binding');
    }
    const consumedLoads = result.loads.map(row => ({id:row.id,
      worldForce: row.worldForce.slice(), worldMoment: row.worldMoment.slice()}));
    const derivatives = projected.map((row,i) => ({id:row.id,
      value:D.derivativeFromTotalLoad(row.state,held[i],consumedLoads[i])}));
    recordStage({ordinal, rawStage: cloneRows(rawRows), projected: cloneRows(projected),
      commands: held.map((u,i)=>({id:ids[i],u:u.slice()})), native:result,
      consumedLoads, derivatives:derivatives.map(row=>({id:row.id,value:row.value.slice()})),
      status:'consumed', consumed:true});
    return derivatives.map(row=>row.value);
  }
  const shifted = (k, scale) => base.map((row,i) => ({id:row.id,
    state:row.state.map((x,j) => x+scale*k[i][j])}));
  const k1=stage(base,0), k2=stage(shifted(k1,h/2),1),
    k3=stage(shifted(k2,h/2),2), k4=stage(shifted(k3,h),3);
  return base.map((row,i) => ({id:row.id,state:D.projectState(row.state.map((x,j) =>
    x+h*(k1[i][j]+2*k2[i][j]+2*k3[i][j]+k4[i][j])/6))}));
}
module.exports = {step};
