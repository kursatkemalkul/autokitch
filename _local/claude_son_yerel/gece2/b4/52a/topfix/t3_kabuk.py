# -*- coding: utf-8 -*-
"""TOPFIX 3 · SOGUK ODA KABUGU ORIJINAL GENISLIKTE (cep yok, astar 1495-2441) + yeni dusme delikleri / gecis kovanlari / dil kanallari /
mandal yuvalari + iki evaporator kasetine iki pencere (4 hava kanali) · A sag levha (yalniz tabla gecisi) · TOPPING dis yan sol (yalniz tabla gecisi).
m7b_kabuk.py'nin DELTA = 0 hali. python t3_kabuk.py giris.glb cikis.glb"""
import os, sys, time, json, numpy as np
from tlib import *
import trimesh
import tgeo as TG
from dikis import kati
K, S_, kes, tekle, bb = TG.kutu, TG.silindir, TG.kes, TG.tekle, TG._bb
t0 = time.time()
gi, go = sys.argv[1:3]
G = Glb(gi)
ETK = json.load(open("t1_etiket.json"))
# ---- olculer (orijinal yer + birim kaymasi)
DXo = {"kiyma": 0.0, "kusbasi": 42.0, "kasar": 26.5, "sucuk": 49.5}     # orijinal (v8w) yerlerden
X_L, X_R, Z_H = 1722.0, 2259.5, -170.0
YARIK_X = [(2030.5 + DXo["kasar"], 2093.5 + DXo["kasar"]), (2279.5 + DXo["sucuk"], 2342.5 + DXo["sucuk"])]
MANDAL = {"kasar": (1932.5 + DXo["kasar"], 1940.5 + DXo["kasar"]), "sucuk": (2244.5 + DXo["sucuk"], 2252.5 + DXo["sucuk"])}
MZ = (-199.5, -193.5)
# ---- evaporator pencereleri (t4 ile ayni): her kaset 1 pencere, 2 kanal (ufleme = fan onu, donus = serpantin onu)
from t_olcu import KASET, PEN, KAN, AGIZ


def pencere(z0, z1):
    s = None
    for x0, x1, y0, y1 in PEN:
        b = K(x0, x1, y0, y1, z0, z1); s = b if s is None else s.fuse(b)
    return tekle(s)


TG.pencere_prizma = pencere
# ================================================================ gomulu elemanlar (PU / astar / arka sac delikleri) · TASINMIS konumlarla
PU_KUTU = (1437.5, 2498.5, 1110.5, 2198.5, -628.5, 38.0)
CAV_IN = (1496.0, 2440.0, 1109.0, 2140.0, -570.0, 39.0)
gomulu, gom_ad = [], []
for p in G.prims:
    nm = p["name"]
    if not nm.startswith("TOPPING_MODUL") or "__PISTON_" in nm or "ACICI" in nm or "ARABA" in nm or p.get("gizli"): continue
    if len(p["T"]) == 0: continue
    tl, kut = G.komp(p); vis = G.gorunur(p)
    for c, (lo, hi, n) in kut.items():
        if (hi - lo).max() > 700: continue
        b = PU_KUTU
        if not (lo[0] < b[1] - 0.5 and hi[0] > b[0] + 0.5 and lo[1] < b[3] - 0.5 and hi[1] > b[2] + 0.5 and lo[2] < b[5] - 0.5 and hi[2] > b[4] + 0.5): continue
        if lo[0] >= 1496.0 - 0.01 and hi[0] <= 2440.01 and lo[2] >= -570.01 and hi[2] <= 38.01: continue
        b = CAV_IN
        if lo[0] >= b[0] and hi[0] <= b[1] and lo[1] >= b[2] and hi[1] <= b[3] and lo[2] >= b[4] and hi[2] <= b[5]: continue
        m = (tl == c) & vis; V = p["X"][np.unique(p["T"][m].reshape(-1))]
        tm = trimesh.Trimesh(V, process=False).convex_hull
        gomulu += kati(np.asarray(tm.vertices), np.asarray(tm.faces))
        gom_ad.append("%s#%d [%.0f-%.0f %.0f-%.0f %.0f-%.0f]" % (nm.replace("TOPPING_MODUL__", ""), c, lo[0], hi[0], lo[1], hi[1], lo[2], hi[2]))
