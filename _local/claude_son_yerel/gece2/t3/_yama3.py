import re
# ---------------- zincir: PU kesim kutuları (tavan yalnız y > 2140,5; kalan iç dilim sol / sağ yarıya)
s = open('zincir_T_tamamla.py', encoding='utf-8').read()
old = s[s.index("PU_KES = ["):s.index("# yapıştırıcı katmanı")]
new = """PU_KES = [('arka', [((-1e4, -1e4, -1e4), (1e4, 1e4, -571.0))]),
          ('sol', [((-1e4, -1e4, -571.0), (1495.0, 1e4, 1e4)), ((1495.0, -1e4, -571.0), (1968.0, 2140.5, 1e4))]),
          ('sag', [((2441.0, -1e4, -571.0), (1e4, 1e4, 1e4)), ((1968.0, -1e4, -571.0), (2441.0, 2140.5, 1e4))]),
          ('tavan', [((1495.0, 2140.5, -571.0), (2441.0, 1e4, 1e4))])]
"""
s = s.replace(old, new)
s = s.replace("""    for ad, lo, hi in PU_KES:
        L = M ^ _kutu(lo, hi)""", """    for ad, kutular in PU_KES:
        L = M ^ mf.Manifold.batch_boolean([_kutu(lo, hi) for lo, hi in kutular], mf.OpType.Add)""")
open('zincir_T_tamamla.py', 'w', encoding='utf-8').write(s)

# ---------------- parça: sınıflama, kondenser, kaset rayı, UNO çıkış
s = open('t3_parca.py', encoding='utf-8').read()
s = s.replace("""def kutu_ad(c):
    if c[2] < -571.0: return 'arka'
    if c[0] < 1495.0: return 'sol'
    if c[0] > 2441.0: return 'sag'
    return 'tavan'""", """def kutu_ad(c):
    if c[2] < -571.0: return 'arka'
    if c[1] > 2140.5 and 1495.0 < c[0] < 2441.0: return 'tavan'
    return 'sol' if c[0] < 1968.0 else 'sag'""")
s = s.replace("""grup('kondenser_kanali', [o for o in S17 if (o['lo'][0] > 2010 and o['hi'][0] < 2280 and o['dug'] in ('TOPPING_MODUL__koyu', 'TOPPING_MODUL__celik', 'TOPPING_MODUL__sac'))],""",
              """grup('kondenser_kanali', [o for o in S17 if (o['lo'][0] > 2010 and o['hi'][0] < 2280 and o['hi'][1] < 1400 and o['dug'] in ('TOPPING_MODUL__koyu', 'TOPPING_MODUL__celik', 'TOPPING_MODUL__sac'))],""")
s = s.replace("""    grup('kaset_' + ad + '_cikis',""", """    grup('kaset_ray_' + ad, [o for o in K_ if id(o) not in ATANAN and o['dug'] == 'TOPPING_MODUL__paslanmaz' and o['lo'][1] > 1150 and o['hi'][1] < 1185 and o['lo'][2] < -500], 'mekanizma', 'mek', '%s kaseti rayı + 4 ayak (raf FHP-M5 saplamalarına)' % ad.capitalize())
    grup('kaset_' + ad + '_cikis',""")
s = s.replace("""    alt = [o for o in U if id(o) not in ATANAN and o['lo'][1] < 1150]""", """    alt = [o for o in U if id(o) not in ATANAN and o['hi'][1] < 1152.5]""")
open('t3_parca.py', 'w', encoding='utf-8').write(s)

# ---------------- montaj sırası
s = open('t3_montaj.py', encoding='utf-8').read()
def rep(a, b):
    global s
    assert a in s, a[:70]
    s = s.replace(a, b)
# M6 cıvatalar teknik perdeden sonra
rep("""M6 = sorted(a for a in P if a.startswith('arayuz_kaide_M6'))
yakin(merkez(M6[0]), 0.3, yon=(0.4, 0.8, 0.5), tt=t)
t = sira_tak(M6, t, 40.0, 0.55, 0.25); olay(t - 0.5, 'ISO 4762 M6 × 12 × 2: dış taban Ø6,6 → kaide plakası PEM SP-M6'); t += 0.5
""", "")
rep("""t = koy('kuru_bolme_tabani', AD(ARKA9, UST6), 'Kuru bölme tabanı → perdelerin üstüne (punta)', pem=sorted(PEM_SAC['kuru_bolme_tabani']))""",
    """M6 = sorted(a for a in P if a.startswith('arayuz_kaide_M6'))
yakin(merkez(M6[0]), 0.3, yon=(0.4, 0.8, 0.5), tt=t)
t = sira_tak(M6, t, 40.0, 0.55, 0.25); olay(t - 0.5, 'ISO 4762 M6 × 12 × 2: teknik perde deliğinden → dış taban Ø6,6 → kaide plakası PEM SP-M6'); t += 0.5
t = koy('kuru_bolme_tabani', AD(ARKA9, UST6), 'Kuru bölme tabanı → perdelerin üstüne (punta)', pem=sorted(PEM_SAC['kuru_bolme_tabani']))
t = koy('kondenser_kanali', AD(ARKA9), 'Kondenser kanalı → arkadan, braketi taban saplamalarına')""")
rep("for a in ('sogutma_grubu', 'kondenser_kanali'): t = koy(a,", "for a in ('sogutma_grubu',): t = koy(a,")
# burçlar step 8'den çıkar
rep("""for a in sorted(a for a in P if a.startswith('burc_')): koy(a, AD(ARKA9, ON9), '%s → arka duvar deliğine' % P[a]['ac'].split('(')[0].strip(), sure_bekle=0.05)
t = bitti() + 0.3""", """for a in ('evaporator_L', 'evaporator_R'): t = koy(a, AD(ARKA9), '%s → arkadan kanal kovanı ağzına (conta arka dış saca)' % P[a]['ac'].split('(')[0].strip())""")
# step 12: evaporatörler + motor + uno arka çıkar → yalnız bakır + hortum
rep("""for a in ('evaporator_L', 'evaporator_R', 'motor_kasar', 'motor_sucuk', 'uno_kiyma_arka', 'uno_kusbasi_arka', 'uno_sos_arka', 'uno_harc_arka'):
    t = koy(a, AD(ARKA9), '%s → arkadan' % P[a]['ac'].split('(')[0].strip())""", "")
