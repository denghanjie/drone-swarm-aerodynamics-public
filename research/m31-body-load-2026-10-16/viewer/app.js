import {loadArtifact,defaultSelection,loadFamily,loadControls,colorValues,PLANNED} from './adapter.js';
import {fetched,receiverRecord,pairRecord,format,formatScalar,difference,QUERY,POLICY} from './evidence.js';

const $=id=>document.getElementById(id);
let model,frame,controls,scene,loadController,sequence=0;
const text=(id,value)=>{$(id).textContent=String(value??'Unavailable');};
const stringify=value=>JSON.stringify(value,(_,v)=>typeof v==='number'&&!Number.isFinite(v)?String(v):Object.is(v,-0)?'−0':v,2);
function node(tag,value) {const el=document.createElement(tag);el.textContent=String(value??'Unavailable');return el;}
function row(table,cells) {const tr=document.createElement('tr');cells.forEach(v=>tr.append(node('td',v)));$(table).append(tr);}
function identity(entries) {const dl=$('identity');dl.replaceChildren();for(const [k,v]of entries){dl.append(node('dt',k),node('dd',v));}}
function emptyTable(id,columns,label='No saved values') {$(id).replaceChildren();const tr=document.createElement('tr'),td=node('td',label);td.colSpan=columns;tr.append(td);$(id).append(tr);}
function setHead(names) {const tr=document.createElement('tr');names.forEach(x=>tr.append(node('th',x)));$('rotor-head').replaceChildren(tr);}
function disposeScene(message) {scene?.dispose();scene=null;$('scene').replaceChildren();const p=node('p',message);p.className='scene-placeholder';$('scene').append(p);$('reset').disabled=$('focus').disabled=true;}
async function ensureScene(token) {if(scene)return scene;const {createScene}=await import('./scene.js');if(token!==sequence)return null;scene=createScene($('scene'),id=>{$('receiver').value=String(id);showReceiver();});$('reset').disabled=false;return scene;}
function receipt() {
  $('receipt-list').replaceChildren();
  for(const d of model.artifact.receipt??[]){const el=document.createElement('div');el.className='receipt-row';const name=node('span',`${d.name} · ${d.bytes.toLocaleString()} bytes`);const state=fetched.has(d.name)?'Browser bytes verified':'Offline receipt only';el.append(name,node('code',`${state} · SHA-256 ${d.sha256}`));$('receipt-list').append(el);}
}
function failure(error) {
  document.body.dataset.binding='failed';document.body.dataset.ready='false';text('binding','Byte or layout check failed');text('status',error.message);
  ['family','receiver','pair','color','reset','focus'].forEach(id=>{$(id).disabled=true;});disposeScene('Selected evidence could not be verified. Reload after the binding is corrected.');
  text('inspector-title','Selected evidence unavailable');identity([['Verification','Failed'],['Displayed records','None']]);text('record-details',error.message);text('selection-note','No unverified records are displayed.');text('interaction-hint','Evidence verification failed; controls are disabled.');text('legend','No verified geometry is displayed.');$('legend').dataset.mode='unavailable';emptyTable('rotor-table',6,'Selected evidence could not be verified.');emptyTable('body-table',6,'Selected evidence could not be verified.');
}
function coverage() {
  $('coverage-table').replaceChildren();
  for(const p of PLANNED){const f=model.artifact.families.find(x=>x.id===p.id),c=model.result?.cases?.find(x=>x.familyID===p.id);
    row('coverage-table',[`Family ${p.id}`,p.N,Object.keys(f?.files??{}).join(', ')||(f?.observedFiles?.length?'Partial files; see receipt':'None'),disposition(f,c),c?.assessment?`${c.assessment.completed?'Complete':'Partial'}; pass=${c.assessment.pass}; failures=${c.assessment.failureCount??'unavailable'}`:'Unavailable']);}
}
function disposition(f,c) {return c?.status??(c||f?.observedFiles?.length?'Partial evidence; no final family disposition':model.result?'Not executed':'Not bound');}
function controlOnly() {return !!model.result&&model.result.cases?.length===0&&model.artifact.families.every(f=>!f.observedFiles?.length&&!Object.keys(f.files??{}).length);}
function observedGPU() {return model.result?.files?.some(f=>f.name.endsWith('-gpu-output.u32'))??false;}
function availabilityNote() {
  if(!controlOnly()||observedGPU())return '';
  const f=model.artifact.controls?.files??{},saved=[f.pairPoses?'fixed original pair inputs':null,f.pairReference?'R/Q pair reference diagnostics':null].filter(Boolean);
  return `${saved.length?'Available saved evidence: '+saved.join(' and ')+'.':'No pair input or pair diagnostic records are available.'} No observed GPU result and no field-to-body-load result. All four main families were not executed.`;
}
function reports() {
  text('execution',model.result?`${model.result.status} · qualified: ${model.result.qualified}`:'Unavailable');
  if(controlOnly()&&!observedGPU()){
    text('hero-title',model.artifact.controls?.files?.pairPoses?'Saved control inputs. No GPU observation.':'No main or GPU observations.');
    text('hero-intro',`${availabilityNote()} Recorded stopping point: ${model.result.context??'unavailable'}; ${model.result.error?.message??'no error message saved'}.`);
  }
  const reviewStatus=r=>r.statusPointer==='/observedIntegrityVerified'?(r.status===true?'Evidence integrity verified':r.status===false?'Evidence integrity unverified':'Unavailable'):(typeof r.status==='object'?stringify(r.status):String(r.status??'Unavailable'));
  text('review',model.reviews.length?model.reviews.map(r=>`${r.label}: ${reviewStatus(r)}`).join(' · '):'Pending · review-unqualified');
  $('review-list').replaceChildren();
  if(!model.reviews.length)$('review-list').append(node('p','No independent review artifact is bound. The checkpoint remains review-unqualified.'));
  for(const r of model.reviews){const item=document.createElement('div');item.className='review-record';item.append(node('strong',r.label),node('p',`Saved status: ${reviewStatus(r)}. Scientific qualification: ${r.record.qualified??model.result?.qualified??'unavailable'}.`));
    if(r.detail!==null)item.append(node('p',typeof r.detail==='string'?r.detail:stringify(r.detail)));
    const details=document.createElement('details');details.append(node('summary','Complete saved review record'),node('pre',stringify(r.record)));item.append(details);$('review-list').append(item);}
  text('report-details',stringify({result:model.result,controlAssessment:model.controlAssessment,externalReports:model.externalReports??[]}));
}
function familyNote(f) {
  const c=model.result.cases?.find(x=>x.familyID===f.id),availability=frame.poses?`${frame.poses.length} saved poses`:'No saved original poses';
  return `Family ${f.id} · ${availability}. Recorded disposition: ${disposition(f,c)}. Enlarged body glyphs are display aids. These are static records; colors do not establish qualification.`;
}
function showReceiver() {
  if(!frame)return;const N=frame.family.N,id=Number($('receiver').value);
  setHead(['Rotor','R inflow','GPU raw inflow','R force','GPU force','GPU − R force']);
  if(!frame.poses&&!frame.R&&!frame.GPU){text('inspector-title','Main family not executed');identity([['Availability',disposition(frame.family,model.result.cases?.find(x=>x.familyID===frame.family.id))],['Receiver records','None'],['GPU observation','None'],['Body-load result','None']]);emptyTable('rotor-table',6,'No receiver or rotor records were saved.');emptyTable('body-table',6,'No body-load records were saved.');text('record-details','No saved main records. Missing roots are not filled or reconstructed.');text('selection-note',`Family ${frame.family.id} · ${disposition(frame.family,model.result.cases?.find(x=>x.familyID===frame.family.id))}. No flock, receiver, rotor or body-load values are created for this view.`);return;}
  if(!Number.isInteger(id)||id<0||id>=N){$('receiver').setCustomValidity(`Use an integer from 0 to ${N-1}.`);return;}$('receiver').setCustomValidity('');
  scene?.select(id);text('inspector-title',`Receiver ${id}`);
  const r=receiverRecord(frame.R,id,N,'R'),g=receiverRecord(frame.GPU,id,N,'GPU'),pose=frame.poses?.[id];
  identity([['Position',pose?.position.map(format).join(', ')??'Unavailable'],['Quaternion xyzw',pose?.quaternion.map(format).join(', ')??'Unavailable'],['R query',r?`${QUERY[r.header.queryStatus]??r.header.queryStatus}${r.identityOK?'':' · identity mismatch'}`:'Unavailable'],['GPU query',g?`${QUERY[g.header.queryStatus]??g.header.queryStatus}${g.identityOK?'':' · identity mismatch'}`:'Unavailable'],['GPU failure stage',g?.header.failureStage],['Recorded qualification',model.result.cases?.find(x=>x.familyID===frame.family.id)?.qualified]]);
  setHead(['Rotor','R inflow','GPU raw inflow','R force','GPU force','GPU − R force']);$('rotor-table').replaceChildren();
  for(let k=0;k<4;k++)row('rotor-table',[k,formatScalar(r?.roots[k].Uordinary),formatScalar(g?.roots[k].Uraw),formatScalar(r?.roots[k].force),formatScalar(g?.roots[k].force),r?.identityOK&&g?.identityOK?format(difference(g.roots[k].force,r.roots[k].force)):'Unavailable']);
  $('body-table').replaceChildren();['Thrust T','Roll Mx','Pitch My','Nominal yaw Mz'].forEach((label,k)=>row('body-table',[label,formatScalar(r?.body[k]),formatScalar(g?.body[k]),format(difference(g?.body[k],r?.body[k])),formatScalar(r?.body[k+4]),formatScalar(g?.body[k+4])]));
  text('record-details',stringify({R:r,GPU:g}));text('selection-note',familyNote(frame.family));
}
function updateColors() {
  if(!scene||!frame?.poses)return;const mode=$('color').value,range=scene.color(colorValues(frame,mode));
  text('legend',`${mode==='forceError'?'Maximum absolute rotor force error':'Thrust reduction fraction'}: ${format(range.min)} to ${format(range.max)} · ${range.count}/${frame.family.N} available. Blue = lower, orange = higher; gray = unavailable. Scale is local to this family.`);
}
function pairReference(record,key,index) {if(!record||!(record.validity&(1<<index)))return 'Unavailable';return format(record[key]);}
function showPair() {
  if(!controls)return;const id=Number($('pair').value),pose=controls.pairs?.[id],g=pairRecord(controls.GPU,id),r=controls.reference?.R?.find(x=>x.id===id),q=controls.reference?.Q?.find(x=>x.id===id);
  if(pose)scene?.setPair(pose);text('inspector-title',`Fixed pair input ${id}`);
  identity([['Record kind','Saved original control input'],['Receiver position',pose?.receiver.map(format).join(', ')],['Source position',pose?.source.map(format).join(', ')],['Receiver axis',pose?.receiverAxis.map(format).join(', ')],['Source axis',pose?.sourceAxis.map(format).join(', ')],['Saved offset',pose?.offset.map(format).join(', ')],['GPU observation',g?QUERY[g.header.queryStatus]??g.header.queryStatus:'Not observed'],['Expected fixed-control symbol',controls.metadata?.pairs?.expected?.[id]]]);
  setHead(['Saved diagnostic','R reference','Q reference',g?'GPU observation':'GPU · not observed']);$('rotor-table').replaceChildren();row('rotor-table',['Policy symbol',r?`${r.symbol} · ${POLICY[r.symbol]}`:'Unavailable',q?`${q.symbol} · ${POLICY[q.symbol]}`:'Unavailable',g?`${g.symbol} · ${POLICY[g.symbol]}`:'Not observed']);
  ['term','down','radial','projection','center'].forEach((key,k)=>row('rotor-table',[key,pairReference(r,key,k),pairReference(q,key,k),g?formatScalar(g[key==='center'?'centerNorm':key]):'Not observed']));
  text('record-details',stringify({recordKind:'Saved original fixed control input',R:r,Q:q,GPU:g??'Not observed',savedReferenceStatus:controls.referenceStatus}));text('selection-note',`Expected fixed control/input ${id}: geometry is read from the saved ORIGINAL pair input. Cyan marks the receiver, white the source; saved axes and the orange offset are display aids. ${g?'The table includes the saved GPU control observation.':'R/Q are saved reference diagnostics; no GPU observation exists for this pair.'} No drone flock or body-load result is inferred.`);
  text('legend','Fixed original input geometry · cyan receiver · white source · orange saved offset. No force-error or lift-reduction colors apply.');
}
async function selectFamily() {
  const token=++sequence;loadController?.abort();loadController=new AbortController();const signal=loadController.signal;
  document.body.dataset.ready='false';
  frame=null;controls=null;disposeScene('Loading and verifying selected saved evidence…');text('status','Verifying selected evidence bytes…');
  const key=$('family').value,isControls=key==='controls';$('receiver-label').hidden=isControls;$('pair-label').hidden=!isControls;$('body-wrap').hidden=isControls;$('color-label').hidden=isControls;$('focus').hidden=isControls;$('legend').dataset.mode=isControls?'controls':'family';text('interaction-hint',isControls?'Drag to orbit · scroll to zoom · choose a fixed pair input':'Drag to orbit · scroll to zoom · click a body to select');
  $('receiver').disabled=$('pair').disabled=$('color').disabled=true;emptyTable('rotor-table',6);emptyTable('body-table',6);identity([['Availability','Loading']]);text('record-details','Loading');
  try{
    if(isControls){
      const loaded=await loadControls(model.artifact.controls,signal);if(token!==sequence)return;controls=loaded;
      const count=controls.pairs||controls.GPU||controls.reference?model.artifact.controls.pairCount:0;$('pair').replaceChildren();for(let id=0;id<count;id++){const option=node('option',`Pair ${id}`);option.value=String(id);$('pair').append(option);}
      $('pair').disabled=count===0;text('rotor-caption',controls.GPU?'Saved pair-control diagnostics: R/Q references and GPU observation. Fields without their saved validity bit stay unavailable.':'Saved R/Q reference diagnostics for fixed control inputs. No GPU observation was saved. No field-to-body-load result is available; missing outputs and roots are not filled.');
      if(controls.pairs){const s=await ensureScene(token);if(!s)return;}else disposeScene('No saved pair positions are available. Saved comparison records remain readable.');
      if(token!==sequence)return;if(count)showPair();else{text('selection-note','No pair controls were saved.');identity([['Availability','Not executed']]);}
    }else{
      const f=model.artifact.families.find(x=>String(x.id)===key);const loaded=await loadFamily(f,signal);if(token!==sequence)return;frame=loaded;
      $('receiver').max=String(f.N-1);$('receiver').value='0';$('receiver').disabled=!frame.poses&&!frame.R&&!frame.GPU;
      text('rotor-caption','R uses original binary64 inputs. GPU values are the saved binary32 outputs. Invalid or unwritten fields stay unavailable.');
      if(frame.poses){const s=await ensureScene(token);if(!s)return;s.setFamily(frame.poses);$('color').disabled=false;$('focus').disabled=false;updateColors();}else disposeScene('No original saved positions are available for this family. Any saved numerical records remain readable below.');
      if(token!==sequence)return;showReceiver();if(!frame.poses){text('legend','No pose colors are available for this family.');$('legend').dataset.mode='unavailable';text('interaction-hint','No saved geometry is available for this family.');}
    }
    text('binding','Fetched bytes verified');text('status',`${availabilityNote()} Selected records match their bound byte lengths and SHA-256 hashes. Recorded execution and independent review retain their own dispositions.`.trim());document.body.dataset.ready='true';receipt();
  }catch(error){if(error.name!=='AbortError'&&token===sequence)failure(error);}
}
async function start() {
  try{
    model=await loadArtifact();coverage();reports();
    if(model.artifact.binding.state==='unbound')return;
    document.body.dataset.binding='verified';text('binding','Reports verified');receipt();$('family').replaceChildren();
    for(const p of PLANNED){const f=model.artifact.families.find(x=>x.id===p.id),option=node('option',`Family ${p.id} · planned N=${p.N}${Object.keys(f.files).length?'':' · no saved records'}`);option.value=String(p.id);$('family').append(option);}
    const option=node('option','Fixed pair inputs · saved originals + reference diagnostics');option.value='controls';$('family').append(option);$('family').disabled=false;$('family').value=defaultSelection(model.artifact);await selectFamily();
  }catch(error){failure(error);}
}
$('family').addEventListener('change',selectFamily);$('receiver').addEventListener('input',showReceiver);$('pair').addEventListener('change',showPair);$('color').addEventListener('change',updateColors);$('reset').addEventListener('click',()=>scene?.reset());$('focus').addEventListener('click',()=>scene?.focus());window.addEventListener('pagehide',()=>{loadController?.abort();scene?.dispose();});
start();
