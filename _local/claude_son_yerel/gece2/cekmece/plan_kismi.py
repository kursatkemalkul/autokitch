# PLAN (plan_v2.md ile birebir)
# =====================================================================================================================
KAM.append([0.0, K_GENEL[0], K_GENEL[1]])
t = 0.6
TEZ_UZAK = np.array([0.0, 0.0, 1150.0])
CUR['tezgah'] = -TEZ_UZAK.copy(); GOR['tezgah'] = 0.0          # montaj tezgâhı başta dolabın önünde; çekmece sürülünce +z 1150 kayar


def tezgaha(ad_l, ust=60.0, t0=None, hiz=900.0, grup=None, yan=(0, 0, 0)):
    """raftan / üretimden montaj tezgâhına (çekmecenin yerine): kaldır → üstüne → (yan) → indir"""
    grup = grup or [ad_l]; o = CUR[ad_l].copy(); dy = Y_SAFE - (P[ad_l]['V'][:, 1].min() + o[1])
    hedef = DR.copy(); yan = np.asarray(yan, float)
    nok = [o + [0, dy, 0], [hedef[0] + yan[0], o[1] + dy, hedef[2] + yan[2]], hedef + yan + [0, ust, 0], hedef + yan, hedef]
    return yolu(grup, nok, t0, hiz=hiz)


def rafa(ad_l, yer, t0, grup=None, hiz=900.0):
    grup = grup or [ad_l]; c = merkez(ad_l); o = CUR[ad_l].copy(); dy = Y_SAFE - (P[ad_l]['V'][:, 1].min() + o[1])
    h = np.array([yer[0] - c[0], BENCH_Y - P[ad_l]['V'][:, 1].min(), yer[2] - c[2]])
    return yolu(grup, [o + [0, dy, 0], [h[0], o[1] + dy, h[2]], h], t0, hiz=hiz, enaz=0.3)


def dolaba(ad_l, son_yaklasim, t0, hiz=650.0, grup=None):
    """raftan dolaba: kaldır → önde (arka yüzü z 200) hizala → içeri (−z) → son yaklaşım (vektör, son konuma göre)"""
    grup = grup or [ad_l]
    o = CUR[ad_l].copy(); son = np.asarray(son_yaklasim, float)
    dy = Y_SAFE - (P[ad_l]['V'][:, 1].min() + o[1])
    zon = 200.0 - (P[ad_l]['V'][:, 2].min())
    on = np.array([son[0], son[1], max(zon, son[2])])
    return yolu(grup, [o + [0, dy, 0], [on[0], o[1] + dy, on[2]], on, son, np.zeros(3)], t0, hiz=hiz)


KUCUK = [(x_, 0.0, z_) for z_ in (830.0, 940.0) for x_ in (2700.0, 2830.0, 2960.0, 3090.0, 3220.0, 3350.0)]
# ---------------- BÖLÜM 1 · ÜRETİM (küçük sac parçalar) ----------------
adim('Üretim: kızak köşebentleri (eklendi)',
     'Kızak bağlantı köşebendi 1,5 mm × 4: lazerde açınım (yatay kolda Ø4,5), abkantta dik kol 90° bükülür. Modelde kızak ile lama arasında bağ yoktu (yalnız 1 mm temas) — eklendi.',
     'köşebent × 4 · 1 büküm', K_URT)
for k in KOSE:
    t = uret(k['ad'], t, 'Köşebent %s-%s' % ('sol' if k['yan'] == 'sol' else 'sağ', k['ad'][-1]), sure_bukum=0.7); t = rafa(k['ad'], KUCUK.pop(0), t) + 0.05
adim('Üretim: motor braketi · sensör plakası',
     'Motor braketi 3 mm: lazerde göbek deliği Ø22,5, flanş kolunda 4 × M3 havşa (Ø31), tabanda 2 × M5 havşa; abkantta flanş kolu 90° bükülür. Sensör plakası 2 mm düz, 2 × Ø4,5.',
     'motor braketi (1 büküm) · sensör plakası (düz)', K_URT_YAKIN)
