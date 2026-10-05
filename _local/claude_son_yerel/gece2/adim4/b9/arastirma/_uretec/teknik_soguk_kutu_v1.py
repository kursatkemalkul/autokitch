# -*- coding: utf-8 -*-
"""TOPPING · SOĞUK KUTU ÖNERİSİ v1 — ÖN KESİT + YAN KESİT (harç) + 2 DETAY · 25 Eyl 2026
Kemal: "yalıtım çok karışık; contası olacak, üstüne kapak kapanacak, tüm köşeleri bir kutu gibi · hazneleri nasıl alıp
dolduracağız · anlamadım, çizim yap". Öneri: tek dikdörtgen soğuk kutu. Taban = 3 mm raf + 40 PU + 1 mm sac (44 sandviç,
raf yerinde kalır), duvarlar tabanın üstüne oturur (1 + 60 PU + 1 = 62), üstte 3 parça contalı kapak, arkadan yaylı menteşe.
Ölçüler topping_uno_cad_v4 (hazne üstleri, iç 1620 × 461) · teknik_topping_satinalma_v2 (UNO yan kesit) · topping_cad_v22
(soğutma grubu 300 × 220 × 220). İnsan 1750 = VARSAYIM ölçek figürü. 3B modele dokunulmadı (Kemal onayı bekleniyor).
"""
import math, os
from PIL import Image, ImageDraw, ImageFont
U = os.path.dirname(os.path.abspath(__file__)); KOK = os.path.dirname(os.path.dirname(U))
CIKTI = os.path.join(KOK, "arastirma", "FULL_MAKINE", "SOGUK_KUTU_v1_teknik.png")

INK, GRI, ACIK = (25, 25, 28), (120, 124, 130), (205, 208, 212)
PU, PUC = (246, 232, 180), (214, 188, 118)
PAS, BEL, BIZ, SOG = (206, 211, 218), (228, 231, 236), (214, 230, 250), (240, 247, 253)
KIR, MAVI, YES, INSAN = (200, 30, 30), (30, 90, 170), (30, 130, 70), (222, 222, 224)
W, H = 3000, 2010
im = Image.new("RGB", (W, H), (255, 255, 255)); d = ImageDraw.Draw(im)
fn = lambda n, b=False: ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf" if b else "C:/Windows/Fonts/arial.ttf", n)
fB, fG, fE, fO, fK = fn(40, True), fn(27, True), fn(20), fn(19), fn(22, True)

# ---------------------------------------------------------------- ölçüler (mm)
S = 0.62; OY = 1940
Y = lambda y: OY - S * y
TB_ALT, TB_UST, DUV_UST, KAP_UST = 1276.0, 1320.0, 1852.0, 1914.0        # taban 44 · duvar 532 · kapak 62
X_DIS0, X_IC0, X_IC1, X_DIS1 = 28.0, 90.0, 1710.0, 1772.0                   # iç 1620, duvar 62
Z_DIS_ON, Z_IC_ON, Z_IC_ARKA, Z_DIS_ARKA, Z_KURU = -42.0, -104.0, -565.0, -627.0, -830.0
KAPAK_BOL = [(X_DIS0, 790.0), (790.0, 1210.0), (1210.0, X_DIS1)]
UNO = [("SOS", 210, 220, 1737), ("HARÇ", 560, 440, 1832), ("KIYMA", 895, 190, 1667), ("KUŞBAŞI", 1105, 190, 1667)]
KAS = [("KAŞAR", 1220, 1502, 1680), ("SUCUK", 1522, 1664, 1680)]
L_KAP = Z_DIS_ON - Z_DIS_ARKA                                                  # 585 kapak derinliği
ACIK_UST = KAP_UST + L_KAP                                                     # 90° açık: 2499


