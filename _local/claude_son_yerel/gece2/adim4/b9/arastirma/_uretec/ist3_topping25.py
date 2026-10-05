# -*- coding: utf-8 -*-
# TOPPING v25 — KAP TAŞIMA: TEK ÇÖZÜM (TOPPING katı · ALT rafı · STORE −18 katı): kap 14×68×24 altında 2 içi boş kızak (çatal cebi),
# kabinde 2 L raf, robot ucu = ÇATAL (forklift). Kap arkaya dayalı (ara mil yok). STORE −18: sol modül = klapeli kaset katı (çekmece yok), 4 kap.
import io, math, xml.dom.minidom
W, H = 1460, 965
o = []
AP = chr(39)
def esc(s): return str(s).replace('&','&amp;').replace('<','&lt;')
def ln(x1,y1,x2,y2,w=1,c='#111',d=None):
    o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%s"%s stroke-linecap="round"/>' % (x1,y1,x2,y2,c,w,(' stroke-dasharray="%s"'%d) if d else ''))
def rc(x,y,w,h,sw=1,r=0,c='#111',d=None,f='none'):
    o.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%s" fill="%s" stroke="%s" stroke-width="%s"%s/>' % (x,y,w,h,r,f,c,sw,(' stroke-dasharray="%s"'%d) if d else ''))
def ci(x,y,r,sw=1,c='#111',d=None,f='none'):
    o.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" stroke="%s" stroke-width="%s"%s/>' % (x,y,r,f,c,sw,(' stroke-dasharray="%s"'%d) if d else ''))
def tx(x,y,s,fs=9,anc='start',fw='',col='#111'):
    o.append('<text x="%.1f" y="%.1f" font-size="%s" text-anchor="%s" font-weight="%s" fill="%s" font-family="Segoe UI, Arial, sans-serif">%s</text>' % (x,y,fs,anc,fw or 'normal',col,esc(s)))
def poly(pts,sw=1,c='#111',f='none',d=None,op=1):
    o.append('<polygon points="%s" fill="%s" fill-opacity="%s" stroke="%s" stroke-width="%s"%s stroke-linejoin="round"/>' % (' '.join('%.1f,%.1f'%p for p in pts),f,op,c,sw,(' stroke-dasharray="%s"'%d) if d else ''))
def arr(x1,y1,x2,y2,c='#c0392b',w=1.3):
    ln(x1,y1,x2,y2,w,c); a=math.atan2(y2-y1,x2-x1)
    for s in (1,-1): ln(x2,y2,x2-7*math.cos(a-s*.42),y2-7*math.sin(a-s*.42),w,c)
def para(x,y,s,maxc,fs=5.9,col='#333',fw='',lh=None):
    lh = lh or fs*1.6; cur=''; lines=[]
    for wd in s.split(' '):
        if cur and len(cur)+1+len(wd) > maxc: lines.append(cur); cur=wd
        else: cur = (cur+' '+wd) if cur else wd
    if cur: lines.append(cur)
    for l in lines: tx(x,y,l,fs,'start',fw,col); y += lh
    return y
def f1(v): return ('%.1f' % v).replace('.',',')

GRN, RED, BLU, GRY, AMB, PUR = '#1d7a4f', '#c0392b', '#1a49b8', '#666', '#b7791f', '#6b4fa8'
PE, MAT, LIGHT, ICE, STEEL, RAIL = '#e8f0e8', '#e9dfa8', '#f7f6f2', '#e3f2fb', '#cfd8dc', '#9e9e9e'
TH, RT = 55.0, 3.8
WK, LK, HK, ET = 14.0, 68.0, 24.0, 0.6          # kap dış · PE 6 mm
Wi, Hi, Li = WK-2*ET, HK-2*ET, LK-2*ET
KZ_H, KZ_W, CEP_W, CEP_H = 2.0, 3.0, 2.0, 1.4     # kızak dış · cep
TIR_W, TIR_H, TIR_L = 1.6, 1.2, 50.0              # çatal tırnağı (lama 16×12) · boy
def profil_sim(Wi,Hi,n=12):
    xc=Wi/2; t=math.radians(TH)
    pxl,pz = xc-RT*math.sin(t), RT-RT*math.cos(t); rise = pz + pxl*math.tan(t)
    pts=[(0,Hi),(0,rise),(pxl,pz)]
    a0=math.atan2(pz-RT,pxl-xc); a_stop=-math.pi-a0
    for k in range(1,n+1):
        a=a0+(a_stop-a0)*k/n; pts.append((xc+RT*math.cos(a),RT+RT*math.sin(a)))
    pts+=[(Wi-pxl,pz),(Wi,rise),(Wi,Hi)]; return pts,rise
def alan(pts):
    s=0
    for i in range(len(pts)):
        x1,z1=pts[i]; x2,z2=pts[(i+1)%len(pts)]; s+=x1*z2-x2*z1
    return abs(s)/2
