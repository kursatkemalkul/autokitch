# ---- 7 KURU BÖLME + SOĞUTMA GRUBU
adim('Kuru bölme + soğutma grubu', 'Soğutma cebi (lazerden çıkar, 3 kez bükülür, 4 somun preslenir) taşıyıcılara iner; soğutma grubu (hazır ürün) arkadan gelip cebe oturur. Ayırma perdesi ve teknik perdeler yerine girer, iki cıvata perdeden kaide plakasına. Kondenser kanalının alt braketi ve kanalı yerleşir; X ekseninin motoru yukarıdan sağ arka köşeye iner. Kuru bölme tabanı yukarıdan kanalın üstünden geçerek iner (kanal deliği açık); kanal geçiş kapağı sağdan sürülür, 2 vida.',
     'soğutma cebi + 4 somun · soğutma grubu · ayırma ve teknik perdeler · 2 cıvata · kanal braketi · kondenser kanalı · X motoru · kuru bölme tabanı · kanal kapağı + 2 vida')
kamera_genel(['sogutma_cebi', 'teknik_on_perde'], yon=(0.35, 0.6, -0.75), olcek=0.8)
t = koy('sogutma_cebi', AD(ARKA9, UST6), 'Soğutma cebi → cep taşıyıcılara (punta)', pem=sorted(PEM_SAC['sogutma_cebi']))
t = koy('sogutma_grubu', AD(ARKA9, UST6), 'Soğutma grubu (hazır ürün) → arkadan, cebe iner')
for a in ('ayirma_perdesi_cep_sol', 'teknik_on_perde', 'teknik_sag_perde'): t = koy(a, AD(ARKA9, UST6, ON9), '%s → yerine (punta)' % tr(a))
M6 = sorted(a for a in P if a.startswith('arayuz_kaide_M6'))
yakin(merkez(M6[0]), 0.3, yon=(0.4, 0.8, 0.5), tt=t)
t = sira_tak(M6, t, 40.0, 0.55, 0.25); olay(t - 0.5, '2 cıvata M6 × 12: teknik perdeden → dış taban → kaide plakasındaki somun'); t += 0.5
t = koy('kondenser_braketi', AD(UST6, ARKA9), 'Kondenser kanalı alt braketi → dış tabanın saplamalarına')
t = koy('kondenser_kanali', AD(ARKA9, UST6), 'Kondenser kanalı (dirsekli boru) → braketine')
t = koy('x_motor', AD(UST6, ARKA9, (700, 0, 0)), 'X ekseni motoru + braketi → sağ arka köşeye (X ekseni sonra soldan gelip motora bağlanır)')
kamera_genel(['kuru_bolme_tabani'], yon=(0.4, 0.8, -0.6), olcek=0.8)
t = koy('kuru_bolme_tabani', AD(UST6, ARKA9, lift=(300, 500)), 'Kuru bölme tabanı → yukarıdan iner, kanal borusu tabandaki delikten geçer (punta)', pem=sorted(PEM_SAC['kuru_bolme_tabani']))
yakin(merkez('kanal_gecis_kapagi'), 0.35, yon=(0.6, 0.6, -0.5), tt=t)
t = koy('kanal_gecis_kapagi', [YOL((250, 0, 0)), YOL((250, 0, 0), (0, 3, 0)), YOL((250, 20, 0))] + AD(UST6), 'Kanal geçiş kapağı → sağdan, yarığı borunun çevresine sürülür')
KKV = sorted(a for a in P if a.startswith('kanal_kapagi_') and a.endswith('_vida'))
t = sira_tak(KKV, t, 30.0, 0.45, 0.2); olay(t - 0.5, 'Kapak: 2 vida M5 → tabandaki preslenmiş somunlara'); t += 0.4
# ---- 8 SOĞUK ODA ARKA DUVARI
adim('Soğuk oda: taban + arka duvar', 'Soğuk oda alt sacı ve arka dış sacı yerine girer; 4 evaporatör kanal kovanı (iki L + boyuna kaynak) ağızlara; arka duvara POM geçiş blokları. Dış saca yapıştırıcı sürülür, ölçüsünde kesilmiş arka PU levhası önden bastırılır. Evaporatörler ayaklarıyla birlikte arkadan gelir; her ayak kuru bölme tabanına 1 vida ile.',
     'alt sac · arka dış sac · 4 kanal kovanı · POM geçiş blokları · yapıştırıcı · PU levha arka · 2 evaporatör + 4 ayak · 4 vida')
