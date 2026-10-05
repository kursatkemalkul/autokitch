# -*- coding: utf-8 -*-
"""HAT VERSİYON 2 · B ÇEKMECELİ DOLAP ADAPTÖRÜ v1 (30 Eyl 2026 · Claude · YEREL) — store_cad_v14'ün v2 yerleşimi (montajda SC yerine girer).
YÖNTEM (v1'in denetlenmiş parçaları kullanılır, yeniden çizilmez · her modul()'da store_cad_v14.modul() baştan koşar):
  · DİLİM (h2_hesap_v1.B_DILIM, v1 dünya x 1992,5 … 2500): K3|K4 bölmesi B3 + K4 kolonunun tamamı dolaptan çıkar. Sol grup +507,5 (DXL) sağa,
    x ≥ 2500 (B4, K5, K6, şerit, taşıyıcı) YERİNDE. Dolap v2: x 507,5 … 4000 (W_B 3492,5). K3 (v1 1372,5–1992,5) → 1880–2500, sağı B4'e dayanır.
  · Sınıflar: K1–K3 çekmece parçaları (birim CEK_K1/K2/K3_*) BÜTÜN olarak +507,5 (önleri dilimi aşsa da kesilmez: K3 önü 1864–2516, K5 önüne derz 3) ·
    K5 / K6 / şerit / taşıyıcı yerinde · gövde parçaları dilim kuralıyla (tamamen solda → +507,5 · tamamen sağda → yerinde · dilimi aşan → sol parça
    +507,5 + sağ parça, birleşik · dilimin içinde → yalnız K4 içeriği olabilir, başka parça çıkarsa HATA).
  · K4'ÜN İŞİ TAŞINDI (h2_hesap_v1): Secop NLE8.8CN + buharlaştırma tavası + B panosu → E'nin altı (öbür ajan) · kaşar/sucuk deposu → TOPPING üst katı.
    Taşınacak parçalar v1 dünya koordinatında, DEĞİŞTİRİLMEDEN listelenir: SECOP_V1 · PANO_V1 · DEPO_V1 (düşer) · K4_YAPI_V1 (ara katman, K4 kablo kanalı,
    kademe sacı, B3 bölmesi — düşer) · GIDER_V1_KALKAN (v1 gider kılıf / kelepçe / çek valfleri — ana hatla değişti).
  · GİDER v2: iki evaporatör gideri (K2 arkası x 1807,5 · K5 arkası x 2790) TEK Ø20 ana hatta toplanır. Ana hat arkada yerde (z −738, eğim %1,1) sağa koşar,
    şeritte z −760'a döner, x 4000'de sağ dış sacdan çıkar: ARAYÜZ (4000 · 170 · −760) — K içinden E altındaki tavaya öbür ajan devam eder.
    Neden z −738 (plenum −790…−752 değil): her kolonun kablo kanalı (z −790…−765) ve motor braketleri (z −787…−751,5) yerde plenumu kapatıyor;
    ana hat bunların hemen önünden geçer (z aralığı: braket 3,5 · kablo kanalı 17 mm; ölçülen en yakın: K5 kayışı 4,1 · taban iç sacı 4,2 · motor braketi 5,4 mm)
    ve plenum hava geçişlerine (z ≤ −760) değmez.
  · K4'e ÖZGÜ, DİLİMİN DIŞINDA KALAN AYRINTILAR (bayraklı · False → saf dilim kuralı):
      PLINT_IZGARA_KALDIR : plintteki Secop emiş ızgarası (42 yarık, v1 x 1819,75–2707,75) — Secop B'de yok · saf dilim iki yarığı 124,5'lik tek yarığa birleştiriyordu
      B4_HAVA_KAPAT       : B4'teki 2 arka hava geçişi (y 480–570 · 590–635) K4 deposunu sağ bölgeye bağlıyordu; v2'de K3 (sol bölge) ↔ K5 (sağ bölge) arasında
                            kalırdı → v1'deki gibi sol bölgenin sağ duvarı (v1 B3) KAPALI
      KABLO_BAGLANTI      : v1'de üst kablo kanalı (703–728, K1→K4) ile fırın altı kanalı (643–668, K4→K6) K4 dikey kanalıyla bağlıydı (K4 ile çıktı) →
                            K3'ün arka sağ köşesine 40 × 60 dikey bağlantı (kablolar B4 kablo geçişinden K5–K6'ya iner) · E panosuna çıkış öbür ajanda
Dünya ölçüleri: x hat boyunca, y yukarı (zemin 0), z derinlik (ön +79 · arka −830).
SÖZLEŞME (montaj SC olarak kullanır): modul() → özet [(kod, tip, n, ust, acik_ust)] (store_cad_v14 ile aynı yapı) · PARCALAR (dünya, wp) · CEK · STROK · Y_PLINT ·
  RAMPA_SN · KAS_PD · W_B · RAY_ARA_ORAN · KLAPE_AC · H_B · Z_ON · (+ X0 / X1 / KOLON_X / KAPAK_X / BOLME_X / AYAK_XZ / GIDER / BIRIM_AD).
modul() İDEMPOTENT (her çağrı v1'den baştan kurar) · PARCALAR / SECOP_V1 / PANO_V1 / DEPO_V1 listelerinin kimliği korunur ([:] = …).
Çalıştır (öz denetim): python -u ob_calistir.py h2/h2_store_v1.py [hizli]"""
import math, os, re, sys, time

H2 = os.path.dirname(os.path.abspath(__file__)); U = os.path.dirname(H2)
for _p in (U, H2):
    if _p not in sys.path: sys.path.insert(0, _p)
import cadquery as cq
import h2_hesap_v1 as H
import store_cad_v14 as SC0

V = cq.Vector
EPS = 1e-6
# ---------------------------------------------------------------- v2 YERLEŞİM (h2_hesap_v1 tek sayı kaynağı)
DXL = H.DXL                                     # 507,5 · sol grubun sağa kayması
DILIM = H.B_DILIM                               # (1992,5 · 2500) v1 dünya x · dolaptan çıkan dilim
X0, X1 = H.B_X                                  # 507,5 · 4000 (v1 0 · 4000)
W_B = H.W_B                                     # 3492,5 (v1 4000)
assert abs(DILIM[1] - DILIM[0] - DXL) < 1e-9 and abs(X1 - X0 - W_B) < 1e-9 and abs(SC0.W_B - X1) < 1e-9
# bayraklar (üstteki açıklamaya bak)
PLINT_IZGARA_KALDIR = True
B4_HAVA_KAPAT = True
KABLO_BAGLANTI = True

# ---------------------------------------------------------------- v1 ile AYNI sabitler (y / z / hareket)
H_B, Y_PLINT, Z_ON, Z_ON0, Z_ON1 = SC0.H_B, SC0.Y_PLINT, SC0.Z_ON, SC0.Z_ON0, SC0.Z_ON1
STROK, KAS_PD, RAMPA_SN, RAY_ARA_ORAN = SC0.STROK, SC0.KAS_PD, SC0.RAMPA_SN, SC0.RAY_ARA_ORAN
KLAPE_AC, KLAPE_EKSEN, KLAPE_MAX = SC0.KLAPE_AC, SC0.KLAPE_EKSEN, SC0.KLAPE_MAX   # şerit sağ uçta · yerinde
Y_TABAN, Y_TAVAN, Y_TAVAN_F, Z_ARKA, Z_ARKA_DIS, DERINLIK = SC0.Y_TABAN, SC0.Y_TAVAN, SC0.Y_TAVAN_F, SC0.Z_ARKA, SC0.Z_ARKA_DIS, SC0.DERINLIK
Z_CER0, Z_CER1, FUGA, BOLME, WO = SC0.Z_CER0, SC0.Z_CER1, SC0.FUGA, SC0.BOLME, SC0.WO
HH_KOL, Y0_KOL, HH_C, KOLON_W, TAVAN_KOL = dict(SC0.HH_KOL), dict(SC0.Y0_KOL), dict(SC0.HH_C), dict(SC0.KOLON_W), dict(SC0.TAVAN_KOL)
KOLON_AD, KOLON = SC0.KOLON_AD, SC0.KOLON
ALT_KOD, UST_KOD = set(SC0.ALT_KOD), set(SC0.UST_KOD)
SERIT, X_F, TD_X, TD_Z = SC0.SERIT, SC0.X_F, SC0.TD_X, SC0.TD_Z   # x ≥ 2500 → yerinde

