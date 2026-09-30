"""Build a pinned, offline LUT library; fetch data/licenses only, never remote code."""
import argparse
import hashlib
import importlib.metadata
import json
import shutil
import time
import urllib.request
from pathlib import Path

import matplotlib as mpl
import numpy as np

from palette_tools import parse_rgb, write_csv, write_pal

PINS = {
    'cmocean': ('matplotlib/cmocean', '59c35002c3aa5296b65d9646e52604c627441eb6'),
    'cmcrameri': ('callumrollo/cmcrameri', '78f02a088fa3c4fb4cb8aa92bd8e52389ab9d09a'),
    'ncl': ('NCAR/ncl', '8f9e9476281cc6f6d9d12eaa78729c7003ca24b7'),
}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def download(url, destination):
    for attempt in range(3):
        try:
            with urllib.request.urlopen(url, timeout=30) as response:
                data = response.read(2_000_001)
            if len(data) > 2_000_000:
                raise ValueError('Unexpectedly large LUT/license')
            destination.write_bytes(data)
            return url
        except OSError:
            if attempt == 2:
                raise
            time.sleep(1 + attempt)


def fetch(provider, relative, destination):
    repo, commit = PINS[provider]
    return download(f'https://raw.githubusercontent.com/{repo}/{commit}/{relative}', destination)


def refresh_manifest(root):
    (root / 'manifest.json').write_text(json.dumps({
        'files': {str(p.relative_to(root)).replace('\\', '/'): digest(p)
                  for p in sorted(root.rglob('*')) if p.is_file() and p.name != 'manifest.json'}
    }, indent=2), encoding='utf-8')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--allow-network', action='store_true', required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    root = args.out.resolve()
    root.mkdir(parents=True, exist_ok=False)
    for name in ('raw', 'palettes', 'licenses'):
        (root / name).mkdir()
    entries = []
    sources = {}
    for provider, filename in [('cmocean', 'LICENSE.txt'), ('cmcrameri', 'LICENSE.txt'), ('ncl', 'LICENSE')]:
        dest = root / 'licenses' / f'{provider}.txt'
        sources[provider] = {'license_url': fetch(provider, filename, dest),
                             'license_file': str(dest.relative_to(root)).replace('\\', '/'),
                             'commit': PINS[provider][1]}
    sources['ncl']['license_text_url'] = download('https://www.apache.org/licenses/LICENSE-2.0.txt',
                                                 root / 'licenses/Apache-2.0.txt')
    sources['ncl']['license_text_file'] = 'licenses/Apache-2.0.txt'
    dist = importlib.metadata.distribution('matplotlib')
    license_path = next(dist.locate_file(f) for f in dist.files
                        if str(f).endswith('.dist-info/LICENSE'))
    shutil.copy2(license_path, root / 'licenses/matplotlib.txt')
    sources['matplotlib'] = {'version': mpl.__version__, 'license_file': 'licenses/matplotlib.txt',
                             'url': 'https://matplotlib.org/stable/users/explain/colors/colormaps.html'}

    def add(name, rgb, kind, use, provider, url, raw=None):
        pal, table = root / f'palettes/{name}.pal', root / f'palettes/{name}.csv'
        write_pal(pal, rgb)
        write_csv(table, rgb)
        entries.append({'name': name, 'kind': kind, 'count': len(rgb), 'use': use,
                        'provider': provider, 'source_url': url,
                        'pal': f'palettes/{name}.pal', 'csv': f'palettes/{name}.csv',
                        'pal_sha256': digest(pal), 'csv_sha256': digest(table),
                        'raw': str(raw.relative_to(root)).replace('\\', '/') if raw else None,
                        'raw_sha256': digest(raw) if raw else None})

    for name, kind, use in [
        ('viridis', 'sequential', 'Magnitude / moisture / generic positive field'),
        ('cividis', 'sequential', 'Magnitude; restrained blue-yellow'),
        ('magma', 'sequential', 'Intensity / temperature'),
        ('Blues', 'sequential', 'Precipitation / water depth'),
        ('YlGnBu', 'sequential', 'Precipitation / runoff'),
        ('YlOrRd', 'sequential', 'Heat intensity'),
        ('RdBu_r', 'diverging', 'Anomalies: negative blue, positive red'),
        ('BrBG', 'diverging', 'Dry-wet anomalies: negative brown, positive green'),
        ('PuOr', 'diverging', 'Signed differences; specify direction'),
        ('twilight', 'cyclic', 'Phase / direction'),
        ('okabe_ito', 'categorical', 'Groups with line/symbol redundancy'),
        ('tab10', 'categorical', 'Distinct groups')]:
        cmap = mpl.colormaps[name]
        n = cmap.N if kind == 'categorical' else 256
        rgb = np.rint(cmap(np.linspace(0, 1, n))[:, :3] * 255).astype(int)
        add(name, rgb, kind, use, 'matplotlib', sources['matplotlib']['url'])

    for name, kind, use in [
        ('rain', 'sequential', 'Rainfall: pale dry to blue wet'),
        ('thermal', 'sequential', 'Absolute temperature'),
        ('speed', 'sequential', 'Wind speed / IVT magnitude'),
        ('balance', 'diverging', 'Signed anomalies'),
        ('delta', 'diverging', 'Dry-wet difference'),
        ('phase', 'cyclic', 'Phase / direction')]:
        raw = root / f'raw/cmocean_{name}.txt'
        url = fetch('cmocean', f'cmocean/rgb/{name}-rgb.txt', raw)
        add('cmocean_' + name, parse_rgb(raw.read_text(), 1), kind, use, 'cmocean', url, raw)
    for name, kind in [('batlow', 'sequential'), ('vik', 'diverging')]:
        raw = root / f'raw/{name}.txt'
        url = fetch('cmcrameri', f'cmcrameri/cmaps/{name}.txt', raw)
        add(name, parse_rgb(raw.read_text(), 1), kind, 'Scientific Colour Maps; magnitude / anomalies', 'cmcrameri', url, raw)
    for name, kind, use in [
        ('precip_11lev', 'discrete', 'Traditional MeteoSwiss/NCL rainfall levels; 12 colors'),
        ('precip_diff_12lev', 'discrete', 'Traditional NCL precipitation differences'),
        ('BlueWhiteOrangeRed', 'diverging', 'Traditional signed field'),
        ('WhiteBlueGreenYellowRed', 'sequential', 'Traditional multi-hue precipitation / intensity')]:
        raw = root / f'raw/ncl_{name}.rgb'
        url = fetch('ncl', f'ni/src/db/colormaps/{name}.rgb', raw)
        add('ncl_' + name, parse_rgb(raw.read_text(), 255), kind, use, 'ncl', url, raw)
    colors = ['#C7803E', '#686E73', '#296795', '#965D87', '#529E98']
    rgb = np.array([[int(c[i:i+2], 16) for i in (1, 3, 5)] for c in colors])
    add('heat_rain_roles', rgb, 'categorical', 'Local roles: heat, control, rain, conditional, comparison',
        'local', 'Locally selected role palette; not an external meteorological standard')
    sources['local'] = {'license': 'CC0-1.0', 'note': 'Local choice of five color triplets only'}
    (root / 'palette_catalog.json').write_text(json.dumps({
        'schema': 1, 'sources': sources, 'quantization': 'round RGB*255 for float LUTs',
        'note': 'Colors only, no automatic units/norm/levels. NCL traditional tables are not claimed perceptually uniform.',
        'palettes': entries}, indent=2), encoding='utf-8')
    refresh_manifest(root)
    print(f'Built {len(entries)} palettes in {root}')


if __name__ == '__main__':
    main()
