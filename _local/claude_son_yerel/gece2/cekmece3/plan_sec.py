# PLAN (plan_v3.md ile birebir) — tezgâh kutusu YOK: alt montajlar montaj alanında havada durur
# =====================================================================================================================
KAM.append([0.0, K_GENEL[0], K_GENEL[1]])
t = 0.6


def tezgaha(ad_l, ust=60.0, t0=None, hiz=900.0, grup=None, yan=(0, 0, 0)):
    """üretimden / raftan montaj alanına (çekmecenin yerine): kaldır → üstüne → (yan) → indir"""
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


def yakin(adlar, uz=0.20, yon=(0.55, 0.42, 0.72)):
    """birleşim yakın planı: parçaların o anki konumunun merkezi (m)"""
    L = [P[a]['V'] + CUR.get(a, np.zeros(3)) for a in adlar]
    X = np.vstack(L); c = (X.min(0) + X.max(0)) / 2000.0
    d = np.asarray(yon, float); d /= np.linalg.norm(d)
    return ((c + d * uz).round(3).tolist(), c.round(3).tolist())


def birlesim(tt, adlar, metin, uz=0.20, yon=(0.55, 0.42, 0.72)):
    kam(tt, yakin(adlar, uz, yon)); olay(tt, metin)


KUCUK = [(x_, 0.0, z_) for z_ in (830.0, 940.0) for x_ in (2860.0, 2990.0, 3120.0, 3250.0, 3380.0, 3510.0)]
# ---------------- BÖLÜM 1 · ÜRETİM (küçük sac parçalar) ----------------
adim('Üretim: kızak köşebentleri',
     'Kızak köşebendi 1,5 mm (AISI 304) × 4: lazerde açınım (yatay kolda Ø4,5 delik), abkantta dik kol 90° bükülür. Görevi: kızağı (rayın iç elemanı) çekmecenin lamasına bağlamak.',
     'köşebent × 4 · 1,5 mm · 1 büküm · Ø4,5', K_URT)
for k in KOSE:
    t = uret(k['ad'], t, 'Köşebent %s-%s' % ('sol' if k['yan'] == 'sol' else 'sağ', k['ad'][-1]), sure_bukum=0.7); t = rafa(k['ad'], KUCUK.pop(0), t) + 0.05
adim('Üretim: motor braketi · reed plakaları',
     'Motor braketi 3 mm: lazerde göbek deliği, flanş kolunda 4 × M3 havşa (motor vidaları), tabanda 2 × M5 havşa (arka duvar vidaları); abkantta flanş kolu 90° bükülür. Reed plakası 2 mm × 2 (düz): lazerde 2 × Ø4,22, PEM CLS-M3-2 somunlar preste deliğine basılır (sensör vidaları bunlara girer).',
     'motor braketi 3 mm (1 büküm) · reed plakası 2 mm × 2 + 4 × PEM CLS-M3-2', K_URT_YAKIN)
t = uret('motor_braketi', t, 'Motor braketi'); t = rafa('motor_braketi', KUCUK.pop(0), t) + 0.1
for k_ in ('arka', 'on'):
    pl = 'reed_plaka_' + k_
    t = uret(pl, t, 'Reed plakası %s' % ('arka' if k_ == 'arka' else 'ön'), pemler=[('pem_reed_%s_%d' % (k_, i), 0, (-1, 0, 0)) for i in (1, 2)])
    birlesim(t - 2.0, [pl], 'PEM CLS-M3-2 × 2 → reed plakasının Ø4,22 deliklerine preslenir (sac yüzüyle aynı hizada, iç diş M3)', 0.16)
    t = rafa(pl, KUCUK.pop(0), t, grup=[pl, 'pem_reed_%s_1' % k_, 'pem_reed_%s_2' % k_]) + 0.1
adim('Üretim: avara ünitesi (kol · sensör laması · mil · reed plakaları)',
     'Avara kolu 2 mm: lazer → abkant (ön flanş, üst flanş). Sensör laması L 2 mm: tek büküm. Bağlantılar: kol kulağı ↔ lama TIG (iki yan + uç); avara mili Ø6 ↔ kol saplama kaynağı; reed plakaları ↔ lamanın alt yüzü punta (her biri 2 nokta). Mil ucunda E segman yuvası (Ø5 × 0,75).',
     'avara kolu (2 büküm) · sensör laması (1 büküm) · mil · 2 reed plakası · TIG + saplama kaynağı + punta', K_URT_YAKIN)
