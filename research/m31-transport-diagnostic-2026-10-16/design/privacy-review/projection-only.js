const safeWord = x => typeof x === 'string' && /^[A-Za-z][A-Za-z0-9_. -]{0,159}$/.test(x) && !/[a-f0-9]{24}/i.test(x) ? x : null;
const safeNumber = x => typeof x === 'number' && Number.isFinite(x) ? x : null;
const headers = h => {
  const result = {};
  const allow = new Set(['origin','content-type','content-length','access-control-request-method','access-control-request-headers',
    'access-control-request-private-network','access-control-allow-origin','access-control-allow-methods',
    'access-control-allow-headers','access-control-allow-private-network','cache-control']);
  for (const [key, value] of Object.entries(h || {})) {
    const k = key.toLowerCase(); if (allow.has(k)) {const v=String(value);if(v.length>512)truncatedEvents++;result[k]=v.slice(0,512);}
  }
  return result;
};
function urlLabel(value) {
  if (value === sinkURL) return 'reserved-sink';
  if (value === pageBase + 'browser.html') return 'fixture-html';
  if (value === pageBase + 'browser.js') return 'fixture-script';
  if (typeof value === 'string' && value.startsWith('http://127.0.0.1:8876/')) return 'other-page-origin';
  return 'other';
}
function publicHeaders(h) {
  const a = headers(h);
  for (const k of ['origin', 'access-control-allow-origin']) if (k in a)
    a[k] = a[k] === 'http://127.0.0.1:8876' ? 'page-origin' : a[k] === '*' ? '*' : a[k] === 'null' ? 'opaque-null' : 'other-origin';
  for (const [k,v] of Object.entries(a)) {
    if (['origin','access-control-allow-origin'].includes(k)) continue;
    const known = k === 'content-length' ? /^\d{1,8}$/.test(v) : k === 'content-type' ?
      ['application/octet-stream','application/json','text/html','application/javascript'].includes(v) :
      k === 'cache-control' ? ['no-store','no-cache','max-age=0'].includes(v) :
      k.includes('private-network') ? ['true','false'].includes(v) :
      /^(?:(?:POST|OPTIONS|GET|HEAD|Content-Type|content-type)(?:, ?)?)+$/.test(v);
    if(!known)a[k]='other-header-value';
  }
  return a;
}
function publicData(d) {
  const p = {};
  for (const k of ['requestID','connectionID','cdpID','relatedCDPID','method','resourceType','errorName','blockedReason','corsError',
    'issueCode','initiatorType','initiatorIPAddressSpace','resourceIPAddressSpace','localNetworkAccessRequestPolicy','type','reason','stage'])
    if (k in d && d[k] !== undefined) p[k] = safeWord(d[k]);
  if (d.errorText !== undefined) p.errorText = /^net::ERR_[A-Z0-9_]+$/.test(d.errorText) ? d.errorText : 'other-error-text';
  if (d.failedParameter !== undefined) p.failedParameterObserved = true;
  if (d.initiatorOrigin !== undefined) p.initiatorOriginLabel = d.initiatorOrigin === 'http://127.0.0.1:8876' ? 'page-origin' : d.initiatorOrigin === 'null' ? 'opaque-null' : 'other-origin';
  if (d.origin !== undefined) p.originLabel = d.origin === 'http://127.0.0.1:8876' ? 'page-origin' : d.origin === 'null' ? 'opaque-null' : 'other-origin';
  for (const k of ['bytes','receivedBytes','writtenBytes','writeCalls','status','browserMilliseconds','encodedDataLength'])
    if (k in d) p[k] = safeNumber(d[k]);
  for (const k of ['match','started','complete','ok','canceled','hasExtraInfo','ipProtectionUsed','initiatorIsSecureContext','isSecureContext','isWarning','auditReplayPossible','redirected'])
    if (k in d && d[k] !== undefined) p[k] = typeof d[k] === 'boolean' ? d[k] : null;
  if ('url' in d && d.url !== undefined) p.urlLabel = urlLabel(d.url);
  if(d.transferID === 'transfer-1')p.transferID='transfer-1';
  if ('headers' in d) p.headers = publicHeaders(d.headers);
  if ('sha256' in d) p.sha256 = /^[a-f0-9]{64}$/.test(d.sha256) ? d.sha256 : null;
  return p;
}