def tara(x0, y0, x1, y1, adim=9, renk=PUC, dolgu=PU):
    x0, x1 = sorted((x0, x1)); y0, y1 = sorted((y0, y1))
    d.rectangle([x0, y0, x1, y1], fill=dolgu); h = y1 - y0; k = x0 - h
    while k < x1:
        a = max(k, x0); b = min(k + h, x1)
        if b > a: d.line([(a, y1 - (a - k)), (b, y1 - (b - k))], fill=renk, width=1)
        k += adim
    d.rectangle([x0, y0, x1, y1], outline=renk, width=1)


def kutu(x0, y0, x1, y1, fill=None, renk=INK, w=2):
    x0, x1 = sorted((x0, x1)); y0, y1 = sorted((y0, y1))
    d.rectangle([x0, y0, x1, y1], fill=fill, outline=renk, width=w)


def kesik(p0, p1, renk=INK, w=2, a=12, b=7):
    (x0, y0), (x1, y1) = p0, p1; L = math.hypot(x1 - x0, y1 - y0)
    if L < 1: return
    ux, uy = (x1 - x0) / L, (y1 - y0) / L; t = 0.0
    while t < L:
        t1 = min(L, t + a); d.line([(x0 + ux * t, y0 + uy * t), (x0 + ux * t1, y0 + uy * t1)], fill=renk, width=w); t = t1 + b


def kesik_kutu(x0, y0, x1, y1, renk=INK, w=2):
    for p, q in (((x0, y0), (x1, y0)), ((x1, y0), (x1, y1)), ((x1, y1), (x0, y1)), ((x0, y1), (x0, y0))): kesik(p, q, renk, w)


def ok(x, y, dx, dy, renk=INK):
    L = math.hypot(dx, dy); ux, uy = dx / L, dy / L
    d.polygon([(x, y), (x - ux * 12 - uy * 5, y - uy * 12 + ux * 5), (x - ux * 12 + uy * 5, y - uy * 12 - ux * 5)], fill=renk)


def olcu_x(y, x0, x1, t, renk=INK, alt=False):
    d.line([(x0, y), (x1, y)], fill=renk, width=2); ok(x0, y, -1, 0, renk); ok(x1, y, 1, 0, renk)
    tw = d.textlength(t, font=fO); ty = y + 4 if alt else y - 24
    d.rectangle([(x0 + x1) / 2 - tw / 2 - 3, ty, (x0 + x1) / 2 + tw / 2 + 3, ty + 21], fill=(255, 255, 255))
    d.text(((x0 + x1) / 2 - tw / 2, ty), t, font=fO, fill=renk)


def olcu_y(x, y0, y1, t, renk=INK, sol=False):
    d.line([(x, y0), (x, y1)], fill=renk, width=2); ok(x, min(y0, y1), 0, -1, renk); ok(x, max(y0, y1), 0, 1, renk)
    tw = d.textlength(t, font=fO); d.text((x - tw - 8 if sol else x + 8, (y0 + y1) / 2 - 11), t, font=fO, fill=renk)


def uzat(x, y0, y1):
    d.line([(x, y0), (x, y1)], fill=ACIK, width=1)


def et(px, py, hx, hy, t, renk=INK, sag=True, kalin=False):
    d.line([(px, py), (hx, hy)], fill=GRI, width=1); d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=GRI)
    f = fK if kalin else fE; tw = d.textlength(t, font=f); x = hx + 6 if sag else hx - 6 - tw
    d.rectangle([x - 3, hy - 13, x + tw + 3, hy + 13], fill=(255, 255, 255)); d.text((x, hy - 12), t, font=f, fill=renk)


def ortala(t, x, y, f=fO, renk=INK):
    d.text((x - d.textlength(t, font=f) / 2, y), t, font=f, fill=renk)


d.text((60, 28), "TOPPING · SOĞUK KUTU ÖNERİSİ v1 — tek kutu · contalı üst kapak · ince sandviç taban", font=fB, fill=INK)
d.text((60, 82), "ölçüler mm · kotlar yerden · mavi = bizim hazne · gri = Beldos UNO · sarı taralı = PU yalıtım · kırmızı = çözülmesi gereken · "
       "insan figürü ölçek içindir (boy 1750 varsayım)", font=fE, fill=GRI)

