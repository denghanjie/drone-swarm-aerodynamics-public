'use strict';
function nextUp(x){if(x===0)return Number.MIN_VALUE;const b=Buffer.alloc(8);b.writeDoubleLE(x);let u=b.readBigUInt64LE();u+=x>0?1n:-1n;b.writeBigUInt64LE(u);return b.readDoubleLE();}
const nextDown=x=>-nextUp(-x);
function controls(){
 const out=[],add=(id,positions,grid)=>out.push({id,positions,expectedGrid:grid});
 for(const x of [0,-6])for(const [name,fn] of [['below',nextDown],['exact',x=>x],['above',nextUp]])add(`radius-${x}-${name}`,[[x,0,0],[fn(x+3),0,0]],true);
 for(const [axis,name,fn] of [[0,'below',nextDown],[1,'exact',x=>x],[2,'above',nextUp]]){const rotate=v=>v.map((_,k)=>v[(k-axis+3)%3]);add(`cell-${name}`,[[0,0,0],rotate([fn(4),.25,.5]),rotate([4,0,1])],true);}
 add('signed-zero',[[-0,0,0],[0,-0,0]],true);
 const coarse=[[0,0,0],[1,.25,.5],[4,1,2]];add('coarse-origin',coarse,true);add('coarse-translated',coarse.map(a=>a.map(x=>x+2**40)),true);
 add('dense-16',Array.from({length:16},(_,i)=>[i*.05,0,.45*(i%3)]),true);
 add('span-256',[[0,0,0],[256,0,0]],true);add('span-nextUp256',[[0,0,0],[nextUp(256),0,0]],false);
 add('far-invalid258',[[0,0,0],[258,0,0]],false);add('nonfinite-nan',[[0,0,0],[NaN,0,0]],false);add('nonfinite-infinity',[[0,0,0],[Infinity,0,0]],false);add('overflow-span',[[-Number.MAX_VALUE,0,0],[Number.MAX_VALUE,0,0]],false);
 add('near-field',[[0,0,0],[0,0,.02]],true);add('duplicates',[[1,1,1],[1,1,1]],true);
 for(const n of [62,64,66])add(`planes-${n}`,Array.from({length:n},(_,i)=>[0,0,i<n/2?0:.6]),true);
 return out;
}
module.exports={controls,ownershipSequence:['L:sparse2','T:sparse2','L:planes62','T:planes62']};
