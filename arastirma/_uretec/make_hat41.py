# -*- coding: utf-8 -*-
# v40 -> v41 (Kemal, 4 Eyl): PRESS v6 (3 tepsi: yatay raf 2 yan yana + ustunde cop + 3 uc yuvasi) · TOPPING v9 (sogutma 15,
# elektrik 12, dozaj boslugu 14, gecis rafi 3 kat) · OVEN (sadeyag tanki nozulun USTUNDE, cazibe, pompa yok; sprey nisi 14) ·
# STORE v39 (-18 bolmesi 5. raf: 4 donmus kaset; 1L cekmecesi sag kolona) · KONTROL guncel
import io
NL = chr(10)
t = io.open('teknik_cizim40.py', encoding='utf-8').read()
def rep(o, n, c=1):
    global t
    assert t.count(o) == c, 'A(%d): %s' % (t.count(o), o[:80])
    t = t.replace(o, n)
def block(start_marker, end_marker, lines):
    global t
    s = t.index(start_marker); e = t.index(end_marker)
    t = t[:s] + NL.join(lines) + NL + NL + t[e:]

# ================= STORE v39 =================
block("# ================= 1 STORE", "# ================= 2 PRESS", [
"# ================= 1 STORE v39 (-18: 4 hamur rafi + 5. raf donmus kasetler; 1L cekmecesi sag kolon altina) =================",
"a0,a1=xs[0],xs[1]; am=a0+px(700)",
"rc(a0+8,Y0+px(10),a1-a0-16,px(290),1.6)",
"ci(a0+px(350),Y0+px(150),px(78),1.2); ci(a0+px(1050),Y0+px(150),px(78),1.2)",
"ln(a0+px(312),Y0+px(112),a0+px(388),Y0+px(188),.9); ln(a0+px(312),Y0+px(188),a0+px(388),Y0+px(112),.9)",
"ln(a0+px(1012),Y0+px(112),a0+px(1088),Y0+px(188),.9); ln(a0+px(1012),Y0+px(188),a0+px(1088),Y0+px(112),.9)",
"for g in range(4): ln(a0+20,Y0+px(230)+g*px(15),a1-20,Y0+px(230)+g*px(15),.7)",
"rc(a0+8,Y0+px(310),a1-a0-16,px(1530),1.8)",
"rc(am-px(35),Y0+px(310),px(70),px(1530),1.2)",
"rc(a0+px(60),Y0+px(370),am-px(35)-a0-px(60),px(820),1)",
"rc(a0+8,Y0+px(1190),am-px(35)-a0-8,px(50),1.6)",
"for kz in range(11):",
"    ln(a0+px(60),Y0+px(420)+kz*px(70),a0+px(85),Y0+px(420)+kz*px(70),.8)",
"    ln(am-px(85),Y0+px(420)+kz*px(70),am-px(60),Y0+px(420)+kz*px(70),.8)",
"for r in range(4):",
"    ty=Y0+px(490)+r*px(120)",
"    ln(a0+px(72),ty,am-px(72),ty,1.2)",
"    ln(a0+px(72),ty,a0+px(72),ty-px(20),1.2); ln(am-px(72),ty,am-px(72),ty-px(20),1.2)",
"    rc((a0+am)/2-px(80),ty+px(5),px(160),px(14),.9,2)",
"    for i in range(4):",
"        ci(a0+px(175)+i*px(125),ty-px(48),px(46),1)",
"        el(a0+px(175)+i*px(125),ty-px(2),px(56),px(8),.8)",
"# 5. raf: 4 donmus kucuk kaset (kavurma x2, kusbasi x2) — onde 2, arkada 2 (kesik)",
"ln(a0+px(72),Y0+px(1170),am-px(72),Y0+px(1170),1.2); rc((a0+am)/2-px(80),Y0+px(1174),px(160),px(14),.9,2)",
"for i in range(2):",
"    rc(a0+px(100)+i*px(180),Y0+px(905),px(170),px(250),1,2,'#1a49b8','4,3')",
"    rc(a0+px(90)+i*px(180),Y0+px(918),px(170),px(250),1.3,2,'#1a49b8',None,'#eef2fb')",
"    tx(a0+px(175)+i*px(180),Y0+px(1035),['KAV','KUŞ'][i]+' −18',7.5,'middle','bold','#1a49b8')",
"    tx(a0+px(175)+i*px(180),Y0+px(1060),'×2 (arka kesik)',6.5,'middle','','#1a49b8')",
"rc(a0+px(470),Y0+px(918),px(150),px(250),1,2,'#999','4,3'); tx(a0+px(545),Y0+px(1045),'büyüme',6.5,'middle','','#999')",
"tx((a0+am)/2,Y0+px(895),'① ✓ 5. RAF: 4 donmuş kaset 17×21×25 (kavurma ×2 · kuşbaşı ×2) — robot bitişten 1 gün önce alır',6.5,'middle','bold','#1d7a4f')",
"not_((a0+am)/2,Y0+px(332),'DONMUŞ −18° · 4 raf hamur = 80 (1 GÜN) + 5. raf TOPPING kasetleri',fs=8)",
"not_((a0+am)/2,Y0+px(1230),'yatay izoleli ayırıcı — altı +3 °C',fs=8)",
"for k4 in range(4):",
"    cy4=Y0+px(1260)+k4*px(135)",
"    rc(a0+px(30),cy4,am-px(62)-a0,px(120),1.4,3)",
"    for i in range(7): rc(a0+px(40)+i*px(78),cy4+px(6),px(64),px(108),1)",
"not_((a0+am)/2,Y0+px(1252),'İÇECEK+TATLI — 4 çekmece × 7 kanal = 28 (kutu 24 · tatlı 3 · yedek 1)',fs=7.5)",
"a2,a3=am,xs[1]",
"ln(a2+12,Y0+px(310),a3-15,Y0+px(310),1)",
"ln(a2+px(35),Y0+px(315),a3-15,Y0+px(315),1.4)",
"ln(a2+px(35),Y0+px(1455),a3-15,Y0+px(1455),1.4)",
"rc(a2+px(40),Y0+px(360),a3-px(60)-a2-px(40),px(1080),1)",
"for kz in range(20):",
"    ln(a2+px(60),Y0+px(405)+kz*px(70),a2+px(85),Y0+px(405)+kz*px(70),.8)",
"    ln(a3-px(85),Y0+px(405)+kz*px(70),a3-px(60),Y0+px(405)+kz*px(70),.8)",
"for r in range(8):",
"    ty=Y0+px(490)+r*px(130)",
"    ln(a2+px(72),ty,a3-px(72),ty,1.2)",
"    ln(a2+px(72),ty,a2+px(72),ty-px(22),1.2); ln(a3-px(72),ty,a3-px(72),ty-px(22),1.2)",
"    rc((a2+a3)/2-px(80),ty+px(6),px(160),px(16),.9,2)",
"    for i in range(4):",
"        ci(a2+px(175)+i*px(125),ty-px(52),px(50),1)",
"        el(a2+px(175)+i*px(125),ty-px(3),px(58),px(9),.8)",
"not_((a2+a3)/2,Y0+px(340),'TAZE +3 °C · 8 raf × 20 = 160 (2 GÜN)')",
"rc(a2+px(40),Y0+px(1480),a3-px(62)-a2-px(40),px(350),1.6,3)",
"for i in range(5): rc(a2+px(62)+i*px(104),Y0+px(1498),px(84),px(314),1)",
"not_((a2+a3)/2,Y0+px(1472),'1L çekmecesi — 5 kanal × 8 (SOL kolondan buraya: −18\\'e yer açıldı)',fs=7.5)",
])

