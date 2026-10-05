# -*- coding: utf-8 -*-
"""adım 6 · istasyon montaj animasyonu verisi (A, B, E, U, TOPPING, F) — K montaj v1 (hazirla.py) yöntemi
girdi : gece2/adim5/<IST>_sac_v1.glb (üretim sacı, dünya m) + acinim_<IST>/*.json + ana_<IST>.pkl (ana GLB v8zq'dan gövde-dışı parçalar, ana_cek.py)
çıktı : <W>/otonom/hat3d/v3/<ist>_montaj/<ist>_montaj.glb + .json
Hareket modeli (sayfa ile birebir): konum = son + Σ d·(1 − e(u)) · kapak: R_y(Σ a·e(u)) kendi menteşe ekseni etrafında · e = smoothstep
Ağ sadeleştirme YALNIZ bu animasyon kopyasında (vtkQuadricDecimation): bağlantı elemanları, PU ve ana GLB'den gelen büyük gruplar."""
import json, os, re, math, struct, sys, pickle
import numpy as np
sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import glbio
IST = sys.argv[1].upper()
ist = IST.lower()
A5 = os.path.join(os.path.dirname(HERE), 'adim5')
WT = r'C:/Users/Kemal/Desktop/Kemal/WEBSİTE/AUTOKITCH_COORDINATION/worktrees/claude-hat3-v8'
OUT = os.path.join(WT, 'otonom', 'hat3d', 'v3', '%s_montaj' % ist)
os.makedirs(OUT, exist_ok=True)

# ------------------------------------------------------------------ sadeleştirme (vtk)
import vtk
from vtk.util.numpy_support import numpy_to_vtk, vtk_to_numpy, numpy_to_vtkIdTypeArray


def sadele(V, F, hedef):
    n = len(F)
    if hedef >= n or n < 40: return V, F
    pts = vtk.vtkPoints(); pts.SetData(numpy_to_vtk(np.ascontiguousarray(V, np.float64), deep=1))
    cells = np.hstack([np.full((n, 1), 3, np.int64), F.astype(np.int64)]).ravel()
    ca = vtk.vtkCellArray(); ca.SetCells(n, numpy_to_vtkIdTypeArray(cells, deep=1))
    pd = vtk.vtkPolyData(); pd.SetPoints(pts); pd.SetPolys(ca)
    cl = vtk.vtkCleanPolyData(); cl.SetInputData(pd); cl.SetTolerance(1e-7); cl.Update()
    d = vtk.vtkQuadricDecimation(); d.SetInputConnection(cl.GetOutputPort())
    d.SetTargetReduction(max(0.0, min(0.97, 1 - hedef / n))); d.VolumePreservationOn(); d.Update()
    o = d.GetOutput()
    if o.GetNumberOfPolys() < 4: return V, F
    V2 = vtk_to_numpy(o.GetPoints().GetData()).astype(np.float64)
    F2 = vtk_to_numpy(o.GetPolys().GetData()).reshape(-1, 4)[:, 1:]
    return V2, F2


# ------------------------------------------------------------------ parçalar
J, SP = glbio.oku(os.path.join(A5, '%s_sac_v1.glb' % IST))
P = {}          # ad -> dict(V, F, m, kaynak='sac'|'ana', tur)
for ad, p in SP.items():
    tur = p['extras'].get('tur') or p['mat']
    V, F = p['V'], p['F']
    n = len(F)
    if tur in ('baglanti', 'arayuz') and n > 120: V, F = sadele(V, F, max(60, int(n * 0.2)))
    elif tur == 'pu' and n > 2000: V, F = sadele(V, F, int(n * 0.35))
    elif tur == 'kaynak' and n > 300: V, F = sadele(V, F, max(120, int(n * 0.4)))
    m = 'arayuz' if tur == 'arayuz' else {'sac': 'sac', 'kapak': 'kapak', 'profil': 'profil', 'kaynak': 'kaynak', 'baglanti': 'baglanti',
                                          'pu': 'pu', 'yalitim': 'yalitim'}.get(tur, 'sac')
    P[ad] = dict(V=V, F=F, m=m, kay='sac', tur=tur, birim=p['extras'].get('birim', ''))


def kat_ana(mat, dugum, mek_kod):
    m = mat.lower()
    if 'kablo_guc' in m or 'kod_kirmizi' in m or m == 'kablo': return 'guc'
    if 'kablo_veri' in m or 'kablo_sinyal' in m or 'kod_mavi' in m: return 'bilgi'
    if 'hava' in m or mek_kod.endswith('/Hava'): return 'hava'
    if 'kanal' in m: return 'kanal'
    if m.split('__')[0] in ('harting', 'm12', 'rakor', 'etiket', 'lastik_gecit', 'tapa'): return 'fis'
    if 'on_seffaf' in m: return 'kapak_s'
    if m.startswith('motor'): return 'motor'
    if m.split('__')[0] in ('pano', 'cihaz', 'cihaz_koyu', 'din', 'siemens', 'beckhoff', 'kart', 'salter', 'salter_sari', 'salter_kirmizi',
                            'salter_mil', 'salter_somun'): return 'elektrik'
    if m.split('__')[0] in ('hamur', 'kutu_icecek', 'karton', 'karton_yigin', 'sos', 'poset', 'top') or dugum.startswith(('URUN', 'E_PIZZA', 'E_KUTU')): return 'urun'
    if 'sensor' in m: return 'sensor'
    if m.startswith('pu'): return 'pu'
    if m.split('__')[0] in ('silikon', 'conta', 'koyu', 'plastik', 'pom', 'uhmw', 'kayis', 'vakum_kaucuk', 'siyah', 'gfrp', 'bronz'): return 'koyu'
    if m.startswith('aluminyum'): return 'alu'
    return 'mekanizma'


ANA = pickle.load(open(os.path.join(HERE, 'ana_%s.pkl' % IST), 'rb'))
ANA_BILGI = {}
KUMELE = IST in ('TOPPING', 'F')       # TOPPING / F: ana grup → bağlı bileşen kümeleri (kart, kutu, evaporatör ayrı ayrı yerleşsin)
if KUMELE:
    from _kume import kumele


def _ana_ekle(ad, g, V, F, kume=None):
    n = len(F)
    hedef = n if n <= 600 else min(int(600 + 0.25 * (n - 600)), int(3500 + 0.05 * n))
    V, F = sadele(V, F, hedef)
    k = kat_ana(g['mat'], g['dugum'], g['mek_kod'])
    if g['dugum'] == 'F_UST_KABIN__plastik': k = 'fis'          # rakor gövdeleri
    P[ad] = dict(V=V, F=F, m=k, kay='ana', tur=k, birim=g['mek_kod'])
    ANA_BILGI[ad] = dict(dugum=g['dugum'], mek=g['mek_kod'], kpk=g['kpk'], ucgen0=n, ucgen=len(F))
    if kume is not None: ANA_BILGI[ad]['kume'] = kume


for g in ANA:
    ad = 'M__%s__%d%s' % (g['dugum'], g['mek'], '_k' if g['kpk'] else '')
    V, F = g['V'].astype(np.float64), g['F'].astype(np.int64)
    ks = kumele(V, F) if KUMELE else [None]
    if len(ks) == 1 or len(ks) > 60:
        _ana_ekle(ad, g, V, F)
    else:
        ks = sorted(ks, key=lambda s: tuple(np.round(V[F[s]].reshape(-1, 3).min(0), 3)))
        for i, s in enumerate(ks):
            Fi = F[s]; u, inv = np.unique(Fi.reshape(-1), return_inverse=True)
            _ana_ekle('%s__c%02d' % (ad, i), g, V[u], inv.reshape(-1, 3), i)

HAR = {a: [] for a in P}
ROT = {a: [] for a in P}
GOR, KAY = {}, set()
ADIM, KAM, OLAY = [], [], []
GIZLI = set()     # gösterilmeyen (arayüz: karşı parça bu sayfada yok)


def cent(a):
    V = P[a]['V']; return (V.min(0) + V.max(0)) / 2


def bbox(adlar):
    lo = np.min([P[a]['V'].min(0) for a in adlar], 0); hi = np.max([P[a]['V'].max(0) for a in adlar], 0); return lo, hi


def _h(a, t0, t1, d):
    HAR[a].append([round(t0, 3), round(t1, 3)] + [round(float(x), 5) for x in d])


def bekle(a):
    assert a not in GOR, 'iki kez: ' + a


def gel(adlar, d, t0, sure, ara=0.0):
    t = t0
    for a in adlar:
        bekle(a); _h(a, t, t + sure, d); GOR[a] = round(t, 3); t += ara
    return (t - ara + sure) if adlar else t0


def kaynak(adlar, t0, sure=0.45, ara=0.05):
    if len(adlar) > 24: ara = min(ara, 2.4 / len(adlar))
    t = t0
    for a in adlar:
        bekle(a); KAY.add(a); GOR[a] = round(t, 3); _h(a, t, t + sure, (0, 0, 0)); t += ara
    return (t - ara + sure) if adlar else t0


def yerinde(adlar, t0, sure=0.6, ara=0.0):
    return kaynak(adlar, t0, sure, ara)


def ofset(adlar, d, t0, t1):
    for a in adlar: _h(a, t0, t1, d)


def kalan(): return [a for a in P if a not in GOR and a not in GIZLI]


def R(rx, havuz=None):
    """henüz yerleşmemiş ve rx'e uyan parçalar (sıralı)"""
    h = havuz if havuz is not None else P
    return sorted(a for a in h if a not in GOR and a not in GIZLI and re.search(rx, a))


def olay(t, m): OLAY.append([round(t, 2), m])


ZARF = np.array([np.min([P[a]['V'].min(0) for a in P if P[a]['kay'] == 'sac'], 0),
                 np.max([P[a]['V'].max(0) for a in P if P[a]['kay'] == 'sac'], 0)])
if IST == 'F':     # F sacı fırının üstünde; kamera fırını da kapsasın
    ZARF = np.array([np.min([P[a]['V'].min(0) for a in P], 0), np.max([P[a]['V'].max(0) for a in P], 0)])
MERKEZ = ZARF.mean(0); BOY = float(np.linalg.norm(ZARF[1] - ZARF[0]))


def _fit(lo, hi):
    w = hi - lo
    span = max(w[1] * 1.1, (w[0] + w[2] * 0.5) / 1.9, 0.25)
    return span * 2.18 + w[2] / 2


def kam(t, adlar=None, d=(0, 1, 0), uzak=None, yon=None):
    genel = _fit(ZARF[0], ZARF[1])
    if adlar:
        lo, hi = bbox(adlar); h = (lo + hi) / 2
    else:
        lo, hi = ZARF[0], ZARF[1]; h = MERKEZ.copy()
    if yon is None:
        d = np.array(d, float); yon = np.array([0.55, 0.5, 1.0])
        if abs(d[2]) > 1e-9 and d[2] < 0 and abs(d[2]) >= abs(d[0]): yon = np.array([0.6, 0.5, -1.0])
        elif abs(d[0]) > abs(d[2]) and abs(d[0]) > 1e-9: yon = np.array([1.0 * np.sign(d[0]), 0.55, 0.75])
    yon = np.array(yon, float); yon /= np.linalg.norm(yon)
    dist = uzak * 1.6 if uzak else min(max(_fit(lo, hi), genel * 0.45), genel * 1.05)
    pos = h + yon * dist
    pos[1] = max(pos[1], 0.25)
    KAM.append([round(t, 2), [round(float(v), 4) for v in pos], [round(float(v), 4) for v in h]])


def adim(no, ad, t0, t1, metin, liste, kart='3b'):
    ADIM.append(dict(no=no, ad=ad, t0=round(t0, 3), t1=round(t1, 3), metin=metin, liste=liste, kart=kart))


def somunlar(saplamalar, t, L=0.045):
    """saplama → pul + somun (saplama ekseni boyunca, saplamadan somuna)"""
    for s in saplamalar:
        o = s[:-len('_saplama')]
        pul, som = o + '_pul', o + '_somun'
        V = P[s]['V']; i = int(np.argmax(V.max(0) - V.min(0)))
        n = np.zeros(3)
        if som in P: n[i] = np.sign(cent(som)[i] - cent(s)[i]) or 1
        else: n[i] = 1
        if pul in P and pul not in GOR: gel([pul], n * L, t, 0.4)
        if som in P and som not in GOR: gel([som], n * L * 1.4, t + 0.2, 0.45)
        t += 0.05 if len(saplamalar) > 20 else 0.09
    return t + 0.5


def saplamali(rx_sac, d, t, sure=1.4, ek=()):
    """sac + üstündeki preslenmiş saplamalar birlikte gelir; dönüş: (t, saplamalar)"""
    sap = R(rx_sac)
    gel(list(ek), d, t, sure)
    return t + sure, sap


# ------------------------------------------------------------------ açınım 2B (adım 1–3, K ile aynı biçim)
def cizgi(s, n=10):
    if s['t'] == 'L': return [s['p'][0], s['p'][1]]
    if s['t'] == 'A':
        (x0, y0), (xm, ym), (x1, y1) = s['p']; cx, cy = s['c']; r = s['r']
        a0 = math.atan2(y0 - cy, x0 - cx); am = math.atan2(ym - cy, xm - cx); a1 = math.atan2(y1 - cy, x1 - cx)
        def yak(a, b):
            while a - b > math.pi: a -= 2 * math.pi
            while b - a > math.pi: a += 2 * math.pi
            return a
        am = yak(am, a0); a1 = yak(a1, am)
        return [[cx + r * math.cos(a0 + (a1 - a0) * i / n), cy + r * math.sin(a0 + (a1 - a0) * i / n)] for i in range(n + 1)]
    cx, cy = s['c']; r = s['r']
    return [[cx + r * math.cos(2 * math.pi * i / 24), cy + r * math.sin(2 * math.pi * i / 24)] for i in range(25)]


def kontur(segs):
    out = []
    for s in segs:
        q = cizgi(s)
        if out and abs(out[-1][0] - q[0][0]) < 1e-6 and abs(out[-1][1] - q[0][1]) < 1e-6: q = q[1:]
        out += q
    return [[round(x, 2), round(y, 2)] for x, y in out]


def acinim_liste(secim):
    ACI = []
    for ad, adet in secim:
        f = os.path.join(A5, 'acinim_%s' % IST, ad + '.json')
        if not os.path.exists(f): print('açınım yok', ad); continue
        d = json.load(open(f, encoding='utf-8'))
        bk = [dict(no=b['no'], ad=b['ad'], aci=b['aci'], yon=b['yon'], R=b['R'], c=[[round(v, 2) for v in p] for p in b['cizgi']],
                   s=[[round(v, 2) for v in p] for p in b['baslangic']], e=[[round(v, 2) for v in p] for p in b['bitis']]) for b in d['bukumler']]
        pem = [dict(c=[round(v, 2) for v in k['merkez_duz']], tip=k.get('parca') or k['tip']) for k in d.get('kesikler', [])
               if 'pem' in (k.get('tip') or '') and k.get('merkez_duz')]
        ACI.append(dict(ad=ad, adet=adet, t=d['t'], R=d['R'], levha=d['levha'], dis=kontur(d['dis_kontur']), ek=[kontur(k) for k in d.get('ek_dis_konturlar', [])],
                        ic=[kontur(k) for k in d['ic_konturlar']], bukum=bk, pem=pem))
    return ACI


