"""havada denetimi tamamlayıcısı (B v4)
tezgâhta birleşmiş grup (aynı hareket) birlikte iner: grubun bir üyesi yerindeki parçaya değiyorsa, ona değen grup üyeleri de havada değildir.
elde tutulup aynı adımda perçinlenen / vidalanan parça: son konumda değdiği bağlantı elemanı 15 s içinde takılıyorsa havada değildir."""
import json, numpy as np, trimesh


def _deg(Pm, x, y, tol=6e-4):
    lx, hx = Pm[x]['V'].min(0), Pm[x]['V'].max(0); ly, hy = Pm[y]['V'].min(0), Pm[y]['V'].max(0)
    if np.any(lx > hy + tol) or np.any(ly > hx + tol): return False
    for u, v in ((x, y), (y, x)):
        V = Pm[u]['V']; m = np.all(V >= Pm[v]['V'].min(0) - tol, 1) & np.all(V <= Pm[v]['V'].max(0) + tol, 1)
        if m.any() and trimesh.proximity.closest_point(trimesh.Trimesh(Pm[v]['V'], Pm[v]['F'], process=False), V[m][:3000])[1].min() <= tol: return True
    return False


def havada_grup(H, P, Pm, HAR, GOR):
    imz = {a: json.dumps(HAR[a]) for a in HAR}; son = {a: max([h[1] for h in HAR[a]] + [GOR.get(a, 0)]) for a in HAR}
    BG = [b for b in HAR if (b.startswith('b_') and P[b].get('etur') in ('percin', 'saplama', 'civata')) or b.endswith('_burc')]
    H = list(H); deg = True
    while deg:
        deg = False
        for s in list(H):
            es = [b for b in HAR if b != s and imz[b] == imz[s] and b not in H and P[b]['tur'] != 'kablo']
            bg = [b for b in BG if son[s] <= son[b] <= son[s] + 15.0]
            if any(_deg(Pm, s, b) for b in es + bg): H.remove(s); deg = True
    return H
