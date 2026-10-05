# -*- coding: utf-8 -*-
"""h3_k_sac_v1 — K (KESME + SPREY) İSTASYONU GÖVDESİ · ÜRETİM SACI PİLOTU v1 (2 Eki 2026 · Claude · YEREL · TASLAK, montaja bağlı DEĞİL)

Kemal: "gövdede tam çalışma; eğim/büküm gerçek; sanayi mutfaklarında nasıl kuruluyorsa öyle; nereden bükülür, vida nereye atılır, boşluk nerede açılır;
vidasına kadar ama mantıklı; sanayi tipi mutfakçıya verdiğimde direkt üretsin." · Büküm/kesim paftası YOK, önce 3B (açınım JSON'ları ayrıca).

KAYNAKLAR: h3_sac_v1 (sac kütüphanesi) · sac_kararlar_v1.json > sac_standart_v1.json · K'nın mevcut gövdesi (h3_kesme_v1 → kesme_cad_v11) ·
           v3.7 tek kapak ölçüsü h3_kapak_v1.K_X × (788, 2197) · elektrik delikleri h3/_elk (KS ust_sac Harting · KS sol_sac G4 rakoru).
KOORDİNAT: K YERELİ (h3_kesme_v1 ile aynı: x 0…400, dünya = x + 4000 · y yerden · z ön +79 / arka −830). Bütün PARÇALAR KS.PARCALAR sözleşmesinde (wp yerel).

KURGU (atölye mantığı)
  1 · İSKELET = KAYNAKLI ALT MONTAJ (tek parça gelir): 304 kare boru 30 × 30 × 2 (mevcut ölçü — köprü kirişleri K_KESICI dikmeler arasına 812 mm açıklıkla
      oturduğu için 40'lık profile geçilmedi, rapor: sapma) · 4 dikme + alt / orta / üst kuşak (ön + arka) + alt ve orta yan kuşak (orta yan kuşak YENİ: istasyon
      tabanını 4 kenardan taşır, 3 mm taban 812 mm açıklıkta ≈ 9 mm sehim yapıyordu) · dikme başlarında 2 mm tapa · 3 mm taban sacı (788–791) altta, 3 mm
      istasyon tabanı (892–895) orta kuşaklara DELİK KAYNAĞIYLA (yüz taşlanır) · dikmelerin çevresi taban üstünde köşe kaynağıyla kapalı (yağ damlası alta inmez) ·
      panel kulakları (3 mm L) iskelete kaynaklı · köprü yan kirişlerinin uçları dikmelere kaynaklı (K_KESICI parçası, ölçüsü değişmez).
  2 · SÖKÜLEBİLİR PANELLER (servis): sol / sağ yan 1,5 (ön + arka 90° dönüş) → kulaklara PEM FHP-M5 saplama + pul + fiberli somun (dışta iz yok: yan yüzler
      komşu istasyonların sacıyla yüz yüze) · üst sac 1,5 (ön + arka aşağı dönüş) → üst kuşak kulaklarına FHP-M5 (üstte görünür vida yok) · arka sac 1,5 (alt dönüş)
      → arka saca preslenmiş FHP-M5 saplamalar yan panellerin arka dönüşlerinden ve üst sacın arka dönüşünden geçer, pul + somun içeriden
      (v1.1: arka düzlem z −830 Kemal kuralı — dışarı taşan vida başı yok; ISO 7380 başları −832,6'ya taşıyordu).
  ZARF (montaj K_GOVDE denetimi): bütün gövde parçaları x 0–400 (dünya 4000–4400) · y −1…2201 · z −831…80 içinde — öz denetimde de var.
  3 · TEK ÖN KAPAK (v3.7 ölçüsü 4003–4398 × 788–2197): çift cidar (dış tava 1,5 · iç tava 1,0, punta) · köşeler bindirme + TIG · 3 gizli 180° kaldır-çıkar
      menteşe (gövde yarısı sol ön dikmenin içinde, sanal pivot ön-sol köşe x 4003 · z 79) · 3 bas-aç (sağ ön dikmenin içinde) · KULP YOK.
  4 · BAĞLANTI NOKTALARI (K tarafı hazır, karşı taraf ARAYÜZ listesinde): K→B 2 × M8 (sol alt yan kuşaktan B tasiyici_capraz_2'ye) · K↔F 4 × M8 · K↔E 3 × M8
      (dikme / orta kuşak dış duvarında M8 perçin somun + 2 mm ara pul) · mekanizma ayakları için istasyon tabanında 8 × PEM SP-M6.
ARAYÜZLER DEĞİŞMEZ: dış ölçüler 0–400 × 788–1862 × −830…+59 · kapak +59…+79 · 788 / 892 / 1862 kotları · bütün açıklıklar ve delikler (ürün girişi, E penceresi,
  hava girişi, yağ hortumları, G4 rakoru, Harting kesiği) · mekanizma parçalarına dokunulmaz.
Çalıştır (öz denetim + çıktılar <scratchpad>/sac_pilot_K): python -u h3_k_sac_v1.py"""
import math, os, sys, json, time, re
H3 = os.path.dirname(os.path.abspath(__file__)); _U = os.path.dirname(H3)
for _p in (_U, H3):
    if _p not in sys.path: sys.path.insert(0, _p)
import numpy as np
import cadquery as cq
import h3_sac_v1 as S

SURUM = "h3_k_sac_v1"
V = cq.Vector
X_K = 4000.0
# ---------------------------------------------------------------- ARAYÜZ (K yereli · değişmez) ----------------------------------------------------------------
W = 400.0
Y_DOLAP, Y_TABAN, Y_MEK, Y_MEK_UST, Y_UST_ALT, Y_UST = 788.0, 791.0, 892.0, 895.0, 1860.5, 1862.0
Z_ON, Z_KAPAK, Z_ARKA, Z_ARKA_IC = 59.0, 79.0, -830.0, -828.5
KAPAK_X, KAPAK_Y = (3.0, 398.0), (788.0, 2197.0)                       # v3.7 h3_kapak_v1.K_X (4003–4398) − X_K · 788–2197
URUN_GIRISI = (932.0, 1072.0, -420.0, -8.0)                            # sol sac (y0, y1, z0, z1) · F→K
E_PENCERE = (978.0, 1062.0, -372.0, -24.0)                             # sağ sac · K→E
DELIK_SOL = [("hava_giris_rakoru", 1809.0, -770.0, 14.0), ("yag_emis_gecisi", 1828.0, -250.0, 14.0), ("yag_donus_gecisi", 1828.0, -180.0, 12.0),
             ("G4_tarti_FK_duvari_rakoru", 1387.0, -296.0, 16.5)]      # (ad, y, z, Ø) — K11 / h3_kesme_v1 / h3_elk (KS sol_sac_urun_girisi)
