'use strict';
/* Deferred fault injection into the actual supervisor source. Virtual clocks,
 * /proc CPU and child lifecycle make the watchdog deterministic and cheap.
 * This does not claim to benchmark or test real OS scheduling latency. */
if(process.env.JOINT_REFERENCE_WINDOW_ACTIVE!=='1')throw Error('Coordinator-authorized numerical window required');
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const filename=path.resolve(__dirname,'../implementation/src/supervise.cjs'),source=fs.readFileSync(filename,'utf8'),tests=[];
function test(name,fn){try{fn();tests.push({name,passed:true});}catch(e){tests.push({name,passed:false,error:{name:e.name,message:e.message,stack:e.stack}});}}
function harness(){
 const ROOT='/virtual/implementation',saved=new Map(),events={},streamEvents={},timers=[],intervals=[],kills=[];
 let clock=0n,live=false,parentTicks=10,childTicks=0,reapedTicks=0;
 const checkpoint={runId:'synthetic-interrupted',tick:128,state:[[1,2,3]],exactStoppedState:false,meaning:'Last durable checkpoint only'};
 const child={pid:22,stdout:{on:(name,fn)=>{streamEvents.stdout=fn;}},stderr:{on:(name,fn)=>{streamEvents.stderr=fn;}},on(name,fn){events[name]=fn;}};
 function stat(pid){if(pid===22&&!live)throw Error('ENOENT');const p=Array(50).fill('0');p[0]='R';p[1]=pid===22?'7':'1';p[11]=String(pid===7?parentTicks:childTicks);p[13]=String(pid===7?reapedTicks:0);return `${pid} (fixture) ${p.join(' ')}`;}
 const fakefs={
  existsSync(p){return p===ROOT+'/results'||p===ROOT+'/results/audit';},
  readFileSync(p){if(/^\/proc\/\d+\/stat$/.test(p))return stat(Number(p.split('/')[2]));if(p==='/proc/7/task/7/children')return live?'22':'';if(p==='/proc/22/task/22/children')return '';throw Error('Unexpected read '+p);},
  readdirSync(p){if(p===ROOT+'/results')return [{name:'audit',isDirectory:()=>true},{name:'data.f64.partial',isDirectory:()=>false}];if(p===ROOT+'/results/audit')return [{name:'fixture.signatures.bin',isDirectory:()=>false}];throw Error('Unexpected directory '+p);},
  statSync(p){return {size:p.endsWith('.signatures.bin')?39:7};}
 };
 const fakeprocess={argv:['node',filename],env:{},pid:7,hrtime:{bigint:()=>clock},kill(pid,signal){kills.push({pid,signal});},exitCode:0};
 const fakeIO={ROOT,load(relative){if(relative==='results/last-checkpoint.json')return checkpoint;return {};},save(relative,body){saved.set(relative,JSON.parse(JSON.stringify(body)));},retainedBytes:()=>46};
 const requireFake=id=>id==='fs'?fakefs:id==='path'?path:id==='child_process'?{fork(){live=true;return child;},execFileSync(){return '100\n';}}:id==='./io.cjs'?fakeIO:id==='./freeze.cjs'?{validateFreeze(){return {};}}:(()=>{throw Error('Unexpected dependency '+id);})();
 const context={require:requireFake,process:fakeprocess,__dirname:path.dirname(filename),module:{exports:{}},Buffer,console,Date,setInterval(fn){intervals.push(fn);return intervals.length;},clearInterval(){},setTimeout(fn,ms){timers.push({fn,ms});return timers.length;},clearTimeout(){}};
 vm.runInNewContext(`(function(){${source}\n})()`,context,{filename});
 return {saved,events,streamEvents,timers,intervals,kills,checkpoint,process:fakeprocess,advance(ns){clock=BigInt(ns);},cpu({parent=parentTicks,child=childTicks}={}){parentTicks=parent;childTicks=child;},reap(){reapedTicks+=childTicks;live=false;childTicks=0;},close(){this.reap();events.close(null,'SIGKILL');}};
}

test('per-job deadline kills worker process group and reports only last durable checkpoint',()=>{
 const h=harness();h.events.message({type:'job-start',id:'synthetic-job',startMonotonicNs:'0',deadlineMonotonicNs:'20000000'});
 assert.equal(h.timers.length,1);assert.equal(h.timers[0].ms,20);h.cpu({parent:12,child:3});h.advance(21000000);h.timers[0].fn();
 assert.equal(h.kills[0].pid,-22);assert.equal(h.kills[0].signal,'SIGKILL');h.close();
 const report=h.saved.get('results/failures/watchdog.json');assert.equal(report.status,'watchdog-stopped');assert.equal(report.exactStoppedState,false);assert.equal(report.lastDurableCheckpoint.exactStoppedState,false);
 assert.equal(h.saved.get('results/execution-validity.json').qualifiedResultsMayBeConsidered,false);assert.ok(report.totalCpuSeconds>=.049);
 const sig=report.artifactInventory.find(x=>x.path.endsWith('.signatures.bin'));assert.equal(sig.completeSignatureRecords,1);assert.equal(sig.trailingBytes,7);assert.ok(report.artifactInventory.some(x=>x.partial));
});

test('live descendant CPU triggers total watchdog even with negligible wall time',()=>{
 const h=harness();h.cpu({parent:10,child:29900});h.advance(1000000);h.intervals[0]();assert.equal(h.kills.length,1);h.close();
 assert.match(h.saved.get('results/failures/watchdog.json').killed.reason,/CPU/);assert.equal(h.saved.get('results/execution-validity.json').qualifiedResultsMayBeConsidered,false);
});

test('overlapping job lifecycle cannot silently reset watchdog deadline',()=>{
 const h=harness();h.events.message({type:'job-start',id:'first',startMonotonicNs:'0',deadlineMonotonicNs:'20000000'});h.events.message({type:'job-start',id:'second',startMonotonicNs:'0',deadlineMonotonicNs:'20000000'});assert.equal(h.kills.length,1);h.close();assert.match(h.saved.get('results/failures/watchdog.json').killed.reason,/Overlapping/);
});

test('failed or skipped execution cannot be relabeled qualified by normal cleanup',()=>{
 const h=harness();h.reap();h.events.close(1,null);const report=h.saved.get('results/supervisor.json');assert.equal(report.status,'worker-stopped');assert.equal(h.saved.get('results/execution-validity.json').qualifiedResultsMayBeConsidered,false);assert.equal(h.process.exitCode,1);
});
const report={schema:'independent-supervisor-fault-fixtures/v1',kind:'actual supervisor source with virtual clocks, CPU census, process-group kill and partial-file inventory',tests,passed:tests.every(t=>t.passed)};process.stdout.write(JSON.stringify(report)+'\n');if(!report.passed)process.exitCode=1;
