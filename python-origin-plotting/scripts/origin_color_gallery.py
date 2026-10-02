"""Twelve native Origin colour examples with fixed synthetic data, never study data."""
import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
import originpro as op
from scipy.stats import gaussian_kde

from palette_tools import load_palette

W, H = 180, 242
BLUE, ORANGE = '#0072B2', '#D55E00'
LABELS, TABLES = {}, {}
RECTS = [(18, 164, 63, 44), (104, 164, 63, 44), (18, 91, 63, 44),
         (104, 91, 63, 44), (18, 18, 63, 44), (104, 18, 63, 44)]


def hexes(name):
    return ['#%02X%02X%02X' % tuple(v) for v in load_palette(name)[1]]


def tint(color, fraction=.25):
    rgb = np.array([int(color[k:k+2], 16) for k in (1, 3, 5)])
    return '#%02X%02X%02X' % tuple(np.rint(255*(1-fraction)+rgb*fraction).astype(int))


def sheet(book, data):
    name = f'S{len(TABLES)+1:03d}'
    ws = book[0] if not TABLES else book.add_sheet(name)
    ws.name = name
    d = pd.DataFrame(data).reset_index(drop=True)
    ws.from_df(d)
    TABLES[f'[{book.name}]{name}'] = d
    return ws


def line(layer, book, x, y, color, width=.9, dash=0):
    ws = sheet(book, {'x': x, 'y': y})
    p = layer.add_plot(ws, colx=0, coly=1, type='l')
    p.color = color
    p.set_cmd(f'-wp {width}', f'-d {dash}')
    return p


def points(layer, book, x, y, color, size=2, opened=0):
    ws = sheet(book, {'x': x, 'y': y})
    p = layer.add_plot(ws, colx=0, coly=1, type='s')
    p.color = color
    p.symbol_kind = 1 if opened else 2
    p.symbol_size = size
    p.set_cmd(f'-kf {opened}', '-wp .7')


def fill(layer, book, x, low, high, color, outline=None):
    x = np.asarray(x)
    low, high = np.broadcast_to(low, x.shape), np.broadcast_to(high, x.shape)
    assert np.all(low <= high)
    ws = sheet(book, {'x': x, 'high': high, 'low': low})
    upper = layer.add_plot(ws, colx=0, coly=1, type='l')
    lower = layer.add_plot(ws, colx=0, coly=2, type='l')
    for p in [upper, lower]:
        p.color = outline or color
        p.set_cmd('-wp .35')
    c = op.lt_int(f'color("{color}")')
    upper.set_cmd('-pf 1', '-pfv 9', f'-pfb {c}', f'-p2fb {c}')


def text(graph, value, x, y, size=8, bold=0):
    LABELS[graph.name].append(dict(text=value, x=x, y=y, size=size, bold=bold))


def layer_at(graph, rect, xlim, ylim, first=False, ticks=True):
    gl = graph[0] if first else graph.add_layer()
    x, y, w, h = rect
    gl.lt_exec('layer.fixed=1;layer.factor=1;layer.unit=0;layer.clip=0;'
               f'layer.left={x/W*100};layer.top={(H-y-h)/H*100};'
               f'layer.width={w/W*100};layer.height={h/H*100};'
               'label -r legend;label -r xb;label -r yl;'
               f'layer.x.showAxes={int(ticks)};layer.x.showLabels={int(ticks)};'
               'layer.y.showAxes=0;layer.y.showLabels=0;'
               'layer.x.thickness=.6;layer.x.label.fsize=7;layer.x.label.font=font(Arial);'
               'layer.tickL=2;layer.x.minorTicks=0;layer.y.minorTicks=0;')
    gl.set_xlim(*xlim)
    gl.set_ylim(*ylim)
    return gl


def panel(graph, index, title, palette, xlim=(-3, 3, 2), ylim=(-.6, 2.7, 1), ticks=True):
    rect = RECTS[index]
    gl = layer_at(graph, rect, xlim, ylim, first=(index == 0), ticks=ticks)
    x, y, w, h = rect
    text(graph, title, x+w/2, y+h+7, 8.5, 1)
    text(graph, palette, x+w/2, y-13, 7)
    return gl


