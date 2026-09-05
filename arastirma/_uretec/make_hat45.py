# -*- coding: utf-8 -*-
# v44 -> v45: TOPPING blogu v23 (tek kap 16x54x24 · 3 kat x 2 · ust teknik yok · ALT 8 besik + sogutma) + ust gorunum + KONTROL guncel · TEK render
import io, re
NL = chr(10)
SRC = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\_uretec\teknik_cizim44.py"
t = io.open(SRC, encoding='utf-8').read()
def rep(o, n, c=1):
    global t
    assert t.count(o) == c, 'A(%d): %s' % (t.count(o), o[:80])
    t = t.replace(o, n)
def block(start_marker, end_marker, lines):
    global t
    s = t.index(start_marker); e = t.index(end_marker)
    t = t[:s] + NL.join(lines) + NL + NL + t[e:]
def repline(prefix, newline):
    global t
    lines = t.split(NL); hit = [i for i,l in enumerate(lines) if l.startswith(prefix)]
    assert len(hit) == 1, 'L(%d): %s' % (len(hit), prefix)
    lines[hit[0]] = newline; t = NL.join(lines)

# ================= TOPPING on gorunus v23 =================
block("# ================= 3 TOPPING v10", "# ================= 4 OVEN", [
"# ================= 3 TOPPING v23 (tek kap 16x54x24 simetrik · 3 kat x 2 · ust teknik YOK: elektrik arka duvar, sogutma ALT arkasi · ALT 2x4 besik) =================",
"c0,c1=xs[2],xs[3]; cm2=(c0+c1)/2",
"KAPN={0:('KAŞAR A','SUCUK küp'),410:('KAŞAR B','boş / kav.'),820:('KIYMA kav.','KUŞBAŞI sote')}",
"for yt in (0,410,820):",
"    rc(c0+px(15),Y0+px(yt+250),c1-c0-px(30),px(20),1,0,'#1a49b8',None,'#dfe7fb')",
"    for xk,nm in ((190,KAPN[yt][0]),(350,KAPN[yt][1])):",
"        bos=nm.startswith('boş'); col='#999' if bos else '#111'; dsh='4,3' if bos else None",
"        rc(c0+px(xk),Y0+px(yt+10),px(160),px(240),1.3,2,col,dsh,'#f7f6f2' if bos else '#f3efe4')",
"        if not bos:",
"            rc(c0+px(xk+8),Y0+px(yt+40),px(144),px(150),0,0,'none',None,'#e9dfa8')",
"            ln(c0+px(xk+8),Y0+px(yt+215),c0+px(xk+42),Y0+px(yt+240),.8,'#111'); ln(c0+px(xk+152),Y0+px(yt+215),c0+px(xk+118),Y0+px(yt+240),.8,'#111')",
"            ci(c0+px(xk+80),Y0+px(yt+212),px(35),1.1,'#1d7a4f',None,'#fff'); ci(c0+px(xk+80),Y0+px(yt+125),px(45),.9,'#6b4fa8','3,2')",
"            ln(c0+px(xk+80),Y0+px(yt+250),c0+px(xk+80),Y0+px(yt+300),2,'#1d7a4f')",
"        tx(c0+px(xk+80),Y0+px(yt+22),nm,6.4,'middle','bold',col)",
"        if not bos: tx(c0+px(xk+80),Y0+px(yt+34),'16×54×24 · 14,8 L',5.2,'middle','','#333')",
"    tx(c1-px(20),Y0+px(yt+22),'KAT %d' % (yt//410+1),6.5,'end','bold','#555')",
"for b in (270,680,1090):",
"    tray(c0+px(270),Y0+px(b+75),160,True); el(c0+px(430),Y0+px(b+75),px(160),px(18),1,'#1a49b8','4,3')",
"    tx(c1-px(20),Y0+px(b+40),'boşluk 14 · tepsi Ø32',5.6,'end','','#1a49b8')",
"# ALT 74: evaporator 12 + 2 sira besik (27+27) + plint 8; sogutma grubu arkada (kesikli)",
"rc(c0+px(15),Y0+px(1230),c1-c0-px(30),px(120),.9,0,'#7fb3d5',None,'#e3f2fb'); tx(cm2,Y0+px(1300),'evaporatör + fan (soğuk hava arka kanaldan katlara)',6,'middle','','#1a49b8')",
"rc(c0+px(20),Y0+px(1420),c1-c0-px(40),px(460),1,3,'#555','5,3','none'); tx(cm2,Y0+px(1455),'SOĞUTMA GRUBU arkada (20 derin, 1/12 HP)',5.6,'middle','bold','#555')",
"for r_,yt in ((1,1350),(0,1620)):",
"    for i in range(4):",
"        xk=12+i*172; lab=[['park','park','çöz. kıyma','çöz. kuşbaşı'],['kaşar yd','kaşar yd','kaşar yd','kaşar yd']][r_][i]",
"        dsh = r_==0 and i<2",
"        rc(c0+px(xk),Y0+px(yt+240),px(160),px(30),1,1,'#555',None,'#d8d4c8')",
"        rc(c0+px(xk),Y0+px(yt),px(160),px(240),1 if dsh else 1.2,2,'#999' if dsh else '#111','4,3' if dsh else None,'#f7f6f2' if dsh else '#e9eef7')",
"        tx(c0+px(xk+80),Y0+px(yt+128),lab,5.6,'middle','bold','#777' if dsh else '#333')",
"rc(c0+px(15),Y0+px(1890),c1-c0-px(30),px(80),1,0,'#555',None,'#9e9e9e'); tx(cm2,Y0+px(1940),'plint ızgarası (hava)',6,'middle','','#fff')",
"tx(c1-px(20),Y0+px(1250),'ALT 74',6.5,'end','bold','#555')",
"not_(cm2,Y0+px(1832)-px(1832)+Y0*0+Y0+px(1832)-Y0,'',fs=1)",
"tx(cm2,Y0+px(1215),'motorlar + elektrik paneli 10 cm ARKA DUVARDA (görünmez) · kapta elektrik yok · 16 kap tek tip',5.8,'middle','','#1a49b8')",
])

