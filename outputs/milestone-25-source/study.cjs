'use strict';
const fs=require('fs'),path=require('path'),crypto=require('crypto'),os=require('os'),{spawnSync}=require('child_process');
const dir=__dirname,root=path.resolve(dir,'..'),write=(n,x)=>fs.writeFileSync(path.join(root,n),JSON.stringify(x,null,2));
if(process.argv[2]==='job'){
 const job=JSON.parse(process.argv[3]),S=require('./sim.cjs');
 if(job.kind==='timing')S.run({seed:1400,count:job.count,duration:.1,dt:.005,record:false});
 const r=S.run({seed:job.seed,count:job.count,duration:job.duration,dt:job.dt,record:true});
 fs.writeFileSync(path.join(dir,job.id+'.json'),JSON.stringify({...r,job,environment:{node:process.version,platform:process.platform,arch:process.arch,cpu:os.cpus()[0].model},memory:process.memoryUsage()}));
 console.log(job.id,r.metrics.passed,r.metrics.stopReason,r.timing.total);
}else{
 const jobs=[{id:'audit-1302-200-0.00125',kind:'post-hoc refinement',seed:1302,count:200,duration:120,dt:.00125}];
 // Count order rotates across repeats to reduce systematic warm/thermal ordering bias.
 for(const [rep,counts] of [[1,[50,200,1000,5000]],[2,[5000,1000,200,50]],[3,[200,5000,50,1000]]])for(const count of counts)jobs.push({id:`timing-${rep}-${count}`,kind:'timing',rep,seed:1401,count,duration:2,dt:.005});
 const sources=['study.cjs','sim.cjs','grid.cjs','geometry.cjs','factory.cjs','../step02c-source/physics.cjs'];
 write('milestone-25-protocol.json',{created:new Date().toISOString(),jobs,sourceHashes:Object.fromEntries(sources.map(f=>[f,crypto.createHash('sha256').update(fs.readFileSync(path.join(dir,f))).digest('hex')])),purpose:'Post-hoc numerical audit and serial short-window performance of genuine local Boids at50/200/1000/5000. Not completed large-flock factory missions.',audit:'Compare200-drone seed1302 at2.5ms versus1.25ms: identical finish count/stop, end difference<.01s and max endpoint difference<.01m. Previous5→2.5ms failure remains in record. No parameter tuning.',timing:'Three2s repeats per count, each fresh Node process with0.1s same-count warmup. Fixed seed1401 and physics5ms. No concurrent numerical jobs. Wall time includes initialization, steering, RK4, safety and measurements/recording; excludes JSON serialization and browser rendering. OS/background work may affect timing. Identical repeats measure timing variation, not independent navigation replicates.',initialization:'Same0.75m-spaced jittered3D lattice as milestone24; initial volume grows with count, cross-section capped16×9. Not fixed-volume density scaling.',sourceChange:'Only adds timing.initialization after initial states/clones are created. Numerical instructions and sampling unchanged.',airflow:'off',observation:'ideal'});
 const records=[];
 for(const job of jobs){const r=spawnSync(process.execPath,[__filename,'job',JSON.stringify(job)],{stdio:'inherit'});if(r.status!==0)throw Error(job.id+' failed '+r.status);const data=JSON.parse(fs.readFileSync(path.join(dir,job.id+'.json')));const {frames,initial,final,samples,...compact}=data;records.push(compact);write('milestone-25-progress.json',records);}
 write('milestone-25-summary.json',records);
 const a=JSON.parse(fs.readFileSync(path.join(root,'milestone-24-source/run-1302-200-boids-0.0025.json'))),b=JSON.parse(fs.readFileSync(path.join(dir,jobs[0].id+'.json'))),difference=Math.max(...a.final.map((s,i)=>Math.hypot(...s.slice(0,3).map((x,k)=>x-b.final[i][k]))));
 write('milestone-25-audit.json',{comparison:'post-hoc2.5→1.25ms',difference,counts:[a.metrics.passed,b.metrics.passed],stops:[a.metrics.stopReason,b.metrics.stopReason],passed:difference<.01&&a.metrics.passed===b.metrics.passed&&a.metrics.stopReason===b.metrics.stopReason&&Math.abs(a.metrics.end-b.metrics.end)<.01,initialStatesIdentical:JSON.stringify(a.initial)===JSON.stringify(b.initial)});
 const timing=records.filter(r=>r.job.kind==='timing'),stats=[];
 for(const count of [50,200,1000,5000]){const rs=timing.filter(r=>r.config.count===count),totals=rs.map(r=>r.timing.total).sort((a,b)=>a-b);stats.push({count,totalMs:totals,medianMs:totals[1],simulatedSecondsPerWallSecond:2000/totals[1],medianStages:Object.fromEntries(['initialization','steering','physics','safety','measurement'].map(k=>[k,rs.map(r=>r.timing[k]).sort((a,b)=>a-b)[1]])),allReachedTwoSeconds:rs.every(r=>r.metrics.end===2&&!r.metrics.stopReason)});}
 write('milestone-25-scaling.json',stats);
 fs.writeFileSync(path.join(dir,'factory.json'),JSON.stringify(require('./factory.cjs')));
 fs.writeFileSync(path.join(dir,'index.json'),JSON.stringify([records[0],...timing.filter(r=>r.job.rep===1)].map(r=>({config:r.config,metrics:r.metrics,file:r.job.id+'.json'}))));
}
