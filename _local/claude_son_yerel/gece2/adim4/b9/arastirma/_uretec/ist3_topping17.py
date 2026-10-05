# -*- coding: utf-8 -*-
# TOPPING v17 — TEK BÜYÜK KASET (tam derinlik, L-oluk: besleme helezonu + dozaj helezonu, tek tahrik) · kaşar/sucuk haftalık, robot değiştirmez
# kav/kuş: küçük gövde, aynı helezon/dişli/dok (3 gün, STORE −18) — Seçenek A: donmuş dozaj → hepsi haftalık · DOK detayı · isimler
import io, math, xml.dom.minidom
W, H = 1460, 1200
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
def poly(pts,sw=1,c='#111',f='none',d=None):
    o.append('<polygon points="%s" fill="%s" stroke="%s" stroke-width="%s"%s/>' % (' '.join('%.1f,%.1f'%p for p in pts),f,c,sw,(' stroke-dasharray="%s"'%d) if d else ''))
def arr(x1,y1,x2,y2,c='#c0392b',w=1.2):
    ln(x1,y1,x2,y2,w,c); a=math.atan2(y2-y1,x2-x1)
    for s in (1,-1): ln(x2,y2,x2-6*math.cos(a-s*.42),y2-6*math.sin(a-s*.42),w,c)

GRN, RED, BLU, GRY, AMB, PUR = '#1d7a4f', '#c0392b', '#1a49b8', '#666', '#b7791f', '#6b4fa8'
FILL, MAT, SUC, LIGHT, ICE = '#f1efe8', '#e9dfa8', '#e8eef8', '#f7f6f2', '#e3f2fb'
K = 2.5
GAP, KAN, KLP = 4.0, 3.0, 3.0
LK, WB, HK = 27.0, 78.0, 44.0            # büyük kaset: L (x), W (y, tam derinlik), H
YF, YB = 62.0, 23.0                       # ön oluk (dozaj helezonu) y, arka bölge merkezi y
def hacim_buyuk():
    on = LK*38*HK/1000 - (19*19-12.25)*LK/1000
    arka = LK*40*HK/1000 - (13.5*13.5-12.25)*40/1000
    return on, arka, on+arka
vo,va,vt = hacim_buyuk()
Z = [('teknik',27,'#f3f3f3'),('KAT 1',47,'#fff'),('BOŞLUK 1',14,'#eef3ff'),('KAT 2',47,'#fff'),('BOŞLUK 2',14,'#eef3ff'),('ALT',48,'#f7f6f2')]
assert sum(z[1] for z in Z)==197
zt={}; acc=0
for ad,h,_ in Z: zt[ad]=acc; acc+=h
z1,zb1,z2,zb2,za = zt['KAT 1'],zt['BOŞLUK 1'],zt['KAT 2'],zt['BOŞLUK 2'],zt['ALT']

o.append('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">' % (W,H,W,H))
rc(0,0,W,H,0,0,'none',None,'#fff')
tx(30,42,'AUTOKITCH — İSTASYON 3 · TOPPING v17 (5 Eyl 2026) — TEK BÜYÜK KASET: tam derinlik, L-oluk (besleme + dozaj helezonu), tek tahrik · kaşar & sucuk HAFTALIK, robot değiştirmez · aynı mekanizma · 70 × 197 × 84',15,'start','bold')
tx(30,66,'Kemal: "arka arkaya iki kaşar yerine bir büyük kaşar, hepsi aynı parça" → EVET, mantıklı: kaset tam derinliği kaplar (27×78×44, 76 L, kaşar 31 kg), ön oluktaki dozaj helezonu + arka oluktaki besleme helezonu tek dişliden döner. Kav/kuş 3 günlük olduğu için küçük gövde kalır ama helezon, tarak, dişli, dok AYNI parça.',9.5,'start','','#444')
ln(30,78,W-30,78,.8,'#999')

# ================= ÖN KESİT (helezon eksenleri, kademeli) =================
X0,Y0 = 60,120
tx(X0+K*35,Y0-10,'ÖN KESİT A-A (dozaj helezonları) 1:4',9,'middle','bold')
rc(X0,Y0,K*70,K*197,2.2)
zz=0
for ad,h,col in Z:
    rc(X0,Y0+K*zz,K*70,K*h,.8,0,'#111',None,col); zz+=h
