# -*- coding: utf-8 -*-
"""AUTOKITCH · F FIRIN ÜSTÜ KABİN · CAD v1 (27 Eyl 2026 gece · 28 Eyl denetim düzeltmesi) — SPEC_on_duzlem_v63.md §2.4 · keşif on_duzlem_v63/kesif_F.md
Fırın (firin_tp10_cad_v8, gövde 788–1305, ön yüz +79) üstündeki bölmeyi TEMİZ KUTU yapar: ön düzlem +79, arka −830, üst 1862.
28 Eyl DENETİM DÜZELTMESİ (rapor_F.md "DENETÇİ BULGULARI"):
  · HDS-10S-K soft-down stay (kapasite çift başına 5,9–9,3 N·m < kanat 15,8 N·m; gövde 88 × 280 × 30,5 pizza / kompresör yoluna giriyordu) KALDIRILDI →
    kanat başına 1 ÇEKME TİPİ GAZLI YAY (Bansbach easylift gas traction spring 6/15, dış yan şeritte x 2502,75–2517,75 / 3982,25–3997,25):
    kapak açıldıkça uzar, kapağı geri çeker; 0°–90° dengesi hesapla (YAY) — kapak kendiliğinden kapalı kalır, 10°'den sonra 0,2–3 N·m ile yavaş iner.
    İtme tipi yay (Stabilus LIFT-O-MAT) bu menteşe geometrisinde 90°'de moment üretemez (hesap: rapor).
  · Kapağa BURULMA KUTUSU (1,0 C profil, alt bant, y 1309,5–1395): yay tek uçtan tutar, kutu torku iç kenara taşır.
  · Menteşe iki yaprak (sabit: kayıt önünde z 57–59 · hareketli: kutu sırtında z 59–60,5) · süpürme menteşe + yay dahil ölçülür.
  · Mıknatıslı tamponlar SİLİNDİ (hiçbir şeye değmiyorlardı); Blum TIP-ON 956.1004 setinin vidalı karşı plakası kapağa (304 manyetik değil).
  · Tavan kirişinin önüne DİKME (x 3336–3366) + kompresör üstünde 2. dikme (x 3560–3590): üst sacın ön kenarı pizza dışında taşınır.
  · Kompresör: kaynaklı eyer + raf üstü takoz SİLİNDİ → raf açıklığına asılı KOMPRESÖR TAVASI (y 1324–1328) + üreticinin 4 ayağı + 4 titreşim takozu (20);
    tank raftan ayrıldı; gerçek 380 × 380 × 510 zarfı (föy) y 1328–1838 = TU KOMP kutusu (montaj KOMP_KAY DEĞİŞMEZ).
  · Hava hattı geçme bileziği iç Ø10 = hat (sıkı, hattı taşır) · ön çerçeve / donanım adları onyuz_ ile.
PARÇALAR (dünya koordinatı · mm · 304 fırçalı sac 1,5 · üst sac 430):
  · YAN SACLAR (L): sol x 2500–2501,5 · sağ x 3998,5–4000 · üstte y 1305–1860,5 × z −828,5…+59, fırının arkasında şerit y 788–1305 × z −828,5…−651
    · önde (yay geçişinde kertikli) + arkada 15 mm iç büküm · hava hattı Ø16 delik + EPDM geçme bileziği (iç Ø10).
  · ÜST SAC y 1860,5–1862 (430) · 3 kenarı 20 aşağı bükülü (ön kenar serbest: pizza 0,5 mm altında, bkz. AÇIK) · davlumbaz atış ağzı · tavan kirişi + 2 ön dikme.
  · ARKA SAC tek parça y 788–1862 · 4 rakor + 2 panjur.
  · ÖN KAYIT 30 × 30 × 2 (y 1308–1338, z +27…+57) + 3 takoz · 2 dikme 30 × 30 × 2.
  · ÖN KAPAKLAR (onyuz_): 2 kanat tava 20 · x 2500–3248,5 / 3251,5–4000 · y 1308–1859 · ALTTAN MENTEŞELİ DÜŞER KAPAK (pivot y 1308, z +79) · 90°'de dolum rafı.
  · DAVLUMBAZ SAC KUTUSU x 2501,5–3998,5 · y 1315–1790 · z −827…−440 (KARAR: üst 1790) · yan saclara 2 köşebentle asılı.
  · KOMPRESÖR TAVASI + AYAKLAR (F_KOMP_AYAK).
DOKUNULMAYAN: fırın gövdesi / ürün yolu, pizza yedeği 320 kutu (x 2520–3324 · y 1348–1860 · z −424…−20), kompresörün yeri (TU KOMP + KOMP_KAY), hava hattı.
Sözleşme (bulasik_cad_v1 / kaide_cad_v1): kur() · PARCALAR · dunya(p) · BIRIMLER · BIRIM_MODUL (+ ON_BIRIMLER, KAPAK_EKSEN, yay_konum(), havada_denetimi()).
"""
import math, os, sys, time
import cadquery as cq

U = os.path.dirname(os.path.abspath(__file__)); KOK = os.path.dirname(os.path.dirname(U)); sys.path.insert(0, U)
import firin_tp10_cad_v8 as FT

# ================================================================ ÖLÇÜLER ================================================================
Z_ON = FT.Z_ON                                   # +79 ön düzlem (fırın gövdesinin ön yüzü)
TAVA = 20.0                                      # kuru kapak / panel derinliği (SPEC tava 20)
Z_TAVA = Z_ON - TAVA                             # +59 · gövde sacları buraya kadar (kapak arkası)
SAC, SAC_IC = 1.5, 1.0                           # 304 dış sac · omega / burulma kutusu
Z_ARKA = -830.0                                  # arka yüz SABİT
Z_ARKA_IC = Z_ARKA + SAC                         # −828,5
X0, X1 = FT.X_F0, FT.X_F1                        # 2500 · 4000
Y_TABAN = FT.YG0                                 # 788 (dolap üstü)
Y_GOV = FT.YG1                                   # 1305 (fırın üstü)
H_MAK = 1862.0                                   # makine üstü
Y_TAVAN = H_MAK - SAC                            # 1860,5 üst sac altı
Z_FARKA = -FT.D_TP + FT.ZS                       # −651 fırın gövdesi arka yüzü
DERZ = 3.0
FLANS = 15.0                                     # yan sac iç bükümü
KAPAK_Y = (Y_GOV + DERZ, H_MAK - DERZ)           # 1308 · 1859
XM = (X0 + X1) / 2.0                             # 3250
KANAT_X = ((X0, XM - DERZ / 2.0), (XM + DERZ / 2.0, X1))   # 2500–3248,5 · 3251,5–4000
PIVOT = (KAPAK_Y[0], Z_ON)                       # alt ön kenar (y 1308, z +79) · eksen x
ACI_ACIK = 90.0
# ---- dokunulmayanlar (dünya) ----
PIZZA_UST_KUTU, KUTU_T = 320, 1.6                # KURAL (Kemal): 320 kutu · 512 mm yığın
PIZZA = (X0 + 20.0, X0 + 824.0, FT.UST_RAF_Y[1], FT.UST_RAF_Y[1] + PIZZA_UST_KUTU * KUTU_T, -424.0, -20.0)   # = hat_montaj D_PIZZA_YEDEK_UST
X_BC, DY, KOMP_KAY = 700.0, -168.0, (-510.0, 976.0, 0.0)     # hat_montaj_v62: TOPPING x0 · alçak hat · kompresör taşıması (TU → fırın üstü) — DEĞİŞMEZ
TANK = dict(x=(3600.0, 3980.0), yc=1498.0, zc=-230.0, r=150.0)   # JUN-AIR OF302-15B tankı dünyada (TU KOMP + KOMP_KAY) — __main__ TU'dan ölçer
KOMP_ZARF = (3600.0, 3980.0, 1348.0, 1838.0, -380.0, -80.0)      # TU modeli: tank + motor (ölçülen; vana hariç — TOPPING v14 yerini değiştiriyor)
KOMP_GERCEK = (3600.0, 3980.0, 1328.0, 1838.0, -420.0, -40.0)    # föy 380 × 380 × 510 (25 kg) = TU KOMP kutusu dünyada: ayak altı 1328 (tava) · üst 1838
KOMP_KALDIR = 20.0                               # servis: ayaklar tavadan çıksın diye 20 kaldırılır, sonra öne çekilir
HAVA_R = 5.0                                     # Ø10 PU ana hat
ANA = [(3790.0, 1809.0, -380.0), (3790.0, 1809.0, -432.0), (2340.0, 1809.0, -432.0), (2340.0, 1809.0, -740.0), (2340.0, 1167.0, -740.0), (2350.0, 1167.0, -740.0)]   # hat_montaj_v62 ANA_V44 + DY + X_BC
K_DALI = [(3790.0, 1809.0, -432.0), (3790.0, 1809.0, -780.0), (4085.0, 1809.0, -780.0), (4085.0, 1702.0, -780.0)]                                                   # ANA_K48 + DY + X_BC
DELIK = dict(sol=(X0, 1809.0, -432.0), sag=(X1, 1809.0, -780.0))   # yan sac rakor delikleri (SPEC)
R_DELIK, R_BILEZIK_IC, R_BILEZIK_FL = 8.0, HAVA_R, 11.0          # bilezik iç Ø10 = hat (sıkı geçme: hattı taşır · denetçi #10)
# ---- iç düzen ----
KAYIT = (X0 + SAC, X1 - SAC, KAPAK_Y[0], KAPAK_Y[0] + 30.0, Z_TAVA - 32.0, Z_TAVA - 2.0)   # 30 × 30 × 2 · y 1308–1338 · z +27…+57
KAYIT_TAKOZ_X = (2875.0, 3250.0, 3625.0)
KIRIS_X = (3336.0, 3366.0)                        # tavan kirişi (pizza sağ kenarı 3324 + 12)
DIKME_X = (KIRIS_X, (3560.0, 3590.0))             # ön dikmeler: kiriş altı (üst sacı kirişle) · kompresör solu (üst sacı doğrudan) — pizza 3324 < · < 3600 kompresör
DAV = (X0 + SAC, X1 - SAC, Y_GOV + 10.0, 1790.0, Z_ARKA_IC + SAC, -440.0)   # davlumbaz kutusu (KARAR: üst 1790)
ATIS = (2950.0, 3250.0, -720.0, -520.0)           # atış ağzı x · z (300 × 200)
PANJUR_X = (FT.X_DUV0 + 76.0, FT.X_F1 - 140.0)    # 2640 · 3860 = fırın teknik bölme fanları
PANJUR_Y = FT.YG0 + 194.0                         # 982
RAKOR = [("cee_firin", 2560.0, 860.0, 16.5, 20.0, "M32 · fırın beslemesi 5G6 (32 A CEE fişi arka yüzde, x 2530 y 988)"),
         ("sinyal_firin", 2630.0, 830.0, 10.25, 13.0, "M20 · fırın sinyal kablosu"),
         ("kompresor", 3930.0, 1825.0, 10.25, 13.0, "M20 · kompresör beslemesi 230 V (tesisat bandından)"),
         ("davlumbaz_fani", 2600.0, 1825.0, 10.25, 13.0, "M20 · davlumbaz fanı beslemesi")]
