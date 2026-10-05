# -*- coding: utf-8 -*-
"""HAT VERSİYON 2 · TOPPING v2 — İKİ KATLI (30 Eyl 2026 · Claude · YEREL).
Kemal: "topping istasyonunu iki raflı yaptık ki azalsın genişlik … ne kadar genişliği az o kadar iyi … saçma sapan mantık hataları yapma".

YÖNTEM (v1'in denetlenmiş parçaları kullanılır; yalnız değişmesi gerekenler yeniden çizilir):
  · SAĞ TARAF YERİNDE: fırına aktarma (2365,4), sabit bant tahriği, çıkış yarığı, soğutma grubu KLF6.6CND ve teknik bölme v1 ile aynı dünya x'inde.
  · SOL TARAF +507,5: A açıcı, tabla parkı (857,5), X motoru. TOPPING'den çıkan dilim = v1 dünya x 1106,5 … 1614; uzun prizmatik parçalar
    (tekne, kirişler, kayış, enerji zinciri kanalı, kırıntı çekmecesi, taban) bu dilim çıkarılarak kısalır.
  · SOĞUK KUTU YENİ: iç 1267,5 … 2440 × 1152 … 2140, İKİ KAT (üst raf 1572–1575, 304 3 mm, 38,5 bükümlü).
      ALT KAT: kıyma · kuşbaşı UNO + kaşar · küp sucuk kasetleri = v1 bloğu +1 mm (DX_ALT, 4 koşul aşağıda).
      ÜST KAT: sos + harç Beldos UNO (hortumla beslenebilen iki ürün: macun) + kaşar / sucuk 2 günlük yedeği (GN 1/1-200 + GN 1/2-150).
  · YAYICILAR mekanizma bandında EN SOLDA kalır (x 1396 · 1466): v1'deki gibi ürün tablaya ilk bunlardan dökülür (kıyma / kaşar konmuş pide
    yayıcı borusunun 6 mm altından geçemez). Yayıcılar 90° çevrildi (dağıtıcı boru z boyunca, tabla ekseninden arkaya): x'te 70 hatveye sığar;
    dönen tablada yarıçap boyunca olduğu için desen v1 ile aynı (tabla merkezi yayıcı ağzının altında durur, 1 tur).
  · ÜRÜN HORTUMLARI Ø32 (dış 42): üst kattaki UNO çıkışından SOĞUK KUTUNUN İÇİNDEN (hijyen: ürün hiç ılık bölgeye çıkmaz) üst raftan ve alt kat
    tabanından geçip yayıcının girişine iner. Sos hortumu x 1397,5 → 1396 (neredeyse dik); harç hortumu üst katta UNO'ların önünde x 1747,5 → 1466 yürür, sonra düz iner.
  · İSTASYON x'leri 4 koşulun kesişimi (ayrıntı DX_ALT satırında): sos 1396 · harç 1466 · kıyma 1596 · kuşbaşı 1806 · kaşar 2062 · sucuk 2311
    (ilk deneme sos 1420 / harç 1490 / blok +33: sucuk istasyonunda dönen kaset fırın yükleme bandının burnuna giriyordu — montaj denetimi yakaladı).
  · EVAPORATÖR KASETİ kuru bölmede 1778–2318 × 1383–1765: DÖNÜŞ kanalı (1450–1572) ALT KATTA, ÜFLEME kanalı (1592–1702) ÜST KATTA, raf ikisinin
    arasındaki 20 mm'lik bantta. Hava: üst katta öne → rafın önündeki 73 mm açıklıktan (flipper bölgesi) aşağı → alt katta arkaya → dönüş.
    İki kat da süpürülür (tek kaset, kısa devre yok).
Dünya ölçüleri: x hat boyunca, y yukarı, z derinlik (ön +79 · arka −830)."""
import io, math, os, sys, importlib.util as ilu

H2 = os.path.dirname(os.path.abspath(__file__)); U = os.path.dirname(H2)
for _p in (U, H2):
    if _p not in sys.path: sys.path.insert(0, _p)
import cadquery as cq
import h2_hesap_v1 as HS
import topping_cad_v32 as TC0
if not TC0.PARCALAR: TC0.modul()
_sp = ilu.spec_from_file_location("TU0_h2", os.path.join(U, "topping_uno_cad_v19.py"))
TU0 = ilu.module_from_spec(_sp); _sp.loader.exec_module(TU0)

V = cq.Vector
# ---------------------------------------------------------------- v2 ÖLÇÜLERİ (dünya)
DXL = HS.DXL                                  # 507,5 · sol grup sağa kayar
SL = HS.C_DILIM                               # (1106,5, 1614) TOPPING'den çıkan dilim (v1 dünya x)
XT = HS.C_X                                   # (1207,5, 2500)
H_UST = HS.H_UST                              # 2200
SAC = 1.5
Z_KABUK, Z_ON = TC0.Z_KABUK, TC0.Z_ON         # 39 · 79
DXW, DYW = TC0.DX_D, TC0.DY_D                 # TC yerel → dünya (700, 892)
# soğuk kutu (v1 sandviçi: iç 304 1,0 + PU 57,5 + dış 1,5 · yanlarda dış kabuk = TC yan sacı)
KX = (XT[0] + SAC, XT[1] - SAC)              # 1209 … 2498,5 (TC yan saclarının iç yüzü)
KY = (1109.0, H_UST - SAC)                    # 1109 (alt dış sac altı) … 2198,5 (TC dış tavanı altı)
IX = (KX[0] + 58.5, KX[1] - 58.5)            # iç 1267,5 … 2440
IY = (1152.0, KY[1] - 58.5)                   # iç taban 1152 … tavan 2140
IZ = (-570.0, 23.0)
assert abs(IY[1] - HS.T_IC_TAVAN) < 1e-9
RAF2 = HS.T_RAF_UST                           # (1572, 1575) üst kat rafı
DY_U = RAF2[1] - IY[0]                        # 423 · üst kat ünitelerinin yukarı kayması
RAF_ON_Z = -50.0                              # üst rafın ön kenarı: flipper katlanınca −34'e gelir (16 pay) · önündeki 73 mm hava dönüşünün iniş yolu
# istasyonlar (dünya x)
# v2 yerleşimi 4 koşulun kesişimi (montaj v2.1 ilk koşusundan · bantlı tabla kaseti istasyonda döner, süpürme R 223,7):
#   (1) sos istasyonunda kaset süpürmesi A duvarına ≥ 5 (sos 1420'de 34,6 ölçüldü → 1396'da ≈ 10,6)
#   (2) kıyma pidesinin dökülen halkası (x − 105) harç yayıcı borusunun (x + 20) sağında ≥ 5 → kıyma ≥ harç + 130
#   (3) harç hortumu (Ø42) kıyma haznesinin (sol kenarı kıyma − 95) solunda ≥ 5 → kıyma ≥ harç + 121
#   (4) sucuk istasyonunda kaset süpürmesi fırın yükleme bandının burnundan (2521,9) ≥ 5 → sucuk ≤ 2521,9 − 5 − 223,7 + 22,4 = 2315,6
#   → sos 1396 · harç 1466 · alt blok +1 (kıyma 1596 … sucuk 2311): (1) ≈ 10,6 · (2) 5 · (3) 14 · (4) 9,6 mm
#   (ilk deneme +33 / 1420 / 1490: (4) −22 → sucuk dönerken yükleme bandının burun rulosuna giriyordu — montaj yakaladı)
DX_ALT = 1.0
X_YAYICI = {"sos": 1396.0, "harc": 1466.0}
X_V1 = {"sos": 910.0, "harc": 1260.0}         # v1 UNO / yayıcı ekseni
X_UST = {"sos": 1397.5, "harc": 1747.5}      # üst kattaki UNO eksenleri (v1 aralığı 350 korunur, haznelerin arası 20)
DX_UST = {k: X_UST[k] - X_V1[k] for k in X_UST}   # +487,5 · +487,5
ISTASYON = {"SOS": X_YAYICI["sos"], "HARC": X_YAYICI["harc"], "KIYMA": 1595.0 + DX_ALT, "KUSBASI": 1805.0 + DX_ALT,
            "KASAR": 2061.0 + DX_ALT, "SUCUK": 2310.0 + DX_ALT}
# soğutma grubu (KLF6.6CND) hava yolu v2: sol kanat yalnız EMİŞ (5 yarık, ayırma perdesinin 1631,5 solunda) + C kaidesinin ARKA penceresi (h2_kaide_v1) ·
# sağ kanat ATIŞ (9 yarık, kaide atış pencereleri 1630–2090 · 2150–2450 önünde) · 65 hatve (v1 70) · emiş / atış yarıkları arası ≥ 250
IZGARA = {"emis": [1257.5 + 65.0 * i_ for i_ in range(5)], "atis": [1869.5 + 65.0 * i_ for i_ in range(9)]}   # 1257,5–1577,5 · 1869,5–2449,5
FIRE_DX = 1535.0 - 1470.0                     # fire sileceği yayıcılarla kıyma arasında (v1: harç ile kıyma arasında)
# kuru bölme v2 yerleşimi (kutunun sol alt köşesi, dünya) — v1 → v2 öteleme
EVAP_D = (1778.0 - 1470.0, 1383.0 - 1473.0, 0.0)          # kaset 1778–2318 × 1383–1765 (dönüş alt katta, üfleme üst katta) · x: harç UNO silindirinin (≤ 1766,5)
#   sağı ile, soğutma hatlarının kaşar (≤ 2090,6) | sucuk (≥ 2282,4) redüktörleri arasından çıkabildiği aralık (1769,5 … 1786,9) → 1778
KURU_YENI = {"evap_kaseti_": EVAP_D, "sogutma_emis_hatti_ic": EVAP_D, "sogutma_sivi_hatti_ic": EVAP_D,
             "kuru_pano_kutusu": (1215.0 - 900.0, 1880.0 - 1585.0, 0.0),        # pano 1215–1765 × 1880–2140 (en üstte, servis kapağının altında)
             "kuru_din_": (1215.0 - 2020.0, 1680.0 - 1600.0, 0.0),              # DIN plakası + UPS + güç kaynağı 1215–1425 × 1680–1840
             "kuru_ups": (1215.0 - 2020.0, 1680.0 - 1600.0, 0.0), "kuru_guc_kaynagi": (1215.0 - 2020.0, 1680.0 - 1600.0, 0.0),
             "kuru_surucu_": (1575.0 - 1170.0, 0.0, 0.0), "kuru_din_rayi_surucu": (1575.0 - 1170.0, 0.0, 0.0),
             "kuru_din_rayi_ayak_": (1575.0 - 1170.0, 0.0, 0.0)}                  # step sürücüleri 1575–1722 × 1432–1482 (valf adasının sağında)