# ================= PRESS v6 =================
block("# ust bolge: sol TEPSI RAFI YATAY + PENCE (0-365) / sag COP (365-700)", "# ================= 3 TOPPING", [
"# ust bolge v6: sol huni+kova (x 20-360) · sag 3 uc yuvasi (x 380-680) · alt bant y 810-890 TEPSI RAFI (2 tepsi yan yana)",
"xB=b0+px(370); ln(xB,Y0+px(50),xB,Y0+px(795),1.1,'#111','6,5')",
"ln(b0+px(15),Y0+px(800),b1-px(15),Y0+px(800),1.1,'#111','6,5')",
"tx(b0+px(190),Y0+px(92),'ÇÖP',9.5,'middle','bold')",
"ln(b0+px(40),Y0+px(115),b0+px(110),Y0+px(300),1.6); ln(b0+px(340),Y0+px(115),b0+px(270),Y0+px(300),1.6); ln(b0+px(40),Y0+px(115),b0+px(340),Y0+px(115),1.6)",
"not_(b0+px(190),Y0+px(200),'huni — bırak-geç',fs=7)",
"rc(b0+px(75),Y0+px(330),px(230),px(450),1.6,4); tx(b0+px(190),Y0+px(560),'KOVA 30 L',9.5,'middle','bold'); not_(b0+px(190),Y0+px(620),'motorsuz · eleman HER GÜN',fs=7)",
"for k,(ad,dash) in enumerate((('1 · PENÇE',None),('2 · YEDEK PENÇE',None),('3 · BOŞ (büyüme)','4,3'))):",
"    y0_=Y0+px(70+k*245)",
"    rc(b0+px(390),y0_,px(290),px(220),1.3,3,'#999' if dash else '#111',dash)",
"    tx(b0+px(535),y0_+px(32),ad,7.5,'middle','bold','#999' if dash else '#111')",
"    if k<2:",
"        rc(b0+px(490),y0_+px(60),px(90),px(35),1.1,2); ln(b0+px(505),y0_+px(95),b0+px(515),y0_+px(160),1.2); ln(b0+px(565),y0_+px(95),b0+px(555),y0_+px(160),1.2)",
"not_(b0+px(535),Y0+px(780),'kilit pim+burç · \"uç var\" sensörü',fs=6.5)",
"tx(bm,Y0+px(826),'TEPSİ RAFI — YATAY · 2 yuva yan yana (+1 kolda = 3 tepsi)',7.5,'middle','bold','#1a49b8')",
"for i in range(2):",
"    cx_=b0+px(180+i*340)",
"    rc(cx_-px(172),Y0+px(848),px(14),px(14),1,1); rc(cx_+px(158),Y0+px(848),px(14),px(14),1,1)",
"    el(cx_,Y0+px(855),px(165),px(9),1.3,'#1a49b8'); rc(cx_-px(12),Y0+px(850),px(24),px(10),.8,1,'#1a49b8',None,'#dfe7fb')",
"not_(bm,Y0+px(880)+8,'kulp öne · kilit üstten · press plakası ısıtmalı → tepsi soğuma beklemez (v6)',fs=6.5)",
])

