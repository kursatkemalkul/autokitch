# -*- coding: utf-8 -*-
"""çekmece montaj v2 · denetim (kural 17–18) + çıktı (GLB morph + JSON). Girdi: plan_v2.pkl (cek_montaj_v2.py)"""
import sys, os, json, pickle, time, math
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
sys.path.insert(0, os.path.join(HERE, '..', 'adim6')); sys.path.insert(0, HERE); sys.stdout.reconfigure(encoding='utf-8')
import yol_denetim_v2 as Y
import v2geo as G
Y.ADIM = 0.002
W = r'C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH_COORDINATION\worktrees\claude-hat3-v8'
OUT = os.path.join(W, 'otonom', 'hat3d', 'v3', 'cekmece_montaj')
D = pickle.load(open('plan_v2.pkl', 'rb')); D['KAM'].sort(key=lambda k: k[0])
P, HAR, GOR, MF, FR, VU, IST = D['P'], D['HAR'], D['GOR'], D['MF'], D['FRAMES'], D['VU'], D['ISTISNA']
CEV = [a for a in P if P[a]['tur'] == 'cevre']
for a in CEV: GOR[a] = 0.0; HAR.setdefault(a, [])
GOS = [a for a in P if a not in CEV]
print('parça %d · çevre %d · süre %.1f' % (len(GOS), len(CEV), D['TOPLAM']))
print('KIYAS (üretilen ↔ model):'); [print('  ', k, v) for k, v in D['KIYAS'].items()]

# ------------------------------------------------------------------ 1. yol denetimi (rijit hareketler, 2 mm, üçgen CCD)
Pm = {a: dict(V=P[a]['V'] / 1000.0, F=P[a]['F'], tur=P[a]['tur']) for a in P}
KAY = set(IST)
# bilinen / beyan edilen hariç çiftler (son konumda zaten geçme: delik modele işlenmemiş çevre parçası)
ARKA_VIDA = ['vida_braket_1', 'vida_braket_2']
HARIC = {}
def har(a, b, neden):
    HARIC[tuple(sorted((a, b)))] = neden
for v in ARKA_VIDA:
    har(v, 'cevre_sac', 'arka iç sacda PEM deliği modelde yok (eklenecek) — PEM çevrede gösterildi')
    har(v, 'cevre_pu', 'köpük kapağı yeri PU\'da kesilmedi (çevre, eklenecek)')
for k_ in ('sol', 'sag'):
    for i in (1, 2): har('pem_kapak_%s_%d' % (k_, i), 'kapak_ic', 'PEM FHS başı iç panelde kenetli (presleme)')
har('arka_kasnak', 'kayis', 'kayış dişi kasnak dişine oturur (model teması)')
for i in (1, 2):
    har('percin_%d' % i, 'cevre_on_cerceve', 'ön çerçevede Ø3,3 perçin deliği modelde yok (eklenecek)')
for v in ['vida_sol_%d' % k for k in (1, 2, 3)] + ['vida_sag_%d' % k for k in (1, 2, 3)]:
    har(v, 'cevre_kopuk_kapagi', 'M5 × 6 ucu köpük kapağı tabanına 0,77 mm giriyor (onaylı M5 × 6; kapak 1 mm derin olmalı) — AÇIK')
t1 = time.time()
DN = Y.Denetci(Pm, HAR, {}, GOR, KAY, set(), set(HARIC))
CAK = DN.denetle(ilerleme=False)
print('YOL: çift %d · çakışma %d · %.0f s' % (DN.ciftsay, len(CAK), time.time() - t1), flush=True)
for r in CAK: print('  ÇAKIŞMA', r)

# ------------------------------------------------------------------ 2. üretim kareleri (büküm / çevirme / PEM) — tezgâh + o an görünen parçalar
def ofs_t(a, tt):
    o = np.zeros(3)
    for h in HAR[a]:
        u = 1.0 if tt >= h[1] else (0.0 if tt <= h[0] else (tt - h[0]) / (h[1] - h[0]))
        o += np.array(h[2:5]) * 1000.0 * (1 - u * u * (3 - 2 * u))
    return o


