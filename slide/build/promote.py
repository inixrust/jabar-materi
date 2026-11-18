# -*- coding: utf-8 -*-
"""Promosi pola slide yang berulang menjadi layout slide master.

Tiga layout baru (dikloning dari 'Konten' agar latar dan footer sama):
  - Ilustrasi + Poin     : kerangka panggung gambar (statis) + placeholder gambar, poin, kunci ujian, analogi
  - Latihan Terpandu     : tiga pil info, kartu TUJUAN (statis) + placeholder tujuan, langkah, jebakan
  - Judul Merah          : judul merah tanpa label + placeholder subjudul

Slide yang cocok dipindah ke layout baru; bagian statis (kerangka) dipindah dari slide ke layout,
teks statis dijadikan placeholder. Bagian yang beranimasi TIDAK disentuh (id bentuk dan animasi tetap).
"""
import copy
import sys
import uuid

from lxml import etree
from pptx import Presentation
from pptx.opc.constants import RELATIONSHIP_TYPE as RT
from pptx.opc.packuri import PackURI
from pptx.parts.slide import SlideLayoutPart

from postprocess import NS, A, P, NSDECL, X, xfrm, _geom, _near, _to_ph, G_NUM, G_TITLE_WIDE

E = 914400


def emu(v):
    return int(round(v * E))


def g_in(x, y, w, h):
    return (emu(x), emu(y), emu(w), emu(h))


STAGE = g_in(0.4, 1.12, 6.1, 3.35)
POIN = g_in(6.68, 1.12, 2.92, 3.35 - 0.74 - 0.08)
KUNCI = g_in(6.68, 1.12 + 3.35 - 0.74, 2.92, 0.74)
ANALOGI = g_in(0.4, 4.55, 9.2, 0.45)

PILL = [g_in(0.5, 1.2, 2.9, 0.36), g_in(3.55, 1.2, 2.9, 0.36), g_in(6.6, 1.2, 2.9, 0.36)]
TUJUAN_CARD = g_in(0.5, 1.72, 3.9, 2.4)
TUJUAN_TXT = g_in(0.65, 2.1, 3.6, 1.95)
LANGKAH = g_in(4.6, 1.72, 4.9, 2.4)
JEBAKAN = g_in(0.5, 4.27, 9.0, 0.68)
SUB = g_in(0.5, 0.98, 8.3, 0.33)



# ------------------------------------------------------------------ cadangan bila deck belum punya slide contoh
def _plain_box(name, geom, fill, line=None, adj=6000):
    ln = '<a:ln w="9525"><a:solidFill><a:srgbClr val="%s"/></a:solidFill></a:ln>' % line if line else '<a:ln><a:noFill/></a:ln>'
    return X('''<p:sp %s><p:nvSpPr><p:cNvPr id="0" name="%s"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr><p:spPr>%s<a:prstGeom prst="roundRect">
<a:avLst><a:gd name="adj" fmla="val %d"/></a:avLst></a:prstGeom><a:solidFill><a:srgbClr val="%s"/></a:solidFill>%s<a:effectLst/></p:spPr>
<p:txBody><a:bodyPr rtlCol="0" anchor="ctr"/><a:lstStyle/><a:p><a:pPr algn="ctr"/></a:p></p:txBody></p:sp>''' % (NSDECL, name, xfrm(geom), adj, fill, ln))


def _label_tujuan():
    return X('''<p:sp %s><p:nvSpPr><p:cNvPr id="0" name="Label Tujuan"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr><p:spPr>%s
<a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/></p:spPr><p:txBody><a:bodyPr wrap="square" lIns="45720" tIns="27432" rIns="45720" bIns="27432" anchor="t"><a:noAutofit/></a:bodyPr>
<a:lstStyle/><a:p><a:r><a:rPr lang="id-ID" sz="1100" b="1"><a:solidFill><a:srgbClr val="C00000"/></a:solidFill><a:latin typeface="Calibri"/></a:rPr><a:t>TUJUAN</a:t></a:r></a:p></p:txBody></p:sp>'''
             % (NSDECL, xfrm(g_in(0.65, 1.8, 3.6, 0.3))))


