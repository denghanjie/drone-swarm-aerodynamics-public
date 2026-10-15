// No model execution on load. The sole supervised driver explicitly initializes and dispatches.
let device,pipeline,loss=null,pendingValidation=null;
window.initializeReceiver=async()=>{
 window.receiverInitializationEvidence={phase:'request-adapter'};
 if(!navigator.gpu)return {supported:false,reason:'navigator.gpu unavailable'};
 const adapter=await navigator.gpu.requestAdapter({powerPreference:'high-performance'});
 if(!adapter)return {supported:false,reason:'No requested hardware adapter'};
 const info=adapter.info,meta={vendor:info?.vendor,architecture:info?.architecture,device:info?.device,description:info?.description,isFallbackAdapter:info?.isFallbackAdapter??null,features:[...adapter.features],limits:{maxStorageBufferBindingSize:adapter.limits.maxStorageBufferBindingSize,maxComputeWorkgroupsPerDimension:adapter.limits.maxComputeWorkgroupsPerDimension,maxBufferSize:adapter.limits.maxBufferSize}};
 if(meta.isFallbackAdapter!==false)return {supported:false,reason:'Hardware adapter status is absent or fallback; no substitution',adapter:meta};
 if(meta.limits.maxStorageBufferBindingSize<640000||meta.limits.maxBufferSize<640000||meta.limits.maxComputeWorkgroupsPerDimension<313)return {supported:false,reason:'Required fixed batch limits unavailable',adapter:meta};
 window.receiverInitializationEvidence={phase:'request-device',adapter:meta};device=await adapter.requestDevice();meta.deviceLimits={maxStorageBufferBindingSize:device.limits.maxStorageBufferBindingSize,maxComputeWorkgroupsPerDimension:device.limits.maxComputeWorkgroupsPerDimension,maxBufferSize:device.limits.maxBufferSize};window.receiverInitializationEvidence.adapter=meta;
 if(meta.deviceLimits.maxStorageBufferBindingSize<640000||meta.deviceLimits.maxBufferSize<640000||meta.deviceLimits.maxComputeWorkgroupsPerDimension<313)return {supported:false,reason:'Required actual device limits unavailable',adapter:meta};
 device.lost.then(x=>{loss={reason:x.reason,message:x.message};});
 device.addEventListener('uncapturederror',e=>{window.unhandledGPUError=String(e.error?.message??e.error);});
 device.pushErrorScope('validation');window.receiverInitializationEvidence={phase:'shader-compilation',adapter:meta};
 const response=await fetch('receiver.wgsl');if(!response.ok)throw Error('Shader fetch failed');
 const shader=await response.text();window.receiverInitializationEvidence.shader=shader;const module=device.createShaderModule({code:shader}),compilation=await module.getCompilationInfo();
 const messages=Array.from(compilation.messages,m=>({type:m.type,message:m.message,lineNum:m.lineNum,linePos:m.linePos,offset:m.offset,length:m.length}));
 window.receiverInitializationEvidence={phase:'pipeline-creation',adapter:meta,messages,shader};
 if(messages.some(m=>m.type==='error'))return {supported:true,compiled:false,adapter:meta,messages,validation:String((await device.popErrorScope())?.message??'')};
 try{pipeline=await device.createComputePipelineAsync({layout:'auto',compute:{module,entryPoint:'main'}});}catch(e){return {supported:true,compiled:false,adapter:meta,messages,pipelineError:{name:e.name,message:e.message},loss,shader};}const error=await device.popErrorScope();
 return {supported:true,compiled:!error&&!loss&&!window.unhandledGPUError,adapter:meta,messages,validation:error?.message??null,loss,uncaptured:window.unhandledGPUError??null,shader};
};
window.dispatchReceiver=async(bits,timeoutMs)=>{
 if(!device||!pipeline||loss||window.unhandledGPUError)throw Error('GPU unavailable or lost: '+JSON.stringify(loss??window.unhandledGPUError));
 if(bits.length%4||!bits.length)throw Error('Input packing');
 const n=bits.length/4,bytes=n*32;window.lastDispatchEvidence={count:n,groups:Math.ceil(n/64),inputBytes:bits.length*4,outputBytes:bytes,submitted:false};device.pushErrorScope('validation');
 const input=device.createBuffer({size:bits.length*4,usage:GPUBufferUsage.STORAGE|GPUBufferUsage.COPY_DST});
 const output=device.createBuffer({size:bytes,usage:GPUBufferUsage.STORAGE|GPUBufferUsage.COPY_SRC});
 const read=device.createBuffer({size:bytes,usage:GPUBufferUsage.COPY_DST|GPUBufferUsage.MAP_READ});
 device.queue.writeBuffer(input,0,new Uint32Array(bits));
 const group=device.createBindGroup({layout:pipeline.getBindGroupLayout(0),entries:[{binding:0,resource:{buffer:input}},{binding:1,resource:{buffer:output}}]});
 const encoder=device.createCommandEncoder(),pass=encoder.beginComputePass();pass.setPipeline(pipeline);pass.setBindGroup(0,group);pass.dispatchWorkgroups(Math.ceil(n/64));pass.end();encoder.copyBufferToBuffer(output,0,read,0,bytes);device.queue.submit([encoder.finish()]);window.lastDispatchEvidence.submitted=true;
 let timer;
 try{
  await Promise.race([read.mapAsync(GPUMapMode.READ),new Promise((_,reject)=>{timer=setTimeout(()=>{device.destroy();reject(Error('GPU batch timeout'));},timeoutMs);})]);
  const returned=Array.from(new Uint32Array(read.getMappedRange()).slice());read.unmap();
  pendingValidation=device.popErrorScope().then(error=>({validation:error?.message??null})).catch(e=>({validation:String(e.message)}));
  return {bits:returned,count:n,dispatch:window.lastDispatchEvidence};
 }finally{clearTimeout(timer);input.destroy();output.destroy();read.destroy();}
};
window.shutdownReceiver=()=>device?.destroy();window.receiverRunnerReady=true;

window.receiverHealth=()=>({loss,uncaptured:window.unhandledGPUError??null});

window.finishReceiverBatch=async()=>{const result=await pendingValidation;pendingValidation=null;return {...result,loss,uncaptured:window.unhandledGPUError??null};};
