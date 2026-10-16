#!/usr/bin/env python3
"""Saved-only independent finite-runtime center-screen audit. No candidate imports."""
import argparse
import gzip
import hashlib
import importlib.metadata
import importlib.util
import json
import math
import platform
import re
import resource
import statistics
import sys
import time
from pathlib import Path
import numpy as np

MAX_TERMS=2_000_000
RSS_CAP=1610612736
COOPERATIVE_SECONDS=175
CASES=[('n1000-s261601-t2',1000,261601),('n5000-s261602-t2',5000,261602),('n5000-s261603-t2',5000,261603)]
PERMS=['LF','FL']
FULL_PHASES=['input','index','geometry','admission','setup','solve','residual','checksum','remainder']
OWNERSHIP=['L:sparse2','F:sparse2','L:planes62','F:planes62','L:fallback258','F:fallback258']
INHERITED_REFERENCE_SHA256='4b21e84674d0007e23641622aec52724bced4791fcca3c1b97d48189c21f6aeb'
INHERITED_REVIEW_SHA256='a6018cb1280bbe88182204d497ca4401cef8462588698a1c8aa082f8ecbb8bd5'

# This import is reached only by the separately authorized saved-review invocation.
reference_path=Path(__file__).with_name('numeric-reference.py')
if hashlib.sha256(reference_path.read_bytes()).hexdigest()!=INHERITED_REFERENCE_SHA256:
    raise RuntimeError('independent reference pin mismatch')
_spec=importlib.util.spec_from_file_location('pinned_independent_reference',reference_path)
_reference=importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_reference)
constants=_reference.constants
prepare_geometry=_reference.prepare_geometry
classify_receiver=_reference.classify_receiver
direct_solve=_reference.direct_solve
csr_map=_reference.csr_map

def require(ok, text):
    if not ok:
        raise ValueError(text)


def finite(value):
    return type(value) in (int, float) and math.isfinite(value)


def valid_sha(value):
    return isinstance(value, str) and re.fullmatch('[0-9a-f]{64}', value) is not None


def load_json(path):
    require(path.stat().st_size <= 132*(1 << 20), 'JSON exceeds result cap')
    def reject(value):
        raise ValueError('nonfinite JSON token '+value)
    with path.open(encoding='utf-8') as stream:
        return json.load(stream, parse_constant=reject)


def compare_fields(audit, actual, expected, prefix):
    """Compare only required fields; extra descriptive fields are allowed."""
    required(isinstance(actual, dict), prefix+' must be an object')
    for key, wanted in expected.items():
        name = prefix+'.'+key
        if key not in actual:
            audit.check(False, name+' present')
            continue
        got = actual[key]
        if isinstance(wanted, dict):
            compare_fields(audit, got, wanted, name)
        elif isinstance(wanted, float):
            audit.close(got, wanted, name)
        elif isinstance(wanted, bool):
            audit.check(type(got) is bool and got == wanted, name)
        elif isinstance(wanted, int):
            audit.check(type(got) is int and got == wanted, name)
        else:
            audit.check(got == wanted, name)


def input_census(states, g, c):
    finite = bool(np.all(np.isfinite(states)))
    qe = np.abs(g['qnorm']-1)
    ae = np.abs(g['anorm']-1)
    oe = np.abs(g['onorm']-c['D']/2)
    od = np.abs(g['perpendicular'])
    qb = int(np.count_nonzero(~np.isfinite(qe) | (qe > 1e-10)))
    ab = int(np.count_nonzero(~np.isfinite(ae) | (ae > 1e-9)))
    ob = int(np.count_nonzero(~np.isfinite(oe+od) |
                              (oe > 1e-9) | (od > 1e-9)))
    tilt_degrees = g['tilt']*(180/math.pi)
    return dict(finite=finite, quaternionNormMaxError=diagnostic_scalar(np.max(qe)),
                quaternionBadCount=qb, axisNormMaxError=diagnostic_scalar(np.max(ae)),
                axisBadCount=ab, offsetNormMaxError=diagnostic_scalar(np.max(oe)),
                offsetDotMaxAbs=diagnostic_scalar(np.max(od)), offsetBadCount=ob,
                nominalZeroCount=int(np.count_nonzero(g['f0'] == 0)),
                nominalNegativeCount=int(np.count_nonzero(g['f0'] < 0)),
                nominalPositive=bool(finite and np.all(g['f0'] > 0)),
                nominalTotalFinite=bool(np.all(np.isfinite(g['S0']))),
                geometryValid=bool(finite and qb == 0 and ab == 0 and ob == 0),
                maxTiltDegrees=diagnostic_scalar(np.max(tilt_degrees)),
                tiltWithin45Count=int(np.count_nonzero(tilt_degrees <= 45)))


def graph_census(positions, dependencies):
    n = len(positions)
    order = np.lexsort((np.arange(n), -positions[:, 2]))
    rank = np.empty(n, dtype=np.int64)
    rank[order] = np.arange(n)
    incoming = [len(sources) for sources in dependencies]
    height_violations = sum(int(np.count_nonzero(positions[sources, 2] <= positions[i, 2]))
                            for i, sources in enumerate(dependencies))
    order_violations = sum(int(np.count_nonzero(rank[sources] >= rank[i]))
                           for i, sources in enumerate(dependencies))
    eligible = order_violations == 0
    depth = None
    if eligible:
        depth = np.zeros(n, dtype=np.int64)
        for i in order:
            sources = dependencies[i]
            if len(sources):
                depth[i] = 1+np.max(depth[sources])
    return dict(uniqueVehicleEdges=sum(incoming), incomingDegree=incoming,
                maxIncomingDegree=max(incoming), heightViolationEdges=height_violations,
                orderViolationEdges=order_violations, descendingEligible=eligible,
                order=order.tolist(), dependencyDepth=None if depth is None else depth.tolist(),
                maxDependencyDepth=None if depth is None else int(np.max(depth)))


def rotor_arrays(record, n):
    rotors = record.get('rotors')
    required(isinstance(rotors, list) and len(rotors) == n and
             all(isinstance(row, list) and len(row) == 4 for row in rotors),
             'rotor record shape mismatch')
    arrays = {key: np.array([[item[key] for item in row] for row in rotors], dtype=float)
              for key in ('alpha', 'x', 'T')}
    return arrays


def compare_map(audit, record, expected, n, name):
    required(isinstance(record, dict), name+' record absent')
    audit.relative(record.get('y'), expected['y'], name+'.all-y')
    arrays = rotor_arrays(record, n)
    audit.close(arrays['alpha'], expected['alpha'], name+'.all-alpha')
    audit.relative(arrays['x'], expected['x'], name+'.all-x')
    audit.relative(arrays['T'], expected['T'], name+'.all-T')
    audit.check(np.all(np.isfinite(arrays['alpha']) & (arrays['alpha'] >= 0)), name+'.alpha-domain')
    audit.check(np.all(np.isfinite(arrays['x']) & (arrays['x'] > 0) & (arrays['x'] <= 1)),
                name+'.root-domain')
    return arrays


def original_controls():
    # Literal position tokens from the frozen prospective control specification;
    # no runtime geometry or generator is evaluated by this saved-only checker.
    out = []
    def add(ident, tokens, use_grid):
        out.append((ident, tokens, use_grid))
    for x, values in [('0', ['2.9999999999999996', '3', '3.0000000000000004']),
                      ('-6', ['-3.0000000000000004', '-3', '-2.9999999999999996'])]:
        for name, value in zip(['below', 'exact', 'above'], values):
            add('radius-'+x+'-'+name, [[x, '0', '0'], [value, '0', '0']], True)
    add('cell-below', [['0', '0', '0'], ['3.9999999999999996', '0.25', '0.5'], ['4', '0', '1']], True)
    add('cell-exact', [['0', '0', '0'], ['0.5', '4', '0.25'], ['1', '4', '0']], True)
    add('cell-above', [['0', '0', '0'], ['0.25', '0.5', '4.000000000000001'], ['0', '1', '4']], True)
    add('signed-zero', [['-0', '0', '0'], ['0', '-0', '0']], True)
    add('coarse-origin', [['0', '0', '0'], ['1', '0.25', '0.5'], ['4', '1', '2']], True)
    add('coarse-translated', [['1099511627776']*3,
        ['1099511627777', '1099511627776.25', '1099511627776.5'],
        ['1099511627780', '1099511627777', '1099511627778']], True)
    xs = ['0', '0.05', '0.1', '0.15000000000000002', '0.2', '0.25', '0.30000000000000004',
          '0.35000000000000003', '0.4', '0.45', '0.5', '0.55', '0.6000000000000001',
          '0.65', '0.7000000000000001', '0.75']
    add('dense-16', [[x, '0', ['0', '0.45', '0.9'][i % 3]] for i, x in enumerate(xs)], True)
    add('span-256', [['0', '0', '0'], ['256', '0', '0']], True)
    add('span-nextUp256', [['0', '0', '0'], ['256.00000000000006', '0', '0']], False)
    add('far-invalid258', [['0', '0', '0'], ['258', '0', '0']], False)
    add('nonfinite-nan', [['0', '0', '0'], ['NaN', '0', '0']], False)
    add('nonfinite-infinity', [['0', '0', '0'], ['Infinity', '0', '0']], False)
    add('overflow-span', [['-1.7976931348623157e+308', '0', '0'], ['1.7976931348623157e+308', '0', '0']], False)
    add('near-field', [['0', '0', '0'], ['0', '0', '0.02']], True)
    add('duplicates', [['1', '1', '1'], ['1', '1', '1']], True)
    return out


