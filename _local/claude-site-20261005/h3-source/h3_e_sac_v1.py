# -*- coding: utf-8 -*-
"""h3_e_sac_v1 — E (KUTU KATLAMA) İSTASYONU GÖVDESİ · ÜRETİM SACI v1 (4 Eki 2026 · Claude · GECE 2 ADIM 5b · YEREL · montaja bağlı DEĞİL)

Kemal: "üretim sacını yap ama tam yap, üretime yönelik" — sac atölyesi doğrudan 3B'den üretir (pafta yok; açınım JSON + parça listesi CSV).
STANDART: h3_k_sac_v1 (K pilotu) · h3_sac_v1 (gerçek abkant bükümü: iç R = 1,5t · K 0,45 · büküm payı · köşe/uç rahatlatma · açınım) ·
          h3_govde_ortak_v1 (kulak · kapak · M8 · profil · denetim) · sac_kararlar_v1.json.
REFERANS (bugünkü gövde, şekil/ölçü AYNI): hat3_v8zq.glb E_GOVDE__* + E_MODULER__* · kuruluş betikleri e_govde_yeni.py + e_duzelt.py ·
          elektrik birleşim paneli J3 (elk3/tasarim.py: ağız 66 × 56 · 4 burç · PD kanalı) · K ↔ E M8 (h3_k_sac_v1.M8_E).
KOORDİNAT: E YERELİ x 0…830 (dünya = x + 4400) · y yerden · z ön +79 / arka −830. Bütün parçalar g (GO.Govde) defterinde YEREL kurulur.

KURGU (atölye) — E KENDİNDEN TAŞIYICI BÜKÜMLÜ KUTU + KAYNAKLI ÖN KASA (mevcut kurgu korunur, profil iskelet YOK: arka köşelerde UHMW kılavuz,
pano plakası ve besleyici dikmeleri duvara yaslı → arka dikme sığmaz)
  1 · KAYNAKLI ALT MONTAJ (tek parça gelir): TABAN 3 mm (y 123–126) + ÖN KASA 304 kutu profil — sol / sağ dikme 20 × 30 × 2, orta dikme 40 × 30 × 2
      (tam boy, tepede 2 mm tapa), 788 kayıtları 30 × 30 × 2 (dikmeler arasında alın) · dikme ↔ taban köşe dikişi (sızdırmaz) · panel KULAKLARI
      (3 mm L, PEM FHP-M5 saplamalı): yan saclar için taban üstünde + dikme arka yüzünde · üst sac için dikme tepelerinde.
  2 · SÖKÜLEBİLİR PANELLER (1,5 · 304 · R 2,25 · K 0,45): SOL YAN (pizza penceresi · K↔E 3 × Ø9 · J3 ağız 66 × 56 + 4 burç saplaması · arka 16,5
      iç dönüş) · SAĞ YAN (şarjör kapısı açıklığı · arka dönüş YALNIZ kapı açıklığının üstünde y 1000–1855; altta köşebent) · ARKA (alt + üst 90° iç
      dönüş; yan dönüşlere FHP saplama, içten pul + fiberli somun) · ÜST (yan 20 aşağı dönüş · arka sacın üst dönüşüne oturur · Harting 66 × 36).
      Görünür yüzlerde vida YOK: yanlar / arka / üst FHP gömme saplama (baş dış yüzle aynı) · somunlar içeriden.
  3 · KAPAKLAR (4, v3.7 zarfı): çift cidar (dış tava 1,5 dönüş 20 · iç tava 1,0 dönüş 15 · punta) — GO.kapak · sol üstte robot ağzı (iki cidar
      hizalı + kasa çıtası) · sol altta klape açıklığı 130 × 130 (dış) / 144 × 168 (iç) · 12 gizli menteşe (gövde yarısı dikme içinde, ön duvarda
      12 × 60 pencere, iç yan duvardan 2 × M5) · 6 bas-aç (orta dikmede Ø12,2) · KULP YOK.
  4 · ŞARJÖR YAN KAPISI: dış sac 1,5 (yan sacla aynı yüzey) + iç tava 1,5 (4 dönüş, dış saca punta) · 2 gizli menteşe (arka sac üstündeki 3 mm
      taşıyıcı lamaya) · bas-aç (yan saca FHP'li 3 mm lamada).
  5 · KAİDE (E_MODULER yerine, AYNI ölçü): 304 kare / dikdörtgen boru 60 × 60 × 3 + 40 × 60 × 3 KAYNAKLI çerçeve · 6 hijyenik ayarlı ayak M12
      (GN 20 sınıfı, Ø40) · ray alt duvarına DIN 929 M12 kaynak somunu · taban ↔ kaide 8 × M8 ISO 7380 (ray üst duvarı içinde DIN 929 M8).
  6 · BAĞLANTI NOKTALARI: K↔E 3 × Ø9 (K'daki perçin somunlar · cıvata E içinden) · J3 paneli 4 burç (FHP-M5, arayüz) · elektrik PD / B
      kanalları, pano plakası burçları, sensör braketleri, UHMW kılavuzlar, şarjör köşebentleri, kalıp/köprü/besleyici/piston askıları:
      DUVARA DEĞEN HER MEKANİZMA PARÇASINA FHP saplama deliği (M5 duvarlarda · M6 tabanda) → ARAYÜZ (mekanizma tarafında Ø5,5 / Ø6,6 delik).
      U_KE ↔ E: üst sacta 3 × PEM SP-M8 (U_KE tabanından M8).
ÇIKTI (yalnız <scratchpad>/gece2/adim5): E_sac_v1.glb · E_parca.csv · acinim_E/*.json · E_denetim.json. Ana GLB'ye / sayfaya YAZMAZ.
Çalıştır: python -u h3_e_sac_v1.py [--hizli] (--hizli: abkant çarpışma araması atlanır)"""
import math, os, sys, json, time, re, csv, collections, pickle
H3 = os.path.dirname(os.path.abspath(__file__)); _U = os.path.dirname(H3)
for _p in (_U, H3):
    if _p not in sys.path: sys.path.insert(0, _p)
import numpy as np
import cadquery as cq
import h3_sac_v1 as S
import h3_govde_ortak_v1 as GO

SURUM = "h3_e_sac_v1"
assert S.STD.dosyalar, ("sac standardı okunamadı (sac_kararlar_v1.json / sac_standart_v1.json): AUTOKITCH_SAC_STANDART ortam değişkeni → <scratchpad>/sac_standart", S._STD_KLASOR)
V = cq.Vector
X_E = 4400.0
BIRIM = "E_GOVDE"
# ---------------------------------------------------------------- ARAYÜZ (E yereli · değişmez)
W = 830.0
T = 1.5
Y0, YTB, YTV, YH = 123.0, 126.0, 1860.5, 1862.0
ZA, ZAI, ZON, ZK = -830.0, -828.5, 59.0, 79.0
ZC0 = 29.0                                                   # ön kasa arkası
YAN_ARKA = 16.5                                              # yan sac arka iç dönüşü (dış ölçü, x 0 → 16,5)
UST_YAN = 20.0                                               # üst sac yan dönüşleri
PENCERE = (978.0, 1062.0, -372.0, -24.0)                     # K → E pizza penceresi (y0 y1 z0 z1) · sol sac
SARJOR_AC = (231.0, 989.0, -823.0, -411.0)                   # sağ sac şarjör kapısı açıklığı
HARTING = (667.0, 733.0, -778.0, -742.0)                     # üst sac soket ağzı (x0 x1 z0 z1) · U_KE tabanındakiyle aynı
K_M8 = ((1100.0, -800.0), (1750.0, -800.0), (877.0, -100.0))  # K ↔ E M8 (h3_k_sac_v1.M8_E) · sol sacta Ø9
J3 = dict(c=-615.0, Y0=1468.0, agiz=(-8.0, 58.0, 6.0, 62.0), burc=((-54.0, 8.0), (54.0, 75.0), (-54.0, 126.0), (54.0, 98.0)))   # elk3/tasarim.py
DS, DG, DO = (1.5, 21.5), (808.5, 828.5), (441.5, 481.5)     # ön kasa dikmeleri (x)
KY = (773.0, 803.0)                                          # 788 kayıtları (y)
KAPAK = {"alt_sol": (2.0, 460.0, 126.0, 785.0), "alt_sag": (463.0, 830.0, 126.0, 785.0),
         "ust_sol": (2.0, 460.0, 788.0, 2197.0), "ust_sag": (463.0, 830.0, 788.0, 2197.0)}