# ---- kompresör tavası + ayaklar (raf açıklığı firin_tp10_cad_v8.KOMP_ACIKLIK x 3595–3991 · z −385…−75) ----
TAVA_K = dict(x=(3597.0, 3988.0), z=(-383.0, -77.0), y=(1324.0, 1328.0), duvar=2.0, flans=12.0, ust=FT.UST_RAF_Y[0])   # flanşlar raf altına (1341–1344)
AYAK_X, AYAK_Z = (3625.0, 3955.0), (-340.0, -120.0)   # üreticinin 4 ayağı (VARSAYIM föy) · Ø40 × 20 titreşim takozu
# ---- kapak iç yapısı ----
KUTU_Y = (KAPAK_Y[0] + SAC, 1395.0)               # burulma kutusu y 1309,5–1395 (alt bant) · C 1,0 · z 60,5…77,5
KUTU_Z = (Z_TAVA + SAC, Z_ON - SAC)               # 60,5 · 77,5
SERIT = 17.0                                      # dış kenar şeridi (yay + pim): kutu uç plakası dış kenardan 17 … 18
YARIK_SIRA = ((1405.0, 1417.0, 1429.0), (1810.0, 1822.0, 1834.0))   # alt (emiş, kutunun üstünde) · üst (atış) bant · yarık 90 × 5
YARIK_W, YARIK_H, YARIK_N, YARIK_X0, YARIK_ADIM = 90.0, 5.0, 6, 55.0, 110.0
OMEGA_Y = (1445.0, 1795.0)
MENTESE_DX = 130.0                                # kanat kenarından menteşe ekseni (2 / kanat)
# ---- ÇEKME TİPİ GAZLI YAY (Bansbach easylift gas traction spring 6/15 · boy / kuvvet siparişe göre) — F_gazli_hesap ile seçildi ----
YAY = dict(sB=36.0, tB=-9.5, A=(1605.0, 0.0), Lr=268.0, S=47.0, F1=315.0, prog=1.30, FR=50.0,
           D_GOVDE=15.0, D_MIL=6.0, R_GOZ=6.5, T_GOZ=3.0, D_PIM=6.0, BOYUN=12.0, BOS=8.0)
YAY_XC = (X0 + SAC + 8.75, X1 - SAC - 8.75)       # yay ekseni x: sol 2510,25 · sağ 3989,75 (gövde Ø15 → 2502,75–2517,75 · pizza 2520 / kompresör 3980)
RAF_YUKU = 5.0                                    # kg · açık kapak dolum rafı (kanat başına, VARSAYIM)
RO = 7.93e-6                                      # kg/mm³ 304

PARCALAR = []
BIRIMLER = [
    ("F_UST_KABIN", "Fırın üstü kabin gövdesi (bizim) · 304 1,5: L yan saclar (sol 2500–2501,5 · sağ 3998,5–4000, fırın arkasında şeritle dolap üstüne) · üst sac 1860,5–1862 (430, 3 kenarı bükülü, atış ağzı) · TEK PARÇA ARKA SAC 788–1862 (4 rakor + 2 panjur) · ön kayıt 30 × 30 × 2 + 2 dikme · tavan kirişi · hava hattı Ø16 delik + EPDM bilezik (iç Ø10)"),
    ("F_UST_KAPAK", "Fırın üstü ön kapakları · 2 kanat tava 20 (304 fırçalı 1,5, z +59…+79) · x 2500–3248,5 / 3251,5–4000 · y 1308–1859 · ALTTAN MENTEŞELİ DÜŞER KAPAK (Sugatsune SDH-001 · kanat başına 1 çekme gazlı yay Bansbach 6/15 · burulma kutusu) · açıkken dolum rafı · lazer yarık havalandırma · Blum TIP-ON 956.1004 (mıknatıslı, karşı plakalı) · kulp yok"),
    ("F_DAVLUMBAZ", "Davlumbaz sac kutusu (bizim) · 304 1,5 · x 2501,5–3998,5 · y 1315–1790 · z −827…−440 · yan saclara L 40 × 40 × 3 köşebentle asılı · ön yüzde emiş yarıkları (kompresör arkası) · atış kanalı 300 × 200 üst saca · fan + yağ/karbon filtre içinde (AÇIK)"),
    ("F_KOMP_AYAK", "Kompresör tavası (bizim, 304 4 mm · raf açıklığına flanşla asılı, y 1324–1328) + JUN-AIR OF302-15B'nin 4 ayağı ve titreşim takozları (üreticinin, Ø40 × 20 · föy ölçüsü VARSAYIM) · tank raftan 20 mm yukarıda"),
]
BIRIM_MODUL = {k: "D" for k, _a in BIRIMLER}
ON_BIRIMLER = ("F_UST_KAPAK",)                    # ön düzleme (+79) değen birim
KAPAK_EKSEN = {"KAPAK_F_SOL": ((X0, PIVOT[0], PIVOT[1]), (1.0, 0.0, 0.0), ACI_ACIK),   # grup → (eksen noktası, yön, açık açı °) · + açı = üst kenar öne
               "KAPAK_F_SAG": ((X0, PIVOT[0], PIVOT[1]), (1.0, 0.0, 0.0), ACI_ACIK)}
YAY_GRUP = ("YAY_F_SOL", "YAY_F_SAG")             # gazlı yaylar katı dönmez: montaj animasyonu yay_konum(tag, açı) ile yeniden kurar
MALZEME = {"sac": dict(renk=(0.74, 0.77, 0.80, 1.0), met=0.85, ruf=0.32), "paslanmaz": dict(renk=(0.80, 0.82, 0.84, 1.0), met=0.9, ruf=0.30),
           "celik": dict(renk=(0.60, 0.62, 0.66, 1.0), met=1.0, ruf=0.35), "koyu": dict(renk=(0.10, 0.10, 0.11, 1.0), met=0.1, ruf=0.6),
           "conta": dict(renk=(0.90, 0.90, 0.88, 1.0), met=0.0, ruf=0.8), "plastik": dict(renk=(0.55, 0.57, 0.60, 1.0), met=0.0, ruf=0.6)}


# ================================================================ YARDIMCILAR ================================================================
def kut(x0, x1, y0, y1, z0, z1):
    return cq.Workplane("XY").box(abs(x1 - x0), abs(y1 - y0), abs(z1 - z0), centered=False).translate((min(x0, x1), min(y0, y1), min(z0, z1)))
def silx(y, z, r, x0, x1): return cq.Workplane("YZ", origin=(min(x0, x1), y, z)).circle(r).extrude(abs(x1 - x0))
def silz(x, y, r, z0, z1): return cq.Workplane("XY").center(x, y).circle(r).extrude(z1 - z0).translate((0, 0, z0))
def sily(x, z, r, y0, y1): return cq.Workplane("XZ", origin=(x, max(y0, y1), z)).circle(r).extrude(abs(y1 - y0))


def ayna(x0, x1, k):
    """sol kanat için yazılan x aralığı → k = 1 (sağ) ise XM etrafında aynası"""
    return (x0, x1) if k == 0 else (2.0 * XM - x1, 2.0 * XM - x0)


def ekle(ad, wp, mal, birim, bom=None, grup="SABIT", kaynak="VARSAYIM"):
    """bom = (kalem, adet, tanım, not/kaynak, tür)"""
    assert all(p["ad"] != ad for p in PARCALAR), ad
    PARCALAR.append(dict(ad=ad, wp=wp, mal=mal, birim=birim, grup=grup, kaynak=kaynak, bom=bom))


def dunya(p):
    v = p["wp"].vals()
    return v[0] if len(v) == 1 else cq.Compound.makeCompound([o for o in v if isinstance(o, cq.Shape)])


def boru(pts, r):
    """hat_montaj / topping_uno_cad boru() ile aynı: silindirler + köşe küreleri"""
    V = cq.Vector; ss = []
    for a, b in zip(pts[:-1], pts[1:]):
        v = V(*b) - V(*a)
        if v.Length > 1e-6: ss.append(cq.Solid.makeCylinder(r, v.Length, V(*a), v.normalized()))
    for p in pts[1:-1]: ss.append(cq.Solid.makeSphere(r, V(*p), angleDegrees1=-90, angleDegrees2=90))
    return cq.Compound.makeCompound(ss)


def kutu_profil_x(x0, x1, y0, y1, z0, z1, t=2.0):
    return kut(x0, x1, y0, y1, z0, z1).cut(kut(x0 - 1.0, x1 + 1.0, y0 + t, y1 - t, z0 + t, z1 - t))


def kutu_profil_y(x0, x1, y0, y1, z0, z1, t=2.0):
    return kut(x0, x1, y0, y1, z0, z1).cut(kut(x0 + t, x1 - t, y0 - 1.0, y1 + 1.0, z0 + t, z1 - t))


def kutu_profil_z(x0, x1, y0, y1, z0, z1, t=2.0):
    return kut(x0, x1, y0, y1, z0, z1).cut(kut(x0 + t, x1 - t, y0 + t, y1 - t, z0 - 1.0, z1 + 1.0))


def ac(sh, aci):
    """kapak parçası: alt ön kenar ekseninde (x boyunca) aci° (üst kenar öne)"""
    return sh.rotate(cq.Vector(0.0, PIVOT[0], PIVOT[1]), cq.Vector(1.0, PIVOT[0], PIVOT[1]), aci)


def kapak_nokta(s, t, aci):
    """kapağa bağlı nokta (s: pivottan kapak boyunca yukarı · t: ön yüze dik, − = arkaya) → dünya (y, z) · aci° açıkken"""
    th = math.radians(aci); c, si = math.cos(th), math.sin(th)
    return (PIVOT[0] + s * c - t * si, PIVOT[1] + s * si + t * c)


# ================================================================ ÇEKME GAZLI YAY (kinematik + katı) ================================================================
def yay_uclari(aci):
    """A (sabit göz, yan saçta) · B (kapak gözü) · boy L (göz merkezleri, mm)"""
    A = YAY["A"]; B = kapak_nokta(YAY["sB"], YAY["tB"], aci)
    return A, B, math.hypot(B[0] - A[0], B[1] - A[1])


def yay_kuvveti(L):
    """çekme kuvveti (N): kısa boyda F1, strok sonunda F1 · prog (doğrusal, VARSAYIM)"""
    return YAY["F1"] * (1.0 + (YAY["prog"] - 1.0) * (L - YAY["Lr"]) / YAY["S"])


def yay_momenti(aci):
    """(kapatıcı moment N·m, kol mm, L mm, F N) — yay B'yi A'ya çeker"""
    A, B, L = yay_uclari(aci)
    uy, uz = (A[0] - B[0]) / L, (A[1] - B[1]) / L
    ry, rz = B[0] - PIVOT[0], B[1] - PIVOT[1]
    kol = -(uy * (-rz) + uz * ry)                  # + kapatır
    F = yay_kuvveti(L)
    return F * kol / 1000.0, kol, L, F


