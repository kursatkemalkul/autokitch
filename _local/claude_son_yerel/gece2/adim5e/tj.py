import numpy as np
def tjunction_onar(P, tol=1e-3, tur=6):
    """açık ağ (T-birleşimli) → sınır kenarı üzerinde duran köşelerde üçgeni böl · dönüş: yeni P"""
    R = np.round(P.reshape(-1, 3), 4); V, inv = np.unique(R, axis=0, return_inverse=True); F = inv.reshape(-1, 3).tolist()
    for _ in range(tur):
        E = {}
        for fi, f in enumerate(F):
            for k in range(3):
                E.setdefault((f[k], f[(k + 1) % 3]), []).append(fi)
        bd = [e for e in E if (e[1], e[0]) not in E]
        if not bd: break
        bv = np.unique(np.array(bd).reshape(-1))
        Q = V[bv]
        bol = {}
        for a, b in bd:
            A, B = V[a], V[b]; d = B - A; L2 = d @ d
            if L2 < 1e-12: continue
            t = (Q - A) @ d / L2
            m = (t > 1e-6) & (t < 1 - 1e-6)
            if not m.any(): continue
            C = A + t[m, None] * d; dist = np.linalg.norm(Q[m] - C, axis=1)
            ok = dist < tol
            if not ok.any(): continue
            ids = bv[m][ok]; ts = t[m][ok]; o = np.argsort(ts)
            fi = E[(a, b)][0]
            bol.setdefault(fi, []).append((a, b, [int(x) for x in ids[o]]))
        if not bol: break
        NF = []
        for fi, f in enumerate(F):
            if fi not in bol: NF.append(f); continue
            # her kenar için ara noktalar → poligon → üçgen yelpazesi (karşı köşeden)
            poly = []
            ek = {(a, b): ids for a, b, ids in bol[fi]}
            for k in range(3):
                a, b = f[k], f[(k + 1) % 3]; poly.append(a); poly += ek.get((a, b), [])
            # yelpaze: yeni nokta içermeyen köşeden başla
            yeni = set(i for _, _, ids in bol[fi] for i in ids)
            s0 = next(i for i, v in enumerate(poly) if v not in yeni and poly[(i - 1) % len(poly)] in yeni or False) if False else 0
            # kenar ortası noktaları olmayan köşeyi seç
            for i, v in enumerate(poly):
                pv, nv = poly[(i - 1) % len(poly)], poly[(i + 1) % len(poly)]
                if v not in yeni and pv not in yeni and nv not in yeni: s0 = i; break
            else:
                for i, v in enumerate(poly):
                    if v not in yeni: s0 = i; break
            pp = poly[s0:] + poly[:s0]
            for i in range(1, len(pp) - 1):
                tri = [pp[0], pp[i], pp[i + 1]]
                A, B, C = V[tri]
                if np.linalg.norm(np.cross(B - A, C - A)) > 1e-9: NF.append(tri)
        F = NF
    F = np.array(F)
    return V[F]
