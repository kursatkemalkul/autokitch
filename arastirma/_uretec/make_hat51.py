# -*- coding: utf-8 -*-
# HAT v51 = v50 + PACK v4 (ustten beslemeli kutu acici: yigin 84 cm ustte, vakum plunger, kalip, plaka z 60, kapak kolu; plint)
import io
SRC=r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\_uretec\teknik_cizim50.py"
DST=r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\_uretec\teknik_cizim51.py"
s=io.open(SRC,encoding='utf-8').read()
def rep(a,b,cnt=1):
    global s
    assert s.count(a)==cnt, ('%d != %d: '%(s.count(a),cnt))+a[:80]
    s=s.replace(a,b)
rep('hat_on_gorunus_teknik_v50.svg','hat_on_gorunus_teknik_v51.svg')
rep('(6 Eyl 2026, HAT v50)','(6 Eyl 2026, HAT v51)')
rep('HAT v50 · TÜM İSTASYONLAR SON VERSİYON (6 Eyl 2026) — STORE v4 (+ v5 öneri) · PRESS v8 · TOPPING v25 yerleşim + v27 KAP · OVEN v5 (Omake 2 kat · 1 STANDART YAĞ KABI + sprey ortada · KESME PRESİ · kolon 70)','HAT v51 · TÜM İSTASYONLAR (6 Eyl 2026) — STORE v4 · PRESS v8 · TOPPING v25 + v27 KAP · OVEN v5 (Omake 2 kat · 1 yağ kabı · sprey · KESME presi · kolon 70)')
rep('· PACK = şarjör 116 + kutulama",15','· PACK v4 = KUTU AÇICI (yığın 84 = 525 · vakum · kalıp)",15')
rep('"""HAT v50 (','"""HAT v51 (v50 + PACK v4: ustten beslemeli kutu acici, sarjor 84 cm 525 blank, tek dikey eksen + kalip, plint) — v50 (')
rep("    if i not in (2,3): rc(_x+14,YT,12,px(HA),1.4); rc(_x+px(_w)-26,YT,12,px(HA),1.4)   # TOPPING + OVEN: ayak yerine plint",
    "    if i not in (2,3,4): rc(_x+14,YT,12,px(HA),1.4); rc(_x+px(_w)-26,YT,12,px(HA),1.4)   # TOPPING + OVEN + PACK: ayak yerine plint")
rep("TOPPING ve OVEN'de ayak yerine plint 12 = ızgara)","TOPPING, OVEN ve PACK'te ayak yerine plint 12)")
rep("· OVEN v4: kesme kuvveti pilotu · sadeyağ mı sıvı yağ mı · kuru bağlantı tipi\"","· OVEN: kesme pilotu · yağ tipi · kuru bağlantı · PACK v4: vantuz payı (pilot 40 cm) · blank kalıbı · flap kapanması\"")