TU_KURU = {"valf_": (1240.0 - 850.0, 0.0, 0.0),                                  # valf adası 1240–1548 (açıcı rakorlarına 32 mm hortum payı)
           "sartlandirici_": (2420.0 - 2350.0, 0.0, 0.0),                        # FRL 2420–2470: solu sucuk motorundan (2371) 49 · sağında ana hat iner
           "arka_hava_": EVAP_D, "arka_duvar_kaset_yuzu": EVAP_D}                  # kasetin arka duvardaki yüzü ve kanalları kasetle gider
# yeni hat güzergâhları (dünya)
ANA_V2 = [(3790.0, 1809.0, -380.0), (3790.0, 1809.0, -740.0), (2485.0, 1809.0, -740.0), (2485.0, 1167.0, -740.0), (2470.0, 1167.0, -740.0)]
ADA_V2 = [(2420.0, 1167.0, -740.0), (2390.0, 1167.0, -740.0), (2390.0, 1125.0, -740.0), (1560.0, 1125.0, -740.0), (1560.0, 1462.0, -740.0), (1548.0, 1462.0, -740.0)]
SOG_HAT = {"sogutma_emis_hatti": [(2013.0, 1050.0, -700.0), (2258.0, 1050.0, -700.0), (2258.0, 1383.0, -700.0)],
           "sogutma_sivi_hatti": [(2013.0, 1070.0, -660.0), (2236.0, 1070.0, -660.0), (2236.0, 1360.0, -660.0), (2236.0, 1360.0, -700.0), (2236.0, 1383.0, -700.0)]}
SOG_R = {"sogutma_emis_hatti": (15.5, 6.35), "sogutma_sivi_hatti": (3.175, 3.175)}   # dış r (emiş Cu Ø12,7 + Armaflex 9) · çıplak Cu r
TAHLIYE_V2 = [(2203.0, 1425.0, -775.0), (2203.0, 1350.0, -775.0), (2203.0, 1350.0, -805.0), (2203.0, 1372.0, -805.0), (2203.0, 1372.0, -815.0),
              (2203.0, 950.0, -815.0), (2120.0, 950.0, -815.0), (2120.0, 950.0, -770.0), (2120.0, 940.0, -770.0)]   # Ø8 · sifon 1350 → 1372 (22 mm su)
HORTUM = {"sos": [(1397.5, 1613.5, -235.0), (1397.5, 1613.5, -170.0), (1397.5, 1520.0, -170.0), (1396.0, 1440.0, -170.0), (1396.0, 1106.0, -170.0)],
          "harc": [(1747.5, 1613.5, -235.0), (1747.5, 1613.5, -170.0), (1466.0, 1613.5, -170.0), (1466.0, 1106.0, -170.0)]}
HORTUM_R = 21.0                                # Ø32 iç · Ø42 dış gıda hortumu (çelik spiral takviyeli [V])


# ---------------------------------------------------------------- yardımcılar
def kut(x0, x1, y0, y1, z0, z1):
    return cq.Solid.makeBox(abs(x1 - x0), abs(y1 - y0), abs(z1 - z0), V(min(x0, x1), min(y0, y1), min(z0, z1)))


def _sh(o):
    if isinstance(o, cq.Workplane):
        v = [q for q in o.vals() if isinstance(q, cq.Shape)]
        return v[0] if len(v) == 1 else cq.Compound.makeCompound(v)
    return o


def tasi(sh, dx=0.0, dy=0.0, dz=0.0):
    return _sh(sh).translate(V(dx, dy, dz))


def silx(y, z, r, x0, x1): return cq.Solid.makeCylinder(r, abs(x1 - x0), V(min(x0, x1), y, z), V(1, 0, 0))
def sily(x, z, r, y0, y1): return cq.Solid.makeCylinder(r, abs(y1 - y0), V(x, min(y0, y1), z), V(0, 1, 0))
def silz(x, y, r, z0, z1): return cq.Solid.makeCylinder(r, abs(z1 - z0), V(x, y, min(z0, z1)), V(0, 0, 1))


def boru(pts, r):
    return TU0.boru(pts, r)


def dilimle(sh):
    """v1 dünya şeklinden SL dilimini çıkarır: solu +DXL, sağı yerinde (uzun prizmatik parçalar)"""
    sh = _sh(sh); b = sh.BoundingBox()
    if b.xmax <= SL[0] + 1e-6: return tasi(sh, DXL)
    if b.xmin >= SL[1] - 1e-6: return sh
    sol = sh.intersect(kut(b.xmin - 10.0, SL[0], b.ymin - 10.0, b.ymax + 10.0, b.zmin - 10.0, b.zmax + 10.0))
    sag = sh.intersect(kut(SL[1], b.xmax + 10.0, b.ymin - 10.0, b.ymax + 10.0, b.zmin - 10.0, b.zmax + 10.0))
    ss = [s for s in ((tasi(sol, DXL) if sol.Volume() > 1e-6 else None), (sag if sag.Volume() > 1e-6 else None)) if s is not None]
    if not ss: return None
    if len(ss) == 1: return ss[0]
    try:
        return ss[0].fuse(ss[1]).clean()
    except Exception:
        return cq.Compound.makeCompound(ss)


def _rotY(sh, cx, cz, aci):
    return sh.rotate(V(cx, 0, cz), V(cx, 1, cz), aci)


def _ote(ad, tablo):
    for k in sorted(tablo, key=len, reverse=True):
        if ad.startswith(k): return tablo[k]
    return None


# ---------------------------------------------------------------- v1 parçaları (dünya)
def _v1_tc():
    L = []
    for p in TC0.PARCALAR:
        if TC0.eski(p["ad"]): continue
        d_ = TC0.V1_TASI.get(p["ad"], (0.0, 0.0, 0.0))
        sh = _sh(p["wp"]).translate(V(DXW + d_[0], DYW + d_[1], d_[2]))
        if p["ad"] == "cikis_yarigi_contasi":
            sh = _sh(TC0.kut(*TC0.YARIK_V2[0]).cut(TC0.kut(*TC0.YARIK_V2[1])))
        L.append(dict(ad=p["ad"], sh=sh, mal=p["mal"], bom=p.get("bom")))
    return L


def _v1_tu():
    return [dict(q, sh=q["sh"].translate(V(TU0.DX_DUNYA, TU0.DY_DUNYA, 0.0))) for q in TU0.P]


TC_YENI = ("dis_tavan", "dis_arka", "dis_yan_sol", "dis_yan_sag", "kuru_bolme_servis_kapagi", "lineer_ray_", "ray_ortu_",
           "onyuz_mekanizma_kanadi_", "onyuz_cerceve_mek_", "sogutma_emis_hatti", "sogutma_sivi_hatti", "evap_kaseti_tahliye_hortumu",
           "baglama_lamasi_3", "baglama_lamasi_4", "kuru_bolme_tabani")
TC_KAYDIR = {"tabla_bos_sensoru": (DX_ALT, 0.0, 0.0), "sensor_braketi_tabla_bos": (DX_ALT, 0.0, 0.0)}   # sucuk iniş borusu +33 → sensör de sağına (v1 bağıl yeri)
TU_ALT = ("kiyma", "kusbasi", "kasar", "sucuk", "yuva_", "mil_", "kovan_", "reduktor_", "motor_", "raf_kaset_contasi_",
          "raf_gecis_contasi_kiyma", "raf_gecis_contasi_kusbasi")
TU_DUS = ("tasiyici_raf_3mm", "raf_on_bukumu", "raf_arka_bukumu", "raf_kosebendi_", "raf_askisi_burclari_", "alt_yalitim_", "soguk_", "kabin_sol_duvar_PU",
          "kabin_sag_duvar_PU", "yalitim_blogu", "onyuz_", "gecis_blogu_yalitim", "hava_hatti_",
          "raf_gecis_contasi_sos", "raf_gecis_contasi_harc", "sos__agiz_90_derece", "harc__agiz_90_derece")
TU_YERINDE = TC0.V3_CIKAN                     # bağlam / kompresör / eski kabin / tabla_diski / pide: montaj kendi süzer — dokunulmaz


def _hortum_mu(ad):
    return "_hortum_" in ad or ad.endswith("_hava_hortumu") or ad.endswith("_hortumu")


RAPOR = dict(tc={}, tu={})
GRUP_KAYMA = {}                               # TU grup adı → öteleme (animasyon pivotları)


def _say(d, k): d[k] = d.get(k, 0) + 1


