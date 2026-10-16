const $=id=>document.getElementById(id),pct=x=>(100*x).toFixed(2)+'%';
const titles={'level-ladder':'Eight level drones in a vertical stack','tilted-ladder':'Eight tilted drones in a staggered stack','hexagon-cycle':'Six tilted drones with cyclic influence','near-rejection':'Nearby pair: unsupported wake domain'};
async function boundFile(pin){const response=await fetch('../'+pin.path,{cache:'no-store'});if(!response.ok)throw Error('Missing '+pin.path);const bytes=await response.arrayBuffer();const sha=[...new Uint8Array(await crypto.subtle.digest('SHA-256',bytes))].map(x=>x.toString(16).padStart(2,'0')).join('');if(sha!==pin.sha256||bytes.byteLength!==pin.bytes)throw Error('Evidence pin mismatch: '+pin.path);return JSON.parse(new TextDecoder().decode(bytes));}
async function main(){
  const binding=await(await fetch('./binding.json',{cache:'no-store'})).json();
  const [data,review]=await Promise.all(binding.files.map(boundFile));
  if(data.kind!=='four-rotor-static-coupling-development-verification'||data.cases.length!==4||review.kind!=='independent-four-rotor-coupling-saved-review')throw Error('Unexpected evidence scope');
  $('content').hidden=false;document.body.dataset.binding='verified';$('status').textContent='Saved records verified by byte count and SHA-256. No scientific solver is running in this page.';
  $('review').textContent=review.passed?'Passed':'Failures recorded';$('review-detail').textContent=`${review.check_count} checks; ${review.failures.length} recorded failures. Separate geometry implementation and 80-digit root calculation.`;
  const ladders=data.cases.slice(0,2);$('work').textContent=ladders.map(c=>c.solutions?.direct?.work.rootClosures??'—').join(' / ');
  $('outcome').textContent=review.passed?'All four designed fixtures passed the independent development checks. This supports computational consistency for these fixed cases; it does not establish physical accuracy or end-to-end speed.':'The independent review found failures. The records remain visible; the intended verification claim is not accepted.';
  $('pins').textContent=binding.files.map(p=>`${p.path}: ${p.sha256}`).join(' · ');
  const {createScene}=await import('./scene.js'),scene=createScene($('scene'));
  for(const c of data.cases){const o=document.createElement('option');o.value=c.id;o.textContent=titles[c.id];$('case').append(o);}
  let current,timer=null;
  function stop(){if(timer)clearInterval(timer);timer=null;$('play').textContent='Replay updates';}
  function update(){const s=current.solutions,k=Number($('step').value),y=s?.picard.iterates[k];scene.state(y,!current.admission.admitted);
    $('step-label').textContent=s?`${k} / ${s.picard.iterations}`:'Rejected';$('scene-state').textContent=s?(k===s.picard.iterations?'Returned state · saved evidence':`Provisional source estimate · update ${k}`):'No load solve performed';
    $('scene').dataset.case=current.id;$('scene').dataset.step=String(k);$('rows').replaceChildren();
    current.vehicles.forEach((v,i)=>{const tr=document.createElement('tr'),loads=s?.picard.residualMap.rotors[i];for(const text of [v.id,y?pct(y[i]**2):'Not evaluated',loads?loads.map(r=>r.T.toFixed(6)).join(' · '):'Unsupported configuration']){const td=document.createElement('td');td.textContent=text;tr.append(td);}$('rows').append(tr);});
  }
  function select(){stop();current=data.cases.find(c=>c.id===$('case').value);scene.load(current);const s=current.solutions;$('step').max=s?.picard.iterations??0;$('step').value=s?.picard.iterations??0;for(const id of ['step','play','final'])$(id).disabled=!s;
    $('case-title').textContent=titles[current.id];
    $('case-detail').textContent=`${current.geometryWork.pairCalls} rotor-pair evaluations; ${current.graph.edges.length} positive vehicle dependencies. `+(current.admission.admitted?(current.graph.descendingEligible?'Every influence follows the saved height order.':'The height order cannot resolve these dependencies in one pass.'):`${current.admission.errors.length} admission errors recorded. Neither load solver was run.`);
    $('iter-detail').textContent=s?`Simultaneous updates: ${s.picard.iterations}; ${s.picard.work.rootClosures} root closures, plus ${s.picard.residualWork.rootClosures} for its final check. `+(s.direct?`Ordered solve: ${s.direct.work.rootClosures} closures, plus ${s.direct.residualWork.rootClosures} for its final check. `:'Ordered solve: ineligible. ')+`Returned log residual: ${s.picard.residualLog.toExponential(3)}. These counts are not a measured speedup.`:'The red geometry highlights the model limitation. A rejected interaction is not treated as an admissible zero wake.';
    update();
  }
  $('case').addEventListener('change',select);$('step').addEventListener('input',()=>{stop();update();});$('reset').addEventListener('click',scene.reset);$('final').addEventListener('click',()=>{stop();$('step').value=$('step').max;update();});
  $('play').addEventListener('click',()=>{if(timer){stop();return;}if(Number($('step').value)>=Number($('step').max))$('step').value=0;update();$('play').textContent='Pause replay';timer=setInterval(()=>{const n=Number($('step').value)+1;$('step').value=Math.min(n,Number($('step').max));update();if(n>=Number($('step').max))stop();},650);});select();
}main().catch(e=>{document.body.dataset.binding='failed';$('status').className='error';$('status').textContent='Display stopped: '+e.message;});