rc(X0+K*3,Y0+K*3,K*30,K*21,1,2,'#111',None,'#fff'); tx(X0+K*18,Y0+K*12,'SOĞUTMA',6.5,'middle','bold'); tx(X0+K*18,Y0+K*18,'1/12 HP · +3',5.6,'middle','')
rc(X0+K*37,Y0+K*3,K*30,K*21,1,2,'#111',None,'#fff'); tx(X0+K*52,Y0+K*10,'ELEKTRİK',6.5,'middle','bold'); tx(X0+K*52,Y0+K*15,'PLC · 24 V PSU',5,'middle',''); tx(X0+K*52,Y0+K*20,'5 sürücü',5,'middle','')
def kaset_on(x0, sgn, zfloor, L, Hh, ad, alt, tip='helezon', light=False, fill=MAT, tarak2=True):
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
            # konik dişli (besleme helezonuna) L/2'de
            ci(X(L/2),Zc(3.5),K*1.5,.8,'#555',None,'#eee')
        else:
            for k in range(6): rc(min(X(3+k*3.6),X(3+k*3.6+2.6)),Zc(Hh-2),K*2.6,K*(Hh-5),.7,1,'#555',None,'#f4ece6')
            rc(min(X(L-6),X(L-2)),Zc(4),K*4,K*3,1,1,RED,None,'#fdeeee'); tx(X(L-4),Zc(1),'bıçak',4.2,'middle','bold',RED)
        rc(min(X(L-3),X(L-1)),Zc(0),K*2,K*1.2,0,0,'none',None,'#fff'); ln(X(L-2),Zc(0),X(L-2),Zc(-5),1.6,GRN)
        ci(X(-0.5),Zc(3.5),K*1.8,.9,'#555',None,'#eee')
        rc(min(X(-GAP),X(-0.5)),Zc(7),K*(GAP-0.5),K*7,1,1,BLU,None,'#dfe7fb'); tx(X(-GAP/2-0.2),Zc(1.6),'M',4.4,'middle','bold',BLU)
    if ad: tx(X(L/2),Zc(Hh-9),ad,6,'middle','bold','#999' if light else '#111'); tx(X(L/2),Zc(Hh-14),alt,4.6,'middle','','#999' if light else '#333')
for zL,left,right in ((z1,('KAŞAR A','27×78×44 · 31 kg · hafta'),('SUCUK','27×78×27 · çubuk 10 kg')),(z2,('KAŞAR B','27×78×44 · 31 kg · hafta'),('KAVURMA','küçük 27×17×18 · 3 gün'))):
    zfloor=zL+45
    rc(X0,Y0+K*zfloor,K*70,K*2,1,0,'#111',None,'#bbb')
    for xx in (31,39): rc(X0+K*(xx-1.5),Y0+K*zfloor,K*3,K*2,0,0,'none',None,'#fff')
    kaset_on(GAP,+1,zfloor,LK,44,left[0],left[1])
    if right[0]=='SUCUK': kaset_on(70-GAP,-1,zfloor,LK,27,right[0],right[1],'cubuk')
    else: kaset_on(70-GAP,-1,zfloor,LK,18,right[0],right[1],'helezon',tarak2=False)
    rc(X0+K*1,Y0+K*(zL+0.5),K*68,K*46,.8,2,'#111','3,2')
tx(X0+K*70+6,Y0+K*(z1+8),'KAT 1 · 47: kaşar A | sucuk (ikisi tam derinlik)',6.5,'start','bold'); tx(X0+K*70+6,Y0+K*(z1+16),'ağızlar (31, 62) · (39, 62) · robot değiştirmez',5.6,'start','',GRN); tx(X0+K*70+6,Y0+K*(z1+23),'kaset çekmece gibi öne çekilir, eleman üstten doldurur',5.4,'start','',BLU)
tx(X0+K*70+6,Y0+K*(z2+8),'KAT 2 · 47: kaşar B | kavurma + kuşbaşı (küçük)',6.5,'start','bold'); tx(X0+K*70+6,Y0+K*(z2+16),'küçükler önde (y 52,5 / 71,5), çözülen yedekleri arkada',5.6,'start','',GRN); tx(X0+K*70+6,Y0+K*(z2+23),'Seçenek A: sağ yarı −18, donmuş dozaj → haftalık',5.4,'start','',AMB)
for zb,lab in ((zb1,'BOŞLUK 1 · düzlem 1 (sucuklu) · tepsi 111 cm'),(zb2,'BOŞLUK 2 · düzlem 2 (kav/kuş) · tepsi 50 cm')):
    el(X0+K*35,Y0+K*(zb+10.5),K*17,K*1.2,1.2,BLU,None,'#dfe7fb'); tx(X0+K*35,Y0+K*(zb+8),'tepsi Ø34 · spiral',5,'middle','',BLU)
    tx(X0+K*70+6,Y0+K*(zb+8),lab,6.3,'start','',BLU)
rc(X0+K*3,Y0+K*(za+4),K*30,K*40,1,2,'#111','4,3',LIGHT); tx(X0+K*18,Y0+K*(za+20),'boş küçük kaset',5.4,'middle','bold','#666'); tx(X0+K*18,Y0+K*(za+27),'+ park (2)',5,'middle','','#666')
rc(X0+K*37,Y0+K*(za+4),K*30,K*40,1,2,'#111',None,'#fff'); tx(X0+K*52,Y0+K*(za+18),'Seçenek A:',5.4,'middle','bold',AMB); tx(X0+K*52,Y0+K*(za+25),'−18 grubu 1/6 HP',5,'middle','',AMB); tx(X0+K*52,Y0+K*(za+32),'(B'+chr(39)+'de: eleman dolabı)',4.8,'middle','',GRY)
tx(X0+K*70+6,Y0+K*(za+14),'ALT · 48: raf artık gerekmiyor (robot kaşar taşımıyor)',6.3,'start','',GRY); tx(X0+K*70+6,Y0+K*(za+22),'küçük boş kasetler + park · A'+chr(39)+'da −18 kompresörü',5.4,'start','','#333')
ln(X0,Y0+K*197+16,X0+K*70,Y0+K*197+16,.8); tx(X0+K*35,Y0+K*197+28,'70',8,'middle','bold')
ln(X0-14,Y0,X0-14,Y0+K*197,.8); tx(X0-18,Y0+K*98,'197',8,'end','bold')
zz=0
for ad,h,_ in Z: tx(X0-18,Y0+K*(zz+h/2)+3,'%g'%h,5.2,'end','',GRY); zz+=h
tx(X0+K*35,Y0+K*197+42,'27+47+14+47+14+48 = 197 ✓',7,'middle','bold',GRN)

