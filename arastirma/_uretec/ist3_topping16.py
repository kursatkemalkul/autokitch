# -*- coding: utf-8 -*-
# TOPPING v16 — EN DOĞRU GEOMETRİ (v4 ideal kama huni: dikdörtgen, V-oluk 45°, tam boy helezon = canlı taban, tarak) + KARAR C (helezon, ağız uçta)
# haftalık kaset kurgusuna göre boyutlandırıldı (kaşar 15 kg × 4 · sucuk 10 kg × 2 · kav/kuş 3,5 kg × 4) · papyon dizilim · 2 kat + 2 düzlem · yedek arkada
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
def el(x,y,rx,ry,sw=1,c='#111',d=None,f='none'):
    o.append('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="%s" stroke="%s" stroke-width="%s"%s/>' % (x,y,rx,ry,f,c,sw,(' stroke-dasharray="%s"'%d) if d else ''))
def tx(x,y,s,fs=9,anc='start',fw='',col='#111'):
    o.append('<text x="%.1f" y="%.1f" font-size="%s" text-anchor="%s" font-weight="%s" fill="%s" font-family="Segoe UI, Arial, sans-serif">%s</text>' % (x,y,fs,anc,fw or 'normal',col,esc(s)))
def path(d,sw=1,c='#111',f='none',dash=None):
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="%s"%s stroke-linejoin="round"/>' % (d,f,c,sw,(' stroke-dasharray="%s"'%dash) if dash else ''))
def poly(pts,sw=1,c='#111',f='none',d=None):
    o.append('<polygon points="%s" fill="%s" stroke="%s" stroke-width="%s"%s/>' % (' '.join('%.1f,%.1f'%p for p in pts),f,c,sw,(' stroke-dasharray="%s"'%d) if d else ''))
def arr(x1,y1,x2,y2,c='#c0392b',w=1.2):
    ln(x1,y1,x2,y2,w,c); a=math.atan2(y2-y1,x2-x1)
    for s in (1,-1): ln(x2,y2,x2-6*math.cos(a-s*.42),y2-6*math.sin(a-s*.42),w,c)

GRN, RED, BLU, GRY, AMB, PUR = '#1d7a4f', '#c0392b', '#1a49b8', '#666', '#b7791f', '#6b4fa8'
FILL, MAT, SUC, LIGHT = '#f1efe8', '#e9dfa8', '#e8eef8', '#f7f6f2'
K = 2.5
# --- kaset ölçüleri (L = helezon boyu x, W = derinlik y, H) ---
KAS = {'kasar':(27,38,44,'KAŞAR',14.6), 'sucuk':(27,19,27,'SUCUK',10.0), 'kk':(27,17,18,'KAV/KUŞ',3.5)}
def hacim(L,W,Hh):
    w=W/2; v_loss=(w*w-12.25)*L/1000.0; return L*W*Hh/1000.0, v_loss, L*W*Hh/1000.0-v_loss
gK,vK,uK = hacim(27,38,44); gk,vk,uk = hacim(27,17,18)
GAP, KAN, KLP = 4.0, 3.0, 3.0          # duvar motor boşluğu, arka kanal, klape
YC = 84-KLP-38/2                        # çalışan kaşar merkezi y = 62
YB = KAN+38/2                           # yedek merkezi y = 22
Z = [('teknik',27,'#f3f3f3'),('KAT 1',47,'#fff'),('BOŞLUK 1',14,'#eef3ff'),('KAT 2',47,'#fff'),('BOŞLUK 2',14,'#eef3ff'),('RAF',48,'#f7f6f2')]
assert sum(z[1] for z in Z)==197
zt={}; acc=0
for ad,h,_ in Z: zt[ad]=acc; acc+=h
z1,zb1,z2,zb2,zr = zt['KAT 1'],zt['BOŞLUK 1'],zt['KAT 2'],zt['BOŞLUK 2'],zt['RAF']

o.append('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">' % (W,H,W,H))
rc(0,0,W,H,0,0,'none',None,'#fff')
tx(30,42,'AUTOKITCH — İSTASYON 3 · TOPPING v16 (4 Eyl 2026) — EN DOĞRU GEOMETRİ (dikdörtgen kama huni + tam boy helezon + tarak) · haftalık kaset kurgusuna göre ölçü · papyon · 2 kat · 70 × 197 × 84 · cm',15,'start','bold')
tx(30,66,'Kaset = v4 ideal form + v5-C helezon: üstten dikdörtgen, iki yan duvar 45° V ile ortadaki tam boy helezona iner (canlı taban), tarak V ağzında, uç duvarlar dik, ağız helezonun iç ucunda (bant). Ölçüler v7 kurgusu: kaşar 15 kg ×4 (2,3 gün) · sucuk 10 kg ×2 (hafta) · kav/kuş 3,5 kg ×4 (3 gün, 2 donmuş STORE).',9.5,'start','','#444')
ln(30,78,W-30,78,.8,'#999')

# ================= ÖN KESİT A-A (helezon eksenleri; kademeli: kaşar/sucuk y 62, kav y 52,5) =================
X0,Y0 = 60,120
tx(X0+K*35,Y0-10,'ÖN KESİT A-A (helezon eksenleri) 1:4',9,'middle','bold')
rc(X0,Y0,K*70,K*197,2.2)
zz=0
for ad,h,col in Z:
    rc(X0,Y0+K*zz,K*70,K*h,.8,0,'#111',None,col); zz+=h