def kartlar(t, ozet):
    sac_say = sum(1 for a in P if P[a]['tur'] in ('sac', 'kapak'))
    pro_say = sum(1 for a in P if P[a]['tur'] == 'profil')
    for no, ad, metin, liste in [
        (1, 'Lazer kesim', "Saclar açınım dosyalarından lazerde kesilir: N₂ kesme gazı (oksitsiz, kaynağa hazır kenar), folyolu yüz yukarı. Kare/dikdörtgen borular boru lazerde boy + delik ile kesilir. Bütün kenarlar çapaklanır.",
         '%d sac · %d profil — %s' % (sac_say, pro_say, ozet)),
        (2, 'PEM saplama / somun basma', "PEM elemanlar DÜZ sacta, bükümden ÖNCE preste basılır — büküm sonrası flanş presin alt kalıbına engel olur. FHP saplamaların başı dış yüzle aynı (dışta iz yok); mekanizma ve kutu bağlantıları bu saplamalara pul + fiberli somunla yapılır.",
         'turuncu noktalar = PEM yerleri (açınım üstünde)'),
        (3, 'Abkant büküm', "Abkantta açınımdaki büküm çizgilerinden, numaralı sırayla bükülür (iç R = 1,5 t; K faktörü açınım dosyasında). Folyo üstte kalır.",
         'kırmızı kesik = büküm çizgisi · gri = büküm bölgesi')]:
        adim(no, ad, t, t + 6.0, metin, liste, kart='acinim'); kam(t); t += 6.0
    return t


# ------------------------------------------------------------------ İSTASYON SIRALARI
KAPAK_PIV = {}     # parça -> [px, pz, işaret]
GHOST = []         # silik komşu kutular [x0,x1,y0,y1,z0,z1]
GHOST_T = []
FIKSTUR = None
SECIM = []
MONTAJ_SIRASI = []
BASLIK = {}


def kapak_doner(adlar, piv, aci, t0, t1, t2, t3):
    for a in adlar:
        ROT[a] += [[round(t0, 3), round(t1, 3), aci, piv[0], piv[1]], [round(t2, 3), round(t3, 3), -aci, piv[0], piv[1]]]


def kapak_alt(dis, KAP, t, ic_tava, rx_pem, rx_kars, rx_kanat, rx_kvida, rx_kose, ST=0.9, etiket=''):
    """K yöntemi: kapak tezgâhta (ST önde) kurulur, sonra bütün kapak menteşeye gelir"""
    olay(t, 'Kapak alt montajı %s(tezgâhta, önde): iç tava 1,0 + karşılıklar + menteşe kanatları' % etiket)
    kam(t, [dis], (0, 0, 1), uzak=2.2)
    gel([ic_tava] + R(rx_pem), (0, 0.3, 0), t, 1.0); t += 1.1
    k = R(rx_kars)
    if k: gel(k, (0, 0, 0.07), t, 0.6, 0.1); t += 0.9
    gel(R(rx_kanat), (0, 0, -0.1), t, 0.7, 0.08); t += 1.0
    v = R(rx_kvida)
    if v: gel(v, (0, 0, -0.05), t, 0.4, 0.04); t += 0.8
    olay(t, 'Dış tava 1,5: köşeler bindirme + TIG, iç tavanın üstüne oturur (derz 3 mm) · punta')
    bekle(dis); GOR[dis] = round(t, 3)
    dk = R(rx_kose)
    tk = kaynak(dk, t + 0.5, 0.35, 0.12) + 0.2
    ofset([dis] + dk, (0, 0, 0.35), tk, tk + 0.9)
    TA = tk + 1.2
    olay(TA, 'Kapak önden gelir, menteşelere asılır (kaldır-tak)')
    kam(TA, [dis], (0, 0, 1), uzak=2.4)
    ofset(KAP, (0, 0, ST), TA, TA + 1.8)
    return TA + 2.1


def sac_tamam(t):
    olay(t, '%s üretim sacı gövdesi tamam — şimdi diğer parçalar' % IST)
    kam(t, None); t += 2.2
    ADIM[-1]['t1'] = round(t, 3)
    return t


def seq_A():
    global FIKSTUR
    BASLIK.update(kod='A', ad='A · HAMUR AÇMA — kabuk + açıcı montajı',
                  lead="A istasyonunun üretim sacı gövdesi (kaynaklı kaide, iskelet, 4 bükümlü panel, çift cidarlı kapak) atölyede hangi sırayla, hangi yönden, neyle birleşir; sonra satın alınan açıcı (dönme kafası) kaidedeki M8 PEM'lere oturur. A içinde kablo / hava yok (kural).")
    SECIM[:] = [('sol_yan_sac', 1), ('sag_yan_sac_tabla_gecisi', 1), ('ust_sac', 1), ('arka_sac', 1), ('onyuz_kapak_A', 1), ('onyuz_kapak_A_ic_tava', 1), ('kaide_ust_plaka_4', 1), ('kaide_damlama_saci', 1), ('govde_kulak_sol_on_1080', 22)]
    t = kartlar(0.0, 'kaide 7 boru · 4 dikme · üst halka · 4 panel · kapak dış/iç tava · 22 kulak')
    # 4 kaide
    t4 = t; kam(t, R(r'^kaide_'), (0, 1, 0))
    olay(t, 'Kaide boruları (40 × 100) kaynak fikstürüne: ön, arka, sol, sağ')
    t = gel(R(r'^kaide_(on|arka|sol|sag)_boru$'), (0, 0.45, 0), t, 1.0, 0.2) + 0.1
    olay(t, 'Enine + boyuna borular (açıcı kolonu ve tabla rayının altı) · köşe dikişleri TIG')
    t = gel(R(r'^kaide_(enine|boyuna)_boru'), (0, 0.45, 0), t, 1.0, 0.2)
    t = kaynak(R(r'^kaide_.*boru.*kaynak'), t) + 0.2
    olay(t, 'Kaide üst plakası 4 mm — PEM M8 (açıcı) + M6 (ray) DÜZ sacta basılı geldi')
    t = gel(R(r'^kaide_ust_plaka(_\d+)?$') + R(r'^kaide_ust_plaka_pem_'), (0, 0.55, 0), t, 1.3) + 0.1
    olay(t, '16 delik (tapa) kaynağı plakayı borulara bağlar · yüz taşlanır')
    t = kaynak(R(r'^kaide_ust_plaka_delik_kaynagi'), t, 0.4, 0.06) + 0.2
    olay(t, 'Damlama sacı 1,5 mm alttan, kaide içine · dikmelere 2 dikiş')
    t = gel(R(r'^kaide_damlama_saci$'), (0, -0.35, 0), t, 1.0)
    t = kaynak(R(r'^kaide_damlama_dikme_kaynagi'), t) + 0.4
    adim(4, 'Kaide · kaynaklı alt montaj', t4, t,
         "Kaide 40 × 100 kutu profillerden fikstürde kurulur (kare / diyagonal kontrol). Üst plaka 4 mm'dir; açıcı kolonunun 4 × M8 ve tabla rayının 4 × M6 PEM somunları plakaya düz hâlde basılmıştır. Plaka borulara delik (tapa) kaynağıyla bağlanır; altına damlama sacı gelir.",
         '7 kaide borusu · üst plaka 4 mm (4 PEM M8 + 4 PEM M6) · 16 delik kaynağı · damlama sacı 1,5 mm')
    # 5 iskelet
    t5 = t; kam(t, None)
    olay(t, '4 köşe dikmesi (30 × 30) kaide plakasına · şakül kontrol')
    t = gel(R(r'^kose_dikmesi_\d+_-?\d+$'), (0, 0.7, 0), t, 1.1, 0.2) + 0.1
    olay(t, 'Üst halka (ön, arka, sol, sağ) dikmelerin tepesine · köşe dikişleri')
    t = gel(R(r'^ust_halka_(on|arka|sol|sag)$'), (0, 0.4, 0), t, 1.0, 0.2)
    t = kaynak(R(r'^ust_halka_.*kaynak'), t) + 0.1
    t = gel(R(r'^kose_dikmesi_.*_tapa$'), (0, 0.15, 0), t, 0.6, 0.1) + 0.1
    olay(t, '22 panel kulağı iskelete (kaynak ayağı) — saplama ayağı panel iç yüzü hizasında · kulak başına 2 dikiş')
    kam(t, R(r'^govde_kulak_'), (0, 1, 0))
    t = gel(R(r'^govde_kulak_sol_(on|arka)_\d+$'), (-0.3, 0, 0), t, 0.7, 0.08)
    t = gel(R(r'^govde_kulak_sag_(on|arka)_\d+$'), (0.3, 0, 0), t, 0.7, 0.08)
    t = gel(R(r'^govde_kulak_ust_(on|arka)_\d+$'), (0, 0.25, 0), t, 0.7, 0.08)
    t = kaynak(R(r'^govde_kulak_.*_kaynak_[ab]$'), t, 0.35, 0.03) + 0.5
    adim(5, 'İskelet · dikmeler, üst halka, kulaklar', t5, t,
         "Dikmeler kaide plakasının köşelerinde, panel dönüşlerine yer bırakmak için 3,5 / 15 mm içeride. Üst halka dört kenardan dikmeleri bağlar. Kulaklar paneli taşır: kaynak ayağı iskelete, delikli ayağı panel saplamasına.",
         '4 dikme + 4 tapa · 4 üst halka profili · 22 kulak (44 dikiş)')
    # 6 paneller
    t6 = t
    for taraf, sx, sac in (('sol', -1, 'sol_yan_sac'), ('sag', 1, 'sag_yan_sac_tabla_gecisi')):
        olay(t, '%s yan sac: preslenmiş FHP-M5 saplamalar kulak deliklerine oturur%s' % ('Sol' if sx < 0 else 'Sağ', '' if sx < 0 else ' · tabla geçiş ağzı bu sacta'))
        sap = R(r'^govde_kulak_%s_.*_bag_saplama$' % taraf)
        kam(t, [sac], (sx, 0, 0))
        t = gel([sac] + sap, (sx * 0.6, 0, 0), t, 1.4) + 0.1
        olay(t, 'Pul + fiberli somun İÇERİDEN (ön açıklıktan)')
        t = somunlar(sap, t)
    olay(t, 'Üst sac 6 kulağa — üstte görünür vida yok, somunlar alttan')
    sap = R(r'^govde_kulak_ust_.*_bag_saplama$'); kam(t, ['ust_sac'], (0, 1, 0))
    t = gel(['ust_sac'] + sap, (0, 0.55, 0), t, 1.4) + 0.1
    t = somunlar(sap, t)
    olay(t, 'Arka sac arkadan: saplamalar yan / üst sacın arka dönüş deliklerinden geçer · somunlar içeriden')
    sap = R(r'^govde_bag_arka_.*_saplama$'); kam(t, ['arka_sac'], (0, 0, -1))
    t = gel(['arka_sac'] + sap, (0, 0, -0.6), t, 1.5) + 0.1
    t = somunlar(sap, t) + 0.3
    adim(6, 'Paneller · yan → üst → arka', t6, t,
         "Yan saclar kulaklara preslenmiş FHP-M5 saplamalarla oturur, pul + fiberli somun içeriden takılır (dış yüzde iz yok). Sağ yan sacta tabla geçiş ağzı vardır (TOPPING'e). Üst sac kulaklara, arka sac en son arkadan gelir.",
         'sol yan · sağ yan (tabla geçişi) · üst · arka · M5 pul + fiberli somun')
    t = sac_tamam(t)
    t7 = t
    ac = R(r'^M__')
    olay(t, "Açıcı satın alınır (hazır ünite). Ön açıklıktan içeri alınır, kolon flanşı kaidedeki 4 PEM M8'in üstüne indirilir")
    kam(t, ac, (0, 0.3, 1))
    t = gel(ac, (0, 0.35, 0.9), t, 2.2) + 0.2
    olay(t, '4 × ISO 4762 M8 + DIN 125 pul — kolon flanşından kaide plakasındaki PEM somunlara (tork 25 N·m)')
    kam(t, R(r'^arayuz_acici'), (0, 1, 0.4), uzak=0.9)
    t = gel(R(r'^arayuz_acici'), (0, 0.12, 0), t, 0.7, 0.15) + 0.6
    adim(7, 'Açıcı (dönme kafası) montaj tabanına', t7, t,
         "A'nın tek mekanizması satın alınan hamur açıcıdır. Kolon flanşı (90 × 125 eksen, 4 × Ø9) kaide plakasındaki PEM SP-M8'lere cıvatalanır. Açıcıya bu istasyonda kablo / hava bağlanmaz (kural); X ekseni motoru TOPPING ucundadır.",
         'açıcı ünitesi (kolon + dönme kafası + koni) · 4 × M8 + DIN 125')
    # 8 kapak
    t8 = t
    KAP = sorted(a for a in P if a.startswith('onyuz_kapak_A') and not re.search(r'mentese_\d+_sabit|basac_\d+$', a))
    olay(t, '3 gizli menteşe gövdesi sol ön dikmeye (önden) + 2 × M5 vida içeriden')
    kam(t, R(r'mentese_\d_sabit'), (0, 0, 1), uzak=1.1)
    t = gel(R(r'^onyuz_kapak_A_mentese_\d_sabit$'), (0, 0, 0.15), t, 0.7, 0.15)
    t = gel(R(r'^onyuz_kapak_A_mentese_\d_sabit_vida_[ab]$'), (0.06, 0, 0), t, 0.45, 0.06)
    olay(t, '3 bas-aç mandalı sağ ön dikmeye geçme')
    t = gel(R(r'^onyuz_kapak_A_basac_\d$'), (0, 0, 0.12), t, 0.6, 0.12) + 0.2
    t = kapak_alt('onyuz_kapak_A', KAP, t, 'onyuz_kapak_A_ic_tava', r'^onyuz_kapak_A_mentese_\d_pem_[ab]$', r'^onyuz_kapak_A_karsilik_\d$',
                  r'^onyuz_kapak_A_mentese_\d_kanat$', r'^onyuz_kapak_A_mentese_\d_kanat_vida_[ab]$', r'^onyuz_kapak_A_kose_kaynagi_\d$')
    olay(t, 'Kapak bas-aç ile açılır: menteşe ekseni x 736 · z 79, 0 → 100° → kapanır')
    kam(t, ['onyuz_kapak_A'], (1, 0, 1), uzak=2.6, yon=(1.2, 0.6, 1.4))
    kapak_doner(KAP, (0.736, 0.079), -100.0, t, t + 2.0, t + 3.0, t + 5.0)
    t += 5.6
    adim(8, 'Kapak · menteşe · bas-aç', t8, t,
         "Menteşe gövdeleri sol ön dikmenin içine gömülür. Kapak tezgâhta kurulur: iç tava + karşılıklar + menteşe kanatları, üstüne dış tava (köşeler TIG). Kapak önden asılır; kulp yok, 3 bas-aç ile açılır.",
         '3 gizli menteşe · 6 × M5 · 3 bas-aç · dış tava 1,5 · iç tava 1,0 · 3 karşılık · 4 köşe kaynağı')
    # 9 saha
    t9 = t
    GHOST_T.append(round(t, 2))
    olay(t, 'Sahada: A, B dolabının üstüne oturur — 6 × M8 kaide borusunun içinden B tavanına (B silik)')
    GHOST.append([0.736, 4.4, 0.106, 0.788, -0.83, 0.039])
    GHOST.append([1.436, 2.5, 0.788, 2.2, -0.83, 0.079])
    kam(t, R(r'^arayuz_ab'), (0, 1, 0.3))
    t = gel(R(r'^arayuz_ab\d*_pul$'), (0, 0.12, 0), t, 0.5, 0.08)
    t = gel(R(r'^arayuz_ab'), (0, 0.18, 0), t, 0.6, 0.08) + 0.2
    olay(t, 'Silikon servis tapaları Ø16 deliklere bastırılır')
    t = yerinde(R(r'^kaide_servis_tapasi'), t, 0.5, 0.1) + 0.2
    olay(t, 'A → TOPPING: 4 × M8 × 16 + DIN 9021, A içinden sağ yan sactaki Ø9 deliklerden (TOPPING silik)')
    kam(t, R(r'^arayuz_m8_T'), (1, 0, 0))
    t = gel(R(r'^arayuz_m8_T.*_pul$'), (-0.08, 0, 0), t, 0.5, 0.1)
    t = gel(R(r'^arayuz_m8_T\d*(_-?\d+)*$'), (-0.1, 0, 0), t, 0.6, 0.1) + 0.2
    olay(t, 'Folyo sökülür · A tamam')
    kam(t, None); t += 2.5
    for a in R(r'^arayuz_'): GIZLI.add(a)
    adim(9, 'Saha · B ve TOPPING bağlantısı', t9, t,
         "A, B dolabının tavanına kaide borusunun içinden 6 × M8 ile bağlanır (servis delikleri silikon tapayla kapanır). TOPPING ile 4 × M8 A içinden. Tabla rayının 4 × M6 cıvatası ray TOPPING ile geldiğinde takılır (bu sayfada gösterilmez).",
         '6 × M8 × 25 + DIN 9021 (B) · 6 silikon tapa · 4 × M8 × 16 (TOPPING)')
    return t



