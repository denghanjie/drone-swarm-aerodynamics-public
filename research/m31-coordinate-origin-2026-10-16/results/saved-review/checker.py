#!/usr/bin/env python3
"""Independent, saved-byte-only review. Never import or execute scientific sources.

Only representation certificates, integer recipe provenance, recorded-field
comparisons, exact stored-term additions, gates, and bookkeeping are evaluated.
No geometry, norm, dot, profile, rotation, shader, root or integration code exists.
"""
import argparse, array, collections, hashlib, json, math, os, pathlib, struct, sys, time, traceback

START = time.monotonic()
DEADLINE = START + 86.0
IDS = [749, 500, 2250, 4750]
N = 80000
UPPER = [512,1024,2048,8,4,4,64,128,3,1.0010000467300415,1.0010000467300415,128,257,257,257,258,258,258]
FAIL = collections.Counter()
WITNESSES = []
CHECKS = collections.Counter()
NEGATIVES = []
ASSESSMENTS = []
REFS = {}
GPUS = {}
PHASE = 'initialization'

def guard():
    if time.monotonic() >= DEADLINE:
        raise TimeoutError('cooperative saved-review deadline')

def check(ok, category, detail=None):
    CHECKS[category] += 1
    if not ok:
        FAIL[category] += 1
        if len(WITNESSES) < 64:
            WITNESSES.append({'category':category, 'detail':detail})
    return bool(ok)

def eq(actual, expected, category, detail=None):
    return check(actual == expected, category, detail)

def digest(p):
    h=hashlib.sha256()
    with open(p,'rb') as f:
        while True:
            b=f.read(1024*1024)
            if not b: break
            h.update(b); guard()
    return h.hexdigest()

def jread(p):
    guard()
    return json.loads(pathlib.Path(p).read_text())

def rawj(name): return jread(RAW/(name+'.json'))

def values(name, kind, length):
    p=RAW/name
    b=p.read_bytes(); guard()
    a=array.array(kind)
    a.frombytes(b)
    if sys.byteorder!='little': a.byteswap()
    if not eq(len(a),length,'binary-shape',name): raise ValueError('binary shape')
    return a

def f64units(v):
    if not math.isfinite(v): raise ValueError('nonfinite dyadic')
    numerator, denominator = v.as_integer_ratio()
    return numerator << (1074-(denominator.bit_length()-1))

def f32units(w):
    exponent=(w>>23)&255; fraction=w&8388607
    if exponent==255: raise ValueError('nonfinite f32 dyadic')
    magnitude=fraction if exponent==0 else (8388608+fraction) << (exponent-1)
    return -magnitude if w>>31 else magnitude

def f32(w): return struct.unpack('<f',struct.pack('<I',w))[0]
def word32(v): return struct.unpack('<I',struct.pack('<f',v))[0]
def word64(v): return struct.unpack('<Q',struct.pack('<d',v))[0]

def cert(obj, key, coefficient, exponent=-1074):
    c=obj.get(key,{})
    eq(c.get('coefficient'),str(coefficient),'exact-certificate',key)
    eq(c.get('exponent'),exponent,'exact-certificate-exponent',key)
    # approximateDisplay is deliberately never used to decide a scientific gate.
    check(isinstance(c.get('approximateDisplay'),(int,float)) and math.isfinite(c['approximateDisplay']), 'certificate-display-finite', key)
    shift=max(0,abs(coefficient).bit_length()-53)
    display=math.ldexp(float(abs(coefficient)>>shift),exponent+shift)
    if coefficient<0: display=-display
    eq(c.get('approximateDisplay'),display,'certificate-display-encoding',key)

def report(a, label, failures=0, counts=None):
    ASSESSMENTS.append((label,a))
    eq(a.get('integrityPass'),True,'saved-assessor-integrity',label)
    eq(a.get('numericalPass'),failures==0,'saved-assessor-numerical',label)
    eq(a.get('pass'),failures==0,'saved-assessor-pass',label)
    eq(a.get('errorClassCounts'),{'integrity':0,'numerical':failures},'saved-error-counts',label)
    eq(a.get('errorCount'),failures,'saved-error-counts',label)
    eq(a.get('witnessCap'),32,'saved-witness-cap',label)
    eq(len(a.get('witnesses',[])),min(32,failures),'saved-witness-count',label)
    check(all(w.get('errorClass')=='numerical' for w in a.get('witnesses',[])),'saved-witness-class',label)
    if counts is not None: eq(a.get('counts'),counts,'assessment-counters',label)
    if 'threshold' in a and 'epsilon' in a['threshold']:
        cert(a['threshold'],'epsilon',EPS); cert(a['threshold'],'referenceSumAllowance',ALLOW)
    if failures: NEGATIVES.append({'stage':label,'numericalFailures':failures})

def mask_for(code,self_row):
    return (2048 if self_row else 30721) if code==0 else {1:260099,2:260099,3:258055,4:260103,5:260175,6:262143,7:262143}.get(code,-1)

def payload_ok(vals, words, mask, label, ordinal):
    good = not (mask & ~262143)
    for f in range(18):
        v=vals[f]
        if mask & (1<<f):
            good &= math.isfinite(v) and abs(v)<=UPPER[f]
            if f<12 and f not in (1,4): good &= v>=0
            if f in (3,6): good &= v>0
        else: good &= words[f]==0
    return check(good,'payload-field-contract',{'stage':label,'ordinal':ordinal})

def row_ok(meta, vals, words, label, n):
    sel=n//20000; source=(n//4)%5000; rotor=n%4; self_row=source==IDS[sel]
    good=meta[:4]==[n,IDS[sel],source,rotor]
    status,code,mask,flags=meta[4:]
    good &= 0<=code<=7 and code!=3 and mask==mask_for(code,self_row)
    good &= status in (3,4,5) and (not self_row or code==0)
    route=1 if self_row else (2 if code==0 else 0)
    good &= not(flags&~15) and flags&3==route and (code>=6 or flags&12==0)
    term=vals[11]
    good &= math.isfinite(term) and term>=0
    if code<=5: good &= status==3 and term==0
    if code==6: good &= status==4 and term==0 and vals[5]==0
    if code==7: good &= vals[5]>0 and ((status==4 and term==0) or (status==5 and term>0))
    return check(good,'record-semantics',{'stage':label,'ordinal':n}) and payload_ok(vals,words,mask,label,n)

