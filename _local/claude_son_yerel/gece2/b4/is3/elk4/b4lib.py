# -*- coding: utf-8 -*-
"""elk4 ortak: tasarım (YOL: yeniden çizilen kablolar, KAN: yeni kapaklı iç kanallar) -> kontrol + GLB'ye yazma.
Kanal: 304 1,2 mm kapaklı (elk3 ile aynı kanal() geometrisi), kablo geçtiği yüzlerde otomatik delik, uç kapağı geçişte açık."""
import sys, pickle, re, numpy as np
S = r"C:\Users\Kemal\AppData\Local\Temp\claude\C--Users-Kemal-Desktop-Kemal-WEBS-TE\f3ef876a-f062-4b29-bb81-775cc8a1a6d8\scratchpad\gece2\b4\is3"
for q in (S + r"\elk4", S + r"\elk2", S + r"\gece", S, S + r"\birlesim"): sys.path.insert(0, q)
from elib import kanal, tup, kutu
D = pickle.load(open(S + r"\elk4\kay0.pkl", "rb")); KAY = D["KAY"]
T_KANAL = 1.2


def seg_list(ci, YOL):
    """kablo ci'nin doğru parçaları [(a,b,r)] (yeniden çizildiyse yeni yol)"""
    d = KAY[ci]
    if ci in YOL:
        out = []
        r = YOL[ci].get("r", d["r"])
        for Q in YOL[ci]["yol"]:
            Q = [np.asarray(q, float) for q in Q]
            out += [(a, b, r) for a, b in zip(Q[:-1], Q[1:])]
        return out
    return [(q["a"], q["b"], q["r"]) for q in d["S"]]


def kanal_geo(k, segs):
    """k = dict(lo, hi, e, ad, ist). segs: [(a,b,r)] tüm kablolar -> (üçgenler, delik listesi)"""
    lo = np.asarray(k["lo"], float); hi = np.asarray(k["hi"], float); e = k["e"]
    u, w = [i for i in range(3) if i != e]
    t = T_KANAL; delik = {}; uc = [True, True]
    for a, b, r in segs:
        v = b - a
        # 4 duvar düzlemi (u-, u+, w-, w+) + 2 uç kapağı
        for ax in (u, w, e):
            for sg, val in ((-1, lo[ax]), (1, hi[ax])):
                if abs(v[ax]) < 1e-9: continue
                for pl in (val, val - sg * t):          # duvarın iki yüzü
                    s = (pl - a[ax]) / v[ax]
                    if s < -1e-6 or s > 1 + 1e-6: continue
                    P = a + s * v
                    oth = [i for i in range(3) if i != ax]
                    if not all(lo[i] - r <= P[i] <= hi[i] + r for i in oth): continue
                    if ax == e:
                        uc[0 if sg < 0 else 1] = False; continue
                    o2 = w if ax == u else u
                    m = r + 1.5
                    rc = (max(lo[e], P[e] - m), min(hi[e], P[e] + m), max(lo[o2] + t, P[o2] - m), min(hi[o2] - t, P[o2] + m))
                    L = delik.setdefault((ax, sg), [])
                    if not any(abs(rc[0] - q[0]) < 0.5 and abs(rc[2] - q[2]) < 0.5 for q in L): L.append(rc)
    for kk in ("uc0", "uc1"):
        if kk in k: uc[0 if kk == "uc0" else 1] = k[kk]
    lo2 = (lo[u], lo[w]); hi2 = (hi[u], hi[w])
    g = kanal(e, lo[e], hi[e], lo2, hi2, t, delik=delik, uc=tuple(uc))
    return g, delik, uc


def boru_kutular(segs):
    """kablo parçaları -> eksen hizalı kutular (çakışma ön denetimi)"""
    out = []
    for a, b, r in segs:
        out.append((np.minimum(a, b) - r, np.maximum(a, b) + r))
    return out