def kare_zaman(a):
    """kare k → zaman (segment uçları)"""
    seg = MF[a]['seg']; T = {}
    for t0, t1_, k0, k1 in seg: T.setdefault(k0, t0); T[k1] = t1_
    return T


URT_TOP = 421.5
KARE_SORUN = []
TRI = {a: P[a]['V'][P[a]['F']] for a in P}
for a in FR:
    T = kare_zaman(a); o0 = ofs_t(a, -1.0)
    ks = sorted(T)
    for i, k in enumerate(ks):
        X = P[a]['V'] + o0 + FR[a][k]
        Xs = [(X, T[k])]
        if i + 1 < len(ks):
            X2 = P[a]['V'] + o0 + FR[a][ks[i + 1]]; Xs.append(((X + X2) / 2, (T[k] + T[ks[i + 1]]) / 2))
        for XX, tt in Xs:
            if XX[:, 1].min() < URT_TOP - 0.05 and XX[:, 0].min() > 2230:
                KARE_SORUN.append((a, round(tt, 2), 'tezgâha giriyor %.2f mm' % (URT_TOP - XX[:, 1].min())))
            A = XX[P[a]['F']]; lo, hi = XX.min(0), XX.max(0)
            for b in P:
                if b == a or b in ('tezgah_uretim',) or MF.get(b, {}).get('bagli') == a or MF.get(a, {}).get('bagli') == b: continue
                if b in GOR and GOR[b] > tt: continue
                ob = ofs_t(b, tt) if b not in CEV else np.zeros(3)
                if b in FR and tt < max(kare_zaman(b).values()) + 1e-6 and tt >= GOR.get(b, 0): continue   # diğer üretim parçası kendi denetiminde
                Vb = P[b]['V'] + ob
                if np.any(Vb.min(0) > hi + 0.01) or np.any(Vb.max(0) < lo - 0.01): continue
                Bt = TRI[b] + ob
                sa = np.all(A.min(1) <= Vb.max(0), 1) & np.all(A.max(1) >= Vb.min(0), 1)
                sb = np.all(Bt.min(1) <= hi, 1) & np.all(Bt.max(1) >= lo, 1)
                if not sa.any() or not sb.any(): continue
                c = int(Y.poz_kesisim(np.ascontiguousarray(A[sa] / 1000), np.ascontiguousarray(Bt[sb] / 1000), 3e-4).sum())
                if c: KARE_SORUN.append((a, round(tt, 2), 'kesişiyor: %s (%d üçgen)' % (b, c)))
print('ÜRETİM KARELERİ: %d sorun' % len(KARE_SORUN)); [print('  ', s) for s in KARE_SORUN[:30]]

# ------------------------------------------------------------------ 3. belirme · havada · son konum kesişimleri
BELIRME = [a for a in GOS if a not in IST and a not in FR and not any(abs(h[2]) + abs(h[3]) + abs(h[4]) > 1e-9 for h in HAR[a])]
TEM = Y.temas_denetim(Pm, HAR, GOR, KAY, set(), tol=6e-4, turler=('ray', 'sac', 'mek', 'baglanti', 'kapak'))
HAVADA = sorted(a for a, (tl, l) in TEM.items() if not l and not a.startswith('ara_ray_'))   # ara eleman dış elemanın bilyalı kafesinde (katalog ünite, aynı hareket)
SON = Y.son_kesisim(Pm, GOS + CEV, 3e-4)
SON = {k: v for k, v in SON.items() if not (k[0] in CEV and k[1] in CEV)}
KAYNAK_ADS = set(D['KAYNAK'])
son_rap = {}
for (a, b), n in SON.items():
    if a in KAYNAK_ADS or b in KAYNAK_ADS: continue          # dikiş / punta iki parçaya biner (tasarım)
    son_rap['%s ↔ %s' % (a, b)] = dict(ucgen=n, neden=HARIC.get((a, b), ''))
