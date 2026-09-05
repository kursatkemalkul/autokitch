# -*- coding: utf-8 -*-
# TOPPING v23 — TEK KAP TİPİ 16×54×24 (simetrik V, ağız ortada) · 3 kat × 2 kap = 6 pozisyon · üst teknik yok (elektrik arka duvar, soğutma ALT arkası)
# ALT 74 = 2 sıra × 4 beşik + evaporatör bandı · STORE −18 3/modül · pide Ø30, tepsi Ø32, spiral R 11 → süpürme 27 → kap merkezleri x 27 / 43
import io, math, xml.dom.minidom
W, H = 1460, 1560
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
def poly(pts,sw=1,c='#111',f='none',d=None,op=1):
    o.append('<polygon points="%s" fill="%s" fill-opacity="%s" stroke="%s" stroke-width="%s"%s stroke-linejoin="round"/>' % (' '.join('%.1f,%.1f'%p for p in pts),f,op,c,sw,(' stroke-dasharray="%s"'%d) if d else ''))
def elp(x,y,rx,ry,sw=1,c='#111',f='none',op=1,rot=0):
    o.append('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="%s" fill-opacity="%s" stroke="%s" stroke-width="%s" transform="rotate(%g %.1f %.1f)"/>' % (x,y,rx,ry,f,op,c,sw,rot,x,y))
def arr(x1,y1,x2,y2,c='#c0392b',w=1.4):
    ln(x1,y1,x2,y2,w,c); a=math.atan2(y2-y1,x2-x1)
    for s in (1,-1): ln(x2,y2,x2-8*math.cos(a-s*.42),y2-8*math.sin(a-s*.42),w,c)

GRN, RED, BLU, GRY, AMB, PUR = '#1d7a4f', '#c0392b', '#1a49b8', '#666', '#b7791f', '#6b4fa8'
KAS, DIG, PLATE, WALL, LIGHT, PE, MAT, ICE = '#f3efe4', '#e9eef7', '#dfe7fb', '#d9d9d9', '#f7f6f2', '#e8f0e8', '#e9dfa8', '#e3f2fb'
TH, RT = 55.0, 3.8
WK, LK, HK, ET = 16.0, 54.0, 24.0, 0.8          # kap dış ölçüleri, et kalınlığı
Wi, Hi, Li = WK-2*ET, HK-2*ET, LK-2*ET
def profil_sim(Wi,Hi,n=12):
    xc=Wi/2; t=math.radians(TH)
    pxl,pz = xc-RT*math.sin(t), RT-RT*math.cos(t)
    rise = pz + pxl*math.tan(t)
    pts=[(0,Hi),(0,rise),(pxl,pz)]
    a0=math.atan2(pz-RT,pxl-xc); a1=math.pi-a0 if False else (math.pi - a0)   # sağ teğet: simetrik
    # yay: a0 (sol teğet, ~ -145°) → -90° → sağ teğet (-35°)
    a_end = -math.pi - a0 if a0 < -math.pi/2 else a0
    a_start = a0; a_stop = -math.pi - a0
    for k in range(1,n+1):
        a = a_start + (a_stop - a_start)*k/n
        pts.append((xc+RT*math.cos(a), RT+RT*math.sin(a)))
    pts += [(Wi-pxl,pz),(Wi,rise),(Wi,Hi)]
    return pts, rise
def alan(pts):
    s=0
    for i in range(len(pts)):
        x1,z1=pts[i]; x2,z2=pts[(i+1)%len(pts)]; s+=x1*z2-x2*z1
    return abs(s)/2
PROF, RISE = profil_sim(Wi,Hi); AREA = alan(PROF); VOL = AREA*Li/1000
KG = {'KAŞAR':VOL*0.41,'SUCUK':VOL*0.55,'KIYMA':VOL*0.60,'KUŞBAŞI':VOL*0.60}
# yerleşim: 3 kat, her katta sol (x 19-35, merkez 27) + sağ (x 35-51, merkez 43)
XL0, XR0 = 19.0, 35.0
Z = {'alt':(0,74),'b3':(74,88),'k3':(88,115),'b2':(115,129),'k2':(129,156),'b1':(156,170),'k1':(170,197)}
POS = [('KAŞAR A','k1',XL0,'2,7 gün · robot'),('SUCUK','k1',XR0,'hafta · robot'),
       ('KAŞAR B','k2',XL0,'2,7 gün · robot'),('boş / kavurma','k2',XR0,'park · ileride'),
       ('KIYMA','k3',XL0,'3 gün · robot'),('KUŞBAŞI','k3',XR0,'3 gün · robot')]
WALLT, YF = 10, 4
S=3.0; c30=math.cos(math.radians(30)); X0,Y0 = 70, 120+217*S
def P(x,yb,z): return (X0+S*(x*c30+yb*c30), Y0+S*(x*0.5-yb*0.5-z))
def ipoly(pts3,sw=1,c='#111',f='none',d=None,op=1): poly([P(*p) for p in pts3],sw,c,f,d,op)
def iline(p1,p2,w=1,c='#111',d=None): a=P(*p1); b=P(*p2); ln(a[0],a[1],b[0],b[1],w,c,d)

