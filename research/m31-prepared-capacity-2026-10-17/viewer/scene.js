import * as THREE from 'three';
import {OrbitControls} from '../../../outputs/step02b-source/vendor/OrbitControls.js';
// Display saved poses and saved proof partitions only; no dynamics or load solver.
export function createScene(host,expose){
 const scene=new THREE.Scene();scene.background=new THREE.Color('#0b1922');
 const camera=new THREE.PerspectiveCamera(43,1,.01,1000);camera.up.set(0,0,1);
 const renderer=new THREE.WebGLRenderer({antialias:true});renderer.setPixelRatio(Math.min(devicePixelRatio,2));host.appendChild(renderer.domElement);
 const orbit=new OrbitControls(camera,renderer.domElement);orbit.enableDamping=true;
 scene.add(new THREE.HemisphereLight(0xdaf5ff,0x293b48,2.5));const light=new THREE.DirectionalLight(0xffffff,2);light.position.set(2,-4,8);scene.add(light);
 const group=new THREE.Group();scene.add(group);const proofBoxes=new THREE.Group();scene.add(proofBoxes);
 const geometries=[new THREE.BoxGeometry(.05,.035,.02)];
 for(const angle of [Math.PI/4,-Math.PI/4]){const g=new THREE.BoxGeometry(.10,.008,.006);g.rotateZ(angle);geometries.push(g);}
 for(const [x,y]of [[.028,.028],[-.028,.028],[-.028,-.028],[.028,-.028]]){const g=new THREE.CylinderGeometry(.023,.023,.002,12);g.rotateX(Math.PI/2);g.translate(x,y,0);geometries.push(g);}
 const meshes=geometries.map(g=>{const mesh=new THREE.InstancedMesh(g,new THREE.MeshStandardMaterial({color:0xffffff,roughness:.65}),180);mesh.frustumCulled=false;group.add(mesh);return mesh;});group.visible=false;
 const grid=new THREE.GridHelper(12,24,0x365166,0x1c303f);grid.rotation.x=Math.PI/2;scene.add(grid);
 const links=new THREE.LineSegments(new THREE.BufferGeometry(),new THREE.LineBasicMaterial({color:0xffc46c,transparent:true,opacity:.65}));scene.add(links);
 const marker=new THREE.Mesh(new THREE.SphereGeometry(.045,12,8),new THREE.MeshBasicMaterial({color:0xb1fff0}));marker.visible=false;scene.add(marker);
 const colors={self:'#b1fff0',positive:'#ffc46c',zero:'#659eff',scalar:'#8b9eac'};
 let current=null,bounds=null,boxesVisible=true;
 function emit(){if(!current)return;camera.updateMatrixWorld();expose({positions:Array.from({length:current.poses.length},(_,i)=>{const m=new THREE.Matrix4();meshes[0].getMatrixAt(i,m);return m.elements.slice(12,15);}),colors:Array.from({length:current.poses.length},(_,i)=>{const c=new THREE.Color();meshes[0].getColorAt(i,c);return c.toArray();}),kinds:[...current.kinds],bodyCount:current.poses.length,groupCount:proofBoxes.children.length,boxesVisible,selectedRotor:current.rotorPoint,camera:camera.position.toArray(),projection:camera.projectionMatrix.toArray(),view:camera.matrixWorldInverse.toArray(),aspect:camera.aspect});}
 function reset(){if(!bounds)return;orbit.enableDamping=false;orbit.update();const s=bounds.getBoundingSphere(new THREE.Sphere());const v=THREE.MathUtils.degToRad(camera.fov)/2,h=Math.atan(Math.tan(v)*camera.aspect),d=Math.max(.5,s.radius)/Math.sin(Math.min(v,h))*1.13;camera.position.copy(s.center).addScaledVector(new THREE.Vector3(.95,-1.25,.8).normalize(),d);orbit.target.copy(s.center);orbit.update();orbit.enableDamping=true;emit();}
 function show(snapshot,refit=false){current=snapshot;const t=new THREE.Object3D();t.scale.setScalar(3);bounds=new THREE.Box3();
  snapshot.poses.forEach((p,i)=>{t.position.set(...p.position);t.quaternion.set(...p.quaternion);t.updateMatrix();for(const m of meshes){m.setMatrixAt(i,t.matrix);m.setColorAt(i,new THREE.Color(colors[snapshot.kinds[i]]));}bounds.expandByPoint(t.position);});bounds.expandByScalar(.24);
  for(const m of meshes){m.count=snapshot.poses.length;m.instanceMatrix.needsUpdate=true;m.instanceColor.needsUpdate=true;}group.visible=true;
  while(proofBoxes.children.length){const b=proofBoxes.children[0];proofBoxes.remove(b);b.geometry.dispose();b.material.dispose();}
  for(const box of snapshot.boxes){const b=new THREE.Box3(new THREE.Vector3(...box.min),new THREE.Vector3(...box.max)).expandByScalar(.025);const helper=new THREE.Box3Helper(b,0x426cb1);helper.material.transparent=true;helper.material.opacity=.45;proofBoxes.add(helper);}
  proofBoxes.visible=boxesVisible;const p=[];snapshot.kinds.forEach((k,i)=>{if(k==='positive')p.push(...snapshot.rotorPoint,...snapshot.poses[i].position);});links.geometry.dispose();links.geometry=new THREE.BufferGeometry();links.geometry.setAttribute('position',new THREE.Float32BufferAttribute(p,3));
  marker.position.set(...snapshot.rotorPoint);marker.visible=true;const center=bounds.getCenter(new THREE.Vector3());grid.position.set(center.x,center.y,bounds.min.z-.1);
  if(refit)reset();emit();
 }
 function toggle(value){boxesVisible=value;proofBoxes.visible=value;emit();}
 function clear(){current=null;group.visible=false;proofBoxes.visible=false;links.visible=false;marker.visible=false;}
 function resize(){const r=host.getBoundingClientRect();if(!r.width||!r.height)return;renderer.setSize(r.width,r.height,false);camera.aspect=r.width/r.height;camera.updateProjectionMatrix();reset();}
 orbit.addEventListener('change',emit);new ResizeObserver(resize).observe(host);resize();
 function animate(){requestAnimationFrame(animate);orbit.update();renderer.render(scene,camera);}animate();
 return{show,toggle,reset,clear};
}
