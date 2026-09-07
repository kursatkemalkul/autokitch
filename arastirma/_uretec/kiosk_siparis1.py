# -*- coding: utf-8 -*-
# KİOSK v1 (7 Eyl 2026) — Kemal: sipariş ekranı dolabın üstünde olmasın, AYRI olsun (sipariş veren kuryeyi bloke etmesin) ama her şey bir cephede;
# ekranın boyutu/içi, TR üreticiler, "beyin yok değil mi", POS + fiş, üstünde ne olacak.
import io, math, xml.dom.minidom
W, H = 1460, 940
o = []; AP = chr(39)
def esc(s): return str(s).replace('&','&amp;').replace('<','&lt;')
def ln(x1,y1,x2,y2,w=1,c='#111',d=None):
    o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%s"%s stroke-linecap="round"/>' % (x1,y1,x2,y2,c,w,(' stroke-dasharray="%s"'%d) if d else ''))
def rc(x,y,w,h,sw=1,r=0,c='#111',d=None,f='none'):
    o.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%s" fill="%s" stroke="%s" stroke-width="%s"%s/>' % (x,y,w,h,r,f,c,sw,(' stroke-dasharray="%s"'%d) if d else ''))
def ci(x,y,r,sw=1,c='#111',d=None,f='none'):
    o.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" stroke="%s" stroke-width="%s"%s/>' % (x,y,r,f,c,sw,(' stroke-dasharray="%s"'%d) if d else ''))
def tx(x,y,s,fs=9,anc='start',fw='',col='#111'):
    o.append('<text x="%.1f" y="%.1f" font-size="%s" text-anchor="%s" font-weight="%s" fill="%s" font-family="Segoe UI, Arial, sans-serif">%s</text>' % (x,y,fs,anc,fw or 'normal',col,esc(s)))
def txr(x,y,s,fs=5,col='#555',fw=''):
    o.append('<text x="%.1f" y="%.1f" font-size="%s" text-anchor="middle" font-weight="%s" fill="%s" font-family="Segoe UI, Arial, sans-serif" transform="rotate(-90 %.1f %.1f)">%s</text>' % (x,y,fs,fw or 'normal',col,x,y,esc(s)))
def dim(x1,y1,x2,y2,s,fs=5.6,off=0,col='#111'):
    ln(x1,y1,x2,y2,.7,col)
    for (x,y) in ((x1,y1),(x2,y2)):
        if abs(y2-y1)<abs(x2-x1): ln(x,y-3,x,y+3,.7,col)
        else: ln(x-3,y,x+3,y,.7,col)
    if abs(y2-y1)<abs(x2-x1): tx((x1+x2)/2,y1-3+off,s,fs,'middle','bold',col)
    else: tx(x1+4+off,(y1+y2)/2+2,s,fs,'start','bold',col)
def para(x,y,s,maxc,fs=5.9,col='#333',fw='',lh=None):
    lh = lh or fs*1.6; cur=''; lines=[]
    for wd in s.split(' '):
        if cur and len(cur)+1+len(wd) > maxc: lines.append(cur); cur=wd
        else: cur = (cur+' '+wd) if cur else wd
    if cur: lines.append(cur)
    for l in lines: tx(x,y,l,fs,'start',fw,col); y += lh
    return y