o.append('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">' % (W,H,W,H))
rc(0,0,W,H,0,0,'none',None,'#fff')
tx(30,42,'AUTOKITCH — İSTASYON 3 · TOPPING v24 (5 Eyl 2026) — TEK KAP TİPİ 16×54×24 (simetrik, ağız ortada) · 3 kat × 2 = 6 pozisyon · üst teknik yok: elektrik arka duvarda, soğutma ALT arkasında · ALT 8 beşik · + ÜST GÖRÜNÜM · 70×197×84',15,'start','bold')
tx(30,66,'Pide Ø30 → tepsi Ø32 (R 16) + spiral R 11 (saçılma son 2 cm) = süpürme 27 → kap merkezleri x 27 / 43, kaplar duvara tam değer (pay 0). Sağ-sol ayna yok, her kap her yere; 16 kap tek kalıp. Kaşar küçük kapta: %.1f kg = %.2f gün, iki pozisyonla %.1f gün, robot değiştirir.' % (KG['KAŞAR'],KG['KAŞAR']/4.5,2*KG['KAŞAR']/4.5),9.5,'start','','#444')
ln(30,78,W-30,78,.8,'#999')

# ================= İZOMETRİK =================
tx(X0+60,Y0-217*S-14,'İZOMETRİK — dolap içi z 0-197 · 1:3,3',9,'start','bold')
zlo,zhi=0,197
for (a,b) in (((0,0,zlo),(0,0,zhi)),((70,0,zlo),(70,0,zhi)),((0,84,zlo),(0,84,zhi)),((70,84,zlo),(70,84,zhi)),
              ((0,0,zlo),(70,0,zlo)),((0,0,zlo),(0,84,zlo)),((0,0,zhi),(70,0,zhi)),((0,0,zhi),(0,84,zhi)),((70,0,zhi),(70,84,zhi)),((0,84,zhi),(70,84,zhi)),((70,0,zlo),(70,84,zlo))):
    iline(a,b,.7,'#bbb')
ipoly([(0,84-WALLT,zlo),(70,84-WALLT,zlo),(70,84-WALLT,zhi),(0,84-WALLT,zhi)],1,'#555',WALL,None,.9)
ipoly([(0,84-WALLT,zhi),(70,84-WALLT,zhi),(70,84,zhi),(0,84,zhi)],1,'#555','#c8c8c8',None,.9)
ipoly([(70,84-WALLT,zlo),(70,84,zlo),(70,84,zhi),(70,84-WALLT,zhi)],1,'#555','#cfcfcf',None,.9)
# elektrik paneli arka duvarda (kesikli), z 100-190
ipoly([(8,84-WALLT+0.5,100),(62,84-WALLT+0.5,100),(62,84-WALLT+0.5,190),(8,84-WALLT+0.5,190)],.9,BLU,'#eef3ff','4,3',.7)
t=P(35,84-WALLT,190); tx(t[0],t[1]-6,'ELEKTRİK PANELİ (duvar içi): PLC · PSU · 6 sürücü',6,'middle','bold',BLU)
def motor(x,zf):
    for dz in (0,7):
        ipoly([(x-3,84-WALLT+1,zf+dz),(x+3,84-WALLT+1,zf+dz),(x+3,84-WALLT+8,zf+dz),(x-3,84-WALLT+8,zf+dz)],.9,BLU,'#dfe7fb','3,2',.9)
    iline((x-3,84-WALLT+1,zf),(x-3,84-WALLT+1,zf+7),.9,BLU,'3,2'); iline((x+3,84-WALLT+1,zf),(x+3,84-WALLT+1,zf+7),.9,BLU,'3,2')
for (ad,kz,x0,alt) in POS: motor(x0+WK/2, Z[kz][0])
for kz in ('k3','k2','k1'):
    z=Z[kz][0]
    ipoly([(0,0,z),(70,0,z),(70,84-WALLT,z),(0,84-WALLT,z)],1.2,BLU,PLATE,None,.85)
    ipoly([(0,0,z-2),(70,0,z-2),(70,0,z),(0,0,z)],1,BLU,'#c9d6f5',None,.9)
    ipoly([(70,0,z-2),(70,84-WALLT,z-2),(70,84-WALLT,z),(70,0,z)],1,BLU,'#c9d6f5',None,.9)
