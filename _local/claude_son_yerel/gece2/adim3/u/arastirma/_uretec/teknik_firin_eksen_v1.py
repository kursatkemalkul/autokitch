# -*- coding: utf-8 -*-
"""AUTOKITCH · FIRIN ÜRÜN EKSENİ · ÜSTTEN GÖRÜNÜŞ · TEKNİK RESİM v1 (26 Eyl 2026 gece)
Kemal: "anlamadım, teknik yap, üstten görünüş sadece". İki panel aynı ölçekte: BUGÜN (montaj v50) ve PLAN (v51: fırın 79 öne).
Kesit seviyesi: fırın gövdesi (y 956–1473); üstteki raf / davlumbaz / kompresör çizilmedi.
Ölçüler tek kaynaktan: hat_montaj_v50 · firin_tp10_cad_v4 · itici_cad_v2 · kesme_cad_v1 · topping_cad_v24 + topping_hesap_v2.
Kural: paftada yalnız görünüş + ölçü + parça adı; açıklama mesajda.
"""
import math, os
from PIL import Image, ImageDraw, ImageFont

K_HD = 2.0


def _ol(v):
    if isinstance(v, (int, float)):
        return v * K_HD
    if isinstance(v, (list, tuple)):
        return [_ol(x) for x in v]
    return v


class HDraw:
    def __init__(self, im):
        self.d = ImageDraw.Draw(im); self._font = {}

    def _f(self, f):
        if f is None:
            return None
        k = id(f)
        if k not in self._font:
            try:
                self._font[k] = ImageFont.truetype(f.path, max(1, int(round(f.size * K_HD))))
            except Exception:
                self._font[k] = f
        return self._font[k]

    def _w(self, kw):
        if "width" in kw and isinstance(kw["width"], (int, float)):
            kw["width"] = max(1, int(round(kw["width"] * K_HD)))
        if "font" in kw:
            kw["font"] = self._f(kw["font"])
        return kw

    def text(self, xy, s, **kw): return self.d.text(_ol(xy), s, **self._w(kw))
    def line(self, xy, **kw): return self.d.line(_ol(xy), **self._w(kw))
    def rectangle(self, xy, **kw): return self.d.rectangle(_ol(xy), **self._w(kw))
    def ellipse(self, xy, **kw): return self.d.ellipse(_ol(xy), **self._w(kw))
    def polygon(self, xy, **kw): return self.d.polygon(_ol(xy), **self._w(kw))
    def textlength(self, s, font=None, **kw): return self.d.textlength(s, font=self._f(font), **kw) / K_HD


KLASOR = r"C:\Users\Kemal\Desktop\Kemal\WEBSITE\AUTOKITCH\arastirma\FULL_MAKINE".replace("WEBSITE", "WEBS\u0130TE")
SITE_IMG = r"C:\Users\Kemal\Desktop\Kemal\WEBSITE\AUTOKITCH\otonom\hat\img".replace("WEBSITE", "WEBS\u0130TE")
W_PX, H_PX = 3370, 2560
BG, INK, GRAY, LINE = (255, 255, 255), (26, 26, 28), (132, 132, 140), (72, 72, 78)
FILL, ACC, RED, SOFT = (244, 244, 246), (0, 86, 184), (198, 42, 32), (228, 228, 234)
PASL, SICAK, TURUNCU, URUN = (232, 234, 238), (255, 226, 214), (200, 90, 30), (240, 214, 170)
SOGUK, KURU, YESIL, BANT = (222, 236, 250), (238, 238, 232), (22, 128, 74), (250, 244, 232)


def F(sz, b=False):
    for n in (("arialbd.ttf", "segoeuib.ttf") if b else ("arial.ttf", "segoeui.ttf")):
        try:
            return ImageFont.truetype(n, sz)
        except Exception:
            pass
    return ImageFont.load_default()


f7, f8, f9, f11, f13, f16, f30 = F(14), F(16), F(18), F(21), F(24), F(28, True), F(44, True)
f8b, f9b, f11b, f13b = F(16, True), F(18, True), F(21, True), F(24, True)

