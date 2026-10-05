# -*- coding: utf-8 -*-
"""AUTOKITCH · BULAŞIK MAKİNESİ · TEKNİK RESİM v1 (27 Eyl 2026)
Kemal: "bulaşık makinesinin tam çizimini bul ve çiz; bizim sistemde bunların hepsini tek seferde mi makineye atmamız lazım? atılacaksa
makine o boyda olmalı ama standardı bozmamak lazım; imkânsızsa elde yıkayacağız ama bunu istemiyorum."
KAYNAK (ölçüler): MEIKO M-iClean U teknik veri sayfası (meiko.com/en/products/warewashing/undercounter-dishwashers-and-glasswashers/m-iclean-u/technical-data)
  US 460 × 600 × 700 · sepet 400 × 400 · giriş 315 · 90/120/180 s · 40/30/20 sepet/sa · tank 7,5 L · durulama 1,9 L · 6,7 kW
  UM 600 × 600 × 700 · sepet 500 × 500 · giriş 315 · UM+ 600 × 600 × 820 · giriş 435 · 90/120/240 s · UL 600 × 680 × 820 · sepet 500 × 600 · giriş 435
  MEIKO US föyü (Spec_sheets_M-iClean_U.pdf, 8-15-21): kapı açık derinlik 1050 · kapı ağzı 275–590 · bağlantılar arka sol (su 165, gider 95 yerden;
  soldan 40 / 186 / 313) · yükseklik 730 (25 mm kızak tabanıyla) · ayak ±12 · gider hortumu 1,6 m · şebeke bağlantısı en çok 610 (AFF)
  UM föyü (M-iClean_UM_Spec_Sheet.pdf): 600 × 600 (930 kapı açık) × 700 · 400 V 3N 6,7 kW ya da 230 V 1N 2,7 kW · 16 A · tank 11 L · yıkama 60–65 °C · durulama 80–85 °C
KASETLER: harc_cad_v4 / kasar 280 × 360 × 325 (G × Y × D) · kiyma_cad_v9, kusbasi_cad_v8, sucuk_cad_v7 140 × 360 × 325 · UNO hazne 3 L Ø160 × 316 (beldos.html)
Kural: paftada yalnız görünüş + ölçü + parça adı; açıklama mesajda.
"""
import math, os
from PIL import Image, ImageDraw, ImageFont

K_HD = 2.0
NL = chr(10)


def _ol(v):
    if isinstance(v, (int, float)): return v * K_HD
    if isinstance(v, (list, tuple)): return [_ol(x) for x in v]
    return v


class HDraw:
    def __init__(self, im): self.d = ImageDraw.Draw(im); self._font = {}
    def _f(self, f):
        if f is None: return None
        k = id(f)
        if k not in self._font:
            try: self._font[k] = ImageFont.truetype(f.path, max(1, int(round(f.size * K_HD))))
            except Exception: self._font[k] = f
        return self._font[k]
    def _w(self, kw):
        if "width" in kw and isinstance(kw["width"], (int, float)): kw["width"] = max(1, int(round(kw["width"] * K_HD)))
        if "font" in kw: kw["font"] = self._f(kw["font"])
        return kw
    def text(self, xy, s, **kw): return self.d.text(_ol(xy), s, **self._w(kw))
    def line(self, xy, **kw): return self.d.line(_ol(xy), **self._w(kw))
    def rectangle(self, xy, **kw): return self.d.rectangle(_ol(xy), **self._w(kw))
    def ellipse(self, xy, **kw): return self.d.ellipse(_ol(xy), **self._w(kw))
    def polygon(self, xy, **kw): return self.d.polygon(_ol(xy), **self._w(kw))
    def arc(self, xy, a0, a1, **kw): return self.d.arc(_ol(xy), a0, a1, **self._w(kw))
    def textlength(self, s, font=None, **kw): return self.d.textlength(s, font=self._f(font), **kw) / K_HD


