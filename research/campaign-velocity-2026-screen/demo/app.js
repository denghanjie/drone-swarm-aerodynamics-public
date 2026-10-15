// Measurement-plane display only: no aerodynamic kernel, integration or fitted data.
const el=id=>document.getElementById(id),host=el('scene');
let rows=[],unit='normalized',selected='',redraw=()=>{};
const fixed=(x,n=5)=>Number(x).toFixed(n);
function table(){
 el('rows').replaceChildren();
 const ms=unit==='ms';el('observed-label').textContent=ms?'Observed m/s':'Observed u/U_i';
 el('predicted-label').textContent=ms?'Model m/s':'Model κq';
 for(const r of rows){
  const p=ms?r.nominal_m_per_s:null;
  const values=[r.id+' / '+(r.target===15?'self-similar':'developing'),fixed(r.zeta.center,6),fixed(p?p.observed:r.observed.center),fixed(p?p.predicted:r.predicted_on_reported_scale.center),fixed(p?p.paired_difference:r.paired_difference.center),(p?p.paired_difference_interval:r.paired_difference.interval).map(x=>fixed(x,6)).join(' to ')];
  const tr=document.createElement('tr');tr.className=r.id===selected?'selected':'';
  for(const text of values){const td=document.createElement('td');td.textContent=text;tr.append(td)}
  el('rows').append(tr);
 }
 el('scale').textContent='Depth: scene Z = −(z/l) × 0.046 m. Bar scale: '+(ms?'0.027523 scene m per nominal m/s.':'0.12 scene m per normalized velocity unit.')+' Bars are not vectors or spatial velocity magnitudes.';
 redraw();
}
try{
 const response=await fetch('../EPOCH2-RESULT.json');if(!response.ok)throw Error('Result HTTP '+response.status);
 const d=await response.json();rows=d.results;
 if(d.scalar_calls!==18||rows.length!==6||d.geometry.D_opposite_motors_m!==.092||d.geometry.r_m!==0)throw Error('Unexpected result contract');
 for(const r of rows){const o=document.createElement('option');o.value=r.id;o.textContent=r.id+' · z/l '+fixed(r.zeta.center,3);el('point').append(o)}
 el('unit').onchange=()=>{unit=el('unit').value;table()};
 el('point').onchange=()=>{selected=el('point').value;table()};
 table();el('status').textContent='Six recorded points loaded. Graphical envelopes exclude zero; physical uncertainty remains unquantified.';
 try{
  const T=await import('../../campaign-public-support-factorial/demo/vendor/three.module.js');
  const scene=new T.Scene();scene.background=new T.Color('#09141f');
  const camera=new T.OrthographicCamera(-.45,.45,.45,-.45,.001,10);camera.up.set(0,0,1);
  const renderer=new T.WebGLRenderer({antialias:true});renderer.setPixelRatio(Math.min(window.devicePixelRatio||1,2));host.append(renderer.domElement);
  const target=new T.Vector3(0,0,-.34);let yaw=-Math.PI/2,pitch=0,zoom=1;
  scene.add(new T.HemisphereLight(0xffffff,0x2e4151,2.8));
  function line(points,color){const g=new T.BufferGeometry().setFromPoints(points.map(p=>new T.Vector3(...p)));const o=new T.Line(g,new T.LineBasicMaterial({color}));scene.add(o);return o}
  const body=new T.Mesh(new T.BoxGeometry(.026,.026,.012),new T.MeshStandardMaterial({color:0xbdd3e3}));scene.add(body);
  for(const [x,y] of [[.046,0],[-.046,0],[0,.046],[0,-.046]]){
   line([[0,0,0],[x,y,0]],0xa1b9ca);
   const disk=new T.Mesh(new T.CylinderGeometry(.0225,.0225,.0015,32),new T.MeshStandardMaterial({color:0x86a7bf,transparent:true,opacity:.65}));
   disk.rotation.x=Math.PI/2;disk.position.set(x,y,0);scene.add(disk);
  }
  const plane=new T.Mesh(new T.PlaneGeometry(.37,.82),new T.MeshBasicMaterial({color:0x367c91,side:T.DoubleSide,transparent:true,opacity:.12,depthWrite:false}));
  plane.rotation.x=Math.PI/2;plane.position.set(0,0,-.35);scene.add(plane);
  line([[0,0,.03],[0,0,-.79]],0xc4d8e7);
  // Tick depths are physical multiples of l; no extra flow data are generated.
  for(const z of [0,5,10,15])line([[-.008,0,-z*.046],[.008,0,-z*.046]],0xe2eef6);
  const marks=[];
  for(const r of rows){
   const z=-r.zeta.center*.046;
   const dot=new T.Mesh(new T.SphereGeometry(.0034,12,8),new T.MeshBasicMaterial({color:0xf3f7ff}));dot.position.set(0,0,z);scene.add(dot);
   const bars=[];
   for(const [v,side,color] of [[r.observed.center,-1,0xffb36d],[r.predicted_on_reported_scale.center,1,0x79baff]]){
    const len=.12*v,bar=new T.Mesh(new T.BoxGeometry(len,.0028,.0035),new T.MeshBasicMaterial({color}));
    bar.position.set(side*len/2,0,z);scene.add(bar);bars.push(bar);
   }
   marks.push({id:r.id,dot,bars});
  }
  function position(){camera.position.set(target.x+1.4*Math.cos(pitch)*Math.cos(yaw),target.y+1.4*Math.cos(pitch)*Math.sin(yaw),target.z+1.4*Math.sin(pitch));camera.lookAt(target)}
  function size(){const w=Math.max(1,host.clientWidth),h=Math.max(1,host.clientHeight),half=.45/zoom;camera.left=-half*w/h;camera.right=half*w/h;camera.top=half;camera.bottom=-half;camera.updateProjectionMatrix();renderer.setSize(w,h);position();renderer.render(scene,camera)}
  redraw=()=>{for(const m of marks){m.dot.scale.setScalar(selected===m.id?1.8:1);for(const b of m.bars)b.material.opacity=selected&&selected!==m.id?.42:1;for(const b of m.bars)b.material.transparent=true}size()};
  el('front').onclick=()=>{yaw=-Math.PI/2;pitch=0;redraw()};
  el('overview').onclick=()=>{yaw=-1.05;pitch=.24;redraw()};
  el('zoom').oninput=()=>{zoom=Number(el('zoom').value);redraw()};
  let drag=null;
  renderer.domElement.onpointerdown=e=>{if(e.button!==0)return;drag=[e.clientX,e.clientY];renderer.domElement.classList.add('drag');renderer.domElement.setPointerCapture(e.pointerId)};
  renderer.domElement.onpointermove=e=>{if(!drag)return;yaw-=(e.clientX-drag[0])*.007;pitch=Math.max(-1.2,Math.min(1.2,pitch+(e.clientY-drag[1])*.007));drag=[e.clientX,e.clientY];redraw()};
  const end=()=>{drag=null;renderer.domElement.classList.remove('drag')};renderer.domElement.onpointerup=end;renderer.domElement.onpointercancel=end;renderer.domElement.onlostpointercapture=end;
  new ResizeObserver(size).observe(host);redraw();
  renderer.domElement.addEventListener('webglcontextlost',e=>{e.preventDefault();el('status').textContent='3D context lost. The complete numerical table and report remain available.'});
 }catch(error){el('status').textContent='3D view unavailable: '+error.message+'. All six numerical rows and source links remain available.';for(const id of ['front','overview','zoom'])el(id).disabled=true;}
}catch(error){el('status').textContent='Could not load the saved result: '+error.message+'. Open the linked exact result or report.';for(const id of ['front','overview','zoom','unit','point'])el(id).disabled=true;}
