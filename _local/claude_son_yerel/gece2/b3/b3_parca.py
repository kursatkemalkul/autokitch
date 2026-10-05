# -*- coding: utf-8 -*-
"""B montaj v3 · parça çıkarımı: hat3_v9l → b3_parca.pkl  (mm, dünya)
Gövde (B_KASA__*, B_MODULER__baglanti, B_TASIYICI__baglanti): adım-34 ent aralıkları (hat3_v9b_ent.json · aralıklar v9l'de geçerli).
Diğerleri: b_bil.pkl bileşenleri (düğüm + mek + bağlı bileşen) → konum / düğümle sınıflandırılır."""
import sys, os, json, pickle, re, collections
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
sys.path.insert(0, os.path.join(HERE, '..', 'cekmece')); sys.stdout.reconfigure(encoding='utf-8')
from glb import G
g = G(os.path.join(HERE, '..', '..', 'hat3_v9l.glb'))
ENT = json.load(open(os.path.join(HERE, '..', 'adim8', 'is_tam', 'hat3_v9b_ent.json'), encoding='utf-8'))['parca']
BIL = pickle.load(open('b_bil.pkl', 'rb'))['B']
P = {}


def ekle(ad, V, F, m, tur, ac, **k):
    V = np.asarray(V, float); F = np.asarray(F, np.int64)
    u, inv = np.unique(np.round(V, 4), axis=0, return_inverse=True)
    P[ad] = dict(V=u, F=inv.reshape(-1)[F], m=m, tur=tur, ac=ac, **k)


def birles(L):
    VV, FF, n = [], [], 0
    for V, F in L: VV.append(V); FF.append(np.asarray(F) + n); n += len(V)
    return np.vstack(VV), np.vstack(FF)


# ---------------------------------------------------------------- gövde (ent)
NT = {}
def node_tri(d):
    if d not in NT:
        X, T = g.tris(g.byname[d])[0][:2]; NT[d] = (X, T)
    return NT[d]