# ALT: soğutma grubu arkada (yb 58-74, z 0-52), evaporatör bandı z 52-74, beşikler 2 sıra × 4
ipoly([(2,58,0),(68,58,0),(68,58,62),(2,58,62)],1,'#555','#cfd8dc',None,.95)
ipoly([(2,58,62),(68,58,62),(68,74,62),(2,74,62)],1,'#555','#b0bec5',None,.95)
ipoly([(68,58,0),(68,74,0),(68,74,62),(68,58,62)],1,'#555','#c0cbd1',None,.95)
t=P(35,60,25); tx(t[0],t[1],'SOĞUTMA GRUBU',6.5,'middle','bold','#37474f'); tx(t[0],t[1]+9,'1/12 HP · 20 derin · hava plintten',5.4,'middle','','#37474f')
ipoly([(0,0,62),(70,0,62),(70,58,62),(0,58,62)],.9,'#7fb3d5',ICE,None,.6)
ipoly([(0,0,74),(70,0,74),(70,58,74),(0,58,74)],.9,'#7fb3d5',ICE,None,.5)
t=P(35,20,68); tx(t[0],t[1],'evaporatör + fan (12) · soğuk hava arka duvar kanalından katlara',5.6,'middle','',BLU)
ipoly([(0,0,0),(70,0,0),(70,0,8),(0,0,8)],1,'#555','#9e9e9e',None,.8); t=P(35,0,4); tx(t[0],t[1]+3,'plint ızgarası (hava)',5,'middle','','#fff')
for row,zf in ((0,8),(1,35)):
    for i in range(4):
        x0=1.2+i*17.2
        lab = [['park','park','çözülme kıyma','çözülme kuşbaşı'],['kaşar yedek','kaşar yedek','kaşar yedek','kaşar yedek']][row][i]
        dash = row==0 and i<2
        ipoly([(x0,YF,zf),(x0+WK,YF,zf),(x0+WK,YF,zf+3),(x0,YF,zf+3)],.9,'#555','#d8d4c8',None,.9)
        ipoly([(x0,YF,zf+3),(x0+WK,YF,zf+3),(x0+WK,YF+LK,zf+3),(x0,YF+LK,zf+3)],.8,'#555','#e4e0d4',None,.85)
        iline((x0+WK/2,YF+1,zf+3.2),(x0+WK/2,YF+LK-1,zf+3.2),1.2,BLU,'3,2')
        if not dash:
            ipoly([(x0+.5,YF+1,zf+3),(x0+WK-.5,YF+1,zf+3),(x0+WK-.5,YF+1,zf+3+HK-1),(x0+.5,YF+1,zf+3+HK-1)],.9,'#333',DIG,None,.85)
            ipoly([(x0+.5,YF+1,zf+3+HK-1),(x0+WK-.5,YF+1,zf+3+HK-1),(x0+WK-.5,YF+LK-1,zf+3+HK-1),(x0+.5,YF+LK-1,zf+3+HK-1)],.8,'#333',DIG,None,.7)
            ipoly([(x0+WK-.5,YF+1,zf+3),(x0+WK-.5,YF+LK-1,zf+3),(x0+WK-.5,YF+LK-1,zf+3+HK-1),(x0+WK-.5,YF+1,zf+3+HK-1)],.8,'#333','#dde3ee',None,.8)
        t=P(x0+WK/2,YF+2,zf+(13 if not dash else 7)); tx(t[0],t[1],lab,4.4,'middle','bold','#666' if dash else '#333')
t=P(0,-2,42); tx(t[0]-6,t[1]+8,'ALT 74 = plint 8 + 2 sıra × 27 beşik + evaporatör 12 · arkada soğutma',6.5,'end','bold',GRY)

def kap(ad,kz,x0,alt,empty=False):
    zf=Z[kz][0]; yb0=YF; x1=x0+WK
    box=[(x0,yb0,zf),(x1,yb0,zf),(x1,yb0,zf+HK),(x0,yb0,zf+HK)]
    back=[(x,yb0+LK,z) for (x,_,z) in box]
    col='#999' if empty else '#333'; d='3,2' if empty else None; f=LIGHT if empty else PE
    ipoly(back,1,col,f,d,.9)
    for i in range(4):
        a,b=box[i],box[(i+1)%4]; a2,b2=back[i],back[(i+1)%4]
        ipoly([a,b,b2,a2],.9,col,f,d,.85)
    xs=x0+WK/2
    if not empty:
        iline((xs,yb0+1,zf+ET+RT),(xs,yb0+LK-1,zf+ET+RT),2.2,GRN)
        for kk in range(int(LK/3.5)):
            y=yb0+2+kk*3.5
            if y>yb0+LK-2: break
            iline((xs-3,y,zf+ET+1),(xs+3,y,zf+ET+6),1.1,GRN)
        iline((xs,yb0+1,zf+ET+12),(xs,yb0+LK-1,zf+ET+12),1.5,PUR)
        for kk in range(int(LK/4)):
            y=yb0+2.5+kk*4
            if y>yb0+LK-2: break
            s=1 if kk%2==0 else -1; iline((xs,y,zf+ET+12),(xs,y,zf+ET+12+s*4),1,PUR)
    prof=[(x0+ET+x, zf+ET+z) for (x,z) in PROF]
    ipoly([(x,yb0,z) for (x,z) in prof],1.2,col,'#fff' if not empty else LIGHT,d,.55)
    ipoly([(x,yb0,z) for (x,_,z) in box],1.3,col,f,d,.35)
    if not empty:
        ipoly([(xs-2.5,yb0+1,zf-7),(xs+2.5,yb0+1,zf-7),(xs+2.5,yb0+5,zf-7),(xs-2.5,yb0+5,zf-7)],1,GRN,'#eaf6ee')
        for (dx,dy) in ((-2.5,1),(2.5,1),(2.5,5),(-2.5,5)): iline((xs+dx,yb0+dy,zf),(xs+dx,yb0+dy,zf-7),1,GRN)
        a=P(xs,yb0+3,zf-7); arr(a[0],a[1]+2,a[0],a[1]+14,GRN,1.3)
    iline((xs,yb0+LK,zf+ET+RT),(xs,84-WALLT,zf+ET+RT),1.2,BLU,'4,3')
    ipoly([(xs-2,yb0+LK,zf+ET+RT-2),(xs+2,yb0+LK,zf+ET+RT-2),(xs+2,yb0+LK+2,zf+ET+RT-2),(xs-2,yb0+LK+2,zf+ET+RT-2)],.9,BLU,'#dfe7fb')
    t=P(xs, yb0+LK*0.5, zf+HK+3); tx(t[0],t[1]-4,ad,7.5,'middle','bold','#999' if empty else '#111'); tx(t[0],t[1]+5,alt,5.2,'middle','','#666' if empty else '#333')
