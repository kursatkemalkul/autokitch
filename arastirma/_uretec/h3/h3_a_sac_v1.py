# -*- coding: utf-8 -*-
"""h3_a_sac_v1 — A (AÇICI) İSTASYONU GÖVDESİ · ÜRETİM SACI v1 (4 Eki 2026 · Claude · YEREL · bağımsız üreteç, montaja bağlı DEĞİL)

Kemal: "üretim sacını yap ama tam yap, üretime yönelik" — sac atölyesi (lazer + abkant + TIG + PEM presi) doğrudan 3B'den üretir.
STANDART: h3_k_sac_v1 (K pilotu) ile birebir aynı kurgu · h3_sac_v1 kütüphanesi (gerçek büküm R = 1,5t, K 0,45, açınım, DFM, PEM/vida BOM) ·
          sac_kararlar_v1.json > sac_standart_v1.json (kabuk 1,5 · kapak 1,5 + 1,0 · braket 3 · kaide plakası 4).
KURAL (Kemal): A'nın içinde YALNIZ satın alınan açıcı (dönme kafası, kolonu kaide sacına oturur) + tabla geçişi (ray / araba / tabla sağ duvardaki
          ağızdan TOPPING'e geçer). A'dan kablo / kanal / hortum geçmez → A saclarında elektrik ağzı YOK. A dış ölçüsü 700 ve yeri SABİT.
KOORDİNAT: A YERELİ (x 0…700, dünya = x + 736 · y yerden · z ön +59 gövde / +79 kapak önü, arka −830). Bütün parçalar dünyaya dunya_listesi() ile taşınır.

KURGU (atölye mantığı — K ile aynı)
  1 · KAİDE (kaynaklı alt montaj, 788–892): 304 dikdörtgen boru 40 × 100 × 2 (EN 10219 · dış R 4) çevre çerçeve + ortada enine + iki boyuna
      (mevcut A kaidesiyle aynı düzen; çerçeve panel dönüşlerine yer açmak için 3,5 / 15 mm içeri alındı) · 4 mm üst plaka (888–892) borulara
      DELİK KAYNAĞIYLA (yüz taşlanır) · 1,5 mm DAMLAMA / MEKANİZMA SACI (892–893,5: açıcı kolonu ve tabla rayı bunun üstüne oturur) plakaya punta,
      dikme çevresi çentik + TIG (sızdırmaz) · AÇICI KOLONU 4 × PEM SP-M8 (plakanın altında) · TABLA RAYI 4 × PEM SP-M6 · A → B 6 × M8
      (kaide borusunun alt duvarından · baş boru içinde DIN 9021 pulla · üstten Ø16 servis deliği + silikon tapa · B üst kirişlerine perçin somun = ARAYÜZ).
  2 · İSKELET (kaynaklı): 304 kare boru 30 × 30 × 2 · 4 dikme (892 → 2194,5 + 2 mm tapa) + üst halka (ön / arka / sol / sağ kuşak 2168,5–2198,5)
      · K ile aynı dikme eksenleri (yerel x 20 / 680 · z 42 / −800) → yan sacların ön / arka dönüşleri dikmelerin önünde / arkasında.
  3 · SÖKÜLEBİLİR PANELLER (servis): sol / sağ yan 1,5 (ön 16,5 + arka 22 iç dönüş) → dikme / üst halka kulaklarına PEM FHP-M5 saplama + pul +
      fiberli somun (dışta iz yok) · üst sac 1,5 (ön + arka aşağı dönüş) → üst halka kulaklarına FHP-M5 · arka sac 1,5 (alt dönüş, B tavanına oturur)
      → arka saca preslenmiş FHP-M5 saplamalar yan sacların arka dönüşlerinden + üst sacın arka dönüşünden geçer, somun İÇERİDEN (arka yüzde baş yok).
      Sağ yan sacta TABLA GEÇİŞ AĞZI (mevcut ölçü, R6 köşe) — A'da başka ağız yok.
  4 · TEK ÖN KAPAK (mevcut ölçü 736–1434,5 × 788–2197, z 59–79): çift cidar (dış tava 1,5 bindirme + TIG · iç tava 1,0 punta) · 3 gizli 180°
      kaldır-çıkar menteşe (sol ön dikmenin içinde, sanal pivot ön-sol köşe) · 3 bas-aç (sağ ön dikmenin içinde) · KULP YOK · fitil yok
      (A soğuk değil; kapak dönüşü dikme önüne 0,5 boşlukla kapanır, K ile aynı).
  5 · KOMŞU BİRLEŞİMLERİ: A ↔ TOPPING 4 × M8 (TOPPING sol duvarı PU'lu → cıvata A içinden sağ yan sacın Ø9'undan, TOPPING dış sacında PEM SP-M8
      somun = ARAYÜZ) · A → B 6 × M8 (kaide borusundan, B üst kirişlerinde perçin somun = ARAYÜZ).
ARAYÜZLER DEĞİŞMEZ: dış zarf x 736–1436 · y 788–2200 · z −830…+79 · tabla geçiş ağzı (sağ yan) · kapak dış ölçüsü · açıcı kolonunun ve rayın
  oturma yüzü 893,5 · mekanizmaya dokunulmaz.
Çalıştır (öz denetim + çıktılar): gece2/adim5/a_sac_denetim_v1.py (scratchpad) · bu dosya yalnız KURAR."""
import math, os, sys, re, time
H3 = os.path.dirname(os.path.abspath(__file__)); _U = os.path.dirname(H3)
for _p in (_U, H3):
    if _p not in sys.path: sys.path.insert(0, _p)
import numpy as np
import cadquery as cq
import h3_sac_v1 as S