AGIZ = (85.0, 440.0, 886.0, 1062.0)                          # robot ağzı (ust_sol, iki cidar)
KLAPE_AC = (64.0, 194.0, 610.0, 740.0)                       # alt_sol dış tava klape açıklığı
KLAPE_IC = (57.0, 201.0, 603.0, 771.0)                       # alt_sol iç tava klape dönüş deliği
MENT_Y = {"alt": (300.0, 530.0, 680.0), "ust": (900.0, 1360.0, 1750.0)}
MENT_H = 60.0
BASAC_Y = {"alt": (715.0,), "ust": (1015.0, 1715.0)}
BASAC_X = {"sol": 452.0, "sag": 471.0}                       # v8zq 451 / 472 → 452 / 471 (Ø12,2 orta dikme düz yüzüne sığsın, ±1 mm)
KAPI = dict(y=(234.0, 986.0), z=(-820.0, -414.0), tava_x=815.5, tava_y=(236.0, 984.0), tava_z=(-812.0, -420.0), ment_y=(300.0, 900.0), basac_y=610.0)
AYAK_XZ = ((31.5, -760.0), (31.5, -110.0), (415.0, -760.0), (415.0, -110.0), (798.5, -760.0), (798.5, -110.0))
KAIDE_Y = (63.0, 123.0)
U_M8 = ((100.0, -700.0), (730.0, -700.0), (415.0, -700.0))   # U_KE ↔ E üst sac PEM SP-M8
ESKI_GOVDE = ("ayak_0", "ayak_1", "ayak_2", "ayak_3", "ayak_4", "ayak_5", "taban_sac_3", "arka_sac", "ust_sac", "sol_sac_pizza_penceresi", "sag_sac",
              "sarjor_yan_kapisi", "sarjor_yan_kapisi_mentese_0", "sarjor_yan_kapisi_mentese_1", "sarjor_yan_kapisi_basac", "onyuz_dikme_sol",
              "onyuz_dikme_sag", "onyuz_dikme_orta", "onyuz_kayit_788_sol", "onyuz_kayit_788_sag") + tuple(
              "onyuz_kapak_E_%s%s" % (k, e) for k in KAPAK for e in ("", "_ic_sac"))
GOVDE_ONEK = ("ayak_", "taban_sac", "arka_sac", "ust_sac", "sol_sac", "sag_sac", "sarjor_yan_kapisi", "onyuz_", "govde_", "kaide_e_")
S._RENK.update({"profil": ((0.70, 0.73, 0.77, 1.0), 0.85, 0.30), "kapak": ((0.70, 0.82, 0.95, 1.0), 0.2, 0.25)})
MEK_HARIC = re.compile(r"^(E_GOVDE|E_MODULER|K_|U_KE|U_ICECEK|ELK_ZEMIN|ZEMIN|QR)|karton|poset|E_KUTU|kablo|__hava|conta|yigin|plastik$")
# ADIM 8 (4 Eki 2026) · entegrasyonda (zincir 35, sac_ent saplama boyu denetimi) engel yüzünden çıkarılan FHP saplamalar: kur() SONUNDA
# saplama_duzelt() ile kaldırılır — saplama (ARAYÜZ) + sacdaki PEM deliği (kesik) birlikte gider, boş delik kalmaz. Sonda yapılır ki diğer saplamaların
# yer seçimi (guvenli: mevcut deliklere uzaklık) ve ad numaraları birebir aynı kalsın. Taşınamadılar: karşı parçanın tüm yüzü engelin altında / karşı parça yok.
SAPLAMA_CIKAR = {
    "arayuz_j3_burc_1476_669": "J3 üst burç · 23,5 mm'de ELK_ZINCIR etiketi (burç yeri elektrik modelinde sabit; panel alt 2 burçla tutulur)",
    "arayuz_j3_burc_1594_669": "J3 üst burç · 23,5 mm'de Harting (burç yeri elektrik modelinde sabit; panel alt 2 burçla tutulur)",
    "arayuz_mek_sol_2": "şarjör UHMW yan astarı (5 mm) · karton yığını 8 mm'de, astar yüzünün tamamı yığının arkasında",
    "arayuz_mek_sol_3": "şarjör UHMW yan astarı (5 mm) · karton yığını 8 mm'de, astar yüzünün tamamı yığının arkasında",
    "arayuz_mek_arka_19": "şarjör UHMW arka astarı (8 mm) · karton yığını 11 mm'de, astar yüzünün tamamı yığının arkasında",
    "arayuz_mek_arka_20": "şarjör UHMW arka astarı (8 mm) · karton yığını 11 mm'de, astar yüzünün tamamı yığının arkasında",
    "arayuz_mek_taban_38": "karşı parça yok (alüminyum + motor 3,4 mm'de)",
    "arayuz_mek_taban_39": "karşı parça yok (çöp kovası 4,5 mm'de)",
    "arayuz_mek_taban_40": "karşı parça yok (çöp kovası 4,5 mm'de)",
}


def kutu(x0, x1, y0, y1, z0, z1):
    return GO.kutu(x0, x1, y0, y1, z0, z1)


# =====================================================================================================================================
# 0 · DİKDÖRTGEN KUTU PROFİL (GO.Profil kare → iki kenarlı)
# =====================================================================================================================================
class ProfilD(GO.Profil):
    """304 dikdörtgen boru bu × bv × t · bu: dik[0] ekseni boyunca, bv: dik[1] · dış R = 2t"""
    def __init__(self, ad, eksen, a0, a1, c, bu, bv, t=2.0, birim=BIRIM, kaynak=SURUM, not_=""):
        super().__init__(ad, eksen, a0, a1, c, b=max(bu, bv), t=t, birim=birim, kaynak=kaynak, not_=not_)
        self.bu, self.bv = float(bu), float(bv)

    def _yari(self, yuz_ekseni):
        dik = [k for k in "xyz" if k != self.eksen]
        return (self.bu if yuz_ekseni == dik[0] else self.bv) / 2.0

    def _govde(self):
        dis = S.yuz_dikd_r(0.0, 0.0, self.bu, self.bv, 0.0, self.Ro)
        ic = S.yuz_dikd_r(0.0, 0.0, self.bu - 2 * self.t, self.bv - 2 * self.t, 0.0, self.Ro - self.t)
        sh = S._prizma(dis.cut(ic), self.a1 - self.a0)
        dik = [k for k in "xyz" if k != self.eksen]
        ex, ey, ez = GO.EKSEN[dik[0]], GO.EKSEN[dik[1]], GO.EKSEN[self.eksen]
        if np.linalg.det(np.column_stack([ex, ey, ez])) < 0:
            # sağ el çerçevesi için ey ters → yüz yine merkezli simetrik (bv dik[1] boyunca kalır)
            ey = -ey
        return S._tasi(sh, S._M(np.column_stack([ex, ey, ez]), self.merkez(self.a0)))

    def duvar_delik(self, yuz, a, kayma, cap, tip="delik", not_=""):
        n = GO._yuz_vektor(yuz); h = self._yari(yuz[1])
        dik = [k for k in "xyz" if k not in (self.eksen, yuz[1])][0]
        p = self.merkez(a) + n * (h + 1.0) + GO.EKSEN[dik] * kayma
        cut = GO.silindir(p, -n, cap / 2.0, self.t + 1.6)
        self.kesikler.append(dict(sh=cut, tip=tip, yuz=yuz, a=round(a - self.a0, 2), kayma=kayma, cap=cap, not_=not_)); self._sh = None
        return cut

    def duvar_pencere(self, yuz, a, kayma, la, lk, r=1.0, tip="pencere", not_=""):
        sg = 1.0 if yuz[0] == "+" else -1.0; h = self._yari(yuz[1])
        dik = [k for k in "xyz" if k not in (self.eksen, yuz[1])][0]
        c = self.merkez(a); lo, hi = np.zeros(3), np.zeros(3)
        for i, k in enumerate("xyz"):
            if k == self.eksen: lo[i], hi[i] = a - la / 2.0, a + la / 2.0
            elif k == dik: lo[i], hi[i] = c[i] + kayma - lk / 2.0, c[i] + kayma + lk / 2.0
            else:
                d0, d1 = c[i] + sg * (h - self.t - 0.6), c[i] + sg * (h + 1.0); lo[i], hi[i] = min(d0, d1), max(d0, d1)
        cut = kutu(lo[0], hi[0], lo[1], hi[1], lo[2], hi[2])
        self.kesikler.append(dict(sh=cut, tip=tip, yuz=yuz, a=round(a - self.a0, 2), kayma=kayma, olcu=[la, lk], not_=not_)); self._sh = None
        return cut

    def dfm(self):
        out = []; L = self.a1 - self.a0
        for k in self.kesikler:
            dik = [q for q in "xyz" if q not in (self.eksen, k["yuz"][1])][0]
            duz = self._yari(dik) - self.Ro
            yar = (k.get("cap") or k["olcu"][1]) / 2.0
            ok = abs(k["kayma"]) + yar <= duz + 1e-6
            out.append(dict(kural="profil_duz_yuz", durum="GEÇTİ" if ok else "HATA", detay="%s %s %s Ø/en %.1f kayma %.1f · düz yüz ±%.1f" % (self.ad, k["tip"], k["yuz"], 2 * yar, k["kayma"], duz)))
            la = (k.get("cap") or k["olcu"][0]) / 2.0
            uc = min(k["a"] - la, L - k["a"] - la)
            out.append(dict(kural="profil_uc", durum="GEÇTİ" if uc >= 3.0 else "HATA", detay="%s %s → boru ucu %.1f (≥ 3)" % (self.ad, k["tip"], uc)))
            for (yz, b0, b1) in self.uc_kaynak:
                if yz == k["yuz"] and b0 - la - 3.0 < k["a"] < b1 + la + 3.0:
                    out.append(dict(kural="profil_kaynak_bolgesi", durum="HATA", detay="%s %s kaynaklı birleşim bölgesinde (%s %.0f–%.0f)" % (self.ad, k["tip"], yz, b0, b1)))
        out.append(dict(kural="profil_boy", durum="GEÇTİ" if L <= 6000 else "HATA", detay="%s L %.1f ≤ 6000" % (self.ad, L)))
        return out

    def parca(self):
        p = super().parca()
        L = self.a1 - self.a0
        p["bom"] = ("Dikdörtgen boru AISI 304 %g × %g × %g (EN 10217-7 / ASTM A554 · dış R %g) · %s" % (self.bu, self.bv, self.t, self.Ro, self.not_), 1, "L %.1f" % L,
                    p["bom"][3], "ÜRETİM")
        p["meta"]["kesit"] = [self.bu, self.bv, self.t, self.Ro]
        return p


