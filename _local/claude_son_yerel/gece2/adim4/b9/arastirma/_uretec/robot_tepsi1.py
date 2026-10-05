# -*- coding: utf-8 -*-
# ROBOT TEPSI ELI v1 — Kemal konsepti (4 Eyl 2026, el krokileri + Blender):
# kulplu tepsi = robotun eli; pide press'ten kutuya kadar tepside; robot dozaj/sprey altinda tepsiyi GEZDIRIR
# (TOPPING tablasi + kizak + 2 motor KALKAR); press ve firin tepsiyi alir (BIRAKIR), sprey/topping/kesim tepside (BIRAKMAZ)
import io, math

E = []
def ln(x1,y1,x2,y2,w=1.4,c='#111',dash=None):
    d = ' stroke-dasharray="%s"' % dash if dash else ''
    E.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%s"%s/>' % (x1,y1,x2,y2,c,w,d))
def rc(x,y,w_,h,sw=1.4,rx=0,c='#111',dash=None,fill='none'):
    d = ' stroke-dasharray="%s"' % dash if dash else ''
    E.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%s" fill="%s" stroke="%s" stroke-width="%s"%s/>' % (x,y,w_,h,rx,fill,c,sw,d))
def ci(cx,cy,r,sw=1.4,c='#111',dash=None,fill='none'):
    d = ' stroke-dasharray="%s"' % dash if dash else ''
    E.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" stroke="%s" stroke-width="%s"%s/>' % (cx,cy,r,fill,c,sw,d))
def el(cx,cy,rx,ry,sw=1.4,c='#111',dash=None,fill='none'):
    d = ' stroke-dasharray="%s"' % dash if dash else ''
    E.append('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="%s" stroke="%s" stroke-width="%s"%s/>' % (cx,cy,rx,ry,fill,c,sw,d))
def tx(x,y,s,fs=11,a='middle',w='',col='#111'):
    fw = ' font-weight="%s"' % w if w else ''
    E.append('<text x="%.1f" y="%.1f" text-anchor="%s" font-size="%s" fill="%s" font-family="Arial"%s>%s</text>' % (x,y,a,fs,col,fw,s))
def arr(x1,y1,x2,y2,w=1.6,c='#1d7a4f'):
    ln(x1,y1,x2,y2,w,c)
    a = math.atan2(y2-y1,x2-x1)
    for da in (2.6,-2.6):
        ln(x2,y2,x2-9*math.cos(a+da),y2-9*math.sin(a+da),w,c)
def oy(x1,x2,y,cm):
    ln(x1,y,x2,y,1,'#b3452b'); ln(x1,y-5,x1,y+5,1,'#b3452b'); ln(x2,y-5,x2,y+5,1,'#b3452b')
    tx((x1+x2)/2,y-6,cm,10.5,'middle','bold','#b3452b')
def ox(x,y1,y2,cm,side='l'):
    ln(x,y1,x,y2,1,'#b3452b'); ln(x-5,y1,x+5,y1,1,'#b3452b'); ln(x-5,y2,x+5,y2,1,'#b3452b')
    xx = x-9 if side=='l' else x+9
    E.append('<text x="%.1f" y="%.1f" text-anchor="middle" font-size="10" font-weight="bold" fill="#b3452b" font-family="Arial" transform="rotate(-90 %.1f %.1f)">%s</text>' % (xx,(y1+y2)/2,xx,(y1+y2)/2,cm))

W, H = 1560, 1180
tx(40,44,'ROBOT TEPSİ UCU v1 — tepsi = robotun aksesuar ucu (kilitli) · pide press\'ten kutuya kadar TEPSİDE · fırına TEPSİYLE girer · robot dozaj/sprey altında gezdirir',17,'start','bold')
tx(40,68,'Kalkanlar: TOPPING tabla + kızak + 2 motor + 2 sürücü · sprey/kesim altı hareket · kürek · PACK iticisi (robot tepsiyi eğer). Dozaj deseni (spiral · halka · merkez) YAZILIMA iner. Hamur/kutu için PENÇE ayrı uç.',10.5,'start','','#555')

# ================= A) TEPSI UST GORUNUM =================
S = 1.05
def px(mm): return mm*S
CX, CY = 300, 470
RI, RO = 160, 172       # ic yaricap (pide O28 + 2 pay), dis yaricap (bordur 12)
KW, KL = 30, 120
tx(CX,CY-px(RO)-px(KL)-30,'TEPSİ — ÜST GÖRÜNÜM (ölçekli, mm)',12.5,'middle','bold')
ci(CX,CY,px(RO),2)
ci(CX,CY,px(RI),1.4)
# delikli taban (perfore — firinda tas etkisi, hafiflik)
for gx in range(-150,151,15):
    for gy in range(-150,151,15):
        if gx*gx+gy*gy <= (RI-14)**2:
            ci(CX+px(gx),CY+px(gy),1.5,0.6,'#999')
