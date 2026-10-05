# -*- coding: utf-8 -*-
"""GECE2 ADIM 3 · kaşar + sucuk kaseti iç çakışmaları (hat3_v8zp → v8zq). python a1_kaset.py giris.glb cikis.glb
KAŞAR (kasar_cad_v15): yatak kapağı arka alın yüzü z 236 → 238 (yerel) — çıkış borusunun ön dış yüzü (eksen z 212,5 + r 25 = 237,5) kapağın
   bayonet dudağına 1,5 mm giriyordu. Kapak yeni üreteçten (CadQuery katısı, ince ağ) birebir yerine konur.
SUCUK (sucuk_cad_v9): çıkış tüpünün koni geçişi tüp ön ucunda kırpıldı (v8'de tüp ucunun önüne 2,5 mm gaga: ön muylu 16 mm³ + kapak 2,5 mm³ içine); geçme yüzeyli 6 parça (gövde, iki plaka, ön/arka gövde contası, çıkış tüpü, yatak kapağı) kaba ağdan
   (0,12 mm / 0,35 rad: r 39 deliğin kirişi 0,6 mm içeri sarkıyordu) ince ağa (0,02 / 0,1) → kapak ↔ tüp 0,92, gövde ↔ plaka kanalı 0,22 kalkar.
   Tüp ağı ayrıca KAPALI katı olur (eski ağ açıktı → denetimde içi sorulamıyordu).
YARIK DİLİ + RAF KASET CONTASI (topping_uno_cad; POM / silikon, tüpe yaka ile sıkılı, tasarımda tüple TEMAS 0): boru deliğinin köşeleri
   kirişler boruya değecek kadar dışa (r / cos(Δθ/2)) → kiriş sarkması (0,14 / 0,34 / 0,16) kalkar; delik ölçüsü tasarımdaki gibi = boru dış Ø.
Dönüşüm: kaset yerel → dünya = yalnız öteleme (kaşar x 2088,5 · sucuk x 2360,5 · y +1152 · z −362,5), doğrulama: eski ağ kutusu = eski katı kutusu."""
import os, sys, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); S = os.path.dirname(os.path.dirname(HERE))
U = os.environ.get("YAMA_URETEC") or os.path.join(HERE, "u", "arastirma", "_uretec")   # v9 zinciri: derleme ağacının arastirma/_uretec'i (YAMA_URETEC)
for q in (os.path.join(S, "gece"), S, U, os.path.join(S, "_uretec_yama")): sys.path.insert(0, q)   # v9: kasar_cad_v15 / sucuk_cad_v9 / kaset_birlesim_v2 = kaynak/_uretec_yama (en önde)
from m8kit import Glb
import govde_denetim_dogru as G
os.chdir(U)
import cadquery as cq
import kasar_cad_v15 as KV, sucuk_cad_v9 as SV, sucuk_cad_v8 as SV8, kasar_cad_v14 as KV14

LOG = []
def log(*a):
    s = " ".join(str(x) for x in a); LOG.append(s); print(s, flush=True)

g = Glb(sys.argv[1])
OF = {"kasar": np.array([2088.5, 1152.0, -362.5]), "sucuk": np.array([2360.5, 1152.0, -362.5])}


def parcalar(V):
    V.PARCALAR[:] = []; V.kap(); return {p["ad"]: p["wp"].val() for p in V.PARCALAR}


def ag(sh, tol=0.02, aci=0.1):
    vs, ts = sh.copy().tessellate(tol, aci)
    P = np.array([(v.x, v.y, v.z) for v in vs], float); T = np.array(ts, int)
    return P[T]


def kutu(sh, of):
    b = sh.BoundingBox(); return np.array([b.xmin, b.ymin, b.zmin]) + of, np.array([b.xmax, b.ymax, b.zmax]) + of


