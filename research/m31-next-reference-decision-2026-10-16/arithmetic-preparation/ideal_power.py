"""Pure Decimal reference for a specified ideal axial actuator-disk formula.

No data, files, network, clocks, subprocesses or experimental runner are accessed.
Importing this module defines callables; it performs no formula evaluation.
"""

from dataclasses import dataclass
from decimal import (
    Context,
    Decimal,
    DivisionByZero,
    FloatOperation,
    InvalidOperation,
    Overflow,
    ROUND_HALF_EVEN,
    Underflow,
    localcontext,
)


SUPPORTED_PRECISIONS = (80, 120)
AGREEMENT_TOLERANCE = Decimal("1e-50")


def _context(digits: int) -> Context:
    """Use fresh settings, independent of the caller's precision and traps."""
    return Context(
        prec=digits,
        rounding=ROUND_HALF_EVEN,
        Emin=-999999,
        Emax=999999,
        capitals=1,
        clamp=0,
        traps=[InvalidOperation, DivisionByZero, Overflow, Underflow, FloatOperation],
    )


def _precision(precision: int) -> None:
    if type(precision) is not int or precision not in SUPPORTED_PRECISIONS:
        raise ValueError("precision must be the integer 80 or 120")


def _nonnegative_decimal(value: Decimal, name: str) -> None:
    if type(value) is not Decimal:
        raise TypeError(name + " must be Decimal; binary floats are not accepted")
    if not value.is_finite() or value < 0:
        raise ValueError(name + " must be finite and nonnegative")


def _arctan_reciprocal(inverse: int, cutoff: Decimal, max_terms: int) -> Decimal:
    """Alternating arctan series in the active, isolated working context."""
    x = Decimal(1) / Decimal(inverse)
    minus_x_squared = -(x * x)
    numerator = x
    total = x
    for index in range(1, max_terms):
        numerator *= minus_x_squared
        term = numerator / Decimal(2 * index + 1)
        total += term
        if term.copy_abs() < cutoff:
            return total
    raise ArithmeticError("Fixed synthetic-reference arctan series did not converge")


def _machin_pi(digits: int) -> Decimal:
    """pi = 16 atan(1/5) - 4 atan(1/239), with 16 guard digits."""
    with localcontext(_context(digits + 16)):
        cutoff = Decimal(1).scaleb(-(digits + 10))
        terms = 4 * digits + 64
        value = (
            Decimal(16) * _arctan_reciprocal(5, cutoff, terms)
            - Decimal(4) * _arctan_reciprocal(239, cutoff, terms)
        )
    with localcontext(_context(digits)):
        return +value


def pi_decimal(precision: int = 120) -> Decimal:
    """Return a computed pi approximation at 80 or 120 significant digits."""
    _precision(precision)
    return _machin_pi(precision)


def ideal_power_coefficient(
    thrust_coefficient: Decimal,
    advance_ratio: Decimal,
    precision: int = 120,
) -> Decimal:
    """Evaluate CT * (J/2 + sqrt(J**2/4 + 2*CT/pi)).

    Inputs must be exact Decimal objects created from retained decimal text,
    never from a binary float. The mathematical domain is CT >= 0 and J >= 0;
    CT = 0 is an elementary boundary case, not an eligible measured row under
    the proposed positive-thrust study. Signed zero is treated as zero.

    Work uses 32 guard digits before rounding to the requested significant
    digits. Exceptional exponent range/underflow failures propagate; callers
    must retain a numerical-reference failure rather than rescale or retry.
    No claim of a certified end-to-end rounding-error bound is made.
    """
    _precision(precision)
    _nonnegative_decimal(thrust_coefficient, "thrust_coefficient")
    _nonnegative_decimal(advance_ratio, "advance_ratio")
    if thrust_coefficient.is_zero():
        return Decimal(0)
    with localcontext(_context(precision + 32)) as context:
        half_j = advance_ratio / Decimal(2)
        pi = _machin_pi(precision + 32)
        radicand = half_j * half_j + Decimal(2) * thrust_coefficient / pi
        result = thrust_coefficient * (half_j + radicand.sqrt(context=context))
    with localcontext(_context(precision)):
        return +result


@dataclass(frozen=True)
class DecimalReferencePair:
    cp_80: Decimal
    cp_120: Decimal
    absolute_difference: Decimal
    agreement_tolerance: Decimal
    agreement_passed: bool


def reference_pair(thrust_coefficient: Decimal, advance_ratio: Decimal) -> DecimalReferencePair:
    """Retain both fixed-precision outputs and the proposed 1e-50 screen.

    This comparison is arithmetic reproducibility evidence for one formula.
    It neither validates coefficient conventions nor certifies physical truth.
    """
    cp_80 = ideal_power_coefficient(thrust_coefficient, advance_ratio, 80)
    cp_120 = ideal_power_coefficient(thrust_coefficient, advance_ratio, 120)
    with localcontext(_context(160)):
        difference = (cp_80 - cp_120).copy_abs()
    return DecimalReferencePair(
        cp_80=cp_80,
        cp_120=cp_120,
        absolute_difference=difference,
        agreement_tolerance=AGREEMENT_TOLERANCE,
        agreement_passed=difference <= AGREEMENT_TOLERANCE,
    )
