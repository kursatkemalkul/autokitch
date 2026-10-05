# -*- coding: utf-8 -*-
# TOPPING cikis geometrisi v1 — "her cikis kendi kasetinin merkezinde" mumkun mu? (plan gorunus, kaset kati)
# Kural: tepsi R=17, spiral yaricapi 14 (pide ic O32 → topping O28) → cikis merkezi etrafinda R=31 temiz daire gerekir
import io, math
K = 4.0                      # px / cm
def px(c): return c*K
W, H = 1440, 1070
o = []
def ln(x1,y1,x2,y2,w=1,c='#111',d=None):
    o.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%s"%s/>' % (x1,y1,x2,y2,c,w,(' stroke-dasharray="%s"'%d) if d else ''))
def rc(x,y,w,h,sw=1,r=0,c='#111',d=None,f='none',op=1):
    o.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%s" fill="%s" fill-opacity="%s" stroke="%s" stroke-width="%s"%s/>' % (x,y,w,h,r,f,op,c,sw,(' stroke-dasharray="%s"'%d) if d else ''))
def ci(x,y,r,sw=1,c='#111',d=None,f='none'):
    o.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" stroke="%s" stroke-width="%s"%s/>' % (x,y,r,f,c,sw,(' stroke-dasharray="%s"'%d) if d else ''))
def tx(x,y,s,fs=9,anc='start',fw='',col='#111'):
    o.append('<text x="%.1f" y="%.1f" font-size="%s" text-anchor="%s" font-weight="%s" fill="%s" font-family="Segoe UI, Arial, sans-serif">%s</text>' % (x,y,fs,anc,fw or 'normal',col,s))
def arr(x1,y1,x2,y2,c='#c0392b',w=1.2):
    ln(x1,y1,x2,y2,w,c); a=math.atan2(y2-y1,x2-x1)
    for s in (1,-1):
        ln(x2,y2,x2-6*math.cos(a-s*.45),y2-6*math.sin(a-s*.45),w,c)
        ln(x1,y1,x1+6*math.cos(a-s*.45),y1+6*math.sin(a-s*.45),w,c)

GRN, RED, BLU, GRY = '#1d7a4f', '#c0392b', '#1a49b8', '#666'
R_TEPSI, R_SPIRAL = 17, 14
R_SWEEP = R_TEPSI + R_SPIRAL          # 31

o.append('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">' % (W,H,W,H))
rc(0,0,W,H,0,0,'none',None,'#fff')
tx(30,42,'AUTOKITCH — TOPPING · ÇIKIŞ GEOMETRİSİ v1 (4 Eyl 2026) — "her çıkış kendi kasetinin merkezinde" mümkün mü? · plan görünüş, kaset katı · ölçüler cm',15,'start','bold')
tx(30,66,'Kural: tepsi Ø34 (R 17) + spiral yarıçapı 14 (pide iç Ø32 → topping Ø28, 2 cm kenar) → her çıkış merkezi etrafında R = 17 + 14 = 31 cm TEMİZ DAİRE gerekir · yan duvar ≥ 31 · arka duvar ≥ 31 · ön açık (robot tarafı)',9.5,'start','','#444')
ln(30,78,W-30,78,.8,'#999')

def kabin(X,Y,wc,dc,ad):
    rc(X,Y,px(wc),px(dc),2.2)
    tx(X+px(wc)/2,Y-8,ad,10,'middle','bold')
    tx(X+px(wc)/2,Y+px(dc)+14,'ÖN — açık (robot / tepsi kolu)',7.5,'middle','',GRY)
    tx(X+px(wc)/2,Y-22,'ARKA duvar',7,'middle','',GRY)
    ln(X,Y+px(dc)+22,X+px(wc),Y+px(dc)+22,.8); tx(X+px(wc)/2,Y+px(dc)+33,'%g' % wc,8,'middle','bold')
    ln(X-14,Y,X-14,Y+px(dc),.8); tx(X-18,Y+px(dc)/2,'%g' % dc,8,'end','bold')

def kaset(X,Y,x,y,w,d,ad,alt='',col='#111',f='#f1efe8',dash=None):
    rc(X+px(x),Y+px(y),px(w),px(d),1.1,0,col,dash,f)
    tx(X+px(x+w/2),Y+px(y+d/2)-2,ad,7.5,'middle','bold',col)
    if alt: tx(X+px(x+w/2),Y+px(y+d/2)+9,alt,6.5,'middle','',col)

