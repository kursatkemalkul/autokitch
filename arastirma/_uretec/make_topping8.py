# -*- coding: utf-8 -*-
# v7 -> v8: TABLA bolgesi -> ACIK DOZAJ BOSLUGU (robot tepsiyle gezdirir), cikislar kaset merkezlerinde, notlar
import io
NL = chr(10)
t = io.open('ist3_topping7.py', encoding='utf-8').read()
def rep(o, n, c=1):
    global t
    assert t.count(o) == c, 'A(%d): %s' % (t.count(o), o[:80])
    t = t.replace(o, n)

rep("İSTASYON 3 — TOPPING · DETAY v7 (HAFTALIK tedarik · 3 kaset tabanı × tek yükseklik 25 · soğutma EN ÜSTTE · çıkışlar tabla ekseninde)",
    "İSTASYON 3 — TOPPING · DETAY v8 (TEPSİ ELİ: tabla + kızak + 2 motor KALKTI · robot tepsiyi çıkış altında gezdirir · dozaj boşluğu AÇIK)")
rep("→ çark + motor ×4, HER BİRİNİN KENDİ ÇIKIŞI → DÖNER+KAYAR TABLA → GEÇİŞ RAFI 2 kat (robot takas) · buzluk YOK",
    "→ çark + motor ×4, HER BİRİNİN KENDİ ÇIKIŞI (serbest konum, ağız tabandan sarkar) → AÇIK DOZAJ BOŞLUĞU (robot + tepsi) → GEÇİŞ RAFI 2 kat (ayrı soğuk bölme) · buzluk YOK")

# cikislar: kaset merkezleri (kasar 175 / kavurma 435 / sucuk 525 / kusbasi 605)
rep("for cx0,r,sgn in ((300,55,-1),(455,40,1)):", "for cx0,r,sgn in ((200,55,-1),(470,40,1)):")
rep("for cx0 in (390,535):", "for cx0 in (400,520):")
rep("    ln(X0+px(cx0-18),Y0+px(CY+60),X0+px(cx0-18),Y0+px(CY+120),1.5); ln(X0+px(cx0+18),Y0+px(CY+60),X0+px(cx0+18),Y0+px(CY+120),1.5)",
    "    ln(X0+px(cx0-18),Y0+px(CY+60),X0+px(cx0-18),Y0+px(CY+165),1.5); ln(X0+px(cx0+18),Y0+px(CY+60),X0+px(cx0+18),Y0+px(CY+165),1.5)")
rep("    for dy in (70,93,115):", "    for dy in (70,95,120,145):")
rep("    ln(X0+px(cx0-14),Y0+px(CY+15),X0+px(cx0-14),Y0+px(CY+90),1,'#999','4,3'); ln(X0+px(cx0+14),Y0+px(CY+15),X0+px(cx0+14),Y0+px(CY+90),1,'#999','4,3')",
    "    ln(X0+px(cx0-14),Y0+px(CY+15),X0+px(cx0-14),Y0+px(CY+165),1,'#999','4,3'); ln(X0+px(cx0+14),Y0+px(CY+15),X0+px(cx0+14),Y0+px(CY+165),1,'#999','4,3')")
rep("tx(X0+px(120),Y0+px(CY+70),'kaşar çarkı BÜYÜK',8.5,'middle','bold','#b3452b')" + NL + "tx(X0+px(120),Y0+px(CY+87),'(80 g/porsiyon)',8,'middle','','#b3452b')",
    "tx(X0+px(330),Y0+px(CY+70),'kaşar çarkı BÜYÜK',8.5,'middle','bold','#b3452b')" + NL + "tx(X0+px(330),Y0+px(CY+87),'(80 g/porsiyon)',8,'middle','','#b3452b')")
