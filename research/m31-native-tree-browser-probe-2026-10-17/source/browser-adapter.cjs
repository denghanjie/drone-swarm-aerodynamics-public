'use strict';

// SOURCE ONLY. Dependency injection performs no work until the caller invokes it.
const scratch = new DataView(new ArrayBuffer(8));
function word(value) {
  if (typeof value !== 'number') throw new TypeError('binary64 number required');
  scratch.setFloat64(0, value, false);
  return scratch.getUint32(0, false).toString(16).padStart(8, '0') +
    scratch.getUint32(4, false).toString(16).padStart(8, '0');
}
function number(hex) {
  if (typeof hex !== 'string' || !/^[0-9a-f]{16}$/.test(hex)) throw Error('invalid binary64 word');
  scratch.setUint32(0, parseInt(hex.slice(0, 8), 16), false);
  scratch.setUint32(4, parseInt(hex.slice(8), 16), false);
  return scratch.getFloat64(0, false);
}
const words = values => Array.from(values, word);
const cross = (a, b) => [a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]];
function need(ok, message) { if (!ok) throw Error(message); }
function finiteVector(value, n) {
  return Array.isArray(value) && value.length === n && value.every(Number.isFinite);
}
function copyDrones(drones) { return drones.map(({id, state}) => ({id, state: state.slice()})); }
function inputWords(drones) { return {drones: drones.map(({id, state}) => ({id, state: words(state)}))}; }
function freeze(value) {
  if (value && typeof value === 'object' && !Object.isFrozen(value)) {
    for (const item of Object.values(value)) freeze(item);
    Object.freeze(value);
  }
  return value;
}
// Retains malformed native responses without requiring their success schema.
// Numeric values, including NaN and signed zero, retain their exact words.
function snapshot(value, seen = new Map()) {
  if (typeof value === 'number') return {binary64Word: word(value)};
  if (value === null || typeof value === 'string' || typeof value === 'boolean') return value;
  if (typeof value !== 'object') return {unserializableType: typeof value, text: String(value)};
  if (seen.has(value)) return {reference: seen.get(value)};
  seen.set(value, seen.size);
  if (value instanceof ArrayBuffer) return {arrayBufferBytes: Array.from(new Uint8Array(value))};
  if (ArrayBuffer.isView(value)) return {viewType: value.constructor.name,
    viewBytes: Array.from(new Uint8Array(value.buffer, value.byteOffset, value.byteLength))};
  const isArray = Array.isArray(value), keys = Reflect.ownKeys(value);
  const denseArray = isArray && keys.length === value.length+1 &&
    Array.from({length: value.length}, (_, i) => Object.hasOwn(value, i)).every(Boolean);
  const out = denseArray ? [] : Object.create(null);
  if (isArray && !denseArray) out.arrayLength = value.length;
  for (const key of keys) {
    if (isArray && key === 'length') continue;
    const descriptor = Object.getOwnPropertyDescriptor(value, key);
    out[String(key)] = Object.hasOwn(descriptor, 'value') ? snapshot(descriptor.value, seen) : {accessor: true};
  }
  return out;
}
function project(drones) {
  const seen = new Set();
  return drones.map(({id, state}) => {
    need(Number.isSafeInteger(id) && id >= 0 && !Object.is(id, -0) && !seen.has(id), 'projection-id');
    seen.add(id); need(finiteVector(state, 17), 'projection-state');
    const q = state.slice(6, 10);
    const normSquare = ((q[0]*q[0] + q[1]*q[1]) + q[2]*q[2]) + q[3]*q[3];
    const norm = Math.sqrt(normSquare);
    need(norm > 0 && Number.isFinite(norm), 'projection-quaternion');
    const next = state.slice();
    for (let k = 0; k < 4; k++) next[6+k] = q[k]/norm;
    need(next.every(Number.isFinite), 'projection-nonfinite');
    return {id, state: next, rawStateWords: words(state), normSquareWord: word(normSquare), normWord: word(norm)};
  });
}

