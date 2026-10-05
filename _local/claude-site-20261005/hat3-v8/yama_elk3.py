# -*- coding: utf-8 -*-
import io, os
H3 = r"C:\Users\Kemal\AppData\Local\Temp\claude\C--Users-Kemal-Desktop-Kemal-WEBS-TE\f3ef876a-f062-4b29-bb81-775cc8a1a6d8\scratchpad\b3\arastirma\_uretec\h3"


def yama(dosya, ciftler):
    P = os.path.join(H3, dosya)
    s = io.open(P, encoding="utf-8").read()
    for a, b in ciftler:
        assert s.count(a) == 1, (dosya, a[:80], s.count(a))
        s = s.replace(a, b)
    io.open(P, "w", encoding="utf-8").write(s)
    print("yamalandı:", dosya, len(ciftler))


# 1 · rakor deliği sacın tamamını geçsin (kalın sandviç duvarlarda boyun delinmemiş kalıyordu)
yama("h3_elk_ortak.py", [(
    "    r = govde.fuse(boyun).fuse(somun).cut(cq.Solid.makeCylinder(r_kablo, 60.0, c - e * sg * 30.0, e * sg)).clean()",
    "    L_ = max(60.0, 2.0 * (t_sac + 20.0))\n"
    "    r = govde.fuse(boyun).fuse(somun).cut(cq.Solid.makeCylinder(r_kablo, L_, c - e * sg * (L_ / 2.0), e * sg)).clean()")])

# 2 · voksel A*: ağırlıklı sezgi (hızlı) + daha yüksek sınır
yama("h3_elk_voksel.py", [
    ("def bul(S, T, r, pay=1.0, h=4.0, marj=160.0, bolge=None, haric=(), ic_bos=(), yakin_w=1.2):",
     "def bul(S, T, r, pay=1.0, h=4.0, marj=160.0, bolge=None, haric=(), ic_bos=(), yakin_w=1.2, w=1.8):"),
    ("        if say > 1500000: return None, \"A* sınırı\"", "        if say > 4000000: return None, \"A* sınırı\""),
    ("                heapq.heappush(acik, (g2 + hs(n), g2, n, di))", "                heapq.heappush(acik, (g2 + w * hs(n), g2, n, di))"),
    ("    acik = [(hs(s0), 0, s0, -1)]", "    acik = [(w * hs(s0), 0, s0, -1)]"),
])

# 3 · kelepçe: çakışan kelepçe konulmaz, segment boyunca kaydırılır
yama("h3_elk_rota.py", [(
    '''def kelepceler(pts, r, aralik=250.0, haric=()):
    """≥ 200 mm parçalara ~250 mm aralıkla, en yakın yüzeye kelepçe · döner ([(nokta, şekil)], [askıda kalan parça])"""
    out, aski = [], []
    for a, b in zip(pts[:-1], pts[1:]):
        L = math.dist(a, b)
        if L < 200.0: continue
        eksen = "xyz"[[abs(b[k] - a[k]) > 1e-6 for k in range(3)].index(True)]
        n = max(1, int(L // aralik))
        for j in range(n):
            f = (j + 0.5) / n
            p = tuple(a[k] + f * (b[k] - a[k]) for k in range(3))
            y = kelepce_yeri(p, eksen, r, haric=haric)
            if y is None: aski.append((a, b, p)); continue
            out.append((p, EO.kelepce(p, eksen, r, y[0], y[1])))
    return out, aski''',
    '''def kelepceler(pts, r, aralik=250.0, haric=()):
    """≥ 200 mm parçalara ~250 mm aralıkla, en yakın yüzeye kelepçe · kelepçe başka parçaya değiyorsa parça boyunca ±20 / ±40 / ±60 mm kaydırılır ·
    döner ([(nokta, şekil)], [askıda kalan parça])"""
    out, aski = [], []
    for a, b in zip(pts[:-1], pts[1:]):
        L = math.dist(a, b)
        if L < 200.0: continue
        eksen = "xyz"[[abs(b[k] - a[k]) > 1e-6 for k in range(3)].index(True)]
        n = max(1, int(L // aralik))
        for j in range(n):
            f0 = (j + 0.5) / n; kon = None; p0 = None
            for dd in (0.0, 20.0, -20.0, 40.0, -40.0, 60.0, -60.0):
                f = f0 + dd / L
                if not (15.0 / L < f < 1.0 - 15.0 / L): continue
                p = tuple(a[k] + f * (b[k] - a[k]) for k in range(3)); p0 = p0 or p
                y = kelepce_yeri(p, eksen, r, haric=haric)
                if y is None: continue
                ks = EO.kelepce(p, eksen, r, y[0], y[1])
                if temiz(ks, haric)[0]: kon = (p, ks); break
            if kon is None: aski.append((a, b, p0 or a)); continue
            out.append(kon)
    return out, aski''')])
print("tamam")
