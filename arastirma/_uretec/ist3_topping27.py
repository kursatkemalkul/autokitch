# -*- coding: utf-8 -*-
# TOPPING v27 — KAP AĞIZ · KAPAK · TUTMA DETAYI (Kemal'in 4 sorusu): kapalı boru ucu + tek ağız · yaylı menteşeli kapak + raf pimi ·
# kızaklar ±5 (çatal 10) · ön çekme dudağı · eleman ve robot alma dizisi. Kap v26 (Picnic tipi) üzerine; dış 14×68 değişmedi.
import io, math, xml.dom.minidom
W, H = 1460, 1080
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
def leader(x1,y1,x2,y2,c='#999'): ln(x1,y1,x2,y2,.6,c,'2,2')
def f1(v): return ('%.1f' % v).replace('.',',')

GRN, RED, BLU, GRY, AMB, PUR = '#1d7a4f', '#c0392b', '#1a49b8', '#666', '#b7791f', '#6b4fa8'
PC, MAT, POM, STEEL, LIGHT, RAILC, NOSE = '#dbeeff', '#e9dfa8', '#f4f4f4', '#cfd8dc', '#f7f6f2', '#9e9e9e', '#cfe0f5'

# ---------------- GEOMETRİ (cm) — v26 + v27 değişiklikleri ----------------
WK, LK = 14.0, 68.0
ET = 0.5; PLATE = 0.4
KZ_H, KZ_W, CEP_W, CEP_H = 2.0, 3.0, 2.0, 1.4
RX = 5.0                                 # kızak merkezleri ±5 (v26: ±4) → çatal aralığı 10
HTOT = 26.0
Wi = WK-2*ET; Li = LK-2*ET
Hi = HTOT-KZ_H-PLATE-ET                  # 23,1
RT = 3.8; HEL_D, HEL_MIL, HEL_P = 7.0, 2.0, 5.0
ZH = 14.0; RW = Wi/2; RR = RW-0.8; RODS=(RR,RR*0.75,RR*0.5,RR*0.25); ROD_D=0.6
ZC = ZH-math.sqrt(RW**2-RT**2)
TUBE0 = 62.0                             # hazne ön duvarı / kapalı boru başı (arka iç yüzden)
CH0, CH1, CHW = 62.0, 67.0, 4.5          # ağız y aralığı · eni
HEL_L = 66.0
ZB = -ET-PLATE                           # plaka altı = kızak üstü (−0,9)
ZK = ZB-KZ_H                             # kızak altı = kap alt düzlemi (−2,9)
FLAP_T = 0.3; FLAP_L = CH1-CH0
LEVER = 1.8
LIP = 1.5
STUD_D = 0.8; STUD_X = 3.0
assert CHW/2+0.25 <= STUD_X-STUD_D/2 and STUD_X+STUD_D/2 <= RX-KZ_W/2-0.1, 'pim sığmıyor'
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
AREA=alan(PROF); HAVA=2.0
LH = TUBE0-ET
V_HEL=(math.pi*(HEL_MIL/2)**2*HEL_L + (HEL_L/HEL_P)*math.pi*((HEL_D/2)**2-(HEL_MIL/2)**2)*0.6)/1000
V_TAR=(4*math.pi*(ROD_D/2)**2*58 + 2*math.pi*1.5**2*1.2)/1000
VOL_BRUT=AREA*LH/1000
VOL_USE=(AREA-Wi*HAVA)*LH/1000 - V_HEL*LH/HEL_L - V_TAR
DENS={'KAŞAR':0.41,'KIYMA':0.60,'SUCUK':0.55,'KUŞBAŞI':0.60}
CAP={k:VOL_USE*v for k,v in DENS.items()}
GUNLUK={'KAŞAR':4.5,'KIYMA':8.6/3,'SUCUK':8.4/7,'KUŞBAŞI':4.3/3}
DOLUM={'KAŞAR':CAP['KAŞAR'],'KIYMA':min(8.6,CAP['KIYMA']),'SUCUK':min(8.4,CAP['SUCUK']),'KUŞBAŞI':min(4.3,CAP['KUŞBAŞI'])}
GUN={k:DOLUM[k]/GUNLUK[k] for k in DOLUM}
PERIM=sum(math.dist(PROF[i],PROF[i+1]) for i in range(len(PROF)-1))
M_PC=((PERIM*LH + 2*AREA + Wi*Li*0.9)*ET + Wi*Li*PLATE + 2*Li*(KZ_W*KZ_H-CEP_W*CEP_H) + 2*math.pi*(RT+ET)*(Li-LH)*ET)*1.2/1000
M_HEL=V_HEL*1.41+0.1; M_TAR=V_TAR*7.9+0.3; M_KAPAK=0.25; M_BOS=M_PC+M_HEL+M_TAR+M_KAPAK
CATAL=2.0
KOL={k:DOLUM[k]+M_BOS+CATAL for k in DOLUM}
FLAP_HANG = FLAP_L+FLAP_T
PIDE_TOP = 10.0
assert PIDE_TOP-FLAP_HANG >= 2.5, 'kapak pideye yakın'
STUD_TRAVEL = LEVER*math.pi/2
STUD_Y = CH1-STUD_TRAVEL-STUD_D/2
DEG = round(7/GUN['KAŞAR'])+math.ceil(7/GUN['KIYMA'])+math.ceil(7/GUN['SUCUK'])+math.ceil(7/GUN['KUŞBAŞI'])
MAXKAP = max(DOLUM.values())+M_BOS

