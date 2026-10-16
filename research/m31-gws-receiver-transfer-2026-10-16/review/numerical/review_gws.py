"""Prepared independent GWS review. Execute only after source/result handoff.

All input paths are caller arguments. Public output contains no per-row numeric
table and no private filesystem paths. Original analyzer functions are not used.
"""
import argparse
import bisect
import hashlib
import json
import math
import re
import resource
import subprocess
import time
from decimal import Decimal, localcontext
from pathlib import Path

PACKAGE='research/m31-gws-receiver-transfer-2026-10-16'
SCENARIOS=['linear-static-baseline','lower-rpm-anchor','higher-rpm-anchor']
TOL={'baseline':1e-14,'alpha':1e-12,'root':2e-12,'CT':1e-12,'normalized':1e-10,'cubic':1e-12}

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def committed_blobs(repo,commit,names):
    command=subprocess.run(['git','cat-file','--batch'],cwd=str(repo),
                           input=''.join(commit+':'+PACKAGE+'/'+name+'\n' for name in names).encode(),
                           stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=3)
    if command.returncode:
        raise ValueError('Frozen source objects unavailable')
    cursor=0; frozen={}
    for name in names:
        end=command.stdout.index(b'\n',cursor)
        header=command.stdout[cursor:end].split(); cursor=end+1
        if len(header)!=3 or header[1]!=b'blob':
            raise ValueError('Frozen source object is not a blob')
        size=int(header[2]); frozen[name]=command.stdout[cursor:cursor+size]; cursor+=size+1
    return frozen

def read_decimal_table(raw,pin):
    if sha(raw)!=pin['sha256']:
        raise ValueError('Pinned input hash mismatch')
    lines=[line.split() for line in raw.decode('utf-8-sig').splitlines() if line.strip()]
    if lines[0]!=pin['header'] or len(lines)-1!=pin['rows']:
        raise ValueError('Pinned input shape mismatch')
    records=[]
    for index,fields in enumerate(lines[1:],1):
        if len(fields)!=len(lines[0]):
            raise ValueError('Input field count mismatch')
        numbers=[Decimal(field) for field in fields]
        if not all(value.is_finite() for value in numbers):
            raise ValueError('Nonfinite source operand')
        record={'row_id':index}
        record.update(zip(lines[0],numbers))
        records.append(record)
    return records

def positive_cubic_hyperbolic(alpha):
    if not math.isfinite(alpha) or alpha<0:
        raise ValueError('Invalid independent cubic input')
    if alpha==0:
        return 1.0
    # q=3 sqrt(3)/(2 alpha^(3/2)); form log(q) without overflowing q.
    log_q=math.log(1.5*math.sqrt(3))-1.5*math.log(alpha)
    if log_q<=0:
        q=math.exp(log_q)
        if q==0:
            return 1/alpha
        value=math.asinh(q)
        theta=value/3
        sinh_ratio=math.sinh(theta)/theta if theta else 1.0
        return (value/q)*sinh_ratio/alpha
    value=log_q+math.log1p(math.sqrt(1+math.exp(-2*log_q)))
    return 2*(math.sqrt(alpha)/math.sqrt(3))*math.sinh(value/3)

def independent_metrics(records,c0):
    if not records:
        return None
    with localcontext() as ctx:
        ctx.prec=70
        errors=[Decimal.from_float(row['prediction'])-row['reported_CT_decimal'] for row in records]
        maximum=max(abs(e) for e in errors)
        rms=(sum((e*e for e in errors),Decimal(0))/len(errors)).sqrt()
        signed=sum(errors,Decimal(0))/len(errors)
        return {'count':len(records),'row_ids':[row['row_id'] for row in records],
                'max_absolute_CT_discrepancy':float(maximum),
                'maximizing_row_ids':[row['row_id'] for row,e in zip(records,errors) if abs(e)==maximum],
                'rms_CT_discrepancy':float(rms),'max_absolute_divided_by_C0':float(maximum/c0),
                'rms_divided_by_C0':float(rms/c0),'signed_mean_CT_discrepancy':float(signed)}

def compare_metrics(expected,saved):
    if expected is None or saved is None:
        return {'pass':expected is None and saved is None,'maximumCTMetricDelta':0.0,'maximumNormalizedMetricDelta':0.0}
    discrete=['count','row_ids','maximizing_row_ids']
    raw=['max_absolute_CT_discrepancy','rms_CT_discrepancy','signed_mean_CT_discrepancy']
    normalized=['max_absolute_divided_by_C0','rms_divided_by_C0']
    d_raw=max(abs(expected[key]-saved[key]) for key in raw)
    d_norm=max(abs(expected[key]-saved[key]) for key in normalized)
    return {'pass':all(expected[key]==saved[key] for key in discrete) and d_raw<=TOL['CT'] and d_norm<=TOL['normalized'],
            'maximumCTMetricDelta':d_raw,'maximumNormalizedMetricDelta':d_norm}