log("GOMULU %d: %s" % (len(gom_ad), " · ".join(gom_ad)))


def dus(s, al):
    al = [a for a in al if TG._kesisir_bb(bb(a), bb(s), 0.0)]
    return kes(s, al) if al else s


YENI = []
# ================================================================ astar
cav_out = K(1495.0, 2441.0, 1110.5, 2141.0, -571.0, 38.0)
cav_in = K(*CAV_IN)
astar = dus(tekle(cav_out.cut(cav_in)), gomulu + [pencere(-572.0, -569.0)])
YENI.append(("TOPPING_MODUL__paslanmaz", "soguk_ic_kaplama", astar))
# ================================================================ tasiyici raf + bukumler + kosebentler
XR0 = 1496.0
delik = [S_(21.5, (1596.0, 1140, Z_H), (1596.0, 1160, Z_H)), S_(21.5, (1848.0, 1140, Z_H), (1848.0, 1160, Z_H)),
         S_(18.6, (X_L, 1140, Z_H), (X_L, 1160, Z_H)), S_(18.6, (X_R, 1140, Z_H), (X_R, 1160, Z_H))]
delik += [K(a, b, 1140.0, 1160.0, -181.0, 24.0) for a, b in YARIK_X]
delik += [K(a - 0.5, b + 0.5, 1140.0, 1160.0, MZ[0] - 0.5, MZ[1] + 0.5) for a, b in MANDAL.values()]
raf = kes(K(XR0, 2440.0, 1149.0, 1152.0, -570.0, 23.0), delik)
on_b = kes(K(1496.0, 2440.0, 1110.5, 1149.0, 20.0, 23.0), [K(a, b, 1142.5, 1150.0, 19.0, 24.0) for a, b in YARIK_X])
arka_b = K(XR0, 2440.0, 1110.5, 1149.0, -570.0, -567.0)
kb_sol = tekle(K(XR0, XR0 + 3, 1110.5, 1149.0, -567.0, 20.0).fuse(K(XR0 + 3, XR0 + 40, 1146.0, 1149.0, -567.0, 20.0)))
kb_sag = tekle(K(2437.0, 2440.0, 1110.5, 1149.0, -567.0, 20.0).fuse(K(2401.0, 2437.0, 1146.0, 1149.0, -567.0, 20.0)))   # sucuk kovani 2400,5'te biter
for ad, s in (("tasiyici_raf_3mm", raf), ("raf_on_bukumu", on_b), ("raf_arka_bukumu", arka_b), ("raf_kosebendi_sol", kb_sol), ("raf_kosebendi_sag", kb_sag)):
    YENI.append(("TOPPING_MODUL__paslanmaz", ad, s))
# ================================================================ taban gecis kovanlari + alt PU + alt sac
TG.TABAN_GECIS = {"kiyma": [(1577.0, 1615.0, -189.0, -151.0)], "kusbasi": [(1787.0 + 42.0, 1825.0 + 42.0, -189.0, -151.0)],
                  "kasar": [(2023.0 + 26.5, 2101.0 + 26.5, -161.0, -139.0), (2029.0 + 26.5, 2095.0 + 26.5, -182.5, -117.0)],
                  "sucuk": [(2272.0 + 49.5, 2350.0 + 49.5, -161.0, -139.0), (2278.0 + 49.5, 2344.0 + 49.5, -182.5, -117.0)]}
TG.TABAN_YUVARLAK = {"sos": (X_R, -169.8, 15.5), "harc": (X_L, -169.8, 15.5)}
TK, TKD = TG.taban_kovanlari()
for (a, b_), k in zip(YARIK_X, ("kasar", "sucuk")):
    TK["soguk_taban_gecis_kovani_%s" % k] = kes(TK["soguk_taban_gecis_kovani_%s" % k], [K(a, b_, 1142.5, 1150.0, -120.0, -112.0)])
