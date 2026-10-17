// Saved evidence only; no simulation, exact oracle or native load calls.
const BINDING_SHA='6eb3c49e846da16d013fd42aacac1b2c4793d5bb524310358f02262d8b242f35';
const $=id=>document.getElementById(id),need=(v,m)=>{if(!v)throw Error(m);};
const sha=async raw=>[...new Uint8Array(await crypto.subtle.digest('SHA-256',raw))].map(x=>x.toString(16).padStart(2,'0')).join('');
const number=w=>{need(/^[a-f0-9]{16}$/.test(w),'Invalid saved word');const b=new DataView(new ArrayBuffer(8));b.setBigUint64(0,BigInt('0x'+w));const n=b.getFloat64(0);need(Number.isFinite(n),'Nonfinite saved pose');return n;};
const rational=v=>Number(v.n)/Number(v.d),format=v=>v.toLocaleString('en-US');
let binding,index,scene,records=new Map(),selectedRun='fresh-a-t5',receiver=0,rotor=0,state={ready:false};
const expose=()=>{window.__preparedViewer=structuredClone(state);};
async function readPin(pin){need(pin&&typeof pin.path==='string'&&!pin.path.startsWith('/')&&!pin.path.split('/').includes('..')&&pin.bytes<=33554432,'Invalid saved pin');const r=await fetch('../../../'+pin.path,{cache:'no-store'});need(r.ok,'Missing pinned evidence');const b=await r.arrayBuffer();need(b.byteLength===pin.bytes&&await sha(b)===pin.sha256,'Saved evidence hash mismatch');if(pin.path.endsWith('.json'))records.set(pin.path,JSON.parse(new TextDecoder().decode(b)));}
function fail(error){scene?.clear();state={ready:false,error:String(error.message)};expose();$('status').textContent='Evidence unavailable: '+error.message+'. No coverage geometry is displayed.';$('status').style.color='#ffb4ac';for(const e of document.querySelectorAll('select,input,button'))e.disabled=true;}
function update(refit=false){try{need(index.status==='completed'&&index.qualified&&index.complete&&index.outputsPreserved,'Qualification gate');const descriptor=binding.runs.find(x=>x.id===selectedRun),tree=records.get(descriptor.pin.path);need(tree&&tree.id===selectedRun&&tree.status==='admitted','Saved run admission');const drones=tree.input.drones;need(Number.isInteger(receiver)&&receiver>=0&&receiver<64&&Number.isInteger(rotor)&&rotor>=0&&rotor<4,'Selection out of range');
 const q=tree.coverage.queries.find(x=>x.i===receiver&&x.r===rotor);need(q&&q.id===drones[receiver].id&&tree.coverage.complete,'Saved query association');
 const byID=new Map(drones.map((d,i)=>[d.id,i])),kinds=Array(64).fill(null),zeroIds=[],scalarIds=[],positiveIds=[],boxes=[],rules={};kinds[receiver]='self';
 for(const t of q.terminals){if(t.kind==='zero'){rules[t.proofRule]=(rules[t.proofRule]??0)+1;const node=tree.tree.nodes[t.node];boxes.push({min:node.center.map(x=>rational(x[0])),max:node.center.map(x=>rational(x[1]))});for(let p=t.start;p<t.end;p++){const j=byID.get(tree.coverage.permutation[p]);if(j===receiver)continue;need(j!==undefined&&kinds[j]===null,'Duplicate or missing group member');kinds[j]='zero';zeroIds.push(drones[j].id);}}else for(const j of t.sourceIndices){need(kinds[j]===null,'Duplicate scalar member');kinds[j]='scalar';scalarIds.push(drones[j].id);}}
 for(const p of tree.pairs){if(p.ii!==receiver||p.r!==rotor)continue;need(p.j===drones[p.jj].id&&kinds[p.jj]==='scalar','Saved scalar identity');if(p.oracle.status==='positive'){kinds[p.jj]='positive';positiveIds.push(p.j);}}
 need(kinds.every(Boolean)&&zeroIds.length+scalarIds.length===63,'Incomplete coverage display');
 const poses=drones.map(d=>({position:d.state.slice(0,3).map(number),quaternion:d.state.slice(6,10).map(number)})),point=tree.prepared[receiver].value.points[rotor].map(number);
 state={ready:true,run:selectedRun,receiverIndex:receiver,receiverId:drones[receiver].id,rotor,zeroIds,scalarIds,positiveIds,rules,qualified:index.qualified,reuse:index.cases.find(c=>c.id===selectedRun).reuseCounters};
 scene.show({poses,kinds,boxes,rotorPoint:point},refit);$('selected-reuse').textContent=format(state.reuse.prepareOneCalls)+' scene preparations, '+format(state.reuse.oracleCalls)+' pair calls and '+format(state.reuse.pairPreparations)+' preparations inside pairs.';$('selection').textContent='Receiver '+drones[receiver].id+' · rotor '+rotor;
 $('selected-counts').textContent=zeroIds.length+' of 63 neighbours skipped; '+scalarIds.length+' checked individually.';
 $('rules').textContent=positiveIds.length+' positive coefficients. '+Object.entries(rules).map(([k,v])=>k+': '+v+' groups').join(' · ');expose();
 }catch(e){fail(e);}}
