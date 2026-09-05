# -*- coding: utf-8 -*-
# TOPPING — MÜKEMMEL KAP GEOMETRİSİ v1: literatüre göre (Jenike kama huni, EHEDG radyus, milsiz helezon, tarak) 4 malzeme için kap kesitleri
# Büyük kap (kaşar) 32,5×70×60 · Küçük kap (kıyma L / sucuk-kuşbaşı R, ayna) 20×49×24 · malzeme tablosu · hijyen kuralları · kurulum · kaynaklar
import io, math, xml.dom.minidom
W, H = 1460, 1190
o = []
def esc(s): return str(s).replace('&','&amp;').replace('<','&lt;')
def ln(x1,y1,x2,y2,w=1,c='#111',d=None):
    o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%s"%s stroke-linecap="round"/>' % (x1,y1,x2,y2,c,w,(' stroke-dasharray="%s"'%d) if d else ''))
def rc(x,y,w,h,sw=1,r=0,c='#111',d=None,f='none'):
    o.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%s" fill="%s" stroke="%s" stroke-width="%s"%s/>' % (x,y,w,h,r,f,c,sw,(' stroke-dasharray="%s"'%d) if d else ''))
def ci(x,y,r,sw=1,c='#111',d=None,f='none'):
    o.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" stroke="%s" stroke-width="%s"%s/>' % (x,y,r,f,c,sw,(' stroke-dasharray="%s"'%d) if d else ''))
def tx(x,y,s,fs=9,anc='start',fw='',col='#111'):
    o.append('<text x="%.1f" y="%.1f" font-size="%s" text-anchor="%s" font-weight="%s" fill="%s" font-family="Segoe UI, Arial, sans-serif">%s</text>' % (x,y,fs,anc,fw or 'normal',col,esc(s)))
def path(d,sw=1,c='#111',f='none',dash=None):
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="%s"%s stroke-linejoin="round"/>' % (d,f,c,sw,(' stroke-dasharray="%s"'%dash) if dash else ''))
def poly(pts,sw=1,c='#111',f='none',d=None):
    o.append('<polygon points="%s" fill="%s" stroke="%s" stroke-width="%s"%s/>' % (' '.join('%.1f,%.1f'%p for p in pts),f,c,sw,(' stroke-dasharray="%s"'%d) if d else ''))
def arr(x1,y1,x2,y2,c='#c0392b',w=1.1):
    ln(x1,y1,x2,y2,w,c); a=math.atan2(y2-y1,x2-x1)
    for s in (1,-1): ln(x2,y2,x2-6*math.cos(a-s*.42),y2-6*math.sin(a-s*.42),w,c)
def callout(x,y,tx_,ty_,s,col='#333',fs=5.6,fw=''):
    ln(x,y,tx_,ty_,.7,col); ci(x,y,1.6,0,'none',None,col); tx(tx_+(3 if tx_>=x else -3),ty_+2,s,fs,'start' if tx_>=x else 'end',fw,col)

GRN, RED, BLU, GRY, AMB, PUR = '#1d7a4f', '#c0392b', '#1a49b8', '#666', '#b7791f', '#6b4fa8'
PE, MAT, STEEL = '#e8f0e8', '#e9dfa8', '#d9d9d9'
TH = 55.0            # eğimli duvar açısı (yataydan)
RT = 3.8             # oluk yarıçapı (helezon Ø70 + 3 mm boşluk)
def profil(Wi,Hi,mirror=False,n=24):
    # iç profil (x: 0 dış duvar → Wi iç duvar; z: 0 oluk dibi): dış duvar dik → eğim 55° → U oluk → iç duvar dik
    xc = Wi-RT
    t = math.radians(TH)
    nx,nz = -math.sin(t), -math.cos(t)          # eğim çizgisine dik (sol-alt)
    px_,pz_ = xc+RT*nx, RT+RT*nz                # teğet noktası
    rise = pz_ + (px_-0)*math.tan(t)
    pts=[(0,Hi),(0,rise),(px_,pz_)]
    a0 = math.atan2(pz_-RT, px_-xc)             # teğet açısı (merkezden)
    a1 = 0.0                                    # sağ teğet (x = Wi, z = RT)
    for k in range(1,n+1):
        a = a0 + (a1+2*math.pi-a0)*k/n if a1<a0 else a0+(a1-a0)*k/n
        pts.append((xc+RT*math.cos(a), RT+RT*math.sin(a)))
    pts += [(Wi,RT),(Wi,Hi)]
    if mirror: pts=[(Wi-x,z) for (x,z) in pts]
    return pts, rise, xc
