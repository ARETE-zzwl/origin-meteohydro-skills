import tempfile
import unittest
from pathlib import Path

import numpy as np

from palette_tools import parse_rgb, write_pal, read_pal, select_colors, validate_levels, ci_segments


class PaletteTests(unittest.TestCase):
    def test_ncl_header_and_integer_rgb(self):
        data = parse_rgb('# table\nncolors = 2\n255 0 0\n0 255 10', scale=255)
        np.testing.assert_array_equal(data, [[255, 0, 0], [0, 255, 10]])

    def test_float_rgb_rounding(self):
        np.testing.assert_array_equal(parse_rgb('0 .5 1', scale=1), [[0, 128, 255]])

    def test_reject_invalid_rgb(self):
        for value in ('0 1 2', 'nan 0 1', '0 1', '-.1 0 0'):
            with self.assertRaises(ValueError):
                parse_rgb(value, scale=1)

    def test_pal_roundtrip(self):
        data = np.array([[0, 12, 255], [255, 128, 0]])
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'test.pal'
            write_pal(path, data)
            np.testing.assert_array_equal(read_pal(path), data)

    def test_reverse_and_continuous_sampling(self):
        data = np.array([[0, 0, 0], [128, 128, 128], [255, 255, 255]])
        np.testing.assert_array_equal(select_colors(data, 2, reverse=True), data[[2, 0]])

    def test_discrete_colors_not_silently_interpolated(self):
        with self.assertRaises(ValueError):
            select_colors(np.zeros((3, 3), dtype=int), 6, discrete=True)

    def test_levels_must_be_finite_increasing(self):
        for levels in ([0, 0, 1], [1, 0], [0, float('nan')], [0]):
            with self.assertRaises(ValueError):
                validate_levels(levels)
        self.assertEqual(validate_levels([0, 1, 5]), [0., 1., 5.])

    def test_ci_does_not_force_estimate_inside_interval(self):
        x, y = ci_segments([1, 2], [0, 3], [2, 4])
        np.testing.assert_allclose(x, [1, 1, np.nan, 2, 2, np.nan], equal_nan=True)
        np.testing.assert_allclose(y, [0, 2, np.nan, 3, 4, np.nan], equal_nan=True)
        with self.assertRaises(ValueError):
            ci_segments([1], [3], [2])


if __name__ == '__main__':
    unittest.main()