def group_labels(graph, index, ys=(0, 1, 2), labels=('A', 'B', 'C')):
    x, y, w, h = RECTS[index]
    for pos, label in zip(ys, labels):
        text(graph, label, x-4, y+(pos+.6)/3.3*h, 7)


def distributions(graph, book, index, mode, samples, colors):
    titles = ['01  Half violin + points', '02  Split violin', '03  Violin + box',
              '04  Violin + points', '05  Ridgeline', '06  Grouped box']
    palettes = ['Tol bright', 'Blue / vermilion', 'Tol muted', 'Tol vibrant', 'Tol high contrast', 'Blue / vermilion']
    gl = panel(graph, index, titles[index], palettes[index])
    group_labels(graph, index)
    grid = np.linspace(-3, 3, 121)
    for j, values in enumerate(samples):
        color = colors[j % len(colors)]
        density = gaussian_kde(values)(grid)
        density = .34*density/density.max()
        if mode == 'half':
            fill(gl, book, grid, j, j+density, tint(color, .42), color)
            points(gl, book, values, np.full(len(values), j-.12), color, 1.3)
        elif mode == 'split':
            other = values*.85+.55
            second = gaussian_kde(other)(grid)
            second = .34*second/second.max()
            fill(gl, book, grid, j, j+density, tint(BLUE, .5), BLUE)
            fill(gl, book, grid, j-second, j, tint(ORANGE, .5), ORANGE)
        elif mode in ('box', 'points', 'sticks'):
            fill(gl, book, grid, j-density, j+density, tint(color, .30), color)
            if mode == 'box':
                q = np.quantile(values, [.1, .25, .5, .75, .9])
                line(gl, book, q[[0, 4]], [j, j], color)
                fill(gl, book, q[[1, 3]], j-.055, j+.055, color)
                points(gl, book, [q[2]], [j], '#FFFFFF', 2.2)
            elif mode == 'points':
                offsets = .13*np.sin(np.arange(len(values))*2.39996323)
                points(gl, book, values, j+offsets, color, 1.35)
            else:
                sx, sy = [], []
                for v in values:
                    height = np.interp(v, grid, density)
                    sx.extend([v, v, np.nan]); sy.extend([j-height, j+height, np.nan])
                line(gl, book, sx, sy, color, .35)
        elif mode == 'ridge':
            fill(gl, book, grid, j-.3, j-.3+density*1.7, tint(color, .48), color)
        else:
            for k, c in enumerate([BLUE, ORANGE]):
                data = values+.5*k
                q = np.quantile(data, [.1, .25, .5, .75, .9])
                y = j+[-.17, .17][k]
                line(gl, book, q[[0, 4]], [y, y], c)
                fill(gl, book, q[[1, 3]], y-.09, y+.09, tint(c, .35), c)
                line(gl, book, [q[2], q[2]], [y-.09, y+.09], c, 1.1)


