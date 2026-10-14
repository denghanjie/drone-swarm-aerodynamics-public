#!/usr/bin/env python3
"""One-shot AUDIT-C1 supervisor. Source preparation only until explicit release.

Linux /proc + wait4 accounting; no model imports. A successful receipt cannot
substitute for the independent correctness gate. No benchmark calibration/retry.
"""
from __future__ import annotations
import argparse
import ctypes
import hashlib
import json
import math
import os
from pathlib import Path
import resource
import signal
import subprocess
import sys
import time
sys.dont_write_bytecode = True

NEW_CAP = 16_000_000
NORMAL_CAP = 14_000_000
COMBINED_CAP = 200_000_000
CHILD_RSS_CAP = 512 * 1024 * 1024
TREE_RSS_CAP = 1024 * 1024 * 1024
TOTAL_CAP = 300.0
NUMERICAL_STOP = 270.0  # 180 correctness + 90 performance; preserve 30 accounting.
POLL_SECONDS = 0.01
EXPECTED_SEEDS = [840131, 840137]
ORDERS = {840131: ['BC','CB','CB','BC','BC','CB','CB','BC'],
          840137: ['CB','BC','BC','CB','CB','BC','BC','CB']}


class ResourceLimit(RuntimeError):
    pass


def sha_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def read_json(path):
    with open(path, encoding='utf8') as f:
        return json.load(f)


def self_cpu():
    r = resource.getrusage(resource.RUSAGE_SELF)
    return r.ru_utime + r.ru_stime


def child_cpu():
    r = resource.getrusage(resource.RUSAGE_CHILDREN)
    return r.ru_utime + r.ru_stime


def inventory(root):
    """Logical bytes, including temporary/partial files; reject symlink escapes."""
    total = 0
    entries = 0
    if not root.exists():
        return {'bytes': 0, 'files': 0}
    for base, dirs, files in os.walk(root, followlinks=False):
        for name in dirs:
            if Path(base, name).is_symlink():
                raise RuntimeError('Symlink directory in retained tree: ' + str(Path(base, name)))
        for name in files:
            p = Path(base, name)
            if p.is_symlink():
                raise RuntimeError('Symlink file in retained tree: ' + str(p))
            try:
                total += p.stat().st_size
            except FileNotFoundError:
                # Atomic rename may race this census. The writer must independently
                # reserve peak overlap; a later completed-job census is mandatory.
                continue
            entries += 1
    return {'bytes': total, 'files': entries}


def proc_table():
    result = {}
    for item in Path('/proc').iterdir():
        if not item.name.isdigit():
            continue
        try:
            text = (item / 'stat').read_text()
            fields = text[text.rfind(')') + 2:].split()
            result[int(item.name)] = {
                'ppid': int(fields[1]), 'pgrp': int(fields[2]), 'sid': int(fields[3]),
                'cpuTicks': sum(int(fields[i]) for i in (11, 12, 13, 14)),
                'rssBytes': max(0, int(fields[21])) * os.sysconf('SC_PAGE_SIZE'),
                'state': fields[0],
            }
        except (FileNotFoundError, ProcessLookupError, PermissionError):
            continue
    return result


def descendants(table, root_pid):
    found = set()
    frontier = {root_pid}
    while frontier:
        children = {pid for pid, row in table.items() if row['ppid'] in frontier}
        children -= found
        found |= children
        frontier = children
    return found


def expected_performance_slots():
    return [(w, s, b, 'B' if v == 'B' else 'C1')
            for w in ('W-ENDPOINT', 'W-STAGE-FIXTURE')
            for s in EXPECTED_SEEDS for b, order in enumerate(ORDERS[s])
            for v in order]


def verify_jobs(jobs):
    rows = jobs.get('jobs')
    if not isinstance(rows, list) or not rows:
        raise RuntimeError('Missing fixed job list')
    seen_performance = False
    seen = set()
    slots = []
    for row in rows:
        if row.get('id') in seen or not isinstance(row.get('id'), str):
            raise RuntimeError('Missing/duplicate job ID')
        seen.add(row['id'])
        phase = row.get('phase')
        if phase == 'performance':
            seen_performance = True
            if type(row.get('block')) is not int or type(row.get('seed')) is not int:
                raise RuntimeError('Benchmark seed/block must be integers')
            slots.append((row.get('workload'), row.get('seed'), row.get('block'), row.get('variant')))
        elif phase != 'correctness' or seen_performance:
            raise RuntimeError('Incorrect strict phase order')
    if slots != expected_performance_slots():
        raise RuntimeError('Performance jobs must match all 64 prescribed serial slots, zero-based blocks')
    return rows


