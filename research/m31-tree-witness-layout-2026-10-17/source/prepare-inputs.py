"""Packaging-only metadata helper: hashes saved files; never decodes or executes them.
Run only in the parent's reviewed source-packaging step, before publication.
"""
from pathlib import Path
import hashlib,json,os
PACKAGE=Path(__file__).resolve().parents[1];ROOT=PACKAGE.parents[1]
NAME='research/m31-tree-witness-layout-2026-10-17';OLD='research/m31-native-tree-browser-probe-2026-10-17'
ANCHORS={
 'saved-transport.json':(58498,'b5245538e86c9f2a657205ce6177c90702e0c27bf22e247d44db5e63fe6900c7'),
 'browser-journal.jsonl':(23514,'e66b7234016d9851ce0dbc078e80e97c88dd2bbe8ed139db234b46c5d1eaa173'),
 'run-attempt.json':(2096,'ccae2f966e131fe4a4c78640f3268722025060f885138242efa90e32962abc36')}
DECODERS={
 OLD+'/source/transport.cjs':'ad5cc73b6bac321eb78deea82602d67fc8452cc204cc2e1d3b5a7ed84bef7e57',
 OLD+'/source/compact-check.py':'87229101f84c877d70fcadabfde1cf2b88bb530476eefe9dd89da478a7796bee'}
def need(ok,why):
    if not ok:raise ValueError(why)
def identity(relative):
    need(type(relative) is str and not Path(relative).is_absolute() and '..' not in Path(relative).parts,'relative-file')
    f=ROOT/relative;need(f.resolve()==f and f.is_file() and not f.is_symlink(),'regular-file');h=hashlib.sha256();n=0
    with f.open('rb') as stream:
        for block in iter(lambda:stream.read(1048576),b''):h.update(block);n+=len(block)
    return {'path':relative,'bytes':n,'sha256':h.hexdigest()}
def readjson(relative):
    f=ROOT/relative;need(f.stat().st_size<=32*1048576,'json-cap');return json.loads(f.read_bytes())
def write(relative,value):
    f=PACKAGE/relative;need(not f.exists(),'exclusive-packaging-output');data=(json.dumps(value,indent=2,allow_nan=False)+'\n').encode();need(len(data)<=2*1048576,'packaging-file-cap')
    with f.open('xb') as stream:stream.write(data);stream.flush();os.fsync(stream.fileno())
def main():
    need(PACKAGE==ROOT/NAME and not (PACKAGE/'results').exists(),'source-preparation-only')
    for relative in ('input-index.json','input-manifest.json','source/source-bundle.json'):need(not (PACKAGE/relative).exists(),'fresh-packaging-outputs')
    files={};anchors={}
    for name,(length,digest) in ANCHORS.items():
        pin=identity(OLD+'/results/'+name);need(pin['bytes']==length and pin['sha256']==digest,'fixed-anchor-pin');files[pin['path']]=pin;anchors[name]=pin
    saved=readjson(anchors['saved-transport.json']['path']);attempt=readjson(anchors['run-attempt.json']['path'])
    need(saved['schema']=='m31-saved-transport-v1' and saved['complete'] is True and saved['passed'] is True and len(saved['records'])==126,'saved-index')
    need(attempt['status']=='failed' and attempt['sourceCommit']=='4e1818c5b1ac7032018925edf17cecb1a6965e3d' and attempt['sourceManifestSha256']=='52c47de05e7cc1f13203826beba71767575b9ffcedeb212803f274dad7b06449','failed-attempt-binding')
    journal=[json.loads(row) for row in (ROOT/anchors['browser-journal.jsonl']['path']).read_bytes().splitlines()]
    need(len(journal)==66 and [x['sequence'] for x in journal]==list(range(66)),'journal-coverage');native=[x for x in journal if x['kind']=='native'];need(len(native)==30,'native-record-count')
    records=[{'index':i,'origin':'saved','sourceSequence':i,'recordPin':row['recordPin']} for i,row in enumerate(saved['records'])]
    records += [{'index':126+i,'origin':'browser','sourceSequence':row['sequence'],'recordPin':row['recordPin']} for i,row in enumerate(native)]
    need(len({row['recordPin']['path'] for row in records})==156,'unique-record-paths')
    for row in records:
        pin=row['recordPin'];need(identity(pin['path'])==pin,'record-pin');need(pin['path'].startswith(OLD+'/results/'+('saved-records/' if row['origin']=='saved' else 'records/')),'record-origin');files[pin['path']]=pin
        descriptor=readjson(pin['path']);need(descriptor['schema']=='m31-lossless-record-v1','descriptor-schema')
        for field in descriptor['fields']:
            for shard in field['stream']['chunks']:
                need(shard['path']==OLD+'/results/shards/'+shard['sha256']+'.bin' and 0<shard['bytes']<=1048576,'shard-path-size')
                if shard['path'] in files:need(files[shard['path']]==shard,'repeated-pin')
                else:need(identity(shard['path'])==shard,'shard-pin');files[shard['path']]=shard
    index={'schema':'m31-tree-witness-layout-inputs-v1','sourcePackage':OLD,'savedTransportPin':anchors['saved-transport.json'],'browserJournalPin':anchors['browser-journal.jsonl'],'sourceAttemptPin':anchors['run-attempt.json'],'records':records}
    input_manifest={'schema':'m31-tree-witness-layout-input-manifest-v1','files':[files[k] for k in sorted(files)]}
    frozen=[]
    for relative,digest in DECODERS.items():
        pin=identity(relative);need(pin['sha256']==digest,'frozen-decoder-pin');frozen.append(pin)
    local=[identity(str(f.relative_to(ROOT))) for f in sorted((PACKAGE/'source').iterdir()) if f.is_file() and f.suffix in ('.cjs','.py')]
    need(all(any(p['path']==NAME+'/source/'+required for p in local) for required in ('candidate.cjs','check.py','run.py','prepare-inputs.py','transport.cjs')),'local-source-closure')
    write('input-index.json',index);write('input-manifest.json',input_manifest)
    write('source/source-bundle.json',{'schema':'m31-tree-witness-layout-source-closure-v1','kind':'metadata-only-no-browser-bundle','sourceFiles':local,'frozenDecoderFiles':frozen,'inputManifestPin':identity(NAME+'/input-manifest.json'),'scope':'Parent execution manifest must union these sources, all input files, configuration, protocol, runtime and generated metadata. This helper executes no project source.'})
    print(json.dumps({'records':len(records),'inputFiles':len(files),'inputBytes':sum(p['bytes'] for p in files.values()),'localSourceFiles':len(local),'frozenDecoders':len(frozen)},separators=(',',':')))
if __name__=='__main__':main()
