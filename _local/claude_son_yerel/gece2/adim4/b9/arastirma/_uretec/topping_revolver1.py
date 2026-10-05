# -*- coding: utf-8 -*-
# TOPPING REVOLVER v1 — 8 esit 45° dilim (kasar x4, sucuk x2, kavurma, kusbasi) · plan + kesit + dilim detayi + stok/degisim/motor
import io, math
K = 4.0; K2 = 2.0
def px(c): return c*K
W, H = 1460, 1160
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
def arr(x1,y1,x2,y2,c='#c0392b',w=1.2):
    ln(x1,y1,x2,y2,w,c); a=math.atan2(y2-y1,x2-x1)
    for s in (1,-1): ln(x2,y2,x2-6*math.cos(a-s*.45),y2-6*math.sin(a-s*.45),w,c)
def sector(cx,cy,r0,r1,a1,a2,sw=1,c='#111',f='#f1efe8'):
    p = lambda r,a: (cx+r*math.cos(math.radians(a)), cy+r*math.sin(math.radians(a)))
    x1,y1=p(r1,a1); x2,y2=p(r1,a2); x3,y3=p(r0,a2); x4,y4=p(r0,a1)
    path('M%.1f,%.1f A%.1f,%.1f 0 0 1 %.1f,%.1f L%.1f,%.1f A%.1f,%.1f 0 0 0 %.1f,%.1f Z' % (x1,y1,r1,r1,x2,y2,x3,y3,r0,r0,x4,y4),sw,c,f)
def poly(pts,sw=1,c='#111',f='none',d=None):
    o.append('<polygon points="%s" fill="%s" stroke="%s" stroke-width="%s"%s/>' % (' '.join('%.1f,%.1f'%p for p in pts),f,c,sw,(' stroke-dasharray="%s"'%d) if d else ''))

GRN, RED, BLU, GRY, AMB = '#1d7a4f', '#c0392b', '#1a49b8', '#666', '#b7791f'
R1, R0, RA, HD = 33.0, 5.0, 20.0, 28.0        # tabla yaricapi, gobek, huni tepesi yaricapi, dilim yuksekligi
A_DILIM = math.pi*(R1**2-R0**2)/8             # 418 cm2
V_DILIM = A_DILIM*HD/1000                     # 11,7 L
CHORD = 2*R1*math.sin(math.radians(22.5))     # 25,3
DEPTH = R1 - R0*math.cos(math.radians(22.5))  # 28,4

o.append('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">' % (W,H,W,H))
rc(0,0,W,H,0,0,'none',None,'#fff')
tx(30,42,'AUTOKITCH — TOPPING · REVOLVER v1 (4 Eyl 2026) — 8 EŞİT DİLİM 45° · kaşar ×4 · sucuk ×2 · kavurma · kuşbaşı — tek kaset tipi, her dilim önden değişir, tek dozaj noktası',15,'start','bold')
tx(30,66,'Kural 1: çıkış (35, 60) bantta, arka ≥ 31 ✓ · Kural 2: robot her dilimi başka dilimi oynatmadan alır (boşalan öne döner) ✓ · Kural 3: haftalık teslimat, robot gün içinde boşalınca ya da saat dolunca değiştirir ✓ · ölçüler cm',9.5,'start','','#444')
ln(30,78,W-30,78,.8,'#999')

# ================= PLAN =================
X,Y = 100,150
rc(X,Y,px(70),px(84),2.2); tx(X+px(35),Y-26,'PLAN — kaset katı (70×84)',10,'middle','bold')
tx(X+px(35),Y-12,'ARKA duvar',7,'middle','',GRY); tx(X+px(35),Y+px(84)+13,'ÖN — açık (robot)',7.5,'middle','',GRY)
rc(X+px(31),Y,px(8),px(84),0,0,'none',None,'#dff3e6')
cx,cy = X+px(35),Y+px(40)
ci(cx,cy,px(R1+0.5),1.6,'#111',None,'#f7f7f7')
names = ['KAŞAR 1','KUŞBAŞI','KAŞAR 2','SUCUK 1','KAŞAR 3','KAVURMA','KAŞAR 4','SUCUK 2']
for i,ad in enumerate(names):
    a1 = 67.5 + i*45; a2 = a1+45; am = math.radians(a1+22.5)
    sector(cx,cy,px(R0),px(R1),a1,a2,1.1,'#111','#f1efe8' if 'KAŞAR' in ad else '#e8eef8')
    tx(cx+px(25)*math.cos(am),cy+px(25)*math.sin(am)+3,ad,6.3,'middle','bold')
    ax,ay = cx+px(RA)*math.cos(am),cy+px(RA)*math.sin(am)
    ci(ax,ay,3,1.1,BLU,None,'#fff'); ci(ax,ay,1.2,1,BLU,None,BLU)