# pide izi
ci(CX,CY,px(140),1,'#8a6a3a','4,3')
tx(CX,CY-px(60),'pide Ø28',9,'middle','','#8a6a3a')
# on agiz (bordur acik) — alt
gap = 65
rc(CX-px(gap),CY+px(RI)-3,px(2*gap),px(RO-RI)+6,0,0,'#fff',None,'#fff')
ln(CX-px(gap),CY+px(RI),CX-px(gap),CY+px(RO),1.6); ln(CX+px(gap),CY+px(RI),CX+px(gap),CY+px(RO),1.6)
tx(CX,CY+px(RO)+22,'ÖN AĞIZ 13 cm — bordür açık: itici dilimleri kutuya kaydırır',9.5,'middle','bold','#b3452b')
# kulp — ust
KW, KL = 30, 120
rc(CX-px(KW/2),CY-px(RO)-px(KL),px(KW),px(KL)+4,1.8,3)
for yy in (35,45,55):
    ln(CX-px(KW/2),CY-px(RO)-px(KL)+px(yy),CX+px(KW/2),CY-px(RO)-px(KL)+px(yy),0.9,'#555')
tx(CX+px(KW/2)+10,CY-px(RO)-px(KL)+px(48),'KİLİT PİMİ + burç (uç değiştirici erkek parça)',9,'start','bold','#b3452b')
tx(CX+px(KW/2)+10,CY-px(RO)-px(KL)+px(90),'KULP = UÇ KİLİDİ · paslanmaz 30×20 · 120 uzun',9.5,'start','bold')
tx(CX+px(KW/2)+10,CY-px(RO)-px(KL)+px(104),'metal-metal: 350 °C tepsiyi silikon pençe tutamaz',9,'start','','#1d7a4f')
# olculer
oy(CX-px(RO),CX+px(RO),CY+px(RO)+48,'Ø 34 dış')
oy(CX-px(RI),CX+px(RI),CY+px(RI)-10,'Ø 32 iç')
ox(CX-px(RO)-28,CY-px(RO)-px(KL),CY-px(RO),'kulp 12')
tx(CX,CY+px(RO)+70,'taban DELİKLİ (Ø3 · 15 mm aralık — pizza screen mantığı: fırında taş etkisine yakın, hafif, buhar kaçar)',9,'middle','','#555')

# ================= B) YAN KESIT + PENCE =================
Y0 = 960
tx(CX,Y0-118,'YAN KESİT — bordür 12 · taban 3 · kulp 15 mm yukarıda · robot kilidi kulba oturur',12.5,'middle','bold')
xL, xR = CX-px(RO), CX+px(RO)
ln(xL,Y0,xR,Y0,3)                                    # taban 2 mm
rc(xL,Y0-px(12),px(12),px(12),1.6,1); rc(xR-px(12),Y0-px(12),px(12),px(12),1.6,1)   # bordur
ln(xL+px(12),Y0-px(12),xL+px(20),Y0,1,'#777'); ln(xR-px(12),Y0-px(12),xR-px(20),Y0,1,'#777')  # ic egim
el(CX,Y0-px(7),px(140),px(7),1.2,'#8a6a3a')          # pide
tx(CX,Y0-px(7)+3,'pide (12 mm)',8.5,'middle','','#8a6a3a')
# kulp saga: yukselen boyun + yatay kulp
ln(xR,Y0-px(6),xR+px(18),Y0-px(21),2); ln(xR+px(18),Y0-px(21),xR+px(KL),Y0-px(21),2.4)
ln(xR+px(18),Y0-px(1),xR+px(KL),Y0-px(1),2.4); ln(xR+px(KL),Y0-px(21),xR+px(KL),Y0-px(1),2.4)
tx(xR+px(60),Y0+16,'kulp 30×20',9,'middle','','#555')
# pence (paralel 2 parmak, kulbu ustten-alttan degil YANDAN sikar — burada onden gorunum ic ice)
gx = xR+px(70)
rc(gx-px(22),Y0-px(21)-px(34),px(44),px(34),1.8,3)      # kilit govdesi (disi)
rc(gx-px(6),Y0-px(21)-px(6),px(12),px(10),1.2,1,'#b3452b')   # pim yuvasi
tx(gx,Y0-px(21)-px(16),'UÇ KİLİDİ',9,'middle','bold')
ln(gx,Y0-px(21)-px(34),gx,Y0-px(21)-px(34)-px(40),2.2)
tx(gx+14,Y0-px(21)-px(34)-px(22),'robot bileği',9,'start','','#555')
tx(gx+px(30),Y0+px(22)+16,'kilit: pim + burç + kilit bilyesi (SMARTSHIFT / CoboShift sınıfı) — takma 2-3 sn, tekrar ±0,1 mm',8.5,'middle','','#555')
# olculer
ox(xL-26,Y0-px(12),Y0,'12',side='l')
oy(xL,xR,Y0+40,'34')
ox(xR+px(KL)+22,Y0-px(21),Y0-px(1),'20',side='r')
tx(40,Y0+80,'MALZEME: 3 mm DELİKLİ ALÜMİNYUM + SERAMİK yapışmaz kaplama (400 °C) · kulp paslanmaz, perçinli · ~0,8 kg — TAŞ OLMAZ (kordierit 2,3 kg + press darbesinde çatlar) · teflon OLMAZ (350 °C)',9.5,'start','bold','#b3452b')
tx(40,Y0+98,'press: tepsi alt plakaya TAM oturur → darbe yayılır, eğilmez · fırın: delikler taş/sıcak havayı tabana geçirir (pizza screen — Domino\'s standardı) · pilot: 200 ısı turu + 1 hafta yıkama',9,'start','','#555')

