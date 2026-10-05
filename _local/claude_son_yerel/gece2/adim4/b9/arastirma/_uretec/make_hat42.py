# -*- coding: utf-8 -*-
# v41 -> v42 (Kemal, 4 Eyl): TOPPING v10 70x84 (cikislar ortada kume, on sira calisan + arka sira siradaki, gecis rafi 3 kat)
# PRESS v7 yatay katmanlar (tepsi 2 + uc yuvalari + cop cekmecesi + huni) · OVEN tank ustte + mini pompa, teneke stogu
# PACK acik deste kalkti (116 kutu) · ust gorunum TOPPING 70x84 + hareket bolgesi · KONTROL guncel
import io
NL = chr(10)
t = io.open('teknik_cizim41.py', encoding='utf-8').read()
def rep(o, n, c=1):
    global t
    assert t.count(o) == c, 'A(%d): %s' % (t.count(o), o[:80])
    t = t.replace(o, n)
def block(start_marker, end_marker, lines):
    global t
    s = t.index(start_marker); e = t.index(end_marker)
    t = t[:s] + NL.join(lines) + NL + NL + t[e:]

# ================= PRESS v7 — yatay katmanlar =================
block("# ust bolge v6:", "# ================= 3 TOPPING", [
"# ust bolge v7 — YATAY KATMANLAR (alttan uste): tepsi rafi 8 · uc yuvalari 14 · cop cekmecesi 22 · huni",
"for yy_ in (790, 630, 390): ln(b0+px(15),Y0+px(yy_),b1-px(15),Y0+px(yy_),1,'#111','6,4')",
"# katman 1: tepsi rafi (2 yan yana)",
"tx(bm,Y0+px(816),'TEPSİ RAFI — 2 yan yana (+1 kolda = 3)',7,'middle','bold','#1a49b8')",
"for i in range(2):",
"    cx_=b0+px(180+i*340)",
"    rc(cx_-px(172),Y0+px(848),px(14),px(14),1,1); rc(cx_+px(158),Y0+px(848),px(14),px(14),1,1)",
"    el(cx_,Y0+px(855),px(165),px(9),1.3,'#1a49b8'); rc(cx_-px(12),Y0+px(850),px(24),px(10),.8,1,'#1a49b8',None,'#dfe7fb')",
"# katman 2: uc yuvalari YATAY (pence · yedek pence · bos)",
"tx(bm,Y0+px(655),'UÇ YUVALARI — yatay, yan yana',7,'middle','bold')",
"for k,(ad,dash) in enumerate((('PENÇE',None),('YEDEK PENÇE',None),('boş',' 4,3'))):",
"    x_=b0+px(30+k*225)",
"    rc(x_,Y0+px(670),px(205),px(110),1.2,3,'#999' if dash else '#111',dash)",
"    if not dash: rc(x_+px(60),Y0+px(690),px(85),px(30),1,2); ln(x_+px(75),Y0+px(720),x_+px(85),Y0+px(765),1.1); ln(x_+px(130),Y0+px(720),x_+px(120),Y0+px(765),1.1)",
"    tx(x_+px(102),Y0+px(772)+(0 if dash else 0),ad,6.5,'middle','bold','#999' if dash else '#111')",
"# katman 3: cop cekmecesi YATAY (boyu boyunca) 30-40 L",
"rc(b0+px(30),Y0+px(405),b1-b0-px(60),px(210),1.6,4)",
"ln(bm-25,Y0+px(600),bm+25,Y0+px(600),2.2)",
"tx(bm,Y0+px(485),'ÇÖP ÇEKMECESİ — yatay, 70×60×20 ≈ 40 L',8,'middle','bold')",
"not_(bm,Y0+px(540),'poşetli · öne çekilir, motorsuz · eleman HER GÜN',fs=6.8)",
"# katman 4: huni / birak-gec agzi",
"ln(b0+px(60),Y0+px(80),b0+px(200),Y0+px(380),1.6); ln(b1-px(60),Y0+px(80),b1-px(200),Y0+px(380),1.6); ln(b0+px(60),Y0+px(80),b1-px(60),Y0+px(80),1.6)",
"tx(bm,Y0+px(150),'HUNİ — robot bırakır, geçer',8,'middle','bold')",
"not_(bm,Y0+px(230),'ağız 58 · çekmeceye düşer',fs=7)",
"not_(bm,Y0+px(880)+8,'v7: hepsi YATAY — tepsi 8 · uçlar 14 · çöp 22 · huni 32 (kabin 70×84 aynı)',fs=6.5)",
])