AV_YER = np.array([2780.0, 0.0, -230.0])
t = uret('avara_kolu', t, 'Avara kolu')
t = rafa('avara_kolu', AV_YER, t) + 0.05
hedef_k = CUR['avara_kolu'].copy()
t = uret('sensor_lamasi', t, 'Sensör laması')
o_l = CUR['sensor_lamasi'].copy(); dy = Y_SAFE - (P['sensor_lamasi']['V'][:, 1].min() + o_l[1])
t = yolu(['sensor_lamasi'], [o_l + [0, dy, 0], [hedef_k[0] + 60, o_l[1] + dy, hedef_k[2]], hedef_k + [60, -30, 0], hedef_k + [0, -30, 0], hedef_k], t, hiz=900) + 0.1
basla('avara_mili', hedef_k + [60, 0, 0], t); t = yolu(['avara_mili'], [hedef_k], t, hiz=200); vurgu(['avara_mili'], t - 0.3, t + 0.6)
for a in ('kaynak_avara', 'kaynak_avara_mili'):
    kaynak_yap(a, t); CUR[a] = hedef_k.copy()
birlesim(t, ['avara_kolu', 'sensor_lamasi'], 'TIG: avara kolu kulağı ↔ sensör laması (iki yan + uç) · saplama kaynağı: avara mili ↔ kol', 0.30); t += 1.4
REEDP = []
for k_ in ('arka', 'on'):
    pl = 'reed_plaka_' + k_; grp = [pl, 'pem_reed_%s_1' % k_, 'pem_reed_%s_2' % k_]; REEDP += grp + ['punta_reed_' + k_]
    o_p = CUR[pl].copy(); dy = Y_SAFE - (P[pl]['V'][:, 1].min() + o_p[1])
    t = yolu(grp, [o_p + [0, dy, 0], [hedef_k[0], o_p[1] + dy, hedef_k[2]], hedef_k + [0, -40, 0], hedef_k], t, hiz=900) + 0.05
    kaynak_yap('punta_reed_' + k_, t, 0.6); CUR['punta_reed_' + k_] = hedef_k.copy()
    birlesim(t, [pl], 'Punta: reed plakası %s ↔ sensör lamasının alt yüzü (2 nokta)' % ('arka' if k_ == 'arka' else 'ön'), 0.16); t += 1.0
AVARA = ['avara_kolu', 'sensor_lamasi', 'avara_mili', 'kaynak_avara', 'kaynak_avara_mili'] + REEDP
adim('Üretim: kayış çenesi (ayrı blok)',
     'Kayış çenesi artık kola kaynaklı değil, ayrı bloktur. Alt çene 2,5 mm + ara parça 1,2 mm lazerde kesilir (her birinde 2 × Ø3,4), ara parça alt çeneye iki kenarından TIG ile kaynaklanır. Üst çene 2,5 mm (2 × Ø3,4) ayrı. İkisi rafa — çekmece raylara takılıp açıldığında monte edilir.',
     'çene alt gövdesi (alt çene 2,5 + ara 1,2 · TIG 2 × 28 mm) · üst çene 2,5', K_URT_YAKIN)
t = uret('cene_alt', t, 'Çene alt gövdesi')
kaynak_yap('kaynak_cene', t); CUR['kaynak_cene'] = CUR['cene_alt'].copy()
birlesim(t, ['cene_alt'], 'TIG: ara parça ↔ alt çene (iki kenar, 2 × 28 mm)', 0.16); t += 1.2
t = rafa('cene_alt', KUCUK.pop(0), t, grup=['cene_alt', 'kaynak_cene']) + 0.1
t = uret('cene_ust', t, 'Üst çene'); t = rafa('cene_ust', KUCUK.pop(0), t) + 0.1
# ---------------- BÖLÜM 2 · RAY ÜNİTESİ ----------------
adim('Ray ünitesi: iç eleman ayrılır',
     'Accuride DZ3832-0700 teleskopik ray (satın alınan ürün, tek parça gelir: dış + ara + iç eleman). İç eleman (kızak) kilit dili basılarak ray ekseni boyunca öne çekilip ayrılır; çekmeceye bağlanacak.',
     'ray ünitesi sol / sağ (katalog) · iç eleman ayrılır', K_URT)
RAY_YER = {'sol': np.array([2950.0, 0.0, -330.0]), 'sag': np.array([3050.0, 0.0, -330.0])}
for yan in ('sol', 'sag'):
    grp = ['sabit_ray_' + yan, 'ara_ray_' + yan, 'kizak_' + yan]
    c_ = merkez('sabit_ray_' + yan); o_ = np.array([RAY_YER[yan][0] - c_[0], BENCH_Y - P['sabit_ray_' + yan]['V'][:, 1].min(), RAY_YER[yan][2] - c_[2]])
    for a in grp: basla(a, o_ + [0, 260.0, 0], t)
    t = yolu(grp, [o_], t, hiz=600) + 0.1
    t = yolu(['kizak_' + yan], [CUR['kizak_' + yan] + [0, 0, 720]], t, hiz=600); olay(t - 1.2, 'İç eleman (kızak) ray ekseni boyunca öne çekilip ayrılır'); t += 0.15
