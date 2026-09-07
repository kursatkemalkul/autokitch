# -*- coding: utf-8 -*-
# HAT v48 = v47 + OVEN v3 (kolon 65 -> 70, hat 420; kartus + nis alti bos + plenum/fan/filtre + yan yalitim) + TOPPING v27 sayilari + kizak ±5 + KONTROL ② ⑩ kapandi
import io, re
SRC = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\_uretec\teknik_cizim47.py"
DST = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\_uretec\teknik_cizim48.py"
s = io.open(SRC, encoding='utf-8').read()

def rep(a, b, cnt=1):
    global s
    assert s.count(a) == cnt, ('%d != %d: ' % (s.count(a), cnt)) + a[:80]
    s = s.replace(a, b)

# ---- genel: kolon 70, hat 420, v48 ----
rep('("4 · OVEN",650)', '("4 · OVEN",700)')
rep('hat_on_gorunus_teknik_v47.svg', 'hat_on_gorunus_teknik_v48.svg')
rep('"KONTROL — istasyonlar arası uyum (5 Eyl 2026, HAT v47)"', '"KONTROL — istasyonlar arası uyum (6 Eyl 2026, HAT v48)"')
rep('"AUTOKITCH — HAT v47 · TÜM İSTASYONLAR SON VERSİYON (5 Eyl 2026) — STORE v4 (+ v5 öneri: −18 kaset katı) · PRESS v8 · TOPPING v25 yerleşim + v26 KAP (Picnic tipi: daire duvar · POM helezon · çubuk tarak · şeffaf PC) · OVEN tank+pompa · PACK 116"',
    '"AUTOKITCH — HAT v48 · TÜM İSTASYONLAR SON VERSİYON (6 Eyl 2026) — STORE v4 (+ v5 öneri) · PRESS v8 · TOPPING v25 yerleşim + v27 KAP (Picnic tipi, kapalı boru + menteşeli kapak) · OVEN v3 (Omake 2 kat · sadeyağ KARTUŞU · kolon 70) · PACK 116"')
rep('"Robot: tek kol, 16–20 kg sınıfı (en ağır yük: kıyma kabı 8,4 + kap 5,0 + çatal 2,0 = 15,4 kg — ⑦ açık)',
    '"Robot: tek kol, 16–20 kg sınıfı (en ağır yük: kıyma 7,5 + kap 5,7 + çatal 2,0 = 15,2 kg — ⑦ açık)')
rep('"Ölçüler cm. HER KABİN 70/65/140 × 197 × 84 (gövde 185 + ayak 12; TOPPING\'de ayak yerine plint 12 = soğutma ızgarası). Açık: ② fırın kavitesi 44 · ⑤ Fersah Ø30 taban · ⑦ kol yükü 15,4 kg + menzil · ⑩ yağ pompa · ⑫ tepsi Ø32 zinciri (robot uç v2) · ① STORE v5 onayı · TOPPING prototipleri (spiral 11, kaşar akışı, çatal-cep hizası)"',
    '"Ölçüler cm. HER KABİN 70/140 × 197 × 84 (gövde 185 + ayak 12; TOPPING ve OVEN\'de ayak yerine plint 12 = ızgara). Açık: ⑤ Fersah Ø30 taban · ⑦ kol yükü 15,2 kg + menzil · ⑫ robot tepsi eli v2 (kulp 6) · ① STORE v5 onayı · TOPPING prototipleri (spiral 11, kaşar akışı, çatal-cep hizası) · OVEN: kuru bağlantı tipi, karbon filtre tedariki, tepsili pide pilotu"')
rep('haftada ≈ 12 + STORE→ALT 4', 'haftada ≈ 14 + STORE→ALT 4')
rep('en ağır yük kıyma kabı 15,2 kg (⑦)', 'en ağır yük kıyma kabı 15,2 kg (⑦)')   # zaten 15,2
# TOPPING ve OVEN: ayak yerine plint
rep("    if i!=2: rc(_x+14,YT,12,px(HA),1.4); rc(_x+px(_w)-26,YT,12,px(HA),1.4)   # TOPPING: ayak yerine plint",
    "    if i not in (2,3): rc(_x+14,YT,12,px(HA),1.4); rc(_x+px(_w)-26,YT,12,px(HA),1.4)   # TOPPING + OVEN: ayak yerine plint")
