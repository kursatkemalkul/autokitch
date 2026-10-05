# -*- coding: utf-8 -*-
"""e3 · KABLO RENKLERİ: güç kabloları KIRMIZI (#c0392b), bilgi kabloları MAVİ (#1f5fbf).
İstasyon iç kablo düğümlerinde (ELK_TOPPING / ELK_K / ELK_DOLAP / ELK_ISTASYON / ELK_K_TARTI / ELK_QR_KABLO __kablo) her kablo
bileşeni kesitinden ayrılır: yarıçap r = 2·Hacim / Alan (kapalı tüp) · r < 3,3 mm (Ø < 6,6: sensör / enkoder / sinyal / 24 V fan) → MAVİ
yeni düğüm '<düğüm>_sinyal'; geri kalan (motor / besleme / kompresör) → KIRMIZI. *__kablo_veri → MAVİ.
python e3_renk.py e2.glb e3.glb"""
import sys, collections, numpy as np
from elib import *
import m8kit
gi, go = sys.argv[1:3]
G = m8kit.Glb(gi); Y = Yeni(); R = []
KIRMIZI = [0.753, 0.224, 0.169, 1.0]; MAVI = [0.122, 0.373, 0.749, 1.0]
ESIK = 3.3
DUG = ["ELK_TOPPING__kablo", "ELK_K__kablo", "ELK_DOLAP__kablo", "ELK_ISTASYON__kablo", "ELK_K_TARTI__kablo", "ELK_QR_KABLO__kablo"]
ist = collections.Counter()
for ad in DUG:
    for p in G.dprims(ad):
        if p.get("gizli"): continue
        tl, kut = G.komp(p); vis = G.gorunur(p)
        P = p["X"][p["T"]]
        cr = np.cross(P[:, 1] - P[:, 0], P[:, 2] - P[:, 0])
        A = 0.5 * np.linalg.norm(cr, axis=1); V6 = np.einsum("ij,ij->i", P[:, 0], np.cross(P[:, 1], P[:, 2]))
        sinyal = np.zeros(len(P), bool); rs = []
        for i in kut:
            m = (tl == i) & vis
            a = A[m].sum(); v = abs(V6[m].sum()) / 6.0
            r = 2 * v / a if a > 0 else 0
            rs.append(r)
            if r < ESIK: sinyal |= m
        n_s = int(sinyal.sum())
        if n_s:
            gr = collections.defaultdict(list)
            for t in np.where(sinyal)[0]: gr[G._etiketler(p, int(t))].append(t)
            for (kat, mek, kpk), tt in gr.items():
                Y.ekle(ad + "_sinyal", ("ME2_kablo_sinyal", tuple(MAVI), 0.0, 0.55), P[np.array(tt)], kat, mek)
            G.sil(p, sinyal)
        R.append((ad, len(kut), sum(1 for r in rs if r < ESIK), np.round(np.percentile(rs, [0, 50, 100]), 2).tolist() if rs else []))
Y.yaz(G)
# malzeme renkleri
n = 0
for m in G.J["materials"]:
    nm = m.get("name", "")
    if nm.endswith("__kablo") and not nm.startswith("MR_ELK_ANA_HAT") and "ROBOT" not in nm:
        m["pbrMetallicRoughness"]["baseColorFactor"] = KIRMIZI; n += 1
    elif nm.endswith("__kablo_veri"):
        m["pbrMetallicRoughness"]["baseColorFactor"] = MAVI; n += 1
for r in R: print("  %-26s bilesen %4d · sinyal(mavi) %4d · r min/orta/maks %s" % r)
print("  malzeme rengi degisen", n)
G.kaydet(go); print("yazildi", go)
