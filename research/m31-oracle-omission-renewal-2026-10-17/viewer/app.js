// Display adapter only. Fetches pinned compact saved data; no scientific imports.
const BINDING_SHA='8be075947e19308f885b9e2caef6218db0fcef26e381efa92b66d27d4373c297';
const PACKAGE='research/m31-oracle-omission-renewal-2026-10-17';
const PRIOR='research/m31-normalizer-replication-2026-10-17';
const TIERS=['1e-8','1e-4','1e-2'];
const PLAN=['run-a','run-b'].flatMap(runId=>[0,5,10].map(t=>({id:runId+'-t'+t,runId,t})));
const $=id=>document.getElementById(id);
const same=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
const sha=async b=>Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',b)),v=>v.toString(16).padStart(2,'0')).join('');
function need(ok,message){if(!ok)throw Error(message);}
function el(tag,text,cls){const e=document.createElement(tag);if(text!==undefined)e.textContent=text;if(cls)e.className=cls;return e;}
const fmt=n=>n.toLocaleString('en-US');
const percentage=(n,d)=>d>0?(100*n/d).toFixed(2)+'%':'undefined';
const word=w=>typeof w==='string'&&/^[0-9a-f]{16}$/.test(w);
const count=n=>Number.isSafeInteger(n)&&n>=0;
const dv=new DataView(new ArrayBuffer(8));
function number(w){need(word(w),'Invalid coordinate word');dv.setUint32(0,parseInt(w.slice(0,8),16),false);dv.setUint32(4,parseInt(w.slice(8),16),false);const v=dv.getFloat64(0,false);need(Number.isFinite(v),'Nonfinite saved coordinate');return v;}
let binding=null,data=null,replay=null,stateId=PLAN[0].id,tier=TIERS[0],tree='T8',lastSceneState=null;
function selectedState(){return data?.states.find(s=>s.id===stateId)||null;}
function selectedSummary(s){return s.summary.find(v=>v.tier===tier);}
function validate(model){
 need(model.schema==='m31-oracle-display-v1'&&model.package===PACKAGE&&model.checkerPassed===true&&same(model.tiers,TIERS),'Wrong display schema or unchecked analysis');
 need(model.sourceCommit===binding.sourceCommit&&model.sourceManifestSha256===binding.sourceManifestSha256,'Display source identity mismatch');
 need(Array.isArray(model.states)&&same(model.states.map(s=>({id:s.id,runId:s.runId,t:s.t})),PLAN),'Six-state schedule mismatch');
 for(const s of model.states){
  need(/^[0-9a-f]{64}$/.test(s.inputSha256)&&/^[0-9a-f]{64}$/.test(s.inputFileSha256),'Missing semantic or file-byte input identity');
  need(binding.pins.find(p=>p.path===PRIOR+'/results/inputs/'+s.id+'.json')?.sha256===s.inputFileSha256,'Input file-byte pin differs from compact display identity');
  need(Array.isArray(s.ids)&&s.ids.length===64&&new Set(s.ids).size===64&&s.ids.every(n=>Number.isInteger(n)&&n>=0&&n<=65535),'Invalid saved IDs');
  need(Array.isArray(s.poseWords)&&s.poseWords.length===448&&s.poseWords.every(word),'Invalid saved pose words');s.poseWords.forEach(number);
  need(Array.isArray(s.geometry)&&s.geometry.length===64&&same(s.geometry.map(g=>g.id),s.ids),'Geometry identity mismatch');
  for(const [i,g]of s.geometry.entries()){need(g.center.length===3&&g.center.every(word)&&g.points.length===4&&g.points.every(p=>p.length===3&&p.every(word)),'Invalid prepared endpoints');need(same(g.center,s.poseWords.slice(7*i,7*i+3)),'Snapshot and center differ');g.points.flat().forEach(number);}
  need(count(s.positiveTerms)&&s.positiveTerms<=16128&&Array.isArray(s.summary)&&same(s.summary.map(x=>x.tier),TIERS),'Invalid summary denominator');
  const ids=new Set(s.ids);
  for(const q of s.summary){
   need(q.positiveTerms===s.positiveTerms&&count(q.optimisticCeiling)&&count(q.singletonFeasible)&&q.optimisticCeiling<=s.positiveTerms&&q.singletonFeasible<=q.optimisticCeiling,'Invalid singleton counts');
   for(const k of ['T8','T2']){
    const z=q.trees[k],links=s.links[q.tier][k];
    need(z&&['positiveCovered','groups','rowsCovered','membersCovered','nodeVisits'].every(n=>count(z[n]))&&z.positiveCovered<=q.singletonFeasible&&z.rowsCovered<=256,'Invalid tree counts');
    need(z.tenPercentCountHurdle===(s.positiveTerms>0&&10*z.positiveCovered>=s.positiveTerms),'Count hurdle mismatch');
    need(Array.isArray(links)&&links.length===z.positiveCovered&&new Set(links.map(a=>a.join(':'))).size===links.length,'Link count or uniqueness mismatch');
    need(links.every(a=>a.length===3&&ids.has(a[0])&&Number.isInteger(a[1])&&a[1]>=0&&a[1]<4&&ids.has(a[2])&&a[0]!==a[2]),'Invalid saved link identity');
   }
  }
 }
}
function renderTable(){
 const body=$('all-results');body.replaceChildren();
 for(const p of PLAN){
  const s=data?.states.find(v=>v.id===p.id),row=el('tr'),first=el('td');
  const button=el('button',(p.runId==='run-a'?'A':'B')+' · '+p.t+' s','state-link'+(stateId===p.id?' current':''));button.type='button';button.disabled=!s;button.addEventListener('click',()=>{stateId=p.id;$('state').value=p.id;renderSelection(true);});first.append(button);row.append(first);
  if(!s){for(let i=0;i<6;i++)row.append(el('td','Not bound'));body.append(row);continue;}
  const q=selectedSummary(s);row.append(el('td',fmt(s.positiveTerms)));
  for(const n of [q.optimisticCeiling,q.singletonFeasible,q.trees.T8.positiveCovered,q.trees.T2.positiveCovered]){const cell=el('td',fmt(n));cell.append(el('small',percentage(n,s.positiveTerms)));row.append(cell);}
  const z=q.trees[tree];row.append(el('td',[z.groups,z.rowsCovered,z.membersCovered,z.nodeVisits].map(fmt).join(' / ')));body.append(row);
 }
 $('denominator').textContent=(data?'6':'0')+' / 6 states bound. Every scheduled state and its full positive-term denominator is retained.';
}
function publishView(s,links,segments){
 window.__viewState={...(lastSceneState||{}),validEvidence:Boolean(data),stateId:s?.id??null,tier,tree,poseSource:data?'normalizer-replication-saved-snapshot':null,renderedBodyCount:replay?64:0,selectedLinkCount:links.length,overlayCount:replay?replay.overlayCount():0,renderedLinkCount:replay?replay.overlayCount():0,overlaysEnabled:$('overlays').checked,edgeSamples:links.slice(0,8).map((edge,i)=>({receiver:edge[0],rotor:edge[1],source:edge[2],endpoints:segments[i]})),sourceCommit:binding?.sourceCommit??null};
}
function renderSelection(reloadPose=false){
 renderTable();const s=selectedState();if(!s)return;
 const q=selectedSummary(s),z=q.trees[tree],links=s.links[tier][tree],geometry=new Map(s.geometry.map(g=>[g.id,g]));
 const segments=links.map(([i,r,j])=>[...geometry.get(j).center,...geometry.get(i).points[r]].map(number));
 if(replay){if(reloadPose)replay.setFrames(s.runId,[{t:s.t,words:s.poseWords}]);replay.setOverlays($('overlays').checked?segments:[]);}
 $('selected-count').textContent=fmt(z.positiveCovered)+' / '+fmt(s.positiveTerms);
 $('selected-detail').textContent=s.id+' · '+tree+' · '+tier+' · '+percentage(z.positiveCovered,s.positiveTerms)+' of all positive terms.';
 const met=data.states.filter(v=>selectedSummary(v).trees[tree].tenPercentCountHurdle).length;
 $('hurdle-count').textContent=met+' / 6';$('hurdle-count').className=met===6?'pass':'pending';
 $('hurdle-detail').textContent=tree+' at '+tier+': states meeting the fixed term-count hurdle. This is not a speed or accuracy gate.';
 const visible=replay&&$('overlays').checked;
 $('frame-status').textContent='Saved '+s.runId+' snapshot · '+s.t+' s · 64 recorded poses · '+(visible?(links.length?fmt(links.length)+' amber links shown.':'No positive terms selected: the empty overlay is the saved result.'):(replay?'Links hidden; saved counts are unchanged.':'3D unavailable; saved selections remain in the table.'));
 $('selection-summary').textContent='Current selection: '+fmt(z.groups)+' whole nodes · '+fmt(z.rowsCovered)+' of 256 rotor rows · '+fmt(z.membersCovered)+' members, including allowed zero terms · '+fmt(z.nodeVisits)+' node visits. The amber links show only its '+fmt(z.positiveCovered)+' positive terms.';
 publishView(s,links,segments);
 window.__evidenceState={bound:true,denominator:6,tier,tree,checkerPassed:true,stateIds:PLAN.map(p=>p.id),allSixCountHurdle:met===6,sourceCommit:binding.sourceCommit,rows:data.states.map(v=>({id:v.id,positiveTerms:v.positiveTerms,summary:selectedSummary(v)}))};
}
function reject(error){binding=null;data=null;replay?.setOverlays([]);$('scene').querySelectorAll('canvas').forEach(c=>c.hidden=true);for(const id of ['state','tier','tree','reset','overlays'])$(id).disabled=true;$('notice').classList.add('error');$('notice').textContent='Evidence unavailable or inconsistent. No saved selection or pose is accepted.';$('scene-empty').hidden=false;$('scene-empty').textContent='No accepted evidence is displayed.';$('check-status').textContent='Not bound';$('selected-count').textContent='—';$('selected-detail').textContent='No selection accepted.';$('hurdle-count').textContent='— / 6';$('hurdle-detail').textContent='No opportunity interpretation is available.';$('frame-status').textContent='Evidence validation failed.';$('selection-summary').textContent='No saved selection accepted.';renderTable();window.__viewState={validEvidence:false,error:String(error.message)};window.__evidenceState={bound:false,denominator:6,stateIds:PLAN.map(p=>p.id)};}
async function main(){
 for(const p of PLAN){const option=el('option',(p.runId==='run-a'?'Run A':'Run B')+' · '+p.t+' s');option.value=p.id;$('state').append(option);}renderTable();
 need(/^[0-9a-f]{64}$/.test(BINDING_SHA),'Source draft has no accepted evidence binding');
 const response=await fetch('binding.json',{cache:'no-store'});need(response.ok,'Binding unavailable');const bytes=await response.arrayBuffer();need(bytes.byteLength<=128*1024&&await sha(bytes)===BINDING_SHA,'Binding digest mismatch');binding=JSON.parse(new TextDecoder().decode(bytes));
 need(binding.schema==='m31-oracle-view-binding-v1'&&binding.package===PACKAGE&&same(binding.schedule,PLAN)&&binding.display.path==='display-data.json','Wrong binding allocation');
 need(/^[0-9a-f]{40}$/.test(binding.sourceCommit)&&/^[0-9a-f]{64}$/.test(binding.sourceManifestSha256),'Unbound analysis source');
 need(Array.isArray(binding.pins)&&binding.pins.length>0&&new Set(binding.pins.map(p=>p.path)).size===binding.pins.length,'Missing or duplicate evidence pins');
 for(const pin of binding.pins)need((pin.path.startsWith(PACKAGE+'/')||pin.path.startsWith(PRIOR+'/'))&&!pin.path.includes('..')&&count(pin.bytes)&&/^[0-9a-f]{64}$/.test(pin.sha256),'Invalid source pin');
 const dr=await fetch(binding.display.path,{cache:'no-store'});need(dr.ok,'Compact display data missing');const db=await dr.arrayBuffer();need(db.byteLength<=16*1024*1024&&db.byteLength===binding.display.bytes&&await sha(db)===binding.display.sha256,'Display data digest mismatch');data=JSON.parse(new TextDecoder().decode(db));validate(data);
 $('notice').textContent='Accepted saved analysis and independent check are bound. The oracle knows the reference answers; this view runs no approximation, solver or flight.';$('check-status').textContent='Passed';$('check-status').className='pass';
 $('identity').textContent='Analysis source commit '+binding.sourceCommit+' · manifest '+binding.sourceManifestSha256+' · compact display data '+binding.display.sha256+'.';
 $('pose-provenance').textContent='Poses: prior normalizer replication, airflow off, recorded 0 / 5 / 10 s. Saved input pose words match generation frames; overlay endpoints come from the corresponding saved reference prepared words.';
 $('pins').replaceChildren();for(const pin of binding.pins){const item=el('li'),a=el('a',pin.path);a.href='../../../'+pin.path;item.append(a,document.createTextNode(' · '+pin.bytes+' bytes · SHA-256 '+pin.sha256));$('pins').append(item);}
 try{const module=await import('./scene.js');replay=module.createReplay($('scene'),s=>{lastSceneState=s;});$('scene-empty').hidden=true;}catch(error){$('scene-empty').textContent='3D could not initialize. The saved six-state evidence remains available below.';window.__replayError=String(error.message);}
 for(const id of ['state','tier','tree'])$(id).disabled=false;$('reset').disabled=!replay;$('overlays').disabled=!replay;
 $('state').addEventListener('change',()=>{try{stateId=$('state').value;renderSelection(true);}catch(e){reject(e);}});
 $('tier').addEventListener('change',()=>{try{tier=$('tier').value;renderSelection();}catch(e){reject(e);}});
 $('tree').addEventListener('change',()=>{try{tree=$('tree').value;renderSelection();}catch(e){reject(e);}});
 $('overlays').addEventListener('change',()=>{try{renderSelection();}catch(e){reject(e);}});$('reset').addEventListener('click',()=>replay?.reset());renderSelection(true);
}
main().catch(reject);