# ---------------- BÖLÜM 3 · DOLAP İÇİ ----------------
adim('Motor braketi → arka duvar',
     'Motor braketi ön çerçeve açıklığından bölmeye girer, tabanı arka iç saca oturur. Bağlantı: 2 × DIN 7991 M5 × 6 havşa vida → arka iç sacdaki 2 × PEM SP-M5-1 (Ø6,4 deliğe preslenmiş; arkasında köpük kapağı, vida ucu kapağa değmez).',
     'motor braketi · 2 × DIN 7991 M5 × 6 → 2 × PEM SP-M5-1 (arka iç sac)', K_ARKA)
t = dolaba('motor_braketi', (0, 0, 25), t); vurgu(['motor_braketi'], t - 0.4, t + 0.5)
birlesim(t, ['motor_braketi'], 'Motor braketi tabanı ↔ arka iç sac: 2 × DIN 7991 M5 × 6 → PEM SP-M5-1', 0.22, (0.5, 0.35, 0.8))
for i in (1, 2): t = tak('vida_braket_%d' % i, t, 0.8) + 0.1
t += 0.4
adim('Step motor → braket',
     'Step motor (Transmotec PD3665, satın alınan ürün — tek parça) önden girer, ekseni boyunca −x sürülür: redüktör göbeği braketin deliğine oturur. Bağlantı: 4 × DIN 7991 M3 × 6 havşa vida, braketin flanş kolundan redüktör yüzündeki 4 × M3 dişli deliğe (Ø31 daire).',
     'step motor · 4 × DIN 7991 M3 × 6 → motor yüzü M3 dişleri', K_ARKA)
basla('motor', np.array([24.0, Y_SAFE - P['motor']['V'][:, 1].min(), 980.0]), t)
t = yolu(['motor'], [[24.0, 0, 980.0], [24.0, 0, 0], [0, 0, 0]], t, hiz=600); vurgu(['motor'], t - 0.5, t + 0.5)
birlesim(t, ['motor_braketi'], 'Motor ↔ braket flanş kolu: 4 × DIN 7991 M3 × 6 (motor yüzü M3 dişli delik)', 0.20, (0.6, 0.35, 0.7))
for i in range(1, 5): t = tak('vida_motor_%d' % i, t, 0.6) + 0.05
adim('Motor kasnağı · setskur',
     'GT3 motor kasnağı (satın alınan ürün) mil ekseninde (+x) mile geçer. Bağlantı: DIN 913 M3 × 4 setskur, kasnak göbeğindeki radyal M3 dişli delikten milin düz yüzüne sıkılır.',
     'GT3 motor kasnağı · DIN 913 M3 × 4 setskur', K_ARKA_YAKIN)
basla('arka_kasnak', np.array([-14.5, Y_SAFE - P['arka_kasnak']['V'][:, 1].min(), 980.0]), t)
t = yolu(['arka_kasnak'], [[-14.5, 0, 980.0], [-14.5, 0, 0], [0, 0, 0]], t, hiz=600); vurgu(['arka_kasnak'], t - 0.4, t + 0.4)
birlesim(t, ['arka_kasnak'], 'Kasnak göbeği ↔ motor mili: DIN 913 M3 × 4 setskur (radyal M3 delik)', 0.15)
t = tak('setskur', t, 0.6) + 0.3
adim('Ray üniteleri → bölme sacları',
     'Sol ve sağ ray ünitesi (dış + ara eleman) önden girer, yana kayıp bölme sacına yaslanır. Bağlantı: her ray 3 × DIN 7991 M5 × 6 havşa vida, ara elemanın erişim deliklerinden, bölme sacındaki PEM SP-M5\'lere (arkada 1 mm derin köpük kapağı).',
     'ray ünitesi sol / sağ · 6 × DIN 7991 M5 × 6 → PEM SP-M5', K_RAY)
for yan, sx in (('sol', 10.0), ('sag', -9.0)):
    t = dolaba('sabit_ray_' + yan, (sx, 0, 0), t, grup=['sabit_ray_' + yan, 'ara_ray_' + yan], hiz=800) + 0.05
birlesim(t, ['vida_sol_1', 'vida_sol_2', 'vida_sol_3'], 'Ray dış elemanı ↔ bölme sacı: 3 + 3 × DIN 7991 M5 × 6 → PEM SP-M5', 0.55, (0.6, 0.4, 0.7))
for k_ in (1, 2, 3):
    EL[VIDA_RAY[k_ - 1]] = dict(eks=np.array([-1.0, 0, 0]), yol=40.0); EL[VIDA_RAY[k_ + 2]] = dict(eks=np.array([1.0, 0, 0]), yol=40.0)
    t0 = t; tak(VIDA_RAY[k_ - 1], t0, 0.6); t = tak(VIDA_RAY[k_ + 2], t0, 0.6) + 0.1
