'use strict';
const fs=require('fs'),path=require('path');
const {root,save}=require('./common.cjs'),{compare}=require('./boids.cjs');
const dir=path.join(root,'results/boids');
const records=fs.readdirSync(dir).filter(x=>x.endsWith('.json')&&x!=='index.json').map(file=>({id:file.slice(0,-5),file,...JSON.parse(fs.readFileSync(path.join(dir,file)))}));
const comparisons=[],refinements=[];
for(const a of records.filter(r=>r.config.variant==='legacy'))for(const b of records.filter(r=>r.config.variant!=='legacy'&&r.config.seed===a.config.seed&&r.config.count===a.config.count&&r.config.dt===a.config.dt&&r.config.aeroDt===a.config.aeroDt))comparisons.push({a:a.id,b:b.id,...compare(a,b)});
const base=records.find(r=>r.config.seed===4391&&r.config.count===16&&r.config.variant==='lean'&&r.config.dt===.0025&&r.config.aeroDt===.01);
if(base)for(const r of records.filter(r=>r.config.seed===4391&&r.config.count===16&&r.config.variant==='lean'&&(r.config.dt!==.0025||r.config.aeroDt!==.01))){const c=compare(base,r);refinements.push({a:base.id,b:r.id,common:c.common,maxPositionM:c.maxPositionM,complete:c.complete,positionScreenPassed:c.complete&&c.maxPositionM<=.01,criterionM:.01,scope:'Common 50ms saved states over1s only; not trajectory convergence or physical validation'});}
const out={records:records.map(({id,file,config,metrics,sourceHash,stateStreamHash,frames})=>({id,file,config,metrics,sourceHash,stateStreamHash,frameCount:frames.length})),comparisons,refinements,recording:'Full initial/final17-entry states; compact saved pose7 and four held inflows at50ms; SHA256 stream covers every integration state and held field.'};save('results/boids/index.json',out);console.log(JSON.stringify({records:out.records.length,completed:records.filter(r=>r.metrics.complete).length,comparisons,refinements}));