# ================================================================ DETAY A · TABAN KENARI + UNO AĞZI GEÇİŞİ
s = 2.0; ax, ay = 300, 350                         # u = 0 kutunun dış kenarı · v = 0 raf üstü (1320)
A = lambda u, v: (ax + u * s, ay + v * s)
d.text((60, 140), "DETAY A · TABAN", font=fG, fill=INK)
tara(*A(0, -60), *A(62, 0))                                               # duvar kökü (tabanın üstüne oturur)
kutu(*A(0, -60), *A(1, 0), fill=PAS, renk=INK, w=1); kutu(*A(61, -60), *A(62, 0), fill=PAS, renk=INK, w=1)
tara(*A(3, 3), *A(190, 43))                                               # 40 PU
kutu(*A(0, 0), *A(190, 3), fill=PAS, renk=INK, w=2)                       # 3 mm raf
kutu(*A(0, 3), *A(3, 43), fill=PAS, renk=INK, w=2)                        # 40 mm büküm
kutu(*A(0, 43), *A(190, 44), fill=PAS, renk=INK, w=2)                     # 1 mm alt sac
for (u0, u1) in ((116, 120), (170, 174)):                                  # geçiş burcu
    kutu(*A(u0, -6), *A(u1, 44), fill=(60, 60, 64), renk=INK, w=1)
kutu(*A(127, -75), *A(163, 100), fill=BEL, renk=INK, w=2)                 # UNO ağız borusu Ø36
kutu(*A(110, -9), *A(180, -6), fill=(40, 40, 44), renk=INK, w=1)          # conta bileziği
kesik(A(190, -75), A(190, 100), GRI, 1)
olcu_y(A(202, 0)[0], A(0, 0)[1], A(0, 44)[1], "44")
olcu_x(A(0, -68)[1], A(0, 0)[0], A(62, 0)[0], "62")
et(*A(31, -30), 60, A(0, -30)[1], "duvar 1 + 60 PU + 1", sag=True)
et(*A(20, 1.5), 60, A(0, 1.5)[1] - 6, "raf 3 (yükü taşır)", sag=True)
et(*A(20, 25), 60, A(0, 25)[1] + 14, "PU 40", sag=True)
et(*A(20, 43.5), 60, A(0, 60)[1], "alt sac 1", sag=True)
et(*A(145, 90), 400, A(0, 112)[1], "UNO ağzı Ø36 · burç + conta", sag=True)

# ================================================================ DETAY B · KAPAK ÖN KENARI
s2 = 2.3; bx, by = 1045, 440                       # u = 0 iç yüz, u = 62 dış yüz · v = 0 duvar üstü (1852)
B = lambda u, v: (bx + u * s2, by + v * s2)
d.text((790, 140), "DETAY B · KAPAK ÖN KENARI", font=fG, fill=INK)
tara(*B(0, 0), *B(62, 55))
kutu(*B(0, 0), *B(1, 55), fill=PAS, renk=INK, w=1); kutu(*B(61, 0), *B(62, 55), fill=PAS, renk=INK, w=1)
kutu(*B(0, -1), *B(62, 0), fill=PAS, renk=INK, w=1)                       # duvar üst kenar sacı
tara(*B(-30, -72), *B(62, -10))                                           # kapak
kutu(*B(-30, -72), *B(62, -71), fill=PAS, renk=INK, w=1); kutu(*B(-30, -11), *B(62, -10), fill=PAS, renk=INK, w=1)
kutu(*B(61, -72), *B(62, -10), fill=PAS, renk=INK, w=1)
d.rounded_rectangle([*B(14, -10), *B(48, 0)], radius=6, fill=(45, 45, 50), outline=INK)   # conta
kutu(*B(62, -52), *B(74, 22), fill=(150, 154, 160), renk=INK, w=2)       # mandal
kutu(*B(62, -40), *B(70, -22), fill=(90, 94, 100), renk=INK, w=1)
olcu_y(B(-40, 0)[0], B(0, -72)[1], B(0, -10)[1], "62", sol=True)
et(*B(10, -41), 790, B(0, -86)[1], "kapak 1 + 60 PU + 1", sag=True)
et(*B(31, -5), 790, B(0, 8)[1], "conta (4 kenar)", sag=True)
et(*B(31, 35), 790, B(0, 48)[1], "duvar (üst kenar sacı)", sag=True)
et(*B(74, 10), 1090, B(0, 72)[1], "mandal", sag=True)
d.text((B(-30, 0)[0], B(0, 60)[1]), "iç", font=fO, fill=GRI)

