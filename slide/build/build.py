# -*- coding: utf-8 -*-
"""Bangun deck: python3 build.py [keluaran.pptx]

Modul isi slide: c1.py, c2.py, ... (fungsi pre, day1..day5 dipanggil berurutan bila ada).
Ilustrasi diambil dari viz/specs/*.py (kamus SPECS, kunci = judul slide persis).
"""
import sys, importlib, importlib.util
sys.path.insert(0, '.')
import lib
lib.init()
for name in [f'c{i}' for i in range(1, 11)]:
    if importlib.util.find_spec(name) is None:      # find_spec: galat di dalam modul tidak ikut tertelan
        continue
    m = importlib.import_module(name)
    for fn in ('pre',) + tuple(f'day{i}' for i in range(1, 11)) + ('penutup',):
        if hasattr(m, fn):
            getattr(m, fn)()
lib.finalize()
out = sys.argv[1] if len(sys.argv) > 1 else 'deck.pptx'
lib.save(out)
import postprocess, promote
print('master/layout:', postprocess.run(out))
print('layout promosi:', promote.run(out))
print('slides:', lib.CUR['n'])
print('\n'.join(lib.WARN) or 'tanpa peringatan')
