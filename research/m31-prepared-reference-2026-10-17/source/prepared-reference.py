"""Scene-internal prepared-operand adapter; no scientific import at load."""
from fractions import Fraction


PAIR_SHA256 = '845f52cf350a09d2043934dff3e797a7b7416f4ef5c64beb716104bcd74f38f0'
TREE_SHA256 = 'd08efc5e80910066d061a664aa7902c7ae7bab27dc710f5c00c9b2bf1671df65'
COUNTERS = ('prepareOneCalls', 'preparationValidCalls', 'oracleCalls', 'operandLookups',
            'pairPreparations')


class BindingError(Exception):
    """A failed internal operand/context binding, never a scientific decision."""


def need(condition, code):
    if not condition:
        raise BindingError(code)


def snapshot(value):
    """Immutable, type-sensitive snapshots of the small trusted input objects."""
    if isinstance(value, dict):
        return ('dict', tuple(sorted((key, snapshot(item)) for key, item in value.items())))
    if isinstance(value, list):
        return ('list', tuple(snapshot(item) for item in value))
    if isinstance(value, tuple):
        return ('tuple', tuple(snapshot(item) for item in value))
    return (type(value).__name__, value)


class PreparedHelper:
    """Per-scene registry; only frozen preparation can admit an operand.

    original.literal must already implement the caller's decimal/raw-word input
    convention. The other delegated methods must be from the pinned pair module.
    Scientific modules/context verification belongs to the calling driver.
    """
    def __init__(self, original, constant_bits, corners, guard=None, budget=None):
        need(guard is None or callable(guard), 'prepared-guard-shape')
        self.original = original
        self.poll = guard if guard is not None else lambda: None
        self.bits = constant_bits
        self.corners = corners
        self.bits_snapshot = snapshot(constant_bits)
        self.corners_snapshot = snapshot(corners)
        self.constants = {key: original.dyadic(value) for key, value in constant_bits.items()}
        self.constants_snapshot = snapshot(self.constants)
        self.budget = budget if budget is not None else {'oracleCalls': 0, 'limit': 30000}
        need(type(self.budget.get('oracleCalls')) is int and self.budget['oracleCalls'] >= 0
             and type(self.budget.get('limit')) is int and self.budget['limit'] >= 0,
             'prepared-budget-shape')
        self.counts = {key: 0 for key in COUNTERS}
        self.pending = {}
        self.records = {}
        self.vectors = {}
        self.phase = 'preparation'

    def __getattr__(self, name):
        return getattr(self.original, name)

    def _context(self, bits, corners):
        need(self.phase != 'closed', 'prepared-context-closed')
        need(snapshot(self.bits) == self.bits_snapshot
             and snapshot(bits) == self.bits_snapshot, 'prepared-constants-context')
        need(snapshot(self.corners) == self.corners_snapshot
             and snapshot(corners) == self.corners_snapshot, 'prepared-corners-context')
        need(snapshot(self.constants) == self.constants_snapshot, 'prepared-constant-operands')

    def _raw_key(self, raw):
        return tuple(self.original.hex_bits(word) for word in raw)

    def prepare_one(self, raw, constant_bits, corners):
        self.poll()
        self._context(constant_bits, corners)
        need(self.phase == 'preparation', 'prepared-registration-closed')
        need(isinstance(raw, (tuple, list)) and len(raw) == 17
             and all(type(word) is int and 0 <= word < 1 << 64 for word in raw),
             'prepared-raw-word-shape')
        need(all(self.original.finite(word) for word in raw), 'prepared-raw-nonfinite')
        need(all(self.original.dyadic(word) > 0 for word in raw[13:17]), 'prepared-raw-force')
        self.counts['prepareOneCalls'] += 1
        value = self.original.prepare_one(raw, constant_bits, corners)
        key = self._raw_key(raw)
        self.pending[key] = (value, snapshot(value))
        return value

    def preparation_valid(self, raw, value, constants):
        self.poll()
        self._context(self.bits, self.corners)
        need(self.phase == 'preparation', 'prepared-registration-closed')
        need(snapshot(constants) == self.constants_snapshot, 'prepared-validation-constants')
        key = self._raw_key(raw)
        need(key in self.pending, 'prepared-without-original-preparation')
        pending_value, pending_snapshot = self.pending.pop(key)
        need(value is pending_value and snapshot(value) == pending_snapshot,
             'prepared-before-validation-mutated')
        self.counts['preparationValidCalls'] += 1
        valid = self.original.preparation_valid(raw, value, constants)
        if valid:
            # Keep every admitted returned object, including duplicate raw rows,
            # so mutation of an earlier duplicate cannot escape the binding check.
            record = self.records.setdefault(key, {'snapshot': pending_snapshot, 'bindings': []})
            need(record['snapshot'] == pending_snapshot, 'prepared-nondeterministic-prefix')
            record['bindings'].append(value)
            for encoded in ([value['center'], value['axis'], value['forces']]
                            + value['points'] + value['offsets']):
                vector_key = tuple(encoded)
                exact = self.original.exact_vector(encoded)
                need(vector_key not in self.vectors or self.vectors[vector_key] == exact,
                     'prepared-vector-binding')
                self.vectors[vector_key] = exact
        return valid

    def _lookup(self, encoded, side):
        self.counts['operandLookups'] += 1
        key = tuple(encoded)
        need(key in self.records, 'prepared-unregistered-' + side)
        record = self.records[key]
        need(all(snapshot(value) == record['snapshot'] for value in record['bindings']),
             'prepared-operand-mutated')
        return record['bindings'][-1]

    def exact_vector(self, encoded):
        key = tuple(encoded)
        need(key in self.vectors, 'prepared-vector-unregistered')
        return self.vectors[key]

    def oracle_case(self, case, constant_bits, corners):
        self.poll()
        self._context(constant_bits, corners)
        need(not self.pending, 'prepared-incomplete-registration')
        self.phase = 'evaluation'
        prepared = {side: self._lookup(case['input'][side], side)
                    for side in ('receiver', 'source')}
        need(type(self.budget.get('oracleCalls')) is int and self.budget['oracleCalls'] >= 0
             and type(self.budget.get('limit')) is int and self.budget['limit'] >= 0,
             'prepared-budget-shape')
        need(self.budget['oracleCalls'] < self.budget['limit'], 'prepared-oracle-budget')
        self.budget['oracleCalls'] += 1
        self.counts['oracleCalls'] += 1
        return _oracle_suffix(case, prepared, self.constants, self.original, self.exact_vector)

    def close(self):
        self.phase = 'closed'


