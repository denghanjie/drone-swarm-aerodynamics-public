'use strict';
/* SOURCE-ONLY. No numerical initialization, model imports, I/O or execution at
 * import. Explicit calls are science and must be inside the reserved envelope.
 * R arithmetic provenance: independent-frozen.source.txt. Rotation, fades,
 * profile grouping, ordinary/Neumaier updates and bisection are preserved.
 * Added: saved compact evidence, domain guards, early-failure prefixes, masks,
 * same-solve termination diagnostics and explicit parameterization for Q/H.
 */
function assertion(ok, message, detail) {
  if (!ok) { const e = new Error(message); e.name = 'BodyContractError'; e.detail = detail; throw e; }
}
function fbits(value) { const v = new DataView(new ArrayBuffer(4)); v.setFloat32(0,value,true); return v.getUint32(0,true); }
function fvalue(word) { const v = new DataView(new ArrayBuffer(4)); v.setUint32(0,word,true); return v.getFloat32(0,true); }
function wordFinite(w) { return (w & 0x7f800000) !== 0x7f800000; }
function wordZero(w) { return (w & 0x7fffffff) === 0; }
function wordSubnormal(w) { return (w & 0x7f800000) === 0 && (w & 0x7fffff) !== 0; }
function wordNormalPositive(w) { return (w >>> 31) === 0 && (w & 0x7f800000) !== 0 && wordFinite(w); }
function appliedWord(w) { return (wordZero(w) || wordSubnormal(w)) ? 0 : w; }
function dataView(value) {
  if (value instanceof ArrayBuffer) return new DataView(value);
  assertion(ArrayBuffer.isView(value), 'Expected binary view');
  return new DataView(value.buffer,value.byteOffset,value.byteLength);
}
function adjacent64(x,direction) {
  assertion(x>0 && Number.isFinite(x) && (direction===1||direction===-1),'Adjacent64 input');
  const v=new DataView(new ArrayBuffer(8));v.setFloat64(0,x,false);v.setBigUint64(0,v.getBigUint64(0,false)+BigInt(direction),false);return v.getFloat64(0,false);
}
function adjacent32(x,direction) { assertion(x>0 && Number.isFinite(x),'Adjacent32 input');return fvalue(fbits(x)+direction); }
function createConfig() {
  const m=.027,g=9.81,a=.028,rho=1.225,radius=.023;
  const area=Math.PI*radius*radius;
  const names=['D','decay','spread','origin','minDown','neighbor','nearRad','downFade','downCut','radFade','radCut','cosTilt','induced','sqrt2minus1','rho','area','arm','yawRatio','maxNominal','Umax'];
  const values=[2*Math.sqrt(2)*a,10.11,.07668,-5.817,2.5,3,.15,2,2.5,2,3,Math.cos(20*Math.PI/180),Math.sqrt(m*g/(8*rho*area)),Math.sqrt(2)-1,rho,area,a,7.94e-12/3.16e-10,((2.25*m)*g)/4,2**20];
  const original={},decoded={},packedConstants=new Uint32Array(32);
  names.forEach((name,k)=>{original[name]=values[k];packedConstants[k]=fbits(values[k]);decoded[name]=fvalue(packedConstants[k]);});
  const epsT=.005*m*g,epsM=.0005*m*g*original.D,epsRotor=.5*Math.min(epsT/4,epsM/(4*a));
  return {version:1,names,original,decoded,packedConstants,gates:{epsT,epsM,epsRotor,forceMargin:1e-12,momentMargin:1e-13,handoff:epsRotor/4,sumAgreement:1e-10,referenceResidual:1e-12,referenceWidth:2e-15,candidateResidual:2e-6,exposure:.25}};
}
function constantsFor(config,N) { assertion(Number.isInteger(N)&&N>=1&&N<=5000,'N range');const words=config.packedConstants.slice();words[20]=N;return words; }
// Exact source grouping of original independent quaternion rotation.
function rotateI(q,v) { const [x,y,z,w]=q,[vx,vy,vz]=v;return [
  (1-2*(y*y+z*z))*vx+2*(x*y-z*w)*vy+2*(x*z+y*w)*vz,
  2*(x*y+z*w)*vx+(1-2*(x*x+z*z))*vy+2*(y*z-x*w)*vz,
  2*(x*z-y*w)*vx+2*(y*z+x*w)*vy+(1-2*(x*x+y*y))*vz]; }