KLASOR = r"C:\Users\Kemal\Desktop\Kemal\WEBSITE\AUTOKITCH\arastirma\FULL_MAKINE".replace("WEBSITE", "WEBS\u0130TE")
IMG = r"C:\Users\Kemal\Desktop\Kemal\WEBSITE\AUTOKITCH\otonom\hat\img".replace("WEBSITE", "WEBS\u0130TE")
W_PX, H_PX = 3370, 2600
BG, INK, GRAY, LINE = (255, 255, 255), (26, 26, 28), (132, 132, 140), (72, 72, 78)
FILL, ACC, RED, SOFT = (244, 244, 246), (0, 86, 184), (198, 42, 32), (228, 228, 234)
PASL, KOMSU, URUN, YESIL = (232, 234, 238), (150, 150, 158), (240, 214, 170), (22, 128, 74)
SU, CAM = (214, 236, 250), (200, 225, 250)


def F(sz, b=False):
    for n in (("arialbd.ttf", "segoeuib.ttf") if b else ("arial.ttf", "segoeui.ttf")):
        try: return ImageFont.truetype(n, sz)
        except Exception: pass
    return ImageFont.load_default()


f7, f8, f9, f11, f13, f16, f30 = F(14), F(16), F(18), F(21), F(24), F(28, True), F(44, True)
f8b, f9b, f11b = F(16, True), F(18, True), F(21, True)
im = Image.new("RGB", (int(W_PX * K_HD), int(H_PX * K_HD)), BG)
d = HDraw(im)


def txt(x, y, s, f=f9, c=INK, a="lm"): d.text((x, y), s, font=f, fill=c, anchor=a)
def sayi(v):
    s = ("%.1f" % v).rstrip("0").rstrip("."); return s.replace(".", ",")
def dline(p0, p1, c=GRAY, w=1.0, dl=8.0, gp=5.0):
    L = math.hypot(p1[0] - p0[0], p1[1] - p0[1]); ux, uy = (p1[0] - p0[0]) / L, (p1[1] - p0[1]) / L; s = 0.0
    while s < L:
        e = min(L, s + dl); d.line([(p0[0] + ux * s, p0[1] + uy * s), (p0[0] + ux * e, p0[1] + uy * e)], fill=c, width=w); s += dl + gp
def olcu_h(x0, x1, y, s, f=f8, c=INK, ok=6.0):
    d.line([(x0, y), (x1, y)], fill=c, width=1.0)
    for xx, sg in ((x0, 1), (x1, -1)): d.polygon([(xx, y), (xx + sg * ok, y - 3), (xx + sg * ok, y + 3)], fill=c)
    txt((x0 + x1) / 2, y - 5, s, f, c, "mb")
def olcu_v(x, y0, y1, s, f=f8, c=INK, side=1, ok=6.0):
    d.line([(x, y0), (x, y1)], fill=c, width=1.0)
    for yy, sg in ((y0, 1), (y1, -1)): d.polygon([(x, yy), (x - 3, yy + sg * ok), (x + 3, yy + sg * ok)], fill=c)
    txt(x + side * 7, (y0 + y1) / 2, s, f, c, "lm" if side > 0 else "rm")
def hatch(x0, y0, x1, y1, c=(200, 200, 208), step=9.0):
    c0 = x0 - y1; c1 = x1 - y0; cc = math.floor(c0 / step) * step
    while cc <= c1:
        pts = []
        for yy in (y0, y1):
            xx = yy + cc
            if x0 - 1e-6 <= xx <= x1 + 1e-6: pts.append((xx, yy))
        for xx in (x0, x1):
            yy = xx - cc
            if y0 - 1e-6 <= yy <= y1 + 1e-6: pts.append((xx, yy))
        if len(pts) >= 2:
            pts = sorted(set(pts)); d.line([pts[0], pts[-1]], fill=c, width=0.8)
        cc += step


