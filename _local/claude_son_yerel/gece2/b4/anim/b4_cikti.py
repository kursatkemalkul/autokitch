# -*- coding: utf-8 -*-
"""B montaj v3 · denetim (kural 17–18) + çıktı (GLB morph + JSON). Girdi: plan_b3.pkl (b3_montaj.py) · yöntem cek_v3_cikti.py ile aynı"""
import sys, os, json, pickle, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
sys.path.insert(0, os.path.join(HERE, '..', '..', 'cekmece')); sys.path.insert(0, os.path.join(HERE, '..', '..', 'b3')); sys.path.insert(0, HERE); sys.stdout.reconfigure(encoding='utf-8')
import yol_denetim_v2 as Y
import v2geo as G
Y.ADIM = 0.002
W = r'C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH_COORDINATION\worktrees\claude-hat3-v8'
OUT = os.path.join(W, 'otonom', 'hat3d', 'v3', 'b_montaj')
HIZLI = '--hizli' in sys.argv
D = pickle.load(open('plan_b4.pkl', 'rb')); D['KAM'].sort(key=lambda k: k[0])
P, HAR, GOR, MF, FR, VU, IST = D['P'], D['HAR'], D['GOR'], D['MF'], D['FRAMES'], D['VU'], D['ISTISNA']
GOS = list(P)
print('parça %d · süre %.1f · adım %d' % (len(GOS), D['TOPLAM'], len(D['ADIM'])))
Pm = {a: dict(V=P[a]['V'] / 1000.0, F=np.asarray(P[a]['F']), tur=P[a]['tur']) for a in P}
HARIC = {}
def har(a, b, neden): HARIC[tuple(sorted((a, b)))] = neden
for a, b in D['HARIC_PLAN']: har(a, b, D['HARIC_NEDEN'].get((a, b), 'perçin somun başı sacın boşluk deliğinde (Ø15,5 ↔ Ø15, 0,25 mm boşluk; çokgen yaklaşımı)'))
# yapıştırıcı filmi / punta noktaları / kaynak dikişleri birleşme anında yerinde belirir; yol denetiminde engel sayılmaz (levha ya da sac yüzünde)
DEKOR = [a for a in P if a.startswith(('yap_', 'punta_'))]
for d in DEKOR:
    for b in P:
        if b != d: HARIC[tuple(sorted((d, b)))] = 'yapıştırıcı filmi / punta noktası (yüzeyde, birleşme anında belirir)'
# kör perçin (sıkılmış hâliyle modelde: uç şişkin) ve PEM saplama (baskıyla oturur) kendi deliğinden geçer: son konumda değdiği sac / kanal / levha ile çifti beyanlı
LOa_ = {a: P[a]['V'].min(0) for a in P}; HIa_ = {a: P[a]['V'].max(0) for a in P}
for a in P:
    et = P[a].get('etur')
    if not (a.startswith('b_') and (et in ('percin', 'saplama', 'percin_somun') or a.endswith('_burc'))): continue
    for b in P:
        if b == a or P[b]['tur'] == 'kablo' or b.startswith(('b_', 'kaynak_', 'punta_', 'yap_')) and not (b.startswith('b_') and (P[b].get('etur') in ('percin', 'pul', 'saplama', 'sac') or not P[b].get('etur'))): continue
        if np.all(HIa_[b] >= LOa_[a] - 0.3) and np.all(LOa_[b] <= HIa_[a] + 0.3):
            HARIC[tuple(sorted((a, b)))] = 'kör perçin / PEM saplama / aralık burcu kendi deliğinde: gövde düz girer, perçin ucu sıkılınca şişer (model sıkılmış hâli) · saplama baskıyla oturur'
for ck in D['CEKD']:
    har(ck + '_kayis', ck + '_kasnak', 'kayış dişi motor kasnağına oturur (model teması)')
    har(ck + '_kayis', ck + '_avara', 'kayış dişi avara kasnağına oturur (model teması)')
    har(ck + '_kayis', ck + '_cene_alt', 'kayış çene arasında sıkışır'); har(ck + '_kayis', ck + '_cene_ust', 'kayış çene arasında sıkışır')
    har(ck + '_kayis', ck + '_cene_vida', 'çene cıvatası kayış deliğinden geçer')