adim('Avara ünitesi → ön çerçeve (TIG, içeriden)',
     'Kaynaklı avara ünitesi alçaktan açıklıktan girer, içeride sola kayar, yükselip ön flanşıyla ön çerçevenin arkasına oturur. Bağlantı: ön flanş ↔ çerçeve arkası TIG köşe dikişi, içeriden 2 × 8 mm. (v2\'deki kör perçin uygulanmadı: Ø6,5 perçin başı çerçevenin önünde üst çekmecenin fitiline biniyor.)',
     'avara ünitesi · TIG köşe 2 × 8 mm (içeriden)', K_SOL_ON)
o_a = CUR['avara_kolu'].copy()
zon = 200.0 - P['sensor_lamasi']['V'][:, 2].min()
t = yolu(AVARA, [o_a + [0, Y_SAFE - 480, 0], [0.6, o_a[1] + Y_SAFE - 480, zon], [0.6, -21.0, zon], [0.6, -21.0, -0.4], [0, -21.0, -0.4], [0, 0, -0.4], [0, 0, 0]], t, hiz=700)
vurgu(['avara_kolu', 'sensor_lamasi'], t - 0.4, t + 0.5)
kaynak_yap('kaynak_avara_cerceve', t)
birlesim(t, ['avara_kolu'], 'TIG köşe: avara kolu ön flanşı ↔ ön çerçeve arkası (içeriden, 2 × 8 mm)', 0.16, (0.45, 0.3, -0.85)); t += 1.5
adim('Avara kasnağı · E segman',
     'GT3 avara kasnağı (2 × MR126 rulmanlı, satın alınan ürün) mil ekseninde (−x) mile geçer. Bağlantı: DIN 6799 RS 5 E segman, milin ucundaki Ø5 yuvaya yukarıdan radyal takılır — kasnak eksenel tutulur.',
     'GT3 avara kasnağı · DIN 6799 RS 5 E segman', K_SOL_ON)
basla('avara_kasnagi', np.array([40.0, Y_SAFE - P['avara_kasnagi']['V'][:, 1].min(), 200.0 + 18.0]), t)
t = yolu(['avara_kasnagi'], [[40.0, 0, 218.0], [40.0, 0, 0], [0, 0, 0]], t, hiz=400); vurgu(['avara_kasnagi'], t - 0.4, t + 0.5)
basla('e_segman', np.array([0.0, Y_SAFE - P['e_segman']['V'][:, 1].min(), 218.0]), t)
t = yolu(['e_segman'], [[0.0, 20.0, 218.0], [0.0, 20.0, 0.0], [0, 0, 0]], t, hiz=400); vurgu(['e_segman'], t - 0.3, t + 0.7)
birlesim(t, ['e_segman'], 'E segman DIN 6799 RS 5 → mil ucundaki Ø5 yuva (kasnağı eksenel tutar)', 0.10, (0.7, 0.4, 0.6)); t += 0.8
adim('Reed sensörler → reed plakaları',
     'Littelfuse 59135 reed sensör × 2 (satın alınan ürün, 28,57 × 19,05 × 6,35, iki yarıklı montaj deliği) arkada ve önde reed plakasına yaslanır. Bağlantı: her sensör 2 × ISO 7380 M3 × 8, sensörün yarıklarından plakadaki PEM CLS-M3-2\'lere (yarıklar konum ayarı verir).',
     'reed sensör × 2 · 4 × ISO 7380 M3 × 8 → 4 × PEM CLS-M3-2', K_ARKA_YAKIN)
for k_, zg in (('arka', 980.0), ('on', 300.0)):
    a = 'reed_' + k_
    basla(a, np.array([30.0, 0.0, zg]), t); t = yolu([a], [[30.0, 0, 0], [0, 0, 0]], t, hiz=650); vurgu([a], t - 0.3, t + 0.5)
    birlesim(t, [a], 'Reed sensör %s ↔ reed plakası: 2 × ISO 7380 M3 × 8 → PEM CLS-M3-2' % ('arka' if k_ == 'arka' else 'ön'), 0.14, (0.75, 0.35, 0.55))
    for i in (1, 2): t = tak('vida_reed_%s_%d' % (k_, i), t, 0.55) + 0.05
    t += 0.2
# ---------------- BÖLÜM 4 · ÇEKMECE KUTUSU (üretim → montaj alanı) ----------------
adim('Kutu sacları: lazer → montaj alanı → TIG',
     'Lazerde 5 düz sac (AISI 304): taban 2 mm, iki yan, arka, ön 1 mm. Bağlantı: yanlar tabanın üstüne oturur, iç köşeden TIG (tam boy); arka ve ön iki yanın arasına girer, tabana ve iki yana TIG.',
     'kutu tabanı 2 · yan sol / sağ 1 · arka 1 · ön 1 · 4 TIG dikişi', K_URT)