PROF,RISE = profil_sim(Wi,Hi); AREA=alan(PROF); VOL=AREA*Li/1000
# kütleler
PE_CM3 = 2*WK*HK*ET + 2*LK*(Hi-RISE)*ET + 2*LK*5.4*ET + math.pi*RT*LK*ET + 2*LK*(KZ_W*KZ_H-CEP_W*CEP_H)
KAP_PE = PE_CM3*0.94/1000; HELEZON, TARAK = 1.2, 0.5; KAP_BOS = KAP_PE+HELEZON+TARAK
CATAL = 2.0
DENS = {'KAŞAR':0.41,'KIYMA':0.60,'SUCUK':0.55,'KUŞBAŞI':0.60}
CAP = {k:VOL*v for k,v in DENS.items()}
GUNLUK = {'KAŞAR':4.5,'KIYMA':8.6/3,'SUCUK':8.4/7,'KUŞBAŞI':4.3/3}
DOLUM = {'KAŞAR':CAP['KAŞAR'],'KIYMA':8.6,'SUCUK':8.4,'KUŞBAŞI':4.3}
GUN = {k:DOLUM[k]/GUNLUK[k] for k in DOLUM}
KOL = {k:DOLUM[k]+KAP_BOS+CATAL for k in DOLUM}

o.append('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">' % (W,H,W,H))
rc(0,0,W,H,0,0,'none',None,'#fff')
tx(30,40,'AUTOKITCH — TOPPING v25 (5 Eyl 2026) — KAP TAŞIMA: TEK ÇÖZÜM · kap 14×68×24 kızaklı, arkaya dayalı (ara mil yok) · robot ÇATAL ile önden alır · STORE −18 sol modül = aynı kat (çekmece yok)',14,'start','bold')
tx(30,62,'Dört soru → dört cevap: ① robot kabı forklift gibi ÇATALLA alır (tutamak, kanca, kilit yok) · ② kap arka duvara dayalı, ara mil ve ön boşluk yok · ③ donmuş kaplar yalnız STORE sol modülünde (4 × 14 yan yana) · ④ TOPPING katı, ALT rafı ve STORE −18 katı: aynı kızak + aynı L raf + aynı çatal, hepsi ÖNDEN.',9,'start','','#444')
ln(30,74,W-30,74,.8,'#999')

# ================= A · ÇATAL + CEPLİ KIZAK =================
XA,YA,WA,HA = 40,92,560,558
rc(XA,YA,WA,HA,1.4,4,'#111',None,'#fcfdff')
tx(XA+14,YA+22,'A · ROBOT KABI NASIL ALIR, NASIL TAŞIR — ÇATAL (robot ucu) + kabın altındaki CEPLİ KIZAKLAR',10,'start','bold')
# --- A1: kap ön kesit, kızaklar, L raflar, tırnaklar (K=6 px/cm)
K=6.0; ax,az = 72, 150+K*Hi
X=lambda c: ax+K*c; Z=lambda c: az-K*c
rc(X(-ET),Z(Hi+ET),K*(Wi+2*ET),K*(Hi+2*ET),1.2,1,'#111',None,PE)
poly([(X(x),Z(z)) for (x,z) in PROF],1.2,'#111','#fff'); poly([(X(x),Z(min(z,19))) for (x,z) in PROF],0,'none',MAT)
ci(X(Wi/2),Z(RT),K*3.5,1.1,GRN,None,'#fff'); ci(X(Wi/2),Z(12),K*4.5,.9,PUR,'3,2','none')
xc=Wi/2
for sx_ in (xc-4, xc+4):
    rc(X(sx_-KZ_W/2),Z(-ET),K*KZ_W,K*KZ_H,1.1,0,'#111',None,'#d0d7de')                       # kızak
    rc(X(sx_-CEP_W/2),Z(-ET-0.3),K*CEP_W,K*CEP_H,.8,0,'#555',None,'#fff')                     # cep
    rc(X(sx_-TIR_W/2),Z(-ET-0.3-CEP_H+TIR_H),K*TIR_W,K*TIR_H,1.1,0,GRN,None,'#bfe3cc')        # tırnak
    out = -1 if sx_ < xc else 1
    rc(X(sx_-KZ_W/2-0.5),Z(-ET-KZ_H)-K*0.2,K*(KZ_W+1.0),K*0.2,.8,0,'#555',None,RAIL)            # L raf yatay
    xo = sx_-KZ_W/2-0.5 if out<0 else sx_+KZ_W/2+0.3
    rc(X(xo),Z(-ET-KZ_H+0.8)-K*0.2,K*0.2,K*1.0,.8,0,'#555',None,RAIL)                          # L raf dik kenar (dışta)
