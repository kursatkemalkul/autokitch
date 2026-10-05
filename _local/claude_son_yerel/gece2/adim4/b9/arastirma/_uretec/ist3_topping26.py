# -*- coding: utf-8 -*-
# TOPPING v26 — KAP = PICNIC TİPİ (Kemal, 5 Eyl): dairesel duvar (tarak süpürmesiyle eş merkezli) + plastik milli helezon (POM) +
# omurgalı çubuk tarak (kafes) + şeffaf PC gövde; ölçüler bizim istasyona uyarlı: 14×68 dış, kat 27 (kap 26 kızak dahil).
# İstasyon (v25 yerleşim, HAT v46) değişmedi. Referans kareler: 3_TOPPING/referans/picnic_kap_helezon / picnic_kap_tarak / picnic_tarak_detay / picnic_reload_pepp.
import io, math, xml.dom.minidom
W, H = 1460, 1010
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
def pline(pts,sw=1,c='#111',d=None):
    o.append('<polyline points="%s" fill="none" stroke="%s" stroke-width="%s"%s stroke-linejoin="round"/>' % (' '.join('%.1f,%.1f'%p for p in pts),c,sw,(' stroke-dasharray="%s"'%d) if d else ''))
def arr(x1,y1,x2,y2,c='#c0392b',w=1.3):
    ln(x1,y1,x2,y2,w,c); a=math.atan2(y2-y1,x2-x1)
    for s in (1,-1): ln(x2,y2,x2-7*math.cos(a-s*.42),y2-7*math.sin(a-s*.42),w,c)
def dim(x1,y1,x2,y2,s,fs=5.6,off=0,col='#111'):
    ln(x1,y1,x2,y2,.7,col);
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
def f1(v): return ('%.1f' % v).replace('.',',')

GRN, RED, BLU, GRY, AMB, PUR = '#1d7a4f', '#c0392b', '#1a49b8', '#666', '#b7791f', '#6b4fa8'
PC, MAT, POM, STEEL, LIGHT = '#dbeeff', '#e9dfa8', '#f4f4f4', '#cfd8dc', '#f7f6f2'

# ---------------- GEOMETRİ (cm) ----------------
WK, LK = 14.0, 68.0           # dış en · boy
ET = 0.5                      # PC duvar
KZ_H, KZ_W, CEP_W, CEP_H = 2.0, 3.0, 2.0, 1.4
HTOT = 26.0                   # kızak altından üst kenara (v25 ile aynı: kap 24 + kızak 2 → kat 27)
Wi = WK-2*ET; Li = LK-2*ET
Hi = HTOT-KZ_H-ET             # iç yükseklik (iç taban z=0, üst kenar z=Hi)
RT = 3.8                      # yalak yarıçapı (helezon Ø7 + 0,3 pay)
HEL_D, HEL_MIL, HEL_P, HEL_L = 7.0, 2.0, 5.0, 60.0
ZH = 14.0                     # tarak göbek yüksekliği
RW = Wi/2                     # duvar dairesi yarıçapı (göbek merkezli) = 6,5
RR = RW-0.8                   # tarak en dış çubuk merkezi = 5,7 (çubuk Ø6 → duvara 0,5)
RODS = (RR, RR*0.75, RR*0.5, RR*0.25)      # çubuk yarıçapları (omurga üzerinde)
ROD_D = 0.6
ZC = ZH-math.sqrt(RW**2-RT**2)   # daire duvarın boğaz duvarına (x=±3,8) değdiği yükseklik
PAY_HEL = ZH-RR-ROD_D/2-(RT+HEL_D/2)
assert PAY_HEL >= 0.6, 'tarak helezona değiyor: %.2f' % PAY_HEL
def profil(n=24):
    pts=[(-RW,Hi),(-RW,ZH)]
    a0=math.pi; a1=math.pi+math.acos(RT/RW)
    for k in range(1,n+1):
        a=a0+(a1-a0)*k/n; pts.append((RW*math.cos(a),ZH+RW*math.sin(a)))
    pts.append((-RT,RT))
    for k in range(1,n+1):
        a=math.pi+math.pi*k/n; pts.append((RT*math.cos(a),RT+RT*math.sin(a)))
    pts.append((RT,ZC))
    a0=2*math.pi-math.acos(RT/RW); a1=2*math.pi
    for k in range(1,n+1):
        a=a0+(a1-a0)*k/n; pts.append((RW*math.cos(a),ZH+RW*math.sin(a)))
    pts+=[(RW,ZH),(RW,Hi)]
    return pts
