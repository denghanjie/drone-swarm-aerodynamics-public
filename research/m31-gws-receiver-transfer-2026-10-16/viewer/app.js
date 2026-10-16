const $=id=>document.getElementById(id),pct=x=>(100*x).toFixed(1)+'%';
const names=['Interpolated baseline','Lower-RPM anchor','Higher-RPM anchor'];
async function main(){
 const binding=await(await fetch('./binding.json',{cache:'no-store'})).json();if(binding.path!=='results/aggregate.json')throw Error('Unexpected result binding');
 const response=await fetch('../'+binding.path,{cache:'no-store'});if(!response.ok)throw Error('Missing saved evidence');const bytes=await response.arrayBuffer();
 if(bytes.byteLength!==binding.bytes)throw Error('Byte-count mismatch');const sha=Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',bytes)),x=>x.toString(16).padStart(2,'0')).join('');if(sha!==binding.sha256)throw Error('SHA-256 mismatch');
 const r=JSON.parse(new TextDecoder().decode(bytes));if(r.kind!=='exposed-GWS-aggregate-transfer'||r.scenarios.length!==3||r.physical_adequacy_threshold!==null||r.experimental_confidence_interval!==null)throw Error('Unexpected result scope');
 for(const s of r.scenarios)if(s.full_run.count!==14||s.reported_positive_thrust_subset.count!==9||['full_run','reported_positive_thrust_subset'].some(k=>['rms_divided_by_C0','max_absolute_divided_by_C0'].some(m=>!Number.isFinite(s[k][m])||s[k][m]<0)))throw Error('Invalid saved summary');
 document.body.dataset.binding='verified';$('evidence').hidden=false;$('status').textContent='Saved aggregate verified by byte count and SHA-256. No scientific calculation or physical simulation is running.';
 $('full').textContent=pct(r.scenarios[0].full_run.rms_divided_by_C0);$('positive').textContent=pct(r.scenarios[0].reported_positive_thrust_subset.rms_divided_by_C0);
 const values=r.scenarios.map(s=>s.reported_positive_thrust_subset.rms_divided_by_C0);$('range').textContent=pct(Math.min(...values))+'–'+pct(Math.max(...values));
 $('pin').textContent=`${binding.bytes} bytes · SHA-256 ${sha}`;$('raw').textContent=JSON.stringify(r,null,2);
 let scene;function update(){const metric=$('metric').value;const numbers=r.scenarios.map(s=>[s.full_run[metric],s.reported_positive_thrust_subset[metric]]);$('table').replaceChildren();r.scenarios.forEach((s,i)=>{const row=document.createElement('tr');[names[i],s.C0,...numbers[i]].forEach((v,j)=>{const td=document.createElement('td');td.textContent=j>=2?pct(v):j===1?Number(v.toPrecision(7)).toString():v;td.title=String(v);row.append(td);});$('table').append(row);});scene?.update(numbers);$('scene').dataset.values=JSON.stringify(numbers);$('scene').setAttribute('aria-label',`Saved ${metric==='rms_divided_by_C0'?'RMS':'maximum'} discrepancies for three baselines and two analysis sets. No raw individual measurements or simulation.`);}
 $('metric').addEventListener('change',update);update();
 try{const {makeScene}=await import('./scene.js');scene=makeScene($('scene'));$('reset').disabled=false;$('reset').addEventListener('click',()=>scene.reset());update();}catch(e){$('scene').textContent='3D unavailable. Use the exact table and saved aggregate: '+e.message;}
}main().catch(e=>{document.body.dataset.binding='failed';$('evidence').hidden=true;$('status').textContent='Evidence display stopped: '+e.message;});
