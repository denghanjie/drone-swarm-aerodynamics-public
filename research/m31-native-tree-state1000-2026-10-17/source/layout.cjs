'use strict';
// Saved evidence representation only. No scientific dependency or numerical query.
const TREE='m31-native-center-tree-compact-v1',SCHEMA='m31-tree-witness-columns-v1';
const TREE_KEYS=['schema','mode','leafCapacity','eligible','fallback','fallbackReason','complete','n','canonicalIds','nodes','leafDictionary','receivers','counters'];
const LAYOUT_KEYS=['schema','base','receiverIds','cullOffsets','cullCodes','cullDifferences','leavesRefs','gathered'];
const WORD=/^[0-9a-f]{16}$/;
const need=(x,c)=>{if(!x)throw Error('layout-'+c);};
const integer=(x,lo=0,hi=0xffffffff)=>Number.isSafeInteger(x)&&!Object.is(x,-0)&&x>=lo&&x<=hi;
function keys(x,expected){need(x&&typeof x==='object'&&!Array.isArray(x)&&Object.keys(x).length===expected.length&&expected.every(k=>Object.hasOwn(x,k)),'keys');}
function equal(a,b){
 if(Object.is(a,b))return true;
 if(a===null||b===null||typeof a!==typeof b||typeof a!=='object'||Array.isArray(a)!==Array.isArray(b))return false;
 if(Array.isArray(a))return a.length===b.length&&a.every((v,i)=>equal(v,b[i]));
 const ak=Object.keys(a),bk=Object.keys(b);return ak.length===bk.length&&ak.every(k=>Object.hasOwn(b,k)&&equal(a[k],b[k]));
}
function validateActual(actual,n,guard){
 need(Array.isArray(actual)&&actual.length<=n,'actual-shape');let prev=-1;const runs=[];
 for(let i=0;i<actual.length;i++){
  if((i&65535)===0)guard();const v=actual[i];need(integer(v,0,n-1)&&v>prev,'actual-order');
  if(v===prev+1&&i>0)runs[runs.length-1]++;else runs.push(v,1);prev=v;
 }
 return runs;
}
function oldGather(actual,n,guard=()=>{}){const runs=validateActual(actual,n,guard);return runs.length<actual.length?{kind:'runs',data:runs}:{kind:'literal',data:actual.slice()};}
function expandOld(value,n,guard=()=>{}){
 if(value===null)return null;keys(value,['kind','data']);need(Array.isArray(value.data),'old-data');let actual;
 if(value.kind==='literal')actual=value.data.slice();
 else{
  need(value.kind==='runs'&&value.data.length%2===0&&value.data.length<=2*n,'old-runs-shape');actual=[];let end=-1;
  for(let i=0;i<value.data.length;i+=2){
   guard();const s=value.data[i],length=value.data[i+1];need(integer(s,0,n-1)&&integer(length,1,n)&&s> end&&s+length<=n,'old-run');
   for(let j=0;j<length;j++)actual.push(s+j);end=s+length-1;
  }
 }
 validateActual(actual,n,guard);need(equal(value,oldGather(actual,n,guard)),'old-noncanonical');return actual;
}
function selected(actual,n,guard=()=>{}){
 const runs=validateActual(actual,n,guard),costs=[59+4*actual.length,56+4*runs.length,58+8*Math.ceil(n/64)];
 let choice=0;for(let i=1;i<3;i++)if(costs[i]<costs[choice])choice=i;
 if(choice===0)return {kind:'literal',count:actual.length,data:actual.slice()};
 if(choice===1)return {kind:'runs',count:actual.length,data:runs};
 const bytes=new Uint8Array(8*Math.ceil(n/64));
 for(let i=0;i<actual.length;i++){
  if((i&65535)===0)guard();const j=actual[i],word=Math.floor(j/64),bit=j%64;
  bytes[word*8+7-Math.floor(bit/8)]|=1<<(bit%8);
 }
 const data=[];for(let i=0;i<bytes.length;i+=8){let w='';for(let k=0;k<8;k++)w+=bytes[i+k].toString(16).padStart(2,'0');data.push(w);}
 return {kind:'bitmap',count:actual.length,data};
}
function expandNew(value,n,guard=()=>{}){
 if(value===null)return null;keys(value,['kind','count','data']);need(integer(value.count,0,n)&&Array.isArray(value.data),'new-shape');let actual=[];
 if(value.kind==='literal')actual=value.data.slice();
 else if(value.kind==='runs'){
  need(value.data.length%2===0&&value.data.length<=2*n,'new-runs-shape');let end=-1;
  for(let i=0;i<value.data.length;i+=2){guard();const s=value.data[i],length=value.data[i+1];need(integer(s,0,n-1)&&integer(length,1,n)&&s>end&&s+length<=n,'new-run');for(let j=0;j<length;j++)actual.push(s+j);end=s+length-1;}
 }else{
  need(value.kind==='bitmap'&&value.data.length===Math.ceil(n/64)&&value.data.every(w=>typeof w==='string'&&WORD.test(w)),'bitmap-shape');
  for(let wi=0;wi<value.data.length;wi++){
   guard();const word=value.data[wi];
   for(let byte=0;byte<8;byte++){
    const bits=parseInt(word.slice(14-byte*2,16-byte*2),16);
    for(let bit=0;bit<8;bit++)if(bits&(1<<bit)){const j=wi*64+byte*8+bit;need(j<n,'bitmap-tail');actual.push(j);}
   }
  }
 }
 validateActual(actual,n,guard);need(actual.length===value.count,'new-count');need(equal(value,selected(actual,n,guard)),'new-noncanonical');return actual;
}
function baseCheck(base){
 keys(base,TREE_KEYS.filter(k=>k!=='receivers'));need(base.schema===TREE&&integer(base.n,0,5000)&&Array.isArray(base.nodes)&&base.nodes.length<=10000&&Array.isArray(base.leafDictionary),'base-shape');
}
function encode(tree,guard=()=>{}){
 if(tree===null)return null;keys(tree,TREE_KEYS);need(Array.isArray(tree.receivers)&&tree.receivers.length<=tree.n,'receivers-shape');
 const base={};for(const k of Object.keys(tree))if(k!=='receivers')base[k]=tree[k];baseCheck(base);
 const out={schema:SCHEMA,base,receiverIds:[],cullOffsets:[0],cullCodes:[],cullDifferences:[],leavesRefs:[],gathered:[]};
 for(const r of tree.receivers){
  guard();keys(r,['receiver','culled','leavesRef','gathered']);need(integer(r.receiver,0,tree.n-1)&&Array.isArray(r.culled),'receiver-shape');
  need(r.leavesRef===null||integer(r.leavesRef,0,tree.leafDictionary.length-1),'leaf-ref');out.receiverIds.push(r.receiver);out.leavesRefs.push(r.leavesRef);
  for(const c of r.culled){
   keys(c,['node','axis','side','difference']);need(integer(c.node,0,tree.nodes.length-1)&&integer(c.axis,0,2)&&(c.side==='min-ge4'||c.side==='max-le-neg4')&&typeof c.difference==='string'&&WORD.test(c.difference),'cull-shape');
   const code=c.node*6+c.axis*2+(c.side==='max-le-neg4'?1:0);need(integer(code),'cull-code');out.cullCodes.push(code);out.cullDifferences.push(c.difference);
  }
  out.cullOffsets.push(out.cullCodes.length);const actual=expandOld(r.gathered,tree.n,guard);out.gathered.push(actual===null?null:selected(actual,tree.n,guard));
 }
 return out;
}
function decode(layout,guard=()=>{}){
 if(layout===null)return null;keys(layout,LAYOUT_KEYS);need(layout.schema===SCHEMA,'schema');baseCheck(layout.base);const n=layout.base.n;
 for(const k of LAYOUT_KEYS.slice(2))need(Array.isArray(layout[k]),'column-array');const count=layout.receiverIds.length;
 need(count<=n&&layout.cullOffsets.length===count+1&&layout.leavesRefs.length===count&&layout.gathered.length===count&&layout.cullCodes.length===layout.cullDifferences.length&&layout.cullOffsets[0]===0,'column-shapes');
 need(layout.cullOffsets.every(v=>integer(v))&&layout.cullOffsets[count]===layout.cullCodes.length,'offset-end');
 const receivers=[];
 for(let i=0;i<count;i++){
  guard();const receiver=layout.receiverIds[i],leaf=layout.leavesRefs[i],start=layout.cullOffsets[i],end=layout.cullOffsets[i+1];
  need(integer(receiver,0,n-1)&&(leaf===null||integer(leaf,0,layout.base.leafDictionary.length-1))&&start<=end&&end<=layout.cullCodes.length,'receiver-column');
  const culled=[];for(let j=start;j<end;j++){
   const code=layout.cullCodes[j],word=layout.cullDifferences[j];need(integer(code)&&typeof word==='string'&&WORD.test(word),'cull-column');const node=Math.floor(code/6),axis=Math.floor((code%6)/2),side=code%2;
   need(node<layout.base.nodes.length,'cull-node');culled.push({node,axis,side:side?'max-le-neg4':'min-ge4',difference:word});
  }
  const actual=expandNew(layout.gathered[i],n,guard);receivers.push({receiver,culled,leavesRef:leaf,gathered:actual===null?null:oldGather(actual,n,guard)});
 }
 return {...layout.base,receivers};
}
module.exports={SCHEMA,encode,decode,equal,selected,expandNew,expandOld};