ln(X(0),Z(Hi+ET+1.2),X(Wi),Z(Hi+ET+1.2),.7); tx(X(xc),Z(Hi+ET+2.2),'14',5.6,'middle','bold')
ln(X(Wi+ET+1.0),Z(Hi+ET),X(Wi+ET+1.0),Z(-ET),.7); tx(X(Wi+ET+1.6),Z(Hi/2),'24',5.6,'start','bold')
tx(X(xc),Z(-ET-KZ_H-1.6),'ÖN KESİT (kap yerinde)',5.4,'middle','',GRY)
KB=14.0; bx,bz = 118, 382
XB_=lambda c: bx+KB*c; ZB_=lambda c: bz-KB*c
rc(XB_(-2.6),ZB_(2.6),KB*8.4,KB*2.6+KB*1.2,.8,2,'#bbb',None,'#fff')
rc(XB_(-0.4),ZB_(2.6),KB*0.8,KB*0.6,.8,0,'#111',None,PE)   # kap tabanı (PE)
rc(XB_(-KZ_W/2),ZB_(KZ_H),KB*KZ_W,KB*KZ_H,1.1,0,'#111',None,'#d0d7de')
rc(XB_(-CEP_W/2),ZB_(KZ_H-0.3),KB*CEP_W,KB*CEP_H,.8,0,'#555',None,'#fff')
rc(XB_(-TIR_W/2),ZB_(KZ_H-0.3-CEP_H+TIR_H),KB*TIR_W,KB*TIR_H,1.1,0,GRN,None,'#bfe3cc')
rc(XB_(-KZ_W/2-0.5),ZB_(0),KB*(KZ_W+1.0),KB*0.2,.8,0,'#555',None,RAIL); rc(XB_(-KZ_W/2-0.5),ZB_(1.0),KB*0.2,KB*1.0,.8,0,'#555',None,RAIL)
tx(XB_(2.9),ZB_(2.2),'kızak 3,0 × 2,0',4.4,'start','','#333'); tx(XB_(2.9),ZB_(1.6),'cep 2,0 × 1,4',4.4,'start','','#333'); tx(XB_(2.9),ZB_(1.0),'tırnak 16 × 12 mm',4.4,'start','bold',GRN); tx(XB_(2.9),ZB_(0.4),'L raf 20 × 8 × 2',4.4,'start','','#333'); tx(XB_(2.9),ZB_(-0.2),'(dik kenar dışta)',4.2,'start','',GRY)
tx(XB_(0),ZB_(3.0),'DETAY ×2,3 — sol kızak',4.6,'middle','bold',GRY)
ln(X(xc-4)+8,Z(-ET-KZ_H/2),XB_(-2.6)-2,ZB_(1.2),.6,'#999','2,2')
lx, ly = 172, 156
ly = para(lx,ly,'KAP 14 × 68 × 24 · %s L · PE 6 mm · boş ≈ %s kg' % (f1(VOL),f1(KAP_BOS)),60,6.2,'#111','bold')
ly = para(lx,ly,'simetrik kama huni 55° · U oluk R 3,8 · helezon Ø70 (yeşil) · tarak Ø90 (mor)',60,5.6)
ly = para(lx,ly+2,'ALTTA 2 İÇİ BOŞ KIZAK 3,0 × 2,0 · cep 2,0 × 1,4 · merkez ±4 (aralık 8) — kalıpta gövdeyle tek parça',60,5.6,'#111','bold')
ly = para(lx,ly,'KABİNDE 2 L RAF (paslanmaz L 20×8×2 mm): kap kızaklarıyla üstünde kayar; dik kenar dışta = yan kılavuz; rafta hareketli parça yok',60,5.6)
ly = para(lx,ly,'ÇATAL TIRNAĞI (yeşil): lama 16×12 mm, 50 cm — cebin içinde; kaldırınca cep tavanı tırnağa oturur',60,5.6,GRN,'bold')
ly = para(lx,ly,'Ağız kabın ön ucunda, kızakların ARASINDA (aralık 5 > ağız Ø3,5) → altı açık, tepsi altına girer',60,5.6)
ly = para(lx,ly,'Kat 27 = kap 24 + kızak 2 + raf 0,2 + pay 0,8 (kaldırma 0,5) → v23 kat ölçüsü aynı',60,5.6)
ly = para(lx,ly+2,'v24 kabı 16×54 → 14×68: aynı iç geometri, hacim 14,8 → %s L' % f1(VOL),60,5.6,BLU,'bold')
# --- A2: çatal ucu (üstten + yandan)
tX = 362
tx(tX+112,YA+50,'ÇATAL UCU (robot pençesi)',6.8,'middle','bold')
KT=1.5; fy=YA+96
ci(tX+14,fy,6,1.1,'#333',None,'#eee'); tx(tX+14,fy-9,'flanş',4.6,'middle','',GRY)
rc(tX+22,fy-12,3,24,1.2,0,'#333',None,'#bbb'); tx(tX+23,fy-15,'sırt 16',4.6,'middle','',GRY)
for dy in (-6,6): rc(tX+25,fy+dy-1.2,KT*TIR_L,2.4,1,0,GRN,None,'#bfe3cc')
ln(tX+25,fy+16,tX+25+KT*TIR_L,fy+16,.7,RED); tx(tX+25+KT*TIR_L/2,fy+22,'tırnak 50',5,'middle','bold',RED)
ln(tX+25+KT*TIR_L+6,fy-6,tX+25+KT*TIR_L+6,fy+6,.7,RED); tx(tX+25+KT*TIR_L+9,fy+2,'8',5,'start','bold',RED)
tx(tX-4,fy+2,'üstten',4.8,'end','',GRY)
sy=YA+160
ci(tX+14,sy-8,6,1.1,'#333',None,'#eee'); rc(tX+22,sy-16,3,16,1.2,0,'#333',None,'#bbb'); tx(tX+23,sy-19,'sırt 10',4.6,'middle','',GRY)
rc(tX+25,sy-2.4,KT*TIR_L,2.4,1,0,GRN,None,'#bfe3cc')
tx(tX-4,sy-4,'yandan',4.8,'end','',GRY)
ly2 = sy+16
ly2 = para(tX-2,ly2,'2 tırnak (lama 16×12) + sırt plakası + flanş ISO 9409: ≈ 2,0 kg · hareketli parça yok, açma-kapama yok',48,5.4,'#333')
ly2 = para(tX-2,ly2,'Taşıma = forklift: kabı kaldırır, sürtünme + sırt tutar; 5° arkaya yatık taşınır → kap sırta yaslanır, kayamaz',48,5.4,GRN,'bold')
ly2 = para(tX-2,ly2,'Kabı 1 uç, hamur/tepsi 1 uç: uç değiştiricide durur (haftada ~10 kap değişimi, gece)',48,5.4,'#333')
# --- A3: dizi (3 hücre, yandan)
sq = YA+312
tx(XA+14,sq,'ALMA DİZİSİ (yandan, kat 1) — 1 gir · 2 kaldır · 3 çek — koyma tersi',6.8,'start','bold')
KY=0.8
def cell(x0,y0,step):
    xw = x0+165; kh = 27*KY
    rc(xw,y0-kh-6,8,kh+12,1,0,'#555',None,'#ccc'); tx(xw+4,y0-kh-9,'arka',4,'middle','',GRY)
    xf = xw-80*KY
    ln(xf,y0,xw,y0,1.6,'#555'); tx(xf+2,y0+6,'L raf',4,'start','',GRY)
    ln(xf,y0-kh,xw,y0-kh,.7,'#999','3,2')
    rc(xf-4,y0-kh-12,3,12,.8,0,BLU,None,'#dfe7fb'); tx(xf-3,y0-kh-14,'klape açık',4,'middle','',BLU)
    dx_ = 70*KY if step==3 else 0; dz = 3 if step>=2 else 0
    kx = xw-LK*KY-dx_
    rc(kx,y0-KZ_H*KY-dz,LK*KY,KZ_H*KY,.8,0,'#111',None,'#d0d7de')
    rc(kx,y0-KZ_H*KY-HK*KY-dz,LK*KY,HK*KY,1,1,'#111',None,PE); tx(kx+LK*KY/2,y0-KZ_H*KY-HK*KY/2-dz+2,'KAP 68',4.8,'middle','bold')
    ty = y0-KZ_H*KY/2-dz
    ln(kx,ty,kx+TIR_L*KY,ty,2,GRN)
    rc(kx-3,ty-8,3,10,1,0,'#333',None,'#bbb'); ci(kx-8,ty-3,3.5,1,'#333',None,'#eee'); ln(kx-11,ty-3,x0+4,ty-3,3,'#999')
    tx(x0+8,ty-8,'robot kolu',4,'start','',GRY)
    if step==1: arr(kx-40,ty-18,kx-8,ty-18,AMB,1.2); tx(kx-24,ty-22,'50 cm gir',4.6,'middle','bold',AMB)
    if step==2: arr(kx-30,ty-4,kx-30,ty-16,AMB,1.2); tx(kx-34,ty-18,'0,5 kaldır (abartılı)',4.6,'end','bold',AMB)
    if step==3: arr(kx+30,ty-24,kx-10,ty-24,AMB,1.2); tx(kx+10,ty-28,'70 cm düz geri çek',4.6,'middle','bold',AMB)
