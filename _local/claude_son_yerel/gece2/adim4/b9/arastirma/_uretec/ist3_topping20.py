# -*- coding: utf-8 -*-
# TOPPING v20 — Kemal'in krokisi grafikleştirildi: izometrik · üst kat sol KAŞAR (uzun) sağ KAVURMA (kısa, aynı yükseklik) · alt kat SUCUK KÜP + KUŞBAŞI
# hepsi parça malzeme → helezon + tarak (bıçak YOK) · kalın arka duvar, motorlar içinde gizli · ağızlar önde
import io, math, xml.dom.minidom
W, H = 1460, 1100
o = []
def esc(s): return str(s).replace('&','&amp;').replace('<','&lt;')
def ln(x1,y1,x2,y2,w=1,c='#111',d=None):
    o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%s"%s stroke-linecap="round"/>' % (x1,y1,x2,y2,c,w,(' stroke-dasharray="%s"'%d) if d else ''))
def rc(x,y,w,h,sw=1,r=0,c='#111',d=None,f='none'):
    o.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%s" fill="%s" stroke="%s" stroke-width="%s"%s/>' % (x,y,w,h,r,f,c,sw,(' stroke-dasharray="%s"'%d) if d else ''))
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
KAS, DIG, PLATE, WALL = '#f3efe4', '#e9eef7', '#dfe7fb', '#d9d9d9'
# ---- izometrik projeksiyon: x sağa (0-70), yb önden arkaya (0-84), z yukarı ----
S=3.0; c30, s30 = math.cos(math.radians(30)), 0.5
X0, Y0 = 70, 120+217*S
def P(x,yb,z): return (X0 + S*(x*c30 + yb*c30), Y0 + S*(x*s30 - yb*s30 - z))
def ipoly(pts3,sw=1,c='#111',f='none',d=None,op=1): poly([P(*p) for p in pts3],sw,c,f,d,op)
def iline(p1,p2,w=1,c='#111',d=None): a=P(*p1); b=P(*p2); ln(a[0],a[1],b[0],b[1],w,c,d)

# ---- ölçüler ----
WK, SL = 32.5, 25.5                       # kap eni, 45° eğim
HK1, HK2 = 55, 40                         # üst kat kap yüksekliği, alt kat kap yüksekliği
LKA, LKS = 70, 20                         # kaşar boyu, kısa kap boyu
WALLT = 10                                # kalın arka duvar (motorlar içinde)
YF = 4                                    # kap ön yüzü (klape payı)
Z = {'alt':(0,42),'b2':(42,56),'k2':(56,98),'b1':(98,112),'k1':(112,170),'tek':(170,197)}
def kesit(Hh): return WK*Hh - SL*SL/2
vKA = kesit(HK1)*LKA/1000; vKV = kesit(HK1)*LKS/1000; vS = kesit(HK2)*LKS/1000

o.append('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">' % (W,H,W,H))
rc(0,0,W,H,0,0,'none',None,'#fff')
tx(30,42,'AUTOKITCH — TOPPING v20 (5 Eyl 2026) — Kemal'+chr(39)+'in krokisi: üst kat sol KAŞAR (uzun) · sağ KAVURMA (kısa, aynı yükseklik) · alt kat SUCUK KÜP + KUŞBAŞI · hepsi helezon + tarak (bıçak yok) · motorlar kalın arka duvarda',15,'start','bold')
tx(30,66,'Dört malzeme de parça halinde gelir (kaşar rende, sucuk KÜP, kavurma parça, kuşbaşı küp) → dört kapta aynı iç: tek tarak + altta dozaj helezonu. Ağızlar kabın ön ucunda (x 31 / 39), motorlar 10 cm kalın arka duvarın içinde gizli, kap itilince kavrar.',9.5,'start','','#444')
ln(30,78,W-30,78,.8,'#999')

# ================= İZOMETRİK =================
tx(X0+80,Y0-217*S-14,'İZOMETRİK — dolap içi, z 30-175 (ALT ve teknik bölme kısaltıldı) · 1:3,3',9,'start','bold')
zlo, zhi = 30, 175
# dış kabin kenarları (ince)
for (a,b) in (((0,0,zlo),(0,0,zhi)),((70,0,zlo),(70,0,zhi)),((0,84,zlo),(0,84,zhi)),((70,84,zlo),(70,84,zhi)),
              ((0,0,zlo),(70,0,zlo)),((0,0,zlo),(0,84,zlo)),((0,0,zhi),(70,0,zhi)),((0,0,zhi),(0,84,zhi)),((70,0,zhi),(70,84,zhi)),((0,84,zhi),(70,84,zhi)),((70,0,zlo),(70,84,zlo))):
    iline(a,b,.7,'#bbb')
