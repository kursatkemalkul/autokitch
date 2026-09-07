# -*- coding: utf-8 -*-
# PICKUP v1 (7 Eyl 2026) — QR/PIN teslim dolabı: kaç dolap (satışa göre), dolap ölçüsü (3 pide + içecek + tatlı), kapılar (ön müşteri / arka robot klapesi, ısıtıcı yok),
# kod akışı (kendi app / platform Gel-Al / kurye), robot adresleme (sabit XYZ, BEYİN tablosu), TR/yurt dışı satın alma.
import io, math, xml.dom.minidom
W, H = 1460, 900
o = []; AP = chr(39)
def esc(s): return str(s).replace('&','&amp;').replace('<','&lt;')
def ln(x1,y1,x2,y2,w=1,c='#111',d=None):
    o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%s"%s stroke-linecap="round"/>' % (x1,y1,x2,y2,c,w,(' stroke-dasharray="%s"'%d) if d else ''))
def rc(x,y,w,h,sw=1,r=0,c='#111',d=None,f='none'):
    o.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%s" fill="%s" stroke="%s" stroke-width="%s"%s/>' % (x,y,w,h,r,f,c,sw,(' stroke-dasharray="%s"'%d) if d else ''))
def ci(x,y,r,sw=1,c='#111',d=None,f='none'):
    o.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" stroke="%s" stroke-width="%s"%s/>' % (x,y,r,f,c,sw,(' stroke-dasharray="%s"'%d) if d else ''))
def el(cx,cy,rx,ry,sw=1,c='#111',d=None,f='none'):
    o.append('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="%s" stroke="%s" stroke-width="%s"%s/>' % (cx,cy,rx,ry,f,c,sw,(' stroke-dasharray="%s"'%d) if d else ''))
def tx(x,y,s,fs=9,anc='start',fw='',col='#111'):
    o.append('<text x="%.1f" y="%.1f" font-size="%s" text-anchor="%s" font-weight="%s" fill="%s" font-family="Segoe UI, Arial, sans-serif">%s</text>' % (x,y,fs,anc,fw or 'normal',col,esc(s)))
def txr(x,y,s,fs=5,col='#555',fw=''):
    o.append('<text x="%.1f" y="%.1f" font-size="%s" text-anchor="middle" font-weight="%s" fill="%s" font-family="Segoe UI, Arial, sans-serif" transform="rotate(-90 %.1f %.1f)">%s</text>' % (x,y,fs,fw or 'normal',col,x,y,esc(s)))
def arr(x1,y1,x2,y2,c='#c0392b',w=1.3):
    ln(x1,y1,x2,y2,w,c); a=math.atan2(y2-y1,x2-x1)
    for s in (1,-1): ln(x2,y2,x2-7*math.cos(a-s*.42),y2-7*math.sin(a-s*.42),w,c)
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
def hatch(x,y,w,h,step=4,c='#999',f='#f3f0e6'):
    rc(x,y,w,h,.6,0,c,None,f); k=0
    while k < w+h:
        ln(x+max(0,k-h),y+min(k,h),x+min(k,w),y+max(0,k-w),.4,c); k+=step
