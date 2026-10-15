#!/usr/bin/env python3
import base64, json, os, pathlib, re, subprocess, sys, time
if len(sys.argv) not in (2, 3) or not re.fullmatch('[0-9a-f]{64}', sys.argv[1]):
    raise SystemExit('A 64-hex release SHA is required')
root = pathlib.Path(__file__).resolve().parent
receipt = root / "RUN.json"
if receipt.exists() or (root / "EVIDENCE.bin").exists():
    raise SystemExit("No retry permitted")
start, status, code, raw = time.monotonic(), "failed", None, b""
try:
    p = subprocess.run(["node", str(root / "driver.cjs"), *sys.argv[1:]],
                       capture_output=True, timeout=18)
    code, raw = p.returncode, p.stdout+p.stderr
    status = "completed" if code == 0 else "failed"
except subprocess.TimeoutExpired as e:
    status, raw = "timeout", (e.stdout or b"")+(e.stderr or b"")
record = dict(status=status, code=code, release=sys.argv[1], wall_before_receipt=time.monotonic()-start,
              log_bytes=len(raw), truncated=len(raw)>2500, log_base64=base64.b64encode(raw[:2500]).decode())
with receipt.open("xb") as f:
    f.write(json.dumps(record).encode()); f.flush(); os.fsync(f.fileno())
sys.exit(status != 'completed')
