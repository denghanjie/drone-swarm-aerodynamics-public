"""Input serialization only; no scientific/candidate modules or model calls."""
import json
import struct
from pathlib import Path
P=Path(__file__).resolve().parents[1]
def word(token):
    if token.startswith('bits:'):
        result=token[5:]
        assert len(result)==16 and all(c in '0123456789abcdef' for c in result)
        return result
    return struct.pack('>d',float(token)).hex()
def endpoint(token):return word(token)
def interval(a,b=None):return {'l':endpoint(a),'u':endpoint(a if b is None else b)}
Z='bits:0000000000000000'; NZ='bits:8000000000000000'
U='bits:0000000000000001'; NU='bits:8000000000000001'
S='bits:000fffffffffffff'; NS='bits:800fffffffffffff'
N='bits:0010000000000000'; NN='bits:8010000000000000'
M='bits:7fefffffffffffff'; NM='bits:ffefffffffffffff'
H='bits:3ca0000000000000'; NH='bits:bca0000000000000'
Q='bits:3c90000000000000'; NQ='bits:bc90000000000000'
A='bits:3ff0000000000001'; NA='bits:bff0000000000001'
B='bits:3fefffffffffffff'
edge=[('positive-zero',Z),('negative-zero',NZ),('positive-min-subnormal',U),
('negative-min-subnormal',NU),('positive-max-subnormal',S),('negative-max-subnormal',NS),
('positive-min-normal',N),('negative-min-normal',NN),('positive-one','1'),('negative-one','-1'),
('positive-max-finite',M),('negative-max-finite',NM),('positive-infinity','bits:7ff0000000000000'),
('negative-infinity','bits:fff0000000000000'),('positive-qnan','bits:7ff8000000000001'),
('negative-qnan','bits:fff8000000000001')]
records=[]
for op in ('nextUp','nextDown'):
    for label,value in edge:
        records.append({'kind':'primitive','id':op.lower()+'-'+label,'op':op,'word':word(value)})
def add(op,label,*args):records.append({'kind':'primitive','id':op+'-'+label,'op':op,'args':list(args)})
for label,a,b in [
('tie-positive',interval('1'),interval(H)),('tie-negative',interval('-1'),interval(NH)),
('cancellation',interval('1'),interval('-1')),('normal-boundary',interval(S),interval(Z)),
('subnormal-residual',interval(N),interval(NS)),('overflow-positive',interval(M),interval(M)),
('overflow-negative',interval(NM),interval(NM)),('crossing-intervals',interval('-1','1'),interval(NH,H))]:add('add',label,a,b)
for label,a,b in [
('tie-positive',interval('1'),interval(Q)),('tie-negative',interval('-1'),interval(NQ)),
('cancellation',interval('1'),interval('1')),('subnormal',interval(U),interval(NU)),
('normal-boundary',interval(N),interval(S)),('overflow-positive',interval(M),interval(NM)),
('overflow-negative',interval(NM),interval(M)),('crossing-intervals',interval('-1','1'),interval(NH,H))]:add('sub',label,a,b)
for label,a,b in [
('rounding-positive',interval(A),interval(B)),('rounding-negative',interval(NA),interval(B)),
('underflow-positive',interval(U),interval('.5')),('underflow-negative',interval(NU),interval('.5')),
('normal-to-subnormal',interval(N),interval('.5')),('overflow',interval(M),interval('2')),
('mixed-signs',interval('-1','2'),interval('-3','4')),('tiny-crossing',interval(NU,U),interval(NU,U))]:add('mul',label,a,b)
for label,a,b in [
('third-positive',interval('1'),interval('3')),('third-negative',interval('-1'),interval('3')),
('underflow-positive',interval(U),interval('2')),('underflow-negative',interval(NU),interval('2')),
('negative-divisor',interval('1','2'),interval('-4','-2')),('crossing-numerator',interval('-1','1'),interval('2','3')),
('zero-divisor',interval('1'),interval('-1','1')),('overflow',interval(M),interval(U))]:add('div',label,a,b)
for label,a in [
('zero-crossing',interval('-1','1')),('signed-zeros',interval(NZ,Z)),
('tiny-positive',interval(U)),('tiny-negative',interval(NU)),('positive-interval',interval('2','3')),
('negative-interval',interval('-3','-2')),('overflow',interval(M)),('reversed',interval('1','-1'))]:add('square',label,a)
I=['0','0','0','1'];T=['.6','0','0','.8'];L=['-.6','0','0','.8'];C=['.5','.5','.5','.5']
def state(center=('0','0','0'),q=None,motors=None):
    return list(center)+['0']*3+list(I if q is None else q)+['0']*3+list(motors or ['.049','.057','.068','.061'])
