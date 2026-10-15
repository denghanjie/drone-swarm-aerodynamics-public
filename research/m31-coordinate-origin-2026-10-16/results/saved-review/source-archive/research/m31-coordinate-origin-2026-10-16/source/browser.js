// Inert until the sole supervised driver invokes this API. No load-time science.
let device,loss=null,uncaptured=null,pendingValidation=null,stage='uninitialized',current=null;
let common={},cell={},pipelines={},controlGroups={},cellGroups={},seenControls=new Set(),seenCells=new Set();
const arms=['A','B','C'],termBytes=8320000,controlBytes=3200,controlOutputBytes=2080,sumBytes=512;
const bindings={};for(const arm of arms){bindings['terms'+arm]=[[0,'constants'],[1,'nodes'],[2,'offsets'],[3,'ids'],[4,'terms']];bindings['controls'+arm]=[[0,'constants'],[5,'controls'],[6,'controlOutputs']];}bindings.reduceMain=[[3,'ids'],[4,'terms'],[7,'sums']];
const costs={pipelineCreations:0,bufferCreations:0,allocatedBytes:0,uploadedBytes:0,clearedBytes:0,readbackBytes:0,dispatches:0,activeOutputSlots:0,launchedInvocations:0,peakLiveBufferBytes:0,liveBufferBytes:0};
const decode64=s=>Uint8Array.from(atob(s),x=>x.charCodeAt(0));
function encode64(bytes){let chunks=[];for(let i=0;i<bytes.length;i+=32768)chunks.push(String.fromCharCode(...bytes.subarray(i,i+32768)));return btoa(chunks.join(''));}
function create(size,usage){const b=device.createBuffer({size,usage});costs.bufferCreations++;costs.allocatedBytes+=size;costs.liveBufferBytes+=size;costs.peakLiveBufferBytes=Math.max(costs.peakLiveBufferBytes,costs.liveBufferBytes);return b;}
function destroy(b){if(!b)return;costs.liveBufferBytes-=b.size;b.destroy();}
function upload(b,base64){const bytes=decode64(base64);if(bytes.length!==b.size)throw Error('Input byte shape');device.queue.writeBuffer(b,0,bytes);costs.uploadedBytes+=bytes.length;}
function healthy(){if(loss||uncaptured||pendingValidation)throw Error('GPU health or pending API error scope');}
function group(entry,buffers){return device.createBindGroup({layout:pipelines[entry].getBindGroupLayout(0),entries:bindings[entry].map(([binding,key])=>({binding,resource:{buffer:buffers[key]}}))});}
window.coordinateHealth=()=>({loss,uncaptured,stage,current,seenControls:[...seenControls],seenCells:[...seenCells],costs:{...costs}});
window.initializeCoordinate=async()=>{
 window.coordinateInitializationEvidence={phase:'request-adapter'};
 if(!navigator.gpu)return {supported:false,reason:'navigator.gpu unavailable'};
 const adapter=await navigator.gpu.requestAdapter({powerPreference:'high-performance'});if(!adapter)return {supported:false,reason:'No requested adapter'};
 const info=adapter.info,fields=x=>({maxStorageBufferBindingSize:x.maxStorageBufferBindingSize,maxBufferSize:x.maxBufferSize,maxComputeWorkgroupsPerDimension:x.maxComputeWorkgroupsPerDimension,maxStorageBuffersPerShaderStage:x.maxStorageBuffersPerShaderStage});
 const meta={vendor:info?.vendor,architecture:info?.architecture,device:info?.device,description:info?.description,isFallbackAdapter:info?.isFallbackAdapter??null,features:[...adapter.features],limits:fields(adapter.limits)};
 if(meta.isFallbackAdapter!==false)return {supported:false,reason:'Nonfallback hardware not established',adapter:meta};
 const adequate=x=>x.maxStorageBufferBindingSize>=termBytes&&x.maxBufferSize>=termBytes&&x.maxComputeWorkgroupsPerDimension>=1250&&x.maxStorageBuffersPerShaderStage>=5;
 if(!adequate(meta.limits))return {supported:false,reason:'Required adapter limits unavailable',adapter:meta};
 window.coordinateInitializationEvidence={phase:'request-device',adapter:meta};device=await adapter.requestDevice();meta.deviceLimits=fields(device.limits);
 if(!adequate(meta.deviceLimits))return {supported:false,reason:'Required actual device limits unavailable',adapter:meta};
 device.lost.then(x=>{loss={reason:x.reason,message:x.message};});device.addEventListener('uncapturederror',e=>{uncaptured=String(e.error?.message??e.error);});
 device.pushErrorScope('validation');window.coordinateInitializationEvidence={phase:'shader-compilation',adapter:meta};
 const response=await fetch('coordinate.wgsl');if(!response.ok)throw Error('Shader fetch failed');const shader=await response.text(),module=device.createShaderModule({code:shader});
 const compilation=await module.getCompilationInfo(),messages=Array.from(compilation.messages,m=>({type:m.type,message:m.message,lineNum:m.lineNum,linePos:m.linePos,offset:m.offset,length:m.length}));
 window.coordinateInitializationEvidence={phase:'pipeline-creation',adapter:meta,shader,messages};
 if(messages.some(x=>x.type==='error'))return {supported:true,compiled:false,adapter:meta,shader,messages,validation:String((await device.popErrorScope())?.message??'')};
 try{for(const entryPoint of Object.keys(bindings)){window.coordinateInitializationEvidence.entryPoint=entryPoint;costs.pipelineCreations++;pipelines[entryPoint]=await device.createComputePipelineAsync({layout:'auto',compute:{module,entryPoint}});}}
 catch(e){return {supported:true,compiled:false,adapter:meta,shader,messages,pipelineError:{name:e.name,message:e.message,entryPoint:window.coordinateInitializationEvidence.entryPoint},loss,uncaptured};}
 const error=await device.popErrorScope();stage='initialized';return {supported:true,compiled:!error&&!loss&&!uncaptured,adapter:meta,shader,messages,validation:error?.message??null,loss,uncaptured,costs:{...costs}};
};
window.prepareCoordinateControls=async input=>{
 healthy();if(stage!=='initialized')throw Error('Control preparation state');device.pushErrorScope('validation');
 common.constants=create(64,GPUBufferUsage.STORAGE|GPUBufferUsage.COPY_DST);upload(common.constants,input.constants);
 common.controls=create(controlBytes,GPUBufferUsage.STORAGE|GPUBufferUsage.COPY_DST);upload(common.controls,input.controls);
 common.controlOutputs=create(controlOutputBytes,GPUBufferUsage.STORAGE|GPUBufferUsage.COPY_SRC|GPUBufferUsage.COPY_DST);
 for(const arm of arms)controlGroups[arm]=group('controls'+arm,common);
 const e=await device.popErrorScope();stage='controls-ready';return {validation:e?.message??null,loss,uncaptured,sizes:{constants:64,controls:controlBytes,controlOutputs:controlOutputBytes},costs:{...costs}};
};
window.prepareCoordinateCell=async input=>{
 healthy();if(!['controls-complete','idle'].includes(stage)||seenControls.size!==3||!arms.includes(input.arm)||![0,1].includes(input.origin))throw Error('Cell preparation state');
 const key='o'+input.origin+'-'+input.arm;if(seenCells.has(key))throw Error('Duplicate cell');seenCells.add(key);current={key,arm:input.arm,origin:input.origin};device.pushErrorScope('validation');
 const sizes={nodes:input.arm==='C'?240000:160000,offsets:256,ids:16,terms:termBytes,sums:sumBytes};
 for(const [name,size]of Object.entries(sizes)){const output=['terms','sums'].includes(name);cell[name]=create(size,GPUBufferUsage.STORAGE|(output?GPUBufferUsage.COPY_SRC:GPUBufferUsage.COPY_DST));if(!output)upload(cell[name],input[name]);}
 const all={...common,...cell};cellGroups.terms=group('terms'+input.arm,all);cellGroups.reduce=group('reduceMain',all);
 const e=await device.popErrorScope();stage='cell-ready';return {key,sizes,validation:e?.message??null,loss,uncaptured,costs:{...costs}};
};
window.dispatchCoordinate=async(kind,arm,timeoutMs)=>{
 healthy();let entry,bind,output,count,groups,bytes;
 if(kind==='controls'){
  if(stage!=='controls-ready'||!arms.includes(arm)||seenControls.has(arm))throw Error('Control dispatch state');seenControls.add(arm);entry='controls'+arm;bind=controlGroups[arm];output=common.controlOutputs;count=20;groups=1;bytes=controlOutputBytes;
 }else if(kind==='terms'){
  if(stage!=='cell-ready'||arm!==current?.arm)throw Error('Term dispatch state');entry='terms'+arm;bind=cellGroups.terms;output=cell.terms;count=80000;groups=1250;bytes=termBytes;
 }else if(kind==='reduce'){
  if(stage!=='terms-read'||arm!==current?.arm)throw Error('Reduction dispatch state');entry='reduceMain';bind=cellGroups.reduce;output=cell.sums;count=16;groups=1;bytes=sumBytes;
 }else throw Error('Unknown dispatch');
 window.lastCoordinateDispatch={kind,arm,cell:kind==='controls'?null:current.key,count,groups,outputBytes:bytes,submitted:false,materializedTermsPreserved:kind==='reduce'};
 costs.dispatches++;costs.activeOutputSlots+=count;costs.launchedInvocations+=64*groups;
 device.pushErrorScope('validation');const read=create(bytes,GPUBufferUsage.COPY_DST|GPUBufferUsage.MAP_READ);
 const encoder=device.createCommandEncoder();if(kind==='controls'){encoder.clearBuffer(output,0,bytes);costs.clearedBytes+=bytes;}const pass=encoder.beginComputePass();pass.setPipeline(pipelines[entry]);pass.setBindGroup(0,bind);pass.dispatchWorkgroups(groups);pass.end();encoder.copyBufferToBuffer(output,0,read,0,bytes);device.queue.submit([encoder.finish()]);window.lastCoordinateDispatch.submitted=true;
 let timer;try{
  await Promise.race([read.mapAsync(GPUMapMode.READ),new Promise((_,reject)=>{timer=setTimeout(()=>{device.destroy();reject(Error('Coordinate dispatch timeout'));},timeoutMs);})]);
  const returned=new Uint8Array(read.getMappedRange()).slice();read.unmap();costs.readbackBytes+=returned.length;
  stage=kind==='controls'?'control-read':kind==='terms'?'terms-read':'sums-read';
  pendingValidation=device.popErrorScope().then(e=>({validation:e?.message??null})).catch(e=>({validation:String(e.message)}));
  return {base64:encode64(returned),bytes:returned.length,dispatch:window.lastCoordinateDispatch,costs:{...costs}};
 }finally{clearTimeout(timer);destroy(read);}
};
window.finishCoordinateBatch=async()=>{
 if(!pendingValidation)throw Error('No pending batch');const r=await pendingValidation;pendingValidation=null;
 if(stage==='control-read'){
  if(seenControls.size===3){destroy(common.controls);destroy(common.controlOutputs);delete common.controls;delete common.controlOutputs;controlGroups={};stage='controls-complete';}else stage='controls-ready';
 }
 return {...r,loss,uncaptured,stage,costs:{...costs}};
};
window.finishCoordinateCell=()=>{
 healthy();if(!['terms-read','sums-read'].includes(stage))throw Error('Cell finish state');const result={...current,reductionDispatched:stage==='sums-read'};
 for(const b of Object.values(cell))destroy(b);cell={};cellGroups={};current=null;stage='idle';return {...result,costs:{...costs}};
};
window.shutdownCoordinate=()=>{for(const b of Object.values(cell))destroy(b);for(const b of Object.values(common))destroy(b);cell={};common={};device?.destroy();};
window.coordinateRunnerReady=true;
