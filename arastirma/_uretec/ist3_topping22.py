# -*- coding: utf-8 -*-
# TOPPING v22 — kap_geometri_v1 kaplarıyla istasyon: izometrik + ön kesit + ALT beşikleri (kap şeklinde, sol/sağ) + STORE −18 kesiti · tek pafta
# kat 1: KAŞAR (BÜYÜK-L, 32,5×70×60, hafta) + SUCUK (KÜÇÜK-R, 20×54×24, hafta) · kat 2: KIYMA (KÜÇÜK-L) + KUŞBAŞI (KÜÇÜK-R), 3 gün, robot · motorlar arka duvarda
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
def poly(pts,sw=1,c='#111',f='none',d=None,op=1):
    o.append('<polygon points="%s" fill="%s" fill-opacity="%s" stroke="%s" stroke-width="%s"%s stroke-linejoin="round"/>' % (' '.join('%.1f,%.1f'%p for p in pts),f,op,c,sw,(' stroke-dasharray="%s"'%d) if d else ''))
def elp(x,y,rx,ry,sw=1,c='#111',f='none',op=1,rot=0):
    o.append('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="%s" fill-opacity="%s" stroke="%s" stroke-width="%s" transform="rotate(%g %.1f %.1f)"/>' % (x,y,rx,ry,f,op,c,sw,rot,x,y))
def arr(x1,y1,x2,y2,c='#c0392b',w=1.4):
    ln(x1,y1,x2,y2,w,c); a=math.atan2(y2-y1,x2-x1)
    for s in (1,-1): ln(x2,y2,x2-8*math.cos(a-s*.42),y2-8*math.sin(a-s*.42),w,c)

GRN, RED, BLU, GRY, AMB, PUR = '#1d7a4f', '#c0392b', '#1a49b8', '#666', '#b7791f', '#6b4fa8'
KAS, DIG, PLATE, WALL, LIGHT, PE, MAT = '#f3efe4', '#e9eef7', '#dfe7fb', '#d9d9d9', '#f7f6f2', '#e8f0e8', '#e9dfa8'
TH, RT = 55.0, 3.8
def profil(Wi,Hi,mirror=False,n=16):
    xc = Wi-RT; t=math.radians(TH)
    px_,pz_ = xc-RT*math.sin(t), RT-RT*math.cos(t)
    rise = pz_ + px_*math.tan(t)
    pts=[(0,Hi),(0,rise),(px_,pz_)]
    a0=math.atan2(pz_-RT,px_-xc)
    for k in range(1,n+1):
        a=a0+(2*math.pi-a0)*k/n; pts.append((xc+RT*math.cos(a),RT+RT*math.sin(a)))
    pts+=[(Wi,RT),(Wi,Hi)]
    if mirror: pts=[(Wi-x,z) for (x,z) in pts]
    return pts, rise, xc
def alan(pts):
    s=0
    for i in range(len(pts)):
        x1,z1=pts[i]; x2,z2=pts[(i+1)%len(pts)]; s+=x1*z2-x2*z1
    return abs(s)/2
# kaplar (dış ölçüler; iç = dış − 2×et) · x0..x1 kabin, L boy, Hh yük, kat, mirror(R), ad
ET_B, ET_S = 1.0, 0.8
KAPS=[dict(ad='KAŞAR',   x0=2.0, x1=34.5, L=70, Hh=60, kat=1, R=False, et=ET_B, f=KAS, alt='BÜYÜK-L · hafta · eleman'),
      dict(ad='SUCUK KÜP',x0=35.0,x1=55.0, L=54, Hh=24, kat=1, R=True,  et=ET_S, f=DIG, alt='KÜÇÜK-R · hafta · eleman'),
      dict(ad='KIYMA',    x0=14.5,x1=34.5, L=54, Hh=24, kat=2, R=False, et=ET_S, f=DIG, alt='KÜÇÜK-L · 3 gün · robot'),
      dict(ad='KUŞBAŞI',  x0=35.0,x1=55.0, L=54, Hh=24, kat=2, R=True,  et=ET_S, f=DIG, alt='KÜÇÜK-R · 3 gün · robot')]
