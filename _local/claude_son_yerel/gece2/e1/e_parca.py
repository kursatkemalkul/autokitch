# -*- coding: utf-8 -*-
"""E montaj v2 · parça çıkarımı: hat3_v10h (zincir 00–66) → e_parca.pkl (mm, dünya)
Adlı parçalar: zincir adımlarının _ent.json kayıtları (35 E gövde / kaide / kapaklar · 59 emniyet) — bileşen kutusu kaydın kutusunun içinde (0,6 mm),
birden çok kutuya düşerse EN KÜÇÜK kutu.
Kalan E bileşenleri (şarjör, asansör, besleyici, kutu katlama alt montajları, robot çöpü, elektrik, hava): düğüm + mek ile ürün grupları.
E dışı her şey silik çevre. Kullanım: python e_parca.py"""
import sys, os, json, pickle, collections
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
sys.stdout.reconfigure(encoding='utf-8')
BIL = pickle.load(open('e_bil.pkl', 'rb'))
MEK = BIL['MEK']; L = BIL['L']
P = {}
ENTF = [(os.path.join(HERE, 'ent', 'hat3_v9c_ent.json'), None),                              # adım 35 E gövde
        (os.path.join(HERE, 'ent', 'hat3_v10a_ent.json'), lambda a, v: '_E_' in a),          # adım 59 emniyet
        (os.path.join(HERE, 'ent', 'hat3_v10k_ent.json'), None),                             # adım 69 arka PEM + cıvata
        (os.path.join(HERE, 'ent', 'hat3_v10l_ent.json'), None)] + \
       [(os.path.join(HERE, 'ent', 'hat3_v10%s_ent.json' % s_), None) for s_ in 'mnopq']     # adım 81–85 E mekanizma bağlantıları + yeni braketler + kaynaklar
ENT = {}
for f_, s_ in ENTF:
    for a, v in json.load(open(f_, encoding='utf-8'))['parca'].items():
        if s_ is None or s_(a, v): ENT[a] = v
# zincir 80: üst sol sensör + aktüatör x −20 · y −100 · sağdaki iki sensör + aktüatör x +1 (kayıt kutuları adım 59'dan)
for a_, d_ in (('emniyet_E_UST_SOL_sensor', (-20, -100)), ('emniyet_E_UST_SOL_aktuator', (-20, -100)), ('emniyet_E_ALT_SAG_sensor', (1, 0)),
               ('emniyet_E_ALT_SAG_aktuator', (1, 0)), ('emniyet_E_UST_SAG_sensor', (1, 0)), ('emniyet_E_UST_SAG_aktuator', (1, 0))):
    if a_ in ENT:
        k_ = list(ENT[a_]['kutu']); k_[0] += d_[0]; k_[1] += d_[0]; k_[2] += d_[1]; k_[3] += d_[1]; ENT[a_] = dict(ENT[a_], kutu=k_)
print('ent kayıt', len(ENT), collections.Counter(v['dugum'] for v in ENT.values()).most_common())


def ekle(ad, V, F, m, tur, ac, **k):
    V = np.asarray(V, float); F = np.asarray(F, np.int64)
    u, inv = np.unique(np.round(V, 4), axis=0, return_inverse=True)
    assert ad not in P, ad
    P[ad] = dict(V=u, F=inv.reshape(-1)[F], m=m, tur=tur, ac=ac, **k)


def birles(LL):
    VV, FF, n = [], [], 0
    for o in LL: VV.append(o['V']); FF.append(np.asarray(o['F']) + n); n += len(o['V'])
    return np.vstack(VV), np.vstack(FF)


def kod(o): return MEK[o['mek']]['kod'] if o['mek'] >= 0 else ''
def ic(o, lo, hi, tol=0.6): return np.all(o['lo'] >= np.array(lo) - tol) and np.all(o['hi'] <= np.array(hi) + tol)
ATANAN = set()
def grup(ad, LL, m, tur, ac, **k):
    LL = [o for o in LL if id(o) not in ATANAN]
    if ad in P:
        i = 2
        while '%s_%d' % (ad, i) in P: i += 1
        ad = '%s_%d' % (ad, i)
    assert LL, ad
    for o in LL: ATANAN.add(id(o))
    ekle(ad, *birles(LL), m, tur, ac, **k)
def sec(f): return [o for o in L if id(o) not in ATANAN and f(o)]