# ================= TOPPING v9 =================
block("# ================= 3 TOPPING", "# ================= 4 OVEN", [
"# ================= 3 TOPPING v9 (sogutma 15 minibar sinifi · elektrik 12 · kaset 25 · cark 21 · ACIK BOSLUK 14 · gecis rafi 3 kat) =================",
"c0,c1=xs[2],xs[3]; cm2=(c0+c1)/2",
"tx(cm2,Y0+px(35),'SOĞUTMA (ÜSTTE) 15 — minibar sınıfı 1/12 HP ~80 W · +3 °C · buzluk YOK',7.5,'middle','bold')",
"rc(c0+px(60),Y0+px(48),px(150),px(100),1.2,3); ci(c0+px(135),Y0+px(98),px(35),1)",
"rc(c0+px(240),Y0+px(48),px(220),px(100),1.2,3); tx(c0+px(350),Y0+px(103),'kondenser',6.5)",
"rc(c0+px(490),Y0+px(48),px(150),px(100),1.2,3); ci(c0+px(565),Y0+px(98),px(30),1)",
"ln(c0+px(15),Y0+px(160),c1-px(15),Y0+px(160),1,'#111','6,4')",
"tx(cm2,Y0+px(188),'ELEKTRİK 12 · PLC I/O · 4 step sürücü · 24 V',7.5,'middle','bold')",
"rc(c0+px(50),Y0+px(200),px(150),px(70),1.1,2); tx(c0+px(125),Y0+px(242),'PLC',7)",
"for i in range(4): rc(c0+px(225+i*70),Y0+px(200),px(55),px(70),1,2)",
"rc(c0+px(525),Y0+px(200),px(120),px(70),1.1,2); tx(c0+px(585),Y0+px(242),'PSU',7)",
"ln(c0+px(15),Y0+px(290),c1-px(15),Y0+px(290),1.6)",
"KY=300",
"kaset(c0+px(355),Y0+px(KY-8),px(165),px(250),'KAVURMA arka',dash='4,3',c='#888')",
"kaset(c0+px(525),Y0+px(KY-8),px(165),px(250),'KUŞBAŞI arka',dash='4,3',c='#888')",
"kaset(c0+px(10),Y0+px(KY),px(335),px(250),'KAŞAR A','35×42×25 · 15 kg')",
"kaset(c0+px(355),Y0+px(KY),px(335),px(250),'SUCUK (ön)','35×21×25 · 10 kg')",
"CY=KY+320",
"ln(c0+px(15),Y0+px(KY+252),c0+px(150),Y0+px(CY-55),1.2); ln(c0+px(340),Y0+px(KY+252),c0+px(255),Y0+px(CY-55),1.2)",
"ln(c0+px(360),Y0+px(KY+252),c0+px(430),Y0+px(CY-40),1.2); ln(c0+px(685),Y0+px(KY+252),c0+px(510),Y0+px(CY-40),1.2)",
"for cx0,r in ((200,55),(470,40)):",
"    ci(c0+px(cx0),Y0+px(CY),px(r),1.6)",
"    for k in range(6):",
"        a=k*math.pi/3; ln(c0+px(cx0),Y0+px(CY),c0+px(cx0)+px(r)*math.cos(a),Y0+px(CY)+px(r)*math.sin(a),.9)",
"    ln(c0+px(cx0-16),Y0+px(CY+60),c0+px(cx0-16),Y0+px(CY+150),1.3); ln(c0+px(cx0+16),Y0+px(CY+60),c0+px(cx0+16),Y0+px(CY+150),1.3)",
"for cx0 in (400,520):",
"    ci(c0+px(cx0),Y0+px(CY-20),px(35),1,'#999','4,3')",
"    ln(c0+px(cx0-13),Y0+px(CY+15),c0+px(cx0-13),Y0+px(CY+150),.9,'#999','4,3'); ln(c0+px(cx0+13),Y0+px(CY+15),c0+px(cx0+13),Y0+px(CY+150),.9,'#999','4,3')",
"rc(c0+px(120),Y0+px(CY-20),px(45),px(40),1.1,2); tx(c0+px(142),Y0+px(CY+5),'M',7,'middle','bold')",
"rc(c0+px(535),Y0+px(CY-20),px(45),px(40),1.1,2); tx(c0+px(557),Y0+px(CY+5),'M',7,'middle','bold')",
"FL=CY+120",
"ln(c0+px(15),Y0+px(FL),c1-px(15),Y0+px(FL),1.6)",
"tx(cm2,Y0+px(FL-8),'soğuk kabin tabanı · 4 ağız 3 cm sarkar',6,'middle','','#888')",
"# ACIK DOZAJ BOSLUGU 14 cm: tepsi + pide + dusme 3 + bilek payi",
"tray(c0+px(200),Y0+px(FL+95),kulp=True)",
"rc(c0+px(430),Y0+px(FL+55),px(55),px(28),1.1,2,'#1a49b8'); tx(c0+px(457),Y0+px(FL+73),'kilit',5.5,'middle','','#1a49b8')",
"tx(c0+px(560),Y0+px(FL+50),'⑨ ✓ boşluk 14',6.5,'middle','bold','#1d7a4f')",
"tx(c0+px(560),Y0+px(FL+72),'(26 → 14)',6,'middle','','#1d7a4f')",
"tx(c0+px(100),Y0+px(FL+50),'AÇIK BOŞLUK · ③ karar',6,'middle','bold','#1a49b8')",
"GY=FL+140",
"ln(c0+px(15),Y0+px(GY),c1-px(15),Y0+px(GY),1,'#111','6,4')",
"tx(cm2,Y0+px(GY+22),'GEÇİŞ RAFI (robot takas · ayrı soğuk bölme) 3 kat',7.5,'middle','bold','#1a49b8')",
"kaset(c0+px(10),Y0+px(GY+35),px(335),px(250),'KAŞAR B','dolu +3')",
"kaset(c0+px(355),Y0+px(GY+35),px(335),px(250),'KAŞAR C','dolu +3')",
"kaset(c0+px(10),Y0+px(GY+310),px(335),px(250),'KAŞAR D','dolu +3')",
"kaset(c0+px(355),Y0+px(GY+310),px(335),px(250),'SUCUK yedek','haftalık')",
"kaset(c0+px(10),Y0+px(GY+585),px(165),px(250),'ÇÖZÜLME 1','kavurma',fs=7)",
"kaset(c0+px(185),Y0+px(GY+585),px(165),px(250),'ÇÖZÜLME 2','kuşbaşı',fs=7)",
"kaset(c0+px(360),Y0+px(GY+585),px(330),px(250),'büyüme: 5. malzeme','',dash='4,3',c='#999')",
"not_(cm2,Y0+px(1832),'14 kaset döner · donmuşlar STORE −18 · derinlik 55 (önü geride)',fs=6.5)",
])

