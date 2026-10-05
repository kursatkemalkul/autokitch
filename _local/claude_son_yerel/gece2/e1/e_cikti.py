# -*- coding: utf-8 -*-
"""F montaj v2 · denetim (kural 17–18) + çıktı (GLB morph + JSON). Girdi: plan_f.pkl (t5_montaj.py) · yöntem a3_cikti.py ile aynı
(5 Eki 2026 · bulut oturumu). Yol / son konum / havada denetimi MODEL ağıyla (Vm/Fm: hat3_v9x · zincir 00–56); gösterim ağı = açınımdan bükülen sac.
Kullanım: python t5_cikti.py [--hizli] [--out <klasör>]"""
import sys, os, json, pickle, time, collections
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
sys.path.insert(0, os.path.join(HERE, '..', 'cekmece')); sys.path.insert(0, HERE); sys.stdout.reconfigure(encoding='utf-8')
import yol_denetim_v2 as Y
import v2geo as G
Y.ADIM = 0.002
OUT = sys.argv[sys.argv.index('--out') + 1] if '--out' in sys.argv else os.path.normpath(os.path.join(HERE, '..', '..', '..', '..', 'otonom', 'hat3d', 'v3', 'f_montaj'))
HIZLI = '--hizli' in sys.argv
D = pickle.load(open('plan_f.pkl', 'rb')); D['KAM'].sort(key=lambda k: k[0])
P, HAR, GOR, MF, FR, VU, IST, ROT = D['P'], D['HAR'], D['GOR'], D['MF'], D['FRAMES'], D['VU'], D['ISTISNA'], D['ROT']
CEV = set(D['CEVRE'])
# 5 Eki: üst raf geçiş contaları tezgâhta, büküm BİTTİKTEN sonra deliklere takılır → görünme anı = üst rafın son büküm karesi
if 'ust_raf' in MF and 'seg' in MF['ust_raf']:
    for a in [x for x in P if x.endswith('_raf_conta')]: GOR[a] = max(GOR.get(a, 0.0), MF['ust_raf']['seg'][-1][1] + 0.01)
GOS = list(P)
print('parça %d · süre %.1f · adım %d' % (len(GOS), D['TOPLAM'], len(D['ADIM'])))
# denetim ağı = model ağı (bükümlü saclar için açınım ağı yalnız gösterim)
Pm = {a: dict(V=np.asarray(P[a].get('Vm', P[a]['V'])) / 1000.0, F=np.asarray(P[a].get('Fm', P[a]['F'])), tur=P[a]['tur']) for a in P}
HARIC = {}
def har(a, b, neden): HARIC[tuple(sorted((a, b)))] = neden
for a, b in D['HARIC_PLAN']:
    har(a, b, D['HARIC_NEDEN'].get((a, b)) or D['HARIC_NEDEN'].get((b, a)) or 'PEM / saplama / kaynak burcu kendi sacına üretimde preslenir / puntalanır (sacla birlikte gelir)')
# punta / dikiş / yapıştırıcı / silikon işaretleri birleşme anında yerinde belirir (yüzeyde) → yol denetiminde engel değil
DEKOR = [a for a in P if P[a]['tur'] in ('kaynak', 'silikon')]
for d in DEKOR:
    for b in P:
        if b != d: HARIC[tuple(sorted((d, b)))] = 'kaynak dikişi / punta / yapıştırıcı / silikon: birleşme anında yerinde belirir, birleştirdiği yüzeyde kalır'
# kablo / hortum / kayış: kanal boyunca yerinde uzar (kural 9 istisnası) → yol yok
for a in P:
    if P[a]['tur'] == 'kablo':
        for b in P:
            if b != a: HARIC[tuple(sorted((a, b)))] = 'kablo / hortum: kanal boyunca yerinde uzar (kural 9 istisnası)'
for a in [x for x in P if x.endswith('_raf_conta')]: har(a, 'ust_raf', 'kauçuk geçiş contası üst raf deliğine sıkı oturur (conta esner)')
# ------------------------------------------------------------------ 0. son konumda kesişim
SON = Y.son_kesisim(Pm, GOS, 3e-4)
son_rap = {}
for (a, b), n in SON.items():
    son_rap['%s ↔ %s' % (a, b)] = dict(ucgen=int(n), neden=HARIC.get(tuple(sorted((a, b))), ''))