def kesisim(segsA, segsB, pay=0.2):
    """iki kablo arası en kısa mesafe < rA+rB-pay olan parça çiftleri"""
    hits = []
    for a, b, r in segsA:
        for c, d, s in segsB:
            dmin = seg_seg(a, b, c, d)
            if dmin < r + s - pay: hits.append((np.round(a).tolist(), np.round(c).tolist(), round(dmin, 2)))
    return hits


def seg_seg(p1, q1, p2, q2):
    d1 = q1 - p1; d2 = q2 - p2; r = p1 - p2
    a = d1 @ d1; e = d2 @ d2; f = d2 @ r
    if a < 1e-12 and e < 1e-12: return float(np.linalg.norm(r))
    if a < 1e-12: s = 0.0; t = np.clip(f / e, 0, 1)
    else:
        c = d1 @ r
        if e < 1e-12: t = 0.0; s = np.clip(-c / a, 0, 1)
        else:
            b = d1 @ d2; den = a * e - b * b
            s = np.clip((b * f - c * e) / den, 0, 1) if den > 1e-12 else 0.0
            t = (b * s + f) / e
            if t < 0: t = 0.0; s = np.clip(-c / a, 0, 1)
            elif t > 1: t = 1.0; s = np.clip((b - c) / a, 0, 1)
    return float(np.linalg.norm(p1 + d1 * s - (p2 + d2 * t)))


def acik_uzunluk(segs, kanallar, uclar):
    """kablo parçalarının kanal kutuları dışındaki kısmı; uçlardan ≤150 mm (yol boyu) hariç. -> (toplam açık, 150 sonrası açık)"""
    # yol boyu: parçalar sıralı kabul (tek zincir)
    toplam = 0.0; fazla = 0.0; s = 0.0
    L = sum(np.linalg.norm(b - a) for a, b, r in segs)
    for a, b, r in segs:
        l = np.linalg.norm(b - a); n = max(2, int(l / 2) + 1)
        for i in range(n - 1):
            t0 = i / (n - 1); t1 = (i + 1) / (n - 1); P = a + (t0 + t1) / 2 * (b - a); dl = l / (n - 1)
            ic = any(np.all(P >= np.asarray(k["lo"]) + 0.5) and np.all(P <= np.asarray(k["hi"]) - 0.5) for k in kanallar)
            if not ic:
                toplam += dl
                sp = s + (t0 + t1) / 2 * l
                if (uclar[0] and sp <= 150) or (uclar[1] and L - sp <= 150): pass
                else: fazla += dl
        s += l
    return toplam, fazla


def zincir(segs):
    """sırasız parçaları uçtan uca sırala (ana zincir; dallar sona eklenir)"""
    segs = [(np.asarray(a, float), np.asarray(b, float), r) for a, b, r in segs]
    if len(segs) <= 1: return segs
    def bagli(P, j):
        a, b, r = segs[j]
        return min(np.linalg.norm(P - a), np.linalg.norm(P - b)) < 2 * r + 3
    # uç: başka parçaya değmeyen uç noktası
    bas = None
    for i, (a, b, r) in enumerate(segs):
        for P in (a, b):
            if not any(bagli(P, j) for j in range(len(segs)) if j != i): bas = (i, P); break
        if bas: break
    if bas is None: bas = (0, segs[0][0])
    out = []; kalan = set(range(len(segs))); i, P = bas
    while True:
        a, b, r = segs[i]; kalan.discard(i)
        if np.linalg.norm(P - a) <= np.linalg.norm(P - b): out.append((a, b, r)); P = b
        else: out.append((b, a, r)); P = a
        nx = [j for j in kalan if bagli(P, j)]
        if not nx: break
        i = min(nx, key=lambda j: min(np.linalg.norm(P - segs[j][0]), np.linalg.norm(P - segs[j][1])))
    out += [segs[j] for j in sorted(kalan)]
    return out
