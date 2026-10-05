# -*- coding: utf-8 -*-
"""F montaj v2 · parça çıkarımı: hat3_v10h (zincir 00–66) → f_parca.pkl (mm, dünya)
Adlı parçalar: zincir adımlarının _ent.json kayıtları (36 F üst kabin · 38 kapaklar / atış kanalı / baca · 58 acil stop · 59 emniyet · 60 hava emniyet ·
61 filtre servis) — bileşen kutusu kaydın kutusunun içinde (0,6 mm), birden çok kutuya düşerse EN KÜÇÜK kutu.
Kalan F bileşenleri (hazır ürünler, elektrik, hava): düğüm + mek ile ürün grupları. F dışı her şey silik çevre.
Kullanım: python f_parca.py"""
import sys, os, json, pickle, collections
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
sys.stdout.reconfigure(encoding='utf-8')
BIL = pickle.load(open('f_bil.pkl', 'rb'))
MEK = BIL['MEK']; L = BIL['L']
P = {}
ENTF = [('/home/user/main_wt/_local/claude_son_yerel/gece2/adim5e/is/hat3_v9d_ent.json', lambda a, v: v['dugum'].startswith('F_')),
        ('../t3/is_A/hat3_v9f_ent.json', None),
        ('/home/user/is/z58A/hat3_v9z_ent.json', lambda a, v: 'KAPAK_F' in v['dugum']),
        ('/home/user/is/z59A/hat3_v10a_ent.json', lambda a, v: '_F_' in a),
        ('/home/user/is/z60A/hat3_v10b_ent.json', None),
        ('/home/user/is/z61A/hat3_v10c_ent.json', None),
        ('/home/user/is/z67A/hat3_v10i_ent.json', None)]
ENT = {}
for f_, s_ in ENTF:
    for a, v in json.load(open(f_, encoding='utf-8'))['parca'].items():
        if s_ is None or s_(a, v): ENT[a] = v
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
    if t in ('arayuz',) or any(w in a for w in ('_pem', 'pem_', '_vida', 'vida_', '_percin', 'percin_', '_somun', '_pul', '_saplama', 'arayuz_', 'civata')) \
            or any(w in bom for w in ('cıvata', 'vida', 'PEM', 'perçin', 'somun', 'pul ', 'saplama')):
        return 'baglanti', 'baglanti', bom
    if t == 'profil' or 'omega' in a or 'profil' in a: return 'profil', 'profil', bom
    if t == 'sac' or bom.startswith('Sac') or d.endswith('__sac'): return 'sac', 'sac', bom
    return 'mekanizma', 'mek', bom


# ---------------------------------------------------------------- 1. adlı parçalar (ent kutusu)
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
    m, t, bom = sinif(a, ENT[a]); grup(a, TOPLA[a], m, t, bom, dugum=ENT[a]['dugum'], kpk='KAPAK_F' in ENT[a]['dugum'])
eks = sorted(a for a in ENT if a not in TOPLA)
print('adlı parça', len(TOPLA), '· model karşılığı olmayan kayıt', len(eks), eks[:20])

# ---------------------------------------------------------------- 2. F bileşenleri: hazır ürünler + elektrik + hava (düğüm / mek)
FK = lambda o: kod(o).startswith('F/')
def g_(ad, f, m, tur, ac):
    LL = sec(lambda o: FK(o) and f(o))
    if LL: grup(ad, LL, m, tur, ac)
g_('tp10_firin', lambda o: o['dug'].startswith(('F_TP10', 'F_CIKIS_PLAKA')) or o['dug'].startswith('F_DONER__RULO_TP'), 'alu', 'mek', 'TP10 tünel fırın (konveyör + IR + gövde · hazır ürün, tek parça)')
g_('yukleme_bandi_motor', lambda o: o['dug'] == 'F_YUKLEME_BANDI__motor', 'motor', 'mek', 'Yükleme bandı motoru (redüktörlü · hazır)')
g_('yukleme_bandi', lambda o: o['dug'].startswith(('F_YUKLEME_BANDI', 'F_DONER__RULO_GB')), 'mekanizma', 'mek', 'Yükleme bandı (PTFE bant + rulolar + şase · hazır ürün)')
g_('kompresor', lambda o: o['dug'].startswith(('HAVA_KOMPRESOR', 'F_KOMP_AYAK')), 'motor', 'mek', 'Kompresör + tank + ayaklar (hazır ürün)')
g_('hava_emniyet_valfi', lambda o: o['dug'].startswith('HAVA_EMNIYET'), 'mekanizma', 'mek', 'Festo MS6-SV-E emniyet valfi + bobin + susturucu (adım 60)')
g_('hava_hatti', lambda o: o['dug'].startswith(('HAVA_IC', 'ELK_ZINCIR__hava')) or (o['dug'].startswith('ELK_ZINCIR') and kod(o) == 'F/Hava'), 'hava', 'kablo', 'Hava hattı (hortum + askılar + rakorlar)')
g_('davlumbaz_fan_filtre', lambda o: o['dug'].startswith('F_DAVLUMBAZ') and o['dug'] not in ('F_DAVLUMBAZ__sac',), 'mekanizma', 'mek', 'Davlumbaz: fan + yağ filtresi + çerçeve (hazır ürün)')
g_('acil_stop', lambda o: o['dug'].startswith('ACIL_STOP'), 'elektrik', 'mek', 'Acil stop Schneider XB4BS8442 (sağ kapakta, adım 58)')
for o in sorted(sec(lambda o: FK(o) and o['dug'].startswith('EMNIYET')), key=lambda o: (o['lo'][0], o['dug'])):
    yan = 'sol' if o['lo'][0] < 3250 else 'sag'
    tip = 'aktuator' if 'siyah' in o['dug'] else ('braket' if 'paslanmaz' in o['dug'] else 'sensor')
    grup('emniyet_%s_%s' % (yan, tip), [o], 'koyu' if tip != 'braket' else 'mekanizma', 'mek', {'sensor': 'Kapak emniyet sensörü Schmersal RSS36', 'aktuator': 'RST36 aktüatör (kapakta)', 'braket': 'Sensör braketi 2 mm'}[tip], kpk=tip == 'aktuator')