# ================= TOPPING v10 — 70 x 84 =================
block("# ================= 3 TOPPING", "# ================= 4 OVEN", [
"# ================= 3 TOPPING v10 (70x84 — herkesle ayni · cikislar ORTA KUME · on sira calisan + arka sira siradaki · bosluk 14 · gecis rafi 3 kat) =================",
"c0,c1=xs[2],xs[3]; cm2=(c0+c1)/2",
"tx(cm2,Y0+px(35),'SOĞUTMA (ÜSTTE) 15 — minibar sınıfı 1/12 HP · +3 °C · buzluk YOK',7.5,'middle','bold')",
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
"# arka sira (siradaki) — acik gri kesik; on sira — kasar A solda, sag: sucuk onde / kavurma+kusbasi arkasinda",
"kaset(c0+px(20),Y0+px(KY-16),px(320),px(250),'KAŞAR B (arka sıra)',dash='3,3',c='#aaa')",
"kaset(c0+px(360),Y0+px(KY-16),px(160),px(250),'sıradaki KAV',dash='3,3',c='#aaa')",
"kaset(c0+px(525),Y0+px(KY-16),px(160),px(250),'sıradaki KUŞ',dash='3,3',c='#aaa')",
"kaset(c0+px(355),Y0+px(KY-6),px(165),px(250),'KAVURMA',dash='4,3',c='#777')",
"kaset(c0+px(525),Y0+px(KY-6),px(165),px(250),'KUŞBAŞI',dash='4,3',c='#777')",
"kaset(c0+px(10),Y0+px(KY),px(335),px(250),'KAŞAR A','35×42×25 · 15 kg')",
"kaset(c0+px(355),Y0+px(KY),px(335),px(250),'SUCUK (ön)','35×21×25 · 10 kg')",
"CY=KY+320",
"# koniler ORTAYA toplanir: A kasar x26 · C kavurma x33 · D kusbasi x47 · B sucuk x44",
"ln(c0+px(15),Y0+px(KY+252),c0+px(215),Y0+px(CY-55),1.2); ln(c0+px(340),Y0+px(KY+252),c0+px(305),Y0+px(CY-55),1.2)",
"ln(c0+px(360),Y0+px(KY+252),c0+px(400),Y0+px(CY-40),1.2); ln(c0+px(685),Y0+px(KY+252),c0+px(480),Y0+px(CY-40),1.2)",
"for cx0,r in ((260,55),(440,40)):",
"    ci(c0+px(cx0),Y0+px(CY),px(r),1.6)",
"    for k in range(6):",
"        a=k*math.pi/3; ln(c0+px(cx0),Y0+px(CY),c0+px(cx0)+px(r)*math.cos(a),Y0+px(CY)+px(r)*math.sin(a),.9)",
"    ln(c0+px(cx0-16),Y0+px(CY+60),c0+px(cx0-16),Y0+px(CY+150),1.3); ln(c0+px(cx0+16),Y0+px(CY+60),c0+px(cx0+16),Y0+px(CY+150),1.3)",
"for cx0 in (330,470):",
"    ci(c0+px(cx0),Y0+px(CY-25),px(35),1,'#999','4,3')",
"    ln(c0+px(cx0-13),Y0+px(CY+10),c0+px(cx0-13),Y0+px(CY+150),.9,'#999','4,3'); ln(c0+px(cx0+13),Y0+px(CY+10),c0+px(cx0+13),Y0+px(CY+150),.9,'#999','4,3')",
"rc(c0+px(150),Y0+px(CY-20),px(45),px(40),1.1,2); tx(c0+px(172),Y0+px(CY+5),'M',7,'middle','bold')",
"rc(c0+px(540),Y0+px(CY-20),px(45),px(40),1.1,2); tx(c0+px(562),Y0+px(CY+5),'M',7,'middle','bold')",
"FL=CY+120",
"ln(c0+px(15),Y0+px(FL),c1-px(15),Y0+px(FL),1.6)",
"tx(cm2,Y0+px(FL-8),'4 ağız ORTA KÜMEDE (x 26-47) · 3 cm sarkar',6,'middle','','#888')",
"tray(c0+px(350),Y0+px(FL+95),kulp=True)",
"rc(c0+px(575),Y0+px(FL+55),px(55),px(28),1.1,2,'#1a49b8'); tx(c0+px(602),Y0+px(FL+73),'kilit',5.5,'middle','','#1a49b8')",
"tx(c0+px(120),Y0+px(FL+50),'AÇIK BOŞLUK 14',6,'middle','bold','#1a49b8')",
"tx(c0+px(120),Y0+px(FL+72),'③ ✓ X-Y + ±90°',6,'middle','bold','#1d7a4f')",
"GY=FL+140",
"ln(c0+px(15),Y0+px(GY),c1-px(15),Y0+px(GY),1,'#111','6,4')",
"tx(cm2,Y0+px(GY+22),'GEÇİŞ RAFI (ayrı soğuk bölme · 70×84) — 3 kat',7.5,'middle','bold','#1a49b8')",
"kaset(c0+px(10),Y0+px(GY+35),px(335),px(250),'KAŞAR C','dolu +3 (arkada D)')",
"kaset(c0+px(355),Y0+px(GY+35),px(335),px(250),'SUCUK yedek','+ boş yuvalar (arka)')",
"kaset(c0+px(10),Y0+px(GY+310),px(335),px(250),'BOŞ kasetler','biten → eleman toplar',dash=None,c='#555')",
"kaset(c0+px(355),Y0+px(GY+310),px(335),px(250),'BOŞ kasetler','',dash=None,c='#555')",
"kaset(c0+px(10),Y0+px(GY+585),px(680),px(250),'büyüme: 5. malzeme kasetleri (kıyma / zeytin) — 70×84',dash='4,3',c='#999')",
"not_(cm2,Y0+px(1832),'14 kaset: 4 çalışan + 4 sıradaki (üst) + 2 kaşar + sucuk + boşlar (geçiş rafı) · donmuşlar STORE −18',fs=6)",
])

