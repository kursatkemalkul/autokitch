# -*- coding: utf-8 -*-
"""m8c adım 4: bulguları süz + elle doğrulanmış bulgular + demet önerileri -> gece/m8/kablo.json + kablo.md (SALT OKUMA)"""
import os, pickle, json, collections, re
HERE = os.path.dirname(os.path.abspath(__file__)); M8 = os.path.dirname(HERE)
R = pickle.load(open(os.path.join(HERE, '_bulgu.pkl'), 'rb'))
H = pickle.load(open(os.path.join(HERE, '_hareket.pkl'), 'rb'))
KAY = R['KAY']
B0 = R['B'] + H
ELENEN = collections.Counter()
B = []
for b in B0:
    t = b['tur']; a = b['aciklama']; pc = str(b['parca'])
    if t == 'gecis/gomulu':
        m = re.search(r'~(\d+) mm boyunca', a)
        if 'motor_kablosu_' in a: ELENEN['gömülü: motorun kendi kablo ucuyla birleşim (bağlantı, hata değil)'] += 1; continue
        if m and int(m.group(1)) < 10: ELENEN['gömülü: < 10 mm (kanala / cihaza giriş köşesi)'] += 1; continue
    if t == 'gecis/bos_rakor':
        if not (b['dugum'].endswith('__rakor') or 'rakor' in pc.lower()) or re.match(r'(CEK_|E_GOVDE|A_ONYUZ|QR_GOZLER|TEZGAH|B_SOGUTMA)', b['dugum']):
            ELENEN['boş rakor adayı: rakor olmayan küçük plastik parça (yatak, tapa, gider)'] += 1; continue
    if t == 'gecis/deliksiz' and re.search('valf_adasi|sartlandirici', a) and 'hava' in b['dugum']:
        ELENEN['hava borusu ucu kendi cihazının (valf adası / şartlandırıcı) rakoruna giriyor'] += 1; continue
    if t == 'sureklilik/bosta_uc' and 'F_bina_230V' in pc:
        b['agirlik'] = 1; b['aciklama'] += ' · BİNA TARAFI UCU: kablo F_ust_arka_rakoru_230V_M20 ekseninden doğru geçiyor; duvar buatı / priz modelde yok'
        b['oneri'] = 'bina tarafı buatını (z −860 duvarı) modelle ya da ucu "bina hattı" diye işaretle'
    if t == 'hareket/animasyon' and b['istasyon'] == 'ROBOT':
        b['agirlik'] = 1; b['aciklama'] += ' · robot model duruşunda (park) — çekmece açılırken robot önünde olmamalı (Isaac / akış denetimi)'
    B.append(b)