// Verbatim production helpers and rotate grouping, physics.cjs lines5,7.
function add(a,b){return a.map((x,i)=>x+b[i]);}
function scale(a,k){return a.map(x=>x*k);}
function cross(a,b){return [a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]];}
function rotateProduction(q,v){const t=scale(cross(q,v),2);return add(v,add(scale(t,q[3]),cross(q,t)));}
function invokeGuard(options,event) { if(options&&options.guard) options.guard(event); }
function charge(options,name,count) { if(options&&options.charge) options.charge(name,count); }
function preparedAdmission(p,N,c) {
  assertion(p instanceof Float64Array&&p.length===28*N,'Prepared shape');
  let maxAxisNormDrift=0,minTiltMargin=Infinity;
  for(let i=0;i<N;i++) { const b=28*i;
    for(let k=0;k<28;k++) assertion(Number.isFinite(p[b+k]),'Nonfinite prepared',{i,k});
    for(const k of [3,7,11,15,19,23]) assertion(Object.is(p[b+k],0),'Nonzero prepared pad',{i,k});
    for(let k=0;k<3;k++) assertion(Math.abs(p[b+k])<=128&&Math.abs(p[b+4+k])<=1.01,'Prepared node range',{i,k});
    assertion(p[b+6]>=c.cosTilt,'Global tilt admission',{i,axisZ:p[b+6]});
    maxAxisNormDrift=Math.max(maxAxisNormDrift,Math.abs(Math.hypot(p[b+4],p[b+5],p[b+6])-1));
    minTiltMargin=Math.min(minTiltMargin,p[b+6]-c.cosTilt);
    for(let k=8;k<24;k++) assertion(Math.abs(p[b+k])<=.1,'Offset admission',{i,k});
    for(let k=24;k<28;k++) assertion(p[b+k]>=0&&p[b+k]<=c.maxNominal,'Motor admission',{i,k});
  }
  return {maxAxisNormDrift,minTiltMargin};
}
function prepare(states,config,options={}) {
  assertion(Array.isArray(states)&&states.length>=2&&states.length<=5000,'State array/N admission');
  const N=states.length,originalStates=new Float64Array(17*N),candidatePrepared=new Float64Array(28*N),referencePrepared=new Float64Array(28*N),decodedPrepared=new Float64Array(28*N);
  const packed={nodes:new Uint32Array(8*N),offsets:new Uint32Array(16*N),motors:new Uint32Array(4*N)};
  const out={N,originalStates,candidatePrepared,referencePrepared,decodedPrepared,packed,admission:null,completed:false,status:'preparing'};
  let completedStates=0,currentReceiver=-1;
  try {
    const a=config.original.arm,arms=[[a,a,0],[-a,a,0],[-a,-a,0],[a,-a,0]];
    let maxQuaternionNormDrift=0,originalZero=0,packedZeroFromPositive=0,packedSubnormal=0;
    for(let i=0;i<N;i++) {
      currentReceiver=i;
      invokeGuard(options,{stage:'prepare',receiver:i,N});charge(options,'prepareStates',1);
      const s=states[i];assertion(s&&s.length===17&&Array.from(s).every(Number.isFinite),'Original finite17',{i});
      const q=Array.from(s).slice(6,10),drift=Math.abs(Math.hypot(...q)-1);assertion(drift<=1e-10,'Original quaternion norm',{i,drift});maxQuaternionNormDrift=Math.max(maxQuaternionNormDrift,drift);
      for(let k=0;k<3;k++) assertion(Math.abs(s[k])<=128,'Original position',{i,k});
      for(let k=13;k<17;k++) assertion(s[k]>=0&&s[k]<=config.original.maxNominal,'Original nominal',{i,k});
      originalStates.set(s,17*i);
      for(const [p,rotate] of [[candidatePrepared,rotateProduction],[referencePrepared,rotateI]]) {
        p.set(s.slice(0,3),28*i);p.set(rotate(q,[0,0,1]),28*i+4);
        for(let r=0;r<4;r++)p.set(rotate(q,arms[r]),28*i+8+4*r);
        p.set(s.slice(13,17),28*i+24);
      }
      for(let k=0;k<28;k++) { const w=fbits(candidatePrepared[28*i+k]);decodedPrepared[28*i+k]=fvalue(w);
        if(k<8)packed.nodes[8*i+k]=w;else if(k<24)packed.offsets[16*i+k-8]=w;else packed.motors[4*i+k-24]=w;
      }
      for(let r=0;r<4;r++){const n=s[13+r],w=packed.motors[4*i+r];if(n===0)originalZero++;if(n>0&&wordZero(w))packedZeroFromPositive++;if(wordSubnormal(w))packedSubnormal++;}
      completedStates++;
    }
    charge(options,'preparedAdmissionRowsReserved',3*N);
    out.admission={R:preparedAdmission(referencePrepared,N,config.original),candidate:preparedAdmission(candidatePrepared,N,config.original),Q:preparedAdmission(decodedPrepared,N,config.decoded),maxQuaternionNormDrift,originalZero,packedZeroFromPositive,packedSubnormal};
    out.completed=true;out.status='complete';return out;
  } catch(error){out.status='failed';out.failure={message:error.message,detail:error.detail||null};error.partial={kind:'preparation',buffers:{originalStates,candidatePrepared,referencePrepared,decodedPrepared,nodes:packed.nodes,offsets:packed.offsets,motors:packed.motors},metadata:{complete:false,N,counts:{completedStates,currentReceiver},stage:'prepare-or-admission',failure:out.failure}};throw error;}
}
function fade(start,end,value){if(value<=start)return 1;if(value>=end)return 0;const t=(value-start)/(end-start);return (1-t)*(1-t)*(1+2*t);}
function dotAt(p,a,b){return p[a]*p[b]+p[a+1]*p[b+1]+p[a+2]*p[b+2];}
function pairTerm(p,i,j,r,c,centerAlreadyEligible=false) {
  const ib=28*i,jb=28*j,ob=ib+8+4*r;
  const out={symbol:0,term:0,down:0,radial:0,projection:0,center:0,validity:0,stage:0};
  if(i===j){out.symbol=1;out.validity=1;return out;}
  if(!centerAlreadyEligible){const dx=p[jb]-p[ib],dy=p[jb+1]-p[ib+1],dz=p[jb+2]-p[ib+2];out.center=Math.hypot(dx,dy,dz);out.validity|=16;
    if(!Number.isFinite(out.center)||out.center>512||Math.max(Math.abs(dx),Math.abs(dy),Math.abs(dz))>257){out.symbol=11;out.stage=3;return out;}
    if(out.center>=c.neighbor){out.symbol=1;out.validity|=1;return out;}}
  const px=p[ib]+p[ob],py=p[ib+1]+p[ob+1],pz=p[ib+2]+p[ob+2];
  const dx=p[jb]-px,dy=p[jb+1]-py,dz=p[jb+2]-pz;
  if(![dx,dy,dz].every(Number.isFinite)||Math.max(Math.abs(dx),Math.abs(dy),Math.abs(dz))>258){out.symbol=11;out.stage=4;return out;}
  const ax=p[jb+4],ay=p[jb+5],az=p[jb+6];
  const down=dx*ax+dy*ay+dz*az;out.down=down;
  if(!Number.isFinite(down)||Math.abs(down)>1024){out.symbol=11;out.stage=4;return out;}out.validity|=2;
  if(down<=0){out.symbol=2;out.validity|=1;return out;}
  if(down>=c.downCut){out.symbol=3;out.validity|=1;return out;}
  const radial=Math.hypot(dx-down*ax,dy-down*ay,dz-down*az);out.radial=radial;
  if(!Number.isFinite(radial)||radial>2048){out.symbol=11;out.stage=4;return out;}out.validity|=4;
  if(down<c.minDown*c.D){out.symbol=radial<c.nearRad?4:5;out.stage=out.symbol===4?4:0;if(out.symbol===5)out.validity|=1;return out;}
  const normalizedDown=down/c.D;
  const halfWidth=c.spread*(normalizedDown-c.origin)*c.D;
  if(!(halfWidth>0)||!Number.isFinite(halfWidth)){out.symbol=11;out.stage=4;return out;}
  if(radial>=c.radCut*halfWidth){out.symbol=6;out.validity|=1;return out;}
  const receiverProjection=Math.max(0,p[ib+4]*ax+p[ib+5]*ay+p[ib+6]*az);out.projection=receiverProjection;out.validity|=8;
  const xi=(radial/c.D)/(c.spread*(normalizedDown-c.origin));
  const denominator=1+c.sqrt2minus1*xi*xi;
  const normalizedSpeed=(c.decay/(normalizedDown-c.origin))/(denominator*denominator);
  const speed=normalizedSpeed*c.induced*fade(c.downFade,c.downCut,down)*fade(c.radFade,c.radCut,radial/halfWidth)*receiverProjection;
  if(!termAdmitted(speed)||!Number.isFinite(receiverProjection)){out.symbol=11;out.stage=4;return out;}
  out.term=speed;out.validity|=1;out.symbol=receiverProjection<=0?7:(speed>0?8:9);return out;
}
function rootReference(nominal,inflow,c,counters,options={}) {
  counters.rootAttempts++;charge(options,'referenceRootAttempts',1);
  const s={nominal,inflow,vi:0,alpha:0,x:0,force:0,lower:0,upper:0,residual:0,iterations:0,status:0,termination:0,mask:0,productZero:false,consistency:null};
  if(!Number.isFinite(nominal)||nominal<0||nominal>c.maxNominal||!Number.isFinite(inflow)||inflow<0||inflow>c.Umax){s.status=4;return s;}
  s.mask=7;
  if(nominal===0){s.status=1;s.termination=1;s.mask=0x1e7;s.consistency={pass:true,forceWidth:0};return s;}
  if(inflow===0){s.status=2;s.termination=1;s.mask=0x3f7;s.x=1;s.force=nominal;s.lower=1;s.upper=1;s.consistency={pass:true,forceWidth:0};return s;}
  s.vi=Math.sqrt(nominal/(2*c.rho*c.area));s.alpha=inflow/s.vi;
  if(Number.isFinite(s.vi)&&s.vi>0)s.mask|=8;
  if(Number.isFinite(s.alpha)&&s.alpha>=0)s.mask|=16;
  if(!Number.isFinite(s.alpha)||s.alpha<0||!Number.isFinite(s.vi)||s.vi<=0){s.status=5;return s;}
  let lower=0,upper=Math.min(1,1/s.alpha),iterations=0,termination=4;
  counters.bisectionSolves++;charge(options,'referenceBisectionSolves',1);
  for(;iterations<96;iterations++) {
    const middle=lower+(upper-lower)/2;
    if(middle===lower||middle===upper){termination=3;break;}
    const value=middle*middle*middle+s.alpha*middle-1;
    if(value===0){lower=middle;upper=middle;iterations++;termination=2;break;}
    if(value<0)lower=middle;else upper=middle;
  }
  counters.bisectionIterations+=iterations;charge(options,'referenceBisectionIterations',iterations);
  const x=lower+(upper-lower)/2;
  s.x=x;s.force=nominal*x;s.lower=lower;s.upper=upper;s.residual=x*x*x+s.alpha*x-1;s.iterations=iterations;s.termination=termination;s.mask=0x3ff;s.status=3;s.productZero=s.force===0;
  s.consistency=checkReferenceRoot(s,c);if(!s.consistency.pass)s.status=6;
  return s;
}
function checkReferenceRoot(s,c) {
  if(!Number.isFinite(s.nominal)||s.nominal<0||s.nominal>c.maxNominal||!sumAdmitted(s.inflow,c)||![1,2,3].includes(s.status))return {pass:false,forceWidth:0};
  if(s.status===1)return {pass:s.nominal===0&&Object.is(s.force,0)&&Object.is(s.x,0)&&Object.is(s.lower,0)&&Object.is(s.upper,0)&&s.iterations===0&&s.termination===1&&!s.productZero,forceWidth:0};
  if(s.status===2)return {pass:s.nominal>0&&s.inflow===0&&s.force===s.nominal&&s.x===1&&s.lower===1&&s.upper===1&&s.alpha===0&&Object.is(s.residual,0)&&s.iterations===0&&s.termination===1&&!s.productZero,forceWidth:0};
  const p=x=>x*x*x+s.alpha*x-1,loP=p(s.lower),hiP=p(s.upper),residual=p(s.x),width=s.upper-s.lower;
  const pass=[s.nominal,s.inflow,s.vi,s.alpha,s.x,s.force,s.lower,s.upper,s.residual].every(Number.isFinite)&&s.nominal>0&&s.inflow>0&&s.inflow<=c.Umax&&s.nominal<=c.maxNominal&&s.vi>0&&s.alpha>=0&&Object.is(s.vi,Math.sqrt(s.nominal/(2*c.rho*c.area)))&&Object.is(s.alpha,s.inflow/s.vi)&&s.x>0&&s.x<=1&&s.lower>=0&&s.lower<=s.x&&s.x<=s.upper&&s.upper<=(s.alpha>0?Math.min(1,1/s.alpha):1)&&width<=2e-15&&s.iterations<=96&&s.iterations>=0&&Number.isInteger(s.iterations)&&Math.abs(residual)<=1e-12&&loP<=1e-12&&hiP>=-1e-12&&s.force>=0&&s.force<=s.nominal&&Object.is(s.force,s.nominal*s.x)&&Object.is(s.residual,residual)&&[2,3,4].includes(s.termination)&&s.productZero===(s.force===0);
  return {pass,forceWidth:s.nominal*width,residual,lowerPolynomial:loP,upperPolynomial:hiP};
}
function bodyFromForces(forces,nominals,c) {
  const [f0,f1,f2,f3]=forces,[n0,n1,n2,n3]=nominals;
  return {effective:[f0+f1+f2+f3,c.arm*(f0+f1-f2-f3),c.arm*(-f0+f1+f2-f3),c.yawRatio*(n0-n1+n2-n3)],nominal:[n0+n1+n2+n3,c.arm*(n0+n1-n2-n3),c.arm*(-n0+n1+n2-n3),c.yawRatio*(n0-n1+n2-n3)]};
}
function header(view,base,id,N,status,stage=0,full=0,symbols=0,slot=0xffffffff,validity=0) { [id,N,status,stage,full,symbols,slot,validity].forEach((v,k)=>view.setUint32(base+4*k,v,true)); }
function writeReferenceRoot(view,b,s,Ucomp,positiveTerms) {
  const values=[s.inflow,Ucomp,s.nominal,s.vi,s.alpha,s.x,s.force,s.lower,s.upper,s.residual];
  values.forEach((v,k)=>view.setFloat64(b+8*k,(s.mask&(1<<k))?v:0,true));
  let flags=s.mask|(s.termination<<10)|(s.productZero?1<<13:0)|(Object.is(s.nominal,-0)?1<<14:0)|(Object.is(s.inflow,-0)?1<<15:0);
  view.setUint32(b+80,s.status,true);view.setUint32(b+84,s.iterations,true);view.setUint32(b+88,flags,true);view.setUint32(b+92,positiveTerms,true);
}
function readReferenceRoot(view,b) {
  const a=Array.from({length:10},(_,k)=>view.getFloat64(b+8*k,true)),flags=view.getUint32(b+88,true);
  return {inflow:a[0],compensated:a[1],nominal:a[2],vi:a[3],alpha:a[4],x:a[5],force:a[6],lower:a[7],upper:a[8],residual:a[9],status:view.getUint32(b+80,true),iterations:view.getUint32(b+84,true),mask:flags&1023,termination:(flags>>>10)&7,productZero:!!(flags&(1<<13)),flags,positiveTerms:view.getUint32(b+92,true)};
}
function newCounters(){return {receiversAttempted:0,receiversCompleted:0,centerChecks:0,eligiblePairs:0,rotorVisits:0,terminalSymbols:0,rootAttempts:0,bisectionSolves:0,bisectionIterations:0,bodyAssemblies:0};}
function runReference(prepared,path,config,options={}) {
  assertion(path==='R'||path==='Q','Reference path');assertion(prepared.completed,'Prepared not admitted');
  const {N}=prepared,p=path==='R'?prepared.referencePrepared:prepared.decodedPrepared,c=path==='R'?config.original:config.decoded;
  const policy=new Uint16Array(N*N),output=new ArrayBuffer(480*N),v=new DataView(output),counters=newCounters();
  const result={path,N,policy,output,counters,completed:false,status:'running',failure:null};
  let current=-1;
  const flushed={centerChecks:0,eligiblePairs:0,rotorVisits:0,terminalSymbols:0};
  function flushFieldCounters(){for(const [key,name] of [['centerChecks','referenceCenterChecks'],['eligiblePairs','referenceEligiblePairs'],['rotorVisits','referenceRotorVisits'],['terminalSymbols','referenceTerminalSymbols']]){const delta=counters[key]-flushed[key];flushed[key]=counters[key];if(delta)charge(options,name,delta);}}
  function stop(status,stage,slot,message,detail){header(v,current*480,current,N,status,stage,v.getUint32(current*480+16,true),v.getUint32(current*480+20,true),slot,v.getUint32(current*480+28,true));result.status='failed';result.failure={receiver:current,stage,slot,message,detail};flushFieldCounters();return result;}
  function writeSymbol(i,j,r,symbol){const k=i*N+j,shift=4*r,prior=policy[k];assertion(((prior>>>shift)&15)===0,'Duplicate policy write',{i,j,r});policy[k]=prior|(symbol<<shift);counters.terminalSymbols++;const b=i*480;v.setUint32(b+20,v.getUint32(b+20,true)+1,true);v.setUint32(b+28,v.getUint32(b+28,true)|1,true);const now=policy[k];if((now&15)&&((now>>>4)&15)&&((now>>>8)&15)&&((now>>>12)&15))v.setUint32(b+16,v.getUint32(b+16,true)+1,true);}
  try {
    for(let i=0;i<N;i++) {current=i;counters.receiversAttempted++;invokeGuard(options,{stage:'reference-receiver',path,receiver:i,counters});charge(options,'referenceReceivers',1);header(v,i*480,i,N,1);
      const eligible=new Uint32Array(N);let eligibleCount=0;
      for(let j=0;j<N;j++) {
        if(j===i){for(let r=0;r<4;r++)writeSymbol(i,j,r,1);continue;}
        counters.centerChecks++;const dx=p[28*j]-p[28*i],dy=p[28*j+1]-p[28*i+1],dz=p[28*j+2]-p[28*i+2],center=Math.hypot(dx,dy,dz);
        if(!Number.isFinite(center)||center>512||Math.max(Math.abs(dx),Math.abs(dy),Math.abs(dz))>257){writeSymbol(i,j,0,11);return stop(5,3,j*4,'Center guard');}
        if(center<c.neighbor){eligible[eligibleCount++]=j;counters.eligiblePairs++;}else for(let r=0;r<4;r++)writeSymbol(i,j,r,1);
      }
      const totals=new Float64Array(4),comp=new Float64Array(4),positive=new Uint32Array(4);
      for(let r=0;r<4;r++) {let total=0,correction=0;
        for(let k=0;k<eligibleCount;k++){const j=eligible[k];counters.rotorVisits++;const term=pairTerm(p,i,j,r,c,true);writeSymbol(i,j,r,term.symbol);
          if(term.symbol===4)return stop(3,4,j*4+r,'Near-domain invalid');if(term.symbol===10||term.symbol===11)return stop(5,term.stage||4,j*4+r,'Term arithmetic invalid');
          if(term.symbol===7||term.symbol===8||term.symbol===9){const speed=term.term,next=total+speed;correction+=Math.abs(total)>=Math.abs(speed)?(total-next)+speed:(speed-next)+total;total=next;if(speed>0)positive[r]++;}
        }
        totals[r]=total;comp[r]=total+correction;
        if(!sumAdmitted(total,c)||!sumAdmitted(comp[r],c))return stop(6,5,r,'Sum range',{ordinary:total,compensated:comp[r]});
        const partialRoot=i*480+32+96*r;v.setFloat64(partialRoot,total,true);v.setFloat64(partialRoot+8,comp[r],true);v.setFloat64(partialRoot+16,p[28*i+24+r],true);v.setUint32(partialRoot+88,7,true);v.setUint32(partialRoot+92,positive[r],true);
        if(Math.abs(total-comp[r])>config.gates.sumAgreement)return stop(5,5,r,'Ordinary/Neumaier disagreement');
      }
      v.setUint32(i*480+28,3,true);const roots=[],forces=[],nominals=[];let firstRootFailure=-1;
      for(let r=0;r<4;r++){const n=p[28*i+24+r],s=rootReference(n,totals[r],c,counters,options);writeReferenceRoot(v,i*480+32+96*r,s,comp[r],positive[r]);roots.push(s);forces.push(s.force);nominals.push(n);if(s.status<1||s.status>3){if(firstRootFailure<0)firstRootFailure=r;}}
      v.setUint32(i*480+28,7,true);if(firstRootFailure>=0)return stop(7,7,firstRootFailure,'Reference root failure',roots[firstRootFailure]);
      const body=bodyFromForces(forces,nominals,c);counters.bodyAssemblies++;charge(options,'referenceBodyAssemblies',1);
      if(![...body.effective,...body.nominal].every(Number.isFinite))return stop(8,9,0,'Body nonfinite');
      [...body.effective,...body.nominal].forEach((x,k)=>v.setFloat64(i*480+416+8*k,x,true));header(v,i*480,i,N,2,0,N,4*N,0xffffffff,31);counters.receiversCompleted++;
      flushFieldCounters();
      invokeGuard(options,{stage:'reference-receiver-complete',path,receiver:i,counters});
    }
    result.completed=true;result.status='complete';return result;
  }catch(error){result.status='failed';result.failure={receiver:current,message:error.message,detail:error.detail||null};error.partial=result;throw error;}
}
function writeHandoffRoot(v,b,s) {
  const mask=s.mask===0x1e7?0x3c:s.mask===0x3f7?0x7e:s.mask===0x3ff?0x7f:0;
  [s.vi,s.alpha,s.x,s.force,s.lower,s.upper,s.residual].forEach((x,k)=>v.setFloat64(b+8*k,(mask&(1<<k))?x:0,true));
  v.setUint32(b+56,s.iterations,true);v.setUint32(b+60,s.status|(s.termination<<4)|(mask<<8)|(s.productZero?1<<15:0),true);
}
function readHandoffRoot(v,b,nominal,inflow) {
  const a=Array.from({length:7},(_,k)=>v.getFloat64(b+8*k,true)),meta=v.getUint32(b+60,true);
  return {nominal,inflow,vi:a[0],alpha:a[1],x:a[2],force:a[3],lower:a[4],upper:a[5],residual:a[6],iterations:v.getUint32(b+56,true),status:meta&15,termination:(meta>>>4)&7,mask:(meta>>>8)&127,productZero:!!(meta&(1<<15)),meta};
}
function readGpuRoot(v,b) {
  const word=k=>v.getUint32(b+4*k,true),float=k=>v.getFloat32(b+4*k,true),meta=word(8);
  return {inflow:float(0),inflowWord:word(0),nominal:float(1),nominalWord:word(1),vi:float(2),viWord:word(2),coefficient:float(3),coefficientWord:word(3),x:float(4),force:float(5),forceWord:word(5),residual:float(6),step:float(7),meta,branch:meta&7,iterations:(meta>>>3)&15,status:(meta>>>7)&7,flags:(meta>>>10)&65535,mask:word(9),positiveTerms:word(10),pad:word(11)};
}
function runHandoff(gpuOutput,prepared,config,options={}) {
  const gv=dataView(gpuOutput),N=prepared.N;assertion(gv.byteLength===256*N,'GPU output shape');
  const output=new ArrayBuffer(288*N),v=new DataView(output),counters=newCounters(),result={N,output,counters,completed:false,status:'running',failure:null};
  try{
    for(let i=0;i<N;i++){invokeGuard(options,{stage:'handoff',receiver:i,counters});charge(options,'handoffReceivers',1);counters.receiversAttempted++;header(v,i*288,i,N,1);let invalid=-1,attempted=0;
      for(let r=0;r<4;r++){const g=readGpuRoot(gv,i*256+32+48*r);if((g.mask&3)!==3||g.nominalWord!==prepared.packed.motors[4*i+r]){if(invalid<0)invalid=r;continue;}
        const s=rootReference(g.nominal,g.inflow,config.decoded,counters,options);attempted++;writeHandoffRoot(v,i*288+32+64*r,s);if((s.status<1||s.status>3)&&invalid<0)invalid=r;}
      if(invalid>=0){header(v,i*288,i,N,7,7,0,0,invalid,attempted===4?4:0);result.status='failed';result.failure={receiver:i,rotor:invalid,attempted};return result;}
      header(v,i*288,i,N,2,0,0,0,0xffffffff,4);counters.receiversCompleted++;
    }result.completed=true;result.status='complete';return result;
  }catch(error){result.status='failed';result.failure={message:error.message,detail:error.detail||null};error.partial=result;throw error;}
}
function dyadic(x) {
  assertion(Number.isFinite(x),'Finite exact-comparison operand');
  const v=new DataView(new ArrayBuffer(8));v.setFloat64(0,x,false);const bits=v.getBigUint64(0,false),e=Number((bits>>52n)&2047n),f=bits&((1n<<52n)-1n),sign=(bits>>63n)?-1n:1n;
  return {n:sign*(e===0?f:(1n<<52n)|f),e:e===0?-1074:e-1075};
}
function exactMarginGate(a,b,margin,limit) {
  if(![a,b,margin,limit].every(Number.isFinite))return false;
  const d=[a,b,margin,limit].map(dyadic),e=Math.min(...d.map(v=>v.e)),q=d.map(v=>v.n<<BigInt(v.e-e));const delta=q[0]-q[1];return (delta<0n?-delta:delta)+q[2]<=q[3];
}
function checkGpuRoot(g,expectedNominalWord,c) {
  const failures=[];const check=(ok,why)=>{if(!ok)failures.push(why);};
  check(g.pad===0&&g.mask<=255&&(g.meta&0xfc000000)===0&&(g.flags&0xf800)===0,'root reserved');
  check(g.nominalWord===expectedNominalWord,'raw nominal binding');
  check(wordFinite(g.nominalWord)&&wordFinite(g.inflowWord)&&g.nominal>=0&&g.nominal<=c.maxNominal&&g.inflow>=0&&g.inflow<=c.Umax,'root raw admission');
  check(g.status===1,'root valid status');
  const nw=appliedWord(g.nominalWord),uw=appliedWord(g.inflowWord),n=fvalue(nw),U=fvalue(uw);
  const flags=(wordSubnormal(g.nominalWord)?1:0)|(wordSubnormal(g.inflowWord)?2:0)|(wordZero(g.nominalWord)?4:0)|(wordZero(g.inflowWord)?8:0)|(g.nominalWord===0x80000000?16:0)|(g.inflowWord===0x80000000?32:0);
  check((g.flags&63)===flags,'canonicalization flags');
  let normalizedResidual=null;
  if(n===0||U===0){const branch=n===0?1:2;check(g.branch===branch&&g.iterations===0&&g.mask===51,'identity metadata');check(g.x===(n===0?0:1)&&Object.is(g.force,n===0?0:n),'identity outputs');check(g.viWord===0&&g.coefficientWord===0&&Object.is(g.residual,0)&&Object.is(g.step,0),'identity masked fields');check((g.flags&~63)===0,'identity unexpected arithmetic flag');}
  else{
    check(g.mask===255&&g.iterations===12,'positive metadata');check(wordNormalPositive(g.viWord),'vi normal positive');
    check((g.coefficientWord>>>31)===0&&(g.forceWord>>>31)===0,'nonnegative arithmetic encodings');
    check(Number.isFinite(g.x)&&g.x>0&&g.x<=1&&Number.isFinite(g.force)&&g.force>=0&&g.force<=n&&Number.isFinite(g.residual)&&Number.isFinite(g.step),'positive outputs');
    if(U<=g.vi){check(g.branch===3&&Number.isFinite(g.coefficient)&&g.coefficient>=0&&g.coefficient<=1,'low branch/coefficient');normalizedResidual=g.x*g.x*g.x+g.coefficient*g.x-1;
      check(!!(g.flags&64)===(g.coefficient===0),'alpha zero flag');check(!!(g.flags&128)===wordSubnormal(g.coefficientWord),'alpha subnormal flag');
    }else{check(g.branch===4&&wordNormalPositive(g.coefficientWord)&&g.coefficient<=1,'high branch/coefficient');normalizedResidual=g.x*g.x*g.x+g.x/g.coefficient-1;check((g.flags&192)===0,'high alpha flags');}
    check(Number.isFinite(normalizedResidual)&&Math.abs(normalizedResidual)<=2e-6,'candidate normalized residual');
    check(!!(g.flags&256)===(g.force===0),'force zero flag');check(!!(g.flags&1024)===wordSubnormal(g.forceWord),'force subnormal flag');
  }
  return {pass:failures.length===0,failures,normalizedResidual,appliedNominal:n,appliedInflow:U};
}
function policyClass(symbol) { if(symbol>=1&&symbol<=3)return symbol-1;if(symbol>=5&&symbol<=7)return symbol-1;if(symbol===8||symbol===9)return 7;return -1; }
function assertReferenceEncoding(s,v,b) {
  const expected=s.status===1?0x1e7:s.status===2?0x3f7:s.status===3?0x3ff:-1;
  if(s.mask!==expected||(s.flags&0xffff0000)!==0||!!(s.flags&(1<<14))!==Object.is(s.nominal,-0)||!!(s.flags&(1<<15))!==Object.is(s.inflow,-0)||s.productZero!==(s.status===3&&s.force===0))return false;
  if((s.status===1||s.status===2)&&s.termination!==1)return false;
  for(let k=0;k<10;k++)if(!(s.mask&(1<<k))&&!Object.is(v.getFloat64(b+8*k,true),0))return false;
  return true;
}
function assertHandoffEncoding(s,v,b) {
  const expected=s.status===1?0x3c:s.status===2?0x7e:s.status===3?0x7f:-1;
  if(s.mask!==expected||(s.meta&0xffff0080)!==0||s.productZero!==(s.status===3&&s.force===0))return false;
  if((s.status===1||s.status===2)&&s.termination!==1)return false;
  for(let k=0;k<7;k++)if(!(s.mask&(1<<k))&&!Object.is(v.getFloat64(b+8*k,true),0))return false;
  return true;
}
function assess(bundle,config,options={}) {
  const {prepared,R,Q,GPU,H}=bundle,N=prepared.N,rv=dataView(R.output),qv=dataView(Q.output),gv=dataView(GPU.output),hv=dataView(H.output),gp=dataView(GPU.policy);
  assertion(rv.byteLength===480*N&&qv.byteLength===480*N&&gv.byteLength===256*N&&hv.byteLength===288*N&&gp.byteLength===4*N*N,'Assessment shapes');
  assertion(R.policy.length===N*N&&Q.policy.length===N*N,'Reference policy shapes');
  const result={completed:false,pass:true,integrityPass:true,failures:[],failureCount:0,policySymbols:0,policy7NumericalStatusDifferences:0,positiveCounts:{R:0,Q:0,GPU:0},max:{rotorError:0,handoffError:0,thrustError:0,momentError:0,RQinflow:0,QGinflow:0,RGinflow:0,referenceForceWidth:0,candidateResidual:0,bodyRecomposition:0},counters:{policyPairChecks:0,rootRecordChecks:0,referenceRootChecks:0,bodyRecordChecks:0,exposureChecks:0}};
  const numericalKinds=new Set(['policy agreement','original rotor gate','raw handoff gate','original body gate']);
  function check(ok,kind,detail){if(!ok){result.pass=false;if(!numericalKinds.has(kind))result.integrityPass=false;result.failureCount++;if(result.failures.length<64)result.failures.push({kind,...detail});}}
  try{
    check(R.completed&&Q.completed&&H.completed&&prepared.completed,'path completion',{});
    for(let i=0;i<N;i++) {
      invokeGuard(options,{stage:'saved-assessment',receiver:i,counters:result.counters});charge(options,'assessmentReceivers',1);
      for(const [name,v,stride,mask,full,symbols] of [['R',rv,480,31,N,4*N],['Q',qv,480,31,N,4*N],['GPU',gv,256,31,N,4*N],['H',hv,288,4,0,0]]) {
        const b=i*stride;
        check(completeHeader(v,b,i,N,mask,full,symbols),'header',{path:name,receiver:i});
      }
      const positiveR=new Uint32Array(4),positiveQ=new Uint32Array(4),positiveG=new Uint32Array(4);
      for(let j=0;j<N;j++) {
        const index=i*N+j,rw=R.policy[index],qw=Q.policy[index],gw=gp.getUint32(index*4,true);
        if((gw&0xf0f0f0f0)!==0)check(false,'policy high nibble',{receiver:i,source:j});
        for(let r=0;r<4;r++) {const rs=(rw>>>(4*r))&15,qs=(qw>>>(4*r))&15,gs=(gw>>>(8*r))&15,rc=policyClass(rs),qc=policyClass(qs),gc=policyClass(gs);
          if(rc<0||qc<0||gc<0)check(false,'policy validity',{receiver:i,source:j,rotor:r,R:rs,Q:qs,GPU:gs});
          if(rc!==qc||rc!==gc)check(false,'policy agreement',{receiver:i,source:j,rotor:r,R:rs,Q:qs,GPU:gs});
          if(rc===7&&qc===7&&gc===7&&(rs!==qs||rs!==gs))result.policy7NumericalStatusDifferences++;
          if(rs===8)positiveR[r]++;if(qs===8)positiveQ[r]++;if(gs===8)positiveG[r]++;result.policySymbols++;
        }result.counters.policyPairChecks++;
      }
      charge(options,'assessmentPolicyPairs',N);
      const gForces=[],gNominals=[],rForces=[],qForces=[],rNominals=[],qNominals=[];
      for(let r=0;r<4;r++) {
        const rb=i*480+32+96*r,gb=i*256+32+48*r,hb=i*288+32+64*r,sR=readReferenceRoot(rv,rb),sQ=readReferenceRoot(qv,rb),g=readGpuRoot(gv,gb),h=readHandoffRoot(hv,hb,g.nominal,g.inflow);
        for(const [name,s,c,v,p,pc] of [['R',sR,config.original,rv,prepared.referencePrepared,positiveR],['Q',sQ,config.decoded,qv,prepared.decodedPrepared,positiveQ]]){
          const qc=checkReferenceRoot(s,c);result.counters.referenceRootChecks++;
          check(assertReferenceEncoding(s,v,rb)&&qc.pass,'reference root',{path:name,receiver:i,rotor:r});
          check(Object.is(s.nominal,p[28*i+24+r])&&s.positiveTerms===pc[r]&&Math.abs(s.inflow-s.compensated)<=config.gates.sumAgreement&&s.compensated>=0&&s.compensated<=c.Umax,'reference bindings/sum',{path:name,receiver:i,rotor:r});
          result.max.referenceForceWidth=Math.max(result.max.referenceForceWidth,qc.forceWidth||0);
        }
        const gcheck=checkGpuRoot(g,prepared.packed.motors[4*i+r],config.decoded);check(gcheck.pass,'GPU root',{receiver:i,rotor:r,reasons:gcheck.failures});check(g.positiveTerms===positiveG[r],'positive term count',{receiver:i,rotor:r});
        const hc=checkReferenceRoot(h,config.decoded);result.counters.referenceRootChecks++;
        check(hc.pass&&assertHandoffEncoding(h,hv,hb),'handoff reference',{receiver:i,rotor:r});
        check(exactMarginGate(g.force,sR.force,config.gates.forceMargin,config.gates.epsRotor),'original rotor gate',{receiver:i,rotor:r});
        check(exactMarginGate(g.force,h.force,config.gates.forceMargin,config.gates.handoff),'raw handoff gate',{receiver:i,rotor:r});
        result.max.rotorError=Math.max(result.max.rotorError,Math.abs(g.force-sR.force));result.max.handoffError=Math.max(result.max.handoffError,Math.abs(g.force-h.force));result.max.candidateResidual=Math.max(result.max.candidateResidual,Math.abs(gcheck.normalizedResidual||0));
        result.max.RQinflow=Math.max(result.max.RQinflow,Math.abs(sR.inflow-sQ.inflow));result.max.QGinflow=Math.max(result.max.QGinflow,Math.abs(sQ.inflow-g.inflow));result.max.RGinflow=Math.max(result.max.RGinflow,Math.abs(sR.inflow-g.inflow));
        gForces.push(g.force);gNominals.push(gcheck.appliedNominal);rForces.push(sR.force);qForces.push(sQ.force);rNominals.push(sR.nominal);qNominals.push(sQ.nominal);
        result.positiveCounts.R+=positiveR[r];result.positiveCounts.Q+=positiveQ[r];result.positiveCounts.GPU+=positiveG[r];result.counters.rootRecordChecks++;
      }
      charge(options,'assessmentRootRecords',4);charge(options,'assessmentReferenceRootChecks',12);
      const br=bodyFromForces(rForces,rNominals,config.original),bq=bodyFromForces(qForces,qNominals,config.decoded),bg=bodyFromForces(gForces,gNominals,config.decoded);
      for(let k=0;k<8;k++) {const rr=rv.getFloat64(i*480+416+8*k,true),qq=qv.getFloat64(i*480+416+8*k,true),gg=gv.getFloat32(i*256+224+4*k,true),rExpected=k<4?br.effective[k]:br.nominal[k-4],qExpected=k<4?bq.effective[k]:bq.nominal[k-4],gDiagnostic=k<4?bg.effective[k]:bg.nominal[k-4];
        check(Number.isFinite(rr)&&Number.isFinite(qq)&&Number.isFinite(gg)&&Object.is(rr,rExpected)&&Object.is(qq,qExpected),'body saved/recomposition',{receiver:i,component:k});
        result.max.bodyRecomposition=Math.max(result.max.bodyRecomposition,Math.abs(gg-gDiagnostic));
        if(k<4){const margin=k===0?config.gates.forceMargin:config.gates.momentMargin,limit=k===0?config.gates.epsT:config.gates.epsM;check(exactMarginGate(gg,rr,margin,limit),'original body gate',{receiver:i,component:k});const key=k===0?'thrustError':'momentError';result.max[key]=Math.max(result.max[key],Math.abs(gg-rr));}
      }result.counters.bodyRecordChecks++;charge(options,'assessmentBodyRecords',1);
    }
    if(bundle.designatedReceiverIds){for(const i of bundle.designatedReceiverIds){assertion(i<N,'Designated receiver ID');for(let r=0;r<4;r++){check(rv.getFloat64(i*480+32+96*r,true)>=config.gates.exposure,'material exposure',{receiver:i,rotor:r});result.counters.exposureChecks++;}}charge(options,'exposureChecks',result.counters.exposureChecks);}
    result.completed=true;return result;
  }catch(error){error.partial={kind:'assessment',buffers:{},metadata:result};throw error;}
}
function buildControls(config,options={}) {
  const pairsInput=new Uint32Array(15*64),rootsInput=new Uint32Array(146*64),pairOriginal=new Float64Array(15*16),rootOriginal=new Float64Array(146*2),pairExpected=[1,1,2,2,2,3,3,4,5,6,8,8,8,8,7];
  try {
  const D=config.original.D,offset=[.028,.028,0];
  const displacements=[null,null,null,[.4,0,0],[.4,0,-.25],[0,0,2.5],[0,0,2.75],[0,0,D],[.25,0,D],[.75,0,.6],[0,0,.6],[.02,0,2.25],[.2,0,.6],[.5,0,2.25],[0,0,.6]];
  for(let id=0;id<15;id++) {const b=id*64,rnode=[0,0,0,0,0,0,1,0],snode=[0,0,0,0,0,0,1,0];
    if(id===1)snode[0]=3;else if(id===2)snode[0]=adjacent32(3,-1);else if(id>2)for(let k=0;k<3;k++)snode[k]=offset[k]+displacements[id][k];
    if(id===14){rnode[4]=1;rnode[6]=0;}
    pairsInput.set([id,1,id===14?1:0,0,0,id===0?0:1,0,2],b);pairsInput.set(rnode.map(fbits),b+8);pairsInput.set(snode.map(fbits),b+16);pairsInput.set([...offset,0].map(fbits),b+24);
    pairOriginal.set([...rnode.slice(0,3),...rnode.slice(4,7),...snode.slice(0,3),...snode.slice(4,7),...offset,0],16*id);
  }
  const n=2**-126,d=2**-149,m=n-d/2,fmax=config.original.maxNominal;
  const nominals=[0,2**-1074,2**-151,2**-150,adjacent64(2**-150,1),d,n-d,m,adjacent64(m,-1),n,n+d,2**-32,2**-16,fmax/64,fmax/2,fmax];
  const rootDefinitions=[];
  function addRoot(id,nominal,U,label){const b=id*64;rootsInput.set([id,2,0,0,0,0,0,1],b);rootsInput[b+28]=fbits(nominal);rootsInput[b+32]=fbits(U);rootOriginal.set([nominal,U],2*id);rootDefinitions.push({id,label,nominalIndex:id<144?Math.floor(id/9):null,inflowIndex:id<144?id%9:null});}
  nominals.forEach((nominal,k)=>{const nw=fbits(nominal),dn=fvalue(nw);let vstar=1;
    if(wordNormalPositive(nw)){charge(options,'controlViConstructions',1);const twoRho=Math.fround(2*config.decoded.rho),den=Math.fround(twoRho*config.decoded.area),ratio=Math.fround(dn/den);vstar=Math.fround(Math.sqrt(ratio));}
    const U=[0,d,n,1/4,4,2**20,adjacent32(vstar,-1),vstar,adjacent32(vstar,1)];U.forEach((u,l)=>addRoot(9*k+l,nominal,u,'N'+k+'/U'+l));
  });addRoot(144,-0,1/4,'signed-negative-zero-nominal');addRoot(145,fmax/2,-0,'signed-negative-zero-inflow');
  charge(options,'controlPairConstruction',15);charge(options,'controlRootConstruction',146);
  return {completed:true,status:'constructed',pairs:{count:15,input:pairsInput,original:pairOriginal,expected:pairExpected,outputsBytes:15*256},roots:{count:146,input:rootsInput,original:rootOriginal,definitions:rootDefinitions,outputsBytes:146*256},hostOnly:{globalTilt:'P15',admissionCount:12,decoderCount:16}};
  } catch(error) {error.partial={kind:'control-construction',buffers:{pairsInput,rootsInput,pairOriginal,rootOriginal},metadata:{complete:false,message:error.message}};throw error;}
}
function controlPrepared(controls,id,path) {
  const p=new Float64Array(56),b=id*64,input=controls.pairs.input;
  if(path==='Q'){for(let k=0;k<8;k++){p[k]=fvalue(input[b+8+k]);p[28+k]=fvalue(input[b+16+k]);}for(let k=0;k<4;k++)p[8+k]=fvalue(input[b+24+k]);}
  else{const a=controls.pairs.original.subarray(16*id,16*id+16);p.set(a.subarray(0,3),0);p.set(a.subarray(3,6),4);p.set(a.subarray(6,9),28);p.set(a.subarray(9,12),32);p.set(a.subarray(12,15),8);}
  return p;
}
function runControlsReference(controls,config,options={}) {
  const result={completed:false,status:'running',pass:true,failure:null,pairs:{R:[],Q:[]},roots:{R:new ArrayBuffer(146*96),Q:new ArrayBuffer(146*96)},counters:newCounters()};
  try{
    for(const path of ['R','Q']) {const c=path==='R'?config.original:config.decoded;
      for(let id=0;id<15;id++){invokeGuard(options,{stage:'pair-control-reference',path,id});charge(options,'controlPairEvaluations',1);admitPairIdentifiers(2,0,id===0?0:1,0);const p=controlPrepared(controls,id,path),term=pairTerm(p,0,id===0?0:1,0,c,false);result.pairs[path].push({id,...term});result.counters.rotorVisits++;if(term.symbol!==controls.pairs.expected[id]){result.pass=false;result.failure={path,id,stage:'pair policy'};}}
      const v=new DataView(result.roots[path]);
      for(let id=0;id<146;id++){invokeGuard(options,{stage:'root-control-reference',path,id});const b=64*id,n=path==='R'?controls.roots.original[2*id]:fvalue(controls.roots.input[b+28]),U=path==='R'?controls.roots.original[2*id+1]:fvalue(controls.roots.input[b+32]),s=rootReference(n,U,c,result.counters,options);writeReferenceRoot(v,96*id,s,U,0);if(s.status<1||s.status>3){result.pass=false;result.failure={path,id,stage:'reference root'};}}
    }result.completed=true;result.status=result.pass?'complete':'failed';return result;
  }catch(error){result.status='failed';error.partial={kind:'control-references',buffers:{Rroots:result.roots.R,Qroots:result.roots.Q},metadata:{complete:false,status:result.status,pairs:result.pairs,counters:result.counters,failure:result.failure,message:error.message}};throw error;}
}
function runControlHandoff(gpuOutput,controls,config,options={}) {
  const gv=dataView(gpuOutput);assertion(gv.byteLength===256*146,'Root control output shape');const output=new ArrayBuffer(64*146),v=new DataView(output),counters=newCounters(),result={output,counters,completed:false,status:'running',pass:true,failure:null};
  try{for(let id=0;id<146;id++){invokeGuard(options,{stage:'root-control-handoff',id});const g=readGpuRoot(gv,id*256+32);assertion((g.mask&3)===3&&g.nominalWord===controls.roots.input[id*64+28]&&g.inflowWord===controls.roots.input[id*64+32],'Control handoff raw binding',{id});const s=rootReference(g.nominal,g.inflow,config.decoded,counters,options);writeHandoffRoot(v,id*64,s);if(s.status<1||s.status>3){result.pass=false;result.failure={id,stage:'handoff root'};}}result.completed=true;result.status=result.pass?'complete':'failed';return result;}catch(error){error.partial={kind:'control-handoff',buffers:{output},metadata:{complete:false,status:'failed',counters,failure:result.failure,message:error.message}};throw error;}
}
function completeHeader(v,b,id,N,mask,full,symbols) {
  return v.getUint32(b,true)===id&&v.getUint32(b+4,true)===N&&v.getUint32(b+8,true)===2&&v.getUint32(b+12,true)===0&&v.getUint32(b+16,true)===full&&v.getUint32(b+20,true)===symbols&&v.getUint32(b+24,true)===0xffffffff&&v.getUint32(b+28,true)===mask;
}
function termAdmitted(value){return Number.isFinite(value)&&value>=0&&value<=128;}
function sumAdmitted(value,c){return Number.isFinite(value)&&value>=0&&value<=c.Umax;}
function admitPairIdentifiers(N,i,j,r){assertion(Number.isInteger(N)&&N>=1&&Number.isInteger(i)&&i>=0&&i<N&&Number.isInteger(j)&&j>=0&&j<N&&Number.isInteger(r)&&r>=0&&r<4,'Pair identifiers');}
function runHostOnlyControls(controls,config,options={}) {
  const records=[],decoder=[],out={completed:false,status:'running',pass:true,records,decoder,counters:{admissionControls:0,decoderControls:0}};
  const expectedMessages={'P15-global-tilt':'Global tilt admission','A00-negative-original-nominal':'Original nominal','A01-above-original-maximum':'Original nominal','A02-nonfinite-quaternion':'Original finite17','A03-infinite-position':'Original finite17','A04-zero-quaternion':'Original quaternion norm','A05-position129':'Original position','A06-packed-pad':'Nonzero prepared pad','A07-state-length':'Original finite17','A08-source-index':'Pair identifiers','A09-term-limit':'Term limit','A10-sum-limit':'Sum limit','A11-unwritten-output':'Unwritten header'};
  function reject(id,fn){invokeGuard(options,{stage:'host-admission-control',id});charge(options,'hostAdmissionControls',1);let rejected=false,message=null,detail=null;try{fn();}catch(error){if(error.name!=='BodyContractError'||error.message!==expectedMessages[id])throw error;rejected=true;message=error.message;detail=error.detail||null;}records.push({id,expected:'BodyContractError: '+expectedMessages[id],rejected,message,detail});out.counters.admissionControls++;if(!rejected)out.pass=false;}
  function state(){return [0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0];}
  function rejectOriginal(id,edit){reject(id,()=>{const s=state();edit(s);prepare([s,state()],config,options);});}
  try{
    reject('P15-global-tilt',()=>preparedAdmission(controlPrepared(controls,14,'Q'),2,config.decoded));
    rejectOriginal('A00-negative-original-nominal',s=>{s[13]=-(2**-149);});
    rejectOriginal('A01-above-original-maximum',s=>{s[13]=adjacent64(config.original.maxNominal,1);});
    rejectOriginal('A02-nonfinite-quaternion',s=>{s[6]=NaN;});
    rejectOriginal('A03-infinite-position',s=>{s[0]=Infinity;});
    rejectOriginal('A04-zero-quaternion',s=>{s[9]=0;});
    rejectOriginal('A05-position129',s=>{s[0]=129;});
    reject('A06-packed-pad',()=>{const p=controlPrepared(controls,10,'Q');p[3]=1;preparedAdmission(p,2,config.decoded);});
    rejectOriginal('A07-state-length',s=>{s.pop();});
    reject('A08-source-index',()=>admitPairIdentifiers(2,0,2,0));
    reject('A09-term-limit',()=>assertion(termAdmitted(adjacent32(128,1)),'Term limit'));
    reject('A10-sum-limit',()=>assertion(sumAdmitted(adjacent32(2**20,1),config.decoded),'Sum limit'));
    reject('A11-unwritten-output',()=>assertion(completeHeader(new DataView(new ArrayBuffer(256)),0,0,2,31,2,8),'Unwritten header'));
    for(let symbol=0;symbol<16;symbol++){const actual=policyClass(symbol),expected=(symbol>=1&&symbol<=3)?symbol-1:(symbol>=5&&symbol<=7)?symbol-1:(symbol===8||symbol===9)?7:-1;decoder.push({symbol,expectedClass:expected,actualClass:actual,pass:actual===expected});if(actual!==expected)out.pass=false;out.counters.decoderControls++;}
    charge(options,'decoderControls',16);out.completed=true;out.status='complete';return out;
  }catch(error){error.partial={kind:'host-admission-controls',buffers:{},metadata:out};throw error;}
}
function assessControls(saved,config,options={}) {
  const {controls,references,GPU,H,hostOnly}=saved,pv=dataView(GPU.pairs),gv=dataView(GPU.roots),hv=dataView(H.output),rv=dataView(references.roots.R),qv=dataView(references.roots.Q);
  assertion(pv.byteLength===15*256&&gv.byteLength===146*256&&hv.byteLength===146*64,'Control assessment shapes');
  const out={completed:false,pass:true,failureCount:0,failures:[],maxRotorError:0,maxHandoffError:0,maxResidual:0,pairTermDifferences:[],counts:{pairs:0,roots:0,hostAdmission:13,decoder:16}};
  const check=(ok,kind,detail)=>{if(!ok){out.pass=false;out.failureCount++;if(out.failures.length<64)out.failures.push({kind,...detail});}};
  try{
    check(references.completed&&references.pass&&H.completed&&H.pass&&hostOnly.completed&&hostOnly.pass,'control path completion',{});
    for(let id=0;id<15;id++){invokeGuard(options,{stage:'pair-control-assessment',id});const b=id*256,symbol=pv.getUint32(b+32,true),r=references.pairs.R[id],q=references.pairs.Q[id],expected=controls.pairs.expected[id],invalid=expected===4;
      check(pv.getUint32(b,true)===id&&pv.getUint32(b+4,true)===2&&pv.getUint32(b+8,true)===(invalid?3:2)&&pv.getUint32(b+12,true)===(invalid?4:0)&&pv.getUint32(b+16,true)===0&&pv.getUint32(b+20,true)===1&&pv.getUint32(b+24,true)===(invalid?0:0xffffffff)&&pv.getUint32(b+28,true)===33,'pair header',{id});
      check(symbol===expected&&r.symbol===expected&&q.symbol===expected,'pair expected policy',{id,symbol,R:r.symbol,Q:q.symbol,expected});
      if(!invalid)check(termAdmitted(r.term)&&termAdmitted(q.term)&&(expected===8?r.term>0&&q.term>0:Object.is(r.term,0)&&Object.is(q.term,0)),'pair reference term/status',{id});
      const mask=pv.getUint32(b+56,true),expectedMask=id<=1?17:id<=6?19:id===7?22:id<=9?23:31,referenceMask=id===0?1:expectedMask;
      check(mask===expectedMask&&r.validity===referenceMask&&q.validity===referenceMask,'pair exact validity',{id});
      for(let k=0;k<5;k++){const x=pv.getFloat32(b+36+4*k,true);check(mask&(1<<k)?Number.isFinite(x):Object.is(x,0),'pair payload validity',{id,k});}
      for(let k=15;k<64;k++)check(pv.getUint32(b+4*k,true)===0,'pair output padding',{id,k});
      if((mask&1)&&!invalid){const gterm=pv.getFloat32(b+36,true);check(termAdmitted(gterm)&&(expected===8?gterm>0:Object.is(gterm,0)),'pair term admission/status',{id});out.pairTermDifferences.push({id,RG:gterm-r.term,QG:gterm-q.term});}
      out.counts.pairs++;
    }charge(options,'controlPairAssessments',15);
    for(let id=0;id<146;id++){invokeGuard(options,{stage:'root-control-assessment',id});const b=id*256,g=readGpuRoot(gv,b+32),r=readReferenceRoot(rv,id*96),q=readReferenceRoot(qv,id*96),h=readHandoffRoot(hv,id*64,g.nominal,g.inflow),gc=checkGpuRoot(g,controls.roots.input[id*64+28],config.decoded);
      check(completeHeader(gv,b,id,1,32,0,0),'root control header',{id});check(g.inflowWord===controls.roots.input[id*64+32]&&g.positiveTerms===0,'root control input binding',{id});
      check(gc.pass,'root control candidate',{id,reasons:gc.failures});
      for(const [path,s,c,v] of [['R',r,config.original,rv],['Q',q,config.decoded,qv]])check(checkReferenceRoot(s,c).pass&&assertReferenceEncoding(s,v,id*96),'root control reference',{id,path});
      check(Object.is(r.nominal,controls.roots.original[2*id])&&Object.is(r.inflow,controls.roots.original[2*id+1])&&Object.is(q.nominal,g.nominal)&&Object.is(q.inflow,g.inflow)&&Object.is(r.compensated,r.inflow)&&Object.is(q.compensated,q.inflow)&&r.positiveTerms===0&&q.positiveTerms===0,'root control reference binding',{id});
      check(checkReferenceRoot(h,config.decoded).pass&&assertHandoffEncoding(h,hv,id*64),'root control handoff reference',{id});
      check(exactMarginGate(g.force,r.force,config.gates.forceMargin,config.gates.epsRotor),'root control R gate',{id});check(exactMarginGate(g.force,h.force,config.gates.forceMargin,config.gates.handoff),'root control H gate',{id});
      for(let k=20;k<64;k++)check(gv.getUint32(b+4*k,true)===0,'root control output padding',{id,k});
      out.maxRotorError=Math.max(out.maxRotorError,Math.abs(g.force-r.force));out.maxHandoffError=Math.max(out.maxHandoffError,Math.abs(g.force-h.force));out.maxResidual=Math.max(out.maxResidual,Math.abs(gc.normalizedResidual||0));out.counts.roots++;
    }charge(options,'controlRootAssessments',146);out.completed=true;return out;
  }catch(error){error.partial={kind:'control-assessment',buffers:{},metadata:out};throw error;}
}
function workReservations() {
  return {main:{families:4,receiversPerPath:10550,pairSlotsPerPath:50252500,rotorSlotsPerPath:201010000,rootAttemptsPerReferencePath:42200,referencePaths:3,maximumBisectionIterations:12153600,maximumGpuNewtonUpdates:506400},controls:{pairsPerPath:15,pairPaths:3,rootAttemptsPerReferencePath:146,referencePaths:3,maximumBisectionIterations:42048,maximumGpuNewtonUpdates:1752,hostAdmission:13,decoder:16},assessment:{mainPolicyPairs:50252500,mainRootRecords:42200,mainReferenceRootChecks:126600,mainBodyRecords:10550,designatedExposureChecks:29700},retention:{formula:'8*N*N+2424*N',allFamiliesBytes:427593200,maxFamilyBytes:212120000,extrasCapBytes:67108864,rawCapBytes:805306368,resultCapBytes:33554432},gpu:{maxMainBuffersBytes:203120128,extrasReserveBytes:1048576,capBytes:218103808},stopping:{scienceSeconds:300,reviewSeconds:120,rssBytes:4294967296}};
}
module.exports={createConfig,constantsFor,prepare,runReference,runHandoff,assess,buildControls,runControlsReference,runControlHandoff,runHostOnlyControls,assessControls,workReservations,
  codecs:{dataView,fbits,fvalue,wordFinite,wordZero,wordSubnormal,wordNormalPositive,appliedWord,readGpuRoot,readReferenceRoot,readHandoffRoot,policyClass},
  savedChecks:{checkReferenceRoot,checkGpuRoot,completeHeader,exactMarginGate,bodyFromForces},provenance:{independentSha256:'da857f37129c6d3fc87fe223efd2b37b140fbf11417c1f1bb92331d5cfa53cec',independentCopy:'independent-frozen.source.txt',productionRotate:'outputs/step02c-source/physics.cjs:7',scope:'body-only; nominal yaw; no scientific execution on import'}};
