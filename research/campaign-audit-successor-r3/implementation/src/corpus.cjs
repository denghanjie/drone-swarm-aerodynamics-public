'use strict';
const fs=require('fs'),path=require('path');
const {sha,WORKSPACE,STUDY,OLD}=require('./load-audit.cjs'),{rawBytes}=require('./exact.cjs');
const readJSON=p=>JSON.parse(fs.readFileSync(p,'utf8'));
function verified(relative,expected,bytes){const b=fs.readFileSync(path.join(WORKSPACE,relative));if(sha(b)!==expected||(bytes!==undefined&&b.length!==bytes))throw Object.assign(Error('Frozen input identity mismatch'),{integrityBlocked:true,detail:{relative,expected,actual:sha(b),expectedBytes:bytes,actualBytes:b.length}});return b;}
function decoded(buffer,offset,n=16){return Array.from({length:n},(_,i)=>Array.from({length:17},(_,k)=>buffer.readDoubleLE(offset+(i*17+k)*8)));}
function sourceArray(index){const manifest=readJSON(path.join(STUDY,'CORPUS-MANIFEST.json')),m=manifest.arrays[index];if(!m)throw Error('Unknown corpus array');const meta=JSON.parse(verified(m.sidecar_path,m.sidecar_sha256).toString()),original=meta.originalSidecar||meta,wrapped=!!meta.originalSidecar;const bytes=wrapped?original.uncompressedBytes:original.bytes,hash=wrapped?original.uncompressedSha256:original.sha256;const shape=original.shape;if(!Array.isArray(shape)||shape.length!==3||shape.some(x=>!Number.isSafeInteger(x)||x<1)||shape[1]!==16||shape[2]!==17||JSON.stringify(shape)!==JSON.stringify(m.shape)||shape.reduce((a,b)=>a*b,8)!==bytes||bytes!==m.expected_bytes||hash!==m.expected_sha256||original.dt!==m.cadence_ticks*(1/51200))throw Error('Malformed or inconsistent frozen raw sidecar');if(wrapped){if(meta.encoding!=='little-endian Float64 bytes; no values interpreted'||original.encoding!=='gzip / little-endian Float64'||original.startTime!==0||original.endTime!==1||m.cadence_ticks!==8)throw Error('Historical materialized sidecar contract');const run=readJSON(path.join(OLD,'inputs/runs',original.runId+'.json'));if(JSON.stringify(run.denseStates)!==JSON.stringify(original))throw Error('Historical nested sidecar/run mismatch');}else if(original.encoding!=='little-endian Float64, uncompressed'||original.count!==16||original.cadenceTicks!==m.cadence_ticks||original.baseTickSeconds!==1/51200)throw Error('Current raw sidecar contract');const buffer=verified(m.binary_path,m.expected_sha256,m.expected_bytes);return {m,meta,buffer,row:i=>decoded(buffer,i*m.shape[1]*17*8,m.shape[1])};}
function anchorsFor(index){const {arrays}=readJSON(path.join(STUDY,'CORPUS-MANIFEST.json')),m=arrays[index],preflight=m.binary_path.includes('/inputs/arrays/'),seed=Number(m.binary_path.match(/s(\d+)-/)[1]),auditId=preflight?`preflight-s${seed}`:path.basename(m.binary_path).split('.')[0],run=preflight?null:readJSON(path.join(OLD,'results/runs',auditId+'.json')),auditPath=path.join(OLD,'results/audit',auditId+'.json'),audit=readJSON(auditPath),stepTicks=preflight?8:run.config.stepTicks,schedule=preflight?'preflight-row':run.config.kind==='joint'?'joint-5':'accepted-endpoint';const signatures=fs.readFileSync(path.join(OLD,audit.signatureStream.path));if(signatures.length!==audit.signatureStream.bytes||sha(signatures)!==audit.signatureStream.sha256)throw Error('Saved signature stream identity');return {auditId,stepTicks,schedule,signatures,audit,preflight};}
function checkAnchor(ctx,s,anchor,tick){const entry=anchor.preflight?tick/8:(tick/anchor.stepTicks)*(anchor.schedule==='joint-5'?5:1);ctx.assert(Number.isInteger(entry)&&entry>=0&&(entry+1)*32<=anchor.signatures.length,'Available endpoint signature index invalid');ctx.assert(Buffer.from(s.B.signatureSha256,'hex').equals(anchor.signatures.subarray(entry*32,(entry+1)*32)),'Available endpoint original signature mismatch');ctx.add('savedSignatureAnchors');}
function indexForAudit(auditId){const {arrays}=readJSON(path.join(STUDY,'CORPUS-MANIFEST.json'));return arrays.findIndex(m=>m.binary_path.includes('/inputs/arrays/')?auditId==='preflight-s'+m.binary_path.match(/s(\d+)-/)[1]:path.basename(m.binary_path).split('.')[0]===auditId);}