# ================================================================ MEIKO ÖLÇÜLERİ (mm) ================================================================
US = dict(ad="M-iClean US", W=460, D=600, H=700, H_US=730, sepet=(400, 400), giris=315, agiz_alt=275, kapi_acik=1050, cevrim=(90, 120, 180), sepet_sa=(40, 30, 20), tank=7.5, durulama=1.9, kW=6.7)
UM = dict(ad="M-iClean UM", W=600, D=600, H=700, sepet=(500, 500), giris=315, cevrim=(90, 120, 180), sepet_sa=(40, 30, 20), tank=11.0, durulama=2.4, kW=6.7)
UMP = dict(ad="M-iClean UM+", W=600, D=600, H=820, sepet=(500, 500), giris=435, cevrim=(90, 120, 240), sepet_sa=(40, 30, 15), tank=11.0, durulama=2.4, kW=6.7)
UL = dict(ad="M-iClean UL", W=600, D=680, H=820, sepet=(500, 600), giris=435, cevrim=(90, 120, 240), sepet_sa=(40, 30, 15), tank=11.0, durulama=2.8, kW=6.7)
# F taban dolabı (montaj v51, dünya): dolap 2500–4000 · iç y 126–953 · bulaşık yuvası x 2540–3000 · z −620…−20 · temizlik 3010–3156 · pizza yedeği 3166–3970
DOLAP = dict(x0=2500, x1=4000, y0=126, y1=953, bul=(2540, 3000), tem=(3010, 3156), piz=(3166, 3970), z=(-620, -20))
# yıkanacaklar (G × Y × D)
YIK = [("Harç kaseti × 2 (harc_cad_v4)", 280, 360, 325, 2), ("Kaşar kabı (kasar_cad_v14)", 280, 360, 325, 1), ("Kıyma kaseti (kiyma_cad_v9)", 140, 360, 325, 1),
       ("Kuşbaşı kaseti (kusbasi_cad_v8)", 140, 360, 325, 1), ("Küp sucuk kaseti (sucuk_cad_v7)", 140, 360, 325, 1),
       ("UNO hazne 3 L (Beldos) × 4", 160, 316, 160, 4), ("UNO silindir Ø52 + piston × 4", 52, 250, 52, 4), ("UNO valf gövdesi × 4", 110, 90, 90, 4),
       ("Tabla çalışma diski Ø340 × 8 (pimli)", 340, 8, 340, 1), ("K yıldız bıçak seti Ø296 × 45", 296, 45, 296, 1), ("K koruma halkası Ø316 × 37", 316, 37, 316, 1),
       ("K sprey ucu + nozül, itici çubuk 170 × 30", 170, 30, 40, 1)]

S = 0.62   # px / mm (görünüşler)


