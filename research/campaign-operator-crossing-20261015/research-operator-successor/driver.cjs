'use strict';
// python3 supervise.py RELEASE_SHA [source-root]
// Release SHA frames each name/content with uint32 LE byte lengths.
const fs=require('fs'), path=require('path'), crypto=require('crypto');
const root=__dirname, digest=b=>crypto.createHash('sha256').update(b).digest('hex');
const sourceRoot=path.resolve(process.argv[3]||root), release=crypto.createHash('sha256');
const released=['driver.cjs','supervise.py','SOURCE-MANIFEST.json',
  '../research-operator-successor-plan/PROTOCOL.md',
  '../research-operator-successor-plan/STORAGE-AMENDMENT.reverse.patch',
  '../research-operator-successor-review/FEASIBILITY-REVIEW.md'];
for(const name of released){
  const key=Buffer.from(name),content=fs.readFileSync(path.resolve(root,name)),frame=Buffer.alloc(8);
  frame.writeUInt32LE(key.length);frame.writeUInt32LE(content.length,4);release.update(frame).update(key).update(content);
}
if(process.argv[2]!==release.digest('hex'))throw Error('Missing hash-bound release');
const manifest=JSON.parse(fs.readFileSync(path.join(root,'SOURCE-MANIFEST.json')));
let sourceBytes=0;
for(const [name,size,blob,sha] of manifest.files){
  const content=fs.readFileSync(path.join(sourceRoot,name));
  const git=crypto.createHash('sha1').update('blob '+content.length+'\0').update(content).digest('hex');
  if(content.length!==size||digest(content)!==sha||git!==blob)throw Error('Source identity: '+name);
  sourceBytes+=size;
}
function inventory(dir){return fs.readdirSync(dir,{withFileTypes:true}).flatMap(e=>{
  const p=path.join(dir,e.name);return e.isDirectory()?inventory(p):[{path:p,size:fs.statSync(p).size}];
});}
const files=[root,path.resolve(root,'../research-operator-successor-plan'),path.resolve(root,'../research-operator-successor-review')].flatMap(inventory);
const localSources=manifest.files.reduce((a,[n])=>a+(fs.existsSync(path.join(root,n))?fs.statSync(path.join(root,n)).size:0),0);
const primary=files.reduce((a,f)=>a+f.size,0)+Math.max(0,20997-localSources)+30000+3000;
if(sourceBytes!==20997||manifest.files.length!==6||primary>90000||primary-20997+4954>75000)throw Error('Storage admission');
if(files.some(f=>f.path.endsWith('/EVIDENCE.bin')||f.path.endsWith('/RUN.json')))throw Error('No retry permitted');
const started=performance.now(), cpu=process.cpuUsage(), C=new Uint32Array(32);
const evidence=Buffer.alloc(26000), output=path.join(root,'EVIDENCE.bin');
const fd=fs.openSync(output,'wx'), streams=Array.from({length:5},()=>crypto.createHash('sha256'));
let currentCase=0,currentNode=0,eventRow=0,currentSide=0,currentMethod=0,completedScores=0;
for(let slot=0;slot<80;slot++)evidence.writeUInt32LE(0xffffffff,10820+slot*88);
function u32(offset,values){for(const v of values){evidence.writeUInt32LE(v,offset);offset+=4;}return offset;}
function f64(offset,values){for(const v of values){if(!Number.isFinite(v))throw Error('Nonfinite record');evidence.writeDoubleLE(v===0?0:v,offset);offset+=8;}return offset;}
function flush(status){
  let at=20416;
  for(const f of fine){at=f64(at,[...f.max,...f.sum,f.rawMax,Number.isFinite(f.min)?f.min:0,f.clampMax,f.clampSum,f.leakMax,f.leakIntegral]);at=u32(at,[f.neg,f.deep,f.leakCount]);}
  for(const c of coarse){at=f64(at,[...c.max,c.leakMax,c.leakIntegral]);at=u32(at,[c.leakCount]);}
  for(const s of strata)at=f64(at,s);at=u32(at,nodeCounts);
  for(const stream of streams){stream.copy().digest().copy(evidence,at);at+=32;}at=u32(at,C);
  times[4]=performance.now()-started;const used=process.cpuUsage(cpu);times[5]=used.user/1000;times[6]=used.system/1000;
  at=f64(at,times);at=u32(at,decisions);check(at===26000,'Schema size');
  const verdict=decisions.some(d=>d&1)?1:decisions.some(d=>d>>>1)?2:0;
  u32(0,[0x3143504f,1,status,currentCase,currentNode,eventRow,currentSide,currentMethod,completedScores,verdict]);
  check(fs.writeSync(fd,evidence,0,evidence.length,0)===26000,'Short write');fs.fsyncSync(fd);
}
function check(ok,label){if(!ok)throw Error(label);}
function hash(stream,tag,integers,values){
  const record=Buffer.alloc(4+4*integers.length+8*values.length);let at=0;
  for(const v of [tag,...integers]){record.writeUInt32LE(v,at);at+=4;}
  for(const v of values){check(Number.isFinite(v),'Hash finite');record.writeDoubleLE(v===0?0:v,at);at+=8;}
  streams[stream].update(record);C[24]++;C[25]+=record.length;
}
function budget(){check(performance.now()-started<17500,'Time budget');check(C[4]+C[7]<=110000,'Kernel cap');}
function metricRow(slot,method,side,truth,raw,value){
  const offset=10816+slot*88;
  f64(u32(offset,[currentCase,currentNode,method,side]),[...truth,...raw,value]);
}
// At20416: fine16*108,coarse16*44,strata16*168,counts4*28,hash5*32,C32*4,
// times7*8,decisions2*4=5584B. Metric n=UINT_MAX/gate flag0 mean absent.
// C: fields/pairs/slots,sourceZeros,kernels,exactCalls/slots/kernels,supportTests,
// geometryNodes,events,degree0/1/2,shadows/gates/terminal,samples/scalars,loads/zero,
// wrenches,scores,clamps,hashRecords/bytes,identityCalls,d1/d2,radialZeros,outsideChecks,crosschecks.
// Event word: case[0:1],interval[2:10],mask[11:26],upperBracket[27]; top bits zero.
// Header40..47: max observed |roll moment|/(weight*arm), all loads/sides.
const fine=Array.from({length:16},()=>({max:[0,0,0],sum:[0,0,0],rawMax:0,min:Infinity,clampMax:0,clampSum:0,leakMax:0,leakIntegral:0,neg:0,deep:0,leakCount:0}));
const coarse=Array.from({length:16},()=>({max:[0,0,0],leakMax:0,leakIntegral:0,leakCount:0}));
const strata=Array.from({length:16},()=>Array(21).fill(0)), nodeCounts=Array(28).fill(0), times=Array(7).fill(0);
const gateSeen=Array(32).fill(false), decisions=[0,0];
class Supply{
  constructor(){this.history=[];this.hold=Array(4).fill(false);this.shadow=[];this.k=-1;}
  value(method,alpha,r){
    const h=this.history,u=h[0][r];
    if(method===0||this.k===0||(method===3&&this.hold[r])){C[11]++;return u;}
    const d1=u-h[1][r],linear=u+alpha*d1;C[27]++;
    if(method===1||this.k===1){C[12]++;return linear;}
    const d2=(u-2*h[1][r])+h[2][r];C[13]++;C[28]++;
    return linear+((alpha*(alpha+1))*0.5)*d2;
  }
  accept(sample,terminal){
    C[17]++;C[18]+=4;
    if(this.k>=2)for(let r=0;r<4;r++){
      const old=this.history.map(h=>h[r]),s=this.shadow[r],N=Math.abs(sample[r]-s),B=Math.abs(sample[r]-old[0]);
      const category=B<=1e-12?(N<=1e-12?0:1):2;
      const hold=category===1||(category===2&&N>0.9*B);
      hash(3,5,[currentCase,this.k+1,r,category,Number(hold),Number(terminal)],[...old,sample[r],s,N,B,0.9*B]);
      if(terminal){C[16]++;continue;}C[15]++;
      if(hold!==this.hold[r]){
        const slot=currentCase*8+r*2+Number(!hold);
        if(!gateSeen[slot]){gateSeen[slot]=true;f64(u32(17856+slot*80,[currentCase,this.k+1,r,1|(Number(hold)<<1)|(category<<2)]),[...old,sample[r],s,N,B,0.9*B]);}
      }
      this.hold[r]=hold;
    }
    this.k++;this.history.unshift(sample.slice());this.history.length=Math.min(3,this.history.length);
    if(this.k>=2&&!terminal)for(let r=0;r<4;r++){
      const [a,b,c]=this.history.map(h=>h[r]),d1=a-b,d2=(a-2*b)+c;
      this.shadow[r]=(a+1*d1)+((1*(1+1))*0.5)*d2;C[14]++;C[27]++;C[28]++;
      hash(3,4,[currentCase,this.k,r],[this.shadow[r]]);
    }
  }
}
try{
  flush(1);
  const X=require(path.join(sourceRoot,'src/exact-aero.cjs')),{A,F,W}=X,exact=X.createEvaluator({variant:'lean'});
  const nominal=F.P.m*F.P.g/4,weight=F.P.m*F.P.g,arm=F.P.a;
  const half=W.parameters.spread*(.5/A.P.motorDistance-W.parameters.origin)*A.P.motorDistance;
  const originalWake=W.normalizedWake;
  W.normalizedWake=(...args)=>{check(C[4]+C[7]<110000,'Kernel cap');C[4]++;return originalWake(...args);};
  const state=(x,z)=>[x,0,z,0,0,0,0,0,0,1,0,0,0,nominal,nominal,nominal,nominal];
  function loads(inflow){
    const thrust=inflow.map(v=>{check(Number.isFinite(v)&&v>=0,'Load input');C[19]++;if(v===0)C[20]++;return A.effectiveThrust(nominal,v);});
    C[21]++;const w=F.wrench(thrust),roll=Math.abs(w.t[0])/(weight*arm);
    evidence.writeDoubleLE(Math.max(evidence.readDoubleLE(40),roll),40);check(roll<=1e-12,'Roll symmetry');
    return {thrust,T:w.T,mx:w.t[0],my:w.t[1]};
  }
  check(A.effectiveThrust(nominal,0)===nominal&&A.effectiveThrust(0,1)===0,'Zero-load identities');C[19]+=2;C[20]+=2;C[26]+=2;
  const power=A.idealPower(nominal,0),nominalWrench=F.wrench(Array(4).fill(nominal));C[26]+=2;C[21]++;
  check(nominalWrench.T===weight&&nominalWrench.t.every(v=>v===0),'Nominal wrench');
  for(currentCase=0;currentCase<4;currentCase++){
    const phase=performance.now(),R=currentCase<2?16:64,phi=currentCase%2?R/25600:0,H=R/12800;
    const position=n=>.22-.12*Math.cos(4*Math.PI*(n/12800+phi));
    const tags=new Map(),brackets=new Map(),supply=new Supply();
    for(let r=0;r<4;r++)for(let type=0;type<4;type++){
      const cutoff=type===0||type===3?2:3,xe=Math.sqrt((cutoff*half)**2-arm**2)-F.rotors[r][0];
      const angle=Math.acos((.22-xe)/.12)/(4*Math.PI),tau=(type<2?angle:.5-angle)-phi;
      check(Number.isFinite(tau)&&tau>0&&tau<.5,'Event domain');
      const tick=tau*12800,lo=Math.floor(tick),hi=Math.ceil(tick);
      check(lo!==hi,'Grid-event ambiguity');
      const sign=n=>Math.hypot(position(n)+F.rotors[r][0],arm)-cutoff*half;
      check(type<2?sign(lo)<0&&sign(hi)>0:sign(lo)>0&&sign(hi)<0,'Event bracket');
      const nearest=Math.round(tau/H),k=Math.abs(tau-nearest*H)<=1e-12?nearest-1:Math.floor(tau/H);
      check(k>=0&&k<6400/R,'Event clock');
      const mask=1<<(4*type+r);tags.set(k,(tags.get(k)||0)|mask);
      for(const [n,side] of [[lo,0],[hi,1]])brackets.set(n,(brackets.get(n)||currentCase)|(k<<2)|(mask<<11)|(side<<27));
      C[10]++;
    }
    check(brackets.size===16,'Unique event nodes');
    for(currentNode=0;currentNode<=6400;currentNode++){
      const n=currentNode,states=[state(0,.5),state(position(n),0)];
      check(states.every(s=>s.length===17&&s.every(Number.isFinite)),'State schema');
      const before=C[4];C[0]++;const field=A.fields(states,'sum-rotor');check(field.candidates===2,'Neighbors');C[1]+=field.candidates;C[2]+=4*field.candidates;C[3]+=4;C[8]+=4;C[29]+=4-(C[4]-before);
      const truth=field.winds[1];check(field.winds[0].every(v=>v===0),'Source zeros');
      truth.forEach(v=>check(Number.isFinite(v)&&v>=0,'Truth finite'));
      hash(0,1,[currentCase,n],field.winds.flat());
      if(n%200===0){
        check(C[4]+C[7]+8<=110000,'Crosscheck kernel reserve');C[5]++;const reference=exact(states);C[6]+=4*reference.candidates;C[7]+=reference.evaluatedRotorKernels;C[3]+=4;C[8]+=4;C[29]+=4-reference.evaluatedRotorKernels;
        for(let i=0;i<2;i++)for(let r=0;r<4;r++){const a=field.winds[i][r],b=reference.winds[i][r];C[31]++;check(Math.abs(a-b)<=1e-12+1e-12*Math.max(Math.abs(a),Math.abs(b)),'Exact crosscheck');}
      }
      const outside=F.rotors.map(([dx,dy])=>Math.hypot(position(n)+dx,dy)>=3*half);
      C[9]++;C[30]+=4;hash(4,6,[currentCase,n,...outside.map(Number)],[position(n),half]);
      const truthLoad=loads(truth);hash(2,3,[currentCase,n,0,4],[...truthLoad.thrust,truthLoad.T,truthLoad.mx,truthLoad.my]);
      if(n===0)for(let r=0;r<4;r++){C[26]++;check(Math.abs(A.idealPower(truthLoad.thrust[r],truth[r])-power)<=1e-12,'Fixed-power identity');}
      if(n===0)supply.accept(truth,false);
      const score=side=>{
        currentSide=side;
        const k=supply.k,alpha=side?0:(n-k*R)/R,flags=tags.get(k)||0;
        const groups=[k<2?0:flags?1:2,...[0,1,2,3].filter(t=>flags&(15<<(4*t))).map(t=>t+3)];
        if(!side)for(const g of groups)nodeCounts[currentCase*7+g]++;
        const allRaw=[];
        for(let method=0;method<4;method++){
          currentMethod=method;
          const raw=truth.map((_,r)=>supply.value(method,alpha,r)),delivered=raw.map(v=>Math.max(0,v));
          check(raw.every(Number.isFinite),'Prediction finite');
          if(side)check(delivered.every((v,r)=>v===truth[r]),'Outgoing equality');
          allRaw.push(...raw);C[22]++;C[23]+=4;
          hash(1,2,[currentCase,n,side,method],[...raw,...delivered]);
          const load=loads(delivered);hash(2,3,[currentCase,n,side,method],[...load.thrust,load.T,load.mx,load.my]);
          const errors=[Math.max(...delivered.map((v,r)=>Math.abs(v-truth[r]))),Math.abs(load.T-truthLoad.T)/weight,Math.hypot(load.mx-truthLoad.mx,load.my-truthLoad.my)/(weight*arm)];
          const index=currentCase*4+method,f=fine[index],c=coarse[index];
          for(let j=0;j<3;j++){
            if(n===0||errors[j]>f.max[j]){f.max[j]=errors[j];metricRow(index*3+j,method,side,truth,raw,errors[j]);}
            if(!side&&n>0)f.sum[j]+=errors[j]/12800;
            for(const g of groups)strata[index][g*3+j]=Math.max(strata[index][g*3+j],errors[j]);
            if(n%2===0)c.max[j]=Math.max(c.max[j],errors[j]);
          }
          const leak=Math.max(...delivered.map((v,r)=>outside[r]?v:0)),minimum=Math.min(...raw);
          if(n===0||leak>f.leakMax){f.leakMax=leak;metricRow(48+index*2,method,side,truth,raw,leak);}
          if(minimum<f.min){f.min=minimum;metricRow(49+index*2,method,side,truth,raw,minimum);}
          if(n%2===0)c.leakMax=Math.max(c.leakMax,leak);
          for(let r=0;r<4;r++){
            const clamp=delivered[r]-raw[r];f.rawMax=Math.max(f.rawMax,Math.abs(raw[r]-truth[r]));f.clampMax=Math.max(f.clampMax,clamp);
            if(!side){f.neg+=Number(raw[r]<0);f.deep+=Number(raw[r]<-1e-12);f.clampSum+=clamp;
              if(outside[r]){f.leakCount+=Number(delivered[r]>1e-12);if(n>0)f.leakIntegral+=delivered[r]/51200;
                if(n%2===0){c.leakCount+=Number(delivered[r]>1e-12);if(n>0)c.leakIntegral+=delivered[r]/25600;}}
            }
          }
          completedScores++;
        }
        if(!side&&brackets.has(n)){f64(u32(64+eventRow*168,[brackets.get(n),n]),[...truth,...allRaw]);eventRow++;}
      };
      score(0);
      if(n>0&&n%R===0){supply.accept(truth,n===6400);if(n<6400)score(1);}
      if(n%256===0){budget();flush(1);}
    }
    times[currentCase]=performance.now()-phase;
  }
  check(eventRow===64&&C[0]===25604&&C[5]===132&&C[14]===3968&&C[15]===3952&&C[16]===16&&C[19]===528018,'Work-count identity');
  for(let candidate=2;candidate<4;candidate++){
    let weak=true,strict=false,reversals=0;
    const reversed=(a,b,floor)=>a*b<0&&Math.abs(a)>floor&&Math.abs(b)>floor;
    for(let ci=0;ci<4;ci++){
      const i=ci*4+candidate,l=ci*4+1;
      for(let j=0;j<3;j++){
        const d=fine[i].max[j]-fine[l].max[j],e=coarse[i].max[j]-coarse[l].max[j];
        weak&&=d<=1e-10&&e<=1e-10;strict||=d<-1e-10&&e<-1e-10;
        if(reversed(d,e,1e-10))reversals|=1<<(ci*6+j);
      }
      for(const [j,key,floor] of [[3,'leakMax',1e-10],[4,'leakCount',0],[5,'leakIntegral',5e-11]]){
        const d=fine[i][key]-fine[l][key],e=coarse[i][key]-coarse[l][key];weak&&=d<=floor&&e<=floor;
        if(reversed(d,e,floor))reversals|=1<<(ci*6+j);
      }
    }
    decisions[candidate-2]=Number(weak&&strict)|(reversals<<1);
  }
  budget();flush(2);fs.closeSync(fd);
}catch(error){try{flush(3);fs.closeSync(fd);}catch{}
  process.stderr.write(String(error.stack).replaceAll(root,'<campaign-code>').replaceAll(sourceRoot,'<source-root>').slice(0,3000));process.exitCode=1;
}