t = uret('motor_braketi', t, 'Motor braketi'); t = rafa('motor_braketi', KUCUK.pop(0), t) + 0.1
t = uret('sensor_plakasi', t, 'Sensör plakası'); t = rafa('sensor_plakasi', KUCUK.pop(0), t) + 0.1
adim('Üretim: avara kolu · sensör laması · kaynak',
     'Avara kolu 2 mm: lazer (ön flanşta 2 × Ø3,3 perçin deliği) → abkant: ön flanş, üst flanş. Sensör laması 2 mm: tek büküm (L). Kol kulağı lamaya TIG ile kaynaklanır, avara mili kola saplama kaynağıyla tutturulur.',
     'avara kolu (2 büküm) · sensör laması (1 büküm) · avara mili · TIG + saplama kaynağı', K_URT_YAKIN)
AV_YER = np.array([2780.0, 0.0, -230.0])
t = uret('avara_kolu', t, 'Avara kolu')
t = rafa('avara_kolu', AV_YER, t) + 0.05
hedef_k = CUR['avara_kolu'].copy()
t = uret('sensor_lamasi', t, 'Sensör laması')
o_l = CUR['sensor_lamasi'].copy(); dy = Y_SAFE - (P['sensor_lamasi']['V'][:, 1].min() + o_l[1])
t = yolu(['sensor_lamasi'], [o_l + [0, dy, 0], [hedef_k[0], o_l[1] + dy, hedef_k[2]], hedef_k + [0, 30, 0], hedef_k], t, hiz=900) + 0.1
olay(t - 0.8, 'Sensör laması kol kulağının altına')
basla('avara_mili', hedef_k + [60, 0, 0], t); t = yolu(['avara_mili'], [hedef_k], t, hiz=200); vurgu(['avara_mili'], t - 0.3, t + 0.6)
for a in ('kaynak_avara', 'kaynak_avara_mili'):
    kaynak_yap(a, t); CUR[a] = hedef_k.copy()
olay(t, 'TIG: kol kulağı ↔ sensör laması · saplama kaynağı: avara mili ↔ kol'); t += 1.3
AVARA = ['avara_kolu', 'sensor_lamasi', 'avara_mili', 'kaynak_avara', 'kaynak_avara_mili']
# ---------------- BÖLÜM 2 · RAY ÜNİTESİ ----------------
adim('Ray ünitesi: iç eleman ayrılır',
     'Accuride DZ3832-0700 ray dış + ara + iç eleman bir arada gelir. İç eleman (kızak) kilit dili basılarak ray ekseni boyunca öne çekilip ayrılır; çekmeceye takılacak.',
     'ray ünitesi sol / sağ (katalog) · iç eleman ayrılır', K_URT)
RAY_YER = {'sol': np.array([2950.0, 0.0, -330.0]), 'sag': np.array([3050.0, 0.0, -330.0])}
for yan in ('sol', 'sag'):
    grp = ['sabit_ray_' + yan, 'ara_ray_' + yan, 'kizak_' + yan]
    c_ = merkez('sabit_ray_' + yan); o_ = np.array([RAY_YER[yan][0] - c_[0], BENCH_Y - P['sabit_ray_' + yan]['V'][:, 1].min(), RAY_YER[yan][2] - c_[2]])
    for a in grp: basla(a, o_ + [0, 260.0, 0], t)
    t = yolu(grp, [o_], t, hiz=600) + 0.1
    t = yolu(['kizak_' + yan], [CUR['kizak_' + yan] + [0, 0, 720]], t, hiz=600); olay(t - 1.2, 'İç eleman (kızak) ray ekseni boyunca öne çekilip ayrılır'); t += 0.15
# ---------------- BÖLÜM 3 · DOLAP İÇİ ----------------
adim('Motor braketi arka duvara',
     'Motor braketi raftan alınır, ön çerçeve açıklığından bölmeye girer, tabanı arka duvara oturur: 2 × DIN 7991 M5 × 6 havşa vida arka iç sacdaki PEM SP-M5\'lere. Vidalar önce: motor takılınca taban vidaları motorun altında kalır.',
     'motor braketi · 2 × DIN 7991 M5 × 6 → PEM SP-M5 (arka iç sac)', K_ARKA)
