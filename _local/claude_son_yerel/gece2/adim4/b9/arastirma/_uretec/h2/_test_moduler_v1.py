# -*- coding: utf-8 -*-
"""TEST · h2_moduler_v1 (+ h2_acici_v1 kaide oturması) — HAT v2 (30 Eyl 2026 · Claude · YEREL). YALNIZ TEST: montaja girmez.
1 · v1 TABAN: moduler_montaj_v4 v1 girdileriyle (store_cad_v14 · kesme_cad_v11 · kutu_cad_v14 · acici_kabin_cad_v1 · kaide_cad_v4 · topping_cad_v32) koşar.
2 · v2: h2_moduler_v1 v2 girdileriyle koşar. h2_store_v1 / h2_kaide_v1 (başka ajanlar) YOKSA ya da yüklenemezse ARA MODEL (yalnız bu dosyada):
      store_cad_v14 / kaide_cad_v4 dünya parçaları dilimlenir — dilimin solu +DXL, içi çıkar, sağı yerinde; dilimi kesen parçalar kes + taşı + birleştir
      (dolap dilimi B_DILIM 1992,5–2500 · C kaidesi dilimi C_DILIM 1106,5–1614 · A kaidesi tümüyle +DXL). TC = RAKOR_ACICI taşıyan ad alanı (topping_cad_v32).
3 · denetimler: A tarafı v1'in birebir +DXL'i (yeni + değişen parçalar) · K / E aynı · B dikmeleri bölme PU'sunda · TD ortak kullanımı · kirişler B içinde ·
    A çerçevesi A içinde · yeni parçalar ↔ mevcut + birbirleri + TOPPING sabitleri çakışma > 0,1 mm³ (v1'de de olan temaslar hariç — v1 aynı ölçütle ölçülür) ·
    A duvarı ↔ C yan sacı derzi · A kabini ↔ A kaidesi oturma.
Çalıştır: python ob_calistir.py h2/_test_moduler_v1.py"""
import os, sys, time, types
H2 = os.path.dirname(os.path.abspath(__file__)); U = os.path.dirname(H2)
for _p in (U, H2):
    if _p not in sys.path: sys.path.insert(0, _p)
import cadquery as cq
import h2_hesap_v1 as H

V = cq.Vector
T0 = time.time()
DEN = []


def kontrol(ad, sart, deger=""):
    DEN.append((ad, bool(sart), deger)); print("  %-160s %s %s" % (ad, "GEÇTİ" if sart else "** KALDI **", deger), flush=True)


def kut(x0, x1, y0, y1, z0, z1):
    return cq.Solid.makeBox(x1 - x0, y1 - y0, z1 - z0, V(x0, y0, z0))


def tek(wp):
    v = [o for o in wp.vals() if isinstance(o, cq.Shape)]
    return v[0] if len(v) == 1 else cq.Compound.makeCompound(v)


def bbt(s):
    b = s.BoundingBox(); return (b.xmin, b.xmax, b.ymin, b.ymax, b.zmin, b.zmax)


def bbk(a, b, pay=0.01):
    return all(min(a[2 * i + 1], b[2 * i + 1]) - max(a[2 * i], b[2 * i]) > pay for i in range(3))


def dilimle(sh, L, R, dx):
    """ARA MODEL: v1 dünya şeklinden [L, R] dilimini çıkarır — solu +dx, içi YOK (None), sağı yerinde · dilimi kesen parça kes + taşı + birleştir"""
    b = sh.BoundingBox()
    if b.xmax <= L + 1e-6: return sh.translate(V(dx, 0, 0))
    if b.xmin >= R - 1e-6: return sh
    if b.xmin >= L - 1e-6 and b.xmax <= R + 1e-6: return None
    ss = []
    if b.xmin < L:
        s = sh.intersect(kut(b.xmin - 10, L, b.ymin - 10, b.ymax + 10, b.zmin - 10, b.zmax + 10))
        if s.Volume() > 1e-6: ss.append(s.translate(V(dx, 0, 0)))
    if b.xmax > R:
        s = sh.intersect(kut(R, b.xmax + 10, b.ymin - 10, b.ymax + 10, b.zmin - 10, b.zmax + 10))
        if s.Volume() > 1e-6: ss.append(s)
    if not ss: return None
    if len(ss) == 1: return ss[0]
    try:
        return ss[0].fuse(ss[1]).clean()
    except Exception:
        return cq.Compound.makeCompound(ss)


