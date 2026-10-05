# -*- coding: utf-8 -*-
"""M7-B · SOĞUK ODA KABUĞU YENİDEN: sol duvar 185 mm sola (A'nın içine CEP) + yeni düşme delikleri / geçişler.
python m7b_kabuk.py giris.glb cikis.glb
SİLİNİP YENİDEN KURULAN (tgeo ölçüleriyle, CadQuery katı):
  astar (soguk_ic_kaplama: ana oda + cep, cep önü z -15/-14 kapalı) · taşıyıcı raf 3 + ön/arka büküm + köşebentler · alt PU · taban geçiş
  kovanları (yeni x) · ön eşik + dil kanalları (yeni x) · ön çerçeve 430 (yeni kaset dili kanalları) · soğuk arka dış sac + alt yalıtım sacı (cep
  dahil) · PU duvar (gömülü elemanlar yeni yerlerinde düşülür) · üst raf (yeni hortum delikleri, cebe uzar) · dış yan sol (cep ağzı) · cep
  sacları (sol / üst / ön) · A dış sacı sağ levhası (cep ağzı; A çerçevesi kesilmez: cep çerçevenin iç açıklığından geçer)
TAŞINAN: sol raf askı burçları (alt 4 + üst 4) -185.
DEĞİŞMEYEN: A dış ölçüsü 736-1436 / ön kapak / açıcı · TOPPING dış zarfı · kanatlar / menteşeler / ön açıklık 1496-2440 · evaporatör.
Üretece taşınacak yer: topping_govde_yeni / tgeo (LIN_X0, cep, YARIK_X, TABAN_GECIS, TABAN_YUVARLAK) + A gövde üreteci (sağ levha cep ağzı)."""
import os, sys, time, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "tg"))
import trimesh
import tgeo as TG
from dikis import kati
from m7kit import Glb
from m7_etiket import etiketle
from m7_olcu import DX, X_L, X_R, Z_H, DELTA, LIN_X0, X_O, CEP_Y1, CEP_ZF, CEP_LIN_ZF, YARIK_X

K, S_, kes, tekle, bb = TG.kutu, TG.silindir, TG.kes, TG.tekle, TG._bb
t0 = time.time()
gi, go = sys.argv[1], sys.argv[2]
G = Glb(gi)
rap = []


def P(ad): return G.bul(ad)


# ================================================================ 1 · SİL (eski kabuk aralıkları; kutularla doğrulanır)
SIL_ARALIK = {"TOPPING_MODUL__paslanmaz": [(10024, 2138, (1437.5, 2498.5, 1109.0, 2198.5)), (13046, 200, (1437.5, 2498.5, 893.5, 2198.5)),
                                           (13246, 36, None), (13282, 44, None), (13326, 28, None), (13354, 28, None), (13382, 12, None),
                                           (13394, 12, None), (13406, 32, None), (13438, 32, None), (13470, 96, None), (13566, 96, None),
                                           (13662, 504, None), (14166, 504, None)],
              "TOPPING_MODUL__pu": [(292, 44, (1496.0, 2440.0, 1110.5, 1150.8)), (336, 1556, (1437.5, 2498.5, 1110.5, 2198.5)),
                                    (1892, 1228, (1499.0, 2437.0, 1110.5, 1149.0))],
              "TOPPING_MODUL__sac": [(4164, 564, (1436.0, 1437.5, 892.0, 2198.5))]}
ETK = {}
for nd, L in SIL_ARALIK.items():
    p = P(nd)
    for a, n, kut in L:
        m = G.aralik(p, a, n)
        Q = p["X"][p["T"][m]].reshape(-1, 3)
        if kut:
            lo, hi = Q.min(0), Q.max(0)
            assert abs(lo[0] - kut[0]) < 0.6 and abs(hi[0] - kut[1]) < 0.6 and abs(lo[1] - kut[2]) < 0.6 and abs(hi[1] - kut[3]) < 0.6, (nd, a, lo, hi)
        ETK.setdefault(nd, (G.etiket_of(p, a), G.etiket_of(p, a, "mek")))
        G.sil(p, m); rap.append("SIL %s [%d +%d] %d üçgen" % (nd, a, n, m.sum()))
# A dış sacı sağ levhası (x >= 1434,5 tümüyle)
pa = P("A_GOVDE__sac"); C = pa["X"][pa["T"]]
ma = G.gorunur(pa) & (C[:, :, 0] >= 1434.4).all(1)
ETK["A_GOVDE__sac"] = (G.etiket_of(pa, int(np.where(ma)[0][0])), G.etiket_of(pa, int(np.where(ma)[0][0]), "mek"))
G.sil(pa, ma); rap.append("SIL A_GOVDE__sac sağ levha %d üçgen" % ma.sum())

