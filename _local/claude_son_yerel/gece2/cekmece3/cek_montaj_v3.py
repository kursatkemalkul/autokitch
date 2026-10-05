# -*- coding: utf-8 -*-
"""TEK ÇEKMECE MONTAJ ANİMASYONU v3 (Kemal geri bildirimi: birleşimler net, her delik + eleman, satın alınan ürün tek parça, tezgâh kutuları yok; model adım 44 = hat3_v9l) — v2 notu:
TEK ÇEKMECE MONTAJ ANİMASYONU v2 (B · K2 sütunu · 3. sıra = CEK_K2_lahm_3) · 4 Eki 2026 · yerel
MONTAJ_ANIMASYON_KURALLARI.md (19 madde) — plan_v2.md ile birebir:
  ÜRETİM: her sac parça DÜZ AÇINIM (lazer: kontur + delik) → ABKANT (büküm tek tek, gerçek sıra) → PEM presleme → hazır rafı · lamalar kesim boyunda + delikli
  MONTAJ: her vida / perçin / PEM / somun / pul tek tek kendi ekseninde · kaynak dikişleri / punta noktaları birleşme anında · ray ünitesi katalog bütünü
Çıktı: otonom/hat3d/v3/cekmece_montaj/cekmece_montaj.glb (morph hedefli: büküm kareleri) + .json · denetim → sonuc_v2.json"""
import sys, os, json, pickle, time, math
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
sys.path.insert(0, os.path.join(HERE, '..', 'adim6')); sys.path.insert(0, os.path.join(HERE, '..', 'cekmece')); sys.path.insert(0, HERE); sys.stdout.reconfigure(encoding='utf-8')
import yol_denetim as Y
import v2geo as G
import cek3geo as C
Y.ADIM = 0.002
W = r'C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH_COORDINATION\worktrees\claude-hat3-v8'
OUT = os.path.join(W, 'otonom', 'hat3d', 'v3', 'cekmece_montaj')
M0 = pickle.load(open('parca3.pkl', 'rb'))         # v3 çıkarımı: hat3_v9l (adım 44 sonrası) — model parçaları + çevre (metre)
M_ESKI = pickle.load(open(os.path.join(HERE, '..', 'cekmece', 'parca.pkl'), 'rb'))   # avara mili (adım 44 ile aynı işlem uygulanır)
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
for a in ('sabit_ray_sol', 'sabit_ray_sag', 'ara_ray_sol', 'ara_ray_sag', 'kizak_sol', 'kizak_sag', 'silikon_tepsi', 'on_panel',
          'kayis', 'kablo_sensor', 'kablo_motor'):
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
ekle('arka_kasnak', MM['arka_kasnak']['V'], MM['arka_kasnak']['F'], 'alu', 'mek', 'GT3 motor kasnağı 30 diş (katalog ürün · Ø8 göbek + radyal M3 setskur deliği)')
ekle('avara_kasnagi', MM['avara_kasnagi']['V'], MM['avara_kasnagi']['F'], 'alu', 'mek', 'GT3 avara kasnağı 30 diş · 2 × MR126-2RS (katalog ürün, tek parça)')
for Vb, Fb in bilesenler(M_ESKI['avara_kasnagi']['V'] * 1000.0, np.asarray(M_ESKI['avara_kasnagi']['F'])):
    if Vb[:, 1].max() - Vb[:, 1].min() < 20:                                      # eski mil → +1 mm + E segman yuvası (adım 44 ile birebir)
        Pm_ = Vb[Fb].copy(); uc_ = Pm_[..., 0].max(); Pm_[..., 0][np.abs(Pm_[..., 0] - uc_) < 0.01] += C.MIL_X1_YENI - C.MIL_X1
        u_, inv_ = np.unique(np.round(Pm_.reshape(-1, 3), 4), axis=0, return_inverse=True)
        mil_ = model_mf(u_, inv_.reshape(-1, 3)) - C.kes_segman_yuvasi(); AVARA_MILI = G.mesh(mil_)
# ray vidaları: model (adım 43) M5 × 6
VIDA_RAY = []
for s_ in ('sol', 'sag'):
    for k_ in (1, 2, 3):
        a = 'vida_%s_%d' % (s_, k_); ekle(a, MM[a]['V'], MM[a]['F'], 'baglanti', 'baglanti', 'DIN 7991 M5 × 6 A2 havşa'); VIDA_RAY.append(a)
# satın alınan sensörler (Littelfuse 59135 reed × 2, 57135 mıknatıs): adım 44 konumu, montaj yarıkları ile (tek parça ürün)
ekle_mf('reed_arka', C.geo_reed()['reed_arka'], 'sensor', 'mek', 'reed sensör Littelfuse 59135 (28,57 × 19,05 × 6,35 · 2 yarık Ø3,18) — kapalı konum')
ekle_mf('reed_on', C.geo_reed()['reed_on'], 'sensor', 'mek', 'reed sensör Littelfuse 59135 — açık konum')
ekle_mf('miknatis', C.geo_a1()['miknatis'], 'sensor', 'mek', 'mıknatıs Littelfuse 57135 (28,57 × 19,05 × 6,35 · 2 yarık)')

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
TEZ = (1520.0, 2010.0, 0.0, 421.5, 330.0, 900.0)                                 # montaj alanı (çekmece burada, havada — tezgâh gösterilmez)
URT = (2230.0, 3640.0, 0.0, 421.5, -760.0, 990.0)                                 # üretim alanı (lazer / abkant / PEM pres + hazır yerleri, havada)
EKLENEN_CEVRE = []
ARKA_PEM = C.ARKA_PEM

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
s = sac('motor_braketi', 3.0, RX(-90), ac='motor braketi 3 mm (lazer: göbek deliği · 2 × M5 havşa · 4 × M3 havşa)')
taban = G.fark(K((1481, 424.5, -790), (1524, 468.5, -787)), [G.silindir((1487.0, YC, ZC), (1, 0, 0), 18.2, 38.0, 64)] +
               [C.havsa((x_, y_, -787.0), (0, 0, -1), 'M5', 3.0) for x_, y_ in ARKA_PEM])
i0 = s.ekle('taban', taban)
dik = G.fark(K((1481, 424.5, -787), (1484, 468.5, -751.5)), [G.silindir((1480.0, YC, ZC), (1, 0, 0), 11.25, 5.0, 64)] +
             [C.havsa((1481.0, y_, z_), (1, 0, 0), 'M3', 3.0) for y_, z_ in M3PCD])
s.ekle('dik_kol', dik, i0, (1482.5, 0, -788.5), (0, 1, 0), 90, 'motor flanş kolu')
# ---- reed plakaları 2 mm (düz, lazer: 2 × Ø4,22 PEM deliği) → PEM CLS-M3-2 preslenir → sensör lamasına punta
RDG = C.geo_reed()
for k_ in ('arka', 'on'):
    s = sac('reed_plaka_' + k_, 2.0, RZ(-90), ac='reed plakası %s 2 mm (düz) · 2 × PEM CLS-M3-2' % ('arka' if k_ == 'arka' else 'ön'))
    s.ekle('plaka', RDG['reed_plaka_' + k_])
