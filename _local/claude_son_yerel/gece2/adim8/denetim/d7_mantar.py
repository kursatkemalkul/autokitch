# -*- coding: utf-8 -*-
"""Kalem 7 · acil stop mantarları kapakla birlikte dönerken çarpıyor mu: python d7_mantar.py   (DENETIM_GLB; meta = cak/meta.json)
mantar = ACIL_STOP__* bileşenleri (konuma göre 6 küme) · taşıyan kapak = mantarın arkasındaki kpk bileşeni · menteşe = parca_kutulari'nda kapak kutusu
(±40 mm) içindeki 'mentese' parçaları (dikey yığılmışsa dikey eksen, yatay dizilmişse yatay eksen); bulunamazsa kapağın 4 kenarı ayrı ayrı denenir.
Mantar (manifold birleşimi) 0 → 100° 2° adımla döndürülür (kapak dışa açılır); sabit = mantar kutusu süpürmesine giren, aynı kapağa ait OLMAYAN kapalı bileşenler; eşik 0,5 mm³.
Çekmece üstündeki mantar (B depo) +z 0 → 700 mm öteleme ile denenir."""
import os, sys, json, re, numpy as np
from collections import defaultdict
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "cak"))
import c8a_ortak as M
import manifold3d as mf
PKJ = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH_COORDINATION\worktrees\claude-hat3-v8\otonom\hat3d\v3\parca_kutulari.json"
PK = json.load(open(PKJ, encoding="utf-8"))["parca"]
MEN = [(b, q[0], np.array(q[2:8], float)) for b, L in PK.items() for q in L if "mentese" in q[0].lower() and "vida" not in q[0] and "pem" not in q[0]]
J, B, LAB = M.tum_bilesenler(True)
KPK = np.array([l[2] > 0.5 for l in LAB])
AS = [i for i, b in enumerate(B) if b.dugum.startswith("ACIL_STOP__")]
# kümele (merkez 60 mm)
kume = []
for i in AS:
    c = (B[i].lo + B[i].hi) / 2
    for k in kume:
        if np.abs(k["c"] - c).max() < 60: k["i"].append(i); break
    else: kume.append(dict(c=c, i=[i]))
LO = np.array([b.lo for b in B]); HI = np.array([b.hi for b in B])


def birlesim(ii):
    ms = [B[i].mf() for i in ii if B[i].mf()]
    return mf.Manifold.batch_boolean(ms, mf.OpType.Add) if ms else None


def rotT(eks, nokta, th):
    """eks birim vektör etrafında nokta'dan geçen eksende th rad dönüş → 3x4"""
    k = np.array(eks, float); K = np.array([[0, -k[2], k[1]], [k[2], 0, -k[0]], [-k[1], k[0], 0]])
    R = np.eye(3) + np.sin(th) * K + (1 - np.cos(th)) * K @ K
    t = np.array(nokta) - R @ np.array(nokta)
    return np.c_[R, t]


def tara(mm, ii, kapak, hareket, ad):
    lo = np.min([B[i].lo for i in ii], 0); hi = np.max([B[i].hi for i in ii], 0)
    # süpürme kutusu: tüm adımlardaki dönüşmüş kutu köşeleri
    kose = np.array([[x, y, z] for x in (lo[0], hi[0]) for y in (lo[1], hi[1]) for z in (lo[2], hi[2])])
    tum = []
    for T in hareket: tum.append(kose @ T[:, :3].T + T[:, 3])
    tum = np.concatenate(tum); slo = tum.min(0) - 1; shi = tum.max(0) + 1
    m = ((LO <= shi) & (HI >= slo)).all(1)
    ayni = set(ii) | set(kapak)
    F = [j for j in np.where(m)[0] if j not in ayni]
    Fk = [j for j in F if B[j].mf()]
    bulgu = {}
    for s, T in enumerate(hareket):
        Mt = mm.transform(T.tolist())
        bb = Mt.bounding_box(); bl = np.array(bb[:3]) - .1; bh = np.array(bb[3:]) + .1
        for j in Fk:
            if np.any(HI[j] < bl) or np.any(LO[j] > bh): continue
            v = (Mt ^ B[j].mf()).volume()
            if v > 0.5:
                r = bulgu.setdefault(j, [s, s, 0.0]); r[1] = s; r[2] = max(r[2], v)
    return bulgu, len(F), len(Fk), (slo, shi)