GRN,RED,BLU,GRY,AMB,PUR,DARK,ICE='#1d7a4f','#c0392b','#1a49b8','#666','#b7791f','#6b4fa8','#2b2e33','#e3f2fb'
o.append('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">' % (W,H,W,H)); rc(0,0,W,H,0,0,'none',None,'#fff')
tx(30,40,'AUTOKITCH — KİOSK v1 (7 Eyl 2026) — SİPARİŞ KİOSKU (ayrı, 40 × 197, 32" dokunmatik + ÖKC POS + fiş) + TESLİM EKRANI (dolap üstünde 10", yalnız kod) · aynı cephede yan yana = 180 · BEYİN kioskta DEĞİL',13.5,'start','bold')
tx(30,62,'Kemal: "sipariş ekranı ayrı olsun; ikisi aynı yerde olursa sipariş veren kuryeyi bloke eder, tatsız · ama her şey bir yerde toplansın · boyutu, içi ne · Türkiye'+AP+'de yapan var mı · beyin yok değil mi · POS, fiş · üstünde ne olacak?"',9,'start','','#444')
ln(30,74,W-30,74,.8,'#999')
# ================= A · CEPHE =================
XA,YA,WA,HA_ = 40,90,420,410
rc(XA,YA,WA,HA_,1.4,4,'#111',None,'#fcfdff'); tx(XA+14,YA+22,'A · CEPHE 180 — KİOSK 40 + PICKUP 140 · iki kuyruk ayrı',10,'start','bold')
K=1.3; ax=XA+40; az=YA+44+K*197
X=lambda x: ax+K*x; Z=lambda z: az-K*z
rc(X(0),Z(197),K*40,K*185,1.3,2,'#111',None,'#d9dcdf'); rc(X(0),Z(12),K*40,K*12,1,0,'#555',None,'#9e9e9e')
rc(X(3),Z(176),K*34,K*71,1.2,2,'#111',None,DARK); tx(X(20),Z(142)+2,'32" dokunmatik',5,'middle','bold','#fff'); tx(X(20),Z(134)+2,'SİPARİŞ + ÖDEME',4.4,'middle','','#ddd')
rc(X(6),Z(102),K*12,K*8,.9,1,'#333',None,'#bbb'); tx(X(12),Z(97)+2,'POS',3.6,'middle','bold')
rc(X(22),Z(102),K*12,K*8,.9,1,'#333',None,'#ddd'); tx(X(28),Z(97)+2,'fiş',3.6,'middle','bold')
rc(X(15),Z(112),K*10,K*5,.8,1,'#333',None,'#bbb'); tx(X(20),Z(108.5)+2,'QR',3.4,'middle','bold')
rc(X(0),Z(197)+2,K*40,0,0,0,'none'); tx(X(20),Z(6)+2,'plint',3.8,'middle','','#fff')
rc(X(42),Z(197),K*140,K*185,1.3,2,'#111',None,'#dfe1e4'); rc(X(42),Z(12),K*140,K*12,1,0,'#555',None,'#9e9e9e')
for r in range(6):
    for c in range(2):
        x0=44+c*61; z0=60+r*20; rc(X(x0),Z(z0+20),K*58,K*20,.7,1,'#666',None,'#eceef1' if r<5 else '#f6efe0')