def _siniflandir():
    TC, TU = [], []
    say, sayu = RAPOR["tc"], RAPOR["tu"]
    for p in _v1_tc():
        a = p["ad"]
        if a.startswith(TC_YENI) and not a.endswith("_hatti_ic"):                              # yeniden çizilenler (kasetin içindeki hat uçları kasetle gider)
            _say(say, "yeni_yerine_dusen"); continue
        k = _ote(a, KURU_YENI)
        if k is not None:
            TC.append(dict(p, sh=tasi(p["sh"], *k), tur="kuru")); _say(say, "kuru_yeni_yer"); continue
        if a in TC_KAYDIR:
            TC.append(dict(p, sh=tasi(p["sh"], *TC_KAYDIR[a]), tur="kaydir")); _say(say, "kaydir"); continue
        if a.startswith("fire_silecegi_"):
            TC.append(dict(p, sh=tasi(p["sh"], FIRE_DX), tur="fire")); _say(say, "fire"); continue
        b = p["sh"].BoundingBox()
        tur = "sol" if b.xmax <= SL[0] + 1e-6 else ("sag" if b.xmin >= SL[1] - 1e-6 else "dilim")
        sh = dilimle(p["sh"])
        if sh is None:
            _say(say, "dilimde_kaldi"); continue
        _say(say, tur)
        TC.append(dict(p, sh=sh, tur=tur))
    for q in _v1_tu():
        a = q["ad"]; g = q["grup"]
        def kay(dx, dy=0.0, dz=0.0):
            if g != "SABIT":
                o = GRUP_KAYMA.setdefault(g, (dx, dy, dz))
                assert o == (dx, dy, dz), "grup %s iki farklı ötelemede: %s / %s (%s)" % (g, o, (dx, dy, dz), a)
            return tasi(q["sh"], dx, dy, dz)
        if a.startswith(TU_YERINDE):
            TU.append(q); _say(sayu, "yerinde"); continue
        if a.startswith(TU_DUS) or _hortum_mu(a):
            _say(sayu, "dus"); continue
        k = _ote(a, TU_KURU)
        if k is not None:
            TU.append(dict(q, sh=kay(*k))); _say(sayu, "kuru"); continue
        if a.startswith(("sos_spreader_", "harc_spreader_")):
            k = "sos" if a.startswith("sos") else "harc"
            assert g == "SABIT", "yayıcı parçası hareketli grupta: %s (%s) — 90° çevirme pivotu bozar" % (a, g)
            sh = tasi(_rotY(q["sh"], X_V1[k], TU0.ZT, 90.0), X_YAYICI[k] - X_V1[k])
            TU.append(dict(q, sh=sh)); _say(sayu, "yayici"); continue
        if a.startswith(("raf_gecis_contasi_sos", "raf_gecis_contasi_harc")):
            k = "sos" if "sos" in a else "harc"
            TU.append(dict(q, sh=kay(X_YAYICI[k] - X_V1[k]))); _say(sayu, "taban_contasi"); continue
        if a.startswith(("sos", "harc")):
            k = "sos" if a.startswith("sos") else "harc"
            TU.append(dict(q, sh=kay(DX_UST[k], DY_U))); _say(sayu, "ust_kat"); continue
        if a.startswith(TU_ALT):
            TU.append(dict(q, sh=kay(DX_ALT))); _say(sayu, "alt_kat"); continue
        sayu.setdefault("SINIFSIZ", []).append(a)
    return TC, TU


# ================================================================ YENİ TC PARÇALARI (dünya)
def _bom(ad, n, ozellik, not_):
    return (ad, n, ozellik, not_)


