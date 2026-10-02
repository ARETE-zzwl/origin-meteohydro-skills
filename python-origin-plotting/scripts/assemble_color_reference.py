"""Embed permitted Arial resources and assemble native Origin and palette pages."""
import argparse
import hashlib
import json
from pathlib import Path

import fitz
from fontTools.ttLib import TTFont

FONTS = {'ArialMT': Path('C:/Windows/Fonts/arial.ttf'),
         'Arial-BoldMT': Path('C:/Windows/Fonts/arialbd.ttf')}


def assemble(source, destination):
    destination.mkdir(parents=True, exist_ok=True)
    merged = fitz.open()
    checked = []
    for filename in ['ColorPage1.pdf', 'ColorPage2.pdf', 'palette_reference_pages.pdf']:
        with fitz.open(source/filename) as doc:
            streams = [[hashlib.sha256(doc.xref_stream(x)).hexdigest() for x in p.get_contents()] for p in doc]
            for page in doc:
                for ref, _, kind, name, *_ in page.get_fonts(full=True):
                    if kind == 'Type3' or doc.extract_font(ref)[3]:
                        continue
                    font = FONTS[name]
                    assert not TTFont(font)['OS/2'].fsType & (2 | 512)
                    data = font.read_bytes()
                    new = doc.get_new_xref()
                    doc.update_object(new, f'<< /Length1 {len(data)} >>')
                    doc.update_stream(new, data)
                    typ, descriptor = doc.xref_get_key(ref, 'FontDescriptor')
                    assert typ == 'xref'
                    doc.xref_set_key(int(descriptor.split()[0]), 'FontFile2', f'{new} 0 R')
            assert streams == [[hashlib.sha256(doc.xref_stream(x)).hexdigest() for x in p.get_contents()] for p in doc]
            merged.insert_pdf(doc)
            checked.append(filename)
    pdf = destination/'Origin_scientific_color_reference.pdf'
    merged.set_metadata({'title': 'Origin scientific colour reference',
                         'subject': 'Synthetic native Origin examples and sourced colour maps; no study data'})
    merged.save(pdf, deflate=True)
    merged.close()
    with fitz.open(pdf) as doc:
        assert len(doc) == 4
        for i, page in enumerate(doc):
            assert not page.get_images()
            for ref, _, kind, name, *_ in page.get_fonts(full=True):
                assert kind == 'Type3' or doc.extract_font(ref)[3], name
            for word in page.get_text('words'):
                assert fitz.Rect(word[:4]) in page.rect, (i, word)
            page.get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False).save(destination/f'page_{i+1}.png')
    (destination/'reference_validation.json').write_text(json.dumps(dict(pages=4, native_origin_pages=2,
        vector_palette_pages=2, no_raster_images=True, all_fonts_embedded=True, text_inside_page=True,
        drawing_streams_unchanged=True, inputs=checked), indent=2), encoding='utf-8')
    print(pdf)


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source', type=Path, required=True)
    p.add_argument('--out', type=Path, required=True)
    args = p.parse_args()
    assemble(args.source.resolve(), args.out.resolve())
