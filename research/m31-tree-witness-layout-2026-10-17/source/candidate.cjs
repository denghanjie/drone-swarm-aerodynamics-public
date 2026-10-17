'use strict';
// One gated saved-data-only attempt. Imports no scientific producer or oracle.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const NAME='research/m31-tree-witness-layout-2026-10-17',OLD='research/m31-native-tree-browser-probe-2026-10-17';
const [rootArg,expected,commit]=process.argv.slice(2),root=path.resolve(rootArg||'.'),pkg=path.join(root,NAME),results=path.join(pkg,'results'),start=performance.now();
const MiB=1048576,need=(x,c)=>{if(!x)throw Error(c);},sha=b=>crypto.createHash('sha256').update(b).digest('hex');
const LIMITS={file:32*MiB,total:64*MiB,evidence:56*MiB,private:4*MiB,other:2*MiB,closure:2*MiB,chunk:MiB,descriptor:2*MiB};
let config,manifest,manifestMap,inputManifest,privateDir,gated=false,newBytes=0,deduplicatedBytes=0,persistenceMilliseconds=0;
const report={schema:'m31-tree-witness-layout-candidate-v1',sourceManifestSha256:expected,sourceCommit:commit,complete:false,passed:false,inputIndexPin:null,records:[],controls:[],targets:[],scope:'Saved tree witnesses only; all other full native fields are unchanged input-only evidence. No scientific query, browser timing, whole-attempt fit or numerical qualification.'};
function guard(){need(performance.now()-start<120000&&Date.now()<Date.parse(config.launchCutoffUtc),'candidate-deadline');}
function regular(file,cap=LIMITS.file){const st=fs.lstatSync(file);need(st.isFile()&&!st.isSymbolicLink()&&st.size<=cap&&fs.realpathSync(file)===file,'file-shape');return st;}
function read(relative,pin){
 need(typeof relative==='string'&&!path.isAbsolute(relative)&&!relative.split('/').includes('..'),'read-path');
 const file=path.join(root,relative);regular(file);const b=fs.readFileSync(file);
 if(pin)need(pin.path===relative&&b.length===pin.bytes&&sha(b)===pin.sha256,'input-pin');return b;
}
function source(relative){const pin=manifestMap.get(relative);need(pin,'missing-source-pin');read(relative,pin);guard();return pin;}
function json(relative,pin){return JSON.parse(read(relative,pin).toString('utf8'));}
function total(dir,priv=false){
 if(!fs.existsSync(dir))return 0;let bytes=0;
 for(const e of fs.readdirSync(dir,{withFileTypes:true})){
  const f=path.join(dir,e.name),st=fs.lstatSync(f);
  if(st.isSymbolicLink()){need(false,'output-symlink');}
  else if(st.isDirectory())bytes+=total(f,priv);
  else{need(st.isFile()&&st.size<=LIMITS.file,'output-file-cap');bytes+=st.size;}
 }
 return bytes;
}
function budget(add,section){
 guard();const evidence=total(path.join(results,'shards'))+total(path.join(results,'records')),priv=total(privateDir,true),all=total(results);
 const ledger=path.join(results,'run-attempt.json'),ledgerBytes=fs.existsSync(ledger)?fs.statSync(ledger).size:0;
 need(priv<=LIMITS.private,'private-cap');need(evidence+(section==='evidence'?add:0)<=LIMITS.evidence,'evidence-cap');
 need(all-evidence-ledgerBytes+(section==='other'?add:0)<=LIMITS.other,'other-public-cap');need(all+priv+add+LIMITS.closure<=LIMITS.total,'aggregate-cap');
}
function write(relative,bytes,section){
 need(bytes.length<=LIMITS.file,'file-cap');budget(bytes.length,section);const file=path.join(root,relative),fd=fs.openSync(file,'wx',0o600);
 try{fs.writeFileSync(fd,bytes);fs.fsyncSync(fd);}finally{fs.closeSync(fd);}const dir=fs.openSync(path.dirname(file),'r');try{fs.fsyncSync(dir);}finally{fs.closeSync(dir);}
 newBytes+=bytes.length;return {path:relative,bytes:bytes.length,sha256:sha(bytes)};
}
function put(value){
 const begin=performance.now(),bytes=Buffer.from(value);need(bytes.length>0&&bytes.length<=LIMITS.chunk,'chunk-cap');
 const hash=sha(bytes),relative=NAME+'/results/shards/'+hash+'.bin',file=path.join(root,relative);let pin;
 if(fs.existsSync(file)){regular(file,LIMITS.chunk);const old=fs.readFileSync(file);need(old.length===bytes.length&&old.equals(bytes),'reuse-bytes');deduplicatedBytes+=bytes.length;pin={path:relative,bytes:bytes.length,sha256:hash};}
 else pin=write(relative,bytes,'evidence');persistenceMilliseconds+=performance.now()-begin;return pin;
}
function getOld(pin){
 need(pin.path===OLD+'/results/shards/'+pin.sha256+'.bin'&&pin.bytes>0&&pin.bytes<=LIMITS.chunk&&/^[a-f0-9]{64}$/.test(pin.sha256),'old-chunk-shape');
 const frozen=manifestMap.get(pin.path);need(frozen&&frozen.bytes===pin.bytes&&frozen.sha256===pin.sha256,'old-chunk-manifest');guard();return read(pin.path,pin);
}
function getNew(pin){need(pin.path===NAME+'/results/shards/'+pin.sha256+'.bin'&&pin.bytes>0&&pin.bytes<=LIMITS.chunk,'new-chunk-shape');guard();return read(pin.path,pin);}
async function main(){
 need(process.argv.length===5&&/^[a-f0-9]{64}$/.test(expected)&&/^[a-f0-9]{40}$/.test(commit),'arguments');
 config=json(NAME+'/config.json');need(config.executionAllowed===true&&config.authorization&&Date.now()<Date.parse(config.launchCutoffUtc)&&process.env.RESEARCH_EXECUTION_CONTEXT==='tool-require-escalated'&&process.env.RESEARCH_STAGE==='candidate'&&process.env.RESEARCH_CHILD_BUDGET_MILLISECONDS==='120000'&&!process.env.NODE_OPTIONS&&!process.env.NODE_PATH&&process.execArgv.length===0,'authorization');
 const attempt=json(NAME+'/results/run-attempt.json'),token=process.env.RESEARCH_RUN_TOKEN;
 need(typeof token==='string'&&attempt.runTokenSha256===sha(token)&&attempt.status==='running'&&attempt.stages?.candidate?.status==='started'&&attempt.sourceCommit===commit&&attempt.sourceManifestSha256===expected,'supervisor-binding');
 const manifestBytes=read(NAME+'/source-manifest.json');need(sha(manifestBytes)===expected,'manifest-sha');manifest=JSON.parse(manifestBytes);manifestMap=new Map(manifest.files.map(p=>[p.path,p]));need(manifestMap.size===manifest.files.length,'manifest-duplicates');
 for(const relative of ['config.json','source/candidate.cjs','source/layout.cjs','source/transport.cjs','input-index.json','input-manifest.json'])source(NAME+'/'+relative);
 source(OLD+'/source/transport.cjs');const runtime=fs.readFileSync(fs.realpathSync(process.execPath));need(runtime.length===manifest.runtime.node.bytes&&sha(runtime)===manifest.runtime.node.sha256,'runtime-pin');
 const publication=json(NAME+'/source-publication.json');need(publication.commit===commit&&publication.manifestSha256===expected&&publication.manifestPath===NAME+'/source-manifest.json'&&publication.manifestBytes===manifestBytes.length&&publication.verifiedFilePins===manifest.files.length&&publication.remoteBytesEqualLocal===true&&publication.committedBytesEqualLocal===true&&Date.parse(publication.verifiedUtc)<=Date.parse(attempt.startedUtc),'publication-binding');
 privateDir=fs.realpathSync(process.env.RESEARCH_PRIVATE_LOG_DIR);need(path.isAbsolute(privateDir)&&privateDir!==root&&!privateDir.startsWith(root+path.sep),'private-path');
 need(!fs.existsSync(path.join(results,'candidate.json'))&&!fs.existsSync(path.join(results,'shards'))&&!fs.existsSync(path.join(results,'records')),'single-attempt');
 const inputIndex=json(NAME+'/input-index.json',source(NAME+'/input-index.json'));inputManifest=json(NAME+'/input-manifest.json',source(NAME+'/input-manifest.json'));
 need(inputIndex.schema==='m31-tree-witness-layout-inputs-v1'&&inputIndex.sourcePackage===OLD&&inputIndex.records.length===156&&inputManifest.schema==='m31-tree-witness-layout-input-manifest-v1','input-schema');
 report.inputIndexPin=source(NAME+'/input-index.json');
 for(const p of inputManifest.files){const q=manifestMap.get(p.path);need(q&&q.bytes===p.bytes&&q.sha256===p.sha256,'input-manifest-binding');source(p.path);}
 const saved=json(inputIndex.savedTransportPin.path,inputIndex.savedTransportPin),journal=read(inputIndex.browserJournalPin.path,inputIndex.browserJournalPin).toString('utf8').trimEnd().split('\n').map(s=>JSON.parse(s)),priorAttempt=json(inputIndex.sourceAttemptPin.path,inputIndex.sourceAttemptPin);
 const natives=journal.filter(r=>r.kind==='native');need(saved.complete===true&&saved.passed===true&&saved.records.length===126&&natives.length===30&&priorAttempt.status==='failed','fixed-corpus');
 const oldTransport=require('../../m31-native-tree-browser-probe-2026-10-17/source/transport.cjs'),transport=require('./transport.cjs'),layout=require('./layout.cjs');
 fs.mkdirSync(path.join(results,'shards'));fs.mkdirSync(path.join(results,'records'));gated=true;
 const reject=fn=>{try{fn();return false;}catch(_){return true;}};
 function control(id,fn){guard();const passed=fn()===true;report.controls.push({id,passed});need(passed,'candidate-control-'+id);}
 control('literal-selection',()=>layout.selected([1],5000).kind==='literal');
 control('run-selection',()=>layout.selected(Array.from({length:100},(_,i)=>i),5000).kind==='runs');
 control('bitmap-boundary-roundtrip',()=>{const actual=[0,1,63,64,69],v=layout.selected(actual,70);return v.kind==='bitmap'&&layout.equal(v.data,['8000000000000003','0000000000000021'])&&layout.equal(layout.expandNew(v,70),actual);});
 control('empty-roundtrip',()=>layout.equal(layout.expandNew(layout.selected([],0),0),[]));
 control('duplicate-source-rejected',()=>reject(()=>layout.selected([1,1],70)));
 control('bitmap-tail-rejected',()=>reject(()=>layout.expandNew({kind:'bitmap',count:5,data:['8000000000000003','8000000000000021']},70)));
 control('wrong-count-rejected',()=>reject(()=>layout.expandNew({kind:'literal',count:2,data:[1]},5000)));
 control('noncanonical-choice-rejected',()=>reject(()=>layout.expandNew({kind:'literal',count:100,data:Array.from({length:100},(_,i)=>i)},5000)));
 for(let index=0;index<156;index++){
  guard();const row=inputIndex.records[index],savedRow=index<126?saved.records[index]:null,journalRow=index<126?null:natives[index-126],wanted=savedRow?savedRow.recordPin:journalRow.recordPin;
  need(row.index===index&&row.origin===(index<126?'saved':'browser')&&row.sourceSequence===(index<126?index:journalRow.sequence)&&layout.equal(row.recordPin,wanted),'input-order');source(row.recordPin.path);
  const descriptor=json(row.recordPin.path,row.recordPin);oldTransport.validateDescriptor(descriptor);const body=await oldTransport.decodeRecord(descriptor,async p=>getOld(p));
  need(['F','H0','H'].includes(body.method),'method');const present=Object.hasOwn(body,'tree'),treeState=!present?'absent':body.tree===null?'null':'object';
  const originalTreeBinaryBytes=present?descriptor.fields.find(f=>f.key==='tree').stream.binaryBytes:0;
  const resultRow={index,origin:row.origin,sourceSequence:row.sourceSequence,sourceRecordPin:row.recordPin,method:body.method,treeState,recordPin:null,originalTreeBinaryBytes,newTreeBinaryBytes:0,logicalRoundtrip:false};
  if(present){
   const encoded=layout.encode(body.tree,guard),roundtrip=layout.decode(encoded,guard);need(layout.equal(body.tree,roundtrip),'tree-logical-roundtrip');
   const output=await transport.encodeRecord({tree:encoded},async b=>put(b),guard),decoded=await transport.decodeRecord(output,async p=>getNew(p));need(layout.equal(encoded,decoded.tree)&&layout.equal(body.tree,layout.decode(decoded.tree,guard)),'transport-logical-roundtrip');
   const bytes=Buffer.from(JSON.stringify(output)+'\n');need(bytes.length<=LIMITS.descriptor,'descriptor-cap');resultRow.recordPin=write(NAME+'/results/records/'+String(index).padStart(3,'0')+'-tree.json',bytes,'evidence');resultRow.newTreeBinaryBytes=output.fields[0].stream.binaryBytes;
   if(row.origin==='browser'&&body.method==='H'&&body.tree?.n===5000){const passed=resultRow.newTreeBinaryBytes<=0.5*originalTreeBinaryBytes;report.targets.push({index,sourceSequence:row.sourceSequence,originalTreeBinaryBytes,newTreeBinaryBytes:resultRow.newTreeBinaryBytes,maximumRatio:0.5,passed});}
  }
  resultRow.logicalRoundtrip=true;report.records.push(resultRow);
 }
 need(report.records.length===156&&report.targets.length===2&&report.targets[0].sourceSequence===60&&report.targets[1].sourceSequence===63,'completion-count');
 need(report.targets.every(t=>t.passed),'saved-large-h-size-target');
 for(const p of inputManifest.files){source(p.path);}guard();report.inputsPreserved=true;report.complete=true;report.passed=true;
}
main().catch(error=>{report.complete=false;report.passed=false;report.reason={code:/^[a-zA-Z0-9-]{1,100}$/.test(error.message||'')?error.message:'candidate-exception',errorClass:error.constructor?.name||'Error'};process.stderr.write(String(error.stack||error)+'\n');process.exitCode=1;}).finally(()=>{
 if(!gated)return;
 try{
  report.transport={newBytes,deduplicatedBytes,persistenceMilliseconds,scope:'Actual byte equality required for reuse; timings cover saved-data encoding/persistence only.'};report.wallMilliseconds=performance.now()-start;
  const bytes=Buffer.from(JSON.stringify(report)+'\n');need(bytes.length<=LIMITS.descriptor,'candidate-index-cap');write(NAME+'/results/candidate.json',bytes,'other');guard();
 }catch(error){process.stderr.write('candidate-finalization-failure\n');process.exitCode=1;}
});