def second_page(graph, book, samples):
    gl = panel(graph, 0, '07  Nested bars', 'Deep line / light fill', (0, 100, 25))
    group_labels(graph, 0)
    for j, n in enumerate([46, 71, 93]):
        for k, color in enumerate([BLUE, ORANGE]):
            y = j+[-.18, .18][k]
            fill(gl, book, [0, n-9*k], y-.11, y+.11, tint(color, .2))
            fill(gl, book, [0, n*.27-5*k], y-.045, y+.045, color)
    gl = panel(graph, 1, '08  Paired points + intervals', 'Blue / vermilion', (-1, 2, 1), (-.5, 3.5, 1))
    line(gl, book, [0, 0], [-.5, 3.5], '#BBBBBB', .5, 2)
    for j, val in enumerate([.3, 1., .5, 1.4]):
        line(gl, book, [val, val-.26], [j+.08, j-.08], '#888888', .7)
        for k, c in enumerate([BLUE, ORANGE]):
            x, y = val-.26*k, j+[.08, -.08][k]
            line(gl, book, [x-.25, x+.36], [y, y], c, .8)
            points(gl, book, [x], [y], c, 2.8, k)
    gl = panel(graph, 2, '09  Trajectory + interval band', 'Dark outlines / 22% colour fill', (0, 7, 2), (0, 2.2, 1))
    x = np.linspace(0, 7, 57)
    for k, c in enumerate([BLUE, ORANGE]):
        y = 1.4*np.exp(-x/(5-2*k))+.2*k
        fill(gl, book, x, y-.14, y+.14, tint(c, .22))
    for k, c in enumerate([BLUE, ORANGE]):
        y = 1.4*np.exp(-x/(5-2*k))+.2*k
        line(gl, book, x, y, c, 1.3, k)
    gl = panel(graph, 3, '10  Shared-scale trellis', 'Tol bright', (0, 7, 2), (0, 2, 1), ticks=False)
    left, bottom, width, height = RECTS[3]
    for n in range(4):
        r, c = divmod(n, 2)
        ax = layer_at(graph, (left+c*34, bottom+r*24, 29, 19), (0, 7, 2), (0, 2, 1), ticks=False)
        for k, color in enumerate(hexes('tol_bright')[:2]):
            y = .6+.2*n+.16*np.sin(x/.9+k)+.1*k
            line(ax, book, x, y, color, 1., k)
        line(ax, book, [0, 7], [0, 0], '#999999', .5)
    gl = panel(graph, 4, '11  Split-cell heatmap', 'vik | difference (synthetic units)', (0, 4, 1), (0, 4, 1), ticks=False)
    lut = np.array(load_palette('vik')[1])
    colors = ['#%02X%02X%02X' % tuple(v) for v in lut[np.rint(np.linspace(0, 255, 9)).astype(int)]]
    values = []
    for row in range(4):
        for col in range(4):
            for k in range(2):
                z = float(np.sin(col*.9+.4*k)*np.cos(row*.8)-.15)
                z = np.clip(z, -1, 1)
                idx = min(8, int((z+1)/2*9))
                if k == 0:
                    fill(gl, book, [col, col+1], [row, row+1], [row+1, row+1], colors[idx])
                else:
                    fill(gl, book, [col, col+1], [row, row], [row, row+1], colors[idx])
                values.append(dict(row=row, column=col, group=k, value=z, bin=idx, color=colors[idx]))
    sheet(book, values)
    # Manual native vector key uses the same bins as both halves; it is not a linked ColorScale object.
    x0, y0, _, _ = RECTS[4]
    bar = layer_at(graph, (x0+6, y0-5.2, 51, 2.5), (-1, 1, 1), (0, 1, 1), ticks=False)
    for k, c in enumerate(colors):
        fill(bar, book, [-1+2*k/9, -1+2*(k+1)/9], 0, 1, c)
    for val in [-1, 0, 1]:
        text(graph, str(val), x0+6+(val+1)/2*51, y0-8, 6.5)
    gl = panel(graph, 5, '12  Violin + observation sticks', 'Tol high contrast')
    group_labels(graph, 5)
    grid = np.linspace(-3, 3, 121)
    for j, (v, color) in enumerate(zip(samples, hexes('tol_high_contrast'))):
        density = gaussian_kde(v)(grid)
        density = .34*density/density.max()
        fill(gl, book, grid, j-density, j+density, tint(color, .28), color)
        sx, sy = [], []
        for val in v:
            ht = np.interp(val, grid, density)
            sx.extend([val, val, np.nan]); sy.extend([j-ht, j+ht, np.nan])
        line(gl, book, sx, sy, color, .4)


def add_labels(graph, book):
    gl = layer_at(graph, (0, 0, W, H), (0, W, 20), (0, H, 20), ticks=False)
    gl.name = 'NativeText'
    gl.lt_exec('layer.color=0;layer.border=0;')
    for r in LABELS[graph.name]:
        ws = sheet(book, {'x': [r['x']], 'y': [r['y']]})
        p = gl.add_plot(ws, colx=0, coly=1, type='s')
        p.set_cmd('-k 1', '-z .01', '-c 0', '-q 1', '-qm 5', f'-qms "{r["text"]}"',
                  '-qp 1', f'-qs {r["size"]}', '-qf font(Arial)', '-qu 0', '-qi 0',
                  f'-qb {r["bold"]}', '-qc 1', '-qx 0', '-qy 0', '-qw 0')


