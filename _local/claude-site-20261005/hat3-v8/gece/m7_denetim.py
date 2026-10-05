# -*- coding: utf-8 -*-
"""M7 · ek denetimler (çakışma dışı): python m7_denetim.py model.glb cikti_klasoru
 1 EVAPORATÖR ↔ üst UNO arka takımı (silindir, konsol, ön ayak, mafsal) x boşlukları
 2 AÇIK PU: 6 bakış (önden kapaklar yok · oda içinden sola / arkaya / aşağı / yukarı · A'nın içinden sağa) raster 1 mm
 3 KASET ÇEKME SÜPÜRMESİ: kaşar / sucuk kaseti önden (+z) 300 mm çekilince yolundaki üçgenler (kendi parçaları, raf/eşik/çerçeve dil kanalı,
   kılavuz ve bastırılmış kilit dili hariç)
 4 UNO HUNİ ÇIKARMA: her hazne için üst boşluk (tavana / üst rafa), yan boşluklar, öne çekme yolu (gerekirse yana kaydırma)
 5 HORTUM: dik mi (x/z sapması), alt birimlerden x boşluğu, raf/üst raf/kovan delik eksenleri
 6 HAVADA PARÇA: kapaklar yok sayılarak bölgede hiçbir şeye değmeyen küçük parça"""
import os, sys, json, numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from m7kit import Glb
from m7_etiket import etiketle, etiketle_yeni
from m7_olcu import DX, X_L, X_R, Z_H, LIN_X0

gi, od = sys.argv[1], sys.argv[2]
os.makedirs(od, exist_ok=True)
G = Glb(gi)
OUT = []


def yaz(*a):
    s = " ".join(str(x) for x in a); print(s); OUT.append(s)


# ---------------------------------------------------------------- ortak: etiketli bileşenler
R = etiketle(G, ("TOPPING_MODUL",)) if "--taban" in sys.argv else etiketle_yeni(G, ("TOPPING_MODUL",), [os.path.join(os.path.dirname(gi), f) for f in ("v8x_b_rapor.txt", "v8x_c_rapor.txt")])
B = []          # (ad, dugum, pid, komp, lo, hi)
for i, (tl, kut, ad) in R.items():
    for c, nm in ad.items():
        lo, hi, n = kut[c]; B.append((nm, G.prims[i]["name"], i, c, lo, hi))


def bul(nm_bas):
    return [b for b in B if b[0].startswith(nm_bas)]


def tri_tum(haric=lambda p: False, kpk_yok=True):
    L = []
    for pid, p in enumerate(G.prims):
        if haric(p) or len(p["T"]) == 0: continue
        ok = G.gorunur(p)
        if kpk_yok: ok &= ~G.kpk_maske(p)
        if not ok.any(): continue
        tl, _ = G.komp(p)
        idx = np.where(ok)[0]
        L.append((pid, idx, tl[idx], p["X"][p["T"][idx]]))
    return L


TRI = tri_tum()

# ================================================================ 1 · evaporatör boşluğu
yaz("== 1 · EVAPORATÖR ↔ ÜST UNO ARKA TAKIMI (evap kaseti dış sacı x 1676–2216 · y 1383–1765 · z −826…−640)")
EV = (1676.0, 2216.0, 1383.0, 1765.0, -826.0, -640.0)
for u in ("harc", "sos"):
    for parca in ("__pnomatik_silindir_D32", "_silindir_konsolu", "__pnomatik_on_ayak", "__pnomatik_arka_mafsal", "__pnomatik_on_bogaz"):
        for nm, dug, pid, c, lo, hi in bul(u + parca):
            yo = lo[1] < EV[3] and hi[1] > EV[2] and lo[2] < EV[5] and hi[2] > EV[4]
            dx = max(EV[0] - hi[0], lo[0] - EV[1])
            yaz("   %-34s x %7.1f–%7.1f  y/z örtüşme %s  →  x boşluğu %+.1f mm %s" % (nm, lo[0], hi[0], "VAR" if yo else "yok", dx, "TAMAM" if (dx >= 5 or not yo) else "YETERSİZ"))