function options(){const tree=records.get(binding.runs.find(x=>x.id===selectedRun).pin.path);$('receiver').replaceChildren(...tree.input.drones.map((d,i)=>{const o=document.createElement('option');o.value=String(i);o.textContent='ID '+d.id;return o;}));$('receiver').value='0';receiver=0;}
async function main(){
 const response=await fetch('binding.json',{cache:'no-store'});need(response.ok,'Missing viewer binding');const raw=await response.arrayBuffer();need(await sha(raw)===BINDING_SHA,'Binding hash mismatch');binding=JSON.parse(new TextDecoder().decode(raw));
 need(binding.schema==='m31-prepared-viewer-binding-v1'&&binding.status==='qualified','New qualification has not been bound');
 for(const p of binding.pins)await readPin(p);
 index=records.get(binding.result.path);need(index&&index.schema==='m31-prepared-reference-result-v1','Missing prepared-reference result');
 need(index.sourceCommit===binding.sourceCommit&&index.sourceManifestSha256===binding.sourceManifestSha256,'Source identity mismatch');
 need(index.status==='completed'&&index.qualified===true&&index.complete===true&&index.outputsPreserved===true,'Complete preserved qualification required');
 need(index.cases.length===24&&binding.runs.length===2&&index.cases.every(c=>c.exactSavedTreeEquality===true),'All 24 exact matches required');
 const names=['prepareOneCalls','preparationValidCalls','oracleCalls','operandLookups','pairPreparations'],totals=Object.fromEntries(names.map(k=>[k,0]));
 for(const c of index.cases){for(const k of names){need(Number.isSafeInteger(c.reuseCounters[k])&&c.reuseCounters[k]>=0,'Invalid reuse counter');totals[k]+=c.reuseCounters[k];}need(c.reuseCounters.operandLookups===2*c.reuseCounters.oracleCalls&&c.reuseCounters.pairPreparations===0,'Invalid reuse accounting');}
 need(totals.oracleCalls===index.scalarOracleCalls,'Scalar total mismatch');
 need(index.bindingControls.length===6&&index.bindingControls.every(c=>c.detected===true&&c.reason===c.expectedReason&&c.reuseCounterDelta.oracleCalls===0&&c.budgetOracleDelta===0),'Binding control qualification');
 $('scenes').textContent=index.cases.length+' / 24';$('prepare-count').textContent=format(totals.prepareOneCalls);$('pair-count').textContent=format(totals.oracleCalls);$('pair-prep-count').textContent=format(totals.pairPreparations);
 $('reuse-detail').textContent=format(totals.preparationValidCalls)+' preparation validations · '+format(totals.operandLookups)+' bound operand lookups. '+format(2*totals.oracleCalls)+' repeated preparations removed relative to the prior oracle path (derived from its two preparations per pair; not a measured timing).';
 for(const c of index.cases){const row=document.createElement('tr'),r=c.reuseCounters;for(const v of [c.id,c.n,format(r.prepareOneCalls),format(r.preparationValidCalls),format(r.oracleCalls),format(r.operandLookups),format(r.pairPreparations),'Exact match']){const td=document.createElement('td');td.textContent=v;row.append(td);}$('results').append(row);}
 $('status').textContent='Qualified on all 24 fixed scenes. Complete saved records matched exactly; no preparation occurred inside pair queries.';
 $('control-detail').textContent='Six new operand-binding corruptions were detected. The six earlier tree-coverage controls are retained evidence, not newly executed controls. No new simulation or browser scientific query was used.';
 $('identity').textContent='Source commit '+binding.sourceCommit+' · saved result SHA-256 '+binding.result.sha256+' · one ordered regression run; no speed claim.';
 const {createScene}=await import('./scene.js');scene=createScene($('scene'),render=>{state.render=render;expose();});options();for(const e of document.querySelectorAll('select,input,button'))e.disabled=false;update(true);
 $('run').onchange=()=>{selectedRun=$('run').value;options();update(true);};$('receiver').onchange=()=>{receiver=Number($('receiver').value);update();};$('rotor').onchange=()=>{rotor=Number($('rotor').value);update();};$('boxes').onchange=()=>scene.toggle($('boxes').checked);$('reset').onclick=()=>scene.reset();
}
main().catch(fail);