function createAdapter({physics: F, nativeF, nativeTree, sha}) {
  need(F && nativeF && nativeTree && typeof nativeF.query === 'function' &&
    typeof nativeTree.query === 'function' && typeof sha === 'function', 'dependencies');
  function nominalLoad({id, state}) {
    const rotor = state.slice(13, 17), q = state.slice(6, 10), axis = F.rotate(q, [0, 0, 1]);
    let collective = 0; const worldMoment = [0, 0, 0];
    for (let r = 0; r < 4; r++) {
      collective += rotor[r];
      const offset = F.rotate(q, [F.rotors[r][0], F.rotors[r][1], 0]);
      const lever = cross(offset, axis);
      for (let k = 0; k < 3; k++) worldMoment[k] += lever[k]*rotor[r];
    }
    return {id, rotor, collective, worldForce: axis.map(x => x*collective), worldMoment};
  }
  function bind(contextToken, projected, envelope) {
    need(envelope && envelope.contextToken === contextToken, 'stale-stage-token');
    const expected = inputWords(projected);
    need(JSON.stringify(envelope.inputWords) === JSON.stringify(expected), 'stale-input-words');
    const result = envelope.result;
    need(result && result.status === 'native-success', 'native-non-success');
    need(Array.isArray(result.raw) && result.raw.length === projected.length, 'native-raw-shape');
    need(JSON.stringify(inputWords(result.raw)) === JSON.stringify(expected), 'native-raw-binding');
    need(Array.isArray(result.loads) && result.loads.length === projected.length, 'native-load-count');
    const byId = new Map();
    for (const load of result.loads) {
      need(load && Number.isSafeInteger(load.id) && !byId.has(load.id), 'native-load-id');
      need(finiteVector(load.rotor, 4) && Number.isFinite(load.collective) &&
        finiteVector(load.worldForce, 3) && finiteVector(load.worldMoment, 3), 'native-load-shape');
      byId.set(load.id, load);
    }
    need(projected.every(item => byId.has(item.id)), 'native-load-missing-id');
    return projected.map(item => byId.get(item.id));
  }
  function consume(item, command, load) {
    need(finiteVector(command, 4), 'command-shape');
    const state = item.state, q = state.slice(6, 10), w = state.slice(10, 13);
    const derivative = F.derivative(state, command);
    for (let k = 0; k < 3; k++) derivative[3+k] = load.worldForce[k]/F.P.m;
    derivative[5] -= F.P.g;
    const bodyArm = F.rotate([-q[0], -q[1], -q[2], q[3]], load.worldMoment);
    const nominalYaw = F.wrench(state.slice(13, 17)).t[2];
    const totalBody = [bodyArm[0], bodyArm[1], bodyArm[2] + nominalYaw];
    const gyro = cross(w, w.map((value, k) => value*F.P.I[k]));
    for (let k = 0; k < 3; k++) derivative[10+k] = (totalBody[k]-gyro[k])/F.P.I[k];
    need(finiteVector(derivative, 17), 'derivative-nonfinite');
    return {derivative, record: {id: item.id, rawStateWords: item.rawStateWords,
      stateWords: words(state), normSquareWord: item.normSquareWord, normWord: item.normWord,
      commandsWords: words(command), nominalMotorWords: words(state.slice(13, 17)),
      consumed: {rotorWords: words(load.rotor), collectiveWord: word(load.collective),
        worldForceWords: words(load.worldForce), worldMomentWords: words(load.worldMoment)},
      bodyArmWords: words(bodyArm), totalBodyWords: words(totalBody), nominalYawWord: word(nominalYaw),
      gyroWords: words(gyro), derivativeWords: words(derivative)}};
  }
  async function evaluate({raw, commands, context, append, guard, methodOrder}) {
    const {caseId, arm, stepIndex, stageIndex, relativeTime, originalTime, dt} = context;
    const stageId = `${caseId}-step${stepIndex}-k${stageIndex}`;
    const evidenceBegin = performance.now();
    const record = {schema: 'm31-tree-browser-stage-v1', stageId, caseId, arm, stepIndex, stageIndex,
      relativeTimeWord: word(relativeTime), originalTimeWord: word(originalTime), dtWord: word(dt),
      status: 'pending', nativeInput: null, nativeRefs: [], records: [], reason: null,
      nativeCalls: 0, rawBeforeProjection: inputWords(raw), commandsBeforeEvaluation: commands.map(words),
      methodOrder: methodOrder.slice(), queryTimings: [], semanticAgreement: false,
      commonTiming: {projectionWallMs: 0, inputEvidenceWallMs: 0, bindingAndDerivativeWallMs: 0}};
    let projected, returned, scientificError = null, persistenceError = null;
    try {
      guard();
      const projectionBegin = performance.now();
      record.commonTiming.inputEvidenceWallMs += projectionBegin-evidenceBegin;
      projected = project(raw);
      record.commonTiming.projectionWallMs = performance.now()-projectionBegin;
      const inputBegin = performance.now();
      need(commands.length === projected.length && commands.every(u => finiteVector(u, 4)), 'commands-count');
      record.nativeInput = inputWords(projected);
      const inputCanonical = JSON.stringify(record.nativeInput);
      const hash = await sha(inputCanonical);
      record.commonTiming.inputEvidenceWallMs += performance.now()-inputBegin;
      let baseline = null, baselineMethod = null, hResult = null;
      for (let queryOrderIndex = 0; queryOrderIndex < methodOrder.length; queryOrderIndex++) {
        const method = methodOrder[queryOrderIndex], native = method === 'F' ? nativeF : nativeTree;
        const timing = {method, queryOrderIndex, queryWallMs: null, encodeWallMs: null,
          semanticCompareWallMs: null, appendWallMs: null, serializationMilliseconds: null, transferMilliseconds: null, persistMilliseconds: null};
        record.queryTimings.push(timing); record.nativeCalls++;
        let result, inputUnchanged = false;
        // The same canonical input words are independently decoded/copied inside each common timer.
        const queryBegin = performance.now();
        try {
          const input = {drones: record.nativeInput.drones.map(item => ({id: item.id, state: item.state.map(number)}))};
          result = native.query(input, method, guard, method === 'F' ? null : {treeEvidence: true});
          // The unchanged native query has consumed every delivered load, ID and status word.
          // Check the actual submitted object, not just the native result's owned raw copy.
          try { inputUnchanged = JSON.stringify(inputWords(input.drones)) === inputCanonical; }
          catch (_) { inputUnchanged = false; }
          if (!inputUnchanged) record.nativeInputMutation = {method, actualInput: snapshot(input)};
        } catch (error) {
          timing.queryWallMs = performance.now()-queryBegin;
          record.nativeThrown = {method, message: String(error && error.message || error), detail: snapshot(error)};
          throw error;
        }
        timing.queryWallMs = performance.now()-queryBegin;
        const encodeBegin = performance.now();
        let encoded;
        try { encoded = native.encodeEvidence(result); }
        catch (error) {
          timing.encodeWallMs = performance.now()-encodeBegin;
          record.nativeMalformed = {method, encodingError: String(error && error.message || error), response: snapshot(result)};
          throw Error('native-evidence-schema');
        }
        timing.encodeWallMs = performance.now()-encodeBegin;
        const compareBegin = performance.now();
        const difference = baseline === null ? null : require('./compact-codec.cjs').semanticDifference(baseline, encoded);
        timing.semanticCompareWallMs = performance.now()-compareBegin;
        const body = {recordMeta: {caseId, stageId, queryOrderIndex, inputUnchanged}, ...encoded,
          caseId: stageId, semanticInputSha256: hash, inlineInputCanonicalSha256: hash,
          auditTiming: {queryWallMs: timing.queryWallMs, encodeWallMs: timing.encodeWallMs,
            semanticCompareWallMs: timing.semanticCompareWallMs}};
        const appendBegin = performance.now();
        let ack;
        try { ack = await append('native', body); } catch (error) { persistenceError = error; throw error; }
        timing.appendWallMs = performance.now()-appendBegin;
        need(ack && ack.durable === true && ack.recordPin, 'native-durable-ack');
        timing.serializationMilliseconds = ack.serializationMilliseconds;
        timing.transferMilliseconds = ack.transferMilliseconds;
        timing.persistMilliseconds = ack.persistMilliseconds;
        record.nativeRefs.push({method, recordPin: ack.recordPin});
        need(inputUnchanged, 'native-input-mutated');
        if (difference !== null) {
          record.firstMismatch = {baselineMethod, method, path: difference};
          throw Error('native-semantic-mismatch');
        }
        if (baseline === null) { baseline = encoded; baselineMethod = method; }
        need(result && result.status === 'native-success', 'native-non-success');
        if (method === 'H') hResult = result;
      }
      need(methodOrder.length === 3 && new Set(methodOrder).size === 3 &&
        methodOrder.every(method => ['F', 'H0', 'H'].includes(method)) && hResult, 'three-arm-method-order');
      record.semanticAgreement = true;
      const consumeBegin = performance.now();
      const loads = bind(stageId, projected, {contextToken: stageId, inputWords: record.nativeInput, result: hResult});
      const evaluated = projected.map((item, i) => consume(item, commands[i], loads[i]));
      record.records = evaluated.map(item => item.record); record.status = 'completed';
      returned = {derivatives: evaluated.map(item => item.derivative), stageId, projected};
      record.commonTiming.bindingAndDerivativeWallMs = performance.now()-consumeBegin;
    } catch (error) {
      if (persistenceError) throw persistenceError;
      record.status = 'failed'; record.reason = String(error && error.message || error);
      if (projected) record.projectedOnFailure = inputWords(projected);
      scientificError = error;
    }
    // Exactly one stage append; all full native arms are already separate durable records.
    await append('stage', record);
    if (scientificError) throw scientificError;
    return returned;
  }
  async function step({drones, commands, caseId, dt, append, guard, methodOrders}) {
    const arm = 'coupled', stepIndex = 0, timeOrigin = 0;
    let combinationBegin = performance.now(), rkCombinationWallMs = 0;
    const base = copyDrones(drones), t = stepIndex*dt, stageIds = [];
    rkCombinationWallMs += performance.now()-combinationBegin;
    const stage = async (raw, stageIndex, relativeTime) => {
      const evaluated = await evaluate({raw, commands, append, guard, methodOrder: methodOrders[stageIndex-1],
        context: {caseId, arm, stepIndex, stageIndex, relativeTime, originalTime: timeOrigin+relativeTime, dt}});
      stageIds.push(evaluated.stageId); return evaluated.derivatives;
    };
    const add = (k, scale) => {
      const begin = performance.now();
      const output = base.map((item, i) => ({id: item.id,
        state: item.state.map((value, j) => value+scale*k[i][j])}));
      rkCombinationWallMs += performance.now()-begin; return output;
    };
    const k1 = await stage(base, 1, t), rawK2 = add(k1, dt/2);
    const k2 = await stage(rawK2, 2, t+dt/2);
    const k3 = await stage(add(k2, dt/2), 3, t+dt/2);
    const k4 = await stage(add(k3, dt), 4, t+dt);
    combinationBegin = performance.now();
    const rawFinal = base.map((item, i) => ({id: item.id, state: item.state.map((value, j) =>
      value+dt*(((k1[i][j]+2*k2[i][j])+2*k3[i][j])+k4[i][j])/6)}));
    rkCombinationWallMs += performance.now()-combinationBegin;
    let final = null, projectionError = null;
    const projectionBegin = performance.now();
    try { final = project(rawFinal); } catch (error) { projectionError = error; }
    const endpointProjectionWallMs = performance.now()-projectionBegin;
    const evidenceBegin = performance.now();
    const record = {schema: 'm31-tree-browser-step-v1', stepId: `${caseId}-step${stepIndex}`,
      caseId, arm, stepIndex, relativeTimeWord: word(t+dt), originalTimeWord: word(timeOrigin+(t+dt)), dtWord: word(dt),
      status: projectionError ? 'failed' : 'completed', reason: projectionError ? String(projectionError.message || projectionError) : null,
      start: base.map(item => ({id: item.id, stateWords: words(item.state)})), stageIds,
      rawFinal: rawFinal.map(item => ({id: item.id, stateWords: words(item.state)})),
      final: final && final.map(item => ({id: item.id, stateWords: words(item.state),
        normSquareWord: item.normSquareWord, normWord: item.normWord})),
      commonTiming: {rkCombinationWallMs, endpointProjectionWallMs, endpointEvidenceWallMs: null}};
    record.commonTiming.endpointEvidenceWallMs = performance.now()-evidenceBegin;
    await append('step', record);
    if (projectionError) throw projectionError;
    return copyDrones(final);
  }
  return {nominalLoad, bind, consume, evaluate, step};
}

module.exports = {createAdapter, word, number, words, project, snapshot, freeze, inputWords, copyDrones, cross};
