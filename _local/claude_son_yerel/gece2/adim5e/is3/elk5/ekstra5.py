# -*- coding: utf-8 -*-
"""elk5 ek isler: ana pano arka cikisi (kablolar dik kanallarda), yan rakorlar kalkar + delikler kapanir, V1 ust kapagi, bina kablosu saltere kisa yol,
ana salter DIN rayinda (ABB OT40F4) + kapakta OHYS2AJ kol + OXP6X mil, eski kapak deligi kor tapa, bosta kompresor hortumu, QR goz ust plakasi
kanal gecisleri, QR musteri paneli kablolari."""
import re, numpy as np
import ek
from ek import komps
from elib import kutu, silindir
from m8kit import tup, delik_ucgenler, kutu_ucgen


def _sil_comp(G, ad, kosul, rapor, etiket):
    n = 0; et = None
    for p in G.prims:
        if p.get("gizli") or p["name"] != ad: continue
        for tri, a, b in komps(G, p):
            if kosul(a, b):
                if et is None: et = (p, G._etiketler(p, int(tri[0])))
                m = np.zeros(len(p["T"]), bool); m[tri] = True; n += G.sil(p, m)
    rapor("sil %s (%s)" % (ad, etiket), n); return et


def halka(c, r0, r1, z0, z1, n=32):
    """z eksenli halka (ic r0, dis r1)"""
    th = np.linspace(0, 2 * np.pi, n + 1); out = []
    def P(r, t, z): return np.array([c[0] + r * np.cos(t), c[1] + r * np.sin(t), z])
    for i in range(n):
        a, b = th[i], th[i + 1]
        for (ra, za), (rb, zb) in (((r1, z0), (r1, z1)), ((r0, z1), (r0, z0)), ((r0, z0), (r1, z0)), ((r1, z1), (r0, z1))):
            A, B, C, D = P(ra, a, za), P(ra, b, za), P(rb, b, zb), P(rb, a, zb)
            out += [(A, B, C), (A, C, D)]
    return np.array(out)


def _delik(G, ad, eks, duz, rect, kutu_lo, kutu_hi, rapor):
    for p in G.prims:
        if p.get("gizli") or p["name"] != ad: continue
        P = p["X"][p["T"]]; vis = G.gorunur(p)
        mm = vis & np.all(P.max(1) >= kutu_lo, 1) & np.all(P.min(1) <= kutu_hi, 1)
        if mm.any():
            on = np.zeros(len(P), bool)
            for d in duz: on |= np.all(np.abs(P[:, :, eks] - d) < 0.02, axis=1)
            mm &= on
        if not mm.any(): continue
        gr = {}
        for t in np.where(mm)[0]: gr.setdefault(G._etiketler(p, t), []).append(t)
        for et, tt in gr.items():
            Q = delik_ucgenler(P[np.array(tt)], eks, duz, *rect)
            mk = np.zeros(len(P), bool); mk[np.array(tt)] = True; G.sil(p, mk); G._ekle_dunya(p, Q, *et)
        rapor("delik %s %s" % (ad, rect), int(mm.sum()))