# ================= C) 5 ISTASYON =================
BX, BY = 640, 118
BW, BH = 245, 150
tx(BX+BW+8,BY-30,'TEPSİ 5 İSTASYONDA — BIRAKIR / BIRAKMAZ (Kemal krokisi temize)',12.5,'middle','bold')
def tray(x,y,w,h=9,kulp=True,c='#111'):
    ln(x,y,x+w,y,2.4,c); rc(x,y-h,7,h,1.3,1,c); rc(x+w-7,y-h,7,h,1.3,1,c)
    if kulp:
        ln(x+w,y-4,x+w+12,y-14,1.6,c); ln(x+w+12,y-14,x+w+40,y-14,2,c); ln(x+w+12,y-2,x+w+40,y-2,2,c); ln(x+w+40,y-14,x+w+40,y-2,2,c)
def pide(x,y,w,c='#8a6a3a'): el(x+w/2,y-5,w/2-10,5,1.1,c)
def pence(x,y,c='#1a49b8'):
    rc(x-7,y-38,14,22,1.4,2,c); rc(x-7,y+2,14,14,1.4,2,c); rc(x-16,y-70,32,32,1.5,3,c); ln(x,y-70,x,y-92,2,c)
def box(col,row,title,tag,tagc):
    x = BX+col*(BW+18); y = BY+row*(BH+22)
    rc(x,y,BW,BH,1.6,8)
    tx(x+10,y+18,title,10.5,'start','bold')
    tx(x+BW-10,y+18,tag,10,'end','bold',tagc)
    return x,y
G, Rd = '#1d7a4f', '#b3452b'
# 1 PRESS — birakir
x,y = box(0,0,'1 · PRESS','BIRAKIR',Rd)
rc(x+40,y+34,150,22,1.6,3); tx(x+115,y+49,'üst plaka Ø29 (ısıtmalı) iner',8,'middle','','#555')
tray(x+40,y+108,150,kulp=False); el(x+115,y+100,22,8,1.2,'#8a6a3a'); tx(x+115,y+92,'top',8,'middle','','#8a6a3a')
rc(x+30,y+110,170,14,1.6,2); tx(x+115,y+121,'alt plaka (ısıtmalı) — tepsi üstünde',7.5,'middle','','#555')
tx(x+115,y+142,'tepsi plakada bekler; PENÇE topu koyar; press basar; robot ucu tepsiye kilitler',7.5,'middle','',Rd)
# 2 SPREY — birakmaz
x,y = box(1,0,'2 · YAĞ SPREYİ','BIRAKMAZ',G)
rc(x+105,y+30,26,18,1.4,2);
for k in range(-2,3): ln(x+118,y+48,x+118+k*14,y+78,0.9,'#c9a227')
tray(x+40,y+108,130); pide(x+40,y+108,130); pence(x+210,y+100)
tx(x+115,y+142,'robot tepsiyi 2 sn altından geçirir',8,'middle','',G)
# 3 TOPPING — birakmaz
x,y = box(0,1,'3 · TOPPING','BIRAKMAZ',G)
for k,xx in enumerate((70,110,150)):
    ln(xx+x-9,y+30,xx+x-9,y+55,1.4); ln(xx+x+9,y+30,xx+x+9,y+55,1.4)
    for dy in (34,44,54): rc(xx+x-3,y+dy,6,6,.7,1,'#8a6a3a')
