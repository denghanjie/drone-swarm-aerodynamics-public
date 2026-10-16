"""Frozen independent semantic source, adapted by text from the prior checker.

No old fixture generators, suites, controls or main routine are included.
Loaded only from verified source bytes by the saved streaming checker.
"""
from collections import Counter
from fractions import Fraction
from math import isqrt
import json
import re
SCALE = 1 << 96
MAX_ERRORS = 48
CATEGORIES = ('rotor','collective','worldForce','worldMoment')
RULES = ('neighbor','upstream','down-cut','near-outside','radial')
WORK_FIELDS = ('preparationCalls','globalProofs','treeNodes','nodeVisits','nodeRuleTests',
               'zeroNodes','zeroPairs','leafVisits','scalarPairs','scalarZeroPairs',
               'positiveTerms','rejectedPairs','unresolvedPairs')

class CheckError(Exception):
    """An intentionally public-safe validation failure."""


def require(condition, code):
    if not condition:
        raise CheckError(code)


def canonical_integer(value):
    require(isinstance(value, str) and len(value) <= 108,
            "endpoint-string-shape")
    require(re.fullmatch(r"0|-?[1-9][0-9]*", value) is not None,
            "endpoint-string-syntax")
    return int(value)


def same_json(left, right):
    """Structural equality without Python's True == 1 or 1.0 == 1 aliases."""
    if type(left) is not type(right):
        return False
    if isinstance(left, dict):
        return set(left) == set(right) and all(same_json(left[k], right[k]) for k in left)
    if isinstance(left, list):
        return len(left) == len(right) and all(same_json(a, b) for a, b in zip(left, right))
    return left == right


class Findings:
    def __init__(self):
        self.total, self.errors = 0, []

    def add(self, code, index=None):
        self.total += 1
        if len(self.errors) < MAX_ERRORS:
            self.errors.append((code if index is None else code + ':scene=' + str(index))[:256])

    def check(self, condition, code, index=None):
        if not condition:
            self.add(code, index)


def fraction_wire(value):
    result = {'n': str(value.numerator), 'd': str(value.denominator)}
    require(all(len(text) <= 256 for text in result.values()), 'outbound-rational-string-budget')
    return result


def interval_wire(interval):
    return {'l': fraction_wire(interval[0]), 'u': fraction_wire(interval[1])}


def fields(value, names, code):
    require(isinstance(value, dict) and set(value) == set(names), code)


def sequence(value, count, code):
    require(isinstance(value, list) and len(value) == count, code)
    return value


def integer(value, low, high, code):
    require(type(value) is int and low <= value <= high, code)
    return value


def candidate_interval(value):
    fields(value, ('l', 'u'), 'interval-fields')
    lo, hi = canonical_integer(value['l']), canonical_integer(value['u'])
    require(-(1 << 352) <= lo <= hi <= 1 << 352, 'interval-order-or-range')
    return Fraction(lo, SCALE), Fraction(hi, SCALE)


def upper_value(value):
    number = canonical_integer(value)
    require(0 <= number <= 1 << 352, 'upper-range')
    return Fraction(number, SCALE)


def rational(value, max_chars=256):
    fields(value, ('n', 'd'), 'rational-fields')
    # Finite binary64 products can have subnormal denominators beyond 128 digits.
    for key in ('n', 'd'):
        require(isinstance(value[key], str) and len(value[key]) <= max_chars and
                re.fullmatch(r'0|-?[1-9][0-9]*', value[key]) is not None,
                'rational-integer-shape')
    numerator, denominator = int(value['n']), int(value['d'])
    require(denominator > 0, 'rational-denominator')
    result = Fraction(numerator, denominator)
    require(result.numerator == numerator and result.denominator == denominator,
            'rational-not-reduced')
    return result


def contains(outer, inner, code):
    require(outer[0] <= inner[0] <= inner[1] <= outer[1], code)


def plus(a, b):
    return a[0] + b[0], a[1] + b[1]


def times(a, b):
    products = (a[0]*b[0], a[0]*b[1], a[1]*b[0], a[1]*b[1])
    return min(products), max(products)


def scaled(a, factor):
    return times(a, (factor, factor))


def sum_intervals(values):
    answer = (Fraction(0), Fraction(0))
    for value in values:
        answer = plus(answer, value)
    return answer