def tapa_d(g, profil, uc="ust", t=2.0, pah=2.0, ad=None):
    """dikdörtgen profil ucuna bu × bv × t tapa (köşeler pah · çevresi TIG alın, taşlanır)"""
    ex, ey = {"y": ((1.0, 0, 0), (0, 0, -1.0)), "x": ((0, 1.0, 0), (0, 0, 1.0)), "z": ((1.0, 0, 0), (0, 1.0, 0))}[profil.eksen]
    ex, ey = np.array(ex), np.array(ey)
    if uc == "alt": ey = -ey
    a = profil.a1 if uc == "ust" else profil.a0
    O = GO.EKSEN[profil.eksen] * a; C = profil.merkez(a)
    cu, cv = float(np.dot(C, ex)), float(np.dot(C, ey)); hu, hv = profil.bu / 2.0, profil.bv / 2.0; c = pah
    u0, u1, v0, v1 = cu - hu, cu + hu, cv - hv, cv + hv
    s = g.sac(ad or profil.ad + "_tapa", "braket", t=t)
    s.taban([(u0 + c, v0), (u1 - c, v0), (u1, v0 + c), (u1, v1 - c), (u1 - c, v1), (u0 + c, v1), (u0, v1 - c), (u0, v0 + c)], O=tuple(O), ex=tuple(ex), ey=tuple(ey), ad="tapa")
    return s


def kulak(g, ad, A, stud, u, v, v_cerceve, L_kaynak=25.0, gen=25.0, uc=9.75, dis="M5", t=None, pul_std="DIN9021"):
    """GO.kulak ile aynı (3 mm L kulak · FHP saplama A'da · pul + fiberli somun kulakta) + kalınlık ve pul seçimi (dar dikmeler için 1,5 kulak + DIN 125)"""
    s = g.sac(ad, "braket", t=t) if t else g.sac(ad, "braket")
    stud = np.asarray(stud, float); u, v = np.asarray(u, float), np.asarray(v, float)
    tt, R = s.t, s.R
    vb = v_cerceve - (R + tt); va = -uc
    n = np.cross(u, v)
    P = s.taban([(-gen / 2, va), (gen / 2, va), (gen / 2, vb), (-gen / 2, vb)], O=tuple(stud), ex=tuple(u), ey=tuple(v), ad="saplama_ayagi")
    P.flans(2, L_kaynak, yon=+1, ad="kaynak_ayagi")
    a = min(tt, 3.0)
    for sg in (+1, -1):
        p0 = stud + u * sg * gen / 2.0 + v * v_cerceve + n * (R + tt)
        p1 = stud + u * sg * gen / 2.0 + v * v_cerceve + n * L_kaynak
        g.kaynak(S.kaynak_dikisi(p0, p1, u * sg, -v, a, ad=ad + "_kaynak_%s" % ("a" if sg > 0 else "b"), birim=g.birim, taraf="dis (köşe)", not_="kulak ↔ iskelet"))
    b = S.vidali_birlesim(A, P, tuple(stud), "pem_saplama", dis=dis, pul_std=pul_std, ad=ad + "_bag", birim=g.birim)
    for q in b["parcalar"]: g.eleman(q)
    g.BIRLESIM.append(b); g.KULAK.append(s)
    return s, P, b


def profil_d(g, ad, eksen, a0, a1, c, bu, bv, t=2.0, not_=""):
    p = ProfilD(ad, eksen, a0, a1, c, bu, bv, t=t, birim=g.birim, kaynak=g.surum, not_=not_)
    g.PROF[ad] = p
    return p


# =====================================================================================================================================
# 1 · YARDIMCILAR: panel noktası güvenli mi · FHP saplama arayüzü · iki panel arası saplama birleşimi
# =====================================================================================================================================
def _kenar_uzaklik(P, u, v):
    pts = P.poly; d = 1e9
    for i in range(len(pts)):
        a = np.array(pts[i]); b = np.array(pts[(i + 1) % len(pts)]); q = np.array([u, v])
        t_ = np.clip(np.dot(q - a, b - a) / max(np.dot(b - a, b - a), 1e-12), 0, 1); d = min(d, float(np.linalg.norm(q - (a + t_ * (b - a)))))
    return d


def _kesik_uzaklik(P, u, v):
    d = 1e9; vx = cq.Vertex.makeVertex(u, v, 0.0)
    for k in P.kesikler:
        if k.tip in ("rahatlatma", "kose_rahatlatma"): continue
        try: d = min(d, k.yuz.distance(vx))
        except Exception: pass
    return d


def guvenli(P, u, v, kenar=11.0, delik=8.0):
    return P.icerir(u, v) and _kenar_uzaklik(P, u, v) >= kenar and _kesik_uzaklik(P, u, v) >= delik


def fhp_arayuz(g, P, nokta, yon, karsi, gerek, dis="M5", boy=12, ad=None, tip_not="mekanizma"):
    """P sacına PEM FHP gömme saplama (baş P'nin 'yon'a ters yüzünde flush) · saplama ARAYÜZ (montaja girmez; karşı parçada delik gerekir)"""
    ya = P.yerel(nokta)
    sp, c = S.pem_saplama("FHP", dis, boy, P.dunya(ya[0], ya[1], 0.0 if np.dot(np.asarray(yon, float), P.normal()) > 0 else P.sac.t), yon,
                          ad=ad or "arayuz_fhp_%s_%d" % (P.sac.ad, len(g.ARAYUZ)), birim=g.birim, sac_ad=P.sac.ad)
    k = P.delik(ya[0], ya[1], c["delik"], tip="pem_saplama", parca=sp["meta"]["parca"], pem_tip="FHP", kenar_min=c["kenar"], min_sac=c["min_sac"])
    g.arayuz(sp, karsi, gerek, tip_not)
    g.__dict__.setdefault("_FHP", {})[sp["ad"]] = (P, k, dict(nokta=np.asarray(nokta, float), yon=yon, karsi=karsi, gerek=gerek, dis=dis, boy=boy, tip_not=tip_not))
    return sp


def saplama_duzelt(g, cikar, tasi=None, log=print):
    """ADIM 8: cikar {ad: gerekçe} → saplama + sacdaki PEM deliği kaldırılır · tasi {ad: [(eksen, değer), ...]} → kaldırılır ve aynı duvarda yeni
    nokta(lar)a (ad, ad + 'b', …) yeniden konur (yer güvenli değilse atlanır, rapora) · fhp_arayuz'un g._FHP kaydını kullanır · kur() SONUNDA çağrılır"""
    F = getattr(g, "_FHP", {}); cik, tas = [], []
    for ad in list(cikar) + list(tasi or {}):
        if ad not in F: continue
        P, k, a = F.pop(ad)
        P.kesikler.remove(k); P.sac._gecersiz()
        g.ARAYUZ[:] = [e for e in g.ARAYUZ if e["ad"] != ad]
        if ad in cikar: cik.append((ad, cikar[ad])); continue
        for j, (eks, deg) in enumerate(tasi[ad]):
            q = a["nokta"].copy(); q[eks] = deg; yq = P.yerel(q)
            if not guvenli(P, yq[0], yq[1], kenar=12.0, delik=9.0): tas.append((ad, "yer güvenli değil %s" % np.round(q, 1).tolist())); continue
            ad_q = ad + "b" * j
            fhp_arayuz(g, P, q, a["yon"], a["karsi"], a["gerek"], dis=a["dis"], boy=a["boy"], ad=ad_q, tip_not=a["tip_not"])
            tas.append((ad_q, np.round(q, 1).tolist()))
    g.SAPLAMA_CIKAR, g.SAPLAMA_TASI = cik, tas
    log("%s · ADIM 8 saplama düzeltmesi: çıkarılan %d · taşınan %s" % (g.birim, len(cik), tas))
    return cik, tas


