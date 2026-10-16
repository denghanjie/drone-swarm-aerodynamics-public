"""Exposed GWS law-plus-bridge transfer. Per-row output must remain private."""
import argparse, hashlib, json, math, resource, signal, subprocess
from pathlib import Path

def digest(raw): return hashlib.sha256(raw).hexdigest()

def read_table(path,pin):
    raw=path.read_bytes()
    assert digest(raw)==pin['sha256'], 'Input hash mismatch'
    lines=[s.split() for s in raw.decode('utf-8-sig').splitlines() if s.strip()]
    assert lines[0]==pin['header'] and len(lines)-1==pin['rows']
    values=[list(map(float,s)) for s in lines[1:]]
    assert all(len(s)==len(lines[0]) and all(math.isfinite(x) for x in s) for s in values)
    return [dict(zip(lines[0],s),row_id=i+1) for i,s in enumerate(values)]

def anchors(rows,n):
    assert all(s['RPM']!=n for s in rows)
    low=max((s for s in rows if s['RPM']<n),key=lambda s:s['RPM'])
    high=min((s for s in rows if s['RPM']>n),key=lambda s:s['RPM'])
    assert sum(s['RPM']==low['RPM'] for s in rows)==sum(s['RPM']==high['RPM'] for s in rows)==1
    coefficient=low['CT']+(n-low['RPM'])/(high['RPM']-low['RPM'])*(high['CT']-low['CT'])
    return low,high,coefficient

def root(alpha):
    assert math.isfinite(alpha) and alpha>=0
    if alpha==0: return {'x':1.,'lo':1.,'hi':1.,'iterations':0,'residual':0.}
    lo,hi=0.,1.
    for iterations in range(1,97):
        mid=(lo+hi)/2
        if mid**3+alpha*mid-1>0: hi=mid
        else: lo=mid
        if hi-lo<=2e-15: break
    x=(lo+hi)/2;residual=x**3+alpha*x-1
    assert lo**3+alpha*lo-1<=1e-14 and hi**3+alpha*hi-1>=-1e-14
    assert 0<x<=1 and hi-lo<=2e-15 and abs(residual)<=1e-12
    return {'x':x,'lo':lo,'hi':hi,'iterations':iterations,'residual':residual}

def metrics(rows,c0):
    assert rows and c0>0
    residuals=[r['residual_CT_prediction_minus_reported'] for r in rows]
    maximum=max(map(abs,residuals));rms=math.sqrt(math.fsum(x*x for x in residuals)/len(rows))
    return {'count':len(rows),'row_ids':[r['row_id'] for r in rows],
            'max_absolute_CT_discrepancy':maximum,'maximizing_row_ids':[r['row_id'] for r in rows if abs(r['residual_CT_prediction_minus_reported'])==maximum],
            'rms_CT_discrepancy':rms,'max_absolute_divided_by_C0':maximum/c0,'rms_divided_by_C0':rms/c0,
            'signed_mean_CT_discrepancy':math.fsum(residuals)/len(rows)}

def tests():
    assert root(0)['x']==1
    for x in [.2,.5,.8]:
        alpha=(1-x**3)/x
        assert abs(root(alpha)['x']-x)<2e-15
    low,high,value=anchors([{'RPM':3,'CT':6},{'RPM':1,'CT':2},{'RPM':4,'CT':8}],2)
    assert low['RPM']==1 and high['RPM']==3 and value==4
    r=metrics([{'row_id':1,'residual_CT_prediction_minus_reported':2},{'row_id':2,'residual_CT_prediction_minus_reported':-2}],4)
    assert r['max_absolute_CT_discrepancy']==2 and r['rms_CT_discrepancy']==2 and r['signed_mean_CT_discrepancy']==0
    return {'passed':True,'checks':6,'scope':'Synthetic roots, unsorted baseline interpolation and residual statistics only'}

