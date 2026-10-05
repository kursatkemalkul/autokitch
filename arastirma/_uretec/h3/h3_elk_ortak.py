# -*- coding: utf-8 -*-
"""HAT v3.2 · ELEKTRİK ORTAK ARAÇLARI (30 Eyl gece · Claude) — kablo / kablo kanalı / P-kelepçe / rakor / DIN cihazı + montaj dökümüne karşı çakışma.
Kemal: "kablolar havada olmasın, kıskaçlarla duvarlara · hangi yöntem doğruysa öyle yap · çok kompleksleştirme".
YÖNTEM (makine / pano imalatı standardı): hat boyu kablolar KAPAKLI KABLO KANALINDA (duvara vidalı) · kanaldan cihaza kısa uç kablo, uçları
P-kelepçeyle duvara / şaseye (≤ 250 mm aralık) · sac geçişleri RAKORLU (IP68 poliamid kablo rakoru) · hareketli eksen ENERJİ ZİNCİRİNDE ·
pano içi DIN rayı + delikli pano kanalı. Parçalar DÜNYA koordinatında.
Çakışma: h3/_dunya/dunya.brep (hat3_montaj_v2 dökümü) — kutu ön elemesi + gerçek katı kesişimi."""
import io, json, math, os, sys
H3 = os.path.dirname(os.path.abspath(__file__)); U = os.path.dirname(H3)
for _p in (U, H3):
    if _p not in sys.path: sys.path.insert(0, _p)
import cadquery as cq

V = cq.Vector
DD = os.path.join(H3, "_dunya")


def kut(x0, x1, y0, y1, z0, z1):
    return cq.Solid.makeBox(abs(x1 - x0), abs(y1 - y0), abs(z1 - z0), V(min(x0, x1), min(y0, y1), min(z0, z1)))


def sil(p0, p1, r):
    a, b = V(*p0), V(*p1); d = b - a
    return cq.Solid.makeCylinder(r, d.Length, a, d.normalized())


def boru(pts, r):
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


def uzunluk(pts):
    return sum(math.dist(a, b) for a, b in zip(pts[:-1], pts[1:]))


# ---------------------------------------------------------------- KABLO KANALI (kapaklı, U kesit) ----------------------------------------------------------------
def kanal(eksen, a, b, c0, c1, d0, d1, acik="+", t=1.5):
    """eksen 'x' | 'y' | 'z' boyunca a → b · kesit iki diğer eksende (c0..c1, d0..d1) · acik: kapağın baktığı yön ('+' / '-') dik eksende (d) ·
    döner (gövde, kapak): gövde U (taban + 2 yan), kapak ayrı parça (d ekseninin açık yüzünde, t kalın)"""
    a, b = min(a, b), max(a, b)
    def K(p0, p1, q0, q1, r0, r1):
        if eksen == "x": return kut(p0, p1, q0, q1, r0, r1)
        if eksen == "y": return kut(q0, q1, p0, p1, r0, r1)
        return kut(q0, q1, r0, r1, p0, p1)
    dis = K(a, b, c0, c1, d0, d1)
    if acik == "+":
        ic = K(a - 1, b + 1, c0 + t, c1 - t, d0 + t, d1 + 1)
        kap = K(a, b, c0, c1, d1, d1 + t)
    else:
        ic = K(a - 1, b + 1, c0 + t, c1 - t, d0 - 1, d1 - t)
        kap = K(a, b, c0, c1, d0 - t, d0)
    return dis.cut(ic), kap