# ================================================================ ÖN KESİT (ön duvarın hemen arkasından)
X = lambda x: 110 + S * x
d.text((60, 628), "ÖN KESİT (kapaklar kapalı · ön duvar kesildi)", font=fG, fill=INK)
d.line([(X(-60), Y(0)), (X(1860), Y(0))], fill=INK, width=3)
kutu(X(0), Y(0), X(1800), Y(123), renk=GRI, w=1); ortala("ayak", X(900), Y(123) + 8, fO, GRI)
kutu(X(0), Y(123), X(1800), Y(1060), renk=GRI, w=1); ortala("alt gövde 123–1060", X(900), Y(600), fO, GRI)
kutu(X(0), Y(1060), X(1800), Y(2030), renk=GRI, w=1)
d.rectangle([X(X_IC0), Y(DUV_UST), X(X_IC1), Y(TB_UST)], fill=SOG)
# taban sandviç (dıştan dışa) + duvarlar tabanın üstünde + kapaklar
tara(X(X_DIS0), Y(TB_UST - 3), X(X_DIS1), Y(TB_ALT + 1))
kutu(X(X_DIS0), Y(TB_UST), X(X_DIS1), Y(TB_UST - 3), fill=PAS, renk=INK, w=2)
kutu(X(X_DIS0), Y(TB_ALT + 1), X(X_DIS1), Y(TB_ALT), fill=PAS, renk=INK, w=1)
tara(X(X_DIS0), Y(DUV_UST), X(X_IC0), Y(TB_UST)); tara(X(X_IC1), Y(DUV_UST), X(X_DIS1), Y(TB_UST))
for i, (a, b) in enumerate(KAPAK_BOL):
    tara(X(a + 3), Y(KAP_UST), X(b - 3), Y(DUV_UST))
    kutu(X(a + 3), Y(KAP_UST), X(b - 3), Y(DUV_UST), renk=INK, w=2)
    ortala("KAPAK %d" % (i + 1), X((a + b) / 2), Y(KAP_UST) - 30, fK)
for xb in (790.0, 1210.0):                                                   # ara kayıt
    kutu(X(xb - 20), Y(DUV_UST), X(xb + 20), Y(DUV_UST - 12), fill=(150, 154, 160), renk=INK, w=1)
for xs in (X_DIS0 + 20, X_DIS1 - 60):                                        # şase köşebenti
    d.polygon([(X(xs), Y(TB_ALT)), (X(xs + 40), Y(TB_ALT)), (X(xs + 40), Y(TB_ALT - 4)), (X(xs + 4), Y(TB_ALT - 4)), (X(xs + 4), Y(TB_ALT - 40)), (X(xs), Y(TB_ALT - 40))], fill=(120, 124, 130))
for n, cx, w, ust in UNO:
    p = [(X(cx - 32), Y(1452)), (X(cx + 32), Y(1452)), (X(cx + w / 2), Y(1632)), (X(cx + w / 2), Y(ust)), (X(cx - w / 2), Y(ust)), (X(cx - w / 2), Y(1632))]
    d.polygon(p, fill=BIZ); d.line(p + [p[0]], fill=MAVI, width=3)
    kutu(X(cx - 41), Y(1392.6), X(cx + 41), Y(TB_UST), fill=BEL, renk=INK, w=2)
    kutu(X(cx - 32), Y(1452), X(cx + 32), Y(1392.6), fill=BEL, renk=INK, w=1)
    kutu(X(cx - 18), Y(TB_ALT), X(cx + 18), Y(1218 if n in ("SOS", "HARÇ") else 1216), fill=BEL, renk=INK, w=1)
    if n in ("SOS", "HARÇ"):
        kutu(X(cx - 8), Y(1218), X(cx + 133), Y(1184), fill=BEL, renk=INK, w=1)
    ortala(n, X(cx), Y(ust) + 8, fK, MAVI)