# ---------------------------------------------------------------- x taşıyan veriler (K1–K3 +507,5 · K4 yok · sağ taraf yerinde)
SOL_KOL = ("K1", "K2", "K3")


def _xv1(x):
    """v1 dünya x → v2 (sol grup +DXL · sağ grup yerinde · dilim içi None)"""
    if x <= DILIM[0] + EPS: return x + DXL
    if x >= DILIM[1] - EPS: return x
    return None


KOLON_X = {k: (v + DXL if k in SOL_KOL else v) for k, v in SC0.KOLON_X.items()}          # 570 · 1225 · 1880 · 2535 · 3190
KAPAK_X = {k: ((a + DXL, b + DXL) if k in SOL_KOL else (a, b)) for k, (a, b) in SC0.KAPAK_X.items() if k != "K4"}
BOLME_AD = {0: "B1", 1: "B2", 3: "B4", 4: "B5", 5: "B6"}                                  # sıra = parça adı (bolme_<i>_*) · B3 (i 2, K3 | K4) dilimle çıktı
BOLME_X = tuple(_xv1(x) if i != 2 else None for i, x in enumerate(SC0.BOLME_X))           # sol yüzler: 1190 · 1845 · None · 2500 · 3155 · 3775 (v1 sırası korunur)
CEK = [(kol, kod, tip, (x0 + DXL if kol in SOL_KOL else x0), yo) for kol, kod, tip, x0, yo in SC0.CEK]   # kodlar AYNI (CEK_K3_hamur_3 …)
AYAK_XZ = [(_xv1(x), z) for x, z in SC0.AYAK_XZ]                                         # sol grup ayakları +507,5 (2467,5 · 2530 yan yana — rapora bak)
EVAP = {y_: dict(e, gider=(_xv1(e["gider"][0]), _xv1(e["gider"][0]))) for y_, e in SC0.EVAP.items()}   # gider çıkışı: sol 1807,5 · sağ 2790

# ---------------------------------------------------------------- GİDER v2 · TEK Ø20 ANA HAT (dünya v2)
ARAYUZ_GIDER = (4000.0, 170.0, -760.0)          # B'nin sağ dış sacı (x 4000) · boru ekseni y 170 · z −760 → K içinden E altındaki tavaya (öbür ajan)
R_ANA, R_KILIF = 10.0, 12.0                     # Ø20 PVC ana hat · Ø24 kılıf (bölme geçişleri) · duvar geçiş lastiği
R_DAL = SC0.DR_R                                # 6 · v1 Ø12 evaporatör giderleri (dal) aynı boru
Z_ANA = -738.0                                  # ana hat ekseni: arka iç sacın (−790) 52 önü (yukarıdaki "Neden z −738")
EGIM = 0.011                                    # ana hat + dalların yatay kısımları · her koşu ≥ %1 (v1 DR_EGIM %1)
X_ANA0 = EVAP["sol"]["gider"][0] - 12.5         # 1795 · ana hattın kapalı başı (sol dal 12,5 sağında girer)
Y_ANA0 = 200.5                                  # başlangıç ekseni y: K5 / K6 kayış alt koşusu (206,3) ile K6 sonu taban (164,5) arasında ortalı
X_DON = (3840.0, 3862.0)                        # şeritte 45° dönüş z −738 → −760 (B6 3775–3810'dan sonra, şeridin arkası boş)
X_KELEPCE = {"K3": 2300.0, "K5": 2950.0, "K6": 3500.0}   # ana hat eyerleri (taban iç sacına) · motor / kablo kanalı / tepsi braketlerinden uzak


def y_ana(x):
    """ana hat ekseni y (x ≤ X_DON[0], z −738 koşusu)"""
    return Y_ANA0 - EGIM * (x - X_ANA0)


def _ana_noktalar():
    a1 = (X_DON[0], y_ana(X_DON[0]), Z_ANA)
    l_ = math.hypot(X_DON[1] - X_DON[0], ARAYUZ_GIDER[2] - Z_ANA)
    a2 = (X_DON[1], a1[1] - EGIM * l_, ARAYUZ_GIDER[2])
    return [(X_ANA0, Y_ANA0, Z_ANA), a1, a2, ARAYUZ_GIDER]


def _dal_noktalar(yan):
    """evaporatör tepsisinin dibinden (v1 çıkışı, z −690) aşağı → arkaya ana hattın eksenine (T girişi) · her koşu ≥ %1"""
    e = EVAP[yan]; gx = e["gider"][0]; ty = e["y"][0] - 15.0
    y2 = y_ana(gx); y1 = y2 + EGIM * abs(SC0.DR_Z - Z_ANA)
    return [(gx, ty, SC0.DR_Z), (gx, y1, SC0.DR_Z), (gx, y2, Z_ANA)]


GIDER = dict(ana=_ana_noktalar(), sol=_dal_noktalar("sol"), sag=_dal_noktalar("sag"), arayuz=ARAYUZ_GIDER, cap=2 * R_ANA, kilif_cap=2 * R_KILIF,
             z=Z_ANA, egim=EGIM, kelepce=dict(X_KELEPCE))
# bölme geçişleri (v2 dünya x): B2 · B4 · B5 · B6 — sol yüz BOLME_X, 35 kalın
GECIS_BOLME = {BOLME_AD[i]: (BOLME_X[i], BOLME_X[i] + BOLME) for i in (1, 3, 4, 5)}
X_YAN_DIS = (X1 - 1.5, X1)                      # sağ dış sac 3998,5–4000
KABLO_BAG_K = (BOLME_X[3] - 40.0, BOLME_X[3], SC0.KAN_UST_F[0], SC0.KAN_UST[0], SC0.KAN_Z[0], SC0.KAN_Z[1])   # 2460–2500 × 643–703 × −790…−765

# ---------------------------------------------------------------- SINIFLAR (v1 adları)
SECOP_GRUP = {   # SECOP_V1 alt grupları (öbür ajan için): v1 dünya, değiştirilmeden
    "unite": ("sogutma_grubu_taban", "sogutma_grubu_kondenser", "sogutma_grubu_fan", "sogutma_grubu_kompresor"),
    "montaj": ("sogutma_grubu_montaj_rayi_arka", "sogutma_grubu_montaj_rayi_on", "sogutma_grubu_takozu_"),
    "conta": ("sogutma_grubu_taban_contasi", "k4_kondenser_contasi", "k4_emis_yan_conta_"),
    "hava_yolu": ("k4_emis_yan_sac_", "k4_emis_on_kapama_", "k4_ara_perde"),
    "servis_paneli": ("k4_kapak_sogutma_dis_sac", "k4_panel_klipsi_"),
    "tava": ("buharlastirma_tavasi",),
}
SECOP_AD = tuple(a for v in SECOP_GRUP.values() for a in v)
K4_YAPI_AD = ("k4_ara_sac_alt", "k4_ara_pu", "k4_ara_sac_ust", "kablo_kanali_K4", "taban_k4_kademe_saci", "bolme_2_")
GIDER_ESKI_AD = ("gider_kilifi_", "gider_kelepcesi_", "gider_cek_valfi_")
GIDER_DAL_AD = {"gider_borusu_sol": "sol", "gider_borusu_sag": "sag"}
BOLME_V1 = {BOLME_AD[i]: i for i in (1, 3, 4, 5)}                                 # gider ana hattının geçtiği bölmeler (bolme_<i>_*)