for j,(cap) in enumerate(('1 · GİR: klape açılır, tırnaklar kızak ceplerine 50 cm girer (hizalama: kamera + konum pimi)','2 · KALDIR 0,5: kap L raftan ayrılır, ağırlık cep tavanından tırnaklara geçer','3 · ÇEK 70: kap çatalın üstünde dışarı; 5° yatık taşı → koyma: sür, arkaya dayat, 0,5 indir, tırnakları çek')):
    x0 = XA+14+j*182; y0 = sq+58
    cell(x0,y0,j+1)
    para(x0,y0+14,cap,44,4.9,'#333')
# --- A4: metin
ty_ = YA+420
ty_ = para(XA+14,ty_,'PENÇE = ÇATAL. Kabın altında 2 içi boş kızak, robotun ucunda 2 tırnak + sırt. Forklift mantığı: tutma kuvveti yok, tutamak yok, kanca yok, kilit yok; 12–15 kg'+AP+'lık 68 cm'+AP+'lik kabı iki parmakla önden kavramak (moment ≈ 45 N·m) yerine yük tırnak boyunca dağılır.',165,5.7,'#111','bold')
ty_ = para(XA+14,ty_+1,'TOPPING'+AP+'de kap arka duvara dayanır: helezon milinin kare ucu duvardaki yaylı sokete eksenel girer (ara mil yok, üstten görünümdeki boşluk yok). ALT ve STORE'+AP+'da arkada yalnız dayama. Kabin tarafında raftan başka bir şey yok → kap yıkanır, raf silinir.',165,5.7)
ty_ = para(XA+14,ty_+1,'Aynı üç parça her yerde: kızaklı kap + L raf çifti + çatal → TOPPING 6 kat pozisyonu · ALT 8 raf · STORE −18 4 raf = 18 raf, tek hareket dizisi, tek kalibrasyon. Eleman da kabı aynı raflara elle iter.',165,5.7,GRN,'bold')
ty_ = para(XA+14,ty_+1,'Açık: kat 1 kızağı z 170 + 50 cm derin → kol menzili / base yüksekliği kontrol · tırnak-cep hizası (pim + kamera) · −18'+AP+'de raf-kızak buzlanması (ısıtıcı şerit 3 W ya da PE raf)',165,5.7,AMB)

