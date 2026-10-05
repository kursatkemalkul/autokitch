def AD(*yon, lift=(20, 40, 120, 300, 500), yan=(30, -30)):
    """aday yollar: her ana yön için düz, sonra kaldırılmış (önce yukarıda gelir, sonra iner) ve yandan kaydırılmış"""
    L_ = []
    for d in yon: L_.append(YOL(d))
    for d in yon:
        for h in lift: L_.append(YOL(d, (0, h, 0)))
        for x in yan: L_.append(YOL(d, (x, 0, 0)))
    return L_
ON9, ARKA9, UST6 = (0, 0, 900), (0, 0, -900), (0, 600, 0)
# ---- 6 DIŞ YAN SAĞ
adim('Dış yan sağ', 'Sağ yan sac (F tarafı, J1 ağzı) lazerde kesilir, abkantta 1 büküm; 4 × PEM SP-M8 (F bağlantısı), 6 × PEM SP-M5 (servis), 2 × FHP-M5-25 (J1) ve 4 × FHP-M5 preslenir. Dış tabanın yan dönüşüne oturur, içeriden TIG.',
     'dış yan sağ · 1 büküm · 16 PEM / saplama · TIG')
kamera_genel(['dis_yan_sag', 'dis_taban'], yon=(0.6, 0.45, 0.65), olcek=0.75)
t = koy('dis_yan_sag', AD((700, 0, 0), UST6), 'Dış yan sağ → dış tabanın yan dönüşüne (TIG)', pem=sorted(PEM_SAC['dis_yan_sag']), grup_kaynak=PUNTA['yan_sag_taban'])
# ---- 7 KURU BÖLME + SOĞUTMA GRUBU
adim('Kuru bölme + soğutma grubu', 'Soğutma cebi (lazer → 3 büküm → 4 × PEM SP-M8) taban ağzından cep taşıyıcılara iner; soğutma grubu (Secop, TEK ÜRÜN) arkadan yukarıda gelir, cebe iner, 4 silikon takoz PEM\'lere; kondenser kanalı braketiyle taban saplamalarına. Ayırma perdesi, teknik ön / sağ perde, kuru bölme tabanı (2 büküm + 5 × FHP-M5) üstlerine; birleşimler punta.',
     'soğutma cebi + 4 PEM · soğutma grubu + 4 takoz · kondenser kanalı · ayırma perdesi · teknik perde × 2 · kuru bölme tabanı + 5 FHP')
kamera_genel(['sogutma_cebi', 'teknik_on_perde'], yon=(0.35, 0.6, -0.75), olcek=0.8)
t = koy('sogutma_cebi', AD(ARKA9, UST6), 'Soğutma cebi → cep taşıyıcılara (punta)', pem=sorted(PEM_SAC['sogutma_cebi']))
for a in ('sogutma_grubu', 'kondenser_kanali'): t = koy(a, AD(ARKA9, UST6), '%s → arkadan, cebe iner' % P[a]['ac'].split('(')[0].strip())
for a in ('ayirma_perdesi_cep_sol', 'teknik_on_perde', 'teknik_sag_perde'): t = koy(a, AD(ARKA9, UST6, ON9), '%s → yerine (punta)' % tr(a))
t = koy('kuru_bolme_tabani', AD(ARKA9, UST6), 'Kuru bölme tabanı → perdelerin üstüne (punta)', pem=sorted(PEM_SAC['kuru_bolme_tabani']))
# ---- 8 SOĞUK ODA ARKA DUVARI
adim('Soğuk oda: taban + arka duvar', 'Soğuk oda alt sacı (2 × FHP-M5) ve arka dış sacı (12 × FHP-M5, kanal ağızları açık) yerine girer; 4 evaporatör kanal kovanı (iki L + boyuna TIG) ağızlara; arka duvara 3 POM geçiş bloğu ve 6 POM duvar burcu (UNO pistonları + kaset motorları); ölçüsünde kesilmiş PU arka levhası önden kovanların ve burçların üstünden geçer, astar arka (1,0) üstüne kapanır.',
     'alt sac · arka dış sac · 4 kanal kovanı · POM geçiş bloğu × 3 · POM duvar burcu × 6 · PU levha arka · astar arka')
kamera_genel(['soguk_alt_sac', 'soguk_arka_dis_sac'], yon=(0.35, 0.5, 0.85), olcek=0.75)
t = koy('soguk_alt_sac', AD(ON9, ARKA9, UST6), 'Soğuk oda alt sacı → teknik perdelerin üstüne (punta)', pem=sorted(PEM_SAC['soguk_alt_sac']))
t = koy('soguk_arka_dis_sac', AD(ARKA9, ON9, UST6), 'Soğuk oda arka dış sacı → alt sac + yanlar (punta)', pem=sorted(PEM_SAC['soguk_arka_dis_sac']))
for k in range(4):
    for j in (1, 2):
        koy('evap_kanal_kovani_%d_L%d' % (k, j), AD(ON9), '%s → arka dış sacın ağzına' % tr('evap_kanal_kovani_%d_L%d' % (k, j)),
            grup_kaynak=(KAY('evap_kanal_kovani_%d_boyuna_kaynak' % k) if j == 2 else ()), sure_bekle=0.05)
    t += 0.4
