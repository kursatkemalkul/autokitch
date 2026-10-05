# -*- coding: utf-8 -*-
# v43 -> v44: STORE v4 (alt buzluk 6 cekmece, kalinliklar, kapaksiz 19 cekmece) + PRESS v8 (sol kova + kol boslugu, sag bos) · TEK render
import io
NL = chr(10)
t = io.open('teknik_cizim43.py', encoding='utf-8').read()
def rep(o, n, c=1):
    global t
    assert t.count(o) == c, 'A(%d): %s' % (t.count(o), o[:80])
    t = t.replace(o, n)
def block(start_marker, end_marker, lines):
    global t
    s = t.index(start_marker); e = t.index(end_marker)
    t = t[:s] + NL.join(lines) + NL + NL + t[e:]

# ================= STORE v4 =================
block("# ================= 1 STORE v39", "# ================= 2 PRESS", [
"# ================= 1 STORE v4 (alt buzluk 6 cekmece · 19 cekmece x 61 · PU 60/80 · kapak yok) =================",
"a0,a1=xs[0],xs[1]; am=a0+px(700)",
"PU='#e9e4d6'",
"rc(a0+6,Y0+px(20),a1-a0-12,px(280),1.2,2)",
"for gx,lab in ((350,'−18 grubu 1/3 HP'),(1050,'+3 grubu 1/4 HP')):",
"    ci(a0+px(gx-60),Y0+px(160),px(55),1.1); rc(a0+px(gx+20),Y0+px(90),px(120),px(150),.9,2); tx(a0+px(gx),Y0+px(278),lab,7,'middle','bold')",
"not_((a0+a1)/2,Y0+px(58),'SOĞUTMA ×2 — bölme 28, üstten servis',fs=8)",
"rc(a0+6,Y0+px(300),a1-a0-12,px(60),1,0,'#111',None,PU)",
"rc(a0+6,Y0+px(300),px(60),px(900),1,0,'#111',None,PU); rc(a1-6-px(60),Y0+px(300),px(60),px(900),1,0,'#111',None,PU)",
"rc(a0+px(690),Y0+px(360),px(20),px(840),1,0,'#111',None,'#ccc')",
"rc(a0+6,Y0+px(1200),a1-a0-12,px(80),1,0,'#111',None,PU)",
"rc(a0+6,Y0+px(1280),px(80),px(570),1,0,'#111',None,PU); rc(a1-6-px(80),Y0+px(1280),px(80),px(570),1,0,'#111',None,PU)",
"rc(a0+6,Y0+px(1770),a1-a0-12,px(80),1,0,'#111',None,PU)",
"rc(a0+px(690),Y0+px(1280),px(20),px(490),1,0,'#111',None,'#ccc')",
"def fr(x,y,w,h,c='#111',fill=PU):",
"    rc(x,y,w,h,1,1,c,None,fill); ln(x+w/2-10,y+h-4,x+w/2+10,y+h-4,1.5,c)",
"xl,xr=a0+px(66),a0+px(714); wc=px(624)",
"for k in range(4):",
"    y=Y0+px(362)+k*px(130); fr(xl,y,wc,px(124))",
"    for i in range(7): rc(xl+px(22)+i*px(82),y+px(5),px(66),px(115),.6,2,'#777','3,3')",
"    tx(xl+wc/2,y+px(68),'İÇECEK %d · 7 kanal' % (k+1),6,'middle','bold')",
"y1=Y0+px(362)+4*px(130); fr(xl,y1,wc,px(316))",
"for i in range(5): rc(xl+px(50)+i*px(110),y1+px(50),px(85),px(250),.6,4,'#777','3,3')",
"tx(xl+wc/2,y1+px(170),'1 L · 5 kanal × 8',6,'middle','bold')",
"for r in range(8):",
"    y=Y0+px(362)+r*px(105); fr(xr,y,wc,px(99))",
"    for i in range(4): el(xr+px(95)+i*px(140),y+px(50),px(45),px(28),.6,'#777','3,3')",
"    ln(xr+px(30),y+px(60),xr+wc-px(30),y+px(60),.6,'#777','3,3')",
"    tx(xr+wc/2,y+px(92),'TAZE %d · 20 top' % (r+1),5.5,'middle','bold')",
"tx(a0+px(700),Y0+px(1252),'YATAY İZOLELİ AYIRICI PU 80',6.5,'middle','bold')",
"xl2,xr2=a0+px(86),a0+px(714); wc2=px(604)",
"for k in range(2):",
"    y=Y0+px(1283)+k*px(100)",
"    for xx_,nm in ((xl2,k+1),(xr2,k+3)):",
"        fr(xx_,y,wc2,px(94),'#1a49b8','#dfe7fb')",
"        for i in range(4): el(xx_+px(92)+i*px(140),y+px(48),px(45),px(26),.6,'#1a49b8','3,3')",
"        tx(xx_+wc2/2,y+px(88),'DONMUŞ %d · 20 top' % nm,5.5,'middle','bold','#1a49b8')",
"yk=Y0+px(1483)",
"for xx_,nm in ((xl2,'KAVURMA'),(xr2,'KUŞBAŞI')):",
"    fr(xx_,yk,wc2,px(284),'#1a49b8','#dfe7fb')",
"    for i in range(2): rc(xx_+px(40)+i*px(185),yk+px(15),px(170),px(250),.8,2,'#1a49b8','3,3')",
"    rc(xx_+px(410),yk+px(15),px(170),px(250),.6,2,'#999','3,3')",
"    tx(xx_+wc2/2,yk+px(275),'KASET %s ×2 · −18' % nm,6,'middle','bold','#1a49b8')",
"tx((a0+a1)/2,Y0+px(347),'① ✓ STORE v4: 19 çekmece × 61 (kapak yok) · alt −18 6 çekmece · PU 60/80 · içecek 13 / taze 10,5 / donmuş 10',6.5,'middle','bold','#1d7a4f')",
"a2,a3=am,xs[1]",
])

