'use strict';

/* Candidate analytical envelope for the unchanged upright M28 pair model.
 * No experiments, field evaluations, dynamics, timers, or file writes here.
 *
 * Construction:
 *   const {bound}=createBound(independentOracle, {
 *     heldThrust: (nominal, U) => production.effectiveThrust(nominal, U),
 *     heldThrustLabel: 'M28 production effectiveThrust'
 *   });
 * Or use this module's bound(), which lazily requires ./independent.cjs and
 * uses that oracle's receiverSolution(...).thrust for held loads too.
 * Endpoint thrust enclosures ALWAYS use independent receiverSolution brackets.
 * Injection permits centering on the exact floating-point held loads used by
 * the caller, instead of calling an independent approximation "actual".
 *
 * bound({states, delta, heldWinds}) takes exactly two 17-component states:
 * receiver index 0, source index 1. states are the HOLD ANCHOR states. delta is
 * a supplied nonnegative bound in metres on the Euclidean change of each
 * source-center/receiver-rotor relative displacement throughout the hold.
 * This module cannot infer or verify a future displacement guarantee from one
 * snapshot. The caller must establish delta independently for its entire hold.
 * heldWinds is the actual four-element receiver inflow array being held.
 *
 * Frozen scope: both orientations [0,0,0,1], angular velocities zero, and all
 * nominal rotor thrust states exactly m*g/4 for BOTH vehicles. Arbitrary finite
 * translational velocities are allowed; neither velocity nor source thrust is
 * used to change the quasi-static source amplitude. The caller must keep the
 * frozen orientation/thrust contract throughout the hold, not just at anchor.
 * Other present states, a lower downstream endpoint below 2.5*D, bad deltas,
 * and nonfinite arithmetic are rejected, never silently continued.
 *
 * In real arithmetic, downstream and radial distances each vary by at most
 * delta. C and downstream fade F are nonincreasing; H is positive increasing;
 * Q is nonnegative nonincreasing. Independent-factor products enclose U:
 *   Ulo = C(dhi)*F(dhi)*Q(rhi/H(dlo))
 *   Uhi = C(dlo)*F(dlo)*Q(rlo/H(dhi)).
 * C=induced*10.11/(d/D+5.817), H=.07668*(d+5.817*D), and
 * Q(x)=fade(2,3,x)/(1+(sqrt(2)-1)*x*x)^2.
 * Wind margins of 1e-12 m/s and per-rotor thrust margins of 1e-14 N are
 * explicitly NON-CERTIFIED numerical padding. The oracle's binary64 bisection
 * brackets are not outward-rounded interval arithmetic, and the accumulation
 * of force/moment intervals is not formally rounded outward either.
 * Therefore this is an analytical envelope subject to numerical checking,
 * NOT a formally certified floating-point enclosure or physical safety bound.
 *
 * M28's source-center 3 m candidate cutoff is redundant for any positive wake
 * in this upright support: source-center distance is at most
 * hypot(2.5, 3*H(2.5)+sqrt(2)*a) < 3. The constructor checks that constant
 * inequality. Outside downstream/radial support the factors are zero.
 * We still reject dmin<2.5D even if the field might be zero elsewhere; this
 * deliberately avoids any near-field extension or ambiguous domain crossing.
 *
 * Returned signed differences are instantaneous rotor-derived load MINUS
 * the load from actual held rotor thrusts. Vector order: [T_N, roll_Nm,
 * pitch_Nm]. Independent intervals may be conservative because rotor and
 * distance correlations are discarded. Yaw stays nominal and is not bounded
 * as a new observable here. No claims about wake memory, calibrated receiver
 * response, controller performance, or physical validation follow.
 */

const NUMERICAL_MARGIN=Object.freeze({wind_mps:1e-12,thrust_N:1e-14,
  formallyCertified:false});
const CONTRACT=Object.freeze({receiver:0,source:1,vehicles:2,
  orientation:'identity quaternion xyzw',nominalThrust:'m*g/4 per rotor',
  errorOrder:Object.freeze(['thrust_N','roll_Nm','pitch_Nm']),
  errorSign:'instantaneous minus held',
  displacement:'source-center to receiver-rotor relative displacement, Euclidean metres',
  floatingPointCertification:false});

