# -*- coding: utf-8 -*-
"""TEK ÇEKMECE MONTAJ ANİMASYONU v2 (B · K2 sütunu · 3. sıra = CEK_K2_lahm_3) · 4 Eki 2026 · yerel
MONTAJ_ANIMASYON_KURALLARI.md (19 madde) — plan_v2.md ile birebir:
  ÜRETİM: her sac parça DÜZ AÇINIM (lazer: kontur + delik) → ABKANT (büküm tek tek, gerçek sıra) → PEM presleme → hazır rafı · lamalar kesim boyunda + delikli
  MONTAJ: her vida / perçin / PEM / somun / pul tek tek kendi ekseninde · kaynak dikişleri / punta noktaları birleşme anında · ray ünitesi katalog bütünü
Çıktı: otonom/hat3d/v3/cekmece_montaj/cekmece_montaj.glb (morph hedefli: büküm kareleri) + .json · denetim → sonuc_v2.json"""
import sys, os, json, pickle, time, math
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
sys.path.insert(0, os.path.join(HERE, '..', 'adim6')); sys.path.insert(0, HERE); sys.stdout.reconfigure(encoding='utf-8')
import yol_denetim as Y
import v2geo as G
Y.ADIM = 0.002
W = r'C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH_COORDINATION\worktrees\claude-hat3-v8'
OUT = os.path.join(W, 'otonom', 'hat3d', 'v3', 'cekmece_montaj')
M0 = pickle.load(open('parca.pkl', 'rb'))          # v1 çıkarımı (metre) — model parçaları + çevre
MM = {a: dict(V=M0[a]['V'] * 1000.0, F=np.asarray(M0[a]['F'])) for a in M0}

P = {}            # ad → dict(V mm, F, m, tur, ac)
ACIKLAMA = {}


def ekle(ad, V, F, m, tur, ac):
    P[ad] = dict(V=np.asarray(V, float), F=np.asarray(F, np.int64), m=m, tur=tur, ac=ac)


def ekle_mf(ad, man, m, tur, ac):
    V, F = G.mesh(man); ekle(ad, V, F, m, tur, ac)


def bilesenler(V, F):
    from scipy.sparse import coo_matrix
    from scipy.sparse.csgraph import connected_components
    n = len(V); r = np.concatenate([F[:, 0], F[:, 1]]); c = np.concatenate([F[:, 1], F[:, 2]])
    k, lab = connected_components(coo_matrix((np.ones(len(r)), (r, c)), shape=(n, n)), directed=False)
    out = []
    for i in range(k):
        fm = lab[F[:, 0]] == i; vi = np.where(lab == i)[0]; mp = -np.ones(n, int); mp[vi] = np.arange(len(vi))
        out.append((V[vi], mp[F[fm]]))
    return out


def model_mf(V, F):
    import manifold3d as mf
    try:
        m = mf.Manifold(mf.Mesh(vert_properties=np.asarray(V, np.float32), tri_verts=np.asarray(F, np.uint32)))
        return m if m.status() == mf.Error.NoError and not m.is_empty() else None
    except Exception:
        return None


# =====================================================================================================================
# 1. MODEL PARÇALARI (katalog / model ağı aynen)
# =====================================================================================================================
for a in ('sabit_ray_sol', 'sabit_ray_sag', 'ara_ray_sol', 'ara_ray_sag', 'kizak_sol', 'kizak_sag', 'silikon_tepsi', 'on_panel', 'reed_arka', 'reed_on',
          'miknatis', 'kayis', 'kablo_sensor', 'kablo_motor'):
    ekle(a, MM[a]['V'], MM[a]['F'], M0[a]['m'], M0[a]['tur'], M0[a]['ac'])
P['on_panel']['ac'] = 'fitil (silikon, ön kapak kanalına geçer)'; P['on_panel']['m'] = 'koyu'; P['on_panel']['tur'] = 'mek'
P['sabit_ray_sol']['ac'] = P['sabit_ray_sag']['ac'] = 'Accuride DZ3832-0700 dış eleman'
P['ara_ray_sol']['ac'] = P['ara_ray_sag']['ac'] = 'Accuride DZ3832-0700 ara eleman (vida erişim delikli)'
P['kizak_sol']['ac'] = P['kizak_sag']['ac'] = 'Accuride DZ3832-0700 iç eleman (ayrılabilir)'
# motor = gövde + mil + arka kapak + rakor + redüktör göbeği (katalog Transmotec PD3665) · M3 dişli delikler (Ø31) açılır
mv = [MM['motor']] + [MM['motor_flansi']]
Vm = np.vstack([MM['motor']['V'], MM['motor_flansi']['V']]); Fm = np.vstack([MM['motor']['F'], MM['motor_flansi']['F'] + len(MM['motor']['V'])])
YC, ZC = 446.75, -769.0                                                         # motor ekseni (y, z)
M3PCD = [(YC + 15.5 * math.cos(math.radians(a_)), ZC + 15.5 * math.sin(math.radians(a_))) for a_ in (45, 135, 225, 315)]
govde = [b for b in bilesenler(MM['motor']['V'], MM['motor']['F'])]
parcalar_motor = []
DELIK_ACILAN = []
for Vb, Fb in govde + bilesenler(MM['motor_flansi']['V'], MM['motor_flansi']['F']):
    m_ = model_mf(Vb, Fb)
    if m_ is not None and Vb[:, 0].min() > 1483.9 and Vb[:, 0].max() < 1600:   # redüktör + gövde: yüzde 4 × M3 dişli delik (derinlik 5)
        m_ = G.fark(m_, [G.silindir((1483.9, y_, z_), (1, 0, 0), 1.5, 5.1, 20) for y_, z_ in M3PCD]); DELIK_ACILAN.append('motor yüzü 4 × M3 (derinlik 5)')
        Vb, Fb = G.mesh(m_)
    parcalar_motor.append((Vb, Fb))
VV, FF, n_ = [], [], 0
for Vb, Fb in parcalar_motor: VV.append(Vb); FF.append(Fb + n_); n_ += len(Vb)
ekle('motor', np.vstack(VV), np.vstack(FF), 'motor', 'mek', 'step motor Transmotec PD3665 (redüktör göbeği + mil + enkoder + M12)')
# motor kasnağı: setskur deliği (önden, +z yönünde göbek) · avara: kasnak / mil ayrı
mk = model_mf(MM['arka_kasnak']['V'], MM['arka_kasnak']['F'])
KX_K = (1469.0 + 1480.0) / 2.0
if mk is not None:
    mk = mk - G.silindir((KX_K, YC, ZC + 4.0), (0, 0, 1), 1.5, 14.0, 16) - G.silindir((1468.0, YC, ZC), (1, 0, 0), 4.3, 13.0, 48); DELIK_ACILAN.append('motor kasnağı radyal M3 setskur deliği + Ø8,1 göbek (H7 boşluğu)')
    ekle_mf('arka_kasnak', mk, 'alu', 'mek', 'GT3 motor kasnağı 30 diş (Ø8 + M3 setskur)')
else:
    ekle('arka_kasnak', MM['arka_kasnak']['V'], MM['arka_kasnak']['F'], 'alu', 'mek', 'GT3 motor kasnağı 30 diş')
for Vb, Fb in bilesenler(MM['avara_kasnagi']['V'], MM['avara_kasnagi']['F']):
    if Vb[:, 1].max() - Vb[:, 1].min() > 20: ekle('avara_kasnagi', Vb, Fb, 'alu', 'mek', 'GT3 avara 30 diş · 2 × MR126-2RS')
    else: AVARA_MILI = (Vb, Fb)
# ray vidaları: M5 × 10 → M5 × 6 (ana model adım 43 ile aynı: uç düzlemi başa doğru 4 mm)
VIDA_RAY = []
for s_ in ('sol', 'sag'):
    for k_ in (1, 2, 3):
        a = 'vida_%s_%d' % (s_, k_); V = MM[a]['V'].copy()
        uc = V[:, 0].min() if s_ == 'sol' else V[:, 0].max()
        m_ = np.abs(V[:, 0] - uc) < 0.01; V[m_, 0] += 4.0 if s_ == 'sol' else -4.0
        ekle(a, V, MM[a]['F'], 'baglanti', 'baglanti', 'DIN 7991 M5 × 6 A2 havşa'); VIDA_RAY.append(a)

# =====================================================================================================================
# 2. ÇEVRE (silik): v1 kırpılmış gövde − B_KABLO dikey kanalı (sütun ortak, tahrikler takıldıktan SONRA) + eklenen PEM / köpük kapağı
# =====================================================================================================================
for a in M0:
    if M0[a]['tur'] != 'cevre': continue
    V, F = MM[a]['V'], MM[a]['F']
    if a == 'cevre_kanal':
        T = V[F]; c = T.mean(1)
        sil = (c[:, 0] > 1643.55) & (c[:, 2] < -764.0)
        tum = np.all(np.abs(T[:, :, 0] - 1643.5) < 0.01, 1) & (T[:, :, 2].max(1) <= -764.5)
        F = F[~(sil | tum)]
    ekle(a, V, F, 'silik', 'cevre', a)
