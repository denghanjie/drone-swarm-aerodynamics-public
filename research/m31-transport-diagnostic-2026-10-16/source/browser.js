'use strict';
(() => {
  let used = false;
  window.transportReady = true;
  window.runTransport = async input => {
    if (used) throw Error('Sole application invocation already consumed');
    used = true;
    const state = {attempted: false, fetchCompleted: false, acknowledged: false,
      httpStatus: null, receipt: null, errorName: null, redirected: null, lastPhase: 'allocated'};
    const mark = async (kind, data = {}) => {
      state.lastPhase = kind;
      await window.__transportTrace({kind, browserMilliseconds: performance.now(), ...data});
    };
    const aborter = new AbortController();
    let timer;
    try {
      await mark('browser-context', {origin: location.origin, isSecureContext: window.isSecureContext});
      const bytes = new Uint8Array(3840);
      for (let i = 0; i < bytes.length; i++) bytes[i] = (i * 73 + 19) % 256;
      await mark('payload-ready', {bytes: bytes.length});
      await mark('fetch-start', {bytes: bytes.length});
      state.attempted = true;
      timer = setTimeout(() => aborter.abort(), 10000);
      const response = await fetch(input.sinkURL, {method: 'POST',
        headers: {'Content-Type': 'application/octet-stream'}, body: bytes, signal: aborter.signal});
      state.fetchCompleted = true;
      state.httpStatus = response.status;
      state.redirected = response.redirected;
      await mark('fetch-response', {status: response.status, ok: response.ok, redirected: response.redirected});
      if (!response.ok) throw Error('Evidence sink rejected synthetic transfer');
      const receipt = await response.json();
      state.receipt = {complete: receipt.complete === true, bytes: receipt.bytes, sha256: receipt.sha256};
      if (receipt.complete !== true || receipt.bytes !== bytes.length || receipt.sha256 !== input.expectedSHA256)
        throw Error('Evidence sink receipt mismatch');
      state.acknowledged = true;
      await mark('receipt-matched', state.receipt);
    } catch (error) {
      state.errorName = error.name;
      await mark('fetch-error', {errorName: error.name, errorMessage: error.message});
    } finally {
      clearTimeout(timer);
    }
    return state;
  };
})();
