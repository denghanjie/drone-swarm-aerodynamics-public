import * as THREE from 'three';
import {OrbitControls} from '../../../outputs/step02b-source/vendor/OrbitControls.js';
export function createScene(host,rows){
  const renderer=new THREE.WebGLRenderer({antialias:true});renderer.setPixelRatio(Math.min(devicePixelRatio,2));renderer.setClearColor(0x102331);renderer.outputColorSpace=THREE.SRGBColorSpace;host.append(renderer.domElement);
  const scene=new THREE.Scene(),camera=new THREE.PerspectiveCamera(38,1,.01,40),controls=new OrbitControls(camera,renderer.domElement);controls.enableDamping=false;controls.minDistance=2;controls.maxDistance=15;
  const group=new THREE.Group();scene.add(group);const labels=[];
  function line(points,color,opacity=1){const item=new THREE.Line(new THREE.BufferGeometry().setFromPoints(points.map(p=>new THREE.Vector3(...p))),new THREE.LineBasicMaterial({color,transparent:opacity<1,opacity}));group.add(item);return item;}
  function label(text,x,y,z){const c=document.createElement('canvas');c.width=256;c.height=64;const ctx=c.getContext('2d');ctx.fillStyle='#d5e5e9';ctx.font='23px system-ui';ctx.textAlign='center';ctx.fillText(text,128,42);const texture=new THREE.CanvasTexture(c);const sp=new THREE.Sprite(new THREE.SpriteMaterial({map:texture,depthTest:false}));sp.position.set(x,y,z);sp.scale.set(1.65,.4125,1);group.add(sp);labels.push(texture);}
  function clear(){for(const o of [...group.children]){o.geometry?.dispose();o.material?.dispose();group.remove(o);}labels.splice(0).forEach(t=>t.dispose());}
  const render=()=>renderer.render(scene,camera);
  function reset(){camera.position.set(4.4,3.4,5);controls.target.set(1.35,.65,0);controls.update();render();}
  function update(index,overlay,dimensional){clear();const selected=rows[index];const colors=[0xf39a65,0x63d5ea];
    for(let j=0;j<2;j++){const z=overlay?0:(j===0?-.4:.4),key=j===0?'g1':'g2';
      for(let i=0;i<=6;i++)line([[0,i*.25,z],[3,i*.25,z]],0x6b8b97,.22);
      line([[0,1.5,z],[0,0,z],[3,0,z]],0xaac0ca,.6);
      line(rows.map(r=>[r.r_over_l,r[key],z]),colors[j]);
      const p=new THREE.Mesh(new THREE.SphereGeometry(.035,12,8),new THREE.MeshBasicMaterial({color:colors[j]}));p.position.set(selected.r_over_l,selected[key],z);group.add(p);
      line([[selected.r_over_l,0,z],[selected.r_over_l,selected[key],z]],colors[j],.5);
      label(j===0?(dimensional?'Transferred Offboard 1':'Offboard 1'):'Offboard 2',2.3,1.45+(overlay?.25*j:0),z);
    }
    for(let i=0;i<=3;i++)label((i*(dimensional?.266:1)).toFixed(dimensional?3:0),i,-.12,.5);
    label(dimensional?'radius / m':'radius r/l',1.5,-.38,.5);label(dimensional?'speed / m/s':'speed / UH',-.12,1.75,0);
    label(dimensional?'14.49':'1.5',-.36,1.5,0);label('0',-.2,0,0);
    host.setAttribute('aria-label',`Static saved profiles, ${overlay?'overlaid':'separated in display depth'}, ${dimensional?'transferred target units':'normalized units'}, selected radius r/l ${selected.r_over_l}. Display depth is not a physical coordinate.`);render();}
  controls.addEventListener('change',render);const observer=new ResizeObserver(()=>{renderer.setSize(host.clientWidth,host.clientHeight,false);camera.aspect=host.clientWidth/host.clientHeight;camera.updateProjectionMatrix();render();});observer.observe(host);reset();
  renderer.domElement.addEventListener('webglcontextlost',()=>{host.setAttribute('aria-label','WebGL context lost; use the exact saved-value table.');});
  return {update,reset};
}