def bag(g, A, B, nokta, ad, tip="pem_saplama", dis="M5", pul_std="DIN125", boy=None):
    b = S.vidali_birlesim(A, B, tuple(nokta), tip, dis=dis, pul_std=pul_std, boy=boy, ad=ad, birim=g.birim)
    for q in b["parcalar"]: g.eleman(q)
    g.BIRLESIM.append(b)
    return b


def dizi(a0, a1, maks=200.0, uc=40.0, min_adet=2):
    return GO.vida_konumlari(a0, a1, maks=maks, uc=uc, min_adet=min_adet)


# =====================================================================================================================================
# 2 · KUR
# =====================================================================================================================================
def taban_ve_kasa(g):
    """KAYNAKLI ALT MONTAJ: 3 mm taban + ön kasa (dikmeler + kayıtlar + tapalar) + kaynaklar"""
    tb = g.sac("taban_sac_3", "braket", t=3.0)
    P = tb.taban([(DS[0], -ZON), (DG[1], -ZON), (DG[1], -ZA), (DS[0], -ZA)], O=(0, Y0, 0), ex=(1, 0, 0), ey=(0, 0, -1), ad="taban")   # u = x · v = −z · n = +y
    g.PANEL["taban"] = P
    yd = (YTB, YTV - 2.0)
    for ad, (x0, x1) in (("onyuz_dikme_sol", DS), ("onyuz_dikme_sag", DG), ("onyuz_dikme_orta", DO)):
        d = profil_d(g, ad, "y", yd[0], yd[1], ((x0 + x1) / 2.0, (ZC0 + ZON) / 2.0), x1 - x0, ZON - ZC0, not_="ön kasa dikmesi (kaynaklı)")
        tapa_d(g, d, t=2.0, pah=2.0)
        if ad != "onyuz_dikme_orta":
            d.kaynak_bolgesi("+x" if ad.endswith("sol") else "-x", KY[0], KY[1])
        else:
            d.kaynak_bolgesi("+x", KY[0], KY[1]); d.kaynak_bolgesi("-x", KY[0], KY[1])
    for ad, (x0, x1) in (("onyuz_kayit_788_sol", (DS[1], DO[0])), ("onyuz_kayit_788_sag", (DO[1], DG[0]))):
        GO.Profil  # 30 × 30 × 2 kare
        k = g.profil(ad, "x", x0, x1, ((KY[0] + KY[1]) / 2.0, (ZC0 + ZON) / 2.0), b=30.0, t=2.0, not_="788 kaydı (dikmeler arasında alın)")
        for x, e in ((x0, (1.0, 0, 0)), (x1, (-1.0, 0, 0))):
            g.kaynak(GO.uc_kaynaklari(ad + "_kaynak_%d" % int(x), (x, (KY[0] + KY[1]) / 2.0, (ZC0 + ZON) / 2.0), e, [(0, 1.0, 0), (0, -1.0, 0)], b=30.0, a=2.0,
                                      flat=30.0 - 8.0, Ro=4.0, birim=g.birim))
    # dikme ↔ taban: arka ve iç yan yüzde köşe dikişi (ön yüz kapak arkasında, dış yan yüz yan saca dayalı → alın kaynağı taşlanır)
    for ad, (x0, x1) in (("onyuz_dikme_sol", DS), ("onyuz_dikme_sag", DG), ("onyuz_dikme_orta", DO)):
        xa_, xb_ = (x0 + 4, min(x1 - 4, 14.0)) if ad.endswith("sol") else (x0 + 4, x1 - 4)       # sol: robot çöpü kızağı x 16'dan başlar
        g.kaynak(S.kaynak_dikisi((xa_, YTB, ZC0), (xb_, YTB, ZC0), (0, 1.0, 0), (0, 0, -1.0), 2.0, ad=ad + "_taban_kaynagi_arka", birim=g.birim,
                                 taraf="iç (sızdırmaz)", not_="dikme ↔ taban"))
        for xs, nx in ((x0, -1.0), (x1, 1.0)):
            if (ad.endswith("sol") and nx < 0) or (ad.endswith("sag") and nx > 0): continue
            g.kaynak(S.kaynak_dikisi((xs, YTB, ZC0 + 4), (xs, YTB, ZON - 4), (0, 1.0, 0), (nx, 0, 0), 2.0, ad=ad + "_taban_kaynagi_%s" % ("sol" if nx < 0 else "sag"),
                                     birim=g.birim, taraf="iç (sızdırmaz)", not_="dikme ↔ taban"))
    g.not_("taban + ön kasa KAYNAKLI ALT MONTAJ: dikmeler tabana (arka + iç yan köşe dikişi, a2), kayıtlar dikmelere (alt/üst köşe dikişi; ön/arka yüz alın, taşlanır) · "
           "dikme tepeleri 2 mm tapa (çevresi TIG alın, taşlanır)")
    return P


def yan(g, taraf):
    """sol: x 0–1,5 (n +x) · sağ: x 830–828,5 (n −x) · arka iç dönüş · ön kenar düz (dikme arkasında, kulaklarla)"""
    ad = "sol_sac_pizza_penceresi" if taraf == "sol" else "sag_sac"
    s = g.sac(ad, "dis", kabuk=True); gg = s.R + s.t
    if taraf == "sol":
        P = s.taban([(Y0, ZAI + gg), (YH, ZAI + gg), (YH, ZON), (Y0, ZON)], O=(0, 0, 0), ex=(0, 1, 0), ey=(0, 0, 1), ad="yan")
        zv = lambda z: z; k_arka = 0
    else:
        P = s.taban([(Y0, -ZON), (YH, -ZON), (YH, -ZAI - gg), (Y0, -ZAI - gg)], O=(W, 0, 0), ex=(0, 1, 0), ey=(0, 0, -1), ad="yan")
        zv = lambda z: -z; k_arka = 2
    # arka dönüş: sol tam boy (y 126–1855) · sağ yalnız kapı açıklığının üstünde (y 1000–1855; açıklık arka kenarı büküme 1,75 mm → DFM)
    y_a = YTB if taraf == "sol" else 1000.0
    kn = P.kenar(k_arka)
    if taraf == "sol": bas, son = y_a - Y0, YH - 1855.0
    else: bas, son = YH - 1855.0, y_a - Y0
    arka = P.flans(k_arka, YAN_ARKA, yon=+1, bas=bas, son=son, ad="arka_donus")
    g.PANEL[taraf] = dict(yan=P, arka=arka, s=s, zv=zv)
    if taraf == "sol":
        y0, y1, z0, z1 = PENCERE
        P.dikdortgen((y0 + y1) / 2.0, zv((z0 + z1) / 2.0), y1 - y0, z1 - z0, r=6.0, tip="pizza_penceresi", parca="K→E pizza penceresi (R6 köşe)")
        for y, z in K_M8:
            P.delik(y, zv(z), 9.0, tip="vida_deligi", parca="K↔E M8 (ISO 273 orta · cıvata E içinden, K dikmesindeki perçin somuna)")
        u0, u1, v0, v1 = J3["agiz"]
        P.dikdortgen(J3["Y0"] + (v0 + v1) / 2.0, zv(J3["c"] + (u0 + u1) / 2.0), v1 - v0 + 1.0, u1 - u0 + 1.0, r=1.0, tip="j3_gecis_agzi",
                     parca="J3 birleşim paneli contalı geçiş ağzı 57 × 67 (EPDM kovan 56 × 66 geçme, çevre 0,5)")
    else:
        y0, y1, z0, z1 = SARJOR_AC
        P.dikdortgen((y0 + y1) / 2.0, zv((z0 + z1) / 2.0), y1 - y0, z1 - z0, r=0.0, tip="sarjor_kapi_acikligi", dfm=False,
                     parca="şarjör yan kapısı açıklığı (lazer · çıkan parça kapının dış sacı olur, 3 mm derz)")
    return s, P


def arka_sac(g):
    s = g.sac("arka_sac", "dis"); gg = s.R + s.t
    P = s.taban([(0.0, YTB + gg), (W, YTB + gg), (W, YTV - gg - 0.5), (0.0, YTV - gg - 0.5)], O=(0, 0, ZA), ex=(1, 0, 0), ey=(0, 1, 0), ad="arka")   # n = +z (içe)
    # üst iç dönüş: üst yüzü 1860,5 (üst sacın altı) · yan sacların ve üst sac yan dönüşlerinin arasında
    ust = P.flans(2, 24.0, yon=+1, bas=4.0, son=4.0, ad="ust_donus")                 # üst yüzü 1860,0 (üst saca 0,5 hava · FHP somunu sıkınca kapanır)
    # alt iç dönüş: taban üstünde (y 126) — tabanın arka kenarı arka sacın iç yüzüne dayalı; dönüş yan dönüşlerin arasında
    alt = P.flans(0, 24.0, yon=+1, bas=18.5, son=18.5, ad="alt_donus", olcu="dis")
    g.PANEL["arka"] = dict(arka=P, ust=ust, alt=alt, s=s)
    return s, P