t = dolaba('motor_braketi', (0, 0, 25), t); vurgu(['motor_braketi'], t - 0.4, t + 0.5)
kam(t, K_ARKA_YAKIN)
for i in (1, 2): t = tak('vida_braket_%d' % i, t, 0.8) + 0.1
olay(t - 1.8, 'Motor braketi: 2 × DIN 7991 M5 × 6 → PEM SP-M5')
t += 0.3
adim('Motor braketine (ekseni boyunca)',
     'Step motor önden girer, ekseni boyunca −x yönünde sürülür: redüktör göbeği braketin Ø22,5 deliğine, mil karşı tarafa geçer. 4 × DIN 7991 M3 × 6 havşa vida kasnak tarafından redüktör yüzündeki M3 dişlere. Sütunun dikey kablo kanalı tahrikler takıldıktan sonra gelir (bu animasyonda yok).',
     'step motor · 4 × DIN 7991 M3 × 6', K_ARKA)
basla('motor', np.array([24.0, Y_SAFE - P['motor']['V'][:, 1].min(), 980.0]), t)
t = yolu(['motor'], [[24.0, 0, 980.0], [24.0, 0, 0], [0, 0, 0]], t, hiz=600); vurgu(['motor'], t - 0.5, t + 0.5); olay(t - 1.0, 'Motor ekseni boyunca braketine sürülür')
kam(t, K_ARKA_YAKIN)
for i in range(1, 5): t = tak('vida_motor_%d' % i, t, 0.6) + 0.05
olay(t - 2.6, 'Motor: 4 × DIN 7991 M3 × 6 (redüktör yüzü)')
adim('Motor kasnağı · setskur',
     'GT3 motor kasnağı mil ekseninde (+x) mile geçer; DIN 913 M3 setskur önden milin düz yüzüne sıkılır. Sol ray henüz yok: kasnak soldan geçer.',
     'GT3 motor kasnağı · DIN 913 M3 × 4', K_ARKA_YAKIN)
basla('arka_kasnak', np.array([-14.5, Y_SAFE - P['arka_kasnak']['V'][:, 1].min(), 980.0]), t)
t = yolu(['arka_kasnak'], [[-14.5, 0, 980.0], [-14.5, 0, 0], [0, 0, 0]], t, hiz=600); vurgu(['arka_kasnak'], t - 0.4, t + 0.4)
t = tak('setskur', t, 0.6) + 0.2
adim('Sensör plakası',
     'Sensör plakası arka duvara: 2 × ISO 7380 M4 × 6 → arka iç sacdaki PEM SP-M4.',
     'sensör plakası · 2 × ISO 7380 M4 × 6', K_ARKA_YAKIN)
t = dolaba('sensor_plakasi', (0, 0, 20), t)
for i in (1, 2): t = tak('vida_sensor_%d' % i, t, 0.6) + 0.05
adim('Ray üniteleri bölme saclarına',
     'Sol ve sağ ray ünitesi (dış + ara eleman) önden çerçeve açıklığından girer, yana kayıp bölme sacına yaslanır. Her ray 3 × DIN 7991 M5 × 6 havşa vidayla, ara elemanın erişim deliklerinden, bölmedeki PEM SP-M5\'lere vidalanır.',
     'ray ünitesi sol / sağ · 6 × DIN 7991 M5 × 6 → PEM SP-M5', K_RAY)
for yan, sx in (('sol', 10.0), ('sag', -9.0)):
    t = dolaba('sabit_ray_' + yan, (sx, 0, 0), t, grup=['sabit_ray_' + yan, 'ara_ray_' + yan], hiz=800) + 0.05
kam(t, K_VIDA)
for k_ in (1, 2, 3):
    EL[VIDA_RAY[k_ - 1]] = dict(eks=np.array([-1.0, 0, 0]), yol=40.0); EL[VIDA_RAY[k_ + 2]] = dict(eks=np.array([1.0, 0, 0]), yol=40.0)
    t0 = t; tak(VIDA_RAY[k_ - 1], t0, 0.6); t = tak(VIDA_RAY[k_ + 2], t0, 0.6) + 0.1