kamera_genel(['soguk_alt_sac', 'soguk_arka_dis_sac'], yon=(0.35, 0.5, 0.85), olcek=0.75)
t = koy('soguk_alt_sac', AD(ON9, ARKA9, UST6), 'Soğuk oda alt sacı → teknik perdelerin üstüne (punta)', pem=sorted(PEM_SAC['soguk_alt_sac']))
t = koy('soguk_arka_dis_sac', AD(ARKA9, ON9, UST6), 'Soğuk oda arka dış sacı → alt sac + yanlar (punta)', pem=sorted(PEM_SAC['soguk_arka_dis_sac']))
for k in range(4):
    for j in (1, 2):
        koy('evap_kanal_kovani_%d_L%d' % (k, j), AD(ON9), '%s → arka dış sacın ağzına' % tr('evap_kanal_kovani_%d_L%d' % (k, j)),
            grup_kaynak=(KAY('evap_kanal_kovani_%d_boyuna_kaynak' % k) if j == 2 else ()), sure_bekle=0.05)
    t += 0.4
t = bitti() + 0.2
for a in sorted(a for a in P if a.startswith('pom_gecis')): koy(a, AD(ON9, ARKA9), 'POM geçiş bloğu → arka duvara', sure_bekle=0.05)
t = bitti() + 0.3
kamera_genel(['pu_levha_arka'], yon=(0.25, 0.4, 0.9), olcek=0.7)
buyu('yapistirici_arka', t, 0.6); olay(t, 'Yapıştırıcı (YEŞİL) → arka dış sacın iç yüzüne'); t += 0.8
t = koy('pu_levha_arka', AD(ON9), 'PU levha arka (ölçüsünde kesilmiş, yan / tavan iç sacının flanş yivleri açık) → yapıştırıcıya bastırılır')
kamera_genel(['evaporator_L', 'evaporator_R'], yon=(0.35, 0.45, -0.85), olcek=0.8)
for nm, ay in (('evaporator_L', ['evaporator_ayagi_0', 'evaporator_ayagi_1']), ('evaporator_R', ['evaporator_ayagi_2', 'evaporator_ayagi_3'])):
    t = koy([nm] + ay, AD(ARKA9), 'Evaporatör kaseti (hazır ürün, ayakları kaynaklı) → arkadan kanal kovanı ağzına, ayaklar kuru bölme tabanına')
EAV = sorted(a for a in P if a.startswith('evaporator_ayak_') and a.endswith('_vida'))
yakin(merkez(EAV[0]), 0.3, yon=(0.4, 0.7, -0.6), tt=t)
t = sira_tak(EAV, t, 30.0, 0.45, 0.2); olay(t - 0.5, 'Her ayak: 1 vida M5 → kuru bölme tabanındaki preslenmiş somun (servis sacı ayrı sökülür)'); t += 0.4
# ---- 9 DIŞ YAN SOL + TAVAN
adim('Dış yan sol + dış tavan', 'Sol yan (A tarafı): lazerden çıkar, 1 kez bükülür, somunlar preslenir, iki kaynak burcu puntalanır → tabanın yan dönüşüne, içeriden kaynak; A tarafındaki 2 somunun iç yüzüne köpük kapağı. Dış tavan: lazer → 3 büküm → 5 kaynak burcu → yan sacların üstüne, kaynak.',
     'dış yan sol + somun / burç · köpük kapağı × 2 · dış tavan + 5 burç · kaynak')
kamera_genel(['dis_yan_sol', 'dis_taban'], yon=(-0.6, 0.45, 0.65), olcek=0.75)
t = koy('dis_yan_sol', AD((-700, 0, 0), UST6), 'Dış yan sol → dış tabanın yan dönüşüne (kaynak)', pem=sorted(PEM_SAC['dis_yan_sol']), grup_kaynak=PUNTA['yan_sol_taban'])
KK = sorted(a for a in P if a.endswith('kopuk_kapagi'))
yakin(merkez(KK[0]), 0.3, yon=(0.8, 0.3, 0.5), tt=t)
for i, a in enumerate(KK): tak(a, t + i * 0.2, 0.5, 40.0)
olay(t, 'Köpük kapağı × 2 → A tarafı somunlarının iç yüzüne'); t = bitti() + 0.3
kamera_genel(['dis_tavan', 'dis_yan_sol'], yon=(0.45, 0.85, 0.6), olcek=0.75)
t = koy('dis_tavan', AD(UST6), 'Dış tavan → yan sacların üstüne (kaynak)', pem=sorted(PEM_SAC['dis_tavan']), grup_kaynak=PUNTA['tavan_yanlar'])
# ---- 10 YALITIM + İÇ SAC (bükümlü, perçinli)
adim('Yalıtım levhaları + iç sac', 'Yüzey yüzey: dış saca yapıştırıcı, ölçüsünde kesilmiş PU levha (sol, sağ, tavan) bastırılır. İç sac TIG ile değil bükümlü kenarlarla bağlanır: sol ve sağ iç sac önden girer (arka kenarı arka levhanın yivine, üst kenarı tavan levhasının yivine); üst kenarlarının altına POM ısı kesici pullar; tavan iç sacı önden kayarak yanların üst kenarının altına; arka kenarlara pullar; arka iç sac en son önden. Kör perçinler içeriden (pul üstünden).',
     'yapıştırıcı × 3 · PU levha sol / sağ / tavan · iç sac sol / sağ / tavan / arka (bükümlü) · POM pul · kör perçin × 34')
