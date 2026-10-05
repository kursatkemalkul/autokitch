# -*- coding: utf-8 -*-
"""tek çekmece (CEK_K2_lahm_3) parçalarını + silik çevreyi hat3_v9j.glb'den çıkarır → parca.pkl (metre)"""
import sys, os, pickle, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, '..', 'cekmece')); os.chdir(HERE)
sys.stdout.reconfigure(encoding='utf-8')
from glb import G, bilesen
g = G('hat3_v9l.glb')
CK = 'CEK_K2_lahm_3__'
P = {}


def ekle(ad, tri, m, tur, ac):
    V = tri.reshape(-1, 3)
    u, inv = np.unique(np.round(V, 4), axis=0, return_inverse=True)
    P[ad] = dict(V=u / 1000.0, F=inv.reshape(-1, 3), m=m, tur=tur, ac=ac)


_C = {}


def comps(nm):
    if nm in _C: return _C[nm]
    ni = g.byname[nm]; out = []
    for k, (X, T, mek, mat, ex) in enumerate(g.tris(ni)):
        Pm = X[T]; ar = np.linalg.norm(np.cross(Pm[:, 1] - Pm[:, 0], Pm[:, 2] - Pm[:, 0]), axis=1)
        T = T[ar > 1e-9]; cl = bilesen(X, T); Pm = X[T]
        for c in np.unique(cl):
            m = cl == c; Q = Pm[m].reshape(-1, 3)
            out.append((Q.min(0), Q.max(0), Pm[m]))
    _C[nm] = out; return out


def sec(nm, lo, tol=0.6):
    r = [c for c in comps(nm) if np.all(np.abs(c[0] - np.array(lo)) < tol)]
    assert len(r) == 1, (nm, lo, len(r)); return r[0][2]


# ---- çekmece ünitesi
ekle('sabit_ray_sol', sec(CK + 'celik', [1453.5, 420.5, -677]), 'mekanizma', 'ray', 'sabit ray (sol)')
ekle('sabit_ray_sag', sec(CK + 'celik', [2065.0, 420.5, -677]), 'mekanizma', 'ray', 'sabit ray (sağ)')
ekle('ara_ray_sol', sec(CK + 'celik__CEKMECE_ARA', [1455.2, 422.2, -675]), 'mekanizma', 'ray', 'ara ray (sol)')
ekle('ara_ray_sag', sec(CK + 'celik__CEKMECE_ARA', [2063.0, 422.2, -675]), 'mekanizma', 'ray', 'ara ray (sağ)')
ekle('kizak_sol', sec(CK + 'celik__CEKMECE', [1456.7, 425.5, -673]), 'mekanizma', 'ray', 'kızak (sol)')
ekle('kizak_sag', sec(CK + 'celik__CEKMECE', [2060.8, 425.5, -673]), 'mekanizma', 'ray', 'kızak (sağ)')
ekle('kizak_lamasi_sol', sec(CK + 'celik__CEKMECE', [1466.2, 420.5, -597]), 'sac', 'sac', 'kızak bağlantı laması (sol)')
ekle('kizak_lamasi_sag', sec(CK + 'celik__CEKMECE', [2043.5, 420.5, -597]), 'sac', 'sac', 'kızak bağlantı laması (sağ)')
# (v3: cek3geo) ekle('kayis_lamasi', sec(CK + 'celik__CEKMECE', [1470.5, 457.9, -751]), 'sac', 'sac', 'kayış kelepçe + mıknatıs laması')
# (v3: cek3geo) ekle('miknatis', sec(CK + 'plastik__CEKMECE', [1470.5, 466.5, -751]), 'sensor', 'mek', 'mıknatıs yuvası')
ekle('on_braket_sol', sec(CK + 'celik__CEKMECE', [1483.5, 428.5, 22]), 'sac', 'sac', 'ön kapak braketi (sol)')
ekle('on_braket_sag', sec(CK + 'celik__CEKMECE', [2028.5, 428.5, 22]), 'sac', 'sac', 'ön kapak braketi (sağ)')
ekle('cekmece_govdesi', sec(CK + 'sac__CEKMECE', [1483.5, 421.5, -597]), 'sac', 'sac', 'çekmece gövdesi (sac tava)')
ekle('silikon_tepsi', sec(CK + 'silikon__CEKMECE', [1498.5, 423.5, -583]), 'tepsi', 'mek', 'silikon tepsi')
ekle('on_kapak', sec(CK + 'on_seffaf__CEKMECE', [1437.5, 401.5, 39]), 'kapak_s', 'kapak', 'ön kapak (şeffaf)')
ekle('on_panel', sec(CK + 'on_seffaf__CEKMECE', [1439.0, 402.0, 24]), 'kapak_s', 'kapak', 'ön panel')
ekle('arka_kasnak', sec(CK + 'aluminyum', [1469.0, 430.0, -785.9]), 'alu', 'mek', 'GT3 motor kasnağı')
ekle('avara_kasnagi', sec(CK + 'aluminyum', [1470.5, 430.0, -17.9]), 'alu', 'mek', 'GT3 avara kasnağı')
# (v3: cek3geo) ekle('motor_braketi', sec(CK + 'celik', [1481.0, 424.5, -790]), 'sac', 'sac', 'motor braketi')
ekle('motor_flansi', sec(CK + 'celik', [1482.0, 435.8, -779.9]), 'mekanizma', 'mek', 'motor flanşı')
# (v3: cek3geo) ekle('sensor_plakasi', sec(CK + 'celik', [1453.9, 463.6, -790]), 'sac', 'sac', 'sensör laması arka plakası')
ekle('avara_braketi', sec(CK + 'celik', [1454.5, 438.5, -756]), 'sac', 'sac', 'avara braketi + sensör laması')
ekle('kayis', sec(CK + 'koyu', [1471.5, 431.3, -783.8]), 'koyu', 'mek', 'GT3 kayış')
ekle('motor', np.concatenate([sec(CK + 'motor', [1484.0, 429.0, -786.9]), sec(CK + 'celik', [1467.0, 442.6, -773]), sec(CK + 'plastik', [1599.5, 431.0, -784.9]), sec(CK + 'koyu', [1619.5, 438.7, -776.9])]), 'motor', 'mek', 'step motor (mil + arka kapak + kablo rakoru)')
# (v3: cek3geo) ekle('reed_arka', sec(CK + 'plastik', [1463.5, 466.5, -751]), 'sensor', 'mek', 'reed sensör (kapalı konum)')
# (v3: cek3geo) ekle('reed_on', sec(CK + 'plastik', [1463.5, 466.5, -51]), 'sensor', 'mek', 'reed sensör (açık konum)')
# vidalar (sabit ray → bölme PEM'i)
for s, x in (('sol', 1450.5), ('sag', 2070.5)):
    for k, z in enumerate((-585, -335, -50)):
        ekle('vida_%s_%d' % (s, k + 1), sec('B_KASA__paslanmaz', [x, 438.3, z]), 'baglanti', 'baglanti', 'M5 × 10 havşa başlı vida')