PARCALAR = []            # v2 · dünya
SECOP_V1 = []            # K4 soğutma grubu + tavası (v1 dünya, değiştirilmeden) → E altı (öbür ajan)
PANO_V1 = []             # B_ELEKTRIK (pano plakası + cihazlar, v1 dünya) → E altı (öbür ajan)
DEPO_V1 = []             # B_DEPO kaşar / sucuk deposu (v1 dünya) → DÜŞER (yedek TOPPING üst katında)
K4_YAPI_V1 = []          # K4 ara katmanı, dikey kablo kanalı, kademe sacı, B3 bölmesi → DÜŞER
GIDER_V1_KALKAN = []     # v1 gider kılıfları / kelepçeleri / çek valfleri → ana hat donanımıyla değişti
V1_PARCALAR = []         # son modul()'ün v1 listesi (denetim referansı)
RAPOR = {}

BIRIM_AD = {
    "B_KASA": "ÇEKMECELİ DOLAP gövdesi (tek parça, +3 °C) · HAT v2 x %.1f–%.0f × 123–788 (v1 K4 kolonu + B3 çıktı) · sandviç kabuk + PU + 5 bölme (B1 · B2 · B4 · B5 · B6) · "
              "fırın altında hava boşluklu ısı kalkanı" % (X0, X1),
    "B_KABLO": "Kablo kanalları 40 × 25: her kolonda dikey + üstte yatay (K1→K3 703–728 · B4'ten K6'ya 643–668, K3 arka sağ köşede dikey bağlantı) · E panosuna çıkış: öbür ajan",
    "B_SOGUTMA": "Soğutma: 2 bölge lamelli evaporatör (sol K2 arkası → K1–K3 · sağ K5 arkası → K5–K6) + davlumbaz + 4 × ebm-papst 4414 FL · gider: Ø12 dallar → "
                 "Ø20 ana hat (arkada yerde, ≥ %1) → sağ dış sac x 4000 (y 170 · z −760) → E altındaki tava · Secop CU NLE8.8CN E'nin altında (öbür ajan)",
    "B_TASIYICI": "Fırın taşıyıcı çerçevesi 304 (v1 ile aynı): 2 kiriş 40 × 40 × 2 + 3 çapraz + 6 dikme (B4 / B5 / B6 bölmelerinde) · x 2502,5–3996,5",
    "B_COP": "ROBOT ÇÖPÜ şeridi 3810–4000 (v1 ile aynı): 15 L kova + atma boşluğu + yaylı klape",
}


# ---------------------------------------------------------------- yardımcılar
def _kut(x0, x1, y0, y1, z0, z1):
    return cq.Solid.makeBox(abs(x1 - x0), abs(y1 - y0), abs(z1 - z0), V(min(x0, x1), min(y0, y1), min(z0, z1)))


def _sekil(wp):
    v = wp.vals() if hasattr(wp, "vals") else [wp]
    v = [o for o in v if isinstance(o, cq.Shape)]
    return v[0] if len(v) == 1 else cq.Compound.makeCompound(v)


def _tek(sh):
    """tek katılı bileşik → katı (montaj wp.val() ile okur)"""
    ss = sh.Solids()
    if len(ss) == 1: return ss[0]
    return cq.Compound.makeCompound(ss) if ss else sh


def _wp(sh):
    return cq.Workplane("XY").add(sh)


def _sinif(b):
    if b.xmax <= DILIM[0] + EPS: return "sol"
    if b.xmin >= DILIM[1] - EPS: return "sag"
    if b.xmin >= DILIM[0] - EPS and b.xmax <= DILIM[1] + EPS: return "ic"
    return "dilim"


def dilimle(sh):
    """v1 dünya şeklinden B_DILIM'i çıkarır: solu +DXL, sağı yerinde, dilimin içi atılır (uzun prizmatik gövde parçaları) · dilimin içindeyse None"""
    b = sh.BoundingBox(); s = _sinif(b)
    if s == "sol": return sh.translate(V(DXL, 0.0, 0.0))
    if s == "sag": return sh
    if s == "ic": return None
    ss = []
    if b.xmin < DILIM[0] - EPS:
        sol = sh.intersect(_kut(b.xmin - 10.0, DILIM[0], b.ymin - 10.0, b.ymax + 10.0, b.zmin - 10.0, b.zmax + 10.0))
        if sol.Volume() > EPS: ss.append(sol.translate(V(DXL, 0.0, 0.0)))
    if b.xmax > DILIM[1] + EPS:
        sag = sh.intersect(_kut(DILIM[1], b.xmax + 10.0, b.ymin - 10.0, b.ymax + 10.0, b.zmin - 10.0, b.zmax + 10.0))
        if sag.Volume() > EPS: ss.append(sag)
    if not ss: return None
    if len(ss) == 1: return _tek(ss[0].clean())
    return _tek(ss[0].fuse(ss[1]).clean())


def _doldur(sh, bolge):
    """sh'nin sınır kutusu içinde 'bolge'yi doldurur (kalkan v1 gider deliği / hava geçişi) → (yeni şekil, dolan hacim)"""
    b = sh.BoundingBox()
    d = bolge.intersect(_kut(b.xmin, b.xmax, b.ymin, b.ymax, b.zmin, b.zmax))
    v = d.Volume()
    if v < EPS: return sh, 0.0
    return _tek(sh.fuse(d).clean()), v


def _yol(P, r):
    return SC0.yol_kati(P, r).val()


def gider_katilari():
    """v2 gider katıları (dünya): ana boru, kılıf dış katısı, dallar (ana boruyla kesilmiş), kılıflar, eyerler, duvar geçişi
    · son koşu %5,5 eğimli → boru ucu x 4000 düzleminde KESİLİR (arayüz ekseni tam 4000 · 170 · −760); delici katılar ucun 10 mm ötesine uzatılır"""
    A = GIDER["ana"]
    u, v = V(*A[-2]), V(*A[-1]); d = (v - u).normalized()
    A_uz = A[:-1] + [(v + d * 10.0).toTuple()]                                  # delici yol (duvarı tam deler)
    ana = _tek(_yol(A_uz, R_ANA).intersect(_kut(X_ANA0 - 50.0, X1, 0.0, 400.0, -900.0, 0.0)).clean())
    dis = _yol(A_uz, R_KILIF)
    out = dict(ana=ana, dis=dis, dal={}, kilif={}, kelepce={})
    for yan in ("sol", "sag"):
        out["dal"][yan] = _tek(_yol(GIDER[yan], R_DAL).cut(ana).clean())
    for ad_, (bx0, bx1) in GECIS_BOLME.items():
        out["kilif"][ad_] = _tek(dis.intersect(_kut(bx0, bx1, 100.0, 300.0, -800.0, -680.0)).cut(ana).clean())
    out["duvar"] = _tek(dis.intersect(_kut(X_YAN_DIS[0], X_YAN_DIS[1], 100.0, 300.0, -800.0, -700.0)).cut(ana).clean())
    for k_, xk in X_KELEPCE.items():
        out["kelepce"][k_] = _tek(_kut(xk - 5.0, xk + 5.0, Y_TABAN, y_ana(xk), Z_ANA - R_KILIF, Z_ANA + R_KILIF).cut(ana).clean())
    return out