meta = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "cak", "meta.json"), encoding="utf-8"))["bil"]
def ad(j): return "%s[%d] %s" % (B[j].dugum, B[j].no, meta[j]["ad"] if meta[j]["dugum"] == B[j].dugum else "")
SONUC = []
for k in kume:
    ii = k["i"]; lo = np.min([B[i].lo for i in ii], 0); hi = np.max([B[i].hi for i in ii], 0); c = (lo + hi) / 2
    yon = 1 if (hi[2] - lo[2]) < 60 and lo[2] > 0 and c[2] < 200 else (-1 if c[2] > 200 else 1)
    # taşıyan kapak: mantar xy'sini örten kpk bileşeni, yüzü mantarın tabanında
    aday = [j for j in range(len(B)) if KPK[j] and not B[j].dugum.startswith("ACIL_STOP") and LO[j][0] <= c[0] <= HI[j][0] and LO[j][1] <= c[1] <= HI[j][1] and LO[j][2] <= hi[2] + 3 and HI[j][2] >= lo[2] - 3]
    sabit = [j for j in range(len(B)) if not KPK[j] and not B[j].dugum.startswith("ACIL_STOP") and LO[j][0] <= c[0] <= HI[j][0] and LO[j][1] <= c[1] <= HI[j][1] and LO[j][2] <= hi[2] + 3 and HI[j][2] >= lo[2] - 3]
    print("\n== MANTAR merkez %s · yön %s z · bileşen %d · kapak aday %d" % (np.round(c).tolist(), "+" if yon > 0 else "−", len(ii), len(aday)))
    print("   mantar kutusu %s..%s · arkasındaki kpk OLMAYAN bileşenler: %s · kpk: %s" % (np.round(lo, 1).tolist(), np.round(hi, 1).tolist(), [ad(j) for j in sabit][:6], [ad(j) for j in aday][:6]))
    mm = birlesim(ii)
    if not aday:
        print("   kapak bulunamadı (mantar sabit gövde üstünde) → dönme süpürmesi yok"); SONUC.append(dict(c=c.tolist(), kapak=None)); continue
    j0 = max(aday, key=lambda j: np.prod(HI[j][:2] - LO[j][:2])); klo, khi = LO[j0], HI[j0]
    print("   kapak %s kutu %s..%s" % (ad(j0), np.round(klo).tolist(), np.round(khi).tolist()))
    kapak = [j for j in range(len(B)) if KPK[j] and (LO[j] >= klo - 40).all() and (HI[j] <= khi + 40).all()]
    cek = "CEK" in B[j0].dugum or "CEKMECE" in B[j0].dugum or "DEPO" in B[j0].dugum
    eksenler = []
    if cek:
        hareket = [np.c_[np.eye(3), [0, 0, yon * dz]] for dz in np.arange(0, 700.1, 10)]
        eksenler.append(("çekmece +z 0→700", hareket))
    else:
        mn = [x for x in MEN if (x[2][0::2] >= klo - 40).all() and (x[2][1::2] <= khi + 40).all()]
        bir = B[j0].dugum.split("__")[0]
        if any(x[0] == bir for x in mn): mn = [x for x in mn if x[0] == bir]
        # kapağın kendi adına bağlı menteşeler (ör. f_ust ... sol) varsa onları al
        mn2 = [x for x in mn if "hareketli" in x[1] or "kanat" in x[1]]
        if mn2: mn = mn2
        print("   menteşe parçaları:", sorted(set("%s %s" % (x[1], np.round((x[2][0::2] + x[2][1::2]) / 2).tolist()) for x in mn))[:8])
        zf = khi[2] if yon > 0 else klo[2]
        if mn:
            P = np.array([(x[2][0::2] + x[2][1::2]) / 2 for x in mn]); sp = P.max(0) - P.min(0)
            if sp[1] >= sp[0]:  # dikey eksen
                xh = P[:, 0].mean(); s = 1 if (klo[0] + khi[0]) / 2 > xh else -1
                eksenler.append(("dikey menteşe x %.0f (%s)" % (xh, ", ".join(sorted(set(x[1] for x in mn))[:2])), [rotT([0, -s * yon, 0], [xh, 0, zf], np.radians(a)) for a in range(0, 101, 2)]))
            else:
                yh = P[:, 1].mean(); s = 1 if (klo[1] + khi[1]) / 2 > yh else -1
                eksenler.append(("yatay menteşe y %.0f (%s)" % (yh, ", ".join(sorted(set(x[1] for x in mn))[:2])), [rotT([s * yon, 0, 0], [0, yh, zf], np.radians(a)) for a in range(0, 101, 2)]))
        else:
            for nm, eks, nok in (("sol kenar dikey (varsayım)", [0, -yon, 0], [klo[0], 0, zf]), ("sağ kenar dikey (varsayım)", [0, yon, 0], [khi[0], 0, zf]),
                                 ("alt kenar yatay (varsayım)", [yon, 0, 0], [0, klo[1], zf]), ("üst kenar yatay (varsayım)", [-yon, 0, 0], [0, khi[1], zf])):
                eksenler.append((nm, [rotT(eks, nok, np.radians(a)) for a in range(0, 101, 2)]))
    km = birlesim([j for j in aday])
    for nm, hareket in eksenler:
        if km is not None and not cek:
            bk, _, _, _ = tara(km, aday, kapak + ii, hareket, nm)
            bk = {j: r for j, r in bk.items() if not re.search(r"mentese|basac|fitil|conta|tip_on", (meta[j]["ad"] or "") + B[j].dugum)}
            print("   KAPAK PANELİ süpürmesi (%s): %s" % (nm, "TEMİZ" if not bk else "; ".join("%s %d→%d° %.0f mm³" % (ad(j), a * 2, b_ * 2, v) for j, (a, b_, v) in sorted(bk.items(), key=lambda x: x[1][0])[:6])))
        if km is not None and cek:
            bk, _, _, _ = tara(km, aday, kapak + ii, hareket, nm)
            print("   ÇEKMECE ÖNÜ süpürmesi: %s" % ("TEMİZ" if not bk else "; ".join("%s %d→%d mm %.0f mm³" % (ad(j), a * 10, b_ * 10, v) for j, (a, b_, v) in sorted(bk.items(), key=lambda x: x[1][0])[:6])))
        bul, nf, nfk, _ = tara(mm, ii, kapak, hareket, nm)
        adim = "mm" if cek else "°"; olc = 10 if cek else 2
        print("   %s · sabit komşu %d (kapalı %d) → %s" % (nm, nf, nfk, "TEMİZ" if not bul else "ÇARPMA %d" % len(bul)))
        for j, (a, b_, v) in sorted(bul.items(), key=lambda x: x[1][0]):
            print("      ÇARPAR %-60s %d→%d %s · en büyük ortak hacim %.1f mm³" % (ad(j), a * olc, b_ * olc, adim, v))
        SONUC.append(dict(c=c.tolist(), kapak=ad(j0), eksen=nm, carpma=[(ad(j), a * olc, b_ * olc, v) for j, (a, b_, v) in bul.items()]))
json.dump(SONUC, open("mantar.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=float)
sys.stdout.flush(); os._exit(0)