def execute(config,static_path,axial_path,public_path,private_path):
    assert not public_path.exists() and not private_path.exists(), 'Refuse output overwrite'
    repo=Path(__file__).resolve().parents[2]
    assert not private_path.resolve().is_relative_to(repo), 'Private row evidence must be outside the public checkout'
    source_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo,text=True).strip()
    assert len(source_commit)==40 and all(c in '0123456789abcdef' for c in source_commit)
    committed=subprocess.check_output(['git','show',source_commit+':'+str(Path(__file__).resolve().relative_to(repo))],cwd=repo)
    assert committed==Path(__file__).read_bytes(), 'Analyzer must match its source commit before scoring'
    static=read_table(static_path,config['static']);axial=read_table(axial_path,config['axial'])
    assert all(s['J']>=0 for s in axial)
    low,high,linear=anchors(static,config['nominal_run_rpm'])
    assert (low['row_id'],low['RPM'],low['CT'])==(13,15006.667,.061549)
    assert (high['row_id'],high['RPM'],high['CT'])==(14,15960.,.062855)
    values=[linear,low['CT'],high['CT']];all_rows=[];summaries=[]
    for name,c0 in zip(config['scenarios'],values):
        assert c0>0
        rows=[]
        for observed in axial:
            alpha=observed['J']*math.sqrt(math.pi/(2*c0));answer=root(alpha);prediction=c0*answer['x']
            rows.append({'row_id':observed['row_id'],'J':observed['J'],'reported_CT':observed['CT'],
                'alpha':alpha,'root':answer,'predicted_CT':prediction,'residual_CT_prediction_minus_reported':prediction-observed['CT'],
                'reported_positive_thrust':observed['CT']>0})
        all_rows.append({'scenario':name,'C0':c0,'rows':rows})
        positive=[r for r in rows if r['reported_positive_thrust']]
        summaries.append({'scenario':name,'C0':c0,'full_run':metrics(rows,c0),'reported_positive_thrust_subset':metrics(positive,c0) if positive else None,
            'nonpositive_row_ids':[r['row_id'] for r in rows if not r['reported_positive_thrust']],
            'max_absolute_cubic_residual':max(abs(r['root']['residual']) for r in rows),
            'max_bracket_width':max(r['root']['hi']-r['root']['lo'] for r in rows),
            'bisection_iterations':sum(r['root']['iterations'] for r in rows)})
    private={'kind':'private-complete-GWS-derived-rows','source_commit':source_commit,'input_hashes':{k:config[k]['sha256'] for k in ['static','axial']},'scenarios':all_rows}
    private_bytes=(json.dumps(private,indent=2,allow_nan=False)+'\n').encode()
    assert len(private_bytes)<256*1024
    with private_path.open('xb') as f:f.write(private_bytes)
    public={'kind':'exposed-GWS-aggregate-transfer','source_commit':source_commit,'analysis_sha256':digest(Path(__file__).read_bytes()),
        'private_row_evidence_sha256':digest(private_bytes),'private_row_evidence_bytes':len(private_bytes),
        'input_hashes':private['input_hashes'],'rows_per_scenario':len(axial),'root_count':len(axial)*len(summaries),
        'baseline_anchors':[{k:row[k] for k in ['row_id','RPM','CT']} for row in [low,high]],'scenarios':summaries,
        'physical_adequacy_threshold':None,'experimental_confidence_interval':None,
        'scope':'Nominal prescribed-RPM coefficient transfer of ideal-disk equation plus explicit f0=T0(run-label) bridge; exposed data, no direct M28 qualification.'}
    with public_path.open('x') as f:json.dump(public,f,indent=2,allow_nan=False);f.write('\n')

if __name__=='__main__':
    resource.setrlimit(resource.RLIMIT_CPU,(15,15))
    signal.alarm(15)
    p=argparse.ArgumentParser();p.add_argument('--test',action='store_true');p.add_argument('--config',type=Path);p.add_argument('--static',type=Path);p.add_argument('--axial',type=Path);p.add_argument('--public-output',type=Path);p.add_argument('--private-output',type=Path);a=p.parse_args()
    if a.test: print(json.dumps(tests(),indent=2))
    else: execute(json.loads(a.config.read_text()),a.static,a.axial,a.public_output,a.private_output)