TEZ = (1520.0, 2010.0, 0.0, 421.5, 330.0, 900.0)                                 # montaj tezgâhı (çekmece burada)
URT = (2230.0, 3640.0, 0.0, 421.5, -760.0, 990.0)                                 # üretim tezgâhı (lazer / abkant / PEM pres + hazır rafı)
ekle_mf('tezgah', G.kutu((TEZ[0], TEZ[2], TEZ[4] + 1150.0), (TEZ[1], TEZ[3], TEZ[5] + 1150.0)), 'tezgah', 'cevre', 'montaj tezgâhı (tekerlekli)')
ekle_mf('tezgah_uretim', G.kutu(URT[0::2], URT[1::2]), 'tezgah', 'cevre', 'üretim tezgâhı')
# arka iç sacda (z −791,2…−790) eklenen PEM'ler + köpük kapakları (B sac üretecinde EKSİK — rapor)
EKLENEN_CEVRE = []
ARKA_PEM = [('M5', 1500.0, 436.0), ('M5', 1500.0, 457.5)]
for i, (d_, x_, y_) in enumerate(ARKA_PEM):
    c_ = G.PEM_SOMUN[d_]
    pem = G.pem_somun((x_, y_, -790.0 - 0.23), (0, 0, -1), d_, 0.97)
    ekle_mf('cevre_pem_arka_%d' % i, pem, 'silik', 'cevre', 'PEM SP-%s-1 (arka iç sac) — modele eklenecek' % d_)
    kap = G.silindir((x_, y_, -791.2), (0, 0, -1), c_['E'] / 2 + 0.8, 3.1, 32) - G.silindir((x_, y_, -791.0), (0, 0, -1), c_['E'] / 2, 2.3, 32)
    ekle_mf('cevre_kopuk_kapagi_arka_%d' % i, kap, 'silik', 'cevre', 'köpük kapağı (PE) — modele eklenecek')
    EKLENEN_CEVRE.append('arka iç sac: PEM SP-%s-1 + köpük kapağı (x %.1f · y %.1f) — B_KASA sac üretecinde yok' % (d_, x_, y_))

# =====================================================================================================================
# 3. ÜRETİLEN SAC / LAMA PARÇALARI (paneller son konumda) — union ≈ model (aşağıda denetlenir)
# =====================================================================================================================
SAC = {}          # ad → G.Sac
YAPI = {}         # ad → dict(model=..., Q=..., delikler=[...], pem=[...], tur)
K = G.kutu


def sac(ad, t, Q, model=None, tip='sac', ac=''):
    s = G.Sac(ad, t); SAC[ad] = s; YAPI[ad] = dict(model=model, Q=Q, ac=ac, tip=tip); return s


RX = lambda d: G.rot((1, 0, 0), d)
RZ = lambda d: G.rot((0, 0, 1), d)
I3 = np.eye(3)
# ---- çekmece kutusu: 5 düz sac, TIG (v14: taban 2 + yanlar 1)
s = sac('kutu_taban', 2.0, I3, ac='çekmece tabanı 2 mm (lazer, düz)'); s.ekle('taban', K((1483.5, 421.5, -597), (2043.5, 423.5, 22)))
s = sac('kutu_yan_sol', 1.0, RZ(-90), ac='kutu sol yanı 1 mm (lazer, düz)'); s.ekle('yan', K((1483.5, 423.5, -597), (1484.5, 481.5, 22)))
s = sac('kutu_yan_sag', 1.0, RZ(90), ac='kutu sağ yanı 1 mm (lazer, düz)'); s.ekle('yan', K((2042.5, 423.5, -597), (2043.5, 481.5, 22)))
s = sac('kutu_arka', 1.0, RX(-90), ac='kutu arkası 1 mm (lazer, düz)'); s.ekle('arka', K((1484.5, 423.5, -597), (2042.5, 481.5, -596)))
s = sac('kutu_on', 1.0, RX(-90), ac='kutu önü 1 mm (lazer, düz)'); s.ekle('on', K((1484.5, 423.5, 21), (2042.5, 481.5, 22)))
# ---- ön bağlantı braketleri (U, 2 mm, 2 büküm) · flanşta 2 × Ø5,5 (kapak saplamaları)
STUD = {'sol': [(1492.0, 440.0), (1492.0, 466.0)], 'sag': [(2035.0, 440.0), (2035.0, 466.0)]}
s = sac('on_braket_sol', 2.0, RX(-90), model='on_braket_sol', ac='ön bağlantı braketi sol · U 2 mm')
i0 = s.ekle('plaka', K((1483.5, 428.5, 22), (1498.5, 477.5, 24)))
i1 = s.ekle('yan', K((1483.5, 428.5, 24), (1485.5, 477.5, 39)), i0, (1484.5, 0, 23.0), (0, 1, 0), 90, 'yan kol')
s.ekle('flans', G.fark(K((1485.5, 428.5, 37), (1498.5, 477.5, 39)), [G.delik((x_, y_, 37), (0, 0, 1), 5.5, 2) for x_, y_ in STUD['sol']]), i1, (1484.5, 0, 38.0), (0, 1, 0), 90, 'ön flanş')
s = sac('on_braket_sag', 2.0, RX(-90), model='on_braket_sag', ac='ön bağlantı braketi sağ · U 2 mm')
i0 = s.ekle('plaka', K((2028.5, 428.5, 22), (2043.5, 477.5, 24)))
i1 = s.ekle('yan', K((2041.5, 428.5, 24), (2043.5, 477.5, 37)), i0, (2042.5, 0, 23.0), (0, 1, 0), 90, 'yan kol')
s.ekle('flans', G.fark(K((2028.5, 428.5, 37), (2043.5, 477.5, 39)), [G.delik((x_, y_, 37), (0, 0, 1), 5.5, 2) for x_, y_ in STUD['sag']]), i1, (2042.5, 0, 38.0), (0, 1, 0), 90, 'ön flanş')
# ---- motor braketi 3 mm (1 büküm): taban 2 × M5 havşa (arka duvara) · dik kol Ø22,5 göbek deliği + 4 × M3 havşa (Ø31)
s = sac('motor_braketi', 3.0, RX(-90), model='motor_braketi', ac='motor braketi 3 mm')
taban = G.fark(K((1481, 424.5, -790), (1524, 468.5, -787)), [G.silindir((1487.0, YC, ZC), (1, 0, 0), 18.2, 38.0, 64)] +
               [G.havsa_delik((x_, y_, -787.0), (0, 0, -1), 'M5', 3.0) for _, x_, y_ in ARKA_PEM[:2]])
i0 = s.ekle('taban', taban)
dik = G.fark(K((1481, 424.5, -787), (1484, 468.5, -751.5)), [G.silindir((1480.0, YC, ZC), (1, 0, 0), 11.25, 5.0, 64)] +
             [G.havsa_delik((1481.0, y_, z_), (1, 0, 0), 'M3', 3.0) for y_, z_ in M3PCD])
s.ekle('dik_kol', dik, i0, (1482.5, 0, -788.5), (0, 1, 0), 90, 'motor flanş kolu')
# ---- sensör plakası 2 mm (düz) · 2 × Ø4,5
s = sac('sensor_plakasi', 2.0, RX(-90), model='sensor_plakasi', ac='sensör plakası 2 mm')
s.ekle('plaka', K((1453.9, 463.55, -790), (1469.9, 487.55, -788)))
# ---- avara kolu 2 mm (2 büküm) + sensör laması L 2 mm (1 büküm) + avara mili (saplama kaynağı) → kaynaklı ünite
PERCIN = [(1457.5, 509.5), (1465.0, 509.5)]
s = sac('avara_kolu', 2.0, RZ(-90), ac='avara kolu 2 mm · ön flanş + üst flanş')
i0 = s.ekle('kol', K((1467.2, 438.5, -9), (1469.2, 503.5, 23)) + K((1467.2, 487.55, -29), (1469.2, 495.55, -9)))
s.ekle('on_flans', G.fark(K((1454.5, 492.5, 21), (1467.2, 512.5, 23)), [G.delik((x_, y_, 23), (0, 0, -1), 3.3, 2) for x_, y_ in PERCIN]), i0, (1468.2, 0, 22.0), (0, 1, 0), 90, 'ön flanş (çerçeveye)')
s.ekle('ust_flans', K((1469.2, 501.5, -9), (1479.2, 503.5, 23)), i0, (1468.2, 502.5, 0), (0, 0, 1), 90, 'üst flanş')
s = sac('sensor_lamasi', 2.0, I3, ac='sensör laması L 6,35 × 8 × 2')
i0 = s.ekle('yatay', K((1463.55, 485.55, -756), (1469.9, 487.55, -9)))
s.ekle('dik', K((1463.55, 487.55, -756), (1465.55, 493.55, -9)), i0, (1464.55, 486.55, 0), (0, 0, 1), 90, 'dik kol')
# ---- ön kapak: dış kabuk 1,5 (4 kenar + 4 arka dönüş = 8 büküm) + iç panel 1,0 (düz) + 4 × PEM FHS-M5-10
s = sac('kapak_dis', 1.5, RX(90), ac='çekmece önü dış kabuk 1,5')
f0 = s.ekle('on_yuz', K((1437.5, 401.5, 77.5), (2089.5, 506.5, 79)))
wl = s.ekle('kenar_sol', K((1437.5, 403, 39), (1439, 505, 77.5)), f0, (1438.25, 0, 78.25), (0, 1, 0), 90, 'sol kenar')
wr = s.ekle('kenar_sag', K((2088, 403, 39), (2089.5, 505, 77.5)), f0, (2088.75, 0, 78.25), (0, 1, 0), 90, 'sağ kenar')
wb = s.ekle('kenar_alt', K((1437.5, 401.5, 39), (2089.5, 403, 77.5)), f0, (0, 402.25, 78.25), (1, 0, 0), 90, 'alt kenar')
wt = s.ekle('kenar_ust', K((1437.5, 505, 39), (2089.5, 506.5, 77.5)), f0, (0, 505.75, 78.25), (1, 0, 0), 90, 'üst kenar')
s.ekle('donus_sol', K((1439, 403, 39), (1442.8, 505, 40.5)), wl, (1438.25, 0, 39.75), (0, 1, 0), 90, 'sol arka dönüş')
s.ekle('donus_sag', K((2084.2, 403, 39), (2088, 505, 40.5)), wr, (2088.75, 0, 39.75), (0, 1, 0), 90, 'sağ arka dönüş')
s.ekle('donus_alt', K((1442.8, 403, 39), (2084.2, 405.8, 40.5)), wb, (0, 402.25, 39.75), (1, 0, 0), 90, 'alt arka dönüş')
s.ekle('donus_ust', K((1442.8, 502.2, 39), (2084.2, 505, 40.5)), wt, (0, 505.75, 39.75), (1, 0, 0), 90, 'üst arka dönüş')
s = sac('kapak_ic', 1.0, RX(-90), ac='çekmece önü iç panel 1,0')
s.ekle('panel', G.fark(K((1449.2, 412.2, 39), (2077.8, 495.8, 40)), [G.delik((x_, y_, 39), (0, 0, 1), G.PEM_SAPLAMA['M5']['delik'], 1) for k_ in STUD for x_, y_ in STUD[k_]]))
# ---- kızak bağlantı köşebendi 1,5 (EKLENDİ — modelde kızak ↔ lama arasında bağ yoktu) · 1 büküm · yatay kolda Ø4,5
KOSE_Z = (-540.0, -100.0)
KOSE = []
for yan, (xw, xs, xe) in (('sol', (1466.2, 1, 1483.5)), ('sag', (2060.8, -1, 2043.5))):
    for j, zc in enumerate(KOSE_Z):
        ad = 'kose_%s_%d' % (yan, j + 1); xv0, xv1 = (xw, xw + 1.5) if xs > 0 else (xw - 1.5, xw)
        xh0, xh1 = (xw, xe) if xs > 0 else (xe, xw)
        xvida = (xw + xe) / 2.0 + 1.0 * xs
        s = sac(ad, 1.5, I3, ac='kızak bağlantı köşebendi 1,5 (eklendi)')
        i0 = s.ekle('yatay', G.fark(K((xh0, 426.5, zc - 10), (xh1, 428.0, zc + 10)), [G.delik((xvida, 428.0, zc), (0, -1, 0), 4.5, 1.5)]))
        s.ekle('dik', K((xv0, 428.0, zc - 10), (xv1, 438.0, zc + 10)), i0, ((xv0 + xv1) / 2, 427.25, 0), (0, 0, 1), 90, 'dik kol (kızağa)')
        KOSE.append(dict(ad=ad, yan=yan, zc=zc, xvida=xvida, xw=xw, xs=xs))
