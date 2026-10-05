# -*- coding: utf-8 -*-
"""TOPPING v2 · STATİK ÇAKIŞMA DENETİMİ (dünya): v2'nin bütün parçaları (montajın düşürdükleri hariç) ikili gerçek kesişim ·
v1'de de aynı çiftte aynı ölçüde olan temaslar (pres geçme, oturma) 'v1'de de var' diye ayrılır; YENİ olanlar raporlanır."""
import os, sys, time, json
H2 = os.path.dirname(os.path.abspath(__file__)); U = os.path.dirname(H2)
for _p in (U, H2):
    if _p not in sys.path: sys.path.insert(0, _p)
import cadquery as cq
import h3_topping_v1 as T

ESIK = 1.0          # mm³


def _bb(s):
    b = s.BoundingBox(); return (b.xmin, b.xmax, b.ymin, b.ymax, b.zmin, b.zmax)


def _ust(a, b, t=0.01):
    return a[0] < b[1] - t and b[0] < a[1] - t and a[2] < b[3] - t and b[2] < a[3] - t and a[4] < b[5] - t and b[4] < a[5] - t


def _hacim(a, b):
    try:
        return abs(a.intersect(b).Volume())
    except Exception:
        return -1.0


def liste():
    TC, TU = T.kur()
    W = [("TC:" + p["ad"], p["sh"]) for p in TC]
    W += [("TU:" + q["ad"], q["sh"]) for q in TU if not q["ad"].startswith(T.TU_YERINDE)]
    return W


def v1_sozluk():
    d = {"TC:" + p["ad"]: p["sh"] for p in T._v1_tc()}
    d.update({"TU:" + q["ad"]: q["sh"] for q in T._v1_tu()})
    return d


def tara(W, filtre=None):
    B = [(a, s, _bb(s)) for a, s in W]
    B.sort(key=lambda t: t[2][0])
    out = []
    for i in range(len(B)):
        a, sa, ba = B[i]
        for j in range(i + 1, len(B)):
            b, sb, bb = B[j]
            if bb[0] >= ba[1]: break
            if not _ust(ba, bb): continue
            if filtre and not filtre(a, b): continue
            v = _hacim(sa, sb)
            if v > ESIK or v < 0: out.append((a, b, round(v, 2)))
    return out


if __name__ == "__main__":
    t0 = time.time()
    W = liste()
    print("parça %d · %.0f sn" % (len(W), time.time() - t0)); sys.stdout.flush()
    cak = tara(W)
    print("çakışan çift %d · %.0f sn" % (len(cak), time.time() - t0)); sys.stdout.flush()
    V1 = v1_sozluk()
    yeni, eski = [], []
    for a, b, v in cak:
        if a in V1 and b in V1:
            v1 = _hacim(V1[a], V1[b])
            if v1 > 0.5 * v and v1 > ESIK:
                eski.append((a, b, v, round(v1, 2))); continue
        yeni.append((a, b, v))
    print("v1'de de var: %d" % len(eski))
    for r in eski[:80]: print("   (v1)", r)
    print("YENİ ÇAKIŞMA: %d" % len(yeni))
    for r in sorted(yeni, key=lambda r: -r[2])[:200]: print("   ", r)
    json.dump(dict(yeni=yeni, eski=eski), open(os.path.join(H2, "_denetim_topping_v1.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    sys.stdout.flush(); os._exit(0)