tx(x+115,y+70,'kaset çıkışları (serbest konum)',8,'middle','','#555')
tray(x+40,y+108,130); pide(x+40,y+108,130); pence(x+210,y+100)
arr(x+60,y+124,x+120,y+124,1.4,'#1a49b8'); arr(x+170,y+124,x+110,y+124,1.4,'#1a49b8')
tx(x+115,y+142,'robot GEZDİRİR: spiral/halka/merkez — tabla YOK',8,'middle','',G)
# 4 OVEN — birakir
x,y = box(1,1,'4 · OVEN','BIRAKIR',Rd)
rc(x+30,y+34,185,90,1.6,4,'#555','6,4'); tx(x+122,y+48,'kavite (taş taban) 350 °C',8,'middle','','#555')
rc(x+40,y+108,165,10,1.4,1,'#777',None,'#eee'); tx(x+122,y+116,'taş',7,'middle','','#777')
tray(x+55,y+104,135,kulp=True); pide(x+55,y+104,135)
tx(x+122,y+142,'tepsi+pide taşa konur, kilit AÇILIR, kapak kapanır; pişince robot yeniden kilitler, alır',7.2,'middle','',Rd)
# 5 PACK — birakmaz
x,y = box(0,2,'5 · PACK (kesim + kutu)','BIRAKMAZ',G)
for k in range(5): ln(x+60+k*28,y+30,x+60+k*28,y+62,1.6)
ln(x+50,y+30,x+180,y+30,1.6); tx(x+115,y+26,'bıçak iner (iz yeter) — tepsi kesim YUVASINA oturur, kuvvet yuvaya',7.5,'middle','','#555')
tray(x+40,y+108,130); pide(x+40,y+108,130)
arr(x+52,y+98,x+18,y+98,1.6,'#1a49b8'); rc(x+2,y+86,14,24,1.4,2,'#1a49b8'); tx(x+9,y+124,'kutu',7.5,'middle','','#1a49b8')
tx(x+115,y+142,'robot tepsiyi EĞER → pide ön ağızdan kutuya kayar (itici YOK), takılı kalır',7.5,'middle','',G)
# 6 DONGU
x,y = box(1,2,'6 · TEPSİ DÖNGÜSÜ (Kemal: ayrı konuşulacak)','8-10 tepsi','#555')
for k,(lab,cc) in enumerate((('KİRLİ RAF','#b3452b'),('BULAŞIK 60×60','#555'),('TEMİZ RAF','#1d7a4f'))):
    rc(x+18+k*76,y+50,62,40,1.4,4,cc); tx(x+49+k*76,y+74,lab,7.5,'middle','bold',cc)
    if k<2: arr(x+80+k*76,y+70,x+94+k*76,y+70,1.4,'#555')
tx(x+122,y+112,'pik: 2 dk\'da 1 pide, tepsi turu ~6 dk + soğuma 3 dk',8,'middle','','#555')
tx(x+122,y+126,'→ hatta 4-5 tepsi, 8-10 toplam · 80 tepsi/gün yıkama (eleman 3-4 sepet)',8,'middle','','#555')
tx(x+122,y+142,'temiz raf = PRESS yanında (robot ilk oradan alır)',8,'middle','','#1d7a4f')

# ================= D) KOL ZAMAN BUTCESI =================
TY = BY+3*(BH+22)+26
tx(BX,TY,'KOL ZAMAN BÜTÇESİ (pide başına, sn) — eskiden ~50, şimdi ~103:',11.5,'start','bold')
segs = [('top al',8,'#555'),('press koy/al',14,'#555'),('uç değiş ×2',8,'#b3452b'),('sprey',4,'#c9a227'),('dozaj gezdir',22,'#1a49b8'),('fırına koy',8,'#555'),('fırından al',8,'#555'),('kesim+kutu',14,'#555'),('kutu→göz + içecek',17,'#555')]
xx = BX; tot = sum(s[1] for s in segs); scale = 500/tot
for lab,sec,cc in segs:
    w = sec*scale
    rc(xx,TY+12,w,22,1.2,2,cc,None,'#fff'); tx(xx+w/2,TY+27,'%d' % sec,8.5,'middle','bold',cc)
    tx(xx+w/2,TY+48,lab,7.5,'middle','',cc)
    xx += w