def ent_mesh(ad):
    v = ENT[ad]; X, T = node_tri(v['dugum']); a, n = v['indis']; Tt = T[a // 3:(a + n) // 3]
    u, inv = np.unique(Tt.reshape(-1), return_inverse=True)
    return X[u], inv.reshape(-1, 3)


from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
YENI = {}
for dug in sorted(set(v['dugum'] for v in ENT.values())):
    X, T = node_tri(dug)
    Pt = X[T]; ar = np.linalg.norm(np.cross(Pt[:, 1] - Pt[:, 0], Pt[:, 2] - Pt[:, 0]), axis=1); ok = ar > 1e-9
    C = Pt.mean(1)
    adlar = [a for a, v in ENT.items() if v['dugum'] == dug]
    K = np.array([ENT[a]['kutu'] for a in adlar]); vol = (K[:, 1] - K[:, 0]) * (K[:, 3] - K[:, 2]) * (K[:, 5] - K[:, 4])
    tol = 1.2 if dug == 'B_KASA__conta' else 0.06
    ata = -np.ones(len(T), int)
    idx = np.where(ok)[0]
    Tv = T[idx]; uu, inv = np.unique(np.round(X[Tv.reshape(-1)], 3), axis=0, return_inverse=True); Vi = inv.reshape(-1, 3)
    r = np.concatenate([Vi[:, 0], Vi[:, 1]]); c = np.concatenate([Vi[:, 1], Vi[:, 2]])
    n_, cl = connected_components(coo_matrix((np.ones(len(r)), (r, c)), shape=(len(uu), len(uu))), directed=False)
    tc = cl[Vi[:, 0]]
    sira = np.argsort(tc, kind='stable'); sinir = np.flatnonzero(np.diff(tc[sira])) + 1
    for grp in np.split(sira, sinir):
        ti = idx[grp]; Q = Pt[ti].reshape(-1, 3); lo, hi = Q.min(0), Q.max(0)
        icer = np.where(np.all(K[:, [0, 2, 4]] <= lo + tol, 1) & np.all(K[:, [1, 3, 5]] >= hi - tol, 1))[0]
        if len(icer):
            ata[ti] = icer[np.argmin(vol[icer])]; continue
        # birleşik bileşen (dokunan parçalar ortak köşeli): üçgen tam içinde olan en küçük kutu
        tl = Pt[ti].min(1); th = Pt[ti].max(1); best = np.full(len(ti), np.inf); sec = -np.ones(len(ti), int)
        for i in range(len(adlar)):
            k = K[i]; m = np.all(tl >= k[[0, 2, 4]] - tol, 1) & np.all(th <= k[[1, 3, 5]] + tol, 1) & (vol[i] < best)
            sec[m] = i; best[m] = vol[i]
        ata[ti] = sec
    for i, a in enumerate(adlar):
        Tt = T[ata == i]
        if not len(Tt): print('  BOŞ', a); continue
        u, inv = np.unique(Tt.reshape(-1), return_inverse=True)
        v = ENT[a]
        if v['tur'] == 'sac': m_, tur = ('kapak' if v['dugum'] == 'B_KASA__on_cerceve' else 'sac'), 'sac'
        elif a.startswith('pu_') or a.endswith('_pu'): m_, tur = 'pu', 'pu'
        elif 'kaynagi' in a: m_, tur = 'kaynak', 'kaynak'
        elif 'silikon' in a: m_, tur = 'koyu', 'silikon'
        elif 'kopuk_kapagi' in a: m_, tur = 'koyu', 'baglanti'
        elif a.startswith('isi_kalkani_takozu'): m_, tur = 'koyu', 'mek'
        else: m_, tur = 'baglanti', 'baglanti'
        ekle('g_' + a, X[u], inv.reshape(-1, 3), m_, tur, a, kaynak=dug, bom=v.get('bom'))
    kalan = np.where(ok & (ata < 0))[0]
    if len(kalan):
        Tk = T[kalan]; uu, inv = np.unique(np.round(X[Tk.reshape(-1)], 3), axis=0, return_inverse=True); Vi = inv.reshape(-1, 3)
        r = np.concatenate([Vi[:, 0], Vi[:, 1]]); c = np.concatenate([Vi[:, 1], Vi[:, 2]])
        n_, cl = connected_components(coo_matrix((np.ones(len(r)), (r, c)), shape=(len(uu), len(uu))), directed=False)
        tc = cl[Vi[:, 0]]
        for j in np.unique(tc):
            Tj = Tk[tc == j]; u, inv2 = np.unique(Tj.reshape(-1), return_inverse=True)
            YENI.setdefault(dug, []).append((X[u], inv2.reshape(-1, 3)))
for dug, L in YENI.items():
    print('  adım 44 eklentisi', dug, len(L), [tuple(np.round(V.max(0) - V.min(0), 2)) for V, F in L[:3]])
    for j, (V, F) in enumerate(L):
        e = V.max(0) - V.min(0)
        if dug == 'B_KASA__paslanmaz': ekle('g_ray_pem_arka_%02d' % j, V, F, 'baglanti', 'baglanti', 'PEM SP-M5-1 (arka iç sac)')
        elif dug == 'B_KASA__conta': ekle('g_ray_pem_arka_%02d_kopuk_kapagi' % j, V, F, 'koyu', 'baglanti', 'köpük kapağı (arka PEM)')
        elif dug.endswith('baglanti'): ekle('g_percin_somun_ek_%02d' % j, V, F, 'baglanti', 'baglanti', 'M8 perçin somun')
        elif dug == 'B_KASA__on_cerceve': ekle('g_cerceve_derz_dolgusu', V, F, 'kapak', 'sac', 'ön çerçeve derz dolgu şeridi')
        else: ekle('g_yeni_%s_%02d' % (dug.replace('__', '_'), j), V, F, 'baglanti', 'baglanti', 'adım 44 eklentisi')
print('gövde (ent):', sum(1 for a in P if a.startswith('g_')))

# ---------------------------------------------------------------- diğer bileşenler
def sec(onek, filt=lambda o: True):
    return [o for o in BIL if o['dug'].startswith(onek) and filt(o)]


def ad_kutu(o): return o['lo'], o['hi']


# şase / modüler / taşıyıcı
k = 0
for o in sec('B_MODULER__paslanmaz'):
    lo, hi = ad_kutu(o)
    if hi[1] <= 123.5 and hi[0] - lo[0] > 3000: nm = 'sase_boy_%s' % ('arka' if lo[2] < -400 else 'on')
    elif hi[1] <= 123.5: nm = 'sase_capraz_%d' % round(lo[0])
    elif hi[0] - lo[0] > 500: nm = 'moduler_cerceve_%s' % ('arka' if lo[2] < -400 else 'on')
    else: nm = 'moduler_dikme_%d_%s' % (round(lo[0]), 'arka' if lo[2] < -400 else 'on')
    ekle(nm, o['V'], o['F'], 'profil', 'profil', 'AISI 304 kutu profil')
gf = sec('B_MODULER__gfrp')
ekle('gfrp_alt', *birles([(o['V'], o['F']) for o in gf if o['hi'][1] < 130]), 'koyu', 'mek', 'GFRP ısı köprüsü takozu × 6 (3 mm)')
for o in gf:
    if o['hi'][1] > 700: ekle('gfrp_ust_%s' % ('arka' if o['lo'][2] < -400 else 'on'), o['V'], o['F'], 'koyu', 'mek', 'GFRP üst şerit (3 mm)')
for o in sec('B_TASIYICI__celik'):
    lo, hi = ad_kutu(o)
    if hi[0] - lo[0] > 500: nm = 'tasiyici_ust'
    elif hi[1] - lo[1] < 3: nm = 'tasiyici_plaka_%d' % round(lo[2])
    else: nm = 'tasiyici_dikme_%d_%d' % (round(lo[0]), round(-lo[2]))
    ekle(nm, o['V'], o['F'], 'profil', 'profil', 'taşıyıcı kutu profil 30 × 30')
ekle('ayaklar', *birles([(o['V'], o['F']) for o in sec('B_KASA__celik')]), 'mekanizma', 'mek', '14 ayarlı ayak M12 (katalog)')
for o in sec('B_MODULER__baglanti') + sec('B_TASIYICI__baglanti'):
    pass
# soğutma
SOG = sec('B_SOGUTMA') + sec('DUZ_B_SERPANTIN')
ev = {1: [], 2: []}; grp = []; gider = []
for o in SOG:
    cx = (o['lo'][0] + o['hi'][0]) / 2
    if o['dug'] == 'B_SOGUTMA__plastik' and o['hi'][0] < 4085 and not (o['lo'][0] > 2020 and o['hi'][0] < 2045) and not (o['lo'][0] > 3010 and o['hi'][0] < 3025): gider.append(o)
    elif cx < 2100: ev[1].append(o)
    elif cx < 3400: ev[2].append(o)
    elif o['dug'] == 'B_SOGUTMA__sac' and o['lo'][2] > 30: ekle('sogutma_on_izgara', o['V'], o['F'], 'sac', 'kapak', 'soğutma bölmesi ön ızgarası')
    elif o['dug'] == 'B_SOGUTMA__celik' and o['lo'][2] > 20: grp.append(('izgara_tutucu', o))
    else: grp.append(('grup', o))
for i in (1, 2):
    ekle('evaporator_%d' % i, *birles([(o['V'], o['F']) for o in ev[i]]), 'alu', 'mek', 'evaporatör %d (fan + serpantin + damlama tavası + braketler · tek ürün)' % i)
ekle('sogutma_grubu', *birles([(o['V'], o['F']) for k_, o in grp if k_ == 'grup']), 'motor', 'mek', 'soğutma grubu (kompresör + kondenser + fan · tek ürün)')
ekle('izgara_tutucu', *birles([(o['V'], o['F']) for k_, o in grp if k_ == 'izgara_tutucu']), 'mekanizma', 'mek', 'ızgara tutucuları')
ekle('gider_hortumu', *birles([(o['V'], o['F']) for o in gider]), 'hava', 'kablo', 'gider hortumu (evaporatörlerden)')
# elektrik
ekle('elektrik_kutusu', *birles([(o['V'], o['F']) for o in sec('B_ELEKTRIK')]), 'elektrik', 'mek', 'B elektrik kutusu (Siemens + kartlar · tek ürün)')
ekle('istasyon_kutusu', *birles([(o['V'], o['F']) for o in sec('ELK_ISTASYON')]), 'elektrik', 'mek', 'istasyon kutusu (pano + DIN + rakor)')
for o in sec('B_KABLO__kanal'):
    ekle('b_kanal_%d' % round(o['lo'][0]), o['V'], o['F'], 'kanal', 'mek', 'B kablo kanalı')
ic = sec('ELK_IC__kanal')
for i_, o in enumerate(sorted(ic, key=lambda o: (round(o['lo'][0]), round(o['lo'][1]), round(o['lo'][2])))):
    ekle('ic_kanal_%02d' % i_, o['V'], o['F'], 'kanal', 'mek', 'iç kablo kanalı parçası')
ekle('zincir_kanal', *birles([(o['V'], o['F']) for o in sec('ELK_ZINCIR') + sec('ELK_ZEMIN')]), 'kanal', 'mek', 'enerji zinciri kanalı + zemin contası')
ekle('guc_kablo', *birles([(o['V'], o['F']) for o in sec('ELK_DOLAP__kablo', lambda o: o['dug'] == 'ELK_DOLAP__kablo')]), 'guc', 'kablo', 'güç kabloları')
ekle('kablo_klips', *birles([(o['V'], o['F']) for o in sec('ELK_DOLAP__celik')]), 'baglanti', 'baglanti', 'kablo klipsi')
SIN = sec('ELK_DOLAP__kablo_sinyal')
ekle('acil_stop', *birles([(o['V'], o['F']) for o in sec('ACIL_STOP')]), 'guc', 'mek', 'acil stop Schneider XB4BS8442 (tek ürün)')
# soğuk depo
dep = sec('B_DEPO')
ekle('depo_ray', *birles([(o['V'], o['F']) for o in dep if o['dug'] == 'B_DEPO__celik']), 'mekanizma', 'ray', 'depo sabit rayları (sol / sağ)')
for o in dep:
    if o['dug'] == 'B_DEPO__sac': ekle('depo_arka_sac' if o['hi'][2] - o['lo'][2] < 3 else 'depo_ic_sac', o['V'], o['F'], 'sac', 'sac', 'depo arka sacı' if o['hi'][2] - o['lo'][2] < 3 else 'depo iç sacı (taban + yanlar)')
ekle('depo_cekmece', *birles([(o['V'], o['F']) for o in dep if '__CEKMECE' in o['dug']]), 'sac', 'mek', 'depo çekmecesi (ön panel + PU + conta + ara ray + kızak)')

# ---------------------------------------------------------------- çekmeceler (21)
CEK = collections.defaultdict(list)
for o in BIL:
    m_ = re.match(r'(CEK_K\d_[a-z0-9]+_\d+)__(.+)$', o['dug'])
    if m_: CEK[m_.group(1)].append((m_.group(2), o))
URUN = ('hamur', 'kutu_icecek')
CEKD = {}
# ray vidaları (arayuz_ray_*): ent adı arayuz_ray_<x>_<y>_<z>
RVIDA = [a for a in P if a.startswith('g_arayuz_ray')]
for ck in sorted(CEK):
    L = CEK[ck]
    rays = [o for mt, o in L if mt == 'celik' and (o['hi'][2] - o['lo'][2]) > 600 and (o['hi'][0] - o['lo'][0]) < 12 and len(o['F']) > 1000]
    rays.sort(key=lambda o: o['lo'][0]); assert len(rays) == 2, (ck, len(rays))
    R0 = rays[0]['lo'].copy(); R0[0] = rays[0]['lo'][0] + 1453.5 - 1453.5
    # K2-3 başvurusu: sol sabit ray alt köşesi (1453.5, 420.5, -677) — v3 ile aynı
    tah, tvid, ava, gov, ara, kay, cene_alt, cene_vida, cene_somun, cene_ust = [], [], [], [], [], [], [], [], [], []
    def yakin(lo, ext, lo_b, ext_b, tol=0.35): return np.all(np.abs(lo - np.array(lo_b)) < tol) and np.all(np.abs(ext - np.array(ext_b)) < tol)
    for mt, o in L:
        if any(mt.startswith(u) for u in URUN): continue
        if o is rays[0] or o is rays[1]: continue
        lo = o['lo'] - R0; hi = o['hi'] - R0; ext = o['hi'] - o['lo']; c = (lo + hi) / 2
        if mt.endswith('__CEKMECE_ARA'): ara.append(o); continue
        if '__CEKMECE' in mt:
            if yakin(lo[1:], ext[1:], (37.45, -74.0), (3.7, 30.0)) and ext[0] < 22: cene_alt.append(o); continue
            if abs(lo[1] - 34.21) < 0.3 and abs(ext[1] - 13.65) < 0.3: cene_vida.append(o); continue
            if abs(lo[1] - 35.05) < 0.3 and abs(ext[1] - 2.4) < 0.3: cene_somun.append(o); continue
            if abs(lo[1] - 41.21) < 0.3 and abs(ext[1] - 5.0) < 0.3:          # üst çene + kol tablası (ortak köşeli tek bileşen) → üçgenle ayır
                T = o['V'][o['F']]; cy = T[:, :, 1].mean(1) - R0[1]
                nrm = np.cross(T[:, 1] - T[:, 0], T[:, 2] - T[:, 0])[:, 1]
                cmask = (cy < 43.71 - 1e-3) | ((np.abs(cy - 43.71) <= 1e-3) & (nrm > 0))
                cene_ust.append((o['V'], o['F'][cmask])); gov.append(dict(V=o['V'], F=o['F'][~cmask])); continue
            gov.append(o); continue
        if mt == 'koyu' and ext[2] > 600: kay.append(o); continue
        if ext[2] > 600: ava.append(o); continue
        if mt == 'celik' and abs(ext[0] - 10) < 0.3 and abs(ext[1] - 10) < 0.3 and abs(ext[2] - 6) < 0.3 and c[2] + R0[2] < -700: tvid.append(o); continue
        if lo[1] >= 45.9 and hi[0] <= 21.0: ava.append(o); continue
        if c[2] + R0[2] > -300: ava.append(o)
        else: tah.append(o)
    CEKD[ck] = dict(R0=R0, sol=rays[0]['lo'][0], sag=rays[1]['hi'][0], y=R0[1])
    for i, (r, yan) in enumerate(((rays[0], 'sol'), (rays[1], 'sag'))):
        ekle('%s_ray_%s' % (ck, yan), r['V'], r['F'], 'mekanizma', 'ray', 'Accuride DZ3832-0700 ray ünitesi (dış eleman)')
        vs = [a for a in RVIDA if a in P and (P[a]['V'].min(0)[1] > r['lo'][1] - 2 and P[a]['V'].max(0)[1] < r['hi'][1] + 2 and
                                   abs((P[a]['V'].min(0)[0] + P[a]['V'].max(0)[0]) / 2 - (r['lo'][0] + r['hi'][0]) / 2) < 15 and
                                   P[a]['V'].min(0)[2] > r['lo'][2] - 2 and P[a]['V'].max(0)[2] < r['hi'][2] + 2)]
        assert len(vs) == 3, (ck, yan, len(vs))
        ekle('%s_vida_%s' % (ck, yan), *birles([(P[a]['V'], P[a]['F']) for a in vs]), 'baglanti', 'baglanti', '3 × DIN 7991 M5 × 6 A2 havşa (ray → PEM SP-M5)',
             eks=(-1.0 if yan == 'sol' else 1.0, 0.0, 0.0))
        for a in vs: P.pop(a)
    assert len(tvid) == 2 and len(cene_alt) == 1 and len(cene_vida) == 2 and len(cene_somun) == 2 and len(cene_ust) == 1 and len(kay) == 1, (ck, len(tvid), len(cene_alt), len(cene_vida), len(cene_somun), len(cene_ust), len(kay))
    brk = [o for o in tah if np.all(np.abs((o['hi'] - o['lo']) - [43.0, 44.0, 38.5]) < 0.3)]
    mv = [o for o in tah if np.all(np.abs((o['hi'] - o['lo']) - [6.0, 6.0, 6.0]) < 0.3)]
    ks = [o for o in tah if abs((o['hi'] - o['lo'])[0] - 11.0) < 0.3 and abs((o['hi'] - o['lo'])[1] - 33.51) < 0.3]
    ss = [o for o in tah if np.all(np.abs((o['hi'] - o['lo']) - [2.9, 2.9, 4.0]) < 0.3)]
    rest = [o for o in tah if not any(o is x for x in brk + mv + ks + ss)]
    assert len(brk) == 1 and len(mv) == 4 and len(ks) == 1 and len(ss) == 1, (ck, len(brk), len(mv), len(ks), len(ss))
    ekle(ck + '_braket', brk[0]['V'], brk[0]['F'], 'sac', 'sac', 'motor braketi 3 mm (1 büküm · göbek deliği · 2 × M5 / 4 × M3 havşa)')
    ekle(ck + '_tahrik', *birles([(o['V'], o['F']) for o in rest]), 'motor', 'mek', 'step motor Transmotec PD3665 (redüktör + mil + enkoder + M12, katalog)')
    ekle(ck + '_motor_vida', *birles([(o['V'], o['F']) for o in mv]), 'baglanti', 'baglanti', '4 × DIN 7991 M3 × 6 A2 (braket → motor yüzü M3)', eks=(1.0, 0.0, 0.0))
    ekle(ck + '_kasnak', ks[0]['V'], ks[0]['F'], 'alu', 'mek', 'GT3 motor kasnağı 30 diş (katalog)', eks=(1.0, 0.0, 0.0))
    ekle(ck + '_setskur', ss[0]['V'], ss[0]['F'], 'baglanti', 'baglanti', 'DIN 913 M3 × 4 setskur', eks=(0.0, 0.0, -1.0))
    ekle(ck + '_tahrik_vida', *birles([(o['V'], o['F']) for o in tvid]), 'baglanti', 'baglanti', '2 × DIN 7991 M5 × 6 A2 (braket → arka PEM SP-M5)', eks=(0.0, 0.0, -1.0))
    ekle(ck + '_avara', *birles([(o['V'], o['F']) for o in ava]), 'mekanizma', 'mek', 'avara ünitesi: avara kolu + sensör laması + mil + kasnak + E segman + 2 reed sensör (kaynaklı, tezgâhta)')
    ekle(ck + '_cekmece', *birles([(o['V'], o['F']) for o in gov]), 'sac', 'mek', 'çekmece alt montajı (kutu + kızaklar + ön kapak + tepsi + kayış kolu + mıknatıs)')
    ekle(ck + '_ara', *birles([(o['V'], o['F']) for o in ara]), 'mekanizma', 'ray', 'ray ara elemanları (sol / sağ)')
    ekle(ck + '_kayis', kay[0]['V'], kay[0]['F'], 'koyu', 'kablo', 'GT3 kayış')
    ekle(ck + '_cene_alt', cene_alt[0]['V'], cene_alt[0]['F'], 'sac', 'sac', 'çene alt gövdesi (alt çene 2,5 + ara 1,2 · TIG)')
    ekle(ck + '_cene_ust', cene_ust[0][0], cene_ust[0][1], 'sac', 'sac', 'üst çene 2,5')
    ekle(ck + '_cene_vida', *birles([(o['V'], o['F']) for o in cene_vida]), 'baglanti', 'baglanti', '2 × ISO 7380 M3 × 12 A2', eks=(0.0, -1.0, 0.0))
    ekle(ck + '_cene_somun', *birles([(o['V'], o['F']) for o in cene_somun]), 'baglanti', 'baglanti', '2 × ISO 4032 M3 A2 somun', eks=(0.0, 1.0, 0.0))
    # kablolar: bu çekmecenin x aralığı + y yakınlığı
print('çekmece', len(CEKD))
# sinyal kablolarını çekmecelere dağıt (en yakın y), kalanlar = evaporatör kabloları
kul = set()
for ck, d in sorted(CEKD.items()):
    pass
for o in SIN:
    cx = (o['lo'][0] + o['hi'][0]) / 2; best = None
    for ck, d in CEKD.items():
        if d['sol'] - 660 < o['lo'][0] < d['sag'] and o['hi'][2] > -100:
            dy = abs(o['lo'][1] - (d['y'] + 420.5 - 420.5 - 162.5))
    o['_c'] = None
# basit: kablo x aralığı → sütun; y → sıra (kablo y ≈ R0y − 162,5 … +16)
for o in SIN:
    if o['hi'][2] < -600 and o['lo'][2] > -800 and o['hi'][1] - o['lo'][1] > 100: o['_c'] = 'evap'; continue
    cand = []
    for ck, d in CEKD.items():
        if d['sol'] - 5 <= o['lo'][0] <= d['sol'] + 20:
            cand.append((abs(o['lo'][1] - (d['y'] + 53.5)), ck))
    if cand: o['_c'] = min(cand)[1]
by = collections.defaultdict(list)
for o in SIN: by[o.get('_c')].append(o)
for ck in CEKD:
    if by.get(ck): ekle(ck + '_kablo', *birles([(o['V'], o['F']) for o in by[ck]]), 'bilgi', 'kablo', 'reed sensör + motor kabloları')
if by.get('evap'): ekle('evap_kablo', *birles([(o['V'], o['F']) for o in by['evap']]), 'bilgi', 'kablo', 'evaporatör fan kabloları')
if by.get(None): print('ATANMAYAN kablo', len(by[None]), [np.round(o['lo']) for o in by[None]])
print('kablo dağılımı', {k: len(v) for k, v in by.items()})
pickle.dump(dict(P=P, ENT=ENT, CEKD={k: dict(R0=v['R0'], sol=v['sol'], sag=v['sag'], y=v['y']) for k, v in CEKD.items()}), open('b3_parca.pkl', 'wb'))
for a in sorted(P):
    if not a.startswith(('g_ray_pem', 'g_arayuz', 'CEK_')): print('%-34s %6d  lo %s hi %s' % (a, len(P[a]['F']), np.round(P[a]['V'].min(0), 1), np.round(P[a]['V'].max(0), 1)))
print('TOPLAM', len(P))