# ------------------------------------------------------------------ 1. yol denetimi
t1 = time.time()
DN = Y.Denetci(Pm, HAR, {}, GOR, set(IST), set(), set(HARIC))
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
            ob = ofs_t(b, tt); l2 = LOa[b] + ob; h2 = HIa[b] + ob
            if np.any(l2 > hi + 0.01) or np.any(h2 < lo - 0.01): continue
            if P[b].get('sac') == a or b.startswith(('yap_', 'punta_')): continue
            Bt = TRI[b] + ob
            sa = np.all(A.min(1) <= h2, 1) & np.all(A.max(1) >= l2, 1)
            sb = np.all(Bt.min(1) <= hi, 1) & np.all(Bt.max(1) >= lo, 1)
            if not sa.any() or not sb.any(): continue
            c = int(Y.poz_kesisim(np.ascontiguousarray(A[sa] / 1000), np.ascontiguousarray(Bt[sb] / 1000), 3e-4).sum())
            if c: KARE_SORUN.append((a, round(tt, 2), 'kesişiyor: %s (%d üçgen)' % (b, c)))
print('ÜRETİM KARELERİ: %d sorun' % len(KARE_SORUN)); [print('  ', s) for s in KARE_SORUN[:20]]
# ------------------------------------------------------------------ 3. belirme · havada · son konum
BELIRME = [a for a in GOS if a not in IST and a not in FR and not MF.get(a, {}).get('buyu') and not any(abs(h[2]) + abs(h[3]) + abs(h[4]) > 1e-9 for h in HAR[a])]
TEM = {} if HIZLI else Y.temas_denetim(Pm, HAR, GOR, set(IST), set(), tol=6e-4, turler=('ray', 'sac', 'mek', 'baglanti', 'kapak', 'profil', 'pu'))
HAVADA = sorted(a for a, (tl, l) in TEM.items() if not l and not a.endswith('_ara') and not P[a].get('ev') and not P[a].get('tezgah') and not P[a].get('fikstur'))   # üretimde preslenen / kaynaklanan, tezgâhta bağlanan, kaynak fikstüründe duran elemanlar
from havada_grup import havada_grup
HAVADA = havada_grup(HAVADA, P, Pm, HAR, GOR)
SON = {} if HIZLI else Y.son_kesisim(Pm, GOS, 3e-4)
KAYNAK_ADS = set(a for a in P if P[a]['tur'] in ('kaynak', 'silikon'))
son_rap = {}
for (a, b), n in SON.items():
    if a in KAYNAK_ADS or b in KAYNAK_ADS: continue
    son_rap['%s ↔ %s' % (a, b)] = dict(ucgen=n, neden=HARIC.get((a, b), ''))
print('BELİRME', BELIRME[:10], len(BELIRME), '· HAVADA', HAVADA)
print('SON KONUM kesişimleri:'); [print('  ', k, v) for k, v in list(son_rap.items())[:40]]
# son konum ↔ model (sac: açınımdan kurulan ağ ↔ ana model v9l kutusu)
SK = []
for a in P:
    if 'model_lo' in P[a]:
        f = max(np.abs(LOa[a] - P[a]['model_lo']).max(), np.abs(HIa[a] - P[a]['model_hi']).max()); SK.append((a, round(float(f), 4)))
SK.sort(key=lambda x: -x[1])
print('SAC ↔ MODEL en büyük kutu farkı:', SK[:5])
# ------------------------------------------------------------------ 4. vida / delik / diş (kural 18) — eksen boyunca ölçü
def uc(a, eks):
    V = P[a]['V']; e = np.asarray(eks, float); s = V @ e; return float(s.max())
VD = []
def vida_kayit(ad, std, eks, delik, karsi, dis_bas, dis_son, adet, not_=''):
    s = uc(ad, eks)
    kav = max(0.0, min(s, dis_son) - dis_bas); tasma = s - dis_son
    VD.append(dict(eleman=ad, std=std, adet=adet, delik=delik, karsi=karsi, kavrama_mm=round(kav, 2), uc_tasma_mm=round(tasma, 2), not_=not_))