o.append('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">' % (W,H,W,H))
rc(0,0,W,H,0,0,'none',None,'#fff')
tx(30,40,'AUTOKITCH — TOPPING v27 (5 Eyl 2026) — KAP AĞZI · KAPAK · TUTMA: kapalı boru ucu + tek ağız 5×4,5 · yaylı menteşeli kapak, raf pimiyle açılır · kızaklar ±5 (çatal 10) · ön çekme dudağı · eleman ve robot alma dizisi',14,'start','bold')
tx(30,62,'Kemal' + AP + 'in dört sorusu: ① kaşar altta tek alandan nasıl çıkıyor? ② dolapta altından dökülmez mi? ③ robot nasıl alır? ④ eleman raftan nasıl alır? — Kap v26 (Picnic tipi) üzerine; dış 14×68, kızakla 26 → kat 27, istasyon yerleşimi ve HAT v47 değişmedi. Kapta elektrik yok; tek hareketli parça: menteşeli kapak + burulma yayı.',9,'start','','#444')
ln(30,74,W-30,74,.8,'#999')

# ================= A · BOY KESİT (ön uç) =================
XA,YA,WA,HA_ = 40,90,720,460
rc(XA,YA,WA,HA_,1.4,4,'#111',None,'#fcfbf8')
tx(XA+14,YA+22,'A · BOY KESİT, ön uç (y 40–68): hazne 0,5–62 · KAPALI BORU 62–67 · AĞIZ altta · KAPAK menteşesi ön kenarda',10,'start','bold')
KL=7.6; y_lo=40.0
bx=XA+30; bz=YA+64+KL*Hi
XL=lambda y: bx+KL*(y-y_lo); ZL=lambda z: bz-KL*z
# gövde
rc(XL(y_lo),ZL(Hi),KL*(LK-y_lo),KL*(Hi+ET+PLATE),1.2,1,'#111',None,PC)
rc(XL(y_lo),ZL(Hi),KL*(TUBE0-y_lo),KL*Hi,.9,0,'#333',None,'#fff')
rc(XL(y_lo),ZL(Hi-HAVA),KL*(TUBE0-y_lo),KL*(Hi-HAVA),0,0,'none',None,MAT)
rc(XL(TUBE0),ZL(2*RT),KL*(Li+ET-TUBE0),KL*(2*RT),.9,0,'#333',None,'#fff')             # boru (Ø7,6)
rc(XL(TUBE0),ZL(Hi),KL*(Li+ET-TUBE0),KL*(Hi-2*RT),.6,0,'#333',None,NOSE)                # burun (dolu PC)
tx(XL(64.7),ZL(17),'BURUN',5,'middle','bold','#5b7ea6'); tx(XL(64.7),ZL(15),'dolu PC',4.2,'middle','','#5b7ea6')
# dudak
poly([(XL(LK),ZL(Hi+ET)),(XL(LK+LIP),ZL(Hi+ET)),(XL(LK+LIP),ZL(Hi-1.2)),(XL(LK+0.4),ZL(Hi-1.2)),(XL(LK+0.4),ZL(Hi-3.0)),(XL(LK),ZL(Hi-3.0))],1.1,'#111',PC)
# plaka + kızak (yandan)
rc(XL(y_lo),ZL(-ET),KL*(LK-y_lo),KL*PLATE,.8,0,'#111',None,NOSE)
rc(XL(y_lo),ZL(ZB),KL*(LK-y_lo),KL*KZ_H,1,0,'#111',None,'#d0d7de'); tx(XL(50),ZL(ZB-1.0)+2,'kızak (arka düzlemde, ±5) · içi çatal cebi',4.4,'middle','','#333')
# ağız oluğu
rc(XL(CH0),ZL(-ET),KL*(CH1-CH0),KL*(ET+PLATE+KZ_H-FLAP_T),0,0,'none',None,'#fff')
ln(XL(CH0),ZL(0),XL(CH0),ZL(ZK+FLAP_T),1,'#111'); ln(XL(CH1),ZL(0),XL(CH1),ZL(ZK+FLAP_T),1,'#111')
tx(XL((CH0+CH1)/2),ZL(-1.5)+2,'AĞIZ',4.6,'middle','bold',GRN)
# helezon
ln(XL(y_lo),ZL(RT),XL(ET+HEL_L),ZL(RT),KL*HEL_MIL,GRN)
y0=ET
while y0+HEL_P<=ET+HEL_L+0.01:
    if y0>=y_lo: pline([(XL(y0),ZL(RT+HEL_D/2)),(XL(y0+HEL_P/2),ZL(RT-HEL_D/2)),(XL(y0+HEL_P),ZL(RT+HEL_D/2))],1.1,GRN)
    y0+=HEL_P