HARTING = (267.0, 333.0, -778.0, -742.0)                               # üst sac kesiği (x0, x1, z0, z1) — h3_elk KS ust_sac 'K Harting Han 10B soket kesiği'
PANO_BURC = [(80.0, 1482.0), (320.0, 1482.0), (80.0, 1847.0), (320.0, 1847.0)]   # arka sac: pano_ara_burcu eksenleri (x, y)
# ---------------------------------------------------------------- iskelet ----------------------------------------------------------------
PB, PT, PRO = 30.0, 2.0, 4.0                                           # 30 × 30 × 2 · dış köşe R = 2t (EN 10219 / soğuk çekme 304)
PX, PZ = (20.0, 380.0), (42.0, -800.0)                                 # dikme eksenleri
Y_KUSAK = dict(alt=(791.0, 821.0), orta=(862.0, 892.0), ust=(1830.5, 1860.5))
Y_DIKME = (791.0, 1856.5)                                              # + 2 mm tapa → 1858.5 (üst sacın ön/arka büküm R'sine girmez · üst sac kuşaklara oturur)
KOPRU_Y = (1419.5, 1459.5)                                             # köprü yan kirişi (K_KESICI · 30 × 40 × 2) · dikmelere kaynak
# kapak donanımı
MENTESE_Y = (950.0, 1360.0, 1750.0)                                    # sol ön dikme (v3.7 taslağında 900 · 950: orta ön kuşağın kaynağından uzak)
BASAC_Y = (1000.0, 1430.0, 1800.0)                                     # sağ ön dikme
BASAC_X = 376.0
# panel kulakları (K yereli) — (taraf, çerçeve, y ya da z)
KULAK_DIKME_Y = dict(on=(841.5, 1150.0, 1600.0, 1810.0), arka_sol=(841.5, 1150.0, 1600.0, 1720.0), arka_sag=(841.5, 1150.0, 1600.0, 1810.0))   # 841,5: alt ve orta yan kuşak kaynakları arası
KULAK_ORTA_Z = (-680.0, -350.0, -20.0)
KULAK_UST = dict(on=(80.0, 320.0), arka=(80.0, 200.0))
# bağlantı noktaları
M8_F = [("arka_dikme", 1000.0, -800.0), ("arka_dikme", 1825.0, -800.0), ("on_dikme", 1700.0, 42.0), ("orta_kusak", 877.0, -720.0)]
M8_E = [("arka_dikme", 1100.0, -800.0), ("arka_dikme", 1750.0, -800.0), ("orta_kusak", 877.0, -100.0)]
KB_X, KB_Z = 16.5, (-480.0, -570.0)                                    # K → B (B tasiyici_capraz_2 x −4…26 · z −600…−130 · üst yüzü 786,5)
PEM_M6 = [(65.0, -421.0, "bant_ayagi_65_-421"), (65.0, -3.0, "bant_ayagi_65_-3"), (335.0, -421.0, "bant_ayagi_335_-421"), (335.0, -3.0, "bant_ayagi_335_-3")]   # ayak ekseni (alttan dişli tapa · arayüz)
PEM_M5_ITICI = [(54.0, -741.0, "itici_taban_40_-755"), (54.0, -769.0, "itici_taban_40_-755"), (54.0, -631.0, "itici_taban_40_-645"), (54.0, -659.0, "itici_taban_40_-645"),
                (346.0, -741.0, "itici_taban_360_-755"), (346.0, -769.0, "itici_taban_360_-755"), (346.0, -631.0, "itici_taban_360_-645"), (346.0, -659.0, "itici_taban_360_-645")]   # 36 × 36 ayak tabanının dış köşeleri (20 × 20 eksen ayağının dışında)
KOSEBENT_Z = (-580.0, -517.0, -455.0)                                  # yağ pompa rafı köşebentleri (yan saca 3 × M5 · y 1625)
BIRIM = "K_GOVDE"
ESKI_GOVDE = ("kose_dikmesi_20_-800", "kose_dikmesi_20_42", "kose_dikmesi_380_-800", "kose_dikmesi_380_42", "onyuz_kayit_140_-800", "onyuz_kayit_140_42",
              "onyuz_kayit_877_-800", "onyuz_kayit_877_42", "onyuz_kayit_1840_-800", "onyuz_kayit_1840_42", "taban_sac_tasiyici_20", "taban_sac_tasiyici_380",
              "taban_sac_3", "istasyon_tabani_3", "arka_sac", "ust_sac", "sol_sac_urun_girisi", "sag_sac_E_penceresi", "onyuz_kapak_alt", "onyuz_kapak_orta",
              "onyuz_kapak_ust")
# GLB / görünüm malzemesi (montajdaki K malzemeleriyle aynı adlar)
S._RENK.update({"profil": ((0.70, 0.73, 0.77, 1.0), 0.85, 0.30), "mekanizma": ((0.42, 0.46, 0.52, 1.0), 0.4, 0.5), "arayuz": ((0.90, 0.22, 0.15, 1.0), 0.3, 0.5),
                "kapak": ((0.70, 0.82, 0.95, 1.0), 0.2, 0.25)})


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
# 1 · KARE PROFİL (gerçek dış R'li) + duvar kesikleri + kesim listesi
# =====================================================================================================================================
EKSEN = {"x": np.array([1.0, 0, 0]), "y": np.array([0, 1.0, 0]), "z": np.array([0, 0, 1.0])}


class Profil:
    """304 kare boru 30 × 30 × 2 · eksen boyunca a0 → a1 · c = (dik eksenlerdeki merkez): x için (y, z) · y için (x, z) · z için (x, y)"""
    def __init__(self, ad, eksen, a0, a1, c, b=PB, t=PT, Ro=PRO, not_=""):
        self.ad, self.eksen, self.a0, self.a1, self.c, self.b, self.t, self.Ro, self.not_ = ad, eksen, float(a0), float(a1), tuple(map(float, c)), b, t, Ro, not_
        self.kesikler, self.uc_kaynak = [], []
        self._sh = None

    def merkez(self, a):
        p = np.zeros(3); p[ "xyz".index(self.eksen)] = a
        dik = [k for k in "xyz" if k != self.eksen]
        p["xyz".index(dik[0])], p["xyz".index(dik[1])] = self.c
        return p

    def _govde(self):
        dis = S.yuz_dikd_r(0.0, 0.0, self.b, self.b, 0.0, self.Ro)
        ic = S.yuz_dikd_r(0.0, 0.0, self.b - 2 * self.t, self.b - 2 * self.t, 0.0, self.Ro - self.t)
        sh = S._prizma(dis.cut(ic), self.a1 - self.a0)
        dik = [k for k in "xyz" if k != self.eksen]
        ex, ey, ez = EKSEN[dik[0]], EKSEN[dik[1]], EKSEN[self.eksen]
        if np.linalg.det(np.column_stack([ex, ey, ez])) < 0: ey = -ey
        return S._tasi(sh, S._M(np.column_stack([ex, ey, ez]), self.merkez(self.a0)))

    def duvar_delik(self, yuz, a, kayma, cap, tip="delik", not_=""):
        """yuz: '+x' / '-x' / '+y' / '-y' / '+z' / '-z' (dış normal) · a: eksen boyunca konum · kayma: duvarın düzleminde, eksene dik ikinci eksen yönünde merkezden"""
        n = EKSEN[yuz[1]] * (1 if yuz[0] == "+" else -1)
        dik = [k for k in "xyz" if k not in (self.eksen, yuz[1])][0]
        p = self.merkez(a) + n * (self.b / 2.0 + 1.0) + EKSEN[dik] * kayma
        cut = silindir(p, -n, cap / 2.0, self.t + 1.6)
        self.kesikler.append(dict(sh=cut, tip=tip, yuz=yuz, a=round(a - self.a0, 2), kayma=kayma, cap=cap, not_=not_)); self._sh = None
        return cut

    def duvar_pencere(self, yuz, a, kayma, la, lk, r=1.0, tip="pencere", not_=""):
        """dikdörtgen pencere: eksen boyunca la · dik yönde lk · yalnız o duvar (iç yüzden 0,6 içeri)"""
        sg = 1.0 if yuz[0] == "+" else -1.0
        dik = [k for k in "xyz" if k not in (self.eksen, yuz[1])][0]
        c = self.merkez(a)
        lo, hi = np.zeros(3), np.zeros(3)
        for i, k in enumerate("xyz"):
            if k == self.eksen: lo[i], hi[i] = a - la / 2.0, a + la / 2.0
            elif k == dik: lo[i], hi[i] = c[i] + kayma - lk / 2.0, c[i] + kayma + lk / 2.0
            else:
                d0, d1 = c[i] + sg * (self.b / 2.0 - self.t - 0.6), c[i] + sg * (self.b / 2.0 + 1.0)
                lo[i], hi[i] = min(d0, d1), max(d0, d1)
        cut = kutu(lo[0], hi[0], lo[1], hi[1], lo[2], hi[2])
        self.kesikler.append(dict(sh=cut, tip=tip, yuz=yuz, a=round(a - self.a0, 2), kayma=kayma, olcu=[la, lk], not_=not_)); self._sh = None
        return cut

    def kati(self):
        if self._sh is None:
            sh = self._govde()
            for k in self.kesikler: sh = sh.cut(k["sh"])
            self._sh = sh.clean()
        return self._sh

    def dfm(self):
        """profil DFM: kesik düz yüz içinde mi (köşe R'sine taşmaz) · uçtan / kaynaklı birleşim bölgesinden uzaklık"""
        out = []
        duz = self.b / 2.0 - self.Ro
        L = self.a1 - self.a0
        for k in self.kesikler:
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
        kes = [dict({k: v for k, v in x.items() if k != "sh"}) for x in self.kesikler]
        return dict(ad=self.ad, wp=cq.Workplane("XY").add(sh), sh=sh, mal="sac", birim=BIRIM, grup="SABIT", kaynak=SURUM, tur="profil",
                    bom=("Kare boru AISI 304 %g × %g × %g (EN 10217-7 / ASTM A554 · dış R %g) · %s" % (self.b, self.b, self.t, self.Ro, self.not_), 1, "L %.1f" % L,
                         "boru lazer / şerit testere 90° · %d kesik · %.2f kg" % (len(kes), kg), "ÜRETİM"),
                    meta=dict(tur="profil", eksen=self.eksen, L=round(L, 2), kesit=[self.b, self.b, self.t, self.Ro], kesikler=kes, kg=round(kg, 3)))