def load_reference(label):
    meta=values(label+'-metadata.u32','I',N*8)
    scalars=values(label+'-scalars.f64','d',N*18)
    terms=values(label+'-terms.f64','d',N)
    codes=values(label+'-codes.u8','B',N)
    ordinary=values(label+'-ordinarySums.f64','d',16)
    compensated=values(label+'-compensatedSums.f64','d',16)
    validity=values(label+'-sumValidity.u8','B',16)
    sum_exact=[0]*16; exact=[]; positives=[0]*16; substantive=[0]*16
    code_counts=[0]*8; status_counts=[0]*7; rotor_visits=0; profile=0; valid=0
    for n in range(N):
        if n%4096==0: guard()
        m=list(meta[n*8:n*8+8]); v=scalars[n*18:n*18+18]
        rawwords=[word64(x) for x in v]
        valid+=row_ok(m,v,rawwords,label,n)
        eq(codes[n],m[5],'reference-code-copy',label)
        eq(word64(terms[n]),rawwords[11],'reference-term-copy',label)
        code_counts[m[5]]+=1; status_counts[m[4]]+=1
        rotor_visits += bool(m[6]&229376)
        profile += m[5] in (6,7)
        unit=f64units(terms[n]); exact.append(unit)
        i=(n//20000)*4+n%4; sum_exact[i]+=unit
        positives[i]+=unit>0; substantive[i]+=unit>=16*EPS
    c=rawj(label+'-counts')
    eq(c.get('complete'),True,'reference-completeness',label); eq(c.get('failure'),None,'reference-completeness',label)
    computed={'reservedPairSlots':N,'initializedSlots':N,'validSlots':valid,'centerChecks':4*(5000-1),'rotorVisits':rotor_visits,'profileEvaluations':profile,'positiveTerms':sum(positives),'eligibleSources':rotor_visits//4,'worldPoints':16,'codeCounts':code_counts,'statusCounts':status_counts}
    eq(c['counts'],computed,'reference-stage-counters',label)
    eq(list(validity),[1]*16,'reference-sum-validity',label)
    r={'meta':meta,'scalars':scalars,'terms':terms,'codes':codes,'ordinary':ordinary,'compensated':compensated,'exact':exact,'sums':sum_exact,'positive':positives,'substantive':substantive,'counts':computed}
    REFS[label]=r
    return r

def sum_display(rows, r, label):
    eq(len(rows),16,'saved-sum-diagnostics-shape',label)
    for i,d in enumerate(rows):
        eq(d,{'index':i,'ordinary':r['ordinary'][i],'compensated':r['compensated'][i],'valid':True,'absoluteDifference':abs(r['ordinary'][i]-r['compensated'][i])},'saved-sum-diagnostics',label)

def qualify_reference(label,r,original=None):
    a=rawj(label+'-assessment'); failures=0
    eq(len(a['rotors']),16,'reference-gate-shape',label)
    if original is None:
        cert(a,'referenceSumAllowance',ALLOW); sum_display(a['sums'],r,label)
    else:
        sum_display(a['RSums'],original,label); sum_display(a['QSums'],r,label)
        failures+=sum(x!=y for x,y in zip(original['codes'],r['codes']))
    l1=[0]*16; signed=[0]*16
    if original is not None:
        for n,(q,x) in enumerate(zip(r['exact'],original['exact'])):
            i=(n//20000)*4+n%4; delta=q-x; l1[i]+=abs(delta); signed[i]+=delta
    for i,d in enumerate(a['rotors']):
        eq(d['index'],i,'reference-gate-index',label)
        ordinary_delta=f64units(r['ordinary'][i])-r['sums'][i]
        compensated_delta=f64units(r['compensated'][i])-r['sums'][i]
        sum_pass=abs(ordinary_delta)<=ALLOW and abs(compensated_delta)<=ALLOW
        failures+=abs(r['ordinary'][i]-r['compensated'][i])>ENC['constants']['referenceSumAllowance']
        if original is None:
            cert(d,'exactStoredTermSum',r['sums'][i]); cert(d,'signedOrdinaryMinusStored',ordinary_delta); cert(d,'signedCompensatedMinusStored',compensated_delta)
            passed=sum_pass; failures+=not passed
        else:
            for k,v in [('l1QR',l1[i]),('signedQR',signed[i]),('exactStoredSumR',original['sums'][i]),('exactStoredSumQ',r['sums'][i]),('signedOrdinaryQMinusStored',ordinary_delta),('signedCompensatedQMinusStored',compensated_delta),('l1PlusAllowance',l1[i]+ALLOW)]: cert(d,k,v)
            eq(d['sumPass'],sum_pass,'Q-sum-gate',label)
            passed=sum_pass and l1[i]+ALLOW<=EPS; failures+=(not sum_pass)+(l1[i]+ALLOW>EPS)
        eq(d['pass'],passed,'reference-gate',{'stage':label,'rotor':i})
    counts={'referenceRowsChecked':N,'referenceNumericFieldsChecked':N*18}
    if original is None: counts.update(referenceSumComparisons=16,RExactStoredTermAdds=N,RExactStoredSumGates=32)
    else: counts.update(packedCodeComparisons=N,packingDyadicTermRows=N,referenceSumComparisons=32,packingExactStoredTermAdds=N*2,QExactStoredSumGates=32)
    report(a,label,failures,counts); r['pass']=failures==0; r['l1QR']=l1; r['signedQR']=signed

def usefulness(o):
    r=REFS[f'o{o}-R']; a=rawj(f'o{o}-usefulness-assessment'); failures=0
    cert(a['threshold'],'termThreshold',16*EPS); cert(a['threshold'],'minimumExactStoredSum',256*EPS)
    eq(a['threshold']['requiredReceivers'],[0,1,2],'usefulness-threshold'); eq(a['threshold']['minimumSubstantiveTermsPerRotor'],4,'usefulness-threshold')
    for i,d in enumerate(a['rotors']):
        passed=i>=12 or (r['substantive'][i]>=4 and r['sums'][i]>=256*EPS)
        for k,v in [('index',i),('required',i<12),('positiveTerms',r['positive'][i]),('substantiveTerms',r['substantive'][i]),('pass',passed)]: eq(d[k],v,'usefulness-gate',i)
        cert(d,'exactStoredSum',r['sums'][i]); failures+=not passed
    report(a,f'o{o}-usefulness',failures,{'usefulnessTermRows':N,'usefulnessDyadicAdds':N,'usefulnessRotorGates':12})
    return failures==0

def controls():
    spec=jread(BASE/'controls/controls.json'); binary=(BASE/'controls/controls.u32').read_bytes()
    eq((RAW/'packed-controls.u32').read_bytes(),binary,'control-input-copy')
    eq(binary,b''.join(struct.pack('<40I',*c['words']) for c in spec['controls']),'control-literal-input')
    fields=['ordinal','receiverID','sourceID','rotor','status','policyCode','validityMask','routingFlags']
    for arm in 'ABC':
        w=values('controls-'+arm+'-gpu.u32','I',520); literals=0
        for i,c in enumerate(spec['controls']):
            expected=c['expectedByArm'][arm]; rec=list(w[i*26:(i+1)*26]); v=[f32(x) for x in rec[8:]]
            eq(rec[:8],[expected[k] for k in fields],'control-literal-metadata',{'arm':arm,'control':i})
            payload_ok(v,rec[8:],rec[6],arm+'-control',i)
            assertion=expected['termAssertion']; reached=bool(rec[6]&2048)
            passed={'zero-valid':reached and v[11]==0,'finite-strictly-positive':reached and v[11]>0,'zero-placeholder-not-valid':not reached and rec[19]==0}.get(assertion,False)
            check(passed,'control-term-assertion',{'arm':arm,'control':i})
            for k,v in expected.get('expectedNumericWords',{}).items(): eq(rec[int(k)],v,'control-literal-output'); literals+=1
        report(rawj('controls-'+arm+'-assessment'),'controls-'+arm,0,{'controlRecordsChecked':20,'numericFieldsChecked':360,'controlLiteralWordComparisons':literals})

def gpu_cell(o,arm):
    label=f'o{o}-{arm}'; r=REFS[f'o{o}-R']; q=REFS[f'o{o}-'+('Q1' if arm=='C' else 'Q0')]
    w=values(label+'-terms-gpu.u32','I',N*26); floats=array.array('f'); floats.frombytes(w.tobytes())
    a=rawj(label+'-terms-assessment'); sums=[0]*16; positives=[0]*16; coverage=[0]*16
    totals={k:[0]*16 for k in ['l1TR','l1TQ','l1QR','signedTR','signedTQ','signedQR']}
    maxima=[None]*18; witnesses=[None]*18; compared=0; code_counts=[0]*8; statuses=[0]*7; failures=0
    for n in range(N):
        if n%4096==0: guard()
        b=n*26; meta=list(w[b:b+8]); vals=floats[b+8:b+26]
        valid=row_ok(meta,vals,list(w[b+8:b+26]),label,n)
        status,code,mask,_=meta[4:]
        if code<8: code_counts[code]+=1
        if status<7: statuses[status]+=1
        if not valid: continue
        failures+=code!=r['codes'][n] or code!=q['codes'][n]
        common=mask&q['meta'][n*8+6]
        for f in range(18):
            if common&(1<<f):
                delta=abs(vals[f]-q['scalars'][n*18+f]); compared+=1
                if maxima[f] is None or delta>maxima[f]: maxima[f]=delta; witnesses[f]=n
        i=(n//20000)*4+n%4; t32=f32units(w[b+19]); t=t32<<925; x=r['exact'][n]; y=q['exact'][n]
        coverage[i]+=1; positives[i]+=t>0; sums[i]+=t32
        for name,d in [('TR',t-x),('TQ',t-y),('QR',y-x)]: totals['l1'+name][i]+=abs(d); totals['signed'+name][i]+=d
    eq(a['stageMaxAbsTQ'],maxima,'saved-stage-maxima',label); eq(a['stageMaxAbsTQWitness'],witnesses,'saved-stage-maxima-witness',label)
    eq(a['codeCounts'],code_counts,'GPU-code-counts',label); eq(a['statusCounts'],statuses,'GPU-status-counts',label)
    eq(a['completeTermCoverage'],sum(coverage)==N,'GPU-coverage',label)
    failures+=sum(coverage)!=N
    for i,d in enumerate(a['rotors']):
        for k,v in [('index',i),('receiverID',IDS[i//4]),('rotor',i%4),('qualifiedTermCount',coverage[i]),('positiveTerms',positives[i])]: eq(d[k],v,'GPU-rotor-metadata',label)
        for k,v in totals.items(): cert(d,k,v[i])
        cert(d,'exactStoredTermSum',sums[i],-149); cert(d,'l1PlusAllowance',totals['l1TR'][i]+ALLOW)
        passed=totals['l1TR'][i]+ALLOW<=EPS and coverage[i]==5000
        eq(d['pass'],passed,'GPU-term-gate',{'stage':label,'rotor':i}); failures+=totals['l1TR'][i]+ALLOW>EPS
    report(a,label+'-terms',failures,{'gpuTermRecordsChecked':N,'numericFieldsChecked':N*18,'gpuDyadicTermRows':sum(coverage),'gpuExactStoredTermAdds':sum(coverage),'gpuStageComparisons':compared})
    g={'words':w,'floats':floats,'sums':sums,'totals':totals,'pass':failures==0}; GPUS[label]=g
    return g

def serial(label,g):
    w=values(label+'-reduce-gpu.u32','I',128); a=rawj(label+'-serial-assessment'); failures=0
    r=REFS[label[:2]+'-R']
    for i,d in enumerate(a['rotors']):
        rec=list(w[i*8:i*8+8]); eq(rec[:6],[i//4,IDS[i//4],i%4,2,1,5000],'serial-record-metadata',label); eq(rec[7],4294967295,'serial-first-bad-slot',label)
        check(math.isfinite(f32(rec[6])) and f32(rec[6])>=0,'serial-sum-domain',label)
        s=f32units(rec[6])<<925; t=g['sums'][i]<<925; error=s-t; combined=g['totals']['l1TR'][i]+abs(error)+ALLOW
        for k,v in [('index',i),('receiverID',IDS[i//4]),('rotor',i%4),('rawSumWord',rec[6])]: eq(d[k],v,'serial-certificate-metadata',label)
        for k,v in [('serialSum',s),('exactStoredTermSum',t),('signedReductionError',error),('signedSerialTotalVsR',s-r['sums'][i]),('absoluteReductionError',abs(error)),('combinedConservativeError',combined)]: cert(d,k,v)
        for k in ('l1TR','l1TQ','l1QR'): cert(d,k,g['totals'][k][i])
        eq(d['pass'],combined<=EPS,'serial-conservative-gate',label); failures+=combined>EPS
    report(a,label+'-serial',failures,{'serialRecordsChecked':16,'serialDyadicGates':16})
    return failures==0

def reference_contrast(a_label,b_label,file):
    a=REFS[a_label]; b=REFS[b_label]; saved=rawj(file); l1=[0]*16; signed=[0]*16; maxima=[None]*18; witness=[None]*18; compared=0; mismatches=0
    for n in range(N):
        if n%4096==0: guard()
        ma=a['meta'][n*8+6]; mb=b['meta'][n*8+6]; mismatches+=ma!=mb
        for f in range(18):
            if ma&mb&(1<<f):
                compared+=1; d=abs(b['scalars'][n*18+f]-a['scalars'][n*18+f])
                if maxima[f] is None or d>maxima[f]: maxima[f]=d; witness[f]=n
        i=(n//20000)*4+n%4; delta=b['exact'][n]-a['exact'][n]; l1[i]+=abs(delta); signed[i]+=delta
    for k,v in [('available',True),('diagnosticOnly',True),('codeMismatchCount',sum(x!=y for x,y in zip(a['codes'],b['codes']))),('stageMaskMismatchCount',mismatches),('stageMaxAbs',maxima),('stageMaxAbsWitness',witness)]: eq(saved[k],v,'reference-contrast',file)
    for i,d in enumerate(saved['rotors']):
        eq(d['index'],i,'contrast-rotor-index',file); cert(d,'l1',l1[i]); cert(d,'signed',signed[i]); cert(d,'l1PlusAllowance',l1[i]+ALLOW); eq(d['withinUnchangedEpsilon'],l1[i]+ALLOW<=EPS,'diagnostic-contrast-gate',file)
    report(saved,file,0,{'comparisonTermRows':N,'comparisonStageFields':compared,'comparisonDyadicRows':N})

def vector_contrast(first,second,file):
    a=GPUS[first]; b=GPUS[second]; saved=rawj(file); rows=[{'scalarIndex':12+f,'compared':0,'rawWordDifferences':0,'numericDifferences':0,'maxAbsoluteDifference':None,'maxWitness':None} for f in range(6)]; masks=0
    for n in range(N):
        if n%4096==0: guard()
        base=n*26; ma=a['words'][base+6]; mb=b['words'][base+6]; masks+=(ma&258048)!=(mb&258048)
        for f,d in enumerate(rows):
            if ma&mb&(1<<(12+f)):
                wa=a['words'][base+20+f]; wb=b['words'][base+20+f]; va=a['floats'][base+20+f]; vb=b['floats'][base+20+f]
                d['compared']+=1; d['rawWordDifferences']+=wa!=wb; d['numericDifferences']+=va!=vb; delta=abs(vb-va)
                if d['maxAbsoluteDifference'] is None or delta>d['maxAbsoluteDifference']: d['maxAbsoluteDifference']=delta; d['maxWitness']=n
    eq(saved['fields'],rows,'saved-vector-contrast',file); eq(saved['maskMismatchRows'],masks,'vector-mask-mismatch',file)
    report(saved,file,0,{'vectorComparisonRows':N,'vectorComponentComparisons':sum(d['compared'] for d in rows)})

def identities(index):
    freeze=jread(BASE/'freeze.json'); eq(len(freeze['files']),53,'frozen-pin-count')
    indexed={(e['group'],e['label']):e for e in index['files']}
    for e in index['files']:
        p=pathlib.Path(e['path'])
        eq(p.stat().st_size,e['bytes'],'indexed-input-size',e['label'])
        eq(digest(p),e['sha256'],'indexed-input-hash',e['label'])
    for e in freeze['files']:
        p=REPO/e['path']; expected=indexed[('source',e['path'])]
        eq(expected['bytes'],e['bytes'],'frozen-pin-size',e['path'])
        eq(expected['sha256'],e['sha256'],'frozen-pin-hash',e['path'])
        archive=OUTPUT/'source-archive'/e['path']
        eq(digest(archive),e['sha256'],'source-archive-hash',e['path'])
    eq(len([e for e in index['files'] if e['group']=='raw']),185,'raw-file-count')
    expected_raw=sorted(e['label'] for e in index['files'] if e['group']=='raw')
    eq(sorted(p.name for p in RAW.iterdir()),expected_raw,'raw-inventory')
    eq(len(RESULT['files']),184,'embedded-raw-manifest-size')
    for e in RESULT['files']:
        row=indexed[('raw',e['name'])]
        eq({k:row[k] for k in ('bytes','sha256')},{k:e[k] for k in ('bytes','sha256')},'embedded-raw-manifest',e['name'])
    eq(len(set(e['name'] for e in RESULT['files'])),184,'manifest-unique-names')
    eq(set(e['name'] for e in RESULT['files'])|{'result.json'},set(expected_raw),'manifest-coverage')
    ledger=jread(BASE/'BYTE-ACCOUNTING.json')
    for row in ledger['typedRawFiles']:
        p=RAW/row['path']
        if p.exists(): eq(p.stat().st_size,row['bytes'],'frozen-typed-file-size',row['path'])
    eq((RAW/'result.json').read_bytes(),(BASE/'results/result.json').read_bytes(),'result-byte-copy')
    private={e['label']:pathlib.Path(e['path']) for e in index['files'] if e['group']=='private'}
    inv=jread(private['scientific-invocation']); receipt=jread(private['source-publication-receipt'])
    for obj in (inv,receipt):
        eq(obj['sourceCommit'],RESULT['sourceCommit'],'source-commit-receipt')
        eq(obj['freezeSHA256'],digest(BASE/'freeze.json'),'freeze-receipt')
    eq(receipt['localPinsVerified'],53,'source-publication-pins'); eq(receipt['independentlyRetrievedRemoteCommitAndExactFreeze'],True,'source-publication-remote-receipt')
    eq(inv['scientificInvocationsAllowed'],1,'invocation-attempt-contract'); eq(inv['retriesAllowed'],0,'invocation-attempt-contract')
    eq(inv['environment']['RESEARCH_SOURCE_COMMIT'],RESULT['sourceCommit'],'invocation-source-env')
    eq(inv['workingDirectory'],str(REPO),'invocation-working-directory')
    eq(inv['argv'][1],str(BASE.relative_to(REPO)/'source/run-once.py'),'invocation-launcher')
    eq(inv['argv'][3],str(BASE.relative_to(REPO)/'source/experiment.cjs'),'invocation-driver')
    started=rawj('started'); eq(started['sourceCommit'],RESULT['sourceCommit'],'started-commit'); eq(started['freezeSha256'],digest(BASE/'freeze.json'),'started-freeze')
    eq(started['config'],CONFIG,'started-config'); eq(RESULT['config'],CONFIG,'result-config')
    runtime=jread(BASE/'runtime-provenance.json'); eq(started['runtimePinsVerified'],runtime['pins'],'runtime-pin-receipt')
    served=rawj('served-source-contract'); eq(served['files'],RESULT['servedSources'],'served-source-copy')
    for e in served['files']:
        eq(digest(BASE/'source'/e['name']),e['sha256'],'served-source-hash',e['name']); eq((BASE/'source'/e['name']).stat().st_size,e['bytes'],'served-source-size',e['name'])
    return private

def encoding_certificates():
    original_constants=(BASE/'constants/frozen-original-constants.f64').read_bytes()
    packed_constants=(BASE/'constants/frozen-packed-constants.u32').read_bytes()
    eq(original_constants,b''.join(bytes.fromhex(e['float64LEHex']) for e in ENC['entries']),'constant-f64-encodings')
    eq(packed_constants,b''.join(struct.pack('<I',e['packedWord']) for e in ENC['entries']),'constant-f32-encodings')
    for e in ENC['entries']:
        eq(struct.pack('<d',e['original']).hex(),e['float64LEHex'],'constant-original-encoding')
        eq(word32(e['original']),e['packedWord'],'constant-rounding'); eq(f32(e['packedWord']),e['decoded'],'constant-decoding')
    for k,config_key in [('epsilonWake','epsilonWakeMps'),('referenceSumAllowance','referenceAllowanceMps')]:
        eq(ENC['constants'][k],CONFIG['gates'][config_key],'frozen-threshold-identity',k)
        eq(struct.pack('<d',ENC['constants'][k]).hex(),ENC['extra'][k]['float64LEHex'],'frozen-threshold-encoding',k)
    eq(rawj('original-constants'),ENC['constants'],'original-constants-copy'); eq(RESULT['constants'],ENC['constants'],'result-constants-copy')
    audit=rawj('generator-audit'); eq(RESULT['generator'],audit,'generator-report-copy')
    seed_digest=hashlib.sha256(('m31-coordinate-origin-v1\n'+RESULT['sourceCommit']+'\n').encode()).digest()
    seed=int.from_bytes(seed_digest[:4],'little'); eq(audit['seedDigestHex'],seed_digest.hex(),'seed-digest'); eq(audit['seedWordLE'],seed,'seed-word'); check(seed!=608897,'historical-seed-exclusion')
    eq(audit['shape'],[20,25,10],'generator-shape'); eq(audit['receiverIds'],IDS,'generator-receivers'); eq(audit['randomWords'],30000,'generator-random-count'); eq(audit['noRejectionOrReplacement'],True,'generator-no-redraw')
    canonical=values('generated-canonicalNumerators.i32','i',15000); translated=values('generated-translatedNumerators.i32','i',15000); ticks=values('generated-angleTicks.i32','i',15000)
    angles=values('generated-angles.f64','d',15000); residual=values('generated-translationResiduals.f64','d',15000)
    eq(list(values('generated-receiver-ids.u32','I',4)),IDS,'saved-receiver-ids')
    states=[values(f'o{o}-states.f64','d',85000) for o in range(2)]
    rng=seed
    def random_word():
        nonlocal rng
        rng=(rng+0x6d2b79f5)&0xffffffff
        t=((rng^(rng>>15))*(rng|1))&0xffffffff
        t=(t ^ ((t+(((t^(t>>7))*(t|61))&0xffffffff))&0xffffffff))&0xffffffff
        return (t^(t>>14))&0xffffffff
    for n in range(5000):
        if n%512==0: guard()
        coordinates=[n%20,(n//20)%25,n//500]
        for f in range(3):
            k=n*3+f; jitter=random_word()%16385-8192
            eq(canonical[k]-131072*(2*coordinates[f]-([20,25,10][f]-1)),jitter,'saved-integer-recipe',k)
            check(abs(canonical[k])<2**22 and abs(translated[k])<2**27,'numerator-bounds',k)
            eq(translated[k]-canonical[k],[64,-32,16][f]*1048576,'integer-translation',k)
            for o,nums in enumerate((canonical,translated)):
                eq(f64units(states[o][n*17+f]),nums[k]<<(1074-20),'state-position-certificate',k)
            eq(f64units(states[1][n*17+f])-f64units(states[0][n*17+f]),[64,-32,16][f]<<1074,'dyadic-translation',k)
            eq(word64(residual[k]),0,'translation-residual-zero',k)
            eq(f32(word32(states[0][n*17+f])),states[0][n*17+f],'canonical-f32-exact',k)
        for f in range(3):
            word=random_word(); magnitude=(131072 if f<2 else 65536)+(word&0x7fffffff)%(262145 if f<2 else 11665409)
            eq(ticks[n*3+f],(-1 if word&0x80000000 else 1)*magnitude,'saved-attitude-integer-provenance',n*3+f)
            check(math.isfinite(angles[n*3+f]),'saved-angle-finite')
        for f in range(3,17):
            eq(word64(states[0][n*17+f]),word64(states[1][n*17+f]),'state-origin-copy',n)
            check(math.isfinite(states[0][n*17+f]),'state-finite',n)
            if f in (3,4,5,10,11,12): eq(word64(states[0][n*17+f]),0,'state-zero-fields',n)
            if f>=13: eq(states[0][n*17+f],ENC['constants']['f0'],'state-frozen-force',n)
    for k,v in [('exactTranslationCount',15000),('canonicalF32ExactCount',15000),('positionDenominator',1048576),('angleTickDenominator',65536),('rollPitchMagnitudeTicks',[131072,393216]),('yawMagnitudeTicks',[65536,11730944])]: eq(audit[k],v,'generator-audit-certificate',k)
    packing=[]; prepared={}
    for o in range(2):
        prepared[o]={}
        for ref in ('R','Q0','Q1'):
            p={k:values(f'o{o}-{ref}-prepared-{k}.f64','d',length) for k,length in [('nodes',40000),('offsets',64),('constants',16),('axis-metrics',15000)]}
            eq(list(values(f'o{o}-{ref}-prepared-ids.u32','I',4)),IDS,'prepared-ids'); prepared[o][ref]=p
            check(all(math.isfinite(v) for arr in p.values() for v in arr),'prepared-finite',f'o{o}-{ref}')
            # Saved metrics are admitted as values; no norm, margin or axis is reconstructed.
            check(all(p['axis-metrics'][3*i]>0 and p['axis-metrics'][3*i+2]>=0 for i in range(5000)),'saved-axis-metric-admission',f'o{o}-{ref}')
        p=prepared[o]; packed={}
        for arm,stride in [('AB',8),('C',12)]:
            packed[arm]={k:values(f'o{o}-packed{arm}-{k}.u32','I',length) for k,length in [('nodes',5000*stride),('offsets',64),('constants',16),('ids',4)]}
            eq(list(packed[arm]['ids']),IDS,'packed-ids')
        for field in ('offsets','constants','ids'): eq(packed['AB'][field].tobytes(),packed['C'][field].tobytes(),'shared-packed-fields',field)
        eq(p['R']['constants'].tobytes(),original_constants,'prepared-original-constants')
        eq(packed['AB']['constants'].tobytes(),packed_constants,'prepared-packed-constants')
        qc=dict(ENC['constants'])
        for e in ENC['entries']:
            if e['name'] in qc: qc[e['name']]=e['decoded']
        eq(rawj(f'o{o}-packed-constants'),qc,'decoded-constants-json')
        for field in ('nodes','offsets','constants'):
            for i,v in enumerate(p['R'][field]):
                eq(packed['AB'][field][i],word32(v),'packed-rounding',field)
                eq(word64(p['Q0'][field][i]),word64(f32(packed['AB'][field][i])),'packed-decoding',field)
        for field in ('offsets','constants','axis-metrics'): eq(p['Q0'][field].tobytes(),p['Q1'][field].tobytes(),'Q-nonposition-copy',field)
        pack_res=values(f'o{o}-positionPackingResiduals.f64','d',15000); recon_res=values(f'o{o}-reconstructionResiduals.f64','d',15000)
        nonzero=0; max_low=0.; max_res=0.
        for n in range(5000):
            if n%512==0: guard()
            eq(list(packed['C']['nodes'][n*12:n*12+8]),list(packed['AB']['nodes'][n*8:n*8+8]),'C-base-word-copy',n)
            eq(packed['C']['nodes'][n*12+11],0,'C-padding',n)
            for f in range(8):
                i=n*8+f
                if f>=3: eq(word64(p['Q0']['nodes'][i]),word64(p['Q1']['nodes'][i]),'Q-axis-padding-copy',n)
                if f>=6: eq(word64(p['R']['nodes'][i]),0,'prepared-padding',n)
                if f<3:
                    k=n*3+f; original=p['R']['nodes'][i]; high=p['Q0']['nodes'][i]; low_word=packed['C']['nodes'][n*12+8+f]; low=f32(low_word)
                    eq(word64(original),word64(states[o][n*17+f]),'prepared-state-position',k)
                    eq(low_word,word32(original-high),'split-low-encoding',k)
                    check(abs(low)<=2**-17,'split-low-bound',k)
                    eq(f64units(high)+f64units(low),f64units(original),'exact-high-low-reconstruction',k)
                    eq(word64(p['Q1']['nodes'][i]),word64(original),'Q1-exact-original-position',k)
                    eq(f64units(pack_res[k]),f64units(high)-f64units(original),'packing-residual-certificate',k)
                    eq(word64(recon_res[k]),0,'reconstruction-residual-zero',k)
                    nonzero+=pack_res[k]!=0; max_low=max(max_low,abs(low)); max_res=max(max_res,abs(pack_res[k]))
        a=rawj(f'o{o}-packing-audit')
        for k,v in [('exactReconstructionCount',15000),('ordinaryPackingNonzeroCount',nonzero),('maxAbsLow',max_low),('maxAbsPackingResidual',max_res),('lowBound',2**-17),('sharedAxesOffsetsConstants',True)]: eq(a[k],v,'packing-audit',k)
        packing.append(nonzero)
    for ref in ('R','Q0','Q1'):
        for field in ('offsets','constants','axis-metrics'): eq(prepared[0][ref][field].tobytes(),prepared[1][ref][field].tobytes(),'origin-dependent-preparation-copy',ref+'-'+field)
        for n in range(5000): eq(prepared[0][ref]['nodes'][n*8+3:n*8+8].tobytes(),prepared[1][ref]['nodes'][n*8+3:n*8+8].tobytes(),'origin-axis-copy',ref)
    stimulus={'canonicalPackingExact':packing[0]==0,'translatedPackingLoss':packing[1]>0,'bothReconstructionsExact':FAIL['exact-high-low-reconstruction']==0,'translationExact':FAIL['dyadic-translation']==0}
    eq(rawj('stimulus'),stimulus,'stimulus-flags'); eq(RESULT['stimulus'],stimulus,'result-stimulus-copy')

def lifecycle():
    cap=rawj('capability'); eq(RESULT['capability'],{k:v for k,v in cap.items() if k!='browserVersion'},'capability-copy'); eq(cap['browserVersion'],RESULT['browserVersion'],'capability-browser-version')
    for k,v in [('supported',True),('compiled',True),('messages',[]),('validation',None),('loss',None),('uncaptured',None)]: eq(cap[k],v,'capability-admission',k)
    eq(cap['adapter']['isFallbackAdapter'],False,'adapter-fallback'); eq(RESULT['browserVersion'],jread(BASE/'runtime-provenance.json')['chromeBundleVersion'],'browser-version')
    limits=cap['adapter']['deviceLimits']
    check(limits['maxStorageBufferBindingSize']>=8320000 and limits['maxBufferSize']>=8320000 and limits['maxComputeWorkgroupsPerDimension']>=1250 and limits['maxStorageBuffersPerShaderStage']>=7,'device-resource-limits')
    cost=dict(pipelineCreations=7,bufferCreations=0,allocatedBytes=0,uploadedBytes=0,clearedBytes=0,readbackBytes=0,dispatches=0,activeOutputSlots=0,launchedInvocations=0,peakLiveBufferBytes=0,liveBufferBytes=0)
    eq(cap['costs'],cost,'capability-costs')
    def allocate(size,count=1):
        cost['bufferCreations']+=count; cost['allocatedBytes']+=size; cost['liveBufferBytes']+=size; cost['peakLiveBufferBytes']=max(cost['peakLiveBufferBytes'],cost['liveBufferBytes'])
    def health(d,label):
        for k in ('validation','loss','uncaptured'):
            if k in d: eq(d[k],None,'API-health',label+'-'+k)
    def readback(label,kind,arm,cell,count,size,groups):
        cost['dispatches']+=1; cost['activeOutputSlots']+=count; cost['launchedInvocations']+=groups*64
        allocate(size); cost['readbackBytes']+=size
        rb=rawj(label+'-readback'); eq(rb['bytes'],size,'readback-size',label)
        eq(rb['dispatch'],{'kind':kind,'arm':arm,'cell':cell,'count':count,'groups':groups,'outputBytes':size,'submitted':True,'materializedTermsPreserved':kind=='reduce'},'dispatch-provenance',label)
        eq(rb['costs'],cost,'readback-cost-snapshot',label)
        cost['liveBufferBytes']-=size
        api=rawj(label+'-api'); health(api,label); eq(api['costs'],cost,'API-cost-snapshot',label)
        eq(api['stage'],{'controls':'controls-ready','terms':'terms-read','reduce':'sums-read'}[kind],'API-stage',label)
    allocate(64+3200+2080,3); cost['uploadedBytes']+=64+3200
    initial=rawj('GPU-controls-buffer-contract'); health(initial,'controls-buffer'); eq(initial['sizes'],{'constants':64,'controls':3200,'controlOutputs':2080},'control-buffer-sizes'); eq(initial['costs'],cost,'control-buffer-costs')
    for arm in 'ABC': cost['clearedBytes']+=2080; readback('controls-'+arm,'controls',arm,None,20,2080,1)
    cost['liveBufferBytes']-=3200+2080
    for label in GPUS:
        arm=label[-1]; sizes={'nodes':240000 if arm=='C' else 160000,'offsets':256,'ids':16,'terms':8320000,'sums':512}
        allocate(sum(sizes.values()),5); cost['uploadedBytes']+=sizes['nodes']+256+16
        bc=rawj(label+'-buffer-contract'); health(bc,label); eq(bc['key'],label,'buffer-cell-identity'); eq(bc['sizes'],sizes,'cell-buffer-sizes',label); eq(bc['costs'],cost,'cell-buffer-costs',label)
        readback(label+'-terms','terms',arm,label,N,8320000,1250)
        reduction=(RAW/(label+'-reduce-gpu.u32')).exists()
        if reduction: readback(label+'-reduce','reduce',arm,label,16,512,1)
        cost['liveBufferBytes']-=sum(sizes.values())
        release=rawj(label+'-disposition')['release']; eq(release,{'key':label,'arm':arm,'origin':int(label[1]),'reductionDispatched':reduction,'costs':cost},'cell-release-costs',label)
    final=rawj('final-gpu-health'); health(final,'final'); eq(final['stage'],'idle','GPU-idle'); eq(final['current'],None,'GPU-no-current-cell'); eq(final['seenControls'],list('ABC'),'GPU-controls-ledger'); eq(final['seenCells'],list(GPUS),'GPU-cell-ledger'); eq(final['costs'],cost,'GPU-final-costs')
    eq(RESULT['costs'],cost,'result-GPU-costs'); reconciliation=rawj('cost-reconciliation')
    eq(reconciliation,{'expected':cost,'observed':cost,'cellCount':len(GPUS)},'GPU-cost-reconciliation'); eq(RESULT['costReconciliation'],reconciliation,'result-cost-reconciliation-copy')
    gpu_caps=jread(BASE/'BYTE-ACCOUNTING.json')['GPU']
    for key,limit in [('pipelineCreations','pipelineCreations'),('bufferCreations','maximumBufferCreations'),('allocatedBytes','maximumCumulativeAllocatedBytes'),('uploadedBytes','maximumCumulativeUploadedBytes'),('readbackBytes','maximumCumulativeReadbackBytes'),('clearedBytes','maximumClearedControlOutputBytes'),('peakLiveBufferBytes','maximumLiveBufferBytes'),('dispatches','maximumComputeDispatches')]: check(cost[key]<=gpu_caps[limit],'GPU-resource-cap',key)
    return cost

def decisions_and_counts(useful):
    dispositions=[]; serial_count=0
    for o in range(2):
        for arm in 'ABC':
            label=f'o{o}-{arm}'; d=rawj(label+'-disposition'); q='Q1' if arm=='C' else 'Q0'
            for k,v in [('origin',o),('arm',arm),('key',label),('reference',q)]: eq(d[k],v,'cell-provenance',label)
            if not REFS[f'o{o}-{q}']['pass']:
                expected='skipped-interface-gate'; qualified=False
                check(not (RAW/(label+'-terms-gpu.u32')).exists(),'typed-skip-no-terms',label)
                check('terms' not in d and 'serial' not in d and 'release' not in d,'typed-skip-no-stage-record',label)
            else:
                eq(d['terms'],rawj(label+'-terms-assessment'),'disposition-terms-copy',label)
                if GPUS[label]['pass']:
                    serial_count+=1; eq(d['serial'],rawj(label+'-serial-assessment'),'disposition-serial-copy',label)
                    qualified=d['serial']['pass']; expected='qualified' if qualified else 'failed-combined-error'
                else:
                    expected='failed-term-gate'; qualified=False
                    eq(d.get('serial'),None,'failed-term-no-serial-record',label)
            if not qualified and expected!='failed-combined-error':
                check(not (RAW/(label+'-reduce-gpu.u32')).exists(),'typed-skip-no-reduction',label)
            eq(d['status'],expected,'cell-disposition',label); eq(d['qualified'],qualified,'cell-qualification',label); dispositions.append(d)
    eq(RESULT['cells'],dispositions,'result-dispositions-copy')
    qualified={arm:all(d['qualified'] for d in dispositions if d['arm']==arm) for arm in 'ABC'}
    candidate=None if qualified['A'] else ('B' if qualified['B'] else ('C' if qualified['C'] else None))
    decision='baseline-already-qualifies' if qualified['A'] else ('candidate-earns-separate-fresh-confirmation' if candidate else 'no-candidate')
    eq(RESULT['qualifiedArms'],qualified,'qualified-arms'); eq(RESULT['candidate'],candidate,'candidate'); eq(RESULT['decision'],decision,'candidate-decision'); eq(RESULT['pass'],all(qualified.values()),'result-numerical-pass')
    eq(RESULT['status'],'completed-numerical-comparison','terminal-status'); eq(RESULT['terminal'],True,'terminal-closure'); eq(RESULT['invocationComplete'],True,'invocation-complete'); eq(RESULT['useful'],all(useful),'useful-copy')
    for o in range(2):
        for ref in ('R','Q0','Q1'): eq(RESULT['references'][o][ref],rawj(f'o{o}-{ref}-assessment'),'embedded-reference-copy')
        eq(RESULT['references'][o]['usefulness'],rawj(f'o{o}-usefulness-assessment'),'embedded-usefulness-copy')
        eq(RESULT['references'][o]['packing'],rawj(f'o{o}-packing-audit'),'embedded-packing-copy')
    for arm in 'ABC': eq(RESULT['controls'][arm],rawj('controls-'+arm+'-assessment'),'embedded-controls-copy')
    # Count observable operation dimensions and checked saved assessments; no physical arithmetic.
    expected={'freshGeneratorCalls':1,'generationSeedHashes':1,'generationStates':5000,'generationRandomWords':30000,'generationCoordinateCertificates':15000,'generationQuaternions':5000,'originalPreparationCalls':1,'originalStateAdmissions':5000,'originalQuaternionNorms':5000,'originalAxisRotations':5000,'RAxisMetrics':5000,'originalOffsetRotations':16,'translationPreparationCalls':1,'translatedPreparedFloatCopies':55080,'translatedPreparedIdCopies':4,'translatedStateAdmissions':5000,'translatedPositionWrites':15000,'packingCalls':2,'packedFloatWords':80160,'decodedNodeAdmissions':10000,'decodedOffsetAdmissions':32,'Q0AxisMetrics':10000,'Q1PreparedFloatCopies':110160,'Q1PreparedIdCopies':8,'splitBaseWordCopies':80000,'splitLowFloatWords':30000,'splitCoordinateCertificates':30000,'splitBaseWordComparisons':80000,'QInterfaceNonpositionComparisons':80168,'hostReferencePasses':6,'dispatches':3+len(GPUS)+serial_count,'gpuLaunchedInvocations':3*64+len(GPUS)*80000+serial_count*64,'gpuPaddingInvocations':3*44+serial_count*48,'gpuControlSlots':60,'gpuCellPreparations':len(GPUS),'gpuPairSlots':len(GPUS)*80000,'gpuSumReadReservation':serial_count*80000,'gpuSumSlots':serial_count*16}
    for ref in ('R','Q0','Q1'):
        for name,key in [('PairSlots','reservedPairSlots'),('CenterChecks','centerChecks'),('WorldPoints','worldPoints'),('RotorVisits','rotorVisits'),('ProfileEvaluations','profileEvaluations'),('SumTermVisits','profileEvaluations')]: expected[ref+name]=sum(REFS[f'o{o}-{ref}']['counts'][key] for o in range(2))
    def kind(label):
        if label.startswith('controls-'): return 'controls'
        if label.endswith('-usefulness'): return 'usefulness'
        if label.endswith('-terms'): return 'terms'
        if label.endswith('-serial'): return 'serial'
        if '-vectors-' in label: return 'gpuContrast'
        if label.endswith('-assessment'): return 'referenceContrast'
        return 'R' if label.endswith('-R') else 'Q'
    for label,a in ASSESSMENTS:
        k=kind(label); counter='assessmentCalls:'+k; expected[counter]=expected.get(counter,0)+1
        for name,n in a['counts'].items(): key='assessmentActual:'+name; expected[key]=expected.get(key,0)+n
        for name,n in CONFIG['assessmentReservations'][k].items(): key='assessmentReserved:'+name; expected[key]=expected.get(key,0)+n
    eq(RESULT['counts'],expected,'complete-observed-counter-reconciliation')
    for key,n in expected.items():
        if key.startswith('assessmentActual:'):
            suffix=key.split(':',1)[1]; check(n<=expected['assessmentReserved:'+suffix] and n<=CONFIG['assessmentLimits'][suffix],'assessment-reservation-cap',key)
        elif key.startswith('assessmentReserved:'):
            check(n<=CONFIG['assessmentLimits'][key.split(':',1)[1]],'assessment-reservation-cap',key)
        else: check(n<=CONFIG['limits'][key],'driver-operation-cap',key)
    for k in ('roots','integrationSteps'): eq(RESULT['counts'].get(k,0),0,'no-extra-science',k)

def science_closure(private,index):
    budget=jread(BASE/'results/budget.json')
    for k,v in [('terminal',True),('active',False),('attempts',1),('wallCapSeconds',180),('rawByteCap',268435456),('resultByteCap',33554432),('status','closed'),('timeout',False),('outputCapExceeded',False),('exitCode',0),('retryPermitted',False),('rawWithinCap',True),('resultsWithinCap',True)]: eq(budget[k],v,'science-closure',k)
    check(0<=RESULT['elapsedSeconds']<=budget['wallSeconds']<=180,'science-wall-cap')
    rawfiles=[e for e in index['files'] if e['group']=='raw']; resultfiles=[e for e in index['files'] if e['group']=='result']
    for k,v in [('rawFiles',len(rawfiles)),('rawBytes',sum(e['bytes'] for e in rawfiles)),('resultFiles',len(resultfiles)),('resultBytes',sum(e['bytes'] for e in resultfiles)),('resultBudgetBytes',(BASE/'results/budget.json').stat().st_size),('resultNonBudgetBytes',sum(e['bytes'] for e in resultfiles if e['label']!='budget.json'))]: eq(budget[k],v,'science-output-accounting',k)
    postrun=[e for e in index['files'] if e['group']=='postrun-provenance']
    eq({e['label'] for e in resultfiles},{'budget.json','result.json','scientific-stdout.txt','scientific-stderr.txt','sole-launch.lock'},'original-science-results-inventory')
    eq(sorted(p.name for p in (BASE/'results').iterdir()),sorted(e['label'] for e in resultfiles+postrun),'science-plus-postrun-results-inventory')
    entries=[json.loads(line) for line in private['process-registry'].read_text().splitlines() if line.strip()]
    cleanup=jread(private['process-cleanup']); eq(cleanup['entries'],entries,'private-process-entry-copy'); eq(cleanup['registryComplete'],True,'private-registry-complete'); eq(cleanup['launchError'],None,'private-process-launch-error')
    eq(pathlib.Path(cleanup['registry']).resolve(),private['process-registry'].resolve(),'private-registry-path-copy')
    eq(len(entries),1,'private-process-count'); eq(len(cleanup['cleanup']),2,'private-group-count')
    expected_groups={cleanup['nodePID']}|{e['pid'] for e in entries if e['detached']}
    eq({e['pgid'] for e in cleanup['cleanup']},expected_groups,'private-group-coverage')
    check(all(e['kind']=='chrome' and e['detached'] and e['ownership']['executable'] and e['ownership']['profileArgument'].startswith('--user-data-dir=') for e in entries),'private-process-ownership-records')
    observed={'registeredProcesses':len(entries),'registeredDetachedGroups':sum(e['detached'] for e in entries),'registryComplete':cleanup['registryComplete'],'groupsChecked':len(cleanup['cleanup']),'killSignalsSent':sum(e['killSent'] for e in cleanup['cleanup']),'ownershipChecksPassed':sum(e['ownershipVerified'] for e in cleanup['cleanup']),'errors':[],'confirmedAbsent':all(e['confirmedAbsent'] for e in cleanup['cleanup'])}
    eq(budget['processGroupCleanup'],observed,'process-closure-reconciliation'); check(observed['confirmedAbsent'],'process-closure-absent')
    eq(rawj('process-registration-summary'),{'registeredProcesses':len(entries),'registeredDetachedGroups':sum(e['detached'] for e in entries),'registeredBrowser':any(e['kind']=='chrome' for e in entries)},'public-process-summary')
    check(not pathlib.Path(index['absentPrivateException']).exists(),'private-exception-absent')
    # These are historical receipts. No live process or private identifier is emitted.

def main():
    global REPO,BASE,RAW,OUTPUT,ENC,EPS,ALLOW,CONFIG,RESULT,PHASE
    parser=argparse.ArgumentParser(); parser.add_argument('--repo',required=True); parser.add_argument('--campaign',required=True); parser.add_argument('--input-index',required=True); parser.add_argument('--output',required=True)
    args=parser.parse_args(); REPO=pathlib.Path(args.repo); BASE=REPO/args.campaign; RAW=BASE/'raw'; OUTPUT=pathlib.Path(args.output)
    with open(OUTPUT/'checker.once.lock','x') as f: f.write('Permanent sole saved-evidence review lock; never remove or retry.\n')
    index=jread(args.input_index); RESULT=rawj('result'); CONFIG=jread(BASE/'config.json'); ENC=jread(BASE/'constants/constant-encodings.json')
    EPS=f64units(struct.unpack('<d',bytes.fromhex(ENC['extra']['epsilonWake']['float64LEHex']))[0]); ALLOW=f64units(struct.unpack('<d',bytes.fromhex(ENC['extra']['referenceSumAllowance']['float64LEHex']))[0])
    PHASE='identities'; private=identities(index)
    PHASE='encoding-certificates'; encoding_certificates()
    PHASE='references'; useful=[]
    for o in range(2):
        r=load_reference(f'o{o}-R'); qualify_reference(f'o{o}-R',r)
        for q in ('Q0','Q1'): v=load_reference(f'o{o}-{q}'); qualify_reference(f'o{o}-{q}',v,r)
        useful.append(usefulness(o))
    PHASE='literal-controls'; controls()
    PHASE='GPU-saved-records'
    for o in range(2):
        for arm in 'ABC':
            label=f'o{o}-{arm}'
            if (RAW/(label+'-terms-gpu.u32')).exists():
                g=gpu_cell(o,arm)
                if (RAW/(label+'-reduce-gpu.u32')).exists(): serial(label,g)
    PHASE='saved-contrasts'
    for o in range(2): reference_contrast(f'o{o}-Q0',f'o{o}-Q1',f'o{o}-Q1-Q0-assessment')
    reference_contrast('o0-R','o1-R','R-origin-contrast-assessment')
    vector_contrast('o0-A','o0-B','o0-B-A-vectors-assessment'); vector_contrast('o0-B','o0-C','o0-C-B-vectors-assessment')
    PHASE='decision-and-resources'; decisions_and_counts(useful); lifecycle(); science_closure(private,index)
    PHASE='complete'; guard()

if __name__=='__main__':
    fatal=None
    try: main()
    except BaseException as e:
        # Exception text/tracebacks can contain private paths: retain only class and phase.
        fatal={'exceptionClass':type(e).__name__,'phase':PHASE,'checkerFrames':[{'function':f.name,'line':f.lineno} for f in traceback.extract_tb(e.__traceback__) if pathlib.Path(f.filename).name=='checker.py'][-8:]}
        FAIL['fatal-incomplete-review']+=1
    finished=time.monotonic()
    science=globals().get('RESULT',{})
    result={'review':'sole-independent-saved-evidence-review','terminal':True,'completed':PHASE=='complete','evidenceIntegrityPass':not any(FAIL.values()),'integrityFailureCounts':dict(FAIL),'integrityWitnesses':WITNESSES,'witnessCap':64,'checkCounts':dict(CHECKS),'numericalNegatives':NEGATIVES,'scientificQualification':{'recordedCandidate':science.get('candidate'),'recordedDecision':science.get('decision'),'recordedAllArmsQualified':science.get('pass'),'decisionVerified':PHASE=='complete' and not any(FAIL.values())},'fatal':fatal,'elapsedSeconds':finished-START,'cooperativeCapSeconds':86,'scope':'Saved bytes and receipts only; no scientific model reconstructed. Exact sums are internal numerical consistency, not physical validation. Origins share dependent preparation. Unexecuted stages remain absent. Historical process closure is reconciled from receipts, not re-probed.','sourceIndependence':'Independent Python logic; no scientific source imported, executed, or copied into assessment functions.'}
    destination=globals().get('OUTPUT')
    if destination is not None:
        payload=(json.dumps(result,indent=2,sort_keys=True)+'\n').encode()
        if len(payload)>1024*1024: raise RuntimeError('bounded review report exceeded')
        with open(destination/'report.json','xb') as f: f.write(payload)
    print(json.dumps({'completed':result['completed'],'evidenceIntegrityPass':result['evidenceIntegrityPass'],'numericalNegativeStages':len(NEGATIVES),'elapsedSeconds':result['elapsedSeconds'],'fatal':fatal},sort_keys=True))
    sys.exit(0 if result['evidenceIntegrityPass'] and result['completed'] else 1)

