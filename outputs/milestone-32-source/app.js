import * as T from '../step02b-source/vendor/three.module.js';
import {OrbitControls} from '../step02b-source/vendor/OrbitControls.js';
const $=id=>document.getElementById(id),host=$('scene'),scene=new T.Scene();scene.background=new T.Color('#081523');
const camera=new T.PerspectiveCamera(42,1,.02,160);camera.up.set(0,0,1);
const renderer=new T.WebGLRenderer({antialias:true,preserveDrawingBuffer:true});renderer.setPixelRatio(Math.min(devicePixelRatio,2));host.append(renderer.domElement);
const orbit=new OrbitControls(camera,renderer.domElement);orbit.enableDamping=true;
scene.add(new T.HemisphereLight(0xc5f5ff,0x224457,3));const sun=new T.DirectionalLight(0xffffff,3);sun.position.set(0,-8,12);scene.add(sun);
const content=new T.Group(),obstacles=new T.Group(),wakeGroup=new T.Group(),linkGroup=new T.Group(),cueGroup=new T.Group();scene.add(content,obstacles,wakeGroup,linkGroup,cueGroup);
const grid=new T.GridHelper(60,60,0x325669,0x162d40);grid.rotation.x=Math.PI/2;grid.position.z=.005;scene.add(grid);
let data,mode='flock',playing=false,frameIndex=4,center=new T.Vector3(),previous=0,lastSnapshot=0,axes=[];
const heat=u=>new T.Color().setHSL(.53-Math.min(1,u/4)*.53,.8,.67),avg=a=>a.reduce((x,y)=>x+y,0)/a.length;
function clear(group){for(const o of [...group.children]){o.traverse(c=>{c.geometry?.dispose();if(c.material){c.material.map?.dispose();c.material.dispose();}});group.remove(o);}}
function drone(p,winds,label){const g=new T.Group(),q=new T.Quaternion(...p.slice(3));g.position.set(...p.slice(0,3));g.quaternion.copy(q);const col=winds?heat(Math.max(...winds)):new T.Color('#9da6b4');
 const body=new T.Mesh(new T.BoxGeometry(.045,.035,.02),new T.MeshStandardMaterial({color:col,emissive:col,emissiveIntensity:.3}));g.add(body);
 for(const angle of [-Math.PI/4,Math.PI/4]){const arm=new T.Mesh(new T.BoxGeometry(.095,.006,.006),new T.MeshStandardMaterial({color:0xc5e8ef}));arm.rotation.z=angle;g.add(arm);}
 for(let j=0;j<4;j++){const r=new T.Mesh(new T.TorusGeometry(.023,.0025,6,20),new T.MeshBasicMaterial({color:winds?heat(winds[j]):0x9da6b4}));r.position.set(data.rotors[j][0],data.rotors[j][1],.005);g.add(r);}
 g.scale.setScalar(2);content.add(g);if(label){const el=document.createElement('canvas');el.width=512;el.height=80;const ctx=el.getContext('2d');ctx.font='32px system-ui';ctx.fillStyle='#d9f4ff';ctx.fillText(label,8,48);const texture=new T.CanvasTexture(el),sprite=new T.Sprite(new T.SpriteMaterial({map:texture,transparent:true,depthTest:false}));sprite.scale.set(1.45,.23,1);sprite.position.set(p[0]+.68,p[1],p[2]+.15);content.add(sprite);}
}
function wake(p){const q=new T.Quaternion(...p.slice(3)),origin=new T.Vector3(...p.slice(0,3)),pts=[],rings=[];
 for(let a=0;a<8;a++){const angle=a*Math.PI/4;for(let j=0;j<data.plume.length-1;j++){for(const z of [data.plume[j],data.plume[j+1]])pts.push(...new T.Vector3(z.halfWidth*Math.cos(angle),z.halfWidth*Math.sin(angle),-z.down).applyQuaternion(q).add(origin).toArray());}}
 for(let j=0;j<data.plume.length;j+=6){const z=data.plume[j];for(let a=0;a<32;a++)for(const angle of [a/32*Math.PI*2,(a+1)/32*Math.PI*2])rings.push(...new T.Vector3(z.halfWidth*Math.cos(angle),z.halfWidth*Math.sin(angle),-z.down).applyQuaternion(q).add(origin).toArray());}
 const geo=new T.BufferGeometry();geo.setAttribute('position',new T.Float32BufferAttribute([...pts,...rings],3));wakeGroup.add(new T.LineSegments(geo,new T.LineBasicMaterial({color:0x55dfdb,transparent:true,opacity:mode==='pair'?.34:.12,depthWrite:false})));
 axes.push({origin,q});
}
function factory(){clear(obstacles);if(mode==='pair')return;for(const b of data.geometry.boxes){if(b.kind==='shell'||b.min[0]>6||b.max[0]<-13)continue;const size=b.max.map((x,k)=>x-b.min[k]),m=new T.Mesh(new T.BoxGeometry(...size),new T.MeshStandardMaterial({color:b.kind==='partition'?0x628295:0x567487,transparent:true,opacity:.23,depthWrite:false}));m.position.set(...b.min.map((v,k)=>(v+b.max[k])/2));obstacles.add(m);}}
function reset(){const offset=mode==='pair'?new T.Vector3(3,-5,1.8):new T.Vector3(5,-7,4.5);offset.multiplyScalar(Math.max(1,.9/camera.aspect));orbit.target.copy(center);camera.position.copy(center).add(offset);orbit.update();}
new ResizeObserver(()=>{renderer.setSize(host.clientWidth,host.clientHeight,false);camera.aspect=host.clientWidth/host.clientHeight;camera.updateProjectionMatrix();reset();}).observe(host);
function update(){if(!data)return;for(const g of [content,wakeGroup,linkGroup,cueGroup])clear(g);axes=[];center.set(0,0,0);
 if(mode==='pair'){
  const down=+$('down').value/10,x=+$('offset').value/50,d=data.demo.find(d=>d.down===down&&d.x===x),a=[0,0,3,0,0,0,1],b=[x,0,3-down,0,0,0,1];drone(a,d.sourceWinds,'Upper drone');drone(b,d.winds,'Lower drone');wake(a);center.set(0,0,1.8);
  $('down-value').textContent=down.toFixed(1)+' m';$('offset-value').textContent=x.toFixed(2)+' m';$('label1').textContent='Mean lower-drone inflow';$('label2').textContent='Estimated hover lift loss';$('label3').textContent='Four rotor inflows';
  $('stat1').textContent=d.domain?'Outside domain':avg(d.winds).toFixed(2)+' m/s';$('stat2').textContent=d.domain?'—':(100*(1-d.liftFraction)).toFixed(1)+'%';$('stat3').textContent=d.domain?'—':Math.min(...d.winds).toFixed(2)+'–'+Math.max(...d.winds).toFixed(2)+' m/s';
  $('badge').textContent='Static two-drone model · not a free-flight simulation';$('status').textContent=d.domain?'Model unavailable here: '+d.domain+'. The wake starts 0.20 m below the source.':'Lower-drone color shows predicted inflow. Lift loss is an ideal-power assumption, not a calibrated motor response.';
  if(!d.domain&&avg(d.winds)>.03)addLink(a,b);
 }else{
  const c=data.cases.find(c=>c.mode===$('trial').value);frameIndex=Math.min(frameIndex,c.frames.length-1);const f=c.frames[frameIndex];
  for(let i=0;i<f.poses.length;i++){drone(f.poses[i],f.winds?.[i]);if(c.mode!=='off')wake(f.poses[i]);center.add(new T.Vector3(...f.poses[i].slice(0,3)));}center.divideScalar(f.poses.length);
  for(const edge of f.links)addLink(f.poses[edge.source],f.poses[edge.receiver]);
  $('frame').max=c.frames.length-1;$('frame').value=frameIndex;$('clock').textContent=f.t.toFixed(3)+' / '+c.metrics.end.toFixed(3)+' s';$('badge').textContent='Milestone 28 · 50 local Boids · '+f.t.toFixed(3)+' s';
  $('label1').textContent='Peak receiver inflow';$('label2').textContent='Affected drones · >0.01 m/s';$('label3').textContent='Recorded course completion';$('stat1').textContent=f.domain?'Outside domain':f.maximumInflow.toFixed(2)+' m/s';$('stat2').textContent=f.winds?f.winds.filter(w=>Math.max(...w)>.01).length+' / 50':'—';
  // Completion comes from exact historical samples, never inferred from graphic positions.
  $('stat3').textContent=c.crossings.filter(t=>t!==null&&t<=f.t).length+' / 50';
  $('status').textContent=f.domain?'Snapshot field unavailable: '+f.domain:frameIndex===c.frames.length-1?(c.metrics.stopReason?'Recorded stop at '+c.metrics.end.toFixed(3)+' s: '+c.metrics.stopReason+'.':'Recorded horizon: all 50 completed with airflow off.'):'Exact saved pose; recomputed snapshot field. '+(c.mode==='off'?'Airflow forces were disabled.':'Amber lines connect up to two strongest contributing sources per receiver.');
  if(frameIndex===c.frames.length-1&&c.metrics.failure){for(const i of c.metrics.failure.pair||[c.metrics.failure.drone])if(i!==undefined){const m=new T.Mesh(new T.SphereGeometry(.18,16,10),new T.MeshBasicMaterial({color:0xff5365,wireframe:true,depthTest:false}));m.position.set(...f.poses[i].slice(0,3));content.add(m);}}
 }
 const points=new T.BufferGeometry();points.setAttribute('position',new T.Float32BufferAttribute(new Float32Array(axes.length*60*3),3));cueGroup.add(new T.Points(points,new T.PointsMaterial({color:0x7cefe2,size:mode==='pair'?.013:.023,transparent:true,opacity:.6,depthWrite:false})));
 wakeGroup.visible=$('wakes').checked;linkGroup.visible=$('links').checked;cueGroup.visible=$('motion').checked;obstacles.visible=$('walls').checked;host.dataset.mode=mode;host.dataset.sources=axes.length;host.dataset.links=linkGroup.children.length;
}
function addLink(a,b){const delta=new T.Vector3(...b.slice(0,3)).sub(new T.Vector3(...a.slice(0,3))),length=delta.length();const arrow=new T.ArrowHelper(delta.normalize(),new T.Vector3(...a.slice(0,3)),length,0xffc370,.08,.04);linkGroup.add(arrow);}
function choose(m){mode=m;playing=false;$('play').textContent='Play snapshots';for(const name of ['flock','pair']){$(name).setAttribute('aria-pressed',name===m);$(name+'-controls').hidden=name!==m;}$('timeline').hidden=m!=='flock';factory();update();reset();}
$('pair').onclick=()=>choose('pair');$('flock').onclick=()=>choose('flock');$('camera').onclick=reset;
$('down').oninput=$('offset').oninput=()=>update();$('center').onclick=()=>{$('offset').value=0;update();};$('aside').onclick=()=>{$('offset').value=30;update();};
$('trial').onchange=()=>{playing=false;$('play').textContent='Play snapshots';update();reset();};$('frame').oninput=()=>{playing=false;$('play').textContent='Play snapshots';frameIndex=+$('frame').value;update();};$('outcome').onclick=()=>{playing=false;$('play').textContent='Play snapshots';frameIndex=data.cases.find(c=>c.mode===$('trial').value).frames.length-1;update();reset();};
$('play').onclick=()=>{if(frameIndex===+$('frame').max)frameIndex=0;playing=!playing;lastSnapshot=performance.now();$('play').textContent=playing?'Pause':'Play snapshots';update();};
for(const id of ['wakes','links','motion','walls'])$(id).onchange=()=>update();
function animate(now){if(playing&&now-lastSnapshot>750){lastSnapshot=now;frameIndex++;update();if(frameIndex>=+$('frame').max){playing=false;$('play').textContent='Play snapshots';}}
 const attr=cueGroup.children[0]?.geometry.attributes.position;if(attr&&cueGroup.visible){let k=0;for(const axis of axes)for(let j=0;j<60;j++){const u=((j/60+now/6500)%1),down=.2+u*2.3,z=data.plume[Math.min(46,Math.floor(u*46))],angle=j*2.399963,r=z.halfWidth*(.2+.8*((j*17%61)/61)),p=new T.Vector3(r*Math.cos(angle),r*Math.sin(angle),-down).applyQuaternion(axis.q).add(axis.origin);attr.setXYZ(k++,p.x,p.y,p.z);}attr.needsUpdate=true;}
 orbit.update();renderer.render(scene,camera);previous=now;requestAnimationFrame(animate);}
