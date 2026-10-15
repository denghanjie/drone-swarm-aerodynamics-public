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
  const inspect=value=>{if(typeof value==='string')assert(!/\/(?:Users|private|var|tmp|Volumes|Applications|Library|opt|usr|System)\//.test(value)&&!/https?:\/\/(?:127\.0\.0\.1|localhost)(?::\d+)?\/evidence\//.test(value),'Private path or evidence-sink URL in '+label);else if(Array.isArray(value))value.forEach(inspect);else if(value&&typeof value==='object')Object.entries(value).forEach(([key,val])=>{inspect(key);inspect(val);});};inspect(record);
}
function validatePointer(pointer){assert(typeof pointer==='string'&&(pointer===''||pointer.startsWith('/')),'Review path must be a JSON pointer');}
async function buildBindings(config,destination){
  assert(config.schema==='m31-body-binding-request/1','Unsupported binding request');
  const campaign=fs.realpathSync(config.campaignDir),target=path.resolve(destination),artifactPath=path.join(target,'viewer-artifact.json');
  assert(target!==campaign,'Destination must be a viewer directory');
  if(fs.existsSync(artifactPath)){const old=readJSON(artifactPath);assert(old.binding?.state==='unbound','Refusing to replace an existing bound artifact');}
  assert(!fs.existsSync(path.join(target,'evidence')),'Refusing to overwrite existing evidence assets');
  const pinned=[],receipt=[],rawFiles=new Map();
  async function addPinned(pin,name,label){assert(safeName(name),'Invalid output name');assertPublicJSON(label,'report label');const file=contain(campaign,pin.path);await verify(file,pin);assert(pin.bytes<=MAX_FETCH,'Pinned report exceeds fetch cap');const record=readJSON(file);assertPublicJSON(record,name);pinned.push({name,file,pin,label});return record;}
  const result=await addPinned(config.result,'campaign-result.json','terminal execution');
  assert(result.terminal===true&&Array.isArray(result.files),'Terminal result with raw manifest is required');
  assert(Array.isArray(result.cases),'Result cases must be an array');
  let total=0;
  for(const entry of result.files){
    assert(safeName(entry.name)&&!rawFiles.has(entry.name),'Invalid or duplicate raw manifest entry');
    assert(Number.isSafeInteger(entry.bytes)&&entry.bytes>=0,'Invalid raw byte count');total+=entry.bytes;assert(total<=MAX_RAW,'Raw manifest exceeds reserved cap');
    const file=contain(campaign,'raw/'+entry.name);await verify(file,entry);rawFiles.set(entry.name,{...entry,file});receipt.push({name:entry.name,bytes:entry.bytes,sha256:entry.sha256,verification:'offline-byte-hash'});
  }
  const reviews=[];
  for(const [index,r]of (config.reviews??[]).entries()){
    assert(typeof r.label==='string'&&r.label.length>0,'Review label required');
    if(r.statusPointer!==undefined)validatePointer(r.statusPointer);if(r.detailPointer!==undefined)validatePointer(r.detailPointer);
    await addPinned(r.artifact,`review-${index+1}.json`,r.label);
    reviews.push({label:r.label,name:`review-${index+1}.json`,...(r.statusPointer!==undefined?{statusPointer:r.statusPointer}:{}),...(r.detailPointer!==undefined?{detailPointer:r.detailPointer}:{})});
  }
  const externalReports=[];
  for(const [index,r]of (config.externalReports??[]).entries()){
    assert(typeof r.label==='string'&&r.label.length>0,'External report label required');await addPinned(r.artifact,`external-${index+1}.json`,r.label);externalReports.push({label:r.label,name:`external-${index+1}.json`});
  }
  // Select only exact-layout small saved files. Partial buffers remain in the receipt.
  const selected=new Map();
  function select(name,expected){const d=rawFiles.get(name);if(!d)return null;if(expected!==undefined&&d.bytes!==expected)return null;assert(d.bytes<=MAX_FETCH,'Selected binary exceeds fetch cap');if(name.endsWith('.json'))assertPublicJSON(readJSON(d.file),name);selected.set(name,d);return {name,url:'./evidence/'+name,bytes:d.bytes,sha256:d.sha256};}
  const families=[50,500,5000,5000].map((N,i)=>{
    const id=i+1,key=`family-${id}`,files={};
    for(const [kind,suffix,size]of [['poses','originalStates.f64',17*N*8],['R','R-output.bin',480*N],['GPU','gpu-output.u32',256*N]]){const d=select(`${key}-${suffix}`,size);if(d)files[kind]=d;}
    return {id,N,files,observedFiles:[...rawFiles.keys()].filter(name=>name.startsWith(key+'-'))};
  });
  const controls={pairCount:15,rootCount:146,files:{},assessment:select('control-assessment.json')};
  for(const [kind,name,size]of [['pairPoses','controls-pairs-original.f64',15*16*8],['pairGPU','controls-pairs-gpu-output.u32',15*256],['pairReference','controls-reference-pairs.json'],['referenceStatus','controls-reference-status.json'],['metadata','control-metadata.json']]){const d=select(name,size);if(d)controls.files[kind]=d;}
  for(const item of pinned){assert(!selected.has(item.name),'Output name collision');receipt.push({name:item.name,bytes:item.pin.bytes,sha256:item.pin.sha256,verification:'offline-byte-hash'});}
  fs.mkdirSync(target,{recursive:true});const stage=fs.mkdtempSync(path.join(target,'.binding-'));
  try{
    const assets=path.join(stage,'evidence');fs.mkdirSync(assets);
    // Verify the copied destination too, protecting against source changes after hashing.
    for(const item of [...selected.values(),...pinned]){const dest=path.join(assets,item.name);fs.copyFileSync(item.file,dest,fs.constants.COPYFILE_EXCL);await verify(dest,item.pin??item);}
    function reportDescriptor(name){const item=pinned.find(x=>x.name===name);return {name,url:'./evidence/'+name,bytes:item.pin.bytes,sha256:item.pin.sha256};}
    const artifact={schema:'m31-body-viewer/1',binding:{state:'bound',verifiedAt:new Date().toISOString(),method:'Exact lengths and SHA-256 for all result.files and explicitly pinned reports; no scientific evaluation',rawFileCount:rawFiles.size,rawBytes:total},result:reportDescriptor('campaign-result.json'),reviews:reviews.map(({name,...r})=>({...r,artifact:reportDescriptor(name)})),externalReports:externalReports.map(({name,...r})=>({...r,artifact:reportDescriptor(name)})),families,controls,receipt};
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