def cikis(X,Y,cx,cy,ok,lab='',orbit=False,tepsi=None):
    px_,py_=X+px(cx),Y+px(cy)
    col = GRN if ok else RED
    ci(px_,py_,px(R_SWEEP),1.3,col,'6,4')
    if orbit: ci(px_,py_,px(R_SPIRAL),.9,BLU,'2,3')
    ci(px_,py_,4,1.4,col,None,'#fff'); ci(px_,py_,1.6,1,col,None,col)
    if tepsi:
        tcx,tcy=X+px(tepsi[0]),Y+px(tepsi[1]); ci(tcx,tcy,px(R_TEPSI),1.2,BLU,'5,3'); ci(tcx,tcy,3,1,BLU,None,BLU)
    if lab: tx(px_,py_+px(R_SWEEP)+11,lab,7,'middle','bold',col)

# ---------- Panel 1: 70 dolap, kasetler yan yana (v11 kaset kati), cikis kendi merkezinde ----------
X1,Y1=110,150
kabin(X1,Y1,70,84,'① 70 DOLAP · kasetler YAN YANA (v11 katı) · çıkış kendi merkezinde')
rc(X1+px(31),Y1,px(8),px(84),0,0,'none',None,'#dff3e6')
tx(X1+px(35),Y1+px(10),'izinli',6.5,'middle','bold',GRN); tx(X1+px(35),Y1+px(14),'bant 8',6.5,'middle','bold',GRN)
# arka sira (yedek)
kaset(X1,Y1,0,0,35,42,'KAŞAR B','yedek','#888','#f7f6f2','3,2')
kaset(X1,Y1,35,0,17,21,'kav.','yedek','#888','#f7f6f2','3,2'); kaset(X1,Y1,52,0,17,21,'kuş.','yedek','#888','#f7f6f2','3,2')
kaset(X1,Y1,35,21,35,21,'SUCUK yedek','','#888','#f7f6f2','3,2')
# on sira (calisan)
kaset(X1,Y1,0,42,35,42,'KAŞAR A','35×42')
kaset(X1,Y1,35,42,17,21,'KAV.','17×21'); kaset(X1,Y1,52,42,17,21,'KUŞ.','17×21')
kaset(X1,Y1,35,63,35,21,'SUCUK','35×21')
# cikislar + sweep daireleri
cikis(X1,Y1,17.5,63,False,'',True,(3.5,63))
cikis(X1,Y1,52.5,73.5,False)
cikis(X1,Y1,43.5,52.5,False); cikis(X1,Y1,60.5,52.5,False)
# tasma oklari
arr(X1-px(13.5),Y1+px(63)-px(31)-6,X1,Y1+px(63)-px(31)-6); tx(X1-px(7),Y1+px(63)-px(31)-10,'13,5 ✗',7,'middle','bold',RED)
arr(X1+px(70),Y1+px(73.5)+px(31)+6,X1+px(83.5),Y1+px(73.5)+px(31)+6); tx(X1+px(77),Y1+px(73.5)+px(31)+18,'13,5 ✗',7,'middle','bold',RED)
arr(X1+px(70),Y1+px(52.5)-px(31)-6,X1+px(91.5),Y1+px(52.5)-px(31)-6); tx(X1+px(81),Y1+px(52.5)-px(31)-10,'21,5 ✗',7,'middle','bold',RED)
tx(X1+px(3.5),Y1+px(63)-px(17)-5,'tepsi en solda',6.5,'middle','',BLU)
tx(X1+px(17.5)+px(14)+2,Y1+px(63)+3,'r14',6.5,'start','',BLU)
# panel notu
yy=Y1+px(105)+34
for i,s in enumerate(['SONUÇ ✗ — 4 çıkışın 4'+chr(39)+'ü de yan duvarı aşıyor:',
                      'kaşar merkezi x 17,5 → tepsi x −13,5'+chr(39)+'e çıkmalı (sol duvar 13,5 aşılır)',
                      'sucuk x 52,5 → sağ duvar 13,5 aşılır · kuşbaşı x 60,5 → 21,5 aşılır',
                      'kural: çıkış x ∈ [31, 39] → 70 dolapta yalnız 8 cm'+chr(39)+'lik orta bant',
                      'yan yana iki kasetin merkezi 31'+chr(39)+'den uzağa gelmez → geometrik olarak İMKÂNSIZ']):
    tx(X1-px(14),yy+i*12,s,7.5,'start','bold' if i==0 else '',RED if i in (0,4) else '#333')