# ---- lamalar (6 mm lama, kesim boyu 616) · 2 × M4 dişli kör delik (köşebent vidaları)
LAMA = {}
for yan, x0_, x1_ in (('sol', 1466.2, 1483.5), ('sag', 2043.5, 2060.8)):
    m_ = K((x0_, 420.5, -597), (x1_, 426.5, 19))
    m_ = G.fark(m_, [G.silindir((k['xvida'], 426.6, k['zc']), (0, -1, 0), 2.0, 5.1, 24) for k in KOSE if k['yan'] == yan])
    s = sac('lama_' + yan, 6.0, I3, model='kizak_lamasi_' + yan, tip='lama', ac='kızak lama %s · 6 × 17,3 × 616 (2 × M4 dişli)' % yan); s.ekle('lama', m_)
# ---- kayış çenesi: alt gövde (alt çene + ara parça + kol, TIG) · üst çene + mıknatıs ayağı (2 × M3 ile)
M3K = [(1480.2, -743.0), (1480.2, -729.0)]
del3 = lambda: [G.delik((x_, 470.0, z_), (0, -1, 0), 3.4, 20.0) for x_, z_ in M3K]
s = sac('cene_alt', 2.5, I3, tip='lama', ac='kayış çenesi alt gövde (alt çene 2,5 + ara 1,26 + kol 3) · TIG')
s.ekle('alt_cene', G.fark(K((1470.5, 457.95, -751), (1483.5, 460.45, -721)), del3()))
s.ekle('ara', G.fark(K((1477.5, 460.45, -751), (1483.5, 461.71, -721)), del3()))
s.ekle('kol', K((1480.5, 457.95, -721), (1483.5, 464.21, -567)))
s = sac('cene_ust', 2.5, I3, tip='lama', ac='kayış çenesi üst (dişli) + mıknatıs ayağı')
s.ekle('ust_cene', G.fark(K((1470.5, 461.71, -751), (1483.5, 464.21, -721)), del3()))
s.ekle('ayak', K((1470.5, 464.21, -751), (1476.85, 466.5, -722.43)))

# model ↔ üretilen: hacim farkı (delikler hariç) + kutu
KIYAS = {}
def kiyas(ad, birlesik, model_ad):
    mm_ = model_mf(MM[model_ad]['V'], MM[model_ad]['F'])
    V, F = G.mesh(birlesik); lo, hi = V.min(0), V.max(0)
    lo0, hi0 = MM[model_ad]['V'].min(0), MM[model_ad]['V'].max(0)
    r = dict(kutu_fark=round(float(max(np.abs(lo - lo0).max(), np.abs(hi - hi0).max())), 4))
    if mm_ is not None:
        r['model_hacim'] = round(mm_.volume(), 1); r['uretim_hacim'] = round(birlesik.volume(), 1)
        r['fark_hacim'] = round((mm_ - birlesik).volume() + (birlesik - mm_).volume(), 1)
    KIYAS[ad] = r


# =====================================================================================================================
# 4. BAĞLANTI ELEMANLARI (tek tek)
# =====================================================================================================================
EL = {}          # ad → dict(man, ac, eks (giriş yönü birim), yol (mm, giriş öncesi uzaklık), karsi)
def el(ad, man, ac, eks, yol=30.0):
    EL[ad] = dict(eks=np.asarray(eks, float), yol=yol); ekle_mf(ad, man, 'baglanti', 'baglanti', ac)


# motor braketi → arka duvar: 2 × DIN 7991 M5 × 6 (PEM SP-M5, arka iç sac)
for i, (_, x_, y_) in enumerate(ARKA_PEM[:2]):
    el('vida_braket_%d' % (i + 1), G.din7991((x_, y_, -787.0), (0, 0, -1), 'M5', 6.0), 'DIN 7991 M5 × 6 A2', (0, 0, -1), 40)
# motor → braket: 4 × DIN 7991 M3 × 6 (redüktör yüzündeki M3'e)
for i, (y_, z_) in enumerate(M3PCD):
    el('vida_motor_%d' % (i + 1), G.din7991((1481.0, y_, z_), (1, 0, 0), 'M3', 6.0), 'DIN 7991 M3 × 6 A2', (1, 0, 0), 12)
# kasnak setskuru DIN 913 M3 × 4 (göbekte, önden)
el('setskur', G.setskur((KX_K, YC, ZC + 6.0), (0, 0, 1), 'M3', 4.0) if False else G.silindir((KX_K, YC, ZC + 6.0), (0, 0, 1), 1.45, 4.0, 16), 'DIN 913 M3 × 4 setskur', (0, 0, -1), 25)
# avara kolu ön flanşı → ön çerçeve: 2 × kör perçin Ø3,2 (ISO 15983 A2/A2), önden
for i, (x_, y_) in enumerate(PERCIN):
    el('percin_%d' % (i + 1), G.kor_percin((x_, y_, 24.0), (0, 0, -1), 3.2, 3.0), 'kör perçin Ø3,2 × 6 ISO 15983 A2/A2', (0, 0, -1), 40)
# köşebent → lama: ISO 7380 M4 × 6 (lamadaki M4 dişe)
for k in KOSE:
    el('vida_' + k['ad'], G.iso7380((k['xvida'], 428.0, k['zc']), (0, -1, 0), 'M4', 6.0), 'ISO 7380 M4 × 6 A2', (0, -1, 0), 30)
# üst çene → alt çene: 2 × ISO 7380 M3 × 10 + 2 × ISO 4032 M3
for i, (x_, z_) in enumerate(M3K):
    el('vida_cene_%d' % (i + 1), G.iso7380((x_, 464.21, z_), (0, -1, 0), 'M3', 10.0), 'ISO 7380 M3 × 10 A2', (0, -1, 0), 30)
    el('somun_cene_%d' % (i + 1), G.somun((x_, 457.95, z_), (0, -1, 0), 'M3'), 'ISO 4032 M3 A2', (0, 1, 0), 20)
# kapak saplamaları (PEM FHS-M5-10, iç panele preslenir) + pul + somun
for k_ in STUD:
    for i, (x_, y_) in enumerate(STUD[k_]):
        ekle_mf('pem_kapak_%s_%d' % (k_, i + 1), G.pem_saplama((x_, y_, 40.0), (0, 0, -1), 'M5', 10.0), 'baglanti', 'baglanti', 'PEM FHS-M5-10 saplama')
        el('pul_kapak_%s_%d' % (k_, i + 1), G.pul((x_, y_, 37.0), (0, 0, -1), 'M5'), 'DIN 125 M5 A2 pul', (0, 0, 1), 0)
        el('somun_kapak_%s_%d' % (k_, i + 1), G.somun((x_, y_, 36.0), (0, 0, -1), 'M5'), 'ISO 4032 M5 A2', (0, 0, 1), 0)

# =====================================================================================================================
# 5. KAYNAK DİKİŞLERİ / PUNTA NOKTALARI (birleşme anında belirir + vurgu — kural 5)
# =====================================================================================================================
KAY = {}
def kaynak(ad, L, ac):
    ekle_mf(ad, G.birlesim(L), 'kaynak', 'kaynak', ac); KAY[ad] = ac


kaynak('kaynak_kutu_yan_sol', [G.kaynak_dikisi((1484.5 + 0.6, 423.5 + 0.6, -595.5), (1484.5 + 0.6, 423.5 + 0.6, 20.5))], 'TIG iç köşe: sol yan ↔ taban')
kaynak('kaynak_kutu_yan_sag', [G.kaynak_dikisi((2042.5 - 0.6, 423.5 + 0.6, -595.5), (2042.5 - 0.6, 423.5 + 0.6, 20.5))], 'TIG iç köşe: sağ yan ↔ taban')
kaynak('kaynak_kutu_arka', [G.kaynak_dikisi((1485.1, 424.1, -595.4), (2041.9, 424.1, -595.4)), G.kaynak_dikisi((1485.1, 424.1, -595.4), (1485.1, 480.9, -595.4)),
                            G.kaynak_dikisi((2041.9, 424.1, -595.4), (2041.9, 480.9, -595.4))], 'TIG: arka ↔ taban + iki yan')
