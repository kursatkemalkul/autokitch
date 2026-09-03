# -*- coding: utf-8 -*-
# v37 — KEMAL'IN EL KROKISINDEN PLAN: L istasyonlar + ortada robot + on cephe TEZGAH·KIOSK·QR
import io, math

S = 0.24
def px(mm): return mm*S
W, H = 1300, 1040
parts = []
def ln(x1,y1,x2,y2,w=2,c='#1a1a1a',dash=None):
    d = ' stroke-dasharray="%s"' % dash if dash else ''
    parts.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%.1f"%s/>' % (x1,y1,x2,y2,c,w,d))
def rc(x,y,w,h,sw=2,c='#1a1a1a',fill='none',dash=None):
    d = ' stroke-dasharray="%s"' % dash if dash else ''
    parts.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" stroke="%s" stroke-width="%.1f" fill="%s"%s/>' % (x,y,w,h,c,sw,fill,d))
def tx(x,y,s,size=14,c='#1a1a1a',w='normal',anchor='start'):
    parts.append('<text x="%.1f" y="%.1f" font-family="Arial" font-size="%.1f" fill="%s" font-weight="%s" text-anchor="%s">%s</text>' % (x,y,size,c,w,anchor,s))
def ci(cx,cy,r,sw=2,c='#1a1a1a',fill='none',dash=None):
    d = ' stroke-dasharray="%s"' % dash if dash else ''
    parts.append('<circle cx="%.1f" cy="%.1f" r="%.1f" stroke="%s" stroke-width="%.1f" fill="%s"%s/>' % (cx,cy,r,c,sw,fill,d))
def oy(x,y1,y2,label,side='r'):
    ln(x,y1,x,y2,1.2,'#b3452b'); ln(x-5,y1,x+5,y1,1.2,'#b3452b'); ln(x-5,y2,x+5,y2,1.2,'#b3452b')
    if side=='r': tx(x+8,(y1+y2)/2+4,label,12,'#b3452b','bold')
    else: tx(x-8,(y1+y2)/2+4,label,12,'#b3452b','bold','end')
def ox(y,x1,x2,label):
    ln(x1,y,x2,y,1.2,'#b3452b'); ln(x1,y-5,x1,y+5,1.2,'#b3452b'); ln(x2,y-5,x2,y+5,1.2,'#b3452b')
    tx((x1+x2)/2,y+15,label,12,'#b3452b','bold',anchor='middle')
def arrow(x1,y1,x2,y2,w=2,c='#1d7a4f',dash=None):
    ln(x1,y1,x2,y2,w,c,dash)
    a = math.atan2(y2-y1,x2-x1)
    for da in (2.6,-2.6):
        ln(x2,y2,x2-9*math.cos(a+da),y2-9*math.sin(a+da),w,c)
def num(cx,cy,n):
    ci(cx,cy,11,1.8,'#1d7a4f','#ffffff')
    tx(cx,cy+4.5,str(n),12.5,'#1d7a4f','bold','middle')

tx(30,36,'v37 — EL KROKİSİNDEN PLAN (üstten görünüş)',21,'#1a1a1a','bold')
tx(30,58,'L şeklinde istasyonlar + ortada robot; ÖN CEPHE (müşterinin gördüğü TEK yüz): tezgah → kiosk ekran → QR teslim dolabı (sağ altta). Mutfak tamamen kapalı.',11.5,'#666')
ln(30,70,W-30,70,1,'#999')

X0, Y0 = 80, 110
def PX(mmx): return X0+px(mmx)
def PY(mmy): return Y0+px(mmy)

# UST SIRA (sirt ust duvara): PRES 840-1540, DOZAJ 1540-2240, FIRIN 2240-2890, KESIM 2890-3590
ust = [(840,1540,'2 · PRES','70 · PZP-400 + çöp',2),(1540,2240,'3 · DOZAJ','70 · malzeme + sos hazneleri',3),(2240,2890,'4 · FIRIN','65 · çıkışta yağ spreyi',4),(2890,3590,'5 · KESİM + KUTU','70 · katlama düzeneği',5)]
for a,b,ad,alt,n in ust:
    rc(PX(a),PY(0),px(b-a),px(840),2.4)
    tx((PX(a)+PX(b))/2,PY(360),ad,12.5,'#1a1a1a','bold','middle')
    tx((PX(a)+PX(b))/2,PY(360)+15,alt,9.5,'#555','normal','middle')
    num((PX(a)+PX(b))/2,PY(660),n)

# SOL SIRA: SOGUK DEPO x0-840, y840-2940
rc(PX(0),PY(840),px(840),px(2100),2.4)
tx(PX(420),PY(1820),'1 · SOĞUK DEPO',13,'#1a1a1a','bold','middle')
tx(PX(420),PY(1820)+16,'210 (dik konum) — dolap + buzluk',9.5,'#555','normal','middle')
tx(PX(420),PY(1820)+31,'hamur + içecek + tatlı',9.5,'#555','normal','middle')
num(PX(420),PY(1050),1)

# KOSE (sol ust): teknik
rc(PX(0),PY(0),px(840),px(840),1.4,'#999',dash='6,4')
tx(PX(420),PY(390),'TEKNİK KÖŞE',10.5,'#999','bold','middle')
tx(PX(420),PY(390)+15,'pano · UPS · kompresör',9.5,'#999','normal','middle')

