import sys,os
if sys.flags.optimize or os.environ.get('PYTHONOPTIMIZE'):
 raise RuntimeError('optimized-Python-not-permitted')
"""Byte-only provenance utilities. No simulator imports or numerical descriptors."""
from pathlib import Path
import json,hashlib,io,gzip,time
BASE=Path(__file__).resolve().parent.parent
ROOT=BASE.parent.parent
EVENTS=[]
READ_OPERATION=0
START=time.monotonic()
LIMIT=900

def guard():
 if time.monotonic()-START>LIMIT:raise RuntimeError('wall-budget')

def sha(b):return hashlib.sha256(b).hexdigest()

def checked(path,pin):
 global READ_OPERATION
 READ_OPERATION+=1
 operation=READ_OPERATION
 path=Path(path)
 for attempt in range(1,4):
  guard()
  try:
   b=path.read_bytes()
   if len(b)==pin['bytes'] and sha(b)==pin['sha256']:return b
   event={'path':path.relative_to(ROOT).as_posix(),'attempt':attempt,'operation':operation,'kind':'byte-mismatch','readBytes':len(b),'readSha256':sha(b)}
  except OSError as e:event={'path':path.relative_to(ROOT).as_posix(),'attempt':attempt,'operation':operation,'kind':'read-error','errno':e.errno}
  EVENTS.append(event)
 raise RuntimeError('verified-read-failed:'+path.relative_to(ROOT).as_posix())

def load(path):return json.loads(Path(path).read_text())

def gate():
 raw=(BASE/'source-manifest.json').read_bytes();m=json.loads(raw);p=load(BASE/'source-publication.json')
 assert p['manifestSha256']==sha(raw) and p['remoteBytesEqualLocal'] and p['committedBytesEqualLocal'] and p['verifiedFilePins']==len(m['files'])
 for x in m['files']:checked(ROOT/x['path'],x)
 return p

class Parts(io.RawIOBase):
 def __init__(self,stream):
  super().__init__();self.s=stream;self.i=0;self.current=b'';self.at=0;self.total=0;self.hash=hashlib.sha256();self.verified=False
 def readable(self):return True
 def readinto(self,buf):
  guard()
  if not buf:return 0
  if self.at==len(self.current):
   ps=self.s['descriptor']['parts']
   if self.i==len(ps):
    assert self.total==self.s['descriptor']['bytes'] and self.hash.hexdigest()==self.s['descriptor']['sha256'];self.verified=True;return 0
   p=ps[self.i];assert p['offset']==self.total
   self.current=checked(ROOT/self.s['folder']/p['file'],p);self.at=0;self.i+=1
   self.hash.update(self.current);self.total+=len(self.current)
  n=min(len(buf),len(self.current)-self.at);buf[:n]=self.current[self.at:self.at+n];self.at+=n;return n

def records(stream,receipt):
 parts=Parts(stream);h=hashlib.sha256();offset=0;n=0
 with io.BufferedReader(parts,1024*1024) as buffered,gzip.GzipFile(fileobj=buffered) as z:
  while True:
   guard();line=z.readline(4*1024*1024+1)
   if not line:break
   assert len(line)<=4*1024*1024 and line.endswith(b'\n');h.update(line)
   obj=json.loads(line);assert obj['sequence']==n
   provenance={'sequence':n,'offset':offset,'bytes':len(line),'sha256':sha(line)}
   offset+=len(line);n+=1
   yield obj,provenance
  assert parts.verified
 d=stream['descriptor'];assert n==d['records']
 if 'rawBytes' in d:assert offset==d['rawBytes'] and h.hexdigest()==d['rawSha256']
 receipt.update({'phase':stream['phase'],'caseId':stream['caseId'],'compressedBytes':parts.total,'compressedSha256':parts.hash.hexdigest(),'rawBytes':offset,'rawSha256':h.hexdigest(),'records':n})

def write(path,data):
 b=(json.dumps(data,separators=(',',':'),allow_nan=False)+'\n').encode()
 with Path(path).open('xb') as f:f.write(b)
 return {'file':Path(path).relative_to(BASE).as_posix(),'bytes':len(b),'sha256':sha(b)}
