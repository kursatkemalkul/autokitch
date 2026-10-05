# -*- coding: utf-8 -*-
"""A montaj v3 · denetim (kural 17–18) + çıktı (GLB morph + JSON). Girdi: plan_a3.pkl (a3_montaj.py) · yöntem b3_cikti.py ile aynı (+ kapak dönüşü)"""
import sys, os, json, pickle, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
sys.path.insert(0, os.path.join(HERE, '..', 'cekmece')); sys.path.insert(0, HERE); sys.stdout.reconfigure(encoding='utf-8')
import yol_denetim_v2 as Y
import v2geo as G
Y.ADIM = 0.002
W = r'C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH_COORDINATION\worktrees\claude-hat3-v8'
OUT = os.path.join(W, 'otonom', 'hat3d', 'v3', 'a_montaj')
HIZLI = '--hizli' in sys.argv
D = pickle.load(open('plan_a3.pkl', 'rb')); D['KAM'].sort(key=lambda k: k[0])
P, HAR, GOR, MF, FR, VU, IST, ROT = D['P'], D['HAR'], D['GOR'], D['MF'], D['FRAMES'], D['VU'], D['ISTISNA'], D['ROT']
CEV = set(D['CEVRE'])
GOS = list(P)
print('parça %d · süre %.1f · adım %d' % (len(GOS), D['TOPLAM'], len(D['ADIM'])))
Pm = {a: dict(V=P[a]['V'] / 1000.0, F=np.asarray(P[a]['F']), tur=P[a]['tur']) for a in P}
HARIC = {}
def har(a, b, neden): HARIC[tuple(sorted((a, b)))] = neden
for a, b in D['HARIC_PLAN']:
    har(a, b, 'PEM kendi deliğine preslenir (sıkı geçme, model teması)')
# ------------------------------------------------------------------ 0. son konumda kesişim (önce: geçme çiftleri beyan edilir)
SON = Y.son_kesisim(Pm, GOS, 3e-4)
for (a, b), n in SON.items():
    if (a, b) in HARIC or (b, a) in HARIC: continue
    ka = P[a]['tur'] == 'kaynak' or P[b]['tur'] == 'kaynak'
    if ka: har(a, b, 'kaynak dikişi birleştirdiği parçaya kaynar (dolgu ↔ ana metal)')
print('SON KONUM kesişimleri:', {('%s ↔ %s' % k): v for k, v in SON.items()})
# ------------------------------------------------------------------ 1. yol denetimi (kapak dönüşü dahil)
t1 = time.time()
DN = Y.Denetci(Pm, HAR, {a: [[r[0], r[1], r[2], r[3], r[4]] for r in L] for a, L in ROT.items()}, GOR, set(IST), set(), set(HARIC))
CAK = [] if HIZLI else DN.denetle(ilerleme=True)
print('YOL: çift %d · çakışma %d · %.0f s' % (DN.ciftsay, len(CAK), time.time() - t1), flush=True)
for r in CAK[:40]: print('  ÇAKIŞMA', r)
# ------------------------------------------------------------------ 2. üretim kareleri (büküm) — o an görünen parçalara karşı
def ofs_t(a, tt):
    o = np.zeros(3)
    for h in HAR[a]:
        u = 1.0 if tt >= h[1] else (0.0 if tt <= h[0] else (tt - h[0]) / (h[1] - h[0]))
        o += np.array(h[2:5]) * 1000.0 * (1 - u * u * (3 - 2 * u))
    return o
def kare_zaman(a):
    T = {}
    for t0, t1_, k0, k1 in MF[a]['seg']: T.setdefault(k0, t0); T[k1] = t1_
    return T
