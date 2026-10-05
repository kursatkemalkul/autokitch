# -*- coding: utf-8 -*-
"""AUTOKITCH · ATOSA TABLALI HAT · TEKNIK RESIM v20 (29 Eyl 2026) — montaj v71: fırın v10 (ısıtılan 1316 / 4 ürün korundu, yükleme bandı ısıtılan bölgenin başında).
v19: AUTOKITCH · ATOSA TABLALI HAT · TEKNIK RESIM v19 · BANTLI TABLA (29 Eyl 2026) — montaj v70 ile eşit:
  tabla Ø340 + disk + aktarma iticisi YERİNE kare bant kaseti 310 × 310 (bantli_tabla_cad_v1) · sabit mıknatıslı tahrik TOPPING sağ-arkada ·
  aktarma 2365,4 · HGR15 ray 2298 (x 200–2498) · fırın v9: yükleme bandı ön odada 2522–2845, ısıtılan 2912–3940 = 1028 (3 ürün) · çıktı klasörleri dosyaya göreli.
v18: AUTOKITCH · ATOSA TABLALI HAT · TEKNIK RESIM v18 · ÖN DÜZLEM +79 · TEMİZ KUTU İSTASYONLAR (28 Eyl 2026)
Önceki: teknik_hat_atosa_tablali_v17.py (montaj v57 alçak hat). v17'nin yapısı + stili aynen; içerik SPEC_on_duzlem_v63.md'ye çevrildi.
Tek kaynak: SPEC_on_duzlem_v63.md + on_duzlem_v63/rapor_{A,B,C,F,K,E}.md + kesif_M.md §4 ("Pafta v17" satır listesi) ve yeni üreteçlerin sabitleri:
  store_cad_v8 (önler +39…+79 · K4 yarıklı sökülür panel + depo çekmecesi · plint ızgarası) · acici_kabin_cad_v1 (A kabini · robot ağzı ·
  ışık perdesi) · kaide_cad_v2 · topping_uno_cad_v14 + topping_cad_v25 (K1 / K2 soğuk kapak · T kapağı · mekanizma kanatları · açıcı
  NMRV030 dik açılı, en önü +31,7) · itici_cad_v5 · firin_tp10_cad_v8 + firin_ust_kabin_cad_v1 (2 düşer kapak · dikmeler · kompresör tavası) ·
  kesme_cad_v6 (3 kapak) + bulasik_cad_v2 (ayaksız, tablada) · kutu_cad_v7 (6 tava panel · robot ağzı) · qr_cad_v1 · tezgah_cad_v1 · ray_ek_cad_v1.
v18 değişiklikleri: bütün ön yüzler FT.ZS (+79) düzleminde · arka −830 sabit → derinlik 909 · kapak bölümleri + derz 3 ön görünüşte ·
kapak arkasındaki her şey kesik çizgi (HDraw.kesik kipi) · A kabini + robot ağzı · E robot ağzı · fırın üstü kabin · plint ön düzlemin
60 gerisinde · kırmızı "fırın çıkıntısı" bandı ve "830 + 79 = 909" istisna yazısı kalktı · deterjan rafı ve E ön alt sacı kalktı ·
derinlik ölçüleri 909 (arka −830 sabit), ray ekseni önden 281 · açıcı uyarısı kalktı (en önü +31,7).
PNG (HD) + EKRAN + PDF (EKRAN, 200 dpi) + site kopyası (4200 px) bu dosya yazar.
Kural: paftada yalnız görünüş + ölçü + parça adı; açıklama mesajda.
"""
import math, sys, os
from contextlib import contextmanager
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kesme_cad_v6 as KS                    # v18: K · 3 kapak tava 20 (+59…+79) · bulaşık tablada (BULASIK_YER y 139) · deterjan yok (tezgâhta)
import firin_tp10_cad_v10 as FT               # v18: F = TP10 · gövde 788–1305 · ön yüzü +79 = ÖN DÜZLEM referansı · raf kompresör açıklıklı
import firin_ust_kabin_cad_v1 as FUK         # v18: fırın üstü kabin · 2 düşer kapak 1308–1859 · dikmeler · kompresör tavası
import bantli_tabla_montaj_v1 as BT          # v19: kaset + sabit tahrik + yükleme bandı (itici_cad_v5 KALKTI)
import topping_hesap_v7 as TH7               # v19: aktarma 1665,4 · ray 1798 · X torku
import store_cad_v8 as SC                    # v18: çekmeceli dolap · önler +39…+79 · derinlik 909
import kutu_cad_v7 as KC                     # v18: E · 6 tava panel · robot ağzı x 85–440 · y 886–1062
import acici_kabin_cad_v1 as AK              # v18: A kabini · alt panel + servis kapağı · robot ağzı 200 × 200 · ışık perdesi
import qr_cad_v1 as QR                       # QR dolabı 860 × 520 × 2050
import tezgah_cad_v1 as TZ                   # tezgâh 600 × 450 × 900
import ray_ek_cad_v1 as RE                   # zincir oluğu · enerji zinciri · zemin kanalı
import topping_cad_v25 as TC_V25               # v18b: C ön paneli sabitleri (MEK_PAN_Y0 788 · T_YARIK_Y) — elle yazılmış eski değerler yerine
import kaide_cad_v2 as KD                    # v18: A / C mekanizma kaidesi 788–892 · C ön profil +35 · A taban sacı +39
from PIL import Image, ImageDraw, ImageFont

# ===================== HD KATMANI =====================
# Cizimin TAMAMI K katina olceklenir: koordinatlar, cizgi kalinliklari ve fontlar.
# Boylece sabit piksel kaydirmalari (yaziyi cizginin 26 px altina koy gibi) da
# olcekleniyor ve duzen birebir korunuyor.
K_HD = 2.2


def _ol(v):
    """koordinat dizisini/sayisini olcekle"""
    if isinstance(v, (int, float)):
        return v * K_HD
    if isinstance(v, (list, tuple)):
        return [_ol(x) for x in v]
    return v


class HDraw:
    """ImageDraw sarmalayicisi — her cagriyi K_HD katina cikarir
    v18: kesik kipi (self.kesik = True): dolgu çizilmez, bütün kenarlar / çizgiler / yaylar kesik çizgi olur
    (ön görünüşte kapak arkasında kalan parçalar · lejant: "kesik çizgi = kapak arkası parça"). Yazı etkilenmez."""

    def __init__(self, im):
        self.d = ImageDraw.Draw(im)
        self._font = {}
        self.kesik = False

    @staticmethod
    def _renk(kw):
        c = kw.get("outline") or kw.get("fill")
        if c is None or (isinstance(c, tuple) and sum(c[:3]) > 640):          # çok açık dolgular (SOFT, PUC …) kesikte çizilmez
            return None
        return c

    def _kline(self, p0, p1, c, dash=7.0, gap=4.0):
        (ax, ay), (bx, by) = p0, p1
        L = math.hypot(bx - ax, by - ay)
        if L < 0.5:
            return
        w = max(1, int(round(1 * K_HD)))
        for i in range(int(L // (dash + gap)) + 1):
            t0 = min(1.0, i * (dash + gap) / L)
            t1 = min(1.0, (i * (dash + gap) + dash) / L)
            if t1 > t0:
                self.d.line(_ol([(ax + (bx - ax) * t0, ay + (by - ay) * t0), (ax + (bx - ax) * t1, ay + (by - ay) * t1)]), fill=c, width=w)

    def _kpoly(self, pts, c, kapali=True):
        pts = [tuple(p) for p in pts]
        for a, b in zip(pts, pts[1:] + (pts[:1] if kapali else [])):
            self._kline(a, b, c)

    @staticmethod
    def _kutu(xy):
        if len(xy) == 2:
            (x0, y0), (x1, y1) = xy
        else:
            x0, y0, x1, y1 = xy
        return min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1)

    def _karc(self, xy, a0, a1, c, adim=4.0):
        w = max(1, int(round(1 * K_HD)))
        a = a0
        while a < a1:
            b = min(a1, a + adim)
            self.d.arc(_ol(list(xy)), a, b, fill=c, width=w)
            a = b + adim

    def _f(self, f):
        if f is None:
            return None
        k = id(f)
        if k not in self._font:
            try:
                yol = f.path
                boy = f.size
                self._font[k] = ImageFont.truetype(yol, max(1, int(round(boy * K_HD))))
            except Exception:
                self._font[k] = f
        return self._font[k]

    def _w(self, kw):
        if "width" in kw and isinstance(kw["width"], (int, float)):
            kw["width"] = max(1, int(round(kw["width"] * K_HD)))
        if "font" in kw:
            kw["font"] = self._f(kw["font"])
        return kw

    def text(self, xy, s, **kw):
        return self.d.text(_ol(xy), s, **self._w(kw))

    def line(self, xy, **kw):
        if self.kesik:
            c = self._renk(kw)
            if c is not None:
                self._kpoly(list(xy), c, kapali=False)
            return None
        return self.d.line(_ol(xy), **self._w(kw))

    def rectangle(self, xy, **kw):
        if self.kesik:
            c = self._renk(kw)
            if c is not None:
                x0, y0, x1, y1 = self._kutu(xy)
                self._kpoly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], c)
            return None
        return self.d.rectangle(_ol(xy), **self._w(kw))

    def ellipse(self, xy, **kw):
        if self.kesik:
            c = self._renk(kw)
            if c is not None:
                self._karc(self._kutu(xy), 0.0, 360.0, c)
            return None
        return self.d.ellipse(_ol(xy), **self._w(kw))

    def polygon(self, xy, **kw):
        if self.kesik:
            c = self._renk(kw)
            if c is not None:
                self._kpoly(list(xy), c)
            return None
        return self.d.polygon(_ol(xy), **self._w(kw))

    def arc(self, xy, *a, **kw):
        if self.kesik:
            c = self._renk(kw)
            if c is not None:
                self._karc(self._kutu(xy), a[0], a[1], c)
            return None
        return self.d.arc(_ol(xy), *a, **self._w(kw))

    def textlength(self, s, font=None, **kw):
        # olceklenmemis (cizim koordinat sisteminde) uzunluk dondur
        return self.d.textlength(s, font=self._f(font), **kw) / K_HD
# ======================================================

KLASOR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "FULL_MAKINE")                       # v19: dosyaya göreli (iş klasörü)
SITE_IMG = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "otonom", "hat", "img")   # v19: dosyaya göreli
AD_DOSYA = "HAT_ATOSA_TABLALI_v20"
W_PX, H_PX, S = 6600, 3600, 0.56             # v17: 3400 → 3600 (plan tezgâh + ön duvara kadar, z 1879)
BG, INK, GRAY, LINE = (255, 255, 255), (26, 26, 28), (132, 132, 140), (72, 72, 78)
FILL, ACC, RED, SOFT = (244, 244, 246), (0, 86, 184), (198, 42, 32), (228, 228, 234)
BUZ, DOLAP, BOSL, PUC, EVC = (28, 86, 166), (14, 120, 90), (190, 190, 196), (255, 240, 200), (220, 235, 255)
AGZ, SICAK, TURUNCU, URUN = (253, 244, 243), (255, 226, 214), (200, 90, 30), (240, 214, 170)
KOLI_R, ZINCIR_R = (255, 244, 230), (96, 96, 102)


def F(sz, b=False):
    for n in (("arialbd.ttf", "segoeuib.ttf") if b else ("arial.ttf", "segoeui.ttf")):
        try:
            return ImageFont.truetype(n, sz)
        except Exception:
            pass
    return ImageFont.load_default()


f7, f8, f9, f11, f13, f16, f38 = F(14), F(16), F(18), F(21), F(24), F(28, True), F(54, True)
im = d = None
TASMA = []
yazi = []                                                           # v17: sonradan maskeli yazılacak ağız yazıları                                                          # v17: kutusundan taşan yazı denetimi


def txt(x, y, s, f=None, c=INK, a="la"):
    d.text((x, y), s, font=f or f11, fill=c, anchor=a)


def maskeli(x, y, s, f, c, a="mm", pay=3, zemin=BG):
    """v17: yazının altına zemin rengi dikdörtgen (altındaki çizgi yazıyı kesmesin)"""
    tw = d.textlength(s, font=f)
    x0 = x - tw / 2 if a[0] == "m" else (x - tw if a[0] == "r" else x)
    h = f.size * 0.55
    d.rectangle([x0 - pay, y - h - 1, x0 + tw + pay, y + h + 1], fill=zemin)
    txt(x, y, s, f, c, a)


def satirlar(x, y, s, f, c, adim=20):
    ls = s.split("|")
    y0 = y - adim * (len(ls) - 1) / 2.0
    for i, l in enumerate(ls):
        txt(x, y0 + i * adim, l, f if i == 0 else f7, c if i == 0 else GRAY, "mm")


def sayi(v):
    return ("%g" % v).replace(".", ",")


def etiket(x, y, s, f=None, c=INK, cer=GRAY):
    f = f or f8
    tw = d.textlength(s, font=f)
    d.rectangle([x - tw / 2 - 6, y - 11, x + tw / 2 + 6, y + 11], fill=BG, outline=cer, width=1)
    txt(x, y, s, f, c, "mm")


def olcu_h(x0, x1, y, s, f=None, c=INK):
    f = f or f11
    d.line([(x0, y), (x1, y)], fill=c, width=2)
    for xx in (x0, x1):
        d.line([(xx, y - 8), (xx, y + 8)], fill=c, width=2)
    tw = d.textlength(s, font=f)
    d.rectangle([(x0 + x1) / 2 - tw / 2 - 6, y - 13, (x0 + x1) / 2 + tw / 2 + 6, y + 13], fill=BG)
    txt((x0 + x1) / 2, y, s, f, c, "mm")


def olcu_v(x, y0, y1, s, f=None, c=INK, yon="r"):
    f = f or f11
    d.line([(x, y0), (x, y1)], fill=c, width=2)
    for yy in (y0, y1):
        d.line([(x - 8, yy), (x + 8, yy)], fill=c, width=2)
    txt(x + (12 if yon == "r" else -12), (y0 + y1) / 2, s, f, c, "lm" if yon == "r" else "rm")


def tarali(x0, y0, x1, y1, c=(222, 222, 228), adim=12):
    w, h = x1 - x0, y1 - y0
    for k in range(0, int(w + h), adim):
        ax, ay, bx, by = x0 + k, y1, x0 + k - h, y0
        if ax > x1:
            ay, ax = y1 - (ax - x1), x1
        if bx < x0:
            by, bx = y1 - k, x0
        if ay >= y0:
            d.line([(ax, ay), (bx, by)], fill=c, width=1)