# kalın arka duvar (yb 74-84): ön yüzü + üstü
ipoly([(0,84-WALLT,zlo),(70,84-WALLT,zlo),(70,84-WALLT,zhi),(0,84-WALLT,zhi)],1,'#555',WALL,None,.9)
ipoly([(0,84-WALLT,zhi),(70,84-WALLT,zhi),(70,84,zhi),(0,84,zhi)],1,'#555','#c8c8c8',None,.9)
ipoly([(70,84-WALLT,zlo),(70,84,zlo),(70,84,zhi),(70,84-WALLT,zhi)],1,'#555','#cfcfcf',None,.9)
# motorlar duvar icinde (kesikli silindir): her kabın helezon ekseni hizasında
def motor(x,zf):
    for k in (0,1):
        a=P(x-3, 84-WALLT+1+k*6, zf+1); b=P(x+3, 84-WALLT+1+k*6, zf+1)
    ipoly([(x-3,84-WALLT+1,zf),(x+3,84-WALLT+1,zf),(x+3,84-WALLT+8,zf),(x-3,84-WALLT+8,zf)],.9,BLU,'#dfe7fb','3,2',.9)
    ipoly([(x-3,84-WALLT+1,zf+7),(x+3,84-WALLT+1,zf+7),(x+3,84-WALLT+8,zf+7),(x-3,84-WALLT+8,zf+7)],.9,BLU,'#dfe7fb','3,2',.9)
    iline((x-3,84-WALLT+1,zf),(x-3,84-WALLT+1,zf+7),.9,BLU,'3,2'); iline((x+3,84-WALLT+1,zf),(x+3,84-WALLT+1,zf+7),.9,BLU,'3,2')
for zf in (Z['k1'][0],Z['k2'][0]):
    motor(31,zf); motor(39,zf)
# plakalar: kat 2 tabanı (z 56), kat 1 tabanı (z 112) — mavi
for (z,lab) in ((Z['k2'][0],'kat 2 tabanı'),(Z['k1'][0],'kat 1 tabanı')):
    ipoly([(0,0,z),(70,0,z),(70,84-WALLT,z),(0,84-WALLT,z)],1.2,BLU,PLATE,None,.85)
    ipoly([(0,0,z-2),(70,0,z-2),(70,0,z),(0,0,z)],1,BLU,'#c9d6f5',None,.9)
    ipoly([(70,0,z-2),(70,84-WALLT,z-2),(70,84-WALLT,z),(70,0,z)],1,BLU,'#c9d6f5',None,.9)

