"""One exclusive browser attempt, wall and disk watchdog; no retries."""
from pathlib import Path
import os,sys,subprocess,time,json,signal,datetime,hashlib
ROOT=Path(__file__).resolve().parents[3];P=Path(__file__).resolve().parents[1]
private=Path(sys.argv[2])
assert (P/'expected.json').stat().st_size<4*1048576 and (P/'input-words.json').stat().st_size<1048576
assert (ROOT/'research/m31-native-tree-state1000-2026-10-17/source/browser-bundle.js').stat().st_size<2*1048576
assert sum(f.stat().st_size for f in P.rglob('*')if f.is_file())<12*1048576
private.mkdir(exist_ok=False);out=P/'results';out.mkdir(exist_ok=False)
start=time.monotonic();limit=180;reason=None
def size(p):return sum(f.lstat().st_size for f in p.rglob('*')if f.is_file()or f.is_symlink())
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def write(name,v):(out/name).write_text(json.dumps(v,indent=2)+'\n')
write('attempt.json',{'startedUtc':now(),'maxSeconds':limit,'maxQueries':116,'status':'started'})
with (private/'stdout.log').open('xb')as stdout,(private/'stderr.log').open('xb')as stderr:
 child=subprocess.Popen([sys.argv[1],str(P/'source/run.cjs'),str(ROOT),str(private)],stdout=stdout,stderr=stderr,start_new_session=True)
 while child.poll()is None:
  if time.monotonic()-start>limit:reason='wall-cap'
  elif size(P)>32*1048576 or size(private)>128*1048576:reason='disk-cap'
  elif datetime.datetime.now(datetime.timezone.utc)>=datetime.datetime.fromisoformat('2026-10-18T13:57:26+00:00'):reason='cycle-cutoff'
  if reason:
   os.killpg(child.pid,signal.SIGKILL)
   child.wait(timeout=3)
   break
  time.sleep(.2)
 code=child.wait()
if reason is None:
 if time.monotonic()-start>limit:reason='wall-cap-after-exit'
 elif size(P)>32*1048576 or size(private)>128*1048576:reason='disk-cap-after-exit'
 elif datetime.datetime.now(datetime.timezone.utc)>=datetime.datetime.fromisoformat('2026-10-18T13:57:26+00:00'):reason='cycle-cutoff-after-exit'
write('supervisor.json',{'exitCode':code,'reason':reason,'wallSeconds':time.monotonic()-start,'publicBytes':size(P),'privateBytes':size(private),'finishedUtc':now(),'rootChildExitObserved':True,'allHelperExitVerified':False})
sys.exit(0 if code==0 and reason is None else 1)