def yay_konum(k, aci):
    """k = 0 sol / 1 sağ kanat yayı · aci° kapak açısında: [(ad, shape)] (gövde, mil, 2 göz) — montaj animasyonu için"""
    tag = ("sol", "sag")[k]; xc = YAY_XC[k]
    A, B, L = yay_uclari(aci)
    V = cq.Vector
    a3, b3 = V(xc, A[0], A[1]), V(xc, B[0], B[1])
    u = (b3 - a3).normalized()
    T = YAY["Lr"] - 2.0 * YAY["BOYUN"] - YAY["BOS"]  # gövde boyu (VARSAYIM: çekme yayı kısa boyda mil gövdenin içinde, 8 mm görünür)
    g0 = a3 + u * YAY["BOYUN"]; g1 = a3 + u * (YAY["BOYUN"] + T)
    m1 = b3 - u * YAY["BOYUN"]
    govde = cq.Solid.makeCylinder(YAY["D_GOVDE"] / 2.0, T, g0, u)
    mil = cq.Solid.makeCylinder(YAY["D_MIL"] / 2.0, (m1 - g1).Length, g1, u)
    out = [("onyuz_f_ust_gazli_yay_%s_govde" % tag, govde), ("onyuz_f_ust_gazli_yay_%s_mil" % tag, mil)]
    for uc, merk, yon in (("a", a3, u), ("b", b3, -u)):
        goz = cq.Solid.makeCylinder(YAY["R_GOZ"], YAY["T_GOZ"], merk - V(YAY["T_GOZ"] / 2.0, 0, 0), V(1, 0, 0))
        goz = goz.cut(cq.Solid.makeCylinder(YAY["D_PIM"] / 2.0, YAY["T_GOZ"] + 2.0, merk - V(YAY["T_GOZ"] / 2.0 + 1.0, 0, 0), V(1, 0, 0)))
        boyun = cq.Solid.makeCylinder(4.0, YAY["BOYUN"] - 4.0, merk + yon * 4.0, yon)
        out.append(("onyuz_f_ust_gazli_yay_%s_goz_%s" % (tag, uc), goz.fuse(boyun).clean()))
    return out


def flans_kertigi():
    """yay gövdesinin (Ø15) z = 57,5…59 (yan sac ön bükümü) düzlemlerinde kapladığı y aralığı 0°–90°: eksen kesişimi ± r · L / |Δz| (eğik silindirin izi) + 4 pay"""
    ys = []
    for d in range(0, 91):
        A, B, L = yay_uclari(float(d))
        dz = B[1] - A[1]
        if abs(dz) < 1e-9: continue
        yar = YAY["D_GOVDE"] / 2.0 * L / abs(dz) + 4.0
        for zp in (Z_TAVA - SAC, Z_TAVA):
            if (A[1] - zp) * (B[1] - zp) <= 0:
                t = (zp - A[1]) / dz; yc = A[0] + t * (B[0] - A[0]); ys += [yc - yar, yc + yar]
    return (min(ys), max(ys))


# ================================================================ 1 · GÖVDE ================================================================
def govde():
    B = "F_UST_KABIN"
    kert = flans_kertigi()
    for k, (tag, xs) in enumerate((("sol", X0), ("sag", X1 - SAC))):
        xa, xb = xs, xs + SAC
        w = kut(xa, xb, Y_GOV, Y_TAVAN, Z_ARKA_IC, Z_TAVA).union(kut(xa, xb, Y_TABAN, Y_GOV, Z_ARKA_IC, Z_FARKA)
                                                                .cut(kut(xa - 1.0, xb + 1.0, Y_GOV - FT.TEPE_BANDI, Y_GOV + 1.0, Z_FARKA - 1.0, Z_FARKA + 1.0)))   # fırın arka etiket bandı (1 mm) kertiği
        fa, fb = (X0 + SAC, X0 + SAC + FLANS) if tag == "sol" else (X1 - SAC - FLANS, X1 - SAC)
        on_b = kut(fa, fb, Y_GOV, Y_TAVAN, Z_TAVA - SAC, Z_TAVA).cut(kut(fa - 1.0, fb + 1.0, kert[0], kert[1], Z_TAVA - SAC - 1.0, Z_TAVA + 1.0))   # ön büküm · yay geçiş kertiği
        w = w.union(on_b)
        w = w.union(kut(fa, fb, Y_TABAN, Y_TAVAN, Z_ARKA_IC, Z_ARKA_IC + SAC))                    # arka büküm (arka saca vidalı)
        _dx, dy_, dz_ = DELIK[tag]
        w = w.cut(silx(dy_, dz_, R_DELIK, xa - 1.0, xb + 1.0))                                    # Ø16 hava hattı deliği
        xt = (fa + fb) / 2.0 - (0.5 if tag == "sol" else -0.5)                                    # bas-aç pistonu deliği (ön bükümde)
        w = w.cut(silz(xt, 1820.0, 5.0, Z_TAVA - SAC - 1.0, Z_TAVA + 1.0))
        ekle("f_ust_yan_%s" % tag, w, "sac", B, kaynak="SPEC_on_duzlem_v63 §2.4",
             bom=("Fırın üstü yan sac 304 fırçalı 1,5 (L: üst 555 × 888 + fırın arkasında şerit 517 × 178, 15 mm ön + arka büküm)", 2, "lazer + abkant",
                  "sol / sağ ayna · Ø16 hava hattı deliği (sol y 1809 z −432 · sağ y 1809 z −780) · bas-aç deliği Ø10 · ön bükümde yay geçiş kertiği y %.0f–%.0f" % kert, "ÜRETİM") if tag == "sol" else None)
        # EPDM geçme bileziği (Ø16 delik · iç Ø10 = hat: sıkı geçer, hattı taşır · iç yüzde Ø22 flanş)
        xf = (xb, xb + 1.0) if tag == "sol" else (xa - 1.0, xa)
        bz = silx(dy_, dz_, R_DELIK, xa, xb).union(silx(dy_, dz_, R_BILEZIK_FL, xf[0], xf[1])).cut(silx(dy_, dz_, R_BILEZIK_IC, xa - 2.0, xb + 2.0))
        ekle("f_ust_hava_gecme_bilezigi_%s" % tag, bz, "conta", B, kaynak="VARSAYIM (EPDM geçme bileziği Ø16 / iç Ø10)",
             bom=("Hava hattı geçme bileziği EPDM · delik Ø16 · iç Ø10 (hat Ø10 sıkı geçer)", 2, "katalog (hortum geçiş lastiği)",
                  "yan sac deliğine geçme · hat bileziğe oturur (0,5 mm boşluk kalktı) · rakor yerine: komşu yan sac bitişik, bulkhead somunu komşuya taşar", "SATIN ALMA") if tag == "sol" else None)
        # bas-aç (Blum TIP-ON 956.1004 · mıknatıslı): gövde yan saca braketli · piston ön bükümden kapaktaki karşı plakaya
        bx = (X0 + SAC, X0 + SAC + 14.0) if tag == "sol" else (X1 - SAC - 14.0, X1 - SAC)
        xp = (bx[0] + bx[1]) / 2.0
        ti = kut(bx[0], bx[1], 1810.0, 1830.0, 20.0, Z_TAVA - SAC).union(silz(xp, 1820.0, 4.0, Z_TAVA - SAC, Z_ON - SAC - 1.0))
        ekle("onyuz_f_ust_bas_ac_%s" % tag, ti, "koyu", "F_UST_KAPAK", kaynak="Blum TIP-ON 956.1004 (kısa, mıknatıslı; set: vidalı + yapışkan karşı plaka)",
             bom=("Bas-aç itici Blum TIP-ON 956.1004 (kısa · mıknatıs uçlu · karşı plakalı set)", 2, "katalog", "kanat dış üst köşesi (yan saca braketli) · karşı plakası kapakta · kulp yok · düşer kapakta kullanım üreticiyle doğrulanmalı", "SATIN ALMA") if tag == "sol" else None)
        # çekme gazlı yayın sabit braketi (yan sacın iç yüzü): 3 mm plaka Ø16 + Ø6 pim (gözü taşır)
        xpl = (X0 + SAC, X0 + SAC + 3.0) if tag == "sol" else (X1 - SAC - 3.0, X1 - SAC)
        xpe = (X0 + SAC + 3.0, YAY_XC[0] + YAY["T_GOZ"] / 2.0 + 1.5) if tag == "sol" else (YAY_XC[1] - YAY["T_GOZ"] / 2.0 - 1.5, X1 - SAC - 3.0)
        yA, zA = YAY["A"]
        br = silx(yA, zA, 8.0, xpl[0], xpl[1]).union(silx(yA, zA, YAY["D_PIM"] / 2.0, xpe[0], xpe[1]))
        ekle("onyuz_f_ust_gazli_yay_braketi_%s" % tag, br, "celik", B, kaynak="VARSAYIM (M6 omuzlu pim + 3 mm pul plaka, yan saca perçin somun)",
             bom=("Gazlı yay sabit bağlantısı: M6 omuzlu pim + Ø16 × 3 plaka", 2, "üretim / katalog", "yan sac iç yüzü (y %.0f · z %.0f) · tek kesme" % (yA, zA), "ÜRETİM") if tag == "sol" else None)
    # ---- üst sac (430): 3 kenarı 20 aşağı bükülü, ön kenar serbest · atış ağzı ----
    u = kut(X0, X1, Y_TAVAN, H_MAK, Z_ARKA_IC, Z_TAVA)
    u = u.union(kut(X0 + SAC, X0 + 2 * SAC, Y_TAVAN - 20.0, Y_TAVAN, Z_ARKA_IC + SAC, Z_TAVA - SAC))
    u = u.union(kut(X1 - 2 * SAC, X1 - SAC, Y_TAVAN - 20.0, Y_TAVAN, Z_ARKA_IC + SAC, Z_TAVA - SAC))
    u = u.union(kut(X0 + SAC + FLANS, X1 - SAC - FLANS, Y_TAVAN - 20.0, Y_TAVAN, Z_ARKA_IC, Z_ARKA_IC + SAC))
    u = u.cut(kut(ATIS[0] + SAC, ATIS[1] - SAC, Y_TAVAN - 1.0, H_MAK + 1.0, ATIS[2] + SAC, ATIS[3] - SAC))   # atış kanalının iç ölçüsü
    ekle("f_ust_tavan_sac", u, "sac", B, kaynak="SPEC §2.4 · 430",
         bom=("Fırın üstü üst sac 430 ferritik 1,5 · 1500 × 888 · sol / sağ / arka 20 büküm", 1, "lazer + abkant",
              "atış ağzı 300 × 200 · ön kenar: sol + sağ yan sac, kiriş dikmesi (3336–3366), 2. dikme (3560–3590) taşır; pizza üstünde 834,5 serbest (AÇIK: 320 kutu → 0,5 mm pay)", "ÜRETİM"))
    ekle("f_ust_tavan_kirisi", kutu_profil_z(KIRIS_X[0], KIRIS_X[1], Y_TAVAN - 30.0, Y_TAVAN, Z_ARKA_IC + SAC, Z_TAVA - 2.0), "paslanmaz", B,
         bom=("Tavan kirişi 304 kutu profil 30 × 30 × 2 · L 882", 1, "üretim", "üst sacı bölen enine kiriş (pizza yığınının 12 mm sağında) · arkada arka bükümde, önde dikmede", "ÜRETİM"))
    # ---- arka sac: tek parça 788–1862 · 2 panjur (8 içe bükük lamel) + 4 rakor deliği ----
    a = kut(X0, X1, Y_TABAN, H_MAK, Z_ARKA, Z_ARKA_IC)
    lamel = []
    for fx in PANJUR_X:
        for i in range(8):
            y0 = PANJUR_Y - 88.0 + i * 22.0
            a = a.cut(kut(fx - 85.0, fx + 85.0, y0, y0 + 12.0, Z_ARKA - 1.0, Z_ARKA_IC + 1.0))
            lamel.append((fx, y0))
    for ad_, rx, ry, rd, rn, _n in RAKOR:
        a = a.cut(silz(rx, ry, rd, Z_ARKA - 1.0, Z_ARKA_IC + 1.0))
    ekle("f_ust_arka_sac", a, "sac", B, kaynak="SPEC §2.4 (tek parça, rakorlu, panjurlu)",
         bom=("Fırın bölmesi arka sacı 304 1,5 · TEK PARÇA 1500 × 1074 (788–1862)", 1, "lazer + panjur kalıbı",
              "yan sacların arka bükümlerine + üst sacın arka bükümüne vidalı (sökülür servis) · 2 panjur 170 × 176 (fırın teknik bölme fanları) · 4 rakor deliği", "ÜRETİM"))
    for j, fx in enumerate(PANJUR_X):
        w = None
        for fx_, y0 in lamel:
            if fx_ != fx: continue
            l_ = kut(fx - 85.0, fx + 85.0, y0 + 12.0, y0 + 12.0 + SAC, Z_ARKA_IC, Z_ARKA_IC + 12.0)
            w = l_ if w is None else w.union(l_)
        ekle("f_ust_panjur_lamelleri_%d" % j, w, "sac", B, kaynak="arka sacla tek parça (panjur kalıbı) · ayrı çizildi",
             bom=("Panjur lamelleri (arka sacla tek parça, 12 mm içe bükük) · 8 × 170", 2, "panjur kalıbı", "fırın teknik bölme fanı havası dışarı (önden görünmez)", "ÜRETİM") if j == 0 else None)
    for ad_, rx, ry, rd, rn, not_ in RAKOR:
        ekle("f_ust_rakor_%s" % ad_, silz(rx, ry, rd - 0.5, Z_ARKA, Z_ARKA + 18.0).union(silz(rx, ry, rn, Z_ARKA_IC, Z_ARKA_IC + 6.5)), "plastik", B,
             kaynak="VARSAYIM (poliamid kablo rakoru IP68)", bom=("Kablo rakoru poliamid IP68 · %s" % not_.split(" · ")[0], 1, "katalog", not_, "SATIN ALMA"))
    # ---- ön kayıt 30 × 30 × 2 (menteşe sabit yaprakları) + 3 takoz (fırın üstüne) + 2 dikme (üst sacın ön kenarı) ----
    ekle("onyuz_f_ust_kayit", kutu_profil_x(*KAYIT), "paslanmaz", B,
         bom=("Ön kayıt 304 kutu profil 30 × 30 × 2 · L 1497", 1, "üretim", "yan saclara kaynaklı · 4 menteşe sabit yaprağı + 2 dikme taşır · 3 takozla fırın üstüne basar", "ÜRETİM"))
    for i, xt in enumerate(KAYIT_TAKOZ_X):
        ekle("onyuz_f_ust_kayit_takozu_%d" % i, kut(xt - 20.0, xt + 20.0, Y_GOV, KAYIT[2], KAYIT[4], KAYIT[5]), "paslanmaz", B,
             bom=("Kayıt takozu 304 · 40 × 30 × 3", 3, "lazer", "kayıt → fırın üst sacı (açık kapak rafı yükü)", "ÜRETİM") if i == 0 else None)
    for j, (xa, xb) in enumerate(DIKME_X):
        yb = Y_TAVAN - 30.0 if j == 0 else Y_TAVAN                                               # 0: kirişin altına · 1: üst saca
        ekle("onyuz_f_ust_dikme_%d" % j, kutu_profil_y(xa, xb, KAYIT[3], yb, KAYIT[4], KAYIT[5]), "paslanmaz", B,
             bom=("Ön dikme 304 kutu profil 30 × 30 × 2", 2, "üretim", "kayıt üstü → %s (üst sacın ön kenarını taşır) · pizza (≤ 3324) ile kompresör (≥ 3600) arasında" % ("tavan kirişi" if j == 0 else "üst sac"), "ÜRETİM") if j == 0 else None)