SURUM = "h3_a_sac_v1"
V = cq.Vector
X_A = 736.0
BIRIM = "A_GOVDE"
# ---------------------------------------------------------------- ARAYÜZ (A yereli · değişmez)
W = 700.0
Y_DOLAP, Y_PLAKA, Y_TAVA, Y_MEK = 788.0, 888.0, 892.0, 893.5          # B tavanı · kaide plakası altı · damlama sacı altı / üstü (açıcı + ray oturma yüzü)
Y_UST_ALT, Y_UST = 2198.5, 2200.0
Z_ON, Z_KAPAK, Z_ARKA, Z_ARKA_IC = 59.0, 79.0, -830.0, -828.5
KAPAK_X, KAPAK_Y = (0.0, 698.5), (788.0, 2197.0)                       # mevcut A_ONYUZ: dünya 736–1434,5 × 788–2197
TABLA_AGZI = (893.4, 1042.0, -510.0, 4.0)                              # sağ yan sac (y0, y1, z0, z1) · v8zq A sağ levhası (TOPPING sol sacındaki ağızla eş)
ACICI_M8 = [(305.0, -645.0), (395.0, -645.0), (305.0, -520.0), (395.0, -520.0)]   # açıcı kolonu ayağı dünya x 1026–1146 · z −660…−505 → köşelerden 15 içeri
RAY_M6 = [(144.0, -320.0), (144.0, -20.0), (564.0, -320.0), (564.0, -20.0)]       # tabla rayı tabanı dünya x 836–2495 · z −415…−5 · raydaki serbest bantlar (−335…−305 · −35…−5), boyuna borunun dışında
# ---------------------------------------------------------------- iskelet
PB, PT, PRO = 30.0, 2.0, 4.0
PX, PZ = (20.0, 680.0), (42.0, -800.0)                                 # dikme eksenleri (K ile aynı kenar mesafeleri)
Y_DIKME = (Y_TAVA, 2194.5)                                             # + 2 mm tapa → 2196,5 (üst sacın altında 2 mm)
Y_HALKA = (2168.5, 2198.5)
# kaide (40 × 100 × 2 dikdörtgen boru · y 788–888)
KB, KH, KT, KRO = 40.0, 100.0, 2.0, 4.0
K_X = (5.0, 695.0)                                                     # çevre çerçevenin dış x'i (yan sac iç yüzünden 3,5 içeri — dikmeyle hizalı)
K_Z = (57.0, -815.0)                                                   # çevre çerçevenin ön / arka dış yüzü (dikme ön / arka yüzüyle hizalı)
K_ENINE_X = (330.0, 370.0)                                             # mevcut enine 1066–1106
K_BOYUNA_Z = (-416.8, -376.7)                                          # mevcut boyuna
AB_M8 = [(25.0, -706.0), (25.0, -110.0), (350.0, -706.0), (350.0, -110.0), (675.0, -706.0), (675.0, -110.0)]   # A → B (B üst kirişleri z −721…−691 / −125…−95)
# kapak donanımı (dikme içi)
MENTESE_Y = (950.0, 1500.0, 2050.0)
BASAC_Y = (1000.0, 1560.0, 2100.0)
BASAC_X = 676.0
# kulaklar
KULAK_DIKME_Y = dict(on=(1080.0, 1400.0, 1750.0, 2100.0), arka=(930.0, 1300.0, 1700.0, 2100.0))   # ön: tabla geçiş ağzının (z ≤ 4, y ≤ 1042) dışında
KULAK_UST = dict(on=(120.0, 350.0, 580.0), arka=(120.0, 350.0, 580.0))
M8_T = [(1300.0, -300.0), (1300.0, -700.0), (2000.0, -300.0), (2000.0, -700.0)]     # A ↔ TOPPING (y, z): TOPPING sol duvarı PU'lu soğuk oda → cıvata A İÇİNDEN, TOPPING dış sacında PEM SP-M8
ESKI_GOVDE = ("A_GOVDE__paslanmaz", "A_GOVDE__sac", "A_GOVDE__plastik", "KAIDE_A__paslanmaz", "KAIDE_A__sac", "A_ONYUZ__on_seffaf",
              "A_ONYUZ__on_seffaf__SERVIS_KAPAGI", "A_ONYUZ__paslanmaz", "A_ONYUZ__plastik", "A_MODULER__paslanmaz")
S._RENK.update({"profil": ((0.70, 0.73, 0.77, 1.0), 0.85, 0.30), "mekanizma": ((0.42, 0.46, 0.52, 1.0), 0.4, 0.5), "arayuz": ((0.90, 0.22, 0.15, 1.0), 0.3, 0.5),
                "kapak": ((0.70, 0.82, 0.95, 1.0), 0.2, 0.25), "conta": ((0.15, 0.15, 0.16, 1.0), 0.0, 0.8)})


def kutu(x0, x1, y0, y1, z0, z1):
    return cq.Solid.makeBox(abs(x1 - x0), abs(y1 - y0), abs(z1 - z0), V(min(x0, x1), min(y0, y1), min(z0, z1)))


def silindir(p0, eksen, r, L):
    e = np.asarray(eksen, float); e = e / np.linalg.norm(e)
    return cq.Solid.makeCylinder(float(r), float(L), V(*map(float, p0)), V(*map(float, e)))


def _bir(*ss):
    s = ss[0]
    for q in ss[1:]: s = s.fuse(q)
    return s.clean()


# =====================================================================================================================================
# 1 · PROFİL (kare / dikdörtgen boru, gerçek dış R) — h3_k_sac_v1.Profil ile aynı, kesit b1 × b2
# =====================================================================================================================================
EKSEN = {"x": np.array([1.0, 0, 0]), "y": np.array([0, 1.0, 0]), "z": np.array([0, 0, 1.0])}


class Profil:
    """eksen boyunca a0 → a1 · c = dik eksenlerdeki merkez (x için (y, z) · y için (x, z) · z için (x, y)) · b1 / b2: dik eksen sırasıyla kesit ölçüsü"""
    def __init__(self, ad, eksen, a0, a1, c, b1=PB, b2=None, t=PT, Ro=PRO, not_="", std="Kare boru"):
        self.ad, self.eksen, self.a0, self.a1, self.c = ad, eksen, float(a0), float(a1), tuple(map(float, c))
        self.b1, self.b2, self.t, self.Ro, self.not_, self.std = float(b1), float(b2 if b2 is not None else b1), t, Ro, not_, std
        self.kesikler, self.uc_kaynak = [], []
        self._sh = None

    def merkez(self, a):
        p = np.zeros(3); p["xyz".index(self.eksen)] = a
        dik = [k for k in "xyz" if k != self.eksen]
        p["xyz".index(dik[0])], p["xyz".index(dik[1])] = self.c
        return p

    def yari(self, k):
        dik = [q for q in "xyz" if q != self.eksen]
        return (self.b1 if k == dik[0] else self.b2) / 2.0

    def _govde(self):
        dis = S.yuz_dikd_r(0.0, 0.0, self.b1, self.b2, 0.0, self.Ro)
        ic = S.yuz_dikd_r(0.0, 0.0, self.b1 - 2 * self.t, self.b2 - 2 * self.t, 0.0, self.Ro - self.t)
        sh = S._prizma(dis.cut(ic), self.a1 - self.a0)
        dik = [k for k in "xyz" if k != self.eksen]
        ex, ey, ez = EKSEN[dik[0]], EKSEN[dik[1]], EKSEN[self.eksen]
        if np.linalg.det(np.column_stack([ex, ey, ez])) < 0:
            # sol el → kesiti y'de aynala (b2 simetrik olduğundan şekil aynı)
            ey = -ey
        return S._tasi(sh, S._M(np.column_stack([ex, ey, ez]), self.merkez(self.a0)))

    def duvar_delik(self, yuz, a, kayma, cap, tip="delik", not_=""):
        n = EKSEN[yuz[1]] * (1 if yuz[0] == "+" else -1)
        dik = [k for k in "xyz" if k not in (self.eksen, yuz[1])][0]
        p = self.merkez(a) + n * (self.yari(yuz[1]) + 1.0) + EKSEN[dik] * kayma
        cut = silindir(p, -n, cap / 2.0, self.t + 1.6)
        self.kesikler.append(dict(sh=cut, tip=tip, yuz=yuz, a=round(a - self.a0, 2), kayma=kayma, cap=cap, not_=not_, _dik=dik)); self._sh = None
        return cut

    def duvar_pencere(self, yuz, a, kayma, la, lk, tip="pencere", not_=""):
        sg = 1.0 if yuz[0] == "+" else -1.0
        dik = [k for k in "xyz" if k not in (self.eksen, yuz[1])][0]
        c = self.merkez(a); h = self.yari(yuz[1])
        lo, hi = np.zeros(3), np.zeros(3)
        for i, k in enumerate("xyz"):
            if k == self.eksen: lo[i], hi[i] = a - la / 2.0, a + la / 2.0
            elif k == dik: lo[i], hi[i] = c[i] + kayma - lk / 2.0, c[i] + kayma + lk / 2.0
            else:
                d0, d1 = c[i] + sg * (h - self.t - 0.6), c[i] + sg * (h + 1.0)
                lo[i], hi[i] = min(d0, d1), max(d0, d1)
        cut = kutu(lo[0], hi[0], lo[1], hi[1], lo[2], hi[2])
        self.kesikler.append(dict(sh=cut, tip=tip, yuz=yuz, a=round(a - self.a0, 2), kayma=kayma, olcu=[la, lk], not_=not_, _dik=dik)); self._sh = None
        return cut

    def kati(self):
        if self._sh is None:
            sh = self._govde()
            for k in self.kesikler: sh = sh.cut(k["sh"])
            self._sh = sh.clean()
        return self._sh

    def dfm(self):
        out = []; L = self.a1 - self.a0
        for k in self.kesikler:
            duz = self.yari(k["_dik"]) - self.Ro
            yar = (k.get("cap") or k["olcu"][1]) / 2.0
            ok = abs(k["kayma"]) + yar <= duz + 1e-6
            out.append(dict(kural="profil_duz_yuz", durum="GEÇTİ" if ok else "HATA", detay="%s %s %s Ø/en %.1f kayma %.1f · düz yüz ±%.1f" % (self.ad, k["tip"], k["yuz"], 2 * yar, k["kayma"], duz)))
            la = (k.get("cap") or k["olcu"][0]) / 2.0
            uc = min(k["a"] - la, L - k["a"] - la)
            out.append(dict(kural="profil_uc", durum="GEÇTİ" if uc >= 3.0 else "HATA", detay="%s %s → boru ucu %.1f (≥ 3)" % (self.ad, k["tip"], uc)))
            for (yz, b0, b1) in self.uc_kaynak:
                if yz == k["yuz"] and b0 - la - 3.0 < k["a"] < b1 + la + 3.0:
                    out.append(dict(kural="profil_kaynak_bolgesi", durum="HATA", detay="%s %s kaynaklı birleşim bölgesinde (%s %.0f–%.0f)" % (self.ad, k["tip"], yz, b0, b1)))
        out.append(dict(kural="profil_boy", durum="GEÇTİ" if L <= 6000 else "HATA", detay="%s L %.1f ≤ 6000 (boy stoğu)" % (self.ad, L)))
        return out

    def parca(self):
        sh = self.kati(); L = self.a1 - self.a0
        kg = sh.Volume() * S.YOGUNLUK
        kes = [dict({k: v for k, v in x.items() if k not in ("sh", "_dik")}) for x in self.kesikler]
        return dict(ad=self.ad, wp=cq.Workplane("XY").add(sh), sh=sh, mal="sac", birim=BIRIM, grup="SABIT", kaynak=SURUM, tur="profil",
                    bom=("%s AISI 304 %g × %g × %g (EN 10217-7 / EN 10219 · dış R %g) · %s" % (self.std, self.b1, self.b2, self.t, self.Ro, self.not_), 1, "L %.1f" % L,
                         "boru lazer / şerit testere 90° · %d kesik · %.2f kg" % (len(kes), kg), "ÜRETİM"),
                    meta=dict(tur="profil", eksen=self.eksen, L=round(L, 2), kesit=[self.b1, self.b2, self.t, self.Ro], kesikler=kes, kg=round(kg, 3)))


