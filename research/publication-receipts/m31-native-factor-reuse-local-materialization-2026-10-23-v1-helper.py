"""Prospective OS hydration for one exact Git pack and six exact input paths.

This administrative helper neither reads pack contents nor invokes Git. A cleared
dataless flag is a momentary metadata observation, not byte identity verification.
The OS transfer can outlive this bounded request/polling process.
"""
from pathlib import Path
import argparse
import hashlib
import json
import os
import re
import selectors
import signal
import subprocess
import sys
import time

TASK_START=time.monotonic()
ROOT=Path(__file__).resolve().parents[2]
COMMON=ROOT.parent/'drone-swarm-aerodynamics-public' / '.git'
PREFIX='research/publication-receipts/m31-native-factor-reuse-local-materialization-2026-10-23-v1'
HELPER=PREFIX+'-helper.py'
PROTOCOL=PREFIX+'-protocol.json'
PACK_REL='objects/pack/pack-4aa67c7e8b930735fe1b240a91415d6f8ac5d1f6.pack'
PACK=COMMON/PACK_REL
PACK_BYTES=424593415
SOURCE='7e6ab5b1d3bb819a7a17178c9a5636bde49ca6f2'
REL='research/m31-native-factor-reuse-2026-10-23'
BOUNDS=dict(overallSeconds=360,activationSeconds=10,activationAttemptsPerTarget=1,maxActivationAttempts=7,
    pollingSeconds=300,pollCadenceSeconds=15,maxPollObservations=21,
    metadataSeconds=3,closureReserveSeconds=30,maxCapturedBytes=262144,maxEvidenceBytes=2097152)
TARGETS=[dict(id='git-pack',kind='git-pack',commonGitDirSibling='drone-swarm-aerodynamics-public/.git',relativePath=PACK_REL,bytes=PACK_BYTES)]
for number,digest in ((0,'079b27f80012b61a5b7da88d23604c617b290cc60c98b73c62d3f00cf2b75793'),(1,'32dc050281d8822ddb5b94710b68fac5fb7ad70eeab13a24bdb369038164ce81'),(3,'e44877bab0936c31aab556a39a0151855ec316d13ce6c233db9ceae5ec9fdc86'),(4,'36cbf56cc311de3a453254c0637cd213d047a47dafe5a8c0f01d6a35685838f4')):
    TARGETS.append(dict(id='input-part'+str(number).zfill(3),kind='input',relativePath='research/m31-buffered-motion-2026-10-22/transport/selected.jsonl.gz.part'+str(number).zfill(3),bytes=33554432,sha256=digest))
TARGETS.extend([dict(id='neighbor-stages',kind='input',relativePath='research/m31-neighbor-density-2026-10-23/results/stages.jsonl',bytes=9063908,sha256='8098f5d2478b9a7f7184ed34f5df41199b565f969e9691ad9099ee6f3e48c1c3'),dict(id='radial-audit',kind='input',relativePath='research/m31-radial-integration-2026-10-23/audit/audit.json',bytes=3378809,sha256='59ab04097ac11731e3f978b164c32f3db863a1a3be218e5e55fbb80ddff28017')])
JXA=r'''ObjC.import('Foundation');
function run(argv) {
  try {
    if (argv.length !== 1) throw new Error('exactly-one-target-required');
    var manager = $.NSFileManager.defaultManager;
    var url = $.NSURL.fileURLWithPath($(argv[0]));
    var error = Ref();
    var accepted = Boolean(manager.startDownloadingUbiquitousItemAtURLError(url, error));
    var result = {accepted: accepted, api: 'NSFileManager.startDownloadingUbiquitousItemAtURL:error:'};
    if (!accepted) {
      result.reason = 'system-api-rejected-request';
      try { result.errorDomain = ObjC.unwrap(error[0].domain); result.errorCode = Number(error[0].code); result.errorDescription = ObjC.unwrap(error[0].localizedDescription); }
      catch (ignored) { result.errorDescription = 'NSError unavailable'; }
    }
    return JSON.stringify(result);
  } catch (error) {
    return JSON.stringify({accepted: false, reason: 'unsupported-or-failed-system-api', errorDescription: String(error)});
  }
}'''

def need(value,label):
    if not value: raise AssertionError(label)

def identity(raw): return dict(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())