function createBound(oracle,options={}) {
  if(!oracle || typeof oracle.receiverSolution!=='function' || !oracle.P ||
     !oracle.vehicle || !oracle.rotors || !oracle.wakeParameters) {
    throw new TypeError('Independent oracle with receiverSolution and M28 constants is required');
  }
  const P=oracle.P,v=oracle.vehicle,w=oracle.wakeParameters;
  const expected={rho:1.225,rotorRadius:.023,motorDistance:2*Math.sqrt(2)*.028,
    downstreamFade:2,downstreamCutoff:2.5,radialFade:2,radialCutoff:3,
    neighborRadius:3,nearFieldRadius:.15,maxTiltDegrees:20};
  for(const key of Object.keys(expected)) if(P[key]!==expected[key]) {
    throw new Error('Oracle does not match frozen M28 parameter '+key);
  }
  if(v.mass!==.027 || v.gravity!==9.81 || v.armCoordinate!==.028 ||
     w.decay!==10.11 || w.spread!==.07668 || w.origin!==-5.817 || w.minDownstream!==2.5) {
    throw new Error('Oracle does not match frozen vehicle/wake constants');
  }
  const a=.028,D=expected.motorDistance,nominal=.027*9.81/4;
  const rotorOffsets=[[a,a,1],[-a,a,-1],[-a,-a,1],[a,-a,-1]];
  if(JSON.stringify(oracle.rotors)!==JSON.stringify(rotorOffsets)) {
    throw new Error('Oracle rotor order does not match frozen M28 order');
  }
  const area=Math.PI*.023*.023;
  const induced=Math.sqrt(.027*9.81/(8*1.225*area));
  const H=d=>.07668*(d+5.817*D);
  const C=d=>induced*10.11/(d/D+5.817);
  function fade(begin,end,x) {
    if(x<=begin)return 1;
    if(x>=end)return 0;
    const t=(x-begin)/(end-begin);
    return (1-t)*(1-t)*(1+2*t);
  }
  const F=d=>fade(2,2.5,d);
  function Q(xi) {
    if(xi>=3)return 0;
    const denominator=1+(Math.sqrt(2)-1)*xi*xi;
    return fade(2,3,xi)/(denominator*denominator);
  }
  const maximumPositiveSupportCenterDistance=Math.hypot(2.5,3*H(2.5)+Math.sqrt(2)*a);
  if(!(maximumPositiveSupportCenterDistance<3)) {
    throw new Error('Source-center cutoff redundancy is not established for these constants');
  }
  if(options.heldThrust!==undefined && typeof options.heldThrust!=='function') {
    throw new TypeError('heldThrust must be a function when supplied');
  }
  const heldThrust=options.heldThrust;
  const heldThrustLabel=heldThrust?(options.heldThrustLabel||'injected held-thrust evaluator'):
    'independent receiverSolution midpoint (default)';
  const coefficients=[[1,1,1,1],[a,a,-a,-a],[-a,a,a,-a]];
  function signedSum(intervals,cs) {
    let lower=0,upper=0;
    for(let k=0;k<4;k++) {
      const c=cs[k];lower+=c*(c>=0?intervals[k][0]:intervals[k][1]);
      upper+=c*(c>=0?intervals[k][1]:intervals[k][0]);
    }
    return [lower,upper];
  }
  function bound({states,delta,heldWinds}={}) {
    const counts={stateChecks:0,rotorGeometryChecks:0,windIntervals:0,
      independentReceiverCalls:0,heldLoadCalls:0,injectedHeldLoadCalls:0,
      sourcePairCount:1,fieldCalls:0};
    function reject(code,detail) {
      return {accepted:false,domainRejected:true,rejection:{code,detail},
        intervals:null,maxAbsError:null,counts,formallyCertified:false};
    }
    if(!Array.isArray(states)||states.length!==2) return reject('vehicle-count','Exactly receiver 0 and source 1 are required');
    if(!Number.isFinite(delta)||delta<0) return reject('invalid-delta','delta must be finite and nonnegative metres');
    if(!heldWinds || heldWinds.length!==4 || !Array.from(heldWinds).every(x=>Number.isFinite(x)&&x>=0)) {
      return reject('invalid-held-winds','Four finite nonnegative inflows are required');
    }
    for(let i=0;i<2;i++) {
      const s=states[i];counts.stateChecks++;
      if(!s || s.length!==17 || !Array.from(s).every(Number.isFinite)) return reject('invalid-state',{drone:i});
      if(s[6]!==0||s[7]!==0||s[8]!==0||s[9]!==1) return reject('orientation-contract',{drone:i,required:[0,0,0,1]});
      if(s[10]!==0||s[11]!==0||s[12]!==0) return reject('angular-velocity-contract',{drone:i,required:[0,0,0]});
      if(s[13]!==nominal||s[14]!==nominal||s[15]!==nominal||s[16]!==nominal) {
        return reject('nominal-thrust-contract',{drone:i,requiredPerRotor_N:nominal});
      }
    }
    const receiver=states[0],source=states[1],geometry=[];
    // Check all geometric domains before invoking any receiver solver.
    for(let k=0;k<4;k++) {
      const dx=source[0]-(receiver[0]+rotorOffsets[k][0]);
      const dy=source[1]-(receiver[1]+rotorOffsets[k][1]);
      const d0=source[2]-receiver[2],r0=Math.hypot(dx,dy);
      const dlo=d0-delta,dhi=d0+delta,rlo=Math.max(0,r0-delta),rhi=r0+delta;
      counts.rotorGeometryChecks++;
      if(![d0,r0,dlo,dhi,rlo,rhi].every(Number.isFinite)) return reject('nonfinite-geometry',{rotor:k});
      if(dlo<2.5*D) return reject('far-field-domain',{rotor:k,downstreamLower_m:dlo,requiredMinimum_m:2.5*D});
      geometry.push({rotor:k,anchorDownstream_m:d0,anchorRadial_m:r0,
        downstream_m:[dlo,dhi],radial_m:[rlo,rhi]});
    }
    const winds=[],thrusts=[],heldLoads=[];
    function solve(f,u) {counts.independentReceiverCalls++;return oracle.receiverSolution(f,u);}
    function validSolution(s) {
      return s && Number.isFinite(s.thrust) && s.thrust>=0 && s.bracket &&
        s.bracket.length===2 && s.bracket.every(Number.isFinite) &&
        s.bracket[0]>=0 && s.bracket[0]<=s.bracket[1] && s.bracket[1]<=1;
    }
    try {
      for(let k=0;k<4;k++) {
        const [dlo,dhi]=geometry[k].downstream_m,[rlo,rhi]=geometry[k].radial_m;
        const rawLower=C(dhi)*F(dhi)*Q(rhi/H(dlo));
        const rawUpper=C(dlo)*F(dlo)*Q(rlo/H(dhi));
        const lower=Math.max(0,rawLower-NUMERICAL_MARGIN.wind_mps);
        const upper=rawUpper+NUMERICAL_MARGIN.wind_mps;
        if(![lower,upper].every(Number.isFinite)||lower>upper) return reject('invalid-wind-interval',{rotor:k,lower,upper});
        winds.push([lower,upper]);counts.windIntervals++;
        // Receiving thrust decreases with inflow, so endpoint order reverses.
        const atUpper=solve(nominal,upper),atLower=solve(nominal,lower);
        if(!validSolution(atUpper)||!validSolution(atLower)) return reject('invalid-bisection-result',{rotor:k});
        const thrustLower=Math.max(0,nominal*atUpper.bracket[0]-NUMERICAL_MARGIN.thrust_N);
        const thrustUpper=nominal*atLower.bracket[1]+NUMERICAL_MARGIN.thrust_N;
        if(![thrustLower,thrustUpper].every(Number.isFinite)||thrustLower>thrustUpper) return reject('invalid-thrust-interval',{rotor:k});
        thrusts.push([thrustLower,thrustUpper]);counts.heldLoadCalls++;
        let actualHeld;
        if(heldThrust) {counts.injectedHeldLoadCalls++;actualHeld=heldThrust(nominal,heldWinds[k]);}
        else {const solution=solve(nominal,heldWinds[k]);if(!validSolution(solution)) return reject('invalid-held-bisection-result',{rotor:k});actualHeld=solution.thrust;}
        if(!Number.isFinite(actualHeld)||actualHeld<0) return reject('invalid-held-load',{rotor:k});
        heldLoads.push(actualHeld);
      }
    } catch(error) {
      return reject('receiver-evaluation-error',{name:error.name||'Error',message:String(error.message||error)});
    }
    const rotorDifferences=thrusts.map((q,k)=>[q[0]-heldLoads[k],q[1]-heldLoads[k]]);
    const loadDifferences=coefficients.map(cs=>signedSum(rotorDifferences,cs));
    const modeledLoads=coefficients.map(cs=>signedSum(thrusts,cs));
    const heldWrench=coefficients.map(cs=>cs.reduce((sum,c,k)=>sum+c*heldLoads[k],0));
    const maxAbsError=loadDifferences.map(([lo,hi])=>Math.max(Math.abs(lo),Math.abs(hi)));
    if(!loadDifferences.flat().concat(maxAbsError,heldWrench).every(Number.isFinite)) return reject('nonfinite-load-interval','Load aggregation failed');
    return {accepted:true,domainRejected:false,rejection:null,
      intervals:{winds_mps:winds,rotorThrusts_N:thrusts,
        rotorLoadDifferences_N:rotorDifferences,
        modeledLoads:modeledLoads,loadDifferences:loadDifferences},
      maxAbsError,heldRotorLoads_N:heldLoads,heldWrench,
      heldThrustEvaluator:heldThrustLabel,geometry,counts,
      errorOrder:CONTRACT.errorOrder,errorSign:CONTRACT.errorSign,
      numericalMargins:NUMERICAL_MARGIN,formallyCertified:false};
  }
  return Object.freeze({bound,contract:CONTRACT,numericalMargins:NUMERICAL_MARGIN,
    constants:Object.freeze({D,nominalPerRotor_N:nominal,induced_mps:induced,
      minimumDownstream_m:2.5*D,maximumPositiveSupportCenterDistance_m:maximumPositiveSupportCenterDistance}),
    heldThrustEvaluator:heldThrustLabel});
}

let defaultInstance;
function bound(args) {
  if(!defaultInstance) defaultInstance=createBound(require('./independent.cjs'));
  return defaultInstance.bound(args);
}
module.exports={createBound,bound,CONTRACT,NUMERICAL_MARGIN};
