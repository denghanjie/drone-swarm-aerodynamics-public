'use strict';
// Local, bounded approximation of the pinned finite-support mean-wake model.
// This module does not assert physical validity. All receiver rotors are retained.
const {source}=require('./source.cjs');
const A = source('outputs/milestone-28-source/aero.cjs');
const F = source('outputs/step02c-source/physics.cjs');
const W = source('outputs/step03a-source/wake.cjs');
const {Grid} = source('outputs/milestone-26-source/grid.cjs');
const P = A.P;
const rotorOffset = Math.SQRT2 * F.P.a;
const area = Math.PI * P.rotorRadius ** 2;
const induced = Math.sqrt(F.P.m * F.P.g / (8 * P.rho * area));
const farStart = W.parameters.minDownstream * P.motorDistance;
const margin = 1e-12;
const profileConstant = Math.SQRT2 - 1;
const tiltCosine = Math.cos(P.maxTiltDegrees * Math.PI / 180);
function fade(a,b,x) { const t=Math.max(0,Math.min(1,(x-a)/(b-a))); return 1-t*t*(3-2*t); }
class InputError extends Error {}

function prepare(states) {
  if (!Array.isArray(states) || states.length === 0) throw new InputError('Nonempty state array required');
  const axes=[],points=[];
  for (let i=0;i<states.length;i++) {
    const s=states[i];
    if (!Array.isArray(s) || s.length!==17 || !s.every(Number.isFinite)) throw new InputError('Every state must have 17 finite entries');
    const q=s.slice(6,10);
    if (Math.abs(Math.hypot(...q)-1)>1e-10) throw new InputError('Unit quaternion required');
    const axis=F.rotate(q,[0,0,1]);
    if(axis[2]<tiltCosine) throw new A.DomainError('Source/receiver tilt exceeds exploratory20-degree limit',{drone:i,axis});
    axes.push(axis);
    points.push(F.rotors.map(r=>{const d=F.rotate(q,[r[0],r[1],0]);return [s[0]+d[0],s[1]+d[1],s[2]+d[2]];}));
  }
  return {axes,points};
}

function geometry(p,source,axis) {
  const x=source[0]-p[0], y=source[1]-p[1], z=source[2]-p[2];
  const down=x*axis[0]+y*axis[1]+z*axis[2];
  const radial=Math.hypot(x-down*axis[0],y-down*axis[1],z-down*axis[2]);
  return {down,radial};
}

function assertNearDomain(receiver,source,i,j,axis,points,counters) {
  // Any near-wake rotor point must lie within this Euclidean center envelope.
  const radius=Math.hypot(farStart,P.nearFieldRadius)+rotorOffset*(1+1e-9)+1e-9;
  if (Math.hypot(source[0]-receiver[0],source[1]-receiver[1],source[2]-receiver[2])>radius) return;
  for (const p of points) {
    counters.guardRotorChecks++;
    const {down,radial}=geometry(p,source,axis);
    if (down>0 && down<farStart && radial<P.nearFieldRadius) throw new A.DomainError('Receiver enters unmodeled near wake',{receiver:i,source:j,downstream:down,radial});
  }
}

function pairUpperBound(receiver,source,axis) {
  const {down,radial}=geometry(receiver,source,axis);
  const R=rotorOffset*(1+1e-9)+margin;
  const low=down-R,high=down+R,rmin=Math.max(0,radial-R);
  if(high<farStart || low>=P.downstreamCutoff) return 0;
  const dmin=Math.max(farStart,low),dmax=Math.min(P.downstreamCutoff,high);
  const halfmax=W.parameters.spread*(dmax-W.parameters.origin*P.motorDistance);
  if(rmin>=P.radialCutoff*halfmax) return 0;
  // The peak and maximum width may occur at different downstream locations;
  // multiplying these separate upper bounds deliberately overestimates the pair.
  const centermax=W.parameters.decay/(dmin/P.motorDistance-W.parameters.origin);
  const denominator=1+profileConstant*(rmin/halfmax)**2;
  // Both fades are nonincreasing in their arguments. Every valid rotor point
  // has down >= dmin and radial/halfWidth >= rmin/halfmax, so these are upper
  // bounds on each fade. Keeping them matters: without fades the smallest
  // positive envelope exceeds every preregistered epsilon (preserved v0).
  return centermax*induced/(denominator*denominator)*fade(P.downstreamFade,P.downstreamCutoff,dmin)*fade(P.radialFade,P.radialCutoff,rmin/halfmax)*(1+1e-9);
}

