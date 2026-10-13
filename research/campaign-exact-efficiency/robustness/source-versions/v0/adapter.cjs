'use strict';
const fs=require('node:fs'),path=require('node:path');
const roots=[process.env.EXACT_REPO_ROOT,path.resolve(__dirname,'../../..'),path.resolve(__dirname,'../implementation/repo')].filter(Boolean);
const root=roots.find(r=>fs.existsSync(path.join(r,'outputs/milestone-28-source/aero.cjs')));
if(!root)throw Error('Set EXACT_REPO_ROOT to a repository with the pinned source subset.');
const paths={legacy:path.join(root,'outputs/milestone-28-source/aero.cjs'),previous:path.join(root,'research/campaign-spatial-pruning/src/pruned-aero.cjs'),candidate:process.env.EXACT_CANDIDATE_PATH||path.join(root,'research/campaign-exact-efficiency/src/exact-aero.cjs')};
const F=require(path.join(root,'outputs/step02c-source/physics.cjs')),A=require(paths.legacy),P=require(paths.previous);
const E=fs.existsSync(paths.candidate)?require(paths.candidate):null;
function methods(){const out={legacy:s=>A.fields(s,'sum-rotor'),'previous-zero':s=>P.fields(s,{epsilon:0})};if(E){for(const v of ['lean','support','reuse']){const fn=E.createEvaluator({variant:v});out[v]=s=>fn(s);}}return out;}
module.exports={root,paths,F,A,P,E,methods};