PROF=profil()
def alan(pts):
    s=0
    for i in range(len(pts)):
        x1,z1=pts[i]; x2,z2=pts[(i+1)%len(pts)]; s+=x1*z2-x2*z1
    return abs(s)/2
AREA=alan(PROF)
HAVA=2.0                                   # üstte hava payı
AREA_USE=AREA-Wi*HAVA
VOL_BRUT=AREA*Li/1000
V_HEL=(math.pi*(HEL_MIL/2)**2*HEL_L + (HEL_L/HEL_P)*math.pi*((HEL_D/2)**2-(HEL_MIL/2)**2)*0.6)/1000
V_TAR=(len(RODS)*math.pi*(ROD_D/2)**2*63 + 2*math.pi*1.5**2*1.2)/1000
VOL_USE=AREA_USE*Li/1000-V_HEL-V_TAR
DENS={'KAŞAR':0.41,'KIYMA':0.60,'SUCUK':0.55,'KUŞBAŞI':0.60}
CAP={k:VOL_USE*v for k,v in DENS.items()}
GUNLUK={'KAŞAR':4.5,'KIYMA':8.6/3,'SUCUK':8.4/7,'KUŞBAŞI':4.3/3}
DOLUM={'KAŞAR':CAP['KAŞAR'],'KIYMA':min(8.6,CAP['KIYMA']),'SUCUK':min(8.4,CAP['SUCUK']),'KUŞBAŞI':4.3}
GUN={k:DOLUM[k]/GUNLUK[k] for k in DOLUM}
# kütleler
PERIM=sum(math.dist(PROF[i],PROF[i+1]) for i in range(len(PROF)-1))
M_PC=((PERIM*Li + 2*AREA)*ET + 2*Li*(KZ_W*KZ_H-CEP_W*CEP_H) + Li*2*4.0*0.5)*1.2/1000
M_HEL=V_HEL*1.41+0.1
M_TAR=V_TAR*7.9+0.3
M_BOS=M_PC+M_HEL+M_TAR
CATAL=2.0
KOL={k:DOLUM[k]+M_BOS+CATAL for k in DOLUM}
DEV_CM3=(math.pi*((HEL_D/2)**2-(HEL_MIL/2)**2)*HEL_P)*0.7   # dolum katsayısı 0,7
# tarak-duvar kontrolü (her çubuk, her açı)
def wall_halfwidth(z):
    if z>=ZH: return RW
    if z>=ZC: return math.sqrt(max(RW**2-(z-ZH)**2,0))
    if z>=RT: return RT
    return math.sqrt(max(RT**2-(z-RT)**2,0))
minclr=9
for r in RODS:
    for k in range(360):
        a=math.radians(k); x=r*math.sin(a); z=ZH-r*math.cos(a)
        minclr=min(minclr, wall_halfwidth(z)-abs(x)-ROD_D/2)
        minclr=min(minclr, math.dist((x,z),(0,RT))-HEL_D/2-ROD_D/2)
assert minclr>=0.45, 'tarak paysız: %.2f' % minclr

o.append('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">' % (W,H,W,H))
rc(0,0,W,H,0,0,'none',None,'#fff')
tx(30,40,'AUTOKITCH — TOPPING v26 (5 Eyl 2026) — KAP = PICNIC TİPİ: dairesel duvar (tarak süpürmesiyle eş merkezli) · plastik milli HELEZON (POM) · omurgalı çubuk TARAK · şeffaf PC gövde — ölçüler bizim istasyona uyarlı (14×68, kat 27)',14,'start','bold')
tx(30,62,'Kemal: "biz böyle kuralım — ince uzun (sos) değil, kaşardaki gibi; alttaki plastik helezonu al, üstü ve kap boyunu bize göre ayarla; köprü kırıcıyı resimdeki gibi yap." Referans kareler: referans/picnic_kap_helezon · picnic_kap_tarak · picnic_tarak_detay · picnic_reload_pepp (sitede). İstasyon yerleşimi (v25) ve HAT v46 değişmedi: kap dış ölçüsü, kızaklar, çatal, raflar aynı.',9,'start','','#444')
ln(30,74,W-30,74,.8,'#999')