# ================= B · PLAN KAT 1 =================
XB,YB,WB = 620,92,300
rc(XB,YB,WB,HA,1.4,4,'#111',None,'#fcfbf8')
tx(XB+14,YB+22,'B · PLAN (kat 1) — kap arkaya dayalı, ara mil yok',10,'start','bold')
KU=2.3; px_,py_ = XB+40, YB+52
tx(px_+KU*35,py_-6,'arka duvar 10: 6 motor + elektrik panosu',5,'middle','','#333')
rc(px_,py_,KU*70,KU*84,1.4)
rc(px_,py_,KU*70,KU*10,.9,0,'#555',None,'#d9d9d9')
for (x0,nm) in ((20,'KAŞAR A'),(36,'SUCUK')):
    rc(px_+KU*x0,py_+KU*10,KU*14,KU*68,1.2,1,'#111',None,PE)
    for dx in (3,11): ln(px_+KU*(x0+dx),py_+KU*11,px_+KU*(x0+dx),py_+KU*77,.8,'#555','3,2')
    ln(px_+KU*(x0+7),py_+KU*12,px_+KU*(x0+7),py_+KU*76,1.4,GRN)
    ci(px_+KU*(x0+7),py_+KU*76,2.6,1.3,GRN,None,'#fff'); ci(px_+KU*(x0+7),py_+KU*76,KU*27,.8,GRN,'4,3')
    rc(px_+KU*(x0+5),py_+KU*5,KU*4,KU*5,1,1,BLU,None,'#dfe7fb'); tx(px_+KU*(x0+7),py_+KU*3.5,'soket',3.8,'middle','',BLU)
    tx(px_+KU*(x0+7),py_+KU*40,nm,5.4,'middle','bold'); tx(px_+KU*(x0+7),py_+KU*46,'14×68',4.6,'middle','','#333')
rc(px_,py_+KU*80,KU*70,KU*4,1,0,BLU,None,'#dfe7fb'); tx(px_+KU*35,py_+KU*83,'klape 4',4.2,'middle','',BLU)
tx(px_+KU*10,py_+KU*40,'sol kanal 20',4.4,'middle','',GRY); tx(px_+KU*10,py_+KU*45,'evaporatör',4.2,'middle','',GRY); tx(px_+KU*10,py_+KU*50,'+ fan',4.2,'middle','',GRY)
tx(px_+KU*60,py_+KU*40,'sağ kanal 20',4.4,'middle','',GRY); tx(px_+KU*60,py_+KU*45,'hava dönüş',4.2,'middle','',GRY); tx(px_+KU*60,py_+KU*50,'+ kablo',4.2,'middle','',GRY)
tx(px_+KU*27,py_+KU*81.5,'x 27',3.6,'middle','bold',GRN); tx(px_+KU*43,py_+KU*81.5,'x 43',3.6,'middle','bold',GRN)
tx(px_+KU*35,py_+KU*84+70,'70 · derinlik 10 + 68 + 2 + 4 = 84 ✓ · ön boşluk yok',5.6,'middle','bold',GRN)
by = py_+KU*84+88
for s,c,fw in [('Kap 68 uzun → arka duvara dayanır (y 10–78), pay 2 (soket), klape 80–84. v24'+AP+'teki 16 cm ara mil ve öndeki boşluk kalktı.','#333',''),
               ('Ağız kabın ön ucunda y 76 ≥ 31 ✓ · süpürme R 27: y 49–103 (ön açık) ✓ · bant: kap merkezleri 27 / 43 ✓ (tepsi Ø32 + spiral R 11)',GRN,'bold'),
               ('Kesikli çizgiler = kabın altındaki 2 cep (çatal buraya girer); altında kabinin L rafları.',GRY,''),
               ('Yanlarda 20 cm: sol kanal evaporatör + fan (üfleme katlara), sağ kanal hava dönüşü + kablo. Arka duvar yalnız motor + pano.','#333',''),
               ('Kat 2 / kat 3 aynı plan (kaşar B + boş / kıyma + kuşbaşı). Her katın önünde ayrı klape 4.','#333',''),
               ('Kap 16→14 en: STORE sol modüle 4 kap yan yana sığar. Kap 54→68 boy: çekmece derinlik sınırı (59,5) kalktı, kat 70.',BLU,'bold'),
               ('Hacim %s L: kaşar %s kg (%s gün; iki pozisyon %s gün) · kıyma 3 gün 8,6 (%%%d) · sucuk hafta 8,4 (%%%d) · kuşbaşı 3 gün 4,3' % (f1(VOL),f1(CAP['KAŞAR']),f1(GUN['KAŞAR']),f1(2*GUN['KAŞAR']),8.6/CAP['KIYMA']*100,8.4/CAP['SUCUK']*100),'#333','')]:
    by = para(XB+14,by,s,86,5.7,c,fw)+2

# ================= C · STORE −18 =================
XC,YC,WC = 940,92,480
rc(XC,YC,WC,HA,1.4,4,'#111',None,'#fcfdff')
tx(XC+14,YC+22,'C · STORE −18: SOL MODÜL = klapeli KASET KATI (çekmece yok) · 4 kap · sağ modül boş',10,'start','bold')
KS=3.2; mx,my = XC+30, YC+58
tx(mx+KS*30.5,my-6,'ÖN — klape açık · modül 61 × 29 (iç 59,5 × 27)',6,'middle','bold',GRY)
rc(mx,my,KS*61,KS*29,1.4,1,'#111',None,ICE)
for j in range(4):
    x0 = 0.75+j*15.0
    zb = 27+1-KZ_H            # kızak tabanı (iç taban y=my+KS*28)
    rc(mx+KS*x0,my+KS*(zb-HK),KS*WK,KS*HK,1.1,1,'#111',None,PE)
    poly([(mx+KS*(x0+ET+x),my+KS*(zb-ET-z)) for (x,z) in PROF],.8,'#111','#fff')
    for sx_ in (7-4,7+4):
        rc(mx+KS*(x0+sx_-KZ_W/2),my+KS*zb,KS*KZ_W,KS*KZ_H,.9,0,'#111',None,'#d0d7de')
        rc(mx+KS*(x0+sx_-CEP_W/2),my+KS*(zb+0.3),KS*CEP_W,KS*CEP_H,.6,0,'#555',None,'#fff')
        rc(mx+KS*(x0+sx_-KZ_W/2-0.5),my+KS*(zb+KZ_H),KS*(KZ_W+1),KS*0.25,.7,0,'#555',None,RAIL)
    tx(mx+KS*(x0+7),my+KS*11,['KIYMA','KIYMA','KUŞBAŞI','KUŞBAŞI'][j],4.8,'middle','bold'); tx(mx+KS*(x0+7),my+KS*15.5,'−18',4.2,'middle','','#333')