def run(args,report):
    def check(name,ok,detail=None):
        row={'name':name,'pass':bool(ok)}
        if detail is not None:
            row['detail']=detail
        report['checks'].append(row)
    if not re.fullmatch('[0-9a-f]{40}',args.source_commit):
        raise ValueError('Published immutable source commit is required')
    manifest_bytes=committed_blobs(args.repo,args.source_commit,['source-manifest.json'])['source-manifest.json']
    check('frozen_manifest_matches_handoff_pin',sha(manifest_bytes)==args.expected_manifest_sha256)
    if not report['checks'][-1]['pass']:
        raise ValueError('Source manifest admission failed')
    manifest=json.loads(manifest_bytes)
    names=[entry['path'] for entry in manifest['files']]
    check('source_manifest_shape',manifest['count']==len(names)==18 and len(set(names))==18 and
          all(not Path(name).is_absolute() and '..' not in Path(name).parts and '\n' not in name for name in names) and
          all(name in names for name in ['PROTOCOL.md','config.json','analyze.py']))
    if not report['checks'][-1]['pass']:
        raise ValueError('Source manifest shape failed')
    frozen=committed_blobs(args.repo,args.source_commit,names)
    for entry in manifest['files']:
        raw=frozen[entry['path']]
        check('committed_manifest_entry_'+entry['path'],len(raw)==entry['bytes'] and sha(raw)==entry['sha256'])
    check('current_manifest_matches_commit',(args.repo/PACKAGE/'source-manifest.json').read_bytes()==manifest_bytes)
    config=json.loads(frozen['config.json'])
    check('frozen_configuration_scope',config['nominal_run_rpm']==15030 and config['scenarios']==SCENARIOS and config['static']['rows']==24 and config['axial']['rows']==14 and config['physical_adequacy_threshold'] is None and config['experimental_confidence_interval'] is None)
    for name in names:
        check('current_source_matches_commit_'+name,(args.repo/PACKAGE/name).read_bytes()==frozen[name])
    public_bytes=args.public_result.read_bytes()
    private_bytes=args.private_result.read_bytes()
    public=json.loads(public_bytes); private=json.loads(private_bytes)
    check('saved_source_commit',public['source_commit']==args.source_commit and private['source_commit']==args.source_commit)
    check('saved_analysis_hash',public['analysis_sha256']==sha(frozen['analyze.py']))
    check('private_evidence_hash_and_size',public['private_row_evidence_sha256']==sha(private_bytes) and public['private_row_evidence_bytes']==len(private_bytes))
    check('private_evidence_matches_handoff_pin',sha(private_bytes)==args.expected_private_sha256)
    check('saved_input_pins',all(public['input_hashes'][kind]==private['input_hashes'][kind]==config[kind]['sha256'] for kind in ['static','axial']))
    # Parse target inputs only after immutable source and saved-evidence checks.
    if not all(c['pass'] for c in report['checks']):
        raise ValueError('Source or saved-evidence admission failed before target calculation')
    static_bytes=args.static.read_bytes(); axial_bytes=args.axial.read_bytes()
    static=read_decimal_table(static_bytes,config['static'])
    axial=read_decimal_table(axial_bytes,config['axial'])
    if not all(row['J']>=0 for row in axial):
        raise ValueError('Target inflow outside declared domain')
    ordered=sorted(static,key=lambda row:row['RPM'])
    rpms=[row['RPM'] for row in ordered]; target=Decimal(config['nominal_run_rpm'])
    insertion=bisect.bisect_left(rpms,target)
    if not 0<insertion<len(ordered) or rpms[insertion]==target:
        raise ValueError('Missing strict RPM bracket or unexpected exact match')
    low,high=ordered[insertion-1],ordered[insertion]
    check('nearest_static_anchors_from_sorted_rpm',
          (low['row_id'],low['RPM'],low['CT'])==(13,Decimal('15006.667'),Decimal('.061549')) and
          (high['row_id'],high['RPM'],high['CT'])==(14,Decimal('15960.000'),Decimal('.062855')) and
          rpms.count(low['RPM'])==rpms.count(high['RPM'])==1)
    check('retained_static_order_is_not_fully_sorted',[row['row_id'] for row in ordered]!=[row['row_id'] for row in static])
    if not report['checks'][-2]['pass']:
        raise ValueError('Fixed static anchor admission failed')
    with localcontext() as ctx:
        ctx.prec=70
        fraction=(target-low['RPM'])/(high['RPM']-low['RPM'])
        linear=low['CT']+fraction*(high['CT']-low['CT'])
    c0_values=[linear,low['CT'],high['CT']]
    check('positive_baselines',all(value>0 for value in c0_values))
    expected_anchors=[{'row_id':row['row_id'],'RPM':float(row['RPM']),'CT':float(row['CT'])} for row in [low,high]]
    check('published_anchor_identity',public['baseline_anchors']==expected_anchors)
    check('scenario_identity',len(private['scenarios'])==len(public['scenarios'])==3 and
          [s['scenario'] for s in private['scenarios']]==[s['scenario'] for s in public['scenarios']]==SCENARIOS)
    report['sourcePins']={'commit':args.source_commit,'files':[{'path':name,'sha256':sha(frozen[name]),'bytes':len(frozen[name])} for name in names],
                          'manifestSHA256':sha(manifest_bytes),'manifestEntriesChecked':len(names),
                          'staticSHA256':sha(static_bytes),'axialSHA256':sha(axial_bytes),
                          'privateEvidenceSHA256':sha(private_bytes),'privateEvidenceBytes':len(private_bytes),
                          'publicAggregateSHA256':sha(public_bytes)}
    report['baselineReview']={'method':'Decimal interpolation after numerical RPM sorting',
                             'fileOrderUsedForNeighborSelection':False,'anchors':expected_anchors,
                             'linearInterpolationWeight':str(fraction),'independentC0Values':[float(v) for v in c0_values]}
    report['scenarioReviews']=[]
    count=0; total_iterations=0
    positive_ids=[row['row_id'] for row in axial if row['CT']>0]
    nonpositive_ids=[row['row_id'] for row in axial if row['CT']<=0]
    for scenario,c0,saved_private,saved_public in zip(SCENARIOS,c0_values,private['scenarios'],public['scenarios']):
        check('baseline_recomputed_'+scenario,abs(saved_private['C0']-float(c0))<=TOL['baseline'] and abs(saved_public['C0']-float(c0))<=TOL['baseline'])
        saved_rows=saved_private['rows']
        check('all_fourteen_saved_rows_'+scenario,len(saved_rows)==14 and [r['row_id'] for r in saved_rows]==list(range(1,15)))
        private_records=[]
        maxima={'alphaDelta':0.0,'rootDelta':0.0,'predictionDelta':0.0,'CTResidualDelta':0.0,
                'independentCubicResidual':0.0,'savedCubicResidualRecomputed':0.0,'reportedCubicResidualDelta':0.0}
        failed=[]; iterations=0; saved_residuals=[]; widths=[]
        for observed,saved in zip(axial,saved_rows):
            alpha=float(observed['J'])*math.sqrt(math.pi/(2*float(c0)))
            x=positive_cubic_hyperbolic(alpha)
            cubic=x*x*x+alpha*x-1
            prediction=float(c0)*x
            residual=prediction-float(observed['CT'])
            answer=saved['root']; lo=answer['lo']; hi=answer['hi']; sx=answer['x']
            saved_cubic=sx*sx*sx+saved['alpha']*sx-1
            deltas={'alphaDelta':abs(saved['alpha']-alpha),'rootDelta':abs(sx-x),
                    'predictionDelta':abs(saved['predicted_CT']-prediction),
                    'CTResidualDelta':abs(saved['residual_CT_prediction_minus_reported']-residual),
                    'independentCubicResidual':abs(cubic),'savedCubicResidualRecomputed':abs(saved_cubic),
                    'reportedCubicResidualDelta':abs(answer['residual']-saved_cubic)}
            for key,value in deltas.items(): maxima[key]=max(maxima[key],value)
            operand_ok=saved['row_id']==observed['row_id'] and saved['J']==float(observed['J']) and saved['reported_CT']==float(observed['CT']) and saved['reported_positive_thrust']==(observed['CT']>0)
            numerical_ok=0<x<=1+TOL['root'] and prediction>0 and abs(cubic)<=TOL['cubic'] and deltas['alphaDelta']<=TOL['alpha'] and deltas['rootDelta']<=TOL['root'] and deltas['predictionDelta']<=TOL['CT'] and deltas['CTResidualDelta']<=TOL['CT']
            bracket_ok=0<=lo<=sx<=hi<=1 and 0<sx<=1 and hi-lo<=config['root_width_tolerance'] and abs(saved_cubic)<=config['root_residual_tolerance'] and abs(answer['residual'])<=config['root_residual_tolerance'] and deltas['reportedCubicResidualDelta']<=TOL['cubic'] and lo**3+saved['alpha']*lo-1<=1e-14 and hi**3+saved['alpha']*hi-1>=-1e-14 and lo-TOL['root']<=x<=hi+TOL['root'] and type(answer['iterations']) is int and 0<=answer['iterations']<=config['max_iterations_per_root']
            if not (operand_ok and numerical_ok and bracket_ok): failed.append(observed['row_id'])
            private_records.append({'row_id':observed['row_id'],'prediction':prediction,
                                    'reported_CT_decimal':observed['CT'],'positive':observed['CT']>0})
            widths.append(hi-lo); saved_residuals.append(abs(answer['residual'])); iterations+=answer['iterations']; count+=1
        full=independent_metrics(private_records,c0)
        secondary=independent_metrics([row for row in private_records if row['positive']],c0)
        full_match=compare_metrics(full,saved_public['full_run'])
        secondary_match=compare_metrics(secondary,saved_public['reported_positive_thrust_subset'])
        check('all_predictions_operands_labels_and_brackets_'+scenario,not failed,{'rowsChecked':len(saved_rows),'failedRowIDs':failed})
        check('full_and_secondary_statistics_'+scenario,full_match['pass'] and secondary_match['pass'])
        check('nonpositive_rows_preserved_'+scenario,saved_public['nonpositive_row_ids']==nonpositive_ids and full['row_ids']==list(range(1,15)) and (secondary is None and not positive_ids or secondary is not None and secondary['row_ids']==positive_ids))
        check('saved_numerical_aggregates_'+scenario,abs(saved_public['max_absolute_cubic_residual']-max(saved_residuals))<=TOL['cubic'] and abs(saved_public['max_bracket_width']-max(widths))<=1e-18 and saved_public['bisection_iterations']==iterations)
        total_iterations+=iterations
        report['scenarioReviews'].append({'scenario':scenario,'independentC0':float(c0),'rowsChecked':len(saved_rows),
            'alphaAndPredictionsRecomputedForThisScenario':True,'aggregateNumericalComparisonMaxima':maxima,
            'fullRunIndependentAggregates':full,'reportedPositiveCTIndependentAggregates':secondary,
            'fullRunComparison':full_match,'secondaryComparison':secondary_match,
            'nonpositiveCount':len(nonpositive_ids),'nonpositiveRowIDs':nonpositive_ids,
            'nonpositiveLabel':'Reported CT<=0; outside the model representable positive-thrust branch, not a rejection under original ideal-power control.',
            'savedBisectionIterations':iterations,'allRowsPassed':not failed})
    check('exact_prediction_count_and_iteration_budget',count==42 and public['root_count']==42 and public['rows_per_scenario']==14 and total_iterations<=42*config['max_iterations_per_root'])
    check('no_physical_or_statistical_threshold',public['physical_adequacy_threshold'] is None and public['experimental_confidence_interval'] is None)
    report['predictionsReviewed']=count
    report['savedBisectionIterationTotal']=total_iterations
    report['publicPerRowNumericTableEmitted']=False

