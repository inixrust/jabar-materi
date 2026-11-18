# -*- coding: utf-8 -*-
"""Kit ilustrasi INIXINDO untuk slide Foundation CPUX-F.

Kanvas 610 x 335 satuan (1 satuan = 0.01 inci; gambar tampil 6.1 x 3.35 inci di slide).
Teks minimal 14 satuan (≈10 pt) dan disarankan 16-18 satuan agar terbaca dari belakang kelas.

Pemakaian:
    from viz.kit import D
    d = D('Judul slide', baca='Gambar ini menunjukkan ...')
    d.base_label(...)                      # elemen yang selalu tampak (opsional)
    with d.layer('Poin singkat (<=75 huruf)', say='Yang diucapkan instruktur...', ask='Pertanyaan pemantik'):
        d.label(...); d.arrow(...)
    d.takeaway = 'Kalimat kunci ujian'     # kartu merah di panel
    d.analogy = 'Analogi satu kalimat'     # bar biru di bawah
    return d
"""
import json, os, re, hashlib
from contextlib import contextmanager
from PIL import ImageFont
import cairosvg

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 610, 335
PAL = dict(red='#C00000', blue='#0E5A8A', dark='#1A1A1A', grey='#5A6570', card='#F2F2F2', pink='#FBEAEA',
           lblue='#E8F0F6', green='#2E7D32', lgreen='#D5ECC8', yel='#F5B301', lyel='#FFF3CC', white='#FFFFFF',
           lgrey='#D0D5DA', skin='#F2C9A5', navy='#083A5C', orange='#E07B00', dred='#7A0000', mid='#9AA5B1')
FONT_R = 'C:/Windows/Fonts/calibri.ttf'
FONT_B = 'C:/Windows/Fonts/calibrib.ttf'
_fr = ImageFont.truetype(FONT_R, 100)
_fb = ImageFont.truetype(FONT_B, 100)
_ICONS = None
MIN_FONT = 14


def col(c):
    return PAL.get(c, c)


def tw(s, size, bold=False):
    return (_fb if bold else _fr).getlength(s) * size / 100.0


def wrap(s, size, maxw, bold=False):
    out = []
    for para in str(s).split('\n'):
        words = para.split(' ')
        cur = ''
        for w in words:
            t = (cur + ' ' + w).strip()
            if tw(t, size, bold) <= maxw or not cur:
                cur = t
            else:
                out.append(cur)
                cur = w
        out.append(cur)
    return out


def esc(s):
    return str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def icons():
    global _ICONS
    if _ICONS is None:
        _ICONS = json.load(open(os.path.join(HERE, 'fa_icons.json')))
    return _ICONS