literals=[]
def pair(name,source,receiver=None,rotor=0):
    r=state() if receiver is None else receiver
    literals.append({'kind':'pair','id':name,'receiver':r,'source':source,'rotor':rotor})
for name,center in [
('neighbor-far',('4','0','0')),('neighbor-equal',('3','0','0')),
('neighbor-before',('bits:4007ffffffffffff','0','0')),('neighbor-after',('bits:4008000000000001','0','0')),
('neighbor-negative',('-4','0','0')),('neighbor-diagonal-inside',('2','2','0')),
('neighbor-diagonal-boundary',('1.8','2.4','0')),('center-guard-equal',('257','0','0'))]:pair(name,state(center))
for name,z in [
('down-negative','-.5'),('down-zero','0'),('down-negative-subnormal',NU),('down-positive-subnormal',U),
('down-cut-before','bits:4003ffffffffffff'),('down-cut-equal','2.5'),
('down-cut-after','bits:4004000000000001'),('down-interior','1.25')]:pair(name,state(('.028','.028',z)))
pair('tilted-source-positive',state(('.028','-.932','.278'),T),rotor=1)
pair('tilted-source-mirrored',state(('.028','.988','.278'),L),rotor=2)
pair('axis-permutation',state(('1.028','.028','0'),C),rotor=3)
pair('dot-cancellation-zero',state(('.028','.308','.96'),T))
pair('dot-cancellation-down-cut',state(('.028','-2.372','.7'),T))
large='35184372088832'
pair('translated-neighbor-boundary',state(('35184372088835',large,large)),state((large,large,large)))
pair('translated-tilted-point',state((large,large,large),T),state((large,large,large),T),rotor=3)
pair('guard-before-upstream',state(('258','.028','-.5')))
pair('tail-positive',state(('.028','.028','1')))
pair('tail-near',state(('.028','.028','.1')))
pair('tail-near-outside',state(('.228','.028','.1')))
pair('tail-radial',state(('.728','.028','1')))
pair('tail-projection',state(('0','.028','1.028')),state(q=C))
pair('tail-cap',state(('.028','.028','1'),motors=['1e24']*4))
pair('overflow-geometry',state((M,'0','0')),state((NM,'0','0')))
pair('invalid-force-zero',state(('.028','.028','1'),motors=['0','.057','.068','.061']))
pair('invalid-force-negative',state(('.028','.028','1'),motors=['-.049','.057','.068','.061']))
pair('invalid-quaternion',state(('.028','.028','1'),q=['0','0','0','2']))
x=state(('.028','.028','1'));x[3]='bits:7ff8000000000001';pair('invalid-nan-velocity',x)
x=state(('.028','.028','1'));x[10]='bits:7ff0000000000000';pair('invalid-infinity-angular',x)
assert len(records)==72 and len(literals)==36
for row in literals:
    records.append(dict(row,receiver=[word(x) for x in row['receiver']],source=[word(x) for x in row['source']]))
assert len(records)==108 and len({x['id'] for x in records})==108
spec={'id':'m31-filter-correctness-v1','constants':{'mg0':'.027','g':'9.81','arm':'.028','radius':'.023','rho':'1.225','decay':'10.11','spread':'.07668','origin':'-5.817','minDown':'2.5','neighbor':'3','nearRad':'.15','downFade':'2','downCut':'2.5','radFade':'2','radCut':'3','qTolerance':'1e-10','geometryTolerance':'1e-9'},'PIBits':'400921fb54442d18','corners':[[1,1,0],[-1,1,0],[-1,-1,0],[1,-1,0]],'expectedRecords':108,'expectedPrimitiveRecords':72,'expectedPairRecords':36,'referenceBits':192,'fractionBits':96,'records':records,'scope':'Primitive and single-pair finite correctness only; no full load solve or performance inference.'}
(P/'prefreeze/PAIR-LITERALS.json').write_text(json.dumps(literals,indent=2)+'\n')
(P/'source/spec.json').write_text(json.dumps(spec,indent=2)+'\n')
print('Serialized108fixed input records; no candidate imports or model evaluation.')