for pu in ('pu_levha_sol', 'pu_levha_sag', 'pu_levha_tavan'):
    kamera_genel([pu], yon=(0.25, 0.4, 0.9), olcek=0.7)
    yk = 'yapistirici_' + pu.split('_')[-1]; buyu(yk, t, 0.6); olay(t, 'Yapıştırıcı (YEŞİL) → dış sacın iç yüzüne'); t += 0.8
    d = {'pu_levha_sol': (60, 0, 0), 'pu_levha_sag': (-60, 0, 0), 'pu_levha_tavan': (0, -60, 0)}[pu]
    t = koy(pu, [YOL(ON9, d), YOL(d)] + AD(ON9), '%s → yapıştırıcıya bastırılır' % P[pu]['ac'].split('(')[0].strip())
PUL = lambda pre: sorted(a for a in P if a.startswith('astar_percin_' + pre) and a.endswith('_pul'))
PER = lambda pre: sorted(a for a in P if a.startswith('astar_percin_' + pre) and not a.endswith('_pul'))
for ast in ('astar_sol', 'astar_sag'):
    kamera_genel([ast], yon=(0.3, 0.4, 0.9), olcek=0.75)
    t = koy(ast, AD(ON9, lift=(2, 5)), '%s (bükümlü kenarlar) → önden, arka ve üst kenarı levha yivlerine' % ('Sol iç sac' if ast.endswith('sol') else 'Sağ iç sac'))
kamera_genel(['astar_tavan'], yon=(0.3, -0.3, 0.9), olcek=0.7)
for i, a in enumerate(PUL('tavan_')): tak(a, t + i * 0.05, 0.4, 200.0)
olay(t, 'POM ısı kesici pul × %d → yan iç sacların üst kenarının altına' % len(PUL('tavan_'))); t = bitti() + 0.2
t = koy('astar_tavan', AD(ON9, lift=(-2, -4)), 'Tavan iç sacı → önden kayar, yanların üst kenarının altına (pullar arada)')
kamera_genel(['astar_arka'], yon=(0.25, 0.3, 0.9), olcek=0.7)
for i, a in enumerate(PUL('arka_')): tak(a, t + i * 0.04, 0.4, 300.0)
olay(t, 'POM ısı kesici pul × %d → yan / tavan iç sacının arka kenarlarına' % len(PUL('arka_'))); t = bitti() + 0.2
t = koy('astar_arka', AD(ON9), 'Arka iç sac → en son önden, kenar flanşlarının önüne')
yakin(merkez(PER('arka_sol')[0]), 0.35, yon=(0.6, 0.3, 0.75), tt=t)
t = sira_tak(PER('arka_') + PER('tavan_'), t, 25.0, 0.35, 0.05)
olay(t - 1.0, 'Kör perçin Ø3,2 × %d içeriden: iç sac → POM pul → komşu iç sacın flanşı (sızdırmaz kapalı uç)' % len(PER('arka_') + PER('tavan_'))); t += 0.4
kamera_genel(['astar_sol'], yon=(0.6, 0.4, 0.75), olcek=0.8)
BURC = sorted(a for a in P if a.startswith('pom_burc'))
for i, a in enumerate(BURC):
    e_ = np.asarray(P[a]['eks'], float); t_ = t + i * 0.08
    basla(a, -e_ * 80.0, t_); git(a, np.zeros(3), t_, 0.5); vurgu([a], t_ + 0.3, t_ + 1.2); YER[a] = t_ + 0.5; YERINDE.append(a)