# ------------------------------------------------------------------ ortak: sac + üstündeki saplamalar · diğer parçalar
SAPLAMA_RX = r'(_saplama|_pem_?[ab]?|_pem_M\d.*|_pem_m8.*|pem_m8_.*|_pem)$'


def sahip_ata(panel_sira):
    """her saplama/PEM → zarfı onu içeren SON panel (K: arka sacın saplamaları yan sacın dönüş deliklerinden geçer)"""
    own = {}
    adaylar = [a for a in P if P[a]['kay'] == 'sac' and (re.search(SAPLAMA_RX, a) or re.match(r'^ray_pem_[0-9_]+$', a)) and P[a]['tur'] != 'arayuz']
    for s in adaylar:
        c = cent(s)
        for pnl in panel_sira:
            lo, hi = bbox([pnl])
            if np.all(c >= lo - 0.004) and np.all(c <= hi + 0.004): own[s] = pnl
    return own


SAHIP = {}


def panel(sacs, d, t, metin, sure=1.4, somun_metin='Pul + fiberli somun içeriden', kamd=None):
    sap = sorted(s for s, p in SAHIP.items() if p in sacs and s not in GOR)
    olay(t, metin); kam(t, sacs, kamd or d)
    t = gel(list(sacs) + sap, d, t, sure, 0) + 0.1
    vs = [s for s in sap if s.endswith('_saplama')]
    if vs:
        olay(t, somun_metin); t = somunlar(vs, t)
    return t


NAD = {'E_SARJOR': 'şarjör + asansör', 'E_BESLEYICI': 'besleyici (vakum)', 'E_KALIP': 'katlama kalıbı', 'E_KOPRU': 'köprü', 'E_PISTON': 'piston',
       'E_PARMAK': 'ön parmak', 'E_KAPAK': 'kapak katlayıcı', 'E_KOSE': 'köşe katlayıcı + kaldırıcı', 'E_COP': 'robot çöpü', 'DUZ_E_OLUK': 'çöp oluğu',
       'B_SOGUTMA': 'soğutma grubu (Secop)', 'DUZ_B_SERPANTIN': 'evaporatör serpantini', 'B_DEPO': 'soğuk depo çekmecesi',
       'U_F_HAVALANDIRMA': 'havalandırma fanı + panjur', 'TOPPING_MODUL': 'açıcı', 'TOPPING_DONER': 'açıcı konisi', 'E_KUTU': 'kutu',
       'E_ELEKTRIK': 'E elektrik', 'U_F_GOVDE': 'U_F kapak elemanı'}


def sinif(a):
    p = P[a]; c = p['m']; dg = ANA_BILGI[a]['dugum']
    if c == 'urun': return 'urun'
    if ANA_BILGI[a]['kpk'] or c == 'kapak_s': return 'kapak'
    if c == 'hava': return 'hava'
    if c in ('guc', 'bilgi'): return 'kablo'
    if c == 'fis': return 'fis'
    if c == 'kanal': return 'kanal'
    if 'ELEKTRIK' in dg or dg.startswith('ELK_'): return 'elektrik'
    return 'mek'


def diger(t, no, adlar, mek_metin):
    """ana GLB gruplarını sırayla yerleştirir: mekanizmalar → elektrik kutusu + kanallar → kablolar + fiş → hava → kapaklar → ürün"""
    S = {}
    for a in adlar:
        if a in GOR or a in GIZLI: continue
        S.setdefault(sinif(a), []).append(a)
    if S.get('mek'):
        t0 = t; kam(t, S['mek'], (0, 0.2, 1))
        grp = {}
        for a in S['mek']: grp.setdefault(ANA_BILGI[a]['dugum'].split('__')[0], []).append(a)
        sira = sorted(grp, key=lambda k: (round(bbox(grp[k])[0][1], 1), bbox(grp[k])[0][0]))
        for k in sira:
            olay(t, '%s — ön açıklıktan içeri, PEM saplamalara pul + fiberli somunla' % NAD.get(k, k.replace('_', ' ').lower()))
            kam(t, grp[k], (0, 0.2, 1))
            t = gel(sorted(grp[k]), (0, 0.15, 0.85), t, 1.3) + 0.25
        adim(no, 'Mekanizmalar', t0, t + 0.3, mek_metin, ' · '.join(NAD.get(k, k) for k in sira)); t += 0.3; no += 1
    el = S.get('elektrik', []) + S.get('kanal', [])
    if el:
        t0 = t
        if S.get('elektrik'):
            olay(t, 'Elektrik kutusu / pano, DIN ray cihazları ve sensör braketleri yerine (PEM saplamalara)')
            kam(t, S['elektrik'], (0, 0.2, 1))
            t = gel(sorted(S['elektrik']), (0, 0.1, 0.7), t, 1.3, min(0.15, 3.0 / max(1, len(S['elektrik'])))) + 0.3
        if S.get('kanal'):
            olay(t, 'İç kablo kanalları duvar / tavan boyunca (PEM saplamalı kanal ayakları)')
            kam(t, S['kanal'], (0, 0.2, 1))
            t = gel(sorted(S['kanal']), (0, 0, 0.5), t, 1.2, 0.15) + 0.3
        adim(no, 'Elektrik kutusu + iç kanallar', t0, t + 0.3, "Elektrik kutusu (sürücüler, G/Ç, sigorta) istasyonun kendi gövdesinde, PEM saplamalara oturur. Kablolar yalnız kanal içinden yürür; kanal kapakları kablolar çekildikten sonra kapanır.",
             'elektrik kutusu · DIN ray cihazları · sensör braketleri · iç kanallar'); t += 0.3; no += 1
    kb = S.get('kablo', []) + S.get('fis', [])
    if kb:
        t0 = t
        guc = [a for a in S.get('kablo', []) if P[a]['m'] == 'guc']; bil = [a for a in S.get('kablo', []) if P[a]['m'] == 'bilgi']
        if S.get('fis'):
            olay(t, 'Gömme fiş paneli: Harting / M12 soketler + kablo rakorları (dışarıdan, contalı)')
            kam(t, S['fis'], (0, 0.1, 1))
            t = gel(sorted(S['fis']), (0, 0, 0.35), t, 1.0, 0.1) + 0.3
        if guc:
            olay(t, 'Güç kabloları (KIRMIZI) — fiş panelinden kutuya, kutudan motorlara, kanal içinden')
            kam(t, guc, (0, 0.2, 1)); t = gel(sorted(guc), (0, 0, 0.45), t, 1.4, 0.12) + 0.3
        if bil:
            olay(t, 'Bilgi kabloları (MAVİ) — sensör, enkoder, EtherCAT / G/Ç, ayrı kanal bölmesinden')
            kam(t, bil, (0, 0.2, 1)); t = gel(sorted(bil), (0, 0, 0.45), t, 1.4, 0.12) + 0.3
        adim(no, 'Kablolar + fiş paneli', t0, t + 0.3, "İstasyona dışarıdan yalnız gömme fiş panelinden girilir (Harting güç, M12 bilgi). İçeride güç (kırmızı) ve bilgi (mavi) kabloları ayrı kanal bölmelerinden yürür; uçlar yüksük + etiketle klemense.",
             'fiş paneli · güç kabloları (kırmızı) · bilgi kabloları (mavi)'); t += 0.3; no += 1
    if S.get('hava'):
        t0 = t; olay(t, 'Hava hortumları (YEŞİL) — valf adasından silindir / vakuma, kanal ve kelepçelerle')
        kam(t, S['hava'], (0, 0.2, 1)); t = gel(sorted(S['hava']), (0, 0, 0.45), t, 1.4, 0.12) + 0.6
        adim(no, 'Hava hattı', t0, t, "Basınçlı hava gömme rakordan girer, şartlandırıcı + valf adasından hortumlarla tüketicilere gider. Hortumlar kablo kanalının hava bölmesinden ve kelepçelerle.",
             'rakor · valf adası · hava hortumları (yeşil)'); no += 1
    if S.get('kapak'):
        t0 = t; olay(t, 'Kapak elemanları önden takılır (menteşe, bas-aç, fitil)')
        kam(t, S['kapak'], (0, 0.1, 1)); t = gel(sorted(S['kapak']), (0, 0, 0.5), t, 1.3, 0.12) + 0.6
        adim(no, 'Kapak elemanları', t0, t, "Kapak elemanları en son, iç montaj ve kablolama bittikten sonra takılır: menteşe yarıları, bas-aç mandalları ve fitiller.", 'menteşe · bas-aç · fitil'); no += 1
    if S.get('urun'):
        t0 = t; olay(t, 'Ürün / sarf yüklenir (görsel)')
        kam(t, S['urun'], (0, 1, 0.6)); t = gel(sorted(S['urun']), (0, 0.35, 0.2), t, 1.2, min(0.1, 3.0 / len(S['urun']))) + 0.6
        adim(no, 'Ürün', t0, t, "En son ürün ve sarf malzemesi yüklenir — devreye alma testi için.", 'ürün (görsel)'); no += 1
    return t, no


