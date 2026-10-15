import * as THREE from '../../../campaign-public-support-factorial/demo/vendor/three.module.js';
const el=id=>document.getElementById(id),host=el('scene');
try{
 const response=await fetch('./data.json');if(!response.ok)throw Error('Saved viewer data unavailable');const data=await response.json();
 const scene=new THREE.Scene();scene.background=new THREE.Color('#0c1725');
 const camera=new THREE.PerspectiveCamera(44,1,.01,100);camera.up.set(0,0,1);
 const renderer=new THREE.WebGLRenderer({antialias:true});renderer.setPixelRatio(Math.min(devicePixelRatio,2));host.appendChild(renderer.domElement);
 const group=new THREE.Group();scene.add(group);const center=new THREE.Vector3();let yaw=.8,pitch=.25,distance=12,selected=2,drag=null;
 const axes=new THREE.AxesHelper(.65);scene.add(axes);
 const receiver=new THREE.Mesh(new THREE.SphereGeometry(.06,12,8),new THREE.MeshBasicMaterial({color:0xffffff}));receiver.position.set(...data.receiver);scene.add(receiver);
 const rotorGeo=new THREE.BufferGeometry().setFromPoints(data.rotors.map(v=>new THREE.Vector3(...v)));scene.add(new THREE.Points(rotorGeo,new THREE.PointsMaterial({color:0xffffff,size:.055})));
 function cameraUpdate(){camera.position.set(center.x+distance*Math.cos(pitch)*Math.cos(yaw),center.y+distance*Math.cos(pitch)*Math.sin(yaw),center.z+distance*Math.sin(pitch));camera.lookAt(center);}
 function clear(){while(group.children.length){const object=group.children[0];group.remove(object);object.geometry?.dispose();object.material?.dispose();}}
 function reset(){const L=data.fixtures[selected].extent;center.set(0,0,Math.max(L,2.5)/2);yaw=.8;pitch=.25;distance=Math.max(5,1.7*L);cameraUpdate();}
 function update(){
  const f=data.fixtures[selected],coords=data.clouds[f.cloud].slice(0,f.count);clear();const pos=[],colors=[];
  for(const p of coords){pos.push(...p);const color=new THREE.Color(p[2]<=data.axialFadeStart?'#64d8cc':p[2]<data.axialCutoff?'#f8c562':'#ff8c89');colors.push(color.r,color.g,color.b);}
  const geometry=new THREE.BufferGeometry();geometry.setAttribute('position',new THREE.Float32BufferAttribute(pos,3));geometry.setAttribute('color',new THREE.Float32BufferAttribute(colors,3));group.add(new THREE.Points(geometry,new THREE.PointsMaterial({size:.055,vertexColors:true})));
  const radius=Math.max(.5,...coords.map(p=>Math.hypot(p[0],p[1])));
  const plane=new THREE.Mesh(new THREE.PlaneGeometry(2.4*radius,2.4*radius),new THREE.MeshBasicMaterial({color:0xff8c89,transparent:true,opacity:.12,side:THREE.DoubleSide,depthWrite:false}));plane.position.z=data.axialCutoff;group.add(plane);
  const edges=new THREE.LineSegments(new THREE.EdgesGeometry(plane.geometry),new THREE.LineBasicMaterial({color:0xff8c89}));edges.position.z=data.axialCutoff;group.add(edges);
  const r=f.rotors[0];el('heading').textContent=`${f.count} sources · ${f.extent} m extent · phase ${f.phase} m`;
  el('metrics').textContent=`Rotor 0: P = ${r.P.toFixed(3)} m/s; X = ${r.X.toFixed(3)} m/s (${r.X_over_vi.toFixed(2)} vi). Omitted share of X: ${(100*r.omissionFractionOfX).toFixed(2)}%.`;
  el('counts').textContent=`${f.counts.full} fully retained, ${f.counts.partial} faded, ${f.counts.omitted} fully omitted source centers. Maximum xi across all four rotors: ${f.maxXi.toFixed(5)}. Omission bounds: ${f.boundsMS.lower.toFixed(3)}–${f.boundsMS.upper.toFixed(3)} m/s.`;
  el('rotors').replaceChildren(...f.rotors.map(r=>{const tr=document.createElement('tr');for(const value of [r.rotor,r.P.toFixed(3),r.X.toFixed(3),r.X_over_vi.toFixed(3)]){const td=document.createElement('td');td.textContent=value;tr.appendChild(td)}return tr}));
  el('record').href=f.record;el('provenance').textContent=JSON.stringify({experiment:data.experiment,fixture:f.id,coordinateSha256:f.coordinateSha256,recordSha256:f.recordSha256,postprocess:data.postprocess},null,2);reset();
 }
 data.fixtures.forEach((f,i)=>{const option=document.createElement('option');option.value=i;option.textContent=`Phase ${f.phase} m · extent ${f.extent} m · N=${f.count}`;el('fixture').appendChild(option)});el('fixture').value=selected;el('fixture').onchange=()=>{selected=Number(el('fixture').value);update()};
 el('left').onclick=()=>{yaw-=.25;cameraUpdate()};el('right').onclick=()=>{yaw+=.25;cameraUpdate()};el('reset').onclick=reset;
 host.onpointerdown=e=>{drag=[e.clientX,e.clientY];host.setPointerCapture(e.pointerId)};host.onpointermove=e=>{if(!drag)return;yaw-=(e.clientX-drag[0])*.008;pitch=Math.max(-1.2,Math.min(1.2,pitch+(e.clientY-drag[1])*.008));drag=[e.clientX,e.clientY];cameraUpdate()};host.onpointerup=host.onpointercancel=()=>drag=null;
 host.onwheel=e=>{e.preventDefault();distance=Math.max(2,Math.min(30,distance*Math.exp(e.deltaY*.001)));cameraUpdate()};
 new ResizeObserver(()=>{camera.aspect=host.clientWidth/host.clientHeight;camera.updateProjectionMatrix();renderer.setSize(host.clientWidth,host.clientHeight)}).observe(host);
 update();el('render-status').textContent='Static view ready. No model evaluation or flight animation.';function draw(){requestAnimationFrame(draw);renderer.render(scene,camera)}draw();
}catch(error){el('render-status').textContent='3D unavailable: '+error.message+'. Serve the workspace root over HTTP; result links remain available.';console.error(error);}