# ================= ÜST GÖRÜNÜŞ KAT 1 / KAT 2 =================
XU,YU = 320,120
KU=2.35
def L_kaset(X,Y,x0,sgn,f,lab,alt,tip='helezon'):
    xa=min(x0,x0+sgn*LK)
    rc(X+KU*xa,Y+KU*KAN,KU*LK,KU*WB,1.1,1,'#111',None,f)
    if tip=='helezon':
        # on oluk (dozaj helezonu, x yonunde, y 62) + arka oluk (besleme helezonu, y yonunde, x merkez)
        ln(X+KU*(xa+1),Y+KU*(YF-3.5),X+KU*(xa+LK-1),Y+KU*(YF-3.5),.6,AMB,'2,2'); ln(X+KU*(xa+1),Y+KU*(YF+3.5),X+KU*(xa+LK-1),Y+KU*(YF+3.5),.6,AMB,'2,2')
        ln(X+KU*(xa+1),Y+KU*YF,X+KU*(xa+LK-1),Y+KU*YF,1.2,BLU)
        xm=xa+LK/2
        ln(X+KU*(xm-3.5),Y+KU*(KAN+2),X+KU*(xm-3.5),Y+KU*(YF-3.5),.6,AMB,'2,2'); ln(X+KU*(xm+3.5),Y+KU*(KAN+2),X+KU*(xm+3.5),Y+KU*(YF-3.5),.6,AMB,'2,2')
        ln(X+KU*xm,Y+KU*(KAN+2),X+KU*xm,Y+KU*(YF-4),1.2,PUR); arr(X+KU*xm,Y+KU*(YF-14),X+KU*xm,Y+KU*(YF-6),PUR,1)
        ci(X+KU*xm,Y+KU*YF,2.4,1,'#555',None,'#eee')
        tx(X+KU*xm,Y+KU*30,'besleme',4.2,'middle','bold',PUR); tx(X+KU*xm,Y+KU*35,'helezonu',4.2,'middle','',PUR)
        tx(X+KU*xm,Y+KU*(YF+8),'dozaj helezonu',4.2,'middle','bold',BLU)
    else:
        for r in range(4):
            for k in range(5): ci(X+KU*(xa+4+k*4.6),Y+KU*(10+r*16),KU*1.8,.5,'#555',None,'#f4ece6')
        arr(X+KU*(xa+LK/2),Y+KU*40,X+KU*(xa+LK/2),Y+KU*52,AMB,1); tx(X+KU*(xa+LK/2),Y+KU*38,'eğim → öne',4,'middle','',AMB)
        rc(X+KU*(x0+sgn*(LK-8)) if sgn>0 else X+KU*(x0-LK), Y+KU*(YF-4), KU*8, KU*8, .9,1,RED,None,'#fdeeee')
    ax=x0+sgn*(LK-2); ci(X+KU*ax,Y+KU*YF,2.6,1.3,GRN,None,'#fff'); ci(X+KU*ax,Y+KU*YF,1,1,GRN,None,GRN)
    ci(X+KU*(x0-sgn*0.5),Y+KU*YF,2,1,'#555',None,'#eee')
    rc(X+KU*min(x0-sgn*GAP,x0-sgn*0.5),Y+KU*(YF-3.5),KU*(GAP-0.5),KU*7,1,1,BLU,None,'#dfe7fb')
    tx(X+KU*(xa+LK/2),Y+KU*14,lab,5.4,'middle','bold'); tx(X+KU*(xa+LK/2),Y+KU*20,alt,4.2,'middle','','#333')
def small(X,Y,x0,sgn,yc,light,lab,alt):
    xa=min(x0,x0+sgn*LK)
    rc(X+KU*xa,Y+KU*(yc-8.5),KU*LK,KU*17,1 if not light else .8,1,'#111' if not light else '#999','3,2' if light else None,SUC if not light else LIGHT)
    if not light:
        ln(X+KU*(xa+1),Y+KU*yc,X+KU*(xa+LK-1),Y+KU*yc,1.1,BLU)
        ax=x0+sgn*(LK-2); ci(X+KU*ax,Y+KU*yc,2.6,1.3,GRN,None,'#fff'); ci(X+KU*ax,Y+KU*yc,1,1,GRN,None,GRN)
        ci(X+KU*(x0-sgn*0.5),Y+KU*yc,2,1,'#555',None,'#eee')
        rc(X+KU*min(x0-sgn*GAP,x0-sgn*0.5),Y+KU*(yc-3.5),KU*(GAP-0.5),KU*7,1,1,BLU,None,'#dfe7fb')
    tx(X+KU*(xa+LK/2),Y+KU*(yc-1),lab,4.8,'middle','bold','#999' if light else '#111'); tx(X+KU*(xa+LK/2),Y+KU*(yc+5),alt,4,'middle','','#999' if light else '#333')