# ---------------------------------------------------------------- P-KELEPÇE (kabloyu yüzeye tutar) ----------------------------------------------------------------
def kelepce(p, eksen, r, yuzey, yon, t=1.0, gen=12.0, tab=8.0):
    """p: kablo ekseni noktası · eksen: kablonun ekseni ('x'|'y'|'z') · r: kablo yarıçapı · yuzey: yüzeyin koordinatı (yon ekseninde) ·
    yon: yüzeyin normali ekseni ve işareti ('+x', '-z' …: kablodan yüzeye doğru). Halka (r … r + t) + yüzeye inen dil + yüzey tablası."""
    ax = "xyz".index(eksen); nx = "xyz".index(yon[1]); sg = 1.0 if yon[0] == "+" else -1.0
    e = [0, 0, 0]; e[ax] = 1
    c = V(*p); h = gen / 2.0
    a = V(*[p[i] - e[i] * h for i in range(3)])
    halka = cq.Solid.makeCylinder(r + t, gen, a, V(*e)).cut(cq.Solid.makeCylinder(r, gen + 2, a - V(*e) * 1, V(*e)))
    # dil: halkanın yüzey tarafından yüzeye (r + t kalınlığında şerit)
    lo = [p[i] - (r + t) for i in range(3)]; hi = [p[i] + (r + t) for i in range(3)]
    lo[ax], hi[ax] = p[ax] - h, p[ax] + h
    if sg > 0: lo[nx], hi[nx] = p[nx], yuzey
    else: lo[nx], hi[nx] = yuzey, p[nx]
    ok = [i for i in range(3) if i not in (ax, nx)][0]
    lo[ok], hi[ok] = p[ok] - t / 2.0 - 0.5, p[ok] + t / 2.0 + 0.5
    dil = kut(lo[0], hi[0], lo[1], hi[1], lo[2], hi[2]).cut(cq.Solid.makeCylinder(r, gen + 2, a - V(*e) * 1, V(*e)))
    # yüzey tablası (vida deliği tablası 12 × 16 × t)
    lo2 = [p[i] - tab for i in range(3)]; hi2 = [p[i] + tab for i in range(3)]          # tab 8: 16 mm tabla · dar yerde 5 (M4 vida)
    lo2[ax], hi2[ax] = p[ax] - h, p[ax] + h
    if sg > 0: lo2[nx], hi2[nx] = yuzey - t, yuzey
    else: lo2[nx], hi2[nx] = yuzey, yuzey + t
    tab = kut(lo2[0], hi2[0], lo2[1], hi2[1], lo2[2], hi2[2])
    return halka.fuse(dil).fuse(tab).clean()


def kelepceler(pts, r, yuzeyler, aralik=250.0, uc_pay=60.0):
    """polyline boyunca her ≥ aralik mm'de bir kelepçe: yuzeyler [(segment indeksi, yuzey koordinatı, yon)] · döner [(nokta, şekil)]"""
    out = []
    for i, yuz in yuzeyler:
        a, b = pts[i], pts[i + 1]; L = math.dist(a, b)
        if L < 2 * uc_pay: n = 1
        else: n = max(1, int(math.ceil((L - 2 * uc_pay) / aralik)) + 1)
        eksen = "xyz"[[abs(b[k] - a[k]) > 1e-6 for k in range(3)].index(True)]
        for j in range(n):
            f = 0.5 if n == 1 else (uc_pay + j * (L - 2 * uc_pay) / (n - 1)) / L
            p = tuple(a[k] + f * (b[k] - a[k]) for k in range(3))
            out.append((p, kelepce(p, eksen, r, yuz[0], yuz[1])))
    return out


# ---------------------------------------------------------------- RAKOR (sac geçişi) ----------------------------------------------------------------
def rakor(p, eksen, r_kablo, t_sac, yon="+", disli=None):
    """p: sacın DIŞ yüzündeki merkez · eksen: sac normali · yon: '+' → gövde sacın + tarafında (somun − tarafında) · IP68 PA rakor:
    gövde altıgen (dış) + dişli boyun sacın içinden + somun (iç) · döner (rakor, sac deliği kesicisi)"""
    ax = "xyz".index(eksen); e = [0, 0, 0]; e[ax] = 1; e = V(*e); sg = 1.0 if yon == "+" else -1.0
    rg = disli or max(6.0, r_kablo + 3.0)                       # dişli boyun yarıçapı (M12 · M16 · M20 · M25)
    c = V(*p)
    govde = cq.Solid.makeCylinder(rg + 3.5, 12.0, c, e * sg)
    boyun = cq.Solid.makeCylinder(rg, t_sac + 8.0, c - e * sg * (t_sac + 8.0), e * sg)
    somun = cq.Solid.makeCylinder(rg + 3.0, 5.0, c - e * sg * (t_sac + 5.0), e * sg)
    L_ = max(60.0, 2.0 * (t_sac + 20.0))
    r = govde.fuse(boyun).fuse(somun).cut(cq.Solid.makeCylinder(r_kablo, L_, c - e * sg * (L_ / 2.0), e * sg)).clean()
    delik = cq.Solid.makeCylinder(rg + 0.25, t_sac + 20.0, c - e * sg * (t_sac + 10.0), e * sg)
    return r, delik


