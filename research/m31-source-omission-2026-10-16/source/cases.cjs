'use strict';
// Inputs generated only by the frozen scientific launch; no data-dependent selection.
const f0=.027*9.81/4,a=.028,D=2*Math.SQRT2*a,near=2.5*D;
function state(p,q=[0,0,0,1]){return [...p,0,0,0,...q,0,0,0,f0,f0,f0,f0];}
function quaternion(roll,pitch,yaw){const cr=Math.cos(roll/2),sr=Math.sin(roll/2),cp=Math.cos(pitch/2),sp=Math.sin(pitch/2),cy=Math.cos(yaw/2),sy=Math.sin(yaw/2);return [sr*cp*cy-cr*sp*sy,cr*sp*cy+sr*cp*sy,cr*cp*sy-sr*sp*cy,cr*cp*cy+sr*sp*sy];}
function lattice(shape,seed){let x=seed>>>0;const rand=()=>{x^=x<<13;x^=x>>>17;x^=x<<5;return (x>>>0)/4294967296;},out=[];
 for(let z=0;z<shape[2];z++)for(let y=0;y<shape[1];y++)for(let k=0;k<shape[0];k++){
 const p=[.30*k+.04*(rand()-.5),.30*y+.04*(rand()-.5),.50*z+.04*(rand()-.5)];
 const q=quaternion((rand()*16-8)*Math.PI/180,(rand()*16-8)*Math.PI/180,(rand()*2-1)*Math.PI);out.push(state(p,q));}
 return out;
}
function fixtures(){const items=[];const pair=(id,p,expected='valid',q=[0,0,0,1])=>items.push({id,expected,states:[state([0,0,0]),state(p,q)]});
 for(const e of [-1e-12,0,1e-12])pair('center3-'+String(e),[3+e,0,0]);
 for(const e of [-1e-12,0,1e-12])pair('down0-'+String(e),[.2,0,e]);
 for(const e of [-1e-12,0,1e-12])pair('farStart-'+String(e),[0,0,near+e],e<0?'reject':'valid');
 for(const e of [-1e-12,0,1e-12])pair('downEnd-'+String(e),[0,0,2.5+e]);
 for(const e of [-1e-12,0,1e-12])pair('nearRadius-'+String(e),[a+.15+e,a,.1],e===0?'agreement':e<0?'reject':'valid');
 for(const ratio of [2,3]){const down=1,half=.07668*(down+5.817*D);pair('radial-'+ratio,[a+ratio*half,a,down]);}
 pair('downFade2',[0,0,2]);
 pair('centerInferenceInvalid',[.17,0,.1],'reject');
 pair('combinedTiltYaw',[.28,.19,.65],'valid',quaternion(7*Math.PI/180,-8*Math.PI/180,1.2));
 const q=quaternion(.1,-.1,.7).map(v=>v*(1+1e-12));pair('normDefect',[.3,.2,.7],'valid',q);
 pair('tiltRejected',[0,0,1],'reject',quaternion(21*Math.PI/180,0,0));
 // Deterministic multiple-source stress; total acceptance pattern is an observed outcome.
 items.push({id:'multipleWeak',expected:'valid',states:[state([0,0,0]),state([.31,.12,1]),state([-.31,.12,1]),state([.31,-.12,1]),state([-.31,-.12,1])]});
 items.push({id:'signedMoment',expected:'valid',states:[state([0,0,0]),state([.2,0,.7]),state([-.25,.3,1.4])]});
 return items;
}
module.exports={state,lattice,fixtures,quaternion};