# ================= A · ÖN KESİT =================
XA,YA,WA,HA_ = 40,90,400,500
rc(XA,YA,WA,HA_,1.4,4,'#111',None,'#fcfdff')
tx(XA+14,YA+22,'A · ÖN KESİT — daire duvar R 6,5 · tarak R %s · helezon Ø7 · boğaz 7,6' % f1(RR),10,'start','bold')
K=12.5; ax=XA+110; az=YA+150+K*Hi
X=lambda c: ax+K*c; Z=lambda c: az-K*c
# dış gövde (ince duvar: profil offset ~0,5) — basitlik: dış kontur = profil dışa 0,5 (yaklaşık: aynı profil ölçeklenmiş değil, çizgi kalınlığıyla)
outer=[(x-ET if x<0 else x+ET, z) for (x,z) in PROF]
outer=[(x, z-ET if z<RT+0.01 and abs(x)<=RT+ET else z) for (x,z) in outer]
poly([(X(x),Z(z)) for (x,z) in outer],1.2,'#111',PC)
poly([(X(x),Z(z)) for (x,z) in PROF],1.0,'#333','#fff')
# malzeme (üstte 2 cm hava)
poly([(X(x),Z(min(z,Hi-HAVA))) for (x,z) in PROF],0,'none',MAT,None,.85)
# taban: kızaklar + nervür
for sx_ in (-4,4):
    rc(X(sx_-KZ_W/2),Z(-ET),K*KZ_W,K*KZ_H,1.1,0,'#111',None,'#d0d7de')
    rc(X(sx_-CEP_W/2),Z(-ET-0.3),K*CEP_W,K*CEP_H,.8,0,'#555',None,'#fff')
    # nervür: kızak üstünden yalak dış yüzeyine
    zt=RT-math.sqrt((RT+ET)**2-sx_**2)
    poly([(X(sx_-KZ_W/2),Z(-ET)),(X(sx_+KZ_W/2),Z(-ET)),(X(sx_+KZ_W/2),Z(zt+0.3)),(X(sx_-KZ_W/2),Z(zt-0.3))],.8,'#333',PC)
ln(X(-6),Z(-ET-KZ_H)-K*0.2,X(6),Z(-ET-KZ_H)-K*0.2,1.4,'#555'); tx(X(0),Z(-ET-KZ_H)-K*0.2-4,'L raflar (kabinde)',4.8,'middle','',GRY)
# helezon (kesit): dış daire Ø7, mil Ø2
ci(X(0),Z(RT),K*HEL_D/2,1.2,GRN,None,POM); ci(X(0),Z(RT),K*HEL_MIL/2,1,GRN,None,'#ddd')
for a in range(0,360,45):
    ln(X(HEL_MIL/2*math.cos(math.radians(a))),Z(RT+HEL_MIL/2*math.sin(math.radians(a))),X(HEL_D/2*0.95*math.cos(math.radians(a))),Z(RT+HEL_D/2*0.95*math.sin(math.radians(a))),.6,GRN)
# tarak: süpürme dairesi, göbek, omurga, çubuklar
ci(X(0),Z(ZH),K*RR,.9,PUR,'4,3','none'); ci(X(0),Z(ZH),K*RW,.7,'#999','2,2','none')
ci(X(0),Z(ZH),K*1.5,1.2,'#333',None,'#e8e8e8')
th=math.radians(38)   # omurga açısı (aşağı-sağ)
sx_,sz_=math.sin(th),-math.cos(th)
ln(X(0),Z(ZH),X(RR*sx_),Z(ZH+RR*sz_),3,'#333')
for r in RODS:
    ci(X(r*sx_),Z(ZH+r*sz_),K*ROD_D/2+1.2,1.1,'#111',None,'#fff')