# ---- avara kolu 2 mm (2 büküm) + sensör laması L 2 mm (1 büküm) + avara mili (saplama kaynağı) → kaynaklı ünite
PERCIN = [(1457.5, 509.5), (1465.0, 509.5)]
s = sac('avara_kolu', 2.0, RZ(-90), ac='avara kolu 2 mm · ön flanş + üst flanş')
i0 = s.ekle('kol', K((1467.2, 438.5, -9), (1469.2, 503.5, 23)) + K((1467.2, 487.55, -29), (1469.2, 495.55, -9)))
s.ekle('on_flans', K((1454.5, 492.5, 21), (1467.2, 512.5, 23)), i0, (1468.2, 0, 22.0), (0, 1, 0), 90, 'ön flanş (çerçeveye)')
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
# ---- A1 (adım 44): kol (lama 3, kutuya TIG) · kol tablası 2,5 (kola TIG, 2 × Ø3,4) · mıknatıs kulağı 2 (tablaya TIG, 2 × PEM CLS-M3-2)
#      çene alt gövdesi (alt çene 2,5 + ara 1,2 · TIG) · üst çene 2,5 — ayrı blok, çekmece AÇIKKEN 2 × ISO 7380 M3 × 12 + 2 × ISO 4032 M3
A1G = C.geo_a1()
s = sac('kol', 3.0, RZ(-90), tip='lama', ac='kayış kolu 3 × 6,26 × 154 (lama, kesim boyu) — kutu sol yanına TIG'); s.ekle('kol', A1G['kol'])
s = sac('tabla', 2.5, I3, ac='kol tablası 2,5 (lazer, 2 × Ø3,4) — kola TIG'); s.ekle('tabla', A1G['tabla'])
s = sac('kulak', 2.0, RZ(-90), ac='mıknatıs kulağı 2 mm (lazer, 2 × Ø4,22) + 2 × PEM CLS-M3-2 — tablaya TIG'); s.ekle('kulak', A1G['kulak'])
s = sac('cene_alt', 2.5, I3, tip='lama', ac='çene alt gövdesi: alt çene 2,5 + ara parça 1,2 (TIG) · 2 × Ø3,4')
s.ekle('alt_cene', G.fark(K((1470.5, 457.95, -751.0), (1491.5, 460.45, -721.0)), [C.yd(C.JX, z_, 2.5, 460.45) for z_ in C.JZ]))
s.ekle('ara', G.fark(K((1477.5, 460.45, -751.0), (1491.5, 461.65, -721.0)), [C.yd(C.JX, z_, 1.2, 461.65) for z_ in C.JZ]))
s = sac('cene_ust', 2.5, I3, tip='lama', ac='üst çene 2,5 (2 × Ø3,4)'); s.ekle('ust_cene', A1G['cene_ust'])

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
# 4. BAĞLANTI ELEMANLARI (tek tek) — geometri cek3geo (ana model adım 44 ile aynı)
# =====================================================================================================================
EL = {}          # ad → dict(eks (giriş yönü birim), yol (mm, giriş öncesi uzaklık))
def el(ad, man, ac, eks, yol=30.0):
    EL[ad] = dict(eks=np.asarray(eks, float), yol=yol); ekle_mf(ad, man, 'baglanti', 'baglanti', ac)


MOG = C.geo_motor()
for i in (1, 2):
    el('vida_braket_%d' % i, MOG['vida_braket_%d' % i], 'DIN 7991 M5 × 6 A2 havşa', (0, 0, -1), 40)
for i in range(1, 5):
    el('vida_motor_%d' % i, MOG['vida_motor_%d' % i], 'DIN 7991 M3 × 6 A2 havşa', (1, 0, 0), 12)
el('setskur', MOG['setskur'], 'DIN 913 M3 × 4 A2 setskur', (0, 0, -1), 25)
for i in (1, 2):
    el('vida_cene_%d' % i, A1G['vida_cene_%d' % i], 'ISO 7380 M3 × 12 A2 (bombe başlı, imbus 2)', (0, -1, 0), 20)
    el('somun_cene_%d' % i, A1G['somun_cene_%d' % i], 'ISO 4032 M3 A2 somun', (0, 1, 0), 18)
    ekle_mf('pem_kulak_%d' % i, A1G['pem_kulak_%d' % i], 'baglanti', 'baglanti', 'PEM CLS-M3-2 (mıknatıs kulağına preslenir)')
    el('vida_miknatis_%d' % i, A1G['vida_miknatis_%d' % i], 'ISO 7380 M3 × 8 A2', (1, 0, 0), 25)
for k_ in ('arka', 'on'):
    for i in (1, 2):
        ekle_mf('pem_reed_%s_%d' % (k_, i), RDG['pem_reed_%s_%d' % (k_, i)], 'baglanti', 'baglanti', 'PEM CLS-M3-2 (reed plakasına preslenir)')
        el('vida_reed_%s_%d' % (k_, i), RDG['vida_reed_%s_%d' % (k_, i)], 'ISO 7380 M3 × 8 A2', (-1, 0, 0), 25)
el('e_segman', C.geo_avara()['e_segman'], 'DIN 6799 RS 5 E segman (A2)', (0, -1, 0), 20)
KOG = C.geo_kose()
for k in KOSE:
    el('vida_' + k['ad'], KOG['vida_' + k['ad']], 'ISO 7380 M4 × 6 A2', (0, -1, 0), 30)
for k_ in STUD:
    lo_ = np.array([1483.5, 428.5, 22.0]) if k_ == 'sol' else np.array([2028.5, 428.5, 22.0]); hi_ = lo_ + [15.0, 49.0, 17.0]
    for a_, m_ in C.geo_stud(k_, lo_, hi_).items():
        if a_.startswith('pem'): ekle_mf(a_, m_, 'baglanti', 'baglanti', 'PEM FHS-M5-10 saplama (kapak iç paneline preslenir)')
        elif a_.startswith('pul'): el(a_, m_, 'DIN 125 M5 A2 pul', (0, 0, 1), 0)
        else: el(a_, m_, 'ISO 4032 M5 A2 somun', (0, 0, 1), 0)
ekle_mf('kapak_pu', C.geo_kapak_pu(MM['on_kapak']['V'].min(0), MM['on_kapak']['V'].max(0)), 'pu', 'mek', 'PU köpük (dış kabuk ↔ iç panel, enjeksiyon)')

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
    kaynak('punta_' + k['ad'], [G.kaynak_noktasi((k['xw'], 433.0, k['zc'] + dz), 1.2) for dz in (-5.0, 5.0)], 'punta: köşebent dik kolu ↔ kızak gövdesi (2 nokta)')
kaynak('kaynak_kol_kutu', [G.kaynak_dikisi((1483.5, 457.95, -596.5), (1483.5, 457.95, -567.5)), G.kaynak_dikisi((1483.5, 464.21, -596.5), (1483.5, 464.21, -567.5))],
       'TIG: kol ↔ kutu sol yanı (alt + üst kenar, 2 × 29 mm)')