# ================= TOPPING ust v23 =================
block("# TOPPING ust v11", "# OVEN ust", [
"# TOPPING ust v23: kat 1 plani (kasar A + sucuk), helezon x 270/430, agizlar onde y 620, supurme R 270 (tepsi 160 + spiral 110); arka duvar 100 motorlu",
"rc(c0+px(20),YT2,c1-c0-px(40),px(100),1,0,'#555',None,'#d9d9d9'); tx(cm2,YT2+px(60),'arka duvar 10: motorlar + elektrik',6.2,'middle','bold','#333')",
"for xk,nm,alt in ((190,'KAŞAR A','16×54'),(350,'SUCUK küp','16×54')):",
"    rc(c0+px(xk),YT2+px(260),px(160),px(540),1.3,2,'#111',None,'#f3efe4')",
"    ln(c0+px(xk+80),YT2+px(280),c0+px(xk+80),YT2+px(780),1.4,'#1d7a4f'); ln(c0+px(xk+80),YT2+px(100),c0+px(xk+80),YT2+px(260),1,'#1a49b8','4,3')",
"    ci(c0+px(xk+80),YT2+px(780),px(22),1.4,'#1d7a4f',None,'#fff'); ci(c0+px(xk+80),YT2+px(780),px(270),1,'#1d7a4f','5,3')",
"    tx(c0+px(xk+80),YT2+px(400),nm,6.8,'middle','bold'); tx(c0+px(xk+80),YT2+px(430),alt,5.6,'middle','','#333')",
"    rc(c0+px(xk+60),YT2+px(100),px(40),px(40),1,1,'#1a49b8',None,'#dfe7fb')",
"rc(c0+px(15),YT2+px(800),c1-c0-px(30),px(40),1,0,'#1a49b8',None,'#dfe7fb')",
"not_(cm2,YT2+px(890),'kat 1 planı · ağızlar kap ORTASINDA x 27/43 (pide Ø30: tepsi Ø32 + spiral 11 = 27 → duvar içi) · kat 2 kaşar B + boş · kat 3 kıyma + kuşbaşı · ALT 2×4 beşik',fs=6)",
])

# ================= KONTROL =================
rep('("② OVEN kavite 40×40: tepsi Ø34 + kulp 12 = 46 → kapak kapanmaz","→ kavite derinliği 50 (dış 65 → 75) YA DA kulp 6 cm — KARAR","#b3452b")',
    '("② OVEN kavite 40×40: tepsi Ø32 + kulp 12 = 44 → kapak yine kapanmaz","→ kavite derinliği 50 (dış 65 → 75) YA DA kulp 6 cm — KARAR","#b3452b")')
rep('("③ ✓ TEPSİ DÖNMEZ (Kemal) → yalnız öteleme: ağızlar ORTA HATTA x 35, y 34·46·58·70","→ tepsi merkezi ağız etrafında r 14 tam daire çizer; izinli bölge x 17-53, y ≥17 → analiz v2","#1d7a4f")',
    '("③ ✓ TEPSİ DÖNMEZ → v23: ağızlar kap ORTASINDA x 27/43 (y 78); süpürme R 27 = tepsi 16 + spiral 11","→ sol x 0-54, sağ 16-70: duvar içi, pay 0 (iç yüzey düz) · spiral 11 kenar kapatma → prototip","#1d7a4f")')
rep('("⑤ PRESS üst plaka Ø40 → Ø29 (tepsi içinde basma)","→ Fersah\'a kalıp/plaka sorusu","#b3452b")',
    '("⑤ ✓ PRESS üst plaka Ø29: Fersah cevabı (26 Ağu) CP-330 max 36 cm açar, PLC olur, PZR-250 konveyör olur","→ \'aynı hatta pide olmaz\' dedi — yuvarlak Ø30 taban olduğu tekrar sorulacak","#9a6b1f")')