ck0 = sorted(D['CEKD'])[0]
for ck in sorted(D['CEKD']):
    xs = P[ck + '_ray_sol']['V'][:, 0].min(); xd = P[ck + '_ray_sag']['V'][:, 0].max()
    # sol ray vidası −x yönünde: PEM gövdesi bölme sacının içinde (sac 1,2 → diş boyu 2,0) — v3 tek çekmece ölçüsü (ray dış yüzünden)
    vida_kayit(ck + '_vida_sol', 'DIN 7991 M5 × 6', (-1, 0, 0), 'ray dış eleman havşası', 'PEM SP-M5-1 (bölme sacı)', -(xs - 0.23), -(xs - 2.23), 3)
    vida_kayit(ck + '_vida_sag', 'DIN 7991 M5 × 6', (1, 0, 0), 'ray dış eleman havşası', 'PEM SP-M5-1 (bölme sacı)', xd + 0.23, xd + 2.23, 3)
    zb = P[ck + '_tahrik_vida']['V'][:, 2].min()
    vida_kayit(ck + '_tahrik_vida', 'DIN 7991 M5 × 6', (0, 0, -1), 'motor braketi Ø5,5 + havşa', 'PEM SP-M5-1 (arka iç sac)', 790.23, 792.23, 2)
    ys = P[ck + '_cene_somun']['V'][:, 1]
    vida_kayit(ck + '_cene_vida', 'ISO 7380 M3 × 12', (0, -1, 0), 'tabla + üst çene + alt gövde Ø3,4', 'ISO 4032 M3 somun', -ys.max(), -ys.min(), 2)
yb = P['percin_sase']['V'][:, 1]
vida_kayit('sase_civata', 'ISO 4762 M8 × 16', (0, -1, 0), 'dış taban Ø15,5 + pul', 'M8 kapalı uçlu perçin somun (şase üst duvarı, iç diş dibi y 107,5)', -124.5, -107.5, 10, 'kapalı uç: cıvata ucu diş dibinin %.1f mm üstünde' % (uc('sase_civata', (0, -1, 0)) * -1 - 107.5))
for r in VD[:6] + VD[-1:]: print('  VİDA', r)
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
    if a in IST: PARCA[a]['k'] = 1
    o0 = ofs_t(a, -1.0) / 1000.0; LOt = np.minimum(LOt, V.min(0) + np.minimum(o0, 0)); HIt = np.maximum(HIt, V.max(0) + np.maximum(o0, 0))
n = G.glb_yaz(os.path.join(OUT, 'b_montaj.glb'), dug, MATS)
DEN = dict(model_acigi=sum(1 for k, v in HARIC.items() if v.startswith('MODEL AÇIĞI')), adim=len(D['ADIM']), parca=len(GOS), cevre=0, cift=DN.ciftsay, cakisma=len(CAK), cakismalar=CAK, adim_mm=2.0,
           uretim_kare_sorun=[list(x) for x in KARE_SORUN], belirme=len(BELIRME), belirme_liste=BELIRME, havada=HAVADA, son_konum=son_rap,
           haric={'%s ↔ %s' % k: v for k, v in HARIC.items()}, vida=VD, sac_model=SK[:10], plan_sorun=D['PLAN_SORUN'],
           istisna=sorted(IST), uretilen=sorted(FR), siyirma_mm=Y.SINIR * 1000, oturma_mm=Y.OTURMA * 1000)
OUTJ = dict(surum='b_montaj_v4', ist='B', tarih='4 Eki 2026', kaynak='hat3_v9s.glb (zincir 00–51, adım 37 v2 ile · sayfa ?v=9t) · B gövdesi h3_b_sac_v1 (açınım) + ana model · üretim: b4_montaj.py', sehpa=False,
            birim='m', toplam=D['TOPLAM'], zarf=[np.round(np.maximum(LOt, [-1, 0, -3]), 3).tolist(), np.round(np.minimum(HIt, [7, 3, 4]), 3).tolist()], ghost=[], ghost_t=None,
            adimlar=D['ADIM'], olaylar=sorted(D['OLAY'], key=lambda o: o[0]), kamera=D['KAM'], parcalar=PARCA, acinim=D['ACN'],
            sayim=dict(gosterilen=len(GOS), cevre=0, ucgen=int(sum(len(P[a]['F']) for a in P)), uretilen=len(FR),
                       sac=len(D['SAC_AD']), baglanti=sum(1 for a in GOS if P[a]['tur'] == 'baglanti'), kaynak=sum(1 for a in GOS if P[a]['tur'] == 'kaynak')), denetim=DEN)
json.dump(OUTJ, open(os.path.join(OUT, 'b_montaj.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
json.dump(DEN, open('sonuc_b3.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1, default=str)
print('GLB %.2f MB · JSON yazıldı · zarf %s' % (n / 1e6, OUTJ['zarf']))
