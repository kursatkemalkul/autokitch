# -*- coding: utf-8 -*-
"""ÇEKMECE DÜZELTMESİ v3 — ortak geometri (B · CEK_K2_lahm_3 dünya mm). Hem ana model adım 44 (21 çekmeceye ötelenerek) hem montaj animasyonu v3 bunu kullanır.
Ötelenme: 'L' = sol sabit rayın alt köşesine göre (R0 = 1453.5, 420.5, -677), 'R' = sağ sabit raya göre (Rr0 = 2065.0, 420.5, -677)."""
import os, sys, math
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, '..', 'cekmece'))
import v2geo as G
import manifold3d as mf

R0 = np.array([1453.5, 420.5, -677.0]); RR0 = np.array([2065.0, 420.5, -677.0])
K = G.kutu
YC, ZC = 446.75, -769.0                                  # motor ekseni
M3PCD = [(YC + 15.5 * math.cos(math.radians(a)), ZC + 15.5 * math.sin(math.radians(a))) for a in (45, 135, 225, 315)]
KX_K = (1469.0 + 1480.0) / 2.0                          # motor kasnağı göbek x
AY, AZ = 446.5, -1.0                                     # avara ekseni (y, z) = kasnak deliği merkezi (r 3,0)

# standart eleman tabloları (ek)
PEM_M3 = dict(ad='PEM CLS-M3-2 (AISI 303, 2 mm sac)', delik=4.22, E=4.8, govde=2.0)     # sacla aynı yüzde (flush) — diş boyu = sac 2,0
DIN6799_5 = dict(ad='DIN 6799 RS 5 E segman (mil Ø6–8, yuva Ø5)', yuva=5.0, dis=11.0, s=0.7, agiz=4.7)

def yarik(p, eksen, uz_yon, cap, boy, t):
    """çapraz değil, tek yönlü yarık (cross-slotted gövde deliği yaklaşık): eksen boyunca t derin, uz_yon boyunca 'boy' uzun"""
    p = np.asarray(p, float); u = np.asarray(uz_yon, float); a = np.asarray(eksen, float)
    c1 = G.silindir(p - u * (boy - cap) / 2 - a * 0.5, a, cap / 2, t + 1.0, 24)
    c2 = G.silindir(p + u * (boy - cap) / 2 - a * 0.5, a, cap / 2, t + 1.0, 24)
    return mf.Manifold.batch_hull([c1, c2])


def pem_m3(p, a):
    """PEM CLS-M3-2: p = sacın vida tarafı yüzü merkezi, a = sacın içine doğru · gövde sacın içinde (flush), iç diş Ø3 (nominal)"""
    p = np.asarray(p, float); a = np.asarray(a, float)
    return G.silindir(p, a, PEM_M3['delik'] / 2 - 0.01, PEM_M3['govde'], 32) - G.silindir(p - a * 0.1, a, 1.5, PEM_M3['govde'] + 0.2, 24)


def e_segman(x0, y, z):
    """DIN 6799 RS 5: x0 = segmanın pulley tarafı yüzü, eksen +x, ağız −y yönünde (radyal takılır, yukarıdan aşağı)"""
    d = DIN6799_5
    r = G.silindir((x0, y, z), (1, 0, 0), d['dis'] / 2, d['s'], 40) - G.silindir((x0 - 0.1, y, z), (1, 0, 0), d['yuva'] / 2, d['s'] + 0.2, 32)
    return r - K((x0 - 0.1, y - d['dis'], z - d['agiz'] / 2), (x0 + d['s'] + 0.1, y - 1.2, z + d['agiz'] / 2))


# ============================================================ A1 · kayış çenesi ayrı blok + kol tablası + mıknatıs kulağı
JX = 1488.0; JZ = (-743.0, -729.0)                       # çene cıvataları (eksen −y)
MX0, MX1 = 1476.5, 1482.85                               # mıknatıs (57135) x
MY0, MY1 = 466.71, 485.76
MZ0, MZ1 = -751.0, -722.43
MYC = (MY0 + MY1) / 2; MZC = (MZ0 + MZ1) / 2
DELIK_ARA = 19.05                                        # 57135 / 59135 montaj deliği aralığı (gövde boyu 28,57 boyunca) — VARSAYIM, datasheet teyidi
MZH = (MZC - DELIK_ARA / 2, MZC + DELIK_ARA / 2)
KUL_X0, KUL_X1 = 1482.85, 1484.85                        # mıknatıs kulağı 2 mm