olay(t - 2.1, 'Ray vidaları: 3 + 3 × DIN 7991 M5 × 6, kendi eksenlerinde')
adim('Avara ünitesi · perçin · avara kasnağı · reed',
     'Kaynaklı avara ünitesi (kol + sensör laması + mil) 21 mm alçaktan açıklıktan girer, içeride sola kayar, yükselip ön flanşıyla çerçevenin arkasına oturur: 2 × kör perçin Ø3,2 önden. GT3 avara kasnağı mil ekseninde (−x) mile geçer (mil ucunda E segman payı modelde yok — açık). İki reed sensör lamanın altına yandan oturur (bağlantı deliği modelde yok — açık).',
     'avara ünitesi · 2 × kör perçin Ø3,2 · GT3 avara kasnağı · reed × 2', K_SOL_ON)
o_a = CUR['avara_kolu'].copy()
zon = 200.0 - P['sensor_lamasi']['V'][:, 2].min()
t = yolu(AVARA, [o_a + [0, Y_SAFE - 480, 0], [10.0, o_a[1] + Y_SAFE - 480, zon], [10.0, -21.0, zon], [10.0, -21.0, -2.0], [0, -21.0, -2.0], [0, 0, -2.0], [0, 0, 0]], t, hiz=700)
vurgu(['avara_kolu', 'sensor_lamasi'], t - 0.4, t + 0.5)
for i in (1, 2): t = tak('percin_%d' % i, t, 0.6) + 0.05
olay(t - 1.3, 'Avara ünitesi: 2 × kör perçin Ø3,2 (çerçeve önünden)')
basla('avara_kasnagi', np.array([40.0, Y_SAFE - P['avara_kasnagi']['V'][:, 1].min(), 200.0 + 18.0]), t)
t = yolu(['avara_kasnagi'], [[40.0, 0, 218.0], [40.0, 0, 0], [0, 0, 0]], t, hiz=400); vurgu(['avara_kasnagi'], t - 0.4, t + 0.5)
for a in ('reed_arka', 'reed_on'):
    basla(a, np.array([20.0, 0, 0]), t); git(a, np.zeros(3), t, 0.7); vurgu([a], t + 0.4, t + 1.1)
t += 0.9
# ---------------- BÖLÜM 4 · ÇEKMECE KUTUSU (üretim → montaj tezgâhı) ----------------
adim('Kutu sacları: lazer → tezgâh → TIG',
     'Lazerde 5 düz sac (AISI 304): taban 2 mm, iki yan, arka, ön 1 mm. Taban montaj tezgâhına konur; yanlar tabanın üstüne oturup iç köşeden TIG ile kaynaklanır; arka ve ön iki yanın arasına girip tabana ve yanlara kaynaklanır.',
     'kutu tabanı 2 · yan sol / sağ 1 · arka 1 · ön 1 · 4 TIG dikişi', K_URT)
t = uret('kutu_taban', t, 'Kutu tabanı 2 mm'); kam(t, K_TEZ); t = tezgaha('kutu_taban', 40, t) + 0.1
kam(t, K_URT)
for ad, nm, yn in (('kutu_yan_sol', 'Kutu sol yanı', 'sol'), ('kutu_yan_sag', 'Kutu sağ yanı', 'sag')):
    t = uret(ad, t, nm); kam(t, K_TEZ); t = tezgaha(ad, 80, t) + 0.05
    k_ = 'kaynak_kutu_yan_' + yn; kaynak_yap(k_, t); CUR[k_] = DR.copy(); olay(t, 'TIG: %s yan ↔ taban (iç köşe)' % ('sol' if yn == 'sol' else 'sağ')); t += 1.0
    kam(t, K_URT)
for ad, nm, k_ in (('kutu_arka', 'Kutu arkası', 'kaynak_kutu_arka'), ('kutu_on', 'Kutu önü', 'kaynak_kutu_on')):
    t = uret(ad, t, nm); kam(t, K_TEZ); t = tezgaha(ad, 80, t) + 0.05
    kaynak_yap(k_, t); CUR[k_] = DR.copy(); olay(t, 'TIG: %s ↔ taban + iki yan' % ('arka' if 'arka' in ad else 'ön')); t += 1.0
    kam(t, K_URT)
