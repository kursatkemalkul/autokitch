# -*- coding: utf-8 -*-
"""A montaj v3 · parça çıkarımı: hat3_v9l_A.glb (= hat3_v9l + zincir_A_tamamla.py) → a3_parca.pkl (mm, dünya)
A gövdesi: adım-33 ent aralıkları (hat3_v9a_ent.json · v9l'de geçerli, 326/326 kutu farkı 0) + zincirin eklediği 4 pul (primitif sonu).
Açıcı (A/Açıcı mek, satın alınan TEK ÜRÜN) + silik çevre (B üst bölgesi, TOPPING sol duvarı + tabla rayı tabanı) cevre_bil.pkl'den (v9l, değişmeyen düğümler)."""
import sys, os, json, pickle
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
sys.path.insert(0, os.path.join(HERE, '..', 'cekmece')); sys.stdout.reconfigure(encoding='utf-8')
from glb import G
g = G(os.path.join(HERE, 'hat3_v9l_A.glb'))
ENT = json.load(open(os.path.join(HERE, '..', 'adim8', 'is_tam', 'hat3_v9a_ent.json'), encoding='utf-8'))['parca']
P = {}


def ekle(ad, V, F, m, tur, ac, **k):
    V = np.asarray(V, float); F = np.asarray(F, np.int64)
    u, inv = np.unique(np.round(V, 4), axis=0, return_inverse=True)
    P[ad] = dict(V=u, F=inv.reshape(-1)[F], m=m, tur=tur, ac=ac, **k)


NT = {}
def node_tri(d):
    if d not in NT: NT[d] = g.tris(g.byname[d])[0][:2]
    return NT[d]


for a, v in ENT.items():
    X, T = node_tri(v['dugum']); s, n = v['indis']; Tt = T[s // 3:(s + n) // 3]
    u, inv = np.unique(Tt.reshape(-1), return_inverse=True)
    bom = (v.get('bom') or [''])[0]
    t = v['tur']
    if t == 'sac': m = 'kapak' if v['kpk'] else 'sac'
    elif t == 'profil': m = 'profil'
    elif t == 'kaynak': m = 'kaynak'
    elif t == 'arayuz': m = 'arayuz'; t = 'baglanti'
    elif 'tapa' in a or 'basac' in a: m = 'koyu'
    else: m = 'baglanti'
    ekle(a, X[u], inv.reshape(-1, 3), m, t, bom, dugum=v['dugum'], kpk=v['kpk'])
# zincir_A_tamamla eklentisi: 4 × DIN 125 pul (A_GOVDE__paslanmaz primitifinin son 1024 üçgeni)
X, T = node_tri('A_GOVDE__paslanmaz')
ent_son = max(v['indis'][0] + v['indis'][1] for v in ENT.values() if v['dugum'] == 'A_GOVDE__paslanmaz') // 3
Te = T[ent_son:]
Ce = X[Te].mean(1)
for i, (x, z) in enumerate([(305.0, -645.0), (395.0, -645.0), (305.0, -520.0), (395.0, -520.0)]):
    m = np.hypot(Ce[:, 0] - (x + 736), Ce[:, 2] - z) < 9.0
    Tt = Te[m]; u, inv = np.unique(Tt.reshape(-1), return_inverse=True)
    V = X[u]; c = (V.min(0) + V.max(0)) / 2
    assert abs(c[0] - (x + 736)) < 0.05 and abs(c[2] - z) < 0.05 and abs(c[1] - 902.8) < 0.05, (c, x, z)
    ekle('arayuz_acici_kolonu_M8_%d_%d_pul' % (x, -z), V, inv.reshape(-1, 3), 'arayuz', 'baglanti', 'DIN 125-1 M8 pul (8,4 / 16 × 1,6) · zincir_A_tamamla A2')
assert sum(len(P[a]['F']) for a in P if a.endswith('_pul') and a.startswith('arayuz_acici')) == len(Te)
print('A gövdesi', len(P))

# ---------------------------------------------------------------- açıcı + çevre
C = pickle.load(open('cevre_bil.pkl', 'rb'))
def birles(L):
    VV, FF, n = [], [], 0
    for o in L: VV.append(o['V']); FF.append(np.asarray(o['F']) + n); n += len(o['V'])
    return np.vstack(VV), np.vstack(FF)
ac = [o for o in C if o['mek'] == 1]
ekle('acici', *birles([o for o in ac if o['dug'] != 'TOPPING_MODUL__sac']), 'mekanizma', 'mek', 'Açıcı (dönme kafası + motor · satın alınan TEK ÜRÜN, kolonla birlikte)')
ekle('acici_kolon', *birles([o for o in ac if o['dug'] == 'TOPPING_MODUL__sac']), 'mekanizma', 'mek', 'Açıcı kolonu + taban flanşı (aynı ürün · denetim için ayrı ağ)')
print('açıcı bileşen', len(ac), len(P['acici']['F']), len(P['acici_kolon']['F']))
# B (silik, baştan): dış kabuk sacları + üst kiriş + GFRP pedler + perçin somunlar (A tabanı altında)
B_ = [o for o in C if o['dug'] in ('B_KASA__sac', 'B_KASA__on_cerceve')]
ekle('cevre_B_kabuk', *birles(B_), 'silik', 'cevre', 'B dolabı (silik çevre)')
ekle('cevre_B_kiris', *birles([o for o in C if o['dug'] == 'B_MODULER__paslanmaz']), 'silik', 'cevre', 'B üst kirişleri (silik)')
ekle('cevre_B_gfrp', *birles([o for o in C if o['dug'] == 'B_MODULER__gfrp']), 'silik', 'cevre', 'B GFRP pedleri (silik)')
ekle('cevre_B_percin', *birles([o for o in C if o['dug'] == 'B_MODULER__baglanti']), 'silik', 'cevre', 'B üst kiriş M8 perçin somunları (silik)')
# TOPPING (silik, hat bağlantısı adımında): sol duvar kabuğu + iç sac + PEM / köpük kapağı + kaide C + tabla rayı tabanı
T_ = [o for o in C if o['dug'] in ('TOPPING_GOVDE__kabuk', 'TOPPING_GOVDE__sac', 'TOPPING_GOVDE__cerceve', 'KAIDE_C__paslanmaz')]
ekle('cevre_T_govde', *birles(T_), 'silik', 'cevre', 'TOPPING gövdesi (silik çevre)')
ekle('cevre_T_pem', *birles([o for o in C if o['dug'] in ('TOPPING_GOVDE__paslanmaz', 'TOPPING_GOVDE__conta')]), 'silik', 'cevre', 'TOPPING sol dış sacındaki PEM SP-M8 + köpük kapağı (silik)')
ekle('cevre_T_ray', *birles([o for o in C if o['dug'] == 'TOPPING_MODUL__sac' and o['mek'] == 8]), 'silik', 'cevre', 'TOPPING tabla rayı taban sacı (TOPPING ile gelir · silik)')
for a in [a for a in P if a.startswith('cevre')]: print('%-16s %6d  lo %s hi %s' % (a, len(P[a]['F']), np.round(P[a]['V'].min(0)), np.round(P[a]['V'].max(0))))
pickle.dump(dict(P=P, ENT=ENT), open('a3_parca.pkl', 'wb'))
print('TOPLAM', len(P))
