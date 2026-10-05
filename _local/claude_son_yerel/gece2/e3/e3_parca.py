# -*- coding: utf-8 -*-
"""E (KUTU KATLAMA) montaj v3 · parça çıkarımı: hat3_v9s (zincir 00–51) [+ zincir_E_tamamla] → e3_parca.pkl (mm, dünya, tam düğüm dönüşümü)
Gövde (E_GOVDE__*, E_MODULER__paslanmaz): adım-35 ent adları (hat3_v9c_ent.json) — __sac / E_MODULER indis aralıklarıyla (v9s'de geçerli),
  __celik / __kabuk / __plastik / __on_seffaf bileşen kutusuyla (birebir; __on_seffaf indis sırası adım 45'te değişti).
Mekanizmalar (E/Şarjör … E/Hava): e_bil.pkl bileşenleri → modül (alt montaj) + satın alınan ürün (motor, sensör, kayış, vakum, pano cihazı, fiş) ayrımı."""
import sys, os, json, pickle, re, collections
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
sys.path.insert(0, os.path.join(HERE, '..', 'cekmece')); sys.stdout.reconfigure(encoding='utf-8')
from glb import G
GLB = sys.argv[1] if len(sys.argv) > 1 else 'hat3_v9s_E.glb'
BIL = sys.argv[2] if len(sys.argv) > 2 else 'e_bil_E.pkl'
g = G(GLB)
ENT = json.load(open(os.path.join(HERE, '..', 'adim8', 'is_tam', 'hat3_v9c_ent.json'), encoding='utf-8'))['parca']
ZR = json.load(open('zincir_E_rapor.json', encoding='utf-8')) if os.path.exists('zincir_E_rapor.json') else dict(eklenen=[], eklenmedi=[])
EKK = []
for k in ZR['eklenen']:
    for t_ in ('pul', 'somun'): EKK.append((k['ad'] + '_z' + t_, np.array(k[t_ + '_kutu'][:3]), np.array(k[t_ + '_kutu'][3:])))
BB = pickle.load(open(BIL, 'rb'))['E']
P = {}


def ekle(ad, V, F, m, tur, ac, **k):
    V = np.asarray(V, float); F = np.asarray(F, np.int64)
    u, inv = np.unique(np.round(V, 4), axis=0, return_inverse=True)
    P[ad] = dict(V=u, F=inv.reshape(-1)[F], m=m, tur=tur, ac=ac, **k)


def birles(L):
    VV, FF, n = [], [], 0
    for V, F in L: VV.append(V); FF.append(np.asarray(F) + n); n += len(V)
    return np.vstack(VV), np.vstack(FF)


def kut(k): return np.array(k[0::2], float), np.array(k[1::2], float)


# ---------------------------------------------------------------- 1. gövde
ARALIK = ('E_GOVDE__sac', 'E_MODULER__paslanmaz')
NT = {}
def node_tri(d):
    if d not in NT: NT[d] = g.tris(g.byname[d])[0][:2]
    return NT[d]


