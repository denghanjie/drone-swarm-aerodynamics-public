// Source preparation only. No GPU operation occurs on page load.
// The sole frozen driver owns every batch, sink URL and resource reservation.
let device, loss=null, uncaptured=null, stage='uninitialized', current=null;
const pipelines={}, seen=new Set(), bufferLedger=[], RAW_GPU_CAP=218103808;
const costs={pipelineCreations:0,bufferCreations:0,allocatedBytes:0,uploadedBytes:0,
 readbackBytes:0,dispatches:0,activeInvocations:0,launchedInvocations:0,
 liveBufferBytes:0,peakLiveBufferBytes:0};
const entries=['mainBody','controlPairs','controlRoots'];
const decode=s=>Uint8Array.from(atob(s),c=>c.charCodeAt(0));
function check(ok,message){if(!ok)throw Error(message);}
function health(){return {stage,current,loss,uncaptured,seen:[...seen],costs:{...costs}};}
function limits(x){return {maxStorageBufferBindingSize:x.maxStorageBufferBindingSize,
 maxBufferSize:x.maxBufferSize,maxComputeWorkgroupsPerDimension:x.maxComputeWorkgroupsPerDimension,
 maxStorageBuffersPerShaderStage:x.maxStorageBuffersPerShaderStage,
 maxComputeWorkgroupSizeX:x.maxComputeWorkgroupSizeX,maxComputeInvocationsPerWorkgroup:x.maxComputeInvocationsPerWorkgroup};}
function adequate(x){return x.maxStorageBufferBindingSize>=100000000&&x.maxBufferSize>=100000000&&
 x.maxComputeWorkgroupsPerDimension>=79&&x.maxStorageBuffersPerShaderStage>=6&&
 x.maxComputeWorkgroupSizeX>=64&&x.maxComputeInvocationsPerWorkgroup>=64;}