def f1(v): return ('%.1f' % v).replace('.',',')
GRN,RED,BLU,GRY,AMB,PUR,KRAFT,ICE,DARK='#1d7a4f','#c0392b','#1a49b8','#666','#b7791f','#6b4fa8','#e8d8b0','#e3f2fb','#2b2e33'
# ---------------- sayılar ----------------
PIDE_GUN=(80,100); PIDE_SIP=1.4; PIK_PAY=0.5; PIK_SAAT=2.0
SIP_GUN=tuple(round(p/PIDE_SIP) for p in PIDE_GUN)            # 57, 71
SIP_PIK=tuple(round(s*PIK_PAY/PIK_SAAT) for s in SIP_GUN)      # 14, 18 /saat
SIP_PIK_MAX=20
DWELL_ORT, DWELL_MAX = 12, 25                                  # dk
DOLU_ORT = SIP_PIK_MAX*DWELL_ORT/60                            # 4
DOLU_95 = 8                                                    # Poisson(4) %95
GEC = 2
N_GEREK = DOLU_95+GEC                                          # 10
N_TASARIM = 12
BOX=(32.4,32.4,4.4); LK_IN=(56,36,16); LK_PITCH=(60,20); DERIN=60
o.append('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">' % (W,H,W,H)); rc(0,0,W,H,0,0,'none',None,'#fff')
tx(30,40,('AUTOKITCH — PICKUP v1 (7 Eyl 2026) — QR / PIN TESLİM DOLABI: %d dolap (hesap: %d gerek) · dolap içi 56×36×16 (3 pide + 2 içecek + 2 tatlı) · ön kapı müşteri, arka klape robot · ısıtıcı YOK · kod BEYİN'+AP+'den · kabin 140 × 60 × 197') % (N_TASARIM,N_GEREK),13.5,'start','bold')
tx(30,62,'Kemal: "kaç kutu, nasıl hesap? · boyut ne, üst üste 3 kutu, içecek yatık, tatlı yanda? · arka kapak var mı, ısıtıcı? · Getir/Yemeksepeti QR mi numara mı, kurye nasıl açar? · Türkiye'+AP+'de satan var mı? · robot nasıl adresler, kamera mı ana sistem mi?" — cevaplar bu paftada.',9,'start','','#444')
ln(30,74,W-30,74,.8,'#999')
# ================= A · MÜŞTERİ CEPHESİ =================
XA,YA,WA,HA_ = 40,90,330,560
rc(XA,YA,WA,HA_,1.4,4,'#111',None,'#fcfdff'); tx(XA+14,YA+22,'A · MÜŞTERİ CEPHESİ 140 × 197 — 2 sütun × 6 sıra + kiosk şeridi',10,'start','bold')
K=2.0; ax=XA+30; az=YA+44+K*197
X=lambda x: ax+K*x; Z=lambda z: az-K*z
rc(X(0),Z(197),K*140,K*185,1.4,2,'#111',None,'#dfe1e4'); rc(X(0),Z(12),K*140,K*12,1,0,'#555',None,'#9e9e9e')
for r in range(6):
    for c in range(2):
        x0=2+c*60+ (0 if c==0 else 2); z0=60+r*20
        rc(X(x0),Z(z0+20),K*58,K*20,.9,1,'#666',None,'#eceef1' if r<5 else '#f6efe0')
        rc(X(x0+50),Z(z0+12),K*1.6,K*5,.8,1,'#444',None,'#444')                    # kol
        ci(X(x0+4),Z(z0+10),2,1,GRN,None,'#c8f0d8')                                  # LED
        tx(X(x0+29),Z(z0+8.5)+2,'%d' % (r*2+c+1),6,'middle','bold','#333')
