'use strict';
// Saved-data codec qualification only: never require a scientific producer.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const NAME='research/m31-native-tree-browser-probe-2026-10-17',OLD='research/m31-native-tree-design-2026-10-17/results/evidence/';
const [rootArg,expected,commit]=process.argv.slice(2),root=path.resolve(rootArg||'.'),pkg=path.join(root,NAME),start=performance.now();
const need=(v,c)=>{if(!v)throw Error(c);},sha=b=>crypto.createHash('sha256').update(b).digest('hex');
let config,store,gated=false;const result={schema:'m31-saved-transport-v1',sourceManifestSha256:expected,sourceCommit:commit,complete:false,passed:false,records:[],codecControls:[],scope:'126 frozen encoded native payloads only; no new native queries or numerical kernel imports'};
function guard(){need(performance.now()-start<15000&&Date.now()<Date.parse(config.launchCutoffUtc),'saved-codec-deadline');}
function identity(file){const b=fs.readFileSync(file);guard();return {bytes:b.length,sha256:sha(b)};}
function load(file){need(fs.statSync(file).size<=32*1048576,'json-cap');return JSON.parse(fs.readFileSync(file,'utf8'));}
function pin(relative,manifest){const p=manifest.files.find(p=>p.path===relative);need(p&&fs.realpathSync(path.join(root,relative))===path.join(root,relative),'source-pin-path');const actual=identity(path.join(root,relative));need(actual.bytes===p.bytes&&actual.sha256===p.sha256,'source-pin');return p;}
async function main(){
 need(process.argv.length===5&&/^[a-f0-9]{64}$/.test(expected)&&/^[a-f0-9]{40}$/.test(commit),'arguments');config=load(path.join(pkg,'config.json'));
 need(config.executionAllowed===true&&config.authorization&&Date.now()<Date.parse(config.launchCutoffUtc)&&process.env.RESEARCH_EXECUTION_CONTEXT==='tool-require-escalated'&&process.env.RESEARCH_STAGE==='saved-validation'&&process.env.RESEARCH_CHILD_BUDGET_MILLISECONDS==='15000'&&!process.env.NODE_OPTIONS&&!process.env.NODE_PATH&&process.execArgv.length===0,'authorization');
 const attempt=load(path.join(pkg,'results/run-attempt.json')),token=process.env.RESEARCH_RUN_TOKEN;need(typeof token==='string'&&attempt.runTokenSha256===sha(token)&&attempt.status==='running'&&attempt.stages?.['saved-validation']?.status==='started'&&attempt.sourceCommit===commit&&attempt.sourceManifestSha256===expected,'supervisor-binding');
 const manifestBytes=fs.readFileSync(path.join(pkg,'source-manifest.json'));need(sha(manifestBytes)===expected,'manifest-sha');const manifest=JSON.parse(manifestBytes);
 for(const rel of ['config.json','source/qualify-transport.cjs','source/transport.cjs','source/transport-store.cjs','source/compact-codec.cjs'])pin(NAME+'/'+rel,manifest);
 const runtime=identity(fs.realpathSync(process.execPath));need(runtime.bytes===manifest.runtime.node.bytes&&runtime.sha256===manifest.runtime.node.sha256,'runtime-pin');
 const publication=load(path.join(pkg,'source-publication.json'));need(publication.commit===commit&&publication.manifestSha256===expected&&publication.remoteBytesEqualLocal===true&&publication.committedBytesEqualLocal===true&&Date.parse(publication.verifiedUtc)<=Date.parse(attempt.startedUtc),'publication-binding');
 need(!fs.existsSync(path.join(pkg,'results/saved-transport.json')),'single-use-saved-codec');
 const transport=require('./transport.cjs'),codec=require('./compact-codec.cjs');store=require('./transport-store.cjs').createStore(root,fs.realpathSync(process.env.RESEARCH_PRIVATE_LOG_DIR),guard);gated=true;
 const originals=manifest.files.filter(p=>p.path.startsWith(OLD)&&/^\d{3}-.+-(F|H0|H)\.json$/.test(p.path.slice(OLD.length))).sort((a,b)=>{const x=/^(\d{3})-.+-(F|H0|H)\.json$/.exec(a.path.slice(OLD.length)),y=/^(\d{3})-.+-(F|H0|H)\.json$/.exec(b.path.slice(OLD.length));return Number(x[1])-Number(y[1])||({F:0,H0:1,H:2}[x[2]]-{F:0,H0:1,H:2}[y[2]]);});need(originals.length===126,'fixed-saved-record-count');
 for(const sourceOldPin of originals){
  guard();pin(sourceOldPin.path,manifest);const original=load(path.join(root,sourceOldPin.path)),body={...original};if(Object.hasOwn(original,'tree'))body.tree=codec.compactLegacyTree(original.tree);
  const suffix=sourceOldPin.path.slice(OLD.length),match=/^(\d{3})-(.+)-(F|H0|H)\.json$/.exec(suffix);need(match&&original.method===match[3],'saved-method-binding');
  const descriptor=await transport.encodeRecord(body,async bytes=>store.put(bytes),guard),decoded=await transport.decodeRecord(descriptor,async p=>store.get(p));need(JSON.stringify(body)===JSON.stringify(decoded),'saved-transport-roundtrip');
  const recordPin=store.record('saved-records',suffix.slice(0,-5),descriptor);result.records.push({caseId:match[2],method:match[3],sourceOldPin,recordPin});
 }
 function control(id,fn){guard();const pass=fn()===true;result.codecControls.push({id,pass});need(pass,'saved-codec-control-'+id);}
 const reject=(chunks,descriptor)=>{try{transport.unpackValue(chunks,descriptor);return false;}catch(_){return true;}};
 control('literal-word-and-signed-zero',()=>{const p=transport.packValue(['7ff8000000000000',-0,0,1.25],guard),v=transport.unpackValue(p.chunks,p);return v[0]==='7ff8000000000000'&&Object.is(v[1],-0)&&Object.is(v[2],0)&&v[3]===1.25;});
 control('unknown-tag-rejected',()=>reject([Uint8Array.of(255)],{binaryBytes:1,elements:1}));
 control('trailing-byte-rejected',()=>reject([Uint8Array.of(0,0)],{binaryBytes:2,elements:1}));
 control('truncated-word-rejected',()=>reject([Uint8Array.of(7,0)],{binaryBytes:2,elements:1}));
 control('empty-optimized-array-rejected',()=>reject([Uint8Array.of(8,0,0,0,0)],{binaryBytes:5,elements:1}));
 control('fixed-boundary-word-roundtrip',()=>{const words=Array(131073).fill('3ff0000000000000'),p=transport.packValue(words,guard),v=transport.unpackValue(p.chunks,p);return p.chunks.length===2&&p.chunks[0].length===1048576&&v.length===words.length&&v.every((w,i)=>w===words[i]);});
 for(const p of originals)pin(p.path,manifest);
 result.complete=true;result.passed=true;result.transport=store.stats();
}
main().catch(error=>{result.reason={code:/^[a-z0-9-]{1,100}$/.test(error.message||'')?error.message:'saved-codec-exception',errorClass:error.constructor?.name||'Error'};process.stderr.write(String(error.stack||error)+'\n');process.exitCode=1;}).finally(()=>{
 if(!gated)return;try{const bytes=Buffer.from(JSON.stringify(result)+'\n');need(bytes.length<=2*1048576,'saved-index-cap');store.budget(bytes.length);const f=fs.openSync(path.join(pkg,'results/saved-transport.json'),'wx',0o600);try{fs.writeFileSync(f,bytes);fs.fsyncSync(f);}finally{fs.closeSync(f);}guard();}catch(_){process.stderr.write('saved-codec-finalization-failure\n');process.exitCode=1;}
});