# ================================================================ 1 · v1 GİRDİLERİ ================================================================
import store_cad_v14 as SC14, kesme_cad_v11 as KS, kutu_cad_v14 as KC, acici_kabin_cad_v1 as AK1, kaide_cad_v4 as KD4, topping_cad_v32 as TC32
import moduler_montaj_v4 as M4
SC14.PARCALAR[:] = []; SC14.modul()
KS.modul(); KC.modul(); AK1.kur(); KD4.kur()
print("v1 girdileri: store %d · K %d · E %d · A %d · kaide %d parça · %.0f sn" % (len(SC14.PARCALAR), len(KS.PARCALAR), len(KC.PARCALAR), len(AK1.PARCALAR), len(KD4.PARCALAR), time.time() - T0), flush=True)

# ================================================================ 2 · v2 GİRDİLERİ (gerçek ya da ARA MODEL) — v1 moduler çalışmadan ÖNCE (v1 parçaları yerinde değişir) ================================================================
DXL = H.DXL
ARA = "ara" in sys.argv[1:]                                                             # "ara": gerçek h2_store_v1 / h2_kaide_v1 olsa da ARA MODEL kullan
try:
    if ARA: raise ImportError("ara bayrağı")
    import h2_store_v1 as SC2
    if not SC2.PARCALAR: SC2.modul()
    SC_KAYNAK = "GERÇEK h2_store_v1 (%d parça)" % len(SC2.PARCALAR)
except Exception as e:
    t1 = time.time(); _sp = []
    for p in SC14.PARCALAR:
        s = dilimle(tek(p["wp"]), H.B_DILIM[0], H.B_DILIM[1], DXL)
        if s is not None: _sp.append(dict(p, wp=cq.Workplane(obj=s)))
    SC2 = types.SimpleNamespace(PARCALAR=_sp)
    SC_KAYNAK = "ARA MODEL (h2_store_v1 yok: %s) · store_cad_v14 dilimli %d / %d parça · %.0f sn" % (str(e)[:70], len(_sp), len(SC14.PARCALAR), time.time() - t1)
try:
    if ARA: raise ImportError("ara bayrağı")
    import h2_kaide_v1 as KD2
    KD2.kur()
    KD_KAYNAK = "GERÇEK h2_kaide_v1 (%d parça)" % len(KD2.PARCALAR)
except Exception as e:
    _kp = []
    for p in KD4.PARCALAR:
        s = tek(p["wp"]).translate(V(DXL, 0, 0)) if p["birim"] == "KAIDE_A" else dilimle(tek(p["wp"]), H.C_DILIM[0], H.C_DILIM[1], DXL)
        if s is not None: _kp.append(dict(p, wp=cq.Workplane(obj=s)))
    KD2 = types.SimpleNamespace(PARCALAR=_kp)
    KD_KAYNAK = "ARA MODEL (h2_kaide_v1 yok: %s) · kaide_cad_v4 A +DXL, C dilimli %d parça" % (str(e)[:70], len(_kp))
TC2 = types.SimpleNamespace(RAKOR_ACICI=TC32.RAKOR_ACICI)
print("SC v2: %s\nKD v2: %s" % (SC_KAYNAK, KD_KAYNAK), flush=True)
# TOPPING sabitleri A|C sınırında (montaj _tc72 süzgeci: _bom yok · v1_kalir · grup SABIT · V1_TASI · X_BC 700 · Y_MEK 892 · xmin < 710) → v2 = + DXL
if not TC32.PARCALAR: TC32.modul()
_TCB1 = []
for p in TC32.PARCALAR:
    if p["ad"].startswith("_bom") or not KD4.v1_kalir(p["ad"]) or AK1.grup_tc(p["ad"]) != "SABIT": continue
    d_ = AK1.V1_TASI.get(p["ad"], (0.0, 0.0, 0.0))
    sh = tek(p["wp"]).translate(V(700.0 + d_[0], 892.0 + d_[1], d_[2]))
    if sh.BoundingBox().xmin < 710.0: _TCB1.append(("TOPPING:" + p["ad"], sh))