def ust_sac(g):
    s = g.sac("ust_sac", "dis"); gg = s.R + s.t
    P = s.taban([(T + gg, -ZON), (W - T - gg, -ZON), (W - T - gg, -ZA), (T + gg, -ZA)], O=(0, YTV, 0), ex=(1, 0, 0), ey=(0, 0, -1), ad="ust")   # n = +y · y 1860,5–1862
    # yan dönüşler AŞAĞI (yon −1): dış yüzü x 1,5 / 828,5 (yan sacların iç yüzü; yan saclar y 1862'ye kadar çıkar, üst sac aralarına oturur) · dış ölçü 21,5
    sag = P.flans(1, UST_YAN + T, yon=-1, bas=ZON - ZC0 + 1.0, son=8.0, ad="sag_donus")    # kenar 1: x = W − 1,5 − g (ön → arka) · önde dikme (z 29–59)
    sol = P.flans(3, UST_YAN + T, yon=-1, bas=8.0, son=ZON - ZC0 + 1.0, ad="sol_donus")    # kenar 3: (arka → ön)
    x0, x1, z0, z1 = HARTING
    P.dikdortgen((x0 + x1) / 2.0, -(z0 + z1) / 2.0, x1 - x0, z1 - z0, r=2.0, tip="harting_kesigi", parca="E Harting Han 10B soket kesiği 66 × 36 (U_KE tabanındakiyle aynı)")
    g.PANEL["ust"] = dict(ust=P, sol=sol, sag=sag, s=s)
    return s, P


def ust_sac_poly_duzelt(g):
    """üst sac yan sacların üstüne biner (x 0 … 830): taban poligonu g kadar içeriden başlar, yan dönüş bükümü + R dış köşe → dış zarf x 0–830 değil
    1,5 + … — dönüşlerin dış yüzü x 1,5 / 828,5. Üst sacın kendisi x 1,5 – 828,5 arasında kalır; yan sacların tepe kenarı (y 1860,5) üst sacın altına
    dayanır, dış köşe yan sacın dış yüzüyle hizalı DEĞİL (1,5 içeride) → dış zarf için üst sac yan kenarları 1,5 taşırılır: dönüşün dış ölçüsü 20."""
    pass


def kulaklar(g):
    """yan saclar: taban üstünde (y 145) ve dikme arka yüzünde (z 10) · üst sac: dikme tepelerinde (z 10) — 3 mm L, FHP-M5 saplama + pul + fiberli somun"""
    L, R_ = g.PANEL["sol"]["yan"], g.PANEL["sag"]["yan"]
    # taban kulakları — mekanizma ayak izlerinin dışında (E_COP kızağı z −397…29 sol · eşik z −414…−399 · şarjör)
    for tr, A, xs, sx, zs in (("sol", L, 1.5, 1.0, (-790.0, -620.0, -470.0)), ("sag", R_, W - 1.5, -1.0, (-760.0, -620.0, -470.0, -300.0, -150.0, -30.0))):
        for z in zs:
            GO.kulak(g, "govde_kulak_%s_taban_%d" % (tr, int(-z)), A, (xs, YTB + 19.0, z), (0, 0, 1.0 * sx), (0, -1.0, 0), 19.0, L_kaynak=24.0, gen=25.0)
    # dikme arka yüzü kulakları (yan sacın ön kenarı)
    for tr, A, xs, sx, (d0, d1) in (("sol", L, 1.5, 1.0, DS), ("sag", R_, W - 1.5, -1.0, DG)):
        for y in (250.0, 450.0, 620.0, 850.0, 1100.0, 1300.0, 1500.0, 1700.0, 1820.0):
            kulak(g, "govde_kulak_%s_on_%d" % (tr, int(y)), A, (xs, y, ZC0 - 19.0), (0, 1.0 * sx, 0), (0, 0, 1.0), 19.0, L_kaynak=16.0, gen=25.0, t=2.0)   # dikme 20: 2 mm kulak
    # üst sac ↔ dikme tepeleri
    U = g.PANEL["ust"]["ust"]
    for ad, xc, gen, tk in (("sol", 13.0, 12.0, 1.5), ("orta", (DO[0] + DO[1]) / 2.0, 18.0, None), ("sag", W - 13.0, 12.0, 1.5)):
        # yan dikmeler 20 genişlikte: 1,5 kulak (kaynak dikişi a1,5 dikme yüzünde kalır) · saplama yan dönüş bükümünden ≥ 9,45 (PEM kuralı) → x 13
        kulak(g, "govde_kulak_ust_%s" % ad, U, (xc, YTV, ZC0 - 19.0), (1.0, 0, 0), (0, 0, 1.0), 19.0, L_kaynak=16.0, gen=gen, t=tk, pul_std="DIN125" if tk else "DIN9021")


def panel_baglantilari(g):
    """yan ↔ arka (arka sactan FHP · içten somun) · yan ↔ üst (yan sactan FHP · üst sacın yan dönüşünde somun) · üst ↔ arka (üst sactan FHP · arka sacın
    üst dönüşünde somun) · taban ↔ arka alt dönüş (tabandan FHP) · sağ alt köşebent"""
    A = g.PANEL["arka"]["arka"]
    for tr, xx in (("sol", 10.5), ("sag", W - 10.5)):
        B = g.PANEL[tr]["arka"]
        ys = [y for y in dizi(YTB if tr == "sol" else 1000.0, 1855.0, maks=200.0, uc=35.0) if not (1600 < y < 1665)]
        for y in ys:
            bag(g, A, B, (xx, y, ZA), "govde_bag_arka_%s_%d" % (tr, int(y)), dis="M5", boy=10)     # saplama ucu z −820 (karton yığını −819)
    U = g.PANEL["ust"]["ust"]
    for tr, xs in (("sol", 0.0), ("sag", W)):
        A_ = g.PANEL[tr]["yan"]; B = g.PANEL["ust"][tr]
        for z in dizi(-790.0, 0.0, maks=200.0, uc=10.0):
            bag(g, A_, B, (xs, 1849.0, z), "govde_bag_ust_%s_%d" % (tr, int(-z)), dis="M5")
    Bu = g.PANEL["arka"]["ust"]
    for x in dizi(40.0, W - 40.0, maks=200.0, uc=10.0):
        bag(g, U, Bu, (x, YH, -815.0), "govde_bag_ust_arka_%d" % int(x), dis="M5")
    Tb = g.PANEL["taban"]; Ba = g.PANEL["arka"]["alt"]
    for x in dizi(60.0, W - 60.0, maks=200.0, uc=10.0):
        bag(g, Tb, Ba, (x, Y0, -815.0), "govde_bag_taban_arka_%d" % int(x), dis="M5")
    # sağ arka alt köşebent (yan sacın arka dönüşü kapı açıklığı yüzünden y < 1000'de yok): 3 mm L · arka sac + yan sac FHP
    s = g.sac("govde_kosebent_sag_arka_alt", "braket")
    tt, R = s.t, s.R
    Pk = s.taban([(W - 1.5 - 32.0, 140.0), (W - 1.5 - tt - R, 140.0), (W - 1.5 - tt - R, 220.0), (W - 1.5 - 32.0, 220.0)], O=(0, 0, ZAI), ex=(1, 0, 0), ey=(0, 1, 0), ad="arka_ayak")
    Fk = Pk.flans(1, 32.0, yon=+1, ad="yan_ayak")
    bag(g, A, Pk, (W - 22.0, 180.0, ZA), "govde_bag_kosebent_arka", dis="M5")
    bag(g, g.PANEL["sag"]["yan"], Fk, (W, 180.0, ZAI + 22.0), "govde_bag_kosebent_yan", dis="M5")


def kapaklar(g):
    KK = {}
    for kn, (x0, x1, y0, y1) in KAPAK.items():
        K = GO.kapak(g, "onyuz_kapak_E_%s" % kn, x0, x1, y0, y1, w_dis=ZK, w_ic=ZON, ustte="yatay")
        KK[kn] = K
        if kn == "ust_sol":
            a0, a1, b0, b1 = AGIZ
            GO.aciklik(K, "robot_agzi", (a0 + a1) / 2.0, (b0 + b1) / 2.0, a1 - a0, b1 - b0, r=0.0, tip="pencere", kasa=True, kasa_ayak=10.0)
        if kn == "alt_sol":
            a0, a1, b0, b1 = KLAPE_AC
            K.D.dikdortgen((a0 + a1) / 2.0, (b0 + b1) / 2.0, a1 - a0, b1 - b0, tip="klape_acikligi", parca="robot çöpü klape açıklığı 130 × 130 (ön yüz)")
            a0, a1, b0, b1 = KLAPE_IC
            K.I.dikdortgen((a0 + a1) / 2.0, (b0 + b1) / 2.0, a1 - a0, b1 - b0, tip="klape_donus_deligi", parca="klape levhası + yaprak dönüş deliği 144 × 168 (iç tava)")
    g.KAPAK_E = KK
    return KK


