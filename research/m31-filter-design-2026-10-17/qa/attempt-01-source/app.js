import {draw} from './scene.js';
const EXPECTED_BINDING='2d90d7bf6352a4e17b96a4d2ca4e947d6a42433d54cca44499679b5b9b0dfd1b';
const el=id=>document.getElementById(id),sha=async bytes=>Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',bytes))).map(x=>x.toString(16).padStart(2,'0')).join('');
async function read(url,pin){const response=await fetch(url,{cache:'no-store'});if(!response.ok)throw Error('Saved evidence unavailable');const bytes=await response.arrayBuffer();if(pin&&(bytes.byteLength!==pin.bytes||await sha(bytes)!==pin.sha256))throw Error('Saved evidence identity mismatch');return {value:JSON.parse(new TextDecoder().decode(bytes)),bytes};}
function metric(value,label){const d=document.createElement('div');d.className='metric';const s=document.createElement('strong');s.textContent=value;const p=document.createElement('span');p.textContent=label;d.append(s,p);el('metrics').append(d);}
function field(label,value){const dt=document.createElement('dt'),dd=document.createElement('dd');dt.textContent=label;dd.textContent=value;el('record').append(dt,dd);}
try{
 const rawBinding=await read('binding.json');if(await sha(rawBinding.bytes)!==EXPECTED_BINDING)throw Error('Viewer binding identity mismatch');const binding=rawBinding.value;
 const [saved,checked]=await Promise.all([read('../results/filter-results.json',binding.result),read('../results/independent-check.json',binding.checker)]);
 const data=saved.value;if(data.records.length!==108||data.sourceManifestSha256!==binding.sourceManifestSha256)throw Error('Record count or source binding mismatch');
 const pairs=data.records.filter(r=>r.kind==='pair'),primitives=data.records.filter(r=>r.kind==='primitive');if(pairs.length!==36||primitives.length!==72)throw Error('Unexpected record partition');
 // Qualification text is a saved closeout statement bound to both raw/checker
 // digests, not an independently rerun oracle in the browser.
 const hits=pairs.filter(r=>r.candidate.decision.kind==='zero').length,falls=pairs.filter(r=>r.candidate.decision.kind==='fallback').length,rejected=pairs.filter(r=>r.candidate.decision.kind==='preparation').length;
 metric(primitives.length,'primitive cases');metric(hits,binding.qualified?'pairs proved zero by filter':'reported zeros · unqualified');metric(falls,'pairs sent to exact fallback');metric(rejected,'raw preparations rejected');
 el('summary').textContent=binding.summary;el('qualification').textContent=binding.qualification;
 el('status').textContent=binding.qualified?'Saved evidence verified · finite correctness gate passed':'Saved evidence verified · this attempt did not qualify';if(!binding.qualified)el('status').classList.add('error');
 for(const text of binding.controls){const li=document.createElement('li');li.textContent=text;el('controls').append(li);}
 for(const p of primitives){const tr=document.createElement('tr');for(const value of [p.id,p.op,p.outcome.kind+(p.outcome.reason?' · '+p.outcome.reason:'')]){const td=document.createElement('td');td.textContent=value;tr.append(td);}el('primitives').append(tr);}
 for(const p of pairs){const option=document.createElement('option');option.value=p.id;option.textContent=p.id;el('case').append(option);}
 function show(){const row=pairs.find(p=>p.id===el('case').value);el('case-title').textContent=row.id;el('record').replaceChildren();field('Filter decision',row.candidate.decision.kind==='zero'?(binding.qualified?'Proved zero':'Candidate zero · unqualified'):row.candidate.decision.kind==='preparation'?'Raw preparation rejected':'Exact fallback');field('Decision detail',row.candidate.decision.branch??row.candidate.decision.reason??row.prepared.rejection??'—');field('Exact baseline',row.baseline.status+' · '+row.baseline.branch);field('Candidate result',row.candidate.result.status+' · '+row.candidate.result.branch);field('Rotor',String(row.input.rotor));el('raw').textContent=JSON.stringify(row,null,2);draw(row);}
 el('case').addEventListener('change',show);el('next').addEventListener('click',()=>{el('case').selectedIndex=(el('case').selectedIndex+1)%pairs.length;show();});el('claims').hidden=false;show();window.__filterViewer={ready:true,caseCount:pairs.length,primitiveCount:primitives.length,hits,falls,rejected,qualified:binding.qualified};
}catch(error){el('claims').hidden=true;el('status').classList.add('error');el('status').textContent='Evidence check failed. Claims and geometry are hidden: '+error.message;window.__filterViewer={ready:false,error:error.message};}
