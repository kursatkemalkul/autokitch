# -*- coding: utf-8 -*-
"""ADIM 47 ortak geometri: standart bağlantı elemanları (CadQuery katısı, mm, dünya) — eksen +x/−x/+y/−y/+z/−z.
Her eleman dict(ad, sh, bom, tur) · tur: 'saplama' | 'civata' | 'somun' | 'pul' | 'kaynak_somunu' | 'percin_somun' | 'perçin' | 'sac' (konsol / plaka)
Ölçüler: PEM FHS (Bülten FH), ISO 4762, ISO 7380-1, ISO 4032, DIN 125-A, DIN 929, kapalı uçlu perçin somun (düz baş), DIN 7337 kör perçin."""
import numpy as np
import cadquery as cq

V = cq.Vector
SOMUN = {"M3": (5.5, 2.4), "M4": (7.0, 3.2), "M5": (8.0, 4.7), "M6": (10.0, 5.2), "M8": (13.0, 6.8)}            # ISO 4032 s, m
PUL = {"M3": (7.0, 0.5, 3.2), "M4": (9.0, 0.8, 4.3), "M5": (10.0, 1.0, 5.3), "M6": (12.0, 1.6, 6.4), "M8": (16.0, 1.6, 8.4)}  # DIN 125-A d2, h, d1
KAFA4762 = {"M4": (7.0, 4.0), "M5": (8.5, 5.0), "M6": (10.0, 6.0), "M8": (13.0, 8.0)}
KAFA7380 = {"M4": (7.6, 2.2), "M5": (9.5, 2.75), "M6": (10.5, 3.3)}
FHS_BAS = {"M3": (6.1, 1.0), "M4": (7.1, 1.0), "M5": (8.1, 1.0), "M6": (9.6, 1.2)}                                # FH baş Ø, sac içinde gömülü baş yüksekliği
DIN929 = {"M5": (8.0, 4.0), "M6": (10.0, 5.0)}                                                    # kaynak somunu s, h (pilotsuz model)
D = {"M3": 3.0, "M4": 4.0, "M5": 5.0, "M6": 6.0, "M8": 8.0}


def _n(n):
    n = np.asarray(n, float); return n / np.linalg.norm(n)


def sil(r, o, n, a, b):
    """o + n·t, t ∈ [a, b] silindir"""
    n = _n(n); p0 = np.asarray(o, float) + n * a
    return cq.Solid.makeCylinder(r, b - a, V(*p0), V(*n))


def alti(s, o, n, a, b):
    """altıgen prizma (anahtar ağzı s) eksen n, t ∈ [a, b]"""
    n = _n(n); p0 = np.asarray(o, float) + n * a
    pl = cq.Plane(origin=V(*p0), xDir=V(*_dik(n)), normal=V(*n))
    return cq.Workplane(pl).polygon(6, s / np.cos(np.pi / 6)).extrude(b - a).val()


def _dik(n):
    a = np.array([1.0, 0, 0]) if abs(n[0]) < 0.9 else np.array([0, 1.0, 0])
    u = np.cross(n, a); return u / np.linalg.norm(u)


def halka(R, r, o, n, a, b):
    return sil(R, o, n, a, b).cut(sil(r, o, n, a - 0.01, b + 0.01))


def kutu(lo, hi):
    lo = np.asarray(lo, float); hi = np.asarray(hi, float)
    return cq.Solid.makeBox(*(hi - lo), V(*lo))


def fhs(m, L, o, n, t, ad, not_=""):
    """PEM FHS-m-L paslanmaz saplama: o = sacın ÖN yüzü (saplamanın çıktığı yüz) eksen noktası, n = çıkış yönü, t = sac kalınlığı.
    Baş sac içinde gömülü (arka yüzle aynı düzlem), gövde ön yüzden L."""
    dk, h = FHS_BAS[m]; h = min(h, t)
    bas = sil(dk / 2.0, o, n, -t, -t + h); gov = sil(D[m] / 2.0, o, n, -t + h, L)
    return dict(ad=ad, sh=bas.fuse(gov).clean(), bom=["PEM FHS-%s-%d kendinden perçinli saplama (paslanmaz) %s" % (m, L, not_)], tur="saplama", n=list(_n(n)))