# ================================================================ 2 · ÖN KAPAKLAR ================================================================
def kapaklar():
    B = "F_UST_KAPAK"
    for k, (a, b) in enumerate(KANAT_X):
        tag = ("sol", "sag")[k]; g = "KAPAK_F_%s" % tag.upper()
        a0, b0 = KANAT_X[0]                                                                        # sol kanat ölçüsü → sağda ayna (yay dış kenarda)
        p = kut(a, b, KAPAK_Y[0], KAPAK_Y[1], Z_TAVA, Z_ON).cut(kut(a + SAC, b - SAC, KAPAK_Y[0] + SAC, KAPAK_Y[1] - SAC, Z_TAVA - 1.0, Z_ON - SAC))
        for sira in YARIK_SIRA:
            for yr in sira:
                for i in range(YARIK_N):
                    xc = a + YARIK_X0 + i * YARIK_ADIM
                    p = p.cut(kut(xc, xc + YARIK_W, yr, yr + YARIK_H, Z_ON - SAC - 0.5, Z_ON + 0.5))
        ekle("onyuz_f_ust_kapak_%s" % tag, p, "sac", B, grup=g, kaynak="SPEC §2.4 tava 20",
             bom=("Fırın üstü kapak kanadı · tava 20 · 304 fırçalı 1,5 · %.1f × %.0f" % (b - a, KAPAK_Y[1] - KAPAK_Y[0]), 2, "lazer + abkant (4 kenar 20 arkaya)",
                  "alttan menteşeli düşer kapak · alt (1405–1434) + üst (1810–1839) bantta 3 × 6 lazer yarık 90 × 5 · kulp / vida / menteşe önden görünmez", "ÜRETİM") if k == 0 else None)
        for j, xo in enumerate((a + 250.0, b - 250.0)):                                          # omega 1,0 (panel > 600): flanş 40, gövde 18 × 15
            om = kut(xo - 20.0, xo + 20.0, OMEGA_Y[0], OMEGA_Y[1], Z_ON - SAC - SAC_IC, Z_ON - SAC)
            for xw in (xo - 9.0, xo + 8.0):
                om = om.union(kut(xw, xw + SAC_IC, OMEGA_Y[0], OMEGA_Y[1], Z_ON - SAC - 15.0, Z_ON - SAC - SAC_IC))
            om = om.union(kut(xo - 9.0, xo + 9.0, OMEGA_Y[0], OMEGA_Y[1], Z_ON - SAC - 15.0, Z_ON - SAC - 15.0 + SAC_IC))
            ekle("onyuz_f_ust_kapak_%s_omega_%d" % (tag, j), om, "paslanmaz", B, grup=g,
                 bom=("Kapak omega takviyesi 304 1,0 · 40 × 15 · L 350", 4, "abkant", "kapak iç yüzüne punta (panel > 600)", "ÜRETİM") if k == 0 and j == 0 else None)
        # burulma kutusu: 1,0 C profil (alt ayak alt dönüşe, üst ayak 1395, sırt z 60,5) + dış uç plakası · kutunun iç ucu iç yan dönüşe değer
        kx = ayna(a0 + SERIT + SAC, b0 - SAC, k)                                                    # sol: 2518,5–3247
        ky, kz = KUTU_Y, KUTU_Z
        kt = kut(kx[0], kx[1], ky[0], ky[0] + SAC_IC, kz[0], kz[1]).union(kut(kx[0], kx[1], ky[1] - SAC_IC, ky[1], kz[0], kz[1])) \
            .union(kut(kx[0], kx[1], ky[0], ky[1], kz[0], kz[0] + SAC_IC))
        ux = ayna(a0 + SERIT + SAC, a0 + SERIT + SAC + SAC_IC, k)                                   # dış uç plakası (yay pimi burada)
        kt = kt.union(kut(ux[0], ux[1], ky[0], ky[1], kz[0], kz[1]))
        ekle("onyuz_f_ust_kapak_%s_burulma_kutusu" % tag, kt, "paslanmaz", B, grup=g, kaynak="denetçi #1–#2 (tek uçtan yay → burulma)",
             bom=("Kapak burulma kutusu 304 1,0 · C 85,5 × 17 · L 728 + uç plakası", 2, "abkant + punta", "kapak içinde alt bantta · yay pimi uç plakasında (çift kesme) · menteşe hareketli yaprakları sırtında", "ÜRETİM") if k == 0 else None)
        # yay pimi (kapak tarafı): dış yan dönüş ↔ kutu uç plakası, Ø6 çift kesme
        yB, zB = kapak_nokta(YAY["sB"], YAY["tB"], 0.0)
        px = ayna(a0 + SAC, a0 + SERIT + SAC, k)
        ekle("onyuz_f_ust_kapak_%s_yay_pimi" % tag, silx(yB, zB, YAY["D_PIM"] / 2.0, px[0], px[1]), "celik", B, grup=g, kaynak="VARSAYIM Ø6 omuzlu pim",
             bom=("Gazlı yay kapak pimi Ø6 · çift kesme (yan dönüş + kutu uç plakası)", 2, "katalog", "y %.0f · z %.0f (pivottan s %.0f · t %.0f)" % (yB, zB, YAY["sB"], YAY["tB"]), "SATIN ALMA") if k == 0 else None)
        # TIP-ON karşı plakası (setin vidalı çelik plakası): kapak iç yüzü, pistonun karşısı
        xp = (X0 + SAC + 8.5) if k == 0 else (X1 - SAC - 8.5)                                    # plaka 2502–2518 (tava içi; piston 2504,5–2512,5)
        ekle("onyuz_f_ust_kapak_%s_tipon_plakasi" % tag, kut(xp - 8.0, xp + 8.0, 1810.0, 1830.0, Z_ON - SAC - 1.0, Z_ON - SAC), "celik", B, grup=g,
             kaynak="Blum 956.1004 setindeki vidalı karşı plaka (ölçü VARSAYIM 16 × 20 × 1)",
             bom=("TIP-ON karşı plakası (956.1004 setinde) · çelik", 2, "katalog", "kapak iç yüzüne perçin · TIP-ON mıknatısı tutar (304 kapak manyetik değil)", "SET İÇİNDE") if k == 0 else None)
        # düşer kapak menteşesi (2 / kanat): sabit yaprak kayıt önünde (z 57–59) · hareketli yaprak kutu sırtında (z 59–60,5) — iç bağlantı (sanal pivot) şematik
        for j, xh in enumerate((a + MENTESE_DX, b - MENTESE_DX)):
            ekle("onyuz_f_ust_mentese_sabit_%s_%d" % (tag, j), kut(xh - 19.0, xh + 19.0, 1310.5, 1336.5, KAYIT[5], Z_TAVA), "celik", B,
                 kaynak="Sugatsune SDH-001 (düşer kapak menteşesi · 90° · açıkken yüzey hizası) — sabit yaprak + sac adaptör VARSAYIM",
                 bom=("Düşer kapak menteşesi Sugatsune SDH-001 + sac adaptör plakası", 4, "katalog (sugatsune.com drop hinge)",
                      "sanal pivot kapağın alt ön kenarında (y 1308, z +79) · 90° durdurma menteşede (VARSAYIM) · kanat başına 2 · kapasite üreticiyle doğrulanmalı (AÇIK)", "SATIN ALMA") if k == 0 and j == 0 else None)
            ekle("onyuz_f_ust_mentese_hareketli_%s_%d" % (tag, j), kut(xh - 19.0, xh + 19.0, 1310.5, 1336.5, Z_TAVA, KUTU_Z[0]), "celik", B, grup=g,
                 kaynak="Sugatsune SDH-001 hareketli yaprak (şematik)")