function assessStimulus(bundle,config,options={}) {
  const {generated,prepared,R,Q}=bundle,N=prepared.N,rv=dataView(R.output),out={completed:false,pass:true,failureCount:0,failures:[],exposureChecks:0};
  const check=(ok,kind,detail)=>{if(!ok){out.pass=false;out.failureCount++;if(out.failures.length<32)out.failures.push({kind,...detail});}};
  check(prepared.completed&&R.completed&&Q.completed,'reference completion',{});
  const a=generated.audit;
  check(a&&a.nonF32Coordinates*100>=99*3*N&&a.coreDesignatedCount*3>=a.designatedCount*2,'stimulus schedule',{});
  check(generated.designatedReceiverIds&&generated.designatedReceiverIds.length===a.designatedCount,'designated identity',{});
  if(generated.designatedReceiverIds)for(const i of generated.designatedReceiverIds){invokeGuard(options,{stage:'stimulus-exposure',receiver:i});check(Number.isInteger(i)&&i>=0&&i<N,'designated index',{receiver:i});if(i>=N)continue;for(let r=0;r<4;r++){check(rv.getFloat64(i*480+32+96*r,true)>=config.gates.exposure,'material exposure',{receiver:i,rotor:r});out.exposureChecks++;}}
  charge(options,'stimulusExposureChecks',out.exposureChecks);out.completed=true;return out;
}
module.exports.assessStimulus=assessStimulus;
