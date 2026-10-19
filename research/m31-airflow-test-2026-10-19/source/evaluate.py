"""One prospective, no-fit axial airflow comparison; no evaluation on import."""
import hashlib,importlib.util,json,math,pathlib,struct,time,zlib
BASE=pathlib.Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('piv_mat5',BASE/'source/mat5.py');mat=importlib.util.module_from_spec(spec);spec.loader.exec_module(mat)
def guard():
    root=BASE.parents[1];b=(BASE/'source-manifest.json').read_bytes();m=json.loads(b)
    receipt=json.loads((BASE/'source-publication.json').read_text())
    assert receipt['manifestSha256']==hashlib.sha256(b).hexdigest() and receipt['remoteBytesEqualLocal'] and receipt['committedBytesEqualLocal']
    for p in m['files']:
        raw=(root/p['path']).read_bytes();assert len(raw)==p['bytes'] and hashlib.sha256(raw).hexdigest()==p['sha256'],p['path']
    return receipt['commit']
def radial_fade(r):
    if r<=2:return 1.
    if r>=3:return 0.
    t=r-2;return (1-t)**2*(1+2*t)

def predictions(X,Z):
    k=2*math.sqrt(2);q=Z/k+5.817;w=.07668*q*k;r=math.sqrt(X*X+1)/w
    f=radial_fade(r)
    a=(10.11/q)/(1+(math.sqrt(2)-1)*r*r)**2*f
    qb=Z+6.0585;wb=.0667*qb
    b=(9.508/qb)/(1+(math.sqrt(2)-1)*(abs(X)/wb)**2)**2
    return a,b

def metrics(rows,key):
    if not rows:return {'count':0,'mae':None,'rmse':None,'bias':None,'maxAbsoluteError':None,'maxIndex':None}
    es=[r[key]-r['u'] for r in rows];mx=max(range(len(es)),key=lambda i:abs(es[i]))
    return {'count':len(rows),'mae':math.fsum(abs(e) for e in es)/len(es),'rmse':math.sqrt(math.fsum(e*e for e in es)/len(es)),'bias':math.fsum(es)/len(es),'maxAbsoluteError':abs(es[mx]),'maxIndex':rows[mx]['index']}

def controls():
    def el(t,b):return struct.pack('<II',t,len(b))+b+b'\0'*((-len(b))%8)
    head=b' '*124+struct.pack('<H',256)+b'IM';flags=el(6,struct.pack('<II',6,0));dims=el(5,struct.pack('<ii',2,3));name=struct.pack('<I',1|(1<<16))+b'a\0\0\0'
    payload=el(14,flags+dims+name+el(9,struct.pack('<6d',1,2,float('nan'),4,5,6)))
    cp=zlib.compress(payload);packed=head+struct.pack('<II',15,len(cp))+cp
    for raw in [head+payload,packed]:
        d=mat.read(raw,allow_nonfinite=True);assert d['shape']==[2,3] and d['values'][1]==2 and math.isnan(d['values'][2]) and d['values'][5]==6
    for raw in [packed[:-1],packed]:
        try:mat.read(raw)
        except ValueError:pass
        else:raise AssertionError('malformed/nonfinite accepted')
    k=2*math.sqrt(2)
    for X,Z in [(0.,8.),(1.,12.),(4.,30.)]:
        a,b=predictions(X,Z);assert (a,b)==predictions(-X,Z)
        # Same RSS model rewritten entirely in D units, including numerator/origin.
        zd=Z/k;xd=X/k;s0=6.0585/k;bd=9.508/k;w=.0667*(zd+s0)
        alt=(bd/(zd+s0))/(1+(math.sqrt(2)-1)*(xd/w)**2)**2
        assert abs(b-alt)<2e-15 and a>=0 and b>0
    assert radial_fade(2)==1 and radial_fade(3)==0
    return {'passed':True,'checks':['plain/compressed masked MAT','truncation and strict nonfinite refused','three symmetry and unit-conversion identities','two fade endpoints']}