kaynak('kaynak_kutu_on', [G.kaynak_dikisi((1485.1, 424.1, 20.4), (2041.9, 424.1, 20.4)), G.kaynak_dikisi((1485.1, 424.1, 20.4), (1485.1, 480.9, 20.4)),
                          G.kaynak_dikisi((2041.9, 424.1, 20.4), (2041.9, 480.9, 20.4))], 'TIG: ön ↔ taban + iki yan')
for yan, xf in (('sol', 1483.5), ('sag', 2043.5)):
    kaynak('punta_lama_' + yan, [G.kaynak_noktasi((xf, 424.8, z_), 1.6) for z_ in (-560.0, -380.0, -200.0, -20.0)], 'punta: lama ↔ kutu yanı (4 nokta)')
    kaynak('punta_braket_' + yan, [G.kaynak_noktasi((x_, y_, 22.0), 1.6) for x_, y_ in ((1491.0, 436.0), (1491.0, 470.0))] if yan == 'sol' else
           [G.kaynak_noktasi((x_, y_, 22.0), 1.6) for x_, y_ in ((2036.0, 436.0), (2036.0, 470.0))], 'punta: ön braket ↔ kutu önü (2 nokta)')
for k in KOSE:
    kaynak('punta_' + k['ad'], [G.kaynak_noktasi((k['xw'], 433.0, k['zc'] + dz), 1.2) for dz in (-5.0, 5.0)], 'punta: köşebent ↔ kızak gövdesi (2 nokta) — ÖNERİ, Kemal kararı')
kaynak('kaynak_cene', [G.kaynak_dikisi((1480.5, 457.95 + 0.7, -721.0), (1480.5, 463.5, -721.0), 0.6), G.kaynak_dikisi((1477.9, 460.95, -751.0), (1483.1, 460.95, -751.0), 0.45), G.kaynak_dikisi((1477.9, 460.95, -721.0), (1480.4, 460.95, -721.0), 0.45)],
       'TIG: kol ↔ alt çene · ara parça ↔ alt çene')
kaynak('kaynak_cene_kutu', [G.kaynak_dikisi((1483.5, 457.95, -596.5), (1483.5, 457.95, -567.5)), G.kaynak_dikisi((1483.5, 464.21, -596.5), (1483.5, 464.21, -567.5))],
       'TIG: çene kolu ↔ kutu sol yanı (alt + üst kenar)')
kaynak('kaynak_avara', [G.kaynak_dikisi((1467.2, 487.55 + 0.4, -29.0), (1467.2, 487.55 + 0.4, -9.0)), G.kaynak_dikisi((1469.2, 487.55 + 0.4, -29.0), (1469.2, 487.55 + 0.4, -9.0)),
                        G.kaynak_dikisi((1467.6, 486.55, -9.0), (1469.6, 486.55, -9.0))], 'TIG: avara kolu kulağı ↔ sensör laması (iki yan + uç)')
kaynak('kaynak_avara_mili', [G.silindir((1469.2, YC, -1.0), (1, 0, 0), 4.2, 0.9, 24) - G.silindir((1469.0, YC, -1.0), (1, 0, 0), 3.0, 1.4, 24)], 'saplama kaynağı: avara mili ↔ kol')
ekle('avara_mili', AVARA_MILI[0], AVARA_MILI[1], 'mekanizma', 'mek', 'avara mili Ø6 (kola saplama kaynaklı)')

# =====================================================================================================================
# 6. SAC KARELERİ (açınım → bükümler → çevirme) + açınım 2B verisi
# =====================================================================================================================
BENCH_Y = URT[3]


def sac_hazirla(ad):
    s = SAC[ad]; V, F, PI = s.ag()
    birl = s.katı()
    if YAPI[ad]['model']: kiyas(ad, birl, YAPI[ad]['model'])
    ekle(ad, V, F, 'sac' if YAPI[ad]['tip'] == 'sac' else 'profil', 'sac', YAPI[ad]['ac'])
    P[ad]['PI'] = PI
    return V, F, PI


for ad in SAC: sac_hazirla(ad)
# avara ünitesi + kapak + çekmece kutusu: model ile kıyas (birleşik)
kiyas('avara_unitesi', SAC['avara_kolu'].katı() + SAC['sensor_lamasi'].katı(), 'avara_braketi')
kiyas('kutu', G.birlesim([SAC[a].katı() for a in ('kutu_taban', 'kutu_yan_sol', 'kutu_yan_sag', 'kutu_arka', 'kutu_on')]), 'cekmece_govdesi')
kiyas('cene', SAC['cene_alt'].katı() + SAC['cene_ust'].katı(), 'kayis_lamasi')
_ki = SAC['kapak_dis'].katı() + SAC['kapak_ic'].katı(); _V, _ = G.mesh(_ki)
KIYAS['kapak'] = dict(kutu_fark=round(float(max(np.abs(_V.min(0) - MM['on_kapak']['V'].min(0)).max(), np.abs(_V.max(0) - MM['on_kapak']['V'].max(0)).max())), 4),
                      not_='model ağı kapalı değil (hacim kıyası yapılamaz) — dış kutu kıyaslandı')

# =====================================================================================================================
# 7. ZAMAN ÇİZELGESİ
# =====================================================================================================================
HAR = {a: [] for a in P}; GOR = {}; MF = {}; FR = {}; VU = {a: [] for a in P}; ISTISNA = set()
ADIM, OLAY, KAM, ACN = [], [], [], []
t = 0.0
CUR = {}         # ad → mevcut öteleme (mm, son konuma göre)


def mm2(v): return [round(float(x) / 1000.0, 6) for x in v]


def merkez(ad):
    V = P[ad]['V']; return (V.min(0) + V.max(0)) / 2.0


def basla(ad, ofs, tg):
    CUR[ad] = np.asarray(ofs, float); GOR[ad] = round(tg, 3)


def git(ad, ofs, t0, sure):
    ofs = np.asarray(ofs, float)
    d = CUR[ad] - ofs
    if np.linalg.norm(d) > 1e-9: HAR[ad].append([round(t0, 3), round(t0 + sure, 3)] + mm2(d))
    CUR[ad] = ofs


def yolu(adlar, noktalar, t0, hiz=420.0, enaz=0.35):
    """adlar ortak hareket: noktalar = öteleme dizisi (ilk adın ötelemesi); diğerleri aynı farkla · süre = mesafe / hız"""
    tt = t0; ref = adlar[0]
    for n_ in noktalar:
        n_ = np.asarray(n_, float); d = n_ - CUR[ref]; L = np.linalg.norm(d)
        if L < 1e-9: continue
        sure = max(enaz, L / hiz)
        for a in adlar: git(a, CUR[a] + d, tt, sure)
        tt += sure
    return tt


def vurgu(adlar, t0, t1):
    for a in adlar: VU[a].append([round(t0, 3), round(t1, 3)])


def olay(tt, m): OLAY.append([round(tt, 3), m])


def adim(ad, metin, liste, kam):
    ADIM.append(dict(no=len(ADIM) + 1, ad=ad, t0=round(t, 3), metin=metin, liste=liste))
    KAM.append([round(t, 3), kam[0], kam[1]])


def kam(tt, k): KAM.append([round(tt, 3), k[0], k[1]])


# ---------------------------------------------------------------- üretim (morph kareleri)
FAB = np.array([2470.0, 0.0, 560.0])                     # lazer / abkant noktası (x, z)
RAF = {}                                                  # hazır rafı yuvaları
_raf_x = [2700.0, 2860.0, 3020.0, 3170.0]; _raf_z = [300.0, 470.0, 640.0, 810.0]
_raf_sira = [(x_, z_) for z_ in _raf_z for x_ in _raf_x]


def raf_yeri(ad, genis=False):
    x_, z_ = _raf_sira.pop(0); return np.array([x_, 0.0, z_])


def sac_kareleri(ad, ek=(), yer=None):
    """ad sacının üretim kareleri (dünya mm): kayarak gelir (düz) → bükümler sırayla → son yönelime çevrilir · ek: aynı sacla taşınan (PEM) [ad, panel, giriş ekseni, zaman]"""
    s = SAC[ad]; V = P[ad]['V']; PI = P[ad]['PI']; Q = YAPI[ad]['Q']; c = merkez(ad)
    nb = len(s.bukum)
    def poz(u, R, kay=0.0):
        X = s.kare(V, PI, u); X = (X - c) @ R.T
        return X
    # son konum (tezgâhta, son yönelim) — sacın en altı tezgâhta
    X1 = poz({}, I3); yer = FAB.copy() if yer is None else yer
    ofs0 = np.array([yer[0] - c[0], BENCH_Y - (X1[:, 1].min() + c[1]), yer[2] - c[2]])     # sac son yönelimde tezgâhta → öteleme
    kareler = []           # (dünya köşeleri) listesi
    def ekle_kare(u, R, kay=0.0):
        X = poz(u, R); X[:, 1] += BENCH_Y - X[:, 1].min(); X[:, 0] += yer[0]; X[:, 2] += yer[2] + kay
        kareler.append(X)
    u_duz = {i: 1.0 for i in range(nb)}
    zam = []               # (kare indisi aralığı, olay)
    ekle_kare(u_duz, Q, 260.0); ekle_kare(u_duz, Q, 0.0); zam.append(('kay', 0, 1))
    u = dict(u_duz)
    for bi in range(nb):
        k0 = len(kareler) - 1
        for f in np.linspace(1, 0, 7)[1:]:
            u[bi] = f; ekle_kare(dict(u), Q)
        zam.append(('bukum', k0, len(kareler) - 1, bi))
    if not np.allclose(Q, I3):
        k0 = len(kareler) - 1
        for f in np.linspace(0, 1, 7)[1:]:
            ekle_kare({}, G.slerp_R(Q, I3, f))
        zam.append(('cevir', k0, len(kareler) - 1))
    return kareler, zam, ofs0, c


