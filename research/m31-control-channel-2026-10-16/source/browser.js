'use strict';
(() => {
  let used = false;
  window.runControlChannelPayload = () => {
    if (used) throw Error('Sole payload return already consumed');
    used = true;
    const start = performance.now();
    const bytes = new Uint8Array(3840);
    for (let i=0;i<bytes.length;i++) bytes[i] = (73*i+19)%256;
    const values = Array.from(bytes);
    return {version:1,format:'uint8-values-v1',payloadId:'synthetic-control-channel-3840-v1',
      byteLength:bytes.length,values,origin:location.origin,isSecureContext:window.isSecureContext,
      constructionPhase:'array-ready',browserConstructionMilliseconds:performance.now()-start};
  };
})();
