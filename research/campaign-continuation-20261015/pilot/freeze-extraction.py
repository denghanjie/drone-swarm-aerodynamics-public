"""Reproduce frozen image-calibration bounds and the selection stop.
No figure download, new marker reading, wake import, model prediction or ratio.
"""
from pathlib import Path
import csv,hashlib,itertools,json,math
P=Path(__file__).resolve().parent
CAP=1000000

def emit(name,value):
    data=(json.dumps(value,indent=2,allow_nan=False)+'\n').encode()
    total=sum(f.stat().st_size for f in P.rglob('*') if f.is_file())
    old=(P/name).stat().st_size if (P/name).exists() else 0
    assert total-old+len(data)<=CAP
    (P/name).write_bytes(data)

def affine_vertices(ticks):
    # p = a*value+b, each frozen tick supplies p-h <= a*value+b <= p+h.
    lines=[(v,p+d) for v,p,h in ticks for d in (-h,h)]
    out=[]
    for (v1,p1),(v2,p2) in itertools.combinations(lines,2):
        if v1==v2: continue
        a=(p2-p1)/(v2-v1);b=p1-a*v1
        if all(abs(a*v+b-p)<=h+1e-9 for v,p,h in ticks):
            if not any(abs(a-c)<1e-9 and abs(b-d)<1e-9 for c,d in out): out.append((a,b))
    assert out
    return out

def value_bounds(p,h,verts):
    # Affine denominator has constant nonzero sign; fractional-linear extrema
    # over this convex calibration polygon occur at vertices.
    assert min(a for a,b in verts)*max(a for a,b in verts)>0
    values=[(x-b)/a for x in (p-h,p+h) for a,b in verts]
    return [min(values),max(values)]

def distance_bounds(bounds,target):
    lo,hi=bounds
    return [0 if lo<=target<=hi else min(abs(lo-target),abs(hi-target)),max(abs(lo-target),abs(hi-target))]

cal={'coordinate_system':'Original 560x420 raster; origin top-left, x rightward, y downward; integer pixel centers','axes':'Both linear; x=z/l, y=u_c/U_i','method':'Read 1 visual; read 2 tick-line inspection on nearest-neighbor enlarged original. Repeated reads share the same raster and are not independent experiments.','x_pairs':[[0,20],[5,20]],'y_pairs':[[0,1],[0.2,0.8]],'tick_read_1':{'x':[[0,77],[5,184],[20,506]],'y':[[0,347],[0.2,284],[0.8,94],[1,31]]},'tick_read_2':{'x':[[0,77],[5,184],[20,506]],'y':[[0,347],[0.2,284],[0.8,94],[1,31]]},'visible_tick_extent_pixels':1,'tick_half_bound_pixels':2,'calibration_model':'Shared affine map constrained by every tick interval, using joint feasible polygon vertices. Two-pair central coefficients are averaged.','x_center_coefficients':[ (21.45+322/15)/2, (77+(184-5*(322/15)))/2 ],'y_center_coefficients':[(-316-190/.6)/2,(347+(284+.2*(190/.6)))/2]}
xt=[(0,77,2),(5,184,2),(20,506,2)]
yt=[(0,347,2),(.2,284,2),(.8,94,2),(1,31,2)]
xv=affine_vertices(xt);yv=affine_vertices(yt)
cal['x_feasible_vertices']=xv;cal['y_feasible_vertices']=yv
emit('calibration.json',cal)
read2={'method':'Orange centerline-series pixels only, identified from full legend; no maximum-series substitution. Second-read centers are visible-orange bounding-box midpoints.','orange_threshold':'R>=230, 100<=G<=190, 60<=B<=160, R-G>=50','selected_windows_native_pixels':[[241,170,251,240],[305,170,316,240]],'records':[{'target':8,'bbox_inclusive':[244,182,248,185],'orange_pixel_count':16,'center':[246,183.5]},{'target':11,'bbox_inclusive':[308,186,312,189],'orange_pixel_count':14,'center':[310,187.5]}],'extent_convention':'Inclusive bbox extent=max-min+1','stopped':'No second read of targets 14,17,20 after target 11 fails nearestness gate. Their first-read values remain provisional only.'}
emit('read-2.json',read2)
first=json.loads((P/'read-1.json').read_text())
rows=[];decisions=[]
neighbor_data={8:[(230.5,3,[229,232]),(262,3.5,[260,264])],11:[(294,3.5,[292,296]),(326,3.5,[324,328])]}
for r in read2['records']:
    t=r['target'];r1=next(v for v in first['selected_visual_reads'] if v['target']==t)
    px=(r1['x']+r['center'][0])/2;py=(r1['y']+r['center'][1])/2
    bx0,by0,bx1,by1=r['bbox_inclusive']
    hx=max(2,(bx1-bx0+1)/2+1,abs(r1['x']-r['center'][0]))
    hy=max(2,(by1-by0+1)/2+1,abs(r1['y']-r['center'][1]))
    zb=value_bounds(px,hx,xv);vb=value_bounds(py,hy,yv)
    xa,xb=cal['x_center_coefficients'];ya,yb=cal['y_center_coefficients']
    row={'target':t,'series':'u_c/U_i orange filled circles','kind':'digitized visual estimate, not raw data','pixel_center':[px,py],'pixel_half_bounds':[hx,hy],'zeta':(px-xb)/xa,'zeta_bounds':zb,'v':(py-yb)/ya,'v_bounds':vb}
    rows.append(row);dd=distance_bounds(zb,t)
    neighbors=[]
    for nx,nh,bbox in neighbor_data[t]:
        nb=value_bounds(nx,nh,xv)
        neighbors.append({'x_bbox_inclusive':bbox,'pixel_center':nx,'pixel_half_bound':nh,'zeta_bounds':nb,'distance_bounds':distance_bounds(nb,t),'response_ordinate_collected':False})
    dec={'target':t,'selected_distance_bounds':dd,'neighbor_x_only_witnesses':neighbors,'within_075_window':dd[1]<=.75,'strict_nearestness':all(dd[1]<n['distance_bounds'][0] for n in neighbors),'exact_farfield_floor':zb[0]>=2.5*(2*math.sqrt(2)),'nonnegative_v_lower':vb[0]>=0,'anchor_positive_v_lower':vb[0]>0 if t==8 else None}
    decisions.append(dec)
    if not dec['strict_nearestness']: break
assert decisions[0]['strict_nearestness'] and not decisions[1]['strict_nearestness']
emit('partial-measurements.json',{'status':'incomplete; not eligible for model evaluation','records':rows,'uncompleted_targets':[14,17,20],'provisional_first_reads_retained':'read-1.json','observed_ratios_computed':False})
emit('selection-stop.json',{'status':'stopped-at-predeclared-selection-gate','failed_target':11,'failed_rule':'winner distance upper bound must be strictly less than each competitor distance lower bound','decisions':decisions,'collection_passes':1,'model_calls':0,'observed_ratios_computed':False,'physical_inference':'None. Failure is a conservative extraction/selection certificate, not evidence against the wake model.'})
print(json.dumps({'decisions':decisions,'campaign_bytes_before_final_receipt':sum(f.stat().st_size for f in P.rglob('*') if f.is_file())},indent=2))
