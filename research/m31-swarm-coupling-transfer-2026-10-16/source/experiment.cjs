'use strict';
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto'),zlib=require('node:zlib');
const {pairTerm}=require('./reference-excerpt.cjs');
const mg=.027*9.81,arm=.028,radius=.023,rho=1.225,A=Math.PI*radius*radius,R=Math.sqrt(2)*arm;
const c={D:2*R,decay:10.11,spread:.07668,origin:-5.817,minDown:2.5,neighbor:3,nearRad:.15,downFade:2,downCut:2.5,radFade:2,radCut:3,induced:Math.sqrt(mg/(8*rho*A)),sqrt2minus1:Math.sqrt(2)-1};
const constants={mg,arm,radius,rho,A,R,c};
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
let packagePath,started,outputBytes=0,current=null,progress={};
function guard(){if(process.memoryUsage().rss>1.5*1024**3)throw new Error('RSS guard exceeded');if(performance.now()-started>175000)throw new Error('internal wall guard exceeded');}
function write(rel,b,emergency=false){if(typeof b==='string')b=Buffer.from(b);if(outputBytes+b.length>(emergency?256:255)*1024**2)throw new Error('total output guard exceeded');fs.writeFileSync(path.join(packagePath,rel),b,{flag:'wx'});outputBytes+=b.length;return {path:rel,bytes:b.length,sha256:sha(b)};}
function json(rel,obj){return write(rel,JSON.stringify(obj)+'\n');}
function artifact(id,kind,typed,encoding){return {...write(`results/${id}-${kind}.bin`,Buffer.from(typed.buffer,typed.byteOffset,typed.byteLength)),encoding,shape:[typed.length]};}
function cross(a,b){return [a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]];}
function rotate(q,v){const t=cross(q,v).map(x=>2*x),u=cross(q,t);return v.map((x,k)=>x+(q[3]*t[k]+u[k]));}
const emptyWork=()=>({rootClosures:0,bisectionIterations:0,positiveTermMultiplications:0});
function root(alpha,w){if(!(alpha>=0&&Number.isFinite(alpha)))throw new Error('invalid alpha');w.rootClosures++;if(alpha===0)return 1;let lo=0,hi=1;for(let k=0;k<56;k++){let x=(lo+hi)/2;if(x*x*x+alpha*x-1>0)hi=x;else lo=x;w.bisectionIterations++;}return (lo+hi)/2;}
function logDistance(a,b){let v=0;for(let i=0;i<a.length;i++)v=Math.max(v,Math.abs(Math.log(a[i])-Math.log(b[i])));return v;}
function runCase(info){
 const {id,n,t}=info;current=id;progress={phase:'input'};guard();
 const raw=fs.readFileSync(path.join(packagePath,info.path));if(raw.length!==n*17*8||sha(raw)!==info.sha256)throw new Error('input byte/hash mismatch');
 const states=Array.from({length:n},(_,i)=>Array.from({length:17},(_,k)=>raw.readDoubleLE((17*i+k)*8)));
 const p=new Float64Array(28*n),nominal=states.map(s=>s.slice(13,17)),S0=nominal.map(a=>a.reduce((s,x)=>s+x,0));
 const input={finite:true,quaternionNormMaxError:0,quaternionBadCount:0,axisNormMaxError:0,axisBadCount:0,offsetNormMaxError:0,offsetDotMaxAbs:0,offsetBadCount:0,nominalZeroCount:0,nominalNegativeCount:0,nominalPositive:true,nominalTotalFinite:S0.every(Number.isFinite),geometryValid:false,maxTiltDegrees:0,tiltWithin45Count:0};
 const corners=[[arm,arm,0],[-arm,arm,0],[-arm,-arm,0],[arm,-arm,0]];
 for(let i=0;i<n;i++){
   const s=states[i],q=s.slice(6,10),axis=rotate(q,[0,0,1]);input.finite&&=s.every(Number.isFinite);
   const qe=Math.abs(Math.hypot(...q)-1),ae=Math.abs(Math.hypot(...axis)-1);input.quaternionNormMaxError=Math.max(input.quaternionNormMaxError,qe);input.axisNormMaxError=Math.max(input.axisNormMaxError,ae);if(qe>1e-10||!Number.isFinite(qe))input.quaternionBadCount++;if(ae>1e-9||!Number.isFinite(ae))input.axisBadCount++;
   p.set(s.slice(0,3),28*i);p.set(axis,28*i+4);
   const tilt=Math.acos(Math.max(-1,Math.min(1,axis[2]/Math.hypot(...axis))))*180/Math.PI;input.maxTiltDegrees=Math.max(input.maxTiltDegrees,tilt);if(tilt<=45)input.tiltWithin45Count++;
   for(let r=0;r<4;r++){const o=rotate(q,corners[r]);p.set(o,28*i+8+4*r);const ne=Math.abs(Math.hypot(...o)-R),de=Math.abs(o[0]*axis[0]+o[1]*axis[1]+o[2]*axis[2]);input.offsetNormMaxError=Math.max(input.offsetNormMaxError,ne);input.offsetDotMaxAbs=Math.max(input.offsetDotMaxAbs,de);if(ne>1e-9||de>1e-9||!Number.isFinite(ne+de))input.offsetBadCount++;if(nominal[i][r]===0)input.nominalZeroCount++;if(nominal[i][r]<0)input.nominalNegativeCount++;}
 }
 input.nominalPositive=input.finite&&nominal.every(a=>a.every(x=>x>0));input.geometryValid=input.finite&&input.quaternionBadCount===0&&input.axisBadCount===0&&input.offsetBadCount===0;
 const nominalOK=input.nominalPositive&&input.nominalTotalFinite;
 const symbols=Buffer.alloc(n*n*4,1),symbolCounts=Array(12).fill(0),offsets=new Uint32Array(4*n+1),sources=[],K=[],deps=Array.from({length:n},()=>[]);
 const geometryWork={directedCenterTests:0,centerEligiblePairs:0,centerGuardRejectedPairs:0,pairCalls:0,positiveRotorTerms:0};
 const order=Array.from({length:n},(_,i)=>i).sort((i,j)=>states[j][2]-states[i][2]||i-j),rank=new Uint32Array(n);order.forEach((i,k)=>rank[i]=k);
 let scaledCapMax=nominalOK?0:null,scaledCapViolationCount=nominalOK?0:null,uniqueVehicleEdges=0,heightViolationEdges=0,orderViolationEdges=0;
 for(let i=0;i<n;i++){
  progress={phase:'geometry',receiver:i,geometryWork};guard();const rows=[[],[],[],[]],incoming=new Set();
  for(let j=0;j<n;j++)if(i!==j){
   geometryWork.directedCenterTests++;const dx=p[28*j]-p[28*i],dy=p[28*j+1]-p[28*i+1],dz=p[28*j+2]-p[28*i+2],center=Math.hypot(dx,dy,dz),base=4*(i*n+j);
   if(!Number.isFinite(center)||center>512||Math.max(Math.abs(dx),Math.abs(dy),Math.abs(dz))>257){symbols.fill(11,base,base+4);geometryWork.centerGuardRejectedPairs++;continue;}
   if(center>=c.neighbor)continue;geometryWork.centerEligiblePairs++;
   for(let r=0;r<4;r++){const f=pairTerm(p,i,j,r,c,true);geometryWork.pairCalls++;symbols[base+r]=f.symbol;
    if(f.term>0){rows[r].push([j,f.term]);incoming.add(j);geometryWork.positiveRotorTerms++;if(geometryWork.positiveRotorTerms>2000000)throw new Error('positive coefficient guard exceeded');
     if(nominalOK){const v=f.term*Math.sqrt(S0[j]/mg);scaledCapMax=Math.max(scaledCapMax,v);if(!Number.isFinite(v)||v>128)scaledCapViolationCount++;}
    }
   }
  }
  for(let r=0;r<4;r++){for(const [j,k] of rows[r]){sources.push(j);K.push(k);}offsets[4*i+r+1]=sources.length;}
  deps[i]=[...incoming].sort((a,b)=>a-b);uniqueVehicleEdges+=deps[i].length;
  for(const j of deps[i]){if(states[j][2]<=states[i][2])heightViolationEdges++;if(rank[j]>=rank[i])orderViolationEdges++;}
 }
 for(const s of symbols)symbolCounts[s]++;
 const compressed=zlib.gzipSync(symbols,{level:6});if(compressed.length>64*1024**2)throw new Error('compressed symbol guard exceeded');
 const symbolArtifact={...write(`results/${id}-symbols.u8.gz`,compressed),encoding:'gzip-uint8',shape:[n,n,4],rawBytes:symbols.length,rawSha256:sha(symbols)};
 const src=Uint32Array.from(sources),kv=Float64Array.from(K),csr={offsets:artifact(id,'offsets',offsets,'uint32le'),sources:artifact(id,'sources',src,'uint32le'),K:artifact(id,'K',kv,'float64le')};
 const incomingDegree=deps.map(a=>a.length),descendingEligible=orderViolationEdges===0;let depth=null;
 if(descendingEligible){depth=Array(n).fill(0);for(const i of order)for(const j of deps[i])depth[i]=Math.max(depth[i],depth[j]+1);}
 const graph={uniqueVehicleEdges,incomingDegree,maxIncomingDegree:Math.max(...incomingDegree),heightViolationEdges,orderViolationEdges,descendingEligible,order,dependencyDepth:depth,maxDependencyDepth:depth?Math.max(...depth):null};
 const reasons=[];if(!input.geometryValid)reasons.push('geometry');if(!nominalOK)reasons.push('nominal');if(symbolCounts[4])reasons.push('near-field');if(symbolCounts[11])reasons.push('invalid-term');if(scaledCapViolationCount)reasons.push('scaled-cap');
 const admission={admitted:reasons.length===0,reasons,unsupportedNearCount:symbolCounts[4],invalidTermCount:symbolCounts[11],scaledCapMax,scaledCapViolationCount};
 let ordinaryLmax=null,aa=null;
 if(nominalOK){aa=new Float64Array(K.length);let maxSum=0;for(let row=0;row<4*n;row++){let sum=0;for(let z=offsets[row];z<offsets[row+1];z++){aa[z]=kv[z]*Math.sqrt(S0[src[z]]/mg)/Math.sqrt(nominal[Math.floor(row/4)][row%4]/(2*rho*A));sum+=aa[z];}maxSum=Math.max(maxSum,sum);}ordinaryLmax=maxSum/(4*Math.sqrt(2));}
 function nodeMap(i,y,w){const rotors=[];let total=0;for(let r=0;r<4;r++){const row=4*i+r;let alpha=0;for(let z=offsets[row];z<offsets[row+1];z++){alpha+=aa[z]*y[src[z]];w.positiveTermMultiplications++;}const x=root(alpha,w),T=nominal[i][r]*x;rotors.push({alpha,x,T});total+=T;}return {y:Math.sqrt(total/S0[i]),rotors};}
 function map(y,w){const rows=[];for(let i=0;i<n;i++){progress.receiver=i;progress.work=w;guard();rows.push(nodeMap(i,y,w));}return {y:rows.map(x=>x.y),rotors:rows.map(x=>x.rotors)};}
 function finish(y,rotors,work,extra={}){progress={phase:'residual',completedSolveWork:work};guard();const residualWork=emptyWork(),residualMap=map(y,residualWork);let sourceReceiverMismatch=0;for(let i=0;i<n;i++)sourceReceiverMismatch=Math.max(sourceReceiverMismatch,Math.abs(S0[i]*y[i]*y[i]-residualMap.rotors[i].reduce((s,x)=>s+x.T,0))/S0[i]);return {y,rotors,work,residualMap,residualWork,residualLog:logDistance(y,residualMap.y),sourceReceiverMismatch,...extra};}
 let solutions=null;
 if(admission.admitted&&descendingEligible){
   progress={phase:'direct'};const y=Array(n).fill(1),rotors=Array(n),work=emptyWork();for(const i of order){progress={phase:'direct',receiver:i,work};guard();const z=nodeMap(i,y,work);y[i]=z.y;rotors[i]=z.rotors;}const direct=finish(y,rotors,work);
   let yy=Array(n).fill(1),rr=null,iterates=[yy.slice()],pw=emptyWork(),converged=false,lastChange=null;
   for(let k=0;k<64;k++){progress={phase:'picard',update:k};guard();const z=map(yy,pw);lastChange=logDistance(yy,z.y);yy=z.y;rr=z.rotors;iterates.push(yy.slice());if(lastChange<=1e-11){converged=true;break;}}
   solutions={direct,picard:finish(yy,rr,pw,{iterates,iterations:iterates.length-1,converged,lastChange})};
 }
 const result={id,n,t,inputSha256:sha(raw),input,admission,symbols:symbolArtifact,symbolCounts,csr,geometryWork,graph,ordinaryLmax,solutions};json(`results/${id}.json`,result);return result;
}
function main(){packagePath=process.argv[2];if(!packagePath)throw new Error('package path required');started=performance.now();if(require('node:os').endianness()!=='LE')throw new Error('little-endian runtime required');
 const out={kind:'historical-swarm-frozen-pose-coupling-transfer',constants,cases:[],complete:false,runtime:{node:process.version}};
 try{const index=JSON.parse(fs.readFileSync(path.join(packagePath,'inputs/index.json'),'utf8'));for(const info of index.cases){const result=runCase(info);out.cases.push(result);console.log(JSON.stringify({id:result.id,admitted:result.admission.admitted,reasons:result.admission.reasons,positiveRotorTerms:result.geometryWork.positiveRotorTerms,iterations:result.solutions?.picard.iterations??null}));}out.complete=true;json('results/evidence.json',out);}
 catch(e){const safeMessages=['RSS guard exceeded','internal wall guard exceeded','total output guard exceeded','input byte/hash mismatch','positive coefficient guard exceeded','compressed symbol guard exceeded','invalid alpha'];const failure={id:current,progress,error:safeMessages.includes(e.message)?e.message:'unexpected execution exception',exceptionClass:e.constructor.name,completed:out.cases.map(x=>({id:x.id,path:`results/${x.id}.json`}))};write('results/failure.json',JSON.stringify(failure)+'\n',true);write('results/partial-evidence.json',JSON.stringify({kind:out.kind,constants,complete:false,cases:failure.completed,runtime:out.runtime})+'\n',true);process.exitCode=1;}
}
if(require.main===module)main();