for n, x0, x1, ust in KAS:
    kutu(X(x0 + 2), Y(ust), X(x1 - 2), Y(TB_UST + 8), fill=(250, 244, 222), renk=INK, w=2)
    kutu(X((x0 + x1) / 2 - 22), Y(TB_ALT), X((x0 + x1) / 2 + 22), Y(1216), fill=BEL, renk=INK, w=1)
    ortala(n, X((x0 + x1) / 2), Y(ust) + 8, fK)
kutu(X(210 - 170), Y(1168), X(210 + 170), Y(1154), fill=(250, 226, 196), renk=INK, w=1)
kutu(X(210 - 140), Y(1176), X(210 + 140), Y(1168), fill=(240, 200, 150), renk=INK, w=1)
d.text((X(390) + 4, Y(1176) - 4), "tabla", font=fO, fill=GRI)
yk = Y(KAP_UST) - 62
for a, b in KAPAK_BOL: uzat(X(a), Y(KAP_UST), yk - 8)
uzat(X(X_DIS1), Y(KAP_UST), yk - 8)
olcu_x(yk, X(KAPAK_BOL[0][0]), X(KAPAK_BOL[0][1]), "762"); olcu_x(yk, X(KAPAK_BOL[1][0]), X(KAPAK_BOL[1][1]), "420")
olcu_x(yk, X(KAPAK_BOL[2][0]), X(KAPAK_BOL[2][1]), "562")
yi = Y(1000)
uzat(X(X_IC0), Y(TB_ALT), yi + 8); uzat(X(X_IC1), Y(TB_ALT), yi + 8); uzat(X(X_DIS0), Y(TB_ALT), yi + 48); uzat(X(X_DIS1), Y(TB_ALT), yi + 48)
olcu_x(yi, X(X_IC0), X(X_IC1), "iç 1620"); olcu_x(yi + 40, X(X_DIS0), X(X_DIS1), "kutu dış 1744")
et(X(1210), Y(DUV_UST - 6), X(1330), Y(1990), "ara kayıt 40 + conta", sag=True)
et(X(X_DIS0 + 4), Y(TB_ALT - 30), X(300), Y(1115), "şase köşebenti (taban iki ucundan taşınır)", sag=True)

# ================================================================ KOT SÜTUNU (iki görünüş arası)
Zp = lambda z: 1600 + S * (z + 900.0)
KX0, KX1 = X(1800) + 8, Zp(-900) - 4
for y, t, renk in [(0, "0 yer", INK), (1060, "1060", INK), (TB_ALT, "1276 kutu altı", INK), (TB_UST, "1320 taban üstü", INK),
                   (1832, "1832 harç ağzı", MAVI), (DUV_UST, "1852 kenar (kapak açık)", INK), (KAP_UST, "1914 kapak üstü", INK),
                   (2030, "2030 modül üstü", GRI), (ACIK_UST, "%.0f açık kapak üstü" % ACIK_UST, KIR)]:
    kesik((KX0, Y(y)), (KX1, Y(y)), ACIK, 1, 6, 6)
    d.text((KX0 + 6, Y(y) + (2 if y == 1832 else -23)), t, font=fO, fill=renk)