# ================================================================ 2 · sol raf askı burçları → cebe (-185)
R = etiketle(G, ("TOPPING_MODUL",))
for i, (tl, kut, ad) in R.items():
    p = G.prims[i]
    for c, nm in ad.items():
        if nm.startswith(("raf_askisi_burclari_sol", "ust_raf_askisi_burclari_sol")):
            m = (tl == c) & G.gorunur(p)
            if not m.any(): continue
            G.tasi(p, m, lambda V: V - np.array([DELTA, 0, 0])); rap.append("TASI %s -%.0f" % (nm, DELTA))

# ================================================================ 3 · GÖMÜLÜ ELEMANLAR (PU / astar / arka sac delikleri) · taşınmış konumlarıyla
PU_KUTULAR = [(1437.5, 2498.5, 1110.5, 2198.5, -628.5, 38.0), (X_O + 1.5, 1437.5, 1110.5, CEP_Y1 - 1.5, -628.5, CEP_ZF - 1.5)]
CAV_IN = [(1496.0, 2440.0, 1109.0, 2140.0, -570.0, 39.0), (LIN_X0 + 1, 1497.0, 1109.0, 2140.0, -570.0, CEP_LIN_ZF - 1)]
gomulu, gom_ad = [], []
for p in G.prims:
    nm = p["name"]
    if not nm.startswith("TOPPING_MODUL") or "__PISTON_" in nm or "ACICI" in nm or "ARABA" in nm: continue
    if len(p["T"]) == 0: continue
    tl, kut = G.komp(p)
    vis = G.gorunur(p)
    for c, (lo, hi, n) in kut.items():
        if (hi - lo).max() > 700: continue
        ic = False
        for b in PU_KUTULAR:
            if lo[0] < b[1] - 0.5 and hi[0] > b[0] + 0.5 and lo[1] < b[3] - 0.5 and hi[1] > b[2] + 0.5 and lo[2] < b[5] - 0.5 and hi[2] > b[4] + 0.5: ic = True
        if not ic: continue
        if lo[0] >= LIN_X0 + 1 - 0.01 and hi[0] <= 2440.01 and lo[2] >= -570.01 and hi[2] <= 38.01: continue   # oda içi / taban geçişi (kovanlar ayrı)
        icb = False
        for b in CAV_IN:
            if lo[0] >= b[0] and hi[0] <= b[1] and lo[1] >= b[2] and hi[1] <= b[3] and lo[2] >= b[4] and hi[2] <= b[5]: icb = True
        if icb: continue
        m = (tl == c) & vis; V = p["X"][np.unique(p["T"][m].reshape(-1))]
        tm = trimesh.Trimesh(V, process=False).convex_hull
        ss = kati(np.asarray(tm.vertices), np.asarray(tm.faces))
        gomulu += ss; gom_ad.append("%s#%d [%.0f-%.0f %.0f-%.0f %.0f-%.0f]" % (nm.replace("TOPPING_MODUL__", ""), c, lo[0], hi[0], lo[1], hi[1], lo[2], hi[2]))
rap.append("GÖMÜLÜ %d: %s" % (len(gom_ad), " · ".join(gom_ad)))
print("gömülü", len(gom_ad), "%.0f s" % (time.time() - t0))


def dus(s, al):
    al = [a for a in al if TG._kesisir_bb(bb(a), bb(s), 0.0)]
    return kes(s, al) if al else s