# ================================================================ A · MEIKO US GÖRÜNÜŞLER ================================================================
def meiko_gorunus(x0, y0, M, etiket):
    W, D, H = M["W"], M["D"], M["H"]
    # ÖN
    fx = lambda x: x0 + x * S; fy = lambda y: y0 + (H + 40 - y) * S
    d.rectangle([fx(0), fy(H), fx(W), fy(0)], fill=PASL, outline=INK, width=1.6)
    d.rectangle([fx(20), fy(M["agiz_alt"] + M["giris"] + 22), fx(W - 20), fy(M["agiz_alt"] + 4)], fill=(236, 238, 242), outline=INK, width=1.0)   # kapı
    d.rectangle([fx(W / 2 - 60), fy(H - 28), fx(W / 2 + 60), fy(H - 58)], fill=INK)                                                              # ekran
    d.ellipse([fx(W / 2 - 12), fy(M["agiz_alt"] + M["giris"] - 30), fx(W / 2 + 12), fy(M["agiz_alt"] + M["giris"] - 54)], outline=INK, width=1.0)   # kulp göstergesi
    for xx in (30, W - 30): d.rectangle([fx(xx - 12), fy(0), fx(xx + 12), fy(-25)], fill=SOFT, outline=INK, width=0.8)                           # ayaklar ±12
    olcu_h(fx(0), fx(W), fy(H) - 26, "%s" % sayi(W), f9b)
    olcu_v(fx(W) + 30, fy(H), fy(0), "%s (föy) · ABD 730" % sayi(H) if M is US else sayi(H), f8, INK, 1)
    olcu_v(fx(0) - 30, fy(M["agiz_alt"] + M["giris"]), fy(M["agiz_alt"]), "kapı ağzı %s" % sayi(M["giris"]), f8, ACC, -1)
    olcu_v(fx(0) - 30, fy(M["agiz_alt"]), fy(0), sayi(M["agiz_alt"]), f7, INK, -1)
    txt(fx(W / 2), fy(H) - 50, "ÖN", f8b, ACC, "mm")
    # YAN (kapı açık, kesik)
    sx0 = x0 + (W + 420) * S
    sx = lambda z: sx0 + z * S
    d.rectangle([sx(0), fy(H), sx(D), fy(0)], fill=PASL, outline=INK, width=1.6)
    d.rectangle([sx(30), fy(M["agiz_alt"] + M["giris"]), sx(D - 30), fy(M["agiz_alt"])], fill=SU, outline=None)                                  # tank / sepet bölgesi
    d.rectangle([sx(60), fy(M["agiz_alt"] + 30), sx(60 + M["sepet"][1]), fy(M["agiz_alt"] + 10)], fill=(200, 210, 224), outline=INK, width=0.8)   # sepet
    ka = M.get("kapi_acik", D + 450)
    d.line([(sx(0), fy(M["agiz_alt"])), (sx(-(ka - D)), fy(M["agiz_alt"]))], fill=INK, width=2.0)                                                # kapı yatay (açık)
    dline((sx(0), fy(M["agiz_alt"] + M["giris"] + 22)), (sx(-(ka - D)), fy(M["agiz_alt"])), GRAY, 1.0)
    d.arc([sx(-(ka - D)), fy(M["agiz_alt"] + (ka - D)), sx(ka - D), fy(M["agiz_alt"] - (ka - D))], 180, 270, fill=GRAY, width=1.0)
    olcu_h(sx(-(ka - D)), sx(D), fy(H) - 26, "kapı açık %s" % sayi(ka), f8, ACC)
    olcu_h(sx(-(ka - D)), sx(0), fy(H) - 56, sayi(ka - D), f7, INK); olcu_h(sx(0), sx(D), fy(H) - 56, sayi(D), f9b)
    olcu_v(sx(D) + 30, fy(M["agiz_alt"] + M["giris"]), fy(M["agiz_alt"]), sayi(M["giris"]), f8, ACC, 1)
    olcu_v(sx(D) + 30, fy(M["agiz_alt"]), fy(0), sayi(M["agiz_alt"]), f7, INK, 1)
    for yy, ad in ((165, "su ¾\""), (95, "gider DN22 / 38")):
        d.ellipse([sx(D) - 4, fy(yy) - 4, sx(D) + 4, fy(yy) + 4], fill=BG, outline=INK, width=1.0); txt(sx(D) + 110, fy(yy), "%s · %s" % (ad, sayi(yy)), f7, INK, "lm")
    txt(sx(D / 2), fy(H) - 84, "YAN (kapı açık)", f8b, ACC, "mm")
    # ÜST
    tx0 = x0; ty0 = y0 + (H + 40) * S + 90
    tx = lambda x: tx0 + x * S; tz = lambda z: ty0 + z * S
    d.rectangle([tx(0), tz(0), tx(W), tz(D)], fill=PASL, outline=INK, width=1.6)
    d.rectangle([tx(20), tz(20), tx(W - 20), tz(D - 20)], fill=SU, outline=GRAY, width=0.8)
    d.rectangle([tx((W - M["sepet"][0]) / 2), tz(60), tx((W + M["sepet"][0]) / 2), tz(60 + M["sepet"][1])], fill=(200, 210, 224), outline=INK, width=1.0)
    txt(tx(W / 2), tz(60 + M["sepet"][1] / 2), "sepet %s × %s" % (sayi(M["sepet"][0]), sayi(M["sepet"][1])), f8b, INK, "mm")
    for xx, ad in ((186, "W"), (313, "D")):
        d.ellipse([tx(xx) - 4, tz(-14) - 4, tx(xx) + 4, tz(-14) + 4], fill=BG, outline=INK, width=1.0); txt(tx(xx), tz(-30), ad, f7, INK, "mm")
    d.ellipse([tx(40) - 5, tz(-14) - 5, tx(40) + 5, tz(-14) + 5], fill=INK); txt(tx(40), tz(-30), "elektrik", f7, INK, "mm")
    olcu_h(tx(0), tx(W), tz(D) + 30, sayi(W), f9b); olcu_v(tx(W) + 30, tz(0), tz(D), sayi(D), f9b, INK, 1)
    olcu_h(tx(0), tx(186), tz(-48), "186", f7); olcu_h(tx(186), tx(313), tz(-48), "127", f7)
    txt(tx(W / 2), tz(D) + 62, "ÜST (bağlantılar arkada, soldan 40 / 186 / 313 · ABD föyü)", f8b, ACC, "mm")
    txt(x0, y0 - 120, etiket, f16, ACC)