# ================= OVEN — tank ustte + MINI POMPA, teneke stogu =================
block("rc(d0+px(25),Y0+px(1180),d1-d0-px(50),px(110),1.6)", "rc(d0+px(40),Y0+px(20),d1-d0-px(80),px(115),1.4,3); ci(dm,Y0+px(77),px(42),1.1)", [
"rc(d0+px(25),Y0+px(1180),d1-d0-px(50),px(120),1.6)",
"rc(d0+px(45),Y0+px(1195),px(230),px(90),1.4,3,'#c9a227',None,'#fff8e0'); tx(d0+px(160),Y0+px(1232),'TANK 4 L',7,'middle','bold','#8a6a3a'); tx(d0+px(160),Y0+px(1258),'45 °C ısıtıcı',6,'middle','','#8a6a3a')",
"rc(d0+px(300),Y0+px(1195),px(130),px(90),1.2,3); tx(d0+px(365),Y0+px(1232),'POMPA',6.5,'middle','bold'); tx(d0+px(365),Y0+px(1258),'12 V · 8 W',6,'middle','','#555')",
"rc(d0+px(450),Y0+px(1195),px(120),px(90),1,2); tx(d0+px(510),Y0+px(1245),'vana',6.5,'middle','','#555')",
"tx(dm,Y0+px(1172),'⑩ SADEYAĞ ÜSTTE + MİNİ POMPA: püskürtme 1-2 bar ister, cazibe damlatır',6.3,'middle','bold','#9a6b1f')",
"rc(dm-px(22),Y0+px(1300),px(44),px(28),1.3); ln(dm,Y0+px(1328),dm,Y0+px(1345),1.4)",
"rc(d0+px(25),Y0+px(1320),d1-d0-px(50),px(145),1.4)",
"ln(dm,Y0+px(1345),dm-px(100),Y0+px(1425),1,'#111','4 4'); ln(dm,Y0+px(1345),dm+px(100),Y0+px(1425),1,'#111','4 4')",
"tray(dm,Y0+px(1437),kulp=True)",
"not_(dm,Y0+px(1458),'sprey nişi 14 — tepsi 2 sn geçer, yağ sıcak pidede erir',fs=6.3)",
"rc(d0+18,Y0+px(1490),d1-d0-36,px(345),1.4,3)",
"for i in range(3): rc(d0+px(60)+i*px(180),Y0+px(1540),px(150),px(250),1.2,2); tx(d0+px(135)+i*px(180),Y0+px(1675),'teneke',6.5)",
"not_(dm,Y0+px(1520),'SADEYAĞ STOĞU — 3 teneke ≈ 4 ay (kapaklı bölme; çekmece yok)',fs=6.5)",
])

# ================= PACK — acik deste kalkti, sarjor 116 =================
rep("for r in range(24):" + NL + "    for kx in (e0+8, e0+8+px(320)+4): rc(kx,Y0+px(520)+r*px(45),px(320),px(45),1.05)",
    "for r in range(29):" + NL + "    for kx in (e0+8, e0+8+px(320)+4): rc(kx,Y0+px(520)+r*px(45),px(320),px(45),1.05)")
