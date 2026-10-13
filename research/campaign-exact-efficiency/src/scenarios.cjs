'use strict';
const F=require('./source.cjs').source('outputs/step02c-source/physics.cjs');
const nominal=F.P.m*F.P.g/4;
function rng(seed){let x=seed>>>0;return()=>((x=(1664525*x+1013904223)>>>0)/4294967296);}
function pose(x,y,z,tilt=0,azimuth=0,thrustScale=1){return [x,y,z,0,0,0,Math.sin(tilt/2)*Math.cos(azimuth),Math.sin(tilt/2)*Math.sin(azimuth),0,Math.cos(tilt/2),0,0,0,...Array(4).fill(nominal*thrustScale)];}
function cloud({count=16,seed=3301,family='sparse',t=0}){
  const random=rng(seed),side=Math.ceil(Math.cbrt(count)),spacing=family==='dense'?.4:.75;
  const out=[];
  for(let i=0;i<count;i++){
    const x=i%side,y=Math.floor(i/side)%side,z=Math.floor(i/(side*side));
    const phase=random()*2*Math.PI;
    const p=[(x-(side-1)/2)*spacing,(y-(side-1)/2)*spacing,3+z*spacing].map((v,k)=>v+(random()-.5)*.03+.025*Math.sin(2*Math.PI*t+phase+k));
    const tilt=family==='tilted'?(10+5*Math.sin(phase+t))*Math.PI/180:0;
    const s=pose(...p,tilt,phase,1+.1*Math.sin(phase+t));
    for(let k=0;k<3;k++)s[3+k]=.05*Math.PI*Math.cos(2*Math.PI*t+phase+k);
    out.push(s);
  }
  return out;
}
function fixtures(){return [
 {name:'centered',states:[pose(0,0,1),pose(0,0,2)]},
 {name:'offset',states:[pose(0,0,1),pose(.28,.07,2)]},
 {name:'weak-tail',states:[pose(0,0,1),pose(.57,.0,3.48)]},
 {name:'outside-support',states:[pose(0,0,1),pose(0,0,3.5)]},
 {name:'sparse-16',states:cloud({})},
 {name:'dense-16',states:cloud({family:'dense'})},
 {name:'tilted-16',states:cloud({family:'tilted'})}
];}
module.exports={rng,pose,cloud,fixtures,nominal};