tx(X(0),Z(ZH)+3,'göbek',4.4,'middle','bold','#333')
# ölçüler
dim(X(-WK/2),Z(Hi+1.2),X(WK/2),Z(Hi+1.2),'14 dış · iç 13',5.8)
dim(X(-RT),Z(ZC-0.3),X(RT),Z(ZC-0.3),'boğaz 7,6',5.2,0,GRN)
dim(X(WK/2+5.0),Z(Hi),X(WK/2+5.0),Z(-ET-KZ_H),'26 (kızak dahil) → kat 27',5.6,0)
dim(X(WK/2+1.0),Z(Hi),X(WK/2+1.0),Z(ZH),'%s dik' % f1(Hi-ZH),4.8,0,GRY)
dim(X(WK/2+1.0),Z(ZH),X(WK/2+1.0),Z(ZC),'%s daire' % f1(ZH-ZC),4.8,0,GRY)
dim(X(WK/2+1.0),Z(ZC),X(WK/2+1.0),Z(RT),'%s boğaz' % f1(ZC-RT),4.8,0,GRY)
dim(X(WK/2+1.0),Z(RT),X(WK/2+1.0),Z(0),'3,8 yalak',4.8,0,GRY)
tx(X(0),Z(Hi-HAVA)+2,'dolu seviye (2 cm hava)',4.4,'middle','',AMB)
ly=YA+40
for s,c,fw in [('ŞEKİL = Picnic kaşar haznesi: göbeğin etrafında R 6,5 daire duvar → çubuklar (Ø6) duvara 0,5 cm yaklaşır, ölü köşe yok; üstte 9 cm dik duvar (depo); altta 7,6 boğaz + yalak R 3,8, içinde helezon.','#111','bold'),
               ('Tarak göbeği z %s: en alt çubuk altı z %s, helezon tepesi %s → pay %s; çubuk–duvar en az %s.' % (f1(ZH),f1(ZH-RR-ROD_D/2),f1(RT+HEL_D/2),f1(PAY_HEL),f1(minclr)),GRN,''),
               ('Hacim: kesit %s cm² → brüt %s L · kullanılabilir (2 cm hava, helezon + tarak düşülmüş) %s L.' % (f1(AREA),f1(VOL_BRUT),f1(VOL_USE)),'#333',''),
               ('Gövde: şeffaf polikarbonat 5 mm (Picnic gibi; seviye görünür; −40 °C ✓, bulaşık ✓) — v25 opak UHMW-PE yerine.','#333',''),
               ('Kızaklar ve nervür gövdeyle tek kalıp (çatal cebi 2,0×1,4). Kap dışı 14×68, kızakla 26 → kat 27, v25 raflar aynı.','#333','')]:
    ly=para(XA+14,ly if ly>YA+40 else YA+40,s,68,5.4,c,fw)
# (metin panelin üst kısmında; kesit onun altında — kesit ax/az yukarıda ayarlandı, çakışmasın diye kesit sağa kaydırılmış)

# ================= B · BOY KESİT =================
XB,YB,WB,HB = 460,90,660,265
rc(XB,YB,WB,HB,1.4,4,'#111',None,'#fcfbf8')
tx(XB+14,YB+22,'B · BOY KESİT — helezon Ø7 hatve 5 boy 60 (POM) · arka topuz Ø5 (2 cm dışarı) · tarak çubukları boydan boya · ağız ön uçta 6×6,5',10,'start','bold')
KL=8.6; bx=XB+40; bz=YB+50+KL*Hi
XL=lambda y: bx+KL*y; ZL=lambda z: bz-KL*z
# gövde (yan duvar kesiti): arka duvar y 0-0,5, ön duvar 67,5-68
rc(XL(0),ZL(Hi),KL*LK,KL*(Hi+ET),1.2,1,'#111',None,PC)
rc(XL(ET),ZL(Hi),KL*Li,KL*Hi,.9,0,'#333',None,'#fff')
rc(XL(ET),ZL(Hi-HAVA),KL*Li,KL*(Hi-HAVA),0,0,'none',None,MAT)   # malzeme
# kızaklar (yandan)
rc(XL(0),ZL(-ET-KZ_H),KL*LK,KL*KZ_H,1,0,'#111',None,'#d0d7de'); tx(XL(34),ZL(-ET-KZ_H/2)+2,'kızak (2 adet, boydan boya) — çatal cebi 2,0×1,4',4.6,'middle','','#333')
# ağız: ön uçta yalak tabanında delik y 60-66,5
AG0,AG1=60.0,66.5
rc(XL(AG0),ZL(0)-2,KL*(AG1-AG0),KL*ET+4,0,0,'none',None,'#fff')
ln(XL(AG0),ZL(0),XL(AG0),ZL(-ET),1,'#111'); ln(XL(AG1),ZL(0),XL(AG1),ZL(-ET),1,'#111')
arr(XL((AG0+AG1)/2),ZL(-ET-KZ_H)+6,XL((AG0+AG1)/2),ZL(-ET-KZ_H)+30,GRN,1.4); tx(XL(AG0)-6,ZL(-ET-KZ_H)+26,'AĞIZ 6 × 6,5 → tepsi (merkez y 63 ≥ 31 ✓)',5,'end','bold',GRN)
# helezon: mil + kanatlar
ln(XL(ET),ZL(RT),XL(ET+HEL_L),ZL(RT),KL*HEL_MIL,GRN)
n=int(HEL_L/HEL_P)
for i in range(n):
    y0=ET+i*HEL_P
    pline([(XL(y0),ZL(RT+HEL_D/2)),(XL(y0+HEL_P/2),ZL(RT-HEL_D/2)),(XL(y0+HEL_P),ZL(RT+HEL_D/2))],1.1,GRN)
