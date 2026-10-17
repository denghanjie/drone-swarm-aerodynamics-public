'use strict';

const A = require('./adapter.cjs');
const {word, number, words, project, snapshot, freeze, inputWords, copyDrones} = A;
function need(ok, message) { if (!ok) throw Error(message); }
const distance = (a, b) => Math.hypot(...a.map((x, i) => x-b[i]));
function errors(actual, exact, hover) {
  const q = actual.slice(6, 10), target = exact.slice(6, 10);
  return {position: distance(actual.slice(0, 3), exact.slice(0, 3)),
    velocity: distance(actual.slice(3, 6), exact.slice(3, 6)),
    attitude: 2*Math.min(distance(q, target), distance(q, target.map(x => -x))),
    omega: distance(actual.slice(10, 13), exact.slice(10, 13)),
    motor: Math.max(...actual.slice(13, 17).map((x, i) => Math.abs(x-exact[13+i])/hover))};
}
function basicState() { return [0, 0, 1, .2, -.1, .05, 0, 0, 0, 1, 0, 0, 0, .06, .06, .06, .06]; }

function createDriver({physics: F, swarm: S, Grid, geometry: G, native}) {
  const adapter = A.createAdapter({physics: F, native});
  let used = false;

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

  async function manufacturedControls(config, emit, guard) {
    const reports = [], hover = F.P.m*F.P.g/4, T = config.manufactured.duration;
    for (const caseId of config.manufactured.cases) {
      const runs = [];
      for (let level = 0; level < config.manufactured.timesteps.length; level++) {
        guard(); const dt = config.manufactured.timesteps[level], count = Math.round(T/dt);
        const id = `${caseId}-h${level}`, initial = basicState();
        if (caseId !== 'translation') initial.splice(3, 3, 0, 0, 0);
        if (caseId === 'principal-spin') initial[12] = 1;
        if (caseId === 'motor-relaxation') initial.splice(13, 4, .04, .04, .04, .04);
        const command = Array(4).fill(caseId === 'motor-relaxation' ? .08 : .06), exact = initial.slice();
        if (caseId === 'translation') for (let k = 0; k < 3; k++) exact[k] += T*initial[3+k];
        if (caseId === 'principal-spin') { exact[8] = Math.sin(T/2); exact[9] = Math.cos(T/2); }
        if (caseId === 'motor-relaxation') for (let r = 0; r < 4; r++) exact[13+r] = .08+(.04-.08)*Math.exp(-T/F.P.motorTau);
        const record = {schema: 'm31-manufactured-run-v1', id, caseId, dtWord: word(dt), durationWord: word(T),
          steps: count, initial: [{id: 11, stateWords: words(initial)}], commandsWords: [words(command)],
          events: [], final: null, exactFinal: [{id: 11, stateWords: words(exact)}], errors: null,
          nativeCalls: 0, complete: false, reason: null,
          law: 'prescribed-world-force-mg-and-zero-world-arm-moment; nominal actuator yaw retained'};
        let drones = [{id: 11, state: initial.slice()}];
        try {
          for (let stepIndex = 0; stepIndex < count; stepIndex++) {
            drones = await adapter.step({drones, commands: [command], arm: id, stepIndex, dt, timeOrigin: 0,
              append: async (kind, item) => { record.events.push({kind, record: item}); }, guard,
              loadProvider: projected => projected.map(item => ({id: item.id, rotor: item.state.slice(13, 17),
                collective: item.state.slice(13, 17).reduce((a, b) => a+b, 0),
                worldForce: [0, 0, F.P.m*F.P.g], worldMoment: [0, 0, 0]}))});
          }
          record.final = drones.map(item => ({id: item.id, stateWords: words(item.state)}));
          record.errors = errors(drones[0].state, exact, hover);
          record.complete = Object.values(record.errors).every(Number.isFinite);
        } catch (error) { record.reason = String(error && error.message || error); }
        await emit('manufactured-run', record); runs.push(record);
      }
      const gates = {};
      for (const [component, tolerance] of Object.entries(config.manufactured.tolerances)) {
        const e = runs.map(run => run.errors && run.errors[component]);
        const floor = config.manufactured.roundoffFloor, ratio = config.manufactured.refinementRatio;
        const available = runs.every(run => run.complete) && e.every(x => typeof x === 'number' && Number.isFinite(x));
        gates[component] = {errors: e, tolerance, roundoffFloor: floor,
          pass: available && e[2] <= tolerance && e[1] <= Math.max(floor, ratio*e[0]) && e[2] <= Math.max(floor, ratio*e[1])};
      }
      const report = {schema: 'm31-manufactured-summary-v1', caseId,
        runIds: runs.map(run => run.id), gates, pass: Object.values(gates).every(gate => gate.pass),
        observedOrder: null, interpretation: 'analytic endpoint and contraction checks only; no convergence-order claim'};
      await emit('manufactured-summary', report); reports.push(report);
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

  async function run({config, initialInput, append, guard}) {
    need(!used, 'driver-single-use'); used = true;
    need(typeof append === 'function' && typeof guard === 'function', 'driver-callbacks');
    const counts = {coupledStages: 0, coupledCompleted: 0, primaryNativeCalls: 0, offStages: 0,
      offCompleted: 0, offNativeCalls: 0, steps: 0, controllers: 0, rawDiagnostics: 0,
      wiringControls: 0, manufacturedRuns: 0, manufacturedSummaries: 0, manufacturedStages: 0};
    async function emit(kind, record) {
      await append(kind, freeze(record));
      if (kind === 'stage') {
        const prefix = record.arm === 'coupled' ? 'coupled' : 'off'; counts[prefix+'Stages']++;
        if (record.status === 'completed') counts[prefix+'Completed']++;
        if (prefix === 'coupled') counts.primaryNativeCalls += record.nativeCalls;
        else counts.offNativeCalls += record.nativeCalls;
      }
      if (kind === 'step') counts.steps++;
      if (kind === 'controller') counts.controllers++;
      if (kind === 'raw-diagnostic') counts.rawDiagnostics++;
      if (kind === 'wiring-control') counts.wiringControls++;
      if (kind === 'manufactured-run') { counts.manufacturedRuns++; counts.manufacturedStages += record.events.filter(event => event.kind === 'stage').length; }
      if (kind === 'manufactured-summary') counts.manufacturedSummaries++;
    }
    const arms = [], failures = [];
    try {
      guard();
      need(config.schema === 'm31-coupled-science-config-v1' && config.integration.dt === .0025 &&
        config.integration.steps === 8 && config.integration.duration === .02 && config.integration.timeOrigin === 5 &&
        config.integration.controlDt === .01 && config.integration.stepsPerControl === 4, 'fixed-integration-config');
      need(F.P.controlDt === .01 && S.P.controlDt === .01 && S.course.id === 'factory-v1', 'frozen-physics-course');
      need(initialInput && Array.isArray(initialInput.drones) && initialInput.drones.length === 64, 'saved-initial-count');
      const initial = initialInput.drones.map(item => ({id: item.id, state: item.state.map(number)}));
      need(initial.every((item, i) => item.id === i && item.state.length === 17 && item.state.every(Number.isFinite)), 'saved-initial-layout');
      await emit('initial', {schema: 'm31-coupled-initial-v1', source: config.initialInput,
        originalTimeWord: word(5), relativeTimeWord: word(0), input: inputWords(initial)});
      const wiring = await wiringControls(config, emit, guard);
      const manufactured = await manufacturedControls(config, emit, guard);
      need(wiring.every(item => item.pass) && manufactured.every(item => item.pass), 'fixed-control-failure');
      for (const arm of ['coupled', 'off']) {
        let drones = copyDrones(initial), commands = null, completedSteps = 0;
        try {
          for (let stepIndex = 0; stepIndex < config.integration.steps; stepIndex++) {
            guard();
            if (stepIndex%config.integration.stepsPerControl === 0) {
              const update = control(drones, arm, stepIndex, config); commands = update.commands;
              await emit('controller', update.record);
            }
            const old = drones;
            drones = await adapter.step({drones, commands, arm, stepIndex, dt: config.integration.dt,
              timeOrigin: config.integration.timeOrigin, append: emit, guard,
              onRawK2: arm === 'coupled' && stepIndex === 0 ? async raw => {
                const records = raw.map(({id, state}) => {
                  const q = state.slice(6, 10), sum = ((q[0]*q[0]+q[1]*q[1])+q[2]*q[2])+q[3]*q[3];
                  const norm = Math.sqrt(sum), defect = Math.abs(norm-1);
                  return {id, rawStateWords: words(state), normSquareWord: word(sum), normWord: word(norm),
                    defectWord: word(defect), passesNormPrerequisite: Number.isFinite(norm) && defect <= config.projection.qTolerance};
                });
                await emit('raw-diagnostic', {schema: 'm31-raw-quaternion-prerequisite-v1',
                  stageId: 'coupled-step0-k2', qToleranceWord: word(config.projection.qTolerance), records,
                  nativeCalls: 0, referenceCalls: 0, fullPreparationAttempted: false, admissionConclusion: null,
                  interpretation: 'quaternion norm prerequisite only; passing implies neither complete geometry nor modeled-domain admission'});
              } : null});
            completedSteps++;
            const issues = safety(old, drones);
            await emit('safety', {schema: 'm31-coupled-safety-v1', arm, stepIndex, issues, pass: issues.length === 0});
            need(issues.length === 0, 'continuation-safety-failure');
          }
          const report = {arm, complete: true, completedSteps, final: inputWords(drones)};
          arms.push(report); await emit('arm-summary', report);
        } catch (error) {
          const report = {arm, complete: false, completedSteps, reason: String(error && error.message || error), final: inputWords(drones)};
          arms.push(report); failures.push(report); await emit('arm-summary', report);
        }
      }
      const exactCounts = Object.entries(config.expectedRuntimeCounts).every(([key, value]) => counts[key] === value);
      const complete = exactCounts && arms.length === 2 && arms.every(arm => arm.complete);
      const summary = {schema: 'm31-coupled-driver-summary-v1', complete, counts, exactCounts,
        arms: arms.map(({arm, complete: ok, completedSteps, reason}) => ({arm, complete: ok, completedSteps, reason: reason || null})),
        failures, independentReferenceAcceptance: 'pending-external-checker', qualification: 'not-established-by-producer'};
      await emit('driver-summary', summary); return summary;
    } catch (error) {
      const summary = {schema: 'm31-coupled-driver-summary-v1', complete: false, counts,
        reason: String(error && error.message || error), failures, qualification: 'not-established'};
      await emit('driver-failure', summary); return summary;
    }
  }
  return {run};
}

module.exports = {createDriver};
