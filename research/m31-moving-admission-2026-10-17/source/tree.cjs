'use strict';
const R=require('./rational.cjs'),B=require('./boxes.cjs'),A=require('./adapter.cjs'),spec=require('./spec.json');
const C=A.exact,le=(a,b)=>R.cmp(a,b)<=0,ge=(a,b)=>R.cmp(a,b)>=0,lt=(a,b)=>R.cmp(a,b)<0,gt=(a,b)=>R.cmp(a,b)>0,q=n=>R.q(BigInt(n));
function globalGuard(exact){
 const values=[...exact.values()],centers=B.bounds(values.map(d=>d.center)),axes=B.bounds(values.map(d=>d.axis)),points=B.bounds(values.flatMap(d=>d.points));
 const centerDiff=B.difference(centers,centers),d=B.difference(centers,points),h=B.dot(d,axes),e=d.map((v,k)=>B.sub(v,B.mul(h,axes[k])));
 const checks={centerComponent:centerDiff.every(v=>le(B.absMax(v),q(257))),centerNorm:le(B.normUpper2(centerDiff),q(512*512)),rotorComponent:d.every(v=>le(B.absMax(v),q(258))),down:le(B.absMax(h),q(1024)),radial:le(B.normUpper2(e),q(2048*2048))};
 return {passed:Object.values(checks).every(Boolean),checks};
}
function build(exact){
 const permutation=[],nodes=[];
 function visit(ids){
  const center=B.bounds(ids.map(id=>exact.get(id).center)),axis=B.bounds(ids.map(id=>exact.get(id).axis));
  const id=nodes.length,node={id,start:permutation.length,end:null,left:null,right:null,center,axis};nodes.push(node);
  if(ids.length<=spec.leafCapacity)permutation.push(...ids);
  else{
   const span=center.map(v=>R.sub(v[1],v[0]));let k=0;for(let j=1;j<3;j++)if(gt(span[j],span[k]))k=j;
   const sorted=ids.slice().sort((a,b)=>R.cmp(exact.get(a).center[k],exact.get(b).center[k])||a-b),mid=Math.floor(sorted.length/2);
   node.left=visit(sorted.slice(0,mid));node.right=visit(sorted.slice(mid));
  }
  node.end=permutation.length;return id;
 }
 visit([...exact.keys()]);return {permutation,nodes};
}
function zeroRule(node,receiver,rotor,work){
 work.nodeRuleTests++;
 const c=receiver.center.map(B.point),p=receiver.points[rotor].map(B.point);
 if(ge(B.normLower2(B.difference(node.center,c)),R.sq(C.neighbor)))return 'neighbor';
 const d=B.difference(node.center,p),h=B.dot(d,node.axis);
 work.nodeRuleTests++;if(le(h[1],R.zero))return 'upstream';
 work.nodeRuleTests++;if(ge(h[0],C.downCut))return 'down-cut';
 const e=d.map((v,k)=>B.sub(v,B.mul(h,node.axis[k]))),r2=B.normLower2(e),near=R.mul(C.minDown,C.D);
 work.nodeRuleTests++;if(lt(h[1],near)&&ge(r2,R.sq(C.nearRad)))return 'near-outside';
 const width=B.scale(B.scale(B.sub(B.dividePositive(h,C.D),B.point(C.origin)),C.spread),C.D);
 work.nodeRuleTests++;if(ge(h[0],near)&&gt(width[0],R.zero)&&ge(r2,R.sq(R.mul(C.radCut,width[1]))))return 'radial';
 return null;
}
const wire=tree=>({permutation:tree.permutation,nodes:tree.nodes.map(n=>({...n,center:B.wire(n.center),axis:B.wire(n.axis)}))});
module.exports={globalGuard,build,zeroRule,wire};