# ---------------------------------------------------------------- elle doğrulanan / modelde eksik
EL = [
    dict(tur='sureklilik/kablo_yok', istasyon='TOPPING', dugum='ELK_TOPPING__kablo', parca='kablo_TOPPING_sensor_x_limit_sol + kablo_TOPPING_sensor_x_home',
         konum_mm=[1056.0, 920.0, -22.0], agirlik=3,
         aciklama="x sol limit (1050–1062 · 914–926 · −25…−19) ve x sıfır (1080–1092) sensörleri yerinde ama KABLOLARI YOK (v7'de vardı: parca_kutulari 'kablo_TOPPING_sensor_x_limit_sol' + 7 kelepçe + 'x_home'). G10 rakoru (A|TOPPING duvarı x 1436 · y 1612 · z −720) boş kaldı.",
         oneri="v7 yolunu geri kur: sensör (1056, 920, −19) → z −13 → x 886 → (x 886→1388,5 @ y 920 · z −775, X motoru kablosunun 4,5 mm yanında spiral demet) → y 1612 → G10 (1436, 1612, −720) → TOPPING pano (1520, 1879,8, −730); x sıfır kısa uçla (1086 → 1058 @ z −13) katılır. X motoru kelepçeleri (x 888 · 1013 · 1263 · 1388, y 911) çift halkalı yapılır."),
    dict(tur='sureklilik/kablo_yok', istasyon='TOPPING', dugum='TOPPING_MODUL (hava)', parca='valf adası → 4 UNO silindiri + sos/harç spreader hava hortumları',
         konum_mm=[1998.0, 1295.0, -744.0], agirlik=3,
         aciklama="valf adası 12 × 5/2 (x 1998, y 1295, z −744) ile 4 pnömatik silindir (kıyma 1624,5 · kuşbaşı 1818,5 · harç 1497 · sos 2250) ve 2 spreader hava rakoru arasında HİÇ HAVA HORTUMU yok; modeldeki tek hava hattı şartlandırıcı → ada (Ø6,6). m7a birim kaydırmasından sonra silindir portları yeni x'lerde.",
         oneri="her silindire 2 × Ø6 PU (A/B portu) + 2 spreader'a 1 × Ø6: adadan +y yukarı kuru bölme arka duvarında (z −820) tek dikey demet (x 2000, y 1295→1700) → üst raf geçiş contası → silindir hizasında yatay dağıtım; m7 'hortum dikliği' kuralı: dik iniş, kelepçe 250 mm"),
    dict(tur='sureklilik/kopuk_uc', istasyon='QR', dugum='ELK_QR_KABLO__kablo', parca='goz_00…51_isitici_kablosu (12 göz)',
         konum_mm=[4982.0, 452.5, 1000.0], agirlik=2,
         aciklama="12 göz ısıtıcı kablosunun her biri yalnız 3–4 mm'lik bir uç (x 4980–4984 / 5006–5010 · y 451, 651 … 1451 · z 999–1001); kanala / panoya giden kablo yok.",
         oneri="her ısıtıcı ucunu kendi göz sensör kablosunun yolundan kanal#2'ye (x 4994, z 930) bağla: (x, y, 1000) → z 930 → x 4994 parmak yuvası"),
    dict(tur='gecis/bos_rakor', istasyon='TOPPING', dugum='ELK_TOPPING__rakor', parca='rakor_G10_A_TOPPING_sensor_0',
         konum_mm=[1436.0, 1612.0, -720.0], agirlik=2,
         aciklama="G10 (x sol limit + x sıfır için 2 delikli conta) rakorundan kablo geçmiyor — kablolar modelden düşmüş (yukarıdaki bulgu).",
         oneri="sensör kabloları geri kurulunca bu rakordan geçir; kurulmayacaksa rakor + A sağ levhası / TOPPING sol yan sac deliğini kapat"),
    dict(tur='sureklilik/kablo_yok', istasyon='B', dugum='B_SOGUTMA__bakir', parca='evaporatör dirsekleri + kondenser (kutu yer tutucu)',
         konum_mm=[1698.5, 450.0, -709.5], agirlik=1,
         aciklama="B soğutmada bakır 'evaporator_sol/sag_dirsek_a/b' ve 'sogutma_grubu_kondenser' gerçek boru değil 12 üçgenlik kutu (ör. 1693,5–1703,5 · 258–642 · −745…−674); kompresör ↔ evaporatör emme / sıvı hatları modelde yok (yalnız sıcak gaz serpantini boru).",
         oneri="Secop NLE8.8CN emme Ø8 / sıvı Ø6 hatlarını teknik sütundan (x 4040) evaporatörlere B_KABLO kanalının altından (z −800) boru olarak modelle; dirsek kutularını gerçek 180° dirsekle değiştir"),
]
B += EL

for i, b in enumerate(B): b['no'] = i + 1

# ---------------------------------------------------------------- istasyon özeti
IST = ['A', 'TOPPING', 'F', 'K', 'E', 'B', 'U', 'QR', 'ANA_HAT', 'ROBOT', 'TEZGAH']
oz = collections.OrderedDict()
for s in IST:
    bb = [b for b in B if b['istasyon'] == s]
    if not bb: continue
    oz[s] = dict(toplam=len(bb), kritik=sum(b['agirlik'] == 3 for b in bb), orta=sum(b['agirlik'] == 2 for b in bb), dusuk=sum(b['agirlik'] == 1 for b in bb),
                 tur=dict(collections.Counter(b['tur'] for b in bb)))


