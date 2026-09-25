# -*- coding: utf-8 -*-
"""BELDOS MINI-FILL ELEKTRO-PNÖMATİK + BELTOP UNO 275 (SEHPASIZ) · 3B MODEL v1 (25 Eyl 2026)

Kemal (25 Eyl 2026, beldos.com ekran görüntüsüyle): "Bana şu Beldos firması var ya, onun bir Mini ve şunların
modellemesini yap; ama Beltop UNO'da gereksiz parçaları sil, ayaklık, sac büküm var ya onun gibi. Yeterli veri
bulamazsan buna benzeyen başka markalar var, teknik resimleri olabilir; bul ve modelle."
Ekran görüntüsündeki iki makine: Mini-fill Electro-pneumatic (15 L hazne + pnömatik dik ağız) · Beltop UNO 275.
Başka marka gerekmedi: Beldos'un iki broşüründe ölçülü ve ölçekli çizim var.

HER ÖLÇÜNÜN KAYNAK ETİKETİ
  [B] broşürde yazan ölçü   (Mini-fill EN 2021 s.6 · Beltop UNO 08012023 s.2 ve s.6)
  [Ö] broşürün ölçekli çiziminden okundu: piksel × ölçek; ölçek broşürdeki ölçülerden (UNO 2,28 px/mm @14x ·
      Mini-fill 1,322 px/mm @5x) · hata ±3 mm
  [F] ürün fotoğrafından oranla (±10 mm)
  [H] broşür verisinden hesap (hesap satırı yanında)
  [V] VARSAYIM: görünmüyor ya da yazmıyor
  [BİZİM] Beldos'ta yok, bizim ekledimiz parça

KOORDİNAT: X sağa, Y ARKAYA (+), Z yukarı, mm. Ön yüz −Y'de (sağ el kuralı). GLB'de ön +z'ye bakar.
  Mini-fill: X 0 = gövdenin sol ucu, Y 0 = gövdenin ön yüzü, Z 0 = masa.
  UNO:       X 0 = döner valf / hazne ekseni, Y 0 = aynı eksen düzlemi, Z 0 = SİLİNEN SAC KAİDENİN ÜST YÜZÜ.
ÇIKTI: otonom/hat3d/beldos_minifill_ep_v1.glb · beldos_uno275_v1.glb · beldos_v1.json (ölçüm + parça kaynakları)
STEP / SolidWorks çıktısı YOK (Kemal 25 Eyl: "SolidWorks için bir şey yapmayacağız").
"""
import json, math, os, struct, sys, time
import cadquery as cq

U = os.path.dirname(os.path.abspath(__file__))
KOK = os.path.dirname(os.path.dirname(U))
OUT = os.path.join(KOK, "otonom", "hat3d")
MM = 0.001

MALZEME = {
    "beyaz":        dict(renk=(0.93, 0.93, 0.91, 1.0), met=0.0, ruf=0.45),
    "siyah":        dict(renk=(0.07, 0.07, 0.08, 1.0), met=0.1, ruf=0.6),
    "paslanmaz":    dict(renk=(0.80, 0.82, 0.85, 1.0), met=0.95, ruf=0.26),
    "fircali":      dict(renk=(0.74, 0.76, 0.79, 1.0), met=0.9, ruf=0.42),
    "pc":           dict(renk=(0.86, 0.92, 0.97, 0.30), met=0.0, ruf=0.05, saydam=True),
    "pp":           dict(renk=(0.96, 0.96, 0.95, 0.66), met=0.0, ruf=0.35, saydam=True),
    "pom":          dict(renk=(0.96, 0.96, 0.94, 1.0), met=0.0, ruf=0.4),
    "kirmizi":      dict(renk=(0.82, 0.10, 0.08, 1.0), met=0.0, ruf=0.5),
    "ekran":        dict(renk=(0.10, 0.03, 0.03, 1.0), met=0.2, ruf=0.2),
    "ekran_tus":    dict(renk=(0.85, 0.22, 0.14, 1.0), met=0.0, ruf=0.4),
    "aluminyum":    dict(renk=(0.80, 0.82, 0.85, 1.0), met=0.9, ruf=0.3),
    "mavi":         dict(renk=(0.15, 0.35, 0.75, 1.0), met=0.0, ruf=0.5),
    "saydam_celik": dict(renk=(0.82, 0.85, 0.89, 0.32), met=0.6, ruf=0.25, saydam=True),
    "kabuk":        dict(renk=(0.78, 0.81, 0.85, 0.24), met=0.4, ruf=0.35, saydam=True),
    "bizim":        dict(renk=(0.30, 0.55, 0.95, 0.45), met=0.0, ruf=0.6, saydam=True),
}
TR = {"guc": "güç", "unitesi": "ünitesi", "govde": "gövde", "sag": "sağ", "tusu": "tuşu", "girisi": "girişi", "blogu": "bloğu",
      "seffaf": "şeffaf", "cikis": "çıkış", "agzi": "ağzı", "bilezigi": "bileziği", "flansi": "flanşı", "kelepcesi": "kelepçesi",
      "kanadi": "kanadı", "kapagi": "kapağı", "agiz": "ağız", "halkasi": "halkası", "manson": "manşon", "pnomatik": "pnömatik",
      "baglanti": "bağlantı", "kirmizi": "kırmızı", "kivrimi": "kıvrımı", "bandi": "bandı", "contasi": "contası", "donen": "dönen",
      "isareti": "işareti", "dondurme": "döndürme", "aktuatoru": "eyleyicisi", "urun": "ürün", "korugu": "körüğü", "saci": "sacı",
      "cizgi": "çizgi", "hizli": "hızlı", "sokme": "sökme", "hiz": "hız", "bogaz": "boğaz", "on": "ön", "dayamasi": "dayaması",
      "sartlandirici": "şartlandırıcı", "kabi": "kabı", "plakasi": "plakası", "kavramasi": "kavraması", "kelebegi": "kelebeği",
      "derece": "°", "2lob": "(2 loblu)", "BIZIM": "(BİZİM)", "mili": "mili", "D52": "Ø52", "D32": "Ø32", "D12": "Ø12",
      "tc": "TC", "25L": "25 L", "15L": "15 L", "ic": "iç", "uzun": "uzun", "2.5in": '2,5"', "ekran": "ekran", "tuslari": "tuşları", "doner": "döner", "kelepce": "kelepçe", "giris": "giriş"}


def gorunen_ad(ad):
    w = [TR.get(k, k) for k in ad.split("_")]
    s_ = " ".join(w).replace(" °", "°")
    return s_[:1].upper() + s_[1:]


KAYNAK_AD = {"B": "broşürde yazan ölçü", "Ö": "broşürün ölçekli çiziminden", "F": "fotoğraftan oranla",
             "H": "broşür verisinden hesap", "V": "VARSAYIM", "BİZİM": "Beldos'ta yok · bizim"}


# ================================================================ yardımcılar
def kati(x):
    if isinstance(x, cq.Workplane):
        v = [o for o in x.vals() if isinstance(o, cq.Shape)]
        return v[0] if len(v) == 1 else cq.Compound.makeCompound(v)
    return x


def kutu(x0, x1, y0, y1, z0, z1):
    return cq.Workplane("XY").box(abs(x1 - x0), abs(y1 - y0), abs(z1 - z0), centered=False).translate((min(x0, x1), min(y0, y1), min(z0, z1)))


def silx(y, z, r, x0, x1): return cq.Workplane("YZ").center(y, z).circle(r).extrude(x1 - x0).translate((x0, 0, 0))
def sily(x, z, r, y0, y1): return cq.Workplane("XZ").center(x, z).circle(r).extrude(-(y1 - y0)).translate((0, y0, 0))
def silz(x, y, r, z0, z1): return cq.Workplane("XY").center(x, y).circle(r).extrude(z1 - z0).translate((0, 0, z0))


def dondur(profil, cx, cy):
    """(r, z) kapalı profil → düşey eksen (cx, cy) etrafında 360°"""
    return cq.Workplane("XZ").polyline(profil).close().revolve(360, (0, 0, 0), (0, 1, 0)).translate((cx, cy, 0))