# ------------------------------------------------------------------ pembangun XML
def _sp(sid, name, ph, geom, fill=None, line=None, body='', lst='', prompt='', prst='rect', adj=None):
    av = '<a:avLst/>' if adj is None else '<a:avLst><a:gd name="adj" fmla="val %d"/></a:avLst>' % adj
    f = '<a:solidFill><a:srgbClr val="%s"/></a:solidFill>' % fill if fill else ''
    ln = ('<a:ln w="9525"><a:solidFill><a:srgbClr val="%s"/></a:solidFill></a:ln>' % line) if line else ''
    phx = '<p:ph %s/>' % ph if ph else ''
    runs = ''.join('<a:p>%s<a:r><a:rPr lang="id-ID"/><a:t>%s</a:t></a:r></a:p>' % (
        '<a:pPr lvl="0"/>' if ph and 'type="title"' not in ph else '', t) for t in prompt.split('|'))
    return X('''<p:sp %s><p:nvSpPr><p:cNvPr id="%d" name="%s"/><p:cNvSpPr><a:spLocks noGrp="1"/></p:cNvSpPr>
<p:nvPr>%s</p:nvPr></p:nvSpPr><p:spPr>%s<a:prstGeom prst="%s">%s</a:prstGeom>%s%s</p:spPr>
<p:txBody>%s<a:lstStyle>%s</a:lstStyle>%s</p:txBody></p:sp>''' % (
        NSDECL, sid, name, phx, xfrm(geom), prst, av, f, ln, body, lst, runs))


def _lvl(sz, color='1A1A1A', b=0, i=0, algn='l', bu='<a:buNone/>', marL=0, indent=0, spc=0):
    return ('<a:lvl1pPr marL="%d" indent="%d" algn="%s"><a:spcBef><a:spcPts val="%d"/></a:spcBef>%s'
            '<a:defRPr sz="%d" b="%d" i="%d"><a:solidFill><a:srgbClr val="%s"/></a:solidFill></a:defRPr></a:lvl1pPr>'
            % (marL, indent, algn, spc, bu, sz, b, i, color))


def _bp(l=45720, t=27432, r=45720, b=27432, anchor='t', rtl=False):
    return ('<a:bodyPr wrap="square" lIns="%d" tIns="%d" rIns="%d" bIns="%d" anchor="%s"><a:noAutofit/></a:bodyPr>'
            % (l, t, r, b, anchor))


# ------------------------------------------------------------------ kloning layout
def clone_layout(prs, src, name):
    master = prs.slide_master
    pkg = prs.part.package
    pn = pkg.next_partname('/ppt/slideLayouts/slideLayout%d.xml')
    new = SlideLayoutPart.load(pn, src.part.content_type, pkg, src.part.blob)
    new.relate_to(master.part, RT.SLIDE_MASTER)
    # gambar latar: salin relasi, sesuaikan rId pada XML
    remap = {}
    for rid, rel in src.part.rels.items():
        if rel.reltype == RT.IMAGE:
            remap[rid] = new.relate_to(rel.target_part, RT.IMAGE)
    for el in new._element.iter():
        for att in list(el.attrib):
            if att.endswith('}embed') and el.attrib[att] in remap:
                el.attrib[att] = remap[el.attrib[att]]
    rid = master.part.relate_to(new, RT.SLIDE_LAYOUT)
    lst = master._element.find('p:sldLayoutIdLst', NS)
    ids = [int(x) for x in lst.xpath('p:sldLayoutId/@id')]
    ids += [int(x) for x in prs.part._element.xpath('.//p:sldMasterId/@id')]
    el = etree.SubElement(lst, P + 'sldLayoutId')
    el.set('id', str(max(ids) + 1))
    el.set('{%s}id' % NS['r'], rid)
    new._element.find('p:cSld', NS).set('name', name)
    for L in prs.slide_layouts:
        if L.part is new:
            return L
    raise RuntimeError('layout baru tidak ditemukan')


def _tree(L):
    return L._element.find('p:cSld/p:spTree', NS)


def _next_id(tree):
    return max(int(x) for x in tree.xpath('.//p:cNvPr/@id')) + 1


def _drop_ph(tree, pred):
    for sp in tree.findall('p:sp', NS):
        ph = sp.find('p:nvSpPr/p:nvPr/p:ph', NS)
        if ph is not None and pred(ph):
            tree.remove(sp)


