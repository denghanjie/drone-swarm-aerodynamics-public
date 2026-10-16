"""Administrative audit of closed saved evidence. Never imports scientific code."""
import argparse, collections, datetime, hashlib, json, re, subprocess
from fractions import Fraction
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
PKG=Path(__file__).resolve().parents[1]
RES=PKG/'results'
CHECKS=[];ERRORS=[];READS={};INITIAL={}

def sha(b): return hashlib.sha256(b).hexdigest()
def ck(label,actual,expected=True):
    ok=actual==expected and (not isinstance(expected,bool) or type(actual) is bool)
    CHECKS.append({'check':label,'passed':ok})
    if not ok: ERRORS.append({'check':label,'actual':actual,'expected':expected})
    return ok
def rd(p,kind='parsed saved evidence'):
    p=Path(p);b=p.read_bytes();key=str(p.relative_to(ROOT)) if p.is_relative_to(ROOT) else 'PRIVATE/'+p.name
    READS.setdefault(key,set()).add(kind);INITIAL.setdefault(str(p),sha(b));return b
def pin(p):
    p=Path(p);b=rd(p,'hash-only file identity');return {'path':str(p.relative_to(ROOT)),'bytes':len(b),'sha256':sha(b)}
def duplicate_checked(pairs):
    d={}
    for k,v in pairs:
        if k in d:raise ValueError('duplicate saved JSON key:'+k)
        d[k]=v
    return d
def parse(b):return json.loads(b,object_pairs_hook=duplicate_checked)
def doc(p):return parse(rd(p))
def canon(v):return json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False).encode()
def digest(v):return sha(canon(v))
def wire(p,v):ck(str(p.relative_to(PKG))+': canonical saved bytes',rd(p),canon(v)+b'\n')
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT)
def f(v):return Fraction(int(v['n']),int(v['d']))
def fq(v):return {'n':str(v.numerator),'d':str(v.denominator)}
def median(v):v=sorted(v);return (v[1]+v[2])/2

def interval_check(tag,v):
    ck(tag+': canonical nonnegative times',all(type(x) is str and re.fullmatch(r'0|[1-9][0-9]{0,19}',x) for x in v.values()))
    ck(tag+': elapsed',int(v['totalNs']),int(v['endNs'])-int(v['startNs']))
    ck(tag+': ordered',0<=int(v['startNs'])<=int(v['endNs']))

