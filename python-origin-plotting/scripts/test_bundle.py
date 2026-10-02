"""Offline checks against actual bundled resources and source-table rules."""
import csv
import hashlib
import json
import re
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

from palette_tools import ASSETS, catalog, read_pal
from originpro_plot_template import validate


class BundleTests(unittest.TestCase):
    def test_all_palettes_have_matching_csv_pal_and_hashes(self):
        entries = catalog()['palettes']
        self.assertEqual(len({p['name'] for p in entries}), len(entries))
        self.assertTrue({'viridis', 'batlow', 'vik', 'navia', 'tol_bright', 'tol_high_contrast'} <= {p['name'] for p in entries})
        for entry in entries:
            rgb = read_pal(ASSETS / entry['pal'])
            self.assertEqual(len(rgb), entry['count'])
            with (ASSETS / entry['csv']).open(encoding='utf-8') as f:
                rows = list(csv.DictReader(f))
            np.testing.assert_array_equal(rgb, [[int(r[k]) for k in ('R', 'G', 'B')] for r in rows])
            for row, (r, g, b) in zip(rows, rgb):
                self.assertEqual(row['HEX'], f'#{r:02X}{g:02X}{b:02X}')
            for kind in ('pal', 'csv', 'raw'):
                if entry.get(kind):
                    self.assertEqual(hashlib.sha256((ASSETS / entry[kind]).read_bytes()).hexdigest(), entry[kind+'_sha256'])

    def test_manifest_and_licenses(self):
        for filename, sha in json.loads((ASSETS / 'manifest.json').read_text())['files'].items():
            self.assertEqual(hashlib.sha256((ASSETS / filename).read_bytes()).hexdigest(), sha, filename)
        for source in catalog()['sources'].values():
            if 'license_file' in source:
                self.assertTrue((ASSETS / source['license_file']).is_file())
        self.assertGreater((ASSETS / 'licenses/Apache-2.0.txt').stat().st_size, 10000)

    def test_document_local_links_exist(self):
        root = ASSETS.parent
        for path in [root/'SKILL.md', *sorted((root/'references').glob('*.md'))]:
            for link in re.findall(r'\]\(([^)]+)\)', path.read_text(encoding='utf-8')):
                if not link.startswith(('http:', 'https:', '#')):
                    self.assertTrue((path.parent/link).is_file(), str(path)+': '+link)

    def test_point_outside_interval_and_metadata_preserved(self):
        data = pd.DataFrame({'x': [1], 'estimate': [2], 'lo': [3], 'hi': [4], 'group': ['A']})
        pd.testing.assert_frame_equal(validate(data), data)

    def test_missing_and_inverted_interval_rejected(self):
        for lo, hi in [(float('nan'), 3), (3, 2)]:
            data = pd.DataFrame({'x': [1], 'estimate': [2], 'lo': [lo], 'hi': [hi]})
            with self.assertRaises(ValueError):
                validate(data)


if __name__ == '__main__':
    unittest.main()
