import * as THREE from 'three';
import {OrbitControls} from '../../../outputs/step02b-source/vendor/OrbitControls.js';
// Recorded-state display only. Adapted from the prior native-fresh viewer.
// No solver, coefficient builder, load reconstruction or trajectory interpolation.
export function createRecordedScene(host,onChange){
 const scene=new THREE.Scene();scene.background=new THREE.Color('#0a141d');
 const camera=new THREE.PerspectiveCamera(43,1,.01,1000);camera.up.set(0,0,1);
 const renderer=new THREE.WebGLRenderer({antialias:true});renderer.setPixelRatio(Math.min(devicePixelRatio,2));host.appendChild(renderer.domElement);
 const controls=new OrbitControls(camera,renderer.domElement);controls.enableDamping=true;controls.dampingFactor=.09;
 scene.add(new THREE.HemisphereLight(0xd9f8ff,0x223445,2));const light=new THREE.DirectionalLight(0xffffff,2);light.position.set(3,-4,10);scene.add(light);
 const bodies=new THREE.Group();scene.add(bodies);bodies.visible=false;
 const body=new THREE.InstancedMesh(new THREE.BoxGeometry(.048,.035,.018),new THREE.MeshStandardMaterial({color:0xffffff,roughness:.5}),64);bodies.add(body);
 const armGeometry=new THREE.BoxGeometry(.09,.007,.005);armGeometry.rotateZ(Math.PI/4);
 const arm1=new THREE.InstancedMesh(armGeometry,new THREE.MeshStandardMaterial({color:'#d3e4ea'}),64);bodies.add(arm1);
 const arm2Geometry=armGeometry.clone();arm2Geometry.rotateZ(Math.PI/2);const arm2=new THREE.InstancedMesh(arm2Geometry,arm1.material,64);bodies.add(arm2);
 const rotors=[];for(const [x,y]of [[.028,.028],[-.028,.028],[-.028,-.028],[.028,-.028]]){
  const geometry=new THREE.CylinderGeometry(.023,.023,.002,12);geometry.rotateX(Math.PI/2);geometry.translate(x,y,0);
  const mesh=new THREE.InstancedMesh(geometry,new THREE.MeshStandardMaterial({color:'#87adbd',transparent:true,opacity:.65}),64);bodies.add(mesh);rotors.push(mesh);
 }
 const meshes=[body,arm1,arm2,...rotors],transform=new THREE.Object3D();transform.scale.setScalar(3);
 const positions=new Float32Array(64*6),colors=new Float32Array(64*6),geometry=new THREE.BufferGeometry();
 geometry.setAttribute('position',new THREE.BufferAttribute(positions,3).setUsage(THREE.DynamicDrawUsage));
 geometry.setAttribute('color',new THREE.BufferAttribute(colors,3).setUsage(THREE.DynamicDrawUsage));geometry.setDrawRange(0,0);
 const lines=new THREE.LineSegments(geometry,new THREE.LineBasicMaterial({vertexColors:true,transparent:true,opacity:.9}));lines.frustumCulled=false;scene.add(lines);
 const heads=new THREE.InstancedMesh(new THREE.ConeGeometry(1,1,10),new THREE.MeshBasicMaterial({color:0xffffff}),64);heads.count=0;heads.frustumCulled=false;scene.add(heads);
 const grid=new THREE.GridHelper(14,28,0x46616e,0x1b3342);grid.rotation.x=Math.PI/2;scene.add(grid);
 let current=null,center=new THREE.Vector3(),extent=5,scale=2,visible=false,selectedId=0,arrowCount=0,segments=[],fitBounds=null;
 const yAxis=new THREE.Vector3(0,1,0),direction=new THREE.Vector3(),tip=new THREE.Vector3(),head=new THREE.Object3D();
 function reset(){
  const damping=controls.enableDamping;controls.enableDamping=false;controls.update();
  const sphere=fitBounds?fitBounds.getBoundingSphere(new THREE.Sphere()):new THREE.Sphere(center.clone(),Math.max(1,extent/2));
  const vertical=THREE.MathUtils.degToRad(camera.fov)/2,horizontal=Math.atan(Math.tan(vertical)*camera.aspect);
  const distance=Math.max(.5,sphere.radius)/Math.sin(Math.min(vertical,horizontal))*1.12;
  camera.position.copy(sphere.center).addScaledVector(new THREE.Vector3(.95,-1.25,.8).normalize(),distance);
  camera.far=Math.max(1000,distance+sphere.radius*4);camera.updateProjectionMatrix();controls.target.copy(sphere.center);controls.update();controls.enableDamping=damping;
 }
 function setFitEnvelope(envelope){
  if(!envelope||envelope.min.length!==3||envelope.max.length!==3||!envelope.min.concat(envelope.max).every(Number.isFinite)||envelope.min.some((x,i)=>x>envelope.max[i]))throw Error('Saved camera envelope');
  // 0.23 m covers the enlarged glyph and the arrow head around saved centers/endpoints.
  fitBounds=new THREE.Box3(new THREE.Vector3(...envelope.min),new THREE.Vector3(...envelope.max)).expandByScalar(.23);
 }
 function expose(){if(!current)return;camera.updateMatrixWorld();onChange({stateId:current.id,arm:current.arm,frameType:current.kind,ids:current.ids,
  renderedBodyCount:64,positions:Array.from({length:64},(_,i)=>{const m=new THREE.Matrix4();body.getMatrixAt(i,m);return m.elements.slice(12,15);}),
  arrowScale:scale,arrowsEnabled:visible,renderedArrowCount:visible?arrowCount:0,arrowSegments:segments,
  uploadedArrowPositions:Array.from(positions.slice(0,arrowCount*6)),selectedId,camera:camera.position.toArray(),
  cameraProjection:camera.projectionMatrix.toArray(),cameraWorldInverse:camera.matrixWorldInverse.toArray(),cameraAspect:camera.aspect,
  fitBounds:fitBounds?{min:fitBounds.min.toArray(),max:fitBounds.max.toArray()}:null,playing:false});}
 controls.addEventListener('change',expose);
 function arrows(){
  geometry.setDrawRange(0,0);heads.count=0;arrowCount=0;segments=[];
  if(!current)return;
  for(let i=0;i<64;i++){
   const origin=current.poses[i].position,force=current.worldForces?.[i]??null;
   const color=new THREE.Color(current.ids[i]===selectedId?'#ffe3a6':'#f8b54d');
   body.setColorAt(i,new THREE.Color(current.ids[i]===selectedId?'#ffe3a6':current.arm==='off'?'#8dbaff':'#67dfc5'));
   if(force===null)continue;direction.set(...force);const length=direction.length()*scale;if(length===0)continue;
   direction.normalize();tip.set(origin[0]+force[0]*scale,origin[1]+force[1]*scale,origin[2]+force[2]*scale);
   const segment=[...origin,...tip.toArray()];positions.set(segment,6*arrowCount);colors.set([...color.toArray(),...color.toArray()],6*arrowCount);
   const headLength=Math.min(.18,length*.24);head.position.copy(tip).addScaledVector(direction,-headLength/2);
   head.quaternion.setFromUnitVectors(yAxis,direction);head.scale.set(headLength*.34,headLength,headLength*.34);head.updateMatrix();heads.setMatrixAt(arrowCount,head.matrix);heads.setColorAt(arrowCount,color);
   segments.push({id:current.ids[i],force:[...force],endpoints:segment});arrowCount++;
  }
  geometry.attributes.position.needsUpdate=true;geometry.attributes.color.needsUpdate=true;geometry.setDrawRange(0,visible?arrowCount*2:0);
  heads.count=visible?arrowCount:0;heads.instanceMatrix.needsUpdate=true;if(heads.instanceColor)heads.instanceColor.needsUpdate=true;if(body.instanceColor)body.instanceColor.needsUpdate=true;
  expose();
 }
 function setSnapshot(snapshot,resetCamera=false){
  if(snapshot.poses.length!==64||snapshot.ids.length!==64||(snapshot.worldForces!==null&&snapshot.worldForces.length!==64))throw Error('Saved scene shape');
  const finite=values=>values.every(Number.isFinite);
  if(snapshot.poses.some(p=>p.position.length!==3||p.quaternion.length!==4||!finite([...p.position,...p.quaternion]))||(snapshot.worldForces!==null&&snapshot.worldForces.some(f=>f.length!==3||!finite(f))))throw Error('Saved scene word range');
  current=snapshot;geometry.setDrawRange(0,0);heads.count=0;bodies.visible=false;
  const bounds=new THREE.Box3();
  for(let i=0;i<64;i++){
   const pose=current.poses[i];transform.position.set(...pose.position);transform.quaternion.set(...pose.quaternion);transform.updateMatrix();for(const mesh of meshes)mesh.setMatrixAt(i,transform.matrix);bounds.expandByPoint(transform.position);
  }
  for(const mesh of meshes){mesh.instanceMatrix.needsUpdate=true;mesh.frustumCulled=false;}
  center=bounds.getCenter(new THREE.Vector3());extent=Math.max(3,bounds.getSize(new THREE.Vector3()).length());grid.position.set(center.x,center.y,bounds.min.z-.3);
  if(resetCamera)reset();bodies.visible=true;arrows();
 }
 function style(options){if(options.scale!==2)throw Error('Arrow display scale');scale=options.scale;visible=options.visible;selectedId=options.selectedId;arrows();}
 function clear(){current=null;bodies.visible=false;geometry.setDrawRange(0,0);heads.count=0;arrowCount=0;segments=[];}
 function resize(){const r=host.getBoundingClientRect();if(r.width<=0||r.height<=0)return;renderer.setSize(r.width,r.height,false);camera.aspect=r.width/r.height;camera.updateProjectionMatrix();if(current&&fitBounds)reset();expose();}
 function animate(){requestAnimationFrame(animate);controls.update();renderer.render(scene,camera);}
 new ResizeObserver(resize).observe(host);reset();resize();requestAnimationFrame(animate);
 return {setSnapshot,setFitEnvelope,style,reset,clear};
}