YENI = []   # (dugum, ad, kati)
# ================================================================ 4 · ASTAR (ana oda + cep)
cav_out = K(1495.0, 2441.0, 1110.5, 2141.0, -571.0, 38.0).fuse(K(LIN_X0, 1496.0, 1110.5, 2141.0, -571.0, CEP_LIN_ZF))
cav_in = K(*CAV_IN[0]).fuse(K(*CAV_IN[1]))
astar = tekle(cav_out.cut(cav_in))
astar = dus(astar, gomulu + [TG.pencere_prizma(-572.0, -569.0)])
YENI.append(("TOPPING_MODUL__paslanmaz", "soguk_ic_kaplama_cepli", astar))
# ================================================================ 5 · TAŞIYICI RAF + bükümler + köşebentler
XR0 = LIN_X0 + 1.0                                     # 1311 astar iç yüzü
MANDAL = {"kasar": (1932.5 + DX["kasar"], 1940.5 + DX["kasar"]), "sucuk": (2244.5 + DX["sucuk"], 2252.5 + DX["sucuk"])}   # kilit dili x (kaset ön yüzü önünde, z -199,5…-193,5)
MZ = (-199.5, -193.5)
ZPF = CEP_LIN_ZF - 1.0                                 # cep astarı ön iç yüzü (−15): cepte raf / büküm / alt PU / köşebent burada biter
delik = [S_(21.5, (1596.0 + DX["kiyma"], 1140, Z_H), (1596.0 + DX["kiyma"], 1160, Z_H)),
         S_(21.5, (1806.0 + DX["kusbasi"], 1140, Z_H), (1806.0 + DX["kusbasi"], 1160, Z_H)),
         S_(18.6, (X_L, 1140, Z_H), (X_L, 1160, Z_H)), S_(18.6, (X_R, 1140, Z_H), (X_R, 1160, Z_H))]
delik += [K(XR0 - 1, 1496.0, 1140.0, 1160.0, ZPF, 30.0)]
delik += [K(a, b, 1140.0, 1160.0, -181.0, 24.0) for a, b in YARIK_X]
delik += [K(a - 0.5, b + 0.5, 1140.0, 1160.0, MZ[0] - 0.5, MZ[1] + 0.5) for a, b in MANDAL.values()]
raf = kes(K(XR0, 2440.0, 1149.0, 1152.0, -570.0, 23.0), delik)
on_b = kes(K(1496.0, 2440.0, 1110.5, 1149.0, 20.0, 23.0), [K(a, b, 1142.5, 1150.0, 19.0, 24.0) for a, b in YARIK_X])
on_b_cep = K(XR0, 1496.0, 1110.5, 1149.0, ZPF - 3.0, ZPF)
arka_b = K(XR0, 2440.0, 1110.5, 1149.0, -570.0, -567.0)
kb_sol = tekle(K(XR0, XR0 + 3, 1110.5, 1149.0, -567.0, ZPF - 3.0).fuse(K(XR0 + 3, XR0 + 40, 1146.0, 1149.0, -567.0, ZPF - 3.0)))
kb_sag = tekle(K(2437.0, 2440.0, 1110.5, 1149.0, -567.0, 20.0).fuse(K(2400.0, 2437.0, 1146.0, 1149.0, -567.0, 20.0)))
for ad, s in (("tasiyici_raf_3mm", raf), ("raf_on_bukumu", on_b), ("raf_on_bukumu_cep", on_b_cep), ("raf_arka_bukumu", arka_b), ("raf_kosebendi_sol", kb_sol), ("raf_kosebendi_sag", kb_sag)):
    YENI.append(("TOPPING_MODUL__paslanmaz", ad, s))
# ================================================================ 6 · TABAN GEÇİŞ KOVANLARI (yeni x) + alt PU + alt sac
TG.TABAN_GECIS = {"kiyma": [(1577.0 + DX["kiyma"], 1615.0 + DX["kiyma"], -189.0, -151.0)],
                  "kusbasi": [(1787.0 + DX["kusbasi"], 1825.0 + DX["kusbasi"], -189.0, -151.0)],
                  "kasar": [(2023.0 + DX["kasar"], 2101.0 + DX["kasar"], -161.0, -139.0), (2029.0 + DX["kasar"], 2095.0 + DX["kasar"], -182.5, -117.0)],
                  "sucuk": [(2272.0 + DX["sucuk"], 2350.0 + DX["sucuk"], -161.0, -139.0), (2278.0 + DX["sucuk"], 2344.0 + DX["sucuk"], -182.5, -117.0)]}
TG.TABAN_YUVARLAK = {"sos": (X_R, -169.8, 15.5), "harc": (X_L, -169.8, 15.5)}   # yayıcı uzatma borusu Ø30 ekseni (x, −169,8)
TK, TKD = TG.taban_kovanlari()
for (a, b_), k in zip(YARIK_X, ("kasar", "sucuk")):        # kaset dili kovanın ön duvarının üstünden geçer (v8w'de 4 mm çakışıyordu) → duvarda dil çentiği
    TK["soguk_taban_gecis_kovani_%s" % k] = kes(TK["soguk_taban_gecis_kovani_%s" % k], [K(a, b_, 1142.5, 1150.0, -120.0, -112.0)])
