"""Freeze observed image-coordinate evidence only. No model/ratio evaluation."""
from pathlib import Path
import csv,hashlib,json,math
P=Path(__file__).resolve().parent
OLD=P.parent/'research-velocity-ratio-screen'
CAP=1000000
manifest=json.loads((OLD/'evidence-freeze.json').read_text())
assert hashlib.sha256((OLD/'evidence-freeze.json').read_bytes()).hexdigest()=='fd0c462a38aa82589492472dc881ede6fe43bc1ff9f0eb34566af577922f70bd'
for name in ['figure-original.png','calibration.json','partial-measurements.json','read-1.json','read-2.json']:
    assert hashlib.sha256((OLD/name).read_bytes()).hexdigest()==manifest['files'][name]['sha256']
cal=json.loads((OLD/'calibration.json').read_text())
xv=cal['x_feasible_vertices'];yv=cal['y_feasible_vertices']
old=json.loads((OLD/'partial-measurements.json').read_text())['records']
r1=json.loads((P/'read-1-new.json').read_text())
r2=json.loads((P/'read-2-new.json').read_text())

def emit(name,obj):
    s=(json.dumps(obj,indent=2,allow_nan=False)+'\n').encode()
    total=sum(f.stat().st_size for base in (P,OLD) for f in base.rglob('*') if f.is_file())
    previous=(P/name).stat().st_size if (P/name).exists() else 0
    assert total-previous+len(s)<=CAP
    (P/name).write_bytes(s)

def bounds(p,h,verts):
    assert min(a for a,b in verts)*max(a for a,b in verts)>0
    vv=[(px-b)/a for px in (p-h,p+h) for a,b in verts]
    return [min(vv),max(vv)]

def memberships(zb):
    return [t for t in (11,14,17,20) if zb[1]>=t-.75 and zb[0]<=t+.75]

anchor=dict(next(r for r in old if r['target']==8));anchor.update({'id':'anchor246','role':'fixed certified pilot anchor','reused_without_rereading':True})
completed=dict(next(r for r in old if r['target']==11));completed.update({'id':'m310','reused_without_rereading':True,'x_bbox_inclusive':[308,312]})
records=[completed]
first={r['id']:r for r in r1['new_first_reads']}
first.update(r1['reused_first_reads'])
for read in r2['records']:
    id=read['id'];f=first[id];x0,y0,x1,y1=read['bbox_inclusive']
    px=(f['x']+read['center'][0])/2;py=(f['y']+read['center'][1])/2
    hx=max(2,(x1-x0+1)/2+1,abs(f['x']-read['center'][0]))
    hy=max(2,(y1-y0+1)/2+1,abs(f['y']-read['center'][1]))
    a,b=cal['x_center_coefficients'];c,d=cal['y_center_coefficients']
    records.append({'id':id,'kind':'digitized visual estimate, not raw data','series':'orange measured u_c/U_i','pixel_center':[px,py],'pixel_half_bounds':[hx,hy],'zeta':(px-b)/a,'zeta_bounds':bounds(px,hx,xv),'v':(py-d)/c,'v_bounds':bounds(py,hy,yv),'x_bbox_inclusive':[x0,x1],'overlap':read['overlap'],'reused_without_rereading':False})
records.sort(key=lambda r:r['pixel_center'][0])
for r in records:
    groups=memberships(r['zeta_bounds']);assert len(groups)==1,(r['id'],groups)
    t=groups[0];r['neighborhood']=t
    r['partial_eligibility']=not(t-.75<=r['zeta_bounds'][0] and r['zeta_bounds'][1]<=t+.75)
    assert r['v_bounds'][0]>=0
    assert r['zeta_bounds'][0]>=2.5*(2*math.sqrt(2))
assert len(records)+1<=15
assert anchor['v_bounds'][0]>0 and anchor['zeta_bounds'][0]>=2.5*(2*math.sqrt(2))
selection=[]
for span in r2['x_spans_for_selection']:
    matching=[r for r in records if r['x_bbox_inclusive']==span]
    if matching:
        rr=matching[0];selection.append({'x_span':span,'status':'included','id':rr['id'],'zeta_bounds':rr['zeta_bounds'],'neighborhood':rr['neighborhood'],'partial_eligibility':rr['partial_eligibility']})
    else:
        mid=(span[0]+span[1])/2;h=max(2,(span[1]-span[0]+1)/2+1)
        zb=bounds(mid,h,xv);assert not memberships(zb),(span,zb)
        selection.append({'x_span':span,'status':'excluded-outside-all-windows','zeta_bounds':zb,'ordinate_collected':False})
summary=[]
for t in (11,14,17,20):
    subset=[r for r in records if r['neighborhood']==t]
    assert subset
    summary.append({'target':t,'window':[t-.75,t+.75],'marker_ids':[r['id'] for r in subset],'partial_eligibility_ids':[r['id'] for r in subset if r['partial_eligibility']],'eligibility_not_guaranteed_by_marginal_bounds':not any(not r['partial_eligibility'] for r in subset),'source_truncated':t==20,'source_coverage_note':'Original plot stops at z/l=20; full [19.25,20.75] coverage is not claimed' if t==20 else 'Within plotted source bounds'})
emit('measurements.json',{'status':'frozen-observations-pending-independent-extraction-review','anchor':anchor,'responses':records,'calibration_reference':'../research-velocity-ratio-screen/calibration.json','calibration_sha256':manifest['files']['calibration.json']['sha256'],'experimental_uncertainty':'Unavailable; pixel bounds do not supply it','model_predictions_computed':False,'observed_ratios_computed':False})
emit('selection.json',{'new_observation_definition':'All observed centerline-marker intervals intersecting four windows; no nearestness test','scan_band':[275,170,506,244],'scan_scope_note':'Full original inspected. Earlier plotted markers are left of all four windows; far-field orange responses occupy the scanned band. No entirely hidden orange series identities observed. Purple rings and black fit overlap recorded, never substituted.','x_only_selection_bookkeeping':selection,'neighborhoods':summary,'total_unique_markers_including_anchor':len(records)+1,'model_calls':0})
fields=['id','neighborhood','zeta','zeta_low','zeta_high','v','v_low','v_high','partial_eligibility','kind']
with (P/'measurements.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
    for r in [anchor]+records:
        w.writerow({'id':r['id'],'neighborhood':r.get('neighborhood','anchor8'),'zeta':r['zeta'],'zeta_low':r['zeta_bounds'][0],'zeta_high':r['zeta_bounds'][1],'v':r['v'],'v_low':r['v_bounds'][0],'v_high':r['v_bounds'][1],'partial_eligibility':r.get('partial_eligibility',False),'kind':'digitized visual estimate, not raw data'})
assert sum(f.stat().st_size for base in (P,OLD) for f in base.rglob('*') if f.is_file())<=CAP
print(json.dumps({'unique_markers':len(records)+1,'neighborhoods':summary,'model_calls':0,'combined_retained_bytes':sum(f.stat().st_size for base in (P,OLD) for f in base.rglob('*') if f.is_file())},indent=2))