# ================= PRESS v8 =================
block("# ust bolge v7", "# ================= 3 TOPPING", [
"# ust bolge v8: sol yari kova + 14 kol boslugu · sag yari bos · altta yatay bantlar (uclar 14, tepsi 8)",
"xB=b0+px(350); ln(xB,Y0+px(40),xB,Y0+px(640),1.1,'#111','6,5')",
"rc(b0+px(55),Y0+px(190),px(240),px(440),1.6,3); ln(b0+px(55),Y0+px(240),b0+px(295),Y0+px(240),.8)",
"tx(b0+px(175),Y0+px(420),'KOVA 30 L',8,'middle','bold'); not_(b0+px(175),Y0+px(470),'kapaksız · poşetli · öne çekilir',fs=6); not_(b0+px(175),Y0+px(510),'eleman HER GÜN boşaltır',fs=6)",
"rc(b0+px(30),Y0+px(45),px(290),px(140),1,2,'#1a49b8','4,3'); tx(b0+px(175),Y0+px(105),'KOL BOŞLUĞU 14',7,'middle','bold','#1a49b8'); tx(b0+px(175),Y0+px(140),'huni YOK · pençe bırakır',6,'middle','','#1a49b8')",
"rc(b0+px(380),Y0+px(45),px(290),px(585),1,3,'#999','4,3'); tx(b0+px(525),Y0+px(330),'BOŞ (şimdilik)',8,'middle','bold','#999'); tx(b0+px(525),Y0+px(360),'35×59×84',6.5,'middle','','#999')",
"ln(b0+px(15),Y0+px(650),b1-px(15),Y0+px(650),1,'#111','6,4')",
"tx(bm,Y0+px(672),'UÇ YUVALARI — yatay · 14',7,'middle','bold')",
"for k,(ad,dash) in enumerate((('PENÇE',None),('YEDEK',None),('boş',' 4,3'))):",
"    x_=b0+px(30+k*225); rc(x_,Y0+px(685),px(205),px(105),1.1,2,'#999' if dash else '#111',dash); tx(x_+px(102),Y0+px(745),ad,6,'middle','bold','#999' if dash else '#111')",
"ln(b0+px(15),Y0+px(800),b1-px(15),Y0+px(800),1,'#111','6,4')",
"tx(bm,Y0+px(820),'TEPSİ RAFI — 2 yan yana (+1 kolda) · 8',7,'middle','bold','#1a49b8')",
"for i in range(2):",
"    cx_=b0+px(180+i*340); el(cx_,Y0+px(855),px(160),px(9),1.2,'#1a49b8'); rc(cx_-px(12),Y0+px(850),px(24),px(10),.8,1,'#1a49b8',None,'#dfe7fb')",
"not_(bm,Y0+px(880)+8,'v8: sol kova + 14 boşluk · sağ boş · altta uçlar + tepsiler',fs=6.5)",
])