BEYANSIZ_SON = {k: v for k, v in son_rap.items() if not v['neden']}
print('SON KONUM kesişimi %d · beyansız %d' % (len(son_rap), len(BEYANSIZ_SON)))
for k, v in list(BEYANSIZ_SON.items())[:40]: print('   ', k, v['ucgen'])
# ------------------------------------------------------------------ 1. yol denetimi (kapak dönüşü dahil)
t1 = time.time()
DN = Y.Denetci(Pm, HAR, {a: [[r[0], r[1], r[2], r[3], r[4]] for r in L] for a, L in ROT.items()}, GOR, set(IST), set(), set(HARIC))
CAK = [] if HIZLI else DN.denetle(ilerleme=True)
print('YOL: çift %d · aday çakışma %d · %.0f s' % (DN.ciftsay, len(CAK), time.time() - t1), flush=True)
# 1b. aday çakışmaların doğrulaması (5 Eki): denetçi CCD'si sıfır boşluklu kaymayı da sayar → hareket penceresi boyunca 0,5 mm adımla parça konumu
#     (öteleme + kapak dönüşü, oynatıcıyla aynı formül) ve model ağlarında 0,3 mm toleranslı gerçek kesişim aranır; kesişim yoksa 'yüzey teması'
def _e(u): u = min(max(u, 0.0), 1.0); return u * u * (3 - 2 * u)
def _uu(t, h): return 1.0 if t >= h[1] else (0.0 if t <= h[0] else (t - h[0]) / (h[1] - h[0]))
def konum(a, tt):
    X = Pm[a]['V'][Pm[a]['F']].copy()
    ang = 0.0; px = pz = 0.0
    for r in ROT.get(a, []): ang += r[2] * _e(_uu(tt, r)); px, pz = r[3], r[4]
    if abs(ang) > 1e-9:
        cs, sn = np.cos(np.radians(ang)), np.sin(np.radians(ang)); dx = X[..., 0] - px; dz = X[..., 2] - pz
        X[..., 0] = px + cs * dx + sn * dz; X[..., 2] = pz - sn * dx + cs * dz
    o = np.zeros(3)
    for h in HAR[a]: o += np.array(h[2:5]) * (1 - _e(_uu(tt, h)))
    return X + o
def gercek_mi(c):
    a, b = c['a'], c['b']; t0, t1 = c['w']; n = max(10, int((t1 - t0) / 0.01))
    for tt in np.linspace(t0, t1, n):
        A = konum(a, tt); B = konum(b, tt)
        lo = np.maximum(A.reshape(-1, 3).min(0), B.reshape(-1, 3).min(0)) - 1e-3; hi = np.minimum(A.reshape(-1, 3).max(0), B.reshape(-1, 3).max(0)) + 1e-3
        if np.any(lo > hi): continue
        sa = np.all(A.max(1) >= lo, 1) & np.all(A.min(1) <= hi, 1); sb = np.all(B.max(1) >= lo, 1) & np.all(B.min(1) <= hi, 1)
        if not sa.any() or not sb.any(): continue
        k = int(Y.poz_kesisim(np.ascontiguousarray(A[sa]), np.ascontiguousarray(B[sb]), 3e-4).sum())
        if k: return dict(t=round(float(tt), 3), ucgen=k)
    return None
TEMAS = []
CAK2 = []
for c in CAK:
    g_ = gercek_mi(c)
    if g_: c['kesisim'] = g_; CAK2.append(c)
    else: TEMAS.append('%s ↔ %s' % (c['a'], c['b']))
CAK = CAK2
print('YOL (doğrulanmış): gerçek çakışma %d · sıfır boşluklu yüzey teması %d' % (len(CAK), len(TEMAS)), flush=True)
for r in CAK[:60]: print('  ÇAKIŞMA', r)
# ------------------------------------------------------------------ 2. üretim kareleri (büküm) — o an görünen parçalara karşı (gösterim ağıyla)
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
TRI = {a: np.asarray(P[a].get('Vm', P[a]['V']))[np.asarray(P[a].get('Fm', P[a]['F']))] for a in P}
LOa = {a: P[a]['V'].min(0) for a in P}; HIa = {a: P[a]['V'].max(0) for a in P}
for a in FR:
    T = kare_zaman(a); ks = sorted(T)
    for i, k in enumerate(ks):
        tt = T[k]; X = P[a]['V'] + ofs_t(a, tt) + FR[a][k]
        A = X[P[a]['F']]; lo, hi = X.min(0), X.max(0)
        for b in P:
            if b == a or GOR.get(b, 0) > tt or b in DEKOR or P[b]['tur'] == 'kablo': continue
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
# ------------------------------------------------------------------ 3. belirme · havada
BELIRME = [a for a in GOS if a not in IST and a not in CEV and a not in FR and not MF.get(a, {}).get('buyu') and P[a]['tur'] not in ('kaynak', 'silikon', 'kablo')
           and not any(abs(h[2]) + abs(h[3]) + abs(h[4]) > 1e-9 for h in HAR[a])]