def yeni_tc():
    L = []
    def ek(ad, sh, mal, bom=None):
        L.append(dict(ad=ad, sh=_sh(sh), mal=mal, bom=bom, tur="yeni"))
    x0, x1 = XT
    # ---- 1 · DIŞ KABUK (304 1,5): tavan · kuru bölme servis kapağı · iki yan · arka ----
    ek("dis_tavan", kut(x0, x1, H_UST - SAC, H_UST, -630.0, Z_KABUK), "sac",
       _bom("Dış tavan sacı", 1, "304 1,5 mm · lazer + abkant · 1292,5 × 669", "v2 · iki katlı soğuk kutunun üstü (2198,5–2200) · makine üstü 2200"))
    ek("kuru_bolme_servis_kapagi", kut(x0, x1, H_UST - SAC, H_UST, -830.0, -630.0), "sac",
       _bom("Kuru bölme servis kapağı", 1, "304 1,5 mm · 1292,5 × 200 · kenarları bükülü · 8 × M5 perçin somun",
            "v2 · pano (üstte) + DIN / UPS + sürücüler + valf adası + evaporatör kaseti ÜSTTEN buradan"))
    for s in ("sol", "sag"):
        xa = x0 if s == "sol" else x1 - SAC
        ys = kut(xa, xa + SAC, 892.0 + SAC, H_UST - SAC, -830.0, Z_KABUK)
        xd = (xa + SAC, xa + SAC + 30.0) if s == "sol" else (xa - 30.0, xa)
        ys = ys.fuse(kut(xd[0], xd[1], 892.0 + SAC, H_UST - SAC, Z_KABUK - SAC, Z_KABUK))          # 30 mm ön dönüş (içe) — çerçeve + kapak menteşesi buna
        ys = ys.cut(kut(xa - 1.0, xa + SAC + 1.0, 893.0, 1042.0, -510.0, 5.0))                    # tabla + ürün geçişi (v1 yerel 1–150)
        ys = ys.cut(kut(xa - 1.0, xa + SAC + 1.0, 893.0, 958.0, -510.0, -1.0))                    # mekanizma geçişi (v1 yerel 1–66)
        if s == "sag":
            ys = ys.cut(silx(TC0.RAKOR_ANA[0] + DYW, TC0.RAKOR_ANA[1], 7.0, xa - 1.0, xa + SAC + 1.0))
        else:
            for ry, rz in TC0.RAKOR_ACICI:
                ys = ys.cut(silx(ry + DYW, rz, 6.0, xa - 1.0, xa + SAC + 1.0))
        ek("dis_yan_" + s, ys, "sac", _bom("Dış yan sac", 2, "304 1,5 mm · lazer + abkant · 1306,5 yüksek · 30 ön dönüş",
                                          "komşu modüle cıvatalanır (lego birleşim) · v2: 2200'e kadar") if s == "sol" else None)
    ek("dis_arka", kut(x0 + SAC, x1 - SAC, 892.0 + SAC, H_UST - SAC, -830.0, -830.0 + SAC), "sac",
       _bom("Dış arka sac", 1, "304 1,5 mm · 1289,5 × 1305", "kuru bölmenin arkası; kablo rakorları burada"))
    # ---- 2 · LİNEER KIZAK (MGN15H) + KAPALI RAY ÇATISI: tek parça ray (sol uç 507,5 kısaldı → 1826 ≤ 1960) ----
    rx0, rx1 = TC0.RAY2_X[0] + DXL, TC0.RAY2_X[1]                                               # yerel −32,5 … 1793,5
    n_top = 0
    for ad_, zc_ in (("on", -65.0), ("arka", -275.0)):
        r_, cv_, n_, E_ = _mgn_ray_tek(rx0, rx1, zc_)
        n_top += n_
        ek("lineer_ray_%s" % ad_, tasi(r_, DXW, DYW), "celik",
           _bom("Lineer ray %s × %.1f (TEK PARÇA)" % (TC0.MGNR["ad"], rx1 - rx0), 2, "paslanmaz · %s" % TC0.MGNR["kaynak"],
                "v2 · sol uç 507,5 kısaldı → tek parça (ek yok) · ray kirişine %s · uç payları %s" % (TC0.MGNR["civata"], E_)) if ad_ == "on" else None)
        ek("lineer_ray_%s_civatalari" % ad_, tasi(cv_, DXW, DYW), "celik",
           _bom("Cıvata %s · A2 paslanmaz (ray bağlantısı)" % TC0.MGNR["civata"], 2 * n_, "havşa Ø6 × 4,5 dibinde · hatve 40 · uçtan 15", "ray kirişine (dişli)") if ad_ == "on" else None)
    _cx = TC0.CATI_X
    TC0.CATI_X = (rx0 - 1.5, TC0.CATI_X[1])
    try:
        for ad_, zc_ in (("on", -65.0), ("arka", -275.0)):
            ek("ray_ortu_catisi_%s" % ad_, tasi(TC0.ray_catisi(zc_), DXW, DYW), "sac",
               _bom("Ray çatısı · AISI 304 1,5 tek parça bükme", 2, "boy %.1f · kirişe vidalı ayak + dış etek · üst 3° dışa eğimli · iç damlama eteği" % (TC0.CATI_X[1] - TC0.CATI_X[0]),
                    "v32/v2 · üstte yarık yok · kızak ayakları iç eteğin altından dolanır (ters kap labirent)") if ad_ == "on" else None)
            for u_, (xa_, xe_) in (("sol", (TC0.CATI_X[0], rx0)), ("sag", (rx1, TC0.CATI_X[1]))):
                ek("ray_ortu_kapagi_%s_%s" % (ad_, u_), tasi(TC0.ray_catisi_kapagi(zc_, xa_, xe_), DXW, DYW), "sac",
                   _bom("Ray çatısı uç kapağı · AISI 304 1,5", 4, "çatının iç kesitini kapatır", "ray ucu kapalı") if (ad_, u_) == ("on", "sol") else None)
    finally:
        TC0.CATI_X = _cx
    # ---- 3 · BAĞLAMA LAMALARI: v1 0–2 sola kayar (+507,5), 5–8 yerinde; dilimde kalan 3 + 4 yerine TEK lama aralığın ortasına (587,5 … 980 → 783,75) ----
    xb = ((587.5 + 40.0) + 980.0) / 2.0 - 20.0                                                  # 627,5 ile 980'in ortası 803,75 → lama 783,75–823,75 (yerel)
    ek("baglama_lamasi_3", tasi(kut(xb, xb + 40.0, 4.5, 20.5, -335.0, -305.0), DXW, DYW), "celik")
    # ---- 4 · ÖN ÇERÇEVE (30 × 20 × 2, z +39…+59) + MEKANİZMA KANATLARI (tava, derz 3) — soğuk kapaklarla aynı bölüm çizgisi 1851,5 | 1854,5 ----
    MEK_Y = (791.0, 1107.5); MEK_PY = (TC0.MEK_PAN_Y0, 1107.5)
    DERZ = (1851.5, 1854.5); XO = (DERZ[0] + DERZ[1]) / 2.0 - 15.0                               # orta dikme 1838–1868
    zc0, zc1 = TC0.Z_CER_C
    CER = [("onyuz_cerceve_mek_sol_dikme", TC0.boru_y(x0 + SAC, x0 + SAC + 30.0, zc0, zc1, MEK_Y[0], MEK_Y[1])),
           ("onyuz_cerceve_mek_sag_dikme", TC0.boru_y(x1 - SAC - 30.0, x1 - SAC, zc0, zc1, MEK_Y[0], MEK_Y[1])),
           ("onyuz_cerceve_mek_alt_kayit", TC0.boru_x(MEK_Y[0], MEK_Y[0] + 30.0, zc0, zc1, x0 + SAC + 30.0, x1 - SAC - 30.0)),
           ("onyuz_cerceve_mek_ust_kayit", TC0.boru_x(MEK_Y[1] - 30.0, MEK_Y[1], zc0, zc1, x0 + SAC + 30.0, x1 - SAC - 30.0)),
           ("onyuz_cerceve_mek_orta_dikme_alt", TC0.boru_y(XO, XO + 30.0, zc0, zc1, MEK_Y[0] + 30.0, 965.0).union(TC0.kut(XO, XO + 30.0, 963.0, 965.0, zc0, zc1))),
           ("onyuz_cerceve_mek_orta_dikme_ust", TC0.boru_y(XO, XO + 30.0, zc0, zc1, 1012.0, MEK_Y[1] - 30.0).union(TC0.kut(XO, XO + 30.0, 1012.0, 1014.0, zc0, zc1)))]
    for i_, (a_, w_) in enumerate(CER):
        ek(a_, w_, "celik", _bom("C ön çerçevesi 30 × 20 × 2 AISI 304 dikdörtgen profil · kaynaklı", len(CER),
                                 "mekanizma bandı (6 parça) · z +39…+59 · yan sacların ön dönüşüne M6", "gizli menteşe + bas-aç mandallar bu çerçeveye") if i_ == 0 else None)
    # soğutma grubu ızgarası (kaide hizası 826–886): EMİŞ ayırma perdesinin (1631,5) SOLUNDA (kaide emiş penceresi 1257,5–1614) ·
    # ATIŞ sağında (kaide atış pencereleri 1630–2090 · 2150–2450) · arada 102,5 dolu (kısa devre yok)
    IZ_EMIS, IZ_ATIS = IZGARA["emis"], {"sol": [], "sag": IZGARA["atis"]}
    yar = {"sol": [(x_, x_ + 60.0, y_, y_ + 6.0) for x_ in IZ_EMIS + IZ_ATIS["sol"] for y_ in TC0.IZGARA_Y],
           "sag": [(x_, x_ + 60.0, y_, y_ + 6.0) for x_ in IZ_ATIS["sag"] for y_ in TC0.IZGARA_Y]}
    PAN = [("onyuz_mekanizma_kanadi_sol", (x0 + SAC, DERZ[0], MEK_PY[0], MEK_PY[1]), "sol"),
           ("onyuz_mekanizma_kanadi_sag", (DERZ[1], x1 - 3.0, MEK_PY[0], MEK_PY[1]), "sag")]
    for a_, (px0, px1, py0, py1), mt_ in PAN:
        ek(a_, TC0.tava(px0, px1, py0, py1, tuple(yar[mt_])), "sac",
           _bom("%s · tava 20 · AISI 304 fırçalı 1,5" % a_.replace("onyuz_", ""), 1,
                "%.1f × %.1f · %d lazer yarık 60 × 6 alt bantta (kaide hizası · soğutma grubu havası)" % (px1 - px0, py1 - py0, len(yar[mt_])),
                "gizli menteşe %s · bas-aç · kaide bandını (788–892) da örter · v2: soğuk kapaklarla aynı derz (1851,5 | 1854,5)" % mt_))
        ek(a_ + "_omega", TC0.omega_pz(px0 + 3.0, px1 - 3.0, 949.0, Z_ON - 1.5, -1.0), "celik",
           _bom("Panel omegası 1,0 · 40 × 15", 2, "AISI 304 1,0 · yüz sacının arkasına punta", "") if mt_ == "sol" else None)
        xm = (px0 + 2.5, px0 + 27.5) if mt_ == "sol" else (px1 - 27.5, px1 - 2.5)
        for j_, ym in enumerate((py0 + 40.0, py1 - 110.0)):
            ek("%s_mentese_%d" % (a_, j_), kut(xm[0], xm[1], ym, ym + 70.0, TC0.Z_PAN_C[0] + 3.0, Z_ON - 1.5), "celik",
               _bom("Gizli menteşe · çok kollu, sanal dönme merkezi panelin ön dış köşesi", 4, "AISI 304 · ürün + parça no VARSAYIM", "") if (mt_ == "sol" and j_ == 0) else None)
            xt = (px0 + 20.5, px0 + 27.5) if mt_ == "sol" else (px1 - 27.5, px1 - 20.5)
            ek("%s_mentese_%d_taban" % (a_, j_), kut(xt[0], xt[1], ym, ym + 70.0, TC0.Z_PAN_C[0], TC0.Z_PAN_C[0] + 3.0), "celik")
        xbs = (px1 - 27.0, px1 - 2.0) if mt_ == "sol" else (px0 + 2.0, px0 + 27.0)
        ek(a_ + "_basac", kut(xbs[0], xbs[1], 1082.5, 1102.5, TC0.Z_PAN_C[0], Z_ON - 1.5), "plastik",
           _bom("Bas-aç mandal (push-to-open, gizli) · Southco E4 touch latch", 2, "parça no + ölçü VARSAYIM", "kulpsuz kapak") if mt_ == "sol" else None)
    ek("onyuz_mekanizma_kanadi_sol_filtre", kut(IZ_EMIS[0] - 5.0, IZ_EMIS[-1] + 65.0, 823.0, 886.0, TC0.Z_PAN_C[0] + 3.0, Z_ON - 1.5), "pom",
       _bom("Kondenser emiş filtresi · yıkanabilir paslanmaz tel örgü + çerçeve", 1, "%.0f × 63 × 15,5 · sol kanadın alt bandında 2 klipsle" % (IZ_EMIS[-1] + 70.0 - IZ_EMIS[0]),
            "yalnız EMİŞ yarıklarının arkasında · ayda 1 yıkanır (VARSAYIM)"))
    # ---- 5 · SOĞUTMA HATLARI (ünite servis vanaları SAĞ yüzde [V: föy] → teknik bölmede 1050'de sağa → kaşar | sucuk motorlarının arasından kasete) ----
    for a_, pts in SOG_HAT.items():
        r_dis, r_cu = SOG_R[a_]
        ek(a_, boru(pts, r_dis), "bakir" if a_.endswith("sivi_hatti") else "koyu",
           _bom("Soğutma hattı %s" % ("emiş Cu Ø12,7 + Armaflex 9" if "emis" in a_ else "sıvı Cu Ø6,35"), 1, "ünite → evaporatör kaseti · lehimli",
                "v2 · kaşar (≤2122) ile sucuk (≥2315) motorlarının arasından dik çıkar · soğutmacı firma kesinleştirecek"))
    kt = kut(x0 + SAC, 2420.0, 1107.5, 1109.0, -828.5, -630.0)
    for x_, z_, r_ in ((2258.0, -700.0, 16.5), (2236.0, -660.0, 4.2), (2203.0, -815.0, 5.0)):
        kt = kt.cut(sily(x_, z_, r_, 1106.0, 1110.0))
    ek("kuru_bolme_tabani", kt, "sac", _bom("Kuru bölme tabanı 304 1,5", 1, "1211 × 198,5 · soğutma hatları + tahliye geçiş delikleri (lastik bilezikli)", "v2 · teknik bölmenin üstü"))
    ek("evap_kaseti_tahliye_hortumu", boru(TAHLIYE_V2, 4.0), "silikon",
       _bom("Kaset tahliye hortumu Ø8 silikon", 1, "sifonlu (22 mm su) · kaşar | sucuk motorlarının arasından iner", "ucu yoğuşma tavasının üstünde (hava boşluklu)"))
    return L


def _mgn_ray_tek(x0, x1, zc):
    """MGNR15R tek parça (TC0.mgn_ray'in iki parçalı sürümünün tek parçası): uçtan E 15 · hatve 40 · havşa + geçme delik + DIN 912 M3 × 10"""
    M = TC0.MGNR; Yk, Yr = TC0.Y_KIRIS, TC0.Y_RAY
    p_ = TC0.kut(x0, x1, Yk, Yr, zc - M["WR"] / 2.0, zc + M["WR"] / 2.0)
    for s_ in (-1.0, 1.0):
        p_ = p_.cut(TC0.kut(x0 - 1.0, x1 + 1.0, Yr - 3.7, Yr - 1.3, zc + s_ * M["WR"] / 2.0 - 1.0, zc + s_ * M["WR"] / 2.0 + 1.0))
    xd = x0 + M["E"]; son = xd; cv = None; n = 0
    while xd <= x1 - M["E_min"] + 1e-6:
        p_ = p_.cut(TC0.sily(xd, zc, M["D"] / 2.0, Yr - M["h"], Yr + 1.0)).cut(TC0.sily(xd, zc, M["d"] / 2.0, Yk - 1.0, Yr))
        al = cq.Workplane("XZ").center(xd, zc).polygon(6, 2.5 / math.cos(math.radians(30.0))).extrude(-1.5).translate((0, Yr - M["h"] + 3.0 - 1.5, 0))
        b2 = TC0.sily(xd, zc, 2.75, Yr - M["h"], Yr - M["h"] + 3.0).cut(al).union(TC0.sily(xd, zc, 1.5, Yk, Yr - M["h"]))
        cv = b2 if cv is None else cv.union(b2); n += 1; son = xd; xd += M["P"]
    return p_, cv, n, [(round(M["E"], 2), round(x1 - son, 2), round(x1 - x0, 2))]


