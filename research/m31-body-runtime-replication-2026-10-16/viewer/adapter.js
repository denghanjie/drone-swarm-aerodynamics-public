import {assert,fetchJSON,fetchVerified,view,decodePoses,decodePairPoses,receiverRecord,value,difference,pointer} from './evidence.js';
export const PLANNED=[{id:1,N:50},{id:2,N:500},{id:3,N:5000},{id:4,N:5000}];
const FAMILY_JSON=new Set(['assessment','stimulus','audit','admission','Rstatus','Qstatus','Hstatus','GPUapi','disposition']);
export async function loadArtifact(signal){
  const response=await fetch('./viewer-artifact.json',{cache:'no-store',signal});assert(response.ok,'Cannot load viewer artifact');const artifact=await response.json();
  assert(artifact.schema==='m31-runtime-body-viewer/1','Unsupported runtime replication viewer schema');
  if(artifact.binding?.state==='unbound')return {artifact,result:null,reviews:[],externalReports:[],controlAssessment:null,constants:null};
  assert(artifact.binding?.state==='bound','Unsupported binding state');
  const sourceFreeze=await fetchJSON(artifact.sourceFreeze,signal);assert(Array.isArray(sourceFreeze.files),'Source freeze manifest is absent');
  const result=await fetchJSON(artifact.result,signal);assert(result.sourceCommit===artifact.sourceCommit,'Result source identity mismatch');assert(result.terminal===true&&Array.isArray(result.files)&&Array.isArray(result.cases),'Terminal result contract is missing');
  assert(artifact.families?.length===4&&Array.isArray(artifact.reviews),'Family/review collection is missing');
  assert(artifact.reviews.filter(r=>r.role==='final-external-observation').length===1,'Exactly one final external observation must be designated');
  assert(artifact.controls?.pairCount===15&&artifact.controls?.rootCount===146,'Fixed-control count contract mismatch');
  const manifest=new Map(result.files.map(d=>[d.name,d]));
  const descriptors=[...artifact.families.flatMap(f=>Object.values(f.files)),...Object.values(artifact.controls?.files??{}),artifact.controls?.assessment,artifact.constants,...Object.values(artifact.executionEvidence??{})].filter(Boolean);
  for(const d of descriptors){const pin=manifest.get(d.name);assert(pin&&pin.bytes===d.bytes&&pin.sha256===d.sha256,'Descriptor does not match terminal raw manifest: '+d.name);}
  for(const p of PLANNED){const f=artifact.families.find(x=>x.id===p.id);assert(f&&f.N===p.N,'Family contract mismatch');}
  const reviews=await Promise.all(artifact.reviews.map(async r=>{const record=await fetchJSON(r.artifact,signal);return {...r,record,status:r.statusPointer===undefined?null:pointer(record,r.statusPointer),detail:r.detailPointer===undefined?null:pointer(record,r.detailPointer)};}));
  for(const r of reviews){if(r.role==='final-external-observation')assert(typeof r.status==='boolean','Final external observation status is not a saved boolean');if(r.detailPointer!==undefined)assert(r.detail!==undefined,'Review detail pointer does not resolve');}
  const externalReports=await Promise.all((artifact.externalReports??[]).map(async r=>({label:r.label,record:await fetchJSON(r.artifact,signal)})));
  const controlAssessmentRecord=artifact.controls?.assessment?await fetchJSON(artifact.controls.assessment,signal):null,controlAssessment=controlAssessmentRecord?.metadata??controlAssessmentRecord;
  const constants=artifact.constants?await fetchJSON(artifact.constants,signal):null;
  const executionEvidence=Object.fromEntries(await Promise.all(Object.entries(artifact.executionEvidence??{}).map(async([key,d])=>[key,await fetchJSON(d,signal)])));
  return {artifact,result,reviews,externalReports,controlAssessment,controlAssessmentRecord,constants,sourceFreeze,executionEvidence};
}
export function defaultSelection(a){const selectable=f=>['poses','R','Q','GPU','H'].some(k=>f.files[k]);return String(a.families.find(f=>f.id===3&&selectable(f))?.id??a.families.find(selectable)?.id??(a.controls?.files?.pairPoses?'controls':a.controls?.files?.rootOriginal?'roots':1));}
export async function loadFamily(family,signal){
  const loaded=Object.fromEntries(await Promise.all(Object.entries(family.files).map(async([k,d])=>[k,FAMILY_JSON.has(k)?await fetchJSON(d,signal):await fetchVerified(d,signal)])));
  const N=family.N;return {family,poses:loaded.poses?decodePoses(loaded.poses,N):null,R:loaded.R?view(loaded.R,480*N,'R output'):null,Q:loaded.Q?view(loaded.Q,480*N,'Q output'):null,GPU:loaded.GPU?view(loaded.GPU,256*N,'GPU output'):null,H:loaded.H?view(loaded.H,288*N,'H output'):null,reports:Object.fromEntries([...FAMILY_JSON].filter(k=>loaded[k]).map(k=>[k,loaded[k]]))};
}
export async function loadControls(c,mode,signal){
  const f=c?.files??{},root=mode==='roots',out={mode};
  const kinds=root?['rootOriginal','rootR','rootQ','rootGPU','rootH','metadata','referenceStatus','handoffStatus']:['pairPoses','pairGPU','pairReference','metadata','referenceStatus'];
  for(const k of kinds){if(!f[k])continue;out[k]=f[k].name.endsWith('.json')?await fetchJSON(f[k],signal):await fetchVerified(f[k],signal);}
  if(!out.pairReference&&out.referenceStatus?.metadata?.pairs)out.pairReference=out.referenceStatus.metadata.pairs;
  if(out.pairPoses)out.pairs=decodePairPoses(out.pairPoses,c.pairCount);
  for(const [k,n]of [['pairGPU',c.pairCount*256],['rootOriginal',c.rootCount*16],['rootR',c.rootCount*96],['rootQ',c.rootCount*96],['rootGPU',c.rootCount*256],['rootH',c.rootCount*64]])if(out[k])out[k]=view(out[k],n,k);
  return out;
}
// Display-only differences/ratios. Saved gate decisions are never recomputed.
export function colorValues(frame,mode){return Array.from({length:frame.family.N},(_,id)=>{const g=receiverRecord(frame.GPU,id,frame.family.N,'GPU');if(!g?.identityOK||g.header.queryStatus!==2)return null;if(mode==='liftReduction'){const effective=value(g.body[0]),nominal=value(g.body[4]);return effective===null||nominal===null||nominal===0?null:1-effective/nominal;}const r=receiverRecord(frame.R,id,frame.family.N,'R');if(!r?.identityOK||r.header.queryStatus!==2)return null;const errors=g.roots.map((root,k)=>difference(root.force,r.roots[k].force));return errors.some(x=>x===null)?null:Math.max(...errors.map(Math.abs));});}
// Bounded failures are samples, not a complete per-record success ledger.
export function recordedGate(assessment,kind,selector){if(!assessment)return 'Not assessed';const found=(assessment.failures??[]).some(f=>f.kind===kind&&Object.entries(selector).every(([k,v])=>f[k]===v));if(found)return 'Failed · saved sample';if(assessment.completed===true&&assessment.pass===true)return 'Passed · complete saved assessment';return 'No individual pass recorded';}