for (ad,kz,x0,alt) in POS: kap(ad,kz,x0,alt,empty=(ad.startswith('boş')))
for kz in ('b1','b2','b3'):
    z=Z[kz][0]+3
    cpt=P(27,YF+10,z); elp(cpt[0],cpt[1],16*S*0.95,16*S*0.5,1.2,BLU,'#dfe7fb',.9,-30)
    cpt2=P(27+16,YF+10,z); tx(cpt2[0]+10,cpt2[1],'tepsi Ø32 · %d cm' % (Z[kz][0]+2),5.6,'start','',BLU)
a=P(-6,-4,Z['k3'][0]+10); arr(a[0]-40,a[1]+24,a[0],a[1],AMB,1.6); tx(a[0]-44,a[1]+36,'ÖN (robot)',8,'middle','bold',AMB)
t=P(70,84-WALLT/2,zhi+4); tx(t[0]+6,t[1],'ARKA DUVAR 10 — motorlar + elektrik',7.5,'start','bold',BLU)
lx,ly=X0+300,Y0-217*S+8
for i,(col,lab) in enumerate(((GRN,'helezon (ortada) → ağız ortada'),(PUR,'tarak'),(BLU,'pençe / ara mil / motor'),('#37474f','soğutma ALT arkası, elektrik arka duvar'))):
    ln(lx,ly+i*13,lx+18,ly+i*13,2.2,col); tx(lx+24,ly+i*13+3,lab,6.5,'start','','#333')

# ================= ÖN KESİT =================
XC,YC = 560,100
tx(XC+88,YC-6,'ÖN KESİT (helezon hattı) 1:4',8.5,'middle','bold')
K=2.5
rc(XC,YC,K*70,K*197,1.8)
for ad,kz,col in (('KAT 1','k1','#fff'),('boşluk 1','b1','#eef3ff'),('KAT 2','k2','#fff'),('boşluk 2','b2','#eef3ff'),('KAT 3','k3','#fff'),('boşluk 3','b3','#eef3ff'),('ALT','alt','#f7f6f2')):
    z0,z1=Z[kz]; rc(XC,YC+K*(197-z1),K*70,K*(z1-z0),.7,0,'#111',None,col); tx(XC+K*70+4,YC+K*(197-(z0+z1)/2)+3,'%s %g'%(ad,z1-z0),5.4,'start','',GRY)
def kesit_kap(zf,x0,ad='',empty=False):
    Zc=lambda c: YC+K*(197-zf-c)
    col='#999' if empty else '#111'; d='3,2' if empty else None
    rc(XC+K*x0,Zc(HK),K*WK,K*HK,1,1,col,d,LIGHT if empty else PE)
    poly([(XC+K*(x0+ET+x),Zc(ET+z)) for (x,z) in PROF],1,col,LIGHT if empty else '#fff',d)
    if not empty:
        poly([(XC+K*(x0+ET+x),Zc(ET+min(z,20))) for (x,z) in PROF],0,'none',MAT)
        ci(XC+K*(x0+WK/2),Zc(ET+RT),K*3.5,1,GRN,'#fff'); ci(XC+K*(x0+WK/2),Zc(ET+12),K*4.5,.8,PUR,'none','3,2')
    if ad: tx(XC+K*(x0+WK/2),Zc(HK-5),ad,4.8,'middle','bold','#999' if empty else '#111')
