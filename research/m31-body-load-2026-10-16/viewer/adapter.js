import {assert,fetchJSON,fetchVerified,view,decodePoses,decodePairPoses,receiverRecord,value,difference,pointer} from './evidence.js';
export const PLANNED = [{id:1,N:50},{id:2,N:500},{id:3,N:5000},{id:4,N:5000}];
export async function loadArtifact(signal) {
  const response=await fetch('./viewer-artifact.json',{cache:'no-store',signal});assert(response.ok,'Cannot load viewer artifact');
  const artifact=await response.json();assert(artifact.schema==='m31-body-viewer/1','Unsupported viewer schema');
  if(artifact.binding?.state==='unbound')return {artifact,result:null,reviews:[],controlAssessment:null};
  assert(artifact.binding?.state==='bound','Unsupported byte-binding state');
  const result=await fetchJSON(artifact.result,signal);assert(result.terminal===true,'Evidence result is not terminal');
  assert(Array.isArray(artifact.families)&&artifact.families.length===4,'All four family dispositions required');
  assert(Array.isArray(result.files)&&Array.isArray(artifact.reviews),'Manifest/review collection is missing');
  const manifest=new Map(result.files.map(d=>[d.name,d]));
  for(const d of [...artifact.families.flatMap(f=>Object.values(f.files)),...Object.values(artifact.controls?.files??{}),artifact.controls?.assessment].filter(Boolean)){
    const pin=manifest.get(d.name);assert(pin&&pin.bytes===d.bytes&&pin.sha256===d.sha256,'Descriptor does not match terminal raw manifest: '+d.name);
  }
  for(const p of PLANNED){const f=artifact.families.find(x=>x.id===p.id);assert(f&&f.N===p.N,'Family contract mismatch');}
  const reviews=await Promise.all(artifact.reviews.map(async r=>{
    const record=await fetchJSON(r.artifact,signal);
    return {...r,record,status:r.statusPointer===undefined?'No mapped status':pointer(record,r.statusPointer),detail:r.detailPointer===undefined?null:pointer(record,r.detailPointer)};
  }));
  const controlAssessment=artifact.controls?.assessment?await fetchJSON(artifact.controls.assessment,signal):null;
  const externalReports=await Promise.all((artifact.externalReports??[]).map(async r=>({label:r.label,record:await fetchJSON(r.artifact,signal)})));
  return {artifact,result,reviews,controlAssessment,externalReports};
}
export function defaultSelection(artifact) {
  const third=artifact.families.find(f=>f.id===3&&Object.keys(f.files??{}).length);
  const any=artifact.families.find(f=>Object.keys(f.files??{}).length);
  return third?String(third.id):any?String(any.id):artifact.controls?.files?.pairPoses?'controls':'1';
}
export async function loadFamily(family,signal) {
  const entries=await Promise.all(Object.entries(family.files).map(async ([key,d])=>[key,await fetchVerified(d,signal)]));
  const saved=Object.fromEntries(entries),N=family.N;
  return {family,poses:saved.poses?decodePoses(saved.poses,N):null,R:saved.R?view(saved.R,480*N,'R output'):null,GPU:saved.GPU?view(saved.GPU,256*N,'GPU output'):null};
}
export async function loadControls(controls,signal) {
  if(!controls)return {pairs:null,GPU:null,reference:null,metadata:null};
  const f=controls.files;
  const pairs=f.pairPoses?decodePairPoses(await fetchVerified(f.pairPoses,signal),controls.pairCount):null;
  const GPU=f.pairGPU?view(await fetchVerified(f.pairGPU,signal),256*controls.pairCount,'pair control GPU'):null;
  const reference=f.pairReference?await fetchJSON(f.pairReference,signal):null;
  const metadata=f.metadata?await fetchJSON(f.metadata,signal):null;
  const referenceStatus=f.referenceStatus?await fetchJSON(f.referenceStatus,signal):null;
  return {pairs,GPU,reference,metadata,referenceStatus};
}
// These are display differences, never scientific gates or qualification decisions.
export function colorValues(frame,mode) {
  return Array.from({length:frame.family.N},(_,id)=>{
    const g=receiverRecord(frame.GPU,id,frame.family.N,'GPU');
    if(!g?.identityOK||g.header.queryStatus!==2)return null;
    if(mode==='liftReduction') {const effective=value(g.body[0]),nominal=value(g.body[4]);return effective===null||nominal===null||nominal===0?null:1-effective/nominal;}
    const r=receiverRecord(frame.R,id,frame.family.N,'R');if(!r?.identityOK||r.header.queryStatus!==2)return null;
    const errors=g.roots.map((root,k)=>difference(root.force,r.roots[k].force));
    return errors.some(x=>x===null)?null:Math.max(...errors.map(Math.abs));
  });
}