t = uret('kutu_taban', t, 'Kutu tabanı 2 mm'); kam(t, K_TEZ); t = tezgaha('kutu_taban', 40, t) + 0.1
kam(t, K_URT)
for ad, nm, yn in (('kutu_yan_sol', 'Kutu sol yanı', 'sol'), ('kutu_yan_sag', 'Kutu sağ yanı', 'sag')):
    t = uret(ad, t, nm); kam(t, K_TEZ); t = tezgaha(ad, 80, t) + 0.05
    k_ = 'kaynak_kutu_yan_' + yn; kaynak_yap(k_, t); CUR[k_] = DR.copy()
    birlesim(t, [ad], 'TIG iç köşe: %s yan ↔ taban (tam boy 616 mm)' % ('sol' if yn == 'sol' else 'sağ'), 0.55); t += 1.2
    kam(t, K_URT)
for ad, nm, k_ in (('kutu_arka', 'Kutu arkası', 'kaynak_kutu_arka'), ('kutu_on', 'Kutu önü', 'kaynak_kutu_on')):
    t = uret(ad, t, nm); kam(t, K_TEZ); t = tezgaha(ad, 80, t) + 0.05
    kaynak_yap(k_, t); CUR[k_] = DR.copy()
    birlesim(t, [ad], 'TIG: %s ↔ taban + iki yan (3 dikiş)' % ('arka' if 'arka' in ad else 'ön'), 0.55); t += 1.2
    kam(t, K_URT)
adim('Kızak lamaları → kutu (punta)',
     'Lamalar 6 mm sacdan 17,3 × 616 kesilir, köşebent vidaları için 2 × M4 dişli kör delik (derinlik 5) açılır. Bağlantı: kutunun iki yanına punta, her biri 4 nokta.',
     'lama sol / sağ · 2 × M4 dişli · punta 4 + 4', K_URT_YAKIN)
for yan, sx in (('sol', -70.0), ('sag', 70.0)):
    t = uret('lama_' + yan, t, 'Kızak laması %s' % ('sol' if yan == 'sol' else 'sağ')); kam(t, K_TEZ_SOL)
    t = tezgaha('lama_' + yan, 0, t, yan=(sx, 0, 0)) + 0.05
    kaynak_yap('punta_lama_' + yan, t, 0.6); CUR['punta_lama_' + yan] = DR.copy()
    birlesim(t, ['lama_' + yan], 'Punta: lama ↔ kutu %s yanı (4 nokta)' % ('sol' if yan == 'sol' else 'sağ'), 0.5); t += 1.0
    kam(t, K_URT_YAKIN)
adim('Ön bağlantı braketleri → kutu önü (punta)',
     'Her braket 2 mm sacdan açınım olarak kesilir (ön flanşta 2 × Ø5,5 — kapak saplamaları için), abkantta önce yan kol, sonra ön flanş 90°. Bağlantı: kutu önüne punta, 2 nokta.',
     'ön braket sol / sağ · 2 büküm · punta 2 + 2', K_URT_YAKIN)
for yan in ('sol', 'sag'):
    t = uret('on_braket_' + yan, t, 'Ön braket %s' % ('sol' if yan == 'sol' else 'sağ')); kam(t, K_TEZ)
    t = tezgaha('on_braket_' + yan, 0, t, yan=(0, 0, 60)) + 0.05
    kaynak_yap('punta_braket_' + yan, t, 0.6); CUR['punta_braket_' + yan] = DR.copy()
    birlesim(t, ['on_braket_' + yan], 'Punta: ön braket %s ↔ kutu önü (2 nokta)' % ('sol' if yan == 'sol' else 'sağ'), 0.22); t += 1.0
    kam(t, K_URT_YAKIN)
adim('Kayış kolu · tabla · mıknatıs kulağı (kutuya)',
     'Kol: 3 mm sacdan 6,26 × 154 kesilir → kutu sol yanının arkasına TIG (alt + üst kenar, 2 × 29 mm). Tabla 2,5 mm (2 × Ø3,4 — çene cıvataları) → kolun ucuna TIG köşe (2 × 9 mm). Mıknatıs kulağı 2 mm (2 × Ø4,22 + 2 × PEM CLS-M3-2 preslenir) → tablaya TIG köşe (iki yan).',
     'kol 3 · tabla 2,5 · kulak 2 + 2 PEM · TIG 3 birleşim', K_URT_YAKIN)