for (ad,kz,x0,alt) in POS:
    kesit_kap(Z[kz][0],x0,ad,ad.startswith('boş'))
    if not ad.startswith('boş'): ln(XC+K*(x0+WK/2),YC+K*(197-Z[kz][0]),XC+K*(x0+WK/2),YC+K*(197-Z[kz][0]+6),1.6,GRN)
for kz in ('b1','b2','b3'):
    z=Z[kz][0]+3; o.append('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="#dfe7fb" stroke="%s" stroke-width="1"/>' % (XC+K*27,YC+K*(197-z),K*16,K*1.2,BLU))
    # süpürme bandı: sol x 0-54, sağ 16-70
    ln(XC,YC+K*(197-z)+5,XC+K*54,YC+K*(197-z)+5,.8,GRN,'3,2'); ln(XC+K*16,YC+K*(197-z)+8,XC+K*70,YC+K*(197-z)+8,.8,GRN,'3,2')
for row,zf in ((0,8),(1,35)):
    for i in range(4):
        x0=1.2+i*17.2; dash = row==0 and i<2
        rc(XC+K*x0,YC+K*(197-zf-3),K*WK,K*3,.9,1,'#555',None,'#d8d4c8')
        kesit_kap(zf+3,x0,'',dash)
rc(XC,YC+K*(197-74),K*70,K*12,.7,0,'#7fb3d5',None,ICE); tx(XC+K*35,YC+K*(197-67),'evaporatör + fan 12',4.8,'middle','',BLU)
rc(XC,YC+K*(197-8),K*70,K*8,.7,0,'#555',None,'#9e9e9e'); tx(XC+K*35,YC+K*(197-3),'plint ızgarası · arkada soğutma grubu',4.4,'middle','','#fff')
tx(XC+K*35,YC+K*197+14,'70',7,'middle','bold'); tx(XC+K*35,YC+K*197+26,'3 × (27+14) + 74 = 197 ✓',6.5,'middle','bold',GRN)
tx(XC+K*35,YC+K*197+38,'tepsi 158 / 117 / 76 cm · süpürme (kesikli yeşil) duvar içinde',5.6,'middle','',BLU)

# ================= KAP DETAYI + STORE =================
XD,YD = 760,100
rc(XD,YD,320,300,1.3,3,'#999',None,'#fcfdff')
tx(XD+160,YD+16,'TEK KAP 16×54×24 — simetrik kesit (iç 14,4×22,4)',7.5,'middle','bold')
KD=6.0
dx_,dz_ = XD+60, YD+40+KD*Hi
Xd=lambda c: dx_+KD*c; Zd=lambda c: dz_-KD*c
rc(Xd(-ET),Zd(Hi+ET),KD*(Wi+2*ET),KD*(Hi+2*ET),1.2,1,'#111',None,PE)
poly([(Xd(x),Zd(z)) for (x,z) in PROF],1.2,'#111','#fff')
poly([(Xd(x),Zd(min(z,20))) for (x,z) in PROF],0,'none',MAT)
ci(Xd(Wi/2),Zd(RT),KD*3.5,1.1,'#333','#fff'); ci(Xd(Wi/2),Zd(RT),KD*RT,1,BLU,'3,2')
ci(Xd(Wi/2),Zd(12),KD*4.5,1,PUR,'4,3'); ci(Xd(Wi/2),Zd(12),KD*.5,1,PUR,None,'#efeaf8')
for a_ in (30,150,270):
    a=math.radians(a_); ln(Xd(Wi/2),Zd(12),Xd(Wi/2)+KD*4.5*math.cos(a),Zd(12)-KD*4.5*math.sin(a),1.2,PUR)