def main():
    parser=argparse.ArgumentParser()
    for name in ['repo','static','axial','private-result','public-result']:
        parser.add_argument('--'+name,type=Path,required=True)
    parser.add_argument('--source-commit',required=True)
    parser.add_argument('--expected-manifest-sha256',required=True)
    parser.add_argument('--expected-private-sha256',required=True)
    args=parser.parse_args()
    resource.setrlimit(resource.RLIMIT_CPU,(15,15))
    start=time.process_time()
    here=Path(__file__).resolve().parent
    report={'kind':'independent-GWS-aggregate-saved-result-review','checks':[],
            'reviewPlanSHA256':sha((here/'REVIEW-PLAN.json').read_bytes()),
            'rootAnalyzerImports':0,'rootAnalyzerReruns':0,'newPhysicalData':0}
    try:
        run(args,report)
    except Exception as error:
        report['exceptionType']=type(error).__name__
        report['checks'].append({'name':'completed_without_exception','pass':False})
    report['cpuSecondsForAllocationOnly']=time.process_time()-start
    report['checks'].append({'name':'review_cpu_under_fifteen_seconds','pass':report['cpuSecondsForAllocationOnly']<15})
    report['allChecksPass']=all(row['pass'] for row in report['checks'])
    report['checkCount']=len(report['checks'])
    report['limits']=['Exposed ideal-disk equation plus prescribed-RPM baseline bridge; equation and bridge errors are not isolated.',
                      'Endpoint scenarios are baseline-choice sensitivity, not confidence intervals.',
                      'No physical adequacy threshold, shaft-power validation or original vehicle qualification.',
                      'No complete raw table or complete per-row derived table is included.']
    output=(json.dumps(report,indent=2,sort_keys=True,allow_nan=False)+'\n').encode()
    if len(output)>=256*1024:
        raise ValueError('Public review output cap exceeded')
    with (here/'REVIEW-CHECKS.json').open('xb') as stream:
        stream.write(output)
    print(json.dumps({'allChecksPass':report['allChecksPass'],'checkCount':report['checkCount'],
                      'predictionsReviewed':report.get('predictionsReviewed',0),'publicOutputBytes':len(output),
                      'rootAnalyzerReruns':0}))
    raise SystemExit(0 if report['allChecksPass'] else 1)

if __name__=='__main__':
    main()
