"""One prospectively supervised saved-data review. Never import scientific code.

Only file identities, saved typed values, classifications and exact dyadic
arithmetic are inspected. No geometry, profile, root, shader or state generation.
"""
import argparse, collections, hashlib, json, math, pathlib, struct, sys, time

N = 5000
M = 80000
IDS = [27, 445, 4500, 988]
NONE = 0xffffffff
CAMPAIGN = 'research/m31-browser-wake-slice-2026-10-16'
EXPECTED_SOURCE = '4767787487fc7f8c3a8e8189523b1299c9c7f190'
EXPECTED_FREEZE = '5862d96e2556d58852f7b1d3a65e00e5303c8061e137f27280041156191c282f'
MAX_OUTPUT = 14 * 1024 * 1024
MAX_EXAMPLES = 64
START = None
REPORT = None
CACHE = {}

def sha(data):
    return hashlib.sha256(data).hexdigest()

def check(ok, label, detail=None):
    REPORT['checks'] += 1
    if not ok:
        REPORT['integrityFailures'] += 1
        if len(REPORT['integrityExamples']) < MAX_EXAMPLES:
            REPORT['integrityExamples'].append({'issue': label, 'detail': detail})
    return bool(ok)

def finding(ok, label, detail=None):
    REPORT['scientificChecks'] += 1
    if not ok:
        REPORT['scientificFindings'] += 1
        if len(REPORT['scientificExamples']) < MAX_EXAMPLES:
            REPORT['scientificExamples'].append({'issue': label, 'detail': detail})
    return bool(ok)

def guard():
    if time.perf_counter() - START > 55:
        raise RuntimeError('Saved review cooperative ceiling')

def read(path):
    path = pathlib.Path(path)
    key = str(path.resolve())
    if key not in CACHE:
        CACHE[key] = path.read_bytes()
    return CACHE[key]

def obj(path):
    return json.loads(read(path))

def raw_words(data, width):
    if len(data) % width:
        raise ValueError('Nonintegral typed byte length')
    return [x[0] for x in struct.iter_unpack('<I' if width == 4 else '<Q', data)]

def finite_bits(word, width):
    return ((word >> (23 if width == 4 else 52)) & (255 if width == 4 else 2047)) != (255 if width == 4 else 2047)

def units(word, width):
    """Exact integer in 2^-1074 units; no floating arithmetic in a gate."""
    frac_bits, exp_bits = (23, 8) if width == 4 else (52, 11)
    exponent = (word >> frac_bits) & ((1 << exp_bits) - 1)
    if exponent == (1 << exp_bits) - 1:
        raise ValueError('Nonfinite dyadic operand')
    fraction = word & ((1 << frac_bits) - 1)
    magnitude = fraction if exponent == 0 else ((1 << frac_bits) + fraction) << (exponent - 1)
    if width == 4:
        magnitude <<= 925
    return -magnitude if word >> (width * 8 - 1) else magnitude

def number(word, width):
    return struct.unpack('<f' if width == 4 else '<d', word.to_bytes(width, 'little'))[0]

def float_word(value):
    return int.from_bytes(struct.pack('<d', value), 'little')

def cert(value, exponent=-1074):
    return {'coefficient': str(value if exponent == -1074 else value >> 925), 'exponent': exponent}

def certify(saved, value, label, exponent=-1074):
    expected = cert(value, exponent)
    ok = isinstance(saved, dict) and saved.get('coefficient') == expected['coefficient'] and saved.get('exponent') == exponent
    check(ok, 'Exact certificate ' + label)
    if isinstance(saved, dict) and 'approximateDisplay' in saved:
        check(isinstance(saved['approximateDisplay'], (int, float)) and math.isfinite(saved['approximateDisplay']), 'Finite certificate display ' + label)

def expected_mask(code, is_self):
    return (2048 if is_self else 2049) if code == 0 else {1:2051, 2:2051, 3:7, 4:2055, 5:2127, 6:4095, 7:4095}.get(code)

def numeric_fields(words, mask, width, label, slot, shader_bounds=False):
    values = []
    ok = finding((mask & ~4095) == 0, label + ' defined validity mask', {'slot':slot})
    upper = [512,1024,2048,8,4,4,64,128,3,1.0010000467300415,1.0010000467300415,128]
    for f, word in enumerate(words):
        if not (mask & (1 << f)):
            ok = finding(word == 0, label + ' unavailable payload is raw +0', {'slot':slot,'field':f}) and ok
            values.append(None)
            continue
        valid = finite_bits(word, width)
        ok = finding(valid, label + ' reached field finite', {'slot':slot,'field':f}) and ok
        if not valid:
            values.append(None)
            continue
        v = number(word, width)
        values.append(v)
        if shader_bounds:
            valid = (f in (1,4) or v >= 0) and abs(v) <= upper[f] and (f not in (3,6) or v > 0)
            ok = finding(valid, label + ' reached scalar bounds', {'slot':slot,'field':f}) and ok
    return ok, values