def sec(f):
    return [b['no'] for b in B if f(b)]


KRITIK = [
    dict(baslik="TOPPING x sol limit + x sıfır sensör kabloları YOK", no=sec(lambda b: 'sensor_x_limit_sol' in str(b['parca'])),
         ozet="Sensörler (1056 / 1086, 920, −22) yerinde, kablo + 7 kelepçe v8x'te yok; G10 rakoru (1436, 1612, −720) boş. X ekseni kör kalır.",
         duzeltme="v7 yolunu X motoru kablosuyla aynı hatta spiral demet olarak geri kur: x 886→1388,5 @ y 920/924,5 · z −775 → y 1612 → G10 → pano (1520, 1879,8, −730)."),
    dict(baslik="TOPPING pnömatik hortumları yok (valf adası → 4 silindir + 2 spreader)", no=sec(lambda b: 'valf adası → 4 UNO' in str(b['parca'])),
         ozet="Ada (1998, 1295, −744) ile silindirler (x 1497 / 1624,5 / 1818,5 / 2250) arasında hortum yok.",
         duzeltme="Ada → kuru bölme arka duvarı z −820'de tek dikey demet (x 2000, y 1295→1700) → üst raf geçiş contası → silindir hizasında dik iniş."),
    dict(baslik="KLF6.6 soğutma grubu kablosu cihazda bitmiyor", no=sec(lambda b: 'KLF66' in str(b['parca']) and b['tur'].startswith('sureklilik')),
         ozet="Uç (1700, 1087, −805): 30 mm içinde cihaz yüzü yok, en yakın katı G2 rakoru 14 mm (cihaz kutusu z −785…−478 · kablo 20 mm arkada havada).",
         duzeltme="Ucu cihazın arka-üst yüzüne al: (1700, 1087, −780) ve 1087→1300 dikey hattı z −780'e kaydır (G2 rakoru da z −780) ya da cihazın kablo çıkış yerini (klemens kutusu) üreticiden al."),
    dict(baslik="Ana hat demetinde kablolar birbirinin İÇİNDEN geçiyor (85 kesişme)", no=sec(lambda b: b['tur'] == 'gecis/kablo_kablo' and b['istasyon'] == 'ANA_HAT'),
         ozet="Kümeler: üst kanal y 2134–2151 → x 2555–2591, 2904–2936 (UF3/UF4 geçişi, ~20), 3284–3420, 3662–3680, 3972; TOPPING sağ dikey hat x 2423–2457 (y 748–1298); zemin kanalı x 4074–4126 (y 2–12).",
         duzeltme="Kanal içinde şerit düzeni: güç katı z −810…−760, veri katı z −700…−660 (ayrı kat, EMC de ister); her dal kendi şeridinden DİK çıkar, başka şeridi kesmez — dal sırası = şerit sırası (ilk ayrılan en dış şeritte)."),
    dict(baslik="Ana hat A güç + veri A gövde sacını deliksiz geçiyor", no=sec(lambda b: b['tur'] == 'gecis/deliksiz' and 'A_GOVDE' in b['aciklama']),
         ozet="(1432,5, 2149–2151, −805 / −817): A_GOVDE paslanmaz sacında delik / rakor yok.",
         duzeltme="A sağ yan sacına (x 1432,5) 2 × M25 rakor: (y 2150, z −805) ve (y 2150, z −817) — ya da tek M40 çift delikli conta."),
    dict(baslik="Ana hat bina (Ø19,6) KD1 kanal kapağından geçiyor + besleme kanalına gömülü", no=sec(lambda b: 'ana_hat_bina' in str(b['parca']) and b['tur'] in ('gecis/deliksiz', 'gecis/gomulu')),
         ozet="(2442, 1265, −790) KD1 (x 2421–2449, z −828,3…−788,5) kapağını kesiyor; (2462,5, 1256,5, −814) ana_besleme_kanali duvarına 25 mm gömülü.",
         duzeltme="Bina hattını KD1'in sağına al: x 2460 (KD1 sağ yüzü 2449 + r 9,8 + 1), z −805; besleme kanalına girişi kanal ağzından yap."),
    dict(baslik="QR kilit kartı uçları ×4 kanal duvarını deliyor ve karta ulaşmıyor", no=sec(lambda b: 'qrk_kart_ucu' in str(b['parca']) and b['tur'] != 'hareket/kapak'),
         ozet="(5160 / 5200 / 5240 / 5280, 1676, 1033,5→1060): kanal#0 duvarı deliksiz, uç kilit kartı elemanlarına 11 mm kala bitiyor.",
         duzeltme="Uçları z 1071'e (kart yüzü) uzat; kanal#0 yan yüzünde 4 parmak yuvası (x 5160–5280, z 1033,5)."),
    dict(baslik="QR UPS uçları ×2 iki ucu da boşta", no=sec(lambda b: 'qrk_ups_ucu' in str(b['parca']) and b['tur'].startswith('sureklilik')),
         ozet="12 mm'lik eğik parça (4991–5005, 1692–1704, z 816–824 / 846–854): UPS'e de kanala da (9 mm) değmiyor.",
         duzeltme="UPS çıkışından (QR_UPS x 5005) kanal#0 yan yüzüne dik: x 5005 → 4995, y 1700, z 820 / 850."),
    dict(baslik="QR göz ısıtıcı kabloları ×12 yalnız 3 mm'lik uç", no=sec(lambda b: 'isitici' in str(b['parca'])),
         ozet="x 4980–4984 / 5006–5010 · y 451…1451 · z 999–1001; panoya giden kablo yok.",
         duzeltme="Göz sensör kablosunun yolundan kanal#2'ye (x 4994, z 930)."),
    dict(baslik="Havada kelepçeler (8)", no=sec(lambda b: b['tur'] == 'tutucu/havada_kelepce'),
         ozet="Valf adası (2201,7, 1295, −732,7) · K giriş alıcı (4193, 1110, −39) · K EC5000 (4374, 1189, −727,6) · B evap fan sağ 2 (3477,5, 476, −768,5) · UF fan emiş 1 (3510, 2048, −790) · QR ana hat ×2 (4956, 1960, 783 / 797) · K hava giriş rakoru (4001, 1809, −770).",
         duzeltme="Her birinde kelepçe dilini en yakın sac yüzüne uzat (M4 perçin somunu) ya da kabloyu yüzeye yaslayıp kelepçeyi o yüzeye taşı; m7'de taşınan raf / kaset yüzeyleri nedeniyle valf adası kelepçesi tabanı boşta kaldı."),
    dict(baslik="Boş / kaçık rakorlar (kablo geçmiyor)", no=sec(lambda b: b['tur'] == 'gecis/bos_rakor'),
         ozet="F üst kabin arka rakorları (2600 / 2630 / 3689, 830 / 1825, −821) · DOLAP kutu rakoru M20 (4295, 603,6, −660; harting iç kablosu 13 mm kaçık) · QR kutu rakorları (4880, 1938 / 1996, 790) · ana ayırıcı rakoru (5491, 1301, 950) · TOPPING pano rakoru (2010,8, 2040, −796) · F rakor (2840, 968, −778) · DOLAP (4240, 665, −592,5) · ana pano Harting ×8 (3472,6 / 3828).",
         duzeltme="Kabloyu rakor eksenine kaydır (DOLAP harting iç kablosu ucu y 580 → 603,6) ya da kullanılmayan rakor + sac deliğini kaldır."),
    dict(baslik="PulsaJet nozül parçaları havada", no=sec(lambda b: b['tur'] == 'tutucu/havada_kucuk_parca'),
         ozet="(4025, 1143–1175, −170): gövde / kapak / uç hiçbir yere değmiyor; basınç hortumu ucu 11 mm uzakta.",
         duzeltme="Nozülü yag_basinc_hortumu ucuna (4025, 1210, −192) dirsekle bağla ve K kesici braketine M5 ile vidala."),
    dict(baslik="QR alt arka paneli açılınca dikey kablolara çarpar", no=sec(lambda b: b['tur'] == 'hareket/kapak' and 'ELK_QR_MONTAJ' in b['aciklama']),
         ozet="Panel x 4572–5427 · y 21–446 · z 670 (robot tarafına −z açılır, kanat 425); önünde ana hat bina / QR / ROBOT / modem + robot uzatma kabloları x 5350–5400, y 12–60, z 240→640 dikey çıkıyor.",
         duzeltme="Dikey çıkışları panelin yan dışına (x ≥ 5435) ya da zemin_ustu_kanal_QR_basligi kapaklı kanalının içine al; menteşe tarafını kablo tarafına koy."),
    dict(baslik="Ana hat kabloları kanal duvarlarına gömülü (deliksiz kanal çıkışı)", no=sec(lambda b: b['tur'] == 'gecis/gomulu' and b['istasyon'] == 'ANA_HAT'),
         ozet="ana_besleme_kanali x 2423 duvarı (y 745–763, z −614…−709: DOLAP güç, ROBOT güç, modem, DOLAP veri, QR veri 15–20 mm) · üst kanal #0 (x 2002–2110 / 2563 / 2908, y 2104–2144) · zemin kanalı (x 4043–4126, y 2) · bina ayırıcı rakoru (5477, 1103, 937).",
         duzeltme="Kanal çıkışlarında parmak / kesik (kablo Ø + 2 mm) aç; dalları kanal ağzından (uç kapaktan) çıkar."),
    dict(baslik="Robot kablosu ↔ çekmece K3_hamur_3 çekme yolu", no=sec(lambda b: b['tur'] == 'hareket/animasyon'),
         ozet="Robot park duruşunda kol kablosu (2710, 395–411, 470) K3_hamur_3 çekmecesinin 430–700 mm açılma yolunda.",
         duzeltme="Çekmece açılırken robot park yeri x < 2050 ya da > 2790 olmalı (akış kuralı); kablo kol üzerinde kalır."),
]