kaynak('kaynak_tabla', [G.kaynak_dikisi((1480.5, 464.21, -720.5), (1480.5, 464.21, -711.5), 0.6), G.kaynak_dikisi((1483.5, 464.21, -720.5), (1483.5, 464.21, -711.5), 0.6)],
       'TIG köşe: tabla ↔ kol üst yüzü (2 × 9 mm)')
kaynak('kaynak_kulak', [G.kaynak_dikisi((C.KUL_X0, C.MY0, C.MZ0 + 1.0), (C.KUL_X0, C.MY0, C.MZ1 - 1.0), 0.6), G.kaynak_dikisi((C.KUL_X1, C.MY0, C.MZ0 + 1.0), (C.KUL_X1, C.MY0, C.MZ1 - 1.0), 0.6)],
       'TIG köşe: mıknatıs kulağı ↔ tabla (iki yan, 2 × 26 mm)')
kaynak('kaynak_cene', [G.kaynak_dikisi((1477.5, 460.45, -750.0), (1477.5, 460.45, -722.0), 0.5), G.kaynak_dikisi((1491.5, 460.45, -750.0), (1491.5, 460.45, -722.0), 0.5)],
       'TIG: ara parça ↔ alt çene (iki kenar, 2 × 28 mm)')
for k_ in ('arka', 'on'):
    z0, z1 = C.RZ[k_]
    kaynak('punta_reed_' + k_, [G.kaynak_noktasi((C.RPX0 + 1.0, C.RY1, z_), 1.0) for z_ in (z0 + 5.0, z1 - 5.0)], 'punta: reed plakası ↔ sensör laması alt yüzü (2 nokta)')
kaynak('kaynak_avara', [G.kaynak_dikisi((1467.2, 487.55 + 0.4, -29.0), (1467.2, 487.55 + 0.4, -9.0)), G.kaynak_dikisi((1469.2, 487.55 + 0.4, -29.0), (1469.2, 487.55 + 0.4, -9.0)),
                        G.kaynak_dikisi((1467.6, 486.55, -9.0), (1469.6, 486.55, -9.0))], 'TIG: avara kolu kulağı ↔ sensör laması (iki yan + uç)')
kaynak('kaynak_avara_mili', [G.silindir((1469.2, C.AY, -1.0), (1, 0, 0), 4.2, 0.9, 24) - G.silindir((1469.0, C.AY, -1.0), (1, 0, 0), 3.0, 1.4, 24)], 'saplama kaynağı: avara mili ↔ kol')
kaynak('kaynak_avara_cerceve', [G.kaynak_dikisi((1455.5, 492.2, 22.7), (1463.5, 492.2, 22.7), 0.6), G.kaynak_dikisi((1454.2, 494.5, 22.7), (1454.2, 502.5, 22.7), 0.6)],
       'TIG köşe (içeriden): avara kolu ön flanşı ↔ ön çerçeve arkası (2 × 8 mm)')
ekle('avara_mili', AVARA_MILI[0], AVARA_MILI[1], 'mekanizma', 'mek', 'avara mili Ø6 (+1 mm, E segman yuvası Ø5) — kola saplama kaynaklı')

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
# PLAN (plan_v3.md ile birebir) — tezgâh kutusu YOK: alt montajlar montaj alanında havada durur
# =====================================================================================================================
KAM.append([0.0, K_GENEL[0], K_GENEL[1]])
t = 0.6


def tezgaha(ad_l, ust=60.0, t0=None, hiz=900.0, grup=None, yan=(0, 0, 0)):
    """üretimden / raftan montaj alanına (çekmecenin yerine): kaldır → üstüne → (yan) → indir"""
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


def yakin(adlar, uz=0.20, yon=(0.55, 0.42, 0.72), nokta=None):
    """birleşim yakın planı: parçaların o anki konumunun merkezi (m) · nokta (mm, son konum) verilirse ilk parçanın ötelemesiyle oraya"""
    if nokta is not None:
        c = (np.asarray(nokta, float) + CUR.get(adlar[0], np.zeros(3))) / 1000.0
    else:
        L = [P[a]['V'] + CUR.get(a, np.zeros(3)) for a in adlar]
        X = np.vstack(L); c = (X.min(0) + X.max(0)) / 2000.0
    d = np.asarray(yon, float); d /= np.linalg.norm(d)
    return ((c + d * uz).round(3).tolist(), c.round(3).tolist())


def birlesim(tt, adlar, metin, uz=0.20, yon=(0.55, 0.42, 0.72), nokta=None):
    """yakın kamera + olay metni + birleşen parçalar 1,6 s turuncu vurgu"""
    kam(tt, yakin(adlar, uz, yon, nokta)); olay(tt, metin)
    if not metin.startswith(('TIG', 'Punta')): vurgu([a for a in adlar if a in P], tt, tt + 1.6)      # kaynakta yalnız dikiş vurgulanır


KUCUK = [(x_, 0.0, z_) for z_ in (830.0, 940.0) for x_ in (2860.0, 2990.0, 3120.0, 3250.0, 3380.0, 3510.0)]
# ---------------- BÖLÜM 1 · ÜRETİM (küçük sac parçalar) ----------------
adim('Üretim: kızak köşebentleri',
     'Kızak köşebendi 1,5 mm (AISI 304) × 4: lazerde açınım (yatay kolda Ø4,5 delik), abkantta dik kol 90° bükülür. Görevi: kızağı (rayın iç elemanı) çekmecenin lamasına bağlamak.',
     'köşebent × 4 · 1,5 mm · 1 büküm · Ø4,5', K_URT)
for k in KOSE:
    t = uret(k['ad'], t, 'Köşebent %s-%s' % ('sol' if k['yan'] == 'sol' else 'sağ', k['ad'][-1]), sure_bukum=0.7); t = rafa(k['ad'], KUCUK.pop(0), t) + 0.05
adim('Üretim: motor braketi · reed plakaları',
     'Motor braketi 3 mm: lazerde göbek deliği, flanş kolunda 4 × M3 havşa (motor vidaları), tabanda 2 × M5 havşa (arka duvar vidaları); abkantta flanş kolu 90° bükülür. Reed plakası 2 mm × 2 (düz): lazerde 2 × Ø4,22, PEM CLS-M3-2 somunlar preste deliğine basılır (sensör vidaları bunlara girer).',
     'motor braketi 3 mm (1 büküm) · reed plakası 2 mm × 2 + 4 × PEM CLS-M3-2', K_URT_YAKIN)
t = uret('motor_braketi', t, 'Motor braketi'); t = rafa('motor_braketi', KUCUK.pop(0), t) + 0.1
for k_ in ('arka', 'on'):
    pl = 'reed_plaka_' + k_
    t = uret(pl, t, 'Reed plakası %s' % ('arka' if k_ == 'arka' else 'ön'), pemler=[('pem_reed_%s_%d' % (k_, i), 0, (-1, 0, 0)) for i in (1, 2)])
    birlesim(t - 2.0, [pl], 'PEM CLS-M3-2 × 2 → reed plakasının Ø4,22 deliklerine preslenir (sac yüzüyle aynı hizada, iç diş M3)', 0.16)
    t = rafa(pl, KUCUK.pop(0), t, grup=[pl, 'pem_reed_%s_1' % k_, 'pem_reed_%s_2' % k_]) + 0.1