# ================================================================ YENİ TU PARÇALARI (dünya) — soğuk kutu
TU0.M.setdefault("hortum_gida", ((0.93, 0.93, 0.90, 1.0), 0.0, 0.45, False))
TU0.M.setdefault("gn", ((0.82, 0.84, 0.87, 1.0), 0.9, 0.3, False))
TU0.M.setdefault("kasar_urun", ((0.98, 0.90, 0.62, 1.0), 0.0, 0.8, False))
TU0.M.setdefault("sucuk_urun", ((0.62, 0.20, 0.14, 1.0), 0.0, 0.7, False))


def yeni_tu(TUm):
    """TUm: taşınmış TU ünite parçaları (delikleri onlara göre açılır)"""
    L = []
    def ek(ad, sh, mal, not_="", grup="SABIT", kaynak="V2"):
        assert mal in TU0.M, mal
        L.append(dict(ad=ad, sh=_sh(sh), mal=mal, kaynak=kaynak, grup=grup, not_=not_))
    bul = {q["ad"]: q["sh"] for q in TUm}
    X0, X1 = KX; ZF = IZ[1]                                                                      # 1209 … 2498,5 · ön zarf +23
    # ---- (a) ARKA DUVAR + TAVAN: dış sac 1,5 (kuru bölmeye bakar) + PU 57,5 TEK KÖPÜK + iç sac 1,0 ----
    arka_dis = kut(X0, X1, KY[0], KY[1], -630.0, -628.5)
    pu = kut(X0, X1, KY[0] + 1.5, KY[1], -628.5, -571.0).fuse(kut(X0, X1, IY[1] + 1.0, KY[1], -571.0, ZF))
    ic = kut(IX[0] - 1.0, IX[1] + 1.0, KY[0] + 1.5, IY[1] + 1.0, -571.0, ZF).cut(kut(IX[0], IX[1], KY[0], IY[1], -570.0, ZF + 1.0))
    # duvar geçişleri: UNO mil kovanları + kaset kovanları (katılarıyla) · kaset yüzü kesiği · hortum geçiş blokları
    KAS_YUZ = (1492.0 + EVAP_D[0], 1988.0 + EVAP_D[0], 1495.0 + EVAP_D[1], 1833.0 + EVAP_D[1])        # 1812–2308 × 1405–1743
    GB = {"alt": (1560.0, 1780.0, 1272.0, 1302.0), "ust": (1290.0, 1790.0, 1700.0, 1730.0)}
    delik = [kut(KAS_YUZ[0], KAS_YUZ[1], KAS_YUZ[2], KAS_YUZ[3], -631.0, -569.0)]
    delik += [kut(g[0], g[1], g[2], g[3], -631.0, -569.0) for g in GB.values()]
    for a, s in bul.items():
        if a.endswith("mil_gecis_kovani") or a.startswith("kovan_"):
            b = s.BoundingBox()
            delik.append(silz((b.xmin + b.xmax) / 2.0, (b.ymin + b.ymax) / 2.0, max(b.xlen, b.ylen) / 2.0, -631.0, -569.0))
    for d in delik:
        arka_dis = arka_dis.cut(d); pu = pu.cut(d); ic = ic.cut(d)
    # yan duvar PU (57,5 · TC yan sacının içinde) + raf askısı GFRP burçları (alt kat 1128,25 · üst kat 1550,5)
    BURC = {"alt": (1128.25, (-520.0, -360.0, -200.0, -40.0), (-567.0, 20.0)), "ust": (1550.5, (-520.0, -360.0, -200.0, -90.0), (-567.0, RAF_ON_Z - 3.0))}
    for yn, (xa, xb) in (("sol", (X0, IX[0] - 1.0)), ("sag", (IX[1] + 1.0, X1))):
        w = kut(xa, xb, KY[0] + 1.5, IY[1] + 1.0, -571.0, ZF)
        for kat, (by, bzs, _z) in BURC.items():
            for bz in bzs:
                w = w.cut(silx(by, bz, 8.0, xa - 1.0, xb + 1.0))
        ek("kabin_%s_duvar_PU" % yn, w, "pu", "v2 · yan duvar PU 57,5 (40 kg/m³) · iç sacla TC yan sacı arasında · 1110,5–2141 · 8 × GFRP burç yuvası Ø16")
    # kaset penceresi: iki POM kanalın dışında kalan boşluk PU ile dolar (v2: dönüş ALT katta, üfleme ÜST katta → aradan kısa devre olmamalı)
    kn_ = [bul[a].BoundingBox() for a in ("arka_hava_kanali_ust", "arka_hava_kanali_alt")]
    dol = kut(KAS_YUZ[0], KAS_YUZ[1], KAS_YUZ[2], KAS_YUZ[3], -628.5, -570.0)
    for b in kn_:
        dol = dol.cut(kut(b.xmin, b.xmax, b.ymin, b.ymax, -631.0, -569.0))
    ek("kaset_penceresi_dolgusu", dol, "pu", "v2 · kaset penceresinde kanalların dışı PU 57,5 · kanallar arası 20 mm bant (üst raf hizası) kapalı: üfleme (üst kat) ile dönüş (alt kat) arasında kısa devre yok")
    ek("yalitim_blogu", pu, "pu", "v2 · PU 57,5 TEK KÖPÜK: arka duvar + tavan · 4 UNO + 4 kaset kovanı + 2 hortum geçiş bloğu + kaset yüzü (%.0f × %.0f) kesiği"
       % (KAS_YUZ[1] - KAS_YUZ[0], KAS_YUZ[3] - KAS_YUZ[2]))
    ek("soguk_arka_dis_sac", arka_dis, "paslanmaz", "v2 · arka duvarın dış kabuğu AISI 304 1,5 · 1289,5 × 1089,5 · kovan / blok delikleri + kaset yüzü kesiği")
    ek("soguk_ic_kaplama", ic, "paslanmaz", "v2 · iç kaplama AISI 304 1,0: yanlar + tavan + arka tek parça (köşeler R) · iç 1172,5 × 988 × 593")
    # ---- (b) ALT KAT TABANI: alt dış sac 1,5 + PU 38,5 + taşıyıcı raf 3 (bükümlü) + köşebentler + burçlar ----
    alt_sac = kut(X0, X1, KY[0], KY[0] + 1.5, -628.5, ZF)
    alt_pu = kut(IX[0] + 3.0, IX[1] - 3.0, KY[0] + 1.5, 1149.0, -567.0, 20.0)
    raf = kut(IX[0], IX[1], 1149.0, 1152.0, -570.0, ZF)
    buk = [kut(IX[0], IX[1], KY[0] + 1.5, 1149.0, 20.0, ZF), kut(IX[0], IX[1], KY[0] + 1.5, 1149.0, -570.0, -567.0)]
    for k_ in ("KIYMA", "KUSBASI"):                                                              # UNO dirsekleri Ø36 ↔ konta ↔ raf deliği Ø42
        raf = raf.cut(sily(ISTASYON[k_], TU0.ZT, 21.0, 1148.0, 1153.0))
    for k_, x_ in X_YAYICI.items():                                                              # ürün hortumu Ø42 ↔ konta ↔ raf deliği Ø48
        raf = raf.cut(sily(x_, TU0.ZT, HORTUM_R + 3.0, 1148.0, 1153.0))
        ek("raf_gecis_contasi_%s" % k_, sily(x_, TU0.ZT, HORTUM_R + 3.0, 1149.0, 1152.0).cut(sily(x_, TU0.ZT, HORTUM_R, 1148.0, 1153.0)), "conta",
           "v2 · silikon grommet Ø48 / Ø42 · %s ürün hortumu alt kat tabanından yayıcıya iner" % k_)
    for _ad, _mod, _x0, _x1 in TU0.KASET:                                                        # kaset tüpü: delik Ø60 + öne açık U-yarık (yarık dili doldurur) · v1 ile aynı
        xc = (_x0 + _x1) / 2.0 + TU0.DX_DUNYA + DX_ALT; r_ = TU0.KAS_R[_mod][0]; kz = TU0.KAS_Z
        raf = raf.cut(sily(xc, kz, r_, 1148.0, 1153.0)).cut(kut(xc - r_, xc + r_, 1148.0, 1153.0, kz, ZF + 1.0))
        buk[0] = buk[0].cut(kut(xc - r_, xc + r_, 1143.0, 1150.0, 19.0, ZF + 1.0))
        alt_pu = alt_pu.cut(kut(xc - r_, xc + r_, 1143.0, 1150.0, kz - r_ - 3.0, 21.0))
    KL = {}
    for yn, xa, sg in (("sol", IX[0], 1.0), ("sag", IX[1], -1.0)):
        a_, b_ = sorted((xa, xa + sg * 40.0)); c_, d_ = sorted((xa, xa + sg * 3.0))
        KL[yn] = kut(a_, b_, 1146.0, 1149.0, -567.0, 20.0).fuse(kut(c_, d_, KY[0] + 1.5, 1149.0, -567.0, 20.0))
        alt_pu = alt_pu.cut(KL[yn])
    # taban geçişleri: konta yuvaları (raf) · iniş boruları / huniler / UNO dirsekleri / hortumlar (PU + alt sac)
    for a, s in bul.items():
        b = s.BoundingBox()
        if not (b.ymin < 1152.0 - 0.1 and b.ymax > 1109.0 + 0.1 and b.xmin < IX[1] and b.xmax > IX[0] and b.zmax > -570.0 and b.zmin < ZF): continue
        if a.startswith(("raf_gecis_contasi_", "raf_kaset_contasi_")) or "yarik_dili" in a or a.endswith("__cikis_tupu"): continue   # raf delikleri yukarıda (v1 kurgusu)
        dil = s.intersect(kut(b.xmin - 1.0, b.xmax + 1.0, KY[0] - 1.0, 1149.0, b.zmin - 1.0, b.zmax + 1.0))
        if dil.Volume() < 1e-3: continue
        d = dil.BoundingBox()                                                                    # yalnız alt PU + alt sacın içinden geçen kısım (+1 pay)
        kk = kut(d.xmin - 1.0, d.xmax + 1.0, KY[0] - 1.0, 1149.5, d.zmin - 1.0, d.zmax + 1.0)
        alt_pu = alt_pu.cut(kk); alt_sac = alt_sac.cut(kk)
    for k, x_ in X_YAYICI.items():                                                               # ürün hortumları tabanı dikine geçer (konta rafta)
        c = sily(x_, TU0.ZT, HORTUM_R + 0.5, KY[0] - 1.0, 1149.5)
        alt_pu = alt_pu.cut(c); alt_sac = alt_sac.cut(c)
    ek("alt_yalitim_saci", alt_sac, "paslanmaz", "v2 · soğuk kutunun alt dış sacı AISI 304 1,5 · 1289,5 × 651,5 · kontaların altında geçiş delikleri")
    ek("alt_yalitim_PU", alt_pu, "pu", "v2 · alt kat tabanı PU 38,5")
    ek("tasiyici_raf_3mm", raf, "paslanmaz", "v2 · ALT KAT TABANI 304 3 mm · 1172,5 × 593 · kıyma / kuşbaşı UNO + kaşar / sucuk kaseti bunun üstünde · geçişlerde konta")
    ek("raf_on_bukumu", buk[0], "paslanmaz", "v2 · rafın ön bükümü 38,5 (rafla tek parça)")
    ek("raf_arka_bukumu", buk[1], "paslanmaz", "v2 · rafın arka bükümü 38,5 (rafla tek parça)")
    for yn in ("sol", "sag"):
        ek("raf_kosebendi_%s" % yn, KL[yn], "paslanmaz", "v2 · L 40 × 40 × 3 AISI 304 · alt kat rafı yatay koluna oturur · 4 × M8 GFRP burçtan TC yan sacına")
    # ---- (c) ÜST KAT RAFI 1572–1575 (304 3, ön + arka 38,5 büküm) + köşebentler: açıklık 1172,5 · yük ≈150 kg (harç UNO + dolu hazne ≈80 · sos ≈35 · GN ≈35) ----
    #      kesit (3 × 520 + 2 × 38,5 büküm): I ≈ 1,18e5 mm⁴, W ≈ 3130 mm³ → σ ≈ 69 MPa (304 akma 205 → emniyet 3) · sehim ≈ 1,4 mm [H]
    RZ0, RZ1 = IZ[0], RAF_ON_Z
    ust = kut(IX[0], IX[1], RAF2[0], RAF2[1], RZ0, RZ1)
    ubuk = [kut(IX[0], IX[1], RAF2[0] - 38.5, RAF2[0], RZ1 - 3.0, RZ1),
            kut(IX[0], IX[1], RAF2[0] - 38.5, RAF2[0], RZ0, RZ0 + 3.0).cut(kut(KAS_YUZ[0] + 28.0, KAS_YUZ[1] - 88.0, RAF2[0] - 40.0, RAF2[0] + 1.0, RZ0 - 1.0, RZ0 + 4.0))]
    UK = {}
    for yn, xa, sg in (("sol", IX[0], 1.0), ("sag", IX[1], -1.0)):
        a_, b_ = sorted((xa, xa + sg * 40.0)); c_, d_ = sorted((xa, xa + sg * 3.0))
        UK[yn] = kut(a_, b_, RAF2[0] - 3.0, RAF2[0], RZ0 + 3.0, RZ1 - 3.0).fuse(kut(c_, d_, RAF2[0] - 40.0, RAF2[0] - 3.0, RZ0 + 3.0, RZ1 - 3.0))
    UH = {}                                                                                      # hortumların üst raftan geçtiği nokta (dik segment rafı keser)
    for k, pts in HORTUM.items():
        for a, b in zip(pts[:-1], pts[1:]):
            if min(a[1], b[1]) < RAF2[0] and max(a[1], b[1]) > RAF2[1]:
                t = (RAF2[1] - a[1]) / (b[1] - a[1]) if abs(b[1] - a[1]) > 1e-9 else 0.0
                UH[k] = (a[0] + t * (b[0] - a[0]), a[2] + t * (b[2] - a[2]))
    for k, (hx, hz) in UH.items():
        ust = ust.cut(sily(hx, hz, HORTUM_R + 1.0, RAF2[0] - 1.0, RAF2[1] + 1.0))
        ek("ust_raf_gecis_contasi_%s" % k, sily(hx, hz, HORTUM_R + 1.0, RAF2[0], RAF2[1]).cut(sily(hx, hz, HORTUM_R, RAF2[0] - 1.0, RAF2[1] + 1.0)), "conta",
           "v2 · üst raftan hortum geçiş kontası silikon Ø44/Ø42 · hortum sökülünce tapa takılır")
    ek("ust_raf_3mm", ust, "paslanmaz", "v2 · ÜST KAT RAFI AISI 304 3 · 1172,5 × 520 · sos + harç UNO + kaşar / sucuk GN yedeği · ön kenarı −50 (flipper + hava inişi) · "
       "açıklık 1172,5 · ≈150 kg → σ ≈ 69 MPa · sehim ≈ 1,4 mm [H]")
    ek("ust_raf_on_bukumu", ubuk[0], "paslanmaz", "v2 · üst rafın ön bükümü 38,5 (rafla tek parça)")
    ek("ust_raf_arka_bukumu", ubuk[1], "paslanmaz", "v2 · üst rafın arka bükümü 38,5 · kaset dönüş kanalının önünde çentikli (hava alt kattan kasete)")
    for yn in ("sol", "sag"):
        ek("ust_raf_kosebendi_%s" % yn, UK[yn], "paslanmaz", "v2 · L 40 × 40 × 3 AISI 304 · üst raf yatay koluna oturur · 4 × M8 GFRP burçtan TC yan sacına · uç başına ≈0,75 kN")
    for kat, (by, bzs, _z) in BURC.items():
        for yn, (xa, xb) in (("sol", (X0, IX[0] - 1.0)), ("sag", (IX[1] + 1.0, X1))):
            bc = None
            for bz in bzs:
                b_ = silx(by, bz, 8.0, xa, xb).cut(silx(by, bz, 4.5, xa - 1.0, xb + 1.0))
                bc = b_ if bc is None else bc.fuse(b_)
            ek("%sraf_askisi_burclari_%s" % ("" if kat == "alt" else "ust_", yn), bc, "pom",
               "v2 · 4 × ısı köprüsü kesici burç GFRP Ø16/Ø9 × 57,5 · raf köşebendini TC yan sacına bağlayan M8 A2 cıvata içinden geçer")
    # ---- (d) ÖN YÜZ: 430 çerçeve sacı + soğuk kapaklar K1 / K2 (eşit 642,5) + flipper — v1 kurgusu (topping_uno_cad_v19 5b) yeni ölçüde ----
    xu, yu = TU0.xu, TU0.yu
    DERZ = (1851.5, 1854.5)
    cer_d = [(X0, KY[0]), (X1, KY[0]), (X1, KY[1]), (X0, KY[1])]
    ag = [(IX[0], IY[0]), (IX[1], IY[0]), (IX[1], IY[1]), (IX[0], IY[1])]
    cer = cq.Workplane("XY", origin=(0, 0, TU0.Z_CER[0])).polyline(cer_d).close().extrude(1.0)
    cer = cer.cut(cq.Workplane("XY", origin=(0, 0, TU0.Z_CER[0] - 1.0)).polyline(ag).close().extrude(3.0))
    for _ad, _mod, _x0, _x1 in TU0.KASET:
        xc = (_x0 + _x1) / 2.0 + TU0.DX_DUNYA + DX_ALT; r = TU0.KAS_R[_mod][0] + 1.0
        cer = cer.cut(TU0.kut(xc - r, xc + r, 1143.0, IY[0] + 1.0, TU0.Z_CER[0] - 1.0, TU0.Z_CER[1] + 1.0))
    ek("onyuz_soguk_cerceve_saci", cer, "sac", "v2 · 430 ferritik 1,0 (manyetik fitil tutar) · 1289,5 × 1089,5 · kaset tüpü çentikleri 62 × 10 · çevresinde ısıtıcı kablo (VARSAYIM 10 W/m)")
    SK = {"K1": dict(x=(X0, DERZ[0]), fitil=(IX[0], DERZ[0] - 18.5), mentese="sol"),
          "K2": dict(x=(DERZ[1], XT[1] - 3.0), fitil=(DERZ[1] + 16.0, IX[1]), mentese="sag")}
    KY_K = (1110.5, H_UST - 3.0)                                                                 # 1110,5 … 2197
    for kn, k in SK.items():
        x0, x1 = xu(k["x"][0]), xu(k["x"][1]); y0, y1 = yu(KY_K[0]), yu(KY_K[1]); z0, z1 = TU0.Z_SKAPAK
        ac = (xu(k["fitil"][0]), xu(k["fitil"][1]), yu(1136.0), yu(IY[1]))
        ds = TU0.kut(x0, x1, y0, y1, z0, z1).cut(TU0.kut(x0 + 1.5, x1 - 1.5, y0 + 1.5, y1 - 1.5, z0 - 1.0, z1 - 1.5))
        pu_ = TU0.kut(x0 + 1.5, x1 - 1.5, y0 + 1.5, y1 - 1.5, z0 + 1.0, z1 - 1.5)
        ic_ = TU0.kut(x0 + 1.5, x1 - 1.5, y0 + 1.5, y1 - 1.5, z0, z0 + 1.0)
        kn_ = TU0.cevre_supur(*ac, TU0.KANAL_PROF)
        pu_, ic_ = pu_.cut(kn_), ic_.cut(kn_)
        pl = TU0.kut(x0 + 1.0, x1 - 1.0, y0 + 1.0, y1 - 1.0, z0, z0 + 1.5).cut(kn_)
        pp = sorted(pl.solids().vals(), key=lambda s_: -s_.BoundingBox().xlen * s_.BoundingBox().ylen)
        assert len(pp) == 2, "%s: kanal dış halkası %d parça" % (kn, len(pp))
        halka = cq.Workplane(obj=pp[0]); ds = ds.union(halka); pu_ = pu_.cut(halka)
        ip = sorted(ic_.solids().vals(), key=lambda s_: s_.BoundingBox().xlen * s_.BoundingBox().ylen)
        assert len(ip) == 2, "%s: iç sac %d parça" % (kn, len(ip))
        ic_ = cq.Workplane(obj=ip[0])
        w_, h_ = k["x"][1] - k["x"][0], KY_K[1] - KY_K[0]
        kg = (w_ * h_ * 1.5 + 2 * (w_ + h_) * 38.5 * 1.5 + (w_ - 3) * (h_ - 3) * 1.0) * 7.93e-6 + (w_ - 3) * (h_ - 3) * 37.5 * 40e-9
        T = lambda s: _sh(s).translate(V(TU0.DX_DUNYA, TU0.DY_DUNYA, 0.0))
        ek("onyuz_%s_dis_sac" % kn, T(ds), "sac", "v2 · soğuk kapak %s %.1f × %.1f × 40 · AISI 304 fırçalı 1,5 dört kenardan bükülü · ≈%.1f kg · gizli menteşe %s · iki katı birden örter"
           % (kn, w_, h_, kg, k["mentese"]))
        ek("onyuz_%s_pu" % kn, T(pu_), "pu", "PU 37,5 (40 kg/m³) · fitil kanalı")
        ek("onyuz_%s_ic_sac" % kn, T(ic_), "paslanmaz", "AISI 304 1,0 · kanalın içindeki panel")
        ek("onyuz_%s_fitil" % kn, T(TU0.cevre_supur(*ac, TU0.FITIL_PROF)), "conta",
           "geçmeli manyetik fitil 21 × 18,5 · çevre %.0f mm" % (2 * (ac[1] - ac[0] + ac[3] - ac[2] + 4 * TU0.FITIL_G)))
    # menteşeler (sanal pivot ön dış köşe) · v2: 2 menteşe (alt 1162 · üst 2070)
    for ad_, xa, xb, y0_, tx in (("K1_mentese_0", X0 + 30.0, X0 + 42.5, 1162.0, (X0, X0 + 30.0)), ("K1_mentese_1", X0 + 30.0, X0 + 42.5, 2070.0, (X0, X0 + 30.0)),
                                 ("K2_mentese_0", 2456.0, 2468.5, 1162.0, (2468.5, X1)), ("K2_mentese_1", 2456.0, 2468.5, 2070.0, (2468.5, X1))):
        ek("onyuz_" + ad_, kut(xa, xb, y0_, y0_ + 70.0, TU0.Z_CER[1], TU0.Z_SKAPAK[0]), "paslanmaz", "çok kollu gizli menteşe KOLU (Sugatsune HES3D sınıfı — VARSAYIM)")
        ek("onyuz_mentese_tabani_" + ad_, kut(tx[0], tx[1], y0_, y0_ + 70.0, TU0.Z_CER[1], TU0.Z_SKAPAK[0] - 1.5), "paslanmaz", "menteşe TABANI AISI 304 30 × 13,5 × 70 · TC yan sacına 2 × M6")
    DXF = DERZ[0] + 1.5 - 1599.25                                                                # flipper v1 → v2 (derz ortası 1599,25 → 1853)
    for ad_, xa, xb in (("basac_K1", 1559.25 + DXF, 1589.25 + DXF), ("basac_K2", 1609.25 + DXF, 1639.25 + DXF)):
        ek("onyuz_" + ad_, kut(xa, xb, H_UST - 40.0, H_UST - 10.0, TU0.Z_CER[1], TU0.Z_SKAPAK[0]), "plastik", "bas-aç mandal (push-to-open, gizli) · Southco E4 sınıfı — VARSAYIM")
    # flipper: katlanma ekseni derzin 27 solunda (v1 ile aynı bağıl) · kam oluğu v2 kapak genişliğiyle YENİDEN hesaplanır
    fl = dict(FLIP_EKSEN=TU0.FLIP_EKSEN, K1_PIVOT=TU0.K1_PIVOT, KILAVUZ=TU0.KILAVUZ, FLIP=TU0.FLIP, FLIP_PIM=TU0.FLIP_PIM)
    try:
        TU0.FLIP_EKSEN = (xu(1572.25 + DXF), 20.0)
        TU0.K1_PIVOT = (xu(X0), Z_ON)
        TU0.KILAVUZ = (xu(1519.25 + DXF), xu(1626.25 + DXF), TU0.SOGUK_TABAN, TU0.SOGUK_TABAN + 15.0, -40.0, TU0.Z_CER[1])
        TU0.FLIP = (xu(1572.25 + DXF), xu(1626.25 + DXF), TU0.KILAVUZ[3] + 0.5, yu(IY[1]) - 0.5)
        TU0.FLIP_PIM = (xu(1620.25 + DXF), -10.0, 4.0, TU0.KILAVUZ[3] - 9.5)
        yol = TU0._pim_yolu()
        T = lambda s: _sh(s).translate(V(TU0.DX_DUNYA, TU0.DY_DUNYA, 0.0))
        ol = [TU0.sily(x_, z_, TU0.FLIP_PIM[2], TU0.FLIP_PIM[3] - 0.5, TU0.KILAVUZ[3] + 1.0).val() for x_, z_, _a in yol]
        while len(ol) > 1:
            ol = [ol[i].fuse(ol[i + 1]) if i + 1 < len(ol) else ol[i] for i in range(0, len(ol), 2)]
        ek("onyuz_kilavuz_flipper", T(TU0.kut(*TU0.KILAVUZ).cut(ol[0])), "pom", "flipper KILAVUZ BLOĞU POM-C 107 × 15 × 64 · kam oluğu v2 kapak genişliğiyle (%d nokta, α 0–%.2f°)" % (len(yol), yol[-1][2]))
        fp = TU0.sily(TU0.FLIP_EKSEN[0], TU0.FLIP_EKSEN[1], 3.0, TU0.FLIP[2] - 1.0, TU0.FLIP[3] + 1.0)
        F = TU0.FLIP
        ek("onyuz_flipper_govde", T(TU0.kut(F[0], F[1], F[2], F[3], -16.0, TU0.Z_CER[1] - 1.5).cut(fp)), "plastik",
           "katlanır orta dikme 54 × %.0f × 38,5 · ABS + PU + ısıtıcı kablo · iki katı boydan boya örter" % (F[3] - F[2]))
        ek("onyuz_flipper_on_sac", T(TU0.kut(F[0], F[1], F[2], F[3], TU0.Z_CER[1] - 1.5, TU0.Z_CER[1]).cut(fp)), "sac", "430 ferritik 1,5 · manyetik fitil tutar")
        ek("onyuz_flipper_pimi", T(TU0.sily(TU0.FLIP_PIM[0], TU0.FLIP_PIM[1], TU0.FLIP_PIM[2], TU0.FLIP_PIM[3], F[2])), "celik", "kam pimi Ø8 × 10 AISI 316")
        for i_, y0_ in enumerate((yu(1192.0), yu(1652.0), yu(2092.0))):                          # v2: 3 menteşe (flipper 972 boy)
            ek("onyuz_K1_flipper_mentese_%d" % i_, T(TU0.kut(xu(1560.25 + DXF), TU0.FLIP_EKSEN[0], y0_, y0_ + 20.0, TU0.FLIP_EKSEN[1] + 1.0, TU0.Z_SKAPAK[0])
                                                       .union(TU0.sily(TU0.FLIP_EKSEN[0], TU0.FLIP_EKSEN[1], 3.0, y0_ - 5.0, y0_ + 25.0))), "paslanmaz",
               "flipper menteşesi (K1 ile döner) + burulma yayı")
        FLIP_V2 = dict(eksen_x=TU0.FLIP_EKSEN[0] + TU0.DX_DUNYA, pim_yolu=len(yol))
    finally:
        for k_, v_ in fl.items(): setattr(TU0, k_, v_)
    # ---- (e) ÜRÜN HORTUMLARI (Ø32 iç · soğuk kutunun içinde) ----
    for k, pts in HORTUM.items():
        uz = sum(math.dist(a, b) for a, b in zip(pts[:-1], pts[1:]))
        ek("%s_urun_hortumu_D32" % k, boru(pts, HORTUM_R), "hortum_gida",
           "v2 · Ø32 / Ø42 gıda hortumu, çelik spiral takviyeli (esneme → doz hassasiyeti) [V] · %s UNO çıkışı (TC) → üst raf → alt kat → taban kontası → yayıcı girişi · "
           "boy ≈ %.0f mm · ölü hacim ≈ %.2f L (soğukta kalır) · temizlikte TC kelepçelerden sökülür" % (k, uz, math.pi / 4 * 32.0 ** 2 * uz / 1e6))
    # ---- (f) KAŞAR / SUCUK 2 GÜNLÜK SOĞUK YEDEĞİ (kural 5.4 · v1'de dolabın K4 deposu) — üst katın sağında, GN 1/1 üstünde GN 1/2 ----
    def gn(ad, x0, x1, y0, h, z0, z1, mal_urun, doluluk, not_):
        g = kut(x0, x1, y0, y0 + h, z0, z1).cut(kut(x0 + 0.8, x1 - 0.8, y0 + 0.8, y0 + h + 1.0, z0 + 0.8, z1 - 0.8))
        g = g.fuse(kut(x0 - 6.0, x1 + 6.0, y0 + h - 1.0, y0 + h, z0 - 6.0, z1 + 6.0).cut(kut(x0 + 0.8, x1 - 0.8, y0 + h - 2.0, y0 + h + 1.0, z0 + 0.8, z1 - 0.8)))
        ek(ad + "_kap", g, "gn", not_)
        ek(ad + "_kapak", kut(x0 - 6.0, x1 + 6.0, y0 + h, y0 + h + 1.2, z0 - 6.0, z1 + 6.0), "gn", "GN düz kapak 0,8 · AISI 304")
        ek(ad + "_urun", kut(x0 + 1.0, x1 - 1.0, y0 + 0.8, y0 + 0.8 + (h - 12.0) * doluluk, z0 + 1.0, z1 - 1.0), mal_urun, "yedek ürün (gösterim)")
    GX = (1990.0, 2315.0); GZ1 = (-511.0, 19.0)
    y_ = RAF2[1]
    gn("gn_kasar_yedek_1_1_200", GX[0], GX[1], y_, 200.0, GZ1[0] + 6.0, GZ1[1] - 6.0, "kasar_urun", HS.KASAR_2GUN_L / HS.GN_KASAR["L"],
       "v2 · %s AISI 304 · kaşar rendesi 2 günlük yedek %.1f L (4 günün 2. yarısı · kural 5.4) · kaset boşalınca personel doldurur" % (HS.GN_KASAR["ad"], HS.KASAR_2GUN_L))
    gn("gn_sucuk_yedek_1_2_150", GX[0], GX[1], y_ + 200.0 + 1.2, 150.0, GZ1[1] - 6.0 - 265.0, GZ1[1] - 6.0, "sucuk_urun", HS.SUCUK_2GUN_L / HS.GN_SUCUK["L"],
       "v2 · %s AISI 304 · küp sucuk 2 günlük yedek %.1f L · kaşar GN'sinin kapağı üstünde (istiflenebilir düz kapak)" % (HS.GN_SUCUK["ad"], HS.SUCUK_2GUN_L))
    # ---- (g) HORTUM GEÇİŞ BLOKLARI (pnömatik hortumlar kuru bölmeden soğuk kutuya) + UNO silindir konsolları ----
    for k, (gx0, gx1, gy0, gy1) in GB.items():
        ek("gecis_blogu_%s" % k, kut(gx0, gx1, gy0, gy1, -630.0, -570.0), "pom",
           "v2 · hortumların soğuk hücreye geçtiği keçeli POM blok (%s kat: %s)" % (k, "kıyma + kuşbaşı UNO valf / piston" if k == "alt" else "sos + harç UNO valf / piston + yayıcı kesme valfleri"))
    for a, s in bul.items():
        if not a.endswith("__pnomatik_on_ayak"): continue
        b = s.BoundingBox(); u_ = a.split("__")[0]
        ek("%s_silindir_konsolu" % u_, kut(b.xmin - 5.0, b.xmax + 5.0, b.ymin - 3.0, b.ymin, -692.0, -630.0).fuse(kut(b.xmin - 5.0, b.xmax + 5.0, b.ymin - 43.0, b.ymin, -633.0, -630.0)),
           "paslanmaz", "v2 · UNO pnömatik silindirinin ön ayağı buna oturur · L 3 mm AISI 304 · soğuk kutunun arka dış sacına 2 × M6 (v1'de ayak boştaydı)")
    # ---- (h) HAVA HATLARI (kuru bölme) ----
    ek("hava_hatti_sartlandirici_ada", boru(ADA_V2, 5.0), "hava_ana", "v2 · Ø10 PU · FRL sol portu → kaset motorlarının ALTINDAN (1125) → valf adasının sağ ucu")
    for j_, (yA, zA, xd, yP, renk) in enumerate(((1472.0, -700.0, 420.0 + DXL, 1460.0, "hortum_mavi"), (1460.0, -712.0, 428.0 + DXL, 1292.0, "hortum_siyah"))):
        ek("hava_hatti_acici_D6_%d" % (j_ + 1), boru([(1240.0, yA, zA), (xd, yA, zA), (xd, yP, zA), (xd, yP, -540.0), (372.5 + DXL, yP, -540.0)], 3.0), renk,
           "Ø6 PU · valf adası → TC sol yan sacı rakoru → açıcı Z silindiri (%s port)" % ("arka" if j_ == 0 else "ön"))
    return L, dict(KAS_YUZ=KAS_YUZ, GB=GB, UH=UH, FLIP=FLIP_V2)


