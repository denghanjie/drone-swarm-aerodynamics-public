"""One bounded source-accounting audit, separate from all historical campaigns."""
import sys, os, re, json, math, hashlib, subprocess, time, platform
from pathlib import Path

def save(path, value):
    data=(json.dumps(value, indent=2, allow_nan=False)+'\n').encode()
    with path.open('xb') as stream:
        stream.write(data)

def fade(lo, hi, x):
    if x <= lo: return 1.0
    if x >= hi: return 0.0
    t=(x-lo)/(hi-lo)
    return (1-t)**2*(1+2*t)

def simpson(fn, lo, hi, n):
    h=(hi-lo)/n
    return h/3*(fn(lo)+fn(hi)+math.fsum((4 if i%2 else 2)*fn(lo+i*h) for i in range(1,n)))

def main():
    base=Path(__file__).resolve().parents[1]
    repo=base.parents[1]
    if len(sys.argv)!=2: raise ValueError('Supply the existing Node executable')
    node=Path(sys.argv[1]); out=base/'results'
    source_commit=os.environ.get('RESEARCH_SOURCE_COMMIT','')
    assert re.fullmatch('[0-9a-f]{40}',source_commit),'Source commit required'
    if any(out.iterdir()): raise ValueError('Results directory must be empty; no overwrite or retry')
    freeze_bytes=(base/'freeze.json').read_bytes()
    freeze=json.loads(freeze_bytes)
    for pin in freeze['files']:
        data=(repo/pin['path']).read_bytes()
        assert len(data)==pin['bytes'] and hashlib.sha256(data).hexdigest()==pin['sha256'],pin['path']
    start=time.perf_counter()
    save(out/'started.json',{'sourceCommit':source_commit,'freezeSHA256':hashlib.sha256(freeze_bytes).hexdigest(),'pythonVersion':platform.python_version(),'nodeExecutableSHA256':hashlib.sha256(node.read_bytes()).hexdigest(),'scope':'New CPU-only finite source audit; no historical campaign invocation'})
    # Only one direct child; no browser or child process acquisition/monitoring.
    witness=subprocess.run([str(node),str(base/'source/witness.cjs')],capture_output=True,timeout=5)
    (out/'witness-stdout.json').write_bytes(witness.stdout)
    (out/'witness-stderr.txt').write_bytes(witness.stderr)
    assert len(witness.stdout)+len(witness.stderr)<100000
    w=json.loads(witness.stdout)
    assert witness.returncode==0 and w['calls']==20 and w['stimulusAdmitted'] and w['sourceIndependentInTheseCases']
    a=math.sqrt(2)-1; C=10.11; S=.07668; origin=-5.817
    arm=.028; R=.023; D=2*math.sqrt(2)*arm; rho=1.225; mass=.027; g=9.81
    T=mass*g; UH=math.sqrt(T/(8*rho*math.pi*R*R))
    full_integral=1/(6*a)
    tail3=1/(6*a*(1+9*a)**3)
    shape=lambda x:x/(1+a*x*x)**4
    q=[]
    for n in [128,256,512,1024]:
        full=math.fsum(simpson(shape,lo,lo+1,n) for lo in [0,1,2])+tail3
        radial=math.fsum(simpson(lambda x:shape(x)*fade(2,3,x)**2,lo,lo+1,n) for lo in [0,1,2])
        q.append({'subdivisionsPerUnitInterval':n,'untruncatedIntegral':full,'analyticIntegral':full_integral,'absoluteError':abs(full-full_integral),'radialFadedIntegral':radial,'retention':radial/full_integral})
    gate=q[-1]['absoluteError']<=1e-9 and abs(q[-1]['untruncatedIntegral']-q[-2]['untruncatedIntegral'])<=1e-9 and abs(q[-1]['radialFadedIntegral']-q[-2]['radialFadedIntegral'])<=1e-9
    ratio=C*C*S*S*D*D/(24*a*R*R)
    planes=[]
    for s in [.25,.6,1,1.5,2,2.1,2.25,2.4,2.5,3]:
        b=S*(s/D-origin)*D; Uc=C*UH/(s/D-origin); f=fade(2,2.5,s)
        untruncated=math.pi*rho*Uc*Uc*b*b/(3*a)
        radial=2*math.pi*rho*Uc*Uc*b*b*q[-1]['radialFadedIntegral']
        planes.append({'downstreamM':s,'halfWidthM':b,'nominalRadialCutoffM':3*b,'fadedFieldIdenticallyZero':f==0,'centerlineUntruncatedMps':Uc,'downstreamFade':f,'JUntruncatedN':untruncated,'JRadialOnlyN':radial,'JBothFadesN':radial*f*f,'JBothOverNominalWeight':radial*f*f/T,
          'profile':[{'xi':k/10,'radiusM':k/10*b,'untruncatedMps':Uc/(1+a*(k/10)**2)**2,'radialOnlyMps':Uc/(1+a*(k/10)**2)**2*fade(2,3,k/10),'bothFadesMps':Uc/(1+a*(k/10)**2)**2*fade(2,3,k/10)*f} for k in range(41)]})
    nf,nb,Ff,Fb=94.,81.,5.32,3.90
    pred=(nf/nb)**2; observed=Ff/Fb
    published={'source':'https://link.springer.com/article/10.1007/s00348-024-03880-3','locator':'section3.2','frontFrequencyHz':nf,'backFrequencyHz':nb,'frontFlowMomentumN':Ff,'backFlowMomentumN':Fb,'printedFrontBackSumN':Ff+Fb,'totalFlowMomentumN':9.21,'weightProxyN':8.98,'authorReportedForceRatio':1.366,'authorReportedSquaredFrequencyRatio':1.347,'recomputedSquaredFrequencyRatio':pred,'recomputedFlowRatio':observed,'signedRatioDifference':pred-observed,'relativeRatioDifference':pred/observed-1,'squaredFrequencyRoundingRange':[((nf-.5)/(nb+.5))**2,((nf+.5)/(nb-.5))**2],'flowRatioRoundingRange':[(Ff-.005)/(Fb+.005),(Ff+.005)/(Fb-.005)],'roundingRangesAreMeasurementUncertainty':False,'physicalValidationEstablished':False}
    plane_invariance=max(abs(p['JUntruncatedN']/T-ratio) for p in planes)
    gate=gate and plane_invariance<=1e-12
    result={'convergence512To1024':{'untruncatedAbsoluteDifference':abs(q[-1]['untruncatedIntegral']-q[-2]['untruncatedIntegral']),'radialFadedAbsoluteDifference':abs(q[-1]['radialFadedIntegral']-q[-2]['radialFadedIntegral'])},'planeRatioMaxDifference':plane_invariance,'kind':'finite-source-accounting-result','numericalGatePass':gate,'constants':{'a':a,'C':C,'S':S,'origin':origin,'D':D,'rotorRadius':R,'rho':rho,'mass':mass,'g':g,'nominalWeightN':T,'UH':UH},'untruncatedJOverWeight':ratio,'quadrature':q,'radialSquaredProfileRetention':q[-1]['retention'],'planes':planes,'publishedComparison':published,'fieldPlaneExcludesReceiverCenterGate':True,'JIsMeasuredThrust':False,'newPhysicalMeasurements':0,'runtimeSeconds':time.perf_counter()-start}
    save(out/'result.json',result)
    total=sum(p.stat().st_size for p in out.iterdir() if p.is_file())
    assert gate and total<2*1024*1024 and result['runtimeSeconds']<30
    print(json.dumps({'numericalGatePass':gate,'calls':w['calls'],'untruncatedJOverWeight':ratio,'radialSquaredProfileRetention':q[-1]['retention'],'publishedRelativeDifference':published['relativeRatioDifference'],'resultBytes':total}))

if __name__=='__main__': main()
