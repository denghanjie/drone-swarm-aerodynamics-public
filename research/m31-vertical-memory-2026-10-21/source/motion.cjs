'use strict';
// Inherited Boids/controller wrapper with one explicit bounded vertical memory term.
// The safety function is unchanged. No physics constants or aerodynamic loads change.
const F=require('../../m31-native-fresh-transfer-2026-10-17/source/vendor/generation/step02c-source/physics.cjs');
const S=require('../../m31-native-fresh-transfer-2026-10-17/source/vendor/generation/milestone-31-source/sim.cjs');
const G=require('../../m31-native-fresh-transfer-2026-10-17/source/vendor/generation/milestone-31-source/geometry.cjs');
const {Grid}=require('../../m31-native-fresh-transfer-2026-10-17/source/vendor/generation/milestone-31-source/grid.cjs');
const {words,word}=require('../../m31-coupled-stage-qualification-2026-10-17/source/adapter.cjs');
  function control(drones, arm, stepIndex, config, memory) {
    const states = drones.map(item => item.state), grid = new Grid(states, S.P.neighbor), commands = [], records = [];
    for (let i = 0; i < states.length; i++) {
      const state = states[i], neighbors = grid.neighbors(i, S.P.neighbor);
      const velocity = S.steer(i, states, neighbors, 'boids', 'wall-priority');
      const item=memory[i], before={integralWord:word(item.integral),previousErrorWord:word(item.previousError),updates:item.updates};
      const increment=item.updates===0?0:(2.5*.01)*item.previousError;
      const unclamped=item.integral+increment;
      item.integral=Math.max(-5,Math.min(5,unclamped));
      item.previousError=velocity[2]-state[5];item.updates++;
      const after={integralWord:word(item.integral),previousErrorWord:word(item.previousError),updates:item.updates};
      const target = {vx: velocity[0], vy: velocity[1], z: state[2]+((2.5*velocity[2]+1.5*state[5])+item.integral)/6,
        yaw: Math.atan2(velocity[1], velocity[0])};
      const actuator = F.control(state, target, 2.25); commands.push(actuator.u.slice());
      records.push({verticalMemory:{before,incrementWord:word(increment),unclampedWord:word(unclamped),after},id: drones[i].id, stateWords: words(state), neighborIds: neighbors.map(j => drones[j].id),
        desiredVelocityWords: words(velocity), target: {vxWord: word(target.vx), vyWord: word(target.vy),
          zWord: word(target.z), yawWord: word(target.yaw)}, commandsWords: words(actuator.u),
        saturated: actuator.saturated, desiredQuaternionWords: words(actuator.qd)});
    }
    const time = stepIndex*config.integration.dt;
    return {commands, record: {schema: 'm31-vertical-memory-controller-v1', arm,
      controlIndex: stepIndex/config.integration.stepsPerControl, globalControlIndex:config.integration.timeOrigin/.01+stepIndex/config.integration.stepsPerControl, stepIndex,
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


function initialMemory(n){return Array.from({length:n},(_,id)=>({id,integral:0,previousError:0,updates:0}));}
function memoryWords(memory){return memory.map(x=>({id:x.id,integralWord:word(x.integral),previousErrorWord:word(x.previousError),updates:x.updates}));}
module.exports={control,safety,initialMemory,memoryWords};
