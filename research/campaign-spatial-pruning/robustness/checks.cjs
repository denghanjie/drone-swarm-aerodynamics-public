'use strict';
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto'),cp=require('node:child_process'),os=require('node:os');
const X=require('./fixtures.cjs'),O=require('./oracle.cjs');
const legacyPath=path.join(X.SOURCE,'outputs/milestone-28-source/aero.cjs'),A=require(legacyPath);
const candidatePath=path.resolve(__dirname,'../src/pruned-aero.cjs');
const hash=file=>crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex');
const initialCandidateHash=fs.existsSync(candidatePath)?hash(candidatePath):null;
const candidate=initialCandidateHash?require(candidatePath):null;
const safe=(fn)=>{try{return {ok:true,result:fn()};}catch(e){return {ok:false,name:e.name,message:e.message,detail:e.detail};}};
const max=xs=>xs.length?Math.max(...xs):0;
function comparison(states,reference,actual){
  const a=reference.winds.flat(),b=actual.winds.flat();
  if(a.length!==b.length||!b.every(Number.isFinite))return {finiteAndShape:false};
  const errors=a.map((v,i)=>Math.abs(v-b[i]));let forceMax=0,momentMax=0,normalizedForceMax=0,normalizedMomentMax=0;
  for(let i=0;i<states.length;i++){
    const nominal=states[i].slice(13,17),ra=nominal.map((v,k)=>A.effectiveThrust(v,reference.winds[i][k])),
      rb=nominal.map((v,k)=>A.effectiveThrust(v,actual.winds[i][k])),wa=X.F.wrench(ra),wb=X.F.wrench(rb),
      force=Math.abs(wa.T-wb.T),moment=Math.hypot(wa.t[0]-wb.t[0],wa.t[1]-wb.t[1]);
    forceMax=Math.max(forceMax,force);momentMax=Math.max(momentMax,moment);
    normalizedForceMax=Math.max(normalizedForceMax,force/X.C.weight);normalizedMomentMax=Math.max(normalizedMomentMax,moment/(X.C.weight*X.F.P.a));
  }
  return {finiteAndShape:true,inflowMaxAbs:max(errors),inflowRMS:Math.sqrt(errors.reduce((a,b)=>a+b*b,0)/Math.max(errors.length,1)),
    forceMaxAbs:forceMax,momentXYMaxAbs:momentMax,forceMaxWeightFraction:normalizedForceMax,momentMaxWeightArmFraction:normalizedMomentMax,
    exactPass:max(errors)<=1e-10&&forceMax<=1e-12&&momentMax<=1e-12,
    approximationTolerancePass:normalizedForceMax<=.005&&normalizedMomentMax<=.0075};
}
function invalidCheck(modulePath,kind,isCandidate){
  // Use a short-lived isolated process: the inherited grid may loop for Infinity.
  const code=`const X=require(${JSON.stringify(path.join(__dirname,'fixtures.cjs'))}),A=require(${JSON.stringify(modulePath)});let s=[X.state(),X.state([0,0,2])];const kind=${JSON.stringify(kind)};
  if(kind==='nan_position')s[0][0]=NaN;if(kind==='infinite_position')s[0][0]=Infinity;
  if(kind==='nan_quaternion')s[0][6]=NaN;if(kind==='zero_quaternion')s[0].splice(6,4,0,0,0,0);
  if(kind==='nonunit_quaternion')s[0][9]=2;if(kind==='short_state')s[0].pop();if(kind==='negative_nominal')s[0][13]=-.01;
  try{let r=A.fields(s,${isCandidate?"{epsilon:0,search:'grid'}":"'sum-rotor'"});process.stdout.write(JSON.stringify({rejected:false,finite:r.winds.flat().every(Number.isFinite),winds:r.winds}));}
  catch(e){process.stdout.write(JSON.stringify({rejected:true,name:e.name,message:e.message,detail:e.detail}));}`;
  const r=cp.spawnSync(process.execPath,['-e',code],{encoding:'utf8',timeout:1000});
  if(r.error)return {timeout:r.error.code==='ETIMEDOUT',error:r.error.message};
  try{return JSON.parse(r.stdout);}catch(e){return {executionError:true,status:r.status,stderr:r.stderr,stdout:r.stdout};}
}
function main(){
  const full=process.argv.includes('--full');
  const smokeIds=['empty','isolated','equal_height_square','vertical_0.2','vertical_0.75','radial_3_-1e-9','tilt_19.999','tilt_20.001','near_domain','many_weak_8'];
  const fixtures=full?X.fixtures():X.fixtures().filter(f=>smokeIds.includes(f.id)),records=[];const methods=[['legacy',s=>A.fields(s,'sum-rotor')]];
  if(candidate){methods.push(['exact_grid',s=>candidate.fields(s,{epsilon:0,search:'grid'})],['exact_brute',s=>candidate.fields(s,{epsilon:0,search:'brute'})]);
    for(const epsilon of [.002,.01,.04])methods.push([`epsilon_${epsilon}`,s=>candidate.fields(s,{epsilon,search:'grid'})]);}
  for(const fixture of fixtures){
    const serialized=JSON.stringify(fixture.states),reference=safe(()=>O.fields(fixture.states));
    const row={id:fixture.id,tags:fixture.tags,expectedDomainFailure:!!fixture.expectedDomainFailure,reference,methods:{}};
    for(const [name,fn]of methods){
      const actual=safe(()=>fn(fixture.states));row.methods[name]=actual;
      actual.inputsUnmutated=JSON.stringify(fixture.states)===serialized;
      actual.domainOutcomeMatch=actual.ok===reference.ok;
      if(actual.ok&&reference.ok){actual.comparison=comparison(fixture.states,reference.result,actual.result);
        if(actual.result.omittedBounds){const b=actual.result.omittedBounds;
          actual.boundCompliance=reference.result.winds.every((u,i)=>u.every((v,k)=>v-actual.result.winds[i][k]>=-1e-12&&v-actual.result.winds[i][k]<=b[i]+1e-12));}}
    }
    records.push(row);
  }
  const metamorphic=[];
  for(const fixture of fixtures.filter(f=>['many_weak_8','lattice_N27_spacing1','vertical_0.75'].includes(f.id))){
    for(const [name,fn]of methods){
      const original=safe(()=>fn(fixture.states));if(!original.ok)continue;
      const reversed=safe(()=>fn([...fixture.states].reverse()));
      const translated=safe(()=>fn(fixture.states.map(s=>s.map((v,k)=>k<3?v+[1.499999,-3.000001,.125][k]:v))));
      const permuted=reversed.ok?{...reversed.result,winds:[...reversed.result.winds].reverse()}:null;
      const exactOriginal=O.fields(fixture.states),reversedStates=[...fixture.states].reverse(),exactReversed=O.fields(reversedStates);
      const reversedBoundCompliance=reversed.ok&&reversed.result.omittedBounds?exactReversed.winds.every((u,i)=>u.every((v,k)=>v-reversed.result.winds[i][k]>=-1e-12&&v-reversed.result.winds[i][k]<=reversed.result.omittedBounds[i]+1e-12)):null;
      metamorphic.push({fixture:fixture.id,method:name,permutation:permuted?comparison(fixture.states,original.result,permuted):reversed,
        originalAgainstExact:comparison(fixture.states,exactOriginal,original.result),
        reversedAgainstExact:reversed.ok?comparison(reversedStates,exactReversed,reversed.result):reversed,reversedBoundCompliance,
        translation:translated.ok?comparison(fixture.states,original.result,translated.result):translated,
        note:name.startsWith('epsilon')?'Greedy omission is source-order dependent. Exact invariance is diagnostic, not a required property for this candidate. Bounds must remain valid.':null});
    }
  }
  const invalid={};for(const [name,p]of [['legacy',legacyPath],...(candidate?[['candidate',candidatePath]]:[])]){
    invalid[name]={};for(const kind of ['nan_position','infinite_position','nan_quaternion','zero_quaternion','nonunit_quaternion','short_state','negative_nominal'])invalid[name][kind]=invalidCheck(p,kind,name==='candidate');}
  const files=[__filename,path.join(__dirname,'fixtures.cjs'),path.join(__dirname,'oracle.cjs'),legacyPath,...(candidate?[candidatePath]:[])];
  const finalCandidateHash=candidate?hash(candidatePath):null;
  const result={utc:new Date().toISOString(),phase:candidate?'candidate-independent-checks':'legacy-baseline-checks',coverage:full?'full-functional':'smoke-functional',sourceCommit:X.C.sourceCommit,
    initialCandidateHash,finalCandidateHash,sourceStable:initialCandidateHash===finalCandidateHash,
    node:process.version,platform:process.platform,arch:process.arch,cpus:os.cpus().map(x=>({model:x.model,speedMHz:x.speed})),sourceHashes:Object.fromEntries(files.map(f=>[path.relative(__dirname,f),hash(f)])),
    methods:methods.map(x=>x[0]),records,metamorphic,invalid,scope:'Tiny deterministic functional tests; durations are not measured performance evidence.'};
  const file=path.join(__dirname,'raw',candidate?(full?'candidate_checks.json':'candidate_smoke_checks.json'):'legacy_checks.json');fs.writeFileSync(file,JSON.stringify(result,null,2));
  const domainMismatches=records.flatMap(r=>Object.entries(r.methods).filter(([n,x])=>!x.domainOutcomeMatch).map(([n,x])=>({fixture:r.id,method:n})));
  const exactFailures=records.flatMap(r=>Object.entries(r.methods).filter(([n,x])=>!n.startsWith('epsilon')&&x.comparison&&!x.comparison.exactPass).map(([n,x])=>({fixture:r.id,method:n,comparison:x.comparison})));
  const approxFailures=records.flatMap(r=>Object.entries(r.methods).filter(([n,x])=>n.startsWith('epsilon')&&x.comparison&&(!x.comparison.approximationTolerancePass||x.boundCompliance===false)).map(([n,x])=>({fixture:r.id,method:n,comparison:x.comparison,boundCompliance:x.boundCompliance})));
  console.log(JSON.stringify({file,fixtures:records.length,methods:result.methods,domainMismatches,exactFailures,approxFailures,invalid},null,2));
}
if(require.main===module)main();module.exports={comparison};
