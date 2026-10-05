# -*- coding: utf-8 -*-
# TOPPING cikis geometrisi v2 — 70 dolap, tek kolon; kaset olculeri serbest (hacim sabit) → 3 optimum dizilis
import io, math
K = 4.0; K2 = 2.0
def px(c): return c*K
W, H = 1440, 1090
o = []
def ln(x1,y1,x2,y2,w=1,c='#111',d=None):
    o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%s"%s/>' % (x1,y1,x2,y2,c,w,(' stroke-dasharray="%s"'%d) if d else ''))
def rc(x,y,w,h,sw=1,r=0,c='#111',d=None,f='none',op=1):
    o.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%s" fill="%s" fill-opacity="%s" stroke="%s" stroke-width="%s"%s/>' % (x,y,w,h,r,f,op,c,sw,(' stroke-dasharray="%s"'%d) if d else ''))
def ci(x,y,r,sw=1,c='#111',d=None,f='none'):
    o.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" stroke="%s" stroke-width="%s"%s/>' % (x,y,r,f,c,sw,(' stroke-dasharray="%s"'%d) if d else ''))
def tx(x,y,s,fs=9,anc='start',fw='',col='#111'):
    o.append('<text x="%.1f" y="%.1f" font-size="%s" text-anchor="%s" font-weight="%s" fill="%s" font-family="Segoe UI, Arial, sans-serif">%s</text>' % (x,y,fs,anc,fw or 'normal',col,s))
def poly(pts,sw=1,c='#111',f='none',d=None):
    o.append('<polygon points="%s" fill="%s" stroke="%s" stroke-width="%s"%s/>' % (' '.join('%.1f,%.1f'%p for p in pts),f,c,sw,(' stroke-dasharray="%s"'%d) if d else ''))

GRN, RED, BLU, GRY, AMB = '#1d7a4f', '#c0392b', '#1a49b8', '#666', '#b7791f'
VK, VS, Vk = 36750.0, 18400.0, 8900.0      # cm3: kasar 15 kg / sucuk 10 kg / kavurma-kusbasi 3,5 kg
R_SW = 31

o.append('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">' % (W,H,W,H))
rc(0,0,W,H,0,0,'none',None,'#fff')
tx(30,42,'AUTOKITCH — TOPPING · ÇIKIŞ GEOMETRİSİ v2 (4 Eyl 2026) — 70 DOLAP · her çıkış kendi kasetinin altında · kaset ölçüleri serbest (hacim sabit) · 3 dizilim',15,'start','bold')
tx(30,66,'Kural: çıkış merkezi yan duvardan ≥ 31 → izinli bant x 31–39 (8 cm) · arka duvardan ≥ 31 · ön açık. Hacimler: kaşar 36,8 L (15 kg) · sucuk 18,4 L (10 kg) · kavurma / kuşbaşı 8,9 L (3,5 kg). Ölçüler cm, kaset = en × derinlik × yükseklik.',9.5,'start','','#444')
ln(30,78,W-30,78,.8,'#999')