for k in KAPS:
    Wi=k['x1']-k['x0']-2*k['et']; Hi=k['Hh']-2*k['et']; k['Wi'],k['Hi']=Wi,Hi
    k['prof'],k['rise'],xc = profil(Wi,Hi,k['R'])
    k['xs'] = (k['x1']-k['et']-RT) if not k['R'] else (k['x0']+k['et']+RT)   # helezon ekseni (kabin x)
    k['vol'] = alan(k['prof'])*(k['L']-2*k['et'])/1000
Z = {'alt':(0,52),'b2':(52,66),'k2':(66,93),'b1':(93,107),'k1':(107,170),'tek':(170,197)}
WALLT, YF = 10, 4
S=3.0; c30=math.cos(math.radians(30)); X0,Y0 = 70, 120+217*S
def P(x,yb,z): return (X0+S*(x*c30+yb*c30), Y0+S*(x*0.5-yb*0.5-z))
def ipoly(pts3,sw=1,c='#111',f='none',d=None,op=1): poly([P(*p) for p in pts3],sw,c,f,d,op)
def iline(p1,p2,w=1,c='#111',d=None): a=P(*p1); b=P(*p2); ln(a[0],a[1],b[0],b[1],w,c,d)

o.append('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">' % (W,H,W,H))
rc(0,0,W,H,0,0,'none',None,'#fff')
tx(30,42,'AUTOKITCH — İSTASYON 3 · TOPPING v22 (5 Eyl 2026) — kap_geometri_v1 kaplarıyla: kat 1 KAŞAR + SUCUK KÜP (hafta, eleman) · kat 2 KIYMA + KUŞBAŞI (3 gün, robot) · ALT kap şeklinde beşikler · STORE −18 kesiti · 70 × 197 × 84',15,'start','bold')
tx(30,66,'Kaplar tek eğimli kama (55°), U-oluk iç kenarda, helezon x 30 (sol) / 40 (sağ) = bant kenarları (pide Ø30) · motorlar 10 cm arka duvarda, kap itilince pençe kavrar · sağ/sol kaplar ve beşikler ayna · kapta elektrik yok',9.5,'start','','#444')
ln(30,78,W-30,78,.8,'#999')

# ================= İZOMETRİK =================
tx(X0+60,Y0-217*S-14,'İZOMETRİK — dolap içi z 0-175 · 1:3,3',9,'start','bold')
zlo,zhi=0,175
for (a,b) in (((0,0,zlo),(0,0,zhi)),((70,0,zlo),(70,0,zhi)),((0,84,zlo),(0,84,zhi)),((70,84,zlo),(70,84,zhi)),
              ((0,0,zlo),(70,0,zlo)),((0,0,zlo),(0,84,zlo)),((0,0,zhi),(70,0,zhi)),((0,0,zhi),(0,84,zhi)),((70,0,zhi),(70,84,zhi)),((0,84,zhi),(70,84,zhi)),((70,0,zlo),(70,84,zlo))):
    iline(a,b,.7,'#bbb')
ipoly([(0,84-WALLT,zlo),(70,84-WALLT,zlo),(70,84-WALLT,zhi),(0,84-WALLT,zhi)],1,'#555',WALL,None,.9)
ipoly([(0,84-WALLT,zhi),(70,84-WALLT,zhi),(70,84,zhi),(0,84,zhi)],1,'#555','#c8c8c8',None,.9)
ipoly([(70,84-WALLT,zlo),(70,84,zlo),(70,84,zhi),(70,84-WALLT,zhi)],1,'#555','#cfcfcf',None,.9)
def motor(x,zf):
    for dz in (0,7):
        ipoly([(x-3,84-WALLT+1,zf+dz),(x+3,84-WALLT+1,zf+dz),(x+3,84-WALLT+8,zf+dz),(x-3,84-WALLT+8,zf+dz)],.9,BLU,'#dfe7fb','3,2',.9)
    iline((x-3,84-WALLT+1,zf),(x-3,84-WALLT+1,zf+7),.9,BLU,'3,2'); iline((x+3,84-WALLT+1,zf),(x+3,84-WALLT+1,zf+7),.9,BLU,'3,2')
