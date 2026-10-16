import * as THREE from '../../../outputs/step02b-source/vendor/three.module.js';
import {OrbitControls} from '../../../outputs/step02b-source/vendor/OrbitControls.js';
const box=document.getElementById('pair-canvas'),renderer=new THREE.WebGLRenderer({antialias:true});renderer.setPixelRatio(Math.min(devicePixelRatio,2));renderer.setClearColor(0x102431);box.appendChild(renderer.domElement);
const scene=new THREE.Scene(),camera=new THREE.PerspectiveCamera(42,1,.001,5000);camera.up.set(0,0,1);const controls=new OrbitControls(camera,renderer.domElement);controls.enableDamping=true;controls.addEventListener('change',()=>{box.dataset.camera=camera.position.toArray().map(v=>v.toFixed(6)).join(',');});
scene.add(new THREE.HemisphereLight(0xffffff,0x597c8a,2));const content=new THREE.Group();scene.add(content);
const grid=new THREE.GridHelper(6,12,0x51717a,0x263d48);grid.rotation.x=Math.PI/2;grid.position.z=-.15;scene.add(grid);
function value(bits){const a=new ArrayBuffer(8),v=new DataView(a);v.setBigUint64(0,BigInt('0x'+bits));return v.getFloat64(0);}
function line(points,color,opacity=1){content.add(new THREE.Line(new THREE.BufferGeometry().setFromPoints(points.map(p=>new THREE.Vector3(...p))),new THREE.LineBasicMaterial({color,transparent:opacity<1,opacity})));}
function sphere(p,size,color){const mesh=new THREE.Mesh(new THREE.SphereGeometry(size,12,8),new THREE.MeshStandardMaterial({color,roughness:.6}));mesh.position.set(...p);content.add(mesh);}
function clear(){content.traverse(o=>{o.geometry?.dispose();if(Array.isArray(o.material))o.material.forEach(m=>m.dispose());else o.material?.dispose();});content.clear();}
function draw(record,receiverIndex=0,rotor=0){const method=record.methods[1];const row={id:record.id,...method,pairs:method.assembly.queries.flatMap(q=>q.terminals.flatMap(t=>(t.entries??[]).map(e=>({i:record.input.drones[q.i].id,r:q.r,j:record.input.drones[e.j].id,result:e.result}))))};clear();box.dataset.case=row.id;box.dataset.status=row.result.status;const valid=row.prepared.filter(d=>d.value&&[d.value.center,...d.value.points].flat().every(b=>Number.isFinite(value(b))));box.dataset.drones=valid.length;box.dataset.drawable=String(valid.length>0);if(!valid.length){document.getElementById('pair-note').textContent='No finite prepared geometry to draw. The full refused record remains saved.';return;}
 const bounds=new THREE.Box3();for(const d of valid)bounds.expandByPoint(new THREE.Vector3(...d.value.center.map(value)));const origin=bounds.getCenter(new THREE.Vector3()).toArray();const rel=a=>a.map((b,k)=>value(b)-origin[k]),byId=new Map(valid.map(d=>[d.id,d]));const loads=new Map((row.certificate?.loads??[]).map(d=>[d.id,d]));
 for(const d of valid){const p=d.value,c=rel(p.center),load=loads.get(d.id);let fraction=1;if(load){const f=load.candidate.collective;const nominal=p.forces.map(value).reduce((a,b)=>a+b,0);fraction=(Number(f.n)/Number(f.d))/nominal;}
  const color=d.rejection?0xf67f73:!load?0x839aa5:new THREE.Color().setHSL(.08+.39*Math.max(0,Math.min(1,fraction)),.65,.6);sphere(c,.025,color);for(const rotor of p.points){const t=rel(rotor);line([c,t],color);sphere(t,.012,color);}if(load){const axis=new THREE.Vector3(...p.axis.map(value));if(axis.length()>0){axis.normalize();content.add(new THREE.ArrowHelper(axis,new THREE.Vector3(...c),.22*fraction,0xf8e7ba,.04,.02));}}
 }
 let edges=0,visibleEdges=0;for(const pair of row.pairs)if(pair.result.status==='positive'&&byId.has(pair.i)&&byId.has(pair.j)){edges++;if(pair.i===record.input.drones[receiverIndex].id&&pair.r===rotor){line([rel(byId.get(pair.j).value.center),rel(byId.get(pair.i).value.points[pair.r])],0x8ea9b0,.5);visibleEdges++;}}box.dataset.visibleEdges=visibleEdges;
 box.dataset.positiveEdges=edges;
 const query=method.assembly.queries.find(q=>q.i===receiverIndex&&q.r===rotor);let zeroBoxes=0,pruned=0;
 if(method.assembly.tree&&query)for(const terminal of query.terminals){
  const node=method.assembly.tree.nodes[terminal.node];if(!node)continue;
  const a=node.center.map(v=>Number(v[0].n)/Number(v[0].d)),b=node.center.map(v=>Number(v[1].n)/Number(v[1].d));
  const box3=new THREE.Box3(new THREE.Vector3(...a.map((x,k)=>x-origin[k]-.035)),new THREE.Vector3(...b.map((x,k)=>x-origin[k]+.035)));
  content.add(new THREE.Box3Helper(box3,terminal.kind==='zero'?0x60d9cf:0xd59b63));if(terminal.kind==='zero'){zeroBoxes++;pruned+=terminal.count;}
 }
 const receiver=row.prepared[receiverIndex];if(receiver?.value){const point=rel(receiver.value.points[rotor]);sphere(point,.025,0xfff27b);}
 box.dataset.zeroBoxes=zeroBoxes;box.dataset.pruned=pruned;box.dataset.receiver=receiverIndex;box.dataset.rotor=rotor;
 document.getElementById('query-note').textContent=method.assembly.mode==='hierarchy'?'Selected receiver rotor: '+zeroBoxes+' teal zero-proof boxes covering '+pruned+' nonself source pairs. Amber boxes are scanned leaves; yellow marks the selected rotor. Boxes enclose source centers and are padded for visibility.':method.assembly.mode==='fallback'?'Global proof could not establish all bounds: complete scalar fallback, no tree.':'Preparation refused: no hierarchy or pair work.';
 const radius=Math.max(.45,bounds.getSize(new THREE.Vector3()).length()*.65);controls.target.set(0,0,0);camera.position.set(radius*1.5,-radius*1.9,radius*.95);camera.far=Math.max(1000,radius*10);camera.updateProjectionMatrix();controls.update();grid.visible=radius<10;
 document.getElementById('pair-note').textContent='Saved geometry: '+valid.length+' drones, '+edges+' positive rotor–source links in the full record; '+visibleEdges+' selected-rotor links are drawn. '+(loads.size?'Green→amber shows greater predicted thrust reduction; pale arrows show normalized force direction.':'No certified load estimate: gray indicates unavailable.')+' Refused preparation is red. Markers are enlarged for legibility; no new trajectory or airflow particles.';
}
function resize(){const w=box.clientWidth,h=box.clientHeight;if(w&&h){renderer.setSize(w,h,false);camera.aspect=w/h;camera.updateProjectionMatrix();}}new ResizeObserver(resize).observe(box);renderer.setAnimationLoop(()=>{controls.update();renderer.render(scene,camera);});export {draw};
