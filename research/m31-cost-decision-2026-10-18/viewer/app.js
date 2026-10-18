import * as THREE from 'three';
import {OrbitControls} from '../../../outputs/step02b-source/vendor/OrbitControls.js';
const $=id=>document.getElementById(id);const hash=async b=>Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',b)),x=>x.toString(16).padStart(2,'0')).join('');
const need=(v,m)=>{if(!v)throw Error(m);};
async function read(url,pin){const r=await fetch(url,{cache:'no-store'});need(r.ok,'Saved file unavailable');const b=await r.arrayBuffer();need(b.byteLength<12*1048576,'Display byte cap');if(pin)need(b.byteLength===pin.bytes&&await hash(b)===pin.sha256,'Saved file identity mismatch');return JSON.parse(new TextDecoder().decode(b));}
const view=new DataView(new ArrayBuffer(8));function number(w){need(/^[0-9a-f]{16}$/.test(w),'Bad saved word');view.setBigUint64(0,BigInt('0x'+w),false);const v=view.getFloat64(0,false);need(Number.isFinite(v),'Bad coordinate');return v;}
window.__costView={loaded:false};
try{
 const pins=await read('pins.json'),input=await read('../input-words.json',pins.input),r=await read('../results/analysis.json',pins.analysis);need(r.complete&&r.correctnessPassed&&input.drones.length===1000,'Incomplete evidence');
 $('verdict').textContent=r.keepGatePassed?'The shortcut passed the speed gate for this saved state.':'The shortcut did not pass the speed gate for this saved state.';
 const names={F:'F · direct scan',H:'H · tree shortcut',HC:'HC · tree + records',H0:'H0 · tree, no skipping'};
 for(const arm of ['F','H','HC','H0']){const a=r.arms[arm],tr=document.createElement('tr');for(const v of [names[arm],a.medianMs.toFixed(2)+' ms',a.p25Ms.toFixed(2)+'–'+a.p75Ms.toFixed(2)]){const td=document.createElement('td');td.textContent=v;tr.appendChild(td);}$('timings').appendChild(tr);}
 $('gate').textContent=`Median paired H / F: ${r.medianPairedHtoF.toFixed(3)}. H was faster in ${r.strictWins}/24 pairs. The predeclared gate required a ratio ≤0.90 and at least 20 wins.`;
 $('capture').textContent=`Median paired cost with records / without records: ${r.medianPairedCaptureRatio.toFixed(2)}×.`;
 $('correctness').textContent=`All ${r.queriesChecked} queries matched the complete saved numerical outputs and retained scientific diagnostics exactly. Their actual output bytes were saved and independently checked.`;
 $('phases').textContent=Object.entries(r.arms).map(([arm,a])=>names[arm]+'\n'+Object.entries(a.phaseMedianMs).map(([k,v])=>'  '+k+': '+v.toFixed(2)+' ms').join('\n')).join('\n\n');
 const scene=new THREE.Scene();scene.background=new THREE.Color('#101f2a');const camera=new THREE.PerspectiveCamera(45,1,.01,1000);camera.up.set(0,0,1);
 const renderer=new THREE.WebGLRenderer({antialias:true});renderer.setPixelRatio(Math.min(devicePixelRatio,2));$('scene').appendChild(renderer.domElement);
 const controls=new OrbitControls(camera,renderer.domElement);controls.enableDamping=true;
 scene.add(new THREE.HemisphereLight(0xffffff,0x244356,2.5));const light=new THREE.DirectionalLight(0xffffff,2);light.position.set(3,-8,15);scene.add(light);
 const mesh=new THREE.InstancedMesh(new THREE.BoxGeometry(.16,.16,.045),new THREE.MeshStandardMaterial({color:0x8ae0c6,roughness:.5}),1000),dummy=new THREE.Object3D(),bounds=new THREE.Box3(),positions=[];
 input.drones.forEach((drone,i)=>{const s=drone.state.map(number);dummy.position.set(...s.slice(0,3));dummy.quaternion.set(...s.slice(6,10));dummy.updateMatrix();mesh.setMatrixAt(i,dummy.matrix);bounds.expandByPoint(dummy.position);positions.push(dummy.position.toArray());});scene.add(mesh);
 const sphere=bounds.getBoundingSphere(new THREE.Sphere());function reset(){const v=THREE.MathUtils.degToRad(camera.fov)/2,h=Math.atan(Math.tan(v)*camera.aspect),d=sphere.radius/Math.sin(Math.min(v,h))*1.15;controls.target.copy(sphere.center);camera.position.copy(sphere.center).addScaledVector(new THREE.Vector3(.8,-1.2,.7).normalize(),d);controls.update();}
 new ResizeObserver(()=>{const b=$('scene').getBoundingClientRect();renderer.setSize(b.width,b.height,false);camera.aspect=b.width/b.height;camera.updateProjectionMatrix();reset();}).observe($('scene'));$('reset').onclick=reset;
 controls.addEventListener('change',()=>{window.__costView.camera=camera.position.toArray();});
 window.__costView={loaded:true,count:1000,positions,keepGatePassed:r.keepGatePassed,ratio:r.medianPairedHtoF,camera:camera.position.toArray()};
 function animate(){requestAnimationFrame(animate);controls.update();renderer.render(scene,camera);}animate();
}catch(error){$('error').textContent=error.message;$('verdict').textContent='Evidence unavailable; result withheld.';window.__costView={loaded:false,error:error.message};}
