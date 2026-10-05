

# ------------------------------------------------------------------ TOPPING + F (adım 6 devamı · 4 Eki)
def AN(pred):
    """henüz yerleşmemiş ana-model parçaları (küme) — pred(ad, bilgi, lo, hi)"""
    out = []
    for a in P:
        if P[a]['kay'] != 'ana' or a in GOR or a in GIZLI: continue
        b = ANA_BILGI[a]; lo, hi = bbox([a])
        if pred(a, b, lo, hi): out.append(a)
    return sorted(out)


def mekk(*kodlar):
    return lambda a, b, lo, hi: b['mek'] in kodlar


def kam_k(t, adlar, kay, uzak=None, yon=(0.55, 0.5, 1.0)):
    """kaydırılmış (tezgâhta / alt montajda) parçalara kamera"""
    lo, hi = bbox(adlar); h = (lo + hi) / 2 + np.array(kay, float)
    yon = np.array(yon, float); yon /= np.linalg.norm(yon)
    dist = uzak * 1.6 if uzak else min(max(_fit(lo, hi), _fit(ZARF[0], ZARF[1]) * 0.45), _fit(ZARF[0], ZARF[1]) * 1.05)
    pos = h + yon * dist; pos[1] = max(pos[1], 0.25)
    KAM.append([round(t, 2), [round(float(v), 4) for v in pos], [round(float(v), 4) for v in h]])


def gel_say(adlar, d, t, sure=1.1, top=2.4):
    """çok parçalı grup: aralık toplam süreye sığar"""
    if not adlar: return t
    ara = min(0.12, top / max(1, len(adlar)))
    return gel(adlar, d, t, sure, ara)


