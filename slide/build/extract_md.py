# -*- coding: utf-8 -*-
"""Ekspor penjelasan konten deck ke Markdown (+ img/ berisi ilustrasi gabungan semua layer).
    python3 extract_md.py <out-dir> --title "Judul Pelatihan" [--deck nama.pptx] [--repo /path/repo-lab] [--md nama.md]
Membangun ulang struktur deck di memori (tanpa menyimpan pptx) lalu menulis: judul, jenis, durasi, isi komponen,
ilustrasi + urutan klik, code + penjelasan per baris (+ path file di repo lab bila --repo), lab, kuis, notes, sumber."""
import sys, os, re, argparse, importlib, importlib.util
sys.path.insert(0, '.')
import lib
import code as codemod

ap = argparse.ArgumentParser()
ap.add_argument('out')
ap.add_argument('--title', required=True)
ap.add_argument('--deck', default='deck.pptx')
ap.add_argument('--repo', default=None)
ap.add_argument('--md', default='Penjelasan_Slide.md')
ARGS = ap.parse_args()
OUT = ARGS.out
IMG = os.path.join(OUT, 'img')
os.makedirs(IMG, exist_ok=True)

# ---- tangkap argumen code_slide dan ex_slide
_orig_code = codemod.code_slide
def code_slide(modul, mins, title, code, notes, marks, practice, fname='', lang='java', size=None):
    s = _orig_code(modul, mins, title, code, notes, marks, practice, fname=fname, lang=lang, size=size)
    e = [x for x in lib.SL if x['title'] == title][-1]
    e['code'] = dict(code=code.strip('\n'), marks=marks, practice=practice, fname=fname, lang=lang)
    return s
codemod.code_slide = code_slide

_orig_ex = lib.ex_slide
def ex_slide(modul, ex, short, mins, steps, jebakan=None, notes=None, tujuan=None, fmt=None):
    s = _orig_ex(modul, ex, short, mins, steps, jebakan=jebakan, notes=notes, tujuan=tujuan, fmt=fmt)
    lib.SL[-1]['ex'] = dict(ex=ex, steps=steps, jebakan=jebakan, tujuan=tujuan, fmt=fmt, mins=mins)
    return s
lib.ex_slide = ex_slide

_orig_tf = lib.tf_slide
def tf_slide(modul, mins, title, stmts, answers, notes=None):
    s = _orig_tf(modul, mins, title, stmts, answers, notes=notes)
    lib.SL[-1]['tf'] = dict(stmts=stmts, answers=answers)
    return s
lib.tf_slide = tf_slide

lib.init()
for name in [f'c{i}' for i in range(1, 11)]:
    if importlib.util.find_spec(name) is None:
        continue
    m = importlib.import_module(name)
    for attr in ('ex_slide', 'tf_slide'):
        if hasattr(m, attr):
            setattr(m, attr, getattr(lib, attr))
    if hasattr(m, 'code_slide'):
        m.code_slide = code_slide
    for fn in ('pre',) + tuple(f'day{i}' for i in range(1, 11)) + ('penutup',):
        if hasattr(m, fn):
            getattr(m, fn)()
lib.finalize()

# ---- ilustrasi: gabungkan base + layer menjadi satu PNG
from PIL import Image
reg = lib._load_vis()
def compose(title):
    d = reg[title]()
    r = d.render(lib.VIS_DIR)
    paths = ([r['base']] if r['base'] else []) + list(r['layers'])
    im = None
    for p in paths:
        L = Image.open(p).convert('RGBA')
        if im is None:
            im = Image.new('RGBA', L.size, (245, 248, 251, 255))
        im.alpha_composite(L.resize(im.size))
    slug = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')[:60]
    fn = f'{slug}.png'
    im.convert('RGB').save(os.path.join(IMG, fn), optimize=True)
    return fn, [L['point'] for L in d.layers], d.takeaway, getattr(d, 'baca', '')

# ---- util teks
ICON = re.compile(r'^(Fa|Md|Io|Bs|Gi|Bi|Ri)[A-Z][A-Za-z0-9]+$')
REPO = ARGS.repo
REPO_FILES = {}
for root, dirs, files in (os.walk(REPO) if REPO else []):
    dirs[:] = [d for d in dirs if d not in ('target', '.git', 'logs')]
    for f_ in files:
        REPO_FILES.setdefault(f_, []).append(os.path.relpath(os.path.join(root, f_), REPO))