ln(Xd(Wi/2),Zd(-ET),Xd(Wi/2),Zd(-6),1.8,GRN)
tx(Xd(Wi/2),Zd(-8),'ağız ORTADA (x 27 / 43)',5.6,'middle','bold',GRN)
tx(Xd(1.2),Zd(RISE/2+1.5),'55°',5,'start','bold',AMB); tx(Xd(Wi-1.2),Zd(RISE/2+1.5),'55°',5,'end','bold',AMB)
tx(Xd(Wi/2)+KD*5,Zd(RT)+3,'helezon Ø70',5.2,'start','bold',BLU); tx(Xd(Wi/2)+KD*5.5,Zd(12)+3,'tarak Ø9',5.2,'start','bold',PUR)
tx(Xd(Wi/2),Zd(19),'yığın ≤ 20',5,'middle','',AMB)
ln(Xd(0),Zd(Hi+ET+2),Xd(Wi),Zd(Hi+ET+2),.7); tx(Xd(Wi/2),Zd(Hi+ET+3.5),'14,4 iç · 16 dış',5.4,'middle','bold')
ln(Xd(Wi+ET+2),Zd(0),Xd(Wi+ET+2),Zd(Hi),.7); tx(Xd(Wi+ET+3),Zd(Hi/2),'22,4 · 24',5.4,'start','bold')
tx(XD+160,YD+232,'kesit %.0f cm² × 52,4 = %.1f L → kaşar %.1f kg · sucuk %.1f · kıyma %.1f · kuşbaşı %.1f' % (AREA,VOL,KG['KAŞAR'],KG['SUCUK'],KG['KIYMA'],KG['KUŞBAŞI']),5.6,'middle','bold','#333')
tx(XD+160,YD+245,'V kısa (eğim 3,4 cm), gövde nerdeyse U-tekne: helezon tabanı tarar, köprü kuracak genişlik yok',5.2,'middle','','#333')
tx(XD+160,YD+258,'kavrama ortada, arka uçta; ayna yok → 16 kap tek kalıp, tek beşik, tek STORE yuvası',5.4,'middle','bold',GRN)
tx(XD+160,YD+271,'kaşar: milsiz spiral h35 · küpler: milli h50 · kıyma: milsiz h30 — spiral sökülüp takılır, gövde aynı',5.2,'middle','','#333')
tx(XD+160,YD+284,'PE 8 mm gövde ~3,5 kg; dolu ≤ 13 kg (kıyma) → robot ✓',5.2,'middle','',GRY)
# STORE
XS,YS = 1100,100
rc(XS,YS,330,300,1.3,3,'#999',None,'#fcfbf8')
tx(XS+165,YS+16,'STORE −18 ÇEKMECESİ (61×65×29): 3 kap / modül',7.5,'middle','bold')
KS2=2.2
for m,(my,lab,adet) in enumerate(((YS+40,'KIYMA modülü',2),(YS+150,'KUŞBAŞI modülü',2))):
    mx=XS+20
    rc(mx,my,KS2*61,KS2*29,1.3,1,'#111',None,'#dbeafe'); rc(mx+KS2*.75,my+KS2*.5,KS2*59.5,KS2*28,.8,0,'#555','3,2','none')
    for j in range(3):
        x0=2+j*19
        dash = j>=adet
        rc(mx+KS2*x0,my+KS2*(28.5-HK),KS2*WK,KS2*HK,1,1,'#111' if not dash else '#999','3,2' if dash else None,PE if not dash else LIGHT)
        poly([(mx+KS2*(x0+ET+x),my+KS2*(28.5-ET-z)) for (x,z) in PROF],.8,'#111' if not dash else '#999','#fff' if not dash else LIGHT,'3,2' if dash else None)
    tx(mx+KS2*30.5,my-5,lab+' · 2 dolu + 1 boş yuva',5.6,'middle','bold',GRY)
    tx(mx+KS2*30.5,my+KS2*29+9,'3 × 16 = 48 ≤ 59,5 ✓ · 24 ≤ 29 ✓ · derinlik 54 ≤ 59,5 ✓',5,'middle','bold',GRN)
tx(XS+165,YS+262,'eleman haftalık: 2 kıyma + 2 kuşbaşı buraya (donmuş, kavrulmuş/sote)',5.4,'middle','','#333')
tx(XS+165,YS+275,'robot 1 gün önce ALT çözülme beşiğine alır · STORE v4 değişmez',5.4,'middle','','#333')
tx(XS+165,YS+288,'kaşar yedekleri +3'+chr(39)+'te ALT'+chr(39)+'ta (4 beşik), donmaz',5.4,'middle','bold',GRN)

# ================= TABLO + KONTROL =================
XT,YT = 760,420
rc(XT,YT,670,500,1.4,4)
tx(XT+14,YT+22,'POZİSYONLAR · ADET · AKIŞ · KONTROL',10,'start','bold')
hdr=['pozisyon','kat','x','malzeme','dolum','dayanır','değişim','adet/hafta']
cx_=[XT+14,XT+90,XT+130,XT+170,XT+270,XT+340,XT+420,XT+560]
for i,h in enumerate(hdr): tx(cx_[i],YT+46,h,6.4,'start','bold',GRY)
ln(XT+12,YT+52,XT+658,YT+52,.8,'#bbb')
rows=[('1 sol','kat 1','27','KAŞAR A','%.1f kg' % KG['KAŞAR'],'2,7 gün (yarı yük)','robot · ALT'+chr(39)+'tan','kaşar 6 + 1'),
      ('1 sağ','kat 1','43','SUCUK küp','%.1f kg' % KG['SUCUK'],'6,8 gün (≈ hafta)','robot · eleman getirir','sucuk 1 + 1'),
      ('2 sol','kat 2','27','KAŞAR B','%.1f kg' % KG['KAŞAR'],'2,7 gün','robot · ALT'+chr(39)+'tan','(kaşar toplam 7)'),
      ('2 sağ','kat 2','43','boş / kavurma','—','—','değişim parkı','—'),
      ('3 sol','kat 3','27','KIYMA kavrulmuş','%.1f kg' % KG['KIYMA'],'3 gün','robot · ALT çözülme','kıyma 2 + 2'),
      ('3 sağ','kat 3','43','KUŞBAŞI sote','%.1f kg' % KG['KUŞBAŞI'],'3 gün','robot · ALT çözülme','kuşbaşı 2 + 2')]