# kapak kapalı + menteşe
rc(XL(CH0-0.3),ZL(ZK+FLAP_T),KL*(FLAP_L+0.3),KL*FLAP_T,1.2,0,RED,None,'#f7d7d7')
ci(XL(CH1),ZL(ZK+FLAP_T/2),2.8,1.2,RED,None,'#fff')
# kapak açık (kesikli)
rc(XL(CH1)-KL*FLAP_T/2,ZL(ZK+FLAP_T/2),KL*FLAP_T,KL*FLAP_L,1,0,RED,'4,3','none')
arr(XL(CH0+2.5),ZL(ZK-0.6),XL(CH0+2.5),ZL(ZK-4.0),GRN,1.4)
# kol + pim
ln(XL(CH1),ZL(ZB),XL(CH1),ZL(ZB-LEVER),2.2,RED)
ci(XL(STUD_Y),ZL(ZB-LEVER+0.3),KL*STUD_D/2,1,'#333',None,'#bbb')
# tepsi düzlemi + pide üstü
ln(XL(y_lo),ZL(ZK-12),XL(LK+1.5),ZL(ZK-12),1.4,BLU); ln(XL(y_lo),ZL(ZK-10),XL(LK+1.5),ZL(ZK-10),.8,'#8a6a3a','3,2')
# istasyon: klape 4 (y 80–84 → kap koordinatında 70–74)
rc(XL(LK+2.0),ZL(Hi+ET+0.8),KL*4,KL*(Hi+ET+0.8-ZK+12.5),.8,0,BLU,None,'#dfe7fb'); tx(XL(LK+4),ZL(Hi/2),'klape 4',4.4,'middle','',BLU)
# ölçüler
dim(XL(TUBE0),ZL(Hi+ET+1.4),XL(CH1),ZL(Hi+ET+1.4),'boru 5',5,0,GRN)
dim(XL(y_lo),ZL(Hi+ET+3.2),XL(TUBE0),ZL(Hi+ET+3.2),'hazne (arka 40 cm kesildi) — 0,5 → 62 = 61,5',4.8,0,GRY)
# LEGEND (sağ sütun, kılavuz çizgili)
LX=XL(LK+7.5)
def leg(zsrc, ysrc, ztxt, s, col, fw=''):
    leader(XL(ysrc),ZL(zsrc),LX-4,ZL(ztxt)-2,col); tx(LX,ZL(ztxt),s,5,'start',fw,col)
leg(Hi-0.6, LK+LIP, Hi+1.5, 'ÖN ÇEKME DUDAĞI 1,5 × 3: parmak takar, kabı öne çeker → kap üstte 69,5 (STORE iç 70 ✓, klape 80 ✓)', GRN, 'bold')
leg(RT, ET+HEL_L, 8.5, 'helezon Ø7 · son hatve borunun içinde → malzemeyi tek ağza iter · durunca borudaki malzeme kalır', GRN)
leg(RT, 64.5, 5.5, 'KAPALI BORU 62–67: yatağın devamı, üstü kapalı → helezon dönmeden malzeme inmez', '#5b7ea6')
leg(-1.5, 64.5, 2.5, 'AĞIZ 5 × 4,5 (küp 1,5 → ≥ 4,5 ✓), plakayı ve boşluğu geçer', GRN, 'bold')
leg(ZK+FLAP_T/2, CH1, -0.6, 'KAPAK 5,1 × 5 × 0,3 PC · menteşe ön kenarda (y 67) · burulma yayı KAPALI tutar', RED, 'bold')
leg(ZB-LEVER+0.3, STUD_Y, -3.2, 'RAF PİMİ Ø8 (yalnız TOPPING katında): kap son 3 cm girerken kola dayanır → kapak 90° sarkar', RED)
leg(ZB-LEVER, CH1, -5.6, 'kol 1,8 (x +3), plaka altındaki 2 cm boşlukta — alt düzlemden hiçbir şey sarkmaz (STORE/ALT rafında güvenli)', '#333')
leg(ZK-3.0, CH1, -8.0, 'AÇIK kapak (kesikli) %s sarkar · pide üstü kap altından 10 → pay %s ✓' % (f1(FLAP_HANG),f1(PIDE_TOP-FLAP_HANG)), RED)
leg(ZK-12, LK+1.5, -10.6, 'tepsi Ø32 düzlemi: kat 1 → 158 (kap altı 170) · pide üstü 160', BLU)
py=YA+380
py=para(XA+14,py,'① TEK ALANDAN ÇIKIŞ: hazne y 62' + AP + 'de biter, yatak Ø7,6 boru olarak 5 cm sürer; helezonun son hatvesi borunun içinde. Malzeme yalnız helezon dönünce borudan geçip alttaki tek ağızdan düşer; durunca yerçekimiyle inebileceği açık yol yok (klasik vidalı besleyici). Gramaj = devir: ≈ 50 g kaşar / devir, adım motoru.',175,5.6,'#111','bold')
py=para(XA+14,py+1,'② DÖKÜLMEZ: ağzın altında menteşeli kapak, yay kapalı tutar (STORE, ALT, elemanın elinde, taşımada, üst kapak da takılı). Yalnız TOPPING katında raflar arasındaki sabit pim, kap arka duvara dayanmadan önceki son 3 cm' + AP + 'de kolu iter → kapak 90° sarkar, ağız açılır. Kap çekilince yay kapatır. Kapta elektrik yok.',175,5.6,'#333')

