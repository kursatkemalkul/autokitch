# -*- coding: utf-8 -*-
"""k_baglanti_plan.json → arastirma/_uretec/h3/yama_v9/veri/86_k_baglanti.json (zincir adımı 86'nın girdisi)"""
import json, pickle, os
import numpy as np
P = pickle.load(open('plan_k_clip_full.pkl', 'rb'))['P']
J = json.load(open('k_baglanti_plan.json', encoding='utf-8'))
def kutu(a): return dict(dugum=P[a]['dugum'], lo=P[a]['V'].min(0).round(3).tolist(), hi=P[a]['V'].max(0).round(3).tolist())
out = dict(tasi={a: dict(kutu(a), v=v) for a, v in J['tasi'].items()}, sil={a: kutu(a) for a in J['sil']},
           eleman=[e for a in sorted(J['sonuc']) for e in J['sonuc'][a].get('eleman', [])],
           beyan={a: dict(yontem=v['yontem'], neden=v['neden'], karsi=v.get('karsi')) for a, v in J['sonuc'].items() if v['yontem'].startswith('BEYAN')},
           yontem={a: dict(yontem=v['yontem'], neden=v['neden']) for a, v in J['sonuc'].items()})
hedef = os.path.join('..', '..', '..', 'arastirma', '_uretec', 'h3', 'yama_v9', 'veri', '86_k_baglanti.json')
json.dump(out, open(hedef, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print('eleman', len(out['eleman']), 'taşı', len(out['tasi']), 'sil', len(out['sil']), 'beyan', len(out['beyan']), '→', os.path.normpath(hedef))
