MOTOR_GRUP = ['motor_braketi', 'motor', 'motor_flansi', 'motor_rakoru', 'arka_kasnak']
TM = (150, -3, 1300)        # motor alt montajı tezgâhta: son yerinden +x 150, −y 3 (braket tezgâha oturur), +z 1300

# ================================================================== PLAN (plan.md ile birebir)
KAM.append([0.0, K_TEZ[0], K_TEZ[1]])
bekle(1.0)
adim('Tezgâh: motor grubu',
     'Tahrikin arka grubu tezgâhta hazırlanır: motor braketi tezgâha konur; step motor (mili ve arka kapağıyla), flanşı ve kablo rakoru kendi ekseni boyunca yandan braketin içine sürülüp vidalanır; GT3 motor kasnağı mile karşı taraftan, mil ekseninde takılır. Motor dolabın içinde braketin içine giremez — arkadaki dikey kablo kanalı yolu kapatır; bu yüzden grup tezgâhta kurulur.',
     'motor braketi · step motor (mil + arka kapak) · motor flanşı · kablo rakoru · GT3 motor kasnağı', K_TEZM)
hareket(['motor_braketi'], [((0, 120, 0), 1.2)], 'Motor braketi tezgâha konur')
bekle(0.2)
hareket(['motor', 'motor_flansi', 'motor_rakoru'], [((60, 0, 0), 1.3)], 'Step motor kendi ekseninde braketin içine sürülür')
bekle(0.2)
hareket(['arka_kasnak'], [((-30, 0, 0), 1.0)], 'GT3 motor kasnağı mile takılır (mil ekseninde)')
bekle(0.5)

adim('Motor grubu arka duvara',
     'Motor grubu tezgâhtan kaldırılır, önden çerçeve açıklığından bölmeye girer ve braket arka duvara oturup cıvatalanır. Sol sabit ray henüz takılı değildir; kasnak sol taraftan rahat geçer.',
     'motor grubu (5 parça) · braket → arka duvar', K_ARKA)
grup_bacak(MOTOR_GRUP, (0, TM[1], 0), 0.5, 'Motor grubu tezgâhtan kaldırılır')
grup_bacak(MOTOR_GRUP, (TM[0], 0, 0), 1.0, None)
grup_bacak(MOTOR_GRUP, (0, 0, TM[2]), 3.2, 'Motor grubu önden girer, braket arka duvara oturur')
bekle(0.6)

adim('Sensör plakası · sabit raylar',
     'Sensör lamasının arka plakası yukarıdan arka duvara oturur. Sol ve sağ sabit raylar (bilyalı teleskop rayın dış profili) önden, çerçeve açıklığından bölmeye girer; sonra yana kayıp bölme sacına yaslanır. Ray delikleri bölmedeki PEM somunlarının hizasındadır.',
     'sensör plakası · sabit ray sol · sabit ray sağ', K_RAY)
hareket(['sensor_plakasi'], [((0, 40, 0), 0.9)], 'Sensör plakası yukarıdan arka duvara oturur')
bekle(0.2)
t0 = t
hareket(['sabit_ray_sol'], [((0, 0, 800), 2.2), ((10, 0, 0), 0.7)], 'Sabit raylar önden girer, bölme saclarına yaslanır', bas=t0)
t = t0
hareket(['sabit_ray_sag'], [((0, 0, 800), 2.2), ((-10, 0, 0), 0.7)], None, bas=t0)
bekle(0.5)

adim('Ray vidaları',
     'Her ray 3 adet M5 × 10 havşa başlı vidayla bölme sacındaki PEM somununa vidalanır (toplam 6). Vidalar ray gövdesine dik, kendi eksenleri boyunca girer; arkadaki köpük kapağı PU sızıntısını önler.',
     '6 × M5 × 10 havşa başlı (DIN 7991) · PEM SP-M5 bölmede hazır', K_SOL)
for k in (1, 2, 3):
    t0 = t
    hareket(['vida_sol_%d' % k], [((40, 0, 0), 0.7)], 'Ray vidası %d / 3 (sol ve sağ) — kendi ekseninde' % k, bas=t0)
    t = t0
    hareket(['vida_sag_%d' % k], [((-40, 0, 0), 0.7)], None, bas=t0)
    bekle(0.15)
bekle(0.5)

adim('Avara braketi · reed sensörler',
     'Ön avara braketi ile sensör laması tek kaynaklı parçadır: bölmenin içinden yana kayarak yerine gelir, kulağı ön çerçevenin arkasına cıvatalanır. İki reed sensör (kapalı ve açık konum) lamanın altına aşağıdan takılır.',
     'avara braketi + sensör laması · reed sensör (arka = kapalı) · reed sensör (ön = açık)', K_SOL)
hareket(['avara_braketi'], [((30, 0, 0), 1.2)], 'Avara braketi + sensör laması yana kayarak yerine gelir')
bekle(0.3)
t0 = t
hareket(['reed_arka'], [((0, -20, 0), 0.8)], 'Reed sensörler lamanın altına aşağıdan takılır', bas=t0)
t = t0
hareket(['reed_on'], [((0, -20, 0), 0.8)], None, bas=t0)
bekle(0.5)