# ================================================================ B · F TABAN DOLABINDA YERİ ================================================================
def dolap(x0, y0):
    Sd = 0.30
    fx = lambda x: x0 + (x - DOLAP["x0"]) * Sd; fy = lambda y: y0 + (1000 - y) * Sd
    txt(x0, y0 - 40, "F TABAN DOLABI · ÖN (x 2500–4000)", f16, ACC)
    d.rectangle([fx(2500), fy(956), fx(4000), fy(123)], fill=FILL, outline=INK, width=1.6)
    for (a, b), ad, c, dy_ in ((DOLAP["bul"], "BULAŞIK 460" + NL + "MEIKO US", SU, 0), (DOLAP["tem"], "temizlik" + NL + "146", SOFT, 24), (DOLAP["piz"], "PİZZA KUTUSU YEDEĞİ" + NL + "804 × 808 · 505 kutu", URUN, 0)):
        d.rectangle([fx(a), fy(953), fx(b), fy(130)], fill=c, outline=LINE, width=1.0); txt(fx((a + b) / 2), fy(123) + 34 + dy_, ad, f7, INK, "mm")
    # makine (US 460 × 700/730) yuvada: kapı ağzı 275–590 (+ dolap tabanı 126)
    d.rectangle([fx(2540), fy(126 + US["H_US"]), fx(3000), fy(126)], fill=PASL, outline=INK, width=1.4)
    d.rectangle([fx(2560), fy(126 + US["agiz_alt"] + US["giris"] + 22), fx(2980), fy(126 + US["agiz_alt"] + 4)], fill=(236, 238, 242), outline=INK, width=0.8)
    olcu_v(fx(2540) - 22, fy(126 + US["H_US"]), fy(126), "730", f8, INK, -1)
    olcu_v(fx(2540) - 22, fy(953), fy(126 + US["H_US"]), "97", f7, RED, -1)
    olcu_h(fx(2540), fx(3000), fy(956) - 16, "yuva 460 = US 460", f7, INK)
    olcu_h(fx(3000), fx(3140), fy(956) - 16, "+140 (UM+)", f7, RED)
    olcu_h(fx(2500), fx(4000), fy(123) + 90, "F 1500 · üst 956 · fırın gövdesi 956–1473 (79 öne)", f9b)

    # yan kesit (z): dolap 830 derin, makine 600, kapı açık +430 koridora, robot rayı 260–500 yerde
    zx0 = x0 + 1500 * Sd + 170
    zx = lambda z: zx0 + (z + 830) * Sd
    txt(zx0, y0 - 40, "YAN KESİT (kapı açık)", f16, ACC)
    d.rectangle([zx(-830), fy(956), zx(0), fy(123)], fill=FILL, outline=INK, width=1.6)
    d.rectangle([zx(-620), fy(126 + US["H_US"]), zx(-20), fy(126)], fill=PASL, outline=INK, width=1.4)
    d.rectangle([zx(-600), fy(126 + US["agiz_alt"] + US["giris"]), zx(-40), fy(126 + US["agiz_alt"])], fill=SU, outline=None)
    d.line([(zx(-20), fy(126 + US["agiz_alt"])), (zx(-20 + 450), fy(126 + US["agiz_alt"]))], fill=INK, width=2.0)
    dline((zx(-20), fy(126 + US["agiz_alt"] + US["giris"] + 22)), (zx(430), fy(126 + US["agiz_alt"])), GRAY, 1.0)
    d.rectangle([zx(260), fy(60), zx(500), fy(0)], fill=SOFT, outline=ACC, width=1.0); txt(zx(380), fy(0) + 16, "robot rayı z 260–500 · y 0–60", f7, ACC, "mm")
    d.rectangle([zx(0), fy(1000), zx(79), fy(956)], fill=(255, 238, 170), outline=RED, width=1.4); txt(zx(79) + 8, fy(978), "fırın çıkıntısı 79 (956–1473)", f7, RED, "lm")
    olcu_h(zx(-20), zx(430), fy(126 + US["agiz_alt"]) - 14, "kapı açık 450 · alt kenarı yerden %s: rayın üstünden" % sayi(126 + US["agiz_alt"]), f7, ACC)
    olcu_h(zx(-830), zx(0), fy(123) + 40, "F 830", f9b); olcu_h(zx(-620), zx(-20), fy(123) + 70, "makine 600", f8)
    txt(zx(-415), fy(1520), "ön (z 0)", f7, GRAY, "mm")