rc(X0+K*3,Y0+K*3,K*30,K*21,1,2,'#111',None,'#fff'); tx(X0+K*18,Y0+K*12,'SOĞUTMA',6.5,'middle','bold'); tx(X0+K*18,Y0+K*18,'1/12 HP · +3',5.6,'middle','')
rc(X0+K*37,Y0+K*3,K*30,K*21,1,2,'#111',None,'#fff'); tx(X0+K*52,Y0+K*10,'ELEKTRİK',6.5,'middle','bold'); tx(X0+K*52,Y0+K*15,'PLC · 24 V PSU',5,'middle',''); tx(X0+K*52,Y0+K*20,'5 sürücü',5,'middle','')
def kaset_on(x0, sgn, zfloor, L, Hh, ad, alt, tip='helezon', tarak2=False, light=False, fill=MAT):
    # x0: tip ucu (duvar tarafı) x; sgn +1 sağa doğru (sol kaset), -1 (sağ kaset); ağız iç uçta
    X=lambda c: X0+K*(x0+sgn*c); Zc=lambda c: Y0+K*(zfloor-c)
    col='#999' if light else '#111'; d='3,2' if light else None
    rc(min(X(0),X(L)),Zc(Hh),K*L,K*Hh,1.2,1,col,d,LIGHT if light else FILL)
    if not light:
        rc(min(X(.3),X(L-.3)),Zc(Hh-4),K*(L-.6),K*(Hh-4-7.3),0,0,'none',None,fill)
        if tip=='helezon':
            rc(min(X(1),X(L-1)),Zc(7),K*(L-2),K*7,1,2,'#111',None,'#fff')
            for k in range(1,int((L-2)/2.5)): ln(X(1+k*2.5),Zc(7),X(1+k*2.5),Zc(0),.6,'#999')
            ln(X(1),Zc(3.5),X(L-1),Zc(3.5),.8,'#555','3,2')
            ln(X(1),Zc(13),X(L-1),Zc(13),1.2,BLU)
            for k in range(int((L-2)/3)):
                r_=2+k*3; s=1 if k%2==0 else -1; ln(X(r_),Zc(13),X(r_),Zc(13+s*4.5),.8,BLU)
            if tarak2:
                ln(X(1),Zc(30),X(L-1),Zc(30),1.2,BLU)
                for k in range(int((L-2)/3)):
                    r_=3.5+k*3; s=1 if k%2==0 else -1; ln(X(r_),Zc(30),X(r_),Zc(30+s*4.5),.8,BLU)
        else:  # çubuk + bıçak
            for k in range(6): rc(min(X(3+k*3.6),X(3+k*3.6+2.6)),Zc(Hh-2),K*2.6,K*(Hh-5),.7,1,'#555',None,'#f4ece6')
            rc(min(X(L-6),X(L-2)),Zc(4),K*4,K*3,1,1,RED,None,'#fdeeee'); tx(X(L-4),Zc(1),'bıçak',4.2,'middle','bold',RED)
        # ağız iç uçta (L-3 .. L-1)
        rc(min(X(L-3),X(L-1)),Zc(0),K*2,K*1.2,0,0,'none',None,'#fff'); ln(X(L-2),Zc(0),X(L-2),Zc(-5),1.6,GRN)
        # tip dişlisi + duvar motoru (pancake, 4 cm boşluk)
        ci(X(-0.5),Zc(3.5),K*1.8,.9,'#555',None,'#eee')
        rc(min(X(-GAP),X(-0.5)),Zc(7),K*(GAP-0.5),K*7,1,1,BLU,None,'#dfe7fb'); tx(X(-GAP/2-0.2),Zc(1.6),'M',4.4,'middle','bold',BLU)
    if ad: tx(X(L/2),Zc(Hh-9),ad,6,'middle','bold','#999' if light else '#111'); tx(X(L/2),Zc(Hh-14),alt,4.6,'middle','','#999' if light else '#333')
for zL,left,right in ((z1,('KAŞAR A','27×38×44 · 14,6 kg'),('SUCUK','27×19×27 · çubuk')),(z2,('KAŞAR B','27×38×44 · 14,6 kg'),('KAVURMA','27×17×18 · kesit y 52,5'))):
    zfloor=zL+45
    rc(X0,Y0+K*zfloor,K*70,K*2,1,0,'#111',None,'#bbb')
    for xx in (31,39): rc(X0+K*(xx-1.5),Y0+K*zfloor,K*3,K*2,0,0,'none',None,'#fff')
    kaset_on(GAP,+1,zfloor,27,44,left[0],left[1],'helezon',True)
    if right[0]=='SUCUK': kaset_on(70-GAP,-1,zfloor,27,27,right[0],right[1],'cubuk')
    else: kaset_on(70-GAP,-1,zfloor,27,18,right[0],right[1],'helezon')
    rc(X0+K*1,Y0+K*(zL+0.5),K*68,K*46,.8,2,'#111','3,2')