def main(private):
    manifest=doc(PKG/'source-manifest.json');pub=doc(PKG/'source-publication.json');spec=doc(PKG/'source/spec.json');contract=doc(PKG/'source/result-contract.json')
    idx=doc(RES/'timing-index.json');report=doc(RES/'independent-check.json');runtime=doc(PKG/'runtime-pins.json')
    ms=sha(rd(PKG/'source-manifest.json'));ss=sha(rd(PKG/'source/spec.json'));commit=pub['commit']
    ck('manifest pin count',len(manifest['files']),61);ck('manifest duplicate paths',len(set(x['path'] for x in manifest['files'])),61)
    ck('publication local manifest pin',{k:pub[k] for k in ['manifestPath','manifestBytes','manifestSha256']},{'manifestPath':str((PKG/'source-manifest.json').relative_to(ROOT)),'manifestBytes':len(rd(PKG/'source-manifest.json')),'manifestSha256':ms})
    ck('publication recorded remote equality',pub['remoteBytesEqualLocal']);ck('publication committed equality',pub['committedBytesEqualLocal']);ck('publication count',pub['verifiedFilePins'],61)
    ck('publication URL exact-commit manifest',pub['remoteUrl'],f'https://raw.githubusercontent.com/denghanjie/drone-swarm-aerodynamics-public/{commit}/{pub["manifestPath"]}')
    ck('committed manifest bytes',sha(git('show',commit+':'+pub['manifestPath'])),ms)
    ck('manifest Git blob',git('rev-parse',commit+':'+pub['manifestPath']).decode().strip(),pub['manifestGitBlob'])
    ck('source commit parent',git('rev-parse',commit+'^').decode().strip(),manifest['parentCommit'])
    for x in manifest['files']:
        p=ROOT/x['path'];ck('manifest local:'+x['path'],pin(p),x)
        b=git('show',commit+':'+x['path']);ck('manifest Git:'+x['path'],{'bytes':len(b),'sha256':sha(b)},{k:x[k] for k in ['bytes','sha256']})
        ck('manifest canonical path:'+x['path'],p.resolve()==p and not p.is_symlink())
    ck('checker verified all manifest pins',report['verifiedSources'],manifest['files'])
    ck('checker manifest pin',report['sourceManifest'],pin(PKG/'source-manifest.json'))
    ck('checker input pin',report['input'],pin(RES/'timing-index.json'))
    ck('index source manifest',idx['sourceManifestSha256'],ms);ck('index spec hash',idx['specSha256'],ss)
    ck('index spec identity',idx['specId'],spec['id']);ck('constant identity',idx['constants'],report['expectedConstantEncodings'])
    ck('index source hashes',idx['sourceSha256'],{n:sha(rd(PKG/'source'/n,'hash-only file identity')) for n in contract['sourceFiles']})
    wire(RES/'timing-index.json',idx);wire(RES/'independent-check.json',report)
    for key in ['passed','fullQualification','scientificQualification','verificationPassed','tolerancePassed','timingIntegrity','trialDigestConsistency','inputsUnchangedAfter','sourcesUnchangedAfter']:
        ck('checker qualification:'+key,report[key])
    ck('checker errors',report['errors'],[]);ck('checker errorCount',report['errorCount'],0)
    ck('checker record counts',[report[k] for k in ['totalRecords','qualifiedRecords','admittedRecords']],[6]*3)
    ck('checker logical pair totals',[report['expectedPlannedPairsPerMethod'],report['independentCoefficientOutcomes'],report['validatedMethodOutcomes']],[422560,422560,845120])
    ids=[s['id'] for s in spec['scenes']];ck('six exact scene identities',[x['id'] for x in idx['scenes']],ids);ck('checker scene identities',[x['id'] for x in report['scenes']],ids)
    ck('trial count',len(idx['trials']),60)
    journal=[]
    for line in rd(RES/'timing-index.json.jsonl').splitlines(keepends=True):
        ev=parse(line);ck('journal canonical line '+str(len(journal)),line,canon(ev)+b'\n');journal.append(ev)
    ck('journal event count',len(journal),80)
    ck('checker journal pin',report['journal'],{'bytes':len(rd(RES/'timing-index.json.jsonl')),'events':80,'passed':True,'sha256':sha(rd(RES/'timing-index.json.jsonl'))})
    expected_events=[('run-start',{k:idx[k] for k in ['specSha256','sourceManifestSha256','runtime','sourceSha256','constants']})]
    aggregates={name:collections.Counter() for name in spec['methods']};scene_audits=[];references=0;last_end=0
    for si,(scene,descriptor,verified) in enumerate(zip(spec['scenes'],idx['scenes'],report['scenes'])):
        sid=scene['id'];n=len(scene['drones']);p=PKG/descriptor['path'];shard=doc(p);wire(p,shard)
        ck(sid+': scene file pin', {k:descriptor[k] for k in ['path','bytes','sha256']},{'path':str(p.relative_to(PKG)),'bytes':p.stat().st_size,'sha256':sha(rd(p))})
        ck(sid+': shard context',[shard['id'],shard['specId'],shard['specSha256'],shard['sourceManifestSha256']],[sid,spec['id'],ss,ms])
        raw=digest({'domain':contract['encoding']['rawInputDigestDomain'],'sceneId':sid,'input':shard['input']})
        ck(sid+': raw input binding',[shard['rawInputSha256'],descriptor['rawInputSha256']],[raw,raw])
        ck(sid+': raw stable IDs',[d['id'] for d in shard['input']['drones']],[d['id'] for d in scene['drones']])
        conv=descriptor['inputConversionTiming'];interval_check(sid+': conversion',conv);ck(sid+': conversion chronology',int(conv['startNs'])>=last_end)
        expected_events.append(('input-ready',{'sceneIndex':si,'sceneId':sid,'rawInputSha256':raw,'inputConversionTiming':conv}))
        summaries=[];method_data={};common_data=[]
        ck(sid+': methods',[m['name'] for m in shard['methods']],spec['methods'])
        for m,vm in zip(shard['methods'],verified['methods']):
            name=m['name'];a=m['assembly'];w=collections.Counter({k:0 for k in contract['workFields']});w['preparationCalls']=n;w['globalProofs']=1
            tree=a['tree'];nodes=tree['nodes'];perm=tree['permutation'];w['treeNodes']=len(nodes);w['filterPrepared']=n if name=='filtered' else 0
            branches=collections.Counter({b:0 for b in ['neighbor','upstream','down-cut','near-outside','radial','projection']});zero_rules=collections.Counter({b:0 for b in spec['zeroRuleOrder']});positive=[];coverage_ok=True
            ck(sid+'/'+name+': guard passed',a['globalGuard']['passed']);ck(sid+'/'+name+': query identities',[(q['i'],q['r']) for q in a['queries']],[(i,r) for i in range(n) for r in range(4)])
            for q in a['queries']:
                terminals={t['node']:t for t in q['terminals']};seen=[];visit_order=[]
                def visit(nid):
                    node=nodes[nid];w['nodeVisits']+=1
                    if nid in terminals:
                        t=terminals[nid];visit_order.append(nid);members=[j for j,d in enumerate(shard['input']['drones']) if d['id'] in perm[node['start']:node['end']] and j!=q['i']];seen.extend(members)
                        if t['kind']=='zero':
                            w['zeroNodes']+=1;w['zeroPairs']+=t['count'];w['nodeRuleTests']+=spec['zeroRuleOrder'].index(t['rule'])+1;zero_rules[t['rule']]+=1
                            if t['count']!=len(members):return False
                        else:
                            if t['kind']!='leaf' or node['left'] is not None:return False
                            w['nodeRuleTests']+=5;w['leafVisits']+=1;w['scalarPairs']+=len(members);w['scalarZeroPairs']+=t['zeroCount'];entries=t['entries'];zeros=t['filterZeros']
                            if len(entries)+t['zeroCount']!=len(members):return False
                            ej=[e['j'] for e in entries];zj=[z['j'] for z in zeros]
                            if ej!=sorted(set(ej)) or zj!=sorted(set(zj)) or set(ej)&set(zj) or not set(ej+zj)<=set(members):return False
                            if name=='hierarchy' and zeros:return False
                            for e in entries:
                                status=e['result']['status'];w[{'positive':'positiveTerms','rejected':'rejectedPairs','unresolved':'unresolvedPairs'}[status]]+=1
                                if status=='positive':positive.append({'i':q['i'],'r':q['r'],'j':e['j'],'coefficient':e['result']['coefficient']})
                            for z in zeros:branches[z['branch']]+=1
                            w['filterZeros']+=len(zeros)
                        return True
                    w['nodeRuleTests']+=5
                    return visit(node['left']) and visit(node['right'])
                coverage_ok=visit(0) and coverage_ok
                coverage_ok=(len(terminals)==len(q['terminals']) and visit_order==[t['node'] for t in q['terminals']] and sorted(seen)==[j for j in range(n) if j!=q['i']]) and coverage_ok
            w['filterAttempts']=w['scalarPairs'] if name=='filtered' else 0;w['exactScalarCalls']=w['scalarPairs']-w['filterZeros']
            ck(sid+'/'+name+': structural pair and terminal coverage',coverage_ok)
            ck(sid+'/'+name+': work structurally reconstructed',a['work'],dict(w));ck(sid+'/'+name+': saved checker work',vm['work'],dict(w));aggregates[name].update(w)
            ck(sid+'/'+name+': logical pairs',w['scalarPairs']+w['zeroPairs'],4*n*(n-1));ck(sid+'/'+name+': no refused scalar outcomes',w['rejectedPairs']+w['unresolvedPairs'],0)
            ck(sid+'/'+name+': saved zero branches',vm['filterZeroBranchCounts'],dict(branches));ck(sid+'/'+name+': node zero counts',vm['zeroRuleCounts'],dict(zero_rules))
            ck(sid+'/'+name+': checker method totals',[vm['accountedPairs'],vm['positiveCoefficientRecords']],[4*n*(n-1),w['positiveTerms']]);ck(sid+'/'+name+': checker verified',vm['verified'])
            ck(sid+'/'+name+': certified result',m['result'],{'status':'certified','branch':'loads','witness':None,'toleranceAchieved':True})
            maxima={key:max(int(v) for load in m['certificate']['loads'] for v in (load['error'][key] if key=='rotor' else [load['error'][key]])) for key in ['rotor','collective','worldForce','worldMoment']}
            ck(sid+'/'+name+': recorded error maxima',m['certificate']['maxErrors'],{k:str(v) for k,v in maxima.items()});ck(sid+'/'+name+': checker error maxima',vm['maxErrorUppers'],m['certificate']['maxErrors'])
            ck(sid+'/'+name+': all recorded normalized tolerances',all(v*100000000<=2**96 for v in maxima.values()))
            positive.sort(key=lambda e:(e['i'],e['r'],e['j']));common={'prepared':m['prepared'],'result':m['result'],'canonicalPositiveEntries':[dict(e,i=shard['input']['drones'][e['i']]['id'],j=shard['input']['drones'][e['j']]['id']) for e in positive],'solve':m['solve'],'certificate':m['certificate']};common_data.append(common)
            context={'specSha256':ss,'sourceManifestSha256':ms,'sceneId':sid,'rawInputSha256':raw}
            md=digest({'domain':contract['encoding']['methodDigestDomain'],**context,'method':name,'scientific':m});cd=digest({'domain':contract['encoding']['commonDigestDomain'],**context,'scientific':common})
            ck(sid+'/'+name+': checker method digest',verified['methodDigests'][name],md);ck(sid+'/'+name+': checker common digest',verified['commonDigests'][name],cd)
            method_data[name]={'scientificDigest':md,'commonDigest':cd,'work':dict(w)}
        ck(sid+': full common scientific equality',common_data[0]==common_data[1]);ck(sid+': checker method equality',verified['methodEquality']);ck(sid+': checker scene verified',verified['verified'])
        ck(sid+': fixed first measured representatives',descriptor['representatives'],[dict(method=name,trialSequence=si*10+2+k,scientificDigest=method_data[name]['scientificDigest'],commonDigest=method_data[name]['commonDigest']) for k,name in enumerate(spec['methods'])])
        scene_trials=idx['trials'][si*10:si*10+10]
        for local,t in enumerate(scene_trials):
            pair=local//2;pos=local%2;order=['AB','AB','BA','BA','AB'][pair];name={'A':'hierarchy','B':'filtered'}[order[pos]];tag='trial'+str(si*10+local)
            ck(tag+': schedule',[t[k] for k in ['sequence','sceneIndex','sceneId','phase','repetition','pairOrder','pairPosition','method']],[si*10+local,si,sid,'warmup' if pair==0 else 'measured',pair,order,pos,name])
            ck(tag+': method/common/work binding',{k:t[k] for k in method_data[name]},method_data[name])
            tm=t['timing'];interval_check(tag,{k:tm[k] for k in ['startNs','endNs','totalNs']});o={k:int(v) for k,v in tm['offsetsNs'].items()};st={k:int(v) for k,v in tm['stagesNs'].items()}
            ck(tag+': offset order',0<=o['prepared']<=o['spatial']<=o['assembled']<=o['completed']);ck(tag+': offset completion',o['completed'],int(tm['totalNs']))
            ck(tag+': stage partition',st,{'preparation':o['prepared'],'spatial':o['spatial']-o['prepared'],'assembly':o['assembled']-o['spatial'],'admissionSolveCertificate':o['completed']-o['assembled']})
            ck(tag+': method chronological',int(tm['startNs'])>=max(last_end,int(conv['endNs'])) and int(tm['totalNs'])>0)
            h=t['harnessTiming'];interval_check(tag+': harness',{k:h[k] for k in ['startNs','endNs','totalNs']});ck(tag+': harness partition',int(h['serializationNs'])+int(h['hashNs']),int(h['totalNs']));ck(tag+': harness chronology',int(h['startNs'])>=int(tm['endNs']) and min(int(h['serializationNs']),int(h['hashNs']))>=0);last_end=int(h['endNs'])
            expected_events.append(('trial-complete',t))
            if local==3:expected_events.append(('representative-shard',descriptor))
        expected_events.append(('scene-complete',{'sceneIndex':si,'sceneId':sid,'firstSequence':si*10,'lastSequence':si*10+9,'sha256':descriptor['sha256']}))
        pairs=[]
        for rep in range(1,5):
            ts={t['method']:t for t in scene_trials if t['repetition']==rep};a=int(ts['hierarchy']['timing']['totalNs']);b=int(ts['filtered']['timing']['totalNs']);pairs.append({'repetition':rep,'pairOrder':ts['hierarchy']['pairOrder'],'hierarchyNs':str(a),'filteredNs':str(b),'ratio':fq(Fraction(b,a))})
        hm=median([Fraction(int(p['hierarchyNs'])) for p in pairs]);fm=median([Fraction(int(p['filteredNs'])) for p in pairs]);mr=median([f(p['ratio']) for p in pairs]);wins=sum(int(p['filteredNs'])<int(p['hierarchyNs']) for p in pairs)
        summary={'sceneId':sid,'pairs':pairs,'hierarchyMedianNs':fq(hm),'filteredMedianNs':fq(fm),'medianPairedRatio':fq(mr),'ratioOfMedians':fq(fm/hm),'winCount':wins,'practicalBenefitPassed':mr<=Fraction(9,10) and wins>=3}
        ck(sid+': exact timing summary',idx['summaries'][si],summary);ck(sid+': independent summary',report['timingSummaries'][si],summary)
        refpin=verified['referenceEvidence'];rp=RES/refpin['path'];ref=doc(rp);wire(rp,ref);ck(sid+': reference pin',{'path':refpin['path'],'bytes':rp.stat().st_size,'sha256':sha(rd(rp))},refpin);references+=rp.stat().st_size
        ck(sid+': reference context',[ref['sceneId'],ref['rawInputSha256'],ref['plannedPairsPerMethod']],[sid,raw,4*n*(n-1)]);ck(sid+': reference IDs',[x['id'] for x in ref['independentReference']],[x['id'] for x in shard['input']['drones']])
        scene_audits.append({'sceneId':sid,'family':scene['family'],'drones':n,'summary':summary,'work':{name:method_data[name]['work'] for name in spec['methods']}})
    primary=all(s['summary']['practicalBenefitPassed'] for s in scene_audits if s['family']=='dense');ck('dense count',sum(s['family']=='dense' for s in scene_audits),3);ck('primary benefit',idx['primaryBenefitPassed'],primary);ck('checker primary benefit',report['primaryBenefitPassed'],primary)
    ck('reference evidence byte total',report['referenceEvidenceBytes'],references)
    resultpin=pin(RES/'timing-index.json');expected_events.append(('run-complete',{'resultPath':str((RES/'timing-index.json').relative_to(PKG)),'resultBytes':resultpin['bytes'],'resultSha256':resultpin['sha256'],'trialCount':60,'sceneCount':6}))
    for seq,(event,(typ,payload)) in enumerate(zip(journal,expected_events)):
        ck('journal'+str(seq)+': full event binding',event,{'schema':contract['journal']['schema'],'eventSequence':seq,'type':typ,'payload':payload})
    controls=report['faultControls'];recipes=contract['controls']['recipes'];ck('control count',len(controls),18);ck('control names',[x['name'] for x in controls],[x['name'] for x in recipes])
    for c,r in zip(controls,recipes):
        tag='control:'+c['name'];ck(tag+': flags',[c[k] for k in ['executed','rejected','intendedCoreFailure']],[True]*3);ck(tag+': failure families',c['requiredFailureFamilies'],r['failurePrefixes']);ck(tag+': actual intended failure',bool(c['errors']) and any(any(e.startswith(prefix) for prefix in r['failurePrefixes']) for e in c['errors']));ck(tag+': retained witness',bool(c['witness']));ck(tag+': witness size',len(canon(c['witness']))<=contract['wireLimits']['controlWitnessBytes'])
    supervis={stage:doc(RES/(stage+'-supervision.json')) for stage in ['kernel','checker']};attempts={stage:doc(RES/(stage+'-attempt.json')) for stage in supervis};M=1024*1024
    for stage,s in supervis.items():
        for key in ['success','closed','childGroupAbsent','sourceAndRuntimeRechecked','scientificChildAbsentBeforeRelease']:ck(stage+': '+key,s[key])
        ck(stage+': exits',[s['exitCode'],s['guardianExitCode']],[0,0]);ck(stage+': termination',s['terminationReason'],None);ck(stage+': source context',[s['sourceCommit'],s['sourceManifestSha256']],[commit,ms]);ck(stage+': runtime pins',s['runtimePins'],runtime)
        ck(stage+': limits',[s['wallLimitSeconds'],s['guardianWallLimitSeconds'],s['sampledRssLimitBytes'],s['outputLimitBytes'],s['logMetadataLimitBytes'],s['finalReportLimitBytes']],[600,610,1024*M,768*M,16*M,65536]);ck(stage+': measured limits',0<s['wallSeconds']<=600 and s['peakSampledGroupRssBytes']<=1024*M and s['samples']>0)
        ck(stage+': stage attempt',[attempts[stage]['stage'],attempts[stage]['sourceCommit'],attempts[stage]['sourceManifestSha256']],[stage,commit,ms])
        events=[parse(l) for l in rd(RES/(stage+'-guardian.jsonl')).splitlines()];ck(stage+': guardian sequence',[e['event'] for e in events],['child-start','child-exit']);ck(stage+': guardian group',events[0]['guardian'],s['processGroup']);ck(stage+': guardian direct child exit',[events[1]['pid'],events[1]['exitCode']],[events[0]['pid'],0])
        for x in s['scientificEvidence']+s.get('checkerEvidence',[])+[s['output']]+([s['journal']] if 'journal' in s else []):ck(stage+': evidence '+x['path'],pin(ROOT/x['path']),x)
        ck(stage+': no anomaly',s['anomalyEvidence'],[])
        ck(stage+': private directory identity',sha(str(private.resolve()).encode()),s['privateLogDirectorySha256'])
        for x in s['privateRawLogs']:
            raw=rd(private/x['name'],'private raw log identity');ck(stage+': raw '+x['name'],{'name':x['name'],'bytes':len(raw),'sha256':sha(raw)},x)
        for x in s['logs']:
            pp=ROOT/x['path'];rawp=private/(pp.stem+'.raw');raw=rd(rawp,'private raw log identity');published=rd(pp)
            ck(stage+': raw/public log pin '+pp.name,[len(raw),sha(raw),len(published),sha(published)],[x['rawBytes'],x['rawSha256'],x['publishedBytes'],x['publishedSha256']]);ck(stage+': raw/public equality for path-free saved log '+pp.name,raw,published)
        ac=s['outputAccountingBeforeReport'];ck(stage+': accounting violations',ac['violations'],[]);ck(stage+': accounting aggregate',sum(x['bytes'] for x in ac['files']),ac['aggregateBytes']);ck(stage+': before-report total',s['finalOutputBytesBeforeReport'],ac['aggregateBytes'])
        for entry in ac['files']:
            p=(RES if entry['scope']=='results' else private)/entry['path'];ck(stage+': accounting size '+entry['scope']+'/'+entry['path'],p.stat().st_size,entry['bytes'])
        ck(stage+': accounting category sum',sum(ac[k] for k in ['indexBytes','journalBytes','scientificShardBytes','checkerBytes','logMetadataBytes','reportBytes','unclassifiedBytes']),ac['aggregateBytes'])
        ck(stage+': accounting caps',ac['aggregateBytes']+65536<=768*M and ac['scientificShardBytes']<=384*M and ac['checkerBytes']<=128*M and ac['logMetadataBytes']<=16*M and ac['indexBytes']<=8*M and ac['journalBytes']<=8*M)
    ck('stable science across stages',supervis['kernel']['scientificEvidence'],supervis['checker']['scientificEvidence'])
    ck('checker prior raw logs',[x for x in supervis['checker']['privateRawLogs'] if x['name'].startswith('kernel-')],supervis['kernel']['privateRawLogs'])
    date=lambda x:datetime.datetime.fromisoformat(x.replace('Z','+00:00'))
    ck('publication precedes allocations',date(manifest['frozenUtc'])<=date(pub['verifiedUtc'])<date(attempts['kernel']['startedUtc'])<date(attempts['checker']['startedUtc']))
    ck('checker starts after kernel wall interval',date(attempts['checker']['startedUtc'])>=date(attempts['kernel']['startedUtc'])+datetime.timedelta(seconds=supervis['kernel']['wallSeconds']))
    expected={'timing-index.json','timing-index.json.jsonl','independent-check.json'}|{f'{d}/{sid}.json' for d in ['scenes','reference-scenes'] for sid in ids}|{stage+suffix for stage in supervis for suffix in ['-attempt.json','-guardian.jsonl','-stdout.log','-stderr.log','-supervision.json']}
    actual={str(p.relative_to(RES)) for p in RES.rglob('*') if p.is_file()};ck('closed result file set',sorted(actual),sorted(expected));ck('private file set',sorted(p.name for p in private.iterdir()),sorted(stage+'-'+stream+'.raw' for stage in supervis for stream in ['stdout','stderr']))
    ck('no output symlinks',all(not p.is_symlink() for p in RES.rglob('*')) and all(not p.is_symlink() for p in private.iterdir()))
    ck('closed result directory set',sorted(str(p.relative_to(RES)) for p in RES.rglob('*') if p.is_dir()),['anomalies','reference-scenes','scenes'])
    total=sum((RES/n).stat().st_size for n in actual)+sum(p.stat().st_size for p in private.iterdir());ck('final aggregate cap',total<=768*M);ck('final accounting after report',total,supervis['checker']['finalOutputBytesBeforeReport']+(RES/'checker-supervision.json').stat().st_size)
    ck('all scene shard caps',all((RES/'scenes'/f'{sid}.json').stat().st_size<=128*M for sid in ids));ck('short report caps',all((RES/(stage+'-supervision.json')).stat().st_size<=65536 for stage in supervis))
    ck('final stored totals match categories',sum((RES/'scenes'/f'{sid}.json').stat().st_size for sid in ids),supervis['checker']['outputAccountingBeforeReport']['scientificShardBytes'])
    for p,h in INITIAL.items():ck('audit inputs unchanged:'+('PRIVATE/'+Path(p).name if not Path(p).is_relative_to(ROOT) else str(Path(p).relative_to(ROOT))),sha(Path(p).read_bytes()),h)
    return {'sourceCommit':commit,'sourceManifestSha256':ms,'sourcePins':61,'scenes':scene_audits,'aggregateWorkPerOneCallPerScene':{k:dict(v) for k,v in aggregates.items()},'measuredPairWins':sum(s['summary']['winCount'] for s in scene_audits),'primaryBenefitPassed':primary,'controls':[{k:c[k] for k in ['name','executed','rejected','intendedCoreFailure','errors','requiredFailureFamilies']} for c in controls],'closedStages':{k:{key:s[key] for key in ['wallSeconds','samples','peakSampledGroupRssBytes','maxSampleGapSeconds','success','closed']} for k,s in supervis.items()},'finalRetainedOutputBytes':total,'scientificShardBytes':supervis['checker']['outputAccountingBeforeReport']['scientificShardBytes'],'checkerCorpusBytes':supervis['checker']['outputAccountingBeforeReport']['checkerBytes'],'trialCount':60,'journalEvents':80,'referenceFiles':6}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--private-dir',required=True);args=ap.parse_args();facts={}
    try:facts=main(Path(args.private_dir))
    except Exception as e:ERRORS.append({'check':'audit execution','exceptionType':type(e).__name__,'detail':str(e)})
    output={'schema':'m31-filter-cost-saved-evidence-audit-v1','scope':'Administrative saved-evidence reconciliation only. No model/checker import or execution, numerical oracle replay, new timing allocation, browser action or remote fetch. Structural work is reconstructed from recorded terminal membership/traversal, not recomputed geometry. Remote verification is a recorded receipt; local/Git source bytes are independently rechecked.','passed':not ERRORS,'checkCount':len(CHECKS),'failedCheckCount':sum(not c['passed'] for c in CHECKS),'errorCount':len(ERRORS),'errors':ERRORS,'facts':facts,'checks':CHECKS,'readingDisclosure':{'newInheritedContentReads':0,'priorCurrentCycleInheritedContentCount':5,'conservativePriorCountIncludingCopiedCurrentSources':10,'freshInheritedContentCap':16,'note':'Historical manifest pins are read as opaque bytes solely for SHA256/Git identity and are not decoded, interpreted or imported. Full parsed content reads in this allocation are current-package saved evidence and frozen metadata only. Private log bytes are compared but not published.','paths':[{'path':k,'uses':sorted(v)} for k,v in sorted(READS.items())]},'scriptSha256':sha(Path(__file__).read_bytes())}
    out=PKG/'review/SAVED-EVIDENCE-AUDIT.json';out.write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({'passed':output['passed'],'checkCount':len(CHECKS),'errorCount':len(ERRORS),'errors':ERRORS,'facts':{k:v for k,v in facts.items() if k not in ['scenes','controls','aggregateWorkPerOneCallPerScene']}}))