def hava_yolu():
    """v1 denetimi (topping_cad_v32 · dunya_denetimi 8) v2 ölçüsüyle: 240 m³/h (KLF6.6CND 32 °C'de atılan ısı, hava 10 K) · yarık etkin alanı yalnız kaide
    penceresinin önündekiler · arka pencere filtreli (açık oran 0,6 [V]) · sınırlar v1: hız ≤ 3,5 m/s · emiş / atış yarıkları arası ≥ 250"""
    import h2_kaide_v1 as KD2
    Q = (TC0.KLF66[32] + 279.0 * 1.1) / (1.2 * 1006.0 * 10.0)
    et = lambda xs, pen: sum(max(0.0, min(x_ + 60.0, b_) - max(x_, a_)) for x_ in xs for a_, b_ in pen) * 6.0 * len(TC0.IZGARA_Y) * 1e-6
    pw = lambda pen: sum(b_ - a_ for a_, b_ in pen) * (KD2.C_PENCERE_Y[1] - KD2.C_PENCERE_Y[0]) * 1e-6
    on_e = et(IZGARA["emis"], KD2.C_PENCERE_X["emis"]); arka_e = 0.6 * pw(KD2.C_ARKA_PENCERE_X); at = et(IZGARA["atis"], KD2.C_PENCERE_X["atis"])
    ara = IZGARA["atis"][0] - (IZGARA["emis"][-1] + 60.0)
    d = dict(Q_m3h=Q * 3600.0, emis_on=on_e, emis_arka=arka_e, v_emis=Q / (on_e + arka_e), v_emis_yalniz_on=Q / on_e, atis=at, v_atis=Q / at, ara=ara,
             sol_ayirma=IZGARA["emis"][-1] + 60.0 <= T_AYIRMA, sag_ayirma=IZGARA["atis"][0] >= T_AYIRMA)
    d["gecti"] = d["v_emis"] <= 3.5 and d["v_atis"] <= 3.5 and ara >= 250.0 and d["sol_ayirma"] and d["sag_ayirma"]
    return d