# ---- PACK on gorunus ----
i0=s.index('# ================= 5 PACK v49'); i1=s.index('# ================= UST GORUNUM')
PACK=r'''# ================= 5 PACK v4 (üstten beslemeli kutu açıcı: yığın üstte · vakum plunger · kalıp plakası z 60 · kapak kolu · plint) =================
e0,e1=xs[4],xs[5]; em=(e0+e1)/2; WE=e1-e0-px(40)
Ze=lambda z: YZ-px(z*10)
PZ=[(0,12,'#e9e4d6','plint 12'),(12,30,'#e3f2fb','PANO 18 · PLC · step + 2 motor sürücü · 3 servo · 24 V'),(30,45,'#eef3f8','STEP NEMA 23 + bilyalı vida · VAKUM POMPASI 24 V 30 L/dk'),(45,55,'#f4f0fa','BOYUNDURUK 36×72 (tek dikey eksen, strok 48)'),(55,60,'#f4f0fa',''),(60,104,'#fbf3e6',''),(104,188,'#fff8e0',''),(188,197,'#e9e4d6','üst pay 9')]
for z0_,z1_,col,lab in PZ:
    rc(e0+px(30),Ze(z1_),e1-e0-px(60),px((z1_-z0_)*10),.8,0,'#555',None,col)
    if lab: notew(em,Ze((z0_+z1_)/2)+2,lab,WE-px(20),5.2,'#333','middle','bold' if z0_ in (12,45) else '')
# sarjor: yatay yigin 84 cm
rc(e0+px(150),Ze(188),px(400),px(840),.8,0,'#5a3d13',None,'#e8d8b0')
for i in range(1,21): ln(e0+px(150),Ze(104+i*4),e0+px(550),Ze(104+i*4),.35,'#a8905e')
for xx_ in (e0+px(140),e0+px(552)): rc(xx_,Ze(190),px(8),px(860),1,0,'#333',None,'#333')
notew(em,Ze(150),'ŞARJÖR 84: 525 açık kutu (blank 40×76, E-dalga 1,6 mm) yatay yığın · 80 pide: 3 gün 38 cm · 5 gün 64 · dolu 6,6 gün · eleman haftada 1 demet sürer (ön kapı)',px(380),5.2,'#5a3d13','middle','bold')
rc(e0+px(140),Ze(104.6),px(420),px(6),.8,0,'#333',None,'#333'); tx(em,Ze(106.5)+2,'alt tutucu raylar (yığın ağırlığı burada) — en alttaki vakumla aşağı çekilir',4.4,'middle','','#333')
# kalip plakasi z 60 + pencere + kutu
rc(e0+px(30),Ze(60.6),e1-e0-px(60),px(6),.8,0,'#333',None,'#999')
rc(e0+px(187),Ze(60),px(6),px(45),.8,0,'#333',None,'#666'); rc(e0+px(507),Ze(60),px(6),px(45),.8,0,'#333',None,'#666')
tx(em,Ze(57.5)+2,'kalıp: pencere 32,5 · duvar 4,5 · köşe plowları',4.4,'middle','','#333')
rc(e0+px(189),Ze(64.6),px(323),px(40),1.2,0,'#5a3d13',None,'#e8d8b0'); tx(em,Ze(68)+2,'KUTU plakada (yükseldi) · kapak açık arkada · z 60',5,'middle','bold','#5a3d13')
# plunger + vantuz + posts
rc(e0+px(192),Ze(58),px(316),px(20),1.1,1,'#6b4fa8',None,'#ece6f6'); tx(em,Ze(53)+2,'plunger 31,6 + 6 vantuz Ø40',4.4,'middle','','#6b4fa8')
for xx_ in (220,480): rc(e0+px(xx_-15),Ze(59),px(30),px(10),.7,0,'#6b4fa8',None,'#fff')
ln(em,Ze(45),em,Ze(55),1.4,'#333')
# kapak yayi + kol
rc(e0+px(189),Ze(100.6),px(323),px(360),.8,0,'#5a3d13','4 3','none')
tx(em,Ze(102)+2,'kapak dikey geçerken (kesik) tepe z 100 < 104 ✓ · U çevirme kolu 24 V + 3 flap parmağı (servo)',4.4,'middle','','#5a3d13')
ln(e0+px(120),Ze(72),e0+px(120),Ze(97),1.1,'#6b4fa8'); E.append('<path d="M %.1f %.1f l -3 6 h 6 z" fill="#6b4fa8"/>' % (e0+px(120),Ze(97))); tx(e0+px(112),Ze(84)+2,'plunger ↑48',4,'end','','#6b4fa8')
ln(e0+px(580),Ze(97),e0+px(580),Ze(72),1.1,'#5a3d13'); E.append('<path d="M %.1f %.1f l -3 -6 h 6 z" fill="#5a3d13"/>' % (e0+px(580),Ze(72))); tx(e0+px(588),Ze(84)+2,'blank ↓',4,'start','','#5a3d13')
tray(em,Ze(75),kulp=True); tx(em,Ze(79)+2,'tepsi eğilir, 4 parça kayar · pençe alır',4.4,'middle','','#1a49b8')
# klape + on kapi
rc(e0+px(18),Ze(104),px(10),px(440),1,0,'#1a49b8',None,'#dfe7fb'); txr(e0+px(12),Ze(82),'KLAPE 66×44 (robot)',4,'#1a49b8','bold')
rc(e0+px(18),Ze(197),px(10),px(930),1,0,'#b7791f',None,'#fde9c9'); txr(e0+px(12),Ze(150),'ÖN KAPI (eleman)',4,'#b7791f','bold')
tx(em,Ze(6)+2,'plint 12',4.6,'middle','','#333')

'''
s=s[:i0]+PACK+s[i1:]
# ---- PACK ust ----
i0=s.index('# PACK ust v49'); i1=s.index('# ROBOT KORIDORU')
PU=r'''# PACK ust v4: kalip plakasi — pencere 32,5 onde (y 5,5–38), kapak bolgesi arkada (orta ray + flap parmaklari), yigin kilavuzlari 40, U kol
rc(e0+px(150),YT2+px(65),px(400),px(760),.6,0,'#5a3d13','3,2','#f3ead6')
rc(em-px(162),YT2+px(460),px(325),px(325),1.3,0,'#111',None,'#fff'); tx(em,YT2+px(630),'PENCERE 32,5',5.2,'middle','bold'); tx(em,YT2+px(660),'kutu burada oluşur',4.2,'middle','','#777')
ci(em,YT2+px(640),px(160),1,'#1a49b8','4,3')
for (xx_,yy_) in ((-130,510),(130,510),(-130,760),(130,760)): ci(em+px(xx_),YT2+px(yy_),px(20),.8,'#6b4fa8','3,2')
rc(em-px(50),YT2+px(50),px(100),px(410),.6,0,'#777',None,'#e6e6e6')
for yy_ in (160,340): rc(em-px(15),YT2+px(yy_),px(30),px(44),.6,0,'#6b4fa8',None,'#ece6f6')
rd(e0+px(150),YT2+px(100),px(40),px(320),.8,'#b7791f'); rd(e0+px(510),YT2+px(100),px(40),px(320),.8,'#b7791f'); rd(e0+px(190),YT2+px(60),px(320),px(40),.8,'#b7791f')
for xx_ in (e0+px(140),e0+px(552)): rc(xx_,YT2+px(60),px(8),px(770),1,0,'#333',None,'#333')
ln(e0+px(130),YT2+px(460),e0+px(130),YT2+px(160),1.4,'#1d7a4f'); ln(e0+px(570),YT2+px(460),e0+px(570),YT2+px(160),1.4,'#1d7a4f'); ln(e0+px(130),YT2+px(160),e0+px(570),YT2+px(160),1.4,'#1d7a4f')
tx(em,YT2+px(30),'ön dil parmağı · yan flap parmakları (turuncu) · U kol (yeşil)',4.4,'middle','','#777')
notew(em,YN,"kalıp plakası z 60: pencere 32,5 önde (tepsi Ø32 kesik), kapak bölgesi arkada (orta ray + 3 flap parmağı), yığın kılavuzları 40, blank izi 40×76 (kesik) · üstte şarjör 84",e1-e0-20,7)
'''
s=s[:i0]+PU+s[i1:]
# ---- KONTROL ----
rep(''' ("④ ✓ PACK = şarjör 2×2×29 = 116 kutu (eleman katlar) + kutulama (tepsi eğilir, 4 parça kayar) — KESİM OVEN'e taşındı (v4 KESME presi z 32–82)","→ pres: bıçak yıldızı + (2 × 28, paslanmaz 1,2 mm) · 24 V lineer aktüatör 1500 N, strok 100 mm, kendini kilitler · kuvvet 56 cm × 15–20 N/cm = 0,85–1,1 kN · tepsi zemin plakasına dayanır, robot yalnız kulpu tutar · PACK'te 26 cm boşaldı","#1d7a4f"),''',
    ''' ("④ ✓ PACK v4 = ÜSTTEN BESLEMELİ KUTU AÇICI: açık kutu (blank 40×76, 32×32×4 köşe tırnaklı) yığını üstte 84 cm = 525 (3 gün 38 cm garanti · 5 gün 64 hedef · dolu 6,6 gün; 7 gün 90 sığmaz) · tek dikey eksen (bilyalı vida + NEMA 23, strok 48): plunger + 6 vantuz Ø40 en alt blankı çeker, kalıp penceresinden tabanı 4 cm çekince duvarlar + tırnaklar katlanır (1 vuruş) · kutu plakaya (z 60) yükselir · tepsi eğilir 4 parça kayar · 3 flap parmağı + U kol kapağı kapatır · eksen 6 kaldırır, pençe alır → PICKUP","→ zonlar: plint 12 / pano 18 / step+vakum 15 / boyunduruk 10 / kalıp 5 / yükleme 44 (kapak yayı 40) / şarjör 84 / üst 9 = 197 ✓ · derinlik blank 76 + 2×4 = 84 ✓ · kompresör yok (24 V diyafram vakum pompası) · çevrim 15 sn · eleman haftada 1 demet sürer · AÇIK: dolu yığın 60 kg vantuz payı 1,2× (pilot 40 cm), blank bıçak kalıbı, flap kapanması (pençe yedek) · KESİM OVEN'de (v4 pres)","#1d7a4f"),''')
io.open(DST,'w',encoding='utf-8').write(s); print('teknik_cizim51.py yazildi')