def run_binding_controls(adapter, target, constant_bits, corners):
    """Six fixed dense-cube-27 binding failures on this live completed context."""
    need(target['id'] == 'dense-cube-27', 'binding-fixed-scene')
    rows = target['input']['drones']
    need(len(rows) == 27 and rows[0]['id'] == 100 and rows[1]['id'] == 101,
         'binding-fixed-row-identities')
    base = {'id': target['id'], 'input': {'receiver': list(rows[0]['state']),
            'source': list(rows[1]['state']), 'self': False, 'rotor': 0}}
    reports = []

    def attempt(identifier, case, bits, rotor_corners, expected):
        before = dict(adapter.counts)
        before_budget = adapter.budget['oracleCalls']
        observed = None
        try:
            adapter.oracle_case(case, bits, rotor_corners)
        except BindingError as error:
            observed = str(error)
        # Unexpected exceptions propagate. A missed binding may execute a suffix,
        # but that actual call remains counted and cannot qualify as a control.
        delta = {key: adapter.counts[key] - before[key] for key in COUNTERS}
        detected = observed == expected and delta['oracleCalls'] == 0
        reports.append({'id': identifier, 'scene': target['id'], 'detected': detected,
                        'expectedReason': expected, 'reason': observed,
                        'reuseCounterDelta': delta,
                        'budgetOracleDelta': adapter.budget['oracleCalls'] - before_budget,
                        'setupPreparationCalls': 0})

    for side, replacement, code in (
            ('receiver', '3ff0000000000000', 'prepared-unregistered-receiver'),
            ('source', '4000000000000000', 'prepared-unregistered-source')):
        case = {'id': base['id'], 'input': {key: list(value) if isinstance(value, list) else value
                                         for key, value in base['input'].items()}}
        need(case['input'][side][0] != replacement, 'binding-fixed-word-already-equal')
        case['input'][side][0] = replacement
        need(tuple(case['input'][side]) not in adapter.records, 'binding-fixed-word-registered')
        attempt('unregistered-' + side, case, constant_bits, corners, code)

    registered = adapter.records[tuple(base['input']['receiver'])]['bindings'][0]
    previous = registered['center'][0]
    need(previous != '3ff0000000000000', 'binding-fixed-prepared-already-equal')
    try:
        registered['center'][0] = '3ff0000000000000'
        attempt('mutated-prepared-center', base, constant_bits, corners, 'prepared-operand-mutated')
    finally:
        registered['center'][0] = previous
    need(snapshot(registered) == adapter.records[tuple(base['input']['receiver'])]['snapshot'],
         'binding-prepared-restoration')

    changed_bits = dict(constant_bits)
    changed_bits['mg'] ^= 1
    attempt('changed-constant-word', base, changed_bits, corners, 'prepared-constants-context')
    changed_corners = [list(row) for row in corners]
    changed_corners[0], changed_corners[1] = changed_corners[1], changed_corners[0]
    need(snapshot(changed_corners) != snapshot(corners), 'binding-fixed-corners-equal')
    attempt('changed-corner-order', base, constant_bits, changed_corners, 'prepared-corners-context')
    adapter.close()
    attempt('closed-context', base, constant_bits, corners, 'prepared-context-closed')
    need(len(reports) == 6, 'binding-control-count')
    return reports


