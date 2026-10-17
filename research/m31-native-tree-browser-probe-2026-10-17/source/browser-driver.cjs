'use strict';

// Fixed one-step, three-arm browser opportunity probe; no work runs on import.
const A = require('./browser-adapter.cjs');
const {word, number, words, project, snapshot, inputWords, copyDrones} = A;
function need(ok, message) { if (!ok) throw Error(message); }
const distance = (a, b) => Math.hypot(...a.map((x, i) => x-b[i]));
function basicState() { return [0, 0, 1, .2, -.1, .05, 0, 0, 0, 1, 0, 0, 0, .06, .06, .06, .06]; }

function createDriver({physics: F, swarm: S, Grid, geometry: G, nativeF, nativeTree}) {
  let adapter = null, used = false;
  async function wiringControls(config, emit, guard) {
    const declared = config.wiringControls.ids, reports = [];
    for (const id of declared) {
      guard(); const tilted = ['tilted-unequal', 'nominal-yaw', 'motor-lag'].includes(id);
      const state = tilted ? config.wiringControls.tilted.rawState.slice() : basicState();
      let raw = [{id: 11, state}];
      if (['reversed-load-ids', 'duplicate-load-id', 'missing-load-id'].includes(id)) {
        const second = basicState(); second[0] = 2; second[13] = .05;
        raw.push({id: 29, state: second});
      }
      if (id === 'zero-quaternion') raw[0].state.splice(6, 4, 0, 0, 0, 0);
      if (id === 'nonfinite-quaternion') raw[0].state[6] = Infinity;
      const commands = raw.map(() => tilted ? config.wiringControls.tilted.commands.slice() : [.07, .08, .09, .10]);
      const expected = config.wiringControls.rejectedIds.includes(id) ? 'rejected' : 'accepted';
      const record = {schema: 'm31-wiring-control-v1', id, expected, observed: null,
        reason: null, nativeCalls: 0, fixture: {rawInput: inputWords(raw), commandsWords: commands.map(words),
          contextToken: `control-${id}`, envelope: null}, records: [], pass: false};
      try {
        const projected = project(raw);
        const loads = projected.map(item => tilted ? {id: item.id,
          rotor: config.wiringControls.tilted.rotor.slice(), collective: config.wiringControls.tilted.collective,
          worldForce: config.wiringControls.tilted.worldForce.slice(), worldMoment: config.wiringControls.tilted.worldMoment.slice()} : adapter.nominalLoad(item));
        const envelope = {contextToken: record.fixture.contextToken, inputWords: inputWords(projected),
          result: {status: 'native-success', raw: copyDrones(projected), loads}};
        if (id === 'reversed-load-ids') envelope.result.loads.reverse();
        if (id === 'duplicate-load-id') envelope.result.loads[1].id = envelope.result.loads[0].id;
        if (id === 'missing-load-id') envelope.result.loads[1].id = 99;
        if (id === 'stale-stage-token') envelope.contextToken = 'control-previous-stage';
        if (id === 'stale-raw-input') envelope.result.raw[0].state[0] += 1;
        if (id === 'nonfinite-load') envelope.result.loads[0].worldForce[0] = NaN;
        record.fixture.envelope = snapshot(envelope);
        const bound = adapter.bind(record.fixture.contextToken, projected, envelope);
        const evaluated = projected.map((item, i) => adapter.consume(item, commands[i], bound[i]));
        record.records = evaluated.map(item => item.record);
        if (id === 'null-load') {
          record.baselineDerivativeWords = projected.map((item, i) => words(F.derivative(item.state, commands[i])));
          need(evaluated.every((item, i) => distance(item.derivative, F.derivative(projected[i].state, commands[i])) <= config.wiringControls.algebraTolerance), 'null-load-algebra');
        }
        if (id === 'tilted-unequal') {
          const body = record.records[0].bodyArmWords.map(number);
          need(distance(body, config.wiringControls.tilted.expectedBodyArm) <= config.wiringControls.algebraTolerance, 'frame-transform-algebra');
        }
        if (id === 'nominal-yaw') {
          const expectedYaw = F.wrench(projected[0].state.slice(13, 17)).t[2];
          need(record.records[0].nominalYawWord === word(expectedYaw), 'nominal-yaw-policy');
          need(word(expectedYaw) !== word(F.wrench(bound[0].rotor).t[2]), 'yaw-control-degenerate');
        }
        if (id === 'motor-lag') {
          need(evaluated[0].derivative.slice(13, 17).every((v, r) => word(v) === word((commands[0][r]-projected[0].state[13+r])/F.P.motorTau)), 'motor-lag-algebra');
        }
        if (id === 'reversed-load-ids') {
          need(record.records.every((item, i) => item.id === projected[i].id &&
            JSON.stringify(item.consumed.rotorWords) === JSON.stringify(words(projected[i].state.slice(13, 17)))), 'stable-id-algebra');
        }
        record.observed = 'accepted'; record.pass = expected === 'accepted';
      } catch (error) {
        record.observed = 'rejected'; record.reason = String(error && error.message || error);
        record.pass = expected === 'rejected' && record.reason === config.wiringControls.expectedReasons[id];
      }
      await emit('wiring-control', record); reports.push({id, pass: record.pass, observed: record.observed});
    }
    return reports;
  }

  function control(drones, arm, stepIndex, config) {
    const states = drones.map(item => item.state), grid = new Grid(states, S.P.neighbor), commands = [], records = [];
    for (let i = 0; i < states.length; i++) {
      const state = states[i], neighbors = grid.neighbors(i, S.P.neighbor);
      const velocity = S.steer(i, states, neighbors, 'boids', 'wall-priority');
      const target = {vx: velocity[0], vy: velocity[1], z: state[2]+(2.5*velocity[2]+1.5*state[5])/6,
        yaw: Math.atan2(velocity[1], velocity[0])};
      const actuator = F.control(state, target, 2.25); commands.push(actuator.u.slice());
      records.push({id: drones[i].id, stateWords: words(state), neighborIds: neighbors.map(j => drones[j].id),
        desiredVelocityWords: words(velocity), target: {vxWord: word(target.vx), vyWord: word(target.vy),
          zWord: word(target.z), yawWord: word(target.yaw)}, commandsWords: words(actuator.u),
        saturated: actuator.saturated, desiredQuaternionWords: words(actuator.qd)});
    }
    const time = stepIndex*config.integration.dt;
    return {commands, record: {schema: 'm31-coupled-controller-v1', arm,
      controlIndex: stepIndex/config.integration.stepsPerControl, stepIndex,
      relativeTimeWord: word(time), originalTimeWord: word(config.integration.timeOrigin+time), records}};
  }
  function safety(old, next) {
    const issues = [], a = old.map(item => item.state), b = next.map(item => item.state);
    for (let i = 0; i < b.length; i++) {
      if (!b[i].every(Number.isFinite) || b[i][2] < S.P.bodyRadius) issues.push({kind: 'vehicle-model-limit', id: next[i].id});
      const hits = S.obstacleContacts(a[i], b[i]);
      if (hits.length) issues.push({kind: 'obstacle-contact', id: next[i].id, hits});
    }
    for (const [i, j] of S.contactCandidates(a, b)) {
      const separation = G.segmentPair(a[i], b[i], a[j], b[j]);
      if (separation < 2*S.P.bodyRadius) issues.push({kind: 'drone-contact', ids: [next[i].id, next[j].id], distanceWord: word(separation)});
    }
    return issues;
  }

  async function run({config, append, guard, sha}) {
    need(!used, 'driver-single-use'); used = true;
    need(typeof append === 'function' && typeof guard === 'function' && typeof sha === 'function', 'driver-callbacks');
    adapter = A.createAdapter({physics: F, nativeF, nativeTree, sha});
    const browserBegin = performance.now(), appendTimings = [];
    let persistenceFailure = false;
    const counts = {coupledStages: 0, coupledCompleted: 0, primaryNativeCalls: 0,
      steps: 0, controllers: 0, initials: 0, safetyChecks: 0, wiringControls: 0};
    const cases = [], stageTimings = [];
    async function emit(kind, record) {
      const begin = performance.now();
      let ack;
      try { ack = await append(kind, record); }
      catch (error) { persistenceFailure = true; throw error; }
      appendTimings.push({kind, caseId: record.caseId || null, stageId: record.stageId || record.recordMeta && record.recordMeta.stageId || null,
        appendWallMs: performance.now()-begin, serializationMilliseconds: ack.serializationMilliseconds, transferMilliseconds: ack.transferMilliseconds,
        persistMilliseconds: ack.persistMilliseconds, recordPin: ack.recordPin});
      if (kind === 'native') counts.primaryNativeCalls++;
      if (kind === 'stage') {
        counts.coupledStages++; if (record.status === 'completed') counts.coupledCompleted++;
        stageTimings.push({caseId: record.caseId, stageId: record.stageId, status: record.status,
          methodOrder: record.methodOrder, queryTimings: record.queryTimings, commonTiming: record.commonTiming});
      }
      if (kind === 'step') counts.steps++;
      if (kind === 'controller') counts.controllers++;
      if (kind === 'initial') counts.initials++;
      if (kind === 'safety') counts.safetyChecks++;
      if (kind === 'wiring-control') counts.wiringControls++;
      return ack;
    }
    try {
      guard();
      need(config.schema === 'm31-native-tree-browser-science-v1' && config.integration.dt === .0025 &&
        config.integration.steps === 1 && config.integration.duration === .0025 && config.integration.timeOrigin === 0 &&
        config.integration.controlDt === .01 && config.integration.stepsPerControl === 4, 'fixed-integration-config');
      need(F.P.controlDt === .01 && S.P.controlDt === .01 && S.course.id === 'factory-v1', 'frozen-physics-course');
      const orders = [['F','H0','H'],['H0','H','F'],['H','F','H0'],['H','H0','F'],['H0','F','H'],['F','H','H0']];
      const fixed = [
        {caseId:'tree-t0-n64-a',n:64,seed:26171731,methodOrders:[orders[0],orders[1],orders[2],orders[3]]},
        {caseId:'tree-t0-n1000-a',n:1000,seed:26171732,methodOrders:[orders[4],orders[5],orders[0],orders[1]]},
        {caseId:'tree-t0-n5000-a',n:5000,seed:26171733,methodOrders:[orders[0],orders[1],orders[2],orders[3]]},
        {caseId:'tree-t0-n5000-b',n:5000,seed:26171734,methodOrders:[orders[4],orders[5],orders[0],orders[1]]}
      ];
      need(Array.isArray(config.cases) && config.cases.length === fixed.length &&
        config.cases.every((item, i) => Object.keys(item).length === 4 && item.caseId === fixed[i].caseId &&
          item.n === fixed[i].n && item.seed === fixed[i].seed &&
          JSON.stringify(item.methodOrders) === JSON.stringify(fixed[i].methodOrders)) &&
        JSON.stringify(config.methodOrderTable) === JSON.stringify(orders), 'fixed-case-order');
      const wiringBegin = performance.now();
      const wiring = await wiringControls(config, emit, guard);
      const wiringWallMs = performance.now()-wiringBegin;
      need(wiring.every(item => item.pass), 'fixed-control-failure');
      for (const spec of config.cases) {
        guard();
        const caseBegin = performance.now(), initializationBegin = performance.now();
        const initial = S.initial(spec.seed, spec.n).map((state, id) => ({id, state}));
        const initializationWallMs = performance.now()-initializationBegin;
        need(initial.length === spec.n && initial.every((item, i) => item.id === i &&
          item.state.length === 17 && item.state.every(Number.isFinite)), 'fresh-initial-layout');
        const initialEvidenceBegin = performance.now();
        const initialRecord = {schema: 'm31-tree-browser-initial-v1', caseId: spec.caseId,
          n: spec.n, seed: spec.seed, originalTimeWord: word(0), relativeTimeWord: word(0),
          input: inputWords(initial), initializationWallMs, inputEvidenceWallMs: null};
        initialRecord.inputEvidenceWallMs = performance.now()-initialEvidenceBegin;
        await emit('initial', initialRecord);
        const controllerBegin = performance.now();
        const update = control(initial, 'coupled', 0, config);
        const controllerWallMs = performance.now()-controllerBegin;
        update.record.caseId = spec.caseId; update.record.controllerWallMs = controllerWallMs;
        await emit('controller', update.record);
        const next = await adapter.step({drones: initial, commands: update.commands, caseId: spec.caseId,
          dt: config.integration.dt, append: emit, guard, methodOrders: spec.methodOrders});
        const safetyBegin = performance.now(), issues = safety(initial, next);
        const safetyWallMs = performance.now()-safetyBegin;
        await emit('safety', {schema: 'm31-coupled-safety-v1', caseId: spec.caseId, arm: 'coupled',
          stepIndex: 0, issues, pass: issues.length === 0, safetyWallMs});
        need(issues.length === 0, 'continuation-safety-failure');
        const report = {schema: 'm31-tree-browser-case-summary-v1', caseId: spec.caseId, n: spec.n,
          complete: true, completedSteps: 1, initializationWallMs, controllerWallMs, safetyWallMs,
          diagnosticCaseWallMs: performance.now()-caseBegin, final: inputWords(next)};
        cases.push(report); await emit('case-summary', report);
      }
      const exactCounts = Object.entries(config.expectedRuntimeCounts).every(([key, value]) => counts[key] === value);
      const summary = {schema: 'm31-tree-browser-driver-summary-v1', complete: exactCounts && cases.length === 4,
        counts, exactCounts, cases: cases.map(({caseId, n, complete, completedSteps, initializationWallMs, controllerWallMs, safetyWallMs, diagnosticCaseWallMs}) =>
          ({caseId, n, complete, completedSteps, initializationWallMs, controllerWallMs, safetyWallMs, diagnosticCaseWallMs})),
        wiringWallMs, stageTimings, appendTimings: appendTimings.slice(),
        diagnosticBrowserWallMs: performance.now()-browserBegin,
        independentReferenceAcceptance: 'pending-external-checker', qualification: 'not-established-by-producer',
        timingInterpretation: 'all-arm diagnostic wall; queryWallMs is the registered primary metric, not standalone production frame time'};
      await emit('driver-summary', summary); return summary;
    } catch (error) {
      // A failed append cannot be relabelled as a complete scientific failure record.
      if (persistenceFailure) throw error;
      const summary = {schema: 'm31-tree-browser-driver-summary-v1', complete: false, counts,
        reason: String(error && error.message || error), completedCaseIds: cases.map(item => item.caseId),
        stageTimings, appendTimings: appendTimings.slice(), diagnosticBrowserWallMs: performance.now()-browserBegin,
        qualification: 'not-established'};
      await emit('driver-failure', summary); return summary;
    }
  }
  return {run};
}
module.exports = {createDriver};