ci(cx,cy,px(R0),1,'#111',None,'#ddd'); ci(cx,cy,px(RA),.8,BLU,'2,3'); tx(cx,cy+3,'göbek',5.5,'middle','',GRY)
ci(X+px(35),Y+px(60),px(31),1.1,GRN,'6,4'); ci(X+px(35),Y+px(60),4.5,1.6,GRN,None,'#fff'); ci(X+px(35),Y+px(60),1.8,1,GRN,None,GRN)
tx(X+px(35)+px(31)+3,Y+px(60)+3,'x 4–66 ✓',7,'start','bold',GRN)
tx(X+px(35),Y+px(69),'DOZAJ + DEĞİŞİM (35, 60)',6.5,'middle','bold',GRN)
path('M%.1f,%.1f A%.1f,%.1f 0 0 1 %.1f,%.1f' % (cx+px(36)*math.cos(math.radians(195)),cy+px(36)*math.sin(math.radians(195)),px(36),px(36),cx+px(36)*math.cos(math.radians(300)),cy+px(36)*math.sin(math.radians(300))),1.2,BLU)
tx(cx-px(26),cy-px(33),'45° adım 1,5 sn',6.3,'middle','',BLU)
arr(X+px(35),Y+px(74),X+px(35),Y+px(83),BLU,1.2); tx(X+px(52),Y+px(80),'dilim öne çekilir',6.3,'start','',BLU)
ln(X,Y+px(84)+22,X+px(70),Y+px(84)+22,.8); tx(X+px(35),Y+px(84)+33,'70',8,'middle','bold')
ln(X-14,Y,X-14,Y+px(84),.8); tx(X-18,Y+px(42),'84',8,'middle','bold')
ln(cx-px(R1),Y+px(4),cx+px(R1),Y+px(4),.8); tx(cx,Y+px(3),'Ø66',6.5,'middle','bold')
ln(cx,cy,cx+px(RA)*math.cos(math.radians(-30)),cy+px(RA)*math.sin(math.radians(-30)),.8,BLU); tx(cx+px(12),cy-px(8),'r 20',6,'start','bold',BLU)
ny = Y+px(84)+56
for i,s in enumerate(['eksen (35, 40) · tabla Ø66 · göbek Ø10 · 8 × 45°',
                      'huni tepeleri r 20 dairesinde → öne dönen dilimin tepesi hep (35, 60)',
                      'kaşar dilimleri 90° aralıkla → en çok 45° dönüşle kaşar önde',
                      'tabla yalnız değişim ve malzeme seçiminde döner; kaşarlı pidede çoğu kez durur']):
    tx(X-px(3),ny+i*11.5,s,7.2,'start','','#333')