def kabuk_profili(dis, t):
    """dış çizgi (alttan üste) + t kalınlık içeride → kapalı ince duvar profili"""
    ic = [(max(r - t, 0.5), z) for r, z in reversed(dis)]
    return list(dis) + ic


def boru(noktalar, r):
    """nokta dizisinden dolu boru: parça silindirler + eklem küreleri"""
    ss = []
    for a, b in zip(noktalar[:-1], noktalar[1:]):
        v = cq.Vector(*b) - cq.Vector(*a)
        if v.Length < 1e-6:
            continue
        ss.append(cq.Solid.makeCylinder(r, v.Length, cq.Vector(*a), v.normalized()))
    for p in noktalar[1:-1]:
        ss.append(cq.Solid.makeSphere(r, cq.Vector(*p), angleDegrees1=-90, angleDegrees2=90))
    return cq.Compound.makeCompound(ss)


def hortum(kontrol, r):
    """kontrol noktalarından geçen yumuşak eğri (B-spline) boyunca Ø2r süpürme"""
    yol = cq.Wire.assembleEdges([cq.Edge.makeSpline([cq.Vector(*p) for p in kontrol])])
    e = yol.Edges()[0]
    prof = cq.Wire.makeCircle(r, e.startPoint(), e.tangentAt(0))
    return cq.Solid.sweep(prof, [], yol, True, True)


def egri(kontrol, n=10):
    """Catmull-Rom: kontrol noktalarından yumuşak hortum çizgisi"""
    P = [cq.Vector(*p) for p in kontrol]
    out = []
    for i in range(len(P) - 1):
        p0 = P[i - 1] if i > 0 else P[i]; p1 = P[i]; p2 = P[i + 1]; p3 = P[i + 2] if i + 2 < len(P) else P[i + 1]
        for k in range(n):
            t = k / float(n); t2 = t * t; t3 = t2 * t
            v = (p1 * 2 + (p2 - p0) * t + (p0 * 2 - p1 * 5 + p2 * 4 - p3) * t2 + (p1 * 3 - p0 - p2 * 3 + p3) * t3) * 0.5
            out.append((v.x, v.y, v.z))
    out.append((P[-1].x, P[-1].y, P[-1].z))
    return out


def yay(merkez, r, a0, a1, duzlem="XZ", n=10):
    """merkez etrafında yay noktaları (derece); düzlem XZ: (x,z)"""
    cx, cy, cz = merkez
    pts = []
    for i in range(n + 1):
        a = math.radians(a0 + (a1 - a0) * i / float(n))
        if duzlem == "XZ":
            pts.append((cx + r * math.cos(a), cy, cz + r * math.sin(a)))
        else:
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a), cz))
    return pts


def dogru_fillet(wp, r, secici="|Z"):
    try:
        return wp.edges(secici).fillet(r)
    except Exception:
        return wp


def lob_rotor(cx, cy, z0, z1, faz):
    """2 loblu rotor: r(θ) = 17,5 + 7,5·cos 2(θ − faz) → uç 25, kök 10; iki rotor arası 36"""
    pts = []
    for i in range(96):
        a = 2 * math.pi * i / 96.0
        r = 17.5 + 7.5 * math.cos(2 * (a - faz))
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return cq.Workplane("XY").polyline(pts).close().extrude(z1 - z0).translate((0, 0, z0))


class Model(object):
    def __init__(self, ad):
        self.ad = ad
        self.P = []
        self.grup = {"SABIT": (0.0, 0.0, 0.0)}
        self.silinen = []

    def ekle(self, ad, sh, mal, kaynak, grup="SABIT", not_=""):
        assert mal in MALZEME, mal
        assert all(p["ad"] != ad for p in self.P), "ayni ad: " + ad
        assert all(k in KAYNAK_AD for k in kaynak.split("+")), kaynak
        self.P.append(dict(ad=ad, sh=kati(sh), mal=mal, kaynak=kaynak, grup=grup, not_=not_))

    def kutu_olc(self, adlar=None, gruplar=None):
        ss = [p["sh"] for p in self.P if (adlar is None or p["ad"] in adlar or any(p["ad"].startswith(a) for a in adlar))
              and (gruplar is None or p["grup"] in gruplar)]
        return cq.Compound.makeCompound(ss).BoundingBox()


# ================================================================ 1 · MINI-FILL ELEKTRO-PNÖMATİK
MF = Model("minifill_ep")
MF_L, MF_B, MF_H = 477.0, 296.0, 228.0            # [B] güç ünitesi (power base) 477 × 296 × 228
MF_AYAK = 17.0                                     # [Ö] ayak altı → siyah tabanın altı
MF_PLINT = (17.0, 45.0)                            # [Ö] siyah taban bandı
MF_SOL = (0.0, 262.0)                              # [Ö] sol (pompa) gövdesi
MF_SOL_UST = 217.0                                 # [Ö] sol gövde üstü (topuz 228'e çıkar)
MF_SAG_UST = 203.0                                 # [Ö] sağ (ekran) gövde üstü
MF_DERIN = 295.0                                   # [B] 296 = gövde 295 + ön logo kabartması 1
CEP_X = (59.0, 214.0)                              # [Ö] pompa cebi (önden ve üstten açık)
CEP_DUDAK = 142.0                                  # [Ö] cebin ön dudağı (önden görünüşteki U'nun dibi)
CEP_TABAN = 135.0                                  # [F] cep tabanı: blok üstü gövde üstünün 5 mm altında (foto)
CEP_ARKA = 174.0                                   # [Ö] cep arka duvarı (plan)
KULE = (59.0, 113.0, 159.0, 212.0)                 # [Ö] cebin sol arkasındaki kule (plan)
TOPUZ = (76.0, 194.0, 12.0)                        # [Ö] kule topuzu Ø24, üstü 228
BLOK_W, BLOK_H = 149.0, 77.0                       # [B] 149 · [Ö] 77 (hazne çiziminde blok)
BLOK_X = ((CEP_X[0] + CEP_X[1]) / 2.0 - BLOK_W / 2.0, (CEP_X[0] + CEP_X[1]) / 2.0 + BLOK_W / 2.0)   # 62 … 211
BLOK_Y = (9.0, 157.0)                              # [F] ön duvarın arkası 9 → kuleye 2 mm kala (derinlik 148 ≈ 149 kare)
BLOK_Z = (CEP_TABAN, CEP_TABAN + BLOK_H)           # 135 … 212
HZ_X = (CEP_X[0] + CEP_X[1]) / 2.0                 # 136,5 hazne ekseni x (cep ortası)
HZ_Y = BLOK_Y[0] + 110.0                           # [Ö] 3 L planında blok önü eksenden 110 önde → y 119
AGIZ_Z = BLOK_Z[0] + 62.8                          # [Ö] çıkış ağzı ekseni blok altından 62,8 → 197,8
ROTOR_Y = 85.5                                     # [Ö] kavrama plandan: önden 85,5
ROTOR_X = (HZ_X - 18.0, HZ_X + 18.0)               # [V] 2 loblu rotor, eksenler arası 36 (sağdaki tahrikli: kavrama x 155 [Ö])
ROTOR_Z = (BLOK_Z[0] + 22.0, BLOK_Z[0] + 52.0)     # [V] rotor boyu 30
SPOUT = (70.0, -45.0)                              # [F] pnömatik dik ağız ekseni (ekran görüntüsü: gövdenin sol önü)
SPOUT_UC = 20.0                                    # [F] ağız ucu masadan 20
SPOUT_GIRIS = 90.0                                 # [F] yan giriş ağzın ekseninde z 90