def regenerate_scene(scene, spec, constant_bits, original, semantic, tree,
                     guard=None, budget=None, run_controls=False):
    """Return (target, scientific_reuse_counters, binding_reports).

    The pinned tree dispatcher is unchanged. Counters are copied before optional
    live-context controls; their deltas are recorded separately in each report.
    """
    helper = PreparedHelper(original, constant_bits, spec['corners'], guard, budget)
    try:
        target = tree.regenerate_scene(scene, spec, constant_bits, helper, semantic, guard=guard)
        reuse = dict(helper.counts)
        reports = run_binding_controls(helper, target, constant_bits, spec['corners']) if run_controls else []
        return target, reuse, reports
    finally:
        helper.close()


def _oracle_suffix(case, prepared, c, original, exact_vector):
    """Literal frozen suffix; only exact_vector resolves validated cached vectors."""
    answer = {'id': case['id'], 'input': case['input'], 'prepared': prepared,
              'status': None, 'branch': None}
    dot = original.dot
    require = original.require
    fade_exact = original.fade_exact
    sqrt_enclosure = original.sqrt_enclosure
    positive_product = original.positive_product
    dyadic = original.dyadic
    parse_bits = original.parse_bits

    def finish(status, branch, intervals=None):
        answer['status'], answer['branch'] = status, branch
        if intervals is not None:
            answer['referenceIntervals'] = intervals
        return answer

    if case["input"]["self"]:
        return finish("zero", "self")
    receiver, source = prepared["receiver"], prepared["source"]
    centers = tuple(a - b for a, b in zip(exact_vector(source["center"]),
                                         exact_vector(receiver["center"])))
    if any(abs(v) > 257 for v in centers) or dot(centers, centers) > 512 ** 2:
        return finish("rejected", "center-guard")
    if dot(centers, centers) >= c["neighbor"] ** 2:
        return finish("zero", "neighbor")
    displacement = tuple(a - b for a, b in zip(exact_vector(source["center"]),
                                              exact_vector(receiver["points"][case["input"]["rotor"]])))
    if any(abs(v) > 258 for v in displacement):
        return finish("rejected", "rotor-guard")
    axis = exact_vector(source["axis"])
    down = dot(displacement, axis)
    if abs(down) > 1024:
        return finish("rejected", "down-guard")
    if down <= 0:
        return finish("zero", "upstream")
    if down >= c["downCut"]:
        return finish("zero", "down-cut")
    residual = tuple(d - down * a for d, a in zip(displacement, axis))
    radial_squared = dot(residual, residual)
    if radial_squared > 2048 ** 2:
        return finish("rejected", "radial-guard")
    if down < c["minDown"] * c["D"]:
        if radial_squared < c["nearRad"] ** 2:
            return finish("rejected", "near")
        return finish("zero", "near-outside")
    height = down / c["D"] - c["origin"]
    width = c["spread"] * height * c["D"]
    if width <= 0 or height <= 0:
        return finish("rejected", "width")
    if radial_squared >= (c["radCut"] * width) ** 2:
        return finish("zero", "radial")
    projection = max(Fraction(0), dot(exact_vector(receiver["axis"]), axis))
    if projection == 0:
        return finish("zero", "projection")
    xi_squared = radial_squared / (width * width)
    rational_profile = (c["decay"] / height / (1 + c["kappa"] * xi_squared) ** 2
                        * c["induced"] * projection
                        * fade_exact(down, c["downFade"], c["downCut"]))
    require(rational_profile > 0, "reference-positive-profile")
    xi = sqrt_enclosure(xi_squared)
    fade = (fade_exact(xi[1], c["radFade"], c["radCut"]),
            fade_exact(xi[0], c["radFade"], c["radCut"]))
    K = (rational_profile * fade[0], rational_profile * fade[1])
    nominal_total = sum(exact_vector(source["forces"]), Fraction(0))
    beta = sqrt_enclosure(nominal_total / c["mg"])
    scaled_K = positive_product(K, beta)
    intervals = {"K": K, "scaledK": scaled_K, "beta": beta}
    if K[0] > 128 or scaled_K[0] > 128:
        return finish("rejected", "cap", intervals)
    if K[1] > 128 or scaled_K[1] > 128:
        return finish("reference-undecidable", "cap", intervals)
    receiver_force = dyadic(parse_bits(receiver["forces"][case["input"]["rotor"]]))
    # This denominator is exact-real, unlike the rounded induced graph above.
    nu = sqrt_enclosure(receiver_force / (2 * c["rho"] * c["A"]))
    intervals["nu"] = nu
    if nu[0] <= 0:
        return finish("reference-undecidable", "normalizer", intervals)
    intervals["coefficient"] = (scaled_K[0] / nu[1], scaled_K[1] / nu[0])
    return finish("positive", "active", intervals)
