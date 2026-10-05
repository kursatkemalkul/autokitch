# -*- coding: utf-8 -*-
"""E açınımları GÜNCEL üreteçten (h3_e_sac_v1, adım 8 saplama düzeltmesi dahil — zincir adım 35'in kullandığı sürüm) → e3/acinim_E/*.json
ortam: zincir adım 35 ile aynı (yama_v9/sac_ent: ADIM5 = yama_v9/veri, AUTOKITCH_SAC_STANDART = yama_v9/sac_standart) · ana depoya / GLB'ye YAZMAZ"""
import os, sys, json
H = r'C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH_COORDINATION\worktrees\claude-hat3-v8\arastirma\_uretec\h3'
sys.path.insert(0, os.path.join(H, 'yama_v9')); sys.path.insert(0, H); sys.stdout.reconfigure(encoding='utf-8')
import sac_ent as SE   # ortam değişkenleri
import h3_e_sac_v1 as E
g = E.kur(log=print)
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'acinim_E'); os.makedirs(OUT, exist_ok=True)
n = 0
for s in g.SAC:
    a = s.acinim(); json.dump(a, open(os.path.join(OUT, s.ad + '.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1); n += 1
print('açınım', n, 'yazıldı')