_TCB2 = [(a, s.translate(V(DXL, 0, 0))) for a, s in _TCB1]
print("TOPPING sabitleri A|C sınırında: %d parça (v1 xmin < 710 → v2 + %.1f)" % (len(_TCB1), DXL), flush=True)

# ================================================================ 3 · v1 TABAN ÇALIŞMASI ================================================================
t1 = time.time()
Y1 = M4.uygula(types.SimpleNamespace(SC=SC14, KS=KS, KC=KC, AK=AK1, KD=KD4, TC=TC32, X_K=4000.0, X_E=4400.0, Y_MEK=892.0))
N1 = {p["name"]: p for p in Y1}
D1 = list(M4.DEGISEN)
E1 = {(p["module"], p["name"]): p["shape"] for p in M4.PARTS if not p["new"]}                  # v1 mevcut parçalar (değişmiş halleriyle)
print("v1 moduler_montaj_v4: %d yeni · %d değişen · %.0f sn" % (len(Y1), len(D1), time.time() - t1), flush=True)
assert not any(d.startswith(("K:", "E:")) for d in D1), "v1 K/E parçası değişti — KS/KC v2 için temiz değil"

# ================================================================ 4 · v2 ÇALIŞMASI ================================================================
import h2_acici_v1 as AK2, h2_moduler_v1 as M2
AK2.kur()                                                                              # v1 kabinini baştan kurar (v1 moduler'in değiştirdikleri atılır) → +DXL
t1 = time.time()
Y2 = M2.uygula(types.SimpleNamespace(SC=SC2, KS=KS, KC=KC, AK=AK2, KD=KD2, TC=TC2, X_K=4000.0, X_E=4400.0, Y_MEK=892.0))
N2 = {p["name"]: p for p in Y2}
D2 = list(M2.DEGISEN)
E2 = {(p["module"], p["name"]): p["shape"] for p in M2.PARTS if not p["new"]}
print("v2 h2_moduler_v1: %d yeni · %d değişen · %.0f sn" % (len(Y2), len(D2), time.time() - t1), flush=True)
print("KONUMLAR (v1 → v2):")
for ad_, a_, b_ in M2.KONUMLAR:
    print("   %-62s %s → %s" % (ad_, a_, tuple(round(v, 2) for v in b_) if isinstance(b_, tuple) else round(b_, 2)))
print("YENİ PARÇALAR v2:")
for p in Y2:
    b = bbt(p["shape"])
    print("   %-36s %-2s %-5s %-8s x %8.2f %8.2f y %7.2f %7.2f z %8.2f %8.2f" % (p["name"], p["module"], p["material"], p["kind"], *b))
print("DEĞİŞEN v2: %s" % D2)
print("DENETİM (h2_moduler_v1 · %s · %s)" % (SC_KAYNAK.split(" (")[0], KD_KAYNAK.split(" (")[0]), flush=True)


def fark_dx(s2, s1, dx):
    a, b = bbt(s2), bbt(s1)
    return max(abs(a[0] - b[0] - dx), abs(a[1] - b[1] - dx), *(abs(a[i] - b[i]) for i in range(2, 6)), abs(s2.Volume() - s1.Volume()))