ln(XL(ET),ZL(RT+HEL_D/2),XL(ET+HEL_L),ZL(RT+HEL_D/2),.5,GRN,'2,2'); ln(XL(ET),ZL(RT-HEL_D/2),XL(ET+HEL_L),ZL(RT-HEL_D/2),.5,GRN,'2,2')
# arka kavrama topuzu (dışarı 2 cm)
rc(XL(-2.0),ZL(RT+2.5),KL*2.0,KL*5.0,1.2,2,GRN,None,POM); tx(XL(-1.0),ZL(RT+3.2),'topuz Ø5',4.2,'middle','bold',GRN)
for k in range(6): ln(XL(-2.0),ZL(RT+2.5-k*0.8-0.4),XL(0),ZL(RT+2.5-k*0.8-0.4),.5,GRN)
tx(XL(-1.0),ZL(RT-3.4),'yaylı',4.0,'middle','',GRN); tx(XL(-1.0),ZL(RT-4.0),'sokete',4.0,'middle','',GRN)
# tarak: arka göbek (duvardan tahrik), omurga, çubuklar boydan boya, ön omurga + pim yatağı
ci(XL(1.5),ZL(ZH),KL*1.5,1.1,'#333',None,'#e8e8e8'); rc(XL(-1.2),ZL(ZH+0.7),KL*1.2,KL*1.4,1,1,'#333',None,'#ccc')
tx(XL(3.5),ZL(ZH+2.6),'tarak kavraması (kare uç, duvardan)',4.2,'start','',GRY)
ci(XL(Li-0.6),ZL(ZH),KL*1.2,1,'#333',None,'#e8e8e8'); tx(XL(Li-0.6),ZL(ZH+2.2),'ön omurga + pim yatağı',4.2,'middle','',GRY)
for r in RODS:
    z=ZH+r*sz_
    ln(XL(2.5),ZL(z),XL(Li-1.5),ZL(z),KL*ROD_D+0.6,'#333')
ln(XL(2.5),ZL(ZH),XL(2.5),ZL(ZH+RR*sz_),2.6,'#333'); ln(XL(Li-1.5),ZL(ZH),XL(Li-1.5),ZL(ZH+RR*sz_),2.6,'#333')
tx(XL(34),ZL(ZH+1.0),'TARAK: 4 çubuk Ø6 paslanmaz, boy 63 (r %s/%s/%s/%s) · omurga arka + ön · göbek z %s · 10–20 dev/dk' % (f1(RODS[0]),f1(RODS[1]),f1(RODS[2]),f1(RODS[3]),f1(ZH)),5,'middle','bold','#333')
ln(XL(2.5),ZL(ZH+RR),XL(Li-1.5),ZL(ZH+RR),.6,PUR,'4,3'); ln(XL(2.5),ZL(ZH-RR),XL(Li-1.5),ZL(ZH-RR),.6,PUR,'4,3'); tx(XL(34),ZL(ZH+RR)-3,'süpürme bandı R %s (z %s–%s)' % (f1(RR),f1(ZH-RR),f1(ZH+RR)),4.4,'middle','',PUR)
# kapak (kesikli)
rc(XL(0),ZL(Hi+1.2),KL*LK,KL*1.2,.8,1,BLU,'4,3','none'); tx(XL(34),ZL(Hi+1.2)-3,'geçmeli şeffaf kapak (depolama / taşıma; katta çıkarılır ya da açık kalır)',4.6,'middle','',BLU)
# ölçüler
dim(XL(ET),ZL(RT+HEL_D/2+0.9),XL(ET+HEL_L),ZL(RT+HEL_D/2+0.9),'helezon 60 (12 hatve × 5)',4.8,0,GRN)
tx(XL(LK)-2,ZL(Hi+0.8),'ÖN',4.6,'end','bold',GRY)
tx(XL(0)+2,ZL(Hi+0.8),'ARKA',4.6,'start','bold',GRY)