# kizaklar ±5 (v27): on gorunus glyph + plan cepleri
rep("    for dx_ in (30,110): rc(x+px(dx_-15),y+px(240),px(30),px(20),.7,0,col,dsh,'#d0d7de' if not bos else '#f7f6f2')   # kızaklar",
    "    for dx_ in (20,120): rc(x+px(dx_-15),y+px(240),px(30),px(20),.7,0,col,dsh,'#d0d7de' if not bos else '#f7f6f2')   # kızaklar ±5 (v27)")
rep("    for dx_ in (30,110): ln(c0+px(xk+dx_),YT2+px(110),c0+px(xk+dx_),YT2+px(770),.7,'#555','3,2')      # kızak cepleri (çatal buraya girer)",
    "    for dx_ in (20,120): ln(c0+px(xk+dx_),YT2+px(110),c0+px(xk+dx_),YT2+px(770),.7,'#555','3,2')      # kızak cepleri ±5 (çatal buraya girer)")

# ---- OVEN on gorunus: v47 blogu -> v3 kolonu ----
i0 = s.index('# ================= 4 OVEN (tepsiyle · tank + pompa) =================')
i1 = s.index('# ================= 5 PACK')
OVEN = r'''# ================= 4 OVEN v3 (Omake FPZ01.E21 2 kat · sadeyağ KARTUŞU · niş altı boş · plenum + fan + filtre · yan yalıtım 3) =================
d0,d1=xs[3],xs[4]; dm=(d0+d1)/2; WD=d1-d0-px(40)
Zh=lambda z: YZ-px(z*10)          # zeminden cm -> y
# yan yalitim seritleri (2 seramik elyaf + 1 hava) kartus katindan filtre ustune
for xs_ in (d0+4, d1-4-px(30)):
    rc(xs_,Zh(187),px(20),px(145*10),.6,0,'#b08968',None,'#f3f0e6'); rc(xs_+px(20),Zh(187),px(10),px(145*10),.5,0,'#7fb3d5',None,'#eef6fb')
ZON=[(0,12,'#e9e4d6','plint 12 — HAVA GİRİŞİ ızgarası'),(12,42,'#e3f2fb','PANO 30 · PLC I/O · 2 menteşe sürücüsü · 2 SSR · 24 V'),(42,72,'#fff8e0',''),(72,90,'#fbf3e6',''),(146,172,'#fde9c9',''),(172,187,'#eef3f8','FAN 140 m³/h + yağ filtresi + aktif karbon 15'),(187,197,'#e9e4d6','üst çıkış ızgarası → mekân')]
for z0_,z1_,col,lab in ZON:
    rc(d0+px(30),Zh(z1_),d1-d0-px(60),px((z1_-z0_)*10),.8,0,'#555',None,col)
    if lab: notew(dm,Zh((z0_+z1_)/2)+2,lab,WD-px(40),5.4,'#333','middle','bold' if z0_ in (12,146,172) else '')
# firin govdesi 64x56 (z 90-146), 2 kapak (asagi acilir cam), tepsi duzlemleri 95/123
rc(d0+px(30),Zh(146),px(640),px(560),2,3,'#111',None,'#f4f4f4')
for zk0,zk1,nm,tp in ((90,118,'KAPAK 1 · alt kat',95),(118,146,'KAPAK 2 · üst kat',123)):
    rc(d0+px(65),Zh(zk1-4),px(570),px((zk1-zk0-8)*10),1.2,1,'#333',None,'#dbeeff')
    rc(d0+px(65),Zh(zk0+4)+px(12),px(570),px(12),.8,0,'#333',None,'#999')
    tx(dm,Zh((zk0+zk1)/2)+2,nm+' · hazne 40×40×10 · tepsi düzlemi %d' % tp,5.2,'middle','bold','#333')
    rc(d1-4-px(27),Zh(zk0+7),px(24),px(60),1,1,'#c0392b',None,'#f7d7d7')                   # menteşe motoru (yan aralıkta)
tx(d1-px(40),Zh(147.2)+2,'menteşe motoru ×2 Ø28 (yan aralıkta)',4.2,'end','','#c0392b')
# sprey nisi 18 (z 72-90): nozul ustte, alti bos, tepsi onden girer
ci(dm,Zh(88.5),px(30),1,'#c9a227',None,'#fff8e0')
E.append('<polygon points="%.1f,%.1f %.1f,%.1f %.1f,%.1f" fill="#fff3c4" fill-opacity="0.5" stroke="#c9a227" stroke-width="0.6"/>' % (dm,Zh(88.5),dm-px(150),Zh(73.5),dm+px(150),Zh(73.5)))
tray(dm,Zh(75),kulp=True)
tx(dm,Zh(85.5)+2,'SPREY NİŞİ 18 — altı boş · nozül 90° → Ø30 · 4 ml / 0,5 sn',4.8,'middle','bold','#b7791f')
# kartus yuvasi 30 (z 42-72): kartus 4 L + pompa + on kapak (eleman)
rc(d0+px(80),Zh(69),px(200),px(220),1.2,2,'#c9a227',None,'#fff8e0'); tx(d0+px(180),Zh(60)+2,'KARTUŞ 4 L',6,'middle','bold','#8a6a3a'); tx(d0+px(180),Zh(54)+2,'ısıtma ceketi 45 °C',4.6,'middle','','#8a6a3a'); tx(d0+px(180),Zh(49)+2,'kuru bağlantı altta',4.6,'middle','','#8a6a3a')
rc(d0+px(320),Zh(58),px(90),px(80),1,2,'#333',None,'#eee'); tx(d0+px(365),Zh(54)+2,'POMPA',4.8,'middle','bold'); tx(d0+px(365),Zh(47.5)+2,'24 V dişli',4,'middle','','#555')
ln(d0+px(365),Zh(58),d0+px(365),Zh(72),1,'#c9a227'); ln(d0+px(365),Zh(72),dm,Zh(88.5)-px(30),1,'#c9a227')
notew(d0+px(540),Zh(62),'ÖN KAPAK: eleman haftada 1 kartuşu değiştirir (10 gün) · robot dokunmaz',px(220),4.6,'#b7791f','middle','bold')
tx(d0+px(22),Zh(70)+2,'kartuş yuvası 30',4.6,'start','','#8a6a3a')
# hava akisi
for xx_ in (d0+px(19), d1-px(19)):
    ln(xx_,Zh(6),xx_,Zh(40),1,'#7fb3d5'); E.append('<path d="M %.1f %.1f l -3 6 h 6 z" fill="#7fb3d5"/>' % (xx_,Zh(40)))
ln(dm+px(230),Zh(189),dm+px(230),Zh(196),1.2,'#1a49b8'); E.append('<path d="M %.1f %.1f l -3 6 h 6 z" fill="#1a49b8"/>' % (dm+px(230),Zh(196)))
tx(dm,Zh(168)+2,'PLENUM 26 — sıcak hava toplanır',5.4,'middle','bold','#333')
notew(dm,Zh(161),'yan 3 = 2 seramik elyaf + 1 hava aralığı (sol TOPPING +3 °C, sağ PACK karton) · komşu yüzey < oda + 10 °C · bacasız: fırın buharı arka kanaldan plenuma',WD-px(30),4.8,'#555')

'''
s = s[:i0] + OVEN + s[i1:]