for k in KAPS: motor(k['xs'], Z['k%d'%k['kat']][0])
for z in (Z['k2'][0],Z['k1'][0]):
    ipoly([(0,0,z),(70,0,z),(70,84-WALLT,z),(0,84-WALLT,z)],1.2,BLU,PLATE,None,.85)
    ipoly([(0,0,z-2),(70,0,z-2),(70,0,z),(0,0,z)],1,BLU,'#c9d6f5',None,.9)
    ipoly([(70,0,z-2),(70,84-WALLT,z-2),(70,84-WALLT,z),(70,0,z)],1,BLU,'#c9d6f5',None,.9)
# ALT beşikleri: 2 sıra × 3 (x 3-23 L, 25-45 R, 47-67 R), z 0 ve 26, derinlik yb 4-58
ipoly([(0,0,26),(70,0,26),(70,84-WALLT,26),(0,84-WALLT,26)],.9,'#999','#ececec',None,.8)
BES=[(3,0,'park (L)',True,True),(25,0,'park (R)',True,False),(47,0,'yedek (R)',True,False),(3,26,'kıyma çözülme',False,True),(25,26,'kuş. çözülme',False,False),(47,26,'boş yedek (R)',True,False)]
for (x0,zf,lab,dash,left) in BES:
    # beşik: 20 en, 54 boy, 6 yüksek blok + U yatak (oluk tarafı iç kenarda)
    ipoly([(x0,YF,zf),(x0+20,YF,zf),(x0+20,YF,zf+5),(x0,YF,zf+5)],.9,'#555','#d8d4c8',None,.9)
    ipoly([(x0,YF,zf+5),(x0+20,YF,zf+5),(x0+20,YF+54,zf+5),(x0,YF+54,zf+5)],.8,'#555','#e4e0d4',None,.85)
    ipoly([(x0+20,YF,zf),(x0+20,YF+54,zf),(x0+20,YF+54,zf+5),(x0+20,YF,zf+5)],.8,'#555','#cfcbbf',None,.85)
    ux = x0+20-4.6 if left else x0+4.6
    iline((ux,YF+1,zf+5.2),(ux,YF+53,zf+5.2),1.2,BLU,'3,2')
    if not dash:
        ipoly([(x0+1,YF+1,zf+5),(x0+19,YF+1,zf+5),(x0+19,YF+1,zf+26),(x0+1,YF+1,zf+26)],.9,'#333',DIG,None,.85)
        ipoly([(x0+1,YF+1,zf+26),(x0+19,YF+1,zf+26),(x0+19,YF+53,zf+26),(x0+1,YF+53,zf+26)],.8,'#333',DIG,None,.7)
        ipoly([(x0+19,YF+1,zf+5),(x0+19,YF+53,zf+5),(x0+19,YF+53,zf+26),(x0+19,YF+1,zf+26)],.8,'#333','#dde3ee',None,.8)
    t=P(x0+10,YF+3,zf+(14 if not dash else 9)); tx(t[0],t[1],lab,5.2,'middle','bold','#666' if dash else '#333')
t=P(0,-2,44); tx(t[0]-6,t[1]+8,'ALT 52: 2 sıra × 3 beşik, kap şeklinde (U yatak), sol/sağ ayna',6.5,'end','bold',GRY)
t=P(0,-2,18); tx(t[0]-6,t[1]+8,'robot boşalanı parka, çözülmüşü kat 2'+chr(39)+'ye koyar',6,'end','',GRY)