ln(mx,my+KS*29+9,mx+KS*61,my+KS*29+9,.7); tx(mx+KS*30.5,my+KS*29+18,'61 · 4 × 14 + 3 × 1 + 0,5 = 59,5 ✓',5.4,'middle','bold',GRN)
ln(mx+KS*61+8,my,mx+KS*61+8,my+KS*29,.7); tx(mx+KS*61+12,my+KS*13,'29 = kap 24 +',5,'start','bold',GRN); tx(mx+KS*61+12,my+KS*16,'kızak 2 + pay 3',5,'start','bold',GRN)
# dikey şerit (öneri: kaset katı üstte)
vx,vy,KV = XC+350, YC+40, 0.8
rc(vx,vy,KV*70,KV*185,1)
z=0
for (h,lab,col,fw) in ((2,'','#e9e4d6',''),(28,'soğutma 28','#f3f3f3',''),(6,'','#e9e4d6',''),(84,'+3 · 84','#fff',''),(8,'','#e9e4d6',''),(29,'KASET KATI 29','#dbeafe','bold'),(10,'hamur −18','#e3f2fb',''),(10,'hamur −18','#e3f2fb',''),(8,'','#e9e4d6','')):
    rc(vx,vy+KV*z,KV*70,KV*h,.5,0,'#111',None,col)
    if lab: tx(vx+KV*35,vy+KV*(z+h/2)+1.8,lab,4.2 if h>=28 else 3.8,'middle',fw,'#111')
    z+=h
tx(vx+KV*35,vy+KV*185+9,'STORE sol modül (dikey, öneri)',4.6,'middle','',GRY)
tx(vx+KV*35,vy+KV*185+17,'kaset katı z 28–57 · hamur 8–28',4.4,'middle','',GRY)
# yan kesit
sx2,sy2,KS2 = XC+30, YC+218, 2.0
tx(sx2+KS2*42,sy2-6,'YAN — kap arkaya dayalı, önde izole klape · robot sağdan',6,'middle','bold',GRY)
rc(sx2,sy2,KS2*84,KS2*29,1.2,1,'#111',None,ICE)
rc(sx2,sy2,KS2*8,KS2*29,.9,0,'#555',None,'#ccc'); tx(sx2+KS2*4,sy2+KS2*15,'PU 8',4,'middle','','#333')
fl = sy2+KS2*27.5
rc(sx2+KS2*8,fl-KS2*KZ_H,KS2*LK,KS2*KZ_H,.9,0,'#111',None,'#d0d7de')
rc(sx2+KS2*8,fl-KS2*(KZ_H+HK),KS2*LK,KS2*HK,1.1,1,'#111',None,PE); tx(sx2+KS2*42,fl-KS2*(KZ_H+HK/2)+2,'KAP 68 (arkaya dayalı) · pay 2',5.2,'middle','bold')
ln(sx2+KS2*8,fl,sx2+KS2*78,fl,1.4,'#555')
rc(sx2+KS2*78,sy2,KS2*6,KS2*29,1,0,BLU,None,'#dfe7fb'); tx(sx2+KS2*81,sy2+KS2*29+8,'klape 6',4.4,'middle','',BLU)
arr(sx2+KS2*112,fl-KS2*1,sx2+KS2*86,fl-KS2*1,GRN,1.3); tx(sx2+KS2*114,fl-KS2*12,'çatal önden girer',5,'start','bold',GRN); tx(sx2+KS2*114,fl-KS2*8,'TOPPING'+AP+'le aynı hareket',4.6,'start','',GRN); tx(sx2+KS2*114,fl-KS2*4,'(klape motorlu açılır)',4.4,'start','',GRY)
tx(XC+14,sy2+KS2*29+20,'arka PU 8 + kap 68 + pay 2 + klape 6 = 84 ✓ · çekmece, teleskopik ray, çekmece motoru yok',5.4,'start','bold',GRY)
cy_ = YC+316
for s,c,fw in [('Sağ modül boş kalır: 4 kap (kıyma ×2 + kuşbaşı ×2) sol modülün 59,5 cm iç genişliğine yan yana sığıyor; sağdaki 29'+AP+'luk bant ileride 3. hamur çekmecesi ya da kavurma.',GRN,'bold'),
               ('Çekmece → klapeli kat: STORE v4'+AP+'ün −18 kaset çekmecesi (61 × 70 × 29, teleskopik ray + 24 V motor) yerine izole klape (6, motorlu) + 4 çift L raf. Tek hareketli parça: klape.','#333',''),
               ('Robot: klape açılır → çatal istediği kabı önden alır (4 kap da önde, hepsi erişilir) → TOPPING ALT çözülme rafına → 1 gün sonra kat 3'+AP+'e. TOPPING'+AP+'deki hareketin aynısı.','#333',''),
               ('Eleman haftada 1: 2 kıyma + 2 kuşbaşı donmuş kabı aynı kızaklarla iter (çekmece açma yok); boş kapları TOPPING ALT park rafından alır.','#333',''),
               ('Öneri: kaset katı −18 bandının ÜSTÜNE (z 28–57), hamur çekmeceleri altta (8–28) → çatal z 29'+AP+'da girer (v4'+AP+'te kaset çekmecesi z 8–37: kol için çok alçak). Buzlanma: L raf ısıtıcı şerit 3 W ya da PE raf.',AMB,''),
               ('STORE v5 = yalnız bu bant: sol −18 kaset çekmecesi → klapeli kat (4 raf), sağdaki boş; hamur çekmeceleri aşağı. Dikey 185, derinlik 84, en 140 aynı.',BLU,'bold')]:
    cy_ = para(XC+14,cy_,s,142,5.7,c,fw)+2