# ================================================================ ÖLÇÜLER (dünya, mm) — kaynak dosyalardan ================================================================
X0, X1 = 1950.0, 4750.0            # çizilen x aralığı
Z_ON, Z_ARKA = 0.0, -830.0
# TOPPING (topping_uno_cad_v8 / topping_hesap_v2 / topping_cad_v24)
Z_SOGUK = (-104.0, -565.0); Z_BOLME = (-565.0, -630.0); Z_KURU = (-630.0, -830.0)
ZT = -170.0                        # tabla ekseni = Z_KASET[0] + 30
Z_BORU = -150.0                    # kaset iniş borusu ekseni (tabla ekseninin 20 mm önünde)
BORU = ((2061.0, 25.0, "KAŞAR Ø50"), (2310.0, 24.0, "SUCUK Ø48"))     # itici_cad_v2 (TU6 ölçüldü)
X_DISK, R_DISK, R_PIDE = 2337.0, 170.0, 150.0
X_C_SAG = 2500.0
# İTİCİ (itici_cad_v2)
C0 = (2337.0, -170.0); C1 = (2507.0, -249.0)
S_HOME, S_END, W_AXIS, STROK = -37.5, 202.5, -42.0, 250.0
MY_Z, MY_NW = 160.0, 37.0
BAR_W = (-90.0, 80.0)
DESTEK = (2200.0, 2490.0, -420.0, -345.0)
# FIRIN (firin_tp10_cad_v4)
X_F0, X_F1 = 2500.0, 4000.0
D_TP = 730.0
TUNEL_Z = (-485.0, -79.0); BANT_Z = (-473.5, -92.5)
ON_ODA, DUVAR = 64.0, 60.0
X_DUV0 = 2564.0; X_TUN0, X_TUN1 = 2624.0, 3940.0
BANT_X = (2568.0, 3996.0)
Z_URUN_FIRIN = -249.0
ADIM = 310.0
GB_X = (2510.5, 2564.0)            # giriş bandı (burun 2520,5 · tahrik 2554)
OLU_X = (3997.0, 4018.0)
# K (kesme_cad_v1) · dünya = 4000 + yerel
X_K0, X_K1 = 4000.0, 4600.0
K_BANT_X = (4022.0, 4585.0); K_BANT_Z = (-412.0, -12.0)
XC_K, ZC_K = 4300.0, -170.0
KORUMA_R, BICAK_R = 158.0, 148.0
_ca = math.radians(20.0)
CIT_P0 = (XC_K + 160.0 * math.sin(_ca), ZC_K + 160.0 * math.cos(_ca))       # (4354,7 · −19,6)
CIT_Z_DUZ = -206.0 + 150.0                                                     # −56
CIT_X_DONUS = CIT_P0[0] + (CIT_P0[1] - CIT_Z_DUZ) / math.tan(_ca)             # 4454,7
K_CIT = [(4330.0, CIT_P0[1] - math.tan(_ca) * (4330.0 - CIT_P0[0])), (CIT_X_DONUS, CIT_Z_DUZ), (4597.0, CIT_Z_DUZ)]
GIRIS_CIT = [(4026.0, Z_URUN_FIRIN - 150.0 - 3.0), (4257.0, ZC_K - 150.0 - 3.0), (4290.0, ZC_K - 150.0 - 3.0)]   # F'nin K girişi çiti (arka taraf)
# E (kutu_cad_v3)
X_E0 = 4600.0; ZB_E = -206.0; E_BLANK_Z = (-408.0, -4.0); E_PENCERE_Z = (-372.0, -24.0)

# ================================================================ SAYFA ================================================================
S = 1.10                              # px / mm
ML = 150.0
PANEL_H = 930.0 * S                   # z +100 … −830
PT_A, PT_B = 235.0, 235.0 + PANEL_H + 190.0
Z_ALT = 100.0                         # panelin alt sınırı (z, ön yüzün 100 önü)

im = Image.new("RGB", (int(W_PX * K_HD), int(H_PX * K_HD)), BG)
d = HDraw(im)


def px(x): return ML + (x - X0) * S
def pz(z, PT): return PT + (z - Z_ARKA) * S       # z −830 üstte, +100 altta


def rect(PT, x0, x1, z0, z1, fill=None, outline=INK, width=1.0):
    d.rectangle([px(min(x0, x1)), pz(min(z0, z1), PT), px(max(x0, x1)), pz(max(z0, z1), PT)], fill=fill, outline=outline, width=width)


