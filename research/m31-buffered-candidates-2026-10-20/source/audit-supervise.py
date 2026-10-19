#!/usr/bin/env python3
"""Permanent single-use supervisor for the 120 s saved-evidence audit.

Not executed during source preparation. The 130 s external ceiling includes
audit startup/termination. This process never imports any scientific module.
"""
import datetime as dt
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time

BASE = Path(__file__).resolve().parent.parent
ROOT = BASE.parent.parent
LIMIT = 2 * 1048576


def public_text(text):
    return text.replace(str(ROOT), '[repository]')


def main():
    lock = BASE / 'audit-supervisor-launch.lock'
    with lock.open('xb') as f:
        f.write((dt.datetime.now(dt.timezone.utc).isoformat() + '\n').encode())
    start = time.monotonic()
    process = None
    receipt = {'schema': 'm31-buffered-audit-supervisor-v1',
               'allocation': 'closed-no-rerun', 'externalLimitSeconds': 130,
               'auditLimitSeconds': 120, 'nativeQueriesExecuted': 0}
    code = 1
    try:
        process = subprocess.Popen([sys.executable, str(BASE / 'source/audit.py')],
                                   cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   text=True, start_new_session=True)
        stdout, stderr = process.communicate(timeout=130)
        receipt.update(returncode=process.returncode, stdout=public_text(stdout)[-2000:], stderr=public_text(stderr)[-2000:])
        code = 0 if process.returncode == 0 else 1
    except subprocess.TimeoutExpired:
        receipt['timeout'] = True
        os.killpg(process.pid, signal.SIGKILL)
        stdout, stderr = process.communicate(timeout=2)
        receipt.update(returncode=process.returncode, stdout=public_text(stdout)[-2000:], stderr=public_text(stderr)[-2000:])
    except Exception as error:
        receipt['failure'] = public_text(type(error).__name__ + ': ' + str(error))[:1500]
        if process is not None and process.poll() is None:
            os.killpg(process.pid, signal.SIGKILL)
    receipt['wallSeconds'] = time.monotonic() - start
    if receipt['wallSeconds'] > 130:
        receipt['externalDeadlineExceeded'] = True
        code = 1
    report = BASE / 'results/audit.json'
    audit_lock = BASE / 'results/audit.lock'
    size = lock.stat().st_size + sum(p.stat().st_size for p in (report, audit_lock) if p.is_file())
    body = (json.dumps(receipt, separators=(',', ':'), allow_nan=False) + '\n').encode()
    if size + len(body) > LIMIT:
        receipt = {'schema': 'm31-buffered-audit-supervisor-v1', 'allocation': 'closed-no-rerun',
                   'failure': 'combined audit output budget', 'nativeQueriesExecuted': 0}
        body = (json.dumps(receipt, separators=(',', ':')) + '\n').encode()
        code = 1
    with (BASE / 'audit-supervisor.json').open('xb') as f:
        f.write(body)
    print(json.dumps({'returncode': code, 'receipt': str((BASE / 'audit-supervisor.json').relative_to(ROOT))}))
    return code


if __name__ == '__main__':
    sys.exit(main())