# ---- OVEN ust gorunum ----
i0 = s.index('# OVEN ust')
i1 = s.index('# PACK ust')
OVU = r'''# OVEN ust v3: firin 64x60 onde, arka kanal 20 (hava + kablo + buhar) + arka yalitim 2, yan 3 yalitim
rc(d0+px(30),YT2+px(20),px(640),px(600),1.6,2,'#111',None,'#f4f4f4')
rc(d0+px(30),YT2+px(640),px(640),px(180),.8,0,'#7fb3d5',None,'#eef6fb'); tx(dm,YT2+px(735),'arka kanal 20: hava + kablo + buhar',5,'middle','','#1a49b8')
for xs_ in (d0+4, d1-4-px(30)): rc(xs_,YT2,px(30),px(840),.6,0,'#b08968',None,'#f3f0e6')
rd(dm-px(200),YT2+px(120),px(400),px(400))
ci(dm,YT2+px(320),px(160),1.2,'#1a49b8','4,3'); rc(dm-px(15),YT2+px(480),px(30),px(60),1,1,'#1a49b8'); tx(dm+px(50),YT2+px(560),'kulp 6 (v2 el)',5,'start','','#1a49b8')
tx(dm,YT2+px(90),'kavite 40×40 (kesik) · fırın 64×60',5.2,'middle','','#555')
rc(d0+px(50),YT2+px(545),px(190),px(70),1,2,'#c9a227','4,3','#fff8e0'); tx(d0+px(145),YT2+px(590),'kartuş (alt, kesik)',4.4,'middle','','#8a6a3a')
notew(dm,YN,"fırın 64×60 + arka kanal 20 + arka yalıtım 2 = 84 · yan 3 (yalıtım 2 + hava 1) · tepsi Ø32 + kulp 6 = 38 ≤ 40 ✓ (② kapandı)",d1-d0-20,7)
'''
s = s[:i0] + OVU + s[i1:]

