'use strict';

/* Independent arithmetic reference for the declared M28 finite-support model.
 * No imports from aero.cjs, wake.cjs, physics.cjs, or Grid; no file I/O, timers,
 * controller calls, state advancement, or experimental trajectories.
 *
 * State layout: p[0:3], v[3:6], quaternion xyzw[6:10], omega[10:13],
 *               nominal lagged rotor thrusts in newtons[13:17].
 * Caller supplies normalized quaternions. This module does not normalize them
 * silently: the frozen model's rotation likewise assumes normalized inputs.
 *
 * API:
 *   fields(states, 'sum-rotor', {onReceiver,onTerm,guard}={}) -> {
 *     winds,compensatedWinds,maximumInflow,candidates,contributions,
 *     centerChecks,rotorVisits
 *   }
 * Only the selected sum-rotor field mode is supported by this extension.
 * Scalar/root/load helpers retain the reviewed starting module's semantics.
 * The synchronous guard receives cumulative counters at receiver start/end.
 * The synchronous onReceiver callback receives a completed receiver's codes,
 * complete Float64Array terms, counts, geometry, ordinary/compensated winds
 * and local work counters. terms[4*source+rotor] is the actual already-used
 * independent source contribution in m/s, not a reconstructed or bound value.
 * Self/outside-center and valid zero classes remain exactly zero. A code-3
 * near-domain failure throws before any completed receiver is emitted, so its
 * uncomputed slot must never be interpreted as a valid zero contribution.
 *
 * Optional onTerm receives one synchronous record per valid eligible rotor
 * visit, in existing receiver/rotor/ascending-source order, after classification
 * and accumulation. No callbacks are added for self/outside-center code-0
 * slots; the complete receiver arrays retain those slots. The record contains
 * receiver, source, rotor, code, term, cumulative and receiver-local counters.
 * onTerm may stop execution by throwing, but must not mutate the input states.
 * onReceiver owns its new codes/terms arrays; the module never reuses them.
 * The caller should persist only selected terms and release full arrays when
 * possible. An omitted onTerm adds no per-term callback/object allocation.
 * No source term is evaluated twice; fields never calls a scalar/root helper.
 *
 * Static extension provenance: copied from the closed full-flock force oracle
 * at scientific source 89c3b14e6d59f2446d257bd106e3af4bbcb029c6, parent SHA-256
 * 4e1e31c00184f3dc82db8c040f5ba79313c724881d30b7c1581ddb26488270ee.
 * Only documentation/provenance and same-pass observation/storage were added.
 * Constants, rotation, wake/fades, receiver bisection, and load helpers retain
 * the parent's exact source text. Prepared by static text edits only; no case,
 * geometry, field, fixture or receiver root was executed during preparation.
 *   effectiveThrust(f0_N, U_mps) -> thrust_N (independent bisection)
 *   receiverSolution(f0_N, U_mps) -> thrust/root/residual/bracket diagnostics
 *   rotorWrench([f0,f1,f2,f3]) -> {T, t}; t is body [roll,pitch,yaw] Nm
 *   receiverWrench(nominalThrusts, winds, mode='sum-rotor') -> modeled {T,t}
 *       plus nominal/effective rotor and wrench diagnostics
 *   loads(state, winds, mode='sum-rotor') -> receiverWrench plus body/world
 *       force, world moment, and changes relative to isolated nominal thrust
 *   rotate(q_xyzw, vector3), normalizedWake(s,r), idealPower(thrust,inflow)
 *
 * 'sum-rotor' means a single source-vehicle mean wake sampled at each receiving
 * rotor center. It does NOT mean four source-rotor wakes. Source amplitude is
 * prescribed isolated-hover weight, independent of source motor states.
 * The bisection solves x^3 + alpha*x - 1 = 0, alpha=U/sqrt(f0/(2*rho*A)).
 * This preserves assumed ideal induced power, NOT measured electrical power,
 * fixed PWM, or fixed RPM. Nominal yaw torque is explicitly retained.
 *
 * This is an implementation oracle for specified equations, not aerodynamic
 * truth. The literature ledger says the source model is mean near-hover/far-
 * field flow (measured vehicles start at 230 g), whereas M28 applies it to 27 g.
 * Finite support/fades, 20-degree domain bound, aggregation, rotor-point
 * sampling, receiver law, and nominal-yaw retention are implementation
 * assumptions/extensions. No wake transport/history, fluctuations, source
 * thrust feedback, translational relative flow, walls, or ground effects are
 * represented. A prescribed moving-pose comparison tests stale-field error
 * for this quasi-static model, not physical unsteady-wake accuracy. A two-drone
 * case with only one contributing source cannot validate wake aggregation.
 */

