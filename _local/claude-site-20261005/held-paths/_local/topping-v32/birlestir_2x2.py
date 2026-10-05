# -*- coding: utf-8 -*-
"""2 × 2 pano: python birlestir_2x2.py <cikti> <h> <r1> <b1> <a1> <r2> <b2> <a2> <r3> <b3> <a3> <r4> <b4> <a4> [dipnot]"""
import sys
from PIL import Image, ImageDraw, ImageFont
out, H = sys.argv[1], int(sys.argv[2]); a = sys.argv[3:15]; dip = sys.argv[15] if len(sys.argv) > 15 else ""
f = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 30); f2 = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 21); f3 = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 20)
P = []
for i in range(4):
    im = Image.open(a[3 * i]).convert("RGB"); im = im.resize((int(im.width * H / im.height), H)); P.append((im, a[3 * i + 1], a[3 * i + 2]))
gap, cap = 18, 78
W = P[0][0].width + gap + P[1][0].width
img = Image.new("RGB", (W, 2 * (cap + H) + gap + (40 if dip else 0)), (255, 255, 255)); dr = ImageDraw.Draw(img)
for i, (im, t1, t2) in enumerate(P):
    x = 0 if i % 2 == 0 else P[0][0].width + gap; y = (i // 2) * (cap + H + gap)
    dr.text((x + 8, y + 6), t1, font=f, fill=(20, 20, 20)); dr.text((x + 8, y + 44), t2, font=f2, fill=(70, 70, 70)); img.paste(im, (x, y + cap))
if dip: dr.text((8, img.height - 32), dip, font=f3, fill=(90, 90, 90))
img.save(out, optimize=True); print("ok", img.size)
