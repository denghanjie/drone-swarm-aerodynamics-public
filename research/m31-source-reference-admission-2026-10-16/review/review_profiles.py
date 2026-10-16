"""Independent saved-result review from admitted pypdf coordinates.

Arguments: repository root, independent VISIBLE-PROFILES.json.
No original analysis function or extractor is imported or executed.
"""
import bisect
import hashlib
import json
import math
import resource
import subprocess
import sys
import time
from pathlib import Path

resource.setrlimit(resource.RLIMIT_CPU,(30,30))
REPO=Path(sys.argv[1])
OWN_INPUT=Path(sys.argv[2])
HERE=Path(__file__).resolve().parent
PACKAGE='research/m31-source-reference-admission-2026-10-16'
BASE=REPO/PACKAGE
COMMIT='37750e0ea4d929ac7bb414a7636cfebaea3f3c2a'
MANIFEST_HASH='d6b3b245699eab623251d11c20377e9b4ff10865c54ebac3a6dc6c40ee9d521d'
OWN_HASH='fc9a0bc90dd50912dc95d7a96f5c39ee1089e2ea294164db86656c3b6e0ad09d'
PDF_HASH='81987dfd1cf2980270defd9447a9e5fb6c1586eab77b75b730de127c932d373c'
started=time.process_time()
checks=[]
report={'kind':'independent-exposed-profile-saved-result-review','sourceCommit':COMMIT,'checks':checks,
        'rootAnalysisImports':0,'rootAnalyzerReruns':0,'newPhysicalData':0,'privateOffAxisPathsRead':False,
        'confidenceIntervalsComputed':False,'physicalRejectionClaim':False,'noveltyClaim':False}

def sha(data): return hashlib.sha256(data).hexdigest()
def check(name,passed,detail=None):
    row={'name':name,'pass':bool(passed)}
    if detail is not None: row['detail']=detail
    checks.append(row)
def near(a,b,tolerance=1e-10): return math.isfinite(a) and math.isfinite(b) and abs(a-b)<=tolerance
def interpolate(curve,x):
    xs=[p[0] for p in curve]
    if x<xs[0]-1e-12 or x>xs[-1]+1e-12: raise ValueError('Interpolation outside admitted support')
    index=max(0,min(len(curve)-2,bisect.bisect_right(xs,x)-1))
    x0,y0=curve[index]; x1,y1=curve[index+1]
    return y0+(x-x0)*(y1-y0)/(x1-x0)

def crossings(curve):
    threshold=curve[0][1]/2
    roots=[]; plateaus=[]
    for index,((x0,y0),(x1,y1)) in enumerate(zip(curve,curve[1:])):
        d0=y0-threshold; d1=y1-threshold
        if d0==0 and d1==0:
            plateaus.append([x0,x1])
        elif d0*d1<0:
            roots.append({'radius':x0+(threshold-y0)*(x1-x0)/(y1-y0),
                          'direction':'downward' if d0>0 and d1<0 else 'upward',
                          'bracketIndices':[index,index+1],
                          'bracketRadii':[x0,x1],'endpointResiduals':[d0,d1]})
    for index,(x,y) in enumerate(curve):
        if y!=threshold: continue
        if any(lo<=x<=hi for lo,hi in plateaus): continue
        left=curve[index-1][1]-threshold if index else None
        right=curve[index+1][1]-threshold if index+1<len(curve) else None
        if left is None or right is None: direction='boundary'
        elif left>0 and right<0: direction='downward'
        elif left<0 and right>0: direction='upward'
        else: direction='tangential'
        roots.append({'radius':x,'direction':direction,'exactVertexIndex':index})
    roots.sort(key=lambda row:row['radius'])
    unique=len(roots)==1 and not plateaus
    return {'threshold':threshold,'roots':roots,'plateauIntervals':plateaus,
            'uniqueIntersection':unique,'uniqueDownwardCrossing':unique and roots[0]['direction']=='downward'}

