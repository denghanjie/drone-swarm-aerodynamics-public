'use strict';
// Pure validation only. No I/O, browser access, reference-byte generation, or hashing.
const FIXTURE_ID='m31-u32-readback-128-v1';
const LAYOUT=Object.freeze({wordBytes:4,wordCount:32,byteLength:128,prefixWords:4,activeWords:17,suffixWords:11,workgroupSize:8,dispatchGroups:3,launchedInvocations:24,endianness:'little'});
const FILTERS=['out-of-memory','internal','validation'];
const ERROR_KINDS=['validation','out-of-memory','internal','other'];
const LOSS_KINDS=['not-observed','destroyed','unknown','other'];
const FAILURE_CODES=['work-deadline','cleanup-deadline','insecure-context','webgpu-unavailable','adapter-timeout','adapter-unavailable','fallback-adapter-rejected','fallback-status-unavailable','device-timeout','unexpected-device-loss','limits-unavailable','compilation-timeout','compilation-message-cap','shader-compilation-error','pipeline-timeout','pipeline-error-validation','pipeline-error-internal','pipeline-error-other','map-timeout','map-state-mismatch','mapped-byte-length','owned-copy-shape','api-operation-rejected','unmap-rejected','mapped-range-not-detached','mapped-range-observation-failed','storage-destroy-rejected','readback-destroy-rejected','error-scope-nonempty','scope-pop-rejected','device-destroy-rejected','destroy-loss-unobserved','return-conversion-failed','uncaptured-error-observed','evidence-cap'];
const SUCCESS_STAGES=['entered','adapter-requested','adapter-available','adapter-kind-observed','device-requested','device-available','limits-admitted','scope-pushed','scope-pushed','scope-pushed','buffers-created','sentinels-queued','shader-created','compilation-observed','pipeline-requested','pipeline-created','dispatch-encoded','readback-copy-encoded','submitted','map-requested','mapped','owned-copy-made','cleanup-started','unmap-returned','mapped-range-after-unmap','storage-destroy-returned','readback-destroy-returned','scope-popped','scope-popped','scope-popped','device-destroy-intent','device-destroy-returned','expected-destroy-loss','owned-copy-after-release','owned-values-created','return-envelope-ready'];
const EXTRA_STAGES=['uncaptured-error','unexpected-device-loss','work-failed'];
const LAST_STAGES=['entered','adapter-requested','device-requested','buffers-created','shader-created','pipeline-requested','submitted','map-requested','mapped','owned-copy-made'];
const COUNTS=['adapterRequests','deviceRequests','initializationWrites','pipelineCreations','dispatchEncodes','copyEncodes','submissions','mapRequests','ownedCopies','returnConversions'];
const OBS_KEYS=['adapterAvailable','isFallbackAdapter','limitsAdmitted','compilationErrors','compilationWarnings','compilationInfos','mapStateAtCopy','mappedByteLengthBeforeUnmap','mappedByteLengthAfterUnmap','ownedByteLengthBeforeRelease','ownedByteLengthAfterRelease','ownedIndependent','rangeDetached','unmapSucceeded','storageDestroyed','readbackDestroyed','deviceDestroyAttempted','deviceDestroySucceeded','lossBeforeDestroySnapshot','deviceLostReason','unexpectedDeviceLoss','expectedDestroyLossObserved','uncapturedErrorKinds','uncapturedErrorOverflow','pendingAdapterRequest','pendingDeviceRequest','pendingMapRequest','pendingWork','scopes','cleanupDeadlineExceeded'];
function demand(ok,code){if(!ok)throw new Error(code);}
function record(value,keys,label){demand(value!==null&&typeof value==='object'&&!Array.isArray(value),label+':object');const proto=Object.getPrototypeOf(value);demand(proto===Object.prototype||proto===null,label+':prototype');const own=Reflect.ownKeys(value);demand(own.length===keys.length&&own.every(key=>typeof key==='string'&&keys.includes(key)),label+':keys');for(const key of keys){const d=Object.getOwnPropertyDescriptor(value,key);demand(d&&Object.hasOwn(d,'value')&&d.enumerable,label+':data-properties');}}
function array(value,max,label){demand(Array.isArray(value)&&Object.getPrototypeOf(value)===Array.prototype,label+':array');const ld=Object.getOwnPropertyDescriptor(value,'length');demand(ld&&Object.hasOwn(ld,'value')&&Number.isSafeInteger(ld.value)&&ld.value>=0&&ld.value<=max,label+':length');const n=ld.value;demand(Reflect.ownKeys(value).length===n+1,label+':dense-keys');for(let i=0;i<n;i++){const d=Object.getOwnPropertyDescriptor(value,String(i));demand(d&&Object.hasOwn(d,'value')&&d.enumerable,label+':dense-data');}return n;}
function integer(value,max,label){demand(Number.isSafeInteger(value)&&!Object.is(value,-0)&&value>=0&&value<=max,label+':integer');}
function number(value,max,label){demand(typeof value==='number'&&Number.isFinite(value)&&!Object.is(value,-0)&&value>=0&&value<=max,label+':number');}
function boolean(value,label){demand(typeof value==='boolean',label+':boolean');}
function oneOf(value,choices,label){demand(choices.includes(value),label+':enum');}
function validateEnvelope(input){
  try{
    const v=input;
    record(v,['version','kind','fixtureId','phaseEvidenceKind','requiresIndependentPersistenceReview','scientificQualified','historicalFailureExplained','performanceClaim','layout','context','status','values','returnedByteLength','events','failures','eventOverflow','failureOverflow','counts','observation','lastWorkStage','browserElapsedMilliseconds'],'envelope');
    demand(v.version===1&&v.kind==='synthetic-gpu-readback-envelope'&&v.fixtureId===FIXTURE_ID,'identity');
    demand(v.phaseEvidenceKind==='page-self-report'&&v.requiresIndependentPersistenceReview===true&&v.scientificQualified===false&&v.historicalFailureExplained===false&&v.performanceClaim===false,'claim-boundary');
    record(v.layout,Object.keys(LAYOUT),'layout');for(const key of Object.keys(LAYOUT))demand(v.layout[key]===LAYOUT[key],'layout:'+key);
    record(v.context,['originLabel','isSecureContext','webgpuSupported'],'context');oneOf(v.context.originLabel,['page-origin','opaque-null','other-origin'],'origin');boolean(v.context.isSecureContext,'secure');boolean(v.context.webgpuSupported,'webgpu');
    oneOf(v.status,['candidate-readback','failed'],'status');boolean(v.eventOverflow,'eventOverflow');boolean(v.failureOverflow,'failureOverflow');
    integer(v.returnedByteLength,128,'returnedByteLength');
    if(v.values!==null){demand(array(v.values,128,'values')===128,'values:exact-length');for(const byte of v.values)integer(byte,255,'byte');demand(v.returnedByteLength===128,'returned-byte-count');}
    else demand(v.returnedByteLength===0,'null-byte-count');
    array(v.failures,16,'failures');for(const code of v.failures)oneOf(code,FAILURE_CODES,'failure');
    record(v.counts,COUNTS,'counts');for(const key of COUNTS)integer(v.counts[key],1,'count:'+key);
    for(let i=1;i<COUNTS.length;i++)demand(v.counts[COUNTS[i]]<=v.counts[COUNTS[i-1]],'count-order:'+COUNTS[i]);
    demand(v.counts.returnConversions===(v.values===null?0:1),'conversion-count');
    const o=v.observation;record(o,OBS_KEYS,'observation');oneOf(o.adapterAvailable,[null,true,false],'adapterAvailable');oneOf(o.isFallbackAdapter,[true,false,'unavailable'],'isFallbackAdapter');
    for(const key of ['limitsAdmitted','unmapSucceeded','storageDestroyed','readbackDestroyed','deviceDestroyAttempted','deviceDestroySucceeded','unexpectedDeviceLoss','expectedDestroyLossObserved','uncapturedErrorOverflow','pendingAdapterRequest','pendingDeviceRequest','pendingMapRequest','pendingWork','cleanupDeadlineExceeded'])boolean(o[key],key);
    for(const key of ['compilationErrors','compilationWarnings','compilationInfos'])integer(o[key],64,key);demand(o.compilationErrors+o.compilationWarnings+o.compilationInfos<=64,'compilation-total');
    oneOf(o.mapStateAtCopy,[null,'mapped','unmapped','pending','other'],'mapStateAtCopy');
    for(const key of ['mappedByteLengthBeforeUnmap','mappedByteLengthAfterUnmap','ownedByteLengthBeforeRelease','ownedByteLengthAfterRelease'])if(o[key]!==null)integer(o[key],4096,key);
    for(const key of ['ownedIndependent','rangeDetached'])oneOf(o[key],[null,true,false],key);
    for(const key of ['lossBeforeDestroySnapshot','deviceLostReason'])oneOf(o[key],LOSS_KINDS,key);
    array(o.uncapturedErrorKinds,8,'uncapturedErrorKinds');for(const kind of o.uncapturedErrorKinds)oneOf(kind,ERROR_KINDS,'uncaptured-kind');
    demand(array(o.scopes,3,'scopes')===3,'scopes:length');for(let i=0;i<3;i++){const scope=o.scopes[i];record(scope,['filter','state','errorKind'],'scope');demand(scope.filter===FILTERS[i],'scope:filter-order');oneOf(scope.state,['unpushed','pushed','popped','unresolved'],'scope:state');oneOf(scope.errorKind,[null,...ERROR_KINDS],'scope:error');if(scope.state!=='popped')demand(scope.errorKind===null,'scope:error-without-pop');}
    oneOf(v.lastWorkStage,LAST_STAGES,'lastWorkStage');number(v.browserElapsedMilliseconds,60000,'elapsed');
    const n=array(v.events,64,'events');demand(n>0,'events:empty');let previous=0,cursor=0;const stages=[];
    for(let i=0;i<n;i++){const e=v.events[i];record(e,['sequence','stage','browserMilliseconds'],'event');demand(e.sequence===i+1,'event:sequence');oneOf(e.stage,[...SUCCESS_STAGES,...EXTRA_STAGES],'event:stage');number(e.browserMilliseconds,60000,'event:time');demand(e.browserMilliseconds>=previous&&e.browserMilliseconds<=v.browserElapsedMilliseconds,'event:time-order');previous=e.browserMilliseconds;stages.push(e.stage);
      if(!EXTRA_STAGES.includes(e.stage)){const index=SUCCESS_STAGES.indexOf(e.stage,cursor);demand(index!==-1,'event:lifecycle-order');cursor=index+1;}}
    demand(stages[0]==='entered','events:entered-first');if(!v.eventOverflow)demand(stages.at(-1)==='return-envelope-ready','events:return-last');
    if(v.eventOverflow)demand(n===64,'overflow:event-cap');if(v.failureOverflow)demand(v.failures.length===16,'overflow:failure-cap');if(o.uncapturedErrorOverflow)demand(o.uncapturedErrorKinds.length===8,'overflow:uncaptured-cap');
    const has=stage=>stages.includes(stage),count=stage=>stages.filter(x=>x===stage).length;
    if(!v.eventOverflow){
      demand(count('scope-pushed')===o.scopes.filter(s=>s.state!=='unpushed').length,'scope:push-count');demand(count('scope-popped')===o.scopes.filter(s=>s.state==='popped').length,'scope:pop-count');
      for(const [key,stage] of [['adapterRequests','adapter-requested'],['deviceRequests','device-requested'],['initializationWrites','sentinels-queued'],['pipelineCreations','pipeline-requested'],['dispatchEncodes','dispatch-encoded'],['copyEncodes','readback-copy-encoded'],['submissions','submitted'],['mapRequests','map-requested'],['ownedCopies','owned-copy-made'],['returnConversions','owned-values-created']])demand(v.counts[key]===count(stage),'event:count:'+key);
      for(const [key,stage] of [['limitsAdmitted','limits-admitted'],['unmapSucceeded','unmap-returned'],['storageDestroyed','storage-destroy-returned'],['readbackDestroyed','readback-destroy-returned'],['deviceDestroyAttempted','device-destroy-intent'],['deviceDestroySucceeded','device-destroy-returned'],['expectedDestroyLossObserved','expected-destroy-loss'],['unexpectedDeviceLoss','unexpected-device-loss']])demand(o[key]===has(stage),'event:observation:'+key);
      demand(count('work-failed')<=1,'event:work-failed-count');demand(has('cleanup-started'),'cleanup:event');}
    if(v.counts.deviceRequests)demand(o.adapterAvailable===true&&o.isFallbackAdapter===false,'device:nonfallback-admission');
    if(o.isFallbackAdapter!==false)demand(v.counts.deviceRequests===0,'device:fallback-rejected');
    if(v.counts.initializationWrites)demand(o.limitsAdmitted,'initialization:limits');
    if(o.deviceDestroySucceeded)demand(o.deviceDestroyAttempted,'destroy:attempt');
    if(o.lossBeforeDestroySnapshot!=='not-observed')demand(o.unexpectedDeviceLoss,'loss:pre-destroy-unexpected');
    if(o.expectedDestroyLossObserved)demand(o.deviceDestroyAttempted&&o.deviceLostReason==='destroyed'&&!o.unexpectedDeviceLoss&&o.lossBeforeDestroySnapshot==='not-observed','loss:expected');
    if(o.unexpectedDeviceLoss)demand(v.failures.includes('unexpected-device-loss')||v.failureOverflow,'loss:failure');
    if(o.rangeDetached!==null)demand(o.mappedByteLengthAfterUnmap!==null&&o.rangeDetached===(o.mappedByteLengthAfterUnmap===0),'range:detachment');
    if(v.counts.ownedCopies)demand(o.ownedIndependent===true&&o.ownedByteLengthBeforeRelease===128&&o.mappedByteLengthBeforeUnmap===128&&o.mapStateAtCopy==='mapped','copy:shape');
    if(v.values!==null)demand(o.unmapSucceeded&&o.storageDestroyed&&o.readbackDestroyed&&o.deviceDestroySucceeded&&o.ownedByteLengthAfterRelease===128,'values:release');
    if(o.pendingAdapterRequest)demand(v.counts.adapterRequests===1&&o.adapterAvailable===null,'pending:adapter');
    if(o.pendingDeviceRequest)demand(v.counts.deviceRequests===1&&!o.deviceDestroyAttempted,'pending:device');
    if(o.pendingMapRequest)demand(v.counts.mapRequests===1&&v.counts.ownedCopies===0,'pending:map');
    if(o.pendingWork)demand(v.counts.initializationWrites===1&&v.counts.dispatchEncodes===0,'pending:work');
    if(v.status==='candidate-readback'){
      demand(v.context.originLabel==='page-origin'&&v.context.isSecureContext&&v.context.webgpuSupported,'candidate:context');
      demand(v.values!==null&&v.failures.length===0&&!v.eventOverflow&&!v.failureOverflow,'candidate:failure-or-missing-bytes');
      demand(COUNTS.every(key=>v.counts[key]===1),'candidate:counts');
      demand(stages.length===SUCCESS_STAGES.length&&stages.every((s,i)=>s===SUCCESS_STAGES[i]),'candidate:exact-lifecycle');
      demand(o.adapterAvailable===true&&o.isFallbackAdapter===false&&o.limitsAdmitted&&o.compilationErrors===0,'candidate:admission');
      demand(o.mappedByteLengthBeforeUnmap===128&&o.mappedByteLengthAfterUnmap===0&&o.ownedByteLengthBeforeRelease===128&&o.ownedByteLengthAfterRelease===128&&o.ownedIndependent===true&&o.rangeDetached===true,'candidate:ownership');
      demand(o.unmapSucceeded&&o.storageDestroyed&&o.readbackDestroyed&&o.deviceDestroyAttempted&&o.deviceDestroySucceeded,'candidate:cleanup');
      demand(o.lossBeforeDestroySnapshot==='not-observed'&&o.deviceLostReason==='destroyed'&&o.expectedDestroyLossObserved&&!o.unexpectedDeviceLoss,'candidate:loss');
      demand(o.scopes.every(s=>s.state==='popped'&&s.errorKind===null),'candidate:scopes');
      demand(o.uncapturedErrorKinds.length===0&&!o.uncapturedErrorOverflow&&!o.pendingAdapterRequest&&!o.pendingDeviceRequest&&!o.pendingMapRequest&&!o.pendingWork&&!o.cleanupDeadlineExceeded,'candidate:unresolved');
      demand(v.lastWorkStage==='owned-copy-made'&&v.browserElapsedMilliseconds<10000,'candidate:time-or-stage');
    }else demand(v.failures.length>0||v.failureOverflow||v.eventOverflow,'failed:reason-required');
    // A copied byte vector is not a content match or independent phase/persistence proof.
    return {ok:true,status:v.status,candidateByPageSelfReport:v.status==='candidate-readback',byteValues:v.values===null?null:v.values.slice(),independentPersistenceVerified:false};
  }catch(error){return {ok:false,error:typeof error?.message==='string'?error.message.slice(0,120):'invalid-envelope'};}
}
module.exports=Object.freeze({validateEnvelope,FIXTURE_ID,LAYOUT,SUCCESS_STAGES:Object.freeze(SUCCESS_STAGES.slice()),FAILURE_CODES:Object.freeze(FAILURE_CODES.slice())});