def _set_layout(slide, L):
    for rel in slide.part.rels.values():
        if rel.reltype == RT.SLIDE_LAYOUT:
            rel._target = L.part
            return
    raise RuntimeError('relasi layout tidak ada')


def _anim_ids(slide):
    return set(int(x) for x in slide._element.xpath('.//p:timing//@spid'))


def _shapes(slide):
    return slide.shapes._spTree.findall('p:sp', NS)


# ------------------------------------------------------------------ layout 1: Ilustrasi + Poin
def build_ilustrasi(prs, konten):
    L = clone_layout(prs, konten, 'Ilustrasi + Poin')
    tree = _tree(L)
    nid = _next_id(tree)
    # kerangka panggung diambil dari slide pertama yang cocok (bentuk persis sama dengan slide lain)
    frame = None
    for s in prs.slides:
        for sp in _shapes(s):
            if _near(_geom(sp), STAGE, 8000) and ''.join(sp.xpath('.//a:srgbClr/@val')).startswith('F5F8FB'):
                frame = copy.deepcopy(sp)
                break
        if frame is not None:
            break
    if frame is None:                       # belum ada slide ilustrasi: buat kerangka baku
        frame = _plain_box('Kerangka Panggung', STAGE, 'F5F8FB', 'D0D5DA', 3000)
    frame.find('p:nvSpPr/p:cNvPr', NS).set('id', str(nid))
    frame.find('p:nvSpPr/p:cNvPr', NS).set('name', 'Kerangka Panggung')
    tree.append(frame)
    tree.append(X('''<p:sp %s><p:nvSpPr><p:cNvPr id="%d" name="Ilustrasi"/><p:cNvSpPr><a:spLocks noGrp="1"/></p:cNvSpPr>
<p:nvPr><p:ph type="pic" sz="quarter" idx="14"/></p:nvPr></p:nvSpPr><p:spPr>%s</p:spPr>
<p:txBody><a:bodyPr anchor="ctr"/><a:lstStyle><a:lvl1pPr marL="0" indent="0" algn="ctr"><a:buNone/><a:defRPr sz="1400">
<a:solidFill><a:srgbClr val="5A6570"/></a:solidFill></a:defRPr></a:lvl1pPr></a:lstStyle>
<a:p><a:r><a:rPr lang="id-ID"/><a:t>Ilustrasi konsep (satu gambar utama)</a:t></a:r></a:p></p:txBody></p:sp>''' % (NSDECL, nid + 1, xfrm(STAGE))))
    bu = '<a:buClr><a:srgbClr val="C00000"/></a:buClr><a:buFont typeface="+mj-lt"/><a:buAutoNum type="arabicPeriod"/>'
    tree.append(_sp(nid + 2, 'Poin', 'type="body" sz="quarter" idx="15"', POIN, body=_bp(t=45720),
                    lst=_lvl(1300, bu=bu, marL=228600, indent=-228600, spc=600),
                    prompt='Poin 1: satu gagasan pendek|Poin 2|Poin 3'))
    tree.append(_sp(nid + 3, 'Kunci Ujian', 'type="body" sz="quarter" idx="16"', KUNCI, fill='FBEAEA', line='C00000',
                    body=_bp(l=109728, t=219456, r=109728, b=27432), lst=_lvl(1250, b=1), prompt='Poin kunci: satu kalimat',
                    prst='roundRect', adj=10000))
    tree.append(_sp(nid + 4, 'Analogi', 'type="body" sz="quarter" idx="17"', ANALOGI, fill='E8F0F6',
                    body=_bp(l=1097280, t=27432, r=137160, b=27432, anchor='ctr'), lst=_lvl(1150, i=1),
                    prompt='Analogi dari kehidupan sehari-hari', prst='roundRect', adj=12000))
    return L


def adopt_ilustrasi(prs, L):
    n = 0
    for s in prs.slides:
        if s.slide_layout.name != 'Konten':
            continue
        pics = sum(1 for sh in s.shapes if sh.shape_type == 13)
        anim = _anim_ids(s)
        for sp in _shapes(s):
            sid = int(sp.find('p:nvSpPr/p:cNvPr', NS).get('id'))
            if (pics >= 2 and sid not in anim and _near(_geom(sp), STAGE, 8000)
                    and ''.join(sp.xpath('.//a:srgbClr/@val')).startswith('F5F8FB')):
                sp.getparent().remove(sp)
                _set_layout(s, L)
                n += 1
                break
    return n