const provenance = Object.freeze({
  purpose: 'Independent full-reference oracle with same-pass complete source terms, domain codes and compensated-sum diagnostics for a separately frozen bounded-omission challenge; prepared without execution.',
  parentIndependentSha256: '4e1e31c00184f3dc82db8c040f5ba79313c724881d30b7c1581ddb26488270ee',
  parentScientificSourceCommit: '89c3b14e6d59f2446d257bd106e3af4bbcb029c6',
  baseIndependentSha256: 'e0445be31ec647c8ddfb79533d4866dc8133e99ba5f25061bf393aab6bc58baf',
  sources: Object.freeze({
    'outputs/milestone-28-source/aero.cjs': '710b0a8f0df62208e3385ac9b8288240b379fe9248a1a645251a77c533f24a62',
    'outputs/step03a-source/wake.cjs': 'fb6d5a1d632a0023818041ef6bc39316ff8ed950f318da1a6649e2515b9fd8bc',
    'outputs/step02c-source/physics.cjs': '0c46c9beb4e831c621658f6600c074f97c95966de07f5000eb64aa476a443fa1',
    'research/m31-restart-2026-10-15/literature/annotated-ledger.md': 'c54fe9b943c76e2d146289ea6a655d1bec52b334ff72a0d4d59880f1e2cf0b37'
  }),
  arithmetic: 'Explicit rotation matrix; direct deterministic receiver/rotor/source loops; bisection rather than Newton; explicit signed rotor wrench.',
  scope: 'Binary64 equivalence up to rounding, not bitwise identity. Domain-boundary decisions are strict and may be sensitive to last-bit rotation differences.'
});

const vehicle = Object.freeze({mass: 0.027, gravity: 9.81, armCoordinate: 0.028,
  thrustCoefficient: 3.16e-10, dragMomentCoefficient: 7.94e-12});
const P = Object.freeze({rho: 1.225, rotorRadius: 0.023,
  motorDistance: 2 * Math.sqrt(2) * vehicle.armCoordinate,
  downstreamFade: 2, downstreamCutoff: 2.5, radialFade: 2, radialCutoff: 3,
  neighborRadius: 3, maxTiltDegrees: 20, nearFieldRadius: 0.15});
const wakeParameters = Object.freeze({decay: 10.11, spread: 0.07668,
  origin: -5.817, minDownstream: 2.5});
const area = Math.PI * P.rotorRadius * P.rotorRadius;
const induced = Math.sqrt(vehicle.mass * vehicle.gravity / (8 * P.rho * area));
const a = vehicle.armCoordinate;
const rotors = Object.freeze([
  Object.freeze([ a, a, 1]), Object.freeze([-a, a,-1]),
  Object.freeze([-a,-a, 1]), Object.freeze([ a,-a,-1])
]);
const modes = Object.freeze(['off', 'sum-force', 'sum-rotor', 'rss-rotor']);

class DomainError extends Error {
  constructor(message, detail) { super(message); this.name='DomainError'; this.detail=detail; }
}
function requireMode(mode) {
  if (!modes.includes(mode)) throw new Error('Unknown aerodynamic model');
}
function requireVector(v, size, label) {
  if (!v || v.length !== size || !Array.from(v).every(Number.isFinite)) {
    throw new TypeError(label+' must have '+size+' finite components');
  }
}
function requireState(s) { requireVector(s, 17, 'state'); }
function dot3(u,v) { return u[0]*v[0] + u[1]*v[1] + u[2]*v[2]; }