GOV = {}
for a, v in ENT.items():
    if v['dugum'] in ARALIK:
        X, T = node_tri(v['dugum']); s, n = v['indis']; Tt = T[s // 3:(s + n) // 3]
        u, inv = np.unique(Tt.reshape(-1), return_inverse=True); V = X[u]
        lo, hi = kut(v['kutu']); assert np.abs(V.min(0) - lo).max() < 0.06 and np.abs(V.max(0) - hi).max() < 0.06, a
        GOV[a] = (V, inv.reshape(-1, 3))
for dug in sorted(set(v['dugum'] for v in ENT.values()) - set(ARALIK)):
    C = [o for o in BB if o['dug'] == dug]; kul = set()
    for a, v in ENT.items():
        if v['dugum'] != dug: continue
        lo, hi = kut(v['kutu'])
        c = [i for i, b in enumerate(C) if i not in kul and np.all(np.abs(b['lo'] - lo) < 0.35) and np.all(np.abs(b['hi'] - hi) < 0.35)]
        if len(c) != 1: print('  EŞLEŞMEDİ', dug, a, len(c)); continue
        kul.add(c[0]); GOV[a] = (C[c[0]]['V'], C[c[0]]['F'])
    for i, b in enumerate(C):
        if i not in kul:
            nm = next((n_ for n_, l_, h_ in EKK if np.abs(b['lo'] - l_).max() < 0.05 and np.abs(b['hi'] - h_).max() < 0.05), None)
            if nm: GOV[nm] = (b['V'], b['F']); print('  zincir_E_tamamla eklentisi', nm)
            else: print('  ATANMAYAN', dug, np.round(b['lo'], 1), np.round(b['hi'], 1))
BOM = {a: (v.get('bom') or [None])[0] for a, v in ENT.items()}


def sinif(a):
    v = ENT.get(a); t = v['tur'] if v else 'baglanti'; dug = v['dugum'] if v else 'E_GOVDE__celik'
    if a.startswith('arayuz_uke'): return None
    if a.endswith('_zpul'): return 'baglanti', 'baglanti', 'pul'
    if a.endswith('_zsomun'): return 'baglanti', 'baglanti', 'somun'
    if t == 'sac': return ('kapak' if dug == 'E_GOVDE__on_seffaf' else 'sac'), 'sac', None
    if t == 'profil': return 'profil', 'profil', None
    if t == 'kaynak': return 'kaynak', 'kaynak', None
    if re.match(r'ayak_\d+$', a): return 'mekanizma', 'mek', None
    if a.endswith('_kontra'): return 'baglanti', 'baglanti', 'somun'
    if 'basac' in a: return 'koyu', 'mek', None
    if re.search(r'mentese_(sol|sag)_\d+_(sabit|kanat)$', a) or re.match(r'sarjor_yan_kapisi_mentese_\d(_kanat)?$', a): return 'mekanizma', 'mek', None
    if a.endswith('_saplama') or a.startswith(('arayuz_mek', 'arayuz_j3')): return 'baglanti', 'baglanti', 'saplama'
    if a.startswith('govde_pem_m8'): return 'baglanti', 'baglanti', 'pem'
    if a.endswith('_pul'): return 'baglanti', 'baglanti', 'pul'
    if a.endswith('_somun') or re.match(r'kaide_e_somun_', a): return 'baglanti', 'baglanti', 'somun'
    if a.startswith('kaide_e_ayak_somunu'): return 'baglanti', 'baglanti', 'kaynak_somunu'
    if re.search(r'_vida(_[ab])?$', a) or a.startswith('kaide_e_vida_'): return 'baglanti', 'baglanti', 'civata'
    return 'baglanti', 'baglanti', 'diger'


for a, (V, F) in GOV.items():
    s = sinif(a)
    if s is None: continue
    m, tur, et = s
    ekle('g_' + a, V, F, m, tur, a, bom=BOM.get(a) or ({'pul': 'DIN 125-1 M5 pul (zincir_E_tamamla)', 'somun': 'ISO 10511 M5 fiberli somun (zincir_E_tamamla)'}.get(et) if a.endswith(('_zpul', '_zsomun')) else None), etur=et, ek=a.endswith(('_zpul', '_zsomun')))
print('gövde', sum(1 for a in P if a.startswith('g_')), collections.Counter(P[a].get('etur') for a in P))

# ---------------------------------------------------------------- 2. mekanizmalar: modül + satın alınan ürün
MOD = [  # (düğüm deseni, mek kodu, modül anahtarı)
    (r'^E_SARJOR__karton_yigin', None, 'urun_karton'),
    (r'^E_KUTU__', None, 'urun_kutu'),
    (r'^E_SARJOR__(sac|uhmw)$', 'E/Şarjör', 'sarjor'),
    (r'^E_SARJOR__', 'E/Asansör', 'asansor'),
    (r'^E_ELEKTRIK__(aluminyum|sensor)$', 'E/Asansör', 'asansor'),
    (r'^E_BESLEYICI__vakum_kaucuk', 'E/Hava', 'besleyici'),
    (r'^E_BESLEYICI__', 'E/Besleyici', 'besleyici'),
    (r'^E_ELEKTRIK__(aluminyum|sensor)$', 'E/Besleyici', 'besleyici'),
    (r'^E_KALIP__', None, 'kalip'), (r'^E_KAPAK__', None, 'katlayici'), (r'^E_KOPRU__', None, 'kopru'),
    (r'^E_PISTON__', None, 'piston'), (r'^E_PARMAK__', None, 'parmak'), (r'^E_KOSE__', None, 'kose'),
    (r'^E_ELEKTRIK__(aluminyum|sensor)$', 'E/Kutu katlama', 'kopru'),
    (r'^(DUZ_E_OLUK|E_COP)__', None, 'cop'),
    (r'^E_ELEKTRIK__', 'E/Elektrik', 'pano'),
    (r'^ELK_ZINCIR__', None, 'fis'),
]
SATIN = re.compile(r'__(motor|sensor|kayis|vakum_kaucuk|siemens|beckhoff|harting|m12|rakor|kod_\w+|etiket|kablo_\w+|hava|poset|plastik)')
MEKK = {}
for o in BB:
    if o['dug'].startswith(('E_GOVDE__', 'E_MODULER__')): continue
    kod = g.MEK[o['mek']]['kod']; mod = None
    for rx, mk, md in MOD:
        if re.match(rx, o['dug']) and (mk is None or mk == kod): mod = md; break
    assert mod, (o['dug'], kod)
    MEKK.setdefault(mod, []).append(o)
for md, L in sorted(MEKK.items()): print('modül %-11s %3d bileşen · %s' % (md, len(L), dict(collections.Counter(re.sub(r'^[A-Z_]+?__', '', o['dug']) for o in L))))
pickle.dump(dict(P=P, ENT=ENT, MEKK=MEKK), open('e3_parca_ham.pkl', 'wb'))
print('TOPLAM gövde', len(P))