# ---- KONTROL satirlari ----
rep(''' ("② OVEN kavite 40×40: tepsi Ø32 + kulp 12 = 44 → kapak kapanmaz — AÇIK","→ öneri: kulp ÖNE dönük (robot kürek gibi sürer) + kavite derinliği 50 → 84 derinliğe sığar, kabin büyümez · alternatif kulp 6 cm — KARAR","#b3452b"),''',
    ''' ("② ✓ OVEN kavite 40×40×10: tepsi Ø32 + kulp 6 = 38 ≤ 40 — KAPANDI (kulp 6, robot tepsi eli v2)","→ Omake FPZ01.E21 çift katlı (64×60×56, 4,8 kW, 2 camlı kapak aşağı açılır, 24 V lineer aktüatör + 2 switch) · tepsi düzlemleri 95 / 123 · durumlar KAPALI / ÖN ISITMA / BEKLEME 340 / EKO 250 / PİŞİRME","#1d7a4f"),''')
rep(''' ("⑦ KOL YÜKÜ YENİDEN AÇIK: kap boş ≈ 5,0 kg (PC 5 mm 3,3 + POM helezon 0,7 + tarak 1,0) + çatal 2,0 → kıyma 15,4 kg · sucuk 14,7 · kaşar 12,8",''',
    ''' ("⑦ KOL YÜKÜ AÇIK (v27): kap boş ≈ 5,7 kg (PC 5 mm + taban plakası + POM helezon 66 + tarak + kapak) + çatal 2,0 → kıyma 15,2 kg · sucuk 14,6 · kaşar 12,8",''')