for ad, s in TK.items(): YENI.append(("TOPPING_MODUL__paslanmaz", ad, s))
ic_del = [TG._rect_birlesim(rs, 0.0, 1107.0, 1112.0) for rs in TG.TABAN_GECIS.values()]
ic_del += [S_(r, (x, 1107.0, z), (x, 1112.0, z)) for x, z, r in TG.TABAN_YUVARLAK.values()]
MG_KUTU = {k: (a - 8.0, b + 8.0, 1124.0, 1149.0, -214.0, -180.0) for k, (a, b) in MANDAL.items()}
altpu = K(XR0 + 3, 2437.0, 1110.5, 1149.0, -567.0, 20.0)
altpu = kes(altpu, TKD + [K(XR0 + 3, XR0 + 40, 1146.0, 1149.5, -568.0, 21.0), K(2400.0, 2437.0, 1146.0, 1149.5, -568.0, 21.0)]
            + [K(a - 1.0, b + 1.0, 1143.0, 1150.0, -117.0, 21.0) for a, b in YARIK_X] + [K(*v) for v in MG_KUTU.values()])
YENI.append(("TOPPING_MODUL__pu", "soguk_oda_PU_alt", altpu))
altsac = kes(K(1437.5, 2498.5, 1109.0, 1110.5, -628.5, 38.0), ic_del)
YENI.append(("TOPPING_MODUL__paslanmaz", "alt_yalitim_saci", altsac))
# ================================================================ esik + dil kanallari + on cerceve
TG.YARIK_X = YARIK_X
ES, EP = TG.esik()
for nm in list(ES):
    if nm.startswith("soguk_raf_dil_kanali_tabani"): del ES[nm]
for (a, b), nm in zip(YARIK_X, ("kasar", "sucuk")):
    ES["soguk_raf_dil_kanali_tabani_%s" % nm] = K(a, b, 1142.4, 1144.0, -116.0, 20.0)
for ad, s in ES.items(): YENI.append(("TOPPING_MODUL__paslanmaz", ad, s))
for ad, s in EP.items(): YENI.append(("TOPPING_MODUL__pu", ad, s))
MG, _MK = TG.menteseler()
YENI.append(("TOPPING_MODUL__paslanmaz", "onyuz_on_cerceve_430", TG.on_cerceve(MG)))
# ================================================================ arka dis sac + PU duvar
arka = dus(K(1437.5, 2498.5, 1109.0, 2198.5, -630.0, -628.5), gomulu + [pencere(-631.0, -627.5)])
YENI.append(("TOPPING_MODUL__paslanmaz", "soguk_arka_dis_sac", arka))
pu = tekle(K(*PU_KUTU).cut(cav_out))
pu = tekle(pu.cut(pencere(-640.0, -570.0)))
bas = []
for g in gomulu:
    if not TG._kesisir_bb(bb(g), bb(pu), 0.0): continue
    try:
        r = pu.cut(g)
        if r.isNull() or r.Volume() <= 0: raise ValueError("bos")
        pu = tekle(r)
    except Exception as e:
        pu = tekle(pu.cut(K(*bb(g)))); bas.append(str(bb(g)))