t = uret('kol', t, 'Kayış kolu'); kam(t, K_TEZ_SOL); t = tezgaha('kol', 0, t, yan=(-50, 0, 0)) + 0.05
kaynak_yap('kaynak_kol_kutu', t); CUR['kaynak_kol_kutu'] = DR.copy()
birlesim(t, ['kol'], 'TIG: kol ↔ kutu sol yanı (alt + üst kenar, 2 × 29 mm)', 0.16, (0.7, 0.45, -0.55)); t += 1.3
t = uret('tabla', t, 'Kol tablası'); kam(t, K_TEZ_SOL); t = tezgaha('tabla', 30, t, yan=(-50, 0, 0)) + 0.05
kaynak_yap('kaynak_tabla', t); CUR['kaynak_tabla'] = DR.copy()
birlesim(t, ['tabla', 'kol'], 'TIG köşe: tabla ↔ kolun üst yüzü (2 × 9 mm)', 0.13, (0.7, 0.5, -0.5)); t += 1.3
t = uret('kulak', t, 'Mıknatıs kulağı', pemler=[('pem_kulak_%d' % i, 0, (1, 0, 0)) for i in (1, 2)])
birlesim(t - 2.0, ['kulak'], 'PEM CLS-M3-2 × 2 → kulağın Ø4,22 deliklerine preslenir', 0.14)
kam(t, K_TEZ_SOL); t = tezgaha('kulak', 30, t, grup=['kulak', 'pem_kulak_1', 'pem_kulak_2'], yan=(0, 0, -40)) + 0.05
kaynak_yap('kaynak_kulak', t); CUR['kaynak_kulak'] = DR.copy()
birlesim(t, ['kulak', 'tabla'], 'TIG köşe: mıknatıs kulağı ↔ tabla (iki yan, 2 × 26 mm)', 0.13, (0.7, 0.5, -0.5)); t += 1.3
adim('Mıknatıs → kulak',
     'Littelfuse 57135 mıknatıs (satın alınan ürün, tek parça, iki yarıklı) tablanın üstünde kulağa yaslanır. Bağlantı: 2 × ISO 7380 M3 × 8, mıknatısın yarıklarından kulaktaki PEM CLS-M3-2\'lere (baş reed tarafında, reed vida başıyla arası 1,3 mm).',
     'mıknatıs · 2 × ISO 7380 M3 × 8 → 2 × PEM CLS-M3-2', K_TEZ_SOL)
basla('miknatis', DR + np.array([-30.0, 60.0, 0.0]), t)
t = yolu(['miknatis'], [DR + [-30.0, 0.0, 0.0], DR], t, hiz=300); vurgu(['miknatis'], t - 0.3, t + 0.5)
birlesim(t, ['miknatis', 'kulak'], 'Mıknatıs ↔ kulak: 2 × ISO 7380 M3 × 8 → PEM CLS-M3-2', 0.13, (-0.6, 0.45, -0.6))
for i in (1, 2):
    a = 'vida_miknatis_%d' % i; e_ = EL[a]['eks']; basla(a, DR - e_ * EL[a]['yol'], t); git(a, DR, t, 0.55); vurgu([a], t + 0.3, t + 1.0); t += 0.65
t += 0.2
kam(t, K_TEZ)
basla('silikon_tepsi', DR + np.array([0, 160.0, 0]), t); git('silikon_tepsi', DR, t, 1.0); olay(t, 'Silikon tepsi kutuya serbest oturur (bağlantısız, yıkamak için çıkar)'); t += 1.2
# ---------------- BÖLÜM 5 · KIZAKLAR + DOLABA ----------------
adim('Köşebentler · kızaklar (montaj alanında)',
     'Bağlantı: köşebentlerin yatay kolu lamaya ISO 7380 M4 × 6 ile (lamadaki M4 dişe). Kızaklar (rayın iç elemanı) köşebentlerin dik koluna yaslanır, punta (her köşebent 2 nokta).',
     'köşebent × 4 + 4 × ISO 7380 M4 × 6 · kızak × 2 (punta 2 × 2)', K_TEZ_SOL)
for k in KOSE:
    t = tezgaha(k['ad'], 40, t, hiz=1100)
    a = 'vida_' + k['ad']; basla(a, DR + np.array([0, 30.0, 0]), t); git(a, DR, t, 0.5); vurgu([a], t + 0.3, t + 1.0)
    if k['ad'] == 'kose_sol_1': birlesim(t, [k['ad']], 'Köşebent ↔ lama: ISO 7380 M4 × 6 (lamada M4 dişli kör delik)', 0.12)
    t += 0.6
for yan, sx in (('sol', -1.0), ('sag', 1.0)):
    t = tezgaha('kizak_' + yan, 0, t, hiz=1000, yan=(sx * 40, 0, 0))
    for k in KOSE:
        if k['yan'] == yan: kaynak_yap('punta_' + k['ad'], t, 0.5); CUR['punta_' + k['ad']] = DR.copy()
    birlesim(t, ['kose_%s_1' % yan], 'Punta: kızak ↔ köşebent dik kolu (2 × 2 nokta)', 0.14); t += 0.9