def uret(ad, t0, metin_ad, pemler=(), sure_bukum=0.95, yer=None):
    """ad sacını üret: kareler + zaman · pemler: [(pem_ad, panel_i, eksen)] bükümden ÖNCE preslenir (düzken)"""
    global t
    kar, zam, ofs0, c = sac_kareleri(ad, yer=yer)
    basla(ad, ofs0, t0)
    s = SAC[ad]
    # kamera: parçanın düz açınım boyuna göre yakın plan (üretim noktası)
    X1_ = kar[1]; boy = float(np.max(X1_.max(0) - X1_.min(0))); d_ = np.array([0.42, 0.62, 0.66]); d_ /= np.linalg.norm(d_)
    hed = np.array([FAB[0] / 1000.0, (BENCH_Y + min(boy, 300) / 6.0) / 1000.0, FAB[2] / 1000.0]); uz = min(1.7, max(0.2, boy / 1000.0 * 1.6))
    kam(t0, ((hed + d_ * uz).round(3).tolist(), hed.round(3).tolist()))
    base = P[ad]['V'] - c - ofs0 - c * 0          # yerel: köşe − (c + ofs0) ; GLB'de düğüm = c
    seg = []; tt = t0
    yerel = [X - (c + ofs0) for X in kar]
    base_yerel = P[ad]['V'] - c
    FR[ad] = yerel                                 # kare k (yerel, düğüm c + ofs0'a göre … aşağıda düğüm = c olduğu için ofs eklenir)
    # kayma
    seg.append([round(tt, 3), round(tt + 1.0, 3), 0, 1]); olay(tt, '%s · LAZER KESİM: düz açınım (kontur + %d delik) tezgâha gelir' % (metin_ad, sum(p_['m'].genus() for p_ in s.panel)))
    tt += 1.0
    ACN.append(dict(ad=ad, t0=round(tt - 1.0, 3)))
    tt += 0.9
    # PEM presleme (düz sacta)
    for z_ in zam:
        if z_[0] == 'bukum':
            b = s.bukum[z_[3]]
            seg.append([round(tt, 3), round(tt + sure_bukum, 3), z_[1], z_[2]])
            olay(tt, '%s · ABKANT büküm %d / %d: %s · %d° · iç R %.1f' % (metin_ad, b['no'], len(s.bukum), b['aciklama'], round(b['aci']), s.t))
            tt += sure_bukum + 0.25
        elif z_[0] == 'cevir':
            seg.append([round(tt, 3), round(tt + 1.0, 3), z_[1], z_[2]]); olay(tt, '%s · abkanttan alınır, montaj yönüne çevrilir' % metin_ad); tt += 1.15
    # PEM presleme: sac son yönelimde (dik) — saplamalar yatay, tezgâha değmez; pres ekseni boyunca
    for pa, pi, eks in pemler:
        e_ = np.asarray(eks, float); basla(pa, CUR[ad] - e_ * 30.0, tt); git(pa, CUR[ad], tt, 0.9); vurgu([pa], tt + 0.6, tt + 1.4)
        olay(tt, '%s · PEM presleme: %s' % (metin_ad, P[pa]['ac'])); tt += 1.1
    ACN[-1]['t1'] = round(tt, 3)
    # son kare = taban (öteleme ofs0'da) → morph dizisi bitince taban geometrisi
    MF[ad] = dict(seg=seg)
    FRAMES[ad] = [X - (c + ofs0) - (P[ad]['V'] - c) for X in kar]          # delta (yerel)
    return tt


FRAMES = {}


