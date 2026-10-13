'use strict';
const {F}=require('./adapter.cjs');
const C=Object.freeze({weight:F.P.m*F.P.g,rho:1.225,rotorRadius:.023,motorDistance:2*Math.SQRT2*F.P.a,spread:.07668,origin:-5.817,decay:10.11,minDownstream:2.5,nearFieldRadius:.15,maxTilt:20,axialFade:2,axialCutoff:2.5,radialFade:2,radialCutoff:3});
const rng=seed=>()=>((seed=(1664525*seed+1013904223)>>>0)/4294967296);
const quat=(roll=0,pitch=0,yaw=0)=>F.qmul(F.qmul([0,0,Math.sin(yaw*Math.PI/360),Math.cos(yaw*Math.PI/360)],[0,Math.sin(pitch*Math.PI/360),0,Math.cos(pitch*Math.PI/360)]),[Math.sin(roll*Math.PI/360),0,0,Math.cos(roll*Math.PI/360)]);
const state=(p=[0,0,1],q=quat(),thrust=[1,1,1,1])=>[...p,0,0,0,...q,0,0,0,...thrust.map(x=>x*C.weight/4)];
const half=d=>C.spread*(d-C.origin*C.motorDistance);
function lattice(n,spacing,seed=628731,tilt=0){const r=rng(seed),side=Math.ceil(Math.cbrt(n));return Array.from({length:n},(_,i)=>state([(i%side)*spacing+(r()-.5)*spacing*.025,(Math.floor(i/side)%side)*spacing+(r()-.5)*spacing*.025,1+Math.floor(i/side**2)*spacing+(r()-.5)*spacing*.025],quat(0,tilt*(2*r()-1),360*r()),[.5+r(),.5+r(),.5+r(),.5+r()]));}
function fixtures(full=false){const out=[];const add=(id,states,tags=[],extra={})=>out.push({id,states,tags,...extra});const fs=C.minDownstream*C.motorDistance;
add('isolated',[state()],['zero']);add('centered',[state(),state([0,0,2])],['pair']);add('offset_asymmetric',[state(undefined,quat(),[.1,.8,1.4,2.25]),state([.24,.06,2])],['pair','asymmetric-thrust']);
add('near_domain',[state(),state([.16,0,1.1])],['domain']);add('coincident_same_plane',[state(),state()],['zero','overlap-model-stress']);
for(const deg of [19.999999,20,20.000001]){const q=quat(0,deg,37),ax=F.rotate(q,[0,0,1]);add('tilt_'+deg,[state(),state([ax[0],ax[1],1+ax[2]],q)],['tilt']);}
if(!full)return out;
for(const d of [0,fs,2,2.5])for(const e of [-1e-12,0,1e-12])add(`axial_${d}_${e}`,[state(),state([0,0,1+d+e])],['axial-boundary']);
for(const d of [.5,1.3,2.499])for(const r of [2,3])for(const e of [-1e-12,0,1e-12])add(`radial_${d}_${r}_${e}`,[state(),state([F.rotors[0][0]+r*half(d)+e,F.rotors[0][1],1+d])],['radial-boundary']);
for(const e of [-1e-12,0,1e-12]){add(`near_radial_${e}`,[state(),state([F.rotors[0][0]+C.nearFieldRadius+e,F.rotors[0][1],1+fs/2])],['near-boundary']);add(`search_${e}`,[state(),state([Math.sqrt(9-1)+e,0,2])],['search-boundary']);}
for(const n of [16,50,100,200]){
 for(const spacing of [.35,1,4])add(`density_N${n}_s${spacing}`,lattice(n,spacing),['fixed-N','density'],{seed:628731,spacing});
 add(`fixed_volume_N${n}`,lattice(n,2/(Math.ceil(Math.cbrt(n))-1)),['fixed-volume'],{seed:628731,extent:2});
 add(`zero_field_N${n}`,Array.from({length:n},(_,i)=>state([i*4,0,1])),['zero','fixed-N']);
 const d=1.75,r=2.7*half(d);add(`many_weak_N${n}`,[state(),...Array.from({length:n-1},(_,i)=>{const a=i*2*Math.PI/(n-1);return state([r*Math.cos(a),r*Math.sin(a),1+d]);})],['many-weak','deliberately-overlapping-software-stress']);
 add(`many_strong_N${n}`,[state(),...Array.from({length:n-1},()=>state([0,0,2]))],['accumulation','deliberately-coincident-software-stress']);
}
for(const deg of [-19,0,19])add('tilted_N50_'+deg,lattice(50,.75,628732,deg),['tilt','accumulation']);
return out;}
function permutation(states,seed=887){const ids=states.map((_,i)=>i),r=rng(seed);for(let i=ids.length-1;i>0;i--){const j=Math.floor(r()*(i+1));[ids[i],ids[j]]=[ids[j],ids[i]];}return {states:ids.map(i=>states[i].slice()),ids};}
function translate(states,d=[1.499999999999,-3.000000000001,.125]){return states.map(s=>s.map((x,k)=>k<3?x+d[k]:x));}
function yawRotate(states,degrees=73){const q=quat(0,0,degrees);return states.map(s=>{const out=s.slice(),p=F.rotate(q,s.slice(0,3)),v=F.rotate(q,s.slice(3,6));out.splice(0,6,...p,...v);out.splice(6,4,...F.qmul(q,s.slice(6,10)));return out;});}
module.exports={C,F,rng,quat,state,half,lattice,fixtures,permutation,translate,yawRotate};