tx(X0+K*70+6,Y0+K*(z1+8),'KAT 1 · 47: kaşar A | sucuk',6.5,'start','bold'); tx(X0+K*70+6,Y0+K*(z1+16),'ağızlar (31, 62) · (39, 62)',5.6,'start','',GRN); tx(X0+K*70+6,Y0+K*(z1+23),'klape ön, motorlu, izole · +3 °C',5.4,'start','',BLU); tx(X0+K*70+6,Y0+K*(z1+30),'kaşarda çift tarak (z 13 · 30)',5.4,'start','',BLU)
tx(X0+K*70+6,Y0+K*(z2+8),'KAT 2 · 47: kaşar B | kavurma + kuşbaşı',6.5,'start','bold'); tx(X0+K*70+6,Y0+K*(z2+16),'sağda 2 kaset yan yana (y): ağız (39, 52,5) · (39, 71,5)',5.6,'start','',GRN); tx(X0+K*70+6,Y0+K*(z2+23),'kuşbaşı bu kesitte görünmez (y 71,5)',5.4,'start','',GRY)
for zb,lab in ((zb1,'BOŞLUK 1 · düzlem 1 (sucuklu) · tepsi 111 cm'),(zb2,'BOŞLUK 2 · düzlem 2 (kav/kuş) · tepsi 50 cm')):
    el(X0+K*35,Y0+K*(zb+10.5),K*17,K*1.2,1.2,BLU,None,'#dfe7fb'); tx(X0+K*35,Y0+K*(zb+8),'tepsi Ø34 · spiral',5,'middle','',BLU)
    tx(X0+K*70+6,Y0+K*(zb+8),lab,6.3,'start','',BLU)
# raf: on yuvalar park (bos kasar kaseti sigar 44 ≤ 48)
zfloor=zr+46
rc(X0,Y0+K*zfloor,K*70,K*2,1,0,'#111',None,'#bbb')
kaset_on(GAP,+1,zfloor,27,44,'PARK','boş kaşar kaseti','helezon',False,True)
kaset_on(70-GAP,-1,zfloor,27,44,'PARK','boş kaşar kaseti','helezon',False,True)
tx(X0+K*70+6,Y0+K*(zr+12),'RAF · 48: önde 2 PARK (boş kaşar 44 sığar)',6.3,'start','',GRY); tx(X0+K*70+6,Y0+K*(zr+20),'arkada 2: boş kav / kuş kaseti (4. kaset)',5.4,'start','','#333')
ln(X0,Y0+K*197+16,X0+K*70,Y0+K*197+16,.8); tx(X0+K*35,Y0+K*197+28,'70',8,'middle','bold')
ln(X0-14,Y0,X0-14,Y0+K*197,.8); tx(X0-18,Y0+K*98,'197',8,'end','bold')
zz=0
for ad,h,_ in Z: tx(X0-18,Y0+K*(zz+h/2)+3,'%g'%h,5.2,'end','',GRY); zz+=h
tx(X0+K*35,Y0+K*197+42,'27+47+14+47+14+48 = 197 ✓',7,'middle','bold',GRN)
tx(X0+K*35,Y0+K*197+54,'kesit kademeli: kaşar/sucuk y 62, kavurma y 52,5',5.4,'middle','',GRY)

# ================= YAN KESİT B-B (x 31 — sol ağız hattı) =================
XS,YS = 320,120
tx(XS+K*42,YS-10,'YAN KESİT B-B (x 31, sol ağız hattı) 1:4',9,'middle','bold')
rc(XS,YS,K*84,K*197,2.2)
zz=0
for ad,h,col in Z:
    rc(XS,YS+K*zz,K*84,K*h,.8,0,'#111',None,col); zz+=h
rc(XS+K*2,YS+K*2,K*80,K*23,1,2,'#111',None,'#fff'); tx(XS+K*42,YS+K*14,'teknik: soğutma + elektrik (üstten servis)',5.6,'middle','')
def v_sec(yc, zfloor, Wd, Hh, light=False, lab='', tarak2=False):
    Yy=lambda y: XS+K*y; Zc=lambda c: YS+K*(zfloor-c)
    w=Wd/2; vd=w-3.5
    col='#999' if light else '#111'; d='3,2' if light else None
    poly([(Yy(yc-w),Zc(Hh)),(Yy(yc+w),Zc(Hh)),(Yy(yc+w),Zc(vd)),(Yy(yc+3.5),Zc(0)),(Yy(yc-3.5),Zc(0)),(Yy(yc-w),Zc(vd))],1.2,col,LIGHT if light else FILL,d)
    if not light:
        poly([(Yy(yc-w+.3),Zc(Hh-4)),(Yy(yc+w-.3),Zc(Hh-4)),(Yy(yc+w-.3),Zc(vd)),(Yy(yc+3.5),Zc(0.3)),(Yy(yc-3.5),Zc(0.3)),(Yy(yc-w+.3),Zc(vd))],0,'none',MAT)
        ci(Yy(yc),Zc(3.5),K*3.5,1,'#111',None,'#fff')
        for k in range(6):
            a=math.radians(k*60+20); ln(Yy(yc),Zc(3.5),Yy(yc)+K*3.5*math.cos(a),Zc(3.5)+K*3.5*math.sin(a),.6,'#999')
        ci(Yy(yc),Zc(13),K*5.5,.8,BLU,'3,2'); ci(Yy(yc),Zc(13),K*0.6,1,BLU,None,'#dfe7fb')
        if tarak2: ci(Yy(yc),Zc(30),K*5.5,.8,BLU,'3,2'); ci(Yy(yc),Zc(30),K*0.6,1,BLU,None,'#dfe7fb')
        tx(Yy(yc-w)+3,Zc(vd/2),'45°',4.4,'start','bold',AMB)
    if lab: tx(Yy(yc),Zc(Hh-9),lab,5.4,'middle','bold','#999' if light else '#111')
