# -*- coding: utf-8 -*-
"""B sac parçaları: açınım JSON'undan (h3_sac_v1 · acinim_B) düz levha ağı + büküm kareleri (morph).
Yerel çerçeve: açınım düzlemi (x, y), z = 0 alt yüz, z = t üst yüz. Büküm: baslangic (kök tarafı teğet) → bitis (flanş tarafı teğet),
yon 'yukari' → flanş +z tarafına döner (eksen z = t + R), 'asagi' → −z (eksen z = −R). Bölge uzunluğu = BA (nötr eksen boyu).
kare(f) : her büküm için açı oranı f[b] (0 düz … 1 tam) → yerel köşeler · donusum_3b ile dünyaya."""
import json, math, os
import numpy as np
import manifold3d as mf

ACN_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "acinim_TOPPING")
OFS = np.zeros(3)


def _yay(c, r, p0, p1, p2, n=12):
    a0 = math.atan2(p0[1] - c[1], p0[0] - c[0]); a2 = math.atan2(p2[1] - c[1], p2[0] - c[0]); a1 = math.atan2(p1[1] - c[1], p1[0] - c[0])
    def norm(x): return (x + 2 * math.pi) % (2 * math.pi)
    d = norm(a2 - a0); d1 = norm(a1 - a0)
    if d1 > d: d = d - 2 * math.pi            # ters yön
    return [(c[0] + r * math.cos(a0 + d * k / n), c[1] + r * math.sin(a0 + d * k / n)) for k in range(n + 1)]


def kontur(seg):
    pts = []
    for s in seg:
        if s['t'] == 'L': q = [tuple(s['p'][0]), tuple(s['p'][1])]
        elif s['t'] == 'A': q = _yay(s['c'], s['r'], *s['p'])
        elif s['t'] == 'C':
            return [(s['c'][0] + s['r'] * math.cos(2 * math.pi * k / 24), s['c'][1] + s['r'] * math.sin(2 * math.pi * k / 24)) for k in range(24)]
        for p in q:
            if not pts or abs(pts[-1][0] - p[0]) + abs(pts[-1][1] - p[1]) > 1e-6: pts.append(p)
    if len(pts) > 2 and abs(pts[0][0] - pts[-1][0]) + abs(pts[0][1] - pts[-1][1]) < 1e-6: pts.pop()
    return pts


