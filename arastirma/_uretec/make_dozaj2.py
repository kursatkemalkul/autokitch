# -*- coding: utf-8 -*-
# v1 -> v2: A panelinde GERCEK Picnic kareleri (webp gomulu) + genisletilmis yerlesim · TEK render
import io, base64, os
NL = chr(10)
src = io.open('topping_dozaj1.py', encoding='utf-8').read()
R = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\3_TOPPING\referans"
b64 = {}
for k,n in (('IM1','picnic_kare1_kopru_kirici.webp'),('IM2','picnic_kare2_rotor.webp')):
    b64[k] = base64.b64encode(open(os.path.join(R,n),'rb').read()).decode()

def rep(o,n,c=1):
    global src
    assert src.count(o)==c, 'A(%d): %s' % (src.count(o), o[:70])
    src = src.replace(o,n)

# --- tuval + svg acilis (xlink) ---
rep('W, H = 1470, 1150', 'W, H = 1470, 1420')
rep("o.append('<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"%d\" height=\"%d\" viewBox=\"0 0 %d %d\">' % (W,H,W,H))",
    "o.append('<svg xmlns=\"http://www.w3.org/2000/svg\" xmlns:xlink=\"http://www.w3.org/1999/xlink\" width=\"%d\" height=\"%d\" viewBox=\"0 0 %d %d\">' % (W,H,W,H))")
rep("tx(30,42,'AUTOKITCH — TOPPING · DOZAJ ÜNİTESİ v1 (4 Eyl 2026)",
    "tx(30,42,'AUTOKITCH — TOPPING · DOZAJ ÜNİTESİ v2 (4 Eyl 2026)")
rep("hat_on_gorunus", "hat_on_gorunus") if False else None
rep("topping_dozaj_unitesi_v1.svg", "topping_dozaj_unitesi_v2.svg")
rep("topping_dozaj_unitesi_v1 · 4 Eyl 2026", "topping_dozaj_unitesi_v2 · 4 Eyl 2026")

# --- gorsel yardimcisi ---
rep("random.seed(7)", """random.seed(7)
IMG = {}
def img(x,y,w,h,key):
    o.append('<image x="%.1f" y="%.1f" width="%.1f" height="%.1f" preserveAspectRatio="xMidYMid slice" href="data:image/webp;base64,%s"/>' % (x,y,w,h,IMG[key]))""")