KAB = ('kablo',)
g_('kablo_guc', lambda o: o['dug'].endswith(('__kablo', '__kablo_guc')), 'guc', 'kablo', 'Güç kabloları (kırmızı)')
g_('kablo_bilgi', lambda o: o['dug'].endswith(('__kablo_sinyal', '__kablo_veri')), 'bilgi', 'kablo', 'Bilgi kabloları (mavi)')
g_('istasyon_kutusu', lambda o: o['dug'].startswith('ELK_ISTASYON') and o['dug'] != 'ELK_ISTASYON__rakor', 'elektrik', 'mek', 'F istasyon kutusu (pano + DIN + cihazlar · hazır)')
g_('fis_paneli_sol', lambda o: o['dug'].startswith('ELK_ZINCIR') and kod(o) == 'F/Elektrik' and (o['lo'][0] + o['hi'][0]) / 2 < 3250, 'elektrik', 'mek', 'Fiş paneli sol (Harting + M12 · TOPPING tarafı)')
g_('fis_paneli_sag', lambda o: o['dug'].startswith('ELK_ZINCIR') and kod(o) == 'F/Elektrik', 'elektrik', 'mek', 'Fiş paneli sağ (Harting + M12 · K tarafı)')
for o in sorted(sec(lambda o: FK(o) and o['dug'].startswith(('ELK_', 'F_UST_KABIN__plastik'))), key=lambda o: (o['lo'][0], o['lo'][1])):
    grup('elk_%s_%d_%d' % (o['dug'].split('__')[-1], round(o['lo'][0]), round(o['lo'][1])), [o], 'kanal' if 'kanal' in o['dug'] else 'elektrik', 'mek', '%s (F iç)' % o['dug'].split('__')[-1])
# F gövde kalan (ent dışı): kapak menteşe gövdesi / gazlı yay / ön şeffaf / ... — kendi bileşenleriyle
for o in sorted(sec(lambda o: FK(o)), key=lambda o: (o['dug'], o['lo'][0], o['lo'][1], o['lo'][2])):
    d = o['dug']; kp = 'KAPAK_F' in d or 'YAY_F' in d
    grup('%s_%d_%d_%d' % (d.lower().replace('__', '_'), round(o['lo'][0]), round(o['lo'][1]), round(o['lo'][2])), [o], 'mekanizma', 'mek', '%s (F)' % d, kpk=kp)

# ---------------------------------------------------------------- 3. çevre (silik)
def cev(ad, f, ac):
    LL = [o for o in L if id(o) not in ATANAN and f(o)]
    if not LL: return
    for o in LL: ATANAN.add(id(o))
    ekle(ad, *birles(LL), 'silik', 'cevre', ac)
cev('cevre_B', lambda o: o['dug'].startswith(('B_', 'CEK_', 'ELK_DOLAP')) or (o['dug'].startswith('ELK_IC') and o['hi'][1] < 800), 'B dolabı (silik çevre)')
cev('cevre_U', lambda o: o['dug'].startswith(('U_', 'ELK_ANA_PANO', 'D_PIZZA')) or kod(o).startswith('U/'), 'U üst depo + ana pano (silik çevre)')
cev('cevre_TOPPING', lambda o: kod(o).startswith('TOPPING/') or o['dug'].startswith(('TOPPING_', 'KAIDE_C')), 'TOPPING (silik çevre)')
cev('cevre_K', lambda o: kod(o).startswith('K/') or o['dug'].startswith('K_'), 'K (silik çevre)')
cev('cevre_diger', lambda o: True, 'Hat (silik çevre)')
kalan = [o for o in L if id(o) not in ATANAN]
print('ATANMAYAN', len(kalan))
pickle.dump(dict(P=P, ENT=ENT), open('f_parca.pkl', 'wb'))
c = collections.Counter(v['tur'] for v in P.values()); print('tür', dict(c))
for a in sorted(P):
    if P[a]['tur'] in ('sac', 'profil', 'mek', 'cevre', 'pu', 'kablo'):
        print('%-46s %-9s %-5s %6d  lo %s hi %s' % (a, P[a]['m'], P[a]['tur'], len(P[a]['F']), np.round(P[a]['V'].min(0)).astype(int).tolist(), np.round(P[a]['V'].max(0)).astype(int).tolist()))
print('TOPLAM', len(P))