# ================= C · ÜST GÖRÜNÜM (kap planı) =================
XC,YC,WC,HC = 460,370,660,220
rc(XC,YC,WC,HC,1.4,4,'#111',None,'#fcfdff')
tx(XC+14,YC+22,'C · KAP PLANI — helezon eksende · tarak çubukları omurga açısında · ağız ön uçta kızaklar arasında',10,'start','bold')
KP=8.6; cx0=XC+40; cy0=YC+60
XP=lambda y: cx0+KP*y; YP=lambda x: cy0+KP*(WK/2+x)
rc(XP(0),YP(-WK/2),KP*LK,KP*WK,1.2,1,'#111',None,PC); rc(XP(ET),YP(-Wi/2),KP*Li,KP*Wi,.9,0,'#333',None,'#fff')
for sx_ in (-4,4): rc(XP(0),YP(sx_-KZ_W/2),KP*LK,KP*KZ_W,.8,0,'#555','3,2','none')
tx(XP(20),YP(-4)+2,'kızak / çatal cebi',4.2,'middle','',GRY); tx(XP(20),YP(4)+2,'kızak / çatal cebi',4.2,'middle','',GRY)
rc(XP(AG0),YP(-3),KP*(AG1-AG0),KP*6,1.2,1,GRN,None,'#eaf6ee'); tx(XP((AG0+AG1)/2),YP(0)+2,'AĞIZ',4.8,'middle','bold',GRN)
ln(XP(ET),YP(0),XP(ET+HEL_L),YP(0),KP*HEL_MIL,GRN)
for i in range(n):
    y0=ET+i*HEL_P
    pline([(XP(y0),YP(-HEL_D/2)),(XP(y0+HEL_P/2),YP(HEL_D/2)),(XP(y0+HEL_P),YP(-HEL_D/2))],.9,GRN)
for r in RODS:
    x=r*sx_
    ln(XP(2.5),YP(x),XP(Li-1.5),YP(x),KP*ROD_D+0.6,'#333')
ln(XP(2.5),YP(-RR),XP(Li-1.5),YP(-RR),.6,PUR,'4,3'); ln(XP(2.5),YP(RR),XP(Li-1.5),YP(RR),.6,PUR,'4,3')
rc(XP(-2.0),YP(-2.5),KP*2.0,KP*5.0,1.2,2,GRN,None,POM); tx(XP(-1.0),YP(-3.2),'topuz',4.2,'middle','bold',GRN)
rc(XP(-1.2),YP(-0.7)-KP*ZH*0,KP*1.2,KP*1.4,1,1,'#333',None,'#ccc')
tx(XP(34),YP(-WK/2)-6,'plan: helezon (yeşil) eksende, tarak çubukları (siyah) omurga açısında sağ yarıda; süpürme ±%s (mor); arka duvarda 2 kavrama: helezon (z 3,8) + tarak (z %s)' % (f1(RR),f1(ZH)),5,'middle','','#333')
dim(XP(0),YP(WK/2)+16,XP(LK),YP(WK/2)+16,'68',5.6)
dim(XP(LK)+10,YP(-WK/2),XP(LK)+10,YP(WK/2),'14',5.6)

# ================= D · PARÇALAR =================
XD,YD,WD,HD = 1140,90,290,500
rc(XD,YD,WD,HD,1.4,4,'#111',None,'#fff')
tx(XD+14,YD+22,'D · PARÇA LİSTESİ (1 kap)',10,'start','bold')
parts=[('1 GÖVDE','şeffaf PC 5 mm, tek kalıp: daire duvar + boğaz + yalak + 2 kızak + nervür; üst açık, geçmeli kapak · ≈ %s kg' % f1(M_PC)),
       ('2 HELEZON','POM beyaz, milli: Ø70 dış · mil Ø20 · hatve 50 · boy 600 · kanat 6 mm · arka uçta tırtıllı topuz Ø50 (2 cm dışarı, yaylı sokete) · ≈ %s kg · %d cm³/dev (dolum 0,7)' % (f1(M_HEL),DEV_CM3)),
       ('3 TARAK (kafes)','304 paslanmaz: arka göbek Ø30 (kare uç kavrama) + omurga 6 mm + 4 çubuk Ø6 × 630 (r %d/%d/%d/%d mm) + ön omurga + pim yatağı · göbek z %s · ≈ %s kg' % (RODS[0]*10,RODS[1]*10,RODS[2]*10,RODS[3]*10,f1(ZH),f1(M_TAR))),
       ('4 KAPAK','şeffaf PC, geçmeli; depolama/taşıma (STORE −18, ALT); kat içinde kapak çıkarılır'),
       ('5 SIZDIRMAZLIK','arka duvar 2 delik: helezon mili Ø20 + tarak mili Ø10, gıda tipi dudak keçe'),
       ('KABİN TARAFI','kap başına 2 yaylı soket (z 3,8 helezon · z %s tarak): helezon adım motoru (dozaj = devir) + tarak motoru 10 W, 10–20 dev/dk (ya da tek motor + 1:10 kayış) · L raf çifti · klape' % f1(ZH))]
py_=YD+40
for a_,b_ in parts:
    tx(XD+14,py_,a_,6.2,'start','bold','#111'); py_=para(XD+14,py_+9,b_,54,5.2,'#333')+4
