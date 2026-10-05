# -*- coding: utf-8 -*-
import io, os
H3 = r"C:\Users\Kemal\AppData\Local\Temp\claude\C--Users-Kemal-Desktop-Kemal-WEBS-TE\f3ef876a-f062-4b29-bb81-775cc8a1a6d8\scratchpad\b3\arastirma\_uretec\h3"


def yama(dosya, ciftler):
    P = os.path.join(H3, dosya)
    s = io.open(P, encoding="utf-8").read()
    for a, b in ciftler:
        assert s.count(a) == 1, (dosya, a[:100], s.count(a))
        s = s.replace(a, b)
    io.open(P, "w", encoding="utf-8").write(s)
    print("yamalandı:", dosya, len(ciftler))


P = os.path.join(H3, "h3_elk_ortak.py")
s = io.open(P, encoding="utf-8").read()
i0 = s.index("def boru(pts, r):")
i1 = s.index("def uzunluk(pts):")
yeni = '''def boru(pts, r):
    """kablo: düz parçalar, iç köşelerde komşu parçalar birbirinin içine r kadar uzar (köşe dolu, katı birleştirme sağlam ·
    eski 'köşede küre' teğet yüzey yüzünden birleştirmeyi bozuyordu) · uçlar düz (kanal / pano / cihaz yüzüne dayanır)"""
    q = [pts[0]]
    for p in pts[1:]:
        if math.dist(p, q[-1]) > 1e-6: q.append(p)
    n = len(q); ss = []
    for i, (a, b) in enumerate(zip(q[:-1], q[1:])):
        ss.append(sil_uzun(a, b, r, i > 0, i < n - 2))
    if len(ss) == 1: return ss[0]
    alt = sum(math.pi * r * r * math.dist(a, b) for a, b in zip(q[:-1], q[1:]))
    adaylar = []
    try:
        s = ss[0]
        for x in ss[1:]: s = s.fuse(x)
        adaylar.append(s.clean())
    except Exception:
        pass
    try:
        adaylar.append(ss[0].fuse(*ss[1:], tol=0.01).clean())
    except Exception:
        pass
    for s in adaylar:
        try:
            if len(s.Solids()) == 1 and s.Volume() >= 0.7 * alt: return s.Solids()[0]
        except Exception:
            continue
    return cq.Compound.makeCompound(ss)


def sil_uzun(a, b, r, bas_uzat, son_uzat):
    L = math.dist(a, b); d = [(b[k] - a[k]) / L for k in range(3)]
    a2 = tuple(a[k] - d[k] * r for k in range(3)) if bas_uzat else a
    b2 = tuple(b[k] + d[k] * r for k in range(3)) if son_uzat else b
    return sil(a2, b2, r)


'''
s = s[:i0] + yeni + s[i1:]
io.open(P, "w", encoding="utf-8").write(s)
print("yamalandı: h3_elk_ortak.py boru")

yama("h3_elk_rota.py", [(
    '''        for j_, (a_, b_) in enumerate(zip(q[:-1], q[1:])):          # parça parça (ince kutular → az aday) · sonuç önbellekte
            son_ = j_ == len(q) - 2                                 # son parçanın ucu düz (kanal / pano yüzüne dayanır)
            k_ = (tuple(round(v, 1) for v in a_), tuple(round(v, 1) for v in b_), r, son_)
            if k_ not in _ONB:
                seg = EO.sil(a_, b_, r)
                if not son_: seg = seg.fuse(cq.Solid.makeSphere(r, V(*b_), angleDegrees1=-90, angleDegrees2=90))''',
    '''        for j_, (a_, b_) in enumerate(zip(q[:-1], q[1:])):          # parça parça (ince kutular → az aday) · sonuç önbellekte
            son_ = j_ == len(q) - 2; bas_ = j_ == 0                 # uçlar düz · iç köşelerde parça r kadar uzar (EO.boru ile aynı zarf)
            k_ = (tuple(round(v, 1) for v in a_), tuple(round(v, 1) for v in b_), r, son_, bas_)
            if k_ not in _ONB:
                seg = EO.sil_uzun(a_, b_, r, not bas_, not son_)''')])
print("tamam")