# --- A paneli: gercek kareler ---
i0 = src.index("# ================= A · REFERANS =================")
i1 = src.index("# ================= B · BİZİM DİLİM KESİTİ =================")
A = NL.join([
"# ================= A · REFERANS (gercek kareler) =================",
"XA,YA = 40,110",
"rc(XA,YA,700,430,1.4,4,'#111',None,'#fcfbf8')",
"tx(XA+14,YA+22,'A · REFERANS — Picnic Works, videodan iki kare (Kemal) + çözümlemesi',9.5,'start','bold')",
"tx(XA+14,YA+38,'firma Mayıs 2026 tasfiye — makine mantığı geçerli · dosyalar: 3_TOPPING/referans/',7,'start','',GRY)",
"IW,IH = 320,238",
"# --- kare 1 ---",
"x1,y1 = XA+22, YA+52",
"rc(x1-1,y1-1,IW+2,IH+2,1.2,2,'#111')",
"img(x1,y1,IW,IH,'IM1')",
"tx(x1,y1-4,'kare 1 (0:07) — huni içi',7.5,'start','bold',BLU)",
"arr(x1+232,y1+52,x1+150,y1+96,'#ff2d2d',2.2)",
"rc(x1+186,y1+22,132,26,1.2,3,'#ff2d2d',None,'#fff')",
"tx(x1+252,y1+39,'köprü kırıcı tel',7.6,'middle','bold','#ff2d2d')",
"arr(x1+96,y1+214,x1+140,y1+196,'#ff2d2d',2.2)",
"rc(x1+8,y1+204,96,22,1.2,3,'#ff2d2d',None,'#fff')",
"tx(x1+56,y1+219,'5 g dozaj',7.2,'middle','bold','#ff2d2d')",
"# --- kare 2 ---",
"x2,y2 = XA+366, YA+52",
"rc(x2-1,y2-1,IW+2,IH+2,1.2,2,'#111')",
"img(x2,y2,IW,IH,'IM2')",
"tx(x2,y2-4,'kare 2 (0:22) — huni ağzı',7.5,'start','bold',BLU)",
"arr(x2+40,y2+40,x2+118,y2+96,'#ff2d2d',2.2)",
"rc(x2+6,y2+16,124,26,1.2,3,'#ff2d2d',None,'#fff')",
"tx(x2+68,y2+33,'dozaj rotoru',7.6,'middle','bold','#ff2d2d')",
"arr(x2+286,y2+186,x2+214,y2+164,'#ff2d2d',2.2)",
"rc(x2+206,y2+188,110,22,1.2,3,'#ff2d2d',None,'#fff')",
"tx(x2+261,y2+203,'pide (döner)',7.2,'middle','bold','#ff2d2d')",
"# --- cozumleme metinleri ---",
"ny = YA+306",
"tx(XA+22,ny,'ince paslanmaz tel = KÖPRÜ KIRICI (bridge breaker)',7.6,'start','bold')",
"for i,s in enumerate(['karıştırıcı değil, yapışma için de değil — 2-5 dev/dk',",
"                      'lifli malzeme hunide kemer kurar: altı boşalır, üstü',",
"                      'asılı kalır, akış durur. Tel kemeri sürekli kırar.',",
"                      '\"5 GRAMS\" = tartı geri beslemeli dozaj (bizde yük hücresi)']):",
"    tx(XA+22,ny+16+i*13,s,7,'start','','#333')",
"tx(XA+366,ny,'huni ağzındaki dönen parça = DOZAJ ROTORU',7.6,'start','bold')",
"for i,s in enumerate(['devir × cep hacmi = gram — senin dediğin vida mantığı',",
"                      'peynirde helezon (auger) DEĞİL oluklu rotor: helezon',",
"                      'lifli peyniri sıkıştırıp topak yapar (panel C)',",
"                      'orada da pide dönüyor, ağız sabit — bizim kuralın aynısı']):",
"    tx(XA+366,ny+16+i*13,s,7,'start','bold' if i==3 else '',GRN if i==3 else '#333')",
"",
])
src = src[:i0] + A + src[i1:]

# --- B/C/D/E yeni konumlar ---
rep("XB,YB = 470,110", "XB,YB = 760,110")
rep("rc(XB,YB,470,410,1.4,4,'#111',None,'#fcfdff')", "rc(XB,YB,670,430,1.4,4,'#111',None,'#fcfdff')")
rep("zx = lambda c: XB+40+S*c", "zx = lambda c: XB+130+S*c")
rep("ny=YB+372", "ny=YB+386")
rep("XC,YC = 960,110", "XC,YC = 40,570")
rep("rc(XC,YC,470,410,1.4,4,'#111',None,'#fcfbf8')", "rc(XC,YC,430,380,1.4,4,'#111',None,'#fcfbf8')")
rep("yy = YC+70+i*112", "yy = YC+74+i*104")
rep("if i<2: ln(XC+16,yy+54,XC+454,yy+54,.6,'#ddd')", "if i<2: ln(XC+16,yy+50,XC+414,yy+50,.6,'#ddd')")
rep("tx(XC+16,YC+396,'Cep hacmi 25 cm³ × 6 cep = 150 cm³/tur · rotor Ø7 × boy 8 cm · paslanmaz, sökülebilir',7.2,'start','bold','#333')",
    "tx(XC+16,YC+366,'cep 25 cm³ × 6 = 150 cm³/tur · rotor Ø7 × 8 cm · paslanmaz, sökülebilir',7,'start','bold','#333')")
rep("XD,YD = 40,540", "XD,YD = 490,570")
rep("rc(XD,YD,620,290,1.4,4)", "rc(XD,YD,460,380,1.4,4)")
rep("colx = [XD+18, XD+118, XD+208, XD+300, XD+378, XD+436, XD+506]", "colx = [XD+16, XD+116, XD+196, XD+272, XD+330, XD+374, XD+420]")
rep("ln(XD+14,YD+54,XD+606,YD+54,.8,'#bbb')", "ln(XD+14,YD+54,XD+446,YD+54,.8,'#bbb')")
rep("ln(XD+14,YD+182,XD+606,YD+182,.8,'#bbb')", "ln(XD+14,YD+182,XD+446,YD+182,.8,'#bbb')")
rep("tx(XD+14,YD+24,'D · DOZAJ HESABI — cep hacmi 25 cm³, 6 cep/tur, rotor 60 dev/dk',9.5,'start','bold')",
    "tx(XD+14,YD+24,'D · DOZAJ HESABI — cep 25 cm³, 6 cep/tur, 60 dev/dk',9,'start','bold')")