def uc_kaynaklari(ad, nokta, yon_ray, yuzler, b, flat, a=PT):
    """boru ucu ↔ karşı boru yüzü köşe kaynakları · nokta: birleşim düzleminde boru ekseni · yon_ray: borudan uzağa · yuzler: içbükey köşe yan yüz normalleri
    · b: o normal doğrultusundaki boru ölçüsü · flat: dikiş boyu (düz yüz)"""
    e = np.asarray(yon_ray, float); out = []
    for i, nf in enumerate(yuzler):
        nf = np.asarray(nf, float); w = np.cross(e, nf)
        p = np.asarray(nokta, float) + nf * (b / 2.0)
        out.append(S.kaynak_dikisi(p - w * flat / 2.0, p + w * flat / 2.0, e, nf, a, ad="%s_%d" % (ad, i), birim=BIRIM, taraf="dis (köşe)",
                                   not_="boru ucu ↔ boru · TIG 141 · ER308LSi"))
    return out


# =====================================================================================================================================
# 2 · KUR
# =====================================================================================================================================
class G:
    SAC, PROFIL, ELEMAN, KAYNAK, BIRLESIM, ARAYUZ, KULAK = [], [], [], [], [], [], []
    PANEL, NOT, PROF, M8 = {}, [], {}, []
    kuruldu = False


def _sac(ad, rol, **k):
    s = S.Sac(ad, rol=rol, birim=BIRIM, kaynak=SURUM, **k); G.SAC.append(s); return s


def _eleman(p, mal="celik"):
    p["mal"] = p.get("mal") if p.get("mal") not in (None, "katalog", "paslanmaz") else mal
    p["birim"] = BIRIM; G.ELEMAN.append(p); return p


def _arayuz(p, karsi, gerek, not_=""):
    p["tur"] = "arayuz"; p["arayuz"] = dict(karsi=karsi, gerek=gerek, not_=not_); p["birim"] = BIRIM; G.ARAYUZ.append(p); return p


def _ozel(ad, sh, std, tanim, olcu, malzeme="AISI 304", mal="celik", uretim=False, tur="baglanti", meta=None):
    p = S._bp(ad, sh, std, tanim, olcu, malzeme, birim=BIRIM, meta=meta or {}, uretim=uretim, mal=mal)
    p["tur"] = tur
    return p


def _halka(merkez, eksen, r_dis, r_ic, h):
    return silindir(merkez, eksen, r_dis, h).cut(silindir(np.asarray(merkez) - np.asarray(eksen) * 1.0, eksen, r_ic, h + 2.0))