def _plint_v1_izgarasiz():
    """store_cad_v14 onyuz_plint tarifi, Secop emiş ızgarası (PLINT_IZGARA) OLMADAN · v1 dünya"""
    PZ = (Z_ON - 61.5, Z_ON - 60.0)
    pl_ = SC0.kut(SC0.X_IC0, SC0.X_IC1, 0.0, Y_PLINT, PZ[0], PZ[1]).union(
        SC0.kut(SC0.X_IC0 + 1.5, SC0.X_IC1 - 1.5, Y_PLINT - 1.5, Y_PLINT, PZ[0] - SC0.PLINT_FLANS, PZ[0]))
    return _sekil(pl_)


def _hava_b4():
    """B4 arka hava geçişleri (store_cad_v14.hava_gecis(3, …) kutuları) · v1 = v2 dünya (B4 yerinde)"""
    g = None
    for y0_, y1_ in SC0.HAVA_GECIS.get(3, ()):
        k = _kut(SC0.BOLME_X[3] - 1.0, SC0.BOLME_X[3] + BOLME + 1.0, y0_, y1_, SC0.HAVA_Z[0], SC0.HAVA_Z[1])
        g = k if g is None else g.fuse(k)
    return g


def modul():
    """v2 dolap parçaları (dünya) → PARCALAR · store_cad_v14.modul() özetini aynen döndürür (21 çekmece, kodlar aynı) · İDEMPOTENT"""
    oz = SC0.modul()
    v1 = list(SC0.PARCALAR)
    V1_PARCALAR[:] = v1
    G1 = SC0.gider_yollari()                                                       # v1 gider kılıf bölgeleri = bölmelerdeki eski delikler
    eski_delik = {"B2": [_sekil(d_) for a_, d_, _k in G1["sol"]["kilif"] if a_ == "B2"],
                  "B4": [_sekil(d_) for a_, d_, _k in G1["sag"]["kilif"] if a_ == "B4"]}
    GK = gider_katilari()
    HB4 = _hava_b4() if B4_HAVA_KAPAT else None
    out, secop, pano, depo, yapi, gider_eski = [], [], [], [], [], []
    say = dict(kaydi=0, yerinde=0, dilim=0, cekmece_sol=0, cekmece_sag=0, degisti=0, yeni=0)
    doldu = {}
    for p in v1:
        a, bir = p["ad"], p["birim"]
        if bir.startswith(tuple("CEK_%s_" % k for k in SOL_KOL)):
            out.append(dict(p, wp=p["wp"].translate((DXL, 0.0, 0.0)))); say["cekmece_sol"] += 1; continue
        if bir.startswith("CEK_"):
            out.append(dict(p)); say["cekmece_sag"] += 1; continue
        if bir == "B_ELEKTRIK":
            pano.append(dict(p)); continue
        if bir == "B_DEPO":
            depo.append(dict(p)); continue
        if a.startswith(SECOP_AD):
            secop.append(dict(p)); continue
        if a.startswith(K4_YAPI_AD):
            yapi.append(dict(p)); continue
        if a.startswith(GIDER_ESKI_AD):
            gider_eski.append(dict(p)); continue
        if a in GIDER_DAL_AD:                                                     # ad / malzeme / BOM korunur, yol yeni (ana hatta T)
            out.append(dict(p, wp=_wp(GK["dal"][GIDER_DAL_AD[a]]))); say["degisti"] += 1; continue
        sh = _sekil(p["wp"])
        if a == "onyuz_plint" and PLINT_IZGARA_KALDIR:
            sh = _plint_v1_izgarasiz()
        m = re.match(r"^bolme_(\d)_(sac_a|sac_b|pu)$", a)
        bol = {v_: k_ for k_, v_ in BOLME_V1.items()}.get(int(m.group(1))) if m else None
        if bol in eski_delik:                                                     # v1 gider deliği (B2 sol · B4 sağ) doldurulur (v1 dünya)
            for d_ in eski_delik[bol]:
                sh, v_ = _doldur(sh, d_); doldu[(a, "gider")] = v_
        if bol == "B4" and HB4 is not None:
            sh, v_ = _doldur(sh, HB4); doldu[(a, "hava")] = v_
        s = _sinif(sh.BoundingBox())
        if s == "ic":
            raise AssertionError("dilimin içinde sınıfsız gövde parçası: %s (%s)" % (a, bir))
        yeni = dilimle(sh)
        say["kaydi" if s == "sol" else "yerinde" if s == "sag" else "dilim"] += 1
        if bol is not None:                                                       # ana hat kılıfı için delik (v2 dünya)
            yeni = _tek(yeni.cut(GK["dis"]).clean()); say["degisti"] += 1
        if a == "kasa_yan_dis_sac_sag":
            yeni = _tek(yeni.cut(GK["dis"]).clean()); say["degisti"] += 1
        if a == "onyuz_plint" and PLINT_IZGARA_KALDIR:
            say["degisti"] += 1
        out.append(dict(p, wp=_wp(yeni)))
    # ---- yeni parçalar (gider ana hattı + kablo bağlantısı) ----
    B_ = "B_SOGUTMA"
    L_ = sum(math.dist(u, v) for u, v in zip(GIDER["ana"], GIDER["ana"][1:]))
    out.append(dict(ad="gider_ana_hatti_borusu", wp=_wp(GK["ana"]), mal="plastik", birim=B_, grup="SABIT",
                    bom=("Gider ana hattı Ø20 × 1,5 PVC", 1, "iki evaporatör giderini toplar (K2 arkası x %.1f · K5 arkası x %.0f, T girişli) · arkada yerde z %.0f, sürekli ≥ %%%.1f eğim · "
                         "şeritte z %.0f'a döner · B'nin sağ dış sacından x %.0f'de çıkar (eksen y %.0f · z %.0f) → K içinden E altındaki tavaya"
                         % (EVAP["sol"]["gider"][0], EVAP["sag"]["gider"][0], Z_ANA, 100.0 * EGIM, ARAYUZ_GIDER[2], ARAYUZ_GIDER[0], ARAYUZ_GIDER[1], ARAYUZ_GIDER[2]),
                         "boy %.0f mm (B içinde) · bölme geçişleri Ø24 kılıfta · kuru kapan (ördek gagası) tava ucunda (öbür ajan)" % L_)))
    for i_, (ad_, k_) in enumerate(GK["kilif"].items()):
        out.append(dict(ad="gider_ana_hatti_kilifi_" + ad_, wp=_wp(k_), mal="plastik", birim=B_, grup="SABIT",
                        bom=("Gider ana hattı kılıfı Ø24 × 2 PVC", len(GK["kilif"]), "bölme PU'su içinde köpükle birlikte · içinden Ø20 boru kayar", "B2 · B4 · B5 · B6 geçişleri") if i_ == 0 else None))
    out.append(dict(ad="gider_ana_hatti_duvar_gecisi", wp=_wp(GK["duvar"]), mal="plastik", birim=B_, grup="SABIT",
                    bom=("Duvar geçiş lastiği Ø24 / Ø20", 1, "B sağ dış sacında (x 3998,5–4000) · boru içinden kayar", "arayüz noktası: öbür ajan K'da devam eder")))
    for i_, (ad_, k_) in enumerate(GK["kelepce"].items()):
        out.append(dict(ad="gider_ana_hatti_kelepcesi_" + ad_, wp=_wp(k_), mal="plastik", birim=B_, grup="SABIT",
                        bom=("Boru eyeri Ø20 · PA", len(GK["kelepce"]), "taban iç sacına 2 × perçin · boru eyere kelepçeyle", "K3 · K5 · K6") if i_ == 0 else None))
    say["yeni"] = 2 + len(GK["kilif"]) + len(GK["kelepce"])                    # ana boru + duvar geçişi + kılıflar + eyerler
    if KABLO_BAGLANTI:
        out.append(dict(ad="kablo_kanali_baglanti_B4", wp=_wp(_kut(*KABLO_BAG_K)), mal="kanal", birim="B_KABLO", grup="SABIT", bom=None))
        say["yeni"] += 1
    PARCALAR[:] = out
    SECOP_V1[:] = secop; PANO_V1[:] = pano; DEPO_V1[:] = depo; K4_YAPI_V1[:] = yapi; GIDER_V1_KALKAN[:] = gider_eski
    RAPOR.clear(); RAPOR.update(say=say, doldu=doldu, secop=len(secop), pano=len(pano), depo=len(depo), yapi=len(yapi), gider_eski=len(gider_eski))
    return [tuple(o) for o in oz]


