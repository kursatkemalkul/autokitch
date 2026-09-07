# -*- coding: utf-8 -*-
"""HAT v51 (v50 + PACK v4: ustten beslemeli kutu acici, sarjor 84 cm 525 blank, tek dikey eksen + kalip, plint) — v50 (v49 + OVEN v5: tek yag kabi sol, sag slot bos, 12 L = 30 gun, tek pompa) — v49 (v48 + OVEN v4: 2 standart yag kabi sag/sol + pompalar arkada + sprey ortada, KESME presi OVEN, PACK = sarjor + kutulama, zonlar hesapla kuculdu) — v48 (v47 + OVEN v3: kolon 70, hat 420, kartus, nis alti bos, plenum/fan/filtre, yan yalitim; TOPPING v27 sayilari, kizak ±5; ② ⑩ kapandi) — v47 (v46 + TOPPING kap simgesi v26 Picnic tipi, ⑦ 15,4, ⑧ v26, robot ≈ 12 kap/hafta) — v46: TUM ISTASYONLAR SON VERSIYON (5 Eyl 2026): STORE v4 (+ v5 oneri: −18 kaset kati ustte, klapeli, 4 kap sol modul) ·
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
    if i not in (2,3,4): rc(_x+14,YT,12,px(HA),1.4); rc(_x+px(_w)-26,YT,12,px(HA),1.4)   # TOPPING + OVEN + PACK: ayak yerine plint
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

# ================= 4 OVEN v4 (Omake 2 kat · 2 STANDART YAĞ KABI + sprey ortada · KESME presi · plenum/fan 12 · filtre 5 opsiyon · yan yalıtım 3) =================
d0,d1=xs[3],xs[4]; dm=(d0+d1)/2; WD=d1-d0-px(40)
Zh=lambda z: YZ-px(z*10)          # zeminden cm -> y
for xs_ in (d0+4, d1-4-px(30)):
    rc(xs_,Zh(185),px(20),px(103*10),.6,0,'#b08968',None,'#f3f0e6'); rc(xs_+px(20),Zh(185),px(10),px(103*10),.5,0,'#7fb3d5',None,'#eef6fb')
ZON=[(0,12,'#e9e4d6','plint 12 — hava girişi ızgarası'),(12,32,'#e3f2fb','PANO 20 · PLC · menteşe ×2 + pres sürücüsü · 2 SSR · pompa rölesi · 24 V'),(32,82,'#f4eef8',''),(82,112,'#fff8e0',''),(168,180,'#fde9c9','PLENUM 12 + FAN Ø120 (şart)'),(180,185,'#eef3f8','karbon filtre 5 (opsiyon)'),(185,197,'#f7f7f7','')]
for z0_,z1_,col,lab in ZON:
    rc(d0+px(30),Zh(z1_),d1-d0-px(60),px((z1_-z0_)*10),.8,0,'#555',None,col)
    if lab: notew(dm,Zh((z0_+z1_)/2)+2,lab,WD-px(40),5.2,'#333','middle','bold' if z0_ in (12,168) else '')
tx(dm,Zh(193.5)+2,'üst boşluk 12 (yedek)',4.6,'middle','','#333'); notew(dm,Zh(188.5)+2,'yan 3 = 2 yalıtım + 1 hava · egzoz üst ızgaradan mekâna (bacasız)',WD-px(30),4.2,'#555')
# fırın 64×56 (z 112-168), tepsi düzlemleri 117/145
rc(d0+px(30),Zh(168),px(640),px(560),2,3,'#111',None,'#f4f4f4')
for zk0,zk1,nm,tp in ((112,140,'KAPAK 1 · alt kat',117),(140,168,'KAPAK 2 · üst kat',145)):
    rc(d0+px(65),Zh(zk1-4),px(570),px((zk1-zk0-8)*10),1.2,1,'#333',None,'#dbeeff')
    rc(d0+px(65),Zh(zk0+4)+px(12),px(570),px(12),.8,0,'#333',None,'#999')
    tx(dm,Zh((zk0+zk1)/2)+2,nm+' · hazne 40×40×10 · tepsi düzlemi %d' % tp,5.2,'middle','bold','#333')
    rc(d1-4-px(27),Zh(zk0+7),px(24),px(60),1,1,'#c0392b',None,'#f7d7d7')
tx(d1-px(40),Zh(169.2)+2,'menteşe motoru ×2 Ø28 (yan aralıkta)',4.2,'end','','#c0392b')
ci(dm-px(230),Zh(174),px(50),1,'#333',None,'#fff'); tx(dm-px(230),Zh(174)+2,'FAN',4,'middle','bold')
# YAĞ + SPREY 30 (z 82-112): 2 standart kap yanlarda (slot 15), tepsi ortada (34), nozül üstte, klape 4 önde, sıcak dolap 42
rc(d0+px(525),Zh(108),px(140),px(240),.8,1,'#999','4,3','none'); tx(d0+px(595),Zh(96)+2,'boş 15',4.4,'middle','','#999')
for x0_ in (35,):
    rc(d0+px(x0_),Zh(108),px(140),px(240),1.1,1,'#c9a227',None,'#dbeeff'); rc(d0+px(x0_+5),Zh(102),px(130),px(170),0,0,'none',None,'#f6d76b')
    for dx_ in (20,120): rc(d0+px(x0_+dx_-15),Zh(84),px(30),px(20),.6,0,'#555',None,'#d0d7de')
    ln(d0+px(x0_-6),Zh(82),d0+px(x0_+146),Zh(82),1.2,'#555')
    tx(d0+px(x0_+70),Zh(96)+2,'YAĞ KABI',4.6,'middle','bold','#8a6a3a'); tx(d0+px(x0_+70),Zh(91)+2,'12 L · 30 gün',4,'middle','','#8a6a3a')
ci(dm,Zh(106),px(30),1,'#c9a227',None,'#fff8e0')
E.append('<polygon points="%.1f,%.1f %.1f,%.1f %.1f,%.1f" fill="#fff3c4" fill-opacity="0.5" stroke="#c9a227" stroke-width="0.6"/>' % (dm,Zh(106),dm-px(150),Zh(90),dm+px(150),Zh(90)))
tray(dm,Zh(90),kulp=False)
rc(d0+px(190),Zh(85),px(320),px(15),.6,0,'#555',None,'#ccc')
tx(dm,Zh(110.5)+2,'YAĞ + SPREY 30 · kap 15 | tepsi 34 | boş 15 · klape 4 · sıcak dolap 42 °C',4.4,'middle','bold','#b7791f')
tx(dm,Zh(86.5)+2,'damlalık',3.6,'middle','','#555')
# KESME 50 (z 32-82): zemin plakası + halka, tepsi, pide, bıçak yıldızı +, kızak, 2 mil, aktüatör dikey
rc(d0+px(120),Zh(36),px(460),px(20),1,0,'#333',None,'#bbb')
tray(dm,Zh(36),kulp=False)
E.append('<path d="M %.1f %.1f A %.1f %.1f 0 0 1 %.1f %.1f Z" fill="#f0d9a8" stroke="#8a6a3a" stroke-width="0.8"/>' % (dm-px(150),Zh(36),px(150),px(40),dm+px(150),Zh(36)))
rc(d0+px(210),Zh(48),px(280),px(40),1,0,'#333',None,'#e8e8e8'); ln(d0+px(210),Zh(44),d0+px(490),Zh(44),1.4,'#111')
rc(d0+px(320),Zh(51),px(60),px(30),.8,1,'#333',None,'#ccc'); rc(d0+px(170),Zh(54),px(360),px(30),1,0,'#333',None,'#ddd')
for xg in (190,510): ln(d0+px(xg),Zh(34),d0+px(xg),Zh(72),1.6,'#555'); rc(d0+px(xg-12),Zh(54),px(24),px(30),.6,0,'#333',None,'#999')
rc(d0+px(310),Zh(78),px(80),px(210),1.2,2,'#6b4fa8',None,'#ece6f5'); ln(dm,Zh(54),dm,Zh(57),2,'#6b4fa8')
tx(d0+px(405),Zh(73)+2,'AKTÜATÖR 24 V',4,'start','bold','#6b4fa8'); tx(d0+px(405),Zh(68)+2,'1500 N · 100 mm',3.8,'start','','#6b4fa8'); tx(d0+px(405),Zh(63)+2,'kendini kilitler',3.8,'start','','#6b4fa8')
tx(dm,Zh(80.5)+2,'KESME 50 · bıçak + (2 × 28) · tepsi zemine dayanır · 0,85–1,1 kN',4.4,'middle','bold','#6b4fa8')
tx(d0+px(100),Zh(45)+2,'bıçak',3.6,'end','','#333'); tx(d0+px(100),Zh(38)+2,'pide',3.6,'end','','#8a6a3a'); tx(d0+px(100),Zh(55)+2,'kızak',3.6,'end','','#333')
# hava
for xx_ in (d0+px(19), d1-px(19)):
    ln(xx_,Zh(6),xx_,Zh(30),1,'#7fb3d5'); E.append('<path d="M %.1f %.1f l -3 6 h 6 z" fill="#7fb3d5"/>' % (xx_,Zh(30)))
ln(dm+px(230),Zh(187),dm+px(230),Zh(196),1.2,'#1a49b8'); E.append('<path d="M %.1f %.1f l -3 6 h 6 z" fill="#1a49b8"/>' % (dm+px(230),Zh(196)))

# ================= 5 PACK v4 (üstten beslemeli kutu açıcı: yığın üstte · vakum plunger · kalıp plakası z 60 · kapak kolu · plint) =================
e0,e1=xs[4],xs[5]; em=(e0+e1)/2; WE=e1-e0-px(40)
Ze=lambda z: YZ-px(z*10)
PZ=[(0,12,'#e9e4d6','plint 12'),(12,30,'#e3f2fb','PANO 18 · PLC · step + 2 motor sürücü · 3 servo · 24 V'),(30,45,'#eef3f8','STEP NEMA 23 + bilyalı vida · VAKUM POMPASI 24 V 30 L/dk'),(45,55,'#f4f0fa','BOYUNDURUK 36×72 (tek dikey eksen, strok 48)'),(55,60,'#f4f0fa',''),(60,104,'#fbf3e6',''),(104,188,'#fff8e0',''),(188,197,'#e9e4d6','üst pay 9')]
for z0_,z1_,col,lab in PZ:
    rc(e0+px(30),Ze(z1_),e1-e0-px(60),px((z1_-z0_)*10),.8,0,'#555',None,col)
    if lab: notew(em,Ze((z0_+z1_)/2)+2,lab,WE-px(20),5.2,'#333','middle','bold' if z0_ in (12,45) else '')
# sarjor: yatay yigin 84 cm
rc(e0+px(150),Ze(188),px(400),px(840),.8,0,'#5a3d13',None,'#e8d8b0')
for i in range(1,21): ln(e0+px(150),Ze(104+i*4),e0+px(550),Ze(104+i*4),.35,'#a8905e')
for xx_ in (e0+px(140),e0+px(552)): rc(xx_,Ze(190),px(8),px(860),1,0,'#333',None,'#333')
notew(em,Ze(150),'ŞARJÖR 84: 525 açık kutu (blank 40×76, E-dalga 1,6 mm) yatay yığın · 80 pide: 3 gün 38 cm · 5 gün 64 · dolu 6,6 gün · eleman haftada 1 demet sürer (ön kapı)',px(380),5.2,'#5a3d13','middle','bold')
rc(e0+px(140),Ze(104.6),px(420),px(6),.8,0,'#333',None,'#333'); tx(em,Ze(106.5)+2,'alt tutucu raylar (yığın ağırlığı burada) — en alttaki vakumla aşağı çekilir',4.4,'middle','','#333')
# kalip plakasi z 60 + pencere + kutu
rc(e0+px(30),Ze(60.6),e1-e0-px(60),px(6),.8,0,'#333',None,'#999')
rc(e0+px(187),Ze(60),px(6),px(45),.8,0,'#333',None,'#666'); rc(e0+px(507),Ze(60),px(6),px(45),.8,0,'#333',None,'#666')
tx(em,Ze(57.5)+2,'kalıp: pencere 32,5 · duvar 4,5 · köşe plowları',4.4,'middle','','#333')
rc(e0+px(189),Ze(64.6),px(323),px(40),1.2,0,'#5a3d13',None,'#e8d8b0'); tx(em,Ze(68)+2,'KUTU plakada (yükseldi) · kapak açık arkada · z 60',5,'middle','bold','#5a3d13')
# plunger + vantuz + posts
rc(e0+px(192),Ze(58),px(316),px(20),1.1,1,'#6b4fa8',None,'#ece6f6'); tx(em,Ze(53)+2,'plunger 31,6 + 6 vantuz Ø40',4.4,'middle','','#6b4fa8')
for xx_ in (220,480): rc(e0+px(xx_-15),Ze(59),px(30),px(10),.7,0,'#6b4fa8',None,'#fff')
ln(em,Ze(45),em,Ze(55),1.4,'#333')
# kapak yayi + kol
rc(e0+px(189),Ze(100.6),px(323),px(360),.8,0,'#5a3d13','4 3','none')
tx(em,Ze(102)+2,'kapak dikey geçerken (kesik) tepe z 100 < 104 ✓ · U çevirme kolu 24 V + 3 flap parmağı (servo)',4.4,'middle','','#5a3d13')
ln(e0+px(120),Ze(72),e0+px(120),Ze(97),1.1,'#6b4fa8'); E.append('<path d="M %.1f %.1f l -3 6 h 6 z" fill="#6b4fa8"/>' % (e0+px(120),Ze(97))); tx(e0+px(112),Ze(84)+2,'plunger ↑48',4,'end','','#6b4fa8')
ln(e0+px(580),Ze(97),e0+px(580),Ze(72),1.1,'#5a3d13'); E.append('<path d="M %.1f %.1f l -3 -6 h 6 z" fill="#5a3d13"/>' % (e0+px(580),Ze(72))); tx(e0+px(588),Ze(84)+2,'blank ↓',4,'start','','#5a3d13')
tray(em,Ze(75),kulp=True); tx(em,Ze(79)+2,'tepsi eğilir, 4 parça kayar · pençe alır',4.4,'middle','','#1a49b8')
# klape + on kapi
rc(e0+px(18),Ze(104),px(10),px(440),1,0,'#1a49b8',None,'#dfe7fb'); txr(e0+px(12),Ze(82),'KLAPE 66×44 (robot)',4,'#1a49b8','bold')
rc(e0+px(18),Ze(197),px(10),px(930),1,0,'#b7791f',None,'#fde9c9'); txr(e0+px(12),Ze(150),'ÖN KAPI (eleman)',4,'#b7791f','bold')
tx(em,Ze(6)+2,'plint 12',4.6,'middle','','#333')

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
# OVEN ust v4: fırın 64×60 önde + arka kanal 20 + arka yalıtım 2; altta (kesik): 2 yağ kabı 68 yanlarda + pompalar arkada, tepsi ortada
rc(d0+px(30),YT2+px(20),px(640),px(600),1.6,2,'#111',None,'#f4f4f4')
rc(d0+px(30),YT2+px(640),px(640),px(180),.8,0,'#7fb3d5',None,'#eef6fb'); tx(dm,YT2+px(735),'arka kanal 20: hava + kablo + buhar',5,'middle','','#1a49b8')
for xs_ in (d0+4, d1-4-px(30)): rc(xs_,YT2,px(30),px(840),.6,0,'#b08968',None,'#f3f0e6')
rd(dm-px(200),YT2+px(120),px(400),px(400))
ci(dm,YT2+px(320),px(160),1.2,'#1a49b8','4,3'); rc(dm-px(15),YT2+px(480),px(30),px(60),1,1,'#1a49b8'); tx(dm+px(50),YT2+px(560),'kulp 6 (v2 el)',5,'start','','#1a49b8')
tx(dm,YT2+px(90),'kavite 40×40 (kesik) · fırın 64×60',5.2,'middle','','#555')
for x0_ in (35,):
    rc(d0+px(x0_),YT2+px(40),px(140),px(680),1,2,'#c9a227','4,3','none'); tx(d0+px(x0_+70),YT2+px(400),'yağ kabı',4.4,'middle','','#8a6a3a'); tx(d0+px(x0_+70),YT2+px(430),'68 (alt, kesik)',4,'middle','','#8a6a3a')
    rc(d0+px(x0_+20),YT2+px(730),px(100),px(90),.8,2,'#333','3,2','none'); tx(d0+px(x0_+70),YT2+px(785),'pompa',3.8,'middle','','#333')
notew(dm,YN,"fırın 64×60 + arka kanal 20 + yalıtım 2 = 84 · alt zon: 1 yağ kabı 68 (sol slot 15, sağ boş) + kuru bağlantı + pompa arkada, tepsi Ø32 ortada (34) · fırında tepsi + kulp 6 = 38 ≤ 40 ✓",d1-d0-20,7)
# PACK ust v4: kalip plakasi — pencere 32,5 onde (y 5,5–38), kapak bolgesi arkada (orta ray + flap parmaklari), yigin kilavuzlari 40, U kol
rc(e0+px(150),YT2+px(65),px(400),px(760),.6,0,'#5a3d13','3,2','#f3ead6')
rc(em-px(162),YT2+px(460),px(325),px(325),1.3,0,'#111',None,'#fff'); tx(em,YT2+px(630),'PENCERE 32,5',5.2,'middle','bold'); tx(em,YT2+px(660),'kutu burada oluşur',4.2,'middle','','#777')
ci(em,YT2+px(640),px(160),1,'#1a49b8','4,3')
for (xx_,yy_) in ((-130,510),(130,510),(-130,760),(130,760)): ci(em+px(xx_),YT2+px(yy_),px(20),.8,'#6b4fa8','3,2')
rc(em-px(50),YT2+px(50),px(100),px(410),.6,0,'#777',None,'#e6e6e6')
for yy_ in (160,340): rc(em-px(15),YT2+px(yy_),px(30),px(44),.6,0,'#6b4fa8',None,'#ece6f6')
rd(e0+px(150),YT2+px(100),px(40),px(320),.8,'#b7791f'); rd(e0+px(510),YT2+px(100),px(40),px(320),.8,'#b7791f'); rd(e0+px(190),YT2+px(60),px(320),px(40),.8,'#b7791f')
for xx_ in (e0+px(140),e0+px(552)): rc(xx_,YT2+px(60),px(8),px(770),1,0,'#333',None,'#333')
ln(e0+px(130),YT2+px(460),e0+px(130),YT2+px(160),1.4,'#1d7a4f'); ln(e0+px(570),YT2+px(460),e0+px(570),YT2+px(160),1.4,'#1d7a4f'); ln(e0+px(130),YT2+px(160),e0+px(570),YT2+px(160),1.4,'#1d7a4f')
tx(em,YT2+px(30),'ön dil parmağı · yan flap parmakları (turuncu) · U kol (yeşil)',4.4,'middle','','#777')
notew(em,YN,"kalıp plakası z 60: pencere 32,5 önde (tepsi Ø32 kesik), kapak bölgesi arkada (orta ray + 3 flap parmağı), yığın kılavuzları 40, blank izi 40×76 (kesik) · üstte şarjör 84",e1-e0-20,7)
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
tx(kx,ky,"KONTROL — istasyonlar arası uyum (6 Eyl 2026, HAT v51)",12,"start","bold","#b3452b")
K=[
 ("① STORE v4 ✓ + v5 ÖNERİ (onay bekliyor): sol modül −18 kaset ÇEKMECESİ → klapeli KASET KATI 29 (4 kap 14×68×24 yan yana: 4×14 + 3×1 + 0,5 = 59,5 ✓; arka PU 8 + 68 + 2 + klape 6 = 84 ✓)","→ kaset katı −18 bandının ÜSTÜNE (z 28–57), hamur çekmeceleri altta (8–28): çatal z 29'da girer · sağ modül bandı boş · 17 çekmece + 1 klape · dikey 2+28+6+84+8+49+8 = 185 ✓","#9a6b1f"),
 ("② ✓ OVEN kavite 40×40×10: tepsi Ø32 + kulp 6 = 38 ≤ 40 — KAPANDI (kulp 6, robot tepsi eli v2)","→ Omake FPZ01.E21 çift katlı (64×60×56, 4,8 kW, 2 camlı kapak aşağı açılır, 24 V lineer aktüatör + 2 switch) · tepsi düzlemleri 95 / 123 · durumlar KAPALI / ÖN ISITMA / BEKLEME 340 / EKO 250 / PİŞİRME","#1d7a4f"),
 ("③ ✓ TEPSİ DÖNMEZ → v25: ağızlar kabın ÖN ucunda (y 76 ≥ 31), merkezler x 27/43; süpürme R 27 = tepsi 16 + spiral 11","→ sol x 0–54, sağ 16–70: duvar içi, pay 0 · spiral 11 kenar kapatma + kaşar akışı → prototip","#1d7a4f"),
 ("④ ✓ PACK v4 = ÜSTTEN BESLEMELİ KUTU AÇICI: açık kutu (blank 40×76, 32×32×4 köşe tırnaklı) yığını üstte 84 cm = 525 (3 gün 38 cm garanti · 5 gün 64 hedef · dolu 6,6 gün; 7 gün 90 sığmaz) · tek dikey eksen (bilyalı vida + NEMA 23, strok 48): plunger + 6 vantuz Ø40 en alt blankı çeker, kalıp penceresinden tabanı 4 cm çekince duvarlar + tırnaklar katlanır (1 vuruş) · kutu plakaya (z 60) yükselir · tepsi eğilir 4 parça kayar · 3 flap parmağı + U kol kapağı kapatır · eksen 6 kaldırır, pençe alır → PICKUP","→ zonlar: plint 12 / pano 18 / step+vakum 15 / boyunduruk 10 / kalıp 5 / yükleme 44 (kapak yayı 40) / şarjör 84 / üst 9 = 197 ✓ · derinlik blank 76 + 2×4 = 84 ✓ · kompresör yok (24 V diyafram vakum pompası) · çevrim 15 sn · eleman haftada 1 demet sürer · AÇIK: dolu yığın 60 kg vantuz payı 1,2× (pilot 40 cm), blank bıçak kalıbı, flap kapanması (pençe yedek) · KESİM OVEN'de (v4 pres)","#1d7a4f"),
 ("⑤ PRESS üst plaka Ø29 — Fersah cevabı (26 Ağu): CP-330 max 36 cm açar, PLC olur, PZR-250 konveyör olur — AÇIK","→ 'aynı hatta pide olmaz' dedi — yuvarlak Ø30 taban olduğu TEKRAR SORULACAK","#9a6b1f"),
 ("⑥ ✓ PRESS v8: sol yarı 30 L kova + 14 cm kol boşluğu (huni/çekmece yok) · sağ yarı boş","→ altta yatay uç yuvaları 14 (pençe · ÇATAL 50 derinlemesine · boş) + tepsi rafı 8 (2 yan yana + 1 kolda)","#1d7a4f"),
 ("⑦ KOL YÜKÜ AÇIK (v27): kap boş ≈ 5,7 kg (PC 5 mm + taban plakası + POM helezon 66 + tarak + kapak) + çatal 2,0 → kıyma 15,2 kg · sucuk 14,6 · kaşar 12,8","→ 12,5 kg kobot YETMEZ → 16–20 kg sınıfı + menzil ≥ 130 (CRX-20iA/L 142 · H2017 170 · TM20 130; UR16e 90 ✗) ya da kıyma/sucuk 2 günlük dolum (6 kg) — KARAR","#b3452b"),
 ("⑧ ✓ TOPPING v25 yerleşim + v27 KAP (Picnic tipi): dış 14×68×24 · daire duvar R 6,5 + boğaz 7,6 + yalak · POM helezon Ø70 hatve 50 boy 66 + topuz → yaylı soket · göbek + 4 çubuk tarak · şeffaf PC 5 mm · KAPALI BORU ucu (y 62–67) + tek ağız 5×4,5 altta + yaylı menteşeli kapak + raf pimi Ø8 (yalnız TOPPING katında açılır) · kızaklar ±5 · ön çekme dudağı","→ 12,5 L kullanılabilir: kaşar 5,1 kg 1,1 gün (2 poz. 2,3) · kıyma 7,5 kg 2,6 gün · sucuk 6,9 kg 5,7 gün · kuşbaşı 4,3 kg 3 gün → robot ≈ 14 kap/hafta · kap başına 2 soket (helezon z 3,8 + tarak z 14) ya da tek motor + kayış — AÇIK · 3 kat × 2 · kap ARKAYA DAYALI · 2 kızak + 2 L raf · ÇATAL","#1d7a4f"),
 ("⑨ ✓ Dozaj boşluğu 14 × 3 kat (tepsi 158 / 117 / 76 cm) · kilit 8,5 < ağız 11 · her tarif tek düzlemde","→ AÇIK: kat 1 kızağı z 170 + çatal 50 derin → kol menzili / base yüksekliği kontrol","#9a6b1f"),
 ("⑩ ✓ OVEN v5 sadeyağ: 1 STANDART KAP (yağ versiyonu: helezon/tarak yok, taban kapalı, geçmeli kapak + dolum ağzı, arka soket = kuru bağlantı, şamandıra) sol slot 15 (sağ 15 boş), 12 L = 30 gün, dolu 14,1 kg — ELEMAN ayda 1 değiştirir (kapanışta, dolapta sabaha erir), ROBOT DOKUNMAZ · 1 mini pompa 24 V arka duvarda, şamandıra 4 gün kala 'yağ az'","→ sprey ortada (34): nozül 20 derinlikte, tepsi 40 girer, 4 ml / 0,5 sn · zon = sıcak dolap 42 °C (klape 4; sadeyağ 32 °C altında katı, pompalanmaz; pide için sıcak şart değil) · hat ısıtması yok (dolapta) · damlalık haftalık · alternatif: sıvı yağ → ısıtıcı yok (lezzet kararı)","#1d7a4f"),
 ("⑪ 197 ✓ · 420 ✓ · derinlik 84 HER KABİN ✓ · TOPPING 3×(27+14) + 74 = 197 · OVEN v4 zeminden: plint 12 + pano 20 + KESME 50 + YAĞ/SPREY 30 + fırın 56 + plenum/fan 12 + filtre 5 + yedek 12 = 197 ✓ (v3'e göre plenum+filtre+üst 51 → 17, pano 30 → 20, niş 18 kalktı)","→ OVEN derinlik: fırın 60 + arka kanal 20 + yalıtım 2 = 84 ✓ · yağ zonu: kap 68 + kuru bağlantı 4 + pompa 12 = 84 ✓ · genişlik kap 15 + tepsi 34 + boş 15 = 64 ✓ · TOPPING 10 + 68 + 2 + 4 = 84 ✓ · STORE kaset 8 + 68 + 2 + 6 = 84 ✓ · fan ŞART (kabin ısısı), karbon filtre OPSİYON (AVM), baca YOK (elektrikli) · ısı mekâna günde 6–8 kWh","#1d7a4f"),
 ("⑬ ÇATAL ucu: 2 lama 16×12 mm × 50 cm + sırt plakası ≈ 2 kg · dizi: gir 50 → kaldır 0,5 → çek 70 (5° yatık taşıma) · 18 çift L raf (TOPPING 6 + ALT 8 + STORE 4) · çatal aralığı 10 (kızak ±5)","→ haftalık (v27 kap): robot ≈ 14 kap değişimi (kaşar 6 · kıyma 3 · kuşbaşı 2 · sucuk 1 + park) + 4 STORE→ALT taşıma (gece) · eleman haftada 1 (kaplar + OVEN yağ kartuşu, boşları alır) · uç değiştirici PRESS alt yuvaları","#1d7a4f"),
 ("⑫ Pide Ø30 → tepsi Ø32 zinciri: PRESS plaka Ø29 ✓ · OVEN kesme bıçağı Ø28 ✓ (PACK'ten taşındı) · OVEN fırın 38 ✓ (kulp 6) · robot tepsi eli v1 (Ø34) → v2 GEREK (kulp 6 + çatal)","→ harçlar KAVRULMUŞ/SOTE vakumlu (çiğ olmaz) · açıklar: tırnak-cep hizası (pim + kamera) · −18 raf buzlanması · klape contaları · soğutma grubu ≤ 20 boy · v27: yayıcı plaka mı spiral süpürme mi · gramaj prototipi (123 cm³/dev) · PC çizilme · OVEN v4: kesme kuvveti pilotu (15–20 N/cm varsayım) · sadeyağ mı sıvı yağ mı · PC gövde + 42 °C yağ (pilot) · kuru bağlantı tipi · PACK'te boşalan 26 cm","#9a6b1f"),
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
tx(X0,Y0-94,"AUTOKITCH — HAT v51 · TÜM İSTASYONLAR (6 Eyl 2026) — STORE v4 · PRESS v8 · TOPPING v25 + v27 KAP · OVEN v5 (Omake 2 kat · 1 yağ kabı · sprey · KESME presi · kolon 70) · PACK v4 = KUTU AÇICI (yığın 84 = 525 · vakum · kalıp)",15,"start","bold")
tx(X0,Y0-72,"Robot: tek kol, 16–20 kg sınıfı (en ağır yük: kıyma 7,5 + kap 5,7 + çatal 2,0 = 15,2 kg — ⑦ açık) · uç değiştirici: TEPSİ eli (pide press'ten kutuya kadar tepside, fırına tepsiyle) + PENÇE (hamur · kutu · içecek) + ÇATAL (kap, forklift gibi önden). Mavi = tepsi Ø32 (pide Ø30). Kırmızı = KONTROL bulgusu.",10,"start","","#333")
tx(X0,Y0-54,"Ölçüler cm. HER KABİN 70/140 × 197 × 84 (gövde 185 + ayak 12; TOPPING, OVEN ve PACK'te ayak yerine plint 12). Açık: ⑤ Fersah Ø30 taban · ⑦ kol yükü 15,2 kg + menzil · ⑫ robot tepsi eli v2 (kulp 6) · ① STORE v5 onayı · TOPPING prototipleri (spiral 11, kaşar akışı, çatal-cep hizası) · OVEN: kesme pilotu · yağ tipi · kuru bağlantı · PACK v4: vantuz payı (pilot 40 cm) · blank kalıbı · flap kapanması",10,"start","","#333")

W=int(X0+px(T)+px(2200)); H=int(max(YT2+px(1990), _kbot+40))
svg=(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}"><rect width="{W}" height="{H}" fill="#ffffff"/>'+''.join(E)+'</svg>')
xml.dom.minidom.parseString(svg.encode('utf-8'))
OUT=r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\FULL_MAKINE\hat_on_gorunus_teknik_v51.svg"
io.open(OUT,'w',encoding='utf-8').write(svg)
print('yazildi + XML gecerli:',OUT,'|',W,'x',H)