def alan(pts):
    s=0
    for i in range(len(pts)):
        x1,z1=pts[i]; x2,z2=pts[(i+1)%len(pts)]; s+=x1*z2-x2*z1
    return abs(s)/2
WB,HB,LB = 30.5,58.0,68.0      # kaşar iç ölçüler (dış 32,5 × 70 × 60, PE 10 mm)
WS,HS,LS = 18.4,22.4,52.4      # küçük iç ölçüler (dış 20 × 54 × 24, PE 8 mm)
pB,riseB,xcB = profil(WB,HB); aB = alan(pB); vB = aB*LB/1000
pS,riseS,xcS = profil(WS,HS); aS = alan(pS); vS = aS*LS/1000

o.append('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">' % (W,H,W,H))
rc(0,0,W,H,0,0,'none',None,'#fff')
tx(30,42,'AUTOKITCH — TOPPING · KAP GEOMETRİSİ v1 (5 Eyl 2026) — 4 malzeme için "mükemmel" hazne: Jenike kama huni kuralı · EHEDG radyus · milsiz helezon · çift tarak · UHMW-PE · her kap = ürün = pozisyon (sol/sağ ayna)',15,'start','bold')
tx(30,66,'Sorun: kaşar rende yığın altında sıkışır, kekleşir, hunide kemer kurar; kavrulmuş kıyma yağ sıvar; sote küp ağızda kilitlenir. Cevap tek geometri değil, 6 kural: eğimli duvar 55°, U-oluk helezon ölçüsünde, iç köşe R ≥ 6, düşük sürtünmeli yüzey, yığın yüksekliği sınırı, oluk üstünde tarak. Sağ/sol kaplar ayna — kavrama mili kabın iç kenarında.',9.5,'start','','#444')
ln(30,78,W-30,78,.8,'#999')

# ================= A · KAŞAR KABI ÖN KESİT =================
XA,YA = 40,100
rc(XA,YA,470,560,1.4,4,'#111',None,'#fcfdff')
tx(XA+14,YA+22,'A · KAŞAR KABI — ÖN KESİT (iç 30,5 × 58 · dış 32,5 × 60 · PE 10 mm)',10,'start','bold')
K=4.2
ox,oz = XA+60, YA+60+K*HB
X=lambda c: ox+K*c; Zc=lambda c: oz-K*c
# dış kabuk (PE 10 mm) — iç profili 1 cm dışa taşı
outer=[(X(-1),Zc(HB+1)),(X(-1),Zc(-1)),(X(WB+1),Zc(-1)),(X(WB+1),Zc(HB+1))]
poly(outer,1.3,'#111',PE)
poly([(X(x),Zc(z)) for (x,z) in pB],1.3,'#111','#fff')
# malzeme (yığın ≤ 50)
matpts=[(x,min(z,50)) for (x,z) in pB]
poly([(X(x),Zc(z)) for (x,z) in matpts],0,'none',MAT)
# helezon (milsiz spiral) kesiti
ci(X(xcB),Zc(RT),K*3.5,1.1,'#333','#fff'); ci(X(xcB),Zc(RT),K*3.5-K*.6,.8,'#333','#eee')
ci(X(xcB),Zc(RT),K*RT,1,BLU,'3,2')
# taraklar
for (za,r,lab) in ((13,5.5,'T1 Ø11'),(36,8,'T2 Ø16')):
    ci(X(xcB-2),Zc(za),K*r,1,PUR,'4,3'); ci(X(xcB-2),Zc(za),K*.6,1.1,PUR,None,'#efeaf8')
    for a_ in (30,150,270):
        a=math.radians(a_); ln(X(xcB-2),Zc(za),X(xcB-2)+K*r*math.cos(a),Zc(za)-K*r*math.sin(a),1.3,PUR)