def circ(PT, x, z, r, fill=None, outline=INK, width=1.0):
    d.ellipse([px(x - r), pz(z - r, PT), px(x + r), pz(z + r, PT)], fill=fill, outline=outline, width=width)


def poly(PT, pts, fill=None, outline=INK, width=1.0):
    p = [(px(x), pz(z, PT)) for x, z in pts]
    if fill is not None:
        d.polygon(p, fill=fill, outline=outline)
    if outline is not None and width:
        d.line(p + [p[0]], fill=outline, width=width)


def pline(PT, pts, fill=INK, width=1.0):
    d.line([(px(x), pz(z, PT)) for x, z in pts], fill=fill, width=width)


def dash(PT, pts, fill=GRAY, width=1.0, dl=9.0, gp=6.0):
    for (xa, za), (xb, zb) in zip(pts[:-1], pts[1:]):
        ax, ay, bx, by = px(xa), pz(za, PT), px(xb), pz(zb, PT)
        L = math.hypot(bx - ax, by - ay)
        if L < 1e-6:
            continue
        ux, uy = (bx - ax) / L, (by - ay) / L
        s = 0.0
        while s < L:
            e = min(L, s + dl)
            d.line([(ax + ux * s, ay + uy * s), (ax + ux * e, ay + uy * e)], fill=fill, width=width)
            s += dl + gp


def hatch(PT, x0, x1, z0, z1, fill=(150, 150, 158), step=9.0, width=0.8):
    """eksenlere paralel dikdörtgenin içine 45° tarama (px düzleminde)"""
    ax, bx = px(min(x0, x1)), px(max(x0, x1)); ay, by = pz(min(z0, z1), PT), pz(max(z0, z1), PT)
    c0 = ax - by; c1 = bx - ay
    c = math.floor(c0 / step) * step
    while c <= c1:
        pts = []
        for yy in (ay, by):
            xx = yy + c
            if ax - 1e-6 <= xx <= bx + 1e-6: pts.append((xx, yy))
        for xx in (ax, bx):
            yy = xx - c
            if ay - 1e-6 <= yy <= by + 1e-6: pts.append((xx, yy))
        if len(pts) >= 2:
            pts = sorted(set(pts))
            d.line([pts[0], pts[-1]], fill=fill, width=width)
        c += step


def txt(PT, x, z, s, font=f9, fill=INK, anchor="mm", dx=0.0, dy=0.0):
    d.text((px(x) + dx, pz(z, PT) + dy), s, font=font, fill=fill, anchor=anchor)


def vtxt(PT, x, z, s, font=f7, fill=INK):
    """dikey yazı (aşağıdan yukarıya okunur), merkezi (x, z)"""
    ft = d._f(font)
    tmp = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    bb = tmp.textbbox((0, 0), s, font=ft); w, h = bb[2] - bb[0] + 4, bb[3] - bb[1] + 4
    lay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(lay).text((2 - bb[0], 2 - bb[1]), s, font=ft, fill=fill)
    lay = lay.rotate(90, expand=True)
    cx, cy = px(x) * K_HD, pz(z, PT) * K_HD
    im.paste(lay, (int(round(cx - lay.width / 2.0)), int(round(cy - lay.height / 2.0))), lay)


def dim_v(PT, x, z0, z1, s, font=f9, fill=INK, side=1, ext=(0.0, 0.0), ok=6.0):
    """dikey ölçü çizgisi (z0 → z1) x'te; yazı side>0 sağda, <0 solda"""
    xa = px(x); ya, yb = pz(z0, PT), pz(z1, PT)
    d.line([(xa, ya), (xa, yb)], fill=fill, width=1.0)
    for yy, sg in ((ya, 1), (yb, -1)):
        if abs(yb - ya) < 2 * ok:
            d.line([(xa - 4, yy), (xa + 4, yy)], fill=fill, width=1.0)
        else:
            d.polygon([(xa, yy), (xa - 3, yy + sg * ok), (xa + 3, yy + sg * ok)], fill=fill)
    if ext[0]:
        d.line([(xa, ya), (xa + ext[0], ya)], fill=GRAY, width=0.8)
    if ext[1]:
        d.line([(xa, yb), (xa + ext[1], yb)], fill=GRAY, width=0.8)
    if s:
        d.text((xa + side * 7, (ya + yb) / 2.0), s, font=font, fill=fill, anchor="lm" if side > 0 else "rm")