KARE_SORUN = []
TRI = {a: P[a]['V'][P[a]['F']] for a in P}
LOa = {a: P[a]['V'].min(0) for a in P}; HIa = {a: P[a]['V'].max(0) for a in P}
for a in FR:
    T = kare_zaman(a); ks = sorted(T)
    for i, k in enumerate(ks):
        tt = T[k]; X = P[a]['V'] + ofs_t(a, tt) + FR[a][k]
        A = X[P[a]['F']]; lo, hi = X.min(0), X.max(0)
        for b in P:
            if b == a or GOR.get(b, 0) > tt: continue
            if P[b].get('sac') == a: continue
            ob = ofs_t(b, tt); l2 = LOa[b] + ob; h2 = HIa[b] + ob
            if np.any(l2 > hi + 0.01) or np.any(h2 < lo - 0.01): continue
            Bt = TRI[b] + ob
            sa = np.all(A.min(1) <= h2, 1) & np.all(A.max(1) >= l2, 1)
            sb = np.all(Bt.min(1) <= hi, 1) & np.all(Bt.max(1) >= lo, 1)
            if not sa.any() or not sb.any(): continue
            c = int(Y.poz_kesisim(np.ascontiguousarray(A[sa] / 1000), np.ascontiguousarray(Bt[sb] / 1000), 3e-4).sum())
            if c: KARE_SORUN.append((a, round(tt, 2), 'kesişiyor: %s (%d üçgen)' % (b, c)))
print('ÜRETİM KARELERİ: %d sorun' % len(KARE_SORUN)); [print('  ', s) for s in KARE_SORUN[:20]]
# ------------------------------------------------------------------ 3. belirme · havada · son konum
BELIRME = [a for a in GOS if a not in IST and a not in CEV and a not in FR and not MF.get(a, {}).get('buyu') and not any(abs(h[2]) + abs(h[3]) + abs(h[4]) > 1e-9 for h in HAR[a])]
GOSm = {a: Pm[a] for a in P}
TEM = {} if HIZLI else Y.temas_denetim(GOSm, HAR, GOR, set(IST) | CEV, set(), tol=6e-4, turler=('ray', 'sac', 'mek', 'baglanti', 'kapak', 'profil'))
HAVADA = sorted(a for a, (tl, l) in TEM.items() if not l)
if 'acici' in HAVADA and 'acici_kolon' not in HAVADA: HAVADA.remove('acici')      # aynı ürün: kafa kolona bağlı (tek parça)
son_rap = {}
for (a, b), n in SON.items():
    son_rap['%s ↔ %s' % (a, b)] = dict(ucgen=n, neden=HARIC.get((a, b)) or HARIC.get((b, a)) or '')
print('BELİRME', BELIRME[:10], len(BELIRME), '· HAVADA', HAVADA)
SK = []
for a in P:
    if 'model_lo' in P[a]:
        f = max(np.abs(LOa[a] - P[a]['model_lo']).max(), np.abs(HIa[a] - P[a]['model_hi']).max()); SK.append((a, round(float(f), 4)))
SK.sort(key=lambda x: -x[1])
print('SAC ↔ MODEL en büyük kutu farkı:', SK[:5])
# ------------------------------------------------------------------ 4. vida / delik / diş (kural 18) — eksen boyunca ölçü
VD = []
def eksen_aralik(V, c, e, r):
    """V köşelerinden eksene (c, e) r içinde olanların eksen boyunca aralığı"""
    d = V - c; s = d @ e; rad = np.linalg.norm(d - np.outer(s, e), axis=1); m = rad <= r
    return (float(s[m].min()), float(s[m].max())) if m.any() else (None, None)
def vida(ad, std, d_nom, karsi, karsi_ad, delikler, kesisen_yok=()):
    V = P[ad]['V']; e = np.asarray(P[ad].get('eks', (0, -1, 0)), float); e /= np.linalg.norm(e)
    c = (V.min(0) + V.max(0)) / 2; c = c - (c @ e) * e          # eksen üstü nokta (eksen bileşeni 0)
    s = V @ e; uc = float(s.max())
    k0, k1 = eksen_aralik(P[karsi]['V'], c, e, d_nom * 0.9)
    kav = 0.0 if k0 is None else max(0.0, min(uc, k1) - k0)
    tas = None if k1 is None else uc - k1
    kes = [b for b in delikler if ('%s ↔ %s' % tuple(sorted((ad, b)))) in son_rap or ('%s ↔ %s' % (ad, b)) in son_rap or ('%s ↔ %s' % (b, ad)) in son_rap]
    VD.append(dict(eleman=ad, std=std, karsi=karsi_ad, kavrama_mm=round(kav, 2), dis_boyu_mm=None if k0 is None else round(k1 - k0, 2), uc_tasma_mm=None if tas is None else round(tas, 2),
                   delik_gecis=('TEMİZ' if not kes else 'KESİŞİM: ' + ', '.join(kes)), gecilen=list(delikler)))
