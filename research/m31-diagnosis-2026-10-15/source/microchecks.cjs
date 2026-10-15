'use strict';
const fs=require('fs'),path=require('path'),assert=require('assert/strict'),crypto=require('crypto');
const E=require('./engine.cjs'),root=path.resolve(__dirname,'../../..'),base=path.resolve(__dirname,'..'),raw=path.join(base,'raw'),evidence=path.resolve(process.argv[2]||root),report=path.join(base,'results/microchecks.json');
if(fs.existsSync(report)||fs.existsSync(path.join(raw,'micro-started.json')))throw Error('Microchecks already attempted; no replay of allowance');
fs.mkdirSync(raw,{recursive:true});fs.writeFileSync(path.join(raw,'micro-started.json'),JSON.stringify({allowedTraces:4,totalSimulatedSeconds:.2,consumedOrReserved:[]})+'\n',{flag:'wx'});
const hash=x=>crypto.createHash('sha256').update(x).digest('hex');
const A=E.loadStart(evidence,'A'),B=E.loadStart(evidence,'B');
// No-integration retained first-command controls, both starts.
const firstChecks=[];
for(const [name,ctx,file] of [['A',A,'closed-0.0025-commands.f64'],['B',B,'fine-start-0.0025-commands.f64']]){
 const b=fs.readFileSync(path.join(evidence,'outputs/milestone-32-source',file)),grid=new E.Grid(ctx.states,E.S.P.neighbor);let matched=0;
 for(let i=0;i<1000;i++){const s=ctx.states[i],ids=grid.neighbors(i,E.S.P.neighbor),v=E.steer(i,ctx.states,ids,'boids','wall-priority'),c=E.F.control(s,{vx:v[0],vy:v[1],z:s[2]+(2.5*v[2]+1.5*s[5])/6,yaw:Math.atan2(v[1],v[0])},2.25);for(let k=0;k<4;k++)assert.equal(c.u[k],b.readDoubleLE((i*4+k)*8));matched++;}
 firstChecks.push({start:name,source:file,matchedMotorTargets:matched*4});
}
// Pure fixed-state gate fixtures: change one pair inclusion, keeping all other inputs fixed.
const fixture=[A.states[0].slice(),A.states[1].slice(),A.states[2].slice()];fixture[0].splice(0,3,-10,0,4);fixture[1].splice(0,3,-8.4,0,4);fixture[2].splice(0,3,-10,1,4);
let on,natural;E.steer(0,fixture,[1,2],'boids','wall-priority',d=>natural=d);E.steer(0,fixture,[1,2],'boids','wall-priority',d=>on=d,{pairOverride:{i:0,j:1,include:true}});
assert.deepEqual(natural.pairs.map(x=>x.neighbor),[2]);assert.deepEqual(on.pairs.map(x=>x.neighbor),[1,2]);fixture[1][0]=-8.6;let off;E.steer(0,fixture,[1,2],'boids','wall-priority',d=>off=d,{pairOverride:{i:0,j:1,include:false}});assert.deepEqual(off.pairs.map(x=>x.neighbor),[2]);
const outputs=[],reserve=[];
function reserveTrace(name){reserve.push({name,seconds:.05});fs.writeFileSync(path.join(raw,'micro-started.json'),JSON.stringify({allowedTraces:4,totalSimulatedSeconds:.2,consumedOrReserved:reserve})+'\n');}
function run(id,duration,instrument,context){const job={id,start:'A',dt:.0025,duration,instrument,precontrol:instrument,context};const m=E.runJob(job,evidence,raw);assert(m.complete&&!m.stop);return {meta:m,context:JSON.parse(fs.readFileSync(path.join(raw,id+'-final-context.json')))};}
reserveTrace('frozen');outputs.push(run('micro-frozen',.05,false));
reserveTrace('instrumented');outputs.push(run('micro-instrumented',.05,true));
reserveTrace('boundary-split');const b1=run('micro-boundary-a',.02,true),b2=run('micro-boundary-b',.03,true,b1.context);outputs.push({...b2,parts:[b1.meta,b2.meta]});
reserveTrace('held-command-split');const h1=run('micro-held-a',.025,true),h2=run('micro-held-b',.025,true,h1.context);outputs.push({...h2,parts:[h1.meta,h2.meta]});
const fields=['states','timeTick','controls','crossings','stop','saturationSeconds'];
for(const x of outputs.slice(1))for(const key of fields)assert.deepEqual(x.context[key],outputs[0].context[key],key);
function commands(ids){return Buffer.concat(ids.map(id=>fs.readFileSync(path.join(raw,id+'-commands.f64'))));}
const original=commands(['micro-frozen']);
for(const ids of [['micro-instrumented'],['micro-boundary-a','micro-boundary-b'],['micro-held-a','micro-held-b']])assert(original.equals(commands(ids)),ids.join(','));
const p=outputs[1].meta.phaseMilliseconds;
// Conservative planning rates; diagnostic I/O rates include complete control/state writes.
// The two micro samples are used to estimate the 650 full-matrix samples separately.
const estimateSeconds=2*((p.physics+p.safety)/1000/.05*88+p.control/1000/.05*44+p.io/1000/.05*64+p.measurement/1000/2*650)+120;
const budget=JSON.parse(fs.readFileSync(path.join(base,'results/budget.json'))),alreadyUsed=budget.entries.reduce((s,x)=>s+x.wallSeconds,0);
const result={firstChecks,pairOverrideFixtures:{forcedOnBeyondCutoff:true,forcedOffInsideCutoff:true,otherPairRetained:true},traces:4,totalSimulatedSeconds:.2,endStatesAndHeldControlExactlyEqual:true,allCommandStreamsExactlyEqual:true,endpointHash:hash(JSON.stringify(outputs[0].context.states)),microPhaseMilliseconds:p,fullMatrixPlanningSeconds:estimateSeconds,alreadyUsedBeforeMicroJob:alreadyUsed,preliminaryPlanningGate:estimateSeconds<1200-alreadyUsed,planningLimit:'Supervisor measured current microcheck time must also be subtracted before launch; estimate is a conservative planning gate, not a completion guarantee.',runtime:process.version,outputIds:outputs.map(x=>x.parts?x.parts.map(y=>y.id):[x.meta.id])};
fs.writeFileSync(report,JSON.stringify(result,null,2)+'\n',{flag:'wx'});console.log(JSON.stringify(result));
