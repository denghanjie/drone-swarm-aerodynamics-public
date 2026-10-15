'use strict';
// Pure data policy and injected-file writer. No browser, process, clock or filesystem imports.
const {validateEnvelope}=require('./validation.cjs');
const LIMITS=Object.freeze({wallSeconds:60,workerSeconds:40,evaluateSeconds:12,cleanupSeconds:58,combinedBytes:8388608,ownedRSSBytes:2147483648,traceEvents:2048});
const code=error=>typeof error==='string'&&/^[A-Za-z0-9:._-]{1,120}$/.test(error)?error:'invalid-envelope';
function admitExecution(config,now){
  if(!config||config.executionAllocated!==true)return {ok:false,code:'execution-not-allocated'};
  if(config.version!==1||config.scope!=='synthetic-gpu-readback-host')return {ok:false,code:'config-identity'};
  const date=value=>typeof value==='string'&&/^(?!0000)\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$/.test(value)&&Number.isFinite(Date.parse(value))&&new Date(Date.parse(value)).toISOString()===value.replace('Z','.000Z');
  if(!['notBeforeUTC','stopNewLaunchUTC','reviewNotBeforeUTC','reviewStopNewLaunchUTC'].every(key=>date(config[key])))return {ok:false,code:'explicit-window-required'};
  const start=Date.parse(config.notBeforeUTC),stop=Date.parse(config.stopNewLaunchUTC);
  if(start>=stop||Date.parse(config.reviewNotBeforeUTC)>=Date.parse(config.reviewStopNewLaunchUTC)||!Number.isFinite(now)||now<start||now>=stop)return {ok:false,code:'outside-new-launch-window'};
  if(!config.limits||Object.keys(config.limits).length!==Object.keys(LIMITS).length||Object.entries(LIMITS).some(([k,v])=>config.limits[k]!==v))return {ok:false,code:'proposed-limit-mismatch'};
  return {ok:true,start,stop,limits:LIMITS};
}
function prepareDecodedEnvelope(actual){
  const checked=validateEnvelope(actual);
  if(!checked.ok)return {ok:false,validationError:code(checked.error),projection:{kind:'rejected-decoded-return-projection',errorCode:code(checked.error),rootType:actual===null?'null':typeof actual,rootIsArray:Array.isArray(actual),originalRetained:false}};
  // Only an exact bounded validated envelope is serialized. Wrong bytes are not replaced.
  const json=JSON.stringify(actual)+'\n';
  if(json.length>32768)return {ok:false,validationError:'validated-json-cap',projection:{kind:'rejected-decoded-return-projection',errorCode:'validated-json-cap',rootType:'object',rootIsArray:false,originalRetained:false}};
  return {ok:true,json,byteValues:checked.byteValues,pageStatus:actual.status,pageFailureCodes:actual.failures.slice(),candidateByPageSelfReport:checked.candidateByPageSelfReport,
    pageReport:{phaseEvidenceKind:'page-self-report',browserElapsedMilliseconds:actual.browserElapsedMilliseconds,lastWorkStage:actual.lastWorkStage,counts:{...actual.counts},observation:JSON.parse(JSON.stringify(actual.observation)),independentPersistenceVerified:false}};
}
function emptyWriteReceipt(){return {attempted:false,opened:false,closed:false,complete:false,writtenBytes:0,writeCalls:0};}
function writeExclusive(io,filename,data,receipt,guard=()=>{},onWrite=()=>{}){
  guard();receipt.attempted=true;let fd;
  try{fd=io.openSync(filename,'wx');receipt.opened=true;
    while(receipt.writtenBytes<data.length){guard();const remaining=data.length-receipt.writtenBytes;
      const n=io.writeSync(fd,data,receipt.writtenBytes,remaining);if(!Number.isSafeInteger(n)||n<=0||n>remaining)throw Error('invalid-write-count');
      receipt.writtenBytes+=n;receipt.writeCalls++;onWrite(receipt);}
  }finally{if(fd!==undefined){io.closeSync(fd);receipt.closed=true;}}
  receipt.complete=receipt.closed&&receipt.writtenBytes===data.length;
  return receipt;
}
function classify(out){
  if(!out.localObservationComplete)return 'host-incomplete';
  if(!out.returned.received)return 'evaluate-rejected';
  if(!out.returned.validationPassed)return 'envelope-rejected';
  if(out.returned.bytes!==null&&!(out.persistence.complete&&out.persistence.closed&&out.persistence.equalsReturned))return 'persistence-failed';
  if(out.returned.pageStatus==='failed')return out.returned.bytes===null?'page-failed-without-bytes':'page-failed-with-bytes';
  if(out.returned.exact!==true)return 'valid-byte-mismatch';
  return 'candidate-byte-transfer-recorded';
}
module.exports=Object.freeze({LIMITS,admitExecution,prepareDecodedEnvelope,emptyWriteReceipt,writeExclusive,classify});
