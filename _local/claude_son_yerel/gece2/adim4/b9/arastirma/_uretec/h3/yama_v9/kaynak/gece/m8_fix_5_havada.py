# -*- coding: utf-8 -*-
"""MADDE 8 · adim 5 · havada parcalar + kapak (kpk) gizleme etiketleri (m8_k123.pkl / havada_pu_kapak taramasi). python m8_fix_5_havada.py giris.glb cikis.glb"""
import sys, os, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from m8kit import Glb, Yuzey, bosluk, radyal, kutu_ucgen
g = Glb(sys.argv[1]); LOG = []
def log(*a): LOG.append(" ".join(str(x) for x in a)); print(*a)
def B(d, lo, hi):
    c = (np.array(lo, float) + np.array(hi, float)) / 2
    b = g.bul_nokta(d, c, tol=0.3)
    if np.abs(b["lo"] - lo).max() > 1.0 or np.abs(b["hi"] - hi).max() > 1.0:
        # kutu tam uymuyorsa ayni dugumde kutusu en yakin bilesen
        L = g._bc[d]; b = min(L, key=lambda q: np.abs(q["lo"] - lo).sum() + np.abs(q["hi"] - hi).sum())
    return b

# ---------- cozumle ----------
HAV = []   # (ad, dugum, lo, hi, yontem)
# TOPPING sabit tahrik motoru civatalari (0,5-1,35 delik boslugu): tasima motor flansina cakistirdi -> dokunulmadi (acik: uretecte delik/civata capi)
KBI = []   # K bant avara rulosu ic kabugu (dis rulo [4021,7-4071] icinde gorunmez, 1,5 mm havada) -> silinir
HAV += [
        ("K itici araba kizak pabucu arka", "K_ITICI__aluminyum__ITICI_ARABA", [4049.6, 984.0, -767.0], [4100.4, 1042.0, -743.0], "tasi"),
        ("K itici araba kizak pabucu on", "K_ITICI__aluminyum__ITICI_ARABA", [4049.6, 984.0, -657.0], [4100.4, 1042.0, -633.0], "tasi"),
        ("E govde sag arka sac", "E_GOVDE__sac", [5217.0, 237.5, -810.5], [5228.5, 982.5, -421.5], "tasi"),
        ("Tezgah evye batarya krom", "TEZGAH_EVYE__krom", [4140.0, 986.0, 1682.6], [4220.0, 1006.0, 1706.6], "tasi"),
        ("Tezgah evye sensor cami", "TEZGAH_EVYE__sensor_cam", [4218.0, 960.0, 1686.6], [4220.0, 978.0, 1702.6], "tasi"),
        ("Tezgah sarf poset", "TEZGAH_SARF__poset", [4350.0, 104.2, 1779.3], [4480.0, 173.2, 1848.7], "tasi"),
        ("TOPPING tabla parcasi", "TOPPING_DONER__TABLA", [1076.2, 972.8, -308.0], [1096.0, 981.0, -275.0], "tasi")]
# Ana pano RevPi DIO/AIO klemens fisleri modul on yuzune 1,1 mm takili (gecme) -> havada degil, dokunulmadi
HB = []
for ad, d, lo, hi, y in HAV:
    try: HB.append((ad, d, B(d, lo, hi), y))
    except Exception as e: log("BULUNAMADI", ad, e)
KPK_EKLE = [("QR_MUSTERI_PANELI__ekran_cam", [4835.0, 1663.0, 1163.0], [5010.0, 1773.0, 1188.5]),
            ("QR_MUSTERI_PANELI__paslanmaz", [5150.0, 1675.0, 1158.5], [5236.0, 1761.0, 1188.5]),
            ("QR_MUSTERI_PANELI__plastik", [5040.0, 1683.0, 1143.0], [5120.0, 1743.0, 1188.5]),
            ("QR_HAVALANDIRMA__plastik", [5225.0, 275.0, 671.5], [5375.0, 425.0, 711.5]),
            ("QR_HAVALANDIRMA__plastik", [5245.0, 1885.0, 671.5], [5395.0, 2035.0, 711.5]),
            ("TEZGAH_BULASIK__ekran_cam", [3855.5, 655.0, 1220.2], [3857.0, 685.0, 1340.2]),
            ("TEZGAH_BULASIK__kulp_isik", [3849.0, 597.1, 1265.6], [3857.0, 626.9, 1295.2]),
            ("TEZGAH_CEKMECE__celik", [3834.0, 790.0, 1210.0], [3857.0, 805.0, 1350.0])]