for a in sorted(x for x in P if x.startswith('arayuz_ab_') and not x.endswith('_pul')):
    vida(a, 'ISO 4762 M8 × 25 (+ ISO 7092 pul)', 8, 'cevre_B_percin', 'B kirişi M8 perçin somun', ['kaide_damlama_saci', 'kaide_ust_plaka_4', 'kaide_sol_boru', 'kaide_sag_boru', 'kaide_enine_boru', 'cevre_B_kabuk', 'cevre_B_gfrp', 'cevre_B_kiris'])
for a in sorted(x for x in P if x.startswith('arayuz_acici') and not x.endswith('_pul')):
    k = 'kaide_ust_plaka_pem_M8_acici_' + a.split('_M8_')[1]
    vida(a, 'ISO 4762 M8 × 20 (+ DIN 125 pul)', 8, k, 'PEM SP-M8-2 (kaide plakası)', ['acici_kolon', 'kaide_damlama_saci', 'kaide_ust_plaka_4'])
for a in sorted(x for x in P if x.startswith('arayuz_tabla')):
    k = 'kaide_ust_plaka_pem_M6_ray_' + a.split('_M6_')[1]
    vida(a, 'ISO 4762 M6 × 16', 6, k, 'PEM SP-M6-2 (kaide plakası)', ['cevre_T_ray', 'kaide_damlama_saci', 'kaide_ust_plaka_4'])
for a in sorted(x for x in P if x.startswith('arayuz_m8_T') and not x.endswith('_pul')):
    vida(a, 'ISO 4762 M8 × 16 (+ DIN 9021 pul)', 8, 'cevre_T_pem', 'TOPPING sol dış sacı PEM SP-M8', ['sag_yan_sac_tabla_gecisi', 'cevre_T_govde'])
for a in sorted(x for x in P if x.endswith('_saplama')):
    b = a[:-len('_saplama')]
    P[a]['eks'] = -np.asarray(P[a]['yan'], float)      # saplama dıştan içe
    if b.startswith('govde_bag_arka'):
        tr = b.split('_')[3]; gec = ['sol_yan_sac'] if tr == 'sol' else (['sag_yan_sac_tabla_gecisi'] if tr == 'sag' else ['ust_sac'])
        vida(a, 'PEM FHP-M5-12 saplama (arka sac)', 5, b + '_somun', 'ISO 10511 M5 fiberli somun', gec + ['arka_sac'])
    else:
        vida(a, 'PEM FHP-M5-15 saplama (yan / üst sac)', 5, b + '_somun', 'ISO 10511 M5 fiberli somun', [b[:-len('_bag')], P[a]['sac']])
for i in range(3):
    for v in ('a', 'b'):
        vida('onyuz_kapak_A_mentese_%d_sabit_vida_%s' % (i, v), 'ISO 7380 M5 × 12', 5, 'onyuz_kapak_A_mentese_%d_sabit' % i, 'menteşe gövdesi M5 dişi', ['kose_dikmesi_20_42'])
        vida('onyuz_kapak_A_mentese_%d_kanat_vida_%s' % (i, v), 'ISO 7380 M5 × 6', 5, 'onyuz_kapak_A_mentese_%d_pem_%s' % (i, v), 'PEM SP-M5-1 (iç tava)', ['onyuz_kapak_A_mentese_%d_kanat' % i, 'onyuz_kapak_A_ic_tava'])
import collections
ozet = collections.OrderedDict()
for r in VD:
    k = (r['std'], r['karsi'])
    o = ozet.setdefault(k, dict(adet=0, kav=[], dis=[], tas=[], gecis=set()))
    o['adet'] += 1; o['kav'].append(r['kavrama_mm']); o['dis'].append(r['dis_boyu_mm']); o['tas'].append(r['uc_tasma_mm']); o['gecis'].add(r['delik_gecis'][:8])
for k, o in ozet.items(): print('  VİDA', k, o['adet'], 'kavrama', min(o['kav']), max(o['kav']), 'diş', set(o['dis']), 'taşma', min(x for x in o['tas'] if x is not None) if any(x is not None for x in o['tas']) else None, o['gecis'])
# ------------------------------------------------------------------ 5. çıktı
MATAD = ['sac', 'kapak', 'profil', 'kaynak', 'baglanti', 'arayuz', 'pu', 'yalitim', 'mekanizma', 'motor', 'alu', 'koyu', 'sensor', 'elektrik',
         'kanal', 'fis', 'guc', 'bilgi', 'hava', 'kapak_s', 'urun', 'silik', 'tezgah', 'tepsi']
