"""Pure retained-snapshot classification; no process control or evidence acquisition."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Row:
    pid: int
    ppid: int
    pgid: int

    def __post_init__(self):
        if any(type(n) is not int for n in (self.pid, self.ppid, self.pgid)):
            raise TypeError("Process identifiers must be integers")
        if self.pid <= 0 or self.ppid < 0 or self.pgid <= 0:
            raise ValueError("Invalid process identifier")


@dataclass(frozen=True)
class Snapshot:
    label: str  # Evidence label only; NOT a process-instance identity token.
    rows: tuple[Row, ...]

    def __post_init__(self):
        if type(self.label) is not str or not self.label:
            raise ValueError("A nonempty snapshot label is required")
        if type(self.rows) is not tuple or any(type(r) is not Row for r in self.rows):
            raise TypeError("Snapshot rows must be an immutable tuple of Row values")
        if len({r.pid for r in self.rows}) != len(self.rows):
            raise ValueError("Duplicate PID within one snapshot")


@dataclass(frozen=True)
class ValidatedCoverage:
    """CALLER assertion of exact owned-group coverage for this retained snapshot.

    Neither the assertion nor this helper's result grants permission to signal.
    The helper cannot verify the caller's ownership evidence.
    """

    snapshot: Snapshot
    groups: frozenset[int]

    def __post_init__(self):
        if type(self.snapshot) is not Snapshot or type(self.groups) is not frozenset:
            raise TypeError("Coverage requires an immutable snapshot and frozenset")
        if any(type(g) is not int or g <= 0 for g in self.groups):
            raise ValueError("Invalid covered process group")


@dataclass(frozen=True)
class Observation:
    snapshot_label: str
    row: Row

    def __post_init__(self):
        if type(self.snapshot_label) is not str or not self.snapshot_label:
            raise ValueError("Observation requires its original snapshot label")
        if type(self.row) is not Row:
            raise TypeError("Observation requires an immutable Row value")


@dataclass(frozen=True)
class Reconciliation:
    covered_after_refresh: tuple[Observation, ...]
    still_unadmitted: tuple[Observation, ...]
    ledger: tuple[Observation, ...]
    refresh_available: bool

    def closure_permitted(self, known_group_closure: bool) -> bool:
        """Additional closure gate, not proof of unobserved-process completeness."""
        if type(known_group_closure) is not bool:
            raise TypeError("Known-group closure must be a boolean")
        return known_group_closure and not self.ledger


def reconcile(before: ValidatedCoverage, after: ValidatedCoverage | None,
              ledger: tuple[Observation, ...]) -> Reconciliation:
    """Compare caller-validated coverage on ONE snapshot; append permanent taint.

    ``after=None`` means refresh unavailable/failed; prior coverage is retained.
    Start with (); supply the previous result's entire ledger on every later call.
    No later registration, disappearance, terminal evidence, or numeric-ID match
    discharges a ledger entry. There is deliberately no recovery/discharge API.
    """
    if type(before) is not ValidatedCoverage or (after is not None and type(after) is not ValidatedCoverage):
        raise TypeError("Coverage must be caller-validated immutable values")
    if type(ledger) is not tuple or any(type(o) is not Observation for o in ledger):
        raise TypeError("Ledger must be an immutable tuple of observations")
    if after is not None and after.snapshot != before.snapshot:
        raise ValueError("Both coverage assertions must refer to the same snapshot")
    rows = before.snapshot.rows
    groups = before.groups | (after.groups if after is not None else frozenset())
    reachable = {r.pid for r in rows if r.pgid in groups}
    while True:
        expanded = reachable | {r.pid for r in rows if r.ppid in reachable}
        if expanded == reachable:
            break
        reachable = expanded
    candidates = tuple(Observation(before.snapshot.label, r) for r in rows
                       if r.pid in reachable and r.pgid not in before.groups)
    covered = tuple(o for o in candidates if o.row.pgid in groups)
    unadmitted = tuple(o for o in candidates if o.row.pgid not in groups)
    return Reconciliation(covered, unadmitted, ledger + unadmitted, after is not None)
