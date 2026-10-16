import * as THREE from '../../../outputs/step02b-source/vendor/three.module.js';
import {OrbitControls} from '../../../outputs/step02b-source/vendor/OrbitControls.js';
const box=document.getElementById('pair-canvas'),renderer=new THREE.WebGLRenderer({antialias:true});renderer.setPixelRatio(Math.min(devicePixelRatio,2));renderer.setClearColor(0x102431);box.appendChild(renderer.domElement);
const scene=new THREE.Scene(),camera=new THREE.PerspectiveCamera(45,1,.001,2000),controls=new OrbitControls(camera,renderer.domElement);controls.enableDamping=true;camera.up.set(0,0,1);
scene.add(new THREE.HemisphereLight(0xffffff,0x597c8a,2));const content=new THREE.Group();scene.add(content);
const grid=new THREE.GridHelper(6,12,0x51717a,0x263d48);grid.rotation.x=Math.PI/2;grid.position.z=-.12;scene.add(grid);scene.add(new THREE.AxesHelper(.3));
function value(bits){const a=new ArrayBuffer(8),v=new DataView(a);v.setBigUint64(0,BigInt('0x'+bits));return v.getFloat64(0);}
function line(points,color){const g=new THREE.BufferGeometry().setFromPoints(points.map(p=>new THREE.Vector3(...p)));content.add(new THREE.Line(g,new THREE.LineBasicMaterial({color})));}
function sphere(p,size,color){const mesh=new THREE.Mesh(new THREE.SphereGeometry(size,12,8),new THREE.MeshStandardMaterial({color,roughness:.6}));mesh.position.set(...p);content.add(mesh);}
function clear(){for(const o of [...content.children]){o.geometry?.dispose();o.material?.dispose();content.remove(o);}}
function draw(row){clear();box.dataset.case=row.id;box.dataset.status=row.result.status;const prepared=row.prepared;if(!prepared){box.dataset.drawable='false';document.getElementById('pair-note').textContent='Input rejected before geometry preparation. No drawable prepared geometry for this record.';return;}
 const p=prepared.receiver,s=prepared.source,origin=p.center.map(value);const rel=a=>a.map((b,i)=>value(b)-origin[i]);const all=[p,s].flatMap(x=>[x.center,...x.points]);if(all.some(a=>rel(a).some(v=>!Number.isFinite(v)))){box.dataset.drawable='false';document.getElementById('pair-note').textContent='Prepared geometry is nonfinite; the record is retained without drawing it.';return;}
 box.dataset.drawable='true';for(const [drone,color] of [[p,0x4fe1c1],[s,0xffba72]]){const c=rel(drone.center),axis=drone.axis.map(value);sphere(c,.025,color);for(const a of drone.points){const t=rel(a);line([c,t],color);sphere(t,.012,color);}line([c,c.map((x,i)=>x+.25*axis[i])],color);}
 line([rel(s.center),rel(p.points[row.input.rotor])],row.result.status==='positive'?0xf9e7b3:0x7b939b);
 const sc=rel(s.center),radius=Math.max(.4,Math.hypot(...sc));controls.target.set(sc[0]/2,sc[1]/2,sc[2]/2);camera.position.set(sc[0]/2+radius*1.5,sc[1]/2-radius*1.8,sc[2]/2+radius);camera.far=Math.max(1000,radius*10);camera.updateProjectionMatrix();controls.update();
 document.getElementById('pair-note').textContent='Saved prepared geometry only. Teal: receiver; amber: source. Short lines show each supplied axis. Pale connector identifies the tested receiver rotor. Body/rotor markers enlarged for legibility; no airflow particles or simulated trajectory.';
}
function resize(){const w=box.clientWidth,h=box.clientHeight;if(!w||!h)return;renderer.setSize(w,h,false);camera.aspect=w/h;camera.updateProjectionMatrix();}new ResizeObserver(resize).observe(box);resize();renderer.setAnimationLoop(()=>{controls.update();renderer.render(scene,camera);});
export {draw};