for ad, s in TK.items(): YENI.append(("TOPPING_MODUL__paslanmaz", ad, s))
ic_del = [TG._rect_birlesim(rs, 0.0, 1107.0, 1112.0) for rs in TG.TABAN_GECIS.values()]
ic_del += [S_(r, (x, 1107.0, z), (x, 1112.0, z)) for x, z, r in TG.TABAN_YUVARLAK.values()]
# mandal gövdesi cebi (alt PU)
MG_KUTU = {k: (a - 8.0, b + 8.0, 1124.0, 1149.0, -214.0, -180.0) for k, (a, b) in MANDAL.items()}
altpu = K(XR0 + 3, 2437.0, 1110.5, 1149.0, -567.0, 20.0)
altpu = kes(altpu, TKD + [K(XR0 + 3, XR0 + 40, 1146.0, 1149.5, -568.0, 21.0), K(2400.0, 2437.0, 1146.0, 1149.5, -568.0, 21.0),
                          K(XR0, 1496.0, 1110.0, 1150.0, ZPF - 3.0, 21.0)]
            + [K(a - 1.0, b + 1.0, 1143.0, 1150.0, -117.0, 21.0) for a, b in YARIK_X] + [K(*v) for v in MG_KUTU.values()])
YENI.append(("TOPPING_MODUL__pu", "soguk_oda_PU_alt_cepli", altpu))
altsac = tekle(K(1437.5, 2498.5, 1109.0, 1110.5, -628.5, 38.0).fuse(K(X_O + 1.5, 1437.5, 1109.0, 1110.5, -628.5, CEP_ZF - 1.5)))
altsac = kes(altsac, ic_del)
YENI.append(("TOPPING_MODUL__paslanmaz", "alt_yalitim_saci_cepli", altsac))
# ================================================================ 7 · ÖN EŞİK + dil kanalları + ön çerçeve (yeni YARIK_X)
TG.YARIK_X = YARIK_X
ES, EP = TG.esik()
for nm in list(ES):
    if nm.startswith("soguk_raf_dil_kanali_tabani"): del ES[nm]
for (a, b), nm in zip(YARIK_X, ("kasar", "sucuk")):
    ES["soguk_raf_dil_kanali_tabani_%s" % nm] = K(a, b, 1143.0, 1144.0, -116.0, 20.0)   # raf yarığıyla aynı genişlik: yarıktan bakınca PU görünmez
for ad, s in ES.items(): YENI.append(("TOPPING_MODUL__paslanmaz", ad, s))
for ad, s in EP.items(): YENI.append(("TOPPING_MODUL__pu", ad, s))
MG, _MK = TG.menteseler()
YENI.append(("TOPPING_MODUL__paslanmaz", "onyuz_on_cerceve_430", TG.on_cerceve(MG)))
# ================================================================ 8 · ARKA DIŞ SAC (cep dahil) + PU DUVAR
arka = tekle(K(1437.5, 2498.5, 1109.0, 2198.5, -630.0, -628.5).fuse(K(X_O + 1.5, 1437.5, 1109.0, CEP_Y1, -630.0, -628.5)))
arka = dus(arka, gomulu + [TG.pencere_prizma(-631.0, -627.5)])
YENI.append(("TOPPING_MODUL__paslanmaz", "soguk_arka_dis_sac_cepli", arka))
pu = tekle(K(*PU_KUTULAR[0]).fuse(K(*PU_KUTULAR[1])))
pu = tekle(pu.cut(cav_out))
pu = tekle(pu.cut(TG.pencere_prizma(-640.0, -570.0)))
bas = []
for g in gomulu:
    if not TG._kesisir_bb(bb(g), bb(pu), 0.0): continue
    try:
        r = pu.cut(g)
        if r.isNull() or r.Volume() <= 0: raise ValueError("boş")
        pu = tekle(r)
    except Exception as e:
        pu = tekle(pu.cut(K(*bb(g)))); bas.append(str(bb(g)))
