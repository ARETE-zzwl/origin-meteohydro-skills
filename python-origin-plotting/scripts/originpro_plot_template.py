"""Native editable Origin point/interval figure; no fitting or implicit data cleaning."""
import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

from palette_tools import ci_segments


def validate(data):
    columns = ['x', 'estimate', 'lo', 'hi']
    values = data[columns].to_numpy(dtype=float)
    if len(data) == 0 or not np.isfinite(values).all():
        raise ValueError('Nonempty finite x, estimate, lo and hi required; resolve missing data explicitly')
    if np.any(data.lo > data.hi):
        raise ValueError('Lower interval endpoint exceeds upper endpoint')
    return data.copy()


def build(op, data, out, xlabel, ylabel, title, preview):
    op.new()
    wb = op.new_book(lname='Figure source and interval endpoints')
    wb.name = 'PlotData'
    wb[0].name = 'Audit'
    wb[0].from_df(data)
    wb[0].cols_axis('xyyy', repeat=False)
    x, y = ci_segments(data.x, data.lo, data.hi)
    bounds = wb.add_sheet('Intervals')
    bounds.from_df(pd.DataFrame({'x': x, 'y': y}))
    bounds.cols_axis('xy', repeat=False)
    gp = op.new_graph(template='Origin', lname=title)
    gp.name = 'Figure'
    gp.lt_exec('page.kar=0; page.width=120/25.4*page.resX; page.height=95/25.4*page.resY; page.color=1;')
    gl = gp[0]
    for sheet, kind in [(bounds, 'l'), (wb[0], 's')]:
        plot = gl.add_plot(sheet, colx=0, coly=1, type=kind)
        plot.color = '#296795'
        plot.set_cmd('-wp 1.2', '-d 0')
        if kind == 's':
            plot.symbol_kind = 2
            plot.symbol_size = 5
            plot.set_cmd('-kf 0')
    gl.rescale()
    gl.axis('x').title = r'\f:Arial(' + xlabel + ')'
    gl.axis('y').title = r'\f:Arial(' + ylabel + ')'
    for name in ('xb', 'yl'):
        gl.label(name).set_float('fsize', 9)
    gl.lt_exec('label -r legend; layer.x.label.fsize=9; layer.y.label.fsize=9; '
               'layer.x.label.font=font(Arial); layer.y.label.font=font(Arial); '
               'layer.tickL=3; layer.x.minorTicks=0; layer.y.minorTicks=0;')
    gp.activate()
    gp.lt_exec('doc -uw;')
    project = out / 'figure.opju'
    op.save(str(project))
    if preview:
        for ext in ('png', 'svg'):
            dimensions = ' tr1.Unit:=2 tr1.Width:=1800' if ext == 'png' else ''
            gp.lt_exec(f'expgraph -sw type:={ext} filename:="preview" path:="{out}" '
                       f'overwrite:=rename tr.Margin:=2{dimensions};')
            if not (out / f'preview.{ext}').is_file():
                raise RuntimeError(f'Missing Origin preview: {ext}')
    op.open(str(project), readonly=True, asksave=False)
    loaded = op.find_sheet('w', '[PlotData]Audit').to_df()
    pd.testing.assert_frame_equal(loaded, data, check_dtype=False, check_exact=False, atol=1e-12, rtol=0)
    np.testing.assert_allclose(loaded[['x', 'estimate', 'lo', 'hi']].to_numpy(dtype=float),
                               data[['x', 'estimate', 'lo', 'hi']].to_numpy(dtype=float), rtol=0, atol=1e-12)
    intervals = op.find_sheet('w', '[PlotData]Intervals').to_df().to_numpy(dtype=float)
    if len(intervals) not in (len(x)-1, len(x)):
        raise RuntimeError('Interval rows truncated')
    np.testing.assert_allclose(intervals, np.column_stack([x, y])[:len(intervals)], equal_nan=True)
    if len(op.find_graph('Figure')[0].plot_list()) != 2:
        raise RuntimeError('Native plot count mismatch')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--synthetic', action='store_true')
    group.add_argument('--csv', type=Path, help='Required columns: x,estimate,lo,hi; metadata columns preserved')
    parser.add_argument('--out', required=True, type=Path)
    parser.add_argument('--xlabel', default='Relative day')
    parser.add_argument('--ylabel', default='Effect (specify units)')
    parser.add_argument('--export-preview', action='store_true')
    args = parser.parse_args()
    if args.synthetic:
        data = pd.DataFrame({'x': range(1, 8), 'estimate': [.4, .6, .7, .55, .4, .25, .1],
                             'lo': [.1, .2, .3, .15, 0, -.1, -.2],
                             'hi': [.7, 1, 1.1, .95, .8, .6, .4]})
    else:
        data = pd.read_csv(args.csv)
    data = validate(data)
    # Keep plot columns first; no sorting, dropping, recomputation or interval symmetrization.
    columns = ['x', 'estimate', 'lo', 'hi']
    data = data[columns + [c for c in data.columns if c not in columns]]
    out = args.out.resolve()
    out.mkdir(parents=True, exist_ok=False)
    data.to_csv(out / 'source.csv', index=False, encoding='utf-8-sig')
    import originpro as op
    try:
        op.set_show(False)  # Dedicated external instance. Never call attach here.
        build(op, data, out, args.xlabel, args.ylabel,
              'SYNTHETIC DEMO - not research results' if args.synthetic else 'Provided data', args.export_preview)
        manifest = {'backend': 'OriginPro', 'synthetic': args.synthetic, 'rows': len(data),
                    'status': 'NATIVE_SAVED_AND_REOPEN_VERIFIED', 'origin_version': op.lt_float('@V'),
                    'note': 'Audit and Intervals are copied sheets, not formula-linked. Preview needs visual review.',
                    'files': {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                              for p in out.iterdir() if p.is_file()}}
        (out / 'manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    finally:
        op.exit()  # Only the dedicated instance created by this script.
    print(out)


if __name__ == '__main__':
    main()