# ================= KESİT (y–z, x=35) =================
XS,YS = 470,150
tx(XS+K2*42,YS-26,'KESİT — dolap boyu (1:2)',10,'middle','bold'); tx(XS+K2*42,YS-12,'arka ← y → ön',7,'middle','',GRY)
z = lambda c: YS + K2*c
rc(XS,z(0),K2*84,K2*197,1.6)
rc(XS,z(0),K2*84,K2*27,1,0,'#111',None,'#f3f3f3'); tx(XS+K2*42,z(15),'TEKNİK 27 (soğutma 15 + elektrik 12)',6.5,'middle','bold')
rc(XS,z(27),K2*84,K2*3,.8,0,'#111',None,'#ccc')
# kaset kati 30-63: dilimler 33-61, tabla 61-63
rc(XS+K2*7,z(33),K2*28,K2*HD,1.1,0,'#111',None,'#f1efe8'); tx(XS+K2*21,z(48),'arka dilim',6,'middle','bold')
rc(XS+K2*45,z(33),K2*28,K2*HD,1.1,0,'#111',None,'#dff3e6'); tx(XS+K2*59,z(46),'ön dilim',6,'middle','bold',GRN); tx(XS+K2*59,z(52),'(dozajda)',5.5,'middle','',GRN)
rc(XS+K2*35,z(33),K2*10,K2*HD,.8,0,'#111',None,'#ddd'); tx(XS+K2*40,z(48),'göbek',5,'middle','',GRY)
rc(XS+K2*7,z(61),K2*66,K2*2,1,0,'#111',None,'#bbb'); tx(XS+K2*84+4,z(63),'tabla 2 (paslanmaz)',6,'start','',GRY)
tx(XS+K2*84+4,z(47),'dilim %g' % HD,6.5,'start','bold')
# huni tepesi + surgu (on dilim y 60)
poly([(XS+K2*52,z(58)),(XS+K2*68,z(58)),(XS+K2*63,z(61)),(XS+K2*57,z(61))],.8,BLU,'#fff'); tx(XS+K2*60,z(57),'taban eğimi 15° + kürek',5,'middle','',BLU)
# cark kati 63-84
rc(XS,z(63),K2*84,K2*21,.8,0,'#111',None,'#fafafa'); tx(XS+K2*84+4,z(74),'çark katı 21',6.5,'start','',GRY)
rc(XS+K2*25,z(63),K2*30,K2*3,.8,0,'#111',None,'#ddd'); tx(XS+K2*40,z(72),'bilyalı ring Ø30',5.5,'middle','',GRY)
rc(XS+K2*34,z(67),K2*12,K2*15,.9,0,'#111',None,'#eee'); tx(XS+K2*40,z(78),'tabla motoru',5,'middle','bold'); tx(XS+K2*40,z(82),'24 V 60 W',5,'middle','')
rc(XS+K2*57,z(63),K2*6,K2*3,.8,0,BLU,None,'#dfe7fb'); tx(XS+K2*72,z(66),'kavrama',5,'start','',BLU)
ci(XS+K2*60,z(72),K2*5,1,BLU,None,'#fff'); tx(XS+K2*72,z(74),'çark Ø10 (sabit motor)',5,'start','',BLU)
poly([(XS+K2*56,z(77)),(XS+K2*64,z(77)),(XS+K2*61.5,z(84)),(XS+K2*58.5,z(84))],.8,BLU,'#fff'); tx(XS+K2*72,z(81),'huni → çıkış (35, 60)',5,'start','',BLU)
# bosluk 84-98
rc(XS,z(84),K2*84,K2*14,1,0,BLU,'4,3','#eef3ff'); tx(XS+K2*84+4,z(92),'boşluk 14',6.5,'start','',BLU)
ln(XS+K2*60,z(84),XS+K2*60,z(90),1.4,GRN)
rc(XS+K2*29,z(94.5),K2*34,K2*1.5,1,BLU,None,'#dfe7fb'); rc(XS+K2*63,z(93.5),K2*12,K2*3,1,BLU,None,'#dfe7fb')
tx(XS+K2*46,z(93),'tepsi en geride (merkez y 46)',5,'middle','',BLU)
rc(XS+K2*57,z(94.5),K2*34,K2*1.5,.8,BLU,'2,2','none'); tx(XS+K2*74,z(100.5),'en önde (y 74, 7 taşar)',5,'start','',BLU)
# gecis rafi 98-197: 3 kat x 33
for k in range(3):
    zt = 98 + k*33
    ln(XS,z(zt),XS+K2*84,z(zt),.8)
    for (yy,lab,fill) in ((8,'arka yuva','#f7f6f2'),(44,'ön yuva','#f1efe8')):
        rc(XS+K2*yy,z(zt+3),K2*28,K2*HD,.9,0,'#111' if fill=='#f1efe8' else '#888',None if fill=='#f1efe8' else '3,2',fill)
        tx(XS+K2*(yy+14),z(zt+18),lab,5.5,'middle','',GRY)
    tx(XS+K2*84+4,z(zt+18),'geçiş rafı kat %d · 33' % (k+1),6.5,'start','',GRY)
ln(XS+K2*84,z(0),XS+K2*84,z(197),2)
tx(XS+K2*84+4,z(6),'z 0',5.5,'start','',GRY); tx(XS+K2*84+4,z(196),'197',6,'start','bold')
tx(XS+K2*84+4,z(150),'her kat 2 yan yana × 2 derin = 4 yuva',6,'start','','#333'); tx(XS+K2*84+4,z(156),'önden FIFO (arka öne düşer)',6,'start','','#333')
tx(XS+K2*84+4,z(30),'dikey: 27+3+33+21+14+99 = 197 ✓',6,'start','bold',GRN)