def plan(X,Y,baslik,kat):
    tx(X+KU*35,Y-8,baslik,8.5,'middle','bold')
    rc(X,Y,KU*70,KU*84,1.4)
    rc(X+KU*31,Y,KU*8,KU*84,0,0,'none',None,'#dff3e6')
    L_kaset(X,Y,GAP,+1,FILL,'KAŞAR A' if kat==1 else 'KAŞAR B','27×78×44 · L-oluk')
    if kat==1:
        L_kaset(X,Y,70-GAP,-1,SUC,'SUCUK','çubuk + bıçak · tam derinlik','cubuk')
        outs=((31,YF),(39,YF))
    else:
        small(X,Y,70-GAP,-1,52.5,False,'KAVURMA','27×17×18')
        small(X,Y,70-GAP,-1,71.5,False,'KUŞBAŞI','27×17×18')
        small(X,Y,70-GAP,-1,12.5,True,'kav. yedek','çözülüyor')
        small(X,Y,70-GAP,-1,31.5,True,'kuş. yedek','çözülüyor')
        outs=((31,YF),(39,52.5),(39,71.5))
    for (ox,oy) in outs: ci(X+KU*ox,Y+KU*oy,KU*31,.8,GRN,'5,3')
    rc(X,Y+KU*81,KU*70,KU*3,1,0,BLU,None,'#dfe7fb'); tx(X+KU*35,Y+KU*83.2,'klape',4.2,'middle','',BLU)
    rc(X,Y,KU*70,KU*3,0,0,'none',None,'#e5e5e5')
    tx(X+KU*35,Y+KU*84+11,'süpürme R31: sol x 0-62 · sağ x 8-70 · y 31-93 ✓',4.8,'middle','bold',GRN)
plan(XU,YU,'ÜST — KAT 1 (sucuklu düzlem)',1)
plan(XU,YU+KU*84+36,'ÜST — KAT 2 (kavurma / kuşbaşı düzlemi)',2)
tx(XU+KU*35,YU+2*KU*84+54,'büyük kaset tam derinlik: arka bölge malzemesini besleme helezonu (mor) öne taşır, dozaj helezonu (mavi) ağza götürür',4.6,'middle','','#333')
tx(XU+KU*35,YU+2*KU*84+65,'Seçenek A: kat 2 sağ yarı −18 hücre, kav/kuş büyük gövdede donmuş, yedek yok, robot hiç kaset taşımaz',4.6,'middle','',AMB)