# ---------------------------------------------------------------- v3.6 · HARTING Han-Modular 10B (istasyon ↔ ana pano fişli bağlantısı) ----------------------------------------------------------------
# Kemal (1 Eki): "her istasyon kendi başına çalışabilsin · istasyon kutusu ↔ ana pano tek güç + tek veri hattı, FİŞLE".
# Tek konnektör = Han-Modular 10B menteşeli çerçeve: Han E modülü (güç, 16 A · L-N-PE) + Han-Modular RJ45 modülü (Cat6A) · PE çerçeveden.
# Ölçüler (10B) [VARSAYIM: Harting föyünden teyit]: anbau (duvar) gövdesi flanş 83 × 57 × 3 + gövde 72 × 43 × 19 · pano kesiği 66 × 36 ·
# iç insert + bağlantı payı 62 × 32 × 30 (duvarın içinde) · fiş kapağı (hood) 72 × 43 × 45, ÜSTTEN çıkışlı · rakor M32 (Ø40 × 18, 2 delikli conta: güç + veri).
HAN10B = dict(fl=(83.0, 57.0, 3.0), gv=(72.0, 43.0, 19.0), kes=(66.0, 36.0), ins=(62.0, 32.0, 30.0), hood=(72.0, 43.0, 45.0), rk=(20.0, 18.0), kilit=(6.0, 47.0, 26.0))


def _eks_kut(o, n_ax, sg, L_ax, W_ax, h0, h1, L, W, cL=0.0, cW=0.0):
    """o merkez · n_ax normal ekseni (sg yönünde h0..h1) · L_ax / W_ax boyunca L × W (merkez kaydırma cL / cW)"""
    lo = list(o); hi = list(o)
    a, b = (o[n_ax] + sg * h0, o[n_ax] + sg * h1)
    lo[n_ax], hi[n_ax] = min(a, b), max(a, b)
    lo[L_ax], hi[L_ax] = o[L_ax] + cL - L / 2.0, o[L_ax] + cL + L / 2.0
    lo[W_ax], hi[W_ax] = o[W_ax] + cW - W / 2.0, o[W_ax] + cW + W / 2.0
    return kut(lo[0], hi[0], lo[1], hi[1], lo[2], hi[2])