def kaide():
    """kaynaklı kaide: 40 × 100 × 2 dikdörtgen boru çevre + enine + 2 boyuna · kaynaklar · A → B delikleri"""
    P = G.PROF
    yc = (Y_DOLAP + Y_PLAKA) / 2.0
    x0, x1 = K_X; zf, zb = K_Z
    # ön / arka: tam boy (x) · kesit dik eksenler (y, z) → b1 = y (100) · b2 = z (40)
    P["kaide_on_boru"] = Profil("kaide_on_boru", "x", x0, x1, (yc, zf - KB / 2), b1=KH, b2=KB, t=KT, Ro=KRO, std="Dikdörtgen boru", not_="kaide ön (100 × 40)")
    P["kaide_arka_boru"] = Profil("kaide_arka_boru", "x", x0, x1, (yc, zb + KB / 2), b1=KH, b2=KB, t=KT, Ro=KRO, std="Dikdörtgen boru", not_="kaide arka")
    za, zo = zb + KB, zf - KB                                                                          # yan boruların z aralığı (ön / arka borular arası)
    for ad, xm in (("kaide_sol_boru", x0 + KB / 2), ("kaide_sag_boru", x1 - KB / 2), ("kaide_enine_boru", sum(K_ENINE_X) / 2)):
        P[ad] = Profil(ad, "z", za, zo, (xm, yc), b1=KB, b2=KH, t=KT, Ro=KRO, std="Dikdörtgen boru", not_="kaide yan / enine (z)")
    zbm = sum(K_BOYUNA_Z) / 2
    P["kaide_boyuna_boru_sol"] = Profil("kaide_boyuna_boru_sol", "x", x0 + KB, K_ENINE_X[0], (yc, zbm), b1=KH, b2=K_BOYUNA_Z[1] - K_BOYUNA_Z[0], t=KT, Ro=KRO,
                                        std="Dikdörtgen boru", not_="kaide boyuna (orta)")
    P["kaide_boyuna_boru_sag"] = Profil("kaide_boyuna_boru_sag", "x", K_ENINE_X[1], x1 - KB, (yc, zbm), b1=KH, b2=K_BOYUNA_Z[1] - K_BOYUNA_Z[0], t=KT, Ro=KRO,
                                        std="Dikdörtgen boru", not_="kaide boyuna (orta)")
    # kaynaklar: yan / enine uçları ön ve arka borulara (dikey yan yüzlerde iç köşe · üst / alt yüz alın kaynağı taşlanır)
    K = G.KAYNAK
    for ad in ("kaide_sol_boru", "kaide_sag_boru", "kaide_enine_boru"):
        xm = P[ad].c[0]
        for z, e in ((zo, (0, 0, -1.0)), (za, (0, 0, 1.0))):
            K += uc_kaynaklari("%s_kaynak_%d" % (ad, int(-z)), (xm, yc, z), e, [(1.0, 0, 0), (-1.0, 0, 0)], KB, KH - 2 * KRO)
    for ad, xs, e in (("kaide_boyuna_boru_sol", x0 + KB, (1.0, 0, 0)), ("kaide_boyuna_boru_sol", K_ENINE_X[0], (-1.0, 0, 0)),
                      ("kaide_boyuna_boru_sag", K_ENINE_X[1], (1.0, 0, 0)), ("kaide_boyuna_boru_sag", x1 - KB, (-1.0, 0, 0))):
        K += uc_kaynaklari("%s_kaynak_%d" % (ad, int(xs)), (xs, yc, zbm), e, [(0, 0, 1.0), (0, 0, -1.0)], K_BOYUNA_Z[1] - K_BOYUNA_Z[0], KH - 2 * KRO)
    # A → B: alt duvarda Ø9 (cıvata) · üst duvarda Ø16 (baş + alyan anahtarı geçişi) — cıvata başı alt duvarın iç yüzüne DIN 9021 pulla oturur
    for x, z in AB_M8:
        ad = "kaide_sol_boru" if x < 100 else ("kaide_sag_boru" if x > 600 else "kaide_enine_boru")
        pr = P[ad]
        pr.duvar_delik("-y", z, x - pr.c[0], 9.0, tip="ab_civata", not_="A→B M8 (alt duvar · ISO 273 orta)")
        pr.duvar_delik("+y", z, x - pr.c[0], 16.0, tip="ab_servis", not_="A→B M8 baş geçişi (üst duvar)")
    G.NOT.append("kaide: 40 × 100 × 2 dikdörtgen boru (mevcut A kaidesiyle aynı kesit ve düzen) · uç birleşimleri dikey yüzlerde TIG köşe, üst / alt yüz alın kaynağı taşlanır")
    return P


def iskelet():
    P = G.PROF
    y0, y1 = Y_DIKME
    for x in PX:
        for z in PZ:
            ad = "kose_dikmesi_%d_%d" % (int(x), int(z))
            P[ad] = Profil(ad, "y", y0, y1, (x, z), not_="köşe dikmesi (kaynaklı iskelet)")
    ya, yb = Y_HALKA; yc = (ya + yb) / 2.0
    for z in PZ:
        ad = "ust_halka_%s" % ("on" if z > 0 else "arka")
        P[ad] = Profil(ad, "x", PX[0] + PB / 2, PX[1] - PB / 2, (yc, z), not_="üst halka %s" % ("ön" if z > 0 else "arka"))
    for x in PX:
        ad = "ust_halka_%s" % ("sol" if x < 350 else "sag")
        P[ad] = Profil(ad, "z", PZ[1] + PB / 2, PZ[0] - PB / 2, (x, yc), not_="üst halka yan")
    K = G.KAYNAK
    for x, sx in ((PX[0], 1), (PX[1], -1)):
        for z in PZ:
            dk = P["kose_dikmesi_%d_%d" % (int(x), int(z))]
            dk.uc_kaynak.append(("+x" if sx > 0 else "-x", ya - y0, yb - y0))
            dk.uc_kaynak.append(("-z" if z > 0 else "+z", ya - y0, yb - y0))
    # üst halka uçları (dikmenin iç yan yüzüne · alt yüzde iç köşe; üst yüzü üst sac oturur → alın, taşlanır)
    for z in PZ:
        for xx, e in ((PX[0] + PB / 2, (1.0, 0, 0)), (PX[1] - PB / 2, (-1.0, 0, 0))):
            K += uc_kaynaklari("ust_halka_kaynak_%d_%d" % (int(-z), int(xx)), (xx, yc, z), e, [(0, -1.0, 0)], PB, PB - 2 * PRO)
    for x in PX:
        for zz, e in ((PZ[0] - PB / 2, (0, 0, -1.0)), (PZ[1] + PB / 2, (0, 0, 1.0))):
            K += uc_kaynaklari("ust_halka_yan_kaynak_%d_%d" % (int(x), int(-zz)), (x, yc, zz), e, [(0, -1.0, 0)], PB, PB - 2 * PRO)
    # dikme tapaları (2 mm · pahlı · alın kaynağı taşlanır)
    c = 2.5
    for x in PX:
        for z in PZ:
            t = _sac("kose_dikmesi_%d_%d_tapa" % (int(x), int(z)), "braket", t=2.0)
            u0, u1, v0, v1 = x - PB / 2, x + PB / 2, -(z + PB / 2), -(z - PB / 2)
            t.taban([(u0 + c, v0), (u1 - c, v0), (u1, v0 + c), (u1, v1 - c), (u1 - c, v1), (u0 + c, v1), (u0, v1 - c), (u0, v0 + c)],
                    O=(0, Y_DIKME[1], 0), ex=(1, 0, 0), ey=(0, 0, -1), ad="tapa")
    return P


