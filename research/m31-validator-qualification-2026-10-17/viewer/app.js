import * as THREE from 'three';
import {OrbitControls} from '../../../outputs/step02b-source/vendor/OrbitControls.js';
// Display only. Scientific calculations never run in this page.
const BINDING_SHA='c24e9c7c124e01a7387cc2208f8ec18077f997bce73a5008ab15add27f90fc37';
const $=id=>document.getElementById(id);
const sha=async b=>Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',b)),v=>v.toString(16).padStart(2,'0')).join('');
async function checked(url,expected){const r=await fetch(url,{cache:'no-store'});if(!r.ok)throw Error('Evidence file unavailable');const b=await r.arrayBuffer();if(await sha(b)!==expected)throw Error('Evidence digest mismatch');return JSON.parse(new TextDecoder().decode(b));}
const dv=new DataView(new ArrayBuffer(8));
function number(word){if(!/^[0-9a-f]{16}$/.test(word))throw Error('Invalid recorded word');dv.setUint32(0,parseInt(word.slice(0,8),16),false);dv.setUint32(4,parseInt(word.slice(8),16),false);const x=dv.getFloat64(0,false);if(!Number.isFinite(x))throw Error('Nonfinite recorded pose');return x;}
let binding, generations={},frames=[],run='run-a',frame=0,playing=false,last=0;
const scene=new THREE.Scene();scene.background=new THREE.Color('#0a141d');
const camera=new THREE.PerspectiveCamera(43,1,.01,1000);camera.up.set(0,0,1);
const renderer=new THREE.WebGLRenderer({antialias:true});renderer.setPixelRatio(Math.min(devicePixelRatio,2));$('scene').appendChild(renderer.domElement);
const controls=new OrbitControls(camera,renderer.domElement);controls.enableDamping=true;controls.dampingFactor=.09;
scene.add(new THREE.HemisphereLight(0xd9f8ff,0x223445,2));const light=new THREE.DirectionalLight(0xffffff,2);light.position.set(3,-4,10);scene.add(light);
const group=new THREE.Group();scene.add(group);const body=new THREE.InstancedMesh(new THREE.BoxGeometry(.048,.035,.018),new THREE.MeshStandardMaterial({color:'#67dfc5',roughness:.5}),64);group.add(body);
const armGeom=new THREE.BoxGeometry(.09,.007,.005);armGeom.rotateZ(Math.PI/4);const arms1=new THREE.InstancedMesh(armGeom,new THREE.MeshStandardMaterial({color:'#d3e4ea'}),64);group.add(arms1);
const armGeom2=armGeom.clone();armGeom2.rotateZ(Math.PI/2);const arms2=new THREE.InstancedMesh(armGeom2,arms1.material,64);group.add(arms2);
const rotorMeshes=[];for(const [x,y] of [[.028,.028],[-.028,.028],[-.028,-.028],[.028,-.028]]){const g=new THREE.CylinderGeometry(.023,.023,.002,12);g.rotateX(Math.PI/2);g.translate(x,y,0);const m=new THREE.InstancedMesh(g,new THREE.MeshStandardMaterial({color:'#87adbd',transparent:true,opacity:.65}),64);group.add(m);rotorMeshes.push(m);}
const axisPositions=new Float32Array(64*6),axisGeometry=new THREE.BufferGeometry();axisGeometry.setAttribute('position',new THREE.BufferAttribute(axisPositions,3));const axes=new THREE.LineSegments(axisGeometry,new THREE.LineBasicMaterial({color:'#efb26a',transparent:true,opacity:.8}));group.add(axes);
const grid=new THREE.GridHelper(14,28,0x46616e,0x1b3342);grid.rotation.x=Math.PI/2;scene.add(grid);
const object=new THREE.Object3D();object.scale.setScalar(3);const tip=new THREE.Vector3();let center=new THREE.Vector3(),extent=5;
function resize(){const r=$('scene').getBoundingClientRect();renderer.setSize(r.width,r.height,false);camera.aspect=r.width/r.height;camera.updateProjectionMatrix();}new ResizeObserver(resize).observe($('scene'));
function reset(){camera.position.copy(center).add(new THREE.Vector3(extent*.95,-extent*1.25,extent*.8));controls.target.copy(center);controls.update();}
function draw(){
 const f=frames[frame];if(!f)return;if(f.words.length!==448)throw Error('Unexpected pose dimensions');
 for(let i=0;i<64;i++){const w=f.words.slice(7*i,7*i+7).map(number);object.position.set(w[0],w[1],w[2]);object.quaternion.set(w[3],w[4],w[5],w[6]);object.updateMatrix();for(const m of [body,arms1,arms2,...rotorMeshes])m.setMatrixAt(i,object.matrix);tip.set(0,0,.23).applyQuaternion(object.quaternion).add(object.position);axisPositions.set([w[0],w[1],w[2],tip.x,tip.y,tip.z],6*i);}
 for(const m of [body,arms1,arms2,...rotorMeshes]){m.instanceMatrix.needsUpdate=true;m.frustumCulled=false;}axisGeometry.attributes.position.needsUpdate=true;axes.frustumCulled=false;
 $('frame').value=String(frame);$('time').textContent=Number(f.t).toFixed(1)+' s';
 const row=binding.rows.find(r=>r.runId===run&&r.t===f.t);
 $('frame-status').textContent=row?'Tested snapshot · '+row.outcome+' · '+row.validation:'Recorded pose only · no aerodynamic load query at this time.';
 document.querySelectorAll('.checkpoint').forEach(el=>el.classList.toggle('current',Number(el.dataset.t)===f.t));
 window.__viewState={run,frame,t:f.t,wordCount:f.words.length,bodyCount:body.count,positions:Array.from({length:64},(_,i)=>{const m=new THREE.Matrix4();body.getMatrixAt(i,m);return m.elements.slice(12,15);}),validEvidence:true,camera:camera.position.toArray()};
}
function choose(id){run=id;frames=generations[id].frames;if(!frames.length)throw Error('No saved pose frames');frame=0;$('frame').max=String(frames.length-1);$('outcomes').replaceChildren();
 for(const r of binding.rows.filter(r=>r.runId===id)){const el=document.createElement('div');el.className='checkpoint'+(r.outcome.startsWith('certified')?'':' refused');el.dataset.t=String(r.t);const b=document.createElement('b');b.textContent=r.t+' s · '+r.outcome;el.append(b,document.createTextNode(r.validation));$('outcomes').appendChild(el);}
 const bounds=new THREE.Box3();for(const f of frames)for(let i=0;i<64;i++)bounds.expandByPoint(new THREE.Vector3(...f.words.slice(7*i,7*i+3).map(number)));center=bounds.getCenter(new THREE.Vector3());extent=Math.max(3,bounds.getSize(new THREE.Vector3()).length());grid.position.set(center.x,center.y,bounds.min.z-.3);reset();draw();
}
function fail(e){playing=false;$('notice').classList.add('error');$('notice').textContent='Evidence unavailable or inconsistent. Research claims and replay are hidden.';$('scene').classList.add('hidden');$('outcomes').replaceChildren();$('all-results').replaceChildren();$('qualification-cards').replaceChildren();$('verdict').textContent='';$('diagnosis').textContent='';$('frame-status').textContent='Evidence validation failed.';for(const id of ['run','play','frame','reset'])$(id).disabled=true;window.__viewState={validEvidence:false,error:String(e.message)};}
try{
 binding=await checked('binding.json',BINDING_SHA);if(binding.schema!=='m31-validator-view-v1'||binding.rows.length!==6)throw Error('Invalid view binding');
 const evidence={};for(const pin of binding.pins)evidence[pin.path]=await checked('../../../'+pin.path,pin.sha256);
 for(const [id,path]of Object.entries(binding.generationPaths))generations[id]=evidence[path];
 const checkedResult=evidence[binding.checkPath],index=evidence[binding.indexPath];
 if(checkedResult.passed!==false||checkedResult.advancement!==false||checkedResult.denominator!==6||checkedResult.counts.certified!==6||checkedResult.counts.independentlyVerified!==6||checkedResult.fixedControlsPassed!==true||checkedResult.nontriviality.informative!==true)throw Error('Summary mismatch');
 if(checkedResult.corruptionControls.length!==20||checkedResult.corruptionControls.filter(x=>x.rejected).length!==20||checkedResult.corruptionControls.filter(x=>x.intendedCoreFailure).length!==19)throw Error('Control summary mismatch');
 if(index.scheduled.length!==6||index.sourceCommit!==checkedResult.sourceCommit)throw Error('Index binding mismatch');
 for(const row of binding.rows){const schedule=index.scheduled.find(s=>s.id===row.id),outcome=checkedResult.outcomes.find(o=>o.id===row.id);if(!schedule||!outcome||schedule.t!==row.t||schedule.runId!==row.runId||schedule.status!=='evaluated'||schedule.record.path!==row.recordPath||outcome.verified!==true||outcome.certified!==true||outcome.status!==row.modelStatus||outcome.branch!==row.modelBranch||row.captured!=='yes'||row.outcome!=='certified'||row.validation!=='Passed individually; overall gate failed')throw Error('Scheduled result mismatch');}
 for(const [id,path]of Object.entries(binding.generationPaths)){const g=generations[id],entry=index.generations.find(g=>g.id===id);if(!entry||entry.path!==path||g.id!==id||g.frames.length!==51||g.sourceCommit!==index.sourceCommit)throw Error('Generation binding mismatch');}

 for(const row of binding.rows){if(row.recordPath){const rec=evidence[row.recordPath];if(rec.id!==row.id||!rec.method||rec.method.result.status!==row.modelStatus||rec.method.result.branch!==row.modelBranch)throw Error('Outcome record mismatch');}}
 const qualification=evidence[binding.qualificationPath],supervision=evidence[binding.supervisionPath];
 if(qualification.schema!=='m31-validator-qualification-v1'||qualification.historicalOriginalPassed!==false||qualification.historicalOriginalAdvancement!==false||qualification.transferAuthorized!==false||qualification.freshReplication!==false||qualification.priorSourceCommit!==index.sourceCommit||qualification.sourceCommit!==supervision.sourceCommit||qualification.passed!==binding.qualificationPassed||supervision.success!==binding.supervisionPassed)throw Error('Qualification identity mismatch');
 const targeted=qualification.corruptionControls.filter(c=>c.executed&&c.rejected&&c.intendedCoreFailure).length;
 if(targeted!==binding.targetedCount||qualification.corruptionControls.length!==binding.controlCount)throw Error('Qualification control summary mismatch');
 window.__qualificationState={passed:qualification.passed,supervisionPassed:supervision.success,targeted,total:qualification.corruptionControls.length,historicalPassed:checkedResult.passed};
 const oldCard=document.createElement('p');oldCard.textContent='Original moving-state experiment: FAILED · 19 / 20 intended negative checks.';
 const newCard=document.createElement('p');newCard.textContent='New saved-corpus qualification: '+(qualification.passed&&supervision.success?'PASSED':'FAILED')+' · '+targeted+' / '+qualification.corruptionControls.length+' intended negative checks.';
 $('qualification-cards').replaceChildren(oldCard,newCard);
 $('notice').textContent=binding.headline;$('diagnosis').textContent=binding.diagnosis;$('verdict').textContent=binding.verdict;
 for(const row of binding.rows){const tr=document.createElement('tr');for(const text of [row.runId,row.t+' s',row.captured,row.outcome,row.validation]){const td=document.createElement('td');td.textContent=text;tr.appendChild(td);}$('all-results').appendChild(tr);}
 choose(run);$('run').addEventListener('change',e=>{playing=false;$('play').textContent='Play';try{choose(e.target.value);}catch(e){fail(e);}});$('frame').addEventListener('input',e=>{playing=false;$('play').textContent='Play';frame=Number(e.target.value);try{draw();}catch(e){fail(e);}});$('play').addEventListener('click',()=>{playing=!playing;last=performance.now();$('play').textContent=playing?'Pause':'Play';});$('reset').addEventListener('click',reset);
}catch(e){fail(e);}
function animate(t){requestAnimationFrame(animate);if(window.__viewState?.validEvidence)window.__viewState.camera=camera.position.toArray();if(playing&&frames.length&&t-last>=200){frame=(frame+1)%frames.length;last=t;try{draw();}catch(e){fail(e);}}controls.update();renderer.render(scene,camera);}resize();requestAnimationFrame(animate);