def panel(X,Y,baslik,kasets,notlar,sonuc,sonuc_col,huni=None,tabla=False):
    # kasets: (ad, x0, y0, w, d, h, ox, oy, col)  — y0 arka duvardan
    rc(X,Y,px(70),px(84),2.2)
    tx(X+px(35),Y-26,baslik,10,'middle','bold')
    tx(X+px(35),Y-12,'ARKA duvar',7,'middle','',GRY)
    tx(X+px(35),Y+px(84)+13,'ÖN — açık (robot / tepsi kolu)',7.5,'middle','',GRY)
    rc(X+px(31),Y,px(8),px(84),0,0,'none',None,'#dff3e6')
    tx(X+px(35),Y+px(84)-4,'bant 8',6,'middle','bold',GRN)
    ymin = min(k[2] for k in kasets)
    rc(X,Y,px(70),px(ymin),0,0,'none',None,'#fbeaea'); tx(X+px(35),Y+px(ymin/2)+3,'arka pay %.1f (spiral ≥ 31)' % ymin,6.5,'middle','',RED)
    for ad,x0,y0,w,d,h,ox,oy,col in kasets:
        rc(X+px(x0),Y+px(y0),px(w),px(d),1.1,0,col,None,'#f1efe8')
        tx(X+px(x0+w/2),Y+px(y0+d/2)-1,ad,7.5,'middle','bold',col)
        tx(X+px(x0+w/2),Y+px(y0+d/2)+8,'%g×%g×%g' % (round(w,1),round(d,1),round(h,1)),6.3,'middle','',col)
        ci(X+px(ox),Y+px(oy),px(R_SW),1.1,GRN,'6,4')
        ci(X+px(ox),Y+px(oy),4,1.4,GRN,None,'#fff'); ci(X+px(ox),Y+px(oy),1.6,1,GRN,None,GRN)
    if huni:
        for (x1,y1),(x2,y2) in huni: ln(X+px(x1),Y+px(y1),X+px(x2),Y+px(y2),1,BLU,'3,2')
    ln(X,Y+px(84)+22,X+px(70),Y+px(84)+22,.8); tx(X+px(35),Y+px(84)+33,'70',8,'middle','bold')
    ln(X-14,Y,X-14,Y+px(84),.8); tx(X-18,Y+px(42),'84',8,'middle','bold')
    tx(X+px(35)+px(31)+3,Y+px(kasets[0][7])+3,'x 4–66 ✓',7,'start','bold',GRN)
    # ---- yan kesit (y–z) ----
    KY = Y+px(84)+56
    tx(X,KY-6,'YAN KESİT (derinlik × yükseklik, 1:2)',7.5,'start','bold',GRY)
    hmax = max(k[5] for k in kasets)
    zb = KY + 6 + K2*(hmax+21+14)         # zemin (bosluk tabani)
    zc = zb - K2*14                        # bosluk tavani = cark tabani
    zk = zc - K2*21                        # cark tavani = kaset tabani
    rc(X,zk,K2*84,K2*21,1,0,'#111',None,'#f7f7f7'); tx(X+K2*84+4,zk+K2*12,'çark 21',6.5,'start','',GRY)
    rc(X,zc,K2*84,K2*14,1,0,BLU,'4,3','#eef3ff'); tx(X+K2*84+4,zc+K2*9,'boşluk 14',6.5,'start','',BLU)
    ln(X,zb,X+K2*84+40,zb,1.2)
    ln(X,zk-K2*(hmax+2),X,zb,1.2)          # arka duvar
    if tabla: rc(X,zk-K2*1.5,K2*84,K2*1.5,.8,0,AMB,None,'#fbeed0'); tx(X+K2*84+4,zk-1,'tabla 1,5 (84 tam açılır)',6.5,'start','',AMB)
    for ad,x0,y0,w,d,h,ox,oy,col in kasets:
        top = zk - K2*(1.5 if tabla else 0)
        rc(X+K2*y0,top-K2*h,K2*d,K2*h,1,0,col,None,'#f1efe8')
        tx(X+K2*(y0+d/2),top-K2*h/2+3,ad[:3],6,'middle','bold',col)
        # huni + cark + cikis
        poly([(X+K2*(oy-d/2*0.9),zk),(X+K2*(oy+d/2*0.9),zk),(X+K2*(oy+3),zk+K2*9),(X+K2*(oy-3),zk+K2*9)],.8,'#111','#fff')
        ci(X+K2*oy,zk+K2*13,K2*5,.9,'#111'); ln(X+K2*oy,zk+K2*18,X+K2*oy,zc,1,'#111')
        ln(X+K2*oy,zc,X+K2*oy,zc+K2*6,1.2,GRN)
    tx(X+K2*84+4,zk-K2*hmax/2,'kaset %g' % hmax,6.5,'start','bold')
    # tepsi (en arkadaki cikisin altinda, en geri konum) + kulp
    oy0 = kasets[0][7]; tcy = oy0-14
    rc(X+K2*(tcy-17),zb-K2*3.5,K2*34,K2*1.5,1,BLU,None,'#dfe7fb'); rc(X+K2*(tcy+17),zb-K2*4.5,K2*12,K2*3,1,BLU,None,'#dfe7fb')
    tx(X+K2*(tcy+17),zb+9,'tepsi en geride (kulp %g)' % round(tcy+17+12,1),6,'middle','',BLU)
    # ---- notlar ----
    ny = zb+26
    tx(X-px(3),ny,sonuc,8,'start','bold',sonuc_col)
    for i,s in enumerate(notlar): tx(X-px(3),ny+13+i*11.5,s,7.2,'start','','#333')