# ================= D · ALT =================
XD,YD,WD,HD = 40,670,560,270
rc(XD,YD,WD,HD,1.4,4)
tx(XD+14,YD+22,'D · TOPPING ALT 74 — beşik yerine aynı L raflar (2 sıra × 4) · soğutma grubu dipte · evaporatör sol yan kanalda',10,'start','bold')
KD=2.0; dx,dy = XD+30, YD+40
rc(dx,dy,KD*70,KD*74,1.2)
rc(dx,dy+KD*54,KD*70,KD*20,.9,0,'#555',None,STEEL); tx(dx+KD*35,dy+KD*63,'SOĞUTMA GRUBU 20 · 1/12 HP yatay',5,'middle','bold','#37474f'); tx(dx+KD*35,dy+KD*69,'plint ızgarası (hava önden)',4.4,'middle','','#37474f')
for row,(z0,labs) in enumerate(((0,('kaşar yd','kaşar yd','kaşar yd','kaşar yd')),(27,('park','park','çöz. kıyma','çöz. kuşbaşı')))):
    for j in range(4):
        x0 = 4.75+j*15.5; zb = z0+0.2+KZ_H
        dsh = row==1 and j<2
        rc(dx+KD*x0,dy+KD*(zb),KD*WK,KD*HK,1 if dsh else 1.1,1,'#999' if dsh else '#111','3,2' if dsh else None,LIGHT if dsh else PE)
        for sx_ in (7-4,7+4):
            rc(dx+KD*(x0+sx_-KZ_W/2),dy+KD*(z0+0.2),KD*KZ_W,KD*KZ_H,.7,0,'#888' if dsh else '#111',None,'#e6e9ec' if dsh else '#d0d7de')
        ln(dx+KD*x0,dy+KD*(z0+0.2),dx+KD*(x0+14),dy+KD*(z0+0.2),.9,'#555')
        tx(dx+KD*(x0+7),dy+KD*(zb+13),labs[j],4.4,'middle','bold','#888' if dsh else '#333')
tx(dx+KD*70+8,dy+KD*13,'sıra 1 (z 47–74): 4 kaşar yedeği (+3)',5.4,'start','','#333')
tx(dx+KD*70+8,dy+KD*40,'sıra 2 (z 20–47): park ×2 (boş kap) + çözülme ×2 (kıyma, kuşbaşı)',5.4,'start','','#333')
tx(dx+KD*70+8,dy+KD*49,'ALT önü: sıra başına 1 klape · kaplar 68 derin, arkaya dayalı (84 içinde)',5.4,'start','',GRY)
tx(dx+KD*70+8,dy+KD*62,'soğutma z 0–20: 1/12 HP (Embraco EM sınıfı ≤ 19 boy) yatay; hava ön plintten girer, arkadan çıkar',5.4,'start','','#333')
tx(dx+KD*70+8,dy+KD*69,'evaporatör + fan sol yan kanalda (x 0–20, kat bölgesi); ALT'+AP+'a yanlardan 4 cm hava kanalı',5.4,'start','','#333')
para(XD+14,YD+210,'Dikey: 3 × (27 + 14) = 123 · ALT 74 = 20 + 27 + 27 → 197 ✓ · kat 27 = kap 24 + kızak 2 + raf 0,2 + pay 0,8 · tepsi düzlemleri 158 / 117 / 76 değişmedi',165,5.8,GRN,'bold')
para(XD+14,YD+226,'Beşik yok: ALT rafları TOPPING katları ve STORE katıyla birebir aynı L profil (70 cm). Kabinde toplam 18 çift L raf, hiçbirinde hareketli parça yok.',165,5.8,'#333')
para(XD+14,YD+242,'Açık: soğutma grubu boyu ≤ 20 (kompresör seçimi) · ALT klape contası · plint hava yolu',165,5.8,AMB)

