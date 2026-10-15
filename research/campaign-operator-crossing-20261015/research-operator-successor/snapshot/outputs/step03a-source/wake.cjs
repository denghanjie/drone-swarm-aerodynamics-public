/* Original implementation of the normalized mean far-field model in
 * Bauersfeld et al., arXiv:2403.13321v3, Eqs. 3–9 and Section VI-C.
 * No force law, rotor response, near-field continuation, or swarm superposition.
 */
'use strict';
const parameters=Object.freeze({decay:10.11,spread:.07668,origin:-5.817,minDownstream:2.5});
function positive(x,name){if(!Number.isFinite(x)||x<=0)throw new Error(name+' must be finite and positive');}
function normalizedWake(s,r){
 if(!Number.isFinite(s)||!Number.isFinite(r)||r<0)throw new Error('Finite coordinates and nonnegative radial distance required');
 if(s<parameters.minDownstream)return {status:'outside-far-field-domain',speed:null,centerline:null,halfWidth:null,xi:null};
 const distance=s-parameters.origin,halfWidth=parameters.spread*distance,centerline=parameters.decay/distance,xi=r/halfWidth;
 return {status:'formula-evaluated-not-independently-validated',speed:centerline/(1+(Math.sqrt(2)-1)*xi*xi)**2,centerline,halfWidth,xi};
}
// motorDistance must use the paper's geometry convention, not an arbitrary arm length.
// Calling this explicitly assumes a hovering source, uncanted rotors and free air.
function hoverWake({downstream,radial,mass,propRadius,motorDistance,rho=1.225,g=9.81}){
 for(const [key,value] of Object.entries({mass,propRadius,motorDistance,rho,g}))positive(value,key);
 const induced=Math.sqrt(mass*g/(2*rho*Math.PI*propRadius**2*4));
 const result=normalizedWake(downstream/motorDistance,radial/motorDistance);
 return {...result,speedMS:result.speed===null?null:result.speed*induced,halfWidthM:result.halfWidth===null?null:result.halfWidth*motorDistance,inducedMS:induced};
}
// Ideal induced aerodynamic power ratio for maintained hover thrust, Eq. 11.
// NOT electrical power, thrust loss, or motor-command conversion.
function idealPowerRatio(alpha){if(!Number.isFinite(alpha)||alpha<0)throw new Error('Nonnegative finite downwash / receiver induced velocity required');return (alpha+Math.hypot(alpha,2))/2;}
module.exports={parameters,normalizedWake,hoverWake,idealPowerRatio};
