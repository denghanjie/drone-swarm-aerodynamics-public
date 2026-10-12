import * as THREE from 'three';
import {OrbitControls} from '../step02b-source/vendor/OrbitControls.js';
const $=id=>document.getElementById(id),data=await fetch('./milestone-01-source/demo.json').then(r=>{if(!r.ok)throw Error('Could not load simulation records');return r.json();});
const scene=new THREE.Scene();scene.background=new THREE.Color('#f7fafc');const camera=new THREE.PerspectiveCamera(42,1,.01,50);camera.up.set(0,0,1);
const renderer=new THREE.WebGLRenderer({antialias:true,preserveDrawingBuffer:true});renderer.setPixelRatio(Math.min(devicePixelRatio,2));$('scene').replaceChildren(renderer.domElement);
renderer.domElement.setAttribute('aria-label','Orbitable 3D drones with two alternative receiver predictions');
scene.add(new THREE.HemisphereLight(0xffffff,0x637888,3));const light=new THREE.DirectionalLight(0xffffff,3);light.position.set(1,-2,4);scene.add(light);
const orbit=new OrbitControls(camera,renderer.domElement);orbit.enableDamping=true;orbit.minDistance=.35;orbit.maxDistance=6;
const grid=new THREE.GridHelper(2,20,0xb5c8d0,0xe1e9ed);grid.rotation.x=Math.PI/2;grid.position.z=.65;scene.add(grid);
function drone(color,wireframe=false){const g=new THREE.Group(),mat=new THREE.MeshStandardMaterial({color,roughness:.4,wireframe,transparent:wireframe,opacity:wireframe?.8:1});
const box=(x,y,z,pos,rz=0)=>{const mesh=new THREE.Mesh(new THREE.BoxGeometry(x,y,z),mat);mesh.position.set(...pos);mesh.rotation.z=rz;g.add(mesh);};box(.038,.032,.014,[0,0,0]);
for(const x of [-.028,.028])for(const y of [-.028,.028]){box(Math.hypot(x,y),.004,.004,[x/2,y/2,0],Math.atan2(y,x));const disk=new THREE.Mesh(new THREE.CylinderGeometry(.023,.023,.002,24),mat);disk.rotation.x=Math.PI/2;disk.position.set(x,y,.012);g.add(disk);box(.044,.004,.002,[x,y,.015]);}scene.add(g);return g;}
const a=drone(0x087f83),b=drone(0xb66d21,true),sources=[drone(0x597ba7),drone(0x597ba7)];
const ta=new THREE.Line(new THREE.BufferGeometry(),new THREE.LineBasicMaterial({color:0x087f83})),tb=new THREE.Line(new THREE.BufferGeometry(),new THREE.LineBasicMaterial({color:0xb66d21,transparent:true,opacity:.6}));scene.add(ta,tb);
const target=new THREE.Mesh(new THREE.RingGeometry(.045,.05,40),new THREE.MeshBasicMaterial({color:0x91a2ad,side:THREE.DoubleSide}));target.position.z=1;scene.add(target);
let preset=data[0],t=0,playing=false,last=null;
function view(){orbit.target.set(.04,0,1.07);camera.position.set(.78,-1.25,1.70);orbit.update();}
function sample(trace,time){const i=Math.min(trace.length-1,Math.floor(time/.04));return {i,row:trace[i]};}
function renderState(){for(const [j,mesh,trail] of [[0,a,ta],[1,b,tb]]){const {i,row}=sample(preset.traces[j],t);mesh.position.set(row[1],row[2],row[3]);mesh.quaternion.set(row[4],row[5],row[6],row[7]);trail.geometry.setDrawRange(0,i+1);} $('time').value=t;$('clock').textContent=t.toFixed(2)+' / '+preset.end.toFixed(2)+' s';$('status').textContent=(playing?'Playing':'Paused')+' · Initial lift loss: '+preset.initialLiftLoss.map(v=>(100*v).toFixed(1)+'%').join(' vs ') + (preset.end<16?' · Stops at a model limit.':' · Full 16-second comparison.');}
function select(){preset=data.find(p=>p.id===$('preset').value);t=0;playing=false;last=null;$('play').textContent='Play';$('story').textContent=preset.explanation;$('labelA').textContent=preset.labels[0];$('labelB').textContent=preset.labels[1];$('time').max=preset.end;sources.forEach((s,i)=>{s.visible=i<preset.sources.length;if(s.visible)s.position.set(...preset.sources[i]);});[ta,tb].forEach((l,i)=>{l.geometry.dispose();l.geometry=new THREE.BufferGeometry().setFromPoints(preset.traces[i].map(r=>new THREE.Vector3(r[1],r[2],r[3])));});renderState();view();}
$('preset').onchange=select;$('play').onclick=()=>{if(t>=preset.end)t=0;playing=!playing;last=null;$('play').textContent=playing?'Pause':'Play';renderState();};$('reset').onclick=select;$('camera').onclick=view;$('time').oninput=()=>{playing=false;$('play').textContent='Play';t=Number($('time').value);renderState();};
new ResizeObserver(()=>{const r=$('scene').getBoundingClientRect();renderer.setSize(r.width,r.height,false);camera.aspect=r.width/r.height;camera.updateProjectionMatrix();}).observe($('scene'));
function frame(now){if(playing){if(last!==null)t=Math.min(preset.end,t+Math.min(.1,(now-last)/1000));if(t>=preset.end){playing=false;$('play').textContent='Play';}renderState();}last=now;orbit.update();renderer.render(scene,camera);requestAnimationFrame(frame);}select();requestAnimationFrame(frame);
