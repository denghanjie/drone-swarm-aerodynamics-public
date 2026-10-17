'use strict';
// Fixed prospective definitions. No source import, fixture evaluation or tuning here.
function nextUp(x){if(x===0)return Number.MIN_VALUE;const b=Buffer.alloc(8);b.writeDoubleLE(x);let u=b.readBigUInt64LE();u+=x>0?1n:-1n;b.writeBigUInt64LE(u);return b.readDoubleLE();}
const nextDown=x=>-nextUp(-x);

const controlIds=Object.freeze([
 'radius-0-below','radius-0-exact','radius-0-above',
 'radius--6-below','radius--6-exact','radius--6-above',
 'cell-below','cell-exact','cell-above','signed-zero','coarse-origin','coarse-translated',
 'dense-16','span-256','span-nextUp256','far-invalid258','nonfinite-nan','nonfinite-infinity',
 'overflow-span','near-field','duplicates','planes-62','planes-64','planes-66',
 'component-x-below','component-x-exact','component-x-above',
 'component-y-below','component-y-exact','component-y-above',
 'component-z-below','component-z-exact','component-z-above',
 'span-diagonal-256','span-nextDown256','center-257-fallback','center-nextUp257-fallback',
 'mixed-near-far','mixed-positive-far','invalid-quaternion-far',
 'nominal-zero-positive-far','nominal-negative-positive-far','nominal-nan-positive-far',
 'scaled-cap-positive-far','invalid-quaternion-nan-far','nominal-infinity-positive-far',
 'nominal-total-overflow-positive-far','nominal-unequal-positive-far'
]);

function controls(){
 // The original 24 positional definitions are retained without arithmetic changes.
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
 const originalFallback={
  'span-nextUp256':'span-out-of-range','far-invalid258':'span-out-of-range',
  'nonfinite-nan':'coordinate-nonfinite','nonfinite-infinity':'coordinate-nonfinite',
  'overflow-span':'span-nonfinite'
 };
 for(const item of out){item.expectedScreenEligible=item.expectedGrid;item.expectedFallbackReason=originalFallback[item.id]||null;}

 const addScreen=(id,positions,eligible=true,statePatches=[],fallbackReason=null)=>out.push({
  id,positions,expectedScreenEligible:eligible,expectedFallbackReason:fallbackReason,statePatches
 });
 for(const [axis,axisName] of [[0,'x'],[1,'y'],[2,'z']]){
  for(const [name,fn] of [['below',nextDown],['exact',x=>x],['above',nextUp]]){
   const position=[0,0,0];position[axis]=fn(4);
   addScreen(`component-${axisName}-${name}`,[[0,0,0],position]);
  }
 }
 addScreen('span-diagonal-256',[[0,0,0],[256,256,256]]);
 addScreen('span-nextDown256',[[0,0,0],[nextDown(256),0,0]]);
 addScreen('center-257-fallback',[[0,0,0],[257,0,0]],false,[],'span-out-of-range');
 addScreen('center-nextUp257-fallback',[[0,0,0],[nextUp(257),0,0]],false,[],'span-out-of-range');
 addScreen('mixed-near-far',[[0,0,0],[0,0,.02],[4,0,0]]);
 addScreen('mixed-positive-far',[[0,0,0],[0,0,.6],[4,0,0]]);
 addScreen('invalid-quaternion-far',[[0,0,0],[4,0,0]],true,[{vehicle:0,index:9,value:2}]);
 addScreen('nominal-zero-positive-far',[[0,0,0],[0,0,.6],[4,0,0]],true,[{vehicle:1,index:13,value:0}]);
 addScreen('nominal-negative-positive-far',[[0,0,0],[0,0,.6],[4,0,0]],true,[{vehicle:1,index:13,value:-.01}]);
 addScreen('nominal-nan-positive-far',[[0,0,0],[0,0,.6],[4,0,0]],true,[{vehicle:1,index:13,value:NaN}]);
 addScreen('scaled-cap-positive-far',[[0,0,0],[0,0,.6],[4,0,0]],true,[13,14,15,16].map(index=>({vehicle:1,index,value:1e12})));
 addScreen('invalid-quaternion-nan-far',[[0,0,0],[4,0,0]],true,[{vehicle:0,index:6,value:NaN}]);
 addScreen('nominal-infinity-positive-far',[[0,0,0],[0,0,.6],[4,0,0]],true,[{vehicle:1,index:13,value:Infinity}]);
 addScreen('nominal-total-overflow-positive-far',[[0,0,0],[0,0,.6],[4,0,0]],true,[13,14,15,16].map(index=>({vehicle:1,index,value:Number.MAX_VALUE})));
 addScreen('nominal-unequal-positive-far',[[0,0,0],[0,0,.6],[4,0,0]],true,[.03,.04,.05,.06].map((value,r)=>({vehicle:1,index:13+r,value})));
 return out;
}

// Six separately paid cross-call builds, while retaining planes-66 L/F outputs.
// sparse2=[[0,0,0],[4,0,0]], planes62 is the original planes-62 literal,
// fallback258=[[0,0,0],[258,0,0]]. Each call receives fresh state arrays.
const ownershipSequence=Object.freeze(['L:sparse2','F:sparse2','L:planes62','F:planes62','L:fallback258','F:fallback258']);
module.exports={controls,controlIds,ownershipSequence};