def sinif(a, v):
    t = v.get('tur', ''); bom = '; '.join(str(x) for x in (v.get('bom') or []) if isinstance(x, str))
    d = v['dugum']
    if 'kaynak' in a or 'kaynagi' in a or 'punta' in a: return 'kaynak', 'kaynak', bom or 'TIG dikişi'
    if 'silikon' in a or d.endswith('__conta'): return 'yapistirici', 'silikon', bom
    if d.endswith('__yalitim') or a.startswith('yalitim'): return 'pu', 'pu', bom
    if t in ('arayuz', 'baglanti') or any(w in a for w in ('_pem', 'pem_', '_vida', 'vida_', '_percin', 'percin_', '_somun', '_pul', '_saplama', 'arayuz_', 'civata',
                                                           '_setskur', '_segman', '_pim', '_sap')) \
            or any(w in bom for w in ('cıvata', 'vida', 'PEM', 'perçin', 'somun', 'pul ', 'saplama')):
        return 'baglanti', 'baglanti', bom
    if t == 'profil' or 'omega' in a or 'profil' in a: return 'profil', 'profil', bom
    if t == 'sac' or bom.startswith('Sac') or d.endswith('__sac'): return 'sac', 'sac', bom
    return 'mekanizma', 'mek', bom


# ---------------------------------------------------------------- 1. adlı parçalar (ent kutusu)
# zincir 69: preslenmiş somunun deliği (r 2,5) cıvata gövdesiyle çakışık yüzey → tek bağlı bileşen. Üçgen başına ayır:
# baş + arka sac içindeki gövde (z < −828,5) ve eksenden DIŞA bakan r ≈ 2,5 yüzeyler + uç kapağı → cıvata · diğerleri (gövde dışı, eksene bakan delik) → somun
for o in [o for o in L if o['dug'] == 'E_GOVDE_BAG__vida']:
    Q = o['V'][o['F']]; C = Q.mean(1); n = np.cross(Q[:, 1] - Q[:, 0], Q[:, 2] - Q[:, 0])
    yc = min((float(a.split('_')[-1]) for a in ENT if a.startswith('e_arka_civata_')), key=lambda y: abs(y - (o['lo'][1] + o['hi'][1]) / 2))
    yc = [v for a, v in ENT.items() if a == 'e_arka_civata_%d' % yc][0]['kutu']; ax = np.array([(yc[0] + yc[1]) / 2, (yc[2] + yc[3]) / 2])
    rv = C[:, :2] - ax; r = np.linalg.norm(rv, axis=1)
    civ = (C[:, 2] < -828.5) | ((r < 2.6) & ((np.einsum('ij,ij->i', n[:, :2], rv) > 0) | (np.abs(n[:, 2]) > np.linalg.norm(n[:, :2], axis=1))))
    for ad_, mm in (('civata', civ), ('pem', ~civ)):
        Tc = o['F'][mm]; u, inv = np.unique(Tc.reshape(-1), return_inverse=True)
        L.append(dict(o, V=o['V'][u], F=inv.reshape(-1, 3), lo=o['V'][u].min(0), hi=o['V'][u].max(0)))
    L.remove(o)
ENT_DUG = set(v['dugum'] for v in ENT.values())
TOPLA = collections.defaultdict(list)
for o in list(L):
    if o['dug'] not in ENT_DUG: continue
    en, hc = None, None
    for a, v in ENT.items():
        if v['dugum'] != o['dug']: continue
        k = v['kutu']; lo, hi = [k[0], k[2], k[4]], [k[1], k[3], k[5]]
        if ic(o, lo, hi):
            h = float(np.prod(np.subtract(hi, lo) + 1e-3))
            if hc is None or h < hc: en, hc = a, h
    if en: TOPLA[en].append(o); continue
    # birbirine bitişik (ortak kenarlı) adlı saclar tek bileşen: üçgen merkezi hangi kayıt kutusundaysa (en küçük) ona
    Q = o['V'][o['F']]; Tl = Q.min(1); Th = Q.max(1); C = Q.mean(1); lab = np.full(len(C), '', dtype=object); hcv = np.full(len(C), np.inf)
    for a, v in ENT.items():
        if v['dugum'] != o['dug']: continue
        k = v['kutu']; lo, hi = np.array([k[0], k[2], k[4]]) - 0.6, np.array([k[1], k[3], k[5]]) + 0.6
        m = np.all(Tl >= lo, 1) & np.all(Th <= hi, 1); h = float(np.prod(hi - lo))
        m &= h < hcv; lab[m] = a; hcv[m] = h
    if not (lab != '').any(): continue
    for a in set(lab) - {''}:
        mm = lab == a; Tc = o['F'][mm]; u, inv = np.unique(Tc.reshape(-1), return_inverse=True)
        TOPLA[a].append(dict(o, V=o['V'][u], F=inv.reshape(-1, 3), lo=o['V'][u].min(0), hi=o['V'][u].max(0)))
    if (lab == '').any():
        mm = lab == ''; Tc = o['F'][mm]; u, inv = np.unique(Tc.reshape(-1), return_inverse=True)
        L.append(dict(o, V=o['V'][u], F=inv.reshape(-1, 3), lo=o['V'][u].min(0), hi=o['V'][u].max(0), artik=True))
    ATANAN.add(id(o))