def main():
    plan=(HERE/'REVIEW-PLAN.json').read_bytes()
    report['reviewPlanSHA256']=sha(plan)
    source_manifest=(BASE/'source-manifest.json').read_bytes()
    manifest=json.loads(source_manifest)
    check('manifest_hash_matches_published_checkpoint',sha(source_manifest)==MANIFEST_HASH)
    requests=[PACKAGE+'/source-manifest.json']+[PACKAGE+'/'+p['path'] for p in manifest['files']]
    raw=subprocess.run(['git','cat-file','--batch'],cwd=str(REPO),
                       input=''.join(COMMIT+':'+p+'\n' for p in requests).encode(),
                       stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=5)
    cursor=0; blobs={}
    for name in requests:
        stop=raw.stdout.index(b'\n',cursor)
        header=raw.stdout[cursor:stop].split(); cursor=stop+1
        if len(header)!=3 or header[1]!=b'blob': raise ValueError('Missing expected committed blob')
        size=int(header[2]); blobs[name]=raw.stdout[cursor:cursor+size]; cursor+=size+1
    check('published_manifest_blob_matches',raw.returncode==0 and blobs[requests[0]]==source_manifest)
    pin_checks=[]
    for pin in manifest['files']:
        value=blobs[PACKAGE+'/'+pin['path']]
        pin_checks.append({'path':pin['path'],'bytes':len(value),'sha256':sha(value),
                           'pass':len(value)==pin['bytes'] and sha(value)==pin['sha256']})
    check('all_committed_source_pins_match',all(x['pass'] for x in pin_checks) and len(pin_checks)==manifest['count'],pin_checks)
    for name in ['PROFILE-PROTOCOL.md','analyze_profiles.py','visible-profiles.json','independent/VISIBLE-PROFILES.json']:
        check('current_required_file_matches_source_commit_'+name,(BASE/name).read_bytes()==blobs[PACKAGE+'/'+name])
    own_bytes=OWN_INPUT.read_bytes()
    check('independent_pypdf_input_pin',sha(own_bytes)==OWN_HASH and own_bytes==blobs[PACKAGE+'/independent/VISIBLE-PROFILES.json'])
    own=json.loads(own_bytes)
    author_input_bytes=(BASE/'visible-profiles.json').read_bytes()
    author_input=json.loads(author_input_bytes)
    result_bytes=(BASE/'results/result.json').read_bytes()
    saved=json.loads(result_bytes)
    execution_bytes=(BASE/'results/execution.json').read_bytes()
    report['inputPins']={'sourceManifestSHA256':sha(source_manifest),'independentPypdfSHA256':sha(own_bytes),
                         'authorVisibleInputSHA256':sha(author_input_bytes),'savedResultSHA256':sha(result_bytes),
                         'savedExecutionSHA256':sha(execution_bytes),'analysisSourceSHA256':sha(blobs[PACKAGE+'/analyze_profiles.py'])}
    report['savedExecutionReceipt']=json.loads(execution_bytes)
    check('saved_execution_source_commit',report['savedExecutionReceipt']['source_commit']==COMMIT)
    check('result_provenance_fields',saved['source_commit']==COMMIT and saved['input_sha256']==sha(author_input_bytes) and saved['analysis_source_sha256']==sha(blobs[PACKAGE+'/analyze_profiles.py']))
    check('source_identity_and_visible_scope',own['sourcePDFSHA256']==PDF_HASH and own['page']==5 and own['figure']==7 and own['normalizedDownstreamStation']==3 and author_input['source_sha256']==PDF_HASH and author_input['page']==5 and author_input['figure']==7)

    names=['Offboard 1','Offboard 2']; colors=[[.85,.325,.098],[.929,.694,.125]]
    check('profile_attribution',[s['series'] for s in own['series']]==names and [s['name'] for s in author_input['profiles']]==names and all(s['pathMetadata']['strokeColor']==c for s,c in zip(own['series'],colors)))
    curves=[]; extraction_deltas=[]
    for index,series in enumerate(own['series']):
        original=series['visibleOriginalVertices']; endpoint=series['clippedDisplayEndpoint']
        check('visible_and_clipped_semantics_'+names[index],len(original)==16 and all(v['insideDisplayedAxes'] for v in original) and not endpoint['isOriginalVertex'] and not endpoint['isAdditionalMeasurement'] and endpoint['type']=='display_interpolation_at_clip_boundary')
        curve=[(v['normalizedRadius'],v['normalizedSpeed']) for v in original]
        curve.append((endpoint['normalizedRadius'],endpoint['normalizedSpeed']))
        check('finite_shared_support_'+names[index],all(math.isfinite(z) for p in curve for z in p) and curve[0][0]==0 and curve[-1][0]==3 and all(a[0]<b[0] for a,b in zip(curve,curve[1:])) and curve[0][1]>0)
        curves.append(curve)
        root_knots=author_input['profiles'][index]['knots']
        delta=max(max(abs(x-k['r_over_l']),abs(y-k['speed_over_UH'])) for (x,y),k in zip(curve,root_knots))
        extraction_deltas.append({'series':names[index],'maxCoordinateDifference':delta})
        check('independent_extraction_reconciliation_'+names[index],len(root_knots)==17 and delta<=1e-6)
    union=sorted(set(x for curve in curves for x,y in curve))
    check('union_size_and_support',len(union)==17 and union[0]==0 and union[-1]==3)
    own_knots=[{'r_over_l':x,'g1':interpolate(curves[0],x),'g2':interpolate(curves[1],x)} for x in union]
    for row in own_knots: row['difference_g2_minus_g1']=row['g2']-row['g1']
    saved_knots=saved['union_knot_records']
    check('saved_union_knot_count',len(saved_knots)==len(union))
    knot_checks=[]
    for index,(x,row) in enumerate(zip(union,saved_knots)):
        values={'r_over_l':x,'g1':interpolate(curves[0],row['r_over_l']),
                'g2':interpolate(curves[1],row['r_over_l'])}
        values['difference_g2_minus_g1']=values['g2']-values['g1']
        deltas={key:row[key]-value for key,value in values.items()}
        knot_checks.append({'index':index,'savedRadius':row['r_over_l'],'independentAtSavedRadius':values,
                            'savedMinusIndependent':deltas,'pass':all(abs(v)<=1e-10 for v in deltas.values())})
    check('all_saved_union_values_and_signs',all(x['pass'] for x in knot_checks))
    maximum=max(abs(row['difference_g2_minus_g1']) for row in own_knots)
    maximizing=[row['r_over_l'] for row in own_knots if abs(row['difference_g2_minus_g1'])==maximum]
    check('maximum_absolute_discrepancy',near(saved['max_absolute_normalized_discrepancy'],maximum))
    check('all_maximizing_knots',len(saved['maximizing_radii'])==len(maximizing) and all(near(a,b) for a,b in zip(saved['maximizing_radii'],maximizing)))
    report['unionKnotReview']=knot_checks
    report['independentUnionKnots']=own_knots
    report['extractionReconciliation']=extraction_deltas

    quadratures=[]
    rules=[('two_point',[(-1/math.sqrt(3),1),(1/math.sqrt(3),1)]),
           ('three_point',[(-math.sqrt(3/5),5/9),(0,8/9),(math.sqrt(3/5),5/9)])]
    for name,rule in rules:
        segments=[]
        for low,high in zip(union,union[1:]):
            center=(low+high)/2; half=(high-low)/2
            numer=[]; denom=[]
            for node,weight in rule:
                x=center+half*node
                g1=interpolate(curves[0],x); g2=interpolate(curves[1],x)
                numer.append(half*weight*x*(g2-g1)**2)
                denom.append(half*weight*x*g2*g2)
            segments.append({'interval':[low,high],'differenceIntegral':math.fsum(numer),'offboard2ReferenceIntegral':math.fsum(denom)})
        num=math.fsum(x['differenceIntegral'] for x in segments)
        den=math.fsum(x['offboard2ReferenceIntegral'] for x in segments)
        if den<=0: raise ValueError('Nonpositive reference denominator')
        quadratures.append({'rule':name,'nodesPerInterval':len(rule),'intervalCount':len(segments),
                            'abscissaEvaluations':len(rule)*len(segments),'segments':segments,
                            'differenceIntegral':num,'offboard2ReferenceIntegral':den,'relativeL2':math.sqrt(num/den)})
    q2,q3=quadratures
    check('two_and_three_point_gauss_agree',all(near(q2[key],q3[key],1e-12) for key in ['differenceIntegral','offboard2ReferenceIntegral','relativeL2']))
    check('saved_squared_difference_integral',near(saved['weighted_squared_difference_integral'],q3['differenceIntegral']))
    check('saved_offboard2_reference_integral',near(saved['weighted_squared_reference_integral'],q3['offboard2ReferenceIntegral']))
    check('saved_asymmetric_radially_weighted_relative_L2',near(saved['radially_weighted_relative_L2_using_offboard2_reference'],q3['relativeL2']))
    report['independentQuadrature']=quadratures

    crossing_records=[]
    for index,curve in enumerate(curves):
        fresh=crossings(curve); old=saved['half_centerline_crossings'][index]
        check('centerline_'+names[index],near(saved['centerline_values'][index],curve[0][1]))
        check('half_centerline_threshold_'+names[index],near(old['threshold'],fresh['threshold']))
        check('all_crossing_radii_'+names[index],len(old['radii'])==len(fresh['roots']) and all(near(x,y['radius']) for x,y in zip(old['radii'],fresh['roots'])))
        check('crossing_direction_and_uniqueness_'+names[index],old['directions']==[r['direction'] for r in fresh['roots']] and old['plateau_intervals']==fresh['plateauIntervals'] and old['unique_intersection']==fresh['uniqueIntersection'] and old['unique_downward_crossing']==fresh['uniqueDownwardCrossing'])
        crossing_records.append({'series':names[index],**fresh})
    report['independentHalfCenterlineCrossings']=crossing_records
    report['independentSummary']={'maximumAbsoluteNormalizedDiscrepancy':maximum,'maximizingRadii':maximizing,
                                   'radiallyWeightedRelativeL2Offboard2Reference':q3['relativeL2'],
                                   'weightedSquaredDifferenceIntegral':q3['differenceIntegral'],
                                   'weightedSquaredReferenceIntegral':q3['offboard2ReferenceIntegral'],
                                   'centerlineValues':[c[0][1] for c in curves]}
    check('descriptive_result_and_no_inference',saved['kind']=='exposed-published-profile-descriptive-audit' and saved['experimental_confidence_interval'] is None and saved['physical_pass_threshold'] is None)
    check('graphical_width_only',near(saved['graphical_stroke_half_width_normalized_x'],.79701/2*3/198.42685) and near(saved['graphical_stroke_half_width_normalized_y'],.79701/2*1.5/99.21342))

