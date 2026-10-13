'use strict';
const fs=require('fs'),path=require('path'),{spawn}=require('child_process');const dir=__dirname,root=path.resolve(dir,'..'),save=(f,x)=>fs.writeFileSync(path.join(root,f),JSON.stringify(x,null,2));
if(process.argv[2]==='job'){
 const job=JSON.parse(process.argv[3]),S=require('./sim.cjs'),fd=fs.openSync(path.join(dir,job.id+'.f64'),'w');let frames=0;
 const r=S.run({...job,record:true,frameEvery:1,frameSink(frame){const b=Buffer.allocUnsafe(frame.length*8);frame.forEach((x,i)=>b.writeDoubleLE(x,i*8));fs.writeSync(fd,b);frames++;},progress(p){save('milestone-30-source/progress-'+job.id+'.json',{...p,job,updated:new Date().toISOString()});}});fs.closeSync(fd);r.job=job;r.replay={file:job.id+'.f64',frames,valuesPerFrame:1+7*job.count,dtype:'Float64LE',cadence:1};save('milestone-30-source/'+job.id+'.json',r);console.log('DONE',job.id,JSON.stringify(r.metrics),JSON.stringify(r.diagnostics));
}else(async()=>{
 const protocol=JSON.parse(fs.readFileSync(path.join(root,'milestone-30-protocol.json'))),jobs=protocol.jobs,results=[];let next=0;
 async function worker(){while(next<jobs.length){const job=jobs[next++];const file=path.join(dir,job.id+'.json');if(!fs.existsSync(file))await new Promise((resolve,reject)=>{const c=spawn(process.execPath,[__filename,'job',JSON.stringify(job)],{stdio:'inherit'});c.on('error',reject);c.on('exit',c=>c===0?resolve():reject(Error('job failed '+job.id)));});const r=JSON.parse(fs.readFileSync(file));results.push({config:r.config,metrics:r.metrics,diagnostics:r.diagnostics,job:r.job,file:job.id+'.json',geometry:'factory-wide.json'});save('milestone-30-progress.json',results);save('milestone-30-source/index.json',results);}}
 await Promise.all([worker(),worker()]);save('milestone-30-summary.json',results.sort((a,b)=>jobs.findIndex(j=>j.id===a.job.id)-jobs.findIndex(j=>j.id===b.job.id)));
})().catch(e=>{console.error(e);process.exitCode=1;});
