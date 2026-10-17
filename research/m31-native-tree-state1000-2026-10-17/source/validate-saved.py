"""Metadata-only retained prerequisite gate. No project imports or scientific calls."""
from pathlib import Path
import datetime, hashlib, json, os, sys, time
START = time.monotonic_ns()
NAME = 'research/m31-native-tree-state1000-2026-10-17'
MAX_FILE = 32 * 1048576

def need(ok, reason):
    if not ok: raise ValueError(reason)

def main(root, expected, commit):
    package = root / NAME
    def read(file):
        need(file.is_file() and not file.is_symlink() and file.stat().st_size <= MAX_FILE, 'metadata-file')
        return json.loads(file.read_bytes())
    config = read(package / 'config.json')
    need(config['executionAllowed'] is True and config['authorization'], 'execution-not-authorized')
    cutoff = datetime.datetime.fromisoformat(config['launchCutoffUtc'])
    need(cutoff.tzinfo is not None and datetime.datetime.now(datetime.timezone.utc) < cutoff, 'authorization-window')
    need(os.environ.get('RESEARCH_EXECUTION_CONTEXT') == 'tool-require-escalated'
         and os.environ.get('RESEARCH_STAGE') == 'saved-validation'
         and os.environ.get('RESEARCH_CHILD_BUDGET_MILLISECONDS') == '15000', 'dispatch-context')
    deadline = min(START + 15_000_000_000, int(os.environ['RESEARCH_CHILD_DEADLINE_MONOTONIC_NS']),
                   int(os.environ['RESEARCH_TOTAL_DEADLINE_MONOTONIC_NS']))
    def guard():
        need(time.monotonic_ns() < deadline and datetime.datetime.now(datetime.timezone.utc) < cutoff, 'metadata-deadline')
    def identity(file):
        h = hashlib.sha256(); count = 0
        with file.open('rb') as stream:
            for block in iter(lambda: stream.read(1048576), b''):
                guard(); h.update(block); count += len(block)
        return {'bytes':count,'sha256':h.hexdigest()}
    def verify(pin):
        rel = pin['path']; need(type(rel) is str and not Path(rel).is_absolute() and '..' not in Path(rel).parts, 'pin-path')
        file = root / rel
        need(file.resolve() == file and file.is_file() and not file.is_symlink(), 'pin-location')
        need(identity(file) == {k:pin[k] for k in ('bytes','sha256')}, 'pin-identity')
        return file
    attempt = read(package / 'results/run-attempt.json')
    token = os.environ.get('RESEARCH_RUN_TOKEN','')
    need(token and attempt['status'] == 'running' and attempt['stages']['saved-validation']['status'] == 'started'
         and hashlib.sha256(token.encode()).hexdigest() == attempt['runTokenSha256']
         and attempt['sourceCommit'] == commit and attempt['sourceManifestSha256'] == expected, 'supervisor-binding')
    manifest_path = package / 'source-manifest.json'; manifest_identity = identity(manifest_path)
    need(manifest_identity['sha256'] == expected, 'manifest-identity'); manifest = read(manifest_path)
    pins = {p['path']:p for p in manifest['files']}; need(len(pins) == len(manifest['files']), 'source-duplicates')
    for pin in pins.values(): verify(pin)
    need(identity(Path(sys.executable).resolve()) == {k:manifest['runtime']['python'][k] for k in ('bytes','sha256')}, 'python-runtime')
    for rel in ('config.json','source/validate-saved.py','prerequisites.json','review/STORAGE-ADMISSION.json'):
        need(NAME+'/'+rel in pins, 'required-source')
    publication = read(package / 'source-publication.json')
    need(publication['commit'] == commit and publication['manifestPath'] == NAME+'/source-manifest.json'
         and publication['manifestSha256'] == expected and publication['manifestBytes'] == manifest_identity['bytes']
         and publication['verifiedFilePins'] == len(pins) and publication['remoteBytesEqualLocal'] is True
         and publication['committedBytesEqualLocal'] is True
         and datetime.datetime.fromisoformat(publication['verifiedUtc']) <= datetime.datetime.fromisoformat(attempt['startedUtc']), 'publication-binding')
    output = {'schema':'m31-state1000-retained-validation-v1','sourceCommit':commit,'sourceManifestSha256':expected,
              'complete':False,'passed':False,'scientificCalls':0,'prerequisites':[], 'errors':[],
              'scope':'Exact retained checkpoint metadata and file integrity only; no scientific or control rerun.'}
    try:
        admission = read(package / 'review/STORAGE-ADMISSION.json')
        need(admission['admitted'] is True and admission['scope'] == 'cold-complete-success-evidence-no-sharing'
             and type(admission['evidenceUpperBoundBytes']) is int
             and 0 < admission['evidenceUpperBoundBytes'] <= 160*1048576, 'whole-evidence-not-admitted')
        # The independently reviewed structural proof must itself be source-pinned.
        proof = admission['proofPin']; need(pins.get(proof['path']) == proof, 'admission-proof-pin'); verify(proof)
        need(type(admission['sourcePins']) is list and len(admission['sourcePins']) >= 15, 'admission-source-closure')
        for source_pin in admission['sourcePins']:
            need(pins.get(source_pin['path']) == source_pin, 'admission-source-binding'); verify(source_pin)
        prerequisites = read(package / 'prerequisites.json')
        need(prerequisites['schema'] == 'm31-state1000-retained-prerequisites-v1'
             and [p['id'] for p in prerequisites['items']] == ['coupled64','native-tree42','saved-layout156'], 'prerequisite-set')
        for item in prerequisites['items']:
            guard()
            for key in ('resultManifestPin','checkPin','attemptPin'):
                need(pins.get(item[key]['path']) == item[key], 'prerequisite-root-pin'); verify(item[key])
            prior_manifest = read(root / item['resultManifestPin']['path'])
            for pin in prior_manifest['files']:
                need(pins.get(pin['path']) == pin, 'prerequisite-closure')
            check = read(root / item['checkPin']['path']); prior_attempt = read(root / item['attemptPin']['path'])
            need(check.get('complete') is True and check.get('passed') is True and prior_attempt.get('status') == 'completed', 'prerequisite-status')
            need(check['sourceCommit'] == prior_attempt['sourceCommit']
                 and check['sourceManifestSha256'] == prior_attempt['sourceManifestSha256'], 'prerequisite-source-binding')
            output['prerequisites'].append({'id':item['id'],'checkPin':item['checkPin'],'attemptPin':item['attemptPin'],
                                           'resultManifestPin':item['resultManifestPin'],'verifiedClosurePins':len(prior_manifest['files']),
                                           'retainedPass':True,'rerun':False})
        output['storageAdmissionPin'] = pins[NAME+'/review/STORAGE-ADMISSION.json']
        output['complete'] = output['passed'] = True
    except Exception as error:
        output['errors'].append({'type':type(error).__name__,'code':str(error) if str(error).replace('-','').isalnum() and len(str(error))<=120 else 'metadata-validation-failure'})
    guard()
    for pin in pins.values(): verify(pin)
    raw = (json.dumps(output,allow_nan=False,separators=(',',':'))+'\n').encode()
    need(len(raw) <= 1048576, 'metadata-report-cap')
    file = package/'results/saved-validation.json'
    with file.open('xb') as stream: stream.write(raw); stream.flush(); os.fsync(stream.fileno())
    fd=os.open(file.parent,os.O_RDONLY)
    try: os.fsync(fd)
    finally: os.close(fd)
    guard()
    return 0 if output['passed'] else 1

if __name__ == '__main__':
    need(len(sys.argv)==4,'usage-root-sha-commit')
    raise SystemExit(main(Path(sys.argv[1]).resolve(),sys.argv[2],sys.argv[3]))