rep("not_(X0+px(350),Y0+px(CY+150),'4 AYRI ÇIKIŞ, hepsi TABLA EKSENİNDE (x 30·39·45,5·53,5) — ortak boru YOK',c='#b3452b')",
    "ln(X0+px(15),Y0+px(CY+135),X0+px(685),Y0+px(CY+135),1.6,'#111')" + NL +
    "tx(X0+px(350),Y0+px(CY+172),'↑ soğuk kabin tabanı (izoleli) · 4 çıkış ağzı 3 cm SARKAR · x 20-52 bandında (tepsi duvara çarpmaz) · kapak YOK',7.5,'middle','','#b3452b')")

# TABLA blogu -> ACIK DOZAJ BOSLUGU
start = t.index("# --- TABLA + MOTOR")
end = t.index("# --- GECIS RAFI")
Q = chr(34)
blk = [
"# --- ACIK DOZAJ BOSLUGU y CY+135 .. GY (robot tepsiyle girer; sogutulmaz, kapak yok)",
"TY = CY+235",
"tx(X0+px(350),Y0+px(CY+196),'AÇIK DOZAJ BOŞLUĞU — tabla · kızak · 2 motor YOK; robot TEPSİYİ gezdirir',9.5,'middle','bold','#1a49b8')",
"txx = X0+px(200)",
"ln(txx-px(170),Y0+px(TY+50),txx+px(170),Y0+px(TY+50),3)",
"rc(txx-px(170),Y0+px(TY+38),px(12),px(12),1.3,1); rc(txx+px(158),Y0+px(TY+38),px(12),px(12),1.3,1)",
"el(txx,Y0+px(TY+44),px(140),px(6),1.2,'#8a6a3a')",
"ln(txx+px(170),Y0+px(TY+46),txx+px(188),Y0+px(TY+31),2); ln(txx+px(188),Y0+px(TY+31),txx+px(290),Y0+px(TY+31),2.2); ln(txx+px(188),Y0+px(TY+49),txx+px(290),Y0+px(TY+49),2.2); ln(txx+px(290),Y0+px(TY+31),txx+px(290),Y0+px(TY+49),2.2)",
"gx = txx+px(245)",
"rc(gx-px(9),Y0+px(TY+31)-px(20),px(18),px(20),1.4,2,'#1a49b8'); rc(gx-px(9),Y0+px(TY+49),px(18),px(16),1.4,2,'#1a49b8')",
"rc(gx-px(30),Y0+px(TY+31)-px(20)-px(26),px(60),px(26),1.6,3,'#1a49b8'); tx(gx,Y0+px(TY+31)-px(20)-px(9),'PENÇE',8,'middle','bold','#1a49b8')",
"ln(gx,Y0+px(TY+31)-px(20)-px(26),gx+px(40),Y0+px(CY+228),2.2,'#1a49b8'); tx(gx+px(48),Y0+px(CY+236),'bilek',8,'start','','#1a49b8')",
"arr(txx-px(60),Y0+px(TY+78),txx+px(120),Y0+px(TY+78),1.6,'#1a49b8'); arr(txx+px(60),Y0+px(TY+92),txx-px(120),Y0+px(TY+92),1.6,'#1a49b8')",
"tx(txx+px(60),Y0+px(TY+116),'tepsi Ø34 (kilitli uç) — kol X-Y + döndürme: spiral / halka / merkez',8.5,'middle','','#1a49b8')",
"tx(X0+px(350),Y0+px(CY+384),'26 cm: tepsi 34 + bilek payı · soğutulmaz · ön açık, kapak yok',8.5,'middle','','#555')",
"rc(X0+px(655),Y0+px(CY+135),px(25),px(265),1.1,2,'#1a49b8','4,3')",
"E.append('<text x=" + Q + "%.1f" + Q + " y=" + Q + "%.1f" + Q + " text-anchor=" + Q + "middle" + Q + " font-size=" + Q + "7.5" + Q + " fill=" + Q + "#1a49b8" + Q + " font-family=" + Q + "Arial" + Q + " transform=" + Q + "rotate(-90 %.1f %.1f)" + Q + ">soğuk hava kanalı → geçiş rafı</text>' % (X0+px(667),Y0+px(CY+268),X0+px(667),Y0+px(CY+268)))",
"",
]
t = t[:start] + NL.join(blk) + NL + t[end:]
rep("GY = TY+195", "GY = CY+400")
rep("tx(X0+px(350),Y0+px(425),'— izoleli tavan: soğuk bölge başlar —',8.5,'middle','','#888')", "tx(X0+px(150),Y0+px(424),'— izoleli tavan: soğuk bölge —',8,'middle','','#888')")
rep("tx(X0+px(350),Y0+px(GY+20),'GEÇİŞ RAFI (robot takas) — kat A',9.5,'middle','bold','#1a49b8')",
    "tx(X0+px(350),Y0+px(GY+20),'GEÇİŞ RAFI (robot takas · AYRI SOĞUK BÖLME, kendi kapağı) — kat A',9.5,'middle','bold','#1a49b8')")

