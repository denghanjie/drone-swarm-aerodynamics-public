'use strict';
const fs=require('fs'),assert=require('assert'),{spawnSync}=require('child_process');
if(process.argv[2]==='variant'){
 const old=require('../milestone-30-source/sim.cjs'),current=require('./sim.cjs');let checks=0;
 for(const count of [50,1000,5000])for(const filter of ['baseline','wall-priority']){
  const config={count,filter,seed:1501,duration:.1,dt:.0025,record:false},a=old.run(config),b=current.run(config);
  assert.deepStrictEqual(a.final,b.final);assert.deepStrictEqual(a.metrics,b.metrics);assert.deepStrictEqual(a.diagnostics,b.diagnostics);checks+=3;
 }
 const states=current.initial(1501,5000),{Grid}=require('./grid.cjs'),grid=new Grid(states,current.P.neighbor);let taggedWalls=0,taggedPairs=0;
 for(let i=0;i<states.length;i++)current.steer(i,states,grid.neighbors(i,current.P.neighbor),'boids','wall-priority',d=>{for(const w of d.walls){assert(current.course.boxes.some(b=>b.id===w.obstacle));taggedWalls++;}for(const p of d.pairs){assert(Number.isInteger(p.neighbor)&&p.neighbor!==i);taggedPairs++;}});
 assert(taggedWalls>0&&taggedPairs>0);checks+=2;console.log(JSON.stringify({variant:process.env.FLOCK_FACTORY_VARIANT,checks,taggedWalls,taggedPairs,passed:true}));
}else{const results=[];for(const variant of ['wide','narrow']){const r=spawnSync(process.execPath,[__filename,'variant'],{env:{...process.env,FLOCK_FACTORY_VARIANT:variant},encoding:'utf8'});if(r.status!==0)throw Error(r.stderr);results.push(JSON.parse(r.stdout));}fs.writeFileSync(__dirname+'/../milestone-31-checks.json',JSON.stringify({checks:results.reduce((s,r)=>s+r.checks,0),passed:true,scope:'Exact old/new final states, metrics and diagnostics for 50/1000/5000 drones, both filters, both factory variants over 0.1s. Tagged wall/pair identifiers verified through the real interface.',results},null,2));console.log(results);}