# ---- güç ünitesi (beyaz gövde, siyah taban, ayaklar) ----
sol = kutu(MF_SOL[0], MF_SOL[1], 0, MF_DERIN, MF_PLINT[1], MF_SOL_UST)
sol = dogru_fillet(sol, 22.0, "|Z")
cep = kutu(CEP_X[0], CEP_X[1], -1, KULE[2], CEP_DUDAK, MF_SOL_UST + 5)                     # önden açık üst kısım
cep = cep.union(kutu(CEP_X[0], CEP_X[1], 8.0, KULE[2], CEP_TABAN, MF_SOL_UST + 5))          # ön duvarın arkasında cep tabanı
cep = cep.union(kutu(KULE[1], CEP_X[1], 8.0, CEP_ARKA, CEP_TABAN, MF_SOL_UST + 5))          # kulenin sağında arka duvar 174
sol = sol.cut(cep)
MF.ekle("guc_unitesi_sol_govde", sol, "beyaz", "B+Ö", not_="pompa cebi önden ve üstten açık; cep tabanı 135 [F]")
sag = (cq.Workplane("YZ").polyline([(5.0, MF_PLINT[1]), (5.0, 117.0), (10.0, 121.0), (55.0, 121.0), (189.0, 197.0),
                                    (200.0, MF_SAG_UST), (283.0, MF_SAG_UST), (MF_DERIN - 5.0, 196.0), (MF_DERIN - 5.0, MF_PLINT[1])])
       .close().extrude(MF_L - MF_SOL[1]).translate((MF_SOL[1], 0, 0)))
sag = dogru_fillet(sag, 18.0, "|Z and >X")
MF.ekle("guc_unitesi_sag_govde", sag, "beyaz", "Ö", not_="ekran gövdesi; eğik panel 55→189 mm derinlikte, 121→197 mm yükseklikte")
plint = dogru_fillet(kutu(4.0, MF_L - 4.0, 4.0, MF_DERIN - 4.0, MF_PLINT[0], MF_PLINT[1]), 18.0, "|Z")
MF.ekle("siyah_taban", plint, "siyah", "Ö")
for i, (x, y) in enumerate([(40.0, 35.0), (40.0, 256.0), (437.0, 35.0), (437.0, 256.0)]):
    MF.ekle("ayak_%d" % (i + 1), silz(x, y, 15.0, 0.0, MF_PLINT[0]), "siyah", "Ö+V", not_="yükseklik ölçekten, yer VARSAYIM")
MF.ekle("logo_paneli", kutu(62.0, 208.0, -1.0, 0.5, 68.0, 125.0), "beyaz", "Ö", not_="ön yüzde kabartma 'mini-fill' paneli")
MF.ekle("kule_topuzu", silz(TOPUZ[0], TOPUZ[1], TOPUZ[2], MF_SOL_UST, MF_H), "siyah", "Ö+V", not_="üstü 228 [B]; işlevi (kilit / hava çıkışı) VARSAYIM")
# eğik dokunmatik panel: 185 × 154 paslanmaz plaka, üstünde 107 × 57 ekran + 3×3 tuş
eg = math.atan2(197.0 - 121.0, 189.0 - 55.0)            # 29,6°
L_EG = math.hypot(197.0 - 121.0, 189.0 - 55.0)          # 154,5


def egik(x0, x1, s0, s1, t0, t1):
    """eğik panel yüzeyinde (s: yüzey boyunca 55/121'den, t: yüzeye dik) kutu"""
    b = kutu(x0, x1, s0, s1, t0, t1)
    b = b.rotate((0, 0, 0), (1, 0, 0), math.degrees(eg))
    return b.translate((0, 55.0, 121.0))


MF.ekle("dokunmatik_panel_plakasi", egik(275.0, 459.0, 2.0, L_EG - 2.0, 0.0, 1.6), "fircali", "Ö", not_="eğim %.1f°" % math.degrees(eg))
MF.ekle("dokunmatik_ekran", egik(313.5, 420.5, (L_EG - 57.0) / 2.0, (L_EG + 57.0) / 2.0, 1.6, 2.4), "ekran", "Ö")
for i in range(3):
    for j in range(3):
        x0 = 318.0 + i * 33.5; s0 = (L_EG - 57.0) / 2.0 + 4.0 + j * 17.0
        MF.ekle("ekran_tusu_%d%d" % (i, j), egik(x0, x0 + 30.0, s0, s0 + 14.5, 2.4, 2.8), "ekran_tus", "F")
MF.ekle("kavrama_diski", silz(ROTOR_X[1], ROTOR_Y, 15.0, CEP_TABAN, CEP_TABAN + 6.0), "paslanmaz", "Ö+V",
        not_="pompa tahrik kavraması: yer plandan [Ö], çap VARSAYIM")
MF.ekle("hava_girisi_rakor", sily(100.0, 80.0, 6.0, MF_DERIN, MF_DERIN + 20.0), "mavi", "V",
        not_="basınçlı hava girişi 6 bar (kompresör 1,5 kW · 24 L · 196 L/dk ayrı [B]); yeri VARSAYIM")

# ---- dolum ünitesi: şeffaf pompa bloğu + 2 loblu rotorlar ----
blok = kutu(BLOK_X[0], BLOK_X[1], BLOK_Y[0], BLOK_Y[1], BLOK_Z[0], BLOK_Z[1])
blok = dogru_fillet(blok, 6.0, "|Z")
blok = blok.cut(kutu(BLOK_X[0] + 18.0, BLOK_X[1] - 18.0, BLOK_Y[0] + 14.0, BLOK_Y[1] - 14.0, BLOK_Z[0] - 1, BLOK_Z[0] + 15.0))   # alt pencere (bacaklar)
MF.ekle("pompa_blogu_seffaf", blok, "pc", "B+Ö+F", not_="149 genişlik [B], 77 yükseklik [Ö], 148 derinlik [F]")
for k, (x, faz, grup) in enumerate([(ROTOR_X[0], 0.0, "ROTOR_1"), (ROTOR_X[1], math.pi / 2.0, "ROTOR_2")]):
    MF.grup[grup] = (x, ROTOR_Y, 0.0)
    MF.ekle("rotor_%d_2lob" % (k + 1), lob_rotor(x, ROTOR_Y, ROTOR_Z[0], ROTOR_Z[1], faz), "pom", "B+V", grup=grup,
            not_="broşür: 2 loblu dişli takımı, parçacık ≤ 15 mm [B]; profil VARSAYIM")
    MF.ekle("rotor_%d_mili" % (k + 1), silz(x, ROTOR_Y, 5.0, BLOK_Z[0] + 2.0, ROTOR_Z[1] + 6.0), "paslanmaz", "V", grup=grup)
for k, dx in enumerate((-32.0, 32.0)):
    MF.ekle("kelebek_vida_%d" % (k + 1), silz(HZ_X + dx, BLOK_Y[0] + 30.0, 7.0, BLOK_Z[1], BLOK_Z[1] + 9.0), "paslanmaz", "F")
# çıkış ağzı (öne bakar) + 1,5" TC kelepçe
MF.ekle("cikis_agzi_bilezigi", sily(HZ_X, AGIZ_Z, 19.5, -9.0, BLOK_Y[0]), "pc", "Ö", not_="Ø39, bloktan 18 mm çıkar")
MF.ekle("cikis_tc_flansi", sily(HZ_X, AGIZ_Z, 25.25, -14.6, -9.0), "paslanmaz", "F", not_="1,5\" TC ferrule Ø50,5")
MF.ekle("cikis_tc_kelepcesi", sily(HZ_X, AGIZ_Z, 32.0, -20.0, -4.0).cut(sily(HZ_X, AGIZ_Z, 25.6, -21.0, -3.0)), "paslanmaz", "F")
MF.ekle("cikis_tc_kanadi", kutu(HZ_X - 4.0, HZ_X + 4.0, -16.0, -8.0, AGIZ_Z + 31.0, AGIZ_Z + 46.0), "paslanmaz", "F")
# ---- 15 L hazne (yarı saydam PP), kapak, kubbe ----
HZ0 = BLOK_Z[0]                                    # hazne çizimindeki 0 = blok altı
dis = [(34.0, 77.0), (34.0, 98.3), (113.0, 143.7), (121.0, 152.0), (126.0, 163.0), (128.0, 177.8), (128.0, 478.0)]
MF.ekle("hazne_15L", dondur(kabuk_profili([(r, HZ0 + z) for r, z in dis], 2.5), HZ_X, HZ_Y), "pp", "B+Ö",
        not_="Ø256 [B], blok altından 495 [B]; koni/omuz profili [Ö]")