tx(X(62),Z(183)+2,'sıra 6 = yedek / büyük sipariş (2 dolap tek kod)',4.4,'middle','',AMB)
# kiosk seridi
rc(X(122),Z(180),K*16,K*120,.8,1,'#333',None,'#f4f4f4')
rc(X(124),Z(155),K*12,K*22,1,1,'#111',None,DARK); tx(X(130),Z(144)+2,'10" ekran',3.8,'middle','','#fff')
rc(X(125),Z(128),K*10,K*7,.8,1,'#333',None,'#ddd'); tx(X(130),Z(124)+2,'PIN',3.8,'middle','bold')
rc(X(125),Z(118),K*10,K*6,.8,1,'#333',None,'#bbb'); tx(X(130),Z(114.5)+2,'QR',3.8,'middle','bold')
ci(X(130),Z(105),3,1,'#333',None,'#333'); tx(X(130),Z(99)+2,'kamera',3.4,'middle','','#555')
txr(X(130),Z(75),'KİOSK ŞERİDİ 20',4.6,'#333','bold')
rc(X(2),Z(60),K*136,K*48,.8,0,'#666',None,'#e3f2fb'); tx(X(70),Z(38)+2,'PANO 48: BEYİN PC · 12 kilit kontrol kartı · 12 V PSU · router · (UPS SERVICE'+AP+'te)',5,'middle','bold','#1a49b8')
tx(X(70),Z(5)+2,'plint 12',4.6,'middle','','#fff')
dim(X(0),Z(0)+12,X(140),Z(0)+12,'140 = 60 + 60 + kiosk 20',5.4)
para(XA+14,YA+470,'Dolaplar 6 sıra × 20 = 120 (z 60–180), pano 48 (z 12–60). Ergonomi: alt sıra z 60 (eğilmeden), üst sıra z 160–180 (uzanarak) → sıra 6 yedek. Kapak: sağ kol, sol menteşe, 12 V elektrikli kilit, yeşil LED "sizin dolabınız", açık-kaldı sensörü (30 sn → uyarı). Cam yok.',78,5.1,'#333')
# ================= B · DOLAP İÇİ =================
XB,YB,WB,HB = 390,90,330,560
rc(XB,YB,WB,HB,1.4,4,'#111',None,'#fff'); tx(XB+14,YB+22,'B · BİR DOLAP — plan 56 × 36 ve kesit (yükseklik 16)',10,'start','bold')
KB=3.2; bx=XB+40; by=YB+60+KB*36
PX=lambda x: bx+KB*x; PY=lambda y: by-KB*y     # y: müşteri (ön) 0 → robot (arka) 36
rc(PX(0),PY(36),KB*56,KB*36,1.3,1,'#111',None,'#f4f4f4')
rc(PX(21.5),PY(34.5),KB*BOX[0],KB*BOX[1],1.1,1,'#5a3d13',None,KRAFT); tx(PX(37.7),PY(18)+2,'PİDE KUTUSU 32×32',5.2,'middle','bold','#5a3d13'); tx(PX(37.7),PY(13)+2,'(3 üst üste = 13,2)',4.2,'middle','','#5a3d13')
ln(PX(20.5),PY(1),PX(20.5),PY(35),.8,'#999','3,2')
rc(PX(2),PY(31),KB*8.5,KB*27,1,4,BLU,None,'#dfe7fb'); tx(PX(6.2),PY(17)+2,'1 L',4.6,'middle','bold',BLU); tx(PX(6.2),PY(12)+2,'yatık',3.8,'middle','',BLU)
# tatli: on tarafta 2 kase 12x12 -> yukseklikte ayni katta olmuyor; plan: tatli iceceklerin ONUNDE degil, yanda: 20 genislik: sise 8,5 + tatli 12 = 20,5 -> 2. sise yerine tatli
rc(PX(10.5),PY(33),KB*9,KB*13,1,1,AMB,None,'#fde9c9'); tx(PX(15),PY(27)+2,'TATLI',4.4,'middle','bold',AMB); tx(PX(15),PY(23)+2,'12×12×6',3.6,'middle','',AMB)
rc(PX(10.5),PY(19),KB*9,KB*13,1,1,AMB,'3,2','none'); tx(PX(15),PY(12)+2,'tatlı 2 /',3.6,'middle','',AMB); tx(PX(15),PY(8.5)+2,'kutu içecek ×2',3.6,'middle','',AMB)
tx(PX(28),PY(-4),'MÜŞTERİ KAPISI (ön)',4.6,'middle','bold',GRY); tx(PX(28),PY(36)-21,'ROBOT KLAPESİ (arka)',4.6,'middle','bold',GRY)
dim(PX(0),PY(36)-12,PX(20.5),PY(36)-12,'20',4.6,0,GRY); dim(PX(20.5),PY(36)-12,PX(56),PY(36)-12,'35,5',4.6,0,GRY)
dim(PX(56)+12,PY(36),PX(56)+12,PY(0),'36',4.6,0,GRY)
# kesit (yandan): 3 kutu, on kapi, arka klape, yalitim, buhar delikleri
KS=3.2; sx=XB+40; sz=YB+400
SX=lambda y: sx+KS*y; SZ=lambda z: sz-KS*z
hatch(SX(-2),SZ(18),KS*40,KS*2,3,'#b08968','#f3e6d3'); hatch(SX(-2),SZ(0),KS*40,KS*2,3,'#b08968','#f3e6d3')
rc(SX(0),SZ(16),KS*36,KS*16,1.1,0,'#333',None,'#fff')
for i in range(3): rc(SX(1.6),SZ(4.4*(i+1)),KS*32.4,KS*4.4,1,0,'#5a3d13',None,KRAFT)
rc(SX(-2),SZ(17),KS*2,KS*18,1.2,1,'#333',None,'#cfd3d8'); tx(SX(-4),SZ(8)+2,'ön kapı',3.8,'end','','#333'); tx(SX(-4),SZ(4)+2,'12 V kilit',3.4,'end','','#333')
ln(SX(36),SZ(16),SX(30),SZ(9),1.4,GRN); ln(SX(36),SZ(16),SX(36),SZ(0),.8,GRN,'3,2'); ci(SX(36),SZ(16),1.6,1,GRN,None,GRN)
tx(SX(38),SZ(9)+2,'arka klape: üst menteşe,',3.6,'start','',GRN); tx(SX(38),SZ(5.5)+2,'içeri açılır, yay kapatır,',3.6,'start','',GRN); tx(SX(38),SZ(2)+2,'mıknatıs kilit (BEYİN)',3.6,'start','',GRN)
for yy in (24,28,32): ci(SX(yy),SZ(16.5),1,.6,'#555',None,'#fff')
tx(SX(28),SZ(20.5)+2,'buhar delikleri Ø8 ×3 (arka üst) — kabuk yumuşamasın',3.6,'middle','','#555')
tx(SX(18),SZ(0)+36,'PU yalıtım 20 mm alt/üst/yan · ısıtıcı YOK · 15 dk sıcak kalır',3.8,'middle','','#333')
dim(SX(0),SZ(0)+24,SX(36),SZ(0)+24,'36',4.6,0,GRY); dim(SX(36)+56,SZ(0),SX(36)+56,SZ(16),'16',4.6,0,GRY)
arr(SX(48),SZ(12),SX(38),SZ(12),BLU,1.1); tx(SX(49),SZ(12)+2,'robot',3.8,'start','',BLU)
para(XB+14,YB+492,'İçerik: 3 pide (13,2) + 1 L şişe yatık (Ø8,5×27) + tatlı 12×12×6 ×2 ya da 2 kutu içecek. %95 sipariş tek dolaba sığar; 4+ pide → 2 dolap, aynı kod ikisini açar. Kilitli ön kapı ile arka klape asla aynı anda açık olmaz (interlock).',76,5.1,'#333')
# ================= C · KAÇ DOLAP =================
XC,YC,WC,HC = 740,90,340,300
rc(XC,YC,WC,HC,1.4,4,'#111',None,'#fff'); tx(XC+14,YC+22,'C · KAÇ DOLAP LAZIM? — satıştan hesap',10,'start','bold')
rows=[('satış','%d–%d pide/gün' % PIDE_GUN),('sipariş','%s pide/sipariş → %d–%d sipariş/gün' % (f1(PIDE_SIP),SIP_GUN[0],SIP_GUN[1])),
      ('pik',('günün %%%d'+AP+'i 2 saatte → %d–%d sipariş/saat, tasarım %d') % (50,SIP_PIK[0],SIP_PIK[1],SIP_PIK_MAX)),
      ('bekleme','kutu hazır → alınma: ort. %d dk, max %d (ısıtıcı yok!)' % (DWELL_ORT,DWELL_MAX)),
      ('dolu (ort.)','%d/saat × %d/60 = %s dolap' % (SIP_PIK_MAX,DWELL_ORT,f1(DOLU_ORT))),
      ('dolu (%95)','Poisson(%s) → %d dolap' % (f1(DOLU_ORT),DOLU_95)),
      ('geç alan','+%d (45 dk üstü, gün sonu eleman boşaltır)' % GEC),
      ('GEREKEN','%d dolap' % N_GEREK),('TASARIM','%d dolap (2 × 6) — 150 pide/güne kadar yeter' % N_TASARIM)]