def pul(m, o, n, a, ad):
    d2, h, d1 = PUL[m]
    return dict(ad=ad, sh=halka(d2 / 2.0, d1 / 2.0, o, n, a, a + h), bom=["DIN 125-A %s pul A2" % m], tur="pul", n=list(_n(n))), a + h


def somun(m, o, n, a, ad):
    s, h = SOMUN[m]
    return dict(ad=ad, sh=alti(s, o, n, a, a + h).cut(sil(D[m] / 2.0, o, n, a - 0.01, a + h + 0.01)), bom=["ISO 4032 %s somun A2" % m], tur="somun", n=list(_n(n))), a + h


def civata4762(m, L, o, n, a, ad):
    """baş altı düzlemi o + n·a, gövde +n yönünde L · baş −n tarafında"""
    dk, k = KAFA4762[m]
    sh = sil(dk / 2.0, o, n, a - k, a).fuse(sil(D[m] / 2.0, o, n, a, a + L)).clean()
    return dict(ad=ad, sh=sh, bom=["ISO 4762 %s × %d A2 imbus cıvata" % (m, L)], tur="civata", n=list(_n(n)))


def civata7380(m, L, o, n, a, ad):
    dk, k = KAFA7380[m]
    bas = sil(dk / 2.0, o, n, a - k, a)
    sh = bas.fuse(sil(D[m] / 2.0, o, n, a, a + L)).clean()
    return dict(ad=ad, sh=sh, bom=["ISO 7380-1 %s × %d A2 bombe başlı cıvata" % (m, L)], tur="civata", n=list(_n(n)))


def kaynak_somunu(m, o, n, a, ad):
    s, h = DIN929[m]
    return dict(ad=ad, sh=alti(s, o, n, a, a + h).cut(sil(D[m] / 2.0, o, n, a - 0.01, a + h + 0.01)), bom=["DIN 929 %s kaynak somunu A2 (uç plakasına TIG)" % m], tur="kaynak_somunu", n=list(_n(n))), a + h


def percin_somun_kapali(o, n, ad, m="M8", bas_d=15.0, bas_h=1.5, gov_d=11.0, boy=21.5, dis_derin=16.5):
    """kapalı uçlu düz başlı perçin somun: o = baş üst yüzü ekseni, n = deliğe giriş yönü (gövde n yönünde) · iç diş Ø m, derinlik dis_derin, kör uç"""
    bas = sil(bas_d / 2.0, o, n, 0.0, bas_h)
    gov = sil(gov_d / 2.0, o, n, bas_h - 0.01, boy)
    sh = bas.fuse(gov).clean().cut(sil(D[m] / 2.0, o, n, -0.01, dis_derin))
    return dict(ad=ad, sh=sh, bom=["%s kapalı uçlu perçin somun, düz baş Ø%.0f, A2 (kör uç, iç diş derinliği %.1f)" % (m, bas_d, dis_derin)], tur="percin_somun", n=list(_n(n)))


def kor_percin(o, n, a, L, ad, d=3.2, dk=6.4, k=1.0, bulb=4.5):
    """DIN 7337 kör perçin Ø d (A2/A2): baş −n tarafında (o + n·a'da baş altı), gövde L, kapalı uçta şişkin uç (bulb Ø)"""
    sh = sil(dk / 2.0, o, n, a - k, a).fuse(sil(d / 2.0, o, n, a, a + L - 1.5)).fuse(sil(bulb / 2.0, o, n, a + L - 1.5, a + L)).clean()
    return dict(ad=ad, sh=sh, bom=["DIN 7337 kör perçin Ø%.1f × %.0f A2 (sıkılmış)" % (d, L)], tur="percin", n=list(_n(n)))