def seq_B():
    global SAHIP
    BASLIK.update(kod='B')
    SECIM[:] = [('dis_sol_yan', 1), ('dis_taban_1', 1), ('dis_arka_1', 1), ('dis_tavan_2', 1), ('ic_sol_duvar', 1), ('ic_taban_1', 1), ('bolme_1_sac_a', 1),
                ('isi_kalkani_u', 1), ('on_cerceve_1', 1), ('kosebent_sol_alt_2', 1)]
    t = kartlar(0.0, 'dış kabuk 2 parçalı + ek lamaları · iç kabuk · 9 bölme sacı · 14 kovan · ısı kalkanı · ön çerçeve 2 parça · 126 ray PEM SP-M5')
    PANEL = ['dis_taban_1', 'dis_taban_2', 'dis_sol_yan', 'dis_sag_yan', 'dis_arka_1', 'dis_arka_2', 'ic_taban_1', 'ic_taban_2', 'ic_sol_duvar', 'teknik_sol_duvar',
             'ic_arka_1', 'ic_arka_2'] + R(r'^bolme_\d_sac_[ab]$') + ['ic_tavan_1', 'ic_tavan_2', 'dis_tavan_1', 'dis_tavan_2']
    SAHIP = sahip_ata(PANEL)
    t4 = t; kam(t, None)
    olay(t, '14 ayarlı ayak zemine, terazide')
    t = gel(R(r'^M__B_KASA__celik'), (0, 0.25, 0), t, 1.0) + 0.1
    olay(t, "Alt şase + PU'ya gömülecek dikme / kirişler (B_MODULER) + GFRP pedler — ayakların üstüne")
    t = gel(R(r'^M__B_MODULER__'), (0, 0.5, 0), t, 1.5, 0.2) + 0.1
    olay(t, "Taşıyıcı (K'nın oturduğu çapraz kirişler)")
    t = gel(R(r'^M__B_TASIYICI__'), (0, 0.4, 0), t, 1.1) + 0.5
    adim(4, 'Ayaklar · alt şase · gömülü iskelet', t4, t,
         "B dolabı kendi şasesi üstünde kurulur: ayaklar, alt şase boyunaları, PU'ya gömülecek dikme ve kirişler (A ve K bunların üstüne oturur) ve aradaki GFRP ısı köprüsü pedleri. Sac kabuk bu iskeletin çevresine kapanır.",
         '14 ayak · alt şase + dikmeler (B_MODULER) · GFRP ped · taşıyıcı kirişler')
    t5 = t
    t = panel(['dis_taban_1', 'dis_taban_2'], (0, 0.4, 0), t, 'Dış taban 2 parça (ek x 2091) dikmelerin geçişlerinden iner')
    t = gel(['dis_taban_ek_lamasi'], (0, 0.15, 0), t, 0.7) + 0.1
    olay(t, '10 × M8 × 20 + DIN 9021 içeriden şaseye (köpüklemeden ÖNCE)')
    kam(t, R(r'^arayuz_sase'), (0, 1, 0.3))
    t = gel(R(r'^arayuz_sase.*_pul$'), (0, 0.12, 0), t, 0.45, 0.05)
    t = gel(R(r'^arayuz_sase'), (0, 0.18, 0), t, 0.5, 0.05) + 0.2
    olay(t, 'Alt köşebentler (yan sacı tabana bağlar)')
    t = gel(R(r'^kosebent_s(ol|ag)_alt'), (0, 0.2, 0), t, 0.7, 0.06) + 0.1
    t = panel(['dis_sol_yan'], (-0.6, 0, 0), t, 'Sol dış yan sac (yalnız arka dönüş) — köşebentlere')
    t = panel(['dis_sag_yan'], (0.6, 0, 0), t, 'Sağ dış yan sac — E kabuğuna yüz yüze, dış yüz düz')
    t = panel(['dis_arka_1', 'dis_arka_2'], (0, 0, -0.6), t, 'Dış arka 2 parça arkadan + ek laması')
    t = gel(['dis_arka_ek_lamasi'], (0, 0, -0.15), t, 0.7) + 0.1
    olay(t, 'Ek yerleri ve arka köşeler gıda silikonuyla kapatılır (köpük sızmasın)')
    t = yerinde(R(r'^ek_yeri_silikon_(taban|arka)$') + R(r'^arka_kose_silikonu'), t, 0.5, 0.15) + 0.4
    adim(5, 'Dış kabuk · taban → yanlar → arka', t5, t,
         "Dış kabuk iki parçalıdır (levha boyu 3000 sınırı): taban ve arka x 2091'de ek lamasıyla birleşir. Yan saclar tava değil, yalnız arka dönüşlü; tabana köşebentle bağlanır. Şase cıvataları köpüklemeden önce içeriden takılır.",
         'dış taban 2 + ek laması · 10 × M8 şase cıvatası · 8 alt köşebent · 2 yan · dış arka 2 + ek laması · silikon')
    t6 = t
    t = panel(['ic_taban_1', 'ic_taban_2'], (0, 0, 0.9), t, 'İç taban 2 parça önden — dikme geçişleri 31 × 31')
    t = panel(['ic_sol_duvar', 'teknik_sol_duvar'], (0, 0, 0.9), t, "İç sol duvar + teknik bölme duvarı — ray PEM'leri düz sacta basılı geldi")
    t = panel(['ic_arka_1', 'ic_arka_2'], (0, 0, 0.9), t, 'İç arka 2 parça · iç köşeler TIG + taşlama')
    olay(t, "Bölme sacları (çift cidar a/b) önden — her yüzde 3 ray PEM'i SP-M5")
    kam(t, R(r'^bolme_\d_sac'), (0, 0.3, 1))
    for b in sorted(set(re.sub(r'_sac_[ab]$', '', a) for a in R(r'^bolme_\d_sac_[ab]$'))):
        sacs = R(r'^%s_sac_[ab]$' % b)
        sap = sorted(s for s, p in SAHIP.items() if p in sacs and s not in GOR)
        t = gel(sacs + sap, (0, 0, 0.9), t, 1.0, 0) + 0.15
    olay(t, 'Kablo / gider kovanları (U, L) bölmelere · köpüğe açılan köşe ağızları TIG')
    t = gel(R(r'^bolme_\d_kovan_\d+(_ust_L)?$'), (0, 0.15, 0), t, 0.7, 0.05)
    t = kaynak(R(r'kovan_\d+_kose_kaynagi'), t) + 0.2
    t = panel(['ic_tavan_1', 'ic_tavan_2'], (0, 0, 0.9), t, 'İç tavan 2 parça önden')
    olay(t, 'Isı kalkanı (fırın altı): U sac + ışınım sacı + 12 PTFE / cam elyaf takoz')
    kam(t, R(r'^isi_kalkani'), (0, 0.4, 1))
    t = gel(R(r'^isi_kalkani_takozu'), (0, 0.15, 0), t, 0.5, 0.04)
    t = gel(R(r'^isi_kalkani_(u|isinim)'), (0, 0, 0.9), t, 1.2, 0.2) + 0.1
    t = gel(R(r'^tk_ara_arka_sac'), (0, 0, 0.6), t, 0.9) + 0.4
    adim(6, 'İç kabuk · bölmeler · kovanlar · ısı kalkanı', t6, t,
         "İç kabuk ve bölme ön kenarları ön çerçeveye ALIN gelir. Çekmece raylarının 126 PEM SP-M5'i duvar ve bölme saclarına düz hâlde basılmıştır. Bölmelerde kanal ve gider için 1 mm boşluklu U / L kovanlar; köpüğe açılan köşe ağızları kaynakla kapanır. Fırın altına ısı kalkanı.",
         'iç taban 2 · iç sol duvar · teknik duvar · iç arka 2 · 9 bölme sacı · 14 kovan · iç tavan 2 · ısı kalkanı + 12 takoz')
    t7 = t
    olay(t, 'Üst köşebentler')
    t = gel(R(r'^kosebent_s(ol|ag)_ust'), (0, 0.2, 0), t, 0.7, 0.06) + 0.1
    t = panel(['dis_tavan_1', 'dis_tavan_2'], (0, 0.5, 0), t, 'Dış tavan 2 parça üstten (A ve K bağlantı delikleri Ø9 hazır)')
    t = gel(R(r'^dis_tavan_ek_lamasi'), (0, 0.15, 0), t, 0.6, 0.08) + 0.1
    olay(t, 'Köpüklemeden önce: PEM gövdelerine PE köpük kapağı, ek yeri + gider silikonları')
    kam(t, None)
    t = yerinde(R(r'_kopuk_kapagi$'), t, 0.4, 0.01)
    t = yerinde(R(r'^ek_yeri_silikon_tavan$') + R(r'gider_silikonu'), t, 0.4, 0.08) + 0.3
    olay(t, 'PU köpükleme (SARI): kalıpta, iç / dış kabuk arası 40 kg/m³ — 24 saat kür')
    pu = [a for a in P if P[a]['tur'] == 'pu' and a not in GOR]
    t = yerinde(sorted(pu), t, 1.6, 0.12) + 0.6
    adim(7, 'Tavan · köpük hazırlığı · PU köpükleme', t7, t,
         "Tavan kapanınca gövde köpükleme kalıbına girer. Önce bütün PEM gövdelerine PE köpük kapağı, ek yerlerine ve gider halkalarına silikon; sonra iç ve dış kabuk arası PU ile doldurulur (sahnede sarı; normalde görünmez).",
         '7 üst köşebent · dış tavan 2 + 3 ek laması · 126 köpük kapağı · silikonlar · 19 PU bloğu')
    t8 = t
    olay(t, 'Ön çerçeve 2 parça (430) önden — ek x 2091 · 35 mm ek laması arkasında')
    kam(t, R(r'^on_cerceve'), (0, 0.2, 1))
    t = gel(['on_cerceve_ek_lamasi'], (0, 0, 0.5), t, 0.8) + 0.1
    t = gel(R(r'^on_cerceve_\d$'), (0, 0, 0.7), t, 1.3, 0.3) + 0.5
    adim(8, 'Ön çerçeve', t8, t, "Kalıptan çıkan gövdeye ön çerçeve takılır; iç kabuk ve bölmeler çerçeveye alın gelir (açık oluk / görünür PU yok).",
         'ön çerçeve 2 parça + ek laması')
    t = sac_tamam(t)
    rest = R(r'^M__')
    raylar = [a for a in rest if re.match(r'^M__CEK_.*__celik__\d+$', a)]
    cek_govde = [a for a in rest if a.startswith('M__CEK_') and a not in raylar and P[a]['m'] not in ('urun', 'kapak_s') and not ANA_BILGI[a]['kpk']]
    cek_on = [a for a in rest if a.startswith('M__CEK_') and (P[a]['m'] == 'kapak_s' or ANA_BILGI[a]['kpk'])]
    no = 9
    t, no = diger(t, no, [a for a in rest if not a.startswith('M__CEK_') and sinif(a) == 'mek'],
                  "Soğutma grubu teknik bölmeye, evaporatör ve soğuk depo yerine; hepsi gövdedeki PEM saplamalara pul + fiberli somunla.")
    t, no = diger(t, no, [a for a in rest if not a.startswith('M__CEK_') and sinif(a) in ('elektrik', 'kanal', 'kablo', 'fis', 'hava')], '')
    t0 = t
    olay(t, '42 sabit çekmece rayı önden duvar / bölme yüzlerine')
    kam(t, raylar, (0, 0.3, 1))
    t = gel(sorted(raylar), (0, 0, 0.8), t, 1.0, 0.04) + 0.2
    olay(t, "Her ray 3 × DIN 7991 M5 × 10 havşa başlı — duvardaki PEM SP-M5'lere")
    t = gel(R(r'^arayuz_ray'), (0, 0, 0.12), t, 0.4, 0.008) + 0.4
    adim(no, 'Çekmece rayları', t0, t, "Sabit raylar duvar ve bölme saclarındaki PEM SP-M5'lere havşa başlı vidayla bağlanır (sacın arkası köpüklü olduğu için somun yok — PEM şart).",
         '42 sabit ray · 126 × M5 × 10 havşa başlı'); no += 1
    t0 = t
    olay(t, 'Çekmeceler (tahrik + kızak + kasa) önden raylara sürülür')
    kam(t, cek_govde, (0, 0.3, 1))
    grp = {}
    for a in cek_govde: grp.setdefault(ANA_BILGI[a]['dugum'].split('__')[0], []).append(a)
    for k in sorted(grp, key=lambda k: (bbox(grp[k])[0][0], bbox(grp[k])[0][1])):
        t = gel(sorted(grp[k]), (0, 0, 0.9), t, 0.9) + 0.1
    if cek_on:
        olay(t + 0.3, 'Çekmece ön kapakları + fitiller')
        t = gel(sorted(cek_on), (0, 0, 0.4), t + 0.3, 0.8, 0.05) + 0.4
    adim(no, 'Çekmeceler + ön kapaklar', t0, t, "Her çekmece kendi tahrik motoru ve kızağıyla hazır gelir, önden raya sürülür; ön kapak ve fitil en son.",
         '%d çekmece · ön kapaklar · fitiller' % len(grp)); no += 1
    t, no = diger(t, no, R(r'^M__'), '')
    olay(t, 'B tamam'); kam(t, None); t += 2.0
    for a in R(r'^arayuz_'): GIZLI.add(a)
    return t


def seq_E():
    global SAHIP
    BASLIK.update(kod='E')
    SECIM[:] = [('sol_sac_pizza_penceresi', 1), ('sag_sac', 1), ('arka_sac', 1), ('ust_sac', 1), ('taban_sac_3', 1), ('onyuz_kapak_E_ust_sol', 1),
                ('onyuz_kapak_E_alt_sag_ic_tava', 1), ('sarjor_yan_kapisi', 1), ('govde_kulak_sol_on_1100', 18)]
    t = kartlar(0.0, 'taban 3 mm · ön kasa 3 dikme + 2 kayıt · yan / arka / üst sac · 4 kapak dış + iç tava · şarjör yan kapısı · kulaklar')
    PANEL = ['taban_sac_3', 'sol_sac_pizza_penceresi', 'sag_sac', 'arka_sac', 'ust_sac']
    SAHIP = sahip_ata(PANEL)
    t4 = t; kam(t, None)
    olay(t, '6 ayarlı ayak (GN 20 sınıfı M12) + kontra somun')
    t = gel(R(r'^ayak_\d+(_kontra)?$'), (0, 0.2, 0), t, 0.8, 0.06) + 0.1
    olay(t, 'Kaide rayları (60 × 60) + kayıtlar (40 × 60) fikstürde · uç tapaları · TIG')
    t = gel(R(r'^kaide_e_ray_(on|arka)$'), (0, 0.4, 0), t, 1.0, 0.2)
    t = gel(R(r'^kaide_e_kayit_(sol|orta|sag)$'), (0, 0.4, 0), t, 1.0, 0.15)
    t = kaynak(R(r'^kaide_e_kayit_.*kaynak'), t)
    t = gel(R(r'^kaide_e_ray_.*_tapa'), (0, 0, 0.1), t, 0.5, 0.08)
    t = gel(R(r'^kaide_e_ayak_somunu'), (0, -0.1, 0), t, 0.5, 0.05) + 0.4
    adim(4, 'Ayaklar · kaynaklı kaide', t4, t, "Kaide 60 × 60 × 3 raylar ve 40 × 60 × 3 kayıtlardan kaynaklı çerçevedir; uçlar tapalı. Ayaklar kaide rayının altındaki somunlara vidalanır, terazide ayarlanır.",
         '6 ayak + kontra · 2 ray + 4 tapa · 3 kayıt · ayak somunları')
    t5 = t
    t = panel(['taban_sac_3'], (0, 0.4, 0), t, 'Taban sacı 3 mm kaideye')
    olay(t, 'Taban → kaide: M8 vida + somun')
    t = gel(R(r'^kaide_e_vida_'), (0, 0.15, 0), t, 0.5, 0.06)
    t = gel(R(r'^kaide_e_somun_'), (0, -0.12, 0), t, 0.5, 0.06) + 0.1
    olay(t, 'Ön kasa: 3 dikme (sol, orta, sağ) tabana · köşe dikişleri · tepe tapaları')
    kam(t, R(r'^onyuz_dikme_'), (0, 0.2, 1))
    t = gel(R(r'^onyuz_dikme_(sol|sag|orta)$'), (0, 0.6, 0), t, 1.0, 0.2)
    t = kaynak(R(r'^onyuz_dikme_.*taban_kaynagi'), t)
    t = gel(R(r'^onyuz_dikme_.*_tapa$'), (0, 0.15, 0), t, 0.5, 0.08)
    olay(t, 'Ön kayıtlar (y 788) dikmeler arasına')
    t = gel(R(r'^onyuz_kayit_788_(sol|sag)$'), (0, 0, 0.3), t, 0.8, 0.15)
    t = kaynak(R(r'^onyuz_kayit.*kaynak'), t) + 0.1
    olay(t, 'Panel kulakları: dikme arkasına (yan) ve tabana · kulak başına 2 dikiş')
    kam(t, R(r'^govde_kulak_'), (0, 0.3, 1))
    t = gel(R(r'^govde_kulak_sol_(on|taban)_\d+$'), (-0.25, 0, 0), t, 0.6, 0.05)
    t = gel(R(r'^govde_kulak_sag_(on|taban)_\d+$'), (0.25, 0, 0), t, 0.6, 0.05)
    t = gel(R(r'^govde_kulak_ust_(sol|orta|sag)$'), (0, 0.25, 0), t, 0.6, 0.08)
    t = kaynak(R(r'^govde_kulak_.*_kaynak_[ab]$'), t, 0.3, 0.03)
    t = gel(R(r'^govde_kosebent_[a-z_]+$'), (0.2, 0, 0), t, 0.6) + 0.4
    adim(5, 'Taban · ön kasa · kulaklar', t5, t, "Taban 3 mm sac kaideye cıvatalanır. Ön kasanın 3 dikmesi tabana kaynaklanır; y 788'de kayıtlar alt ve üst kapakları ayırır. Kulaklar yan ve üst sacı taşır.",
         'taban 3 mm · 7 M8 vida + somun · 3 dikme + tapa · 2 kayıt · 39 kulak · köşebent')
    t6 = t
    t = panel(['sol_sac_pizza_penceresi'], (-0.6, 0, 0), t, "Sol yan sac (pizza penceresi, K'dan gelen ürün için) — FHP saplamalar kulaklara")
    t = panel(['sag_sac'], (0.6, 0, 0), t, 'Sağ yan sac (şarjör kapısı açıklığı) — saplamalar kulaklara')
    t = panel(['arka_sac'], (0, 0, -0.6), t, 'Arka sac arkadan: taban üstünden başlar, alt iç dönüş tabana')
    t = panel(['ust_sac'], (0, 0.55, 0), t, 'Üst sac yan sacların ARASINA oturur (21,5 aşağı dönüş) · U_KE için 3 × PEM SP-M8')
    olay(t, 'Şarjör kapısı taşıyıcı lamaları (arka sacta menteşe, yan sacta bas-aç)')
    kam(t, R(r'^sarjor_yan_kapisi_(mentese|basac)_lamasi'), (1, 0, 0))
    t = gel(R(r'^sarjor_yan_kapisi_(mentese|basac)_lamasi$'), (0.2, 0, 0), t, 0.7, 0.1)
    vs = R(r'^govde_bag_kapi_.*_saplama$')
    t = gel(vs, (0.15, 0, 0), t, 0.5, 0.05)
    t = somunlar(vs, t)
    kal = R(r'_saplama$')
    if kal:
        olay(t, 'Kalan köşe bağlantıları (köşebent) · pul + somun')
        t = gel(kal, (0, 0, 0.1), t, 0.5, 0.05); t = somunlar(kal, t)
    t = yerinde(R(r'^govde_pem_m8_ust'), t, 0.4, 0.05) + 0.3
    adim(6, 'Paneller · yan → arka → üst', t6, t, "Yan saclar kulaklara preslenmiş FHP-M5 saplamalarla oturur, pul + fiberli somun içeriden (dışta iz yok). Arka sac arkadan, üst sac yan sacların arasına. Şarjör yan kapısının lamaları arka ve yan saca bağlanır.",
         'sol yan (pizza penceresi) · sağ yan · arka · üst · şarjör kapısı lamaları · M5 pul + fiberli somun')
    t = sac_tamam(t)
    no = 7
    rest = R(r'^M__')
    t, no = diger(t, no, [a for a in rest if sinif(a) in ('mek', 'elektrik', 'kanal', 'kablo', 'fis', 'hava')],
                  "Mekanizmalar alttan yukarı sırayla ön açıklıktan girer (kapaklar daha takılmadı): her biri gövdedeki PEM saplamalara (ARAYÜZ listesi) pul + fiberli somunla bağlanır.")
    t0 = t
    olay(t, '12 gizli menteşe gövdesi dikmelere + 2 × M5 · 6 bas-aç orta dikmeye')
    kam(t, R(r'^onyuz_kapak_E_mentese_.*_sabit$'), (0, 0, 1))
    t = gel(R(r'^onyuz_kapak_E_mentese_(sol|sag)_\d+_sabit$'), (0, 0, 0.15), t, 0.6, 0.06)
    t = gel(R(r'^onyuz_kapak_E_mentese_(sol|sag)_\d+_sabit_vida_[ab]$'), (0, 0, 0.06), t, 0.4, 0.02)
    t = gel(R(r'^onyuz_kapak_E_basac_'), (0, 0, 0.12), t, 0.5, 0.06) + 0.2
    for kap_ad, taraf in [('onyuz_kapak_E_alt_sol', 'sol'), ('onyuz_kapak_E_alt_sag', 'sag'), ('onyuz_kapak_E_ust_sol', 'sol'), ('onyuz_kapak_E_ust_sag', 'sag')]:
        mn = '[012]' if '_alt_' in kap_ad else '[345]'
        rx_kanat = r'^onyuz_kapak_E_mentese_%s_%s_kanat$' % (taraf, mn)
        KAP = sorted(set([a for a in P if a.startswith(kap_ad) and a not in GOR] + R(rx_kanat)))
        t = kapak_alt(kap_ad, KAP, t, kap_ad + '_ic_tava', r'^%s_robot_agzi_kasa_\w+$' % kap_ad, r'^%s_karsilik_\d$' % kap_ad,
                      rx_kanat, r'^$', r'^%s_kose_kaynagi_\d$' % kap_ad, etiket='%s ' % kap_ad.replace('onyuz_kapak_E_', '').replace('_', ' '))
        piv = (4.402, 0.079) if taraf == 'sol' else (5.23, 0.079)
        KAPAK_PIV[kap_ad] = (KAP, piv, -100.0 if taraf == 'sol' else 100.0)
    olay(t, 'Kapaklar bas-aç ile açılır / kapanır — sol kanatlar x 4402, sağ kanatlar x 5230 ekseninde')
    kam(t, None, yon=(0.4, 0.5, 1.2))
    for kad, (KAP, piv, aci) in KAPAK_PIV.items(): kapak_doner(KAP, piv, aci, t, t + 2.0, t + 3.0, t + 5.0)
    t += 5.5
    olay(t, 'Şarjör yan kapısı: iç tava + dış tava, menteşeler arka sactaki lamaya, bas-aç yan sactaki lamaya')
    kam(t, ['sarjor_yan_kapisi'], (1, 0, 0))
    t = gel(R(r'^sarjor_yan_kapisi_mentese_?\d*$'), (0.12, 0, 0), t, 0.6, 0.1)
    t = gel(R(r'^sarjor_yan_kapisi'), (0.5, 0, 0), t, 1.2) + 0.5
    adim(no, 'Kapaklar · menteşe · bas-aç', t0, t, "4 ön kapak (2 × 2) tezgâhta kurulur: iç tava + karşılıklar + menteşe kanatları, üstüne dış tava (köşeler TIG); üst sol kapakta robot ağzı kasası. Kapaklar önden asılır, kulp yok, bas-aç ile açılır. Şarjör yan kapısı sağdan.",
         '12 gizli menteşe · 6 bas-aç · 4 kapak (dış + iç tava) · robot ağzı kasası · şarjör yan kapısı'); no += 1
    t, no = diger(t, no, R(r'^M__'), '')
    olay(t, 'E tamam'); kam(t, None); t += 2.0
    return t


