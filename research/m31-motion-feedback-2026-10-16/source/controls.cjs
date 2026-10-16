'use strict';
const A=require('./adapter.cjs');
function controls(){const h=A.nominalHover,s=[0,0,4.5,0,0,0,0,0,0,1,0,0,0,h,h,h,h],records=[],corners=[[.028,.028],[-.028,.028],[-.028,-.028],[.028,-.028]];
 for(let r=0;r<4;r++){const f=Array(4).fill(h);f[r]+=.01;const actual=A.correction(s,f),expected={force:[0,0,.01],torque:[corners[r][1]*.01,-corners[r][0]*.01,0]},err=Math.max(...actual.force.map((x,k)=>Math.abs(x-expected.force[k])),...actual.torque.map((x,k)=>Math.abs(x-expected.torque[k])));records.push({id:'rotor-'+r,actual,expected,maxError:err,pass:err<1e-14});}
 const zero=A.correction(s,Array(4).fill(h));records.push({id:'zero-correction',actual:zero,pass:[...zero.force,...zero.torque].every(x=>x===0)});
 const angles=[A.angle([0,0,0,1],[0,0,0,-1]),A.angle([0,0,0,1],[Math.SQRT1_2,0,0,Math.SQRT1_2])];records.push({id:'quaternion-angle',actual:angles,expected:[0,Math.PI/2],pass:angles[0]===0&&Math.abs(angles[1]-Math.PI/2)<1e-14});return {pass:records.every(x=>x.pass),records};}
module.exports={controls};