# ================================================================ YAN KESİT · HARÇ İSTASYONU
d.text((Zp(-900), 140), "YAN KESİT · HARÇ İSTASYONU (kapak açık, dolum anı)", font=fG, fill=INK)
d.line([(Zp(-900), Y(0)), (Zp(760), Y(0))], fill=INK, width=3)
kutu(Zp(-830), Y(0), Zp(0), Y(123), renk=GRI, w=1)
kutu(Zp(-830), Y(123), Zp(0), Y(1060), renk=GRI, w=1)
kutu(Zp(-830), Y(1060), Zp(0), Y(2030), renk=GRI, w=1)
d.rectangle([Zp(Z_IC_ARKA), Y(DUV_UST), Zp(Z_IC_ON), Y(TB_UST)], fill=SOG)
tara(Zp(Z_DIS_ARKA), Y(TB_UST - 3), Zp(Z_DIS_ON), Y(TB_ALT + 1))
kutu(Zp(Z_DIS_ARKA), Y(TB_UST), Zp(Z_DIS_ON), Y(TB_UST - 3), fill=PAS, renk=INK, w=2)
kutu(Zp(Z_DIS_ARKA), Y(TB_ALT + 1), Zp(Z_DIS_ON), Y(TB_ALT), fill=PAS, renk=INK, w=1)
tara(Zp(Z_DIS_ARKA), Y(DUV_UST), Zp(Z_IC_ARKA), Y(TB_UST)); tara(Zp(Z_IC_ON), Y(DUV_UST), Zp(Z_DIS_ON), Y(TB_UST))
# kapak: kapalı yeri kesik, açık hali (arka üst köşeden menteşeli, 90°) — ön duvar ağzı tamamen açık
kesik_kutu(Zp(Z_DIS_ARKA), Y(KAP_UST), Zp(Z_DIS_ON), Y(DUV_UST), GRI, 2)
tara(Zp(Z_DIS_ARKA), Y(ACIK_UST), Zp(Z_DIS_ARKA + 62), Y(KAP_UST))
kutu(Zp(Z_DIS_ARKA), Y(ACIK_UST), Zp(Z_DIS_ARKA + 62), Y(KAP_UST), renk=INK, w=2)
d.rectangle([Zp(Z_DIS_ARKA + 62), Y(ACIK_UST - 14), Zp(Z_DIS_ARKA + 66), Y(KAP_UST + 14)], fill=(45, 45, 50))
d.ellipse([Zp(Z_DIS_ARKA) - 8, Y(KAP_UST) - 8, Zp(Z_DIS_ARKA) + 8, Y(KAP_UST) + 8], fill=INK)
d.arc([Zp(Z_DIS_ARKA) - L_KAP * S, Y(KAP_UST) - L_KAP * S, Zp(Z_DIS_ARKA) + L_KAP * S, Y(KAP_UST) + L_KAP * S], 270, 360, fill=GRI, width=1)
ok(Zp(Z_DIS_ARKA) + 3, Y(KAP_UST) - L_KAP * S + 1, -1, 0, GRI)
# harç UNO (teknik_topping_satinalma_v2 yan kesiti + v4 hava silindiri)
VZ, VE = -387.0, TB_UST + 38.5
hp = [(Zp(VZ + 32), Y(1452)), (Zp(VZ - 32), Y(1452)), (Zp(-560), Y(1632)), (Zp(-560), Y(1832)), (Zp(-120), Y(1832)), (Zp(-120), Y(1632))]
d.polygon(hp, fill=BIZ); d.line(hp + [hp[0]], fill=MAVI, width=3)
kutu(Zp(VZ + 41), Y(TB_UST), Zp(VZ - 41), Y(1392.6), fill=BEL, renk=INK, w=2)
kutu(Zp(VZ + 32), Y(1392.6), Zp(VZ - 32), Y(1452), fill=BEL, renk=INK, w=1)
kutu(Zp(VZ + 41), Y(VE - 18), Zp(-152), Y(VE + 18), fill=BEL, renk=INK, w=2)
kutu(Zp(-188), Y(VE + 18), Zp(-152), Y(1218), fill=BEL, renk=INK, w=2)
kutu(Zp(-196), Y(1218), Zp(-144), Y(1184), fill=BEL, renk=INK, w=2)
kutu(Zp(VZ - 41), Y(VE - 29), Zp(-559), Y(VE + 29), fill=(232, 236, 242), renk=INK, w=2)
kutu(Zp(-559), Y(VE - 6), Zp(-672), Y(VE + 6), fill=(170, 60, 60), renk=KIR, w=1)
kutu(Zp(-672), Y(VE - 19), Zp(-811), Y(VE + 19), fill=(210, 214, 220), renk=INK, w=2)
kutu(Zp(-340), Y(1154), Zp(0), Y(1168), fill=(250, 226, 196), renk=INK, w=1)
kutu(Zp(-310), Y(1168), Zp(-30), Y(1176), fill=(240, 200, 150), renk=INK, w=1)
# kuru bölme: pano/UPS/güç/sürücü (üstte, ≤170 derin) · soğutma grubu 220 (sığmıyor)
kutu(Zp(-830), Y(2020), Zp(-660), Y(1760), fill=(236, 236, 240), renk=INK, w=2)
kesik_kutu(Zp(-830), Y(1680), Zp(-610), Y(1460), KIR, 3)
ortala("220", (Zp(-830) + Zp(-610)) / 2, Y(1640), fO, KIR)
# ölçü zinciri (derinlik) — kutunun altında · açık kapak boyu düşey
yz = Y(1112)
for z in (-830, Z_DIS_ARKA, Z_IC_ARKA, Z_IC_ON): uzat(Zp(z), Y(TB_ALT) if z != -830 else Y(1060), yz + 8)
olcu_x(yz, Zp(-830), Zp(Z_DIS_ARKA), "kuru 203", alt=True); olcu_x(yz, Zp(Z_IC_ARKA), Zp(Z_IC_ON), "iç 461", alt=True)
olcu_y(Zp(Z_DIS_ARKA) - 16, Y(ACIK_UST), Y(KAP_UST), "585", sol=True)
# basamak + insan (ölçek figürü, boy 1750 varsayım)
BS = 300.0
kutu(Zp(110), Y(BS), Zp(470), Y(0), fill=(236, 236, 238), renk=INK, w=2)
for yy in (100, 200): d.line([(Zp(110), Y(yy)), (Zp(470), Y(yy))], fill=ACIK, width=1)
olcu_y(Zp(500), Y(0), Y(BS), "300")
zc = 330.0
def P(z, y): return (Zp(z), Y(BS + y))
d.polygon([P(170, 0), P(420, 0), P(420, 55), P(360, 80), P(250, 70)], fill=INSAN, outline=(150, 150, 154))
d.polygon([P(265, 70), P(395, 70), P(410, 910), P(250, 910)], fill=INSAN, outline=(150, 150, 154))
d.polygon([P(235, 900), P(430, 900), P(440, 1440), P(250, 1450), P(225, 1300)], fill=INSAN, outline=(150, 150, 154))
d.polygon([P(290, 1440), P(360, 1440), P(360, 1520), P(290, 1520)], fill=INSAN, outline=(150, 150, 154))
d.ellipse([Zp(zc - 95), Y(BS + 1750), Zp(zc + 95), Y(BS + 1520)], fill=INSAN, outline=(150, 150, 154))
omuz, dirsek, el = (320, 1420), (60, 1580), (-210, 1680)
for a_, b_ in ((omuz, dirsek), (dirsek, el)):
    d.line([P(*a_), P(*b_)], fill=(185, 185, 190), width=22)