def seq_U():
    global SAHIP
    BASLIK.update(kod='U')
    SECIM[:] = [('ust_f_taban_sac', 1), ('ust_f_yan_sol', 1), ('ust_f_arka_sac', 1), ('ust_f_tavan_sac', 1), ('ust_ke_tavan_sac', 1), ('f_ust_yan_sag', 1),
                ('f_ust_taban_levhasi', 1), ('f_ust_tavan_sac', 1), ('f_davlumbaz_bolme_duvari', 1), ('ust_f_giris_cebi', 1)]
    t = kartlar(0.0, 'F üst kabin 10 sac + 6 profil · U_F 6 sac · U_KE 5 sac · omega profiller · panjur lamelleri')
    PANEL = ['f_ust_taban_levhasi', 'f_ust_yan_sol', 'f_ust_yan_sag', 'f_ust_arka_sac', 'f_davlumbaz_bolme_duvari', 'f_ust_tavan_sac',
             'ust_f_taban_sac', 'ust_f_yan_sol', 'ust_f_yan_sag', 'ust_f_arka_sac', 'ust_f_tavan_sac', 'ust_f_giris_cebi',
             'ust_ke_taban_sac', 'ust_ke_yan_sol', 'ust_ke_yan_sag', 'ust_ke_arka_sac', 'ust_ke_tavan_sac']
    SAHIP = sahip_ata(PANEL)
    t4 = t; kam(t, R(r'^f_ust_|^onyuz_f_ust'), (0, 1, 0))
    olay(t, 'F üst kabini: 3 alt profil (ön, orta, arka) fikstürde · yan kaynaklar')
    t = gel(R(r'^f_ust_alt_profil_(on|orta|arka)$'), (0, 0.4, 0), t, 1.0, 0.2)
    t = kaynak(R(r'^f_ust_alt_profil_.*kaynagi'), t) + 0.1
    t = panel(['f_ust_taban_levhasi'], (0, 0.45, 0), t, 'Taban levhası profillerin üstüne · 15 delik kaynağı')
    t = kaynak(R(r'^f_ust_taban_levhasi_delik_kaynagi'), t, 0.35, 0.05)
    olay(t, 'Rakor + kablo kovanları tabandan; taş yünü yalıtım kılıf tavasına, kılıf perçinle tabana')
    t = gel(R(r'^f_ust_taban_(rakor|v2)_kovani$'), (0, -0.2, 0), t, 0.7, 0.15)
    t = yerinde(R(r'^f_ust_taban_yalitimi_'), t, 0.8, 0.2)
    t = gel(R(r'^f_ust_taban_yalitim_kilifi_'), (0, -0.3, 0), t, 1.0, 0.2)
    t = yerinde(R(r'^f_ust_kilif_percin_'), t, 0.3, 0.02) + 0.1
    olay(t, 'Ön üst kayıt + orta dikme + tavan kirişi (tapalı) · kaynaklar')
    t = gel(R(r'^onyuz_f_ust_ust_kayit$') + R(r'^onyuz_f_ust_dikme_\d$'), (0, 0, 0.35), t, 0.9, 0.2)
    t = gel(R(r'^f_ust_tavan_kirisi$'), (0, 0.3, 0), t, 0.8)
    t = gel(R(r'^f_ust_tavan_kirisi_tapa$'), (0, 0, -0.1), t, 0.5)
    t = kaynak(R(r'^onyuz_f_ust_.*kaynagi|^f_ust_tavan_kirisi_kaynagi'), t) + 0.4
    adim(4, 'F üst kabini · profiller · taban · yalıtım', t4, t, "F'nin üst kabini fırının üstündedir: 3 alt profil taban levhasını taşır, levhanın altı taş yünüyle yalıtılır (kılıf tavası perçinli). Önde üst kayıt ve orta dikme, üstte tavan kirişi.",
         '3 alt profil · taban levhası + 15 delik kaynağı · 2 kovan · taş yünü + kılıf · ön kayıt + dikme · tavan kirişi')
    t5 = t
    t = panel(['f_ust_yan_sol'], (-0.6, 0, 0), t, 'Sol yan sac (y 788–1862, fırın bölgesi dahil) — J1 ağzı')
    t = panel(['f_ust_yan_sag'], (0.6, 0, 0), t, "Sağ yan sac — K'dan gelen tartı / yağ hortumu geçişleri")
    t = panel(['f_ust_arka_sac'], (0, 0, -0.6), t, 'Arka sac arkadan · köşebent')
    t = gel(R(r'^govde_fu_kosebent_[a-z_]+$'), (0, 0, -0.2), t, 0.6) + 0.1
    t = panel(['f_davlumbaz_bolme_duvari'], (0, 0.45, 0), t, 'Davlumbaz bölme duvarı (atış kanalı ile ayrılır)')
    olay(t, 'Panjur lamelleri (2 × 8) havalandırma ağzına · lamel başına 2 dikiş')
    kam(t, R(r'^f_ust_panjur_lameli_\d_\d$'), (0, 0.3, -1))
    t = gel(R(r'^f_ust_panjur_lameli_\d_\d$'), (0, 0, -0.2), t, 0.5, 0.04)
    t = kaynak(R(r'^f_ust_panjur_lameli_.*_kaynak'), t, 0.3, 0.02)
    t = panel(['f_ust_tavan_sac'], (0, 0.5, 0), t, 'Tavan sacı üstten')
    kal = R(r'^govde_fu_.*_saplama$')
    if kal:
        olay(t, 'Kalan bağlantılar · pul + somun'); t = gel(kal, (0, 0, 0.1), t, 0.5, 0.03); t = somunlar(kal, t)
    t = yerinde(R(r'^govde_fu_pem'), t, 0.4, 0.05) + 0.3
    adim(5, 'F üst kabini · yanlar · arka · bölme · panjur · tavan', t5, t, "Yan saclar yalnız arka dönüşlü (J1/J2 kanalı için kısaltıldı); FHP saplamalı bağlantılar içeriden pul + fiberli somunla. Davlumbaz bölme duvarı, panjur lamelleri ve tavan sacı.",
         'sol / sağ yan · arka + köşebent · davlumbaz bölme duvarı · 16 panjur lameli · tavan')
    t6 = t
    GHOST_T.append(round(t, 2))
    GHOST.extend([[2.5, 4.4, 0.106, 0.788, -0.83, 0.039], [4.0, 4.4, 0.788, 1.862, -0.83, 0.079], [4.4, 5.23, 0.0, 1.862, -0.83, 0.079]])
    olay(t, 'U_F ve U_KE sahada F üst kabini, K ve E üstüne kurulur (B, K, E silik)')
    for b, ad in (('f', 'U_F (F üstü, ana pano bölmesi)'), ('ke', 'U_KE (K + E üstü)')):
        t = panel(['ust_%s_taban_sac' % b], (0, 0.45, 0), t, '%s: taban sacı' % ad)
        t = panel(['ust_%s_yan_sol' % b], (-0.5, 0, 0), t, 'Sol yan sac')
        t = panel(['ust_%s_yan_sag' % b], (0.5, 0, 0), t, 'Sağ yan sac · taban yan kaynakları')
        t = kaynak(R(r'^ust_%s_taban_yan_kaynagi' % b), t, 0.3, 0.04)
        t = panel(['ust_%s_arka_sac' % b], (0, 0, -0.5), t, 'Arka sac arkadan')
        if b == 'f': t = panel(['ust_f_giris_cebi'], (0, 0, -0.3), t, 'Gömme bina giriş cebi (rakorlar cebin içinde)')
        olay(t, 'Omega profil (hazır haddeli) tavanın altına · punta')
        t = gel(R(r'^ust_%s_tavan_omegasi' % b), (0, 0.3, 0), t, 0.7)
        t = panel(['ust_%s_tavan_sac' % b], (0, 0.45, 0), t, 'Tavan yan sacların ARASINA, dört kenar dönüşlü')
        kal = R(r'^govde_%s_.*_saplama$' % b)
        if kal:
            olay(t, 'Kalan bağlantılar · pul + somun'); t = gel(kal, (0, 0, 0.1), t, 0.5, 0.03); t = somunlar(kal, t)
    olay(t, "U_F ↔ U_KE: 3 × M8 vida + 2 pul + somun · U_F → fırın PEM'leri")
    kam(t, R(r'^govde_f_ke_m8'), (0, 1, 0.4))
    t = gel(R(r'^govde_f_ke_m8.*_vida$'), (-0.12, 0, 0), t, 0.5, 0.1)
    t = gel(R(r'^govde_f_ke_m8.*_(pul\d|somun)$'), (0.12, 0, 0), t, 0.5, 0.05)
    t = yerinde(R(r'^govde_f_m8_firin|^govde_ke_m8_e'), t, 0.4, 0.06) + 0.4
    adim(6, 'U_F + U_KE kabinleri', t6, t, "Üst kabinler aynı düzende: taban → yanlar (taban yan kaynakları) → arka → omega + tavan. Tavan yan sacların arasına oturur. U_F'de bina beslemesi için gömme giriş cebi; U_F ile U_KE 3 × M8 ile birbirine bağlanır.",
         'U_F: taban, 2 yan, arka, giriş cebi, omega, tavan · U_KE: taban, 2 yan, arka, omega, tavan · 3 × M8')
    t = sac_tamam(t)
    no = 7
    t, no = diger(t, no, R(r'^M__'), "Ana pano U_F'nin içinde bağımsız bir paslanmaz pano ürünüdür (ayakları U_F tabanındaki PEM'lere); havalandırma fanı ve panjuru U_F arka sacına.")
    olay(t, 'U tamam'); kam(t, None); t += 2.0
    return t




# ------------------------------------------------------------------ TOPPING + F (adım 6 devamı · 4 Eki)
def AN(pred):
    """henüz yerleşmemiş ana-model parçaları (küme) — pred(ad, bilgi, lo, hi)"""
    out = []
    for a in P:
        if P[a]['kay'] != 'ana' or a in GOR or a in GIZLI: continue
        b = ANA_BILGI[a]; lo, hi = bbox([a])
        if pred(a, b, lo, hi): out.append(a)
    return sorted(out)


def mekk(*kodlar):
    return lambda a, b, lo, hi: b['mek'] in kodlar


def kam_k(t, adlar, kay, uzak=None, yon=(0.55, 0.5, 1.0)):
    """kaydırılmış (tezgâhta / alt montajda) parçalara kamera"""
    lo, hi = bbox(adlar); h = (lo + hi) / 2 + np.array(kay, float)
    yon = np.array(yon, float); yon /= np.linalg.norm(yon)
    dist = uzak * 1.6 if uzak else min(max(_fit(lo, hi), _fit(ZARF[0], ZARF[1]) * 0.45), _fit(ZARF[0], ZARF[1]) * 1.05)
    pos = h + yon * dist; pos[1] = max(pos[1], 0.25)
    KAM.append([round(t, 2), [round(float(v), 4) for v in pos], [round(float(v), 4) for v in h]])


def gel_say(adlar, d, t, sure=1.1, top=2.4):
    """çok parçalı grup: aralık toplam süreye sığar"""
    if not adlar: return t
    ara = min(0.12, top / max(1, len(adlar)))
    return gel(adlar, d, t, sure, ara)