TEM = {} if HIZLI else Y.temas_denetim(Pm, HAR, GOR, set(IST) | CEV | set(DEKOR), set(), tol=6e-4, turler=('sac', 'mek', 'baglanti', 'kapak', 'profil', 'pu'))
HAVADA = sorted(a for a, (tl, l) in TEM.items() if not l and not P[a].get('tezgah'))
try:
    from havada_grup import havada_grup
    HAVADA = havada_grup(HAVADA, P, Pm, HAR, GOR)
except Exception as e:
    print('havada_grup atlandı:', e)
print('BELİRME', len(BELIRME), BELIRME[:10], '· HAVADA', HAVADA)
SK = []
for a in P:
    if 'model_lo' in P[a]:
        f = max(np.abs(LOa[a] - P[a]['model_lo']).max(), np.abs(HIa[a] - P[a]['model_hi']).max()); SK.append((a, round(float(f), 4)))
SK.sort(key=lambda x: -x[1])
print('SAC (gösterim) ↔ MODEL en büyük kutu farkı:', SK[:5])
# ------------------------------------------------------------------ 4. vida / delik / diş (kural 18) — eksen boyunca ölçü (model ağı)
VD = []
def eksen_aralik(V, c, e, r):
    d = V - c; s = d @ e; rad = np.linalg.norm(d - np.outer(s, e), axis=1); m = rad <= r
    return (float(s[m].min()), float(s[m].max())) if m.any() else (None, None)
def Vm(a): return np.asarray(P[a].get('Vm', P[a]['V']))
def vida(ad, std, d_nom, karsi, karsi_ad, delikler, eks=None):
    V = Vm(ad); e = np.asarray(eks if eks is not None else P[ad].get('eks', (0, -1, 0)), float); e /= np.linalg.norm(e)
    c = (V.min(0) + V.max(0)) / 2; c = c - (c @ e) * e
    s = V @ e; uc = float(s.max())
    k0, k1 = eksen_aralik(Vm(karsi), c, e, d_nom * 0.9)
    kav = 0.0 if k0 is None else max(0.0, min(uc, k1) - k0)
    tas = None if k1 is None else uc - k1
    kes = [b for b in delikler if b in P and (('%s ↔ %s' % (ad, b)) in BEYANSIZ_SON or ('%s ↔ %s' % (b, ad)) in BEYANSIZ_SON)]
    VD.append(dict(eleman=ad, std=std, karsi=karsi_ad, kavrama_mm=round(kav, 2), dis_boyu_mm=None if k0 is None else round(k1 - k0, 2),
                   uc_tasma_mm=None if tas is None else round(tas, 2), delik_gecis=('TEMİZ' if not kes else 'KESİŞİM: ' + ', '.join(kes)), gecilen=list(delikler)))
for a in sorted(x for x in P if x.startswith('arayuz_kb_') and not x.endswith('_pul')):
    vida(a, 'ISO 4762 M8 × 25 (+ ISO 7092 pul)', 8, 'percin_somun_tb_' + a[len('arayuz_kb_'):], 'B kirişi M8 kapalı perçin somun', ['kaide_ust_plaka_4', 'kaide_arka_boru', 'kaide_sol_boru', 'kaide_sag_boru', 'kaide_enine_boru'])
for a in sorted(x for x in P if x.startswith('arayuz_kaide_M6')):
    vida(a, 'ISO 4762 M6 × 12', 6, 'kaide_plaka_pem_M6_' + a[-1], 'PEM SP-M6-2 (kaide plakası)', ['teknik_on_perde', 'dis_taban', 'kaide_ust_plaka_4'])
for a in sorted(x for x in P if x.startswith('arayuz_m8_F') and not x.endswith('_pul')):
    vida(a, 'ISO 4762 M8 × 16 (+ ISO 7092 pul)', 8, 'pem_M8_F_' + a[len('arayuz_m8_F_'):], 'PEM SP-M8-1 (sağ dış yan)', ['dis_yan_sag'])
for a in sorted(x for x in P if x.startswith('servis_arka') and x.endswith('_vida')):
    vida(a, 'DIN 7991 M5 × 12 (çökertme)', 5, a[:-len('_vida')] + '_burc', 'kaynak burcu M5 (dönüşün iç yüzü)', ['dis_arka_servis'])
for a in sorted(x for x in P if x.startswith('evaporator_ayak_') and x.endswith('_vida')):
    vida(a, 'ISO 7380 M5 × 6', 5, a[:-len('_vida')] + '_pem', 'PEM SP-M5-1 (kuru bölme tabanı)', ['evaporator_ayagi_' + a.split('_')[2]])
