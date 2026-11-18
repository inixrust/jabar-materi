import sys, importlib, os
from PIL import Image
from viz.kit import W, H
mod = importlib.import_module('viz.specs.' + sys.argv[1])
tmp = 'C:/Users/inixindo/AppData/Local/Temp/claude/c0e5d4da64472f57/a0721b0d-5681-4d5c-adf7-1b675b16337e/scratchpad/viz_prev/_qf'; os.makedirs(tmp, exist_ok=True)
frames = []
for t, fn in mod.SPECS.items():
    d = fn(); r = d.render(tmp, scale=2)
    im = Image.new('RGBA', (W*2, H*2), '#F5F8FB')
    for p in ([r['base']] if r['base'] else []) + r['layers']:
        im.alpha_composite(Image.open(p).convert('RGBA'))
    frames.append(im.convert('RGB'))
per = 4; k = 0
for i in range(0, len(frames), per):
    ch = frames[i:i+per]
    sheet = Image.new('RGB', (2*W*2+30, ((len(ch)+1)//2)*(H*2+10)+10), 'white')
    for j, f in enumerate(ch):
        sheet.paste(f, (10 + (j % 2)*(W*2+10), 10 + (j//2)*(H*2+10)))
    p = f'C:/Users/inixindo/AppData/Local/Temp/claude/c0e5d4da64472f57/a0721b0d-5681-4d5c-adf7-1b675b16337e/scratchpad/viz_prev/final_{sys.argv[1]}_{k}.png'; sheet.save(p); print(p); k += 1