rep("XE,YE = 680,540", "XE,YE = 970,570")
rep("rc(XE,YE,750,290,1.4,4)", "rc(XE,YE,460,380,1.4,4)")
rep("tx(XE+14,YE+42,'Rendelenmiş/parçalı malzeme cebe dolar; sucuk DİLİMLERİ birbirine yapışır, cebe düzensiz girer, ikişer üçer düşer.',7.4,'start','','#333')",
    "tx(XE+14,YE+42,'Parçalı malzeme cebe dolar; sucuk DİLİMLERİ birbirine yapışır,',7.2,'start','','#333')" + NL + "tx(XE+14,YE+56,'cebe düzensiz girer, ikişer üçer düşer.',7.2,'start','','#333')")
rep("yy = YE+68+i*46", "yy = YE+90+i*62")
rep("tx(XE+44,yy-2,ad,8,'start','bold',col); tx(XE+230,yy-2,ne,7.2,'start','','#333'); tx(XE+230,yy+12,sonuc,7.2,'start','bold' if i==2 else '',col)",
    "tx(XE+44,yy-2,ad,8,'start','bold',col); tx(XE+44,yy+13,ne,7,'start','','#333'); tx(XE+44,yy+27,sonuc,7,'start','bold' if i==2 else '',col)")
rep("xs_=XE+560", "xs_=XE+322")
rep("for k in range(5): rc(xs_+k*17,YE+70,13,80,1.1,2,'#111',None,'#f4ece6')",
    "for k in range(5): rc(xs_+k*17,YE+96,13,74,1.1,2,'#111',None,'#f4ece6')")
rep("ln(xs_-6,YE+156,xs_+90,YE+156,1.6,RED); tx(xs_+42,YE+168,'bıçak (dozajda keser)',6.3,'middle','bold',RED)",
    "ln(xs_-6,YE+176,xs_+90,YE+176,1.6,RED); tx(xs_+42,YE+188,'bıçak (dozajda keser)',6.3,'middle','bold',RED)")
rep("tx(xs_+42,YE+62,'sucuk çubukları (dik)',6.5,'middle','',GRY)", "tx(xs_+42,YE+88,'sucuk çubukları (dik)',6.5,'middle','',GRY)")
rep("for k in range(3): el(xs_+30+k*14,YE+178+k*4,7,3,.9,'#111',None,'#e8d5c8')", "for k in range(3): el(xs_+30+k*14,YE+198+k*4,7,3,.9,'#111',None,'#e8d5c8')")
rep("tx(XE+16,YE+228,'Öneri ③: 2 sucuk dilimi = 7,9 kg ≈ 5,5 gün (haftalık 10 kg için geçiş rafında 1 yedek yeter).',7.4,'start','bold',GRN)",
    "tx(XE+16,YE+296,'Öneri ③: 2 sucuk dilimi = 7,9 kg ≈ 5,5 gün (geçiş rafında 1 yedek).',7.2,'start','bold',GRN)")
rep("tx(XE+16,YE+244,'Bedel: dilime bıçak + servo (dilim artık tam pasif değil — kavramadan tahrik, bıçak tek eksen).',7.4,'start','','#333')",
    "tx(XE+16,YE+312,'Bedel: dilime bıçak + servo (kavramadan tahrik, tek eksen).',7.2,'start','','#333')")
rep("tx(XE+16,YE+260,'Alternatif: sucuğu tedarikçiden dilimli değil çubuk al — hem ucuz hem raf ömrü uzun (kesilmemiş).',7.4,'start','',GRY)",
    "tx(XE+16,YE+328,'Alternatif: tedarikçiden dilimli değil ÇUBUK sucuk al — ucuz, uzun ömür.',7.2,'start','',GRY)")
rep("yk0 = 850", "yk0 = 970")

# --- gorselleri goma ---
src = src.replace("o.append('<svg xmlns=", "IMG['IM1'] = %r\nIMG['IM2'] = %r\no.append('<svg xmlns=" % (b64['IM1'], b64['IM2']), 1)
io.open('topping_dozaj2.py','w',encoding='utf-8',newline='\n').write(src)
print('v2 uretici ok')