def yaylar():
    for k in (0, 1):
        for ad, sh in yay_konum(k, 0.0):
            bom = None
            if k == 0 and ad.endswith("_govde"):
                bom = ("Çekme tipi gazlı yay Bansbach easylift gas traction spring 6/15 · kısa boy %.0f · strok %.0f · F1 %.0f N (siparişe göre)" % (YAY["Lr"], YAY["S"], YAY["F1"]), 2,
                       "katalog (bansbach.com gas traction springs · 6/15 ek boy)", "kanat başına 1, dış yan şeritte · kapak açıldıkça uzar, geri çeker · mil aşağı · ölçü VARSAYIM", "SATIN ALMA")
            ekle(ad, cq.Workplane(obj=sh), "koyu" if "govde" in ad else "celik", "F_UST_KAPAK", grup=YAY_GRUP[k], kaynak="Bansbach easylift 6/15 çekme gazlı yay (VARSAYIM ölçü)", bom=bom)


# ================================================================ 3 · DAVLUMBAZ SAC KUTUSU ================================================================
def davlumbaz():
    B = "F_DAVLUMBAZ"
    x0, x1, y0, y1, z0, z1 = DAV
    w = kut(x0, x1, y0, y1, z0, z1).cut(kut(x0 + SAC, x1 - SAC, y0 + SAC, y1 - SAC, z0 + SAC, z1 - SAC))
    w = w.cut(kut(ATIS[0] + SAC, ATIS[1] - SAC, y1 - SAC - 1.0, y1 + 1.0, ATIS[2] + SAC, ATIS[3] - SAC))   # atış ağzı (üst) = kanal iç ölçüsü
    for yr in (1520.0, 1620.0, 1720.0):                                                             # emiş yarıkları: kompresörün arkasında
        for xa in (3390.0, 3590.0, 3790.0):
            w = w.cut(kut(xa, xa + 160.0, yr, yr + 10.0, z1 - SAC - 1.0, z1 + 1.0))
    ekle("f_davlumbaz_kutusu", w, "sac", B, kaynak="SPEC §2.4 basit sac kutu · üst 1790 KARAR (hava hattı K dalı)",
         bom=("Davlumbaz sac kutusu 304 1,5 · 1497 × 475 × 387", 1, "lazer + abkant + kaynak",
              "yan saclara köşebentle asılı · ön yüzde 9 emiş yarığı 160 × 10 (kompresör arkası) · üstte atış ağzı 300 × 200 · fan + yağ / karbon filtre içinde (AÇIK)", "ÜRETİM"))
    ekle("f_davlumbaz_atis_kanali", kut(ATIS[0], ATIS[1], y1, Y_TAVAN, ATIS[2], ATIS[3]).cut(kut(ATIS[0] + SAC, ATIS[1] - SAC, y1 - 1.0, Y_TAVAN + 1.0, ATIS[2] + SAC, ATIS[3] - SAC)),
         "sac", B, bom=("Atış kanalı 304 1,5 · 300 × 200 × 70", 1, "abkant + kaynak", "davlumbaz kutusu → üst sac atış ağzı", "ÜRETİM"))
    for tag, (xa, xb, xv) in (("sol", (X0 + SAC, X0 + SAC + 40.0, X0 + SAC + 3.0)), ("sag", (X1 - SAC - 40.0, X1 - SAC, X1 - SAC - 3.0))):
        kb = kut(xa, xb, y0 - 3.0, y0, -826.0, Z_FARKA - 3.0)
        kb = kb.union(kut(min(xv, xa if tag == "sol" else xb), max(xv, xa if tag == "sol" else xb), y0 - 40.0, y0, -826.0, Z_FARKA - 3.0))
        ekle("f_davlumbaz_askisi_%s" % tag, kb, "paslanmaz", B,
             bom=("Davlumbaz askı köşebendi 304 L 40 × 40 × 3 · L 172", 2, "üretim", "fırının arkasında (z −826…−654) yan saca vidalı, kutu tabanı üstüne oturur", "ÜRETİM") if tag == "sol" else None)


# ================================================================ 4 · KOMPRESÖR TAVASI + AYAKLAR ================================================================
def kompresor_ayaklari():
    B = "F_KOMP_AYAK"
    (x0, x1), (z0, z1), (y0, y1) = TAVA_K["x"], TAVA_K["z"], TAVA_K["y"]
    d, fl, yu = TAVA_K["duvar"], TAVA_K["flans"], TAVA_K["ust"]
    t = kut(x0, x1, y0, y1, z0, z1)                                                                # taban 4 mm
    for w in (kut(x0, x0 + d, y1, yu - 3.0, z0, z1), kut(x1 - d, x1, y1, yu - 3.0, z0, z1),         # duvarlar (raf altına 3 mm kalana kadar)
              kut(x0, x1, y1, yu - 3.0, z0, z0 + d), kut(x0, x1, y1, yu - 3.0, z1 - d, z1)):
        t = t.union(w)
    for w in (kut(x0 - fl, x0 + d, yu - 3.0, yu, z0 - fl, z1 + fl),                                 # flanşlar raf altına (sol · arka · ön; sağ uç rafın ucu)
              kut(x0 - fl, x1, yu - 3.0, yu, z0 - fl, z0 + d), kut(x0 - fl, x1, yu - 3.0, yu, z1 - d, z1 + fl)):
        t = t.union(w)
    ekle("f_komp_tavasi", t, "paslanmaz", B, kaynak="KARAR (denetçi #4): tank raftan ayrılsın, üreticinin ayakları çalışsın · kompresör yeri değişmez",
         bom=("Kompresör tavası 304 · taban 4 mm 391 × 306 + 2 mm duvar + 12 mm flanş", 1, "lazer + abkant + kaynak",
              "fırın rafının açıklığına (x 3595–3991 · z −385…−75) alttan flanşla vidalı · taban y 1324–1328 (kalkan 1315,8'e 8 mm) · 25 kg", "ÜRETİM"))
    tank = silx(TANK["yc"], TANK["zc"], TANK["r"], TANK["x"][0] - 10.0, TANK["x"][1] + 10.0)
    i = 0
    for xa in AYAK_X:
        for za in AYAK_Z:
            ekle("f_komp_titresim_takozu_%d" % i, sily(xa, za, 20.0, y1, y1 + 20.0), "koyu", B, kaynak="JUN-AIR OF302-15B titreşim takozu (üreticinin; Ø40 × 20 VARSAYIM)",
                 bom=("Kompresör titreşim takozu (üreticinin ayağıyla gelir) · Ø40 × 20 · M8", 4, "kompresörle birlikte", "tavaya M8 · föy ölçüsü VARSAYIM", "SET İÇİNDE") if i == 0 else None)
            ekle("f_komp_urun_ayagi_%d" % i, kut(xa - 20.0, xa + 20.0, y1 + 20.0, y1 + 92.0, za - 15.0, za + 15.0).cut(tank), "celik", B,
                 kaynak="JUN-AIR OF302-15B tank ayağı (ÜRETİCİNİN — tankla birlikte gelir; biz tanka kaynak YAPMAYIZ · ölçü VARSAYIM)",
                 bom=("Kompresör tank ayağı (JUN-AIR OF302-15B'nin kendi ayağı)", 4, "kompresörle birlikte", "CE/PED tankına üretici dışında kaynak yok · föy ölçüsü VARSAYIM", "SET İÇİNDE") if i == 0 else None)
            i += 1


def kur():
    PARCALAR[:] = []
    govde(); kapaklar(); yaylar(); davlumbaz(); kompresor_ayaklari()
    return PARCALAR


# ================================================================ 5 · DENETİM ================================================================
def _bbk(A, B, pay=0.01):
    return A.xmin < B.xmax - pay and B.xmin < A.xmax - pay and A.ymin < B.ymax - pay and B.ymin < A.ymax - pay and A.zmin < B.zmax - pay and B.zmin < A.zmax - pay


def capraz(S, T, esik=1.0, haric=()):
    """S, T: [(ad, shape)] · gerçek katı kesişimi > eşik · haric: (a_öneki, c_öneki) çiftleri (bağlantı: aynı menteşe / pim–göz)"""
    S = [(a, s, s.BoundingBox()) for a, s in S]; T = [(a, s, s.BoundingBox()) for a, s in T]
    out = []
    for a, sa, A in S:
        for c, sc, B in T:
            if a == c or not _bbk(A, B): continue
            if any((a.startswith(h1) and c.startswith(h2)) or (a.startswith(h2) and c.startswith(h1)) for h1, h2 in haric): continue
            try: v = sa.intersect(sc).Volume()
            except Exception: v = -1.0
            if v > esik or v < 0: out.append((round(v, 1), a, c))
    return sorted(out, reverse=True)


def kendi_arasinda(ps):
    S = [(p["ad"], dunya(p)) for p in ps]
    out = []
    for i in range(len(S)):
        out += capraz([S[i]], S[i + 1:])
    return sorted(out, reverse=True)


_KP = []