rep("rc(e0+8,Y0+px(1620),px(320)*2+4,px(220),1.4)" + NL + "for i in range(4): ln(e0+16,Y0+px(1660)+i*px(40),e0+196,Y0+px(1660)+i*px(40),.8)" + NL, "")
rep("not_(em,Y0+px(505),'katlanmış kutu 2×2×24 = 96 — ELEMAN katlar (ıslak mendil içinde)',fs=7.5)",
    "not_(em,Y0+px(505),'katlanmış kutu 2×2×29 = 116 — ELEMAN katlar (ıslak mendil içinde) · açık deste YOK',fs=7)")
rep("not_(em,Y0+px(1835),'açık deste ≈50',fs=7.5)" + NL, "")

# ================= UST GORUNUM: TOPPING 70x84 =================
rep("for i,(_ad,_w) in enumerate(M):" + NL + "    if i==2: continue" + NL + "    rc(xs[i]+2,YT2,px(_w)-4,px(840),2,5)",
    "for i,(_ad,_w) in enumerate(M):" + NL + "    rc(xs[i]+2,YT2,px(_w)-4,px(840),2,5)")
block("# TOPPING ust: 70 x 55", "# OVEN ust", [
"# TOPPING ust v10: 70 x 84 — arka sira (siradaki) + on sira (calisan) · cikislar orta kume · tepsi hareket bolgesi",
"rc(c0+px(0)+6,YT2+px(6),px(350)-8,px(420)-8,1,2,'#999','4,3'); tx(c0+px(175),YT2+px(200),'KAŞAR B',7,'middle','bold','#888'); tx(c0+px(175),YT2+px(225),'sıradaki',6,'middle','','#888')",
"rc(c0+px(350)+2,YT2+px(6),px(350)-4,px(210)-8,1,2,'#999','4,3'); tx(c0+px(525),YT2+px(115),'SUCUK yedek',7,'middle','bold','#888')",
"rc(c0+px(350)+2,YT2+px(212),px(170)-4,px(210)-8,1,2,'#999','4,3'); tx(c0+px(435),YT2+px(320),'sır. KAV',6.5,'middle','bold','#888')",
"rc(c0+px(520)+2,YT2+px(212),px(170)-4,px(210)-8,1,2,'#999','4,3'); tx(c0+px(605),YT2+px(320),'sır. KUŞ',6.5,'middle','bold','#888')",
"rc(c0+px(0)+6,YT2+px(426),px(350)-8,px(420)-12,1.3,2); tx(c0+px(175),YT2+px(600),'KAŞAR A',8,'middle','bold'); tx(c0+px(175),YT2+px(625),'35×42',6.5)",
"rc(c0+px(350)+2,YT2+px(426),px(170)-4,px(210)-8,1.3,2); tx(c0+px(435),YT2+px(520),'KAVURMA',7,'middle','bold')",
"rc(c0+px(520)+2,YT2+px(426),px(170)-4,px(210)-8,1.3,2); tx(c0+px(605),YT2+px(520),'KUŞBAŞI',7,'middle','bold')",
"rc(c0+px(350)+2,YT2+px(632),px(350)-4,px(210)-12,1.3,2); tx(c0+px(525),YT2+px(740),'SUCUK 35×21',7.5,'middle','bold')",
"ln(c0+2,YT2+px(422),c1-2,YT2+px(422),1.2,'#111','3,3')",
"for x_,y_,ad in ((260,560,'A'),(440,620,'B'),(330,420,'C'),(470,420,'D')):",
"    ci(c0+px(x_),YT2+px(y_),px(20),1.4,'#b3452b',None,'#fde3dc'); tx(c0+px(x_),YT2+px(y_)+3,ad,6,'middle','bold','#b3452b')",
"rc(c0+px(170),YT2+px(170),px(360),px(670),1,0,'#1d7a4f','5,3')",
"ci(c0+px(260),YT2+px(700),px(170),1.2,'#1a49b8','5,4'); rc(c0+px(245),YT2+px(870),px(30),px(120),1,1,'#1a49b8')",
"not_(cm2,YT2+px(890),'v10: ön sıra çalışan · arka sıra sıradaki · ağızlar A kaşar B sucuk C kav D kuş · yeşil: tepsi merkez bölgesi x 17-53, y ≥17',fs=6.5)",
])
rep("not_(cm2,YT2+px(590),\"ön 29 cm geride (koridora yer)\",fs=7.5)" + NL, "", 0) if "ön 29 cm geride" in t else None