CEKMECE = (['kutu_taban', 'kutu_yan_sol', 'kutu_yan_sag', 'kutu_arka', 'kutu_on', 'kaynak_kutu_yan_sol', 'kaynak_kutu_yan_sag', 'kaynak_kutu_arka', 'kaynak_kutu_on',
            'lama_sol', 'lama_sag', 'punta_lama_sol', 'punta_lama_sag', 'kizak_sol', 'kizak_sag',
            'on_braket_sol', 'on_braket_sag', 'punta_braket_sol', 'punta_braket_sag', 'silikon_tepsi',
            'kol', 'kaynak_kol_kutu', 'tabla', 'kaynak_tabla', 'kulak', 'pem_kulak_1', 'pem_kulak_2', 'kaynak_kulak', 'miknatis', 'vida_miknatis_1', 'vida_miknatis_2']
           + [k['ad'] for k in KOSE] + ['vida_' + k['ad'] for k in KOSE] + ['punta_' + k['ad'] for k in KOSE])
adim('Çekmece raylara sürülür',
     'Çekmece montaj alanından ray ekseni boyunca düz çizgide içeri sürülür: kızaklar ara elemanların bilyalı kafesine geçer. Kol, tabla ve mıknatıs avara kasnağının üstünden / yanından geçer (çene bloğu henüz yok).',
     'çekmece grubu · 900 mm sürme · ray ekseni z', K_SUR)
t = yolu(CEKMECE, [np.zeros(3)], t, hiz=170.0) + 0.3
olay(t - 5.6, 'Çekmece ray ekseni boyunca sürülür — kızak ara elemanın içinde')
# ---------------- BÖLÜM 6 · KAYIŞ + ÇENE (çekmece AÇIKKEN) ----------------
adim('Kayış · çekmece açılır · çene bloğu',
     'GT3 kayış (satın alınan ürün) motor kasnağı ile avara kasnağına sarılır. Çekmece 700 mm açılır: tabla öne, avara kasnağının hemen arkasına gelir. Alt gövde ve üst çene açık çekmecenin üstünden bölmeye alınır, sağdan kayışın altına / üstüne sürülür. Bağlantı: 2 × ISO 7380 M3 × 12 yukarıdan (tabla + üst çene + ara + alt çene) + altta 2 × ISO 4032 M3 — kayış ara parçanın yanında iki çene arasında sıkışır. Çekmece kapatılır.',
     'GT3 kayış (sarılır) · çekmece açık · alt gövde · üst çene · 2 × ISO 7380 M3 × 12 · 2 × ISO 4032 M3', K_ARKA)
basla('kayis', np.zeros(3), t); ISTISNA.add('kayis'); MF['kayis'] = dict(buyu=[round(t, 3), round(t + 1.8, 3)]); olay(t, 'GT3 kayış kasnaklara sarılır (istisna: sarılarak uzar)'); t += 2.0
ACIK = np.array([0.0, 0.0, 700.0])
kam(t, K_SUR); t = yolu(CEKMECE, [ACIK], t, hiz=300.0) + 0.2; olay(t - 2.0, 'Çekmece 700 mm açılır (tabla avara kasnağının arkasında)')
JAW = []
for grp in (['cene_alt', 'kaynak_cene'], ['cene_ust']):
    a0 = grp[0]; o = CUR[a0].copy(); dy = Y_SAFE - (P[a0]['V'][:, 1].min() + o[1])
    yk = 483.0 - P[a0]['V'][:, 1].min()                                   # açık kutunun üstünden geçiş yüksekliği (kutu üstü 481,5 · açıklık üstü 491,5)
    nok = [o + [0, dy, 0], [40.0, o[1] + dy, 700.0 + 800.0], [40.0, yk, 700.0 + 800.0], [40.0, yk, 700.0], [40.0, 0.0, 700.0], ACIK]
    kam(t, yakin(['tabla'], 0.30, (0.55, 0.55, 0.65))); t = yolu(grp, nok, t, hiz=650.0) + 0.1; vurgu([a0], t - 0.4, t + 0.5); JAW += grp
birlesim(t, ['cene_alt', 'cene_ust', 'tabla'], 'Çene bloğu ↔ tabla: 2 × ISO 7380 M3 × 12 + 2 × ISO 4032 M3 (kayış iki çene arasında)', 0.14, (0.65, 0.5, 0.55))
for i in (1, 2):
    for a, yol_ in (('vida_cene_%d' % i, 20.0), ('somun_cene_%d' % i, 18.0)):
        e_ = EL[a]['eks']; basla(a, ACIK - e_ * yol_, t); git(a, ACIK, t, 0.5); vurgu([a], t + 0.3, t + 1.0); t += 0.6; JAW.append(a)
t += 0.3
kam(t, K_SUR); t = yolu(CEKMECE + JAW, [np.zeros(3)], t, hiz=300.0) + 0.3; olay(t - 2.0, 'Çekmece kapatılır — çene bloğu kayışla birlikte arkaya gider')
# ---------------- BÖLÜM 7 · ÖN KAPAK ----------------
adim('Üretim: ön kapak (8 büküm) · iç panel + PEM · PU',
     'Dış kabuk 1,5 mm: lazer → abkant 8 büküm (dört kenar, sonra dört arka dönüş). İç panel 1,0 mm: 4 delik, PEM FHS-M5-10 saplamalar preslenir. İç panel kabuğun arkasına yerleşir; aradaki boşluğa PU köpük enjekte edilir (görünmez, ısı yalıtımı).',
     'dış kabuk 1,5 (8 büküm) · iç panel 1,0 · 4 × PEM FHS-M5-10 · PU köpük', K_URT)
