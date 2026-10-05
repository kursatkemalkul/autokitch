# -*- coding: utf-8 -*-
"""ZİNCİR ADIMI ÖNERİSİ · E (KUTU KATLAMA) MEKANİZMA BAĞLANTI AÇIKLARI (4 Eki 2026 · Claude · yerel) — hat3_v9s (zincir 00–51) sonrası
Kullanım: python zincir_E_tamamla.py giris.glb cikis.glb [rapor.json]
Düğüm adı tabanlı: yalnız 'E_GOVDE__celik' düğümünün tek primitifine üçgen EKLER (mevcut üçgen sırası korunur → adım-35 ent indisleri değişmez;
mek / kat aralığı komşu saplamanın değeriyle). Diğer düğümlere dokunmaz. Okuma: E/* mekanizma bileşenleri (tam düğüm dönüşümüyle) yalnız denetim için.

Açık (adım 35 entegrasyon notu §4 + DURUM 04:45): "mekanizma FHP somun / pul modellenmedi". Mekanizmayı gövdeye tutan 34 FHP saplamanın
(arayuz_mek_*) ve 2 J3 burcunun karşı tarafında pul + somun YOK. Bu betik her saplamayı ölçer (eksen boyunca ışın: sac iç yüzü → karşı parçanın
dayanma yüzü → saplama ucu) ve YALNIZ sığan + diş boyu yeten yerlere DIN 125-1 M5 pul (5,3 / 10 × 1) + ISO 10511 M5 fiberli somun (SW 8 × 5)
ekler. Sığmayan / karşı parçası olmayan / kör delikte biten saplamalar RAPORLANIR, değiştirilmez (Kemal / üreteç kararı).
Eklenen her eleman: tüm E bileşenleriyle hacim kesişimi 0 (nokta örneklemesi 0,4 mm) olmadan eklenmez."""
import json, struct, sys, os, pickle
import numpy as np
import trimesh
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'a3')); sys.path.insert(0, os.path.join(HERE, '..', 'cekmece'))
from zincir_A_tamamla import GLB, duz_kati
from glb import bilesen

PUL = (5.3, 10.0, 1.0)            # DIN 125-1 M5: d1 5,3 · d2 10 · h 1
SOMUN = (5.0, 8.0, 5.0)           # ISO 10511 M5: d 5 (diş) · s 8 · m 5
TOL = 0.05


def silindir_halka(c, e, s0, s1, ri, ro, n=32, alti=False):
    import manifold3d as mf
    h = s1 - s0
    if alti:
        R = ro / np.cos(np.pi / 6)
        m = mf.Manifold.cylinder(h, R, R, 6) - mf.Manifold.cylinder(h + 2, ri, ri, n).translate([0, 0, -1])
    else:
        m = mf.Manifold.cylinder(h, ro, ro, n) - mf.Manifold.cylinder(h + 2, ri, ri, n).translate([0, 0, -1])
    me = m.to_mesh(); V = np.asarray(me.vert_properties, float)[:, :3]; F = np.asarray(me.tri_verts, np.int64)
    e = np.asarray(e, float); a = np.array([1.0, 0, 0]) if abs(e[0]) < 0.9 else np.array([0, 1.0, 0])
    u = np.cross(e, a); u /= np.linalg.norm(u); v = np.cross(e, u)
    W = c + np.outer(V[:, 0], u) + np.outer(V[:, 1], v) + np.outer(V[:, 2] + s0, e)
    return W, F


