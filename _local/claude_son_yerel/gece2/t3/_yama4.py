s = open('t3_parca.py', encoding='utf-8').read()
s = s.replace("    if c[2] < -571.0: return 'arka'\n    if c[1] > 2140.5", "    if c[2] < -569.9: return 'arka'\n    if c[1] > 2140.5")
# UNO çıkış: kıyma / kuşbaşı / sos ön grupla birlikte (çıkış başı alt sac deliğinden büyük); harç ayrı kalır (açık)
s = s.replace("    alt = [o for o in U if id(o) not in ATANAN and o['hi'][1] < 1152.5]\n    grup('uno_%s_cikis' % ad, alt,",
              "    alt = [o for o in U if id(o) not in ATANAN and o['hi'][1] < 1152.5] if ad == 'harc' else []\n    if alt: grup('uno_%s_cikis' % ad, alt,")
open('t3_parca.py', 'w', encoding='utf-8').write(s)
s = open('t3_montaj.py', encoding='utf-8').read()
s = s.replace("INIS = dict(lift=(60, 80, 100, 130), yan=())", "INIS = dict(lift=(110, 120, 130, 140), yan=())")
s = s.replace("for ad in ('kiyma', 'kusbasi', 'sos', 'harc'):\n    t = koy('uno_%s_cikis' % ad, ALT,", "for ad in ('harc',):\n    t = koy('uno_%s_cikis' % ad, ALT,")
s = s.replace("""for pu_ in ('pu_levha_sol', 'pu_levha_sag', 'pu_levha_arka', 'yapistirici_arka', 'yapistirici_sol', 'yapistirici_sag', 'pu_levha_tavan', 'yapistirici_tavan'):""",
"""for k_ in ('sol', 'sag', 'arka', 'tavan'):
    HARIC_PLAN.add(('pu_levha_' + k_, 'yapistirici_' + k_)); HARIC_NEDEN[('pu_levha_' + k_, 'yapistirici_' + k_)] = 'levha yapıştırıcı katmanına bastırılır (yüzey teması)'
for pu_ in ('pu_levha_sol', 'pu_levha_sag', 'pu_levha_arka', 'yapistirici_arka', 'yapistirici_sol', 'yapistirici_sag', 'pu_levha_tavan', 'yapistirici_tavan'):""")
# kondenser kanalı tabandan önce, taban yukarıdan
s = s.replace("""t = koy('kuru_bolme_tabani', AD(ARKA9, UST6), 'Kuru bölme tabanı → perdelerin üstüne (punta)', pem=sorted(PEM_SAC['kuru_bolme_tabani']))
t = koy('kondenser_kanali', AD(ARKA9), 'Kondenser kanalı → arkadan, braketi taban saplamalarına')""",
"""t = koy('kondenser_kanali', AD(ARKA9), 'Kondenser kanalı → arkadan, braketi taban saplamalarına')
t = koy('kuru_bolme_tabani', AD(UST6, ARKA9, lift=(300, 500)), 'Kuru bölme tabanı → yukarıdan, perdelerin üstüne (punta)', pem=sorted(PEM_SAC['kuru_bolme_tabani']))""")
open('t3_montaj.py', 'w', encoding='utf-8').write(s)
print('ok')
