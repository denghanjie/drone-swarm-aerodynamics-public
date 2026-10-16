import * as THREE from 'three';
import {OrbitControls} from '../../../outputs/step02b-source/vendor/OrbitControls.js';
export function createScene(host){
 const renderer=new THREE.WebGLRenderer({antialias:true});renderer.setPixelRatio(Math.min(devicePixelRatio,2));renderer.setClearColor('#102431');host.append(renderer.domElement);
 const scene=new THREE.Scene(),camera=new THREE.PerspectiveCamera(42,1,.01,3000);camera.up.set(0,0,1);const controls=new OrbitControls(camera,renderer.domElement);controls.enableDamping=false;
 scene.add(new THREE.HemisphereLight(0xd5f5ff,0x325149,3));const light=new THREE.DirectionalLight(0xffffff,2);light.position.set(10,-20,50);scene.add(light);
 let group=new THREE.Group(),center=new THREE.Vector3(),fitRadius=1,record,poses,scale=4;scene.add(group);const render=()=>renderer.render(scene,camera);controls.addEventListener('change',render);
 function reset(){const v=THREE.MathUtils.degToRad(camera.fov)/2,h=Math.atan(Math.tan(v)*camera.aspect),d=1.12*fitRadius/Math.sin(Math.min(v,h));camera.position.copy(center).add(new THREE.Vector3(1,-1.6,1).normalize().multiplyScalar(d));controls.target.copy(center);controls.update();render();}
 function build(){scene.remove(group);group.traverse(o=>{o.geometry?.dispose();if(Array.isArray(o.material))o.material.forEach(m=>m.dispose());else o.material?.dispose();});group=new THREE.Group();scene.add(group);
  const rejected=new Set(record.rejectedVehicles);
  const n=record.n,bounds=new THREE.Box3();for(let i=0;i<n;i++)bounds.expandByPoint(new THREE.Vector3(...poses.slice(17*i,17*i+3)));center=bounds.getCenter(new THREE.Vector3());fitRadius=bounds.getSize(new THREE.Vector3()).length()/2+1;
  const span=Math.max(bounds.max.x-bounds.min.x,bounds.max.y-bounds.min.y,2),grid=new THREE.GridHelper(span*1.15,20,0x47717d,0x25404d);grid.rotation.x=Math.PI/2;grid.position.set(center.x,center.y,bounds.min.z-.3);group.add(grid);
  const mat=new THREE.MeshStandardMaterial({color:0xffffff,roughness:.7}),body=new THREE.InstancedMesh(new THREE.BoxGeometry(.075,.075,.018),mat,n),rotors=new THREE.InstancedMesh(new THREE.TorusGeometry(.023,.0035,4,10),mat,4*n),obj=new THREE.Object3D(),p=new THREE.Vector3(),q=new THREE.Quaternion(),o=new THREE.Vector3(),corners=[[.028,.028,0],[-.028,.028,0],[-.028,-.028,0],[.028,-.028,0]],color=new THREE.Color(),blue=new THREE.Color('#53c2da'),amber=new THREE.Color('#eab86b');
  for(let i=0;i<n;i++){p.fromArray(poses,17*i);q.fromArray(poses,17*i+6);obj.position.copy(p);obj.quaternion.copy(q);obj.scale.setScalar(scale);obj.updateMatrix();body.setMatrixAt(i,obj.matrix);
   if(rejected.has(i))color.set('#ff746d');else if(record.solutions){const ratio=record.solutions.direct.y[i]**2;color.copy(amber).lerp(blue,Math.max(0,Math.min(1,ratio)));}else color.copy(blue);
   body.setColorAt(i,color);for(let r=0;r<4;r++){o.fromArray(corners[r]).multiplyScalar(scale).applyQuaternion(q);obj.position.copy(p).add(o);obj.updateMatrix();rotors.setMatrixAt(4*i+r,obj.matrix);rotors.setColorAt(4*i+r,color);}}
  group.add(body,rotors);
  if(record.rejectionEdges.length){const points=[];for(const [j,i] of record.rejectionEdges){points.push(...poses.slice(j*17,j*17+3),...poses.slice(i*17,i*17+3));}const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.Float32BufferAttribute(points,3));group.add(new THREE.LineSegments(g,new THREE.LineBasicMaterial({color:0xff746d,transparent:true,opacity:.65})));}
  host.dataset.instances=String(n);host.dataset.size=String(scale);render();
 }
 function load(c,s){record=c;poses=s;build();reset();}function size(v){scale=v;if(record)build();}
 new ResizeObserver(()=>{const r=host.getBoundingClientRect();renderer.setSize(r.width,r.height,false);camera.aspect=r.width/r.height;camera.updateProjectionMatrix();reset();}).observe(host);return {load,size,reset};
}
