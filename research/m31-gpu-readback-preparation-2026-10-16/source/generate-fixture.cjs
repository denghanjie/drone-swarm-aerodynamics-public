'use strict';
// Static integer reference only. Does not load or execute the browser module/WGSL.
const fs=require('node:fs');const path=require('node:path');const crypto=require('node:crypto');
const MASK=0xffffffffn;
const initial=Array.from({length:32},(_,j)=>0xd15ea5e5n^((BigInt(j)*0x01010101n)&MASK));
const expected=initial.slice();
for(let i=0;i<17;i++)expected[4+i]=(((0x9e3779b9n*BigInt(i+1)&MASK)^0xa5a5a5a5n)+0x7f4a7c15n)&MASK;
function bytes(words){return Buffer.from(words.flatMap(word=>[0n,8n,16n,24n].map(shift=>Number((word>>shift)&255n))));}
const initialBytes=bytes(initial),expectedBytes=bytes(expected);
const sha=bytes=>crypto.createHash('sha256').update(bytes).digest('hex');
const descriptor={version:1,kind:'static-only-gpu-readback-fixture',fixtureId:'m31-u32-readback-128-v1',wordCount:32,byteLength:128,prefixWords:4,activeWords:17,suffixWords:11,workgroupSize:8,dispatchGroups:3,launchedInvocations:24,endianness:'little',initialFormula:'S(j) = 0xD15EA5E5 XOR ((j * 0x01010101) mod 2^32)',activeFormula:'word[4+i] = ((((0x9E3779B9 * (i+1)) mod 2^32) XOR 0xA5A5A5A5) + 0x7F4A7C15) mod 2^32',initialSHA256:sha(initialBytes),expectedSHA256:sha(expectedBytes),initialWordsHex:initial.map(v=>v.toString(16).padStart(8,'0')),expectedWordsHex:expected.map(v=>v.toString(16).padStart(8,'0')),executionAllocated:false};
fs.writeFileSync(path.join(__dirname,'initial-sentinels.bin'),initialBytes);
fs.writeFileSync(path.join(__dirname,'expected.bin'),expectedBytes);
fs.writeFileSync(path.join(__dirname,'FIXTURE.json'),JSON.stringify(descriptor,null,2)+'\n');
console.log(JSON.stringify({byteLength:128,initialSHA256:descriptor.initialSHA256,expectedSHA256:descriptor.expectedSHA256}));
