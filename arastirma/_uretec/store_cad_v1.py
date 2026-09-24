# -*- coding: utf-8 -*-
"""AUTOKITCH · B ÇEKMECE MODÜLÜ — ÜRETİM MODELİ v1 (24 Eyl 2026)
Kemal: "şu çekmeceleri detaylandırsana teknik resimdeki gibi"

YERLEŞİM paftadan OKUNUR (teknik_hat_atosa_tablali_v7 · ORTAK VERİ = HAT v19 ile aynı):
  K1 6 pide · K2 2 pide + 6 lahmacun · K3 6 lahmacun + 2 katlı içecek · K4 soğutma grubu + kaşar/sucuk deposu + temizlik nişi
  K1 üstü kuru teknik bölme (B kartı + çekmece sürücüleri). Kolon 620 · bölme 35 · fuga 3 · bindirme 15 (alın 33).
YAPIM detayları eski STORE kararlarından (1_STORE PROBLEMLER M8–M19, Kemal onaylı):
  kulpsuz düz ön: iç sac 1,0 + PU 37,5 + dış sac 1,5 (dört kenardan bükülü) · manyetik conta 21 × 18,5 (sıkışmış 15)
  ön çerçeve sacı 1,0 · çekmece başına 2 teleskopik ray + GT3 kayış + 24 V redüktörlü motor + enkoder + reed sensör.

PAFTADA OLDUĞU GİBİ SIĞMAYAN ÜÇ ŞEY — MODELDE ÇÖZÜLDÜ (hesap aşağıda, denetimde yazdırılır):
  1) TOP YÜKSEKLİĞİ: eski silikon tepsi (30 kalın, 18-20 çukur) ile pide topu 78,5'e, lahmacun topu 68,5'e çıkıyor;
     paftadaki açıklık 75 / 60. Çekmece çekilince top ön çerçeveye çarpar.
     ÇÖZÜM: İNCE TEPSİ 10 mm, çukur 7 + kutu tabanı 5 → top oturma kotu açıklık tabanı + 9.
       pide 9 + 59,5 = 68,5  (açıklık 75 → 6,5 pay) · lahmacun 9 + 47,5 = 56,5 (açıklık 60 → 3,5 pay)
  2) LAHMACUN ADEDİ: eski tepsi 5 × 6 = 30 top; pafta çekmece başına 35 diyor (12 × 30 = 360 < 2 gün 400).
     ÇÖZÜM: 6 × 6 = 36 çukur Ø80 (x adım 88 · z adım 90) → 12 × 36 = 432 ≥ 400.
  3) STROK: pafta 700 diyor. Kayış çekmeceyi arka pabuçtan çeker; pabuç ancak arka motor kasnağı ile ön avara
     arasında gidebilir (avara ön çerçevenin arkasında, motor arka duvarın önünde). Bu derinlikte 640.
     GN 2/1 (650 derin) ile arka sıra top ön yüzün İÇİNDE kalıyordu (merkez z +10 / 0) → robot alamaz.
     ÇÖZÜM: tepsiler derinlikte kısaldı, kutu tepsiye göre: pide 5 × 4 (x 105 · z 130) tepsi 530 × 520, kutu 530;
     lahmacun 6 × 6 tepsi 530 × 540, kutu 550. Açılınca arka sıra topun arka kenarı ön yüzün ÖNÜNDE (denetimde ölçülür).
     Toplar arası boşluk: pide x 10 / z 35 · lahmacun x 13 / z 15 → kavrama ön-arka (z) yönünde.
KOORDİNAT: hat ile aynı — x 0..2500 (B), y 0..1060, z 0 = çekmece ön yüzü, −830 arka.
"""
import io, math, os
import cadquery as cq
from kaset_3d_v3 import MALZEME

U = os.path.dirname(os.path.abspath(__file__))
_p = io.open(os.path.join(U, "teknik_hat_atosa_tablali_v7.py"), encoding="utf-8").read()
_g = {"__name__": "_pafta7", "os": os, "math": math}
exec(_p[_p.index("# ======================= ORTAK VERI (HAT 2 KOL v19) ======================="):_p.index("\nOX, FY_TOP")], _g)
WO, BIND, FUGA, BOLME, XI, YUZ0 = (_g[k] for k in ("WO", "BIND", "FUGA", "BOLME", "XI", "YUZ0"))
HH, CAP, KOLON, KOLON_AD = _g["HH"], _g["CAP"], _g["KOLON"], _g["KOLON_AD"]
H_B, W_B, DZ = _g["H_B"], _g["W_B"], _g["DZ"]

MALZEME.setdefault("sac", dict(renk=(0.74, 0.77, 0.80, 1.0), met=0.85, ruf=0.32))
MALZEME.setdefault("pu", dict(renk=(0.93, 0.88, 0.72, 1.0), met=0.0, ruf=0.85))
MALZEME.setdefault("motor", dict(renk=(0.18, 0.19, 0.22, 1.0), met=0.5, ruf=0.45))
MALZEME.setdefault("kart", dict(renk=(0.10, 0.35, 0.22, 1.0), met=0.1, ruf=0.6))
MALZEME.setdefault("hamur", dict(renk=(0.94, 0.86, 0.68, 1.0), met=0.0, ruf=0.9))
MALZEME.setdefault("silikon", dict(renk=(0.86, 0.30, 0.22, 1.0), met=0.0, ruf=0.7))
MALZEME.setdefault("kutu_icecek", dict(renk=(0.78, 0.10, 0.12, 1.0), met=0.7, ruf=0.35))
MALZEME.setdefault("izgara", dict(renk=(0.30, 0.32, 0.35, 1.0), met=0.6, ruf=0.5))

