# -*- coding: utf-8 -*-
# TOPPING kaset FORMU arastirmasi v1 — kutu / kama / revolver (doner tabla, sektor) / tambur (dusey) — 70x84 dolap, cikis bandi x 31-39
import io, math
K = 4.0; K2 = 2.0
def px(c): return c*K
W, H = 1460, 1150
o = []
def ln(x1,y1,x2,y2,w=1,c='#111',d=None):
    o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%s"%s/>' % (x1,y1,x2,y2,c,w,(' stroke-dasharray="%s"'%d) if d else ''))
def rc(x,y,w,h,sw=1,r=0,c='#111',d=None,f='none',op=1):
    o.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%s" fill="%s" fill-opacity="%s" stroke="%s" stroke-width="%s"%s/>' % (x,y,w,h,r,f,op,c,sw,(' stroke-dasharray="%s"'%d) if d else ''))
def ci(x,y,r,sw=1,c='#111',d=None,f='none'):
    o.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" stroke="%s" stroke-width="%s"%s/>' % (x,y,r,f,c,sw,(' stroke-dasharray="%s"'%d) if d else ''))
def tx(x,y,s,fs=9,anc='start',fw='',col='#111'):
    o.append('<text x="%.1f" y="%.1f" font-size="%s" text-anchor="%s" font-weight="%s" fill="%s" font-family="Segoe UI, Arial, sans-serif">%s</text>' % (x,y,fs,anc,fw or 'normal',col,s))
def path(d,sw=1,c='#111',f='none',dash=None):
    o.append('<path d="%s" fill="%s" stroke="%s" stroke-width="%s"%s/>' % (d,f,c,sw,(' stroke-dasharray="%s"'%dash) if dash else ''))
def arr(x1,y1,x2,y2,c='#c0392b',w=1.2,both=False):
    ln(x1,y1,x2,y2,w,c); a=math.atan2(y2-y1,x2-x1)
    for s in (1,-1):
        ln(x2,y2,x2-6*math.cos(a-s*.45),y2-6*math.sin(a-s*.45),w,c)
        if both: ln(x1,y1,x1+6*math.cos(a-s*.45),y1+6*math.sin(a-s*.45),w,c)
def sector(cx,cy,r0,r1,a1,a2,sw=1,c='#111',f='#f1efe8'):
    p = lambda r,a: (cx+r*math.cos(math.radians(a)), cy+r*math.sin(math.radians(a)))
    x1,y1=p(r1,a1); x2,y2=p(r1,a2); x3,y3=p(r0,a2); x4,y4=p(r0,a1)
    la = 1 if (a2-a1)>180 else 0
    path('M%.1f,%.1f A%.1f,%.1f 0 %d 1 %.1f,%.1f L%.1f,%.1f A%.1f,%.1f 0 %d 0 %.1f,%.1f Z' % (x1,y1,r1,r1,la,x2,y2,x3,y3,r0,r0,la,x4,y4),sw,c,f)

GRN, RED, BLU, GRY, AMB = '#1d7a4f', '#c0392b', '#1a49b8', '#666', '#b7791f'
R_SW = 31

o.append('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">' % (W,H,W,H))
rc(0,0,W,H,0,0,'none',None,'#fff')
tx(30,42,'AUTOKITCH — TOPPING · KASET FORMU ARAŞTIRMASI v1 (4 Eyl 2026) — 70×84 dolap · "hangi form hem düzgün görünür, hem mantıklı yerleşir, hem çıkışı kendi altında tutar?" · 4 form',15,'start','bold')
tx(30,66,'Değişmez kural: çıkış (huni tepesi / çark) x 31–39 bandında, arka duvardan ≥ 31, ön açık. Yeni bilgi: geniş form = uzun huni eğimi = yükseklik (eğim 50°: 31 cm yatay → 37 cm düşü). Kaşar (rendelenmiş) her formda karıştırıcı ister — köprüler.',9.5,'start','','#444')
ln(30,78,W-30,78,.8,'#999')

def kabin(X,Y,baslik,etiket=True):
    rc(X,Y,px(70),px(84),2.2)
    tx(X+px(35),Y-26,baslik,10,'middle','bold')
    tx(X+px(35),Y-12,'ARKA duvar',7,'middle','',GRY)
    tx(X+px(35),Y+px(84)+13,'ÖN — açık (robot)',7.5,'middle','',GRY)
    if etiket:
        rc(X+px(31),Y,px(8),px(84),0,0,'none',None,'#dff3e6')
    ln(X,Y+px(84)+22,X+px(70),Y+px(84)+22,.8); tx(X+px(35),Y+px(84)+33,'70',8,'middle','bold')
    ln(X-14,Y,X-14,Y+px(84),.8); tx(X-18,Y+px(42),'84',8,'middle','bold')
