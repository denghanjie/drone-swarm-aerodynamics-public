'use strict';
// Explicitly authorized data-independent constant materialization only.
// Does not import reference.cjs, decode states, prepare geometry, calculate wake
// terms, solve roots, open a browser, compile WGSL or dispatch a GPU.
const fs=require('fs'),path=require('path'),crypto=require('crypto');
const output=process.argv[2];if(!output)throw Error('Output directory required');
const mass=.027,gravity=9.81,armCoordinate=.028,rho=1.225,rotorRadius=.023;
const area=Math.PI*rotorRadius*rotorRadius;
const sourceInduced=Math.sqrt(mass*gravity/(8*rho*area));
const f0=.027*9.81/4;
const C={D:2*Math.sqrt(2)*armCoordinate,decay:10.11,spread:.07668,origin:-5.817,
 minDownstream:2.5,neighborRadius:3,nearFieldRadius:.15,downstreamFade:2,
 downstreamCutoff:2.5,radialFade:2,radialCutoff:3,tiltCosine:Math.cos(20*Math.PI/180),
 sourceInduced,sqrt2Minus1:Math.sqrt(2)-1,f0,area,
 epsilonWake:3*sourceInduced*1e-7/f0,referenceSumAllowance:1e-12};
const names=['D','decay','spread','origin','minDownstream','neighborRadius','nearFieldRadius','downstreamFade','downstreamCutoff','radialFade','radialCutoff','tiltCosine','sourceInduced','sqrt2Minus1'];
const original=Buffer.alloc(128),packed=Buffer.alloc(64),entries=[];
function encoding(value){const f64=Buffer.alloc(8),f32=Buffer.alloc(4);f64.writeDoubleLE(value);f32.writeFloatLE(value);return {original:value,float64LEHex:f64.toString('hex'),float64WordHex:f64.readBigUInt64LE().toString(16).padStart(16,'0'),packedWord:f32.readUInt32LE(),packedWordHex:f32.readUInt32LE().toString(16).padStart(8,'0'),decoded:f32.readFloatLE()};}
for(let i=0;i<16;i++){const name=i<14?names[i]:'pad'+(i-14),value=i<14?C[name]:0;original.writeDoubleLE(value,i*8);packed.writeFloatLE(value,i*4);entries.push({index:i,name,...encoding(value)});}
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
const extra={};for(const key of ['f0','area','epsilonWake','referenceSumAllowance'])extra[key]=encoding(C[key]);
const result={status:'DATA_INDEPENDENT_CONSTANT_MATERIALIZATION_ONLY',authorization:'Coordinator explicitly authorized isolated arithmetic constant encoding before freeze; no empirical output was seen.',sourceReferenceSha256:'da857f37129c6d3fc87fe223efd2b37b140fbf11417c1f1bb92331d5cfa53cec',runtime:{node:process.version,platform:process.platform,architecture:process.arch},generatorSha256:sha(fs.readFileSync(__filename)),constants:C,entries,extra,originalConstants:{path:'frozen-original-constants.f64',bytes:128,sha256:sha(original)},packedConstants:{path:'frozen-packed-constants.u32',bytes:64,sha256:sha(packed)},operations:{dataIndependentConstants:18,statesDecoded:0,geometryPrepared:0,wakeTerms:0,rootSolves:0,browserLaunches:0,shaderCompilations:0,gpuDispatches:0}};
fs.writeFileSync(path.join(output,'frozen-original-constants.f64'),original,{flag:'wx'});
fs.writeFileSync(path.join(output,'frozen-packed-constants.u32'),packed,{flag:'wx'});
fs.writeFileSync(path.join(output,'constant-encodings.json'),JSON.stringify(result,null,2)+'\n',{flag:'wx'});
console.log(JSON.stringify({status:result.status,originalSha256:sha(original),packedSha256:sha(packed),epsilonWake:C.epsilonWake,referenceSumAllowance:C.referenceSumAllowance}));