def kap(k):
    x0,x1,L,Hh,zf,R,et,f = k['x0'],k['x1'],k['L'],k['Hh'],Z['k%d'%k['kat']][0],k['R'],k['et'],k['f']
    yb0=YF
    # dış kabuk kutu: arka yüz, yan yüzler
    box=[(x0,yb0,zf),(x1,yb0,zf),(x1,yb0,zf+Hh),(x0,yb0,zf+Hh)]
    back=[(x,yb0+L,z) for (x,_,z) in box]
    ipoly(back,1,'#333',PE,None,.95)
    for i in range(4):
        a,b=box[i],box[(i+1)%4]; a2,b2=back[i],back[(i+1)%4]
        ipoly([a,b,b2,a2],.9,'#333',PE,None,.9)
    # iç: helezon, taraklar (y boyunca)
    xs=k['xs']
    iline((xs,yb0+1,zf+et+RT),(xs,yb0+L-1,zf+et+RT),2.2,GRN)
    for kk in range(int(L/3.5)):
        y=yb0+2+kk*3.5
        if y>yb0+L-2: break
        iline((xs-3,y,zf+et+1),(xs+3,y,zf+et+6),1.1,GRN)
    taraks = ((13,5.5),(36,8)) if Hh>40 else ((12,5),)
    for (zt,r) in taraks:
        xa = xs-2 if not R else xs+2
        iline((xa,yb0+1,zf+et+zt),(xa,yb0+L-1,zf+et+zt),1.5,PUR)
        for kk in range(int(L/4)):
            y=yb0+2.5+kk*4
            if y>yb0+L-2: break
            s=1 if kk%2==0 else -1; iline((xa,y,zf+et+zt),(xa,y,zf+et+zt+s*r*0.8),1,PUR)
    # ön yüz: profil (yarı saydam), dış kabuk kenarı
    prof=[(x0+et+x, zf+et+z) for (x,z) in k['prof']]
    ipoly([(x,yb0,z) for (x,z) in prof],1.2,'#111','#fff',None,.55)
    ipoly([(x,yb0,z) for (x,_,z) in box],1.3,'#111',PE,None,.35)
    # ağız ön uçta (helezon x), plakadan aşağı
    ipoly([(xs-2.5,yb0+1,zf-7),(xs+2.5,yb0+1,zf-7),(xs+2.5,yb0+5,zf-7),(xs-2.5,yb0+5,zf-7)],1,GRN,'#eaf6ee')
    for (dx,dy) in ((-2.5,1),(2.5,1),(2.5,5),(-2.5,5)): iline((xs+dx,yb0+dy,zf),(xs+dx,yb0+dy,zf-7),1,GRN)
    a=P(xs,yb0+3,zf-7); arr(a[0],a[1]+2,a[0],a[1]+16,GRN,1.4)
    # arka kavrama + ara mil
    if yb0+L < 84-WALLT-1: iline((xs,yb0+L,zf+et+RT),(xs,84-WALLT,zf+et+RT),1.2,BLU,'4,3')
    ipoly([(xs-2,yb0+L,zf+et+RT-2),(xs+2,yb0+L,zf+et+RT-2),(xs+2,yb0+L+2,zf+et+RT-2),(xs-2,yb0+L+2,zf+et+RT-2)],.9,BLU,'#dfe7fb')
    t=P((x0+x1)/2, yb0+L*0.5, zf+Hh+3); tx(t[0],t[1]-4,k['ad'],8.5,'middle','bold'); tx(t[0],t[1]+6,'%g×%g×%g · %.0f L · %s' % (x1-x0,L,Hh,k['vol'],k['alt']),5.6,'middle','','#333')