def degistir(dugum, eski_sh, yeni_sh, of, ad):
    lo, hi = kutu(eski_sh, of)
    b = g.bilesen(dugum, lo=lo, hi=hi, tol=0.6)                     # eski ağ = eski katı (kutusu 0,6 içinde)
    gr = set()
    for p, tri in b["parca"]:
        for t in tri: gr.add(g._etiketler(p, t))
    assert len(gr) == 1, (ad, gr)
    Pw = ag(yeni_sh) + of
    ilk = [True]
    def f(_):
        if ilk[0]: ilk[0] = False; return Pw
        return None
    g.donustur(b, f)
    nl, nh = kutu(yeni_sh, of)
    log("%-24s %s[%d] eski kutu %s..%s → yeni %s..%s · %d üçgen (ince ağ) · etiket %s" % (
        ad, dugum, b["no"], np.round(lo, 1).tolist(), np.round(hi, 1).tolist(), np.round(nl, 1).tolist(), np.round(nh, 1).tolist(), len(Pw), sorted(gr)[0]))


K15, K14 = parcalar(KV), parcalar(KV14)
S9, S8 = parcalar(SV), parcalar(SV8)
# --- katı düzeyinde: değişen yalnız kaşar yatak kapağı; sucuk v9 = v8
for a in K15:
    if a == "yatak_kapagi": continue
    assert abs(K15[a].Volume() - K14[a].Volume()) < 1e-6, a
for a in S9:
    if a == "cikis_tupu": continue
    assert abs(S9[a].Volume() - S8[a].Volume()) < 1e-6, a
for a_, b_ in (("helezon_D", "cikis_tupu"), ("cikis_tupu", "yatak_kapagi")):
    log("KATI · sucuk %s ∩ %s: v8 %.2f mm³ → v9 %.3f mm³" % (a_, b_, S8[a_].intersect(S8[b_]).Volume(), S9[a_].intersect(S9[b_]).Volume()))
log("KATI · sucuk tüp hacmi v8 %.1f → v9 %.1f mm³ · tüp en ön z v8 %.2f → v9 %.2f (yerel)" % (S8["cikis_tupu"].Volume(), S9["cikis_tupu"].Volume(), S8["cikis_tupu"].BoundingBox().zmax, S9["cikis_tupu"].BoundingBox().zmax))
v_eski = K14["yatak_kapagi"].intersect(K14["cikis_tupu"]).Volume(); v_yeni = K15["yatak_kapagi"].intersect(K15["cikis_tupu"]).Volume()
d_yeni = K15["yatak_kapagi"].distance(K15["cikis_tupu"])
log("KATI · kaşar kapak ∩ tüp: v14 %.1f mm³ → v15 %.3f mm³ (kapak–tüp en yakın %.3f: tırnak cebe oturur) · kapak hacmi %.0f → %.0f mm³" % (
    v_eski, v_yeni, d_yeni, K14["yatak_kapagi"].Volume(), K15["yatak_kapagi"].Volume()))
# boru ön dış yüzü ↔ kapak arka yüzü
bz = (KV.AG_Z0 + KV.AG_Z1) / 2 + KV.BORU_D / 2 + KV.BORU_ET
log("KATI · kaşar boru ön dış yüzü z %.1f · kapak arka yüzü z %.1f → boşluk %.1f mm" % (bz, K15["yatak_kapagi"].BoundingBox().zmin, K15["yatak_kapagi"].BoundingBox().zmin - bz))

# --- GLB: iki kasette INCE parçalar yeni üreteçten (kaşar v15 · sucuk v9) ince ağla yerine konur
INCE = [("yatak_kapagi", "TOPPING_MODUL__pom"), ("govde", "TOPPING_MODUL__cam"), ("plaka_on", "TOPPING_MODUL__cam"), ("plaka_arka", "TOPPING_MODUL__cam"),
        ("cikis_tupu", "TOPPING_MODUL__cam"), ("conta_on", "TOPPING_MODUL__silikon"), ("conta_arka", "TOPPING_MODUL__silikon"),
        ("oring_tup", "TOPPING_MODUL__silikon"), ("oring_kapak", "TOPPING_MODUL__silikon")]