def plaka_ve_tava():
    """4 mm kaide üst plakası (delik kaynağı ile borulara) + 1,5 mm damlama / mekanizma sacı (punta) · PEM'ler · servis delikleri"""
    x0, x1 = K_X; zf, zb = K_Z
    pl = _sac("kaide_ust_plaka_4", "braket", t=4.0)
    Q = pl.taban([(x0, -zf), (x1, -zf), (x1, -zb), (x0, -zb)], O=(0, Y_PLAKA, 0), ex=(1, 0, 0), ey=(0, 0, -1), ad="plaka")
    tv = _sac("kaide_damlama_saci", "dis", bolge="sicrama")
    T = tv.taban([(x0, -zf), (x1, -zf), (x1, -zb), (x0, -zb)], O=(0, Y_TAVA, 0), ex=(1, 0, 0), ey=(0, 0, -1), ad="damlama")
    G.PANEL["plaka"], G.PANEL["tava"] = Q, T
    # dikme çentikleri (damlama sacı: dikme çevresi 0,5 boşluk, TIG ile kapatılır)
    for x in PX:
        for z in PZ:
            u0, u1 = (x0 - 1.0, x + PB / 2 + 0.5) if x < 350 else (x - PB / 2 - 0.5, x1 + 1.0)
            v0, v1 = (-zf - 1.0, -(z - PB / 2 - 0.5)) if z > 0 else (-(z + PB / 2 + 0.5), -zb + 1.0)
            T.kesik([(u0, v0), (u1, v0), (u1, v1), (u0, v1)], tip="dikme_centigi", dfm=False, parca="dikme çevresi 0,5 boşluk · TIG köşe kaynağıyla kapatılır")
    # delik kaynağı yarıkları (plaka ↔ kaide boruları) · yüz taşlanır
    yar = [(x, zf - KB / 2, 0.0) for x in (120.0, 240.0, 460.0, 580.0)] + [(x, zb + KB / 2, 0.0) for x in (120.0, 240.0, 460.0, 580.0)] + \
          [(x0 + KB / 2, z, 90.0) for z in (-640.0, -200.0)] + [(x1 - KB / 2, z, 90.0) for z in (-640.0, -200.0)] + \
          [(sum(K_ENINE_X) / 2, z, 90.0) for z in (-600.0, -200.0)] + [(x, sum(K_BOYUNA_Z) / 2, 0.0) for x in (180.0, 520.0)]
    for x, z, a in yar:
        Q.oblong(x, -z, 25.0, 8.0, a, tip="kaynak_yarigi", parca="delik kaynağı 25 × 8 (boruya) · yüz taşlanır")
    for i, (x, z, a) in enumerate(yar):
        f = S.yuz_oblong(x, -z, 25.0, 8.0, a)
        sh = S._tasi(S._prizma(f, 4.0), S._M(np.column_stack([[1, 0, 0], [0, 0, -1.0], [0, 1.0, 0]]), (0, Y_PLAKA, 0)))
        G.KAYNAK.append(dict(ad="kaide_ust_plaka_delik_kaynagi_%d" % i, wp=cq.Workplane("XY").add(sh), sh=sh, mal="sac", birim=BIRIM, grup="SABIT", kaynak=SURUM, tur="kaynak",
                             bom=("Delik (yarık) kaynağı · TIG 141 · ER308LSi · yüz taşlanır", 1, "25 × 8 × 4", "kaide plakası ↔ boru", "ÜRETİM"),
                             meta=dict(tur="kaynak", tip="delik", yontem="TIG 141")))
    # damlama sacı ↔ plaka: punta (köşeler + kenar ortaları)
    tv.punta(pl, [(x, Y_TAVA, z) for x in (40.0, 350.0, 660.0) for z in (20.0, -400.0, -780.0)], not_="damlama sacı → kaide plakası · plakadaki punta izi alt yüzde")
    # dikme ↔ plaka (çentik içinden) + damlama sacı üstünde sızdırmaz köşe kaynağı
    for x in PX:
        for z in PZ:
            sx = 1.0 if x < 350 else -1.0; sz = -1.0 if z > 0 else 1.0
            px = x + sx * PB / 2; pz = z + sz * PB / 2
            G.KAYNAK.append(S.kaynak_dikisi((px, Y_MEK, z - 11), (px, Y_MEK, z + 11), (sx, 0, 0), (0, 1.0, 0), 2.0,
                                            ad="kaide_damlama_dikme_kaynagi_%d_%d_a" % (int(x), int(z)), birim=BIRIM, taraf="üst (sızdırmaz)", not_="damlama sacı + plaka ↔ dikme"))
            G.KAYNAK.append(S.kaynak_dikisi((x - 11, Y_MEK, pz), (x + 11, Y_MEK, pz), (0, 0, sz), (0, 1.0, 0), 2.0,
                                            ad="kaide_damlama_dikme_kaynagi_%d_%d_b" % (int(x), int(z)), birim=BIRIM, taraf="üst (sızdırmaz)", not_="damlama sacı + plaka ↔ dikme"))
    # AÇICI KOLONU: plakanın altında PEM SP-M8 · damlama sacında Ø9
    for x, z in ACICI_M8:
        ps, c, ms = S.pem_somun("SP", "M8", (x, Y_PLAKA, z), (0, -1.0, 0), pl.t, ad="kaide_ust_plaka_pem_M8_acici_%d_%d" % (int(x), int(-z)), birim=BIRIM)
        Q.delik(x, -z, c["delik"], tip="pem_somun", parca=ps["meta"]["parca"], pem_tip="SP", kenar_min=c["kenar"], min_sac=ms)
        T.delik(x, -z, 9.0, tip="vida_deligi", parca="açıcı kolonu M8 (ISO 273 orta)")
        _eleman(ps)
        _arayuz(S.vida("ISO4762", "M8", 20, (x, Y_MEK + 10.0, z), (0, -1.0, 0), ad="arayuz_acici_kolonu_M8_%d_%d" % (int(x), int(-z)), birim=BIRIM),
                "AÇICI (satın alınan) kolon ayağı", "kolon taban flanşında Ø9 delik (4 köşe, 90 × 125 eksen) · ISO 4762 M8 + DIN 125 → kaide plakasındaki PEM SP-M8",
                "açıcı satın alınırken flanş delik ölçüsü bu eksenlere göre istenir (ya da adaptör plakası)")
    # TABLA RAYI: PEM SP-M6
    for x, z in RAY_M6:
        ps, c, ms = S.pem_somun("SP", "M6", (x, Y_PLAKA, z), (0, -1.0, 0), pl.t, ad="kaide_ust_plaka_pem_M6_ray_%d_%d" % (int(x), int(-z)), birim=BIRIM)
        Q.delik(x, -z, c["delik"], tip="pem_somun", parca=ps["meta"]["parca"], pem_tip="SP", kenar_min=c["kenar"], min_sac=ms)
        T.delik(x, -z, 6.6, tip="vida_deligi", parca="tabla rayı M6 (ISO 273 orta)")
        _eleman(ps)
        _arayuz(S.vida("ISO4762", "M6", 16, (x, Y_MEK + 8.0, z), (0, -1.0, 0), ad="arayuz_tabla_rayi_M6_%d_%d" % (int(x), int(-z)), birim=BIRIM),
                "TOPPING tabla rayı taban sacı (TOPPING_MODUL__sac, dünya x 836–2495)", "ray tabanında Ø6,6 delik · ISO 4762 M6 → kaide plakasındaki PEM SP-M6", "TOPPING sahibi")
    # A → B servis delikleri (plaka Ø16 + damlama Ø16, silikon tapa)
    for x, z in AB_M8:
        Q.delik(x, -z, 16.0, tip="servis_deligi", parca="A→B M8 lokma geçişi")
        T.delik(x, -z, 16.0, tip="servis_deligi", parca="A→B M8 lokma geçişi · gıda sınıfı silikon tapa")
        tp = silindir((x, Y_PLAKA, z), (0, 1.0, 0), 8.0, Y_MEK - Y_PLAKA)
        G.ELEMAN.append(_ozel("kaide_servis_tapasi_%d_%d" % (int(x), int(-z)), tp, "gıda sınıfı silikon (FDA 21 CFR 177.2600)",
                              "Gömme kapama tapası Ø16 delik · başsız, yüzle aynı (ray / açıcı altına da gelir) · silikon", "Ø16,2 × 5,5 (sıkı geçme)", malzeme="VMQ silikon", mal="conta"))
    return pl, tv


def _yan(taraf):
    """sol: x 0–1,5 (n +x) · sağ: x 700–698,5 (n −x) · ön + arka 90° iç dönüş · u = y · v = ±z"""
    ad = "sol_yan_sac" if taraf == "sol" else "sag_yan_sac_tabla_gecisi"
    s = _sac(ad, "dis"); g = s.R + s.t
    if taraf == "sol":
        P = s.taban([(Y_DOLAP, Z_ARKA_IC + g), (Y_UST_ALT, Z_ARKA_IC + g), (Y_UST_ALT, Z_ON - g), (Y_DOLAP, Z_ON - g)], O=(0, 0, 0), ex=(0, 1, 0), ey=(0, 0, 1), ad="yan")
        k_arka, k_on = 0, 2
        zv = lambda z: z
    else:
        P = s.taban([(Y_DOLAP, -Z_ON + g), (Y_UST_ALT, -Z_ON + g), (Y_UST_ALT, -Z_ARKA_IC - g), (Y_DOLAP, -Z_ARKA_IC - g)], O=(W, 0, 0), ex=(0, 1, 0), ey=(0, 0, -1), ad="yan")
        k_arka, k_on = 2, 0
        zv = lambda z: -z
    arka = P.flans(k_arka, 22.0, yon=+1, ad="arka_donus")
    on = P.flans(k_on, 16.5, yon=+1, ad="on_donus")
    G.PANEL[taraf] = dict(yan=P, arka=arka, on=on, s=s, zv=zv)
    if taraf == "sag":
        y0, y1, z0, z1 = TABLA_AGZI
        P.dikdortgen((y0 + y1) / 2.0, zv((z0 + z1) / 2.0), y1 - y0, z1 - z0, r=6.0, tip="tabla_gecis_agzi", parca="A → TOPPING tabla geçiş ağzı (R6 · çapaksız · TOPPING sol sacındaki ağızla eş)")
    return s, P