requestAnimationFrame(animate);
try{const response=await fetch('./milestone-32-source/airflow.json');if(!response.ok)throw Error('Airflow data HTTP '+response.status);data=await response.json();choose('flock');$('loading').hidden=true;document.querySelector('main').setAttribute('aria-busy','false');}catch(e){$('loading').textContent='Could not load model: '+e.message;}
fetch('./milestone-32-comparisons.json').then(r=>{if(!r.ok)throw Error('pending');return r.json();}).then(rows=>{$('numerics').innerHTML='<table><tr><th>Comparison · 20–30 s</th><th>Max path difference</th></tr>'+rows.map((r,i)=>'<tr><td>'+['Feedback: 2.5 vs 1.25 ms','Feedback: 1.25 vs 0.625 ms','Same commands: 2.5 vs 1.25 ms','Same commands: 1.25 vs 0.625 ms'][i]+'</td><td>'+r.maximum.toExponential(2)+' m</td></tr>').join('')+'</table><p class="note">Post-hoc restart diagnosis. These results do not replace the three failed full-trajectory checks.</p>';}).catch(()=>{});

fetch('./milestone-32-checkpoint-comparisons.json').then(r=>{if(!r.ok)throw Error('pending');return r.json();}).then(d=>{$('diagnosis').textContent='Changing only the inherited starting state reproduces '+(d.sameStepDifferentStartingStates.maximum*100).toFixed(2)+' cm of divergence at the same step size. Earlier state differences matter in this window; the specific controller mechanism remains unresolved.';}).catch(()=>{});