rep('("⑦ Kol sınıfı ≥12 kg (kaşar kaseti 15 kg) — UR16e / CRX-20iA/L","→ ray aynı","#9a6b1f")',
    '("⑦ ✓ Kol yükü ≤ 13 kg: tek kap 16×54×24 (kaşar 6,1 kg + kap 3,5) — 37 kg kaşar kabı yok","→ 12 kg kobot yeter (UR10e / CRX-10iA) · ray aynı","#1d7a4f")')
rep('("⑧ ✓ TOPPING 70×84: kaset katı ÖN sıra çalışan + ARKA sıra sıradaki → tam dolu","→ \'çözülme alanı\' yok: donmuş kaset arka sıradaki küçük yuvaya 1 gün önce gelir","#1d7a4f")',
    '("⑧ ✓ TOPPING v23: TEK kap tipi 16×54×24 (simetrik, ayna yok, 16 kap) · 3 kat × 2 · üst teknik yok","→ elektrik arka duvar içi, soğutma grubu ALT arkası (plint ızgarası) · ALT 2×4 beşik · STORE −18 3/modül","#1d7a4f")')
rep('("⑨ ✓ Dozaj boşluğu 14 · soğutma 15 (minibar sınıfı) · elektrik 12","→ kilit tepeye 8,5 cm, ağız 11 cm → 2,5 cm pay; düşme 6,5 cm","#1d7a4f")',
    '("⑨ ✓ Dozaj boşluğu 14 × 3 kat (tepsi 158 / 117 / 76 cm) · kilit 8,5 < ağız 11","→ 158 cm üst düzlem: kobot erişimi kontrol · her tarif tek düzlemde (kat değişimi yok)","#1d7a4f")')
rep('("⑪ 197 ✓ · 415 ✓ · derinlik 84 HER KABİN ✓ · TOPPING içi 27+25+21+14+83 = 170 + 15","→ STORE sol kolon 29+7+82+5+54 = 177 + 8 pay ✓","#1d7a4f"),',
    '("⑪ 197 ✓ · 415 ✓ · derinlik 84 HER KABİN ✓ · TOPPING içi 3×(27+14) + 74 = 197 ✓","→ STORE sol kolon 29+7+82+5+54 = 177 + 8 pay ✓ · TOPPING derinlik 4 + 54/70 + 10 = 84 ✓","#1d7a4f"),' + NL +
    ' ("⑫ Pide Ø30 → tepsi Ø34 → Ø32 zinciri: PRESS plaka Ø29 ✓ · PACK bıçak Ø28 ✓ · OVEN 44 (②) · robot uç","→ robot_tepsi_el v1 (Ø34) → v2; harçlar KAVRULMUŞ/SOTE vakumlu (çiğ olmaz); kaşar akış prototipi","#9a6b1f"),')
rep('tx(kx,ky,"KONTROL — istasyonlar arası uyum (4 Eyl 2026)",12,"start","bold","#b3452b")',
    'tx(kx,ky,"KONTROL — istasyonlar arası uyum (5 Eyl 2026)",12,"start","bold","#b3452b")')

# ================= BASLIK =================
repline('tx(X0,Y0-94,"AUTOKITCH — HAT v44',
        'tx(X0,Y0-94,"AUTOKITCH — HAT v45 · TÜM İSTASYONLAR SON VERSİYON (5 Eyl 2026) — STORE v4 · PRESS v8 · TOPPING v23 (tek kap 16×54×24, 3 kat, üst teknik yok) · OVEN tank+pompa · PACK 116",15,"start","bold")')
repline('tx(X0,Y0-72,"Robot:',
        'tx(X0,Y0-72,"Robot: tek kol (12 kg yeter — en ağır kap 13 kg), uç değiştirici — TEPSİ ucu (pide press\'ten kutuya kadar tepside, fırına tepsiyle) + PENÇE ucu (hamur · kutu · içecek · kap). Mavi = tepsi Ø32 (pide Ø30). Kırmızı = KONTROL bulgusu.",10,"start","","#333")')
repline('tx(X0,Y0-54,"Ölçüler cm.',
        'tx(X0,Y0-54,"Ölçüler cm. HER KABİN 70/65/140 × 197 × 84. Açık: ② fırın kavitesi 44 · ⑩ yağ pompa · ⑫ tepsi Ø32 zinciri (robot uç v2) · TOPPING prototip (spiral 11, kaşar akış) — bu turda çözülen: ③ ⑤ ⑦ ⑧ ⑨ ⑪",10,"start","","#333")')
rep('hat_on_gorunus_teknik_v44.svg', 'hat_on_gorunus_teknik_v45.svg')
OUT = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\_uretec\teknik_cizim45.py"
io.open(OUT, 'w', encoding='utf-8', newline='\n').write(t)
print('v45 uretici ok')
