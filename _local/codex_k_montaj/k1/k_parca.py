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
# Legacy names remain provisional; unique same-node bounds within the existing v6 0.6 mm naming tolerance account for polygonal cylinders. No surface equality is implied.
cat={v['name']:v for v in json.loads((ROOT/'_local/codex_k_montaj/legacy_catalog.json').read_text(encoding='utf-8'))}
SOURCE_COMPONENTS=json.loads((ROOT/'_local/codex_k_montaj/source_components.json').read_text(encoding='utf-8'))['components']
for m in json.loads((ROOT/'_local/codex_k_montaj/source_matches.json').read_text(encoding='utf-8')):
    a=m['legacy_name']
    if m.get('bbox_error_mm',99)<=0.6 and a in cat and a not in ENT:
        v=cat[a];matches=[o for o in SOURCE_COMPONENTS if o['node']==m['source_component'].split('[')[0] and np.max(np.abs(np.array(o['lo']+o['hi'])-np.array(v['lo']+v['hi'])))<=0.6]
        if len(matches)!=1: continue
        v=cat[a];lo=v['lo'];hi=v['hi'];ENT[a]={'dugum':m['source_component'].split('[')[0],'kutu':[lo[0],hi[0],lo[1],hi[1],lo[2],hi[2]],'tur':v['type'],'bom':v.get('bom',[]),'provisional_legacy_name':True}
# Current standard washers have smaller OD than the provisional legacy wide-washer catalog.
# Match their actual isolated ring by axis, thickness and centre, never change the geometry.
for a,v in cat.items():
 if a in ENT or not a.endswith('_pul'):continue
 meta=v.get('meta') or {}
 if not meta.get('h'):continue
 lo=np.array(v['lo']);hi=np.array(v['hi']);axis=int(np.argmin(hi-lo));perp=[i for i in range(3) if i!=axis];centre=(lo+hi)/2
 candidates=[o for o in L if o['dug']=='K_GOVDE__celik' and abs((o['hi']-o['lo'])[axis]-meta['h'])<.4 and np.max(np.abs(((o['lo']+o['hi'])/2-centre)[perp]))<.2 and abs(((o['lo']+o['hi'])/2-centre)[axis])<.6]
 if len(candidates)!=1:continue
 o=candidates[0];l=o['lo'];h=o['hi'];ENT[a]={'dugum':o['dug'],'kutu':[l[0],h[0],l[1],h[1],l[2],h[2]],'tur':'baglanti','bom':['Current source washer; geometry from authoritative model'],'current_washer_geometry':True}
ENT.update(json.loads((Path(HERE)/'k_local_ent.json').read_text(encoding='utf-8'))['parca'])
# Native source provides purchased/mechanical names only; the latest mesh remains authoritative.
for v in json.loads((Path(HERE)/'native_mechanism_names.json').read_text(encoding='utf-8')):
 if v['name'] in ENT:continue
 lo=np.array(v['lo']);hi=np.array(v['hi'])
 candidates=[o for o in L if o['dug'].startswith('K_') and not o['dug'].startswith('K_GOVDE') and o['dug'].split('__')[1:2]==[v['material']] and np.all(o['lo']>=lo-.6) and np.all(o['hi']<=hi+.6)]
 nodes=set(o['dug'] for o in candidates)
 if len(nodes)!=1:
  # Connected components can contain touching native parts. Find a unique node whose triangle-level bounds match the native record on all six faces.
  pieces=collections.defaultdict(list)
  for o in L:
   if not o['dug'].startswith('K_') or o['dug'].startswith('K_GOVDE') or o['dug'].split('__')[1:2]!=[v['material']]:continue
   if np.any(o['hi']<lo-.6) or np.any(o['lo']>hi+.6):continue
   q=o['V'][o['F']];m=np.all(q.min(1)>=lo-.6,1)&np.all(q.max(1)<=hi+.6,1)
   if m.any():pieces[o['dug']].append(q[m].reshape(-1,3))
  nodes=set()
  for node,qs in pieces.items():
   q=np.vstack(qs)
   if np.max(np.abs(q.min(0)-lo))<=.6 and np.max(np.abs(q.max(0)-hi))<=.6:nodes.add(node)
 if len(nodes)!=1:continue
 ENT[v['name']]={'dugum':nodes.pop(),'kutu':[lo[0],hi[0],lo[1],hi[1],lo[2],hi[2]],'bom':v.get('bom'),'source_group':v['group'],'native_metadata_only':True}
# Two touching surfaces form one GLB component: separate supplier body from our mounting plate by their native records.
for v in json.loads((Path(HERE)/'native_mechanism_names.json').read_text(encoding='utf-8')):
 if v['name'] not in ('DGRF_baglanti_plakasi','DGRF-C-63-125_govde'):continue
 lo=np.array(v['lo']);hi=np.array(v['hi']);node='K_KESICI__aluminyum'
 candidates=[o for o in L if o['dug']==node and np.all(o['hi']>=lo) and np.all(o['lo']<=hi)]
 assert candidates,v['name']
 ENT[v['name']]={'dugum':node,'kutu':[lo[0],hi[0],lo[1],hi[1],lo[2],hi[2]],'bom':v['bom'],'native_metadata_only':True}

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
    if d=='ELK_ZINCIR__hava' or 'hortum' in a or a.startswith(('bant_PU_', 'bant_sarim_')): return 'kablo', 'kablo', bom or 'Flexible hose or belt installed along its route (KURALLAR 2.3/9)'
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
    # Split touching sheets even when their whole component fits a larger parent sheet box.
    # The smallest containing record is selected per triangle below.
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
    d=o['dug'];tip='kablo' if d=='ELK_ZINCIR__hava' or any(w in d for w in ('kablo','hortum','pu_bant')) else 'mek'
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
from k_yuz_etiket import apply as apply_verified_surface_names
P=apply_verified_surface_names(P)
pickle.dump(dict(P=P, ENT=ENT), open('k_parca.pkl', 'wb'))
c = collections.Counter(v['tur'] for v in P.values()); print('tür', dict(c))
for a in sorted(P):
    if P[a]['tur'] in ('sac', 'profil', 'mek', 'cevre', 'pu', 'kablo'):
        print('%-46s %-9s %-5s %6d  lo %s hi %s' % (a, P[a]['m'], P[a]['tur'], len(P[a]['F']), np.round(P[a]['V'].min(0)).astype(int).tolist(), np.round(P[a]['V'].max(0)).astype(int).tolist()))
print('TOPLAM', len(P))

original=INPUT_TRIANGLES; assigned=sum(len(v["F"]) for v in P.values()); assert original==assigned,(original,assigned)
json.dump({"input_triangles":original,"assigned_triangles":assigned,"parts":len(P),"unassigned":len(kalan),"provisional_names":[a for a,v in ENT.items() if v.get("provisional_legacy_name")]},open("part_audit.json","w"),ensure_ascii=False,indent=2)