# ================= DİLİM DETAYI =================
XD,YD = 880,150
tx(XD+60,YD-26,'DİLİM (tek tip) — plan + yan',10,'middle','bold')
dc = (XD+65, YD+px(2))   # sanal eksen (ustte), dilim asagi bakar
sector(dc[0],dc[1],px(R0),px(R1),67.5,112.5,1.3,'#111','#f1efe8')
am = math.radians(90); ax,ay = dc[0]+px(RA)*math.cos(am),dc[1]+px(RA)*math.sin(am)
ci(ax,ay,4,1.3,BLU,None,'#fff'); ci(ax,ay,1.5,1,BLU,None,BLU); tx(ax+8,ay+3,'huni tepesi r 20',6,'start','bold',BLU)
rc(dc[0]-px(6),dc[1]+px(R1)-2,px(12),px(2.5),1,1,'#111',None,'#bbb'); tx(dc[0],dc[1]+px(R1)+px(5.5),'tutamak (pençe)',6,'middle','',GRY)
ln(dc[0]-px(CHORD/2),dc[1]+px(R1)+px(8),dc[0]+px(CHORD/2),dc[1]+px(R1)+px(8),.8); tx(dc[0],dc[1]+px(R1)+px(11),'dış kiriş %.1f' % CHORD,6.5,'middle','bold')
ln(dc[0]+px(CHORD/2)+10,dc[1]+px(R0*math.cos(math.radians(22.5))),dc[0]+px(CHORD/2)+10,dc[1]+px(R1),.8); tx(dc[0]+px(CHORD/2)+14,dc[1]+px(18),'%.1f' % DEPTH,6.5,'start','bold')
tx(dc[0],dc[1]+px(9),'45°',6.5,'middle','bold')
# yan gorunus
ys = dc[1]+px(R1)+px(16)
rc(dc[0]-px(14),ys,px(28),px(HD),1.2,0,'#111',None,'#f1efe8')
ln(dc[0]-px(14),ys+px(HD)-px(4),dc[0]+px(1),ys+px(HD),.9,BLU); ln(dc[0]+px(14),ys+px(HD)-px(4),dc[0]+px(1),ys+px(HD),.9,BLU)
rc(dc[0]-px(3),ys+px(HD)-3,px(6),4,.9,0,BLU,None,'#dfe7fb'); tx(dc[0],ys+px(HD)+12,'taban sürgüsü 6 (kam açar)',6,'middle','',BLU)
ln(dc[0]-px(9),ys+px(6),dc[0]+px(9),ys+px(6),.9,'#111'); ci(dc[0],ys+px(6),3,.9); tx(dc[0]+px(10),ys+px(7),'kürek mili',5.5,'start','',GRY)
tx(dc[0]-px(17),ys+px(HD/2)+3,'%g' % HD,6.5,'end','bold')
rc(dc[0]+px(14),ys+px(2),px(1.5),px(4),.8,0,'#111',None,'#bbb'); tx(dc[0]+px(17),ys+px(5),'tutamak',5.5,'start','',GRY)
tx(dc[0],ys-4,'yan (ön yüzden)',6,'middle','',GRY)
ny = ys+px(HD)+30
for i,s in enumerate(['alan %.0f cm² · hacim %.1f L (eğim payı düşülmüş ~11 L)' % (A_DILIM, V_DILIM),
                      'kaşar 4,8 kg · sucuk 5 kg · kavurma / kuşbaşı 3,5 kg → dolu ≤ 6 kg',
                      'boş 1,2 kg (1,5 mm paslanmaz) → robot yükü 12 kg sorunu kapandı',
                      'STORE −18 kaset çekmecesi 29 ≥ 28 ✓ (donmuş kavurma/kuşbaşı dilimi)',
                      'kaşar dilimine kürek (çark kavramasından dişliyle) — köprüleme',
                      'kaset kimliği: RFID/etiket → robot dilimi tanır, saat kuralını tutar']):
    tx(XD-8,ny+i*11.5,s,7.2,'start','','#333')