# kapak
rc(X(-1),Zc(HB+1)-K*1.2,K*(WB+2),K*1.2,1,1,'#111',None,'#cfd8dc')
# ölçüler
ln(X(0),Zc(-4),X(WB),Zc(-4),.7); tx(X(WB/2),Zc(-5.5),'30,5 iç · 32,5 dış',5.6,'middle','bold')
ln(X(WB+4),Zc(0),X(WB+4),Zc(HB),.7); tx(X(WB+5),Zc(HB/2),'58 iç',5.6,'start','bold'); tx(X(WB+5),Zc(HB/2-3),'60 dış',5.2,'start','',GRY)
ln(X(WB+4),Zc(0),X(WB+4),Zc(50),0); tx(X(WB+5),Zc(52),'yığın ≤ 50',5.4,'start','bold',AMB)
# callout'lar
callout(X(-0.5),Zc(riseB+8),X(-9),Zc(riseB+18),'dış duvar dik, üstte 8 cm',GRY)
callout(X(8),Zc(riseB-8*math.tan(math.radians(TH))),X(-9),Zc(riseB-2),'eğimli duvar 55° (yataydan)',AMB,5.8,'bold')
callout(X(4),Zc(riseB-4*math.tan(math.radians(TH))-3),X(-9),Zc(riseB-9),'Jenike: kama huni, PE için ≥ 50°',GRY)
callout(X(-0.3),Zc(riseB+0.5),X(-9),Zc(riseB+5),'köşe R 20 (iç açı 145°)',GRY)
callout(X(xcB-RT*.9),Zc(RT-RT*.4),X(-9),Zc(-2.5),'U-oluk R 38 = helezon 35 + 3 boşluk',BLU,5.8,'bold')
callout(X(xcB),Zc(RT),X(xcB+14),Zc(-9),'milsiz spiral Ø70 · h 35 · 30 dev/dk',BLU,5.8,'bold')
callout(X(WB-0.3),Zc(RT+2),X(WB+5),Zc(8),'iç duvar dik (bant!) · tarak kolu sıyırır',GRY)
callout(X(WB-0.3),Zc(30),X(WB+5),Zc(30),'köşe yok: U → duvar teğet',GRY)
callout(X(xcB-2),Zc(13),X(xcB+7),Zc(19),'T1: köprü kırıcı, oluk ağzında, 5 dev/dk',PUR,5.8,'bold')
callout(X(xcB-2),Zc(36),X(xcB+8),Zc(42),'T2: sıkışma önleyici + duvar sıyırıcı kol, 3 dev/dk',PUR,5.8,'bold')
callout(X(WB/2),Zc(HB+0.6),X(WB/2+6),Zc(HB+4.5),'kapak izole + conta (nem kaybı yok)',GRY)
callout(X(WB/2-8),Zc(45),X(WB/2-16),Zc(56),'yüzey: UHMW-PE (PE1000) Ra ≤ 0,8',GRN,5.8,'bold')
callout(X(WB/2+4),Zc(24),X(WB+5),Zc(20),'+2…+4 °C: yağ katı, yapışma az',GRN)
ny=YA+400
lines=[('kesit alanı %.0f cm² × iç boy 68 = %.0f L → kaşar %.0f kg (0,41) · yeni menüde kaşar ~4,5 kg/gün → %.1f gün ≥ hafta ✓' % (aB,vB,vB*0.41,vB*0.41/4.5),'#111','bold'),
       ('Neden 55° (45° değil): rende kaşar + PE duvar sürtünme açısı ~18-22°; kama hunide kütle akışı için duvar ≥ 50° ister (koniye göre 10-12° daha yatık yeter). 55° = pay.','#333',''),
       ('Neden milsiz spiral: lifli/yapışkan malzeme mile sarılır, tıkar; milsiz spiral mile sarılmayı ortadan kaldırır (KWS, Orthman uygulama kılavuzları) — oluğa PE astar, boşluk 3 mm.','#333',''),
       ('Neden iki tarak: kaşar kendi ağırlığında sıkışıp keke döner; T1 oluk ağzında kemeri kırar, T2 üst yığını gevşek tutar + iç dik duvarı sıyırır (patent: wiping arm + blending arm).','#333',''),
       ('Neden yığın ≤ 50: 60 cm kabın üst 8 cm boş; rendelenmiş peynir 50 cm sütunda bile katkılı (selüloz) olmalı — tedarikçiden "topaklanma önleyicili rende" istenir.','#333',''),
       ('Köşeler: EHEDG Doc 8 → iç açı ≤ 135° ise R ≥ 3 mm; biz gıda teması olan her yerde R ≥ 6, oluk-duvar geçişi teğet (köşe yok), uç duvarlar R 10. İçeride cıvata yok.','#333',''),
       ('Ağız: ön uçta 70 × 60, kenarlar R 10, kam açmalı sürgü (kap dışarıdayken kapalı). Kavrama: arka uçta kısa mil + pençe; kap raya oturunca eksenel kilitlenir.','#333','')]
