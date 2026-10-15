'use strict';
// Lifecycle instrumentation only. The numerical worker and browser launch options
// are unchanged. Private pre-spawn intent closes the detached-browser record gap.
const fs = require('fs'), cp = require('child_process'), path = require('path');
const registry = process.env.RESEARCH_PROCESS_REGISTRY;
const nonce = process.env.RESEARCH_PROCESS_NONCE;
if (!registry || !path.isAbsolute(registry) || !/^[a-f0-9]{32}$/.test(nonce || ''))
  throw Error('Observer registry and nonce required');
const st = fs.lstatSync(registry);
if (!st.isFile() || st.isSymbolicLink()) throw Error('Private regular registry required');
const entries = [], original = cp.spawn;
let sequence = 0;
function append(entry) {
  const data = Buffer.from(JSON.stringify({version: 1, nonce, ...entry}) + '\n');
  if (data.length > 8192 || fs.statSync(registry).size + data.length > 65536)
    throw Error('Process registry cap');
  const fd = fs.openSync(registry, fs.constants.O_WRONLY | fs.constants.O_APPEND | fs.constants.O_NOFOLLOW);
  try { if (fs.writeSync(fd, data) !== data.length) throw Error('Partial registry append'); }
  finally { fs.closeSync(fd); }
}
cp.spawn = function(command, args, options) {
  const detached = options?.detached === true;
  const profile = Array.isArray(args) ? args.find(x => typeof x === 'string' && x.startsWith('--user-data-dir=')) : null;
  const kind = command === process.env.RESEARCH_CHROME_EXECUTABLE ? 'chrome' : 'auxiliary';
  if (detached && (kind !== 'chrome' || !profile || /\s/.test(profile)))
    throw Error('Unidentifiable detached process prohibited');
  if (++sequence > 8) throw Error('Process spawn count cap');
  const id = 'spawn-' + sequence;
  const ownership = {executable: typeof command === 'string' ? command : null, profileArgument: profile || null};
  append({phase: 'spawn-intent', id, detached, kind, ownership});
  const child = original.apply(this, arguments);
  const entry = {phase: 'spawned', id, pid: child.pid ?? null, detached, kind, ownership};
  try { append(entry); entries.push(entry); }
  catch (error) {
    // The observer can identify a detached Chrome from the already saved intent.
    // Do not signal a possibly reused PID/group here after asynchronous exit.
    throw error;
  }
  return child;
};
module.exports = {
  hasRegisteredBrowser: () => entries.some(e => e.kind === 'chrome' && e.detached && Number.isInteger(e.pid) && e.pid > 0 && e.ownership.profileArgument),
  summary: () => ({registeredProcesses: entries.length, registeredDetachedGroups: entries.filter(e => e.detached && e.pid).length, registeredBrowser: entries.some(e => e.kind === 'chrome' && e.detached && e.pid)})
};