# ---------- Panel 2: 70 dolap, TEK KOLON ----------
X2,Y2=500,150
kabin(X2,Y2,70,84,'② SEÇENEK A · 70 DOLAP · TEK KOLON (her kaset x = 35'+chr(39)+'te)')
# olcu: kasar 45x32.7 (36,75 L), sucuk 45x16.3 (18,4 L), kucuk cift 21x17 x2 (Y-huni)
dK, dS, dk = 36.75e3/(45*25), 18.4e3/(45*25), 17.0     # 32.7 / 16.35 / 17
y0 = 31 - dK/2                                        # 14.65
yS = y0 + dK + 1; yk = yS + dS + 1; yend = yk + dk
assert yend <= 84, yend
rc(X2,Y2,px(70),px(y0),0,0,'none',None,'#fbeaea'); tx(X2+px(35),Y2+px(y0/2)+3,'ölü bölge %.1f — spiral arka duvar payı (çıkış ≥ 31)' % y0,6.5,'middle','',RED)
kaset(X2,Y2,12.5,y0,45,dK,'KAŞAR A','45×33 (hacim aynı)')
kaset(X2,Y2,12.5,yS,45,dS,'SUCUK','45×16 (hacim aynı)')
kaset(X2,Y2,14,yk,21,dk,'KAV.','21×17'); kaset(X2,Y2,35,yk,21,dk,'KUŞ.','21×17')
# Y-huni
ln(X2+px(24.5),Y2+px(yk+dk),X2+px(35),Y2+px(yk+dk)+10,1,BLU,'3,2'); ln(X2+px(45.5),Y2+px(yk+dk),X2+px(35),Y2+px(yk+dk)+10,1,BLU,'3,2')
tx(X2+px(58),Y2+px(yk+dk)+8,'Y-huni 10 cm (boru değil)',6.5,'start','',BLU)
c1,c2,c3 = y0+dK/2, yS+dS/2, yk+dk/2
cikis(X2,Y2,35,c1,True); cikis(X2,Y2,35,c2,True); cikis(X2,Y2,35,c3,True)
tx(X2+px(35)+px(31)+3,Y2+px(c1)+3,'x 4–66 ✓',7,'start','bold',GRN)
tx(X2+px(35)+px(31)+3,Y2+px(c3)+3,'öne taşar ✓ (açık)',7,'start','bold',GRN)
yy=Y2+px(105)+34
for i,s in enumerate(['SONUÇ ✓ — sığar, pay %.1f cm:' % (84-yend),
                      'derinlik: %.1f + %.1f + 1 + %.1f + 1 + 17 = %.1f ≤ 84' % (y0,dK,dS,yend),
                      'kaşar/sucuk kaseti genişletildi (45 en) → merkez x 35, hacim aynı',
                      'kavurma+kuşbaşı yan yana (merkez x 24,5 / 45,5 → tek başına ✗) → Y-huni ile x 35',
                      'yedek kasetler kaset katından çıkar → geçiş rafına (3 kat) · dolap 70 kalır']):
    tx(X2-px(14),yy+i*12,s,7.5,'start','bold' if i==0 else '',GRN if i==0 else '#333')