rc(X(164),Z(180),K*16,K*120,.8,1,'#333',None,'#f4f4f4'); rc(X(166),Z(155),K*12,K*22,1,1,'#111',None,DARK); tx(X(172),Z(143)+2,'10"',3.8,'middle','bold','#fff'); tx(X(172),Z(136)+2,'KOD',3.2,'middle','','#ddd')
rc(X(167),Z(128),K*10,K*7,.7,1,'#333',None,'#ddd'); rc(X(167),Z(118),K*10,K*6,.7,1,'#333',None,'#bbb')
rc(X(44),Z(60),K*136,K*48,.7,0,'#666',None,ICE); tx(X(112),Z(38)+2,'PANO: BEYİN PC burada',4.4,'middle','bold','#1a49b8')
dim(X(0),Z(0)+14,X(40),Z(0)+14,'40',5); dim(X(42),Z(0)+14,X(182),Z(0)+14,'140',5); dim(X(0),Z(0)+30,X(182),Z(0)+30,'180 (+ arada 2 fuga)',5.4)
# zemin kuyruk noktalari
for (xx,lab,col) in ((20,'sipariş veren',BLU),(112,'alan / kurye',GRN)): ci(X(xx),Z(0)+52,7,1,col,'3,2','none'); tx(X(xx),Z(0)+66,lab,4.2,'middle','',col)
tx(X(66),Z(0)+52+2,'≈ 1 m',4,'middle','',GRY)
para(XA+14,YA+384,'İki ayrı ekran, tek cephe: soldaki uzun iş (sipariş + ödeme, 1–2 dk), sağdaki 3 saniyelik iş (kod gir, kapı açılır). Kurye asla sipariş verenin arkasında beklemez.',96,5.2,GRN,'bold')
# ================= B · KİOSK ÖNDEN =================
XB,YB,WB,HB = 480,90,300,560
rc(XB,YB,WB,HB,1.4,4,'#111',None,'#fff'); tx(XB+14,YB+22,'B · SİPARİŞ KİOSKU 40 × 197 × 25 — duvara gömme',10,'start','bold')
KB=2.4; bx=XB+120; bz=YB+46+KB*197
BX=lambda x: bx+KB*x; BZ=lambda z: bz-KB*z
rc(BX(0),BZ(197),KB*40,KB*185,1.4,2,'#111',None,'#d9dcdf'); rc(BX(0),BZ(12),KB*40,KB*12,1,0,'#555',None,'#9e9e9e'); tx(BX(20),BZ(5.5)+2,'plint 12',4.2,'middle','','#fff')
rc(BX(3),BZ(181),KB*34,KB*71,1.3,2,'#111',None,DARK); tx(BX(20),BZ(150)+2,'32" DOKUNMATİK',6,'middle','bold','#fff'); tx(BX(20),BZ(142)+2,'portre 40×71 · 1080×1920',4.2,'middle','','#ddd'); tx(BX(20),BZ(135)+2,'merkez z 145 · cam 4 mm',4,'middle','','#ddd')
ci(BX(20),BZ(186),2.2,1,'#333',None,'#333'); tx(BX(20)+5,BZ(186)+2,'kamera + hoparlör',3.8,'start','','#333')
rc(BX(15),BZ(108.5),KB*10,KB*4.5,.9,1,'#333',None,'#bbb'); tx(BX(20),BZ(102.6)+2,'2D okuyucu (app QR, kupon)',3.6,'middle','','#333')
rc(BX(5),BZ(101),KB*13,KB*9,1,1,'#333',None,'#c9ced4'); tx(BX(11.5),BZ(97)+2,'ÖKC POS',4.2,'middle','bold'); tx(BX(11.5),BZ(93.5)+2,'temassız · çip',3.2,'middle','','#333')
rc(BX(22),BZ(101),KB*13,KB*9,1,1,'#333',None,'#e6e6e6'); tx(BX(28.5),BZ(97)+2,'FİŞ ağzı',4.2,'middle','bold'); tx(BX(28.5),BZ(93.5)+2,'80 mm termal',3.2,'middle','','#333')
rc(BX(3),BZ(90),KB*34,KB*28,.8,1,'#666',None,'#e3f2fb'); tx(BX(20),BZ(84)+2,'GÖVDE 28: mini PC (i5 / 8 GB)',4.2,'middle','bold','#1a49b8'); tx(BX(20),BZ(78)+2,'yazıcı (rulo 80 mm) · PSU · LAN',4,'middle','','#1a49b8'); tx(BX(20),BZ(70)+2,'BEYİN YOK — yalnız istemci,',4,'middle','bold',RED); tx(BX(20),BZ(65)+2,'LAN ile BEYİN'+AP+'e bağlı',4,'middle','bold',RED)
rc(BX(3),BZ(60),KB*34,KB*48,.8,1,'#666',None,'#eee'); tx(BX(20),BZ(40)+2,'servis kapağı',4,'middle','','#555'); tx(BX(20),BZ(34)+2,'(eleman: rulo, POS)',3.6,'middle','','#555')
dim(BX(0),BZ(197)-12,BX(40),BZ(197)-12,'40',5)
for z0,z1,lab in ((110,181,'ekran 71'),(92,101,'POS/fiş'),(62,90,'gövde 28'),(12,62,'servis 50')):
    dim(BX(40)+14,BZ(z1),BX(40)+14,BZ(z0),lab,4.4,0,GRY)
