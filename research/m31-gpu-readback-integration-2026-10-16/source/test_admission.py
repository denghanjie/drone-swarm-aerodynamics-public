"""Pure in-memory config tests. Never import lifecycle entrypoints."""
import copy
import datetime
import unittest
from admission import admit, LIMITS


class AdmissionTests(unittest.TestCase):
    def setUp(self):
        self.now = datetime.datetime(2030, 1, 1, 0, 0, 5, tzinfo=datetime.timezone.utc)
        self.config = dict(version=1, scope='synthetic-gpu-readback-host', executionAllocated=True,
                           notBeforeUTC='2030-01-01T00:00:00Z', stopNewLaunchUTC='2030-01-01T00:00:10Z',
                           reviewNotBeforeUTC='2030-01-01T00:00:20Z', reviewStopNewLaunchUTC='2030-01-01T00:00:30Z',
                           limits=copy.deepcopy(LIMITS))

    def test_windows_and_boundaries(self):
        self.assertTrue(admit(self.config, 'launch', self.now))
        self.assertTrue(admit(self.config, 'launch', self.now.replace(second=0)))
        self.assertTrue(admit(self.config, 'review', self.now.replace(second=20)))
        for phase, second in [('launch', 10), ('review', 5), ('review', 30)]:
            with self.subTest(phase=phase, second=second), self.assertRaises(ValueError):
                admit(self.config, phase, self.now.replace(second=second))

    def test_disabled_and_invalid_configs(self):
        changes = [('executionAllocated', False), ('executionAllocated', 1), ('version', True),
                   ('scope', 'other'), ('notBeforeUTC', None), ('reviewNotBeforeUTC', None),
                   ('stopNewLaunchUTC', '2030-01-01T00:00:00Z'),
                   ('reviewStopNewLaunchUTC', '2030-01-01T00:00:20Z'),
                   ('notBeforeUTC', '2030-02-30T00:00:00Z'),
                   ('notBeforeUTC', '2030-01-01T00:00:00+00:00'),
                   ('notBeforeUTC', '2030-01-01T00:00:00.000Z')]
        for key, value in changes:
            config = copy.deepcopy(self.config); config[key] = value
            with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                admit(config, 'launch', self.now)

    def test_limits_are_exact_integers(self):
        for value in (True, 60.0, 61):
            config = copy.deepcopy(self.config); config['limits']['wallSeconds'] = value
            with self.subTest(value=value), self.assertRaises(ValueError):
                admit(config, 'launch', self.now)

    def test_phase_and_clock(self):
        with self.assertRaises(ValueError): admit(self.config, 'other', self.now)
        with self.assertRaises(ValueError): admit(self.config, 'launch', self.now.replace(tzinfo=None))


if __name__ == '__main__':
    unittest.main()