function exactWake(p,source,axis,cosine,counters) {
  const {down,radial}=geometry(p,source,axis);
  if(down<=0 || down>=P.downstreamCutoff || down<farStart) return 0;
  const normalizedDown=down/P.motorDistance;
  const distance=normalizedDown-W.parameters.origin;
  const half=W.parameters.spread*distance*P.motorDistance;
  if(radial>=P.radialCutoff*half) return 0;
  const xi=(radial/P.motorDistance)/(W.parameters.spread*distance);
  const denominator=1+profileConstant*xi*xi;
  counters.evaluatedRotorKernels++;
  const wake=(W.parameters.decay/distance)/(denominator*denominator)*induced*fade(P.downstreamFade,P.downstreamCutoff,down)*fade(P.radialFade,P.radialCutoff,radial/half)*cosine;
  counters.contributions++;
  return wake;
}

function fields(states,{epsilon=0,search='grid'}={}) {
  if(!Number.isFinite(epsilon) || epsilon<0) throw new InputError('Finite nonnegative epsilon required');
  if(!['grid','brute','all'].includes(search)) throw new InputError('Unknown search');
  const {axes,points}=prepare(states);
  const grid=search==='grid'?new Grid(states,1.5):null;
  const winds=states.map(()=>[0,0,0,0]),omittedBounds=states.map(()=>0);
  const counters={candidates:0,guardRotorChecks:0,boundEvaluations:0,exactZeroPairs:0,omittedPairs:0,retainedPairs:0,evaluatedRotorKernels:0,contributions:0};
  let maximumInflow=0;
  for(let i=0;i<states.length;i++) {
    const receiver=states[i];
    const ids=grid?grid.neighbors(i,P.neighborRadius):states.map((_,j)=>j).filter(j=>j!==i&&(search==='all'||Math.hypot(receiver[0]-states[j][0],receiver[1]-states[j][1],receiver[2]-states[j][2])<P.neighborRadius));
    counters.candidates+=ids.length;
    for(const j of ids) {
      const source=states[j],axis=axes[j];
      // The independent guard runs before every possible approximation skip.
      assertNearDomain(receiver,source,i,j,axis,points[i],counters);
      // Both zero and positive budgets pay for the identical bound. Exact-zero
      // support culling belongs to the same-equation control, not pruning gains.
      counters.boundEvaluations++;
      const bound=pairUpperBound(receiver,source,axis);
      if(bound===0) { counters.exactZeroPairs++; continue; }
      if(epsilon>0 && omittedBounds[i]+bound<=epsilon) {
        omittedBounds[i]+=bound;
        counters.omittedPairs++;
        continue;
      }
      counters.retainedPairs++;
      const cosine=Math.max(0,axes[i][0]*axis[0]+axes[i][1]*axis[1]+axes[i][2]*axis[2]);
      for(let r=0;r<4;r++) winds[i][r]+=exactWake(points[i][r],source,axis,cosine,counters);
    }
    maximumInflow=Math.max(maximumInflow,...winds[i]);
  }
  return {winds,omittedBounds,maximumInflow,...counters,counters};
}

function loads(state,winds) {
  const nominal=state.slice(13,17);
  if(nominal.length!==4 || nominal.some(x=>!Number.isFinite(x)||x<0)) throw new InputError('Four finite nonnegative nominal rotor thrusts required');
  const rotorThrusts=nominal.map((f,r)=>A.effectiveThrust(f,winds[r]));
  const effective=F.wrench(rotorThrusts),original=F.wrench(nominal);
  return {rotorThrusts,force:F.rotate(state.slice(6,10),[0,0,effective.T]),moment:[effective.t[0],effective.t[1],original.t[2]]};
}

function loadBounds(state,keptWinds,omittedBound) {
  const nominal=state.slice(13,17);
  if(nominal.length!==4 || nominal.some(x=>!Number.isFinite(x)||x<0)) throw new InputError('Four finite nonnegative nominal rotor thrusts required');
  if(!Number.isFinite(omittedBound)||omittedBound<0) throw new InputError('Finite nonnegative omitted bound required');
  const rotor=nominal.map((f,r)=>A.effectiveThrust(f,keptWinds[r])-A.effectiveThrust(f,keptWinds[r]+omittedBound));
  const force=rotor.reduce((s,x)=>s+x,0);
  const component=[0,1].map(k=>rotor.reduce((s,x,r)=>s+Math.abs(F.rotors[r][1-k])*x,0));
  const lipschitzForce=nominal.reduce((s,f)=>s+Math.sqrt(2*P.rho*area*f)/3*omittedBound,0);
  return {rotor,force,momentComponents:component,moment:Math.hypot(...component),lipschitzForce};
}

module.exports={fields,loads,loadBounds,pairUpperBound,prepare,geometry,P,rotorOffset,farStart,InputError,DomainError:A.DomainError,integrate:A.integrate,F,A,W};