# ================= OVEN: sadeyag tanki ustte, cazibe =================
block("rc(d0+px(25),Y0+px(1180),d1-d0-px(50),px(190),1.6)", "rc(d0+px(40),Y0+px(20),d1-d0-px(80),px(115),1.4,3); ci(dm,Y0+px(77),px(42),1.1)", [
"rc(d0+px(25),Y0+px(1180),d1-d0-px(50),px(110),1.6)",
"rc(d0+px(45),Y0+px(1195),px(230),px(80),1.4,3,'#c9a227',None,'#fff8e0'); tx(d0+px(160),Y0+px(1230),'TANK 4 L',7,'middle','bold','#8a6a3a'); tx(d0+px(160),Y0+px(1255),'45 °C ısıtıcı',6,'middle','','#8a6a3a')",
"rc(d0+px(300),Y0+px(1195),px(120),px(80),1,2); rc(d0+px(440),Y0+px(1195),px(120),px(80),1,2); tx(d0+px(430),Y0+px(1240),'teneke ×2',6,'middle','','#555')",
"tx(dm,Y0+px(1172),'⑩ ✓ SADEYAĞ ÜSTTE — cazibe akış, pompa YOK · solenoid vana',6.5,'middle','bold','#1d7a4f')",
"rc(dm-px(22),Y0+px(1290),px(44),px(28),1.3); ln(dm,Y0+px(1318),dm,Y0+px(1338),1.4)",
"rc(d0+px(25),Y0+px(1325),d1-d0-px(50),px(145),1.4)",
"ln(dm,Y0+px(1338),dm-px(100),Y0+px(1420),1,'#111','4 4'); ln(dm,Y0+px(1338),dm+px(100),Y0+px(1420),1,'#111','4 4')",
"tray(dm,Y0+px(1432),kulp=True)",
"not_(dm,Y0+px(1462),'sprey nişi 14 — tepsi 2 sn geçer, yağ sıcak pidede erir',fs=6.5)",
"for k in range(3):",
"    rc(d0+18,Y0+px(1490)+k*px(115),d1-d0-36,px(100),1.4)",
"    ln(dm-22,Y0+px(1490)+k*px(115)+px(50),dm+22,Y0+px(1490)+k*px(115)+px(50),2)",
"not_(dm,Y0+px(1482),'servis çekmeceleri + teneke stoğu',fs=6.5)",
])
rep('not_(dm,Y0+px(1172),"sadeyağ sprey — sıcak pide TEPSİDE geçer, yağ erir",fs=8)' + NL, '')
rep('not_(dm,Y0+px(1412),"sadeyağ teneke ×3 + pompa·ısıtıcı",fs=8)' + NL, '')
rep('not_(dm,Y0+px(1638),"servis çekmeceleri",fs=8)' + NL, '')