class D:
    def __init__(self, title, baca=''):
        self.title = title
        self.baca = baca            # penjelasan umum gambar untuk notes (apa yang dilihat dan cara membaca)
        self.tanya = ''
        self.takeaway = ''
        self.analogy = ''
        self.base = []
        self.layers = []
        self._cur = self.base
        self.warn = []
        self.bg = None              # warna latar panggung (None = dari template)

    # ------------------------------------------------------------ layer
    @contextmanager
    def layer(self, point, say='', ask=''):
        L = {'point': point, 'say': say, 'ask': ask, 'els': []}
        self.layers.append(L)
        prev = self._cur
        self._cur = L['els']
        try:
            yield
        finally:
            self._cur = prev

    def _add(self, s):
        self._cur.append(s)

    # ------------------------------------------------------------ bentuk dasar
    def rect(self, x, y, w, h, fill='card', stroke=None, sw=2, r=10, dash=None, opacity=1.0, shadow=False):
        a = ''
        if stroke:
            a += f' stroke="{col(stroke)}" stroke-width="{sw}"'
        if dash:
            a += f' stroke-dasharray="{dash}"'
        if opacity != 1.0:
            a += f' opacity="{opacity}"'
        f = col(fill) if fill else 'none'
        if shadow:
            self._add(f'<rect x="{x + 2}" y="{y + 3}" width="{w}" height="{h}" rx="{r}" fill="#000" opacity="0.10"/>')
        self._add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{f}"{a}/>')

    def circle(self, cx, cy, r, fill='card', stroke=None, sw=2, dash=None, opacity=1.0):
        a = ''
        if stroke:
            a += f' stroke="{col(stroke)}" stroke-width="{sw}"'
        if dash:
            a += f' stroke-dasharray="{dash}"'
        if opacity != 1.0:
            a += f' opacity="{opacity}"'
        self._add(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{col(fill) if fill else "none"}"{a}/>')

    def ellipse(self, cx, cy, rx, ry, fill='card', stroke=None, sw=2, dash=None, opacity=1.0):
        a = ''
        if stroke:
            a += f' stroke="{col(stroke)}" stroke-width="{sw}"'
        if dash:
            a += f' stroke-dasharray="{dash}"'
        if opacity != 1.0:
            a += f' opacity="{opacity}"'
        self._add(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{col(fill) if fill else "none"}"{a}/>')

    def line(self, x1, y1, x2, y2, color='grey', sw=3, dash=None, cap='round'):
        a = f' stroke-dasharray="{dash}"' if dash else ''
        self._add(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{col(color)}" stroke-width="{sw}" stroke-linecap="{cap}"{a}/>')

    def path(self, d, fill=None, stroke='grey', sw=3, dash=None, opacity=1.0):
        a = f' stroke-dasharray="{dash}"' if dash else ''
        if opacity != 1.0:
            a += f' opacity="{opacity}"'
        self._add(f'<path d="{d}" fill="{col(fill) if fill else "none"}" stroke="{col(stroke) if stroke else "none"}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"{a}/>')

    def polygon(self, pts, fill='card', stroke=None, sw=2, opacity=1.0):
        p = ' '.join(f'{x},{y}' for x, y in pts)
        a = f' stroke="{col(stroke)}" stroke-width="{sw}" stroke-linejoin="round"' if stroke else ''
        if opacity != 1.0:
            a += f' opacity="{opacity}"'
        self._add(f'<polygon points="{p}" fill="{col(fill)}"{a}/>')

    def arrow(self, x1, y1, x2, y2, color='red', sw=4, head=12, dash=None, curve=0, both=False):
        """Panah lurus (curve=0) atau lengkung (curve = pergeseran titik kontrol tegak lurus)."""
        import math
        c = col(color)
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        dx, dy = x2 - x1, y2 - y1
        L = math.hypot(dx, dy) or 1
        nx, ny = -dy / L, dx / L
        cx, cy = mx + nx * curve, my + ny * curve
        # arah ujung
        ex, ey = (x2 - cx, y2 - cy) if curve else (dx, dy)
        sx, sy = (cx - x1, cy - y1) if curve else (dx, dy)
        el = math.hypot(ex, ey) or 1
        ux, uy = ex / el, ey / el
        sl = math.hypot(sx, sy) or 1
        vx, vy = sx / sl, sy / sl
        # potong garis agar tidak menembus kepala panah
        x2b, y2b = x2 - ux * head * 0.7, y2 - uy * head * 0.7
        x1b, y1b = (x1 + vx * head * 0.7, y1 + vy * head * 0.7) if both else (x1, y1)
        da = f' stroke-dasharray="{dash}"' if dash else ''
        if curve:
            self._add(f'<path d="M{x1b},{y1b} Q{cx},{cy} {x2b},{y2b}" fill="none" stroke="{c}" stroke-width="{sw}" stroke-linecap="round"{da}/>')
        else:
            self._add(f'<line x1="{x1b}" y1="{y1b}" x2="{x2b}" y2="{y2b}" stroke="{c}" stroke-width="{sw}" stroke-linecap="round"{da}/>')

        def headpoly(px, py, dx_, dy_):
            bx, by = px - dx_ * head, py - dy_ * head
            wx, wy = -dy_ * head * 0.55, dx_ * head * 0.55
            self._add(f'<polygon points="{px},{py} {bx + wx},{by + wy} {bx - wx},{by - wy}" fill="{c}"/>')
        headpoly(x2, y2, ux, uy)
        if both:
            headpoly(x1, y1, -vx, -vy)

    # ------------------------------------------------------------ teks
    def text(self, x, y, s, size=17, color='dark', bold=False, anchor='middle', maxw=None, lh=1.18, italic=False):
        """y = titik tengah vertikal blok teks. maxw → bungkus otomatis."""
        if size < MIN_FONT:
            self.warn.append(f'font {size} < {MIN_FONT}: {str(s)[:30]}')
        lines = wrap(s, size, maxw, bold) if maxw else str(s).split('\n')
        n = len(lines)
        y0 = y - (n - 1) * size * lh / 2
        fw = ' font-weight="700"' if bold else ''
        fs = ' font-style="italic"' if italic else ''
        for i, ln in enumerate(lines):
            self._add(f'<text x="{x}" y="{y0 + i * size * lh}" font-family="Calibri" font-size="{size}"{fw}{fs} fill="{col(color)}" '
                      f'text-anchor="{anchor}" dominant-baseline="central">{esc(ln)}</text>')
        return n * size * lh

    def label(self, x, y, w, h, s, fill='blue', color='white', size=17, bold=True, r=10, stroke=None, sw=2, dash=None,
              shadow=False, pad=8, minsize=14, align='middle'):
        """Kotak bertulisan. Ukuran huruf diturunkan otomatis sampai muat (min `minsize`)."""
        self.rect(x, y, w, h, fill=fill, stroke=stroke, sw=sw, r=r, dash=dash, shadow=shadow)
        sz = size
        while True:
            lines = wrap(s, sz, w - 2 * pad, bold)
            if len(lines) * sz * 1.18 <= h - 6 or sz <= minsize:
                break
            sz -= 1
        if len(lines) * sz * 1.18 > h - 4 or any(tw(l, sz, bold) > w - 2 * pad + 1 for l in lines):
            self.warn.append(f'teks meluap: "{str(s)[:30]}" ({w}x{h})')
        tx = x + w / 2 if align == 'middle' else x + pad
        self.text(tx, y + h / 2, s, size=sz, color=color, bold=bold, anchor=align if align != 'middle' else 'middle', maxw=w - 2 * pad)

    def pill(self, x, y, w, h, s, fill='blue', color='white', size=16, bold=True, **k):
        self.label(x, y, w, h, s, fill=fill, color=color, size=size, bold=bold, r=h / 2, **k)

    def badge(self, cx, cy, n, r=13, fill='red', color='white', size=16):
        self.circle(cx, cy, r, fill=fill)
        self.text(cx, cy + 0.5, str(n), size=size, color=color, bold=True)

    # ------------------------------------------------------------ ikon vektor
    def icon(self, name, cx, cy, size=30, color='blue', opacity=1.0):
        ic = icons().get(name)
        if not ic:
            self.warn.append(f'ikon tidak ada: {name}')
            return
        vb = [float(v) for v in ic['vb'].split()]
        s = size / max(vb[2], vb[3])
        tx = cx - vb[2] * s / 2 - vb[0] * s
        ty = cy - vb[3] * s / 2 - vb[1] * s
        op = f' opacity="{opacity}"' if opacity != 1.0 else ''
        self._add(f'<g transform="translate({tx},{ty}) scale({s})" fill="{col(color)}"{op}>{ic["inner"]}</g>')

    def iconcircle(self, cx, cy, r, name, fill='blue', color='white', scale=0.52, stroke=None):
        self.circle(cx, cy, r, fill=fill, stroke=stroke)
        self.icon(name, cx, cy, r * 2 * scale, color=color)

    # ------------------------------------------------------------ tokoh
    def person(self, cx, cy, s=1.0, color='blue', skin='skin', label=None, label_size=15, label_color='dark', acc=None, acc_color='white'):
        """Tokoh sederhana. (cx, cy) = pusat kepala; tinggi total ≈ 68*s di bawah kepala. label di bawah tubuh."""
        hr = 13 * s
        self.circle(cx, cy, hr, fill=skin)
        bw = 38 * s
        top = cy + hr + 3 * s
        self.path(f'M{cx - bw / 2},{top + 36 * s} Q{cx - bw / 2},{top} {cx},{top} Q{cx + bw / 2},{top} {cx + bw / 2},{top + 36 * s} Z',
                  fill=color, stroke=None, sw=0)
        if acc:
            self.icon(acc, cx, top + 20 * s, 17 * s, color=acc_color)
        if label:
            self.text(cx, top + 36 * s + 11 + label_size / 2, label, size=label_size, color=label_color, bold=True)

    # ------------------------------------------------------------ perangkat dan UI tiruan
    def phone(self, x, y, w, h, screen='white', body='navy'):
        self.rect(x, y, w, h, fill=body, r=16)
        self.rect(x + 5, y + 14, w - 10, h - 26, fill=screen, r=5)
        self.circle(x + w / 2, y + 7, 2.5, fill='mid')

    def browser(self, x, y, w, h, title='', screen='white'):
        self.rect(x, y, w, h, fill=screen, stroke='lgrey', sw=2, r=8)
        self.rect(x, y, w, 20, fill='lgrey', r=8)
        self.rect(x, y + 12, w, 8, fill='lgrey', r=0)
        for i, c in enumerate(('red', 'yel', 'green')):
            self.circle(x + 11 + i * 12, y + 10, 3.5, fill=c)
        if title:
            self.text(x + 58, y + 10.5, title, size=14, color='grey', anchor='start')

    def ui_button(self, x, y, w, h, s, fill='blue', color='white', size=14):
        self.label(x, y, w, h, s, fill=fill, color=color, size=size, r=h / 4, pad=4, minsize=10)

    def ui_input(self, x, y, w, h, s='', size=14):
        self.rect(x, y, w, h, fill='white', stroke='mid', sw=1.5, r=4)
        if s:
            self.text(x + 6, y + h / 2, s, size=size, color='mid', anchor='start')

    def ui_lines(self, x, y, w, n=3, gap=9, color='lgrey', h=4.5):
        for i in range(n):
            ww = w if i < n - 1 else w * 0.6
            self.rect(x, y + i * gap, ww, h, fill=color, r=2)

    def bubble(self, x, y, w, h, s, tail='bl', fill='white', stroke='mid', color='dark', size=16, bold=False):
        self.rect(x, y, w, h, fill=fill, stroke=stroke, sw=2, r=12)
        tx = {'bl': x + 22, 'br': x + w - 22, 'tl': x + 22, 'tr': x + w - 22}[tail]
        if tail[0] == 'b':
            self.polygon([(tx - 7, y + h - 1), (tx + 7, y + h - 1), (tx - 2 if tail[1] == 'l' else tx + 2, y + h + 13)], fill=fill, stroke=stroke, sw=2)
            self.rect(tx - 6, y + h - 3, 12, 5, fill=fill, r=0)
        else:
            self.polygon([(tx - 7, y + 1), (tx + 7, y + 1), (tx - 2 if tail[1] == 'l' else tx + 2, y - 13)], fill=fill, stroke=stroke, sw=2)
            self.rect(tx - 6, y - 2, 12, 5, fill=fill, r=0)
        self.text(x + w / 2, y + h / 2, s, size=size, color=color, bold=bold, maxw=w - 16)

    def group(self, x, y, w, h, label='', fill='lblue', stroke='blue', dash='6 5', tab=None, size=15, r=14, sw=2):
        self.rect(x, y, w, h, fill=fill, stroke=stroke, sw=sw, r=r, dash=dash)
        if label:
            lw = tw(label, size, True) + 18
            self.rect(x + 14, y - 11, lw, 22, fill=tab or stroke, r=11)
            self.text(x + 14 + lw / 2, y, label, size=size, color='white', bold=True)

    def check(self, cx, cy, r=11):
        self.circle(cx, cy, r, fill='green')
        self.path(f'M{cx - r * .45},{cy} L{cx - r * .1},{cy + r * .38} L{cx + r * .5},{cy - r * .35}', stroke='white', sw=max(2.2, r * .22))

    def cross(self, cx, cy, r=11):
        self.circle(cx, cy, r, fill='red')
        k = r * .4
        self.path(f'M{cx - k},{cy - k} L{cx + k},{cy + k} M{cx - k},{cy + k} L{cx + k},{cy - k}', stroke='white', sw=max(2.2, r * .22))

    # ------------------------------------------------------------ keluaran
    def _svg(self, els):
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
                + ''.join(els) + '</svg>')

    def render(self, outdir, scale=3, tag=None):
        """Render base dan tiap layer ke PNG transparan berukuran sama. Mengembalikan {'base': path|None, 'layers': [path]}."""
        os.makedirs(outdir, exist_ok=True)
        tag = tag or re.sub(r'[^a-z0-9]+', '_', self.title.lower())[:40]
        res = {'base': None, 'layers': []}

        def put(name, els):
            svg = self._svg(els)
            h = hashlib.md5(svg.encode()).hexdigest()[:8]
            p = os.path.join(outdir, f'{tag}_{name}_{h}.png')
            if not os.path.exists(p):
                cairosvg.svg2png(bytestring=svg.encode(), write_to=p, output_width=W * scale, output_height=H * scale)
            return p
        if self.base:
            res['base'] = put('base', self.base)
        for i, L in enumerate(self.layers, 1):
            res['layers'].append(put(f'L{i}', L['els']))
        return res

    def preview(self, path, upto=None, bg='#F5F8FB'):
        """Kontak-sheet tahap-tahap (komulatif) untuk QA visual."""
        from PIL import Image
        n = len(self.layers) if upto is None else upto
        tmp = os.path.join(os.path.dirname(path) or '.', '_pv')
        r = self.render(tmp, scale=2)
        frames = []
        for k in range(0, n + 1):
            im = Image.new('RGBA', (W * 2, H * 2), bg)
            for pth in ([r['base']] if r['base'] else []) + r['layers'][:k]:
                im.alpha_composite(Image.open(pth).convert('RGBA'))
            frames.append(im.convert('RGB'))
        cols = 2 if len(frames) > 2 else len(frames)
        rows = (len(frames) + cols - 1) // cols
        sheet = Image.new('RGB', (cols * W * 2 + (cols + 1) * 10, rows * H * 2 + (rows + 1) * 10), 'white')
        for i, fr in enumerate(frames):
            sheet.paste(fr, (10 + (i % cols) * (W * 2 + 10), 10 + (i // cols) * (H * 2 + 10)))
        sheet.save(path)
        return self.warn