adim('Üretim: avara ünitesi (kol · sensör laması · mil · reed plakaları)',
     'Avara kolu 2 mm: lazer → abkant (ön flanş, üst flanş). Sensör laması L 2 mm: tek büküm. Bağlantılar: kol kulağı ↔ lama TIG (iki yan + uç); avara mili Ø6 ↔ kol saplama kaynağı; reed plakaları ↔ lamanın alt yüzü punta (her biri 2 nokta). Mil ucunda E segman yuvası (Ø5 × 0,75).',
     'avara kolu (2 büküm) · sensör laması (1 büküm) · mil · 2 reed plakası · TIG + saplama kaynağı + punta', K_URT_YAKIN)
AV_YER = np.array([2780.0, 0.0, -230.0])
t = uret('avara_kolu', t, 'Avara kolu')
t = rafa('avara_kolu', AV_YER, t) + 0.05
hedef_k = CUR['avara_kolu'].copy()
t = uret('sensor_lamasi', t, 'Sensör laması')
o_l = CUR['sensor_lamasi'].copy(); dy = Y_SAFE - (P['sensor_lamasi']['V'][:, 1].min() + o_l[1])
t = yolu(['sensor_lamasi'], [o_l + [0, dy, 0], [hedef_k[0] + 60, o_l[1] + dy, hedef_k[2]], hedef_k + [60, -30, 0], hedef_k + [0, -30, 0], hedef_k], t, hiz=900) + 0.1
basla('avara_mili', hedef_k + [60, 0, 0], t); t = yolu(['avara_mili'], [hedef_k], t, hiz=200); vurgu(['avara_mili'], t - 0.3, t + 0.6)
for a in ('kaynak_avara', 'kaynak_avara_mili'):
    kaynak_yap(a, t); CUR[a] = hedef_k.copy()
birlesim(t, ['avara_kolu', 'sensor_lamasi'], 'TIG: avara kolu kulağı ↔ sensör laması (iki yan + uç) · saplama kaynağı: avara mili ↔ kol', 0.30); t += 1.4
REEDP = []
for k_ in ('arka', 'on'):
    pl = 'reed_plaka_' + k_; grp = [pl, 'pem_reed_%s_1' % k_, 'pem_reed_%s_2' % k_]; REEDP += grp + ['punta_reed_' + k_]
    o_p = CUR[pl].copy(); dy = Y_SAFE - (P[pl]['V'][:, 1].min() + o_p[1])
    t = yolu(grp, [o_p + [0, dy, 0], [hedef_k[0] - 40, o_p[1] + dy, hedef_k[2]], hedef_k + [-40, -40, 0], hedef_k + [0, -40, 0], hedef_k], t, hiz=900) + 0.05
    kaynak_yap('punta_reed_' + k_, t, 0.6); CUR['punta_reed_' + k_] = hedef_k.copy()
    birlesim(t, [pl], 'Punta: reed plakası %s ↔ sensör lamasının alt yüzü (2 nokta)' % ('arka' if k_ == 'arka' else 'ön'), 0.16); t += 1.0
AVARA = ['avara_kolu', 'sensor_lamasi', 'avara_mili', 'kaynak_avara', 'kaynak_avara_mili'] + REEDP
adim('Üretim: kayış çenesi (ayrı blok)',
     'Kayış çenesi artık kola kaynaklı değil, ayrı bloktur. Alt çene 2,5 mm + ara parça 1,2 mm lazerde kesilir (her birinde 2 × Ø3,4), ara parça alt çeneye iki kenarından TIG ile kaynaklanır. Üst çene 2,5 mm (2 × Ø3,4) ayrı. İkisi rafa — çekmece raylara takılıp açıldığında monte edilir.',
     'çene alt gövdesi (alt çene 2,5 + ara 1,2 · TIG 2 × 28 mm) · üst çene 2,5', K_URT_YAKIN)
t = uret('cene_alt', t, 'Çene alt gövdesi')
kaynak_yap('kaynak_cene', t); CUR['kaynak_cene'] = CUR['cene_alt'].copy()
birlesim(t, ['cene_alt'], 'TIG: ara parça ↔ alt çene (iki kenar, 2 × 28 mm)', 0.16); t += 1.2
t = rafa('cene_alt', KUCUK.pop(0), t, grup=['cene_alt', 'kaynak_cene']) + 0.1
t = uret('cene_ust', t, 'Üst çene'); t = rafa('cene_ust', KUCUK.pop(0), t) + 0.1
# ---------------- BÖLÜM 2 · RAY ÜNİTESİ ----------------
adim('Ray ünitesi: iç eleman ayrılır',
     'Accuride DZ3832-0700 teleskopik ray (satın alınan ürün, tek parça gelir: dış + ara + iç eleman). İç eleman (kızak) kilit dili basılarak ray ekseni boyunca öne çekilip ayrılır; çekmeceye bağlanacak.',
     'ray ünitesi sol / sağ (katalog) · iç eleman ayrılır', K_URT)
RAY_YER = {'sol': np.array([2950.0, 0.0, -330.0]), 'sag': np.array([3050.0, 0.0, -330.0])}
for yan in ('sol', 'sag'):
    grp = ['sabit_ray_' + yan, 'ara_ray_' + yan, 'kizak_' + yan]
    c_ = merkez('sabit_ray_' + yan); o_ = np.array([RAY_YER[yan][0] - c_[0], BENCH_Y - P['sabit_ray_' + yan]['V'][:, 1].min(), RAY_YER[yan][2] - c_[2]])
    for a in grp: basla(a, o_ + [0, 260.0, 0], t)
    t = yolu(grp, [o_], t, hiz=600) + 0.1
    t = yolu(['kizak_' + yan], [CUR['kizak_' + yan] + [0, 0, 720]], t, hiz=600); olay(t - 1.2, 'İç eleman (kızak) ray ekseni boyunca öne çekilip ayrılır'); t += 0.15
# ---------------- BÖLÜM 3 · DOLAP İÇİ ----------------
adim('Motor braketi → arka duvar',
     'Motor braketi ön çerçeve açıklığından bölmeye girer, tabanı arka iç saca oturur. Bağlantı: 2 × DIN 7991 M5 × 6 havşa vida → arka iç sacdaki 2 × PEM SP-M5-1 (Ø6,4 deliğe preslenmiş; arkasında köpük kapağı, vida ucu kapağa değmez).',
     'motor braketi · 2 × DIN 7991 M5 × 6 → 2 × PEM SP-M5-1 (arka iç sac)', K_ARKA)