yy=YC+44
for a_,b_ in rows:
    bold = a_ in ('GEREKEN','TASARIM'); tx(XC+14,yy,a_,5.4,'start','bold',GRN if bold else '#111'); tx(XC+92,yy,b_,5.4,'start','bold' if bold else '',GRN if bold else '#333'); yy+=13.5
rows[2]=rows[2]
para(XC+14,yy+4,'Bekleme süresi asıl anahtar: BEYİN pişirmeyi müşterinin/kuryenin gelişine göre başlatır (app "yoldayım", platform "kurye atandı" sinyali) → kutu dolapta 12 dk bekler. 20 dk geçince SMS "soğuyor", 45 dk geçince sipariş "geç" listesine düşer.',68,5.1,'#333')
# düzeltme: pik satırı format
# ================= D · KOD AKIŞI =================
XD,YD,WD,HD = 1100,90,320,300
rc(XD,YD,WD,HD,1.4,4,'#111',None,'#fcfdff'); tx(XD+14,YD+22,'D · KOD KİMDEN GELİR? — 3 kanal, tek kural',10,'start','bold')
flow=[('KENDİ APP / QR sipariş',BLU,'müşteri telefonu bizde → SMS/WhatsApp: 4 haneli PIN + QR link. Kioskta PIN ya da QR.'),
      ('PLATFORM GEL-AL (Yemeksepeti · Getir · Trendyol Go)',AMB,'platform dolap kodu ÜRETMEZ, telefonu maskeler. Sipariş entegratörle (Adisyo / Menulux tipi) BEYİN'+AP+'e düşer, BEYİN dolap atar. Müşteri kioskta sipariş numarasının son 4 hanesini girer (uygulamasında görür).'),
      ('KURYE (platform kuryesi)',RED,'kurye uygulamasında sipariş numarası var, kod yok. Kioskta "kurye" → son 4 hane → dolap açılır. Kamera kaydeder. Yanlış 3 deneme → 2 dk kilit.')]