KE = []
for d, lo, hi in KPK_EKLE:
    try: KE.append((d, B(d, lo, hi)))
    except Exception as e: log("BULUNAMADI kpk", d, e)
g.bilesen("TEZGAH_CEKMECE__celik", 0)
for b in g._bc["TEZGAH_CEKMECE__celik"]:
    if b["lo"][0] > 3854 and b["hi"][0] < 3882 and 835 < b["lo"][1] < 840 and 1270 < b["lo"][2] < 1271: KE.append(("TEZGAH_CEKMECE__celik", b))
g.bilesen("ELK_ISTASYON__pano", 0); g.bilesen("ELK_ISTASYON__rakor", 0)
B_GOVDE = B("ELK_ISTASYON__pano", [4160.0, 605.0, -698.0], [4320.0, 725.0, -612.0])
B_ARKA = B("ELK_ISTASYON__pano", [4160.0, 605.0, -700.0], [4320.0, 725.0, -698.0])
B_RAKOR = [b for b in g._bc["ELK_ISTASYON__rakor"] if b["lo"][0] >= 4190 and b["hi"][0] <= 4290 and b["lo"][1] >= 630 and b["hi"][1] <= 700 and b["lo"][2] > -650 and b["hi"][2] < -520]
OLUK = B("E_COP__sac", [4449.0, 545.5, 0.0], [4609.0, 603.0, 57.5])
for lo, hi in (([4023.2, 945.7, -403.0], [4069.5, 992.3, -21.0]), ([4331.2, 945.7, -403.0], [4377.5, 992.3, -21.0])):
    KBI.append(B("K_BANT__aluminyum", lo, hi))
g.bilesen("ELK_TOPPING__kanal", 0)
KIC = [b for b in g._bc["ELK_TOPPING__kanal"] if (abs(b["lo"][0] - 2422.5) < 0.2 and abs(b["hi"][0] - 2447.5) < 0.2 and abs(b["lo"][2] + 826.8) < 0.2)
       or (abs(b["lo"][0] - 1891.5) < 0.2 and abs(b["lo"][1] - 1841.5) < 0.2)]
TAB = [B("TOPPING_MODUL__paslanmaz", [2030.5, 1143.0, -116.0], [2093.5, 1144.0, 20.0]), B("TOPPING_MODUL__paslanmaz", [2324.0, 1143.0, -116.0], [2387.0, 1144.0, 20.0])]
MEKY = [("x motoru kablo klipsi (KAIDE_A'ya bagli)", B("ELK_TOPPING__celik", [880.0, 893.5, -627.7], [896.0, 920.6, -615.6]), 18),
        ("F ana hat tavan rakoru M40 (B kasasi + ana hat)", B("ELK_ISTASYON__rakor", [2971.6, 778.5, -690.0], [3008.4, 800.0, -653.5]), 26),
        ]
g.bilesen("ELK_QR_MONTAJ__paslanmaz", 0)
for b in g._bc["ELK_QR_MONTAJ__paslanmaz"]:
    if b["lo"][0] >= 5039.9 and b["hi"][0] <= 5157.1 and b["lo"][1] >= 20.5 and b["hi"][1] <= 83.7 and b["lo"][2] >= 669.9 and b["hi"][2] <= 691.6:
        MEKY.append(("QR giris plakasi a parcasi (robot kontrol kutusu altinda)", b, 56))
YS = Yuzey(g, haric=("ROBOT", "INSAN", "ZEMIN", "URUN"))
log("cozuldu: havada", len(HB), "kpk+", len(KE), "B rakor", len(B_RAKOR))