# ON CEPHE y2940-3490: TEZGAH 840-2000, KIOSK 2000-2600, QR 2600-3590
rc(PX(840),PY(2940),px(1160),px(550),2.4)
tx(PX(1420),PY(3230),'TEZGAH',12.5,'#1a1a1a','bold','middle')
tx(PX(1420),PY(3230)+15,'116 — müşteri karşılama',9.5,'#555','normal','middle')
rc(PX(2000),PY(2940),px(600),px(550),2.4)
tx(PX(2300),PY(3230),'KİOSK',12.5,'#1a1a1a','bold','middle')
tx(PX(2300),PY(3230)+15,'60 — ekran',9.5,'#555','normal','middle')
rc(PX(2600),PY(2940),px(990),px(550),2.4)
tx(PX(3095),PY(3210),'6 · QR TESLİM',12.5,'#1a1a1a','bold','middle')
tx(PX(3095),PY(3210)+15,'99 — 10-12 ısıtmalı göz',9.5,'#555','normal','middle')
tx(PX(3095),PY(3210)+30,'arkadan robot doldurur',9.5,'#555','normal','middle')
num(PX(3095),PY(3060),6)

# BAKIM KAPISI (sol alt hucre)
rc(PX(0),PY(2940),px(840),px(550),1.4,'#999',dash='6,4')
tx(PX(420),PY(3210),'BAKIM KAPISI',10.5,'#999','bold','middle')
tx(PX(420),PY(3210)+15,'iç koridora insan girişi (kilitli)',9.5,'#999','normal','middle')

# MUSTERI tarafi
arrow(PX(2200),PY(3490)+56,PX(2200),PY(3490)+16,2.2,'#2a6a9a')
tx(PX(2260),PY(3490)+44,'MÜŞTERİ — yalnız bu yüzü görür',11.5,'#2a6a9a','bold')

# ROBOT: kisa ray
ry_ = PY(1890)
rx0, rx1 = PX(1400), PX(2900)
ln(rx0,ry_,rx1,ry_,3.5,'#8a2be2')
ci((rx0+rx1)/2,ry_,9,2,'#8a2be2','#ffffff')
tx((rx0+rx1)/2,ry_-16,'ROBOT — kısa ray 150 (krokideki "robot ayağı")',11,'#8a2be2','bold','middle')
for cx_ in (rx0,rx1):
    ci(cx_,ry_,px(1300),1.2,'#8a2be2',dash='5,5')
tx((rx0+rx1)/2,ry_+30,'erişim R130 — tüm cepheler kapsanır',9.5,'#8a2be2','normal','middle')

# akis oklari
arrow(PX(760),PY(1400),PX(1120),PY(770),1.8,'#1d7a4f',dash='4,3')
arrow(PX(1260),PY(660),PX(1750),PY(660),1.8,'#1d7a4f',dash='4,3')
arrow(PX(2030),PY(660),PX(2430),PY(660),1.8,'#1d7a4f',dash='4,3')
arrow(PX(2700),PY(660),PX(3100),PY(660),1.8,'#1d7a4f',dash='4,3')
arrow(PX(3240),PY(770),PX(3095),PY(2900),1.8,'#1d7a4f',dash='4,3')

# olculer
ox(PY(0)-22,PX(840),PX(1540),'70'); ox(PY(0)-22,PX(1540),PX(2240),'70')
ox(PY(0)-22,PX(2240),PX(2890),'65'); ox(PY(0)-22,PX(2890),PX(3590),'70')
oy(PX(0)-34,PY(840),PY(2940),'210',side='l')
oy(PX(0)-34,PY(2940),PY(3490),'55',side='l')
ox(PY(3490)+70,PX(840),PX(2000),'116'); ox(PY(3490)+70,PX(2000),PX(2600),'60'); ox(PY(3490)+70,PX(2600),PX(3590),'99')
ox(PY(3490)+104,PX(0),PX(3590),'TOPLAM ≈ 359')
oy(PX(3590)+30,PY(0),PY(3490),'349')

# notlar (sag sutun)
NX = PX(3590)+80
tx(NX,PY(300),'ÖZET:',14,'#1a1a1a','bold')
notlar = [
 ('· Ayak izi ≈ 3,6 × 3,5 m ≈ 12,5 m²','#1a1a1a',12,'bold'),
 ('  (tezgah + kiosk + QR dahil —','#555',11,'normal'),
 ('  müşteri cephesi makineyle bütün)','#555',11,'normal'),
 ('· Kroki düzeni birebir: sağ altta','#1a1a1a',12,'normal'),
 ('  QR → solunda kiosk → solu tezgah','#1a1a1a',12,'normal'),
 ('· Mutfak KAPALI — cam yok;','#1a1a1a',12,'normal'),
 ('  müşteri yalnız ön yüzü görür','#1a1a1a',12,'normal'),
 ('· Stok: HAFTALIK (v31 iç düzenleri)','#1a1a1a',12,'normal'),
 ('· Servis istasyonu 70 ayrı duvarda','#555',11,'normal'),
 ('· Çöp pres kabininde · sprey fırın','#555',11,'normal'),
 ('  çıkışında (krokideki gibi)','#555',11,'normal'),
]
yy = PY(300)+26
for s,c,sz,w_ in notlar:
    tx(NX,yy,s,sz,c,w_)
    yy += 21

tx(W-30,H-14,'AUTOKITCH · hat_plan_kroki_v37',10.5,'#999','normal','end')

svg = '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d"><rect width="%d" height="%d" fill="#ffffff"/>%s</svg>' % (W,H,W,H,W,H,''.join(parts))
out = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\hat_plan_kroki_v37.svg"
io.open(out,'w',encoding='utf-8').write(svg)
print('ok', out)
