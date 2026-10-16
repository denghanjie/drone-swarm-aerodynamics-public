import * as THREE from '../../../outputs/step02b-source/vendor/three.module.js';
import {OrbitControls} from '../../../outputs/step02b-source/vendor/OrbitControls.js';
const holder=document.getElementById('canvas');
const renderer=new THREE.WebGLRenderer({antialias:true});renderer.setPixelRatio(Math.min(devicePixelRatio,2));renderer.setClearColor(0x102431);holder.appendChild(renderer.domElement);
const scene=new THREE.Scene(),camera=new THREE.PerspectiveCamera(42,1,.001,1000);camera.up.set(0,0,1);const orbit=new OrbitControls(camera,renderer.domElement);orbit.enableDamping=true;orbit.addEventListener('change',()=>holder.dataset.camera=camera.position.toArray().join(','));scene.add(new THREE.HemisphereLight(0xffffff,0x4e6e7e,2));const group=new THREE.Group();scene.add(group);
function number(word){const v=new DataView(new ArrayBuffer(8));v.setBigUint64(0,BigInt('0x'+word),false);return v.getFloat64(0,false);}
function point(p,r,color){const m=new THREE.Mesh(new THREE.SphereGeometry(r,14,10),new THREE.MeshStandardMaterial({color,roughness:.65}));m.position.set(...p);group.add(m);}
function line(a,b,color){group.add(new THREE.Line(new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(...a),new THREE.Vector3(...b)]),new THREE.LineBasicMaterial({color})));}
function clear(){group.traverse(o=>{o.geometry?.dispose();if(Array.isArray(o.material))o.material.forEach(m=>m.dispose());else o.material?.dispose();});group.clear();}
export function draw(row){clear();holder.dataset.case=row.id;holder.dataset.decision=row.candidate.decision.kind;holder.dataset.drawable='false';holder.dataset.drones='0';
 const prepared=row.prepared.prepared;if(row.prepared.rejection||!prepared){document.getElementById('geometry-note').textContent='Preparation was rejected. No admitted geometry is drawn; the complete raw input and refusal remain in the saved record.';return;}
 const drones=[prepared.receiver,prepared.source],centers=drones.map(d=>d.center.map(number));
 if(centers.flat().some(x=>!Number.isFinite(x))){document.getElementById('geometry-note').textContent='Geometry is outside finite display range. The record remains available below.';return;}
 // Translate by the receiver center for display only; preserve saved differences.
 const origin=centers[0],relative=w=>w.map((x,k)=>number(x)-origin[k]);const positions=drones.map(d=>relative(d.center));
 const distance=new THREE.Vector3(...positions[1]).length();if(!Number.isFinite(distance)){document.getElementById('geometry-note').textContent='Separation exceeds display range. This case remains visible as a saved numerical record.';return;}
 const span=Math.max(.35,distance),marker=Math.max(.018,span*.012),colors=[0x8fb8ff,0xffbd79];
 drones.forEach((d,k)=>{const c=positions[k];point(c,marker,colors[k]);d.points.forEach((p,r)=>{const v=relative(p);line(c,v,colors[k]);point(v,marker*.45,k===0&&r===row.input.rotor?0xfff079:colors[k]);});const axis=new THREE.Vector3(...d.axis.map(number));if(axis.length()>0){axis.normalize();group.add(new THREE.ArrowHelper(axis,new THREE.Vector3(...c),span*.16,colors[k],span*.035,span*.018));}});
 const color=row.candidate.decision.kind==='zero'?0x6fdec5:row.candidate.result.status==='positive'?0xf6cc78:0xfa968f;line(positions[1],relative(prepared.receiver.points[row.input.rotor]),color);
 const middle=new THREE.Vector3(...positions[1]).multiplyScalar(.5);orbit.target.copy(middle);camera.position.copy(middle).add(new THREE.Vector3(span*1.1,-span*1.65,span*.9));camera.near=Math.max(.00001,span/10000);camera.far=span*20;camera.updateProjectionMatrix();orbit.update();holder.dataset.drawable='true';holder.dataset.drones='2';
 document.getElementById('geometry-note').textContent='Blue: receiver. Orange: source. Yellow: tested rotor. Lines indicate the tested pair, not an airflow field. Axes and markers are enlarged for visibility; positions use saved prepared words and a translated display origin. Drag to orbit; scroll or pinch to zoom.';
}
function resize(){const w=holder.clientWidth,h=holder.clientHeight;if(w&&h){renderer.setSize(w,h,false);camera.aspect=w/h;camera.updateProjectionMatrix();}}new ResizeObserver(resize).observe(holder);function frame(){requestAnimationFrame(frame);orbit.update();renderer.render(scene,camera);}resize();frame();
