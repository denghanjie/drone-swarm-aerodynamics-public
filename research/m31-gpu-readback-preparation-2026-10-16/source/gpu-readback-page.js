'use strict';
// Static-only preparation. No invocation occurs merely by loading this definition.
(() => {
  const SHADER = String.raw`@group(0) @binding(0)
var<storage, read_write> output: array<u32, 32>;

@compute @workgroup_size(8)
fn main(@builtin(global_invocation_id) gid: vec3<u32>) {
  let i: u32 = gid.x;
  if (i >= 17u) { return; }
  output[4u + i] = ((0x9E3779B9u * (i + 1u)) ^ 0xA5A5A5A5u) + 0x7F4A7C15u;
}
`;
  const BYTE_LENGTH=128, WORD_COUNT=32, WORK_MS=8000, CLEANUP_MS=10000;
  const FILTERS=['out-of-memory','internal','validation'];
  const FAILURE_CODES=new Set(['work-deadline','cleanup-deadline','insecure-context','webgpu-unavailable','adapter-timeout','adapter-unavailable','fallback-adapter-rejected','fallback-status-unavailable','device-timeout','unexpected-device-loss','limits-unavailable','compilation-timeout','compilation-message-cap','shader-compilation-error','pipeline-timeout','pipeline-error-validation','pipeline-error-internal','pipeline-error-other','map-timeout','map-state-mismatch','mapped-byte-length','owned-copy-shape','api-operation-rejected','unmap-rejected','mapped-range-not-detached','mapped-range-observation-failed','storage-destroy-rejected','readback-destroy-rejected','error-scope-nonempty','scope-pop-rejected','device-destroy-rejected','destroy-loss-unobserved','return-conversion-failed','uncaptured-error-observed','evidence-cap']);
  let consumed=false;
  const errorKind=error=>({GPUValidationError:'validation',GPUOutOfMemoryError:'out-of-memory',GPUInternalError:'internal'}[error?.constructor?.name]||'other');
  window.runSyntheticGPUReadback = async () => {
    if(consumed)throw Error('Sole GPU readback invocation already consumed');
    consumed=true;
    const start=performance.now();let sealed=false,stopped=false,device=null,storage=null,readback=null,mappedRange=null,owned=null;
    let intentionalDestroy=false,lossReject=null,lossObserved=false,scopesPending=0;
    const lossSignal=new Promise((_,reject)=>{lossReject=reject;});lossSignal.catch(()=>{});
    const out={version:1,kind:'synthetic-gpu-readback-envelope',fixtureId:'m31-u32-readback-128-v1',
      phaseEvidenceKind:'page-self-report',requiresIndependentPersistenceReview:true,scientificQualified:false,historicalFailureExplained:false,performanceClaim:false,
      layout:{wordBytes:4,wordCount:32,byteLength:128,prefixWords:4,activeWords:17,suffixWords:11,workgroupSize:8,dispatchGroups:3,launchedInvocations:24,endianness:'little'},
      context:{originLabel:location.origin==='http://127.0.0.1:8876'?'page-origin':location.origin==='null'?'opaque-null':'other-origin',isSecureContext:window.isSecureContext,webgpuSupported:!!navigator.gpu},
      status:'failed',values:null,returnedByteLength:0,events:[],failures:[],eventOverflow:false,failureOverflow:false,
      counts:{adapterRequests:0,deviceRequests:0,initializationWrites:0,pipelineCreations:0,dispatchEncodes:0,copyEncodes:0,submissions:0,mapRequests:0,ownedCopies:0,returnConversions:0},
      observation:{adapterAvailable:null,isFallbackAdapter:'unavailable',limitsAdmitted:false,compilationErrors:0,compilationWarnings:0,compilationInfos:0,
        mapStateAtCopy:null,mappedByteLengthBeforeUnmap:null,mappedByteLengthAfterUnmap:null,ownedByteLengthBeforeRelease:null,ownedByteLengthAfterRelease:null,
        ownedIndependent:null,rangeDetached:null,unmapSucceeded:false,storageDestroyed:false,readbackDestroyed:false,
        deviceDestroyAttempted:false,deviceDestroySucceeded:false,lossBeforeDestroySnapshot:'not-observed',deviceLostReason:'not-observed',
        unexpectedDeviceLoss:false,expectedDestroyLossObserved:false,uncapturedErrorKinds:[],uncapturedErrorOverflow:false,
        pendingAdapterRequest:false,pendingDeviceRequest:false,pendingMapRequest:false,pendingWork:false,
        scopes:FILTERS.map(filter=>({filter,state:'unpushed',errorKind:null})),cleanupDeadlineExceeded:false},
      lastWorkStage:'entered',browserElapsedMilliseconds:0};
    function event(stage){if(sealed)return;if(out.events.length>=64){out.eventOverflow=true;return;}
      out.events.push({sequence:out.events.length+1,stage,browserMilliseconds:performance.now()-start});}
    function failure(code){if(sealed)return;if(out.failures.length>=16){out.failureOverflow=true;return;}out.failures.push(FAILURE_CODES.has(code)?code:'api-operation-rejected');}
    function problem(code){const e=new Error(code);e.code=code;return e;}
    function requireStep(ok,code){if(!ok)throw problem(code);}
    function workGuard(){requireStep(!stopped&&performance.now()-start<WORK_MS,'work-deadline');}
    // A timeout does not cancel the underlying promise. Pending means not yet settled.
    function track(factory,key){out.observation[key]=true;let promise;
      try{promise=factory();}catch(error){out.observation[key]=false;throw error;}
      return Promise.resolve(promise).then(value=>{if(!sealed)out.observation[key]=false;return value;},error=>{if(!sealed)out.observation[key]=false;throw error;});}
    async function wait(promise,code,cleanup=false){
      // Observe rejection even if the deadline expires before Promise.race is attached.
      Promise.resolve(promise).catch(()=>{});
      const remain=(cleanup?CLEANUP_MS:WORK_MS)-(performance.now()-start);
      if(remain<=0)throw problem(cleanup?'cleanup-deadline':'work-deadline');
      let timer;try{return await Promise.race([promise,...(cleanup?[]:[lossSignal]),new Promise((_,reject)=>{timer=setTimeout(()=>reject(problem(code)),remain);})]);}
      finally{clearTimeout(timer);}
    }
    const uncaptured=eventObject=>{if(sealed)return;
      if(out.observation.uncapturedErrorKinds.length>=8)out.observation.uncapturedErrorOverflow=true;
      else out.observation.uncapturedErrorKinds.push(errorKind(eventObject.error));event('uncaptured-error');};
    let deviceLossPromise=null;
    event('entered');
    try {
      requireStep(out.context.isSecureContext,'insecure-context');requireStep(out.context.webgpuSupported,'webgpu-unavailable');
      workGuard();out.lastWorkStage='adapter-requested';out.counts.adapterRequests++;event('adapter-requested');
      const adapterPromise=track(()=>navigator.gpu.requestAdapter(),'pendingAdapterRequest');
      const adapter=await wait(adapterPromise,'adapter-timeout');out.observation.adapterAvailable=adapter!==null;
      requireStep(adapter!==null,'adapter-unavailable');event('adapter-available');
      // This API report admits a nonfallback adapter; it does not attest physical hardware.
      try{const fallback=adapter.info?.isFallbackAdapter;out.observation.isFallbackAdapter=typeof fallback==='boolean'?fallback:'unavailable';}catch(_){out.observation.isFallbackAdapter='unavailable';}
      event('adapter-kind-observed');
      requireStep(out.observation.isFallbackAdapter!=='unavailable','fallback-status-unavailable');
      requireStep(out.observation.isFallbackAdapter===false,'fallback-adapter-rejected');
      workGuard();out.lastWorkStage='device-requested';out.counts.deviceRequests++;event('device-requested');
      const devicePromise=track(()=>adapter.requestDevice(),'pendingDeviceRequest').then(value=>{
        // A late device is never used; the future external browser supervisor remains authoritative.
        if(stopped||sealed){try{value.destroy();}catch(_){}}
        return value;
      });
      device=await wait(devicePromise,'device-timeout');event('device-available');
      device.addEventListener('uncapturederror',uncaptured);
      deviceLossPromise=device.lost.then(info=>{if(sealed)return info;
        lossObserved=true;const reason=['destroyed','unknown'].includes(info.reason)?info.reason:'other';out.observation.deviceLostReason=reason;
        if(intentionalDestroy&&reason==='destroyed'){out.observation.expectedDestroyLossObserved=true;event('expected-destroy-loss');}
        else {out.observation.unexpectedDeviceLoss=true;failure('unexpected-device-loss');event('unexpected-device-loss');lossReject(problem('unexpected-device-loss'));}
        return info;
      });
      const limits=device.limits;
      requireStep(limits.maxStorageBufferBindingSize>=BYTE_LENGTH&&limits.maxBufferSize>=BYTE_LENGTH&&limits.maxComputeInvocationsPerWorkgroup>=8&&limits.maxComputeWorkgroupSizeX>=8&&limits.maxComputeWorkgroupsPerDimension>=3,'limits-unavailable');
      out.observation.limitsAdmitted=true;event('limits-admitted');
      for(const filter of FILTERS){workGuard();device.pushErrorScope(filter);out.observation.scopes[scopesPending].state='pushed';scopesPending++;event('scope-pushed');}
      workGuard();out.lastWorkStage='buffers-created';
      storage=device.createBuffer({label:'fixed-u32-output',size:BYTE_LENGTH,usage:GPUBufferUsage.STORAGE|GPUBufferUsage.COPY_SRC|GPUBufferUsage.COPY_DST});
      readback=device.createBuffer({label:'fixed-u32-readback',size:BYTE_LENGTH,usage:GPUBufferUsage.COPY_DST|GPUBufferUsage.MAP_READ});event('buffers-created');
      const initial=new Uint8Array(BYTE_LENGTH),initialView=new DataView(initial.buffer);
      for(let j=0;j<WORD_COUNT;j++)initialView.setUint32(j*4,(0xD15EA5E5^Math.imul(j,0x01010101))>>>0,true);
      device.queue.writeBuffer(storage,0,initial);out.counts.initializationWrites++;event('sentinels-queued');
      workGuard();out.lastWorkStage='shader-created';const module=device.createShaderModule({label:'fixed-u32-arithmetic',code:SHADER});event('shader-created');
      const compilation=await wait(track(()=>module.getCompilationInfo(),'pendingWork'),'compilation-timeout');
      requireStep(compilation.messages.length<=64,'compilation-message-cap');
      for(const message of compilation.messages){if(message.type==='error')out.observation.compilationErrors++;else if(message.type==='warning')out.observation.compilationWarnings++;else out.observation.compilationInfos++;}
      event('compilation-observed');requireStep(out.observation.compilationErrors===0,'shader-compilation-error');
      workGuard();out.lastWorkStage='pipeline-requested';out.counts.pipelineCreations++;event('pipeline-requested');
      const pipeline=await wait(track(()=>device.createComputePipelineAsync({label:'fixed-u32-pipeline',layout:'auto',compute:{module,entryPoint:'main'}}),'pendingWork'),'pipeline-timeout');event('pipeline-created');
      const group=device.createBindGroup({layout:pipeline.getBindGroupLayout(0),entries:[{binding:0,resource:{buffer:storage,offset:0,size:BYTE_LENGTH}}]});
      workGuard();const encoder=device.createCommandEncoder();const pass=encoder.beginComputePass();pass.setPipeline(pipeline);pass.setBindGroup(0,group);
      pass.dispatchWorkgroups(3);out.counts.dispatchEncodes++;pass.end();event('dispatch-encoded');
      encoder.copyBufferToBuffer(storage,0,readback,0,BYTE_LENGTH);out.counts.copyEncodes++;event('readback-copy-encoded');
      workGuard();device.queue.submit([encoder.finish()]);out.counts.submissions++;out.lastWorkStage='submitted';event('submitted');
      workGuard();out.counts.mapRequests++;out.lastWorkStage='map-requested';event('map-requested');
      const mapping=track(()=>readback.mapAsync(GPUMapMode.READ,0,BYTE_LENGTH),'pendingMapRequest');
      await wait(mapping,'map-timeout');out.lastWorkStage='mapped';event('mapped');workGuard();
      out.observation.mapStateAtCopy=['mapped','unmapped','pending'].includes(readback.mapState)?readback.mapState:'other';
      requireStep(readback.mapState==='mapped','map-state-mismatch');mappedRange=readback.getMappedRange(0,BYTE_LENGTH);
      out.observation.mappedByteLengthBeforeUnmap=mappedRange.byteLength;requireStep(mappedRange.byteLength===BYTE_LENGTH,'mapped-byte-length');
      owned=new Uint8Array(BYTE_LENGTH);owned.set(new Uint8Array(mappedRange));out.counts.ownedCopies++;
      out.observation.ownedIndependent=owned.buffer!==mappedRange;out.observation.ownedByteLengthBeforeRelease=owned.byteLength;
      requireStep(out.observation.ownedIndependent&&owned.byteLength===BYTE_LENGTH,'owned-copy-shape');out.lastWorkStage='owned-copy-made';event('owned-copy-made');
    } catch(error) {stopped=true;
      const code=error?.name==='GPUPipelineError'?`pipeline-error-${['validation','internal'].includes(error.reason)?error.reason:'other'}`:error?.code;
      failure(code);event('work-failed');}
    finally {
      stopped=true;event('cleanup-started');
      if(readback){try{readback.unmap();out.observation.unmapSucceeded=true;event('unmap-returned');}
        catch(_){failure('unmap-rejected');}
        if(mappedRange){try{out.observation.mappedByteLengthAfterUnmap=mappedRange.byteLength;out.observation.rangeDetached=mappedRange.byteLength===0;event('mapped-range-after-unmap');
          if(!out.observation.rangeDetached)failure('mapped-range-not-detached');}catch(_){failure('mapped-range-observation-failed');}}}
      if(storage){try{storage.destroy();out.observation.storageDestroyed=true;event('storage-destroy-returned');}catch(_){failure('storage-destroy-rejected');}}
      if(readback){try{readback.destroy();out.observation.readbackDestroyed=true;event('readback-destroy-returned');}catch(_){failure('readback-destroy-rejected');}}
      // Scope results must be observed before deliberate device destruction; a lost device may otherwise yield null.
      while(device&&scopesPending>0){const index=--scopesPending;const scope=out.observation.scopes[index];
        if(performance.now()-start>=CLEANUP_MS){scope.state='unresolved';out.observation.cleanupDeadlineExceeded=true;failure('cleanup-deadline');continue;}
        try {const error=await wait(device.popErrorScope(),'scope-pop-timeout',true);scope.state='popped';scope.errorKind=error?errorKind(error):null;
          if(error)failure('error-scope-nonempty');event('scope-popped');}
        catch(_){scope.state='unresolved';failure('scope-pop-rejected');}}
      if(device){out.observation.lossBeforeDestroySnapshot=lossObserved?out.observation.deviceLostReason:'not-observed';
        intentionalDestroy=true;out.observation.deviceDestroyAttempted=true;event('device-destroy-intent');
        try{device.destroy();out.observation.deviceDestroySucceeded=true;event('device-destroy-returned');}catch(_){failure('device-destroy-rejected');}
        if(deviceLossPromise){try{await wait(deviceLossPromise,'destroy-loss-timeout',true);}catch(_){failure('destroy-loss-unobserved');}}
        device.removeEventListener('uncapturederror',uncaptured);}
      if(performance.now()-start>=CLEANUP_MS){out.observation.cleanupDeadlineExceeded=true;failure('cleanup-deadline');}
      if(owned){out.observation.ownedByteLengthAfterRelease=owned.byteLength;event('owned-copy-after-release');}
      const released=out.observation.unmapSucceeded&&out.observation.storageDestroyed&&out.observation.readbackDestroyed&&out.observation.deviceDestroySucceeded;
      if(owned&&released){try{requireStep(owned.byteLength===BYTE_LENGTH,'owned-copy-shape');out.values=Array.from(owned);out.returnedByteLength=out.values.length;out.counts.returnConversions++;event('owned-values-created');}
        catch(_){failure('return-conversion-failed');out.values=null;out.returnedByteLength=0;}}
      if(out.observation.uncapturedErrorKinds.length||out.observation.uncapturedErrorOverflow)failure('uncaptured-error-observed');
      event('return-envelope-ready');
      if(out.eventOverflow||out.failureOverflow)failure('evidence-cap');
      out.browserElapsedMilliseconds=performance.now()-start;
      if(out.browserElapsedMilliseconds>=CLEANUP_MS&&!out.observation.cleanupDeadlineExceeded){out.observation.cleanupDeadlineExceeded=true;failure('cleanup-deadline');}
      const clean=out.failures.length===0&&!out.eventOverflow&&!out.failureOverflow&&out.values!==null&&out.observation.rangeDetached===true
        &&out.observation.ownedIndependent===true&&out.observation.expectedDestroyLossObserved&&!out.observation.unexpectedDeviceLoss
        &&out.observation.lossBeforeDestroySnapshot==='not-observed'&&!out.observation.cleanupDeadlineExceeded
        &&out.observation.scopes.every(x=>x.state==='popped'&&x.errorKind===null)&&!out.observation.pendingAdapterRequest&&!out.observation.pendingDeviceRequest&&!out.observation.pendingMapRequest&&!out.observation.pendingWork;
      out.status=clean?'candidate-readback':'failed';sealed=true;
    }
    return out;
  };
})();