for i,(s,c,fw) in enumerate(lines): tx(XA+14,ny+i*14,s,6,'start',fw,c)
tx(XA+14,ny+108,'Alternatif malzeme: 316L paslanmaz 1,5 mm elektro-parlatılmış (Ra 0,4) — daha ağır (3×), peynire PE'+chr(39)+'den daha çok yapışır; PE tercih.',5.6,'start','',GRY)
tx(XA+14,ny+121,'Prototipte ölçülecek: kaşar-PE duvar sürtünme açısı (Jenike hücresi), köprüleme çıkış genişliği, 50 cm yığında kekleşme (24 s bekleme testi).',5.6,'start','',AMB)
tx(XA+14,ny+134,'İç duvara 3-5° dışa eğim (köprü karşıtı) istenirdi ama bant kuralı (helezon x 30) buna izin vermiyor → yerine T2 sıyırıcı kol.',5.6,'start','',GRY)

# ================= B · KAŞAR YAN KESİT =================
XB,YB = 530,100
rc(XB,YB,400,270,1.3,3,'#999',None,'#fff')
tx(XB+200,YB+16,'B · KAŞAR KABI — YAN KESİT (arka ← y → ön)',7.5,'middle','bold')
KY=2.4
bx,bz = XB+40, YB+40+KY*HB
Yy=lambda c: bx+KY*c; Zy=lambda c: bz-KY*c
rc(Yy(-1),Zy(HB+1),KY*(LB+2),KY*(HB+2),1.2,1,'#111',None,PE)
rc(Yy(0),Zy(HB),KY*LB,KY*HB,1,0,'#111',None,'#fff')
rc(Yy(.2),Zy(50),KY*(LB-.4),KY*(50-7.6),0,0,'none',None,MAT)
# spiral (milsiz): sinüs
path('M'+' L'.join('%.1f,%.1f' % (Yy(1+k*0.5), Zy(RT+3.2*math.sin(k*0.5/35*2*math.pi))) for k in range(int((LB-2)/0.5)+1)),1.6,'#333')
path('M'+' L'.join('%.1f,%.1f' % (Yy(1+k*0.5), Zy(RT-3.2*math.sin(k*0.5/35*2*math.pi))) for k in range(int((LB-2)/0.5)+1)),1.6,'#333')
ln(Yy(0),Zy(0),Yy(LB),Zy(0),1,BLU); ln(Yy(0),Zy(7.6),Yy(LB),Zy(7.6),1,BLU)
for (za,lab) in ((13,'T1'),(36,'T2')):
    ln(Yy(1),Zy(za),Yy(LB-1),Zy(za),1.4,PUR)
    for k in range(10):
        y=3+k*6.8; s=1 if k%2==0 else -1; ln(Yy(y),Zy(za),Yy(y),Zy(za+s*(5 if za==13 else 7)),.9,PUR)
    tx(Yy(LB/2),Zy(za+9),lab,5,'middle','bold',PUR)