for zL,ad in ((z1,'KAŞAR A'),(z2,'KAŞAR B')):
    zfloor=zL+45
    rc(XS+K*2,YS+K*zfloor,K*80,K*2,1,0,'#111',None,'#bbb'); rc(XS+K*(YC-1.5),YS+K*zfloor,K*3,K*2,0,0,'none',None,'#fff')
    v_sec(YC,zfloor,38,44,False,ad,True); v_sec(YB,zfloor,38,44,True,'yedek (arka)')
    tx(XS+K*YB,YS+K*(zfloor-30),'aynı rayda',4.6,'middle','',GRY); tx(XS+K*YB,YS+K*(zfloor-26),'öne çekilir →',4.6,'middle','',GRY)
    ln(XS+K*YC,YS+K*(zfloor+2),XS+K*YC,YS+K*(zfloor+6),1.6,GRN); tx(XS+K*(YC+3),YS+K*(zfloor+6),'ağız',5,'start','bold',GRN)
    rc(XS+K*81,YS+K*(zL+0.5),K*3,K*46,1,0,BLU,None,'#dfe7fb'); rc(XS+K*1,YS+K*(zL+0.5),K*80,K*46,.8,2,'#111','3,2')
for zb in (zb1,zb2):
    rc(XS+K*(YC-17),YS+K*(zb+10.5),K*34,K*1.5,1.1,BLU,None,'#dfe7fb'); rc(XS+K*(YC+17),YS+K*(zb+9.5),K*6,K*3,1,BLU,None,'#dfe7fb')
    tx(XS+K*(YC-2),YS+K*(zb+8.5),'tepsi (merkez y 62)',4.8,'middle','',BLU)
    rc(XS,YS+K*(zb+12),K*84,K*2,1,0,'#111',None,'#bbb')
zfloor=zr+46
rc(XS+K*2,YS+K*zfloor,K*80,K*2,1,0,'#111',None,'#bbb')
v_sec(YC,zfloor,38,44,True,'PARK'); v_sec(YB,zfloor,17,18,True,'boş kav')
rc(XS+K*81,YS+K*(zr+0.5),K*3,K*47,1,0,BLU,None,'#dfe7fb')
tx(XS+K*84+4,YS+K*(z1+6),'KAT 1',6,'start','bold'); tx(XS+K*84+4,YS+K*(z1+13),'W 38: V yarı genişlik 19,',5,'start','','#333'); tx(XS+K*84+4,YS+K*(z1+19),'V derinliği 15,5 (45°)',5,'start','','#333'); tx(XS+K*84+4,YS+K*(z1+25),'helezon Ø7 · tarak ×2 Ø11',5,'start','',BLU); tx(XS+K*84+4,YS+K*(z1+31),'dik duvar 28,5 (depo)',5,'start','','#333')
tx(XS+K*84+4,YS+K*(zb1+8),'boşluk 1 · taban sabit plaka',5.4,'start','',BLU)
tx(XS+K*84+4,YS+K*(z2+6),'KAT 2',6,'start','bold'); tx(XS+K*84+4,YS+K*(z2+13),'yedek arkada, aynı ray',5,'start','','#333'); tx(XS+K*84+4,YS+K*(z2+19),'derinlik 3+38+2+38+3 = 84',5,'start','',GRY)
tx(XS+K*84+4,YS+K*(zb2+8),'boşluk 2',5.4,'start','',BLU)
tx(XS+K*84+4,YS+K*(zr+12),'RAF: park önde / boş küçük arkada',5.4,'start','',GRY); tx(XS+K*84+4,YS+K*(zr+20),'klape: kat 1, kat 2, raf',5,'start','',BLU)
ln(XS,YS+K*197+16,XS+K*84,YS+K*197+16,.8); tx(XS+K*42,YS+K*197+28,'84 · arka ← y → ön',8,'middle','bold')