DEMET = {
    'TOPPING': [
        "Sürücü bölgesi (x 1478–1585, y 1270–1536, z −810…−700): 4 kaset motor kablosu (sürücü → KD3, y 1270–1420, 33 mm arayla) tek demet: x 1530 ± 8, y 1270→1420, z −783; kelepçe y 1300 / 1400 (UPS DIN plakası z −826,5).",
        "Valf adası kablosu (x 1998→2402, y 1295, z −744, 404 mm açık, kelepçesi havada) + şartlandırıcı → ada hava hattı (x 2010→2395, y 1125, z −740): ikisi de x boyunca → kuru bölme arka duvarında ortak 30 × 40 kanal: x 2000–2420, y 1110–1150, z −828…−788 (KD1'e dik bağlanır).",
        "Sağ cep: tabla boş + x sağ limit (x 2494, y 1070 / 1074,5) zaten çift demet; enerji zinciri demeti (x 2459, y 923,5) + sabit tahrik (x 2459, y 986,5) z −811→−460 iki ayrı açık hat → tek demet x 2459, y 923,5→986,5 arası ortak kelepçe (z −600, −700).",
        "KLF6.6 kablosu (x 1670, y 1300→1880, z −805, 580 mm açık) + soğutma grubu 1087→1300: sürücü dikey kanalına (x 1523–1553) bağlanmak için y 1300'de x 1670 → 1553'e dik dön; açık hat 580 → 120 mm.",
    ],
    'A': [
        "X motoru kablosu (A içinde 1968 mm açık: x 888 dikey z −462→−775, x 888→1388,5 @ y 924,5 z −775, y 924,5→1640 @ x 1388,5): A'nın arka-alt köşesinde 30 × 30 kapaklı kanal: x 880–1395, y 905–935, z −790…−760 + dikey x 1380–1395, y 935–1650. Eksik x sol limit / x sıfır kabloları da bu kanala."
    ],
    'F': [
        "Kompresör hava ana hattı (y 1809, x 2480→3549, z −740, 1069 mm açık, 0 kelepçe) + K'ye dal (x 3549→3994, z −770, 445 mm) + dikey iniş (x 2485, y 1167→1809): F üst kabin arka duvarında (z −820) P-kelepçe her 250 mm; dal ve ana hat aynı y (1809) → ortak çift kelepçe.",
        "Davlumbaz fanı kablosu (x 2972→3460 @ y 900 z −780 + x 3460 y 900→1490, 1116 mm açık, 0 kelepçe) + F yükleme bandı motoru (x 2449→2784 @ y 1121,5 z −800): F arka duvarına 25 × 25 kanal x 2449–3460, y 890–910, z −800…−775; dikey kısım x 3450–3470.",
    ],
    'K': [
        "Arka dikey demet (5 kablo ayrı ayrı, 11–46 mm arayla): giriş alıcı x 4189 · DGRF_SMT8M_0 x 4200 · SMT8M_1 x 4216 · durus alıcı x 4246 — hepsi y 1632–1642, z −731…−429 ve −429…−141. Tek dikey kapaklı kanal 40 × 20: x 4180–4255, y 1625–1650, z −760…−140 (klemens sırası x 4176–4255 hemen altında).",
        "Y yönü yatay demet: PulsaJet (x 4025, y 1220→1642) + giriş verici (x 4185, y 1210→1534, 13 mm) ve duruş verici (x 4370) + EC5000 bant motoru (x 4374, 10 mm) → iki ortak demet: sol x 4180 ± 5 ve sağ x 4372 ± 5, z −735; kelepçe her 200 mm.",
        "Hava hortumları X_0 / X_1 (x 4386 / 4392, y 993→1405, 8 mm arayla, 0 kelepçe) tek spiral; DGRF ön / arka (x 4206 / 4226, z −690→−154, 23 mm arayla, 0 kelepçe) tek demet; yağ hortumları (emiş x 4080, dönüş x 4295, basınç x 4355) 0 kelepçe → K arka duvarında (z −825) P-kelepçe her 250 mm.",
    ],
    'B': [
        "Reed açık kabloları: her kolonda 4–5 kablo (x 806 / 1461 / 2116 / 2771 / 3426, y 271–703) ön → arka z −55→−760, 705–709 mm açık, 0 kelepçe (üreteç 'lamaya kablo bağıyla' diyor ama bağ yok). Kablo bağını modelle: her 150 mm (z −100, −250, −400, −550, −700) lamaya sabit klips; açık + kapalı çifti (6 mm arayla, x 812–988) tek spiral.",
        "Secop NLE8.8 kablosu (x 4036, z −784→−240, 544 mm açık): teknik sütun dikmesine (x 4030) 2 kelepçe daha (z −400, −600).",
    ],
    'U': [
        "UF fan kabloları: atış 0 / 1 (y 2040 / 2050, x 2691→3343 ve 2871→3343, 10 mm arayla) ve emiş 0 / 1 (y 2040 / 2050, x 3377→3912) iki ayrı çift: her çift tek spiral demet, y 2045, z −790; ortak kelepçe x 2900, 3150, 3550, 3800 (U_F havalandırma tabanı z −828).",
    ],
    'QR': [
        "QR arka ana hat (güç ROBOT 3G2,5 + QR güç + 3 Cat6A, x 4983–4995, y 28–1666, z 1002–1045): 5 kablo yan yana ama birbirini 9 noktada kesiyor, ROBOT güç + ROBOT Cat6A kanal#1 duvarını (4983, 293–307, 1045) deliksiz geçiyor → kanal#1 içinde iki kat (güç z 1036–1045, veri z 1002–1020), çıkış parmak yuvasından; 2 havada kelepçe (4955–4956, 1960, 783 / 797) kanal#0 yan yüzüne.",
        "Göz kabloları (motor / sensör / mandal) kanal#2'ye (x 4995, z 931 / 1079) temiz bağlı; demetleme gerekmez. Yalnız 12 ısıtıcı kablosu eksik (3 mm uç) ve UPS / kilit kartı uçları kopuk (kritik listede).",
    ],
    'ANA_HAT': [
        "Üst kanal (y 2104–2151, x 1990–4300): 14 kablo aynı kanalda; güç (7) ve veri (7) aynı katta karışık → 85 kesişme. Güç katı z −810…−760, veri katı z −700…−660 (ayrı ayırıcılı kanal); dallar istasyon hizasında kendi şeridinden dik iner: A x 2000, TOPPING x 2084, F x 2845 / 3823, ana pano x 3426–3506, K x 4295, E x 5093.",
        "TOPPING sağ dikey hat (x 2423–2462, y 745–1300): 7 kablo ana_besleme_kanali duvarına gömülü / birbirini kesiyor → kanal genişliği 40 → 60 mm, kablolar x sırası 2428 / 2438 / 2448 / 2458 sabit, kanaldan çıkış uç kapaktan.",
        "Zemin kanalı (y 0–123, x 4040–5520): bina + QR güç + ROBOT güç + modem + QR veri x 4043–4126 aralığında birbirini kesiyor; kanala giriş sırası = kanal içindeki yanal sıra.",
        "ana_hat_F_guc yolu 4725 mm, uçlar arası dik mesafe 2308 mm (oran 2,0): ana pano (3822, 2021, −427) → F (2845, 1041, −780) için üst kanal + TOPPING sağ dikey hat yerine F üst kabin arka duvarından doğrudan (x 3822 → 2845 @ y 1860, z −800) ~1500 mm kısalır.",
    ],
}