T_AYIRMA = TC0.AYIRMA_X


# ================================================================ KUR (önbellekli)
_KUR = {}


def kur():
    if _KUR: return _KUR["TC"], _KUR["TU"]
    TCs, TUs = _siniflandir()
    assert not RAPOR["tu"].get("SINIFSIZ"), RAPOR["tu"]["SINIFSIZ"]
    TCn = yeni_tc()
    TUn, BILGI = yeni_tu(TUs)
    _KUR.update(TC=TCs + TCn, TU=TUs + TUn, BILGI=BILGI)
    adlar = [p["ad"] for p in _KUR["TC"]]; assert len(adlar) == len(set(adlar)), [a for a in adlar if adlar.count(a) > 1][:5]
    adlar = [p["ad"] for p in _KUR["TU"]]; assert len(adlar) == len(set(adlar)), [a for a in adlar if adlar.count(a) > 1][:5]
    return _KUR["TC"], _KUR["TU"]


def eski_tc():
    """montajın ÇİZMEDİĞİ ama ölçü okuduğu TC parçaları (TC0.eski: eski aktarma bandı 'bant' vb. · v1 soğuk hücresi · _bom) — aynı dilim kuralıyla, önbellekli ·
    montaj bunları v1_kalir / AKTARMA_TP10 / KAPAK süzgeçleriyle zaten düşürür (görünmez, denetime girmez)"""
    if "ESKI" in _KUR: return _KUR["ESKI"]
    L = []
    for p in TC0.PARCALAR:
        if not TC0.eski(p["ad"]): continue
        d_ = TC0.V1_TASI.get(p["ad"], (0.0, 0.0, 0.0))
        sh = dilimle(_sh(p["wp"]).translate(V(DXW + d_[0], DYW + d_[1], d_[2])))
        if sh is None: continue
        L.append(dict(ad=p["ad"], sh=sh, mal=p["mal"], bom=p.get("bom"), tur="eski"))
    _KUR["ESKI"] = L
    return L


def grup_pivotlari():
    """TU grup pivotları (TU dünyası = dünya − (700, −168)) · taşınan grupların pivotları parçalarıyla aynı ötelenir"""
    g = {}
    for k, v in TU0.GRUP.items():
        d = GRUP_KAYMA.get(k, (0.0, 0.0, 0.0))
        g[k] = (v[0] + d[0], v[1] + d[1], v[2] + d[2])
    return g


if __name__ == "__main__":
    import time
    t0 = time.time()
    TC, TU = kur()
    print("TC v2 %d parça · TU v2 %d parça · %.0f sn" % (len(TC), len(TU), time.time() - t0))
    print("TC:", RAPOR["tc"]); print("TU:", {k: (v if k != "SINIFSIZ" else len(v)) for k, v in RAPOR["tu"].items()})
    print("grup kaymaları:", GRUP_KAYMA)
    print("bilgi:", _KUR["BILGI"])
    sys.stdout.flush(); os._exit(0)