t = bitti() + 0.2
for a in sorted(a for a in P if a.startswith(('pom_gecis', 'burc_'))): koy(a, AD(ON9), '%s → arka duvara' % P[a]['ac'].split('(')[0].strip(), sure_bekle=0.05)
t = bitti() + 0.3
kamera_genel(['pu_levha_arka', 'astar_arka'], yon=(0.25, 0.4, 0.9), olcek=0.7)
t = koy('pu_levha_arka', AD(ON9), 'PU levha arka (ölçüsünde kesilmiş) → arka dış saca yaslanır')
t = koy('astar_arka', AD(ON9), 'Astar arka 1,0 → levhanın önüne')
# ---- 9 DIŞ YAN SOL + TAVAN
adim('Dış yan sol + dış tavan', 'Sol yan (A tarafı): lazer → 1 büküm → 4 × PEM SP-M8 (A) + 2 × PEM SP-M5 → tabanın yan dönüşüne, içeriden TIG; A tarafındaki 2 PEM\'in iç yüzüne köpük kapağı. Dış tavan: lazer → 3 büküm → 5 × PEM SP-M5 → yan sacların üstüne, TIG.',
     'dış yan sol + 6 PEM · köpük kapağı × 2 · dış tavan + 5 PEM · TIG')
kamera_genel(['dis_yan_sol', 'dis_taban'], yon=(-0.6, 0.45, 0.65), olcek=0.75)
t = koy('dis_yan_sol', AD((-700, 0, 0), UST6), 'Dış yan sol → dış tabanın yan dönüşüne (TIG)', pem=sorted(PEM_SAC['dis_yan_sol']), grup_kaynak=PUNTA['yan_sol_taban'])
KK = sorted(a for a in P if a.endswith('kopuk_kapagi'))
yakin(merkez(KK[0]), 0.3, yon=(0.8, 0.3, 0.5), tt=t)
for i, a in enumerate(KK): tak(a, t + i * 0.2, 0.5, 40.0)
olay(t, 'Köpük kapağı × 2 → A tarafı PEM SP-M8\'lerin iç yüzüne'); t = bitti() + 0.3
kamera_genel(['dis_tavan', 'dis_yan_sol'], yon=(0.45, 0.85, 0.6), olcek=0.75)
t = koy('dis_tavan', AD(UST6), 'Dış tavan → yan sacların üstüne (TIG)', pem=sorted(PEM_SAC['dis_tavan']), grup_kaynak=PUNTA['tavan_yanlar'])
# ---- 10 YALITIM + ASTAR (sol, sağ, tavan)
adim('Yalıtım levhaları + astar', 'Yüzey yüzey: ölçüsünde kesilmiş PU levha (delikleri ve cepleri açılmış) önden girer, dış saca yaslanır; hemen önüne o yüzün astar sacı (1,0) kapanır ve iç köşede astar arkaya TIG ile bağlanır. Sıra: sol → sağ → tavan. Raf askı burçları (POM) astar ve levha deliklerinden içeriden.',
     'PU levha sol + astar sol · PU levha sağ + astar sağ · PU levha tavan + astar tavan · iç köşe TIG · POM burç × 16')
for pu, ast, d in (('pu_levha_sol', 'astar_sol', 80), ('pu_levha_sag', 'astar_sag', -80), ('pu_levha_tavan', 'astar_tavan', 0)):
    kamera_genel([pu, ast], yon=(0.25, 0.4, 0.9), olcek=0.7)
    yp = ([YOL(ON9, (d, 0, 0))] if d else []) + AD(ON9)
    t = koy(pu, yp, '%s → dış saca yaslanır' % P[pu]['ac'].split('(')[0].strip())
    t = koy(ast, AD(ON9) + yp, '%s → levhanın önüne · iç köşe TIG' % tr(ast), grup_kaynak=PUNTA[ast])
t += 0.3
kamera_genel(['astar_sol'], yon=(0.6, 0.4, 0.75), olcek=0.8)
BURC = sorted(a for a in P if a.startswith('pom_burc'))
for i, a in enumerate(BURC):
    e_ = np.asarray(P[a]['eks'], float); t_ = t + i * 0.08
    basla(a, -e_ * 80.0, t_); git(a, np.zeros(3), t_, 0.5); vurgu([a], t_ + 0.3, t_ + 1.2); YER[a] = t_ + 0.5; YERINDE.append(a)