def main():
    t=time.monotonic();out=BASE/'results';out.mkdir(exist_ok=True)
    with (out/'launch.lock').open('x') as f:f.write('sole airflow comparison\n')
    try:
        commit=guard();(out/'controls.json').write_text(json.dumps(controls(),indent=2)+'\n')
        arrays={}
        for pin in json.loads((BASE/'DATA-PINS.json').read_text()):
            raw=(BASE/'data'/pin['file']).read_bytes();assert len(raw)==pin['bytes'] and hashlib.sha256(raw).hexdigest()==pin['sha256']
            if not pin['file'].endswith('.mat'):continue
            a=mat.read(raw,allow_nonfinite=True);assert a['name']==pin['file'][:-4] and a['shape']==[272,537];arrays[a['name']]=a['values']
        counts=dict(candidates=0,nonfiniteCoordinates=0,outsideDomain=0,missingU=0,accepted=0,missingV=0);cases=[]
        for c in range(0,537,4):
            for r in range(0,272,4):
                i=c*272+r;counts['candidates']+=1;X=arrays['x_piv'][i];Z=arrays['z_piv'][i]
                if not math.isfinite(X) or not math.isfinite(Z):counts['nonfiniteCoordinates']+=1;continue
                if not (8<=Z<=30 and abs(X)<=4):counts['outsideDomain']+=1;continue
                u=arrays['u_piv'][i];v=arrays['v_piv'][i]
                if not math.isfinite(u):counts['missingU']+=1;continue
                if not math.isfinite(v):counts['missingV']+=1;v=None
                a,b=predictions(X,Z);cases.append(dict(row=r,column=c,index=i,X=X,Z=Z,u=u,v=v,a=a,b=b,residualA=a-u,residualB=b-u));counts['accepted']+=1
        assert counts['candidates']<=9216 and len(cases)>=20 and len(set(c['Z'] for c in cases))>=3
        bins=[]
        for lo,hi,label in [(8,12,'8<=Z<12'),(12,20,'12<=Z<20'),(20,30,'20<=Z<=30')]:
            rows=[c for c in cases if lo<=c['Z'] and (c['Z']<=hi if hi==30 else c['Z']<hi)]
            bins.append({'label':label,'a':metrics(rows,'a'),'b':metrics(rows,'b')})
        ma=metrics(cases,'a');mb=metrics(cases,'b')
        result={'status':'completed-descriptive-airflow-comparison','sourceCommit':commit,'units':'axial velocity / Ui','models':{'a':'M31-directed-axial-wake-v1','b':'RSS-published-planar-fit'},'counts':counts,'cases':cases,'metrics':{'a':ma,'b':mb},'maeDifferenceAminusB':ma['mae']-mb['mae'],'bins':bins,'plane':{'y_l':1,'l_m':.0325},'limits':['RSS curve fitted to these experiments; no independent validation','Finite sampled mean cells are not independent trials','Planar field only; full3D airflow and receiving thrust untested','Calibration and stitched-field uncertainties not quantified','Original Bauersfeld observable is flow magnitude; A is project axial interpretation','A assumes shared Ui=UH induced-velocity normalization; no independent SI calibration']}
        body=json.dumps(result,indent=2,allow_nan=False)+'\n';assert len(body.encode())<16*1024**2 and time.monotonic()-t<60
        (out/'comparison.json').write_text(body);(out/'execution.json').write_text(json.dumps({'status':'complete','elapsedSeconds':time.monotonic()-t,'resultBytes':len(body.encode()),'sha256':hashlib.sha256(body.encode()).hexdigest()},indent=2)+'\n');print(json.dumps({'counts':counts,'metrics':result['metrics']}))
    except BaseException as e:
        (out/'failure.json').write_text(json.dumps({'type':type(e).__name__,'message':str(e),'elapsedSeconds':time.monotonic()-t},indent=2)+'\n');raise
if __name__=='__main__':main()