def menteseler(g, KK):
    """gizli 180° kaldır-çıkar menteşe (Southco R6 / EMKA 1046 sınıfı · ölçüler TEMSİLİ): GÖVDE yarısı yan dikmenin içinde (ön duvarda 12 × 60 pencere ·
    dikmenin istasyona bakan yan duvarından 2 × ISO 7380 M5) · KANAT yarısı: kol pencereden geçer, iç tavadaki cepten kapak boşluğuna, plaka iç tavaya 4 punta"""
    P = g.PROF
    for kn, K in KK.items():
        alt_ust, tr = kn.split("_")
        d = P["onyuz_dikme_sol"] if tr == "sol" else P["onyuz_dikme_sag"]
        x0, x1 = (DS if tr == "sol" else DG)
        xc = (x0 + x1) / 2.0; sg = 1.0 if tr == "sol" else -1.0           # sg: istasyon içine (+x sol)
        xi = x1 if tr == "sol" else x0                                      # dikmenin iç yan yüzü
        K.mentese_kenari = tr
        for j, y in enumerate(MENT_Y[alt_ust]):
            i = j + (0 if alt_ust == "alt" else 3)
            ad = "onyuz_kapak_E_mentese_%s_%d" % (tr, i)
            ym = y + MENT_H / 2.0
            d.duvar_pencere("+z", ym, 0.0, MENT_H, 12.0, tip="mentese_penceresi", not_="gizli menteşe gövdesi + kol")
            for dy in (-15.0, 15.0):
                d.duvar_delik("+x" if tr == "sol" else "-x", ym + dy, 44.0 - (ZC0 + ZON) / 2.0, 5.5, tip="mentese_vidasi", not_="menteşe gövdesi 2 × M5")
            gx0, gx1 = sorted((xc - sg * 5.5, xc + sg * 5.5))
            gov = kutu(gx0, gx1, y, y + MENT_H, 33.0, ZON - 2.0)
            for dy in (-15.0, 15.0):
                gov = gov.cut(GO.silindir((xc - sg * 6.0, ym + dy, 44.0), (sg, 0, 0), 2.5, 12.0))
            g.eleman(g.ozel(ad + "_sabit", gov, "Southco R6 / EMKA 1046 sınıfı", "Gizli 180° kaldır-çıkar menteşe · GÖVDE yarısı (dikme içinde) AISI 316",
                            "11 × 60 × 24 · 2 × M5 (dikme iç yan duvarından)", malzeme="AISI 316 pasive", mal="celik",
                            meta=dict(kaldir_cikar=True, aci=180, kenar=tr, pivot=[K.u0 if tr == "sol" else K.u1, ym, ZK])), sabit=K)
            for dy, ek in ((-15.0, "a"), (15.0, "b")):
                g.eleman(S.vida("ISO7380", "M5", 10, (xi, ym + dy, 44.0), (-sg, 0, 0), ad=ad + "_sabit_vida_" + ek, birim=g.birim), sabit=K)
            # kanat: kol (dikme ön duvarı penceresinden) + cep kutusu (kapak boşluğunda) + plaka (iç tava ön yüzünde, 4 punta)
            kx0, kx1 = sorted((xc - sg * 1.5, xc + sg * 5.5))
            px0, px1 = sorted((xc - sg * 1.5, xc + sg * 30.0))
            kanat = GO.bir(kutu(kx0, kx1, y + 8, y + MENT_H - 8, ZON - 2.0, ZON + K.ki.t),
                           kutu(px0, px1, y - 5, y + MENT_H + 5, ZON + K.ki.t, ZON + K.ki.t + 1.5),
                           kutu(kx0, kx1, y + 8, y + MENT_H - 8, ZON + K.ki.t + 1.5, ZON + 12.0))
            g.eleman(g.ozel(ad + "_kanat", kanat, "Southco R6 / EMKA 1046 sınıfı", "Gizli 180° kaldır-çıkar menteşe · KANAT yarısı + kol (kapakla döner) · plaka iç tavaya 4 punta",
                            "kol 7 × 44 · plaka 31,5 × 70 × 1,5", malzeme="AISI 316 pasive", mal="celik", meta=dict(kapakla_doner=True)), doner=K)
            K.I.dikdortgen((kx0 + kx1) / 2.0, ym, (kx1 - kx0) + 1.0, MENT_H - 16.0 + 1.0, tip="mentese_cebi", parca="menteşe kolu geçişi (iç tava)")
            g.not_("%s: kanat plakası iç tavaya 4 punta (kapak kapanmadan önce, iç tava ön yüzü)" % ad)
            K.menteseler.append(dict(ad=ad, kenar=tr, konum=ym, dikme=d.ad))


def basaclar(g, KK):
    """bas-aç (push-to-open, Southco 97 / EMKA 1080 sınıfı): orta dikmenin ön duvarında Ø12,2 · gövde dikmenin içinde · pim kapağın iç tavasına basar
    (iç tava ön yüzünde 1,5 karşılık plakası, 2 punta)"""
    d = g.PROF["onyuz_dikme_orta"]
    for kn, K in KK.items():
        alt_ust, tr = kn.split("_")
        x = BASAC_X[tr]
        for j, y in enumerate(BASAC_Y[alt_ust]):
            i = j + (0 if alt_ust == "alt" else 1)
            ad = "onyuz_kapak_E_basac_%s_%d" % (tr, i)
            d.duvar_delik("+z", y, x - (DO[0] + DO[1]) / 2.0, 12.2, tip="basac_deligi", not_="bas-aç gövdesi (geçme Ø12)")
            sh = GO.silindir((x, y, 33.0), (0, 0, 1.0), 6.0, ZON - 33.0).fuse(GO.silindir((x, y, ZON - 4.0), (0, 0, 1.0), 7.0, 1.5))
            g.eleman(g.ozel(ad, sh, "Southco 97 / EMKA 1080 sınıfı", "Bas-aç mandalı (push-to-open, geçme gövde Ø12 · flanş dikme ön duvarının arkasında) · pim iç tavaya basar",
                            "Ø12 × 26 · flanş Ø14 × 1,5 · strok 7", malzeme="AISI 316 / POM", mal="siyah"), sabit=K)
            if kn == "ust_sol" and AGIZ[2] - 15 < y < AGIZ[3] + 15:
                g.not_("%s: karşılık plakası yok — robot ağzı kasa çıtası (iç tavaya punta) pimin bastığı yüzü taşır" % ad)
                K.basaclar.append(dict(ad=ad, kenar=tr, konum=y)); continue
            dp = g.sac("onyuz_kapak_E_%s_karsilik_%d" % (kn, j), "dis", mal=K.mal, doner=K)
            xa, xb = (x - 10.0, x + 3.5) if tr == "sol" else (x - 3.5, x + 10.0)
            dp.taban([(xa, y - 15), (xb, y - 15), (xb, y + 15), (xa, y + 15)], O=(0, 0, ZON + K.ki.t), ex=(1, 0, 0), ey=(0, 1, 0), ad="plaka")
            dp.punta(K.ki, [((xa + xb) / 2.0, y - 10, ZON + K.ki.t), ((xa + xb) / 2.0, y + 10, ZON + K.ki.t)], not_="karşılık plakası → iç tava")
            K.basaclar.append(dict(ad=ad, kenar=tr, konum=y))


