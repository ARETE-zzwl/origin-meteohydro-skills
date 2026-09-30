"""Scientific boundary checks: reject deceptive encodings, preserve valid inputs."""
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

from check_plot_table import check


class PlotTableTests(unittest.TestCase):
    def test_examples_are_valid_and_unchanged(self):
        root = Path(__file__).resolve().parents[1] / 'assets' / 'journal_examples'
        for kind in ['reliability', 'fdc', 'composite', 'portrait']:
            data = pd.read_csv(root / (kind + '.csv'))
            original = data.copy(deep=True)
            self.assertEqual(check(data, kind)['status'], 'TABLE_CHECKS_PASSED')
            pd.testing.assert_frame_equal(data, original)

    def reliability(self):
        return pd.DataFrame({'bin_left': [0, .5], 'bin_right': [.5, 1],
                             'mean_probability': [.25, np.nan],
                             'event_frequency': [.2, np.nan], 'n': [20, 0]})

    def test_empty_bin_must_not_be_encoded_as_zero(self):
        data = self.reliability()
        data.loc[1, ['mean_probability', 'event_frequency']] = 0
        with self.assertRaisesRegex(ValueError, 'Empty bins'):
            check(data, 'reliability')

    def test_reliability_probability_and_support_constraints(self):
        for column, value in [('event_frequency', 1.2), ('mean_probability', .8),
                              ('n', 2.5), ('n', -1), ('event_frequency', np.nan)]:
            data = self.reliability()
            data[column] = data[column].astype(float)
            data.loc[0, column] = value
            with self.assertRaises(ValueError):
                check(data, 'reliability')

    def test_overlapping_bins_rejected(self):
        data = self.reliability()
        data.loc[1, 'bin_left'] = .4
        with self.assertRaisesRegex(ValueError, 'overlapping'):
            check(data, 'reliability')

    def test_fdc_zero_flow_preserved_but_not_log_compatible(self):
        data = pd.DataFrame({'exceedance_pct': [10, 50, 90], 'discharge': [8, 3, 0]})
        self.assertFalse(check(data, 'fdc')['log_y_compatible'])
        self.assertEqual(data.discharge.iloc[-1], 0)

    def test_fdc_reversed_probability_and_negative_flow_rejected(self):
        for p, q in [([90, 50, 10], [8, 3, 1]), ([10, 50, 90], [1, 3, 8]),
                     ([10, 50, 90], [8, 3, -1]), ([0, 50, 100], [8, 3, 1])]:
            with self.assertRaises(ValueError):
                check(pd.DataFrame({'exceedance_pct': p, 'discharge': q}), 'fdc')

    def test_point_estimate_outside_interval_is_preserved(self):
        data = pd.DataFrame({'lag': [0], 'estimate': [2.0], 'lo': [3.0], 'hi': [4.0], 'n': [12]})
        check(data, 'composite')
        self.assertEqual(data.estimate.iloc[0], 2)

    def test_unsupported_lag_and_reversed_interval_rejected(self):
        for n, lo, hi in [(0, 0, 2), (12, 3, 2)]:
            data = pd.DataFrame({'lag': [0], 'estimate': [1], 'lo': [lo], 'hi': [hi], 'n': [n]})
            with self.assertRaises(ValueError):
                check(data, 'composite')

    def test_portrait_duplicate_and_missing_zero_rejected(self):
        data = pd.DataFrame({'model': ['A'], 'metric': ['NSE'], 'reference': ['obs'],
                             'value': [-2], 'better': ['higher'], 'status': ['available']})
        check(data, 'portrait')  # Negative skill values must remain valid.
        with self.assertRaisesRegex(ValueError, 'Duplicate'):
            check(pd.concat([data, data]), 'portrait')
        data.loc[0, 'status'] = 'missing'
        data.loc[0, 'value'] = 0
        with self.assertRaisesRegex(ValueError, 'Missing cells'):
            check(data, 'portrait')


if __name__ == '__main__':
    unittest.main()