# ================= BÜYÜK KASET DETAYI =================
XD,YD = 520,120
rc(XD,YD,330,470,1.2,3,'#999',None,'#fcfdff')
tx(XD+165,YD+16,'BÜYÜK KASET 27×78×44 — L-oluk, tek tahrik',7.5,'middle','bold')
KD=1.75
# plan
px_,py_ = XD+16, YD+30
rc(px_,py_,KD*LK,KD*WB,1.1,0,'#111',None,FILL)
ln(px_+KD*1,py_+KD*(59-3.5),px_+KD*(LK-1),py_+KD*(59-3.5),.6,AMB,'2,2'); ln(px_+KD*1,py_+KD*(59+3.5),px_+KD*(LK-1),py_+KD*(59+3.5),.6,AMB,'2,2')
ln(px_+KD*1,py_+KD*59,px_+KD*(LK-1),py_+KD*59,1.2,BLU)
ln(px_+KD*(LK/2-3.5),py_+KD*2,px_+KD*(LK/2-3.5),py_+KD*(59-3.5),.6,AMB,'2,2'); ln(px_+KD*(LK/2+3.5),py_+KD*2,px_+KD*(LK/2+3.5),py_+KD*(59-3.5),.6,AMB,'2,2')
ln(px_+KD*LK/2,py_+KD*2,px_+KD*LK/2,py_+KD*(59-4),1.2,PUR); ci(px_+KD*LK/2,py_+KD*59,2.4,1,'#555',None,'#eee')
ci(px_+KD*(LK-2),py_+KD*59,2.4,1.2,GRN,None,'#fff'); ci(px_-1,py_+KD*59,2,1,'#555',None,'#eee')
tx(px_+KD*LK/2,py_+KD*WB+9,'27',5,'middle','bold'); tx(px_-4,py_+KD*WB/2+3,'78',5,'end','bold'); tx(px_+KD*LK/2,py_-4,'ÜST',5,'middle','',GRY)
tx(px_+KD*LK+4,py_+KD*20,'A',6,'start','bold',RED); tx(px_+KD*LK+4,py_+KD*59+3,'B',6,'start','bold',RED)
ln(px_-6,py_+KD*59,px_+KD*LK+2,py_+KD*59,.6,RED,'4,2'); ln(px_+KD*LK/2,py_-6,px_+KD*LK/2,py_+KD*WB+2,.6,RED,'4,2')
tx(px_+KD*LK/2,py_+KD*WB+18,'B: dozaj oluğu (y 59) · A: besleme oluğu (x orta)',4.4,'middle','',GRY)
# kesit B (x boyunca, dozaj helezonu) — sağda üstte
bx,by = XD+90, YD+30
Xb=lambda c: bx+KD*c; Zb=lambda c: by+KD*(44-c)
rc(Xb(0),Zb(44),KD*LK,KD*44,1.1,0,'#111',None,FILL)
rc(Xb(1),Zb(7),KD*(LK-2),KD*7,.9,1,'#111',None,'#fff'); ln(Xb(1),Zb(13),Xb(LK-1),Zb(13),1,BLU); ln(Xb(1),Zb(30),Xb(LK-1),Zb(30),1,BLU)
ci(Xb(LK/2),Zb(3.5),KD*1.6,.8,'#555',None,'#eee'); ln(Xb(LK-2),Zb(0),Xb(LK-2),Zb(-5),1.4,GRN); ci(Xb(-0.5),Zb(3.5),2,1,'#555',None,'#eee')
tx(Xb(LK/2),by-4,'KESİT B — dozaj helezonu (x)',5,'middle','',GRY); tx(Xb(LK/2),Zb(22),'depo',4.4,'middle','','#333'); tx(Xb(LK/2),Zb(9.5),'konik → besleme',3.8,'middle','',PUR)
tx(Xb(LK)+3,Zb(3),'ağız',4.2,'start','bold',GRN); tx(Xb(-3),Zb(9),'dişli',4,'end','','#555')
# kesit A (y boyunca, besleme helezonu) — sağda altta
ax_,ay_ = XD+150, YD+30
Xa=lambda c: ax_+KD*c; Za=lambda c: ay_+KD*(44-c)
rc(Xa(0),Za(44),KD*WB,KD*44,1.1,0,'#111',None,FILL)
# arka oluk taban: y 2-55 helezon; on oluk V duvarı y 55-59 (45°): sadece taban cizgileri
rc(Xa(2),Za(7),KD*53,KD*7,.9,1,'#111',None,'#fff'); ln(Xa(2),Za(3.5),Xa(56),Za(3.5),.8,PUR); arr(Xa(30),Za(3.5),Xa(50),Za(3.5),PUR,1)
ln(Xa(2),Za(13),Xa(55),Za(13),1,BLU)
ci(Xa(59),Za(3.5),KD*3.5,.9,'#111',None,'#fff'); tx(Xa(59),Za(-2),'dozaj hlz.',3.8,'middle','',BLU)
ln(Xa(59),Za(13),Xa(59),Za(13),1,BLU); ci(Xa(59),Za(13),KD*5.5,.6,BLU,'2,2'); ci(Xa(59),Za(30),KD*5.5,.6,BLU,'2,2')
ln(Xa(55),Za(7),Xa(59)-KD*3.5,Za(7),1,'#111'); tx(Xa(78)+3,Za(22),'44',5,'start','bold'); tx(Xa(39),ay_-4,'KESİT A — besleme helezonu (y), arka → ön',5,'middle','',GRY)
tx(Xa(28),Za(24),'arka depo (y 3-55)',4.4,'middle','','#333'); tx(Xa(28),Za(9.5),'besleme helezonu → öne iter',3.8,'middle','',PUR); tx(Xa(66),Za(24),'ön depo',4.4,'middle','','#333')
tx(Xa(39),Za(44)+KD*44+9,'78 (arka ← y → ön)',5,'middle','bold')
# metin
ny=YD+250
lines=[('Hacim: ön bölge %.1f L + arka bölge %.1f L = %.1f L → kaşar %.0f kg (0,41 kg/L)' % (vo,va,vt,vt*0.41),'#333'),
       ('Haftalık kaşar 45,5 kg → A + B = 62 kg ≥ hafta ✓ · robot HİÇ değiştirmez, eleman haftada 1 doldurur','#1d7a4f'),
       ('Gövde: PE-HD 8 mm (gıda, −18/+3, yıkanır) ~7 kg · helezon + tarak + dişli paslanmaz ~4 kg → boş 11 kg, dolu 42 kg','#333'),
       ('Doldurma: kaset teleskopik rayda 60 cm öne çekilir (60 kg ray), üst kapak açılır, 3 × 10 kg torba dökülür, geri itilir → dişli meshler','#333'),
       ('Temizlik: haftalık, boşken çıkarılır (11 kg, iki el) · içi tek parça: iki helezon + iki tarak sökülmeden yıkanır','#333'),
       ('Tahrik: duvardaki motor → dış uç dişlisi → dozaj helezonu → ortadaki konik dişli → besleme helezonu; taraklar 1:20 aynı milden','#1a49b8'),
       ('Besleme helezonu ön oluğun DİBİNE iter (T kavşağı); ön oluk dolu kalır, dozaj helezonu hep aynı yükle çalışır → doz sabit','#333'),
       ('Sucuk aynı gövde: içi çubuk kanalı + eğimli taban (8°) + bıçak; besleme helezonu yok, çubuklar kendi kayar','#b7791f'),
       ('Küçük kaset 27×17×18 (kav/kuş): SADECE dozaj helezonu — aynı helezon, tarak, dişli, dok; farklı olan yalnız gövde kabuğu','#1d7a4f')]
