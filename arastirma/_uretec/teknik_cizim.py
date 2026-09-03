# -*- coding: utf-8 -*-
"""Render'in cizgi-teknik on gorunusu: gercek olculerle (mm), yalniz cizgi, olcu oklu SVG."""
import io

S = 0.3          # px per mm
X0, Y0 = 90, 120 # govde sol-ust px
H_GOVDE = 2050   # mm
H_AYAK  = 150
MODULLER = [     # (ad, genislik mm)
    ("HAMUR", 760), ("PRES", 660), ("DOZAJ", 900),
    ("FIRIN", 800), ("KESİM+KUTU", 740), ("İÇECEK", 740),
]
TOPLAM = sum(w for _, w in MODULLER)   # 4600

def px(mm): return mm * S

Y_TABAN = Y0 + px(H_GOVDE)             # govde alti
Y_ZEMIN = Y_TABAN + px(H_AYAK)         # zemin

E = []  # svg elemanlari
def ln(x1,y1,x2,y2,w=1.4): E.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#111" stroke-width="{w}"/>')
def rc(x,y,w,h,sw=1.4,rx=0): E.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="none" stroke="#111" stroke-width="{sw}"/>')
def ci(cx,cy,r,sw=1.4): E.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="none" stroke="#111" stroke-width="{sw}"/>')
def el(cx,cy,rx,ry,sw=1.4): E.append(f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" fill="none" stroke="#111" stroke-width="{sw}"/>')
def tx(x,y,s,fs=12,anchor="middle",w=""):
    fw=f' font-weight="{w}"' if w else ""
    E.append(f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" font-size="{fs}" fill="#111" font-family="Arial, sans-serif"{fw}>{s}</text>')
def olcu_y(x1,x2,y,mm):  # yatay olcu cizgisi
    ln(x1,y,x2,y,1); ln(x1,y-5,x1,y+5,1); ln(x2,y-5,x2,y+5,1)
    E.append(f'<path d="M {x1:.1f} {y:.1f} l 8 -3 v 6 z" fill="#111"/>')
    E.append(f'<path d="M {x2:.1f} {y:.1f} l -8 -3 v 6 z" fill="#111"/>')
    tx((x1+x2)/2, y-7, str(mm), 12)
def olcu_x(x,y1,y2,mm):  # dikey olcu
    ln(x,y1,x,y2,1); ln(x-5,y1,x+5,y1,1); ln(x-5,y2,x+5,y2,1)
    E.append(f'<path d="M {x:.1f} {y1:.1f} l -3 8 h 6 z" fill="#111"/>')
    E.append(f'<path d="M {x:.1f} {y2:.1f} l -3 -8 h 6 z" fill="#111"/>')
    E.append(f'<text x="{x-10:.1f}" y="{(y1+y2)/2:.1f}" text-anchor="middle" font-size="12" fill="#111" font-family="Arial" transform="rotate(-90 {x-10:.1f} {(y1+y2)/2:.1f})">{mm}</text>')

# ---- govde ve ayaklar
rc(X0, Y0, px(TOPLAM), px(H_GOVDE), 2.6, rx=8)
for i in range(7):
    xa = X0 + px(sum(w for _,w in MODULLER[:i]))
    if 0 < i < 7: ln(xa, Y0, xa, Y_TABAN, 2)
for fx in [X0+15, X0+px(TOPLAM)-27] + [X0 + px(sum(w for _,w in MODULLER[:i])) - 6 for i in range(1,6)]:
    rc(fx, Y_TABAN, 12, px(H_AYAK), 1.4)
ln(X0-40, Y_ZEMIN, X0+px(TOPLAM)+40, Y_ZEMIN, 2)

xs = [X0 + px(sum(w for _,w in MODULLER[:i])) for i in range(7)]

# ---- A HAMUR (ust vitrin 350 / tepsili dolap 1100 / rezerv 600)
a0, a1 = xs[0], xs[1]
rc(a0+9, Y0+px(60),  a1-a0-18, px(300), 1.6)                      # ilik raf vitrini
for i in range(4): ci(a0+38+i*px(115), Y0+px(60)+px(160), px(50))
rc(a0+9, Y0+px(420), a1-a0-18, px(1000), 1.6)                     # tepsili buzdolabi
for r in range(6):
    yv = Y0+px(420)+px(140)+r*px(140); ln(a0+16, yv, a1-16, yv, 1)
    for i in range(4): ci(a0+38+i*px(115), yv-px(52), px(50), 1)
rc(a0+9, Y0+px(1480), a1-a0-18, px(540), 1.6)                     # rezerv kapagi
ln(a1-30, Y0+px(1700), a1-30, Y0+px(1800), 2)                     # kulp

# ---- B PRES
b0, b1 = xs[1], xs[2]; bm=(b0+b1)/2
rc(b0+30, Y0+px(120), b1-b0-60, px(700), 1.6)                     # pres kabini
ln(bm-34, Y0+px(170), bm-34, Y0+px(560), 2.2); ln(bm+34, Y0+px(170), bm+34, Y0+px(560), 2.2)
rc(bm-52, Y0+px(200), 104, px(70), 1.6)                           # ust plaka
rc(bm-52, Y0+px(480), 104, px(50), 1.6)                           # alt plaka
el(bm, Y0+px(560), 40, 7)                                         # taban
rc(b0+20, Y0+px(1050), b1-b0-40, px(970), 1.6)                    # alt kabin
ln(b0+34, Y0+px(1500), b0+34, Y0+px(1620), 2)

# ---- C DOZAJ (3 hazne + huni + tabla)
c0, c1 = xs[2], xs[3]; cw=(c1-c0-36)/3
for i in range(3):
    hx = c0+14+i*(cw+4)
    rc(hx, Y0+px(80), cw, px(340), 1.6)                           # hazne
    E.append(f'<path d="M {hx:.1f} {Y0+px(420):.1f} L {hx+cw/2-8:.1f} {Y0+px(560):.1f} h 16 L {hx+cw:.1f} {Y0+px(420):.1f}" fill="none" stroke="#111" stroke-width="1.6"/>')
    ln(hx+cw/2, Y0+px(560), hx+cw/2, Y0+px(680), 2)               # boru
cm=(c0+c1)/2
el(cm, Y0+px(760), px(200), 10, 2)                                     # doner tabla
el(cm, Y0+px(748), px(140), 6)                                         # taban/pide
ln(cm, Y0+px(772), cm, Y0+px(840), 2.2)                           # mil
ln(c0+30, Y0+px(860), c1-30, Y0+px(860), 1.6)                     # tezgah
rc(c0+20, Y0+px(1100), c1-c0-40, px(920), 1.6)                    # alt kabin

# ---- D FIRIN (2 kavite + 3 cekmece)
d0, d1 = xs[3], xs[4]
for k in range(2):
    ky = Y0+px(180)+k*px(560)
    rc(d0+18, ky, d1-d0-36, px(450), 2)                           # kavite govde
    rc(d0+40, ky+px(70), d1-d0-80, px(310), 1.4)                  # cam
    ln(d0+18, ky+px(450), d1-18, ky+px(450), 2.6)                 # kapak mentese hatti
for k in range(3):
    rc(d0+20, Y0+px(1420)+k*px(200), d1-d0-40, px(160), 1.4)      # cekmeceler
    ln((d0+d1)/2-24, Y0+px(1420)+k*px(200)+px(80), (d0+d1)/2+24, Y0+px(1420)+k*px(200)+px(80), 2)

# ---- E KESIM + KUTU
e0, e1 = xs[4], xs[5]; em=(e0+e1)/2
ln(em, Y0+px(90), em, Y0+px(260), 2.6)                            # piston
rc(em-16, Y0+px(150), 32, px(90), 1.6)
ci(em, Y0+px(430), px(150), 2)                                         # bicak yildizi
for dx,dy in [(0,1),(1,0),(0.71,0.71),(0.71,-0.71)]:
    ln(em-px(150)*dx, Y0+px(430)-px(150)*dy, em+px(150)*dx, Y0+px(430)+px(150)*dy, 1.2)
el(em, Y0+px(600), px(150), 8)                                         # kesim tablasi
for r in range(20):                                               # kutu istifi (320x45, 20 adet)
    rc(em-px(160), Y0+px(740)+r*px(55), px(320), px(45), 1.1)
rc(e0+20, Y0+px(1880), e1-e0-40, px(140), 1.4)                    # alt cekmece

# ---- F ICECEK + PAKETLI
f0, f1 = xs[5], xs[6]
rc(f0+12, Y0+px(70), f1-f0-24, px(980), 1.6)                      # icecek sogutucu
for r in range(4):
    yv=Y0+px(70)+px(220)+r*px(220); ln(f0+18, yv, f1-18, yv, 1)
    for i in range(3): rc(f0+30+i*px(105), yv-px(118), px(66), px(115), 1)
rc(f0+12, Y0+px(1130), f1-f0-24, px(890), 1.6)                    # paketli urun dolabi
for r in range(3):
    yv=Y0+px(1130)+px(230)+r*px(230); ln(f0+18, yv, f1-18, yv, 1)
    for i in range(3): ci(f0+34+i*26, yv-12, 8, 1)

# ---- olculer
for i,(ad,w) in enumerate(MODULLER):
    olcu_y(xs[i], xs[i+1], Y0-28, w)
    tx((xs[i]+xs[i+1])/2, Y_ZEMIN+26, ad, 12, w="bold")
olcu_y(X0, X0+px(TOPLAM), Y_ZEMIN+52, TOPLAM)
olcu_x(X0-34, Y0, Y_TABAN, H_GOVDE)
olcu_x(X0-34, Y_TABAN, Y_ZEMIN, H_AYAK)
tx(X0, Y0-64, "AUTOKITCH — HAT ÖN GÖRÜNÜŞÜ · teknik çizim altlığı", 15, "start", "bold")
tx(X0, Y0-46, "ölçüler mm · derinlik 800 mm · yalnız çizgi — üzerine çalışılmak için", 12, "start")

W = int(X0+px(TOPLAM)+80); H = int(Y_ZEMIN+80)
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">'
       f'<rect width="{W}" height="{H}" fill="#ffffff"/>' + "".join(E) + '</svg>')
OUT = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\hat_on_gorunus_teknik.svg"
io.open(OUT, 'w', encoding='utf-8').write(svg)
print('yazildi:', OUT, '|', len(svg), 'karakter |', W, 'x', H)