def cikis(X,Y,cx,cy,col=GRN,sweep=True):
    if sweep: ci(X+px(cx),Y+px(cy),px(R_SW),1.1,col,'6,4')
    ci(X+px(cx),Y+px(cy),4,1.4,col,None,'#fff'); ci(X+px(cx),Y+px(cy),1.6,1,col,None,col)
def kutu(X,Y,x,y,w,d,ad,alt='',col='#111',f='#f1efe8'):
    rc(X+px(x),Y+px(y),px(w),px(d),1.1,0,col,None,f)
    tx(X+px(x+w/2),Y+px(y+d/2)-1,ad,7.5,'middle','bold',col)
    if alt: tx(X+px(x+w/2),Y+px(y+d/2)+8,alt,6.3,'middle','',col)
def notlar(X,y,sonuc,col,lines):
    tx(X-px(3),y,sonuc,8,'start','bold',col)
    for i,s in enumerate(lines): tx(X-px(3),y+13+i*11.5,s,7.2,'start','','#333')
def puan(X,y,vals):
    # vals: (cikis bandi, huni/yukseklik, yerlesim-degisim, gorunus) → '✓','~','✗'
    for i,(ad,v) in enumerate(zip(('çıkış bandı','huni / yükseklik','yerleşim · değişim','görünüş'),vals)):
        c = GRN if v=='✓' else (AMB if v=='~' else RED)
        rc(X+i*70,y-9,66,13,.8,2,c,None,'#fff'); tx(X+i*70+33,y+1,'%s %s' % (v,ad),6.3,'middle','bold',c)

# ---------- F1 KUTU KOLONU ----------
X,Y=100,150
kabin(X,Y,'F1 · KUTU KOLONU (arka arkaya, v2-A1)')
rc(X,Y,px(70),px(21.8),0,0,'none',None,'#fbeaea')
kutu(X,Y,15,21.8,40,18.4,'SUCUK','40×18×25'); kutu(X,Y,15,41.2,40,8.9,'KUŞBAŞI','40×9×25'); kutu(X,Y,15,51.1,40,8.9,'KAVURMA','40×9×25'); kutu(X,Y,5,61,60,20.4,'KAŞAR A','60×20×30')
for cy in (31,45.65,55.55,71.2): cikis(X,Y,35,cy,GRN,cy==31)
puan(X-px(3),Y+px(84)+56,('✓','✓','~','~'))
notlar(X,Y+px(84)+80,'SONUÇ ✓ çalışır — form nötr, "raf" görünümü',GRN,
 ['kompakt kutu → çark tam merkezde, huni kısa (en 40 → eğim 20 cm → 24 düşü) ✓',
  'yuvarlak kova kolonu aynı mantık ama 128 cm derinlik ister ✗ (daire yer yer)',
  'değişim: kaşar önde doğrudan; küçükler için kaşar çıkar-girer; sucuk eleman',
  'pay 2,6 · kaset katı 30 · ek mekanizma yok',
  'görünüş: dört kutu arka arkaya, üstten bakınca raf gibi — sıradan'])

# ---------- F2 KAMA 2x2 ----------
X,Y=470,150
kabin(X,Y,'F2 · KAMA / ASİMETRİK HUNİ (2×2 yan yana)')
kutu(X,Y,1,9,33,44.5,'KAŞAR A','33×44×h'); kutu(X,Y,36,30,33,22.3,'SUCUK','33×22×h')
kutu(X,Y,1,55,33,10.8,'KAVURMA','33×11×h'); kutu(X,Y,36,54,33,10.8,'KUŞBAŞI','33×11×h')
for (cx,cy) in ((32,31.2),(38,41.2),(32,60.4),(38,59.4)): cikis(X,Y,cx,cy,AMB,False)
ci(X+px(32),Y+px(31.2),px(R_SW),1.1,AMB,'6,4'); ci(X+px(38),Y+px(41.2),px(R_SW),1.1,AMB,'6,4')
# egim oklari (dis duvardan apex'e)
arr(X+px(2),Y+px(31.2),X+px(30),Y+px(31.2),RED,1.2); tx(X+px(16),Y+px(31.2)-4,'huni eğimi 31 →',6.3,'middle','bold',RED)
arr(X+px(68),Y+px(41.2),X+px(40),Y+px(41.2),RED,1.2)
tx(X+px(35),Y+px(78),'çıkışlar x 32 / 38 (kayık) — kutu kendi hunisi',6.5,'middle','',AMB)
puan(X-px(3),Y+px(84)+56,('✓','✗','✓','✓'))
notlar(X,Y+px(84)+80,'SONUÇ ~ geometri ✓, yerçekimi ✗ — ancak karıştırıcıyla',AMB,
 ['iki sıra, iki kolon; her kutunun tepesi iç kenarda (x 32 / 38) → banda girer ✓',
  'ama huni dış duvardan tepeye 31 cm yatay → 50° eğimle 37 cm düşü + depo → kaset ≥ 55 ✗',
  'düz tabanlı yapılırsa kutu içi kürek/karıştırıcı malzemeyi köşeye süpürür (4 kavrama)',
  'değişim: hepsi önden (sıra 2, kolon 2) ✓ · derinlik bol (pay 18)',
  'görünüş: simetrik 2×2, temiz ✓ — bedeli: her kasette hareketli parça'])