# sag olculer
rep("ox(xr,Y0+px(KY0),Y0+px(KY0+250),'kaset 25',side='r'); ox(xr,Y0+px(KY0+255),Y0+px(CY+125),'çark+çıkış 22',side='r')",
    "ox(xr,Y0+px(KY0),Y0+px(KY0+250),'kaset 25',side='r'); ox(xr,Y0+px(KY0+255),Y0+px(CY+135),'çark+çıkış 23',side='r')")
rep("ox(xr,Y0+px(TY-10),Y0+px(TY+170),'tabla+motor 18',side='r'); ox(xr,Y0+px(GY),Y0+px(GY+610),'geçiş rafı 61',side='r')",
    "ox(xr,Y0+px(CY+140),Y0+px(GY-5),'AÇIK dozaj boşluğu 26',side='r'); ox(xr,Y0+px(GY),Y0+px(GY+610),'geçiş rafı 61',side='r')")

# UST GORUNUM
rep("tx(X2+p2(350),Y2-36,'ÜST GÖRÜNÜM (kaset katı) — 70 × 42 · TAM DOLU · çıkışlar tabla ekseninde',12.5,'middle','bold')",
    "tx(X2+p2(350),Y2-36,'ÜST GÖRÜNÜM (kaset katı) — 70 × 42 · TAM DOLU · çıkışlar her kasetin altında',12.5,'middle','bold')")
s2 = t.index("# tabla ekseni + travel")
e2 = t.index("oy(X2,X2+p2(350),Y2-14,'35')")
blk2 = [
"# cikislar (kirmizi) — kaset merkezleri; tepsi (mavi kesik) kasar cikisinin altinda, spiral yol",
"for cx_,cy_ in ((200,210),(400,175),(520,175),(470,300)):",
"    ci(X2+p2(cx_),Y2+p2(cy_),p2(18),1.4,'#b3452b','3,2')",
"    ci(X2+p2(cx_),Y2+p2(cy_),2.2,1,'#b3452b',None,'#b3452b')",
"ci(X2+p2(200),Y2+p2(210),p2(170),1.2,'#1a49b8','5,4')",
"ci(X2+p2(520),Y2+p2(175),p2(170),0.9,'#1a49b8','3,3')",
"rc(X2+p2(20),Y2+p2(420),p2(660),p2(60),1,0,'#1a49b8','3,3'); tx(X2+p2(350),Y2+p2(445)+4,'ÖN AÇIK — tepsi öne taşabilir (robot tarafı, duvar yok)',8,'middle','','#1a49b8')",
"pth = ''",
"for k in range(0,200):",
"    a = k*0.16; r = p2(6+k*0.62)",
"    pth += ('M' if k==0 else 'L') + '%.1f %.1f ' % (X2+p2(200)+r*math.cos(a), Y2+p2(210)+r*math.sin(a))",
"E.append('<path d=" + Q + "%s" + Q + " fill=" + Q + "none" + Q + " stroke=" + Q + "#1a49b8" + Q + " stroke-width=" + Q + "1" + Q + "/>' % pth)",
"tx(X2+p2(350),Y2+p2(510),'kırmızı: 4 ÇIKIŞ x 20·40·47·52 (kaset altında, koni 3-8 cm içe çeker) · mavi: TEPSİ Ø34 iki uç konumda + spiral yolu',9.5,'middle','','#1a49b8')",
"tx(X2+p2(350),Y2+p2(533),'tepsi merkezi x 20-52 (yan duvarlar) · y ≥ 17 (arka duvar; ön açık) → Blender modelindeki sağ uç çarpması çözüldü',9.5,'middle','','#b3452b')",
"",
]
t = t[:s2] + NL.join(blk2) + NL + t[e2:]
# kaset etiketleri ust kenara (cikislar merkezde)
rep("def tk(kx,ky,kw,kh,ad,alt,kulp=True):", "def tk(kx,ky,kw,kh,ad,alt,kulp=True,fr=0.28):")
rep("    tx(X2+p2(kx)+p2(kw/2)-(p2(12) if kulp else 0),Y2+p2(ky)+p2(kh/2)-2,ad,9.5,'middle','bold')" + NL + "    tx(X2+p2(kx)+p2(kw/2)-(p2(12) if kulp else 0),Y2+p2(ky)+p2(kh/2)+12,alt,8.2)",
    "    tx(X2+p2(kx)+p2(kw/2)-(p2(12) if kulp else 0),Y2+p2(ky)+p2(kh)*fr-2,ad,9.5,'middle','bold')" + NL + "    tx(X2+p2(kx)+p2(kw/2)-(p2(12) if kulp else 0),Y2+p2(ky)+p2(kh)*fr+12,alt,8.2)")
