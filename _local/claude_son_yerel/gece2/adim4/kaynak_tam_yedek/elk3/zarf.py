# -*- coding: utf-8 -*-
"""DIŞ ZARF TARAMASI: her üçgen istasyon dış zarflarından birinin içinde mi (tolerans 0,5 mm)"""
import sys, numpy as np, json, re
from collections import defaultdict
d = sys.argv[1]
D = np.load(d + r"\m8_onbellek.npz"); PJ = json.load(open(d + r"\m8_parca.json", encoding="utf-8"))
ad = np.array([p["ad"] for p in PJ["parca"]]); MEK = PJ["MEK"]
A, B, C, P = D["A"], D["B"], D["C"], D["P"]
lo = np.minimum(np.minimum(A, B), C); hi = np.maximum(np.maximum(A, B), C)
t = 0.5
Z = {"MAKINE (A…E, x 736–5230, z −830…79)": ((736, 0, -830), (5230, 2200, 79)),
     "QR": ((4570, 0, 670), (5430, 2050, 1190)),
     "TEZGAH": ((3834, 0, 1038), (4510, 1880, 1880))}
ic = np.zeros(len(A), bool)
for k, (a, b) in Z.items():
    ic |= np.all(lo >= np.array(a) - t, 1) & np.all(hi <= np.array(b) + t, 1)
nm = ad[P]
haric = np.array([bool(re.match(r"ZEMIN_DOSEME|INSAN|URUN|E_KUTU", s)) for s in ad])[P]
dis = ~ic & ~haric
gr = defaultdict(lambda: [0, np.full(3, 1e9), np.full(3, -1e9)])
for i in np.where(dis)[0]:
    g = gr[(nm[i], str(MEK[D["mek"][i]].get("kod") if isinstance(MEK[D["mek"][i]],dict) else MEK[D["mek"][i]]) if D["mek"][i] >= 0 else "-")]; g[0] += 1; g[1] = np.minimum(g[1], lo[i]); g[2] = np.maximum(g[2], hi[i])
print("zarf dışı üçgen:", int(dis.sum()), "/", len(A))
for (n, m), (c, a, b) in sorted(gr.items(), key=lambda kv: -kv[1][0]):
    print("  %-40s %-28s %6d  lo %s hi %s" % (n, m, c, np.round(a).astype(int).tolist(), np.round(b).astype(int).tolist()))
# arka düzlem: z < −830.5 olan her şey
arka = (lo[:, 2] < -830.5) & ~haric
print("arka düzlemin (z −830) arkasında üçgen:", int(arka.sum()))
gg = defaultdict(int)
for i in np.where(arka)[0]: gg[nm[i]] += 1
for k, v in gg.items(): print("   ", k, v)