MF.ekle("hazne_bayonet_bilezigi", dondur(kabuk_profili([(38.5, HZ0 + 77.0), (38.5, HZ0 + 89.0)], 4.5), HZ_X, HZ_Y), "pp", "Ö")
MF.ekle("hazne_kapagi", dondur([(0.0, HZ0 + 478.0), (129.5, HZ0 + 478.0), (129.5, HZ0 + 488.0), (0.0, HZ0 + 488.0)], HZ_X, HZ_Y), "pp", "Ö")
kub = [(45.0 * math.cos(math.radians(a)), HZ0 + 488.0 + 7.5 * math.sin(math.radians(a))) for a in range(0, 90, 10)]
MF.ekle("kapak_kubbesi", dondur([(0.0, HZ0 + 488.0)] + kub + [(0.0, HZ0 + 495.5)], HZ_X, HZ_Y), "pp", "Ö", not_="üstü blok altından 495 [B]")
# ---- pnömatik dik ağız (E-P'ye özel, damlatmaz) ----
sx, sy = SPOUT
parca = [("agiz_ucu", dondur([(0.0, SPOUT_UC), (10.0, SPOUT_UC), (15.0, SPOUT_UC + 10.0), (0.0, SPOUT_UC + 10.0)], sx, sy), "pom"),
         ("agiz_halkasi", silz(sx, sy, 26.5, SPOUT_UC + 10.0, SPOUT_UC + 38.0), "pom"),
         ("agiz_alt_borusu", silz(sx, sy, 16.0, SPOUT_UC + 38.0, 150.0), "paslanmaz"),
         ("agiz_manson", silz(sx, sy, 23.5, 150.0, 226.0), "pom"),
         ("agiz_manson_bilezigi", silz(sx, sy, 24.0, 203.0, 207.0), "paslanmaz"),
         ("agiz_pnomatik_silindiri", silz(sx, sy, 16.5, 226.0, 333.0), "paslanmaz"),
         ("agiz_silindir_kapagi", silz(sx, sy, 17.5, 333.0, 345.0), "paslanmaz"),
         ("agiz_hava_rakoru", silz(sx, sy, 5.0, 345.0, 355.0), "siyah")]
for ad, sh, mal in parca:
    MF.ekle(ad, sh, mal, "F", not_="ekran görüntüsü + broşür s.3 fotoğrafı; toplam ≈ 335 mm, boru Ø32 alındı")
# çıkış ağzından dik ağza eğik bağlantı borusu (yan giriş ≈ 57° — broşürdeki fotoğraftaki eğik ağızla aynı)
P1 = (HZ_X, -30.0, AGIZ_Z)
P2 = (sx, sy, SPOUT_GIRIS)
MF.ekle("baglanti_borusu", boru([(HZ_X, -20.0, AGIZ_Z), P1, P2], 10.0), "paslanmaz", "F",
        not_="Ø20 [V]; eğim %.0f° [F]" % math.degrees(math.atan2(AGIZ_Z - SPOUT_GIRIS, math.hypot(P1[0] - P2[0], P1[1] - P2[1]))))
# hava hortumları (kırmızı + siyah Ø4): ağzın tepesi → sol kenar → kule topuzu
for k, (mal, d) in enumerate([("kirmizi", 0.0), ("siyah", 6.0)]):
    kon = [(sx, sy, 355.0), (sx - 18.0 + d, sy - 7.0, 362.0), (36.0 + d, sy - 3.0, 335.0), (26.0 + d, -30.0, 285.0),
           (26.0 + d, 0.0, 242.0), (28.0 + d, 40.0, 223.0), (30.0 + d, 120.0, 222.0), (52.0 + d, TOPUZ[1] - 14.0, 223.0),
           (TOPUZ[0] - 10.0, TOPUZ[1] + d - 3.0, MF_H - 4.0)]
    MF.ekle("hava_hortumu_%s" % mal, hortum(kon, 2.0), mal, "F+V", not_="ağız pnömatiğinin 2 hattı; güzergâh VARSAYIM")

# ================================================================ 2 · BELTOP UNO 275 · ÇEKİRDEK (sehpasız)
UN = Model("beltop_uno275")
UNO_L, UNO_AGIZ_EKSEN, UNO_H, UNO_TABAN, UNO_B, UNO_HZ = 685.0, 197.0, 690.0, 483.0, 313.0, 384.0     # [B] s.6
Z_EKSEN = 38.5                                    # [Ö] ağız / valf / silindir ekseni, kaide üstünden
H_KAIDE = UNO_AGIZ_EKSEN - Z_EKSEN                # [H] 158,5 — silinen sac kaidenin yüksekliği
X_SOL = -159.6                                    # [Ö] 685'in sol ucu: ağız kelepçesi
X_SAG = X_SOL + UNO_L                             # 525,4 — hacim ayar milinin ucu
VB = 41.0                                         # [Ö] valf bloğu yarı genişliği (82) · derinlik [V] küp
VB_H = 72.6                                       # [Ö]
KASA_X = (48.4, 459.5)                            # [Ö] saclı kasa
KASA_Y = (-49.0, 120.0)                           # [Ö] plan: eksenden 49 önde, 120 arkada
KASA_Z = 118.6                                    # [Ö]
OLUK_X1 = 207.0                                   # [Ö] oluk (açık) → etiketli kutu
URUN_D, URUN_OD = 52.0, 58.0                      # [B] silindir seçeneği Ø52 (151 ml) · dış çap [V]
STROK_MAX = 151000.0 / (math.pi / 4.0 * URUN_D ** 2)          # [H] 71,1 mm
XP_ON, XP_ARKA = VB + 8.0, VB + 8.0 + STROK_MAX   # piston yüzü: basmada 49, emişte 120,1
PNO_D = 32.0                                      # [H] hava tüketiminden (aşağıda)
PNO_X = (275.0, 424.0)                            # [V] Ø32 × 80 strok yuvarlak silindir gövdesi (ön boğaz 275)
L_URUN_MILI = PNO_X[0] - 22.0 - XP_ARKA           # kavrama ekseni: basmada 181,9 · emişte 253
HAVA_L_DK = 29.0                                  # [B] 29 L/dk @ 30 doz/dk, 7 bar
HAVA_CEVRIM = HAVA_L_DK / 30.0                    # 0,967 L serbest hava / çevrim
PNO_STROK_HESAP = HAVA_CEVRIM * 1e6 / (2.0 * math.pi / 4.0 * PNO_D ** 2 * (7.0 + 1.013) / 1.013)   # [H] ≈ 76 mm

# ---- 25 L konik hazne (paslanmaz, kapaksız) ----
hz_dis = [(31.75, 72.6), (31.75, 131.7), (179.2, 377.0), (179.2, 525.6)]
UN.ekle("hazne_25L_konik", dondur(kabuk_profili(hz_dis, 1.5), 0.0, 0.0), "paslanmaz", "B+Ö",
        not_="ağız Ø384 [B]; silindir Ø358 × 149, koni Ø358→Ø64 × 245 [Ö]; hacim hesabı aşağıda")
UN.ekle("hazne_agiz_kivrimi", dondur([(179.2, 525.6), (192.0, 525.6), (192.0, 530.0), (179.2, 530.0)], 0.0, 0.0), "paslanmaz", "B+Ö",
        not_="Ø384 × 4,4; üstü kaideden 530 → yerden 688,5 ≈ 690 [B]")
UN.ekle("hazne_kaynak_bandi", dondur(kabuk_profili([(180.2, 377.0), (180.2, 388.0)], 1.0), 0.0, 0.0), "paslanmaz", "Ö")
UN.ekle("hazne_tc_kelepcesi_2.5in", dondur(kabuk_profili([(45.5, 90.2), (45.5, 107.7)], 13.0), 0.0, 0.0), "paslanmaz", "Ö+F",
        not_="2,5\" TC; Ø91 [Ö]")