class Sac:
    def __init__(self, ad, nb_dilim=6):
        self.ad = ad
        d = self.d = json.load(open(os.path.join(ACN_DIR, ad + '.json'), encoding='utf-8'))
        self.t = d['t']; self.R = d['R']
        self.M = np.array(d['donusum_3b'], float)
        polys = [kontur(d['dis_kontur'])] + [kontur(k) for k in d['ek_dis_konturlar']] + [kontur(k) for k in d['ic_konturlar']]
        cs = mf.CrossSection([np.array(p, float) for p in polys], mf.FillRule.EvenOdd)
        self.bukum = []
        for b in d['bukumler']:
            b0 = np.array(b['baslangic'], float); b1 = np.array(b['bitis'], float)
            u = b0[1] - b0[0]; u /= np.linalg.norm(u)
            n = (b1[0] - b0[0]); n = n - u * (n @ u); Lb = float(np.linalg.norm(n)); n /= Lb
            self.bukum.append(dict(no=b['no'], ad=b['ad'], aci=b['aci'], yon=1 if b['yon'] == 'yukari' else -1, R=b['R'], L0=b0[0], u=u, n=n, Lb=Lb))
        # eş doğrultulu bölünmüş bükümler (ör. raf ön bükümleri, kesiklerle ayrılmış): maske u aralığıyla sınırlanır
        for b in self.bukum:
            b['uara'] = None
            for a in self.bukum:
                if a is b: continue
                if abs(abs(a['n'] @ b['n']) - 1) < 1e-6 and abs((a['L0'] - b['L0']) @ b['n']) < 1e-3 and a['n'] @ b['n'] > 0:
                    u0 = (np.array(d['bukumler'][[x['no'] for x in self.bukum].index(b['no'])]['baslangic'], float) - b['L0']) @ b['u']
                    b['uara'] = (u0.min() - 0.5, u0.max() + 0.5)
        # derinlik (iç içe büküm: çocuğun başlangıcı ebeveynin flanşında)
        for b in self.bukum:
            b['ebeveyn'] = None
            for a in self.bukum:
                if a is b: continue
                if ((b['L0'] - a['L0']) @ a['n']) >= a['Lb'] - 1e-6: b['ebeveyn'] = a['no']
        # bölge dilimleri: her büküm bölgesi nb_dilim şeride bölünür (köşeler bükümle yay olur)
        parcalar = [cs]
        BIG = 1e5
        for b in self.bukum:
            yeni = []
            kes = [0.0] + [b['Lb'] * k / nb_dilim for k in range(1, nb_dilim)] + [b['Lb']]
            for p in parcalar:
                for i in range(len(kes) + 1):
                    lo = -BIG if i == 0 else kes[i - 1]; hi = BIG if i == len(kes) else kes[i]
                    # şerit: L0 + n·[lo, hi] · u boyunca sonsuz
                    c0 = b['L0'] + b['n'] * lo; c1 = b['L0'] + b['n'] * hi
                    q = np.array([c0 - b['u'] * BIG, c0 + b['u'] * BIG, c1 + b['u'] * BIG, c1 - b['u'] * BIG])
                    if np.cross(q[1] - q[0], q[2] - q[1]) < 0: q = q[::-1]
                    r = p ^ mf.CrossSection([q], mf.FillRule.EvenOdd)
                    if not r.is_empty() and r.area() > 1e-6: yeni.append(r)
            parcalar = yeni
        m = mf.Manifold.batch_boolean([pp.extrude(self.t) for pp in parcalar], mf.OpType.Add)
        me = m.to_mesh(); self.V0 = np.asarray(me.vert_properties)[:, :3].astype(float); self.F = np.asarray(me.tri_verts).astype(np.int64)
        self.levha = d['levha']

    def yerel(self, f):
        """f: büküm no → oran (0 düz, 1 tam) · çocuklar önce, ebeveynler sonra uygulanır (ebeveyn flanşı rijit döner)"""
        X = self.V0.copy()
        XY = self.V0[:, :2]
        sira = sorted(self.bukum, key=lambda b: -self._derin(b))
        for b in sira:
            fr = f.get(b['no'], 1.0)
            if fr <= 1e-9: continue
            th = math.radians(b['aci']) * fr
            d = (XY - b['L0']) @ b['n']
            n3 = np.array([b['n'][0], b['n'][1], 0.0]); z3 = np.array([0, 0, 1.0]) * b['yon']
            # eksen: L0 + z (yukari: t + R, asagi: −R) ; yerel (d, h): h = yön boyunca yükseklik
            ax0 = np.array([b['L0'][0], b['L0'][1], 0.0]) + (np.array([0, 0, self.t + b['R']]) if b['yon'] > 0 else np.array([0, 0, -b['R']]))
            bol = (d > 1e-9) & (d < b['Lb'] - 1e-9); fl = d >= b['Lb'] - 1e-9
            if b['uara'] is not None:
                uk = (XY - b['L0']) @ b['u']; mu = (uk >= b['uara'][0]) & (uk <= b['uara'][1]); bol &= mu; fl &= mu
            # bölge: φ = th · d / Lb ; r = (t + R − z) (yukari) ya da (R + z) (asagi)
            for msk, isfl in ((bol, False), (fl, True)):
                if not msk.any(): continue
                P = X[msk]
                if not isfl:
                    zz = P[:, 2]; r = (self.t + b['R'] - zz) if b['yon'] > 0 else (b['R'] + zz)
                    ph = th * d[msk] / b['Lb']
                    # nokta = eksen − r·z3 döndürülmüş: eksen + r(sinφ n − cosφ z3) ; u boyunca bileşen korunur
                    ucomp = (P[:, :2] - b['L0']) @ b['u']
                    base = ax0 + np.outer(ucomp, np.array([b['u'][0], b['u'][1], 0.0]))
                    X[msk] = base + r[:, None] * (np.sin(ph)[:, None] * n3 - np.cos(ph)[:, None] * z3)
                else:
                    # rijit: flanş noktaları eksen etrafında th döner + bölge boyu (Lb) ile yay boyu farkı
                    # düz durumdaki karşılığı: bölge sonundaki nokta + (d − Lb) n
                    # dönüş matrisi (eksen u): n → cos n + sin z3 ; z3 → −sin n + cos z3
                    rel = P - ax0
                    a_n = rel @ n3; a_z = rel @ z3; a_u = rel @ np.array([b['u'][0], b['u'][1], 0.0])
                    # düzde: a_n = d (bölge başına göre), a_z = −r ; bölgeyi 'çıkar': a_n' = a_n − Lb
                    an2 = a_n - b['Lb']
                    # bükülmüş: eksen + r(sinθ n − cosθ z3) + an2 (cosθ n + sinθ z3) ; r = −a_z
                    r = -a_z
                    X[msk] = ax0 + np.outer(a_u, np.array([b['u'][0], b['u'][1], 0.0])) + \
                        (r * np.sin(th) + an2 * np.cos(th))[:, None] * n3 + (-r * np.cos(th) + an2 * np.sin(th))[:, None] * z3
        return X

    def _derin(self, b):
        k = 0; e = b['ebeveyn']
        while e is not None:
            k += 1; e = next(a for a in self.bukum if a['no'] == e)['ebeveyn']
        return k

    def dunya(self, X):
        return X @ self.M[:3, :3].T + self.M[:3, 3] + OFS        # A yereli → dünya (x + 736)


if __name__ == '__main__':
    import sys, glob
    sys.stdout.reconfigure(encoding='utf-8')
    ent = json.load(open(os.path.join(ACN_DIR, '..', '..', 'adim8', 'is_tam', 'hat3_v9e_ent.json'), encoding='utf-8'))['parca']
    for f in sorted(glob.glob(os.path.join(ACN_DIR, '*.json'))):
        ad = os.path.basename(f)[:-5]
        s = Sac(ad); X = s.dunya(s.yerel({}))
        kb = np.array(ent[ad]['kutu']); lo, hi = X.min(0), X.max(0)
        fark = max(np.abs(lo - kb[[0, 2, 4]]).max(), np.abs(hi - kb[[1, 3, 5]]).max())
        print('%-26s nb %d  V %6d  fark %.4f' % (ad, len(s.bukum), len(s.V0), fark))
