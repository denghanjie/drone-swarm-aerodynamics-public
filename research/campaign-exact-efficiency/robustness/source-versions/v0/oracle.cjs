'use strict';
// Independently coded scalar all-pairs oracle. No candidate kernels or spatial index.
const {C,F}=require('./fixtures.cjs');
const dot=(a,b)=>a.reduce((v,x,k)=>v+x*b[k],0);
const fade=(a,b,x)=>{const u=Math.max(0,Math.min(1,(x-a)/(b-a)));return 1-u*u*(3-2*u);};
function fields(states){const axes=states.map(s=>F.rotate(s.slice(6,10),[0,0,1]));for(let i=0;i<axes.length;i++)if(axes[i][2]<Math.cos(C.maxTilt*Math.PI/180))throw Object.assign(Error('tilt domain'),{detail:{drone:i}});
const vi=Math.sqrt(C.weight/(8*C.rho*Math.PI*C.rotorRadius**2));let positiveInteractions=0,contributions=0;
const winds=states.map((s,i)=>F.rotors.map(rotor=>{const delta=F.rotate(s.slice(6,10),[rotor[0],rotor[1],0]),p=delta.map((x,k)=>x+s[k]);let total=0;for(let j=0;j<states.length;j++){if(i===j)continue;const d=states[j].slice(0,3).map((x,k)=>x-p[k]),down=dot(d,axes[j]);if(down<=0||down>=C.axialCutoff)continue;const radial=Math.hypot(...d.map((x,k)=>x-down*axes[j][k]));if(down<C.minDownstream*C.motorDistance){if(radial<C.nearFieldRadius)throw Object.assign(Error('near-field domain'),{detail:{receiver:i,source:j,downstream:down,radial}});continue;}
const nd=down/C.motorDistance,distance=nd-C.origin,half=C.spread*distance*C.motorDistance;if(radial>=C.radialCutoff*half)continue;const xi=(radial/C.motorDistance)/(C.spread*distance),profile=C.decay/distance/(1+(Math.sqrt(2)-1)*xi*xi)**2;const u=profile*vi*fade(C.axialFade,C.axialCutoff,down)*fade(C.radialFade,C.radialCutoff,radial/half)*Math.max(0,dot(axes[i],axes[j]));total+=u;contributions++;if(u>0)positiveInteractions++;}return total;}));
return {winds,maximumInflow:Math.max(0,...winds.flat()),contributions,positiveInteractions};}
module.exports={fields};
