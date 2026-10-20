'use strict';
// Lossless byte storage only. No model or scientific dependency is loaded here.
const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto'),zlib=require('node:zlib'),assert=require('node:assert/strict');
class Journal{
 constructor(dir,file,{guard,charge,maxRecordBytes=4*1024*1024,blockBytes=16*1024*1024,partBytes=32*1024*1024}){
  assert.ok(/^[a-zA-Z0-9-]+\.jsonl\.gz$/.test(file));assert.ok(Number.isSafeInteger(blockBytes)&&blockBytes>=maxRecordBytes);assert.ok(Number.isSafeInteger(partBytes)&&partBytes>0);
  Object.assign(this,{dir,file,guard,charge,maxRecordBytes,blockBytes,partBytes,records:0,rawBytes:0,bytes:0,blocks:[],blockSize:0,parts:[],fd:null,current:null,closed:false});
  this.rawHash=crypto.createHash('sha256');this.hash=crypto.createHash('sha256');
 }
 append(value){assert.ok(!this.closed);this.guard();const raw=Buffer.from(JSON.stringify(value)+'\n');assert.ok(raw.length<=this.maxRecordBytes,'record-size-budget');if(this.blockSize+raw.length>this.blockBytes)this.flush();this.blocks.push(raw);this.blockSize+=raw.length;this.rawHash.update(raw);this.rawBytes+=raw.length;this.records++;}
 openPart(){const file=this.file+'.part'+String(this.parts.length).padStart(3,'0');this.fd=fs.openSync(path.join(this.dir,file),'wx');this.current={file,bytes:0,offset:this.bytes,hash:crypto.createHash('sha256')};}
 closePart(){if(this.fd===null)return;fs.fsyncSync(this.fd);fs.closeSync(this.fd);this.fd=null;const p=this.current;this.parts.push({file:p.file,bytes:p.bytes,sha256:p.hash.digest('hex'),offset:p.offset});this.current=null;}
 flush(){this.guard();if(!this.blockSize)return;const compressed=zlib.gzipSync(Buffer.concat(this.blocks,this.blockSize),{level:6});this.guard();this.charge(compressed.length);let off=0;
  while(off<compressed.length){this.guard();if(this.fd===null)this.openPart();const n=Math.min(this.partBytes-this.current.bytes,compressed.length-off),chunk=compressed.subarray(off,off+n);let written=0;while(written<n){const m=fs.writeSync(this.fd,chunk,written,n-written);assert.ok(m>0,'short-write');written+=m;}this.current.hash.update(chunk);this.hash.update(chunk);this.current.bytes+=n;this.bytes+=n;off+=n;if(this.current.bytes===this.partBytes)this.closePart();}
  this.blocks=[];this.blockSize=0;
 }
 finish(){assert.ok(!this.closed);this.flush();this.closePart();this.closed=true;return {file:this.file,bytes:this.bytes,sha256:this.hash.digest('hex'),records:this.records,parts:this.parts,rawBytes:this.rawBytes,rawSha256:this.rawHash.digest('hex')};}
 closeIncomplete(){if(this.fd!==null){fs.fsyncSync(this.fd);fs.closeSync(this.fd);this.fd=null;}this.closed=true;}
}
module.exports={Journal};