# kablolar
ekle('kablo_sensor', sec('ELK_DOLAP__kablo_sinyal', [1456.7, 474.0, -779]), 'bilgi', 'kablo', 'reed sensör kabloları')
ekle('kablo_motor', sec('ELK_DOLAP__kablo_sinyal', [1464.7, 474.0, -773]), 'bilgi', 'kablo', 'motor kablosu')

# ---- silik çevre (bölmenin gövdesi) — kutuya kırpılmış
LO = np.array([1405., 392., -800.]); HI = np.array([2120., 522., 90.])


def kirp(tri):
    out = []
    tl = tri.min(1); th = tri.max(1)
    sel = np.all(th >= LO, 1) & np.all(tl <= HI, 1)
    for t in tri[sel]:
        poly = [p for p in t]
        for ax in range(3):
            for s, lim in ((1, LO[ax]), (-1, HI[ax])):
                if not poly: break
                new = []
                for i in range(len(poly)):
                    a = poly[i]; b = poly[(i + 1) % len(poly)]
                    da = s * (a[ax] - lim); db = s * (b[ax] - lim)
                    if da >= 0: new.append(a)
                    if (da >= 0) != (db >= 0): new.append(a + (b - a) * (da / (da - db)))
                poly = new
        for i in range(1, len(poly) - 1): out.append([poly[0], poly[i], poly[i + 1]])
    out = np.array(out)
    if len(out):
        ar = np.linalg.norm(np.cross(out[:, 1] - out[:, 0], out[:, 2] - out[:, 0]), axis=1); out = out[ar > 1e-6]
    return out


cev = []
for nm in ['B_KASA__sac', 'B_KASA__pu', 'B_KASA__on_cerceve', 'B_MODULER__paslanmaz', 'B_SOGUTMA__aluminyum', 'B_SOGUTMA__bakir',
           'B_SOGUTMA__motor', 'B_SOGUTMA__sac', 'B_KABLO__kanal', 'ELK_IC__kanal']:
    ni = g.byname[nm]
    for X, T, mek, mat, ex in g.tris(ni):
        t = kirp(X[T])
        if len(t): cev.append((nm, t))
for x in (1451.3, 2073.7):
    for z in (-584.4, -334.4, -49.4):
        cev.append(('PEM', sec('B_KASA__paslanmaz', [x, 438.9, z])))
for x in (1449.5, 2074.7):
    for z in (-585.2, -335.2, -50.2):
        cev.append(('kopuk_kapagi', sec('B_KASA__conta', [x, 438.1, z])))
for y in (436.0, 457.5):
    cev.append(('PEM', sec('B_KASA__paslanmaz', [1495.55, y - 4.45, -792.2], 0.4)))
    cev.append(('kopuk_kapagi', sec('B_KASA__conta', [1494.75, y - 5.25, -794.3], 0.4)))
AD = {'B_KASA__sac': 'cevre_sac', 'B_KASA__pu': 'cevre_pu', 'B_KASA__on_cerceve': 'cevre_on_cerceve', 'B_MODULER__paslanmaz': 'cevre_dikme',
      'ELK_IC__kanal': 'cevre_kanal', 'B_KABLO__kanal': 'cevre_kanal', 'PEM': 'cevre_pem', 'kopuk_kapagi': 'cevre_kopuk_kapagi'}
grup = {}
for nm, t in cev: grup.setdefault(AD.get(nm, 'cevre_sogutma'), []).append(t)
for k, L in grup.items(): ekle(k, np.concatenate(L), 'silik', 'cevre', k)
for a in P: print('%-20s %6d üçgen  lo %s  hi %s' % (a, len(P[a]['F']), np.round(P[a]['V'].min(0) * 1000, 1), np.round(P[a]['V'].max(0) * 1000, 1)))
pickle.dump(P, open('parca3.pkl', 'wb'))