# ================= B · ÖN KESİT y 64 =================
XB,YB,WB,HB = 780,90,320,460
rc(XB,YB,WB,HB,1.4,4,'#111',None,'#fcfdff')
tx(XB+14,YB+22,'B · ÖN KESİT y 64 — boru, ağız, kızaklar ±5, pim',10,'start','bold')
K=9.0; ax=XB+158; az=YB+58+K*Hi
X=lambda c: ax+K*c; Z=lambda c: az-K*c
rc(X(-WK/2),Z(Hi+ET),K*WK,K*(Hi+2*ET+PLATE),1.2,1,'#111',None,NOSE)
ci(X(0),Z(RT),K*RT,1,'#333',None,'#fff')
ci(X(0),Z(RT),K*HEL_D/2,1.1,GRN,None,POM); ci(X(0),Z(RT),K*HEL_MIL/2,.9,GRN,None,'#ddd')
for a in range(0,360,45): ln(X(HEL_MIL/2*math.cos(math.radians(a))),Z(RT+HEL_MIL/2*math.sin(math.radians(a))),X(HEL_D/2*0.95*math.cos(math.radians(a))),Z(RT+HEL_D/2*0.95*math.sin(math.radians(a))),.6,GRN)
zc_=RT-math.sqrt(RT**2-(CHW/2)**2)
rc(X(-CHW/2),Z(zc_),K*CHW,K*(zc_-(ZK+FLAP_T)),1,0,'#111',None,'#fff')
rc(X(-CHW/2-0.3),Z(ZK+FLAP_T),K*(CHW+0.6),K*FLAP_T,1.2,0,RED,None,'#f7d7d7')
for sx_ in (-RX,RX):
    rc(X(sx_-KZ_W/2),Z(ZB),K*KZ_W,K*KZ_H,1.1,0,'#111',None,'#d0d7de'); rc(X(sx_-CEP_W/2),Z(ZB-0.3),K*CEP_W,K*CEP_H,.8,0,'#555',None,'#fff')
    rc(X(sx_-KZ_W/2-0.5),Z(ZK)-K*0.2,K*(KZ_W+1),K*0.2,.8,0,'#555',None,RAILC)
    xo = sx_-KZ_W/2-0.5 if sx_<0 else sx_+KZ_W/2+0.3
    rc(X(xo),Z(ZK+0.8)-K*0.2,K*0.2,K*1.0,.8,0,'#555',None,RAILC)