for i,(s,c) in enumerate(lines): tx(XD+12,ny+i*13.5,s,5.6,'start','bold' if i in (1,8) else '',c)
tx(XD+12,ny+130,'V-oluk (kama huni): ön yarı genişlik 19 → derinlik 15,5 · arka yarı genişlik 13,5 → derinlik 10 · üstte dik depo',5.4,'start','',GRY)
tx(XD+12,ny+143,'"5 g" dozaj: ray altı yük hücresi kaset ağırlığını okur (kayıp-ağırlık ilkesi), helezon turu kesilir ±3 g',5.4,'start','',GRY)
tx(XD+12,ny+160,'Neden 2 helezon: tek helezonla 78 cm'+chr(39)+'lik hazneyi boşaltmak için V 35 cm derin olurdu (hacim yarıya iner) →',5.4,'start','',AMB)
tx(XD+12,ny+173,'arka oluk kendi helezonuyla öne besler. Endüstride adı: çapraz besleyicili (cross-feed) hazne.',5.4,'start','',AMB)
tx(XD+12,ny+190,'Kemal'+chr(39)+'in "hepsi aynı kilo" fikri: kaşar/sucuk ✓ (haftalık, büyük). Kav/kuş 3,5 günlük olduğu için büyük gövde',5.4,'start','bold','#333')
tx(XD+12,ny+203,'doldurulamaz (taze); ya küçük gövde (B) ya da donmuş dozaj + −18 hücre (A) → o zaman hepsi büyük ve haftalık.',5.4,'start','bold','#333')

# ================= DOK DETAYI + ELEKTRİK KARŞILAŞTIRMA =================
XE,YE = 870,120
rc(XE,YE,560,470,1.4,4,'#111',None,'#fcfdff')
tx(XE+14,YE+22,'DOK — kaset nereye, nasıl oturur? Elektrik nasıl gelir?',10,'start','bold')
# dok cizimi: on gorunus (x-z) kaset rayda, motor duvarda
dx,dy = XE+16,YE+34
rc(dx,dy,300,210,1,3,'#999',None,'#fff'); tx(dx+150,dy+14,'DOK KESİTİ (kaset ucu, duvar tarafı)',7,'middle','bold')
KDk=3.2
Xd=lambda c: dx+40+KDk*c; Zd=lambda c: dy+150-KDk*c
rc(Xd(0),Zd(44),KDk*20,KDk*44,1.1,0,'#111',None,FILL); tx(Xd(10),Zd(30),'KASET',6,'middle','bold'); tx(Xd(10),Zd(24),'(pasif)',4.8,'middle','',GRY)
rc(Xd(1),Zd(7),KDk*18,KDk*7,.9,1,'#111',None,'#fff'); ln(Xd(1),Zd(3.5),Xd(19),Zd(3.5),.8,'#555','3,2'); tx(Xd(10),Zd(2),'helezon',4.4,'middle','')
ci(Xd(-0.7),Zd(3.5),KDk*2,1.1,'#111',None,'#eee'); ci(Xd(-4.9),Zd(3.5),KDk*2.2,1.1,BLU,None,'#dfe7fb')
rc(Xd(-9),Zd(0),KDk*3.6,KDk*7,1,1,BLU,None,'#dfe7fb'); tx(Xd(-7.2),Zd(-3),'M',5,'middle','bold',BLU)
rc(Xd(-10),Zd(46),KDk*1,KDk*48,1,0,'#111',None,'#ccc'); tx(Xd(-11.5),Zd(22),'yan duvar',4.6,'end','',GRY)
# raylar (kaset yan yuzunde, y yonunde) — kesitte iki kare
for zc in (6,38):
    rc(Xd(20),Zd(zc+2),KDk*1.6,KDk*3,1,0,'#555',None,'#ddd'); rc(Xd(-1.6),Zd(zc+2),KDk*1.6,KDk*3,1,0,'#555',None,'#ddd')
tx(Xd(22.5),Zd(38),'ray ×2 (yan)',4.4,'start','','#555'); tx(Xd(22.5),Zd(6),'teleskopik 60 kg',4.4,'start','','#555')
# yuk hucresi ray altinda
rc(Xd(20.6),Zd(-3),KDk*2.6,KDk*2.2,1,1,AMB,None,'#fdf3dd'); rc(Xd(-3.4),Zd(-3),KDk*2.6,KDk*2.2,1,1,AMB,None,'#fdf3dd')
tx(Xd(24),Zd(-2.2),'yük hücresi ×2 (ray taşıyıcısı altında)',4.4,'start','bold',AMB)
rc(Xd(20),Zd(0),KDk*3,KDk*1.2,.8,0,'#111',None,'#bbb'); tx(Xd(24),Zd(1.6),'kat tabanı',4.2,'start','',GRY)
arr(Xd(10),Zd(52),Xd(10),Zd(47),AMB,1); tx(Xd(10),Zd(55),'kaset öne-arkaya kayar (y)',4.4,'middle','',AMB)
tx(dx+150,dy+178,'dişli YANDAN meshler: kaset son 2 cm'+chr(39)+'de pahlı dişler birbirine oturur',4.8,'middle','bold',BLU)
tx(dx+150,dy+190,'kasette kablo, motor, sensör YOK · elektrik yalnız duvarda',4.8,'middle','bold',GRN)
tx(dx+150,dy+202,'kaset = hazne + 2 helezon + 2 tarak + dişliler; bulaşık makinesine girer',4.6,'middle','','#333')
# karsilastirma
cx_,cy_ = XE+326,YE+34
rc(cx_,cy_,220,210,1,3,'#999',None,'#fff'); tx(cx_+110,cy_+14,'MOTOR NEREDE? (senin sorun)',7,'middle','bold')
tx(cx_+8,cy_+32,'① motor KASETTE + kontak pimleri',6,'start','bold',RED)
for i,s in enumerate(['takınca temas eder, "elektriği alır" — olur',
                      '− 5 motor + sürücü + IP69K conta ×5 (maliyet ×5)',
                      '− kontaklar +3 °C nemde oksitlenir, kırıntı girer',
                      '− kaset ağırlaşır (motor 1 kg), yıkanamaz (elektronik)',
                      '− her kaset "makine" olur: arıza ×5, yedek ×5']):
    tx(cx_+8,cy_+44+i*11,s,5,'start','',RED if s.startswith('−') else '#333')