try:
    main()
except Exception as error:
    report['exceptionType']=type(error).__name__
    check('completed_without_exception',False)
report['cpuSecondsForAllocationOnly']=time.process_time()-started
check('review_cpu_under_thirty_seconds',report['cpuSecondsForAllocationOnly']<30)
report['allChecksPass']=all(x['pass'] for x in checks)
report['checkCount']=len(checks)
report['limits']=['Descriptive exposed median polylines only; graphical vertices are not raw independent observations.',
                  'Graphical extraction and arithmetic agreement do not establish physical equivalence, rejection or transfer validation.',
                  'No confidence intervals, significance, causal attribution or novelty claim.',
                  'Weighted relative L2 is asymmetric with Offboard 2 as reference; it is not thrust error or a momentum balance.',
                  'Clipped endpoints remain display interpolations; no off-axis extrapolation was used.']
data=(json.dumps(report,indent=2,sort_keys=True,allow_nan=False)+'\n').encode()
if len(data)>=2*1024*1024: raise ValueError('Review output cap exceeded')
with (HERE/'RAW-CHECKS.json').open('xb') as stream: stream.write(data)
print(json.dumps({'allChecksPass':report['allChecksPass'],'checkCount':len(checks),'outputBytes':len(data),
                  'rootAnalyzerReruns':0,'quadratureAbscissae':80,'cpuSecondsForAllocationOnly':report['cpuSecondsForAllocationOnly']}))
raise SystemExit(0 if report['allChecksPass'] else 1)