ln(X(STUD_X),Z(ZB),X(STUD_X),Z(ZB-LEVER),2.2,RED)
rc(X(STUD_X-STUD_D/2),Z(ZK)-K*0.2,K*STUD_D,K*(ZB-LEVER+0.6-ZK)+K*0.2,1,1,'#333',None,'#bbb')
rc(X(-RX-KZ_W/2-0.5),Z(ZK)-K*0.2,K*(2*RX+KZ_W+1),K*0.2,.6,0,'#555','3,2','none')
# etiketler (kısa, yanlara)
tx(X(-WK/2)-6,Z(RT)+2,'boru Ø7,6',4.6,'end','','#333'); leader(X(-RT),Z(RT),X(-WK/2)-4,Z(RT))
tx(X(WK/2)+6,Z(RT+1.5)+2,'helezon Ø7 (POM)',4.6,'start','',GRN)
tx(X(WK/2)+6,Z(0.5)+2,'oluk 4,5',4.6,'start','',GRN)
tx(X(WK/2)+6,Z(ZK+0.2)+2,'kapak (kapalı)',4.6,'start','bold',RED)
tx(X(-WK/2)-6,Z(ZB-1)+2,'kızak 3×2',4.6,'end','','#333'); tx(X(-WK/2)-6,Z(ZB-2.2)+2,'L raf',4.4,'end','',GRY)
tx(X(WK/2)+6,Z(ZB-0.2)+2,'kol (x +3)',4.6,'start','bold',RED)
tx(X(WK/2)+6,Z(ZK-1.3)+2,'pim Ø8 → çapraz çubukta',4.6,'start','','#333')
dim(X(-WK/2),Z(Hi+ET+1.4),X(WK/2),Z(Hi+ET+1.4),'14',5.4)
dim(X(-RX),Z(ZK-2.2),X(RX),Z(ZK-2.2),'çatal aralığı 10 (±5)',5,0,GRN)
dim(X(-CHW/2),Z(2*RT+1.0),X(CHW/2),Z(2*RT+1.0),'4,5',4.8,0,GRN)
tx(X(0),Z(Hi-4),'burun: dolu PC',4.6,'middle','','#5b7ea6')
para(XB+14,YB+335,'Pim, oluk (±2,25) ile kızak iç yüzü (±3,5) arasındaki 1,25 cm' + AP + 'lik şeride oturur. Kapak menteşe mili oluğun ön kenarı boyunca uzanır, x +3' + AP + 'te kola bağlanır. Çapraz çubuk (pimi taşır) yalnız TOPPING katlarında L raflar arasındadır; STORE −18 ve ALT raflarında yok → kapak hep kapalı.',74,5.4,'#333')
para(XB+14,YB+415,'Kızak ±5: kap eni 14 içinde (dış kenar 6,5 ≤ 7). L raflar da ±5 — 18 çift raf ve çatal aralığı 10 buna göre.',74,5.4,GRN,'bold')

# ================= C · ALTTAN (ön uç) =================
XC,YC,WC,HC = 1120,90,300,460
rc(XC,YC,WC,HC,1.4,4,'#111',None,'#fcfdff')
tx(XC+14,YC+22,'C · ALTTAN GÖRÜNÜM (ön 30 cm)',10,'start','bold')
KP=8.4; y_c0=38.0; cx0=XC+22; cy0=YC+70
XP=lambda y: cx0+KP*(y-y_c0); YP=lambda x: cy0+KP*(WK/2+x)
rc(XP(y_c0),YP(-WK/2),KP*(LK-y_c0),KP*WK,1.2,1,'#111',None,NOSE)
rc(XP(y_c0),YP(-RX+KZ_W/2),KP*(LK-y_c0),KP*(2*RX-KZ_W),0,0,'none',None,'#eef3f8')
for sx_ in (-RX,RX):
    rc(XP(y_c0),YP(sx_-KZ_W/2),KP*(LK-y_c0),KP*KZ_W,1,0,'#111',None,'#d0d7de'); rc(XP(y_c0),YP(sx_-CEP_W/2),KP*(LK-y_c0),KP*CEP_W,.6,0,'#555','3,2','none')