function create(label,size,usage){
 check(Number.isSafeInteger(size)&&size>0&&size%4===0,'Invalid buffer shape');
 check(size<=device.limits.maxBufferSize&&costs.liveBufferBytes+size<=RAW_GPU_CAP,'Raw GPU allocation cap');
 const buffer=device.createBuffer({label,size,usage});
 const record={id:bufferLedger.length,label,size,createdAtBatch:current?.key??null,destroyed:false};
 bufferLedger.push(record);costs.bufferCreations++;costs.allocatedBytes+=size;costs.liveBufferBytes+=size;
 costs.peakLiveBufferBytes=Math.max(costs.peakLiveBufferBytes,costs.liveBufferBytes);
 return {buffer,record};
}
function destroy(item){if(!item||item.record.destroyed)return;item.buffer.destroy();item.record.destroyed=true;costs.liveBufferBytes-=item.record.size;}
function expectedPlan(input){
 check(entries.includes(input.entry)&&typeof input.key==='string'&&!seen.has(input.key),'Unknown or duplicate batch');
 check(Number.isInteger(input.count)&&Number.isInteger(input.groups)&&input.groups===Math.ceil(input.count/64),'Invocation coverage');
 if(input.entry==='mainBody'){
  check([50,500,5000].includes(input.count),'Unreserved main shape');const n=input.count;
  return {inputs:[[0,'constants',128],[1,'nodes',32*n],[2,'offsets',64*n],[3,'motors',16*n]],outputs:[[4,'policy',4*n*n],[5,'output',256*n]]};
 }
 const count=input.entry==='controlPairs'?15:146;
 check(input.count===count,'Unreserved control shape');
 return {inputs:[[0,'constants',128],[6,'controls',256*count]],outputs:[[7,'output',256*count]]};
}
window.bodyHealth=health;
window.initializeBody=async()=>{
 check(stage==='uninitialized','Duplicate initialization');stage='request-adapter';
 window.bodyInitializationEvidence={stage};
 if(!navigator.gpu)return {supported:false,reason:'navigator.gpu unavailable'};
 const adapter=await navigator.gpu.requestAdapter({powerPreference:'high-performance'});
 if(!adapter)return {supported:false,reason:'Requested adapter unavailable'};
 const i=adapter.info,meta={vendor:i?.vendor,architecture:i?.architecture,device:i?.device,
  description:i?.description,isFallbackAdapter:i?.isFallbackAdapter??null,
  features:[...adapter.features],limits:limits(adapter.limits)};
 window.bodyInitializationEvidence={stage:'request-device',adapter:meta};
 if(meta.isFallbackAdapter!==false||!adequate(meta.limits))return {supported:false,reason:'Hardware/adapter admission failed',adapter:meta};
 device=await adapter.requestDevice();meta.deviceLimits=limits(device.limits);
 if(!adequate(meta.deviceLimits))return {supported:false,reason:'Actual default device limits inadequate',adapter:meta};
 device.lost.then(v=>{loss={reason:v.reason,message:v.message};});
 device.addEventListener('uncapturederror',e=>{uncaptured=String(e.error?.message??e.error);});
 device.pushErrorScope('validation');stage='compiling';
 const response=await fetch('body.wgsl');check(response.ok,'Shader fetch failed');
 const shader=await response.text(),module=device.createShaderModule({code:shader});
 const info=await module.getCompilationInfo(),messages=[...info.messages].map(m=>({type:m.type,message:m.message,lineNum:m.lineNum,linePos:m.linePos,offset:m.offset,length:m.length}));
 window.bodyInitializationEvidence={stage,adapter:meta,shader,messages};
 let pipelineError=null;
 if(!messages.some(m=>m.type==='error')){
  try{for(const entryPoint of entries){window.bodyInitializationEvidence.entryPoint=entryPoint;costs.pipelineCreations++;pipelines[entryPoint]=await device.createComputePipelineAsync({layout:'auto',compute:{module,entryPoint}});}}
  catch(e){pipelineError={name:e.name,message:e.message,entryPoint:window.bodyInitializationEvidence.entryPoint};}
 }
 const validation=(await device.popErrorScope())?.message??null;
 const compiled=!messages.some(m=>m.type==='error')&&!pipelineError&&!validation&&!loss&&!uncaptured;
 stage=compiled?'ready':'failed-initialization';
 return {supported:true,compiled,adapter:meta,shader,messages,pipelineError,validation,...health()};
};
window.runBodyBatch=async input=>{
 check(stage==='ready'&&!loss&&!uncaptured,'Device not ready');
 const plan=expectedPlan(input);seen.add(input.key);current={key:input.key,entry:input.entry,count:input.count,groups:input.groups};stage='preparing';
 const items=[],reads=[],dispatch={...current,submitted:false,readbacks:[],completed:false};
 window.lastBodyDispatch=dispatch;const before={...costs};let timer,scopeOpen=false,scopePromise=null,validation=null,error=null,active=true;
 const aborter=new AbortController(),cleanupErrors=[];
 const ensureActive=()=>check(active,'Terminal batch continuation rejected');
 const takeScope=()=>{if(!scopePromise&&scopeOpen){scopeOpen=false;scopePromise=device.popErrorScope();}return scopePromise;};
 try{
  check(input.inputs.length===plan.inputs.length&&input.outputs.length===plan.outputs.length,'Batch binding coverage');
  device.pushErrorScope('validation');scopeOpen=true;const bindings=[];
  for(let k=0;k<plan.inputs.length;k++){
   const [binding,name,size]=plan.inputs[k],given=input.inputs[k];
   check(given.binding===binding&&given.name===name,'Input binding identity');const bytes=decode(given.base64);check(bytes.length===size,'Input byte length');
   if(name==='constants'){const view=new DataView(bytes.buffer,bytes.byteOffset,bytes.byteLength);check(view.getUint32(80,true)===input.count,'Constant dimension identity');}
   const item=create(input.key+':'+name,size,GPUBufferUsage.STORAGE|GPUBufferUsage.COPY_DST);items.push(item);
   device.queue.writeBuffer(item.buffer,0,bytes);costs.uploadedBytes+=size;bindings.push({binding,resource:{buffer:item.buffer}});
  }
  for(let k=0;k<plan.outputs.length;k++){
   const [binding,name,size]=plan.outputs[k],given=input.outputs[k];
   check(given.binding===binding&&given.name===name&&given.size===size,'Output binding identity');
   const sink=new URL(given.sinkURL);check(sink.protocol==='http:'&&sink.hostname==='127.0.0.1'&&sink.pathname.startsWith('/evidence/'),'Local evidence sink only');
   const item=create(input.key+':'+name,size,GPUBufferUsage.STORAGE|GPUBufferUsage.COPY_SRC);items.push(item);
   const read=create(input.key+':'+name+':readback',size,GPUBufferUsage.COPY_DST|GPUBufferUsage.MAP_READ);reads.push(read);
   bindings.push({binding,resource:{buffer:item.buffer}});dispatch.readbacks.push({name,bytes:size,persisted:false});
  }
  const bind=device.createBindGroup({layout:pipelines[input.entry].getBindGroupLayout(0),entries:bindings});
  const encoder=device.createCommandEncoder(),pass=encoder.beginComputePass();
  pass.setPipeline(pipelines[input.entry]);pass.setBindGroup(0,bind);pass.dispatchWorkgroups(input.groups);pass.end();
  for(let k=0;k<reads.length;k++)encoder.copyBufferToBuffer(items[plan.inputs.length+k].buffer,0,reads[k].buffer,0,reads[k].record.size);
  costs.dispatches++;costs.activeInvocations+=input.count;costs.launchedInvocations+=64*input.groups;
  device.queue.submit([encoder.finish()]);dispatch.submitted=true;stage='submitted';
  const work=(async()=>{
   await Promise.all(reads.map(x=>x.buffer.mapAsync(GPUMapMode.READ)));ensureActive();stage='mapped';
   for(let k=0;k<reads.length;k++){
    ensureActive();const bytes=new Uint8Array(reads[k].buffer.getMappedRange());
    const result=await fetch(input.outputs[k].sinkURL,{method:'POST',headers:{'Content-Type':'application/octet-stream'},body:bytes,signal:aborter.signal});
    ensureActive();check(result.ok,'Evidence sink rejected readback');const receipt=await result.json();ensureActive();
    check(receipt.bytes===bytes.length&&receipt.complete===true,'Evidence sink byte completion');
    costs.readbackBytes+=bytes.length;dispatch.readbacks[k]={...dispatch.readbacks[k],persisted:true,sha256:receipt.sha256};reads[k].buffer.unmap();
   }
   const scopeResult=await takeScope();ensureActive();validation=scopeResult?.message??null;
   check(!validation&&!loss&&!uncaptured,'GPU validation/loss/uncaptured error');
  })();
  check(input.timeoutMs===30000,'Frozen batch deadline');
  await Promise.race([work,new Promise((_,reject)=>{timer=setTimeout(()=>{active=false;aborter.abort();device.destroy();reject(Error('Body batch deadline'));},input.timeoutMs);})]);
  ensureActive();dispatch.completed=true;
 }catch(e){error={name:e.name,message:String(e.message)};}
 finally{
  active=false;aborter.abort();clearTimeout(timer);
  for(const read of reads){try{if(read.buffer.mapState==='mapped')read.buffer.unmap();}catch(e){cleanupErrors.push('unmap: '+String(e.message));}try{destroy(read);}catch(e){cleanupErrors.push('destroy readback: '+String(e.message));}}
  for(const item of items){try{destroy(item);}catch(e){cleanupErrors.push('destroy storage: '+String(e.message));}}
  if(scopeOpen||scopePromise){let scopeTimer;try{const e=await Promise.race([takeScope(),new Promise((_,reject)=>{scopeTimer=setTimeout(()=>reject(Error('Cleanup error-scope deadline')),1000);})]);if(validation===null)validation=e?.message??null;}catch(e){cleanupErrors.push(String(e.message));}finally{clearTimeout(scopeTimer);}}
  if(cleanupErrors.length&&!error)error={name:'CleanupError',message:'Batch cleanup failed'};
  stage=error?'failed-batch':'ready';current=null;
 }
 // This snapshot is AFTER all batch buffers/readbacks have been released.
 // The independent reviewer must model this exact lifecycle, not a stale one.
 return {dispatch:JSON.parse(JSON.stringify(dispatch)),error,validation,cleanupErrors,allocated:bufferLedger.filter(x=>x.createdAtBatch===input.key).map(x=>({...x})),before,after:{...costs},health:health()};
};
window.shutdownBody=()=>{check(costs.liveBufferBytes===0,'Unreleased batch buffers');device?.destroy();stage='shutdown';return {deviceDestroyed:Boolean(device),costs:{...costs}};};
window.bodyRunnerReady=true;
