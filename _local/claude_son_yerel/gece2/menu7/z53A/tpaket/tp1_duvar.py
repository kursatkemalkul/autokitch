# -*- coding: utf-8 -*-
"""TP1 · SOGUK ODA ARKA DUVARI: eski evaporator pencereleri (2 kaset ust uste) kapatilir, yeni yan yana kasetlerin 4 penceresi acilir
(L: donus + ufleme, R: donus + ufleme) + yayici aktuatorlerinin hortumlari icin 2 duvar gecis kovani (harc x 1745, sos x 2239, taban ustu).
Yontem: bolge (BOLGE L/R) icindeki eski pencere parcalari (tamamen icindeki ucgenler) silinir; arka dis sac / PU / astar duzlemlerindeki
(z -630, -628.5, -571, -570) ucgenlerden bolge dikdortgeni kirpilir (ust raf arka bukumu ve raf ucu haric); bolgeye yeni panel (sac, PU, astar)
+ pencere parcalari (lazer yarikli on sac, kovanlar) eklenir. python tp1_duvar.py giris.glb cikis.glb"""
import os, sys, numpy as np
TPD = os.path.dirname(os.path.abspath(__file__)); S = os.path.dirname(TPD)
gi, go = [os.path.abspath(a) for a in sys.argv[1:3]]
sys.path.insert(0, os.path.join(S, "topfix")); sys.path.insert(0, TPD)
from tlib import *
from m8kit import delik_ucgenler
import tgeo as TG
from tp_olcu import *
Kb, kes, tekle, bb = TG.kutu, TG.kes, TG.tekle, TG._bb
G = Glb(gi)
PLAN = [-630.0, -628.5, -571.0, -570.0]
DUG = ["TOPPING_MODUL__paslanmaz", "TOPPING_MODUL__pu"]


def haric_raf(P):
    lo = P.min(1); hi = P.max(1)
    return (lo[:, 1] >= 1533.0) & (hi[:, 1] <= 1576.3)


def kirp(ad, rect, haric=None, not_=""):
    """z duzlemlerindeki ucgenlerden rect (x0,x1,y0,y1) cikar (duvar yok). donus: ilk ucgen etiketi"""
    x0, x1, y0, y1 = rect; et = None; n0 = n1 = 0
    for p in G.prims:
        if p["name"] != ad or p.get("gizli") or len(p["T"]) == 0: continue
        P = p["X"][p["T"]]; lo = P.min(1); hi = P.max(1)
        flat = (hi[:, 2] - lo[:, 2]) < 0.02
        on = np.zeros(len(P), bool)
        for v in PLAN: on |= flat & (np.abs(P[:, :, 2] - v).max(1) < 0.02)
        m = G.gorunur(p) & on & (hi[:, 0] > x0 + 1e-6) & (lo[:, 0] < x1 - 1e-6) & (hi[:, 1] > y0 + 1e-6) & (lo[:, 1] < y1 - 1e-6)
        if haric is not None: m &= ~haric(P)
        if not m.any(): continue
        idx = np.where(m)[0]; gr = {}
        for t in idx: gr.setdefault(_tek(p, t), []).append(t)
        for (kat, mek, kpk), tt in gr.items():
            Q = P[np.array(tt)]
            for v in PLAN:
                sel = np.abs(Q[:, :, 2] - v).max(1) < 0.02
                if not sel.any(): continue
                R = delik_ucgenler(Q[sel], 2, [v], x0, x1, y0, y1)
                if len(R): G._ekle_dunya(p, R, kat, mek, kpk); n1 += len(R)
                if et is None: et = (kat, mek, kpk)
        n0 += G.sil(p, m)
    log("KIRP %-26s %s  %d -> %d ucgen %s" % (ad, [round(v, 1) for v in rect], n0, n1, not_))
    return et


def _tek(p, t):
    ex = p["pr"].get("extras", {})
    return (G.etiket_of(p, t, "kat") if ex.get("kat") else None, G.etiket_of(p, t, "mek") if ex.get("mek") else None,
            bool(G.kpk_maske(p)[t]) if ex.get("kpk") else False)