def uc_kaynaklari(ad, nokta, yon_ray, yuzler, b=PB, a=PT, flat=None):
    """kuşak ucu ↔ dikme yüzü köşe kaynakları · nokta: birleşim düzleminde kuşak ekseni · yon_ray: kuşak boyunca dikmeden uzağa · yuzler: içbükey köşe olan yan yüz normalleri"""
    flat = flat if flat is not None else b - 2 * PRO
    e = np.asarray(yon_ray, float); out = []
    for i, nf in enumerate(yuzler):
        nf = np.asarray(nf, float); w = np.cross(e, nf)
        p = np.asarray(nokta, float) + nf * (b / 2.0)
        out.append(S.kaynak_dikisi(p - w * flat / 2.0, p + w * flat / 2.0, e, nf, a, ad="%s_%d" % (ad, i), birim=BIRIM, taraf="dis (köşe)",
                                   not_="kuşak ucu ↔ dikme · TIG 141 · ER308LSi"))
    return out


# =====================================================================================================================================
# 2 · KUR
# =====================================================================================================================================
class G:
    """kurulan her şey (modül düzeyinde tek örnek)"""
    SAC, PROFIL, ELEMAN, KAYNAK, BIRLESIM, ARAYUZ, KULAK = [], [], [], [], [], [], []
    PANEL, NOT, ESLEME = {}, [], {}
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


def iskelet():
    """kaynaklı alt montaj: dikmeler + kuşaklar + tapalar + kovanlar + kaynaklar"""
    P = {}
    y0, y1 = Y_DIKME
    for x in PX:
        for z in PZ:
            ad = "kose_dikmesi_%d_%d" % (int(x), int(z))
            P[ad] = Profil(ad, "y", y0, y1, (x, z), not_="köşe dikmesi (kaynaklı iskelet)")
    for ky, (ya, yb) in Y_KUSAK.items():
        for z in PZ:
            ad = "onyuz_kayit_%s_%d" % ({"alt": "140", "orta": "877", "ust": "1840"}[ky], int(z))
            P[ad] = Profil(ad, "x", PX[0] + PB / 2, PX[1] - PB / 2, ((ya + yb) / 2.0, z), not_="%s %s kuşak" % ("ön" if z > 0 else "arka", ky))
    for x in PX:
        for ky, onek in (("alt", "taban_sac_tasiyici_"), ("orta", "istasyon_tabani_tasiyici_")):
            ya, yb = Y_KUSAK[ky]
            P[onek + "%d" % int(x)] = Profil(onek + "%d" % int(x), "z", PZ[1] + PB / 2, PZ[0] - PB / 2, (x, (ya + yb) / 2.0),
                                             not_="%s yan kuşak" % ("alt" if ky == "alt" else "orta (YENİ · istasyon tabanı taşıyıcı)"))
    G.PROF = P
    # --- birleşim bölgeleri (profil DFM için) ve uç kaynakları
    K = G.KAYNAK
    ky = Y_KUSAK
    for x, sx in ((PX[0], +1), (PX[1], -1)):
        for z in PZ:
            dk = P["kose_dikmesi_%d_%d" % (int(x), int(z))]
            for kk, (ya, yb) in ky.items():
                dk.uc_kaynak.append(("+x" if sx > 0 else "-x", ya - y0, yb - y0))           # ön / arka kuşak bu yüze kaynaklı
                dk.uc_kaynak.append(("-z" if z > 0 else "+z", ya - y0, yb - y0) if kk != "ust" else ("-z" if z > 0 else "+z", -1e9, -1e9))
            dk.uc_kaynak.append(("-z" if z > 0 else "+z", KOPRU_Y[0] - y0, KOPRU_Y[1] - y0))
    # ön / arka kuşak uçları (dikmenin iç yan yüzüne): içbükey köşe yalnız üst / alt yüzde (z yüzleri dikmeyle aynı düzlem → alın kaynağı, taşlanır)
    for kk, (ya, yb) in ky.items():
        yc = (ya + yb) / 2.0
        yz = [(0, 1.0, 0)] if kk == "alt" else [(0, -1.0, 0)]                          # orta: üstü istasyon tabanının altında (alın dikişi, taşlanır) · üst: üst sac oturur
        for z in PZ:
            for x, e in ((PX[0] + PB / 2, (1.0, 0, 0)), (PX[1] - PB / 2, (-1.0, 0, 0))):
                K += uc_kaynaklari("onyuz_kayit_kaynak_%s_%d_%d" % (kk, int(z), int(x)), (x, yc, z), e, yz)
    # yan kuşak uçları (dikmenin ön/arka yüzüne)
    for kk in ("alt", "orta"):
        ya, yb = ky[kk]; yc = (ya + yb) / 2.0
        yz = [(0, 1.0, 0)] if kk == "alt" else [(0, -1.0, 0)]
        for x in PX:
            for z, e in ((PZ[0] - PB / 2, (0, 0, -1.0)), (PZ[1] + PB / 2, (0, 0, 1.0))):
                K += uc_kaynaklari("%s_kaynak_%d_%d" % ("taban_sac_tasiyici" if kk == "alt" else "istasyon_tabani_tasiyici", int(x), int(z)), (x, yc, z), e, yz)
    # köprü yan kirişi uçları (K_KESICI · 30 (x) × 40 (y) · üst + alt yüz)
    for x in PX:
        for z, e in ((PZ[0] - PB / 2, (0, 0, -1.0)), (PZ[1] + PB / 2, (0, 0, 1.0))):
            K += uc_kaynaklari("kose_dikmesi_kopru_kaynagi_%d_%d" % (int(x), int(z)), (x, (KOPRU_Y[0] + KOPRU_Y[1]) / 2.0, z), e, [(0, 1.0, 0), (0, -1.0, 0)], b=40.0,
                               flat=PB - 2 * PRO)
    # dikme tapaları (2 mm · dikme üstünü kapatır, üst sac oturur) · köşeler 2,5 pah (boru dış R4'ün içinde) · çevre alın kaynağı taşlanır (yüzle aynı → katı yok)
    c = 2.5
    for x in PX:
        for z in PZ:
            t = _sac("kose_dikmesi_%d_%d_tapa" % (int(x), int(z)), "braket", t=2.0)
            u0, u1, v0, v1 = x - PB / 2, x + PB / 2, -(z + PB / 2), -(z - PB / 2)
            t.taban([(u0 + c, v0), (u1 - c, v0), (u1, v0 + c), (u1, v1 - c), (u1 - c, v1), (u0 + c, v1), (u0, v1 - c), (u0, v0 + c)],
                    O=(0, Y_DIKME[1], 0), ex=(1, 0, 0), ey=(0, 0, -1), ad="tapa")
    G.NOT.append("dikme tapaları 30 × 30 × 2, köşeler 2,5 pah · çevresi TIG alın kaynağı, taşlanır (kapalı profil)")
    # dikme + alt kuşaklar ↔ taban sacı (iç yüzlerde dikiş kaynak, 3 × 40)
    for z in PZ:
        zz = z - PB / 2 if z > 0 else z + PB / 2
        nz = (0, 0, -1.0) if z > 0 else (0, 0, 1.0)
        for xc in (110.0, 200.0, 290.0):
            K.append(S.kaynak_dikisi((xc - 20, Y_TABAN, zz), (xc + 20, Y_TABAN, zz), nz, (0, 1.0, 0), 2.0, ad="taban_sac_dikis_kaynagi_%d_%d" % (int(z), int(xc)),
                                     birim=BIRIM, taraf="iç (dikiş)", not_="kuşak ↔ taban sacı 3 × 40 / kenar"))
    for x in PX:
        xx = x + PB / 2 if x < 200 else x - PB / 2
        nx = (1.0, 0, 0) if x < 200 else (-1.0, 0, 0)
        for zc in (-600.0, -380.0, -160.0):
            K.append(S.kaynak_dikisi((xx, Y_TABAN, zc - 20), (xx, Y_TABAN, zc + 20), (0, 1.0, 0), nx, 2.0, ad="taban_sac_dikis_kaynagi_x%d_%d" % (int(x), int(zc)),
                                     birim=BIRIM, taraf="iç (dikiş)", not_="yan kuşak ↔ taban sacı"))
    # K → B kovanları (sol alt yan kuşak · Ø12 × 1,5 · üst duvardan takılır, üstte çevre kaynak)
    ta = P["taban_sac_tasiyici_20"]
    for z in KB_Z:
        ta.duvar_delik("-y", z, KB_X - PX[0], 9.0, tip="kb_civata", not_="K→B M8 (alt duvar)")
        ta.duvar_delik("+y", z, KB_X - PX[0], 12.2, tip="kb_kovan", not_="kovan Ø12 (üst duvar)")
        kv = _halka((KB_X, Y_TABAN + PT, z), (0, 1.0, 0), 6.0, 4.5, Y_KUSAK["alt"][1] + 1.0 - Y_TABAN - PT)
        G.ELEMAN.append(_ozel("taban_sac_tasiyici_20_kovan_%d" % int(-z), kv, "özel (304 boru Ø12 × 1,5)", "Kovan AISI 304 Ø12 × 1,5 · L 29 (K→B M8 cıvatası kuşağı ezmesin · üst duvardan 1 taşar)",
                              "Ø12/Ø9 × 29", uretim=True, mal="sac"))
        K.append(S.kaynak_halka((KB_X, Y_KUSAK["alt"][1], z), (0, 1.0, 0), 6.0, 1.0, ad="taban_sac_tasiyici_20_kovan_kaynagi_%d" % int(-z), birim=BIRIM))
        om = P["istasyon_tabani_tasiyici_20"]
        om.duvar_delik("-y", z, KB_X - PX[0], 13.5, tip="kb_gecis", not_="K→B cıvata başı geçişi (alt duvar)")
        om.duvar_delik("+y", z, KB_X - PX[0], 13.5, tip="kb_gecis", not_="K→B cıvata başı geçişi (üst duvar) · istasyon tabanında Ø16 + tapa")
    return P