tx(cx_+8,cy_+108,'② motor DUVARDA + yandan dişli (seçilen)',6,'start','bold',GRN)
for i,s in enumerate(['+ kaset pasif, ucuz, hafif, komple yıkanır',
                      '+ elektrik hep kuru tarafta, kontak yok',
                      '+ endüstri standardı: Picnic, Grote, kahve dozerleri',
                      '− dişli hizası: pahlı diş + 1 mm ray toleransı yeter',
                      '+ arıza: motor duvarda 4 vidayla değişir']):
    tx(cx_+8,cy_+120+i*11,s,5,'start','',GRN if s.startswith('+') else AMB)
tx(cx_+110,cy_+190,'KARAR: ② — kaset "kap"tır, motor "makine"dir',5.2,'middle','bold',GRN)
tx(cx_+110,cy_+202,'"haznenin üstüne oturmaz": kaset kendisi haznedir',5,'middle','','#333')
# isimler
iy=YE+256
tx(XE+14,iy,'PROFESYONEL İSİMLER (TR / EN)',8,'start','bold')
names=[('kaset','dozaj haznesi — hopper / feed hopper'),
       ('bütün ünite','kayıp-ağırlık esaslı vidalı besleyici — loss-in-weight (LIW) screw feeder'),
       ('helezon (rotor)','dozaj helezonu / vidalı besleyici — metering screw / auger'),
       ('arka helezon','besleme helezonu / çapraz besleyici — feed screw / cross-feeder'),
       ('tarak','köprü kırıcı karıştırıcı — bridge breaker / agitator (pimleri: agitator pins)'),
       ('V-oluk taban','kama huni, canlı taban — wedge hopper, live bottom'),
       ('ağız','boşaltma ağzı — discharge outlet / spout'),
       ('uç dişlisi','dişli kaplin / tahrik kavraması — gear coupling / drive engagement'),
       ('yük hücresi','yük hücresi, gravimetrik kontrol — load cell, gravimetric dosing'),
       ('ray + klape','teleskopik kızak, izole kapak — telescopic slide, insulated hatch')]
for i,(a,b) in enumerate(names):
    yy=iy+16+i*13.5; tx(XE+14,yy,a,5.8,'start','bold'); tx(XE+110,yy,b,5.6,'start','','#333')
tx(XE+14,iy+158,'Picnic'+chr(39)+'teki tel = "wire agitator / bridge breaker"; altındaki = "auger feeder"; altta dönen pide = "rotary platen"',5.4,'start','',GRY)
tx(XE+14,iy+172,'Bizim dozaj yöntemi: hacimsel helezon (tur sayısı) + gravimetrik düzeltme (yük hücresi) = hibrit; sanayide "LIW feeder"',5.4,'start','',GRY)
tx(XE+14,iy+190,'Kavurma/kuşbaşı için endüstri: "IQF" (tek tek şoklanmış) donmuş ürün — Seçenek A bunu ister',5.4,'start','bold',AMB)

# ================= STOK · SEÇENEK A/B · KONTROL =================
XT,YT = 60,620
rc(XT,YT,1370,330,1.4,4)
tx(XT+16,YT+24,'STOK · İKİ SEÇENEK · ROBOT · KONTROL',11,'start','bold')
col1=XT+16; col2=XT+470; col3=XT+930
tx(col1,YT+48,'KAŞAR & SUCUK (kesin)',8,'start','bold',GRN)
for i,s in enumerate(['kaşar A + B: 2 × 31 kg = 62 kg ≥ 45,5 kg/hafta ✓ — kaşar 14 gün dayanır, +3 °C',
                      'sucuk: 1 büyük gövde, 10 kg çubuk = hafta ✓ (7 gün raf ömrü)',
                      'robot bu üçüne HİÇ dokunmaz → kol yükü sorunu (18 kg) KAPANDI',
                      'eleman haftada 1: 3 kaseti öne çeker, doldurur (kaşar 3 torba), boşsa yıkar',
                      'yedek kaset yok, raf yok, park yok, FIFO yok — ALT 48 cm boşa çıktı',
                      'saat kuralı: kaşar 14 g ✓, sucuk 7 g ✓ (haftalık dolumla uyumlu)']):
    tx(col1,YT+64+i*13,s,6.2,'start','','#333')