// Rotation matrix written independently of the original double-cross formula.
function rotate(q, v) {
  requireVector(q,4,'quaternion'); requireVector(v,3,'vector');
  const [x,y,z,w]=q, [vx,vy,vz]=v;
  return [
    (1-2*(y*y+z*z))*vx + 2*(x*y-z*w)*vy + 2*(x*z+y*w)*vz,
    2*(x*y+z*w)*vx + (1-2*(x*x+z*z))*vy + 2*(y*z-x*w)*vz,
    2*(x*z-y*w)*vx + 2*(y*z+x*w)*vy + (1-2*(x*x+y*y))*vz
  ];
}
function fade(start, end, value) {
  if (value <= start) return 1;
  if (value >= end) return 0;
  const t=(value-start)/(end-start);
  // Equivalent cubic in nonnegative factored form; independent arithmetic.
  return (1-t)*(1-t)*(1+2*t);
}
function normalizedWake(s, r) {
  if (!Number.isFinite(s)||!Number.isFinite(r)||r<0) throw new Error('Invalid normalized coordinates');
  if (s < wakeParameters.minDownstream) return {status:'outside-far-field-domain',speed:null,centerline:null,halfWidth:null,xi:null};
  const length=s-wakeParameters.origin;
  const centerline=wakeParameters.decay/length;
  const halfWidth=wakeParameters.spread*length;
  const xi=r/halfWidth;
  const denominator=1+(Math.sqrt(2)-1)*xi*xi;
  return {status:'formula-evaluated-not-independently-validated',
    speed:centerline/(denominator*denominator),centerline,halfWidth,xi};
}