def kap(x0,x1,yb0,L,zf,Hh,slope_left,fill,lab,alt,screw_col=GRN):
    # slope_left: True → dış (sol) duvar eğimli, oluk sağ kenarda (sol kaplar); False → ayna (sağ kaplar)
    if slope_left:
        front=[(x0,yb0,zf+SL),(x0,yb0,zf+Hh),(x1,yb0,zf+Hh),(x1,yb0,zf),(x1-7,yb0,zf)]
        xs, xa = x1-3.5, x1-9        # helezon x, tarak x
    else:
        front=[(x0,yb0,zf),(x0+7,yb0,zf),(x1,yb0,zf+SL),(x1,yb0,zf+Hh),(x0,yb0,zf+Hh)]
        xs, xa = x0+3.5, x0+9
    back=[(x,yb0+L,z) for (x,_,z) in front]
    # arka yüz, taban, yan yüzler
    ipoly(back,1,'#333',fill,None,.95)
    n=len(front)
    for i in range(n):
        a,b = front[i], front[(i+1)%n]; a2,b2 = back[i], back[(i+1)%n]
        ipoly([a,b,b2,a2],.9,'#333',fill,None,.9)
    # iç: helezon (yeşil, ticks) + tarak (mor, pimler) — ön yüzden görünsün
    iline((xs,yb0+1,zf+3.5),(xs,yb0+L-1,zf+3.5),2.2,screw_col)
    nt=max(3,int(L/3.5))
    for k in range(nt):
        y=yb0+2+k*3.5
        if y>yb0+L-2: break
        iline((xs-3,y,zf+1),(xs+3,y,zf+6),1.2,screw_col)
    iline((xa,yb0+1,zf+16),(xa,yb0+L-1,zf+16),1.6,PUR)
    for k in range(nt):
        y=yb0+2.5+k*3.5
        if y>yb0+L-2: break
        s=1 if k%2==0 else -1; iline((xa,y,zf+16),(xa,y,zf+16+s*6),1,PUR)
    # üst yüz (yarı saydam) + ön yüz (yarı saydam)
    ipoly([front[1] if slope_left else front[4], front[2] if slope_left else front[3], back[2] if slope_left else back[3], back[1] if slope_left else back[4]],1,'#333',fill,None,.55)
    ipoly(front,1.3,'#111',fill,None,.5)
    # ağız: ön uçta, tabandan aşağı 7 (plakadan geçer)
    ipoly([(xs-2.5,yb0+1,zf-7),(xs+2.5,yb0+1,zf-7),(xs+2.5,yb0+6,zf-7),(xs-2.5,yb0+6,zf-7)],1,GRN,'#eaf6ee')
    for (dx,dy) in ((-2.5,1),(2.5,1),(2.5,6),(-2.5,6)): iline((xs+dx,yb0+dy,zf),(xs+dx,yb0+dy,zf-7),1,GRN)
    a=P(xs,yb0+3.5,zf-7); arr(a[0],a[1]+2,a[0],a[1]+16,GRN,1.4)
    # arka kavrama + ara mil (kısa kaplar için duvara kadar)
    if yb0+L < 84-WALLT-1: iline((xs,yb0+L,zf+3.5),(xs,84-WALLT,zf+3.5),1.2,BLU,'4,3')
    ipoly([(xs-2,yb0+L,zf+1.5),(xs+2,yb0+L,zf+1.5),(xs+2,yb0+L+2,zf+1.5),(xs-2,yb0+L+2,zf+1.5)],.9,BLU,'#dfe7fb')
    # etiket
    t=P((x0+x1)/2, yb0+L*0.55, zf+Hh+3); tx(t[0],t[1]-4,lab,8.5,'middle','bold'); tx(t[0],t[1]+6,alt,6.2,'middle','','#333')

# çizim sırası: arkadan öne, soldan sağa (kat 1 kaşar uzun → önce), sonra kat 2
kap(2,34.5,YF,LKA,Z['k1'][0],HK1,True,KAS,'KAŞAR','32,5 × 70 × 55 · %.0f L · %.0f kg · hafta' % (vKA, vKA*0.41))
kap(35.5,68,YF,LKS,Z['k1'][0],HK1,False,DIG,'KAVURMA','32,5 × 20 × 55 · 3 gün · 3,3 kg')
kap(2,34.5,YF,LKS,Z['k2'][0],HK2,True,DIG,'SUCUK KÜP','32,5 × 20 × 40 · %.1f L · hafta 8,4 kg' % vS)
kap(35.5,68,YF,LKS,Z['k2'][0],HK2,False,DIG,'KUŞBAŞI','32,5 × 20 × 40 · 3 gün · 4 kg')
# tepsiler (boşluklarda), ağız altında
for (z,x) in ((Z['b1'][0]+3,31),(Z['b2'][0]+3,31)):
    cpt=P(x,YF+10,z); elp(cpt[0],cpt[1],17*S*0.95,17*S*0.5,1.2,BLU,'#dfe7fb',.9,-30)
    cpt2=P(x+17,YF+10,z); tx(cpt2[0]+12,cpt2[1],'tepsi Ø34 — spiral',6.2,'start','',BLU)
# teknik alt çizgisi
ipoly([(0,0,Z['tek'][0]),(70,0,Z['tek'][0]),(70,84-WALLT,Z['tek'][0]),(0,84-WALLT,Z['tek'][0])],.8,'#999','#f3f3f3',None,.5)
t=P(35,40,Z['tek'][0]+3); tx(t[0],t[1],'teknik bölme (soğutma + elektrik) 27 ↑',6.5,'middle','',GRY)
# etiketler: ön ok, arka duvar, motor
a=P(-6,-4,Z['k2'][0]+20); arr(a[0]-40,a[1]+24,a[0],a[1],AMB,1.6); tx(a[0]-44,a[1]+36,'ÖN (robot)',8,'middle','bold',AMB)
t=P(70,84-WALLT/2,zhi+4); tx(t[0]+6,t[1],'ARKA DUVAR 10 — motorlar + sürücüler içinde',7.5,'start','bold',BLU)
t=P(70,84-WALLT+4,Z['k1'][0]+4); tx(t[0]+8,t[1]+3,'motor (gizli)',6.2,'start','',BLU)
t=P(70,84-WALLT+4,Z['k2'][0]+4); tx(t[0]+8,t[1]+3,'motor (gizli)',6.2,'start','',BLU)
t=P(68,YF+LKS+2,Z['k1'][0]+3.5); tx(t[0]+8,t[1]-6,'ara mil (duvara)',5.8,'start','',BLU)
t=P(35,0,Z['b1'][0]+7); tx(t[0]-90,t[1]+40,'boşluk 1 · 14 (tepsi düzlemi 1)',6.2,'start','',BLU)
t=P(35,0,Z['b2'][0]+7); tx(t[0]-90,t[1]+40,'boşluk 2 · 14 (tepsi düzlemi 2)',6.2,'start','',BLU)
t=P(0,0,zlo); tx(t[0]-4,t[1]+12,'ALT 42 ↓ (yedekler / çözülme / park)',6.2,'start','',GRY)
# renk anahtari
lx,ly=X0+330,Y0-217*S+6
for i,(col,lab) in enumerate(((GRN,'helezon (dozaj, ~20 g/tur)'),(PUR,'tarak (köprü kırıcı, pimli mil)'),(BLU,'kavrama / ara mil / motor'),(GRN,'ağız → tepsi'))):
    ln(lx,ly+i*13,lx+18,ly+i*13,2.2 if i!=3 else 1.4,col); tx(lx+24,ly+i*13+3,lab,6.5,'start','','#333')

