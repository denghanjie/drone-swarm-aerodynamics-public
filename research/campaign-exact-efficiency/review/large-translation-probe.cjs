'use strict';
// Tiny deterministic numerical counterexample, intentionally not a flight layout.
// Pass the candidate module path explicitly; no local machine path is embedded.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const file=path.resolve(process.argv[2]);
let E;if(process.argv[3]){const base=path.resolve(process.argv[3]),M=require('node:module'),m=new M(base);m.filename=base;m.paths=M._nodeModulePaths(path.dirname(base));m._compile(fs.readFileSync(file,'utf8'),base);E=m.exports;}else E=require(file);
const pose=(x,y,z,q=[0,0,0,1])=>[x,y,z,0,0,0,...q,0,0,0,...Array(4).fill(E.F.P.m*E.F.P.g/4)];
const d=.45/(3*E.W.parameters.spread)+E.W.parameters.origin*E.P.motorDistance;
const states=[pose(0,3e14,1,[0,0,Math.sin(Math.PI/8),Math.cos(Math.PI/8)]),pose(0,3e14+.5,1+d)];
const results={};
for(const variant of ['legacy',...E.variants]){
 try{results[variant]=variant==='legacy'?E.A.fields(states,'sum-rotor'):E.fields(states,{variant});}
 catch(e){results[variant]={error:e.name,message:e.message,detail:e.detail};}
}
console.log(JSON.stringify({scope:'Extreme-coordinate software boundary probe, not a plausible flight or physical reference',sourceSHA256:crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex'),states,results},null,2));