py_=para(XD+14,py_+2,'Boş kap ≈ %s kg (v25 4,6). Gramaj: helezon 1 devir ≈ %d cm³ → kaşar ≈ %d g, sucuk küp ≈ %d g; 1 pide 60–80 g ≈ 1–1,5 devir, adım motoruyla 1/16 devir çözünürlük.' % (f1(M_BOS),DEV_CM3,DEV_CM3*0.41,DEV_CM3*0.55),54,5.2,GRN,'bold')

# ================= E · PICNIC → BİZ =================
XE,YE,WE,HE = 40,610,640,370
rc(XE,YE,WE,HE,1.4,4,'#111',None,'#fcfdff')
tx(XE+14,YE+22,'E · PICNIC KAŞAR HAZNESİNDEN ALINANLAR → BİZİM KABA UYARLAMA',10,'start','bold')
rows=[('Şekil','şarap kadehi: göbek etrafında daire duvar, üstte geniş dik, altta boğaz','aynı mantık, 14 cm ene sığdırıldı: R 6,5 daire, 9 dik, 7,6 boğaz'),
      ('Helezon','yalakta boydan boya beyaz plastik milli helezon, uçta tırtıllı topuz (elle takılır)','POM Ø70 hatve 50 boy 60, topuz Ø50 → yaylı soket; hepsi aynı (milsiz spiral iptal)'),
      ('Köprü kırıcı','göbek + omurga + omurgaya dik ince çubuklar (tarak), arka duvardan tahrik','4 çubuk Ø6 × 630, r %d/%d/%d/%d mm, göbek z %s, arka + ön omurga (63 cm sehim için)' % (RODS[0]*10,RODS[1]*10,RODS[2]*10,RODS[3]*10,f1(ZH))),
      ('Gövde','şeffaf, seviye görünür, üstten dolum, kapak','şeffaf PC 5 mm; robot değiştirir, eleman ALT/STORE rafına iter; geçmeli kapak'),
      ('Ağız','ön uçta, altta dozaj kafası + yayıcı plaka, pizza bantta geçer','ön uçta 6×6,5 delik, tepsi robotla süpürür (yayıcı plaka sorusu açık)'),
      ('Kat/istasyon','tek hazne tek istasyon, bant','2 kap yan yana, 3 kat, kızak + L raf + çatal (v25) — değişmedi')]
tx(XE+14,YE+44,'öğe',5.8,'start','bold',GRY); tx(XE+100,YE+44,'Picnic (karelerde)',5.8,'start','bold',GRY); tx(XE+370,YE+44,'bizde (v26)',5.8,'start','bold',GRY)
ln(XE+12,YE+49,XE+WE-12,YE+49,.8,'#bbb')
yy=YE+62
for a_,b_,c_ in rows:
    tx(XE+14,yy,a_,5.8,'start','bold','#111')
    y1=para(XE+100,yy,b_,60,5.4,'#333'); y2=para(XE+370,yy,c_,62,5.4,GRN)
    yy=max(y1,y2)+4
para(XE+14,yy+4,'Almadıklarımız: sos pompası (bizde sos yok) · pepperoni karton şarjörü ve dilimleyici (sucuk KÜP gelir, kesme yok) · cepli çark hazneleri (küpler helezonla; alternatif olarak not) · bant (bizde robot + tepsi).',105,5.4,AMB)

# ================= F · KG · GÜN · ROBOT · KONTROL =================
XF,YF,WF,HF = 700,610,730,370
rc(XF,YF,WF,HF,1.4,4,'#111',None,'#fff')
tx(XF+14,YF+22,'F · KAPASİTE · DEĞİŞİM · KOL YÜKÜ · KONTROL (kap %s L kullanılabilir; v25 17,5 L brüt ≈ 15 kullanılabilir)' % f1(VOL_USE),10,'start','bold')
hdr=['malzeme','kapasite','dolum','gün','değişim/hafta','dolu kap','kol (+çatal 2)']
cx_=[XF+14,XF+110,XF+210,XF+300,XF+380,XF+490,XF+580]
for i,h in enumerate(hdr): tx(cx_[i],YF+44,h,5.9,'start','bold',GRY)
ln(XF+12,YF+49,XF+WF-12,YF+49,.8,'#bbb')
tbl=[('KAŞAR rende','%s kg' % f1(CAP['KAŞAR']),'%s kg (tam)' % f1(DOLUM['KAŞAR']),'%s (2 poz. %s)' % (f1(GUN['KAŞAR']),f1(2*GUN['KAŞAR'])),'%d' % round(7/GUN['KAŞAR'])),
     ('KIYMA kavrulmuş','%s kg' % f1(CAP['KIYMA']),'%s kg' % f1(DOLUM['KIYMA']),f1(GUN['KIYMA']),'%d' % math.ceil(7/GUN['KIYMA'])),
     ('SUCUK küp','%s kg' % f1(CAP['SUCUK']),'%s kg' % f1(DOLUM['SUCUK']),f1(GUN['SUCUK']),'%d' % math.ceil(7/GUN['SUCUK'])),
     ('KUŞBAŞI sote','%s kg' % f1(CAP['KUŞBAŞI']),'4,3 kg (3 gün)','3','2')]