def kompresor_parcalari():
    """TU (topping_uno_cad v14 varsa, yoksa v13) kompresör parçaları → dünya (DY + KOMP_KAY + X_BC; hat_montaj_v62 ile aynı) · bir kez yüklenir"""
    if _KP: return _KP[0]
    import importlib.util as ilu
    for v in (14, 13):
        yol = os.path.join(U, "topping_uno_cad_v%d.py" % v)
        if os.path.exists(yol): break
    sp = ilu.spec_from_file_location("TU_FUK", yol)
    TU = ilu.module_from_spec(sp); sp.loader.exec_module(TU)
    t = cq.Vector(X_BC + KOMP_KAY[0], DY + KOMP_KAY[1], KOMP_KAY[2])
    _KP.append(([(q["ad"], q["sh"].translate(t)) for q in TU.P if q["ad"].startswith("kompresor_")], os.path.basename(yol)))
    return _KP[0]


def _vana_bagli(KP):
    from OCP.BRepExtrema import BRepExtrema_DistShapeShape as _DSS
    vn = [s for a, s in KP if a == "kompresor_cikis_vanasi"]
    if not vn: return None, None
    d_ = min(_DSS(vn[0].wrapped, s.wrapped).Value() for a, s in KP if a != "kompresor_cikis_vanasi")
    return d_, d_ <= 0.05


def havada_denetimi(yaz=True, aci=0.0):
    """BİRLEŞİK havada denetimi: firin_tp10_cad_v8 + bu kabin (kapaklar + yaylar aci° konumda) + kompresör tank + motor (+ vana motora bağlıysa).
    Tek başına (denetim_temas_v1 CLI) kompresör ayakları / tavası fırın rafına (firin_tp10_cad_v8) oturduğu için görünür — raf o listede yok.
    Beyaz liste: YOK. İSTİSNA (yazılı): kompresör çıkış vanası TOPPING'in parçası — TU v13'te motordan 12 mm uzakta; v14'te motora bağlı → o zaman kendiliğinden dahil."""
    import denetim_temas_v1 as DT
    if not PARCALAR: kur()
    FT.kur(uyarla=True)
    F = [(p["birim"] + ":" + p["ad"], FT.dunya(p)) for p in FT.PARCALAR]
    KP, _tu = kompresor_parcalari()
    _d, _b = _vana_bagli(KP)
    kp = [(a, s) for a, s in KP if a != "kompresor_cikis_vanasi" or _b]
    K = []
    for p in PARCALAR:
        if p["grup"] in YAY_GRUP: continue
        s = dunya(p)
        K.append((p["ad"], ac(s, aci) if p["grup"].startswith("KAPAK_F_") and aci else s))
    for k in (0, 1):
        K += yay_konum(k, aci)
    r = DT.havada(F + K + kp)
    if yaz:
        DT.yaz(r, en_cok=60, baslik="HAVADA PARCA DENETIMI · firin_tp10_cad_v8 + firin_ust_kabin_cad_v1 (kapak %.0f°) + kompresör (%s)"
               % (aci, "tank + motor + vana" if _b else "tank + motor · vana TU'da havada → istisna"))
    return r


def kapak_kutlesi(k=0):
    """kanat (kapak grubu parçaları) kütlesi kg + ağırlık merkezi (s, t) pivota göre (kapalı)"""
    ps = [p for p in PARCALAR if p["grup"] == "KAPAK_F_%s" % ("SOL", "SAG")[k]]
    m = 0.0; my = 0.0; mz = 0.0
    for p in ps:
        s = dunya(p); v = s.Volume(); c = s.Center()
        m += v; my += v * c.y; mz += v * c.z
    return m * RO, (my / m - PIVOT[0], mz / m - PIVOT[1])


def denge_tablosu(k=0, adim=5):
    """[(açı, yerçekimi açıcı N·m, yay kapatıcı N·m, net açıcı, kol, L, F)]"""
    m, (s_cg, t_cg) = kapak_kutlesi(k)
    out = []
    for d in range(0, 91, adim):
        cy, cz = kapak_nokta(s_cg, t_cg, float(d))
        Mg = m * 9.81 * (cz - PIVOT[1]) / 1000.0
        Ms, kol, L, F = yay_momenti(float(d))
        out.append((d, Mg, Ms, Mg - Ms, kol, L, F))
    return out, m, (s_cg, t_cg)


DEN = []


def kontrol(ad, sart, deger=""):
    DEN.append((ad, bool(sart), deger)); print("  %-126s %s %s" % (ad, "GEÇTİ" if sart else "** KALDI **", deger))