# ---- A: yeni parçalar + değişen parçalar = v1 + DXL ----
a1 = [n for n, p in N1.items() if p["module"] == "A"]; a2 = [n for n, p in N2.items() if p["module"] == "A"]
fa = max(fark_dx(N2[n]["shape"], N1[n]["shape"], DXL) for n in a1) if a1 == a2 else 1e9
kontrol("A YENİ parçalar (%s) = v1 + %.1f x (sınır kutusu + hacim) · en büyük sapma %.2e" % (", ".join(a2), DXL, fa), a1 == a2 and fa < 1e-6)
da1 = sorted(d for d in D1 if d.startswith("A:")); da2 = sorted(d for d in D2 if d.startswith("A:"))
fd = max(fark_dx(E2[("A", d[2:])], E1[("A", d[2:])], DXL) for d in da1) if da1 == da2 else 1e9
kontrol("A DEĞİŞEN mevcut parçalar (%d: sağ çerçeve −2 kayan 7 + kırpılan / kesilen 6) = v1 + %.1f x · en büyük sapma %.2e" % (len(da2), DXL, fd), da1 == da2 and fd < 1e-6, str(sorted(set(da1) ^ set(da2))))
fak = max(fark_dx(E2[("A", p["ad"])], E1[("A", p["ad"])], DXL) for p in AK2.PARCALAR)
kontrol("A kabininin BÜTÜN parçaları (%d) montaj sonrası = v1 montaj sonrası + %.1f x · en büyük sapma %.2e" % (len(AK2.PARCALAR), DXL, fak), fak < 1e-6)
ain = [(n, bbt(N2[n]["shape"])) for n in a2]
kontrol("A çerçevesi + kendi sağ duvarı A içinde (x %.1f–%.1f): %s" % (H.A_X[0], H.A_X[1], " · ".join("%s x %.1f–%.1f" % (n.replace("A_", ""), b[0], b[1]) for n, b in ain)),
        all(H.A_X[0] - 1e-6 <= b[0] and b[1] <= H.A_X[1] + 1e-6 for _n, b in ain))
# ---- K / E aynı ----
ke1 = sorted(n for n, p in N1.items() if p["module"] in ("K", "E")); ke2 = sorted(n for n, p in N2.items() if p["module"] in ("K", "E"))
fke = max(fark_dx(N2[n]["shape"], N1[n]["shape"], 0.0) for n in ke1) if ke1 == ke2 else 1e9
kontrol("K / E yeni parçaları (%d) v1 ile birebir · sapma %.2e · K / E mevcut parça değişmedi" % (len(ke2), fke), ke1 == ke2 and fke < 1e-6 and not any(d.startswith(("K:", "E:")) for d in D2))
# ---- B ----
ort = list(M2.B_AC_ORTAK)
kontrol("TD ORTAK: z −110 hattında B4 ekseni x %.1f'te fırın taşıyıcı dikmesi ORTAK kullanıldı, ikinci dikme YOK: %s" % (M2.TD_X0, ort),
        ort == [(0, 3, M2.TD_X0, -110.0, "tasiyici_dikme_0")] and not any(n.endswith("_0_3") for n in N2))
b1 = sorted(n for n, p in N1.items() if p["module"] == "B" and n.startswith("B_AC_")); b2 = sorted(n for n, p in N2.items() if p["module"] == "B" and n.startswith("B_AC_"))
kontrol("B/AC parça adları = v1 − {B_AC_dikme_0_3, B_AC_alt_isikesici_0_3, B_AC_alt_pabucluk_0_3} (TD ortak) · %d parça" % len(b2),
        b2 == sorted(set(b1) - {"B_AC_dikme_0_3", "B_AC_alt_isikesici_0_3", "B_AC_alt_pabucluk_0_3"}))
SC2P = {p["ad"]: tek(p["wp"]) for p in SC2.PARCALAR}                                     # (geri yazılmış, kesilmiş haller)
S0 = {p["name"]: p["s0"] for p in M2.PARTS if not p["new"] and p["module"] == "B"}       # dolabın moduler ÖNCESİ şekilleri
pu = [(n, bbt(s)) for n, s in S0.items() if n.startswith(("bolme_", "yan_pu_sol")) and "_pu" in n]
dik = []
for n in sorted(n for n in N2 if n.startswith("B_AC_dikme_")):
    b = bbt(N2[n]["shape"])
    ev = [pn for pn, pb in pu if pb[0] - 1e-6 <= b[0] and b[1] <= pb[1] + 1e-6 and pb[4] - 1e-6 <= b[4] and b[5] <= pb[5] + 1e-6]
    dik.append((n, (b[0] + b[1]) / 2.0, ev[0] if ev else None))
