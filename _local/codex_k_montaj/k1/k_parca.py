# -*- coding: utf-8 -*-
"""F montaj v2 · parça çıkarımı: hat3_v10h (zincir 00–66) → f_parca.pkl (mm, dünya)
Adlı parçalar: zincir adımlarının _ent.json kayıtları (36 F üst kabin · 38 kapaklar / atış kanalı / baca · 58 acil stop · 59 emniyet · 60 hava emniyet ·
61 filtre servis) — bileşen kutusu kaydın kutusunun içinde (0,6 mm), birden çok kutuya düşerse EN KÜÇÜK kutu.
Kalan F bileşenleri (hazır ürünler, elektrik, hava): düğüm + mek ile ürün grupları. F dışı her şey silik çevre.
Kullanım: python f_parca.py"""
from pathlib import Path
import sys, os, json, pickle, collections
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
sys.stdout.reconfigure(encoding='utf-8')
BIL = pickle.load(open('k_bil.pkl', 'rb'))
MEK = BIL['MEK']; L = BIL['L']
INPUT_TRIANGLES=sum(len(o['F']) for o in L)
P = {}
ROOT=Path(HERE).parents[2]
ENT={}
for f_ in sorted((ROOT/'_local/claude_son_yerel/gece2').rglob('*_ent.json')):
    data=json.loads(f_.read_text(encoding='utf-8-sig'))
    for a,v in data.get('parca',{}).items():
        if isinstance(v,dict) and v.get('dugum','').startswith(('K_','KAPAK_K','ELK_K')) and 'kutu' in v: ENT[a]=v
# Legacy CAD names are provisional and only used when an exact source component box matched.
cat={v['name']:v for v in json.loads((ROOT/'_local/codex_k_montaj/legacy_catalog.json').read_text(encoding='utf-8'))}
for m in json.loads((ROOT/'_local/codex_k_montaj/source_matches.json').read_text(encoding='utf-8')):
    a=m['legacy_name']
    if m.get('bbox_unique_match') and m.get('bbox_error_mm',99)<0.01 and a in cat and a not in ENT:
        v=cat[a];lo=v['lo'];hi=v['hi'];ENT[a]={'dugum':m['source_component'].split('[')[0],'kutu':[lo[0],hi[0],lo[1],hi[1],lo[2],hi[2]],'tur':v['type'],'bom':v.get('bom',[]),'provisional_legacy_name':True}
ENT.update(json.loads((Path(HERE)/'k_local_ent.json').read_text(encoding='utf-8'))['parca'])
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
    m, t, bom = sinif(a, ENT[a]); grup(a, TOPLA[a], m, t, bom, dugum=ENT[a]['dugum'], kpk='KAPAK_K' in ENT[a]['dugum'])
eks = sorted(a for a in ENT if a not in TOPLA)
print('adlı parça', len(TOPLA), '· model karşılığı olmayan kayıt', len(eks), eks[:20])

# Purchased components stay separate from custom supporting brackets.
FK=lambda o:kod(o).startswith('K/')
for o in sorted(sec(FK),key=lambda o:(o['dug'],*o['lo'])):
    d=o['dug'];tip='kablo' if any(w in d for w in ('kablo','hortum')) else 'mek'
    mal='guc' if 'kablo_guc' in d else 'bilgi' if 'kablo' in d else 'motor' if 'motor' in d else 'mekanizma'
    ad=d.lower().replace('__','_')+'_'+str(sum(1 for a in P if a.startswith(d.lower().replace('__','_'))))
    grup(ad,[o],mal,tip,d+' · K',dugum=d,kpk='KAPAK_K' in d)
# ---------------------------------------------------------------- 3. çevre (silik)
def cev(ad, f, ac):
    LL = [o for o in L if id(o) not in ATANAN and f(o)]
    if not LL: return
    for o in LL: ATANAN.add(id(o))
    ekle(ad, *birles(LL), 'silik', 'cevre', ac)
cev('cevre_B', lambda o: o['dug'].startswith(('B_', 'CEK_', 'ELK_DOLAP')) or (o['dug'].startswith('ELK_IC') and o['hi'][1] < 800), 'B dolabı (silik çevre)')
cev('cevre_U', lambda o: o['dug'].startswith(('U_', 'ELK_ANA_PANO', 'D_PIZZA')) or kod(o).startswith('U/'), 'U üst depo + ana pano (silik çevre)')
cev('cevre_TOPPING', lambda o: kod(o).startswith('TOPPING/') or o['dug'].startswith(('TOPPING_', 'KAIDE_C')), 'TOPPING (silik çevre)')
cev('cevre_F', lambda o: kod(o).startswith('F/') or o['dug'].startswith('F_'), 'F (silik çevre)')
cev('cevre_diger', lambda o: True, 'Hat (silik çevre)')
kalan = [o for o in L if id(o) not in ATANAN]
print('ATANMAYAN', len(kalan))
pickle.dump(dict(P=P, ENT=ENT), open('k_parca.pkl', 'wb'))
c = collections.Counter(v['tur'] for v in P.values()); print('tür', dict(c))
for a in sorted(P):
    if P[a]['tur'] in ('sac', 'profil', 'mek', 'cevre', 'pu', 'kablo'):
        print('%-46s %-9s %-5s %6d  lo %s hi %s' % (a, P[a]['m'], P[a]['tur'], len(P[a]['F']), np.round(P[a]['V'].min(0)).astype(int).tolist(), np.round(P[a]['V'].max(0)).astype(int).tolist()))
print('TOPLAM', len(P))

original=INPUT_TRIANGLES; assigned=sum(len(v["F"]) for v in P.values()); assert original==assigned,(original,assigned)
json.dump({"input_triangles":original,"assigned_triangles":assigned,"parts":len(P),"unassigned":len(kalan),"provisional_names":[a for a,v in ENT.items() if v.get("provisional_legacy_name")]},open("part_audit.json","w"),ensure_ascii=False,indent=2)