def taban_ve_istasyon_tabani():
    # --- taban sacı 3 (788–791): iskeletin altı, kaynaklı
    tb = _sac("taban_sac_3", "braket", t=3.0)
    P = tb.taban([(1.5, -59.0), (398.5, -59.0), (398.5, 829.0), (1.5, 829.0)], O=(0, Y_DOLAP, 0), ex=(1, 0, 0), ey=(0, 0, -1), ad="taban")
    for z in KB_Z: P.delik(KB_X, -z, 9.0, tip="vida_deligi", parca="K→B M8 (ISO 273 orta)")
    G.PANEL["taban"] = P
    # --- istasyon tabanı 3 (892–895): orta kuşaklara delik kaynağı · köşe çentikleri dikme çevresinde kaynakla kapalı
    it = _sac("istasyon_tabani_3", "braket", t=3.0, bolge="sicrama")
    Q = it.taban([(1.5, -59.0), (398.5, -59.0), (398.5, 828.5), (1.5, 828.5)], O=(0, Y_MEK, 0), ex=(1, 0, 0), ey=(0, 0, -1), ad="istasyon_tabani")
    for x in PX:
        for z in PZ:
            u0, u1 = (0.5, x + PB / 2 + 0.5) if x < 200 else (x - PB / 2 - 0.5, 399.5)          # açık köşe çentiği (sac kenarından 1 dışarı)
            v0, v1 = (-60.0, -(z - PB / 2 - 0.5)) if z > 0 else (-(z + PB / 2 + 0.5), 829.5)
            Q.kesik([(u0, v0), (u1, v0), (u1, v1), (u0, v1)], tip="dikme_centigi", dfm=False, parca="dikme çevresi 0,5 boşluk · TIG köşe kaynağıyla kapatılır")
    for z in KB_Z:
        Q.delik(KB_X, -z, 16.0, tip="servis_deligi", parca="K→B M8 lokma geçişi · gıda sınıfı silikon tapa")
    yariklar = [(80.0, 42.0, 0.0), (200.0, 42.0, 0.0), (320.0, 42.0, 0.0), (80.0, -800.0, 0.0), (200.0, -800.0, 0.0), (320.0, -800.0, 0.0),
                (20.0, -150.0, 90.0), (20.0, -380.0, 90.0), (380.0, -150.0, 90.0), (380.0, -380.0, 90.0)]
    for x, z, a in yariklar:
        Q.oblong(x, -z, 25.0, 8.0, a, tip="kaynak_yarigi", parca="delik kaynağı 25 × 8 (kuşağa) · yüz taşlanır")
    G.PANEL["istasyon_tabani"] = Q; G.YARIK = yariklar
    # mekanizma ayakları: PEM SP-M6 (gövdesi altta, üst yüz düz)
    for x, z, hedef in PEM_M6:
        ps, c, ms = S.pem_somun("SP", "M6", (x, Y_MEK, z), (0, -1.0, 0), it.t, ad="istasyon_tabani_pem_M6_%s" % hedef, birim=BIRIM)
        Q.delik(x, -z, c["delik"], tip="pem_somun", parca=ps["meta"]["parca"], pem_tip="SP", kenar_min=c["kenar"], min_sac=ms)
        _eleman(ps)
        _arayuz(S.vida("ISO4762", "M6", 16, (x, Y_MEK_UST + 8.0, z), (0, -1.0, 0), ad="arayuz_" + hedef + "_M6", birim=BIRIM), "K mekanizma: " + hedef,
                "ayakta Ø6,6 delik · ISO 4762 M6 × 16 (ayak et kalınlığına göre) → istasyon tabanındaki PEM SP-M6", "mekanizma sahibi")
    for x, z, hedef in PEM_M5_ITICI:
        ps, c, ms = S.pem_somun("SP", "M5", (x, Y_MEK, z), (0, -1.0, 0), it.t, ad="istasyon_tabani_pem_M5_%s_%d" % (hedef, int(-z)), birim=BIRIM)
        Q.delik(x, -z, c["delik"], tip="pem_somun", parca=ps["meta"]["parca"], pem_tip="SP", kenar_min=c["kenar"], min_sac=ms)
        _eleman(ps)
        _arayuz(S.vida("ISO4762", "M5", 16, (x, Y_MEK_UST + 8.0, z), (0, -1.0, 0), ad="arayuz_%s_M5_%d" % (hedef, int(-z)), birim=BIRIM), "K mekanizma: " + hedef,
                "8 mm ayak tabanının dış köşesinde Ø5,5 delik · ISO 4762 M5 × 16 → istasyon tabanındaki PEM SP-M5", "mekanizma sahibi")
    # delik kaynakları (yarık dolgusu, yüzle aynı)
    for i, (x, z, a) in enumerate(yariklar):
        f = S.yuz_oblong(x, -z, 25.0, 8.0, a)
        sh = S._tasi(S._prizma(f, 3.0), S._M(np.column_stack([[1, 0, 0], [0, 0, -1.0], [0, 1.0, 0]]), (0, Y_MEK, 0)))
        G.KAYNAK.append(dict(ad="istasyon_tabani_delik_kaynagi_%d" % i, wp=cq.Workplane("XY").add(sh), sh=sh, mal="sac", birim=BIRIM, grup="SABIT", kaynak=SURUM, tur="kaynak",
                             bom=("Delik (yarık) kaynağı · TIG 141 · ER308LSi · yüz taşlanır", 1, "25 × 8 × 3", "istasyon tabanı ↔ orta kuşak", "ÜRETİM"),
                             meta=dict(tur="kaynak", tip="delik", yontem="TIG 141")))
    # dikme çevresi köşe kaynakları (taban üstü ↔ dikme iki iç yüzü)
    for x in PX:
        for z in PZ:
            sx = 1.0 if x < 200 else -1.0; sz = -1.0 if z > 0 else 1.0
            px = x + sx * PB / 2; pz = z + sz * PB / 2
            G.KAYNAK.append(S.kaynak_dikisi((px, Y_MEK_UST, z - 11), (px, Y_MEK_UST, z + 11), (sx, 0, 0), (0, 1.0, 0), 2.0,
                                            ad="istasyon_tabani_dikme_kaynagi_%d_%d_a" % (int(x), int(z)), birim=BIRIM, taraf="üst (sızdırmaz)", not_="taban ↔ dikme"))
            G.KAYNAK.append(S.kaynak_dikisi((x - 11, Y_MEK_UST, pz), (x + 11, Y_MEK_UST, pz), (0, 0, sz), (0, 1.0, 0), 2.0,
                                            ad="istasyon_tabani_dikme_kaynagi_%d_%d_b" % (int(x), int(z)), birim=BIRIM, taraf="üst (sızdırmaz)", not_="taban ↔ dikme"))
    # K→B servis delikleri tapası
    for z in KB_Z:
        tp = silindir((KB_X, Y_MEK, z), (0, 1.0, 0), 8.0, 3.0).fuse(silindir((KB_X, Y_MEK_UST, z), (0, 1.0, 0), 10.0, 1.0))
        G.ELEMAN.append(_ozel("istasyon_tabani_tapa_%d" % int(-z), tp, "gıda sınıfı silikon (FDA 21 CFR 177.2600)", "Kapama tapası Ø16 delik · Ø20 × 1 baş · silikon",
                              "Ø16 × 3 + Ø20 × 1", malzeme="VMQ silikon", mal="conta"))
    return P, Q


