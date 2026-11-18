# -*- coding: utf-8 -*-
"""Gabungkan PNG hasil render menjadi lembar kontak.
Pemakaian: python sheet.py <folder_png> <keluaran.png> [kolom] [pola]"""
import sys, glob, os
from PIL import Image, ImageDraw

src, out = sys.argv[1], sys.argv[2]
cols = int(sys.argv[3]) if len(sys.argv) > 3 else 3
pat = sys.argv[4] if len(sys.argv) > 4 else '*.png'
files = sorted(glob.glob(os.path.join(src, pat)))
if not files:
    sys.exit('tidak ada png')
w, h = Image.open(files[0]).size
pad = 26
rows = (len(files) + cols - 1) // cols
sheet = Image.new('RGB', (cols * w, rows * (h + pad)), 'white')
d = ImageDraw.Draw(sheet)
for i, f in enumerate(files):
    im = Image.open(f).convert('RGB').resize((w, h))
    x, y = (i % cols) * w, (i // cols) * (h + pad)
    sheet.paste(im, (x, y + pad))
    d.text((x + 6, y + 6), os.path.basename(f), fill='black')
sheet.save(out)
print(out, len(files))
