'use strict';
// Offline byte binder. Inert on import. Never imports campaign science modules.
// Run only after terminal evidence and separate authorization to bind it.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const MAX_FETCH=16*1024*1024,MAX_RAW=805306368;
const safeName=name=>typeof name==='string'&&/^[A-Za-z0-9][A-Za-z0-9._-]*$/.test(name);
function assert(ok,message){if(!ok)throw Error(message);}
function contain(root,relative){assert(typeof relative==='string'&&!path.isAbsolute(relative),'Artifact path must be relative');const full=fs.realpathSync(path.resolve(root,relative));assert(full.startsWith(root+path.sep),'Artifact escapes campaign directory');return full;}
async function digest(file){const hash=crypto.createHash('sha256');let bytes=0;for await(const chunk of fs.createReadStream(file)){hash.update(chunk);bytes+=chunk.length;}return {bytes,sha256:hash.digest('hex')};}
async function verify(file,pin){assert(Number.isSafeInteger(pin.bytes)&&pin.bytes>=0&&/^[a-f0-9]{64}$/.test(pin.sha256),'Explicit byte/hash pin required');const actual=await digest(file);assert(actual.bytes===pin.bytes&&actual.sha256===pin.sha256,'Byte/hash mismatch: '+path.basename(file));return actual;}
function readJSON(file){assert(fs.statSync(file).size<=MAX_FETCH,'JSON exceeds browser fetch cap');return JSON.parse(fs.readFileSync(file,'utf8'));}
function assertPublicJSON(record,label){
  const inspect=value=>{if(typeof value==='string')assert(!/(?:^|[\s\"'(<])\/(?:Users|private|var|tmp|Volumes|Applications|Library|opt|usr|System)\//.test(value)&&!/https?:\/\/(?:127\.0\.0\.1|localhost)(?::\d+)?\/evidence\//.test(value),'Private path or evidence-sink URL in '+label);else if(Array.isArray(value))value.forEach(inspect);else if(value&&typeof value==='object')Object.entries(value).forEach(([key,val])=>{inspect(key);inspect(val);});};inspect(record);
}
function validatePointer(pointer){assert(typeof pointer==='string'&&(pointer===''||pointer.startsWith('/')),'Review path must be a JSON pointer');}
function resolvePointer(record,pointer){return pointer===''?record:pointer.slice(1).split('/').map(k=>k.replace(/~1/g,'/').replace(/~0/g,'~')).reduce((v,k)=>v?.[k],record);}
async function buildBindings(config,destination){
  assert(config.schema==='m31-runtime-body-binding-request/1','Unsupported binding request');
  const campaign=fs.realpathSync(config.campaignDir),target=path.resolve(destination),artifactPath=path.join(target,'viewer-artifact.json');
  assert(path.basename(campaign)==='m31-body-runtime-replication-2026-10-16','Wrong campaign directory');assert(target===path.join(campaign,'viewer'),'Destination must be this replication viewer directory');
  assert(/^[a-f0-9]{40}$/.test(config.expectedSourceCommit??''),'Actual published source commit required');
  if(fs.existsSync(artifactPath)){const old=readJSON(artifactPath);assert(old.binding?.state==='unbound','Refusing to replace an existing bound artifact');}
  assert(!fs.existsSync(path.join(target,'evidence')),'Refusing to overwrite existing evidence assets');
  const pinned=[],receipt=[],rawFiles=new Map();
  async function addPinned(pin,name,label){assert(safeName(name),'Invalid output name');assertPublicJSON(label,'report label');const file=contain(campaign,pin.path);await verify(file,pin);assert(pin.bytes<=MAX_FETCH,'Pinned report exceeds fetch cap');const record=readJSON(file);assertPublicJSON(record,name);pinned.push({name,file,pin,label});return record;}
  const freeze=await addPinned(config.freeze,'source-freeze.json','published source freeze');assert(Array.isArray(freeze.files),'Source freeze manifest required');
  const result=await addPinned(config.result,'campaign-result.json','terminal execution');assert(result.sourceCommit===config.expectedSourceCommit,'Result source identity mismatch');
  assert(result.terminal===true&&Array.isArray(result.files),'Terminal result with raw manifest is required');
  assert(Array.isArray(result.cases),'Result cases must be an array');
  let total=0;
  for(const entry of result.files){
    assert(safeName(entry.name)&&!rawFiles.has(entry.name),'Invalid or duplicate raw manifest entry');
    assert(Number.isSafeInteger(entry.bytes)&&entry.bytes>=0,'Invalid raw byte count');total+=entry.bytes;assert(total<=MAX_RAW,'Raw manifest exceeds reserved cap');
    const file=contain(campaign,'raw/'+entry.name);await verify(file,entry);rawFiles.set(entry.name,{...entry,file});receipt.push({name:entry.name,bytes:entry.bytes,sha256:entry.sha256,verification:'offline-byte-hash'});
  }
  const started=rawFiles.get('started.json');if(started){const r=readJSON(started.file);assert(r.sourceCommit===config.expectedSourceCommit&&r.freezeSha256===config.freeze.sha256,'Started source/freeze identity mismatch');}
  assert((config.reviews??[]).filter(r=>r.role==='final-external-observation').length===1,'Exactly one final externally observed authority must be pinned');
  const reviews=[];
  for(const [index,r]of (config.reviews??[]).entries()){
    assert(typeof r.label==='string'&&r.label.length>0,'Review label required');assert(['final-external-observation','saved-review-report'].includes(r.role),'Review role required');if(r.role==='final-external-observation')validatePointer(r.statusPointer);
    if(r.statusPointer!==undefined)validatePointer(r.statusPointer);if(r.detailPointer!==undefined)validatePointer(r.detailPointer);
    const record=await addPinned(r.artifact,`review-${index+1}.json`,r.label);
    if(r.role==='final-external-observation')assert(typeof resolvePointer(record,r.statusPointer)==='boolean','Final external observation status must resolve to a saved boolean');
    if(r.detailPointer!==undefined)assert(resolvePointer(record,r.detailPointer)!==undefined,'Review detail pointer does not resolve');
    reviews.push({label:r.label,role:r.role,name:`review-${index+1}.json`,...(r.statusPointer!==undefined?{statusPointer:r.statusPointer}:{}),...(r.detailPointer!==undefined?{detailPointer:r.detailPointer}:{})});
  }
  const externalReports=[];
  for(const [index,r]of (config.externalReports??[]).entries()){
    assert(typeof r.label==='string'&&r.label.length>0,'External report label required');await addPinned(r.artifact,`external-${index+1}.json`,r.label);externalReports.push({label:r.label,name:`external-${index+1}.json`});
  }
  // Select exact-layout small saved files; known full-layout partial R/Q/H buffers retain their names. Truncated files remain receipt-only.
  const selected=new Map();
  function select(name,expected){const d=rawFiles.get(name);if(!d)return null;if(expected!==undefined&&d.bytes!==expected)return null;assert(d.bytes<=MAX_FETCH,'Selected binary exceeds fetch cap');if(name.endsWith('.json'))assertPublicJSON(readJSON(d.file),name);selected.set(name,d);return {name,url:'./evidence/'+name,bytes:d.bytes,sha256:d.sha256};}
  const families=[50,500,5000,5000].map((N,i)=>{
    const id=i+1,key=`family-${id}`,files={};
    for(const [kind,suffix,size]of [['poses','originalStates.f64',17*N*8],['R','R-output.bin',480*N],['Q','Q-output.bin',480*N],['GPU','gpu-output.u32',256*N],['H','H-output.bin',288*N]]){const d=select(`${key}-${suffix}`,size)??(['R','Q','H'].includes(kind)?select(`${key}-${kind}-partial-output.bin`,size):null);if(d)files[kind]=d;}
    for(const [kind,suffix]of [['assessment','assessment.json'],['stimulus','stimulus.json'],['audit','generator-audit.json'],['admission','admission.json'],['Rstatus','R-status.json'],['Qstatus','Q-status.json'],['Hstatus','H-status.json'],['GPUapi','gpu-api.json'],['disposition','disposition.json']]){const d=select(`${key}-${suffix}`)??(kind==='assessment'?select(`${key}-assessment-partial-status.json`):null)??(['Rstatus','Qstatus','Hstatus'].includes(kind)?select(`${key}-${kind[0]}-partial-status.json`):null);if(d)files[kind]=d;}
    return {id,N,files,observedFiles:[...rawFiles.keys()].filter(name=>name.startsWith(key+'-'))};
  });
  const controls={pairCount:15,rootCount:146,files:{},assessment:select('control-assessment.json')??select('controls-assessment-partial-status.json')};
  for(const [kind,name,size]of [['pairPoses','controls-pairs-original.f64',15*16*8],['pairGPU','controls-pairs-gpu-output.u32',15*256],['pairReference','controls-reference-pairs.json'],['referenceStatus','controls-reference-status.json'],['metadata','control-metadata.json'],['rootOriginal','controls-roots-original.f64',146*16],['rootR','controls-reference-R-roots.bin',146*96],['rootQ','controls-reference-Q-roots.bin',146*96],['rootGPU','controls-roots-gpu-output.u32',146*256],['rootH','controls-handoff-output.bin',146*64],['handoffStatus','controls-handoff-status.json']]){const partial={rootR:'controls-reference-partial-Rroots.bin',rootQ:'controls-reference-partial-Qroots.bin',rootH:'controls-handoff-partial-output.bin',referenceStatus:'controls-reference-partial-status.json',handoffStatus:'controls-handoff-partial-status.json'};const d=select(name,size)??(partial[kind]?select(partial[kind],size):null);if(d)controls.files[kind]=d;}
  const constants=select('scientific-constants-and-gates.json');
  const executionEvidence={};for(const [key,name]of [['pairDispatch','controls-pairs-gpu-api.json'],['browserFailure','browser-failure-evidence.json'],['capability','capability.json'],['runtimeBefore','browser-runtime-before-launch.json'],['runtimeAfter','browser-runtime-after-launch.json'],['hostControls','controls-host-only-result.json']]){const d=select(name);if(d)executionEvidence[key]=d;}
  for(const item of pinned){assert(!selected.has(item.name),'Output name collision');receipt.push({name:item.name,bytes:item.pin.bytes,sha256:item.pin.sha256,verification:'offline-byte-hash'});}
  fs.mkdirSync(target,{recursive:true});const stage=fs.mkdtempSync(path.join(target,'.binding-'));
  try{
    const assets=path.join(stage,'evidence');fs.mkdirSync(assets);
    // Verify the copied destination too, protecting against source changes after hashing.
    for(const item of [...selected.values(),...pinned]){const dest=path.join(assets,item.name);fs.copyFileSync(item.file,dest,fs.constants.COPYFILE_EXCL);await verify(dest,item.pin??item);}
    function reportDescriptor(name){const item=pinned.find(x=>x.name===name);return {name,url:'./evidence/'+name,bytes:item.pin.bytes,sha256:item.pin.sha256};}
    const artifact={schema:'m31-runtime-body-viewer/1',binding:{state:'bound',verifiedAt:new Date().toISOString(),method:'Exact lengths and SHA-256 for all result.files and explicitly pinned reports; no scientific evaluation',rawFileCount:rawFiles.size,rawBytes:total},sourceCommit:config.expectedSourceCommit,sourceFreeze:reportDescriptor('source-freeze.json'),result:reportDescriptor('campaign-result.json'),reviews:reviews.map(({name,...r})=>({...r,artifact:reportDescriptor(name)})),externalReports:externalReports.map(({name,...r})=>({...r,artifact:reportDescriptor(name)})),families,controls,constants,executionEvidence,receipt};
    fs.writeFileSync(path.join(stage,'viewer-artifact.json'),JSON.stringify(artifact,null,2)+'\n',{flag:'wx'});
    fs.renameSync(assets,path.join(target,'evidence'));fs.renameSync(path.join(stage,'viewer-artifact.json'),artifactPath);fs.rmdirSync(stage);
    return {artifactPath,rawFileCount:rawFiles.size,browserAssets:selected.size+pinned.length};
  }catch(error){fs.rmSync(stage,{recursive:true,force:true});throw error;}
}
module.exports={buildBindings};
if(require.main===module){
  const [request,destination]=process.argv.slice(2);if(!request||!destination){console.error('Usage: node build-bindings.cjs <pinned-request.json> <viewer-directory>');process.exitCode=2;}
  else{const config=JSON.parse(fs.readFileSync(request,'utf8'));buildBindings(config,destination).then(result=>console.log(JSON.stringify(result))).catch(error=>{console.error(error.message);process.exitCode=1;});}
}
