'use strict';
// Invoke only after the parent has explicitly authorized the final plan.
const fs=require('fs'),path=require('path');
const {ROOT,load,save,sha,fileSha,sourceManifest}=require('./io.cjs');
if(process.argv[2]!=='--parent-authorized')throw Error('Explicit parent authorization argument required');
if(fs.existsSync(path.join(ROOT,'FREEZE.json')))throw Error('Already frozen; use an explicit amendment instead');
if(!fs.existsSync(path.join(ROOT,'PLAN.md')))throw Error('Final approved PLAN.md missing');
const cfg=load('configs/campaign.json');cfg.status='FROZEN_AUTHORIZED';save('configs/campaign.json',cfg);
const sources=sourceManifest();save('source-manifest.json',sources);
const freeze={status:'FROZEN_AUTHORIZED',frozenAt:new Date().toISOString(),planSha256:fileSha(path.join(ROOT,'PLAN.md')),sourceManifestSha256:sha(JSON.stringify(sources)),sourceAggregateSha256:sources.aggregate,exactEvaluatorSha256:fileSha(path.join(ROOT,'src/exact-aero.cjs')),runtime:{node:process.version,platform:process.platform,arch:process.arch},claim:'Prospective numerical protocol; no new numerical cases observed before freeze'};
save('FREEZE.json',freeze);console.log(JSON.stringify(freeze));