def yd(x, z, t, y0):          # dikey (−y) delik
    return G.silindir((x, y0 + 0.5, z), (0, -1, 0), 1.7, t + 1.0, 24)


def geo_a1():
    D = {}
    D['kol'] = K((1480.5, 457.95, -721.0), (1483.5, 464.21, -567.0))
    D['tabla'] = G.fark(K((1474.0, 464.21, -751.0), (1491.5, 466.71, -711.0)), [yd(JX, z, 2.5, 466.71) for z in JZ])
    D['kulak'] = G.fark(K((KUL_X0, MY0, MZ0), (KUL_X1, MY1, MZ1)), [G.silindir((KUL_X0 - 0.5, MYC, z), (1, 0, 0), PEM_M3['delik'] / 2, 3.0, 32) for z in MZH])
    D['cene_alt'] = G.fark(K((1470.5, 457.95, -751.0), (1491.5, 460.45, -721.0)) + K((1477.5, 460.45, -751.0), (1491.5, 461.65, -721.0)),
                           [yd(JX, z, 4.0, 461.65) for z in JZ])
    D['cene_ust'] = G.fark(K((1470.5, 461.71, -751.0), (1491.5, 464.21, -721.0)), [yd(JX, z, 2.5, 464.21) for z in JZ])
    for i, z in enumerate(JZ):
        D['vida_cene_%d' % (i + 1)] = G.iso7380((JX, 466.71, z), (0, -1, 0), 'M3', 12.0)
        D['somun_cene_%d' % (i + 1)] = G.somun((JX, 457.95, z), (0, -1, 0), 'M3')
    D['miknatis'] = G.fark(K((MX0, MY0, MZ0), (MX1, MY1, MZ1)), [yarik((MX0, MYC, z), (1, 0, 0), (0, 0, 1), 3.18, 7.82, 6.35) for z in MZH])
    for i, z in enumerate(MZH):
        D['pem_kulak_%d' % (i + 1)] = pem_m3((KUL_X0, MYC, z), (1, 0, 0))
        D['vida_miknatis_%d' % (i + 1)] = G.iso7380((MX0, MYC, z), (1, 0, 0), 'M3', 8.0)   # M3 × 10 ucu çene cıvatasının yolunu kesiyor
    return D


# ============================================================ reed sensörler (59135) + reed plakaları (A3 ile birlikte)
RX0, RX1 = 1465.55, 1471.9
RY0, RY1 = 466.5, 485.55
RZ = {'arka': (-751.0, -722.43), 'on': (-51.0, -22.43)}
RPX0, RPX1 = 1463.55, 1465.55                            # reed plakası 2 mm (düz), lamaya punta


def geo_reed():
    D = {}
    yc = (RY0 + RY1) / 2
    for k, (z0, z1) in RZ.items():
        zc = (z0 + z1) / 2; zh = (zc - DELIK_ARA / 2, zc + DELIK_ARA / 2)
        D['reed_' + k] = G.fark(K((RX0, RY0, z0), (RX1, RY1, z1)), [yarik((RX1, yc, z), (-1, 0, 0), (0, 0, 1), 3.18, 7.82, 6.35) for z in zh])
        D['reed_plaka_' + k] = G.fark(K((RPX0, RY0, z0), (RPX1, RY1, z1)), [G.silindir((RPX1 + 0.5, yc, z), (-1, 0, 0), PEM_M3['delik'] / 2, 3.0, 32) for z in zh])
        for i, z in enumerate(zh):
            D['pem_reed_%s_%d' % (k, i + 1)] = pem_m3((RPX1, yc, z), (-1, 0, 0))
            D['vida_reed_%s_%d' % (k, i + 1)] = G.iso7380((RX1, yc, z), (-1, 0, 0), 'M3', 8.0)
    return D


# ============================================================ avara mili +1 mm (E segman yuvası) + segman
MIL_X0, MIL_X1, MIL_X1_YENI = 1469.2, 1481.0, 1482.0
SEG_X = 1480.0