adim('Kızak lamaları (kesim boyu, M4 dişli) → punta',
     'Lamalar 6 × 17,3 lamadan 616 boyda kesilir, köşebent vidaları için 2 × M4 dişli kör delik açılır; kutunun iki yanına puntalanır (4 nokta).',
     'lama sol / sağ · 2 × M4 dişli · punta 4 + 4', K_URT_YAKIN)
for yan, sx in (('sol', -70.0), ('sag', 70.0)):
    t = uret('lama_' + yan, t, 'Kızak laması %s' % ('sol' if yan == 'sol' else 'sağ')); kam(t, K_TEZ_SOL)
    t = tezgaha('lama_' + yan, 0, t, yan=(sx, 0, 0)) + 0.05
    kaynak_yap('punta_lama_' + yan, t, 0.6); CUR['punta_lama_' + yan] = DR.copy(); olay(t, 'Punta: lama ↔ kutu yanı (4 nokta)'); t += 0.8
    kam(t, K_URT_YAKIN)
adim('Ön bağlantı braketleri: abkant → punta',
     'Her braket 2 mm sacdan açınım olarak kesilir (flanşta 2 × Ø5,5), abkantta önce yan kol, sonra ön flanş 90° bükülür; kutu önüne puntalanır.',
     'ön braket sol / sağ · 2 büküm · punta 2 + 2', K_URT_YAKIN)
for yan in ('sol', 'sag'):
    t = uret('on_braket_' + yan, t, 'Ön braket %s' % ('sol' if yan == 'sol' else 'sağ')); kam(t, K_TEZ)
    t = tezgaha('on_braket_' + yan, 0, t, yan=(0, 0, 60)) + 0.05
    kaynak_yap('punta_braket_' + yan, t, 0.6); CUR['punta_braket_' + yan] = DR.copy(); olay(t, 'Punta: braket ↔ kutu önü'); t += 0.8
    kam(t, K_URT_YAKIN)
adim('Kayış çenesi: alt gövde TIG → kutuya TIG · üst çene · tepsi',
     'Alt çene, ara parça ve kol lamadan kesilir, TIG ile birleşir; alt gövde kutunun sol yanına TIG ile kaynaklanır. Üst çene (mıknatıs ayaklı) rafa — kayış takılınca M3 ile bağlanır. Silikon tepsi kutuya serbest oturur.',
     'çene alt gövde (TIG) · kutuya TIG · üst çene · silikon tepsi', K_URT_YAKIN)
t = uret('cene_alt', t, 'Kayış çenesi alt gövde')
kaynak_yap('kaynak_cene', t); CUR['kaynak_cene'] = CUR['cene_alt'].copy(); olay(t, 'TIG: kol ↔ alt çene · ara parça ↔ alt çene'); t += 1.0
kam(t, K_TEZ_SOL); t = tezgaha('cene_alt', 0, t, grup=['cene_alt', 'kaynak_cene'], yan=(-40, 0, 0)) + 0.05
kaynak_yap('kaynak_cene_kutu', t); CUR['kaynak_cene_kutu'] = DR.copy(); olay(t, 'TIG: çene kolu ↔ kutu sol yanı'); t += 1.0
kam(t, K_URT_YAKIN)
t = uret('cene_ust', t, 'Kayış çenesi üst'); t = rafa('cene_ust', KUCUK.pop(0), t) + 0.1
kam(t, K_TEZ)
basla('silikon_tepsi', DR + np.array([0, 160.0, 0]), t); git('silikon_tepsi', DR, t, 1.0); olay(t, 'Silikon tepsi kutuya serbest oturur'); t += 1.2
# ---------------- BÖLÜM 5 · ÇEKMECE TAMAMLANIR + DOLABA ----------------
adim('Tezgâh: köşebentler · kızaklar',
     'Köşebentler lamanın üstüne ISO 7380 M4 × 6 ile vidalanır (lamadaki M4 dişe). Kızaklar (iç eleman) köşebentlerin dik koluna oturur ve puntalanır (ÖNERİ: modelde kızak ile lama arasında bağ yoktu — Kemal kararı).',
     'köşebent × 4 + 4 × ISO 7380 M4 × 6 · kızak × 2 (punta 2 × 2)', K_TEZ_SOL)