def sarjor_kapisi(g):
    """şarjör yan kapısı: dış sac 1,5 (sağ sacın açıklığından çıkan parça, 3 mm derz) + iç tava 1,5 (4 dönüş dış saca punta) · 2 gizli menteşe
    (arka sac üstündeki 3 mm taşıyıcı lamaya) · bas-aç (yan saca FHP'li 3 mm lamada)"""
    kd = g.sac("sarjor_yan_kapisi", "kapak_dis", kabuk=True)
    D = kd.taban([(KAPI["y"][0], -KAPI["z"][1]), (KAPI["y"][1], -KAPI["z"][1]), (KAPI["y"][1], -KAPI["z"][0]), (KAPI["y"][0], -KAPI["z"][0])],
                 O=(W, 0, 0), ex=(0, 1, 0), ey=(0, 0, -1), ad="dis")        # n = y × (−z) = −x (içe) · x 830 → 828,5
    ki = g.sac("sarjor_yan_kapisi_ic_tava", "dis")
    tx = KAPI["tava_x"]; gi = ki.R + ki.t
    (ya, yb), (za, zb) = KAPI["tava_y"], KAPI["tava_z"]
    I = ki.taban([(ya + gi, -zb + gi), (yb - gi, -zb + gi), (yb - gi, -za - gi), (ya + gi, -za - gi)], O=(tx + ki.t, 0, 0), ex=(0, 1, 0), ey=(0, 0, -1), ad="tava")
    don = 13.0                                                                 # iç tava dış yüzü (x 815,5) → dış sac iç yüzü (828,5)
    fi = [I.flans(i, don, yon=-1, ad=a) for i, a in enumerate(("on_donus", "ust_donus", "arka_donus", "alt_donus"))]
    for i in range(4): ki.kose(fi[i], fi[(i + 1) % 4], "acik")
    nok = [(W - 1.5, y, KAPI["tava_z"][1] - 0.5) for y in np.arange(280.0, 960.0, 150.0)] + [(W - 1.5, y, KAPI["tava_z"][0] + 0.5) for y in np.arange(280.0, 960.0, 150.0)]
    ki.punta(kd, nok, not_="iç tava dönüşleri → dış sac (≈150 aralık)")
    g.PANEL["kapi"] = dict(dis=D, ic=I, kd=kd, ki=ki)
    # menteşe taşıyıcı lama (3 mm) arka sacın iç yüzünde · arka sactan 3 × FHP
    lm = g.sac("sarjor_yan_kapisi_mentese_lamasi", "braket", t=2.0)
    L = lm.taban([(812.5, 245.0), (828.4, 245.0), (828.4, 975.0), (812.5, 975.0)], O=(0, 0, ZAI), ex=(1, 0, 0), ey=(0, 1, 0), ad="lama")
    for y in (420.0, 600.0, 780.0):
        bag(g, g.PANEL["arka"]["arka"], L, (820.5, y, ZA), "govde_bag_kapi_lamasi_%d" % int(y), dis="M5")
    for i, yc in enumerate(KAPI["ment_y"]):
        ad = "sarjor_yan_kapisi_mentese_%d" % i
        gov = kutu(819.0, 826.5, yc - 25.0, yc + 25.0, ZAI + 2.0, -814.0)
        g.eleman(g.ozel(ad, gov, "Southco E6 sınıfı", "Gizli menteşe · GÖVDE yarısı (taşıyıcı lamaya 2 × M5 vida, lamada diş)", "7,5 × 50 × 11,5",
                        malzeme="AISI 316 pasive", mal="celik"))
        lm_del = [(820.5, yc - 15.0), (820.5, yc + 15.0)]
        for (xx, yy) in lm_del: L.delik(xx, yy, 4.2, tip="dis_delik", parca="M5 diş (3 mm lama · kılavuz)")
        kan = kutu(819.0, 826.5, yc - 20.0, yc + 20.0, -814.0, KAPI["tava_z"][0])
        g.eleman(g.ozel(ad + "_kanat", kan, "Southco E6 sınıfı", "Gizli menteşe · KANAT yarısı (iç tava arka dönüşünün arka yüzüne 2 punta)", "7,5 × 40 × 2",
                        malzeme="AISI 316 pasive", mal="celik", meta=dict(kapakla_doner=True)))
    # bas-aç lama (yan sacın iç yüzünde, açıklığın önünde) · yan sactan 2 × FHP
    ba = g.sac("sarjor_yan_kapisi_basac_lamasi", "braket")
    B = ba.taban([(KAPI["basac_y"] - 30.0, 380.0), (KAPI["basac_y"] + 30.0, 380.0), (KAPI["basac_y"] + 30.0, 409.5), (KAPI["basac_y"] - 30.0, 409.5)],
                 O=(W - 1.5, 0, 0), ex=(0, 1, 0), ey=(0, 0, -1), ad="lama")         # n = −x · x 828,5 → 825,5 · z −380 … −409,5
    for y in (KAPI["basac_y"] - 18.0, KAPI["basac_y"] + 18.0):
        bag(g, g.PANEL["sag"]["yan"], B, (W, y, -395.0), "govde_bag_kapi_basac_%d" % int(y), dis="M5")
    bs = kutu(819.0, 825.5, KAPI["basac_y"] - 10.0, KAPI["basac_y"] + 10.0, -418.3, -406.0)
    g.eleman(g.ozel("sarjor_yan_kapisi_basac", bs, "Southco 97 sınıfı", "Bas-aç (push-to-open) · lamaya 2 × M4", "6,5 × 20 × 12", malzeme="AISI 316 / POM", mal="siyah"))
    g.not_("şarjör kapısı: menteşe kanatları iç tava arka dönüşüne punta · kapı açıklığında çevre derz 3 mm · iç tavada sağ UHMW kılavuz (3 mm) havşa vidalı (mevcut)")


def kaide(g):
    """E_MODULER yerine AYNI ölçüde kaynaklı kaide: 2 boy ray 60 × 60 × 3 (x 1,5–828,5) + 2 uç kayıt 60 × 60 × 3 + orta kayıt 40 × 60 × 3 · 6 ayarlı ayak M12"""
    yc = (KAIDE_Y[0] + KAIDE_Y[1]) / 2.0
    R = {}
    for z0, z1, ad in ((-790.0, -730.0, "arka"), (-140.0, -80.0, "on")):
        R[ad] = g.profil("kaide_e_ray_%s" % ad, "x", DS[0] + 3.0, DG[1] - 3.0, (yc, (z0 + z1) / 2.0), b=60.0, t=3.0, not_="kaide boy rayı (uçlar 3 mm tapa)")
    for ad, (x0, x1), b in (("sol", (1.5, 61.5), 60.0), ("orta", (395.0, 435.0), 40.0), ("sag", (768.5, 828.5), 60.0)):
        if b == 60.0: k = g.profil("kaide_e_kayit_%s" % ad, "z", -730.0, -140.0, ((x0 + x1) / 2.0, yc), b=60.0, t=3.0, not_="kaide uç kaydı")
        else: k = profil_d(g, "kaide_e_kayit_%s" % ad, "z", -730.0, -140.0, ((x0 + x1) / 2.0, yc), x1 - x0, 60.0, t=3.0, not_="kaide orta kaydı")
        for z, e in ((-730.0, (0, 0, 1.0)), (-140.0, (0, 0, -1.0))):
            yz_ = {"sol": [(1.0, 0, 0)], "sag": [(-1.0, 0, 0)], "orta": [(1.0, 0, 0), (-1.0, 0, 0)]}[ad]     # dış yüzler ray ucuyla aynı düzlem → alın
            g.kaynak(GO.uc_kaynaklari("kaide_e_kayit_%s_kaynak_%d" % (ad, int(-z)), ((x0 + x1) / 2.0, yc, z), e, yz_,
                                      b=b, a=3.0, flat=60.0 - 12.0, Ro=6.0, birim=g.birim))
            rr = R["arka" if z < -400 else "on"]
            rr.kaynak_bolgesi("+z" if z < -400 else "-z", x0, x1)
    for i, (x, z) in enumerate(AYAK_XZ):
        rr = R["arka" if z < -400 else "on"]
        rr.duvar_delik("-y", x, 0.0, 13.0, tip="ayak_deligi", not_="ayarlı ayak M12")
        g.eleman(S.kaynak_somunu("M12", (x, KAIDE_Y[0] + 3.0, z), (0, 1.0, 0), ad="kaide_e_ayak_somunu_%d" % i, birim=g.birim))
        for q in S.ayarli_ayak("M12", (x, 0.0, z), (0, 1.0, 0), KAIDE_Y[0], D_taban=40.0, ad="ayak_%d" % i, birim=g.birim): g.eleman(q, mal="celik")
    # taban ↔ kaide: ISO 7380 M8 (taban üstünden) + ray üst duvarı içinde DIN 929 M8 kaynak somunu
    Tb = g.PANEL["taban"]
    for z, ad, xs in ((-760.0, "arka", (120.0, 300.0, 530.0, 710.0)), (-110.0, "on", (230.0, 530.0, 710.0))):   # ön sıra: robot çöpü kızağı x 16–198 dışı
        for x in xs:
            R[ad].duvar_delik("+y", x, 0.0, 9.0, tip="m8_deligi", not_="taban ↔ kaide M8")
            Tb.delik(x, -z, 9.0, tip="vida_deligi", parca="taban ↔ kaide M8 (ISO 273 orta)")
            g.eleman(S.vida("ISO7380", "M8", 16, (x, YTB, z), (0, -1.0, 0), ad="kaide_e_vida_%s_%d" % (ad, int(x)), birim=g.birim))
            g.eleman(S.kaynak_somunu("M8", (x, KAIDE_Y[1] - 3.0, z), (0, -1.0, 0), ad="kaide_e_somun_%s_%d" % (ad, int(x)), birim=g.birim))
    g.not_("kaide: 60 × 60 × 3 boy rayları + uç kayıtlar 90° alın, köşe dikişi a3 (iç bükey yüzler) · ray alt duvarında Ø13 + DIN 929 M12 kaynak somunu (ayak) · "
           "ray üst duvarında Ø9 + içte DIN 929 M8 (taban bağlantısı) · ray uçları açık profil → 3 mm tapa (kaide_e_*_tapa)")
    for ad in ("arka", "on"):
        ts = GO.dikme_tapasi(g, R[ad], uc="ust", t=3.0, pah=3.0, ad="kaide_e_ray_%s_tapa_sag" % ad)
        ts2 = GO.dikme_tapasi(g, R[ad], uc="alt", t=3.0, pah=3.0, ad="kaide_e_ray_%s_tapa_sol" % ad)