# ================= UST GORUNUM: PRESS tepsi rafi 2 yan yana =================
rep("rc(b0+px(25),YT2+px(380),px(340),px(460),1.2,2,'#1a49b8','5,4'); tx(b0+px(195),YT2+px(600),'tepsi rafı 36×46 (üst)',7,'middle','','#1a49b8')",
    "ci(b0+px(180),YT2+px(560),px(170),1.1,'#1a49b8','5,4'); ci(b0+px(520),YT2+px(560),px(170),1.1,'#1a49b8','5,4'); tx(bm,YT2+px(790),'tepsi rafı: 2 yan yana (üst, kesik)',7,'middle','','#1a49b8')")
rep('not_(bm,YT2+px(890),"PZP-400 64×80 · üst plaka Ø29 · üstte tepsi rafı (kesik)")', 'not_(bm,YT2+px(890),"PZP-400 64×80 · üst plaka Ø29 · üstte 2 tepsi yan yana (kesik)")')

# ================= KONTROL =================
s = t.index("K=["); e = t.index("]", t.index('("⑪')) + 1
K = '''K=[
 ("① ✓ STORE −18: 5. raf çizildi — 4 donmuş kaset (kavurma ×2 · kuşbaşı ×2)","→ 1L çekmecesi sağ kolona; −18 bölmesi 54 → 82 cm; içecek çekmeceleri aşağı","#1d7a4f"),
 ("② OVEN kavite 40×40: tepsi Ø34 + kulp 12 = 46 → kapak kapanmaz","→ kavite derinliği 50 (dış 65 → 75) YA DA kulp 6 cm — KARAR","#b3452b"),
 ("③ TOPPING dozaj hareketi: kenar tutuşlu tepsi 360° dönemez","→ karar: ön saçak (öneri) / C-tutucu — analiz v1","#b3452b"),
 ("④ ✓ PACK: bıçak yatay, önden ince — bölge 73 → 41 cm; bıçak Ø28","→ kazanılan yer şarjöre (96 kutu)","#1d7a4f"),
 ("⑤ PRESS üst plaka Ø40 → Ø29 (tepsi içinde basma)","→ Fersah'a kalıp/plaka sorusu","#b3452b"),
 ("⑥ ✓ Tepsi 3 adet yeter (fırında 2 + kolda 1): press plakası ısıtmalı, soğuma beklemez","→ PRESS'te yatay raf 2 yuva yan yana (8 cm); üstünde çöp + 3 uç yuvası (v6)","#1d7a4f"),
 ("⑦ Kol sınıfı ≥12 kg (kaşar kaseti 15 kg) — UR16e / CRX-20iA/L","→ ray aynı","#9a6b1f"),
 ("⑧ ✓ TOPPING soğutma 25 → 15 cm: hacim ~0,3 m³ → minibar sınıfı 1/12 HP","→ 2 kapılı dolabın 29 cm'lik grubuyla ölçeklenmişti; hacme göre küçüldü","#1d7a4f"),
 ("⑨ ✓ Dozaj boşluğu 26 → 14 cm: tepsi 3 + pide 1,5 + düşme 3 + bilek payı","→ kazanılan yer geçiş rafına 3. kat (çözülme ×2 + büyüme)","#1d7a4f"),
 ("⑩ ✓ OVEN sadeyağ tankı nozülün ÜSTÜNDE: cazibe akış, pompa yok, ısıtıcı + vana","→ sprey nişi 19 → 14 cm; teneke stoğu çekmecede","#1d7a4f"),
 ("⑪ Yükseklik 197 ✓ · genişlik 415 ✓ · TOPPING içi 27+25+21+14+83 = 170 + 15 pay ✓","→ STORE sol kolon 29+7+82+5+54 = 177 + 8 pay ✓","#1d7a4f"),
]'''
t = t[:s] + K + t[e:]
rep('tx(X0,Y0-94,"AUTOKITCH — HAT v40 · TÜM İSTASYONLAR SON VERSİYON (4 Eyl 2026) — STORE v38 · PRESS v5 (yatay tepsi rafı) · TOPPING v8 · OVEN tepsiyle · PACK kesim yandan · robot TEPSİ ucu v1",15,"start","bold")',
    'tx(X0,Y0-94,"AUTOKITCH — HAT v41 · TÜM İSTASYONLAR SON VERSİYON (4 Eyl 2026) — STORE v39 (5. raf) · PRESS v6 (3 tepsi) · TOPPING v9 (soğutma 15 · boşluk 14) · OVEN yağ üstte · PACK kesim yandan",15,"start","bold")')
rep('tx(X0,Y0-54,"Ölçüler cm. Açık kararlar: ③ dozaj hareketi (saçak / C-tutucu) · ① STORE 5. raf (1L çekmecesi sağa) · ② fırın kavitesi 50 / kulp 6 — ⑥ tepsi rafı ÇÖZÜLDÜ (PRESS v5)",10.5,"start","","#b3452b")',
    'tx(X0,Y0-54,"Ölçüler cm. Açık kararlar: ② fırın kavitesi 50 / kulp 6 · ③ dozaj hareketi (saçak / C-tutucu) · ⑤ Fersah Ø29 — bu turda çözülen: ① ④ ⑥ ⑧ ⑨ ⑩ (yeşil)",10.5,"start","","#b3452b")')
rep('hat_on_gorunus_teknik_v40.svg', 'hat_on_gorunus_teknik_v41.svg')
io.open('teknik_cizim41.py', 'w', encoding='utf-8', newline='\n').write(t)
print('v41 uretici ok')