def seq_TOPPING():
    global SAHIP
    BASLIK.update(kod='TOPPING')
    SECIM[:] = [('dis_yan_sol', 1), ('dis_taban', 1), ('dis_tavan', 1), ('dis_arka_servis', 1), ('astar_arka', 1), ('raf', 1), ('ust_raf', 1), ('soguk_esik', 1),
                ('on_cerceve_430', 1), ('kaide_on_perde_menfezli', 1), ('sogutma_cebi', 1), ('evap_kanal_kovani_0_L1', 8)]
    t = kartlar(0.0, 'kaide 7 boru + menfezli ön perde C · dış kabuk 4 sac · sökülür arka servis sacı · soğuk oda 13 sac · 6 düşme kovanı · 4 evaporatör kanal kovanı')
    for a in R(r'^arayuz_(mek_|j1_)'): GIZLI.add(a)        # mekanizma FHP-M5 / J1 burçları: karşı parça ana modelde
    PANEL = ['kaide_ust_plaka_4', 'dis_taban', 'dis_yan_sol', 'dis_yan_sag', 'dis_tavan', 'sogutma_cebi']
    SAHIP = sahip_ata(PANEL)
    # 4 kaide
    t4 = t; kam(t, R(r'^kaide_'), (0, 1, 0))
    olay(t, 'Kaide boruları (40 × 100 × 2) fikstürde: arka, sol, sağ, enine · boyuna borular')
    t = gel(R(r'^kaide_(arka|sol|sag|enine)_boru$'), (0, 0.45, 0), t, 1.0, 0.2) + 0.1
    t = gel(R(r'^kaide_boyuna_boru_\d$') + R(r'^kaide_enine_lama_\d$'), (0, 0.45, 0), t, 1.0, 0.15)
    t = kaynak(R(r'^kaide_.*(boru|lama).*kaynak'), t) + 0.2
    olay(t, 'Menfezli ön perde (2,0 C) — kanat menfezleri hizasında · soğutma cebi taşıyıcı L × 2')
    t = gel(R(r'^kaide_on_perde_menfezli$'), (0, 0, 0.5), t, 1.1)
    t = gel(R(r'^kaide_cep_tasiyici_\d$'), (0, 0.3, 0), t, 0.8, 0.15) + 0.1
    olay(t, 'Kaide üst plakası 4 mm — PEM SP-M6 (ray + gövde) DÜZ sacta basılı · 17 delik kaynağı')
    sap = sorted(s for s, p in SAHIP.items() if p == 'kaide_ust_plaka_4')
    t = gel(['kaide_ust_plaka_4'] + sap, (0, 0.55, 0), t, 1.3) + 0.1
    t = kaynak(R(r'^kaide_ust_plaka_delik_kaynagi'), t, 0.35, 0.05) + 0.4
    adim(4, 'Kaide · menfezli ön perde', t4, t,
         "TOPPING kaidesi 40 × 100 × 2 borulardan fikstürde kaynaklanır. Önde menfezli 2,0 mm C perde (kanat menfezleriyle aynı hizada, kuru bölmenin emiş havası buradan), arkada emiş filtresi yeri. Üst plaka 4 mm; tabla rayının 4 × M6 ve gövdenin 2 × M6 PEM'i düz sacta basılıdır.",
         '7 boru + enine lama · menfezli ön perde C · 2 cep taşıyıcı L · üst plaka 4 mm + 6 PEM SP-M6 · 17 delik kaynağı')
    # 5 dış kabuk + kuru bölme
    t5 = t
    t = panel(['dis_taban'], (0, 0.45, 0), t, 'Dış taban 1,5 (3 büküm) kaideye — servis sacının PEM SP-M5 somunları arka dönüşte')
    olay(t, 'Gövde → kaide: 2 × ISO 4762 M6 tabandan plakadaki PEM\'e')
    t = gel(R(r'^arayuz_kaide_M6_[01]$'), (0, 0.12, 0), t, 0.5, 0.1) + 0.1
    t = panel(['dis_yan_sol'], (-0.6, 0, 0), t, "Sol yan sac (A tarafı) — tabla ağzı alta açık · A bağlantısı 4 × PEM SP-M8")
    t = gel(R(r'^pem_M8_A_\d+_\d+$'), (-0.15, 0, 0), t, 0.5, 0.05) + 0.1
    t = panel(['dis_yan_sag'], (0.6, 0, 0), t, "Sağ yan sac (F tarafı) — J1 ağzı 57 × 67 · F bağlantısı 4 × PEM SP-M8")
    t = gel(R(r'^pem_M8_F_\d+_\d+$'), (0.15, 0, 0), t, 0.5, 0.05) + 0.1
    t = panel(['dis_tavan'], (0, 0.55, 0), t, 'Dış tavan yanların arasına (yan dönüş yalnız kuru bölmede) · köşeler TIG')
    olay(t, 'Kuru (teknik) bölme: soğutma cebi + ayırma perdesi, teknik ön / sağ perde, kuru bölme tabanı')
    kam(t, R(r'^(sogutma_cebi|ayirma_perdesi|teknik_|kuru_bolme)'), (0, 0.3, 1))
    sap = sorted(s for s, p in SAHIP.items() if p == 'sogutma_cebi')
    t = gel(['sogutma_cebi'] + sap, (0, 0, 0.7), t, 1.1) + 0.1
    t = gel(R(r'^ayirma_perdesi_cep_sol$') + R(r'^teknik_(on|sag)_perde$'), (0, 0, 0.7), t, 1.0, 0.2)
    t = gel(R(r'^kuru_bolme_tabani$'), (0, 0, 0.7), t, 1.0) + 0.4
    adim(5, 'Dış kabuk · kuru bölme', t5, t,
         "Dış kabuk 304 1,5 mm, kaynaklı: taban → sol yan → sağ yan → tavan. Arka yüz açık kalır (sökülür servis sacı en sonda). Soğuk odanın altındaki kuru bölmede soğutma cebi (4 × PEM SP-M8 titreşim takozu), ayırma perdesi, teknik perdeler ve kuru bölme tabanı.",
         'dış taban · 2 × M6 gövde → kaide · sol yan + 4 PEM M8 (A) · sağ yan + 4 PEM M8 (F) · tavan · soğutma cebi · ayırma + teknik perdeler · kuru bölme tabanı')
    # 6 soğuk oda iç kabuğu + raflar
    t6 = t
    olay(t, 'Soğuk oda alt sacı + arka dış sacı (evaporatör kanal ağızları açık)')
    kam(t, R(r'^(soguk_|astar_|raf|ust_raf)'), (0, 0.3, 1))
    t = gel(R(r'^soguk_alt_sac$'), (0, 0, 0.8), t, 1.1)
    t = gel(R(r'^soguk_arka_dis_sac$'), (0, 0, 0.8), t, 1.1) + 0.1
    olay(t, '4 evaporatör kanal kovanı (iki L, boyuna dikiş) arka dış sac ile astar arasına')
    t = gel(R(r'^evap_kanal_kovani_\d_L\d$'), (0, 0, 0.5), t, 0.7, 0.06)
    t = kaynak(R(r'^evap_kanal_kovani_.*kaynak'), t, 0.3, 0.04) + 0.1
    olay(t, 'Astar 1,0 — 4 düz sac (arka, sol, sağ, tavan) · TIG + R3 iç köşe')
    t = gel(R(r'^astar_arka$'), (0, 0, 0.8), t, 1.0)
    t = gel(R(r'^astar_(sol|sag)$'), (0, 0, 0.8), t, 0.9, 0.2)
    t = gel(R(r'^astar_tavan$'), (0, 0, 0.8), t, 0.9) + 0.1
    olay(t, 'Raf 3,0 (iki büküm) + köşebentler · düşme kovanları (kıyma / kuşbaşı 3,0 sac · sos / harç boru · kaşar / sucuk POM-C)')
    kam(t, R(r'^(raf|dusme_kovani|dil_kanali|soguk_esik)'), (0, 0.4, 1))
    t = gel(R(r'^raf_kosebendi_(sol|sag)$'), (0, 0, 0.6), t, 0.7, 0.15)
    t = gel(R(r'^raf$'), (0, 0, 0.8), t, 1.0)
    t = kaynak(R(r'^raf_arka_kose_dolgusu'), t, 0.4) + 0.1
    t = gel(R(r'^dusme_kovani_(kiyma|kusbasi)_L\d$') + R(r'^dusme_kovani_(sos|harc|kasar|sucuk)$'), (0, -0.25, 0), t, 0.7, 0.08)
    t = kaynak(R(r'^dusme_kovani_.*kaynak'), t, 0.3, 0.04) + 0.1
    olay(t, 'Kaşar / sucuk dil kanalları (U 1,0) + eşik 1,2 — yiv dolgusu TIG + taşlama (gıda yüzeyi düz)')
    t = gel(R(r'^dil_kanali_(kasar|sucuk)$'), (0, 0, 0.5), t, 0.8, 0.15)
    t = gel(R(r'^soguk_esik$'), (0, 0, 0.6), t, 0.9)
    t = kaynak(R(r'^(raf_esik_yiv_dolgusu|esik_on_yiv_dolgusu)'), t, 0.3, 0.05)
    t = yerinde(R(r'^dil_kesik_kose_silikonu'), t, 0.3, 0.03) + 0.1
    olay(t, 'Üst raf 3,0 + köşebentler · raf askı burçları (POM + paslanmaz pim)')
    t = gel(R(r'^ust_raf_kosebendi_(sol|sag)$'), (0, 0, 0.6), t, 0.7, 0.15)
    t = gel(R(r'^ust_raf$'), (0, 0, 0.8), t, 1.0)
    burc = AN(lambda a, b, lo, hi: b['mek'] == 'TOPPING/Gövde' and not b['kpk'] and P[a]['m'] != 'kapak_s' and hi[2] < 0.0)
    t = gel_say(burc, (0, 0, 0.3), t, 0.6, 1.6) + 0.1
    olay(t, 'Ön çerçeve 430 1,0 önden — soğuk oda boşluğunu kapatır')
    t = gel(R(r'^on_cerceve_430$'), (0, 0, 0.7), t, 1.2) + 0.4
    adim(6, 'Soğuk oda · astar, raflar, eşik, kovanlar, ön çerçeve', t6, t,
         "Soğuk oda iç kabuğu dış kabuğun içine kurulur: alt sac, arka dış sac, 4 düz astar sacı. Raf ve üst raf 3 mm (iki büküm + köşebent); raf ile eşik dil kanalıyla tek parça. Malzeme düşme kovanları raftan geçer (kaşar / sucuk POM-C CNC, kıyma / kuşbaşı 3 mm sac, sos / harç boru). Evaporatör hava yolu için 4 kanal kovanı. Ön çerçeve köpük boşluğunu kapatır.",
         'alt sac · arka dış sac · 4 kanal kovanı · astar 4 sac · raf + 2 köşebent · 6 düşme kovanı · 2 dil kanalı · eşik · üst raf + 2 köşebent · raf burçları · ön çerçeve')
    # 7 PU
    t7 = t
    olay(t, 'Köpüklemeden önce: A tarafındaki PEM\'lere PE köpük kapağı')
    kam(t, None)
    t = yerinde(R(r'_kopuk_kapagi$'), t, 0.4, 0.1) + 0.2
    olay(t, 'PU köpükleme (SARI): dış kabuk ↔ astar ve raf / eşik içi, 40 kg/m³ — kalıpta, 24 saat kür')
    t = yerinde(sorted(a for a in P if P[a]['tur'] == 'pu' and a not in GOR), t, 1.6, 0.4) + 0.6
    adim(7, 'PU köpükleme', t7, t,
         "Soğuk odanın duvarları ve raf / eşik çift cidarı PU ile doldurulur (sahnede sarı; normalde görünmez). Evaporatör kanal kovanları köpüğün içinden geçer, ağızları açık kalır.",
         '2 köpük kapağı · PU soğuk duvar · PU raf + eşik')
    # 8 arka servis sacı alt montajı (tezgâhta, arkada)
    t8 = t
    SV = (0, 0, -1.1)
    serv_kutu = AN(lambda a, b, lo, hi: b['mek'] == 'TOPPING/Elektrik' and b['dugum'] in ('TOPPING_MODUL__sac', 'TOPPING_MODUL__celik'))
    SERV = ['dis_arka_servis'] + R(r'^servis_arka_.*_vida$') + R(r'^kaide_arka_emis_filtresi$') + serv_kutu
    olay(t, 'Arka servis sacı alt montajı (tezgâhta, arkada): sac + pano kutusu + DIN plakası / rayları + emiş filtresi')
    kam_k(t, ['dis_arka_servis'], SV, uzak=1.5, yon=(0.5, 0.45, -1.0))
    t = gel(['dis_arka_servis'], (0, 0, -0.5), t, 1.2) + 0.1
    t = gel(serv_kutu, (0, 0, -0.35), t, 0.9, 0.15) + 0.1
    t = gel(R(r'^kaide_arka_emis_filtresi$'), (0, -0.2, 0), t, 0.7) + 0.4
    adim(8, 'Arka servis sacı · alt montaj', t8, t,
         "Arka yüz tek parça sökülür servis sacıdır (bakım bu yüzden). Pano kutusu, DIN plakası, emiş filtresi ve evaporatör ayakları bu sacın FHP-M5 saplamalarına bağlanır; sacla birlikte sökülür. Sac şimdilik tezgâhta bekler — iç montaj arkadan yapılır, sac en sonda 17 × M5 ile kapanır.",
         'servis sacı 1,5 · pano kutusu · DIN plakası + rayları · emiş filtresi')
    t = sac_tamam(t)
    no = 9
    # 9 soğutma
    t0 = t
    sog = AN(mekk('TOPPING/Soğutma'))
    grup = [a for a in sog if bbox([a])[1][1] < 1.105 and P[a]['m'] != 'pu']
    bak = [a for a in sog if ANA_BILGI[a]['dugum'].endswith(('__bakir', '__silikon')) and a not in grup]
    evL = [a for a in sog if a not in grup and a not in bak and bbox([a])[0][0] < 1.70]
    evR = [a for a in sog if a not in grup and a not in bak and a not in evL]
    olay(t, 'Soğutma grubu (Secop) arkadan soğutma cebine — 4 silikon titreşim takozu cep tabanındaki PEM SP-M8\'lere')
    kam(t, grup, (0, 0.2, -1))
    t = gel(grup, (0, 0, -0.8), t, 1.4) + 0.2
    olay(t, 'Evaporatör L ve R (kaset + fan) arkadan — kanal kovanlarının ağzına, ayakları servis sacının FHP-M5 saplamalarına')
    kam(t, evL + evR, (0, 0.2, -1))
    t = gel(evL, (0, 0, -0.8), t, 1.3) + 0.15
    t = gel(evR, (0, 0, -0.8), t, 1.3) + 0.2
    olay(t, 'Bakır hatlar (emiş / sıvı) + yoğuşma hortumu — grup ↔ evaporatörler, kanal içinden')
    kam(t, bak, (0, 0.2, -1))
    t = gel(bak, (0, 0, -0.5), t, 1.3, 0.2) + 0.5
    adim(no, 'Soğutma grubu + evaporatör L / R + bakır hatlar', t0, t,
         "Kompakt soğutma grubu (Secop) kuru bölmedeki cebe titreşim takozlarıyla oturur. İki evaporatör kaseti soğuk odanın arkasında, kanal kovanlarının ağzında; ayakları servis sacına bağlanır. Bakır hatlar ve yoğuşma hortumu grubu evaporatörlere bağlar.",
         'soğutma grubu + 4 takoz · evaporatör L · evaporatör R · bakır hatlar · yoğuşma hortumu'); no += 1
    # 10 kaset tahrik motorları
    t0 = t
    km = AN(lambda a, b, lo, hi: b['mek'] in ('TOPPING/Kaşar', 'TOPPING/Sucuk') and b['dugum'] == 'TOPPING_MODUL__motor')
    olay(t, 'Kaşar + sucuk kaset tahrik motorları arkadan — kaplin raf arkasında, kaset sürülünce geçer')
    kam(t, km, (0, 0.2, -1))
    t = gel(km, (0, 0, -0.6), t, 1.2, 0.3) + 0.5
    adim(no, 'Kaset tahrik motorları', t0, t, "Kaşar ve sucuk kasetlerinin tahrik motorları soğuk odanın arkasındaki kuru boşlukta sabit kalır; kaset önden sürüldüğünde kaplin kendiliğinden geçer (kaset sökülürken motor yerinde).",
         '2 kaset tahrik motoru'); no += 1
    # 11 elektrik
    t0 = t
    elk = AN(mekk('TOPPING/Elektrik'))
    kart = [a for a in elk if ANA_BILGI[a]['dugum'] in ('TOPPING_MODUL__kart', 'TOPPING_MODUL__koyu')]
    kanal = [a for a in elk if P[a]['m'] == 'kanal' or ANA_BILGI[a]['dugum'] == 'ELK_TOPPING__celik']
    fis = [a for a in elk if P[a]['m'] == 'fis' or ANA_BILGI[a]['dugum'] == 'ELK_ZINCIR__paslanmaz']
    guc = [a for a in elk if P[a]['m'] == 'guc' and a not in fis]
    bil = [a for a in elk if P[a]['m'] == 'bilgi' and a not in fis]
    kalanE = [a for a in elk if a not in kart + kanal + fis + guc + bil]
    olay(t, 'Sürücü kartları DIN rayına + istasyon kutusu cihazları (servis sacı üstünde, tezgâhta)')
    kam_k(t, kart, SV, uzak=1.1, yon=(0.5, 0.45, -1.0))
    t = gel(kart + kalanE, (0, 0.25, 0), t, 0.8, 0.15) + 0.2
    SERV += kart + kalanE
    olay(t, 'İç kablo kanalları + braketler (PEM saplamalı kanal ayakları)')
    kam(t, kanal, (0, 0.2, -1))
    t = gel_say(kanal, (0, 0, -0.45), t, 0.9, 1.6) + 0.2
    olay(t, 'Güç kabloları (KIRMIZI) — motorlara, kanal içinden')
    kam(t, guc, (0, 0.2, -1)); t = gel_say(guc, (0, 0, -0.45), t, 1.0, 2.0) + 0.2
    olay(t, 'Bilgi kabloları (MAVİ) — sensör, enkoder, EtherCAT · ayrı kanal bölmesinden')
    kam(t, bil, (0, 0.2, -1)); t = gel_say(bil, (0, 0, -0.45), t, 1.0, 2.0) + 0.2
    olay(t, 'Gömme fiş paneli (J1, sağ yanda): Harting güç + M12 bilgi + kablo rakorları')
    kam(t, fis, (1, 0.1, 0))
    t = gel_say(fis, (0.3, 0, 0), t, 0.9, 1.6) + 0.5
    adim(no, 'Elektrik · kartlar, kutu, kanallar, kablolar, fiş paneli', t0, t,
         "Sürücü kartları ve istasyon kutusu cihazları servis sacındaki DIN rayına (sacla birlikte sökülür). Kablolar yalnız kanal içinden: güç kırmızı, bilgi mavi, ayrı bölmelerden. İstasyona dışarıdan yalnız sağ yandaki gömme J1 fiş panelinden girilir (Harting / M12).",
         '%d sürücü kartı + kutu cihazları · iç kanallar · güç (kırmızı) · bilgi (mavi) · J1 fiş paneli' % sum(1 for a in kart if 'kart' in ANA_BILGI[a]['dugum'])); no += 1
    # 12 hava
    t0 = t
    hv = AN(mekk('TOPPING/Hava'))
    vada = [a for a in hv if ANA_BILGI[a]['dugum'] in ('TOPPING_MODUL__siyah', 'TOPPING_MODUL__aluminyum', 'TOPPING_MODUL__pom')]
    olay(t, 'Valf adası (12 valf) arka bölmeye · hava kanalı + askılar')
    kam(t, hv, (0, 0.2, -1))
    t = gel(vada, (0, 0, -0.4), t, 0.9, 0.05) + 0.1
    kn = [a for a in hv if a not in vada and ANA_BILGI[a]['dugum'].startswith(('HAVA_IC__', 'ELK_ZINCIR__rakor', 'ELK_ZINCIR__kod'))]
    t = gel_say(kn, (0, 0, -0.35), t, 0.8, 1.4) + 0.1
    olay(t, 'Hava hortumları (YEŞİL) — valf adasından UNO pistonlarına, J1 hava rakorundan girişe')
    t = gel_say([a for a in hv if a not in vada and a not in kn], (0, 0, -0.45), t, 1.1, 1.6) + 0.5
    adim(no, 'Valf adası + hava hortumları', t0, t, "Basınçlı hava J1 panelindeki gömme rakordan girer; valf adası 4 UNO pistonunu ve yayıcıları sürer. Hortumlar hava kanalında, askılarla.",
         'valf adası (12 valf) · hava kanalı + askılar · hava hortumları (yeşil)'); no += 1
    # 13 servis sacı kapanır
    t0 = t
    olay(t, 'Servis sacı (pano + kartlar + filtre üstünde) arkadan gelir — 17 × ISO 7380 M5 yan / tavan / taban dönüşündeki PEM SP-M5\'lere')
    kam(t, ['dis_arka_servis'], (0, 0, -1), uzak=1.9)
    ofset(SERV, SV, t, t + 2.0)
    t += 2.6
    adim(no, 'Arka servis sacı kapanır', t0, t, "İç montaj bitince servis sacı alt montajıyla birlikte arkadan takılır. Bombe başlı M5 vidalar gövde dönüşlerindeki PEM somunlara girer; bakımda sac tek parça çıkar (evaporatör bakır bağlantısı ayrılmalı — açık madde).",
         'servis sacı + pano + kartlar + filtre · 17 × ISO 7380 M5'); no += 1
    # 14 UNO
    t0 = t
    uno_ad = [('TOPPING/Kıyma', 'kıyma'), ('TOPPING/Kuşbaşı', 'kuşbaşı'), ('TOPPING/Sos', 'sos'), ('TOPPING/Harç', 'harç')]
    for kod, ad in uno_ad:
        g = AN(mekk(kod))
        h = [a for a in g if ANA_BILGI[a]['dugum'].endswith(('__hortum_gida', '__yayici_sabit_baglanti', '__conta'))]
        gv = [a for a in g if a not in h]
        olay(t, 'UNO · %s: hazne + piston + valf önden, raf burcuna · gıda hortumu + yayıcı' % ad)
        kam(t, g, (0, 0.2, 1))
        t = gel(gv, (0, 0, 0.8), t, 1.2) + 0.1
        t = gel(h, (0, -0.2, 0.2), t, 0.7, 0.1) + 0.2
    adim(no, "UNO'lar (4) + hortumlar + yayıcılar", t0, t + 0.3, "Dört dozaj ünitesi (kıyma, kuşbaşı, sos, harç) soğuk odaya önden girer, raf burçlarına oturur; pistonlar valf adasının hortumlarına bağlanır. Gıda hortumu ve yayıcı tabla üstüne düşen dozu dağıtır.",
         'UNO kıyma · UNO kuşbaşı · UNO sos · UNO harç · gıda hortumları · yayıcılar'); t += 0.3; no += 1
    # 15 kasetler
    t0 = t
    for kod, ad in (('TOPPING/Kaşar', 'kaşar'), ('TOPPING/Sucuk', 'sucuk')):
        g = AN(mekk(kod))
        olay(t, '%s kaseti dil kanalından raya sürülür — kaplin motora geçer, mandal kilitler' % ad.capitalize())
        kam(t, g, (0, 0.2, 1))
        t = gel(g, (0, 0, 0.75), t, 1.8) + 0.3
    adim(no, 'Kaşar + sucuk kasetleri', t0, t + 0.2, "Kasetler hazır ünite olarak önden, raftaki dil kanalına oturan raydan sürülür; arkadaki motorun kaplinine geçer, mandal kilitler. Sökmek için mandal açılır, kaset çekilir (motor yerinde kalır).",
         'kaşar kaseti · sucuk kaseti · mandal'); t += 0.2; no += 1
    # 16 tabla + X ekseni
    t0 = t
    tb = AN(mekk('TOPPING/Tabla'))
    ray = [a for a in tb if not ANA_BILGI[a]['dugum'].endswith(('__ARABA', '__TABLA')) and 'TABLA' not in ANA_BILGI[a]['dugum']]
    arb = [a for a in tb if a not in ray]
    olay(t, 'X ekseni: ray tabanı + lineer ray + tahrik motoru — tabanı 4 × M6 kaide plakasındaki PEM\'lere (A geçiş ağzından)')
    kam(t, tb, (0, 0.3, 1))
    t = gel(ray, (0, 0, 0.7), t, 1.4) + 0.1
    t = gel(R(r'^arayuz_kaide_M6_[2-5]$'), (0, 0.12, 0), t, 0.5, 0.1) + 0.1
    olay(t, 'Araba + bantlı tabla raya')
    t = gel(arb, (0, 0.35, 0), t, 1.2) + 0.5
    adim(no, 'Tabla + X ekseni', t0, t, "X ekseni rayı A'dan TOPPING'e uzanır; tabanı kaide plakasına 4 × M6. Tahrik motoru TOPPING ucundadır (A'da kablo yok). Araba ve bantlı tabla en son raya takılır.",
         'ray tabanı + lineer ray · X motoru · 4 × M6 · araba · tabla'); no += 1
    # 17 kapaklar
    t0 = t
    kp = AN(lambda a, b, lo, hi: b['mek'] == 'TOPPING/Gövde')
    gvd = [a for a in kp if not ANA_BILGI[a]['kpk'] and P[a]['m'] != 'kapak_s']
    kan = [a for a in kp if a not in gvd]
    olay(t, 'Gizli menteşe gövdeleri + bas-aç mandalları ön kasaya')
    kam(t, kp, (0, 0.1, 1))
    t = gel_say(gvd, (0, 0, 0.15), t, 0.6, 1.2) + 0.1
    olay(t, 'Kanatlar K1 / K2 (çift cidar + PU + fitil) önden, menteşelere')
    t = gel(kan, (0, 0, 0.6), t, 1.4) + 0.5
    adim(no, 'Kapaklar (kanatlar)', t0, t, "Ön kanatlar en son: menteşe gövdeleri ve bas-aç mandalları ön kasaya, kanatlar (çift cidar + PU + fitil, menfezli) önden asılır.",
         'menteşe gövdeleri · bas-aç · kanat K1 · kanat K2'); no += 1
    # 18 saha
    t0 = t
    GHOST_T.append(round(t, 2))
    GHOST.extend([[0.736, 4.4, 0.106, 0.788, -0.83, 0.039], [0.736, 1.436, 0.788, 2.2, -0.83, 0.079], [2.5, 4.0, 0.788, 2.2, -0.83, 0.079]])
    olay(t, 'Sahada: kaide B tavanına 4 × M8 + DIN 9021 (kaide borusunun içinden) — A, B, F silik')
    kam(t, R(r'^arayuz_kb'), (0, 1, 0.3))
    t = gel(R(r'^arayuz_kb_\d+_\d+_pul$'), (0, 0.12, 0), t, 0.5, 0.08)
    t = gel(R(r'^arayuz_kb_\d+_\d+$'), (0, 0.18, 0), t, 0.6, 0.08) + 0.2
    olay(t, 'TOPPING ↔ F: 4 × ISO 4762 M8 × 16, F içinden sağ yandaki PEM SP-M8\'lere')
    kam(t, R(r'^arayuz_m8_F'), (1, 0, 0))
    t = gel(R(r'^arayuz_m8_F_.*_pul$'), (0.08, 0, 0), t, 0.5, 0.1)
    t = gel(R(r'^arayuz_m8_F_\d+_\d+$'), (0.1, 0, 0), t, 0.6, 0.1) + 0.3
    olay(t, 'TOPPING tamam'); kam(t, None); t += 2.5
    adim(no, 'Saha · B, A ve F bağlantısı', t0, t, "TOPPING kaidesi B tavanına 4 × M8 ile bağlanır. A, TOPPING'in sol yanındaki PEM'lere A içinden (A sayfasında); F sağ yandaki PEM'lere F içinden 4 × M8.",
         '4 × M8 + DIN 9021 (B) · 4 × M8 × 16 (F)')
    for a in R(r'^arayuz_'): GIZLI.add(a)
    return t