olay(t, 'Raf askı burcu POM × 16 → astar + levha deliklerinden içeriden (sıkı geçme)'); t = bitti() + 0.5
# ---- 11 RAF
adim('Raf, kovanlar, eşik', 'Raf köşebentleri ve 6 düşme kovanı (kıyma / kuşbaşı iki L + TIG, sos / harç boru, kaşar / sucuk POM) alt saca; PU raf levhası yukarıdan kovanların üstünden iner; raf (3 mm, lazer → 4 büküm → 4 × FHP-M5) levhanın üstüne kapanır, arka köşe dolgu kaynağı. Dil kanalları, eşik (3 büküm), yiv dolguları + köşe silikonu.',
     'raf köşebendi × 2 · düşme kovanı × 6 · PU raf levhası · raf + 4 FHP · dil kanalı × 2 · eşik · yiv dolgusu × 10 · silikon × 8')
kamera_genel(['raf', 'raf_kosebendi_sol'], yon=(0.35, 0.7, 0.75), olcek=0.75)
for a in ('raf_kosebendi_sol', 'raf_kosebendi_sag'): koy(a, AD(ON9, UST6), '%s → alt saca (punta)' % tr(a))
t = bitti()
for a in ('dusme_kovani_kiyma_L1', 'dusme_kovani_kiyma_L2', 'dusme_kovani_kusbasi_L1', 'dusme_kovani_kusbasi_L2'):
    koy(a, AD(ON9, UST6), '%s → alt sacın deliğine' % tr(a), grup_kaynak=(KAY(a[:-3] + '_boyuna_kaynak') if a.endswith('L2') else ()), sure_bekle=0.05)
for a in ('dusme_kovani_sos', 'dusme_kovani_harc', 'dusme_kovani_kasar', 'dusme_kovani_sucuk'):
    koy(a, AD(ON9, UST6), '%s → alt sacın deliğine' % P[a]['ac'].split('·')[0].strip(), sure_bekle=0.05)
t = bitti() + 0.2
t = koy('pu_raf_esik', AD(UST6, ON9, lift=(100, 300, 500)), 'PU raf levhası → kovanların üstünden alt saca')
t = koy('raf', AD(UST6, ON9, lift=(60, 100, 300, 500)), 'Raf → PU levhanın üstüne, kenarları köşebentlere (punta)', pem=sorted(PEM_SAC['raf']), grup_kaynak=KAY('raf_arka_kose_dolgusu'))
kamera_genel(['soguk_esik', 'dil_kanali_kasar'], yon=(0.3, 0.6, 0.9), olcek=0.7)
for a in ('dil_kanali_kasar', 'dil_kanali_sucuk'): t = koy(a, AD(ON9, UST6), '%s → rafın kesiğine' % tr(a))
t = koy('soguk_esik', AD(ON9, UST6), 'Eşik → rafın ön kenarına', grup_kaynak=KAY('raf_esik_yiv') + KAY('esik_on_yiv'))
for k in sorted(a for a in P if a.startswith('dil_kesik_kose_silikonu')): buyu(k, t, 0.4)
olay(t, 'Yiv dolgusu TIG + taşlama × 10 · eşik kesiği köşe silikonu × 8'); t += 0.9
# ---- 12 SOĞUTMA + MOTORLAR + UNO ARKA
adim('Evaporatörler, motorlar, UNO arka grupları', 'Arka açıkken: iki evaporatör kaseti (TEK ÜRÜN) arkadan kanal kovanı ağızlarına; kaşar ve sucuk tahrik motorları arkadan, kaplini duvar burcundan geçer; dört UNO\'nun arka grubu (pnömatik silindir + piston mili + duvar flanşı, üründen ayrılmış) arkadan, mil POM burcundan geçer, flanş FHP-M5 saplamaya. Bakır hatlar ve yoğuşma hortumu yerinde uzar.',
     'evaporatör L · evaporatör R · kaşar motoru · sucuk motoru · UNO arka grubu × 4 · bakır hatlar · yoğuşma hortumu')
kamera_genel(['evaporator_L', 'evaporator_R', 'uno_kiyma_arka'], yon=(0.35, 0.45, -0.85), olcek=0.8)
for a in ('evaporator_L', 'evaporator_R', 'motor_kasar', 'motor_sucuk', 'uno_kiyma_arka', 'uno_kusbasi_arka', 'uno_sos_arka', 'uno_harc_arka'):
    t = koy(a, AD(ARKA9), '%s → arkadan' % P[a]['ac'].split('(')[0].strip())