def geo_avara():
    D = {}
    D['avara_mili'] = G.silindir((MIL_X0, AY, AZ), (1, 0, 0), 2.98, MIL_X1_YENI - MIL_X0, 32) - \
        (G.silindir((SEG_X, AY, AZ), (1, 0, 0), 3.2, DIN6799_5['s'] + 0.05, 32) - G.silindir((SEG_X - 0.1, AY, AZ), (1, 0, 0), DIN6799_5['yuva'] / 2, 1.0, 32))
    D['e_segman'] = e_segman(SEG_X, AY, AZ)
    return D


# ============================================================ motor braketi (delikli) + vidalar + arka PEM / köpük kapağı + motor M3 delikleri
ARKA_PEM = [(1500.0, 436.0), (1500.0, 457.5)]


def havsa(p, a, d, t):
    """DIN 7991 başına uyan havşa: başın koni ölçüsü + 0,1 boşluk, sonra ISO 273 geçiş"""
    dk, k = G.DIN7991[d]; a = np.asarray(a, float); p = np.asarray(p, float); r2 = G.D_NOM[d] / 2 - 0.05 + 0.1
    return G.silindir(p - a * 0.01, a, dk / 2 + 0.1, k + 0.02, 40, r2) + G.silindir(p - a * 0.5, a, G.GECIS[d] / 2, t + 1.0, 24)


def geo_motor():
    D = {}
    taban = G.fark(K((1481, 424.5, -790), (1524, 468.5, -787)), [G.silindir((1487.0, YC, ZC), (1, 0, 0), 18.2, 38.0, 64)] +
                   [havsa((x, y, -787.0), (0, 0, -1), 'M5', 3.0) for x, y in ARKA_PEM])
    dik = G.fark(K((1481, 424.5, -787), (1484, 468.5, -751.5)), [G.silindir((1480.0, YC, ZC), (1, 0, 0), 11.25, 5.0, 64)] +
                 [havsa((1481.0, y, z), (1, 0, 0), 'M3', 3.0) for y, z in M3PCD])
    D['motor_braketi'] = taban + dik
    for i, (x, y) in enumerate(ARKA_PEM):
        D['vida_braket_%d' % (i + 1)] = G.din7991((x, y, -787.0), (0, 0, -1), 'M5', 6.0)
        D['pem_arka_%d' % (i + 1)] = G.pem_somun((x, y, -790.0 - 0.23), (0, 0, -1), 'M5', 0.97)
        c = G.PEM_SOMUN['M5']
        D['kopuk_kapagi_arka_%d' % (i + 1)] = G.silindir((x, y, -791.2), (0, 0, -1), c['E'] / 2 + 0.8, 3.1, 32) - G.silindir((x, y, -791.0), (0, 0, -1), c['E'] / 2, 2.3, 32)
    for i, (y, z) in enumerate(M3PCD):
        D['vida_motor_%d' % (i + 1)] = G.din7991((1481.0, y, z), (1, 0, 0), 'M3', 6.0)
    D['setskur'] = G.silindir((KX_K, YC, ZC + 4.0), (0, 0, 1), 1.45, 4.0, 16)
    return D


def kes_motor():
    """motor yüzü 4 × M3 dişli (derinlik 5) · arka iç sac Ø6,4 PEM deliği · PU köpük kapağı cebi · kasnak setskur deliği"""
    return dict(motor=[G.silindir((1483.9, y, z), (1, 0, 0), 1.5, 5.1, 20) for y, z in M3PCD],
                sac=[G.silindir((x, y, -789.5), (0, 0, -1), G.PEM_SOMUN['M5']['delik'] / 2, 2.2, 32) for x, y in ARKA_PEM],
                pu=[G.silindir((x, y, -791.0), (0, 0, -1), G.PEM_SOMUN['M5']['E'] / 2 + 0.8, 3.3, 32) for x, y in ARKA_PEM],
                kasnak=[G.silindir((KX_K, YC, ZC + 4.0), (0, 0, 1), 1.5, 14.0, 16)])


# ============================================================ avara kolu ön flanşı → ön çerçeve: 2 × kör perçin (delikler)
PERCIN_X = (1457.5, 1465.0)


def percin_y(flans_ust):
    return flans_ust - 3.0