for k in KAPS: kap(k)
for (z,x) in ((Z['b1'][0]+3,30),(Z['b2'][0]+3,30)):
    cpt=P(x,YF+10,z); elp(cpt[0],cpt[1],17*S*0.95,17*S*0.5,1.2,BLU,'#dfe7fb',.9,-30)
    cpt2=P(x+17,YF+10,z); tx(cpt2[0]+12,cpt2[1],'tepsi Ø34 · pide Ø30',6,'start','',BLU)
ipoly([(0,0,Z['tek'][0]),(70,0,Z['tek'][0]),(70,84-WALLT,Z['tek'][0]),(0,84-WALLT,Z['tek'][0])],.8,'#999','#f3f3f3',None,.5)
t=P(35,40,Z['tek'][0]+3); tx(t[0],t[1],'teknik 27 ↑ (soğutma +2…+4 · elektrik)',6.5,'middle','',GRY)
a=P(-6,-4,Z['k2'][0]+14); arr(a[0]-40,a[1]+24,a[0],a[1],AMB,1.6); tx(a[0]-44,a[1]+36,'ÖN (robot)',8,'middle','bold',AMB)
t=P(70,84-WALLT/2,zhi+4); tx(t[0]+6,t[1],'ARKA DUVAR 10 — motorlar + sürücüler',7.5,'start','bold',BLU)
lx,ly=X0+290,Y0-217*S+8
for i,(col,lab) in enumerate(((GRN,'helezon (kaşar/kıyma milsiz spiral, küp milli)'),(PUR,'tarak (kaşarda ×2)'),(BLU,'pençe kavrama / ara mil / motor'),(GRN,'ağız → tepsi (x 30 / 40)'))):
    ln(lx,ly+i*13,lx+18,ly+i*13,2.2,col); tx(lx+24,ly+i*13+3,lab,6.5,'start','','#333')

# ================= ÖN KESİT =================
XC,YC = 560,100
tx(XC+88,YC-6,'ÖN KESİT (helezon hattı) 1:4',8.5,'middle','bold')
K=2.5
rc(XC,YC,K*70,K*197,1.8)
for ad,(z0,z1),col in (('teknik',Z['tek'],'#f3f3f3'),('KAT 1',Z['k1'],'#fff'),('boşluk 1',Z['b1'],'#eef3ff'),('KAT 2',Z['k2'],'#fff'),('boşluk 2',Z['b2'],'#eef3ff'),('ALT',Z['alt'],'#f7f6f2')):
    rc(XC,YC+K*(197-z1),K*70,K*(z1-z0),.7,0,'#111',None,col); tx(XC+K*70+4,YC+K*(197-(z0+z1)/2)+3,'%s %g'%(ad,z1-z0),5.4,'start','',GRY)
def kesit_kap(k,zf,x0,dash=None):
    Zc=lambda c: YC+K*(197-zf-c); et=k['et']; x1=x0+(k['x1']-k['x0'])
    rc(XC+K*x0,Zc(k['Hh']),K*(x1-x0),K*k['Hh'],1,1,'#111' if not dash else '#999',dash,PE if not dash else LIGHT)
    prof=[(XC+K*(x0+et+x),Zc(et+z)) for (x,z) in k['prof']]
    poly(prof,1,'#111' if not dash else '#999','#fff' if not dash else LIGHT,dash)
    if not dash:
        poly([(XC+K*(x0+et+x),Zc(et+min(z,k['Hi']-6))) for (x,z) in k['prof']],0,'none',MAT)
        xs=k['xs'] if x0==k['x0'] else (x0+(k['xs']-k['x0']))
        ci(XC+K*xs,Zc(et+RT),K*3.5,1,GRN,'#fff')
        for (zt,r) in (((13,5.5),(36,8)) if k['Hh']>40 else ((12,5),)):
            ci(XC+K*(xs-2 if not k['R'] else xs+2),Zc(et+zt),K*r,.8,PUR,'none','3,2')
        if zf in (Z['k1'][0],Z['k2'][0]): ln(XC+K*xs,Zc(0),XC+K*xs,Zc(-6),1.6,GRN)
    tx(XC+K*(x0+x1)/2,Zc(k['Hh']-6),k['ad'] if not dash else '',5.6,'middle','bold')