# ---------- Panel 3: 105 dolap, IKI KOLON ----------
X3,Y3=880,150
kabin(X3,Y3,105,84,'③ SEÇENEK B · 105 DOLAP · İKİ KOLON (çıkış = kaset merkezi, huni/boru yok)')
for xx in (0,105-13.5): rc(X3+px(xx),Y3,px(13.5),px(84),0,0,'none',None,'#fbeaea')
tx(X3+px(6.75),Y3+px(80),'13,5',6.5,'middle','',RED); tx(X3+px(105-6.75),Y3+px(80),'13,5',6.5,'middle','',RED)
# sol kolon x 13.5-48.5 (merkez 31): kasar 35x42 y 10-52, kavurma 21x17 y 53-70
kaset(X3,Y3,13.5,10,35,42,'KAŞAR A','35×42 (orijinal)')
kaset(X3,Y3,20.5,53,21,17,'KAV.','21×17')
# sag kolon x 56.5-91.5 (merkez 74): sucuk 35x21 y 20.5-41.5, kusbasi 21x17 y 42.5-59.5, yedek kucuk y 61-78
kaset(X3,Y3,56.5,20.5,35,21,'SUCUK','35×21 (orijinal)')
kaset(X3,Y3,63.5,42.5,21,17,'KUŞ.','21×17')
kaset(X3,Y3,63.5,61,21,17,'yedek küçük','çıkışsız','#888','#f7f6f2','3,2')
cikis(X3,Y3,31,31,True); cikis(X3,Y3,31,61.5,True); cikis(X3,Y3,74,31,True); cikis(X3,Y3,74,51,True)
ln(X3+px(31),Y3-30,X3+px(31),Y3-24,.8); ln(X3+px(74),Y3-30,X3+px(74),Y3-24,.8)
ln(X3,Y3-27,X3+px(31),Y3-27,.8); ln(X3+px(31),Y3-27,X3+px(74),Y3-27,.8); ln(X3+px(74),Y3-27,X3+px(105),Y3-27,.8)
tx(X3+px(15.5),Y3-31,'31',7,'middle','bold'); tx(X3+px(52.5),Y3-31,'43',7,'middle','bold'); tx(X3+px(89.5),Y3-31,'31',7,'middle','bold')
yy=Y3+px(105)+34
for i,s in enumerate(['SONUÇ ✓ — temiz geometri, pay bol:',
                      'kolon merkezi = duvar + 31 → 105 = 31 + 43 + 31 · daireler x 0–62 / 43–105 duvar içinde',
                      'sol kolon: kaşar (y 10–52, ç 31) + kavurma (ç 61,5) · sağ: sucuk (ç 31) + kuşbaşı (ç 51)',
                      'kasetler orijinal ölçüde, her çark kendi kasetinin altında, huni düz iner',
                      'bedel: hat +35 cm (105 = 1,5 modül) · yedekler geçiş rafı (105 geniş, 3 kat) + sağ kolon arkası']):
    tx(X3-px(14),yy+i*12,s,7.5,'start','bold' if i==0 else '',GRN if i==0 else '#333')

# ---------- KARAR ----------
yk0 = 720
rc(30,yk0,W-60,H-yk0-30,1.6,4)
tx(48,yk0+24,'MATEMATİK ÖZETİ ve KARAR',12,'start','bold')
rows = [
 ('Tepsi dönmez, robot tepsiyi x-y düzleminde öteler → çıkış O sabit, tepsi merkezi C = O − P (P pide üstündeki nokta). Spiral tüm pideyi dolaşacaksa C, O etrafında R 14 daire çizer; tepsi gövdesi (R 17) → O etrafında R 31 temiz alan.', '#333'),
 ('70 dolapta izinli çıkış bandı x 31–39 (8 cm). Kaset kendi merkezinde çıkış verecekse kaset merkezi bu banda gelmeli → kasetler YAN YANA olamaz, ARKA ARKAYA (tek kolon) dizilmeli. İki kolon isteniyorsa en az 97, temiz çözüm 105.', '#333'),
 ('A · 70 + tek kolon: kaşar 45×33, sucuk 45×16 (hacimler aynı), küçük çift 21×17 yan yana + 10 cm Y-huni · derinlik 82,7 / 84 (pay 1,3 cm) · yedekler geçiş rafına.', GRN),
 ('B · 105 + iki kolon: her çıkış tam kaset merkezinde, huni düz, kasetler orijinal, pay bol · bedel: hat 35 cm uzar, TOPPING 1,5 modül olur.', GRN),
 ('ÖNERİ: B (105). "Boru yok, huni düz iner, pay var" isteğini yalnız B tam karşılıyor; A sığıyor ama sıfıra yakın payla ve küçük çift için yine Y-huni ister. Karar Kemal'+chr(39)+'in → seçilen TOPPING v12 olarak çizilir, HAT v45'+chr(39)+'e girer.', BLU),
 ('Varsayımlar: topping yarıçapı 14 (2 cm kenar); tepsi Ø34; kaset yüksekliği 25 sabit; arka duvar kapalı, ön açık. Topping yarıçapı 12'+chr(39)+'ye insе bant 4 cm genişler (29–41) — yan yana kaseti yine kurtarmaz.', GRY),
]
for i,(s,c) in enumerate(rows):
    tx(48,yk0+48+i*40,s[:150],8.5,'start','bold' if i>=2 and i<=4 else '',c)
    if len(s)>150: tx(48,yk0+48+i*40+13,s[150:],8.5,'start','',c)
tx(W-40,H-38,'AUTOKITCH · arastirma/3_TOPPING/topping_cikis_geometri_v1 · 4 Eyl 2026',7,'end','',GRY)
o.append('</svg>')
out = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\3_TOPPING\topping_cikis_geometri_v1.svg"
io.open(out,'w',encoding='utf-8').write(chr(10).join(o))
print('yazildi', out, '| A derinlik %.2f (pay %.2f)' % (yend, 84-yend))