UN.ekle("hazne_kelepce_kelebegi", silx(-40.0, 99.0, 4.0, 30.0, 62.0).union(kutu(56.0, 62.0, -52.0, -28.0, 93.0, 105.0)), "paslanmaz", "F")
UN.ekle("hazne_contasi", dondur(kabuk_profili([(40.0, 88.6), (40.0, 90.2)], 8.2), 0.0, 0.0), "kirmizi", "F", not_="fotoğrafta kırmızı conta")
# ---- valf bloğu + döner valf ----
vb = dogru_fillet(kutu(-VB, VB, -VB, VB, 0.4, VB_H), 4.0, "|Z")
vb = vb.cut(sily(0.0, Z_EKSEN, 24.0, -VB - 1.0, VB + 1.0))
UN.ekle("valf_blogu", vb, "paslanmaz", "Ö+V", not_="82 × 72,6 [Ö]; derinlik 82 VARSAYIM (fotoğrafta küp)")
UN.grup["VALF"] = (0.0, 0.0, Z_EKSEN)
rot = sily(0.0, Z_EKSEN, 23.5, -VB - 2.0, VB + 2.0)
tb = silz(0.0, 0.0, 12.0, Z_EKSEN - 23.0, Z_EKSEN + 23.0).union(silx(0.0, Z_EKSEN, 12.0, 0.0, 23.0))   # T delik (emiş: üst+sağ)
UN.ekle("doner_valf_rotoru", rot.cut(tb), "pom", "B+V", grup="VALF",
        not_="broşür: 'rotation cylinder' [B]; T delik: emişte üst↔sağ, 90° dönünce sağ↔sol [V]")
UN.ekle("valf_topuzu", sily(0.0, Z_EKSEN, 21.0, -VB - 26.0, -VB - 2.0), "siyah", "F", grup="VALF")
UN.ekle("valf_topuzu_isareti", kutu(-3.0, 3.0, -VB - 27.0, -VB - 25.0, Z_EKSEN + 6.0, Z_EKSEN + 19.0), "beyaz", "V", grup="VALF")
UN.ekle("valf_dondurme_aktuatoru", kutu(-28.0, 28.0, VB, VB + 50.0, 16.0, 60.0), "aluminyum", "V",
        not_="valfi 90° çeviren pnömatik döner eyleyici; arkada, görünmüyor → VARSAYIM")
# ---- ağız tarafı: 1,5" çıkış borusu + TC + 90° ağız ----
UN.ekle("cikis_borusu", silx(0.0, Z_EKSEN, 18.0, -136.3, -VB), "paslanmaz", "Ö", not_="Ø36 [Ö]")
UN.ekle("cikis_tc_ferrule", silx(0.0, Z_EKSEN, 25.25, -151.8, -146.2), "paslanmaz", "F")
UN.ekle("cikis_tc_kelepcesi", silx(0.0, Z_EKSEN, 29.5, X_SOL, -138.4).cut(silx(0.0, Z_EKSEN, 25.6, X_SOL - 1, -137.4)), "paslanmaz", "Ö",
        not_="Ø59 × 21 [Ö]; sol ucu 685 ölçüsünün başı")
UN.ekle("cikis_tc_kelebegi", kutu(-153.0, -145.0, -4.0, 4.0, Z_EKSEN + 29.0, Z_EKSEN + 45.0), "paslanmaz", "Ö")
V_ = cq.Vector
_c = (-172.0, Z_EKSEN - 45.0)                     # dirsek merkezi (x, z), eksen yarıçapı 45
_w = cq.Wire.assembleEdges([cq.Edge.makeLine(V_(-151.8, 0, Z_EKSEN), V_(-172.0, 0, Z_EKSEN)),
                            cq.Edge.makeThreePointArc(V_(-172.0, 0, Z_EKSEN), V_(_c[0] - 45.0 * math.sqrt(0.5), 0, _c[1] + 45.0 * math.sqrt(0.5)), V_(-217.0, 0, _c[1])),
                            cq.Edge.makeLine(V_(-217.0, 0, _c[1]), V_(-217.0, 0, -56.5))])
_d = cq.Solid.sweep(cq.Wire.makeCircle(18.0, V_(-151.8, 0, Z_EKSEN), V_(-1, 0, 0)), [cq.Wire.makeCircle(16.5, V_(-151.8, 0, Z_EKSEN), V_(-1, 0, 0))], _w, True, False)
UN.ekle("agiz_90_derece", _d, "paslanmaz", "B+F", not_="broşür seçeneği 'nozzle 90°' [B]; Ø36, dirsek R45 fotoğraftan [F]")
UN.ekle("agiz_ucu", silz(-217.0, 0.0, 22.0, -74.5, -56.5), "pom", "F")
# ---- ürün silindiri (Ø52 seçildi) + piston ----
UN.ekle("urun_silindiri_bilezigi", silx(0.0, Z_EKSEN, 33.0, VB, VB + 8.0), "paslanmaz", "F")
us = silx(0.0, Z_EKSEN, URUN_OD / 2.0, VB + 8.0, 165.0).cut(silx(0.0, Z_EKSEN, URUN_D / 2.0, VB + 7.0, 166.0))
UN.ekle("urun_silindiri_D52", us, "saydam_celik", "B+Ö",
        not_="Ø52 (30–151 ml) [B]; boy [Ö]; içi görünsün diye SAYDAM çizildi (gerçekte paslanmaz)")
UN.ekle("urun_silindiri_kapagi", silx(0.0, Z_EKSEN, 33.0, 165.0, 172.0).cut(silx(0.0, Z_EKSEN, 7.0, 164.0, 173.0)), "paslanmaz", "Ö")
kor = None
for i, (r, a, b) in enumerate([(30.0, 172.0, 181.0), (33.5, 181.0, 190.0), (37.0, 190.0, 198.0), (39.5, 198.0, 207.0)]):
    s = silx(0.0, Z_EKSEN, r, a, b)
    kor = s if kor is None else kor.union(s)
UN.ekle("mil_korugu", kor.cut(silx(0.0, Z_EKSEN, 12.0, 171.0, 208.0)), "siyah", "Ö", not_="çizimdeki basamaklı koni; siyah körük, mil kavraması içinden geçer [F]")
UN.grup["PISTON"] = (XP_ON, 0.0, Z_EKSEN)          # basma sonu (piston yüzü 49) = düğümün sıfırı
UN.ekle("urun_pistonu", silx(0.0, Z_EKSEN, URUN_D / 2.0 - 0.3, XP_ON, XP_ON + 20.0), "pom", "H", grup="PISTON",
        not_="strok %.1f mm = 151 ml / (π/4·52²) [H]" % STROK_MAX)