def validate_csr(audit, offsets, sources, k, n, name):
    require(offsets.shape == (4*n+1,), 'CSR offsets shape mismatch')
    require(sources.shape == k.shape and offsets[0] == 0 and offsets[-1] == len(sources) and
            np.all(np.diff(offsets.astype(np.int64)) >= 0), 'invalid CSR row partition')
    audit.check(np.all(sources < n) and np.all(np.isfinite(k) & (k > 0)), name+'.valid-positive-CSR')
    ordered = True
    for row in range(4*n):
        ids = sources[int(offsets[row]):int(offsets[row+1])]
        if len(ids) > 1 and not np.all(ids[1:] > ids[:-1]):
            ordered = False
            break
    audit.check(ordered, name+'.strict-source-order')


def rotor_values(solution, n):
    y = np.asarray(solution['y'], dtype=float)
    require(y.shape == (n,), 'amplitude shape mismatch')
    def block(rotors):
        require(len(rotors) == n and all(len(row) == 4 for row in rotors), 'rotor shape mismatch')
        return np.asarray([[[item[key] for key in ('alpha', 'x', 'T')] for item in row] for row in rotors], dtype=float)
    rotors = block(solution['rotors'])
    residual_y = np.asarray(solution['residualMap']['y'], dtype=float)
    require(residual_y.shape == (n,), 'residual amplitude shape mismatch')
    residual_rotors = block(solution['residualMap']['rotors'])
    return np.concatenate((y, rotors.ravel(), residual_y, residual_rotors.ravel())), y, rotors, residual_y


def saved_checksum(solution, kvals):
    # Arithmetic over already saved outputs only; no map or root evaluation.
    value = 0.
    for i, y in enumerate(solution['y']):
        total = 0.
        for rotor in solution['rotors'][i]:
            total += rotor['T']
        value += y*(i+1)+total
    return (value+(float(kvals[0]) if len(kvals) else 0.))+(float(kvals[-1]) if len(kvals) else 0.)


class Audit:
    def __init__(self, package):
        self.package=package
        self.root=package.parent.parent
        self.started=time.monotonic()
        self.checks=[]
        self.errors=[]
        self.qualified={}
        self.calls=[]
        self.generation=[]
        self.controls=[]
        self.frames=[]
        self.resources={}
        self.evidence={}
    def guard(self):
        require(time.monotonic()-self.started < COOPERATIVE_SECONDS, 'new reviewer 175-second cooperative cap')
        rss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        if sys.platform != 'darwin': rss*=1024
        require(rss<=RSS_CAP, 'new reviewer RSS cap')
    def check(self, ok, name, details=None):
        rec={'name':name,'pass':bool(ok)}
        if details is not None: rec['details']=safe_json(details)
        self.checks.append(rec)
        if not ok: self.errors.append(name)
        return bool(ok)
    def error(self, name, error):
        message='saved-audit exception; inspect named failed checks and exception class'
        self.check(False,name,{'type':type(error).__name__,'message':message})
    def numeric(self, actual, expected, name, atol=2e-12, rtol=2e-12):
        a,b=np.asarray(actual,dtype=float),np.asarray(expected,dtype=float)
        if a.shape!=b.shape:
            self.check(False,name,{'actualShape':list(a.shape),'expectedShape':list(b.shape)})
            return False
        with np.errstate(invalid='ignore',over='ignore'):
            d=np.abs(a-b)
            bad=~(np.isfinite(a)&np.isfinite(b)) | (d>atol+rtol*np.abs(b))
        ids=np.flatnonzero(bad.ravel())
        details={'length':int(a.size),'bad':int(ids.size),'maxAbs':float(np.max(d,initial=0.))}
        if ids.size:
            i=int(ids[0]);details['first']={'index':i,'actual':float(a.ravel()[i]),'expected':float(b.ravel()[i])}
        return self.check(not ids.size,name,details)
    def close(self, actual, expected, name, atol=2e-12, rtol=2e-12):
        return self.numeric(actual,expected,name,atol,rtol)
    def relative(self, actual, expected, name):
        return self.numeric(actual,expected,name,0.,1e-9)
    def exact(self, actual, expected, name):
        # Numeric JSON arrays may contain signed zeros: compare their binary64 representation.
        return self.check(canonical(actual)==canonical(expected),name)
    def path(self, base, relative):
        require(isinstance(relative,str) and relative,'artifact path absent')
        rel=Path(relative)
        require(not rel.is_absolute() and '..' not in rel.parts,'artifact path escapes')
        p=(base/rel).resolve()
        require(p.is_relative_to(base.resolve()) and p.is_file(),'artifact missing or outside base')
        return p
    def digest(self,path):
        h=hashlib.sha256()
        with path.open('rb') as f:
            for b in iter(lambda:f.read(1<<20),b''):
                self.guard();h.update(b)
        return h.hexdigest()
    def pin(self, base, meta, name, size=None):
        require(isinstance(meta,dict),'artifact metadata absent')
        p=self.path(base,meta.get('path'))
        self.check(type(meta.get('bytes')) is int and meta['bytes']==p.stat().st_size,name+'.bytes')
        if size is not None: require(p.stat().st_size==size,name+' shape bytes')
        require(p.stat().st_size<=256*(1<<20),'artifact file cap')
        self.check(valid_sha(meta.get('sha256')) and self.digest(p)==meta['sha256'],name+'.sha256')
        return p


def canonical(value):
    if isinstance(value,bool) or value is None or isinstance(value,str): return (type(value).__name__,value)
    if isinstance(value,(int,float)):
        return ('number',np.float64(value).tobytes())
    if isinstance(value,list): return ('list',tuple(canonical(x) for x in value))
    if isinstance(value,dict): return ('dict',tuple((k,canonical(value[k])) for k in sorted(value)))
    raise TypeError('unsupported canonical value')


def read_array(audit,meta,dtype,count,name):
    p=audit.pin(audit.package,meta,name,count*np.dtype(dtype).itemsize)
    return np.fromfile(p,dtype=dtype)


def bundle(audit,doc,name):
    n=doc['n'];a=doc['artifacts']
    m=a['sources']['bytes']//4
    require(type(n) is int and 0<n<=5000 and 0<=m<=MAX_TERMS,'bundle dimensions')
    off=read_array(audit,a['offsets'],'<u4',4*n+1,name+'.offsets').astype(np.int64)
    src=read_array(audit,a['sources'],'<u4',m,name+'.sources')
    k=read_array(audit,a['K'],'<f8',m,name+'.K')
    aa=read_array(audit,a['a'],'<f8',m,name+'.a')
    validate_csr(audit,off,src,k,n,name)
    audit.check(np.all(np.isfinite(aa)&(aa>0)),name+'.positive-a')
    check_work(audit,doc['geometryWork'],n,m,name+'.work')
    check_certificate(audit,doc['certificate'],doc['geometryWork'],'all',name+'.certificate')
    sy=audit.pin(audit.package,a['symbols'],name+'.symbols')
    require(a['symbols'].get('rawBytes')==4*n*n,'raw symbol size')
    require(sy.stat().st_size<=64*(1<<20),'compressed symbol cap')
    audit.check(valid_sha(doc.get('matrixHash')) and valid_sha(doc.get('solutionHash')),name+'.fingerprint-format')
    return {'doc':doc,'n':n,'m':m,'off':off,'src':src,'k':k,'a':aa,'symbolPath':sy}


def generation_review(audit):
    index=load_json(audit.path(audit.package,'inputs/index.json'))
    audit.check(index.get('kind')=='fresh-airflow-off-boids-states' and index.get('shape')==['vehicle',17] and index.get('dtype')=='float64le','inputs.index-contract')
    entries=index['cases']
    require(len(entries)==3,'exactly three fresh input cases required')
    require([(x.get('id'),x.get('n'),x.get('seed')) for x in entries]==CASES, 'fresh case order/IDs/seeds/counts')
    require(len({x['id'] for x in entries})==3,'duplicate fresh case ID')
    summaries=audit.evidence.get('generation',[])
    audit.check([x.get('id') for x in summaries]==[x[0] for x in CASES],'generation.evidence-order')
    for entry in entries:
        audit.guard();ident,n,seed=entry['id'],entry['n'],entry['seed']
        state=read_array(audit,entry,'<f8',17*n,ident+'.input').reshape(n,17)
        require(entry.get('generationPath')=='generation/'+ident+'.json','generation path mismatch')
        gen=load_json(audit.path(audit.package,entry['generationPath']))
        audit.check(gen.get('id')==ident and gen.get('complete') is True,ident+'.generation-id-complete')
        summary=next(x for x in summaries if x['id']==ident)
        audit.pin(audit.package,summary['pin'],ident+'.generation-summary-pin')
        audit.check(summary.get('complete') is True and summary.get('generationMs')==gen.get('generationMs'),ident+'.generation-summary')
        compare_fields(audit,gen.get('config'),dict(seed=seed,count=n,mode='boids',dt=.0025,duration=2,
            search='grid',filter='wall-priority',airflow='off',observation='ideal'),ident+'.generator-config')
        audit.check(gen['config'].get('course')=='factory-v1',ident+'.wide-course')
        metrics=gen['metrics']
        audit.check(metrics.get('end')==2 and metrics.get('stopReason') is None and metrics.get('failure') is None,ident+'.generation-complete')
        initial=read_array(audit,gen['initial'],'<f8',17*n,ident+'.initial').reshape(n,17)
        final=read_array(audit,gen['final'],'<f8',17*n,ident+'.final').reshape(n,17)
        audit.check(state.tobytes()==final.tobytes(),ident+'.input-is-unaltered-final')
        audit.check(np.all(np.isfinite(initial)) and np.all(np.isfinite(final)),ident+'.finite-full-states')
        poses=read_array(audit,gen['poses'],'<f8',21*(1+7*n),ident+'.poses').reshape(21,1+7*n)
        audit.check(np.all(np.isfinite(poses)),ident+'.finite-poses')
        require(gen['poses'].get('frames')==21 and gen['poses'].get('width')==1+7*n,'pose metadata shape')
        frames=gen['frames'];require(len(frames)==21,'frame pin count')
        for frame_index,pin in enumerate(frames):
            frame=read_array(audit,pin,'<f8',1+7*n,ident+'.frame.'+str(frame_index))
            audit.check(pin.get('t')==poses[frame_index,0] and frame.tobytes()==poses[frame_index].tobytes(),ident+'.frame-concatenation.'+str(frame_index))
        audit.numeric(poses[:,0],np.arange(21)/10,ident+'.pose-times',1e-12,0.)
        for ix,source in [(0,initial),(-1,final)]:
            wanted=np.concatenate((source[:,:3],source[:,6:10]),axis=1)
            audit.check(poses[ix,1:].tobytes()==wanted.tobytes(),ident+'.pose-endpoint.'+str(ix))
        audit.check(gen.get('recording',{}).get('cadence')==.1,ident+'.recording-cadence')
        duration=gen.get('generationMs',gen.get('timing',{}).get('total'))
        audit.check(finite(duration) and duration>=0,ident+'.generation-time-separate')
        audit.numeric([s['t'] for s in gen['samples']],np.arange(21)/10,ident+'.sample-times',1e-12,0.)
        audit.generation.append({'id':ident,'n':n,'seed':seed,'state':state,'entry':entry})
    return entries


