"""Elementary synthetic tests only. No measured row or dataset is accessed."""

import json
import sys
import unittest
from decimal import Decimal, Inexact, ROUND_DOWN, getcontext, localcontext

sys.dont_write_bytecode = True
from ideal_power import ideal_power_coefficient, pi_decimal, reference_pair


# Mathematical test constant only, not used by the implementation.
KNOWN_PI = Decimal(
    "3.14159265358979323846264338327950288419716939937510"
    "582097494459230781640628620899862803482534211706798"
    "214808651328230664709384460955058223172535940812848"
)


def rounded(value, precision):
    with localcontext() as context:
        context.prec = precision
        return +value


class IdealPowerSyntheticTests(unittest.TestCase):
    def test_machin_pi_matches_independent_decimal_expansion(self):
        for precision in (80, 120):
            self.assertEqual(pi_decimal(precision), rounded(KNOWN_PI, precision))

    def test_zero_thrust_boundary(self):
        for ct in (Decimal("0"), Decimal("-0")):
            for j in (Decimal("0"), Decimal("2")):
                self.assertEqual(ideal_power_coefficient(ct, j, 80), Decimal(0))

    def test_constructed_static_solution(self):
        with localcontext() as context:
            context.prec = 160
            ct = KNOWN_PI / 2
        # J = 0 and CT = pi/2 imply induced speed coefficient = 1.
        for precision in (80, 120):
            self.assertEqual(ideal_power_coefficient(ct, Decimal(0), precision), rounded(ct, precision))

    def test_constructed_forward_solution(self):
        with localcontext() as context:
            context.prec = 160
            ct = KNOWN_PI / 2
        # J = 3/2 and induced speed coefficient = 1/2 give CP = pi.
        for precision in (80, 120):
            self.assertEqual(ideal_power_coefficient(ct, Decimal("1.5"), precision), rounded(KNOWN_PI, precision))

    def test_static_momentum_identity(self):
        for precision in (80, 120):
            ct = Decimal("0.25")
            cp = ideal_power_coefficient(ct, Decimal(0), precision)
            with localcontext() as context:
                context.prec = 160
                residual = abs(cp * cp - 2 * ct ** 3 / KNOWN_PI)
                tolerance = Decimal(1).scaleb(-precision + 1)
            self.assertLess(residual, tolerance)

    def test_homogeneous_velocity_scaling(self):
        # CT -> s^2 CT, J -> s J gives CP -> s^3 CP.
        for precision in (80, 120):
            base = ideal_power_coefficient(Decimal("0.25"), Decimal("0.5"), precision)
            scaled = ideal_power_coefficient(Decimal("1"), Decimal("1"), precision)
            with localcontext() as context:
                context.prec = 160
                residual = abs(scaled - 8 * base)
                tolerance = Decimal(1).scaleb(-precision + 1)
            self.assertLess(residual, tolerance)

    def test_monotonicity_and_useful_power_lower_limit(self):
        ct, j = Decimal("0.25"), Decimal("0.5")
        cp = ideal_power_coefficient(ct, j)
        self.assertGreater(cp, ct * j)
        self.assertGreater(ideal_power_coefficient(ct * 2, j), cp)
        self.assertGreater(ideal_power_coefficient(ct, j * 2), cp)

    def test_pair_retains_two_precisions_and_passes_small_synthetic_values(self):
        for ct, j in (("0.25", "0"), ("0.5", "2"), ("1e-50", "1e-50")):
            pair = reference_pair(Decimal(ct), Decimal(j))
            self.assertEqual(pair.cp_80, ideal_power_coefficient(Decimal(ct), Decimal(j), 80))
            self.assertEqual(pair.cp_120, ideal_power_coefficient(Decimal(ct), Decimal(j), 120))
            self.assertLessEqual(pair.absolute_difference, Decimal("1e-50"))
            self.assertTrue(pair.agreement_passed)

    def test_absolute_agreement_screen_can_fail_without_rescaling(self):
        # Deliberately enormous synthetic coefficients exercise the fixed absolute gate.
        pair = reference_pair(Decimal("1e80"), Decimal("1e40"))
        self.assertGreater(pair.absolute_difference, Decimal("1e-50"))
        self.assertFalse(pair.agreement_passed)
        self.assertTrue(pair.cp_80.is_finite() and pair.cp_120.is_finite())

    def test_negative_or_nonfinite_domain_is_rejected(self):
        for bad in (Decimal("-1"), Decimal("NaN"), Decimal("sNaN"), Decimal("Infinity"), Decimal("-Infinity")):
            with self.assertRaises(ValueError):
                ideal_power_coefficient(bad, Decimal(0))
            with self.assertRaises(ValueError):
                ideal_power_coefficient(Decimal(1), bad)

    def test_nondecimal_inputs_are_rejected(self):
        for bad in (0.25, 1, True, "0.25", None):
            with self.assertRaises(TypeError):
                ideal_power_coefficient(bad, Decimal(0))
            with self.assertRaises(TypeError):
                ideal_power_coefficient(Decimal(1), bad)

    def test_only_prespecified_precisions_are_accepted(self):
        for bad in (28, 79, 81, 121, True, 80.0, "80", None):
            with self.assertRaises(ValueError):
                ideal_power_coefficient(Decimal(1), Decimal(0), bad)
            with self.assertRaises(ValueError):
                pi_decimal(bad)

    def test_ambient_context_cannot_change_reference_or_receive_flags(self):
        expected = reference_pair(Decimal("0.25"), Decimal("0.5"))
        with localcontext() as ambient:
            ambient.prec = 7
            ambient.rounding = ROUND_DOWN
            ambient.traps[Inexact] = True
            ambient.clear_flags()
            before = (ambient.prec, ambient.rounding, dict(ambient.traps), dict(ambient.flags))
            self.assertEqual(reference_pair(Decimal("0.25"), Decimal("0.5")), expected)
            after = (ambient.prec, ambient.rounding, dict(ambient.traps), dict(ambient.flags))
            self.assertEqual(before, after)


if __name__ == "__main__":
    result = unittest.TextTestRunner(verbosity=2).run(
        unittest.defaultTestLoader.loadTestsFromTestCase(IdealPowerSyntheticTests)
    )
    print(json.dumps({
        "kind": "ideal-power-pure-synthetic-test-results",
        "testsRun": result.testsRun,
        "failures": len(result.failures),
        "errors": len(result.errors),
        "measuredRowsRead": 0,
        "measuredRowFormulaEvaluations": 0,
        "networkInvocations": 0,
        "browserInvocations": 0,
        "gpuInvocations": 0,
    }, sort_keys=True))
    raise SystemExit(0 if result.wasSuccessful() else 1)