def _yan(taraf):
    """sol: x 0–1,5 (n +x) · sağ: x 400–398,5 (n −x) · ön + arka 90° iç dönüş · u = y · v = ±z"""
    ad = "sol_sac_urun_girisi" if taraf == "sol" else "sag_sac_E_penceresi"
    s = _sac(ad, "dis", bolge="sicrama"); g = s.R + s.t
    if taraf == "sol":
        P = s.taban([(Y_TABAN, Z_ARKA_IC + g), (Y_UST_ALT, Z_ARKA_IC + g), (Y_UST_ALT, Z_ON - g), (Y_TABAN, Z_ON - g)], O=(0, 0, 0), ex=(0, 1, 0), ey=(0, 0, 1), ad="yan")
        k_arka, k_on = 0, 2
        zv = lambda z: z
    else:
        P = s.taban([(Y_TABAN, -Z_ON + g), (Y_UST_ALT, -Z_ON + g), (Y_UST_ALT, -Z_ARKA_IC - g), (Y_TABAN, -Z_ARKA_IC - g)], O=(W, 0, 0), ex=(0, 1, 0), ey=(0, 0, -1), ad="yan")
        k_arka, k_on = 2, 0
        zv = lambda z: -z
    arka = P.flans(k_arka, 22.0, yon=+1, ad="arka_donus")                     # arka sac buna PEM SP-M5 ile bağlanır
    on = P.flans(k_on, 16.5, yon=+1, ad="on_donus")                          # ön kenar: kapak arkasında 0,5 boşluk · dikme önünde
    G.PANEL[taraf] = dict(yan=P, arka=arka, on=on, s=s, zv=zv)
    if taraf == "sol":
        y0, y1, z0, z1 = URUN_GIRISI
        P.dikdortgen((y0 + y1) / 2.0, zv((z0 + z1) / 2.0), y1 - y0, z1 - z0, r=6.0, tip="urun_girisi", parca="F→K ürün girişi (R6 köşe · kenar çapaksız)")
        for nm, y, z, cap in DELIK_SOL:
            P.delik(y, zv(z), cap, tip="gecis", parca=nm)
    else:
        y0, y1, z0, z1 = E_PENCERE
        P.dikdortgen((y0 + y1) / 2.0, zv((z0 + z1) / 2.0), y1 - y0, z1 - z0, r=6.0, tip="e_penceresi", parca="K→E pizza penceresi (R6 köşe)")
    # pompa rafı köşebendi: 3 × FHP-M5 deliği (saplamalar ARAYÜZ: köşebende Ø5,5 gerekir)
    for z in KOSEBENT_Z:
        P.delik(1625.0, zv(z), 5.0, tip="pem_saplama", parca="FHP-M5 (köşebent)", pem_tip="FHP", kenar_min=7.2, min_sac=1.0)
    return s, P


def yanlar():
    return _yan("sol"), _yan("sag")


def ust_sac():
    s = _sac("ust_sac", "dis"); g = s.R + s.t
    P = s.taban([(0.0, -Z_ON + g), (W, -Z_ON + g), (W, -Z_ARKA_IC - g), (0.0, -Z_ARKA_IC - g)], O=(0, Y_UST_ALT, 0), ex=(1, 0, 0), ey=(0, 0, -1), ad="ust")
    on = P.flans(0, Y_UST - 1840.5, yon=-1, bas=17.0, son=17.0, ad="on_donus")
    arka = P.flans(2, Y_UST - 1840.5, yon=-1, bas=23.0, son=23.0, ad="arka_donus")
    x0, x1, z0, z1 = HARTING
    P.dikdortgen((x0 + x1) / 2.0, -(z0 + z1) / 2.0, x1 - x0, z1 - z0, tip="harting_kesigi", parca="K Harting Han 10B soket kesiği (h3_elk · KS ust_sac)")
    for xb, yb in PANO_BURC:
        if yb < 1840.0: continue
        pts = [arka.yerel((xb + sx, yy, Z_ARKA_IC)) for sx, yy in ((-6.0, 1839.0), (6.0, 1839.0), (6.0, 1853.0), (-6.0, 1853.0))]
        arka.kesik([(p_[0], p_[1]) for p_ in pts], tip="burc_centigi", dfm=False, parca="pano ara burcu geçişi (açık çentik 12 × 14 · büküm iç yüzüne 7,5)")
    G.PANEL["ust"] = dict(ust=P, on=on, arka=arka, s=s)
    return s, P


def arka_sac():
    s = _sac("arka_sac", "dis"); g = s.R + s.t
    P = s.taban([(0.0, Y_TABAN + g), (W, Y_TABAN + g), (W, Y_UST), (0.0, Y_UST)], O=(0, 0, Z_ARKA), ex=(1, 0, 0), ey=(0, 1, 0), ad="arka")
    alt = P.flans(0, 13.5, yon=+1, bas=23.0, son=23.0, ad="alt_donus")       # taban sacına oturur · arka alt kuşağın 1,5 gerisinde biter
    for x, y in PANO_BURC:
        P.delik(x, y, 5.0, tip="pem_saplama", parca="pano ara burcu · PEM FHP-M5 (arayüz)", pem_tip="FHP", kenar_min=7.2, min_sac=1.0)
    G.PANEL["arka"] = dict(arka=P, alt=alt, s=s)
    return s, P