ETK = {}
# ---------------------------------------------------------------- 1 · pencere bolgeleri
for k, (x0, x1, y0, y1) in BOLGE.items():
    for ad in DUG:
        sil_tri(G, ad, (x0, x1, y0, y1, -630.05, -569.95), e=0.02, not_="eski pencere parcalari (%s)" % k, bekle=False)
    for ad in DUG:
        et = kirp(ad, (x0, x1, y0, y1), haric=haric_raf, not_="bolge %s" % k)
        if et and ad not in ETK: ETK[ad] = et
log("etiket", ETK)
SAC, PUE = ETK["TOPPING_MODUL__paslanmaz"], ETK["TOPPING_MODUL__pu"]
ZP0, ZP1 = -628.5, -571.2
YENI = []
for k, (x0, x1, y0, y1) in BOLGE.items():
    kan = [v for kk, v in KAN.items() if kk[0] == k]; pen = [v for kk, v in PEN.items() if kk[0] == k]; agz = [v for kk, v in AGIZ.items() if kk[0] == k]
    YENI.append(("TOPPING_MODUL__paslanmaz", "soguk_arka_dis_sac_%s" % k, kes(Kb(x0, x1, y0, y1, -630.0, -628.5), [Kb(a, b, c, d, -631, -627) for a, b, c, d in kan]), SAC))
    pu = kes(Kb(x0, x1, y0, y1, -628.5, -571.0), [Kb(a, b, c, d, -629.5, -570) for a, b, c, d in kan] + [Kb(a, b, c, d, -571.2, -570) for a, b, c, d in pen])
    YENI.append(("TOPPING_MODUL__pu", "soguk_oda_PU_duvar_%s" % k, pu, PUE))
    YENI.append(("TOPPING_MODUL__paslanmaz", "soguk_ic_kaplama_%s" % k, kes(Kb(x0, x1, y0, y1, -571.0, -570.0), [Kb(a, b, c, d, -572, -569) for a, b, c, d in pen]), SAC))
    for (a, b, c, d), (a2, b2, c2, d2) in zip(pen, agz):
        yar = TG.yarik_alani(a2 + 2.0, b2 - 2.0, c2 + 4.0, d2 - 4.0, ZP1 - 1, -569.0, "z", gen=6.0, boy=d2 - c2 - 8.0, adim=12.0)
        YENI.append(("TOPPING_MODUL__paslanmaz", "evap_penceresi_on_sac_lazer_yarik_%s" % k, kes(Kb(a, b, c, d, ZP1, -570.0), yar), SAC))
    for i, (a, b, c, d) in enumerate(kan):
        YENI.append(("TOPPING_MODUL__paslanmaz", "evap_hava_kanali_kovani_%s%d" % (k, i), tekle(Kb(a, b, c, d, ZP0, ZP1).cut(Kb(a + 1, b - 1, c + 1, d - 1, ZP0 - 1, ZP1 + 1))), SAC))
# ---------------------------------------------------------------- 2 · yayici hortum gecis kovanlari (2 x O6 PU hortum, taban ustu)
for nm, d in SPR.items():
    xc = d["serit_x"]; r = (xc - 5.0, xc + 5.0, 1153.0, 1175.0)
    for ad in DUG: kirp(ad, r, not_="gecis kovani %s" % nm)
    YENI.append(("TOPPING_MODUL__paslanmaz", "yayici_hortum_gecis_kovani_%s" % nm, tekle(Kb(r[0], r[1], r[2], r[3], -630.0, -570.0).cut(Kb(r[0] + 1, r[1] - 1, r[2] + 1, r[3] - 1, -631, -569))), SAC))
    for z0 in (-630.0, -573.0):
        tapa = kes(Kb(r[0] + 1, r[1] - 1, r[2] + 1, r[3] - 1, z0, z0 + 3.0), [TG.silindir(3.0, (xc, y, z0 - 1), (xc, y, z0 + 4)) for y in (Y_HAT_A, Y_HAT_B)])
        YENI.append(("TOPPING_MODUL__silikon", "yayici_gecis_tapasi_%s" % nm, tapa, (kat_no(G, "HAVA"), mek_no(G, "TOPPING/Hava"), False)))
for nd, ad, s, (kt, mk, kp) in YENI:
    n = ekle_kati(G, nd, [s], kt, mk, False)
    log("YENI %-26s %-44s %s %d" % (nd.replace("TOPPING_MODUL__", ""), ad, [round(v, 1) for v in bb(s)], n))
kaydet(G, go)
sys.stdout.flush(); os._exit(0)