def eski_bul(dugum, sh, of, ad):
    """eski ağ bileşen(ler)i: kutusu eski katının kutusunun İÇİNDE (± 0,6) ve birleşik kutusu katı kutusuyla 1 mm içinde örtüşen (açık ağ birden çok bileşen olabilir)"""
    lo, hi = kutu(sh, of)
    g.bilesen(dugum, no=0)
    L = [b for b in g._bc[dugum] if np.all(b["lo"] >= lo - 0.6) and np.all(b["hi"] <= hi + 0.6) and (b["hi"] - b["lo"]).max() > 0.6 * (hi - lo).max()]
    assert L, (ad, lo, hi)
    ulo = np.min([b["lo"] for b in L], 0); uhi = np.max([b["hi"] for b in L], 0)
    tl = 3.0 if ad == "sucuk cikis_tupu" else 1.0                  # sucuk v8 katısında tüp ucunun önünde 2,5 mm gaga var, montaj ağında yoktu (açık ağ, kesik)
    assert np.all(np.abs(ulo - lo) < tl) and np.all(np.abs(uhi - hi) < tl), (ad, ulo, lo, uhi, hi)
    return L


def degistir2(dugum, eski_sh, yeni_sh, of, ad):
    L = eski_bul(dugum, eski_sh, of, ad)
    gr = set()
    for b in L:
        for p, tri in b["parca"]:
            for t in tri: gr.add(g._etiketler(p, t))
    assert len(gr) == 1, (ad, gr)
    Pw = ag(yeni_sh) + of; ilk = [True]; n0 = sum(len(t) for b in L for _, t in b["parca"])
    for b in L:
        def f(_):
            if ilk[0]: ilk[0] = False; return Pw
            return None
        g.donustur(b, f)
    lo, hi = kutu(eski_sh, of); nl, nh = kutu(yeni_sh, of)
    deg_ = "" if np.allclose(lo, nl, atol=0.01) and np.allclose(hi, nh, atol=0.01) else " → yeni %s..%s" % (np.round(nl, 1).tolist(), np.round(nh, 1).tolist())
    log("%-24s %s %s · %d eski bileşen (%s) %d üçgen → ince ağ %d üçgen · kutu %s..%s%s" % (
        ad, dugum, sorted(gr)[0], len(L), "kapalı" if all(b["kapali"] for b in L) else "AÇIK", n0, len(Pw),
        np.round(lo, 1).tolist(), np.round(hi, 1).tolist(), deg_))


for kad, YENI, ESKI in (("kaşar", K15, K14), ("sucuk", S9, S8)):
    for ad, dug in INCE:
        degistir2(dug, ESKI[ad], YENI[ad], OF["kasar" if kad == "kaşar" else "sucuk"], "%s %s" % (kad, ad))

# --- GLB: yarık dili + raf kaset contası boru deliği köşeleri dışa (kirişler boru dış yüzüne teğet)
def delik_dis(dugum, lo, hi, cx, cz, R, ad):
    """boru deliği: köşeleri (r ≈ delik yarıçapı) en küçük kareler çemberiyle bul → delik ekseni = BORU ekseni (cx, cz), yarıçap = boru dış r;
    köşeler kirişler bu çembere TEĞET olacak kadar dışa: r' = R / cos(Δθ/2). (eski ağda delik merkezi kesitten ölçülmüş, boru eksenine göre ~0,05 kaçık)"""
    b = g.bilesen(dugum, lo=np.array(lo), hi=np.array(hi), tol=0.6)
    say = [0, 0.0, 0.0, 0.0]
    def f(P):
        Q = P.reshape(-1, 3).copy(); r = np.hypot(Q[:, 0] - cx, Q[:, 2] - cz)
        m = (r > R - 0.15) & (r < R + 0.2)
        if not m.any(): return P
        X, Z = Q[m, 0], Q[m, 2]
        A_ = np.c_[2 * X, 2 * Z, np.ones(len(X))]; c_ = np.linalg.lstsq(A_, X * X + Z * Z, rcond=None)[0]
        xf, zf = c_[0], c_[1]; Rf = np.sqrt(c_[2] + xf * xf + zf * zf)
        # kiriş payı: delik yüzeyindeki HER üçgen kenarının açı açıklığından (iki ucu delikte olan kenarlar; çapraz kenarlar dahil)
        th = np.full(len(Q), np.nan); th[m] = np.arctan2(Z - zf, X - xf); T3 = th.reshape(-1, 3)
        da = []
        for i, j in ((0, 1), (1, 2), (2, 0)):
            d = np.abs((T3[:, i] - T3[:, j] + np.pi) % (2 * np.pi) - np.pi); da.append(d[np.isfinite(d)])
        da = np.concatenate(da); da = da[da < np.radians(60.0)]
        k = 1.0 / np.cos(da.max() / 2.0) if len(da) else 1.0
        u = np.c_[X - xf, Z - zf]; u /= np.linalg.norm(u, axis=1)[:, None]
        Q[m, 0] = cx + u[:, 0] * R * k; Q[m, 2] = cz + u[:, 1] * R * k
        say[0] += int(m.sum()); say[1] = R * (k - 1.0); say[2] = Rf; say[3] = np.hypot(xf - cx, zf - cz)
        return Q.reshape(-1, 3, 3)
    g.donustur(b, f)
    log("%-24s %s[%d] boru deliği: eski çember r %.3f, merkezi boru ekseninden %.3f kaçık → boru ekseninde r %.2f; %d köşe, kiriş payı %.3f (kirişler çembere teğet)" % (
        ad, dugum, b["no"], say[2], say[3], R, say[0], say[1]))


