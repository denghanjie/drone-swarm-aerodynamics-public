'use strict';
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto');
const k=require('./interval.cjs'),spec=require('./spec.json');
const output=process.env.RESEARCH_RESULT_PATH;if(!output)throw Error('RESEARCH_RESULT_PATH required');
const journal=fs.openSync(output+'.jsonl','wx');
fs.writeSync(journal,JSON.stringify({kind:'header',schema:'m31-fixed96-journal-v1',specId:spec.id})+'\n');fs.fsyncSync(journal);
let state=BigInt('0x'+spec.seedHex);const mask=(1n<<BigInt(spec.modulusPower))-1n;
const next=()=>state=(state*BigInt(spec.multiplier)+BigInt(spec.increment))&mask;
const bits=spec.explicitBits.slice();for(let i=0;i<spec.generatedBits;i++)bits.push(next().toString(16).padStart(16,'0'));
const S=1n<<BigInt(spec.fractionBits),M=1n<<BigInt(spec.maxEndpointPower);
const symbols={'0':0n,'1':1n,'-1':-1n,S,'-S':-S,'2S':2n*S,'-2S':-2n*S,'3S':3n*S,'-3S':-3n*S,M,'-M':-M,'M-1':M-1n,'-M+1':-M+1n,'S/2':S/2n,'S-1':S-1n,'S+1':S+1n,'4S':4n*S,'9S':9n*S};
const intervals=spec.explicitIntervals.map(([l,u])=>k.interval(symbols[l],symbols[u]));
for(let i=0;i<spec.generatedIntervals;i++){
 const a=(next()%(1n<<40n))-(1n<<39n),b=(next()%(1n<<40n))-(1n<<39n),shift=next()%310n;
 intervals.push(k.interval((a<b?a:b)<<shift,(a>b?a:b)<<shift));
}
const pairs=spec.explicitPairs.map(p=>p.slice());for(let i=0;i<spec.generatedPairs;i++)pairs.push([Number((next()>>32n)%BigInt(intervals.length)),Number((next()>>32n)%BigInt(intervals.length))]);
if(pairs.length!==spec.pairs)throw Error('Pair allocation mismatch');
const rows=[],sha=b=>crypto.createHash('sha256').update(b).digest('hex');
function run(id,op,args){
 const input=op==='fromBits'?args:args.map(k.encode),before=JSON.stringify(input);let result;
 try{result={status:'ok',interval:k.encode(k[op](...args))};}
 catch(e){if(!(e instanceof k.Unqualified))throw e;result={status:e.code};}
 const after=JSON.stringify(op==='fromBits'?args:args.map(k.encode));
 const row={id,op,input,result,inputUnchanged:before===after};rows.push(row);
 fs.writeSync(journal,JSON.stringify({kind:'record',row})+'\n');if(rows.length%32===0)fs.fsyncSync(journal);
}
bits.forEach((b,i)=>run('bits-'+i,'fromBits',[b]));
intervals.forEach((a,i)=>{run('square-'+i,'square',[a]);run('sqrt-'+i,'sqrt',[a]);});
pairs.forEach(([i,j],n)=>{for(const op of ['add','sub','mul','div'])run(op+'-'+n,op,[intervals[i],intervals[j]]);});
if(rows.length!==spec.expectedRecords)throw Error('Allocation count mismatch');
const document={schema:'m31-fixed96-result-v1',specId:spec.id,runtime:{node:process.version,v8:process.versions.v8,platform:process.platform,arch:process.arch},sourceSha256:Object.fromEntries(['interval.cjs','spec.json','run.cjs'].map(n=>[n,sha(fs.readFileSync(path.join(__dirname,n)))])),records:rows};
fs.writeSync(journal,JSON.stringify({kind:'complete',records:rows.length})+'\n');fs.fsyncSync(journal);fs.closeSync(journal);
fs.writeFileSync(output,JSON.stringify(document,null,2)+'\n',{flag:'wx'});
console.log(JSON.stringify({records:rows.length,pathLabel:path.basename(output)}));