# ================= ÖN KESİT (kompakt) =================
XC,YC = 900,100
tx(XC+105,YC-6,'ÖN KESİT (helezon hattı) 1:4',8.5,'middle','bold')
K=2.5
rc(XC,YC,K*70,K*197,1.8)
zz=197
for ad,(z0,z1) in (('teknik',Z['tek']),('KAT 1',Z['k1']),('boşluk 1',Z['b1']),('KAT 2',Z['k2']),('boşluk 2',Z['b2']),('ALT',Z['alt'])):
    col={'teknik':'#f3f3f3','boşluk 1':'#eef3ff','boşluk 2':'#eef3ff','ALT':'#f7f6f2'}.get(ad,'#fff')
    rc(XC,YC+K*(197-z1),K*70,K*(z1-z0),.7,0,'#111',None,col); tx(XC+K*70+4,YC+K*(197-(z0+z1)/2)+3,'%s %g'%(ad,z1-z0),5.4,'start','',GRY)
def kesit_on(x0,Hh,zf,slope_left,fill,lab):
    Zc=lambda c: YC+K*(197-zf-c)
    if slope_left: pts=[(x0,SL),(x0,Hh),(x0+WK,Hh),(x0+WK,0),(x0+WK-7,0)]
    else: pts=[(x0,0),(x0+7,0),(x0+WK,SL),(x0+WK,Hh),(x0,Hh)]
    poly([(XC+K*x,Zc(z)) for (x,z) in pts],1.1,'#111',fill)
    xs = x0+WK-3.5 if slope_left else x0+3.5; xa = x0+WK-9 if slope_left else x0+9
    o.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#fff" stroke="%s" stroke-width="1"/>' % (XC+K*xs,Zc(3.5),K*3.5,GRN))
    o.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="none" stroke="%s" stroke-width=".8" stroke-dasharray="3,2"/>' % (XC+K*xa,Zc(16),K*5.5,PUR))
    ln(XC+K*xs,Zc(0),XC+K*xs,Zc(-6),1.6,GRN)
    tx(XC+K*(x0+WK/2),Zc(Hh-8),lab,6,'middle','bold')
kesit_on(2,HK1,Z['k1'][0],True,KAS,'KAŞAR'); kesit_on(35.5,HK1,Z['k1'][0],False,DIG,'KAVURMA')
kesit_on(2,HK2,Z['k2'][0],True,DIG,'SUCUK KÜP'); kesit_on(35.5,HK2,Z['k2'][0],False,DIG,'KUŞBAŞI')
for z in (Z['b1'][0]+3,Z['b2'][0]+3):
    o.append('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="#dfe7fb" stroke="%s" stroke-width="1"/>' % (XC+K*35,YC+K*(197-z),K*17,K*1.2,BLU))
tx(XC+K*35,YC+K*197+14,'70',7,'middle','bold'); tx(XC-8,YC+K*98,'197',7,'end','bold')
tx(XC+K*35,YC+K*197+26,'27+58+14+42+14+42 = 197 ✓',6.5,'middle','bold',GRN)