# ================================================================ 2 · açık PU (raster)
yaz("\n== 2 · AÇIK PU (1 mm raster · kapaklar yok · PU = düğüm adı __pu)")


def raster(eks, isaret, bas, u_ar, v_ar, kutu, h=1.0):
    """eks: bakış ekseni (0 x,1 y,2 z) · isaret: +1 → artan eksen yönüne bakılır (bas düzleminden ileri) · u,v diğer eksenler"""
    ua, va = [a for a in (0, 1, 2) if a != eks]
    us = np.arange(u_ar[0] + h / 2, u_ar[1], h); vs = np.arange(v_ar[0] + h / 2, v_ar[1], h)
    zb = np.full((len(vs), len(us)), 1e18); kim = np.full((len(vs), len(us)), -1)
    adl = []
    for pid, idx, tl, C in TRI:
        nm = G.prims[pid]["name"]
        if nm.startswith(("INSAN", "ZEMIN", "ROBOT")): continue
        d = (C[:, :, eks] - bas) * isaret
        m = (d.max(1) > 0) & (C[:, :, ua].max(1) > u_ar[0]) & (C[:, :, ua].min(1) < u_ar[1]) & (C[:, :, va].max(1) > v_ar[0]) & (C[:, :, va].min(1) < v_ar[1])
        for kk, (lo, hi) in enumerate(zip(kutu[0::2], kutu[1::2])):
            m &= (C[:, :, kk].max(1) >= lo) & (C[:, :, kk].min(1) <= hi)
        if not m.any(): continue
        k = len(adl); adl.append(nm)
        for tri in C[m]:
            P2 = tri[:, [ua, va]]; D = (tri[:, eks] - bas) * isaret
            (x0, y0), (x1, y1), (x2, y2) = P2
            dd = (y1 - y2) * (x0 - x2) + (x2 - x1) * (y0 - y2)
            if abs(dd) < 1e-9: continue
            ix = np.where((us >= P2[:, 0].min()) & (us <= P2[:, 0].max()))[0]; iy = np.where((vs >= P2[:, 1].min()) & (vs <= P2[:, 1].max()))[0]
            if not len(ix) or not len(iy): continue
            XX, YY = np.meshgrid(us[ix], vs[iy])
            a = ((y1 - y2) * (XX - x2) + (x2 - x1) * (YY - y2)) / dd; b = ((y2 - y0) * (XX - x2) + (x0 - x2) * (YY - y2)) / dd; c = 1 - a - b
            ins = (a >= -1e-6) & (b >= -1e-6) & (c >= -1e-6)
            Z = a * D[0] + b * D[1] + c * D[2]
            ins &= Z > 0
            sub = zb[np.ix_(iy, ix)]; ks = kim[np.ix_(iy, ix)]
            yeni = ins & (Z < sub - 1e-4)
            sub[yeni] = Z[yeni]; ks[yeni] = k
            zb[np.ix_(iy, ix)] = sub; kim[np.ix_(iy, ix)] = ks
    pu = np.array(["__pu" in a for a in adl] + [False])
    ac = pu[kim]
    from scipy import ndimage
    lab, n = ndimage.label(ac)
    bolge = []
    for j in range(1, n + 1):
        w = np.where(lab == j); bolge.append((len(w[0]), us[w[1]].min(), us[w[1]].max(), vs[w[0]].min(), vs[w[0]].max()))
    bolge.sort(key=lambda r: -r[0])
    return int(ac.sum()), bolge, "xyz"[ua], "xyz"[va]