for k in KAPS: kesit_kap(k,Z['k%d'%k['kat']][0],k['x0'])
for z in (Z['b1'][0]+3,Z['b2'][0]+3):
    o.append('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="#dfe7fb" stroke="%s" stroke-width="1"/>' % (XC+K*35,YC+K*(197-z),K*17,K*1.2,BLU))
# ALT: beşikler + kaplar (kesitte)
small_L=[k for k in KAPS if k['ad']=='KIYMA'][0]; small_R=[k for k in KAPS if k['ad']=='KUŞBAŞI'][0]
for (x0,zf,lab,dash,left) in BES:
    kk = small_L if left else small_R
    rc(XC+K*x0,YC+K*(197-zf-5),K*20,K*5,.9,1,'#555',None,'#d8d4c8')
    kesit_kap(kk, zf+5, x0, '3,2' if dash else None)
    tx(XC+K*(x0+10),YC+K*(197-zf-2),lab,4.2,'middle','','#444')
tx(XC+K*35,YC+K*197+14,'70',7,'middle','bold'); tx(XC+K*35,YC+K*197+26,'27+63+14+27+14+52 = 197 ✓',6.5,'middle','bold',GRN)
tx(XC+K*35,YC+K*197+38,'tepsi düzlemleri 95 / 54 cm',6,'middle','',BLU)

# ================= STORE −18 KESİTİ =================
XS,YS = 760,100
rc(XS,YS,670,300,1.3,3,'#999',None,'#fcfbf8')
tx(XS+335,YS+16,'STORE −18 KASET ÇEKMECESİ (61 × 65 × 29) — küçük kaplar döndürmeden 2/modül: kıyma L ×2 · kuşbaşı R ×2',7.5,'middle','bold')
KS=1.8
sx,sy = XS+16, YS+30
rc(sx,sy,KS*70,KS*185,1.1)
for (z0,h,lab,col) in ((2,28,'soğutma 28','#f3f3f3'),(30,6,'','#ddd'),(36,84,'+3 bölge 84','#fff'),(120,8,'ayırıcı','#e9e4d6'),(128,10,'hamur','#e3f2fb'),(138,10,'hamur','#e3f2fb'),(148,29,'KASET ÇEKMECESİ 29','#dbeafe'),(177,8,'','#e9e4d6')):
    rc(sx,sy+KS*z0,KS*70,KS*h,.6,0,'#111',None,col)
    if lab: tx(sx+KS*35,sy+KS*(z0+h/2)+2,lab,4.4,'middle','bold' if 'KASET' in lab else '','#111')
tx(sx+KS*35,sy+KS*185+10,'STORE v4 (dikey konum)',5,'middle','',GRY)
KD=2.4
for m,(mx,lab,mir) in enumerate(((XS+160,'KIYMA modülü (L)',False),(XS+405,'KUŞBAŞI modülü (R)',True))):
    dy=YS+44
    rc(mx,dy,KD*61,KD*29,1.4,1,'#111',None,'#dbeafe'); rc(mx+KD*0.75,dy+KD*0.5,KD*59.5,KD*28,.8,0,'#555','3,2','none')
    kk = small_L if not mir else small_R
    for j in range(2):
        x0=1.5+j*21
        rc(mx+KD*x0,dy+KD*(28.5-24),KD*20,KD*24,1,1,'#111',None,PE)
        prof=[(mx+KD*(x0+kk['et']+x),dy+KD*(28.5-kk['et']-z)) for (x,z) in kk['prof']]
        poly(prof,.9,'#111','#fff')
        tx(mx+KD*(x0+10),dy+KD*12,'%s' % ('kıyma' if not mir else 'kuşbaşı'),5,'middle','bold')
    tx(mx+KD*30.5,dy-6,lab,6,'middle','bold',GRY)
    ln(mx,dy+KD*29+10,mx+KD*61,dy+KD*29+10,.7); tx(mx+KD*30.5,dy+KD*29+8,'61 · 2 × 20 = 40 ≤ 59,5 ✓',5.2,'middle','bold',GRN)
    ln(mx+KD*61+8,dy,mx+KD*61+8,dy+KD*29,.7); tx(mx+KD*61+12,dy+KD*15,'29 (24 ✓ pay 5)',5.2,'start','bold',GRN)
    # ust
    uy=dy+KD*29+38
    rc(mx,uy,KD*61,KD*40,1.1,1,'#111',None,'#dbeafe')
    for j in range(2): rc(mx+KD*(1.5+j*21),uy+KD*3,KD*20,KD*54*0.6,1,1,'#111',None,PE)
    tx(mx+KD*30.5,uy+KD*33,'üst: 54 derin ≤ 59,5 ✓ (1:1,67)',4.6,'middle','',GRY)