def dim_h(PT, z, x0, x1, s, font=f9, fill=INK, above=True, ok=6.0):
    ya = pz(z, PT); xa, xb = px(x0), px(x1)
    d.line([(xa, ya), (xb, ya)], fill=fill, width=1.0)
    for xx, sg in ((xa, 1), (xb, -1)):
        if abs(xb - xa) < 2 * ok:
            d.line([(xx, ya - 4), (xx, ya + 4)], fill=fill, width=1.0)
        else:
            d.polygon([(xx, ya), (xx + sg * ok, ya - 3), (xx + sg * ok, ya + 3)], fill=fill)
    if s:
        d.text(((xa + xb) / 2.0, ya + (-5 if above else 5)), s, font=font, fill=fill, anchor="mb" if above else "mt")


def arrow(PT, pts, fill=ACC, width=2.2, ok=9.0):
    p = [(px(x), pz(z, PT)) for x, z in pts]
    d.line(p, fill=fill, width=width)
    (ax, ay), (bx, by) = p[-2], p[-1]
    L = math.hypot(bx - ax, by - ay); ux, uy = (bx - ax) / L, (by - ay) / L
    d.polygon([(bx, by), (bx - ux * ok * 1.8 - uy * ok * 0.7, by - uy * ok * 1.8 + ux * ok * 0.7), (bx - ux * ok * 1.8 + uy * ok * 0.7, by - uy * ok * 1.8 - ux * ok * 0.7)], fill=fill)


def itici_pts(c0, c1):
    """kolsuz silindir gövdesi + çubuk (ev ve son) köşe noktaları — itici_cad_v2 yerel çerçevesi (s itme yönü, w dik)"""
    dx, dz = c1[0] - c0[0], c1[1] - c0[1]; L = math.hypot(dx, dz)
    U = (dx / L, dz / L); W = (-U[1], U[0])
    PC = (c0[0] - R_PIDE * U[0], c0[1] - R_PIDE * U[1])
    P = lambda s, w: (PC[0] + s * U[0] + w * W[0], PC[1] + s * U[1] + w * W[1])
    s0 = S_HOME - 5.0 - MY_Z / 2.0; s1 = S_HOME - 5.0 + STROK + MY_Z / 2.0
    govde = [P(s0, W_AXIS - MY_NW / 2), P(s1, W_AXIS - MY_NW / 2), P(s1, W_AXIS + MY_NW / 2), P(s0, W_AXIS + MY_NW / 2)]
    bar = lambda s: [P(s - 12.0, BAR_W[0]), P(s, BAR_W[0]), P(s, BAR_W[1]), P(s - 12.0, BAR_W[1])]
    return govde, bar(S_HOME), bar(S_END), L, math.degrees(math.atan2(-U[1], U[0])), P


