"""Finite descriptive comparison of two exposed published graphical profiles."""
import argparse
import hashlib
import json
import math
import subprocess
from pathlib import Path

def interp(knots, x):
    for (a, ya), (b, yb) in zip(knots, knots[1:]):
        if a <= x <= b:
            return ya + (yb - ya) * ((x - a) / (b - a))
    raise ValueError('No extrapolation allocated')

def weighted_square(a, b, ya, yb):
    # Local coordinate t=x-a avoids cancellation in small global intervals.
    h = b-a
    slope = (yb-ya)/h
    return a*ya*ya*h + (ya*ya+2*a*ya*slope)*h*h/2 + (2*ya*slope+a*slope*slope)*h**3/3 + slope*slope*h**4/4

def crossings(knots):
    target = knots[0][1]/2
    assert knots[0][0] == 0 and target > 0
    points, plateaus = [], []
    for (a, ya), (b, yb) in zip(knots, knots[1:]):
        if ya == yb == target:
            plateaus.append([a,b])
        elif ya != yb and min(ya,yb) <= target <= max(ya,yb):
            x = a+(target-ya)*(b-a)/(yb-ya)
            if not points or abs(points[-1]-x) > 1e-12:
                points.append(x)
    directions=[]
    for x in points:
        left=[a for a,y in knots if a<x]
        right=[a for a,y in knots if a>x]
        if not left or not right:
            directions.append('boundary intersection')
        else:
            before=interp(knots,(max(left)+x)/2)-target
            after=interp(knots,(min(right)+x)/2)-target
            directions.append('downward' if before>0>after else 'upward' if before<0<after else 'tangential or plateau contact')
    return {'threshold': target, 'radii': points, 'directions': directions, 'plateau_intervals': plateaus,
            'unique_intersection': len(points)==1 and not plateaus,
            'unique_downward_crossing': len(points)==1 and not plateaus and directions==['downward']}

def validate(data):
    assert data['schema']=='published-profile-extraction-v1'
    assert data['source_sha256']=='81987dfd1cf2980270defd9447a9e5fb6c1586eab77b75b730de127c932d373c'
    assert data['source']=='https://arxiv.org/pdf/2403.13321v3'
    assert data['page']==5 and data['figure']==7
    assert data['axes']['x_domain']==[0.,3.] and data['axes']['y_domain']==[0.,1.5]
    assert data['axes']['x']=='r/l' and data['axes']['y']=='speed magnitude / calculated hover induced speed UH'
    assert data['axes']['downstream_s_over_l']==3.
    assert len(data['profiles'])==2
    for s,name,index in zip(data['profiles'],['Offboard 1','Offboard 2'],[32,33]):
        assert s['name']==name and s['curve_index']==index and s['visible_original_vertices']==16
        knots=s['knots']
        assert len(knots)==17 and knots[0]['r_over_l']==0 and knots[-1]['r_over_l']==3
        assert all(math.isfinite(p['r_over_l']) and math.isfinite(p['speed_over_UH']) and 0<=p['speed_over_UH']<=1.5 for p in knots)
        assert all(b['r_over_l']>a['r_over_l'] for a,b in zip(knots,knots[1:]))
        assert knots[0]['speed_over_UH']>0
        assert all(p['kind']=='original graphical vertex' for p in knots[:-1])
        assert knots[-1]['kind']=='interpolated clip intersection; not a measured vertex'

def compare(first, second):
    assert first[0][0] == second[0][0] == 0 and first[-1][0] == second[-1][0] == 3
    union = sorted(set(x for x,y in first+second))
    rows = [{'r_over_l': x, 'g1': interp(first,x), 'g2': interp(second,x)} for x in union]
    for row in rows:
        row['difference_g2_minus_g1'] = row['g2']-row['g1']
    numerator = denominator = 0.
    for a,b in zip(rows,rows[1:]):
        numerator += weighted_square(a['r_over_l'],b['r_over_l'],a['difference_g2_minus_g1'],b['difference_g2_minus_g1'])
        denominator += weighted_square(a['r_over_l'],b['r_over_l'],a['g2'],b['g2'])
    assert denominator > 0 and numerator >= 0
    maximum = max(abs(row['difference_g2_minus_g1']) for row in rows)
    return {'max_absolute_normalized_discrepancy': maximum,
            'maximizing_radii': [row['r_over_l'] for row in rows if abs(abs(row['difference_g2_minus_g1'])-maximum)<1e-14],
            'radially_weighted_relative_L2_using_offboard2_reference': math.sqrt(numerator/denominator),
            'weighted_squared_difference_integral': numerator, 'weighted_squared_reference_integral': denominator,
            'half_centerline_crossings': [crossings(first),crossings(second)], 'union_knot_records': rows}

def tests():
    flat = [(0.,1.),(3.,1.)]
    ramp = [(0.,2.),(1.,1.),(3.,0.)]
    same = compare(ramp,ramp)
    assert same['max_absolute_normalized_discrepancy'] == 0
    assert same['radially_weighted_relative_L2_using_offboard2_reference'] == 0
    assert abs(weighted_square(0,3,0,3)-81/4) < 1e-12
    assert abs(weighted_square(1,2,1,2)-15/4) < 1e-12
    assert crossings(ramp)['radii'] == [1.]
    assert not crossings(flat)['unique_intersection']
    assert crossings([(0.,2.),(1.,0.),(2.,2.),(3.,0.)])['radii'] == [.5,1.5,2.5]
    assert crossings([(0.,2.),(1.,1.),(2.,1.),(3.,0.)])['plateau_intervals'] == [[1.,2.]]
    assert crossings([(0.,2.),(1.,1.),(3.,2.)])['directions']==['tangential or plateau contact']
    assert not crossings([(0.,2.),(1.,1.),(3.,2.)])['unique_downward_crossing']
    return {'passed': True, 'checks': 10, 'scope': 'Synthetic algebra, identical curves, missing/multiple/plateau/tangential half-speed intersections; no experimental contrasts'}

if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--test',action='store_true')
    parser.add_argument('--input',type=Path)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    if args.test:
        print(json.dumps(tests(),indent=2))
    else:
        tests()
        raw=args.input.read_bytes()
        data=json.loads(raw)
        validate(data)
        first,second=[[(p['r_over_l'],p['speed_over_UH']) for p in s['knots']] for s in data['profiles']]
        result=compare(first,second)
        result.update({'kind': 'exposed-published-profile-descriptive-audit',
            'input_sha256': hashlib.sha256(raw).hexdigest(),
            'analysis_source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'source_commit': subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),
            'centerline_values': [first[0][1],second[0][1]],
            'graphical_stroke_half_width_normalized_y': .79701/2*1.5/data['axes']['height_pt'],
            'graphical_stroke_half_width_normalized_x': .79701/2*3/data['axes']['width_pt'],
            'experimental_confidence_interval': None, 'physical_pass_threshold': None,
            'scope': 'Two displayed median polylines, one exposed same tabulated frame-dimension hover pair at s/l=3. No independent validation or novelty claim.'})
        with args.output.open('x') as f:
            json.dump(result,f,indent=2,allow_nan=False);f.write('\n')