tx(XS+16,YS+262,'Akış: eleman haftalık STORE −18'+chr(39)+'e 2 kıyma + 2 kuşbaşı (donmuş, kavrulmuş/sote) koyar → robot 1 gün önce TOPPING ALT çözülme beşiğine → 3. gün kat 2'+chr(39)+'ye. Boşalan kap ALT park → eleman toplar.',6,'start','','#333')
tx(XS+16,YS+276,'Kap = ürün = pozisyon: kıyma kapları hep L (oluk sağ kenarda), kuşbaşı/sucuk kapları hep R. STORE modülleri de buna göre: sol modül L, sağ modül R.',6,'start','bold',RED)
tx(XS+16,YS+290,'Çekmece 29 yüksek: kap 24 → 5 cm pay; STORE v4 değişmez ✓',6,'start','',GRN)

# ================= TABLO + KONTROL =================
XT,YT = 760,420
rc(XT,YT,670,500,1.4,4)
tx(XT+14,YT+22,'KAPLAR · ADET · AKIŞ · KONTROL',10,'start','bold')
hdr=['malzeme','kap (tip)','dış ölçü','hacim','dolum','gün','pozisyon','değiştiren','adet']
cx_=[XT+14,XT+90,XT+180,XT+262,XT+318,XT+378,XT+430,XT+520,XT+620]
for i,h in enumerate(hdr): tx(cx_[i],YT+46,h,6.4,'start','bold',GRY)
ln(XT+12,YT+52,XT+658,YT+52,.8,'#bbb')
rows=[('KAŞAR rende','BÜYÜK-L','32,5×70×60','%.0f L' % KAPS[0]['vol'],'37 kg','8 (hafta)','kat 1 sol','eleman','2'),
      ('SUCUK küp','KÜÇÜK-R','20×54×24','%.1f L' % KAPS[1]['vol'],'8,4 kg','7 (hafta)','kat 1 sağ','eleman','2'),
      ('KIYMA kavrulmuş','KÜÇÜK-L','20×54×24','%.1f L' % KAPS[2]['vol'],'8,6 kg','3','kat 2 sol','robot','4'),
      ('KUŞBAŞI sote','KÜÇÜK-R','20×54×24','%.1f L' % KAPS[3]['vol'],'4,3 kg','3','kat 2 sağ','robot','4')]
for i,r in enumerate(rows):
    yy=YT+70+i*18
    for j,v in enumerate(r): tx(cx_[j],yy,v,6.2,'start','bold' if j==0 else '','#111' if j==0 else '#333')