rc(Yy(LB-8),Zy(0),KY*7,KY*1,0,0,'none',None,'#fff'); ln(Yy(LB-4.5),Zy(0),Yy(LB-4.5),Zy(-6),1.8,GRN)
rc(Yy(LB-8),Zy(-1)-2,KY*7,3,1,0,RED,None,'#fdeeee'); tx(Yy(LB-4.5),Zy(-9),'ağız 70×60 · kam sürgü',5.2,'middle','bold',GRN)
rc(Yy(-6),Zy(RT+2.5),KY*5,KY*5,1,1,BLU,None,'#dfe7fb'); tx(Yy(-3.5),Zy(RT-4.5),'pençe',4.8,'middle','bold',BLU); tx(Yy(-3.5),Zy(RT-8),'(arka)',4.4,'middle','',BLU)
rc(Yy(-1),Zy(HB+1)-KY*1.2,KY*(LB+2),KY*1.2,1,1,'#111',None,'#cfd8dc'); tx(Yy(LB/2),Zy(HB+4.5),'kapak izole, arkadan menteşe, doldurma önden',5,'middle','',GRY)
tx(Yy(LB/2),Zy(30),'yığın ≤ 50',5.4,'middle','bold',AMB)
tx(Yy(LB/2),Zy(RT+11),'milsiz spiral Ø70 · hatve 35 · 30 dev/dk · ~20 g/tur',5,'middle','',BLU)
ln(Yy(0),Zy(-14),Yy(LB),Zy(-14),.7); tx(Yy(LB/2),Zy(-16),'68 iç · 70 dış',5.4,'middle','bold')
tx(XB+200,YB+256,'kavrama iç kenarda (x 30) → sol kap; sağ kap aynı kesit AYNA (kavrama x 40). Kap = ürün = pozisyon.',5.6,'middle','bold',RED)

# ================= C · KÜÇÜK KAP (L / R ayna) =================
XC,YC = 530,390
rc(XC,YC,400,270,1.3,3,'#999',None,'#fff')
tx(XC+200,YC+16,'C · KÜÇÜK KAP 20 × 54 × 24 — kıyma (SOL) · sucuk & kuşbaşı (SAĞ, ayna)',7.5,'middle','bold')
KS=3.6
for (i,(mir,lab,alt)) in enumerate(((False,'SOL — KIYMA','oluk sağ kenarda → helezon x 30'),(True,'SAĞ — SUCUK · KUŞBAŞI','oluk sol kenarda → helezon x 40'))):
    sx,sz = XC+30+i*200, YC+40+KS*HS
    Xs=lambda c: sx+KS*c; Zs=lambda c: sz-KS*c
    pts,rise,xc = profil(WS,HS,mir)
    poly([(Xs(-0.8),Zs(HS+0.8)),(Xs(-0.8),Zs(-0.8)),(Xs(WS+0.8),Zs(-0.8)),(Xs(WS+0.8),Zs(HS+0.8))],1.2,'#111',PE)
    poly([(Xs(x),Zs(z)) for (x,z) in pts],1.2,'#111','#fff')
    poly([(Xs(x),Zs(min(z,20))) for (x,z) in pts],0,'none',MAT)
    xcm = (WS-xc) if mir else xc
    ci(Xs(xcm),Zs(RT),KS*3.5,1,'#333','#fff'); ci(Xs(xcm),Zs(RT),KS*1.2,.8,'#333','#eee')
    xa_ = xcm+(2 if mir else -2)
    ci(Xs(xa_),Zs(12),KS*5,.9,PUR,'3,2'); ci(Xs(xa_),Zs(12),KS*.6,1,PUR,None,'#efeaf8')
    for a_ in (30,150,270):
        a=math.radians(a_); ln(Xs(xa_),Zs(12),Xs(xa_)+KS*5*math.cos(a),Zs(12)-KS*5*math.sin(a),1.1,PUR)
    tx(Xs(WS/2),YC+34,lab,6.2,'middle','bold'); tx(Xs(WS/2),Zs(-4.5),alt,5,'middle','',GRY)
    tx(Xs(WS/2),Zs(HS+3.5),'20 dış · 18,4 iç',5,'middle','bold')
    tx(Xs(WS+1.5) if not mir else Xs(-1.5),Zs(HS/2),'24',5,'start' if not mir else 'end','bold')
    tx(Xs(3 if not mir else WS-3),Zs(rise/2+2),'55°',5,'middle','bold',AMB)
    tx(Xs(WS/2),Zs(16),'yığın ≤ 20',4.6,'middle','',AMB)