def ust_sac():
    s = _sac("ust_sac", "dis"); g = s.R + s.t
    P = s.taban([(0.0, -Z_ON + g), (W, -Z_ON + g), (W, -Z_ARKA_IC - g), (0.0, -Z_ARKA_IC - g)], O=(0, Y_UST_ALT, 0), ex=(1, 0, 0), ey=(0, 0, -1), ad="ust")
    on = P.flans(0, Y_UST - Y_HALKA[0] - 10.0, yon=-1, bas=17.0, son=17.0, ad="on_donus")
    arka = P.flans(2, Y_UST - Y_HALKA[0] - 10.0, yon=-1, bas=23.0, son=23.0, ad="arka_donus")
    G.PANEL["ust"] = dict(ust=P, on=on, arka=arka, s=s)
    return s, P


def arka_sac():
    s = _sac("arka_sac", "dis"); g = s.R + s.t
    P = s.taban([(0.0, Y_DOLAP + g), (W, Y_DOLAP + g), (W, Y_UST), (0.0, Y_UST)], O=(0, 0, Z_ARKA), ex=(1, 0, 0), ey=(0, 1, 0), ad="arka")
    alt = P.flans(0, 13.5, yon=+1, bas=23.0, son=23.0, ad="alt_donus")          # B tavanına oturur · kaide arka borusunun 1,5 gerisinde biter
    G.PANEL["arka"] = dict(arka=P, alt=alt, s=s)
    return s, P


def kulak(ad, A, stud, u, v, v_cerceve, L_kaynak=25.0, gen=25.0):
    """3 mm L kulak (h3_k_sac_v1 ile aynı): taban = saplama ayağı (panel iç yüzüne) · flanş = kaynak ayağı (çerçeve yüzüne)"""
    s = _sac(ad, "braket")
    u, v = np.asarray(u, float), np.asarray(v, float)
    t, R = s.t, s.R
    vb = v_cerceve - (R + t)
    va = -9.75
    P = s.taban([(-gen / 2, va), (gen / 2, va), (gen / 2, vb), (-gen / 2, vb)], O=tuple(stud), ex=tuple(u), ey=tuple(v), ad="saplama_ayagi")
    P.flans(2, L_kaynak, yon=+1, ad="kaynak_ayagi")
    n = np.cross(u, v)
    for sg in (+1, -1):
        p0 = np.asarray(stud) + u * sg * gen / 2.0 + v * v_cerceve + n * (R + t)
        p1 = np.asarray(stud) + u * sg * gen / 2.0 + v * v_cerceve + n * L_kaynak
        G.KAYNAK.append(S.kaynak_dikisi(p0, p1, u * sg, -v, min(t, 3.0), ad=ad + "_kaynak_%s" % ("a" if sg > 0 else "b"), birim=BIRIM, taraf="dis (köşe)",
                                        not_="kulak ↔ iskelet"))
    b = S.vidali_birlesim(A, P, tuple(stud), "pem_saplama", ad=ad + "_bag", birim=BIRIM)
    for q in b["parcalar"]: _eleman(q)
    G.BIRLESIM.append(b); G.KULAK.append(s)
    return s, P, b


def kulaklar():
    L = G.PANEL["sol"]["yan"], G.PANEL["sag"]["yan"]
    for A, xs, sx in ((L[0], 1.5, 1.0), (L[1], W - 1.5, -1.0)):
        tr = "sol" if sx > 0 else "sag"
        for y in KULAK_DIKME_Y["on"]:
            kulak("govde_kulak_%s_on_%d" % (tr, int(y)), A, (xs, y, 8.0), (0, 1.0 * sx, 0), (0, 0, 1.0), 19.0)
        for y in KULAK_DIKME_Y["arka"]:
            kulak("govde_kulak_%s_arka_%d" % (tr, int(y)), A, (xs, y, -766.0), (0, -1.0 * sx, 0), (0, 0, -1.0), 19.0)
    U = G.PANEL["ust"]["ust"]
    for x in KULAK_UST["on"]:
        kulak("govde_kulak_ust_on_%d" % int(x), U, (x, Y_UST_ALT, 8.0), (1.0, 0, 0), (0, 0, 1.0), 19.0)
    for x in KULAK_UST["arka"]:
        kulak("govde_kulak_ust_arka_%d" % int(x), U, (x, Y_UST_ALT, -766.0), (-1.0, 0, 0), (0, 0, -1.0), 19.0)


def arka_baglantilari():
    """arka sac: dışarı taşan vida başı YOK (K v1.1 kuralı) → arka saca preslenmiş PEM FHP-M5 (baş dış yüzle aynı), yan sacların arka dönüşlerinde /
    üst sacın arka dönüşünde Ø5,5 · DIN 9021 pul + ISO 10511 somun İÇERİDEN (dikme ↔ arka sac arası 13,5 mm yarıktan SW8)"""
    A = G.PANEL["arka"]["arka"]
    for tr, xx in (("sol", 12.5), ("sag", W - 12.5)):
        B = G.PANEL[tr]["arka"]
        for y in (850.0, 1150.0, 1450.0, 1750.0, 2050.0):
            b = S.vidali_birlesim(A, B, (xx, y, Z_ARKA), "pem_saplama", ad="govde_bag_arka_%s_%d" % (tr, int(y)), birim=BIRIM)
            for q in b["parcalar"]: _eleman(q)
            G.BIRLESIM.append(b)
    B = G.PANEL["ust"]["arka"]
    for x in (60.0, 350.0, 640.0):
        b = S.vidali_birlesim(A, B, (x, Y_UST - 12.0, Z_ARKA), "pem_saplama", ad="govde_bag_arka_ust_%d" % int(x), birim=BIRIM)
        for q in b["parcalar"]: _eleman(q)
        G.BIRLESIM.append(b)