YONTEM = [
    "Model: hat3_v8x.glb (gece madde 1–7 sonrası), SALT OKUMA. Kablo / hortum / boru = düğüm malzemesi kablo · kablo_veri · hava_ana · hava · bakir · hortum_gida · hortum_yag · hortum_orgu (325 bağlı bileşen, 12 üçgenli kutular hariç).",
    "Eksen çıkarımı: silindir / yuvarlatılmış kare yan şeritlerinden doğru parçalar (serit.py); bulunamazsa geodezik dilim. Bileşen adı parca_kutulari (pk_yeni, m7 kaydırmalı) en küçük kapsayan kutu.",
    "Süreklilik: serbest uç (başka segmente r1+r2+6 mm'den uzak) önünde r+4 mm içinde başka katı yoksa boşta. Geçiş: eksen doğru parçası × tüm üçgenler (rtree + Möller–Trumbore). Gömülü: eksenden 0,55 r içinde katı yüzey (5 mm adım).",
    "Tutucu: ELK / K_YAG / ROBOT / HAVA küçük çelik-plastik bileşenler (< 45 mm); halka kabloyu sarıyor mu (köşe–eksen mesafesi − r < 2 mm), 0,8 mm içinde gövde yüzeyi var mı.",
    "Hareket: animasyonlu düğümlerin öteleme yolu boyunca (5 mm adım) yüzey örnekleri ↔ kablo noktaları; kapaklar (kpk, ≤ 25 mm kalın) kısa kenar kadar dışa açılma kutusu; kaşar/sucuk kaseti +z 300, UNO hazneleri öne; TOPPING araba/kızak/motor zarfları (h3_elk_ist_v1) ve robot koridoru (z 79–669).",
]
SINIR = [
    "Menteşe yerleri modelde yok → kapak süpürmesi kutu yaklaşımı (kanat = kısa kenar); kesin değil.",
    "Robot erişimi ayrıntılı değil (koridor kutusu); robot / enerji zinciri Kemal kuralı gereği Isaac'ta.",
    "Döner animasyonlu E kutu düğümleri (E_KUTU, E_KOSE) süpürmeye alınmadı (yakınında kablo yok).",
    "Kablo içi kanalda çizilmeyen yollar (kapaklı kanal) denetlenmedi; kanal doluluk oranı hesaplanmadı.",
    "Ad eşleme v7 kutularıyla: m3 / m7c ile yeniden çekilen kabloların bazıları adsız (ELK_TOPPING__kablo#9534 = tabla boş sensörü, #9632 = x sağ limit).",
]