function fields(states, mode='sum-rotor', options={}) {
  requireMode(mode);
  if (mode!=='sum-rotor') throw new Error('This reference-only fields API supports sum-rotor only');
  if (!Array.isArray(states)) throw new TypeError('states must be an array');
  if (!options || typeof options!=='object') throw new TypeError('field options must be an object');
  const {onReceiver,onTerm,guard}=options;
  if (onReceiver!==undefined && typeof onReceiver!=='function') throw new TypeError('onReceiver must be a function');
  if (onTerm!==undefined && typeof onTerm!=='function') throw new TypeError('onTerm must be a function');
  if (guard!==undefined && typeof guard!=='function') throw new TypeError('guard must be a function');
  states.forEach(requireState);
  let maximumInflow=0, contributions=0, candidates=0, centerChecks=0, rotorVisits=0;
  const axes=states.map(s=>rotate(s.slice(6,10),[0,0,1]));
  const cosineLimit=Math.cos(P.maxTiltDegrees*Math.PI/180);
  for(let i=0;i<states.length;i++) {
    if(axes[i][2]<cosineLimit) throw new DomainError('Source/receiver tilt exceeds exploratory20-degree limit',{
      receiver:i,source:null,rotor:null,drone:i,axis:axes[i].slice(),
      receiverState:Array.from(states[i]),centerChecks,rotorVisits,candidates,contributions
    });
  }
  const winds=[],compensatedWinds=[];
  const context=receiver=>({receiver,centerChecks,rotorVisits,candidates,contributions});
  // Every ordered pair is directly inspected; no spatial grid or neighbor helper.
  // Strict source-center distance <3 m is retained to match the declared model.
  for(let i=0;i<states.length;i++) {
    if(guard) guard(context(i));
    const receiver=states[i];
    const eligible=[];
    const codes=new Uint8Array(4*states.length),terms=new Float64Array(4*states.length),counts=Array(8).fill(0);
    counts[0]=codes.length;
    let receiverCenterChecks=0,receiverRotorVisits=0,receiverContributions=0;
    for(let j=0;j<states.length;j++) {
      if(j===i) continue;
      centerChecks++;receiverCenterChecks++;
      const source=states[j];
      if(Math.hypot(source[0]-receiver[0],source[1]-receiver[1],source[2]-receiver[2])<P.neighborRadius) {
        eligible.push(j); candidates++;
      }
    }
    const rotorWinds=[],compensatedRotorWinds=[],worldrotors=[];
    for(let k=0;k<4;k++) {
      const arm=rotate(receiver.slice(6,10),[rotors[k][0],rotors[k][1],0]);
      const point=[receiver[0]+arm[0],receiver[1]+arm[1],receiver[2]+arm[2]];
      worldrotors.push(point);
      let total=0,correction=0;
      for(const j of eligible) {
        rotorVisits++;receiverRotorVisits++;
        const source=states[j], axis=axes[j];
        const displacement=[source[0]-point[0],source[1]-point[1],source[2]-point[2]];
        const down=dot3(displacement,axis);
        let code,radial=null;
        if(down<=0) code=1;
        else if(down>=P.downstreamCutoff) code=2;
        else {
          const perpendicular=[displacement[0]-down*axis[0],displacement[1]-down*axis[1],displacement[2]-down*axis[2]];
          radial=Math.hypot(...perpendicular);
          if(down<wakeParameters.minDownstream*P.motorDistance) {
            code=radial<P.nearFieldRadius?3:4;
          } else {
            const normalizedDown=down/P.motorDistance;
            const halfWidth=wakeParameters.spread*(normalizedDown-wakeParameters.origin)*P.motorDistance;
            if(radial>=P.radialCutoff*halfWidth) code=5;
            else {
              const receiverProjection=Math.max(0,dot3(axes[i],axis));
              code=receiverProjection<=0?6:7;
              const xi=(radial/P.motorDistance)/(wakeParameters.spread*(normalizedDown-wakeParameters.origin));
              const denominator=1+(Math.sqrt(2)-1)*xi*xi;
              const normalizedSpeed=(wakeParameters.decay/(normalizedDown-wakeParameters.origin))/(denominator*denominator);
              const speed=normalizedSpeed*induced*fade(P.downstreamFade,P.downstreamCutoff,down)*
                fade(P.radialFade,P.radialCutoff,radial/halfWidth)*receiverProjection;
              // Save the already computed term without another profile evaluation.
              terms[4*j+k]=speed;
              // Ordinary ascending-source sum is preserved. Neumaier's residual
              // uses the same term and rounded addition, never another field pass.
              const next=total+speed;
              correction+=Math.abs(total)>=Math.abs(speed)?(total-next)+speed:(speed-next)+total;
              total=next;
              contributions++;receiverContributions++;
            }
          }
        }
        codes[4*j+k]=code;counts[0]--;counts[code]++;
        if(code===3) throw new DomainError('Receiver enters unmodeled near wake',{
          receiver:i,source:j,rotor:k,code,downstream:down,radial,
          receiverState:Array.from(receiver),sourceState:Array.from(source),
          receiverRotorPoint:point.slice(),sourceAxis:axis.slice(),
          centerChecks,rotorVisits,candidates,contributions,
          receiverCenterChecks,receiverRotorVisits,receiverEligible:eligible.length,
          receiverContributions,receiverPartialCounts:counts.slice()
        });
        if(onTerm) onTerm({
          receiver:i,source:j,rotor:k,code,term:terms[4*j+k],
          centerChecks,rotorVisits,candidates,contributions,
          receiverCenterChecks,receiverRotorVisits,receiverEligible:eligible.length,
          receiverContributions
        });
      }
      rotorWinds.push(total);compensatedRotorWinds.push(total+correction);
      maximumInflow=Math.max(maximumInflow,total);
    }
    winds.push(rotorWinds);compensatedWinds.push(compensatedRotorWinds);
    if(guard) guard(context(i));
    if(onReceiver) onReceiver({
      receiver:i,codes,terms,counts,axis:axes[i].slice(),
      worldrotors:worldrotors.map(point=>point.slice()),
      winds:rotorWinds.slice(),compensatedWinds:compensatedRotorWinds.slice(),
      centerChecks:receiverCenterChecks,rotorVisits:receiverRotorVisits,
      eligible:eligible.length,contributions:receiverContributions
    });
  }
  return {winds,compensatedWinds,maximumInflow,candidates,contributions,centerChecks,rotorVisits};
}