def kulak(ad, A, stud, u, v, v_cerceve, L_kaynak=25.0, gen=25.0):
    """3 mm L kulak: taban = saplama ayağı (A panelinin iç yüzüne oturur) · flanş = kaynak ayağı (çerçeve yüzüne) · stud: A iç yüzündeki saplama noktası (dünya)"""
    s = _sac(ad, "braket")
    u, v = np.asarray(u, float), np.asarray(v, float)
    t, R = s.t, s.R
    vb = v_cerceve - (R + t)
    va = -9.75
    P = s.taban([(-gen / 2, va), (gen / 2, va), (gen / 2, vb), (-gen / 2, vb)], O=tuple(stud), ex=tuple(u), ey=tuple(v), ad="saplama_ayagi")
    f = P.flans(2, L_kaynak, yon=+1, ad="kaynak_ayagi")
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
    for i, (A, xs, sx) in enumerate(((L[0], 1.5, 1.0), (L[1], 398.5, -1.0))):
        tr = "sol" if sx > 0 else "sag"
        n = np.array([sx, 0, 0])
        # ön dikme arka yüzü (z 27): saplama z 8
        for y in KULAK_DIKME_Y["on"]:
            u = np.cross(np.array([0, 0, 1.0]), n); u = np.array([0, 1.0 * sx, 0])     # n = u × v · v = +z
            kulak("govde_kulak_%s_on_%d" % (tr, int(y)), A, (xs, y, 8.0), u, (0, 0, 1.0), 19.0)
        for y in KULAK_DIKME_Y["arka_sol" if sx > 0 else "arka_sag"]:
            kulak("govde_kulak_%s_arka_%d" % (tr, int(y)), A, (xs, y, -766.0), (0, -1.0 * sx, 0), (0, 0, -1.0), 19.0)
        for z in KULAK_ORTA_Z:
            kulak("govde_kulak_%s_orta_%d" % (tr, int(-z)), A, (xs, 843.0, z), (0, 0, -1.0 * sx), (0, 1.0, 0), 19.0)
    U = G.PANEL["ust"]["ust"]
    for x in KULAK_UST["on"]:
        kulak("govde_kulak_ust_on_%d" % int(x), U, (x, Y_UST_ALT, 8.0), (1.0, 0, 0), (0, 0, 1.0), 19.0)
    for x in KULAK_UST["arka"]:
        kulak("govde_kulak_ust_arka_%d" % int(x), U, (x, Y_UST_ALT, -766.0), (-1.0, 0, 0), (0, 0, -1.0), 19.0)


def arka_baglantilari():
    """arka sac: ARKA DÜZLEM z −830 KEMAL KURALI → dışarı taşan vida başı YOK (v1.1 · 2 Eki): arka saca preslenmiş PEM FHP-M5 saplama (baş dış yüzle aynı),
    yan sacların arka dönüşlerinde / üst sacın arka dönüşünde Ø5,5 · DIN 9021 pul + ISO 10511 somun İÇERİDEN (dikme ↔ arka sac arası 13,5 mm yarıktan SW8 açık ağız).
    Arka sacı içeri almak mümkün değil: pano ara burçları (K_ELEKTRIK) ve 2 elektrik kelepçesi arka sacın iç yüzüne (−828,5) oturuyor."""
    A = G.PANEL["arka"]["arka"]
    for tr, xx in (("sol", 12.5), ("sag", W - 12.5)):
        B = G.PANEL[tr]["arka"]
        for y in (850.0, 1100.0, 1350.0, 1600.0, 1830.0):
            b = S.vidali_birlesim(A, B, (xx, y, Z_ARKA), "pem_saplama", ad="govde_bag_arka_%s_%d" % (tr, int(y)), birim=BIRIM)
            for q in b["parcalar"]: _eleman(q)
            G.BIRLESIM.append(b)
    B = G.PANEL["ust"]["arka"]
    for x in (40.0, 360.0):                                                       # x 200 yok: içerideki somun pano plakasına (x 67,5–332,5 · z −822) değerdi
        b = S.vidali_birlesim(A, B, (x, 1849.5, Z_ARKA), "pem_saplama", ad="govde_bag_arka_ust_%d" % int(x), birim=BIRIM)
        for q in b["parcalar"]: _eleman(q)
        G.BIRLESIM.append(b)
    # pano ara burçları (arayüz): arka saca preslenmiş FHP-M5 saplama (baş dış yüzle aynı) → burcun iç dişine
    for x, y in PANO_BURC:
        _arayuz(S.pem_saplama("FHP", "M5", 12, (x, y, Z_ARKA), (0, 0, 1.0), ad="arayuz_pano_burcu_%d_%d" % (int(x), int(y)), birim=BIRIM, sac_ad="arka_sac")[0],
                "K_ELEKTRIK pano_ara_burcu", "burç M5 İÇ DİŞLİ olmalı (saplama burca vidalanır) · arka sacta FHP Ø5,0 hazır", "pano sahibi")
    # köşebent saplamaları (arayüz)
    for tr, xs, sx in (("sol", 0.0, 1.0), ("sag", W, -1.0)):
        for z in KOSEBENT_Z:
            sp, c = S.pem_saplama("FHP", "M5", 12, (xs, 1625.0, z), (sx, 0, 0), ad="arayuz_kosebent_%s_%d" % (tr, int(-z)), birim=BIRIM, sac_ad=G.PANEL[tr]["s"].ad)
            _arayuz(sp, "K_YAG yag_pompa_rafi_kosebendi_%s" % tr, "köşebent dik ayağında Ø5,5 delik · DIN 9021 pul + ISO 10511 somun içeriden", "yağ sahibi")


def m8_noktalari():
    """K tarafı: dikme / orta kuşak dış duvarında M8 perçin somun + 2 mm ara pul + yan sacta Ø9 · cıvata komşu taraftan (ARAYÜZ)"""
    P = G.PROF
    out = []
    for tr, liste, x_dis, sx in (("F", M8_F, 5.0, 1.0), ("E", M8_E, 395.0, -1.0)):
        A = G.PANEL["sol" if sx > 0 else "sag"]["yan"]
        xd = PX[0] if sx > 0 else PX[1]
        for yer, y, z in liste:
            if yer == "orta_kusak":
                pr = P["istasyon_tabani_tasiyici_%d" % int(xd)]; a = z
            else:
                pr = P["kose_dikmesi_%d_%d" % (int(xd), int(z))]; a = y
            pr.duvar_delik("-x" if sx > 0 else "+x", a, 0.0, 11.0, tip="m8_percin_somun", not_="K↔%s M8" % tr)
            ps, c = S.percin_somun("M8", PT, (x_dis, y, z), (sx, 0, 0), ad="govde_m8_%s_%d_%d" % (tr, int(y), int(-z)), birim=BIRIM)
            _eleman(ps)
            ara = _halka((x_dis - sx * 1.5, y, z), (-sx, 0, 0), 8.0, 4.6, 2.0)
            _eleman(_ozel("govde_m8_ara_pul_%s_%d_%d" % (tr, int(y), int(-z)), ara, "özel (304 · lazer)", "Ara pul AISI 304 Ø16 / Ø9,2 × 2 (yan sac ↔ perçin somun başı)", "Ø16 × 2",
                          uretim=True, mal="sac"))
            A.delik(y, z if sx > 0 else -z, 9.0, tip="vida_deligi", parca="K↔%s M8 (ISO 273 orta)" % tr)
            # arayüz cıvatası: komşu sacın iç yüzünden (F: x −1,5 · E: x 401,5) · DIN 125 pul
            xk = -1.5 if sx > 0 else W + 1.5
            pu = S.pul("DIN125", "M8", (xk - sx * 1.6, y, z), (sx, 0, 0), ad="arayuz_m8_%s_%d_%d_pul" % (tr, int(y), int(-z)), birim=BIRIM)
            vd = S.vida("ISO4762", "M8", 25, (xk - sx * 1.6, y, z), (sx, 0, 0), ad="arayuz_m8_%s_%d_%d" % (tr, int(y), int(-z)), birim=BIRIM)
            karsi = "F_UST_KABIN f_ust_yan_sag" if tr == "F" else "E_GOVDE sol_sac_pizza_penceresi"
            _arayuz(pu, karsi, "komşu yan sacta Ø9 delik (aynı eksen)", "")
            _arayuz(vd, karsi, "ISO 4762 M8 × 25 A2-70 + DIN 125 · komşu istasyonun içinden takılır", "")
            out.append(dict(taraf=tr, yer=yer, y=y, z=z, dunya=[round(xk + X_K, 1), y, z]))
    # K → B (arayüz cıvatası: başı kovanın üstünde)
    for z in KB_Z:
        yk = Y_KUSAK["alt"][1] + 1.0                                                          # kovan üstü
        pu = S.pul("DIN125", "M8", (KB_X, yk, z), (0, 1.0, 0), ad="arayuz_kb_%d_pul" % int(-z), birim=BIRIM)
        vd = S.vida("ISO4762", "M8", 50, (KB_X, yk + 1.6, z), (0, -1.0, 0), ad="arayuz_kb_%d" % int(-z), birim=BIRIM)
        _arayuz(pu, "B_TASIYICI tasiyici_capraz_2 + B_KASA tavan_dis_sac", "", "")
        _arayuz(vd, "B_TASIYICI tasiyici_capraz_2 + B_KASA tavan_dis_sac",
                "B: capraz_2 üst duvarına M8 perçin somun (PU köpüklemeden ÖNCE) dünya x %.1f z %.0f · tavan dış sacında Ø9 · ISO 4762 M8 × 50 + DIN 125" % (KB_X + X_K, z),
                "istasyon tabanındaki Ø16 servis deliğinden uzatmalı lokma (tapa sonra takılır)")
        out.append(dict(taraf="B", yer="alt_yan_kusak", y=Y_DOLAP, z=z, dunya=[KB_X + X_K, Y_DOLAP, z]))
    G.M8 = out