kontrol("B/AC DİKMELERİ bölme / sol duvar PU'sunun içinde (x ± 15): %s" % " · ".join("%s x %.1f ⊂ %s" % (n.replace("B_AC_dikme_", "d"), x, e) for n, x, e in dik), all(e for _n, _x, e in dik))
exp_x = {0: M2.B_AC_DIKME_X[0], 1: M2.B_AC_DIKME_X[1], 2: M2.B_AC_DIKME_X[2], 3: M2.B_AC_DIKME_X[3]}
kontrol("B/AC dikme eksenleri %s = h2_hesap'tan (sol duvar B_X[0] + 17 · B1 / B2 v1 + DXL · B4 B_DILIM[1] + 17,5)" % sorted(set(round(x, 2) for _n, x, _e in dik)),
        all(abs(x - exp_x[int(n[-1])]) < 1e-6 for n, x, _e in dik))
kr = [(n, bbt(N2[n]["shape"])) for n in ("B_AC_ust_kiris_0", "B_AC_ust_kiris_1", "B_AC_ust_isikesici_0", "B_AC_ust_isikesici_1")]
kontrol("B/AC kirişleri dolabın içinde (x %.1f–%.0f · y ≤ 788): %s" % (H.B_X[0], H.B_X[1], " · ".join("%s x %.1f–%.1f" % (n.replace("B_AC_ust_", ""), b[0], b[1]) for n, b in kr)),
        all(H.B_X[0] <= b[0] and b[1] <= H.B_X[1] and b[3] <= 788.0 + 1e-6 for _n, b in kr)
        and abs(kr[0][1][1] - M2.TK_X0) < 1e-6 and abs(kr[1][1][1] - (M2.TD_X0 + 15.0)) < 1e-6 and abs(kr[0][1][0] - (H.B_X[0] + 2.0)) < 1e-6)
ZU = list(M2.B_AC_Z_UYGULANAN)
print("   B/AC hatları (i, v1 z, uygulanan z, v1 z'deki engeller): %s" % ZU, flush=True)
if SC_KAYNAK.startswith("ARA"):
    kontrol("B/AC hatları ARA MODELDE v1 z'sinde (engel yok → kaydırma yok): %s" % [(z0, z) for _i, z0, z, _e in ZU], all(z == z0 and not e for _i, z0, z, e in ZU))
else:
    gp = [(n, s) for n, s in S0.items() if n.startswith("gider_ana_hatti")]
    dd = [(n.replace("B_AC_", ""), g.replace("gider_ana_hatti_", ""), N2[n]["shape"].distance(s)) for n in sorted(N2) if n.startswith("B_AC_dikme_") for g, s in gp
          if abs((bbt(N2[n]["shape"])[0] + bbt(N2[n]["shape"])[1]) / 2.0 - (bbt(s)[0] + bbt(s)[1]) / 2.0) < 400.0 or g.endswith("borusu")]
    dmin = min(d for _a, _b, d in dd) if dd else 1e9
    kontrol("GERÇEK dolap: B/AC hatları %s · kayan hattın dikmeleri ↔ gider ana hattı (boru + kılıflar) en yakın %.2f mm ≥ %.0f"
            % ([(z0, z, e) for _i, z0, z, e in ZU], dmin, M2.B_AC_BOSLUK), dmin >= M2.B_AC_BOSLUK - 1e-3 and ZU[0][2] == ZU[0][1])
zA = ZU[1][2]
tdp, tdk = S0["tasiyici_dikme_0"], S0["tasiyici_kiris_on"]
k0, k1_, d13 = N2["B_AC_ust_kiris_0"]["shape"], N2["B_AC_ust_kiris_1"]["shape"], N2["B_AC_dikme_1_3"]["shape"]
tm = [("kiriş z−110 ↔ TD dikmesi (tasiyici_dikme_0)", k0.distance(tdp), k0.intersect(tdp).Volume()), ("kiriş z−110 ↔ fırın ön taşıyıcı kirişi", k0.distance(tdk), k0.intersect(tdk).Volume()),
      ("kiriş z%.0f ↔ yeni B4 dikmesi (1_3)" % zA, k1_.distance(d13), k1_.intersect(d13).Volume())]