def seq_TOPPING():
    global SAHIP
    BASLIK.update(kod='TOPPING')
    SECIM[:] = [('dis_yan_sol', 1), ('dis_taban', 1), ('dis_tavan', 1), ('dis_arka_servis', 1), ('astar_arka', 1), ('raf', 1), ('ust_raf', 1), ('soguk_esik', 1),
                ('on_cerceve_430', 1), ('kaide_on_perde_menfezli', 1), ('sogutma_cebi', 1), ('evap_kanal_kovani_0_L1', 8)]
    t = kartlar(0.0, 'kaide 7 boru + menfezli ön perde C · dış kabuk 4 sac · sökülür arka servis sacı · soğuk oda 13 sac · 6 düşme kovanı · 4 evaporatör kanal kovanı')
    for a in R(r'^arayuz_(mek_|j1_)'): GIZLI.add(a)        # mekanizma FHP-M5 / J1 burçları: karşı parça ana modelde
    PANEL = ['kaide_ust_plaka_4', 'dis_taban', 'dis_yan_sol', 'dis_yan_sag', 'dis_tavan', 'sogutma_cebi']
    SAHIP = sahip_ata(PANEL)
    # 4 kaide
    t4 = t; kam(t, R(r'^kaide_'), (0, 1, 0))
    olay(t, 'Kaide boruları (40 × 100 × 2) fikstürde: arka, sol, sağ, enine · boyuna borular')
    t = gel(R(r'^kaide_(arka|sol|sag|enine)_boru$'), (0, 0.45, 0), t, 1.0, 0.2) + 0.1
    t = gel(R(r'^kaide_boyuna_boru_\d$') + R(r'^kaide_enine_lama_\d$'), (0, 0.45, 0), t, 1.0, 0.15)
    t = kaynak(R(r'^kaide_.*(boru|lama).*kaynak'), t) + 0.2
    olay(t, 'Menfezli ön perde (2,0 C) — kanat menfezleri hizasında · soğutma cebi taşıyıcı L × 2')
    t = gel(R(r'^kaide_on_perde_menfezli$'), (0, 0, 0.5), t, 1.1)
    t = gel(R(r'^kaide_cep_tasiyici_\d$'), (0, 0.3, 0), t, 0.8, 0.15) + 0.1
    olay(t, 'Kaide üst plakası 4 mm — PEM SP-M6 (ray + gövde) DÜZ sacta basılı · 17 delik kaynağı')
    sap = sorted(s for s, p in SAHIP.items() if p == 'kaide_ust_plaka_4')
    t = gel(['kaide_ust_plaka_4'] + sap, (0, 0.55, 0), t, 1.3) + 0.1
    t = kaynak(R(r'^kaide_ust_plaka_delik_kaynagi'), t, 0.35, 0.05) + 0.4
    adim(4, 'Kaide · menfezli ön perde', t4, t,
         "TOPPING kaidesi 40 × 100 × 2 borulardan fikstürde kaynaklanır. Önde menfezli 2,0 mm C perde (kanat menfezleriyle aynı hizada, kuru bölmenin emiş havası buradan), arkada emiş filtresi yeri. Üst plaka 4 mm; tabla rayının 4 × M6 ve gövdenin 2 × M6 PEM'i düz sacta basılıdır.",
         '7 boru + enine lama · menfezli ön perde C · 2 cep taşıyıcı L · üst plaka 4 mm + 6 PEM SP-M6 · 17 delik kaynağı')
    # 5 dış kabuk + kuru bölme
    t5 = t
    t = panel(['dis_taban'], (0, 0.45, 0), t, 'Dış taban 1,5 (3 büküm) kaideye — servis sacının PEM SP-M5 somunları arka dönüşte')
    olay(t, 'Gövde → kaide: 2 × ISO 4762 M6 tabandan plakadaki PEM\'e')
    t = gel(R(r'^arayuz_kaide_M6_[01]$'), (0, 0.12, 0), t, 0.5, 0.1) + 0.1
    t = panel(['dis_yan_sol'], (-0.6, 0, 0), t, "Sol yan sac (A tarafı) — tabla ağzı alta açık · A bağlantısı 4 × PEM SP-M8")
    t = gel(R(r'^pem_M8_A_\d+_\d+$'), (-0.15, 0, 0), t, 0.5, 0.05) + 0.1
    t = panel(['dis_yan_sag'], (0.6, 0, 0), t, "Sağ yan sac (F tarafı) — J1 ağzı 57 × 67 · F bağlantısı 4 × PEM SP-M8")
    t = gel(R(r'^pem_M8_F_\d+_\d+$'), (0.15, 0, 0), t, 0.5, 0.05) + 0.1
    t = panel(['dis_tavan'], (0, 0.55, 0), t, 'Dış tavan yanların arasına (yan dönüş yalnız kuru bölmede) · köşeler TIG')
    olay(t, 'Kuru (teknik) bölme: soğutma cebi + ayırma perdesi, teknik ön / sağ perde, kuru bölme tabanı')
    kam(t, R(r'^(sogutma_cebi|ayirma_perdesi|teknik_|kuru_bolme)'), (0, 0.3, 1))
    sap = sorted(s for s, p in SAHIP.items() if p == 'sogutma_cebi')
    t = gel(['sogutma_cebi'] + sap, (0, 0, 0.7), t, 1.1) + 0.1
    t = gel(R(r'^ayirma_perdesi_cep_sol$') + R(r'^teknik_(on|sag)_perde$'), (0, 0, 0.7), t, 1.0, 0.2)
    t = gel(R(r'^kuru_bolme_tabani$'), (0, 0, 0.7), t, 1.0) + 0.4
    adim(5, 'Dış kabuk · kuru bölme', t5, t,
         "Dış kabuk 304 1,5 mm, kaynaklı: taban → sol yan → sağ yan → tavan. Arka yüz açık kalır (sökülür servis sacı en sonda). Soğuk odanın altındaki kuru bölmede soğutma cebi (4 × PEM SP-M8 titreşim takozu), ayırma perdesi, teknik perdeler ve kuru bölme tabanı.",
         'dış taban · 2 × M6 gövde → kaide · sol yan + 4 PEM M8 (A) · sağ yan + 4 PEM M8 (F) · tavan · soğutma cebi · ayırma + teknik perdeler · kuru bölme tabanı')
    # 6 soğuk oda iç kabuğu + raflar
    t6 = t
    olay(t, 'Soğuk oda alt sacı + arka dış sacı (evaporatör kanal ağızları açık)')
    kam(t, R(r'^(soguk_|astar_|raf|ust_raf)'), (0, 0.3, 1))
    t = gel(R(r'^soguk_alt_sac$'), (0, 0, 0.8), t, 1.1)
    t = gel(R(r'^soguk_arka_dis_sac$'), (0, 0, 0.8), t, 1.1) + 0.1
    olay(t, '4 evaporatör kanal kovanı (iki L, boyuna dikiş) arka dış sac ile astar arasına')
    t = gel(R(r'^evap_kanal_kovani_\d_L\d$'), (0, 0, 0.5), t, 0.7, 0.06)
    t = kaynak(R(r'^evap_kanal_kovani_.*kaynak'), t, 0.3, 0.04) + 0.1
    olay(t, 'Astar 1,0 — 4 düz sac (arka, sol, sağ, tavan) · TIG + R3 iç köşe')
    t = gel(R(r'^astar_arka$'), (0, 0, 0.8), t, 1.0)
    t = gel(R(r'^astar_(sol|sag)$'), (0, 0, 0.8), t, 0.9, 0.2)
    t = gel(R(r'^astar_tavan$'), (0, 0, 0.8), t, 0.9) + 0.1
    olay(t, 'Raf 3,0 (iki büküm) + köşebentler · düşme kovanları (kıyma / kuşbaşı 3,0 sac · sos / harç boru · kaşar / sucuk POM-C)')
    kam(t, R(r'^(raf|dusme_kovani|dil_kanali|soguk_esik)'), (0, 0.4, 1))
    t = gel(R(r'^raf_kosebendi_(sol|sag)$'), (0, 0, 0.6), t, 0.7, 0.15)
    t = gel(R(r'^raf$'), (0, 0, 0.8), t, 1.0)
    t = kaynak(R(r'^raf_arka_kose_dolgusu'), t, 0.4) + 0.1
    t = gel(R(r'^dusme_kovani_(kiyma|kusbasi)_L\d$') + R(r'^dusme_kovani_(sos|harc|kasar|sucuk)$'), (0, -0.25, 0), t, 0.7, 0.08)
    t = kaynak(R(r'^dusme_kovani_.*kaynak'), t, 0.3, 0.04) + 0.1
    olay(t, 'Kaşar / sucuk dil kanalları (U 1,0) + eşik 1,2 — yiv dolgusu TIG + taşlama (gıda yüzeyi düz)')
    t = gel(R(r'^dil_kanali_(kasar|sucuk)$'), (0, 0, 0.5), t, 0.8, 0.15)
    t = gel(R(r'^soguk_esik$'), (0, 0, 0.6), t, 0.9)
    t = kaynak(R(r'^(raf_esik_yiv_dolgusu|esik_on_yiv_dolgusu)'), t, 0.3, 0.05)
    t = yerinde(R(r'^dil_kesik_kose_silikonu'), t, 0.3, 0.03) + 0.1
    olay(t, 'Üst raf 3,0 + köşebentler · raf askı burçları (POM + paslanmaz pim)')
    t = gel(R(r'^ust_raf_kosebendi_(sol|sag)$'), (0, 0, 0.6), t, 0.7, 0.15)
    t = gel(R(r'^ust_raf$'), (0, 0, 0.8), t, 1.0)
    burc = AN(lambda a, b, lo, hi: b['mek'] == 'TOPPING/Gövde' and not b['kpk'] and P[a]['m'] != 'kapak_s' and hi[2] < 0.0)
    t = gel_say(burc, (0, 0, 0.3), t, 0.6, 1.6) + 0.1
    olay(t, 'Ön çerçeve 430 1,0 önden — soğuk oda boşluğunu kapatır')
    t = gel(R(r'^on_cerceve_430$'), (0, 0, 0.7), t, 1.2) + 0.4
    adim(6, 'Soğuk oda · astar, raflar, eşik, kovanlar, ön çerçeve', t6, t,
         "Soğuk oda iç kabuğu dış kabuğun içine kurulur: alt sac, arka dış sac, 4 düz astar sacı. Raf ve üst raf 3 mm (iki büküm + köşebent); raf ile eşik dil kanalıyla tek parça. Malzeme düşme kovanları raftan geçer (kaşar / sucuk POM-C CNC, kıyma / kuşbaşı 3 mm sac, sos / harç boru). Evaporatör hava yolu için 4 kanal kovanı. Ön çerçeve köpük boşluğunu kapatır.",
         'alt sac · arka dış sac · 4 kanal kovanı · astar 4 sac · raf + 2 köşebent · 6 düşme kovanı · 2 dil kanalı · eşik · üst raf + 2 köşebent · raf burçları · ön çerçeve')
    # 7 PU
    t7 = t
    olay(t, 'Köpüklemeden önce: A tarafındaki PEM\'lere PE köpük kapağı')
    kam(t, None)
    t = yerinde(R(r'_kopuk_kapagi$'), t, 0.4, 0.1) + 0.2
    olay(t, 'PU köpükleme (SARI): dış kabuk ↔ astar ve raf / eşik içi, 40 kg/m³ — kalıpta, 24 saat kür')
    t = yerinde(sorted(a for a in P if P[a]['tur'] == 'pu' and a not in GOR), t, 1.6, 0.4) + 0.6
    adim(7, 'PU köpükleme', t7, t,
         "Soğuk odanın duvarları ve raf / eşik çift cidarı PU ile doldurulur (sahnede sarı; normalde görünmez). Evaporatör kanal kovanları köpüğün içinden geçer, ağızları açık kalır.",
         '2 köpük kapağı · PU soğuk duvar · PU raf + eşik')
    # 8 arka servis sacı alt montajı (tezgâhta, arkada)
    t8 = t
    SV = (0, 0, -1.1)
    serv_kutu = AN(lambda a, b, lo, hi: b['mek'] == 'TOPPING/Elektrik' and b['dugum'] in ('TOPPING_MODUL__sac', 'TOPPING_MODUL__celik'))
    SERV = ['dis_arka_servis'] + R(r'^kaide_arka_emis_filtresi$') + serv_kutu
    olay(t, 'Arka servis sacı alt montajı (tezgâhta, arkada): sac + pano kutusu + DIN plakası / rayları + emiş filtresi')
    kam_k(t, ['dis_arka_servis'], SV, uzak=1.5, yon=(0.5, 0.45, -1.0))
    t = gel(['dis_arka_servis'], (0, 0, -0.5), t, 1.2) + 0.1
    t = gel(serv_kutu, (0, 0, -0.35), t, 0.9, 0.15) + 0.1
    t = gel(R(r'^kaide_arka_emis_filtresi$'), (0, -0.2, 0), t, 0.7) + 0.4
    adim(8, 'Arka servis sacı · alt montaj', t8, t,
         "Arka yüz tek parça sökülür servis sacıdır (bakım bu yüzden). Pano kutusu, DIN plakası, emiş filtresi ve evaporatör ayakları bu sacın FHP-M5 saplamalarına bağlanır; sacla birlikte sökülür. Sac şimdilik tezgâhta bekler — iç montaj arkadan yapılır, sac en sonda 17 × M5 ile kapanır.",
         'servis sacı 1,5 · pano kutusu · DIN plakası + rayları · emiş filtresi')
    t = sac_tamam(t)
    no = 9
    # 9 soğutma
    t0 = t
    sog = AN(mekk('TOPPING/Soğutma'))
    grup = [a for a in sog if bbox([a])[1][1] < 1.105 and P[a]['m'] != 'pu']
    bak = [a for a in sog if ANA_BILGI[a]['dugum'].endswith(('__bakir', '__silikon')) and a not in grup]
    evL = [a for a in sog if a not in grup and a not in bak and bbox([a])[0][0] < 1.70]
    evR = [a for a in sog if a not in grup and a not in bak and a not in evL]
    olay(t, 'Soğutma grubu (Secop) arkadan soğutma cebine — 4 silikon titreşim takozu cep tabanındaki PEM SP-M8\'lere')
    kam(t, grup, (0, 0.2, -1))
    t = gel(grup, (0, 0, -0.8), t, 1.4) + 0.2
    olay(t, 'Evaporatör L ve R (kaset + fan) arkadan — kanal kovanlarının ağzına, ayakları servis sacının FHP-M5 saplamalarına')
    kam(t, evL + evR, (0, 0.2, -1))
    t = gel(evL, (0, 0, -0.8), t, 1.3) + 0.15
    t = gel(evR, (0, 0, -0.8), t, 1.3) + 0.2
    olay(t, 'Bakır hatlar (emiş / sıvı) + yoğuşma hortumu — grup ↔ evaporatörler, kanal içinden')
    kam(t, bak, (0, 0.2, -1))
    t = gel(bak, (0, 0, -0.5), t, 1.3, 0.2) + 0.5
    adim(no, 'Soğutma grubu + evaporatör L / R + bakır hatlar', t0, t,
         "Kompakt soğutma grubu (Secop) kuru bölmedeki cebe titreşim takozlarıyla oturur. İki evaporatör kaseti soğuk odanın arkasında, kanal kovanlarının ağzında; ayakları servis sacına bağlanır. Bakır hatlar ve yoğuşma hortumu grubu evaporatörlere bağlar.",
         'soğutma grubu + 4 takoz · evaporatör L · evaporatör R · bakır hatlar · yoğuşma hortumu'); no += 1
    # 10 kaset tahrik motorları
    t0 = t
    km = AN(lambda a, b, lo, hi: b['mek'] in ('TOPPING/Kaşar', 'TOPPING/Sucuk') and b['dugum'] == 'TOPPING_MODUL__motor')
    olay(t, 'Kaşar + sucuk kaset tahrik motorları arkadan — kaplin raf arkasında, kaset sürülünce geçer')
    kam(t, km, (0, 0.2, -1))
    t = gel(km, (0, 0, -0.6), t, 1.2, 0.3) + 0.5
    adim(no, 'Kaset tahrik motorları', t0, t, "Kaşar ve sucuk kasetlerinin tahrik motorları soğuk odanın arkasındaki kuru boşlukta sabit kalır; kaset önden sürüldüğünde kaplin kendiliğinden geçer (kaset sökülürken motor yerinde).",
         '2 kaset tahrik motoru'); no += 1
    # 11 elektrik
    t0 = t
    elk = AN(mekk('TOPPING/Elektrik'))
    kart = [a for a in elk if ANA_BILGI[a]['dugum'] in ('TOPPING_MODUL__kart', 'TOPPING_MODUL__koyu')]
    kanal = [a for a in elk if P[a]['m'] == 'kanal' or ANA_BILGI[a]['dugum'] == 'ELK_TOPPING__celik']
    fis = [a for a in elk if P[a]['m'] == 'fis' or ANA_BILGI[a]['dugum'] == 'ELK_ZINCIR__paslanmaz']
    guc = [a for a in elk if P[a]['m'] == 'guc' and a not in fis]
    bil = [a for a in elk if P[a]['m'] == 'bilgi' and a not in fis]
    kalanE = [a for a in elk if a not in kart + kanal + fis + guc + bil]
    olay(t, 'Sürücü kartları DIN rayına + istasyon kutusu cihazları (servis sacı üstünde, tezgâhta)')
    kam_k(t, kart, SV, uzak=1.1, yon=(0.5, 0.45, -1.0))
    t = gel(kart + kalanE, (0, 0.25, 0), t, 0.8, 0.15) + 0.2
    SERV += kart + kalanE
    olay(t, 'İç kablo kanalları + braketler (PEM saplamalı kanal ayakları)')
    kam(t, kanal, (0, 0.2, -1))
    t = gel_say(kanal, (0, 0, -0.45), t, 0.9, 1.6) + 0.2
    olay(t, 'Güç kabloları (KIRMIZI) — motorlara, kanal içinden')
    kam(t, guc, (0, 0.2, -1)); t = gel_say(guc, (0, 0, -0.45), t, 1.0, 2.0) + 0.2
    olay(t, 'Bilgi kabloları (MAVİ) — sensör, enkoder, EtherCAT · ayrı kanal bölmesinden')
    kam(t, bil, (0, 0.2, -1)); t = gel_say(bil, (0, 0, -0.45), t, 1.0, 2.0) + 0.2
    olay(t, 'Gömme fiş paneli (J1, sağ yanda): Harting güç + M12 bilgi + kablo rakorları')
    kam(t, fis, (1, 0.1, 0))
    t = gel_say(fis, (0.3, 0, 0), t, 0.9, 1.6) + 0.5
    adim(no, 'Elektrik · kartlar, kutu, kanallar, kablolar, fiş paneli', t0, t,
         "Sürücü kartları ve istasyon kutusu cihazları servis sacındaki DIN rayına (sacla birlikte sökülür). Kablolar yalnız kanal içinden: güç kırmızı, bilgi mavi, ayrı bölmelerden. İstasyona dışarıdan yalnız sağ yandaki gömme J1 fiş panelinden girilir (Harting / M12).",
         '%d sürücü kartı + kutu cihazları · iç kanallar · güç (kırmızı) · bilgi (mavi) · J1 fiş paneli' % sum(1 for a in kart if 'kart' in ANA_BILGI[a]['dugum'])); no += 1
    # 12 hava
    t0 = t
    hv = AN(mekk('TOPPING/Hava'))
    vada = [a for a in hv if ANA_BILGI[a]['dugum'] in ('TOPPING_MODUL__siyah', 'TOPPING_MODUL__aluminyum', 'TOPPING_MODUL__pom')]
    olay(t, 'Valf adası (12 valf) arka bölmeye · hava kanalı + askılar')
    kam(t, hv, (0, 0.2, -1))
    t = gel(vada, (0, 0, -0.4), t, 0.9, 0.05) + 0.1
    kn = [a for a in hv if a not in vada and ANA_BILGI[a]['dugum'].startswith(('HAVA_IC__', 'ELK_ZINCIR__rakor', 'ELK_ZINCIR__kod'))]
    t = gel_say(kn, (0, 0, -0.35), t, 0.8, 1.4) + 0.1
    olay(t, 'Hava hortumları (YEŞİL) — valf adasından UNO pistonlarına, J1 hava rakorundan girişe')
    t = gel_say([a for a in hv if a not in vada and a not in kn], (0, 0, -0.45), t, 1.1, 1.6) + 0.5
    adim(no, 'Valf adası + hava hortumları', t0, t, "Basınçlı hava J1 panelindeki gömme rakordan girer; valf adası 4 UNO pistonunu ve yayıcıları sürer. Hortumlar hava kanalında, askılarla.",
         'valf adası (12 valf) · hava kanalı + askılar · hava hortumları (yeşil)'); no += 1
    # 13 servis sacı kapanır
    t0 = t
    olay(t, 'Servis sacı (pano + kartlar + filtre üstünde) arkadan gelir — 17 × ISO 7380 M5 yan / tavan / taban dönüşündeki PEM SP-M5\'lere')
    kam(t, ['dis_arka_servis'], (0, 0, -1), uzak=1.9)
    ofset(SERV, SV, t, t + 2.0)
    t += 2.2
    t = gel(R(r'^servis_arka_.*_vida$'), (0, 0, -0.07), t, 0.45, 0.05) + 0.5
    adim(no, 'Arka servis sacı kapanır', t0, t, "İç montaj bitince servis sacı alt montajıyla birlikte arkadan takılır. Bombe başlı M5 vidalar gövde dönüşlerindeki PEM somunlara girer; bakımda sac tek parça çıkar (evaporatör bakır bağlantısı ayrılmalı — açık madde).",
         'servis sacı + pano + kartlar + filtre · 17 × ISO 7380 M5'); no += 1
    # 14 UNO
    t0 = t
    uno_ad = [('TOPPING/Kıyma', 'kıyma'), ('TOPPING/Kuşbaşı', 'kuşbaşı'), ('TOPPING/Sos', 'sos'), ('TOPPING/Harç', 'harç')]
    for kod, ad in uno_ad:
        g = AN(mekk(kod))
        h = [a for a in g if ANA_BILGI[a]['dugum'].endswith(('__hortum_gida', '__yayici_sabit_baglanti', '__conta'))]
        gv = [a for a in g if a not in h]
        olay(t, 'UNO · %s: hazne + piston + valf önden, raf burcuna · gıda hortumu + yayıcı' % ad)
        kam(t, g, (0, 0.2, 1))
        t = gel(gv, (0, 0, 0.8), t, 1.2) + 0.1
        t = gel(h, (0, -0.2, 0.2), t, 0.7, 0.1) + 0.2
    adim(no, "UNO'lar (4) + hortumlar + yayıcılar", t0, t + 0.3, "Dört dozaj ünitesi (kıyma, kuşbaşı, sos, harç) soğuk odaya önden girer, raf burçlarına oturur; pistonlar valf adasının hortumlarına bağlanır. Gıda hortumu ve yayıcı tabla üstüne düşen dozu dağıtır.",
         'UNO kıyma · UNO kuşbaşı · UNO sos · UNO harç · gıda hortumları · yayıcılar'); t += 0.3; no += 1
    # 15 kasetler
    t0 = t
    for kod, ad in (('TOPPING/Kaşar', 'kaşar'), ('TOPPING/Sucuk', 'sucuk')):
        g = AN(mekk(kod))
        olay(t, '%s kaseti dil kanalından raya sürülür — kaplin motora geçer, mandal kilitler' % ad.capitalize())
        kam(t, g, (0, 0.2, 1))
        t = gel(g, (0, 0, 0.75), t, 1.8) + 0.3
    adim(no, 'Kaşar + sucuk kasetleri', t0, t + 0.2, "Kasetler hazır ünite olarak önden, raftaki dil kanalına oturan raydan sürülür; arkadaki motorun kaplinine geçer, mandal kilitler. Sökmek için mandal açılır, kaset çekilir (motor yerinde kalır).",
         'kaşar kaseti · sucuk kaseti · mandal'); t += 0.2; no += 1
    # 16 tabla + X ekseni
    t0 = t
    tb = AN(mekk('TOPPING/Tabla'))
    ray = [a for a in tb if not ANA_BILGI[a]['dugum'].endswith(('__ARABA', '__TABLA')) and 'TABLA' not in ANA_BILGI[a]['dugum']]
    arb = [a for a in tb if a not in ray]
    olay(t, 'X ekseni: ray tabanı + lineer ray + tahrik motoru — tabanı 4 × M6 kaide plakasındaki PEM\'lere (A geçiş ağzından)')
    kam(t, tb, (0, 0.3, 1))
    t = gel(ray, (0, 0, 0.7), t, 1.4) + 0.1
    t = gel(R(r'^arayuz_kaide_M6_[2-5]$'), (0, 0.12, 0), t, 0.5, 0.1) + 0.1
    olay(t, 'Araba + bantlı tabla raya')
    t = gel(arb, (0, 0.35, 0), t, 1.2) + 0.5
    adim(no, 'Tabla + X ekseni', t0, t, "X ekseni rayı A'dan TOPPING'e uzanır; tabanı kaide plakasına 4 × M6. Tahrik motoru TOPPING ucundadır (A'da kablo yok). Araba ve bantlı tabla en son raya takılır.",
         'ray tabanı + lineer ray · X motoru · 4 × M6 · araba · tabla'); no += 1
    # 17 kapaklar
    t0 = t
    kp = AN(lambda a, b, lo, hi: b['mek'] == 'TOPPING/Gövde')
    gvd = [a for a in kp if not ANA_BILGI[a]['kpk'] and P[a]['m'] != 'kapak_s']
    kan = [a for a in kp if a not in gvd]
    olay(t, 'Gizli menteşe gövdeleri + bas-aç mandalları ön kasaya')
    kam(t, kp, (0, 0.1, 1))
    t = gel_say(gvd, (0, 0, 0.15), t, 0.6, 1.2) + 0.1
    olay(t, 'Kanatlar K1 / K2 (çift cidar + PU + fitil) önden, menteşelere')
    t = gel(kan, (0, 0, 0.6), t, 1.4) + 0.5
    adim(no, 'Kapaklar (kanatlar)', t0, t, "Ön kanatlar en son: menteşe gövdeleri ve bas-aç mandalları ön kasaya, kanatlar (çift cidar + PU + fitil, menfezli) önden asılır.",
         'menteşe gövdeleri · bas-aç · kanat K1 · kanat K2'); no += 1
    # 18 saha
    t0 = t
    GHOST_T.append(round(t, 2))
    GHOST.extend([[0.736, 4.4, 0.106, 0.788, -0.83, 0.039], [0.736, 1.436, 0.788, 2.2, -0.83, 0.079], [2.5, 4.0, 0.788, 2.2, -0.83, 0.079]])
    olay(t, 'Sahada: kaide B tavanına 4 × M8 + DIN 9021 (kaide borusunun içinden) — A, B, F silik')
    kam(t, R(r'^arayuz_kb'), (0, 1, 0.3))
    t = gel(R(r'^arayuz_kb_\d+_\d+_pul$'), (0, 0.12, 0), t, 0.5, 0.08)
    t = gel(R(r'^arayuz_kb_\d+_\d+$'), (0, 0.18, 0), t, 0.6, 0.08) + 0.2
    olay(t, 'TOPPING ↔ F: 4 × ISO 4762 M8 × 16, F içinden sağ yandaki PEM SP-M8\'lere')
    kam(t, R(r'^arayuz_m8_F'), (1, 0, 0))
    t = gel(R(r'^arayuz_m8_F_.*_pul$'), (0.08, 0, 0), t, 0.5, 0.1)
    t = gel(R(r'^arayuz_m8_F_\d+_\d+$'), (0.1, 0, 0), t, 0.6, 0.1) + 0.3
    olay(t, 'TOPPING tamam'); kam(t, None); t += 2.5
    adim(no, 'Saha · B, A ve F bağlantısı', t0, t, "TOPPING kaidesi B tavanına 4 × M8 ile bağlanır. A, TOPPING'in sol yanındaki PEM'lere A içinden (A sayfasında); F sağ yandaki PEM'lere F içinden 4 × M8.",
         '4 × M8 + DIN 9021 (B) · 4 × M8 × 16 (F)')
    for a in R(r'^arayuz_'): GIZLI.add(a)
    return t