if bas: rap.append("UYARI PU kutu ile düşüldü: " + "; ".join(bas))
YENI.append(("TOPPING_MODUL__pu", "soguk_oda_PU_duvar_cepli", pu))
print("PU %.0f s" % (time.time() - t0))
# ================================================================ 9 · ÜST RAF (cebe uzar, hortum delikleri X_L / X_R)
ur = kes(K(XR0, 2440.0, 1572.0, 1575.0, -570.0, -50.0), [S_(20.3, (x, 1570, -172.45), (x, 1577, -172.45)) for x in (X_L, X_R)])
YENI += [("TOPPING_MODUL__paslanmaz", "ust_raf_3mm", ur),
         ("TOPPING_MODUL__paslanmaz", "ust_raf_on_bukumu", K(XR0, 2440.0, 1534.0, 1572.0, -53.0, -50.0)),
         ("TOPPING_MODUL__paslanmaz", "ust_raf_arka_bukumu", K(XR0, 2440.0, 1534.0, 1572.0, -570.0, -567.0)),
         ("TOPPING_MODUL__paslanmaz", "ust_raf_kosebendi_sol", tekle(K(XR0, XR0 + 3, 1532.0, 1572.0, -567.0, -53.0).fuse(K(XR0 + 3, XR0 + 40, 1569.0, 1572.0, -567.0, -53.0)))),
         ("TOPPING_MODUL__paslanmaz", "ust_raf_kosebendi_sag", tekle(K(2437.0, 2440.0, 1532.0, 1572.0, -567.0, -53.0).fuse(K(2400.0, 2437.0, 1569.0, 1572.0, -567.0, -53.0))))]
# ================================================================ 10 · DIŞ YAN SOL (cep ağzı) + CEP SACLARI + A sağ levha
cep_agiz = K(1433.0, 1438.5, 1109.0, CEP_Y1, -630.0, CEP_ZF)
sol = [K(TG.X0 - 1, TG.XI0 + 1, TG.YBI, 1042.0, -510.0, 5.0), K(TG.X0 - 1, TG.XI0 + 1, 2142.0, 2167.5, -827.0, -765.0)]
sol += [S_(8.2, (TG.X0 - 1, yc, -720.1), (TG.XI0 + 1, yc, -720.1)) for yc in (1612.0, 1640.0)] + [cep_agiz]
YENI.append(("TOPPING_MODUL__sac", "dis_yan_sol", kes(K(TG.X0, TG.XI0, TG.YB, TG.YTI, TG.ZA, TG.ZF), sol)))
YENI += [("TOPPING_MODUL__sac", "cep_sol_sac", K(X_O, X_O + 1.5, 1109.0, CEP_Y1, -630.0, CEP_ZF)),
         ("TOPPING_MODUL__sac", "cep_ust_sac", K(X_O + 1.5, 1437.5, CEP_Y1 - 1.5, CEP_Y1, -628.5, CEP_ZF - 1.5)),
         ("TOPPING_MODUL__sac", "cep_on_sac", K(X_O + 1.5, 1437.5, 1109.0, CEP_Y1, CEP_ZF - 1.5, CEP_ZF))]
a_del = [K(1433.0, 1437.0, 894.0, 1042.0, -510.0, 4.0), cep_agiz, K(1433.0, 1437.0, 2142.0, 2167.5, -827.0, -765.0)]   # tabla geçişi · cep · ana hat kanalı
a_del += [S_(8.2, (1433.0, yc, -720.1), (1437.0, yc, -720.1)) for yc in (1612.0, 1640.0)]                                  # TOPPING yan sacındaki rakor delikleriyle aynı
YENI.append(("A_GOVDE__sac", "A_sag_levha_cep_agizli", kes(K(1434.5, 1436.0, 788.0, 2198.5, -830.0, 59.0), a_del)))
print("katılar %.0f s" % (time.time() - t0))

# ================================================================ 11 · GLB'ye ekle
REF = {"TOPPING_MODUL__paslanmaz": ETK["TOPPING_MODUL__paslanmaz"], "TOPPING_MODUL__pu": ETK["TOPPING_MODUL__pu"],
       "TOPPING_MODUL__sac": ETK["TOPPING_MODUL__sac"], "A_GOVDE__sac": ETK["A_GOVDE__sac"]}
for nd, ad, s in YENI:
    Pp, I = G.ag([s])
    p = P(nd); kt, mk = REF[nd]
    G.ekle_etiket(p, Pp, I, kat=kt, mek=mk)
    b = bb(s); rap.append("YENI %-26s %-40s x %7.1f %7.1f y %7.1f %7.1f z %7.1f %7.1f  %d üçgen" % (nd.replace("TOPPING_MODUL__", ""), ad, *b, len(I)))
G.kaydet(go)
open(go.replace(".glb", "_rapor.txt"), "w", encoding="utf-8").write("\n".join(rap))
print("\n".join(r for r in rap if not r.startswith("GÖMÜLÜ")))
print("yazildi", go, "%.0f s" % (time.time() - t0))
sys.stdout.flush(); os._exit(0)
