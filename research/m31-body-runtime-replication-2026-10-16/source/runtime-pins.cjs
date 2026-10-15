'use strict';
// Read-only environment admission. No scientific module or input is constructed.
const fs=require('fs'),path=require('path'),crypto=require('crypto');
function inspectChrome(executable,runtime,guard=()=>{}){
 const out={completed:false,explicitExecutable:false,executableLabel:'Google Chrome',frameworkVersion:null,files:[],currentFile:null,bytesChecked:0,scope:'Read-only partial runtime inventory; no scientific construction or browser workload.'};
 const check=(ok,message)=>{if(!ok)throw Error(message);};
 try{
  check(typeof executable==='string'&&path.isAbsolute(executable),'Explicit absolute browser executable required');
  check(path.basename(executable)==='Google Chrome'&&path.basename(path.dirname(executable))==='MacOS','Browser executable layout');
  const contents=path.resolve(path.dirname(executable),'..');
  check(fs.realpathSync(executable)===path.resolve(executable),'Explicit executable must be resolved');out.explicitExecutable=true;
  const framework=path.join(contents,'Frameworks/Google Chrome Framework.framework/Versions/Current');
  const resolvedFramework=fs.realpathSync(framework),frameworkVersion=path.basename(resolvedFramework);
  out.frameworkVersion=/^\d+(?:\.\d+){2,4}$/.test(frameworkVersion)?frameworkVersion:'[non-version target]';
  check(frameworkVersion===runtime.chromeFrameworkVersion,'Current browser framework version');
  check(resolvedFramework===path.resolve(contents,'Frameworks/Google Chrome Framework.framework/Versions',runtime.chromeFrameworkVersion),'Current browser framework location');
  check(Array.isArray(runtime.chromePins)&&runtime.chromePins.length===6,'Browser inventory coverage');
  const chunk=Buffer.alloc(1024*1024);
  for(const pin of runtime.chromePins){
   guard();out.currentFile={label:pin.label,expectedBytes:pin.bytes,expectedSHA256:pin.sha256,observedBytes:null,bytesRead:0,observedSHA256:null};
   const filename=path.resolve(contents,pin.relativeToContents);
   check(filename.startsWith(contents+path.sep),'Contained browser pin');
   check(fs.realpathSync(filename).startsWith(contents+path.sep),'Contained resolved browser pin');
   check(Number.isSafeInteger(pin.bytes)&&pin.bytes>0&&/^[a-f0-9]{64}$/.test(pin.sha256),'Browser pin shape');
   let fd;
   try{
    fd=fs.openSync(filename,'r');out.currentFile.observedBytes=fs.fstatSync(fd).size;check(out.currentFile.observedBytes===pin.bytes,'Browser pin byte length');
    const h=crypto.createHash('sha256');let read=0;
    while(read<pin.bytes){guard();const n=fs.readSync(fd,chunk,0,Math.min(chunk.length,pin.bytes-read),read);check(n>0,'Truncated browser pin');h.update(chunk.subarray(0,n));read+=n;out.currentFile.bytesRead=read;}
    check(fs.readSync(fd,chunk,0,1,pin.bytes)===0,'Growing browser pin');const digest=h.digest('hex');out.currentFile.observedSHA256=digest;check(digest===pin.sha256,'Browser pin digest');
    out.bytesChecked+=read;out.files.push({label:pin.label,bytes:read,sha256:digest});out.currentFile=null;
   }finally{if(fd!==undefined)fs.closeSync(fd);}
  }
  out.completed=true;return out;
 }catch(error){error.partial={kind:'runtime-inventory',buffers:{},metadata:{...out,status:'failed',errorType:error.name,message:error.message}};throw error;}
}
module.exports={inspectChrome};
