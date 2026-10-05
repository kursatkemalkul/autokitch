# -*- coding: utf-8 -*-
# ist2_pres5 -> ist2_pres6: 3 tepsi (yatay raf 2 yan yana, 8 cm) + ustunde cop + 3 uc yuvasi (pence / yedek pence / bos)
import io
NL = chr(10)
t = io.open('ist2_pres5.py', encoding='utf-8').read()
def rep(o, n, c=1):
    global t
    assert t.count(o) == c, 'A(%d): %s' % (t.count(o), o[:80])
    t = t.replace(o, n)
rep("İSTASYON 2 — PRESS · DETAY v5 (tepsi rafı YATAY: 8 yuva · pençe yuvası · çöp · PZP-400 zeminde · tepsi içinde basma)",
    "İSTASYON 2 — PRESS · DETAY v6 (3 tepsi: yatay raf 2 yan yana · üstünde çöp + 3 uç yuvası · PZP-400 zeminde · tepsi içinde basma)")
rep("Kemal: \"tepsi ucu dikey cebe sığmaz — yatayda kurgula.\" Ø34 + kulp 12 = 46 cm, kabin derinliği 84 → yatay raf sığıyor; sol 36 = pençe yuvası + 8 tepsi (pitch 5) · sağ 34 = huni + 30 L kova · genişlik 70 DEĞİŞMEDİ",
    "Kemal: \"1-2 tepsi yeter, yatay kur, üstüne çöpü koy.\" 3 tepsi = fırında 2 + kolda 1 (press plakası ısıtmalı → soğuma beklemez). Alt bant 8 cm: 2 tepsi yan yana (kulp öne) · üstte sol huni + 30 L kova, sağ 3 uç yuvası · 70 × 84 DEĞİŞMEDİ")
s = t.index("# --- UST BOLGE y 50-880"); e = t.index("# olculer")
blk = [
"# --- UST BOLGE y 50-890: sol HUNI+KOVA (x 20-360) · sag 3 UC YUVASI (x 380-680) · alt bant y 805-890 TEPSI RAFI (2 yan yana)",
"xB = X0+px(370)",
"ln(xB,Y0+px(50),xB,Y0+px(795),1.1,'#111','6,5')",
"ln(X0+px(15),Y0+px(800),X0+px(685),Y0+px(800),1.1,'#111','6,5')",
"# COP (sol)",
"tx(X0+px(190),Y0+px(95),'ÇÖP',10,'middle','bold')",
"ln(X0+px(40),Y0+px(120),X0+px(110),Y0+px(300),1.6); ln(X0+px(340),Y0+px(120),X0+px(270),Y0+px(300),1.6); ln(X0+px(40),Y0+px(120),X0+px(340),Y0+px(120),1.6)",
"not_(X0+px(190),Y0+px(200),'huni ağzı — robot bırakır, durmaz',fs=8)",
"ln(X0+px(110),Y0+px(300),X0+px(110),Y0+px(330),1.2); ln(X0+px(270),Y0+px(300),X0+px(270),Y0+px(330),1.2)",
"rc(X0+px(75),Y0+px(340),px(230),px(440),1.6,4)",
"ln(X0+px(75),Y0+px(390),X0+px(305),Y0+px(390),1); not_(X0+px(190),Y0+px(376),'poşet kelepçesi',fs=7.5)",
"tx(X0+px(190),Y0+px(560),'KOVA 30 L',10,'middle','bold')",
"not_(X0+px(190),Y0+px(620),'Ø30 · göğüs hizasında',fs=8)",
"not_(X0+px(190),Y0+px(660),'öne çekilir, MOTORSUZ',fs=8)",
"not_(X0+px(190),Y0+px(700),'eleman HER GÜN boşaltır',fs=8)",
"# 3 UC YUVASI (sag)",
"for k,(ad,dash) in enumerate((('1 · PENÇE ucu',None),('2 · YEDEK PENÇE',None),('3 · BOŞ (büyüme)','4,3'))):",
"    y0_ = Y0+px(70+k*245)",
"    rc(X0+px(390),y0_,px(290),px(220),1.4,4,'#999' if dash else '#111',dash)",
"    tx(X0+px(535),y0_+px(35),ad,9,'middle','bold','#999' if dash else '#111')",
"    if k<2:",
"        rc(X0+px(485),y0_+px(65),px(100),px(40),1.2,2); ln(X0+px(500),y0_+px(105),X0+px(515),y0_+px(175),1.3); ln(X0+px(570),y0_+px(105),X0+px(555),y0_+px(175),1.3)",
"        not_(X0+px(535),y0_+px(205),'kilit pim+burç · \"uç var\" sensörü',fs=7)",
"# TEPSI RAFI yatay — 2 yuva yan yana",
"tx(X0+px(350),Y0+px(822),'TEPSİ RAFI — YATAY · 2 yuva yan yana (+1 kolda = 3 tepsi)',9.5,'middle','bold',Bl)",
"for i in range(2):",
"    cx_ = X0+px(180+i*340)",
"    rc(cx_-px(174),Y0+px(846),px(16),px(16),1,1); rc(cx_+px(158),Y0+px(846),px(16),px(16),1,1)",
"    el(cx_,Y0+px(854),px(165),px(10),1.4,Bl); rc(cx_-px(14),Y0+px(848),px(28),px(12),.9,1,Bl,None,'#dfe7fb')",
"    tx(cx_,Y0+px(882),'yuva %d' % (i+1),7,'middle','','#999')",
"",
]
t = t[:s] + NL.join(blk) + NL + t[e:]
# olculer
rep("oy(X0,xB,Y0-2+px(26),'36'); oy(xB,X0+px(GW),Y0-2+px(26),'34')", "oy(X0,xB,Y0-2+px(26),'37 çöp'); oy(xB,X0+px(GW),Y0-2+px(26),'33 uç')")
rep("ox(xr,Y0+px(70),Y0+px(260),'pençe 19',side='r'); ox(xr,Y0+px(320),Y0+px(720),'tepsi rafı 40',side='r'); ox(xr,Y0+px(900),Y0+px(1850),'PZP 95',side='r')",
    "ox(xr,Y0+px(70),Y0+px(780),'çöp + uç yuvaları 71',side='r'); ox(xr,Y0+px(805),Y0+px(890),'tepsi 8',side='r'); ox(xr,Y0+px(900),Y0+px(1850),'PZP 95',side='r')")