olay(t, 'Raf askı burcu POM × 16 → iç sac ve levha deliklerinden içeriden (sıkı geçme)'); t = bitti() + 0.5
# ---- 11 RAF
adim('Raf, kovanlar, eşik', 'Raf köşebentleri ve 6 düşme kovanı alt saca; PU raf levhası yukarıdan kovanların üstünden iner; kaset kilit mandalları levhanın cebine; raf (3 mm, lazer → 4 büküm) üstüne kapanır, arka köşe dolgu kaynağı; kovan contaları raf deliklerine. Dil kanalları, eşik, yiv dolguları + köşe silikonu.',
     'raf köşebendi × 2 · düşme kovanı × 6 · PU raf levhası · kilit mandalı × 2 · raf · kovan contası · dil kanalı × 2 · eşik · yiv dolgusu · silikon')
kamera_genel(['raf', 'raf_kosebendi_sol'], yon=(0.35, 0.7, 0.75), olcek=0.75)
for a in ('raf_kosebendi_sol', 'raf_kosebendi_sag'): koy(a, AD(ON9, UST6), '%s → alt saca (punta)' % tr(a))
t = bitti()
for a in ('dusme_kovani_kiyma_L1', 'dusme_kovani_kiyma_L2', 'dusme_kovani_kusbasi_L1', 'dusme_kovani_kusbasi_L2'):
    koy(a, AD(ON9, UST6), '%s → alt sacın deliğine' % tr(a), grup_kaynak=(KAY(a[:-3] + '_boyuna_kaynak') if a.endswith('L2') else ()), sure_bekle=0.05)
for a in ('dusme_kovani_sos', 'dusme_kovani_harc', 'dusme_kovani_kasar', 'dusme_kovani_sucuk'):
    koy(a, AD(ON9, UST6), 'Düşme kovanı → alt sacın deliğine', sure_bekle=0.05)
t = bitti() + 0.2
t = koy('pu_raf_esik', AD(UST6, ON9, lift=(100, 300, 500)), 'PU raf levhası → kovanların üstünden alt saca')
for ad in ('kasar', 'sucuk'): koy('kaset_%s_mandal' % ad, AD(UST6), 'Kaset kilit mandalı → levhanın cebine', sure_bekle=0.05)
t = bitti()
t = koy('raf', AD(UST6, ON9, lift=(60, 100, 300, 500)), 'Raf → PU levhanın üstüne, kenarları köşebentlere (punta)', pem=sorted(PEM_SAC['raf']), grup_kaynak=KAY('raf_arka_kose_dolgusu'))
for a in sorted(a for a in P if a.endswith('_conta') and a.startswith(('kaset_', 'uno_'))): koy(a, AD(UST6), 'Kovan contası → raf deliğine', sure_bekle=0.03)
t = bitti()
kamera_genel(['soguk_esik', 'dil_kanali_kasar'], yon=(0.3, 0.6, 0.9), olcek=0.7)
for a in ('dil_kanali_kasar', 'dil_kanali_sucuk'): t = koy(a, AD(ON9, UST6), '%s → rafın kesiğine' % tr(a))
t = koy('soguk_esik', AD(ON9, UST6), 'Eşik → rafın ön kenarına', grup_kaynak=KAY('raf_esik_yiv') + KAY('esik_on_yiv'))
for k in sorted(a for a in P if a.startswith('dil_kesik_kose_silikonu')): buyu(k, t, 0.4)
olay(t, 'Yiv dolgusu kaynak + taşlama · eşik kesiği köşe silikonu'); t += 0.9
# ---- UNO ÖN + KASET + ÜST RAF + ÇERÇEVE
adim('UNO\'lar, kasetler, üst raf, ön çerçeve', 'Kaset rayları raf saplamalarına. Kıyma ve kuşbaşı UNO\'su önden gelip rafa iner. Üst raf köşebentlerine. Sos ve harç UNO\'su önden üst rafa oturur; çıkış borusu + yayıcı alttan kovana takılır, gıda hortumu üst raf deliğinden iner, kelepçeyle boruya bağlanır. Kaşar / sucuk çıkış ağzı alttan kovana; kaset (hazır ürün) önden dil kanalında sürülür. Arkadan: POM duvar burçları, kaset motorları, UNO pnömatik silindirleri. Ön çerçeve: pullar iç sacın ön kenarlarına, çerçeve önden, havşa başlı perçinler çerçeveden; derz silikonu.',
     'kaset rayı × 2 · UNO × 4 · üst raf · çıkış borusu × 2 + hortum + kelepçe · kaşar / sucuk çıkış ağzı + kaset · POM burç · motor × 2 · UNO silindiri × 4 · pul × 20 · ön çerçeve · havşa perçin × 20 · derz silikonu')
