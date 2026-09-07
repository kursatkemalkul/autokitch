# -*- coding: utf-8 -*-
"""HAT v48 (v47 + OVEN v3: kolon 70, hat 420, kartus, nis alti bos, plenum/fan/filtre, yan yalitim; TOPPING v27 sayilari, kizak ±5; ② ⑩ kapandi) — v47 (v46 + TOPPING kap simgesi v26 Picnic tipi, ⑦ 15,4, ⑧ v26, robot ≈ 12 kap/hafta) — v46: TUM ISTASYONLAR SON VERSIYON (5 Eyl 2026): STORE v4 (+ v5 oneri: −18 kaset kati ustte, klapeli, 4 kap sol modul) ·
PRESS v8 (tepsi O32, catal yuvasi) · TOPPING v25 (kap 14x68x24, L raf, catal, kap arkaya dayali, ALT: sogutma dipte + 2 sira raf,
evaporator sol yan kanal) · OVEN tank+pompa (② 32+12 = 44) · PACK 116 · SERVICE. Ust gorunum + KONTROL (genis kutu, sarilmis satirlar).
Tum notlar kendi kolonuna sarilir (notew) — tasan/ust uste binen yazi yok."""
import io, math, xml.dom.minidom

S=0.3
X0,Y0=90,150
HG,HA=1850,120
M=[("1 · STORE — soğuk depo (hamur + içecek + tatlı + donmuş kap ×4)",1400),("2 · PRESS",700),("3 · TOPPING",700),("4 · OVEN",700),("5 · PACK",700)]
T=sum(w for _,w in M)
def px(mm): return mm*S
YT=Y0+px(HG); YZ=YT+px(HA)
E=[]
def esc(s): return str(s).replace('&','&amp;').replace('<','&lt;')
def ln(x1,y1,x2,y2,w=1.4,c="#111",dash=None):
    d=f' stroke-dasharray="{dash}"' if dash else ""
    E.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}"{d}/>')
def rc(x,y,w,h,sw=1.4,rx=0,c="#111",dash=None,fill="none"):
    d=f' stroke-dasharray="{dash}"' if dash else ""
    E.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}" stroke="{c}" stroke-width="{sw}"{d}/>')
def ci(cx,cy,r,sw=1.4,c="#111",dash=None,fill="none"):
    d=f' stroke-dasharray="{dash}"' if dash else ""
    E.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{fill}" stroke="{c}" stroke-width="{sw}"{d}/>')