def flat(x):
    if x is None: return ''
    if isinstance(x, str): return '' if ICON.match(x) else x
    if isinstance(x, (int, float)): return str(x)
    if isinstance(x, dict):
        for k in ('runs', 'text', 'title', 'point'):
            if k in x: return flat(x[k])
        return ' — '.join(flat(v) for v in x.values() if isinstance(v, (str, list, tuple)))
    if isinstance(x, (list, tuple)):
        parts = [flat(v) for v in x]
        return ' — '.join(p for p in parts if p and p.strip())
    return ''

def clean(t):
    return re.sub(r'\s+', ' ', t.replace('­', '')).strip()

def md_table(header, data):
    esc = lambda c: clean(flat(c)).replace('|', '\\|')
    out = ['| ' + ' | '.join(esc(h) for h in header) + ' |', '|' + '---|' * len(header)]
    out += ['| ' + ' | '.join(esc(c) for c in row) + ' |' for row in data]
    return '\n'.join(out)

# label notes dikenali dari kata kuncinya (emoji di depannya diabaikan)
LABELS = {'BUKA': 'Pembuka', 'GAMBAR': 'Gambar', 'TANYA': 'Pertanyaan', 'INTI': 'Inti', 'NUANSA': 'Nuansa',
          'JEBAKAN': 'Jebakan', 'JEBAKAN UJIAN': 'Jebakan', 'LATIHAN': 'Saat latihan', 'BILA SEPI': 'Bila kelas sepi',
          'PERSIAPAN': 'Persiapan', 'JAWABAN': 'Jawaban', 'SUMBER': 'Sumber'}
LABEL_RE = re.compile(r'^\S+\s+(' + '|'.join(sorted(LABELS, key=len, reverse=True)) + r'):\s*(.*)$')
SKIP_RE = re.compile(r'^\S+\s+(KLIK:|TRANSISI:|URUTAN KLIK|±\d)')

def notes_md(slide):
    try:
        text = slide.notes_slide.notes_text_frame.text
    except Exception:
        return [], ''
    items, src = [], ''
    for line in text.split('\n'):
        line = line.strip()
        if not line or SKIP_RE.match(line):
            continue
        m = LABEL_RE.match(line)
        if m:
            lab, body = LABELS[m.group(1)], m.group(2).strip()
            if lab == 'Sumber':
                src = body
            else:
                items.append((lab, body))
        elif re.match(r'^Klik \d+', line):
            items.append(('§', line))
        else:
            items.append(('·', line))
    return items, src

def part_md(p):
    k, a = p['kind'], p.get('a') or ()
    kw = p.get('k') or {}
    out = []
    if k == 'table':
        header, data = a[0], a[1]
        out.append(md_table(header, data))
    elif k in ('rows',):
        for it in a[0]:
            if isinstance(it, (list, tuple)) and len(it) >= 2:
                out.append(f'- **{clean(flat(it[0]))}**: {clean(flat(it[1:]))}')
            else:
                out.append(f'- {clean(flat(it))}')
    elif k in ('keys', 'numbered_steps'):
        for i, it in enumerate(a[0], 1):
            out.append(f'{i}. {clean(flat(it))}' if k == 'numbered_steps' else f'- {clean(flat(it))}')
    elif k in ('cards', 'flow', 'pairs', 'trap_rows'):
        for it in a[0]:
            if isinstance(it, (list, tuple)):
                it = [v for v in it if not (isinstance(v, str) and ICON.match(v))]
            if isinstance(it, (list, tuple)) and len(it) >= 2:
                out.append(f'- **{clean(flat(it[0]))}**: {clean(flat(it[1:]))}')
            elif isinstance(it, dict):
                ttl = flat(it.get('title') or it.get('t') or '')
                rest = clean(flat({kk: vv for kk, vv in it.items() if kk not in ('title', 't', 'icon')}))
                out.append(f'- **{clean(ttl)}**: {rest}' if ttl else f'- {rest}')
            else:
                out.append(f'- {clean(flat(it))}')
    elif k == 'compare':
        L, R = a[0], a[1]
        for side in (L, R):
            if isinstance(side, dict):
                out.append(f'- **{clean(flat(side.get("title", "")))}**: ' + '; '.join(clean(flat(x)) for x in side.get('items', [])))
            else:
                out.append(f'- {clean(flat(side))}')
    elif k in ('analogy', 'bottom_pill', 'bottom_callout', 'callout'):
        t = next((x for x in a if isinstance(x, str)), '')
        if t:
            out.append(f'> {clean(t)}')
    return '\n'.join(out)