# ------------------------------------------------------------------ layout 2: Latihan Terpandu
def build_latihan(prs, konten, card_src):
    L = clone_layout(prs, konten, 'Latihan Terpandu')
    tree = _tree(L)
    nid = _next_id(tree)
    card = copy.deepcopy(card_src[0])
    card.find('p:nvSpPr/p:cNvPr', NS).set('id', str(nid))
    card.find('p:nvSpPr/p:cNvPr', NS).set('name', 'Kartu Tujuan')
    lab = copy.deepcopy(card_src[1])
    lab.find('p:nvSpPr/p:cNvPr', NS).set('id', str(nid + 1))
    lab.find('p:nvSpPr/p:cNvPr', NS).set('name', 'Label Tujuan')
    tree.append(card)
    tree.append(lab)
    fills = ['0E5A8A', 'C00000', '0E5A8A']
    names = ['Pil Format', 'Pil Durasi', 'Pil Dokumen']
    for i in range(3):
        tree.append(_sp(nid + 2 + i, names[i], 'type="body" sz="quarter" idx="%d"' % (14 + i), PILL[i], fill=fills[i],
                        body='<a:bodyPr wrap="square" lIns="137160" tIns="27432" rIns="137160" bIns="27432" anchor="ctr"><a:noAutofit/></a:bodyPr>',
                        lst=_lvl(1200, color='FFFFFF', b=1, algn='ctr'),
                        prompt=['Format: individu / berpasangan', 'Durasi: 15 menit', 'Lab L#.#'][i],
                        prst='roundRect', adj=50000))
    tree.append(_sp(nid + 5, 'Tujuan', 'type="body" sz="quarter" idx="17"', TUJUAN_TXT, body=_bp(), lst=_lvl(1600),
                    prompt='Tujuan latihan dalam satu kalimat'))
    bu = '<a:buClr><a:srgbClr val="C00000"/></a:buClr><a:buFont typeface="+mj-lt"/><a:buAutoNum type="arabicPeriod"/>'
    tree.append(_sp(nid + 6, 'Langkah', 'type="body" sz="quarter" idx="18"', LANGKAH, body=_bp(t=45720),
                    lst=_lvl(1400, bu=bu, marL=285750, indent=-285750, spc=900),
                    prompt='Langkah 1 (dengan durasi)|Langkah 2|Langkah 3'))
    tree.append(_sp(nid + 7, 'Jebakan Umum', 'type="body" sz="quarter" idx="19"', JEBAKAN, fill='FBEAEA', line='C00000',
                    body=_bp(l=1097280, t=27432, r=137160, b=27432, anchor='ctr'), lst=_lvl(1400, color='C00000'),
                    prompt='Jebakan umum: kesalahan yang paling sering muncul', prst='roundRect', adj=12000))
    return L


def _latihan_parts(s):
    """Kembalikan (pil1, pil2, pil3, kartu, label, teks) bila slide berpola Latihan Terpandu, kalau tidak None."""
    anim = _anim_ids(s)
    found = {}
    for sp in _shapes(s):
        sid = int(sp.find('p:nvSpPr/p:cNvPr', NS).get('id'))
        if sid in anim:
            continue
        g = _geom(sp)
        for i, pg in enumerate(PILL):
            if _near(g, pg, 8000) and sp.find('p:txBody', NS) is not None:
                found['pil%d' % i] = sp
        if _near(g, TUJUAN_CARD, 8000):
            found['kartu'] = sp
        elif _near(g, g_in(0.65, 1.8, 3.6, 0.3), 8000) and ''.join(sp.xpath('.//a:t/text()')) == 'TUJUAN':
            found['label'] = sp
        elif _near(g, TUJUAN_TXT, 8000):
            found['teks'] = sp
    keys = ['pil0', 'pil1', 'pil2', 'kartu', 'label', 'teks']
    return [found[k] for k in keys] if all(k in found for k in keys) else None


def adopt_latihan(prs, L):
    n = 0
    for s in prs.slides:
        if s.slide_layout.name != 'Konten':
            continue
        parts = _latihan_parts(s)
        if not parts:
            continue
        for i in range(3):
            _to_ph(parts[i], '<p:ph type="body" sz="quarter" idx="%d"/>' % (14 + i), PILL[i])
        _to_ph(parts[5], '<p:ph type="body" sz="quarter" idx="17"/>', TUJUAN_TXT)
        for sp in parts[3:5]:
            sp.getparent().remove(sp)
        _set_layout(s, L)
        n += 1
    return n