for a in sorted(TOPLA):
    m, t, bom = sinif(a, ENT[a]); grup(a, TOPLA[a], m, t, bom, dugum=ENT[a]['dugum'], kpk=a.startswith(('onyuz_kapak_E', 'sarjor_yan_kapisi')) or a.endswith('aktuator'))
eks = sorted(a for a in ENT if a not in TOPLA)
print('adlı parça', len(TOPLA), '· model karşılığı olmayan kayıt', len(eks), eks[:20])

# ---------------------------------------------------------------- 1b. E mekanizma parçaları tek tek (zincir 81–85 · veri/e_mek_parcalar.json kutuları; 'ek' kutuları aynı parçaya)
MEKV = json.load(open(os.path.join(HERE, '..', '..', '..', '..', 'arastirma', '_uretec', 'h3', 'yama_v9', 'veri', 'e_mek_parcalar.json'), encoding='utf-8'))
MEK_KUTU = [(k, d, np.array(lo), np.array(hi), float(np.prod(np.subtract(hi, lo)))) for k, v in MEKV.items()
            for d, lo, hi in [(v['dug'], v['lo'], v['hi'])] + [(e['dug'], e['lo'], e['hi']) for e in v.get('ek', [])]]
MTOP = collections.defaultdict(list)
for o in L:
    if id(o) in ATANAN: continue
    en, hc = None, None
    for k, d, lo, hi, h in MEK_KUTU:
        if d == o['dug'] and h < (hc if hc is not None else np.inf) and ic(o, lo, hi, 0.8): en, hc = k, h
    ic_ic = en and any(k != en and d == o['dug'] and h < hc and np.all(lo >= o['lo'] - 0.8) and np.all(hi <= o['hi'] + 0.8) for k, d, lo, hi, h in MEK_KUTU)
    if en and not ic_ic: MTOP[en].append(o); continue                         # bileşenin içinde başka (küçük) adlı parça kutusu yoksa bütün olarak
    # delik açma (zincir 81–85) değen parçaları aynı ağda birleştirmiş olabilir: üçgen başına en küçük kutuya ayır
    KD = [(k, lo, hi, h) for k, d, lo, hi, h in MEK_KUTU if d == o['dug'] and np.all(o['hi'] >= lo - 0.8) and np.all(o['lo'] <= hi + 0.8)]
    if not KD: continue
    Q = o['V'][o['F']]; Tl = Q.min(1); Th = Q.max(1); lab = np.full(len(Q), '', dtype=object); hcv = np.full(len(Q), np.inf)
    for k, lo, hi, h in KD:
        m = np.all(Tl >= lo - 0.8, 1) & np.all(Th <= hi + 0.8, 1) & (h < hcv); lab[m] = k; hcv[m] = h
    C = Q.mean(1); hc2 = np.full(len(Q), np.inf); bos_ = lab == ''                 # kalan (iki parçaya taşan) üçgenler: merkezine göre
    for k, lo, hi, h in KD:
        m = bos_ & np.all(C >= lo - 0.8, 1) & np.all(C <= hi + 0.8, 1) & (h < hc2); lab[m] = k; hc2[m] = h
    if not (lab != '').any(): continue
    for k in sorted(set(lab) - {''}):
        mm = lab == k; Tc = o['F'][mm]; u, inv = np.unique(Tc.reshape(-1), return_inverse=True)
        MTOP[k].append(dict(o, V=o['V'][u], F=inv.reshape(-1, 3), lo=o['V'][u].min(0), hi=o['V'][u].max(0)))
    if (lab == '').any():
        mm = lab == ''; Tc = o['F'][mm]; u, inv = np.unique(Tc.reshape(-1), return_inverse=True)
        L.append(dict(o, V=o['V'][u], F=inv.reshape(-1, 3), lo=o['V'][u].min(0), hi=o['V'][u].max(0), artik=True))
    ATANAN.add(id(o))