# ---------- F3 REVOLVER ----------
X,Y=840,150
kabin(X,Y,'F3 · REVOLVER — döner tabla, sektör kasetler')
cx,cy = X+px(35),Y+px(40)
ci(cx,cy,px(33.5),1.6,'#111',None,'#f7f7f7')
secs = [('KAŞAR A',22.5,157.5,'#111'),('SUCUK',157.5,247.5,'#111'),('KAVURMA',247.5,315,'#111'),('KUŞBAŞI',315,382.5,'#111')]
for ad,a1,a2,col in secs:
    sector(cx,cy,px(5),px(33),a1,a2,1.1,col)
    am = math.radians((a1+a2)/2)
    tx(cx+px(26)*math.cos(am),cy+px(26)*math.sin(am)+3,ad,7,'middle','bold')
    tx(cx+px(26)*math.cos(am),cy+px(26)*math.sin(am)+12,'%g°' % (a2-a1),6,'middle','',GRY)
    ax,ay = cx+px(20)*math.cos(am),cy+px(20)*math.sin(am)
    ci(ax,ay,3.5,1.2,BLU,None,'#fff'); ci(ax,ay,1.4,1,BLU,None,BLU)
ci(cx,cy,px(5),1,'#111',None,'#ddd'); ci(cx,cy,px(20),.8,BLU,'2,3')
tx(cx,cy+3,'eksen',5.5,'middle','',GRY)
cikis(X,Y,35,60,GRN,True); tx(X+px(35)+px(31)+3,Y+px(60)+3,'x 4–66 ✓',7,'start','bold',GRN)
tx(X+px(35),Y+px(66),'DOZAJ NOKTASI (35, 60) — hep aynı',6.5,'middle','bold',GRN)
# donus oku
path('M%.1f,%.1f A%.1f,%.1f 0 0 1 %.1f,%.1f' % (cx+px(36)*math.cos(math.radians(200)),cy+px(36)*math.sin(math.radians(200)),px(36),px(36),cx+px(36)*math.cos(math.radians(300)),cy+px(36)*math.sin(math.radians(300))),1.2,BLU)
tx(cx-px(30),cy-px(30),'tabla döner',6.5,'middle','',BLU)
arr(X+px(35),Y+px(74),X+px(35),Y+px(83),BLU,1.2); tx(X+px(50),Y+px(80),'boş sektör öne → çekilir',6.3,'start','',BLU)
puan(X-px(3),Y+px(84)+56,('✓','~','✓','✓'))
notlar(X,Y+px(84)+80,'SONUÇ ✓✓ — kaset çıkışa gider, çıkış kasete değil',GRN,
 ['Ø66 tabla, göbek Ø10, 4 sektör: kaşar 135° (37,6 L h30) · sucuk 90° (25 L) · küçükler 67,5° (18,8 L)',
  'her sektörün huni tepesi r 20 dairesinde → öne dönen sektörün tepesi hep (35, 60) → TEK dozaj noktası',
  'robot spirali her malzemede aynı yol ✓ · tek sabit çark motoru, sektöre kavrama → kasetler pasif',
  'boşalan sektör öne döner → tüm kasetler ÖNDEN değişir ✓ · kaşar 135°: karıştırıcı (huni 31)',
  'bedel: tabla motoru + rulman + 4 taban sürgüsü · dönüş ≤ 6 sn · görünüş: premium, "objektif"'])