# ================================================================ PANEL ================================================================
def panel(PT, plan):
    sh = 79.0 if plan else 0.0                      # fırın gövdesi + ürün ekseni öne kayma
    ZF = Z_URUN_FIRIN + sh                          # fırında ürün ekseni
    c1 = (2507.0, ZF)
    # --- modül kutuları ---
    rect(PT, X0, X_C_SAG, Z_ON, Z_ARKA, fill=FILL, outline=None)
    rect(PT, X_F0, X_F1, Z_ON, Z_ARKA, fill=FILL, outline=None)
    rect(PT, X_K0, X_K1, Z_ON, Z_ARKA, fill=FILL, outline=None)
    rect(PT, X_E0, X1, Z_ON, Z_ARKA, fill=FILL, outline=None)
    # TOPPING bölmeleri
    rect(PT, X0, X_C_SAG - 1.5, Z_SOGUK[0], Z_SOGUK[1], fill=SOGUK, outline=None)
    rect(PT, X0, X_C_SAG - 1.5, Z_BOLME[0], Z_BOLME[1], fill=SOFT, outline=None)
    rect(PT, X0, X_C_SAG - 1.5, Z_KURU[0], Z_KURU[1], fill=KURU, outline=None)
    dash(PT, [(X0, Z_SOGUK[0]), (X_C_SAG - 1.5, Z_SOGUK[0])]); dash(PT, [(X0, Z_SOGUK[1]), (X_C_SAG - 1.5, Z_SOGUK[1])]); dash(PT, [(X0, Z_KURU[0]), (X_C_SAG - 1.5, Z_KURU[0])])
    txt(PT, 2020.0, -335.0, "SOĞUK HÜCRE  −104…−565", f8, GRAY, "lm")
    txt(PT, 2020.0, -597.0, "yalıtımlı bölme 65", f7, GRAY, "lm")
    txt(PT, 2020.0, -700.0, "KURU MAKİNE BÖLMESİ  200", f8, GRAY, "lm")
    txt(PT, 2020.0, -730.0, "(12 kaset motoru + redüktör, eş eksenli)", f7, GRAY, "lm")
    # --- FIRIN gövdesi ---
    zg0, zg1 = Z_ON + sh, -D_TP + sh
    rect(PT, X_F0, X_F1, zg0, zg1, fill=PASL, outline=INK, width=1.6)
    # ısıtılan oda + uç duvarları + ön oda
    rect(PT, X_TUN0, X_TUN1, TUNEL_Z[1] + sh, TUNEL_Z[0] + sh, fill=SICAK, outline=None)
    for xa, xb in ((X_DUV0, X_TUN0), (X_TUN1, X_F1)):
        rect(PT, xa, xb, zg0, zg1, fill=SOFT, outline=None); hatch(PT, xa, xb, zg0, zg1, step=7.0)
    dash(PT, [(X_DUV0, zg0), (X_DUV0, zg1)], INK, 1.0)
    # tünel + teknik bölme
    rect(PT, X_DUV0, X_F1, TUNEL_Z[1] + sh, TUNEL_Z[0] + sh, fill=None, outline=INK, width=1.2)
    rect(PT, X_F0 + 2.0, X_F1 - 2.0, TUNEL_Z[0] + sh - 3.0, zg1 + 3.0, fill=None, outline=GRAY, width=0.8)
    # bant
    rect(PT, BANT_X[0], BANT_X[1], BANT_Z[1] + sh, BANT_Z[0] + sh, fill=(246, 214, 190), outline=TURUNCU, width=1.2)
    for xx in (BANT_X[0] + 26.0, BANT_X[1] - 26.0):
        dash(PT, [(xx, BANT_Z[1] + sh), (xx, BANT_Z[0] + sh)], TURUNCU, 1.0, 5.0, 4.0)
    # giriş bandı (ön oda) + çıkış ölü plakası
    rect(PT, GB_X[0], GB_X[1], ZF + 160.0, ZF - 160.0, fill=BANT, outline=INK, width=0.9)
    rect(PT, OLU_X[0], OLU_X[1], ZF + 150.0, ZF - 150.0, fill=SOFT, outline=INK, width=0.8)
    # çıkıntı (plan)
    if plan:
        rect(PT, X_F0, X_F1, Z_ON, Z_ON + sh, fill=(255, 238, 170), outline=RED, width=1.6)
        hatch(PT, X_F0, X_F1, Z_ON, Z_ON + sh, fill=(200, 150, 40), step=8.0)
        txt(PT, 3250.0, 40.0, "ÇIKINTI 79 · ön yüzün önünde · y 956–1473 (fırın gövdesi yüksekliği)", f9b, RED)
    # ürünler fırında
    for i in range(4):
        xc = X_TUN0 + 155.0 + i * ADIM
        circ(PT, xc, ZF, R_PIDE, fill=URUN, outline=(160, 120, 60), width=1.0)
    # --- TOPPING: tabla + pide + borular + itici ---
    circ(PT, X_DISK, ZT, R_DISK, fill=(214, 216, 222), outline=INK, width=1.2)
    circ(PT, X_DISK, ZT, R_PIDE, fill=URUN, outline=(160, 120, 60), width=1.0)
    circ(PT, X_DISK, ZT, 3.0, fill=INK, outline=INK)
    for xb, rb, ad in BORU:
        circ(PT, xb, Z_BORU, rb, fill=(200, 208, 220), outline=INK, width=1.0)
        circ(PT, xb, Z_BORU, 2.0, fill=INK, outline=INK)
    txt(PT, 1958.0, -252.0, "kaşar iniş borusu Ø50", f7, INK, "lm")
    pline(PT, [(2040.0, -246.0), (2061.0 - 12.0, Z_BORU - 22.0)], GRAY, 0.8)
    txt(PT, 2310.0, -150.0 + 24.0 + 10.0, "sucuk iniş borusu Ø48", f7, INK, "mt", dx=-30)
    if not plan:
        rect(PT, DESTEK[0], DESTEK[1], DESTEK[3], DESTEK[2], fill=None, outline=GRAY, width=0.9)
        dash(PT, [(DESTEK[0], DESTEK[3]), (DESTEK[1], DESTEK[2])], GRAY, 0.8)
        txt(PT, 2345.0, -432.0, "destek plakası 2 mm · y 1167", f7, GRAY, "mt")
    govde, bar0, bar1, L_it, th, P = itici_pts(C0, c1)
    poly(PT, govde, fill=(200, 208, 220), outline=INK, width=1.0)
    poly(PT, bar0, fill=(120, 124, 130), outline=INK, width=0.8)
    poly(PT, bar1, fill=None, outline=GRAY, width=0.8)
    # --- K ---
    rect(PT, K_BANT_X[0], K_BANT_X[1], K_BANT_Z[1], K_BANT_Z[0], fill=BANT, outline=INK, width=1.0)
    for xx in (4037.0, 4560.0):
        dash(PT, [(xx, K_BANT_Z[1]), (xx, K_BANT_Z[0])], GRAY, 0.8, 5.0, 4.0)
    circ(PT, XC_K, ZC_K, R_PIDE, fill=URUN, outline=(160, 120, 60), width=1.0)
    circ(PT, XC_K, ZC_K, KORUMA_R, fill=None, outline=GRAY, width=0.8)
    for i in range(6):
        a = math.radians(60.0 * i)
        pline(PT, [(XC_K + 15.0 * math.cos(a), ZC_K + 15.0 * math.sin(a)), (XC_K + BICAK_R * math.cos(a), ZC_K + BICAK_R * math.sin(a))], (110, 112, 118), 0.9)
    circ(PT, XC_K, ZC_K, 3.0, fill=INK, outline=INK)
    pline(PT, K_CIT, INK, 2.4)
    if not plan:
        pline(PT, GIRIS_CIT, RED, 2.4)
    # --- E ---
    dash(PT, [(X_E0 + 8.0, E_BLANK_Z[1]), (X1, E_BLANK_Z[1])], GRAY, 0.9); dash(PT, [(X_E0 + 8.0, E_BLANK_Z[0]), (X1, E_BLANK_Z[0])], GRAY, 0.9)
    rect(PT, X_E0 + 8.0, X1, E_BLANK_Z[1], E_BLANK_Z[0], fill=(246, 236, 214), outline=None)
    circ(PT, X1 + 110.0, ZB_E, R_PIDE, fill=None, outline=None)
    # --- modül sınırları, ön/arka yüz ---
    for xx in (X_C_SAG, X_K0, X_E0):
        pline(PT, [(xx, Z_ON), (xx, Z_ARKA)], INK, 1.6)
    # E penceresi: sınır çizgisinde boşluk
    pline(PT, [(X_E0, E_PENCERE_Z[0]), (X_E0, E_PENCERE_Z[1])], (246, 236, 214), 3.0)
    pline(PT, [(X0, Z_ON), (X1, Z_ON)], INK, 2.6)
    pline(PT, [(X0, Z_ARKA), (X1, Z_ARKA)], INK, 1.2)
    # --- ürün yolu (eksen) ---
    yol = [(X0, ZT), (X_DISK, ZT), c1, (X_F1, ZF)]
    if plan:
        yol += [(4330.0, ZC_K)]
    else:
        yol += [(4257.0, ZC_K), (4330.0, ZC_K)]
    yol += [(CIT_X_DONUS, ZB_E), (X1, ZB_E)]
    dash(PT, yol, ACC, 2.2, 14.0, 7.0)
    for x, z in ((X_DISK, ZT), (XC_K, ZC_K)):
        pass
    # eksen etiketleri
    txt(PT, X0 + 8.0, ZT, "−170", f8b, ACC, "lm", dy=16)
    txt(PT, 3250.0, ZF, "fırında ürün ekseni %d" % int(round(ZF)), f9b, ACC, "mm", dy=-(R_PIDE * S + 14))
    txt(PT, XC_K, ZC_K, "kesme merkezi −170", f8b, ACC, "mm", dy=-(KORUMA_R * S + 12))
    txt(PT, X1 - 8.0, ZB_E, "kutu ekseni −206", f8b, ACC, "rm", dy=-22)
    # --- ölçüler ---
    # tabla ↔ boru 20
    dim_v(PT, 2310.0 + 24.0 + 16.0, Z_BORU, ZT, "20", f8, INK, 1)
    # ön yüz → tabla ekseni, sol kenarda
    dim_v(PT, X0 + 28.0, Z_ON, ZT, "170", f8, INK, 1)
    # fırın: ön yüz → ürün ekseni · duvar · bant · teknik · arka boşluk (x = 2594 dikey zincir, uç duvarında)
    xd = 2594.0
    dim_v(PT, xd, Z_ON, ZF, "%d" % int(round(-ZF)), f8, INK, 1)
    dim_v(PT, xd - 18.0, zg0, TUNEL_Z[1] + sh, "79", f8, INK, -1)
    dim_v(PT, xd, TUNEL_Z[1] + sh, TUNEL_Z[0] + sh, "406", f8, INK, 1)
    dim_v(PT, xd, TUNEL_Z[0] + sh, zg1, "245", f8, INK, 1)
    dim_v(PT, xd, zg1, Z_ARKA, "%d" % int(round(zg1 + 830.0)), f8, INK, 1)
    # bant 381 (sağ uç duvarında)
    dim_v(PT, 3970.0, BANT_Z[1] + sh, BANT_Z[0] + sh, "bant 381", f8, INK, -1)
    # ürün ön kenarı → tünel duvarı 20
    dim_v(PT, 3089.0 + 150.0 + 14.0, ZF + 150.0, TUNEL_Z[1] + sh, "20", f8, INK, 1)
    # eksen farkı (giriş)
    if not plan:
        dim_v(PT, 2470.0, ZT, ZF, "79", f9b, RED, -1)
        dim_v(PT, 4270.0, ZF, ZC_K, "79", f9b, RED, 1)
    dim_v(PT, 4618.0, ZC_K, ZB_E, "36", f9b, INK, 1)
    # K bant 400 · kesme
    dim_v(PT, 4595.0, K_BANT_Z[1], K_BANT_Z[0], "400", f8, INK, -1)
    # x ölçüleri (panel üstü, arka yüzün üstünde)
    zx = Z_ARKA - 34.0
    dim_h(PT, zx, X_F0, X_F1, "F · 1500", f8b)
    dim_h(PT, zx, X_K0, X_K1, "K · 600", f8b)
    dim_h(PT, zx, X_C_SAG - 550.0, X_C_SAG, "C · TOPPING (700–2500)", f8b)
    dim_h(PT, zx, X_E0, X1, "E · 4600–5430", f8b)
    dim_h(PT, Z_ARKA - 12.0, X_F0, X_DUV0, "64", f7)
    dim_h(PT, Z_ARKA - 12.0, X_DUV0, X_TUN0, "60", f7)
    dim_h(PT, Z_ARKA - 12.0, X_TUN0, X_TUN1, "ısıtılan 1316 · 4 ürün · adım 310", f7)
    dim_h(PT, Z_ARKA - 12.0, X_TUN1, X_F1, "60", f7)
    # itme
    arrow(PT, [C0, c1], ACC, 2.4)
    txt(PT, (C0[0] + c1[0]) / 2.0, (C0[1] + c1[1]) / 2.0, ("itme %.0f · düz" % L_it) if plan else ("itme %.1f · %.1f°" % (L_it, th)), f8b, ACC, "rb", dx=-10, dy=-8)
    dim_h(PT, ZT + 234.0, X_DISK, 2507.0, "170", f8)
    # parça etiketleri
    txt(PT, 1965.0, -300.0, "SMC MY1B16-250 (kolsuz silindir)", f7, INK, "lm")
    txt(PT, X_DISK, ZT + R_DISK + 16.0, "tabla Ø340 · ekseni z −170 · aktarma konumu x 2337", f7, INK, "mt")
    vtxt(PT, (GB_X[0] + GB_X[1]) / 2.0, ZF, "giriş bandı 320 (F'nin)", f7, INK)
    txt(PT, 3250.0, TUNEL_Z[0] + sh - 40.0, "TEKNİK BÖLME 245 · ekran + tahrik arkada", f8, INK)
    txt(PT, 3250.0, (TUNEL_Z[0] + BANT_Z[0]) / 2.0 + sh, "tünel 406 · bant 381", f7, GRAY)
    txt(PT, 3250.0, (zg1 + Z_ARKA) / 2.0, "F arka sacı −830 · gövde arkasında boşluk %d" % int(round(zg1 + 830.0)), f7, GRAY)
    txt(PT, (K_BANT_X[0] + K_BANT_X[1]) / 2.0, K_BANT_Z[0] - 12.0, "K bandı PU 400", f7, INK, "mb")
    txt(PT, 4470.0, CIT_Z_DUZ + 22.0, "K çiti 20° · −170 → −206", f7, INK, "mm")
    if plan:
        txt(PT, 4140.0, -395.0, "giriş çiti YOK", f8b, YESIL, "mm")
        txt(PT, 2300.0, -440.0, "destek plakası YOK", f8b, YESIL, "mm")
    else:
        txt(PT, 4140.0, -430.0, "giriş çiti 20° (F'nin) · −249 → −170", f7, RED, "mm")
    txt(PT, X1 - 8.0, E_BLANK_Z[0] - 12.0, "E · düz açılım 404 (−4…−408)", f7, GRAY, "rb")
    vtxt(PT, 4007.5, ZF, "ölü plaka", f7, INK)
    # ön yüz / arka yazıları
    txt(PT, X0 + 8.0, Z_ON, "ÖN YÜZ  z 0", f8b, INK, "lm", dy=16)
    txt(PT, X0 + 8.0, Z_ARKA, "ARKA  z −830", f8b, INK, "lm", dy=-16)
    # panel başlığı
    if plan:
        bas = "PLAN · MONTAJ v51 · fırın gövdesi 79 mm öne (+79…−651) · ürün ekseni −170 baştan sona (E −206) · F modülü 909"
    else:
        bas = "BUGÜN · MONTAJ v50 · fırın gövdesi 0…−730 · ürün ekseni TOPPING/K −170 · FIRIN −249 · E −206"
    d.text((px(X0), pz(Z_ARKA, PT) - 92), bas, font=f16, fill=INK, anchor="ls")