# ------------------------------------------------------------------ layout 3: Judul Merah
def build_merah(prs, konten):
    L = clone_layout(prs, konten, 'Judul Merah')
    tree = _tree(L)
    _drop_ph(tree, lambda ph: ph.get('type') == 'title' or ph.get('idx') == '13')
    nid = _next_id(tree)
    tree.append(_sp(nid, 'Judul', 'type="title"', G_TITLE_WIDE, body=_bp(anchor='ctr'),
                    lst=_lvl(2600, color='C00000', b=1), prompt='Judul slide'))
    tree.append(_sp(nid + 1, 'Subjudul', 'type="body" sz="quarter" idx="14"', SUB, body=_bp(),
                    lst=_lvl(1200, color='C00000'), prompt='Subjudul satu baris (opsional)'))
    return L


def adopt_merah(prs, L):
    n = 0
    for s in prs.slides:
        if s.slide_layout.name != 'Konten':
            continue
        title = None
        has_label = False
        for sp in _shapes(s):
            ph = sp.find('p:nvSpPr/p:nvPr/p:ph', NS)
            if ph is None:
                continue
            if ph.get('type') == 'title':
                title = sp
            elif ph.get('idx') == '13':
                has_label = True
        if title is None or has_label or not _near(_geom(title), G_TITLE_WIDE, 40000):
            continue
        # teks subjudul statis (merah 12 pt tepat di bawah judul)
        for sp in _shapes(s):
            if sp.find('p:nvSpPr/p:nvPr/p:ph', NS) is None and _near(_geom(sp), SUB, 60000) \
                    and sp.find('p:txBody', NS) is not None \
                    and {r.get('sz') for r in sp.iter(A + 'rPr')} == {'1200'} \
                    and 'C00000' in sp.xpath('.//a:srgbClr/@val'):
                _to_ph(sp, '<p:ph type="body" sz="quarter" idx="14"/>', SUB)
                break
        x = title.find('p:spPr/a:xfrm', NS)
        if x is not None:
            title.find('p:spPr', NS).remove(x)
        _set_layout(s, L)
        n += 1
    return n


# ------------------------------------------------------------------ utama
def run(src, dst=None):
    prs = Presentation(src)
    konten = next(L for L in prs.slide_layouts if L.name == 'Konten')
    # sumber kartu TUJUAN (statis) dari slide Latihan pertama
    card_src = None
    for s in prs.slides:
        parts = _latihan_parts(s) if s.slide_layout.name == 'Konten' else None
        if parts:
            card_src = (parts[3], parts[4])
            break
    if card_src is None:                    # belum ada slide latihan: buat kartu TUJUAN baku
        card_src = (_plain_box('Kartu Tujuan', TUJUAN_CARD, 'F2F2F2', None, 6000), _label_tujuan())
    L1 = build_ilustrasi(prs, konten)
    L2 = build_latihan(prs, konten, card_src)
    L3 = build_merah(prs, konten)
    st = {'Ilustrasi + Poin': adopt_ilustrasi(prs, L1),
          'Latihan Terpandu': adopt_latihan(prs, L2),
          'Judul Merah': adopt_merah(prs, L3)}
    # urutan layout: Pembuka, Konten, layout baru, Penutup
    lst = prs.slide_master._element.find('p:sldLayoutIdLst', NS)
    order = ['Pembuka Hari', 'Konten', 'Ilustrasi + Poin', 'Latihan Terpandu', 'Judul Merah', 'Penutup']
    rid2name = {}
    for L in prs.slide_layouts:
        for rid, rel in prs.slide_master.part.rels.items():
            if rel.reltype == RT.SLIDE_LAYOUT and rel.target_part is L.part:
                rid2name[rid] = L.name
    items = list(lst)
    items.sort(key=lambda e: order.index(rid2name[e.get('{%s}id' % NS['r'])]))
    for e in items:
        lst.remove(e)
    for e in items:
        lst.append(e)
    prs.save(dst or src)
    return st


if __name__ == '__main__':
    print(run(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None))