tx(XP(48),YP(-RX)+2,'kızak / çatal cebi',4.2,'middle','','#333'); tx(XP(48),YP(RX)+2,'kızak / çatal cebi',4.2,'middle','','#333')
tx(XP(50),YP(0)+2,'boşluk (plaka altı, 2 cm)',4.2,'middle','',GRY)
rc(XP(CH0),YP(-CHW/2),KP*(CH1-CH0),KP*CHW,1.2,0,GRN,None,'#eaf6ee'); tx(XP((CH0+CH1)/2),YP(0)+2,'AĞIZ',4.6,'middle','bold',GRN)
rc(XP(CH0-0.3),YP(-CHW/2-0.3),KP*(FLAP_L+0.3),KP*(CHW+0.6),1.2,0,RED,None,'none')
ln(XP(CH1),YP(-CHW/2-0.6),XP(CH1),YP(STUD_X+0.3),1.8,RED)
rc(XP(CH1-0.2),YP(STUD_X-0.2),KP*0.4,KP*0.4,1,0,RED,None,RED)
ci(XP(STUD_Y),YP(STUD_X),KP*STUD_D/2,1,'#333',None,'#bbb')
ln(XP(TUBE0),YP(-WK/2),XP(TUBE0),YP(WK/2),.8,'#5b7ea6','3,2')
tx(XP(LK)+3,YP(0)+2,'ÖN',4.4,'start','bold',GRY)
# etiketler altta, kılavuzlu
ly0=YP(WK/2)+18
leader(XP(CH1),YP(-CHW/2-0.6),XP(CH1),ly0-4); tx(XP(CH1),ly0,'menteşe mili (ön kenar)',4.4,'middle','bold',RED)
leader(XP(CH1),YP(STUD_X),XP(CH1)+20,ly0+12); tx(XP(CH1)+22,ly0+14,'kol',4.4,'start','bold',RED)
leader(XP(STUD_Y),YP(STUD_X),XP(STUD_Y)-22,ly0+12); tx(XP(STUD_Y)-24,ly0+14,'pim',4.4,'end','bold','#333')
leader(XP(TUBE0),YP(WK/2),XP(TUBE0),ly0+26); tx(XP(TUBE0),ly0+30,'hazne | burun (y 62)',4.2,'middle','','#5b7ea6')
para(XC+14,YC+250,'Kızaklar tam boy; aradaki 2 cm boşluk plakanın altında ve önden açık: kol ve pim burada çalışır. Kapak kapalıyken kabın alt düzleminden aşağı hiçbir şey sarkmaz → ALT ve STORE raflarında kap düz oturur, pim yoksa kapak açılmaz.',60,5.4,'#333')
para(XC+14,YC+335,'Pim, kap kenetliyken ağız merkezinden %s cm arkada (y %s), x +3. Kap son 3 cm girerken kol pime dayanır ve 90° döner; kap 3 cm geri çekilince yay kapatır, ağız ancak ondan sonra rafın önüne çıkar.' % (f1((CH0+CH1)/2-STUD_Y),f1(STUD_Y)),60,5.4,AMB)

# ================= D · ELEMAN =================
XD,YD,WD,HD = 40,570,720,230
rc(XD,YD,WD,HD,1.4,4,'#111',None,'#fff')
tx(XD+14,YD+22,'D · ELEMAN KABI NASIL ALIR (STORE −18 katı / ALT rafı) — alt kapak kapalı, üst kapak takılı, dolu ≈ %s kg' % f1(MAXKAP),10,'start','bold')
KE=1.55
def eleman_cell(x0,y0,step,cap):
    xw=x0+14; ln(xw,y0-56,xw,y0+6,3,'#555'); ln(xw,y0,xw+KE*76,y0,1.6,'#555'); tx(xw+KE*38,y0+8,'L raf (kabin)',3.9,'middle','',GRY)
    dx_=(0,KE*30,KE*55)[step-1]; dz=(0,0,-24)[step-1]
    kx=xw+dx_
    rc(kx,y0-KE*2+dz,KE*68,KE*2,.8,0,'#111',None,'#d0d7de')                                  # kızak
    rc(kx,y0-KE*26+dz,KE*68,KE*24,1,1,'#111',None,PC)                                        # kap
    rc(kx,y0-KE*27.5+dz,KE*68,KE*1.5,.8,1,BLU,None,'#dfe7fb')                                # üst kapak
    poly([(kx+KE*68,y0-KE*26+dz),(kx+KE*69.5,y0-KE*26+dz),(kx+KE*69.5,y0-KE*23+dz),(kx+KE*68,y0-KE*23+dz)],.9,'#111',PC)   # dudak
    rc(kx+KE*62,y0-KE*0.5+dz,KE*5,KE*0.5,.8,0,RED,None,RED)                                  # alt kapak kapalı
    rc(kx-KE*2,y0-KE*7+dz,KE*2,KE*5,.8,1,GRN,None,POM)                                      # topuz (arka)
    h1=(kx+KE*71,y0-KE*24.5+dz)
    ci(h1[0],h1[1],4,1.2,AMB,None,'#fde9c9')
    if step==1: arr(h1[0]+8,h1[1],h1[0]+26,h1[1],AMB,1.3)
    if step>=2: ci(kx+KE*14,y0+4+dz,4,1.2,AMB,None,'#fde9c9')
    if step==3: arr(kx+KE*34,y0+14,kx+KE*34,y0-4,AMB,1.3)
    para(x0+4,y0+22,cap,52,4.6,'#333','bold' if step==1 else '')
caps=('1 · Parmak dudağa: kabı öne çek. Kızaklar L rafta kayar, kilit yok; alt kapak yayla kapalı.',
      '2 · Yarısı çıkınca ikinci el kabın altına (arka yarı). Topuz arkada, ele gelmez.',
      '3 · Kaldır, yatay taşı: önde dudak, arkada alttan tutuş. Koyma: rafın önüne oturt, dudaktan it, dayanınca bırak.')