def valid_record(meta, scalar_words, width, slot, label, ref_codes=None):
    i, source, rotor = slot // 20000, (slot // 4) % N, slot % 4
    receiver = IDS[i]
    ok = finding(list(meta[:4]) == [slot,receiver,source,rotor], label + ' slot identity', {'slot':slot})
    status, code, mask, flags = meta[4:8]
    expected_route = 1 if source == receiver else (2 if code == 0 else 0)
    ok = finding(mask == expected_mask(code, source == receiver), label + ' policy mask', {'slot':slot}) and ok
    ok = finding((flags & ~15) == 0 and (flags & 3) == expected_route and (code >= 6 or (flags & 12) == 0), label + ' routing', {'slot':slot}) and ok
    numeric_ok, values = numeric_fields(scalar_words, mask, width, label, slot, width == 4)
    ok = numeric_ok and ok
    term, projection = values[11], values[5]
    if code in (0,1,2,4,5):
        valid = status == 3 and term == 0
    elif code == 6:
        valid = status == 4 and term == 0 and projection == 0
    elif code == 7:
        valid = projection is not None and projection > 0 and ((status == 4 and term == 0) or (status == 5 and term is not None and term > 0))
    else:
        valid = False
    ok = finding(valid and (mask & 2048) != 0, label + ' valid summand status/sign', {'slot':slot,'status':status,'code':code}) and ok
    if ref_codes is not None:
        ok = finding(all(code == codes[slot] for codes in ref_codes), label + ' reference policy equality', {'slot':slot,'code':code}) and ok
    return ok, values

def phase_report(name, present=False, complete=False, passed=None):
    entry = {'present':present,'complete':complete,'pass':passed}
    REPORT['exposure'][name] = entry
    return entry

def raw_obj(raw, name):
    p = raw / name
    return obj(p) if p.exists() else None