def delik_say(ad):
    s = SAC[ad]; V, F = G.mesh(s.katı())
    import trimesh
    try:
        return max(0, -int(trimesh.Trimesh(V, F, process=True).euler_number // 2) + 1)
    except Exception:
        return 0


def pem_kareleri(pa, sac_ad, pi, eks, X_duz, tg):
    """PEM: düz sacın panelindeki deliğine eksen boyunca preslenir; sonra sacla aynı dönüşümle bükülür / çevrilir"""
    s = SAC[sac_ad]; Vp = P[pa]['V']; cs = merkez(sac_ad)
    # pem köşesinin her karedeki konumu: sacın panel pi dönüşümü (son konumdan) ile
    # sac karelerini yeniden kur (aynı mantık)
    Q = YAPI[sac_ad]['Q']; nb = len(s.bukum)
    ofs_s = CUR[sac_ad]
    yer = None
    kar = []
    def poz(u, R):
        M = s.donusum(pi, u); X = Vp @ M[:3, :3].T + M[:3, 3]; return (X - cs) @ R.T
    # sacın kare ötelemeleri: sac karelerindeki y kaldırma + x/z yer → sac karelerinden türet (aynı min-y kaydırması)
    Vs = P[sac_ad]['V']; PI = P[sac_ad]['PI']
    def sac_poz(u, R):
        X = s.kare(Vs, PI, u); return (X - cs) @ R.T
    def kare(u, R, kay=0.0, ek=None):
        Xs = sac_poz(u, R); dy = BENCH_Y - Xs[:, 1].min()
        X = poz(u, R); X[:, 1] += dy; X[:, 0] += FAB[0] + kay; X[:, 2] += FAB[2]
        if ek is not None: X = X + ek
        return X
    u_duz = {i: 1.0 for i in range(nb)}
    e_ = (Q @ np.asarray(eks, float))
    kar.append(kare(u_duz, Q, 0.0, -e_ * 30.0))          # 0: 30 mm geride (pres zımbası ekseninde)
    kar.append(kare(u_duz, Q, 0.0))                       # 1: deliğinde
    u = dict(u_duz)
    for bi in range(nb):
        for f in np.linspace(1, 0, 7)[1:]:
            u[bi] = f; kar.append(kare(dict(u), Q))
    if not np.allclose(Q, I3):
        for f in np.linspace(0, 1, 7)[1:]: kar.append(kare({}, G.slerp_R(Q, I3, f)))
    cp = merkez(pa)
    ofs0 = ofs_s.copy()                                   # PEM sacla aynı öteleme (son konum sacla birlikte)
    basla(pa, ofs0, tg)
    FRAMES[pa] = [X - (cp + ofs0) - (Vp - cp) for X in kar]
    # zaman: 0→1 presleme, sonra sacın büküm / çevirme segmentleriyle aynı (sacın seg listesi henüz yazılmadı → uret sonunda eşlenir)
    MF[pa] = dict(seg=[[round(tg, 3), round(tg + 0.9, 3), 0, 1]], bagli=sac_ad)
    vurgu([pa], tg + 0.6, tg + 1.4)


def pem_seg_esle():
    """PEM'in büküm / çevirme segmentleri = sacınınkiler (kare indisleri: sacın k ↔ pem k (sacın 0. karesi kayma, 1. düz))"""
    for pa, d in MF.items():
        if 'bagli' not in d: continue
        sg = MF[d['bagli']]['seg'][1:]                     # sacın kayma segmenti hariç
        d['seg'] += [[a_, b_, k0, k1] for a_, b_, k0, k1 in sg]


# ---------------------------------------------------------------- yardımcı: bağlantı elemanı kendi ekseninde
def tak(ad, t0, sure=0.7, yol=None):
    e_ = EL[ad]['eks']; L = EL[ad]['yol'] if yol is None else yol
    basla(ad, -e_ * L, t0); git(ad, np.zeros(3), t0, sure); vurgu([ad], t0 + sure * 0.6, t0 + sure + 0.6)
    return t0 + sure


def kaynak_yap(ad, t0, sure=0.9):
    basla(ad, np.zeros(3), t0); ISTISNA.add(ad); VU[ad].append([round(t0, 3), round(t0 + sure + 0.8, 3)])
    MF[ad] = dict(buyu=[round(t0, 3), round(t0 + sure, 3)])
    return t0 + sure


# ---------------------------------------------------------------- kamera noktaları (m)
K_URT = ([2.95, 1.05, 1.55], [2.55, 0.43, 0.56])
K_URT_YAKIN = ([2.78, 0.78, 1.05], [2.47, 0.44, 0.56])
K_TEZ = ([2.62, 1.12, 1.95], [1.77, 0.43, 0.62])
K_TEZ_SOL = ([1.95, 0.78, 1.45], [1.55, 0.45, 0.62])
K_ARKA = ([2.10, 0.98, 0.42], [1.56, 0.46, -0.70])
K_ARKA_YAKIN = ([1.72, 0.62, -0.42], [1.49, 0.45, -0.77])
K_RAY = ([2.35, 0.95, 1.05], [1.70, 0.44, -0.33])
K_VIDA = ([1.86, 0.63, 0.22], [1.45, 0.445, -0.33])
K_SOL_ON = ([1.80, 0.70, 0.45], [1.47, 0.47, -0.05])
K_SUR = ([3.05, 1.15, 1.85], [1.75, 0.44, 0.15])
K_SON = ([2.55, 0.92, 1.30], [1.76, 0.44, -0.22])
K_GENEL = ([3.6, 1.6, 2.6], [2.3, 0.42, 0.25])

Y_SAFE = 680.0
DR = np.array([0.0, 0.0, 900.0])           # çekmece montaj tezgâhında (son konumdan +z 900)


def raf_kaldir(ad, t0, hedef_ofs=None, yer=None):
    """üretim noktasından hazır rafına (kaldır → taşı → indir)"""
    c = merkez(ad); o = CUR[ad].copy(); dy = Y_SAFE - (P[ad]['V'][:, 1].min() + o[1])
    yr = raf_yeri(ad) if yer is None else yer
    hedef = np.array([yr[0] - c[0], o[1], yr[2] - c[2]])
    return yolu([ad], [o + [0, dy, 0], hedef + [0, dy, 0], hedef], t0, hiz=900.0, enaz=0.3)


# =====================================================================================================================
# PLAN (plan_v2.md ile birebir)
# =====================================================================================================================
KAM.append([0.0, K_GENEL[0], K_GENEL[1]])
t = 0.6
TEZ_UZAK = np.array([0.0, 0.0, 1150.0])
CUR['tezgah'] = -TEZ_UZAK.copy(); GOR['tezgah'] = 0.0          # montaj tezgâhı başta dolabın önünde; çekmece sürülünce +z 1150 kayar


def tezgaha(ad_l, ust=60.0, t0=None, hiz=900.0, grup=None, yan=(0, 0, 0)):
    """raftan / üretimden montaj tezgâhına (çekmecenin yerine): kaldır → üstüne → (yan) → indir"""
    grup = grup or [ad_l]; o = CUR[ad_l].copy(); dy = Y_SAFE - (P[ad_l]['V'][:, 1].min() + o[1])
    hedef = DR.copy(); yan = np.asarray(yan, float)
    nok = [o + [0, dy, 0], [hedef[0] + yan[0], o[1] + dy, hedef[2] + yan[2]], hedef + yan + [0, ust, 0], hedef + yan, hedef]
    return yolu(grup, nok, t0, hiz=hiz)


def rafa(ad_l, yer, t0, grup=None, hiz=900.0):
    grup = grup or [ad_l]; c = merkez(ad_l); o = CUR[ad_l].copy(); dy = Y_SAFE - (P[ad_l]['V'][:, 1].min() + o[1])
    h = np.array([yer[0] - c[0], BENCH_Y - P[ad_l]['V'][:, 1].min(), yer[2] - c[2]])
    return yolu(grup, [o + [0, dy, 0], [h[0], o[1] + dy, h[2]], h], t0, hiz=hiz, enaz=0.3)


def dolaba(ad_l, son_yaklasim, t0, hiz=650.0, grup=None):
    """raftan dolaba: kaldır → önde (arka yüzü z 200) hizala → içeri (−z) → son yaklaşım (vektör, son konuma göre)"""
    grup = grup or [ad_l]
    o = CUR[ad_l].copy(); son = np.asarray(son_yaklasim, float)
    dy = Y_SAFE - (P[ad_l]['V'][:, 1].min() + o[1])
    zon = 200.0 - (P[ad_l]['V'][:, 2].min())
    on = np.array([son[0], son[1], max(zon, son[2])])
    return yolu(grup, [o + [0, dy, 0], [on[0], o[1] + dy, on[2]], on, son, np.zeros(3)], t0, hiz=hiz)


KUCUK = [(x_, 0.0, z_) for z_ in (830.0, 940.0) for x_ in (2860.0, 2990.0, 3120.0, 3250.0, 3380.0, 3510.0)]
# ---------------- BÖLÜM 1 · ÜRETİM (küçük sac parçalar) ----------------
adim('Üretim: kızak köşebentleri (eklendi)',
     'Kızak bağlantı köşebendi 1,5 mm × 4: lazerde açınım (yatay kolda Ø4,5), abkantta dik kol 90° bükülür. Modelde kızak ile lama arasında bağ yoktu (yalnız 1 mm temas) — eklendi.',
     'köşebent × 4 · 1 büküm', K_URT)
for k in KOSE:
    t = uret(k['ad'], t, 'Köşebent %s-%s' % ('sol' if k['yan'] == 'sol' else 'sağ', k['ad'][-1]), sure_bukum=0.7); t = rafa(k['ad'], KUCUK.pop(0), t) + 0.05
adim('Üretim: motor braketi · sensör plakası',
     'Motor braketi 3 mm: lazerde göbek deliği Ø22,5, flanş kolunda 4 × M3 havşa (Ø31), tabanda 2 × M5 havşa; abkantta flanş kolu 90° bükülür. Sensör plakası 2 mm düz, 2 × Ø4,5.',
     'motor braketi (1 büküm) · sensör plakası (düz)', K_URT_YAKIN)
t = uret('motor_braketi', t, 'Motor braketi'); t = rafa('motor_braketi', KUCUK.pop(0), t) + 0.1
t = uret('sensor_plakasi', t, 'Sensör plakası'); t = rafa('sensor_plakasi', KUCUK.pop(0), t) + 0.1
adim('Üretim: avara kolu · sensör laması · kaynak',
     'Avara kolu 2 mm: lazer (ön flanşta 2 × Ø3,3 perçin deliği) → abkant: ön flanş, üst flanş. Sensör laması 2 mm: tek büküm (L). Kol kulağı lamaya TIG ile kaynaklanır, avara mili kola saplama kaynağıyla tutturulur.',
     'avara kolu (2 büküm) · sensör laması (1 büküm) · avara mili · TIG + saplama kaynağı', K_URT_YAKIN)
AV_YER = np.array([2780.0, 0.0, -230.0])
t = uret('avara_kolu', t, 'Avara kolu')
t = rafa('avara_kolu', AV_YER, t) + 0.05
hedef_k = CUR['avara_kolu'].copy()
t = uret('sensor_lamasi', t, 'Sensör laması')
o_l = CUR['sensor_lamasi'].copy(); dy = Y_SAFE - (P['sensor_lamasi']['V'][:, 1].min() + o_l[1])
t = yolu(['sensor_lamasi'], [o_l + [0, dy, 0], [hedef_k[0] + 60, o_l[1] + dy, hedef_k[2]], hedef_k + [60, -30, 0], hedef_k + [0, -30, 0], hedef_k], t, hiz=900) + 0.1
olay(t - 0.8, 'Sensör laması kol kulağının altına (alttan)')
basla('avara_mili', hedef_k + [60, 0, 0], t); t = yolu(['avara_mili'], [hedef_k], t, hiz=200); vurgu(['avara_mili'], t - 0.3, t + 0.6)
for a in ('kaynak_avara', 'kaynak_avara_mili'):
    kaynak_yap(a, t); CUR[a] = hedef_k.copy()
olay(t, 'TIG: kol kulağı ↔ sensör laması · saplama kaynağı: avara mili ↔ kol'); t += 1.3
AVARA = ['avara_kolu', 'sensor_lamasi', 'avara_mili', 'kaynak_avara', 'kaynak_avara_mili']
# ---------------- BÖLÜM 2 · RAY ÜNİTESİ ----------------
adim('Ray ünitesi: iç eleman ayrılır',
     'Accuride DZ3832-0700 ray dış + ara + iç eleman bir arada gelir. İç eleman (kızak) kilit dili basılarak ray ekseni boyunca öne çekilip ayrılır; çekmeceye takılacak.',
     'ray ünitesi sol / sağ (katalog) · iç eleman ayrılır', K_URT)
RAY_YER = {'sol': np.array([2950.0, 0.0, -330.0]), 'sag': np.array([3050.0, 0.0, -330.0])}
for yan in ('sol', 'sag'):
    grp = ['sabit_ray_' + yan, 'ara_ray_' + yan, 'kizak_' + yan]
    c_ = merkez('sabit_ray_' + yan); o_ = np.array([RAY_YER[yan][0] - c_[0], BENCH_Y - P['sabit_ray_' + yan]['V'][:, 1].min(), RAY_YER[yan][2] - c_[2]])
    for a in grp: basla(a, o_ + [0, 260.0, 0], t)
    t = yolu(grp, [o_], t, hiz=600) + 0.1
    t = yolu(['kizak_' + yan], [CUR['kizak_' + yan] + [0, 0, 720]], t, hiz=600); olay(t - 1.2, 'İç eleman (kızak) ray ekseni boyunca öne çekilip ayrılır'); t += 0.15
# ---------------- BÖLÜM 3 · DOLAP İÇİ ----------------
adim('Motor braketi arka duvara',
     'Motor braketi raftan alınır, ön çerçeve açıklığından bölmeye girer, tabanı arka duvara oturur: 2 × DIN 7991 M5 × 6 havşa vida arka iç sacdaki PEM SP-M5\'lere. Vidalar önce: motor takılınca taban vidaları motorun altında kalır.',
     'motor braketi · 2 × DIN 7991 M5 × 6 → PEM SP-M5 (arka iç sac)', K_ARKA)
t = dolaba('motor_braketi', (0, 0, 25), t); vurgu(['motor_braketi'], t - 0.4, t + 0.5)
kam(t, K_ARKA_YAKIN)
for i in (1, 2): t = tak('vida_braket_%d' % i, t, 0.8) + 0.1
olay(t - 1.8, 'Motor braketi: 2 × DIN 7991 M5 × 6 → PEM SP-M5')
t += 0.3
adim('Motor braketine (ekseni boyunca)',
     'Step motor önden girer, ekseni boyunca −x yönünde sürülür: redüktör göbeği braketin Ø22,5 deliğine, mil karşı tarafa geçer. 4 × DIN 7991 M3 × 6 havşa vida kasnak tarafından redüktör yüzündeki M3 dişlere. Sütunun dikey kablo kanalı tahrikler takıldıktan sonra gelir (bu animasyonda yok).',
     'step motor · 4 × DIN 7991 M3 × 6', K_ARKA)
basla('motor', np.array([24.0, Y_SAFE - P['motor']['V'][:, 1].min(), 980.0]), t)
t = yolu(['motor'], [[24.0, 0, 980.0], [24.0, 0, 0], [0, 0, 0]], t, hiz=600); vurgu(['motor'], t - 0.5, t + 0.5); olay(t - 1.0, 'Motor ekseni boyunca braketine sürülür')
kam(t, K_ARKA_YAKIN)
for i in range(1, 5): t = tak('vida_motor_%d' % i, t, 0.6) + 0.05
olay(t - 2.6, 'Motor: 4 × DIN 7991 M3 × 6 (redüktör yüzü)')
adim('Motor kasnağı · setskur',
     'GT3 motor kasnağı mil ekseninde (+x) mile geçer; DIN 913 M3 setskur önden milin düz yüzüne sıkılır. Sol ray henüz yok: kasnak soldan geçer.',
     'GT3 motor kasnağı · DIN 913 M3 × 4', K_ARKA_YAKIN)
basla('arka_kasnak', np.array([-14.5, Y_SAFE - P['arka_kasnak']['V'][:, 1].min(), 980.0]), t)
t = yolu(['arka_kasnak'], [[-14.5, 0, 980.0], [-14.5, 0, 0], [0, 0, 0]], t, hiz=600); vurgu(['arka_kasnak'], t - 0.4, t + 0.4)
t = tak('setskur', t, 0.6) + 0.2
adim('Sensör plakası (model açığı)',
     'Modeldeki sensör plakası arka duvarda, kablo kanalının (ELK_IC) içinde kalıyor ve sensör lamasına bağlı değil (lama ucu 32 mm önde biter). Bağlantı yapılmadı: plaka kaldırılmalı ya da lama arka duvara uzatılıp bu plakayla vidalanmalı — Kemal kararı.',
     'sensör plakası — bağlantısız (açık)', K_ARKA_YAKIN)
t = dolaba('sensor_plakasi', (0, 0, 20), t); vurgu(['sensor_plakasi'], t - 0.4, t + 0.6)
olay(t - 0.8, 'Sensör plakası — MODEL AÇIĞI: kablo kanalının içinde, lamaya bağlı değil (bağlantı yapılmadı)')
adim('Ray üniteleri bölme saclarına',
     'Sol ve sağ ray ünitesi (dış + ara eleman) önden çerçeve açıklığından girer, yana kayıp bölme sacına yaslanır. Her ray 3 × DIN 7991 M5 × 6 havşa vidayla, ara elemanın erişim deliklerinden, bölmedeki PEM SP-M5\'lere vidalanır.',
     'ray ünitesi sol / sağ · 6 × DIN 7991 M5 × 6 → PEM SP-M5', K_RAY)
for yan, sx in (('sol', 10.0), ('sag', -9.0)):
    t = dolaba('sabit_ray_' + yan, (sx, 0, 0), t, grup=['sabit_ray_' + yan, 'ara_ray_' + yan], hiz=800) + 0.05
kam(t, K_VIDA)
for k_ in (1, 2, 3):
    EL[VIDA_RAY[k_ - 1]] = dict(eks=np.array([-1.0, 0, 0]), yol=40.0); EL[VIDA_RAY[k_ + 2]] = dict(eks=np.array([1.0, 0, 0]), yol=40.0)
    t0 = t; tak(VIDA_RAY[k_ - 1], t0, 0.6); t = tak(VIDA_RAY[k_ + 2], t0, 0.6) + 0.1
olay(t - 2.1, 'Ray vidaları: 3 + 3 × DIN 7991 M5 × 6, kendi eksenlerinde')
adim('Avara ünitesi · perçin · avara kasnağı · reed',
     'Kaynaklı avara ünitesi (kol + sensör laması + mil) 21 mm alçaktan açıklıktan girer, içeride sola kayar, yükselip ön flanşıyla çerçevenin arkasına oturur: 2 × kör perçin Ø3,2 önden. GT3 avara kasnağı mil ekseninde (−x) mile geçer (mil ucunda E segman payı modelde yok — açık). İki reed sensör lamanın altına yandan oturur (bağlantı deliği modelde yok — açık).',
     'avara ünitesi · 2 × kör perçin Ø3,2 · GT3 avara kasnağı · reed × 2', K_SOL_ON)
o_a = CUR['avara_kolu'].copy()
zon = 200.0 - P['sensor_lamasi']['V'][:, 2].min()
t = yolu(AVARA, [o_a + [0, Y_SAFE - 480, 0], [0.6, o_a[1] + Y_SAFE - 480, zon], [0.6, -21.0, zon], [0.6, -21.0, -0.4], [0, -21.0, -0.4], [0, 0, -0.4], [0, 0, 0]], t, hiz=700)
vurgu(['avara_kolu', 'sensor_lamasi'], t - 0.4, t + 0.5)
for i in (1, 2): t = tak('percin_%d' % i, t, 0.6) + 0.05
olay(t - 1.3, 'Avara ünitesi: 2 × kör perçin Ø3,2 (çerçeve önünden)')
basla('avara_kasnagi', np.array([40.0, Y_SAFE - P['avara_kasnagi']['V'][:, 1].min(), 200.0 + 18.0]), t)
t = yolu(['avara_kasnagi'], [[40.0, 0, 218.0], [40.0, 0, 0], [0, 0, 0]], t, hiz=400); vurgu(['avara_kasnagi'], t - 0.4, t + 0.5)
for a in ('reed_arka', 'reed_on'):
    basla(a, np.array([20.0, 0, 0]), t); git(a, np.zeros(3), t, 0.7); vurgu([a], t + 0.4, t + 1.1)
t += 0.9
# ---------------- BÖLÜM 4 · ÇEKMECE KUTUSU (üretim → montaj tezgâhı) ----------------
adim('Kutu sacları: lazer → tezgâh → TIG',
     'Lazerde 5 düz sac (AISI 304): taban 2 mm, iki yan, arka, ön 1 mm. Taban montaj tezgâhına konur; yanlar tabanın üstüne oturup iç köşeden TIG ile kaynaklanır; arka ve ön iki yanın arasına girip tabana ve yanlara kaynaklanır.',
     'kutu tabanı 2 · yan sol / sağ 1 · arka 1 · ön 1 · 4 TIG dikişi', K_URT)
t = uret('kutu_taban', t, 'Kutu tabanı 2 mm'); kam(t, K_TEZ); t = tezgaha('kutu_taban', 40, t) + 0.1
kam(t, K_URT)
for ad, nm, yn in (('kutu_yan_sol', 'Kutu sol yanı', 'sol'), ('kutu_yan_sag', 'Kutu sağ yanı', 'sag')):
    t = uret(ad, t, nm); kam(t, K_TEZ); t = tezgaha(ad, 80, t) + 0.05
    k_ = 'kaynak_kutu_yan_' + yn; kaynak_yap(k_, t); CUR[k_] = DR.copy(); olay(t, 'TIG: %s yan ↔ taban (iç köşe)' % ('sol' if yn == 'sol' else 'sağ')); t += 1.0
    kam(t, K_URT)
for ad, nm, k_ in (('kutu_arka', 'Kutu arkası', 'kaynak_kutu_arka'), ('kutu_on', 'Kutu önü', 'kaynak_kutu_on')):
    t = uret(ad, t, nm); kam(t, K_TEZ); t = tezgaha(ad, 80, t) + 0.05
    kaynak_yap(k_, t); CUR[k_] = DR.copy(); olay(t, 'TIG: %s ↔ taban + iki yan' % ('arka' if 'arka' in ad else 'ön')); t += 1.0
    kam(t, K_URT)
adim('Kızak lamaları (kesim boyu, M4 dişli) → punta',
     'Lamalar 6 × 17,3 lamadan 616 boyda kesilir, köşebent vidaları için 2 × M4 dişli kör delik açılır; kutunun iki yanına puntalanır (4 nokta).',
     'lama sol / sağ · 2 × M4 dişli · punta 4 + 4', K_URT_YAKIN)
for yan, sx in (('sol', -70.0), ('sag', 70.0)):
    t = uret('lama_' + yan, t, 'Kızak laması %s' % ('sol' if yan == 'sol' else 'sağ')); kam(t, K_TEZ_SOL)
    t = tezgaha('lama_' + yan, 0, t, yan=(sx, 0, 0)) + 0.05
    kaynak_yap('punta_lama_' + yan, t, 0.6); CUR['punta_lama_' + yan] = DR.copy(); olay(t, 'Punta: lama ↔ kutu yanı (4 nokta)'); t += 0.8
    kam(t, K_URT_YAKIN)
adim('Ön bağlantı braketleri: abkant → punta',
     'Her braket 2 mm sacdan açınım olarak kesilir (flanşta 2 × Ø5,5), abkantta önce yan kol, sonra ön flanş 90° bükülür; kutu önüne puntalanır.',
     'ön braket sol / sağ · 2 büküm · punta 2 + 2', K_URT_YAKIN)
for yan in ('sol', 'sag'):
    t = uret('on_braket_' + yan, t, 'Ön braket %s' % ('sol' if yan == 'sol' else 'sağ')); kam(t, K_TEZ)
    t = tezgaha('on_braket_' + yan, 0, t, yan=(0, 0, 60)) + 0.05
    kaynak_yap('punta_braket_' + yan, t, 0.6); CUR['punta_braket_' + yan] = DR.copy(); olay(t, 'Punta: braket ↔ kutu önü'); t += 0.8
    kam(t, K_URT_YAKIN)
adim('Kayış çenesi: alt gövde TIG → kutuya TIG · üst çene · tepsi',
     'Alt çene, ara parça ve kol lamadan kesilir, TIG ile birleşir; alt gövde kutunun sol yanına TIG ile kaynaklanır. Üst çene (mıknatıs ayaklı) rafa — kayış takılınca M3 ile bağlanır. Silikon tepsi kutuya serbest oturur.',
     'çene alt gövde (TIG) · kutuya TIG · üst çene · silikon tepsi', K_URT_YAKIN)
t = uret('cene_alt', t, 'Kayış çenesi alt gövde')
kaynak_yap('kaynak_cene', t); CUR['kaynak_cene'] = CUR['cene_alt'].copy(); olay(t, 'TIG: kol ↔ alt çene · ara parça ↔ alt çene'); t += 1.0
kam(t, K_TEZ_SOL); t = tezgaha('cene_alt', 0, t, grup=['cene_alt', 'kaynak_cene'], yan=(-40, 0, 0)) + 0.05
kaynak_yap('kaynak_cene_kutu', t); CUR['kaynak_cene_kutu'] = DR.copy(); olay(t, 'TIG: çene kolu ↔ kutu sol yanı'); t += 1.0
kam(t, K_URT_YAKIN)
t = uret('cene_ust', t, 'Kayış çenesi üst'); t = rafa('cene_ust', KUCUK.pop(0), t) + 0.1
kam(t, K_TEZ)
basla('silikon_tepsi', DR + np.array([0, 160.0, 0]), t); git('silikon_tepsi', DR, t, 1.0); olay(t, 'Silikon tepsi kutuya serbest oturur'); t += 1.2
# ---------------- BÖLÜM 5 · ÇEKMECE TAMAMLANIR + DOLABA ----------------
adim('Tezgâh: köşebentler · kızaklar',
     'Köşebentler lamanın üstüne ISO 7380 M4 × 6 ile vidalanır (lamadaki M4 dişe). Kızaklar (iç eleman) köşebentlerin dik koluna oturur ve puntalanır (ÖNERİ: modelde kızak ile lama arasında bağ yoktu — Kemal kararı).',
     'köşebent × 4 + 4 × ISO 7380 M4 × 6 · kızak × 2 (punta 2 × 2)', K_TEZ_SOL)
for k in KOSE:
    t = tezgaha(k['ad'], 40, t, hiz=1100)
    a = 'vida_' + k['ad']; basla(a, DR + np.array([0, 30.0, 0]), t); git(a, DR, t, 0.5); vurgu([a], t + 0.3, t + 1.0); t += 0.6
olay(t - 4.5, 'Köşebentler lamalara: ISO 7380 M4 × 6')
for yan, sx in (('sol', -1.0), ('sag', 1.0)):
    t = tezgaha('kizak_' + yan, 0, t, hiz=1000, yan=(sx * 40, 0, 0))
    for k in KOSE:
        if k['yan'] == yan: kaynak_yap('punta_' + k['ad'], t, 0.5); CUR['punta_' + k['ad']] = DR.copy()
    olay(t, 'Kızak köşebentlere puntalanır (öneri)'); t += 0.7
CEKMECE = (['kutu_taban', 'kutu_yan_sol', 'kutu_yan_sag', 'kutu_arka', 'kutu_on', 'kaynak_kutu_yan_sol', 'kaynak_kutu_yan_sag', 'kaynak_kutu_arka', 'kaynak_kutu_on',
            'lama_sol', 'lama_sag', 'punta_lama_sol', 'punta_lama_sag', 'kizak_sol', 'kizak_sag', 'cene_alt', 'kaynak_cene', 'kaynak_cene_kutu',
            'on_braket_sol', 'on_braket_sag', 'punta_braket_sol', 'punta_braket_sag', 'silikon_tepsi']
           + [k['ad'] for k in KOSE] + ['vida_' + k['ad'] for k in KOSE] + ['punta_' + k['ad'] for k in KOSE])
adim('Çekmece raylara sürülür',
     'Çekmece tezgâhtan ray ekseni boyunca, düz bir çizgide içeri sürülür: kızaklar ara elemanların bilyalı kafesine geçer. Çekmece arka konumda durur; montaj tezgâhı çekilir.',
     'çekmece grubu · 900 mm sürme · ray ekseni z', K_SUR)
t = yolu(CEKMECE, [np.zeros(3)], t, hiz=170.0) + 0.3
olay(t - 5.6, 'Çekmece ray ekseni boyunca sürülür — kızak ara elemanın içinde')
git('tezgah', np.zeros(3), t, 2.0); olay(t, 'Montaj tezgâhı (tekerlekli) öne çekilir'); t += 2.2
adim('Kayış · üst çene · mıknatıs',
     'GT3 kayış motor kasnağı ile avara kasnağına sarılır, üst kolu alt çenenin üstüne yatar. Üst çene üstten gelir: 2 × ISO 7380 M3 × 10 + altta 2 × ISO 4032 M3. Mıknatıs ayağa oturur (57135\'in montaj yüzü modelde yok — açık).',
     'GT3 kayış (sarılır) · üst çene · 2 × ISO 7380 M3 × 10 · 2 × ISO 4032 M3 · mıknatıs', K_ARKA)
basla('kayis', np.zeros(3), t); ISTISNA.add('kayis'); MF['kayis'] = dict(buyu=[round(t, 3), round(t + 1.8, 3)]); olay(t, 'GT3 kayış kasnaklara sarılır (istisna: sarılarak uzar)'); t += 2.0
t = dolaba('cene_ust', (0, 20, 0), t); vurgu(['cene_ust'], t - 0.4, t + 0.4)
kam(t, K_ARKA_YAKIN)
for i in (1, 2): t = tak('vida_cene_%d' % i, t, 0.5); t = tak('somun_cene_%d' % i, t, 0.5) + 0.05
basla('miknatis', np.array([0, 22.0, 0]), t); git('miknatis', np.zeros(3), t, 0.6); vurgu(['miknatis'], t + 0.3, t + 1.0); t += 0.8
# ---------------- BÖLÜM 6 · ÖN KAPAK ----------------
adim('Üretim: ön kapak (8 büküm) · iç panel + PEM',
     'Dış kabuk 1,5 mm: lazer → abkant 8 büküm (dört kenar, sonra dört arka dönüş). İç panel 1,0 mm: 4 delik, PEM FHS-M5-10 saplamalar preslenir. İç panel kabuğun arkasına yerleşir (fitil kanalı 6,4 arada); modelde PU köpük yok.',
     'dış kabuk 1,5 (8 büküm) · iç panel 1,0 · 4 × PEM FHS-M5-10', K_URT)
t = uret('kapak_dis', t, 'Kapak dış kabuğu', sure_bukum=0.75)
KP_YER = np.array([3000.0, 0.0, -300.0])
t = rafa('kapak_dis', KP_YER, t) + 0.1
h_d = CUR['kapak_dis'].copy()
PEMK = [('pem_kapak_%s_%d' % (k_, i + 1), 0, (0, 0, -1)) for k_ in STUD for i in range(2)]
t = uret('kapak_ic', t, 'Kapak iç paneli', pemler=PEMK, sure_bukum=0.75)
o_i = CUR['kapak_ic'].copy(); grp_i = ['kapak_ic'] + [p_[0] for p_ in PEMK]
dy = Y_SAFE - (P['kapak_ic']['V'][:, 1].min() + o_i[1])
t = yolu(grp_i, [o_i + [0, dy, 0], [h_d[0], o_i[1] + dy, h_d[2] - 260], h_d + [0, 0, -260], h_d], t, hiz=800) + 0.2
KAPAK = ['kapak_dis'] + grp_i
olay(t - 0.6, 'İç panel kabuğun arkasına yerleşir — saplamalar arkaya bakar')
adim('Ön kapak · fitil · somunlar',
     'Fitil (silikon) kapağın kanalına arkadan bastırılır. Kapak dolabın önüne gelir; PEM saplamaları braket flanşlarındaki deliklerden geçer. Her saplamaya U braketin açık yanından pul (DIN 125 M5) ve somun (ISO 4032 M5) takılır.',
     'fitil · ön kapak (saplamalar) · 4 × DIN 125 M5 · 4 × ISO 4032 M5', K_SON)
o_k2 = CUR['kapak_dis'].copy()
basla('on_panel', o_k2 + np.array([0, 0, -120.0]), t); t = yolu(['on_panel'], [o_k2], t, hiz=200); vurgu(['on_panel'], t - 0.4, t + 0.5)
olay(t - 0.8, 'Fitil kapak kanalına bastırılır')
KAPAK = KAPAK + ['on_panel']
o_k3 = CUR['kapak_dis'].copy(); dy = Y_SAFE - (P['kapak_dis']['V'][:, 1].min() + o_k3[1])
t = yolu(KAPAK, [o_k3 + [0, dy, 0], [0, o_k3[1] + dy, 400.0], [0, 0, 400.0], [0, 0, 0]], t, hiz=650); vurgu(['kapak_dis'], t - 0.5, t + 0.5)
olay(t - 1.0, 'Kapak: saplamalar braket flanşından geçer')
kam(t, K_SOL_ON)
for k_ in STUD:
    sx = 1.0 if k_ == 'sol' else -1.0
    for i in (1, 2):
        for tip, dz in (('pul', 11.35), ('somun', 6.65)):
            a = '%s_kapak_%s_%d' % (tip, k_, i)
            basla(a, np.array([sx * 30.0, 0, -dz]), t); git(a, np.array([0, 0, -dz]), t, 0.35); git(a, np.zeros(3), t + 0.35, 0.4); vurgu([a], t + 0.5, t + 1.1); t += 0.8
olay(t - 6.4, 'Saplamalara pul + somun (U braketin açık yanından)')
adim('Kablolar',
     'Reed sensör kabloları ve motor kablosu bölmedeki kablo kanalı boyunca arkaya çekilir (sütunun dikey kanalı tahrikler bittikten sonra).',
     'reed sensör kabloları · motor kablosu', K_ARKA)
for a in ('kablo_sensor', 'kablo_motor'):
    basla(a, np.zeros(3), t); ISTISNA.add(a); MF[a] = dict(buyu=[round(t, 3), round(t + 2.2, 3)])
olay(t, 'Kablolar kanal boyunca çekilir (istisna)'); t += 2.6
KAM.append([round(t, 3), K_SON[0], K_SON[1]]); t += 2.4
TOPLAM = round(t, 2)
for i, a in enumerate(ADIM): a['t1'] = ADIM[i + 1]['t0'] if i + 1 < len(ADIM) else TOPLAM
# tüm parçalar son konumda mı
for a in P:
    if P[a]['tur'] == 'cevre': continue
    assert a in CUR, ('zaman çizelgesinde yok', a)
    assert np.linalg.norm(CUR[a]) < 1e-6, ('son konumda değil', a, CUR[a])
print('süre %.1f s · adım %d' % (TOPLAM, len(ADIM)), flush=True)
pickle.dump(dict(P=P, HAR=HAR, GOR=GOR, MF=MF, FRAMES=FRAMES, VU=VU, ISTISNA=ISTISNA, ADIM=ADIM, OLAY=OLAY, KAM=KAM, ACN=ACN, TOPLAM=TOPLAM,
                 KIYAS=KIYAS, EKLENEN_CEVRE=EKLENEN_CEVRE, DELIK_ACILAN=DELIK_ACILAN, EL={k: dict(eks=v['eks'].tolist(), yol=v['yol']) for k, v in EL.items()},
                 SAC={a: dict(t=SAC[a].t, bukum=[dict(no=b['no'], panel=b['panel'], p=b['p'].tolist(), a=b['a'].tolist(), aci=b['aci'], sg=b['sg'], ack=b['aciklama']) for b in SAC[a].bukum],
                              panel=[p_['ad'] for p_ in SAC[a].panel]) for a in SAC}, KAYNAK=KAY, YAPI={a: dict(ac=YAPI[a]['ac'], tip=YAPI[a]['tip']) for a in YAPI}),
            open('plan_v2.pkl', 'wb'))
