"""Single bounded, no-fit experiment. Invoke after public source verification."""
import hashlib,itertools,json,math,pathlib,struct,time,zlib
import importlib.util
BASE=pathlib.Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("physical_mat5",BASE/"source/mat5.py")
mat5=importlib.util.module_from_spec(spec);spec.loader.exec_module(mat5)
read=mat5.read

def root(alpha):
    if not math.isfinite(alpha) or alpha<0: raise ValueError('alpha')
    if alpha==0:return 1.0
    lo,hi=0.,1.
    for _ in range(56):
        x=(lo+hi)/2
        if x*x*x+alpha*x>1:hi=x
        else:lo=x
    return (lo+hi)/2

def fade(start,end,x):
    if x<=start:return 1.
    if x>=end:return 0.
    t=(x-start)/(end-start);return (1-t)**2*(1+2*t)

def predict(z,l=.0325,qu=1.,ql=1.):
    D=2*l
    if z<2.5*D:raise ValueError('near domain')
    if math.hypot(z,0)>=3 or z>=2.5:return {'upper':qu,'lower':ql,'alpha':0.,'rotorRatio':1.}
    zn=z/D;w=.07668*(zn+5.817)*D;r=l
    profile=0. if r>=3*w else (10.11/(zn+5.817))/(1+(math.sqrt(2)-1)*(r/w)**2)**2*fade(2,2.5,z)*fade(2,3,r/w)
    alpha=profile*math.sqrt(qu/ql);x=root(alpha)
    return {'upper':qu,'lower':ql*x,'alpha':alpha,'rotorRatio':x}

def controls():
    def el(t,b):return struct.pack('<II',t,len(b))+b+b'\0'*((-len(b))%8)
    flags=el(6,struct.pack('<II',6,0));dims=el(5,struct.pack('<ii',2,3))
    # MATLAB values are column-major: rows [1,3,5],[2,4,6].
    vals=el(9,struct.pack('<6d',1,2,3,4,5,6));name=struct.pack('<I',1|(1<<16))+b'a\0\0\0'
    matrix=el(14,flags+dims+name+vals);head=b' '*124+struct.pack('<H',256)+b'IM'
    packed=zlib.compress(matrix);compressed=head+struct.pack('<II',15,len(packed))+packed
    for b in [head+matrix,compressed]:
        r=read(b);assert r=={'name':'a','shape':[2,3],'order':'column-major','values':[1,2,3,4,5,6]}
    failures=[]
    for label,b in [('truncated',compressed[:-1]),('nonfinite',head+el(14,flags+dims+name+el(9,struct.pack('<6d',1,2,float('nan'),4,5,6))))]:
        try:read(b)
        except ValueError:failures.append(label)
        else:raise AssertionError(label)
    assert len(failures)==2 and root(0)==1
    for a in [0.,.01,1.,10.]:
        x=root(a);assert abs(x**3+a*x-1)<1e-14
    try:predict(.13)
    except ValueError:pass
    else:raise AssertionError('near exclusion')
    assert predict(.21)['upper']==predict(1.1)['upper']==1
    return {'passed':True,'parser':['plain','compressed','small tag','column major','truncated rejected','nonfinite rejected'],'model':['zero root','four cubic residuals','near refused','upper null']}

def main():
    start=time.monotonic();out=BASE/'results';out.mkdir(exist_ok=True)
    with (out/'launch.lock').open('x') as f:f.write('single physical comparison\n')
    try:
        c=controls();(out/'controls.json').write_text(json.dumps(c,indent=2)+'\n')
        arrays={}
        for pin in json.loads((BASE/'SCHEMA.json').read_text()):
            name=pin['name'];b=(BASE/'data'/ (name+'.mat')).read_bytes()
            assert len(b)==pin['bytes'] and hashlib.sha256(b).hexdigest()==pin['sha256']
            if name not in ['x_l','z_l','upper_F_W','lower_F_W','upper_Fstd_W','lower_Fstd_W']:continue
            a=read(b);assert a['name']==name and a['shape']==[14,12];arrays[name]=a['values']
        assert arrays['x_l'][:14]==[0.]*14
        zs=arrays['z_l'][:14];assert [i for i,z in enumerate(zs) if z>=6]==list(range(2,14))
        assert all(zs[i]<zs[i+1] for i in range(13))
        cases=[]
        for i in range(2,14):
            z=zs[i]*.0325;p=predict(z)
            observed={k:arrays[k][i] for k in ['upper_F_W','lower_F_W','upper_Fstd_W','lower_Fstd_W']}
            assert observed['upper_Fstd_W']>=0 and observed['lower_Fstd_W']>=0
            sensitivity=[]
            for l,dz,qu,ql in itertools.product([.03245,.0325,.03255],[-.001,0.,.001],[.9,1.,1.1],[.9,1.,1.1]):
                sp=predict(z+dz,l,qu,ql);sensitivity.append({'l':l,'dz':dz,'qu':qu,'ql':ql,**sp})
            cases.append({'row':i,'column':0,'x_l':0.,'z_l':zs[i],'z_m':z,'observed':observed,'prediction':p,'lowerResidual':observed['lower_F_W']-p['lower'],'sensitivity':sensitivity,'sampledLowerRange':[min(s['lower'] for s in sensitivity),max(s['lower'] for s in sensitivity)]})
            assert time.monotonic()-start<60
        difference=cases[0]['observed']['upper_F_W']-cases[-1]['observed']['upper_F_W']
        errors=[abs(c['lowerResidual']) for c in cases]
        result={'status':'completed-descriptive-comparison','model':'Kiran-stacked-fixedPWM-v1','units':'force divided by W; approximate W=0.265 N','cases':cases,'excluded':[{'row':0,'z_m':zs[0]*.0325,'reason':'near domain'},{'row':1,'z_m':zs[1]*.0325,'reason':'preselected conservative margin'}],'primary':{'nearRow':2,'farRow':13,'measuredDifference':difference,'predictedDifference':0.,'minimumDifferentialBiasToReconcile':abs(difference),'equalOpposingPerCaseBias':abs(difference)/2,'approxDifferenceN':difference*.265,'calibratedStatisticalRejection':False},'secondary':{'mae':sum(errors)/len(errors),'maxAbsoluteError':max(errors),'maxAbsoluteErrorApproxN':max(errors)*.265,'maeApproxN':sum(errors)/len(errors)*.265},'counts':{'cases':12,'nominalEvaluations':12,'sensitivityEvaluations':972},'limitations':['Aggregate published means, not individual trials','SD semantics unresolved; not confidence intervals','Tare drift calibration and full pose uncertainty unavailable','Lower nominal baseline equals W by assumption','Sensitivity grid is illustrative, not a validated uncertainty enclosure','Not a blind holdout, not a novelty claim']}
        body=json.dumps(result,indent=2,allow_nan=False)+'\n';assert len(body)<32*1024**2
        (out/'comparison.json').write_text(body)
        (out/'execution.json').write_text(json.dumps({'status':'completed','elapsedSeconds':time.monotonic()-start,'resultBytes':len(body),'resultSha256':hashlib.sha256(body.encode()).hexdigest()},indent=2)+'\n')
        print(json.dumps({'primary':result['primary'],'secondary':result['secondary'],'counts':result['counts']}))
    except BaseException as e:
        (out/'failure.json').write_text(json.dumps({'type':type(e).__name__,'message':str(e),'elapsedSeconds':time.monotonic()-start},indent=2)+'\n');raise
if __name__=='__main__':main()