GOR = [("önden (kapaklar yok)", 2, -1, 200.0, (1240, 2510), (1040, 2205), (-1e9, 1e9, -1e9, 1e9, -1e9, 1e9)),
       ("oda içinden sola (x 2000 → −x)", 0, -1, 2000.0, (1152.5, 2139.5), (-569.5, 36.5), (-1e9, 1e9, 1100, 2200, -640, 40)),
       ("oda içinden sağa (x 1600 → +x)", 0, +1, 1600.0, (1152.5, 2139.5), (-569.5, 36.5), (-1e9, 1e9, 1100, 2200, -640, 40)),
       ("oda içinden arkaya (z 0 → −z)", 2, -1, 0.0, (1297.5, 2439.5), (1152.5, 2139.5), (1240, 2510, 1100, 2200, -1e9, 1e9)),
       ("oda içinden aşağı (y 2100 → −y)", 1, -1, 2100.0, (1297.5, 2439.5), (-569.5, 36.5), (1240, 2510, -1e9, 1e9, -640, 40)),
       ("oda içinden yukarı · ana oda (y 1160 → +y)", 1, +1, 1160.0, (1496.5, 2439.5), (-569.5, 36.5), (1240, 2510, -1e9, 1e9, -640, 40)),
       ("oda içinden yukarı · cep (y 1160 → +y)", 1, +1, 1160.0, (1297.5, 1495.5), (-569.5, -15.5), (1240, 2510, -1e9, 1e9, -640, 40)),
       ("mekanizma bandından yukarı (y 1050 → +y)", 1, +1, 1050.0, (1240, 2510), (-640, 40), (1240, 2510, -1e9, 1e9, -640, 40)),
       ("A'nın içinden sağa (x 1180 → +x)", 0, +1, 1180.0, (1100, 2200), (-640, 30), (-1e9, 1e9, 1100, 2200, -640, 30))]
PU_TOPLAM = 0
for ad, eks, isr, bas, ua, va, kutu in GOR:
    n, bol, un, vn = raster(eks, isr, bas, ua, va, kutu)
    PU_TOPLAM += n
    yaz("   %-42s açık PU %6d mm² · %d bölge %s" % (ad, n, len(bol), "" if not bol else "· en büyükler: " + "; ".join(
        "%d mm² %s %.0f–%.0f %s %.0f–%.0f" % (r[0], un, r[1], r[2], vn, r[3], r[4]) for r in bol[:6])))

# ================================================================ 3 · kaset çekme süpürmesi
yaz("\n== 3 · KASET ÖNDEN ÇEKME SÜPÜRMESİ (+z 300 mm · kilit dili bastırılmış)")
for k, pre in (("kasar", "kasar_cad_v14"), ("sucuk", "sucuk_cad_v8")):
    kas = [b for b in B if b[0].startswith(pre)]
    own = {(b[2], b[3]) for b in kas}
    izin = ("tasiyici_raf", "soguk_esik", "onyuz_on_cerceve", "raf_on_bukumu", "yuva_%s_kilavuz" % k, "yuva_%s_kilit" % k,
            "raf_kaset_contasi_%s" % k, "soguk_raf_dil_kanali_tabani_%s" % k)
    hit = {}
    for nm, dug, pid, c, lo, hi in kas:
        e = 0.3
        sl, sh = lo.copy() + e, hi.copy() - e; sh[2] = hi[2] + 300.0
        for pid2, idx, tl, C in TRI:
            mn = C.min(1); mx = C.max(1)
            m = (mx[:, 0] > sl[0]) & (mn[:, 0] < sh[0]) & (mx[:, 1] > sl[1]) & (mn[:, 1] < sh[1]) & (mx[:, 2] > sl[2]) & (mn[:, 2] < sh[2])
            if not m.any(): continue
            for j in np.where(m)[0]:
                key = (pid2, int(tl[j]))
                if key in own: continue
                nm2 = G.prims[pid2]["name"]
                if nm2.startswith("TOPPING_DONER__") and nm2.endswith(k.upper()): continue
                hit.setdefault(key, []).append(nm)
    sorun = []
    for (pid2, c2), kimler in hit.items():
        p2 = G.prims[pid2]; ad2 = R[pid2][2].get(c2, "?") if pid2 in R else p2["name"]
        if ad2.startswith(izin) or "kpk" in ad2: continue
        if G.kpk_maske(p2)[(R[pid2][0] == c2) if pid2 in R else slice(None)].any() if pid2 in R else False: continue
        tl2, kut2 = G.komp(p2); lo2, hi2, _ = kut2[c2]
        sorun.append((ad2 if ad2 != "?" else p2["name"] + "#%d" % c2, sorted(set(kimler))[:3], lo2, hi2))
    if not sorun: yaz("   %s: yol TEMİZ (izinli: raf dil kanalı / eşik / çerçeve yarığı / kılavuz / bastırılmış dil)" % k)
    for a, kim_, lo2, hi2 in sorun:
        yaz("   %s: YOLDA %-44s x %.0f–%.0f y %.0f–%.0f z %.0f–%.0f ← %s" % (k, a, lo2[0], hi2[0], lo2[1], hi2[1], lo2[2], hi2[2], ", ".join(kim_)))

