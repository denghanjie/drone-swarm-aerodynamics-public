'use strict';
// New public-kernel fixed-state support sensitivity. No ODE or R8 execution.
const fs=require('fs'),path=require('path'),crypto=require('crypto');
const ROOT=path.resolve(__dirname,'..'),WS=path.resolve(ROOT,'..');
const BASE=path.join(WS,'research-recovery-r8/public-baseline');
const J='research/campaign-joint-stage-reference/implementation/';
const PLAN='2879a16281c5ce16ef064165fbcd9254ccf77ca6fde7759844144838305add44';
const MANIFEST='8cd490bc9b83e5b8f0819be17206aad308d320ac436e1e1a9a1e79c17662f35d';
const N=16,ROWS=401,ARMS=['P','X','R','U'],CAP=2000000;
const OUT=path.join(ROOT,'results'),ROWBYTES=N*17*8,WROW=4*N*4*8,LROW=4*N*3*8;
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
const elapsed=()=>Number(process.hrtime.bigint()-start)/1e9;
const start=process.hrtime.bigint(),cpuStart=process.cpuUsage();
let completed=0,location={phase:'admission'},wfd=null,lfd=null,outputCreated=false;
let A,F,W,area,vi,D,farStart,mg,armScale,raw,identities,adoption;
const check=(ok,message,detail={})=>{if(!ok)throw Object.assign(Error(message),{detail});};
const close=(a,b)=>Math.abs(a-b)<=1e-12+1e-12*Math.max(Math.abs(a),Math.abs(b));
const sums=(n)=>Array(n).fill(0);
function outputBytes(){return fs.readdirSync(OUT).reduce((s,f)=>s+fs.statSync(path.join(OUT,f)).size,0);}
function record(name,obj,failure=false){const b=Buffer.from(JSON.stringify(obj,null,2)+'\n'),p=path.join(OUT,name),old=fs.existsSync(p)?fs.statSync(p).size:0;const atomic=name==='progress.json';check(outputBytes()-(atomic?0:old)+b.length<=(failure?CAP:CAP-20000),'Output byte cap',{name,bytes:b.length});if(atomic){const tmp=p+'.pending';fs.writeFileSync(tmp,b,{flag:'wx'});fs.renameSync(tmp,p);}else fs.writeFileSync(p,b);}
function progress(status){record('progress.json',{status,completeRows:completed,totalRows:ROWS,validRowRange:completed?[0,completed-1]:null,unwrittenOrPartialRowsInvalid:true,location,wallSeconds:elapsed()});}
function guard(){check(elapsed()<59,'Cooperative wall reserve reached');check(process.memoryUsage().rss<=256*1024*1024,'Observed RSS threshold exceeded');}
function verified(relative){const m=identities.entries.find(x=>x.path===relative);check(m,'Missing pinned source identity',{relative});const b=fs.readFileSync(path.join(BASE,relative));check(b.length===m.bytes&&sha(b)===m.sha256,'Source/input identity mismatch',{relative,bytes:b.length,sha256:sha(b)});return b;}
function checkedWrite(fd,b,offset){let n=0;while(n<b.length){const k=fs.writeSync(fd,b,n,b.length-n,offset+n);check(k>0,'Short tensor write',{offset,n});n+=k;}}
function decode(row){return Array.from({length:N},(_,i)=>Array.from({length:17},(_,k)=>raw.readDoubleLE(row*ROWBYTES+(i*17+k)*8)));}
function nonmutation(states,row){for(let i=0;i<N;i++)for(let k=0;k<17;k++)check(Object.is(states[i][k],raw.readDoubleLE(row*ROWBYTES+(i*17+k)*8)),'Input state mutation',{row,receiver:i,index:k});}
function fade(a,b,x){const t=Math.max(0,Math.min(1,(x-a)/(b-a)));return 1-t*t*(3-2*t);}
function radialBin(x){return x<=2?0:x<3?1:x<=5?2:3;}
function axialBin(d){return d<2?0:d<2.5?1:2;}
const bins=Array.from({length:12},(_,k)=>({radial:['core_xi_le_2','transition_2_lt_xi_lt_3','outer_3_le_xi_le_5','extreme_xi_gt_5'][Math.floor(k/3)],axial:['d_lt_2','2_le_d_lt_2.5','d_ge_2.5'][k%3],pairs:0,armInflowSums:sums(4),interactionSum:0}));
const counts={pairVisits:0,upstreamExcluded:0,nearFieldExcluded:0,farFieldPairs:0,originalExactRotorMatches:0,originalRotorComparisons:0,baselineZeroRotors:0,newlyNonzeroRotors:sums(3)};
const checks={maxProductionInflowResidual:0,maxProductionLoadResidual:0,maxInteractionResidual:0,maxReceiverCubicResidual:0,inputNonmutationRows:0};
const addedMax=ARMS.slice(1).map(arm=>({arm,maxDownstream:null,maxXi:null,positivePairTerms:0}));
const topPairs=ARMS.slice(1).map(()=>[]);
function keepPair(a,w){if(!(w.value>0))return;const t=topPairs[a];t.push(w);t.sort((x,y)=>y.value-x.value||x.row-y.row||x.receiver-y.receiver||x.rotor-y.rotor||x.source-y.source);if(t.length>8)t.length=8;}
function allPairs(states,row){
 const axes=states.map((s,i)=>{check(Array.isArray(s)&&s.length===17&&s.every(Number.isFinite),'Invalid full17 state',{row,receiver:i});check(Math.max(...s.slice(0,3).map(Math.abs))<=1e6,'Position domain exceeded',{row,receiver:i});check(Math.abs(Math.hypot(...s.slice(6,10))-1)<=1e-10,'Quaternion norm domain',{row,receiver:i});check(s.slice(13).every(x=>x>=0),'Negative nominal thrust',{row,receiver:i});const a=F.rotate(s.slice(6,10),[0,0,1]);check(a[2]>=Math.cos(A.P.maxTiltDegrees*Math.PI/180),'Tilt domain',{row,receiver:i,axis:a});return a;});
 const winds=ARMS.map(()=>Array.from({length:N},()=>sums(4))),interaction=Array.from({length:N},()=>sums(4));
 for(let i=0;i<N;i++)for(let r=0;r<4;r++){
  const delta=F.rotate(states[i].slice(6,10),[F.rotors[r][0],F.rotors[r][1],0]),p=delta.map((x,k)=>x+states[i][k]);
  for(let j=0;j<N;j++)if(j!==i){location={phase:'replay',row,receiver:i,rotor:r,source:j};counts.pairVisits++;
   const d=[states[j][0]-p[0],states[j][1]-p[1],states[j][2]-p[2]],axis=axes[j],down=d.reduce((z,x,k)=>z+x*axis[k],0);
   if(down<=0){counts.upstreamExcluded++;continue;}
   const radial=Math.hypot(...d.map((x,k)=>x-down*axis[k]));
   if(down<farStart){check(radial>=A.P.nearFieldRadius,'Receiver enters unmodeled near wake',{...location,downstream:down,radial});counts.nearFieldExcluded++;continue;}
   const normalizedDown=down/D,half=W.parameters.spread*(normalizedDown-W.parameters.origin)*D;
   const cosine=Math.max(0,axes[i].reduce((z,x,k)=>z+x*axis[k],0)),speed=W.normalizedWake(normalizedDown,radial/D).speed;
   check(Number.isFinite(speed)&&speed>=0,'Invalid normalized profile',{...location,speed});
   const xi=radial/half,fz=fade(A.P.downstreamFade,A.P.downstreamCutoff,down),fr=fade(A.P.radialFade,A.P.radialCutoff,xi);
   // P reproduces production multiplication order and exact support tests.
   const terms=[down<A.P.downstreamCutoff&&radial<A.P.radialCutoff*half?speed*vi*fz*fr*cosine:0,speed*vi*fr*cosine,down<A.P.downstreamCutoff?speed*vi*fz*cosine:0,speed*vi*cosine];
   const cross=speed*vi*(1-fz)*(1-fr)*cosine;
   counts.farFieldPairs++;const b=bins[radialBin(xi)*3+axialBin(down)];b.pairs++;b.interactionSum+=cross;
   for(let a=0;a<4;a++){check(Number.isFinite(terms[a])&&terms[a]>=0,'Invalid pair contribution',{...location,arm:ARMS[a]});winds[a][i][r]+=terms[a];b.armInflowSums[a]+=terms[a];}
   interaction[i][r]+=cross;
   for(let a=1;a<4;a++){const diff=terms[a]-terms[0];if(diff>0){const e=addedMax[a-1];e.positivePairTerms++;e.maxDownstream=e.maxDownstream===null?down:Math.max(e.maxDownstream,down);e.maxXi=e.maxXi===null?xi:Math.max(e.maxXi,xi);keepPair(a-1,{value:diff,row,time:row*.0025,receiver:i,rotor:r,source:j,downstream:down,radial,xi});}}
  }
 }
 for(let i=0;i<N;i++)for(let r=0;r<4;r++){
  const [p,x,rr,u]=winds.map(w=>w[i][r]);location={phase:'factorial-check',row,receiver:i,rotor:r};
  check((x>=p||close(x,p))&&(rr>=p||close(rr,p))&&(u>=x||close(u,x))&&(u>=rr||close(u,rr)),'Inflow monotonicity failure',location);
  const cross=u-x-rr+p,expected=interaction[i][r];checks.maxInteractionResidual=Math.max(checks.maxInteractionResidual,Math.abs(cross-expected));check(close(cross,expected)&&(cross>=0||close(cross,0)),'Factorial interaction failure',{...location,cross,expected});
 }
 return winds;
}
function load(s,wind){const nominal=s.slice(13),rotor=nominal.map((f,r)=>A.effectiveThrust(f,wind[r]));for(let r=0;r<4;r++){check(Number.isFinite(rotor[r])&&rotor[r]>=0&&rotor[r]<=nominal[r],'Invalid receiver load',{...location,rotor:r,nominal:nominal[r],effective:rotor[r]});if(nominal[r]>0){const t=rotor[r]/nominal[r],alpha=wind[r]/Math.sqrt(nominal[r]/(2*A.P.rho*area)),res=Math.abs(t*t*t+alpha*t-1);check(Number.isFinite(res)&&res<=1e-10,'Receiver cubic residual failure',{...location,rotor:r,res});checks.maxReceiverCubicResidual=Math.max(checks.maxReceiverCubicResidual,res);}}const w=F.wrench(rotor);return [w.T,w.t[0],w.t[1]];}
const metrics=ARMS.slice(1).map(arm=>({arm,values:{inflow:[],thrust:[],roll:[],pitch:[],angular:[],momentNorm:[],verticalForce:[]},maxima:{},bins:{inflow:[0,0,0],thrust:[0,0,0],angular:[0,0,0]},longestSampleRun:{inflow:0,thrust:0,angular:0},runs:Array.from({length:N},()=>({inflow:0,thrust:0,angular:0}))}));
const armInflows=ARMS.map(()=>[]);
function sample(m,key,value,witness){m.values[key].push(value);const magnitude=Math.abs(value);if(!m.maxima[key]||magnitude>m.maxima[key].absolute)m.maxima[key]={value,absolute:magnitude,...witness};}
function bucket(x,a,b){return x<=a?0:x<=b?1:2;}
function summarizeValues(a){const s=a.slice().sort((x,y)=>x-y),n=s.length;return {count:n,min:s[0],median:s[Math.ceil(n*.5)-1],p95:s[Math.ceil(n*.95)-1],max:s[n-1]};}
function metricRecord(m){const values=Object.fromEntries(Object.entries(m.values).map(([k,v])=>[k,{signed:summarizeValues(v),absolute:summarizeValues(v.map(Math.abs))}]));return {arm:m.arm,values,maxima:m.maxima,descriptiveBins:m.bins,longestConsecutiveSampleRunAboveUpperBin:m.longestSampleRun};}
function probes(){const out=[];for(const d of [1,2,2.25,2.5,3])for(const xi of [0,1,2,2.5,3]){const s=d/D,b=W.parameters.spread*(s-W.parameters.origin)*D,r=xi*b,z=W.normalizedWake(s,r/D),direct=(W.parameters.decay/(s-W.parameters.origin))/(1+(Math.sqrt(2)-1)*xi*xi)**2,az=fade(2,2.5,d),ar=fade(2,3,xi);check(close(z.speed,direct),'Scalar profile identity failed',{d,xi});const vals=[z.speed*vi*az*ar,z.speed*vi*ar,z.speed*vi*az,z.speed*vi];check(vals[3]>=vals[1]&&vals[3]>=vals[2]&&vals[1]>=vals[0]&&vals[2]>=vals[0],'Scalar arm ordering',{d,xi});out.push({downstream:d,xi,speedMS:vals,axialFade:az,radialFade:ar});}check(fade(2,2.5,2)===1&&fade(2,2.5,2.25)===.5&&fade(2,2.5,2.5)===0,'Axial smoothstep identities');check(fade(2,3,2)===1&&fade(2,3,2.5)===.5&&fade(2,3,3)===0,'Radial smoothstep identities');return out;}
function receipt(status,error=null){const ru=process.resourceUsage();return {status,completeRows:completed,totalRows:ROWS,wallSecondsBeforeReceipt:elapsed(),cpuMicroseconds:process.cpuUsage(cpuStart),maxRSSBytes:ru.maxRSS*1024,rssSemantics:'Linux process.resourceUsage maxRSS, observed; no hard OS RSS limit claimed',rssThresholdBytes:256*1024*1024,rssChecks:'sampled at row boundaries',cooperativeWallReserveSeconds:59,externalWallCapSeconds:60,node:process.version,platform:process.platform,arch:process.arch,location,error,outputBytesBeforeReceipt:outputCreated?outputBytes():null};}
try{
 check(process.argv.length===3&&process.argv[2]==='--execute','Explicit --execute required after static review');
 check(process.platform==='linux','Resource receipt currently specifies Linux semantics');
 check(sha(fs.readFileSync(path.join(ROOT,'feasibility/FINITE-SUPPORT-PLAN.md')))===PLAN,'Frozen plan identity mismatch');
 adoption=JSON.parse(fs.readFileSync(path.join(ROOT,'ADOPTION.json'),'utf8'));check(adoption.plan_sha256===PLAN&&adoption.caps.output_bytes===CAP,'Adoption mismatch');
 const manifestBytes=fs.readFileSync(path.join(WS,'research-recovery-r8/public-source-identities.json'));check(sha(manifestBytes)===MANIFEST,'Public identity manifest changed');identities=JSON.parse(manifestBytes);
 check(identities.commit==='1336f5c416875a9651f92b58b2ed06649f25b04e','Public commit mismatch');
 const sources=['snapshot/outputs/milestone-28-source/aero.cjs','snapshot/outputs/step02c-source/physics.cjs','snapshot/outputs/step03a-source/wake.cjs','snapshot/outputs/milestone-26-source/grid.cjs'];sources.forEach(p=>verified(J+p));
 const input=J+'results/raw/s4301-compatibility.common.f64';raw=verified(input);const sidecar=JSON.parse(verified(input+'.json')),run=JSON.parse(verified(J+'results/runs/s4301-compatibility.json'));
 check(JSON.stringify(sidecar.shape)==='[401,16,17]'&&sidecar.bytes===ROWS*ROWBYTES&&sidecar.dt===.0025&&sidecar.cadenceTicks===128&&sidecar.baseTickSeconds===1/51200&&sidecar.encoding==='little-endian Float64, uncompressed','Input sidecar mismatch');
 check(run.complete===true&&run.config.count===16&&run.config.duration===1&&run.config.kind==='held'&&run.config.airTicks===512&&run.config.stepTicks===128,'Historical run metadata mismatch');
 // Kernel imports occur only after frozen identities are checked.
 A=require(path.join(BASE,J+sources[0]));F=require(path.join(BASE,J+sources[1]));W=require(path.join(BASE,J+sources[2]));
 D=A.P.motorDistance;farStart=W.parameters.minDownstream*D;mg=F.P.m*F.P.g;armScale=mg*F.P.a;area=Math.PI*A.P.rotorRadius**2;vi=Math.sqrt(mg/(2*A.P.rho*area*4));
 const supportBound=Math.hypot(A.P.downstreamCutoff,A.P.radialCutoff*W.parameters.spread*(A.P.downstreamCutoff-W.parameters.origin*D))+D/2+1e-6;
 const nearBound=Math.hypot(farStart,A.P.nearFieldRadius)+D/2+1e-6;
 check(supportBound<2.64&&supportBound<A.P.neighborRadius&&nearBound<A.P.neighborRadius,'Conservative grid-support bound failed',{supportBound,nearBound});
 fs.mkdirSync(OUT);outputCreated=true; // Exclusive attempt: an existing results directory prevents rerun.
 wfd=fs.openSync(path.join(OUT,'winds.f64'),'wx');fs.ftruncateSync(wfd,ROWS*WROW);
 lfd=fs.openSync(path.join(OUT,'loads.f64'),'wx');fs.ftruncateSync(lfd,ROWS*LROW);
 record('metadata.json',{schema:'public-support-factorial/v1',initialStatus:'running',validity:'Read progress.json and final summary/receipt for terminal status and valid tensor rows',claim:'Fixed-state finite-population formal support sensitivity; not physical validation or a new flight',planSha256:PLAN,runnerSha256:sha(fs.readFileSync(__filename)),commit:identities.commit,input:{path:input,sha256:sidecar.sha256,shape:sidecar.shape},sources:sources.map(p=>identities.entries.find(x=>x.path===J+p)),armOrder:ARMS,arms:{P:'both original tapers',X:'remove axial taper/cutoff, retain radial taper',R:'retain axial taper/cutoff, remove radial taper',U:'uncut formal continuation over finite sources'},winds:{path:'winds.f64',shape:[ROWS,4,N,4],bytes:ROWS*WROW,units:'m/s',encoding:'little-endian float64'},loads:{path:'loads.f64',shape:[ROWS,4,N,3],bytes:ROWS*LROW,columns:['total thrust N','body roll moment N m','body pitch moment N m'],encoding:'little-endian float64',yaw:'nominal original yaw torque unchanged'},dt:.0025,supportBound,nearBound,vi,mg,armScale,inertia:F.P.I,countsMeaning:'Rows, source terms and receiver-times are correlated; no independent-replicate inference',partitionMeaning:'Unweighted sums over endpoint source-to-rotor terms, not time integrals',tolerance:'absolute1e-12 + relative1e-12 for adapter comparisons',caps:{outputBytes:CAP,wallSeconds:60},durability:'Row progress replaced atomically using a counted temporary file; tensor fsync only at final close; no per-row power-loss durability claim'});
 record('probes.json',{kind:'25 scalar profile checks, not Boids fixtures',arms:ARMS,points:probes()});progress('running');
 for(let row=0;row<ROWS;row++){
  guard();const states=decode(row),winds=allPairs(states,row);location={phase:'production-comparator',row};const original=A.fields(states,'sum-rotor').winds;
  const wb=Buffer.alloc(WROW),lb=Buffer.alloc(LROW),loads=ARMS.map(()=>[]);
  for(let i=0;i<N;i++){
   location={phase:'load-check',row,receiver:i};
   for(let a=0;a<4;a++){loads[a][i]=load(states[i],winds[a][i]);for(let r=0;r<4;r++)wb.writeDoubleLE(winds[a][i][r],((a*N+i)*4+r)*8);for(let k=0;k<3;k++)lb.writeDoubleLE(loads[a][i][k],((a*N+i)*3+k)*8);armInflows[a].push(...winds[a][i]);}
   const oldLoad=load(states[i],original[i]);for(let k=0;k<3;k++){checks.maxProductionLoadResidual=Math.max(checks.maxProductionLoadResidual,Math.abs(loads[0][i][k]-oldLoad[k]));check(close(loads[0][i][k],oldLoad[k]),'Production load mismatch',{row,receiver:i,k});}
   for(let r=0;r<4;r++){counts.originalRotorComparisons++;if(Object.is(winds[0][i][r],original[i][r]))counts.originalExactRotorMatches++;const residual=Math.abs(winds[0][i][r]-original[i][r]);checks.maxProductionInflowResidual=Math.max(checks.maxProductionInflowResidual,residual);check(close(winds[0][i][r],original[i][r]),'Production field mismatch',{row,receiver:i,rotor:r,baseline:winds[0][i][r],original:original[i][r]});if(winds[0][i][r]===0){counts.baselineZeroRotors++;for(let a=1;a<4;a++)if(winds[a][i][r]>0)counts.newlyNonzeroRotors[a-1]++;}}
   for(let a=1;a<4;a++){
    check(loads[a][i][0]<=loads[0][i][0]||close(loads[a][i][0],loads[0][i][0]),'Thrust monotonicity failure',{row,receiver:i,arm:ARMS[a]});
    const m=metrics[a-1],du=winds[a][i].map((u,r)=>u-winds[0][i][r]),inflow=Math.max(...du),rotor=du.indexOf(inflow),dt=loads[a][i][0]-loads[0][i][0],tx=loads[a][i][1]-loads[0][i][1],ty=loads[a][i][2]-loads[0][i][2],angular=Math.max(Math.abs(tx/F.P.I[0]),Math.abs(ty/F.P.I[1])),vertical=F.rotate(states[i].slice(6,10),[0,0,dt])[2],wit={row,time:row*.0025,receiver:i};
    for(const [key,value] of Object.entries({inflow,thrust:dt,roll:tx,pitch:ty,angular,momentNorm:Math.hypot(tx,ty),verticalForce:vertical}))sample(m,key,value,key==='inflow'?{...wit,rotor}:wit);
    const bs={inflow:bucket(inflow/vi,.01,.05),thrust:bucket(Math.abs(dt)/mg,.001,.01),angular:bucket(angular,.01,.1)};
    for(const key of Object.keys(bs)){m.bins[key][bs[key]]++;m.runs[i][key]=bs[key]===2?m.runs[i][key]+1:0;m.longestSampleRun[key]=Math.max(m.longestSampleRun[key],m.runs[i][key]);}
   }
  }
  nonmutation(states,row);checks.inputNonmutationRows++;checkedWrite(wfd,wb,row*WROW);checkedWrite(lfd,lb,row*LROW);completed=row+1;location={phase:'row-complete',row};progress('running');
 }
 check(counts.pairVisits===ROWS*N*4*(N-1)&&completed===ROWS,'Incomplete candidate coverage');guard();
 fs.fsyncSync(wfd);fs.closeSync(wfd);wfd=null;fs.fsyncSync(lfd);fs.closeSync(lfd);lfd=null;
 location={phase:'finalize'};record('summary.json',{status:'complete',interpretation:'In-model support sensitivity on one fixed historical trajectory; uncut arms are not physical truth',completeRows:completed,rotorSamplesPerArm:ROWS*N*4,receiverTimes:ROWS*N,counts,checks,baselineBitEquality:counts.originalExactRotorMatches===counts.originalRotorComparisons,armInflowMS:ARMS.map((arm,a)=>({arm,...summarizeValues(armInflows[a])})),contrasts:metrics.map(metricRecord),normalizers:{inflow:vi,thrust:mg,rollPitchMoment:armScale,angular:'rad/s^2'},descriptiveBins:{inflowNormalized:[.01,.05],thrustMagnitudeNormalized:[.001,.01],angularMagnitude:[.01,.1],meaning:'Conventions only; no physical pass/fail threshold'},partitions:bins,addedContributionExtents:addedMax,worstAddedPairTerms:topPairs,artifacts:['winds.f64','loads.f64'].map(f=>({path:f,bytes:fs.statSync(path.join(OUT,f)).size,sha256:sha(fs.readFileSync(path.join(OUT,f)))}))});
 progress('complete');record('receipt.json',receipt('complete'));check(outputBytes()<=CAP,'Final output cap');process.stdout.write(JSON.stringify({status:'complete',rows:completed,outputBytes:outputBytes()})+'\n');
}catch(e){
 for(const fd of [wfd,lfd])if(fd!==null)try{fs.closeSync(fd);}catch(_){}
 const error={name:e.name,message:e.message,detail:e.detail||null};
 if(outputCreated){try{progress('failed');}catch(writeError){process.stderr.write('Failure progress error: '+writeError.message+'\n');}try{record('failure.json',receipt('failed',error),true);}catch(writeError){process.stderr.write('Failure receipt error: '+writeError.message+'\n');}}
 process.stderr.write(JSON.stringify({status:'failed',rows:completed,location,error})+'\n');process.exitCode=1;
}
