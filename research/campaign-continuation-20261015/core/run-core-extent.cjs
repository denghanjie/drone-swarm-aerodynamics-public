"use strict";
// Prospective single-receiver mathematical benchmark. No flight or source coupling.
const fs=require('fs'),path=require('path'),crypto=require('crypto');
const ROOT=__dirname,WS=path.dirname(ROOT),OUT=path.join(ROOT,'results');
const ID='CORE-EXTENT-CERTIFICATE-20261015',COMMIT='1336f5c416875a9651f92b58b2ed06649f25b04e';
const PLAN='b71f9b869b64836b38f0cb21c87cebd460def9cafd62dee9315d4d68c4ca4eaa';
const BASE=path.join(WS,'research-recovery-r8/public-baseline/research/campaign-joint-stage-reference/implementation');
const SOURCES=[
 ['snapshot/outputs/milestone-28-source/aero.cjs','710b0a8f0df62208e3385ac9b8288240b379fe9248a1a645251a77c533f24a62'],
 ['snapshot/outputs/step02c-source/physics.cjs','0c46c9beb4e831c621658f6600c074f97c95966de07f5000eb64aa476a443fa1'],
 ['snapshot/outputs/step03a-source/wake.cjs','fb6d5a1d632a0023818041ef6bc39316ff8ed950f318da1a6649e2515b9fd8bc'],
 ['snapshot/outputs/milestone-26-source/grid.cjs','f06010781770b64432935e5d825bcd1405b154b735ac4d0d654f145600cea302']
];
const CAP=100000,TOTAL=200000,MAX_N=4096,MAX_SLOTS=196608,DELTA=.25,EXTENTS=[2,4,8],PHASES=[0,.125];
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
const start=process.hrtime.bigint(),cpuStart=process.cpuUsage();
let created=false,completed=0,location={phase:'admission'},pairVisits=0,armSlots=0,fixtures=[];
let A,F,W,D,r0,s,k,vi,coef,c,f2,sourceRecords,runnerHash;
const elapsed=()=>Number(process.hrtime.bigint()-start)/1e9;
function check(ok,message,detail={}){if(!ok)throw Object.assign(Error(message),{detail});}
function tol(a,b){return 1e-12*Math.max(1,Math.abs(a),Math.abs(b));}
function close(a,b){return Number.isFinite(a)&&Number.isFinite(b)&&Math.abs(a-b)<=tol(a,b);}
function fade(a,b,x){const t=Math.max(0,Math.min(1,(x-a)/(b-a)));return 1-t*t*(3-2*t);}
function bytes(dir){return fs.readdirSync(dir).reduce((n,f)=>{const p=path.join(dir,f),st=fs.lstatSync(p);check(!st.isSymbolicLink(),'Symlinks forbidden in campaign',{p});return n+(st.isDirectory()?bytes(p):st.size);},0);}
function guard(){check(elapsed()<59,'Cooperative wall reserve reached');check(bytes(ROOT)<=TOTAL,'Campaign byte cap exceeded');}
function record(name,obj,failure=false){
 const data=Buffer.from(JSON.stringify(obj,null,2)+'\n'),target=path.join(OUT,name),tmp=target+'.pending';
 // Count the old file plus the pending replacement at peak, and reserve failure space.
 check(bytes(OUT)+data.length<=(failure?CAP:CAP-8000),'Output byte cap',{name,bytes:data.length});
 check(bytes(ROOT)+data.length<=TOTAL,'Campaign byte cap',{name});
 fs.writeFileSync(tmp,data,{flag:'wx'});fs.renameSync(tmp,target);
}
function progress(status){record('progress.json',{experimentId:ID,status,completeFixtures:completed,totalFixtures:6,completeFixtureIds:fixtures.slice(0,completed).map(f=>f.id),pairVisits,armSlots,location,wallSeconds:elapsed(),partialCoverageInvalidForCompleteClaim:true});}
function verifySources(){return SOURCES.map(([p,expected])=>{const b=fs.readFileSync(path.join(BASE,p));check(sha(b)===expected,'Public source identity mismatch',{path:p});return {path:p,sha256:expected,bytes:b.length};});}
function coordinateHash(coords){const b=Buffer.alloc(coords.length*24);coords.forEach((v,i)=>v.forEach((x,j)=>b.writeDoubleLE(x,24*i+8*j)));return sha(b);}
function makeFixture(phase,L){
 const id='phase-'+(phase===0?'0':'0125')+'-L'+L,coords=[],layers=[],seen=new Set();
 for(let j=0;j<=(L-.5)/DELTA;j++){
  const d=.5+j*DELTA,b=k*(d+s),R=2*b-r0,lim=Math.ceil((R+phase)/DELTA)+1;
  check(R>0&&Number.isInteger(lim),'Invalid layer geometry',{id,j});let count=0;
  for(let iy=-lim;iy<=lim;iy++)for(let ix=-lim;ix<=lim;ix++){
   const x=ix*DELTA+phase,y=iy*DELTA+phase;
   if(x*x+y*y<=R*R){const key=[x,y,d].join(',');check(!seen.has(key),'Duplicate source',{id,key});seen.add(key);coords.push([x,y,d]);count++;check(coords.length<=MAX_N,'Fixture source cap',{id});}
  }
  const h=DELTA/Math.SQRT2,lower=Math.PI*Math.max(R-h,0)**2/DELTA**2,upper=Math.PI*(R+h)**2/DELTA**2;
  check(count>=lower-tol(count,lower)&&count<=upper+tol(count,upper),'Lattice disk count bound failed',{id,j,count,lower,upper});
  layers.push({downstream:d,sourceRadius:R,count,axialFade:fade(A.P.downstreamFade,A.P.downstreamCutoff,d),countLower:lower,countUpper:upper});
 }
 check(layers.length===(L-.5)/DELTA+1&&layers.reduce((n,l)=>n+l.count,0)===coords.length,'Layer coverage',{id});
 return {id,phaseMeters:[phase,phase],extentMeters:L,sourceCount:coords.length,coordinatesSha256:coordinateHash(coords),layers,coords};
}
function score(f){
 const P=[0,0,0,0],X=[0,0,0,0],omitted=[0,0,0,0];
 const B=f.layers.reduce((v,l)=>v+l.count*(1-l.axialFade)/(l.downstream+s),0),bounds={lower:coef*f2*B,upper:coef*B};
 const checks={maxClosedFormResidual:0,maxOmissionCancellationResidual:0,maxXi:0,minDownstream:Infinity,maxDownstream:0,maxRotorRadiusResidual:0,radialWeightsExactlyOne:0,pairVisits:0};
 let largestTerm=null,largestOmitted=null;
 for(let r=0;r<4;r++){
  const [rx,ry]=F.rotors[r];
  for(let i=0;i<f.coords.length;i++){
   if(i%256===0)guard();location={phase:'score',fixture:f.id,rotor:r,source:i};
   const [x,y,d]=f.coords[i],radial=Math.hypot(x-rx,y-ry),nd=d/D,half=W.parameters.spread*(nd-W.parameters.origin)*D;
   const xi=radial/half,fr=fade(A.P.radialFade,A.P.radialCutoff,xi),fz=fade(A.P.downstreamFade,A.P.downstreamCutoff,d);
   check(d>=.5&&d>=W.parameters.minDownstream*D,'Near-field/domain failure',location);
   check(xi<=2+1e-12&&fr===1,'All-rotor core certificate failed',{...location,xi,fr,radial,half});
   const normalized=W.normalizedWake(nd,radial/D);check(normalized.speed!==null,'Kernel rejected geometry',location);
   const w=normalized.speed*vi,closed=coef/(d+s)/(1+c*(radial/(k*(d+s)))**2)**2;
   check(close(w,closed),'Closed-form/profile mismatch',{...location,w,closed});
   // Exact finite-support tests and original arithmetic order; projection is 1.
   const p=d<A.P.downstreamCutoff&&radial<A.P.radialCutoff*half?normalized.speed*vi*fz*fr*1:0;
   const q=normalized.speed*vi*fr*1,add=q-p;
   check([p,q,add].every(Number.isFinite)&&p>=0&&q>=p,'Invalid arm term',{...location,p,q});
   P[r]+=p;X[r]+=q;omitted[r]+=add;pairVisits++;armSlots+=2;checks.pairVisits++;
   checks.radialWeightsExactlyOne++;checks.maxXi=Math.max(checks.maxXi,xi);checks.minDownstream=Math.min(checks.minDownstream,d);checks.maxDownstream=Math.max(checks.maxDownstream,d);
   checks.maxRotorRadiusResidual=Math.max(checks.maxRotorRadiusResidual,radial-2*k*(d+s));
   checks.maxClosedFormResidual=Math.max(checks.maxClosedFormResidual,Math.abs(w-closed));
   const witness={rotor:r,sourceIndex:i,coordinates:[x,y,d],downstream:d,radial,xi,P:p,X:q,omitted:add};
   if(largestTerm===null||q>largestTerm.X)largestTerm=witness;
   if(largestOmitted===null||add>largestOmitted.omitted)largestOmitted=witness;
  }
 }
 const rotorResults=P.map((p,r)=>{
  const difference=X[r]-p;
  check(close(difference,omitted[r]),'Omitted-term summation mismatch',{fixture:f.id,rotor:r,difference,direct:omitted[r]});
  check(difference>=bounds.lower-tol(difference,bounds.lower)&&difference<=bounds.upper+tol(difference,bounds.upper),'Finite support bound failed',{fixture:f.id,rotor:r,difference,bounds});
  checks.maxOmissionCancellationResidual=Math.max(checks.maxOmissionCancellationResidual,Math.abs(difference-omitted[r]));
  return {rotor:r,P:p,X:X[r],P_over_vi:p/vi,X_over_vi:X[r]/vi,difference,directOmissionSum:omitted[r],omissionFractionOfX:X[r]===0?null:difference/X[r],lowerSlack:difference-bounds.lower,upperSlack:bounds.upper-difference};
 });
 check(checks.pairVisits===f.sourceCount*4&&checks.radialWeightsExactlyOne===checks.pairVisits,'Incomplete rotor coverage',{fixture:f.id});
 if(f.extentMeters>=4)check(bounds.lower>0,'Expected positive omitted-core bound',{fixture:f.id});
 check(coordinateHash(f.coords)===f.coordinatesSha256,'Source input mutation',{fixture:f.id});
 return {experimentId:ID,status:'complete',fixture:f.id,phaseMeters:f.phaseMeters,extentMeters:f.extentMeters,sourceCount:f.sourceCount,coordinates:{encoding:'ordered xyz Float64 little-endian triples, no header',sha256:f.coordinatesSha256,bytes:f.sourceCount*24,retained:false},layers:f.layers,B,boundsMS:bounds,rotors:rotorResults,largestIndividualTerm:largestTerm,largestIndividualOmission:largestOmitted,checks,inputNonmutation:true};
}
function receipt(status,error=null){return {experimentId:ID,status,completeFixtures:completed,totalFixtures:6,pairVisits,armSlots,wallSecondsBeforeReceipt:elapsed(),cpuMicroseconds:process.cpuUsage(cpuStart),node:process.version,location,error,outputBytesBeforeReceipt:created?bytes(OUT):null};}
try{
 check(process.argv.length===3&&process.argv[2]==='--execute','Explicit --execute required after independent review');
 check(sha(fs.readFileSync(path.join(ROOT,'PLAN.md')))===PLAN,'Frozen plan mismatch');runnerHash=sha(fs.readFileSync(__filename));
 const adoption=JSON.parse(fs.readFileSync(path.join(ROOT,'ADOPTION.json'),'utf8'));
 check(adoption.experiment_id===ID&&adoption.plan_sha256===PLAN&&adoption.runner_sha256===runnerHash&&adoption.caps.wall_seconds===60&&adoption.caps.output_bytes===CAP&&adoption.caps.total_bytes===TOTAL,'Release/adoption mismatch');
 sourceRecords=verifySources();A=require(path.join(BASE,SOURCES[0][0]));F=require(path.join(BASE,SOURCES[1][0]));W=require(path.join(BASE,SOURCES[2][0]));
 check(F.P.a===.028&&F.P.m===.027&&F.P.g===9.81&&A.P.rho===1.225&&A.P.rotorRadius===.023,'Frozen vehicle constants mismatch');
 check(JSON.stringify(F.rotors.map(v=>v.slice(0,2)))===JSON.stringify([[.028,.028],[-.028,.028],[-.028,-.028],[.028,-.028]]),'Rotor geometry/order changed');
 check(W.parameters.decay===10.11&&W.parameters.spread===.07668&&W.parameters.origin===-5.817&&W.parameters.minDownstream===2.5,'Frozen wake constants mismatch');
 check(A.P.downstreamFade===2&&A.P.downstreamCutoff===2.5&&A.P.radialFade===2&&A.P.radialCutoff===3&&A.P.neighborRadius===3,'Frozen supports mismatch');
 D=A.P.motorDistance;r0=D/2;s=-W.parameters.origin*D;k=W.parameters.spread;c=Math.sqrt(2)-1;f2=(1+4*c)**-2;
 check(D===2*Math.SQRT2*F.P.a&&F.rotors.every(r=>Math.hypot(r[0],r[1])<=r0+1e-15),'Rotor offset envelope mismatch');
 const area=Math.PI*A.P.rotorRadius**2;vi=Math.sqrt(F.P.m*F.P.g/(2*A.P.rho*area*4));coef=W.parameters.decay*D*vi;
 const supportBound=Math.hypot(A.P.downstreamCutoff,A.P.radialCutoff*k*(A.P.downstreamCutoff+s))+r0+1e-6;
 check(supportBound<2.64&&supportBound<A.P.neighborRadius,'Original P search-envelope proof failed');
 check(fade(2,2.5,2)===1&&fade(2,2.5,2.25)===.5&&fade(2,2.5,2.5)===0&&fade(2,3,2)===1,'Fade boundary/midpoint check failed');
 check(bytes(ROOT)<=TOTAL,'Initial campaign cap');fs.mkdirSync(OUT);created=true;
 record('metadata.json',{experimentId:ID,initialStatus:'running',planSha256:PLAN,runnerSha256:runnerHash,publicCommit:COMMIT,sources:sourceRecords,geometry:{receiver:[0,0,0],quaternion:[0,0,0,1],rotors:F.rotors.map(r=>[r[0],r[1],0]),delta:DELTA,phases:PHASES,extents:EXTENTS,order:'phase, extent; coordinates height/y/x'},constants:{D,r0,s,k,vi,A:coef,c,f2,supportBound},arms:{P:'original finite axial/radial support',X:'axial support removed, radial support retained'},claim:'Conditional finite-population core support certificate; no physical accuracy, source-source coupling, load law, flight, or novelty claim',limits:'Core radial location does not validate 8 m axial extent or multi-source independence',caps:{outputBytes:CAP,campaignBytes:TOTAL,wallSeconds:60,maxSourcesPerFixture:MAX_N,maxSourceRotorArmSlots:MAX_SLOTS},inputReuse:'No input files or historical replay are evaluated; existing PUBLIC-SUPPORT-FACTORIAL-20261015 is context only'});
 location={phase:'preflight'};progress('running');
 for(const phase of PHASES)for(const L of EXTENTS){guard();fixtures.push(makeFixture(phase,L));}
 const expectedPairs=fixtures.reduce((n,f)=>n+f.sourceCount*4,0);check(expectedPairs*2<=MAX_SLOTS,'Total evaluation cap');
 for(let p=0;p<2;p++)for(let e=1;e<3;e++){
  const prev=fixtures[p*3+e-1],next=fixtures[p*3+e];
  check(next.sourceCount>prev.sourceCount&&coordinateHash(next.coords.slice(0,prev.sourceCount))===prev.coordinatesSha256,'Nested source-prefix mismatch',{previous:prev.id,next:next.id});
  check(JSON.stringify(next.layers.slice(0,prev.layers.length))===JSON.stringify(prev.layers),'Nested layer-prefix mismatch');
 }
 const results=[];
 for(const f of fixtures){guard();const result=score(f);record(f.id+'.json',result);results.push(result);completed++;location={phase:'fixture-complete',fixture:f.id};progress('running');}
 const crossExtent=[];
 for(let p=0;p<2;p++)for(let r=0;r<4;r++){
  const a=results[p*3].rotors[r],b=results[p*3+1].rotors[r],d=results[p*3+2].rotors[r];
  check(Object.is(b.P,d.P),'P plateau is not bit-identical',{phase:PHASES[p],rotor:r,P4:b.P,P8:d.P});
  check(d.X>b.X&&b.X>a.X,'Strict X growth failed',{phase:PHASES[p],rotor:r});
  crossExtent.push({phaseMeters:PHASES[p],rotor:r,P4_equals_P8_bitwise:true,X4_over_X2:b.X/a.X,X8_over_X4:d.X/b.X});
 }
 check(completed===6&&pairVisits===expectedPairs&&armSlots===expectedPairs*2,'Incomplete final coverage');
 check(JSON.stringify(verifySources())===JSON.stringify(sourceRecords),'Postrun public source change');guard();location={phase:'finalize'};
 record('summary.json',{experimentId:ID,status:'complete',completeFixtures:completed,pairVisits,armSlots,fixtureRecords:results.map(r=>{const name=r.fixture+'.json',b=fs.readFileSync(path.join(OUT,name));return {path:name,bytes:b.length,sha256:sha(b),sourceCount:r.sourceCount,coordinatesSha256:r.coordinates.sha256};}),crossExtent,allInputNonmutation:true,publicSourcesRechecked:true,interpretation:'Finite bounds and finite extent ratios only; no fitted exponent, physical validation, new Boids flight, or speed benefit',anchor:'Existing PUBLIC-SUPPORT-FACTORIAL-20261015 genuine local3D replay had no axial exposure; not rerun'});
 progress('complete');record('receipt.json',receipt('complete'));check(bytes(OUT)<=CAP&&bytes(ROOT)<=TOTAL,'Final storage cap');
 process.stdout.write(JSON.stringify({experimentId:ID,status:'complete',completeFixtures:completed,pairVisits,armSlots,outputBytes:bytes(OUT)})+'\n');
}catch(e){
 const error={name:e.name,message:e.message,detail:e.detail||null};
 if(created){try{progress('failed');}catch(w){process.stderr.write('Progress retention failed: '+w.message+'\n');}try{record('failure.json',receipt('failed',error),true);}catch(w){process.stderr.write('Failure receipt retention failed: '+w.message+'\n');}}
 process.stderr.write(JSON.stringify({experimentId:ID,status:'failed',completeFixtures:completed,location,error})+'\n');process.exitCode=1;
}