for a in ('bakir_hat', 'yogusma_hortumu'): buyu(a, t, 1.0)
olay(t, 'Bakır hatlar (lehim) + yoğuşma hortumu: grup ↔ evaporatörler'); t += 1.4
# ---- 13 HAVA + ELEKTRİK İÇ
adim('Valf adası, hava kanalı, iç kanallar, J1', 'Hava kanalı askıları arka dış sacın ve kuru tabanın FHP-M5 saplamalarına, hava kanalları üstlerine; valf adası (12 valf, TEK ÜRÜN). İç kablo kanalları ve braketler; J1 gömme fiş paneli sağ yandaki FHP-M5-25 saplamalarına içeriden. Hava hortumları ve kablolar kanal boyunca uzar.',
     'hava askısı × 13 · hava kanalı × 3 · valf adası · iç kanallar · J1 paneli · hortumlar · kablolar')
kamera_genel(['valf_adasi', 'hava_kanal_2014_1259'], yon=(0.35, 0.45, -0.85), olcek=1.0)
for a in sorted(a for a in P if a.startswith('hava_aski')): koy(a, AD(ARKA9), 'Hava askısı → FHP-M5 saplamaya', sure_bekle=0.03)
t = bitti()
for a in sorted(a for a in P if a.startswith('hava_kanal')): t = koy(a, AD(ARKA9), 'Hava kanalı → askılara')
t = koy('valf_adasi', AD(ARKA9), 'Valf adası → arkadan')
for a in sorted(a for a in P if a.startswith('elk_')): koy(a, AD(ARKA9, ON9), '%s → yerine' % P[a]['ac'], sure_bekle=0.03)
t = bitti()
t = koy('j1_panel', [YOL((0, 0, -500), (-60, 0, 0))] + AD(ARKA9), 'J1 gömme fiş paneli → sağ yanın FHP-M5-25 saplamalarına (içeriden)')
for a in ('hava_hortum', 'hava_giris', 'j1_kablo', 'kablo_guc', 'kablo_bilgi'): buyu(a, t, 1.0)
olay(t, 'Hava hortumları (YEŞİL) · güç (KIRMIZI) / bilgi (MAVİ) kabloları kanal boyunca'); t += 1.4
# ---- UNO ÖN + KASET + ÜST RAF + ÇERÇEVE
adim('UNO ön grupları, kasetler, üst raf', 'Dört UNO\'nun ön grubu (hazne + dozaj gövdesi + döner valf) önden rafa sürülür, piston miline geçer; çıkış ağzı + yayıcı tabla açıklığından raf kovanına yukarı takılır. Kaşar / sucuk kaseti (TEK ÜRÜN) önden dil kanalına, kaplin motora geçer; çıkış ağzı kovandan. Üst raf köşebentleri + üst raf (2 büküm); ön çerçeve 430 köpük boşluğunu kapatır.',
     'UNO ön grubu × 4 · çıkış ağzı × 4 · kaşar / sucuk kaseti + çıkış · üst raf + 2 köşebent · ön çerçeve 430')
kamera_genel(['uno_kiyma_on', 'uno_sos_on', 'kaset_kasar'], yon=(0.3, 0.45, 0.9), olcek=0.9)
ALT = [YOL((0, 0, 700), (0, -150, 0)), YOL((0, 0, 700), (0, -120, 0)), YOL((0, -150, 0))]
for ad in ('kiyma', 'kusbasi', 'sos', 'harc'):
    t = koy('uno_%s_on' % ad, AD(ON9, lift=(10, 15, 30)), 'UNO %s ön grubu → rafa, piston miline' % ad)
    t = koy('uno_%s_cikis' % ad, ALT, 'UNO %s çıkış ağzı + yayıcı → raf kovanına (alttan)' % ad)
for ad in ('kasar', 'sucuk'):
    t = koy('kaset_' + ad, AD(ON9, lift=(10, 15, 30)), '%s → dil kanalından, kaplin motora' % P['kaset_' + ad]['ac'].split('(')[0].strip())
    t = koy('kaset_%s_cikis' % ad, ALT, '%s → kovana (alttan)' % P['kaset_%s_cikis' % ad]['ac'].split('(')[0].strip())
kamera_genel(['ust_raf'], yon=(0.3, 0.5, 0.9), olcek=0.8)
for a in ('ust_raf_kosebendi_sol', 'ust_raf_kosebendi_sag'): koy(a, AD(ON9), '%s → yan astarlara (punta)' % tr(a))
t = bitti()
t = koy('ust_raf', AD(ON9, lift=(20, 40)), 'Üst raf → köşebentlere (punta)')
kamera_genel(['on_cerceve_430'], yon=(0.3, 0.4, 0.9), olcek=0.75)
t = koy('on_cerceve_430', AD(ON9), 'Ön çerçeve 430 → soğuk oda önü (punta)') + 0.3
