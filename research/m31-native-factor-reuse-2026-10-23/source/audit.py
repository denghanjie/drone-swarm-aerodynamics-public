"""Saved-evidence audit only. Never import or invoke a numerical model/fixture.

Infrastructure only is imported from common.py. Normalization, control reconstruction,
archive bindings, paired payloads, timings and CSR accounting are implemented here.
Identity/provenance architecture was adapted as source text from the radial-integration
and phase-attribution auditors; their numerical modules are never imported.
"""
from pathlib import Path
import copy
import gzip
import hashlib
import io
import json
import math
import re
import struct
import sys
import time
import traceback
import common as infrastructure

BASE=Path(__file__).resolve().parent.parent
ROOT=BASE.parent.parent
REL=BASE.relative_to(ROOT).as_posix()
OLD='research/m31-buffered-motion-2026-10-22'
PRIOR='research/m31-radial-integration-2026-10-23'
DENSITY='research/m31-neighbor-density-2026-10-23'
PHASE='research/m31-phase-attribution-2026-10-23'
EXCLUSIONS=['method','timing','diagnostics.buildPhasesMs','diagnostics.geometryWork.gatheredNonselfCandidates','diagnostics.screen.orderedPairVisits','diagnostics.screen.componentTests','caseId','semanticInputSha256','inlineInputCanonicalSha256']
PAIR_EXCLUSIONS=['timing','diagnostics.buildPhasesMs']
WORK=EXCLUSIONS[3:6]
SCOPE='native query-local factor reuse on exposed dependent N64 saved states; no novelty, physical validity, full-flight or scaling claim'
CASE_IDS=['seed2026102101-original-h0025','seed2026102101-memory-h0025','seed2026102102-original-h0025','seed2026102102-memory-h0025']
TOTAL=[5792,8000,8000,8000]
WINDOWS=[dict(window=3*c+w,caseId=case,start=start,length=160) for c,case in enumerate(CASE_IDS) for w,start in enumerate((0,4000,TOTAL[c]-160))]
SHA=re.compile('[0-9a-f]{64}');WORD=re.compile('[0-9a-f]{16}')
PINS={};CHECKS=[];OUT=None

def need(condition,label):
    if not condition:raise AssertionError(label)

def sha(raw):return hashlib.sha256(raw).hexdigest()
def word(value):return struct.pack('>d',float(value)).hex()
def number(value):
    need(type(value) is str and WORD.fullmatch(value),'binary64-word')
    return struct.unpack('>d',bytes.fromhex(value))[0]
def finite(value):
    need(type(value) in (int,float) and math.isfinite(value),'finite-number')
    return value
def integer(value,lo=0,hi=2**53-1):
    need(type(value) is int and lo<=value<=hi,'bounded-integer')
    return value
def strict_pairs(pairs):
    out={}
    for k,v in pairs:need(k not in out,'duplicate-json-key');out[k]=v
    return out
def parse(raw,numeric_tokens=None):
    def bad(value):raise ValueError('nonfinite-json:'+value)
    def jf(value):
        result=finite(float(value))
        if numeric_tokens is not None:
            key=word(result)
            if key in numeric_tokens:need(numeric_tokens[key]==value,'consistent-query-number-spelling')
            numeric_tokens[key]=value
        return result
    return json.loads(raw,object_pairs_hook=strict_pairs,parse_constant=bad,parse_float=jf)