def m8_noktalari():
    """A ↔ TOPPING: 4 × M8 — TOPPING sol duvarı PU'lu soğuk oda (içeriden erişim yok) → cıvata A İÇİNDEN sağ yan sacın Ø9'undan, TOPPING sol dış sacına
    köpüklemeden önce preslenmiş PEM SP-M8 somuna (ARAYÜZ) · A → B: kaide borusunun alt duvarından M8 × 25 (B üst kirişinde perçin somun = ARAYÜZ)"""
    out = []
    A = G.PANEL["sag"]["yan"]
    for y, z in M8_T:
        A.delik(y, -z, 9.0, tip="vida_deligi", parca="A↔TOPPING M8 (ISO 273 orta)")
        rs, c, ms = S.pem_somun("SP", "M8", (W + 1.5, y, z), (1.0, 0, 0), 1.5, ad="arayuz_m8_T_%d_%d_pem" % (int(y), int(-z)), birim=BIRIM)
        _arayuz(rs, "TOPPING sol dış sacı (1,5 · PU'lu soğuk oda duvarı)", "TOPPING dış sacında Ø%.2f delik + PEM SP-M8 somun (gövde PU tarafında, dış yüz düz · köpüklemeden ÖNCE köpük kapağı takılır) dünya x 1436 y %.0f z %.0f" % (c["delik"], y, z),
                "TOPPING sahibi")
        pu = S.pul("DIN9021", "M8", (W - 1.5, y, z), (-1.0, 0, 0), ad="arayuz_m8_T_%d_%d_pul" % (int(y), int(-z)), birim=BIRIM)
        vd = S.vida("ISO4762", "M8", 16, (W - 1.5 - 2.0, y, z), (1.0, 0, 0), ad="arayuz_m8_T_%d_%d" % (int(y), int(-z)), birim=BIRIM)
        _arayuz(pu, "A sağ yan sacı iç yüzü", "DIN 9021 M8 (A içinden)", "")
        _arayuz(vd, "A sağ yan sacı → TOPPING perçin somunu", "ISO 4762 M8 × 16 A2-70 · A içinden alyan 6", "")
        out.append(dict(taraf="TOPPING", yer="sag_yan_sac", y=y, z=z, dunya=[W + X_A, y, z]))
    for x, z in AB_M8:
        yk = Y_DOLAP + KT                                                                  # kaide borusu alt duvarının iç yüzü (790)
        pu = S.pul("DIN9021", "M8", (x, yk, z), (0, 1.0, 0), ad="arayuz_ab_%d_%d_pul" % (int(x), int(-z)), birim=BIRIM)
        vd = S.vida("ISO4762", "M8", 25, (x, yk + 2.0, z), (0, -1.0, 0), ad="arayuz_ab_%d_%d" % (int(x), int(-z)), birim=BIRIM)
        _arayuz(pu, "B_MODULER üst kiriş + B dış tavan sacı", "", "")
        _arayuz(vd, "B_MODULER üst kiriş + B dış tavan sacı",
                "B: üst kiriş üst duvarına M8 kapalı uçlu perçin somun (köpüklemeden ÖNCE) dünya x %.1f z %.0f · GFRP pedde + dış tavan sacında Ø9 · ISO 4762 M8 × 25 + DIN 9021" % (x + X_A, z),
                "plaka, damlama sacı ve boru üst duvarındaki Ø16'dan alyan (6) ile · servis tapası sonra takılır")
        out.append(dict(taraf="B", yer="kaide_borusu", y=Y_DOLAP, z=z, dunya=[x + X_A, Y_DOLAP, z]))
    G.M8 = out


def kapak():
    """çift cidarlı tek kapak (h3_k_sac_v1.kapak ile aynı kurgu) · dış tava 1,5 · iç tava 1,0 · 3 gizli menteşe · 3 bas-aç"""
    x0, x1 = KAPAK_X; y0, y1 = KAPAK_Y
    kd = _sac("onyuz_kapak_A", "kapak_dis", mal="on_seffaf"); g = kd.R + kd.t
    D = kd.taban([(x0 + g, y0 + g), (x1 - g, y0 + g), (x1 - g, y1 - g), (x0 + g, y1 - g)], O=(0, 0, Z_KAPAK - kd.t), ex=(1, 0, 0), ey=(0, 1, 0), ad="on_yuz")
    fa = [D.flans(i, Z_KAPAK - Z_ON, yon=-1, ad=a) for i, a in enumerate(("alt_donus", "sag_donus", "ust_donus", "sol_donus"))]
    kd.kose(fa[0], fa[1], "bindirme", ustte=fa[0]); kd.kose(fa[1], fa[2], "bindirme", ustte=fa[2])
    kd.kose(fa[2], fa[3], "bindirme", ustte=fa[2]); kd.kose(fa[3], fa[0], "bindirme", ustte=fa[0])
    ki = _sac("onyuz_kapak_A_ic_tava", "kapak_ic", mal="on_seffaf"); gi = ki.R + ki.t
    b = S.STD.kapak()["ic_dis_bosluk"]
    xi0, xi1, yi0, yi1 = x0 + kd.t + b, x1 - kd.t - b, y0 + kd.t + b, y1 - kd.t - b
    I = ki.taban([(xi0 + gi, yi0 + gi), (xi1 - gi, yi0 + gi), (xi1 - gi, yi1 - gi), (xi0 + gi, yi1 - gi)], O=(0, 0, Z_ON), ex=(1, 0, 0), ey=(0, 1, 0), ad="ic_tava")
    fi = [I.flans(i, S.STD.kapak()["ic_donus"], yon=+1, ad=a) for i, a in enumerate(("alt_donus", "sag_donus", "ust_donus", "sol_donus"))]
    for i in range(4): ki.kose(fi[i], fi[(i + 1) % 4], "acik")
    zp = Z_ON + 1.0 + 7.5
    nok = [(x, yi0 - b / 2.0, zp) for x in np.arange(60, 680, 120)] + [(x, yi1 + b / 2.0, zp) for x in np.arange(60, 680, 120)]
    nok += [(xi0 - b / 2.0, y, zp) for y in np.arange(860, 2190, 160)] + [(xi1 + b / 2.0, y, zp) for y in np.arange(860, 2190, 160)]
    ki.punta(kd, nok, not_="iç tava dönüşleri → dış tava dönüşleri (0,5 boşluk elektrotla kapanır) · ≈ 150 aralık")
    # iç tava takviyesi (700 genişlik: dikey omega yerine iki yatay Z takviye — dış tavaya punta · çarpılma / sehim)
    G.PANEL["kapak"] = dict(dis=D, ic=I, kd=kd, ki=ki)
    # menteşeler (sol ön dikme içi) — Southco R6 / EMKA 1046 sınıfı gizli 180° kaldır-çıkar (ölçüler TEMSİLİ, katalogdan doğrulanacak)
    dk = G.PROF["kose_dikmesi_20_42"]
    for i, yh in enumerate(MENTESE_Y):
        dk.duvar_pencere("+z", yh, 23.75 - PX[0], 52.0, 13.0, tip="mentese_penceresi", not_="gizli menteşe gövdesi")
        for dy in (-15.0, 15.0):
            dk.duvar_delik("+x", yh + dy, 44.0 - PZ[0], 5.5, tip="mentese_vidasi", not_="menteşe gövdesi 2 × M5")
        gov = kutu(17.5, 30.0, yh - 25, yh + 25, 31.0, 57.0)
        for dy in (-15.0, 15.0):
            gov = gov.cut(silindir((22.0, yh + dy, 44.0), (1.0, 0, 0), 2.5, 9.0))
        G.ELEMAN.append(_ozel("onyuz_kapak_A_mentese_%d_sabit" % i, gov, "Southco R6 / EMKA 1046 sınıfı", "Gizli 180° kaldır-çıkar menteşe · GÖVDE yarısı (dikme içine gömülü) AISI 316",
                              "13 × 50 × 26 · 2 × M5 (dikme iç yan duvarından)", malzeme="AISI 316 pasive", mal="celik", meta=dict(kaldir_cikar=True, aci=180, pivot=[KAPAK_X[0], Z_KAPAK])))
        for dy in (-15.0, 15.0):
            _eleman(S.vida("ISO7380", "M5", 12, (35.0, yh + dy, 44.0), (-1.0, 0, 0), ad="onyuz_kapak_A_mentese_%d_sabit_vida_%s" % (i, "a" if dy < 0 else "b"), birim=BIRIM))
        pl = kutu(17.0, 48.0, yh - 30, yh + 30, Z_ON - 1.5, Z_ON)
        for dy in (-20.0, 20.0):
            pl = pl.cut(silindir((42.0, yh + dy, Z_ON - 2.0), (0, 0, 1.0), 2.75, 3.0))
        kanat = _bir(pl, kutu(18.0, 30.0, yh - 25, yh + 25, Z_ON, Z_ON + 11.0), kutu(20.0, 28.0, yh - 18, yh + 18, 57.0, Z_ON - 1.5))
        G.ELEMAN.append(_ozel("onyuz_kapak_A_mentese_%d_kanat" % i, kanat, "Southco R6 / EMKA 1046 sınıfı", "Gizli 180° kaldır-çıkar menteşe · KANAT yarısı + kol (kapakla döner)",
                              "plaka 31 × 60 × 1,5 + cep 12 × 50 × 11", malzeme="AISI 316 pasive", mal="celik", meta=dict(kapakla_doner=True)))
        I.dikdortgen(24.25, yh, 13.0, 51.0, tip="mentese_cebi", parca="menteşe kanat cebi (kol geçişi)")
        for dy in (-20.0, 20.0):
            ps, c, ms = S.pem_somun("SP", "M5", (42.0, yh + dy, Z_ON + ki.t), (0, 0, 1.0), ki.t, ad="onyuz_kapak_A_mentese_%d_pem_%s" % (i, "a" if dy < 0 else "b"), birim=BIRIM)
            ps["meta"]["kapakla_doner"] = True
            I.delik(42.0, yh + dy, c["delik"], tip="pem_somun", parca=ps["meta"]["parca"], pem_tip="SP", kenar_min=c["kenar"], min_sac=ms)
            _eleman(ps)
            vd = S.vida("ISO7380", "M5", 6, (42.0, yh + dy, Z_ON - 1.5), (0, 0, 1.0), ad="onyuz_kapak_A_mentese_%d_kanat_vida_%s" % (i, "a" if dy < 0 else "b"), birim=BIRIM)
            vd["meta"]["kapakla_doner"] = True
            _eleman(vd)
    # bas-aç (sağ ön dikme içi) — Southco 97 / EMKA 1080 sınıfı
    dr = G.PROF["kose_dikmesi_680_42"]
    for i, yb in enumerate(BASAC_Y):
        dr.duvar_delik("+z", yb, BASAC_X - PX[1], 12.2, tip="basac_deligi", not_="bas-aç gövdesi (geçme)")
        sh = silindir((BASAC_X, yb, 31.0), (0, 0, 1.0), 6.0, 26.0).fuse(silindir((BASAC_X, yb, 57.0), (0, 0, 1.0), 7.0, 1.0)).fuse(silindir((BASAC_X, yb, 58.0), (0, 0, 1.0), 3.0, 1.0))
        G.ELEMAN.append(_ozel("onyuz_kapak_A_basac_%d" % i, sh, "Southco 97 / EMKA 1080 sınıfı", "Bas-aç mandalı (push-to-open, geçme gövde Ø12 · O-ring) — dikme ön yüzünde Ø12,2",
                              "Ø12 × 26 · baş Ø14 × 1 · strok 7", malzeme="AISI 316 / POM", mal="siyah"))
        dp = _sac("onyuz_kapak_A_karsilik_%d" % i, "dis", mal="on_seffaf")
        dp.taban([(BASAC_X - 12, yb - 20), (BASAC_X + 12, yb - 20), (BASAC_X + 12, yb + 20), (BASAC_X - 12, yb + 20)], O=(0, 0, Z_ON + ki.t), ex=(1, 0, 0), ey=(0, 1, 0), ad="plaka")
        dp.punta(ki, [(BASAC_X - 7, yb - 13, Z_ON + ki.t), (BASAC_X + 7, yb + 13, Z_ON + ki.t)], not_="karşılık takviyesi → iç tava (kapak kapanmadan önce)")
    return kd, ki


