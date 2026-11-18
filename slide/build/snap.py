import sys, json, copy, subprocess, os, glob
from pptx import Presentation
deck, outdir = sys.argv[1], sys.argv[2]
req = [tuple(map(int, a.split(':'))) for a in sys.argv[3:]]   # slide:state (state = jumlah klik sudah dijalankan)
P = json.load(open(os.path.join(os.path.dirname(deck) or '.', 'anim_plan.json')))
os.makedirs(outdir, exist_ok=True)
for n, k in req:
    prs = Presentation(deck)
    lst = prs.slides._sldIdLst
    ids = list(lst)
    for i, sid in enumerate(ids, 1):
        if i != n:
            prs.part.drop_rel(sid.rId); lst.remove(sid)
    s = prs.slides[0]
    clicks = P.get(str(n), [])
    hide = set()
    for c in clicks[k:]:
        hide |= set(c['ids'])
    # bentuk yang akan muncul dan belum muncul pada state ini
    for sh in list(s.shapes):
        if sh.shape_id in hide:
            sh._element.getparent().remove(sh._element)
    # buang timing agar render statis
    for el in s._element.findall('{http://schemas.openxmlformats.org/presentationml/2006/main}timing'):
        s._element.remove(el)
    name = f'{outdir}/s{n:03d}_k{k}.pptx'
    prs.save(name)
    subprocess.run(['soffice', '--headless', '--convert-to', 'pdf', '--outdir', outdir, name], capture_output=True)
    subprocess.run(['pdftoppm', '-r', '55', '-png', '-singlefile', name.replace('.pptx', '.pdf'), name.replace('.pptx', '')])
print('ok')
