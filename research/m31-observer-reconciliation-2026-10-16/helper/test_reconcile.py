"""Deterministic synthetic tests. No live processes or legacy runner imports."""

from dataclasses import FrozenInstanceError
import unittest

from reconcile import Observation, Row, Snapshot, ValidatedCoverage, reconcile


def coverage(snapshot, *groups):
    return ValidatedCoverage(snapshot, frozenset(groups))


class ReconciliationTests(unittest.TestCase):
    def setUp(self):
        self.snapshot = Snapshot("capture-1", (
            Row(10, 1, 10), Row(20, 10, 20), Row(21, 20, 20),
        ))

    def test_late_registration_on_same_snapshot(self):
        result = reconcile(coverage(self.snapshot, 10), coverage(self.snapshot, 10, 20), ())
        self.assertEqual(tuple(o.row.pid for o in result.covered_after_refresh), (20, 21))
        self.assertEqual(result.still_unadmitted, ())
        self.assertEqual(result.ledger, ())
        self.assertTrue(result.closure_permitted(True))
        self.assertFalse(result.closure_permitted(False))

    def test_still_unadmitted_is_retained_and_vetoes_closure(self):
        result = reconcile(coverage(self.snapshot, 10), coverage(self.snapshot, 10), ())
        self.assertEqual(result.ledger, tuple(Observation("capture-1", r) for r in self.snapshot.rows[1:]))
        self.assertEqual(result.still_unadmitted, result.ledger)
        self.assertEqual(result.covered_after_refresh, ())
        self.assertFalse(result.closure_permitted(True))

    def test_failed_or_unavailable_refresh_preserves_prior_coverage(self):
        result = reconcile(coverage(self.snapshot, 10), None, ())
        self.assertFalse(result.refresh_available)
        self.assertEqual(tuple(o.row.pid for o in result.ledger), (20, 21))
        self.assertNotIn(10, tuple(o.row.pid for o in result.ledger))

    def test_partial_refresh_cannot_clear_unadmitted_nested_group(self):
        snapshot = Snapshot("nested", self.snapshot.rows + (Row(30, 21, 30), Row(31, 30, 31)))
        result = reconcile(coverage(snapshot, 10), coverage(snapshot, 20), ())
        self.assertEqual(tuple(o.row.pid for o in result.covered_after_refresh), (20, 21))
        self.assertEqual(tuple(o.row.pid for o in result.ledger), (30, 31))

    def test_refreshed_group_also_seeds_recursive_descendant_check(self):
        snapshot = Snapshot("reparented", (Row(20, 1, 20), Row(30, 20, 30)))
        result = reconcile(coverage(snapshot, 10), coverage(snapshot, 20), ())
        self.assertEqual(tuple(o.row.pid for o in result.covered_after_refresh), (20,))
        self.assertEqual(tuple(o.row.pid for o in result.ledger), (30,))

    def test_unrelated_group_is_not_invented_as_descendant(self):
        snapshot = Snapshot("unrelated", self.snapshot.rows + (Row(99, 1, 99),))
        result = reconcile(coverage(snapshot, 10), coverage(snapshot, 10), ())
        self.assertEqual(tuple(o.row.pid for o in result.ledger), (20, 21))

    def test_later_exact_coverage_never_clears_prior_taint(self):
        first = reconcile(coverage(self.snapshot, 10), coverage(self.snapshot, 10), ())
        later = Snapshot("capture-2", self.snapshot.rows)
        result = reconcile(coverage(later, 10, 20), coverage(later, 10, 20), first.ledger)
        self.assertEqual(result.still_unadmitted, ())
        self.assertEqual(result.ledger, first.ledger)
        self.assertFalse(result.closure_permitted(True))

    def test_later_absence_never_clears_prior_taint(self):
        first = reconcile(coverage(self.snapshot, 10), None, ())
        empty = Snapshot("capture-empty", ())
        result = reconcile(coverage(empty), coverage(empty), first.ledger)
        self.assertEqual(result.ledger, first.ledger)
        self.assertFalse(result.closure_permitted(True))

    def test_reused_numeric_ids_cannot_clear_or_relabel_old_observation(self):
        first = reconcile(coverage(self.snapshot, 10), None, ())
        reused = Snapshot("reused-numbers", (Row(20, 1, 20), Row(21, 20, 20)))
        result = reconcile(coverage(reused, 20), coverage(reused, 20), first.ledger)
        self.assertEqual(result.ledger, first.ledger)
        self.assertTrue(all(o.snapshot_label == "capture-1" for o in result.ledger))
        self.assertFalse(result.closure_permitted(True))

    def test_append_preserves_every_previous_record(self):
        first = reconcile(coverage(self.snapshot, 10), None, ())
        later = Snapshot("capture-2", (Row(10, 1, 10), Row(30, 10, 30)))
        result = reconcile(coverage(later, 10), None, first.ledger)
        self.assertEqual(result.ledger, first.ledger + (Observation("capture-2", later.rows[1]),))
        self.assertEqual(len(first.ledger), 2)

    def test_no_ledger_truncation_or_capacity_clearing(self):
        old = tuple(Observation(f"capture-{n}", Row(20, 10, 20)) for n in range(4096))
        result = reconcile(coverage(self.snapshot, 10), None, old)
        self.assertEqual(result.ledger[:4096], old)
        self.assertEqual(len(result.ledger), 4098)
        self.assertFalse(result.closure_permitted(True))

    def test_different_snapshot_rejected_even_if_label_reused(self):
        changed = Snapshot("capture-1", (Row(20, 1, 20),))
        with self.assertRaises(ValueError):
            reconcile(coverage(self.snapshot, 10), coverage(changed, 20), ())

    def test_immutable_inputs_and_output(self):
        before = coverage(self.snapshot, 10)
        result = reconcile(before, None, ())
        with self.assertRaises(FrozenInstanceError):
            self.snapshot.rows[0].pgid = 20
        with self.assertRaises(FrozenInstanceError):
            before.groups = frozenset({20})
        with self.assertRaises(FrozenInstanceError):
            result.ledger = ()
        with self.assertRaises(FrozenInstanceError):
            result.ledger[0].snapshot_label = "changed"
        self.assertEqual(before.groups, frozenset({10}))
        self.assertEqual(self.snapshot.rows[0], Row(10, 1, 10))

    def test_mutable_or_malformed_input_rejected(self):
        with self.assertRaises(TypeError):
            Snapshot("mutable", list(self.snapshot.rows))
        with self.assertRaises(TypeError):
            ValidatedCoverage(self.snapshot, {10})
        with self.assertRaises(TypeError):
            reconcile(coverage(self.snapshot, 10), None, [])
        with self.assertRaises(TypeError):
            Observation("mutable", [20, 10, 20])
        with self.assertRaises(ValueError):
            Snapshot("duplicate", (Row(10, 1, 10), Row(10, 2, 20)))
        with self.assertRaises(TypeError):
            Row(True, 1, 10)

    def test_omitted_ledger_is_rejected(self):
        with self.assertRaises(TypeError):
            reconcile(coverage(self.snapshot, 10), None)


if __name__ == "__main__":
    unittest.main()
