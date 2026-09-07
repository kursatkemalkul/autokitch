# -*- coding: utf-8 -*-
# HAT v49 = v48 + OVEN v4 (2 standart yag kabi sag/sol + pompalar arkada + sprey ortada; KESME presi OVEN'de; plenum/fan 12 + filtre 5 opsiyon; pano 20)
#           + PACK = sarjor 116 + kutulama (kesim kalkti) + KONTROL ④ ⑩ ⑪ ⑫
import io
SRC = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\_uretec\teknik_cizim48.py"
DST = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\_uretec\teknik_cizim49.py"
s = io.open(SRC, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    assert s.count(a) == cnt, ('%d != %d: ' % (s.count(a), cnt)) + a[:80]
    s = s.replace(a, b)

rep('hat_on_gorunus_teknik_v48.svg', 'hat_on_gorunus_teknik_v49.svg')
rep('"KONTROL — istasyonlar arası uyum (6 Eyl 2026, HAT v48)"', '"KONTROL — istasyonlar arası uyum (6 Eyl 2026, HAT v49)"')
rep('"AUTOKITCH — HAT v48 · TÜM İSTASYONLAR SON VERSİYON (6 Eyl 2026) — STORE v4 (+ v5 öneri) · PRESS v8 · TOPPING v25 yerleşim + v27 KAP (Picnic tipi, kapalı boru + menteşeli kapak) · OVEN v3 (Omake 2 kat · sadeyağ KARTUŞU · kolon 70) · PACK 116"',
    '"AUTOKITCH — HAT v49 · TÜM İSTASYONLAR SON VERSİYON (6 Eyl 2026) — STORE v4 (+ v5 öneri) · PRESS v8 · TOPPING v25 yerleşim + v27 KAP · OVEN v4 (Omake 2 kat · 2 STANDART YAĞ KABI + sprey ortada · KESME PRESİ · kolon 70) · PACK = şarjör 116 + kutulama"')
rep('· OVEN: kuru bağlantı tipi, karbon filtre tedariki, tepsili pide pilotu"', '· OVEN v4: kesme kuvveti pilotu · sadeyağ mı sıvı yağ mı · kuru bağlantı tipi"')
rep('"""HAT v48 (v47 + OVEN v3:', '"""HAT v49 (v48 + OVEN v4: 2 standart yag kabi sag/sol + pompalar arkada + sprey ortada, KESME presi OVEN, PACK = sarjor + kutulama, zonlar hesapla kuculdu) — v48 (v47 + OVEN v3:')

# ---- OVEN on gorunus v4 ----
i0 = s.index('# ================= 4 OVEN v3'); i1 = s.index('# ================= 5 PACK')
OVEN = r'''# ================= 4 OVEN v4 (Omake 2 kat · 2 STANDART YAĞ KABI + sprey ortada · KESME presi · plenum/fan 12 · filtre 5 opsiyon · yan yalıtım 3) =================
d0,d1=xs[3],xs[4]; dm=(d0+d1)/2; WD=d1-d0-px(40)
Zh=lambda z: YZ-px(z*10)          # zeminden cm -> y
for xs_ in (d0+4, d1-4-px(30)):
    rc(xs_,Zh(185),px(20),px(103*10),.6,0,'#b08968',None,'#f3f0e6'); rc(xs_+px(20),Zh(185),px(10),px(103*10),.5,0,'#7fb3d5',None,'#eef6fb')
ZON=[(0,12,'#e9e4d6','plint 12 — hava girişi ızgarası'),(12,32,'#e3f2fb','PANO 20 · PLC · menteşe ×2 + pres sürücüsü · 2 SSR · 2 pompa rölesi · 24 V'),(32,82,'#f4eef8',''),(82,112,'#fff8e0',''),(168,180,'#fde9c9','PLENUM 12 + FAN Ø120 (şart)'),(180,185,'#eef3f8','karbon filtre 5 (opsiyon)'),(185,197,'#f7f7f7','')]
for z0_,z1_,col,lab in ZON:
    rc(d0+px(30),Zh(z1_),d1-d0-px(60),px((z1_-z0_)*10),.8,0,'#555',None,col)
    if lab: notew(dm,Zh((z0_+z1_)/2)+2,lab,WD-px(40),5.2,'#333','middle','bold' if z0_ in (12,168) else '')
tx(dm,Zh(193.5)+2,'üst boşluk 12 (yedek)',4.6,'middle','','#333'); notew(dm,Zh(188.5)+2,'yan 3 = 2 yalıtım + 1 hava · egzoz üst ızgaradan mekâna (bacasız)',WD-px(30),4.2,'#555')
# fırın 64×56 (z 112-168), tepsi düzlemleri 117/145
rc(d0+px(30),Zh(168),px(640),px(560),2,3,'#111',None,'#f4f4f4')
for zk0,zk1,nm,tp in ((112,140,'KAPAK 1 · alt kat',117),(140,168,'KAPAK 2 · üst kat',145)):
    rc(d0+px(65),Zh(zk1-4),px(570),px((zk1-zk0-8)*10),1.2,1,'#333',None,'#dbeeff')
    rc(d0+px(65),Zh(zk0+4)+px(12),px(570),px(12),.8,0,'#333',None,'#999')
    tx(dm,Zh((zk0+zk1)/2)+2,nm+' · hazne 40×40×10 · tepsi düzlemi %d' % tp,5.2,'middle','bold','#333')
    rc(d1-4-px(27),Zh(zk0+7),px(24),px(60),1,1,'#c0392b',None,'#f7d7d7')
tx(d1-px(40),Zh(169.2)+2,'menteşe motoru ×2 Ø28 (yan aralıkta)',4.2,'end','','#c0392b')
ci(dm-px(230),Zh(174),px(50),1,'#333',None,'#fff'); tx(dm-px(230),Zh(174)+2,'FAN',4,'middle','bold')
# YAĞ + SPREY 30 (z 82-112): 2 standart kap yanlarda (slot 15), tepsi ortada (34), nozül üstte, klape 4 önde, sıcak dolap 42
for x0_ in (35, 525):
    rc(d0+px(x0_),Zh(108),px(140),px(240),1.1,1,'#c9a227',None,'#dbeeff'); rc(d0+px(x0_+5),Zh(102),px(130),px(170),0,0,'none',None,'#f6d76b')
    for dx_ in (20,120): rc(d0+px(x0_+dx_-15),Zh(84),px(30),px(20),.6,0,'#555',None,'#d0d7de')
    ln(d0+px(x0_-6),Zh(82),d0+px(x0_+146),Zh(82),1.2,'#555')
    tx(d0+px(x0_+70),Zh(96)+2,'YAĞ KABI',4.6,'middle','bold','#8a6a3a'); tx(d0+px(x0_+70),Zh(91)+2,'10 L · 25 gün',4,'middle','','#8a6a3a')
ci(dm,Zh(106),px(30),1,'#c9a227',None,'#fff8e0')
E.append('<polygon points="%.1f,%.1f %.1f,%.1f %.1f,%.1f" fill="#fff3c4" fill-opacity="0.5" stroke="#c9a227" stroke-width="0.6"/>' % (dm,Zh(106),dm-px(150),Zh(90),dm+px(150),Zh(90)))
tray(dm,Zh(90),kulp=False)
rc(d0+px(190),Zh(85),px(320),px(15),.6,0,'#555',None,'#ccc')
tx(dm,Zh(110.5)+2,'YAĞ + SPREY 30 · slot 15 | tepsi 34 | slot 15 · klape 4 · sıcak dolap 42 °C',4.4,'middle','bold','#b7791f')
tx(dm,Zh(86.5)+2,'damlalık',3.6,'middle','','#555')
# KESME 50 (z 32-82): zemin plakası + halka, tepsi, pide, bıçak yıldızı +, kızak, 2 mil, aktüatör dikey
rc(d0+px(120),Zh(36),px(460),px(20),1,0,'#333',None,'#bbb')
tray(dm,Zh(36),kulp=False)
E.append('<path d="M %.1f %.1f A %.1f %.1f 0 0 1 %.1f %.1f Z" fill="#f0d9a8" stroke="#8a6a3a" stroke-width="0.8"/>' % (dm-px(150),Zh(36),px(150),px(40),dm+px(150),Zh(36)))
rc(d0+px(210),Zh(48),px(280),px(40),1,0,'#333',None,'#e8e8e8'); ln(d0+px(210),Zh(44),d0+px(490),Zh(44),1.4,'#111')
rc(d0+px(320),Zh(51),px(60),px(30),.8,1,'#333',None,'#ccc'); rc(d0+px(170),Zh(54),px(360),px(30),1,0,'#333',None,'#ddd')
for xg in (190,510): ln(d0+px(xg),Zh(34),d0+px(xg),Zh(72),1.6,'#555'); rc(d0+px(xg-12),Zh(54),px(24),px(30),.6,0,'#333',None,'#999')
rc(d0+px(310),Zh(78),px(80),px(210),1.2,2,'#6b4fa8',None,'#ece6f5'); ln(dm,Zh(54),dm,Zh(57),2,'#6b4fa8')
tx(d0+px(405),Zh(73)+2,'AKTÜATÖR 24 V',4,'start','bold','#6b4fa8'); tx(d0+px(405),Zh(68)+2,'1500 N · 100 mm',3.8,'start','','#6b4fa8'); tx(d0+px(405),Zh(63)+2,'kendini kilitler',3.8,'start','','#6b4fa8')
tx(dm,Zh(80.5)+2,'KESME 50 · bıçak + (2 × 28) · tepsi zemine dayanır · 0,85–1,1 kN',4.4,'middle','bold','#6b4fa8')
tx(d0+px(100),Zh(45)+2,'bıçak',3.6,'end','','#333'); tx(d0+px(100),Zh(38)+2,'pide',3.6,'end','','#8a6a3a'); tx(d0+px(100),Zh(55)+2,'kızak',3.6,'end','','#333')
# hava
for xx_ in (d0+px(19), d1-px(19)):
    ln(xx_,Zh(6),xx_,Zh(30),1,'#7fb3d5'); E.append('<path d="M %.1f %.1f l -3 6 h 6 z" fill="#7fb3d5"/>' % (xx_,Zh(30)))
ln(dm+px(230),Zh(187),dm+px(230),Zh(196),1.2,'#1a49b8'); E.append('<path d="M %.1f %.1f l -3 6 h 6 z" fill="#1a49b8"/>' % (dm+px(230),Zh(196)))

'''
s = s[:i0] + OVEN + s[i1:]

# ---- PACK on gorunus: kesim kalkti ----
i0 = s.index('# ================= 5 PACK'); i1 = s.index('# ================= UST GORUNUM')
PACK = r'''# ================= 5 PACK v49 (kesim OVEN'e taşındı · şarjör 116 · kutulama) =================
e0,e1=xs[4],xs[5]; em=(e0+e1)/2; WE=e1-e0-px(40)
rc(e0+px(30),Y0+px(20),e1-e0-px(60),px(260),1,3,'#999','5,4'); tx(em,Y0+px(125),'BOŞ 26',8,'middle','bold','#999')
notew(em,Y0+px(165),"kesim OVEN'e taşındı (v4 KESME presi z 32–82) · ileride: 2. şarjör ya da poşet",WE,5.4,'#999')
rc(em-px(200),Y0+px(330),px(400),px(35),1.4,3,'#777',None,'#eee')
tray(em,Y0+px(332),kulp=True)
rc(em-px(160),Y0+px(405),px(320),px(45),1.2,2,'#8a6a3a',None,'#fbf3e6'); notew(em,Y0+px(472),'AÇIK KUTU 32×32×4,5 · tepsi eğilir, 4 parça kayar · ön ağız 13',WE,5.6,'#8a6a3a')
notew(em,Y0+px(303),'KUTULAMA yuvası — tepsi oturur, eğilir',WE,5.8)
for r in range(29):
    for kx in (e0+8, e0+8+px(320)+4): rc(kx,Y0+px(560)+r*px(44),px(320),px(44),1.05)
notew(em,Y0+px(505),'ŞARJÖR: katlanmış kutu 2×2×29 = 116 — ELEMAN katlar (ıslak mendil içinde) · açık deste YOK',WE,5.6)

'''
s = s[:i0] + PACK + s[i1:]

# ---- OVEN ust v4 ----
i0 = s.index('# OVEN ust v3'); i1 = s.index('# PACK ust')
OVU = r'''# OVEN ust v4: fırın 64×60 önde + arka kanal 20 + arka yalıtım 2; altta (kesik): 2 yağ kabı 68 yanlarda + pompalar arkada, tepsi ortada
rc(d0+px(30),YT2+px(20),px(640),px(600),1.6,2,'#111',None,'#f4f4f4')
rc(d0+px(30),YT2+px(640),px(640),px(180),.8,0,'#7fb3d5',None,'#eef6fb'); tx(dm,YT2+px(735),'arka kanal 20: hava + kablo + buhar',5,'middle','','#1a49b8')
for xs_ in (d0+4, d1-4-px(30)): rc(xs_,YT2,px(30),px(840),.6,0,'#b08968',None,'#f3f0e6')
rd(dm-px(200),YT2+px(120),px(400),px(400))
ci(dm,YT2+px(320),px(160),1.2,'#1a49b8','4,3'); rc(dm-px(15),YT2+px(480),px(30),px(60),1,1,'#1a49b8'); tx(dm+px(50),YT2+px(560),'kulp 6 (v2 el)',5,'start','','#1a49b8')
tx(dm,YT2+px(90),'kavite 40×40 (kesik) · fırın 64×60',5.2,'middle','','#555')
for x0_ in (35,525):
    rc(d0+px(x0_),YT2+px(40),px(140),px(680),1,2,'#c9a227','4,3','none'); tx(d0+px(x0_+70),YT2+px(400),'yağ kabı',4.4,'middle','','#8a6a3a'); tx(d0+px(x0_+70),YT2+px(430),'68 (alt, kesik)',4,'middle','','#8a6a3a')
    rc(d0+px(x0_+20),YT2+px(730),px(100),px(90),.8,2,'#333','3,2','none'); tx(d0+px(x0_+70),YT2+px(785),'pompa',3.8,'middle','','#333')
notew(dm,YN,"fırın 64×60 + arka kanal 20 + yalıtım 2 = 84 · alt zon: 2 yağ kabı 68 (slot 15) + kuru bağlantı + pompalar arkada, tepsi Ø32 ortada (34) · fırında tepsi + kulp 6 = 38 ≤ 40 ✓",d1-d0-20,7)
'''
s = s[:i0] + OVU + s[i1:]

# ---- PACK ust ----
i0 = s.index('# PACK ust'); i1 = s.index('# ROBOT KORIDORU')
PKU = r'''# PACK ust v49: kutulama yuvası önde (tepsi Ø32 + açık kutu), şarjör 2×2 arkada (kesik); kesim yok
rc(em-px(200),YT2+px(440),px(400),px(400),1.4,4,'#777')
ci(em,YT2+px(640),px(160),1.2,'#1a49b8','4,3'); rc(em-px(160),YT2+px(480),px(320),px(320),1,2,'#8a6a3a','4,3')
for yy_ in (60,390): rd(e0+8,YT2+px(yy_),px(320),px(320)); rd(e0+8+px(320)+4,YT2+px(yy_),px(320),px(320))
tx(em,YT2+px(50),'şarjör 2×2 (kesik, z 52-182)',5,'middle','','#777')
notew(em,YN,"kutulama yuvası (tepsi Ø32 + açık kutu 32×32) önde · şarjör 2×2 arkada (kesik) · kesim OVEN'de",e1-e0-20,7)
'''
s = s[:i0] + PKU + s[i1:]

# ---- KONTROL ----
rep(''' ("④ ✓ PACK: bıçak yıldızı Ø28 yatay, önden ince plaka; açık deste kalktı → şarjör 2×2×29 = 116 kutu (eleman katlar)","→ kesim yuvası tepsi Ø32 + yuva pimleri","#1d7a4f"),''',
    ''' ("④ ✓ PACK = şarjör 2×2×29 = 116 kutu (eleman katlar) + kutulama (tepsi eğilir, 4 parça kayar) — KESİM OVEN'e taşındı (v4 KESME presi z 32–82)","→ pres: bıçak yıldızı + (2 × 28, paslanmaz 1,2 mm) · 24 V lineer aktüatör 1500 N, strok 100 mm, kendini kilitler · kuvvet 56 cm × 15–20 N/cm = 0,85–1,1 kN · tepsi zemin plakasına dayanır, robot yalnız kulpu tutar · PACK'te 26 cm boşaldı","#1d7a4f"),''')
rep(''' ("⑩ ✓ OVEN v3 sadeyağ: KARTUŞ 4 L paslanmaz (16×16×18, ısıtma ceketi 45 °C, kuru bağlantı, kilit) — ELEMAN haftada 1 değiştirir (10 gün), ROBOT DOKUNMAZ · 24 V dişli pompa 0,5 L/dk + ısıtmalı hat Ø6 + çek valf + 90° nozül → Ø30 iz, 4 ml/0,5 sn","→ niş altı boş: robot tepsiyi sokar, 1 sn, çeker · stok 2,8 L/hafta (1 hafta çok değil, ikiye bölmeye gerek yok) · yedek boş kartuş + 16 kg teneke SERVICE'te oda sıcaklığı · şamandıra 'yağ az' → BEYİN","#1d7a4f"),''',
    ''' ("⑩ ✓ OVEN v4 sadeyağ: 2 STANDART KAP (yağ versiyonu: helezon/tarak yok, taban kapalı, geçmeli kapak + dolum ağzı, arka soket = kuru bağlantı, şamandıra) sağ/sol slot 15, 10 L = 25 gün (max 12 L = 30), dolu 12,3 kg — ELEMAN ayda 1 değiştirir, ROBOT DOKUNMAZ · 2 mini pompa 24 V arka duvarda, BEYİN biri boşalınca diğerine geçer","→ sprey ortada (34): nozül 20 derinlikte, tepsi 40 girer, 4 ml / 0,5 sn · zon = sıcak dolap 42 °C (klape 4; sadeyağ 32 °C altında katı, pompalanmaz; pide için sıcak şart değil) · hat ısıtması yok (dolapta) · damlalık haftalık · alternatif: sıvı yağ → ısıtıcı yok (lezzet kararı)","#1d7a4f"),''')
rep(''' ("⑪ 197 ✓ · 420 ✓ (OVEN 65 → 70: menteşe motorları + yan yalıtım 3) · derinlik 84 HER KABİN ✓ · TOPPING 3×(27+14) + 74 = 197 · OVEN 12 + 30 + 30 + 18 + 56 + 26 + 15 + 10 = 197 ✓","→ TOPPING derinlik 10 + 68 + 2 + 4 = 84 ✓ · STORE kaset katı 8 + 68 + 2 + 6 = 84 ✓ · OVEN fırın 60 + arka kanal 20 + yalıtım 2 = 84 ✓ · TOPPING ve OVEN'de ayak yerine plint 12 (ızgara) · OVEN ısı: bekleme 0,7 kW, egzoz +15 °C, günde 6–8 kWh mekâna (küçük radyatör kadar)","#1d7a4f"),''',
    ''' ("⑪ 197 ✓ · 420 ✓ · derinlik 84 HER KABİN ✓ · TOPPING 3×(27+14) + 74 = 197 · OVEN v4 zeminden: plint 12 + pano 20 + KESME 50 + YAĞ/SPREY 30 + fırın 56 + plenum/fan 12 + filtre 5 + yedek 12 = 197 ✓ (v3'e göre plenum+filtre+üst 51 → 17, pano 30 → 20, niş 18 kalktı)","→ OVEN derinlik: fırın 60 + arka kanal 20 + yalıtım 2 = 84 ✓ · yağ zonu: kap 68 + kuru bağlantı 4 + pompa 12 = 84 ✓ · genişlik 15 + 34 + 15 = 64 ✓ · TOPPING 10 + 68 + 2 + 4 = 84 ✓ · STORE kaset 8 + 68 + 2 + 6 = 84 ✓ · fan ŞART (kabin ısısı), karbon filtre OPSİYON (AVM), baca YOK (elektrikli) · ısı mekâna günde 6–8 kWh","#1d7a4f"),''')
rep("PACK bıçak Ø28 ✓ · OVEN 38 ✓ (kulp 6)", "OVEN kesme bıçağı Ø28 ✓ (PACK'ten taşındı) · OVEN fırın 38 ✓ (kulp 6)")
rep("· OVEN: kuru bağlantı (CPC gıda tipi), karbon filtre, tepsili pide pilotu", "· OVEN v4: kesme kuvveti pilotu (15–20 N/cm varsayım) · sadeyağ mı sıvı yağ mı · PC gövde + 42 °C yağ (pilot) · kuru bağlantı tipi · PACK'te boşalan 26 cm")
io.open(DST, 'w', encoding='utf-8').write(s)
print('teknik_cizim49.py yazildi')