# ---------- 1 . havada parcalar: en yakin yuzeye temas (gercekte vidali / oturur) ----------
for ad, d, b, y in HB:
    R = bosluk(g, YS, b["lo"], b["hi"], "__YOK__", maxd=12.0)
    if not R: log("havada", ad, "yakin yuzey yok -> dokunulmadi"); continue
    t, ax, sg = R[0]
    ext = b["hi"] - b["lo"]
    if y == "tasi" and ext.max() / max(ext.min(), 0.1) > 5:          # ince uzun (saplama/civata): eksen boyunca otur
        Ra = [r for r in R if r[1] == int(np.argmax(ext)) and r[0] <= 2.0]
        if Ra: t, ax, sg = Ra[0]
    if t > 5.0: log("havada", ad, "en yakin yuzey %.1f mm -> dokunulmadi" % t); continue
    if y == "tambur":           # K bant yan profili (46x46): sasiye 2 kosebent (bant haric en yakin yapi)
        R2 = bosluk(g, YS, b["lo"], b["hi"], "K_BANT__pu_bant", maxd=80.0, yapi=True, haric_eksen=2)
        if not R2: log("havada", ad, "yapi bulunamadi"); continue
        t, ax, sg = R2[0]; lo, hi = b["lo"], b["hi"]
        for zc in (lo[2] + 25, hi[2] - 25):
            a = np.zeros(3); e = np.zeros(3); a[ax] = hi[ax] if sg > 0 else lo[ax]; e[ax] = a[ax] + sg * t
            u = [i for i in (0, 1) if i != ax][0]; L = np.minimum(a, e); H = np.maximum(a, e)
            L[u] = (lo[u] + hi[u]) / 2 - 15; H[u] = (lo[u] + hi[u]) / 2 + 15; L[2] = zc - 15; H[2] = zc + 15
            g.ekle_dugum(d, kutu_ucgen(L, H), ornek=b)
        log("havada", ad, "2 kosebent %.1f mm %s%s" % (t, "+" if sg > 0 else "-", "xyz"[ax]))
    else:
        dv = np.zeros(3); dv[ax] = sg * t
        g.tasi_b(b, dv); log("havada", ad, "%s%s %.2f mm" % ("+" if sg > 0 else "-", "xyz"[ax], t))

# ---------- 2 . kapak gizleme (kpk): kapak kanadina takili parcalar kapakla gizlenir ----------
for d, b in KE: g.kpk_yaz(b, True); log("kpk +", d, b["lo"].round(0))
for b in B_RAKOR: g.kpk_yaz(b, True); log("kpk + B istasyon kutusu kapak rakoru", b["lo"].round(0))
g.kpk_yaz(B_GOVDE, False); g.kpk_yaz(B_ARKA, False)
log("kpk - B istasyon kutusu govde + arka montaj plakasi (yalniz on kapak kpk)")

# ---------- 3 . E cop oluğu yalniz on kapaga dayaniyordu -> E govdesine 2 L braket ----------
R = bosluk(g, YS, OLUK["lo"], OLUK["hi"], "E_COP__sac", maxd=80.0, yapi=True, haric_eksen=2)
log("E oluk bosluklar", [(round(t, 1), "xyz"[a], s) for t, a, s in R[:4]])
if R:
    t, ax, sg = R[0]; lo, hi = OLUK["lo"].copy(), OLUK["hi"].copy()
    for zc in (lo[2] + 12, hi[2] - 12):
        a = np.zeros(3); e = np.zeros(3)
        a[ax] = hi[ax] if sg > 0 else lo[ax]; e[ax] = a[ax] + sg * t
        u = [i for i in (0, 1) if i != ax][0]
        L = np.minimum(a, e); H = np.maximum(a, e)
        L[u] = (lo[u] + hi[u]) / 2 - 15; H[u] = (lo[u] + hi[u]) / 2 + 15
        L[2] = zc - 1.0; H[2] = zc + 1.0
        g.ekle_dugum("E_COP__sac", kutu_ucgen(L, H), ornek=OLUK)
    log("E oluk braketi", round(t, 1), "xyz"[ax], sg)

# ---------- 4 . KD1/KD2 kanal ic kabugu (dis kutu kapali; ic kabuk gorunmez, 1,5 mm havada) silindi ----------
for b in KIC + KBI: g.sil_b(b)
log("KD1/KD2 ic kabuk silindi", len(KIC), "+ K bant avara ic kabugu", len(KBI))
# ---------- 5 . acikta PU yarigi (kasar/sucuk dil kanali tabani onunde 0,5 mm) -> taban sacinin alt yuzu y 1142,4 ----------
from m8kit import esle
for b in TAB: g.donustur(b, lambda P: esle(P, 1, 1143.0, 1142.4, tol=0.05))
log("PU yarigi kapatildi", len(TAB))
# ---------- 6 . istasyon etiketi (mek) ----------
for ad, b, m in MEKY: g.mek_yaz(b, m); log("mek", ad, "->", m)
g.kaydet(sys.argv[2]); log("kaydedildi", sys.argv[2])
open(os.path.splitext(sys.argv[2])[0] + "_log.txt", "w", encoding="utf-8").write("\n".join(LOG))