def mek_m(k, v):
    d = v['dug']; r = v['rol']
    if r == 'motor' or d.endswith('__motor') or '__motor__' in d: return 'motor'
    if r in ('sensor',) or '__sensor' in d: return 'sensor'
    if r in ('kayis', 'vantuz', 'hortum') or 'kayis' in d or 'kaucuk' in d: return 'koyu'
    if 'aluminyum' in d or 'plastik' in d: return 'alu'
    return 'mekanizma'
for k in sorted(MTOP):
    v = MEKV[k]; grup(k, MTOP[k], mek_m(k, v), 'mek', '%s · %s' % (v.get('tip', ''), k.replace('_', ' ')), aile=v['aile'], rol=v['rol'], mek_ad=True)
print('mekanizma parçası (adlı)', len(MTOP), '/', len(MEKV), '· eksik', sorted(set(MEKV) - set(MTOP))[:30])

# ---------------------------------------------------------------- 2. E bileşenleri: alt montajlar + elektrik + hava (düğüm / mek)
EK = lambda o: kod(o).startswith('E/')
def g_(ad, f, m, tur, ac, **k):
    LL = sec(lambda o: EK(o) and f(o))
    if LL: grup(ad, LL, m, tur, ac, **k)
def ds(*p): return lambda o: o['dug'].startswith(p)
g_('karton_stok', lambda o: o['dug'].startswith(('E_SARJOR__karton', 'E_KUTU__')), 'karton', 'urun', 'Kutu kartonu yığını (işletmede doldurulur)')
g_('sarjor_asansor', lambda o: o['dug'].startswith('E_SARJOR') or kod(o) == 'E/Asansör', 'mekanizma', 'mek', 'Şarjör + asansör (yığın kaldırma, motor + vida · hazır alt montaj)')
g_('besleyici_vakum', lambda o: o['dug'].endswith('__VAC_Y') or (kod(o) == 'E/Hava' and 'vakum' in o['dug']), 'mekanizma', 'mek', 'Vakum kolu (Y ekseni + vantuzlar · alt montaj)')
g_('besleyici_itici', lambda o: o['dug'].endswith('__ITICI'), 'mekanizma', 'mek', 'İtici (karton sürücü · alt montaj)')
g_('besleyici_motor', lambda o: o['dug'] in ('E_BESLEYICI__motor', 'E_BESLEYICI__kayis'), 'motor', 'mek', 'Besleyici motoru + kayış')
g_('besleyici_sasi', lambda o: o['dug'].startswith('E_BESLEYICI') or kod(o) == 'E/Besleyici', 'alu', 'mek', 'Besleyici şasisi (profil + raylar + sensör)')
for k_, ad_, ac_ in (('KOPRU', 'kopru', 'Köprü (katlama girişi · motor + sensör)'), ('NEST', 'kalip_yuva', 'Kalıp yuvası (nest)'),
                     ('KATLAYICI', 'kapak_katlayici', 'Kapak katlayıcı kolu'), ('CNR_LIFT', 'kose_kaldirici', 'Köşe kaldırıcılar × 4 (motorlu)'),
                     ('FRONT_Y', 'parmak_y', 'Ön parmak Y ekseni (motor + kayış)')):
    g_(ad_, lambda o, k_=k_: o['dug'].endswith('__' + k_), 'mekanizma', 'mek', ac_)
