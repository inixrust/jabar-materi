# -*- coding: utf-8 -*-
"""QA integritas XML + notes (references/deck-engine.md). Pemakaian: python qa.py deck.pptx"""
import sys
from pptx import Presentation
p = Presentation(sys.argv[1]); bad = 0
for i, s in enumerate(p.slides, 1):
    ids = [int(x) for x in s._element.xpath('.//p:cNvPr/@id')]
    if len(ids) != len(set(ids)): bad += 1; print('id ganda', i)
    tgt = set(int(x) for x in s._element.xpath('.//p:timing//@spid'))
    if not tgt <= set(ids): bad += 1; print('target animasi hilang', i)
    t = [int(x) for x in s._element.xpath('.//p:timing//p:cTn/@id')]
    if t != sorted(t) or len(t) != len(set(t)): bad += 1; print('cTn tak unik/tak naik', i)
    try:
        n = s.notes_slide.notes_text_frame.text
    except Exception:
        n = ''
    if len(n) < 80 and s.slide_layout.name not in ('Penutup',): bad += 1; print('notes pendek', i, len(n))
print('slides:', len(p.slides), 'masalah:', bad)