def k4_parcalari():
    """(SECOP_V1, PANO_V1, DEPO_V1) — boşsa modul() koşar (öbür ajan doğrudan çağırabilir)"""
    if not SECOP_V1: modul()
    return SECOP_V1, PANO_V1, DEPO_V1


# ---------------------------------------------------------------- ÖZ DENETİM
DEN = []


def kontrol(ad, sart, deger=""):
    DEN.append((ad, bool(sart), deger)); print("  %-160s %s %s" % (ad, "GEÇTİ" if sart else "** KALDI **", deger)); sys.stdout.flush()


def _bb(p):
    return _sekil(p["wp"]).BoundingBox()


def _bbk(A, B, pay=0.05):
    return A.xmin < B.xmax - pay and B.xmin < A.xmax - pay and A.ymin < B.ymax - pay and B.ymin < A.ymax - pay and A.zmin < B.zmax - pay and B.zmin < A.zmax - pay


def _icerik(ad):
    return "_top_" in ad or "_kutu330_" in ad or "_tatlikabi_" in ad


def _tarama(L1, L2=None, esik=1.0):
    """[(ad, şekil, bb)] listelerinde gerçek kesişim > esik (L2 None → L1 kendi arasında) · ön süzgeç değen kutuları da alır (ince örtüşme kaçmaz)"""
    bul, aday = [], 0
    ayni = L2 is None; L2 = L1 if ayni else L2
    for i, (a, sa, A) in enumerate(L1):
        for c, sc, B in (L2[i + 1:] if ayni else L2):
            if a == c or not _bbk(A, B, pay=-0.01): continue
            aday += 1
            v = sa.intersect(sc).Volume()
            if v > esik: bul.append((round(v, 2), a, c))
    return sorted(bul, reverse=True), aday