kontrol("TEMASLAR (alın alına / üstüne oturur): " + " · ".join("%s: aralık %.3f mm · kesişim %.3f mm³" % t for t in tm), all(abs(d) < 1e-3 and v <= 0.1 for _a, d, v in tm))
# v1'de de aynı temaslar vardı (kiriş z−110 sağ ucu 2502,5 ↔ fırın ön taşıyıcı kirişi)
tv1 = N1["B_AC_ust_kiris_0"]["shape"].distance(E1[("B", "tasiyici_kiris_on")])
kontrol("v1'de kiriş z−110 sağ ucu da 2502,5'te fırın ön taşıyıcı kirişine alın alına (aralık %.3f mm) → v2 teması v1'dekiyle aynı cins" % tv1, abs(tv1) < 1e-3)
# ---- çakışma: yeni ↔ mevcut (değişmiş) + TOPPING sınır sabitleri · yeni ↔ yeni — v1 aynı ölçütle ----


def carpis(YY, PP, TCB, esik=0.1):
    out = []
    kars = [("%s:%s" % (p["module"], p["name"]), p["shape"], bbt(p["shape"])) for p in PP if not p["new"]] + [(a, s, bbt(s)) for a, s in TCB]
    yy = [(p["name"], p["shape"], bbt(p["shape"])) for p in YY if p["kind"] != "connection"]
    for n, s, b in yy:
        for c, sc, bc in kars:
            if bbk(b, bc):
                v = s.intersect(sc).Volume()
                if v > esik: out.append((round(v, 3), n, c))
    for i, (n, s, b) in enumerate(yy):
        for m, sm, bm in yy[i + 1:]:
            if bbk(b, bm):
                v = s.intersect(sm).Volume()
                if v > esik: out.append((round(v, 3), n, "YENI:" + m))
    return out


t1 = time.time()
P1 = list(M4.PARTS)                                                                     # (v1 PARTS listesi M4.uygula sonrası; M2 ayrı modül)
C1 = carpis(Y1, P1, _TCB1); C2 = carpis(Y2, M2.PARTS, _TCB2)
print("   (mevcut parça listesi v1 %d · v2 %d · ad çiftleri tekil: v1 %s · v2 %s)" % (sum(1 for p in P1 if not p["new"]), sum(1 for p in M2.PARTS if not p["new"]),
      len(E1) == sum(1 for p in P1 if not p["new"]), len(E2) == sum(1 for p in M2.PARTS if not p["new"])), flush=True)
k1s = {(a, c) for _v, a, c in C1}
yeni_b = [x for x in C2 if (x[1], x[2]) not in k1s]
print("   ÇAKIŞMA (> 0,1 mm³): v1 %d · v2 %d · %.0f sn" % (len(C1), len(C2), time.time() - t1), flush=True)
for x in sorted(C1, reverse=True)[:12]: print("      v1 %10.3f mm3  %-32s <-> %s" % x)
for x in sorted(C2, reverse=True)[:12]: print("      v2 %10.3f mm3  %-32s <-> %s" % x)
kontrol("YENİ parçalar (bağlantı hariç %d) ↔ mevcut dolap / K / E / A / kaide (moduler sonrası) + TOPPING A|C sabitleri (%d) + birbirleri: > 0,1 mm³ çakışma v2 %d · v1'de OLMAYAN bulgu %d"
        % (sum(1 for p in Y2 if p["kind"] != "connection"), len(_TCB2), len(C2), len(yeni_b)), not yeni_b, str(sorted(yeni_b, reverse=True)[:8]))