# ================= ÜST GÖRÜNÜŞ KAT 1 / KAT 2 =================
XU,YU = 600,120
KU=2.35
def plan(X,Y,baslik,kat):
    tx(X+KU*35,Y-8,baslik,8.5,'middle','bold')
    rc(X,Y,KU*70,KU*84,1.4)
    rc(X+KU*31,Y,KU*8,KU*84,0,0,'none',None,'#dff3e6')
    def kut(x0,sgn,yc,L,Wd,light,f,lab='',alt='',tip='helezon'):
        xa=min(x0,x0+sgn*L); rc(X+KU*xa,Y+KU*(yc-Wd/2),KU*L,KU*Wd,1 if not light else .8,1,'#111' if not light else '#999','3,2' if light else None,f if not light else LIGHT)
        if not light:
            if tip=='helezon':
                ln(X+KU*(xa+1),Y+KU*(yc-3.5),X+KU*(xa+L-1),Y+KU*(yc-3.5),.6,AMB,'2,2'); ln(X+KU*(xa+1),Y+KU*(yc+3.5),X+KU*(xa+L-1),Y+KU*(yc+3.5),.6,AMB,'2,2')
                ln(X+KU*(xa+1),Y+KU*yc,X+KU*(xa+L-1),Y+KU*yc,1.1,BLU)
            else:
                for k in range(5): ci(X+KU*(xa+4+k*4.5),Y+KU*yc,KU*1.8,.6,'#555',None,'#f4ece6')
            ax=x0+sgn*(L-2); ci(X+KU*ax,Y+KU*yc,2.6,1.3,GRN,None,'#fff'); ci(X+KU*ax,Y+KU*yc,1,1,GRN,None,GRN)
            ci(X+KU*(x0-sgn*0.5),Y+KU*yc,2,1,'#555',None,'#eee')
            rc(X+KU*min(x0-sgn*GAP,x0-sgn*0.5),Y+KU*(yc-3.5),KU*(GAP-0.5),KU*7,1,1,BLU,None,'#dfe7fb')
        if lab: tx(X+KU*(xa+L/2),Y+KU*(yc-2),lab,5.2,'middle','bold','#999' if light else '#111')
        if alt: tx(X+KU*(xa+L/2),Y+KU*(yc+6),alt,4.2,'middle','','#999' if light else '#333')
    kut(GAP,+1,YC,27,38,False,FILL,'KAŞAR A' if kat==1 else 'KAŞAR B','27×38 · helezon → ağız')
    kut(GAP,+1,YB,27,38,True,FILL,'yedek (arka)','öne alınır')
    if kat==1:
        kut(70-GAP,-1,YC,27,19,False,SUC,'SUCUK','çubuk + bıçak','cubuk')
        kut(70-GAP,-1,YB,27,19,True,SUC,'2. sucuk','eleman','cubuk')
        outs=((31,YC),(39,YC))
    else:
        kut(70-GAP,-1,52.5,27,17,False,SUC,'KAVURMA','27×17')
        kut(70-GAP,-1,71.5,27,17,False,SUC,'KUŞBAŞI','27×17')
        kut(70-GAP,-1,12.5,27,17,True,SUC,'kav. yedek','çözülür')
        kut(70-GAP,-1,31.5,27,17,True,SUC,'kuş. yedek','çözülür')
        outs=((31,YC),(39,52.5),(39,71.5))
    for (ox,oy) in outs: ci(X+KU*ox,Y+KU*oy,KU*31,.8,GRN,'5,3')
    rc(X,Y+KU*81,KU*70,KU*3,1,0,BLU,None,'#dfe7fb'); tx(X+KU*35,Y+KU*83.2,'klape',4.2,'middle','',BLU)
    rc(X,Y,KU*70,KU*3,0,0,'none',None,'#e5e5e5'); tx(X+KU*35,Y+KU*2.3,'kanal 3',3.8,'middle','',GRY)
    arr(X+KU*17,Y+KU*(YB+8),X+KU*17,Y+KU*(YB+17),AMB,1)
    tx(X+KU*35,Y+KU*84+11,'süpürme R31: sol x 0-62 · sağ x 8-70 · y 31-93 ✓ (ön açık)',4.8,'middle','bold',GRN)
plan(XU,YU,'ÜST — KAT 1 (sucuklu düzlem)',1)
plan(XU,YU+KU*84+36,'ÜST — KAT 2 (kavurma / kuşbaşı düzlemi)',2)
tx(XU+KU*35,YU+2*KU*84+54,'üstten DİKDÖRTGEN: sarı kesikli = V-oluk yuvası, mavi = helezon, yeşil = ağız, M = duvar motoru (4 cm)',4.8,'middle','','#333')