rep("adim('Evaporatörler, motorlar, UNO arka grupları', 'Arka açıkken: iki evaporatör kaseti (TEK ÜRÜN) arkadan kanal kovanı ağızlarına; kaşar ve sucuk tahrik motorları arkadan, kaplini duvar burcundan geçer; dört UNO\\'nun arka grubu (pnömatik silindir + piston mili + duvar flanşı, üründen ayrılmış) arkadan, mil POM burcundan geçer, flanş FHP-M5 saplamaya. Bakır hatlar ve yoğuşma hortumu yerinde uzar.',\n     'evaporatör L · evaporatör R · kaşar motoru · sucuk motoru · UNO arka grubu × 4 · bakır hatlar · yoğuşma hortumu')",
    "adim('Soğutma hatları', 'Bakır hatlar (emiş + sıvı, lehimli) ve yoğuşma hortumu soğutma grubu ile evaporatörler arasında yerinde uzar.', 'bakır hatlar · yoğuşma hortumu')")
rep("kamera_genel(['evaporator_L', 'evaporator_R', 'uno_kiyma_arka'], yon=(0.35, 0.45, -0.85), olcek=0.8)", "kamera_genel(['evaporator_L', 'evaporator_R'], yon=(0.35, 0.45, -0.85), olcek=0.8)")
# UNO / kaset bölümü yeniden
a = s.index("ALT = [YOL((0, 0, 700), (0, -150, 0))"); b = s.index("kamera_genel(['on_cerceve_430']")
s = s[:a] + """ALT = [YOL((0, 0, 700), (0, -150, 0)), YOL((0, 0, 700), (0, -120, 0)), YOL((0, -150, 0))]
INIS = dict(lift=(60, 80, 100, 130), yan=())
for ad in ('kasar', 'sucuk'): t = koy('kaset_ray_' + ad, AD(ON9, lift=(15, 20, 30)), '%s → raf saplamalarına' % P['kaset_ray_' + ad]['ac'].split('(')[0].strip())
for ad in ('kiyma', 'kusbasi'):
    t = koy('uno_%s_on' % ad, AD(ON9, **INIS), 'UNO %s ön grubu → önden yukarıda gelir, rafa ve kovana iner' % ad)
kamera_genel(['ust_raf'], yon=(0.3, 0.5, 0.9), olcek=0.8)
for a in ('ust_raf_kosebendi_sol', 'ust_raf_kosebendi_sag'): koy(a, AD(ON9), '%s → yan astarlara (punta)' % tr(a))
t = bitti()
t = koy('ust_raf', AD(ON9, lift=(20, 40)), 'Üst raf → köşebentlere (punta)')
for ad in ('sos', 'harc'):
    t = koy('uno_%s_on' % ad, AD(ON9, **INIS), 'UNO %s ön grubu → üst raf deliğinden rafa iner' % ad)
for ad in ('kasar', 'sucuk'):
    t = koy('kaset_' + ad, AD(ON9, lift=(5, 10)), '%s → rayından sürülür' % P['kaset_' + ad]['ac'].split('(')[0].strip())
for ad in ('kiyma', 'kusbasi', 'sos', 'harc'):
    t = koy('uno_%s_cikis' % ad, ALT, 'UNO %s çıkış ağzı + yayıcı → raf kovanına (alttan)' % ad)
for ad in ('kasar', 'sucuk'):
    t = koy('kaset_%s_cikis' % ad, ALT, '%s → kovana (alttan)' % P['kaset_%s_cikis' % ad]['ac'].split('(')[0].strip())
kamera_genel(['motor_kasar', 'uno_kiyma_arka', 'uno_sos_arka'], yon=(0.35, 0.45, -0.85), olcek=0.9)
for a in sorted(a for a in P if a.startswith('burc_')): koy(a, AD(ARKA9), '%s → arkadan duvar deliğine (sıkı geçme)' % P[a]['ac'].split('(')[0].strip(), sure_bekle=0.05)
t = bitti() + 0.2
for a in ('motor_kasar', 'motor_sucuk', 'uno_kiyma_arka', 'uno_kusbasi_arka', 'uno_sos_arka', 'uno_harc_arka'):
    t = koy(a, AD(ARKA9), '%s → arkadan, burçtan geçer' % P[a]['ac'].split('(')[0].strip())
""" + s[b:]
# eski üst raf satırları (yeni bölümde var) — ikinci kopyayı sil
i1 = s.index("kamera_genel(['ust_raf'], yon=(0.3, 0.5, 0.9), olcek=0.8)"); i2 = s.index("kamera_genel(['ust_raf'], yon=(0.3, 0.5, 0.9), olcek=0.8)", i1 + 10) if s.count("kamera_genel(['ust_raf']") > 1 else -1
assert i2 == -1
rep("'UNO ön grubu × 4 · çıkış ağzı × 4 · kaşar / sucuk kaseti + çıkış · üst raf + 2 köşebent · ön çerçeve 430'",
    "'kaset rayı × 2 · UNO ön grubu × 4 · üst raf + 2 köşebent · kaşar / sucuk kaseti · çıkış ağzı × 6 · POM duvar burcu × 6 · kaset motoru × 2 · UNO arka grubu × 4 · ön çerçeve 430'")