t = uret('kapak_dis', t, 'Kapak dış kabuğu', sure_bukum=0.75)
KP_YER = np.array([3000.0, 0.0, -300.0])
t = rafa('kapak_dis', KP_YER, t) + 0.1
h_d = CUR['kapak_dis'].copy()
PEMK = [('pem_kapak_%s_%d' % (k_, i + 1), 0, (0, 0, -1)) for k_ in STUD for i in range(2)]
t = uret('kapak_ic', t, 'Kapak iç paneli', pemler=PEMK, sure_bukum=0.75)
o_i = CUR['kapak_ic'].copy(); grp_i = ['kapak_ic'] + [p_[0] for p_ in PEMK]
dy = Y_SAFE - (P['kapak_ic']['V'][:, 1].min() + o_i[1])
t = yolu(grp_i, [o_i + [0, dy, 0], [h_d[0], o_i[1] + dy, h_d[2] - 260], h_d + [0, 0, -260], h_d], t, hiz=800) + 0.2
olay(t - 0.6, 'İç panel kabuğun arkasına yerleşir — saplamalar arkaya bakar')
basla('kapak_pu', h_d.copy(), t); ISTISNA.add('kapak_pu'); MF['kapak_pu'] = dict(buyu=[round(t, 3), round(t + 1.6, 3)]); VU['kapak_pu'].append([round(t, 3), round(t + 2.2, 3)])
olay(t, 'PU köpük iki sac arasına enjekte edilir (istisna: köpük büyüyerek doldurur)'); t += 2.0
KAPAK = ['kapak_dis', 'kapak_pu'] + grp_i
adim('Ön kapak · fitil · somunlar',
     'Fitil (silikon) kapağın kanalına arkadan bastırılır. Kapak dolabın önüne gelir; PEM saplamaları braket flanşlarındaki Ø5,5 deliklerden geçer. Bağlantı: her saplamaya U braketin açık yanından DIN 125 M5 pul + ISO 4032 M5 somun.',
     'fitil · ön kapak (saplamalar) · 4 × DIN 125 M5 · 4 × ISO 4032 M5', K_SON)
o_k2 = CUR['kapak_dis'].copy()
basla('on_panel', o_k2 + np.array([0, 0, -120.0]), t); t = yolu(['on_panel'], [o_k2], t, hiz=200); vurgu(['on_panel'], t - 0.4, t + 0.5)
olay(t - 0.8, 'Fitil kapak kanalına bastırılır')
KAPAK = KAPAK + ['on_panel']
o_k3 = CUR['kapak_dis'].copy(); dy = Y_SAFE - (P['kapak_dis']['V'][:, 1].min() + o_k3[1])
t = yolu(KAPAK, [o_k3 + [0, dy, 0], [0, o_k3[1] + dy, 400.0], [0, 0, 400.0], [0, 0, 0]], t, hiz=650); vurgu(['kapak_dis'], t - 0.5, t + 0.5)
birlesim(t, ['on_braket_sol'], 'Kapak saplaması ↔ braket flanşı: DIN 125 M5 pul + ISO 4032 M5 somun (× 4)', 0.20, (0.75, 0.35, -0.55))
for k_ in STUD:
    sx = 1.0 if k_ == 'sol' else -1.0
    if k_ == 'sag': kam(t, yakin(['on_braket_sag'], 0.20, (-0.75, 0.35, -0.55)))
    for i in (1, 2):
        for tip, dz in (('pul', 11.35), ('somun', 6.65)):
            a = '%s_kapak_%s_%d' % (tip, k_, i)
            basla(a, np.array([sx * 30.0, 0, -dz]), t); git(a, np.array([0, 0, -dz]), t, 0.35); git(a, np.zeros(3), t + 0.35, 0.4); vurgu([a], t + 0.5, t + 1.1); t += 0.8
adim('Kablolar',
     'Reed sensör kabloları ve motor kablosu bölmedeki kablo kanalı boyunca arkaya çekilir (sütunun dikey kanalı tahrikler bittikten sonra).',
     'reed sensör kabloları · motor kablosu', K_ARKA)
for a in ('kablo_sensor', 'kablo_motor'):
    basla(a, np.zeros(3), t); ISTISNA.add(a); MF[a] = dict(buyu=[round(t, 3), round(t + 2.2, 3)])
olay(t, 'Kablolar kanal boyunca çekilir (istisna)'); t += 2.6
KAM.append([round(t, 3), K_SON[0], K_SON[1]]); t += 2.4
