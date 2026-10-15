import * as THREE from './vendor/three.module.js';
const el=id=>document.getElementById(id),host=el('scene');
try {
const data=await fetch('./data.json').then(r=>{if(!r.ok)throw Error('Data unavailable');return r.json()});
const scene=new THREE.Scene();scene.background=new THREE.Color('#08131d');
const camera=new THREE.PerspectiveCamera(45,1,.01,1000);camera.up.set(0,0,1);
const renderer=new THREE.WebGLRenderer({antialias:true});renderer.setPixelRatio(Math.min(devicePixelRatio,2));host.appendChild(renderer.domElement);
const center=new THREE.Vector3();data.frames[0].positions.forEach(p=>center.add(new THREE.Vector3(...p)));center.divideScalar(16);
let yaw=.8,pitch=.55,distance=6,playing=false,frame=0,last=0;
function cameraUpdate(){camera.position.set(center.x+distance*Math.cos(pitch)*Math.cos(yaw),center.y+distance*Math.cos(pitch)*Math.sin(yaw),center.z+distance*Math.sin(pitch));camera.lookAt(center)}
const drones=[],arrows=[];
for(let i=0;i<16;i++){const group=new THREE.Group();const material=new THREE.MeshBasicMaterial({color:'#74d8d1'});for(let k=0;k<2;k++){const bar=new THREE.Mesh(new THREE.BoxGeometry(.20,.018,.018),material);bar.rotation.z=k*Math.PI/2;group.add(bar)}const body=new THREE.Mesh(new THREE.SphereGeometry(.035,10,6),material);group.add(body);scene.add(group);drones.push({group,material});const arrow=new THREE.ArrowHelper(new THREE.Vector3(0,0,-1),new THREE.Vector3(),.1,0x82a8ed,.04,.022);scene.add(arrow);arrows.push(arrow)}
const axes=new THREE.AxesHelper(.4);axes.position.copy(center).add(new THREE.Vector3(-1,-1,-.5));scene.add(axes);
const grid=new THREE.GridHelper(5,10,0x31515c,0x19313f);grid.rotation.x=Math.PI/2;grid.position.copy(center);grid.position.z-=.6;scene.add(grid);
el('frame').max=data.frames.length-1;
function update(){const f=data.frames[frame],arm=+el('arm').value;let maxLoss=0,maxWind=0;for(let i=0;i<16;i++){const p=f.positions[i];drones[i].group.position.set(...p);drones[i].group.quaternion.set(...f.quaternions[i]);const loss=(f.loads[0][i][0]-f.loads[arm][i][0])/data.mg;maxLoss=Math.max(maxLoss,loss);drones[i].material.color.setRGB(.25+Math.min(1,loss/.02)*.75,.82-Math.min(1,loss/.02)*.30,.77-Math.min(1,loss/.02)*.60);const u=f.winds[arm][i].reduce((a,b)=>a+b,0)/4;maxWind=Math.max(maxWind,u);arrows[i].position.set(...p);arrows[i].setDirection(new THREE.Vector3(0,0,-1).applyQuaternion(drones[i].group.quaternion).normalize());arrows[i].setLength(Math.max(.001,u*.20),.04,.025);arrows[i].visible=u>0}el('time').textContent=`t=${f.time.toFixed(4)} s · original row ${f.row}`;el('frame').value=frame;el('status').textContent=`This saved snapshot: largest thrust difference ${(100*maxLoss).toFixed(3)}% of weight; largest mean rotor inflow ${maxWind.toFixed(3)} m/s. P and X coincide here; R and U coincide here.`}
el('hashes').textContent=JSON.stringify({experiment:data.experiment,selection:data.selection,inputSha256:data.inputSha256,windsSha256:data.windsSha256,loadsSha256:data.loadsSha256},null,2);
el('arm').onchange=update;el('frame').oninput=()=>{frame=+el('frame').value;update()};el('play').onclick=()=>{playing=!playing;el('play').textContent=playing?'Pause':'Play saved snapshots'};el('reset').onclick=()=>{yaw=.8;pitch=.55;distance=6;cameraUpdate()};
let drag=null;host.onpointerdown=e=>{drag=[e.clientX,e.clientY];host.setPointerCapture(e.pointerId)};host.onpointermove=e=>{if(!drag)return;yaw-=(e.clientX-drag[0])*.008;pitch=Math.max(-1.3,Math.min(1.3,pitch+(e.clientY-drag[1])*.008));drag=[e.clientX,e.clientY];cameraUpdate()};host.onpointerup=()=>drag=null;host.onwheel=e=>{e.preventDefault();distance=Math.max(.5,Math.min(30,distance*Math.exp(e.deltaY*.001)));cameraUpdate()};
new ResizeObserver(()=>{camera.aspect=host.clientWidth/host.clientHeight;camera.updateProjectionMatrix();renderer.setSize(host.clientWidth,host.clientHeight)}).observe(host);
cameraUpdate();update();function animate(t){requestAnimationFrame(animate);if(playing&&t-last>180){frame=(frame+1)%data.frames.length;last=t;update()}renderer.render(scene,camera)}requestAnimationFrame(animate);
} catch(error){el('status').textContent='3D view could not load: '+error.message+'. Open via the supplied local HTTP server instructions; numerical evidence links remain available.';console.error(error)}
