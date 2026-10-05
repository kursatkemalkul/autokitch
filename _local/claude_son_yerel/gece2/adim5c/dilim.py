# -*- coding: utf-8 -*-
"""v8zq bileşenini (düğüm, no) ince ekseninin orta düzleminde kes → 2B dış kontur + delikler (dünya eksenleriyle)
kullanım: python dilim.py "DUGUM:no[:eksen[:konum]]" ...   (eksen x/y/z · konum verilmezse ince eksenin ortası)"""
import sys, os, pickle, json, numpy as np
import trimesh
B = pickle.load(open(r"C:\Users\Kemal\AppData\Local\Temp\claude\C--Users-Kemal-Desktop-Kemal-WEBS-TE\f3ef876a-f062-4b29-bb81-775cc8a1a6d8\scratchpad\gece2\adim5\_is\bil_hepsi.pkl", "rb"))
IDX = {(b["ad"], b["no"]): b for b in B}


def zincir(S2):
    """2B parça listesi → kapalı döngüler (uç noktaları 0,01 yuvarlanır)"""
    import collections
    key = lambda p: (round(p[0] * 50), round(p[1] * 50))
    adj = collections.defaultdict(list)
    for i, (a, b) in enumerate(S2):
        ka, kb = key(a), key(b)
        if ka == kb: continue
        adj[ka].append((kb, i)); adj[kb].append((ka, i))
    used = set(); loops = []
    pt = {}
    for a, b in S2: pt[key(a)] = a; pt[key(b)] = b
    for k0 in list(adj):
        for (k1, i) in adj[k0]:
            if i in used: continue
            used.add(i); L = [k0, k1]; prev = k0; cur = k1
            while cur != k0:
                nx_ = [(k, j) for k, j in adj[cur] if j not in used]
                if not nx_: break
                k, j = nx_[0]; used.add(j); L.append(k); cur = k
            if cur == k0 and len(L) > 3: loops.append(np.array([pt[k] for k in L]))
    return loops


def dilim(ad, no, eksen=None, konum=None):
    b = IDX[(ad, no)]; P = b["P"].reshape(-1, 3)
    lo, hi = P.min(0), P.max(0)
    ax = int(np.argmin(hi - lo)) if eksen is None else "xyz".index(eksen)
    c = (lo[ax] + hi[ax]) / 2.0 if konum is None else konum
    m = trimesh.Trimesh(P, np.arange(len(P)).reshape(-1, 3), process=True)
    n = np.zeros(3); n[ax] = 1.0; o = np.zeros(3); o[ax] = c
    from trimesh.intersections import mesh_plane
    seg = mesh_plane(m, n, o)
    if not len(seg): return None
    dik = [k for k in range(3) if k != ax]
    from matplotlib.path import Path as MP
    loops = []
    for q in zincir(seg[:, :, dik]):
        q = np.asarray(q)
        if len(q) < 4: continue
        x, y = q[:, 0], q[:, 1]
        A = 0.5 * abs(np.dot(x, np.roll(y, 1)) - np.dot(y, np.roll(x, 1)))
        if A < 0.5: continue
        loops.append((A, q))
    loops.sort(key=lambda t: -t[0])
    out = []
    for i, (A, q) in enumerate(loops):
        pm = q.mean(0) if False else q[0] + 1e-3
        d = 0
        for j, (A2, q2) in enumerate(loops):
            if j == i or A2 <= A: continue
            if MP(q2).contains_point(tuple(q[len(q) // 3])): d += 1
        out.append((d, q, A))
    res = dict(ad=ad, no=no, eksen="xyz"[ax], konum=round(c, 3), dik=["xyz"[k] for k in dik], lo=np.round(lo, 2).tolist(), hi=np.round(hi, 2).tolist(), dis=[], delik=[])
    for d, q, A in out:
        pts = np.round(q, 2).tolist()
        bb = [round(float(q[:, 0].min()), 2), round(float(q[:, 1].min()), 2), round(float(q[:, 0].max()), 2), round(float(q[:, 1].max()), 2)]
        if d % 2 == 0: res["dis"].append(dict(bb=bb, n=len(pts), alan=round(A, 1), pts=pts))
        else: res["delik"].append(dict(bb=bb, n=len(pts), alan=round(A, 1), pts=pts))
    return res


if __name__ == "__main__":
    tum = []
    for a in sys.argv[1:]:
        k = a.split(":"); ad, no = k[0], int(k[1]); ex = k[2] if len(k) > 2 and k[2] else None; ko = float(k[3]) if len(k) > 3 else None
        r = dilim(ad, no, ex, ko)
        if r is None: print(a, "kesit yok"); continue
        tum.append(r)
        print("== %s[%d] eksen %s=%.2f (%s,%s) dış %d delik %d" % (ad, no, r["eksen"], r["konum"], r["dik"][0], r["dik"][1], len(r["dis"]), len(r["delik"])))
        for d in r["dis"]: print("   DIŞ   bb %s n %d" % (d["bb"], d["n"]))
        for d in r["delik"]: print("   delik bb %s n %d alan %.0f" % (d["bb"], d["n"], d["alan"]))
    if os.environ.get("DILIM_JSON"):
        json.dump(tum, open(os.environ["DILIM_JSON"], "w"), indent=0)