# ================= E · TABLO + KONTROL =================
XE,YE,WE = 620,670,800
rc(XE,YE,WE,HD,1.4,4)
tx(XE+14,YE+22,'E · KG · KOL YÜKÜ · DEĞİŞİM · KONTROL',10,'start','bold')
hdr=['malzeme','kap 14×68×24 (%s L)' % f1(VOL),'dolum','dolu kap','kol yükü (+çatal 2)','gün','değişim/hafta','yedek nerede']
cx_=[XE+14,XE+96,XE+206,XE+286,XE+356,XE+446,XE+496,XE+574]
for i,h in enumerate(hdr): tx(cx_[i],YE+42,h,5.9,'start','bold',GRY)
ln(XE+12,YE+47,XE+WE-12,YE+47,.8,'#bbb')
rows=[('KAŞAR rende','%s kg (0,41 kg/L)' % f1(CAP['KAŞAR']),'%s kg (tam)' % f1(DOLUM['KAŞAR']),f1(DOLUM['KAŞAR']+KAP_BOS),f1(KOL['KAŞAR']),'%s (2 poz. %s)' % (f1(GUN['KAŞAR']),f1(2*GUN['KAŞAR'])),'4–5','ALT sıra 1 (+3)'),
      ('KIYMA kavrulmuş','%s kg (0,60)' % f1(CAP['KIYMA']),'8,6 kg (3 gün)',f1(DOLUM['KIYMA']+KAP_BOS),f1(KOL['KIYMA']),'3','2','STORE −18 sol → ALT çözülme'),
      ('SUCUK küp','%s kg (0,55)' % f1(CAP['SUCUK']),'8,4 kg (hafta)',f1(DOLUM['SUCUK']+KAP_BOS),f1(KOL['SUCUK']),'7','1','eleman getirir'),
      ('KUŞBAŞI sote','%s kg (0,60)' % f1(CAP['KUŞBAŞI']),'4,3 kg (3 gün)',f1(DOLUM['KUŞBAŞI']+KAP_BOS),f1(KOL['KUŞBAŞI']),'3','2','STORE −18 sol → ALT çözülme')]
for i,r in enumerate(rows):
    yy=YE+62+i*15
    for j,v in enumerate(r): tx(cx_[j],yy,v,5.9,'start','bold' if j==0 else '','#111' if j==0 else ('#c0392b' if (j==4 and float(v.replace(',','.'))>12.5) else '#333'))
ln(XE+12,YE+124,XE+WE-12,YE+124,.8,'#bbb')
ey = YE+140
for s,c,fw in [(('KOL YÜKÜ ⑦ YENİDEN AÇIK: kap boş ≈ %s kg (PE 6 mm %s + helezon 1,2 + tarak 0,5) + çatal 2,0 → kıyma %s kg, sucuk %s, kaşar %s → 12,5 kg kobot YETMEZ → 16–20 kg sınıfı (UR16e · Fanuc CRX-20iA/L · Doosan H2017 · TM20) — ya da kıyma/sucuk dolumu 6 kg (2 gün) ile 12,5'+AP+'te kalınır (haftada +3 değişim).') % (f1(KAP_BOS),f1(KAP_PE),f1(KOL['KIYMA']),f1(KOL['SUCUK']),f1(KOL['KAŞAR'])),RED,'bold'),
               ('Değişim dizisi (kaşar A boşaldı, ~90 sn): kat 1 klape aç → çatal gir / kaldır / çek → ALT park rafına koy → ALT sıra 1'+AP+'den dolu kaşar al → kat 1'+AP+'e sür (soket kavrar) → klapeler kapan.','#333',''),
               ('Haftalık: robot 4–5 kaşar + 2 kıyma + 2 kuşbaşı + 1 sucuk = 9–10 değişim + STORE→ALT 4 taşıma (gece). Eleman haftada 1: 5 kaşar + 1 sucuk (ALT / kat), 2 + 2 donmuş (STORE sol kat), 10 boş kap alır.','#333',''),
               ('KONTROL ① ağız y 76 ≥ 31 ✓ · bant 27 / 43 ✓ · ② kap her yerde önde, önü boş (18 raf, 1 çatal) ✓ · ③ ara mil yok, ön boşluk yok ✓ · ④ 197 ✓ · 84 ✓ · ⑤ STORE sol 4 kap ✓ (59,5), sağ boş · ⑥ STORE derinlik 70 ≥ 68 + 2 ✓ · ⑦ kol yükü AÇIK (üstte)',GRN,'bold'),
               ('AÇIK: ⑦ kobot sınıfı · çatal uç değiştirici · kat 1 kızağı z 170 kol menzili · −18 raf buzlanması · klape contası (TOPPING 3 + ALT 2 + STORE 1) · soğutma grubu ≤ 20 boy · robot_tepsi_el v2 (Ø32) · helezon soketi (kare uç, yaylı) prototip',AMB,''),
               ('v24 → v25: kap 16×54 → 14×68 · beşik → L raf · ara mil iptal, kap arkaya dayalı · STORE −18 çekmece → klapeli kat (sol modül, 4 kap) · soğutma grubu ALT dibine, evaporatör sol yan kanala · pençe = çatal · ⑦ yeniden açık',BLU,'bold')]:
    ey = para(XE+14,ey,s,240,5.8,c,fw)+2
tx(W-40,H-10,'AUTOKITCH · arastirma/3_TOPPING/ist3_topping_detay_v25 · 5 Eyl 2026',7,'end','',GRY)
o.append('</svg>')
svg = chr(10).join(o)
xml.dom.minidom.parseString(svg.encode('utf-8'))
out = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\3_TOPPING\ist3_topping_detay_v25.svg"
io.open(out,'w',encoding='utf-8').write(svg)
print('yazildi + XML gecerli | alan %.0f cm2 -> %.1f L · kap PE %.2f kg bos %.2f · kasar %.1f (%.2f gun) · kol: kiyma %.1f sucuk %.1f kasar %.1f kusbasi %.1f' % (AREA,VOL,KAP_PE,KAP_BOS,CAP['KAŞAR'],GUN['KAŞAR'],KOL['KIYMA'],KOL['SUCUK'],KOL['KAŞAR'],KOL['KUŞBAŞI']))
