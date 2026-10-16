import * as THREE from 'three';
import {OrbitControls} from '../../../outputs/step02b-source/vendor/OrbitControls.js';
// Geometry and recorded-word rendering adapted from the validator/moving viewer.
// This module contains no scientific method, generator, or aerodynamic query.
const dv=new DataView(new ArrayBuffer(8));
function number(word){if(typeof word!=='string'||!/^[0-9a-f]{16}$/.test(word))throw Error('Invalid saved pose word');dv.setUint32(0,parseInt(word.slice(0,8),16),false);dv.setUint32(4,parseInt(word.slice(8),16),false);const x=dv.getFloat64(0,false);if(!Number.isFinite(x))throw Error('Nonfinite saved pose');return x;}
export function createReplay(host,onFrame){
 let frames=[],frame=0,run=null,playing=false,last=0,center=new THREE.Vector3(),extent=5;
 const scene=new THREE.Scene();scene.background=new THREE.Color('#0a141d');
 const camera=new THREE.PerspectiveCamera(43,1,.01,1000);camera.up.set(0,0,1);
 const renderer=new THREE.WebGLRenderer({antialias:true});renderer.setPixelRatio(Math.min(devicePixelRatio,2));host.appendChild(renderer.domElement);
 const controls=new OrbitControls(camera,renderer.domElement);controls.enableDamping=true;controls.dampingFactor=.09;
 scene.add(new THREE.HemisphereLight(0xd9f8ff,0x223445,2));const light=new THREE.DirectionalLight(0xffffff,2);light.position.set(3,-4,10);scene.add(light);
 const group=new THREE.Group();scene.add(group);group.visible=false;
 const body=new THREE.InstancedMesh(new THREE.BoxGeometry(.048,.035,.018),new THREE.MeshStandardMaterial({color:'#67dfc5',roughness:.5}),64);group.add(body);
 const armGeom=new THREE.BoxGeometry(.09,.007,.005);armGeom.rotateZ(Math.PI/4);const arms1=new THREE.InstancedMesh(armGeom,new THREE.MeshStandardMaterial({color:'#d3e4ea'}),64);group.add(arms1);
 const armGeom2=armGeom.clone();armGeom2.rotateZ(Math.PI/2);const arms2=new THREE.InstancedMesh(armGeom2,arms1.material,64);group.add(arms2);
 const rotorMeshes=[];for(const [x,y]of [[.028,.028],[-.028,.028],[-.028,-.028],[.028,-.028]]){const g=new THREE.CylinderGeometry(.023,.023,.002,12);g.rotateX(Math.PI/2);g.translate(x,y,0);const m=new THREE.InstancedMesh(g,new THREE.MeshStandardMaterial({color:'#87adbd',transparent:true,opacity:.65}),64);group.add(m);rotorMeshes.push(m);}
 const meshes=[body,arms1,arms2,...rotorMeshes];const axisPositions=new Float32Array(64*6),axisGeometry=new THREE.BufferGeometry();axisGeometry.setAttribute('position',new THREE.BufferAttribute(axisPositions,3));const axes=new THREE.LineSegments(axisGeometry,new THREE.LineBasicMaterial({color:'#efb26a',transparent:true,opacity:.8}));group.add(axes);
 const grid=new THREE.GridHelper(14,28,0x46616e,0x1b3342);grid.rotation.x=Math.PI/2;scene.add(grid);
 const object=new THREE.Object3D();object.scale.setScalar(3);const tip=new THREE.Vector3();
 function reset(){const damping=controls.enableDamping;controls.enableDamping=false;controls.update();camera.position.copy(center).add(new THREE.Vector3(extent*.95,-extent*1.25,extent*.8));controls.target.copy(center);controls.update();controls.enableDamping=damping;}
 function resize(){const r=host.getBoundingClientRect();if(r.width<=0||r.height<=0)return;renderer.setSize(r.width,r.height,false);camera.aspect=r.width/r.height;camera.updateProjectionMatrix();}
 function draw(){const f=frames[frame];if(!f)return;for(let i=0;i<64;i++){const w=f.words.slice(7*i,7*i+7).map(number);object.position.set(w[0],w[1],w[2]);object.quaternion.set(w[3],w[4],w[5],w[6]);object.updateMatrix();for(const m of meshes)m.setMatrixAt(i,object.matrix);tip.set(0,0,.23).applyQuaternion(object.quaternion).add(object.position);axisPositions.set([w[0],w[1],w[2],tip.x,tip.y,tip.z],6*i);}for(const m of meshes){m.instanceMatrix.needsUpdate=true;m.frustumCulled=false;}axisGeometry.attributes.position.needsUpdate=true;axes.frustumCulled=false;group.visible=true;onFrame({run,frame,t:f.t,wordCount:f.words.length,bodyCount:64,playing,positions:Array.from({length:64},(_,i)=>{const m=new THREE.Matrix4();body.getMatrixAt(i,m);return m.elements.slice(12,15);}),camera:camera.position.toArray()});}
 function setFrames(id,saved){playing=false;run=id;frames=saved;frame=0;group.visible=false;if(!frames.length)return;let prior=-1;const bounds=new THREE.Box3();for(const f of frames){if(typeof f.t!=='number'||!Number.isFinite(f.t)||f.t<0||f.t>10||f.t<=prior||!Array.isArray(f.words)||f.words.length!==448)throw Error('Invalid saved pose frame');prior=f.t;for(let i=0;i<64;i++){const w=f.words.slice(7*i,7*i+7).map(number);bounds.expandByPoint(new THREE.Vector3(...w.slice(0,3)));}}center=bounds.getCenter(new THREE.Vector3());extent=Math.max(3,bounds.getSize(new THREE.Vector3()).length());grid.position.set(center.x,center.y,bounds.min.z-.3);reset();draw();}
 function seek(value){if(!Number.isInteger(value)||value<0||value>=frames.length)return;playing=false;frame=value;draw();}
 function play(value){playing=Boolean(value)&&frames.length>0;last=performance.now();draw();return playing;}
 function animate(t){requestAnimationFrame(animate);if(playing&&frames.length&&t-last>=200){frame=(frame+1)%frames.length;last=t;draw();}controls.update();renderer.render(scene,camera);}
 new ResizeObserver(resize).observe(host);reset();resize();requestAnimationFrame(animate);
 return {setFrames,seek,play,reset,camera:()=>camera.position.toArray()};
}