g_('kose_piston', lambda o: o['dug'].startswith('E_KOSE') and o['dug'].endswith('__PISTON'), 'mekanizma', 'mek', 'Köşe pistonu')
g_('kose_tutucu', lambda o: o['dug'].startswith('E_KOSE__CNR'), 'mekanizma', 'mek', 'Köşe tutucuları × 4')
g_('kalip', ds('E_KALIP'), 'alu', 'mek', 'Katlama kalıbı (çerçeve + motor + sensör · alt montaj)')
g_('kapak_mekanizmasi', ds('E_KAPAK'), 'mekanizma', 'mek', 'Kutu kapağı katlama mekanizması (motorlar + kol)')
g_('kopru_govde', ds('E_KOPRU'), 'mekanizma', 'mek', 'Köprü gövdesi + motor')
g_('parmak', ds('E_PARMAK'), 'mekanizma', 'mek', 'Ön parmaklar')
g_('piston_itici', lambda o: o['dug'].startswith('E_PISTON') and not o['dug'].endswith('__PISTON'), 'mekanizma', 'mek', 'Arka itici (motor + kayış + sensör)')
g_('piston', ds('E_PISTON'), 'mekanizma', 'mek', 'Arka itici pistonu')
g_('robot_copu', lambda o: o['dug'].startswith(('E_COP', 'DUZ_E_OLUK')), 'mekanizma', 'mek', 'Robot çöpü (kova + poşet + oluk · sol önde)')
g_('elk_sensor', lambda o: o['dug'].startswith('E_ELEKTRIK') and o['dug'].endswith(('__sensor', '__aluminyum')) and o['lo'][1] < 1300, 'elektrik', 'mek', 'Asansör / besleyici / katlama uç sensörleri')
g_('istasyon_kutusu', ds('E_ELEKTRIK'), 'elektrik', 'mek', 'E istasyon panosu (Beckhoff + Siemens + sürücüler + DIN · hazır, arka tavanda)')
g_('hava_hatti', lambda o: kod(o) == 'E/Hava', 'hava', 'kablo', 'Hava (vakum) hattı + rakor')
g_('kablo_guc', lambda o: o['dug'].endswith(('__kablo', '__kablo_guc')), 'guc', 'kablo', 'Güç kabloları (kırmızı)')
g_('kablo_bilgi', lambda o: o['dug'].endswith(('__kablo_sinyal', '__kablo_veri')), 'bilgi', 'kablo', 'Bilgi kabloları (mavi)')
g_('fis_paneli', lambda o: o['dug'].startswith('ELK_ZINCIR'), 'elektrik', 'mek', 'Fiş paneli (Harting + M12 · K tarafı, sol yan)')
for o in sorted(sec(lambda o: EK(o) and o['dug'].startswith('EMNIYET')), key=lambda o: (o['lo'][1], o['lo'][0], o['dug'])):
    tip = 'aktuator' if 'siyah' in o['dug'] else ('braket' if 'paslanmaz' in o['dug'] else 'sensor')
    grup('emniyet_%s_%d_%d' % (tip, round(o['lo'][0]), round(o['lo'][1])), [o], 'koyu' if tip != 'braket' else 'mekanizma', 'mek',
         {'sensor': 'Kapak emniyet sensörü Schmersal RSS36', 'aktuator': 'RST36 aktüatör (kapakta)', 'braket': 'Sensör braketi 2 mm'}[tip], kpk=tip == 'aktuator')
for o in sorted(sec(lambda o: EK(o)), key=lambda o: (o['dug'], o['lo'][0], o['lo'][1], o['lo'][2])):
    d = o['dug']
    grup('%s_%d_%d_%d' % (d.lower().replace('__', '_'), round(o['lo'][0]), round(o['lo'][1]), round(o['lo'][2])), [o], 'mekanizma', 'mek', '%s (E)' % d)

# ---------------------------------------------------------------- 3. çevre (silik)
def cev(ad, f, ac):
    LL = [o for o in L if id(o) not in ATANAN and f(o)]
    if not LL: return
    for o in LL: ATANAN.add(id(o))
    ekle(ad, *birles(LL), 'silik', 'cevre', ac)
cev('cevre_B', lambda o: o['dug'].startswith(('B_', 'CEK_', 'ELK_DOLAP', 'ELK_IC', 'ELK_ISTASYON')) or kod(o).startswith('B/'), 'B dolabı (silik çevre)')
cev('cevre_U', lambda o: o['dug'].startswith(('U_', 'ELK_ANA_PANO', 'D_PIZZA')) or kod(o).startswith('U/'), 'U üst depo (silik çevre)')
cev('cevre_K', lambda o: kod(o).startswith('K/') or o['dug'].startswith('K_'), 'K (silik çevre)')
cev('cevre_diger', lambda o: True, 'Hat (silik çevre)')
kalan = [o for o in L if id(o) not in ATANAN]
print('ATANMAYAN', len(kalan))
pickle.dump(dict(P=P, ENT=ENT), open('e_parca.pkl', 'wb'))
c = collections.Counter(v['tur'] for v in P.values()); print('tür', dict(c))
for a in sorted(P):
    if P[a]['tur'] in ('sac', 'profil', 'mek', 'cevre', 'pu', 'kablo'):
        print('%-46s %-9s %-5s %6d  lo %s hi %s' % (a, P[a]['m'], P[a]['tur'], len(P[a]['F']), np.round(P[a]['V'].min(0)).astype(int).tolist(), np.round(P[a]['V'].max(0)).astype(int).tolist()))
print('TOPLAM', len(P))