def conta_yeni(lo, hi, xc, zb, R, ad, kas_z=-150.0, Rd=30.0):
    """raf kaset contası (silikon yarım halka, raf deliğinin arka yarısı Ø60 ↔ tüp) — eski ağ 60 üçgenlik kaba çokgen (iç kenarı çemberde değil, 0,16 boruya giriyordu):
    topping_uno_cad'deki tanımla AYNI katı CadQuery ile kurulur, ince ağ: Ø60 (merkez raf deliği x, z −150) ∩ arka yarı − tüp dış çemberi (r R, boru ekseni)"""
    b = g.bilesen("TOPPING_MODUL__conta", lo=np.array(lo), hi=np.array(hi), tol=0.6)
    sh = SV.sily(xc, kas_z, Rd, 1149.0, 1152.0).intersect(SV.kut(xc - Rd - 1, xc + Rd + 1, 1148.0, 1153.0, kas_z - Rd - 1, kas_z)).cut(SV.sily(xc, zb, R, 1148.0, 1153.0)).val()
    Pw = ag(sh); ilk = [True]
    def f(_):
        if ilk[0]: ilk[0] = False; return Pw
        return None
    g.donustur(b, f)
    bb = sh.BoundingBox()
    log("%-24s TOPPING_MODUL__conta[%d] yeniden: yarım halka r %.0f (raf deliği) − tüp r %.2f · kutu x %.1f..%.1f z %.1f..%.1f · %d üçgen (eski 60)" % (ad, b["no"], Rd, R, bb.xmin, bb.xmax, bb.zmin, bb.zmax, len(Pw)))


RK = KV.BORU_D / 2 + KV.BORU_ET; RS = SV.BORU_D / 2 + SV.BORU_ET
ZK = (KV.AG_Z0 + KV.AG_Z1) / 2 - 362.5; ZS = (SV.AG_Z0 + SV.AG_Z1) / 2 - 362.5
delik_dis("TOPPING_MODUL__pom", (2057.5, 1143.0, -180.0), (2119.5, 1152.0, 24.0), 2088.5, ZK, RK, "kaşar yarık dili")
conta_yeni((2058.5, 1149.0, -179.2), (2118.5, 1152.0, -150.0), 2088.5, ZK, RK, "kaşar raf kaset contası")
delik_dis("TOPPING_MODUL__pom", (2329.5, 1143.0, -180.0), (2391.5, 1152.0, 24.0), 2360.5, ZS, RS, "sucuk yarık dili")
conta_yeni((2330.5, 1149.0, -179.2), (2390.5, 1152.0, -150.0), 2360.5, ZS, RS, "sucuk raf kaset contası")

g.kaydet(sys.argv[2])
json.dump(dict(kasar_kapak=[x.tolist() for x in kutu(K15["yatak_kapagi"], OF["kasar"])]), open(os.path.join(HERE, "a1_kutu.json"), "w"))
open(os.path.join(HERE, "a1_log.txt"), "w", encoding="utf-8").write("\n".join(LOG) + "\n")
sys.stdout.flush(); os._exit(0)