def el(cx,cy,rx,ry,sw=1.4,c="#111",dash=None):
    d=f' stroke-dasharray="{dash}"' if dash else ""
    E.append(f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" fill="none" stroke="{c}" stroke-width="{sw}"{d}/>')
def tx(x,y,s,fs=11,a="middle",w="",col="#111"):
    fw=f' font-weight="{w}"' if w else ""
    E.append(f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{a}" font-size="{fs}" fill="{col}" font-family="Arial"{fw}>{esc(s)}</text>')
def wrap(s,maxc):
    out=[]; cur=''
    for wd in str(s).split(' '):
        if cur and len(cur)+1+len(wd)>maxc: out.append(cur); cur=wd
        else: cur=(cur+' '+wd) if cur else wd
    if cur: out.append(cur)
    return out
def notew(x,y,s,wpx,fs=6.5,c="#555",a="middle",w="",lh=None):
    """kolon genisligine (wpx) sarilmis not; ilk satir y'de, sonrakiler lh asagida; son y'yi dondurur"""
    lh=lh or fs*1.25; maxc=max(12,int(wpx/(fs*0.56)))
    for i,l in enumerate(wrap(s,maxc)): tx(x,y+i*lh,l,fs,a,w,c)
    return y+len(wrap(s,maxc))*lh
def oy(x1,x2,y,cm,fs=11):
    ln(x1,y,x2,y,1); ln(x1,y-5,x1,y+5,1); ln(x2,y-5,x2,y+5,1)
    E.append(f'<path d="M {x1:.1f} {y:.1f} l 8 -3 v 6 z" fill="#111"/><path d="M {x2:.1f} {y:.1f} l -8 -3 v 6 z" fill="#111"/>')
    tx((x1+x2)/2,y-6,cm,fs)
def ox(x,y1,y2,cm,fs=11):
    ln(x,y1,x,y2,1); ln(x-5,y1,x+5,y1,1); ln(x-5,y2,x+5,y2,1)
    E.append(f'<path d="M {x:.1f} {y1:.1f} l -3 8 h 6 z" fill="#111"/><path d="M {x:.1f} {y2:.1f} l -3 -8 h 6 z" fill="#111"/>')
    E.append(f'<text x="{x-9:.1f}" y="{(y1+y2)/2:.1f}" text-anchor="middle" font-size="{fs}" fill="#111" font-family="Arial" transform="rotate(-90 {x-9:.1f} {(y1+y2)/2:.1f})">{esc(cm)}</text>')
def txr(x,y,s,fs=6,c='#555',w=''):
    fw=f' font-weight="{w}"' if w else ""
    E.append(f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="middle" font-size="{fs}" fill="{c}" font-family="Arial"{fw} transform="rotate(-90 {x:.1f} {y:.1f})">{esc(s)}</text>')
def not_(x,y,s,c="#555",fs=9.5): tx(x,y,s,fs,"middle","",c)
def rd(x,y,w,h,sw=1.2,c="#111"):
    E.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="none" stroke="{c}" stroke-width="{sw}" stroke-dasharray="5 4"/>')
def nk(x,y,s,fs=9): tx(x,y,s,fs,"middle","bold","#b3452b")   # KONTROL bulgusu (kirmizi)
def tray(cx,cy,r=160,kulp=False,c='#1a49b8'):
    el(cx,cy,px(r),px(18),1.8,c); el(cx,cy-px(6),px(r-20),px(9),1,'#8a6a3a')
    if kulp: ln(cx+px(r),cy-px(4),cx+px(r+120),cy-px(4),2,c); ln(cx+px(r),cy+px(6),cx+px(r+120),cy+px(6),2,c)
# TOPPING v26 kabi (on gorunus, Picnic tipi): dis 14x24 + altta 2 kizak 3x2 + L raf; ic: daire duvar R 6,5 (gobek z 14) + bogaz 7,6 + yalak R 3,8, helezon O7, gobek + 4 cubuk tarak
def _prof26():
    RW,ZH,RT,Hi=6.5,14.0,3.8,23.5; ZC=ZH-math.sqrt(RW**2-RT**2); n=10
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
PROF26=_prof26()
def kap25(x,y,nm,alt='',bos=False,c='#111',fill='#f3efe4',fs=6.2,rail=True):
    col='#999' if bos else c; dsh='4,3' if bos else None
    rc(x,y,px(140),px(240),1.2 if bos else 1.3,2,col,dsh,'#f7f6f2' if bos else '#dbeeff')   # şeffaf PC gövde
    X_=lambda cx: x+px(70+cx*10); Y_=lambda cz: y+px(5+(23.5-cz)*10)
    if not bos:
        E.append('<polygon points="%s" fill="#fff" stroke="%s" stroke-width="0.8"/>' % (' '.join('%.1f,%.1f'%(X_(a),Y_(b)) for a,b in PROF26),col))
        E.append('<polygon points="%s" fill="#e9dfa8" stroke="none"/>' % ' '.join('%.1f,%.1f'%(X_(a),Y_(min(b,21.0))) for a,b in PROF26))   # malzeme (2 cm hava)
        ci(X_(0),Y_(3.8),px(35),1,'#1d7a4f',None,'#f4f4f4'); ci(X_(0),Y_(3.8),px(10),.6,'#1d7a4f',None,'#ddd')   # POM helezon Ø7
        ci(X_(0),Y_(14.0),px(57),.6,'#6b4fa8','3,2','none')                                                       # tarak süpürmesi R 5,7
        ci(X_(0),Y_(14.0),px(12),.8,'#333',None,'#e8e8e8')                                                        # göbek
        th=math.radians(38)
        ln(X_(0),Y_(14.0),X_(5.7*math.sin(th)),Y_(14.0-5.7*math.cos(th)),1.4,'#333')                              # omurga
        for r in (5.7,4.3,2.9,1.4): ci(X_(r*math.sin(th)),Y_(14.0-r*math.cos(th)),px(4),.7,'#111',None,'#fff')   # çubuklar
    else:
        E.append('<polygon points="%s" fill="none" stroke="#bbb" stroke-width="0.6" stroke-dasharray="3,2"/>' % ' '.join('%.1f,%.1f'%(X_(a),Y_(b)) for a,b in PROF26))
    for dx_ in (20,120): rc(x+px(dx_-15),y+px(240),px(30),px(20),.7,0,col,dsh,'#d0d7de' if not bos else '#f7f6f2')   # kızaklar ±5 (v27)
    if rail: ln(x-px(6),y+px(262),x+px(146),y+px(262),1.3,'#555')                                # L raf
    tx(x+px(70),y+px(26),nm,fs,'middle','bold',col)
    if alt: tx(x+px(70),y+px(36),alt,4.4,'middle','','#333')

xs=[X0+px(sum(w for _,w in M[:i])) for i in range(6)]
for i,(_ad,_w) in enumerate(M):
    _x=xs[i]
    rc(_x+2,Y0,px(_w)-4,px(HG),2.2,5)
    if i not in (2,3): rc(_x+14,YT,12,px(HA),1.4); rc(_x+px(_w)-26,YT,12,px(HA),1.4)   # TOPPING + OVEN: ayak yerine plint
ln(X0-46,YZ,X0+px(T)+70,YZ,2)

# ================= 1 STORE v4 (+ v5 oneri: −18 kaset kati ustte, klapeli, 4 kap sol modul) =================
a0,a1=xs[0],xs[1]; am=a0+px(700)
PU='#e9e4d6'
rc(a0+6,Y0+px(20),a1-a0-12,px(280),1.2,2)
for gx,lab in ((350,'−18 grubu 1/3 HP'),(1050,'+3 grubu 1/4 HP')):
    ci(a0+px(gx-60),Y0+px(160),px(55),1.1); rc(a0+px(gx+20),Y0+px(90),px(120),px(150),.9,2); tx(a0+px(gx),Y0+px(278),lab,7,'middle','bold')
not_((a0+a1)/2,Y0+px(58),'SOĞUTMA ×2 — bölme 28, üstten servis',fs=8)
rc(a0+6,Y0+px(300),a1-a0-12,px(60),1,0,'#111',None,PU)
rc(a0+6,Y0+px(300),px(60),px(900),1,0,'#111',None,PU); rc(a1-6-px(60),Y0+px(300),px(60),px(900),1,0,'#111',None,PU)
rc(a0+px(690),Y0+px(360),px(20),px(840),1,0,'#111',None,'#ccc')
rc(a0+6,Y0+px(1200),a1-a0-12,px(80),1,0,'#111',None,PU)
rc(a0+6,Y0+px(1280),px(80),px(570),1,0,'#111',None,PU); rc(a1-6-px(80),Y0+px(1280),px(80),px(570),1,0,'#111',None,PU)
rc(a0+6,Y0+px(1770),a1-a0-12,px(80),1,0,'#111',None,PU)
rc(a0+px(690),Y0+px(1280),px(20),px(490),1,0,'#111',None,'#ccc')
def fr(x,y,w,h,c='#111',fill=PU):
    rc(x,y,w,h,1,1,c,None,fill); ln(x+w-px(70),y+h-4,x+w-px(20),y+h-4,1.5,c)
xl,xr=a0+px(66),a0+px(714); wc=px(624)
for k in range(4):
    y=Y0+px(362)+k*px(130); fr(xl,y,wc,px(124))
    for i in range(7): rc(xl+px(22)+i*px(82),y+px(5),px(66),px(115),.6,2,'#777','3,3')
    tx(xl+wc/2,y+px(68),'İÇECEK %d · 7 kanal' % (k+1),6,'middle','bold')
y1=Y0+px(362)+4*px(130); fr(xl,y1,wc,px(316))
for i in range(5): rc(xl+px(50)+i*px(110),y1+px(50),px(85),px(250),.6,4,'#777','3,3')
tx(xl+wc/2,y1+px(170),'1 L · 5 kanal × 8',6,'middle','bold')
for r in range(8):
    y=Y0+px(362)+r*px(105); fr(xr,y,wc,px(99))
    for i in range(4): el(xr+px(95)+i*px(140),y+px(50),px(45),px(28),.6,'#777','3,3')
    tx(xr+wc/2,y+px(92)+2,'TAZE %d · 20 top' % (r+1),5.5,'middle','bold')
tx(a0+px(700),Y0+px(1252),'YATAY İZOLELİ AYIRICI PU 80',6.5,'middle','bold')
xl2,xr2=a0+px(86),a0+px(714); wc2=px(604)
# −18 bandi (49): USTTE kaset kati 29 (v5 oneri: z 28-57, kol erisimi), ALTTA 2 sira hamur cekmecesi (10+10)
yk=Y0+px(1283)
rc(xl2,yk,wc2,px(284),1,1,'#1a49b8',None,'#dfe7fb')
for j in range(4):
    kx_=xl2+px(7.5+j*150); ky_=yk+px(22)
    kap25(kx_,ky_,['KIYMA','KIYMA','KUŞBAŞI','KUŞBAŞI'][j],'',False,'#1a49b8','#eef3ff',5.2,rail=False)
ln(xl2+px(6),yk+px(283),xl2+wc2-px(6),yk+px(283),1.3,'#1a49b8')
tx(xl2+wc2/2,yk+px(13),'KASET KATI −18 · klape 6 (açık) · 4 kap 14×68×24 · L raf · çekmece YOK',4.9,'middle','bold','#1a49b8')
rc(xr2,yk,wc2,px(284),.8,1,'#999','4,3'); notew(xr2+wc2/2,yk+px(130),'boş bant 29 — ileride 3. hamur çekmecesi ya da kavurma',wc2-10,5.5,'#999')
for k in range(2):
    y=Y0+px(1573)+k*px(100)
    for xx_,nm in ((xl2,k+1),(xr2,k+3)):
        fr(xx_,y,wc2,px(94),'#1a49b8','#dfe7fb')
        for i in range(4): el(xx_+px(92)+i*px(140),y+px(48),px(45),px(26),.6,'#1a49b8','3,3')
        tx(xx_+wc2/2,y+px(90),'DONMUŞ %d · 20 top' % nm,5.5,'middle','bold','#1a49b8')
tx((a0+a1)/2,Y0+px(347),'① STORE v4 + v5 ÖNERİ: −18 üstte klapeli KASET KATI (sol modül 4 kap), altta 4 hamur çekmecesi · 17 çekmece × 61 · kapak yok',6.2,'middle','bold','#1d7a4f')

# ================= 2 PRESS v8 (tepsi O32 · catal yuvasi) =================
b0,b1=xs[1],xs[2]; bm=(b0+b1)/2; WB=b1-b0-px(40)
rc(b0+px(15),Y0+px(900),b1-b0-px(30),px(950),1.8,3)
notew(bm,Y0+px(950),"FERSAH PZP-400 (zeminde · 64×80×95 · 170 kg)",WB,7.5,'#111','middle','bold')
rc(bm-px(130),Y0+px(1000),px(260),px(110),1.4,3)
ln(bm,Y0+px(1110),bm,Y0+px(1190),1.6)
rc(bm-px(145),Y0+px(1190),px(290),px(40),1.4,2)
notew(bm,Y0+px(1262),"üst plaka Ø29 ısıtmalı (Ø40 → Ø29: tepsi bordürüne çarpmasın)",WB,6.3)
tray(bm,Y0+px(1380),kulp=False)
rc(bm-px(200),Y0+px(1398),px(400),px(22),1.4,2)
notew(bm,Y0+px(1326),"TEPSİ Ø32 alt plakada bekler · top tepsiye · press tepsi İÇİNDE basar",WB,6.3)
notew(bm,Y0+px(1450),"alt plaka (ısıtmalı) · zeminden ~90",WB,6.3)
rc(b0+px(80),Y0+px(1500),b1-b0-px(160),px(300),1.2,3)
notew(bm,Y0+px(1660),"motor + rezistans · 3,5 kW · 220 V",WB,6.3)
# ust bolge v8: sol yari kova + 14 kol boslugu · sag yari bos · altta yatay uc yuvalari 14 + tepsi rafi 8
xB=b0+px(350); ln(xB,Y0+px(40),xB,Y0+px(640),1.1,'#111','6,5')
rc(b0+px(55),Y0+px(190),px(240),px(440),1.6,3); ln(b0+px(55),Y0+px(240),b0+px(295),Y0+px(240),.8)
tx(b0+px(175),Y0+px(420),'KOVA 30 L',8,'middle','bold'); not_(b0+px(175),Y0+px(465),'kapaksız · poşetli',fs=5.4); not_(b0+px(175),Y0+px(495),'öne çekilir',fs=5.4); not_(b0+px(175),Y0+px(525),'eleman HER GÜN boşaltır',fs=5.4)
rc(b0+px(30),Y0+px(45),px(290),px(140),1,2,'#1a49b8','4,3'); tx(b0+px(175),Y0+px(105),'KOL BOŞLUĞU 14',7,'middle','bold','#1a49b8'); tx(b0+px(175),Y0+px(140),'huni YOK · pençe bırakır',6,'middle','','#1a49b8')
rc(b0+px(380),Y0+px(45),px(290),px(585),1,3,'#999','4,3'); tx(b0+px(525),Y0+px(330),'BOŞ (şimdilik)',8,'middle','bold','#999'); tx(b0+px(525),Y0+px(360),'35×59×84',6.5,'middle','','#999')
ln(b0+px(15),Y0+px(650),b1-px(15),Y0+px(650),1,'#111','6,4')
tx(bm,Y0+px(672),'UÇ YUVALARI — yatay · 14 · uç değiştirici',6.8,'middle','bold')
for k,(ad,alt,dash) in enumerate((('PENÇE','hamur·kutu·içecek',None),('ÇATAL','kap · 50 derinlemesine',None),('boş','kolda olan uç',' 4,3'))):
    x_=b0+px(30+k*225); rc(x_,Y0+px(685),px(205),px(105),1.1,2,'#999' if dash else '#111',dash)
    tx(x_+px(102),Y0+px(730),ad,6,'middle','bold','#999' if dash else '#111'); tx(x_+px(102),Y0+px(765),alt,4.4,'middle','','#777')
ln(b0+px(15),Y0+px(800),b1-px(15),Y0+px(800),1,'#111','6,4')
tx(bm,Y0+px(820),'TEPSİ RAFI — 2 yan yana (+1 kolda) · 8 · Ø32',6.8,'middle','bold','#1a49b8')
for i in range(2):
    cx_=b0+px(180+i*340); el(cx_,Y0+px(855),px(160),px(9),1.2,'#1a49b8'); rc(cx_-px(12),Y0+px(850),px(24),px(10),.8,1,'#1a49b8',None,'#dfe7fb')
not_(bm,Y0+px(886),'v8: sol kova + 14 boşluk · sağ boş · altta uç yuvaları + tepsiler',fs=5.4)

# ================= 3 TOPPING v25 (kap 14x68x24 · 3 kat x 2 · L raf · catal · ALT: 2 sira raf + sogutma dipte · evaporator sol kanal) =================
c0,c1=xs[2],xs[3]; cm2=(c0+c1)/2; WC=c1-c0-px(40)
rc(c0+px(15),Y0+px(5),px(175),px(1185),.8,2,'#7fb3d5','3,3','#eef6fb'); txr(c0+px(100),Y0+px(640),'SOL KANAL 20 — evaporatör + fan (üfleme katlara)',5.2,'#1a49b8')
rc(c0+px(510),Y0+px(5),px(175),px(1185),.8,2,'#7fb3d5','3,3','#eef6fb'); txr(c0+px(600),Y0+px(640),'SAĞ KANAL 20 — hava dönüşü + kablo',5.2,'#1a49b8')
KAPN={0:('KAŞAR A','SUCUK küp'),410:('KAŞAR B','boş / park'),820:('KIYMA kav.','KUŞBAŞI sote')}
for yt in (0,410,820):
    rc(c0+px(15),Y0+px(yt+5),c1-c0-px(30),px(265),.8,2,'#1a49b8','5,3')                 # klape (kat önü, açık çizildi)
    for xk,nm in ((200,KAPN[yt][0]),(360,KAPN[yt][1])):
        bos=nm.startswith('boş')
        kap25(c0+px(xk),Y0+px(yt+10),nm,'',bos)
        if not bos: ln(c0+px(xk+70),Y0+px(yt+250),c0+px(xk+70),Y0+px(yt+300),2,'#1d7a4f')   # ağız → tepsi
    tx(c1-px(22),Y0+px(yt+22),'KAT %d' % (yt//410+1),6.5,'end','bold','#555')
    tx(c0+px(22),Y0+px(yt+22),'klape 4',4.8,'start','','#1a49b8')
for b,zt in ((270,158),(680,117),(1090,76)):
    tray(c0+px(270),Y0+px(b+118),160,True); el(c0+px(430),Y0+px(b+118),px(160),px(18),1,'#1a49b8','4,3')
    tx(c1-px(22),Y0+px(b+40),'boşluk 14 · tepsi Ø32 · düzlem %d' % zt,5.2,'end','','#1a49b8')
# yan kanallar (kat bolgesi): sol evaporator + fan, sag hava donusu + kablo
# ALT 74 = 2 sira x 27 L raf (kaslar yd / park + cozulme) + sogutma grubu dipte 20 (plint = izgara)
tx(c1-px(22),Y0+px(1233),'ALT 74',6.5,'end','bold','#555')
for r_,yt in ((0,1240),(1,1510)):
    for i in range(4):
        xk=47+i*155; lab=[['kaşar yd','kaşar yd','kaşar yd','kaşar yd'],['park','park','çöz. kıyma','çöz. kuşbaşı']][r_][i]
        dsh = r_==1 and i<2
        kap25(c0+px(xk),Y0+px(yt),lab,'',dsh,'#333','#e9eef7',5.2)
    tx(c0+px(22),Y0+px(yt+22),'sıra %d' % (r_+1),4.6,'start','','#555')
    rc(c0+px(15),Y0+px(yt-5),c1-c0-px(30),px(268),.8,2,'#1a49b8','5,3')
rc(c0+px(15),Y0+px(1775),c1-c0-px(30),px(195),1,0,'#555',None,'#cfd8dc')
tx(cm2,Y0+px(1810),'SOĞUTMA GRUBU 20 · 1/12 HP yatay',6,'middle','bold','#37474f')
rc(c0+px(15),Y0+px(1850),c1-c0-px(30),px(120),1,0,'#555',None,'#9e9e9e')
for i in range(9):
    if i not in (3,4,5): ln(c0+px(60)+i*px(70),Y0+px(1870),c0+px(60)+i*px(70),Y0+px(1950),1,'#fff')
tx(cm2,Y0+px(1938),'plint = soğutma ızgarası 12',5.4,'middle','','#fff')

# ================= 4 OVEN v3 (Omake FPZ01.E21 2 kat · sadeyağ KARTUŞU · niş altı boş · plenum + fan + filtre · yan yalıtım 3) =================
d0,d1=xs[3],xs[4]; dm=(d0+d1)/2; WD=d1-d0-px(40)
Zh=lambda z: YZ-px(z*10)          # zeminden cm -> y
# yan yalitim seritleri (2 seramik elyaf + 1 hava) kartus katindan filtre ustune
for xs_ in (d0+4, d1-4-px(30)):
    rc(xs_,Zh(187),px(20),px(145*10),.6,0,'#b08968',None,'#f3f0e6'); rc(xs_+px(20),Zh(187),px(10),px(145*10),.5,0,'#7fb3d5',None,'#eef6fb')
ZON=[(0,12,'#e9e4d6','plint 12 — HAVA GİRİŞİ ızgarası'),(12,42,'#e3f2fb','PANO 30 · PLC I/O · 2 menteşe sürücüsü · 2 SSR · 24 V'),(42,72,'#fff8e0',''),(72,90,'#fbf3e6',''),(146,172,'#fde9c9',''),(172,187,'#eef3f8','FAN 140 m³/h + yağ filtresi + aktif karbon 15'),(187,197,'#e9e4d6','üst çıkış ızgarası → mekân')]
for z0_,z1_,col,lab in ZON:
    rc(d0+px(30),Zh(z1_),d1-d0-px(60),px((z1_-z0_)*10),.8,0,'#555',None,col)
    if lab: notew(dm,Zh((z0_+z1_)/2)+2,lab,WD-px(40),5.4,'#333','middle','bold' if z0_ in (12,146,172) else '')
# firin govdesi 64x56 (z 90-146), 2 kapak (asagi acilir cam), tepsi duzlemleri 95/123
rc(d0+px(30),Zh(146),px(640),px(560),2,3,'#111',None,'#f4f4f4')
for zk0,zk1,nm,tp in ((90,118,'KAPAK 1 · alt kat',95),(118,146,'KAPAK 2 · üst kat',123)):
    rc(d0+px(65),Zh(zk1-4),px(570),px((zk1-zk0-8)*10),1.2,1,'#333',None,'#dbeeff')
    rc(d0+px(65),Zh(zk0+4)+px(12),px(570),px(12),.8,0,'#333',None,'#999')
    tx(dm,Zh((zk0+zk1)/2)+2,nm+' · hazne 40×40×10 · tepsi düzlemi %d' % tp,5.2,'middle','bold','#333')
    rc(d1-4-px(27),Zh(zk0+7),px(24),px(60),1,1,'#c0392b',None,'#f7d7d7')                   # menteşe motoru (yan aralıkta)
tx(d1-px(40),Zh(147.2)+2,'menteşe motoru ×2 Ø28 (yan aralıkta)',4.2,'end','','#c0392b')
# sprey nisi 18 (z 72-90): nozul ustte, alti bos, tepsi onden girer
ci(dm,Zh(88.5),px(30),1,'#c9a227',None,'#fff8e0')
E.append('<polygon points="%.1f,%.1f %.1f,%.1f %.1f,%.1f" fill="#fff3c4" fill-opacity="0.5" stroke="#c9a227" stroke-width="0.6"/>' % (dm,Zh(88.5),dm-px(150),Zh(73.5),dm+px(150),Zh(73.5)))
tray(dm,Zh(75),kulp=True)
tx(dm,Zh(85.5)+2,'SPREY NİŞİ 18 — altı boş · nozül 90° → Ø30 · 4 ml / 0,5 sn',4.8,'middle','bold','#b7791f')
# kartus yuvasi 30 (z 42-72): kartus 4 L + pompa + on kapak (eleman)
rc(d0+px(80),Zh(69),px(200),px(220),1.2,2,'#c9a227',None,'#fff8e0'); tx(d0+px(180),Zh(60)+2,'KARTUŞ 4 L',6,'middle','bold','#8a6a3a'); tx(d0+px(180),Zh(54)+2,'ısıtma ceketi 45 °C',4.6,'middle','','#8a6a3a'); tx(d0+px(180),Zh(49)+2,'kuru bağlantı altta',4.6,'middle','','#8a6a3a')
rc(d0+px(320),Zh(58),px(90),px(80),1,2,'#333',None,'#eee'); tx(d0+px(365),Zh(54)+2,'POMPA',4.8,'middle','bold'); tx(d0+px(365),Zh(47.5)+2,'24 V dişli',4,'middle','','#555')
ln(d0+px(365),Zh(58),d0+px(365),Zh(72),1,'#c9a227'); ln(d0+px(365),Zh(72),dm,Zh(88.5)-px(30),1,'#c9a227')
notew(d0+px(540),Zh(62),'ÖN KAPAK: eleman haftada 1 kartuşu değiştirir (10 gün) · robot dokunmaz',px(220),4.6,'#b7791f','middle','bold')
tx(d0+px(22),Zh(70)+2,'kartuş yuvası 30',4.6,'start','','#8a6a3a')
# hava akisi
for xx_ in (d0+px(19), d1-px(19)):
    ln(xx_,Zh(6),xx_,Zh(40),1,'#7fb3d5'); E.append('<path d="M %.1f %.1f l -3 6 h 6 z" fill="#7fb3d5"/>' % (xx_,Zh(40)))
ln(dm+px(230),Zh(189),dm+px(230),Zh(196),1.2,'#1a49b8'); E.append('<path d="M %.1f %.1f l -3 6 h 6 z" fill="#1a49b8"/>' % (dm+px(230),Zh(196)))
tx(dm,Zh(168)+2,'PLENUM 26 — sıcak hava toplanır',5.4,'middle','bold','#333')
notew(dm,Zh(161),'yan 3 = 2 seramik elyaf + 1 hava aralığı (sol TOPPING +3 °C, sağ PACK karton) · komşu yüzey < oda + 10 °C · bacasız: fırın buharı arka kanaldan plenuma',WD-px(30),4.8,'#555')

# ================= 5 PACK (bicak yildizi YATAY -> onden ince plaka · sarjor 116) =================
e0,e1=xs[4],xs[5]; em=(e0+e1)/2; WE=e1-e0-px(40)
rc(em-px(60),Y0+px(60),px(120),px(90),1.4,3); ln(em,Y0+px(150),em,Y0+px(250),2.6)
rc(em-px(140),Y0+px(250),px(280),px(14),1.6,2)
for i in range(7): ln(em-px(126)+i*px(42),Y0+px(264),em-px(126)+i*px(42),Y0+px(298),1.2)
rc(em-px(200),Y0+px(330),px(400),px(35),1.4,3,'#777',None,'#eee')
tray(em,Y0+px(332),kulp=True)
rc(em-px(160),Y0+px(405),px(320),px(45),1.2,2,'#8a6a3a',None,'#fbf3e6'); notew(em,Y0+px(472),'AÇIK KUTU 32×32×4,5 — tepsi eğilir, pide kayar (ön ağız 13)',WE,5.6,'#8a6a3a')
notew(em,Y0+px(30),'24 V piston · bıçak yıldızı Ø28 YATAY (önden ince plaka)',WE,6)
notew(em,Y0+px(312),'kesim yuvası — tepsi oturur, kilit takılı',WE,5.8)
nk(em,Y0+px(390),'④ bıçak Ø28 (tepsi Ø32, pay 2)',6.5)
for r in range(29):
    for kx in (e0+8, e0+8+px(320)+4): rc(kx,Y0+px(560)+r*px(44),px(320),px(44),1.05)
notew(em,Y0+px(505),'ŞARJÖR: katlanmış kutu 2×2×29 = 116 — ELEMAN katlar (ıslak mendil içinde) · açık deste YOK',WE,5.6)

# ================= UST GORUNUM =================
YT2=YZ+150
tx(X0,YT2-26,"ÜST GÖRÜNÜM",13,"start","bold")
for i,(_ad,_w) in enumerate(M):
    rc(xs[i]+2,YT2,px(_w)-4,px(840),2,5)
YN=YT2+px(880)
# STORE ust v4
ln(am,YT2,am,YT2+px(840),1.4)
for i in range(7): rc(a0+px(62)+i*px(82),YT2+px(60),px(66),px(700),1,2)
for j in range(11): ln(a0+px(62),YT2+px(80)+j*px(62),a0+px(62)+7*px(82),YT2+px(80)+j*px(62),.5,'#999')
tx(a0+px(350),YT2+px(45),'içecek: 7 kanal × 11 kutu (derinlemesine) · 1 L altında',6.5,'middle','','#555')
rc(am+px(85),YT2+px(85),px(530),px(650),1.4)
for j in range(5):
    for i in range(4):
        ci(am+px(162)+i*px(125),YT2+px(160)+j*px(125),px(50),1); ci(am+px(162)+i*px(125),YT2+px(160)+j*px(125),px(60),.7)
tx(am+px(350),YT2+px(45),'taze tepsi 53×65, 4×5 çukur · −18 bandı altta',6.5,'middle','','#555')
rc(a0+px(20),YT2+px(770),a1-a0-px(40),px(60),1.4,0,'#111',None,PU)
notew((a0+a1)/2,YN,'17 çekmece önü (izoleli) + 1 klapeli kaset katı — kapak yok · çekmece 70 tam açılır · kaset katına robot çatalla önden girer (kap 68 ≤ iç 70)',a1-a0-20,7)
# PRESS ust
rc(bm-px(320),YT2+px(20),px(640),px(800),1.6)
ci(b0+px(180),YT2+px(560),px(160),1.1,'#1a49b8','5,4'); ci(b0+px(520),YT2+px(560),px(160),1.1,'#1a49b8','5,4'); tx(bm,YT2+px(790),'tepsi rafı: 2 yan yana (üst, kesik)',6.5,'middle','','#1a49b8')
ci(bm,YT2+px(420),px(145),1.4); ci(bm,YT2+px(420),px(160),1.2,'#1a49b8','4,3')
ci(b0+px(175),YT2+px(640),px(150),1,'#777','4,3'); tx(b0+px(175),YT2+px(645),'kova Ø30 (üst)',5.2,'middle','','#777')
rd(b0+px(275),YT2+px(300),px(160),px(500),1,'#1d7a4f'); txr(b0+px(300),YT2+px(550),'ÇATAL 50 (alt yuva, kesik)',5,'#1d7a4f')
notew(bm,YN,"PZP-400 64×80 · üst plaka Ø29 · üstte 2 tepsi Ø32 yan yana (kesik) · kova Ø30 (üst kat) · altta uç yuvaları, çatal 50 derinlemesine",b1-b0-20,7)
# TOPPING ust v25: kat 1 plani — kaplar 14x68 arka duvara dayali (y 100-780), pay 20, klape 40; helezon ortada, agiz onde y 760; supurme R 270
rc(c0+px(20),YT2,c1-c0-px(40),px(100),1,0,'#555',None,'#d9d9d9'); tx(cm2,YT2+px(34),'arka duvar 10: 6 motor + pano',5.8,'middle','bold','#333')
for xk,nm in ((200,'KAŞAR A'),(360,'SUCUK küp')):
    rc(c0+px(xk),YT2+px(100),px(140),px(680),1.3,2,'#111',None,'#f3efe4')
    for dx_ in (20,120): ln(c0+px(xk+dx_),YT2+px(110),c0+px(xk+dx_),YT2+px(770),.7,'#555','3,2')      # kızak cepleri ±5 (çatal buraya girer)
    ln(c0+px(xk+70),YT2+px(105),c0+px(xk+70),YT2+px(705),1.4,'#1d7a4f')
    rc(c0+px(xk+40),YT2+px(700),px(60),px(65),1.2,1,'#1d7a4f',None,'#eaf6ee'); ci(c0+px(xk+70),YT2+px(732),px(270),1,'#1d7a4f','5,3')
    tx(c0+px(xk+70),YT2+px(400),nm,6.4,'middle','bold'); tx(c0+px(xk+70),YT2+px(430),'14×68',5.6,'middle','','#333')
    rc(c0+px(xk+50),YT2+px(50),px(40),px(50),1,1,'#1a49b8',None,'#dfe7fb')                              # yaylı soket (duvar içinde)
rc(c0+px(15),YT2+px(800),c1-c0-px(30),px(40),1,0,'#1a49b8',None,'#dfe7fb'); tx(cm2,YT2+px(828),'klape 4',4.6,'middle','','#1a49b8')
txr(c0+px(110),YT2+px(440),'sol kanal 20: evaporatör + fan',5,'#1a49b8'); txr(c0+px(590),YT2+px(440),'sağ kanal 20: hava dönüşü + kablo',5,'#1a49b8')
notew(cm2,YT2+px(1050),'kat 1 planı · kap 68 arka duvara dayalı, ara mil yok · ağız ön uçta y 63 (6×6,5), merkez x 27/43 · süpürme R 27 = tepsi 16 + spiral 11 · kesikli = kızak cepleri (çatal) · 10+68+2+4 = 84',c1-c0-20,6.5)
# OVEN ust v3: firin 64x60 onde, arka kanal 20 (hava + kablo + buhar) + arka yalitim 2, yan 3 yalitim
rc(d0+px(30),YT2+px(20),px(640),px(600),1.6,2,'#111',None,'#f4f4f4')
rc(d0+px(30),YT2+px(640),px(640),px(180),.8,0,'#7fb3d5',None,'#eef6fb'); tx(dm,YT2+px(735),'arka kanal 20: hava + kablo + buhar',5,'middle','','#1a49b8')
for xs_ in (d0+4, d1-4-px(30)): rc(xs_,YT2,px(30),px(840),.6,0,'#b08968',None,'#f3f0e6')
rd(dm-px(200),YT2+px(120),px(400),px(400))
ci(dm,YT2+px(320),px(160),1.2,'#1a49b8','4,3'); rc(dm-px(15),YT2+px(480),px(30),px(60),1,1,'#1a49b8'); tx(dm+px(50),YT2+px(560),'kulp 6 (v2 el)',5,'start','','#1a49b8')
tx(dm,YT2+px(90),'kavite 40×40 (kesik) · fırın 64×60',5.2,'middle','','#555')
rc(d0+px(50),YT2+px(545),px(190),px(70),1,2,'#c9a227','4,3','#fff8e0'); tx(d0+px(145),YT2+px(590),'kartuş (alt, kesik)',4.4,'middle','','#8a6a3a')
notew(dm,YN,"fırın 64×60 + arka kanal 20 + arka yalıtım 2 = 84 · yan 3 (yalıtım 2 + hava 1) · tepsi Ø32 + kulp 6 = 38 ≤ 40 ✓ (② kapandı)",d1-d0-20,7)
# PACK ust
rc(em-px(200),YT2+px(440),px(400),px(400),1.4,4,'#777')
ci(em,YT2+px(640),px(160),1.2,'#1a49b8','4,3'); ci(em,YT2+px(640),px(140),1.6)
for dx,dy in [(0,1),(1,0),(0.71,0.71),(0.71,-0.71)]:
    ln(em-px(140)*dx,YT2+px(640)-px(140)*dy,em+px(140)*dx,YT2+px(640)+px(140)*dy,1)
for yy_ in (60,390): rd(e0+8,YT2+px(yy_),px(320),px(320)); rd(e0+8+px(320)+4,YT2+px(yy_),px(320),px(320))
tx(em,YT2+px(50),'şarjör 2×2 (kesik, z 52-182)',5,'middle','','#777')
notew(em,YN,"kesim yuvası (tepsi Ø32) önde · bıçak yıldızı Ø28 yatay · şarjör 2×2 arkada (kesik)",e1-e0-20,7)
# ROBOT KORIDORU
ln(X0,YT2+px(840),X0,YT2+px(1740),1); ln(X0+px(T),YT2+px(840),X0+px(T),YT2+px(1740),1)
ry=YT2+px(1290)
ln(X0+px(200),ry-5,X0+px(T)-px(200),ry-5,1.6); ln(X0+px(200),ry+5,X0+px(T)-px(200),ry+5,1.6)
rc(cm2-px(160),ry-px(90),px(320),px(180),1.6,3); ci(cm2,ry,px(120),1.8)
E.append(f'<path d="M {cm2-px(1300):.1f} {ry:.1f} A {px(1300):.1f} {px(1300):.1f} 0 0 1 {cm2+px(1300):.1f} {ry:.1f}" fill="none" stroke="#111" stroke-width="1" stroke-dasharray="6 5"/>')
notew(cm2+px(230),ry-46,"3-4 m ray · kol 16-20 kg sınıfı, menzil ≥ 130 (CRX-20iA/L 142 · H2017 170 · TM20 130; UR16e 90 ✗) — en ağır yük kıyma kabı 15,2 kg (⑦)",X0+px(T)-cm2-px(260),8.6,"#555","start")
notew(cm2+px(230),ry-20,"uçlar: TEPSİ eli + PENÇE + ÇATAL (uç değiştirici PRESS kabininin altında) · kap değişimleri gece, haftada ≈ 14 + STORE→ALT 4",X0+px(T)-cm2-px(260),8.6,"#555","start")
ln(X0-30,YT2+px(1740),X0+px(T)+30,YT2+px(1740),2.4); ln(X0-30,YT2+px(1762),X0+px(T)+30,YT2+px(1762),1)
tx(X0+px(T)/2,YT2+px(1815),"KAPALI PANEL — CAM YOK · tek açıklık: kiosk + QR teslim dolabı (PICKUP, müşteri cephesi — bu çizimde değil)",10,"middle","","#555")
ox(X0+px(T)+28,YT2,YT2+px(840),"84")
ox(X0+px(T)+28,YT2+px(840),YT2+px(1740),"90 koridor")

# ================= SERVICE =================
sv=X0+px(T)+px(260); sw=px(700)
rc(sv,Y0,sw,px(HG),2.2,5); rc(sv+12,YT,12,px(HA),1.4); rc(sv+sw-24,YT,12,px(HA),1.4)
ln(sv+8,Y0+px(300),sv+sw-8,Y0+px(300),1.4)
rc(sv+px(40),Y0+px(60),px(200),px(160),1.4,3); tx(sv+px(140),Y0+px(155),"UPS",10,"middle","bold")
rc(sv+px(300),Y0+px(90),px(320),px(110),1.4,20); ci(sv+px(320),Y0+px(145),px(28),1.1)
notew(sv+sw/2,Y0+px(262),"TEKNİK: mini UPS (yalnız BEYİN) · yangın tüpü · priz",sw-16,6.3)
ln(sv+8,Y0+px(780),sv+sw-8,Y0+px(780),1); ln(sv+8,Y0+px(1260),sv+sw-8,Y0+px(1260),1.4)
for rrr in (360,830):
    for i in range(6): ln(sv+px(80)+i*px(95),Y0+px(rrr),sv+px(80)+i*px(95),Y0+px(rrr)+px(380),.8)
notew(sv+sw/2,Y0+px(330),"AMBALAJ: yassı kutu 2 raf × 160 = 320 + şarjör 116 (≈ 5 gün, haftada 2 ikmal)",sw-16,6)
rc(sv+px(60),Y0+px(1320),sw-px(120),px(360),1.4,4); ci(sv+px(120),Y0+px(1360),px(16),1.1)
for i in range(4): rc(sv+px(110)+i*px(130),Y0+px(1450),px(90),px(190),1,3)
notew(sv+sw/2,Y0+px(1300),"TEMİZLİK — kilitli · mop kapı içinde",sw-16,6.3)
rc(sv+px(40),Y0+px(1720),sw-px(80),px(100),1.4,3); ln(sv+sw/2-20,Y0+px(1770),sv+sw/2+20,Y0+px(1770),2)
notew(sv+sw/2,Y0+px(1706),"poşet + çöp poşedi çekmecesi",sw-16,6.3)
oy(sv,sv+sw,Y0-24,"70")
tx(sv+sw/2,YZ+24,"7 · SERVICE",11.5,"middle","bold"); tx(sv+sw/2,YZ+42,"(ayrı duvarda — makineye bağlı değil)",9.5,"middle","","#555")

# ================= KONTROL KUTUSU (genis) =================
kx=X0+px(T)+px(220); ky=YT2+10; KW=px(1950)
_ki=len(E)
tx(kx,ky,"KONTROL — istasyonlar arası uyum (6 Eyl 2026, HAT v48)",12,"start","bold","#b3452b")
K=[
 ("① STORE v4 ✓ + v5 ÖNERİ (onay bekliyor): sol modül −18 kaset ÇEKMECESİ → klapeli KASET KATI 29 (4 kap 14×68×24 yan yana: 4×14 + 3×1 + 0,5 = 59,5 ✓; arka PU 8 + 68 + 2 + klape 6 = 84 ✓)","→ kaset katı −18 bandının ÜSTÜNE (z 28–57), hamur çekmeceleri altta (8–28): çatal z 29'da girer · sağ modül bandı boş · 17 çekmece + 1 klape · dikey 2+28+6+84+8+49+8 = 185 ✓","#9a6b1f"),
 ("② ✓ OVEN kavite 40×40×10: tepsi Ø32 + kulp 6 = 38 ≤ 40 — KAPANDI (kulp 6, robot tepsi eli v2)","→ Omake FPZ01.E21 çift katlı (64×60×56, 4,8 kW, 2 camlı kapak aşağı açılır, 24 V lineer aktüatör + 2 switch) · tepsi düzlemleri 95 / 123 · durumlar KAPALI / ÖN ISITMA / BEKLEME 340 / EKO 250 / PİŞİRME","#1d7a4f"),
 ("③ ✓ TEPSİ DÖNMEZ → v25: ağızlar kabın ÖN ucunda (y 76 ≥ 31), merkezler x 27/43; süpürme R 27 = tepsi 16 + spiral 11","→ sol x 0–54, sağ 16–70: duvar içi, pay 0 · spiral 11 kenar kapatma + kaşar akışı → prototip","#1d7a4f"),
 ("④ ✓ PACK: bıçak yıldızı Ø28 yatay, önden ince plaka; açık deste kalktı → şarjör 2×2×29 = 116 kutu (eleman katlar)","→ kesim yuvası tepsi Ø32 + yuva pimleri","#1d7a4f"),
 ("⑤ PRESS üst plaka Ø29 — Fersah cevabı (26 Ağu): CP-330 max 36 cm açar, PLC olur, PZR-250 konveyör olur — AÇIK","→ 'aynı hatta pide olmaz' dedi — yuvarlak Ø30 taban olduğu TEKRAR SORULACAK","#9a6b1f"),
 ("⑥ ✓ PRESS v8: sol yarı 30 L kova + 14 cm kol boşluğu (huni/çekmece yok) · sağ yarı boş","→ altta yatay uç yuvaları 14 (pençe · ÇATAL 50 derinlemesine · boş) + tepsi rafı 8 (2 yan yana + 1 kolda)","#1d7a4f"),
 ("⑦ KOL YÜKÜ AÇIK (v27): kap boş ≈ 5,7 kg (PC 5 mm + taban plakası + POM helezon 66 + tarak + kapak) + çatal 2,0 → kıyma 15,2 kg · sucuk 14,6 · kaşar 12,8","→ 12,5 kg kobot YETMEZ → 16–20 kg sınıfı + menzil ≥ 130 (CRX-20iA/L 142 · H2017 170 · TM20 130; UR16e 90 ✗) ya da kıyma/sucuk 2 günlük dolum (6 kg) — KARAR","#b3452b"),
 ("⑧ ✓ TOPPING v25 yerleşim + v27 KAP (Picnic tipi): dış 14×68×24 · daire duvar R 6,5 + boğaz 7,6 + yalak · POM helezon Ø70 hatve 50 boy 66 + topuz → yaylı soket · göbek + 4 çubuk tarak · şeffaf PC 5 mm · KAPALI BORU ucu (y 62–67) + tek ağız 5×4,5 altta + yaylı menteşeli kapak + raf pimi Ø8 (yalnız TOPPING katında açılır) · kızaklar ±5 · ön çekme dudağı","→ 12,5 L kullanılabilir: kaşar 5,1 kg 1,1 gün (2 poz. 2,3) · kıyma 7,5 kg 2,6 gün · sucuk 6,9 kg 5,7 gün · kuşbaşı 4,3 kg 3 gün → robot ≈ 14 kap/hafta · kap başına 2 soket (helezon z 3,8 + tarak z 14) ya da tek motor + kayış — AÇIK · 3 kat × 2 · kap ARKAYA DAYALI · 2 kızak + 2 L raf · ÇATAL","#1d7a4f"),
 ("⑨ ✓ Dozaj boşluğu 14 × 3 kat (tepsi 158 / 117 / 76 cm) · kilit 8,5 < ağız 11 · her tarif tek düzlemde","→ AÇIK: kat 1 kızağı z 170 + çatal 50 derin → kol menzili / base yüksekliği kontrol","#9a6b1f"),
 ("⑩ ✓ OVEN v3 sadeyağ: KARTUŞ 4 L paslanmaz (16×16×18, ısıtma ceketi 45 °C, kuru bağlantı, kilit) — ELEMAN haftada 1 değiştirir (10 gün), ROBOT DOKUNMAZ · 24 V dişli pompa 0,5 L/dk + ısıtmalı hat Ø6 + çek valf + 90° nozül → Ø30 iz, 4 ml/0,5 sn","→ niş altı boş: robot tepsiyi sokar, 1 sn, çeker · stok 2,8 L/hafta (1 hafta çok değil, ikiye bölmeye gerek yok) · yedek boş kartuş + 16 kg teneke SERVICE'te oda sıcaklığı · şamandıra 'yağ az' → BEYİN","#1d7a4f"),
 ("⑪ 197 ✓ · 420 ✓ (OVEN 65 → 70: menteşe motorları + yan yalıtım 3) · derinlik 84 HER KABİN ✓ · TOPPING 3×(27+14) + 74 = 197 · OVEN 12 + 30 + 30 + 18 + 56 + 26 + 15 + 10 = 197 ✓","→ TOPPING derinlik 10 + 68 + 2 + 4 = 84 ✓ · STORE kaset katı 8 + 68 + 2 + 6 = 84 ✓ · OVEN fırın 60 + arka kanal 20 + yalıtım 2 = 84 ✓ · TOPPING ve OVEN'de ayak yerine plint 12 (ızgara) · OVEN ısı: bekleme 0,7 kW, egzoz +15 °C, günde 6–8 kWh mekâna (küçük radyatör kadar)","#1d7a4f"),
 ("⑬ ÇATAL ucu: 2 lama 16×12 mm × 50 cm + sırt plakası ≈ 2 kg · dizi: gir 50 → kaldır 0,5 → çek 70 (5° yatık taşıma) · 18 çift L raf (TOPPING 6 + ALT 8 + STORE 4) · çatal aralığı 10 (kızak ±5)","→ haftalık (v27 kap): robot ≈ 14 kap değişimi (kaşar 6 · kıyma 3 · kuşbaşı 2 · sucuk 1 + park) + 4 STORE→ALT taşıma (gece) · eleman haftada 1 (kaplar + OVEN yağ kartuşu, boşları alır) · uç değiştirici PRESS alt yuvaları","#1d7a4f"),
 ("⑫ Pide Ø30 → tepsi Ø32 zinciri: PRESS plaka Ø29 ✓ · PACK bıçak Ø28 ✓ · OVEN 38 ✓ (kulp 6) · robot tepsi eli v1 (Ø34) → v2 GEREK (kulp 6 + çatal)","→ harçlar KAVRULMUŞ/SOTE vakumlu (çiğ olmaz) · açıklar: tırnak-cep hizası (pim + kamera) · −18 raf buzlanması · klape contaları · soğutma grubu ≤ 20 boy · v27: yayıcı plaka mı spiral süpürme mi · gramaj prototipi (123 cm³/dev) · PC çizilme · OVEN: kuru bağlantı (CPC gıda tipi), karbon filtre, tepsili pide pilotu","#9a6b1f"),
]
yy=ky+22
KWc=KW-24
for a_,b_,c_ in K:
    for l in wrap(a_,int(KWc/(8.6*0.53))): tx(kx,yy,l,8.6,"start","bold",c_); yy+=12
    for l in wrap(b_,int(KWc/(8.2*0.53))): tx(kx+12,yy,l,8.2,"start","","#444"); yy+=11.5
    yy+=5
E.insert(_ki, '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="6" fill="#fff8f5" stroke="#b3452b" stroke-width="1.4"/>' % (kx-10,ky-18,KW,yy-ky+22))
_kbot=yy

# ================= OLCULER + BASLIK =================
for i,(ad,w) in enumerate(M):
    oy(xs[i],xs[i+1],Y0-24,str(round(w/10)))
    tx((xs[i]+xs[i+1])/2,YZ+24,ad,10.5,w="bold")
oy(X0,X0+px(T),YZ+52,"TOPLAM "+str(round(T/10))+" cm",12)
ox(X0-30,Y0,YT,str(round(HG/10))); ox(X0-30,YT,YZ,str(round(HA/10))); ox(X0-64,Y0,YZ,"TOPLAM "+str(round((HG+HA)/10)))
tx(X0,Y0-94,"AUTOKITCH — HAT v48 · TÜM İSTASYONLAR SON VERSİYON (6 Eyl 2026) — STORE v4 (+ v5 öneri) · PRESS v8 · TOPPING v25 yerleşim + v27 KAP (Picnic tipi, kapalı boru + menteşeli kapak) · OVEN v3 (Omake 2 kat · sadeyağ KARTUŞU · kolon 70) · PACK 116",15,"start","bold")
tx(X0,Y0-72,"Robot: tek kol, 16–20 kg sınıfı (en ağır yük: kıyma 7,5 + kap 5,7 + çatal 2,0 = 15,2 kg — ⑦ açık) · uç değiştirici: TEPSİ eli (pide press'ten kutuya kadar tepside, fırına tepsiyle) + PENÇE (hamur · kutu · içecek) + ÇATAL (kap, forklift gibi önden). Mavi = tepsi Ø32 (pide Ø30). Kırmızı = KONTROL bulgusu.",10,"start","","#333")
tx(X0,Y0-54,"Ölçüler cm. HER KABİN 70/140 × 197 × 84 (gövde 185 + ayak 12; TOPPING ve OVEN'de ayak yerine plint 12 = ızgara). Açık: ⑤ Fersah Ø30 taban · ⑦ kol yükü 15,2 kg + menzil · ⑫ robot tepsi eli v2 (kulp 6) · ① STORE v5 onayı · TOPPING prototipleri (spiral 11, kaşar akışı, çatal-cep hizası) · OVEN: kuru bağlantı tipi, karbon filtre tedariki, tepsili pide pilotu",10,"start","","#333")

W=int(X0+px(T)+px(2200)); H=int(max(YT2+px(1990), _kbot+40))
svg=(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}"><rect width="{W}" height="{H}" fill="#ffffff"/>'+''.join(E)+'</svg>')
xml.dom.minidom.parseString(svg.encode('utf-8'))
OUT=r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\FULL_MAKINE\hat_on_gorunus_teknik_v48.svg"
io.open(OUT,'w',encoding='utf-8').write(svg)
print('yazildi + XML gecerli:',OUT,'|',W,'x',H)