# ---- susun markdown
md = []
toc = []
n = 0
cur_day = None
for e in lib.SL:
    n += 1
    s = e['slide']
    title = clean(e['title'])
    if e['kind'] == 'cover':
        hdr = clean(e.get('eyebrow', '')) or title
        md.append(f'\n---\n\n## {hdr}\n')
        toc.append(f'- [{hdr}](#{re.sub(r"[^a-z0-9 -]", "", hdr.lower()).replace(" ", "-")})')
        items, src = notes_md(s)
        for lab, body in items:
            md.append(f'- **{lab}:** {body}' if lab else f'- {body}')
        md.append('')
        continue
    if e['kind'] == 'finish':
        continue
    modul = e.get('modul', '')
    badge = e.get('badge') or ''
    mins = e.get('mins')
    md.append(f'### {n}. {title}\n')
    meta = ' · '.join(x for x in dict.fromkeys([modul, badge, f'±{mins} menit' if mins else '']) if x)
    if meta:
        md.append(f'*{meta}*\n')

    if e.get('visual') and title in reg:
        fn, points, takeaway, baca = compose(title)
        md.append(f'![{title}](img/{fn})\n')
        md.append('Ilustrasi dibuka per klik, satu gagasan per lapisan:\n')
        for i, pt in enumerate(points, 1):
            md.append(f'{i}. {clean(pt)}')
        if takeaway:
            md.append(f'\n> **Poin kunci:** {clean(takeaway)}')
        md.append('')
    if 'code' in e:
        c = e['code']
        lang = {'properties': 'properties', 'yaml': 'yaml', 'bash': 'bash', 'sql': 'sql', 'text': 'text', 'js': 'js', 'ts': 'tsx', 'json': 'json', 'md': 'markdown'}.get(c['lang'], 'java')
        if c['fname']:
            hits = REPO_FILES.get(c['fname'], [])
            where = (' · di repo: ' + ', '.join(f'`{h}`' for h in hits[:2])) if hits else ''
            md.append(f'`{c["fname"]}`{where}\n')
        md.append(f'```{lang}\n{c["code"]}\n```\n')
        md.append('Penjelasan per baris:\n')
        for m in c['marks']:
            a, b, txt = m[0], m[1], m[2]
            rng = f'baris {a}' if a == b else f'baris {a}–{b}'
            md.append(f'- **{rng}:** {clean(txt)}')
        md.append(f'\n> **Best practice:** {clean(c["practice"])}\n')
    elif 'ex' in e:
        x = e['ex']
        md.append(f'**Format:** {x["fmt"] or "-"} · **Durasi:** {x["mins"]} menit · panduan repo: `docs/labs/{x["ex"]}.md`\n')
        if x['tujuan']:
            md.append(f'**Tujuan:** {clean(x["tujuan"])}\n')
        md.append('**Langkah:**\n')
        for i, st in enumerate(x['steps'], 1):
            md.append(f'{i}. {clean(flat(st))}')
        if x['jebakan']:
            md.append(f'\n> **Jebakan umum:** {clean(x["jebakan"])}')
        md.append('')
    elif 'tf' in e:
        md.append('**Pernyataan (Benar/Salah):**\n')
        for i, (st, (ans, why)) in enumerate(zip(e['tf']['stmts'], e['tf']['answers']), 1):
            md.append(f'{i}. {clean(st)}  \n   **{ans}**: {clean(why)}')
        md.append('')
    elif not e.get('visual'):
        body = [part_md(p) for p in e.get('parts', [])]
        body = [b for b in body if b.strip()]
        if body:
            md.append('\n\n'.join(body) + '\n')

    items, src = notes_md(s)
    if 'code' in e:
        items = [it for it in items if it[0] != 'Gambar']
    if 'tf' in e:
        items = [it for it in items if it[0] != 'Jawaban']
    if items:
        md.append('**Penjelasan untuk instruktur:**\n')
        for lab, body in items:
            if lab == '§':
                md.append(f'- **{clean(body)}**')
            elif lab == '·':
                md.append(f'  - {clean(body)}')
            else:
                md.append(f'- **{lab}:** {clean(body)}')
        md.append('')
    if src:
        md.append(f'*Sumber: {clean(src)}*\n')

head = f'''# {ARGS.title}

**Penjelasan konten slide instruktur (versi Markdown)** · Inixindo Bandung · {n} slide

Padanan teks dari deck *{ARGS.deck}*: setiap slide berisi judul, isi utama (tabel, poin, code dengan penjelasan per
baris, langkah lab), ilustrasi (gambar gabungan semua lapisan klik), penjelasan untuk instruktur dari speaker notes,
dan sumber rujukan.

## Daftar isi

''' + '\n'.join(toc) + '\n'

text = head + '\n'.join(md).replace('\n\n\n', '\n\n')
with open(os.path.join(OUT, ARGS.md), 'w', encoding='utf-8') as f:
    f.write(text)
print('slides', n, 'images', len(os.listdir(IMG)), 'chars', len(text))