def quantize(interval, bits):
    scale = 1 << bits
    lower, upper = interval[0] * scale, interval[1] * scale
    return (Fraction(lower.numerator // lower.denominator, scale),
            Fraction(-((-upper.numerator) // upper.denominator), scale))


def sqrt_bounds(value, bits):
    require(value >= 0, 'sqrt-domain')
    scale = 1 << bits
    squared = value * scale * scale
    lower = isqrt(squared.numerator // squared.denominator)
    upper = lower if lower * lower == squared else lower + 1
    return Fraction(lower, scale), Fraction(upper, scale)


def cross(a, b):
    return tuple(a[(k+1)%3]*b[(k+2)%3] - a[(k+2)%3]*b[(k+1)%3]
                 for k in range(3))


def prepared_exact(value, helper):
    forces = helper.exact_vector(value['forces'])
    axis = helper.exact_vector(value['axis'])
    offsets = [helper.exact_vector(row) for row in value['offsets']]
    return {'forces': forces, 'axis': axis, 'levers': [cross(v, axis) for v in offsets],
            'weights': tuple(v / sum(forces, Fraction(0)) for v in forces)}


def load_boxes(prepared, roots):
    rotor = [scaled(x, f) for x, f in zip(roots, prepared['forces'])]
    collective = sum_intervals(rotor)
    force = [scaled(collective, v) for v in prepared['axis']]
    moment = [sum_intervals(scaled(rotor[r], prepared['levers'][r][k]) for r in range(4))
              for k in range(3)]
    return {'rotor': rotor, 'collective': collective, 'force': force, 'moment': moment}


def bisect_cubic(alpha):
    """Exactly 128 prescribed bisections; exact roots are retained as points."""
    require(alpha >= 0, 'reference-alpha-domain')
    if alpha == 0:
        return Fraction(1), Fraction(1)
    lower, upper = Fraction(0), Fraction(1)
    for _ in range(128):
        middle = (lower + upper) / 2
        value = middle**3 + alpha * middle
        if value == 1:
            lower = upper = middle
        elif value < 1:
            lower = middle
        else:
            upper = middle
    return lower, upper


def source_box(weights, roots, bits):
    weighted = sum_intervals(scaled(root, weight) for root, weight in zip(roots, weights))
    return sqrt_bounds(weighted[0], bits)[0], sqrt_bounds(weighted[1], bits)[1]


def reference_roots(target):
    roots, sources, loads = {}, {}, {}
    rows = {(drone_id, r): [] for drone_id in target['order'] for r in range(4)}
    for pair in target['pairs']:
        if pair['oracle']['status'] == 'positive':
            rows[(pair['i'], pair['r'])].append((pair['j'], pair['coefficient']))
    for drone_id in target['order']:
        group = []
        for r in range(4):
            alpha = sum_intervals(times(coefficient, sources[source])
                                  for source, coefficient in rows[(drone_id, r)])
            root = (bisect_cubic(alpha[1])[0], bisect_cubic(alpha[0])[1])
            require(0 < root[0] <= root[1] <= 1, 'reference-root-domain')
            roots[(drone_id, r)] = root
            group.append(root)
        sources[drone_id] = source_box(target['exact'][drone_id]['weights'], group, 192)
        loads[drone_id] = load_boxes(target['exact'][drone_id], group)
    return roots, loads


def absolute_error(point, box):
    return max(abs(point-box[0]), abs(point-box[1]))


def validate_certificate(row, target, coefficients, helper, constants, emit_reference=False):
    solve, certificate = row['solve'], row['certificate']
    fields(solve, ('iterations','bisections','candidate'), 'solve-fields')
    require(type(solve['iterations']) is int and solve['iterations'] == 48 and
            type(solve['bisections']) is int and solve['bisections'] == 54, 'solve-recipe-metadata')
    ids = [d['id'] for d in target['input']['drones']]
    candidates = sequence(solve['candidate'], len(ids), 'candidate-count')
    xhat, yhat = {}, {}
    for identifier, candidate in zip(ids, candidates):
        fields(candidate, ('id','x'), 'candidate-fields')
        require(type(candidate['id']) is int and candidate['id'] == identifier, 'candidate-id-order')
        values = sequence(candidate['x'], 4, 'candidate-rotor-count')
        roots = []
        for rotor, value in enumerate(values):
            word = helper.parse_bits(value)
            require(helper.finite(word), 'candidate-nonfinite')
            exact = helper.dyadic(word)
            require(0 < exact <= 1, 'candidate-domain')
            xhat[(identifier,rotor)] = exact
            roots.append((exact,exact))
        yhat[identifier] = source_box(target['exact'][identifier]['weights'], roots, 96)
    fields(certificate, ('rows','Kbar','loads','maxErrors'), 'certificate-fields')
    # Exact candidate load identity precedes row/root checks so a mutated
    # native word cannot be rejected only by a downstream enclosure check.
    for identifier, load in zip(ids, sequence(certificate['loads'],len(ids),'load-count')):
        fields(load, ('id','candidate','bounds','error'), 'load-fields')
        require(type(load['id']) is int and load['id'] == identifier,'load-id-order')
        fields(load['candidate'],('rotor','collective','force','moment'),'candidate-load-fields')
        exact_load = load_boxes(target['exact'][identifier],
            [(xhat[(identifier,r)],xhat[(identifier,r)]) for r in range(4)])
        for category,count in (('rotor',4),('force',3),('moment',3)):
            values=sequence(load['candidate'][category],count,'candidate-load-vector-count')
            for k,value in enumerate(values):
                point=rational(value)
                require(exact_load[category][k] == (point,point),'candidate-load-identity:'+category)
        point=rational(load['candidate']['collective'])
        require(exact_load['collective'] == (point,point),'candidate-load-identity:collective')
    Kbar = upper_value(certificate['Kbar'])
    require(Kbar >= 1, 'global-factor-domain')
    rows = sequence(certificate['rows'], 4*len(ids), 'certificate-row-count')
    grouped = {(identifier,r): [] for identifier in ids for r in range(4)}
    for pair, coefficient in zip(target['pairs'], coefficients):
        if pair['oracle']['status'] == 'positive':
            require(coefficient is not None, 'missing-certified-coefficient')
            grouped[(pair['i'],pair['r'])].append(times(coefficient, yhat[pair['j']]))
    xstar = {}
    for index, saved in enumerate(rows):
        identifier, rotor = ids[index//4], index%4
        fields(saved, ('id','r','s','p','kbar','xstar'), 'certificate-row-fields')
        require(type(saved['id']) is int and saved['id'] == identifier and
                type(saved['r']) is int and saved['r'] == rotor, 'certificate-row-id-order')
        source = candidate_interval(saved['s'])
        require(source[0] >= 0, 'row-source-domain')
        contains(source, sum_intervals(grouped[(identifier,rotor)]), 'complete-row-contraction')
        proposal = xhat[(identifier,rotor)]
        defect = candidate_interval(saved['p'])
        contains(defect, plus((proposal**3,proposal**3), scaled(source, proposal)),
                 'row-defect-enclosure')
        require(defect[0] > 0, 'defect-positive-lower')
        kbar = upper_value(saved['kbar'])
        require(kbar >= max(Fraction(1), defect[1], 1/defect[0]), 'row-factor-upper')
        require(Kbar >= kbar, 'global-factor-upper')
        root = candidate_interval(saved['xstar'])
        require(0 <= root[0] <= root[1] <= 1, 'root-interval-domain')
        contains(root, (proposal/(kbar*Kbar), min(Fraction(1),proposal*kbar*Kbar)),
                 'root-defect-corollary')
        contains(root, target['roots'][(identifier,rotor)], 'independent-root-containment')
        xstar[(identifier,rotor)] = root
    loads = sequence(certificate['loads'], len(ids), 'load-count')
    maxima = {name: Fraction(0) for name in CATEGORIES}
    reference_evidence = []
    mg, radius = constants['mg'], constants['R']
    require(mg > 0 and radius > 0, 'normalization-domain')
    for identifier, load in zip(ids, loads):
        fields(load, ('id','candidate','bounds','error'), 'load-fields')
        require(type(load['id']) is int and load['id'] == identifier, 'load-id-order')
        geometry = target['exact'][identifier]
        proposal_boxes = load_boxes(geometry, [(xhat[(identifier,r)], xhat[(identifier,r)]) for r in range(4)])
        propagated = load_boxes(geometry, [xstar[(identifier,r)] for r in range(4)])
        reference = target['loads'][identifier]
        fields(load['candidate'], ('rotor','collective','force','moment'), 'candidate-load-fields')
        fields(load['bounds'], ('rotor','collective','force','moment'), 'load-bounds-fields')
        point, boxes = {}, {}
        for name, count in (('rotor',4),('force',3),('moment',3)):
            point[name] = [rational(v) for v in sequence(load['candidate'][name], count,
                                                       'candidate-load-vector-count')]
            boxes[name] = [candidate_interval(v) for v in sequence(load['bounds'][name], count,
                                                                  'load-box-vector-count')]
            for k in range(count):
                require(proposal_boxes[name][k] == (point[name][k],point[name][k]),
                        'candidate-load-identity:' + name)
                contains(boxes[name][k], propagated[name][k], 'signed-root-load-propagation:' + name)
                contains(boxes[name][k], reference[name][k], 'independent-load-containment:' + name)
        point['collective'] = rational(load['candidate']['collective'])
        boxes['collective'] = candidate_interval(load['bounds']['collective'])
        require(proposal_boxes['collective'] == (point['collective'],point['collective']),
                'candidate-load-identity:collective')
        contains(boxes['collective'], propagated['collective'], 'signed-root-load-propagation:collective')
        contains(boxes['collective'], reference['collective'], 'independent-load-containment:collective')
        fields(load['error'], CATEGORIES, 'load-error-fields')
        rotor_errors = [upper_value(v) for v in sequence(load['error']['rotor'],4,'rotor-error-count')]
        for r, error in enumerate(rotor_errors):
            require(error * (mg/4) >= absolute_error(point['rotor'][r], boxes['rotor'][r]),
                    'rotor-error-full-box')
        maxima['rotor'] = max(maxima['rotor'], *rotor_errors)
        collective_error = upper_value(load['error']['collective'])
        require(collective_error * mg >= absolute_error(point['collective'], boxes['collective']),
                'collective-error-full-box')
        maxima['collective'] = max(maxima['collective'], collective_error)
        for category, name, denominator in (('worldForce','force',mg),('worldMoment','moment',mg*radius)):
            error = upper_value(load['error'][category])
            norm_squared = sum((absolute_error(point[name][k],boxes[name][k])**2 for k in range(3)), Fraction(0))
            require((error*denominator)**2 >= norm_squared, category + '-error-full-box')
            maxima[category] = max(maxima[category], error)
        if emit_reference:
            reference_evidence.append({'id': identifier,
                'roots': [interval_wire(target['roots'][(identifier,r)]) for r in range(4)],
                'loads': {name: interval_wire(value) if name == 'collective' else
                          [interval_wire(v) for v in value] for name,value in reference.items()}})
    fields(certificate['maxErrors'], CATEGORIES, 'scene-max-error-fields')
    declared = {name: upper_value(certificate['maxErrors'][name]) for name in CATEGORIES}
    for name in CATEGORIES:
        require(declared[name] >= maxima[name], 'scene-max-error-upper:' + name)
    achieved = all(value*100000000 <= 1 for value in declared.values())
    require(same_json(row['result'], {'status': 'certified' if achieved else 'tolerance-failed',
             'branch': 'loads', 'witness': None, 'toleranceAchieved': achieved}),
            'tolerance-status-exact-decision')
    return {'toleranceAchieved': achieved, 'maxErrorUppers': certificate['maxErrors'],
            'independentReference': reference_evidence}


def compact_bytes(value):
    return len(json.dumps(value,separators=(',',':'),ensure_ascii=True).encode('utf-8'))


def box_of(vectors):
    require(bool(vectors),'empty-box-membership')
    return tuple((min(v[k] for v in vectors),max(v[k] for v in vectors)) for k in range(3))


def subtract(a,b):
    return a[0]-b[1],a[1]-b[0]


def absolute_max(interval):
    return max(abs(interval[0]),abs(interval[1]))


def absolute_min(interval):
    return Fraction(0) if interval[0] <= 0 <= interval[1] else min(abs(interval[0]),abs(interval[1]))


def box_wire(box):
    return [[fraction_wire(endpoint) for endpoint in interval] for interval in box]


def global_guard(geometry):
    centers = box_of([v['center'] for v in geometry])
    axes = box_of([v['axis'] for v in geometry])
    points = box_of([point for v in geometry for point in v['points']])
    center_difference = tuple(subtract(v,v) for v in centers)
    displacement = tuple(subtract(a,b) for a,b in zip(centers,points))
    height = sum_intervals(times(a,b) for a,b in zip(displacement,axes))
    residual = tuple(subtract(d,times(height,a)) for d,a in zip(displacement,axes))
    upper = {'centerComponent':max(absolute_max(v) for v in center_difference),
             'centerNorm':sum((absolute_max(v)**2 for v in center_difference),Fraction(0)),
             'rotorComponent':max(absolute_max(v) for v in displacement),
             'down':absolute_max(height),
             'radial':sum((absolute_max(v)**2 for v in residual),Fraction(0))}
    limits = {'centerComponent':Fraction(257),'centerNorm':Fraction(512**2),
              'rotorComponent':Fraction(258),'down':Fraction(1024),'radial':Fraction(2048**2)}
    checks = {key:upper[key] <= limit for key,limit in limits.items()}
    return {'passed':all(checks.values()),'checks':checks}, {'upper':upper,'limits':limits}


def reconstruct_tree(geometry,ids):
    nodes,permutation,members,boxes = [],[],{},{}
    def build(indices):
        node_id = len(nodes)
        center = box_of([geometry[i]['center'] for i in indices])
        axis = box_of([geometry[i]['axis'] for i in indices])
        node = {'id':node_id,'start':len(permutation),'end':None,'left':None,'right':None,
                'center':box_wire(center),'axis':box_wire(axis)}
        nodes.append(node)
        members[node_id] = tuple(indices)
        boxes[node_id] = {'center':center,'axis':axis}
        if len(indices) <= 8:
            # Preserve incoming recursive order; a small root preserves input order.
            permutation.extend(ids[i] for i in indices)
        else:
            spans = [interval[1]-interval[0] for interval in center]
            split_axis = max(range(3),key=lambda k:(spans[k],-k))
            ordered = sorted(indices,key=lambda i:(geometry[i]['center'][split_axis],ids[i]))
            midpoint = len(ordered)//2
            node['left'] = build(ordered[:midpoint])
            node['right'] = build(ordered[midpoint:])
        node['end'] = len(permutation)
        return node_id
    build(list(range(len(ids))))
    return {'permutation':permutation,'nodes':nodes},members,boxes


def zero_rule(node,receiver,rotor,constants):
    centers,axes = node['center'],node['axis']
    center_distance = tuple((v[0]-receiver['center'][k],v[1]-receiver['center'][k])
                            for k,v in enumerate(centers))
    displacement = tuple((v[0]-receiver['points'][rotor][k],v[1]-receiver['points'][rotor][k])
                         for k,v in enumerate(centers))
    height = sum_intervals(times(a,b) for a,b in zip(displacement,axes))
    residual = tuple(subtract(d,times(height,a)) for d,a in zip(displacement,axes))
    radial_lower = sum((absolute_min(v)**2 for v in residual),Fraction(0))
    # W=(spread*(H/D-origin))*D; subtract origin before multiplying spread.
    width = scaled((height[0]/constants['D']-constants['origin'],
                    height[1]/constants['D']-constants['origin']),constants['spread']*constants['D'])
    conditions = (
        sum((absolute_min(v)**2 for v in center_distance),Fraction(0)) >= constants['neighbor']**2,
        height[1] <= 0,
        height[0] >= constants['downCut'],
        height[1] < constants['minDown']*constants['D'] and radial_lower >= constants['nearRad']**2,
        height[0] >= constants['minDown']*constants['D'] and width[0] > 0 and
            radial_lower >= constants['radCut']**2*width[1]**2)
    for index,condition in enumerate(conditions):
        if condition:
            return RULES[index],index+1
    return None,len(RULES)


def blank_work(count):
    result = {name:0 for name in WORK_FIELDS}
    result['preparationCalls'] = count
    return result


def assembly_plan(target,method,constants):
    n = len(target['input']['drones'])
    work = blank_work(n)
    if target['globalInvalid']:
        return {'mode':'global-preparation','globalGuard':None,'tree':None,'queries':[],
                'work':work,'rules':{name:0 for name in RULES}}
    guard = target['globalGuard'] if method == 'hierarchy' else None
    mode = 'complete' if method == 'complete' else ('hierarchy' if guard['passed'] else 'fallback')
    if method == 'hierarchy':
        work['globalProofs'] = 1
    tree = target['tree'] if mode == 'hierarchy' else None
    if tree is not None:
        work['treeNodes'] = len(tree['nodes'])
    queries,rule_counts = [],{name:0 for name in RULES}
    for receiver in range(n):
        for rotor in range(4):
            terminals = []
            def add_scalar(kind,eligible,node=None):
                terminal = {'kind':kind,'members':tuple(sorted(eligible))}
                if node is not None:
                    terminal['node'] = node
                    work['leafVisits'] += 1
                terminals.append(terminal)
                work['scalarPairs'] += len(eligible)
                for source in eligible:
                    status = target['lookup'][(receiver,rotor,source)]['oracle']['status']
                    counter = {'zero':'scalarZeroPairs','positive':'positiveTerms',
                               'rejected':'rejectedPairs','reference-undecidable':'unresolvedPairs'}[status]
                    work[counter] += 1
            if mode != 'hierarchy':
                add_scalar('scan',[j for j in range(n) if j != receiver])
            else:
                def visit(node_id):
                    node = tree['nodes'][node_id]
                    eligible = tuple(j for j in target['members'][node_id] if j != receiver)
                    work['nodeVisits'] += 1
                    rule,tests = zero_rule(target['boxes'][node_id],target['geometry'][receiver],rotor,constants)
                    work['nodeRuleTests'] += tests
                    if rule is not None:
                        # A finite full-oracle cross-check supplements, but does not
                        # replace, the independent node interval proof.
                        require(all(target['lookup'][(receiver,rotor,j)]['oracle']['status'] == 'zero'
                                    for j in eligible),'reference-zero-rule-contradiction')
                        terminals.append({'kind':'zero','node':node_id,'rule':rule,
                                          'count':len(eligible),'members':eligible})
                        work['zeroNodes'] += 1
                        work['zeroPairs'] += len(eligible)
                        rule_counts[rule] += 1
                    elif node['left'] is None:
                        add_scalar('leaf',eligible,node_id)
                    else:
                        visit(node['left'])
                        visit(node['right'])
                visit(0)
            covered = [j for terminal in terminals for j in terminal['members']]
            require(sorted(covered) == [j for j in range(n) if j != receiver],
                    'reference-plan-partition')
            queries.append({'i':receiver,'r':rotor,'terminals':terminals})
    require(work['zeroPairs']+work['scalarPairs'] == target['planned'],'reference-work-coverage')
    return {'mode':mode,'globalGuard':guard,'tree':tree,'queries':queries,'work':work,'rules':rule_counts}


def regenerate_scene(scene, spec, constant_bits, helper):
    """Only one scene oracle exists; still evaluate every logical nonself pair."""
    constants = {name:helper.dyadic(value) for name,value in constant_bits.items()}
    fields(scene,('id','family','expectedClass','drones'),'spec-scene-fields')
    name = scene['id']
    require(isinstance(name,str) and re.fullmatch(r'[a-z][a-z0-9-]{0,63}',name)
            ,'spec-scene-id')
    drones = scene['drones']
    require(isinstance(drones,list) and 1 <= len(drones) <= 216,'spec-drone-count')
    inputs,prepared,ids,exact,geometry = [],[],[],{},[]
    for drone in drones:
        fields(drone,('id','state'),'spec-drone-fields')
        identifier = integer(drone['id'],0,65535,'spec-stable-id')
        require(identifier not in ids,'spec-duplicate-id')
        ids.append(identifier)
        state = sequence(drone['state'],17,'spec-raw-state-count')
        require(all(isinstance(v,str) and len(v) <= 128 for v in state),'spec-raw-literal')
        raw = tuple(helper.literal(v) for v in state)
        inputs.append({'id':identifier,'state':[helper.hex_bits(v) for v in raw]})
        value,rejection = None,None
        if not all(helper.finite(v) for v in raw):
            rejection = 'raw-nonfinite'
        elif not all(helper.dyadic(v) > 0 for v in raw[13:17]):
            rejection = 'raw-force'
        else:
            value = helper.prepare_one(raw,constant_bits,spec['corners'])
            if not helper.preparation_valid(raw,value,constants):
                rejection = 'preparation'
            else:
                exact[identifier] = prepared_exact(value,helper)
        prepared.append({'id':identifier,'value':value,'rejection':rejection})
    planned = 4*len(ids)*(len(ids)-1)
    target = {'id':name,'input':{'drones':inputs},'prepared':prepared,'exact':exact,
              'planned':planned,'pairs':[],'lookup':{},'order':[],
              'expectedClass':scene['expectedClass'],'tree':None,'globalGuard':None}
    first_bad = next((v for v in prepared if v['rejection'] is not None),None)
    target['globalInvalid'] = first_bad is not None
    if first_bad is not None:
        target.update(status='rejected',branch=first_bad['rejection'],witness={'id':first_bad['id']})
    else:
        for item in prepared:
            p = item['value']
            geometry.append({'center':helper.exact_vector(p['center']),
                             'axis':helper.exact_vector(p['axis']),
                             'points':[helper.exact_vector(point) for point in p['points']]})
        target['geometry'] = geometry
        target['globalGuard'],target['guardEvidence'] = global_guard(geometry)
        if target['globalGuard']['passed']:
            target['tree'],target['members'],target['boxes'] = reconstruct_tree(geometry,ids)
        order_indices = sorted(range(len(ids)),key=lambda i:(-geometry[i]['center'][2],ids[i]))
        target['order'] = [ids[i] for i in order_indices]
        ranks = {identifier:index for index,identifier in enumerate(target['order'])}
        for receiver,drone in enumerate(inputs):
            for rotor in range(4):
                for source,other in enumerate(inputs):
                    if receiver == source:
                        continue
                    oracle_full = helper.oracle_case({'id':name,'input':{'receiver':drone['state'],
                        'source':other['state'],'self':False,'rotor':rotor}},constant_bits,spec['corners'])
                    oracle = {'status':oracle_full['status'],'branch':oracle_full['branch']}
                    pair = {'i':ids[receiver],'r':rotor,'j':ids[source],
                            'ii':receiver,'jj':source,'oracle':oracle}
                    if oracle['status'] == 'positive':
                        # One outward fixed192 quantization; do not retain a second
                        # unquantized reference or a rounded coefficient midpoint.
                        pair['coefficient'] = quantize(oracle_full['referenceIntervals']['coefficient'],192)
                    target['pairs'].append(pair)
                    target['lookup'][(receiver,rotor,source)] = pair
        rejected = next((p for p in target['pairs'] if p['oracle']['status'] == 'rejected'),None)
        uncertain = next((p for p in target['pairs'] if p['oracle']['status'] == 'reference-undecidable'),None)
        wrong = next((p for p in target['pairs'] if p['oracle']['status'] == 'positive' and
                      ranks[p['j']] >= ranks[p['i']]),None)
        positives = sum(p['oracle']['status'] == 'positive' for p in target['pairs'])
        if rejected is not None:
            target.update(status='rejected',branch='pair-'+rejected['oracle']['branch'],
                          witness={k:rejected[k] for k in ('i','r','j')})
        elif uncertain is not None:
            target.update(status='reference-undecidable',branch='pair-'+uncertain['oracle']['branch'],
                          witness={k:uncertain[k] for k in ('i','r','j')})
        elif wrong is not None:
            target.update(status='rejected',branch='ordering',witness={k:wrong[k] for k in ('i','r','j')})
        elif positives > spec['positiveTermCap']:
            target.update(status='resource',branch='positive-term-budget',witness=None)
        else:
            target.update(status='admitted',branch='loads',witness=None)
            target['roots'],target['loads'] = reference_roots(target)
    target['referenceClass'] = ('admitted' if target['status'] == 'admitted' else
                                target['status']+':'+target['branch'])
    target['plans'] = {method:assembly_plan(target,method,constants) for method in ('complete','hierarchy')}
    return target

def validate_tree_wire(value,target):
    fields(value,('permutation','nodes'),'tree-fields')
    sequence(value['permutation'],len(target['input']['drones']),'tree-permutation-count')
    sequence(value['nodes'],len(target['tree']['nodes']),'tree-node-count')
    for node in value['nodes']:
        fields(node,('id','start','end','left','right','center','axis'),'tree-node-fields')
        require(compact_bytes(node) <= 8192,'tree-node-byte-budget')
        for name in ('center','axis'):
            for interval in sequence(node[name],3,'tree-vector-count'):
                lower,upper = sequence(interval,2,'tree-interval-count')
                for endpoint in (lower,upper):
                    fields(endpoint,('n','d'),'tree-rational-fields')
                    require(isinstance(endpoint['n'],str) and len(endpoint['n']) <= 310 and
                            isinstance(endpoint['d'],str) and len(endpoint['d']) <= 324,
                            'tree-rational-string-budget')
                require(rational(lower,324) <= rational(upper,324),'tree-interval-order')
    require(same_json(value,target['tree']),'tree-operation-graph')


def validate_nonzero(value,pair):
    require(isinstance(value,dict),'nonzero-result-object')
    oracle = pair['oracle']
    require(oracle['status'] != 'reference-undecidable','reference-uncertain-pair')
    require(value.get('status') != 'unresolved','unresolved-not-qualified')
    if oracle['status'] == 'positive':
        fields(value,('status','branch','coefficient'),'positive-result-fields')
        require(value['status'] == 'positive' and value['branch'] == 'active','positive-status')
        coefficient = candidate_interval(value['coefficient'])
        require(coefficient[0] >= 0,'negative-coefficient')
        contains(coefficient,pair['coefficient'],'coefficient-reference-containment')
        return coefficient
    require(oracle['status'] == 'rejected','explicit-nonzero-oracle-zero')
    require(same_json(value,oracle),'rejected-pair-status-branch')
    return None


def validate_assembly(assembly,target,method,constants):
    fields(assembly,('mode','globalGuard','tree','queries','work'),'assembly-fields')
    plan = target['plans'][method]
    require(same_json(assembly['globalGuard'],plan['globalGuard']),'global-guard-operation-graph')
    require(assembly['mode'] == plan['mode'],'assembly-mode')
    if plan['tree'] is None:
        require(assembly['tree'] is None,'unexpected-tree')
    else:
        validate_tree_wire(assembly['tree'],target)
    queries = sequence(assembly['queries'],len(plan['queries']),'query-count')
    saved_pairs = {}
    coverage_count = 0
    for query,reference_query in zip(queries,plan['queries']):
        fields(query,('i','r','terminals'),'query-fields')
        require(type(query['i']) is int and query['i'] == reference_query['i'] and
                type(query['r']) is int and query['r'] == reference_query['r'],'query-index-or-order')
        receiver,rotor = query['i'],query['r']
        terminals = sequence(query['terminals'],len(reference_query['terminals']),'terminal-count')
        covered = []
        for terminal,reference_terminal in zip(terminals,reference_query['terminals']):
            require(isinstance(terminal,dict),'terminal-object')
            kind = terminal.get('kind')
            require(kind in ('zero','leaf','scan'),'terminal-kind')
            if kind == 'scan':
                fields(terminal,('kind','entries','zeroCount'),'scan-fields')
                require(plan['mode'] in ('complete','fallback'),'scan-in-screened-mode')
                members = tuple(j for j in range(len(target['input']['drones'])) if j != receiver)
            else:
                fields(terminal,('kind','node','rule','count') if kind == 'zero' else
                       ('kind','node','entries','zeroCount'),'tree-terminal-fields')
                require(plan['mode'] == 'hierarchy','tree-terminal-without-global-proof')
                node_id = integer(terminal['node'],0,len(target['tree']['nodes'])-1,'terminal-node-id')
                members = tuple(sorted(j for j in target['members'][node_id] if j != receiver))
                if kind == 'zero':
                    proven_rule,_ = zero_rule(target['boxes'][node_id],target['geometry'][receiver],rotor,constants)
                    require(terminal['rule'] in RULES and terminal['rule'] == proven_rule,'node-zero-rule')
                    require(all(target['lookup'][(receiver,rotor,j)]['oracle']['status'] == 'zero'
                                for j in members),'node-zero-oracle-member')
                    require(type(terminal['count']) is int and terminal['count'] == len(members),'node-zero-count')
                else:
                    require(target['tree']['nodes'][node_id]['left'] is None,'nonleaf-scalar-terminal')
            covered.extend(members)
            require(kind == reference_terminal['kind'] and
                    (kind == 'scan' or terminal['node'] == reference_terminal['node']),
                    'terminal-canonical-traversal')
            if kind == 'zero':
                continue
            entries = terminal['entries']
            require(isinstance(entries,list) and len(entries) <= len(members),'entry-count')
            seen,previous = set(),-1
            for entry in entries:
                fields(entry,('j','result'),'entry-fields')
                require(compact_bytes(entry) <= 384,'entry-byte-budget')
                source = integer(entry['j'],0,len(target['input']['drones'])-1,'entry-source-index')
                require(source in members and source not in seen and source > previous,'entry-membership-or-order')
                seen.add(source)
                previous = source
                pair = target['lookup'][(receiver,rotor,source)]
                coefficient = validate_nonzero(entry['result'],pair)
                key = (receiver,rotor,source)
                require(key not in saved_pairs,'duplicate-singleton')
                saved_pairs[key] = {'result':entry['result'],'coefficient':coefficient}
            require(type(terminal['zeroCount']) is int and terminal['zeroCount'] == len(members)-len(entries),
                    'implicit-zero-count')
            for source in members:
                if source not in seen:
                    require(target['lookup'][(receiver,rotor,source)]['oracle']['status'] == 'zero',
                            'implicit-zero-nonzero')
        require(sorted(covered) == [j for j in range(len(target['input']['drones'])) if j != receiver],
                'source-partition-incomplete-or-overlap')
        coverage_count += len(covered)
    require(coverage_count == (0 if target['globalInvalid'] else target['planned']),'accounted-pair-count')
    require(same_json(assembly['work'],plan['work']),'work-counter-reconstruction')
    coefficients,canonical_positive = [],[]
    for pair in target['pairs']:
        saved = saved_pairs.get((pair['ii'],pair['r'],pair['jj']))
        if pair['oracle']['status'] == 'positive':
            require(saved is not None and saved['coefficient'] is not None,'missing-positive-singleton')
            coefficients.append(saved['coefficient'])
            canonical_positive.append({'i':pair['i'],'r':pair['r'],'j':pair['j'],
                                       'coefficient':saved['result']['coefficient']})
        else:
            coefficients.append(None)
    return coefficients,canonical_positive,coverage_count


def validate_method(value,target,method,constants,helper,emit_reference):
    fields(value,('name','prepared','assembly','result','solve','certificate'),'method-fields')
    require(value['name'] == method,'method-name-or-order')
    require(same_json(value['prepared'],target['prepared']),'prepared-operation-graph')
    fields(value['result'],('status','branch','witness','toleranceAchieved'),'result-fields')
    coefficients,canonical_positive,coverage = validate_assembly(value['assembly'],target,method,constants)
    result = {'name':method,'mode':target['plans'][method]['mode'],
              'work':target['plans'][method]['work'],'zeroRuleCounts':target['plans'][method]['rules'],
              'accountedPairs':coverage,'positiveCoefficientRecords':len(canonical_positive),
              'verified':True,'toleranceAchieved':None}
    if target['status'] == 'admitted':
        require(isinstance(value['certificate'],dict),'certificate-object')
        for row in value['certificate'].get('rows',[]):
            require(compact_bytes(row) <= 1024,'certificate-row-byte-budget')
        for load in value['certificate'].get('loads',[]):
            require(compact_bytes(load) <= 12288,'load-record-byte-budget')
        result.update(validate_certificate(value,target,coefficients,helper,constants,emit_reference))
    else:
        require(target['status'] != 'reference-undecidable','reference-scene-uncertain')
        require(same_json(value['result'],{'status':target['status'],'branch':target['branch'],
                'witness':target['witness'],'toleranceAchieved':None}),'canonical-model-refusal')
        require(value['solve'] is None and value['certificate'] is None,'refusal-payload')
    return result,canonical_positive