def seq_F():
    global SAHIP
    BASLIK.update(kod='F')
    SECIM[:] = [('onyuz_kapak_F_sol_dis_tava', 2), ('onyuz_kapak_F_sol_alt_kayit', 2), ('onyuz_kapak_F_sol_ust_kayit', 2), ('davlumbaz_atis_kanali_L1', 2),
                ('baca_ic_kanal_L1', 2), ('baca_dis_kilif_L1', 2), ('baca_ust_flansi_on', 2), ('baca_alt_kapama_lamasi_on', 2)]
    for a in R(r'^arayuz_|_mentese_\d+_vida_\d+$'): GIZLI.add(a)      # karşı parça U sacında / menteşe vidası menteşeyle gelir
    GHOST_T.append(0.0)
    GHOST.extend([[2.5, 4.0, 0.106, 0.788, -0.83, 0.039], [1.436, 2.5, 0.788, 2.2, -0.83, 0.079], [4.0, 4.4, 0.788, 1.862, -0.83, 0.079]])
    t = kartlar(0.0, 'davlumbaz atış kanalı 2 L · baca iç kanal 2 L + dış kılıf 2 L + 4 alt lama + 4 üst flanş · 2 ön kapak (dış tava + 2 omega + 2 kayıt + karşılık)')
    # 4 davlumbaz atış kanalı
    t4 = t
    olay(t, 'F üst kabini (U sayfası) ve komşular silik. Davlumbaz atış kanalı: iki L 1,5, boyuna dikiş — fırın üstünden baca ağzına')
    kam(t, R(r'^davlumbaz_'), (0, 0.3, 1))
    t = gel(R(r'^davlumbaz_atis_kanali_L\d$'), (0, 0, 0.6), t, 1.1, 0.25)
    t = kaynak(R(r'^davlumbaz_atis_kanali_.*kaynak'), t, 0.4, 0.1) + 0.4
    adim(4, 'Davlumbaz atış kanalı', t4, t, "Fırın buharı davlumbaz bölmesinden atış kanalıyla yukarı, bacaya gider. Kanal 296 × 196, iki L sacın boyuna kaynağıyla; üst ucu bacanın iç kanalına 30 mm teleskopik girer (yüksek sıcaklık silikonu).",
         'atış kanalı L1 + L2 · 2 boyuna dikiş')
    # 5 baca
    t5 = t
    olay(t, 'Baca iç kanalı (iki L 1,5) · taş yünü A1 sarılır')
    kam(t, R(r'^baca_'), (0, 0.4, 1))
    t = gel(R(r'^baca_ic_kanal_L\d$'), (0, 0.5, 0), t, 1.0, 0.2)
    t = kaynak(R(r'^baca_ic_kanal_.*kaynak'), t, 0.4, 0.1) + 0.1
    t = yerinde(R(r'^yalitim_baca'), t, 1.0) + 0.1
    olay(t, 'Dış kılıf (iki L 0,8) taş yününün üstüne · alt kapama lamaları + köşe silikonu')
    t = gel(R(r'^baca_dis_kilif_L\d$'), (0, 0.5, 0), t, 1.0, 0.2)
    t = kaynak(R(r'^baca_dis_kilif_.*kaynak'), t, 0.4, 0.1)
    t = gel(R(r'^baca_alt_kapama_lamasi_'), (0, -0.2, 0), t, 0.7, 0.1)
    t = yerinde(R(r'^baca_alt_kose_silikonu'), t, 0.3, 0.05) + 0.1
    olay(t, "Üst flanş 4 lama (3 mm) + 8 PEM SP-M6 kör başlıklı — U_F tavanına 8 × M6 (U sayfası)")
    t = gel(R(r'^baca_ust_flansi_'), (0, 0.3, 0), t, 0.8, 0.1)
    t = gel(R(r'^baca_flans_pem_M6_\d$'), (0, 0.15, 0), t, 0.5, 0.03)
    t = gel(R(r'^baca_flans_pem_M6_\d_kapak$'), (0, 0.15, 0), t, 0.5, 0.03) + 0.4
    adim(5, 'Baca · iç kanal, taş yünü, dış kılıf, flanş', t5, t, "Baca çift cidarlıdır: iç kanal 1,5 + taş yünü A1 + dış kılıf 0,8 (dışı elle tutulur sıcaklıkta). Altta kapama lamaları yalıtımı örter; üstte 3 mm flanş U_F tavanına 8 × M6 ile bağlanır.",
         'iç kanal 2 L · taş yünü · dış kılıf 2 L · 4 alt lama + silikon · 4 flanş lamaya 8 PEM SP-M6')
    # 6 ön kapak alt montajı (tezgâhta)
    t6 = t
    ST = (0, 0, 0.9)
    KAPS = {}
    for taraf in ('sol', 'sag'):
        k = 'onyuz_kapak_F_%s' % taraf
        KAP = sorted(a for a in P if a.startswith(k) and a not in GIZLI)
        KAPS[taraf] = KAP
        olay(t, 'Ön kapak %s (tezgâhta, önde): dış tava 1,5 — bindirme köşeler TIG · 36 panjur yarığı' % ('sol' if taraf == 'sol' else 'sağ'))
        kam_k(t, [k + '_dis_tava'], ST, uzak=1.6, yon=(0.4, 0.35, 1.0))
        t = gel([k + '_dis_tava'], (0, 0.3, 0), t, 1.0) + 0.1
        t = kaynak(R(r'^%s_dis_tava_kose_kaynagi' % k), t, 0.3, 0.08) + 0.1
        olay(t, '2 omega (hazır haddeli 40 × 15) + alt / üst kayıt (U 1,5) içeriden · menteşe PEM SP-M5 · bas-aç karşılığı')
        t = gel(R(r'^%s_omega_\d$' % k), (0, 0, -0.15), t, 0.7, 0.15)
        t = gel(R(r'^%s_(alt|ust)_kayit$' % k), (0, 0, -0.15), t, 0.7, 0.15)
        t = gel(R(r'^%s_mentese_\d+_pem_\d+$' % k), (0, 0, -0.06), t, 0.4, 0.04)
        t = gel(R(r'^%s_basac_karsilik$' % k), (0, 0, -0.08), t, 0.5) + 0.3
    adim(6, 'Ön kapaklar · tezgâhta alt montaj', t6, t, "İki ön kapak tezgâhta kurulur: dış tava 1,5 (bindirme köşe TIG, 36 panjur yarığı), içinde 2 omega ve alt / üst kayıt; menteşe PEM'leri ve bas-aç karşılığı. Kapaklar tezgâhta bekler, en son asılır.",
         'dış tava × 2 · 4 omega · 4 kayıt · 8 menteşe PEM SP-M5 · 2 bas-aç karşılığı · 8 köşe kaynağı')
    t = sac_tamam(t)
    no = 7
    # 7 TP10
    t0 = t
    fr = AN(lambda a, b, lo, hi: b['mek'] == 'F/Fırın' and P[a]['m'] not in ('fis', 'guc', 'bilgi', 'kanal'))
    olay(t, 'TP10 konveyör fırın (satın alınır, gövdesine dokunulmaz) önden B tavanındaki yerine sürülür')
    kam(t, fr, (0, 0.2, 1))
    t = gel(fr, (0, 0.05, 1.1), t, 2.6) + 0.5
    adim(no, 'TP10 fırın yerine', t0, t, "Fırın hazır cihazdır (TP10, kendi kabuğu + konveyör); yalnız yerine oturur. B tavanındaki ısı kalkanının üstüne önden sürülür, ayakları terazilenir.",
         'TP10 gövde · konveyör + tel bant · giriş / çıkış ruloları · çıkış plakası'); no += 1
    # 8 yükleme bandı
    t0 = t
    bd = AN(mekk('F/Yükleme bandı'))
    mt = [a for a in bd if ANA_BILGI[a]['dugum'].endswith(('__motor', '__aluminyum', '__koyu', '__sac')) and bbox([a])[1][1] > 1.09]
    olay(t, 'Yükleme bandı (PTFE bant + burun / tahrik ruloları) fırın girişinin içine')
    kam(t, bd, (0, 0.3, 1))
    t = gel([a for a in bd if a not in mt], (-0.5, 0, 0), t, 1.4) + 0.2
    olay(t, 'Bant motoru + braketi')
    t = gel(mt, (0, 0.25, 0), t, 0.9) + 0.5
    adim(no, 'Yükleme bandı + motoru', t0, t, "Yükleme bandı TOPPING tablasından gelen ürünü fırın konveyörüne verir; TP10 girişinin içinde, motoru üstte braketle.",
         'PTFE bant · burun + tahrik rulosu · bant motoru + braket'); no += 1
    # 9 davlumbaz fanı
    t0 = t
    dv = AN(lambda a, b, lo, hi: b['mek'] == 'F/Davlumbaz' and P[a]['m'] not in ('fis',))
    if dv:
        olay(t, 'Davlumbaz fanı + yağ filtresi bölmeye, atış kanalının altına')
        kam(t, dv, (0, 0.2, 1))
        t = gel(dv, (0, 0, 0.6), t, 1.2, 0.2) + 0.5
        adim(no, 'Davlumbaz fanı + filtre', t0, t, "Davlumbaz bölmesindeki fan ve filtre buharı atış kanalına basar.", 'fan · filtre'); no += 1
    # 10 elektrik
    t0 = t
    elk = AN(lambda a, b, lo, hi: b['mek'] in ('F/Elektrik', 'F/Fırın', 'F/Davlumbaz', 'F/Gövde', 'F/Hava') and P[a]['m'] in ('elektrik', 'kanal', 'guc', 'bilgi', 'fis')
             or (b['mek'] == 'F/Elektrik'))
    kutu = [a for a in elk if ANA_BILGI[a]['dugum'].startswith('ELK_ISTASYON__') and P[a]['m'] in ('elektrik', 'mekanizma', 'koyu')]
    kanal = [a for a in elk if P[a]['m'] == 'kanal']
    fis = [a for a in elk if P[a]['m'] == 'fis' or ANA_BILGI[a]['dugum'] in ('ELK_ZINCIR__paslanmaz', 'F_UST_KABIN__plastik')]
    fis = [a for a in fis if a not in kutu]
    guc = [a for a in elk if P[a]['m'] == 'guc' and a not in fis + kutu]
    bil = [a for a in elk if P[a]['m'] == 'bilgi' and a not in fis + kutu]
    rest = [a for a in elk if a not in kutu + kanal + fis + guc + bil]
    olay(t, 'F kutusu (sürücü + G/Ç + sigorta) arka alt köşeye, PEM saplamalara')
    kam(t, kutu + rest, (0, 0.2, -1))
    t = gel(kutu + rest, (0, 0, -0.5), t, 1.1, 0.12) + 0.2
    olay(t, 'İç kanallar arka duvar boyunca')
    kam(t, kanal, (0, 0.2, -1)); t = gel_say(kanal, (0, 0, -0.45), t, 1.0, 1.4) + 0.2
    olay(t, 'Güç kabloları (KIRMIZI) — fırın, bant motoru, fan, kompresör')
    kam(t, guc, (0, 0.2, -1)); t = gel_say(guc, (0, 0, -0.45), t, 1.0, 1.6) + 0.2
    olay(t, 'Bilgi kabloları (MAVİ) — sensör, EtherCAT / G/Ç')
    kam(t, bil, (0, 0.2, -1)); t = gel_say(bil, (0, 0, -0.45), t, 1.0, 1.6) + 0.2
    olay(t, 'Gömme fiş panelleri (Harting / M12) + rakorlar')
    kam(t, fis, (0, 0.2, -1)); t = gel_say(fis, (0, 0, -0.35), t, 0.9, 1.6) + 0.5
    adim(no, 'F kutusu + kanallar + kablolar + fiş panelleri', t0, t, "F'nin elektrik kutusu kendi gövdesinde (arka alt köşe). Kablolar kanal içinden: güç kırmızı, bilgi mavi. Komşu istasyonlara yalnız gömme fiş panellerinden bağlanılır.",
         'F kutusu · iç kanallar · güç (kırmızı) · bilgi (mavi) · fiş panelleri'); no += 1
    # 11 kompresör + hava
    t0 = t
    hv = AN(lambda a, b, lo, hi: b['mek'] == 'F/Hava' or (b['mek'] == 'F/Gövde' and b['dugum'] == 'F_UST_KABIN__paslanmaz'))
    kmp = [a for a in hv if ANA_BILGI[a]['dugum'].startswith(('HAVA_KOMPRESOR__kompresor', 'HAVA_KOMPRESOR__siyah', 'F_KOMP_AYAK'))]
    olay(t, 'Kompresör titreşim ayaklarıyla F üst kabin tabanındaki PEM\'lere (davlumbaz bölmesinin önünde)')
    kam(t, kmp, (0, 0.3, 1))
    t = gel(kmp, (0, 0.3, 0.4), t, 1.4) + 0.2
    olay(t, 'Hava hortumları (YEŞİL) + kelepçe / askı lamaları — kompresörden hat boyunca istasyonlara')
    rh = [a for a in hv if a not in kmp]
    kam(t, rh, (0, 0.2, -1)); t = gel_say(rh, (0, 0, -0.45), t, 1.1, 1.6) + 0.5
    adim(no, 'Kompresör + hava hattı', t0, t, "Hattın hava kaynağı kompresör F üst kabinindedir; hava hortumları kelepçe ve askı lamalarıyla arka kanal boyunca TOPPING, K ve E'ye gider.",
         'kompresör + ayaklar · hava hortumları (yeşil) · kelepçe + askı lamaları'); no += 1
    # 12 kapaklar
    t0 = t
    kp = AN(lambda a, b, lo, hi: b['mek'] == 'F/Gövde' and (b['kpk'] or P[a]['m'] == 'kapak_s'))
    olay(t, 'Menteşeler (gövde + kanat) ve gazlı yaylar + bilyeli braketler')
    kam(t, kp, (0, 0.1, 1))
    t = gel_say(kp, (0, 0, 0.3), t, 0.8, 1.2) + 0.2
    olay(t, 'Ön kapaklar tezgâhtan gelir — menteşelere asılır, gazlı yaya takılır, bas-aç ile kapanır')
    KAP = KAPS['sol'] + KAPS['sag']
    kam(t, KAP, (0, 0.1, 1), uzak=2.0)
    ofset(KAP, ST, t, t + 1.9)
    t += 2.4
    adim(no, 'Ön kapaklar', t0, t, "Kapaklar en son, iç montaj bittikten sonra asılır: alt kenardaki menteşeler, yanlarda gazlı yaylar, üstte bas-aç. Panjur yarıkları fırın bölmesinin havalandırmasıdır.",
         'menteşe × 4 · gazlı yay × 2 · ön kapak sol · ön kapak sağ'); no += 1
    kal = AN(lambda a, b, lo, hi: True)
    if kal:
        t0 = t; olay(t, 'Yedek pizza kutusu stoku (görsel)'); kam(t, kal, (0, 0.5, 1))
        t = gel(kal, (0, 0.3, 0.3), t, 1.0, 0.1) + 0.5
        adim(no, 'Ürün', t0, t, "Fırın üstündeki yedek pizza kutusu stoku (görsel).", 'pizza kutusu yedeği'); no += 1
    olay(t, 'F tamam'); kam(t, None); t += 2.0
    return t


