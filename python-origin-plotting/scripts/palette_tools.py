"""Offline palette export. A PAL carries colors, not units or data boundaries."""
import argparse
import csv
import json
from pathlib import Path

import numpy as np

ASSETS = Path(__file__).resolve().parents[1] / 'assets'


def parse_rgb(text, scale):
    rows = []
    for line in text.splitlines():
        line = line.split('#')[0].strip()
        if not line or line.startswith('ncolors'):
            continue
        rows.append([float(v) for v in line.split()])
    values = np.asarray(rows, dtype=float)
    if (scale not in (1, 255) or values.ndim != 2 or values.shape[1] != 3
            or len(values) == 0 or not np.isfinite(values).all()
            or np.any(values < 0) or np.any(values > scale)):
        raise ValueError('Expected finite RGB rows within declared scale')
    return np.rint(values * (255 / scale)).astype(int)


def write_pal(path, rgb):
    path.write_text('JASC-PAL\n0100\n' + str(len(rgb)) + '\n' +
                    '\n'.join(' '.join(str(int(v)) for v in row) for row in rgb) + '\n', encoding='ascii')


def read_pal(path):
    lines = path.read_text(encoding='ascii').splitlines()
    if lines[:2] != ['JASC-PAL', '0100']:
        raise ValueError('Not a JASC PAL')
    rgb = parse_rgb('\n'.join(lines[3:]), 255)
    if len(rgb) != int(lines[2]):
        raise ValueError('PAL count mismatch')
    return rgb


def write_csv(path, rgb):
    with path.open('w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['index', 'R', 'G', 'B', 'HEX'])
        for i, (r, g, b) in enumerate(rgb):
            writer.writerow([i, r, g, b, f'#{r:02X}{g:02X}{b:02X}'])


def select_colors(rgb, count, reverse=False, discrete=False):
    if count < 1 or (discrete and count != len(rgb)):
        raise ValueError('Use the native color count for discrete/categorical palettes')
    rgb = rgb[::-1] if reverse else rgb
    return rgb[np.rint(np.linspace(0, len(rgb) - 1, count)).astype(int)]


def validate_levels(levels):
    values = np.asarray(levels, dtype=float)
    if len(values) < 2 or not np.isfinite(values).all() or np.any(np.diff(values) <= 0):
        raise ValueError('Levels must contain at least two finite increasing boundaries')
    return values.tolist()


def ci_segments(x, lo, hi):
    x, lo, hi = (np.asarray(v, dtype=float) for v in (x, lo, hi))
    if not (x.shape == lo.shape == hi.shape) or x.ndim != 1:
        raise ValueError('CI columns must be aligned 1-D arrays')
    if not np.isfinite([x, lo, hi]).all() or np.any(lo > hi):
        raise ValueError('CI endpoints must be finite and ordered')
    gap = np.full(len(x), np.nan)
    return np.column_stack([x, x, gap]).ravel(), np.column_stack([lo, hi, gap]).ravel()


def catalog():
    return json.loads((ASSETS / 'palette_catalog.json').read_text(encoding='utf-8'))


def load_palette(name):
    entry = next((p for p in catalog()['palettes'] if p['name'] == name), None)
    if entry is None:
        raise ValueError(f'Unknown palette: {name}')
    return entry, read_pal(ASSETS / entry['pal'])


def mpl_cmap(name):
    from matplotlib.colors import ListedColormap
    return ListedColormap(load_palette(name)[1] / 255, name=name)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('list')
    export = sub.add_parser('export')
    export.add_argument('--name', required=True)
    export.add_argument('--levels', type=float, nargs='+', required=True)
    export.add_argument('--reverse', action='store_true')
    export.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    if args.command == 'list':
        for p in catalog()['palettes']:
            print(f"{p['name']:32} {p['kind']:14} {p['count']:3} {p['use']}")
        return
    entry, rgb = load_palette(args.name)
    levels = validate_levels(args.levels)
    colors = select_colors(rgb, len(levels) - 1, args.reverse,
                           entry['kind'] in ('discrete', 'categorical'))
    args.out.mkdir(parents=True, exist_ok=False)
    write_pal(args.out / f'{args.name}.pal', colors)
    write_csv(args.out / f'{args.name}.csv', colors)
    with (args.out / 'interval_colors.csv').open('w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['lower', 'upper', 'HEX'])
        for lo, hi, (r, g, b) in zip(levels[:-1], levels[1:], colors):
            writer.writerow([lo, hi, f'#{r:02X}{g:02X}{b:02X}'])
    (args.out / 'mapping.json').write_text(json.dumps({
        'palette': args.name, 'levels': levels, 'reverse': args.reverse,
        'units': 'USER MUST SPECIFY', 'under_over_missing': 'USER MUST SPECIFY',
        'interval_convention': 'Lower-inclusive/upper-exclusive; decide final upper endpoint in plotting tool',
        'note': 'PAL contains colors only; set levels and missing-value treatment separately in Origin.'
    }, indent=2), encoding='utf-8')
    print(args.out.resolve())


if __name__ == '__main__':
    main()