tx(XC+200,YC+205,'kesit %.0f cm² × iç boy 52,4 = %.1f L: kıyma 3 gün 8,6 kg (14,3 L) ✓ · sucuk hafta 8,4 kg (15,3 L) ✓ · kuşbaşı 3 gün 4,3 kg (7 L) ✓' % (aS,vS),5.6,'middle','bold',GRN)
tx(XC+200,YC+218,'helezon: kıyma/sucuk milli Ø70 h 30 · kuşbaşı Ø70 h 50 (küp 20 mm → hatve ≥ 2,5×, ağız ≥ 3× = 60 ✓) · tek tarak Ø10 z 12',5.4,'middle','','#333')
tx(XC+200,YC+231,'dar-uzun (20 × 54) = düşük yığın (≤ 20): kavrulmuş kıyma yağ sıvamaz, sote küp ezilmez; kısa kap ağzı öne, arkaya ara mil',5.4,'middle','','#333')
tx(XC+200,YC+244,'STORE −18 çekmecesine (61 × 65 × 29) döndürülmeden 2 yan yana: 2 × 20 = 40 ≤ 59,5 · 54 ≤ 59,5 · 24 ≤ 29 (pay 5) ✓',5.4,'middle','bold',GRN)
tx(XC+200,YC+257,'sol ve sağ kap aynı kalıp değil: ayna. Kıyma hep solda (L ×4), sucuk + kuşbaşı sağda (R ×6).',5.4,'middle','',RED)

# ================= D · MALZEME TABLOSU =================
XD,YD = 950,100
rc(XD,YD,480,330,1.4,4)
tx(XD+14,YD+22,'D · MALZEME DAVRANIŞI → GEOMETRİ',10,'start','bold')
hdr=['','KAŞAR rende','KIYMA kavrulmuş','KUŞBAŞI sote','SUCUK küp']
cx_=[XD+12,XD+108,XD+200,XD+296,XD+392]
for i,h in enumerate(hdr): tx(cx_[i],YD+44,h,6,'start','bold',GRY)
ln(XD+10,YD+50,XD+470,YD+50,.8,'#bbb')
rows=[('parçacık','lif 2×2×20 mm','kırıntı 3-8 mm','küp 15-20 mm','küp 8-10 mm'),
      ('yığın kg/L','0,41','0,60','0,60','0,55'),
      ('kohezyon','YÜKSEK (yağ+lif)','orta (yağ)','düşük-orta (sos)','düşük (+3 °C)'),
      ('ana risk','kemer + kekleşme','yağ sıvama, topak','ağızda kilit, ezilme','sıcakta yapışma'),
      ('duvar açısı','55°','55°','50°','50°'),
      ('helezon','milsiz Ø70 h35','milsiz Ø70 h30','milli Ø70 h50','milli Ø70 h35'),
      ('tarak','×2 (z13, z36)','×1 z12','×1 hafif','×1 hafif'),
      ('ağız','70×60','70×60','70×60 (≥3×küp)','70×60'),
      ('yığın sınırı','≤ 50','≤ 20','≤ 20','≤ 20'),
      ('sıcaklık','+2…+4','+2…+4','+2…+4','+2…+4'),
      ('tedarik şartı','selülozlu rende','suyu alınmış, vakum','sos azaltılmış','katkısız küp'),
      ('kap','BÜYÜK L','KÜÇÜK L','KÜÇÜK R','KÜÇÜK R')]
for i,r in enumerate(rows):
    yy=YD+66+i*19
    for j,v in enumerate(r): tx(cx_[j],yy,v,5.8,'start','bold' if j==0 else '','#111' if j==0 else '#333')