print('BELİRME', BELIRME, '· HAVADA', HAVADA)
print('SON KONUM kesişimleri:'); [print('  ', k, v) for k, v in son_rap.items()]

# ------------------------------------------------------------------ 4. vida / delik / diş eşleşmesi (kural 18)
def uc(a, eks):
    V = P[a]['V']; e = np.asarray(eks, float); s = V @ e; return V[np.argmax(s)], float(s.max())
VD = []
def vida_kayit(ad, std, eks, delik_yeri, karsi, dis_bas, dis_son, not_=''):
    p, s = uc(ad, eks); e = np.asarray(eks, float)
    kav = max(0.0, min(s, dis_son) - dis_bas)                 # eksen üzerinde diş kavrama boyu
    tasma = s - dis_son
    VD.append(dict(eleman=ad, std=std, delik=delik_yeri, karsi=karsi, kavrama_mm=round(kav, 2), uc_tasma_mm=round(tasma, 2), not_=not_))
# ray vidası: eksen −x (sol) / +x (sağ); PEM diş x 1451,27–1453,27 (sol) · köpük kapağı iç tabanı 1451,27
for k in (1, 2, 3):
    vida_kayit('vida_sol_%d' % k, 'DIN 7991 M5 × 6', (-1, 0, 0), 'ray dış eleman havşası + ara eleman erişim deliği', 'PEM SP-M5-1 (bölme sacı)', -1453.27, -1451.27,
               'uç PEM arkasından kapak tabanına girer (kapak iç tabanı = PEM arkası)')
    vida_kayit('vida_sag_%d' % k, 'DIN 7991 M5 × 6', (1, 0, 0), 'ray dış eleman havşası + ara eleman erişim deliği', 'PEM SP-M5-1 (bölme sacı)', 2073.73, 2075.73,
               'uç PEM arkasından kapak tabanına girer')
for i in (1, 2):
    vida_kayit('vida_braket_%d' % i, 'DIN 7991 M5 × 6', (0, 0, -1), 'motor braketi tabanı Ø5,5 + havşa', 'PEM SP-M5-1 (arka iç sac, eklendi)', 790.23, 792.0, 'uç köpük kapağı boşluğunda (1,0 pay)')
for i in range(1, 5):
    vida_kayit('vida_motor_%d' % i, 'DIN 7991 M3 × 6', (1, 0, 0), 'motor braketi Ø3,4 + havşa (3 mm sacta gömme)', 'redüktör yüzü M3 dişli delik (derinlik 5)', 1484.0, 1489.0)
for nm in ('vida_kose_sol_1', 'vida_kose_sol_2', 'vida_kose_sag_1', 'vida_kose_sag_2'):
    vida_kayit(nm, 'ISO 7380 M4 × 6', (0, -1, 0), 'köşebent Ø4,5', 'lamada M4 dişli kör delik (5 derin, 6 mm lama)', -426.5, -421.4)
for i in (1, 2):
    vida_kayit('vida_cene_%d' % i, 'ISO 7380 M3 × 10', (0, -1, 0), 'üst çene + ara parça + alt çene Ø3,4', 'ISO 4032 M3 somun (alt çenenin altında)', -457.95, -455.55, 'somundan 1,3 taşar (≥ 1 diş)')
for k_ in ('sol', 'sag'):
    for i in (1, 2):
        vida_kayit('pem_kapak_%s_%d' % (k_, i), 'PEM FHS-M5-10 saplama', (0, 0, -1), 'braket flanşı Ø5,5', 'DIN 125 M5 pul + ISO 4032 M5 somun', -36.0, -31.3, 'somundan 1,3 taşar')