UN.ekle("urun_mili", silx(0.0, Z_EKSEN, 6.0, XP_ON + 20.0, XP_ON + L_URUN_MILI), "paslanmaz", "V", grup="PISTON")
UN.ekle("mil_kavramasi", silx(0.0, Z_EKSEN, 10.0, XP_ON + L_URUN_MILI - 8.0, XP_ON + L_URUN_MILI + 8.0), "paslanmaz", "V", grup="PISTON")
UN.ekle("pnomatik_mil_D12", silx(0.0, Z_EKSEN, 6.0, XP_ON + L_URUN_MILI + 8.0, XP_ON + L_URUN_MILI + 22.0 + STROK_MAX + 20.0), "paslanmaz", "V", grup="PISTON")
# ---- saclı kasa: sol oluk (önü ve üstü açık) + etiketli kutu ----
t = 1.5
oluk = kutu(KASA_X[0], OLUK_X1, KASA_Y[0], KASA_Y[1], 0.4, 0.4 + t)                       # taban
oluk = oluk.union(kutu(KASA_X[0], OLUK_X1, KASA_Y[1] - t, KASA_Y[1], 0.4, KASA_Z))         # arka duvar
oluk = oluk.union(kutu(KASA_X[0], OLUK_X1, KASA_Y[0], KASA_Y[0] + t, 0.4, 6.0))            # ön dudak
oluk = oluk.union(kutu(KASA_X[0], KASA_X[0] + t, 0.0, KASA_Y[1], 0.4, KASA_Z).cut(silx(0.0, Z_EKSEN, 34.0, KASA_X[0] - 1, KASA_X[0] + t + 1)))
oluk = oluk.union(kutu(KASA_X[0], OLUK_X1, KASA_Y[1] - 30.0, KASA_Y[1], KASA_Z - t, KASA_Z))    # arka üst flanş
UN.ekle("kasa_oluk_saci", oluk, "fircali", "Ö+F", not_="ürün silindiri açık olukta yatar (fotoğraf)")
kasa = kutu(OLUK_X1, KASA_X[1], KASA_Y[0], KASA_Y[1], 0.4, KASA_Z)
kasa = kasa.cut(kutu(OLUK_X1 + t, KASA_X[1] - t, KASA_Y[0] + t, KASA_Y[1] - t, 0.4 + t, KASA_Z - t))
kasa = kasa.cut(silx(0.0, Z_EKSEN, 12.0, OLUK_X1 - 1, OLUK_X1 + t + 1))
UN.ekle("kasa_kutu_saci", kasa, "kabuk", "Ö", not_="içi görünsün diye SAYDAM çizildi (gerçekte paslanmaz sac)")
UN.ekle("etiket_paneli", kutu(206.7, 448.5, KASA_Y[0] - 1.5, KASA_Y[0], 0.4, 79.2), "siyah", "Ö", not_="'BELDOS 275' paneli")
UN.ekle("etiket_kirmizi_cizgi", kutu(206.7, 448.5, KASA_Y[0] - 1.8, KASA_Y[0] - 1.5, 74.0, 76.0), "kirmizi", "F")
UN.ekle("hizli_sokme_pimi", silz(222.0, 20.0, 7.0, KASA_Z, KASA_Z + 10.0), "siyah", "F")
UN.ekle("hiz_ayar_topuzu", sily(430.0, 98.0, 11.0, KASA_Y[0] - 12.0, KASA_Y[0]), "siyah", "F+V", not_="'adjust the speed' [B]; yeri VARSAYIM")
# ---- pnömatik silindir Ø32 (hesap) + hacim ayarı ----
UN.ekle("pnomatik_silindir_D32", silx(0.0, Z_EKSEN, 19.0, PNO_X[0] + 10.0, PNO_X[1]), "aluminyum", "H+V",
        not_="Ø32: 29 L/dk ÷ 30 = 0,97 L/çevrim → çift etkili Ø32 × %.0f mm [H]; gövde boyu VARSAYIM" % PNO_STROK_HESAP)
UN.ekle("pnomatik_on_bogaz", silx(0.0, Z_EKSEN, 12.0, PNO_X[0], PNO_X[0] + 10.0), "aluminyum", "V")
UN.ekle("pnomatik_arka_mafsal", kutu(PNO_X[1], PNO_X[1] + 16.0, -12.0, 12.0, Z_EKSEN - 12.0, Z_EKSEN + 12.0), "aluminyum", "V")
UN.ekle("pnomatik_arka_ayak", kutu(PNO_X[1] + 16.0, PNO_X[1] + 22.0, -25.0, 25.0, 1.9, Z_EKSEN + 14.0).cut(silx(0.0, 15.0, 6.0, PNO_X[1] + 15.0, PNO_X[1] + 23.0)), "fircali", "V")
UN.ekle("pnomatik_on_ayak", kutu(PNO_X[0] + 12.0, PNO_X[0] + 18.0, -25.0, 25.0, 1.9, Z_EKSEN - 18.0), "fircali", "V")
UN.ekle("hacim_ayar_topuzu", silx(0.0, 15.0, 31.5, 479.3, 503.5), "siyah", "Ö", not_="Ø63 × 24 tırtıllı [Ö]; 'adjust the volume' [B]")
UN.ekle("hacim_ayar_mili", silx(0.0, 15.0, 5.0, 440.0, X_SAG), "paslanmaz", "Ö+V", not_="ucu 685 ölçüsünün sonu; iç mekanizma VARSAYIM")
UN.ekle("hacim_ayar_dayamasi", kutu(432.0, 440.0, -14.0, 14.0, 6.0, 24.0), "paslanmaz", "V")
# ---- hava şartlandırıcı (arka sağ) + kırmızı hortum ----
RX0, RX1, RY0, RY1 = 459.5, 499.0, 77.0, 117.0     # [Ö] plan + görünüş
rc = ((RX0 + RX1) / 2.0, (RY0 + RY1) / 2.0)
UN.ekle("sartlandirici_govde", kutu(RX0, RX1, RY0, RY1, 68.0, 116.0), "siyah", "Ö")
UN.ekle("sartlandirici_ayar_topuzu", silz(rc[0], rc[1], 14.0, 116.0, 160.0), "siyah", "Ö", not_="üstü kaideden 160 [Ö]")
UN.ekle("sartlandirici_filtre_kabi", silz(rc[0], rc[1], 15.0, 3.0, 68.0), "saydam_celik", "Ö+V")
UN.ekle("sartlandirici_manometre", sily(rc[0], 94.0, 14.0, RY0 - 10.0, RY0), "beyaz", "Ö")
UN.ekle("hava_giris_rakoru", silx(rc[1], 94.0, 5.0, RX1, RX1 + 26.0), "siyah", "Ö")
kon = [(26.0, -20.0, VB_H + 2.0), (52.0, -42.0, 95.0), (120.0, -58.0, 72.0), (200.0, -60.0, 26.0), (262.0, -56.0, 8.0), (305.0, -51.5, 7.0)]
UN.ekle("hava_hortumu_kirmizi", hortum(kon, 3.0), "kirmizi", "F", not_="fotoğraftaki kırmızı hortum; bağlantı noktaları VARSAYIM")
# ---- bizim bağlantı plakası (silinen sac kaidenin yerine) ----
UN.ekle("baglanti_plakasi_BIZIM", kutu(-45.0, 462.0, -55.0, 125.0, -8.0, 0.0), "bizim", "BİZİM",
        not_="Beldos'ta yok: sac kaidenin üst tablası yerine 8 mm düz plaka; ölçü VARSAYIM")
UN.silinen = [
    ("4 ayak (lastik uçlu)", "Ö", "kaide köşelerinde; yerden 0 → ~30"),
    ("alt taban sacı 483 × 313", "B", "broşür ölçüsü; köşeleri yuvarlak"),
    ("büküm sac gövde (eğik sağ yan, elmas delikli)", "Ö", "yerden 30 → 158,5; sağ yanı eğik"),
    ("üst tabla + 'BELTOP UNO' etiketi", "F", "valf bloğu ve kasa buna oturuyordu → yerine BİZİM bağlantı plakası"),
    ("yan kanat rayları (plandaki 2 kulak, cıvatalı)", "Ö", "313 genişliğin uçları"),
    ("valf bloğu kilit kolu (siyah)", "F", "bloğu sac tablaya kilitliyordu"),
]


# ================================================================ 3 · ANİMASYON (iki makinede de 2 sn = 30 doz/dk)
DONGU = 2.0


def ss(a, b, t):
    if t <= a: return 0.0
    if t >= b: return 1.0
    u = (t - a) / (b - a)
    return u * u * (3 - 2 * u)


def mf_rotor_aci(t):
    return 2.0 * math.pi * ss(0.2, 1.4, t)          # dozda 1 tur [V], sonra bekler


def uno_piston_dx(t):
    # 0–0,8 emiş (piston geri, +x) · 0,8–1,0 valf 90° · 1,0–1,8 basma · 1,8–2,0 valf geri
    if t <= 0.8: return STROK_MAX * ss(0.0, 0.8, t)
    if t <= 1.0: return STROK_MAX
    return STROK_MAX * (1.0 - ss(1.0, 1.8, t))


def uno_valf_aci(t):
    if t <= 0.8: return 0.0
    if t <= 1.0: return math.pi / 2.0 * ss(0.8, 1.0, t)       # makine +Y ekseni etrafında +90°: T'nin sapı sağ → alt
    if t <= 1.8: return math.pi / 2.0
    return math.pi / 2.0 * (1.0 - ss(1.8, 2.0, t))


