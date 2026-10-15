import * as T from '../../../outputs/step02b-source/vendor/three.module.js';
import {OrbitControls} from '../../../outputs/step02b-source/vendor/OrbitControls.js';

// Display transforms only. Positions/quaternions and pair axes come from saved bytes.
export function createScene(host,onSelect) {
  host.replaceChildren();
  const scene=new T.Scene(),content=new T.Group(),marker=new T.Group();scene.background=new T.Color('#102031');scene.add(content,marker);
  const camera=new T.PerspectiveCamera(45,1,.001,100000);camera.up.set(0,0,1);
  const renderer=new T.WebGLRenderer({antialias:true});renderer.setPixelRatio(Math.min(devicePixelRatio,2));host.append(renderer.domElement);
  renderer.domElement.setAttribute('aria-label','Static saved positions. Use the receiver input for keyboard selection.');
  const orbit=new OrbitControls(camera,renderer.domElement);orbit.enableDamping=false;
  scene.add(new T.HemisphereLight(0xffffff,0x536075,3));
  const light=new T.DirectionalLight(0xffffff,2);light.position.set(5,-10,30);scene.add(light);
  let body=null,arms=null,poses=[],pair=null,selected=0,disposed=false,displayScale=.1,pointer=null;
  const bounds=new T.Box3(),matrix=new T.Matrix4();
  const render=()=>{if(!disposed)renderer.render(scene,camera);};
  function clear(group) {for(const child of [...group.children]){child.traverse(node=>{node.geometry?.dispose();if(Array.isArray(node.material))node.material.forEach(m=>m.dispose());else node.material?.dispose();});group.remove(child);}}
  function sphere(position,radius,color) {const m=new T.Mesh(new T.SphereGeometry(radius,12,8),new T.MeshBasicMaterial({color,depthTest:false}));m.position.set(...position);m.renderOrder=10;marker.add(m);}
  function line(points,color) {const g=new T.BufferGeometry().setFromPoints(points.map(p=>new T.Vector3(...p)));content.add(new T.Line(g,new T.LineBasicMaterial({color})));}
  function axis(position,direction,color) {if(![...position,...direction].every(Number.isFinite))return;const end=position.map((p,k)=>p+direction[k]*displayScale*3);line([position,end],color);}
  function fit(focus=false) {
    if(bounds.isEmpty())return;
    const box=focus&&poses[selected]?new T.Box3().setFromCenterAndSize(new T.Vector3(...poses[selected].position),new T.Vector3(1,1,1).multiplyScalar(displayScale*16)):bounds;
    const center=box.getCenter(new T.Vector3()),radius=Math.max(.1,box.getSize(new T.Vector3()).length()/2);
    const vertical=T.MathUtils.degToRad(camera.fov/2),half=Math.min(vertical,Math.atan(Math.tan(vertical)*camera.aspect));
    camera.position.copy(center).add(new T.Vector3(.8,-1,.7).normalize().multiplyScalar(1.2*radius/Math.sin(half)));
    camera.near=Math.max(.0001,radius/10000);camera.far=Math.max(100,radius*100);camera.updateProjectionMatrix();orbit.target.copy(center);orbit.update();render();
  }
  function select(id) {selected=id;clear(marker);if(pair){sphere(pair.receiver,displayScale*.65,'#62dfec');sphere(pair.source,displayScale*.5,'#ffffff');}else if(poses[id]&&poses[id].position.every(Number.isFinite)){sphere(poses[id].position,displayScale*.75,'#62dfec');}render();}
  function setFamily(next) {
    clear(content);clear(marker);body=arms=null;pair=null;poses=next;bounds.makeEmpty();
    for(const p of poses)if(p.position.every(Number.isFinite))bounds.expandByPoint(new T.Vector3(...p.position));
    if(bounds.isEmpty())return;
    displayScale=Math.max(.035,Math.min(.15,bounds.getSize(new T.Vector3()).length()/150));
    body=new T.InstancedMesh(new T.BoxGeometry(.6,.4,.2),new T.MeshStandardMaterial(),poses.length);
    arms=new T.InstancedMesh(new T.BoxGeometry(1.5,.1,.08),new T.MeshStandardMaterial(),poses.length*2);
    body.frustumCulled=arms.frustumCulled=false;content.add(body,arms);
    const q=new T.Quaternion(),p=new T.Vector3(),s=new T.Vector3();
    for(const pose of poses){
      const drawable=[...pose.position,...pose.quaternion].every(Number.isFinite)&&pose.quaternion.some(x=>x!==0);
      p.set(...(drawable?pose.position:[0,0,0]));q.set(...(drawable?pose.quaternion:[0,0,0,1]));s.setScalar(drawable?displayScale:0);
      matrix.compose(p,q,s);body.setMatrixAt(pose.id,matrix);
      for(let k=0;k<2;k++){const armQ=q.clone().multiply(new T.Quaternion().setFromAxisAngle(new T.Vector3(0,0,1),k?-Math.PI/4:Math.PI/4));matrix.compose(p,armQ,s);arms.setMatrixAt(pose.id*2+k,matrix);}
    }
    body.instanceMatrix.needsUpdate=arms.instanceMatrix.needsUpdate=true;fit();select(0);
  }
  function setPair(next) {
    clear(content);clear(marker);body=arms=null;poses=[];pair=next;bounds.makeEmpty();
    if(![...pair.receiver,...pair.source,...pair.receiverAxis,...pair.sourceAxis,...pair.offset].every(Number.isFinite))return;
    bounds.expandByPoint(new T.Vector3(...pair.receiver));bounds.expandByPoint(new T.Vector3(...pair.source));
    displayScale=Math.max(.04,bounds.getSize(new T.Vector3()).length()/30);
    axis(pair.receiver,pair.receiverAxis,'#62dfec');axis(pair.source,pair.sourceAxis,'#ffffff');
    const offsetPoint=pair.receiver.map((v,k)=>v+pair.offset[k]);line([pair.receiver,offsetPoint],'#f49b41');bounds.expandByPoint(new T.Vector3(...offsetPoint));
    for(const [position,direction] of [[pair.receiver,pair.receiverAxis],[pair.source,pair.sourceAxis]])bounds.expandByPoint(new T.Vector3(...position.map((v,k)=>v+direction[k]*displayScale*3)));
    bounds.expandByScalar(displayScale*.65);
    select(0);fit();
  }
  function color(values) {
    if(!body)return {min:null,max:null,count:0};
    const finite=values.filter(Number.isFinite),min=finite.length?Math.min(...finite):null,max=finite.length?Math.max(...finite):null;
    const low=new T.Color('#4394cc'),high=new T.Color('#f49b41'),gray=new T.Color('#667784');
    for(let id=0;id<poses.length;id++){const v=values[id],c=Number.isFinite(v)?low.clone().lerp(high,max===min?0:(v-min)/(max-min)):gray;body.setColorAt(id,c);arms.setColorAt(2*id,c);arms.setColorAt(2*id+1,c);}
    body.instanceColor.needsUpdate=arms.instanceColor.needsUpdate=true;render();return {min,max,count:finite.length};
  }
  const down=e=>{pointer=[e.clientX,e.clientY];};
  const up=e=>{const start=pointer;pointer=null;if(!body||!start||Math.hypot(e.clientX-start[0],e.clientY-start[1])>5)return;const rect=renderer.domElement.getBoundingClientRect(),ray=new T.Raycaster();ray.setFromCamera(new T.Vector2(2*(e.clientX-rect.left)/rect.width-1,1-2*(e.clientY-rect.top)/rect.height),camera);const hit=ray.intersectObject(body)[0];if(hit?.instanceId!==undefined)onSelect(hit.instanceId);};
  renderer.domElement.addEventListener('pointerdown',down);renderer.domElement.addEventListener('pointerup',up);orbit.addEventListener('change',render);
  const observer=new ResizeObserver(()=>{if(disposed||!host.clientWidth||!host.clientHeight)return;renderer.setSize(host.clientWidth,host.clientHeight,false);camera.aspect=host.clientWidth/host.clientHeight;camera.updateProjectionMatrix();fit();render();});observer.observe(host);
  return {setFamily,setPair,select,color,reset:()=>fit(),focus:()=>fit(true),dispose(){disposed=true;observer.disconnect();orbit.removeEventListener('change',render);orbit.dispose();renderer.domElement.removeEventListener('pointerdown',down);renderer.domElement.removeEventListener('pointerup',up);clear(content);clear(marker);renderer.dispose();renderer.forceContextLoss();renderer.domElement.remove();}};
}
