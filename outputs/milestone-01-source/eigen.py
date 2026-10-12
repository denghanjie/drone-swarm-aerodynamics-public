"""macOS Accelerate LAPACK eigenvalues; standard-library Python, no package install."""
import ctypes as C, json
from pathlib import Path
lib=C.CDLL('/System/Library/Frameworks/Accelerate.framework/Accelerate')
def eigen(a):
    n=len(a); N=C.c_int(n); lda=C.c_int(n); one=C.c_int(1); lwork=C.c_int(8*n); info=C.c_int()
    arr=(C.c_double*(n*n))(*(a[i][j] for j in range(n) for i in range(n)))
    wr=(C.c_double*n)();wi=(C.c_double*n)();dummy=(C.c_double*1)();work=(C.c_double*(8*n))()
    lib.dgeev_(C.c_char_p(b'N'),C.c_char_p(b'N'),C.byref(N),arr,C.byref(lda),wr,wi,dummy,C.byref(one),dummy,C.byref(one),work,C.byref(lwork),C.byref(info))
    if info.value: raise RuntimeError(info.value)
    return sorted([{'real':r,'imag':i,'magnitude':(r*r+i*i)**.5} for r,i in zip(wr,wi)],key=lambda v:-v['magnitude'])
root=Path(__file__).resolve().parent.parent
rows=json.loads((root/'milestone-01-diagnostic-matrices.json').read_text())
for r in rows:
    if 'matrix' not in r: continue
    r['eigenvalues']=eigen(r.pop('matrix'));r['radius']=r['eigenvalues'][0]['magnitude']
(root/'milestone-01-diagnostics.json').write_text(json.dumps(rows,indent=2))
for name in ['original','selected']:
    for tau in [.01,.02,.04,.08]:
        rr=[r for r in rows if r['name']==name and r['motorTau']==tau and 'radius' in r]
        unstable=[r['momentScale'] for r in rr if r['radius']>1]
        print(name,tau,'first unstable',min(unstable) if unstable else None,'full',rr[-1]['radius'],'max residual',max(r['residual'] for r in rr))