ln(XT+12,YT+146,XT+658,YT+146,.8,'#bbb')
notes=[('Menü: kıymalı · kuşbaşılı · kaşarlı · sucuklu-kaşarlı. Kaşar kat 1'+chr(39)+'de: sucuklu ve kaşarlı tek düzlemde; kıymalı/kuşbaşılı kat 2'+chr(39)+'de tek düzlemde. "Kaşarlı kıymalı" → +1 kat geçişi (5 sn).',GRN,'bold'),
       ('Kıyma + kuşbaşı harçları KAVRULMUŞ / SOTE, suyu alınmış, vakumlu, donmuş gelir (çiğ harç su salar → helezon sulanır, 1-2 gün). Yumurta + tereyağı: fırın çıkışı, ayrı modül.',AMB,''),
       ('Robot hamleleri: 3 günde 1 (kıyma + kuşbaşı birlikte): kat 2 boş → ALT park · ALT çözülmüş → kat 2 (kap ≤ 10 kg) · STORE → ALT (1 gün önce). Sucuk + kaşar: eleman haftalık.','#333',''),
       ('Beşikler kabın U tabanına oturur; sol beşik (oluk sağda) ve sağ beşik (oluk solda) ayrı — robot hangi kabı nereye koyacağını RFID ile bilir.','#333',''),
       ('Motorlar: M1 kaşar (x 30), M2 sucuk (x 40, ara mil 16), M3 kıyma (x 30, ara mil), M4 kuşbaşı (x 40, ara mil) — hepsi arka duvarda, 40 W, enkoder; tarak 1:10 aynı milden.','#333',''),
       ('Derinlik: klape 4 + kap 70 + duvar 10 = 84 ✓ · kısa kaplar y 4-58, arkası ara mil · kaşar tam derinlik','#333',''),
       ('KONTROL ① bant: helezon x 30 (sol) / 40 (sağ) ∈ [30,40] ✓ (pide Ø30, tepsi 17 + spiral 13) · ağız y 78 ≥ 31 ✓ · süpürme sol x 0-60, sağ 10-70 ✓',GRN,'bold'),
       ('② erişim: her kabın önü boş ✓ · ALT beşikleri önden ✓ · ③ kap geometrisi = kap_geometri_v1 (55°, U-oluk, R ≥ 6, PE, tarak) ✓ · ④ dikey 197 ✓ · robot yükü ≤ 10 kg ✓ · STORE 24 ≤ 29 ✓',GRN,'bold'),
       ('⑤ AÇIK: kaşar prototip (sürtünme, köprüleme, 50 cm kekleşme) · kat 2 tepsi 54 cm kobot erişimi · klape/soğuk hacim · eleman kaşar kabı 53 kg (ray + yerinde dolum)',AMB,''),
       ('⑥ HAT v45: TOPPING bloğu bu çizimle (kat 63/27, çark katı yok, ALT beşikli) · STORE v4 değişmez · KONTROL ⑦ kapandı (kol ≤ 10 kg)',BLU,'')]
for i,(s,c,fw) in enumerate(notes): tx(XT+14,YT+164+i*19,s,6.1,'start',fw,c)
tx(XT+14,YT+364,'v21 → v22: çapraz helezon iptal, ön-arka iptal; kaplar tek eğimli kama; kaşar 37 kg hafta; küçük kap 20×54×24 üç ürün; kat 1 = hafta (eleman), kat 2 = 3 gün (robot).',6.2,'start','bold','#111')
tx(XT+14,YT+380,'Sıradaki: HAT v45 (TOPPING v22 bloğu + KONTROL) · site güncellemesi (onayla)',6.2,'start','',GRY)
tx(W-40,H-12,'AUTOKITCH · arastirma/3_TOPPING/ist3_topping_detay_v22 · 5 Eyl 2026',7,'end','',GRY)
o.append('</svg>')
svg = chr(10).join(o)
xml.dom.minidom.parseString(svg.encode('utf-8'))
out = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\3_TOPPING\ist3_topping_detay_v22.svg"
io.open(out,'w',encoding='utf-8').write(svg)
print('yazildi + XML gecerli | ' + ' · '.join('%s %.1f L (helezon x %.1f)' % (k['ad'],k['vol'],k['xs']) for k in KAPS))
