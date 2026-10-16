'use strict';
// One bounded, synchronous allocation. This file has not run before source publication.
const fs=require('node:fs'),path=require('node:path');
const spec=require('./spec.json'),contract=require('./result-contract.json');
const adapter=require('./adapter.cjs'),methods=require('./methods.cjs'),C=require('./canonical.cjs');
const output=process.env.RESEARCH_RESULT_PATH,manifestPath=process.env.RESEARCH_SOURCE_MANIFEST_PATH;
if(!output||!manifestPath||path.basename(output)!=='timing-index.json')throw Error('Required frozen output/manifest path');
const limits=contract.wireLimits,root=path.dirname(output),origin=process.hrtime.bigint();
const now=()=>process.hrtime.bigint()-origin;
const specSha256=C.sha(fs.readFileSync(path.join(__dirname,'spec.json'))),sourceManifestSha256=C.sha(fs.readFileSync(manifestPath));
const runtime={node:process.version,v8:process.versions.v8,platform:process.platform,arch:process.arch};
const sourceSha256=Object.fromEntries(contract.sourceFiles.map(n=>[n,C.sha(fs.readFileSync(path.join(__dirname,n)))]));
const constants=adapter.constantBits;
const serialize=v=>C.encode(v)+'\n';
function capText(s,n,label){if(Buffer.byteLength(s)>n)throw Error('wire-cap:'+label);return s;}
function cap(v,n,label){capText(C.encode(v),n,label);}
function strings(v,n,label){if(typeof v==='string'&&v.length>n)throw Error('wire-string:'+label);if(v&&typeof v==='object')for(const x of Object.values(v))strings(x,n,label);}
function checkRecord(m){
 strings(m,4096,'general');
 for(const n of m.assembly.tree?.nodes??[]){cap(n,limits.treeNodeBytes,'tree-node');for(const b of [n.center,n.axis])for(const ends of b)for(const q of ends)if(q.n.length>limits.treeNumeratorChars||q.d.length>limits.treeDenominatorChars)throw Error('wire-tree-rational');}
 for(const q of m.assembly.queries)for(const t of q.terminals)for(const e of t.entries??[]){cap(e,limits.nonzeroEntryBytes,'nonzero-entry');if(e.result.coefficient)strings(e.result.coefficient,limits.fixed96IntegerChars,'coefficient');}
 for(const r of m.certificate?.rows??[]){cap(r,limits.certificateRowBytes,'certificate-row');strings(r,limits.fixed96IntegerChars,'certificate-row');}
 for(const l of m.certificate?.loads??[]){cap(l,limits.loadRecordBytes,'load');strings(l.bounds,limits.fixed96IntegerChars,'load-bounds');strings(l.error,limits.fixed96IntegerChars,'load-error');strings(l.candidate,limits.candidateLoadRationalIntegerChars,'candidate-load');}
 if(m.certificate){strings(m.certificate.Kbar,limits.fixed96IntegerChars,'Kbar');strings(m.certificate.maxErrors,limits.fixed96IntegerChars,'maxErrors');}
}
function durableFile(filename,text,limit){
 capText(text,limit,'file');const fd=fs.openSync(filename,'wx');
 try{fs.writeFileSync(fd,text);fs.fsyncSync(fd);}finally{fs.closeSync(fd);}
 const dir=fs.openSync(path.dirname(filename),'r');try{fs.fsyncSync(dir);}finally{fs.closeSync(dir);}
 return {path:'results/'+path.relative(root,filename).split(path.sep).join('/'),bytes:Buffer.byteLength(text),sha256:C.sha(text)};
}
fs.mkdirSync(path.join(root,'scenes'));
fs.mkdirSync(path.join(root,'anomalies'));
const journal=fs.openSync(output+'.jsonl','wx');let journalBytes=0,eventSequence=0,scienceBytes=0;
function append(type,payload){
 const text=serialize({schema:'m31-screening-cost-journal-v1',eventSequence,type,payload});
 capText(text,limits.journalLineBytes,'journal-line');if(journalBytes+Buffer.byteLength(text)>limits.journalBytes)throw Error('wire-cap:journal');
 fs.writeFileSync(journal,text);fs.fsyncSync(journal);journalBytes+=Buffer.byteLength(text);eventSequence++;
}
const interval=(a,b)=>({startNs:String(a),endNs:String(b),totalNs:String(b-a)});
function common(m,input){
 const entries=[];
 for(const q of m.assembly.queries)for(const t of q.terminals)for(const e of t.entries??[])if(e.result.status==='positive')entries.push({i:q.i,r:q.r,j:e.j,result:e.result});
 entries.sort((a,b)=>a.i-b.i||a.r-b.r||a.j-b.j);
 return {prepared:m.prepared,result:m.result,canonicalPositiveEntries:entries.map(e=>({...e,i:input.drones[e.i].id,j:input.drones[e.j].id})),solve:m.solve,certificate:m.certificate};
}
function digestRecord(m,input,sceneId,rawInputSha256){
 const a=now(),context={specSha256,sourceManifestSha256,sceneId,rawInputSha256};
 const methodText=C.encode({domain:'m31-screening-cost/method/v1',...context,method:m.name,scientific:m});
 const commonText=C.encode({domain:'m31-screening-cost/common/v1',...context,scientific:common(m,input)});
 const b=now(),scientificDigest=C.sha(methodText),commonDigest=C.sha(commonText),c=now();
 return {scientificDigest,commonDigest,harnessTiming:{...interval(a,c),serializationNs:String(b-a),hashNs:String(c-b)}};
}
const gcd=(a,b)=>{a=a<0n?-a:a;while(b){const t=a%b;a=b;b=t;}return a;};
function frac(n,d=1n){if(d<=0n)throw Error('summary-denominator');const g=gcd(n,d);return {n:String(n/g),d:String(d/g)};}
const compare=(a,b)=>{const q=BigInt(a.n)*BigInt(b.d)-BigInt(b.n)*BigInt(a.d);return q<0n?-1:q>0n?1:0;};
function median(xs){const a=xs.slice().sort(compare),x=a[1],y=a[2];return frac(BigInt(x.n)*BigInt(y.d)+BigInt(y.n)*BigInt(x.d),2n*BigInt(x.d)*BigInt(y.d));}
function summarize(sceneId,trials){
 const pairs=[1,2,3,4].map(repetition=>{const pair=trials.filter(t=>t.phase==='measured'&&t.repetition===repetition),a=pair.find(t=>t.method==='complete'),b=pair.find(t=>t.method==='hierarchy');return {repetition,pairOrder:a.pairOrder,completeNs:a.timing.totalNs,hierarchyNs:b.timing.totalNs,ratio:frac(BigInt(a.timing.totalNs),BigInt(b.timing.totalNs))};});
 const a=median(pairs.map(p=>frac(BigInt(p.completeNs)))),b=median(pairs.map(p=>frac(BigInt(p.hierarchyNs))));
 return {sceneId,pairs,completeMedianNs:a,hierarchyMedianNs:b,medianPairedRatio:median(pairs.map(p=>p.ratio)),ratioOfMedians:frac(BigInt(a.n)*BigInt(b.d),BigInt(a.d)*BigInt(b.n))};
}
const scenes=[],trials=[],summaries=[];
let sceneIndex=null,trialSequence=null,failure={previousDigest:null,currentDigest:null,offendingPath:null,offendingBytes:null,offendingSha256:null};
function mismatch(sceneId,name,scientific,previousDigest,currentDigest){
 const text=serialize({schema:'m31-screening-cost-anomaly-v1',sceneId,method:name,sequence:trialSequence,previousDigest,currentDigest,scientific});
 const required=Buffer.byteLength(text),available=Math.min(limits.sceneFileBytes,limits.scientificShardsAndAnomalyBytes-scienceBytes);
 failure={previousDigest,currentDigest,offendingPath:null,offendingBytes:required,offendingSha256:C.sha(text)};
 if(required>available)throw Error('anomaly-retention-resource:required='+required+',available='+available);
 const pin=durableFile(path.join(root,'anomalies','first-mismatch.json'),text,limits.sceneFileBytes);scienceBytes+=pin.bytes;
 failure.offendingPath=pin.path;throw Error('scientific-digest-mismatch');
}
try{
 append('run-start',{specSha256,sourceManifestSha256,runtime,sourceSha256,constants});
 for(sceneIndex=0;sceneIndex<spec.scenes.length;sceneIndex++){
  const scene=spec.scenes[sceneIndex],a=now(),input=methods.makeInput(scene),b=now(),inputConversionTiming=interval(a,b);
  const rawInputSha256=C.sha(C.encode({domain:'m31-screening-cost/raw-input/v1',sceneId:scene.id,input}));
  append('input-ready',{sceneIndex,sceneId:scene.id,rawInputSha256,inputConversionTiming});
  const observed={},representatives={},representativeMeta={},sceneTrials=[];let descriptor=null;
  for(let pairIndex=0;pairIndex<5;pairIndex++){
   const pairOrder=['AB','AB','BA','BA','AB'][pairIndex];
   for(let pairPosition=0;pairPosition<2;pairPosition++){
    trialSequence=trials.length;const name=pairOrder[pairPosition]==='A'?'complete':'hierarchy',offsets={};
    let hookIndex=0;const start=now();
    const record=methods.method(input,name,label=>{if(label!==['prepared','spatial','assembled'][hookIndex++])throw Error('phase-hook-order');offsets[label]=now()-start;});
    const end=now();offsets.completed=end-start;
    if(hookIndex!==3||offsets.completed<=0n||offsets.prepared<0n||offsets.spatial<offsets.prepared||offsets.assembled<offsets.spatial||offsets.completed<offsets.assembled)throw Error('phase-hook-partition');
    const timing={...interval(start,end),offsetsNs:Object.fromEntries(Object.entries(offsets).map(([k,v])=>[k,String(v)])),stagesNs:{preparation:String(offsets.prepared),spatial:String(offsets.spatial-offsets.prepared),assembly:String(offsets.assembled-offsets.spatial),admissionSolveCertificate:String(offsets.completed-offsets.assembled)}};
    const digest=digestRecord(record,input,scene.id,rawInputSha256);
    const trial={sequence:trialSequence,sceneIndex,sceneId:scene.id,phase:pairIndex===0?'warmup':'measured',repetition:pairIndex,pairOrder,pairPosition,method:name,timing,...digest,work:{...record.assembly.work}};
    // Journal the completed call before qualification, including the first mismatch.
    append('trial-complete',trial);trials.push(trial);sceneTrials.push(trial);
    if(observed[name]&&observed[name]!==digest.scientificDigest)mismatch(scene.id,name,record,observed[name],digest.scientificDigest);
    observed[name]=digest.scientificDigest;checkRecord(record);
    if(pairIndex===1){representatives[name]=record;representativeMeta[name]={method:name,trialSequence,scientificDigest:digest.scientificDigest,commonDigest:digest.commonDigest};}
   }
   if(pairIndex===1){
    const shard={schema:'m31-screening-cost-scene-v1',specId:spec.id,specSha256,sourceManifestSha256,id:scene.id,rawInputSha256,input,methods:spec.methods.map(n=>representatives[n])};
    const text=serialize(shard);if(scienceBytes+Buffer.byteLength(text)>limits.scientificShardsAndAnomalyBytes)throw Error('wire-cap:scientific-shards');
    const pin=durableFile(path.join(root,'scenes',scene.id+'.json'),text,limits.sceneFileBytes);scienceBytes+=pin.bytes;
    descriptor={sceneIndex,id:scene.id,...pin,rawInputSha256,representatives:spec.methods.map(n=>representativeMeta[n]),inputConversionTiming};
    append('representative-shard',descriptor);
   }
  }
  scenes.push(descriptor);summaries.push(summarize(scene.id,sceneTrials));
  append('scene-complete',{sceneIndex,sceneId:scene.id,firstSequence:sceneIndex*10,lastSequence:sceneIndex*10+9,sha256:descriptor.sha256});
 }
 if(trials.length!==60||scenes.length!==6)throw Error('allocation-count');
 const result={schema:'m31-screening-cost-result-v1',specId:spec.id,specSha256,sourceManifestSha256,runtime,sourceSha256,constants,clock:'process.hrtime.bigint',recordedHarnessScope:contract.trialProtocol.recordedHarnessScope,scenes,trials,summaries};
 const pin=durableFile(output,serialize(result),limits.resultIndexBytes);
 append('run-complete',{resultPath:pin.path,resultBytes:pin.bytes,resultSha256:pin.sha256,trialCount:trials.length,sceneCount:scenes.length});
 console.log(C.encode({status:'kernel-complete-awaiting-independent-qualification',trials:trials.length,scenes:scenes.length,scienceBytes}));
}catch(e){
 const reason=String(e.message||e).slice(0,limits.maxErrorChars);
 append('run-failed',{reason,sceneIndex,trialSequence,...failure});throw e;
}finally{fs.closeSync(journal);}