def kapak():
    """çift cidarlı tek kapak · dış tava 1,5 (bindirme + TIG) · iç tava 1,0 (punta) · 3 gizli menteşe · 3 bas-aç"""
    x0, x1 = KAPAK_X; y0, y1 = KAPAK_Y
    kd = _sac("onyuz_kapak_K", "kapak_dis", mal="on_seffaf"); g = kd.R + kd.t
    D = kd.taban([(x0 + g, y0 + g), (x1 - g, y0 + g), (x1 - g, y1 - g), (x0 + g, y1 - g)], O=(0, 0, Z_KAPAK - kd.t), ex=(1, 0, 0), ey=(0, 1, 0), ad="on_yuz")
    fa = [D.flans(i, Z_KAPAK - Z_ON, yon=-1, ad=a) for i, a in enumerate(("alt_donus", "sag_donus", "ust_donus", "sol_donus"))]
    kd.kose(fa[0], fa[1], "bindirme", ustte=fa[0]); kd.kose(fa[1], fa[2], "bindirme", ustte=fa[2])
    kd.kose(fa[2], fa[3], "bindirme", ustte=fa[2]); kd.kose(fa[3], fa[0], "bindirme", ustte=fa[0])
    ki = _sac("onyuz_kapak_K_ic_tava", "kapak_ic", mal="on_seffaf"); gi = ki.R + ki.t
    b = S.STD.kapak()["ic_dis_bosluk"]
    xi0, xi1, yi0, yi1 = x0 + kd.t + b, x1 - kd.t - b, y0 + kd.t + b, y1 - kd.t - b
    I = ki.taban([(xi0 + gi, yi0 + gi), (xi1 - gi, yi0 + gi), (xi1 - gi, yi1 - gi), (xi0 + gi, yi1 - gi)], O=(0, 0, Z_ON), ex=(1, 0, 0), ey=(0, 1, 0), ad="ic_tava")
    fi = [I.flans(i, S.STD.kapak()["ic_donus"], yon=+1, ad=a) for i, a in enumerate(("alt_donus", "sag_donus", "ust_donus", "sol_donus"))]
    for i in range(4): ki.kose(fi[i], fi[(i + 1) % 4], "acik")
    zp = Z_ON + 1.0 + 7.5
    nok = [(x, yi0 - b / 2.0, zp) for x in np.arange(60, 360, 100)] + [(x, yi1 + b / 2.0, zp) for x in np.arange(60, 360, 100)]
    nok += [(xi0 - b / 2.0, y, zp) for y in np.arange(860, 2190, 160)] + [(xi1 + b / 2.0, y, zp) for y in np.arange(860, 2190, 160)]
    ki.punta(kd, nok, not_="iç tava dönüşleri → dış tava dönüşleri (0,5 boşluk elektrotla kapanır) · ≈ 150 aralık")
    G.PANEL["kapak"] = dict(dis=D, ic=I, kd=kd, ki=ki)
    # --- menteşeler (sol ön dikme içi) — Southco R6 / EMKA 1046 sınıfı gizli 180° kaldır-çıkar (ölçüler TEMSİLİ, katalogdan doğrulanacak)
    dk = G.PROF["kose_dikmesi_20_42"]
    for i, yh in enumerate(MENTESE_Y):
        dk.duvar_pencere("+z", yh, 23.75 - PX[0], 52.0, 13.0, tip="mentese_penceresi", not_="gizli menteşe gövdesi")
        for dy in (-15.0, 15.0):
            dk.duvar_delik("+x", yh + dy, 44.0 - PZ[0], 5.5, tip="mentese_vidasi", not_="menteşe gövdesi 2 × M5")
        gov = kutu(17.5, 30.0, yh - 25, yh + 25, 31.0, 57.0)
        for dy in (-15.0, 15.0):
            gov = gov.cut(silindir((22.0, yh + dy, 44.0), (1.0, 0, 0), 2.5, 9.0))
        G.ELEMAN.append(_ozel("onyuz_kapak_K_mentese_%d_sabit" % i, gov, "Southco R6 / EMKA 1046 sınıfı", "Gizli 180° kaldır-çıkar menteşe · GÖVDE yarısı (dikme içine gömülü) AISI 316",
                              "13 × 50 × 26 · 2 × M5 (dikme iç yan duvarından)", malzeme="AISI 316 pasive", mal="celik", meta=dict(kaldir_cikar=True, aci=180, pivot=[KAPAK_X[0], Z_KAPAK])))
        for dy in (-15.0, 15.0):
            _eleman(S.vida("ISO7380", "M5", 12, (35.0, yh + dy, 44.0), (-1.0, 0, 0), ad="onyuz_kapak_K_mentese_%d_sabit_vida_%s" % (i, "a" if dy < 0 else "b"), birim=BIRIM))
        # kanat yarısı: plaka 1,5 (kapak iç yüzü arkasında) + cep kutusu (kapak boşluğunda) + kol
        pl = kutu(17.0, 48.0, yh - 30, yh + 30, Z_ON - 1.5, Z_ON)
        for dy in (-20.0, 20.0):
            pl = pl.cut(silindir((42.0, yh + dy, Z_ON - 2.0), (0, 0, 1.0), 2.75, 3.0))
        kanat = _bir(pl, kutu(18.0, 30.0, yh - 25, yh + 25, Z_ON, Z_ON + 11.0), kutu(20.0, 28.0, yh - 18, yh + 18, 57.0, Z_ON - 1.5))
        G.ELEMAN.append(_ozel("onyuz_kapak_K_mentese_%d_kanat" % i, kanat, "Southco R6 / EMKA 1046 sınıfı", "Gizli 180° kaldır-çıkar menteşe · KANAT yarısı + kol (kapakla döner)",
                              "plaka 31 × 60 × 1,5 + cep 12 × 50 × 11", malzeme="AISI 316 pasive", mal="celik", meta=dict(kapakla_doner=True)))
        I.dikdortgen(24.25, yh, 13.0, 51.0, tip="mentese_cebi", parca="menteşe kanat cebi (kol geçişi)")
        for dy in (-20.0, 20.0):
            ps, c, ms = S.pem_somun("SP", "M5", (42.0, yh + dy, Z_ON + ki.t), (0, 0, 1.0), ki.t, ad="onyuz_kapak_K_mentese_%d_pem_%s" % (i, "a" if dy < 0 else "b"), birim=BIRIM)
            ps["meta"]["kapakla_doner"] = True
            I.delik(42.0, yh + dy, c["delik"], tip="pem_somun", parca=ps["meta"]["parca"], pem_tip="SP", kenar_min=c["kenar"], min_sac=ms)
            _eleman(ps)
            vd = S.vida("ISO7380", "M5", 6, (42.0, yh + dy, Z_ON - 1.5), (0, 0, 1.0), ad="onyuz_kapak_K_mentese_%d_kanat_vida_%s" % (i, "a" if dy < 0 else "b"), birim=BIRIM)
            vd["meta"]["kapakla_doner"] = True
            _eleman(vd)
    # --- bas-aç (sağ ön dikme içi) — Southco 97 / EMKA 1080 sınıfı mekanik push-to-open, geçme gövde
    dr = G.PROF["kose_dikmesi_380_42"]
    for i, yb in enumerate(BASAC_Y):
        dr.duvar_delik("+z", yb, BASAC_X - PX[1], 12.2, tip="basac_deligi", not_="bas-aç gövdesi (geçme)")
        sh = silindir((BASAC_X, yb, 31.0), (0, 0, 1.0), 6.0, 26.0).fuse(silindir((BASAC_X, yb, 57.0), (0, 0, 1.0), 7.0, 1.0)).fuse(silindir((BASAC_X, yb, 58.0), (0, 0, 1.0), 3.0, 1.0))
        G.ELEMAN.append(_ozel("onyuz_kapak_K_basac_%d" % i, sh, "Southco 97 / EMKA 1080 sınıfı", "Bas-aç mandalı (push-to-open, geçme gövde Ø12 · O-ring) — dikme ön yüzünde Ø12,2",
                              "Ø12 × 26 · baş Ø14 × 1 · strok 7", malzeme="AISI 316 / POM", mal="siyah"))
        dp = _sac("onyuz_kapak_K_karsilik_%d" % i, "dis", mal="on_seffaf")
        dp.taban([(BASAC_X - 12, yb - 20), (BASAC_X + 12, yb - 20), (BASAC_X + 12, yb + 20), (BASAC_X - 12, yb + 20)], O=(0, 0, Z_ON + ki.t), ex=(1, 0, 0), ey=(0, 1, 0), ad="plaka")
        dp.punta(ki, [(BASAC_X - 7, yb - 13, Z_ON + ki.t), (BASAC_X + 7, yb + 13, Z_ON + ki.t)], not_="karşılık takviyesi → iç tava (kapak kapanmadan önce)")
    return kd, ki