for i,(nm,cap,dol,gun,deg) in enumerate(tbl):
    yy=YF+64+i*15; k=nm.split(' ')[0]
    for j,v in enumerate((nm,cap,dol,gun,deg,f1(DOLUM[k]+M_BOS),f1(KOL[k]))):
        tx(cx_[j],yy,v,5.9,'start','bold' if j==0 else '','#111' if j==0 else (RED if (j==6 and KOL[k]>12.5) else '#333'))
ln(XF+12,YF+128,XF+WF-12,YF+128,.8,'#bbb')
notes=[('Hacim v25 → v26: 17,5 L brüt → %s L brüt / %s L kullanılabilir. Sonuç: kaşar %s gün (2 pozisyon %s), kıyma %s gün, sucuk %s gün. Robot haftada ≈ %d kap değişimi (v25 9–10).' % (f1(VOL_BRUT),f1(VOL_USE),f1(GUN['KAŞAR']),f1(2*GUN['KAŞAR']),f1(GUN['KIYMA']),f1(GUN['SUCUK']),round(7/GUN['KAŞAR'])+math.ceil(7/GUN['KIYMA'])+math.ceil(7/GUN['SUCUK'])+2),'#333',''),
       ('Kol yükü: en ağır kıyma kabı %s kg (kap boş %s + çatal 2) → ⑦ değişmedi: 16–20 kg sınıfı, menzil ≥ 130.' % (f1(KOL['KIYMA']),f1(M_BOS)),RED,'bold'),
       ('KONTROL ✓ kap dışı 14×68, kızakla 26 → kat 27, tepsi düzlemleri 158/117/76 aynı · ✓ ağız ön uçta y 63 ≥ 31 · ✓ tarak–helezon pay %s, tarak–duvar ≥ %s · ✓ küp: kanal derinliği (70−20)/2 = 2,5 ≥ 1,5 · hatve 5 ≥ 2,5×1,5 · ağız 6 ≥ 3×1,5 · ✓ PC −40 °C, bulaşık 90 °C' % (f1(PAY_HEL),f1(minclr)),GRN,'bold'),
       ('AÇIK: arka duvarda kap başına 2 motor (helezon + tarak) mi, tek motor + kayış mı · ağız altında Picnic yayıcı plakası (tepsi düz geçiş) mi, spiral süpürme mi (Kemal) · kuşbaşı parça ≤ 2 cm şartı · gramaj testi (dolum katsayısı 0,7 varsayım) · PC çizilme (UHMW daha dayanıklıydı) · HAT v46 kap simgesi v26 iç şekline güncellenecek (dış ölçü aynı).',AMB,''),
       ('Sıradaki: bu kap onaylanırsa ağız/yayıcı detayı + gramaj prototipi; STORE v5 ve HAT v46 değişmez (kap dışı aynı).',BLU,'bold')]
ny=YF+144
for s,c,fw in notes: ny=para(XF+14,ny,s,150,5.7,c,fw)+3
tx(W-40,H-10,'AUTOKITCH · arastirma/3_TOPPING/ist3_topping_detay_v26 · 5 Eyl 2026',7,'end','',GRY)
o.append('</svg>')
svg=chr(10).join(o)
xml.dom.minidom.parseString(svg.encode('utf-8'))
out=r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\3_TOPPING\ist3_topping_detay_v26.svg"
io.open(out,'w',encoding='utf-8').write(svg)
print('yazildi + XML gecerli | alan %.1f cm2 · brut %.1f L · kullanilabilir %.1f L · ZC %.2f · minclr %.2f · PC %.2f hel %.2f tar %.2f bos %.2f · dev %d cm3 · kasar %.1f kg %.2f gun · kiyma %.1f sucuk %.1f · kol kiyma %.1f' % (AREA,VOL_BRUT,VOL_USE,ZC,minclr,M_PC,M_HEL,M_TAR,M_BOS,DEV_CM3,CAP['KAŞAR'],GUN['KAŞAR'],CAP['KIYMA'],CAP['SUCUK'],KOL['KIYMA']))