def small_local_read(name,cap=1048576):
    # Only small administrative records; input and pack payloads are never read.
    need(type(name) is str and name and not Path(name).is_absolute() and '..' not in Path(name).parts,'safe-administrative-path')
    need(type(cap) is int and 0<=cap<=1048576,'small-administrative-read-cap')
    seconds=min(5,BOUNDS['overallSeconds']-(time.monotonic()-TASK_START));need(seconds>0,'overall-bound-before-local-read')
    code="import pathlib,sys; r=pathlib.Path(sys.argv[1]); p=r/sys.argv[2]; n=int(sys.argv[3]); assert p.is_file() and not p.is_symlink() and p.resolve().is_relative_to(r); f=p.open('rb'); b=f.read(n+1); assert len(b)<=n; sys.stdout.buffer.write(b)"
    got=subprocess.run([sys.executable,'-c',code,str(ROOT),name,str(cap)],stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=seconds,env={'PATH':'/usr/bin:/bin','LC_ALL':'C'})
    need(got.returncode==0,'bounded-small-administrative-read:'+name);return got.stdout

def read_pin(pin):
    need(set(pin)=={'file','bytes','sha256'},'exact-file-pin')
    name=pin['file'];need(type(name) is str and name and not Path(name).is_absolute() and '..' not in Path(name).parts,'safe-pin-path')
    raw=small_local_read(name,pin['bytes']);need(identity(raw)=={k:pin[k] for k in ('bytes','sha256')},'unchanged-pinned-file:'+name);return raw

def clean(value):
    return str(value).replace(str(ROOT),'[repository]').replace(str(COMMON),'[shared-git-directory]')[:2000]

def absent_allocations():
    paths=[]
    for phase in ('producer','audit','finalize','ui'):
        paths.extend([REL+'/'+phase+'-supervisor-launch.lock',REL+'/'+phase+'-supervisor.json',REL+'/'+('results' if phase=='producer' else phase)])
    paths.append(REL+'/viewer/pins.json')
    seconds=min(5,BOUNDS['overallSeconds']-(time.monotonic()-TASK_START));need(seconds>0,'overall-bound-before-allocation-check')
    code="import json,pathlib,sys; r=pathlib.Path(sys.argv[1]); paths=json.loads(sys.argv[2]); print(json.dumps([p for p in paths if (r/p).exists()]))"
    got=subprocess.run([sys.executable,'-c',code,str(ROOT),json.dumps(paths)],stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=seconds,env={'PATH':'/usr/bin:/bin','LC_ALL':'C'})
    need(got.returncode==0 and json.loads(got.stdout)==[],'all-scientific-and-display-allocations-must-remain-unstarted')
    return dict(state='all-unstarted',absentPaths=paths)