PARCALAR = []
def ekle(ad, wp, mal, birim, bom=None, grup="SABIT"):
    PARCALAR.append(dict(ad=ad, wp=wp, mal=mal, birim=birim, bom=bom, grup=grup))

kut = lambda x0, x1, y0, y1, z0, z1: cq.Workplane("XY").box(abs(x1 - x0), abs(y1 - y0), abs(z1 - z0), centered=False).translate((min(x0, x1), min(y0, y1), min(z0, z1)))
def sily(x, z, r, y0, y1): return cq.Workplane("XZ").center(x, z).circle(r).extrude(-(y1 - y0)).translate((0, y0, 0))
def silx(y, z, r, x0, x1): return cq.Workplane("YZ").center(y, z).circle(r).extrude(x1 - x0).translate((x0, 0, 0))
def silz(x, y, r, z0, z1): return cq.Workplane("XY").center(x, y).circle(r).extrude(z1 - z0).translate((0, 0, z0))

# ---------------------------------------------------------------- KOTLAR
Z_ON0, Z_ON1 = -40.0, 0.0              # çekmece ön yüzü (40: iç sac 1 + PU 37,5 + dış sac 1,5)
Z_CON0, Z_CON1 = -55.0, -40.0          # manyetik conta 21 × 18,5 (sıkışmış 15)
Z_CER0, Z_CER1 = -56.0, -55.0          # ön çerçeve sacı 1,0
Z_ARKA = -790.0                        # iç arka sac yüzü (arkada 40 sandviç)
Y_PLINT, Y_TABAN, Y_TAVAN = 80.0, 121.5, 1000.0
X_IC0, X_IC1 = 30.0, W_B - 30.0        # yan sandviç 30
KC = 5.0                               # kutu tabanı açıklık tabanından 5 yukarı (ince tepsi için 8 → 5)
KUTU_KENAR = 16.0                      # kutu yan duvarı açıklık kenarından 16 içeride (ray 12,7 + boşluk)
TEPSI_T, CUKUR_H = 10.0, 7.0           # ince tepsi
Y_OTUR = KC + 1.0 + TEPSI_T - CUKUR_H  # 9 — top oturma kotu (açıklık tabanından)
TOP = {"hamur": dict(R=47.5, hc=12.0, cr=50.0, nx=5, nz=4, ax=105.0, az=130.0, td=520.0),   # 220 g · Ø95 × 59,5 (_ortak/HAMUR_TOPU_220g)
       "lahm": dict(R=37.5, hc=10.0, cr=40.0, nx=6, nz=6, ax=88.0, az=90.0, td=540.0)}      # 110 g · Ø75 × 47,5 (_ortak/HAMUR_TOPU_110g)
TUB = {"hamur": 530.0, "lahm": 550.0, "icecek": 660.0}                                   # kutu derinliği = tepsi + 10
# ray: Accuride DZ3832 sınıfı tam çekilir teleskopik ray, 28" (711,2) · kesit 45,7 × 12,7 [katalog; üretici STEP'i henüz alınmadı]
RAY_H, RAY_T, RAY_L, RAY_Y0 = 45.7, 12.7, 711.2, 4.0
# tahrik: GT3 kayış 6 mm · kasnak/avara Ø30 · 24 V redüktörlü DC motor + enkoder (Ø37 sınıfı; parça seçilmedi)
KS_R, KAYIS_X, KAYIS_W, KAYIS_T = 15.0, 17.0, 6.0, 1.5
Y_KAYIS_UST = KC - 1.5                 # kayış üst koşusunun üst yüzü (kutu tabanının 1,5 altı) = 3,5
Y_KASNAK = Y_KAYIS_UST - KAYIS_T - KS_R    # kasnak ekseni açıklık tabanından −13
Z_MOTOR, Z_AVARA = -770.0, -73.0       # motor kasnağı (arka) · ön avara (çerçevenin 2 mm arkası)
PABUC = (-755.0, -725.0)               # kayış pabucu: kutunun ARKASINA uzanan braket üstünde
STROK = (Z_AVARA - KS_R) - PABUC[1] + 3.0   # pabuç ön kenarı avaranın teğet noktasına 3 mm kala durur
ICECEK_KAT = 115.0                     # 330 ml kutu Ø66 × 115
ICECEK = dict(r=33.0, ax=82.0, az=75.0)    # eski STORE hizalama sacı adımı (delik Ø68)


def kolonlar():
    """paftadaki kolon ve çekmece dizilimi → [(kolon, kod, tip, x0, yo)] (yo = AÇIKLIK tabanı)"""
    out, cx = [], XI
    for ki, gruplar in enumerate(KOLON):
        yo, n = YUZ0 + BIND, {}
        for adet, tip in gruplar:
            for _ in range(adet):
                n[tip] = n.get(tip, 0) + 1
                out.append((KOLON_AD[ki], "CEK_%s_%s_%d" % (KOLON_AD[ki], tip, n[tip]), tip, cx, yo))
                yo += HH[tip] + 2 * BIND + FUGA
        cx += WO + BOLME
    return out, cx                                   # cx = K4'ün sol kenarı


CEK, K4X = kolonlar()
K4W = 400.0
KOLON_X = {KOLON_AD[i]: XI + i * (WO + BOLME) for i in range(len(KOLON))}
K1X = KOLON_X["K1"]