def geo_percin(py):
    return {'percin_%d' % (i + 1): G.kor_percin((x, py, 24.0), (0, 0, -1), 3.2, 3.0) for i, x in enumerate(PERCIN_X)}


def kes_percin(py):
    return [G.silindir((x, py, 25.0), (0, 0, -1), 1.65, 6.0, 24) for x in PERCIN_X]


# ============================================================ kızak köşebentleri 1,5 + ISO 7380 M4 × 6 + lama M4 dişleri
KOSE_Z = (-540.0, -100.0)


def kose_list():
    L = []
    for yan, (xw, xs, xe) in (('sol', (1466.2, 1, 1483.5)), ('sag', (2060.8, -1, 2043.5))):
        for j, zc in enumerate(KOSE_Z):
            L.append(dict(ad='kose_%s_%d' % (yan, j + 1), yan=yan, zc=zc, xw=xw, xs=xs, xe=xe, xvida=(xw + xe) / 2.0 + 1.0 * xs))
    return L


def geo_kose():
    D = {}
    for k in kose_list():
        xw, xs, xe, zc = k['xw'], k['xs'], k['xe'], k['zc']
        xv0, xv1 = (xw, xw + 1.5) if xs > 0 else (xw - 1.5, xw)
        xh0, xh1 = (xw, xe) if xs > 0 else (xe, xw)
        yatay = G.fark(K((xh0, 426.5, zc - 10), (xh1, 428.0, zc + 10)), [G.delik((k['xvida'], 428.0, zc), (0, -1, 0), 4.5, 1.5)])
        D[k['ad']] = (yatay, K((xv0, 428.0, zc - 10), (xv1, 438.0, zc + 10)))      # (yatay kol, dik kol) — abkant
        D['vida_' + k['ad']] = G.iso7380((k['xvida'], 428.0, zc), (0, -1, 0), 'M4', 6.0)
    return D


def kes_lama(yan):
    return [G.silindir((k['xvida'], 426.6, k['zc']), (0, -1, 0), 2.0, 5.1, 24) for k in kose_list() if k['yan'] == yan]


# ============================================================ ön braket Ø5,5 + kapak saplamaları (PEM FHS-M5-10) + pul + somun
def stud_xy(yan, lo, hi):
    x = lo[0] + 8.5 if yan == 'sol' else hi[0] - 8.5
    return [(x, lo[1] + 11.5), (x, hi[1] - 11.5)]


def geo_stud(yan, lo, hi):
    D = {}; zf = hi[2]                                                         # braket ön flanşı ön yüzü (z 39)
    for i, (x, y) in enumerate(stud_xy(yan, lo, hi)):
        D['pem_kapak_%s_%d' % (yan, i + 1)] = G.pem_saplama((x, y, zf + 1.0), (0, 0, -1), 'M5', 10.0)
        D['pul_kapak_%s_%d' % (yan, i + 1)] = G.pul((x, y, zf - 2.0), (0, 0, -1), 'M5')
        D['somun_kapak_%s_%d' % (yan, i + 1)] = G.somun((x, y, zf - 3.0), (0, 0, -1), 'M5')
    return D


def kes_stud(yan, lo, hi):
    return [G.silindir((x, y, hi[2] + 0.5), (0, 0, -1), 2.75, 3.0, 32) for x, y in stud_xy(yan, lo, hi)]


# ============================================================ ön kapak PU (dış kabuk ↔ iç panel arası)
def geo_kapak_pu(lo, hi):
    """çekirdek: iç panel alanı (iç panel arkası → dış kabuk) ∪ kenar bandı: fitil kanalının (z ≤ lo+8,3) önünde"""
    lo = np.asarray(lo, float); hi = np.asarray(hi, float)
    return K(lo + [11.7, 10.7, 1.0], hi - [11.7, 10.7, 1.5]) + K(lo + [1.5, 1.5, 8.4], hi - 1.5)


def kes_segman_yuvasi():
    """mil üzerindeki E segman yuvası (Ø6 → Ø5, 0,75 genişlik)"""
    return G.silindir((SEG_X, AY, AZ), (1, 0, 0), 3.3, DIN6799_5['s'] + 0.05, 32) - G.silindir((SEG_X - 0.1, AY, AZ), (1, 0, 0), DIN6799_5['yuva'] / 2, 1.0, 32)