# ================= KASET DETAYI (ideal form, 3 görünüş) =================
XD,YD = 600,600
rc(XD,YD,250,320,1.2,3,'#999',None,'#fcfdff')
tx(XD+125,YD+16,'KAŞAR KASETİ 27×38×44 — üst / ön / yan',7.5,'middle','bold')
KD=1.9
# ust
ux,uy = XD+18, YD+30
rc(ux,uy,KD*27,KD*38,1.1,0,'#111',None,FILL)
ln(ux+KD*1,uy+KD*15.5,ux+KD*26,uy+KD*15.5,.6,AMB,'2,2'); ln(ux+KD*1,uy+KD*22.5,ux+KD*26,uy+KD*22.5,.6,AMB,'2,2')
ln(ux+KD*1,uy+KD*19,ux+KD*26,uy+KD*19,1.1,BLU); ci(ux+KD*25,uy+KD*19,2.4,1.2,GRN,None,'#fff'); ci(ux-1,uy+KD*19,2,1,'#555',None,'#eee')
tx(ux+KD*13.5,uy+KD*38+9,'27',5,'middle','bold'); tx(ux-4,uy+KD*19+3,'38',5,'end','bold'); tx(ux+KD*13.5,uy-4,'ÜST',5,'middle','',GRY)
# on (helezon boyunca)
fx,fy = XD+90, YD+30
rc(fx,fy,KD*27,KD*44,1.1,0,'#111',None,FILL)
rc(fx+KD*1,fy+KD*37,KD*25,KD*7,.9,1,'#111',None,'#fff'); ln(fx+KD*1,fy+KD*31,fx+KD*26,fy+KD*31,1,BLU); ln(fx+KD*1,fy+KD*14,fx+KD*26,fy+KD*14,1,BLU)
ln(fx+KD*25,fy+KD*44,fx+KD*25,fy+KD*49,1.4,GRN); ci(fx-1,fy+KD*40.5,2,1,'#555',None,'#eee')
tx(fx+KD*13.5,fy-4,'ÖN (helezon boyu)',5,'middle','',GRY); tx(fx+KD*27+4,fy+KD*22,'44',5,'start','bold')
tx(fx+KD*13.5,fy+KD*10,'depo',4.4,'middle','','#333'); tx(fx+KD*13.5,fy+KD*28,'tarak z 13 / 30',4,'middle','',BLU)
# yan (V kesiti)
sx,sy = XD+170, YD+30
w=19; vd=15.5
poly([(sx,sy),(sx+KD*38,sy),(sx+KD*38,sy+KD*(44-vd)),(sx+KD*(19+3.5),sy+KD*44),(sx+KD*(19-3.5),sy+KD*44),(sx,sy+KD*(44-vd))],1.1,'#111',FILL)
ci(sx+KD*19,sy+KD*40.5,KD*3.5,.9,'#111',None,'#fff'); ci(sx+KD*19,sy+KD*31,KD*5.5,.7,BLU,'3,2'); ci(sx+KD*19,sy+KD*14,KD*5.5,.7,BLU,'3,2')
tx(sx+KD*19,sy-4,'YAN (V kesiti)',5,'middle','',GRY); tx(sx+3,sy+KD*37,'45°',4.4,'start','bold',AMB); tx(sx+KD*19,sy+KD*44+9,'38',5,'middle','bold')
tx(XD+125,YD+140,'gross %.1f L − V-oluk %.1f L = %.1f L → kaşar %.1f kg (0,41 kg/L) · 2,25 gün' % (gK,vK,uK,uK*0.41),4.8,'middle','','#333')
tx(XD+125,YD+152,'kaset boş ~3,5 kg (1,5 mm paslanmaz) → dolu ~18 kg → robot kolu ≥ 20 kg (⑦)',4.8,'middle','bold',RED)
rows=[('KAŞAR ×4','27×38×44','14,6 kg','2,3 gün','A, B çalışan · C, D arkada'),
      ('SUCUK ×2','27×19×27','10 kg çubuk','hafta','çalışan + arkada (eleman)'),
      ('KAV ×4','27×17×18','3,5 kg','3 gün','çalışan + arka (çözülür) + 2 STORE −18 + 1 boş'),
      ('KUŞ ×4','27×17×18','3,5 kg','3 gün','aynı')]
tx(XD+12,YD+172,'KASET KURGUSU (v7 kuralı: boy = güvenli gün × günlük; adet = haftalık parça + 1)',5.2,'start','bold')
cols=[XD+12,XD+70,XD+128,XD+178,XD+12]
for i,(a,b,c,d,e) in enumerate(rows):
    yy=YD+188+i*24
    tx(cols[0],yy,a,5.2,'start','bold'); tx(cols[1],yy,b,5,'start','','#333'); tx(cols[2],yy,c,5,'start','','#333'); tx(cols[3],yy,d,5,'start','','#333'); tx(cols[4],yy+10,e,4.6,'start','',GRY)
tx(XD+125,YD+292,'kav/kuş kaseti STORE −18 çekmecesine (29 yüksek, 61 modül): 2 yan yana ✓',4.8,'middle','',GRN)
tx(XD+125,YD+306,'helezon Ø7 tam boy 25 · hatve 2→4 · 30 dev/dk · ~20 g/tur kaşar',4.8,'middle','',BLU)