rep("adim('UNO ön grupları, kasetler, üst raf', 'Dört UNO\\'nun ön grubu (hazne + dozaj gövdesi + döner valf) önden rafa sürülür, piston miline geçer; çıkış ağzı + yayıcı tabla açıklığından raf kovanına yukarı takılır. Kaşar / sucuk kaseti (TEK ÜRÜN) önden dil kanalına, kaplin motora geçer; çıkış ağzı kovandan. Üst raf köşebentleri + üst raf (2 büküm); ön çerçeve 430 köpük boşluğunu kapatır.',",
    "adim('UNO\\'lar, kasetler, üst raf', 'Kaset rayları raf saplamalarına. Kıyma ve kuşbaşı UNO ön grubu (hazne + dozaj gövdesi + döner valf, içinde piston) önden yukarıda gelir, rafa iner; üst raf (2 büküm) köşebentlerine; sos ve harç UNO ön grubu üst raf deliğinden iner. Kaşar / sucuk kaseti (TEK ÜRÜN) rayından sürülür. Çıkış ağızları tabla açıklığından kovanlara. Arkadan: 6 POM duvar burcu, kaset motorları (kaplin kasete geçer) ve UNO arka grupları (silindir + mil; mil burçtan geçip pistona vidalanır). Ön çerçeve 430 köpük boşluğunu kapatır.',")
rep("t = koy('x_ekseni', AD(ON9, lift=(5, 10, 20))", "t = koy('x_ekseni', AD(ON9, lift=(-10, -12, -15, -20, 5, 10))")
# beyanlı sıkı geçmeler
rep("KAY = lambda pre:", """for b_ in [a for a in P if a.startswith('burc_')]:
    for w_ in ('soguk_arka_dis_sac', 'pu_levha_arka', 'astar_arka', 'yapistirici_arka'): HARIC_PLAN.add((b_, w_)); HARIC_NEDEN[(b_, w_)] = 'POM burç duvar deliğine sıkı geçme (delik Ø = burç Ø; çokgen farkı ≤ 0,4 mm)'
for ad_ in ('kasar', 'sucuk'):
    HARIC_PLAN.add(('motor_' + ad_, 'burc_motor_' + ad_)); HARIC_NEDEN[('motor_' + ad_, 'burc_motor_' + ad_)] = 'kaplin burcun içinden geçer (yuva = kaplin, sıfır boşluk)'
    HARIC_PLAN.add(('motor_' + ad_, 'kaset_' + ad_)); HARIC_NEDEN[('motor_' + ad_, 'kaset_' + ad_)] = 'kaplin kasetin kaplinine geçer (geçme)'
for ad_ in ('kiyma', 'kusbasi', 'sos', 'harc'):
    for b_ in ('burc_uno_' + ad_, 'uno_%s_on' % ad_):
        HARIC_PLAN.add(('uno_%s_arka' % ad_, b_)); HARIC_NEDEN[('uno_%s_arka' % ad_, b_)] = 'piston mili burçtan geçer, ucu pistona vidalanır (sıfır boşluk)'
for pu_ in ('pu_levha_sol', 'pu_levha_sag', 'pu_levha_arka', 'yapistirici_arka', 'yapistirici_sol', 'yapistirici_sag', 'pu_levha_tavan', 'yapistirici_tavan'):
    HARIC_PLAN.add((pu_, 'dis_tavan')); HARIC_NEDEN[(pu_, 'dis_tavan')] = 'levha üst yüzü dış tavanın alt yüzüne sıfır boşlukla temas (yüzey boyunca kayma)'
KAY = lambda pre:""")
open('t3_montaj.py', 'w', encoding='utf-8').write(s)
print('tamam')
