import * as THREE from 'three';
import {OrbitControls} from '../../../outputs/step02b-source/vendor/OrbitControls.js';
export function createScene(host){
  const renderer=new THREE.WebGLRenderer({antialias:true});renderer.setPixelRatio(Math.min(devicePixelRatio,2));renderer.setClearColor('#102431');host.append(renderer.domElement);
  const scene=new THREE.Scene(),camera=new THREE.PerspectiveCamera(40,1,.001,100);camera.up.set(0,0,1);
  const controls=new OrbitControls(camera,renderer.domElement);controls.enableDamping=false;
  scene.add(new THREE.HemisphereLight(0xc7e5ff,0x435548,3));const light=new THREE.DirectionalLight(0xffffff,3);light.position.set(2,-1,5);scene.add(light);
  let group=new THREE.Group(),nodes=[],center=new THREE.Vector3(),span=1,fitRadius=1;scene.add(group);
  const render=()=>renderer.render(scene,camera);controls.addEventListener('change',render);
  function reset(){const vertical=THREE.MathUtils.degToRad(camera.fov)/2,horizontal=Math.atan(Math.tan(vertical)*camera.aspect),distance=1.18*fitRadius/Math.sin(Math.min(vertical,horizontal));camera.position.copy(center).add(new THREE.Vector3(1.25,-1.5,.8).normalize().multiplyScalar(distance));controls.target.copy(center);controls.update();render();}
  function label(text,p,size){const cv=document.createElement('canvas');cv.width=128;cv.height=64;const ctx=cv.getContext('2d');ctx.fillStyle='#e4f2f1';ctx.font='bold 30px system-ui';ctx.textAlign='center';ctx.fillText(text,64,42);const texture=new THREE.CanvasTexture(cv),sprite=new THREE.Sprite(new THREE.SpriteMaterial({map:texture,depthTest:false,transparent:true}));sprite.position.copy(p);sprite.scale.set(size,size/2,1);return sprite;}
  function line(points,color,opacity=1){return new THREE.Line(new THREE.BufferGeometry().setFromPoints(points),new THREE.LineBasicMaterial({color,transparent:true,opacity}));}
  function load(c){
    scene.remove(group);group.traverse(o=>{o.geometry?.dispose();if(o.material){o.material.map?.dispose();o.material.dispose();}});group=new THREE.Group();scene.add(group);nodes=[];
    const bounds=new THREE.Box3();c.vehicles.forEach(v=>bounds.expandByPoint(new THREE.Vector3(...v.q)));center=bounds.getCenter(new THREE.Vector3());const extent=bounds.getSize(new THREE.Vector3()).length();span=Math.max(.18,extent*.7);fitRadius=extent/2+.12;
    const grid=new THREE.GridHelper(span*2,12,0x47717d,0x24424f);grid.rotation.x=Math.PI/2;grid.position.set(center.x,center.y,bounds.min.z-.09);group.add(grid);
    for(const v of c.vehicles){const q=new THREE.Vector3(...v.q),axis=new THREE.Vector3(...v.axis),mat=new THREE.MeshStandardMaterial({color:0x51bad0,roughness:.5,metalness:.2}),body=new THREE.Mesh(new THREE.SphereGeometry(.018,16,10),mat);body.position.copy(q);group.add(body);
      const rotors=[];for(const o of v.offsets){const p=q.clone().add(new THREE.Vector3(...o));group.add(line([q,p],0x94b6be));const rotor=new THREE.Mesh(new THREE.TorusGeometry(.023,.0025,6,26),mat);rotor.position.copy(p);rotor.quaternion.setFromUnitVectors(new THREE.Vector3(0,0,1),axis);group.add(rotor);rotors.push(rotor);}
      group.add(new THREE.ArrowHelper(axis,q,.08,0xb6c4ff,.013,.007));group.add(label(String(v.id),q.clone().add(new THREE.Vector3(.065,0,.035)),Math.max(.045,span*.05)));nodes.push({mat,body,rotors});
    }
    let edges=c.graph.edges,color=c.id==='hexagon-cycle'?0xe7ba61:0x49bfa7;
    if(!c.admission.admitted){edges=[...new Set(c.pairs.filter(p=>p.symbol===4||p.symbol===11).map(p=>`${p.j},${p.i}`))].map(s=>s.split(',').map(Number));color=0xff6f66;}
    for(const [j,i] of edges){const a=new THREE.Vector3(...c.vehicles[j].q),b=new THREE.Vector3(...c.vehicles[i].q),dir=b.clone().sub(a),length=dir.length();dir.normalize();if(length>.09){group.add(new THREE.ArrowHelper(dir,a.clone().addScaledVector(dir,.04),length-.08,color,Math.min(.035,length*.12),Math.min(.015,length*.07)));}else group.add(line([a,b],color));}
    reset();
  }
  function state(y,rejected){for(let i=0;i<nodes.length;i++){const ratio=y?.[i]**2;nodes[i].mat.color.set(rejected?'#ff7568':'#efb45d');if(!rejected)nodes[i].mat.color.lerp(new THREE.Color('#4fc1dc'),Math.min(1,Math.max(0,ratio)));}render();}
  new ResizeObserver(()=>{const r=host.getBoundingClientRect();renderer.setSize(r.width,r.height,false);camera.aspect=r.width/r.height;camera.updateProjectionMatrix();reset();}).observe(host);
  return {load,state,reset};
}