function runArray(ctx,index){
 const {m,row}=sourceArray(index),anchor=anchorsFor(index),n=m.shape[0],logicalId=anchor.preflight?anchor.auditId:`replay-${anchor.auditId}`;
 const mapping=i=>anchor.preflight?i:(i*m.cadence_ticks/anchor.stepTicks)*(anchor.schedule==='joint-5'?5:1);
 const selector={manifestIndex:index,binaryPath:m.binary_path,rows:[0,n-1],rowCount:n,anchor:{auditId:anchor.auditId,stepTicks:anchor.stepTicks,cadenceTicks:m.cadence_ticks,schedule:anchor.schedule,firstIndex:0,lastIndex:mapping(n-1),checkedCount:n}};
 ctx.case(`array-${index}`,anchor.preflight?'original-preflight':'saved-endpoint-replay',()=>{
  const p=ctx.pair({id:logicalId,persist:anchor.preflight});let previous=null;
  for(let i=0;i<n;i++){
   ctx.tick();const states=row(i),tick=i*m.cadence_ticks,location={tick,time:anchor.preflight?i/6400:tick*(1/51200),role:'endpoint'};
   ctx.setCurrent({sourceSelector:{manifestIndex:index,binaryPath:m.binary_path,row:i,tick,signatureIndex:mapping(i)}});
   const s=p.observe(states,location);ctx.assert(!s.errorB,'Unexpected domain error on saved endpoint');
   const entry=mapping(i);ctx.assert(Number.isInteger(entry)&&entry>=0&&(entry+1)*32<=anchor.signatures.length,'Nonintegral/out-of-range original signature anchor');
   const actual=Buffer.from(s.B.signatureSha256,'hex'),saved=anchor.signatures.subarray(entry*32,(entry+1)*32);ctx.assert(actual.equals(saved),'Saved original signature anchor mismatch');ctx.add('savedSignatureAnchors');
   if(previous){const risk=p.checkStep([previous,s]);if(!risk.B.ok)ctx.assert(risk.B.error.unresolvedJump===true&&risk.B.error.message==='Unresolved finite-jump sampled-range risk','Unexpected replay exception');if(anchor.preflight)ctx.assert(risk.B.ok,'Original preflight unexpectedly flags a range risk');}previous=s;
  }
  const result=p.finish();ctx.assert(!result.errorB,'Unexpected finish error');
  if(anchor.preflight){ctx.exact(JSON.parse(fs.readFileSync(path.join(p.roots.B,'results/audit',logicalId+'.json'),'utf8')),anchor.audit,'original.preflight.orderedJson');for(const a of ctx.artifacts.filter(x=>x.logicalPath.startsWith(`results/audit/${logicalId}.`))){const originalPath=path.join(OLD,a.logicalPath),b=fs.readFileSync(path.join(STUDY,a.baselinePath)),original=fs.readFileSync(originalPath);ctx.assert(b.equals(original),'Original preflight artifact bytes differ');a.kind='original-preflight';a.originalPath=path.relative(STUDY,originalPath);a.originalBytesEqual=true;ctx.add('directArtifactByteComparisons');}ctx.add('completeOriginalPreflightAudits');}
 },selector,['exact-values','signed-zero','property-order','input-aliases','nonmutation','float64-bytes','original-signature-anchors','full-finish-equality',...(anchor.preflight?['original-preflight-complete-byte-reproduction']:['sparse-replay-risk-equality'])]);
}
function runBrackets(ctx){
 const provenance=readJSON(path.join(STUDY,'PROVENANCE.json'));
 for(const item of provenance.saved_audit_metadata_inventory){
  const audit=JSON.parse(verified(item.path,item.sha256).toString()),meta=audit.bracketRaw,anchor=anchorsFor(indexForAudit(audit.id)),buffer=verified(path.relative(WORKSPACE,path.join(OLD,meta.path)),meta.sha256,meta.bytes);
  for(const [category,entry]of Object.entries(audit.brackets))for(const key of ['first','worst']){
   const bracket=entry[key],id=`bracket-${audit.id}-${category}-${key}`;
   ctx.case(id,'saved-bracket-original-pair',()=>{
    const p=ctx.pair({id,persist:false}),samples=[];
    for(const side of ['from','to']){const v=bracket[side];ctx.assert(v.geometryBytes===16*17*8,'Saved bracket shape');const slice=buffer.subarray(v.geometryOffsetBytes,v.geometryOffsetBytes+v.geometryBytes);ctx.assert(sha(slice)===v.geometrySha256,'Saved bracket side hash');const states=decoded(slice,0),raw=v.rawStageOffsetBytes===undefined?states:decoded(buffer,v.rawStageOffsetBytes);ctx.assert(rawBytes(states).equals(slice),'Saved bracket Float64 decode/reencode');ctx.setCurrent({sourceSelector:{audit:item.path,category,key,side,location:v.location,offset:v.geometryOffsetBytes}});const s=p.observe(states,v.location,{raw,comparePrevious:false});ctx.assert(!s.errorB,'Unexpected saved bracket domain error');checkAnchor(ctx,s,anchor,v.location.tick);samples.push(s);ctx.add('savedBracketSides');}
    p.compare(samples[0],samples[1]);ctx.add('savedBracketPairs');p.finish();
   },{auditPath:item.path,category,key,from:bracket.from,to:bracket.to},['saved-whole-swarm-sides','original-bracket-pair','float64-bytes','locations-and-offsets','original-signature-anchors','exact-values','property-order','aliases','nonmutation','full-finish-equality']);
  }
 }
}
function runJsonStates(ctx){
 const manifest=readJSON(path.join(STUDY,'CORPUS-MANIFEST.json')),entries=[];
 for(let index=0;index<manifest.arrays.length;index++){
  const m=manifest.arrays[index],source=m.binary_path.includes('/inputs/arrays/'),id=source?path.basename(m.binary_path).split('.')[0]:path.basename(m.binary_path).split('.')[0],relative=source?`research-next/implementation/inputs/runs/${id}.json`:`research-next/implementation/results/runs/${id}.json`,run=readJSON(path.join(WORKSPACE,relative));
  for(const side of ['initial','final'])entries.push({id:`json-${index}-${side}`,manifestIndex:index,relative,side,states:run[side],location:{tick:side==='initial'?0:run.endTick===undefined?51200:run.endTick,role:'endpoint',jsonSide:side}});
 }
 const stopPath='research-next/implementation/results/failures/s840131-P1.json',stop=readJSON(path.join(WORKSPACE,stopPath));ctx.assert(stop.tick===50768&&stop.exactStoppedState===true,'P1 stop is not the exact tick50768 state');entries.push({id:'json-exact-P1-stop',manifestIndex:5,relative:stopPath,side:'state',states:stop.state,location:{tick:50768,role:'endpoint',stopPhase:stop.phase}});
 for(const e of entries)ctx.case(e.id,'saved-json-full17-state',()=>{ctx.setCurrent({sourceSelector:{path:e.relative,side:e.side,tick:e.location.tick}});const p=ctx.pair({id:e.id}),s=p.observe(e.states,e.location);ctx.assert(!s.errorB,'Saved JSON state domain failure');checkAnchor(ctx,s,anchorsFor(e.manifestIndex),e.location.tick);ctx.add('savedJsonStates');p.finish();},{path:e.relative,side:e.side,tick:e.location.tick},['saved-json-state','original-signature-anchors','exact-values','signed-zero','nonmutation','input-aliases','full-finish-equality']);
}
module.exports={runArray,runBrackets,runJsonStates,sourceArray,anchorsFor,decoded};