kontrol("v2 çakışma listesi v1'den fazla değil (v1 %d → v2 %d; v1'deki temaslar kaynaklı birleşimler / PU dolgusu)" % (len(C1), len(C2)), len(C2) <= len(C1))
# ---- A duvarı ↔ C yan sacı (TOPPING dis_yan_sol) derzi ----
ys2 = [s for a, s in _TCB2 if a == "TOPPING:dis_yan_sol"]
if ys2:
    dw2 = N2["A_bagimsiz_sag_duvar_1p5"]["shape"].distance(ys2[0]); dw1 = N1["A_bagimsiz_sag_duvar_1p5"]["shape"].distance([s for a, s in _TCB1 if a == "TOPPING:dis_yan_sol"][0])
    kontrol("A kendi sağ duvarı ↔ C sol yan sacı derzi v2 %.3f mm = v1 %.3f mm (0,5) · duvar x %.1f–%.1f · C yan sacı x %.1f"
            % (dw2, dw1, bbt(N2["A_bagimsiz_sag_duvar_1p5"]["shape"])[0], bbt(N2["A_bagimsiz_sag_duvar_1p5"]["shape"])[1], bbt(ys2[0])[0]), abs(dw2 - 0.5) < 1e-3 and abs(dw1 - 0.5) < 1e-3)
# ---- B alt şase ----
bs = [(n, bbt(N2[n]["shape"])) for n in N2 if n.startswith("B_alt_sasi_boyuna")]
kontrol("B alt şase boyunaları x %s (v1 1,5–3998,5 → v2 %.1f–%.1f, sol dış sacın içi)" % (" · ".join("%.1f–%.1f" % (b[0], b[1]) for _n, b in bs), *M2.B_SASE_X),
        bs and all(abs(b[0] - M2.B_SASE_X[0]) < 1e-6 and abs(b[1] - M2.B_SASE_X[1]) < 1e-6 for _n, b in bs))
# ---- A kabini ↔ A kaidesi (h2_acici_v1 öz denetiminden buraya) ----
kda = [p for p in KD2.PARCALAR if p["birim"] == "KAIDE_A"]
ts = [tek(p["wp"]).BoundingBox() for p in kda if p["ad"] == "kaide_A_mekanizma_taban_saci"][0]
AK2.kur()                                                                                  # moduler öncesi kabin (v1 denetimi de öyleydi)
P_ = {p["ad"]: p for p in AK2.PARCALAR}
ot = []
for ad_ in ("a_kose_dikmesi_arka_sol", "a_kose_dikmesi_arka_sag", "onyuz_cerceve_sol_dikme", "onyuz_cerceve_sag_dikme"):
    kes = AK2.dunya(P_[ad_]).intersect(kut(H.A_X[0] - 5, H.A_X[1] + 5, AK2.Y_TABAN, AK2.Y_TABAN + 1.0, -835.0, 84.0))
    des = kut(ts.xmin, ts.xmax, AK2.Y_TABAN, AK2.Y_TABAN + 1.0, ts.zmin, ts.zmax)
    if "cerceve" in ad_:
        al = AK2.dunya(P_[ad_.replace("_dikme", "_alt_dikme")]).BoundingBox()
        des = des.fuse(kut(al.xmin, al.xmax, AK2.Y_TABAN, AK2.Y_TABAN + 1.0, al.zmin, al.zmax))
    ot.append(100.0 * kes.intersect(des).Volume() / kes.Volume())
ck = []
for p in AK2.PARCALAR:
    for q in kda:
        s1, s2 = AK2.dunya(p), tek(q["wp"])
        if bbk(bbt(s1), bbt(s2)):
            v = s1.intersect(s2).Volume()
            if v > 0.1: ck.append((round(v, 3), p["ad"], q["ad"]))
kontrol("A kabini (h2_acici_v1) ↔ A kaidesi (%s): çakışma > 0,1 mm³ %d · 4 dikme taban sacına (x %.1f–%.1f, üst %.1f) oturma %s"
        % (KD_KAYNAK.split(" (")[0], len(ck), ts.xmin, ts.xmax, ts.ymax, " · ".join("%%%.2f" % v for v in ot)), not ck and all(v >= 99.99 for v in ot), str(ck[:6]))
