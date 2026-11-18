# -*- coding: utf-8 -*-
"""Gambar keadaan akhir (semua layer) per slide, 2 slide per gambar. python3 -m viz.final <modul> [judul-sebagian]"""
import sys, importlib, os
from PIL import Image
from viz.kit import W, H
mod = importlib.import_module('viz.specs.' + sys.argv[1])
flt = sys.argv[2].lower() if len(sys.argv) > 2 else None
os.makedirs('C:/Users/inixindo/AppData/Local/Temp/claude/c0e5d4da64472f57/a0721b0d-5681-4d5c-adf7-1b675b16337e/scratchpad/viz_fin', exist_ok=True)
fr = []
for i, (t, fn) in enumerate(mod.SPECS.items(), 1):
    if flt and flt not in t.lower(): continue
    d = fn(); r = d.render('C:/Users/inixindo/AppData/Local/Temp/claude/c0e5d4da64472f57/a0721b0d-5681-4d5c-adf7-1b675b16337e/scratchpad/viz_fin/_r', scale=2)
    im = Image.new('RGBA', (W*2, H*2), '#F5F8FB')
    for p in ([r['base']] if r['base'] else []) + r['layers']:
        im.alpha_composite(Image.open(p).convert('RGBA'))
    fr.append((i, t, im.convert('RGB')))
for k in range(0, len(fr), 2):
    ch = fr[k:k+2]
    sh = Image.new('RGB', (W*2, len(ch)*(H*2+10)), 'white')
    for j, (i, t, im) in enumerate(ch): sh.paste(im, (0, j*(H*2+10)))
    p = f'C:/Users/inixindo/AppData/Local/Temp/claude/c0e5d4da64472f57/a0721b0d-5681-4d5c-adf7-1b675b16337e/scratchpad/viz_fin/{sys.argv[1]}_f{k//2+1}.png'; sh.save(p); print(p, [c[0] for c in ch])
