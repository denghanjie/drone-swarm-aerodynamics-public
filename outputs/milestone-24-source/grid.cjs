'use strict';
class Grid{
 constructor(states,cell=1.8){if(!(cell>0))throw Error('Positive cell size required');this.states=states;this.cell=cell;this.cells=new Map();for(let i=0;i<states.length;i++){const p=states[i],key=this.key(...p.slice(0,3).map(x=>Math.floor(x/cell)));if(!this.cells.has(key))this.cells.set(key,[]);this.cells.get(key).push(i);}}
 key(x,y,z){return x+','+y+','+z;}
 candidates(p,r){const c=this.cell,lo=p.slice(0,3).map(x=>Math.floor((x-r)/c)),hi=p.slice(0,3).map(x=>Math.floor((x+r)/c)),out=[];for(let x=lo[0];x<=hi[0];x++)for(let y=lo[1];y<=hi[1];y++)for(let z=lo[2];z<=hi[2];z++){const ids=this.cells.get(this.key(x,y,z));if(ids)out.push(...ids);}return out.sort((a,b)=>a-b);}
 neighbors(i,r){const p=this.states[i];return this.candidates(p,r).filter(j=>j!==i&&Math.hypot(...p.slice(0,3).map((x,k)=>x-this.states[j][k]))<r);}
}
module.exports={Grid};
