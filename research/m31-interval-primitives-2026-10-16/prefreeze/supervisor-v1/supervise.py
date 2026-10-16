"""One-shot bounded scientific child supervision. No retries or paid services."""
import argparse, hashlib, json, os, signal, subprocess, sys, time
from pathlib import Path

def sha(b): return hashlib.sha256(b).hexdigest()
def dump(p,x):
    with p.open('x') as f: json.dump(x,f,indent=2); f.write('\n')
def main():
    parser=argparse.ArgumentParser();parser.add_argument('stage',choices=['kernel','checker']);args=parser.parse_args()
    package=Path(__file__).resolve().parents[1];root=package.parents[1]
    manifest_path=package/'source-manifest.json';manifest_bytes=manifest_path.read_bytes();manifest=json.loads(manifest_bytes)
    publication=json.loads((package/'source-publication.json').read_text())
    if publication.get('remoteBytesEqualLocal') is not True or publication.get('manifestSha256')!=sha(manifest_bytes): raise RuntimeError('Source publication gate failed')
    for pin in manifest['files']:
        p=root/pin['path'];b=p.read_bytes()
        if len(b)!=pin['bytes'] or sha(b)!=pin['sha256']: raise RuntimeError('Frozen source pin mismatch')
    resultdir=package/'results';resultdir.mkdir(exist_ok=True)
    if args.stage=='checker':
        previous=json.loads((resultdir/'kernel-supervision.json').read_text())
        if not previous.get('success') or not previous.get('closed'): raise RuntimeError('Kernel stage not qualified for saved checker')
    private=Path(os.environ['RESEARCH_PRIVATE_RUN_DIR']);private.mkdir(parents=True,exist_ok=True)
    attempt=resultdir/(args.stage+'-attempt.json')
    dump(attempt,{'stage':args.stage,'sourceCommit':publication['commit'],'sourceManifestSha256':sha(manifest_bytes),'allocation':'sole attempt; existence prevents retry','startedUtc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())})
    env=os.environ.copy();output=resultdir/('primitive-results.json' if args.stage=='kernel' else 'independent-check.json')
    if args.stage=='kernel':
        command=[env['RESEARCH_NODE'],str(package/'source/run.cjs')];env['RESEARCH_RESULT_PATH']=str(output)
    else:
        command=[sys.executable,str(package/'source/check.py'),'--spec',str(package/'source/spec.json'),'--input',str(resultdir/'primitive-results.json'),'--manifest',str(manifest_path),'--output',str(output),'--root',str(root)]
    stdout=private/(args.stage+'-stdout.raw');stderr=private/(args.stage+'-stderr.raw')
    report={'stage':args.stage,'sourceCommit':publication['commit'],'sourceManifestSha256':sha(manifest_bytes),'wallLimitSeconds':120,'sampledRssLimitBytes':1073741824,'outputLimitBytes':16777216,'pollSeconds':0.1,'success':False,'closed':False,'samples':0,'peakSampledGroupRssBytes':0,'terminationReason':None}
    started=time.monotonic();child=None
    try:
        with stdout.open('xb') as out,stderr.open('xb') as err:
            child=subprocess.Popen(command,cwd=root,env=env,stdout=out,stderr=err,start_new_session=True)
            report['processGroup']=child.pid
            while True:
                rc=child.poll();elapsed=time.monotonic()-started
                table=subprocess.run(['ps','-axo','pid=,pgid=,rss='],capture_output=True,text=True,timeout=2,check=True).stdout
                members=[tuple(map(int,line.split())) for line in table.splitlines() if len(line.split())==3]
                group=[row for row in members if row[1]==child.pid];rss=sum(row[2]*1024 for row in group)
                report['samples']+=1;report['peakSampledGroupRssBytes']=max(report['peakSampledGroupRssBytes'],rss)
                size=sum(p.stat().st_size for p in [stdout,stderr] if p.exists())+sum(p.stat().st_size for p in resultdir.iterdir() if p.is_file())
                reason='wall-limit' if elapsed>120 else 'rss-limit' if rss>1073741824 else 'output-limit' if size>16777216 else 'unexpected-child-process' if any(p[0]!=child.pid for p in group) else None
                if reason:report['terminationReason']=reason;break
                if rc is not None:break
                time.sleep(0.1)
            if child.poll() is None:
                os.killpg(child.pid,signal.SIGTERM)
                try:child.wait(timeout=2)
                except subprocess.TimeoutExpired:os.killpg(child.pid,signal.SIGKILL);child.wait(timeout=2)
            report['exitCode']=child.returncode
    except Exception as e:
        report['terminationReason']='supervisor-'+type(e).__name__
    finally:
        if child is not None:
            try:os.killpg(child.pid,signal.SIGKILL)
            except ProcessLookupError:pass
            try:child.wait(timeout=2)
            except subprocess.TimeoutExpired:pass
            try:os.killpg(child.pid,0);absent=False
            except ProcessLookupError:absent=True
            report['childGroupAbsent']=absent
        else:report['childGroupAbsent']=True
        report['wallSeconds']=time.monotonic()-started
        report['closed']=report['childGroupAbsent']
        report['success']=report.get('exitCode')==0 and report['terminationReason'] is None and report['closed'] and output.exists()
        logs=[]
        for p in [stdout,stderr]:
            if not p.exists():continue
            raw=p.read_bytes();text=raw.decode('utf-8',errors='replace').replace(str(root),'REPOSITORY_ROOT').replace(str(private),'PRIVATE_RUN_DIR').replace(sys.executable,'PYTHON_EXECUTABLE')
            if env.get('RESEARCH_NODE'):text=text.replace(env['RESEARCH_NODE'],'NODE_EXECUTABLE')
            dest=resultdir/(p.stem+'.log');dest.write_text(text)
            logs.append({'path':str(dest.relative_to(root)),'rawBytes':len(raw),'rawSha256':sha(raw),'publishedBytes':dest.stat().st_size,'publishedSha256':sha(dest.read_bytes()),'redaction':'replace repository/private/runtime path prefixes; raw logs retained privately'})
        report['logs']=logs
        if output.exists():report['output']={'path':str(output.relative_to(root)),'bytes':output.stat().st_size,'sha256':sha(output.read_bytes())}
        journal=Path(str(output)+'.jsonl')
        if journal.exists():report['journal']={'path':str(journal.relative_to(root)),'bytes':journal.stat().st_size,'sha256':sha(journal.read_bytes())}
        dump(resultdir/(args.stage+'-supervision.json'),report)
        print(json.dumps({k:report[k] for k in ['stage','success','closed','wallSeconds','peakSampledGroupRssBytes','terminationReason']}))
    return 0 if report['success'] else 1
if __name__=='__main__':sys.exit(main())