# ================= STOK · DEĞİŞİM · MOTOR =================
XT,YT = 1120,150
tx(XT,YT-26,'STOK · DEĞİŞİM · MOTOR',10,'start','bold')
kasar_hafta = 6.5*7/4.8
rows = [
 ('TABLA (8 dilim)','bold','#111'),
 ('kaşar ×4 = 19 kg ≈ 3 gün · sucuk ×2 = 10 kg = hafta','', '#333'),
 ('kavurma ×1 · kuşbaşı ×1 = 3,5 kg (3 gün taze)','', '#333'),
 ('HAFTALIK (eleman 1×)','bold','#111'),
 ('kaşar 6,5 kg/gün → 45,5 kg → %.1f → 10 dilim + 1 = 11' % kasar_hafta,'', '#333'),
 ('  → 4 tablada + 7 geçiş rafında','', '#333'),
 ('sucuk 2 (tablada) · kavurma 1 taze + 2 donmuş (STORE)','', '#333'),
 ('kuşbaşı 1 taze + 2 donmuş (STORE) · boş dilim 4','', '#333'),
 ('GEÇİŞ RAFI 12 yuva','bold','#111'),
 ('7 kaşar + 5 boş yuva (boşalan dilim buraya, sayı sabit)','', '#333'),
 ('kat 1: kaşar 5-6 / 7-8 · kat 2: kaşar 9-10-11 + boş · kat 3: boş ×4','', '#333'),
 ('DEĞİŞİM TETİĞİ','bold','#111'),
 ('① dozaj noktasında tartı hücresi → dilim boş','', '#333'),
 ('② saat kuralı doldu (kaşar 2,3 g · küçük 3 g · sucuk 7 g)','', '#333'),
 ('③ kuyruk boşken yap; doluysa ≤ 30 dk ertele (yedek dilim tablada)','', '#333'),
 ('5 hamle ~75 sn · günde ~1,5 değişim (kaşar 1,3 + diğer 0,2)','', '#333'),
 ('MOTOR','bold','#111'),
 ('dönen kütle: ürün 38 + dilim 10 + tabla 5 = ~55 kg','', '#333'),
 ('atalet ~3,5 kg·m² → 0,5 sn ivme + sürtünme ≈ 6 N·m','', '#333'),
 ('24 V 60 W redüktörlü + Ø30 bilyalı ring · 45° 1,5 sn · 180° 6 sn','', '#333'),
 ('dozaj çarkı: 1 sabit motor (35, 60), dilime kavrama · dilimler pasif','', '#333'),
 ('zaman: 2 malzemeli pidede ≤ 1 dönüş → bütçe 103 sn içinde %3','', GRN),
]
for i,(s,fw,c) in enumerate(rows):
    tx(XT,YT+i*15,s,7.3 if fw else 6.9,'start',fw,c)

# ================= KARAR =================
yk0 = 930
rc(30,yk0,W-60,H-yk0-30,1.6,4)
tx(48,yk0+24,'KARAR — Kemal'+chr(39)+'in iki önerisi arasında',12,'start','bold')
rows = [
 ('② İki sıra (kaşar üstte büyük, altta diğerleri yan yana): altta yan yana üç kaset → yalnız ortadaki 31–39 bandına girer, sol ve sağ pide erişemez (senin de gördüğün gibi). Üstteki kaşarın düşey hunisi de tam ortadan iner, alttaki orta kaseti keser. Alttakileri arka arkaya dizersen erişim kuralı bozulur. → ✗', RED),
 ('① Revolver + kaşarı bölmek: 8 eşit dilim tam oturuyor — kaşar ×4, sucuk ×2, kavurma, kuşbaşı = 360°. Tek kaset tipi, dolu ≤ 6 kg (robot yükü sorunu bitti), her dilim önden değişir, tek dozaj noktası, kaşarlı pidede tabla çoğu kez durur. Boş yer: 8 yuva dolu; 4 kaşar zaten 3 gün → daha fazla kaşara gerek yok. → ✓ KARAR', GRN),
 ('Sonraki adım: TOPPING v12 bu düzenle (teknik 27 · kaset katı 33 · çark 21 · boşluk 14 · geçiş rafı 3×33 = 197) çizilir → HAT v45. STORE v4 kaset çekmecesi dilimi alıyor (29 ≥ 28), değişiklik yok. Açık: tabla motoru/ring seçimi, kürek kavraması, dilim RFID.', BLU),
]
for i,(s,c) in enumerate(rows):
    tx(48,yk0+46+i*44,s[:175],8.5,'start','bold' if i==1 else '',c)
    if len(s)>175: tx(48,yk0+46+i*44+13,s[175:],8.5,'start','',c)
tx(W-40,H-36,'AUTOKITCH · arastirma/3_TOPPING/topping_revolver_v1 · 4 Eyl 2026',7,'end','',GRY)
o.append('</svg>')
out = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\3_TOPPING\topping_revolver_v1.svg"
io.open(out,'w',encoding='utf-8').write(chr(10).join(o))
print('yazildi | dilim alan %.0f cm2, hacim %.1f L, kiris %.1f, derinlik %.1f, kasar/hafta %.1f dilim' % (A_DILIM,V_DILIM,CHORD,DEPTH,kasar_hafta))