def denetim(tarama=True):
    from OCP.BRepExtrema import BRepExtrema_DistShapeShape as _DSS
    t0 = time.time()
    P2 = {p["ad"]: p for p in PARCALAR}
    V1 = {p["ad"]: p for p in V1_PARCALAR}
    SH = {a: _sekil(p["wp"]) for a, p in P2.items()}
    BB = {a: s.BoundingBox() for a, s in SH.items()}
    SH1 = {a: _sekil(p["wp"]) for a, p in V1.items()}
    BB1 = {a: s.BoundingBox() for a, s in SH1.items()}
    dist = lambda a, b: _DSS(a.wrapped, b.wrapped).Value()
    print("h2_store_v1 · v2 %d parça (v1 %d) · %s" % (len(PARCALAR), len(V1_PARCALAR), RAPOR["say"]))
    kontrol("parça adları tekil (%d)" % len(P2), len(P2) == len(PARCALAR))
    # ---- 1 · ÇEKMECELER: 21 · kodlar v1 ile aynı · her çekmecenin parçası var · K1–K3 +507,5 · K5–K6 yerinde (sınır kutusundan) ----
    kod1 = [c[1] for c in SC0.CEK]; kod2 = [c[1] for c in CEK]
    eksik = [k for k in kod2 if not any(p["birim"] == k for p in PARCALAR)]
    kay = 0.0
    for p in PARCALAR:
        if p["birim"].startswith("CEK_"):
            b2, b1 = BB[p["ad"]], BB1[p["ad"]]
            dx = DXL if p["birim"].split("_")[1] in SOL_KOL else 0.0
            kay = max(kay, abs(b2.xmin - b1.xmin - dx), abs(b2.xmax - b1.xmax - dx), abs(b2.ymin - b1.ymin), abs(b2.zmax - b1.zmax))
    kontrol("21 çekmece · kodlar v1 ile aynı (%s … %s) · her kodun parçası var · K1–K3 parçaları v1 + %.1f, K5–K6 yerinde (en büyük sapma %.1e)"
            % (kod2[0], kod2[-1], DXL, kay), len(CEK) == 21 and kod1 == kod2 and not eksik and kay < 1e-6, str(eksik[:4]))
    # ---- 2 · ZARF: bütün parçalar x 507,5 … 4000 · y 0 … 788 · z −830 … +79 · gövde altı 123 ----
    xs0 = min(b.xmin for b in BB.values()); xs1 = max(b.xmax for b in BB.values())
    ys1 = max(b.ymax for b in BB.values()); zs0 = min(b.zmin for b in BB.values()); zs1 = max(b.zmax for b in BB.values())
    tas = [a for a, b in BB.items() if b.xmin < X0 - 0.01 or b.xmax > X1 + 0.01]
    gov = min(b.ymin for a, b in BB.items() if not a.startswith(("ayak_", "onyuz_plint")))
    kontrol("ZARF x %.2f–%.2f ⊂ [%.1f, %.0f] (taşan %d) · üst %.2f = %.0f · z %.1f…%+.1f · gövde altı %.2f = %.0f (ayak + plint hariç)"
            % (xs0, xs1, X0, X1, len(tas), ys1, H_B, zs0, zs1, gov, Y_PLINT),
            not tas and abs(xs0 - X0) < 0.01 and abs(xs1 - X1) < 0.01 and abs(ys1 - H_B) < 0.01 and abs(zs0 - Z_ARKA_DIS) < 0.01 and abs(zs1 - Z_ON1) < 0.01 and abs(gov - Y_PLINT) < 0.01, str(tas[:4]))
    # ---- 3 · K4 İÇERİĞİ: v2'de yok · taşınanlar v1 dünyasında değiştirilmeden ----
    k4ad = re.compile(r"^(sogutma_grubu_|k4_|buharlastirma_tavasi|pano_montaj|din_ray_|plc_|guc_kaynagi|surucu_EM|role_\d|klemens_blogu|kablo_kanali_K4$|bolme_2_|taban_k4_kademe|gider_(kilifi|kelepcesi|cek_valfi)_)")
    kalan = [a for a in P2 if k4ad.match(a)]
    deg = [p["ad"] for L_ in (SECOP_V1, PANO_V1, DEPO_V1) for p in L_ if _sekil(p["wp"]).BoundingBox().xmin != BB1[p["ad"]].xmin or p["wp"] is not V1[p["ad"]]["wp"]]
    kontrol("K4 içeriği v2'de YOK (%d) · SECOP_V1 %d + PANO_V1 %d + DEPO_V1 %d parça v1 dünyasında DEĞİŞTİRİLMEDEN (aynı wp nesnesi) · K4 yapısı %d + eski gider donanımı %d düşer"
            % (len(kalan), len(SECOP_V1), len(PANO_V1), len(DEPO_V1), len(K4_YAPI_V1), len(GIDER_V1_KALKAN)), not kalan and not deg, str((kalan + deg)[:6]))
    tum = {p["ad"] for L_ in (SECOP_V1, PANO_V1, DEPO_V1, K4_YAPI_V1, GIDER_V1_KALKAN) for p in L_}
    kay_v1 = [a for a in V1 if a not in P2 and a not in tum]
    kontrol("v1'in her parçası ya v2'de ya bir K4 / gider listesinde (kayıp %d) · v1 %d = v2'ye geçen %d + listelenen %d"
            % (len(kay_v1), len(V1), len([a for a in V1 if a in P2]), len(tum)), not kay_v1 and len(V1) == len([a for a in V1 if a in P2]) + len(tum), str(kay_v1[:5]))
    # ---- 4 · DİLİM HACMİ: dilimi aşan gövde parçaları v2 hacmi = v1 − dilimin içi (değişen parçalar hariç) ----
    degisen = {"onyuz_plint", "kasa_yan_dis_sac_sag"} | {a for a in P2 if re.match(r"^bolme_[1345]_(sac_a|sac_b|pu)$", a)}
    kutu_d = _kut(DILIM[0], DILIM[1], -10.0, 900.0, -900.0, 200.0)
    dh, nd = 0.0, 0
    for a in P2:
        if a not in V1 or a in degisen or P2[a]["birim"].startswith("CEK_") or a in GIDER_DAL_AD: continue
        if _sinif(BB1[a]) != "dilim": continue
        v1_, v2_ = SH1[a].Volume(), SH[a].Volume(); vic = SH1[a].intersect(kutu_d).Volume()
        dh = max(dh, abs(v1_ - vic - v2_) / max(1.0, v1_)); nd += 1
        if not SH[a].isValid(): dh = 9.9
    kontrol("DİLİM: dilimi aşan %d gövde parçasında hacim v2 = v1 − dilim içi (en büyük bağıl sapma %.1e) · katılar geçerli" % (nd, dh), nd == 15 and dh < 1e-6)
    sol_sag = max(max(abs(BB[a].xmin - BB1[a].xmin - (DXL if _sinif(BB1[a]) == "sol" else 0.0)), abs(BB[a].ymax - BB1[a].ymax), abs(SH[a].Volume() - SH1[a].Volume()))
                  for a in P2 if a in V1 and a not in degisen and not P2[a]["birim"].startswith("CEK_") and a not in GIDER_DAL_AD and _sinif(BB1[a]) in ("sol", "sag"))
    kontrol("tamamen solda kalan gövde parçaları v1 + %.1f, sağdakiler yerinde (sınır kutusu + hacim, en büyük sapma %.1e)" % (DXL, sol_sag), sol_sag < 1e-6)
    gec = [a for a, s in SH.items() if not s.isValid()]
    kontrol("bütün v2 katıları geçerli (%d)" % len(SH), not gec, str(gec[:5]))
    # ---- 5 · ÖN YÜZ ızgarası: kolon önleri 126–785 · aralar 3 · kolonlar arası 3 · 507,5 → 4000 (katılardan) ----
    on = [BB[a] for a in P2 if (a.endswith("_on_dis_sac_1.5") and a.startswith("CEK_")) or a.startswith("serit_on_")]
    top_ok, sut_r = True, []
    for kol, (pa, pb) in sorted(KAPAK_X.items(), key=lambda kv: kv[1][0]):
        sut = sorted((b for b in on if abs(b.xmin - pa) < 0.05 and abs(b.xmax - pb) < 0.05), key=lambda b: b.ymin)
        ok = bool(sut) and abs(sut[0].ymin - SC0.ON_ALT) < 0.05 and abs(sut[-1].ymax - SC0.ON_UST) < 0.05 and all(abs(v_.ymin - u_.ymax - FUGA) < 0.05 for u_, v_ in zip(sut, sut[1:]))
        top_ok &= ok; sut_r.append("%s %.1f–%.1f ×%d" % (kol, pa, pb, len(sut)))
    xs = sorted(KAPAK_X.values())
    top_ok &= all(abs(b[0] - a[1] - FUGA) < 0.05 for a, b in zip(xs, xs[1:])) and abs(xs[0][0] - X0) < 0.01 and abs(xs[-1][1] - X1) < 0.01
    kontrol("ÖN YÜZ: %s · kolonlar arası 3 · %.1f → %.0f kesintisiz (K3 önü B4'ün 16'sını örter, K5 önüne derz 3)" % (" · ".join(sut_r), X0, X1), top_ok)
    # ---- 6 · K3 ↔ B4: kesişim < 1 mm³ · K3 sağ dış rayları B4 sacına ≤ 2 mm (bağlı) ----
    B4 = [a for a in P2 if re.match(r"^bolme_3_(sac_a|sac_b|pu)$", a)]
    K3 = [a for a in P2 if P2[a]["birim"].startswith("CEK_K3_")]
    k3b4 = []
    for a in K3:
        for c in B4:
            if _bbk(BB[a], BB[c], pay=-0.05):
                v_ = SH[a].intersect(SH[c]).Volume()
                if v_ >= 1.0: k3b4.append((round(v_, 2), a, c))
    ray = [a for a in K3 if a.endswith("_ray_dis_sag")]
    rd = {a: dist(SH[a], SH["bolme_3_sac_a"]) for a in ray}
    kontrol("K3 ↔ B4: %d K3 parçası × %d B4 parçası kesişim ≥ 1 mm³ = %d · K3 sağ dış rayları (%d) B4 sacına en çok %.3f mm (≤ 2, dış eleman bölmeye vidalı) · K3 sağ ucu %.1f = B4 sol yüzü %.1f"
            % (len(K3), len(B4), len(k3b4), len(ray), max(rd.values()), max(BB[a].xmax for a in ray), BB["bolme_3_sac_a"].xmin),
            not k3b4 and len(ray) == 5 and max(rd.values()) <= 2.0 and abs(max(BB[a].xmax for a in ray) - BB["bolme_3_sac_a"].xmin) < 0.01, str(k3b4[:4]))
    # ---- 7 · GİDER: eğim · arayüz · bölmelerdeki eski delikler dolu, yeni delik kılıf kadar ----
    eg = []
    for k_ in ("ana", "sol", "sag"):
        P_ = GIDER[k_]
        for u, v in zip(P_, P_[1:]):
            yat = math.hypot(v[0] - u[0], v[2] - u[2]); eg.append((k_, (u[1] - v[1]) / yat if yat > 1e-9 else 99.0))
    ana_b = BB["gider_ana_hatti_borusu"]
    uf = [f for f in SH["gider_ana_hatti_borusu"].Faces() if f.geomType() == "PLANE" and abs(f.Center().x - X1) < 1e-3]
    uc = uf[0].Center() if len(uf) == 1 else V(0.0, 0.0, 0.0)
    ucb = uf[0].BoundingBox() if len(uf) == 1 else ana_b
    kontrol("GİDER EĞİMİ: ana hat %s · dallar sol %s / sağ %s → her koşu ≥ %%1 · en alçak nokta = arayüz (sifon yok)"
            % (" / ".join("%.2f%%" % (100 * e) for k, e in eg if k == "ana"), " / ".join("%s" % ("dik" if e > 9 else "%.2f%%" % (100 * e)) for k, e in eg if k == "sol"),
               " / ".join("%s" % ("dik" if e > 9 else "%.2f%%" % (100 * e)) for k, e in eg if k == "sag")),
            min(e for _k, e in eg) >= 0.01 - 1e-9 and all(u[1] > v[1] for k_ in ("ana", "sol", "sag") for u, v in zip(GIDER[k_], GIDER[k_][1:])))
    kontrol("GİDER ARAYÜZÜ: ana boru uç yüzü (x %.0f düzleminde kesik, %d yüz) merkezi x %.3f · y %.3f · z %.3f · yükseklik %.2f · genişlik %.2f (Ø20) = (%.0f · %.0f · %.0f) · boru en sağ %.3f · sağ dış sac dış yüzü %.1f"
            % (X1, len(uf), uc.x, uc.y, uc.z, ucb.ylen, ucb.zlen, *ARAYUZ_GIDER, ana_b.xmax, BB["kasa_yan_dis_sac_sag"].xmax),
            len(uf) == 1 and abs(uc.x - ARAYUZ_GIDER[0]) < 1e-3 and abs(uc.y - ARAYUZ_GIDER[1]) < 1e-3 and abs(uc.z - ARAYUZ_GIDER[2]) < 1e-3
            and abs(ucb.zlen - 2 * R_ANA) < 0.01 and abs(ucb.ylen - 2 * R_ANA) < 0.05 and abs(ana_b.xmax - X1) < 1e-6 and abs(BB["kasa_yan_dis_sac_sag"].xmax - X1) < 0.01)
    dol = RAPOR["doldu"]
    G1 = SC0.gider_yollari()                                                       # v1 eski delik bölgeleri (B2 +DXL · B4 yerinde)
    eski = {"bolme_1": [_sekil(d_).translate(V(DXL, 0.0, 0.0)) for a_, d_, _k in G1["sol"]["kilif"] if a_ == "B2"],
            "bolme_3": [_sekil(d_) for a_, d_, _k in G1["sag"]["kilif"] if a_ == "B4"] + ([_hava_b4()] if B4_HAVA_KAPAT else [])}
    dk_ = []
    for a in B4 + [a for a in P2 if re.match(r"^bolme_1_(sac_a|sac_b|pu)$", a)]:
        kb_ = _kut(BB[a].xmin, BB[a].xmax, BB[a].ymin, BB[a].ymax, BB[a].zmin, BB[a].zmax)
        for d_ in eski[a[:7]]:
            hedef_ = d_.intersect(kb_).Volume()
            if hedef_ > EPS: dk_.append((SH[a].intersect(d_).Volume() / hedef_, a))
    kontrol("BÖLMELER: v1 gider delikleri DOLDU (B2 %s · B4 %s mm³) · B4 hava geçişleri %s (dolan %.0f mm³) · eski bölgelerde malzeme oranı en az %.6f (%d bölge × parça)"
            % ("/".join("%.0f" % v for (a, k), v in dol.items() if a.startswith("bolme_1") and k == "gider"), "/".join("%.0f" % v for (a, k), v in dol.items() if a.startswith("bolme_3") and k == "gider"),
               "KAPALI" if B4_HAVA_KAPAT else "AÇIK", sum(v for (a, k), v in dol.items() if k == "hava"), min(r_ for r_, _a in dk_), len(dk_)),
            min(r_ for r_, _a in dk_) > 0.9999 and all(v > 1.0 for (a, k), v in dol.items() if k == "gider") and len([1 for (a, k) in dol if k == "gider"]) == 6)
    dis = gider_katilari()["dis"]
    ic_b = [(a, round(SH[a].intersect(dis).Volume(), 3)) for a in P2 if re.match(r"^bolme_[1345]_(sac_a|sac_b|pu)$", a) or a == "kasa_yan_dis_sac_sag"]
    kontrol("BÖLME GEÇİŞLERİ: B2 · B4 · B5 · B6 sac + PU ve sağ dış sac Ø24 kılıf kadar delik (kalan malzeme %.3f mm³) · kılıflar %s"
            % (sum(v for _a, v in ic_b), " · ".join("%s x %.0f–%.0f" % (a[-2:], BB[a].xmin, BB[a].xmax) for a in P2 if a.startswith("gider_ana_hatti_kilifi_"))),
            sum(v for _a, v in ic_b) < 0.01 and len([a for a in P2 if a.startswith("gider_ana_hatti_kilifi_")]) == 4)
    # gider ↔ bütün parçalar (kapalı konum) · en yakın komşular
    GID = [a for a in P2 if a.startswith("gider_") or a == "kablo_kanali_baglanti_B4"]
    Lg = [(a, SH[a], BB[a]) for a in GID]; La = [(a, SH[a], BB[a]) for a in P2 if a not in GID]
    g_c, g_ad = _tarama(Lg, La, esik=0.1)
    g_i, _n = _tarama(Lg, None, esik=0.1)
    kontrol("GİDER + KABLO BAĞLANTISI (%d parça) ↔ öbür %d parça: kesişim > 0,1 mm³ = %d (aday %d) · kendi arasında %d" % (len(Lg), len(La), len(g_c), g_ad, len(g_i)), not g_c and not g_i, str((g_c + g_i)[:6]))
    ana = SH["gider_ana_hatti_borusu"]
    yak = []
    for a, s_, b_ in La:
        if b_.xmin > ana_b.xmax + 30 or ana_b.xmin > b_.xmax + 30 or b_.ymin > ana_b.ymax + 30 or ana_b.ymin > b_.ymax + 30 or b_.zmin > ana_b.zmax + 30 or ana_b.zmin > b_.zmax + 30:
            continue
        d_ = dist(ana, s_)
        if d_ < 30.0: yak.append((round(d_, 2), a))
    for a in GID:
        if a != "gider_ana_hatti_borusu":
            d_ = dist(ana, SH[a])
            if d_ < 30.0: yak.append((round(d_, 2), a))
    yak.sort()
    tem = sorted(a for d_, a in yak if d_ <= 0.05)
    bek = {"gider_borusu_sol", "gider_borusu_sag", "gider_ana_hatti_duvar_gecisi"} | {a for a in P2 if a.startswith(("gider_ana_hatti_kilifi_", "gider_ana_hatti_kelepcesi_"))}
    kontrol("ANA HAT TEMASLARI yalnız kendi donanımı (%s) · en yakın öbür parçalar: %s"
            % (", ".join(tem), " · ".join("%s %.1f" % (a, d_) for d_, a in yak if d_ > 0.05)[:420]), set(tem) <= bek and "kasa_yan_dis_sac_sag" not in tem)
    for yan in ("sol", "sag"):
        tb = BB["damlama_teknesi_%s" % yan]; db = BB["gider_borusu_%s" % yan]
        kontrol("dal %s: tepsi dibi y %.1f = boru üstü %.1f · x %.1f ⊂ tepsi %.1f–%.1f · ana hatta T (temas %.3f mm)"
                % (yan, tb.ymin, db.ymax, (db.xmin + db.xmax) / 2.0, tb.xmin, tb.xmax, dist(SH["gider_borusu_%s" % yan], ana)),
                abs(tb.ymin - db.ymax) < 0.01 and tb.xmin < db.xmin and db.xmax < tb.xmax and dist(SH["gider_borusu_%s" % yan], ana) < 0.01)
    if not tarama:
        return
    # ---- 8 · DİKİŞ PENCERESİ (sınır kutusu x 1850–2600'e değen bütün parçalar, kapalı) · v1'de değen çiftler serbest ----
    t1 = time.time()
    W = [a for a in P2 if not _icerik(a) and BB[a].xmax > 1850.0 and BB[a].xmin < 2600.0]
    Lw = [(a, SH[a], BB[a]) for a in W]
    bul, aday = _tarama(Lw, None, esik=1.0)
    W1 = [a for a in W if a in V1]
    Lw1 = [(a, SH1[a], BB1[a]) for a in W1]
    bul1, aday1 = _tarama(Lw1, None, esik=1.0)
    serbest = {(a, c) for _v, a, c in bul1} | {(c, a) for _v, a, c in bul1}
    yeni_c = [x for x in bul if (x[1], x[2]) not in serbest]
    kontrol("DİKİŞ PENCERESİ x 1850–2600 (kapalı · %d parça, içerik hariç · %d aday · %.0f sn): gerçek kesişim > 1 mm³ = %d · v1'deki aynı parçalar (%d, %d aday) kesişim %d → serbest liste %d · yeni %d"
            % (len(W), aday, time.time() - t1, len(bul), len(W1), aday1, len(bul1), len(serbest) // 2, len(yeni_c)), not yeni_c, str(yeni_c[:6]))
    # ---- 9 · K3 STROK TARAMASI (çekmece 700 · ara ray 350, 4 konum) + K2 / K5 / K6 ↔ gider ----
    HAR = {"CEKMECE": 1.0, "CEKMECE_ARA": RAY_ARA_ORAN}
    SAB = [(a, SH[a], BB[a]) for a in P2 if P2[a]["grup"] not in HAR and not _icerik(a)]           # store_cad_v14.cakisma() ile aynı (KLAPE dahil)
    for kol, hedef, ad_ in (("K3", SAB, "bütün sabit parçalar"), ("K2", [x for x in SAB if x[0] in GID], "gider"), ("K5", [x for x in SAB if x[0] in GID], "gider"),
                            ("K6", [x for x in SAB if x[0] in GID], "gider")):
        t1 = time.time(); top_b, top_a = [], 0
        Hk = [(a, SH[a]) for a in P2 if P2[a]["birim"].startswith("CEK_%s_" % kol) and P2[a]["grup"] in HAR and not _icerik(a)]
        for oran in (0.25, 0.5, 0.75, 1.0):
            Hm = [(a, s_.translate(V(0.0, 0.0, STROK * oran * HAR[P2[a]["grup"]]))) for a, s_ in Hk]
            Hm = [(a, s_, s_.BoundingBox()) for a, s_ in Hm]
            b_, n_ = _tarama(Hm, hedef, esik=1.0); top_b += b_; top_a += n_
            if kol == "K3":
                b2_, n2_ = _tarama([h for h in Hm if P2[h[0]]["grup"] == "CEKMECE"], [h for h in Hm if P2[h[0]]["grup"] == "CEKMECE_ARA"], esik=1.0); top_b += b2_; top_a += n2_
        kontrol("%s STROK TARAMASI (%d hareketli parça × %s · strok %.0f × 0,25 / 0,5 / 0,75 / 1 · ara ray × %.2f · %d aday · %.0f sn): kesişim > 1 mm³ = %d"
                % (kol, len(Hk), ad_, STROK, RAY_ARA_ORAN, top_a, time.time() - t1, len(top_b)), not top_b, str(top_b[:5]))
    # ---- 10 · HAVADA PARÇA (denetim_temas_v1 · kapalı · v1 beyaz listesi: bilyeli ray ara elemanı) ----
    import denetim_temas_v1 as DT
    t1 = time.time()
    bl = {a for a in P2 if any(re.search(k_, a) for k_, _g in SC0.BEYAZ_LISTE)}
    hv = DT.havada([(a, SH[a]) for a in P2], haric=bl)
    DT.yaz(hv, baslik="HAVADA PARCA DENETIMI · h2_store_v1 (kapali · beyaz liste %d)" % len(bl))
    kontrol("HAVADA PARÇA = 0 (%d parça · kök %d · bağlı %d · beyaz liste %d ray ara elemanı · %.0f sn)" % (hv["parca"], hv["kok"], hv["bagli"], len(bl), time.time() - t1),
            not hv["bilesen"], str([d_["en"] for d_ in hv["bilesen"]][:6]))


if __name__ == "__main__":
    t0 = time.time()
    arg = sys.argv[1:]
    oz = modul()
    kimlik = (id(PARCALAR), id(SECOP_V1))
    ad1 = [p["ad"] for p in PARCALAR]; bb1 = [_bb(p) for p in PARCALAR]
    oz2 = modul()
    ad2 = [p["ad"] for p in PARCALAR]; bb2 = [_bb(p) for p in PARCALAR]
    idem = max(max(abs(a.xmin - b.xmin), abs(a.xmax - b.xmax), abs(a.ymin - b.ymin), abs(a.zmax - b.zmax)) for a, b in zip(bb1, bb2))
    print("h2_store_v1 · %d parça · modul() 2 kez %.0f sn" % (len(PARCALAR), time.time() - t0))
    print("ÖZ DENETİM (h2_store_v1)")
    kontrol("İDEMPOTENT: modul() 2 kez → %d = %d parça, adlar aynı sırada, en büyük sınır kutusu farkı %.1e · PARCALAR / SECOP_V1 nesnesi aynı · özet aynı (%d)"
            % (len(ad1), len(ad2), idem, len(oz2)), ad1 == ad2 and idem < 1e-9 and kimlik == (id(PARCALAR), id(SECOP_V1)) and oz == oz2)
    kap = {}
    for _k, t_, n_, _u, _a in oz:
        kap[t_] = kap.get(t_, 0) + n_
    kontrol("ÖZET (montaj SC_OZET yapısı): %d çekmece · pide %d · lahmacun %d · içecek %d · tatlı %d (2 gün kuralı 160 / 400 / 139 / 11)"
            % (len(oz), kap.get("hamur", 0), kap.get("lahm", 0), kap.get("ic1", 0), kap.get("tatli", 0)),
            len(oz) == 21 and (kap.get("hamur"), kap.get("lahm"), kap.get("ic1"), kap.get("tatli")) == (175, 420, 144, 12))
    print("SECOP_V1 (%d): %s" % (len(SECOP_V1), ", ".join(p["ad"] for p in SECOP_V1)))
    print("PANO_V1 (%d): %s" % (len(PANO_V1), ", ".join(p["ad"] for p in PANO_V1)))
    print("DEPO_V1 (%d): %s" % (len(DEPO_V1), ", ".join(p["ad"] for p in DEPO_V1)))
    print("K4_YAPI_V1 (%d): %s" % (len(K4_YAPI_V1), ", ".join(p["ad"] for p in K4_YAPI_V1)))
    print("GIDER_V1_KALKAN (%d): %s" % (len(GIDER_V1_KALKAN), ", ".join(p["ad"] for p in GIDER_V1_KALKAN)))
    print("GIDER v2: ana %s · sol %s · sag %s" % ([tuple(round(c, 3) for c in q) for q in GIDER["ana"]], [tuple(round(c, 3) for c in q) for q in GIDER["sol"]],
                                               [tuple(round(c, 3) for c in q) for q in GIDER["sag"]]))
    denetim(tarama="hizli" not in arg)
    kal = [d_ for d_ in DEN if not d_[1]]
    print("DENETİM: %d madde · %d KALDI · toplam %.0f sn" % (len(DEN), len(kal), time.time() - t0))
    sys.stdout.flush()
    os._exit(1 if kal else 0)