def bindings(graph):
    return [[str(l.obj.DataPlots.GetItem(i)) for i in range(l.obj.DataPlots.GetCount())] for l in graph]


def main(out):
    out.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(20261002)
    samples = [np.clip(rng.normal(mu, .52+.12*j, 36), -2.9, 2.9) for j, mu in enumerate([-.7, .0, .65])]
    spec = {}
    try:
        op.set_show(False); op.new()
        book = op.new_book(lname='Synthetic colour examples, not research results')
        book.name = 'Colors'
        sheet(book, {f'Group{j}': v for j, v in enumerate(samples)})
        palettes = [hexes('tol_bright')[:3], [BLUE, ORANGE],
                    [hexes('tol_muted')[i] for i in [0, 6, 1]],
                    [hexes('tol_vibrant')[i] for i in [1, 5, 3]],
                    hexes('tol_high_contrast'), [BLUE, ORANGE]]
        for page in range(2):
            graph = op.new_graph(template='Origin')
            graph.name = f'ColorPage{page+1}'
            graph.lt_exec(f'page.kar=0;page.width={W}/25.4*page.resX;page.height={H}/25.4*page.resY;page.color=1;')
            LABELS[graph.name] = []
            text(graph, 'Origin scientific colour examples', 90, 234, 12, 1)
            text(graph, 'Synthetic data | native editable Origin plots | colours chosen by data role', 90, 227, 7.5)
            if page == 0:
                for i, mode in enumerate(['half', 'split', 'box', 'points', 'ridge', 'grouped']):
                    distributions(graph, book, i, mode, samples, palettes[i])
            else:
                second_page(graph, book, samples)
            add_labels(graph, book)
            spec[graph.name] = dict(bindings=bindings(graph), text=LABELS[graph.name])
            print('BUILT', graph.name, flush=True)
        op.save(str(out/'origin_scientific_colors.opju'))
        for name, expected in TABLES.items():
            pd.testing.assert_frame_equal(op.find_sheet('w', name).to_df(), expected, check_dtype=False,
                                          check_exact=False, atol=1e-11, rtol=1e-12)
        (out/'native_build.json').write_text(json.dumps(spec, indent=2), encoding='utf-8')
    finally:
        op.exit()
    try:
        op.set_show(False)
        op.open(str(out/'origin_scientific_colors.opju'), readonly=True, asksave=False)
        for name, expected in TABLES.items():
            pd.testing.assert_frame_equal(op.find_sheet('w', name).to_df(), expected, check_dtype=False,
                                          check_exact=False, atol=1e-11, rtol=1e-12)
        for name, record in spec.items():
            graph = op.find_graph(name)
            assert bindings(graph) == record['bindings']
            graph.activate(); graph.lt_exec('doc -uw;')
            for ext in ['pdf', 'png']:
                extra = ' tr1.Unit:=2 tr1.Width:=2835' if ext == 'png' else ''
                graph.lt_exec(f'expgraph -sw type:={ext} filename:="{name}" path:="{out}" overwrite:=replace tr.Margin:=2{extra};')
            print('REOPEN_EXPORTED', name, flush=True)
        (out/'native_validation.json').write_text(json.dumps(dict(backend='OriginPro', version=op.lt_float('@V'),
            synthetic=True, seed=20261002, native_tables_verified=len(TABLES), all_bindings_verified=True,
            reopened=True, colorbar='Manual native vector bin key with identical mapping in split cells',
            note='XY density geometry; not built-in violin objects. Demonstration only, not inference.'), indent=2), encoding='utf-8')
    finally:
        op.exit()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--synthetic', action='store_true', required=True)
    args = parser.parse_args()
    main(args.out.resolve())