def kur(log=print):
    if G.kuruldu: return G
    t0 = time.time()
    for a in ("SAC", "PROFIL", "ELEMAN", "KAYNAK", "BIRLESIM", "ARAYUZ", "KULAK", "NOT"): setattr(G, a, [])
    G.PANEL = {}
    iskelet()
    taban_ve_istasyon_tabani()
    yanlar(); ust_sac(); arka_sac()
    kulaklar(); arka_baglantilari(); m8_noktalari(); kapak()
    G.PROFIL = list(G.PROF.values())
    G.kuruldu = True
    log("%s · kuruldu: %d sac · %d profil · %d eleman · %d kaynak · %d birleşim · %d arayüz · %.1f sn" % (SURUM, len(G.SAC), len(G.PROFIL), len(G.ELEMAN), len(G.KAYNAK),
                                                                                                    len(G.BIRLESIM), len(G.ARAYUZ), time.time() - t0))
    return G


# =====================================================================================================================================
# 3 · MONTAJ SÖZLEŞMESİ (KS.PARCALAR: ad · wp (yerel) · mal · grup · bom)
# =====================================================================================================================================
def _mal(p):
    ad = p["ad"]
    if ad.startswith("onyuz_kapak_K") and not re.search(r"mentese_\d+_sabit|basac", ad): return "on_seffaf"
    if p.get("tur") in ("sac",):
        return "kabuk" if ad in ("sol_sac_urun_girisi", "sag_sac_E_penceresi", "arka_sac", "ust_sac") else "sac"
    if p.get("tur") in ("profil", "kaynak"): return "sac"
    return p.get("mal") if p.get("mal") in ("celik", "conta", "siyah", "sac", "kabuk") else "celik"


def govde_parcalari():
    """montaja girecek gövde parçaları (arayüz elemanları HARİÇ) · yerel koordinat"""
    kur()
    L = []
    for s in G.SAC: L += s.parcalar()
    L += [p.parca() for p in G.PROFIL] + G.ELEMAN + G.KAYNAK
    out = []
    for p in L:
        sh = p.get("sh") if p.get("sh") is not None else p["wp"].val()
        q = dict(ad=p["ad"], wp=cq.Workplane("XY").add(sh), mal=_mal(p), grup="SABIT", bom=tuple(p["bom"]) if p.get("bom") else None, kaynak=SURUM,
                 birim=BIRIM, tur=p.get("tur", "sac"))
        if p.get("sac"): q["sac"] = p["sac"]
        if p.get("meta"): q["meta"] = p["meta"]
        out.append(q)
    adlar = [q["ad"] for q in out]
    assert len(adlar) == len(set(adlar)), "çift ad: %s" % sorted(a for a in set(adlar) if adlar.count(a) > 1)
    return out


GOVDE_ONEK = ("kose_dikmesi", "onyuz_", "taban_sac", "istasyon_tabani", "arka_sac", "ust_sac", "sol_sac", "sag_sac", "govde_")


def uygula_ks(KS, rapor=None):
    """montaj: KS.modul() SONRASI · eski 21 gövde parçasını çıkarır, yerine üretim sacı gövdesini koyar (yerel) · idempotent"""
    L = KS.PARCALAR
    if any(p["ad"] == "onyuz_kapak_K_ic_tava" for p in L):
        return L
    var = set(p["ad"] for p in L)
    yeni = govde_parcalari()
    eksik = [a for a in ESKI_GOVDE if a not in var]
    assert not eksik, ("h3_k_sac_v1: eski gövde parçası yok", eksik)
    L[:] = [p for p in L if p["ad"] not in ESKI_GOVDE]
    cak = set(p["ad"] for p in L) & set(q["ad"] for q in yeni)
    assert not cak, ("h3_k_sac_v1: mekanizmayla ad çakışması", sorted(cak))
    bilinmeyen = [q["ad"] for q in yeni if not q["ad"].startswith(GOVDE_ONEK)]
    assert not bilinmeyen, ("h3_k_sac_v1: K_GOVDE önekine uymayan ad", bilinmeyen[:5])
    L.extend(yeni)
    if rapor is not None: rapor.append("K üretim sacı gövdesi: −%d eski · +%d yeni (h3_k_sac_v1)" % (len(ESKI_GOVDE), len(yeni)))
    return L


ZARF = (0.0, 400.0, -1.0, 2201.0, -831.0, 80.0)                         # K yereli (dünya x 4000–4400) · montaj K_GOVDE zarf denetimiyle aynı sınırlar


def zarf_denetle(L=None, tol=1e-6):
    """gövde parçaları (arayüz elemanları HARİÇ) zarf içinde mi · dönüş [(ad, [xmin, xmax, ymin, ymax, zmin, zmax] yerel)] — boş = temiz"""
    L = govde_parcalari() if L is None else L
    x0, x1, y0, y1, z0, z1 = ZARF; out = []
    for p in L:
        s = p["wp"].val() if hasattr(p["wp"], "val") else p["wp"]
        b = s.BoundingBox()
        if b.xmin < x0 - tol or b.xmax > x1 + tol or b.ymin < y0 - tol or b.ymax > y1 + tol or b.zmin < z0 - tol or b.zmax > z1 + tol:
            out.append((p["ad"], [round(v, 2) for v in (b.xmin, b.xmax, b.ymin, b.ymax, b.zmin, b.zmax)]))
    return out


def kapakla_doner(ad):
    return ad.startswith("onyuz_kapak_K") and not re.search(r"mentese_\d+_sabit|basac_\d+$", ad)


def dunya_listesi(L):
    """montaj süpürme taraması için: KS parçalarının dünya kopyaları (wp + X_K)"""
    out = []
    for p in L:
        q = dict(p); s = p["wp"].val() if hasattr(p["wp"], "val") else p["wp"]
        q["wp"] = cq.Workplane("XY").add(s.translate(V(X_K, 0, 0))); out.append(q)
    return out


def kapak_dunya(L):
    """kapakla dönen bütün parçalar (dış + iç tava, kanat yarıları, kaynaklar, karşılık plakaları, kapaktaki PEM/vida) · dünya bileşiği"""
    return cq.Compound.makeCompound([(p["wp"].val() if hasattr(p["wp"], "val") else p["wp"]).translate(V(X_K, 0, 0)) for p in L if kapakla_doner(p["ad"])])


# =====================================================================================================================================
# 4 · ÖZ DENETİM + ÇIKTILAR (yalnız <scratchpad>/sac_pilot_K'ya yazar)
# =====================================================================================================================================
def _cikti_klasoru():
    S_ = os.environ.get("K_SAC_CIKTI") or os.path.abspath(os.path.join(H3, "..", "..", "..", "..", "sac_pilot_K"))
    os.makedirs(os.path.join(S_, "acinim"), exist_ok=True)
    return S_


if __name__ == "__main__":
    sys.path.insert(0, _cikti_klasoru())
    import k_sac_denetim_v1 as DEN                                            # ayrı dosya: <scratchpad>/sac_pilot_K/k_sac_denetim_v1.py (yalnız denetim + çıktı)
    DEN.calistir()
    sys.stdout.flush(); os._exit(0)