def assembly_review(audit,stats,n,m,method,name,nominal=True,*,offsets,sources,graph):
    if method=='A': return
    require(isinstance(stats,dict),'assembly stats absent')
    off=np.asarray(offsets,dtype=np.int64)
    src=np.asarray(sources,dtype=np.int64)
    require(off.shape==(4*n+1,) and src.shape==(m,) and off[0]==0 and off[-1]==m and np.all(np.diff(off)>=0),'assembly CSR shape/partition')
    counts=np.diff(off)
    require(np.all(counts<=n-1),'assembly row exceeds distinct nonself sources')
    incoming=[]
    for i in range(n):
        audit.guard()
        incoming.append(int(np.unique(src[off[4*i]:off[4*i+4]]).size))
    dependency_entries=sum(incoming)
    compare_fields(audit,graph,dict(uniqueVehicleEdges=dependency_entries,incomingDegree=incoming,
                                  maxIncomingDegree=max(incoming)),name+'.graph-from-CSR')
    typed=method=='T'
    chunks=(m+4095)//4096 if typed else 0
    # Each nonempty canonical row intersects this many consecutive chunk ranges.
    # Half-open ends use end-1: a row ending exactly at4096 adds no empty segment.
    nonempty=counts>0
    row_segments=int(np.sum((off[1:][nonempty]-1)//4096-off[:-1][nonempty]//4096+1)) if typed else 0
    expected=dict(schema='m31-receiver-row-assembly-v1',mode={'L':'lean','F':'lean','T':'typed'}[method],
        inputN=n,positiveEntries=m,dependencyEntries=dependency_entries,
        rowCapacityEntries=n if typed else None,rowLengthsAtLastReceiver=counts[-4:].tolist(),
        maxRowLengthEntries=int(np.max(counts,initial=0)),rowGrowthCount=0 if typed else None,
        rowScratchTypedArrayAllocations=8 if typed else 0,rowScratchIdBytes=16*n if typed else 0,
        rowScratchKBytes=32*n if typed else 0,rowScratchBytes=48*n if typed else 0,
        rotorPointScratchBytes=12*8,rotorPointTypedArrayAllocations=1,chunkPolicyCapacityEntries=4096,
        chunkCount=chunks,chunkGrowthCount=max(0,chunks-1),chunkTypedArrayAllocations=2*chunks,
        chunkCapacityEntries=4096*chunks,chunkUsedEntries=m if typed else 0,
        chunkSpareEntries=4096*chunks-m if typed else 0,chunkAllocatedPayloadBytes=12*4096*chunks,
        rowToChunkCopySegments=row_segments,chunkToFinalCopySegments=chunks,
        rowToChunkCopiedEntries=m if typed else 0,chunkToFinalCopiedEntries=m if typed else 0,
        rowToChunkCopiedBytes=12*m if typed else 0,chunkToFinalCopiedBytes=12*m if typed else 0,
        ordinaryPositiveTupleCount=0 if typed else m,ordinarySetAddCalls=0 if typed else m,
        ordinaryDependencySetCount=0 if typed else n,ordinaryGlobalSourceEntries=0 if typed else m,
        ordinaryGlobalKEntries=0 if typed else m,ordinaryRowToGlobalCopiedEntries=0 if typed else m,
        ordinaryGlobalToFinalCopiedEntries=0 if typed else m,
        dependencyOutputRepresentation='independent ordinary arrays; ascending unique IDs',dependencyOutputArrays=n,
        finalSourceBytes=4*m,finalKBytes=8*m,offsetBytes=4*(4*n+1),scalingBytes=8*m if nominal else 0,
        outputTypedArraysOwnBuffers=True,scratchViewsReturned=False,jsHeapBytesMeasured=False,
        garbageCollectionMeasured=False,commonPreparedGeometryBytes=28*n*8,commonSymbolBytes=4*n*n)
    # Expected payload totals are formed from independently derived counts, never
    # from the candidate's reported components.
    overlap=expected['rowScratchBytes']+expected['rotorPointScratchBytes']+expected['offsetBytes']+expected['chunkAllocatedPayloadBytes']+expected['finalSourceBytes']+expected['finalKBytes']
    expected['finalizationOverlapKnownPayloadBytes']=overlap
    expected['allocatedAssemblyTypedPayloadBytes']=overlap+expected['scalingBytes']
    compare_fields(audit,stats,expected,name)


required=require

def safe_json(value):
    if isinstance(value,np.generic): value=value.item()
    if isinstance(value,float):
        if math.isnan(value): return 'NaN'
        if math.isinf(value): return 'Infinity' if value>0 else '-Infinity'
        if value==0 and math.copysign(1,value)<0: return '-0'
    if isinstance(value,dict): return {k:safe_json(v) for k,v in value.items()}
    if isinstance(value,(list,tuple)): return [safe_json(v) for v in value]
    return value

def diagnostic_scalar(value): return safe_json(float(value))

def expected_controls():
    out=[dict(id=i,positions=p,eligible=e,patches=[]) for i,p,e in original_controls()]
    for n in (62,64,66):
        out.append(dict(id=f'planes-{n}',positions=[['0','0','0' if i<n//2 else '0.6'] for i in range(n)],eligible=True,patches=[]))
    def add(ident,positions,eligible=True,patches=[]):
        out.append(dict(id=ident,positions=positions,eligible=eligible,patches=patches))
    for axis,axisname in enumerate('xyz'):
        for name,value in zip(('below','exact','above'),('3.9999999999999996','4','4.000000000000001')):
            pos=['0']*3;pos[axis]=value
            add('component-'+axisname+'-'+name,[['0']*3,pos])
    add('span-diagonal-256',[['0']*3,['256']*3])
    add('span-nextDown256',[['0']*3,['255.99999999999997','0','0']])
    add('center-257-fallback',[['0']*3,['257','0','0']],False)
    add('center-nextUp257-fallback',[['0']*3,['257.00000000000006','0','0']],False)
    near=[['0']*3,['0','0','0.02'],['4','0','0']]
    positive=[['0']*3,['0','0','0.6'],['4','0','0']]
    far=[['0']*3,['4','0','0']]
    def patch(vehicle,index,value): return dict(vehicle=vehicle,index=index,value=value)
    add('mixed-near-far',near);add('mixed-positive-far',positive)
    add('invalid-quaternion-far',far,patches=[patch(0,9,'2')])
    for name,value in [('zero','0'),('negative','-0.01'),('nan','NaN')]:
        add('nominal-'+name+'-positive-far',positive,patches=[patch(1,13,value)])
    add('scaled-cap-positive-far',positive,patches=[patch(1,i,'1000000000000') for i in range(13,17)])
    add('invalid-quaternion-nan-far',far,patches=[patch(0,6,'NaN')])
    add('nominal-infinity-positive-far',positive,patches=[patch(1,13,'Infinity')])
    add('nominal-total-overflow-positive-far',positive,patches=[patch(1,i,'1.7976931348623157e+308') for i in range(13,17)])
    add('nominal-unequal-positive-far',positive,patches=[patch(1,13+r,v) for r,v in enumerate(('0.03','0.04','0.05','0.06'))])
    for spec in out:
        ident=spec['id']
        spec['reason']=None if spec['eligible'] else ('coordinate-nonfinite' if ident in ('nonfinite-nan','nonfinite-infinity') else 'span-nonfinite' if ident=='overflow-span' else 'span-out-of-range')
    return out

def states_for(spec):
    n=len(spec['positions']);states=np.zeros((n,17),dtype='<f8')
    states[:,:3]=np.asarray(spec['positions'],dtype=float);states[:,9]=1.;states[:,13:17]=.027*9.81/4
    for patch in spec['patches']: states[patch['vehicle'],patch['index']]=float(patch['value'])
    return states

def token_states(audit,tokens,expected,name):
    require(isinstance(tokens,list) and len(tokens)==len(expected) and all(isinstance(row,list) and len(row)==17 and all(isinstance(v,str) for v in row) for row in tokens),'full state token shape')
    actual=np.asarray(tokens,dtype='<f8')
    audit.check(actual.tobytes()==expected.tobytes(),name+'.all17-state-values-and-zero-signs')
    return actual

def mutation(audit,rec,states,name,token_keys=None):
    expected=hashlib.sha256(states.astype('<f8',copy=False).tobytes()).hexdigest()
    audit.check(rec.get('inputUnchanged') is True,name+'.unchanged')
    audit.check(rec.get('inputBeforeSha256')==expected and rec.get('inputAfterSha256')==expected,name+'.before-after-input-hashes')
    if token_keys:
        for key in token_keys: token_states(audit,rec.get(key),states,name+'.'+key)
        audit.exact(rec[token_keys[0]],rec[token_keys[1]],name+'.token-identity')

def check_work(audit,work,n,m,name):
    fields=['logicalDirectedPairs','gatheredNonselfCandidates','directedCenterTests','certifiedSkippedPairs','centerEligiblePairs','centerGuardRejectedPairs','pairCalls','positiveRotorTerms']
    require(isinstance(work,dict) and all(k in work for k in fields),'geometry work missing')
    audit.check(all(type(work[k]) is int and work[k]>=0 for k in fields),name+'.nonnegative-integers')
    audit.check(work['logicalDirectedPairs']==n*(n-1)==work['gatheredNonselfCandidates'],name+'.all-ordered-pairs-enumerated')
    audit.check(work['directedCenterTests']+work['certifiedSkippedPairs']==n*(n-1),name+'.actual-and-skipped-norms')
    audit.check(work['pairCalls']==4*work['centerEligiblePairs'],name+'.pair-calls')
    audit.check(work['centerEligiblePairs']+work['centerGuardRejectedPairs']<=work['directedCenterTests'],name+'.center-partition')
    audit.check(work['positiveRotorTerms']==m<=MAX_TERMS,name+'.positive-terms')

def check_certificate(audit,cert,work,mode,name,expected_grid=None):
    wanted=dict(finite=None,min=None,max=None,spans=None,certified=None,useGrid=False,fallback=False,reason='all-pairs-selected')
    audit.exact(cert,wanted,name+'.unchanged-all-pairs-certificate')

def screen_predicate(states):
    positions=states[:,:3];mins=[];maxs=[]
    # Explicit Math.min/Math.max signed-zero and NaN behavior, independent of NumPy reduction ties.
    for axis in range(3):
        values=[float(v) for v in positions[:,axis]]
        if any(math.isnan(v) for v in values): lo=hi=math.nan
        else:
            lo,hi=min(values),max(values)
            if lo==0: lo=-0.0 if any(v==0 and math.copysign(1,v)<0 for v in values) else 0.0
            if hi==0: hi=0.0 if any(v==0 and math.copysign(1,v)>0 for v in values) else -0.0
        mins.append(lo);maxs.append(hi)
    spans=[hi-lo for lo,hi in zip(mins,maxs)]
    coordinate=bool(np.all(np.isfinite(positions)));spanfinite=all(math.isfinite(v) for v in spans)
    eligible=coordinate and spanfinite and all(0<=v<=256 for v in spans)
    return dict(schema='m31-center-screen-work-v1',finiteRuntimeOnly=True,runtimeGeneralEquivalenceProven=False,
        historicalCertifiedSkippedPairsIsFormalProof=False,spanLimit=256,componentThreshold=4,
        coordinateFinite=coordinate,spanFinite=spanfinite,min=mins,max=maxs,spans=spans,eligible=eligible,fallback=not eligible,
        fallbackReason=None if eligible else 'coordinate-nonfinite' if not coordinate else 'span-nonfinite' if not spanfinite else 'span-out-of-range',
        omissionEvidence='reconstruct-from-saved-current-positions-and-frozen-predicate')

def omission_mask(states,i,eligible):
    if not eligible: return np.zeros(len(states),dtype=bool)
    delta=states[:,:3]-states[i,:3]
    mask=np.max(np.abs(delta),axis=1)>=4.;mask[i]=False
    return mask

def verify_screen(audit,doc,states,omitted,name,method):
    n=len(states);logical=n*(n-1);work=doc['geometryWork']
    if method=='L':
        audit.check(doc.get('screen') is None,name+'.screen-null')
        audit.check(work['directedCenterTests']==logical and work['certifiedSkippedPairs']==0,name+'.all-center-norms')
        return
    expected=screen_predicate(states)
    expected.update(orderedPairVisits=logical,componentTests=logical if expected['eligible'] else 0,
                    skippedCenterNormCalls=omitted,actualCenterNormCalls=logical-omitted)
    audit.exact(doc.get('screen'),safe_json(expected),name+'.independent-screen-and-counts')
    audit.check(work['directedCenterTests']==logical-omitted and work['certifiedSkippedPairs']==omitted,name+'.work-screen-counts')
    if not expected['eligible']: audit.check(omitted==0,name+'.fallback-no-omissions')

def verify_omission_report(audit,report,states,omitted,name):
    wanted=dict(eligible=screen_predicate(states)['eligible'],orderedPairs=len(states)*(len(states)-1),
        omittedPairs=omitted,checkedRotorSymbols=4*omitted,exactOutsideSymbols=True,firstMismatch=None,screenCounts=True,**{'pass':True})
    audit.exact(report,wanted,name+'.candidate-omission-report')

def literal_bundle(audit,doc,n,name):
    require(doc.get('n')==n,'literal bundle size')
    off=np.asarray(doc['offsets'],dtype=np.int64);src=np.asarray(doc['sources'],dtype=np.int64);k=np.asarray(doc['K'],dtype=float)
    validate_csr(audit,off,src,k,n,name)
    sy=np.asarray(doc['symbols'],dtype=np.uint8);require(sy.shape==(4*n*n,),'literal symbol shape')
    audit.check(all(type(v) is int and 1<=v<=11 for v in doc['symbols']),name+'.literal-terminal-symbols')
    audit.exact(np.bincount(sy,minlength=12).tolist(),doc['symbolCounts'],name+'.literal-symbol-census')
    check_work(audit,doc['geometryWork'],n,len(src),name+'.work');check_certificate(audit,doc['certificate'],doc['geometryWork'],'all',name)
    return dict(doc=doc,n=n,m=len(src),off=off,src=src,k=k,a=None if doc['a'] is None else np.asarray(doc['a'],dtype=float),symbols=sy.reshape(n,n,4))

def exact_models(audit,L,F,name):
    for key in ('input','admission','graph','certificate','symbolCounts','ordinaryLmax','assemblyStats'):
        audit.exact(F['doc'][key],L['doc'][key],name+'.exact-'+key)
    for key in ('off','src','k','a'):
        a,b=L[key],F[key]
        audit.check((a is None and b is None) or (a is not None and b is not None and a.dtype==b.dtype and a.tobytes()==b.tobytes()),name+'.exact-'+key)
    remove=lambda w:{k:v for k,v in w.items() if k not in ('directedCenterTests','certifiedSkippedPairs')}
    audit.exact(remove(F['doc']['geometryWork']),remove(L['doc']['geometryWork']),name+'.exact-model-work')

def independent_solution(audit,solution,states,g,c,off,src,aa,graph,name):
    n=len(states);expected=direct_solve(graph['order'],g['f0'],g['S0'],off,src,aa,audit.guard)
    compare_map(audit,solution,expected,n,name+'.analytic-ordered')
    y=np.asarray(solution['y'],dtype=float);res=csr_map(y,g['f0'],g['S0'],off,src,aa)
    compare_map(audit,solution['residualMap'],res,n,name+'.analytic-residual-map')
    for key,values in [('work',expected),('residualWork',res)]:
        compare_fields(audit,solution[key],dict(rootClosures=4*n,bisectionIterations=56*int(np.count_nonzero(values['alpha']>0)),positiveTermMultiplications=len(src)),name+'.'+key)
    residual=float(np.max(np.abs(np.log(y)-np.log(res['y']))))
    total=((res['T'][:,0]+res['T'][:,1])+res['T'][:,2])+res['T'][:,3]
    discrepancy=float(np.max(np.abs(g['S0']*y*y-total)/g['S0']))
    audit.close(solution['residualLog'],residual,name+'.residual-log')
    audit.close(solution['sourceReceiverMismatch'],discrepancy,name+'.force-consistency')
    audit.check(residual<=1e-9 and discrepancy<=2e-9,name+'.residual-gates')
    audit.check(solution.get('iterations',1)==1 and solution.get('converged',True) is True and solution.get('lastChange') is None,name+'.ordered-termination')
    return residual

def independent_model(audit,states,L,F,name,reader):
    """Complete streamed symbols, all omitted pairs, CSR and independently rebuilt geometry."""
    n=len(states);d=L['doc'];c=constants()
    with np.errstate(all='ignore'): g=prepare_geometry(states,c);census=input_census(states,g,c)
    compare_fields(audit,d['input'],census,name+'.independent-input')
    exact_models(audit,L,F,name)
    counts=np.zeros(12,dtype=np.int64);ids_list=[];k_list=[];offs=[0];deps=[]
    mismatch=support_bad=k_bad=omitted=omission_bad=0;first=[];maxerror=0.
    eligible=screen_predicate(states)['eligible']
    work=dict(logicalDirectedPairs=n*(n-1),gatheredNonselfCandidates=n*(n-1),directedCenterTests=n*(n-1),certifiedSkippedPairs=0,centerEligiblePairs=0,centerGuardRejectedPairs=0,pairCalls=0,positiveRotorTerms=0)
    for i in range(n):
        audit.guard()
        with np.errstate(all='ignore'): sy,rows,rwork=classify_receiver(i,g,c)
        lb,fb=reader(i);require(lb.shape==fb.shape==(n,4),'symbol row shape')
        require(lb.tobytes()==fb.tobytes(),'full L/F symbol element equality')
        mask=omission_mask(states,i,eligible);omitted+=int(np.count_nonzero(mask))
        omission_bad+=int(np.count_nonzero(lb[mask]!=1))+int(np.count_nonzero(fb[mask]!=1))
        bad=lb!=sy;mismatch+=int(np.count_nonzero(bad))
        if np.any(bad) and len(first)<8:
            for j,r in np.argwhere(bad)[:8-len(first)]: first.append([i,int(j),int(r),int(lb[j,r]),int(sy[j,r])])
        counts+=np.bincount(sy.ravel(),minlength=12)
        work['centerEligiblePairs']+=rwork['eligibleCenterPairs'];work['centerGuardRejectedPairs']+=rwork['invalidCenterPairs'];work['pairCalls']+=rwork['pairTermCalls']
        deps.append(np.unique(np.concatenate([ids for ids,ks in rows])))
        for r,(ids,ks) in enumerate(rows):
            row=4*i+r;a,b=int(L['off'][row]),int(L['off'][row+1])
            if not np.array_equal(L['src'][a:b],ids): support_bad+=1
            else:
                err=np.abs(L['k'][a:b]-ks);maxerror=max(maxerror,float(np.max(err,initial=0.)));k_bad+=int(np.any(err>2e-12+2e-12*np.abs(ks)))
            ids_list.append(ids);k_list.append(ks);offs.append(offs[-1]+len(ids));require(offs[-1]<=MAX_TERMS,'independent positive cap')
    audit.check(mismatch==0,name+'.independent-every-symbol',dict(mismatches=mismatch,first=first))
    audit.check(support_bad==0,name+'.independent-every-source-row',dict(badRows=support_bad))
    audit.check(k_bad==0,name+'.independent-every-K',dict(badRows=k_bad,maxAbs=maxerror))
    audit.check(omission_bad==0,name+'.every-omitted-pair-all-four-symbols',dict(omittedOrderedPairs=omitted,checkedRotorSymbols=4*omitted,unexpectedSymbols=omission_bad))
    audit.check(counts.sum()==4*n*n and counts[0]==0,name+'.complete-terminal-census')
    audit.exact(d['symbolCounts'],counts.tolist(),name+'.independent-symbol-census')
    off=np.asarray(offs,dtype=np.int64);src=np.concatenate(ids_list).astype(np.int64);k=np.concatenate(k_list)
    work['positiveRotorTerms']=len(k);compare_fields(audit,d['geometryWork'],work,name+'.independent-L-work')
    graph=graph_census(g['q'],deps);compare_fields(audit,d['graph'],graph,name+'.independent-graph')
    nominal=census['nominalPositive'] and census['nominalTotalFinite'];aa=None;capmax=None;violations=None;lmax=None
    if nominal:
        scaled=k*np.sqrt(g['S0'][src]/c['mg']);rowids=np.repeat(np.arange(4*n),np.diff(off))
        aa=scaled/np.sqrt(g['f0'].ravel()[rowids]/(2*c['rho']*c['area']))
        audit.numeric(L['a'],aa,name+'.independent-every-a')
        capmax=float(np.max(scaled,initial=0.));violations=int(np.count_nonzero(~np.isfinite(scaled)|(scaled>128)))
        lmax=float(np.max(np.bincount(rowids,weights=aa,minlength=4*n))/(4*math.sqrt(2)))
        audit.close(d['ordinaryLmax'],lmax,name+'.independent-ordinary-bound')
    else: audit.check(L['a'] is None and d['ordinaryLmax'] is None,name+'.invalid-nominal-no-scaling')
    reasons=[]
    if not census['geometryValid']: reasons.append('geometry')
    if not nominal: reasons.append('nominal')
    if counts[4]: reasons.append('near-field')
    if counts[11]: reasons.append('invalid-term')
    if violations: reasons.append('scaled-cap')
    admission=dict(admitted=not reasons,reasons=reasons,unsupportedNearCount=int(counts[4]),invalidTermCount=int(counts[11]),scaledCapMax=capmax,scaledCapViolationCount=violations)
    compare_fields(audit,d['admission'],admission,name+'.independent-admission')
    for method,b in [('L',L),('F',F)]:
        verify_screen(audit,b['doc'],states,omitted,name+'.'+method,method)
        assembly_review(audit,b['doc']['assemblyStats'],n,len(src),method,name+'.'+method+'.assembly',nominal,offsets=b['off'],sources=b['src'],graph=b['doc']['graph'])
    return dict(omitted=omitted,graph=graph,admission=admission,g=g,c=c,off=off,src=src,a=aa,maxError=maxerror)

def numeric_report(audit,report,length,name,nullable=False):
    if nullable:
        audit.exact(report,dict(length=0,bad=0,**{'pass':True},firstMismatch=None),name+'.null-equality')
    else:
        compare_fields(audit,report,dict(length=length,maxAbs=0.,maxRel=0.,nonfinitePairs=0,bad=0,firstMismatch=None,**{'pass':True}),name)

def solve_report(audit,report,n,name,solved=True):
    if not solved: audit.exact(report,dict(**{'pass':True},notSolved=True),name+'.unsolved-equality');return
    for key in ('work','termination','residual','exactResidual','completeSolution','pass'):
        audit.check(report.get(key) is True,name+'.'+key)
    numeric_report(audit,report['values'],26*n,name+'.values')

def comparison_report(audit,report,b,name,solved,own=False):
    for key in ('symbols','offsets','sources','prepared','input','admission','graph','dependencies','certificate','symbolCounts','modelGeometry','ordinaryLmax','assembly','symbolAllocation','pass'):
        audit.check(report.get(key) is True,name+'.'+key)
    if own:
        for key in ('screen','allGeometryWork'): audit.check(report.get(key) is True,name+'.'+key)
    numeric_report(audit,report['K'],b['m'],name+'.K')
    numeric_report(audit,report['a'],b['m'],name+'.a',b['a'] is None)
    solve_report(audit,report['solution'],b['n'],name+'.solution',solved)

def controls_review(audit):
    specs=expected_controls();listed=audit.evidence.get('controls',[])
    audit.check(len(specs)==48 and [x.get('id') for x in listed]==[x['id'] for x in specs],'controls.fixed48-order')
    solved_count=0
    for spec in specs:
        audit.guard();ident=spec['id'];name='control.'+ident;before=len(audit.errors);states=states_for(spec);n=len(states)
        rec=load_json(audit.path(audit.package,'results/control-'+ident+'.json'))
        summary=next((x for x in listed if x.get('id')==ident),None);require(summary is not None,'control summary absent')
        audit.pin(audit.package,summary['pin'],name+'.summary')
        audit.check(rec.get('id')==ident and rec.get('n')==n,name+'.identity')
        audit.exact(rec.get('positionTokens'),spec['positions'],name+'.fixed-positions')
        audit.exact(rec.get('statePatches'),spec['patches'],name+'.fixed-patches')
        mutation(audit,rec,states,name,('inputBeforeTokens','stateTokens'))
        audit.check(rec.get('expectedScreenEligible') is spec['eligible'] and rec.get('expectedFallbackReason')==spec['reason'],name+'.fixed-screen-expectation')
        L=literal_bundle(audit,rec['L'],n,name+'.L');F=literal_bundle(audit,rec['F'],n,name+'.F')
        model=independent_model(audit,states,L,F,name,lambda i:(L['symbols'][i],F['symbols'][i]))
        verify_omission_report(audit,rec.get('omissionAudit'),states,model['omitted'],name)
        comparison_report(audit,rec['comparison'],F,name+'.comparison',False)
        solved=model['admission']['admitted'] and model['graph']['descendingEligible']
        audit.exact(rec.get('mutationChecks'),dict(build=dict(L=True,F=True),solve=dict(L=True if solved else None,F=True if solved else None)),name+'.per-call-mutation-checks')
        audit.check(rec.get('solvePolicy')=='admitted-and-descending-only',name+'.solve-policy')
        audit.check(rec.get('noSolveReason')==(None if solved else 'admission' if not model['admission']['admitted'] else 'ordering'),name+'.no-solve-reason')
        audit.check(summary.get('solved') is solved,name+'.summary-solved')
        audit.exact(rec['solutions']['L'],rec['solutions']['F'],name+'.all-solution-and-residual-elements-exact')
        if solved:
            require(len(audit.errors)==before,'control independent geometry/equality gate failed')
            independent_solution(audit,rec['solutions']['L'],states,model['g'],model['c'],model['off'],model['src'],model['a'],model['graph'],name)
            solved_count+=2
        else: audit.check(rec['solutions']['L'] is None and rec['solutions']['F'] is None,name+'.domain-rejection-no-solve')
        solve_report(audit,rec['solutionComparison'],n,name+'.solution-comparison',solved)
        audit.check(rec.get('screenExpectation') is True and rec.get('pass') is True and summary.get('pass') is True,name+'.candidate-pass')
        audit.controls.append(dict(id=ident,n=n,complete=True,**{'pass':len(audit.errors)==before},solved=solved,omittedOrderedPairs=model['omitted']))
    audit.check(audit.evidence.get('controlSolvePolicy')=='admitted-and-descending-only' and audit.evidence.get('actualControlSolves')==solved_count,'controls.actual-solve-accounting')

def ownership_review(audit):
    own=load_json(audit.path(audit.package,'results/ownership.json'));audit.pin(audit.package,audit.evidence['ownership'],'ownership.summary')
    audit.exact(own.get('sequence'),OWNERSHIP,'ownership.fixed6-sequence')
    ctl=load_json(audit.path(audit.package,'results/control-planes-66.json'))
    states=states_for(next(s for s in expected_controls() if s['id']=='planes-66'))
    for key in ('retainedInputBeforeTokens','retainedInputAfterTokens'):token_states(audit,own[key],states,'ownership.'+key)
    sha=hashlib.sha256(states.tobytes()).hexdigest()
    audit.check(own.get('retainedInputBeforeSha256')==sha==own.get('retainedInputAfterSha256'),'ownership.retained-input-sha')
    for method in 'LF':
        retained=own['retained'][method]
        audit.exact(retained['before'],retained['after'],'ownership.'+method+'.complete-output-unchanged')
        audit.exact(retained['before'],ctl[method],'ownership.'+method+'.original-control')
    extras=own['extraBuilds'];require(len(extras)==6,'ownership exactly six extra builds')
    pairs={}
    for index,extra in enumerate(extras):
        method,ident=OWNERSHIP[index].split(':');name='ownership.extra.'+str(index)
        positions=([['0']*3,['4' if ident=='sparse2' else '258','0','0']] if ident!='planes62' else [['0','0','0' if i<31 else '0.6'] for i in range(62)])
        states=states_for(dict(positions=positions,patches=[]));n=len(states)
        audit.check(extra.get('label')==method and extra.get('id')==ident and extra.get('n')==n,name+'.identity')
        audit.exact(extra.get('positionTokens'),positions,name+'.positions')
        mutation(audit,extra,states,name,('inputBeforeTokens','stateTokens'))
        pairs.setdefault(ident,{})[method]=literal_bundle(audit,extra['bundle'],n,name)
        pairs[ident]['states']=states
    for ident,pair in pairs.items():
        L,F=pair['L'],pair['F'];states=pair['states']
        independent_model(audit,states,L,F,'ownership.'+ident,lambda i:(L['symbols'][i],F['symbols'][i]))
        if ident=='planes62':
            orig=load_json(audit.path(audit.package,'results/control-planes-62.json'))
            for method in 'LF':audit.exact(pair[method]['doc'],orig[method],'ownership.planes62.'+method+'.original')
    for key in ('pass','inputUnchanged','returnedStorageDisjoint'):audit.check(own.get(key) is True,'ownership.'+key)

def independent_case(audit,item):
    ident,n,states=item['id'],item['n'],item['state'];before=len(audit.errors);bs={}
    for method in 'LF':
        doc=load_json(audit.path(audit.package,'results/'+ident+'-'+method+'.json'))
        audit.check(doc.get('id')==ident and doc.get('label')==method and doc.get('n')==n,ident+'.'+method+'.identity')
        bs[method]=bundle(audit,doc,ident+'.'+method);audit.qualified[(ident,method)]=bs[method]
    streams={method:gzip.open(bs[method]['symbolPath'],'rb') for method in 'LF'}
    hashes={method:hashlib.sha256() for method in 'LF'}
    def reader(i):
        rows=[]
        for method in 'LF':
            block=streams[method].read(4*n);require(len(block)==4*n,'truncated symbol artifact');hashes[method].update(block)
            rows.append(np.frombuffer(block,dtype=np.uint8).reshape(n,4))
        return rows
    try:
        model=independent_model(audit,states,bs['L'],bs['F'],ident,reader)
        for method in 'LF':
            audit.check(streams[method].read(1)==b'',ident+'.'+method+'.symbols-no-trailing')
            audit.check(hashes[method].hexdigest()==bs[method]['doc']['artifacts']['symbols']['rawSha256'],ident+'.'+method+'.raw-symbol-hash')
    finally:
        for stream in streams.values():stream.close()
    for key in ('solutions','matrixHash','solutionHash'):audit.exact(bs['L']['doc'][key],bs['F']['doc'][key],ident+'.exact-'+key)
    require(model['admission']['admitted'] and model['graph']['descendingEligible'],'fresh target solve-domain rejected')
    require(len(audit.errors)==before,'fresh independent geometry/equality failed before solve')
    residual=independent_solution(audit,bs['L']['doc']['solutions']['O'],states,model['g'],model['c'],model['off'],model['src'],model['a'],model['graph'],ident)
    for method in 'LF':
        b=bs[method];sol=b['doc']['solutions']['O'];values,*_=rotor_values(sol,n)
        require(np.all(np.isfinite(values)),'nonfinite saved solution')
        b['checksum']=saved_checksum(sol,b['k']);b['valuesLength']=len(values);b['stateHash']=item['entry']['sha256']
        selected=[r for r in audit.evidence.get('qualification',[]) if r.get('id')==ident and r.get('label')==method]
        require(len(selected)==1,'qualification identity multiplicity')
        rec=selected[0]
        audit.exact(rec,load_json(audit.path(audit.package,'results/qualification-'+ident+'-'+method+'.json')),ident+'.'+method+'.qualification-copy')
        audit.pin(audit.package,rec['persistence']['meta'],ident+'.'+method+'.qualified-meta')
        audit.check(rec['persistence']['meta']['path']=='results/'+ident+'-'+method+'.json',ident+'.'+method+'.meta-path')
        audit.check(rec.get('matrixHash')==b['doc']['matrixHash'] and rec.get('solutionHash')==b['doc']['solutionHash'],ident+'.'+method+'.qualification-fingerprints')
        comparison_report(audit,rec['comparison'],b,ident+'.'+method+'.qualification-comparison',True)
        mutation(audit,{**rec,'inputUnchanged':rec['comparison'].get('inputUnchanged')},states,ident+'.'+method+'.qualification-mutation')
        if method=='F':verify_omission_report(audit,rec['omissionAudit'],states,model['omitted'],ident+'.qualification')
        else:audit.check(rec.get('omissionAudit') is None,ident+'.L.no-screen-report')
        audit.check(rec.get('pass') is True,ident+'.'+method+'.qualification-pass')
        audit.check(finite(rec.get('qualificationComputeMs')) and rec['qualificationComputeMs']>=0 and finite(rec['persistence'].get('totalPersistenceMs')) and rec['persistence']['totalPersistenceMs']>=0 and rec['persistence'].get('fsync') is False,ident+'.'+method+'.separate-untimed-cost')
    audit.frames.append(dict(id=ident,n=n,complete=True,symbolEntries=4*n*n,omittedOrderedPairs=model['omitted'],omittedRotorSymbolsChecked=4*model['omitted'],coefficientMaxAbs=model['maxError'],independentResidualLog=residual,**{'pass':len(audit.errors)==before}))

def expected_schedule(ids):
    out=[]
    def add(ident,method,block,warmup):out.append(dict(sequence=len(out),workload='full',id=ident,method=method,block=block,warmup=warmup))
    for ident in ids:
        for method in 'LF':add(ident,method,-1,True)
    for block in range(6):
        for j in range(3):
            c=(j+block)%3
            for method in PERMS[(block+c)%2]:add(ids[c],method,block,False)
    return out

def timing_review(audit,ids):
    listed=audit.evidence.get('timings',[]);schedule=expected_schedule(ids)
    audit.check(len(listed)==42,'timing.42-records')
    audit.check(len(list((audit.package/'results').glob('call-*-raw.json')))==42,'timing.42-raw-records')
    for planned in schedule:
        audit.guard();seq=planned['sequence'];name='call.'+str(seq)
        raw=load_json(audit.path(audit.package,f'results/call-{seq:03d}-raw.json'))
        rec=load_json(audit.path(audit.package,f'results/call-{seq:03d}.json'))
        audit.pin(audit.package,rec['raw'],name+'.raw')
        audit.check(rec['raw']['path']==f'results/call-{seq:03d}-raw.json',name+'.raw-path')
        audit.exact({k:v for k,v in rec.items() if k not in ('raw','validation')},raw,name+'.immutable-raw')
        audit.exact(rec,listed[seq],name+'.evidence-copy')
        for key,wanted in planned.items():audit.exact(rec.get(key),wanted,name+'.schedule-'+key)
        audit.check(rec.get('status')=='returned',name+'.returned')
        phases=rec['phasesMs'];fallback=planned['method']=='F' and rec['screen']['fallback']
        require(set(phases)==set(FULL_PHASES+(['screenPreflight'] if fallback else [])),'timed phase set mismatch')
        audit.check(finite(rec.get('totalMs')) and rec['totalMs']>0,name+'.positive-duration')
        audit.check(all(finite(v) and v>=(-1e-7 if k=='remainder' else 0) for k,v in phases.items()),name+'.finite-nonnegative-phases')
        audit.close(sum(phases.values()),rec['totalMs'],name+'.phase-total',1e-7,1e-12)
        b=audit.qualified[(planned['id'],planned['method'])];d=b['doc'];s=d['solutions']['O']
        for key in ('geometryWork','screen','certificate'):audit.exact(rec[key],d[key],name+'.'+key)
        without_symbols=lambda v:{k:x for k,x in v.items() if k!='commonSymbolBytes'}
        audit.exact(without_symbols(rec['assemblyStats']),without_symbols(d['assemblyStats']),name+'.assembly')
        audit.check(rec['assemblyStats'].get('commonSymbolBytes')==0,name+'.no-timed-symbol-tensor')
        for key in ('work','residualWork','residualLog','sourceReceiverMismatch'):audit.exact(rec[key],s[key],name+'.'+key)
        audit.check(rec.get('iterations')==1 and rec.get('converged') is True and rec.get('lastChange') is None,name+'.ordered-termination')
        audit.close(rec['checksum'],b['checksum'],name+'.checksum',1e-8,1e-14)
        v=rec['validation'];comparison_report(audit,v,b,name+'.comparison',True,True)
        for key in ('inputUnchanged','checksum','hashesMatch','finiteTiming','pass'):audit.check(v.get(key) is True,name+'.validation-'+key)
        audit.check(v.get('inputBeforeSha256')==b['stateHash']==v.get('inputAfterSha256'),name+'.unchanged-state-sha')
        audit.check(v.get('matrixHash')==d['matrixHash'] and v.get('solutionHash')==d['solutionHash'],name+'.qualified-fingerprints')
        audit.calls.append(rec)

def analysis(audit):
    out=dict(schema='m31-center-screen-independent-analysis-v1',scope='six paired within-process repeats per fixed fresh state; no population, physical, unseen-state or browser inference',
        independentAuditPass=not audit.errors,performanceRulePass=None,practicalRulePass=None,requiresReviewSupervisorClosure=True,cases=[])
    if len(audit.calls)!=42 or audit.errors:return out
    primary=[]
    for ident,n,seed in CASES:
        rows=[r for r in audit.calls if r['id']==ident and not r['warmup']];grouped={(r['block'],r['method']):r for r in rows}
        item=dict(id=ident,n=n,seed=seed,methods={},pairs={},practicalRulePass=None)
        phase_names=FULL_PHASES+(['screenPreflight'] if any('screenPreflight' in r['phasesMs'] for r in rows) else [])
        for method in 'LF':
            selected=[grouped[b,method] for b in range(6)]
            item['methods'][method]={k:dict(values=values,median=statistics.median(values),min=min(values),max=max(values)) for k,values in [('totalMs',[x['totalMs'] for x in selected])]+[(phase,[x['phasesMs'].get(phase,0.) for x in selected]) for phase in phase_names]}
            item['methods'][method]['screenCounts']=[x['screen'] for x in selected]
        ratios=[grouped[b,'F']['totalMs']/grouped[b,'L']['totalMs'] for b in range(6)]
        diffs=[grouped[b,'F']['totalMs']-grouped[b,'L']['totalMs'] for b in range(6)]
        med=statistics.median(ratios);wins=sum(r<1 for r in ratios)
        item['pairs']['F/L']=dict(blocks=list(range(6)),ratios=ratios,differencesMs=diffs,medianPairedRatio=med,strictWins=wins,
            pairedTotalsMs=[dict(block=b,L=grouped[b,'L']['totalMs'],F=grouped[b,'F']['totalMs']) for b in range(6)],
            matchedPhaseDifferenceSumsMs={phase:sum(grouped[b,'F']['phasesMs'].get(phase,0.)-grouped[b,'L']['phasesMs'].get(phase,0.) for b in range(6)) for phase in phase_names})
        item['gates']=dict(independentAudit=True,exactOutputEquality=True,allOmittedPairsChecked=True,controlsAndOwnership=True,generation=True,timingSchedule=True,candidateSupervisorClosure=True,medianPairedRatioAtMost090=med<=.90,atLeast5StrictWins=wins>=5,reviewSupervisorClosure=None,requiredPrimaryCase=n==5000)
        item['performanceRulePass']=med<=.90 and wins>=5
        if n==5000:primary.append(item['performanceRulePass'])
        out['cases'].append(item)
    out['performanceRulePass']=len(primary)==2 and all(primary)
    return out

def provenance_resources(audit):
    cfg=load_json(audit.path(audit.package,'config.json'))
    audit.check([(x['id'],x['n'],x['seed']) for x in cfg['cases']]==CASES and all(x.get('t')==2 for x in cfg['cases']),'config.fixed-cases')
    compare_fields(audit,cfg,dict(schema='m31-center-screen-v1',methods=['L','F'],permutations=PERMS,blocks=6,controls=48,ownershipExtraBuilds=6,qualificationBuilds=6,qualificationSolves=6,warmupCalls=6,measuredCalls=36,totalCalls=42,ownershipSequence=OWNERSHIP,
        controlIds=[s['id'] for s in expected_controls()],controlSolvePolicy='untimed solve+residual iff admitted and descendingEligible; otherwise explicit no-solve reason'),'config')
    compare_fields(audit,cfg['limits'],dict(candidateWallSeconds=900,candidateCooperativeSeconds=895,reviewWallSeconds=180,reviewCooperativeSeconds=175,rssBytes=RSS_CAP,positiveTerms=MAX_TERMS,normalScientificBytes=184*(1<<20),scientificBytes=192*(1<<20),scientificDirectoryBytes=208*(1<<20),compressedSymbolsBytesPerBundle=64*(1<<20),supervisorLogsBytes=4*(1<<20)),'config.limits')
    compare_fields(audit,cfg['generation'],dict(duration=2,dt=.0025,mode='boids',search='grid',filter='wall-priority',record=True,frameEvery=.1,factoryVariant='wide',expectedCourse='factory-v1',airflow='off',observation='ideal'),'config.generation')
    compare_fields(audit,cfg['primary'],dict(ratio='F/L',maximumMedianPairedRatio=.9,minimumStrictWins=5,requiredCases=[x[0] for x in CASES if x[1]==5000]),'config.primary')
    audit.exact(cfg['screen'],dict(spanLimit=256,componentThreshold=4,runtimeGeneralEquivalenceProven=False),'config.screen')
    mf=audit.path(audit.package,'source-manifest.json');manifest=load_json(mf);pins=manifest.get('files')
    require(isinstance(pins,list) and pins,'source manifest pins absent');seen=set()
    for ix,pin in enumerate(pins):
        require(pin.get('path') not in seen,'duplicate source pin');seen.add(pin.get('path'));audit.pin(audit.root,pin,'source.'+str(ix))
    prefix=str(audit.package.relative_to(audit.root))
    required_files=[str(p.relative_to(audit.root)) for p in (audit.package/'source').iterdir() if p.is_file() and p.suffix in ('.py','.cjs')]
    required_files += [prefix+'/'+x for x in ('config.json','runtime.json','PROTOCOL.md')]
    required_files += ['outputs/milestone-31-source/sim.cjs']
    audit.check(set(required_files)<=seen,'source.all-local-scientific-code-config-runtime-protocol-pinned')
    audit.check(audit.digest(audit.package/'source'/'numeric-reference.py')==INHERITED_REFERENCE_SHA256,'source.inherited-independent-reference-exact-pin')
    audit.check(audit.digest(audit.package/'source'/'lean-anchor.cjs')=='1b57d90d1ce1a45fe3e7f637cae57325861bfc37c907de4d4c6f9e1a79f1af96','source.unchanged-lean-comparator-pin')
    runtime=load_json(audit.path(audit.package,'runtime.json'))
    audit.check(sys.platform==runtime.get('platform')=='darwin' and platform.machine()==runtime.get('architecture')=='arm64','runtime.actual-platform')
    audit.check(sys.version==runtime['python']['version'] and sys.flags.optimize==runtime['flags']['pythonOptimize']==0,'runtime.actual-python-version-flags')
    executable=Path(sys.executable).resolve()
    audit.check(executable.stat().st_size==runtime['python']['bytes'] and audit.digest(executable)==runtime['python']['sha256'],'runtime.actual-python-binary')
    dist=importlib.metadata.distribution('numpy');record=dist.read_text('RECORD')
    audit.check(np.__version__==dist.version==runtime['numpy']['version'] and record is not None and hashlib.sha256(record.encode('utf-8')).hexdigest()==runtime['numpy']['distributionRecordSha256'],'runtime.actual-numpy-distribution')
    audit.check(runtime['flags'].get('nodeOptionsEmpty') is True and runtime['flags'].get('nodeExecArgvEmpty') is True,'runtime.default-node-flags')
    run=load_json(audit.path(audit.package,'results/candidate-run.json'))
    for key in ('closed','supervisorSuccess','childGroupAbsent','runtimeIdentityVerified','protectedInputsUnchanged','candidateOutputsUnchanged'):
        audit.check(run.get(key) is True,'candidate.'+key)
    audit.check(run.get('kind')=='candidate' and run.get('returncode')==0,'candidate.returned-success')
    audit.check(run.get('monitorErrors')==[] and run.get('signals')==[] and isinstance(run.get('exitRaces'),list),'candidate.monitor-cleanup-outcomes')
    audit.check(not any(run.get(k) for k in ('exception','cleanupError','finalizationError','finalWallCapExceeded','finalStorageCapExceeded')),'candidate.no-closure-failure')
    audit.check(run.get('wallCapSeconds')==900 and finite(run.get('elapsedSeconds')) and 0<=run['elapsedSeconds']<=900,'candidate.external-wall-cap')
    audit.check(run.get('rssCapBytes')==RSS_CAP and finite(run.get('sampledPeakRSSBytes')) and 0<run['sampledPeakRSSBytes']<=RSS_CAP and type(run.get('rssSamples')) is int and run['rssSamples']>0,'candidate.external-RSS')
    audit.check(run.get('sampleIntervalSeconds')==.1 and run.get('closureReserveBytes')==1<<20,'candidate.sample-and-closure-reserve')
    audit.check(run.get('sourceManifestSha256')==audit.digest(mf),'candidate.source-manifest')
    audit.check(isinstance(run.get('sourceCommit'),str) and re.fullmatch('[0-9a-f]{40}',run['sourceCommit']) is not None,'candidate.published-source-commit-format')
    audit.exact(run.get('runtime'),runtime,'candidate.pinned-runtime')
    artifact_pins=run.get('artifacts');require(isinstance(artifact_pins,list) and artifact_pins,'candidate closed artifact inventory absent')
    names=set();inventory_bytes=0
    for ix,pin in enumerate(artifact_pins):
        require(pin.get('path') not in names,'duplicate candidate closed artifact pin');names.add(pin['path'])
        audit.pin(audit.package,pin,'candidate.closed-artifact.'+str(ix));inventory_bytes+=pin['bytes']
    audit.check(inventory_bytes==run.get('scientificBytesBeforeClosure'),'candidate.closed-inventory-byte-accounting')
    audit.check(inventory_bytes+(audit.package/'results/candidate-run.json').stat().st_size<=208*(1<<20),'candidate.closed-directory-cap')
    candidate_names={str(p.relative_to(audit.package)) for directory in ('inputs','generation','results') for p in (audit.package/directory).rglob('*') if p.is_file() and not (directory=='results' and (p.name.startswith('review-') or p.name in ('candidate-run.json','independent-review.json','analysis.json','qualification.json')))}
    audit.check(names==candidate_names,'candidate.closed-inventory-complete')
    lock=audit.path(audit.package,'results/candidate-invocation.lock');audit.check(lock.stat().st_size>0,'candidate.allocation-consumed')
    reviewlock=audit.path(audit.package,'results/review-invocation.lock');audit.check(reviewlock.stat().st_size>0,'review.allocation-consumed')
    admin={'candidate-invocation.lock','candidate-stdout.txt','candidate-stderr.txt','candidate-run.json','review-invocation.lock','review-stdout.txt','review-stderr.txt','review-run.json','independent-review.json','analysis.json','qualification.json'}
    total=scientific=normal=logbytes=0
    for directory in ('inputs','generation','results'):
        for path in (audit.package/directory).rglob('*'):
            if not path.is_file():continue
            require(path.resolve().is_relative_to(audit.package),'scientific artifact escapes package')
            size=path.stat().st_size;total+=size
            if directory=='results' and path.name.endswith(('-stdout.txt','-stderr.txt')):logbytes+=size
            if directory=='results' and path.parent==audit.package/'results' and path.name in admin:continue
            scientific+=size
            if not (directory=='results' and path.name in ('failure.json','partial-evidence.json')):normal+=size
    audit.check(total<=208*(1<<20) and logbytes<=4*(1<<20),'review.current-directory-and-logs-caps')
    audit.check(scientific<=192*(1<<20) and normal<=184*(1<<20),'candidate.scientific-normal-and-reserve-caps')
    candidate_logs=sum(pin['bytes'] for pin in artifact_pins if pin['path'].endswith(('-stdout.txt','-stderr.txt')))
    audit.check(candidate_logs==run.get('logBytes') and candidate_logs<=4*(1<<20),'candidate.closed-log-cap-and-accounting')
    if audit.evidence.get('complete') is True:
        audit.check(audit.evidence.get('newScientificBytesBeforeEvidence')==scientific-(audit.package/'results/evidence.json').stat().st_size,'candidate.before-evidence-byte-accounting')
    memory=audit.evidence.get('memory',{})
    audit.check(finite(memory.get('sampledPeakRSSBytes')) and 0<memory['sampledPeakRSSBytes']<=RSS_CAP,'candidate.internal-RSS')
    audit.check(isinstance(memory.get('processResourceUsage'),dict) and isinstance(memory.get('platformMaxRSSUnits'),str),'candidate.memory-units')
    audit.resources=dict(candidateExternalElapsedSeconds=run.get('elapsedSeconds'),externalSampledPeakRSSBytes=run.get('sampledPeakRSSBytes'),rssSamples=run.get('rssSamples'),directoryBytesAtReview=total,scientificBytes=scientific,normalScientificBytes=normal,reviewAllocationSeconds=180,reviewCooperativeSeconds=175,candidateSupervisorSuccess=run.get('supervisorSuccess'),sourceCommit=run.get('sourceCommit'),sourceManifestSha256=run.get('sourceManifestSha256'))
    for stage in ('environmentStart','environmentEnd'):
        env=audit.evidence.get(stage,{})
        for key in ('cpuModel','architecture','platform','kernel','node','v8','clock','threads'):
            audit.check(key in env and (env[key] is None or isinstance(env[key],str)),stage+'.'+key)
        audit.check(env.get('nodeExecutableSha256')==runtime['node']['sha256'] and env.get('node')==runtime['node']['version'] and env.get('platform')==runtime['platform'] and env.get('architecture')==runtime['architecture'],stage+'.pinned-node')
        audit.check(env.get('nodeOptionsEmpty') is True and env.get('executionFlagCount')==0,stage+'.default-runtime-flags')
        audit.check(type(env.get('logicalCores')) is int and env['logicalCores']>0 and finite(env.get('installedRAMBytes')) and env['installedRAMBytes']>0,stage+'.hardware')
        audit.check(all(k in env for k in ('physicalCores','powerSource','lowPowerMode','loadAverage')),stage+'.environment-observations')
        load=env.get('loadAverage');audit.check(isinstance(load,list) and len(load)==3 and all(finite(x) and x>=0 for x in load),stage+'.load-average')
    start,end=audit.evidence.get('environmentStart',{}),audit.evidence.get('environmentEnd',{})
    for key in ('nodeExecutableSha256','node','v8','architecture','platform','kernel','clock'):audit.check(key in start and start[key]==end.get(key),'environment.stable-'+key)

def output_bytes(audit,path,obj):
    payload=(json.dumps(safe_json(obj),allow_nan=False,indent=2)+'\n').encode('utf-8')
    total=sum(p.stat().st_size for directory in ('inputs','generation','results') for p in (audit.package/directory).rglob('*') if p.is_file())
    require(total+len(payload)<=208*(1<<20)-(1<<20),'review output exceeds aggregate supervisor-closure reserve')
    with path.open('xb') as stream:stream.write(payload)

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('package',type=Path);parser.add_argument('output',type=Path)
    args=parser.parse_args();package=args.package.resolve();out=args.output.resolve()
    require(package.is_dir() and out==package/'results/independent-review.json','fixed reviewer output path required')
    require(not out.exists() and not (package/'results/analysis.json').exists(),'review outputs must be exclusive new files')
    audit=Audit(package);completed=False
    try:
        evidence=package/'results/evidence.json'
        if not evidence.is_file():evidence=package/'results/partial-evidence.json'
        audit.evidence=load_json(evidence)
        audit.check(audit.evidence.get('complete') is True and audit.evidence.get('kind')=='fresh-boids-center-screen','candidate.complete-kind')
        provenance_resources(audit)
        require(not audit.errors,'candidate closure/provenance/resource gate failed')
        controls_review(audit);ownership_review(audit);entries=generation_review(audit)
        require(not audit.errors,'controls/ownership/generation gate failed')
        audit.check(len(audit.evidence.get('qualification',[]))==6,'qualification.six-builds-solves')
        for item in audit.generation:independent_case(audit,item)
        audit.check(len(audit.frames)==3 and all(f['complete'] and f['pass'] for f in audit.frames),'qualification.all-three-independent-cases')
        require(not audit.errors,'independent qualification failed before timing interpretation')
        timing_review(audit,[entry['id'] for entry in entries]);audit.guard();completed=True
    except Exception as error:audit.error('review-error',error)
    result=analysis(audit)
    if not completed:result.update(independentAuditPass=False,performanceRulePass=None,reason='incomplete-or-failed-audit')
    output_bytes(audit,package/'results/analysis.json',result)
    report=dict(kind='independent-fresh-center-screen-review',complete=completed,**{'pass':completed and not audit.errors},candidateComplete=audit.evidence.get('complete') is True,
        checkCount=len(audit.checks),errors=audit.errors,checks=audit.checks,
        generation=[dict(id=x['id'],n=x['n'],seed=x['seed']) for x in audit.generation],controls=audit.controls,qualification=audit.frames,
        coverage=dict(validatedTimingRecords=len(audit.calls),expectedTimingRecords=42,expectedControls=48,expectedFreshCases=3),
        timing=result,analysis=dict(path='results/analysis.json',bytes=(package/'results/analysis.json').stat().st_size,sha256=audit.digest(package/'results/analysis.json')),
        resources=audit.resources,reviewElapsedSeconds=time.monotonic()-audit.started,
        limitations=['This is finite-runtime evidence for the fixed controls and three new saved states; no universal Math.hypot equivalence proof or unseen-state guarantee.',
        'Independent NumPy hypot/reduction can differ in rounding; exact symbol requirements and inherited numerical tolerances are not relaxed.',
        'Timed transient arrays are fully compared in the candidate process but are not all saved; the independent audit cannot reconstruct every transient timed array.',
        'Saved ownership evidence and source review cover the fixed calls, not all possible future aliasing behavior.',
        'Short synthetic airflow-off generation and frozen-state loads do not establish aerodynamic validity, coupled flight, browser/GPU/live cost, or novel contribution.',
        'The positive-term cap throw is source-reviewed, not exercised with a new giant fixture.',
        'This child cannot observe its own terminal supervisor closure. practicalRulePass stays null until a frozen external seal verifies both terminal supervisors.',
        'The previously disclosed result-bearing arithmetic-file exposure remains; this is not an unexposed design process.'])
    audit.guard();output_bytes(audit,out,report)
    print(json.dumps(dict(**{'pass':report['pass']},complete=completed,checks=len(audit.checks),errors=len(audit.errors),performanceRulePass=result.get('performanceRulePass'),practicalRulePass=None)))
    return 0 if report['pass'] else 1

if __name__=='__main__':raise SystemExit(main())