adim('Ara raylar',
     'Ara raylar (teleskobun orta profili) önden, ray ekseni boyunca sabit rayın içine sürülür.',
     'ara ray sol · ara ray sağ', K_RAY)
t0 = t
hareket(['ara_ray_sol'], [((0, 0, 760), 2.6)], 'Ara raylar ray ekseni boyunca sabit rayın içine sürülür', bas=t0)
t = t0
hareket(['ara_ray_sag'], [((0, 0, 760), 2.6)], None, bas=t0)
bekle(0.6)

adim('Tezgâh: çekmece gövdesi · silikon tepsi',
     'Çekmece tezgâhta kurulur: sac tava (çekmece gövdesi) tezgâha konur, silikon tepsi üstten içine yerleşir.',
     'çekmece gövdesi (sac tava) · silikon tepsi', K_TEZ)
hareket(['cekmece_govdesi'], [((0, 150, 0), 1.2)], 'Çekmece gövdesi tezgâha konur')
bekle(0.2)
hareket(['silikon_tepsi'], [((0, 120, 0), 1.0)], 'Silikon tepsi gövdenin içine yerleşir')
bekle(0.5)

adim('Tezgâh: kızaklar · kayış laması · ön braketler',
     'Kızak bağlantı lamaları gövdenin iki yanına, kızaklar (teleskobun iç profili) lamalara vidalanır. Sol yana kayış kelepçe laması, üstüne mıknatıs yuvası takılır. Ön kapak braketleri gövdenin önüne oturur.',
     'kızak laması sol / sağ · kızak sol / sağ · kayış laması · mıknatıs · ön braket sol / sağ', K_TEZ)
t0 = t
hareket(['kizak_lamasi_sol'], [((-40, 0, 0), 0.8)], 'Kızak lamaları gövdenin yanlarına', bas=t0)
t = t0
hareket(['kizak_lamasi_sag'], [((40, 0, 0), 0.8)], None, bas=t0)
bekle(0.2)
t0 = t
hareket(['kizak_sol'], [((-40, 0, 0), 0.8)], 'Kızaklar lamalara vidalanır', bas=t0)
t = t0
hareket(['kizak_sag'], [((40, 0, 0), 0.8)], None, bas=t0)
bekle(0.2)
hareket(['kayis_lamasi'], [((0, 40, 0), 0.8)], 'Kayış kelepçe laması sol yana')
bekle(0.1)
hareket(['miknatis'], [((0, 40, 0), 0.7)], 'Mıknatıs yuvası lamanın üstüne')
bekle(0.1)
t0 = t
hareket(['on_braket_sol'], [((0, 0, 40), 0.8)], 'Ön kapak braketleri gövdenin önüne', bas=t0)
t = t0
hareket(['on_braket_sag'], [((0, 0, 40), 0.8)], None, bas=t0)
bekle(0.6)

adim('Çekmece raylara sürülür',
     'Kurulan çekmece tezgâhtan alınır, kızaklar ara rayların ağzına hizalanır ve çekmece ray ekseni boyunca, düz bir çizgide içeri sürülür. Kızak ara rayın içinde, profiller hizalı ilerler; çekmece arka konumda durur.',
     'çekmece grubu (10 parça) · 900 mm sürme · ray ekseni z', K_SUR)
grup_bacak(CEKMECE, (0, 0, S), 5.5, 'Çekmece ray ekseni boyunca içeri sürülür — kızak ara rayın içinde')
bekle(0.6)

adim('Avara kasnağı · kayış',
     'Ön avara kasnağı miliyle birlikte önden braketine takılır. GT3 kayış motor kasnağı ile avara kasnağına sarılır, üst kolu çekmecedeki kelepçe lamasına sıkılır ve avara braketinden gerdirilir.',
     'GT3 avara kasnağı + mili · GT3 kayış (sarma)', K_ON)
hareket(['avara_kasnagi'], [((0, 0, 60), 1.0)], 'Avara kasnağı miliyle önden braketine takılır')
bekle(0.3)
cek(['kayis'], 1.8, 'GT3 kayış kasnaklara sarılır, kelepçeye sıkılır, gerdirilir')
bekle(0.5)

adim('Ön panel · ön kapak',
     'Ön panel çekmecenin ön kapak braketlerine, şeffaf ön kapak da panelin önüne takılır.',
     'ön panel · ön kapak (şeffaf)', K_SON)
hareket(['on_panel'], [((0, 0, 240), 1.2)], 'Ön panel braketlere takılır')
bekle(0.2)
hareket(['on_kapak'], [((0, 0, 240), 1.2)], 'Şeffaf ön kapak takılır')
bekle(0.5)

adim('Kablolar',
     'Reed sensör kabloları ve motor kablosu bölmedeki kablo kanalı boyunca arkaya, oradan dikey kanala çekilir.',
     'reed sensör kabloları · motor kablosu', K_ARKA)
cek(['kablo_sensor', 'kablo_motor'], 2.4, 'Sensör ve motor kabloları kanal boyunca çekilir')
bekle(1.5)
KAM.append([round(t, 3), K_SON[0], K_SON[1]])