tx(XD+14,YD+300,'Doz kontrolü hepsinde aynı: helezon turu (hacimsel) + ray altı yük hücresi (gravimetrik) → ±3 g.',5.6,'start','',GRY)
tx(XD+14,YD+313,'Küp malzemede tarak yalnız yığını gevşek tutar; kaşarda tarak olmazsa 45°'+chr(39)+'de bile durur (kemer).',5.6,'start','',GRY)

# ================= E · HİJYEN + KURULUM + KAYNAKLAR =================
XE,YE = 950,450
rc(XE,YE,480,210,1.4,4,'#111',None,'#fcfbf8')
tx(XE+14,YE+22,'E · HİJYEN & YAPIM KURALLARI',10,'start','bold')
for i,s in enumerate(['iç köşe R ≥ 6 mm (EHEDG: ≤135° köşede min 3) · oluk-duvar teğet · uç duvar R 10',
                      'gövde UHMW-PE 10 mm (gıda, −18/+4, sürtünme düşük, hafif) · helezon + tarak 316L',
                      'içeride cıvata/dişli yok: spiral kısa mile kaynaklı, tarak snap-mil, sökmeden yıkanır',
                      'yüzey Ra ≤ 0,8 µm · keskin kenar yok · ölü hacim yok (oluk ucu = ağız)',
                      'kapak conta + izolasyon; kap kapalıyken nem kaçmaz (kaşar kurumaz)',
                      'ağız sürgüsü kam açmalı: kap dışarıdayken kapalı, oturunca açık',
                      'kavrama pençesi pahlı, yaylı: 1 mm ray toleransıyla kendi hizalar']):
    tx(XE+14,YE+42+i*13,s,5.8,'start','','#333')
tx(XE+14,YE+140,'KURULUM: kap tipleri 3 — BÜYÜK-L (kaşar ×2) · KÜÇÜK-L (kıyma ×4) · KÜÇÜK-R (sucuk ×2 + kuşbaşı ×4) = 12 kap',6,'start','bold',GRN)
tx(XE+14,YE+153,'ALT 52: 2 sıra × 3 beşik (20 en × 54 boy): çözülme ×2 · park ×2 · yedek ×2 — beşik kabın U tabanına oturur, robot direkt koyar',5.8,'start','','#333')
tx(XE+14,YE+166,'dikey: teknik 27 · kat 1 63 (kaşar 60) · boşluk 14 · kat 2 27 (küçük 24) · boşluk 14 · ALT 52 = 197 ✓ · tepsi 95 / 54 cm',5.8,'start','','#333')
tx(XE+14,YE+179,'kat 1: kaşar L (x 2-34,5) + sucuk R (x 35-55) · kat 2: kıyma L + kuşbaşı R · motorlar arka duvarda, kısa kaplara ara mil',5.8,'start','','#333')
tx(XE+14,YE+192,'pide Ø30 → bant x 30-40 (tepsi 17 + spiral 13) · helezonlar x 30 (sol) / 40 (sağ) → tam bant kenarı',5.8,'start','bold',BLU)

# ================= KAYNAKLAR + KARAR =================
YK=690
rc(40,YK,1390,470,1.6,4)
tx(56,YK+24,'KAYNAKLAR (araştırma) ve KARAR',12,'start','bold')
src=[('Chemical Engineering — Hopper Design Principles (Jenike): kama huni koniye göre 10-12° daha yatık duvarla kütle akışı verir; duvar sürtünmesi ölçülmeden açı kesinleşmez','chemengonline.com/hopper-design-principles'),
     ('Powder & Bulk Solids — How Wall Friction Affects Hopper Angles: yapışkan malzemede UHMW-PE / parlatılmış paslanmaz astar; Ra ≤ 0,8 µm','powderbulksolids.com'),
     ('EHEDG Doc 8 Hygienic Design Principles: iç açı ≤ 135° → R ≥ 3 mm (tercihen ≥ 6), temizlenebilirlik, ölü hacim yok','ehedg.org · thefoodtech.com/…/Principios-diseno-higienico.pdf'),
     ('KWS / Orthman — Shaftless Screw Conveyor Applications: lifli, yapışkan, sarılan malzemede milsiz spiral; oluk astarı, sıfıra yakın boşluk','kwsmfg.com/engineering-guides/shaftless-screw-conveyor'),
     ('Plastics Today — Agitator Prevents Material Compaction In Feeder Hopper; USPTO 5,287,993 / 5,277,337 Hopper agitator: duvarı sıyıran kol + yığını karıştıran kol','plasticstoday.com · uspto.gov'),
     ('Industrial Plastics — PE1000 (UHMW-PE) hazneler: en düşük sürtünme, yapışkan malzeme, gıda uyumlu','industrialplastics.com.au')]