for j_ in (omuz, dirsek, el):
    x_, y_ = P(*j_); d.ellipse([x_ - 11, y_ - 11, x_ + 11, y_ + 11], fill=(185, 185, 190))
torba = [P(-170, 1740), P(-330, 1680), P(-300, 1560), P(-140, 1620)]
d.polygon(torba, fill=(255, 255, 255), outline=MAVI); d.line([P(-300, 1560), P(-330, 1545)], fill=MAVI, width=3)
# numaralı balonlar + parça listesi (alt gövde içinde)
def balon(n, bxp, byp, px=None, py=None, renk=INK):
    if px is not None:
        d.line([(bxp, byp), (px, py)], fill=GRI, width=1); d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=GRI)
    d.ellipse([bxp - 15, byp - 15, bxp + 15, byp + 15], fill=(255, 255, 255), outline=renk, width=2)
    t = str(n); d.text((bxp - d.textlength(t, font=fO) / 2, byp - 11), t, font=fO, fill=renk)


LISTE = [(1, "kapak · açık 90° · 1 + 60 PU + 1", INK), (2, "yaylı menteşe (sandık dondurucu tipi) · kapakta 2", INK),
         (3, "conta · kapak altı, 4 kenar", INK), (4, "bizim harç haznesi 45 L · ağız 1832", MAVI),
         (5, "vakum paket 7 kg · yerinde boşaltılır", MAVI), (6, "pano · UPS · güç · sürücü (≤ 170 derin)", INK),
         (7, "soğutma grubu 220 → kuru bölme 203'e sığmaz", KIR), (8, "UNO valf + ürün silindiri Ø52 (Beldos)", INK),
         (9, "mil yalıtım duvarından geçer → körük + keçe", KIR), (10, "hava silindiri Ø32 (kuru bölme)", INK),
         (11, "90° ağız + dağıtıcı · tabla Ø340", INK)]