# ================================================================ 4 · GLB
def ag(sh, tol=0.2, aci=0.3):
    vs, ts = sh.tessellate(tol, aci)
    P = [(v.x, v.y, v.z) for v in vs]
    N = [[0.0, 0.0, 0.0] for _ in P]
    for a, b, c in ts:
        ux, uy, uz = P[b][0] - P[a][0], P[b][1] - P[a][1], P[b][2] - P[a][2]
        wx, wy, wz = P[c][0] - P[a][0], P[c][1] - P[a][1], P[c][2] - P[a][2]
        n = (uy * wz - uz * wy, uz * wx - ux * wz, ux * wy - uy * wx)
        for i in (a, b, c):
            N[i][0] += n[0]; N[i][1] += n[1]; N[i][2] += n[2]
    NN = []
    for n in N:
        L = math.sqrt(n[0] ** 2 + n[1] ** 2 + n[2] ** 2) or 1.0
        NN.append((n[0] / L, n[1] / L, n[2] / L))
    return P, NN, [i for tri in ts for i in tri]


def g(v, o=(0.0, 0.0, 0.0)):
    """makine (X, Y arkaya, Z yukarı) mm → glTF (x, y yukarı, z öne) m"""
    return ((v[0] - o[0]) * MM, (v[2] - o[2]) * MM, -(v[1] - o[1]) * MM)


def gn(n):
    return (n[0], n[2], -n[1])


def quat(eksen, a):
    s = math.sin(a / 2.0)
    return (eksen[0] * s, eksen[1] * s, eksen[2] * s, math.cos(a / 2.0))