def harting(p, n, L_eks, t_duvar=1.5, ins=True, olc=HAN10B, kilit=True):
    """p: duvarın DIŞ yüzündeki merkez · n: dışarı normal ('+y' …) · L_eks: konnektörün uzun ekseni ('x' | 'y' | 'z') · t_duvar: arkadaki sac(lar) ·
    döner dict(soket, fis, rakor, kesik, uc): soket = flanş + gövde (+ duvar içindeki insert), fis = hood + kilit kolu, rakor = üst M32, uc = kablonun çıktığı nokta"""
    n_ax = "xyz".index(n[1]); sg = 1.0 if n[0] == "+" else -1.0; L_ax = "xyz".index(L_eks)
    W_ax = [i for i in range(3) if i not in (n_ax, L_ax)][0]
    fl, gv, kes, ins_, hd, rk, kl = olc["fl"], olc["gv"], olc["kes"], olc["ins"], olc["hood"], olc["rk"], olc["kilit"]
    soket = _eks_kut(p, n_ax, sg, L_ax, W_ax, 0.0, fl[2], fl[0], fl[1]).fuse(_eks_kut(p, n_ax, sg, L_ax, W_ax, fl[2] - 0.5, fl[2] + gv[2], gv[0], gv[1]))   # flanşa gömülü 0,5 (tek katı)
    if ins:
        soket = soket.fuse(_eks_kut(p, n_ax, sg, L_ax, W_ax, -t_duvar - ins_[2], 0.0, ins_[0], ins_[1]))
    h0 = fl[2] + gv[2]
    fis = _eks_kut(p, n_ax, sg, L_ax, W_ax, h0, h0 + hd[2], hd[0], hd[1])
    for s_ in ((-1.0, 1.0) if kilit else ()):                               # tek kilit kolu (iki yanda pim + kol) · gövde ile hood eklemini sarar (karşı soket kolu taşıyorsa kilit=False)
        fis = fis.fuse(_eks_kut(p, n_ax, sg, L_ax, W_ax, h0 - 12.0, h0 + 14.0, kl[0], kl[1], cL=s_ * (hd[0] / 2.0 + kl[0] / 2.0)))
    fis = fis.clean()
    e = [0.0, 0.0, 0.0]; e[n_ax] = sg
    a = V(*[p[i] + e[i] * (h0 + hd[2]) for i in range(3)])
    rakor_ = cq.Solid.makeCylinder(rk[0], rk[1], a, V(*e))
    uc = tuple(p[i] + e[i] * (h0 + hd[2] + rk[1]) for i in range(3))
    kesik = _eks_kut(p, n_ax, sg, L_ax, W_ax, -t_duvar - (ins_[2] + 1.0 if ins else 1.0), 1.0, kes[0], kes[1])
    return dict(soket=soket.clean(), fis=fis, rakor=rakor_, kesik=kesik, uc=uc, yuk=h0 + hd[2] + rk[1])


# ---------------------------------------------------------------- DÖKÜM (çakışma) ----------------------------------------------------------------
_D = []


def dokum():
    if not _D:
        from OCP.TopoDS import TopoDS_Iterator
        idx = json.load(io.open(os.path.join(DD, "dunya.json"), encoding="utf-8"))
        sh = cq.Shape.importBrep(os.path.join(DD, "dunya.brep"))
        it = TopoDS_Iterator(sh.wrapped); ch = []
        while it.More():
            ch.append(cq.Shape.cast(it.Value())); it.Next()
        assert len(ch) == len(idx)
        for i, s in zip(idx, ch):
            b = s.BoundingBox()
            _D.append(("%s|%s" % (i[0], i[1]), s, (b.xmin, b.xmax, b.ymin, b.ymax, b.zmin, b.zmax)))
    return _D


def _ust(a, b, t=0.05):
    return a[0] < b[1] - t and b[0] < a[1] - t and a[2] < b[3] - t and b[2] < a[3] - t and a[4] < b[5] - t and b[4] < a[5] - t


def cakisma(sh, haric=(), esik=0.5):
    """sh ↔ montaj dökümü · haric: ad önekleri ('BIRIM|parca' ya da 'BIRIM|') · döner [(ad, hacim)]"""
    b = sh.BoundingBox(); bb = (b.xmin, b.xmax, b.ymin, b.ymax, b.zmin, b.zmax); out = []
    for ad, s, sb in dokum():
        if not _ust(bb, sb): continue
        if haric and ad.startswith(tuple(haric)): continue
        try: v = sh.intersect(s).Volume()
        except Exception: v = -1.0
        if v > esik or v < 0: out.append((ad, round(v, 1)))
    return out


def yakin(bb, pay=30.0, onek=None):
    """kutu çevresindeki döküm parçaları (bilgi / yol arama)"""
    q = (bb[0] - pay, bb[1] + pay, bb[2] - pay, bb[3] + pay, bb[4] - pay, bb[5] + pay)
    return [(ad, sb) for ad, s, sb in dokum() if _ust(q, sb, 0.0) and (onek is None or ad.startswith(onek))]