# ---------- F4 TAMBUR ----------
X,Y=1210,150
kabin(X,Y,'F4 · TAMBUR — düşey paternoster',False)
rc(X+px(15),Y+px(8),px(40),px(68),1.2,0,'#111','5,3','#f1efe8'); tx(X+px(35),Y+px(20),'tambur izdüşümü 40×68',6.5,'middle','',GRY)
ln(X+px(15),Y+px(42),X+px(55),Y+px(42),.8,GRY,'2,2'); tx(X+px(57),Y+px(44),'eksen',6,'start','',GRY)
cikis(X,Y,35,42,GRN,True); tx(X+px(35),Y+px(50),'alt cep = dozaj (35, 42)',6.5,'middle','bold',GRN)
# kucuk yan gorunus (y-z) 1:2
KY = Y+px(84)+44
tx(X,KY-6,'YAN (1:2): Ø64 çark, 6 cep',6.5,'start','bold',GRY)
wc = (X+K2*42, KY+K2*38)
ci(wc[0],wc[1],K2*32,1.2,'#111','4,3')
for k in range(6):
    a = math.radians(90+k*60); px_,py_ = wc[0]+K2*24*math.cos(a), wc[1]+K2*24*math.sin(a)
    rc(px_-K2*8,py_-K2*6,K2*16,K2*12,.9,0,'#111',None,'#f1efe8')
ln(wc[0],wc[1]+K2*30,wc[0],wc[1]+K2*40,1.2,GRN)
tx(X+K2*84+4,wc[1],'yükseklik ~85',6.5,'start','bold',RED)
puan(X-px(3),KY+K2*80+10,('✓','✓','✓','✗'))
notlar(X,KY+K2*80+34,'SONUÇ ✗ şimdi değil — fikir olarak dursun',RED,
 ['kasetler düşey çarkta asılı, alt cep dozaj noktası → çıkış hep (35, 42) ✓, huni kısa ✓',
  '6 cep: 4 çalışan + 2 sıradaki → geçiş rafının işini yutar (kazanç)',
  'ama kaset katı 25 → ~85 (+60), 40 kg döner kütle asılı, kasetler cepten çıkarken devrilme',
  'görünüş: makine gibi (çamaşır kurutucu) — dolap dilinden çıkar'])

# ---------- KARAR ----------
yk0 = 905
rc(30,yk0,W-60,H-yk0-30,1.6,4)
tx(48,yk0+24,'GEOMETRİK SONUÇ ve ÖNERİ',12,'start','bold')
rows = [
 ('Form ne olursa olsun (kare, yuvarlak, üçgen, altıgen) huni tepesi banda girmek zorunda. Geniş bir kaset yaparsan tepesi kenara kayar ama huni eğimi uzar → yükseklik; kompakt kaset yaparsan huni kısa ama kasetler arka arkaya dizilir. Formun kendisi bu kuralı değiştirmez — yalnız KASETİ HAREKET ETTİREN form aşar.', '#333'),
 ('Bu yüzden sektör-revolver (F3) geometrik olarak en doğru form: her kasetin çıkışı kendi altında, dozaj noktası tek ve sabit (robot spirali hep aynı), boşalan kaset kendisi öne gelir (tek erişim noktası), kasetler pasif (tek çark motoru). Bedeli bir döner tabla.', GRN),
 ('Mekanizma istemiyorsan F1 kutu kolonu (v2-A1) çalışır ve sıradan görünür. F2 kama ancak her kasete karıştırıcı koyarsan; F4 tambur bugün değil.', '#333'),
 ('ÖNERİ: F3 REVOLVER → TOPPING v12: kaset katı = Ø66 döner tabla (h 30 + tabla 2), altında sabit çark + huni (35, 60), açık boşluk 14, geçiş rafı sektör yuvalı. Açık: kaşar sektörüne karıştırıcı, tabla motoru/rulman seçimi, sektör sürgü kapağı.', BLU),
]
for i,(s,c) in enumerate(rows):
    tx(48,yk0+46+i*42,s[:175],8.5,'start','bold' if i in (1,3) else '',c)
    if len(s)>175: tx(48,yk0+46+i*42+13,s[175:],8.5,'start','',c)
tx(W-40,H-36,'AUTOKITCH · arastirma/3_TOPPING/topping_kaset_form_v1 · 4 Eyl 2026',7,'end','',GRY)
o.append('</svg>')
out = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\3_TOPPING\topping_kaset_form_v1.svg"
io.open(out,'w',encoding='utf-8').write(chr(10).join(o))
print('yazildi', out)