for k in KOSE:
    t = tezgaha(k['ad'], 40, t, hiz=1100)
    a = 'vida_' + k['ad']; basla(a, DR + np.array([0, 30.0, 0]), t); git(a, DR, t, 0.5); vurgu([a], t + 0.3, t + 1.0); t += 0.6
olay(t - 4.5, 'Köşebentler lamalara: ISO 7380 M4 × 6')
for yan, sx in (('sol', -1.0), ('sag', 1.0)):
    t = tezgaha('kizak_' + yan, 0, t, hiz=1000, yan=(sx * 40, 0, 0))
    for k in KOSE:
        if k['yan'] == yan: kaynak_yap('punta_' + k['ad'], t, 0.5); CUR['punta_' + k['ad']] = DR.copy()
    olay(t, 'Kızak köşebentlere puntalanır (öneri)'); t += 0.7
CEKMECE = (['kutu_taban', 'kutu_yan_sol', 'kutu_yan_sag', 'kutu_arka', 'kutu_on', 'kaynak_kutu_yan_sol', 'kaynak_kutu_yan_sag', 'kaynak_kutu_arka', 'kaynak_kutu_on',
            'lama_sol', 'lama_sag', 'punta_lama_sol', 'punta_lama_sag', 'kizak_sol', 'kizak_sag', 'cene_alt', 'kaynak_cene', 'kaynak_cene_kutu',
            'on_braket_sol', 'on_braket_sag', 'punta_braket_sol', 'punta_braket_sag', 'silikon_tepsi']
           + [k['ad'] for k in KOSE] + ['vida_' + k['ad'] for k in KOSE] + ['punta_' + k['ad'] for k in KOSE])
adim('Çekmece raylara sürülür',
     'Çekmece tezgâhtan ray ekseni boyunca, düz bir çizgide içeri sürülür: kızaklar ara elemanların bilyalı kafesine geçer. Çekmece arka konumda durur; montaj tezgâhı çekilir.',
     'çekmece grubu · 900 mm sürme · ray ekseni z', K_SUR)
t = yolu(CEKMECE, [np.zeros(3)], t, hiz=170.0) + 0.3
olay(t - 5.6, 'Çekmece ray ekseni boyunca sürülür — kızak ara elemanın içinde')
git('tezgah', np.zeros(3), t, 2.0); olay(t, 'Montaj tezgâhı (tekerlekli) öne çekilir'); t += 2.2
adim('Kayış · üst çene · mıknatıs',
     'GT3 kayış motor kasnağı ile avara kasnağına sarılır, üst kolu alt çenenin üstüne yatar. Üst çene üstten gelir: 2 × ISO 7380 M3 × 10 + altta 2 × ISO 4032 M3. Mıknatıs ayağa oturur (57135\'in montaj yüzü modelde yok — açık).',
     'GT3 kayış (sarılır) · üst çene · 2 × ISO 7380 M3 × 10 · 2 × ISO 4032 M3 · mıknatıs', K_ARKA)
basla('kayis', np.zeros(3), t); ISTISNA.add('kayis'); MF['kayis'] = dict(buyu=[round(t, 3), round(t + 1.8, 3)]); olay(t, 'GT3 kayış kasnaklara sarılır (istisna: sarılarak uzar)'); t += 2.0
t = dolaba('cene_ust', (0, 20, 0), t); vurgu(['cene_ust'], t - 0.4, t + 0.4)
kam(t, K_ARKA_YAKIN)
for i in (1, 2): t = tak('vida_cene_%d' % i, t, 0.5); t = tak('somun_cene_%d' % i, t, 0.5) + 0.05
basla('miknatis', np.array([0, 22.0, 0]), t); git('miknatis', np.zeros(3), t, 0.6); vurgu(['miknatis'], t + 0.3, t + 1.0); t += 0.8
# ---------------- BÖLÜM 6 · ÖN KAPAK ----------------
adim('Üretim: ön kapak (8 büküm) · iç panel + PEM',
     'Dış kabuk 1,5 mm: lazer → abkant 8 büküm (dört kenar, sonra dört arka dönüş). İç panel 1,0 mm: 4 delik, PEM FHS-M5-10 saplamalar preslenir. İç panel kabuğun arkasına yerleşir (fitil kanalı 6,4 arada); modelde PU köpük yok.',
     'dış kabuk 1,5 (8 büküm) · iç panel 1,0 · 4 × PEM FHS-M5-10', K_URT)