def ust_m8(g):
    """U_KE ↔ E: üst sacta PEM SP-M8 (gövdesi E içine) · U_KE tabanından ISO 7380 M8 (arayüz)"""
    U = g.PANEL["ust"]["ust"]
    for x, z in U_M8:
        ps, c, ms = S.pem_somun("SP", "M8", (x, YTV, z), (0, -1.0, 0), U.sac.t, ad="govde_pem_m8_ust_%d" % int(x), birim=g.birim)
        ya = U.yerel((x, YH, z))
        U.delik(ya[0], ya[1], c["delik"], tip="pem_somun", parca=ps["meta"]["parca"], pem_tip="SP", kenar_min=c["kenar"], min_sac=ms)
        g.eleman(ps)
        g.arayuz(S.vida("ISO7380", "M8", 16, (x, YH + 1.5, z), (0, -1.0, 0), ad="arayuz_uke_m8_%d" % int(x), birim=g.birim), "U_KE_GOVDE ust_ke_taban_sac",
                 "U_KE tabanında Ø9 (aynı eksen) · ISO 7380 M8 × 16 A2 U_KE içinden", "U_KE ↔ E")
        g.KARSI_DELIK.append(dict(etiket="UKE_E_%d" % int(x), karsi="U_KE_GOVDE ust_ke_taban_sac", cap=9.0, merkez_dunya=[x + X_E, YH + 1.5, z]))


def elektrik(g):
    """J3 birleşim paneli 4 burcu: sol sacta FHP-M5 (arayüz: burç iç dişli değil → saplama burçtan + panel plakasından geçer, önde somun)"""
    L = g.PANEL["sol"]["yan"]
    for (u, v) in J3["burc"]:
        y, z = J3["Y0"] + v, J3["c"] + u
        fhp_arayuz(g, L, (0.0, y, z), (1.0, 0, 0), "ELK_ZINCIR J3 E paneli burcu", "burç Ø10 × 20 + panel plakası Ø5,5 · FHP-M5 × 25 · önde pul + fiberli somun",
                   boy=25, ad="arayuz_j3_burc_%d_%d" % (int(y), int(-z)), tip_not="elektrik")


# --------------------------------------------------------------------------------------------------- mekanizma temas saplamaları (otomatik)
def _bilesen_listesi():
    yol = os.path.join(_cikti(), "_bilesen_v8zq.pkl")
    return pickle.load(open(yol, "rb")) if os.path.exists(yol) else []


DUVARLAR = [  # (panel anahtarı, eksen, iç düzlem (yerel), işaret: parça hangi tarafta, dis, saplama yönü)
    ("sol", 0, 1.5, +1, "M5"), ("sag", 0, W - 1.5, -1, "M5"), ("arka", 2, ZAI, +1, "M5"), ("ust", 1, YTV, -1, "M5"), ("taban", 1, YTB, +1, "M6")]


def mekanizma_saplamalari(g, log=print):
    """duvarın iç yüzüne değen (±0,05) her mekanizma / elektrik bileşenine FHP saplama (yama 1 ya da 2 adet) · yeri güvenli değilse rapora"""
    L = _bilesen_listesi(); out, atla = [], []
    panel = {"sol": g.PANEL["sol"]["yan"], "sag": g.PANEL["sag"]["yan"], "arka": g.PANEL["arka"]["arka"], "ust": g.PANEL["ust"]["ust"], "taban": g.PANEL["taban"]}
    for anah, ax, d, sg, dis in DUVARLAR:
        P = panel[anah]
        for ad, lo, hi, n in L:
            if MEK_HARIC.search(ad): continue
            lo = np.array(lo, float) - np.array([X_E, 0, 0]); hi = np.array(hi, float) - np.array([X_E, 0, 0])
            yuz = lo[ax] if sg > 0 else hi[ax]
            if abs(yuz - d) > 0.06: continue
            o = [i for i in range(3) if i != ax]
            if lo[0] < -1 or hi[0] > W + 1: continue
            if hi[1] < Y0 or lo[1] > YH: continue
            a0, a1 = lo[o[0]], hi[o[0]]; b0, b1 = lo[o[1]], hi[o[1]]
            if min(a1 - a0, b1 - b0) < 9.0: atla.append((anah, ad, "yama dar")); continue
            if (a1 - a0) >= (b1 - b0): nok = [((a0 + a1) / 2.0 + s * (a1 - a0) / 4.0 if (a1 - a0) > 70 else (a0 + a1) / 2.0, (b0 + b1) / 2.0) for s in ((-1, 1) if (a1 - a0) > 70 else (0,))]
            else: nok = [((a0 + a1) / 2.0, (b0 + b1) / 2.0 + s * (b1 - b0) / 4.0 if (b1 - b0) > 70 else (b0 + b1) / 2.0) for s in ((-1, 1) if (b1 - b0) > 70 else (0,))]
            for (a, b) in nok:
                p = np.zeros(3); p[ax] = d; p[o[0]] = a; p[o[1]] = b
                ya = P.yerel(p)
                if not guvenli(P, ya[0], ya[1], kenar=12.0, delik=9.0): atla.append((anah, ad, "yer güvenli değil %s" % np.round(p, 1).tolist())); continue
                yon = np.zeros(3); yon[ax] = sg
                fhp_arayuz(g, P, p, yon, ad + " bbox %s" % [round(float(v), 1) for v in (lo[0] + X_E, hi[0] + X_E, lo[1], hi[1], lo[2], hi[2])],
                           "mekanizma tarafında Ø%.1f delik (FHP-%s saplama · pul + fiberli somun)" % (5.5 if dis == "M5" else 6.6, dis), dis=dis,
                           boy=12 if dis == "M5" else 15, ad="arayuz_mek_%s_%d" % (anah, len(out)))
                out.append((anah, ad, np.round(p, 1).tolist()))
    log("mekanizma temas saplaması: %d · atlanan %d" % (len(out), len(atla)))
    g.MEK_SAPLAMA, g.MEK_ATLA = out, atla
    return out, atla


def kur(log=print):
    t0 = time.time()
    g = GO.Govde(BIRIM, SURUM, istasyon="E", cerceve=GO.Cerceve("E", X_E))
    taban_ve_kasa(g)
    yan(g, "sol"); yan(g, "sag"); arka_sac(g); ust_sac(g)
    kulaklar(g); panel_baglantilari(g)
    KK = kapaklar(g); menteseler(g, KK); basaclar(g, KK)
    sarjor_kapisi(g); kaide(g); ust_m8(g); elektrik(g)
    mekanizma_saplamalari(g, log)
    saplama_duzelt(g, SAPLAMA_CIKAR, log=log)                      # ADIM 8
    g.doner_guncelle()
    log("%s · kuruldu: %d sac · %d profil · %d eleman · %d kaynak · %d birleşim · %d arayüz · %.1f sn" % (SURUM, len(g.SAC), len(g.PROF), len(g.ELEMAN), len(g.KAYNAK),
                                                                                                        len(g.BIRLESIM), len(g.ARAYUZ), time.time() - t0))
    return g


def govde_parcalari(g, dunya=True):
    return GO.govde_parcalari(g, hedef=GO.Cerceve("dunya") if dunya else None)


def uygula(MOD_PARCALAR, g=None, rapor=None):
    """montaj (SONRA, ayrı adım): eski E gövdesi → üretim sacı (dünya koordinatında yazılmış E düğümleri için dunya=True)"""
    g = g or kur()
    return GO.uygula(MOD_PARCALAR, govde_parcalari(g), ESKI_GOVDE, "onyuz_kapak_E_ust_sol_ic_tava", onekler=GOVDE_ONEK, rapor=rapor, etiket="E")


def _cikti():
    """çıktı klasörü: ADIM5 ortam değişkeni (gece 2: <scratchpad>/gece2/adim5) · yoksa sistem geçici klasörü (ana depoya YAZMAZ)"""
    import tempfile
    d = os.environ.get("ADIM5") or os.path.join(tempfile.gettempdir(), "autokitch_adim5")
    os.makedirs(d, exist_ok=True)
    return d


if __name__ == "__main__":
    sys.path.insert(0, _cikti())
    import sac_denetim_5b as DEN                                    # <scratchpad>/gece2/adim5/sac_denetim_5b.py (yalnız denetim + çıktı)
    DEN.calistir_E(sys.modules[__name__], hizli="--hizli" in sys.argv)
    sys.stdout.flush(); os._exit(0)