for j in range(3): eleman_cell(XD+14+j*236,YD+120,j+1,caps[j])
para(XD+14,YD+200,'Eleman haftada 1: donmuş kıyma/kuşbaşı kaplarını STORE −18 katına, kaşar yedekleri + sucuğu ALT rafına iter; boşları alır. Araç yok, kilit yok, elektrik yok; 13 kg tek kişi.',175,5.4,GRY)

# ================= E · ROBOT =================
XE,YE,WE,HE = 780,570,640,230
rc(XE,YE,WE,HE,1.4,4,'#111',None,'#fff')
tx(XE+14,YE+22,'E · ROBOT KABI NASIL ALIR — ÇATAL (v25), aralık 8 → 10',10,'start','bold')
KR=1.15
def robot_cell(x0,y0,step,cap):
    xw=x0+150; rc(xw,y0-KE*30,6,KE*30+8,1,0,'#555',None,'#ccc'); ln(x0+50,y0,xw,y0,1.6,'#555')
    dx_=(0,0,KR*60)[step-1]; dz=(0,-3,-3)[step-1]
    kx=xw-KR*68-dx_
    rc(kx,y0-KR*2+dz,KR*68,KR*2,.8,0,'#111',None,'#d0d7de'); rc(kx,y0-KR*26+dz,KR*68,KR*24,1,1,'#111',None,PC)
    rc(kx+KR*62,y0-KR*0.5+dz,KR*5,KR*0.5,.8,0,RED,None,RED if step==3 else '#f7d7d7')
    ci(xw-KR*4.2,y0-2,1.6,.8,'#333',None,'#bbb')                                              # pim (rafta)
    ty=y0-KR*1+dz
    ln(kx,ty,kx+KR*50,ty,2,GRN); rc(kx-3,ty-8,3,10,1,0,'#333',None,'#bbb'); ci(kx-8,ty-3,3.2,1,'#333',None,'#eee'); ln(kx-11,ty-3,x0+4,ty-3,3,'#999')
    if step==1: arr(kx-40,ty-18,kx-8,ty-18,AMB,1.2)
    if step==2: arr(kx-30,ty-4,kx-30,ty-16,AMB,1.2)
    if step==3: arr(kx+40,ty-24,kx-6,ty-24,AMB,1.2)
    para(x0+4,y0+18,cap,44,4.6,'#333','bold' if step==1 else '')
rcaps=('1 · GİR: tırnaklar (2 lama 16×12, 50 cm, aralık 10) kızak ceplerine önden girer.',
       '2 · KALDIR 0,5: kap L raftan ayrılır, cep tavanı tırnağa oturur.',
       '3 · ÇEK 70: kap 3 cm çıkar çıkmaz yay kapağı kapatır; 5° yatık taşı. Koyma tersi: sür → son 3 cm kol pime, kapak açılır → topuz sokete → indir → çek.')
for j in range(3): robot_cell(XE+14+j*208,YE+110,j+1,rcaps[j])
para(XE+14,YE+200,'Değişen: kızak merkezleri ±4 → ±5 (ağız borusu araya sığsın) → çatal aralığı 10, TOPPING/ALT/STORE L rafları ±5. En ağır kap %s kg + çatal 2 = %s kg → ⑦ aynı sınıf.' % (f1(MAXKAP),f1(max(KOL.values()))),150,5.4,GRN,'bold')

# ================= F · KAPASİTE · PARÇALAR · KONTROL =================
XF,YF,WF,HF = 40,820,1380,235
rc(XF,YF,WF,HF,1.4,4,'#111',None,'#fcfdff')
tx(XF+14,YF+22,'F · KAPASİTE (boru ucu hazneyi 5 cm kısalttı) · PARÇALAR · KONTROL',10,'start','bold')
hdr=['malzeme','kapasite (%s L)' % f1(VOL_USE),'dolum','gün','değişim/hafta','dolu kap','kol (+çatal 2)']
cx_=[XF+14,XF+110,XF+230,XF+320,XF+400,XF+500,XF+590]
for i,h in enumerate(hdr): tx(cx_[i],YF+44,h,5.9,'start','bold',GRY)
ln(XF+12,YF+49,XF+690,YF+49,.8,'#bbb')
tbl=[('KAŞAR rende','%s kg' % f1(CAP['KAŞAR']),'%s (tam)' % f1(DOLUM['KAŞAR']),'%s (2 poz. %s)' % (f1(GUN['KAŞAR']),f1(2*GUN['KAŞAR'])),'%d' % round(7/GUN['KAŞAR'])),
     ('KIYMA kavrulmuş','%s kg' % f1(CAP['KIYMA']),'%s' % f1(DOLUM['KIYMA']),f1(GUN['KIYMA']),'%d' % math.ceil(7/GUN['KIYMA'])),
     ('SUCUK küp','%s kg' % f1(CAP['SUCUK']),'%s' % f1(DOLUM['SUCUK']),f1(GUN['SUCUK']),'%d' % math.ceil(7/GUN['SUCUK'])),
     ('KUŞBAŞI sote','%s kg' % f1(CAP['KUŞBAŞI']),'%s' % f1(DOLUM['KUŞBAŞI']),f1(GUN['KUŞBAŞI']),'%d' % math.ceil(7/GUN['KUŞBAŞI']))]