function receiverSolution(nominal, inflow) {
  if(!Number.isFinite(nominal)||nominal<0||!Number.isFinite(inflow)||inflow<0) throw new Error('Invalid receiver inputs');
  if(nominal===0) return {thrust:0,x:0,alpha:null,residual:null,bracket:[0,0],iterations:0};
  if(inflow===0) return {thrust:nominal,x:1,alpha:0,residual:0,bracket:[1,1],iterations:0};
  const alpha=inflow/Math.sqrt(nominal/(2*P.rho*area));
  if(!Number.isFinite(alpha)) throw new RangeError('Receiver alpha is outside finite binary64 range');
  // f(x)=x^3+alpha*x-1 is strictly increasing; root is in (0,min(1,1/alpha)).
  let lower=0, upper=Math.min(1,1/alpha), iterations=0;
  for(;iterations<96;iterations++) {
    const middle=lower+(upper-lower)/2;
    if(middle===lower || middle===upper) break;
    const value=middle*middle*middle+alpha*middle-1;
    if(value===0) {lower=middle;upper=middle;iterations++;break;}
    if(value<0) lower=middle; else upper=middle;
  }
  const x=lower+(upper-lower)/2;
  return {thrust:nominal*x,x,alpha,residual:x*x*x+alpha*x-1,
    bracket:[lower,upper],iterations};
}
function effectiveThrust(nominal,inflow) { return receiverSolution(nominal,inflow).thrust; }
function idealPower(thrust,inflow=0) {
  if(!Number.isFinite(thrust)||thrust<0||!Number.isFinite(inflow)||inflow<0) throw new Error('Invalid ideal-power inputs');
  return thrust*(inflow/2+Math.sqrt(inflow*inflow/4+thrust/(2*P.rho*area)));
}
function rotorWrench(thrusts) {
  requireVector(thrusts,4,'rotor thrusts');
  const [f0,f1,f2,f3]=thrusts;
  const torquePerThrust=vehicle.dragMomentCoefficient/vehicle.thrustCoefficient;
  return {T:f0+f1+f2+f3,
    t:[a*(f0+f1-f2-f3),a*(-f0+f1+f2-f3),torquePerThrust*(f0-f1+f2-f3)]};
}
function receiverWrench(nominalThrusts,winds,mode='sum-rotor') {
  requireMode(mode); requireVector(nominalThrusts,4,'nominal thrusts'); requireVector(winds,4,'inflows');
  if(winds.some(x=>x<0)) throw new Error('Inflows must be nonnegative');
  const nominal=rotorWrench(nominalThrusts);
  const effectiveThrusts=mode==='off'?Array.from(nominalThrusts):
    Array.from(nominalThrusts,(f,k)=>effectiveThrust(Math.max(0,f),winds[k]));
  const effective=rotorWrench(effectiveThrusts);
  // Match M28's derivative correction: reduced lift gives roll/pitch only.
  const t=(mode==='sum-force'||mode==='off')?nominal.t.slice():[effective.t[0],effective.t[1],nominal.t[2]];
  return {T:effective.T,t,nominal,effective,nominalThrusts:Array.from(nominalThrusts),effectiveThrusts,
    deltaT:effective.T-nominal.T,deltaMomentBody:t.map((v,k)=>v-nominal.t[k])};
}
function loads(state,winds,mode='sum-rotor') {
  requireState(state);
  const result=receiverWrench(state.slice(13,17),winds,mode),q=state.slice(6,10);
  const forceBody_N=[0,0,result.T],forceWorld_N=rotate(q,forceBody_N);
  const nominalForceWorld_N=rotate(q,[0,0,result.nominal.T]);
  return {...result,forceBody_N,forceWorld_N,momentBody_Nm:result.t.slice(),
    momentWorld_Nm:rotate(q,result.t),nominalForceWorld_N,
    deltaForceWorld_N:forceWorld_N.map((v,k)=>v-nominalForceWorld_N[k]),
    note:'Forces are rotor thrust/support forces; gravity and gyro terms are excluded. Nominal lagged motor states, not actuator targets, are the receiver input.'};
}

module.exports={provenance,vehicle,P,wakeParameters,area,induced,rotors,modes,DomainError,
  rotate,normalizedWake,fields,receiverSolution,effectiveThrust,idealPower,
  rotorWrench,wrench:rotorWrench,receiverWrench,loads};