def seq_F():
    global SAHIP
    BASLIK.update(kod='F')
    SECIM[:] = [('onyuz_kapak_F_sol_dis_tava', 2), ('onyuz_kapak_F_sol_alt_kayit', 2), ('onyuz_kapak_F_sol_ust_kayit', 2), ('davlumbaz_atis_kanali_L1', 2),
                ('baca_ic_kanal_L1', 2), ('baca_dis_kilif_L1', 2), ('baca_ust_flansi_on', 2), ('baca_alt_kapama_lamasi_on', 2)]
    for a in R(r'^arayuz_|_mentese_\d+_vida_\d+$'): GIZLI.add(a)      # karşı parça U sacında / menteşe vidası menteşeyle gelir
    GHOST_T.append(0.0)
    GHOST.extend([[2.5, 4.0, 0.106, 0.788, -0.83, 0.039], [1.436, 2.5, 0.788, 2.2, -0.83, 0.079], [4.0, 4.4, 0.788, 1.862, -0.83, 0.079]])
    t = kartlar(0.0, 'davlumbaz atış kanalı 2 L · baca iç kanal 2 L + dış kılıf 2 L + 4 alt lama + 4 üst flanş · 2 ön kapak (dış tava + 2 omega + 2 kayıt + karşılık)')
    # 4 davlumbaz atış kanalı
    t4 = t
    olay(t, 'F üst kabini (U sayfası) ve komşular silik. Davlumbaz atış kanalı: iki L 1,5, boyuna dikiş — fırın üstünden baca ağzına')
    kam(t, R(r'^davlumbaz_'), (0, 0.3, 1))
    t = gel(R(r'^davlumbaz_atis_kanali_L\d$'), (0, 0, 0.6), t, 1.1, 0.25)
    t = kaynak(R(r'^davlumbaz_atis_kanali_.*kaynak'), t, 0.4, 0.1) + 0.4
    adim(4, 'Davlumbaz atış kanalı', t4, t, "Fırın buharı davlumbaz bölmesinden atış kanalıyla yukarı, bacaya gider. Kanal 296 × 196, iki L sacın boyuna kaynağıyla; üst ucu bacanın iç kanalına 30 mm teleskopik girer (yüksek sıcaklık silikonu).",
         'atış kanalı L1 + L2 · 2 boyuna dikiş')
    # 5 baca
    t5 = t
    olay(t, 'Baca iç kanalı (iki L 1,5) · taş yünü A1 sarılır')
    kam(t, R(r'^baca_'), (0, 0.4, 1))
    t = gel(R(r'^baca_ic_kanal_L\d$'), (0, 0.5, 0), t, 1.0, 0.2)
    t = kaynak(R(r'^baca_ic_kanal_.*kaynak'), t, 0.4, 0.1) + 0.1
    t = yerinde(R(r'^yalitim_baca'), t, 1.0) + 0.1
    olay(t, 'Dış kılıf (iki L 0,8) taş yününün üstüne · alt kapama lamaları + köşe silikonu')
    t = gel(R(r'^baca_dis_kilif_L\d$'), (0, 0.5, 0), t, 1.0, 0.2)
    t = kaynak(R(r'^baca_dis_kilif_.*kaynak'), t, 0.4, 0.1)
    t = gel(R(r'^baca_alt_kapama_lamasi_'), (0, -0.2, 0), t, 0.7, 0.1)
    t = yerinde(R(r'^baca_alt_kose_silikonu'), t, 0.3, 0.05) + 0.1
    olay(t, "Üst flanş 4 lama (3 mm) + 8 PEM SP-M6 kör başlıklı — U_F tavanına 8 × M6 (U sayfası)")
    t = gel(R(r'^baca_ust_flansi_'), (0, 0.3, 0), t, 0.8, 0.1)
    t = gel(R(r'^baca_flans_pem_M6_\d$'), (0, 0.15, 0), t, 0.5, 0.03)
    t = gel(R(r'^baca_flans_pem_M6_\d_kapak$'), (0, 0.15, 0), t, 0.5, 0.03) + 0.4
    adim(5, 'Baca · iç kanal, taş yünü, dış kılıf, flanş', t5, t, "Baca çift cidarlıdır: iç kanal 1,5 + taş yünü A1 + dış kılıf 0,8 (dışı elle tutulur sıcaklıkta). Altta kapama lamaları yalıtımı örter; üstte 3 mm flanş U_F tavanına 8 × M6 ile bağlanır.",
         'iç kanal 2 L · taş yünü · dış kılıf 2 L · 4 alt lama + silikon · 4 flanş lamaya 8 PEM SP-M6')
    # 6 ön kapak alt montajı (tezgâhta)
    t6 = t
    ST = (0, 0, 0.9)
    KAPS = {}
    for taraf in ('sol', 'sag'):
        k = 'onyuz_kapak_F_%s' % taraf
        KAP = sorted(a for a in P if a.startswith(k) and a not in GIZLI)
        KAPS[taraf] = KAP
        olay(t, 'Ön kapak %s (tezgâhta, önde): dış tava 1,5 — bindirme köşeler TIG · 36 panjur yarığı' % ('sol' if taraf == 'sol' else 'sağ'))
        kam_k(t, [k + '_dis_tava'], ST, uzak=1.6, yon=(0.4, 0.35, 1.0))
        t = gel([k + '_dis_tava'], (0, 0.3, 0), t, 1.0) + 0.1
        t = kaynak(R(r'^%s_dis_tava_kose_kaynagi' % k), t, 0.3, 0.08) + 0.1
        olay(t, '2 omega (hazır haddeli 40 × 15) + alt / üst kayıt (U 1,5) içeriden · menteşe PEM SP-M5 · bas-aç karşılığı')
        t = gel(R(r'^%s_omega_\d$' % k), (0, 0, -0.15), t, 0.7, 0.15)
        t = gel(R(r'^%s_(alt|ust)_kayit$' % k), (0, 0, -0.15), t, 0.7, 0.15)
        t = gel(R(r'^%s_mentese_\d+_pem_\d+$' % k), (0, 0, -0.06), t, 0.4, 0.04)
        t = gel(R(r'^%s_basac_karsilik$' % k), (0, 0, -0.08), t, 0.5) + 0.3
    adim(6, 'Ön kapaklar · tezgâhta alt montaj', t6, t, "İki ön kapak tezgâhta kurulur: dış tava 1,5 (bindirme köşe TIG, 36 panjur yarığı), içinde 2 omega ve alt / üst kayıt; menteşe PEM'leri ve bas-aç karşılığı. Kapaklar tezgâhta bekler, en son asılır.",
         'dış tava × 2 · 4 omega · 4 kayıt · 8 menteşe PEM SP-M5 · 2 bas-aç karşılığı · 8 köşe kaynağı')
    t = sac_tamam(t)
    no = 7
    # 7 TP10
    t0 = t
    fr = AN(lambda a, b, lo, hi: b['mek'] == 'F/Fırın' and P[a]['m'] not in ('fis', 'guc', 'bilgi', 'kanal'))
    olay(t, 'TP10 konveyör fırın (satın alınır, gövdesine dokunulmaz) önden B tavanındaki yerine sürülür')
    kam(t, fr, (0, 0.2, 1))
    t = gel(fr, (0, 0.05, 1.1), t, 2.6) + 0.5
    adim(no, 'TP10 fırın yerine', t0, t, "Fırın hazır cihazdır (TP10, kendi kabuğu + konveyör); yalnız yerine oturur. B tavanındaki ısı kalkanının üstüne önden sürülür, ayakları terazilenir.",
         'TP10 gövde · konveyör + tel bant · giriş / çıkış ruloları · çıkış plakası'); no += 1
    # 8 yükleme bandı
    t0 = t
    bd = AN(mekk('F/Yükleme bandı'))
    mt = [a for a in bd if ANA_BILGI[a]['dugum'].endswith(('__motor', '__aluminyum', '__koyu', '__sac')) and bbox([a])[1][1] > 1.09]
    olay(t, 'Yükleme bandı (PTFE bant + burun / tahrik ruloları) fırın girişinin içine')
    kam(t, bd, (0, 0.3, 1))
    t = gel([a for a in bd if a not in mt], (-0.5, 0, 0), t, 1.4) + 0.2
    olay(t, 'Bant motoru + braketi')
    t = gel(mt, (0, 0.25, 0), t, 0.9) + 0.5
    adim(no, 'Yükleme bandı + motoru', t0, t, "Yükleme bandı TOPPING tablasından gelen ürünü fırın konveyörüne verir; TP10 girişinin içinde, motoru üstte braketle.",
         'PTFE bant · burun + tahrik rulosu · bant motoru + braket'); no += 1
    # 9 davlumbaz fanı
    t0 = t
    dv = AN(lambda a, b, lo, hi: b['mek'] == 'F/Davlumbaz' and P[a]['m'] not in ('fis',))
    if dv:
        olay(t, 'Davlumbaz fanı + yağ filtresi bölmeye, atış kanalının altına')
        kam(t, dv, (0, 0.2, 1))
        t = gel(dv, (0, 0, 0.6), t, 1.2, 0.2) + 0.5
        adim(no, 'Davlumbaz fanı + filtre', t0, t, "Davlumbaz bölmesindeki fan ve filtre buharı atış kanalına basar.", 'fan · filtre'); no += 1
    # 10 elektrik
    t0 = t
    elk = AN(lambda a, b, lo, hi: b['mek'] in ('F/Elektrik', 'F/Fırın', 'F/Davlumbaz', 'F/Gövde', 'F/Hava') and P[a]['m'] in ('elektrik', 'kanal', 'guc', 'bilgi', 'fis')
             or (b['mek'] == 'F/Elektrik'))
    kutu = [a for a in elk if ANA_BILGI[a]['dugum'].startswith('ELK_ISTASYON__') and P[a]['m'] in ('elektrik', 'mekanizma', 'koyu')]
    kanal = [a for a in elk if P[a]['m'] == 'kanal']
    fis = [a for a in elk if P[a]['m'] == 'fis' or ANA_BILGI[a]['dugum'] in ('ELK_ZINCIR__paslanmaz', 'F_UST_KABIN__plastik')]
    fis = [a for a in fis if a not in kutu]
    guc = [a for a in elk if P[a]['m'] == 'guc' and a not in fis + kutu]
    bil = [a for a in elk if P[a]['m'] == 'bilgi' and a not in fis + kutu]
    rest = [a for a in elk if a not in kutu + kanal + fis + guc + bil]
    olay(t, 'F kutusu (sürücü + G/Ç + sigorta) arka alt köşeye, PEM saplamalara')
    kam(t, kutu + rest, (0, 0.2, -1))
    t = gel(kutu + rest, (0, 0, -0.5), t, 1.1, 0.12) + 0.2
    olay(t, 'İç kanallar arka duvar boyunca')
    kam(t, kanal, (0, 0.2, -1)); t = gel_say(kanal, (0, 0, -0.45), t, 1.0, 1.4) + 0.2
    olay(t, 'Güç kabloları (KIRMIZI) — fırın, bant motoru, fan, kompresör')
    kam(t, guc, (0, 0.2, -1)); t = gel_say(guc, (0, 0, -0.45), t, 1.0, 1.6) + 0.2
    olay(t, 'Bilgi kabloları (MAVİ) — sensör, EtherCAT / G/Ç')
    kam(t, bil, (0, 0.2, -1)); t = gel_say(bil, (0, 0, -0.45), t, 1.0, 1.6) + 0.2
    olay(t, 'Gömme fiş panelleri (Harting / M12) + rakorlar')
    kam(t, fis, (0, 0.2, -1)); t = gel_say(fis, (0, 0, -0.35), t, 0.9, 1.6) + 0.5
    adim(no, 'F kutusu + kanallar + kablolar + fiş panelleri', t0, t, "F'nin elektrik kutusu kendi gövdesinde (arka alt köşe). Kablolar kanal içinden: güç kırmızı, bilgi mavi. Komşu istasyonlara yalnız gömme fiş panellerinden bağlanılır.",
         'F kutusu · iç kanallar · güç (kırmızı) · bilgi (mavi) · fiş panelleri'); no += 1
    # 11 kompresör + hava
    t0 = t
    hv = AN(lambda a, b, lo, hi: b['mek'] == 'F/Hava' or (b['mek'] == 'F/Gövde' and b['dugum'] == 'F_UST_KABIN__paslanmaz'))
    kmp = [a for a in hv if ANA_BILGI[a]['dugum'].startswith(('HAVA_KOMPRESOR__kompresor', 'HAVA_KOMPRESOR__siyah', 'F_KOMP_AYAK'))]
    olay(t, 'Kompresör titreşim ayaklarıyla F üst kabin tabanındaki PEM\'lere (davlumbaz bölmesinin önünde)')
    kam(t, kmp, (0, 0.3, 1))
    t = gel(kmp, (0, 0.3, 0.4), t, 1.4) + 0.2
    olay(t, 'Hava hortumları (YEŞİL) + kelepçe / askı lamaları — kompresörden hat boyunca istasyonlara')
    rh = [a for a in hv if a not in kmp]
    kam(t, rh, (0, 0.2, -1)); t = gel_say(rh, (0, 0, -0.45), t, 1.1, 1.6) + 0.5
    adim(no, 'Kompresör + hava hattı', t0, t, "Hattın hava kaynağı kompresör F üst kabinindedir; hava hortumları kelepçe ve askı lamalarıyla arka kanal boyunca TOPPING, K ve E'ye gider.",
         'kompresör + ayaklar · hava hortumları (yeşil) · kelepçe + askı lamaları'); no += 1
    # 12 kapaklar
    t0 = t
    kp = AN(lambda a, b, lo, hi: b['mek'] == 'F/Gövde' and (b['kpk'] or P[a]['m'] == 'kapak_s'))
    olay(t, 'Menteşeler (gövde + kanat) ve gazlı yaylar + bilyeli braketler')
    kam(t, kp, (0, 0.1, 1))
    t = gel_say(kp, (0, 0, 0.3), t, 0.8, 1.2) + 0.2
    olay(t, 'Ön kapaklar tezgâhtan gelir — menteşelere asılır, gazlı yaya takılır, bas-aç ile kapanır')
    KAP = KAPS['sol'] + KAPS['sag']
    kam(t, KAP, (0, 0.1, 1), uzak=2.0)
    ofset(KAP, ST, t, t + 1.9)
    t += 2.4
    adim(no, 'Ön kapaklar', t0, t, "Kapaklar en son, iç montaj bittikten sonra asılır: alt kenardaki menteşeler, yanlarda gazlı yaylar, üstte bas-aç. Panjur yarıkları fırın bölmesinin havalandırmasıdır.",
         'menteşe × 4 · gazlı yay × 2 · ön kapak sol · ön kapak sağ'); no += 1
    kal = AN(lambda a, b, lo, hi: True)
    if kal:
        t0 = t; olay(t, 'Yedek pizza kutusu stoku (görsel)'); kam(t, kal, (0, 0.5, 1))
        t = gel(kal, (0, 0.3, 0.3), t, 1.0, 0.1) + 0.5
        adim(no, 'Ürün', t0, t, "Fırın üstündeki yedek pizza kutusu stoku (görsel).", 'pizza kutusu yedeği'); no += 1
    olay(t, 'F tamam'); kam(t, None); t += 2.0
    return t