def prepared_checks(base, raw, label, C):
    names = ['nodes','offsets','constants','ids','axis-metrics']
    paths = {n:raw/(label+'-prepared-'+n+('.u32' if n == 'ids' else '.f64')) for n in names}
    if not all(p.exists() for p in paths.values()):
        return
    check(read(paths['ids']) == b''.join(i.to_bytes(4,'little') for i in IDS), label+' prepared ID bytes')
    for name, limit, stride in [('nodes',128,8),('offsets',.1,4),('constants',None,16),('axis-metrics',None,3)]:
        words = raw_words(read(paths[name]),8)
        for index,w in enumerate(words):
            if index % 8192 == 0: guard()
            finite = finite_bits(w,8)
            check(finite,label+' prepared finite '+name,{'index':index})
            if not finite: continue
            v = number(w,8)
            if name == 'nodes':
                check(abs(v) <= (128 if index%8 < 3 else 1.01) if index%8 < 6 else w == 0,label+' node bound/padding',{'index':index})
            elif name == 'offsets':
                check(abs(v) <= .1 if index%4 < 3 else w == 0,label+' offset bound/padding',{'index':index})
            elif name == 'axis-metrics' and index%3 == 2:
                check(v >= 0,label+' saved tilt margin',{'node':index//3})
    if label == 'R':
        check(read(paths['constants']) == read(base/'constants/frozen-original-constants.f64'),'R frozen constant bytes')
    else:
        for key in ['nodes','offsets','constants']:
            packed = raw_words(read(raw/('packed-'+key+'.u32')),4)
            decoded = raw_words(read(paths[key]),8)
            original = raw_words(read(raw/('R-prepared-'+key+'.f64')),8)
            check(len(packed)==len(decoded)==len(original),'Q packing shape '+key)
            for i,(pw,qw,rw) in enumerate(zip(packed,decoded,original)):
                check(finite_bits(pw,4),'Packed finite word',{'field':key,'index':i})
                if not finite_bits(pw,4) or not finite_bits(rw,8): continue
                check(float_word(number(pw,4))==qw,'Exact decoded Q word',{'field':key,'index':i})
                rounded = int.from_bytes(struct.pack('<f',number(rw,8)),'little')
                check(rounded==pw,'Original-to-packed IEEE encoding',{'field':key,'index':i})
        check(read(raw/'packed-constants.u32')==read(base/'constants/frozen-packed-constants.u32'),'Packed constant bytes')
        check(read(raw/'packed-ids.u32')==read(paths['ids']),'Packed ID bytes')

def reference(raw, label):
    filenames = [label+'-'+s for s in ['metadata.u32','scalars.f64','codes.u8','terms.f64','ordinarySums.f64','compensatedSums.f64','sumValidity.u8','counts.json']]
    present = any((raw/n).exists() for n in filenames)
    phase_report(label,present)
    if not present: return None
    complete_files = all((raw/n).exists() for n in filenames)
    check(complete_files,label+' reference file set')
    if not complete_files: return None
    meta_bytes,scalar_bytes,codes,term_bytes,ordinary,compensated,validity = [read(raw/n) for n in filenames[:-1]]
    sizes = [M*32,M*96,M,M*8,128,128,16]
    if not check([len(x) for x in [meta_bytes,scalar_bytes,codes,term_bytes,ordinary,compensated,validity]]==sizes,label+' byte shape'): return None
    count_doc = obj(raw/filenames[-1]);complete=count_doc.get('complete') is True
    phase_report(label,True,complete)
    words = raw_words(term_bytes,8); exact_terms = [None]*M; sums=[0]*16
    codes_count=[0]*8;statuses=[0]*7;qualified=0;positive=0;eligible=set();profile=0
    before=REPORT['scientificFindings']
    for n in range(M):
        if n%4096==0:guard()
        meta=struct.unpack_from('<8I',meta_bytes,n*32);scalars=struct.unpack_from('<12Q',scalar_bytes,n*96)
        status,code,mask,flags=meta[4:8]
        if status<7:statuses[status]+=1
        if code<8:codes_count[code]+=1
        if status in (3,4,5):
            ok,values=valid_record(meta,scalars,8,n,label)
            ok=finding(codes[n]==code,label+' code byte',{'slot':n}) and ok
            ok=finding(words[n]==scalars[11],label+' term duplicate bit identity',{'slot':n}) and ok
            if finite_bits(words[n],8):
                exact_terms[n]=units(words[n],8);sums[n//20000*4+n%4]+=exact_terms[n]
            if ok:qualified+=1
            if values[11] is not None and values[11]>0:positive+=1
            if code>=6:profile+=1
            if code!=0:eligible.add((n//20000,(n//4)%N))
        else:
            finding(not complete,label+' complete reference has invalid/unwritten slot',{'slot':n,'status':status})
            numeric_fields(scalars,mask,8,label,n)
            check((mask&2048)==0 and words[n]==0,label+' invalid term placeholder',{'slot':n})
    if complete:
        finding(qualified==M,label+' full qualified reference coverage')
        check(validity==bytes([1]*16),label+' complete sum validity')
        expected={'reservedPairSlots':M,'initializedSlots':M,'validSlots':M,'centerChecks':19996,'rotorVisits':4*len(eligible),'profileEvaluations':profile,'positiveTerms':positive,'eligibleSources':len(eligible),'worldPoints':16,'codeCounts':codes_count,'statusCounts':statuses}
        check(count_doc['counts']==expected,label+' reconstructed reference counts')
        check(count_doc.get('failure') is None,label+' complete reference failure marker')
    ordinary_words=raw_words(ordinary,8);comp_words=raw_words(compensated,8)
    check(all(finite_bits(w,8) for w in ordinary_words+comp_words),label+' finite stored sums')
    result={'codes':codes,'meta':meta_bytes,'scalars':scalar_bytes,'terms':exact_terms,'sum':sums,'ordinary':ordinary_words,'compensated':comp_words,'validity':validity,'complete':complete,'qualified':qualified,'recordPass':complete and REPORT['scientificFindings']==before,'counts':count_doc['counts']}
    return result

def verify_threshold(report,epsilon,allowance,label):
    if report is not None and 'threshold' in report:
        certify(report['threshold'].get('epsilon'),epsilon,label+' epsilon')
        certify(report['threshold'].get('referenceSumAllowance'),allowance,label+' allowance')

def reference_assessments(base,raw,R,Q,epsilon,allowance):
    results={}
    if R is not None:
        report=raw_obj(raw,'R-assessment.json');check(report is not None,'R assessment available')
        if report is not None and R['complete']:
            saved_codes=b''.join(read(base/'selection'/('selected-'+str(i)+'-codes.u8')) for i in range(4))
            prior_words=raw_words(b''.join(read(base/'selection'/('selected-'+str(i)+'-saved-sums.f64')) for i in range(4)),8)
            before=REPORT['scientificFindings'];finding(R['codes']==saved_codes,'R saved-I code reproduction')
            rows=[]
            for i in range(16):
                prior,ordinary,comp = [units(w,8) for w in [prior_words[i],R['ordinary'][i],R['compensated'][i]]]
                gaps=[R['sum'][i]-prior,ordinary-R['sum'][i],comp-R['sum'][i]]
                passed=all(abs(x)<=allowance for x in gaps)
                finding(passed,'R exact prior-I/ordinary/compensated allowance',{'index':i})
                a,b=number(R['ordinary'][i],8),number(prior_words[i],8)
                finding(abs(a-b)<=1e-11+1e-12*max(abs(a),abs(b)),'R declared ordinary reproduction tolerance',{'index':i})
                finding(abs(a-number(R['compensated'][i],8))<=number(float_word(1e-12),8),'R ordinary/compensated diagnostic',{'index':i})
                s=report['exactStoredSumDiagnostics'][i]
                for key,value in zip(['exactStoredSum','signedStoredMinusPriorI','signedOrdinaryMinusStored','signedCompensatedMinusStored'],[R['sum'][i]]+gaps):certify(s.get(key),value,'R '+str(i)+' '+key)
                check(s.get('pass')==passed and s.get('index')==i,'R row disposition',{'index':i})
                rows.append({'index':i,'exactStoredSum':cert(R['sum'][i]),'priorIGap':cert(gaps[0]),'pass':passed})
            certify(report.get('referenceSumAllowance'),allowance,'R allowance')
            passed=R['recordPass'] and REPORT['scientificFindings']==before
            check(report.get('pass')==passed,'R assessment disposition')
            phase_report('R',True,True,passed);REPORT['RExactRows']=rows;results['R']=passed
        elif report is not None:
            check(report.get('pass') is False,'Incomplete R cannot qualify');phase_report('R',True,False,False)
    if R is not None and Q is not None:
        report=raw_obj(raw,'Q-assessment.json');check(report is not None,'Q assessment available')
        if report is not None and R['complete'] and Q['complete']:
            before=REPORT['scientificFindings'];finding(R['codes']==Q['codes'],'Q/R exact policy equality')
            l1=[0]*16;signed=[0]*16
            for n,(r,q) in enumerate(zip(R['terms'],Q['terms'])):
                if n%8192==0:guard()
                if r is None or q is None:continue
                i=n//20000*4+n%4;l1[i]+=abs(q-r);signed[i]+=q-r
            verify_threshold(report,epsilon,allowance,'Q');rows=[]
            for i in range(16):
                og=units(Q['ordinary'][i],8)-Q['sum'][i];cg=units(Q['compensated'][i],8)-Q['sum'][i]
                sum_pass=abs(og)<=allowance and abs(cg)<=allowance
                passed=l1[i]+allowance<=epsilon and sum_pass
                finding(passed,'Exact packing L1 plus reference allowance',{'index':i})
                for ref in [R,Q]:finding(abs(number(ref['ordinary'][i],8)-number(ref['compensated'][i],8))<=1e-12,'Q reference sum diagnostic',{'index':i})
                s=report['rotors'][i]
                pairs={'l1QR':l1[i],'signedQR':signed[i],'exactStoredSumR':R['sum'][i],'exactStoredSumQ':Q['sum'][i],'signedOrdinaryQMinusStored':og,'signedCompensatedQMinusStored':cg,'l1PlusAllowance':l1[i]+allowance}
                for key,value in pairs.items():certify(s.get(key),value,'Q '+str(i)+' '+key)
                check(s.get('index')==i and s.get('pass')==passed and s.get('sumPass')==sum_pass,'Q rotor disposition',{'index':i})
                rows.append({'index':i,'l1QR':cert(l1[i]),'signedQR':cert(signed[i]),'pass':passed})
            passed=R['recordPass'] and Q['recordPass'] and REPORT['scientificFindings']==before
            check(report.get('pass')==passed,'Q assessment disposition');phase_report('Q',True,True,passed);REPORT['QExactRows']=rows;results['Q']=passed
        elif report is not None:
            check(report.get('pass') is False,'Incomplete Q cannot qualify');phase_report('Q',True,False,False)
    return results

def controls_review(base,raw):
    p=raw/'controls-gpu.u32';phase_report('controls',p.exists())
    if not p.exists():return
    data=read(p);report=raw_obj(raw,'controls-assessment.json');spec=obj(base/'controls/controls.json')
    if not check(len(data)==1280,'Control output shape'):return
    before=REPORT['scientificFindings']
    keys=['ordinal','receiverID','sourceID','rotor','status','policyCode','validityMask','routingFlags']
    for i,c in enumerate(spec['controls']):
        words=struct.unpack_from('<20I',data,80*i)
        finding(list(words[:8])==[c['expected'][k] for k in keys],'Control exact metadata',{'control':i})
        _,v=numeric_fields(words[8:],words[6],4,'control',i,True)
        term=v[11];valid=(words[6]&2048)!=0;assertion=c['expected']['termAssertion']
        good=(valid and term==0) if assertion=='zero-valid' else ((valid and term is not None and term>0) if assertion=='finite-strictly-positive' else (not valid and words[19]==0))
        finding(good,'Control term assertion',{'control':i})
    passed=REPORT['scientificFindings']==before
    check(report is not None,'Control assessment exists')
    if report is not None:check(report.get('pass')==passed,'Control assessment disposition')
    phase_report('controls',True,True,passed)

def terms_review(raw,R,Q,epsilon,allowance):
    p=raw/'terms-gpu.u32';phase_report('terms',p.exists())
    if not p.exists():return None
    data=read(p);report=raw_obj(raw,'terms-assessment.json')
    if not check(len(data)==M*80 and R is not None and Q is not None,'GPU terms/references shape'):return None
    before=REPORT['scientificFindings'];qualified=[0]*16;positive=[0]*16;sums=[0]*16;codes=[0]*8;statuses=[0]*7
    metrics={k:[0]*16 for k in ['l1TR','l1TQ','l1QR','signedTR','signedTQ','signedQR']}
    stage_max=[None]*12;stage_witness=[None]*12
    for n in range(M):
        if n%4096==0:guard()
        words=struct.unpack_from('<20I',data,80*n);i=n//20000*4+n%4
        if words[5]<8:codes[words[5]]+=1
        if words[4]<7:statuses[words[4]]+=1
        ok,v=valid_record(words[:8],words[8:],4,n,'GPU term',[R['codes'],Q['codes']])
        qm=struct.unpack_from('<8I',Q['meta'],n*32);qw=struct.unpack_from('<12Q',Q['scalars'],n*96)
        for f,value in enumerate(v):
            if value is not None and qm[6]&(1<<f) and finite_bits(qw[f],8):
                delta=abs(value-number(qw[f],8))
                if stage_max[f] is None or delta>stage_max[f]:stage_max[f]=delta;stage_witness[f]=n
        if not ok or R['terms'][n] is None or Q['terms'][n] is None:continue
        t=units(words[19],4);r=R['terms'][n];q=Q['terms'][n];qualified[i]+=1;sums[i]+=t
        positive[i]+=int(t>0)
        for suffix,diff in [('TR',t-r),('TQ',t-q),('QR',q-r)]:metrics['l1'+suffix][i]+=abs(diff);metrics['signed'+suffix][i]+=diff
    record_pass=REPORT['scientificFindings']==before
    complete=all(x==N for x in qualified);finding(complete,'Full qualified GPU term coverage')
    check(report is not None,'GPU term assessment exists')
    if report is None:return None
    verify_threshold(report,epsilon,allowance,'terms')
    check(report.get('completeTermCoverage')==complete,'Reported GPU qualified coverage')
    check(report.get('codeCounts')==codes and report.get('statusCounts')==statuses,'GPU class/status counts')
    check(report.get('stageMaxAbsTQ')==stage_max and report.get('stageMaxAbsTQWitness')==stage_witness,'Saved stage maxima and witnesses')
    rows=[];all_gates=True
    for i in range(16):
        total=metrics['l1TR'][i]+allowance;passed=total<=epsilon and qualified[i]==N;all_gates=all_gates and passed
        finding(passed,'Exact pre-reduction T-R L1 gate',{'index':i,'receiverID':IDS[i//4],'rotor':i%4,'l1PlusAllowance':cert(total),'epsilon':cert(epsilon)})
        s=report['rotors'][i]
        check([s.get('index'),s.get('receiverID'),s.get('rotor'),s.get('qualifiedTermCount'),s.get('positiveTerms'),s.get('pass')]==[i,IDS[i//4],i%4,qualified[i],positive[i],passed],'Term rotor metadata/disposition',{'index':i})
        for key,values in metrics.items():certify(s.get(key),values[i],'terms '+str(i)+' '+key)
        certify(s.get('exactStoredTermSum'),sums[i],'terms exact sum '+str(i),-149);certify(s.get('l1PlusAllowance'),total,'terms gate '+str(i))
        rows.append({'index':i,'receiverID':IDS[i//4],'rotor':i%4,'qualifiedTermCount':qualified[i],'positiveTerms':positive[i],'l1PlusAllowance':cert(total),'pass':passed,**{k:cert(v[i]) for k,v in metrics.items()},'exactStoredTermSum':cert(sums[i])})
    passed=record_pass and complete and all_gates
    check(report.get('pass')==passed,'Term assessment disposition')
    phase_report('terms',True,complete,passed);REPORT['termExactRows']=rows
    REPORT['termCoverage']={'qualified':sum(qualified),'positive':sum(positive),'codeCounts':codes,'statusCounts':statuses}
    return {'sum':sums,'metrics':metrics,'pass':passed}

def serial_review(raw,term,epsilon,allowance):
    p=raw/'reduce-gpu.u32';phase_report('serial',p.exists())
    if not p.exists():return
    data=read(p);report=raw_obj(raw,'serial-assessment.json')
    if not check(len(data)==512 and term is not None,'Serial input shape'):return
    before=REPORT['scientificFindings'];rows=[];verify_threshold(report,epsilon,allowance,'serial')
    finding(term['pass'],'Reduction requires passing term stage')
    for i in range(16):
        words=struct.unpack_from('<8I',data,32*i);meta_ok=list(words[:6])==[i//4,IDS[i//4],i%4,2,1,N] and words[7]==NONE
        finding(meta_ok,'Serial metadata',{'index':i})
        numeric=finite_bits(words[6],4) and (not(words[6]>>31) or (words[6]&0x7fffffff)==0)
        finding(numeric,'Serial finite nonnegative sum',{'index':i})
        if not numeric:continue
        s=units(words[6],4);err=s-term['sum'][i];combined=term['metrics']['l1TR'][i]+abs(err)+allowance;passed=meta_ok and combined<=epsilon
        finding(passed,'Exact combined term-plus-addition gate',{'index':i})
        if report is not None:
            row=report['rotors'][i]
            values={'serialSum':s,'exactStoredTermSum':term['sum'][i],'signedReductionError':err,'signedSerialTotalVsR':term['metrics']['signedTR'][i]+err,'absoluteReductionError':abs(err),'combinedConservativeError':combined}
            for key,value in values.items():certify(row.get(key),value,'serial '+str(i)+' '+key)
            check(row.get('pass')==passed and row.get('rawSumWord')==words[6],'Serial row disposition',{'index':i})
        rows.append({'index':i,'signedReductionError':cert(err),'combinedConservativeError':cert(combined),'pass':passed})
    passed=REPORT['scientificFindings']==before
    check(report is not None and report.get('pass')==passed,'Serial assessment disposition')
    phase_report('serial',True,len(rows)==16,passed);REPORT['serialExactRows']=rows

def process_review(index, budget):
    private=index['private']
    cleanup=obj(private['cleanup']['path']);registry=[json.loads(line) for line in read(private['registry']['path']).splitlines() if line]
    invocation=obj(private['invocation']['path'])
    check(invocation.get('sourceCommit')==EXPECTED_SOURCE and invocation.get('sourceFreezeSHA256')==EXPECTED_FREEZE,'Original private scientific invocation binding')
    check(invocation.get('terminalBudget')==budget,'Private invocation terminal ledger identity')
    check(cleanup.get('entries')==registry and cleanup.get('registryComplete') is True,'Private registry/cleanup correspondence')
    details=cleanup.get('cleanup',[]);public=budget['processGroupCleanup']
    check(len(details)==public.get('groupsChecked'),'Private/public group count')
    check(len(registry)==public.get('registeredProcesses'),'Private/public process count')
    check(sum(bool(e.get('detached') and e.get('pid')) for e in registry)==public.get('registeredDetachedGroups'),'Private/public detached count')
    check(sum(bool(x.get('killSent')) for x in details)==public.get('killSignalsSent'),'Private/public signals')
    check(sum(bool(x.get('ownershipVerified')) for x in details)==public.get('ownershipChecksPassed'),'Private/public ownership count')
    for entry in registry:
        check(isinstance(entry.get('pid'),int) and entry['pid']>0,'Registered positive process identifier')
        if entry.get('kind')=='chrome':
            owner=entry.get('ownership',{})
            check(entry.get('detached') is True and isinstance(owner.get('executable'),str) and owner['executable'].endswith('/Google Chrome') and isinstance(owner.get('profileArgument'),str) and owner['profileArgument'].startswith('--user-data-dir='),'Private registered browser identity')
    group_ids={cleanup.get('nodePID')}|{e['pid'] for e in registry if e.get('detached') and isinstance(e.get('pid'),int)}
    check({x.get('pgid') for x in details}==group_ids,'All known groups represented')
    check(all(x.get('confirmedAbsent') is True for x in details),'Private absence confirmation')
    check(all(not x.get('killSent') or x.get('ownershipVerified') for x in details),'Only owned cleanup signals')
    check(public.get('registryComplete') is True and public.get('confirmedAbsent') is True and public.get('errors')==[],'Public process cleanup qualification')
    REPORT['processSummary']={k:public.get(k) for k in ['registeredProcesses','registeredDetachedGroups','groupsChecked','killSignalsSent','ownershipChecksPassed','registryComplete','confirmedAbsent']}

def accounting_review(base,raw,result,budget,R,Q):
    cfg=obj(base/'config.json');counts=result.get('counts',{});limits=cfg['limits']
    for name,value in counts.items():
        if name.startswith('assessmentReserved:') or name.startswith('assessmentActual:'):
            limit=cfg['assessmentLimits'].get(name.split(':',1)[1])
        else:limit=limits.get(name)
        check(isinstance(value,int) and value>=0 and limit is not None and value<=limit,'Attempt counter cap',{'name':name})
    stages=[(name,raw_obj(raw,name+'-assessment.json')) for name in ['R','Q','controls','terms','serial']]
    expected_reserved=collections.Counter();expected_actual=collections.Counter()
    for name,report in stages:
        if report is None:continue
        expected_reserved.update(cfg['assessmentReservations'][name])
        for key,value in report.get('counts',{}).items():
            check(isinstance(value,int) and 0<=value<=cfg['assessmentReservations'][name].get(key,-1),'Stage assessment actual cap',{'stage':name,'name':key})
            expected_actual[key]+=value
        field={'R':'R','Q':'Q','controls':'controls','terms':'terms','serial':'serial'}[name]
        check(result.get(field)==report,'Inline assessment matches saved report',{'stage':name})
        check(len(report.get('witnesses',[]))<=32 and report.get('witnessCap')==32,'Assessment witness cap',{'stage':name})
    for prefix,expected in [('assessmentReserved:',expected_reserved),('assessmentActual:',expected_actual)]:
        observed={k[len(prefix):]:v for k,v in counts.items() if k.startswith(prefix)}
        check(observed==dict(expected),'Aggregate assessment accounting '+prefix)
    for label,ref in [('R',R),('Q',Q)]:
        if ref is None or not ref['complete']:continue
        expected={'PairSlots':M,'CenterChecks':19996,'WorldPoints':16,'RotorVisits':ref['counts']['rotorVisits'],'ProfileEvaluations':ref['counts']['profileEvaluations'],'SumTermVisits':ref['counts']['profileEvaluations']}
        for suffix,value in expected.items():check(counts.get(label+suffix)==value,'Reference callback count '+label+suffix)
    for name,value in [('originalStateAdmissions',5000),('originalQuaternionNorms',5000),('originalAxisRotations',5000),('originalOffsetRotations',16),('RAxisMetrics',5000),('QAxisMetrics',5000),('packedFloatWords',40080),('decodedNodeAdmissions',5000),('decodedOffsetAdmissions',16)]:
        if (raw/'Q-prepared-nodes.f64').exists():check(counts.get(name)==value,'Complete preparation count '+name)
    submitted=[]
    for kind,slots,groups,padding in [('controls',16,1,48),('terms',80000,1250,0),('reduce',16,1,48)]:
        side=raw_obj(raw,kind+'-readback.json');api=raw_obj(raw,kind+'-api.json');data_path=raw/(kind+'-gpu.u32')
        if side is None:
            check(not data_path.exists(),'No unpaired GPU raw output '+kind)
            continue
        d=side['dispatch'];submitted.append(kind)
        check(d.get('submitted') is True and d.get('kind')==kind and d.get('count')==slots and d.get('groups')==groups and d.get('outputBytes')==data_path.stat().st_size and side.get('bytes')==data_path.stat().st_size,'GPU readback declaration '+kind)
        if kind=='reduce':check(d.get('materializedTermsPreserved') is True,'Retained materialized term marker')
        check(api is not None,'GPU API result '+kind)
        if api is not None:finding(not api.get('validation') and not api.get('loss') and not api.get('uncaptured'),'GPU API health '+kind)
    expected_dispatches=len(submitted)
    check(counts.get('dispatches')==expected_dispatches,'Dispatch attempt/readback coverage for saved terminal prefix')
    check(counts.get('gpuControlSlots')==(16 if 'controls' in submitted else 0) and counts.get('gpuPairSlots')==(80000 if 'terms' in submitted else 0) and counts.get('gpuSumSlots')==(16 if 'reduce' in submitted else 0),'Active GPU slot accounting')
    check(counts.get('gpuLaunchedInvocations',0)==sum(80000 if k=='terms' else 64 for k in submitted),'Launched GPU invocations')
    check(counts.get('gpuPaddingInvocations',0)==sum(0 if k=='terms' else 48 for k in submitted),'Padded GPU invocations')
    check(counts.get('gpuSumReadReservation',0)==(80000 if 'reduce' in submitted else 0),'Reduction read reservation')
    check(counts.get('roots')==0 and counts.get('integrationSteps')==0,'No roots or integration')
    raw_files=[p for p in raw.iterdir() if p.is_file()];total=sum(p.stat().st_size for p in raw_files)
    check(total==budget.get('rawBytes') and len(raw_files)==budget.get('rawFiles'),'External raw-byte ledger')
    check(total<=limits['rawBytes'],'Raw evidence ceiling')
    check(budget.get('terminal') is True and budget.get('active') is False and budget.get('attempts')==1 and budget.get('retryPermitted') is False,'Terminal sole-attempt ledger')
    check(budget.get('timeout') is False and 0<=budget.get('wallSeconds',math.inf)<60,'External science wall ceiling')
    check(result.get('terminal') is True and 0<=result.get('elapsedSeconds',math.inf)<60,'Driver terminal/wall ceiling')
    REPORT['resourceSummary']={'dispatches':expected_dispatches,'rawFiles':len(raw_files),'rawBytes':total,'externalWallSeconds':budget.get('wallSeconds'),'driverWallSeconds':result.get('elapsedSeconds'),'roots':0,'integrationSteps':0,'timingInterpretation':'Bookkeeping only; no performance comparison'}

def main(args):
    repo=pathlib.Path(args.repo).resolve();base=repo/CAMPAIGN;raw=base/'raw'
    index=obj(args.input_index);index_bytes=read(args.input_index)
    REPORT.update(sourceCommit=args.source_commit,freezeSha256=args.freeze_sha256,inputIndexSha256=sha(index_bytes),checkerSha256=sha(pathlib.Path(__file__).read_bytes()))
    check(sha(index_bytes)==args.input_index_sha256,'Prospective terminal evidence index identity')
    check(args.source_commit==EXPECTED_SOURCE and args.freeze_sha256==EXPECTED_FREEZE,'Prospective source/freeze identity')
    freeze_bytes=read(base/'freeze.json');check(sha(freeze_bytes)==EXPECTED_FREEZE,'Frozen manifest bytes')
    freeze=json.loads(freeze_bytes);check(len(freeze.get('files',[]))==82,'Frozen pin count')
    seen=set()
    for pin in freeze['files']:
        guard();p=(repo/pin['path']).resolve();check(repo in p.parents and pin['path'] not in seen,'Contained unique frozen pin');seen.add(pin['path']);data=read(p)
        check(len(data)==pin['bytes'] and sha(data)==pin['sha256'],'Frozen source/input pin',{'path':pin['path']})
    check(index.get('sourceCommit')==EXPECTED_SOURCE and index.get('freezeSha256')==EXPECTED_FREEZE,'Input index binding')
    for pin in index['files']:
        p=(repo/pin['path']).resolve();check(repo in p.parents,'Contained science evidence pin');data=read(p)
        check(len(data)==pin['bytes'] and sha(data)==pin['sha256'],'Terminal evidence pin',{'path':pin['path']})
    for name,pin in index['private'].items():
        data=read(pin['path']);check(len(data)==pin['bytes'] and sha(data)==pin['sha256'],'Private evidence identity '+name)
    if REPORT['integrityFailures']:raise ValueError('Identity checks failed before typed decoding')
    cfg=obj(base/'config.json');check(cfg['receiverIds']==IDS and cfg['nSlots']==M and cfg['nSources']==N,'Frozen cohort and slots')
    result=obj(raw/'result.json');budget=obj(base/'results/budget.json');started=obj(raw/'started.json')
    check(read(raw/'result.json')==read(base/'results/result.json'),'Raw/public result byte identity')
    check(result.get('sourceCommit')==EXPECTED_SOURCE and started.get('sourceCommit')==EXPECTED_SOURCE and started.get('freezeSha256')==EXPECTED_FREEZE,'Result source/freeze identity')
    check(result.get('config')==cfg and started.get('config')==cfg,'Frozen config copied exactly')
    file_pins=result.get('files',[]);actual={p.name for p in raw.iterdir() if p.is_file()}-{'result.json'}
    check({x['name'] for x in file_pins}==actual and len(file_pins)==len(actual),'Complete driver raw file inventory')
    for pin in file_pins:
        data=read(raw/pin['name']);check(len(data)==pin['bytes'] and sha(data)==pin['sha256'],'Driver raw digest',{'name':pin['name']})
    fixed=obj(base/'BYTE-ACCOUNTING.json')['fixedTypedRawFiles']
    for row in fixed:
        p=raw/row['name']
        if p.exists():check(len(read(p))==row['bytes'],'Fixed typed-file size',{'name':row['name']})
    enc=obj(base/'constants/constant-encodings.json');C=enc['constants'];epsilon=units(int.from_bytes(bytes.fromhex(enc['extra']['epsilonWake']['float64LEHex']),'little'),8);allowance=units(int.from_bytes(bytes.fromhex(enc['extra']['referenceSumAllowance']['float64LEHex']),'little'),8)
    check(obj(raw/'original-constants.json')==C,'Original frozen constant object')
    for label in ['R','Q']:prepared_checks(base,raw,label,C)
    qc=raw_obj(raw,'Q-constants.json')
    if qc is not None:
        for entry in enc['entries'][:14]:
            check(float_word(qc[entry['name']])==float_word(number(entry['packedWord'],4)),'Decoded constant object '+entry['name'])
        for key in enc['extra']:check(float_word(qc[key])==int.from_bytes(bytes.fromhex(enc['extra'][key]['float64LEHex']),'little'),'Original allocation metadata retained in Q '+key)
    if (raw/'R-prepared-nodes.f64').exists():
        source_states=read(repo/cfg['sourceReferenceDirectory']/'raw'/(cfg['sourceCase']+'-states.f64'));prepared_nodes=read(raw/'R-prepared-nodes.f64')
        check(len(source_states)==N*17*8,'Original state byte shape')
        for i in range(N):
            check(source_states[i*136:i*136+24]==prepared_nodes[i*64:i*64+24],'Original position byte transfer',{'node':i})
    check(read(raw/'selected-ids.u32')==b''.join(i.to_bytes(4,'little') for i in IDS),'Saved selected IDs')
    if (raw/'packed-controls.u32').exists():check(read(raw/'packed-controls.u32')==read(base/'controls/controls.u32'),'Uploaded control byte identity')
    served=raw_obj(raw,'served-source-contract.json')
    if served is not None:
        for record in served['files']:
            data=read(base/'source'/record['name']);check(len(data)==record['bytes'] and sha(data)==record['sha256'],'Served frozen source '+record['name'])
        check(sorted(x['name'] for x in result.get('servedSources',[]))==['browser.html','browser.js','wake.wgsl'],'Exactly one frozen source delivery each')
    cap=raw_obj(raw,'capability.json')
    if cap is not None:
        check(cap.get('browserVersion')==obj(base/'runtime-provenance.json')['chromeBundleVersion'],'Pinned browser version')
        if cap.get('supported'):
            finding(cap.get('compiled') is True and not cap.get('validation') and not cap.get('loss') and not cap.get('uncaptured'),'Compilation/API capability')
            check(cap.get('adapter',{}).get('isFallbackAdapter') is False,'Nonfallback adapter evidence')
            for source in ['limits','deviceLimits']:
                limits=cap['adapter'][source]
                check(limits['maxStorageBufferBindingSize']>=6400000 and limits['maxBufferSize']>=6400000 and limits['maxComputeWorkgroupsPerDimension']>=1250 and limits['maxStorageBuffersPerShaderStage']>=5,'Declared adapter/device limits '+source)
    prep=raw_obj(raw,'GPU-buffer-contract.json')
    if prep is not None:
        check(prep.get('sizes')=={'constants':64,'nodes':160000,'offsets':256,'ids':16,'terms':6400000,'controls':2048,'controlOutputs':1280,'sums':512},'GPU buffer capacities')
        finding(not prep.get('validation') and not prep.get('loss') and not prep.get('uncaptured'),'GPU preparation API health')
    failure_evidence=raw_obj(raw,'browser-failure-evidence.json')
    if failure_evidence is not None:
        health=failure_evidence.get('health') or {};finding(not health.get('loss') and not health.get('uncaptured'),'Failure-prefix GPU health')
    R=reference(raw,'R');Q=reference(raw,'Q');reference_assessments(base,raw,R,Q,epsilon,allowance);controls_review(base,raw);terms=terms_review(raw,R,Q,epsilon,allowance);serial_review(raw,terms,epsilon,allowance)
    process_review(index,budget);accounting_review(base,raw,result,budget,R,Q)
    stages=REPORT['exposure'];failed=[k for k in ['R','Q','controls','terms','serial'] if stages[k]['pass'] is False]
    if failed:
        first=failed[0];order=['R','Q','controls','terms','serial'];later=order[order.index(first)+1:]
        check(all(not stages[k]['present'] for k in later),'No stage after first failed scientific gate')
        check(result.get('pass') is False and result.get('status')=='failed' and budget.get('exitCode')!=0,'Recorded negative scientific disposition')
        if first=='terms':
            check(result.get('error',{}).get('message')=='GPU term qualification','Term gate failure context')
            check(result.get('error',{}).get('detail')==raw_obj(raw,'terms-assessment.json'),'Term failure detail retains complete assessment')
            check(not (raw/'serial-assessment.json').exists() and not (raw/'reduce-api.json').exists(),'Reduction remains unexecuted')
    all_pass=all(stages[k]['complete'] and stages[k]['pass'] is True for k in stages)
    if all_pass:check(result.get('pass') is True and result.get('status')=='completed' and budget.get('exitCode')==0,'Full successful disposition')
    REPORT['fullSuiteQualified']=all_pass and REPORT['integrityFailures']==0 and REPORT['scientificFindings']==0
    REPORT['reviewPass']=REPORT['integrityFailures']==0
    REPORT['status']=('consistent-full-pass' if REPORT['fullSuiteQualified'] else ('consistent-recorded-negative' if failed else 'consistent-incomplete')) if REPORT['reviewPass'] else 'inconsistent'
    REPORT['firstFailedStage']=failed[0] if failed else None
    REPORT['availableStageQualification']={k:v['pass'] for k,v in stages.items()}
    REPORT['exposureStatus']='complete' if all(v['complete'] for v in stages.values()) else 'partial'
    REPORT['limitations']=['Saved operands only; no fresh model reconstruction.','The four receivers are deliberately exposed cases, not holdouts.','Incomplete or unexecuted stages provide no numerical qualification.','Physical accuracy, force composition, portability and performance are not established.','Cleanup was reviewed from saved provenance; no live process or failure-injection probe was performed.']

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--repo',required=True);parser.add_argument('--source-commit',required=True);parser.add_argument('--freeze-sha256',required=True);parser.add_argument('--input-index',required=True);parser.add_argument('--input-index-sha256',required=True);parser.add_argument('--output',required=True);parser.add_argument('--review-lock',required=True);args=parser.parse_args()
    START=time.perf_counter();REPORT={'terminal':False,'status':'running','reviewPass':False,'fullSuiteQualified':False,'checks':0,'scientificChecks':0,'integrityFailures':0,'scientificFindings':0,'integrityExamples':[],'scientificExamples':[],'exposure':{k:{'present':False,'complete':False,'pass':None} for k in ['R','Q','controls','terms','serial']},'fatal':None}
    try:
        with pathlib.Path(args.review_lock).open('x') as f:f.write('Permanent sole saved-review reservation. Never remove or rerun.\n')
        if pathlib.Path(args.output).exists():raise RuntimeError('Review output already exists')
        main(args)
    except BaseException as error:
        REPORT.update(status='review-failed',reviewPass=False,fullSuiteQualified=False,fatal={'type':type(error).__name__,'message':str(error)[:2000]})
    finally:
        REPORT['terminal']=True;REPORT['elapsedBeforeOutputSeconds']=time.perf_counter()-START
        payload=(json.dumps(REPORT,indent=2,allow_nan=False)+'\n').encode()
        if len(payload)>MAX_OUTPUT:
            payload=(json.dumps({'terminal':True,'status':'review-output-cap-failed','reviewPass':False,'fullSuiteQualified':False,'fatal':'Output exceeds 14MiB normal allocation'})+'\n').encode()
        with pathlib.Path(args.output).open('xb') as f:f.write(payload)
    print(json.dumps({k:REPORT[k] for k in ['status','reviewPass','fullSuiteQualified','checks','scientificChecks','integrityFailures','scientificFindings','fatal']}))
    sys.exit(0 if REPORT['reviewPass'] else 1)