tx(BX,TY+70,'pik 30 pide/saat → kol %d sn × 30 = %d dk/saat = DOLULUK %%%d (eskiden %%42)' % (tot, tot*30//60, tot*30*100//3600),9.5,'start','bold','#b3452b')
tx(BX,TY+86,'tek kol hâlâ yeter; 35/saat üstünde sıkışır (fırın zaten 25-35/saat tavanı)',9,'start','','#b3452b')

# ================= E) NOTLAR =================
NX, NY = 1180, 118
tx(NX,NY,'NE DEĞİŞİYOR (v7 → tepsi eli):',12.5,'start','bold')
nots = [
 ('KALKAN parçalar:','#1d7a4f'),
 ('· TOPPING tabla Ø36 + kızak + 2 motor + 2 sürücü','#1d7a4f'),
 ('· çıkışların "tabla ekseninde ±3 cm" kuralı','#1d7a4f'),
 ('  → çıkış her kasetin kendi altında, serbest','#1d7a4f'),
 ('· kombine el: KÜREK yüzü (tepsi onun yerine)','#1d7a4f'),
 ('· PACK iticisi (robot tepsiyi eğer, pide kayar)','#1d7a4f'),
 ('· sprey/kesim altındaki tüm taşıma hareketi','#1d7a4f'),
 ('· pideye doğrudan temas — hiç yok','#1d7a4f'),
 ('ROBOT UÇLARI (uç değiştirici — PRESS kabini):','#333'),
 ('  TEPSİ (kilitli aksesuar) · PENÇE (hamur, kutu,','#666'),
 ('  içecek, kaset kulbu) · uç değişimi pide başı ×2','#666'),
 ('','#333'),
 ('KARAR / DOĞRULAMA NOKTALARI:','#b3452b'),
 ('1 PRESS: üst plaka Ø40 bordüre çarpar →','#b3452b'),
 ('  Ø29 plaka/kalıp — Fersah\'a soru','#666'),
 ('2 MALZEME: delikli alüminyum + seramik kaplama;','#b3452b'),
 ('  taş olmaz (ağır, çatlar), teflon olmaz (350 °C)','#666'),
 ('3 KESİM: bıçak kuvveti (1-2 kN) robota gelmesin →','#b3452b'),
 ('  tepsi kesim yuvasına oturur, kilit takılı kalır;','#666'),
 ('  "iz yeter" → kuvvet düşük, bıçak kaplamayı çizmez','#666'),
 ('4 Tepsi havuzu / yıkama — ayrı konuşulacak','#b3452b'),
 ('5 Sıcak tepsi (150 °C) sprey+kesim+kutu →','#b3452b'),
 ('  yağ erir (Kemal ✓); kutu kartonu 5 sn temas OK','#666'),
 ('','#333'),
 ('ROBOT KAZANCI / BEDELİ:','#333'),
 ('· kol işi 50 → ~103 sn/pide (dozaj + uç değişimi)','#333'),
 ('· pik doluluk %42 → ~%85 — yeter, pay azaldı','#333'),
 ('· dozaj deseni yazılım: reçete = yol + cep sayısı','#333'),
 ('· TOPPING kabini: dozaj boşluğu AÇIK olabilir','#333'),
 ('  (çıkış ağızları tabandan sarkar) → soğuk kapı','#666'),
 ('  20 sn açık kalmaz — bkz. TOPPING v8','#666'),
 ('','#333'),
 ('ÖLÇÜLER: iç Ø32 · dış Ø34 · bordür 12 · taban 3','#333'),
 ('kulp 30×20×120, 15 mm yukarıda · ön ağız 130','#333'),
 ('ağırlık ~0,8 kg · delik Ø3 @15 · kulp paslanmaz','#666'),
 ('Blender modelinle uyumlu (kulp sağda, ağız önde)','#666'),
]
yy = NY+22
for s_,c_ in nots:
    if s_: tx(NX,yy,s_,10.2,'start','bold' if s_.endswith(':') else '',c_)
    yy += 17.5

tx(W-24,H-14,'AUTOKITCH · robot_tepsi_el_v1',10,'end','','#999')
svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d"><rect width="%d" height="%d" fill="#ffffff"/>%s</svg>' % (W,H,W,H,W,H,''.join(E))
OUT = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\8_ROBOT\robot_tepsi_el_v1.svg"
io.open(OUT,'w',encoding='utf-8').write(svg)
print('yazildi:', OUT)