for i,r in enumerate(rows):
    yy=YT+70+i*17
    for j,v in enumerate(r): tx(cx_[j],yy,v,6.1,'start','bold' if j==3 else '','#111' if j==3 else '#333')
ln(XT+12,YT+176,XT+658,YT+176,.8,'#bbb')
notes=[('Düzlemler: kat 1 = sucuklu-kaşarlı (kaşar A + sucuk) · kat 2 = kaşarlı (kaşar B) · kat 3 = kıymalı / kuşbaşılı → hiçbir tarifte kat değişimi yok',GRN,'bold'),
       ('Robot değişimleri/hafta: kaşar 6 · kıyma 2 · kuşbaşı 2 · sucuk 1 = 11; her biri 2 hamle (boş → park beşiği, dolu → pozisyon) ≈ 1 dk; kap ≤ 13 kg',GRN,''),
       ('Eleman haftalık: 6 kaşar + 1 sucuk (ALT beşiklerine / pozisyona) + 2 kıyma + 2 kuşbaşı (STORE −18); parktaki 11 boşu alır, yıkar. 16 kap tek tip.','#333',''),
       ('Üst 27 cm boşaldı: elektrik arka duvar içi (PLC, PSU, 6 sürücü), soğutma grubu ALT arkası 20 derin (1/12 HP, plint ızgarası), evaporatör ALT üstü → 3. kat sığdı','#333',''),
       ('Süpürme: tepsi Ø32 (R 16) + spiral R 11 = 27 → sol x 0-54, sağ 16-70: duvara sıfır pay → boşluk yan duvarları düz, çıkıntısız; istersen kap 15 en → 0,5 pay',AMB,'bold'),
       ('Spiral R 11 kabulü: ağızdan düşen malzeme ±2 cm saçılır, pide kenarı (R 13) kapanır — prototipte doğrulanacak; kapanmazsa kap 15 en + tepsi Ø31','#333',''),
       ('KONTROL ① ağızlar x 27/43, y 78 ≥ 31 ✓ · ② her kabın önü boş ✓ · ③ tek kap tipi, ayna yok ✓ · ④ dikey 3×41 + 74 = 197 ✓ · ⑤ robot yükü ≤ 13 kg ✓ · ⑥ STORE 24 ≤ 29 ✓',GRN,'bold'),
       ('AÇIK: tepsi düzlemi 158 cm (kobot üst erişim) · kaşar 20 cm yığında akış prototipi (küçük kapta kekleşme riski düşük) · plint hava yolu · klape ×3',AMB,''),
       ('HAT v45: TOPPING bloğu bu çizimle (teknik üstte yok, 3 kat, ALT soğutma); KONTROL ⑦ kapandı; STORE v4 değişmez',BLU,'')]