MATS = [dict(name=m, pbrMetallicRoughness=dict(baseColorFactor=[0.8, 0.8, 0.8, 1], metallicFactor=0.5, roughnessFactor=0.4)) for m in MATAD]
os.makedirs(OUT, exist_ok=True)
dug, PARCA = [], {}
LOt = np.array([1e9] * 3); HIt = -LOt.copy()
for a in P:
    V = P[a]['V'] / 1000.0; c = np.round((V.min(0) + V.max(0)) / 2, 6)
    d = dict(ad=a, V=(V - c), F=P[a]['F'], mat=MATAD.index(P[a]['m']), translation=c)
    if a in FR: d['targets'] = [f / 1000.0 for f in FR[a]]
    dug.append(d)
    PARCA[a] = dict(c=c.tolist(), m=P[a]['m'], bb=[np.round(V.min(0), 6).tolist(), np.round(V.max(0), 6).tolist()], g=GOR.get(a, 0.0), h=HAR[a], ad=P[a]['ac'])
    if VU.get(a): PARCA[a]['vu'] = VU[a]
    if a in MF and 'seg' in MF[a]: PARCA[a]['mf'] = MF[a]['seg']
    if a in MF and 'buyu' in MF[a]: PARCA[a]['buyu'] = MF[a]['buyu']
    if a in ROT: PARCA[a]['r'] = [r for r in ROT[a] if abs(r[2]) > 1e-9]
    o0 = ofs_t(a, -1.0) / 1000.0; LOt = np.minimum(LOt, V.min(0) + np.minimum(o0, 0)); HIt = np.maximum(HIt, V.max(0) + np.maximum(o0, 0))
n = G.glb_yaz(os.path.join(OUT, 'a_montaj.glb'), dug, MATS)
DEN = dict(adim=len(D['ADIM']), parca=len(GOS), cevre=len(CEV), cift=DN.ciftsay, cakisma=len(CAK), cakismalar=CAK, adim_mm=2.0,
           uretim_kare_sorun=[list(x) for x in KARE_SORUN], belirme=len(BELIRME), belirme_liste=BELIRME, havada=HAVADA, son_konum=son_rap,
           haric={'%s ↔ %s' % k: v for k, v in HARIC.items()}, vida=VD, sac_model=SK[:10], plan_sorun=D['PLAN_SORUN'],
           istisna=sorted(IST), uretilen=sorted(FR), siyirma_mm=Y.SINIR * 1000, oturma_mm=Y.OTURMA * 1000)
OUTJ = dict(surum='a_montaj_v3', ist='A', tarih='4 Eki 2026', kaynak='hat3_v9l.glb (zincir 00–44) + zincir_A_tamamla.py (A1–A3) · A gövdesi h3_a_sac_v1 (açınım) + ana model · üretim: a3_montaj.py',
            birim='m', toplam=D['TOPLAM'], zarf=[np.round(np.maximum(LOt, [-1, 0, -3]), 3).tolist(), np.round(np.minimum(HIt, [4, 4, 3]), 3).tolist()], ghost=[], ghost_t=0.0,
            adimlar=D['ADIM'], olaylar=sorted(D['OLAY'], key=lambda o: o[0]), kamera=D['KAM'], parcalar=PARCA, acinim=D['ACN'],
            sayim=dict(gosterilen=len(GOS), cevre=len(CEV), ucgen=int(sum(len(P[a]['F']) for a in P)), uretilen=len(FR),
                       sac=len(D['SAC_AD']), baglanti=sum(1 for a in GOS if P[a]['tur'] == 'baglanti'), kaynak=sum(1 for a in GOS if P[a]['tur'] == 'kaynak')), denetim=DEN)
json.dump(OUTJ, open(os.path.join(OUT, 'a_montaj.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'), default=float)
json.dump(DEN, open('sonuc_a3.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1, default=str)
print('GLB %.2f MB · JSON yazıldı · zarf %s' % (n / 1e6, OUTJ['zarf']))
