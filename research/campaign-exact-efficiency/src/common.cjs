'use strict';
const fs=require('fs'),path=require('path'),crypto=require('crypto');
const M=require('./exact-aero.cjs'),Previous=require('../../campaign-spatial-pruning/src/pruned-aero.cjs');
const config=require('../configs/campaign.json'),root=path.resolve(__dirname,'..');
function evaluator(variant){if(variant==='legacy')return s=>M.A.fields(s,'sum-rotor');if(variant==='previous-zero')return s=>Previous.fields(s,{epsilon:0});return M.createEvaluator({variant});}
function sha(x){return crypto.createHash('sha256').update(x).digest('hex');}
function sourceHash(){return sha(fs.readFileSync(path.join(__dirname,'exact-aero.cjs')));}
function save(name,x){const p=path.join(root,name);fs.mkdirSync(path.dirname(p),{recursive:true});fs.writeFileSync(p,JSON.stringify(x,null,2));return p;}
const median=a=>a.slice().sort((a,b)=>a-b)[Math.floor(a.length/2)];
function bootstrap(a){let x=918273;const rng=()=>((x=(1664525*x+1013904223)>>>0)/4294967296),out=[];for(let b=0;b<5000;b++){const s=[];for(let i=0;i<a.length;i++)s.push(a[Math.floor(rng()*a.length)]);out.push(median(s));}out.sort((a,b)=>a-b);return [out[125],out[4875]];}
module.exports={M,Previous,config,root,evaluator,sha,sourceHash,save,median,bootstrap};