panel(PT_A, False)
panel(PT_B, True)

# ================================================================ BAŞLIK / ANTET ================================================================
d.text((ML, 60), "AUTOKITCH · FIRIN ÜRÜN EKSENİ · ÜSTTEN GÖRÜNÜŞ · BUGÜN (v50) / PLAN (v51)", font=f30, fill=INK, anchor="ls")
d.text((ML, 100), "kesit seviyesi: fırın gövdesi y 956–1473 (üstteki havalandırmalı raf, kompresör ve davlumbaz çizilmedi) · ölçüler mm · z: 0 ön yüz, −830 arka · mavi kesik çizgi = ürün merkezinin yolu · ürün Ø300",
       font=f11, fill=LINE, anchor="ls")
yb = H_PX - 70
d.line([(ML, yb - 34), (W_PX - 140, yb - 34)], fill=INK, width=1.2)
d.text((ML, yb), "FIRIN_EKSEN_ustten_v1 · 26 Eyl 2026 gece · ölçek 1 mm = %.2f px (HD ×2) · kaynak: hat_montaj_v50 · firin_tp10_cad_v4 · itici_cad_v2 · kesme_cad_v1 · topping_cad_v24 · topping_hesap_v2 · kutu_cad_v3" % S,
       font=f9, fill=LINE, anchor="ls")
d.text((W_PX - 140, yb), "AUTOKITCH · Torinoarch", font=f11b, fill=INK, anchor="rs")

os.makedirs(KLASOR, exist_ok=True)
png = os.path.join(KLASOR, "FIRIN_EKSEN_ustten_v1.png")
im.save(png, optimize=True)
im.convert("RGB").save(os.path.join(KLASOR, "FIRIN_EKSEN_ustten_v1.pdf"), "PDF", resolution=200.0)
print("YAZILDI", png, im.size)