t = uret('kapak_dis', t, 'Kapak dış kabuğu', sure_bukum=0.75)
KP_YER = np.array([3000.0, 0.0, -300.0])
t = rafa('kapak_dis', KP_YER, t) + 0.1
h_d = CUR['kapak_dis'].copy()
PEMK = [('pem_kapak_%s_%d' % (k_, i + 1), 0, (0, 0, 1)) for k_ in STUD for i in range(2)]
t = uret('kapak_ic', t, 'Kapak iç paneli', pemler=PEMK, sure_bukum=0.75)
pem_seg_esle()
o_i = CUR['kapak_ic'].copy(); grp_i = ['kapak_ic'] + [p_[0] for p_ in PEMK]
dy = Y_SAFE - (P['kapak_ic']['V'][:, 1].min() + o_i[1])
t = yolu(grp_i, [o_i + [0, dy, 0], [h_d[0], o_i[1] + dy, h_d[2] - 260], h_d + [0, 0, -260], h_d], t, hiz=800) + 0.2
KAPAK = ['kapak_dis'] + grp_i
olay(t - 0.6, 'İç panel kabuğun arkasına yerleşir — saplamalar arkaya bakar')
adim('Ön kapak · fitil · somunlar',
     'Fitil (silikon) kapağın kanalına arkadan bastırılır. Kapak dolabın önüne gelir; PEM saplamaları braket flanşlarındaki deliklerden geçer. Her saplamaya U braketin açık yanından pul (DIN 125 M5) ve somun (ISO 4032 M5) takılır.',
     'fitil · ön kapak (saplamalar) · 4 × DIN 125 M5 · 4 × ISO 4032 M5', K_SON)
o_k2 = CUR['kapak_dis'].copy()
basla('on_panel', o_k2 + np.array([0, 0, -120.0]), t); t = yolu(['on_panel'], [o_k2], t, hiz=200); vurgu(['on_panel'], t - 0.4, t + 0.5)
olay(t - 0.8, 'Fitil kapak kanalına bastırılır')
KAPAK = KAPAK + ['on_panel']
o_k3 = CUR['kapak_dis'].copy(); dy = Y_SAFE - (P['kapak_dis']['V'][:, 1].min() + o_k3[1])
t = yolu(KAPAK, [o_k3 + [0, dy, 0], [0, o_k3[1] + dy, 400.0], [0, 0, 400.0], [0, 0, 0]], t, hiz=650); vurgu(['kapak_dis'], t - 0.5, t + 0.5)
olay(t - 1.0, 'Kapak: saplamalar braket flanşından geçer')
kam(t, K_SOL_ON)
for k_ in STUD:
    sx = 1.0 if k_ == 'sol' else -1.0
    for i in (1, 2):
        for tip, dz in (('pul', 12.0), ('somun', 7.0)):
            a = '%s_kapak_%s_%d' % (tip, k_, i)
            basla(a, np.array([sx * 30.0, 0, -dz]), t); git(a, np.array([0, 0, -dz]), t, 0.35); git(a, np.zeros(3), t + 0.35, 0.4); vurgu([a], t + 0.5, t + 1.1); t += 0.8
olay(t - 6.4, 'Saplamalara pul + somun (U braketin açık yanından)')
adim('Kablolar',
     'Reed sensör kabloları ve motor kablosu bölmedeki kablo kanalı boyunca arkaya çekilir (sütunun dikey kanalı tahrikler bittikten sonra).',
     'reed sensör kabloları · motor kablosu', K_ARKA)
for a in ('kablo_sensor', 'kablo_motor'):
    basla(a, np.zeros(3), t); ISTISNA.add(a); MF[a] = dict(buyu=[round(t, 3), round(t + 2.2, 3)])
olay(t, 'Kablolar kanal boyunca çekilir (istisna)'); t += 2.6
KAM.append([round(t, 3), K_SON[0], K_SON[1]]); t += 2.4
TOPLAM = round(t, 2)
