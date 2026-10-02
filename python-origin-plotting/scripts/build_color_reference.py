"""Build vector palette and colorbar reference pages from the offline LUTs."""
import argparse
import csv
from pathlib import Path

from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor

ASSETS = Path(__file__).resolve().parents[1]/'assets'


def palette(name):
    with (ASSETS/f'palettes/{name}.csv').open(encoding='utf-8') as f:
        return [r['HEX'] for r in csv.DictReader(f)]


def strip(c, name, x, y, w, h, categorical=False):
    colors = palette(name)
    if not categorical:
        c.saveState()
        clip = c.beginPath()
        clip.rect(x, y, w, h)
        c.clipPath(clip, stroke=0, fill=0)
        c.linearGradient(x, y, x+w, y, [HexColor(color) for color in colors])
        c.restoreState()
        return
    for i, color in enumerate(colors):
        c.setFillColor(HexColor(color))
        c.rect(x+i*w/len(colors), y, w/len(colors)-.45*mm, h, fill=1, stroke=0)


def label(c, s, x, y, size=8, bold=False, center=False, color='#222222'):
    c.setFillColor(HexColor(color))
    c.setFont('Arial-Bold' if bold else 'Arial', size)
    (c.drawCentredString if center else c.drawString)(x*mm, y*mm, s)


def build(out):
    out.mkdir(parents=True, exist_ok=True)
    pdfmetrics.registerFont(TTFont('Arial', 'C:/Windows/Fonts/arial.ttf'))
    pdfmetrics.registerFont(TTFont('Arial-Bold', 'C:/Windows/Fonts/arialbd.ttf'))
    c = canvas.Canvas(str(out/'palette_reference_pages.pdf'), pagesize=(180*mm, 242*mm), initialFontName='Arial')
    c.setTitle('Scientific palettes and Origin colorbar recipes')
    label(c, 'Scientific colour selection', 12, 229, 16, True)
    label(c, 'Selected options from the 40-palette offline library', 12, 220, 8)
    rows = [
        ('CATEGORY / GROUP', [('tol_bright', '3-7 groups'), ('tol_vibrant', 'strong categorical colours'),
                            ('tol_high_contrast', 'three groups'), ('tol_muted', 'up to nine groups'),
                            ('tol_pale', 'fills only')]),
        ('MAGNITUDE / ORDER', [('navia', 'moisture or intensity'), ('batlow', 'general magnitude'),
                              ('cividis', 'ordered values'), ('glasgow', 'ordered multi-hue'),
                              ('lipari', 'high-range intensity'), ('cmocean_rain', 'precipitation')]),
        ('SIGNED DIFFERENCE', [('vik', 'blue to red'), ('broc', 'blue to olive'),
                               ('bam', 'magenta to green'), ('cmocean_balance', 'blue to red')]),
        ('PHASE / DIRECTION', [('romaO', 'cyclic phase'), ('cmocean_phase', 'cyclic direction')]),
    ]
    y = 208
    for heading, entries in rows:
        label(c, heading, 12, y, 8, True)
        y -= 9
        for name, note in entries:
            label(c, name, 12, y+1, 7.3)
            strip(c, name, 49*mm, y*mm, 77*mm, 3.5*mm, heading.startswith('CATEGORY'))
            label(c, note, 129, y+1, 6.5)
            y -= 8
        y -= 4
    label(c, 'PAL files contain colours only. Set units, limits, centre and missing values in Origin.', 12, 15, 7)
    label(c, 'Sources: Scientific Colour Maps / Paul Tol / cmocean / Matplotlib. See the source index.', 12, 10, 6.7)
    c.showPage()
    label(c, 'Colorbars with a clear meaning', 12, 229, 16, True)
    label(c, 'Illustrative scales: replace ranges and units with the actual study definition.', 12, 220, 8)
    settings = [
        (190, '01  Non-negative magnitude', 'cmocean_rain', 'Rainfall (mm/day)', [0, 10, 20, 30, 40, 50], (0, 50),
         'Use a sequential palette; distinguish zero rainfall from missing data.'),
        (133, '02  Positive and negative change', 'vik', 'Storage change (mm)', [-20, -10, 0, 10, 20], (-20, 20),
         'Place zero at the neutral centre; share the range across comparable panels.'),
        (76, '03  Cyclic direction', 'romaO', 'Direction (degrees)', [0, 90, 180, 270, 360], (0, 360),
         'Use a closed colour cycle; specify whether a vector points to or comes from a direction.'),
    ]
    for y, title, name, units, ticks, limits, note in settings:
        label(c, title, 12, y+12, 9, True)
        strip(c, name, 24*mm, y*mm, 132*mm, 4*mm)
        for tick in ticks:
            x = 24+(tick-limits[0])/(limits[1]-limits[0])*132
            c.setStrokeColor(HexColor('#333333')); c.setLineWidth(.45)
            c.line(x*mm, y*mm, x*mm, (y-1.2)*mm)
            label(c, str(tick), x, y-5, 7.5, center=True)
        label(c, units, 90, y-12, 8, center=True)
        label(c, note, 12, y-21, 7)
    label(c, 'Origin workflow', 12, 34, 9, True)
    label(c, 'Import PAL in Color Manager > set Colormap/Contours levels > adjust Color Scale labels.', 12, 26, 7.4)
    label(c, 'Use 3-6 major labels where readable. Keep minor labels off; retain real overflow indicators.', 12, 20, 7.4)
    label(c, 'Categorical violins, boxes and paired points use legends, not a continuous numerical colorbar.', 12, 14, 7.4)
    c.save()
    print(out/'palette_reference_pages.pdf')


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--out', type=Path, required=True)
    args = p.parse_args()
    build(args.out.resolve())