for i,(nm,cap,dol,gun,deg) in enumerate(tbl):
    yy=YF+64+i*14; k=nm.split(' ')[0]
    for j,v in enumerate((nm,cap,dol,gun,deg,f1(DOLUM[k]+M_BOS),f1(KOL[k]))):
        tx(cx_[j],yy,v,5.8,'start','bold' if j==0 else '','#111' if j==0 else (RED if (j==6 and KOL[k]>12.5) else '#333'))
para(XF+14,YF+128,'v26 → v27: kullanılabilir 14,0 → %s L (hazne 67 → 61,5; taban plakası 0,4). Kaşar %s gün (2 poz. %s) → robot haftada ≈ %d kap değişimi (v26: 12). Boş kap %s kg (PC %s + helezon %s + tarak %s + kapak 0,25).' % (f1(VOL_USE),f1(GUN['KAŞAR']),f1(2*GUN['KAŞAR']),DEG,f1(M_BOS),f1(M_PC),f1(M_HEL),f1(M_TAR)),128,5.5,'#333')
para(XF+14,YF+160,'Kaşar için seçenek: kat 2' + AP + 'deki boş pozisyona 3. kaşar kabı → 3 pozisyon %s gün, değişim haftada %d yerine %d. Kemal kararı.' % (f1(3*GUN['KAŞAR']),round(7/GUN['KAŞAR']),round(7/(3*GUN['KAŞAR'])*2)),128,5.5,AMB)
px_=XF+720; pyy=YF+44
tx(px_,pyy,'YENİ / DEĞİŞEN PARÇALAR',6.2,'start','bold','#111'); pyy+=12
for a_,b_ in [('Kapta','menteşeli kapak PC 5,1×5×0,3 + paslanmaz mil Ø4 + burulma yayı + kol 1,8 (x +3) · ön çekme dudağı 1,5×3 (kalıpta) · taban plakası 0,4 + kızaklar ±5 · burun: boru üstü dolu PC, ön omurga pim yatağı'),
              ('Kabinde','TOPPING 6 pozisyonda raflar arası çapraz çubuk + pim Ø8 (kap kenetliyken ağız merkezinin %s cm arkasında, x +3) · L raflar ±5 (18 çift) · yaylı soket ×2/kap aynı' % f1((CH0+CH1)/2-STUD_Y)),
              ('Robotta','çatal aralığı 10 (v25: 8) · dizi aynı: gir 50 → kaldır 0,5 → çek 70'),
              ('Elemanda','dudaktan çek → alttan tut → taşı; koyarken it, dayanınca bırak · araç yok')]:
    tx(px_,pyy,a_,5.6,'start','bold','#111'); pyy=para(px_+56,pyy,b_,112,5.3,'#333')+2
pyy=para(px_,pyy+2,'KONTROL ✓ ağız 4,5 ≥ 3×küp 1,5 · boru Ø7,6 = yalak · kapak açık sarkma %s < pide payı 10 (pay %s) · pim şeridi 1,25 ≥ Ø0,8 · dudak: kap üstte 69,5 ≤ STORE iç 70, TOPPING 79,5 < klape 80 · kızak ±5 kap eni içinde (dış kenar 6,5 ≤ 7)' % (f1(FLAP_HANG),f1(PIDE_TOP-FLAP_HANG)),128,5.4,GRN,'bold')
pyy=para(px_,pyy+1,'AÇIK: burulma yayı kuvveti (−18' + AP + 'de donmuş parça kapağa yaslanırsa) · kapak contası gerekli mi · pim–kol hizası toleransı ±3 mm · gramaj prototipi',128,5.4,AMB)
tx(W-40,H-10,'AUTOKITCH · arastirma/3_TOPPING/ist3_topping_detay_v27 · 5 Eyl 2026',7,'end','',GRY)
o.append('</svg>')
svg=chr(10).join(o)
xml.dom.minidom.parseString(svg.encode('utf-8'))
out=r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\3_TOPPING\ist3_topping_detay_v27.svg"
io.open(out,'w',encoding='utf-8').write(svg)
print('yazildi + XML gecerli | kullanilabilir %.1f L · kasar %.1f kg %.2f gun · degisim %d · bos %.2f · kol max %.1f · stud_y %.1f' % (VOL_USE,CAP['KAŞAR'],GUN['KAŞAR'],DEG,M_BOS,max(KOL.values()),STUD_Y))
