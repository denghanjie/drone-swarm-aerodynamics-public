'use strict';
// The control and safety function bodies below are copied verbatim from the
// prior qualified driver. This wrapper only supplies their original dependencies.
const F=require('../../m31-native-fresh-transfer-2026-10-17/source/vendor/generation/step02c-source/physics.cjs');
const S=require('../../m31-native-fresh-transfer-2026-10-17/source/vendor/generation/milestone-31-source/sim.cjs');
const G=require('../../m31-native-fresh-transfer-2026-10-17/source/vendor/generation/milestone-31-source/geometry.cjs');
const {Grid}=require('../../m31-native-fresh-transfer-2026-10-17/source/vendor/generation/milestone-31-source/grid.cjs');
const {words,word}=require('../../m31-coupled-stage-qualification-2026-10-17/source/adapter.cjs');
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


module.exports={control,safety};