t = dolaba('motor_braketi', (0, 0, 25), t); vurgu(['motor_braketi'], t - 0.4, t + 0.5)
birlesim(t, ['motor_braketi'], 'Motor braketi tabanı ↔ arka iç sac: 2 × DIN 7991 M5 × 6 → PEM SP-M5-1', 0.22, (0.5, 0.35, 0.8))
for i in (1, 2): t = tak('vida_braket_%d' % i, t, 0.8) + 0.1
t += 0.4
adim('Step motor → braket',
     'Step motor (Transmotec PD3665, satın alınan ürün — tek parça) önden girer, ekseni boyunca −x sürülür: redüktör göbeği braketin deliğine oturur. Bağlantı: 4 × DIN 7991 M3 × 6 havşa vida, braketin flanş kolundan redüktör yüzündeki 4 × M3 dişli deliğe (Ø31 daire).',
     'step motor · 4 × DIN 7991 M3 × 6 → motor yüzü M3 dişleri', K_ARKA)
basla('motor', np.array([24.0, Y_SAFE - P['motor']['V'][:, 1].min(), 980.0]), t)
t = yolu(['motor'], [[24.0, 0, 980.0], [24.0, 0, 0], [0, 0, 0]], t, hiz=600); vurgu(['motor'], t - 0.5, t + 0.5)
birlesim(t, ['motor_braketi'], 'Motor ↔ braket flanş kolu: 4 × DIN 7991 M3 × 6 (motor yüzü M3 dişli delik)', 0.16, (-0.75, 0.3, 0.6), nokta=(1481.0, YC, ZC))
for i in range(1, 5): t = tak('vida_motor_%d' % i, t, 0.6) + 0.05
adim('Motor kasnağı · setskur',
     'GT3 motor kasnağı (satın alınan ürün) mil ekseninde (+x) mile geçer. Bağlantı: DIN 913 M3 × 4 setskur, kasnak göbeğindeki radyal M3 dişli delikten milin düz yüzüne sıkılır.',
     'GT3 motor kasnağı · DIN 913 M3 × 4 setskur', K_ARKA_YAKIN)
basla('arka_kasnak', np.array([-14.5, Y_SAFE - P['arka_kasnak']['V'][:, 1].min(), 980.0]), t)
t = yolu(['arka_kasnak'], [[-14.5, 0, 980.0], [-14.5, 0, 0], [0, 0, 0]], t, hiz=600); vurgu(['arka_kasnak'], t - 0.4, t + 0.4)
birlesim(t, ['arka_kasnak'], 'Kasnak göbeği ↔ motor mili: DIN 913 M3 × 4 setskur (radyal M3 delik)', 0.15)
t = tak('setskur', t, 0.6) + 0.3
adim('Ray üniteleri → bölme sacları',
     'Sol ve sağ ray ünitesi (dış + ara eleman) önden girer, yana kayıp bölme sacına yaslanır. Bağlantı: her ray 3 × DIN 7991 M5 × 6 havşa vida, ara elemanın erişim deliklerinden, bölme sacındaki PEM SP-M5\'lere (arkada 1 mm derin köpük kapağı).',
     'ray ünitesi sol / sağ · 6 × DIN 7991 M5 × 6 → PEM SP-M5', K_RAY)
for yan, sx in (('sol', 10.0), ('sag', -9.0)):
    t = dolaba('sabit_ray_' + yan, (sx, 0, 0), t, grup=['sabit_ray_' + yan, 'ara_ray_' + yan], hiz=800) + 0.05
birlesim(t, ['sabit_ray_sol'], 'Ray dış elemanı ↔ bölme sacı: 3 + 3 × DIN 7991 M5 × 6 → PEM SP-M5', 0.13, (0.6, 0.4, 0.7), nokta=(1456.5, 443.35, -45.0))
for k_ in (1, 2, 3):
    EL[VIDA_RAY[k_ - 1]] = dict(eks=np.array([-1.0, 0, 0]), yol=40.0); EL[VIDA_RAY[k_ + 2]] = dict(eks=np.array([1.0, 0, 0]), yol=40.0)
    t0 = t; tak(VIDA_RAY[k_ - 1], t0, 0.6); t = tak(VIDA_RAY[k_ + 2], t0, 0.6) + 0.1
adim('Avara ünitesi → ön çerçeve (TIG, içeriden)',
     'Kaynaklı avara ünitesi alçaktan açıklıktan girer, içeride sola kayar, yükselip ön flanşıyla ön çerçevenin arkasına oturur. Bağlantı: ön flanş ↔ çerçeve arkası TIG köşe dikişi, içeriden 2 × 8 mm. (v2\'deki kör perçin uygulanmadı: Ø6,5 perçin başı çerçevenin önünde üst çekmecenin fitiline biniyor.)',
     'avara ünitesi · TIG köşe 2 × 8 mm (içeriden)', K_SOL_ON)
o_a = CUR['avara_kolu'].copy()
zon = 200.0 - P['sensor_lamasi']['V'][:, 2].min()
t = yolu(AVARA, [o_a + [0, Y_SAFE - 480, 0], [0.6, o_a[1] + Y_SAFE - 480, zon], [0.6, -21.0, zon], [0.6, -21.0, -0.4], [0.6, -1.0, -0.4], [0, -1.0, -0.4], [0, 0, -0.4], [0, 0, 0]], t, hiz=700)
vurgu(['avara_kolu', 'sensor_lamasi'], t - 0.4, t + 0.5)
kaynak_yap('kaynak_avara_cerceve', t)
birlesim(t, ['avara_kolu'], 'TIG köşe: avara kolu ön flanşı ↔ ön çerçeve arkası (içeriden, 2 × 8 mm)', 0.16, (0.45, 0.3, -0.85)); t += 1.5
adim('Avara kasnağı · E segman',
     'GT3 avara kasnağı (2 × MR126 rulmanlı, satın alınan ürün) mil ekseninde (−x) mile geçer. Bağlantı: DIN 6799 RS 5 E segman, milin ucundaki Ø5 yuvaya yukarıdan radyal takılır — kasnak eksenel tutulur.',
     'GT3 avara kasnağı · DIN 6799 RS 5 E segman', K_SOL_ON)
basla('avara_kasnagi', np.array([40.0, Y_SAFE - P['avara_kasnagi']['V'][:, 1].min(), 200.0 + 18.0]), t)
t = yolu(['avara_kasnagi'], [[40.0, 0, 218.0], [40.0, 0, 0], [0, 0, 0]], t, hiz=400); vurgu(['avara_kasnagi'], t - 0.4, t + 0.5)
basla('e_segman', np.array([0.0, Y_SAFE - P['e_segman']['V'][:, 1].min(), 218.0]), t)
t = yolu(['e_segman'], [[0.0, 20.0, 218.0], [0.0, 20.0, 0.0], [0, 0, 0]], t, hiz=400); vurgu(['e_segman'], t - 0.3, t + 0.7)
birlesim(t, ['e_segman'], 'E segman DIN 6799 RS 5 → mil ucundaki Ø5 yuva (kasnağı eksenel tutar)', 0.10, (0.7, 0.4, 0.6)); t += 0.8
adim('Reed sensörler → reed plakaları',
     'Littelfuse 59135 reed sensör × 2 (satın alınan ürün, 28,57 × 19,05 × 6,35, iki yarıklı montaj deliği) arkada ve önde reed plakasına yaslanır. Bağlantı: her sensör 2 × ISO 7380 M3 × 8, sensörün yarıklarından plakadaki PEM CLS-M3-2\'lere (yarıklar konum ayarı verir).',
     'reed sensör × 2 · 4 × ISO 7380 M3 × 8 → 4 × PEM CLS-M3-2', K_ARKA_YAKIN)