def dline(p0, p1, c, w=1, dash=7, gap=4):
    (ax, ay), (bx, by) = p0, p1
    L = math.hypot(bx - ax, by - ay)
    if L < 1:
        return
    for i in range(int(L // (dash + gap)) + 1):
        t0 = min(1.0, i * (dash + gap) / L)
        t1 = min(1.0, (i * (dash + gap) + dash) / L)
        d.line([(ax + (bx - ax) * t0, ay + (by - ay) * t0), (ax + (bx - ax) * t1, ay + (by - ay) * t1)], fill=c, width=w)


def drect(x0, y0, x1, y1, c, w=1):
    dline((x0, y0), (x1, y0), c, w); dline((x1, y0), (x1, y1), c, w)
    dline((x1, y1), (x0, y1), c, w); dline((x0, y1), (x0, y0), c, w)


def darc(cx, cy, r, a0, a1, c, w=2, adim=4.0):
    a = a0
    while a < a1:
        b = min(a1, a + adim)
        d.arc([cx - r, cy - r, cx + r, cy + r], a, b, fill=c, width=w)
        a = b + adim


@contextmanager
def arkada():
    """v18: ön görünüşte kapak / panel ARKASINDA kalan parçalar → kesik çizgi (dolgusuz)"""
    d.kesik = True
    try:
        yield
    finally:
        d.kesik = False


def panel(x0, x1, y0, y1, c=None, w=2, dolgu=None):
    """v18: ön düzlemdeki (+79) panel / kapak · dünya mm · komşusuyla arasında 3 mm derz (ayrı dikdörtgen)"""
    d.rectangle([fx(x0), fy(y1), fx(x1), fy(y0)], fill=(dolgu or BG), outline=(c or LINE), width=w)


def yarik(x0, x1, y0, y1):
    """v18: lazer yarık / ızgara açıklığı (önden görünür)"""
    d.rectangle([fx(x0), fy(y1), fx(x1), fy(y0)], fill=FILL, outline=GRAY, width=1)


def pan_etiket(x, y, s, c=GRAY):
    """v18: panel adı (küçük, sol üst köşe) · x, y dünya mm (sol üst)"""
    txt(fx(x) + 6, fy(y) + 9, s, f7, c, "la")


# ======================= ORTAK VERI (HAT 2 KOL v19) =======================
DZ = 830.0                                   # ARKA yüz −830 (SABİT) · py() / z() arkaya göre hesaplar — değişmez
ZON = FT.ZS                                  # v18: ÖN DÜZLEM +79 = fırın gövdesinin ön yüzü (bütün kapak / panel dış yüzleri)
DERIN = DZ + ZON                             # v18: gövde derinliği 909
DERZ = 3.0                                   # v18: panel ↔ panel derzi
Z_TAVA = ZON - 20.0                          # v18: tava panel arkası +59 (kuru kapak 20)
Z_SOG = ZON - 40.0                           # v18: soğuk kapak / çekmece önü arkası +39 (40 sandviç)
assert SC.Z_ON == KS.Z_ON == KC.Z_ON == AK.Z_ON == FUK.Z_ON == FT.Z_ON == ZON == 79.0, "ön düzlem sözleşmesi"
assert SC.Z_ARKA_DIS == -DZ and SC.DERINLIK == DERIN == 909.0, "arka −830 · derinlik 909"
# C ön yüzü (topping_cad_v25 L1203 PANEL · topping_uno_cad_v14 SKAPAK/FLIP) — dünya x, y · soğuk kapaklar 40 (+39…+79), diğerleri tava 20
C_SOGUK = (("K1", 701.5, 1518.5, 1110.5, 1859.0), ("K2", 1521.5, 2497.0, 1110.5, 1550.5))
C_TAVA = (("mekanizma kanadı sol", 701.5, 1597.75, TC_V25.MEK_PAN_Y0, 1107.5), ("mekanizma kanadı sağ", 1600.75, 2497.0, TC_V25.MEK_PAN_Y0, 1107.5),   # v18b: kanatlar 788 (topping_cad_v25b)
          ("T · teknik cep kapağı", 1521.5, 2497.0, 1553.5, 1859.0))
C_FLIP = (1493.0, 1547.0)                    # K1 kenarındaki katlanır orta dikme (ısıtıcılı) · ön yüzü +24 (kapak arkası)
C_T_YARIK = ([(700.0 + xg, 700.0 + xg + 60.0, 892.0 + TC_V25.T_YARIK_Y[0] + 10.0 * k, 892.0 + TC_V25.T_YARIK_Y[0] + 4.0 + 10.0 * k) for xg in (860.0, 930.0, 1000.0, 1070.0) for k in range(8)] +
             [(700.0 + xg, 700.0 + xg + 60.0, 892.0 + TC_V25.T_YARIK_Y[1] + 10.0 * k, 892.0 + TC_V25.T_YARIK_Y[1] + 4.0 + 10.0 * k) for xg in (1480.0, 1550.0, 1620.0, 1690.0) for k in range(8)])   # topping_cad_v25 L1050–1056 · 64 × 60 × 4
F_YARIK = [(a + FUK.YARIK_X0 + i * FUK.YARIK_ADIM, a + FUK.YARIK_X0 + i * FUK.YARIK_ADIM + FUK.YARIK_W, yr, yr + FUK.YARIK_H)
           for a, _b in FUK.KANAT_X for sira in FUK.YARIK_SIRA for yr in sira for i in range(FUK.YARIK_N)]                                  # firin_ust_kabin_cad_v1 L321–325
WO, BIND, FUGA, BOLME, XI = 620.0, 15.0, 3.0, 35.0, 62.5
YUZ0 = 167.5
HH = {"hamur": 75.0, "lahm": 60.0, "icecek": 241.0, "ic1": 126.0, "ic1d": 126.0, "tatli": 71.0}
AD = {"hamur": "TAZE PİDE", "lahm": "LAHMACUN", "ic1": "İÇECEK · tek kat", "tatli": "TATLI"}
CAP = {"hamur": (20, "top"), "lahm": (36, "top"), "ic1": (48, "kutu"), "tatli": (12, "kap")}       # v17: tatlı 2 şerit × 6
KOLON_AD = SC.KOLON_AD                                        # store_cad_v8: ("K1", "K2", "K3", "K5", "K6") + K4 (Secop + depo)
CEK_KOL = {k: [c for c in SC.CEK if c[0] == k] for k in KOLON_AD}      # (kol, kod, tip, x0, yo) · alttan üste
H_B, H_MAK = SC.H_B, KS.H                                     # v17: 788 düz çizgi (dolap üstü = A, C, fırın altı) · makine üstü 1862
H_MEK = KD.Y_MEK                                              # v17: A / C mekanizma tabanı 892 (kaide 788–892)
X_A, W_A, X_C, W_C, W_B = 0.0, 700.0, 700.0, 1800.0, SC.W_B  # v17: dolap TEK PARÇA 0–4000
X_F, W_F, X_K, W_K, X_E, W_E = 2500.0, 1500.0, 4000.0, 600.0, 4600.0, 830.0
HAT = X_E + W_E                                              # 5430
Y_ALT, B_TABAN = 123.0, 164.5                                # ALT TABAN ÇİZGİSİ · dolap iç taban üstü (en alt çekmece önü 167,5 − 3)
P_SUREC, BANT_F, PLAKA_K, TEPSI_E = FT.DISK_UST, FT.BANT_UST_HAT, KS.BANT, KC.TEPSI   # v17: 1000 · 998 · 996 · 936
ZT = -170.0                                                  # tabla / ürün ekseni
HAZNE, ADIM = 1400.0, 350.0
KOR = (FT.ZS, TZ.INCE_DUVAR_Z[0])                            # v17: koridor 900 fırın çıkıntısından (z 79–979) · dükkân v13
INCE = TZ.INCE_DUVAR_Z                                       # ince duvar z 979–1039 (x 0–4570)
ON_DUVAR = TZ.Z0 + TZ.D                                      # 1879 · tezgâh ön duvara yaslı
RZ, OMUZ, A2, A3 = RE.RZ, 970.0, 425.0, 395.0                # ray ekseni 360 (DEĞİŞMEZ) · FR5 omuz · kol boyları
ERISIM = 779.0                                               # FR5 pratik bilek erisimi (820 x 0,95)
RX = RE.RX_MONTAJ                                            # 2650 · TEK ROBOT çizimde hattın ortasında
QRX, QRZ, QR_H = (QR.X0, QR.X0 + QR.W), (QR.Z0, QR.Z0 + QR.D), QR.H   # v17: x 4570–5430 · z 670–1190 · 2050
QR_SATIR = QR.GOZ_TABAN                                      # 450 … 1450 (adım 200)

OX, FY_TOP = 300.0, 420.0
FY = FY_TOP + H_MAK * S
PY_TOP = FY + 360.0
SX1 = OX + HAT * S + 270.0
SEC_W = (790.0 + 1390.0) * S
SX2 = SX1 + SEC_W + 190.0


def fx(x):
    return OX + x * S


def fy(y):
    return FY - y * S


def py(z):
    return PY_TOP + (z + 830.0) * S                                  # arka −830 (model), ön 0, koridor +


def kabin(x0mm, w, y0, y1, ad=""):
    x0, x1 = fx(x0mm), fx(x0mm + w)
    if y0 == 0.0:                                                   # gövde 123'ten, altı ayak + süpürgelik (30 içeride)
        d.rectangle([x0, fy(y1), x1, fy(Y_ALT)], fill=FILL, outline=LINE, width=4)
        d.rectangle([fx(x0mm + 30.0), fy(Y_ALT), fx(x0mm + w - 30.0), fy(0)], fill=SOFT, outline=LINE, width=2)
    else:
        d.rectangle([x0, fy(y1), x1, fy(y0)], fill=FILL, outline=LINE, width=4)
    if ad:
        txt((x0 + x1) / 2, fy(H_MAK) - 64, ad, f13, INK, "md")


def kapak(x0mm, a, b, y0, y1, et="", yl=None, fill=None):
    d.rectangle([fx(x0mm + a), fy(y1), fx(x0mm + b), fy(y0)], fill=(fill or BG), outline=LINE, width=2)
    if et:
        satirlar(fx(x0mm + (a + b) / 2), fy(yl if yl else (y0 + y1) / 2), et, f8, INK)


def agiz(x0mm, a, b, y0, y1, et, kot=True):
    d.rectangle([fx(x0mm + a), fy(y1), fx(x0mm + b), fy(y0)], fill=AGZ, outline=RED, width=3)
    cy = (fy(y0) + fy(y1)) / 2
    yazi.append((fx(x0mm + (a + b) / 2), cy - (10 if kot else 0), et, f8, RED, "mm", AGZ))      # v17: ağız içinden geçen çizgiler yazıyı kesmesin → en sonda maskeli
    if kot:
        yazi.append((fx(x0mm + (a + b) / 2), cy + 12, "y %s – %s" % (sayi(y0), sayi(y1)), f7, RED, "mm", AGZ))


def kesik(x0mm, a, b, y0, y1, et="", c=INK, alt=""):
    drect(fx(x0mm + a), fy(y1), fx(x0mm + b), fy(y0), c, 1)
    if et:
        txt(fx(x0mm + (a + b) / 2), fy((y0 + y1) / 2) - (8 if alt else 0), et, f7, c, "mm")
    if alt:
        _n = alt.count("|")
        satirlar(fx(x0mm + (a + b) / 2), fy((y0 + y1) / 2) + 10 + 8.5 * _n, alt, f7, GRAY, 17)


def modul_etiketi(x0mm, w, ad, olcu, renk=ACC, sira=0):
    x0, x1 = fx(x0mm) + 6, fx(x0mm + w) - 6
    yb = fy(0) + 126 + sira * 50
    d.rectangle([x0, yb, x1, yb + 46], fill=renk)
    txt((x0 + x1) / 2, yb + 14, ad, f8, BG, "mm")
    txt((x0 + x1) / 2, yb + 34, olcu, f7, BG, "mm")
    for s_, f_ in ((ad, f8), (olcu, f7)):
        if d.textlength(s_, font=f_) > x1 - x0 - 8:
            TASMA.append(("modul_etiketi", s_))


def kaide(x0, x1, et=""):
    """v17 · kaide_cad_v1: 40 × 100 × 2 kutu profil + 4 mm plaka · 788–892 (dolap üstüne düz oturur)"""
    d.rectangle([fx(x0), fy(H_MEK), fx(x1), fy(H_B)], fill=SOFT, outline=LINE, width=2)
    if et:
        txt(fx((x0 + x1) / 2), fy((H_B + H_MEK) / 2), et, f7, INK, "mm")


# ======================= MODÜL B · TEK PARÇA ÇEKMECELİ DOLAP (store_cad_v8) =======================
def ciz_B():
    """v17 · store_cad_v6: 0–4000 × 123–788 · 24 motorlu çekmece · tam kaplayan önler 126 → 785 · aralar 3 ·
    K5 + K6 fırın altında (PU 60 ısı kalkanı 728–788) · şerit 3810–4000 robot çöpü (soğuk değil)"""
    kabin(X_A, W_B, 0.0, H_B)
    for kol in KOLON_AD:
        cek = CEK_KOL[kol]
        a_, b_ = SC.KAPAK_X[kol]
        pn = []
        for i, (_k, kod, tip, x0, yo) in enumerate(cek):
            p0 = SC.ON_ALT if i == 0 else yo - BIND
            p1 = SC.ON_UST if i == len(cek) - 1 else yo + HH[tip] + BIND
            pn.append((p0, p1, tip))
        for p0, p1, tip in pn:
            d.rectangle([fx(a_), fy(p1), fx(b_), fy(p0)], fill=BG, outline=DOLAP, width=1)
        gr = []                                                     # ardışık aynı tipler
        for p0, p1, tip in pn:
            if gr and gr[-1][2] == tip:
                gr[-1][1] = p1; gr[-1][3] += 1
            else:
                gr.append([p0, p1, tip, 1])
        for g0, g1, tip, n in gr:
            ym = (fy(g0) + fy(g1)) / 2
            cap, br = CAP[tip]
            etiket(fx((a_ + b_) / 2), ym - 13, "%s × %d" % (AD[tip], n), f8, INK, DOLAP)
            etiket(fx((a_ + b_) / 2), ym + 13, "%d %s · +3 °C" % (n * cap, br), f7, DOLAP, DOLAP)
        txt(fx((a_ + b_) / 2), fy(Y_ALT) + 14, kol, f7, GRAY, "mm")
        olcu_h(fx(a_), fx(b_), fy(0) + 44, sayi(b_ - a_), f8, GRAY)
    # K4 · Secop (önde) + B panosu (arkada) + kaşar/sucuk deposu · dar içecek YOK
    a_, b_ = SC.KAPAK_X["K4"]
    for y0_, y1_ in ((SC.ON_ALT, 420.5), (423.5, SC.ON_UST)):          # k4_kapak_sogutma (ızgaralı) · k4_kapak_depo
        d.rectangle([fx(a_), fy(y1_), fx(b_), fy(y0_)], fill=BG, outline=DOLAP, width=1)
    kesik(0.0, 2052.5, 2402.5, 128.5, 400.5, "SOĞUTMA GRUBU", INK, "Secop CU KLF4.0CND|ızgaralı kapak|arkasında B panosu (PLC)")
    satirlar(fx((a_ + b_) / 2), fy(604.0), "KAŞAR + SUCUK DEPOSU · 2 gün|GN 1/1-100 + GN 1/2-100 · +3 °C", f8, INK, 19)
    txt(fx((a_ + b_) / 2), fy(Y_ALT) + 14, "K4", f7, GRAY, "mm")
    olcu_h(fx(a_), fx(b_), fy(0) + 44, sayi(b_ - a_), f8, GRAY)
    # PU 60 ısı kalkanı · fırın altında, dolabın içinde (önlerin arkası)
    kesik(0.0, SC.X_F[0], SC.X_F[1], 728.0, H_B, "", TURUNCU)
    txt(fx(SC.X_F[0] + 20.0), fy(758.0), "PU 60 ısı kalkanı · fırın altı", f7, TURUNCU, "lm")
    # ŞERİT 3810–4000 · robot çöpü (soğuk değil) · servis kapağı + klape paneli
    a_, b_ = SC.KAPAK_X["SERIT"]
    for y0_, y1_ in (SC.SERIT_KAPI, SC.SERIT_PANEL):
        d.rectangle([fx(a_), fy(y1_), fx(b_), fy(y0_)], fill=BG, outline=LINE, width=1)
    k0, k1, k2, k3 = SC.KLAPE_AC
    d.rectangle([fx(k0), fy(k3), fx(k1), fy(k2)], fill=AGZ, outline=RED, width=2)
    txt(fx((k0 + k1) / 2), fy((k2 + k3) / 2), "klape", f7, RED, "mm")
    d.line([(fx(k0), fy(SC.KLAPE_EKSEN[0])), (fx(k1), fy(SC.KLAPE_EKSEN[0]))], fill=INK, width=2)
    kv = SC.KOVA
    kesik(0.0, kv[0], kv[1], kv[2], kv[3], "", INK)
    satirlar(fx((kv[0] + kv[1]) / 2), fy((kv[2] + kv[3]) / 2), "ROBOT|ÇÖPÜ|15 L · poşet", f7, INK, 17)
    txt(fx((a_ + b_) / 2), fy(Y_ALT) + 14, "şerit", f7, GRAY, "mm")
    olcu_h(fx(a_), fx(b_), fy(0) + 44, sayi(b_ - a_), f8, GRAY)
    d.line([(fx(X_A), fy(H_B)), (fx(X_A + W_B), fy(H_B))], fill=LINE, width=4)
    modul_etiketi(X_A, W_B, "MODÜL B · ÇEKMECELİ DOLAP (store_cad_v8) · TEK PARÇA · 24 motorlu çekmece: 8 pide + 12 lahmacun + 3 içecek + 1 tatlı · K4: Secop (arkasında PLC) + kaşar/sucuk deposu · şerit: robot çöpü",
                  "%s × 909 × %s · ön yüz 126–785 · aralar 3 · +3 °C · K5 + K6 fırın altında" % (sayi(W_B), sayi(H_B)), DOLAP, 1)


# ======================= FIRIN · KESME · KUTU =======================
def ciz_F():
    """v17 · firin_tp10_cad_v7: gövde 788–1305 · 79 mm öne · dolabın üstünde · üstte raf 4 mm (10 takoz):
    SOL kutu yedeği 320 · orta boş (temizlik tezgâha) · SAĞ kompresör · davlumbaz arka yarıda"""
    G0, G1 = FT.YG0, FT.YG1
    kabin(X_F, W_F, H_B, H_MAK, "F · TP10 FIRIN · 1500 özel sipariş · 79 mm öne")
    d.rectangle([fx(FT.X_F0), fy(G1), fx(FT.X_F1), fy(G0)], fill=SOFT, outline=INK, width=3)
    tarali(fx(FT.X_DUV0), fy(G1 - 2), fx(FT.X_TUN0), fy(G0 + 2), (226, 214, 190), 11)
    tarali(fx(FT.X_TUN1), fy(G1 - 2), fx(FT.X_F1 - 2), fy(G0 + 2), (226, 214, 190), 11)
    d.rectangle([fx(FT.X_TUN0), fy(FT.TUN_Y[1]), fx(FT.X_TUN1), fy(FT.TUN_Y[0])], fill=SICAK, outline=TURUNCU, width=2)
    txt(fx((FT.X_F0 + FT.X_DUV0) / 2), fy(G1 - 40.0) - 8, "ön", f7, GRAY, "mm")      # denetçi: 64 mm ön odaya sığsın (iki satır)
    txt(fx((FT.X_F0 + FT.X_DUV0) / 2), fy(G1 - 40.0) + 8, "oda", f7, GRAY, "mm")
    d.line([(fx(FT.BANT_X[0]), fy(BANT_F)), (fx(FT.BANT_X[1]), fy(BANT_F))], fill=TURUNCU, width=4)
    for xr in FT.RULO_X:
        d.ellipse([fx(xr - 20), fy(FT.RULO_Y + 20), fx(xr + 20), fy(FT.RULO_Y - 20)], fill=BG, outline=TURUNCU, width=2)
    xm = (FT.X_TUN0 + FT.X_TUN1) / 2.0
    for i in range(FT.N_URUN):
        xx = xm + (i - (FT.N_URUN - 1) / 2.0) * FT.ADIM
        d.ellipse([fx(xx - 150), fy(BANT_F + 28.0), fx(xx + 150), fy(BANT_F + 2.0)], fill=URUN, outline=(180, 140, 70), width=1)
    txt(fx(xm), fy(FT.TUN_Y[1] - 40.0), "ISITILAN %s · kızılötesi üst + alt · aynı anda %d ürün (adım %s) · bant üstü %s" % (sayi(FT.ODA), FT.N_URUN, sayi(FT.ADIM), sayi(BANT_F)), f7, TURUNCU, "mm")
    txt(fx(xm), fy(G1 - 30.0), "gövde ön yüzü 79 mm ÖNDE (çıkıntı · y %s–%s) → üst görünüş" % (sayi(G0), sayi(G1)), f7, RED, "mm")
    # giriş bandı (ön odada) + çıkış ölü plakası
    d.rectangle([fx(FT.YB_BURUN[0] - 6.35), fy(BT.UST), fx(FT.YB_SON), fy(FT.YB_TAHRIK[1] - FT.YB_TAHRIK[2] - 0.35)], fill=EVC, outline=BUZ, width=2)   # v19: yükleme bandı
    txt(fx((FT.YB_BURUN[0] + FT.YB_SON) / 2.0), fy(BT.UST + 22.0), "YÜKLEME BANDI %s–%s" % (sayi(round(FT.YB_BURUN[0] - 6.35, 1)), sayi(round(FT.YB_SON, 1))), f7, BUZ, "mm")
    d.rectangle([fx(3997.0), fy(BANT_F - 0.5), fx(4018.0), fy(BANT_F - 3.0)], fill=INK)
    # üst: ışınım kalkanı + 10 takoz + 4 mm raf · SOL kutu yedeği 320 · orta boş · SAĞ kompresör · davlumbaz arka yarı
    d.line([(fx(FT.X_F0 + 10), fy(FT.ISI_KALKANI_Y[0])), (fx(FT.X_F1 - 10), fy(FT.ISI_KALKANI_Y[0]))], fill=GRAY, width=2)
    for xt in sorted(set(x_ for x_, z_ in FT.TAKOZ_XZ)):
        d.rectangle([fx(xt - 8), fy(FT.UST_RAF_Y[0]), fx(xt + 8), fy(G1)], fill=BG, outline=INK, width=1)
    RAF = FT.UST_RAF_Y[1]                                          # 1348
    d.rectangle([fx(FT.X_F0 + 10), fy(RAF), fx(FT.X_F1 - 10), fy(FT.UST_RAF_Y[0])], fill=INK)
    drect(fx(FT.X_F0 + 3), fy(H_MAK - 3.0), fx(FT.X_F1 - 3), fy(FT.ISI_KALKANI_Y[1] + 2.0), GRAY, 1)
    d.rectangle([fx(2520.0), fy(H_MAK - 2.0), fx(3324.0), fy(RAF)], fill=(252, 240, 215), outline=LINE, width=2)
    satirlar(fx(2922.0), fy(1632.0), "PİZZA KUTUSU YEDEĞİ · TEK YER|320 kutu düz · 804 × 404 × 512|şarjör 462 (≈ 432 kullanılır) + 320|arkada davlumbaz · raf 4 mm, 10 takoz", f8, INK, 20)
    txt(fx(3462.0), fy(1632.0), "BOŞ 262", f7, GRAY, "mm")
    d.rectangle([fx(3600.0), fy(H_MAK - 4.0), fx(3980.0), fy(RAF)], fill=BG, outline=ACC, width=2)
    satirlar(fx(3790.0), fy(1632.0), "KOMPRESÖR|JUN-AIR OF302-15B|25 kg · 380 × 380 × 510", f8, ACC, 20)
    modul_etiketi(X_F, W_F, "MODÜL F · TP10 FIRIN (firin_tp10_cad_v10) + ÜST KABİN", "1500 × 909 × %s · dolap üstünde · gövde %s–%s · bant %s · 79 öne" % (sayi(H_MAK - H_B), sayi(G0), sayi(G1), sayi(BANT_F)))
    olcu_h(fx(X_F), fx(X_F + W_F), fy(H_MAK) - 26, sayi(W_F), f11, INK)


def ciz_K():
    """v18 · kesme_cad_v6: taban sacı 892–895 · bant 996 · 3 kapak (tava 20) · ALTINDA bulaşık (bulasik_cad_v2, ayaksız, tablada)"""
    kabin(X_K, W_K, 0.0, H_MAK, "K · KESME + SPREY")
    d.rectangle([fx(X_K), fy(KS.H_B + 3.0), fx(X_K + W_K), fy(KS.H_B)], fill=LINE)         # taban sacı 892–895
    # K altı: bulaşık makinesi (v18: ayaksız, kirişli tablada · deterjan / parlatıcı rafı yok — tezgâhta)
    ZB = KS.BULASIK_ZARF
    d.rectangle([fx(X_K + ZB["x"][0]), fy(ZB["y"][1]), fx(X_K + ZB["x"][1]), fy(ZB["y"][0])], fill=None, outline=LINE, width=2)
    satirlar(fx(X_K + (ZB["x"][0] + ZB["x"][1]) / 2), fy(752.0), "BULAŞIK MAKİNESİ|MEIKO M-iClean US|460 × 633 × 700 · sağa yaslı", f8, INK, 20)
    kesik(X_K, 54.0, 226.0, 1467.0, 1812.0, "TEREYAĞI", RED, "3 L · ısıtmalı|basınçlı tank|MS4 + valf")
    kesik(X_K, 300.0, 565.0, 1472.0, 1857.0, "PANO (arkada)", GRAY, "S7-1200 · STP-DRV|NDR-240 · PNOZ|PWM sprey")
    # K bandı
    d.rectangle([fx(X_K + KS.X_KUYRUK), fy(KS.BANT), fx(X_K + KS.X_TAHRIK), fy(KS.BANT - 6.0)], fill=EVC, outline=BUZ, width=2)
    for xr, yr, rr in ((KS.X_KUYRUK, KS.Y_KUYRUK, KS.R_KUYRUK), (KS.X_TAHRIK, KS.Y_TAHRIK, KS.R_TAHRIK)):
        d.ellipse([fx(X_K + xr - rr), fy(yr + rr), fx(X_K + xr + rr), fy(yr - rr)], fill=BG, outline=BUZ, width=2)
    txt(fx(X_K + 300.0), fy(KS.BANT + 24.0), "K BANDI 400", f7, BUZ, "mm")
    # kesici + sprey kafası (yukarıda)
    d.rectangle([fx(X_K + 3), fy(KS.Y_KIRIS[1]), fx(X_K + W_K - 3), fy(KS.Y_KIRIS[0])], fill=SOFT, outline=LINE, width=2)
    d.rectangle([fx(X_K + 225), fy(KS.Y_GOVDE[1]), fx(X_K + 375), fy(KS.Y_GOVDE[0])], fill=BG, outline=INK, width=2)
    _gm = fy((KS.Y_GOVDE[0] + KS.Y_GOVDE[1]) / 2)
    txt(fx(X_K + 215), _gm - 27, "Festo", f7, INK, "rm")
    txt(fx(X_K + 215), _gm - 9, "DGRF-C-63-125", f7, INK, "rm")
    txt(fx(X_K + 215), _gm + 9, "1870 N", f7, GRAY, "rm")
    txt(fx(X_K + 215), _gm + 27, "strok 125", f7, GRAY, "rm")
    d.rectangle([fx(X_K + 215), fy(KS.Y_ON_PL[1]), fx(X_K + 385), fy(KS.Y_ON_PL[0])], fill=BG, outline=INK, width=2)
    d.rectangle([fx(X_K + 305), fy(1218.0), fx(X_K + 405), fy(1180.0)], fill=(255, 236, 200), outline=RED, width=2)
    txt(fx(X_K + 470), fy(1199.0), "PulsaJet", f7, RED, "lm")
    d.rectangle([fx(X_K + 185), fy(KS.Y_KAFA[1]), fx(X_K + 415), fy(KS.Y_KAFA[0])], fill=BG, outline=INK, width=2)
    drect(fx(X_K + 300 - KS.KORUMA_R[1]), fy(KS.Y_KAFA[0]), fx(X_K + 300 + KS.KORUMA_R[1]), fy(KS.KORUMA_ALT), INK, 1)
    for i in range(7):
        xx = X_K + 300 - KS.BICAK_R1 + i * KS.BICAK_R1 / 3.0
        d.line([(fx(xx), fy(KS.Y_AGIZ_UST)), (fx(xx), fy(KS.Y_GOBEK))], fill=INK, width=1)
    d.line([(fx(X_K + 300 - KS.BICAK_R1), fy(KS.Y_AGIZ_UST)), (fx(X_K + 300 + KS.BICAK_R1), fy(KS.Y_AGIZ_UST))], fill=INK, width=2)
    txt(fx(X_K + 300), fy(1082.0), "BIÇAK", f7, INK, "mm"); txt(fx(X_K + 300), fy(1053.0), "Ø296 × 6", f7, INK, "mm")
    dline((fx(X_K + 300), fy(KS.Y_UC)), (fx(X_K + 300 - 143), fy(KS.BANT + 15.0)), RED, 1)
    dline((fx(X_K + 300), fy(KS.Y_UC)), (fx(X_K + 300 + 143), fy(KS.BANT + 15.0)), RED, 1)
    olcu_v(fx(X_K + 115), fy(KS.Y_AGIZ_UST), fy(KS.KESIM_ALT), "125", f7, INK, "l")
    # itici (bekleme: yukarıda, sağda) + eksen (arkada)
    iy0 = KS.Y_ITICI[0] + KS.ITICI_KALK; iy1 = KS.Y_ITICI[1] + KS.ITICI_KALK
    d.rectangle([fx(X_K + KS.YUZ_BEKLE - 16), fy(iy1), fx(X_K + KS.YUZ_BEKLE), fy(iy0)], fill=BG, outline=ACC, width=2)
    d.rectangle([fx(X_K + KS.YUZ_BEKLE - 134), fy(iy0 + 38.0), fx(X_K + KS.YUZ_BEKLE - 16), fy(iy0 + 18.0)], fill=BG, outline=ACC, width=1)
    txt(fx(X_K + KS.YUZ_BEKLE - 40), fy(iy1) - 14, "İTİCİ", f7, ACC, "mm")
    drect(fx(X_K + KS.EKSEN_X[0]), fy(KS.Y_EKSEN[1]), fx(X_K + KS.EKSEN_X[1]), fy(KS.Y_EKSEN[0]), ACC, 1)
    txt(fx(X_K + 300), (fy(KS.Y_EKSEN[0]) + fy(KS.H_B + 3.0)) / 2 - 1, "igus ZLW-1040 · arkada · strok 365", f7, ACC, "mm")   # denetçi: eksen kutusu ile taban sacı (895) arasında ortalı
    modul_etiketi(X_K, W_K, "MODÜL K · KESME", "600 × 909 × %s · taban %s · bant %s" % (sayi(H_MAK), sayi(KS.H_B), sayi(KS.BANT)))
    olcu_h(fx(X_K), fx(X_K + W_K), fy(H_MAK) - 26, sayi(W_K), f11, INK)


def ciz_E():
    """v18 · kutu_cad_v7 · E-yerel x 0..830 · kotlar mutlak · önde 6 tava panel + robot ağzı (ön paneller katmanı) · altında içecek yedeği"""
    a0, a1 = 917.0, 1162.0                                   # ön alt sac üstü (on_alt_sac) · ağız üst kirişi altı (v4 − 168)
    kabin(X_E, W_E, 0.0, H_MAK, "E · KUTU KATLAMA · standart 32 × 32 × 4,2 kutu")
    # içecek yedeği 6 koli (önde, sabit ön sacın arkasında) · 2 sütun × 3 kat
    for s_, (x0_, x1_) in enumerate(KC.ICECEK_X):
        for k_ in range(KC.ICECEK_KAT):
            y0_ = KC.ICECEK_Y0 + k_ * KC.KOLI["y"]
            d.rectangle([fx(X_E + x0_), fy(y0_ + KC.KOLI["y"]), fx(X_E + x1_), fy(y0_)], fill=KOLI_R)
            drect(fx(X_E + x0_), fy(y0_ + KC.KOLI["y"]), fx(X_E + x1_), fy(y0_), INK, 1)
    ym_ = KC.ICECEK_Y0 + 1.5 * KC.KOLI["y"]
    txt(fx(X_E + sum(KC.ICECEK_X[0]) / 2), fy(ym_), "İÇECEK YEDEĞİ", f7, INK, "mm")
    txt(fx(X_E + sum(KC.ICECEK_X[1]) / 2), fy(ym_), "6 koli · %d kutu" % KC.ICECEK_YEDEK["kutu"], f7, INK, "mm")
    # şarjör (arkada) · yazısı ağzın altındaki boş bölgede
    kesik(X_E, 8.0, 812.0, KC.Y_PLAT, KC.Y_YIGIN_UST, "", INK)
    satirlar(fx(X_E + 222.0), fy(780.0), "KUTU ŞARJÖRÜ · arkada|yığın %s = %d kutu (1,6)|≈ 432 kullanılır (asansör)|Tr16×4 + NEMA 23 · tahrik altta" % (sayi(KC.Y_YIGIN_UST - KC.Y_PLAT), KC.SARJOR_ADET), f8, INK, 17)
    kesik(X_E, 440.0, 800.0, 629.0, 980.0, "KAPAK MASASI + U FLAP", INK, "kapak kolu R166|SureGear 10:1")
    d.rectangle([fx(X_E + 4.0), fy(KC.ALT_RAF_Y[1]), fx(X_E + 800.0), fy(KC.ALT_RAF_Y[0])], fill=INK)
    txt(fx(X_E + 222.0), fy(KC.ALT_RAF_Y[0]) + 13, "ALT RAF %s–%s" % (sayi(KC.ALT_RAF_Y[0]), sayi(KC.ALT_RAF_Y[1])), f7, INK, "mm")
    agiz(X_E, 2.0, W_E - 2.0, a0, a1, "KUTULAMA AĞZI · robot çatalı tepsiden alır")
    d.rectangle([fx(X_E + 100), fy(TEPSI_E), fx(X_E + 420), fy(TEPSI_E - 18.0)], fill=EVC, outline=BUZ, width=2)
    d.rectangle([fx(X_E + 100), fy(TEPSI_E + 42.0), fx(X_E + 420), fy(TEPSI_E)], fill=URUN, outline=INK, width=2)
    txt(fx(X_E + 260), fy(TEPSI_E + 21.0), "kutu 320 × 42 · tepsi %s" % sayi(TEPSI_E), f7, INK, "mm")
    txt(fx(X_E + 18), fy(1042.0), "PİZZA", f7, RED, "lm"); txt(fx(X_E + 18), fy(1014.0), "sol duvar", f7, RED, "lm")
    drect(fx(X_E + 1), fy(KC.PENCERE[1]), fx(X_E + 12), fy(KC.PENCERE[0]), RED, 2)
    kapak(X_E, 2.0, W_E - 2.0, 1177.0, H_MAK - 2.0)
    kesik(X_E, 100.0, 828.0, 1304.0, 1372.0, "BESLEYİCİ İTİCİ · %s · strok 411" % sayi(KC.Y_BES_PL), INK)
    kesik(X_E, 112.0, 408.0, 1392.0, 1842.0, "PİSTON SFU1610", INK, "taban · kilit|kapak bastırma")   # denetçi: kutuya sığsın
    kesik(X_E, 450.0, 780.0, 1397.0, 1857.0, "PANO · arkada", INK, "S7-1200|7 step sürücü")
    modul_etiketi(X_E, W_E, "MODÜL E · KUTU KATLAMA", "830 × 909 × %s · tepsi %s · ağız %s–%s" % (sayi(H_MAK), sayi(TEPSI_E), sayi(a0), sayi(a1)))
    olcu_h(fx(X_E), fx(X_E + W_E), fy(H_MAK) - 26, sayi(W_E), f11, INK)
    return a0, a1, KC.Y_YIGIN_UST - KC.Y_PLAT


# ======================= PLAN · ORTAK =======================
def plan_ortak(P):
    txt(OX, PY_TOP - 110, "ÜST GÖRÜNÜŞ  ·  PLAN KESİTİ  ·  ray, robot, zincir oluğu, QR dolabı, tezgâh", f16, ACC)
    txt(fx(1200.0), py(-830) - 30, "ARKA", f9, GRAY, "mm")
    zb = -DZ
    for x0m, w, ad in ((X_A, W_A, "A · AÇICI (dolap üstünde)"), (X_C, W_C, "C · TOPPING (dolap üstünde)"), (X_F, W_F, "F · TP10 FIRIN · 79 öne (dolap üstünde)"), (X_K, W_K, "K · KESME"), (X_E, W_E, "E · KUTU")):
        d.rectangle([fx(x0m), py(zb), fx(x0m + w), py(ZON)], fill=FILL, outline=LINE, width=3)                 # v18: ön düzlem +79
        _xl = 2990.0 if x0m == X_F else x0m + w / 2                  # F yazısı erişim dairesinin içinde kalsın
        txt(fx(_xl), py(FT.ZS) + 26, "%s  ·  %s × %s" % (ad, sayi(w), sayi(DERIN)), f8, INK, "mm")
    # A
    d.rectangle([fx(X_A + 29), py(-788.0), fx(X_A + 669), py(12.0)], fill=BG, outline=INK, width=2)
    txt(fx(X_A + 350), py(-745.0), "KONİLİ AÇICI KAFASI · 2 koni + 2 motor", f8, INK, "mm")
    # dolap kolonları (kesik · altta)
    for kol in ("K1", "K2", "K3"):
        cx = SC.KOLON_X[kol]; w = SC.KOLON_W.get(kol, WO)
        drect(fx(cx + 16), py(-680.0), fx(cx + w - 16), py(ZON), DOLAP, 2)
        txt(fx(cx + w / 2), (py(-600.0) if kol == "K1" else py(-20.0) - 6), "%s · %s × 680 · altta (dolap)" % (kol, sayi(w)), f7, DOLAP, "mm")
    drect(fx(SC.K4X + 8), py(-788.0), fx(SC.K4X + SC.K4W - 8), py(ZON), DOLAP, 1)
    txt(fx(2188.0), py(-600.0), "K4 · Secop + depo", f7, DOLAP, "mm")
    # F (firin_tp10_cad_v8 · ön yüzü = ortak ön düzlem +79)
    zb0, zb1 = -FT.D_TP + FT.ZS, FT.ZS
    d.rectangle([fx(FT.X_F0), py(zb0), fx(FT.X_F1), py(zb1)], fill=SOFT, outline=INK, width=2)
    d.rectangle([fx(FT.X_TUN0), py(FT.TUNEL_Z_D[0]), fx(FT.X_TUN1), py(FT.TUNEL_Z_D[1])], fill=SICAK, outline=TURUNCU, width=2)
    tarali(fx(FT.X_DUV0), py(FT.TUNEL_Z_D[0]), fx(FT.X_TUN0), py(zb1 - 2), (226, 214, 190), 11)
    tarali(fx(FT.X_TUN1), py(FT.TUNEL_Z_D[0]), fx(FT.X_F1 - 2), py(zb1 - 2), (226, 214, 190), 11)
    drect(fx(FT.BANT_X[0]), py(FT.BANT_Z_D[0]), fx(FT.BANT_X[1]), py(FT.BANT_Z_D[1]), BUZ, 1)
    xm = (FT.X_TUN0 + FT.X_TUN1) / 2.0
    for i in range(FT.N_URUN):
        xx = xm + (i - (FT.N_URUN - 1) / 2.0) * FT.ADIM
        d.ellipse([fx(xx - 150), py(ZT - 150.0), fx(xx + 150), py(ZT + 150.0)], fill=URUN, outline=(180, 140, 70), width=1)
        txt(fx(xx), py(ZT), "Ø300", f7, (140, 100, 40), "mm")
    txt(fx(xm), py(-560.0), "TEKNİK BÖLME ≈239 (arkada) · sürücü · SSR · bant motoru · gergi · ekran arka yüzde", f7, GRAY, "mm")
    olcu_h(fx(FT.X_TUN0), fx(FT.X_TUN1), py(-830) - 70, "ısıtılan %s" % sayi(FT.ODA), f8, TURUNCU)
    # fırın altı (plan kesitinde görünmez): dolap K5 + K6 + şerit (robot çöpü) · yalnız yazı
    txt(fx(3150.0), py(-752.0), "altında dolap: K5 620 · K6 585 · şerit 190 (robot çöpü)", f7, DOLAP, "mm")
    # K (kesme_cad_v6)
    d.rectangle([fx(X_K + KS.X_KUYRUK), py(KS.BANT_Z[0]), fx(X_K + KS.X_TAHRIK), py(KS.BANT_Z[1])], fill=EVC, outline=BUZ, width=2)
    txt(fx(X_K + 340), py(-560.0), "K BANDI 400 · bıçak Ø296", f7, BUZ, "mm")
    d.ellipse([fx(X_K + 300 - KS.BICAK_R1), py(ZT - KS.BICAK_R1), fx(X_K + 300 + KS.BICAK_R1), py(ZT + KS.BICAK_R1)], outline=INK, width=2)
    for k in range(3):
        a = math.radians(60.0 * k)
        d.line([(fx(X_K + 300) - KS.BICAK_R1 * S * math.cos(a), py(ZT) - KS.BICAK_R1 * S * math.sin(a)), (fx(X_K + 300) + KS.BICAK_R1 * S * math.cos(a), py(ZT) + KS.BICAK_R1 * S * math.sin(a))], fill=INK, width=1)
    _zc = lambda x: KS.CIT_P0[1] - math.tan(math.radians(KS.CIT_ACI)) * (x - KS.CIT_P0[0])
    d.line([(fx(X_K + 330.0), py(_zc(330.0))), (fx(X_K + KS.CIT_X_DONUS), py(KS.CIT_Z_DUZ)), (fx(X_K + 597.0), py(KS.CIT_Z_DUZ))], fill=RED, width=3)
    txt(fx(X_K + 470.0), py(0.0) + 16, "ÇİT 20°", f7, RED, "mm")
    drect(fx(X_K + KS.EKSEN_X[0]), py(KS.Z_EKSEN[0]), fx(X_K + KS.EKSEN_X[1]), py(KS.Z_EKSEN[1]), ACC, 1)
    txt(fx(X_K + 330), py(-505.0), "itici ekseni ZLW-1040", f7, ACC, "mm")
    d.rectangle([fx(X_K + KS.YUZ_BAS - 16), py(KS.ITICI_Z[0]), fx(X_K + KS.YUZ_BAS), py(KS.ITICI_Z[1])], fill=BG, outline=ACC, width=2)
    d.line([(fx(X_K + 300), py(ZT)), (fx(X_K + 500), py(-206.0)), (fx(X_E + 260), py(-206.0))], fill=INK, width=2)
    d.polygon([(fx(X_E + 260), py(-206.0)), (fx(X_E + 240), py(-206.0) - 7), (fx(X_E + 240), py(-206.0) + 7)], fill=INK)
    txt(fx(X_K + 600), py(FT.ZS) + 60, "K: bant ürünü 300 → 500 taşır, çit 36 mm içeri kaydırır · itici 500 → 860 (E'ye 110 mm girer)", f7, RED, "mm")
    # K altı: bulaşık (kesik) · v18: deterjan / parlatıcı yok (tezgâhta)
    ZB = KS.BULASIK_ZARF
    drect(fx(X_K + ZB["x"][0]), py(ZB["z"][0]), fx(X_K + ZB["x"][1]), py(ZB["z"][1]), BUZ, 1)
    txt(fx(X_K + (ZB["x"][0] + ZB["x"][1]) / 2), py(ZB["z"][0] + 22.0), "BULAŞIK (altta, tablada)", f7, BUZ, "mm")
    # E (kutu_cad_v7)
    drect(fx(X_E + 8), py(-819.0), fx(X_E + 812), py(-415.0), GRAY, 1)
    txt(fx(X_E + 410), py(-617.0), "ŞARJÖR · açılım 804 × 404 · %d kutu · y %s–%s" % (KC.SARJOR_ADET, sayi(KC.Y_PLAT), sayi(KC.Y_YIGIN_UST)), f7, GRAY, "mm")
    d.rectangle([fx(X_E + 100), py(-366.0), fx(X_E + 420), py(-46.0)], fill=BG, outline=INK, width=2)
    txt(fx(X_E + 260), py(-219.0), "KUTU", f8, INK, "mm")
    txt(fx(X_E + 260), py(-192.0), "320 × 320 × 42", f7, GRAY, "mm")
    drect(fx(X_E + 440), py(-368.0), fx(X_E + 800), py(-26.0), GRAY, 1)
    txt(fx(X_E + 620), py(-197.0), "kapak masası", f7, GRAY, "mm")
    d.line([(fx(X_E + 1), py(-372.0)), (fx(X_E + 1), py(-24.0))], fill=RED, width=4)
    iz = KC.ICECEK_YEDEK
    drect(fx(X_E + iz["x"][0]), py(iz["z"][0]), fx(X_E + iz["x"][1]), py(iz["z"][1]), TURUNCU, 1)
    txt(fx(X_E + 410), py(iz["z"][0] - 42.0), "içecek yedeği 6 koli (altta)", f7, TURUNCU, "mm")
    # ---- koridor + ray + zincir oluğu + robot + zemin kanalı + ince duvar + QR + tezgâh
    olcu_v(fx(0) - 44, py(-830), py(ZON), sayi(DERIN), f11, INK, "l")                 # v18: derinlik 909 (arka −830 sabit)
    olcu_v(fx(0) - 44, py(KOR[0]), py(KOR[1]), "koridor %s" % sayi(KOR[1] - KOR[0]), f8, GRAY, "l")
    olcu_v(fx(0) - 44, py(INCE[1]), py(ON_DUVAR), "ön zon %s" % sayi(ON_DUVAR - INCE[1]), f8, GRAY, "l")
    rz0, rz1 = RE.RAY_Z
    d.rectangle([fx(RE.RAY_X[0]), py(rz0), fx(RE.RAY_X[1]), py(rz1)], fill=SOFT, outline=LINE, width=1)
    d.line([(fx(RE.RAY_X[0]), py(RZ)), (fx(RE.RAY_X[1]), py(RZ))], fill=ACC, width=2)
    txt(fx(1150.0), py(rz0 + 40.0), "YER RAYI · x %s–%s · ekseni hat yüzünden %s · robot merkezi %s–%s" % (sayi(RE.RAY_X[0]), sayi(RE.RAY_X[1]), sayi(RZ), sayi(RE.ROBOT_X[0]), sayi(RE.ROBOT_X[1])), f7, ACC, "mm")
    ol = RE.OLUK
    d.rectangle([fx(ol["x"][0]), py(ol["z"][0]), fx(ol["x"][1]), py(ol["z"][1])], fill=(238, 238, 242), outline=GRAY, width=1)
    txt(fx(760.0), py(sum(ol["z"]) / 2), "ZİNCİR OLUĞU · x %s–%s · z %s–%s · zeminde" % (sayi(ol["x"][0]), sayi(ol["x"][1]), sayi(ol["z"][0]), sayi(ol["z"][1])), f7, GRAY, "mm")
    zx0 = RE.donus_x(RX) - RE.Z_H["R"]; zw = RE.Z_H["bA"] / 2.0
    d.rectangle([fx(zx0), py(RE.ZC - zw), fx(RE.XF), py(RE.ZC + zw)], fill=ZINCIR_R, outline=INK, width=1)
    txt(fx(1500.0), py(ol["z"][1] + 40.0), "ENERJİ ZİNCİRİ · sabit ucu x %s · robot x %s'de" % (sayi(RE.XF), sayi(RX)), f7, INK, "mm")
    for rx, ad, alt in ((RX, "R · FR5 · TEK ROBOT · rayda", "hamur: çekmece → tabla · kutu → QR · içecek + tatlı · fire → çöp"),):
        cxp, cyp = fx(rx), py(RZ)
        d.rectangle([fx(rx - 200), py(rz0), fx(rx + 200), py(rz1)], fill=BG, outline=ACC, width=2)
        d.ellipse([cxp - 75 * S, cyp - 75 * S, cxp + 75 * S, cyp + 75 * S], fill=BG, outline=ACC, width=3)
        darc(cxp, cyp, ERISIM * S, 0.0, 360.0, ACC, 2, 3.0)
        txt(cxp, py(ol["z"][1] + 115.0), ad, f8, ACC, "mm")
        txt(cxp, py(ol["z"][1] + 150.0), alt, f7, GRAY, "mm")
    txt(fx(20.0), py(KOR[1] - 95.0), "kesik daire: FR5 pratik bilek erişimi %s (820 × 0,95)" % sayi(ERISIM), f7, ACC, "lm")
    txt(fx(HAT / 2), py(KOR[1] - 50.0), "ÖN · robot koridoru", f9, GRAY, "mm")
    # zemin kanalı: kapaklı kısım koridorda (z 575–670) · oluğun ve QR'ın altında kesik
    kn = RE.KANAL
    d.rectangle([fx(kn["x"][0]), py(kn["kapak_z"][0]), fx(kn["x"][1]), py(kn["kapak_z"][1])], fill=SOFT, outline=LINE, width=2)
    drect(fx(kn["x"][0]), py(kn["z"][0]), fx(kn["x"][1]), py(kn["z"][1]), LINE, 1)
    txt(fx(kn["x"][1] + 14.0), py(sum(kn["kapak_z"]) / 2), "ZEMİN KANALI %s · kapaklı · z %s–%s" % (sayi(kn["x"][1] - kn["x"][0]), sayi(kn["z"][0]), sayi(kn["z"][1])), f7, INK, "lm")
    # ince duvar + ön duvar
    d.rectangle([fx(0.0), py(INCE[0]), fx(QRX[0]), py(INCE[1])], fill=SOFT, outline=LINE, width=1)
    tarali(fx(0.0), py(INCE[0]), fx(QRX[0]), py(INCE[1]), (200, 200, 206), 10)
    txt(fx(20.0), py(INCE[1]) + 16, "İNCE DUVAR %s" % sayi(INCE[1] - INCE[0]), f7, GRAY, "lm")
    d.line([(fx(-60), py(ON_DUVAR)), (fx(HAT + 60), py(ON_DUVAR))], fill=LINE, width=3)
    txt(fx(20.0), py(ON_DUVAR) + 18, "ÖN DUVAR (dükkân v13)", f7, GRAY, "lm")
    # QR dolabı (koridorun karşısında)
    d.rectangle([fx(QRX[0]), py(QRZ[0]), fx(QRX[1]), py(QRZ[1])], fill=FILL, outline=LINE, width=3)
    for gx in QR.GOZ_X:
        d.rectangle([fx(QRX[0] + gx), py(QRZ[0] + QR.GOZ_Z[0]), fx(QRX[0] + gx + QR.GOZ_W), py(QRZ[0] + QR.GOZ_Z[1])], fill=EVC, outline=BUZ, width=1)
    drect(fx(kn["x"][0]), py(QRZ[0]), fx(kn["x"][1]), py(kn["z"][1]), LINE, 1)
    olcu_h(fx(QRX[0]), fx(QRX[1]), py(QRZ[1]) + 34, sayi(QR.W), f8, GRAY)
    txt(fx((QRX[0] + QRX[1]) / 2), py(QRZ[1]) + 70, "QR DOLABI · 2 × 6 göz · göz %s × %s × %s" % (sayi(QR.GOZ_W), sayi(QR.GOZ_H), sayi(QR.GOZ_D)), f8, INK, "mm")
    txt(fx((QRX[0] + QRX[1]) / 2), py(QRZ[1]) + 92, "robot yüzü z %s · müşteri yüzü z %s" % (sayi(QRZ[0]), sayi(QRZ[1])), f7, GRAY, "mm")
    # tezgâh (ön zon, ön duvara yaslı)
    t0, t1, u0, u1 = TZ.X0, TZ.X0 + TZ.W, TZ.Z0, TZ.Z0 + TZ.D
    d.rectangle([fx(t0), py(u0), fx(t1), py(u1)], fill=FILL, outline=LINE, width=2)
    txt(fx((t0 + t1) / 2), py((u0 + u1) / 2) - 10, "TEZGÂH", f8, INK, "mm")
    txt(fx((t0 + t1) / 2), py((u0 + u1) / 2) + 12, "%s × %s × %s" % (sayi(TZ.W), sayi(TZ.D), sayi(TZ.H)), f7, GRAY, "mm")
    olcu_h(fx(0), fx(HAT), py(ON_DUVAR) + 60, "HAT  %s" % sayi(HAT), f13, INK)


# ======================= KESITLER =======================
def sec(sx):
    return lambda v: sx + (v + 830.0) * S


def govde(z, h0, h1, plint=False):
    d.rectangle([z(-830), fy(h1), z(ZON), fy(max(h0, Y_ALT) if plint else h0)], fill=FILL, outline=LINE, width=4)   # v18: ön düzlem +79
    if plint:                                                        # süpürgelik 60 geride, gövde 123'ten
        d.rectangle([z(-800), fy(Y_ALT), z(-60), fy(0)], fill=SOFT, outline=LINE, width=2)


def robot_kesit(z, wz, wy, tz, ty, ad):
    """ray + zincir oluğu + araba + FR5 (omuz 970) · bilek (wz,wy) · uc (tz,ty)"""
    d.rectangle([z(RE.RAY_Z[0]), fy(60), z(RE.RAY_Z[1]), fy(0)], fill=SOFT, outline=LINE, width=2)
    d.rectangle([z(RE.OLUK["z"][0]), fy(RE.OLUK["y"][1]), z(RE.OLUK["z"][1]), fy(0)], fill=(238, 238, 242), outline=GRAY, width=1)
    d.rectangle([z(RZ - 110), fy(OMUZ - 120.0), z(RZ + 110), fy(60)], fill=BG, outline=ACC, width=2)
    txt(z(RZ), fy(420.0), "KAİDE", f7, ACC, "mm")
    dz, dy = wz - RZ, wy - OMUZ
    D = math.hypot(dz, dy)
    Dk = min(D, A2 + A3 - 1.0)
    th = math.atan2(dy, dz)
    al = math.acos(max(-1.0, min(1.0, (A2 * A2 + Dk * Dk - A3 * A3) / (2 * A2 * Dk))))
    cand = [(RZ + A2 * math.cos(th + s * al), OMUZ + A2 * math.sin(th + s * al)) for s in (1.0, -1.0)]
    ez, ey = max(cand, key=lambda p: p[1])                     # dirsek yukari
    d.line([(z(RZ), fy(OMUZ)), (z(ez), fy(ey))], fill=ACC, width=9)
    d.line([(z(ez), fy(ey)), (z(wz), fy(wy))], fill=ACC, width=7)
    d.line([(z(wz), fy(wy)), (z(tz), fy(ty))], fill=INK, width=5)
    for pz, pyy, r in ((RZ, OMUZ, 11), (ez, ey, 9), (wz, wy, 8)):
        d.ellipse([z(pz) - r, fy(pyy) - r, z(pz) + r, fy(pyy) + r], fill=BG, outline=ACC, width=3)
    txt(z(RZ) + 16, fy(OMUZ) + 22, "omuz %s" % sayi(OMUZ), f7, ACC, "la")
    txt(z(ez) - 16, fy(ey) - 22, "%s · bilek mesafesi %d / %d" % (ad, round(D), round(ERISIM)), f7, ACC, "lm")
    d.line([(z(0), fy(0)), (z(1390), fy(0))], fill=INK, width=3)
    olcu_h(z(ZON), z(RZ), fy(0) + 44, sayi(RZ - ZON), f8, ACC)                             # v18: ray ekseni ön düzlemden 281
    olcu_h(z(-830), z(ZON), fy(0) + 44, sayi(DERIN), f11, INK)
    return D


def cekmeceler(z, cek, y0):
    for _k, kod, tip, _x0, _yo in cek:
        h = HH[tip] + 2 * BIND
        d.rectangle([z(-720.0), fy(y0 + h), z(-40.0), fy(y0)], fill=BG, outline=DOLAP, width=1)
        d.rectangle([z(Z_SOG), fy(y0 + h), z(ZON), fy(y0)], fill=BG, outline=DOLAP, width=1)   # v18: çekmece önü +39…+79
        d.line([(z(-38.0), fy(y0 + 6.0)), (z(-38.0), fy(y0 + h - 6.0))], fill=RED, width=2)
        d.rectangle([z(-800.0), fy(y0 + h / 2 + 10.0), z(-730.0), fy(y0 + h / 2 - 10.0)], fill=(255, 230, 230), outline=RED, width=1)
        y0 += h + FUGA
    return y0


def kesit_E(P, a0, a1):
    z = sec(SX2)
    txt(SX2, FY_TOP - 200, "KESİT 2 · E + ROBOT + QR DOLABI", f16, ACC)
    txt(SX2, FY_TOP - 162, "Robot kapalı kutuyu tepsinin çubukları arasından çatalla alır, QR gözüne koyar · E: kutu_cad_v7 · QR: qr_cad_v1", f9, GRAY)
    govde(z, 0.0, H_MAK, True)
    d.rectangle([z(-819.0), fy(KC.Y_YIGIN_UST), z(-415.0), fy(KC.Y_PLAT)], fill=BG, outline=GRAY, width=1)
    satirlar(z(-617.0), fy(610.0), "KUTU ŞARJÖRÜ|%d kutu · y %s–%s|asansör Tr16 + NEMA 23" % (KC.SARJOR_ADET, sayi(KC.Y_PLAT), sayi(KC.Y_YIGIN_UST)), f7, GRAY, 16)
    drect(z(-430.0), fy(Y_ALT), z(-354.0), fy(100.0), ACC, 1)
    txt(z(-392.0), fy(80.0), "tahrik · tabanın altında", f7, ACC, "mm")
    # içecek yedeği (önde, altta) + alt raf
    iz = KC.ICECEK_YEDEK
    d.rectangle([z(iz["z"][0]), fy(iz["y"][1]), z(iz["z"][1]), fy(iz["y"][0])], fill=KOLI_R, outline=LINE, width=1)
    for k_ in range(1, KC.ICECEK_KAT):
        yy = KC.ICECEK_Y0 + k_ * KC.KOLI["y"]
        d.line([(z(iz["z"][0]), fy(yy)), (z(iz["z"][1]), fy(yy))], fill=LINE, width=1)
    satirlar(z(sum(iz["z"]) / 2), fy(KC.ICECEK_Y0 + 1.5 * KC.KOLI["y"]), "İÇECEK YEDEĞİ|6 koli · %d kutu" % iz["kutu"], f7, INK, 16)
    d.rectangle([z(-372.0), fy(KC.ALT_RAF_Y[1]), z(-24.0), fy(KC.ALT_RAF_Y[0])], fill=INK)
    txt(z(-198.0), fy(KC.ALT_RAF_Y[1]) - 12, "alt raf %s" % sayi(KC.ALT_RAF_Y[1]), f7, INK, "mm")
    d.line([(z(-819.0), fy(KC.Y_BES_PL)), (z(-408.0), fy(KC.Y_BES_PL))], fill=INK, width=3)
    d.polygon([(z(-408.0), fy(KC.Y_BES_PL)), (z(-428.0), fy(KC.Y_BES_PL) - 7), (z(-428.0), fy(KC.Y_BES_PL) + 7)], fill=INK)
    txt(z(-614.0), fy(KC.Y_BES_PL) - 16, "besleyici %s · strok 411" % sayi(KC.Y_BES_PL), f7, INK, "mm")
    d.rectangle([z(-374.0), fy(982.0), z(-32.0), fy(972.0)], fill=SOFT, outline=INK, width=1)
    d.rectangle([z(-366.0), fy(TEPSI_E), z(-46.0), fy(TEPSI_E - 18.0)], fill=EVC, outline=BUZ, width=2)
    d.rectangle([z(-366.0), fy(TEPSI_E + 42.0), z(-46.0), fy(TEPSI_E)], fill=URUN, outline=INK, width=2)
    txt(z(-206.0), fy(TEPSI_E + 21.0), "kutu 320 × 42", f7, INK, "mm")
    d.rectangle([z(-50.0), fy(a1), z(0.0), fy(a0)], fill=AGZ, outline=RED, width=2)
    txt(z(-30.0), fy(a1) - 14, "KUTULAMA AĞZI %s–%s" % (sayi(a0), sayi(a1)), f7, RED, "rm")
    drect(z(-394.0), fy(1842.0), z(-58.0), fy(1392.0), GRAY, 1)
    txt(z(-226.0), fy(1617.0), "PİSTON SFU1610", f7, GRAY, "mm")
    drect(z(-826.0), fy(1857.0), z(-740.0), fy(1397.0), GRAY, 1)
    txt(z(-783.0), fy(1877.0), "pano", f7, GRAY, "mm")
    ty = TEPSI_E - 9.0
    D = robot_kesit(z, 230.0, ty + 20.0, -206.0, ty, "ROBOT")
    d.line([(z(-366.0), fy(ty)), (z(-46.0), fy(ty))], fill=ACC, width=4)
    txt(z(-60.0), fy(ty) + 16, "çatal · kutu ekseni z −206", f7, ACC, "rm")
    # QR dolabı 860 × 520 × 2050 (qr_cad_v1) · robot yüzü z 670
    q0, q1 = QRZ
    d.rectangle([z(q0), fy(QR_H), z(q1), fy(0.0)], fill=FILL, outline=LINE, width=4)
    d.line([(z(q0), fy(QR.TABAN[1])), (z(q1), fy(QR.TABAN[1]))], fill=LINE, width=2)
    for r0, r1 in (QR.ALT_RAF, QR.UST_RAF):
        d.rectangle([z(q0), fy(r1), z(q1), fy(r0)], fill=INK)
    for yy in QR_SATIR:
        d.rectangle([z(q0 + QR.GOZ_Z[0]), fy(yy + QR.GOZ_H), z(q0 + QR.GOZ_Z[1]), fy(yy)], fill=EVC, outline=BUZ, width=1)
        txt(z(q0 + sum(QR.GOZ_Z) / 2), fy(yy + QR.GOZ_H / 2), "göz %s × %s · y %s" % (sayi(QR.GOZ_W), sayi(QR.GOZ_H), sayi(yy)), f7, BUZ, "mm")
    kk = QR.KONTROL
    d.rectangle([z(q0 + kk["z"][0]), fy(kk["y"][1]), z(q0 + kk["z"][1]), fy(kk["y"][0])], fill=BG, outline=ACC, width=2)
    satirlar(z(q0 + sum(kk["z"]) / 2), fy(sum(kk["y"]) / 2), "ROBOT KONTROL|%s × %s × %s" % (sayi(kk["x"][1] - kk["x"][0]), sayi(kk["y"][1] - kk["y"][0]), sayi(kk["z"][1] - kk["z"][0])), f7, ACC, 16)
    satirlar(z((q0 + kk["z"][1] + q1) / 2), fy(sum(kk["y"]) / 2), "yanda:|kablo|kangalı", f7, GRAY, 16)
    ap = QR.ANA_PANO
    d.rectangle([z(q0 + ap["z"][0]), fy(ap["y"][1]), z(q0 + ap["z"][1]), fy(ap["y"][0])], fill=BG, outline=INK, width=2)
    satirlar(z(q0 + sum(ap["z"]) / 2), fy(sum(ap["y"]) / 2), "ANA PANO|%s × %s × %s" % (sayi(ap["x"][1] - ap["x"][0]), sayi(ap["y"][1] - ap["y"][0]), sayi(ap["z"][1] - ap["z"][0])), f7, INK, 16)
    satirlar(z((q0 + ap["z"][1] + q1) / 2), fy(sum(ap["y"]) / 2), "yanda:|UPS BX500CI|kilit kartı|modem", f7, GRAY, 16)
    txt(z((q0 + q1) / 2), fy(QR_H) - 16, "QR DOLABI · %s × %s × %s" % (sayi(QR.W), sayi(QR.D), sayi(QR.H)), f8, INK, "mm")
    for yy in (QR.TABAN[1], QR_SATIR[0], QR.UST_RAF[0], QR_H):
        d.line([(z(q1) + 6, fy(yy)), (z(q1) + 24, fy(yy))], fill=INK, width=2)
        txt(z(q1) + 30, fy(yy), sayi(yy), f7, INK, "lm")
    olcu_h(z(ZON), z(q0), fy(0) + 84, "QR yüzü %s" % sayi(q0 - ZON), f8, GRAY)
    olcu_h(z(q0), z(q1), fy(0) + 84, sayi(q1 - q0), f8, GRAY)
    for yy in (Y_ALT, KC.Y_PLAT, KC.ALT_RAF_Y[1], TEPSI_E, KC.Y_YIGIN_UST, a1, KC.Y_BES_PL, H_MAK):
        d.line([(z(-830) - 24, fy(yy)), (z(-830) - 6, fy(yy))], fill=INK, width=2)
        txt(z(-830) - 30, fy(yy), sayi(yy), f7, INK, "rm")
    return D


def sar(s, f, w):
    """yazıyı w genişliğine sar (kelime kelime)"""
    if not s:
        return [""]
    out, cur = [], ""
    for k in s.split(" "):
        t = (cur + " " + k) if cur else k
        if d.textlength(t, font=f) <= w or not cur:
            cur = t
        else:
            out.append(cur); cur = k
    out.append(cur)
    return out


def parca_listesi(satirlar_):
    """v17: hücre yazısı sütuna sarılır (v16'da taşıyordu) · satır 34 + 18 × (ek satır)"""
    x0, y0 = SX1, PY_TOP - 60.0
    txt(x0, y0 - 46, "MODÜLLER (lego · cıvatalı flanşla birleşir)  ·  PARÇA LİSTESİ", f16, ACC)
    kol = (0, 250, 1560, 1660)
    gen = 2790
    gw = (230, 1290, 80, 1110)
    d.rectangle([x0, y0, x0 + gen, y0 + 30], fill=SOFT, outline=LINE, width=1)
    for k, b in zip(kol, ("İSTASYON", "PARÇA", "ADET", "NOT")):
        txt(x0 + k + 10, y0 + 15, b, f7, INK, "lm")
    y = y0 + 30
    for r in satirlar_:
        hucre = [sar(v, f7, w) for v, w in zip(r, gw)]
        n = max(len(h) for h in hucre)
        hh = 34 + 18 * (n - 1)
        for k, h in zip(kol, hucre):
            for i, l in enumerate(h):
                txt(x0 + k + 10, y + 17 + 18 * i, l, f7, INK if k < 1560 else GRAY, "lm")
        d.line([(x0, y + hh), (x0 + gen, y + hh)], fill=(225, 225, 230), width=1)
        y += hh
    d.rectangle([x0, y0, x0 + gen, y], outline=LINE, width=1)
    return y


def lejant():
    y = H_PX - 110
    d.line([(OX, y - 40), (W_PX - 170, y - 40)], fill=LINE, width=2)
    x = OX
    for fill, out, ad, kes in ((BG, LINE, "kapak / panel", False), (AGZ, RED, "açık ağız · robot girer", False), (BG, DOLAP, "çekmece +3 °C", False),
                               (SICAK, TURUNCU, "pişirme haznesi / sıcak hava", False), (PUC, GRAY, "PU · taşyünü yalıtım", False), (EVC, BUZ, "bant · tabla · plaka", False),
                               (BG, INK, "kapak arkası parça", True), (BG, ACC, "robot · ray", False)):
        if kes:
            drect(x, y - 12, x + 30, y + 12, out, 1)
        else:
            d.rectangle([x, y - 12, x + 30, y + 12], fill=fill, outline=out, width=2)
        txt(x + 42, y, ad, f8, INK, "lm")
        x += 70 + d.textlength(ad, font=f8) + 40


def kot_cizgileri(kotlar):
    """kot: sayı ya da (sayı, yazı)"""
    olcu_v(fx(0) - 52, fy(H_MAK), fy(0), sayi(H_MAK), f11, INK, "l")
    for k in kotlar:
        yy, s_ = (k if isinstance(k, tuple) else (k, sayi(k)))
        d.line([(fx(HAT) + 8, fy(yy)), (fx(HAT) + 26, fy(yy))], fill=INK, width=2)
        txt(fx(HAT) + 32, fy(yy), s_, f7, INK, "lm")


def birlesimler():
    for xj, et, yb in ((X_C, "A | C", H_B), (X_F, "C | F", H_B), (X_K, "B·F | K", 0.0), (X_E, "K | E", 0.0)):
        dline((fx(xj), fy(H_MAK) - 12), (fx(xj), fy(yb) + 12), ACC, 3, 10, 6)
        txt(fx(xj), fy(H_MAK) - 122, "BİRLEŞİM", f7, ACC, "mm")
        txt(fx(xj), fy(H_MAK) - 106, et, f7, GRAY, "mm")
    for rx, ad in ((RX, "R · FR5 · TEK ROBOT"),):
        d.polygon([(fx(rx), fy(0) + 4), (fx(rx) - 14, fy(0) + 30), (fx(rx) + 14, fy(0) + 30)], fill=ACC)
        txt(fx(rx), fy(0) + 68, ad + " · koridorda, rayda · z +%s" % sayi(RZ), f8, ACC, "mm")
    olcu_h(fx(0), fx(HAT), fy(0) + 98, "HAT  %s" % sayi(HAT), f13, INK)
    txt(fx(0) - 12, fy(0) + 149, "ÜST", f8, ACC, "rm")
    txt(fx(0) - 12, fy(0) + 199, "ALT", f8, ACC, "rm")


def baslik(ad, alt):
    txt(OX, 70, ad, f38, INK)
    txt(OX, 140, alt, f13, GRAY)
    d.line([(OX, 182), (W_PX - 170, 182)], fill=LINE, width=3)
    txt(OX, FY_TOP - 200, "ÖN GÖRÜNÜŞ", f16, ACC)
    txt(OX, FY_TOP - 162, "kesik çizgi = kapak arkası parça · robot koridorda önde, konumu zeminde işaretli", f9, GRAY)
    for s_, f_ in ((ad, f38), (alt, f13)):
        if d.textlength(s_, font=f_) > W_PX - 170 - OX:
            TASMA.append(("baslik", s_[:60]))


# =====================================================================
#                          ATOSA TABLALI HAT v17 · ALÇAK HAT
# =====================================================================

def on_paneller():
    """v18 · ön görünüşe GERÇEK ön paneller: montaj (hat_v64) parca_kutulari.json'daki dış yüzü +79'da olan panel / kapak kutuları
    yarı saydam dolgu + çevre çizgisi (derzler görünür) · fırın gövdesi · robot ağızları"""
    import json as _js
    _pk = _js.load(open(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "otonom", "hat3d", "parca_kutulari.json"), encoding="utf-8"))
    kutu = []
    for kod, lst in _pk["parca"].items():
        if kod.startswith(("QR", "TEZGAH", "ROBOT", "ZEMIN", "INSAN", "RAY")):
            continue
        for r in lst:
            ad, _s, x0, x1, y0, y1, z0, z1 = r
            if z1 >= ZON - 0.6 and z0 >= Z_SOG - 1.5 and (x1 - x0) >= 80.0 and (y1 - y0) >= 60.0:
                kutu.append((x0, x1, y0, y1))
    kutu.append((FT.X_F0, FT.X_F1, FT.YG0, FT.YG1))                                  # fırın gövdesinin ön yüzü (ortak düzlem)
    kutu = sorted(set((round(a, 1), round(b, 1), round(c, 1), round(e, 1)) for a, b, c, e in kutu))
    from PIL import Image as _Im, ImageDraw as _ID
    ov = _Im.new("RGBA", im.size, (0, 0, 0, 0)); od = _ID.Draw(ov)
    for x0, x1, y0, y1 in kutu:
        od.rectangle([fx(x0) * K_HD, fy(y1) * K_HD, fx(x1) * K_HD, fy(y0) * K_HD], fill=(247, 248, 250, 105), outline=(40, 44, 52, 255), width=max(1, int(1.6 * K_HD)))
    for (ax0, ax1, ay0, ay1) in ((250.0, 450.0, 960.0, 1160.0), (4685.0, 5040.0, 886.0, 1062.0)):   # A ve E robot ağızları (SPEC §2.2 / §2.6)
        od.rectangle([fx(ax0) * K_HD, fy(ay1) * K_HD, fx(ax1) * K_HD, fy(ay0) * K_HD], fill=(255, 255, 255, 0), outline=(200, 40, 30, 255), width=max(1, int(2.2 * K_HD)))
    im.paste(_Im.alpha_composite(im.convert("RGBA"), ov).convert("RGB"))
    for (ax0, ax1, ay0, ay1) in ((250.0, 450.0, 960.0, 1160.0), (4685.0, 5040.0, 886.0, 1062.0)):
        txt(fx((ax0 + ax1) / 2.0), fy(ay1) - 14, "ROBOT AĞZI", f7, RED, "mm")
    return len(kutu)


def tablali():
    global im, d
    im = Image.new("RGB", (int(W_PX * K_HD), int(H_PX * K_HD)), BG); d = HDraw(im)
    P = P_SUREC                                              # çalışma diski üstü 1000 = süreç kotu (mekanizma tabanı 892 + 108)
    baslik("AUTOKITCH  ·  ATOSA TABLALI HAT  ·  TEKNİK RESİM  v20  ·  BANTLI TABLA  ·  ÖN DÜZLEM +79  ·  derinlik 909 (arka −830 sabit)  ·  montaj v71  ·  her istasyon kapaklı temiz kutu",
           "ön · üst · yan görünüş  ·  günde 80 pide + 200 lahmacun (+ pizza)  ·  gövdeler yerden 123 · DÜZ ÇİZGİ 788 = çekmeceli dolap üstü = A, C, fırın altı · mekanizma tabanı 892 · kaset bandı 1000  ·  QR dolabı + tezgâh koridorun karşısında  ·  TEK FR5 yer rayında  ·  SPEC v57  ·  ölçüler mm  ·  27 Eylül 2026")
    # ---- A · AÇICI (içi v16 ile aynı, 168 aşağı · kaide 788–892)
    kabin(X_A, W_A, H_B, H_MAK, "A · KONİLİ DÖNER AÇICI · tabla altında bekler")
    kapak(X_A, 33.0, 667.0, H_MEK + 3.0, H_MAK - 20.0)
    kaide(KD.A_X[0], KD.A_X[1])
    agiz(X_A, 53.0, 647.0, P, P + 220.0, "HAMUR AĞZI · robot TOP halinde bırakır")
    _kx = X_A + 350.0
    for _y in (1.0, -1.0):
        d.polygon([(fx(_kx), fy(P + 8.0)), (fx(_kx + _y * 140.0), fy(P + 8.0)), (fx(_kx + _y * 140.0), fy(P + 96.0))], outline=INK)
    kesik(X_A, 270.0, 430.0, 1142.0, 1154.0, "", INK)
    drect(fx(X_A + 290.0), fy(1272.0), fx(X_A + 410.0), fy(H_MEK), INK, 1)
    satirlar(fx(X_A + 350.0), fy(1532.0), "AÇICI · kolon x 290–410 · 892–1272|kafa plakası 160 × 680 × 12 · kot 1142|Z kızağı strok 60 · Ø32 pnömatik|2 KONİ · boy 140 · taban Ø90 · yarım açı 17,82°|2 × NEMA23 + planet · ters yönde döner", f7, INK, 17)
    modul_etiketi(X_A, W_A, "MODÜL A · AÇICI + KABİN", "700 × 909 × %s · kaide %s" % (sayi(H_MAK - H_B), sayi(KD.KAIDE_H)))
    olcu_h(fx(X_A), fx(X_A + W_A), fy(H_MAK) - 26, sayi(W_A), f11, INK)
    ciz_B()
    # ---- C · TOPPING (topping_cad_v24 + uno v11 · hepsi 168 aşağı · kaide 788–892)
    kabin(X_C, W_C, H_B, H_MAK, "C · TOPPING v2 · 4 UNO + 2 kaset · havalı · kama yarık (v5)")
    kaide(KD.C_X[0], KD.C_X[1], "MEKANİZMA KAİDESİ %s · %s–%s · 40 × 100 profil + 4 mm plaka" % (sayi(KD.KAIDE_H), sayi(H_B), sayi(H_MEK)))
    TEK = (100.0, 2495.0, 893.5, 923.5); RAY = (200.0, 700.0 + TH7.RAY_X1, 912.5, 927.5); KAS = (140.0, 2350.0)   # topping_cad_v24 − 168
    d.rectangle([fx(TEK[0]), fy(TEK[3]), fx(TEK[1]), fy(TEK[2])], fill=SOFT, outline=LINE, width=2)
    d.rectangle([fx(RAY[0]), fy(RAY[3]), fx(RAY[1]), fy(RAY[2])], fill=BG, outline=INK, width=2)
    for _kx in KAS:
        d.ellipse([fx(_kx) - 9.55 * S, fy(925.0) - 9.55 * S, fx(_kx) + 9.55 * S, fy(925.0) + 9.55 * S], fill=BG, outline=ACC, width=2)
    drect(fx(111.5), fy(953.5), fx(168.5), fy(896.5), INK, 1)
    txt(fx(140.0), fy(855.0), "X MOTORU (arkada)", f7, INK, "mm")
    d.rectangle([fx(196.6), fy(P), fx(503.4), fy(978.0)], fill=EVC, outline=BUZ, width=2)                     # v19: kaset (park) · taban 978 · bant üstü 1000
    d.rectangle([fx(200.0), fy(950.5), fx(480.0), fy(940.5)], fill=ACC, outline=ACC)                          # v19: araba plakası 280
    txt(fx(1600.0), fy(965.0), "TABLA ARABASI · strok %s (x 350 → %s) · HGR15 ray %s · GT3 kapalı çevrim · tekne 893–923 · KASET 310 × 310 kare bant · üstü %s · z −170" % (sayi(TH7.X_STROK), sayi(round(BT.AKT, 1)), sayi(TH7.RAY_UZUNLUK), sayi(P)), f7, ACC, "mm")
    _st = [p["sh"].BoundingBox() for p in BT.TAHRIK]                                                           # v19: sabit tahrik (kapak arkasında → kesik)
    drect(fx(min(b_.xmin for b_ in _st)), fy(max(b_.ymax for b_ in _st)), fx(max(b_.xmax for b_ in _st)), fy(min(b_.ymin for b_ in _st)), ACC, 2)
    # 4 UNO çekirdeği (sos · harç · kıyma · kuşbaşı) + 2 bizim kaset (kaşar · küp sucuk) — v16 − 168
    UNO9 = [("SOS", 100.0, 320.0, 1569.0, "15 L (V)", True), ("HARÇ", 340.0, 780.0, 1664.0, "45 L", True),
            ("KIYMA", 800.0, 990.0, 1499.0, "8 L", False), ("KUŞBAŞI", 1010.0, 1200.0, 1499.0, "8 L", False)]
    KAS9 = [("KAŞAR", 1220.0, 1502.0, "bizim rende|8,8 kg"), ("KÜP SUCUK", 1522.0, 1664.0, "bizim|2,8 kg")]
    X = lambda l: fx(X_C + l)
    _pu = [(33.0, 1109.0), (33.0, 1860.0), (820.0, 1860.0), (820.0, 1552.0), (W_C - 33.0, 1552.0), (W_C - 33.0, 1109.0)]   # yalıtım YALNIZ soğuk hacmi sarar
    d.polygon([(X(x_), fy(y_)) for x_, y_ in _pu], fill=PUC, outline=GRAY)
    d.rectangle([X(90.0), fy(1800.0), X(790.0), fy(1149.0)], fill=BG, outline=LINE, width=1)                # soğuk A
    d.rectangle([X(790.0), fy(1522.0), X(1710.0), fy(1149.0)], fill=BG, outline=LINE, width=1)              # soğuk B
    d.rectangle([X(821.5), fy(1859.0), X(W_C - 33.0), fy(1553.5)], fill=SOFT, outline=None)                 # teknik cep (yalıtımsız)
    d.line([(X(821.0), fy(1859.0)), (X(821.0), fy(1553.0)), (X(W_C - 33.0), fy(1553.0))], fill=ACC, width=4)   # saç (teknik tarafı)
    txt(X(440.0), fy(1827.0), "YALITIM YALNIZ SOĞUK HACMİ SARAR · PU 60 / L 30", f7, GRAY, "mm")

    for ad, a0, a1, ust, hz, yassi in UNO9:
        c = (a0 + a1) / 2.0; hw = (a1 - a0) / 2.0
        d.rectangle([X(c - 41), fy(1224.6), X(c + 41), fy(1152.0)], fill=BG, outline=INK, width=2)
        d.rectangle([X(c - 91), fy(1212.0), X(c - 41), fy(1168.0)], fill=BG, outline=ACC, width=2)
        d.rectangle([X(c - 32), fy(1284.0), X(c + 32), fy(1224.6)], fill=BG, outline=INK, width=2)
        d.polygon([(X(c - 32), fy(1284.0)), (X(c + 32), fy(1284.0)), (X(c + hw), fy(1464.0)), (X(c + hw), fy(ust)), (X(c - hw), fy(ust)), (X(c - hw), fy(1464.0))], fill=BG, outline=ACC)
        d.line([(X(c - 32), fy(1284.0)), (X(c - hw), fy(1464.0)), (X(c - hw), fy(ust)), (X(c + hw), fy(ust)), (X(c + hw), fy(1464.0)), (X(c + 32), fy(1284.0))], fill=ACC, width=3)
        uc = 1094.0 if yassi else 1048.0
        d.rectangle([X(c - 18), fy(1172.0), X(c + 18), fy(uc)], fill=BG, outline=INK, width=2)
        if yassi:                                                  # spreader (topping_uno_cad_v4)
            d.rectangle([X(c - 25), fy(1106.0), X(c + 25), fy(1094.0)], fill=BG, outline=INK, width=1)
            d.rectangle([X(c - 18), fy(1094.0), X(c + 18), fy(1072.0)], fill=BG, outline=INK, width=2)
            d.rectangle([X(c - 54), fy(1126.0), X(c - 26), fy(1072.0)], fill=BG, outline=ACC, width=2)
            d.polygon([(X(c - 20), fy(1074.0)), (X(c + 123), fy(1074.0)), (X(c + 123), fy(1046.0))], fill=BG, outline=INK)
            d.rectangle([X(c - 8), fy(1050.0), X(c + 125), fy(1014.0)], fill=BG, outline=INK, width=2)
        satirlar(X(c), fy(ust) + 16, "%s|UNO · %s" % (ad, hz), f7, INK, 16)
    for ad, a0, a1, alt in KAS9:
        c = (a0 + a1) / 2.0
        d.rectangle([X(a0 + 2), fy(1512.0), X(a1 - 2), fy(1162.0)], fill=BG, outline=INK, width=3)
        d.rectangle([X(c - 22), fy(1162.0), X(c + 22), fy(1048.0)], fill=BG, outline=INK, width=2)
        satirlar(X(c), fy(1392.0), "%s|%s" % (ad.replace(" ", "|") if a1 - a0 < 200 else ad, alt), f7, INK, 16)
    etiket(fx(2120.0), fy(1084.0), "SABİT TAHRİK · mıknatıslı · NEMA23", f7, ACC, ACC)
    txt(X(1170.0), fy(1030.0), "ağızlar z −170 · spreader altı 1014 · yuvarlak uç 1048 · pide üstü 1008", f7, INK, "mm")
    d.rectangle([X(90.0), fy(1152.0), X(1710.0), fy(1149.0)], fill=INK)
    txt(X(781.0), fy(1128.0), "RAF 1149–1152", f7, INK, "mm")
    drect(X(150.0), fy(1492.0), X(458.0), fy(1432.0), GRAY, 1); txt(X(210.0), fy(1417.0), "valf adası", f7, GRAY, "mm")
    drect(X(1650.0), fy(1252.0), X(1700.0), fy(1082.0), GRAY, 1)                        # şartlandırıcı (arkada) · yazısı parça listesinde
    # teknik bant yalnız x 850–1710 (yerel): soğutma + pano + güç + UPS
    kesik(X_C, 850.0, 1150.0, 1563.5, 1783.5, "SOĞUTMA GRUBU", INK)
    kesik(X_C, 1180.0, 1580.0, 1563.5, 1803.5, "PANO", INK, "PLC · röleler")
    kesik(X_C, 1600.0, 1655.0, 1563.5, 1688.5, "", INK)
    txt(fx(X_C + 1627.0), fy(1707.0), "güç", f7, INK, "mm")
    kesik(X_C, 1660.0, 1709.0, 1563.5, 1685.5, "", INK)
    txt(fx(X_C + 1684.0), fy(1727.0), "UPS", f7, INK, "mm")
    modul_etiketi(X_C, W_C, "MODÜL C · TOPPING v2 (topping_uno_cad_v15 + topping_cad_v27) · soğuk kapaklı · 4 UNO + 2 bizim kaset · havalı · bantlı tabla", "1800 × 909 × %s · dolap üstünde (kaide %s) · kaset bandı %s" % (sayi(H_MAK - H_B), sayi(KD.KAIDE_H), sayi(P)))
    olcu_h(fx(X_C), fx(X_C + W_C), fy(H_MAK) - 26, sayi(W_C), f11, INK)
    # ---- F K E
    ciz_F()
    ciz_K()
    a0, a1, yig = ciz_E()
    _npan = on_paneller()                                     # v18: gerçek ön paneller (montaj v64) + robot ağızları
    print('on paneller:', _npan)
    for x_, y_, s_, f_, c_, a_, z_ in yazi:
        maskeli(x_, y_, s_, f_, c_, a_, zemin=z_)
    del yazi[:]
    birlesimler()
    kot_cizgileri((Y_ALT, H_B, H_MEK, TEPSI_E, (P, "996 · 998 · 1000"), 1152.0, FT.YG1, FT.UST_RAF_Y[1], 1522.0, 1552.0, H_MAK))
    # ---- PLAN
    plan_ortak(P)
    d.rectangle([fx(196.6), py(ZT - 155.0), fx(503.4), py(ZT + 155.0)], fill=EVC, outline=BUZ, width=2)            # v19: kaset 310 × 310 (park)
    txt(fx(350.0), py(ZT - 175.0), "KASET 310 × 310 · park · z −170 · dönüş Ø%s" % sayi(round(2.0 * BT.H.R_SUP, 1)), f7, BUZ, "mm")
    d.rectangle([fx(790.0), py(-630.0), fx(2410.0), py(-104.0)], outline=GRAY, width=1)
    for ad, a0_, a1_, ust, hz, yassi in UNO9:
        c = X_C + (a0_ + a1_) / 2.0; hw = (a1_ - a0_) / 2.0
        drect(fx(c - hw), py(-560.0), fx(c + hw), py(-120.0), ACC, 2)
        d.rectangle([fx(c - 41), py(-428.0), fx(c + 41), py(-346.0)], fill=BG, outline=INK, width=2)
        d.rectangle([fx(c - 18), py(-346.0), fx(c + 18), py(-170.0 + 18)], fill=BG, outline=INK, width=2)
        d.rectangle([fx(c - 29), py(-559.0), fx(c + 29), py(-428.0)], fill=BG, outline=INK, width=2)
        d.rectangle([fx(c - 15), py(-635.0), fx(c + 15), py(-560.0)], fill=BG, outline=INK, width=1)
        d.rectangle([fx(c - 19), py(-811.0), fx(c + 19), py(-672.0)], fill=BG, outline=ACC, width=2)
        if yassi:
            d.rectangle([fx(c - 8), py(-188.0), fx(c + 125), py(-152.0)], fill=BG, outline=INK, width=2)
        maskeli(fx(c), py(-470.0) - 8, ad, f7, INK, zemin=FILL); maskeli(fx(c), py(-470.0) + 8, "UNO", f7, GRAY, zemin=FILL)
    for ad, a0_, a1_, alt in KAS9:
        d.rectangle([fx(X_C + a0_ + 2), py(-525.0), fx(X_C + a1_ - 2), py(-200.0)], fill=BG, outline=INK, width=2)
        satirlar(fx(X_C + (a0_ + a1_) / 2), py(-400.0), "%s|bizim" % ad.replace(" ", "|"), f7, INK, 16)
    dline((fx(350.0), py(ZT)), (fx(BT.AKT), py(ZT)), ACC, 3, 12, 6)
    drect(fx(850.0), py(-760.0), fx(1158.0), py(-660.0), GRAY, 2); txt(fx(1004.0), py(-790.0) - 12, "valf adası", f7, GRAY, "mm")
    drect(fx(2350.0), py(-780.0), fx(2400.0), py(-700.0), GRAY, 2)
    dline((fx(2340.0), py(-740.0)), (fx(2340.0), py(-432.0)), (60, 110, 200), 3, 10, 6)
    dline((fx(2340.0), py(-432.0)), (fx(3790.0), py(-432.0)), (60, 110, 200), 3, 10, 6)
    dline((fx(3790.0), py(-432.0)), (fx(3790.0), py(-780.0)), (60, 110, 200), 3, 10, 6)
    dline((fx(3790.0), py(-780.0)), (fx(4085.0), py(-780.0)), (60, 110, 200), 3, 10, 6)
    txt(fx(3065.0), py(-462.0), "HAVA ANA HATTI Ø10 · üstte y 1782–1809 · K dalı z −780 → MS4", f7, (60, 110, 200), "mm")
    darc(fx(1957.5), py(ZT), BT.H.R_SUP * S, 0.0, 360.0, BUZ, 2, 4.0)                                            # v19: kasetin dönüş zarfı (kaşar istasyonu)
    drect(fx(BT.AKT - 153.4), py(ZT - 155.0), fx(BT.AKT + 153.4), py(ZT + 155.0), BUZ, 2)                           # kaset aktarmada
    drect(fx(min(b_.xmin for b_ in _st)), py(min(b_.zmin for b_ in _st)), fx(max(b_.xmax for b_ in _st)), py(max(b_.zmax for b_ in _st)), ACC, 2)
    txt(fx(2465.0), py(-560.0), "sabit tahrik", f7, ACC, "mm")
    d.rectangle([fx(FT.YB_BURUN[0] - 6.35), py(BT.ZE - 148.0), fx(FT.YB_SON), py(BT.ZE + 148.0)], fill=EVC, outline=BUZ, width=2)   # v19: yükleme bandı
    txt(fx(2684.0), py(-75.0), "YÜKLEME BANDI", f7, BUZ, "mm")
    txt(fx(1600.0), py(-75.0), "TABLA HATTI z −170", f7, ACC, "mm")
    # ---- KESİT 1 · A + DOLAP (K1) + ROBOT
    z = sec(SX1)
    txt(SX1, FY_TOP - 200, "KESİT 1 · A + DOLAP (K1) + ROBOT", f16, ACC)
    txt(SX1, FY_TOP - 162, "Robot hamur TOPUNU ağızdan kasetin bandının ortasına bırakır · kafa iner, koniler döner, hamur Ø280'e açılır", f9, GRAY)
    govde(z, 0.0, H_B, True)
    d.rectangle([z(-760), fy(B_TABAN), z(-2), fy(Y_ALT + 1.5)], fill=PUC, outline=GRAY, width=1)
    cekmeceler(z, CEK_KOL["K1"], YUZ0)
    txt(z(-380), fy(757.0), "K1 · 6 lahmacun · çekmece 680 · açılım 628", f7, DOLAP, "mm")
    govde(z, H_B, H_MAK)
    d.rectangle([z(KD.KZ[0]), fy(H_MEK), z(KD.KZ[1]), fy(H_B)], fill=SOFT, outline=LINE, width=2)
    txt(z(-415.0), fy((H_B + H_MEK) / 2), "MEKANİZMA KAİDESİ %s · %s–%s" % (sayi(KD.KAIDE_H), sayi(H_B), sayi(H_MEK)), f7, INK, "mm")
    d.rectangle([z(-415.0), fy(923.5), z(-5.0), fy(893.5)], fill=SOFT, outline=LINE, width=1)
    d.rectangle([z(-315.0), fy(950.5), z(-25.0), fy(940.5)], fill=ACC, outline=ACC)
    d.rectangle([z(-325.0), fy(P), z(-15.0), fy(978.0)], fill=EVC, outline=BUZ, width=2)                                   # v19: kaset kesiti
    txt(z(-170.0), fy(966.0), "kaset 310 · bant üstü %s" % sayi(P), f7, BUZ, "mm")
    d.polygon([(z(-324.0), fy(1008.0)), (z(-16.0), fy(1008.0)), (z(-16.0), fy(1096.0)), (z(-324.0), fy(1096.0))], outline=INK)
    txt(z(-332.0), fy(1052.0), "2 koni", f7, INK, "rm")
    d.rectangle([z(-500.0), fy(1154.0), z(180.0), fy(1142.0)], fill=SOFT, outline=RED, width=2)
    d.rectangle([z(88.0), fy(1140.0), z(167.0), fy(1067.0)], fill=BG, outline=RED, width=2)
    drect(z(-660.0), fy(1272.0), z(-490.0), fy(H_MEK), INK, 1)
    txt(z(-575.0), fy(1292.0), "açıcı kolonu · Z kızağı 60", f7, INK, "mm")
    satirlar(z(-420.0), fy(1732.0), "UYARI · açıcının kafa plakası ve ön koni motoru|gövdenin 180 mm önüne taşıyor (modeldeki hali)", f7, RED, 17)
    d.rectangle([z(-50.0), fy(P + 220.0), z(0.0), fy(P)], fill=AGZ, outline=RED, width=2)
    txt(z(-30.0), fy(P + 235.0), "HAMUR AĞZI %s–%s" % (sayi(P), sayi(P + 220.0)), f7, RED, "rm")
    D1 = robot_kesit(z, -170.0 + 232.5, P + 100.0, -170.0, P + 100.0, "ROBOT")
    d.ellipse([z(-170.0) - 47.5 * S, fy(P + 100.0) - 47.5 * S, z(-170.0) + 47.5 * S, fy(P + 100.0) + 47.5 * S], fill=URUN, outline=(180, 140, 70), width=2)
    for yy in (Y_ALT, B_TABAN, H_B, H_MEK, P, P + 220.0, 1272.0, H_MAK):
        d.line([(z(-830) - 24, fy(yy)), (z(-830) - 6, fy(yy))], fill=INK, width=2)
        txt(z(-830) - 30, fy(yy), sayi(yy), f7, INK, "rm")
    D2 = kesit_E(P, a0, a1)
    D3 = max(r[5] for r in QR.erisim_tablosu())                   # QR en uzak göz (bilek hedefi göz tabanı + 100)
    ys = int(round(KC.ICECEK_YEDEK["kutu"]))
    y_son = parca_listesi([
        ("MODÜL A", "KONİLİ DÖNER AÇICI · 2 koni (boy 140 · taban Ø90 · yarım açı 17,82°) · 2 × NEMA23 + planet · Z kızağı strok 60 · Ø32 pnömatik · içi v16 ile aynı, 168 aşağı", "1",
         "700 × 909 × 1074 · dolap üstünde · kaide 104 · 40–160 N · örs YOK · v18: açıcı ön redüktörü dik açılı (Motovario NMRV030), en önü +31,7 — ön düzlemin içinde"),
        ("MODÜL B", "ÇEKMECELİ DOLAP (store_cad_v8) · TEK PARÇA 0–4000 · 24 motorlu çekmece (Transmotec PD3665 + GT3 kayış + Accuride DZ3832 · strok 628) · tam kaplayan önler 126–785 · K1 6 lahmacun · K2 6 lahmacun · K3 5 pide · K4 Secop CU KLF4.0CND + arkasında B panosu (PLC) + kaşar/sucuk deposu · K5 (fırın altı) 3 pide + tatlı · K6 (fırın altı) 3 içecek · PU 60 ısı kalkanı + fırın taşıyıcı çerçevesi", "1",
         "4000 × 909 × 788 · +3 °C · soğuk: pide 160 · lahmacun 432 · içecek 144 · tatlı 12 (2 gün) · Secop CU NLE8.8CN + 2 bölge lamelli evaporatör (store_cad_v8)"),
        ("ROBOT ÇÖPÜ", "şerit 3810–4000 (soğuk değil, 3810'da yalıtımlı ara duvar) · 15 L kova 165 × 300 × 400 poşetli · yaylı klape 130 × 130 (y 610–740, mil 748) · alt servis kapağı 126–560", "1",
         "x 3822,5–3987,5 · y 126–426 · z −420…−20 · klape üstü 740 ile fırın çıkıntısı 788 arası 48"),
        ("KAİDE", "mekanizma kaidesi (kaide_cad_v1) · 40 × 100 × 2 kutu profil + 4 mm plaka · A: 7 profil 4,16 m · C: 11 profil 8,86 m", "2",
         "A x 8–692 · C x 708–2492 · 788–892 → mekanizma tabanı 892 · kaset bandı 1000"),
        ("MODÜL C", "TOPPING v2 (topping_uno_cad_v15 + topping_cad_v27 · bantlı tabla, 168 aşağı · yalıtım yalnız soğuk hacmi sarar, teknik cep dışarıda · sos + harç yayıcısında KAMA YARIK) · 4 UNO çekirdeği (Beldos valf + ürün silindiri + Ø32 hava silindiri · sos 15 L V · harç 45 L · kıyma 8 L · kuşbaşı 8 L) · kaşar kaseti 280 + küp sucuk kaseti 140 · 3 mm taşıyıcı raf · valf adası 12 × 5/2 + şartlandırıcı", "1",
         "1800 × 909 × 1074 · dolap üstünde (kaide 104) · kaset bandı 1000 · soğuk hacim A 1800 / B 1522 · teknik cep 820–1800 × 1552–1860 dışarıda"),
        ("HAVA", "JUN-AIR OF302-15B yağsız kompresör · 15 L · 43 L/dk @ 7 bar · FIRIN ÜSTÜ RAFTA SAĞDA · Ø10 ana hat yığınların arkasından (z −432) TOPPING teknik cebine, K dalı MS4'e", "1",
         "x 3600–3980 · 1348–1858 · 25 kg · ortam sınırı 40 °C [föy] · raf üstü sıcaklığı pilotta ölçülecek"),
        ("KASET (bantlı tabla)", "kare bant kaseti 310 × 310 · Forbo Transilon E 3/1 U0/U2 MT 296 · 2 × Ø12 rulo (SMR115-2RS) · kuyruk yaylı gergi (Century 62266SCS) · burun GT2 20T ↔ rotor 28T (Gates 140-2GT-6) · 6 mıknatıslı rotor · motor/kablo YOK · ayar bileziğine 2 pimle oturur, elle çıkar", "1",
         "8,45 kg · bant üstü 1000 · dönüş Ø%s · park AÇICININ ALTI · tabla ekseni z −170" % sayi(round(2.0 * BT.H.R_SUP, 1))),
        ("X TAHRİK", "GT3 KAPALI ÇEVRİM kayış · 2 × 20 diş kasnak x 165 ve 2535 · araba bütün strokta kayışa bağlı · gergi sol kasnak plakasından", "1",
         "strok %s (x 350 → %s) · HGR15 ray %s (x 200–%s), 2 sıra · tekne 2440 (893–923)" % (sayi(TH7.X_STROK), sayi(round(BT.AKT, 1)), sayi(TH7.RAY_UZUNLUK), sayi(700.0 + TH7.RAY_X1))),
        ("X MOTORU", "NEMA23 kapalı çevrim step, TEKNENİN ARKASINDA · mili servis cebinden sağ kasnağa girer", "1",
         "1,2 N·m · gereken %s → %s kat pay (kaset 8,45 kg) · sürtünme 10 N VARSAYIM" % (sayi(round(TH7.X_GEREKEN_TORK, 3)), sayi(round(TH7.X_TORK_PAY, 2)))),
        ("SABİT TAHRİK", "TOPPING sağ-arkasında · pencereli paslanmaz kutu (IP69K yıkama) + NEMA23 STP-MTR-23079 · 6 mıknatıslı disk kasetin rotorunu 4,6 mm'den dokunmadan kavrar · kasette kilit: rotor mıknatısı 1.4016 pime", "1",
         "x 2435–2497 · z −356…−508 · y 954–1019 · kayış kirişine braketli"),
        ("YÜKLEME BANDI", "F ön odasında (bizim) · PTFE 296 · Ø12 burun + Ø30 tahrik · STP-MTR-23079 + GT2 1:1 (teknik bölmede) · kaset burnu %s → bant → fırın bandı %s" % (sayi(round(FT.X_DISK_KENAR, 1)), sayi(FT.BANT_X[0])), "1",
         "x %s–%s · üstü %s · ayaklar gövde tabanında" % (sayi(round(FT.YB_BURUN[0] - 6.35, 1)), sayi(round(FT.YB_SON, 1)), sayi(BT.UST))),
        ("MODÜL F", "TP10 KESİTLİ KONVEYÖR FIRIN (firin_tp10_cad_v10) + ÜST KABİN (firin_ust_kabin_cad_v1, 2 düşer kapak) · Sveba Dahlen TP10 kesiti 730 × 517, gövde 1500 ÖZEL SİPARİŞ · ön oda %s · yükleme bandı ısıtılan bölgenin başında (hızlı alır, sonra fırın hızında) · kızılötesi üst + alt · ısıtılan %s · aynı anda %d ürün" % (sayi(FT.ON_ODA), sayi(FT.ODA), FT.N_URUN) + " · 79 mm ÖNE · ÇEKMECELİ DOLABIN ÜSTÜNDE (altında K5, K6, şerit) · üstte raf 4 mm + 10 takoz: SOL kutu yedeği 320, orta boş 262, SAĞ kompresör · davlumbaz arka yarı", "1",
         "1500 × 909 × 1074 · gövde 788–1305 · bant 998 · raf üstü 1348 · raf yükü 99 kg → şartname: 10 × M6 saplama"),
        ("MODÜL K", "KESME + SPREY (kesme_cad_v6 · 3 kapak tava 20) · K bandı PU 400 + RollerDrive EC5000 · Festo DGRF-C-63-125 + yıldız bıçak Ø296 × 6 + koruma Ø316 · PulsaJet + TG 90° nozül · 20° çit · itici igus ZLW-1040 + SMC MGPM20-60 · üstte tereyağı tankı 3 L + pano · ALTINDA bulaşık + arkasında deterjan / parlatıcı", "1",
         "600 × 909 × 1862 · taban sacı 892–895 · bant 996 · bıçak alt dayama 996,5 · itici E'ye 110"),
        ("BULAŞIK MAKİNESİ", "MEIKO M-iClean US · sepet 400 × 400 · giriş 315 (meiko.com) · K altında, sağ ön dikmeye yaslı (kapağı dikmeye çarpmaz) · solunda önde 77 boş", "1",
         "460 × 633 × 700 · x 4108,5–4568,5 · y 126–826 · z −645…−12 · arka pay 25 · kapak açık z −20…435"),
        ("MODÜL E", "KUTU KATLAMA (kutu_cad_v7 · 6 tava panel + robot ağzı) · standart 32 × 32 × 4,2 E-dalga · şarjör arkada, asansörlü · besleyici 1332 · zımba kalıbı + 4 çubuklu tepsi · köprü · piston SFU1610 · devirme parmağı · U flap katlayıcı · kapak kolu · 7 × NEMA 23 · kalıp ayakları alt rafta 618–622", "1",
         "830 × 909 × 1862 · tepsi 936 · şarjör 240–980 = %d kutu (1,6) · asansör sınırı → ≈ 432 kullanılır · + fırın üstü 320 ≈ 752 (≈ 2,7 gün)" % KC.SARJOR_ADET),
        ("İÇECEK YEDEĞİ", "koli 400 × 267 × 123 (24 kutu) · 2 sütun × 3 kat · E altında önde, sabit ön sacın arkasında · soğutmasız", "6",
         "x 4603–5405 · y 130–499 · z −350…−83 · %d kutu · kapak / sökülür panel AÇIK" % ys),
        ("ROBOT", "Fairino FR5 · TEK ROBOT · yer rayında · omuz 970 · hamur: çekmece → tabla · kutu (çatal) → QR · içecek + tatlı · fire → robot çöpü", "1",
         "bilek mesafesi: tabla %d · kutu %d · QR en uzak göz %d (sınır %d)" % (round(D1), round(D2), round(D3), round(ERISIM))),
        ("RAY", "yer rayı · tek araba · ekseni hat yüzünden 360 (DEĞİŞMEZ)", "1",
         "x %s–%s · z %s–%s · robot merkezi %s–%s · zincirle sol sınır %d" % (sayi(RE.RAY_X[0]), sayi(RE.RAY_X[1]), sayi(RE.RAY_Z[0]), sayi(RE.RAY_Z[1]), sayi(RE.ROBOT_X[0]), sayi(RE.ROBOT_X[1]), round(RE.x_min_etkin()))),
        ("ZİNCİR OLUĞU + ENERJİ ZİNCİRİ", "oluk 90 × 60 · AISI 304 2 mm + 3 mm basılır kapak · rayın koridor tarafında, zeminde · enerji zinciri L %d, sabit ucu ray ortası x %s, hareketli ucu robot arabasında" % (round(RE.L_ZINCIR), sayi(RE.XF)), "1 + 1",
         "oluk x 200–5100 · z 485–575 · y 0–60 · zincirin U döngüsü 340 yüksek, oluk 60: AÇIK"),
        ("ZEMİN KANALI", "kapaklı, üstüne basılır · QR'ın robot tarafından zincir oluğuna, koridoru geçer · robot kablosu + güç / veri iki bölme", "1",
         "x 4760–4840 · z 490–1000 · y −60…0 · kapak z 575–670"),
        ("ROBOT KABLOSU", "kol ↔ kontrol kutusu tek kablo · Fairino standart 4 m + 11 m uzatma = 15 m (inluxrobotics.eu) · artanı QR alt bölmesinde kangal", "1",
         "gereken ≈ 7,1 m · kangal ≈ 7,9 m (Ø270)"),
        ("QR DOLABI", "qr_cad_v1 · 860 × 520 × 2050 · 12 göz 2 × 6 · göz 380 × 190 × 440 (adım 200, 450–1650) · alt bölme 20–447: ROBOT KONTROL KUTUSU 475 × 423 × 268 + kablo kangalı · üst bölme 1653–2048: ANA PANO 400 × 350 × 250 + UPS BX500CI + QR kilit kartı + modem · servis kapakları robot tarafında", "1",
         "x %s–%s · z %s–%s · robot yüzü %s · göz tabanında çatal yarığı yok: AÇIK" % (sayi(QRX[0]), sayi(QRX[1]), sayi(QRZ[0]), sayi(QRZ[1]), sayi(QRZ[0]))),
        ("TEZGÂH", "tezgah_cad_v1 · 600 × 450 × 900 · altta temizlik 2 × 5 L bidon · raf 412 · bez / eldiven / poşet + çöp 10 L · kilitli kişisel çekmece 700–855 (strok 300) · duvar askısı 1650", "1",
         "x %s–%s · z %s–%s (ön duvara yaslı)" % (sayi(TZ.X0), sayi(TZ.X0 + TZ.W), sayi(TZ.Z0), sayi(TZ.Z0 + TZ.D))),
        ("YEDEK STOK", "İÇECEK: dolapta 144 + E altında %d = %d (4 gün 277) · PİZZA KUTUSU: şarjör %d (≈ 432 kullanılır) + fırın üstü 320 · kaşar + sucuk 2 gün (K4 deposu) → 4 gün" % (ys, 144 + ys, KC.SARJOR_ADET), "",
         "robotun erişiminde DEĞİL — eleman 2 günde bir ana gözlere aktarır"),
        ("KONTROL", "ana pano PLC + UPS + robot kontrol kutusu: QR dolabında · B panosu (PLC) K4'te Secop'un arkasında · K ve E panoları kendi üst bölmelerinde · TOPPING panosu + UPS + güç + soğutma üst bantta · ekran yok (tablet)", "", ""),
    ])
    lejant()
    if y_son > H_PX - 170:
        TASMA.append(("parca_listesi", "tablo alti %.0f > %.0f" % (y_son, H_PX - 170)))
    yol = os.path.join(KLASOR, AD_DOSYA + "_HD.png")
    im.save(yol, dpi=(int(200 * K_HD), int(200 * K_HD))); print("yazildi:", yol, "· hat", sayi(HAT), "· bilek", round(D1), round(D2), round(D3), "· tablo alti", round(y_son))
    if TASMA:
        print("UYARI tasma:", TASMA)
    return yol, im


if __name__ == "__main__":
    yol, hd = tablali()
    k = hd.resize((7990, int(hd.size[1] * 7990 / hd.size[0])), Image.LANCZOS)
    k.save(os.path.join(KLASOR, AD_DOSYA + "_EKRAN.png"), optimize=True); print("yazildi EKRAN", k.size)
    k.save(os.path.join(KLASOR, AD_DOSYA + ".pdf"), "PDF", resolution=200.0, title=AD_DOSYA); print("yazildi PDF")
    s = k.resize((4200, int(k.size[1] * 4200 / k.size[0])), Image.LANCZOS)
    s.save(os.path.join(SITE_IMG, AD_DOSYA + "_teknik.png"), optimize=True); print("yazildi site", s.size)