yy=YD+42
for t,c,s_ in flow:
    tx(XD+14,yy,t,5.8,'start','bold',c); yy=para(XD+14,yy+9,s_,64,5.1,'#333')+4
para(XD+14,yy+2,'Tek kural: kodu HER ZAMAN BEYİN üretir; platforma güvenmeyiz. Dolap numarası ekranda yanar + LED yeşil. Kapı 30 sn açık kalırsa uyarı, kapanınca IR sensör "boş" der → dolap serbest.',64,5.1,GRN,'bold')
# ================= E · ROBOT ADRESLEME =================
XE,YE,WE,HE = 740,410,340,240
rc(XE,YE,WE,HE,1.4,4,'#111',None,'#fff'); tx(XE+14,YE+22,'E · ROBOT NASIL ADRESLER? — kamera değil, tablo',10,'start','bold')
yy=para(XE+14,YE+42,'BEYİN'+AP+'de dolap tablosu: no · durum (boş / yükleniyor / dolu-bekliyor / geç) · sipariş · ön kapı sensörü · arka klape sensörü · IR "kutu var". Robot için her dolabın 12 sabit XYZ hedefi öğretilmiştir (ray x, kol y, yükseklik z) — TOPPING kapları gibi. Kamera gerekmez; IR sensör kutunun girdiğini doğrular.',70,5.2,'#333')
yy=para(XE+14,yy+3,'DİZİ: sipariş hazır → BEYİN en yakın boş dolabı seçer (alt sıralar önce) → arka mıknatıs kilit açılır → robot içecek/tatlıyı STORE'+AP+'dan getirip sol bölmeye koyar → pide kutusunu pençeyle iter, klape yayla kapanır → IR ✓ → kod aktif, SMS gider → müşteri açar, alır, kapatır → IR boş → dolap serbest. Pide dolapta en fazla 20 dk hedef.',70,5.2,'#333')
para(XE+14,yy+3,'Robot menzili: koridor 90, PICKUP karşı duvarda; robot rayı koridor ortasında → dolap arkasına 45 + 6 cm uzanır ✓ (en üst sıra z 180: kol menzili 130+ ✓).',70,5.1,GRY)
# ================= F · SATIN ALMA =================
XF,YF,WF,HF = 1100,410,320,240
rc(XF,YF,WF,HF,1.4,4,'#111',None,'#fff'); tx(XF+14,YF+22,'F · TÜRKİYE'+AP+'DE VAR MI? — kargo dolabı var, yemek dolabı yok',10,'start','bold')
yy=para(XF+14,YF+42,'TR: kargo/emanet dolabı yapanlar — pudo, Easy Point, Kargopark, Zelfbox, Emanetmatik, Fitekno (Kargodrop), kutu.tech. Hepsi tek taraflı (önden yükle önden al), ısı/buhar düşünülmemiş; kilit kartı + kiosk yazılımı özel yapılabiliyor.',64,5.1,'#333')
yy=para(XF+14,yy+3,'Yurt dışı yemek dolabı: Apex OrderHQ Array (modüler, pizza boyu bölme, pass-through), Hatco Minnow Pod (bölme 34,5×52,4×36,8, pass-through, QR/SMS; ısıtmalı seçenek), Minnow X.',64,5.1,'#333')
para(XF+14,yy+3,'ÖNERİ: kabini entegratör yapsın (paslanmaz + PU panel, 12 bölme, arka klapeler); elektronik hazır alınsın: 12 × 12 V elektrikli kilit + 16 kanallı kilit kontrol kartı (KR-CU16 tipi) + Android kiosk (10" ekran + PIN pad + 2D okuyucu) + IR sensörler. Tahmini 60–90 bin TL.',64,5.1,GRN,'bold')
# ================= G · SORULAR — CEVAPLAR =================
XG,YG,WG,HG = 40,670,1380,205
rc(XG,YG,WG,HG,1.4,4,'#111',None,'#fcfdff'); tx(XG+14,YG+22,'G · KEMAL'+AP+'İN SORULARI — CEVAPLAR',10,'start','bold')
QA=[('KAÇ DOLAP?','Sayı satıştan değil pik saatten ve bekleme süresinden çıkar: 20 sipariş/saat × 12 dk bekleme = ortalama 4 dolu; %95 güvenle 8; geç alanlar için +2 → 10 gerek, 12 yapıyoruz (2 sütun × 6 sıra). 150 pide/güne kadar büyümez.'),
    ('DOLAP BOYUTU?','İç 56 × 36 × 16. Sağda 3 pide kutusu üst üste (13,2), solda 20 cm bölme: 1 L şişe yatık + tatlı 12×12 ya da 2 kutu içecek. Yatık şişe yüksekliği 8,5, sorun yok. Kabin 140 × 60 × 197.'),
    ('ARKA KAPAK, ISITICI?','Arka kapak ŞART ama küçük: üst menteşeli yaylı klape, robot kutuyla iterek açar, kendiliğinden kapanır, mıknatıs kilit. Sebep: müşteri ön kapıdan makineye uzanamasın + ısı/hijyen. Isıtıcı yok, haklısın: 20 mm PU yalıtım + 15 dk içinde alınma kuralı yeter; 3 buhar deliği kabuğu korur.'),
    ('QR MI NUMARA MI? KURYEYE KOD GİDİYOR MU?','Platformlar (Yemeksepeti, Getir, Trendyol Go) dolap kodu üretmiyor, müşteri telefonunu da maskeliyor. Bu yüzden kodu BEYİN üretir: kendi app müşterisine SMS/QR; platform müşterisi ve kurye ise kioskta sipariş numarasının son 4 hanesini girer (ikisi de uygulamasında görür). Kamera + LED + 3 yanlışta kilit.'),
    ('TÜRKİYE'+AP+'DE SATAN VAR MI?','Kargo dolabı satan çok (pudo, Easy Point, Emanetmatik, Fitekno…), yemek için iki taraflı dolap yok. Yurt dışında Apex ve Hatco Minnow var, pahalı ve ithalat. Öneri: kabin bizim entegratörden, kilit kartı + kiosk hazır parçadan.'),
    ('ROBOT NASIL ADRESLER?','Kamera gerekmez. BEYİN hangi dolabın boş/dolu olduğunu sensörlerden bilir, robotun 12 sabit hedefi vardır (XYZ öğretilmiş). Robot "3 nolu dolaba git" komutunu alır; içerideki IR sensör kutunun girdiğini doğrular. Kap yerleştirmeyle aynı mantık.')]
col_x=(XG+14,XG+700); yy=[YG+42,YG+42]
for i,(q,a_) in enumerate(QA):
    c=i%2; tx(col_x[c],yy[c],q,6.2,'start','bold',RED if c==0 else BLU); yy[c]=para(col_x[c],yy[c]+9,a_,112,5.4,'#333')+3
tx(W-40,H-8,'AUTOKITCH · arastirma/6_PICKUP/pickup_dolap_teknik_v1 · 7 Eyl 2026',7,'end','',GRY)
o.append('</svg>'); svg=chr(10).join(o); xml.dom.minidom.parseString(svg.encode('utf-8'))
out=r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\6_PICKUP\pickup_dolap_teknik_v1.svg"
io.open(out,'w',encoding='utf-8').write(svg); print('ok | gerek %d, tasarim %d | pik %s' % (N_GEREK,N_TASARIM,SIP_PIK))
