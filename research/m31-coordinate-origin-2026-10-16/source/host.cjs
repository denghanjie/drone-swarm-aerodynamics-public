'use strict';
/* Static draft. Import defines functions only: no constants are evaluated,
 * prepared geometry constructed, wake calculated, file read, or GPU invoked.
 * Independent-I expression source SHA256:
 * da857f37129c6d3fc87fe223efd2b37b140fbf11417c1f1bb92331d5cfa53cec.
 * Fresh frozen coordinate-origin campaign; no roots/dynamics/pruning/normalization.
 */
const CONSTANT_NAMES = Object.freeze(['D','decay','spread','origin','minDownstream',
  'neighborRadius','nearFieldRadius','downstreamFade','downstreamCutoff','radialFade',
  'radialCutoff','tiltCosine','sourceInduced','sqrt2Minus1']);
const N=5000, K=4, M=80000, F=18, WORDS=26, NONE=0xffffffff, WITNESS_CAP=32;
const {generateFresh}=require('./generator.cjs');
function requireThat(ok,message,detail=null) { if(!ok) {const e=Error(message);e.detail=detail;throw e;} }
function chargeWork(charge,name,amount=1) { if(charge)try{charge(name,amount);}catch(error){error.integrityFailure=true;throw error;} }
function makeOriginalConstants() {
  const mass=.027, gravity=9.81, armCoordinate=.028, rho=1.225, rotorRadius=.023;
  const area=Math.PI*rotorRadius*rotorRadius;
  const sourceInduced=Math.sqrt(mass*gravity/(8*rho*area));
  const f0=.027*9.81/4;
  return {D:2*Math.sqrt(2)*armCoordinate,decay:10.11,spread:.07668,origin:-5.817,
    minDownstream:2.5,neighborRadius:3,nearFieldRadius:.15,downstreamFade:2,
    downstreamCutoff:2.5,radialFade:2,radialCutoff:3,
    tiltCosine:Math.cos(20*Math.PI/180),sourceInduced,sqrt2Minus1:Math.sqrt(2)-1,
    f0,area,epsilonWake:3*sourceInduced*1e-7/f0,referenceSumAllowance:1e-12};
}
function rotate(q,v) {
  const [x,y,z,w]=q, [vx,vy,vz]=v;
  return [
    (1-2*(y*y+z*z))*vx + 2*(x*y-z*w)*vy + 2*(x*z+y*w)*vz,
    2*(x*y+z*w)*vx + (1-2*(x*x+z*z))*vy + 2*(y*z-x*w)*vz,
    2*(x*z-y*w)*vx + 2*(y*z+x*w)*vy + (1-2*(x*x+y*y))*vz
  ];
}
function fade(start,end,value) {
  if(value<=start)return 1;
  if(value>=end)return 0;
  const t=(value-start)/(end-start);
  return (1-t)*(1-t)*(1+2*t);
}
function constantsArray(C) {
  const a=new Float64Array(16);
  CONSTANT_NAMES.forEach((key,i)=>{requireThat(Number.isFinite(C[key]),'Invalid constant '+key);a[i]=C[key];});
  return a;
}
function checkedIDs(ids) {
  requireThat(ids&&ids.length===4,'Exactly four receiver IDs required');
  const a=Array.from(ids);
  requireThat(a.every(x=>Number.isInteger(x)&&x>=0&&x<N)&&new Set(a).size===4,'Four distinct receiver IDs in range required');
  return Uint32Array.from(a);
}
function preparedMetrics(P,C,label,charge) {
  const metrics=new Float64Array(N*3);
  for(let i=0;i<N;i++) {
    chargeWork(charge,label+'AxisMetrics');
    const b=i*8,axis=[P.nodes[b+3],P.nodes[b+4],P.nodes[b+5]];
    const norm=Math.hypot(...axis),margin=axis[2]-C.tiltCosine;
    requireThat(Number.isFinite(norm)&&Number.isFinite(margin)&&margin>=0,'Global prepared tilt/domain admission',{label,node:i,norm,margin});
    metrics[3*i]=norm;metrics[3*i+1]=norm-1;metrics[3*i+2]=margin;
  }
  return metrics;
}
function prepareOriginal(states,ids,C,charge) {
  requireThat(Array.isArray(states)&&states.length===N,'Exactly 5000 original states required');
  const P={nodes:new Float64Array(N*8),offsets:new Float64Array(16*4),ids:checkedIDs(ids),constants:constantsArray(C),axisMetrics:null};
  for(let i=0;i<N;i++) {
    chargeWork(charge,'originalStateAdmissions');
    const s=states[i];requireThat(s&&s.length===17&&Array.from(s).every(Number.isFinite),'Original finite 17-state admission',{node:i});
    requireThat(s.slice(0,3).every(x=>Math.abs(x)<=128),'Original position bound',{node:i});
    chargeWork(charge,'originalQuaternionNorms');
    const q=s.slice(6,10),norm=Math.hypot(...q);
    requireThat(Math.abs(norm-1)<=1e-10,'Original quaternion norm admission',{node:i,norm});
  }
  for(let i=0;i<N;i++) {
    chargeWork(charge,'originalAxisRotations');
    const s=states[i],axis=rotate(s.slice(6,10),[0,0,1]);
    requireThat(axis.every(x=>Number.isFinite(x)&&Math.abs(x)<=1.01),'Original axis bound',{node:i});
    P.nodes.set(s.slice(0,3),8*i);P.nodes.set(axis,8*i+3);
  }
  P.axisMetrics=preparedMetrics(P,C,'R',charge);
  const a=.028,arms=[[a,a,0],[-a,a,0],[-a,-a,0],[a,-a,0]];
  for(let i=0;i<K;i++)for(let r=0;r<4;r++) {
    chargeWork(charge,'originalOffsetRotations');
    const offset=rotate(states[P.ids[i]].slice(6,10),arms[r]);
    requireThat(offset.every(x=>Number.isFinite(x)&&Math.abs(x)<=.1),'Original offset bound',{selectedIndex:i,rotor:r});
    P.offsets.set(offset,4*(4*i+r));
  }
  return P;
}
function translatePrepared(P,states,C,charge) {
  requireThat(Array.isArray(states)&&states.length===N,'Exactly 5000 translated states');
  chargeWork(charge,'translatedPreparedFloatCopies',55080);chargeWork(charge,'translatedPreparedIdCopies',4);
  const T={nodes:P.nodes.slice(),offsets:P.offsets.slice(),ids:P.ids.slice(),constants:P.constants.slice(),axisMetrics:P.axisMetrics.slice()};
  for(let i=0;i<N;i++) {
    chargeWork(charge,'translatedStateAdmissions');const s=states[i];
    requireThat(s&&s.length===17&&Array.from(s).every(Number.isFinite)&&s.slice(0,3).every(x=>Math.abs(x)<=128),'Translated state admission',{node:i});
    for(let f=0;f<3;f++){chargeWork(charge,'translatedPositionWrites');T.nodes[8*i+f]=s[f];}
  }
  return T;
}
function packPrepared(P,C,charge) {
  const packedAB={nodes:new Uint32Array(N*8),offsets:new Uint32Array(64),ids:checkedIDs(P.ids),constants:new Uint32Array(16)};
  const Q0={nodes:new Float64Array(N*8),offsets:new Float64Array(64),ids:checkedIDs(P.ids),constants:new Float64Array(16),axisMetrics:null};
  const view=new DataView(new ArrayBuffer(4));
  for(const [key,input]of [['nodes',P.nodes],['offsets',P.offsets],['constants',constantsArray(C)]]) {
    for(let i=0;i<input.length;i++) {
      chargeWork(charge,'packedFloatWords');view.setFloat32(0,input[i],true);packedAB[key][i]=view.getUint32(0,true);Q0[key][i]=view.getFloat32(0,true);
      requireThat(Number.isFinite(Q0[key][i]),'Packed finite admission',{field:key,index:i});
    }
  }
  for(let i=0;i<N;i++) {
    chargeWork(charge,'decodedNodeAdmissions');const b=8*i;
    requireThat(Array.from(Q0.nodes.slice(b,b+3)).every(x=>Math.abs(x)<=128)&&Array.from(Q0.nodes.slice(b+3,b+6)).every(x=>Math.abs(x)<=1.01)&&Q0.nodes[b+6]===0&&Q0.nodes[b+7]===0,'Decoded node bound',{node:i});
  }
  for(let i=0;i<16;i++) {
    chargeWork(charge,'decodedOffsetAdmissions');const b=4*i;
    requireThat(Array.from(Q0.offsets.slice(b,b+3)).every(x=>Math.abs(x)<=.1)&&Q0.offsets[b+3]===0,'Decoded offset bound',{offset:i});
  }
  const QC={};CONSTANT_NAMES.forEach((key,i)=>{QC[key]=Q0.constants[i];});
  for(const key of ['f0','area','epsilonWake','referenceSumAllowance'])QC[key]=C[key];
  Q0.axisMetrics=preparedMetrics(Q0,QC,'Q0',charge);
  chargeWork(charge,'Q1PreparedFloatCopies',55080);chargeWork(charge,'Q1PreparedIdCopies',4);
  const Q1={nodes:Q0.nodes.slice(),offsets:Q0.offsets.slice(),ids:Q0.ids.slice(),constants:Q0.constants.slice(),axisMetrics:Q0.axisMetrics.slice()};
  const packedC={nodes:new Uint32Array(N*12),offsets:packedAB.offsets,ids:packedAB.ids,constants:packedAB.constants};
  const reconstructionResiduals=new Float64Array(15000),positionPackingResiduals=new Float64Array(15000);
  let exactReconstructionCount=0,ordinaryPackingNonzeroCount=0,maxAbsLow=0,maxAbsPackingResidual=0;
  for(let i=0;i<N;i++) {
    for(let f=0;f<8;f++){chargeWork(charge,'splitBaseWordCopies');packedC.nodes[12*i+f]=packedAB.nodes[8*i+f];}
    for(let f=0;f<3;f++) {
      chargeWork(charge,'splitLowFloatWords');const k=3*i+f,original=P.nodes[8*i+f],hi=Q0.nodes[8*i+f];
      view.setFloat32(0,original-hi,true);const lo=view.getFloat32(0,true);packedC.nodes[12*i+8+f]=view.getUint32(0,true);
      requireThat(Number.isFinite(lo)&&Math.abs(lo)<=2**-17,'Split residual bound',{node:i,axis:f});
      const reconstructed=hi+lo;Q1.nodes[8*i+f]=reconstructed;
      chargeWork(charge,'splitCoordinateCertificates');
      const exactResidual=units64(hi)+units64(lo)-units64(original);
      reconstructionResiduals[k]=reconstructed-original;positionPackingResiduals[k]=hi-original;
      requireThat(exactResidual===0n&&units64(reconstructed)===units64(original)&&reconstructionResiduals[k]===0,'Exact split reconstruction',{node:i,axis:f});
      exactReconstructionCount++;if(positionPackingResiduals[k]!==0)ordinaryPackingNonzeroCount++;
      maxAbsLow=Math.max(maxAbsLow,Math.abs(lo));maxAbsPackingResidual=Math.max(maxAbsPackingResidual,Math.abs(positionPackingResiduals[k]));
    }
  }
  for(let i=0;i<N;i++)for(let f=0;f<8;f++){chargeWork(charge,'splitBaseWordComparisons');requireThat(packedC.nodes[12*i+f]===packedAB.nodes[8*i+f],'Split first eight words identity');}
  for(const key of ['nodes','offsets','constants','axisMetrics','ids'])for(let i=0;i<Q0[key].length;i++){
    if(key==='nodes'&&i%8<3)continue;chargeWork(charge,'QInterfaceNonpositionComparisons');requireThat(Object.is(Q0[key][i],Q1[key][i]),'Nonposition Q interface exact identity',{key,index:i});
  }
  return {Q0,Q1,constants:QC,packedAB,packedC,reconstructionResiduals,positionPackingResiduals,audit:{exactReconstructionCount,ordinaryPackingNonzeroCount,maxAbsLow,maxAbsPackingResidual,lowBound:2**-17,sharedAxesOffsetsConstants:true,splitSemantic:'binary64(hi + lo); exact dyadic equality to original positions required'}};
}
function evaluateSelected(P,C,label,charge) {
  requireThat(label==='R'||label==='Q0'||label==='Q1','Reference label must be R, Q0, or Q1');
  const result={label,metadata:new Uint32Array(M*8),scalars:new Float64Array(M*F),codes:new Uint8Array(M),terms:new Float64Array(M),ordinarySums:new Float64Array(16),compensatedSums:new Float64Array(16),sumValidity:new Uint8Array(16),complete:false,failure:null,counts:{reservedPairSlots:M,initializedSlots:0,validSlots:0,centerChecks:0,rotorVisits:0,profileEvaluations:0,positiveTerms:0,eligibleSources:0,worldPoints:0,codeCounts:Array(8).fill(0),statusCounts:Array(7).fill(0)}};
  const {metadata:meta,scalars:x,terms,codes,counts}=result;codes.fill(255);
  const context={selectedIndex:null,receiverID:null,sourceID:null,rotor:null,ordinal:null,stage:'initialize'};
  function numericalRequire(ok,message,detail){if(!ok){const error=Error(message);error.detail=detail;error.referenceNumericalFailure=true;throw error;}}
  function finite(v,name) {numericalRequire(Number.isFinite(v),'Non-finite reference '+name,{...context,value:String(v)});return v;}
  function set(n,f,value) {x[n*F+f]=finite(value,'field '+f);meta[n*8+6]|=1<<f;return value;}
  function done(n,code,status,term=0) {
    meta[n*8+4]=status;meta[n*8+5]=code;codes[n]=code;counts.codeCounts[code]++;counts.statusCounts[status]++;
    if(status===3||status===4||status===5){set(n,11,term);terms[n]=term;counts.validSlots++;}
  }
  try {
    chargeWork(charge,label+'PairSlots',M);
    for(let i=0;i<K;i++)for(let j=0;j<N;j++)for(let r=0;r<4;r++) {
      const n=((i*N+j)*4+r),b=n*8;meta[b]=n;meta[b+1]=P.ids[i];meta[b+2]=j;meta[b+3]=r;meta[b+5]=NONE;counts.initializedSlots++;
    }
    for(let i=0;i<K;i++) {
      const receiver=P.ids[i],ib=8*receiver,eligible=[];
      Object.assign(context,{selectedIndex:i,receiverID:receiver,sourceID:null,rotor:null,ordinal:null,stage:'centers'});
      for(let j=0;j<N;j++) {
        if(j===receiver){for(let r=0;r<4;r++){const n=(i*N+j)*4+r;meta[n*8+7]=1;done(n,0,3);}continue;}
        context.sourceID=j;chargeWork(charge,label+'CenterChecks');counts.centerChecks++;
        const jb=8*j,centerDelta=[P.nodes[jb]-P.nodes[ib],P.nodes[jb+1]-P.nodes[ib+1],P.nodes[jb+2]-P.nodes[ib+2]],center=finite(Math.hypot(...centerDelta),'center norm');
        const admitted=center<C.neighborRadius;
        for(let r=0;r<4;r++){const n=(i*N+j)*4+r;set(n,0,center);for(let f=0;f<3;f++)set(n,12+f,centerDelta[f]);if(!admitted){meta[n*8+7]=2;done(n,0,3);}}
        if(admitted){eligible.push(j);counts.eligibleSources++;}
      }
      for(let r=0;r<4;r++) {
        chargeWork(charge,label+'WorldPoints');counts.worldPoints++;
        const ob=(i*4+r)*4,point=[P.nodes[ib]+P.offsets[ob],P.nodes[ib+1]+P.offsets[ob+1],P.nodes[ib+2]+P.offsets[ob+2]];
        let total=0,correction=0;
        for(const j of eligible) {
          const n=(i*N+j)*4+r,jb=j*8;
          Object.assign(context,{sourceID:j,rotor:r,ordinal:n,stage:'pair'});
          chargeWork(charge,label+'RotorVisits');counts.rotorVisits++;
          const dx=P.nodes[jb]-point[0],dy=P.nodes[jb+1]-point[1],dz=P.nodes[jb+2]-point[2],ax=P.nodes[jb+3],ay=P.nodes[jb+4],az=P.nodes[jb+5];
          set(n,15,dx);set(n,16,dy);set(n,17,dz);
          const down=set(n,1,dx*ax + dy*ay + dz*az);
          if(down<=0){done(n,1,3);continue;}
          if(down>=C.downstreamCutoff){done(n,2,3);continue;}
          const radial=set(n,2,Math.hypot(dx-down*ax,dy-down*ay,dz-down*az));
          if(down<C.minDownstream*C.D) {
            if(radial<C.nearFieldRadius){done(n,3,2);throw Object.assign(Error('Receiver enters unmodeled near wake'),{detail:{...context,down,radial},referenceNumericalFailure:true});}
            done(n,4,3);continue;
          }
          const normalizedDown=set(n,6,down/C.D);
          const halfWidth=set(n,3,C.spread*(normalizedDown-C.origin)*C.D);
          if(radial>=C.radialCutoff*halfWidth){done(n,5,3);continue;}
          const axisDot=set(n,4,P.nodes[ib+3]*ax + P.nodes[ib+4]*ay + P.nodes[ib+5]*az);
          const projection=set(n,5,Math.max(0,axisDot));
          const code=projection<=0?6:7;meta[n*8+5]=code;
          chargeWork(charge,label+'ProfileEvaluations');counts.profileEvaluations++;
          const xi=set(n,7,(radial/C.D)/(C.spread*(normalizedDown-C.origin)));
          const denominator=1+C.sqrt2Minus1*xi*xi;
          const normalizedSpeed=set(n,8,(C.decay/(normalizedDown-C.origin))/(denominator*denominator));
          const fadeDown=set(n,9,fade(C.downstreamFade,C.downstreamCutoff,down));
          const radialRatio=radial/halfWidth;
          const fadeRadial=set(n,10,fade(C.radialFade,C.radialCutoff,radialRatio));
          if(down>C.downstreamFade)meta[n*8+7]|=4;
          if(radialRatio>C.radialFade)meta[n*8+7]|=8;
          const speed=finite(normalizedSpeed*C.sourceInduced*fadeDown*fadeRadial*projection,'term');
          numericalRequire(speed>=0,'Negative reference term',{...context,speed});
          done(n,code,speed===0?4:5,speed);if(speed>0)counts.positiveTerms++;
          chargeWork(charge,label+'SumTermVisits');
          const next=total+speed;
          correction+=Math.abs(total)>=Math.abs(speed)?(total-next)+speed:(speed-next)+total;
          total=next;
          finite(total,'ordinary sum');finite(correction,'Neumaier correction');
          result.ordinarySums[i*4+r]=total;result.compensatedSums[i*4+r]=total+correction;
        }
        result.ordinarySums[i*4+r]=total;result.compensatedSums[i*4+r]=finite(total+correction,'compensated sum');result.sumValidity[i*4+r]=1;
      }
    }
    result.complete=true;
  } catch(error) {
    const n=context.ordinal;
    if(n!==null&&meta[n*8+4]===0){meta[n*8+4]=6;meta[n*8+6]&=~2048;x[n*F+11]=0;terms[n]=0;counts.statusCounts[6]++;}
    result.failure={errorClass:error.referenceNumericalFailure&&!error.integrityFailure?'numerical':'integrity',message:error.message,detail:error.detail??null,context:{...context}};
  }
  return result;
}
function encodeU32(a) {const b=Buffer.alloc(a.length*4);for(let i=0;i<a.length;i++)b.writeUInt32LE(a[i],i*4);return b;}
function encodeI32(a) {const b=Buffer.alloc(a.length*4);for(let i=0;i<a.length;i++)b.writeInt32LE(a[i],i*4);return b;}
function encodeF64(a) {const b=Buffer.alloc(a.length*8);for(let i=0;i<a.length;i++)b.writeDoubleLE(a[i],i*8);return b;}
function decodeF64(b) {requireThat(Buffer.isBuffer(b)&&b.length%8===0,'f64 byte shape');const a=new Float64Array(b.length/8);for(let i=0;i<a.length;i++)a[i]=b.readDoubleLE(i*8);return a;}
function decodeU32(b) {requireThat(Buffer.isBuffer(b)&&b.length%4===0,'u32 byte shape');const a=new Uint32Array(b.length/4);for(let i=0;i<a.length;i++)a[i]=b.readUInt32LE(i*4);return a;}
function absBig(x){return x<0n?-x:x;}
function units64(value) {
  requireThat(Number.isFinite(value),'Finite binary64 dyadic required');
  const b=Buffer.alloc(8);b.writeDoubleLE(value);const word=b.readBigUInt64LE();
  const exponent=Number((word>>52n)&2047n),fraction=word&((1n<<52n)-1n);
  const magnitude=exponent===0?fraction:((1n<<52n)|fraction)<<BigInt(exponent-1);
  return (word>>63n)!==0n?-magnitude:magnitude;
}
function units32(word) {
  const exponent=(word>>>23)&255,fraction=word&0x7fffff;
  requireThat(exponent!==255,'Finite binary32 dyadic required');
  const magnitude=exponent===0?BigInt(fraction):((1n<<23n)|BigInt(fraction))<<BigInt(exponent-1);
  return (word>>>31)!==0?-magnitude:magnitude;
}
function displayDyadic(coefficient,exponent) {
  if(coefficient===0n)return 0;
  const negative=coefficient<0n,magnitude=absBig(coefficient),length=magnitude.toString(2).length,shift=Math.max(0,length-53);
  const display=Number(magnitude>>BigInt(shift))*2**(exponent+shift);
  return negative?-display:display;
}
function certificate(value,exponent=-1074){return {coefficient:value.toString(),exponent,approximateDisplay:displayDyadic(value,exponent)};}
function witness(report,issue,detail,errorClass='integrity') {report.errorCount++;report.errorClassCounts[errorClass]++;report[errorClass+'Pass']=false;if(report.witnesses.length<WITNESS_CAP)report.witnesses.push({issue,errorClass,...detail});}
function reportBase(kind){return {kind,pass:false,integrityPass:true,numericalPass:true,errorCount:0,errorClassCounts:{integrity:0,numerical:0},witnesses:[],witnessCap:WITNESS_CAP,counts:{}};}
function finish(report){report.pass=report.integrityPass&&report.numericalPass;return report;}
function referenceShape(R) {return R&&typeof R.complete==='boolean'&&R.metadata instanceof Uint32Array&&R.metadata.length===M*8&&R.scalars instanceof Float64Array&&R.scalars.length===M*F&&R.codes instanceof Uint8Array&&R.codes.length===M&&R.terms instanceof Float64Array&&R.terms.length===M&&R.ordinarySums instanceof Float64Array&&R.ordinarySums.length===16&&R.compensatedSums instanceof Float64Array&&R.compensatedSums.length===16&&R.sumValidity instanceof Uint8Array&&R.sumValidity.length===16;}
function referenceSumDiagnostics(R,C,report) {
  const rows=[];
  for(let i=0;i<16;i++) {
    const a=R.ordinarySums[i],b=R.compensatedSums[i],valid=R.sumValidity[i]===1&&Number.isFinite(a)&&Number.isFinite(b),difference=valid?Math.abs(a-b):null;
    if(!valid)witness(report,'Completed reference sum metadata/nonfinite corruption',{label:R.label,index:i,valid});
    else if(difference>C.referenceSumAllowance)witness(report,'Reference ordinary/Neumaier sum gate',{label:R.label,index:i,valid,difference},'numerical');
    rows.push({index:i,ordinary:Number.isFinite(a)?a:null,compensated:Number.isFinite(b)?b:null,valid,absoluteDifference:difference});
  }
  return rows;
}
function validateReferenceRow(R,n,out) {
  const before=out.errorClassCounts.integrity,b=n*8,receiverID=[749,500,2250,4750][Math.floor(n/20000)],sourceID=Math.floor(n/4)%N,rotor=n%4,self=receiverID===sourceID,expected=[n,receiverID,sourceID,rotor];
  out.counts.referenceRowsChecked++;
  for(let f=0;f<4;f++)if(R.metadata[b+f]!==expected[f])witness(out,'Reference identity mismatch',{ordinal:n,field:f,expected:expected[f],actual:R.metadata[b+f]});
  const status=R.metadata[b+4],code=R.codes[n],mask=R.metadata[b+6],flags=R.metadata[b+7],term=R.terms[n],scalarTerm=R.scalars[n*F+11];
  if(R.metadata[b+5]!==code||code>7||code===3||self&&code!==0||mask!==expectedMask(code,self))witness(out,'Reference policy/mask malformed',{ordinal:n,status,code,mask});
  const route=self?1:(code===0?2:0);
  if((flags&~15)!==0||(flags&3)!==route||code<6&&(flags&12)!==0)witness(out,'Reference routing malformed',{ordinal:n,flags});
  if(![3,4,5].includes(status)||!Number.isFinite(term)||term<0||!Object.is(term,scalarTerm))witness(out,'Reference status/term malformed',{ordinal:n,status});
  if(code<=5&&(status!==3||term!==0))witness(out,'Reference early zero malformed',{ordinal:n,status,code});
  const projection=R.scalars[n*F+5];
  if(code===6&&(status!==4||term!==0||projection!==0))witness(out,'Reference zero projection malformed',{ordinal:n,status});
  if(code===7&&(!(projection>0)||!(status===4&&term===0||status===5&&term>0)))witness(out,'Reference profile sign malformed',{ordinal:n,status});
  const upper=[512,1024,2048,8,4,4,64,128,3,1.0010000467300415,1.0010000467300415,128,257,257,257,258,258,258];
  for(let f=0;f<F;f++) {
    out.counts.referenceNumericFieldsChecked++;const value=R.scalars[n*F+f],valid=(mask&(1<<f))!==0;
    if(!valid){if(!Object.is(value,0))witness(out,'Reference unreached field must be +0',{ordinal:n,field:f});continue;}
    if(!Number.isFinite(value)||Math.abs(value)>upper[f]||f<12&&f!==1&&f!==4&&value<0||(f===3||f===6)&&value<=0)witness(out,'Reference reached field invalid',{ordinal:n,field:f});
  }
  return out.errorClassCounts.integrity===before;
}
function assessR(R,C) {
  const out=reportBase('original-R-internal-qualification');out.counts={referenceRowsChecked:0,referenceNumericFieldsChecked:0,referenceSumComparisons:0,RExactStoredTermAdds:0,RExactStoredSumGates:0};
  if(!referenceShape(R)){witness(out,'Reference shape mismatch',{});return finish(out);}
  if(!R.complete){witness(out,'Reference incomplete',{failure:R.failure},R.failure?.errorClass==='numerical'?'numerical':'integrity');return finish(out);}
  const sums=Array(16).fill(0n),allowance=units64(C.referenceSumAllowance);
  for(let n=0;n<M;n++) {
    if(!validateReferenceRow(R,n,out))continue;const term=R.terms[n];
    sums[Math.floor(n/20000)*4+n%4]+=units64(term);out.counts.RExactStoredTermAdds++;
  }
  out.sums=referenceSumDiagnostics(R,C,out);out.counts.referenceSumComparisons=16;out.referenceSumAllowance=certificate(allowance);out.rotors=[];
  for(let i=0;i<16;i++) {
    if(!Number.isFinite(R.ordinarySums[i])||!Number.isFinite(R.compensatedSums[i]))continue;
    const ordinary=units64(R.ordinarySums[i])-sums[i],compensated=units64(R.compensatedSums[i])-sums[i],pass=absBig(ordinary)<=allowance&&absBig(compensated)<=allowance;out.counts.RExactStoredSumGates+=2;
    if(!pass)witness(out,'Exact R stored sum allowance gate',{index:i},'numerical');
    out.rotors.push({index:i,exactStoredTermSum:certificate(sums[i]),signedOrdinaryMinusStored:certificate(ordinary),signedCompensatedMinusStored:certificate(compensated),pass});
  }
  return finish(out);
}
function assessQ(R,Q,C) {
  const out=reportBase('decoded-packed-Q-vs-original-R');out.counts={referenceRowsChecked:0,referenceNumericFieldsChecked:0,packedCodeComparisons:0,packingDyadicTermRows:0,referenceSumComparisons:0,packingExactStoredTermAdds:0,QExactStoredSumGates:0};
  if(!referenceShape(R)||!referenceShape(Q)){witness(out,'Reference shape mismatch',{});return finish(out);}
  if(!R.complete){witness(out,'Shared original reference incomplete',{failure:R.failure});return finish(out);}
  if(!Q.complete){witness(out,'Packed reference incomplete',{failure:Q.failure},Q.failure?.errorClass==='numerical'?'numerical':'integrity');return finish(out);}
  const l1=Array(16).fill(0n),signed=Array(16).fill(0n),sumR=Array(16).fill(0n),sumQ=Array(16).fill(0n),allowance=units64(C.referenceSumAllowance),epsilon=units64(C.epsilonWake);
  out.threshold={epsilon:certificate(epsilon),referenceSumAllowance:certificate(allowance)};
  for(let n=0;n<M;n++) {
    const rowValid=validateReferenceRow(Q,n,out);
    out.counts.packedCodeComparisons++;if(R.codes[n]!==Q.codes[n])witness(out,'Packed policy code mismatch',{ordinal:n,R:R.codes[n],Q:Q.codes[n]},'numerical');
    if(!Number.isFinite(R.terms[n])||!Number.isFinite(Q.terms[n])||R.terms[n]<0||Q.terms[n]<0){witness(out,'Invalid reference term',{ordinal:n});continue;}
    if(!rowValid)continue;
    out.counts.packingDyadicTermRows++;const i=Math.floor(n/20000)*4+n%4,q=units64(Q.terms[n]),r=units64(R.terms[n]),difference=q-r;l1[i]+=absBig(difference);signed[i]+=difference;sumQ[i]+=q;sumR[i]+=r;out.counts.packingExactStoredTermAdds+=2;
  }
  out.RSums=referenceSumDiagnostics(R,C,out);out.QSums=referenceSumDiagnostics(Q,C,out);out.counts.referenceSumComparisons=32;
  out.rotors=l1.map((value,i)=>{
    if(!Number.isFinite(Q.ordinarySums[i])||!Number.isFinite(Q.compensatedSums[i]))return {index:i,pass:false};
    const total=value+allowance,ordinaryGap=units64(Q.ordinarySums[i])-sumQ[i],compensatedGap=units64(Q.compensatedSums[i])-sumQ[i];out.counts.QExactStoredSumGates+=2;
    const sumPass=absBig(ordinaryGap)<=allowance&&absBig(compensatedGap)<=allowance,pass=total<=epsilon&&sumPass;
    if(total>epsilon)witness(out,'Exact packing L1 gate',{index:i},'numerical');if(!sumPass)witness(out,'Exact Q stored sum allowance gate',{index:i},'numerical');
    return {index:i,l1QR:certificate(value),signedQR:certificate(signed[i]),exactStoredSumR:certificate(sumR[i]),exactStoredSumQ:certificate(sumQ[i]),signedOrdinaryQMinusStored:certificate(ordinaryGap),signedCompensatedQMinusStored:certificate(compensatedGap),l1PlusAllowance:certificate(total),sumPass,pass};
  });
  return finish(out);
}
function value32(word) {const b=Buffer.alloc(4);b.writeUInt32LE(word);return b.readFloatLE();}
function expectedMask(code,self) {if(code===0)return self?2048:30721;if(code===1||code===2)return 260099;if(code===3)return 258055;if(code===4)return 260103;if(code===5)return 260175;if(code===6||code===7)return 262143;return -1;}
function validateNumerics(words,base,out,identity) {
  const mask=words[base+6],values=[];
  if((mask&~262143)!==0)witness(out,'Unknown validity bit',identity);
  for(let f=0;f<F;f++) {
    out.counts.numericFieldsChecked=(out.counts.numericFieldsChecked??0)+1;
    const w=words[base+8+f],valid=(mask&(1<<f))!==0;
    if(!valid){if(w!==0)witness(out,'Unreached numeric payload must be raw +0',{...identity,field:f,word:w});values.push(null);continue;}
    if((w&0x7f800000)===0x7f800000){witness(out,'Reached numeric field non-finite',{...identity,field:f,word:w});values.push(null);continue;}
    const value=value32(w);values.push(value);
    if(f<12&&f!==1&&f!==4&&value<0)witness(out,'Reached numeric field negative',{...identity,field:f,value});
    if((f===9||f===10)&&value>1.0010000467300415)witness(out,'Fade exceeds shader arithmetic bound',{...identity,field:f,value});
    if(f===3&&value<=0)witness(out,'Nonpositive reached half-width',{...identity,value});
    if(f===6&&value<=0)witness(out,'Nonpositive reached normalized downstream',{...identity,value});
    const upper=[512,1024,2048,8,4,4,64,128,3,1.0010000467300415,1.0010000467300415,128,257,257,257,258,258,258][f];
    if(Math.abs(value)>upper)witness(out,'Reached numeric field exceeds shader bound',{...identity,field:f,value,upper});
  }
  return values;
}
function assessControls(bytes,spec,arm) {
  const out=reportBase('saved-GPU-controls');out.counts={controlRecordsChecked:0,numericFieldsChecked:0,controlLiteralWordComparisons:0};
  if(!Buffer.isBuffer(bytes)||bytes.length!==2080||spec?.controls?.length!==20||!['A','B','C'].includes(arm)){witness(out,'Control shape/arm mismatch',{});return finish(out);}
  const words=decodeU32(bytes),fields=['ordinal','receiverID','sourceID','rotor','status','policyCode','validityMask','routingFlags'];
  for(let i=0;i<20;i++) {
    out.counts.controlRecordsChecked++;const b=WORDS*i,c=spec.controls[i],expected=c.expectedByArm?.[arm]??c.expected;
    if(!expected){witness(out,'Missing arm control expectation',{control:i,arm});continue;}
    fields.forEach((key,j)=>{if(words[b+j]!==expected[key])witness(out,'Control '+key,{control:i,expected:expected[key],actual:words[b+j]});});
    const values=validateNumerics(words,b,out,{control:i}),term=values[11],word=words[b+19],valid=(words[b+6]&2048)!==0,assertion=expected.termAssertion;
    if(assertion==='zero-valid'){if(!valid||term!==0)witness(out,'Control expected valid zero',{control:i});}
    else if(assertion==='finite-strictly-positive'){if(!valid||!(term>0))witness(out,'Control expected positive term',{control:i});}
    else if(assertion==='zero-placeholder-not-valid'){if(valid||word!==0)witness(out,'Control expected invalid zero placeholder',{control:i});}
    else witness(out,'Unknown control term assertion',{control:i,assertion});
    for(const [key,value]of Object.entries(expected.expectedNumericWords??c.expectedNumericWords??{})) {
      out.counts.controlLiteralWordComparisons++;const f=Number(key);
      if(!Number.isInteger(f)||f<8||f>=WORDS||words[b+f]!==value)witness(out,'Control exact numeric word',{control:i,wordIndex:f,expected:value,actual:words[b+f]});
    }
  }
  return finish(out);
}
function arithmeticPrefixValid(mask,code,flags,self) {
  if(self||(mask&2048)!==0||(flags&~12)!==0)return false;
  if([0,28672,28673,258049,258051,258055].includes(mask))return code===NONE&&flags===0;
  if(mask===258127)return (code===NONE||code===6||code===7)&&flags===0;
  if(mask===258303)return (code===6||code===7)&&flags===0;
  return mask===260095&&(code===6||code===7);
}
function assessGpuTerms(R,Q,bytes,C,ids) {
  const out=reportBase('saved-GPU-term-attribution');out.counts={gpuTermRecordsChecked:0,numericFieldsChecked:0,gpuDyadicTermRows:0,gpuExactStoredTermAdds:0,gpuStageComparisons:0};
  if(!referenceShape(R)||!referenceShape(Q)||!R.complete||!Q.complete||!Buffer.isBuffer(bytes)||bytes.length!==M*104||ids?.length!==4){witness(out,'Term/reference shape or incomplete',{});return finish(out);}
  const words=decodeU32(bytes),l1TR=Array(16).fill(0n),l1TQ=Array(16).fill(0n),l1QR=Array(16).fill(0n),signedTR=Array(16).fill(0n),signedTQ=Array(16).fill(0n),signedQR=Array(16).fill(0n),sumT32=Array(16).fill(0n);
  const epsilon=units64(C.epsilonWake),allowance=units64(C.referenceSumAllowance),codeCounts=Array(8).fill(0),statusCounts=Array(7).fill(0),positivePerRotor=Array(16).fill(0),qualifiedPerRotor=Array(16).fill(0);
  out.threshold={epsilon:certificate(epsilon),referenceSumAllowance:certificate(allowance)};out.stageMaxAbsTQ=Array(F).fill(null);out.stageMaxAbsTQWitness=Array(F).fill(null);
  for(let n=0;n<M;n++) {
    out.counts.gpuTermRecordsChecked++;const before=out.errorClassCounts.integrity,b=n*WORDS,selectedIndex=Math.floor(n/20000),sourceID=Math.floor(n/4)%N,rotor=n%4,index=4*selectedIndex+rotor,receiverID=ids[selectedIndex],self=sourceID===receiverID,identity={ordinal:n,receiverID,sourceID,rotor};
    const expected=[n,receiverID,sourceID,rotor];for(let f=0;f<4;f++)if(words[b+f]!==expected[f])witness(out,'Term identity mismatch',{ordinal:n,field:f,expected:expected[f],actual:words[b+f]});
    const status=words[b+4],code=words[b+5],mask=words[b+6],flags=words[b+7];if(code<8)codeCounts[code]++;if(status<7)statusCounts[status]++;
    const values=validateNumerics(words,b,out,identity),term=values[11];
    if(status===6) {
      if(!arithmeticPrefixValid(mask,code,flags,self))witness(out,'Arithmetic failure record malformed',{ordinal:n,code,mask,flags,self});
      witness(out,'GPU reported arithmetic failure',{ordinal:n,code,mask},'numerical');continue;
    }
    if(status===0||status===1||status>6){witness(out,'GPU unwritten or malformed status',{ordinal:n,status,code,mask});continue;}
    if(code>7||mask!==expectedMask(code,self))witness(out,'GPU reached stage mask malformed',{ordinal:n,code,mask,expected:expectedMask(code,self)});
    const expectedRoute=self?1:(code===0?2:0);
    if((flags&~15)!==0||(flags&3)!==expectedRoute||((code<6)&&(flags&12)!==0))witness(out,'GPU routing flags malformed',{ordinal:n,flags,expectedRoute});
    if(self&&code!==0)witness(out,'Self policy record malformed',{ordinal:n,code});
    if(status===2) {
      if(code!==3||term!==null||mask!==258055||flags!==0)witness(out,'Domain failure record malformed',{ordinal:n,status,code,mask,flags});
      witness(out,'GPU reported domain failure',{ordinal:n},'numerical');continue;
    }
    if(code===3||!(status===3||status===4||status===5)||(mask&2048)===0)witness(out,'GPU invalid summand status',{ordinal:n,status,code,mask});
    if(code<=5&&(status!==3||term!==0))witness(out,'GPU early zero status/value malformed',{ordinal:n,status,code,term});
    if(code===6&&(status!==4||term!==0||values[5]!==0))witness(out,'GPU zero projection malformed',{ordinal:n,status,term,projection:values[5]});
    if(code===7&&(!(values[5]>0)||!(status===4&&term===0||status===5&&term>0)))witness(out,'GPU positive projection malformed',{ordinal:n,status,term,projection:values[5]});
    if(status===5&&!(term>0)||status===4&&term!==0)witness(out,'GPU profile sign malformed',{ordinal:n,status,term});
    if(code!==R.codes[n]||code!==Q.codes[n])witness(out,'GPU policy classification mismatch',{ordinal:n,R:R.codes[n],Q:Q.codes[n],GPU:code},'numerical');
    for(let f=0;f<F;f++)if(values[f]!==null&&(Q.metadata[n*8+6]&(1<<f))!==0){out.counts.gpuStageComparisons++;const delta=Math.abs(values[f]-Q.scalars[n*F+f]);if(out.stageMaxAbsTQ[f]===null||delta>out.stageMaxAbsTQ[f]){out.stageMaxAbsTQ[f]=delta;out.stageMaxAbsTQWitness[f]=n;}}
    if(!Number.isFinite(R.terms[n])||!Number.isFinite(Q.terms[n]))witness(out,'Non-finite reference summand',{ordinal:n});
    // Structurally valid class mismatches remain diagnostic summands. Domain,
    // arithmetic, and malformed rows are excluded from every exact sum.
    if(out.errorClassCounts.integrity!==before||term===null)continue;
    qualifiedPerRotor[index]++;out.counts.gpuDyadicTermRows++;out.counts.gpuExactStoredTermAdds++;
    const t32=units32(words[b+19]),t=t32<<925n,r=units64(R.terms[n]),q=units64(Q.terms[n]),tr=t-r,tq=t-q,qr=q-r;
    l1TR[index]+=absBig(tr);l1TQ[index]+=absBig(tq);l1QR[index]+=absBig(qr);signedTR[index]+=tr;signedTQ[index]+=tq;signedQR[index]+=qr;sumT32[index]+=t32;if(term>0)positivePerRotor[index]++;
  }
  out.codeCounts=codeCounts;out.statusCounts=statusCounts;out.completeTermCoverage=out.counts.gpuDyadicTermRows===M;
  if(!out.completeTermCoverage)witness(out,'Incomplete qualified GPU term coverage',{qualified:out.counts.gpuDyadicTermRows,expected:M},'numerical');
  out.rotors=l1TR.map((value,index)=>{const gate=value+allowance,pass=gate<=epsilon&&qualifiedPerRotor[index]===5000;if(gate>epsilon)witness(out,'Exact pre reduction T-R L1 gate',{index},'numerical');return {index,receiverID:ids[Math.floor(index/4)],rotor:index%4,qualifiedTermCount:qualifiedPerRotor[index],positiveTerms:positivePerRotor[index],l1TR:certificate(value),l1TQ:certificate(l1TQ[index]),l1QR:certificate(l1QR[index]),signedTR:certificate(signedTR[index]),signedTQ:certificate(signedTQ[index]),signedQR:certificate(signedQR[index]),exactStoredTermSum:certificate(sumT32[index],-149),l1PlusAllowance:certificate(gate),pass};});
  return finish(out);
}
function assessSerial(termAssessment,bytes,C,ids) {
  const out=reportBase('saved-GPU-serial-reduction');out.counts={serialRecordsChecked:0,serialDyadicGates:0};
  if(!termAssessment?.pass||termAssessment.rotors?.length!==16||!Buffer.isBuffer(bytes)||bytes.length!==512||ids?.length!==4){witness(out,'Serial shape/prior qualification mismatch',{});return finish(out);}
  const words=decodeU32(bytes),epsilon=units64(C.epsilonWake),allowance=units64(C.referenceSumAllowance);out.threshold={epsilon:certificate(epsilon),referenceSumAllowance:certificate(allowance)};out.rotors=[];
  for(let i=0;i<16;i++) {
    out.counts.serialRecordsChecked++;const b=i*8,expected=[Math.floor(i/4),ids[Math.floor(i/4)],i%4,2,1,5000],before=out.errorCount;
    for(let f=0;f<6;f++)if(words[b+f]!==expected[f])witness(out,'Serial metadata mismatch',{index:i,field:f,expected:expected[f],actual:words[b+f]});
    if(words[b+7]!==NONE)witness(out,'Serial firstBadSlot must be sentinel',{index:i,actual:words[b+7]});
    const word=words[b+6];if((word&0x7f800000)===0x7f800000||((word>>>31)!==0&&(word&0x7fffffff)!==0)){witness(out,'Serial sum invalid binary32',{index:i,word});continue;}
    const row=termAssessment.rotors[i];requireThat(row.index===i&&row.exactStoredTermSum.exponent===-149&&row.l1TR.exponent===-1074,'Dyadic certificate schema');
    const exactT=BigInt(row.exactStoredTermSum.coefficient)<<925n,storedSum=units32(word)<<925n,error=storedSum-exactT,combined=BigInt(row.l1TR.coefficient)+absBig(error)+allowance,pass=combined<=epsilon&&before===out.errorCount;
    out.counts.serialDyadicGates++;if(combined>epsilon)witness(out,'Exact combined conservative error gate',{index:i},'numerical');
    out.rotors.push({index:i,receiverID:ids[Math.floor(i/4)],rotor:i%4,rawSumWord:word,serialSum:certificate(storedSum),exactStoredTermSum:certificate(exactT),signedReductionError:certificate(error),signedSerialTotalVsR:certificate(BigInt(row.signedTR.coefficient)+error),absoluteReductionError:certificate(absBig(error)),l1TR:row.l1TR,l1TQ:row.l1TQ,l1QR:row.l1QR,combinedConservativeError:certificate(combined),pass});
  }
  return finish(out);
}
function assessUsefulness(R,C) {
  const out=reportBase('prospective-scene-usefulness');out.counts={usefulnessTermRows:0,usefulnessDyadicAdds:0,usefulnessRotorGates:0};
  if(!referenceShape(R)||!R.complete){witness(out,'Usefulness requires complete original reference',{});return finish(out);}
  const epsilon=units64(C.epsilonWake),termThreshold=16n*epsilon,sumThreshold=256n*epsilon,sums=Array(16).fill(0n),substantive=Array(16).fill(0),positive=Array(16).fill(0);
  for(let n=0;n<M;n++) {
    out.counts.usefulnessTermRows++;if(!Number.isFinite(R.terms[n])||R.terms[n]<0){witness(out,'Invalid usefulness term',{ordinal:n});continue;}
    const i=Math.floor(n/20000)*4+n%4,t=units64(R.terms[n]);sums[i]+=t;out.counts.usefulnessDyadicAdds++;if(t>0n)positive[i]++;if(t>=termThreshold)substantive[i]++;
  }
  out.threshold={requiredReceivers:[0,1,2],minimumSubstantiveTermsPerRotor:4,termThreshold:certificate(termThreshold),minimumExactStoredSum:certificate(sumThreshold)};
  out.rotors=sums.map((sum,i)=>{const required=i<12,pass=!required||(substantive[i]>=4&&sum>=sumThreshold);if(required)out.counts.usefulnessRotorGates++;if(!pass)witness(out,'Prospective activity threshold unmet',{index:i,substantive:substantive[i]},'numerical');return {index:i,required,positiveTerms:positive[i],substantiveTerms:substantive[i],exactStoredSum:certificate(sum),pass};});
  return finish(out);
}
function compareReferences(A,B,C,label) {
  const out=reportBase('saved-reference-comparison');out.label=label;out.diagnosticOnly=true;out.counts={comparisonTermRows:0,comparisonStageFields:0,comparisonDyadicRows:0};
  if(!referenceShape(A)||!referenceShape(B)){witness(out,'Comparison reference shape',{});return finish(out);}
  if(!A.complete||!B.complete){out.available=false;out.reason='Reference incomplete; no partial science comparison';return finish(out);}
  out.available=true;out.codeMismatchCount=0;out.stageMaxAbs=Array(F).fill(null);out.stageMaxAbsWitness=Array(F).fill(null);out.stageMaskMismatchCount=0;
  const l1=Array(16).fill(0n),signed=Array(16).fill(0n),epsilon=units64(C.epsilonWake),allowance=units64(C.referenceSumAllowance);
  for(let n=0;n<M;n++) {
    out.counts.comparisonTermRows++;if(A.codes[n]!==B.codes[n])out.codeMismatchCount++;
    const ma=A.metadata[n*8+6],mb=B.metadata[n*8+6];if(ma!==mb)out.stageMaskMismatchCount++;
    for(let f=0;f<F;f++)if((ma&mb&(1<<f))!==0){out.counts.comparisonStageFields++;const delta=Math.abs(B.scalars[n*F+f]-A.scalars[n*F+f]);if(out.stageMaxAbs[f]===null||delta>out.stageMaxAbs[f]){out.stageMaxAbs[f]=delta;out.stageMaxAbsWitness[f]=n;}}
    if(!Number.isFinite(A.terms[n])||!Number.isFinite(B.terms[n])){witness(out,'Invalid comparison term',{ordinal:n});continue;}
    out.counts.comparisonDyadicRows++;const i=Math.floor(n/20000)*4+n%4,d=units64(B.terms[n])-units64(A.terms[n]);l1[i]+=absBig(d);signed[i]+=d;
  }
  out.rotors=l1.map((v,i)=>({index:i,l1:certificate(v),signed:certificate(signed[i]),l1PlusAllowance:certificate(v+allowance),withinUnchangedEpsilon:v+allowance<=epsilon}));return finish(out);
}
function compareGpuVectors(bytesA,bytesB,label) {
  const out=reportBase('saved-GPU-vector-comparison');out.label=label;out.diagnosticOnly=true;out.counts={vectorComparisonRows:0,vectorComponentComparisons:0};
  if(!Buffer.isBuffer(bytesA)||!Buffer.isBuffer(bytesB)||bytesA.length!==M*104||bytesB.length!==M*104){witness(out,'Vector comparison shape',{});return finish(out);}
  const a=decodeU32(bytesA),b=decodeU32(bytesB);out.fields=Array.from({length:6},(_,f)=>({scalarIndex:12+f,compared:0,rawWordDifferences:0,numericDifferences:0,maxAbsoluteDifference:null,maxWitness:null}));out.maskMismatchRows=0;
  for(let n=0;n<M;n++) {
    out.counts.vectorComparisonRows++;const base=n*WORDS,ma=a[base+6],mb=b[base+6];
    for(let f=0;f<4;f++)if(a[base+f]!==b[base+f])witness(out,'Vector comparison identity mismatch',{ordinal:n,field:f});
    if((ma&258048)!==(mb&258048))out.maskMismatchRows++;
    // The driver calls this only after both byte streams were structurally assessed.
    // Arithmetic/domain failed rows contribute no vectors to diagnostics.
    if(![3,4,5].includes(a[base+4])||![3,4,5].includes(b[base+4]))continue;
    for(let f=0;f<6;f++)if((ma&mb&(1<<(12+f)))!==0){
      out.counts.vectorComponentComparisons++;const row=out.fields[f],wa=a[base+20+f],wb=b[base+20+f],va=value32(wa),vb=value32(wb);row.compared++;
      if(!Number.isFinite(va)||!Number.isFinite(vb)){witness(out,'Nonfinite reached comparison vector',{ordinal:n,field:f});continue;}
      if(wa!==wb)row.rawWordDifferences++;if(va!==vb)row.numericDifferences++;const d=Math.abs(vb-va);if(row.maxAbsoluteDifference===null||d>row.maxAbsoluteDifference){row.maxAbsoluteDifference=d;row.maxWitness=n;}
    }
  }
  return finish(out);
}
module.exports={makeOriginalConstants,generateFresh,prepareOriginal,translatePrepared,packPrepared,evaluateSelected,assessR,assessQ,assessUsefulness,assessControls,assessGpuTerms,assessSerial,compareReferences,compareGpuVectors,encodeU32,encodeI32,encodeF64,decodeF64,decodeU32};