# ================================================================ C · YIKANACAKLAR + SEPET ================================================================
def yikanacaklar(x0, y0):
    txt(x0, y0 - 40, "YIKANACAKLAR · SEPETE SIĞMA (G × Y × D · mm) · yatırılınca yükseklik = genişlik", f16, ACC)
    kol = (0, 40, 470, 560, 640, 720, 800, 1080)
    bas = ("NO", "PARÇA", "adet", "G", "Y", "D", "US 400 × 400 · giriş 315", "UM+ 500 × 500 · giriş 435")
    gen = 1360.0
    d.rectangle([x0, y0, x0 + gen, y0 + 28], fill=SOFT, outline=LINE, width=1.0)
    for k, b in zip(kol, bas): txt(x0 + k + 8, y0 + 14, b, f8b, INK, "lm")
    y = y0 + 28; toplam_us = 0.0; toplam_um = 0.0
    def sigma(G, Y, D, sep, giris):
        # dik: taban G × D, yükseklik Y · yatık: taban Y × D, yükseklik G
        if G <= sep[0] and D <= sep[1] and Y <= giris: return "dik", 1
        if Y <= sep[0] and D <= sep[1] and G <= giris: return "yatık", 1
        return "SIĞMAZ", 0
    for i, (ad, G, Y, D, n) in enumerate(YIK, 1):
        us, nus = sigma(G, Y, D, US["sepet"], US["giris"]); um, num = sigma(G, Y, D, UMP["sepet"], UMP["giris"])
        # sepette kaç tane: dik ise yan yana G'ye göre, yatık ise Y'ye göre (tek sıra)
        def adet(sep, giris, konum):
            if konum == "dik": return max(1, int(sep[0] // G)) * max(1, int(sep[1] // D))
            if konum == "yatık": return max(1, int(sep[0] // Y)) * max(1, int(sep[1] // D))
            return 0
        a_us = min(n, adet(US["sepet"], US["giris"], us)) if nus else 0; a_um = min(n, adet(UMP["sepet"], UMP["giris"], um)) if num else 0
        c_us = (math.ceil(n / a_us) if a_us else 0); c_um = (math.ceil(n / a_um) if a_um else 0)
        toplam_us += c_us; toplam_um += c_um
        d.line([(x0, y + 26), (x0 + gen, y + 26)], fill=(225, 225, 230), width=0.8)
        for k, v in zip(kol, (str(i), ad, str(n), sayi(G), sayi(Y), sayi(D), "%s · sepette %d · %d çevrim" % (us, a_us, c_us) if nus else "SIĞMAZ", "%s · sepette %d · %d çevrim" % (um, a_um, c_um) if num else "SIĞMAZ")):
            txt(x0 + k + 8, y + 13, v, f8, INK if v != "SIĞMAZ" else RED, "lm")
        y += 26
    d.rectangle([x0, y0, x0 + gen, y], outline=LINE, width=1.0)
    y += 16
    txt(x0, y, "Küçük parçalar (silindir, valf, nozül, çubuk, halka) aynı sepette birleşir → gerçek çevrim: US ≈ %d–%d · UM+ ≈ %d–%d" % (toplam_us - 8, toplam_us - 4, toplam_um - 6, toplam_um - 3), f8b, INK, "lm")
    y += 22
    txt(x0, y, "(180 / 240 s çevrim + yükleme) ≈ US 25–30 dk · UM+ 15–20 dk · ikmal ziyaretinde, sıra sıra", f8b, INK, "lm")
    y += 24
    txt(x0, y, "Tek seferde (bütün liste bir sepette) hiçbir tezgâh altı makine almaz; kapaklı (hood) makine (sepet 500 × 500, giriş 440, gövde ≈ 1,5 m, örn. M-iClean H)", f8, RED, "lm")
    y += 20
    txt(x0, y, "gerekir → F dolabına (826) sığmaz, standardı bozar. Elde yıkama gerekmez: sıra sıra yıkanır.", f8, RED, "lm")
    # sepet şemaları
    sx0 = x0; sy0 = y + 80
    Ss = 0.55
    txt(sx0, sy0 - 40, "SEPET ŞEMASI (üstten)", f16, ACC)
    # US 400 × 400: kaşar yatık (360 × 325, yükseklik 280 ≤ 315)
    d.rectangle([sx0, sy0, sx0 + 400 * Ss, sy0 + 400 * Ss], fill=SU, outline=INK, width=1.2)
    d.rectangle([sx0 + 20 * Ss, sy0 + 37 * Ss, sx0 + 380 * Ss, sy0 + 362 * Ss], fill=URUN, outline=INK, width=1.0)
    txt(sx0 + 200 * Ss, sy0 + 200 * Ss, "kaşar / harç YATIK" + NL + "360 × 325" + NL + "yükseklik 280 ≤ 315", f7, INK, "mm")
    txt(sx0 + 200 * Ss, sy0 + 400 * Ss + 14, "US 400 × 400 · 1 kaset / çevrim", f8b, ACC, "mm")
    # UM+ 500 × 500: kaşar dik 280 × 325 + kıyma dik 140 × 325 (yükseklik 360 ≤ 435)
    ux0 = sx0 + 400 * Ss + 90
    d.rectangle([ux0, sy0, ux0 + 500 * Ss, sy0 + 500 * Ss], fill=SU, outline=INK, width=1.2)
    d.rectangle([ux0 + 20 * Ss, sy0 + 87 * Ss, ux0 + 300 * Ss, sy0 + 412 * Ss], fill=URUN, outline=INK, width=1.0)
    d.rectangle([ux0 + 330 * Ss, sy0 + 87 * Ss, ux0 + 470 * Ss, sy0 + 412 * Ss], fill=URUN, outline=INK, width=1.0)
    txt(ux0 + 160 * Ss, sy0 + 250 * Ss, "kaşar DİK\n280 × 325\nyük. 360 ≤ 435", f7, INK, "mm"); txt(ux0 + 400 * Ss, sy0 + 250 * Ss, "kıyma\nDİK\n140", f7, INK, "mm")
    txt(ux0 + 250 * Ss, sy0 + 500 * Ss + 14, "UM+ 500 × 500 · 2 kaset / çevrim (280 + 140)", f8b, ACC, "mm")
    # UM+ 3 dar
    vx0 = ux0 + 500 * Ss + 90
    d.rectangle([vx0, sy0, vx0 + 500 * Ss, sy0 + 500 * Ss], fill=SU, outline=INK, width=1.2)
    for k in range(3):
        d.rectangle([vx0 + (20 + k * 160) * Ss, sy0 + 87 * Ss, vx0 + (160 + k * 160) * Ss, sy0 + 412 * Ss], fill=URUN, outline=INK, width=1.0)
    txt(vx0 + 250 * Ss, sy0 + 250 * Ss, "3 dar kaset DİK · 3 × 140 = 420", f7, INK, "mm")
    txt(vx0 + 250 * Ss, sy0 + 500 * Ss + 14, "UM+ · kıyma + kuşbaşı + sucuk tek çevrim", f8b, ACC, "mm")
    return y


# ================================================================ D · KARŞILAŞTIRMA TABLOSU ================================================================
def tablo(x0, y0):
    txt(x0, y0 - 40, "MEIKO M-iClean U SERİSİ (üretici teknik verisi)", f16, ACC)
    kol = (0, 200, 380, 560, 700, 840, 1040, 1170, 1320)
    bas = ("model", "G × D × Y", "sepet", "kapı ağzı", "çevrim s", "sepet/sa", "durulama L", "güç kW", "F yuvasına (460 × 826)")
    gen = 1560.0
    d.rectangle([x0, y0, x0 + gen, y0 + 28], fill=SOFT, outline=LINE, width=1.0)
    for k, b in zip(kol, bas): txt(x0 + k + 8, y0 + 14, b, f8b, INK, "lm")
    y = y0 + 28
    for M, yuva in ((US, "SIĞAR (460 · 700/730)"), (UM, "genişlik 600: temizlik arkaya alınırsa"), (UMP, "600 · 820 ≤ 826 (6 mm) · temizlik arkaya"), (UL, "600 × 680 · sığar (derinlik 830) · temizlik arkaya")):
        d.line([(x0, y + 26), (x0 + gen, y + 26)], fill=(225, 225, 230), width=0.8)
        vals = (M["ad"], "%d × %d × %d" % (M["W"], M["D"], M["H"]), "%d × %d" % M["sepet"], "%d" % M["giris"], "/".join(str(c) for c in M["cevrim"]), "/".join(str(c) for c in M["sepet_sa"]), sayi(M["durulama"]), sayi(M["kW"]), yuva)
        for k, v in zip(kol, vals): txt(x0 + k + 8, y + 13, v, f8, INK if M is US else GRAY, "lm")
        y += 26
    d.rectangle([x0, y0, x0 + gen, y], outline=LINE, width=1.0)
    return y


# ================================================================ SAYFA ================================================================
txt(150, 60, "AUTOKITCH  ·  BULAŞIK MAKİNESİ  ·  MEIKO M-iClean US (F taban dolabı)  ·  YIKANACAKLAR VE SEPET  ·  TEKNİK RESİM v1", f30, INK, "ls")
txt(150, 100, "ölçüler üretici föyünden (MEIKO M-iClean U teknik veri sayfası + ABD/UM föyleri) · kasetler kendi CAD modellerinden (280/140 × 360 × 325) · ölçüler mm · 27 Eylül 2026", f11, GRAY, "ls")
d.line([(150, 126), (W_PX - 60, 126)], fill=LINE, width=3)
meiko_gorunus(360, 300, US, "MEIKO M-iClean US · 460 × 600 × 700 · sepet 400 × 400 · kapı ağzı 315 (föy)")
dolap(1500, 330)
ty = tablo(1500, 900)
yy = yikanacaklar(190, 1380)
d.line([(150, H_PX - 90), (W_PX - 60, H_PX - 90)], fill=LINE, width=1.2)
txt(150, H_PX - 60, "BULASIK_MAKINESI_v1 · 27 Eyl 2026 · kaynak: meiko.com M-iClean U technical data · MEIKO US Spec_sheets_M-iClean_U.pdf (8-15-21) · M-iClean_UM_Spec_Sheet.pdf · kaset ölçüleri: harc_cad_v4 · kasar_cad_v14 · kiyma_cad_v9 · kusbasi_cad_v8 · sucuk_cad_v7 · UNO: beldos.html (silindir/valf ölçüsü VARSAYIM)", f8, GRAY, "ls")
txt(W_PX - 60, H_PX - 60, "AUTOKITCH · Torinoarch", f11b, INK, "rs")
os.makedirs(KLASOR, exist_ok=True)
yol = os.path.join(KLASOR, "BULASIK_MAKINESI_v1.png")
im.save(yol, optimize=True); im.save(yol.replace(".png", ".pdf"), "PDF", resolution=150.0 * K_HD)
im.resize((int(W_PX * 0.6), int(H_PX * 0.6)), Image.LANCZOS).save(os.path.join(IMG, "BULASIK_MAKINESI_v1.png"), optimize=True)
print("YAZILDI", yol, im.size)