def calistir(G, rapor, Y, MEKL, KAT, SP):
    import p5, qr5
    E = KAT["ELEKTRIK"]; mk_pano = MEKL.index("Elektrik/Ana pano")
    # 1 . pano -> V1 kablolari: arka rakor -> dik kanal -> taban kanali -> V1
    for Q, r, t, y in p5.PYOL.values():
        ad = "ELK_ZINCIR__kablo_" + t
        et = _sil_comp(G, ad, lambda a, b, y=y: 2020 < a[1] < 2030 and abs(b[2] + 344) < 1 and a[1] <= y <= b[1], rapor, "eski havada pano->V1 kablosu y %d" % y)
        if et is None: raise SystemExit("pano kablosu bulunamadi %s %d" % (t, y))
        p, e = et; rapor("yeni %s pano arka -> dik kanal -> V1 (y %d)" % (ad, y), G._ekle_dunya(p, tup(Q, r, 16), *e))
    p = [q for q in G.prims if q["name"] == "ELK_ZINCIR__kanal" and not q.get("gizli")][0]
    P = p["X"][p["T"]]; c = P.mean(1); d = np.linalg.norm(c - np.array([3963, 1900, -826]), axis=1); d[~G.gorunur(p)] = 1e18
    G._ekle_dunya(p, kutu_ucgen((3930, 2030, -826), (3996, 2031.2, -786)), *G._etiketler(p, int(np.argmin(d)))); rapor("V1 ust kapak", 12)
    # 2 . yan rakorlar kalkar, yan duvar delikleri kapanir
    _sil_comp(G, "ELK_ANA_PANO_UF__rakor", lambda a, b: a[0] > 3500 and b[0] < 3530, rapor, "pano sol yan rakorlari")
    for p in G.prims:
        if p.get("gizli") or p["name"] != "ELK_ANA_PANO_UF__pano": continue
        P = p["X"][p["T"]]; vis = G.gorunur(p)
        m = vis & np.all(P.min(1) >= [3517.9, 1889.9, -222.6], 1) & np.all(P.max(1) <= [3519.6, 2152.1, -157.4], 1)
        if m.any():
            et = G._etiketler(p, int(np.where(m)[0][0])); G.sil(p, m)
            rapor("pano sol yan duvar delikli serit -> duz sac", G._ekle_dunya(p, kutu_ucgen((3518, 1890, -222.5), (3519.5, 2152, -157.5)), *et))
    # 3 . ana salter: ABB OT40F4 DIN rayinda + OHYS2AJ kapi kolu + OXP6X mil
    for ad in ("ELK_ANA_PANO_UF__salter__KAPAK_ANA_PANO", "ELK_ANA_PANO_UF__salter_sari__KAPAK_ANA_PANO", "ELK_ANA_PANO_UF__salter_kirmizi__KAPAK_ANA_PANO"):
        for p in G.prims:
            if p["name"] == ad and not p.get("gizli"): rapor("sil eski kapak salteri " + ad, G.sil(p, G.gorunur(p)))
    xc, yc = 3612.0, 2107.0
    Y.ekle("ELK_ANA_PANO_UF__salter", ("ME5_salter_gri", (0.55, 0.56, 0.58, 1.0), 0.2, 0.6), kutu_ucgen((xc - 24, yc - 28, -273.0), (xc + 24, yc + 28, -205.0)), E, mk_pano)
    Y.ekle("ELK_ANA_PANO_UF__salter_mil", ("ME5_mil", (0.75, 0.76, 0.78, 1.0), 0.9, 0.3), kutu_ucgen((xc - 3, yc - 3, -205.0), (xc + 3, yc + 3, -87.0)), E, mk_pano)
    Y.ekle("ELK_ANA_PANO_UF__salter_sari__KAPAK_ANA_PANO", ("ME4_salter_sari", (0.95, 0.75, 0.05, 1.0), 0.0, 0.5), kutu_ucgen((xc - 32.5, yc - 32.5, -87.0), (xc + 32.5, yc + 32.5, -80.0)), E, mk_pano)
    kol = np.concatenate([silindir((xc, yc, -80.0), (xc, yc, -66.0), 20.0, 32), kutu_ucgen((xc - 9, yc - 30, -66.0), (xc + 9, yc + 30, -39.0))])
    Y.ekle("ELK_ANA_PANO_UF__salter_kirmizi__KAPAK_ANA_PANO", ("ME4_salter_kirmizi", (0.80, 0.05, 0.05, 1.0), 0.0, 0.5), kol, E, mk_pano)
    for ad in ("ELK_ANA_PANO_UF__pano__KAPAK_ANA_PANO", "ELK_ANA_PANO_UF__conta__KAPAK_ANA_PANO"):
        for p in G.prims:
            if p["name"] != ad or p.get("gizli"): continue
            P = p["X"][p["T"]]; vis = G.gorunur(p)
            mm = vis & np.all(P.max(1) >= [xc - 12, yc - 12, -91], 1) & np.all(P.min(1) <= [xc + 12, yc + 12, -86], 1)
            nn = np.cross(P[:, 1] - P[:, 0], P[:, 2] - P[:, 0]); nn /= np.maximum(np.linalg.norm(nn, axis=1)[:, None], 1e-12); mm &= np.abs(nn[:, 2]) > 0.999
            if not mm.any(): continue
            duz = sorted(set(np.round(P[mm][:, 0, 2], 3).tolist())); gr = {}
            for t in np.where(mm)[0]: gr.setdefault(G._etiketler(p, t), []).append(t)
            for et, tt in gr.items():
                Q = P[np.array(tt)]
                for dz in duz: Q = delik_ucgenler(Q, 2, [dz], xc - 11.25, xc + 11.25, yc - 11.25, yc + 11.25)
                m2 = np.zeros(len(P), bool); m2[np.array(tt)] = True; G.sil(p, m2); G._ekle_dunya(p, Q, *et)
            rapor("kapak 22,5 kol deligi " + ad, int(mm.sum()))
    tapa = np.concatenate([silindir((3745, 2110, -89.0), (3745, 2110, -87.0), 6.4, 24), silindir((3745, 2110, -87.0), (3745, 2110, -85.5), 8.5, 24),
                           silindir((3745, 2110, -90.5), (3745, 2110, -89.0), 8.5, 24)])
    Y.ekle("ELK_ANA_PANO_UF__tapa__KAPAK_ANA_PANO", ("ME5_tapa_gri", (0.25, 0.25, 0.27, 1.0), 0.0, 0.7), tapa, E, mk_pano)
    rapor("eski 13 mm kapak deligine kor tapa", len(tapa))
    et = _sil_comp(G, "ELK_ZINCIR__kablo_guc", lambda a, b: a[0] < 3610 and b[0] > 3940 and b[2] > -145, rapor, "eski bina kablosu pano ici")
    p, e = et
    rapor("yeni bina kablosu pano ici", G._ekle_dunya(p, tup([(3940, 2146, -318.5), (3940, 2146, -300), (xc, 2146, -300), (xc, 2146, -245), (xc, 2137, -245)], 10.0, 16), *e))
    Y.ekle("ELK_ANA_PANO_UF__lastik_gecit", ("ME5_lastik", (0.08, 0.08, 0.08, 1.0), 0.0, 0.9), halka((xc, 2146), 10.3, 13.0, -284.0, -279.0), E, mk_pano)
    rapor("montaj plakasi gecisine lastik gecit", 1)
    # 4 . bosta kalan kompresor hortumu ucu
    et = _sil_comp(G, "HAVA_KOMPRESOR__hava_ana", lambda a, b: abs(a[2] + 770) < 1 and abs(b[2] + 432) < 1, rapor, "bosta hortum kolu")
    _sil_comp(G, "HAVA_KOMPRESOR__hava_ana", lambda a, b: abs(a[2] + 437) < 1 and b[1] > 1828, rapor, "bosta hortum ucu dirsegi")
    p, e = et; rapor("hortum koprusu z -770..-740", G._ekle_dunya(p, tup([(3549, 1809, -770), (3549, 1809, -740)], 5.0, 16), *e))
    _sil_comp(G, "ELK_K__celik", lambda a, b: a[0] > 4190 and b[0] < 4255 and a[1] > 1318 and b[1] < 1338 and a[2] > -125 and b[2] < -100, rapor, "bosa dusen K kelepce (eski #81 yolu)")
    # 5 . QR goz ust plakasi: dik kanal gecisleri
    for x0, x1, z0, z1 in qr5.PLAKA:
        _delik(G, "QR_GOVDE__qr_govde", 1, [1650.0, 1653.0], (x0, x1, z0, z1), np.array([x0 - 30, 1649, z0 - 30]), np.array([x1 + 30, 1654, z1 + 30]), rapor)
    # 6 . QR musteri paneli kablolari
    ors = {}
    for t, ad in (("veri", "ELK_QR_KABLO__kablo_sinyal"), ("guc", "ELK_QR_KABLO__kablo")):
        p = [q for q in G.prims if q["name"] == ad and not q.get("gizli")][0]
        c = [c for c in komps(G, p) if c[1][2] > 660][0]; ors[t] = (p, G._etiketler(p, int(c[0][0])))
    for Q, r, t in qr5.PANEL:
        p, e = ors[t]; rapor("yeni QR panel kablosu %s %s" % (t, Q[0]), G._ekle_dunya(p, tup(Q, r, 16), *e))