class Supervisor:
    def __init__(self, root, release_path):
        # Clock uses Linux process-start tick, conservatively including Python startup.
        self.start = SCRIPT_START
        self.root = root.resolve()
        self.old = self.root.parent / 'research-next'
        self.release_path = release_path.resolve()
        self.output = self.root / 'robustness-review/results'
        self.output.mkdir(parents=True, exist_ok=True)
        self.phase = 'correctness'
        self.phase_start = self.start
        self.phase_cpu_start = 0.0
        self.completed = []
        self.reaped = []
        self.current = None
        self.stopping = None
        self.peak_new = 0
        self.peak_combined = 0
        self.peak_tree_rss_sampled = 0
        self.peak_child_rss_sampled = 0
        self.cpu_peak = 0.0
        self.ticks = os.sysconf('SC_CLK_TCK')
        self.old_start = inventory(self.old)
        self.new_start = inventory(self.root)
        self.release = read_json(self.release_path)
        self.freeze_path = self.safe_path(self.release.get('freezePath', ''))
        self.jobs_path = self.root / 'implementation/config/jobs.json'
        self.runtime_path = self.root / 'implementation/RUNTIME.json'
        self.runtime = read_json(self.runtime_path)
        self.rows = []

    def safe_path(self, relative):
        if not isinstance(relative, str) or not relative:
            raise RuntimeError('Missing study-relative path')
        p = (self.root / relative).resolve()
        if not p.is_relative_to(self.root):
            raise RuntimeError('Path escapes study')
        return p

    def elapsed(self):
        return time.monotonic() - self.start

    def usage(self):
        table = proc_table()
        own = table.get(os.getpid())
        if own is None:
            raise RuntimeError('Supervisor /proc census unavailable')
        active = descendants(table, os.getpid())
        # Each process contributes own CPU plus its already-waited descendants.
        # Live descendants are distinct; supervisor's reaped children are charged
        # separately by RUSAGE_CHILDREN and no longer appear in this live set.
        live_cpu = sum(table[p]['cpuTicks'] / self.ticks for p in active)
        cpu = self_cpu() + child_cpu() + live_cpu
        self.cpu_peak = max(self.cpu_peak, cpu)
        rss = own['rssBytes'] + sum(table[p]['rssBytes'] for p in active)
        self.peak_tree_rss_sampled = max(self.peak_tree_rss_sampled, rss)
        if active:
            self.peak_child_rss_sampled = max(self.peak_child_rss_sampled,
                                             max(table[p]['rssBytes'] for p in active))
        return {'wallSeconds': self.elapsed(), 'cpuSeconds': self.cpu_peak,
                'rssBytes': rss, 'activePids': sorted(active), 'table': table}

    def storage(self):
        new = inventory(self.root)
        old = inventory(self.old)
        self.peak_new = max(self.peak_new, new['bytes'])
        self.peak_combined = max(self.peak_combined, new['bytes'] + old['bytes'])
        if old != self.old_start:
            raise RuntimeError('Old retained tree size/count changed; integrity blocked')
        if new['bytes'] > NEW_CAP or new['bytes'] + old['bytes'] > COMBINED_CAP:
            raise ResourceLimit('Retained byte hard cap exceeded')
        return {'new': new, 'old': old, 'combinedBytes': new['bytes'] + old['bytes']}

    def atomic_json(self, relative, value, emergency=False):
        body = (json.dumps(value, indent=2, allow_nan=False) + '\n').encode()
        p = self.safe_path(relative)
        temp = p.with_name(p.name + '.partial')
        if temp.exists():
            raise RuntimeError('Existing partial output must not be overwritten')
        state = self.storage()
        # Peak overlap includes the previous target AND temporary replacement.
        cap = NEW_CAP if emergency else NORMAL_CAP
        if state['new']['bytes'] + len(body) > cap:
            raise ResourceLimit('Insufficient retained-byte reserve for atomic write')
        if state['combinedBytes'] + len(body) > COMBINED_CAP:
            raise ResourceLimit('Combined byte cap prevents atomic write')
        p.parent.mkdir(parents=True, exist_ok=True)
        with open(temp, 'xb') as f:
            f.write(body)
            f.flush()
            os.fsync(f.fileno())
        self.peak_new = max(self.peak_new, state['new']['bytes'] + len(body))
        self.peak_combined = max(self.peak_combined, state['combinedBytes'] + len(body))
        os.replace(temp, p)
        fd = os.open(p.parent, os.O_RDONLY)
        try:
            os.fsync(fd)
        finally:
            os.close(fd)

    def verify_release(self):
        r = self.release
        if r.get('schema') != 'audit-c1-execution-release/v1':
            raise RuntimeError('Unsupported release schema')
        for key in ('executionReleased', 'sourceReviewPassed', 'robustnessReviewPassed',
                    'storageForecastPassed', 'noCompetingWorkConfirmed',
                    'oldCampaignRemainsTerminalUnqualified'):
            if r.get(key) is not True:
                raise RuntimeError('Release requirement absent: ' + key)
        if r.get('retries') != 0:
            raise RuntimeError('No retries admitted')
        for key, p in [('freezeSha256', self.freeze_path),
                       ('protocolSha256', self.root/'PROTOCOL.json'),
                       ('jobsSha256', self.jobs_path)]:
            if r.get(key) != sha_file(p):
                raise RuntimeError('Release identity mismatch: ' + key)
        self.jobs = read_json(self.jobs_path)
        self.rows = verify_jobs(self.jobs)
        # Full frozen identity check is required in the child and semantic gate;
        # this independent parent also checks every standard freeze file entry.
        self.verify_frozen_files()
        self.verify_runtime()
        if self.storage()['new']['bytes'] >= NORMAL_CAP:
            raise ResourceLimit('Failure reserve unavailable before first job')

    def verify_frozen_files(self):
        if sha_file(self.freeze_path) != self.release['freezeSha256']:
            raise RuntimeError('Freeze changed during window')
        freeze = read_json(self.freeze_path)
        files = freeze.get('files')
        if not isinstance(files, list) or not files:
            raise RuntimeError('Freeze requires nonempty files [{path, sha256, bytes}]')
        seen = set()
        for item in files:
            if item['path'] in seen:
                raise RuntimeError('Duplicate frozen identity entry')
            seen.add(item['path'])
            original = self.root / item['path']
            p = original.resolve()
            if not (p.is_relative_to(self.root) or p.is_relative_to(self.old)):
                raise RuntimeError('Frozen input outside approved old/new trees')
            if original.is_symlink() or not p.is_file() or p.stat().st_size != item['bytes'] or sha_file(p) != item['sha256']:
                raise RuntimeError('Frozen source/config mismatch: ' + item['path'])
        return {'status':'passed','checkedFiles':len(files),'freezeSha256':self.release['freezeSha256']}

    def verify_runtime(self):
        runtime = read_json(self.runtime_path)
        py = read_json(self.root/'robustness-review/SUPERVISOR-RUNTIME.json')
        python_executable = Path(sys.executable).resolve()
        if py['pythonVersion'] != sys.version or str(python_executable) != py['execPath'] or python_executable.stat().st_size != py['bytes'] or sha_file(python_executable) != py['sha256']:
            raise RuntimeError('Frozen supervisor Python runtime changed')
        executable = Path(runtime['execPath'])
        if runtime.get('schema') != 'audit-c1-runtime/v1' or runtime.get('platform') != 'linux' or runtime.get('execArgv') != []:
            raise RuntimeError('Unreviewed runtime/flags')
        if executable.stat().st_size != runtime['nodeExecutableBytes'] or sha_file(executable) != runtime['nodeExecutableSha256']:
            raise RuntimeError('Frozen Node executable identity changed')
        if runtime.get('clockTicksPerSecond') != self.ticks:
            raise RuntimeError('CPU clock tick differs from freeze')
        self.runtime = runtime
        return {'status':'passed','nodeExecutableSha256':runtime['nodeExecutableSha256']}

    def checkpoint(self):
        self.atomic_json('robustness-review/results/last-durable-checkpoint.json', {
            'schema': 'audit-c1-durable-checkpoint/v1',
            'freezeSha256': self.release['freezeSha256'], 'phase': self.phase,
            'completedJobIds': [r['jobId'] for r in self.completed],
            'pendingJobIds': [r['id'] for r in self.rows if r['id'] not in {x['jobId'] for x in self.completed}],
            'exactCurrentStoppedState': False,
            'meaning': 'Last durably completed job only; not an exact interruption state.',
            'wallSeconds': self.elapsed(), 'cpuSeconds': self.usage()['cpuSeconds'],
            'resources': self.storage()}, emergency=bool(self.stopping))

    def phase_limits(self):
        return 180.0 if self.phase == 'correctness' else 90.0

    def run_child(self, job, command, receipt_path, is_gate=False):
        before = self.usage()
        cap = 45.0 if self.phase == 'correctness' else 20.0
        phase_remaining_wall = self.phase_limits() - (time.monotonic() - self.phase_start)
        phase_remaining_cpu = self.phase_limits() - (before['cpuSeconds'] - self.phase_cpu_start)
        if min(phase_remaining_wall, phase_remaining_cpu, NUMERICAL_STOP-before['wallSeconds'],
               NUMERICAL_STOP-before['cpuSeconds']) <= 1:
            raise ResourceLimit('No reserved room to start next child')
        env = os.environ.copy()
        # NODE_OPTIONS can silently change flags, imports or process behavior.
        if env.get('NODE_OPTIONS'):
            raise RuntimeError('Unfrozen NODE_OPTIONS present')
        env.update({'AUDIT_SUPERVISED': '1', 'AUDIT_FREEZE_SHA256': self.release['freezeSha256'],
            'AUDIT_CHILD_WALL_CAP_SECONDS': str(cap), 'AUDIT_CHILD_COOPERATIVE_SECONDS': str(cap-1),
            'AUDIT_WINDOW_DEADLINE_MONOTONIC_NS': str(int((self.start+NUMERICAL_STOP)*1e9)),
            'AUDIT_PHASE_DEADLINE_MONOTONIC_NS': str(int((self.phase_start+self.phase_limits())*1e9))})
        start = time.monotonic()
        log_out = self.output / (job['id'] + '.stdout.log')
        log_err = self.output / (job['id'] + '.stderr.log')
        # Children must not spawn descendants. RLIMIT_CPU is an additional kernel
        # bound; live tree CPU and phase/total caps remain independently polled.
        def limits():
            resource.setrlimit(resource.RLIMIT_CPU, (int(cap), int(cap)+1))
            resource.setrlimit(resource.RLIMIT_FSIZE, (2_000_000, 2_000_000))
        with open(log_out, 'xb') as out, open(log_err, 'xb') as err:
            child = subprocess.Popen(command, cwd=self.root, env=env, stdin=subprocess.DEVNULL,
                                     stdout=out, stderr=err, start_new_session=True, preexec_fn=limits)
            self.current = {'jobId': job['id'], 'pid': child.pid, 'startWallSeconds': start-self.start,
                            'exactCurrentStoppedState': False}
            term_at = None
            kill_sent = False
            last_storage = 0.0
            direct_status = None
            direct_usage = None
            violation = None
            while True:
                # wait4 is the ONLY reaper: Popen.poll/wait would lose authoritative
                # exited-child CPU/maxRSS. Set returncode explicitly after wait4.
                while True:
                    try:
                        pid, status, ru = os.wait4(-1, os.WNOHANG)
                    except ChildProcessError:
                        break
                    if pid == 0:
                        break
                    row = {'pid': pid, 'userCpuSeconds': ru.ru_utime, 'systemCpuSeconds': ru.ru_stime,
                           'maxRssBytes': int(ru.ru_maxrss)*1024,
                           'exitCode': os.waitstatus_to_exitcode(status)}
                    self.reaped.append(row)
                    if pid == child.pid:
                        direct_status, direct_usage = status, row
                        child.returncode = row['exitCode']
                    else:
                        violation = violation or 'Unexpected descendant process reaped'
                u = self.usage()
                now = time.monotonic()
                live = u['table'].get(child.pid)
                cpu_now = (live['cpuTicks']/self.ticks) if live else (direct_usage['userCpuSeconds'] + direct_usage['systemCpuSeconds'] if direct_usage else 0)
                child_wall = now-start
                extra = [p for p in u['activePids'] if p != child.pid]
                if extra:
                    violation = violation or 'Unexpected descendant/overlapping numerical process'
                if u['rssBytes'] > TREE_RSS_CAP or (live and live['rssBytes'] > CHILD_RSS_CAP):
                    violation = violation or 'RSS hard cap exceeded'
                if direct_usage and direct_usage['exitCode'] in (-signal.SIGXCPU, -signal.SIGXFSZ):
                    violation = violation or 'Kernel CPU/file-size resource limit'
                if direct_usage and direct_usage['maxRssBytes'] > CHILD_RSS_CAP:
                    violation = violation or 'Exited child maximum RSS exceeded cap'
                if now-last_storage >= .05 or direct_status is not None:
                    try:
                        storage = self.storage()
                        if storage['new']['bytes'] > NORMAL_CAP:
                            violation = violation or 'Normal output exhausted reserved failure bytes'
                        if log_out.stat().st_size + log_err.stat().st_size > 1_024:
                            violation = violation or 'Per-child stdout/stderr exceeded 1024-byte allocation'
                    except Exception as e:
                        violation = violation or str(e)
                    last_storage = now
                hard = child_wall >= cap or cpu_now >= cap or (now-self.phase_start) >= self.phase_limits() or (u['cpuSeconds']-self.phase_cpu_start) >= self.phase_limits() or u['wallSeconds'] >= NUMERICAL_STOP or u['cpuSeconds'] >= NUMERICAL_STOP
                cooperative = child_wall >= cap-1 or cpu_now >= cap-1 or (now-self.phase_start) >= self.phase_limits()-1 or (u['cpuSeconds']-self.phase_cpu_start) >= self.phase_limits()-1 or u['wallSeconds'] >= NUMERICAL_STOP-1 or u['cpuSeconds'] >= NUMERICAL_STOP-1
                if violation or cooperative:
                    if term_at is None:
                        term_at = now
                        violation = violation or 'Cooperative resource reserve reached'
                        try:
                            os.killpg(child.pid, signal.SIGTERM)
                        except ProcessLookupError:
                            pass
                if hard or (term_at is not None and now-term_at >= 1):
                    violation = violation or 'Hard resource deadline reached'
                    kill_sent = True
                    try:
                        os.killpg(child.pid, signal.SIGKILL)
                    except ProcessLookupError:
                        pass
                    for pid in extra:
                        try:
                            os.kill(pid, signal.SIGKILL)
                        except ProcessLookupError:
                            pass
                if direct_status is not None and not u['activePids']:
                    break
                time.sleep(POLL_SECONDS)
        after = self.usage()
        receipt = read_json(receipt_path) if receipt_path.is_file() else None
        status = 'passed'
        if violation or direct_usage is None or direct_usage['exitCode'] != 0 or receipt is None or receipt.get('status') != 'passed':
            status = 'resource_limited' if violation else {'failed':'equivalence_failed','resource_limited':'resource_limited','integrity_blocked':'integrity_blocked'}.get((receipt or {}).get('status'),'integrity_blocked')
        if is_gate and receipt and (receipt.get('benchmarkPermission') is not True or set(receipt.get('benchmarkSemanticDigests',{})) != {w+':'+str(seed) for w in ('W-ENDPOINT','W-STAGE-FIXTURE') for seed in EXPECTED_SEEDS}):
            status = 'integrity_blocked'
            violation = violation or 'Gate lacks permission or all four exact workload digests'
        if receipt and (receipt.get('freezeSha256') != self.release['freezeSha256'] or (not is_gate and receipt.get('jobId') != job['id'])):
            status = 'integrity_blocked'
            violation = violation or 'Child receipt job/freeze identity mismatch'
        row = {'schema':'audit-c1-supervised-child/v1', 'jobId':job['id'], 'phase':self.phase,
               'status':status, 'command':command, 'parentWallSeconds':time.monotonic()-start,
               'parentObservedCpuSeconds':after['cpuSeconds']-before['cpuSeconds'],
               'wait4':direct_usage, 'watchdogReason':violation, 'sigkillSent':kill_sent,
               'receiptPath':str(receipt_path.relative_to(self.root)),
               'receiptSha256':sha_file(receipt_path) if receipt_path.is_file() else None,
               'exactCurrentStoppedState':False,
               'failureCaptureAuthority':'Only a separately validated child failure capture can establish exact current state.',
               'storage':self.storage()}
        self.atomic_json('robustness-review/results/jobs/'+job['id']+'.json', row, emergency=status!='passed')
        self.current = None
        if status != 'passed':
            self.stopping = row
            raise RuntimeError(violation or 'Failed/missing child receipt; see child outputs')
        self.completed.append(row)
        self.checkpoint()
        return row

    def run(self):
        # Linux subreaper keeps unexpected orphaned grandchildren accountable.
        if sys.platform != 'linux' or ctypes.CDLL(None, use_errno=True).prctl(36, 1, 0, 0, 0) != 0:
            raise RuntimeError('Linux subreaper unavailable; full descendant accounting blocked')
        marker = self.output / 'WINDOW-STARTED.json'
        # Exclusive marker forbids re-entering/restarting this diagnostic budget.
        with open(marker, 'x', encoding='utf8') as f:
            json.dump({'schema':'audit-c1-window-start/v1', 'releaseSha256':sha_file(self.release_path),
                       'freezeSha256':self.release['freezeSha256'], 'startMonotonic':self.start,
                       'startedAtUtc':time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
                       'numericalStopBySeconds':NUMERICAL_STOP, 'finalAccountingReservedSeconds':30,
                       'retryAllowed':False}, f, indent=2)
            f.write('\n'); f.flush(); os.fsync(f.fileno())
        for directory in (self.output, self.output.parent):
            fd = os.open(directory, os.O_RDONLY)
            try:
                os.fsync(fd)
            finally:
                os.close(fd)
        self.verify_release()
        gate_passed = False
        for job in self.rows:
            if job['phase'] == 'performance' and not gate_passed:
                gate = self.jobs.get('correctnessGate', {})
                command = gate.get('command') or ['node','semantic-review/verify-correctness-receipts.cjs','--root',str(self.root),'--freeze',str(self.freeze_path),'--release',str(self.release_path)]
                replacements = {'{study}':str(self.root),'{freeze}':str(self.freeze_path),'{release}':str(self.release_path)}
                command = [replacements.get(part,part) for part in command]
                if any('{' in part or '}' in part for part in command):
                    raise RuntimeError('Unresolved gate command placeholder')
                if command[0] != 'node':
                    raise RuntimeError('Gate must use frozen Node runtime')
                command[0] = self.runtime['execPath']
                receipt = self.safe_path(gate.get('receipt','semantic-review/results/CORRECTNESS-GATE.json'))
                if receipt.exists():
                    raise RuntimeError('Preexisting correctness gate receipt; restart forbidden')
                self.run_child({'id':'independent-correctness-gate'}, command, receipt, is_gate=True)
                gate_passed = True
                self.phase = 'performance'
                self.phase_start = time.monotonic()
                self.phase_cpu_start = self.usage()['cpuSeconds']
            command = [self.runtime['execPath'],'implementation/src/child.cjs','--job',job['id'],'--release',str(self.release_path)]
            receipt = self.safe_path('implementation/results/receipts/'+job['id']+'.json')
            if receipt.exists():
                raise RuntimeError('Preexisting child receipt; restart forbidden')
            self.run_child(job, command, receipt)
        return 'all_prescribed_jobs_complete_pending_cost_validation'

    def finish(self, status, reason):
        final_runtime = self.verify_runtime() if status == 'all_prescribed_jobs_complete_pending_cost_validation' else {'status':'not_run_after_failed_window'}
        final_identity = self.verify_frozen_files() if status == 'all_prescribed_jobs_complete_pending_cost_validation' else {'status':'not_run_after_failed_window','reason':'No cost qualification; prioritize retained failure evidence.'}
        u = self.usage()
        state = self.storage()
        # After hard stop only evidence cleanup is permitted; any overshoot remains
        # explicit and prevents qualification, even when receipts otherwise pass.
        tree_rss_upper = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024 + max([x['maxRssBytes'] for x in self.reaped] or [0])
        over = u['wallSeconds'] > TOTAL_CAP or u['cpuSeconds'] > TOTAL_CAP or tree_rss_upper > TREE_RSS_CAP
        result = {'schema':'audit-c1-supervisor/v1', 'status':'resource_limited' if over else status,
            'reason':reason, 'wallSecondsBeforeFinalWrite':u['wallSeconds'],
            'processTreeCpuSecondsBeforeFinalWrite':u['cpuSeconds'],
            'hardTotalOverrun':over, 'freezeSha256':self.release.get('freezeSha256'),
            'completedJobIds':[r['jobId'] for r in self.completed],
            'unrunJobIds':[r['id'] for r in self.rows if r['id'] not in {x['jobId'] for x in self.completed}],
            'stoppingJob':self.stopping or self.current, 'reapedProcesses':self.reaped,
            'peakNewLogicalRetainedBytesObserved':self.peak_new,
            'peakCombinedLogicalRetainedBytesObserved':self.peak_combined,
            'peakTreeRssBytesSampled':self.peak_tree_rss_sampled,
            'peakChildRssBytesSampled':self.peak_child_rss_sampled,
            'supervisorMaxRssBytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024,
            'serialTreeRssConservativeUpperBoundBytes':tree_rss_upper,
            'samplingIntervalSeconds':POLL_SECONDS,
            'accounting':'Monotonic wall; supervisor CPU plus wait4/RUSAGE_CHILDREN exited CPU plus every live descendant CPU including its own already-reaped descendants; no double counting of live descendants.',
            'rssLimitations':'Active-tree RSS is sampled. wait4 supplies complete per-process maximum RSS for exited children. Short-lived unexpected descendants invalidate qualification.',
            'exactCurrentStoppedState':False, 'lastDurableCheckpointPath':'robustness-review/results/last-durable-checkpoint.json',
            'oldReferenceQualified':False, 'storage':state, 'finalFrozenIdentityCheck':final_identity,'finalRuntimeIdentityCheck':final_runtime}
        self.atomic_json('robustness-review/results/SUPERVISOR.json', result, emergency=status!='all_prescribed_jobs_complete_pending_cost_validation' or over)
        # Cost validator runs inside final-accounting allocation, imported without
        # simulation dependencies. Its output is not a scientific truth claim.
        if not over and status == 'all_prescribed_jobs_complete_pending_cost_validation':
            from validate_cost_receipts import validate_all
            report = validate_all(self.root, self.rows, self.completed, self.release['freezeSha256'])
            self.atomic_json('robustness-review/results/COST-VALIDATION.json', report, emergency=False)
        final = self.usage()
        self.atomic_json('robustness-review/results/FINAL-ACCOUNTING.json', {
            'schema':'audit-c1-final-accounting/v1',
            'wallSecondsBeforeWrite':final['wallSeconds'], 'processTreeCpuSecondsBeforeWrite':final['cpuSeconds'],
            'withinHardCapsBeforeWrite':final['wallSeconds']<=TOTAL_CAP and final['cpuSeconds']<=TOTAL_CAP,
            'retainedBeforeWrite':self.storage(),
            'peakNewLogicalRetainedBytesBeforeWrite':self.peak_new,
            'peakCombinedLogicalRetainedBytesBeforeWrite':self.peak_combined,
            'qualificationRequires':'Complete passed semantic gate, applicable cost terminal status, all resource/identity caps and no final overrun receipt.', 'meaning':'Final evidence write is charged to same clock; values here are explicitly before this write.'}, emergency=True)
        if self.elapsed()>TOTAL_CAP or self.usage()['cpuSeconds']>TOTAL_CAP:
            self.atomic_json('robustness-review/results/FINAL-OVERRUN.json', {
                'status':'resource_limited','reason':'Final evidence writes exceeded hard total; post-limit work was cleanup only.',
                'wallSeconds':self.elapsed(),'cpuSeconds':self.usage()['cpuSeconds']}, emergency=True)


_STAT = Path('/proc/self/stat').read_text()
_BOOT_MINUS_MONOTONIC = time.clock_gettime(time.CLOCK_BOOTTIME) - time.monotonic()
SCRIPT_START = int(_STAT[_STAT.rfind(')')+2:].split()[19]) / os.sysconf('SC_CLK_TCK') - _BOOT_MINUS_MONOTONIC

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1])
    p.add_argument('--release',type=Path,required=True)
    args=p.parse_args()
    supervisor=None
    try:
        if (args.root/'robustness-review/results/WINDOW-STARTED.json').exists():
            raise RuntimeError('Execution attempt already exists; no restart or overwrite permitted')
        supervisor=Supervisor(args.root,args.release)
        status=supervisor.run()
        supervisor.finish(status,None)
        return 0
    except Exception as e:
        if supervisor is not None:
            try:
                supervisor.finish('resource_limited' if isinstance(e,ResourceLimit) else 'integrity_blocked' if supervisor.stopping is None else supervisor.stopping['status'],str(e))
            except Exception as inner:
                print('Final evidence blocked: '+str(inner),file=sys.stderr)
        print(str(e),file=sys.stderr)
        return 1

if __name__=='__main__':
    raise SystemExit(main())