# ================= TABLO =================
XT,YT = 900,640
rc(XT,YT,530,420,1.4,4)
tx(XT+14,YT+22,'DÖRT KAP — aynı iç (tarak + helezon), farklı boy',10,'start','bold')
hdr=['kap','ölçü (en×boy×yük)','hacim','dolum','gün','kim']
cx_=[XT+14,XT+100,XT+220,XT+280,XT+360,XT+410]
for i,h in enumerate(hdr): tx(cx_[i],YT+46,h,6.8,'start','bold',GRY)
ln(XT+12,YT+52,XT+518,YT+52,.8,'#bbb')
rows=[('KAŞAR','32,5 × 70 × 55','%.0f L' % vKA,'42 kg','6,9 (hafta)','eleman doldurur'),
      ('KAVURMA','32,5 × 20 × 55','%.0f L' % vKV,'3,3 kg','3','robot değiştirir'),
      ('SUCUK KÜP','32,5 × 20 × 40','%.1f L' % vS,'8,4 kg','7 (hafta)','eleman doldurur'),
      ('KUŞBAŞI','32,5 × 20 × 40','%.1f L' % vS,'4 kg','3','robot değiştirir')]
for i,r in enumerate(rows):
    yy=YT+70+i*18
    for j,v in enumerate(r): tx(cx_[j],yy,v,6.6,'start','bold' if j==0 else '','#111' if j==0 else '#333')
ln(XT+12,YT+146,XT+518,YT+146,.8,'#bbb')
notes=[('Kroki birebir: üst sol kaşar uzun (tam derinlik), üst sağ kavurma kısa ama AYNI yükseklik; alt kat sucuk küp + kuşbaşı.',GRN,'bold'),
       ('Sucuk KÜP, kavurma PARÇA → bıçak, çubuk, magazin YOK. Dört kap aynı iç: tek tarak (pimli mil) + dozaj helezonu.',GRN,'bold'),
       ('Arka duvar 10 cm kalın: motorlar, sürücüler ve kablolar içinde gizli; kap itilince helezon mili duvardaki pençeye oturur.',BLU,''),
       ('Kısa kaplar önde (ağız y 74 ≥ 31 kuralı); duvara kadar ara mil (mavi kesikli). Ağızlar x 31 / 39 = bant.',BLU,''),
       ('Kesit asimetrik kama: dış duvar 45°, iç duvar dik, oluk bant kenarında; tarak eğimli tarafa kaydırılmış.','#333',''),
       ('Kavurma kabı 55 yüksek → %11 dolu (3 gün 3,3 kg) — krokideki gibi aynı yükseklik; STORE −18 çekmecesine (29) sığmaz →',AMB,''),
       ('   kavurma yedeği donmuş poşet olarak STORE'+chr(39)+'da, ALT'+chr(39)+'ta çözülme kabı; ya da kavurma kabı 40 (alt kat gibi). Karar senin.',AMB,''),
       ('Robot: kavurma + kuşbaşı 3 günde 1 (kap ≤ 10 kg). Eleman: kaşar + sucuk haftalık. Tepsi düzlemleri 100 / 45 cm.','#333',''),
       ('Derinlik: 4 klape + 70 kaşar + 10 duvar = 84 ✓ · dikey 197 ✓ · kaşar 42 kg = hafta ✓ · sucuk küp %.1f L ≥ 8,4 kg (15 L) ✓' % vS,GRN,'')]
for i,(s,c,fw) in enumerate(notes): tx(XT+14,YT+164+i*17,s,6.3,'start',fw,c)
tx(XT+14,YT+330,'Değişen: sucuk kesme/çubuk fikri iptal (küp) · kaşar ve kavurma aynı yükseklik · motorlar kalın arka duvarda.',6.4,'start','bold','#111')
tx(XT+14,YT+346,'Değişmeyen: papyon dizilim, 2 kat + 2 tepsi düzlemi, ağız bandı, kapta elektrik yok.',6.4,'start','','#333')
tx(XT+14,YT+366,'Sonraki: HAT v45 (TOPPING v20) · kaşar tek eğim + tarak prototipi · kavurma kabı 55 / 40 kararı.',6.4,'start','',GRY)
tx(W-40,H-12,'AUTOKITCH · arastirma/3_TOPPING/ist3_topping_detay_v20 · 5 Eyl 2026 · kroki: Kemal',7,'end','',GRY)
o.append('</svg>')
svg = chr(10).join(o)
xml.dom.minidom.parseString(svg.encode('utf-8'))
out = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\3_TOPPING\ist3_topping_detay_v20.svg"
io.open(out,'w',encoding='utf-8').write(svg)
print('yazildi + XML gecerli | kasar %.0f L → %.0f kg · kavurma %.0f L · kucuk %.1f L' % (vKA, vKA*0.41, vKV, vS))