def kur(log=print):
    if G.kuruldu: return G
    t0 = time.time()
    for a in ("SAC", "PROFIL", "ELEMAN", "KAYNAK", "BIRLESIM", "ARAYUZ", "KULAK", "NOT", "M8"): setattr(G, a, [])
    G.PANEL, G.PROF = {}, {}
    kaide(); iskelet(); plaka_ve_tava()
    _yan("sol"); _yan("sag"); ust_sac(); arka_sac()
    kulaklar(); arka_baglantilari(); m8_noktalari(); kapak()
    G.PROFIL = list(G.PROF.values())
    G.kuruldu = True
    log("%s · kuruldu: %d sac · %d profil · %d eleman · %d kaynak · %d birleşim · %d arayüz · %.1f sn" % (SURUM, len(G.SAC), len(G.PROFIL), len(G.ELEMAN), len(G.KAYNAK),
                                                                                                    len(G.BIRLESIM), len(G.ARAYUZ), time.time() - t0))
    return G


# =====================================================================================================================================
# 3 · SÖZLEŞME (parça listesi · yerel) + dünya
# =====================================================================================================================================
def kapakla_doner(ad):
    return ad.startswith("onyuz_kapak_A") and not re.search(r"mentese_\d+_sabit|basac_\d+$", ad)


def _mal(p):
    ad = p["ad"]
    if kapakla_doner(ad): return "on_seffaf"
    if p.get("tur") == "sac":
        return "kabuk" if ad in ("sol_yan_sac", "sag_yan_sac_tabla_gecisi", "arka_sac", "ust_sac") else "sac"
    if p.get("tur") in ("profil", "kaynak"): return "sac"
    return p.get("mal") if p.get("mal") in ("celik", "conta", "siyah", "sac", "kabuk") else "celik"


def govde_parcalari():
    """gövde parçaları (arayüz elemanları HARİÇ) · A yereli"""
    kur()
    L = []
    for s in G.SAC: L += s.parcalar()
    L += [p.parca() for p in G.PROFIL] + G.ELEMAN + G.KAYNAK
    out = []
    for p in L:
        sh = p.get("sh") if p.get("sh") is not None else p["wp"].val()
        q = dict(ad=p["ad"], wp=cq.Workplane("XY").add(sh), sh=sh, mal=_mal(p), grup="SABIT", bom=tuple(p["bom"]) if p.get("bom") else None, kaynak=SURUM,
                 birim=BIRIM, tur=p.get("tur", "sac"))
        if p.get("sac"): q["sac"] = p["sac"]
        if p.get("meta"): q["meta"] = p["meta"]
        out.append(q)
    adlar = [q["ad"] for q in out]
    assert len(adlar) == len(set(adlar)), "çift ad: %s" % sorted(a for a in set(adlar) if adlar.count(a) > 1)
    return out


ZARF = (0.0, 700.0, 788.0, 2200.0, -830.0, 79.0)                        # A yereli (dünya x 736–1436) · bugünkü A + A_ONYUZ zarfı


def dunya(sh):
    return sh.translate(V(X_A, 0, 0))


def dunya_listesi(L):
    out = []
    for p in L:
        q = dict(p); s = p.get("sh") if p.get("sh") is not None else p["wp"].val()
        q["sh"] = dunya(s); q["wp"] = cq.Workplane("XY").add(q["sh"]); out.append(q)
    return out


if __name__ == "__main__":
    kur()
    L = govde_parcalari()
    print(len(L), "parça")
    sys.stdout.flush(); os._exit(0)
