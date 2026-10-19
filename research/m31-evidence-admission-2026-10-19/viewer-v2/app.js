import * as THREE from 'three';
import {OrbitControls} from '../../../outputs/step02b-source/vendor/OrbitControls.js';
const $=id=>document.getElementById(id);
async function pinned(url,bytes,sha,label){const r=await fetch(url,{cache:'no-store'});if(!r.ok)throw Error(label+' unavailable');const raw=await r.arrayBuffer(),hash=Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',raw)),x=>x.toString(16).padStart(2,'0')).join('');if(raw.byteLength!==bytes||hash!==sha)throw Error(label+' identity changed');return JSON.parse(new TextDecoder().decode(raw));}
try{
const pins=await(await fetch('pins.json',{cache:'no-store'})).json();
const ledger=await pinned('../admission.json',pins.ledgerBytes,pins.ledgerSha256,'Admission record');
const d=await pinned(pins.path,pins.bytes,pins.sha256,'Saved evidence');
const audit=await pinned(pins.auditPath,pins.auditBytes,pins.auditSha256,'Saved audit');
if(ledger.decision!=='no-new-admission'||ledger.entries.length!==4||ledger.newScientificRuns!==0||d.status!=='completed-face-transport'||d.sourceCommit!==pins.sourceCommit||!audit.passed||!audit.complete||audit.resultPin.sha256!==pins.sha256||audit.resultPin.bytes!==pins.bytes||audit.sourceManifestSha256!==pins.sourceManifestSha256)throw Error('Evidence audit or admission incomplete');
const old=d.inheritedAnnular,rows=old.originalCases.map(c=>c.original);if(rows.length!==3240)throw Error('Saved point count changed');
$('headline').textContent='No new test-ready dataset was admitted. The calibration question remains open.';
for(const e of ledger.entries){const o=document.createElement('option');o.value=e.id;o.textContent=e.title;$('candidate').append(o);}
function choose(){const e=ledger.entries.find(e=>e.id===$('candidate').value);for(const k of ['status','reason','missing'])$(k).textContent=e[k];$('source').href=e.url;document.body.dataset.candidate=e.id;}choose();$('candidate').onchange=choose;
const scene=new THREE.Scene();scene.background=new THREE.Color('#10222e');const camera=new THREE.PerspectiveCamera(43,1,.005,20);camera.up.set(0,0,1);const renderer=new THREE.WebGLRenderer({antialias:true,preserveDrawingBuffer:true});renderer.setPixelRatio(Math.min(devicePixelRatio,2));$('scene').append(renderer.domElement);const controls=new OrbitControls(camera,renderer.domElement);controls.enableDamping=true;
const l=.0325,selected=new Set(old.selection.regions.flatMap(r=>r.selectedIndices)),positions=new Float32Array(rows.length*3),colors=new Float32Array(rows.length*3);rows.forEach((o,i)=>positions.set([o.X*l,l,-o.Z*l],i*3));const geom=new THREE.BufferGeometry();geom.setAttribute('position',new THREE.BufferAttribute(positions,3));geom.setAttribute('color',new THREE.BufferAttribute(colors,3));scene.add(new THREE.Points(geom,new THREE.PointsMaterial({size:.005,vertexColors:true})));
const core=new THREE.Mesh(new THREE.CylinderGeometry(l,l,22*l,40,1,true),new THREE.MeshBasicMaterial({color:0xf0c26e,opacity:.15,transparent:true,side:THREE.DoubleSide,depthWrite:false}));core.rotation.x=Math.PI/2;core.position.z=-19*l;scene.add(core);
scene.add(new THREE.Line(new THREE.BufferGeometry().setFromPoints([new THREE.Vector3(0,0,0),new THREE.Vector3(0,0,-30*l)]),new THREE.LineBasicMaterial({color:0xf0c26e})));
// Nominal schematic body at the inherited origin, not measured airframe geometry.
scene.add(new THREE.Mesh(new THREE.BoxGeometry(.04,.035,.012),new THREE.MeshBasicMaterial({color:0x8fd8c9})));
function update(){const on=$('coverage').checked;rows.forEach((o,i)=>{const c=new THREE.Color(on&&selected.has(o.index)?0x8fd8c9:0x526878);colors.set([c.r,c.g,c.b],i*3);});geom.attributes.color.needsUpdate=true;renderer.domElement.dataset.coverage=String(on);$('geometry').textContent='3,240 saved points on one offset plane; 1,220 previously selected points. We did not measure a complete 3D flow volume.';}
function reset(){controls.target.set(0,l,-.57);camera.position.set(.48,-.86,-.27);controls.update();}new ResizeObserver(()=>{const b=$('scene').getBoundingClientRect();renderer.setSize(b.width,b.height,false);camera.aspect=b.width/b.height;camera.updateProjectionMatrix();}).observe($('scene'));
$('coverage').onchange=update;$('reset').onclick=reset;Object.assign(renderer.domElement.dataset,{points:rows.length,selected:selected.size,nominalScale:l,planeY:l,coreRadius:l});reset();update();function frame(){requestAnimationFrame(frame);controls.update();renderer.render(scene,camera);renderer.domElement.dataset.rendered='true';}frame();
}catch(e){$('headline').textContent='Evidence could not be verified.';$('error').textContent=e.message;}