def glb_yaz(M, yol, merkez, animler, anim_adi):
    blob, views, accs, meshes, mats, mat_idx = [], [], [], [], [], {}
    off = [0]

    def gomu(bt, hedef=None):
        while off[0] % 4:
            blob.append(b"\x00"); off[0] += 1
        v = {"buffer": 0, "byteOffset": off[0], "byteLength": len(bt)}
        if hedef:
            v["target"] = hedef
        views.append(v); blob.append(bt); off[0] += len(bt)
        return len(views) - 1

    def mat(k):
        if k not in mat_idx:
            d = MALZEME[k]
            m = {"name": k, "pbrMetallicRoughness": {"baseColorFactor": list(d["renk"]), "metallicFactor": d["met"], "roughnessFactor": d["ruf"]},
                 "doubleSided": True}
            if d.get("saydam"):
                m["alphaMode"] = "BLEND"
            mat_idx[k] = len(mats); mats.append(m)
        return mat_idx[k]

    nodes = [{"name": M.ad, "children": []}]
    gidx = {}
    for gad, piv in M.grup.items():
        gidx[gad] = len(nodes)
        nodes.append({"name": gad, "translation": list(g(piv, merkez)), "children": []})
        nodes[0]["children"].append(gidx[gad])
    ucgen = 0
    for p in M.P:
        piv = M.grup[p["grup"]]
        P, N, I = ag(p["sh"])
        pts = [g(q, piv) for q in P]
        nrm = [gn(n) for n in N]
        vp = gomu(struct.pack("<%df" % (3 * len(pts)), *[c for q in pts for c in q]), 34962)
        vn = gomu(struct.pack("<%df" % (3 * len(nrm)), *[c for q in nrm for c in q]), 34962)
        vi = gomu(struct.pack("<%dI" % len(I), *I), 34963)
        mn = [min(q[i] for q in pts) for i in range(3)]; mx = [max(q[i] for q in pts) for i in range(3)]
        accs.append({"bufferView": vp, "componentType": 5126, "count": len(pts), "type": "VEC3", "min": mn, "max": mx})
        accs.append({"bufferView": vn, "componentType": 5126, "count": len(nrm), "type": "VEC3"})
        accs.append({"bufferView": vi, "componentType": 5125, "count": len(I), "type": "SCALAR"})
        d = MALZEME[p["mal"]]                     # parça başına malzeme: sayfada dokununca parça adı (model3d.js materialFromPoint)
        mm_ = {"name": p["ad"], "pbrMetallicRoughness": {"baseColorFactor": list(d["renk"]), "metallicFactor": d["met"], "roughnessFactor": d["ruf"]},
               "doubleSided": True}
        if d.get("saydam"):
            mm_["alphaMode"] = "BLEND"
        mats.append(mm_)
        meshes.append({"name": p["ad"], "primitives": [{"attributes": {"POSITION": len(accs) - 3, "NORMAL": len(accs) - 2},
                                                          "indices": len(accs) - 1, "material": len(mats) - 1}]})
        nodes.append({"name": p["ad"], "mesh": len(meshes) - 1})
        nodes[gidx[p["grup"]]]["children"].append(len(nodes) - 1)
        ucgen += len(I) // 3
    for n in nodes:
        if "children" in n and not n["children"]:
            del n["children"]
    # animasyon
    N_ = int(round(DONGU * 30)) + 1
    TT = [DONGU * i / (N_ - 1) for i in range(N_)]
    sm, ch = [], []
    for gad, yol_, f in animler:
        ti = gomu(struct.pack("<%df" % len(TT), *TT))
        accs.append({"bufferView": ti, "componentType": 5126, "count": len(TT), "type": "SCALAR", "min": [0.0], "max": [DONGU]})
        if yol_ == "translation":
            base = nodes[gidx[gad]]["translation"]
            vals = []
            for t in TT:
                d = f(t); dg = (d[0] * MM, d[2] * MM, -d[1] * MM)
                vals.append((base[0] + dg[0], base[1] + dg[1], base[2] + dg[2]))
            tip, n = "VEC3", 3
        else:
            eksen, fa = f
            vals = [quat(eksen, fa(t)) for t in TT]
            tip, n = "VEC4", 4
        vo = gomu(struct.pack("<%df" % (n * len(vals)), *[c for v in vals for c in v]))
        accs.append({"bufferView": vo, "componentType": 5126, "count": len(vals), "type": tip})
        sm.append({"input": len(accs) - 2, "output": len(accs) - 1, "interpolation": "LINEAR"})
        ch.append({"sampler": len(sm) - 1, "target": {"node": gidx[gad], "path": yol_}})
    while off[0] % 4:
        blob.append(b"\x00"); off[0] += 1
    bb = b"".join(blob)
    gl = {"asset": {"version": "2.0", "generator": "AUTOKITCH beldos_cad_v1"}, "scene": 0, "scenes": [{"nodes": [0]}],
          "nodes": nodes, "meshes": meshes, "materials": mats, "accessors": accs, "bufferViews": views,
          "buffers": [{"byteLength": len(bb)}]}
    if ch:
        gl["animations"] = [{"name": anim_adi, "samplers": sm, "channels": ch}]
    js = json.dumps(gl, separators=(",", ":")).encode("utf-8")
    while len(js) % 4:
        js += b" "
    os.makedirs(os.path.dirname(yol), exist_ok=True)
    with open(yol, "wb") as f:
        f.write(struct.pack("<4sII", b"glTF", 2, 12 + 8 + len(js) + 8 + len(bb)))
        f.write(struct.pack("<I4s", len(js), b"JSON")); f.write(js)
        f.write(struct.pack("<I4s", len(bb), b"BIN\x00")); f.write(bb)
    print("GLB %s · %d KB · %d parca · %d ucgen · %d anim kanali" % (os.path.basename(yol), (len(bb) + len(js)) // 1024, len(M.P), ucgen, len(ch)))
    return (len(bb) + len(js)) // 1024


# ================================================================ 5 · DENETİM
def hacim_L(profil_ic, z0, z1):
    """iç profilden (r, z) z0–z1 arası dönel hacim (L)"""
    pts = [(0.0, z0)] + [(r, z) for r, z in profil_ic if z0 <= z <= z1] + [(0.0, z1)]
    return dondur(pts, 0.0, 0.0).val().Volume() / 1e6


def kontrol(ad, olcu, hedef, tol, kaynak):
    ok = abs(olcu - hedef) <= tol
    DEN.append(dict(ad=ad, olcu=round(olcu, 1), hedef=hedef, tol=tol, kaynak=kaynak, sonuc="GEÇTİ" if ok else "KALDI"))
    print("  %-58s %8.1f  hedef %7.1f ±%-4g %s" % (ad, olcu, hedef, tol, "GEÇTİ" if ok else "** KALDI **"))


def cakisma(M, a, b, sinir=1.0):
    try:
        A = [p["sh"] for p in M.P if p["ad"] == a][0]; B = [p["sh"] for p in M.P if p["ad"] == b][0]
        return A.intersect(B).Volume() > sinir
    except Exception:
        return False


if __name__ == "__main__":
    t0 = time.time()
    DEN = []
    print("MINI-FILL E-P denetim:")
    b = MF.kutu_olc(adlar=["guc_unitesi", "siyah_taban", "ayak_", "logo_paneli", "kule", "dokunmatik", "ekran"])
    kontrol("güç ünitesi boyu (x)", b.xlen, MF_L, 1.0, "B")
    kontrol("güç ünitesi derinliği (y, arka rakor hariç)", b.ylen, MF_B, 1.0, "B")
    kontrol("güç ünitesi yüksekliği (z, topuz dahil)", b.zmax, MF_H, 0.5, "B")
    b = MF.kutu_olc(adlar=["pompa_blogu_seffaf"])
    kontrol("pompa bloğu genişliği", b.xlen, BLOK_W, 0.5, "B")
    b = MF.kutu_olc(adlar=["hazne_15L", "kapak_kubbesi", "hazne_kapagi"])
    kontrol("hazne çapı (kapak hariç gövde)", MF.kutu_olc(adlar=["hazne_15L"]).xlen, 256.0, 0.5, "B")
    kontrol("hazne + blok yüksekliği (blok altından kubbe tepesine)", b.zmax - BLOK_Z[0], 495.0, 1.0, "B")
    V15 = hacim_L([(r - 2.5, HZ0 + z) for r, z in dis], HZ0 + 77.0, HZ0 + 478.0)
    kontrol("15 L hazne iç hacmi (bilezikten kapağa, L)", V15, 15.0, 2.5, "H")
    tum = MF.kutu_olc()
    MF_TOP = tum.zmax
    print("  toplam: %.0f × %.0f × %.0f mm (x × y × z) · y %.0f…%.0f" % (tum.xlen, tum.ylen, tum.zlen, tum.ymin, tum.ymax))
    assert not cakisma(MF, "pompa_blogu_seffaf", "guc_unitesi_sol_govde"), "blok gövdeye giriyor"
    assert CEP_TABAN + 62.8 - 19.5 > CEP_DUDAK, "çıkış ağzı ön dudağın altında kalıyor"

    print("BELTOP UNO 275 (sehpasız) denetim:")
    b = UN.kutu_olc(adlar=[p["ad"] for p in UN.P if p["ad"] not in ("agiz_90_derece", "agiz_ucu", "baglanti_plakasi_BIZIM") and not p["ad"].startswith("hazne_")])
    kontrol("boy: ağız kelepçesi → hacim ayar mili (685 · hazne ağzı hariç)", b.xlen, UNO_L, 2.0, "B")
    kontrol("hazne ağzının 685'in solundan taşması (çizimde 34)", -UN.kutu_olc(adlar=["hazne_agiz_kivrimi"]).xmin + X_SOL, 34.0, 3.0, "Ö")
    kontrol("hazne ağız çapı (384)", UN.kutu_olc(adlar=["hazne_agiz_kivrimi"]).xlen, UNO_HZ, 0.5, "B")
    kontrol("hazne üstü + silinen kaide 158,5 (690)", UN.kutu_olc(adlar=["hazne_agiz_kivrimi"]).zmax + H_KAIDE, UNO_H, 2.0, "B")
    kontrol("ağız ekseni + silinen kaide (197)", Z_EKSEN + H_KAIDE, UNO_AGIZ_EKSEN, 0.1, "B")
    V25 = hacim_L([(r - 1.5, z) for r, z in hz_dis], 131.7, 525.6)
    kontrol("konik hazne iç hacmi (koni + silindir, L)", V25, 25.0, 1.5, "H")
    kontrol("ürün pistonu strok (Ø52 · 151 ml)", STROK_MAX, 71.1, 0.2, "H")
    kontrol("pnömatik strok hesabı (Ø32 · 0,97 L/çevrim)", PNO_STROK_HESAP, 76.0, 3.0, "H")
    assert XP_ARKA + 20.0 <= 165.0, "piston emişte silindir kapağına çarpıyor"
    assert XP_ON + L_URUN_MILI - 8.0 >= 172.0, "mil kavraması basmada silindirin içine giriyor"
    assert XP_ARKA + L_URUN_MILI + 8.0 <= PNO_X[0], "mil kavraması emişte pnömatik silindire giriyor"
    assert not cakisma(UN, "hacim_ayar_mili", "pnomatik_silindir_D32"), "hacim ayar mili silindire giriyor"
    tumU = UN.kutu_olc()
    print("  toplam (90° ağız + plaka dahil): %.0f × %.0f × %.0f mm · z %.1f…%.1f" % (tumU.xlen, tumU.ylen, tumU.zlen, tumU.zmin, tumU.zmax))
    kal = [d for d in DEN if d["sonuc"] != "GEÇTİ"]
    assert not kal, "KALDI: %s" % kal

    # ---- GLB ----
    mf_kb = glb_yaz(MF, os.path.join(OUT, "beldos_minifill_ep_v1.glb"), ((tum.xmin + tum.xmax) / 2.0, (tum.ymin + tum.ymax) / 2.0, 0.0),
                    [("ROTOR_1", "rotation", ((0.0, 1.0, 0.0), lambda t: mf_rotor_aci(t))),
                     ("ROTOR_2", "rotation", ((0.0, 1.0, 0.0), lambda t: -mf_rotor_aci(t)))], "doz_dongusu_2sn")
    un_kb = glb_yaz(UN, os.path.join(OUT, "beldos_uno275_v1.glb"), ((tumU.xmin + tumU.xmax) / 2.0, (tumU.ymin + tumU.ymax) / 2.0, 0.0),
                    [("PISTON", "translation", lambda t: (uno_piston_dx(t), 0.0, 0.0)),
                     ("VALF", "rotation", ((0.0, 0.0, -1.0), lambda t: uno_valf_aci(t)))], "emis_basma_2sn")

    # ---- JSON (site bu dosyadan okur) ----
    def parca_listesi(M):
        return [dict(ad=p["ad"], etiket=gorunen_ad(p["ad"]), kaynak=p["kaynak"], malzeme=p["mal"], hareket=p["grup"] != "SABIT", not_=p["not_"]) for p in M.P]
    js = dict(
        surum="beldos_cad_v1 · %s" % time.strftime("%d.%m.%Y %H:%M"),
        kaynak_etiketleri=KAYNAK_AD,
        minifill=dict(ad="Beldos Mini-fill Electro-pneumatic 260 W", glb="beldos_minifill_ep_v1.glb", kb=mf_kb,
                      toplam=dict(x=round(tum.xlen), y=round(tum.ylen), z=round(tum.zlen)),
                      hazne_L=round(V15, 1), agiz_ucu_z=SPOUT_UC, cikis_agzi_z=round(AGIZ_Z, 1),
                      parcalar=parca_listesi(MF)),
        uno=dict(ad="Beldos Beltop UNO 275 · çekirdek (sehpasız)", glb="beldos_uno275_v1.glb", kb=un_kb,
                 toplam=dict(x=round(tumU.xlen), y=round(tumU.ylen), z=round(tumU.zlen), zmin=round(tumU.zmin, 1), zmax=round(tumU.zmax, 1)),
                 kaide_H=H_KAIDE, eksen_z=Z_EKSEN, hazne_L=round(V25, 1), strok=round(STROK_MAX, 1),
                 pnomatik_strok_hesap=round(PNO_STROK_HESAP, 1), silinen=[dict(ad=a, kaynak=k, not_=n) for a, k, n in UN.silinen],
                 parcalar=parca_listesi(UN)),
        denetim=DEN)
    with open(os.path.join(OUT, "beldos_v1.json"), "w", encoding="utf-8") as f:
        json.dump(js, f, ensure_ascii=False, indent=1)
    print("JSON beldos_v1.json · %d denetim · hepsi GEÇTİ · %.0f sn" % (len(DEN), time.time() - t0))
