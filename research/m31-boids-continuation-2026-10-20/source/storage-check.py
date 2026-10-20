from pathlib import Path
import hashlib,json,subprocess,os,sys,time,gzip,io
BASE=Path(__file__).resolve().parent.parent
ROOT=BASE.parent.parent
start=time.monotonic()
def guard():assert time.monotonic()-start<20,'storage-wall'
def sha(b):return hashlib.sha256(b).hexdigest()
assert (BASE/'storage-supervisor-launch.lock').is_file()
out=BASE/'storage';out.mkdir()
try:
 raw=(BASE/'source-manifest.json').read_bytes();m=json.loads(raw);p=json.loads((BASE/'source-publication.json').read_bytes())
 assert p['manifestSha256']==sha(raw) and p['remoteBytesEqualLocal'] is True and p['committedBytesEqualLocal'] is True
 assert p['verifiedFilePins']==len(m['files'])
 for pin in m['files']:
  b=(ROOT/pin['path']).read_bytes();assert len(b)==pin['bytes'] and sha(b)==pin['sha256'];guard()
 runtime=json.loads((BASE/'runtime.json').read_text());node=os.environ['M31_NODE'];b=Path(node).read_bytes();assert len(b)==runtime['nodeBytes'] and sha(b)==runtime['nodeSha256']
 assert not os.environ.get('NODE_OPTIONS') and not os.environ.get('NODE_PATH')
 subprocess.run([node,str(BASE/'source/storage-test.cjs')],check=True,timeout=max(1,19-(time.monotonic()-start)))
 identity=json.loads((out/'fixture-index.json').read_text());j=identity['identity'];parts=[];offset=0
 for part in j['parts']:
  assert part['offset']==offset and 0<part['bytes']<=32768
  b=(out/part['file']).read_bytes();assert len(b)==part['bytes'] and sha(b)==part['sha256'];parts.append(b);offset+=len(b);guard()
 compressed=b''.join(parts);expected=(out/'expected.jsonl').read_bytes();decoded=gzip.decompress(compressed)
 assert len(compressed)==j['bytes'] and sha(compressed)==j['sha256']
 assert decoded==expected and len(decoded)==j['rawBytes'] and sha(decoded)==j['rawSha256']
 lines=decoded.splitlines(keepends=True);assert len(lines)==j['records']==40
 assert [json.loads(x)['sequence'] for x in lines]==list(range(40))
 # Each physical part boundary lies inside one complete concatenated stream.
 assert len(parts)>1 and len(compressed)>32768 and len(expected)>65536
 assert len(identity['checks'])==2
 guard();assert sum(p.stat().st_size for p in out.iterdir())+4096<=8*1024*1024
 report={'passed':True,'closed':True,'checks':['40 exact JSON-line byte reconstructions','ordered part offsets and all hashes','multiple raw blocks and physical part boundaries','independent Python gzip decoding','raw aggregate identity']+identity['checks'],'wallSeconds':time.monotonic()-start,'scientificCalls':0}
 code=0
except Exception as e:
 report={'passed':False,'closed':True,'error':str(e).replace(str(ROOT),'[repository]'),'wallSeconds':time.monotonic()-start,'scientificCalls':0};code=1
with (out/'qualification.json').open('x') as f:json.dump(report,f,indent=2);f.write('\n')
print(json.dumps(report));sys.exit(code)
