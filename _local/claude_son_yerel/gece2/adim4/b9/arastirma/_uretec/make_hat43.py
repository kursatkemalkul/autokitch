# -*- coding: utf-8 -*-
# v42 -> v43: TOPPING v11 — TEPSI DONMEZ (yalniz oteleme): 4 agiz ORTA HATTA x 35, derinlikte y 34/46/58/70; kaset kati buna gore
import io
NL = chr(10)
t = io.open('teknik_cizim42.py', encoding='utf-8').read()
def rep(o, n, c=1):
    global t
    assert t.count(o) == c, 'A(%d): %s' % (t.count(o), o[:80])
    t = t.replace(o, n)
def block(start_marker, end_marker, lines):
    global t
    s = t.index(start_marker); e = t.index(end_marker)
    t = t[:s] + NL.join(lines) + NL + t[e:]

# ---- TOPPING on gorunus: kaset kati + koniler + carklar (agizlar orta hatta)
block("KY=300", "FL=CY+120", [
"KY=300",
"# arka sira (siradaki, acik gri) · on sira: sol KASAR A · sag: SUCUK en onde, arkasinda KUSBASI/KAVURMA (orta) ve siradaki kucukler (sag)",
"kaset(c0+px(20),Y0+px(KY-16),px(320),px(250),'KAŞAR B (arka sıra)',dash='3,3',c='#aaa')",
"kaset(c0+px(365),Y0+px(KY-16),px(320),px(250),'SUCUK yedek (arka sıra)',dash='3,3',c='#aaa')",
"kaset(c0+px(525),Y0+px(KY-8),px(160),px(250),'sıradaki KAV/KUŞ',dash='4,3',c='#999')",
"kaset(c0+px(355),Y0+px(KY-6),px(165),px(250),'KAVURMA · KUŞBAŞI',dash='4,3',c='#777')",
"kaset(c0+px(10),Y0+px(KY),px(335),px(250),'KAŞAR A','35×42×25 · 15 kg')",
"kaset(c0+px(355),Y0+px(KY),px(335),px(250),'SUCUK (en ön)','35×21×25 · 10 kg')",
"CY=KY+320",
"# koniler ORTA HATTA (x 35) toplanir",
"ln(c0+px(15),Y0+px(KY+252),c0+px(300),Y0+px(CY-55),1.2); ln(c0+px(340),Y0+px(KY+252),c0+px(330),Y0+px(CY-55),1.2)",
"ln(c0+px(360),Y0+px(KY+252),c0+px(370),Y0+px(CY-55),1.2); ln(c0+px(685),Y0+px(KY+252),c0+px(400),Y0+px(CY-55),1.2)",
"# 4 cark ayni x'te (derinlikte arka arkaya) — onden ust uste gorunur: en ondeki (B sucuk) duz, digerleri kesik/kaydirilmis",
"for k,(dx,r,c_,dash) in enumerate(((-30,38,'#aaa','3,3'),(-15,38,'#999','4,3'),(15,55,'#777','4,3'),(0,40,'#111',None))):",
"    ci(c0+px(350+dx),Y0+px(CY-6*k),px(r),1.6 if not dash else 1,c_,dash)",
"    ln(c0+px(350+dx-16),Y0+px(CY+60),c0+px(350+dx-16),Y0+px(CY+150),1.3 if not dash else .9,c_,dash); ln(c0+px(350+dx+16),Y0+px(CY+60),c0+px(350+dx+16),Y0+px(CY+150),1.3 if not dash else .9,c_,dash)",
"for k in range(6):",
"    a=k*math.pi/3; ln(c0+px(350),Y0+px(CY),c0+px(350)+px(40)*math.cos(a),Y0+px(CY)+px(40)*math.sin(a),.9)",
"rc(c0+px(120),Y0+px(CY-20),px(45),px(40),1.1,2); tx(c0+px(142),Y0+px(CY+5),'M',7,'middle','bold')",
"rc(c0+px(540),Y0+px(CY-20),px(45),px(40),1.1,2); tx(c0+px(562),Y0+px(CY+5),'M ×4',6.5,'middle','bold')",
"tx(c0+px(350),Y0+px(CY+178),'4 ağız ORTA HATTA x 35 · derinlikte y 34·46·58·70 (önden üst üste)',6,'middle','bold','#b3452b')",
])
rep("tx(cm2,Y0+px(FL-8),'4 ağız ORTA KÜMEDE (x 26-47) · 3 cm sarkar',6,'middle','','#888')", "tx(cm2,Y0+px(FL-8),'soğuk kabin tabanı · ağızlar 3 cm sarkar',6,'middle','','#888')")
rep("tx(c0+px(120),Y0+px(FL+72),'③ ✓ X-Y + ±90°',6,'middle','bold','#1d7a4f')", "tx(c0+px(120),Y0+px(FL+72),'③ ✓ yalnız ÖTELEME',6,'middle','bold','#1d7a4f')")

