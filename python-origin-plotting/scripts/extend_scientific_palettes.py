"""Append fixed-source scientific palettes; preserve every existing LUT."""
import argparse
import hashlib
import json
from pathlib import Path
import urllib.request

import numpy as np

from palette_tools import ASSETS, parse_rgb, write_csv, write_pal

PIN = '78f02a088fa3c4fb4cb8aa92bd8e52389ab9d09a'
SCM = [('navia', 'sequential'), ('lipari', 'sequential'), ('glasgow', 'sequential'),
       ('devon', 'sequential'), ('oslo', 'sequential'), ('lajolla', 'sequential'),
       ('bam', 'diverging'), ('broc', 'diverging'), ('romaO', 'cyclic')]
TOL = {
    'tol_bright': ['4477AA', 'EE6677', '228833', 'CCBB44', '66CCEE', 'AA3377', 'BBBBBB'],
    'tol_vibrant': ['EE7733', '0077BB', '33BBEE', 'EE3377', 'CC3311', '009988', 'BBBBBB'],
    'tol_muted': ['CC6677', '332288', 'DDCC77', '117733', '88CCEE', '882255', '44AA99', '999933', 'AA4499'],
    'tol_high_contrast': ['004488', 'DDAA33', 'BB5566'],
    'tol_medium_contrast': ['6699CC', '004488', 'EECC66', '994455', '997700', 'EE99AA'],
    'tol_pale': ['AACCEE', 'CCEEFF', 'BBDDBB', 'EEEEBB', 'FFBBCC', 'EEBBDD', 'DDDDDD'],
}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def extend(root, allow_network):
    path = root / 'palette_catalog.json'
    catalog = json.loads(path.read_text(encoding='utf-8'))
    original = {p['name']: p.copy() for p in catalog['palettes']}
    added = []

    def append(name, rgb, kind, provider, url, raw, use):
        if name in original:
            return
        pal, csv = root/f'palettes/{name}.pal', root/f'palettes/{name}.csv'
        write_pal(pal, rgb)
        write_csv(csv, rgb)
        catalog['palettes'].append(dict(name=name, kind=kind, count=len(rgb), use=use,
            provider=provider, source_url=url, pal=f'palettes/{name}.pal', csv=f'palettes/{name}.csv',
            pal_sha256=digest(pal), csv_sha256=digest(csv), raw=str(raw.relative_to(root)).replace('\\', '/'),
            raw_sha256=digest(raw)))
        added.append(name)

    for name, kind in SCM:
        if name in original:
            continue
        url = f'https://raw.githubusercontent.com/callumrollo/cmcrameri/{PIN}/cmcrameri/cmaps/{name}.txt'
        raw = root/f'raw/{name}.txt'
        if not raw.exists():
            if not allow_network:
                raise ValueError('Missing raw LUT: use --allow-network explicitly')
            with urllib.request.urlopen(url, timeout=45) as r:
                data = r.read(100_000)
            rgb = parse_rgb(data.decode('ascii'), 1)
            assert rgb.shape == (256, 3)
            raw.write_bytes(data)
        rgb = parse_rgb(raw.read_text(encoding='ascii'), 1)
        append(name, rgb, kind, 'cmcrameri', url, raw, 'SCM 8.0; choose normalization separately')
        print('SCM', name, flush=True)
    tol_raw = root/'raw/tol_qualitative_20261002.json'
    tol_raw.write_text(json.dumps(dict(source='https://sronpersonalpages.nl/~pault/',
        checked='2026-10-02', palettes=TOL, transformation='Exact published RGB triplets; no copied executable code'),
        indent=2), encoding='utf-8')
    catalog['sources']['paul_tol'] = dict(url='https://sronpersonalpages.nl/~pault/',
        retrieved='2026-10-02', attribution='Paul Tol',
        note='Published colour coordinates transcribed as data; original figures and source code not redistributed; no new license asserted.')
    for name, values in TOL.items():
        rgb = np.array([[int(h[k:k+2], 16) for k in (0, 2, 4)] for h in values])
        use = 'Background fills, not thin lines' if name == 'tol_pale' else 'Categorical groups; pair with symbols or line styles'
        append(name, rgb, 'categorical', 'paul_tol', catalog['sources']['paul_tol']['url'], tol_raw, use)
    for entry in catalog['palettes']:
        if entry['name'] in original:
            assert entry == original[entry['name']]
            assert digest(root/entry['pal']) == entry['pal_sha256']
    path.write_text(json.dumps(catalog, indent=2), encoding='utf-8')
    print('Added:', ', '.join(added), '\nTotal:', len(catalog['palettes']))


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--assets', type=Path, default=ASSETS)
    p.add_argument('--allow-network', action='store_true')
    args = p.parse_args()
    extend(args.assets.resolve(), args.allow_network)