def main(gi, go, rap=None):
    g = GLB(gi)
    E = g.dugum('E_GOVDE__celik')
    # bileşenler: E düğümü + mekanizmalar (okuma)
    sys.path.insert(0, os.path.join(HERE, '..', 'cekmece'))
    from glb import G
    gg = G(gi)
    EM = [i for i, m in enumerate(gg.MEK) if m['kod'].startswith('E/')]
    KOMP = []
    for ni, nd in enumerate(gg.J['nodes']):
        if 'mesh' not in nd or ni not in gg.W: continue
        if abs(np.linalg.det(gg.W[ni][:3, :3])) < 1e-9: continue
        for X, T, mek, mat, ex in gg.tris(ni):
            sel = np.isin(mek, EM)
            if not sel.any(): continue
            Tm = T[sel]; cl = bilesen(X, Tm)
            for c in np.unique(cl):
                Tc = Tm[cl == c]; u, inv = np.unique(Tc.reshape(-1), return_inverse=True)
                KOMP.append(dict(dug=nd['name'], V=X[u], F=inv.reshape(-1, 3), lo=X[u].min(0), hi=X[u].max(0)))
    TM = {}

    def tm(i):
        if i not in TM: TM[i] = trimesh.Trimesh(KOMP[i]['V'], KOMP[i]['F'], process=False)
        return TM[i]

    def isin(p0, e, L=60.0):
        out = []
        q0 = np.minimum(p0, p0 + e * L) - 0.5; q1 = np.maximum(p0, p0 + e * L) + 0.5
        for i, o in enumerate(KOMP):
            if np.any(o['lo'] > q1) or np.any(o['hi'] < q0): continue
            loc, _, _ = tm(i).ray.intersects_location([p0], [e])
            for l in loc:
                d = float((l - p0) @ e)
                if 0 <= d <= L: out.append((d, i))
        return sorted(out)

    # saplamalar: E_GOVDE__celik bileşenleri arasından ent adıyla
    ENT = json.load(open(os.path.join(HERE, '..', 'adim8', 'is_tam', 'hat3_v9c_ent.json'), encoding='utf-8'))['parca']
    SAP = {a: v for a, v in ENT.items() if a.startswith(('arayuz_mek_', 'arayuz_j3_'))}
    rapor = dict(eklenen=[], eklenmedi=[])
    CEL = [i for i, o in enumerate(KOMP) if o['dug'] == 'E_GOVDE__celik']
    for a, v in sorted(SAP.items()):
        lo = np.array(v['kutu'][0::2]); hi = np.array(v['kutu'][1::2])
        c_ = [i for i in CEL if np.all(np.abs(KOMP[i]['lo'] - lo) < 0.35) and np.all(np.abs(KOMP[i]['hi'] - hi) < 0.35)]
        if len(c_) != 1: rapor['eklenmedi'].append(dict(ad=a, neden='modelde yok (adım 8 / üreteç düzeltmesiyle çıkarılmış)')); continue
        V = KOMP[c_[0]]['V']; ext = V.max(0) - V.min(0); ax = int(np.argmax(ext)); oth = [k for k in range(3) if k != ax]
        s = V[:, ax]; ml = s < s.min() + 0.6; mh = s > s.max() - 0.6
        e = np.zeros(3); e[ax] = 1.0 if np.ptp(V[ml][:, oth], 0).max() > np.ptp(V[mh][:, oth], 0).max() else -1.0
        cc = (V.min(0) + V.max(0)) / 2; bas = cc.copy(); bas[ax] = s.min() if e[ax] > 0 else s.max()
        Ls = float(ext[ax]); t_sac = 3.0 if a.startswith('arayuz_mek_taban') else 1.5
        # karşı parça yığını: 4 yanal ışın (r 3,3) — sac iç yüzünden itibaren bitişik dolu aralıklar
        yigin = []
        for k in oth:
            for sg in (1, -1):
                off = np.zeros(3); off[k] = 3.3 * sg; p0 = bas + off + e * (t_sac - 0.02)
                h = [(d + t_sac - 0.02, i) for d, i in isin(p0, e) if not KOMP[i]['dug'].startswith('E_GOVDE')]
                ara = []
                for i in set(i for _, i in h):
                    dd = [d for d, j in h if j == i]
                    for q in range(0, len(dd) - 1, 2): ara.append((dd[q], dd[q + 1], i))
                son = t_sac; dolu = []; deg = True
                while deg:
                    deg = False
                    for d0, d1, i in ara:
                        if d0 <= son + 0.06 and d1 > son + 1e-6: son = d1; dolu.append(KOMP[i]['dug']); deg = True
                yigin.append((round(son, 2), dolu))
        oturma = max(y[0] for y in yigin); karsi = sorted(set(d for y in yigin for d in y[1]))
        eks = [(round(d + t_sac - 0.02, 2), KOMP[i]['dug']) for d, i in isin(bas + e * (t_sac - 0.02), e) if not KOMP[i]['dug'].startswith('E_GOVDE')]
        kayit = dict(ad=a, boy=Ls, eksen=e.astype(int).tolist(), bas=np.round(bas, 2).tolist(), karsi=karsi, oturma_mm=oturma,
                     eksen_isin=eks[:3], yanal=[y[0] for y in yigin])
        temas = any(abs(d + t_sac - 0.02 - t_sac) < 0.08 for k in oth for sg in (1, -1) for d, i in isin(bas + np.eye(3)[k] * 3.3 * sg + e * (t_sac - 0.02), e)[:1] if not KOMP[i]['dug'].startswith('E_GOVDE'))
        if (not karsi or oturma <= t_sac + 0.05) and temas and eks and eks[0][0] <= Ls + 0.06:
            kayit['neden'] = 'kör delik: karşı parça (%s) sac yüzüne dayalı dolu blok, saplama %.1f mm derinlikte kör delikte biter — pul + somun yeri yok' % (eks[0][1], eks[0][0])
            rapor['eklenmedi'].append(kayit); continue
        if not karsi or oturma <= t_sac + 0.05:
            kayit['neden'] = 'karşı parça yok: saplama sac iç yüzünden %.1f mm boşluğa çıkıyor (eksen ışını ilk %s)' % (Ls - t_sac, eks[0] if eks else '-')
            rapor['eklenmedi'].append(kayit); continue
        if eks and eks[0][0] < oturma + PUL[2] + SOMUN[2] - 0.05:
            kayit['neden'] = 'kör delik: karşı parça saplama ekseninde dolu (%.2f mm) — pul + somun yeri yok' % eks[0][0]
            rapor['eklenmedi'].append(kayit); continue
        tasma = Ls - (oturma + PUL[2] + SOMUN[2])
        if tasma < -0.01:
            kayit['neden'] = 'saplama kısa: somun %.1f mm dişe oturur (gereken %.1f) — uç taşması %.2f' % (SOMUN[2] + tasma, SOMUN[2], tasma)
            rapor['eklenmedi'].append(kayit); continue
        Vp, Fp = silindir_halka(bas, e, oturma + 0.0, oturma + PUL[2], PUL[0] / 2, PUL[1] / 2)
        Vn, Fn = silindir_halka(bas, e, oturma + PUL[2], oturma + PUL[2] + SOMUN[2], SOMUN[0] / 2, SOMUN[1] / 2, alti=True)
        # hacim denetimi: pul + somun içine nokta örnekle → başka bileşen içinde mi
        ok = True; carp = []
        for (VV, FF, nm) in ((Vp, Fp, 'pul'), (Vn, Fn, 'somun')):
            mm = trimesh.Trimesh(VV, FF, process=False)
            pts = trimesh.sample.volume_mesh(mm, 4000) if mm.is_watertight else VV
            pts = pts[np.linalg.norm(np.cross(pts - bas, e), axis=1) > PUL[0] / 2 + 0.05]
            q0 = pts.min(0); q1 = pts.max(0)
            for i, o in enumerate(KOMP):
                if i == c_[0] or np.any(o['lo'] > q1) or np.any(o['hi'] < q0): continue
                if not tm(i).is_watertight: continue
                ins = tm(i).contains(pts)
                if ins.sum() > 2: ok = False; carp.append((nm, o['dug'], int(ins.sum())))
        if not ok:
            kayit['neden'] = 'pul / somun karşı tarafta başka parçaya çarpıyor: %s' % carp[:3]; rapor['eklenmedi'].append(kayit); continue
        E.ucgen_ekle(*duz_kati(Vp, Fp)); E.ucgen_ekle(*duz_kati(Vn, Fn))
        kayit.update(pul=[round(oturma, 2), round(oturma + PUL[2], 2)], somun=[round(oturma + PUL[2], 2), round(oturma + PUL[2] + SOMUN[2], 2)], uc_tasma_mm=round(tasma, 2),
                     pul_kutu=np.round(np.r_[Vp.min(0), Vp.max(0)], 2).tolist(), somun_kutu=np.round(np.r_[Vn.min(0), Vn.max(0)], 2).tolist())
        rapor['eklenen'].append(kayit)
    n1 = E.kapat(ornek_nokta=tuple(rapor['eklenen'][0]['bas']) if rapor['eklenen'] else None)
    n = g.yaz(go)
    for k in rapor['eklenen']: print('EKLENDİ  %-26s karşı %s · oturma %.2f · uç taşması %.2f' % (k['ad'], k['karsi'], k['oturma_mm'], k['uc_tasma_mm']))
    for k in rapor['eklenmedi']: print('AÇIK     %-26s %s' % (k['ad'], k.get('neden')))
    print('yazıldı %s · E_GOVDE__celik +%d üçgen · %.1f MB · eklenen %d · açık %d' % (go, n1, n / 1e6, len(rapor['eklenen']), len(rapor['eklenmedi'])))
    if rap: json.dump(rapor, open(rap, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    main(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None)