tx(BX(-4),BZ(145)+2,'z 145',4.2,'end','bold',GRY); ln(BX(-2),BZ(145),BX(0),BZ(145),.8,GRY)
tx(BX(-4),BZ(97)+2,'z 92–101',4.2,'end','bold',GRY); tx(BX(-4),BZ(93)+2,'(kart / fiş)',3.6,'end','',GRY)
para(XB+14,YB+528,'Ölçüler: 32" portre ekran 40×71 (merkez z 145 = göz hizası), POS ve fiş z 92–101 (bel), tekerlekli sandalye için POS erişimi ≤ 120 ✓. Derinlik 25 duvara gömülü; ayaklı model istenirse 55×40 taban, aynı iç.',72,5.1,'#333')
# ================= C · SİPARİŞ EKRANI AKIŞI =================
XC,YC,WC,HC = 800,90,620,300
rc(XC,YC,WC,HC,1.4,4,'#111',None,'#fcfdff'); tx(XC+14,YC+22,'C · SİPARİŞ EKRANI AKIŞI — 6 adım, 60–90 sn',10,'start','bold')
steps=[('1 MENÜ','Kaşarlı · Sucuklu · Kıymalı · Kuşbaşılı · Karışık (foto + fiyat) · "en çok satan"'),
       ('2 ÜRÜN','adet · ekstra kaşar · acı · +içecek öner (kola, ayran, su) · +tatlı öner'),
       ('3 SEPET','tutar · tahmini hazır süresi 5–8 dk · "yerinde al / kurye ile" seçimi'),
       ('4 TELEFON (isteğe bağlı)','SMS için numara; vermezse kod fişe basılır · dil TR/EN'),
       ('5 ÖDEME','temassız kart · yemek kartı · QR ödeme (app) · nakit YOK'),
       ('6 FİŞ + KOD','fiş: sipariş no + 4 haneli DOLAP KODU + süre · ekranda "hazır olunca dolap no yanar"')]
for i,(t,s_) in enumerate(steps):
    cx_=XC+16+i*100; rc(cx_,YC+40,90,150,1,3,'#333',None,'#fff'); rc(cx_,YC+40,90,16,0,3,'none',None,DARK); tx(cx_+45,YC+51,t,5.2,'middle','bold','#fff')
    para(cx_+5,YC+68,s_,20,4.8,'#333')
para(XC+14,YC+206,'Kural: sipariş anında BEYİN dolap ayırmaz; pide hazır olunca (4–8 dk) boş dolaba koyar ve o sırada dolap numarasını ekranda + SMS'+AP+'te bildirir. Kod 4 hane, fişte de yazar; telefon şart değil.',110,5.1,'#333')
para(XC+14,YC+250,'Aynı ekran "Gel-Al / Kurye" tuşu da taşır (yedek): teslim ekranı bozulursa kod burada girilir. Normalde girilmez → kuyruk karışmaz.',110,5.1,GRY)
# ================= D · TESLİM EKRANI UI =================
XD,YD,WD,HD = 800,410,300,240
rc(XD,YD,WD,HD,1.4,4,'#111',None,'#fff'); tx(XD+14,YD+22,'D · TESLİM EKRANI 10" (dolap şeridi) — 3 saniyelik iş',10,'start','bold')
rc(XD+20,YD+40,80,140,1.2,3,'#111',None,DARK)
tx(XD+60,YD+56,'KODUNUZU GİRİN',4.6,'middle','bold','#fff'); rc(XD+30,YD+62,60,12,.6,2,'#888',None,'#444'); tx(XD+60,YD+71,'_ _ _ _',6,'middle','bold','#fff')
for r in range(4):
    for c in range(3):
        rc(XD+32+c*19,YD+80+r*19,16,16,.6,2,'#888',None,'#3a3d42'); tx(XD+40+c*19,YD+91+r*19,str([1,2,3,4,5,6,7,8,9,'←',0,'✓'][r*3+c]),5,'middle','bold','#fff')