SEQ = {'A': seq_A, 'B': seq_B, 'E': seq_E, 'U': seq_U, 'TOPPING': seq_TOPPING, 'F': seq_F}
TOPLAM = round(SEQ[IST](), 2)
eksik = kalan()
if eksik:
    print('YERLEŞMEYEN', len(eksik)); [print('   ', a) for a in eksik[:80]]
    raise SystemExit(1)

# ------------------------------------------------------------------ GLB
MATAD = ['sac', 'kapak', 'profil', 'kaynak', 'baglanti', 'arayuz', 'pu', 'yalitim', 'mekanizma', 'motor', 'alu', 'koyu', 'sensor', 'elektrik',
         'kanal', 'fis', 'guc', 'bilgi', 'hava', 'kapak_s', 'urun']
MATS = [dict(name=m, pbrMetallicRoughness=dict(baseColorFactor=[0.8, 0.8, 0.8, 1], metallicFactor=0.5, roughnessFactor=0.4)) for m in MATAD]
dug, PARCA = [], {}
gos = [a for a in P if a not in GIZLI]
for a in gos:
    V = P[a]['V']; c = np.round((V.min(0) + V.max(0)) / 2, 4)
    dug.append(dict(ad=a, V=(V - c).astype(np.float32), F=np.asarray(P[a]['F'], np.uint32), mat=MATAD.index(P[a]['m']), translation=c))
    PARCA[a] = dict(c=c.tolist(), m=P[a]['m'], bb=[np.round(V.min(0), 6).tolist(), np.round(V.max(0), 6).tolist()], g=GOR[a], h=HAR[a])
    if ROT[a]: PARCA[a]['r'] = ROT[a]
    if a in KAY: PARCA[a]['k'] = 1
yol = os.path.join(OUT, '%s_montaj.glb' % ist)
glbio.yaz(yol, dug, MATS)
f = open(yol, 'rb').read(); L = struct.unpack('<I', f[12:16])[0]; JJ = json.loads(f[20:20 + L]); rest = f[20 + L:]
for nd, d in zip(JJ['nodes'], dug): nd['translation'] = [float(x) for x in d['translation']]
js = json.dumps(JJ, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
while len(js) % 4: js += b' '
f = struct.pack('<III', 0x46546C67, 2, 12 + 8 + len(js) + len(rest)) + struct.pack('<II', len(js), 0x4E4F534A) + js + rest
open(yol, 'wb').write(f); boy = len(f)

say = {}
for a in gos:
    g = 'ana:' + P[a]['m'] if P[a]['kay'] == 'ana' else P[a]['tur']
    say[g] = say.get(g, 0) + 1
ACI = acinim_liste(SECIM)
OUTJ = dict(surum='%s_montaj_v1' % ist, ist=IST, tarih='4 Eki 2026', kaynak='gece2/adim5/%s_sac_v1.glb (h3_%s_sac_v1) + hat3_v8zq.glb (gövde dışı, salt okunur)' % (IST, ist),
            birim='m', toplam=TOPLAM, baslik=BASLIK, zarf=ZARF.round(4).tolist(), ghost=GHOST, ghost_t=GHOST_T[0] if GHOST_T else None,
            adimlar=ADIM, olaylar=OLAY, kamera=KAM, parcalar=PARCA, acinim=ACI, montaj_sirasi=MONTAJ_SIRASI,
            sayim=dict(gosterilen=len(gos), sac_parca=sum(1 for a in gos if P[a]['kay'] == 'sac'), ana_grup=sum(1 for a in gos if P[a]['kay'] == 'ana'),
                       gizli=len(GIZLI), ucgen=int(sum(len(P[a]['F']) for a in gos)), grup=say),
            ana_gruplar=ANA_BILGI)
json.dump(OUTJ, open(os.path.join(OUT, '%s_montaj.json' % ist), 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
print(IST, 'parça', len(gos), 'gizli', len(GIZLI), 'üçgen', OUTJ['sayim']['ucgen'], 'GLB %.2f MB' % (boy / 1e6), 'süre %.1f s' % TOPLAM, 'adım', len(ADIM))
print(say)