rep(''' ("⑧ ✓ TOPPING v25 yerleşim + v26 KAP (Picnic tipi): dış 14×68×24 aynı · iç: daire duvar R 6,5 (tarak süpürmesiyle eş merkezli) + boğaz 7,6 + yalak · POM milli helezon Ø70 hatve 50 + topuz → yaylı soket · göbek + 4 çubuk tarak · şeffaf PC 5 mm","→ 14,0 L kullanılabilir: kaşar 5,8 kg 1,3 gün (2 poz. 2,6) · kıyma 8,4 kg 2,9 gün · sucuk 7,7 kg 6,4 gün → robot ≈ 12 kap/hafta · kap başına 2 soket (helezon z 3,8 + tarak z 14) ya da tek motor + kayış — AÇIK · 3 kat × 2 · kap ARKAYA DAYALI · 2 kızak + 2 L raf · ÇATAL","#1d7a4f"),''',
    ''' ("⑧ ✓ TOPPING v25 yerleşim + v27 KAP (Picnic tipi): dış 14×68×24 · daire duvar R 6,5 + boğaz 7,6 + yalak · POM helezon Ø70 hatve 50 boy 66 + topuz → yaylı soket · göbek + 4 çubuk tarak · şeffaf PC 5 mm · KAPALI BORU ucu (y 62–67) + tek ağız 5×4,5 altta + yaylı menteşeli kapak + raf pimi Ø8 (yalnız TOPPING katında açılır) · kızaklar ±5 · ön çekme dudağı","→ 12,5 L kullanılabilir: kaşar 5,1 kg 1,1 gün (2 poz. 2,3) · kıyma 7,5 kg 2,6 gün · sucuk 6,9 kg 5,7 gün · kuşbaşı 4,3 kg 3 gün → robot ≈ 14 kap/hafta · kap başına 2 soket (helezon z 3,8 + tarak z 14) ya da tek motor + kayış — AÇIK · 3 kat × 2 · kap ARKAYA DAYALI · 2 kızak + 2 L raf · ÇATAL","#1d7a4f"),''')
rep(''' ("⑩ OVEN sadeyağ: tank ÜSTTE + 12 V pompa 8 W (püskürtme basınç ister) — AÇIK","→ cazibe yalnız damlatır; çekmeceler kalktı → teneke stoğu ×3 (4 ay)","#9a6b1f"),''',
    ''' ("⑩ ✓ OVEN v3 sadeyağ: KARTUŞ 4 L paslanmaz (16×16×18, ısıtma ceketi 45 °C, kuru bağlantı, kilit) — ELEMAN haftada 1 değiştirir (10 gün), ROBOT DOKUNMAZ · 24 V dişli pompa 0,5 L/dk + ısıtmalı hat Ø6 + çek valf + 90° nozül → Ø30 iz, 4 ml/0,5 sn","→ niş altı boş: robot tepsiyi sokar, 1 sn, çeker · stok 2,8 L/hafta (1 hafta çok değil, ikiye bölmeye gerek yok) · yedek boş kartuş + 16 kg teneke SERVICE'te oda sıcaklığı · şamandıra 'yağ az' → BEYİN","#1d7a4f"),''')
rep(''' ("⑪ 197 ✓ · 415 ✓ · derinlik 84 HER KABİN ✓ · TOPPING 3×(27+14) + 74 = 197 (kat 27 = kap 24 + kızak 2 + raf 0,2 + pay 0,8; ALT 74 = 20 + 27 + 27)","→ TOPPING derinlik 10 + 68 + 2 + 4 = 84 ✓ · STORE kaset katı 8 + 68 + 2 + 6 = 84 ✓ · TOPPING'de ayak yerine plint 12 (soğutma ızgarası)","#1d7a4f"),''',
    ''' ("⑪ 197 ✓ · 420 ✓ (OVEN 65 → 70: menteşe motorları + yan yalıtım 3) · derinlik 84 HER KABİN ✓ · TOPPING 3×(27+14) + 74 = 197 · OVEN 12 + 30 + 30 + 18 + 56 + 26 + 15 + 10 = 197 ✓","→ TOPPING derinlik 10 + 68 + 2 + 4 = 84 ✓ · STORE kaset katı 8 + 68 + 2 + 6 = 84 ✓ · OVEN fırın 60 + arka kanal 20 + yalıtım 2 = 84 ✓ · TOPPING ve OVEN'de ayak yerine plint 12 (ızgara) · OVEN ısı: bekleme 0,7 kW, egzoz +15 °C, günde 6–8 kWh mekâna (küçük radyatör kadar)","#1d7a4f"),''')