for a in sorted(x for x in P if x.startswith('kanal_kapagi_') and x.endswith('_vida')):
    vida(a, 'ISO 7380 M5', 5, a[:-len('_vida')] + '_pem', 'PEM SP-M5-1 (kuru bölme tabanı)', ['kanal_gecis_kapagi'])
ozet = collections.OrderedDict()
for r in VD:
    k = (r['std'], r['karsi'])
    o = ozet.setdefault(k, dict(adet=0, kav=[], dis=[], tas=[], gecis=set()))
    o['adet'] += 1; o['kav'].append(r['kavrama_mm']); o['dis'].append(r['dis_boyu_mm']); o['tas'].append(r['uc_tasma_mm']); o['gecis'].add(r['delik_gecis'][:8])
for k, o in ozet.items():
    print('  VİDA', k, o['adet'], 'kavrama', min(o['kav']), max(o['kav']), 'diş', sorted(set(x for x in o['dis'] if x is not None)), 'taşma',
          min(x for x in o['tas'] if x is not None) if any(x is not None for x in o['tas']) else None, o['gecis'])
# ------------------------------------------------------------------ 5. çıktı
MATAD = ['punta', 'yapistirici', 'sac', 'kapak', 'profil', 'kaynak', 'baglanti', 'arayuz', 'pu', 'yalitim', 'mekanizma', 'motor', 'alu', 'koyu', 'sensor', 'elektrik',
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
    if a in IST: PARCA[a]['k'] = 1
    o0 = ofs_t(a, -1.0) / 1000.0; LOt = np.minimum(LOt, V.min(0) + np.minimum(o0, 0)); HIt = np.maximum(HIt, V.max(0) + np.maximum(o0, 0))
n = G.glb_yaz(os.path.join(OUT, 'f_montaj.glb'), dug, MATS)
MA = {('%s ↔ %s' % k): v for k, v in HARIC.items() if v.startswith('MODEL AÇIĞI')}
DEN = dict(model_acigi=len(MA), yuzey_temasi=TEMAS, adim=len(D['ADIM']), parca=len(GOS), cevre=len(CEV), cift=DN.ciftsay, cakisma=len(CAK), cakismalar=CAK, adim_mm=2.0,
           uretim_kare_sorun=[list(x) for x in KARE_SORUN], belirme=len(BELIRME), belirme_liste=BELIRME, havada=HAVADA, son_konum=son_rap, son_beyansiz=len(BEYANSIZ_SON),
           haric={'%s ↔ %s' % k: v for k, v in HARIC.items() if not v.startswith(('kaynak dikişi /', 'kablo / hortum'))}, vida=VD, sac_model=SK[:10], plan_sorun=D['PLAN_SORUN'],
           istisna=sorted(IST), uretilen=sorted(FR), siyirma_mm=Y.SINIR * 1000, oturma_mm=Y.OTURMA * 1000)
OUTJ = dict(surum='f_montaj_v2', ist='F', tarih='5 Eki 2026',
            kaynak='hat3_v10h.glb (zincir 00–66) · F üst kabin h3_u_sac_v1 + kapak / atış kanalı h3_f_sac_v1 (açınım) + ana model · üretim: f_parca.py + f_montaj.py + f_cikti.py',
            sehpa=False, birim='m', toplam=D['TOPLAM'], zarf=[np.round(np.maximum(LOt, [-1, 0, -3]), 3).tolist(), np.round(np.minimum(HIt, [5, 4, 3]), 3).tolist()], ghost=[], ghost_t=0.0,
            adimlar=D['ADIM'], olaylar=sorted(D['OLAY'], key=lambda o: o[0]), kamera=D['KAM'], parcalar=PARCA, acinim=D['ACN'],
            sayim=dict(gosterilen=len(GOS), cevre=len(CEV), ucgen=int(sum(len(P[a]['F']) for a in P)), uretilen=len(FR),
                       sac=len(D['SAC_AD']), baglanti=sum(1 for a in GOS if P[a]['tur'] == 'baglanti'), kaynak=sum(1 for a in GOS if P[a]['tur'] == 'kaynak')), denetim=DEN,
            aciklama=None, istisna_metin='Kaynak dikişleri ve punta işaretleri birleşme anında belirir ve kalır; kablolar ve hava hortumları kanal boyunca uzar. Baca ve pizza kutusu stoğu U montajında / işletmede.')
OUTJ.pop('aciklama')
json.dump(OUTJ, open(os.path.join(OUT, 'f_montaj.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'), default=float)
json.dump(DEN, open('sonuc_f.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1, default=str)
print('GLB %.2f MB · JSON yazıldı · zarf %s · %s' % (n / 1e6, OUTJ['zarf'], OUT))