for r in VD: print('  VİDA', r)
D_EKSIK = [r for r in VD if r['kavrama_mm'] <= 0]

# ------------------------------------------------------------------ 5. açınım 2B (inset)
ACN = []
for e_ in D['ACN']:
    a = e_['ad']; s = D['SAC'][a]
    # düz kare (k=1) yerel → tezgâh düzlemi (x, z)
    X = P[a]['V'] + ofs_t(a, -1) + FR[a][1]
    F = P[a]['F']; PI = None
    # paneller: köşe → panel indisi plan pickle'da yok → büküm çizgisi için ebeveyn / çocuk sınırını kare 1'de bul
    lo, hi = X.min(0), X.max(0)
    ACN.append(dict(ad=a, t0=e_['t0'], t1=e_['t1'], ac=D['YAPI'][a]['ac'], t=s['t'], nb=len(s['bukum']),
                    bukum=[dict(no=b['no'], aci=b['aci'], ack=b['ack']) for b in s['bukum']],
                    levha=[round(float(hi[0] - lo[0]), 1), round(float(hi[2] - lo[2]), 1), round(float(hi[1] - lo[1]), 1)]))

# ------------------------------------------------------------------ 6. çıktı
MATAD = ['sac', 'kapak', 'profil', 'kaynak', 'baglanti', 'arayuz', 'pu', 'yalitim', 'mekanizma', 'motor', 'alu', 'koyu', 'sensor', 'elektrik',
         'kanal', 'fis', 'guc', 'bilgi', 'hava', 'kapak_s', 'urun', 'silik', 'tezgah', 'tepsi']
MATS = [dict(name=m, pbrMetallicRoughness=dict(baseColorFactor=[0.8, 0.8, 0.8, 1], metallicFactor=0.5, roughnessFactor=0.4)) for m in MATAD]
os.makedirs(OUT, exist_ok=True)
dug, PARCA = [], {}
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
n = G.glb_yaz(os.path.join(OUT, 'cekmece_montaj.glb'), dug, MATS)
DEN = dict(adim=len(D['ADIM']), parca=len(GOS), cevre=len(CEV), cift=DN.ciftsay, cakisma=len(CAK), cakismalar=CAK, adim_mm=2.0,
           uretim_kare_sorun=[list(x) for x in KARE_SORUN], belirme=len(BELIRME), havada=HAVADA, son_konum=son_rap,
           haric={'%s ↔ %s' % k: v for k, v in HARIC.items()}, vida=VD, kiyas=D['KIYAS'], eklenen_cevre=D['EKLENEN_CEVRE'], delik_acilan=D['DELIK_ACILAN'],
           istisna=sorted(IST), uretilen=sorted(FR), siyirma_mm=Y.SINIR * 1000, oturma_mm=Y.OTURMA * 1000)
OUTJ = dict(surum='cekmece_montaj_v2', ist='CEKMECE', tarih='4 Eki 2026', kaynak='hat3_v9j.glb · CEK_K2_lahm_3 + B gövdesi (silik) · üretim: cek_montaj_v2.py',
            birim='m', toplam=D['TOPLAM'], zarf=[[1.40, 0.0, -0.80], [3.64, 0.70, 1.00]], ghost=[], ghost_t=None,
            adimlar=D['ADIM'], olaylar=D['OLAY'], kamera=D['KAM'], parcalar=PARCA, acinim=ACN,
            sayim=dict(gosterilen=len(GOS), cevre=len(CEV), ucgen=int(sum(len(P[a]['F']) for a in P)), uretilen=len(FR),
                       baglanti=sum(1 for a in GOS if P[a]['tur'] == 'baglanti'), kaynak=len(KAYNAK_ADS)), denetim=DEN)
json.dump(OUTJ, open(os.path.join(OUT, 'cekmece_montaj.json'), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
json.dump(DEN, open('sonuc_v2.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1, default=str)
print('GLB %.2f MB · JSON yazıldı' % (n / 1e6))
