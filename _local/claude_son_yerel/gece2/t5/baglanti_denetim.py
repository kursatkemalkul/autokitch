# -*- coding: utf-8 -*-
"""TOPPING v5 · BAĞLI MI denetimi (5 Eki 2026 · Kemal: "parça geliyor dik duruyor, vidası yok, üstüne başka parça konuyor").
Yalnız analiz: plan_t5.pkl okunur, model / animasyon değişmez.
Her taşıyıcı parça (sac, profil, mek, kapak, pu) için:
  geliş  = parçanın son hareketinin bittiği an
  bağlanma = ona DEĞEN (≤ 0,6 mm) ve aynı anda BAŞKA bir parçaya da değen ilk bağlantı elemanının (vida / somun / PEM / perçin / kaynak / yapıştırıcı)
             ve o karşı parçanın ikisinin de yerinde olduğu an
Sınıf: HEMEN (aynı adım) · GEÇİCİ DAYALI (sonraki adımda bağlanıyor; arada üstüne/yanına konan parçalar listelenir) ·
       BAĞLANTISIZ (hiç bağlantı elemanı değmiyor: tezgâhta gelen grubun içinde mi, yoksa yalnız dayanıyor mu).
Çıktı: baglanti_denetim.json + ekrana özet."""
import os, sys, json, pickle
import numpy as np
import trimesh
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE)
D = pickle.load(open('plan_t5.pkl', 'rb'))
P, HAR, GOR, MF, ADIM = D['P'], D['HAR'], D['GOR'], D['MF'], D['ADIM']
CEV = set(D['CEVRE'])
TOL = 0.6
TASIYICI = ('sac', 'profil', 'mek', 'kapak', 'pu')
def baglayici(a):
    t = P[a]['tur']
    if t in ('baglanti', 'kaynak'): return True
    return t == 'silikon' and 'yapistir' in a
ADS = [a for a in P if a in GOR and a not in CEV]
def son(a):
    s = [GOR[a]] + [h[1] for h in HAR[a]]
    if a in MF and MF[a].get('buyu'): s.append(MF[a]['buyu'][1])
    return max(s)
SON = {a: son(a) for a in ADS}
IMZA = {a: json.dumps(HAR[a]) for a in ADS}
def V(a): return np.asarray(P[a].get('Vm', P[a]['V']), float)
def F(a): return np.asarray(P[a].get('Fm', P[a]['F']))
LO = {a: V(a).min(0) for a in ADS}; HI = {a: V(a).max(0) for a in ADS}
TM = {}
def tm(a):
    if a not in TM: TM[a] = trimesh.Trimesh(V(a), F(a), process=False)
    return TM[a]
def degiyor(x, y):
    if np.any(LO[x] > HI[y] + TOL) or np.any(HI[x] < LO[y] - TOL): return False
    for p, q in ((x, y), (y, x)):
        Q = V(p); m = np.all(Q >= LO[q] - TOL, 1) & np.all(Q <= HI[q] + TOL, 1)
        if m.any():
            Q = Q[m]
            if len(Q) > 4000: Q = Q[np.linspace(0, len(Q) - 1, 4000).astype(int)]
            _, d, _ = trimesh.proximity.closest_point(tm(q), Q)
            if d.min() <= TOL: return True
    return False
def adim_no(t):
    n = 1
    for s in ADIM:
        if s['t0'] <= t + 1e-6: n = s['no']
    return n
ADAD = {s['no']: s['ad'] for s in ADIM}
TAS = [a for a in ADS if P[a]['tur'] in TASIYICI]
BAG = [a for a in ADS if baglayici(a)]
# bağlayıcı → değdiği taşıyıcılar
DEG = {}
for i, f in enumerate(BAG):
    DEG[f] = [a for a in TAS if degiyor(f, a)]
    if i % 50 == 0: print('bağlayıcı %d/%d' % (i, len(BAG)), flush=True)
# taşıyıcı ↔ taşıyıcı temas (üstüne konan parçalar için)
out = {}
for a in TAS:
    g = SON[a]; en = None; neyle = None
    for f in BAG:
        if a not in DEG[f]: continue
        for b in DEG[f]:
            if b == a: continue
            t = max(SON[f], SON[b], g)
            if en is None or t < en: en, neyle = t, (f, b)
    if en is None:
        # aynı hareket grubunda gelen ve bağlanan bir parçaya değiyor mu (tezgâh grubu)
        grup = [b for b in TAS if b != a and IMZA[b] == IMZA[a] and HAR[a]]
        out[a] = dict(sinif='BAGLANTISIZ', gelis=g, adim=adim_no(g), grup=len(grup) > 0)
        continue
    ag, ab = adim_no(g), adim_no(en)
    if ab == ag:
        out[a] = dict(sinif='HEMEN', gelis=g, bag=en, adim=ag, neyle=neyle)
        continue
    ustune = [b for b in TAS if b != a and g < SON[b] < en and IMZA[b] != IMZA[a] and degiyor(a, b)]
    out[a] = dict(sinif='GECICI', gelis=g, bag=en, adim=ag, bag_adim=ab, neyle=neyle, ustune=ustune)
json.dump(out, open('baglanti_denetim.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1, default=float)
from collections import Counter
print(Counter(v['sinif'] for v in out.values()))
for a, v in sorted(out.items(), key=lambda kv: kv[1]['gelis']):
    if v['sinif'] == 'GECICI':
        print('GEÇİCİ  %-40s geliş adım %2d (%s) → bağlanma adım %2d (%s) · %s ↔ %s · arada değen: %s' % (
            a, v['adim'], ADAD[v['adim']], v['bag_adim'], ADAD[v['bag_adim']], v['neyle'][0], v['neyle'][1], v['ustune']))
for a, v in sorted(out.items(), key=lambda kv: kv[1]['gelis']):
    if v['sinif'] == 'BAGLANTISIZ':
        print('BAĞSIZ  %-40s %-6s adım %2d (%s) grup:%s' % (a, P[a]['tur'], v['adim'], ADAD[v['adim']], v['grup']))