for k_, zg in (('arka', 980.0), ('on', 300.0)):
    a = 'reed_' + k_
    basla(a, np.array([30.0, 0.0, zg]), t); t = yolu([a], [[30.0, 0, 0], [0, 0, 0]], t, hiz=650); vurgu([a], t - 0.3, t + 0.5)
    birlesim(t, [a], 'Reed sensör %s ↔ reed plakası: 2 × ISO 7380 M3 × 8 → PEM CLS-M3-2' % ('arka' if k_ == 'arka' else 'ön'), 0.14, (0.75, 0.35, 0.55))
    for i in (1, 2): t = tak('vida_reed_%s_%d' % (k_, i), t, 0.55) + 0.05
    t += 0.2
# ---------------- BÖLÜM 4 · ÇEKMECE KUTUSU (üretim → montaj alanı) ----------------
adim('Kutu sacları: lazer → montaj alanı → TIG',
     'Lazerde 5 düz sac (AISI 304): taban 2 mm, iki yan, arka, ön 1 mm. Bağlantı: yanlar tabanın üstüne oturur, iç köşeden TIG (tam boy); arka ve ön iki yanın arasına girer, tabana ve iki yana TIG.',
     'kutu tabanı 2 · yan sol / sağ 1 · arka 1 · ön 1 · 4 TIG dikişi', K_URT)
t = uret('kutu_taban', t, 'Kutu tabanı 2 mm'); kam(t, K_TEZ); t = tezgaha('kutu_taban', 40, t) + 0.1
kam(t, K_URT)
for ad, nm, yn in (('kutu_yan_sol', 'Kutu sol yanı', 'sol'), ('kutu_yan_sag', 'Kutu sağ yanı', 'sag')):
    t = uret(ad, t, nm); kam(t, K_TEZ); t = tezgaha(ad, 80, t) + 0.05
    k_ = 'kaynak_kutu_yan_' + yn; kaynak_yap(k_, t); CUR[k_] = DR.copy()
    birlesim(t, [ad, 'kutu_taban'], 'TIG iç köşe: %s yan ↔ taban (tam boy 616 mm)' % ('sol' if yn == 'sol' else 'sağ'), 0.16, (0.45, 0.45, 0.75),
             nokta=(1485.1 if yn == 'sol' else 2041.9, 424.1, 20.5)); t += 1.4
    kam(t, K_URT)
for ad, nm, k_ in (('kutu_arka', 'Kutu arkası', 'kaynak_kutu_arka'), ('kutu_on', 'Kutu önü', 'kaynak_kutu_on')):
    t = uret(ad, t, nm); kam(t, K_TEZ); t = tezgaha(ad, 80, t) + 0.05
    kaynak_yap(k_, t); CUR[k_] = DR.copy()
    birlesim(t, [ad, 'kutu_taban'], 'TIG: %s ↔ taban + iki yan (3 dikiş)' % ('arka' if 'arka' in ad else 'ön'), 0.18, (0.45, 0.5, 0.75 if 'on' in ad else -0.75),
             nokta=(1485.1, 430.0, -595.4 if 'arka' in ad else 20.4)); t += 1.4
    kam(t, K_URT)
adim('Kızak lamaları → kutu (punta)',
     'Lamalar 6 mm sacdan 17,3 × 616 kesilir, köşebent vidaları için 2 × M4 dişli kör delik (derinlik 5) açılır. Bağlantı: kutunun iki yanına punta, her biri 4 nokta.',
     'lama sol / sağ · 2 × M4 dişli · punta 4 + 4', K_URT_YAKIN)
for yan, sx in (('sol', -70.0), ('sag', 70.0)):
    t = uret('lama_' + yan, t, 'Kızak laması %s' % ('sol' if yan == 'sol' else 'sağ')); kam(t, K_TEZ_SOL)
    t = tezgaha('lama_' + yan, 0, t, yan=(sx, 0, 0)) + 0.05
    kaynak_yap('punta_lama_' + yan, t, 0.6); CUR['punta_lama_' + yan] = DR.copy()
    birlesim(t, ['lama_' + yan, 'kutu_yan_' + yan], 'Punta: lama ↔ kutu %s yanı (4 nokta)' % ('sol' if yan == 'sol' else 'sağ'), 0.14, (0.6 if yan == 'sag' else -0.6, 0.5, 0.6),
             nokta=(1483.5 if yan == 'sol' else 2043.5, 424.8, -20.0)); t += 1.2
    kam(t, K_URT_YAKIN)
adim('Ön bağlantı braketleri → kutu önü (punta)',
     'Her braket 2 mm sacdan açınım olarak kesilir (ön flanşta 2 × Ø5,5 — kapak saplamaları için), abkantta önce yan kol, sonra ön flanş 90°. Bağlantı: kutu önüne punta, 2 nokta.',
     'ön braket sol / sağ · 2 büküm · punta 2 + 2', K_URT_YAKIN)
for yan in ('sol', 'sag'):
    t = uret('on_braket_' + yan, t, 'Ön braket %s' % ('sol' if yan == 'sol' else 'sağ')); kam(t, K_TEZ)
    t = tezgaha('on_braket_' + yan, 0, t, yan=(0, 0, 60)) + 0.05
    kaynak_yap('punta_braket_' + yan, t, 0.6); CUR['punta_braket_' + yan] = DR.copy()
    birlesim(t, ['on_braket_' + yan], 'Punta: ön braket %s ↔ kutu önü (2 nokta)' % ('sol' if yan == 'sol' else 'sağ'), 0.22); t += 1.0
    kam(t, K_URT_YAKIN)
adim('Kayış kolu · tabla · mıknatıs kulağı (kutuya)',
     'Kol: 3 mm sacdan 6,26 × 154 kesilir → kutu sol yanının arkasına TIG (alt + üst kenar, 2 × 29 mm). Tabla 2,5 mm (2 × Ø3,4 — çene cıvataları) → kolun ucuna TIG köşe (2 × 9 mm). Mıknatıs kulağı 2 mm (2 × Ø4,22 + 2 × PEM CLS-M3-2 preslenir) → tablaya TIG köşe (iki yan).',
     'kol 3 · tabla 2,5 · kulak 2 + 2 PEM · TIG 3 birleşim', K_URT_YAKIN)