if bas: log("UYARI PU kutu ile dusuldu: " + "; ".join(bas))
YENI.append(("TOPPING_MODUL__pu", "soguk_oda_PU_duvar", pu))
log("PU %.0f s" % (time.time() - t0))
# ================================================================ ust raf
ur = kes(K(XR0, 2440.0, 1572.0, 1575.0, -570.0, -50.0), [S_(20.3, (x, 1570, -172.45), (x, 1577, -172.45)) for x in (X_L, X_R)])
YENI += [("TOPPING_MODUL__paslanmaz", "ust_raf_3mm", ur),
         ("TOPPING_MODUL__paslanmaz", "ust_raf_on_bukumu", K(XR0, 2440.0, 1534.0, 1572.0, -53.0, -50.0)),
         ("TOPPING_MODUL__paslanmaz", "ust_raf_arka_bukumu", K(XR0, 2440.0, 1534.0, 1572.0, -570.0, -567.0)),
         ("TOPPING_MODUL__paslanmaz", "ust_raf_kosebendi_sol", tekle(K(XR0, XR0 + 3, 1532.0, 1572.0, -567.0, -53.0).fuse(K(XR0 + 3, XR0 + 40, 1569.0, 1572.0, -567.0, -53.0)))),
         ("TOPPING_MODUL__paslanmaz", "ust_raf_kosebendi_sag", tekle(K(2437.0, 2440.0, 1532.0, 1572.0, -567.0, -53.0).fuse(K(2400.0, 2437.0, 1569.0, 1572.0, -567.0, -53.0))))]
# ================================================================ evaporator pencereleri (on lazer yarikli sac · arka sac · PU · 4 kanal kovani)
ZP0, ZP1 = -628.5, -571.2
yar = []
for x0, x1, y0, y1 in AGIZ:
    yar += TG.yarik_alani(x0 + 2.0, x1 - 2.0, y0 + 4.0, y1 - 4.0, ZP1 - 1, -569.0, "z", gen=6.0, boy=y1 - y0 - 8.0, adim=12.0)
YENI.append(("TOPPING_MODUL__paslanmaz", "evap_penceresi_on_sac_lazer_yarik", kes(pencere(ZP1, -570.0), yar)))
YENI.append(("TOPPING_MODUL__paslanmaz", "evap_penceresi_arka_sac", kes(pencere(-630.0, ZP0), [K(x0, x1, y0, y1, -631.0, ZP0 + 1) for x0, x1, y0, y1 in KAN])))
for i, (x0, x1, y0, y1) in enumerate(KAN):
    YENI.append(("TOPPING_MODUL__paslanmaz", "evap_hava_kanali_kovani_%d" % i, tekle(K(x0, x1, y0, y1, ZP0, ZP1).cut(K(x0 + 1.0, x1 - 1.0, y0 + 1.0, y1 - 1.0, ZP0 - 1, ZP1 + 1)))))
YENI.append(("TOPPING_MODUL__pu", "evap_penceresi_PU", kes(pencere(ZP0, ZP1), [K(x0, x1, y0, y1, ZP0 - 1, ZP1 + 1) for x0, x1, y0, y1 in KAN])))
# ================================================================ TOPPING dis yan sol + A sag levha: YALNIZ tabla gecisi (cep / kablo / kanal / rakor agzi yok)
YENI.append(("TOPPING_MODUL__sac", "dis_yan_sol", kes(K(TG.X0, TG.XI0, TG.YB, TG.YTI, TG.ZA, TG.ZF), [K(TG.X0 - 1, TG.XI0 + 1, TG.YBI, 1042.0, -510.0, 5.0)])))
YENI.append(("A_GOVDE__sac", "A_sag_levha", kes(K(1434.5, 1436.0, 788.0, 2198.5, -830.0, 59.0), [K(1433.0, 1437.0, 893.4, 1042.0, -510.0, 4.0)])))
log("katilar %.0f s" % (time.time() - t0))
REF = {"TOPPING_MODUL__paslanmaz": ETK["TOPPING_MODUL__paslanmaz"], "TOPPING_MODUL__pu": ETK["TOPPING_MODUL__pu"],
       "TOPPING_MODUL__sac": ETK["TOPPING_MODUL__sac"], "A_GOVDE__sac": ETK["A_GOVDE__sac"]}
for nd, ad, s in YENI:
    kat, mek, kpk = REF[nd]
    n = ekle_kati(G, nd, [s], kat, mek, False)
    b = bb(s); log("YENI %-26s %-36s x %7.1f %7.1f y %7.1f %7.1f z %7.1f %7.1f  %d ucgen" % (nd.replace("TOPPING_MODUL__", ""), ad, *b, n))
kaydet(G, go)
sys.stdout.flush(); os._exit(0)
