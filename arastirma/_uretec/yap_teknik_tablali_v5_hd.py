# -*- coding: utf-8 -*-
"""teknik_hat_atosa_tablali_v4 -> v5 : HD (yazilar okunsun)

Kemal: "sunu HD yap, yazilar okunmuyor."

YONTEM — ONEMLI
  Kolay yol (tuvali ve fontlari buyutmek) DUZENI BOZAR: cizimde yuzlerce yerde
  "yaziyi cizginin 26 piksel altina koy" gibi SABIT piksel kaydirmalari var.
  Tuval 2 kat buyuyup bu kaydirmalar ayni kalirsa yazilar cizgilere yapisir.
  O yuzden tuvali degil CIZIM KATMANINI olceklendiriyoruz: ImageDraw'in onune bir
  sarmalayici konuyor, her cagrinin KOORDINATLARINI ve FONTUNU K katina cikariyor.
  Boylece sabit kaydirmalar da olcekleniyor, duzen birebir korunuyor, yalniz
  cozunurluk artiyor.

K = 2,2  ->  6600 x 3400  ->  14520 x 7480 (109 MP)
Yazi boyu 14 px -> 31 px; ekranda %50 kuculse bile okunur.
"""
import io, os

U = os.path.dirname(os.path.abspath(__file__))
s = io.open(os.path.join(U, "teknik_hat_atosa_tablali_v4.py"), encoding="utf-8").read()

# ------------------------------------------------------------------ 1) HD sarmalayici
eski = '''import math, sys
from PIL import Image, ImageDraw, ImageFont'''
yeni = '''import math, sys
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
    """ImageDraw sarmalayicisi — her cagriyi K_HD katina cikarir"""

    def __init__(self, im):
        self.d = ImageDraw.Draw(im)
        self._font = {}

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
        return self.d.line(_ol(xy), **self._w(kw))

    def rectangle(self, xy, **kw):
        return self.d.rectangle(_ol(xy), **self._w(kw))

    def ellipse(self, xy, **kw):
        return self.d.ellipse(_ol(xy), **self._w(kw))

    def polygon(self, xy, **kw):
        return self.d.polygon(_ol(xy), **self._w(kw))

    def arc(self, xy, *a, **kw):
        return self.d.arc(_ol(xy), *a, **self._w(kw))

    def textlength(self, s, font=None, **kw):
        # olceklenmemis (cizim koordinat sisteminde) uzunluk dondur
        return self.d.textlength(s, font=self._f(font), **kw) / K_HD
# ======================================================'''
assert eski in s
s = s.replace(eski, yeni, 1)

# ------------------------------------------------------------------ 2) tuval K kati, cizim katmani sarmalayici
s = s.replace(
    'im = Image.new("RGB", (W_PX, H_PX), BG); d = ImageDraw.Draw(im)',
    'im = Image.new("RGB", (int(W_PX * K_HD), int(H_PX * K_HD)), BG); d = HDraw(im)')

# ------------------------------------------------------------------ 3) cikti adi + dpi
s = s.replace(r"\HAT_ATOSA_TABLALI_v4_teknik.png", r"\HAT_ATOSA_TABLALI_v5_HD.png")
s = s.replace("im.save(yol, dpi=(200, 200))", "im.save(yol, dpi=(int(200 * K_HD), int(200 * K_HD)))")
s = s.replace("TEKNİK RESİM  v4", "TEKNİK RESİM  v5 · HD")


# ------------------------------------------------------------------ 4) kesik() alt yazisi COK SATIR olsun
# kesik()'in "alt" parametresi tek satir yaziyordu; acici kolonunun uzun aciklamasi
# paftadan tasip soldaki bosluga sarkiyordu. Artik "|" ile satira boluyor.
eski_k = """    if alt:
        txt(fx(x0mm + (a + b) / 2), fy((y0 + y1) / 2) + 10, alt, f7, GRAY, "mm")"""
yeni_k = """    if alt:
        _n = alt.count("|")
        satirlar(fx(x0mm + (a + b) / 2), fy((y0 + y1) / 2) + 10 + 8.5 * _n, alt, f7, GRAY, 17)"""
assert eski_k in s
s = s.replace(eski_k, yeni_k, 1)

io.open(os.path.join(U, "teknik_hat_atosa_tablali_v5_hd.py"), "w", encoding="utf-8").write(s)
print("teknik_hat_atosa_tablali_v5_hd.py yazildi · K =", 2.2)