# ================= UST GORUNUM STORE v4 =================
block("# STORE ust", "# PRESS ust", [
"# STORE ust v4: sol kolon icecek 7 kanal (11 kutu derinlemesine), sag kolon taze tepsi 4x5; −18 altta; on: 19 cekmece onu",
"ln(am,YT2,am,YT2+px(840),1.4)",
"for i in range(7): rc(a0+px(62)+i*px(82),YT2+px(60),px(66),px(700),1,2)",
"for j in range(11): ln(a0+px(62),YT2+px(80)+j*px(62),a0+px(62)+7*px(82),YT2+px(80)+j*px(62),.5,'#999')",
"tx(a0+px(350),YT2+px(45),'içecek: 7 kanal × 11 kutu (derinlemesine) · 1 L altında',7,'middle','','#555')",
"rc(am+px(85),YT2+px(85),px(530),px(650),1.4)",
"for j in range(5):",
"    for i in range(4):",
"        ci(am+px(162)+i*px(125),YT2+px(160)+j*px(125),px(50),1); ci(am+px(162)+i*px(125),YT2+px(160)+j*px(125),px(60),.7)",
"tx(am+px(350),YT2+px(45),'taze tepsi 53×65, 4×5 çukur · −18 bandı altta',7,'middle','','#555')",
"rc(a0+px(20),YT2+px(770),a1-a0-px(40),px(60),1.4,0,'#111',None,PU)",
"not_((a0+a1)/2,YT2+px(890),'19 çekmece önü (izoleli) — kapak yok · çekmece 70 tam açılır, robot arabası yanda park eder')",
])

# ================= KONTROL + baslik =================
rep('("① ✓ STORE −18: 5. raf — 4 donmuş kaset (kav ×2 · kuş ×2); 1L sağa","→ kapak: çekmece modeli — kapak yok, her çekmece izoleli ön yüzlü (cevap)","#1d7a4f")',
    '("① ✓ STORE v4: alt −18 6 çekmece (4 hamur + 2 kaset) · 19 çekmece × 61 · kapak yok","→ PU 60/80 · ray 12,7 · ölçü kontrolü: tatlı 4 kanal, soğutma 28, top ≤ 6 cm · dikey 185 ✓","#1d7a4f")')
rep('("⑥ ✓ PRESS v7 hepsi YATAY: tepsi 2 · uç yuvaları 3 · çöp çekmecesi 40 L · huni","→ 3 tepsi = fırında 2 + kolda 1; 70×84 aynı","#1d7a4f")',
    '("⑥ ✓ PRESS v8: sol yarı 30 L kova + 14 cm kol boşluğu (huni/çekmece yok) · sağ yarı boş","→ altta yatay uç yuvaları 14 + tepsi rafı 8 (2 yan yana + 1 kolda)","#1d7a4f")')
rep('tx(X0,Y0-94,"AUTOKITCH — HAT v43 · TÜM İSTASYONLAR SON VERSİYON (4 Eyl 2026) — STORE v39 · PRESS v7 (yatay) · TOPPING v11 (70×84, tepsi dönmez, ağızlar orta hatta) · OVEN tank+pompa · PACK 116",15,"start","bold")',
    'tx(X0,Y0-94,"AUTOKITCH — HAT v44 · TÜM İSTASYONLAR SON VERSİYON (4 Eyl 2026) — STORE v4 (alt buzluk, çekmeceli) · PRESS v8 (kova + boşluk) · TOPPING v11 · OVEN tank+pompa · PACK 116",15,"start","bold")')
rep('hat_on_gorunus_teknik_v43.svg', 'hat_on_gorunus_teknik_v44.svg')
io.open('teknik_cizim44.py', 'w', encoding='utf-8', newline='\n').write(t)
print('v44 uretici ok')
