# -*- coding: utf-8 -*-
import sys, numpy as np, json, re
d = sys.argv[1]
D = np.load(d + r"\m8_onbellek.npz"); PJ = json.load(open(d + r"\m8_parca.json", encoding="utf-8"))
ad = np.array([p["ad"] for p in PJ["parca"]])
A, B, C, P = D["A"], D["B"], D["C"], D["P"]
lo = np.minimum(np.minimum(A, B), C); hi = np.maximum(np.maximum(A, B), C)
t = 0.5
Z = [((736, 0, -830), (5230, 2200, 79)), ((4570, 0, 670), (5430, 2050, 1190)), ((3834, 0, 1038), (4510, 1880, 1880))]
ic = np.zeros(len(A), bool)
for a, b in Z: ic |= np.all(lo >= np.array(a) - t, 1) & np.all(hi <= np.array(b) + t, 1)
nm = ad[P]
haric = np.array([bool(re.match(r"ZEMIN_DOSEME|INSAN|URUN|E_KUTU", s)) for s in ad])[P]
dis = ~ic & ~haric
u, inv = np.unique(nm[dis], return_inverse=True)
print("ZARF DIŞI üçgen:", int(dis.sum()), "/", len(A))
for k, n in enumerate(u):
    m = np.where(dis)[0][inv == k]
    print("  %-34s %6d  lo %s hi %s" % (n, len(m), np.round(lo[m].min(0)).astype(int).tolist(), np.round(hi[m].max(0)).astype(int).tolist()))
arka = (lo[:, 2] < -830.5) & ~haric
u, c = np.unique(nm[arka], return_counts=True)
print("ARKA DÜZLEMİN (z −830) ARKASINDA:", int(arka.sum()), dict(zip(u.tolist(), c.tolist())))
# zemin üstü (y>0) ve zarf dışı
ust = dis & (hi[:, 1] > 0.5)
u, c = np.unique(nm[ust], return_counts=True)
print("ZEMİN ÜSTÜNDE ve ZARF DIŞI:", int(ust.sum()), dict(zip(u.tolist(), c.tolist())))
