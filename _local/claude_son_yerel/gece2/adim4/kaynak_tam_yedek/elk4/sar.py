# -*- coding: utf-8 -*-
"""elk4 2: istasyon kablo bacakları -> kanal gereken parçalar, duvar mesafeleri (analiz). python sar.py ISTASYON"""
import sys, pickle, re, numpy as np
S = r"@@KOK_W@@"
sys.path.insert(0, S + r"\elk4")
from ortam4 import Ortam, bolge
IST = dict(TOPPING=((1434, 788, -832), (2500, 2200, 80)), F=((2500, 788, -832), (4000, 1862, 80)), U=((2500, 1840, -832), (4000, 2200, 80)),
           K=((4000, 788, -832), (4400, 2200, 80)), E=((4400, 788, -832), (5232, 2200, 80)), B=((736, 0, -832), (4400, 788, 80)),
           QR=((4560, 0, 660), (5440, 2060, 1200)))
D = pickle.load(open(S + r"\elk4\kay0.pkl", "rb"))
O0 = Ortam()
def kapali_m(O):
    return np.array([bool(re.search(r"__kanal$|__pano$|K_ELEKTRIK__sac$|__pano__", a)) for a in O.nm])
def ucler(Sg):
    E = []
    for i, q in enumerate(Sg):
        for P in (q['a'], q['b']):
            deg = 0
            for j, w in enumerate(Sg):
                if j == i: continue
                dv = w['b'] - w['a']; L2 = max(dv @ dv, 1e-9); t = np.clip((P - w['a']) @ dv / L2, 0, 1)
                if np.linalg.norm(w['a'] + t * dv - P) < q['r'] + w['r'] + 2: deg += 1
            if deg == 0: E.append(P)
    return E
def jeo(Sg, E):
    """her segment örnek noktasının en yakın uca yol uzaklığı (yaklaşık: Dijkstra segment uç düğümleri)"""
    import heapq
    N = []; 
    def nid(P):
        for k, Q in enumerate(N):
            if np.linalg.norm(Q - P) < 8: return k
        N.append(P); return len(N) - 1
    ed = {}
    for q in Sg:
        a, b = nid(q['a']), nid(q['b']); L = np.linalg.norm(q['b'] - q['a'])
        ed.setdefault(a, []).append((b, L)); ed.setdefault(b, []).append((a, L)); q['na'], q['nb'] = a, b
    dist = [np.inf] * len(N); h = []
    for P in E:
        k = nid(P); dist[k] = 0; heapq.heappush(h, (0, k))
    while h:
        d, k = heapq.heappop(h)
        if d > dist[k]: continue
        for j, L in ed.get(k, []):
            if d + L < dist[j]: dist[j] = d + L; heapq.heappush(h, (d + L, j))
    return dist
if __name__ == "__main__":
    ist = sys.argv[1]; lo, hi = IST[ist]
    O = bolge(O0, np.array(lo) - 100, np.array(hi) + 100); KM = kapali_m(O)
    for ci, d in enumerate(D['KAY']):
        if d['ist'] != ist or not d['S']: continue
        Sg = d['S']; E = ucler(Sg); dist = jeo(Sg, E)
        print("#%d %s r%.1f uc %d" % (ci, d['prim'], d['r'], len(E)))
        for q in Sg:
            a, b = q['a'], q['b']; v = b - a; L = np.linalg.norm(v)
            if L < 1: continue
            e = int(np.argmax(np.abs(v))); ax = [i for i in range(3) if i != e]
            n = max(2, int(L / 15) + 1); ts = np.linspace(0, 1, n)
            ihtiyac = []; kap = []
            for t in ts:
                P = a + t * v
                dd = min(dist[q['na']] + t * L, dist[q['nb']] + (1 - t) * L)
                inside = all(O.isin(P, s * np.eye(3)[k], 45, KM)[0] < 45 for k in ax for s in (1, -1))
                kap.append(inside); ihtiyac.append((not inside) and dd > 150)
            ih = np.array(ihtiyac)
            if not ih.any(): 
                print("   %-40s L%5.0f tamam (kapalı %.0f%%)" % ("%s->%s" % (np.round(a).astype(int).tolist(), np.round(b).astype(int).tolist()), L, 100 * np.mean(kap))); continue
            wd = {}
            for k in ax:
                for s in (1, -1):
                    ds = [O.isin(a + t * v, s * np.eye(3)[k], 80, O.yapi & ~KM)[0] for t in ts[ih]]
                    wd["%s%s" % ("+" if s > 0 else "-", "xyz"[k])] = max(ds)
            print("   %-40s L%5.0f KANAL %.0f%%  duvar %s" % ("%s->%s" % (np.round(a).astype(int).tolist(), np.round(b).astype(int).tolist()), L, 100 * ih.mean(), {k: round(v_, 1) for k, v_ in wd.items()}))