J = dict(meta=dict(madde='8c kablo / hortum / boru taraması', model='hat3_v8x.glb', tarih='2026-10-03', salt_okuma=True,
                   kablo_bileseni=len(KAY), segment=sum(len(d['S']) for d in KAY), arac='gece/m8/kablo_is/*.py'),
         yontem=YONTEM, sinirlar=SINIR, istasyon_ozeti=oz, en_kritik_15=KRITIK, demet_onerileri=DEMET,
         elenen_yanlis_pozitif=dict(ELENEN), bulgular=B)
json.dump(J, open(os.path.join(M8, 'kablo.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1, default=float)

# ---------------------------------------------------------------- MD
L = []
L.append("# MADDE 8c · KABLO / HORTUM / BORU TARAMASI (hat3_v8x · salt okuma)\n")
L.append("Model değiştirilmedi. %d kablo/hortum/boru bileşeni, %d doğru parça tarandı. Tam liste: `kablo.json` (%d bulgu, her biri düğüm · istasyon · konum mm · tür · öneri). Ağırlık: 3 kritik · 2 orta · 1 düşük.\n" % (len(KAY), J['meta']['segment'], len(B)))
L.append("## İSTASYON BAŞINA BULGU SAYISI\n")
L.append("| istasyon | toplam | kritik | orta | düşük | en çok |")
L.append("|---|---|---|---|---|---|")
for s, v in oz.items():
    en = ", ".join("%s %d" % (k.split('/')[1], n) for k, n in sorted(v['tur'].items(), key=lambda x: -x[1])[:3])
    L.append("| %s | %d | %d | %d | %d | %s |" % (s, v['toplam'], v['kritik'], v['orta'], v['dusuk'], en))
L.append("")
L.append("## EN KRİTİK 15\n")
for i, k in enumerate(KRITIK, 1):
    L.append("**%d. %s** (bulgu no: %s)  \n%s  \n→ %s\n" % (i, k['baslik'], ", ".join(map(str, k['no'][:12])) + (" …" if len(k['no']) > 12 else ""), k['ozet'], k['duzeltme']))
L.append("## DERLİ TOPLU OLMA · DEMET ÖNERİLERİ (istasyon başına)\n")
L.append("Kemal: \"kablolar neden daha derli toplu değil\" — ana neden: üreteç her kabloyu tek tek en kısa dik yolla çekiyor, ortak kanal yalnız TOPPING (KD1/KD2/sürücü), B kolonları ve ana hatta var; paralel giden kablolar 6–50 mm arayla ayrı, açık hatlarda kelepçe az ya da yok.\n")
for s, lst in DEMET.items():
    L.append("**%s**" % s)
    for x in lst: L.append("- " + x)
    L.append("")
L.append("## KRİTİK + ORTA BULGULAR (kısa liste)\n")
for s in oz:
    bb = [b for b in B if b['istasyon'] == s and b['agirlik'] >= 2]
    if not bb: continue
    L.append("**%s** (%d)" % (s, len(bb)))
    tc = collections.defaultdict(list)
    for b in bb: tc[b['tur']].append(b)
    for t, lst in tc.items():
        if len(lst) > 6:
            L.append("- `%s` × %d — ör. %s @ %s: %s" % (t, len(lst), lst[0]['parca'], lst[0]['konum_mm'], lst[0]['aciklama'][:140]))
        else:
            for b in lst: L.append("- #%d `%s` %s @ %s — %s → %s" % (b['no'], t, b['parca'], b['konum_mm'], b['aciklama'][:170], b['oneri'][:150]))
    L.append("")
L.append("## ELENEN YANLIŞ POZİTİFLER\n")
for k, v in ELENEN.items(): L.append("- %s: %d" % (k, v))
L.append("\n## YÖNTEM\n")
for x in YONTEM: L.append("- " + x)
L.append("\n## SINIRLAR\n")
for x in SINIR: L.append("- " + x)
L.append("\nBetikler: `gece/m8/kablo_is/` (kablo_cikar.py → kablo_denetim.py → hareket.py → birlestir.py; ortam.py, serit.py).")
open(os.path.join(M8, 'kablo.md'), 'w', encoding='utf-8').write("\n".join(L))
print(len(B), dict(ELENEN))
for s, v in oz.items(): print(s, v['toplam'], v['kritik'], v['orta'], v['dusuk'])