class Attempt:
    def __init__(self,protocol_hash):
        self.start=TASK_START;self.captured=0;self.events=[];self.protocol_raw=small_local_read(PROTOCOL)
        need(identity(self.protocol_raw)['sha256']==protocol_hash,'exact-reviewed-protocol-hash')
        self.protocol=json.loads(self.protocol_raw);p=self.protocol
        need(p['schema']=='m31-seven-target-os-materialization-v1' and p['status']=='reviewed-ready' and p['reviewed'] is True,'independent-review-required')
        need(p['bounds']==BOUNDS and p['sourceCommit']==SOURCE and p['outputPrefix']==PREFIX,'fixed-scope-and-bounds')
        need(p['targets']==TARGETS,'exact-seven-targets-only')
        need(p['api']=='NSFileManager.startDownloadingUbiquitousItemAtURL:error:' and p['executionPermission']=='require_escalated','fixed-system-api-and-permission')
        need(p['jxa']==identity(JXA.encode()),'exact-reviewed-JXA-script')
        read_pin(p['helper']);need(p['helper']['file']==HELPER,'exact-helper-path')
        read_pin(p['independentReviewPin'])
        for pin in p['preservedEvidence']:read_pin(pin)
        manifest=json.loads(read_pin(p['sourceManifest']));entries={x['path']:x for x in manifest['files']}
        for target in TARGETS[1:]:need({k:entries[target['relativePath']][k] for k in ('bytes','sha256')}=={k:target[k] for k in ('bytes','sha256')},'exact-manifest-input-descriptor')
        need(small_local_read('.git',4096).decode().strip()=='gitdir: '+str(COMMON/'worktrees/drone-swarm-m31-checkpoint'),'exact-shared-Git-directory')
        self.receipt=ROOT/(PREFIX+'.json');self.journal=ROOT/(PREFIX+'-events.jsonl');lock=ROOT/(PREFIX+'-launch.lock')
        need(not any(x.exists() for x in (self.receipt,self.journal,lock,self.receipt.with_suffix('.writing'))),'single-use-hydration-output-namespace')
        with lock.open('x') as f:f.write('one OS hydration request per exact target; no retry; OS may continue independently\n');f.flush();os.fsync(f.fileno())
        self.journal.touch(exist_ok=False)
        self.result=dict(schema='m31-seven-target-os-materialization-closure-v1',closed=False,passed=False,protocol=dict(file=PROTOCOL,**identity(self.protocol_raw)),helper=p['helper'],sourceCommit=SOURCE,targets=p['targets'],bounds=BOUNDS,events=self.events,activationAttempts=0,activationByTarget={},pollObservations=0,networkToolsInvoked=0,gitCommands=0,scientificQueries=0,packContentRead=False,scientificContentRead=False,scientificArchivesDecoded=False,sourceGateAdvanced=False,publicationAttempted=False,osBackgroundTransferMayContinue=True,contentIdentityVerified=False,residencyGuaranteed=False)
        self.save()
    def target_path(self,target):return (COMMON if target['kind']=='git-pack' else ROOT)/target['relativePath']
    def left(self):
        value=BOUNDS['overallSeconds']-(time.monotonic()-self.start);need(value>0,'overall-administrative-wall-bound');return value
    def save(self):
        self.result.update(wallSeconds=time.monotonic()-self.start,capturedBytes=self.captured)
        raw=json.dumps(self.result,ensure_ascii=False,indent=2,allow_nan=False).encode()+b'\n'
        need(len(raw)+(self.journal.stat().st_size if self.journal.exists() else 0)<=BOUNDS['maxEvidenceBytes'],'bounded-administrative-evidence')
        temp=self.receipt.with_suffix('.writing')
        with temp.open('wb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
        os.replace(temp,self.receipt)
    def event(self,value):
        event=dict(event=len(self.events)+1,elapsedSeconds=time.monotonic()-self.start,**value)
        raw=json.dumps(event,ensure_ascii=False,allow_nan=False,separators=(',',':')).encode()+b'\n'
        need(len(raw)<16384,'bounded-event')
        with self.journal.open('ab') as f:f.write(raw);f.flush();os.fsync(f.fileno())
        self.events.append(event);self.save();return event
    def command(self,operation,args,limit):
        seconds=min(limit,self.left());intent=self.event(dict(kind='command-intent',operation=operation,secondsBound=seconds))
        process=None;selector=selectors.DefaultSelector();out=bytearray();err=bytearray();begin=time.monotonic();code=None;failure=None
        env={'PATH':'/usr/bin:/bin:/usr/sbin:/sbin','LC_ALL':'C','HOME':os.environ.get('HOME','')}
        try:
            process=subprocess.Popen(args,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=env,cwd=ROOT,start_new_session=True)
            for stream,label in ((process.stdout,'stdout'),(process.stderr,'stderr')):
                os.set_blocking(stream.fileno(),False);selector.register(stream,selectors.EVENT_READ,label)
            while selector.get_map():
                left=seconds-(time.monotonic()-begin);need(left>0,'bounded-child-timeout')
                for key,_ in selector.select(min(.2,left)):
                    remain=BOUNDS['maxCapturedBytes']-self.captured-len(out)-len(err);need(remain>0,'aggregate-child-capture-cap')
                    raw=os.read(key.fileobj.fileno(),min(65536,remain))
                    if not raw:selector.unregister(key.fileobj);continue
                    (out if key.data=='stdout' else err).extend(raw)
            code=process.wait(timeout=max(.001,seconds-(time.monotonic()-begin)))
        except BaseException as error:
            failure=error
            if process and process.poll() is None:
                os.killpg(process.pid,signal.SIGKILL);process.wait(timeout=2)
            code=None if process is None else process.returncode
        finally:
            selector.close()
            if process:process.stdout.close();process.stderr.close()
        self.captured+=len(out)+len(err)
        record=dict(kind='command-result',operation=operation,intentEvent=intent['event'],wallSeconds=time.monotonic()-begin,exitCode=code,stdout=identity(out),stderr=identity(err),stdoutText=clean(out.decode('utf8','replace')),stderrText=clean(err.decode('utf8','replace')))
        if failure:record['failure']=dict(type=type(failure).__name__,detail=clean(failure))
        self.event(record)
        if failure:raise failure
        need(code==0,'command-exit-failure:'+operation)
        return bytes(out)
    def metadata(self,target,operation,limit=None):
        raw=self.command(operation,['/usr/bin/stat','-f','%z\t%f\t%Sf\t%HT',str(self.target_path(target))],BOUNDS['metadataSeconds'] if limit is None else min(BOUNDS['metadataSeconds'],limit))
        fields=raw.decode('utf8').strip().split('\t');need(len(fields)==4 and fields[0].isdigit(),'exact-pack-stat-shape')
        size,flags,text,kind=fields;need(int(size)==target['bytes'] and kind=='Regular File','exact-target-size-and-type')
        need(re.fullmatch(r'[A-Za-z0-9_, -]+',text),'bounded-readable-file-flags')
        names=[x.strip() for x in text.split(',')]
        result=dict(target=target['id'],bytes=int(size),flagsNumeric=flags,flagsText=text,dataless='dataless' in names,observedAtElapsedSeconds=time.monotonic()-self.start)
        self.event(dict(kind='metadata-observation',operation=operation,metadata=result));return result
    def run(self):
        phase='initial-boundary'
        try:
            self.result['allocationBoundaryStart']=absent_allocations();phase='initial-metadata';initial={t['id']:self.metadata(t,'initial-'+t['id']) for t in TARGETS};self.result['initialMetadata']=initial
            self.result['latestMetadata']=dict(initial)
            pending=[t for t in TARGETS if initial[t['id']]['dataless']]
            for target in pending:
                phase='one-system-api-activation:'+target['id'];need(target['id'] not in self.result['activationByTarget'],'no-activation-retry')
                self.result['activationAttempts']+=1;self.result['activationByTarget'][target['id']]=dict(outcome='unknown');self.save()
                output=self.command('activate-'+target['id'],['/usr/bin/osascript','-l','JavaScript','-e',JXA,str(self.target_path(target))],BOUNDS['activationSeconds'])
                response=json.loads(output);need(type(response) is dict and type(response.get('accepted')) is bool,'system-api-JSON-shape')
                self.result['activationByTarget'][target['id']]={k:clean(v) if type(v) is str else v for k,v in response.items()};self.save()
                need(response['accepted'] is True,'system-api-unsupported-or-rejected-stop-without-polling')
            if pending:
                phase='bounded-flags-polling';poll_start=time.monotonic();deadline=poll_start+min(BOUNDS['pollingSeconds'],self.left()-BOUNDS['closureReserveSeconds'])
                for index in range(BOUNDS['maxPollObservations']):
                    scheduled=poll_start+index*BOUNDS['pollCadenceSeconds'];remaining=deadline-time.monotonic()
                    if remaining<=0:break
                    delay=scheduled-time.monotonic()
                    if delay>0:time.sleep(min(delay,remaining))
                    remaining=deadline-time.monotonic()
                    if remaining<=0:break
                    self.left()
                    for target in pending:
                        remaining=deadline-time.monotonic();need(remaining>0,'global-polling-budget')
                        observed=self.metadata(target,'poll-'+str(index+1)+'-'+target['id'],remaining);self.result['latestMetadata'][target['id']]=observed
                    self.result['pollObservations']+=1;self.save()
                    pending=[t for t in pending if self.result['latestMetadata'][t['id']]['dataless']]
                    if not pending:break
                need(not pending,'polling-budget-exhausted-without-local-readiness')
            self.result['readiness']='all-seven-not-dataless-at-latest-observations'
        except BaseException as error:self.result['failure']=dict(phase=phase,type=type(error).__name__,detail=clean(error))
        finally:
            try:
                need(small_local_read(PROTOCOL)==self.protocol_raw,'protocol-unchanged-at-closure')
                read_pin(self.protocol['helper']);read_pin(self.protocol['independentReviewPin'])
                read_pin(self.protocol['sourceManifest'])
                for pin in self.protocol['preservedEvidence']:read_pin(pin)
                self.result['allocationBoundaryEnd']=absent_allocations()
                need(self.result['allocationBoundaryEnd']==self.result.get('allocationBoundaryStart'),'allocation-boundary-unchanged')
                if self.result.get('readiness'):
                    self.result['closureMetadata']={t['id']:self.metadata(t,'closure-'+t['id']) for t in TARGETS}
                    need(all(not x['dataless'] for x in self.result['closureMetadata'].values()),'target-became-dataless-again-before-closure')
            except BaseException as error:self.result['closureFailure']=dict(type=type(error).__name__,detail=clean(error))
            self.result['wallCapPassed']=time.monotonic()-self.start<=BOUNDS['overallSeconds']
            self.result['passed']=self.result.get('readiness')=='all-seven-not-dataless-at-latest-observations' and self.result['wallCapPassed'] and not any(k in self.result for k in ('failure','closureFailure'))
            self.result['closed']=True;self.result['eventJournal']=dict(file=PREFIX+'-events.jsonl',**identity(self.journal.read_bytes()));self.save()
        need(self.result['passed'],'seven-target-materialization-failed-retained')

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--protocol-sha256',required=True);args=parser.parse_args()
    need(re.fullmatch(r'[0-9a-f]{64}',args.protocol_sha256),'exact-protocol-SHA256')
    def interrupted(number,frame):raise InterruptedError('administrative-hydration-interrupted:'+str(number))
    for number in (signal.SIGTERM,signal.SIGINT):signal.signal(number,interrupted)
    Attempt(args.protocol_sha256).run()

if __name__=='__main__':main()