# ---- SAĞLAMLIK: TD dikmesinin adı değişse de ORTAK bulunur · B4 dikme yerinde yabancı çelik parça varsa çakışan dikme kurulmaz (assert) ----
_ad = [dict(p, ad=("firin_tasiyici_dikmesi_test" if p["ad"] == "tasiyici_dikme_0" else p["ad"])) for p in SC2.PARCALAR]
AK2.kur()
M2.uygula(types.SimpleNamespace(SC=types.SimpleNamespace(PARCALAR=_ad), KS=KS, KC=KC, AK=AK2, KD=KD2, TC=TC2, X_K=4000.0, X_E=4400.0, Y_MEK=892.0))
kontrol("SAĞLAMLIK · TD dikmesi yeniden adlandırılınca (firin_tasiyici_dikmesi_test) yine ORTAK kullanılır: %s" % M2.B_AC_ORTAK,
        [(i, j, n) for i, j, _x, _z, n in M2.B_AC_ORTAK] == [(0, 3, "firin_tasiyici_dikmesi_test")])
_ek = kut(2505.0, 2530.0, 300.0, 400.0, -760.0, -745.0)                                 # B4 arka dikmesinin yerinde küçük yabancı çelik parça (z −760…−745)
# (ARA MODELDE B2'de v1'in eski gider kılıfı z −698…−637 durur → öne kayma penceresi −725…−718; gerçek dolapta eski kılıf yok, gider ana hattı −750…−726)
_en = [dict(p) for p in SC2.PARCALAR] + [dict(ad="engel_test_kutusu", wp=cq.Workplane(obj=_ek), mal="celik", birim="B_TASIYICI", bom=None, grup="SABIT")]
AK2.kur()
try:
    _y = M2.uygula(types.SimpleNamespace(SC=types.SimpleNamespace(PARCALAR=_en), KS=KS, KC=KC, AK=AK2, KD=KD2, TC=TC2, X_K=4000.0, X_E=4400.0, Y_MEK=892.0))
    _d = [p["shape"] for p in _y if p["name"] == "B_AC_dikme_1_3"][0]
    _zu = M2.B_AC_Z_UYGULANAN[1]; _ara = _d.distance(_ek); _hata = None
except AssertionError as e:
    _zu, _ara, _hata = (None, None, None, []), -1.0, str(e)
kontrol("SAĞLAMLIK · B4 arka dikme yerinde yabancı parça → arka hat öne kayar %s · dikme ↔ parça aralık %.2f mm ≥ %.0f (çakışan dikme KURULMAZ)%s"
        % (_zu[:3], _ara, M2.B_AC_BOSLUK, (" · HATA " + _hata[:90]) if _hata else ""),
        not _hata and _zu[2] > _zu[1] and "engel_test_kutusu" in _zu[3] and _ara >= M2.B_AC_BOSLUK - 1e-3)
_ek2 = kut(2505.0, 2530.0, 300.0, 400.0, -760.0, -600.0)                                # 60 mm öne kayarak da kurtulunamayan engel → DUR
_en2 = [dict(p) for p in SC2.PARCALAR] + [dict(ad="engel_test_uzun", wp=cq.Workplane(obj=_ek2), mal="celik", birim="B_TASIYICI", bom=None, grup="SABIT")]
AK2.kur()
try:
    M2.uygula(types.SimpleNamespace(SC=types.SimpleNamespace(PARCALAR=_en2), KS=KS, KC=KC, AK=AK2, KD=KD2, TC=TC2, X_K=4000.0, X_E=4400.0, Y_MEK=892.0))
    _hata = None
except AssertionError as e:
    _hata = str(e)
kontrol("SAĞLAMLIK · kaydırarak kurtulunamayan engel (z −760…−600) → montaj açık mesajla DURUR: %s" % (_hata or "DURMADI")[:130], bool(_hata) and "engel_test_uzun" in _hata)
print("TEST: %d madde · %d KALDI · %.0f sn · SC %s · KD %s" % (len(DEN), sum(1 for d_ in DEN if not d_[1]), time.time() - T0, SC_KAYNAK, KD_KAYNAK), flush=True)
sys.stdout.flush(); os._exit(0 if all(d_[1] for d_ in DEN) else 1)
