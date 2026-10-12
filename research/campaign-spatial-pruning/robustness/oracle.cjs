'use strict';
// Scalar all-pairs oracle for the declared finite-support model. No spatial index.
const {C,F}=require('./fixtures.cjs');
const fade=(a,b,x)=>{const t=Math.max(0,Math.min(1,(x-a)/(b-a)));return 1-t*t*(3-2*t);};
const dot=(a,b)=>a[0]*b[0]+a[1]*b[1]+a[2]*b[2];
function validate(states){
  if(!Array.isArray(states))throw new TypeError('states must be an array');
  for(let i=0;i<states.length;i++){
    const s=states[i];if(!Array.isArray(s)||s.length!==17||!s.every(Number.isFinite))throw new TypeError(`invalid finite state ${i}`);
    if(Math.abs(Math.hypot(...s.slice(6,10))-1)>1e-10)throw new TypeError(`nonunit quaternion ${i}`);
    if(s.slice(13,17).some(x=>x<0))throw new TypeError(`negative nominal thrust ${i}`);
  }
}
function fields(states,mode='sum-rotor',support={}){
  validate(states);if(!['off','sum-force','sum-rotor','rss-rotor'].includes(mode))throw Error('Unknown mode');
  if(mode==='off')return {winds:states.map(()=>[0,0,0,0]),maximumInflow:0,contributions:0,candidates:0};
  const p={...C,...support}, axes=states.map(s=>F.rotate(s.slice(6,10),[0,0,1]));
  for(let i=0;i<axes.length;i++)if(axes[i][2]<Math.cos(p.maxTilt*Math.PI/180))throw Object.assign(Error('tilt domain'),{detail:{drone:i}});
  const vi=Math.sqrt(C.weight/(8*p.rho*Math.PI*p.rotorRadius**2));let contributions=0,maximumInflow=0;
  const winds=states.map((s,i)=>F.rotors.map(r=>{
    const ro=F.rotate(s.slice(6,10),[r[0],r[1],0]);const receiver=[s[0]+ro[0],s[1]+ro[1],s[2]+ro[2]];let total=0;
    for(let j=0;j<states.length;j++){
      if(i===j)continue;const d=states[j].slice(0,3).map((x,k)=>x-receiver[k]),down=dot(d,axes[j]);
      if(down<=0||down>=p.axialCutoff)continue;
      const radial=Math.hypot(...d.map((x,k)=>x-down*axes[j][k]));
      if(down<p.minDownstream*p.motorDistance){
        if(radial<p.nearFieldRadius)throw Object.assign(Error('near-field domain'),{detail:{receiver:i,source:j,downstream:down,radial}});
        continue;
      }
      const h=p.spread*(down-p.origin*p.motorDistance);if(radial>=p.radialCutoff*h)continue;
      const nd=down/p.motorDistance,xi=radial/h;
      const speed=p.decay/(nd-p.origin)/(1+(Math.sqrt(2)-1)*xi*xi)**2*vi*
        fade(p.axialFade,p.axialCutoff,down)*fade(p.radialFade,p.radialCutoff,xi)*Math.max(0,dot(axes[i],axes[j]));
      total+=mode==='rss-rotor'?speed*speed:speed;contributions++;
    }
    const u=mode==='rss-rotor'?Math.sqrt(total):total;maximumInflow=Math.max(maximumInflow,u);return u;
  }));
  return {winds,maximumInflow,contributions,candidates:states.length*(states.length-1)};
}
module.exports={validate,fields};
