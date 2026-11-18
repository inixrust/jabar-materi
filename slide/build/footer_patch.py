# Mengganti footer yang tertanam di gambar latar layout dengan footer.svg resmi.
import io, os
import cairosvg
from PIL import Image

SVG = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'footer.svg')
RIB = (0, 0x50, 0x81)  # warna pita biru footer lama


def _patch(blob):
    im = Image.open(io.BytesIO(blob)).convert('RGBA')
    w, h = im.size
    if w < 1900:
        return None
    px = im.load()
    top = None
    for y in range(int(h * 0.88), h):
        r, g, b, a = px[int(w * 0.04), y]
        if abs(r - RIB[0]) < 24 and abs(g - RIB[1]) < 24 and abs(b - RIB[2]) < 24 and a > 200:
            top = y
            break
    if top is None:
        return None
    r0, g0, b0, a0 = px[2, top + 2]
    if not (r0 > 235 and g0 > 235 and b0 > 235):
        return None
    png = cairosvg.svg2png(url=SVG, output_width=w)
    ft = Image.open(io.BytesIO(png)).convert('RGBA')
    white = Image.new('RGBA', (w, h - top), (255, 255, 255, 255))
    im.paste(white, (0, top))
    im.alpha_composite(ft, (0, h - ft.size[1]))
    out = io.BytesIO()
    im.save(out, 'PNG')
    return out.getvalue()


def patch_footer(prs):
    done = set()
    n = 0
    for L in prs.slide_layouts:
        if L.name in ('Title Slide', 'Finish'):
            for sh in L.shapes:
                if sh.shape_type == 13 and sh.width >= prs.slide_width * 0.4 and sh.height < prs.slide_height:
                    sh.height = prs.slide_height
    for L in prs.slide_layouts:
        if L.name in ('Title Slide', 'Finish'):
            continue
        for sh in L.shapes:
            if sh.shape_type != 13:
                continue
            part = L.part.related_part(sh._element.blip_rId) if hasattr(sh._element, 'blip_rId') else None
            if part is None or id(part) in done:
                continue
            done.add(id(part))
            nb = _patch(part.blob)
            if nb:
                part._blob = nb
                n += 1
    return n