for i,(s,c,fw) in enumerate(notes): tx(XT+14,YT+194+i*19,s,6.1,'start',fw,c)
tx(XT+14,YT+380,'v22 → v23: 3 kap tipi → 1 · kaşar 37 kg kap → 6,1 kg · sol/sağ ayna yok · teknik bölme üstte yok · 2 kat → 3 kat · ALT 6 → 8 beşik + soğutma',6.4,'start','bold','#111')
tx(XT+14,YT+396,'Sıradaki: HAT v45 · site',6.2,'start','',GRY)
# ================= ÜST GÖRÜNÜM (normal plan) — kat 1 / kat 2 / kat 3 / ALT =================
YU=1230
rc(40,YU-30,1390,340,1.4,4)
tx(56,YU-8,'ÜST GÖRÜNÜM (plan) — her kat 70 × 84 · arka duvar 10 (motorlar) · klape 4 önde · kaplar y 4-58 (önden) · süpürme R 27 kesikli yeşil',10,'start','bold')
KU=2.2
def plan(X,Y,ad,kaplar,alt=False):
    tx(X+KU*35,Y-6,ad,7.5,'middle','bold')
    rc(X,Y,KU*70,KU*84,1.3)
    rc(X,Y,KU*70,KU*10,.8,0,'#555',None,'#d9d9d9'); tx(X+KU*35,Y+KU*6.5,'arka duvar: motor + elektrik',4.4,'middle','','#333')
    if alt:
        rc(X+KU*2,Y+KU*10,KU*66,KU*16,.9,0,'#555',None,'#cfd8dc'); tx(X+KU*35,Y+KU*19,'SOĞUTMA GRUBU (20 derin)',4.8,'middle','bold','#37474f')
        for i,lab in enumerate(('park','park','çöz. kıyma','çöz. kuşbaşı')):
            x0=1.2+i*17.2
            rc(X+KU*x0,Y+KU*26,KU*16,KU*54,1,1,'#555',None,'#e4e0d4'); ln(X+KU*(x0+8),Y+KU*28,X+KU*(x0+8),Y+KU*78,1,BLU,'3,2')
            tx(X+KU*(x0+8),Y+KU*50,lab,4.4,'middle','bold','#444'); tx(X+KU*(x0+8),Y+KU*58,'(üstte kaşar yd)',3.8,'middle','','#777')
        rc(X,Y+KU*80,KU*70,KU*4,.9,0,'#555',None,'#9e9e9e'); tx(X+KU*35,Y+KU*83,'plint ızgarası',3.8,'middle','','#fff')
        return
    for (x0,nm,bos) in kaplar:
        col='#999' if bos else '#111'; d='3,2' if bos else None
        rc(X+KU*x0,Y+KU*26,KU*16,KU*54,1.1,1,col,d,LIGHT if bos else PE)
        if not bos:
            ln(X+KU*(x0+8),Y+KU*28,X+KU*(x0+8),Y+KU*78,1.4,GRN); ln(X+KU*(x0+8),Y+KU*10,X+KU*(x0+8),Y+KU*26,1,BLU,'3,2')
            ci(X+KU*(x0+8),Y+KU*78,2.6,1.3,GRN,None,'#fff'); ci(X+KU*(x0+8),Y+KU*78,KU*27,.8,GRN,'4,3')
            rc(X+KU*(x0+5),Y+KU*2,KU*6,KU*6,.9,1,BLU,None,'#dfe7fb')
        tx(X+KU*(x0+8),Y+KU*44,nm,5,'middle','bold','#888' if bos else '#111'); tx(X+KU*(x0+8),Y+KU*52,'boş' if bos else '16×54',4.2,'middle','','#888' if bos else '#333')
    rc(X,Y+KU*80,KU*70,KU*4,.9,0,BLU,None,'#dfe7fb'); tx(X+KU*35,Y+KU*83,'klape',3.8,'middle','',BLU)
    tx(X+KU*27,Y+KU*81.5,'x 27',3.6,'middle','bold',GRN); tx(X+KU*43,Y+KU*81.5,'x 43',3.6,'middle','bold',GRN)
plan(60,YU+30,'KAT 1 (z 170-197) — sucuklu-kaşarlı düzlemi',[(19,'KAŞAR A',False),(35,'SUCUK',False)])
plan(280,YU+30,'KAT 2 (z 129-156) — kaşarlı düzlemi',[(19,'KAŞAR B',False),(35,'boş / kavurma',True)])
plan(500,YU+30,'KAT 3 (z 88-115) — kıymalı / kuşbaşılı',[(19,'KIYMA',False),(35,'KUŞBAŞI',False)])
plan(720,YU+30,'ALT (z 0-74) — beşikler + soğutma',[],True)
nx,ny_=960,YU+36
for i,(s,c,fw) in enumerate([('Kaplar her katta aynı yerde: x 19-35 (merkez 27) ve x 35-51 (merkez 43) — dolabın orta 32 cm'+chr(39)+'i; yanlarda 19 cm boş (hava kanalı, kablo, ray).','#333',''),
                              ('Ağızlar kabın ön ucunda y 78 (arka duvardan) → süpürme R 27: sol kap x 0-54 / y 51-105, sağ kap x 16-70 — yan duvarlar düz.',GRN,'bold'),
                              ('Helezon (yeşil) kabın ortasında arkadan öne, arka uçta pençe → arka duvardaki motora (mavi kesikli ara mil).','#333',''),
                              ('Klape önde 4 cm, her kat ayrı; robot kabı önden çeker/iter. Yan 19 cm boşluklar kapalı panel (soğuk hacim).','#333',''),
                              ('ALT: soğutma grubu arka 20 cm (y 10-26), 4 beşik y 26-80 iki sırada (alt: park ×2 + çözülme ×2, üst: kaşar yedeği ×4), plint ızgarası önde.','#333',''),
                              ('STORE −18: 3 kap/modül (kıyma 2, kuşbaşı 2). Kaşar yedekleri +3'+chr(39)+'te ALT üst sırada.','#333',''),
                              ('HAT v45: TOPPING bloğu bu haliyle, KONTROL ⑦ ✓ (kol ≤ 13 kg), ⑫ tepsi Ø32 zinciri açık.',BLU,'bold')]):
    tx(nx,ny_+i*15.5,s,6.2,'start',fw,c)

tx(W-40,H-12,'AUTOKITCH · arastirma/3_TOPPING/ist3_topping_detay_v24 · 5 Eyl 2026',7,'end','',GRY)
o.append('</svg>')
svg = chr(10).join(o)
xml.dom.minidom.parseString(svg.encode('utf-8'))
out = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\3_TOPPING\ist3_topping_detay_v24.svg"
io.open(out,'w',encoding='utf-8').write(svg)
print('yazildi + XML gecerli | kap kesit %.0f cm2 → %.1f L · kasar %.1f kg · rise %.1f' % (AREA,VOL,KG['KAŞAR'],RISE))
