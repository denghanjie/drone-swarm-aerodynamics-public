// No GPU/model execution on load. Only the sole supervised driver invokes this API.
let device,loss=null,uncaptured=null,pendingValidation=null,buffers={},pipelines={},groups={},stage='uninitialized';
const sizes={constants:64,nodes:160000,offsets:256,ids:16,terms:6400000,controls:2048,controlOutputs:1280,sums:512};
const bindings={termsMain:[[0,'constants'],[1,'nodes'],[2,'offsets'],[3,'ids'],[4,'terms']],controlsMain:[[0,'constants'],[5,'controls'],[6,'controlOutputs']],reduceMain:[[3,'ids'],[4,'terms'],[7,'sums']]};
const decode64=s=>Uint8Array.from(atob(s),x=>x.charCodeAt(0));
function encode64(bytes){let chunks=[];for(let i=0;i<bytes.length;i+=32768)chunks.push(String.fromCharCode(...bytes.subarray(i,i+32768)));return btoa(chunks.join(''));}
window.wakeHealth=()=>({loss,uncaptured,stage});
window.initializeWake=async()=>{
 window.wakeInitializationEvidence={phase:'request-adapter'};
 if(!navigator.gpu)return {supported:false,reason:'navigator.gpu unavailable'};
 const adapter=await navigator.gpu.requestAdapter({powerPreference:'high-performance'});
 if(!adapter)return {supported:false,reason:'No requested adapter'};
 const info=adapter.info,meta={vendor:info?.vendor,architecture:info?.architecture,device:info?.device,description:info?.description,isFallbackAdapter:info?.isFallbackAdapter??null,features:[...adapter.features],limits:{maxStorageBufferBindingSize:adapter.limits.maxStorageBufferBindingSize,maxBufferSize:adapter.limits.maxBufferSize,maxComputeWorkgroupsPerDimension:adapter.limits.maxComputeWorkgroupsPerDimension,maxStorageBuffersPerShaderStage:adapter.limits.maxStorageBuffersPerShaderStage}};
 if(meta.isFallbackAdapter!==false)return {supported:false,reason:'Nonfallback hardware not established',adapter:meta};
 const adequate=x=>x.maxStorageBufferBindingSize>=6400000&&x.maxBufferSize>=6400000&&x.maxComputeWorkgroupsPerDimension>=1250&&x.maxStorageBuffersPerShaderStage>=5;
 if(!adequate(meta.limits))return {supported:false,reason:'Required adapter limits unavailable',adapter:meta};
 window.wakeInitializationEvidence={phase:'request-device',adapter:meta};
 device=await adapter.requestDevice();meta.deviceLimits={maxStorageBufferBindingSize:device.limits.maxStorageBufferBindingSize,maxBufferSize:device.limits.maxBufferSize,maxComputeWorkgroupsPerDimension:device.limits.maxComputeWorkgroupsPerDimension,maxStorageBuffersPerShaderStage:device.limits.maxStorageBuffersPerShaderStage};
 window.wakeInitializationEvidence={phase:'actual-device-limits',adapter:meta};
 if(!adequate(meta.deviceLimits))return {supported:false,reason:'Required actual device limits unavailable',adapter:meta};
 device.lost.then(x=>{loss={reason:x.reason,message:x.message};});device.addEventListener('uncapturederror',e=>{uncaptured=String(e.error?.message??e.error);});
 window.wakeInitializationEvidence={phase:'shader-compilation',adapter:meta};device.pushErrorScope('validation');
 const response=await fetch('wake.wgsl');if(!response.ok)throw Error('Shader fetch failed');const shader=await response.text(),module=device.createShaderModule({code:shader});
 const compilation=await module.getCompilationInfo(),messages=Array.from(compilation.messages,m=>({type:m.type,message:m.message,lineNum:m.lineNum,linePos:m.linePos,offset:m.offset,length:m.length}));
 window.wakeInitializationEvidence={phase:'pipeline-creation',adapter:meta,shader,messages};
 if(messages.some(x=>x.type==='error'))return {supported:true,compiled:false,adapter:meta,shader,messages,validation:String((await device.popErrorScope())?.message??'')};
 try{for(const entryPoint of Object.keys(bindings)){window.wakeInitializationEvidence.entryPoint=entryPoint;pipelines[entryPoint]=await device.createComputePipelineAsync({layout:'auto',compute:{module,entryPoint}});}}catch(e){return {supported:true,compiled:false,adapter:meta,shader,messages,pipelineError:{name:e.name,message:e.message,entryPoint:window.wakeInitializationEvidence.entryPoint},loss,uncaptured};}
 const error=await device.popErrorScope();stage='initialized';return {supported:true,compiled:!error&&!loss&&!uncaptured,adapter:meta,shader,messages,validation:error?.message??null,loss,uncaptured};
};
window.prepareWake=async input=>{
 if(stage!=='initialized'||loss||uncaptured)throw Error('Wake prepare state');device.pushErrorScope('validation');
 for(const [key,size]of Object.entries(sizes)){
  const output=['terms','controlOutputs','sums'].includes(key);
  buffers[key]=device.createBuffer({size,usage:GPUBufferUsage.STORAGE|(output?GPUBufferUsage.COPY_SRC:GPUBufferUsage.COPY_DST)});
  if(!output){const bytes=decode64(input[key]);if(bytes.length!==size)throw Error('Input byte shape '+key);device.queue.writeBuffer(buffers[key],0,bytes);}
 }
 for(const [entry,items]of Object.entries(bindings))groups[entry]=device.createBindGroup({layout:pipelines[entry].getBindGroupLayout(0),entries:items.map(([binding,key])=>({binding,resource:{buffer:buffers[key]}}))});
 const validation=await device.popErrorScope();stage='prepared';return {sizes,validation:validation?.message??null,loss,uncaptured};
};
window.dispatchWake=async(kind,timeoutMs)=>{
 const configs={controls:{from:'prepared',to:'controls-read',entry:'controlsMain',output:'controlOutputs',groups:1,count:16},terms:{from:'controls-read',to:'terms-read',entry:'termsMain',output:'terms',groups:1250,count:80000},reduce:{from:'terms-read',to:'sums-read',entry:'reduceMain',output:'sums',groups:1,count:16}};
 const c=configs[kind];if(!c||stage!==c.from||loss||uncaptured||pendingValidation)throw Error('Wake dispatch state or GPU health');
 const bytes=sizes[c.output];window.lastWakeDispatch={kind,count:c.count,groups:c.groups,outputBytes:bytes,submitted:false,materializedTermsPreserved:kind==='reduce'};
 device.pushErrorScope('validation');const read=device.createBuffer({size:bytes,usage:GPUBufferUsage.COPY_DST|GPUBufferUsage.MAP_READ});
 const encoder=device.createCommandEncoder(),pass=encoder.beginComputePass();pass.setPipeline(pipelines[c.entry]);pass.setBindGroup(0,groups[c.entry]);pass.dispatchWorkgroups(c.groups);pass.end();encoder.copyBufferToBuffer(buffers[c.output],0,read,0,bytes);device.queue.submit([encoder.finish()]);window.lastWakeDispatch.submitted=true;
 let timer;
 try{await Promise.race([read.mapAsync(GPUMapMode.READ),new Promise((_,reject)=>{timer=setTimeout(()=>{device.destroy();reject(Error('Wake dispatch timeout'));},timeoutMs);})]);
  const bytesReturned=new Uint8Array(read.getMappedRange()).slice();read.unmap();stage=c.to;
  pendingValidation=device.popErrorScope().then(e=>({validation:e?.message??null})).catch(e=>({validation:String(e.message)}));
  return {base64:encode64(bytesReturned),bytes:bytesReturned.length,dispatch:window.lastWakeDispatch};
 }finally{clearTimeout(timer);read.destroy();}
};
window.finishWakeBatch=async()=>{if(!pendingValidation)throw Error('No pending GPU batch');const r=await pendingValidation;pendingValidation=null;return {...r,loss,uncaptured,stage};};
window.shutdownWake=()=>{for(const b of Object.values(buffers))b.destroy();device?.destroy();};
window.wakeRunnerReady=true;