def top_kati(tip):
    t = TOP[tip]
    kure = cq.Workplane("XY").sphere(t["R"]).intersect(kut(-t["R"], t["R"], 0.0, t["R"], -t["R"], t["R"])).translate((0, t["hc"], 0))
    return sily(0.0, 0.0, t["R"], 0.0, t["hc"]).union(kure)


def cekmece(kol, kod, tip, x0, yo):
    h = HH[tip]; x1 = x0 + WO; y1 = yo + h; xc = x0 + WO / 2.0
    TUB_D = TUB[tip]; Z_TUB0 = Z_ON0 - TUB_D
    fa, fb, fc, fd = x0 - BIND, x1 + BIND, yo - BIND, y1 + BIND
    G = "CEKMECE"
    # --- ön yüz (hareketli) ---
    ekle(kod + "_on_ic_sac_1.0", kut(fa + 1.5, fb - 1.5, fc + 1.5, fd - 1.5, Z_ON0, Z_ON0 + 1.0), "sac", kod, grup=G)
    ekle(kod + "_on_pu_37.5", kut(fa + 1.5, fb - 1.5, fc + 1.5, fd - 1.5, Z_ON0 + 1.0, Z_ON1 - 1.5), "pu", kod, grup=G)
    ekle(kod + "_on_dis_sac_1.5", kut(fa, fb, fc, fd, Z_ON0, Z_ON1).cut(kut(fa + 1.5, fb - 1.5, fc + 1.5, fd - 1.5, Z_ON0 - 1, Z_ON1 - 1.5)), "sac", kod,
         bom=("Çekmece önü dış sacı 1,5", 1, "304 · dört kenardan bükülü tek parça · kulp YOK", "%d × %d × 40" % (fb - fa, fd - fc)), grup=G)
    ekle(kod + "_conta_manyetik", kut(fa, fb, fc, fd, Z_CON0, Z_CON1).cut(kut(x0, x1, yo, y1, Z_CON0 - 1, Z_CON1 + 1)), "koyu", kod,
         bom=("Manyetik conta 21 × 18,5", 1, "geçmeli PVC + mıknatıs şerit · endüstriyel standart", "ön yüzün arkasında, açıklığa 15 bindirir"), grup=G)
    # --- kutu (hareketli) ---
    ka, kb, kc, kd = x0 + KUTU_KENAR, x1 - KUTU_KENAR, yo + KC, y1 - 10.0
    u = kut(ka, kb, kc, kc + 1.0, Z_TUB0, Z_ON0).union(kut(ka, ka + 1.0, kc, kd, Z_TUB0, Z_ON0)).union(kut(kb - 1.0, kb, kc, kd, Z_TUB0, Z_ON0))
    ekle(kod + "_kutu_U_1.0", u, "sac", kod, bom=("Çekmece kutusu U 1,0", 1, "304 bükme", "%d × %d × %d" % (kb - ka, kd - kc, TUB_D)), grup=G)
    ekle(kod + "_kutu_arka_1.0", kut(ka + 1.0, kb - 1.0, kc + 1.0, kd, Z_TUB0, Z_TUB0 + 1.0), "sac", kod, grup=G)
    # pabuç braketi: kutunun arkasından motor kasnağına doğru uzanır (strok için)
    ekle(kod + "_pabuc_braketi", kut(x0 + 13.0, x0 + 21.0, yo + Y_KAYIS_UST, kc, PABUC[0], Z_TUB0 + 20.0), "celik", kod,
         bom=("Kayış pabucu + çeki kolu", 1, "304 · kutunun altına kaynaklı · kayışı dişli pabuçla sıkar", "kolu kutunun arkasından motor kasnağına kadar uzanır"), grup=G)
    ekle(kod + "_reed_miknatisi", kut(x0 + 21.0, x0 + 24.0, yo + Y_KAYIS_UST, kc, PABUC[0], PABUC[0] + 8.0), "koyu", kod, grup=G)
    # --- ray (her iki yan): dış profil sabit, iç profil kutuyla gezer ---
    for ad_, rx0 in (("sol", x0), ("sag", x1 - RAY_T)):
        ry0 = yo + RAY_Y0
        dis = kut(rx0, rx0 + RAY_T, ry0, ry0 + RAY_H, Z_CER0 - RAY_L, Z_CER0).cut(kut(rx0 + 1.2, rx0 + RAY_T - 1.2, ry0 + 1.2, ry0 + RAY_H - 1.2, Z_CER0 - RAY_L - 1, Z_CER0 + 1))
        ekle(kod + "_ray_dis_" + ad_, dis, "celik", kod,
             bom=("Teleskopik ray 28\" · Accuride DZ3832 sınıfı", 2, "tam çekilir · 45,7 × 12,7 · ~45 kg [üretici STEP'i henüz alınmadı]", "kasaya sabit dış profil") if ad_ == "sol" else None)
        ekle(kod + "_ray_ic_" + ad_, kut(rx0 + 3.0, rx0 + RAY_T - 3.0, ry0 + 5.0, ry0 + RAY_H - 5.0, Z_TUB0, Z_ON0), "celik", kod, grup=G)
    # --- tahrik (sabit): motor grubu arkada, avara önde, kayış altta ---
    kx, ky = x0 + KAYIS_X, yo + Y_KASNAK
    ekle(kod + "_motor_kasnagi", silx(ky, Z_MOTOR, KS_R, kx - 6.0, kx + 6.0), "celik", kod,
         bom=("GT3 kasnak Ø30 · 6 mm", 1, "alüminyum", "motor milinde"))
    ekle(kod + "_reduktor", kut(kx + 8.0, kx + 48.0, ky - 18.5, ky + 18.5, Z_MOTOR - 18.5, Z_MOTOR + 18.5), "motor", kod,
         bom=("24 V redüktörlü DC motor + enkoder", 1, "Ø37 sınıfı · sonsuz vida (kendinden kilitli) · Hall enkoder [PARÇA SEÇİLMEDİ]", "arka plenumda"))
    ekle(kod + "_motor_24V", silx(ky, Z_MOTOR, 18.5, kx + 48.0, kx + 128.0), "motor", kod)
    ekle(kod + "_enkoder", silx(ky, Z_MOTOR, 15.0, kx + 128.0, kx + 143.0), "koyu", kod)
    ekle(kod + "_motor_braketi", kut(kx + 8.0, kx + 60.0, ky - 25.0, ky - 18.5, Z_MOTOR - 18.0, Z_MOTOR + 18.0), "celik", kod)
    ekle(kod + "_avara", silx(ky, Z_AVARA, KS_R, kx - 6.0, kx + 6.0), "celik", kod, bom=("GT3 avara Ø30 · rulmanlı", 1, "alüminyum + 2 × 625-2RS", "ön çerçevenin arkasında"))
    ekle(kod + "_avara_braketi", kut(kx - 12.0, kx - 7.0, ky - 18.0, ky + 8.0, Z_AVARA - 20.0, Z_AVARA + 14.0), "celik", kod)
    kb_ = kut(kx - KAYIS_W / 2, kx + KAYIS_W / 2, yo + Y_KAYIS_UST - KAYIS_T, yo + Y_KAYIS_UST, Z_MOTOR, Z_AVARA)
    kb_ = kb_.union(kut(kx - KAYIS_W / 2, kx + KAYIS_W / 2, ky - KS_R - KAYIS_T, ky - KS_R, Z_MOTOR, Z_AVARA))
    ekle(kod + "_kayis_GT3", kb_, "koyu", kod, bom=("GT3 kayış 6 mm kapalı çevrim", 1, "~%.0f mm · çelik kordlu PU" % (2 * (Z_AVARA - Z_MOTOR) + 2 * math.pi * KS_R), ""))
    ekle(kod + "_reed_sensor", silz(x0 + 36.0, yo + 14.0, 6.0, PABUC[0] - 7.0, PABUC[0] + 13.0), "koyu", kod,
         bom=("Reed sensör Ø12", 1, "kapalı konum · motor braketine", "pabuç braketindeki mıknatısa 6 mm"))
    # --- içerik (hareketli) ---
    if tip in TOP:
        t = TOP[tip]
        tz0, tz1 = Z_TUB0 + 5.0, Z_TUB0 + 5.0 + t["td"]          # kutuya göre kısaltılmış tepsi
        tx0, tx1 = xc - 265.0, xc + 265.0
        ty0 = kc + 1.0
        X = [xc + (i - (t["nx"] - 1) / 2.0) * t["ax"] for i in range(t["nx"])]
        Zc = (tz0 + tz1) / 2.0
        Z = [Zc + (j - (t["nz"] - 1) / 2.0) * t["az"] for j in range(t["nz"])]
        cuk = cq.Workplane("XZ").pushPoints([(a, b) for a in X for b in Z]).circle(t["cr"]).extrude(-(CUKUR_H + 1.0)).translate((0, ty0 + TEPSI_T - CUKUR_H, 0))
        ekle(kod + "_tepsi", kut(tx0, tx1, ty0, ty0 + TEPSI_T, tz0, tz1).cut(cuk), "silikon", kod,
             bom=("İnce tepsi · %d çukur Ø%.0f" % (len(X) * len(Z), 2 * t["cr"]), 1, "gıda silikonu 10 mm · çukur 7", "530 × %.0f" % t["td"]), grup=G)
        tk = top_kati(tip)
        for i, a in enumerate(X):
            for j, b in enumerate(Z):
                ekle("%s_top_%d_%d" % (kod, i, j), tk.translate((a, yo + Y_OTUR, b)), "hamur", kod, grup=G)
        return len(X) * len(Z), yo + Y_OTUR + t["hc"] + t["R"], y1
    # içecek: 2 katlı — alt kat kutu tabanında, üst kat ara rafta
    r = ICECEK["r"]; ix0, ix1, iz0, iz1 = ka + 3.0, kb - 3.0, Z_TUB0 + 6.0, Z_ON0 - 13.0
    nx = int((ix1 - ix0 - 12.0 - 2 * r) // ICECEK["ax"]) + 1
    nz = int((iz1 - iz0 - 19.0 - 2 * r) // ICECEK["az"]) + 1
    X = [(ix0 + ix1) / 2.0 + (i - (nx - 1) / 2.0) * ICECEK["ax"] for i in range(nx)]
    Z = [iz1 - 6.0 - r - j * ICECEK["az"] for j in range(nz)]
    kat0 = kc + 1.0
    kat1 = kat0 + ICECEK_KAT + 1.0 + 1.5          # ara raf alt kat kutularin 1 mm ustunde (241 aciklikta 2,5 pay kalsin)
    ekle(kod + "_ara_raf_1.5", kut(ka + 1.0, kb - 1.0, kat1 - 1.5, kat1, Z_TUB0 + 1.0, Z_ON0), "sac", kod, grup=G)
    kutu = sily(0.0, 0.0, r, 0.0, ICECEK_KAT)
    n = 0
    for k_, yk in enumerate((kat0, kat1)):
        cuk = cq.Workplane("XZ").pushPoints([(a, b) for a in X for b in Z]).circle(r + 1.0).extrude(-4.0).translate((0, yk + 44.0, 0))
        ekle("%s_hizalama_saci_%d" % (kod, k_), kut(ix0, ix1, yk + 44.0, yk + 45.5, iz0, iz1).cut(cuk), "sac", kod, grup=G)
        for a in X:
            for b in Z:
                ekle("%s_kutu330_%d_%d" % (kod, k_, n), kutu.translate((a, yk, b)), "kutu_icecek", kod, grup=G); n += 1
    return n, kat1 + ICECEK_KAT, y1


def kasa():
    B = "B_KASA"
    # plint + ayarlı ayak
    ekle("plint_on_1.5", kut(X_IC0, X_IC1, 0.0, Y_PLINT, -61.5, -60.0), "sac", B, bom=("Plint ön sacı", 1, "304 1,5 · 60 geride", ""))
    for i, (ax, az) in enumerate([(60.0, -110.0), (W_B - 60.0, -110.0), (60.0, -760.0), (W_B - 60.0, -760.0), (W_B / 2.0, -110.0), (W_B / 2.0, -760.0)]):
        ekle("ayak_%d" % i, sily(ax, az, 20.0, 0.0, 8.0).union(sily(ax, az, 6.0, 8.0, Y_PLINT)), "celik", B,
             bom=("Ayarlı ayak M12 Ø40", 6, "paslanmaz", "") if i == 0 else None)
    # dış kabuk 1,5 · PU · iç sac 1,0 : yanlar 30, tavan 60, arka 40, taban 41,5
    # KÖŞE KURALI (çakışma taraması): dış sac — yanlar tam; tavan/taban yanların ARASINDA; arka tavan ile tabanın ARASINDA.
    # PU — yan PU tam yükseklik (taban sacından tavan sacına); tavan/taban/arka PU yan PU'ların ARASINDA (x 29 .. W−29).
    # İç sac — hücreyi çevreler, önde −1,5'te biter; ön dönüş sacı (1_STORE M17) PU'nun önünü kapatır.
    W_ = W_B
    for ad_, dis_x, pu_x, ic_x, don_x in (("sol", (0.0, 1.5), (1.5, 29.0), (29.0, 30.0), (1.5, 30.0)),
                                          ("sag", (W_ - 1.5, W_), (W_ - 29.0, W_ - 1.5), (W_ - 30.0, W_ - 29.0), (W_ - 30.0, W_ - 1.5))):
        ekle("yan_dis_sac_" + ad_, kut(dis_x[0], dis_x[1], Y_PLINT, H_B, -DZ, 0.0), "sac", B)
        ekle("yan_pu_" + ad_, kut(pu_x[0], pu_x[1], Y_PLINT + 1.5, H_B - 1.5, -DZ + 1.5, -1.5), "pu", B)
        ekle("yan_ic_sac_" + ad_, kut(ic_x[0], ic_x[1], Y_TABAN, Y_TAVAN, Z_ARKA, -1.5), "sac", B)
        ekle("yan_on_donus_" + ad_, kut(don_x[0], don_x[1], Y_PLINT + 1.5, H_B - 1.5, -1.5, 0.0), "sac", B)
    ekle("tavan_dis_sac", kut(1.5, W_ - 1.5, H_B - 1.5, H_B, -DZ, 0.0), "sac", B, bom=("Tavan dış sacı", 1, "304 1,5 · A ve C bunun üstüne oturur", ""))
    ekle("tavan_pu_57.5", kut(29.0, W_ - 29.0, Y_TAVAN + 1.0, H_B - 1.5, -DZ + 1.5, -1.5), "pu", B)
    ekle("tavan_ic_sac", kut(X_IC0, X_IC1, Y_TAVAN, Y_TAVAN + 1.0, Z_ARKA, -1.5), "sac", B)
    ekle("tavan_on_donus", kut(X_IC0, X_IC1, Y_TAVAN, H_B - 1.5, -1.5, 0.0), "sac", B)
    ekle("taban_dis_sac", kut(1.5, W_ - 1.5, Y_PLINT, Y_PLINT + 1.5, -DZ, 0.0), "sac", B)
    ekle("taban_pu", kut(29.0, W_ - 29.0, Y_PLINT + 1.5, Y_TABAN - 1.0, -DZ + 1.5, -1.5), "pu", B)
    ekle("taban_ic_sac", kut(X_IC0, X_IC1, Y_TABAN - 1.0, Y_TABAN, Z_ARKA, -1.5), "sac", B)
    ekle("taban_on_donus", kut(X_IC0, X_IC1, Y_PLINT + 1.5, Y_TABAN, -1.5, 0.0), "sac", B)
    ekle("arka_dis_sac", kut(1.5, W_ - 1.5, Y_PLINT + 1.5, H_B - 1.5, -DZ, -DZ + 1.5), "sac", B)
    ekle("arka_pu_37.5", kut(29.0, W_ - 29.0, Y_TABAN - 1.0, Y_TAVAN + 1.0, -DZ + 1.5, Z_ARKA - 1.0), "pu", B)
    ekle("arka_ic_sac", kut(X_IC0, X_IC1, Y_TABAN, Y_TAVAN, Z_ARKA - 1.0, Z_ARKA), "sac", B)
    # kolon bölmeleri 35 sandviç (sac 1 + PU 33 + sac 1)
    bx = [KOLON_X[k] + WO for k in KOLON_AD]                          # K1|K2 · K2|K3 · K3|K4
    for i, x0_ in enumerate(bx):
        ekle("bolme_%d_sac_a" % i, kut(x0_, x0_ + 1.0, Y_TABAN, Y_TAVAN, Z_ARKA, Z_CER0), "sac", B)
        ekle("bolme_%d_pu" % i, kut(x0_ + 1.0, x0_ + BOLME - 1.0, Y_TABAN, Y_TAVAN, Z_ARKA, Z_CER0), "pu", B)
        ekle("bolme_%d_sac_b" % i, kut(x0_ + BOLME - 1.0, x0_ + BOLME, Y_TABAN, Y_TAVAN, Z_ARKA, Z_CER0), "sac", B)
    # K1 üstü kuru teknik bölme: PU 40 raf + B kartı + sürücüler + 24 V
    k1_ust = max(yo + HH[t] + BIND for kol, _k, t, x0, yo in CEK if kol == "K1")          # 812,5
    ry0 = k1_ust + 3.0
    ekle("k1_teknik_raf_sac_alt", kut(K1X, K1X + WO, ry0, ry0 + 1.0, Z_ARKA, Z_CER0), "sac", B)
    ekle("k1_teknik_raf_pu_38", kut(K1X, K1X + WO, ry0 + 1.0, ry0 + 39.0, Z_ARKA, Z_CER0), "pu", B)
    ekle("k1_teknik_raf_sac_ust", kut(K1X, K1X + WO, ry0 + 39.0, ry0 + 40.0, Z_ARKA, Z_CER0), "sac", B)
    ty = ry0 + 40.0
    ekle("B_karti_kutusu", kut(K1X + 60.0, K1X + 260.0, ty + 25.0, ty + 110.0, -330.0, -120.0), "kart", "B_KART",
         bom=("B kartı (çekmece PLC giriş/çıkış)", 1, "DIN kutu 200 × 85", "kuru bölmede"))
    ekle("din_ray_suruculer", kut(K1X + 295.0, K1X + 615.0, ty + 55.0, ty + 62.5, -240.0, -235.0), "celik", "B_KART")
    ns = len(CEK)
    for i in range(ns):
        sx = K1X + 298.0 + i * 12.4
        ekle("surucu_%02d" % (i + 1), kut(sx, sx + 12.0, ty + 25.0, ty + 110.0, -235.0, -140.0), "kart", "B_KART",
             bom=("DC motor sürücüsü 24 V · DIN 12 mm", ns, "akım sınırlı (sıkışma algılar) · enkoder girişli", "çekmece başına 1") if i == 0 else None)
    ekle("guc_kaynagi_24V", kut(K1X + 60.0, K1X + 260.0, ty + 25.0, ty + 110.0, -560.0, -350.0), "kart", "B_KART",
         bom=("24 V 10 A güç kaynağı", 1, "DIN", "aynı anda en çok 2 çekmece döner"))
    # evaporatörler: her soğuk kolonun arka plenumunda, motor bandının (sol 17..160) dışında
    for kol in ("K1", "K2", "K3"):
        cx = KOLON_X[kol]
        e0, e1 = (330.0, 680.0) if kol == "K1" else (520.0, 900.0)        # fan evaporatorun ALTINDA (ust tavan / K1 kart rafi dolu)
        ekle("evaporator_%s" % kol, kut(cx + 250.0, cx + 560.0, e0, e1, Z_ARKA + 2.0, Z_ARKA + 30.0), "bakir", "B_SOGUTMA",
             bom=("Evaporatör panel 310 × 350..380 × 28", 3, "bakır boru + alüminyum lamel", "arka plenumda, çekmece tahrikinin dışında") if kol == "K1" else None)
        ekle("evap_fan_%s" % kol, kut(cx + 330.0, cx + 480.0, e0 - 160.0, e0 - 10.0, Z_ARKA + 2.0, Z_ARKA + 32.0), "motor", "B_SOGUTMA")
    # K4: soğutma grubu (havalandırmalı ayrı bölme) + kaşar/sucuk deposu + temizlik nişi
    kx0, kx1 = K4X, K4X + K4W
    ekle("sogutma_grubu_1_3HP", kut(kx0 + 5.0, kx1 - 5.0, Y_TABAN + 5.0, Y_TABAN + 225.0, Z_CER0 - 305.0, Z_CER0 - 5.0), "motor", "B_SOGUTMA",
         bom=("Soğutma grubu ⅓ HP", 1, "R290 · 400 × 300 × 220", "K4 altı, öne ızgaralı kapaktan hava alır"))
    s0 = Y_TABAN + 230.0
    ekle("k4_ara_sac_alt", kut(kx0, kx1, s0, s0 + 1.0, Z_ARKA, Z_CER0), "sac", "B_SOGUTMA")
    ekle("k4_ara_pu", kut(kx0, kx1, s0 + 1.0, s0 + 29.0, Z_ARKA, Z_CER0), "pu", "B_SOGUTMA")
    ekle("k4_ara_sac_ust", kut(kx0, kx1, s0 + 29.0, s0 + 30.0, Z_ARKA, Z_CER0), "sac", "B_SOGUTMA")
    d0 = s0 + 30.0; d1 = d0 + 300.0
    for j in range(2):
        gy = d0 + 5.0 + j * 150.0
        ekle("k4_depo_GN11_%d" % j, kut(kx0 + 37.5, kx1 - 37.5, gy, gy + 140.0, Z_CER0 - 540.0, Z_CER0 - 10.0).cut(kut(kx0 + 38.5, kx1 - 38.5, gy + 1.0, gy + 141.0, Z_CER0 - 539.0, Z_CER0 - 11.0)),
             "sac", "B_DEPO", bom=("GN 1/1-150 kap", 2, "304 · kaşar blok / sucuk", "4 günlük depo (içerik VARSAYIM)") if j == 0 else None)
    ekle("k4_depo_raf", kut(kx0, kx1, d0 + 150.0, d0 + 151.5, Z_ARKA, Z_CER0), "sac", "B_DEPO")
    ekle("k4_nis_raf", kut(kx0, kx1, d1 + 3.0, d1 + 4.5, Z_ARKA, Z_CER0), "sac", "B_TEMIZLIK")
    for j in range(2):
        ekle("bidon_5L_%d" % j, sily(kx0 + 110.0 + j * 180.0, Z_CER0 - 180.0, 85.0, d1 + 4.5, d1 + 4.5 + 250.0), "pom", "B_TEMIZLIK",
             bom=("Temizlik malzemesi bidonu 5 L", 2, "deterjan / dezenfektan", "") if j == 0 else None)
    # K4 kapakları (3): ızgaralı soğutma kapağı · depo kapağı · niş kapağı — hepsi çekmece önüyle aynı düzlemde
    kapak = [("k4_kapak_sogutma", Y_TABAN + 3.0, s0 + 12.0, "B_SOGUTMA"), ("k4_kapak_depo", s0 + 15.0, d1 + 1.0, "B_DEPO"), ("k4_kapak_nis", d1 + 4.0, Y_TAVAN - 3.0, "B_TEMIZLIK")]
    PENCERE = (kx0 + 20.0, kx1 - 20.0, Y_TABAN + 23.0, Y_TABAN + 213.0)          # soğutma kapağı hava penceresi
    for ad_, y0_, y1_, bir in kapak:
        a_, b_ = kx0 - BIND, kx1 + BIND
        ds = kut(a_, b_, y0_, y1_, Z_ON0, Z_ON1).cut(kut(a_ + 1.5, b_ - 1.5, y0_ + 1.5, y1_ - 1.5, Z_ON0 - 1, Z_ON1 - 1.5))
        if bir == "B_SOGUTMA":                                                  # sıcak bölme: yalıtımsız, ızgaralı
            ds = ds.cut(kut(PENCERE[0], PENCERE[1], PENCERE[2], PENCERE[3], Z_ON0 - 1, Z_ON1 + 1))
            ekle(ad_ + "_dis_sac", ds, "sac", bir, bom=("Soğutma bölmesi kapağı", 1, "304 1,5 · yalıtımsız · ızgaralı hava penceresi", "yoğuşturucu havasını önden alır"))
            continue
        ekle(ad_ + "_dis_sac", ds, "sac", bir)
        ekle(ad_ + "_pu", kut(a_ + 1.5, b_ - 1.5, y0_ + 1.5, y1_ - 1.5, Z_ON0, Z_ON1 - 1.5), "pu", bir)
    for i in range(11):
        gy = PENCERE[2] + 7.0 + i * 16.0
        ekle("k4_izgara_%02d" % i, kut(PENCERE[0], PENCERE[1], gy, gy + 8.0, Z_ON1 - 1.5, Z_ON1), "izgara", "B_SOGUTMA")
    # K1 teknik bölme kapağı + K2 üstü boş kalan şerit (sabit panel)
    k2_ust = max(yo + HH[t] + BIND for kol, _k, t, x0, yo in CEK if kol == "K2")
    for ad_, xx, y0_, y1_, bir in (("k1_teknik_kapak", K1X, ry0, Y_TAVAN - 3.0, "B_KART"), ("k2_ust_panel", KOLON_X["K2"], k2_ust + 3.0, Y_TAVAN - 3.0, B)):
        a_, b_ = xx - BIND, xx + WO + BIND
        ekle(ad_ + "_dis_sac", kut(a_, b_, y0_, y1_, Z_ON0, Z_ON1).cut(kut(a_ + 1.5, b_ - 1.5, y0_ + 1.5, y1_ - 1.5, Z_ON0 - 1, Z_ON1 - 1.5)), "sac", bir)
        ekle(ad_ + "_pu", kut(a_ + 1.5, b_ - 1.5, y0_ + 1.5, y1_ - 1.5, Z_ON0, Z_ON1 - 1.5), "pu", bir)
    # ön çerçeve sacı 1,0: bütün açıklıklar kesik
    cer = kut(X_IC0, X_IC1, Y_TABAN, Y_TAVAN, Z_CER0, Z_CER1)
    for kol, kod, tip, x0, yo in CEK:
        cer = cer.cut(kut(x0, x0 + WO, yo, yo + HH[tip], Z_CER0 - 1, Z_CER1 + 1))
    for _a, y0_, y1_, _b in kapak:
        cer = cer.cut(kut(kx0, kx1, y0_ + BIND, y1_ - BIND, Z_CER0 - 1, Z_CER1 + 1))
    cer = cer.cut(kut(K1X, K1X + WO, ry0 + BIND, Y_TAVAN - 3.0 - BIND, Z_CER0 - 1, Z_CER1 + 1))
    ekle("on_cerceve_saci_1.0", cer, "sac", B, bom=("Ön çerçeve sacı 1,0", 1, "304 lazer kesim · %d açıklık" % (len(CEK) + 4), "conta buna basar"))


def modul():
    PARCALAR[:] = []
    kasa()
    ozet = []
    for kol, kod, tip, x0, yo in CEK:
        n, ust, acik_ust = cekmece(kol, kod, tip, x0, yo)
        ozet.append((kod, tip, n, ust, acik_ust))
    return ozet


def denetim(ozet):
    print("B CEKMECE MODULU · %d parca · %d cekmece" % (len(PARCALAR), len(CEK)))
    for kod, tip, n, ust, acik in ozet:
        print("   %-22s %-7s %3d adet · icerik ustu %.1f · aciklik ustu %.1f · pay %.1f" % (kod, tip, n, ust, acik, acik - ust))
        assert acik - ust >= 2.0, "%s: icerik aciklik ustune %.1f mm kaliyor" % (kod, acik - ust)
    pide = sum(n for _k, t, n, _u, _a in ozet if t == "hamur"); lahm = sum(n for _k, t, n, _u, _a in ozet if t == "lahm")
    ice = sum(n for _k, t, n, _u, _a in ozet if t == "icecek")
    print("KAPASITE: pide %d top (2 gun = 160) · lahmacun %d top (2 gun = 400) · icecek %d kutu (pafta 180)" % (pide, lahm, ice))
    assert pide >= 160 and lahm >= 400, "2 gunluk hamur kapasitesi tutmuyor"
    print("STROK: kayis pabucu %.0f..%.0f · on avara z %.0f -> strok %.0f mm (pafta 700)" % (PABUC[0], PABUC[1], Z_AVARA, STROK))
    for tip in TOP:
        t = TOP[tip]; z_tub0 = Z_ON0 - TUB[tip]
        arka = z_tub0 + 5.0 + t["td"] / 2.0 - (t["nz"] - 1) / 2.0 * t["az"]        # kapaliyken arka sira merkezi
        kenar = arka + STROK - t["R"]
        print("   %s: arka sira top merkezi acilinca z %+.0f · topun arka kenari z %+.0f (on yuz 0) · x bosluk %.0f · z bosluk %.0f"
              % (tip, arka + STROK, kenar, t["ax"] - 2 * t["R"], t["az"] - 2 * t["R"]))
        assert kenar >= 5.0, "%s arka sira acilinca on yuzun icinde kaliyor" % tip
        assert t["nx"] * t["ax"] <= 530.0 + 0.1 and (t["nz"] - 1) * t["az"] + 2 * t["cr"] <= t["td"] + 0.1, "%s tepsi disina tasiyor" % tip
    print("SURUCU: %d cekmece -> %d surucu (paftada 20 yaziyordu)" % (len(CEK), len(CEK)))
    cakisma()


def cakisma(esik=1.0):
    """GERCEK KESISIM taramasi: kutu zarfi on elemesi + OCC kesisim hacmi. Icerik (top/kutu) haric —
    onlar tepsinin ve kutunun icinde, tepsi/kutu zaten taraniyor. Degen yuzeyler (hacim 0) sayilmaz."""
    import time as _t
    t0 = _t.time()
    L = [(p, p["wp"].val()) for p in PARCALAR if "_top_" not in p["ad"] and "_kutu330_" not in p["ad"]]
    L = [(p, v, v.BoundingBox()) for p, v in L]
    bul, aday = [], 0
    for i in range(len(L)):
        p, a, A = L[i]
        for j in range(i + 1, len(L)):
            q, b, Bb = L[j]
            if A.xmin >= Bb.xmax - 0.05 or Bb.xmin >= A.xmax - 0.05 or A.ymin >= Bb.ymax - 0.05 or Bb.ymin >= A.ymax - 0.05 or A.zmin >= Bb.zmax - 0.05 or Bb.zmin >= A.zmax - 0.05:
                continue
            aday += 1
            v = a.intersect(b).Volume()
            if v > esik:
                bul.append((v, p["ad"], q["ad"]))
    bul.sort(reverse=True)
    print("CAKISMA TARAMASI: %d parca · %d aday cift · %d gercek kesisim (> %.0f mm3) · %.0f sn" % (len(L), aday, len(bul), esik, _t.time() - t0))
    for v, a, b in bul[:40]:
        print("    %9.0f mm3  %s  <->  %s" % (v, a, b))
    assert not bul, "B modulunde %d cakisma var" % len(bul)
    # ---- ACIK KONUM: hareketli paketler (cekmece) STROK kadar one alinir, sabit parcalarla taranir ----
    t0 = _t.time()
    H = [(p, v.translate(cq.Vector(0.0, 0.0, STROK))) for p, v, _B in L if p["grup"] == "CEKMECE"]
    H = [(p, v, v.BoundingBox()) for p, v in H]
    S = [(p, v, Bb) for p, v, Bb in L if p["grup"] != "CEKMECE"]
    bul, aday = [], 0
    for p, a, A in H:
        for q, b, Bb in S:
            if A.xmin >= Bb.xmax - 0.05 or Bb.xmin >= A.xmax - 0.05 or A.ymin >= Bb.ymax - 0.05 or Bb.ymin >= A.ymax - 0.05 or A.zmin >= Bb.zmax - 0.05 or Bb.zmin >= A.zmax - 0.05:
                continue
            aday += 1
            v = a.intersect(b).Volume()
            if v > esik:
                bul.append((v, p["ad"], q["ad"]))
    bul.sort(reverse=True)
    print("ACIK KONUM TARAMASI (strok %.0f): %d hareketli x %d sabit parca · %d aday · %d gercek kesisim · %.0f sn" % (STROK, len(H), len(S), aday, len(bul), _t.time() - t0))
    for v, a, b in bul[:40]:
        print("    %9.0f mm3  %s  <->  %s" % (v, a, b))
    assert not bul, "acik konumda %d cakisma var" % len(bul)


if __name__ == "__main__":
    oz = modul(); denetim(oz)
