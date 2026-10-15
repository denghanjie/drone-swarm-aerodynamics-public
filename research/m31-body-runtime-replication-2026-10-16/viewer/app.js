import {loadArtifact,defaultSelection,loadFamily,loadControls,colorValues,recordedGate,PLANNED} from './adapter.js';
import {fetched,receiverRecord,rootControlRecord,pairRecord,format,formatScalar,difference,QUERY,POLICY} from './evidence.js';

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
  text('inspector-title','Selected evidence unavailable');identity([['Verification','Failed'],['Displayed records','None']]);text('record-details',error.message);text('selection-note','No unverified records are displayed.');text('interaction-hint','Evidence verification failed; controls are disabled.');text('legend','No verified geometry is displayed.');$('legend').dataset.mode='unavailable';emptyTable('rotor-table',$('rotor-head').querySelectorAll('th').length,'Selected evidence could not be verified.');emptyTable('body-table',7,'Selected evidence could not be verified.');
}
function coverage() {
  $('coverage-table').replaceChildren();
  for(const p of PLANNED){const f=model.artifact.families.find(x=>x.id===p.id),c=model.result?.cases?.find(x=>x.familyID===p.id);
    row('coverage-table',[`Family ${p.id}`,p.N,Object.keys(f?.files??{}).join(', ')||(f?.observedFiles?.length?'Partial files; see receipt':'None'),disposition(f,c),c?.assessment?`${c.assessment.completed?'Complete':'Partial'}; pass=${c.assessment.pass}; failures=${c.assessment.failureCount??'unavailable'}`:'Unavailable']);}
}
function disposition(f,c) {return c?.status??(c||f?.observedFiles?.length?'Partial evidence; no final family disposition':model.result?'Not executed':'Not bound');}
function controlOnly() {return !!model.result&&model.result.cases?.length===0&&model.artifact.families.every(f=>!f.observedFiles?.length&&!Object.keys(f.files??{}).length);}
function observedGPU() {return !!(model.artifact.controls?.files?.pairGPU||model.artifact.controls?.files?.rootGPU||model.artifact.families?.some(f=>f.files.GPU));}
function submittedWithoutOutput(){return model.executionEvidence?.pairDispatch?.dispatch?.submitted===true&&!observedGPU();}
function missingPairGPU(){return submittedWithoutOutput()?'Output unavailable':'Not saved';}
function availabilityNote() {
  if(!controlOnly())return '';
  const f=model.artifact.controls?.files??{},saved=[f.pairPoses?'saved original pair inputs':null,f.pairReference?'CPU R/Q pair diagnostics':null,f.rootOriginal?'saved scalar-control operands':null,(f.rootR||f.rootQ)?'CPU R/Q scalar diagnostics':null].filter(Boolean);
  const dispatch=submittedWithoutOutput()?'The first GPU pair dispatch was submitted, but no GPU output binary was saved. ':observedGPU()?'Saved GPU control output is available. ':'No complete GPU output is bound. ';
  return `${saved.length?'Available: '+saved.join(', ')+'. ':'No complete control records are bound. '}${dispatch}No main-family input or field-to-body-load result is available. All four main families were not executed.`;
}
function reports() {
  text('execution',model.result?`${model.result.status} · qualified: ${model.result.qualified}`:'Unavailable');
  text('hero-title','Saved static field-to-body records.');text('hero-intro','Prescribed fixture families and fixed controls from the runtime replication. Original saved poses and R/Q/GPU/H outputs only; no Boids motion, flight integration or inferred missing values.');
  if(controlOnly()&&observedGPU()){text('hero-title','Saved controls. No main-family result.');text('hero-intro','The campaign saved fixed control observations but no main family. These controls do not establish a field-to-body-load result.');}
  if(controlOnly()&&!observedGPU()&&!submittedWithoutOutput()){
    text('hero-title',(model.artifact.controls?.files?.pairPoses||model.artifact.controls?.files?.rootOriginal)?'Saved control inputs. No GPU observation.':'No main or GPU observations.');
    text('hero-intro',`${availabilityNote()} Recorded stopping point: ${model.result.context??'unavailable'}; ${model.result.error?.message??'no error message saved'}.`);
  }
  const pairAPI=model.executionEvidence?.pairDispatch,dispatch=pairAPI?.dispatch,reservation=model.result?.sinkClosure?.reservations?.find(x=>x.name==='controls-pairs-gpu-output.u32');
  text('dispatch-status',dispatch?`Saved pair dispatch: submitted ${dispatch.submitted}; completed ${dispatch.completed}; ${dispatch.count} active / ${pairAPI.after?.launchedInvocations??'unavailable'} launched. Output binary ${model.artifact.controls?.files?.pairGPU?'saved':'unavailable'}. ${pairAPI.error?`Recorded API error: ${pairAPI.error.name}: ${pairAPI.error.message}.`:''} ${reservation?`Persistence reservation: started ${reservation.started}, complete ${reservation.complete}.`:''}`:'No saved pair-dispatch API record is bound.');
  if(submittedWithoutOutput()){
    text('hero-title','GPU dispatch submitted. Output unavailable.');
    text('hero-intro',`${availabilityNote()} Runtime ${model.result.browserVersion??'unavailable'}; saved initialization reports ${model.executionEvidence.capability?.costs?.pipelineCreations??'unavailable'} pipeline creations. Recorded API error: ${pairAPI.error?.message??'unavailable'}. The saved evidence does not establish the cause of that fetch failure.`);
  }
  const reviewStatus=r=>r.role==='final-external-observation'?(r.status===true?'Evidence integrity verified':r.status===false?(r.record.terminalReviewFailureObserved===true?'Saved review failed; integrity unverified':'Evidence integrity unverified'):'Unavailable'):(typeof r.status==='object'?stringify(r.status):String(r.status??'Unavailable'));
  text('review',model.reviews.length?model.reviews.filter(r=>r.role==='final-external-observation').map(r=>`${r.label}: ${reviewStatus(r)}`).join(' · '):'Pending · review-unqualified');
  $('review-list').replaceChildren();
  if(!model.reviews.length)$('review-list').append(node('p','No independent review artifact is bound. The checkpoint remains review-unqualified.'));
  for(const r of model.reviews){const item=document.createElement('div');item.className='review-record';item.append(node('strong',`${r.label} · ${r.role}`),node('p',`Saved status: ${reviewStatus(r)}. Recorded scientific qualification: ${model.result?.qualified??'unavailable'}.`));
    if(r.detail!==null)item.append(node('p',typeof r.detail==='string'?r.detail:stringify(r.detail)));
    const details=document.createElement('details');details.append(node('summary','Complete saved review record'),node('pre',stringify(r.record)));item.append(details);$('review-list').append(item);}
  text('report-details',stringify({result:model.result,sourceFreezeDescriptor:model.artifact.sourceFreeze,controlAssessment:model.controlAssessmentRecord,executionEvidence:model.executionEvidence,externalReports:model.externalReports??[]}));text('gate-record',stringify({savedThresholds:model.constants?.gates??'Not saved',scope:'These are saved gates and assessment decisions. This viewer does not reevaluate any gate.'}));
}
function familyNote(f) {
  const c=model.result.cases?.find(x=>x.familyID===f.id),availability=frame.poses?`${frame.poses.length} saved poses`:'No saved original poses';
  return `Family ${f.id} · ${availability}. Recorded disposition: ${disposition(f,c)}. Enlarged body glyphs are display aids. Prescribed static fixtures, not Boids motion. Original world coordinates and xyzw attitudes are shown; RGB world-origin axes are display guides. Colors do not establish qualification.`;
}
function showReceiver() {
  if(!frame)return;const N=frame.family.N,id=Number($('receiver').value),savedCase=model.result.cases.find(x=>x.familyID===frame.family.id),assessment=frame.reports.assessment?.metadata??frame.reports.assessment??savedCase?.assessment;
  setHead(['Rotor','R inflow','Q inflow','GPU raw inflow','R force','Q force','GPU force','H force','GPU − R force','GPU − H force','Original rotor gate','Handoff gate']);
  text('family-report',stringify({savedReports:frame.reports,case:savedCase??'No case disposition saved',scope:'Only recorded reports and bounded failure samples. No missing gate, root or body value is recomputed.'}));
  if(!frame.poses&&!frame.R&&!frame.Q&&!frame.GPU&&!frame.H){text('inspector-title',savedCase||frame.family.observedFiles?.length?'No complete receiver records':'Main family not executed');identity([['Availability',disposition(frame.family,savedCase)],['Receiver records','None'],['GPU observation','None'],['Body-load result','None']]);emptyTable('rotor-table',12,'No receiver or rotor records were saved.');emptyTable('body-table',7,'No body-load records were saved.');text('record-details','No saved main records. Missing roots are not filled or reconstructed.');text('selection-note',`Family ${frame.family.id} · ${disposition(frame.family,savedCase)}. No geometry or result values are created for this view.`);return;}
  if(!Number.isInteger(id)||id<0||id>=N){$('receiver').setCustomValidity(`Use an integer from 0 to ${N-1}.`);return;}$('receiver').setCustomValidity('');
  scene?.select(id);text('inspector-title',`Receiver ${id}`);
  const records=Object.fromEntries(['R','Q','GPU','H'].map(k=>[k,receiverRecord(frame[k],id,N,k)])),{R:r,Q:q,GPU:g,H:h}=records,pose=frame.poses?.[id];
  identity([['Record kind','Prescribed static fixture'],['Original position',pose?.position.map(format).join(', ')??'Not saved'],['Quaternion xyzw',pose?.quaternion.map(format).join(', ')??'Not saved'],['Coordinate frame','Original saved world frame; no recentering of data'],...Object.entries(records).map(([k,v])=>[`${k} query`,v?`${QUERY[v.header.queryStatus]??v.header.queryStatus}${v.identityOK?'':' · identity mismatch'}`:'Not saved']),['Recorded qualification',savedCase?.qualified??'Not assessed']]);
  const scalar=(record,root,key)=>record?formatScalar(record.roots[root][key]):'Not saved';
  $('rotor-table').replaceChildren();
  for(let k=0;k<4;k++)row('rotor-table',[k,scalar(r,k,'Uordinary'),scalar(q,k,'Uordinary'),scalar(g,k,'Uraw'),scalar(r,k,'force'),scalar(q,k,'force'),scalar(g,k,'force'),scalar(h,k,'force'),format(difference(g?.roots[k].force,r?.roots[k].force)),format(difference(g?.roots[k].force,h?.roots[k].force)),recordedGate(assessment,'original rotor gate',{receiver:id,rotor:k}),recordedGate(assessment,'raw handoff gate',{receiver:id,rotor:k})]);
  $('body-table').replaceChildren();
  for(let k=0;k<8;k++)row('body-table',[`${k<4?'Effective':'Nominal'} ${['T','Mx','My','Mz'][k%4]}`,...[r,q,g].map(v=>v?formatScalar(v.body[k]):'Not saved'),'Not stored in H',format(difference(g?.body[k],r?.body[k])),k<4?recordedGate(assessment,'original body gate',{receiver:id,component:k}):'No separate direct nominal gate']);
  const samples=(assessment?.failures??[]).filter(x=>x.receiver===id);
  text('record-details',stringify({receiver:id,...records,savedFailureSamples:samples,assessmentComplete:assessment?.completed??null,totalFailureCount:assessment?.failureCount??null,note:'Missing failure samples are not individual passes. H stores roots only; its body output is absent.'}));text('selection-note',familyNote(frame.family));
}
function updateColors() {
  if(!scene||!frame?.poses)return;const mode=$('color').value,range=scene.color(colorValues(frame,mode));
  text('legend',`${mode==='forceError'?'Maximum absolute rotor force error':'Thrust reduction fraction'}: ${format(range.min)} to ${format(range.max)} · ${range.count}/${frame.family.N} available. Blue = lower, orange = higher; gray = unavailable. Scale is local to this family.`);
}
function pairReference(record,key,index) {if(!record||!(record.validity&(1<<index)))return 'Unavailable';return format(record[key]);}
function showPair() {
  if(!controls)return;const id=Number($('pair').value),pose=controls.pairs?.[id],g=pairRecord(controls.pairGPU,id),r=controls.pairReference?.R?.find(x=>x.id===id),q=controls.pairReference?.Q?.find(x=>x.id===id);
  if(pose)scene?.setPair(pose);text('inspector-title',`Fixed pair input ${id}`);
  identity([['Record kind','Saved original control input'],['Receiver position',pose?.receiver.map(format).join(', ')],['Source position',pose?.source.map(format).join(', ')],['Receiver axis',pose?.receiverAxis.map(format).join(', ')],['Source axis',pose?.sourceAxis.map(format).join(', ')],['Saved offset',pose?.offset.map(format).join(', ')],['GPU saved output',g?`${QUERY[g.header.queryStatus]??g.header.queryStatus}${g.identityOK?'':' · identity mismatch'}`:missingPairGPU()],['Expected fixed-control symbol',controls.metadata?.pairs?.expected?.[id]]]);
  setHead(['Saved diagnostic','R reference','Q reference',g?'GPU observation':`GPU · ${missingPairGPU().toLowerCase()}`]);$('rotor-table').replaceChildren();row('rotor-table',['Policy symbol',r?`${r.symbol} · ${POLICY[r.symbol]}`:'Unavailable',q?`${q.symbol} · ${POLICY[q.symbol]}`:'Unavailable',g?`${g.symbol} · ${POLICY[g.symbol]}`:missingPairGPU()]);
  ['term','down','radial','projection','center'].forEach((key,k)=>row('rotor-table',[key,pairReference(r,key,k),pairReference(q,key,k),g?formatScalar(g[key==='center'?'centerNorm':key]):missingPairGPU()]));
  text('record-details',stringify({recordKind:'Saved original fixed control input',R:r,Q:q,GPU:g??missingPairGPU(),savedReferenceStatus:controls.referenceStatus,savedControlAssessment:model.controlAssessment}));text('selection-note',`Expected fixed control/input ${id}: geometry is read from the saved ORIGINAL pair input. Cyan marks the receiver, white the source; saved axes and the orange offset are display aids. ${g?'The table includes the saved GPU control observation.':(submittedWithoutOutput()?'A pair dispatch was submitted, but its GPU output was not saved. R/Q remain CPU reference diagnostics.':'R/Q are saved CPU reference diagnostics; no GPU output is saved for this pair.')} No drone flock or body-load result is inferred.`);
  text('legend','Fixed original input geometry · cyan receiver · white source · orange saved offset. No force-error or lift-reduction colors apply.');
}
function showRootControl(){
  if(!controls)return;const id=Number($('pair').value),records=rootControlRecord(controls,id),{original,R:r,Q:q,GPU:g,H:h}=records;
  text('inspector-title',`Fixed scalar control ${id}`);identity([['Record kind','Prescribed fixed scalar input'],['Original nominal',original?formatScalar(original.nominal):'Not saved'],['Original inflow',original?formatScalar(original.inflow):'Not saved'],['GPU query',g?`${QUERY[g.header.queryStatus]??g.header.queryStatus}${g.identityOK?'':' · identity mismatch'}`:'Not observed'],['Body output','Not defined for scalar controls']]);
  setHead(['Saved scalar','R','Q','GPU','H']);$('rotor-table').replaceChildren();
  for(const [label,rk,gk,hk] of [['inflow','Uordinary','Uraw',null],['nominal','nominal','nominalRaw',null],['vi','vi','vi','vi'],['coefficient','alpha','coefficient','alpha'],['x','x','x','x'],['force','force','force','force'],['residual','residual','shaderResidual','residual']])row('rotor-table',[label,r?formatScalar(r[rk]):'Not saved',q?formatScalar(q[rk]):'Not saved',g?formatScalar(g[gk]):'Not observed',hk?(h?formatScalar(h[hk]):'Not saved'):'Not duplicated in H']);
  row('rotor-table',['Recorded gate',recordedGate(model.controlAssessment,'root control R gate',{id}),'No separate Q direct gate', model.controlAssessment?'See saved assessment':'Not assessed',recordedGate(model.controlAssessment,'root control H gate',{id})]);
  text('selection-note',`Scalar control ${id} uses only saved original operands and saved R/Q/GPU/H records. It has no position or body-load geometry. No missing solver output is reconstructed.`);text('legend','Scalar records have no geometry or color scale.');$('legend').dataset.mode='unavailable';text('record-details',stringify({...records,definition:controls.metadata?.roots?.definitions?.[id]??'Not saved',referenceStatus:controls.referenceStatus,handoffStatus:controls.handoffStatus,savedControlAssessment:model.controlAssessment}));
}
async function selectFamily() {
  const token=++sequence;loadController?.abort();loadController=new AbortController();const signal=loadController.signal;
  document.body.dataset.ready='false';
  frame=null;controls=null;disposeScene('Loading and verifying selected saved evidence…');text('status','Verifying selected evidence bytes…');
  const key=$('family').value,isControls=key==='controls'||key==='roots',isRoots=key==='roots';$('receiver-label').hidden=isControls;$('pair-label').hidden=!isControls;$('body-wrap').hidden=isControls;$('color-label').hidden=isControls;$('focus').hidden=isControls;$('legend').dataset.mode=isControls?'controls':'family';text('interaction-hint',isControls?'Drag to orbit · scroll to zoom · choose a fixed pair input':'Drag to orbit · scroll to zoom · click a body to select');
  text('family-report',isControls?'Fixed control reports are included with the selected record.':'Loading selected family reports…');text('selection-note','Verifying selected records…');text('legend','Loading saved records…');
  $('receiver').disabled=$('pair').disabled=$('color').disabled=true;emptyTable('rotor-table',6);emptyTable('body-table',6);identity([['Availability','Loading']]);text('record-details','Loading');
  try{
    if(isControls){
      const loaded=await loadControls(model.artifact.controls,isRoots?'roots':'controls',signal);if(token!==sequence)return;controls=loaded;
      const count=isRoots?(['rootOriginal','rootR','rootQ','rootGPU','rootH'].some(k=>controls[k])?model.artifact.controls.rootCount:0):((controls.pairs||controls.pairGPU||controls.pairReference)?model.artifact.controls.pairCount:0);$('pair').replaceChildren();for(let id=0;id<count;id++){const option=node('option',`${isRoots?'Scalar':'Pair'} ${id}`);option.value=String(id);$('pair').append(option);}
      $('pair').disabled=count===0;text('pair-kind',isRoots?'Scalar control':'Pair control');text('rotor-caption',controls.pairGPU?'Saved pair-control diagnostics: R/Q references and GPU observation. Fields without their saved validity bit stay unavailable.':`Saved CPU R/Q diagnostics for fixed control inputs. ${submittedWithoutOutput()?'A GPU pair dispatch was submitted, but no output binary was saved.':'No GPU output binary is bound.'} Missing outputs and roots are not filled.`);
      if(isRoots){disposeScene('Fixed scalar controls contain no saved positions. Read the saved operands and R/Q/GPU/H values below.');text('rotor-caption','Saved scalar control results. H uses the actual raw GPU operands; H does not duplicate inflow/nominal fields. Validity bits control every displayed scalar.');text('interaction-hint','Choose a saved scalar control');}else if(controls.pairs){const s=await ensureScene(token);if(!s)return;}else disposeScene('No saved pair positions are available. Saved comparison records remain readable.');
      if(token!==sequence)return;if(count){if(isRoots)showRootControl();else showPair();}else{text('inspector-title',isRoots?'Scalar controls not saved':'Pair controls not saved');text('selection-note',`No complete ${isRoots?'scalar':'pair'} control records are bound. Check the receipt for any partial files.`);text('legend','No control values are available.');$('legend').dataset.mode='unavailable';text('interaction-hint','No complete control records');identity([['Availability','No readable records bound']]);}
    }else{
      const f=model.artifact.families.find(x=>String(x.id)===key);const loaded=await loadFamily(f,signal);if(token!==sequence)return;frame=loaded;
      $('receiver').max=String(f.N-1);$('receiver').value='0';$('receiver').disabled=!frame.poses&&!frame.R&&!frame.Q&&!frame.GPU&&!frame.H;
      text('rotor-caption','R = original-input reference; Q = decoded-input reference; GPU = saved candidate; H = actual GPU-input handoff reference. Invalid fields remain unavailable. Differences are display arithmetic; only saved assessment decisions are gates.');
      if(frame.poses){const s=await ensureScene(token);if(!s)return;s.setFamily(frame.poses);$('color').disabled=false;$('focus').disabled=false;updateColors();}else disposeScene('No original saved positions are available for this family. Any saved numerical records remain readable below.');
      if(token!==sequence)return;showReceiver();if(!frame.poses){text('legend','No pose colors are available for this family.');$('legend').dataset.mode='unavailable';text('interaction-hint','No saved geometry is available for this family.');}
    }
    text('binding','Fetched bytes verified');text('status',`${availabilityNote()} Selected records match their bound byte lengths and SHA-256 hashes. Recorded execution and independent review retain their own dispositions.`.trim());document.body.dataset.ready='true';receipt();
  }catch(error){if(error.name!=='AbortError'&&token===sequence)failure(error);}
}
async function start() {
  try{
    model=await loadArtifact();
    if(model.artifact.binding.state==='unbound'){text('binding','Unbound source draft');text('review','No final external observation bound');return;}
    coverage();reports();
    document.body.dataset.binding='verified';text('binding','Reports verified');receipt();$('family').replaceChildren();
    for(const p of PLANNED){const f=model.artifact.families.find(x=>x.id===p.id),option=node('option',`Family ${p.id} · planned N=${p.N}${Object.keys(f.files).length?'':' · no saved records'}`);option.value=String(p.id);$('family').append(option);}
    for(const [key,label]of [['controls','Fixed pair controls · actual saved files only'],['roots','Fixed scalar controls · actual saved files only']]){const option=node('option',label);option.value=key;$('family').append(option);}$('family').disabled=false;$('family').value=defaultSelection(model.artifact);await selectFamily();
  }catch(error){failure(error);}
}
$('family').addEventListener('change',selectFamily);$('receiver').addEventListener('input',showReceiver);$('pair').addEventListener('change',()=>controls?.mode==='roots'?showRootControl():showPair());$('color').addEventListener('change',updateColors);$('reset').addEventListener('click',()=>scene?.reset());$('focus').addEventListener('click',()=>scene?.focus());window.addEventListener('pagehide',()=>{loadController?.abort();scene?.dispose();});
start();