balon(1, Zp(Z_DIS_ARKA) - 70, Y(2420), Zp(Z_DIS_ARKA) + 6, Y(2400))
balon(2, Zp(Z_DIS_ARKA) + 70, Y(1950), Zp(Z_DIS_ARKA) + 4, Y(KAP_UST) - 4)
balon(3, Zp(Z_DIS_ARKA + 62) + 40, Y(2200), Zp(Z_DIS_ARKA + 64), Y(2230))
balon(4, Zp(-340), Y(1700), renk=MAVI)
balon(5, Zp(-235), Y(1650), renk=MAVI)
balon(6, (Zp(-830) + Zp(-660)) / 2, Y(1890))
balon(7, (Zp(-830) + Zp(-610)) / 2, Y(1520), renk=KIR)
balon(8, Zp(-470), Y(1430), Zp(-450), Y(VE + 20))
balon(9, Zp(-600), Y(1225), Zp(-615), Y(VE - 5), renk=KIR)
balon(10, Zp(-742), Y(1265), Zp(-742), Y(VE - 19))
balon(11, Zp(-260), Y(1225), Zp(-196), Y(1200))
d.text((Zp(-820), Y(1030)), "PARÇALAR (yan kesit)", font=fK, fill=INK)
for i, (n, t, r) in enumerate(LISTE):
    yy = Y(1030) + 44 + i * 36
    balon(n, Zp(-800), yy + 1, renk=r); d.text((Zp(-800) + 24, yy - 11), t, font=fE, fill=r)
for harf, zc_, yc_ in (("A", Z_DIS_ON - 20, 1298.0), ("B", Z_DIS_ON - 31, DUV_UST)):
    d.ellipse([Zp(zc_) - 34, Y(yc_) - 34, Zp(zc_) + 34, Y(yc_) + 34], outline=YES, width=2)
    d.text((Zp(zc_) + 30, Y(yc_) + 18), harf, font=fK, fill=YES)
# sağ: insan + basamak
et(Zp(470), Y(BS - 60), Zp(560), Y(420), "basamak 300 (katlanır, serbest)", sag=True)
et(*P(zc + 95, 1640), Zp(560), Y(BS + 1500), "boy 1750 (varsayım)", sag=True)
d.text((Zp(560) + 6, Y(BS + 1500) + 16), "omuz %d · el %d" % (BS + 1420, BS + 1680), font=fO, fill=GRI)

os.makedirs(os.path.dirname(CIKTI), exist_ok=True)
im.save(CIKTI, optimize=True); print("PNG", CIKTI, im.size, "açık kapak üst %.0f" % ACIK_UST)
