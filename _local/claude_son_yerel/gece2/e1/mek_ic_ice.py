# -*- coding: utf-8 -*-
"""E mekanizma parçaları (zincir 81–85) son konumda İÇ İÇE çiftler → mek_ic_ice.json (sıralama hesabı bu çiftleri engel saymaz; rapora MODEL AÇIĞI)."""
import os, sys, json, pickle, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); os.chdir(HERE); sys.path.insert(0, os.path.join(HERE, '..', 'cekmece'))
import yol_denetim_v2 as Y
P = pickle.load(open('e_parca.pkl', 'rb'))['P']
B = {}
for s_ in 'mnopq': B.update(json.load(open('ent/hat3_v10%s_ent.json' % s_, encoding='utf-8'))['baglanti'])
ads = sorted(a for a in P if P[a].get('mek_ad') or (a in B and B[a].get('yeni') and P[a]['tur'] != 'kaynak'))
Pm = {a: dict(V=np.asarray(P[a]['V']) / 1000.0, F=np.asarray(P[a]['F'])) for a in ads}
S = Y.son_kesisim(Pm, ads, 3e-4)
# yüzeyleri kesişmeyen GÖMÜLÜ çiftler (biri ötekinin içinde: mil / motor mili / kılavuz bloğu deliksiz; köşe çerçevesi ağı açık → hacim ölçülemez).
# Kaynak: sökerek sıralama (6 Eki) her yönde yalnız bu parçaya çarpan 21 parça. Üreteçte delik / boşluk açılınca listeden çıkar.
GOMULU = [('kose_piston_kol', 'kose_sasi')] + [('kose_kilavuz_%s_%d' % (k, i), 'kose_sasi') for k in ('sag_arka', 'sag_on', 'sol_arka', 'sol_on') for i in (0, 1)] +          [('parmak_kasnak', 'parmak_gobek'), ('piston_somun_blogu', 'piston_somun_braketi'), ('parmak_mafsal_plaka_0', 'parmak_gobek'), ('besleyici_kasnak_mili', 'besleyici_mil_yatagi')] +          [('kose_motor_%s' % k, 'kose_tutucu_%s_gobek' % k) for k in ('sag_arka', 'sag_on', 'sol_arka', 'sol_on')] +          [('kapak_profil_kapak_0', 'kapak_profil_0'), ('kapak_profil_kapak_1', 'kapak_profil_1'), ('kalip_rulman', 'kalip_rulman_blogu'), ('kalip_sensor', 'kalip_sensor_blogu')]
for a, b in GOMULU:
    if (a, b) not in S and (b, a) not in S: S[(a, b) if a < b else (b, a)] = 0                # 0 = gömülü (yüzey kesişimi yok)
json.dump(sorted([[a, b, n] for (a, b), n in S.items()]), open('mek_ic_ice.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print(len(ads), 'parça ·', len(S), 'iç içe çift')
for (a, b), n in sorted(S.items(), key=lambda x: -x[1]): print('  %-34s ↔ %-34s %d' % (a, b, n))
