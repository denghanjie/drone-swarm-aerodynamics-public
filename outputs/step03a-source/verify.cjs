'use strict';const fs=require('fs'),path=require('path'),{normalizedWake:w,hoverWake,idealPowerRatio:b}=require('./wake.cjs');const checks=[];
function check(name,ok){checks.push({name,passed:!!ok});if(!ok)throw Error(name);}
function near(a,b,tol=1e-12){return Math.abs(a-b)<tol;}
for(const s of [-1,0,2.499])check('No near-field or upstream prediction at '+s,w(s,0).speed===null);
check('Boundary explicitly accepted',w(2.5,0).speed!==null);
for(const s of [2.5,3,5,10]){const p=w(s,0);check('Half-width identity at '+s,near(w(s,p.halfWidth).speed,p.speed/2));check('Radial decay at '+s,p.speed>w(s,p.halfWidth).speed&&w(s,p.halfWidth).speed>w(s,2*p.halfWidth).speed);}
check('Centerline inverse-distance ratio',near(w(3,0).speed/w(5,0).speed,(5+5.817)/(3+5.817)));
check('Half-width grows linearly',near(w(5,0).halfWidth-w(3,0).halfWidth,2*.07668));
const base={downstream:.6,radial:.05,mass:.230,propRadius:.03685,motorDistance:.118};const a=hoverWake(base),scaled=hoverWake({...base,downstream:1.2,radial:.1,propRadius:.0737,motorDistance:.236,mass:.920});
check('Geometric scaling at fixed disk loading preserves speed',near(a.speedMS,scaled.speedMS));
check('Geometric scaling doubles width',near(scaled.halfWidthM,2*a.halfWidthM));
check('Fourfold mass doubles induced velocity',near(hoverWake({...base,mass:.920}).inducedMS,2*a.inducedMS));
check('Zero downwash needs no additional ideal power',b(0)===1);
check('Unit inflow ratio gives golden-ratio ideal power',near(b(1),(1+Math.sqrt(5))/2));
check('Ideal power rises with positive inflow',b(.5)<b(1)&&b(1)<b(2));
for(const bad of [()=>w(NaN,0),()=>w(3,-1),()=>b(-1),()=>hoverWake({...base,propRadius:0})]){let threw=false;try{bad();}catch{threw=true;}check('Reject invalid input '+checks.length,threw);}
const rows=[2.5,3,5,10].map(s=>{const p=w(s,0);return {s_over_l:s,centerline_over_UH:p.centerline,halfwidth_over_l:p.halfWidth,at_halfwidth_over_UH:w(s,p.halfWidth).speed};});
const out=path.resolve(__dirname,'..');fs.writeFileSync(path.join(out,'step-03a-verification.json'),JSON.stringify({kind:'equation-reproduction-checks-not-data-validation',checks,rows},null,2));const keys=Object.keys(rows[0]);fs.writeFileSync(path.join(out,'step-03a-wake-samples.csv'),keys.join(',')+'\n'+rows.map(r=>keys.map(k=>r[k]).join(',')).join('\n'));console.log(JSON.stringify({passed:checks.length,rows},null,2));