kamera_genel(['uno_kiyma_on', 'uno_sos_on', 'kaset_kasar'], yon=(0.3, 0.45, 0.9), olcek=0.9)
ALT = [YOL((0, -150, 0)), YOL((0, 0, 700), (0, -150, 0)), YOL((0, 0, 700), (0, -120, 0))]
INIS = dict(lift=(110, 120, 130, 140), yan=())
for ad in ('kasar', 'sucuk'): t = koy('kaset_ray_' + ad, AD(ON9, lift=(15, 20, 30)), 'Kaset rayı → raf saplamalarına')
for ad in ('kiyma', 'kusbasi'):
    t = koy('uno_%s_on' % ad, AD(ON9, **INIS), 'UNO %s → önden yukarıda gelir, rafa ve kovana iner' % {'kiyma': 'kıyma', 'kusbasi': 'kuşbaşı'}[ad])
kamera_genel(['ust_raf'], yon=(0.3, 0.5, 0.9), olcek=0.8)
for a in ('ust_raf_kosebendi_sol', 'ust_raf_kosebendi_sag'): koy(a, AD(ON9), '%s → yan iç saclara (punta)' % tr(a))
t = bitti()
t = koy('ust_raf', AD(ON9, lift=(20, 40)), 'Üst raf → köşebentlere (punta)')
for ad in ('sos', 'harc'):
    t = koy('uno_%s_on' % ad, AD(ON9, lift=(2, 5, 10, 20)), 'UNO %s gövdesi → önden üst rafa' % {'sos': 'sos', 'harc': 'harç'}[ad])
    t = koy('uno_%s_cikis' % ad, ALT, 'UNO %s çıkış borusu + yayıcı → alttan kovana' % {'sos': 'sos', 'harc': 'harç'}[ad])
    t = buyu('uno_%s_hortum' % ad, t, 0.8); olay(t - 0.8, 'Gıda hortumu → üst raf deliğinden boruya iner')
    t = koy('uno_%s_kelepce' % ad, AD(ON9, UST6, lift=(5, 10)), 'Kelepçe → boru ile hortumu birleştirir (elle kapatılır)')
for ad in ('kasar', 'sucuk'):
    t = koy('kaset_%s_cikis' % ad, ALT, '%s çıkış ağzı → alttan kovana' % {'kasar': 'Kaşar', 'sucuk': 'Sucuk'}[ad])
    t = koy('kaset_' + ad, AD(ON9, lift=(5, 10)), '%s kaseti (hazır ürün) → önden dil kanalında sürülür, mandal kilitler' % {'kasar': 'Kaşar', 'sucuk': 'Sucuk'}[ad])
kamera_genel(['motor_kasar', 'uno_kiyma_arka', 'uno_sos_arka'], yon=(0.35, 0.45, -0.85), olcek=0.9)
for a in sorted(a for a in P if a.startswith('burc_')): koy(a, AD(ARKA9), 'POM duvar burcu → arkadan duvar deliğine (sıkı geçme)', sure_bekle=0.05)
t = bitti() + 0.2
for a in ('motor_kasar', 'motor_sucuk', 'uno_kiyma_arka', 'uno_kusbasi_arka', 'uno_sos_arka', 'uno_harc_arka'):
    t = koy(a, AD(ARKA9), ('Kaset motoru (hazır) → arkadan, kaplini burçtan kasete geçer' if a.startswith('motor') else 'UNO pnömatik silindiri → arkadan, mili burçtan geçip pistona vidalanır'))
kamera_genel(['on_cerceve_430'], yon=(0.3, 0.4, 0.9), olcek=0.75)
for i, a in enumerate(PUL('cerceve_')): tak(a, t + i * 0.04, 0.4, 200.0)
olay(t, 'POM ısı kesici pul × %d → iç sacın ön kenarlarına' % len(PUL('cerceve_'))); t = bitti() + 0.2
t = koy('on_cerceve_430', AD(ON9), 'Ön çerçeve 430 → soğuk oda önü (dış saca punta)') + 0.2
yakin(merkez(PER('cerceve_sol')[0]), 0.3, yon=(0.4, 0.3, 0.9), tt=t)
t = sira_tak(PER('cerceve_'), t, 25.0, 0.35, 0.05); olay(t - 1.0, 'Havşa başlı kör perçin Ø3,2 × %d çerçeveden (yüzeyle aynı düzlem, kapak fitili oturur)' % len(PER('cerceve_'))); t += 0.4
for a in sorted(a for a in P if a.startswith('derz_')): buyu(a, t, 0.8)
olay(t, 'Derz silikonu (YEŞİL) → gıda tarafı iç köşeler + çerçeve derzi'); t += 1.0