t = uret('kol', t, 'Kayış kolu'); kam(t, K_TEZ_SOL); t = tezgaha('kol', 0, t, yan=(-50, 0, 0)) + 0.05
kaynak_yap('kaynak_kol_kutu', t); CUR['kaynak_kol_kutu'] = DR.copy()
birlesim(t, ['kol'], 'TIG: kol ↔ kutu sol yanı (alt + üst kenar, 2 × 29 mm)', 0.16, (0.7, 0.45, -0.55)); t += 1.3
t = uret('tabla', t, 'Kol tablası'); kam(t, K_TEZ_SOL); t = tezgaha('tabla', 30, t, yan=(-50, 0, 0)) + 0.05
kaynak_yap('kaynak_tabla', t); CUR['kaynak_tabla'] = DR.copy()
birlesim(t, ['tabla', 'kol'], 'TIG köşe: tabla ↔ kolun üst yüzü (2 × 9 mm)', 0.13, (0.7, 0.5, -0.5)); t += 1.3
t = uret('kulak', t, 'Mıknatıs kulağı', pemler=[('pem_kulak_%d' % i, 0, (1, 0, 0)) for i in (1, 2)])
birlesim(t - 2.0, ['kulak'], 'PEM CLS-M3-2 × 2 → kulağın Ø4,22 deliklerine preslenir', 0.14)
kam(t, K_TEZ_SOL); t = tezgaha('kulak', 30, t, grup=['kulak', 'pem_kulak_1', 'pem_kulak_2'], yan=(0, 0, -40)) + 0.05
kaynak_yap('kaynak_kulak', t); CUR['kaynak_kulak'] = DR.copy()
birlesim(t, ['kulak', 'tabla'], 'TIG köşe: mıknatıs kulağı ↔ tabla (iki yan, 2 × 26 mm)', 0.13, (0.7, 0.5, -0.5)); t += 1.3
adim('Mıknatıs → kulak',
     'Littelfuse 57135 mıknatıs (satın alınan ürün, tek parça, iki yarıklı) tablanın üstünde kulağa yaslanır. Bağlantı: 2 × ISO 7380 M3 × 8, mıknatısın yarıklarından kulaktaki PEM CLS-M3-2\'lere (baş reed tarafında, reed vida başıyla arası 1,3 mm).',
     'mıknatıs · 2 × ISO 7380 M3 × 8 → 2 × PEM CLS-M3-2', K_TEZ_SOL)
basla('miknatis', DR + np.array([-30.0, 60.0, 0.0]), t)
t = yolu(['miknatis'], [DR + [-30.0, 0.0, 0.0], DR], t, hiz=300); vurgu(['miknatis'], t - 0.3, t + 0.5)
birlesim(t, ['miknatis', 'kulak'], 'Mıknatıs ↔ kulak: 2 × ISO 7380 M3 × 8 → PEM CLS-M3-2', 0.13, (-0.6, 0.45, -0.6))
for i in (1, 2):
    a = 'vida_miknatis_%d' % i; e_ = EL[a]['eks']; basla(a, DR - e_ * EL[a]['yol'], t); git(a, DR, t, 0.55); vurgu([a], t + 0.3, t + 1.0); t += 0.65
t += 0.2
kam(t, K_TEZ)
basla('silikon_tepsi', DR + np.array([0, 160.0, 0]), t); git('silikon_tepsi', DR, t, 1.0); olay(t, 'Silikon tepsi kutuya serbest oturur (bağlantısız, yıkamak için çıkar)'); t += 1.2
# ---------------- BÖLÜM 5 · KIZAKLAR + DOLABA ----------------
adim('Köşebentler · kızaklar (montaj alanında)',
     'Bağlantı: köşebentlerin yatay kolu lamaya ISO 7380 M4 × 6 ile (lamadaki M4 dişe). Kızaklar (rayın iç elemanı) köşebentlerin dik koluna yaslanır, punta (her köşebent 2 nokta).',
     'köşebent × 4 + 4 × ISO 7380 M4 × 6 · kızak × 2 (punta 2 × 2)', K_TEZ_SOL)
for k in KOSE:
    t = tezgaha(k['ad'], 40, t, hiz=1100)
    a = 'vida_' + k['ad']; basla(a, DR + np.array([0, 30.0, 0]), t); git(a, DR, t, 0.5); vurgu([a], t + 0.3, t + 1.0)
    if k['ad'] == 'kose_sol_1': birlesim(t, [k['ad']], 'Köşebent ↔ lama: ISO 7380 M4 × 6 (lamada M4 dişli kör delik)', 0.10, (-0.7, 0.5, 0.5))
    t += 0.6
for yan, sx in (('sol', -1.0), ('sag', 1.0)):
    t = tezgaha('kizak_' + yan, 0, t, hiz=1000, yan=(sx * 40, 0, 0))
    for k in KOSE:
        if k['yan'] == yan: kaynak_yap('punta_' + k['ad'], t, 0.5); CUR['punta_' + k['ad']] = DR.copy()
    birlesim(t, ['kose_%s_1' % yan], 'Punta: kızak ↔ köşebent dik kolu (2 × 2 nokta)', 0.12, (-0.7 if yan == 'sol' else 0.7, 0.5, 0.5)); t += 0.9
CEKMECE = (['kutu_taban', 'kutu_yan_sol', 'kutu_yan_sag', 'kutu_arka', 'kutu_on', 'kaynak_kutu_yan_sol', 'kaynak_kutu_yan_sag', 'kaynak_kutu_arka', 'kaynak_kutu_on',
            'lama_sol', 'lama_sag', 'punta_lama_sol', 'punta_lama_sag', 'kizak_sol', 'kizak_sag',
            'on_braket_sol', 'on_braket_sag', 'punta_braket_sol', 'punta_braket_sag', 'silikon_tepsi',
            'kol', 'kaynak_kol_kutu', 'tabla', 'kaynak_tabla', 'kulak', 'pem_kulak_1', 'pem_kulak_2', 'kaynak_kulak', 'miknatis', 'vida_miknatis_1', 'vida_miknatis_2']
           + [k['ad'] for k in KOSE] + ['vida_' + k['ad'] for k in KOSE] + ['punta_' + k['ad'] for k in KOSE])
adim('Çekmece raylara sürülür',
     'Çekmece montaj alanından ray ekseni boyunca düz çizgide içeri sürülür: kızaklar ara elemanların bilyalı kafesine geçer. Kol, tabla ve mıknatıs avara kasnağının üstünden / yanından geçer (çene bloğu henüz yok).',
     'çekmece grubu · 900 mm sürme · ray ekseni z', K_SUR)
t = yolu(CEKMECE, [np.zeros(3)], t, hiz=170.0) + 0.3
olay(t - 5.6, 'Çekmece ray ekseni boyunca sürülür — kızak ara elemanın içinde')
# ---------------- BÖLÜM 6 · KAYIŞ + ÇENE (çekmece AÇIKKEN) ----------------
adim('Kayış · çekmece açılır · çene bloğu',
     'GT3 kayış (satın alınan ürün) motor kasnağı ile avara kasnağına sarılır. Çekmece 700 mm açılır: tabla öne, avara kasnağının hemen arkasına gelir. Alt gövde ve üst çene açık çekmecenin üstünden bölmeye alınır, sağdan kayışın altına / üstüne sürülür. Bağlantı: 2 × ISO 7380 M3 × 12 yukarıdan (tabla + üst çene + ara + alt çene) + altta 2 × ISO 4032 M3 — kayış ara parçanın yanında iki çene arasında sıkışır. Çekmece kapatılır.',
     'GT3 kayış (sarılır) · çekmece açık · alt gövde · üst çene · 2 × ISO 7380 M3 × 12 · 2 × ISO 4032 M3', K_ARKA)