def dizi(sira, gap=1.0):
    # sira: arkadan one (ad, w, d, h, col, ox) → y konumlari; ilk kasetin merkezi 31
    ks=[]; y = 31 - sira[0][2]/2
    for ad,w,d,h,col,ox in sira:
        ks.append((ad, 35-w/2 if ox is None else ox-w/2, y, w, d, h, 35 if ox is None else ox, y+d/2, col)); y += d+gap
    return ks, y-gap

# ---------- A1: arka arkaya, one KASAR ----------
dS = VS/(40*25); dk = Vk/(40*25); dK = VK/(60*30)
k1, end1 = dizi([('SUCUK',40,dS,25,'#111',None),('KUŞBAŞI',40,dk,25,'#111',None),('KAVURMA',40,dk,25,'#111',None),('KAŞAR A',60,dK,30,'#111',None)])
assert end1 <= 84, end1
panel(90,150,'A1 · ARKA ARKAYA, ÖNE KAŞAR (önerilen)',k1,
 ['sucuk 40×%.1f×25 · kuşbaşı / kavurma 40×%.1f×25 · kaşar 60×%.1f×30' % (dS,dk,dK),
  'kaşar önde → robot doğrudan değiştirir (3×/hafta) · küçükler 2×/hafta:',
  'kaşar çıkar (boş yuva) → küçük değiş → kaşar geri (4 hamle)',
  'sucuk haftalık: eleman öndekileri alır, arkayı değiştirir',
  'kaydırma gerekmedi: hepsi x 35 · kaset katı 30 (v11: 25) · geçiş rafı: kat 1 kaşar B-C-D'],
 'SONUÇ ✓ — derinlik %.1f / 84, pay %.1f' % (end1, 84-end1), GRN)

# ---------- A3: kaset tablasi, kasar arkada (max pay, hepsi 25) ----------
dK3 = VK/(60*25); dS3 = VS/(60*25); dk3 = Vk/(40*25)
k3, end3 = dizi([('KAŞAR A',60,dK3,25,'#111',None),('SUCUK',60,dS3,25,'#111',None),('KUŞBAŞI',40,dk3,25,'#111',None),('KAVURMA',40,dk3,25,'#111',None)])
assert end3 <= 84, end3
panel(560,150,'A3 · TABLA ÇEKMECESİ, KAŞAR ARKADA (max pay)',k3,
 ['kaşar 60×%.1f×25 · sucuk 60×%.1f×25 · küçükler 40×%.1f×25' % (dK3,dS3,dk3),
  'kasetler 84 tam açılan tablada → robot / eleman ÜSTTEN alır, sıra serbest',
  'derin kaşar arkada → arka pay %.1f (A1: %.1f) → toplam pay büyür' % (k3[0][2], k1[0][2]),
  'kaset tabanı sürgü kapaklı (zaten şart: dolu kaset taşınıyor)',
  'bedel: 1 çekmece rayı çifti + tabla · kaset katı 25 kalır'],
 'SONUÇ ✓ — derinlik %.1f / 84, pay %.1f' % (end3, 84-end3), GRN, tabla=True)