tx(XD+60,YD+170,'ya da QR okut ↓',4,'middle','','#ccc')
rc(XD+115,YD+40,165,60,1,2,BLU,None,'#eef3ff'); para(XD+122,YD+54,'MÜŞTERİ: SMS kodu ya da fişteki kod → dolap açılır, LED yanar, ekranda "Dolap 7".',44,4.8,'#1a49b8')
rc(XD+115,YD+108,165,60,1,2,RED,None,'#fff2f0'); para(XD+122,YD+122,'KURYE: "Kurye" tuşu → sipariş numarasının son 4 hanesi (kurye uygulamasında) → dolap açılır.',44,4.8,RED)
para(XD+115,YD+186,'PIN pad fiziksel (eldivenle de basılır) + 2D okuyucu + kamera. Yanlış 3 → 2 dk kilit.',44,4.8,'#333')
# ================= E · İÇİNDE NE VAR · TR ÜRETİCİ · FİŞ =================
XE,YE,WE,HE = 1120,410,300,240
rc(XE,YE,WE,HE,1.4,4,'#111',None,'#fff'); tx(XE+14,YE+22,'E · TÜRKİYE'+AP+'DE VAR MI? · POS ve FİŞ',10,'start','bold')
yy=para(XE+14,YE+40,'VAR, çok: KioSelf (yerli üretim), Onega/Zenyo KSK-3200 (32", i5, 2D okuyucu, 80 mm yazıcı), İnnova, Kardo POS, Novem, PandaX, Menulux, Posgo, robotPOS. Tipik paket: 21–32" ekran + ayak + fiş yazıcı + ödeme cihazı; HD İskender, Kahve Dünyası, Köfteci Ramiz kullanıyor. Tahmini 50–120 bin TL (teklif alınacak).',60,5.0,'#333')
yy=para(XE+14,yy+3,'FİŞ: perakende satışta fiş zorunlu → ÖKC (yazarkasa) entegre POS: Ingenico Move 2500 ÖKC / PAX A920 ÖKC / Hugin — banka POS + yazarkasa tek cihaz, fişi kendi keser. Kağıtsız istersek e-Arşiv fatura yolu var; mali müşavire sorulacak.',60,5.0,'#333')
para(XE+14,yy+3,'Yazılım: kioskun kendi menü/ödeme yazılımı (üreticiden) + BEYİN API: sipariş JSON olarak BEYİN'+AP+'e, dolap no geri.',60,5.0,GRN,'bold')
# ================= F · SORULAR =================
XF,YF,WF,HF = 40,670,1380,250
rc(XF,YF,WF,HF,1.4,4,'#111',None,'#fcfdff'); tx(XF+14,YF+22,'F · KEMAL'+AP+'İN SORULARI — CEVAPLAR',10,'start','bold')
QA=[('NEDEN AYRI EKRAN, AMA NASIL BİR YERDE?','Aynı cephe, iki ekran: solda 40 cm sipariş kiosku (1–2 dk iş), sağda dolap şeridinde 10" teslim ekranı (3 sn iş). Kurye ve gel-al müşterisi sipariş verenin arkasında beklemez. Cephe 180: kiosk 40 + PICKUP 140. Zeminde iki bekleme noktası, 1 m ara.'),
    ('SİPARİŞ EKRANI NASIL, BOYUTU NE?','32" dokunmatik, dikey 40×71, merkez göz hizası z 145. Altında ÖKC entegre POS ve fiş ağzı z 92–101, 2D okuyucu, kamera+hoparlör üstte. Gövde 40×197×25 duvara gömülü; ayaklı istenirse 55×40 taban. Akış 6 adım: menü, ürün, sepet, telefon (isteğe bağlı), ödeme, fiş+kod.'),
    ('BEYİN YOK DEĞİL Mİ?','Yok. Kioskta yalnız küçük bir PC var, ekranı ve POS'+AP+'u çalıştırır; siparişi LAN ile BEYİN'+AP+'e gönderir. BEYİN PICKUP kabininin alt panosunda (z 12–60), hattın hepsini oradan yönetir. Kiosk bozulsa hat çalışır, sadece yeni sipariş alınmaz (app siparişleri devam eder).'),
    ('POS, FİŞ, ÜSTÜNDE NE OLACAK?','ÖKC entegre POS (temassız + çipli, yemek kartı), 80 mm termal fiş (sipariş no + dolap kodu + süre), 2D okuyucu (app QR, kupon), kamera, hoparlör, LAN. Nakit yok. Fiş kesmek yasal zorunluluk; kağıtsız e-Arşiv seçeneği mali müşavirle. Türkiye'+AP+'de KioSelf, Onega, Kardo, Novem hazır satıyor.')]
col_x=(XF+14,XF+700); yy=[YF+42,YF+42]
for i,(q,a_) in enumerate(QA):
    c=i%2; tx(col_x[c],yy[c],q,6.2,'start','bold',RED if c==0 else BLU); yy[c]=para(col_x[c],yy[c]+9,a_,112,5.4,'#333')+4
tx(W-40,H-8,'AUTOKITCH · arastirma/6_PICKUP/kiosk_siparis_ekrani_v1 · 7 Eyl 2026',7,'end','',GRY)
o.append('</svg>'); svg=chr(10).join(o); xml.dom.minidom.parseString(svg.encode('utf-8'))
out=r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\6_PICKUP\kiosk_siparis_ekrani_v1.svg"
io.open(out,'w',encoding='utf-8').write(svg); print('ok')