# ================= KONTROL =================
s = t.index("K=["); e = t.index("]", t.index('("⑪')) + 1
K = '''K=[
 ("① ✓ STORE −18: 5. raf — 4 donmuş kaset (kavurma ×2 · kuşbaşı ×2); 1L çekmecesi sağa","→ KAPAK sorusu: çekmece modeli — kapak yok, her çekmecenin izoleli ön yüzü var (cevapta beyin fırtınası)","#1d7a4f"),
 ("② OVEN kavite 40×40: tepsi Ø34 + kulp 12 = 46 → kapak kapanmaz","→ kavite derinliği 50 (dış 65 → 75) YA DA kulp 6 cm — KARAR","#b3452b"),
 ("③ ✓ TOPPING hareket ÇÖZÜLDÜ (84 derinlik): ağızlar orta kümede x 26-47, y 42-62","→ tepsi merkezi x 17-53 · y ≥17 · kulp öne, ±90° → her ağız pidenin merkez+kenar hepsine ulaşır","#1d7a4f"),
 ("④ ✓ PACK: bıçak yatay, önden ince; açık deste kalktı → şarjör 2×2×29 = 116 kutu","→ bıçak Ø28 + yuva pimleri","#1d7a4f"),
 ("⑤ PRESS üst plaka Ø40 → Ø29 (tepsi içinde basma)","→ Fersah'a kalıp/plaka sorusu","#b3452b"),
 ("⑥ ✓ PRESS v7 hepsi YATAY: tepsi 2 (8) · uç yuvaları 3 (14) · çöp çekmecesi 40 L (22) · huni (32)","→ 3 tepsi = fırında 2 + kolda 1; 70×84 aynı","#1d7a4f"),
 ("⑦ Kol sınıfı ≥12 kg (kaşar kaseti 15 kg) — UR16e / CRX-20iA/L","→ ray aynı","#9a6b1f"),
 ("⑧ ✓ TOPPING 70×84 (herkesle aynı): kaset katı ÖN sıra çalışan + ARKA sıra sıradaki → tam dolu","→ 'çözülme alanı' YOK: donmuş kaset arka sıradaki küçük yuvaya 1 gün önce gelir, orada çözülür","#1d7a4f"),
 ("⑨ ✓ Dozaj boşluğu 14 · soğutma 15 (minibar sınıfı) · elektrik 12","→ kilit tepeye 8,5 cm, ağız 11 cm → 2,5 cm pay; düşme 6,5 cm","#1d7a4f"),
 ("⑩ OVEN sadeyağ: tank ÜSTTE ama püskürtme basınç ister → 12 V diyafram pompa 8 W + vana","→ cazibe yalnız damlatır; çekmeceler kalktı → altta teneke stoğu ×3 (4 ay)","#9a6b1f"),
 ("⑪ Yükseklik 197 ✓ · genişlik 415 ✓ · derinlik 84 HER KABİN ✓ · TOPPING içi 27+25+21+14+83 = 170 + 15 pay","→ STORE sol kolon 29+7+82+5+54 = 177 + 8 pay ✓","#1d7a4f"),
]'''
t = t[:s] + K + t[e:]
rep('tx(X0,Y0-94,"AUTOKITCH — HAT v41 · TÜM İSTASYONLAR SON VERSİYON (4 Eyl 2026) — STORE v39 (5. raf) · PRESS v6 (3 tepsi) · TOPPING v9 (soğutma 15 · boşluk 14) · OVEN yağ üstte · PACK kesim yandan",15,"start","bold")',
    'tx(X0,Y0-94,"AUTOKITCH — HAT v42 · TÜM İSTASYONLAR SON VERSİYON (4 Eyl 2026) — STORE v39 · PRESS v7 (yatay katmanlar) · TOPPING v10 (70×84, orta küme) · OVEN tank+pompa · PACK 116 kutu",15,"start","bold")')
rep('tx(X0,Y0-54,"Ölçüler cm. Açık kararlar: ② fırın kavitesi 50 / kulp 6 · ③ dozaj hareketi (saçak / C-tutucu) · ⑤ Fersah Ø29 — bu turda çözülen: ① ④ ⑥ ⑧ ⑨ ⑩ (yeşil)",10.5,"start","","#b3452b")',
    'tx(X0,Y0-54,"Ölçüler cm. HER KABİN 70/65/140 × 197 × 84. Açık: ② fırın kavitesi 50 / kulp 6 · ⑤ Fersah Ø29 · STORE kapak modeli (cevap) — bu turda çözülen: ③ ④ ⑥ ⑧ ⑨ (yeşil)",10.5,"start","","#b3452b")')
rep('hat_on_gorunus_teknik_v41.svg', 'hat_on_gorunus_teknik_v42.svg')
io.open('teknik_cizim42.py', 'w', encoding='utf-8', newline='\n').write(t)
print('v42 uretici ok')