# ================================================================ 4 · UNO huni çıkarma
yaz("\n== 4 · UNO HUNİSİ ÇIKARMA PAYI (TC kelepçe açılır → huni kalkar → öne çekilir · ön ağız x 1496–2440)")
TAVAN, UST_RAF_ALT, ACIK0 = 2140.0, 1534.0, 1496.0
for u, ust in (("kiyma", UST_RAF_ALT), ("kusbasi", UST_RAF_ALT), ("harc", TAVAN), ("sos", TAVAN)):
    h = bul(u + "_hazne_bizim")[0]; lo, hi = h[4], h[5]
    sol = [b for b in B if b[5][0] <= lo[0] + 0.5 and b[5][0] > lo[0] - 400 and b[4][1] < hi[1] and b[5][1] > lo[1] and b[4][2] < hi[2] and b[5][2] > lo[2] and not b[0].startswith(u)]
    sag = [b for b in B if b[4][0] >= hi[0] - 0.5 and b[4][0] < hi[0] + 400 and b[4][1] < hi[1] and b[5][1] > lo[1] and b[4][2] < hi[2] and b[5][2] > lo[2] and not b[0].startswith(u)]
    ds = min([lo[0] - b[5][0] for b in sol] + [lo[0] - (LIN_X0 + 1)]); dr = min([b[4][0] - hi[0] for b in sag] + [2440 - hi[0]])
    on_engel = max(0.0, ACIK0 - lo[0])
    yaz("   %-8s hazne x %.0f–%.0f y %.0f–%.0f · üst boşluk %.0f mm · sol %.0f · sağ %.0f · %s" % (
        u, lo[0], hi[0], lo[1], hi[1], ust - hi[1], ds, dr,
        "doğrudan öne çekilir" if on_engel <= 0 else "önce %.0f mm sağa kaydırılır (sağ boşluk %.0f %s) sonra öne" % (on_engel, dr, "YETER" if dr >= on_engel else "YETMEZ")))

# ================================================================ 5 · hortumlar
yaz("\n== 5 · ÜST UNO HORTUMLARI (D32, dış Ø42)")
for x, ad in ((X_L, "harç (sol)"), (X_R, "sos (sağ)")):
    hs = [b for b in B if "urun_hortumu_D32" in b[0] and abs((b[4][0] + b[5][0]) / 2 - x) < 25]
    for nm, dug, pid, c, lo, hi in hs:
        yaz("   %-10s hortum x %.1f–%.1f (eksen %.1f) y %.0f–%.0f z %.1f–%.1f · dik: x/z sapma %.1f/%.1f mm" % (
            ad, lo[0], hi[0], (lo[0] + hi[0]) / 2, lo[1], hi[1], lo[2], hi[2], hi[0] - lo[0] - 41.6, hi[2] - lo[2] - 41.6))
    # alt birimlere yatay boşluk (y 1152–1504 bandında)
    alt = [b for b in B if b[4][1] < 1500 and b[5][1] > 1216 and b[4][2] < -149 and b[5][2] > -191 and b[0].startswith(("kiyma", "kusbasi", "kasar_cad", "sucuk_cad", "yuva_"))]
    dl = min([x - 21 - b[5][0] for b in alt if b[5][0] <= x] + [999]); dr = min([b[4][0] - x - 21 for b in alt if b[4][0] >= x] + [999])
    yaz("   %-10s hortumun önünde/arkasında alt birim yok · yatay boşluk sol %.1f · sağ %.1f mm" % (ad, dl, dr))
json.dump(OUT, open(os.path.join(od, "m7_denetim.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
open(os.path.join(od, "m7_denetim.txt"), "w", encoding="utf-8").write("\n".join(OUT))
sys.stdout.flush(); os._exit(0)
