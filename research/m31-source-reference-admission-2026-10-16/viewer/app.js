const $=id=>document.getElementById(id);
const fmt=n=>Number(n.toPrecision(7)).toString();
function require(ok,msg){if(!ok)throw Error(msg);}
async function read(url){const r=await fetch(url,{cache:'no-store'});require(r.ok,`HTTP ${r.status}: ${url}`);const b=await r.arrayBuffer();require(b.byteLength<1000000,'Oversized evidence');return b;}
const parse=b=>JSON.parse(new TextDecoder('utf-8',{fatal:true}).decode(b));
async function main(){
  const binding=parse(await read('./binding.json'));const names=['visible-profiles.json','results/result.json'];
  require(binding.files.length===2 && names.every(n=>binding.files.filter(f=>f.path===n).length===1),'Invalid evidence binding');
  const values={};
  for(const p of binding.files){const bytes=await read('../'+p.path);require(bytes.byteLength===p.bytes,'Byte-count mismatch');
    const sha=Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',bytes)),x=>x.toString(16).padStart(2,'0')).join('');require(sha===p.sha256,'SHA-256 mismatch: '+p.path);values[p.path]=parse(bytes);
    const li=document.createElement('li');li.textContent=`${p.path} · ${p.bytes} bytes · SHA-256 ${sha}`;$('pins').append(li);}
  const data=values[names[0]],result=values[names[1]],rows=result.union_knot_records;
  require(data.profiles.length===2 && data.profiles[0].name==='Offboard 1' && data.profiles[1].name==='Offboard 2','Unexpected measured pair');
  require(result.kind==='exposed-published-profile-descriptive-audit' && result.experimental_confidence_interval===null && result.physical_pass_threshold===null,'Unexpected result scope');
  require(rows.length===17 && rows.every(r=>['r_over_l','g1','g2','difference_g2_minus_g1'].every(k=>Number.isFinite(r[k]))),'Invalid profile values');
  document.body.dataset.binding='verified';$('evidence').hidden=false;$('status').textContent='Saved coordinates and analysis verified against byte counts and SHA-256. Static evidence display; no simulation is running.';
  $('l2').textContent=(100*result.radially_weighted_relative_L2_using_offboard2_reference).toFixed(1)+'%';$('max').textContent=result.max_absolute_normalized_discrepancy.toFixed(3);
  $('max-location').textContent=`At r/l = ${result.maximizing_radii.map(x=>x.toFixed(3)).join(', ')}. Units: speed divided by calculated hover speed.`;
  $('widths').textContent=result.half_centerline_crossings.map(c=>c.unique_downward_crossing?c.radii[0].toFixed(3):'ambiguous').join(' / ');
  for(const r of rows){const tr=document.createElement('tr');for(const k of ['r_over_l','g1','g2','difference_g2_minus_g1']){const td=document.createElement('td');td.textContent=fmt(r[k]);td.title=String(r[k]);tr.append(td);}$('rows').append(tr);}
  $('result-json').textContent=JSON.stringify(result,null,2);$('probe').max=String(rows.length-1);
  let scene;
  function update(){const dimensional=$('units').value==='target';const scaleX=dimensional?.266:1,scaleY=dimensional?9.66:1;const index=Number($('probe').value),r=rows[index];
    $('probe-output').textContent=`${dimensional?'r':'r/l'} = ${fmt(r.r_over_l*scaleX)}${dimensional?' m':''} · ${dimensional?'transferred 1':'Offboard 1'}: ${fmt(r.g1*scaleY)} · Offboard 2: ${fmt(r.g2*scaleY)}${dimensional?' m/s':' normalized speed'}`;
    $('units-explanation').textContent=dimensional?'Both curves use Offboard 2’s tabulated UH = 9.66 m/s and l = 0.266 m. Offboard 1 is an unchanged-profile transfer prediction; Offboard 2 is the plotted median reconstructed with rounded tabulated units. No target fitting.':'Published coordinates: x = r/l and speed/UH at s/l = 3. Hover normalizers are calculated physical scales, not fitted curve peaks. Only the displayed 0–3 radial interval is used.';
    scene?.update(index,$('overlay').checked,dimensional);}
  for(const id of ['units','overlay','probe'])$(id).addEventListener(id==='probe'?'input':'change',update);
  update();
  try{const {createScene}=await import('./scene.js');scene=createScene($('scene'),rows);$('reset').disabled=false;$('reset').addEventListener('click',()=>scene.reset());update();}
  catch(e){$('scene').textContent='3D unavailable. Exact values above/below remain accessible. '+e.message;}
}
main().catch(e=>{document.body.dataset.binding='failed';$('evidence').hidden=true;$('status').textContent='Evidence display stopped: '+e.message;});