# ================= ELEKTRİK & TAHRİK =================
XE,YE = 870,120
rc(XE,YE,560,400,1.4,4,'#111',None,'#fcfdff')
tx(XE+14,YE+22,'ELEKTRİK & TAHRİK — kasette elektrik yok, motor duvarda (4 cm)',10,'start','bold')
kx,ky = XE+16,YE+36
rc(kx,ky,262,180,1,3,'#999',None,'#fff'); tx(kx+131,ky+14,'TİP DİŞLİSİ — yandan meshler',7,'middle','bold')
rc(kx+60,ky+30,190,44,1,0,'#111',None,FILL); tx(kx+160,ky+42,'kaset (pasif) — dış uç (duvar tarafı)',5.4,'middle','',GRY)
ln(kx+90,ky+58,kx+240,ky+58,1.5,'#333'); tx(kx+170,ky+68,'helezon mili (yatay, x yönünde, tam boy)',4.8,'middle','')
ci(kx+80,ky+58,10,1.1,'#111',None,'#eee'); ci(kx+58,ky+58,10,1.1,BLU,None,'#dfe7fb')
rc(kx+22,ky+70,50,30,1,2,'#111',None,'#eee'); tx(kx+47,ky+83,'M 40 W',5.4,'middle','bold'); tx(kx+47,ky+93,'pancake · enkoder',4.4,'middle','')
ln(kx+58,ky+68,kx+52,ky+72,1,BLU)
arr(kx+160,ky+24,kx+120,ky+24,AMB,1); tx(kx+170,ky+27,'kaset öne çekilir / arkadan gelir',4.6,'start','',AMB)
tx(kx+131,ky+118,'kaset raya itilince dış uç dişlisi motor dişlisine YANDAN girer',5,'middle','bold',BLU)
tx(kx+131,ky+130,'(pahlı diş) — arkadan öne alınan yedek aynı yere oturur',5,'middle','','#333')
tx(kx+131,ky+144,'tarak(lar) 1:20 aynı milden · slip ring yok, kablo yok',5,'middle','',GRN)
tx(kx+131,ky+158,'sucuk kasetinde aynı dişli bıçak milini çevirir',5,'middle','',AMB)
tx(kx+131,ky+172,'kaset komple bulaşık makinesine girer',5,'middle','bold',GRN)
bx,by = XE+290,YE+36
rc(bx,by,254,180,1,3,'#999',None,'#fff'); tx(bx+127,by+14,'KONTROL ŞEMASI',7,'middle','bold')
rc(bx+80,by+22,94,24,1.1,3,'#111',None,'#f3f3f3'); tx(bx+127,by+33,'PLC · 24 V · CAN',5.8,'middle','bold')
items=[('M1 kaşar A',BLU),('M2 sucuk bıçak',BLU),('M3 kaşar B',BLU),('M4 kavurma',BLU),('M5 kuşbaşı',BLU),('klape ×3',BLU),('yük hücresi ×5',AMB),('RFID ×5',PUR),('soğutma +3',GRY),('klape sensör',GRY)]
for i,(ad,col) in enumerate(items):
    x_=bx+10+(i%2)*120; y_=by+54+(i//2)*23
    rc(x_,y_,112,18,.9,2,col,None,'#fff'); tx(x_+56,y_+12,ad,5.2,'middle','bold',col)
    ln(bx+127,by+46,x_+56,y_,.5,'#999')
tx(bx+127,by+172,'5 sürücü · 5 tartı · 1 PLC · ~335 W tepe',5.2,'middle','bold',GRN)
ny=YE+232
tx(XE+14,ny,'DOZAJ (sucuklu pide, KAT 1):',8,'start','bold')
seq=['① robot tepsiyi düzlem 1'+chr(39)+'e (111 cm) getirir, (31, 62) altına · M1: kaşar A helezonu ağızdan döker, spiral 14 sn',
     '② ray altı yük hücresi kaset ağırlık farkını okur → 80 g'+chr(39)+'da durur (±3 g) · tepsi 8 cm sağa: (39, 62)',
     '③ M2: bıçak çubuktan 12 dilim keser (12 × 0,6 sn), dilimler ağızdan tepsiye · kat değişmez → fırına',
     '④ kavurmalı: KAT 2 (50 cm): kaşar B (31, 62) + kavurma (39, 52,5) · kuşbaşılı: kuşbaşı (39, 71,5)',
     '⑤ kaset ≤ 1 doz (tartı) ya da saat doldu (kaşar 14 g · sucuk 7 · kav/kuş 3,5) → DEĞİŞİM']
for i,s in enumerate(seq): tx(XE+14,ny+15+i*12.5,s,6.4,'start','','#333')
tx(XE+14,ny+86,'güç: 5×40 + klape 3×10 + soğutma 90 + PLC 15 → ~335 W tepe · ort. ~130 W',6.4,'start','bold',GRY)
tx(XE+14,ny+100,'yük hücresi kaset takılınca tartar (RFID + başlangıç) → her dozda fark → "boşaldı"; ayrı sensör yok',6.4,'start','','#333')
tx(XE+14,ny+114,'ağız kaset tabanında iç uçta; kat tabanındaki delik yalnız çalışan pozisyonda (yedekte taban kapalı)',6.4,'start','','#333')
tx(XE+14,ny+128,'kaşar 44 yüksek sütun → 2. tarak z 30 (rathole önlemi), aynı dişli katarından',6.4,'start','','#333')
tx(XE+14,ny+142,'tepsi düzlemleri 111 / 50 cm: bir pidede kat değişmez · kol yükü 18 kg → ≥ 20 kg kobot (⑦ AÇIK)',6.4,'start','bold',RED)

# ================= STOK · DEĞİŞİM =================
XT,YT = 870,540
rc(XT,YT,560,380,1.4,4)
tx(XT+14,YT+22,'STOK · DEĞİŞİM · HAFTALIK — v7 kaset kurgusu, yedek her kasetin arkasında',10,'start','bold')
rows=[('KAŞAR','A, B çalışan (2 kat) + C, D arkalarında = 4 × 14,6 = 58 kg ≥ 45,5 kg/hafta ✓ · her kat 2,25 günde 1 değişim'),
      ('SUCUK','çubuk kaseti 10 kg = hafta · arkasında 2. kaset (eleman değiştirir, robot dokunmaz)'),
      ('KAV / KUŞ','3,5 kg = 3 gün · yedeği arkada (+3'+chr(39)+'te çözülür) · 2 donmuş STORE −18 · 1 boş rafta = 4 kaset ✓'),
      ('RAF','önde 2 PARK (boşalan kaşar buraya) · arkada 2 boş kav / kuş kaseti'),
      ('STORE','−18 çekmecesi: kav ×2 | kuş ×2 (27×17×18 ≤ 29 ✓) · hafta ortası robot 1 donmuşu KAT 2 arka yuvaya taşır → 1 gün çözülür'),
      ('ELEMAN','haftada 1: 4 kaşar (dolu), 1 sucuk, 1+1 taze + 2+2 donmuş küçük; boşları toplar, kasetleri yıkar')]
for i,(a,b) in enumerate(rows):
    yy=YT+46+i*17; tx(XT+14,yy,a,6.8,'start','bold'); tx(XT+70,yy,b,6.2,'start','','#333')
ln(XT+12,YT+152,XT+548,YT+152,.8,'#bbb')
tx(XT+14,YT+170,'DEĞİŞİM (kaşar A boşaldı) — 2 hamle, ~40 sn:',7.5,'start','bold',BLU)
seq2=['① KAT 1 klapesi açılır → robot boş A'+chr(39)+'yı tutamaktan çeker → RAF PARK yuvasına koyar (44 ≤ 48)',
      '② arkadaki C'+chr(39)+'yi aynı raydan öne çeker: dış uç dişlisi meshler, RFID, tartı = başlangıç → klape kapanır',
      '③ eleman haftalık gelişte: parktaki boşları alır, arka yuvalara dolu C, D koyar (robot değil)',
      '④ kav/kuş: aynı mantık; boşalan STORE'+chr(39)+'daki donmuşla değil, arkada çözülmüş olanla değişir']
for i,s in enumerate(seq2): tx(XT+14,YT+186+i*12.5,s,6.4,'start','','#333')
tx(XT+14,YT+246,'v15 (üçgen) ile fark: kaset üstten dikdörtgen (ideal kama huni) · kaşar 5,5 → 14,6 kg (v7 kurgusu) · kaset sayısı 8 → 4',6.4,'start','bold',GRY)
tx(XT+14,YT+259,'kat yüksekliği 35 → 47 (kaşar 44) · raf 2 kat → 1 kat 48 · 2 düzlem 111 / 50 cm · helezon tam boy 25 (canlı taban)',6.4,'start','',GRY)
tx(XT+14,YT+272,'derinlik 3+38+2+38+3 = 84 ✓ · V-oluk W 38 → derinlik 15,5, üstünde 28,5 dik depo',6.4,'start','',GRY)
tx(XT+14,YT+292,'AÇIK: ⑦ robot yükü 18 kg → UR20 / CRX-25iA / Doosan H2515 sınıfı · kaşar 45° V + helezon akışı prototip',6.2,'start','',AMB)
tx(XT+14,YT+305,'· 44 cm kaşar sütununda rathole → 2. tarak · klape contası · sucuk çubuk kaseti detayı · tepsi 50 cm düzlemi (kobot erişimi)',6.2,'start','',AMB)
tx(XT+14,YT+318,'· sol ağız x 31 → süpürme sol duvara tam değer (pay 0): duvar iç yüzü düz, motor boşluğu duvar içinde',6.2,'start','',AMB)
tx(XT+14,YT+338,'Not: 2,3 gün → 2,25 gün (kaset 14,6 kg, yükseklik 44 sınırı); 15 kg için W 40 / H 45 → dikey 200 ✗ — kabul edilebilir fark',6.2,'start','bold',BLU)
tx(XT+14,YT+356,'Alternatif: kaşar kaseti 2 gün (13 kg, H 40) → kat 43, raf 44, dikey 193 → 4 cm pay',6.2,'start','',GRY)

# ================= KONTROL =================
YK=955
rc(60,YK,1370,215,1.6,4)
tx(76,YK+24,'KONTROL — kurallar ve HAT v45 etkisi',11,'start','bold')
rows=[('① çıkış bandı: ağızlar x 31 · 39 ∈ [31,39] ✓ · y 52,5-71,5 ≥ 31 ✓ · süpürme R31: sol x 0-62, sağ x 8-70 → duvar içinde (pay 0, düz iç yüzey)',GRN),
      ('② erişim: çalışan kasetlerin önünde hiçbir şey yok ✓ · yedek aynı rayda arkada ✓ · park rafta önde ✓ · sucuk yedeğine robot dokunmaz ✓',GRN),
      ('③ form: v4 ideal kama huni (dikdörtgen, 45° V, tam boy helezon = canlı taban, tarak, dik uçlar) + C (helezon, ağız iç uçta, huni yok) ✓ · dönen parça yok ✓',GRN),
      ('④ ölçü: v7 kurgusu — kaşar 14,6 kg ×4 · sucuk 10 ×2 · kav/kuş 3,5 ×4 ✓ · dikey 27+47+14+47+14+48 = 197 ✓ · derinlik 84 ✓ · 70 aynı ✓',GRN),
      ('⑤ HAT v45: TOPPING bloğu bu çizimle (çark katı yok, 2 boşluk, kat 47) · STORE v4 değişmez (kav/kuş 18 ≤ 29) · KONTROL ⑦: kol ≥ 20 kg (18 kg kaset)',BLU),
      ('⑥ AÇIK: ⑦ kobot sınıfı · kaşar V + helezon prototip · 2. tarak · klape/soğuk hacim · sucuk çubuk kaseti · tepsi 50 cm düzlemi erişimi',AMB)]
for i,(s,c) in enumerate(rows):
    tx(76,YK+46+i*27,s,7.4,'start','',c)
tx(W-40,H-12,'AUTOKITCH · arastirma/3_TOPPING/ist3_topping_detay_v16 · 4 Eyl 2026',7,'end','',GRY)
o.append('</svg>')
svg = chr(10).join(o)
xml.dom.minidom.parseString(svg.encode('utf-8'))
out = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\3_TOPPING\ist3_topping_detay_v16.svg"
io.open(out,'w',encoding='utf-8').write(svg)
print('yazildi + XML gecerli | kasar gross %.1f L, V %.1f, kullanilir %.1f L = %.1f kg | kk %.1f L = %.1f kg' % (gK,vK,uK,uK*0.41,uk,uk*0.55))
