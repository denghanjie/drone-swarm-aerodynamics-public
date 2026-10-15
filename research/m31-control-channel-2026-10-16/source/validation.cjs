'use strict';
// Pure decoded-value validation. No I/O, process creation, browser or byte conversion.
const LENGTH = 3840, JSON_CAP = 32768;
const KEYS = ['version','format','payloadId','byteLength','values','origin','isSecureContext','constructionPhase','browserConstructionMilliseconds'];
function requireValue(ok, code) {
  if (!ok) { const error = new TypeError(code); error.code = code; throw error; }
}
function validateEnvelope(value) {
  requireValue(value !== null && typeof value === 'object' && Object.getPrototypeOf(value) === Object.prototype, 'envelope-object');
  const keys = Reflect.ownKeys(value);
  requireValue(keys.length === KEYS.length && keys.every(k => typeof k === 'string' && KEYS.includes(k)), 'envelope-keys');
  for (const key of KEYS) {const d=Object.getOwnPropertyDescriptor(value,key);
    requireValue(Object.hasOwn(d,'value')&&d.enumerable===true, 'envelope-data-properties');}
  requireValue(value.version === 1 && value.format === 'uint8-values-v1' && value.payloadId === 'synthetic-control-channel-3840-v1', 'envelope-identity');
  requireValue(value.byteLength === LENGTH && value.constructionPhase === 'array-ready', 'envelope-byte-shape');
  requireValue(value.origin === 'http://127.0.0.1:8876' || value.origin === 'null', 'envelope-origin');
  requireValue(typeof value.isSecureContext === 'boolean', 'envelope-secure-context');
  requireValue(typeof value.browserConstructionMilliseconds === 'number' && Number.isFinite(value.browserConstructionMilliseconds)
    && value.browserConstructionMilliseconds >= 0 && value.browserConstructionMilliseconds < 10000, 'envelope-browser-duration');
  requireValue(Array.isArray(value.values) && Object.getPrototypeOf(value.values) === Array.prototype && value.values.length === LENGTH, 'values-array-length');
  requireValue(Reflect.ownKeys(value.values).length === LENGTH + 1, 'values-own-key-count');
  for (let i=0;i<LENGTH;i++) {
    const descriptor = Object.getOwnPropertyDescriptor(value.values,String(i));
    requireValue(descriptor && Object.hasOwn(descriptor,'value'), 'values-dense-data');
    const n = descriptor.value;
    requireValue(typeof n === 'number' && Number.isFinite(n) && Number.isInteger(n) && n >= 0 && n <= 255 && !Object.is(n,-0), 'values-uint8');
  }
  const json = JSON.stringify(value) + '\n';
  // All admitted strings are fixed ASCII and all other values are finite primitives.
  requireValue(json.length <= JSON_CAP, 'returned-json-cap');
  return {json, jsonBytes: json.length, byteLength: LENGTH};
}
module.exports = {validateEnvelope, LENGTH, JSON_CAP};