rep(''' ("⑬ ÇATAL ucu: 2 lama 16×12 mm × 50 cm + sırt plakası ≈ 2 kg · dizi: gir 50 → kaldır 0,5 → çek 70 (5° yatık taşıma) · 18 çift L raf (TOPPING 6 + ALT 8 + STORE 4)","→ haftalık (v26 kap): robot ≈ 12 kap değişimi (kaşar 5 · kıyma 3 · kuşbaşı 2 · sucuk 2) + 4 STORE→ALT taşıma (gece) · eleman haftada 1 (5 kaşar + 2 sucuk + 3+2 donmuş, boşları alır) · uç değiştirici PRESS alt yuvaları","#1d7a4f"),''',
    ''' ("⑬ ÇATAL ucu: 2 lama 16×12 mm × 50 cm + sırt plakası ≈ 2 kg · dizi: gir 50 → kaldır 0,5 → çek 70 (5° yatık taşıma) · 18 çift L raf (TOPPING 6 + ALT 8 + STORE 4) · çatal aralığı 10 (kızak ±5)","→ haftalık (v27 kap): robot ≈ 14 kap değişimi (kaşar 6 · kıyma 3 · kuşbaşı 2 · sucuk 1 + park) + 4 STORE→ALT taşıma (gece) · eleman haftada 1 (kaplar + OVEN yağ kartuşu, boşları alır) · uç değiştirici PRESS alt yuvaları","#1d7a4f"),''')
rep(''' ("⑫ Pide Ø30 → tepsi Ø32 zinciri: PRESS plaka Ø29 ✓ · PACK bıçak Ø28 ✓ · OVEN 44 (②) · robot tepsi eli v1 (Ø34) → v2 GEREK",''',
    ''' ("⑫ Pide Ø30 → tepsi Ø32 zinciri: PRESS plaka Ø29 ✓ · PACK bıçak Ø28 ✓ · OVEN 38 ✓ (kulp 6) · robot tepsi eli v1 (Ø34) → v2 GEREK (kulp 6 + çatal)",''')
rep("v26: yayıcı plaka mı spiral süpürme mi · gramaj prototipi (123 cm³/dev) · PC çizilme", "v27: yayıcı plaka mı spiral süpürme mi · gramaj prototipi (123 cm³/dev) · PC çizilme · OVEN: kuru bağlantı (CPC gıda tipi), karbon filtre, tepsili pide pilotu")
# docstring
rep('"""HAT v47 (v46 + TOPPING kap simgesi v26 Picnic tipi, ⑦ 15,4, ⑧ v26, robot ≈ 12 kap/hafta)', '"""HAT v48 (v47 + OVEN v3: kolon 70, hat 420, kartus, nis alti bos, plenum/fan/filtre, yan yalitim; TOPPING v27 sayilari, kizak ±5; ② ⑩ kapandi) — v47 (v46 + TOPPING kap simgesi v26 Picnic tipi, ⑦ 15,4, ⑧ v26, robot ≈ 12 kap/hafta)')
rep("rc(kx-10,ky-18,KW,px(1930),1.4,6,'#b3452b',None,'#fff8f5')", "_ki=len(E)")
NL=chr(10)
rep("    yy+=5"+NL+NL+"# ================= OLCULER + BASLIK =================",
    "    yy+=5"+NL+"E.insert(_ki, '<rect x=\"%.1f\" y=\"%.1f\" width=\"%.1f\" height=\"%.1f\" rx=\"6\" fill=\"#fff8f5\" stroke=\"#b3452b\" stroke-width=\"1.4\"/>' % (kx-10,ky-18,KW,yy-ky+22))"+NL+"_kbot=yy"+NL+NL+"# ================= OLCULER + BASLIK =================")
rep("W=int(X0+px(T)+px(2200)); H=int(YT2+px(1990))", "W=int(X0+px(T)+px(2200)); H=int(max(YT2+px(1990), _kbot+40))")
io.open(DST, 'w', encoding='utf-8').write(s)
print('teknik_cizim48.py yazildi')
