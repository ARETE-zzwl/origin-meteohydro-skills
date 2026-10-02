"""Check LUT integrity, original-palette preservation and quantized lightness trends."""
import argparse
import hashlib
import json
from pathlib import Path

import numpy as np

from palette_tools import ASSETS, read_pal


def lightness(rgb):
    s = np.asarray(rgb)/255
    linear = np.where(s <= .04045, s/12.92, ((s+.055)/1.055)**2.4)
    y = linear @ np.array([.2126, .7152, .0722])
    return np.where(y > (6/29)**3, 116*np.cbrt(y)-16, (29/3)**3*y)


def check(out):
    cat = json.loads((ASSETS/'palette_catalog.json').read_text(encoding='utf-8'))
    assert len(cat['palettes']) == 40
    assert len({p['name'] for p in cat['palettes']}) == 40
    rows = []
    for p in cat['palettes']:
        a = read_pal(ASSETS/p['pal'])
        assert len(a) == p['count']
        for field in ['pal', 'csv', 'raw']:
            if p.get(field):
                assert hashlib.sha256((ASSETS/p[field]).read_bytes()).hexdigest() == p[field+'_sha256']
        l = lightness(a)
        row = dict(name=p['name'], kind=p['kind'], count=len(a),
                   lightness_start=float(l[0]), lightness_end=float(l[-1]))
        if p['kind'] == 'sequential':
            sign = 1 if l[-1] >= l[0] else -1
            row['lightness_reversals_gt_0_1'] = int(np.sum(sign*np.diff(l) < -.1))
            row['note'] = 'Diagnostic only; not a perceptual-uniformity or colour-vision-deficiency certification'
        rows.append(row)
    out.write_text(json.dumps(dict(palettes=rows, count=40, quantization='8-bit RGB',
        categorical_interpolation=False, source_files_and_hashes_verified=True), indent=2), encoding='utf-8')
    print('Verified 40 palettes; report:', out)


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--out', type=Path, required=True)
    args = p.parse_args()
    check(args.out)
