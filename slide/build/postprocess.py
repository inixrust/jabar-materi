# -*- coding: utf-8 -*-
"""Perapian slide master dan layout setelah deck dibangun.

- hapus layout yang tidak dipakai, beri nama layout yang jelas
- tema: warna dan font INIXINDO (Calibri)
- master: placeholder judul, isi, nomor slide + gaya teks
- layout: placeholder judul, label kategori, nomor slide
- slide: judul, label, dan nomor slide dijadikan placeholder sungguhan
  (muncul di Outline, navigasi, dan pembaca layar; nomor slide otomatis)
"""
import copy
import re
import sys
import uuid

from lxml import etree
from pptx import Presentation
from pptx.opc.constants import RELATIONSHIP_TYPE as RT

NS = {'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
      'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
      'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
A = '{%s}' % NS['a']
P = '{%s}' % NS['p']
E = 914400
NSDECL = 'xmlns:a="%s" xmlns:p="%s" xmlns:r="%s"' % (NS['a'], NS['p'], NS['r'])

KEEP = {'Title Slide': 'Pembuka Hari', 'DEFAULT': 'Konten', 'Finish': 'Penutup'}

# geometri (EMU) yang dipakai slide
G_TITLE = (1554480, 365760, 6492240, 502920)      # judul dengan label
G_LABEL = (457200, 365760, 960120, 502920)
G_NUM = (6309360, 4590288, 2377440, 182880)
G_TITLE_WIDE = (457200, 320040, 7589520, 594360)  # judul tanpa label


def X(s):
    return etree.fromstring(s)


def xfrm(g):
    return '<a:xfrm><a:off x="%d" y="%d"/><a:ext cx="%d" cy="%d"/></a:xfrm>' % g


# ---------------------------------------------------------------- tema
def patch_theme(prs):
    part = prs.slide_master.part.part_related_by(RT.THEME)
    root = etree.fromstring(part.blob)
    root.set('name', 'INIXINDO CPUX-F')
    cs = root.find('.//a:clrScheme', NS)
    cs.set('name', 'INIXINDO')
    pal = {'dk2': '1A1A1A', 'lt2': 'F2F2F2', 'accent1': 'C00000', 'accent2': '0E5A8A', 'accent3': '2E7D32',
           'accent4': 'D99A00', 'accent5': '5A6570', 'accent6': '7A0000', 'hlink': '0E5A8A', 'folHlink': '5A6570'}
    for k, v in pal.items():
        el = cs.find('a:' + k, NS)
        for ch in list(el):
            el.remove(ch)
        etree.SubElement(el, A + 'srgbClr').set('val', v)
    fs = root.find('.//a:fontScheme', NS)
    fs.set('name', 'INIXINDO')
    for tag in ('majorFont', 'minorFont'):
        fs.find('a:%s/a:latin' % tag, NS).set('typeface', 'Calibri')
    part._blob = etree.tostring(root, xml_declaration=True, encoding='UTF-8', standalone=True)


# ---------------------------------------------------------------- master
def patch_master(prs):
    m = prs.slide_master
    root = m._element
    tree = root.find('p:cSld/p:spTree', NS)
    for sp in tree.findall('p:sp', NS):
        tree.remove(sp)
    title = X('''<p:sp %s><p:nvSpPr><p:cNvPr id="2" name="Judul"/><p:cNvSpPr><a:spLocks noGrp="1"/></p:cNvSpPr>
<p:nvPr><p:ph type="title"/></p:nvPr></p:nvSpPr><p:spPr>%s<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></p:spPr>
<p:txBody><a:bodyPr wrap="square" lIns="45720" tIns="27432" rIns="45720" bIns="27432" anchor="ctr"><a:noAutofit/></a:bodyPr>
<a:lstStyle/><a:p><a:r><a:rPr lang="id-ID"/><a:t>Klik untuk mengubah judul</a:t></a:r></a:p></p:txBody></p:sp>''' % (NSDECL, xfrm((457200, 320040, 8229600, 594360))))
    body = X('''<p:sp %s><p:nvSpPr><p:cNvPr id="3" name="Isi"/><p:cNvSpPr><a:spLocks noGrp="1"/></p:cNvSpPr>
<p:nvPr><p:ph type="body" idx="1"/></p:nvPr></p:nvSpPr><p:spPr>%s<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></p:spPr>
<p:txBody><a:bodyPr wrap="square" lIns="45720" tIns="27432" rIns="45720" bIns="27432"><a:normAutofit/></a:bodyPr>
<a:lstStyle/><a:p><a:pPr lvl="0"/><a:r><a:rPr lang="id-ID"/><a:t>Klik untuk mengubah teks</a:t></a:r></a:p></p:txBody></p:sp>''' % (NSDECL, xfrm((457200, 1051560, 8229600, 3200400))))
    num = X('''<p:sp %s><p:nvSpPr><p:cNvPr id="4" name="Nomor Slide"/><p:cNvSpPr><a:spLocks noGrp="1"/></p:cNvSpPr>
<p:nvPr><p:ph type="sldNum" sz="quarter" idx="4"/></p:nvPr></p:nvSpPr><p:spPr>%s<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></p:spPr>
<p:txBody><a:bodyPr wrap="square" lIns="0" tIns="0" rIns="0" bIns="0" anchor="t"/>
<a:lstStyle><a:lvl1pPr algn="r"><a:defRPr sz="900"><a:solidFill><a:srgbClr val="8C96A0"/></a:solidFill></a:defRPr></a:lvl1pPr></a:lstStyle>
<a:p><a:fld id="{%s}" type="slidenum"><a:rPr lang="id-ID"/><a:t>&#8249;#&#8250;</a:t></a:fld><a:endParaRPr lang="id-ID"/></a:p></p:txBody></p:sp>'''
             % (NSDECL, xfrm(G_NUM), str(uuid.uuid4()).upper()))
    for sp in (title, body, num):
        tree.append(sp)
    # gaya teks
    ts = root.find('p:txStyles/p:titleStyle/a:lvl1pPr', NS)
    ts.set('algn', 'l')
    d = ts.find('a:defRPr', NS)
    d.set('sz', '2400')
    d.set('b', '1')
    sf = d.find('a:solidFill', NS)
    for ch in list(sf):
        sf.remove(ch)
    etree.SubElement(sf, A + 'srgbClr').set('val', '1A1A1A')
    sizes = {1: 1800, 2: 1600, 3: 1400, 4: 1200, 5: 1200, 6: 1200, 7: 1200, 8: 1200, 9: 1200}
    for lv, sz in sizes.items():
        el = root.find('p:txStyles/p:bodyStyle/a:lvl%dpPr/a:defRPr' % lv, NS)
        if el is not None:
            el.set('sz', str(sz))


# ---------------------------------------------------------------- layout
def _tree(layout):
    return layout._element.find('p:cSld/p:spTree', NS)


def patch_layouts(prs):
    for L in list(prs.slide_layouts):
        if L.name not in KEEP:
            prs.slide_layouts.remove(L)
    for L in prs.slide_layouts:
        old = L.name
        L._element.find('p:cSld', NS).set('name', KEEP[old])
        tree = _tree(L)
        nid = max(int(x) for x in tree.xpath('.//p:cNvPr/@id')) + 1
        if old == 'DEFAULT':
            tree.append(X('''<p:sp %s><p:nvSpPr><p:cNvPr id="%d" name="Judul"/><p:cNvSpPr><a:spLocks noGrp="1"/></p:cNvSpPr>
<p:nvPr><p:ph type="title"/></p:nvPr></p:nvSpPr><p:spPr>%s</p:spPr>
<p:txBody><a:bodyPr wrap="square" lIns="45720" tIns="27432" rIns="45720" bIns="27432" anchor="ctr"><a:noAutofit/></a:bodyPr>
<a:lstStyle><a:lvl1pPr algn="l"><a:defRPr sz="2400" b="1"><a:solidFill><a:srgbClr val="1A1A1A"/></a:solidFill></a:defRPr></a:lvl1pPr></a:lstStyle>
<a:p><a:r><a:rPr lang="id-ID"/><a:t>Judul slide</a:t></a:r></a:p></p:txBody></p:sp>''' % (NSDECL, nid, xfrm(G_TITLE))))
            tree.append(X('''<p:sp %s><p:nvSpPr><p:cNvPr id="%d" name="Label Kategori"/><p:cNvSpPr><a:spLocks noGrp="1"/></p:cNvSpPr>
<p:nvPr><p:ph type="body" sz="quarter" idx="13"/></p:nvPr></p:nvSpPr>
<p:spPr>%s<a:solidFill><a:srgbClr val="C00000"/></a:solidFill><a:ln><a:noFill/></a:ln></p:spPr>
<p:txBody><a:bodyPr wrap="square" lIns="18288" tIns="18288" rIns="18288" bIns="18288" anchor="ctr"><a:noAutofit/></a:bodyPr>
<a:lstStyle><a:lvl1pPr marL="0" indent="0" algn="ctr"><a:spcBef><a:spcPts val="0"/></a:spcBef><a:buNone/><a:defRPr sz="1300" b="1"><a:solidFill><a:srgbClr val="FFFFFF"/></a:solidFill></a:defRPr></a:lvl1pPr></a:lstStyle>
<a:p><a:pPr lvl="0"/><a:r><a:rPr lang="id-ID"/><a:t>Label</a:t></a:r></a:p></p:txBody></p:sp>''' % (NSDECL, nid + 1, xfrm(G_LABEL))))
            tree.append(X('''<p:sp %s><p:nvSpPr><p:cNvPr id="%d" name="Nomor Slide"/><p:cNvSpPr><a:spLocks noGrp="1"/></p:cNvSpPr>
<p:nvPr><p:ph type="sldNum" sz="quarter" idx="12"/></p:nvPr></p:nvSpPr><p:spPr>%s</p:spPr>
<p:txBody><a:bodyPr wrap="square" lIns="0" tIns="0" rIns="0" bIns="0" anchor="t"><a:noAutofit/></a:bodyPr>
<a:lstStyle><a:lvl1pPr algn="r"><a:defRPr sz="900"><a:solidFill><a:srgbClr val="8C96A0"/></a:solidFill></a:defRPr></a:lvl1pPr></a:lstStyle>
<a:p><a:fld id="{%s}" type="slidenum"><a:rPr lang="id-ID"/><a:t>&#8249;#&#8250;</a:t></a:fld><a:endParaRPr lang="id-ID"/></a:p></p:txBody></p:sp>'''
                         % (NSDECL, nid + 2, xfrm(G_NUM), str(uuid.uuid4()).upper())))
        elif old == 'Title Slide':
            tree.append(X('''<p:sp %s><p:nvSpPr><p:cNvPr id="%d" name="Judul"/><p:cNvSpPr><a:spLocks noGrp="1"/></p:cNvSpPr>
<p:nvPr><p:ph type="ctrTitle"/></p:nvPr></p:nvSpPr><p:spPr>%s</p:spPr>
<p:txBody><a:bodyPr wrap="square" lIns="45720" tIns="27432" rIns="45720" bIns="27432" anchor="t"><a:noAutofit/></a:bodyPr>
<a:lstStyle><a:lvl1pPr algn="l"><a:defRPr sz="2800" b="1"><a:solidFill><a:srgbClr val="FFFFFF"/></a:solidFill></a:defRPr></a:lvl1pPr></a:lstStyle>
<a:p><a:r><a:rPr lang="id-ID"/><a:t>Judul</a:t></a:r></a:p></p:txBody></p:sp>''' % (NSDECL, nid, xfrm((640080, 1783080, 4754880, 1691640)))))


# ---------------------------------------------------------------- slide
def _geom(sp):
    x = sp.find('p:spPr/a:xfrm', NS)
    if x is None:
        return None
    o, e = x.find('a:off', NS), x.find('a:ext', NS)
    return (int(o.get('x')), int(o.get('y')), int(e.get('cx')), int(e.get('cy')))


def _near(g, ref, tol=20000):
    return g is not None and all(abs(a - b) <= tol for a, b in zip(g, ref))


def _to_ph(sp, ph_xml, drop_xfrm_if=None):
    nv = sp.find('p:nvSpPr', NS)
    c = nv.find('p:cNvSpPr', NS)
    if 'txBox' in c.attrib:
        del c.attrib['txBox']
    etree.SubElement(c, A + 'spLocks').set('noGrp', '1')
    nvpr = nv.find('p:nvPr', NS)
    for ch in list(nvpr):
        nvpr.remove(ch)
    nvpr.append(X(ph_xml.replace('<p:ph', '<p:ph ' + NSDECL, 1)))
    if drop_xfrm_if and _near(_geom(sp), drop_xfrm_if):
        x = sp.find('p:spPr/a:xfrm', NS)
        x.getparent().remove(x)


def _max_sz(sp):
    szs = [int(r.get('sz')) for r in sp.iter(A + 'rPr') if r.get('sz')]
    return max(szs) if szs else 0


def patch_slides(prs):
    stat = {'judul': 0, 'label': 0, 'nomor': 0, 'ctr': 0, 'nomor_statis': 0}
    for idx, s in enumerate(prs.slides, 1):
        lay = s.slide_layout.name
        sps = s.shapes._spTree.findall('p:sp', NS)
        if lay == 'Konten':
            title = label = num = None
            for sp in sps:
                g = _geom(sp)
                if g is None or sp.find('p:txBody', NS) is None:
                    continue
                txt = ''.join(sp.xpath('.//a:t/text()'))
                if _near(g, G_NUM) and re.match(r'^.+ · \d+$', txt) and num is None:
                    num = sp
                elif _near(g, G_LABEL) and label is None and sp.find('p:nvSpPr/p:cNvSpPr', NS).get('txBox') is None and _max_sz(sp) == 1300:
                    label = sp
                elif title is None and g[1] < 1000000 and _max_sz(sp) in (2400, 2600) and (_near(g, G_TITLE) or _near(g, (457200, 320040, 7589520, 594360), 40000) or g[0] == 457200):
                    title = sp
            if title is not None:
                _to_ph(title, '<p:ph type="title"/>', G_TITLE)
                stat['judul'] += 1
            if label is not None and title is not None:
                _to_ph(label, '<p:ph type="body" sz="quarter" idx="13"/>', G_LABEL)
                stat['label'] += 1
            if num is not None:
                txt = ''.join(num.xpath('.//a:t/text()'))
                m = re.match(r'^(.+ · )(\d+)$', txt)
                if int(m.group(2)) == idx:
                    p_ = num.find('p:txBody/a:p', NS)
                    r0 = p_.find('a:r', NS)
                    rpr = copy.deepcopy(r0.find('a:rPr', NS))
                    r0.find('a:t', NS).text = m.group(1)
                    for extra in p_.findall('a:r', NS)[1:]:
                        p_.remove(extra)
                    fld = etree.Element(A + 'fld')
                    fld.set('id', '{%s}' % str(uuid.uuid4()).upper())
                    fld.set('type', 'slidenum')
                    fld.append(rpr)
                    etree.SubElement(fld, A + 't').text = m.group(2)
                    r0.addnext(fld)
                    _to_ph(num, '<p:ph type="sldNum" sz="quarter" idx="12"/>', G_NUM)
                    stat['nomor'] += 1
                else:
                    stat['nomor_statis'] += 1
        elif lay == 'Pembuka Hari':
            big = max(sps, key=_max_sz, default=None)
            if big is not None and _max_sz(big) == 2800:
                _to_ph(big, '<p:ph type="ctrTitle"/>', (640080, 1783080, 4754880, 1691640))
                stat['ctr'] += 1
    return stat


def run(src, dst=None):
    prs = Presentation(src)
    patch_theme(prs)
    patch_master(prs)
    patch_layouts(prs)
    st = patch_slides(prs)
    cp = prs.core_properties
    cp.title = 'CPUX-F: Slide Instruktur'
    cp.author = 'INIXINDO Bandung'
    cp.subject = 'Persiapan sertifikasi CPUX-F (UXQB Foundation Level)'
    prs.save(dst or src)
    return st


if __name__ == '__main__':
    print(run(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None))