for i,(s,u) in enumerate(src):
    tx(56,YK+46+i*15,'• '+s,6,'start','','#333'); tx(1414,YK+46+i*15,u,5.2,'end','',BLU)
ln(54,YK+140,1414,YK+140,.8,'#bbb')
rows=[('1. Şekil: yan yana kaplar için en doğru geometri = TEK EĞİMLİ KAMA (dış duvar 55°, iç duvar dik, U-oluk iç kenarda). Simetrik V bantla bağdaşmaz; çapraz taşıyıcı yok. Sağ/sol kaplar ayna, kap = ürün = pozisyon (senin tespitin doğru: kavrama mili kayık, mirror şart).',GRN,'bold'),
      ('2. Kaşar: 32,5 × 70 × 60, 55°, milsiz spiral Ø70, iki tarak, PE gövde, yığın ≤ 50 → %.0f L / %.0f kg ≈ 8-9 gün (yeni menüde kaşar ~4,5 kg/gün). Haftalık, eleman doldurur.' % (vB, vB*0.41),'#333',''),
      ('3. Küçük kap: 20 × 54 × 24 dar-uzun, düşük yığın (≤ 20) — kavrulmuş kıyma ve sote küp için doğru olan bu; %.1f L üçüne de yetiyor (sucuk 15,3). STORE çekmecesine döndürmeden 2 yan yana, 5 cm pay.' % vS,'#333',''),
      ('4. Menü: kıymalı · kuşbaşılı · kaşarlı · sucuklu-kaşarlı. Kıyma ve kuşbaşı harçları KAVRULMUŞ / SOTE, suyu alınmış, vakumlu gelir (çiğ harç makinede olmaz — su salar, 1-2 gün). Yumurta + tereyağı: fırın çıkışı, ayrı.',AMB,''),
      ('5. Kat 1 = şarküteri düzlemi (kaşar L + sucuk R, eleman haftalık) · kat 2 = et düzlemi (kıyma L + kuşbaşı R, robot 3 gün) · ALT 2 sıra × 3 beşik · STORE −18 2+2. Dikey 197 ✓.','#333',''),
      ('6. Prototipte ölçülecek (kesinleşmeden üretim yok): kaşar-PE sürtünme açısı, köprüleme ağız genişliği, 50 cm yığın 24 s kekleşme, milsiz spiralde kaşar geri sarması, küp kilitlenmesi.',AMB,''),
      ('Onaylarsan: TOPPING v22 (bu kaplarla izometrik + ön kesit + ALT beşikleri + STORE kesiti, tek pafta) → HAT v45.',BLU,'bold')]
for i,(s,c,fw) in enumerate(rows):
    tx(56,YK+160+i*42,s[:190],7,'start',fw,c)
    if len(s)>190: tx(56,YK+160+i*42+12,s[190:],7,'start','',c)
tx(W-40,H-12,'AUTOKITCH · arastirma/3_TOPPING/kap_geometri_v1 · 5 Eyl 2026',7,'end','',GRY)
o.append('</svg>')
svg = chr(10).join(o)
xml.dom.minidom.parseString(svg.encode('utf-8'))
out = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\3_TOPPING\kap_geometri_v1.svg"
io.open(out,'w',encoding='utf-8').write(svg)
print('yazildi + XML gecerli | kasar kesit %.0f cm2 → %.0f L → %.0f kg (rise %.1f) | kucuk %.0f cm2 → %.1f L (rise %.1f)' % (aB,vB,vB*0.41,riseB,aS,vS,riseS))