def compact(value):return json.dumps(value,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()
def norm(value,path='',excluded=()):
    if type(value) in (int,float):return word(value)
    if type(value) in (list,tuple):return [norm(v,path+'[]',excluded) for v in value]
    if type(value) is dict:return {k:norm(value[k],path+'.'+k if path else k,excluded) for k in sorted(value) if (path+'.'+k if path else k) not in excluded}
    return value
def canonical(value,excluded=()):return compact(norm(value,excluded=excluded))+b'\n'
def exact(a,b,label):need(canonical(a)==canonical(b),label)
def identity(pin):return {k:pin[k] for k in ('bytes','sha256')}
def rooted(value,path):
    for k in path.split('.'):value=value[k]
    return value
def insert(value,path,item):
    keys=path.split('.')
    for k in keys[:-1]:value=value[k]
    need(keys[-1] not in value,'no-overwrite-restored-field');value[keys[-1]]=item
def checked(name,pin=None):
    need(type(name) is str and not name.startswith('/') and '..' not in Path(name).parts,'relative-evidence-path')
    path=BASE/name
    need(path.is_file() and not path.is_symlink(),'regular-evidence-file')
    raw=path.read_bytes();got=dict(bytes=len(raw),sha256=sha(raw))
    if pin is not None:exact(got,identity(pin),'evidence-byte-pin')
    if name in PINS:exact(got,PINS[name],'evidence-stable-identity')
    PINS[name]=got
    return raw
def saved(name):return parse(checked(name))
def frozen(path):return parse(infrastructure.committed(path))
def lines(raw,numeric_tokens=None):
    for line in raw.splitlines(keepends=True):
        need(line.endswith(b'\n') and len(line)<=8*1024**2,'complete-bounded-jsonl-line')
        yield parse(line,numeric_tokens)
def checks_equal(saved_checks,expected):exact(saved_checks,expected,'individual-check-reconstruction');need(all(c['pass'] is True for c in expected),'failed-control-check')
def ck(name,value):return {'id':name,'pass':value is True}
def snapshot(v):
    if type(v) in (int,float):return {'number':word(v)}
    if type(v) is list:return {'array':True,'properties':[[str(i),snapshot(x)] for i,x in enumerate(v)]+[['length',snapshot(len(v))]]}
    if type(v) is dict:return {'array':False,'properties':[[k,snapshot(x)] for k,x in v.items()]}
    return v
def input_from_snapshot(v):
    if type(v) is not dict:return v
    if set(v)=={'number'}:return number(v['number'])
    need(set(v)=={'array','properties'} and type(v['array']) is bool,'descriptor-snapshot-fields')
    keys=[x[0] for x in v['properties']];need(len(set(keys))==len(keys),'unique-own-keys')
    out={k:input_from_snapshot(x) for k,x in v['properties']}
    if v['array']:
        n=out.pop('length');need(math.isfinite(n) and int(n)==n and n>=0,'array-snapshot-length')
        need(all(k.isdecimal() and int(k)<n for k in out),'array-own-index-domain')
        return [out.get(str(i),HOLE) for i in range(int(n))]
    return out
HOLE=object()

def fixture_snapshot(v):
    if type(v) is list:return {'array':True,'properties':[[str(i),fixture_snapshot(x)] for i,x in enumerate(v) if x is not HOLE]+[['length',snapshot(len(v))]]}
    if type(v) is dict:return {'array':False,'properties':[[k,fixture_snapshot(x)] for k,x in v.items()]}
    return snapshot(v)

def kernel_fixtures():
    result=[]
    def add(name,pos,eligible=True,patches=(),reason=None):
        states=[list(p)+[0,0,0,0,0,0,1,0,0,0]+[(.027*9.81)/4]*4 for p in pos]
        for i,k,v in patches:states[i][k]=v
        result.append((name,states,dict(eligible=eligible,reason=reason)))
    up=lambda x:math.nextafter(x,math.inf)
    down=lambda x:math.nextafter(x,-math.inf)
    for x in (0,-6):
        for label,f in [('below',down),('exact',lambda x:x),('above',up)]:add('radius-'+str(x)+'-'+label,[[x,0,0],[f(x+3),0,0]])
    for axis,label,f in [(0,'below',down),(1,'exact',lambda x:x),(2,'above',up)]:
        rotate=lambda v:[v[(k-axis+3)%3] for k in range(3)]
        add('cell-'+label,[[0,0,0],rotate([f(4),.25,.5]),rotate([4,0,1])])
    add('signed-zero',[[-0.0,0,0],[0,-0.0,0]])
    coarse=[[0,0,0],[1,.25,.5],[4,1,2]];add('coarse-origin',coarse);add('coarse-translated',[[x+2**40 for x in p] for p in coarse])
    add('dense-16',[[i*.05,0,.45*(i%3)] for i in range(16)])
    add('span-256',[[0,0,0],[256,0,0]])
    add('span-nextUp256',[[0,0,0],[up(256),0,0]],False,reason='span-out-of-range')
    add('far-invalid258',[[0,0,0],[258,0,0]],False,reason='span-out-of-range')
    add('nonfinite-nan',[[0,0,0],[math.nan,0,0]],False,reason='coordinate-nonfinite')
    add('nonfinite-infinity',[[0,0,0],[math.inf,0,0]],False,reason='coordinate-nonfinite')
    add('overflow-span',[[-sys.float_info.max,0,0],[sys.float_info.max,0,0]],False,reason='span-nonfinite')
    add('near-field',[[0,0,0],[0,0,.02]]);add('duplicates',[[1,1,1],[1,1,1]])
    for n in (62,64,66):add('planes-'+str(n),[[0,0,0 if i<n/2 else .6] for i in range(n)])
    for axis,axisname in enumerate('xyz'):
        for label,f in [('below',down),('exact',lambda x:x),('above',up)]:
            p=[0,0,0];p[axis]=f(4);add('component-'+axisname+'-'+label,[[0,0,0],p])
    add('span-diagonal-256',[[0,0,0],[256,256,256]]);add('span-nextDown256',[[0,0,0],[down(256),0,0]])
    add('center-257-fallback',[[0,0,0],[257,0,0]],False,reason='span-out-of-range')
    add('center-nextUp257-fallback',[[0,0,0],[up(257),0,0]],False,reason='span-out-of-range')
    positive=[[0,0,0],[0,0,.6],[4,0,0]]
    add('mixed-near-far',[[0,0,0],[0,0,.02],[4,0,0]]);add('mixed-positive-far',positive)
    add('invalid-quaternion-far',[[0,0,0],[4,0,0]],patches=[(0,9,2)])
    for label,v in [('zero',0),('negative',-.01),('nan',math.nan)]:add('nominal-'+label+'-positive-far',positive,patches=[(1,13,v)])
    add('scaled-cap-positive-far',positive,patches=[(1,k,1e12) for k in range(13,17)])
    add('invalid-quaternion-nan-far',[[0,0,0],[4,0,0]],patches=[(0,6,math.nan)])
    add('nominal-infinity-positive-far',positive,patches=[(1,13,math.inf)])
    add('nominal-total-overflow-positive-far',positive,patches=[(1,k,sys.float_info.max) for k in range(13,17)])
    add('nominal-unequal-positive-far',positive,patches=[(1,13+r,v) for r,v in enumerate((.03,.04,.05,.06))])
    need(len(result)==48,'independent-48-kernel-fixtures')
    for name,pos,eligible in [('sparse2',[[0,0,0],[4,0,0]],True),('planes62',[[0,0,0 if i<31 else .6] for i in range(62)],True),('fallback258',[[0,0,0],[258,0,0]],False)]:add(name,pos,eligible,reason=None if eligible else 'span-out-of-range')
    return result

def native_fixtures():
    def d(ident=1,p=(0,0,0),f=(.03,.04,.05,.06),q=(0,0,0,1)):
        return dict(id=ident,state=list(p)+[0,0,0]+list(q)+[0,0,0]+list(f))
    pair=lambda z=.6:[d(),d(2,(0,0,z))]
    success='native-success';refused='input-refused';domain='domain-refused';numerical='numerical-failure'
    specs=[]
    def add(name,drones,status=success):specs.append((name,{'drones':drones},status))
    add('isolated-linear-nominal',[d(7)])
    add('reverse-stable-id-order',[d(9,(4,0,0)),d(2)])
    add('duplicate-id',[d(2),d(2,(4,0,0))],refused)
    add('unsafe-id',[d(9007199254740992)],refused);add('negative-zero-id',[d(-0.0)],refused)
    short=d();short['state'].pop();add('short-state',[short],refused)
    sparse=d();sparse['state'][1]=HOLE;add('sparse-state',[sparse],refused)
    add('active-unequal-pair',pair())
    add('subnormal-coupled-output',[d(f=[5e-324]*4),d(2,(0,0,.6))],numerical)
    add('nominal-zero',[d(f=[0,.04,.05,.06])],refused);add('nominal-negative',[d(f=[-.03,.04,.05,.06])],refused)
    add('normalizer-overflow',[d(f=[sys.float_info.max,.04,.05,.06])],numerical)
    add('subnormal-isolated',[d(f=[5e-324]*4)])
    add('quaternion-domain',[d(q=(0,0,0,2))],domain);add('unsupported-near-pair',pair(.02),domain)
    add('neighbor-exact-three',pair(3));add('downcut-exact',pair(2.5));add('downcut-below',pair(2.4999999999999996))
    qt=(0,.7071067811865476,0,.7071067811865476)
    add('projection-zero-farfield',[d(q=qt),d(2,(0,0,.6))])
    add('equal-z-order-refusal',[d(q=qt),d(2,(.6,0,0),q=qt)],domain)
    add('tilted-unequal-linear-loads',[d(5,q=qt)])
    add('tilted-symmetric-cancellation',[d(5,f=[.05]*4,q=(0,.3826834323650898,0,.9238795325112867))])
    bad=d();bad['state'][3]=math.inf;add('nonfinite-unused-velocity',[bad],refused);add('empty-input',[],refused)
    force=[[.03125,.046875,.0625,.078125],[.046875,.0625,.078125,.09375],[.0625,.078125,.09375,.109375]]
    a={'drones':[d(i+1,(0,0,[0,.6,1.2][i]),force[i]) for i in range(3)]};b=copy.deepcopy(a);c=copy.deepcopy(a)
    b['drones'][1]['state'][13]*=2;b['drones'].reverse()
    c['drones'][1]['state'][13:15]=reversed(c['drones'][1]['state'][13:15])
    extras=[('A',a,None),('B',b,None),('C',c,None),('A-repeat',a,None),('guard1',a,1),('guard6',a,6),('A-clean',a,None)]
    return specs,extras

def decoded(value):
    """Only used for known numeric evidence subtrees, never arbitrary strings."""
    if type(value) is str:return number(value)
    if type(value) is list:return [decoded(v) for v in value]
    return value

def analytic(name,e,status):
    out=[ck('expected-status',e['status']==status)]
    if status!='native-success':return out
    ids=e['ids'];out += [ck('canonical-ids',all(ids[i-1]<ids[i] for i in range(1,len(ids)))),ck('all-load-words-consumed',e['consumption']['loadWords']==11*len(ids)),ck('all-ids-and-status-consumed',e['consumption']['identityWords']==len(ids) and e['consumption']['status']=='native-success' and e['consumption']['statusCharacters']==14)]
    out.append(ck('delivered-linear-forces',all(word(number(load['rotor'][r]))==word(number(e['raw'][i]['state'][13+r])*number(e['solution'][i]['rotors'][r]['x']))==e['solution'][i]['rotors'][r]['T'] for i,load in enumerate(e['loads']) for r in range(4))))
    coeff=e['coefficients'];rotors=e['solution'][0]['rotors']
    if name=='active-unequal-pair':out += [ck('all-four-positive-receiver-terms',len(coeff['K'])==4 and coeff['offsets']==[min(i,4) for i in range(9)]),ck('nontrivial-rotor-ratios',all(0<number(r['x'])<1 for r in rotors)),ck('source-ratios-one',all(number(r['x'])==1 for r in e['solution'][1]['rotors']))]
    if name in ('neighbor-exact-three','downcut-exact','projection-zero-farfield'):out.append(ck('zero-positive-support',len(coeff['K'])==0))
    if name=='downcut-below':out.append(ck('positive-fade-side',len(coeff['K'])==4))
    if name=='reverse-stable-id-order':out.append(ck('stable-id-association',ids==[2,9] and number(e['raw'][0]['state'][0])==0 and number(e['raw'][1]['state'][0])==4))
    if name=='subnormal-isolated':out.append(ck('subnormal-force-words',all(v==word(5e-324) for v in e['loads'][0]['rotor']) and e['loads'][0]['collective']==word(2e-323)))
    expected={'isolated-linear-nominal':(.18,[0,0,.18],[-.00112,0,0]),'tilted-unequal-linear-loads':(.18,[.18,0,0],[0,0,.00112]),'tilted-symmetric-cancellation':(.2,[.1414213562373095,0,.1414213562373095],[0,0,0])}.get(name)
    if expected:
        load=e['loads'][0];close=lambda a,b:math.isfinite(number(a)) and abs(number(a)-b)<=1e-14
        out += [ck('nominal-ratios-one',all(number(r['x'])==1 for r in rotors)),ck('analytic-collective',close(load['collective'],expected[0])),ck('analytic-world-force',all(close(x,y) for x,y in zip(load['worldForce'],expected[1]))),ck('analytic-world-moment',all(close(x,y) for x,y in zip(load['worldMoment'],expected[2])))]
    return out

def ownership(record,allocated):
    own=record['ownership'];exact(own['priorIds'],list(allocated),'ownership-complete-prior-id-list')
    caller=set();returned=[]
    for key in ('caller','returned'):
        paths=set();seen=set()
        for a in own[key]:
            need(a['path'] not in paths,'storage-unique-path');paths.add(a['path']);integer(a['id'],1)
            need(a['id'] not in seen,'storage-unique-object-id');seen.add(a['id'])
            if 'buffer' in a:
                need(set(a)=={'path','id','kind','buffer','byteOffset','byteLength','bufferBytes'},'typed-storage-fields')
                for field in ('buffer','byteOffset','byteLength','bufferBytes'):integer(a[field],1 if field=='buffer' else 0)
                need(a['kind'] in ('Float64Array','Uint32Array','Uint8Array','Buffer'),'typed-storage-class')
            else:need(set(a)=={'path','id','kind'} and a['kind']=='Array','array-storage-fields')
            values=[a['id']]+([a['buffer']] if 'buffer' in a else [])
            if key=='caller':caller.update(values)
            else:returned.extend(values)
    expected=[ck('input-storage-disjoint',not caller.intersection(returned)),ck('prior-output-storage-disjoint',not set(allocated).intersection(returned)),ck('typed-full-owned-ranges',all('buffer' not in a or a['byteOffset']==0 and a['byteLength']==a['bufferBytes'] for a in own['returned']))]
    checks_equal(own['checks'],expected)
    for ident in returned:allocated.setdefault(ident,None)
    return expected

def storage_paths(value,path='',kernel=False):
    out={}
    if kernel and type(value) is dict and set(value)=={'typed','values'}:
        out[path]=(value['typed'],len(value['values']));return out
    if type(value) is list:out[path]=('Array',len(value))
    if type(value) in (dict,list):
        entries=value.items() if type(value) is dict else enumerate(value)
        for key,v in entries:
            if kernel and not path and key=='states':continue
            out.update(storage_paths(v,path+'.'+str(key) if path else str(key),kernel))
    return out

def storage_coverage(record,is_kernel):
    caller=storage_paths(input_from_snapshot(record['inputBefore']))
    result=storage_paths(record['output'] if is_kernel else record['encoded'],kernel=is_kernel)
    if not is_kernel:
        # Evidence encoding materializes these four typed coefficient arrays.
        for field,kind in [('offsets','Uint32Array'),('sourceIndices','Uint32Array'),('K','Float64Array'),('a','Float64Array')]:
            path='coefficients.'+field
            if path in result:result[path]=(kind,result[path][1])
    for label,expected in [('caller',caller),('returned',result)]:
        actual={x['path']:x for x in record['ownership'][label]}
        need(set(actual)==set(expected),'complete-storage-path-observations')
        for path,(kind,length) in expected.items():
            need(actual[path]['kind']==kind,'storage-type-from-complete-output')
            if kind!='Array':need(actual[path]['byteLength']==length*({'Float64Array':8,'Uint32Array':4,'Uint8Array':1,'Buffer':1}[kind]),'storage-complete-array-size')

def controls_audit():
    report=saved('results/controls.json');journal=list(lines(checked('results/controls-partial.jsonl')))
    need(set(report)=={'schema','kernel','native','kernelRetention','nativeRetention','pairChecks','analyticWitnesses','nativeCalls','kernelBuilds','passed'},'controls-exact-fields')
    need(report['schema']=='m31-native-factor-controls-v1' and report['passed'] is True and report['nativeCalls']==62 and report['kernelBuilds']==102,'controls-complete-budget')
    exact(saved('results/control-summary.json'),dict(passed=True,nativeCalls=62,kernelBuilds=102),'control-summary')
    events=[];allocated={};pairs=[];kernel={};native={};retk=[];retn=[];witness=[]
    def event(kind,v):events.append(dict(kind=kind,value=v))
    fixtures=kernel_fixtures();need(len(report['kernel'])==102,'control-build-count')
    for fi,(name,states,expected) in enumerate(fixtures):
        pair=[]
        for ai,arm in enumerate(('F','C')):
            ordinal=2*fi+ai+1;r=report['kernel'][ordinal-1]
            need(set(r)=={'ordinal','id','arm','inputBefore','inputAfter','output','phasesMs','ownership','expected','checks'},'kernel-control-fields')
            exact([r['ordinal'],r['id'],r['arm'],r['expected']],[ordinal,name,arm,expected],'fixed-kernel-control-schedule')
            exact(r['inputBefore'],fixture_snapshot(states),'complete-kernel-literal-input');exact(r['inputAfter'],r['inputBefore'],'kernel-input-preservation')
            o=r['output'];need('phasesMs' not in o,'kernel-timing-only-exclusion');exact(o['states'],norm(states),'kernel-saved-input-words')
            storage_coverage(r,True)
            need(o['n']==word(len(states)) and o['symbols']['typed'] in ('Buffer','Uint8Array') and len(o['symbols']['values'])==len(states)**2*4,'kernel-full-symbols')
            expected_checks=[ck('input-preserved',True)]+ownership(r,allocated)+[ck('screen-eligible',o['screen']['eligible']==expected['eligible']),ck('fallback-reason',o['screen']['fallbackReason']==expected['reason'])]
            checks_equal(r['checks'],expected_checks);kernel[ordinal]=r;pair.append(r);event('kernel',r)
        equal=canonical(pair[0]['output'])==canonical(pair[1]['output']);p=dict(kind='kernel',id=name,F=pair[0]['ordinal'],C=pair[1]['ordinal'],equal=equal);need(equal,'full-kernel-byte-pair');pairs.append(p);event('pair',p)
        if fi>=48:
            for arm,held in [('F',47),('C',48)]:
                # planes-66 is fixture24, hence returned builds47/48.
                rr=report['kernelRetention'][len(retk)];want=dict(afterBuild=2*fi+2,arm=arm,ordinal=held,after=kernel[held]['output'],afterInput=kernel[held]['inputBefore'],unchanged=True)
                exact(rr,want,'kernel-retention-full-snapshot');retk.append(rr);event('kernel-retention',rr)
    wrappers,extras=native_fixtures();schedule=[(n,a,inp,st,None,True) for n,inp,st in wrappers for a in ('F','C')]+[(n,a,inp,'native-success' if limit is None else 'resource-failure',limit,False) for a in ('F','C') for n,inp,limit in extras]
    need(len(report['native'])==len(schedule)==62,'native-controls-fixed-count');held=[];extra_by_arm={}
    for ordinal,(name,arm,inp,status,limit,inherited) in enumerate(schedule,1):
        r=report['native'][ordinal-1];e=r['encoded'];exact([r['ordinal'],r['id'],r['arm'],r['expectedStatus'],r['pollLimit']],[ordinal,name,arm,status,limit],'native-control-fixed-schedule')
        need(set(r)=={'ordinal','id','arm','inputBefore','inputAfter','expectedStatus','pollLimit','polls','encoded','ownership','analytic','checks'},'native-control-fields')
        exact(r['inputBefore'],fixture_snapshot(inp),'complete-native-literal-input');exact(r['inputAfter'],r['inputBefore'],'native-input-preserved')
        integer(r['polls'],1);need(e['method']=='F' and e['status']==status,'native-fixed-status-method')
        storage_coverage(r,False)
        cs=[ck('input-preserved',True),ck('expected-status',True),ck('method-F',True)]+ownership(r,allocated)
        if inherited:
            ac=analytic(name,e,status);exact(r['analytic'],{'schema':'m31-native-microcontrol-check-v1','id':name,'checks':ac,'pass':all(x['pass'] for x in ac)},'inherited-analytic-assertion-reconstruction');cs.append(ck('inherited-analytic-checks',all(x['pass'] for x in ac)))
        else:need(r['analytic'] is None,'extra-no-inherited-analytic')
        if limit is not None:cs += [ck('guard-ordinal',r['polls']==limit),ck('guard-reason',e['reason']=='cooperative-guard'),ck('guard-stage',e['stage']==('input' if limit==1 else 'build'))]
        checks_equal(r['checks'],cs);native[ordinal]=r;event('native',r)
        for old in held:
            rr=report['nativeRetention'][len(retn)];want=dict(afterCall=ordinal,heldCall=old,after=native[old]['encoded'],unchanged=True);exact(rr,want,'native-retention-full-evidence');retn.append(rr);event('native-retention',rr)
        if ordinal<=48 and ordinal%2==0:
            p=dict(kind='native',id=name,F=ordinal-1,C=ordinal,equal=canonical(native[ordinal-1]['encoded'],PAIR_EXCLUSIONS)==canonical(e,PAIR_EXCLUSIONS));need(p['equal'],'inherited-native-full-pair');pairs.append(p);event('pair',p)
        if ordinal>48:
            extra_by_arm.setdefault(arm,[]).append(r)
            if name=='A':held.append(ordinal)
            if name=='A-clean':
                a,b,c,rep,g1,g6,clean=extra_by_arm[arm]
                def coeff(rec,row,source):
                    q=rec['encoded']['coefficients'];matches=[number(q['a'][z]) for z in range(q['offsets'][row],q['offsets'][row+1]) if q['sourceIndices'][z]==source];need(len(matches)==1,'fixed-analytic-coefficient');return matches[0]
                aw,bw,an,bn,cn,cs0=coeff(a,0,1),coeff(b,0,1),coeff(a,4,2),coeff(b,4,2),coeff(c,4,2),coeff(c,0,1)
                checks=[ck('B-source-beta-increases-coefficient',bw>aw),ck('B-row-nu-decreases-coefficient',bn<an),ck('C-source-total-preserved',a['encoded']['prepared'][1]['nativeTotal']==c['encoded']['prepared'][1]['nativeTotal']),ck('C-source-coefficient-unchanged',word(aw)==word(cs0)),ck('C-row-nu-changes-coefficient',cn<an),ck('A-repeat-exact',canonical(a['encoded'],PAIR_EXCLUSIONS)==canonical(rep['encoded'],PAIR_EXCLUSIONS)),ck('A-clean-exact',canonical(a['encoded'],PAIR_EXCLUSIONS)==canonical(clean['encoded'],PAIR_EXCLUSIONS))]
                want=dict(arm=arm,coefficients=dict(A_source=word(aw),B_source=word(bw),A_row=word(an),B_row=word(bn),C_source=word(cs0),C_row=word(cn)),checks=checks);rr=report['analyticWitnesses'][len(witness)];exact(rr,want,'independent-A-B-C-analytic-witness');need(all(x['pass'] for x in checks),'analytic-lifetime-witness');witness.append(rr);event('analytic-witness',rr)
    for i,(name,_,_) in enumerate(extras):
        p=dict(kind='native',id=name,F=49+i,C=56+i,equal=canonical(native[49+i]['encoded'],PAIR_EXCLUSIONS)==canonical(native[56+i]['encoded'],PAIR_EXCLUSIONS));need(p['equal'],'extra-native-full-pair');pairs.append(p);event('pair',p)
    exact(report['pairChecks'],pairs,'complete-control-pair-inventory');exact(report['kernelRetention'],retk,'complete-kernel-retention');exact(report['nativeRetention'],retn,'complete-native-retention');exact(report['analyticWitnesses'],witness,'complete-analytic-witnesses');exact(journal,events,'exact-append-before-assert-journal-order')
    CHECKS.append('102 fixed full-kernel comparisons/builds, 62 fixed native controls, exact descriptor inputs, 82 full paired comparisons, all saved retention/ownership and analytic guard/lifetime witnesses checked; no numerical invocation')
    return dict(nativeCalls=62,kernelBuilds=102,pairChecks=len(pairs),journalRecords=len(events),passed=True)

def source_gate():
    pub=infrastructure.gate()
    manifest=parse(checked('source-manifest.json'));exact(parse(checked('source-publication.json')),pub,'stable-source-publication');pins=infrastructure.PINS
    need(set(pins)=={p['path'] for p in manifest['files']},'unique-source-input-pins')
    cfg=parse((BASE/'config.json').read_bytes())
    exact(cfg['exclusions'],EXCLUSIONS,'exact-old-nine-exclusions');exact(cfg['pairExclusions'],PAIR_EXCLUSIONS,'only-two-pair-timer-exclusions')
    exact(cfg['caseIds'],CASE_IDS,'fixed-case-ids');exact(cfg['totalStages'],TOTAL,'fixed-total-stages')
    exact(cfg['repetitions'],list(range(-1,8)),'fixed-repetitions')
    need(cfg['maxCalls']==34560 and cfg['maxNativeControlCalls']==62 and cfg['maxKernelControlBuilds']==102 and cfg['windowLength']==160,'fixed-allocation-query-build-counts')
    exact(cfg['keepGate'],dict(medianAggregateRatioMaximum=.9,strictWinsMinimum=7,exactCorrectnessRequired=True),'fixed-keep-gate')
    exact(cfg['allocations'],dict(producer=dict(seconds=1800,mib=512),audit=dict(seconds=1800,mib=128),finalize=dict(seconds=120,mib=2),ui=dict(seconds=180,mib=16)),'fixed-resource-allocations')
    need(cfg['runtimeGeneralEquivalenceProven'] is False,'conditional-runtime-claim')
    seen=set();queue=[REL+'/source/run.cjs']
    while queue:
        relative=queue.pop()
        if relative in seen:continue
        seen.add(relative);need(relative in pins,'pinned-commonjs-dependency')
        text=(ROOT/relative).read_text()
        for dependency in re.findall(r"require\(['\"]([^'\"]+)['\"]\)",text):
            if dependency.startswith('node:'):continue
            need(dependency.startswith('.'),'no-unpinned-external-scientific-module')
            resolved=(ROOT/relative).parent.joinpath(dependency).resolve().relative_to(ROOT).as_posix()
            need(resolved.endswith('.cjs'),'explicit-commonjs-dependency');queue.append(resolved)
    native=(ROOT/'research/m31-native-fresh-transfer-2026-10-17/source/native-load.cjs').read_bytes()
    candidate=(BASE/'source/candidate.cjs').read_bytes()
    expected=native.replace(b"require('./vendor/kernel.cjs')",b"require('./candidate-kernel.cjs')")
    need(candidate==expected,'wrapper-only-kernel-import-change')
    renderer=['outputs/step02b-source/vendor/'+name for name in ('three.module.js','three.core.js','OrbitControls.js')]
    need(all(name in pins for name in renderer),'complete-renderer-transitive-source-pins')
    need('three.core.js' in (ROOT/renderer[0]).read_text(),'three-module-core-dependency-present')
    CHECKS.append('reviewed public source, exact configuration, literal transitive CommonJS and three-file renderer closure bound; native wrapper differs only in kernel import')
    return pub,manifest,sorted(seen)

def receipt_gate(base,receipt_name,required,commit=None):
    receipt=frozen(receipt_name);manifest=frozen(base+'/result-manifest.json')
    if base==PHASE:
        # This final receipt attests a composite recovery, retaining nine failed
        # screenshot acquisitions; it does not use the older flat receipt schema.
        proof=receipt['manifest'];need(proof['path']==base+'/result-manifest.json','phase-manifest-path')
        exact(identity(proof),identity(infrastructure.PINS[base+'/result-manifest.json']),'phase-manifest-receipt-pin')
        need(receipt['parentSeparatelyFetchedManifest'] is True and receipt['independentPublicReviewPassed'] is True and receipt['freshPublicReads']==73 and 'All nine original screenshot failures remain failures' in receipt['verificationScope'],'phase-composite-public-identity-recovery')
    else:
        need(receipt['manifestPath']==base+'/result-manifest.json','prior-manifest-path')
        exact(dict(bytes=receipt['manifestBytes'],sha256=receipt['manifestSha256']),identity(infrastructure.PINS[base+'/result-manifest.json']),'prior-manifest-receipt-pin')
        need(receipt['remoteManifestBytesEqualLocal'] is True and (receipt.get('committedManifestBytesEqualLocal') is True or receipt.get('committedBytesEqualLocal') is True),'prior-public-and-git-manifest-identities')
    if commit:need(receipt['commit']==commit,'fixed-prior-result-commit')
    table={p['path']:p for p in manifest['files']};need(len(table)==len(manifest['files'])==receipt['verifiedFilePins'],'prior-public-inventory')
    for path in required:exact(identity(infrastructure.PINS[path]),identity(table[path]),'prior-public-source-input-binding')
    return receipt,manifest

def prior_gate():
    old_required=[OLD+'/'+n for n in ('extract/index.json','transport/index.json','audit/audit.json','ALLOCATION-CLOSURE.json')]
    old_receipt,old_manifest=receipt_gate(OLD,'research/publication-receipts/m31-buffered-motion-result-2026-10-22.json',old_required,'0461153a7d6f75cb6e8564850b77e8b6f04cebb2')
    need(old_receipt['independentPublicCheck']['passedWithDisplayProvenanceQualification'] is True,'prior-buffered-qualified-public-review')
    prior_required=[PRIOR+'/'+n for n in ('audit/audit.json','ALLOCATION-CLOSURE.json')]+[DENSITY+'/'+n for n in ('results/stages.jsonl','results/summary.json')]
    receipt,manifest=receipt_gate(PRIOR,'research/publication-receipts/m31-radial-integration-result-2026-10-23.json',prior_required,'8c80900fdb5de6b1cf5b3b211c8a461ecac86f1a')
    need(receipt['independentPublicReviewPassed'] is True and receipt['originalScientificAllocationRetries']==0,'prior-radial-public-and-no-scientific-retry')
    need(receipt['supplementalPublicationRecords'] and 'CLOSED INCOMPLETE' in receipt['verificationScope'] and 'CLOSED FAILED' in receipt['verificationScope'],'prior-publication-failed-history-preserved')
    previous=frozen(PRIOR+'/audit/audit.json');closure=frozen(PRIOR+'/ALLOCATION-CLOSURE.json')
    need(previous['passed'] is True and previous['nativeCalls']==0 and previous['stages']==1920 and previous['calls']==34560,'prior-saved-audit-passed')
    need(previous['exactReferenceEquivalence'] is True and previous['baselineStrictReferenceEquivalence'] is True,'prior-full-baseline-reference-equality')
    need(closure['allClosed'] is True and closure['scientificComparisonPassed'] is True and closure['allocationsRetried'] is False,'prior-radial-closed')
    need(closure['costGate'] is False and closure['coverageGate'] is False and closure['keepGate'] is False,'prior-radial-rejection-retained')
    for phase in ('producer','audit','finalize','ui'):
        c=closure['allocations'][phase];need(c['closed'] is True and c['returncode']==0 and c['allocationWallPassed'] is True and c['outputCapPassed'] is True,'prior-radial-allocation-closure')
    old_audit=frozen(OLD+'/audit/audit.json');old_closure=frozen(OLD+'/ALLOCATION-CLOSURE.json')
    need(old_audit['passed'] is True and old_audit['evidenceIntegrityPassed'] is True and old_audit['exactReferenceEquivalence'] is True and old_audit['selectedStages']==1920,'prior-original-full-provenance-audit')
    need(old_audit['sourcePartsScanned']==93 and old_audit['sourceJournalsScanned']==8,'prior-original-provenance-coverage')
    need(old_closure['allClosed'] is True and old_closure['transportIdentityVerified'] is True and old_closure['transportParts']==6,'prior-selected-transport-closure')
    for phase in ('extract','producer','audit','finalize','ui'):
        c=old_closure['phases'][phase];need(c['closed'] is True and c['returncode']==0 and c['allocationWallPassed'] is True and c['outputCapPassed'] is True,'prior-buffered-allocation-closure')
    ix=frozen(OLD+'/extract/index.json');transport=frozen(OLD+'/transport/index.json')
    need(ix['complete'] is True and ix['selected']==1920 and ix['nativeQueries']==0 and transport['complete'] is True and transport['nativeQueries']==0,'complete-fixed-selected-transport')
    exact(ix['windows'],WINDOWS,'exact-selected-windows')
    exact(identity(ix['selectedPin']),dict(bytes=194862495,sha256='b0d833c23eb6e81c2aa600ef82b2e344587762775a07c412a198d49fc2a56dfa'),'fixed-compressed-selected-identity')
    exact(identity(ix['selectedPin']),identity(transport['original']),'transport-selected-original')
    exact(identity(infrastructure.PINS[OLD+'/extract/index.json']),old_audit['extractionIndexPin'],'original-audited-index')
    exact(identity(ix['selectedPin']),old_audit['filePins'][OLD+'/extract/selected.jsonl.gz'],'original-audited-selected')
    exact(identity(ix['selectedPin']),identity(previous['selectedArchivePin']),'prior-radial-selected-archive')
    exact(transport['parts'],previous['selectedTransportPins'],'prior-radial-six-transport-parts')
    public={p['path']:p for p in old_manifest['files']};offset=0
    need(len(transport['parts'])==6,'six-selected-parts')
    for i,p in enumerate(transport['parts']):
        need(p['file']=='selected.jsonl.gz.part'+str(i).zfill(3) and p['offset']==offset and p['bytes']==(33554432 if i<5 else 27090335),'selected-part-order-size-offset')
        path=OLD+'/transport/'+p['file'];exact(identity(infrastructure.PINS[path]),identity(p),'selected-part-source-pin');exact(identity(public[path]),identity(p),'selected-part-old-public-pin');offset+=p['bytes']
    need(offset==194862495,'selected-total-bytes')
    need(len(previous['inputBindings'])==1920,'full-prior-provenance-bindings')
    density=frozen(DENSITY+'/results/summary.json');need(density['stages']==1920,'density-annotation-population')
    CHECKS.append('six immutable transport parts linked to complete prior 93-part/8-journal provenance audit and prior radial public result/closure; failed publication acquisition history and both failed radial gates retained')
    return ix,transport,previous,dict(originalProvenanceAuditPin=identity(infrastructure.PINS[OLD+'/audit/audit.json']),priorAuditPin=identity(infrastructure.PINS[PRIOR+'/audit/audit.json']),priorReceiptPin=identity(infrastructure.PINS['research/publication-receipts/m31-radial-integration-result-2026-10-23.json']),priorPublicResultCommit=receipt['commit'],priorFailedAcquisitionHistory=receipt['verificationScope'],priorDisplayProvenanceQualification=old_receipt['displayProvenanceQualification'],originalSourcePartsRescanned=0,archiveDecompressions=1,scientificAllocationReopened=False)

def csr_work(e):
    q=e['coefficients'];need(q is not None,'complete-returned-csr')
    offset=q['offsets'];source=q['sourceIndices'];k=q['K'];a=q['a'];n=len(e['ids'])
    need(len(offset)==4*n+1 and offset[0]==0 and offset[-1]==len(source)==len(k)==len(a),'complete-csr-shape')
    for r in range(4*n):
        integer(offset[r],0,len(source));integer(offset[r+1],offset[r],len(source));previous=-1
        for z in range(offset[r],offset[r+1]):
            integer(source[z],0,n-1);need(source[z]>previous and source[z]!=r//4,'csr-source-row-order');previous=source[z]
            need(math.isfinite(number(k[z])) and number(k[z])>0 and math.isfinite(number(a[z])) and number(a[z])>0,'csr-positive-finite-values')
    m=len(source);u=len(set(source));r=sum(offset[i+1]>offset[i] for i in range(4*n))
    need(e['diagnostics']['input']['nominalPositive'] is True and e['diagnostics']['input']['nominalTotalFinite'] is True and e['diagnostics']['screen']['eligible'] is True,'completed-eligible-nominalOK-build')
    need(e['diagnostics']['geometryWork']['positiveRotorTerms']==m,'csr-original-positive-work-count')
    return dict(positiveEntries=m,sourceValues=u,nonemptyRows=r,baselineTargetSqrtExpressions=3*m,candidateTargetSqrtExpressions=u+r)

def archive_audit(ix,transport,previous,publication):
    binding=saved('results/input-binding.json');refs=saved('results/references.json')
    exact(binding,dict(sourceCommit=publication['commit'],manifestSha256=publication['manifestSha256'],selectedPin=ix['selectedPin'],extractionIndex=identity(infrastructure.PINS[OLD+'/extract/index.json'])),'complete-producer-input-binding')
    need(len(refs)==1920,'all-reference-records')
    density_raw=infrastructure.committed(DENSITY+'/results/stages.jsonl');density_lines=density_raw.splitlines(keepends=True);need(len(density_lines)==1920,'all-density-annotations')
    zipped=b''.join(infrastructure.committed(OLD+'/transport/'+p['file']) for p in transport['parts'])
    need(len(zipped)==ix['selectedPin']['bytes'] and sha(zipped)==ix['selectedPin']['sha256'],'concatenated-archive-identity-before-decode')
    items={};bindings=[];refusals=[]
    with gzip.GzipFile(fileobj=io.BytesIO(zipped),mode='rb') as stream:
        for ordinal in range(1920):
            OUT.tick();line=stream.readline(4*1024**2+1);need(line.endswith(b'\n') and len(line)<=4*1024**2,'bounded-complete-selected-record');s=parse(line);w,i=divmod(ordinal,160);old=previous['inputBindings'][ordinal]
            need(set(s)=={'window','index','caseId','globalOrdinal','segment','localStageOrdinal','rawOffset','sourceLineSha256','sourceLineBytes','record'},'full-archive-envelope')
            exact([s['window'],s['index'],s['caseId'],s['globalOrdinal']],[w,i,WINDOWS[w]['caseId'],WINDOWS[w]['start']+i],'fixed-selected-order')
            for field in ('window','index','caseId','globalOrdinal','segment','localStageOrdinal','sourceLineSha256','sourceLineBytes','rawOffset'):exact(s[field],old[field],'full-original-provenance-binding')
            need(sha(line)==old['selectedRecordSha256'],'full-selected-envelope-prior-byte-hash')
            record=s['record'];need(set(record)=={'sequence','kind','body'} and record['kind']=='stage' and record['sequence']==old['sourceSequence'],'original-source-sequence')
            body=record['body'];local=s['localStageOrdinal'];need(body['schema']=='m31-coupled-stage-v1' and body['arm']=='coupled' and body['stepIndex']==local//4 and body['stageIndex']==local%4+1 and body['stageId']=='coupled-step'+str(local//4)+'-k'+str(local%4+1),'original-coupled-stage-fields')
            inp=body['nativeInput'];need(set(inp)=={'drones'} and len(inp['drones'])==64,'full-N64-archived-input')
            for ident,d in enumerate(inp['drones']):
                need(set(d)=={'id','state'} and d['id']==ident and len(d['state'])==17,'fixed-input-id-state-shape')
                need(all(math.isfinite(number(x)) for x in d['state']),'finite-current-input-words')
            h=sha(compact(inp));need(h==old['nativeInputSha256'],'full-current-input-byte-binding')
            pos=[d['state'][:3] for d in inp['drones']];need(sha(compact(pos))==old['positionWordsSha256'] and body['originalTimeWord']==old['timeWord'],'time-and-position-words')
            e=body['native'];need(e['schema']=='m31-native-load-evidence-v1' and e['model']=='ordinary-binary64-full-contribution' and e['method']=='F','archived-native-model-method')
            need(e['caseId']==body['stageId'] and e['semanticInputSha256']==h and e['inlineInputCanonicalSha256']==h,'old-adapter-annotations')
            exact(e['raw'],inp['drones'],'full-native-raw-input-word-equality');exact(e['ids'],list(range(64)),'canonical-native-ids')
            need(len(e['prepared'])==64,'complete-prepared-inputs')
            for ident,p in enumerate(e['prepared']):need(p['id']==ident and p['center']==pos[ident],'prepared-center-word-identity')
            exact([e['status'],e['reason'],e.get('stage'),e['diagnostics']['admission']['reasons']],[old['status'],old['reason'],old['nativeStage'],old['admissionReasons']],'archived-status-stage-admission-reasons')
            if e['status']=='native-success':need(body['status']=='completed' and e['reason'] is None and len(e['loads'])==len(e['solution'])==64,'archived-complete-success')
            else:
                need((w,i)==(2,159) and body['status']=='failed' and body['reason']=='native-non-success' and e['status']=='domain-refused' and e['reason']=='native-admission' and e['stage']=='build' and e['diagnostics']['admission']['reasons']==['near-field'],'only-inherited-near-field-refusal')
                need(not any(k in e for k in ('loads','solution','consumption')),'refused-no-consumed-success')
                refusals.append(dict(window=w,index=i,status=e['status'],reason=e['reason'],originalTimeWord=body['originalTimeWord']))
            neighbor_line=density_lines[ordinal];need(neighbor_line.endswith(b'\n') and sha(neighbor_line)==old['neighborLineSha256'],'complete-prior-viewer-position-line');neighbor=parse(neighbor_line)
            for key in ('window','index','caseId','globalOrdinal','sourceLineSha256'):exact(neighbor[key],s[key],'viewer-selected-provenance')
            need(neighbor['selectedRecordSha256']==sha(line) and neighbor['timeWord']==body['originalTimeWord'] and word(neighbor['time'])==body['originalTimeWord'],'viewer-full-envelope-and-time')
            exact(neighbor['positions'],[[number(v) for v in p] for p in pos],'viewer-positions-exact-words');exact(neighbor['ids'],e['ids'],'viewer-canonical-ids')
            exact([neighbor['status'],neighbor['reason'],neighbor['nativeStage'],neighbor['admissionReasons']],[e['status'],e['reason'],e.get('stage'),e['diagnostics']['admission']['reasons']],'viewer-status-refusal-binding')
            ref=refs[ordinal];need(set(ref)=={'window','index','semantic'} and ref['window']==w and ref['index']==i,'reference-schedule-fields');pin=ref['semantic'];semantic=canonical(e,EXCLUSIONS)
            need(set(pin)=={'file','bytes','sha256'} and pin['file']=='semantic-'+pin['sha256']+'.json' and SHA.fullmatch(pin['sha256']),'semantic-cas-name')
            need(sha(semantic)==pin['sha256']==old['strictBaselineSemanticSha256'] and len(semantic)==pin['bytes'],'independent-old-nine-archive-canonicalization')
            need(checked('results/'+pin['file'],pin)==semantic,'full-old-nine-CAS-byte-comparison')
            restored=parse(semantic);insert(restored,'method','F');added={}
            for path in WORK:
                value=rooted(e,path);integer(value,4032,4032);added[path]=value;insert(restored,path,word(value))
            # Already-normalized CAS words must not be treated as new numbers.
            strict=compact(norm(restored))+b'\n';current=copy.deepcopy(e)
            for key in EXCLUSIONS[6:]:del current[key]
            need(strict==canonical(current,PAIR_EXCLUSIONS),'strict-current-payload-restored-with-only-two-exclusions')
            work=csr_work(e);items[w,i]=dict(reference=pin,inputHash=h,status=e['status'],reason=e['reason'],added=added,pairHash=sha(strict),buildPhases=e['status']=='native-success',work=work)
            bindings.append({k:old[k] for k in ('window','index','caseId','globalOrdinal','segment','localStageOrdinal','sourceSequence','sourceLineSha256','sourceLineBytes','rawOffset','selectedRecordSha256','nativeInputSha256','positionWordsSha256','timeWord','status','reason','nativeStage','admissionReasons','neighborLineSha256','strictBaselineSemanticSha256')})
        need(stream.read(1)==b'','exactly-1920-archive-records')
    exact(refusals,ix['refusals'],'same-complete-inherited-refusal-list');need(len(refusals)==1 and refusals[0]['originalTimeWord']=='400cf5c28f5c28f6','fixed-inherited-refusal-time')
    CHECKS.append('all 1920 full archived envelopes, raw current-state words, source line/offset/sequence, viewer positions/time/status and old-nine canonical CAS bytes independently bound; strict paired payloads restored with method and all three original 4032 work counters')
    return items,bindings

def timing_check(value):
    need(type(value) is dict and set(value)=={'clock','totalMs','phasesMs','boundary'},'native-timing-exact-fields')
    need(value['clock']=='performance.now' and type(value['boundary']) is str,'native-timing-clock-boundary')
    need(finite(value['totalMs'])>=0 and type(value['phasesMs']) is dict,'native-finite-time')
    for v in value['phasesMs'].values():need(finite(v)>=0,'nonnegative-native-phase')

def replay_audit(items,publication):
    groups=saved_groups=list(lines(checked('results/groups.jsonl')));need(len(groups)==108,'108-fixed-replay-groups')
    numeric_tokens={};queries=iter(lines(checked('results/queries.jsonl'),numeric_tokens));call=0;outgroups=[];viewer={};counts=dict(admittedCalls=0,refusedCalls=0,warmupCalls=0,measuredCalls=0,strictPairedComparisons=0,archiveComparisons=0)
    fields={'call','window','rep','method','index','semantic','referenceSha256','pairSemanticSha256','referenceEqual','inputBeforeSha256','inputAfterSha256','inputPreserved','afterInput','methodValid','outerMs','status','reason','excluded','encodePersistMs'}
    for rep in range(-1,8):
        for window in range(12):
            OUT.tick();order=['F','C'] if (rep+window+10)%2==0 else ['C','F'];g=dict(window=window,rep=rep,order=order,pairedEqual=True,pairedChecks=160);strict_first=[]
            for ai,arm in enumerate(order):
                aggregate=dict(sumQueryMs=0.0,totalMs=0.0,admittedMs=0.0,refusedMs=0.0,admittedCalls=0,refusedCalls=0)
                for index in range(160):
                    call+=1;r=next(queries,None);need(type(r) is dict and set(r)==fields,'complete-query-exact-fields')
                    exact([r['call'],r['window'],r['rep'],r['method'],r['index']],[call,window,rep,arm,index],'complete-query-fixed-order')
                    item=items[window,index];exact(r['semantic'],item['reference'],'each-call-entire-old-nine-semantic-CAS')
                    need(r['referenceEqual'] is True and r['referenceSha256']==item['reference']['sha256'],'each-call-reference-byte-equality')
                    need(r['methodValid'] is True and r['afterInput'] is None and r['inputPreserved'] is True and r['inputBeforeSha256']==r['inputAfterSha256']==item['inputHash'],'each-call-full-current-input-words-preserved')
                    need(r['status']==item['status'] and r['reason']==item['reason'],'each-call-inherited-outcome')
                    need(finite(r['outerMs'])>=0 and finite(r['encodePersistMs'])>=0,'nonnegative-query-evidence-duration')
                    excluded=r['excluded'];keys={'method','timing',*WORK}
                    if item['buildPhases']:keys.add('diagnostics.buildPhasesMs')
                    need(set(excluded)==keys,'all-and-only-actual-old-nine-excluded-current-paths')
                    need(excluded['method']=='F','both-arms-native-method-F')
                    for path in WORK:integer(excluded[path],4032,4032);need(excluded[path]==item['added'][path],'all-original-archive-excluded-work-counters')
                    timing_check(excluded['timing']);need(r['outerMs']>=excluded['timing']['totalMs'],'complete-query-outer-boundary')
                    if item['buildPhases']:
                        phases=excluded['diagnostics.buildPhasesMs'];need(set(phases)=={'input','index','geometry','admission'},'unaltered-kernel-build-phase-keys')
                        for value in phases.values():need(finite(value)>=0,'nonnegative-build-phase')
                    # Exact CAS pin plus exact restored method/work fields proves that
                    # this query reconstructs the precomputed complete strict bytes.
                    # Cache only this reconstruction; never omit per-query field checks.
                    need(r['pairSemanticSha256']==item['pairHash'],'each-call-independent-strict-payload-hash')
                    if ai==0:strict_first.append((r['semantic'],{p:excluded[p] for p in ['method',*WORK]},r['pairSemanticSha256']))
                    else:
                        exact(strict_first[index],(r['semantic'],{p:excluded[p] for p in ['method',*WORK]},r['pairSemanticSha256']),'each-pair-entire-reconstructible-protected-payload');counts['strictPairedComparisons']+=1
                    aggregate['sumQueryMs']+=r['outerMs'];aggregate['totalMs']+=r['outerMs'];admitted=r['status']=='native-success';aggregate['admittedMs' if admitted else 'refusedMs']+=r['outerMs'];aggregate['admittedCalls' if admitted else 'refusedCalls']+=1
                    counts['admittedCalls' if admitted else 'refusedCalls']+=1;counts['warmupCalls' if rep==-1 else 'measuredCalls']+=1;counts['archiveComparisons']+=1
                    if rep==0:
                        v=viewer.setdefault(window*160+index,dict(window=window,index=index,status=r['status']));need(v['status']==r['status'],'rep-zero-paired-status');v[arm]=dict(outerMs=r['outerMs'])
                        if 'work' in v:exact(v['work'],item['work'],'rep-zero-paired-CSR-counts')
                        else:v['work']=item['work']
                need(aggregate['totalMs']>0,'positive-complete-group-time');g[arm]=aggregate
            g['ratio']=g['C']['totalMs']/g['F']['totalMs'];exact(groups[len(outgroups)],g,'independent-status-partition-group-arithmetic');outgroups.append(g)
    need(next(queries,None) is None and call==34560,'no-extra-or-missing-query')
    exact(counts,dict(admittedCalls=34542,refusedCalls=18,warmupCalls=3840,measuredCalls=30720,strictPairedComparisons=17280,archiveComparisons=34560),'fixed-query-status-pair-coverage')
    reps=[]
    for rep in range(8):
        f,c=0.0,0.0
        for g in outgroups:
            if g['rep']==rep:f+=g['F']['totalMs'];c+=g['C']['totalMs']
        reps.append(dict(rep=rep,F=f,C=c,ratio=c/f))
    ratios=sorted(r['ratio'] for r in reps);median=(ratios[3]+ratios[4])/2;wins=sum(r['C']<r['F'] for r in reps);cost=median<=.9 and wins>=7
    summary=dict(complete=True,calls=34560,controlNativeCalls=62,controlKernelBuilds=102,referenceEquality=True,pairedEquality=True,reps=reps,medianRatio=median,strictWins=wins,costGate=cost,keepGate=cost,performanceMeasured=True,stages=1920,sourceCommit=publication['commit'],scope=SCOPE)
    saved_summary=saved('results/summary.json');need(set(saved_summary)==set(summary)|{'readEvents','wallSeconds'},'summary-exact-fields');exact({k:saved_summary[k] for k in summary},summary,'independent-complete-decision')
    need(type(saved_summary['readEvents']) is list and 0<=finite(saved_summary['wallSeconds'])<=1800,'summary-duration-read-events');summary.update(readEvents=saved_summary['readEvents'],wallSeconds=saved_summary['wallSeconds'])
    need(len(viewer)==1920,'complete-independent-viewer-rows');rows=[viewer[k] for k in range(1920)]
    raw=checked('results/viewer-rows.json');exact(parse(raw),rows,'complete-independent-rep-zero-viewer-rows')
    reconstructed=viewer_json(rows,numeric_tokens)+b'\n';need(raw==reconstructed,'independently-serialized-viewer-bytes')
    CHECKS.append('all 34560 calls and 17280 current strict pairs, 108 source-order groups, eight aggregate ratios, median, strict wins and unchanged cost/keep gate independently reconstructed; all 18 inherited refusal replays retained')
    CHECKS.append('all 1920 repetition-zero annotations reconstructed from saved query timings and complete archived/current-equal CSR; targeted 3M and U+R counts are source expressions, not primitive instrumentation or predicted speed')
    return summary,counts,reconstructed

def viewer_json(value,numeric_tokens):
    """Reconstruct JSON from independently built rows, using query float lexemes.

    Each floating timing value came from queries.jsonl, whose exact numeric token
    was retained by the strict parser and is rechecked by binary64 word. This
    avoids any assumption that Python and JS choose the same shortest decimal.
    No lexeme or field is copied from the producer's viewer file.
    """
    if value is None:return b'null'
    if value is True:return b'true'
    if value is False:return b'false'
    if type(value) is str:return compact(value)
    if type(value) is int:return str(value).encode()
    if type(value) is float:
        finite(value);token=numeric_tokens[word(value)];need(word(float(token))==word(value),'viewer-query-number-lexeme-word')
        return token.encode()
    if type(value) is list:return b'['+b','.join(viewer_json(v,numeric_tokens) for v in value)+b']'
    need(type(value) is dict,'viewer-json-type')
    return b'{'+b','.join(compact(k)+b':'+viewer_json(v,numeric_tokens) for k,v in value.items())+b'}'

def history_audit():
    names=[PHASE+'/'+n for n in ('results/summary.json','audit/audit.json','ALLOCATION-CLOSURE.json')]
    receipt,_=receipt_gate(PHASE,'research/publication-receipts/m31-phase-attribution-result-2026-10-23.json',names)
    need(receipt['independentPublicReviewPassed'] is True,'phase-public-independent-review')
    summary=frozen(PHASE+'/results/summary.json');audit=frozen(PHASE+'/audit/audit.json');closure=frozen(PHASE+'/ALLOCATION-CLOSURE.json')
    need(audit['passed'] is True and audit['nativeCalls']==0 and closure['allClosed'] is True and closure['nativeQueries']==0 and closure['allocationsRetried'] is False,'closed-saved-only-prior-phase-analysis')
    exact(audit['summary'],summary,'prior-phase-summary-audit-binding')
    decision=closure['decision'];need(decision['largestComponent']=='geometry' and decision['sameWinnerReps']==8 and decision['atLeastHalf'] is False and decision['classification']=='distributed-or-unstable','geometry-largest-distributed-history')
    negative=infrastructure.committed('research/m31-normalizer-replication-2026-10-17/MILESTONE-SUMMARY.md').decode()
    for ratio in ('1.0147','0.9700','0.9808','0.9605','0.9431','0.9766'):need(ratio in negative,'completed-negative-normalizer-history')
    need('08ed31c184f88f95217dca689d3727c44c75e8c4' in negative and 'None of the six' in negative and 'numerical checks passed' in negative,'negative-result-is-complete-not-missing')
    planning=infrastructure.committed('research/m31-normalizer-planning-2026-10-17/CANDIDATE-DESIGN.md')
    typed=infrastructure.committed('research/m31-typed-assembly-2026-10-16/MILESTONE-SUMMARY.md')
    need(len(planning)>0 and len(typed)>0,'prior-proposal-and-storage-negative-pinned')
    return dict(phaseResultReceiptPin=identity(infrastructure.PINS['research/publication-receipts/m31-phase-attribution-result-2026-10-23.json']),phasePublicAcquisitionHistory=receipt['verificationScope'],largestComponent='geometry',largestInRepetitions=8,majority=False,interpretation='distributed work; no isolated sqrt-cost measurement or acceleration prediction',normalizerReplicationCompleteNegative=True,normalizerReplicationRatios=[1.0147,.9700,.9808,.9605,.9431,.9766],normalizerReplicationSourceCommit='08ed31c184f88f95217dca689d3727c44c75e8c4',normalizerReplicationImplementation='per-call directed interval/rational beta/nu reuse, not native Number sqrt',typedAssemblyRejected=True,noveltyEstablished=False)

def closure_and_inventory(items,summary):
    infrastructure.prior('producer');supervisor=saved('producer-supervisor.json');exit_record=saved('results/exit.json');environment=saved('results/environment.json')
    need(exit_record['closed'] is True and exit_record['exitCode']==0 and exit_record['calls']==34560,'producer-closed-complete-success')
    exact(exit_record['controlSummary'],dict(passed=True,nativeCalls=62,kernelBuilds=102),'producer-closed-control-budget')
    exact(exit_record['readEvents'],summary['readEvents'],'producer-read-history-preserved');need(summary['wallSeconds']<=finite(exit_record['wallSeconds'])<=1800,'producer-exit-allocation-wall')
    runtime=parse((BASE/'runtime.json').read_bytes());need(environment['node']==runtime['nodeVersion']=='v24.19.0' and environment['sourceCommit']==summary['sourceCommit'],'producer-node-source-runtime-binding')
    need(set(environment)=={'node','platform','arch','startedUtc','sourceCommit','scope'} and environment['scope']=='single-process exposed recorded-state replay; symmetric evidence work outside primary timer, no full-flight timing','environment-timing-scope')
    fixed={'launch.lock','input-binding.json','environment.json','controls-partial.jsonl','controls.json','control-summary.json','references.json','queries.jsonl','groups.jsonl','viewer-rows.json','summary.json','exit.json'}
    expected=fixed|{x['reference']['file'] for x in items.values()};actual={p.name for p in (BASE/'results').iterdir()};need(actual==expected,'complete-producer-file-inventory-no-failure-or-extra')
    need(checked('results/launch.lock')==b'single bounded native factor replay\n','producer-single-use-lock')
    total=0
    for name in sorted(expected):
        need('results/'+name in PINS,'every-produced-file-fully-audited');total+=PINS['results/'+name]['bytes']
    need(total<=512*1024**2 and total-PINS['results/exit.json']['bytes']==exit_record['bytesWritten'],'exact-producer-payload-accounting')
    need(supervisor['outputBytes']==total and supervisor['closed'] is True and supervisor['returncode']==0 and supervisor['allocationWallPassed'] is True and supervisor['outputCapPassed'] is True and not supervisor.get('timeout') and not supervisor.get('evidenceOverflow'),'producer-supervisor-closed-payload-binding')
    CHECKS.append('complete producer inventory, single-use lock, closed supervisor/exit, exact pre-exit and supervisor byte accounting; all input/source/output identities bound')
    return total

def save_raw(name,raw):
    OUT.tick();need(OUT.bytes+len(raw)<=128*1024**2-512*1024,'audit-output-budget')
    with (OUT.out/name).open('xb') as handle:need(handle.write(raw)==len(raw),'complete-audit-output-write')
    OUT.bytes+=len(raw)
    return dict(file='audit/'+name,bytes=len(raw),sha256=sha(raw))

def audit():
    publication,manifest,dependencies=source_gate();infrastructure.prior('producer')
    ix,transport,previous,provenance=prior_gate();history=history_audit();controls=controls_audit()
    items,bindings=archive_audit(ix,transport,previous,publication);summary,counts,viewer=replay_audit(items,publication)
    total=closure_and_inventory(items,summary)
    # Identity-only rereads; no second archive decode, original-source scan or replay.
    for name,pin in list(PINS.items()):OUT.tick();checked(name,pin)
    for pin in manifest['files']:OUT.tick();infrastructure.checked_local(ROOT/pin['path'],pin)
    viewer_pin=save_raw('viewer-rows.json',viewer)
    report=dict(schema='m31-native-factor-reuse-audit-v1',passed=True,evidenceIntegrityPassed=True,exactReferenceEquivalence=True,strictPairedEquality=True,controls=controls,calls=34560,stages=1920,nativeCalls=0,kernelBuildsByAudit=0,nativeQueriesByAudit=0,summary=summary,counts=counts,checks=CHECKS,sourceCommit=publication['commit'],sourceManifestPin=dict(bytes=(BASE/'source-manifest.json').stat().st_size,sha256=sha((BASE/'source-manifest.json').read_bytes())),sourcePublicationPin=dict(bytes=(BASE/'source-publication.json').stat().st_size,sha256=sha((BASE/'source-publication.json').read_bytes())),sourceEvidence=provenance,history=history,inputBindings=bindings,selectedArchivePin=ix['selectedPin'],selectedTransportPins=transport['parts'],sourcePins=manifest['files'],staticDependencyClosure=dependencies,filePins=[dict(file=name,**pin) for name,pin in sorted(PINS.items())],viewerRowsPin=viewer_pin,producerOutputBytes=total,readEvents=infrastructure.EVENTS,producerReadEvents=summary['readEvents'],normalizationExclusions=EXCLUSIONS,pairNormalizationExclusions=PAIR_EXCLUSIONS,arithmeticDisclosure='Independent sorted exact-binary64 normalization; group and repetition timing sums follow producer source order in Python IEEE binary64. CSR counts are integer source-path counts. No sqrt, norm, force, solver, trajectory or native model invoked.',implementationDisclosure='Controls and audit share an author; independent from candidate/producer numerical code, with separate source challenge. Only common.py identity/gating/output infrastructure imported. Prior auditor source architecture reused as text.',limitations=['Finite fixed exposed N64 dependent population; no holdout, universal equivalence or physical validation.','Identity/ownership observations are producer evidence consistency-checked offline; object identity cannot be reobserved from saved JSON.','Two-million-positive-term capacity boundary is static-review-only; unchanged resource failure behavior is not universally proved.','Targeted 3M versus U+R counts exclude wrapper recomputation and all other sqrt work; they do not measure CPU instructions or isolate sqrt cost.','Same-process balanced arms still share JIT, GC, scheduling and evidence-persistence effects; no full-flight or browser-throughput claim.','Prior failed allocation/publication histories remain; no old allocation reopened.','Only the Node executable is pinned; Python/browser/runtime environment are not hermetic.'],physicalValidity=False,flightSafetyClaim=False,statisticalInference=False,noveltyEstablished=False,runtimeGeneralEquivalenceProven=False,researchComplete=False,wallSeconds=time.monotonic()-OUT.start)
    OUT.save('audit.json',report)

if __name__=='__main__':
    OUT=infrastructure.Output('audit','audit');code=0
    try:audit()
    except Exception as error:
        code=1;OUT.failed=True;OUT.save('failure.json',dict(type=type(error).__name__,message=str(error).replace(str(ROOT),'[repository]')[:2000],stack=traceback.format_exc().replace(str(ROOT),'[repository]')[-5000:],nativeCalls=0,kernelBuilds=0,checks=CHECKS,readEvents=infrastructure.EVENTS,filePins=[dict(file=name,**pin) for name,pin in sorted(PINS.items())]))
    finally:OUT.close(code)
    sys.exit(code)
