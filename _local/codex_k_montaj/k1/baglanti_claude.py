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
D = pickle.load(open('plan_k_clip_full.pkl', 'rb'))
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
# v6 · grup düzeyi + kategori: bağlantı elemanı değmeyen parça neden öyle (bilerek) ya da AÇIK
KAT = [  # (sınama, kategori, açıklama) — sıra önemli, ilk tutan
    # E (6 Eki): bas-aç geçme · modül iç parçaları · çöp kovası
    (lambda a: 'basac' in a and not a.endswith('lamasi'), 'GECME', 'bas-aç mandalı: dikme / lama deliğine yaylı tırnakla geçer (kendi gövdesi)'),
    (lambda a: a in ('besleyici_vakum', 'kose_kaldirici', 'kose_piston', 'kose_tutucu', 'parmak', 'parmak_y', 'kapak_katlayici'), 'UNITE',
     'tezgâhta kurulan E mekanizma modülünün iç parçası (üst / alt modül, mekanizma üreteci); modül bütün olarak askı / yan saplamalarına bağlanır'),
    (lambda a: a == 'robot_copu', 'SOKULUR', 'robot çöpü kovası + poşet tabandaki kılavuzda oturur, boşaltmak için elle çıkar (bilerek)'),
    (lambda a: a in ('kaset_kasar', 'kaset_sucuk'), 'SOKULUR', 'kaset: dil kanalında + kapak K2 POM takozu kilitler (adım 63) · iki günde bir sökülür'),
    (lambda a: a.endswith('_conta') and a.startswith('kaset_'), 'ACIK', 'kovan contası raf deliğinde değmiyor (kovan iç duvarına 3 mm · v5ten) → conta biçimi düzeltilecek'),
    (lambda a: a.endswith('_raf_conta') or a.endswith('_mandal') or a.startswith(('burc_', 'basac_')), 'GECME', 'sıkı geçme / kendi yaylı tırnağı (conta, POM burç, bas-aç, kaset mandalı)'),
    (lambda a: a.startswith('elk_rakor_1689'), 'GECME', 'kablo rakoru kendi somunuyla tabana (tezgâhta)'),
    (lambda a: a.endswith(('_kelepce', '_raf_flans', '_dirsek', '_cikis')) or a.startswith('hava_kanal_'), 'BORU', 'boru / hortum bağlantı parçası: kelepçe, flanş, dirsek, çıkış ağzı (boruyla birlikte tutulur)'),
    (lambda a: a == 'x_motor' or a.startswith(('elk_koyu_', 'evaporator_', 'sogutma_parca_')), 'UNITE', 'hazır ünitenin parçası: X motoru ünitenin kendi braketine · motor sensörleri motorda · evaporatör ayakları + soğutma grubu'),
    (lambda a: a == 'uno_kiyma_arka', 'ACIK', 'kıyma silindirinin halka flanşı evaporatör cebinde → üretici çizimi gerek'),
    (lambda a: a.startswith(('elk_celik_', 'elk_kanal_', 'elk_rakor_')), 'ACIK', 'iç elektrik kanalı / çelik braket / rakor 1–10 mm havada → kuyruk 10 elektrik işi'),
]
for a, v in out.items():
    if v['sinif'] != 'BAGLANTISIZ': continue
    for f_, k_, n_ in KAT:
        if f_(a): v['kategori'], v['neden'] = k_, n_; break
    else:
        # grup: aynı hareketle gelen ve bağlanan bir parçaya değiyorsa tezgâh grubuyla bağlı
        es = [b for b in TAS if b != a and IMZA[b] == IMZA[a] and HAR[a] and out.get(b, {}).get('sinif') in ('HEMEN', 'GECICI') and degiyor(a, b)]
        v['kategori'], v['neden'] = ('GRUP', 'tezgâh grubunda bağlı parçaya değiyor: %s' % es[:3]) if es else ('ACIK', 'bağlantı elemanı yok · kategori yok')
json.dump(out, open('baglanti_claude.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1, default=float)
from collections import Counter
print(Counter(v['sinif'] for v in out.values()))
for a, v in sorted(out.items(), key=lambda kv: kv[1]['gelis']):
    if v['sinif'] == 'GECICI':
        print('GEÇİCİ  %-40s geliş adım %2d (%s) → bağlanma adım %2d (%s) · %s ↔ %s · arada değen: %s' % (
            a, v['adim'], ADAD[v['adim']], v['bag_adim'], ADAD[v['bag_adim']], v['neyle'][0], v['neyle'][1], v['ustune']))
for a, v in sorted(out.items(), key=lambda kv: kv[1]['gelis']):
    if v['sinif'] == 'BAGLANTISIZ':
        print('BAĞSIZ  %-8s %-34s adım %2d · %s' % (v['kategori'], a, v['adim'], v['neden']))
print('KATEGORİ', Counter(v.get('kategori') for v in out.values() if v['sinif'] == 'BAGLANTISIZ'))