# ---------- A2: kucuk cift YAN YANA ayri cikis (Kemal'in sorusu) ----------
wS_ = 6.5; hS_ = 45; dp = Vk/(wS_*hS_)
dS2 = VS/(60*25); dK2 = VK/(60*30)
y0 = 31 - dp/2
k2 = [('KAV.',31.45-wS_/2,y0,wS_,dp,hS_,31.45,31,RED),('KUŞ.',38.55-wS_/2,y0,wS_,dp,hS_,38.55,31,RED)]
y = y0+dp+1; k2.append(('SUCUK',5,y,60,dS2,25,35,y+dS2/2,'#111')); y += dS2+1
k2.append(('KAŞAR A',5,y,60,dK2,30,35,y+dK2/2,'#111')); end2 = y+dK2
assert end2 <= 84, end2
panel(1030,150,'A2 · KÜÇÜK ÇİFT YAN YANA, AYRI ÇIKIŞ (soru)',k2,
 ['iki merkez de 8 cm bandın içinde → kaset ≤ 6,5 en → 6,5×%.1f×45 (dar-uzun)' % dp,
  'çıkışlar x 31,5 / 38,5 (kaydırma ±3,5) · sucuk 60×%.1f×25 · kaşar 60×%.1f×30' % (dS2,dK2),
  'MATEMATİK ✓ — MÜHENDİSLİK ✗: 6,5 cm yarıkta kavurma/kuşbaşı köprüler, tıkanır',
  'kaset katı 45 (+20) · küçükler en arkada → değişimi 2 kaset çıkarmayı ister',
  'yan yana ısrar edilirse en az 12 cm yarık lazım → bant 8 → sığmaz'],
 'SONUÇ ✓ geometri (pay %.1f) · ✗ önerilmez' % (84-end2), AMB)

# ---------- KARAR ----------
yk0 = 850
rc(30,yk0,W-60,H-yk0-30,1.6,4)
tx(48,yk0+24,'CEVAP ve KARAR',12,'start','bold')
rows = [
 ('Sorun: "küçük çift yan yana, ikisi de ayrı çıkış, biraz sağa-sola kayık olsa uyar mı?" → Yalnız iki merkez de 31–39 bandına girerse uyar; yan yana duran iki kutunun merkezleri en çok 8 cm ayrılabilir → her kutu ≤ 6,5 cm en. Dar-uzun (6,5×30×45) yapınca geometri kapanır ama malzeme yarıkta köprüler. Kaydırma bu yüzden işe yaramıyor.', '#333'),
 ('Çözüm kaydırma değil ARKA ARKAYA dizmek: kutular 40 en kalır, hepsi x 35, her çark kendi kasetinin tam altında, huni düz iner, boru yok. Kaset ölçüleri hacim sabit kalarak geniş-sığ yeniden kesildi (kaşar 60 en). Derinlik bütçesi: 31 − d_arka/2 + Σd + 3 ≤ 84.', '#333'),
 ('ÖNERİ A1 (öne kaşar): ek mekanizma yok, en sık değişen kaset robotun önünde, pay %.1f cm. Pay ve standart 25 yükseklik istenirse A3 (tabla çekmecesi, pay %.1f). A2 yalnız cevap için çizildi.' % (84-end1, 84-end3), BLU),
 ('Seçilen dizilim TOPPING v12'+chr(39)+'ye işlenir (kaset katı, çark hattı, geçiş rafı kat düzeni) → HAT v45. Açık: kaset taban sürgü kapağı, 60 cm kaset tutuşu (pençe), geçiş rafında 60 en kasetler arka arkaya (robot erişim derinliği 84).', GRY),
]
for i,(s,c) in enumerate(rows):
    tx(48,yk0+46+i*40,s[:170],8.5,'start','bold' if i==2 else '',c)
    if len(s)>170: tx(48,yk0+46+i*40+13,s[170:],8.5,'start','',c)
tx(W-40,H-36,'AUTOKITCH · arastirma/3_TOPPING/topping_cikis_geometri_v2 · 4 Eyl 2026',7,'end','',GRY)
o.append('</svg>')
out = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\3_TOPPING\topping_cikis_geometri_v2.svg"
io.open(out,'w',encoding='utf-8').write(chr(10).join(o))
print('yazildi | A1 %.1f (pay %.1f) · A3 %.1f (pay %.1f) · A2 %.1f (pay %.1f)' % (end1,84-end1,end3,84-end3,end2,84-end2))