tx(col1,YT+150,'v16 → v17: kaşar kaseti 4 → 2 · robot değişimi 3/hafta → 0 · kaset boyu 27×38 → 27×78',6.2,'start','bold',GRY)
tx(col1,YT+163,'aynı parçalar: helezon Ø7×25 ×1 tip · tarak ×1 tip · uç dişlisi ×1 · motor ×1 tip · ray ×1 tip',6.2,'start','bold',GRN)
tx(col1,YT+176,'gövde kabuğu: büyük (kaşar ×2, sucuk ×1) + küçük (kav/kuş) — B'+chr(39)+'de 2 kabuk, A'+chr(39)+'da 1 kabuk',6.2,'start','','#333')
tx(col2,YT+48,'KAV / KUŞ — B: TAZE, KÜÇÜK GÖVDE (kanıtlı)',8,'start','bold',BLU)
for i,s in enumerate(['27×17×18, 3,5 kg = 3 gün · ×4: çalışan + arkada çözülen + 2 STORE −18 + 1 boş',
                      'robot 3 günde 1 değiştirir (2 hamle) · STORE −18 çekmecesi 29 ≥ 18 ✓ değişmez',
                      'kol yükü ≤ 6 kg · ALT 48: boş küçük kasetler + park (2+2)',
                      'bedel: 2 gövde tipi, 3 günlük değişim rutini, STORE bağımlılığı',
                      '']):
    tx(col2,YT+64+i*13,s,6.2,'start','','#333')
tx(col2,YT+124,'KAV / KUŞ — A: DONMUŞ DOZAJ, BÜYÜK GÖVDE (test ister)',8,'start','bold',AMB)
for i,s in enumerate(['kat 2 sağ yarı −18 hücre (ayrı yalıtım, ALT'+chr(39)+'ta 1/6 HP grup), 2 büyük gövde: kav 8 kg + kuş 8 kg = hafta',
                      'IQF kuşbaşı küp serbest akar ✓ · IQF kavurma kırıntı: tedarikçi teyidi (blok kavurma OLMAZ)',
                      'fırın: donmuş üst malzeme → 350 °C'+chr(39)+'de +1-2 dk, kuşbaşı 2 cm küp pişme testi ŞART',
                      'kazanç: 1 gövde tipi, robot hiç kaset taşımaz, STORE −18 kaset çekmecesi boşa çıkar, çözülme yok',
                      'risk: helezon −18'+chr(39)+'de (kuru buz sürtünmesi OK, yağ donması yok) · ağızda buzlanma → ısıtıcı şerit 5 W']):
    tx(col2,YT+140+i*13,s,6.2,'start','','#333')
tx(col3,YT+48,'KARAR (Kemal sordu: mantıklı mı?)',8,'start','bold')
for i,(s,c) in enumerate([('EVET. Büyük kaset + iki helezon, arka arkaya iki kasetten',GRN),
                          ('daha basit: bir parça, bir dolum, sıfır robot hamlesi.',GRN),
                          ('Kaşar ve sucuk için hemen: v17 tabanı budur.',GRN),
                          ('Kav/kuş için varsayılan B (taze), hedef A (donmuş):',BLU),
                          ('A pişme + tedarik testinden geçerse tek gövde, tek rutin.',BLU),
                          ('Motor duvarda, kaset pasif — kontak pimi yok.',GRN),
                          ('',GRY),
                          ('KONTROL: bant ✓ (31/39) · erişim ✓ (yedek yok)',GRN),
                          ('· dikey 197 ✓ · derinlik 3+78+3 = 84 ✓',GRN),
                          ('· kol yükü ≤ 6 kg ✓ (⑦ kapandı, 12 kg kobot yeter)',GRN),
                          ('· AÇIK: helezon+kaşar prototip · A testleri · klape',AMB),
                          ('· HAT v45: TOPPING v17 bloğu, ALT 48 kullanımı',BLU)]):
    tx(col3,YT+64+i*14,s,6.4,'start','bold' if i<3 else '',c)
tx(XT+16,YT+300,'Bu resim: v16'+chr(39)+'nın üstüne "tek büyük kaset" kararı. Dilim/sektör/revolver yok. Tepsi düzlemleri 111 / 50 cm aynı. Sıradaki: A/B kararı → HAT v45.',6.4,'start','bold','#333')
tx(W-40,H-12,'AUTOKITCH · arastirma/3_TOPPING/ist3_topping_detay_v17 · 5 Eyl 2026',7,'end','',GRY)
o.append('</svg>')
svg = chr(10).join(o)
xml.dom.minidom.parseString(svg.encode('utf-8'))
out = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\3_TOPPING\ist3_topping_detay_v17.svg"
io.open(out,'w',encoding='utf-8').write(svg)
print('yazildi + XML gecerli | buyuk kaset on %.1f + arka %.1f = %.1f L → kasar %.0f kg' % (vo,va,vt,vt*0.41))