basla('kayis', np.zeros(3), t); ISTISNA.add('kayis'); MF['kayis'] = dict(buyu=[round(t, 3), round(t + 1.8, 3)]); olay(t, 'GT3 kayış kasnaklara sarılır (istisna: sarılarak uzar)'); t += 2.0
ACIK = np.array([0.0, 0.0, 700.0])
kam(t, K_SUR); t = yolu(CEKMECE, [ACIK], t, hiz=300.0) + 0.2; olay(t - 2.0, 'Çekmece 700 mm açılır (tabla avara kasnağının arkasında)')
JAW = []
for grp in (['cene_alt', 'kaynak_cene'], ['cene_ust']):
    a0 = grp[0]; o = CUR[a0].copy(); dy = Y_SAFE - (P[a0]['V'][:, 1].min() + o[1])
    yk = 483.0 - P[a0]['V'][:, 1].min()                                   # açık kutunun üstünden geçiş yüksekliği (kutu üstü 481,5 · açıklık üstü 491,5)
    nok = [o + [0, dy, 0], [40.0, o[1] + dy, 700.0 + 800.0], [40.0, yk, 700.0 + 800.0], [40.0, yk, 700.0], [40.0, 0.0, 700.0], ACIK]
    kam(t, yakin(['tabla'], 0.30, (0.55, 0.55, 0.65))); t = yolu(grp, nok, t, hiz=650.0) + 0.1; vurgu([a0], t - 0.4, t + 0.5); JAW += grp
birlesim(t, ['cene_alt', 'cene_ust', 'tabla'], 'Çene bloğu ↔ tabla: 2 × ISO 7380 M3 × 12 + 2 × ISO 4032 M3 (kayış iki çene arasında)', 0.14, (0.65, 0.5, 0.55))
for i in (1, 2):
    for a, yol_ in (('vida_cene_%d' % i, 20.0), ('somun_cene_%d' % i, 18.0)):
        e_ = EL[a]['eks']; basla(a, ACIK - e_ * yol_, t); git(a, ACIK, t, 0.5); vurgu([a], t + 0.3, t + 1.0); t += 0.6; JAW.append(a)
t += 0.3
kam(t, K_SUR); t = yolu(CEKMECE + JAW, [np.zeros(3)], t, hiz=300.0) + 0.3; olay(t - 2.0, 'Çekmece kapatılır — çene bloğu kayışla birlikte arkaya gider')
# ---------------- BÖLÜM 7 · ÖN KAPAK ----------------
adim('Üretim: ön kapak (8 büküm) · iç panel + PEM · PU',
     'Dış kabuk 1,5 mm: lazer → abkant 8 büküm (dört kenar, sonra dört arka dönüş). İç panel 1,0 mm: 4 delik, PEM FHS-M5-10 saplamalar preslenir. İç panel kabuğun arkasına yerleşir; aradaki boşluğa PU köpük enjekte edilir (görünmez, ısı yalıtımı).',
     'dış kabuk 1,5 (8 büküm) · iç panel 1,0 · 4 × PEM FHS-M5-10 · PU köpük', K_URT)
t = uret('kapak_dis', t, 'Kapak dış kabuğu', sure_bukum=0.75)
KP_YER = np.array([3000.0, 0.0, -300.0])
t = rafa('kapak_dis', KP_YER, t) + 0.1
h_d = CUR['kapak_dis'].copy()
PEMK = [('pem_kapak_%s_%d' % (k_, i + 1), 0, (0, 0, -1)) for k_ in STUD for i in range(2)]
t = uret('kapak_ic', t, 'Kapak iç paneli', pemler=PEMK, sure_bukum=0.75)
o_i = CUR['kapak_ic'].copy(); grp_i = ['kapak_ic'] + [p_[0] for p_ in PEMK]
dy = Y_SAFE - (P['kapak_ic']['V'][:, 1].min() + o_i[1])
t = yolu(grp_i, [o_i + [0, dy, 0], [h_d[0], o_i[1] + dy, h_d[2] - 260], h_d + [0, 0, -260], h_d], t, hiz=800) + 0.2
olay(t - 0.6, 'İç panel kabuğun arkasına yerleşir — saplamalar arkaya bakar')
basla('kapak_pu', h_d.copy(), t); ISTISNA.add('kapak_pu'); MF['kapak_pu'] = dict(buyu=[round(t, 3), round(t + 1.6, 3)]); VU['kapak_pu'].append([round(t, 3), round(t + 2.2, 3)])
olay(t, 'PU köpük iki sac arasına enjekte edilir (istisna: köpük büyüyerek doldurur)'); t += 2.0
KAPAK = ['kapak_dis', 'kapak_pu'] + grp_i
adim('Ön kapak · fitil · somunlar',
     'Fitil (silikon) kapağın kanalına arkadan bastırılır. Kapak dolabın önüne gelir; PEM saplamaları braket flanşlarındaki Ø5,5 deliklerden geçer. Bağlantı: her saplamaya U braketin açık yanından DIN 125 M5 pul + ISO 4032 M5 somun.',
     'fitil · ön kapak (saplamalar) · 4 × DIN 125 M5 · 4 × ISO 4032 M5', K_SON)
o_k2 = CUR['kapak_dis'].copy()
basla('on_panel', o_k2 + np.array([0, 0, -120.0]), t); t = yolu(['on_panel'], [o_k2], t, hiz=200); vurgu(['on_panel'], t - 0.4, t + 0.5)
olay(t - 0.8, 'Fitil kapak kanalına bastırılır')
KAPAK = KAPAK + ['on_panel']
o_k3 = CUR['kapak_dis'].copy(); dy = Y_SAFE - (P['kapak_dis']['V'][:, 1].min() + o_k3[1])
t = yolu(KAPAK, [o_k3 + [0, dy, 0], [0, o_k3[1] + dy, 400.0], [0, 0, 400.0], [0, 0, 0]], t, hiz=650); vurgu(['kapak_dis'], t - 0.5, t + 0.5)
birlesim(t, ['on_braket_sol'], 'Kapak saplaması ↔ braket flanşı: DIN 125 M5 pul + ISO 4032 M5 somun (× 4)', 0.20, (0.75, 0.35, -0.55))
for k_ in STUD:
    sx = 1.0 if k_ == 'sol' else -1.0
    if k_ == 'sag': kam(t, yakin(['on_braket_sag'], 0.20, (-0.75, 0.35, -0.55)))
    for i in (1, 2):
        for tip, dz in (('pul', 11.35), ('somun', 6.65)):
            a = '%s_kapak_%s_%d' % (tip, k_, i)
            basla(a, np.array([sx * 30.0, 0, -dz]), t); git(a, np.array([0, 0, -dz]), t, 0.35); git(a, np.zeros(3), t + 0.35, 0.4); vurgu([a], t + 0.5, t + 1.1); t += 0.8
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
            open('plan_v3.pkl', 'wb'))