# yan kesit: raf 8 yuva -> 1 seviye (2 yan yana: yandan tek gorunur) + ust bolge (kova/uc yuvasi yandan)
s = t.index("# pence yuvasi (yandan)"); e = t.index("ln(sx,Y0+px(60),sx,Y0+px(1850),3,'#2a6a9a')")
blk = [
"# ust bolge yandan: kova + uc yuvalari (derinlik icinde), altta tepsi rafi tek seviye",
"rc(sx+px(60),Y0+px(70),px(700),px(710),1.2,4,'#777','5,4'); tx(sx+px(410),Y0+px(400),'çöp kovası / uç yuvaları (derinlik 84 içinde)',9,'middle','','#777')",
"yy = Y0+px(854)",
"ln(sx+px(160),yy-px(2),sx+px(500),yy-px(2),2.6,Bl)                                  # tepsi (yandan) — arkada",
"rc(sx+px(40),yy-px(8),px(120),px(6),1.2,1,Bl,None,'#dfe7fb')                         # kulp ONDE (robot cephesi)",
"ln(sx+px(505),yy-px(20),sx+px(505),yy+px(14),1,'#999')                                # arka ray",
"E.append('<path d=\"M %.1f %.1f L %.1f %.1f L %.1f %.1f\" fill=\"none\" stroke=\"#1d7a4f\" stroke-width=\"1.6\" stroke-dasharray=\"4,3\"/>' % (sx+px(100),yy-px(70),sx+px(100),yy-px(14),sx-px(30),yy-px(14)))",
"tx(sx+px(120),yy-px(80),'kilit kulba iner → 1 cm kaldırır → öne çeker',8.5,'start','','#1d7a4f')",
"oy(sx+px(40),sx+px(500),yy+px(40),'46 (tepsi 34 + kulp 12)')",
"not_(sx+px(650),Y0+px(870),'arkada 38 boş',fs=8.5)",
"",
]
t = t[:s] + NL.join(blk) + NL + t[e:]
# notlar
s = t.index("nots = ["); e = t.index("]", t.index("Fersah\\'a soru")) + 1
t = t[:s] + """nots = [
 ('· KABİN 70 · derinlik 84 — değişmedi','bold','#1a1a1a'),
 ('· 8 tepsi GEREKMEZ (Kemal): press plakası','','#b3452b'),
 ('  ısıtmalı → sıcak tepsi hemen kullanılır','','#b3452b'),
 ('· 3 tepsi = fırında 2 + kolda 1 (pik 30/saat)','','#333'),
 ('· Raf YATAY, 2 yuva yan yana, 8 cm bant','','#333'),
 ('  (v5\\'teki 8 katlı raf iptal)','','#666'),
 ('· Üstünde: sol huni + 30 L kova (göğüs','','#333'),
 ('  hizası, öne çekilir) · sağ 3 uç yuvası:','','#666'),
 ('  pençe · yedek pençe · boş (büyüme)','','#666'),
 ('· Kilit kulba üstten iner, 1 cm kaldırır,','','#333'),
 ('  öne çeker · kulp robota bakar','','#666'),
 ('· Derinlik 46 &lt; 84: arkada 38 boş','','#1d7a4f'),
 ('· Uç değişimi pide başına ×2 (~8 sn)','','#666'),
 ('· PZP-400 zeminde, tepsi içinde basma;','','#333'),
 ('  üst plaka Ø29 — Fersah\\'a soru','','#b3452b'),
]""" + t[e:]
rep("'AUTOKITCH · ist2_pres_detay_v5'", "'AUTOKITCH · ist2_pres_detay_v6'")
rep("ist2_pres_detay_v5.svg", "ist2_pres_detay_v6.svg")
io.open('ist2_pres6.py', 'w', encoding='utf-8', newline='\n').write(t)
print('pres6 ok')