if __name__ == "__main__":
    import denetim_temas_v1 as DT
    from OCP.BRepExtrema import BRepExtrema_DistShapeShape as _DSS
    def _mes(a, b):
        d_ = _DSS(a.wrapped, b.wrapped); return d_.Value() if d_.IsDone() else -1.0
    t0 = time.time(); ARG = sys.argv[1:]
    ps = kur()
    S = [(p["ad"], dunya(p)) for p in ps]
    gec = [a for a, s in S if not s.isValid()]
    print("FIRIN ÜSTÜ KABİN v1 (28 Eyl düzeltme) · %d parça (%s)" % (len(ps), " · ".join("%s %d" % (k, sum(1 for p in ps if p["birim"] == k)) for k, _a in BIRIMLER)))
    print("DENETİM (firin_ust_kabin_cad_v1)")
    kontrol("katılar geçerli", not gec, ", ".join(gec))
    kontrol("BIRIMLER ↔ parçalar (her birimin parçası var · BIRIM_MODUL tam)", all(any(p["birim"] == k for p in ps) for k, _a in BIRIMLER)
            and all(p["birim"] in BIRIM_MODUL for p in ps))
    _yasak = ("on_kapak", "kapak_contasi", "pu_", "bolme", "ray_", "mil_", "on_fitil", "on_cerceve_saci", "plint_on", "yan_dis_sac", "yan_on_donus", "arka_sac",
              "sol_sac", "sag_sac", "taban_kapisi", "ust_kapi", "kabin_", "f_arka_saci", "on_ust_kapak", "yalitim_tasyunu", "arka_dis_sac", "on_alt_sac")
    _ad_k = [p["ad"] for p in ps if p["ad"].startswith(_yasak) or p["mal"] in ("kabuk", "yalitim")]
    _ad_o = [p["ad"] for p in ps if ("_kapak_" in p["ad"] or p["birim"] == "F_UST_KAPAK" or p["ad"].startswith(("f_ust_mentese", "f_ust_amortisor", "f_ust_miknatis", "f_ust_bas_ac", "f_ust_alt_kayit", "f_ust_kayit")))
             and not p["ad"].startswith("onyuz_")]
    kontrol("ADLANDIRMA: gizlenen / düşürülen önek ve 'kabuk' / 'yalitim' YOK · kapak + ön çerçeve + donanım (kayıt, dikme, menteşe, yay, bas-aç) onyuz_ ile (denetçi #8)",
            not _ad_k and not _ad_o, str(_ad_k + _ad_o))
    kontrol("SİLİNENLER: HDS-10S amortisör, mıknatıslı tampon, kaynaklı eyer / raf takozu YOK (denetçi #1–#4)",
            not [p["ad"] for p in ps if any(x_ in p["ad"] for x_ in ("amortisor", "miknatis", "eyer", "komp_ayak_takozu"))])
    # ---- zarf + ön düzlem ----
    BB = {a: s.BoundingBox() for a, s in S}
    zx = (min(b.xmin for b in BB.values()), max(b.xmax for b in BB.values())); zy = (min(b.ymin for b in BB.values()), max(b.ymax for b in BB.values()))
    zz = (min(b.zmin for b in BB.values()), max(b.zmax for b in BB.values()))
    kontrol("ZARF: x %.1f–%.1f ⊂ 2500–4000 · y %.1f–%.1f ⊂ 788–1862 · z %.1f…%.1f ⊂ −830…+79" % (zx + zy + zz),
            zx[0] >= X0 - 0.01 and zx[1] <= X1 + 0.01 and zy[0] >= Y_TABAN - 0.01 and zy[1] <= H_MAK + 0.01 and zz[0] >= Z_ARKA - 0.01 and zz[1] <= Z_ON + 0.01)
    _on = [a for a in BB if a in ("onyuz_f_ust_kapak_sol", "onyuz_f_ust_kapak_sag")]
    kontrol("ÖN DÜZLEM: kapak dış yüzleri zmax = +79,0 (%s) · kapak arkası +59 (tava 20)" % ", ".join("%s %.2f/%.2f" % (a[-3:], BB[a].zmax, BB[a].zmin) for a in _on),
            len(_on) == 2 and all(abs(BB[a].zmax - Z_ON) < 0.01 and abs(BB[a].zmin - Z_TAVA) < 0.01 for a in _on))
    _gv = [a for a in BB if not a.startswith("onyuz_") and BB[a].zmax > Z_TAVA + 0.01]
    kontrol("GÖVDE sacları +59'da biter · +59'u geçen yalnız onyuz_ kapak / donanım", not _gv, str(_gv))
    kontrol("ARKA YÜZ: arka sac z %.1f…%.1f (−830 SABİT) · y %.1f–%.1f tek parça" % (BB["f_ust_arka_sac"].zmin, BB["f_ust_arka_sac"].zmax, BB["f_ust_arka_sac"].ymin, BB["f_ust_arka_sac"].ymax),
            abs(BB["f_ust_arka_sac"].zmin - Z_ARKA) < 0.01 and abs(BB["f_ust_arka_sac"].ymin - Y_TABAN) < 0.01 and abs(BB["f_ust_arka_sac"].ymax - H_MAK) < 0.01)
    ks, kg = BB["onyuz_f_ust_kapak_sol"], BB["onyuz_f_ust_kapak_sag"]
    kontrol("DERZLER 3 mm: fırın üstü %.0f → kapak altı %.0f · kapak üstü %.0f → makine üstü %.0f · kanat arası %.1f → %.1f · komşu: C önü 2497 → %.0f · %.0f → K önü 4003"
            % (Y_GOV, ks.ymin, ks.ymax, H_MAK, ks.xmax, kg.xmin, ks.xmin, kg.xmax),
            abs(ks.ymin - Y_GOV - DERZ) < 0.01 and abs(H_MAK - ks.ymax - DERZ) < 0.01 and abs(kg.xmin - ks.xmax - DERZ) < 0.01 and abs(ks.xmin - X0) < 0.01 and abs(kg.xmax - X1) < 0.01)
    kontrol("YAN SACLAR SPEC: sol x %.1f–%.1f · sağ x %.1f–%.1f · y %.1f–%.1f · z %.1f…%.1f · şerit fırın arka yüzüne (−651)"
            % (BB["f_ust_yan_sol"].xmin, X0 + SAC, X1 - SAC, BB["f_ust_yan_sag"].xmax, BB["f_ust_yan_sol"].ymin, BB["f_ust_yan_sol"].ymax, BB["f_ust_yan_sol"].zmin, BB["f_ust_yan_sol"].zmax),
            abs(BB["f_ust_yan_sol"].xmin - X0) < 0.01 and abs(BB["f_ust_yan_sag"].xmax - X1) < 0.01 and abs(BB["f_ust_yan_sol"].ymin - Y_TABAN) < 0.01
            and abs(BB["f_ust_yan_sol"].ymax - Y_TAVAN) < 0.01 and abs(BB["f_ust_yan_sol"].zmin - Z_ARKA_IC) < 0.01 and abs(BB["f_ust_yan_sol"].zmax - Z_TAVA) < 0.01)
    kontrol("ÜST SAC y %.1f–%.1f (SPEC 1860,5–1862)" % (BB["f_ust_tavan_sac"].ymax - SAC, BB["f_ust_tavan_sac"].ymax), abs(BB["f_ust_tavan_sac"].ymax - H_MAK) < 0.01)
    # ---- kendi arasında ----
    cak = kendi_arasinda(ps)
    for x_ in cak[:20]: print("   %10.1f mm3  %s  <->  %s" % x_)
    kontrol("KENDİ ARASINDA çakışma = 0 (%d parça, > 1 mm³)" % len(ps), not cak, "%d bulgu" % len(cak))
    # ---- fırın (firin_tp10_cad_v8) ----
    FT.kur(uyarla=True)
    F = [(p["birim"] + ":" + p["ad"], FT.dunya(p)) for p in FT.PARCALAR]
    FD = dict(F)
    c1 = capraz(S, F)
    for x_ in c1[:20]: print("   %10.1f mm3  %s  <->  %s" % x_)
    kontrol("ÜST KABİN ↔ FIRIN v8 (%d parça: gövde + raf (kompresör açıklıklı) + giriş bandı + ölü plaka) çakışma = 0" % len(F), not c1, "%d bulgu" % len(c1))
    # ---- pizza yığını + kompresör + hava hattı ----
    PZ = kut(*PIZZA).val()
    c2 = capraz(S, [("PIZZA_YEDEK_320", PZ)])
    kontrol("ÜST KABİN ↔ PİZZA YEDEĞİ 320 kutu (x %.0f–%.0f · y %.0f–%.0f · z %.0f…%.0f) çakışma = 0" % PIZZA, not c2, str(c2[:4]))
    _pay = Y_TAVAN - PIZZA[3]
    kontrol("PİZZA KURALI 320 kutu DEĞİŞMEDİ: yığın üstü %.1f · üst sac altı %.1f → pay %.1f mm (SPEC: 0,5 · sehimle sac yığına oturur → AÇIK)" % (PIZZA[3], Y_TAVAN, _pay), PIZZA_UST_KUTU == 320 and 0.0 <= _pay <= 0.51)
    KP, tu_ad = kompresor_parcalari()
    KPtm = [(a, s) for a, s in KP if a != "kompresor_cikis_vanasi"]
    kb_ = cq.Compound.makeCompound([s for _a, s in KPtm]).BoundingBox()
    kontrol("KOMPRESÖR (%s + KOMP_KAY): tank + motor zarfı x %.0f–%.0f · y %.0f–%.0f · z %.0f…%.0f = sabitler (KOMP_KAY DEĞİŞMEDİ)" % ((tu_ad,) + (kb_.xmin, kb_.xmax, kb_.ymin, kb_.ymax, kb_.zmin, kb_.zmax)),
            len(KPtm) >= 2 and all(abs(a_ - b_) < 0.5 for a_, b_ in zip((kb_.xmin, kb_.xmax, kb_.ymin, kb_.ymax, kb_.zmin, kb_.zmax), KOMP_ZARF)))
    kontrol("KOMPRESÖR GERÇEK ZARFI (föy 380 × 380 × 510): x %.0f–%.0f · y %.0f–%.0f · z %.0f…%.0f · ayak altı = tava üstü %.0f · üst %.0f ≥ model motor üstü %.0f"
            % (KOMP_GERCEK + (TAVA_K["y"][1], KOMP_GERCEK[3], kb_.ymax)),
            abs(KOMP_GERCEK[1] - KOMP_GERCEK[0] - 380.0) < 0.01 and abs(KOMP_GERCEK[3] - KOMP_GERCEK[2] - 510.0) < 0.01 and abs(KOMP_GERCEK[5] - KOMP_GERCEK[4] - 380.0) < 0.01
            and abs(KOMP_GERCEK[2] - TAVA_K["y"][1]) < 0.01 and KOMP_GERCEK[3] >= kb_.ymax - 0.01)
    c3 = capraz([(a, s) for a, s in S if not a.startswith(("f_komp_urun_ayagi_",))], KP)
    kontrol("ÜST KABİN ↔ KOMPRESÖR (tank + motor + vana) çakışma = 0 (üreticinin ayakları tanka oturur: bağlantı)", not c3, str(c3[:4]))
    _tr = _mes([s for a, s in KP if "tank" in a][0], FD["F_UST_RAF:ust_raf"])
    _tt = min(_mes([s for a, s in KP if "tank" in a][0], s) for a, s in S if a.startswith("f_komp_urun_ayagi_"))
    kontrol("TİTREŞİM YALITIMI: tank ↔ fırın rafı %.1f mm (≥ 3: rafa değmez) · tank ↔ ürün ayağı %.2f (oturur) · ayak → Ø40 × 20 takoz → tava → raf (denetçi #4)" % (_tr, _tt),
            _tr >= 3.0 and _tt <= 0.05)
    HV = [("HAVA_ANA", boru(ANA, HAVA_R)), ("HAVA_K_DALI", boru(K_DALI, HAVA_R))]
    c4 = capraz(S, HV)
    kontrol("ÜST KABİN ↔ HAVA HATTI Ø10 (ana + K dalı, hat_montaj_v62 yolu) çakışma = 0", not c4, str(c4[:4]))
    _dm = min(_mes(HV[i][1], s) for i in (0, 1) for a, s in S if a.startswith(("f_ust_yan_", "f_davlumbaz_", "f_ust_tavan", "f_ust_arka_sac", "f_ust_rakor_")))
    _bz = [min(_mes(HV[i][1], s) for i in (0, 1)) for a, s in S if a.startswith("f_ust_hava_gecme_bilezigi_")]
    kontrol("HAVA HATTI: saclara / kutuya en yakın %.1f mm (> 2,5) · bileziklere %s mm (= 0: hat bilezikte taşınır · denetçi #10)" % (_dm, "/".join("%.2f" % b_ for b_ in _bz)),
            _dm >= 2.5 and all(b_ <= 0.05 for b_ in _bz))
    for tag in ("sol", "sag"):
        x_, y_, z_ = DELIK[tag]
        ok_ = any(abs(p1[1] - y_) < 0.01 and abs(p1[2] - z_) < 0.01 and abs(p2[1] - y_) < 0.01 and abs(p2[2] - z_) < 0.01 and min(p1[0], p2[0]) < x_ < max(p1[0], p2[0])
                  for R_ in (ANA, K_DALI) for p1, p2 in zip(R_[:-1], R_[1:]))
        kontrol("RAKOR DELİĞİ %s (x %.0f · y %.0f · z %.0f) hattın ekseninde" % (tag, x_, y_, z_), ok_)
    _dv = BB["f_davlumbaz_kutusu"]
    kontrol("DAVLUMBAZ KUTUSU x %.1f–%.1f · y %.0f–%.0f · z %.1f…%.1f: hava hattının (y 1804–1814) altında, pizza (−424) / kompresör (−420 gerçek) arkasında"
            % (_dv.xmin, _dv.xmax, _dv.ymin, _dv.ymax, _dv.zmin, _dv.zmax), _dv.ymax <= 1809.0 - HAVA_R - 5.0 and _dv.zmax <= KOMP_GERCEK[4] - 10.0 and _dv.zmax <= PIZZA[4] - 10.0)
    # ---- kapak kütlesi + ÇEKME YAYI DENGESİ (denetçi #1 KRİTİK) ----
    tb, m_k, cg_k = denge_tablosu(0)
    tb1, m_k1, _cg1 = denge_tablosu(1)
    print("   KANAT: %.2f kg (sol) / %.2f kg (sağ) · ağırlık merkezi pivottan s %.1f · t %.1f mm · 90°'de yerçekimi %.1f N·m (Sugatsune formülü %.0f kgf·cm)"
          % (m_k, m_k1, cg_k[0], cg_k[1], tb[-1][1], (KAPAK_Y[1] - KAPAK_Y[0]) / 20.0 * m_k))
    print("   YAY DENGESİ (sol; sağ ayna) · açı: yerçekimi / yay / NET açıcı N·m · kol mm · L mm · F N")
    for d, Mg, Ms, net, kol, L, Fy in tb:
        print("     %3d°  %6.2f  %6.2f  %6.2f   kol %6.1f   L %6.1f   F %5.1f" % (d, Mg, Ms, net, kol, L, Fy))
    _net = [r[3] for r in tb if r[0] >= 10]
    kontrol("YAY DENGESİ 10°–90°: net açıcı %.2f…%.2f N·m ⊂ [0,1 ; 3,0] (hiçbir açıda geri kalkmaz / düşmez: yay yerçekiminin %%%.0f–%%%.0f'ini taşır; 90°'de yay %.1f / yerçekimi %.1f N·m)"
            % (min(_net), max(_net), 100.0 * min(r[2] / r[1] for r in tb if r[0] >= 10), 100.0 * max(r[2] / r[1] for r in tb if r[0] >= 10), tb[-1][2], tb[-1][1]),
            all(0.1 <= n <= 3.0 for n in _net))
    kontrol("YAY DENGESİ 0°: net %.2f N·m ≤ −0,2 (kapak kendiliğinden kapalı kalır) · TIP-ON'un yenmesi gereken moment %.2f N·m → üst köşede %.1f N" % (tb[0][3], -tb[0][3], -tb[0][3] / 0.512),
            tb[0][3] <= -0.2)
    _Ls = [r[5] for r in tb]
    kontrol("YAY BOYU: L %.1f → %.1f mm (0° → 90°) ⊂ kısa boy %.0f … %.0f (strok sonu − 3) · strok %.0f · kuvvet %.0f → %.0f N ⊂ 50–400 N" % (_Ls[0], _Ls[-1], YAY["Lr"], YAY["Lr"] + YAY["S"] - 3.0, YAY["S"], tb[0][6], tb[-1][6]),
            YAY["Lr"] - 0.01 <= min(_Ls) and max(_Ls) <= YAY["Lr"] + YAY["S"] - 3.0 and all(_Ls[i] < _Ls[i + 1] for i in range(len(_Ls) - 1)) and 50.0 <= tb[-1][6] <= 400.0)
    kontrol("YAY SAĞ KANAT (ayna): net 10°–90° %.2f…%.2f N·m · 0° %.2f" % (min(r[3] for r in tb1 if r[0] >= 10), max(r[3] for r in tb1 if r[0] >= 10), tb1[0][3]),
            all(0.1 <= r[3] <= 3.0 for r in tb1 if r[0] >= 10) and tb1[0][3] <= -0.2)
    # 90° menteşe durdurma yükü (raf yükü dahil) · burulma
    M_raf = RAF_YUKU * 9.81 * 0.2755
    M_stop = tb[-1][3] + M_raf
    print("   90° DURDURMA: kapak net %.2f + dolum rafı %.0f kg × 275,5 mm = %.1f → menteşe durdurmalarına %.1f N·m / kanat (%.1f N·m / menteşe) — SDH-001 kapasitesi üreticiyle doğrulanmalı (AÇIK)"
          % (tb[-1][3], RAF_YUKU, M_raf, M_stop, M_stop / 2.0))
    A_m = (KUTU_Y[1] - KUTU_Y[0] - SAC_IC) * (KUTU_Z[1] - KUTU_Z[0] - SAC_IC / 2.0)
    J_k = 4.0 * A_m ** 2 / ((KUTU_Y[1] - KUTU_Y[0]) / SAC_IC * 2.0 + (KUTU_Z[1] - KUTU_Z[0]) / SAC_IC + (KUTU_Z[1] - KUTU_Z[0]) / SAC)
    L_k = KANAT_X[0][1] - KANAT_X[0][0]
    tw = max(abs(r[2]) for r in tb) * 1000.0 * L_k / (2.0 * 77000.0 * J_k)
    kontrol("BURULMA KUTUSU: J %.0f mm⁴ · yay en çok %.1f N·m tek uçtan → iç kenarda %.2f° → üst iç köşe gecikmesi %.1f mm (≤ 3)"
            % (J_k, max(abs(r[2]) for r in tb), math.degrees(tw), tw * (KAPAK_Y[1] - KAPAK_Y[0])), tw * (KAPAK_Y[1] - KAPAK_Y[0]) <= 3.0)
    # ---- süpürme: kapak (panel + kutu + pim + menteşe hareketli yaprak + karşı plaka) + yay (her açıda yeniden) ↔ sabit (menteşe sabit yaprak dahil) + fırın ----
    G_KAP = [p for p in ps if p["grup"].startswith("KAPAK_F_")]
    SAB = [(p["ad"], dunya(p)) for p in ps if p["grup"] == "SABIT"]
    BAG = (("onyuz_f_ust_mentese_hareketli_sol_0", "onyuz_f_ust_mentese_sabit_sol_0"), ("onyuz_f_ust_mentese_hareketli_sol_1", "onyuz_f_ust_mentese_sabit_sol_1"),
           ("onyuz_f_ust_mentese_hareketli_sag_0", "onyuz_f_ust_mentese_sabit_sag_0"), ("onyuz_f_ust_mentese_hareketli_sag_1", "onyuz_f_ust_mentese_sabit_sag_1"),
           ("onyuz_f_ust_gazli_yay_sol_goz_a", "onyuz_f_ust_gazli_yay_braketi_sol"), ("onyuz_f_ust_gazli_yay_sag_goz_a", "onyuz_f_ust_gazli_yay_braketi_sag"),
           ("onyuz_f_ust_gazli_yay_sol_goz_b", "onyuz_f_ust_kapak_sol_yay_pimi"), ("onyuz_f_ust_gazli_yay_sag_goz_b", "onyuz_f_ust_kapak_sag_yay_pimi"))
    sup, sup_y = [], []
    for aci in (0.0, 5.0, 15.0, 30.0, 45.0, 60.0, 75.0, 90.0):
        KA = [(p["ad"], ac(dunya(p), aci) if aci else dunya(p)) for p in G_KAP]
        YA = yay_konum(0, aci) + yay_konum(1, aci)
        if aci: sup += [(v, a + "@%.0f" % aci, c) for v, a, c in capraz(KA, SAB + F, haric=BAG)]
        sup += [(v, a + "@%.0f" % aci, c) for v, a, c in capraz(YA, SAB + F + KA, haric=BAG)]
        sup_y += [(v, a + "@%.0f" % aci, c) for v, a, c in capraz(YA[:4], YA[4:], haric=BAG)]
    for x_ in sup[:10]: print("   %10.1f mm3  %s  <->  %s" % x_)
    kontrol("SÜPÜRME 0°–90° (8 konum): kapak + menteşe hareketli yaprak + yay (her açıda) ↔ sabit kabin (menteşe sabit yaprak, kayıt, dikme, bas-aç, yan sac kertiği dahil) + fırın = 0 · hariç yalnız bağlantı çiftleri (menteşe yaprakları, göz ↔ pim)",
            not sup and not sup_y, str((sup + sup_y)[:4]))
    # ---- servis yolları (kapaklar + yaylar 90°) ----
    ACIK = [(p["ad"] + "@90", ac(dunya(p), ACI_ACIK)) for p in G_KAP] + yay_konum(0, ACI_ACIK) + yay_konum(1, ACI_ACIK)
    FR = [(a, s) for a, s in F if not a.endswith(":ust_raf")]
    yol_pz = kut(PIZZA[0], PIZZA[1], PIZZA[2], PIZZA[3], PIZZA[4], 700.0).val()
    c5 = capraz([("PIZZA_YUKLEME_YOLU", yol_pz)], SAB + ACIK + FR)
    kontrol("PİZZA YÜKLEME YOLU (yığın izdüşümü z −424 → +700, kapaklar + yaylar 90°) ↔ kabin + fırın = 0 · gerçek yay gövdesi (Ø15) dahil (denetçi #2)", not c5, str(c5[:4]))
    yol_k = kut(KOMP_GERCEK[0], KOMP_GERCEK[1], KOMP_GERCEK[2] + KOMP_KALDIR, KOMP_GERCEK[3] + KOMP_KALDIR, KOMP_GERCEK[4], 700.0).val()
    c6 = capraz([("KOMPRESOR_CIKARMA_YOLU", yol_k)], [(a, s) for a, s in SAB if not a.startswith(("f_komp_urun_ayagi_", "f_komp_titresim_takozu_"))] + ACIK + FR)
    kontrol("KOMPRESÖR ÇIKARMA YOLU (GERÇEK 380 × 380 × 510, %.0f kaldırılmış: y %.0f–%.0f · z −420 → +700, kapaklar + yaylar açık) ↔ kabin + fırın = 0 (denetçi #2, #4)"
            % (KOMP_KALDIR, KOMP_GERCEK[2] + KOMP_KALDIR, KOMP_GERCEK[3] + KOMP_KALDIR), not c6, str(c6[:4]))
    # ---- üst sac sehimi (ön kenar serbest açıklıklar) ----
    E_, nu_ = 193e9, 0.29; D_ = E_ * (SAC / 1000.0) ** 3 / (12.0 * (1.0 - nu_ ** 2)); q_ = 7930.0 * 9.81 * SAC / 1000.0
    def _seh(Lmm): L_ = Lmm / 1000.0; return q_ * L_ ** 4 / (384.0 * D_) * 1000.0, 5.0 * q_ * L_ ** 4 / (384.0 * D_) * 1000.0
    _ac = [("pizza üstü (yan sac → kiriş)", KIRIS_X[0] - (X0 + 2 * SAC), PIZZA[3]), ("kiriş → 2. dikme", DIKME_X[1][0] - KIRIS_X[1], None),
           ("2. dikme → sağ yan (kompresör üstü)", X1 - 2 * SAC - DIKME_X[1][1], KOMP_GERCEK[3] + KOMP_KALDIR)]
    for ad_, L_, alt_ in _ac:
        wa, wb = _seh(L_)
        print("   BİLGİ · ÜST SAC ön kenarı %-36s serbest %5.0f mm · sehim ankastre %.2f / basit %.2f mm%s" % (ad_, L_, wa, wb,
              (" · altındaki %.0f'a pay %.1f − sehim → %.1f…%.1f mm" % (alt_, Y_TAVAN - alt_, Y_TAVAN - alt_ - wb, Y_TAVAN - alt_ - wa)) if alt_ else ""))
    _wk = _seh(_ac[2][1])[1]
    kontrol("KOMPRESÖR ÜSTÜ: kaldırılmış kompresör (%.0f) ↔ üst sac (%.1f) pay %.1f mm − basit sehim %.2f = %.1f mm > 0,5 (2. dikme sayesinde)"
            % (KOMP_GERCEK[3] + KOMP_KALDIR, Y_TAVAN, Y_TAVAN - KOMP_GERCEK[3] - KOMP_KALDIR, _wk, Y_TAVAN - KOMP_GERCEK[3] - KOMP_KALDIR - _wk),
            Y_TAVAN - KOMP_GERCEK[3] - KOMP_KALDIR - _wk > 0.5)
    # ---- havada parça: kapalı + 90° açık (kapaklar yayla asılı) ----
    hv = havada_denetimi()
    KP_d, KP_b = _vana_bagli(KP)
    kontrol("HAVADA PARÇA (kapalı) = 0 (fırın v8 %d + üst kabin %d + kompresör) · beyaz liste YOK · istisna: TU vanası %s" % (len(F), len(S),
            "YOK (vana motora bağlı)" if KP_b else "(TU'da motordan %.1f mm — TOPPING v14 bağlar)" % (KP_d or -1)), not hv["bilesen"], "%d bileşen" % len(hv["bilesen"]))
    hv9 = havada_denetimi(aci=ACI_ACIK)
    kontrol("HAVADA PARÇA (kapaklar 90° açık) = 0 · açık kapak yaya asılı (menteşe iç bağlantısı modelsiz: yay yolu yeterli)", not hv9["bilesen"], "%d bileşen" % len(hv9["bilesen"]))
    # ---- mühendislik bilgisi ----
    A_yar = 2 * len(YARIK_SIRA[0]) * YARIK_N * YARIK_W * YARIK_H
    print("   BİLGİ · HAVALANDIRMA: kapak yarıkları alt %.0f + üst %.0f mm² (serbest) · davlumbaz emiş yarıkları %.0f mm² · arka panjur 2 × %.0f mm² · doğal çekiş (h 0,41 m, ΔT 15 K) "
          "≈ %.0f m³/h → ≈ %.0f W taşır: fırın üst yüzü + kompresör için YETMEZ → davlumbaz fanı bölmeden emer (cebri, AÇIK: fan seçimi)"
          % (A_yar, A_yar, 9 * 1600.0, 8 * 170.0 * 12.0, 0.6 * math.sqrt(2.0 * 9.81 * 0.41 * 15.0 / 313.0) * A_yar / 1e6 * 3600.0,
             0.6 * math.sqrt(2.0 * 9.81 * 0.41 * 15.0 / 313.0) * A_yar / 1e6 * 1.2 * 1005.0 * 15.0))
    kutle = {k: sum(dunya(p).Volume() for p in ps if p["birim"] == k and p["mal"] in ("sac", "paslanmaz", "celik")) * RO for k, _a in BIRIMLER}
    print("   BİLGİ · KÜTLE (çelik parçalar): %s · toplam %.1f kg" % (" · ".join("%s %.1f kg" % (k, v) for k, v in kutle.items()), sum(kutle.values())))
    print("   BİLGİ · yan sac ön büküm yay kertiği y %.0f–%.0f" % flans_kertigi())
    kal = [d_ for d_ in DEN if not d_[1]]
    print("DENETIM (firin_ust_kabin_cad_v1): %d madde · %d KALDI · %.0f sn" % (len(DEN), len(kal), time.time() - t0))
    assert not kal, [d_[0] for d_ in kal]
    sys.stdout.flush(); os._exit(0)