rep("tk(0,0,350,420,'KAŞAR','35 × 42')", "tk(0,0,350,420,'KAŞAR','35 × 42',fr=0.1)")

# notlar
rep(" ('3. Tabla ilgili ÇIKIŞIN altına kayar + döner:','#333')," + NL + " ('   merkezden kenara spiral, orta da dış da dolar','#666'),",
    " ('3. Kol TEPSİYİ ilgili çıkışın altında gezdirir:','#333')," + NL + " ('   spiral / halka / merkez — desen yazılımda','#666'),")
rep(" ('1. Kol basılmış tabanı TABLAYA koyar','#333'),", " ('1. Taban zaten TEPSİDE (press ten beri)','#333'),")
rep(" ('KARARLAR (v7):','#333'),",
    " ('KARARLAR (v8 — TEPSİ ELİ, Kemal):','#333')," + NL +
    " ('· Tabla + kızak + 2 motor + 2 sürücü KALKTI','#b3452b')," + NL +
    " ('· Çıkış konumu serbest — tek sınır: tepsi merkezi','#b3452b')," + NL +
    " ('  x 20-52, y ≥17 (yan/arka duvar); ön AÇIK','#666')," + NL +
    " ('· Dozaj boşluğu AÇIK: soğuk kapak yok, robot','#b3452b')," + NL +
    " ('  20 sn içeride kalsa da soğuk kaçmaz','#666')," + NL +
    " ('· Geçiş rafı ayrı soğuk bölme + arka kanal','#333'),")
rep(" ('· 4 çıkış tabla ekseninde ±3 cm: rotor kasetin','#333')," + NL + " ('  altında, koni malzemeyi eksene çeker (boru yok)','#666')," + NL, "")
rep("'ELEKTRİK BÖLMESİ (ÜSTTE) — PLC I/O · 4 step sürücü · 24 V güç · tabla sürücüleri'", "'ELEKTRİK BÖLMESİ (ÜSTTE) — PLC I/O · 4 step sürücü · 24 V güç (tabla sürücüleri kalktı)'")
rep("KY = Y2+p2(420)+96", "KY = Y2+p2(420)+150")
rep("'AUTOKITCH · ist3_topping_detay_v7'", "'AUTOKITCH · ist3_topping_detay_v8'")
rep("ist3_topping_detay_v7.svg", "ist3_topping_detay_v8.svg")
io.open('ist3_topping8.py','w',encoding='utf-8',newline='\n').write(t)
print('v8 uretici ok')