# ---- UST GORUNUM TOPPING v11
block("# TOPPING ust v10", "# OVEN ust", [
"# TOPPING ust v11: tepsi DONMEZ — agizlar orta hatta x 35 (y 34/46/58/70); kaset kati: sol kasar A(on)/B(arka), sag: sucuk(on)/yedek(arka), orta kav/kus, sag siradaki",
"def tk2(x,y,w,h,ad,alt='',front=True):",
"    c_='#111' if front else '#999'",
"    rc(c0+px(x)+2,YT2+px(y)+2,px(w)-4,px(h)-4,1.2 if front else 1,2,c_,None if front else '4,3')",
"    tx(c0+px(x+w/2),YT2+px(y+h/2)-1,ad,6.8 if w>200 else 6,'middle','bold',c_)",
"    if alt: tx(c0+px(x+w/2),YT2+px(y+h/2)+9,alt,5.5,'middle','',c_)",
"tk2(0,0,350,420,'KAŞAR B','sıradaki',False); tk2(350,0,350,210,'SUCUK yedek','',False)",
"tk2(350,210,170,210,'KAVURMA'); tk2(350,420,170,210,'KUŞBAŞI'); tk2(520,210,170,210,'sır. KAV','',False); tk2(520,420,170,210,'sır. KUŞ','',False)",
"tk2(0,420,350,420,'KAŞAR A','35×42'); tk2(350,630,350,210,'SUCUK','35×21')",
"rc(c0+px(170),YT2+px(170),px(360),px(670),1,0,'#1d7a4f','5,3')",
"for y_,ad in ((340,'C'),(460,'D'),(580,'A'),(700,'B')):",
"    ci(c0+px(350),YT2+px(y_),px(20),1.4,'#b3452b',None,'#fde3dc'); tx(c0+px(350),YT2+px(y_)+3,ad,6,'middle','bold','#b3452b')",
"ci(c0+px(350),YT2+px(580),px(140),.9,'#1d7a4f','4,3')",
"ci(c0+px(350),YT2+px(720),px(170),1.2,'#1a49b8','5,4'); rc(c0+px(335),YT2+px(890),px(30),px(120),1,1,'#1a49b8')",
"not_(cm2,YT2+px(890),'v11: tepsi DÖNMEZ → ağızlar orta hatta x 35 (C kav 34 · D kuş 46 · A kaşar 58 · B sucuk 70) · yeşil: C bölgesi + A için C-diski',fs=6.2)",
])

# ---- KONTROL
rep('("③ ✓ TOPPING hareket ÇÖZÜLDÜ (84 derinlik): ağızlar ortada x 26-47, y 42-62","→ tepsi merkezi x 17-53, y ≥17 · kulp öne ±90° → merkez + kenar hepsi","#1d7a4f")',
    '("③ ✓ TEPSİ DÖNMEZ (Kemal) → yalnız öteleme: ağızlar ORTA HATTA x 35, y 34·46·58·70","→ tepsi merkezi ağız etrafında r 14 tam daire çizer; izinli bölge x 17-53, y ≥17 → analiz v2","#1d7a4f")')
rep('tx(X0,Y0-94,"AUTOKITCH — HAT v42 · TÜM İSTASYONLAR SON VERSİYON (4 Eyl 2026) — STORE v39 · PRESS v7 (yatay katmanlar) · TOPPING v10 (70×84, orta küme) · OVEN tank+pompa · PACK 116 kutu",15,"start","bold")',
    'tx(X0,Y0-94,"AUTOKITCH — HAT v43 · TÜM İSTASYONLAR SON VERSİYON (4 Eyl 2026) — STORE v39 · PRESS v7 (yatay) · TOPPING v11 (70×84, tepsi dönmez, ağızlar orta hatta) · OVEN tank+pompa · PACK 116",15,"start","bold")')
rep('hat_on_gorunus_teknik_v42.svg', 'hat_on_gorunus_teknik_v43.svg')
io.open('teknik_cizim43.py', 'w', encoding='utf-8', newline='\n').write(t)
print('v43 uretici ok')
