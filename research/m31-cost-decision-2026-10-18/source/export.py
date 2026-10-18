"""One saved-only export. No scientific producer imports or execution."""
from pathlib import Path
import hashlib,json,importlib.util,sys,time,struct
ROOT=Path(__file__).resolve().parents[3]
HERE=Path(__file__).resolve().parents[1]
PACKAGE='research/m31-native-tree-state1000-2026-10-17'
START=time.monotonic()
sys.dont_write_bytecode=True
def need(v,m):
    if not v:raise ValueError(m)
def guard(ctx):need(time.monotonic()-START<30,'export-deadline')
def fields(v,n,m):need(type(v)is dict and set(v)==set(n),m)
def integer(v,lo,hi,m):need(type(v)is int and lo<=v<=hi,m);return v
def decode(b):return json.loads(b)
def pin(p):
    b=p.read_bytes();return {'path':str(p.relative_to(ROOT)),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def read_pin(root,p):
    guard(None);f=root/p['path'];need(f.resolve().is_relative_to(ROOT) and not f.is_symlink(),'path');need(pin(f)==p,'pin');return f.read_bytes()
def write(name,v):
    raw=(json.dumps(v,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode();need(len(raw)<12*1048576,'export-size')
    with (HERE/name).open('xb')as f:f.write(raw)
    return pin(HERE/name)
def main():
    (HERE/'export.lock').open('x').close()
    old=ROOT/PACKAGE
    manifest_pin=pin(old/'result-manifest.json')
    need(manifest_pin['sha256']=='59be1b771384587262d9925742e7ae9bb865b15b952cb3f2e23ea9d4b075749d','prior-result-manifest')
    manifest=json.loads((old/'result-manifest.json').read_bytes())
    bypath={p['path']:p for p in manifest['files']}
    checkpath=PACKAGE+'/results/check.json';check=decode(read_pin(ROOT,bypath[checkpath]))
    need(check['passed'] and check['complete'] and len(check['stages'])==1 and check['stages'][0]['caseId']=='tree-t0-n1000-a' and check['stages'][0]['nativePins']['F']['sha256']=='2c1dacc72cb00ab1685233fd2385518e6df66993bd0175f3e8b3d2f858e50bd9','prior-check')
    decoder='research/m31-native-tree-browser-probe-2026-10-17/source/compact-check.py'
    read_pin(ROOT,bypath[decoder]);spec=importlib.util.spec_from_file_location('saved_reader',ROOT/decoder);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    reader=m.Resolver(sys.modules[__name__],{'root':ROOT});native=reader.record(check['stages'][0]['nativePins']['F'])
    keys=['diagnostics','status','reason','constants','raw','ids','prepared','coefficients','solution','loads','consumption']
    expected={k:native[k] for k in keys};need(expected['status']=='native-success' and len(expected['raw'])==1000,'baseline')
    ignored={'diagnostics.buildPhasesMs','diagnostics.geometryWork.gatheredNonselfCandidates','diagnostics.screen.orderedPairVisits','diagnostics.screen.componentTests'}
    def normalized(v,path=''):
        if type(v)in(int,float):return struct.pack('>d',v).hex()
        if type(v)is list:return [normalized(x,path+'[]')for x in v]
        if type(v)is dict:return {k:normalized(x,path+'.'+k if path else k)for k,x in v.items()if (path+'.'+k if path else k)not in ignored}
        return v
    expected_pin=write('expected.json',normalized(expected))
    input_pin=write('input-words.json',{'drones':expected['raw']})
    reader.verify_preserved()
    write('EXPORT.json',{'resultManifest':manifest_pin,'savedOnly':True,'producerCalls':0,'expected':expected_pin,'input':input_pin,'readPins':[bypath[checkpath],bypath[decoder],*reader.seen.values()],'wallSeconds':time.monotonic()-START})
if __name__=='__main__':main()
