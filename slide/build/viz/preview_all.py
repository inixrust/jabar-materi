# -*- coding: utf-8 -*-
"""Render semua ilustrasi pada satu modul spesifikasi ke C:/Users/inixindo/AppData/Local/Temp/claude/c0e5d4da64472f57/a0721b0d-5681-4d5c-adf7-1b675b16337e/scratchpad/viz_prev dan cetak peringatan.
Pemakaian: cd /home/claude/slides/build && python3 -m viz.preview_all <nama_modul> [judul-sebagian]
"""
import sys, importlib, os, re
mod = importlib.import_module('viz.specs.' + sys.argv[1])
flt = sys.argv[2].lower() if len(sys.argv) > 2 else None
os.makedirs('C:/Users/inixindo/AppData/Local/Temp/claude/c0e5d4da64472f57/a0721b0d-5681-4d5c-adf7-1b675b16337e/scratchpad/viz_prev', exist_ok=True)
bad = 0
for i, (title, fn) in enumerate(mod.SPECS.items(), 1):
    if flt and flt not in title.lower():
        continue
    d = fn()
    out = f'C:/Users/inixindo/AppData/Local/Temp/claude/c0e5d4da64472f57/a0721b0d-5681-4d5c-adf7-1b675b16337e/scratchpad/viz_prev/{sys.argv[1]}_{i:02d}.png'
    w = d.preview(out)
    nl = len(d.layers)
    msgs = list(w)
    if nl > 5: msgs.append(f'layer {nl} > 5')
    for k, L in enumerate(d.layers, 1):
        if len(L['point']) > 52: msgs.append(f'point {k} terlalu panjang ({len(L["point"])}): {L["point"][:30]}')
        if len(L['say']) < 80: msgs.append(f'say {k} terlalu singkat')
        if not L['ask']: msgs.append(f'ask {k} kosong')
    if len(d.takeaway) > 72: msgs.append(f'takeaway terlalu panjang ({len(d.takeaway)})')
    if not d.takeaway: msgs.append('takeaway kosong')
    if len(d.analogy) > 160: msgs.append(f'analogy terlalu panjang ({len(d.analogy)})')
    if len(d.baca) < 80: msgs.append('baca terlalu singkat')
    print(f'{i:02d} {title}  -> {out}  layers={nl}', ('| PERINGATAN: ' + '; '.join(msgs)) if msgs else '| OK')
    bad += len(msgs)
print('total peringatan:', bad)
