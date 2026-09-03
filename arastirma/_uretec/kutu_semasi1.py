# -*- coding: utf-8 -*-
# Kutu talep semasi v1 — kutu ureticisine gonderilecek istek gorseli (TR+EN)
import io

W, H = 1250, 620
parts = []
def ln(x1,y1,x2,y2,w=2,c='#1a1a1a',dash=None):
    d = ' stroke-dasharray="%s"' % dash if dash else ''
    parts.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%.1f"%s/>' % (x1,y1,x2,y2,c,w,d))
def rc(x,y,w,h,sw=2,c='#1a1a1a',fill='none',dash=None,rx=0):
    d = ' stroke-dasharray="%s"' % dash if dash else ''
    r = ' rx="%d"' % rx if rx else ''
    parts.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" stroke="%s" stroke-width="%.1f" fill="%s"%s%s/>' % (x,y,w,h,c,sw,fill,d,r))
def tx(x,y,s,size=15,c='#1a1a1a',w='normal',anchor='start'):
    parts.append('<text x="%.1f" y="%.1f" font-family="Arial" font-size="%d" fill="%s" font-weight="%s" text-anchor="%s">%s</text>' % (x,y,size,c,w,anchor,s))
def ci(cx,cy,r,sw=2,c='#1a1a1a',fill='none'):
    parts.append('<circle cx="%.1f" cy="%.1f" r="%.1f" stroke="%s" stroke-width="%.1f" fill="%s"/>' % (cx,cy,r,c,sw,fill))
def arrow(x1,y1,x2,y2,w=2.5,c='#b3452b'):
    ln(x1,y1,x2,y2,w,c)
    import math
    a = math.atan2(y2-y1,x2-x1)
    for da in (2.6,-2.6):
        ln(x2,y2,x2-12*math.cos(a+da),y2-12*math.sin(a+da),w,c)

# Baslik
tx(30,42,'İSTENEN ÜRÜN: TEK HAMLEDE KURULAN (KENDİNDEN KİLİTLİ) PİDE KUTUSU',22,'#1a1a1a','bold')
tx(30,66,'Requested product: one-motion self-locking flatbread (pide/pizza) box — machine-erectable, glue-free',14,'#666')
ln(30,80,W-30,80,1,'#999')

PY = 120   # panel ust
PH = 360   # panel yukseklik

# ---------- PANEL 1: DUZ ISTIF ----------
P1 = 40
tx(P1,PY-26,'1 · DÜZ İSTİF',17,'#1a1a1a','bold')
tx(P1,PY-8,'flat stack',13,'#888')
# yassi blank destesi
sx, sy = P1+40, PY+240
for i in range(16):
    y = sy - i*7
    ln(sx, y, sx+240, y, 2.2, '#8a6a3a')
    ln(sx+4, y-3, sx+236, y-3, 1, '#c9b28e')
rc(sx-14, sy-16*7-8, 268, 16*7+22, 1.5, '#1a1a1a', dash='6,4')
tx(sx+120, sy+34, 'açılmamış düz kutular / flat blanks', 13, '#555', anchor='middle')
# olcu oku
ln(sx+282, sy-16*7-8, sx+282, sy+6, 1.4, '#b3452b')
ln(sx+276, sy-16*7-8, sx+288, sy-16*7-8, 1.4, '#b3452b')
ln(sx+276, sy+6, sx+288, sy+6, 1.4, '#b3452b')
tx(sx+296, sy-52, '1 kutu ≈ 3 mm', 13, '#b3452b')
tx(sx+296, sy-34, '160 kutu ≈ 50 cm', 13, '#b3452b')
tx(P1, PY+330, 'Kutu yassı sevk edilir ve makinede', 13.5, '#333')
tx(P1, PY+348, 'yassı depolanır. / Shipped and stored flat.', 13.5, '#333')

arrow(P1+380, PY+170, P1+430, PY+170)

# ---------- PANEL 2: TEK HAMLEDE KURULUM ----------
P2 = 490
tx(P2,PY-26,'2 · TEK HAMLEDE KURULUM',17,'#1a1a1a','bold')
tx(P2,PY-8,'one-motion erect',13,'#888')
# vantuz + blank
bx, by = P2+30, PY+70
tx(bx, by-14, 'vakum tek yaprak çeker / vacuum picks one blank', 12.5, '#555')
ln(bx, by+30, bx+260, by+30, 3, '#8a6a3a')            # blank
ci(bx+100, by+16, 9, 1.8, '#2a6a9a'); ci(bx+160, by+16, 9, 1.8, '#2a6a9a')  # vantuzlar
ln(bx+100, by+7, bx+100, by-6, 1.8, '#2a6a9a'); ln(bx+160, by+7, bx+160, by-6, 1.8, '#2a6a9a')
ln(bx+100, by-6, bx+160, by-6, 1.8, '#2a6a9a')
# piston
px_, pyy = bx+130, by+58
arrow(px_, pyy, px_, pyy+52, 3, '#b3452b')
tx(px_+12, pyy+34, 'tek piston bastırır', 13, '#b3452b')
tx(px_+12, pyy+50, 'single press stroke', 12, '#b3452b')
# disi kalip (V yanakli yuva)
kx, ky = bx+20, by+130
ln(kx, ky, kx+50, ky+60, 2.4)           # sol egik yanak
ln(kx+50, ky+60, kx+170, ky+60, 2.4)    # taban
ln(kx+170, ky+60, kx+220, ky, 2.4)      # sag egik yanak
ln(kx-24, ky, kx, ky, 2.4); ln(kx+220, ky, kx+244, ky, 2.4)
tx(kx+110, ky+92, 'eğimli dişi kalıp / tapered forming die', 12.5, '#555', anchor='middle')
# kurulan kutu kesiti kalibin icinde
ln(kx+58, ky+52, kx+162, ky+52, 3, '#8a6a3a')
ln(kx+58, ky+52, kx+40, ky+12, 3, '#8a6a3a')
ln(kx+162, ky+52, kx+180, ky+12, 3, '#8a6a3a')
tx(P2, PY+310, 'Kenarlar dil-yuva kilidiyle KENDİLİĞİNDEN kilitlenir —', 13.5, '#1a1a1a', 'bold')
tx(P2, PY+328, 'tutkal YOK, bant YOK, sıcak yapıştırma YOK. Süre 1-2 sn.', 13.5, '#1a1a1a', 'bold')
tx(P2, PY+348, 'Self-locking tabs — no glue, no tape, no hot-melt. 1-2 s.', 12.5, '#666')

arrow(P2+330, PY+170, P2+380, PY+170)

# ---------- PANEL 3: KURULMUS KUTU ----------
P3 = 910
tx(P3,PY-26,'3 · KURULMUŞ KUTU',17,'#1a1a1a','bold')
tx(P3,PY-8,'erected box',13,'#888')
gx, gy = P3+20, PY+90
# govde
rc(gx, gy+60, 220, 62, 2.4, '#1a1a1a')
# acik kapak (menteseli, geriye yatik)
ln(gx, gy+60, gx+50, gy-10, 2.2, '#1a1a1a')
ln(gx+50, gy-10, gx+270, gy-10, 2.2, '#1a1a1a')
ln(gx+270, gy-10, gx+220, gy+60, 2.2, '#1a1a1a')
tx(gx+160, gy+8, 'menteşeli kapak / hinged lid', 12, '#555', anchor='middle')
# pide
ci(gx+110, gy+91, 26, 2, '#8a6a3a')
tx(gx+110, gy+96, 'Ø28', 12.5, '#8a6a3a', 'bold', 'middle')
# olculer
ln(gx, gy+140, gx+220, gy+140, 1.4, '#b3452b')
ln(gx, gy+134, gx, gy+146, 1.4, '#b3452b'); ln(gx+220, gy+134, gx+220, gy+146, 1.4, '#b3452b')
tx(gx+110, gy+160, '32 cm', 13, '#b3452b', 'bold', 'middle')
ln(gx+238, gy+60, gx+238, gy+122, 1.4, '#b3452b')
ln(gx+232, gy+60, gx+244, gy+60, 1.4, '#b3452b'); ln(gx+232, gy+122, gx+244, gy+122, 1.4, '#b3452b')
tx(gx+248, gy+95, '4,5 cm', 13, '#b3452b', 'bold')
tx(P3, PY+280, 'Dış ≈ 32 × 32 × 4,5 cm (iç Ø30 tabana uygun).', 13.5, '#333')
tx(P3, PY+300, 'Kapak tek hareketle kapanır (eğik sac ile).', 13.5, '#333')
tx(P3, PY+320, 'Outside ≈ 32×32×4.5 cm; lid closes in one motion.', 12.5, '#666')

# ---------- ALT NOTLAR ----------
ln(30, PY+PH+20, W-30, PY+PH+20, 1, '#999')
ny = PY+PH+48
tx(30, ny, 'ŞARTLAR / REQUIREMENTS:', 15, '#1a1a1a', 'bold')
tx(30, ny+26, '· Gıda temasına uygun karton veya E-flüt oluklu (sıcak ürün ~90 °C) / food-grade board or E-flute, hot food safe', 13.5, '#333')
tx(30, ny+48, '· Kurulum İNSANSIZ — otomatik makinenin içindeki basit düzenek kuracak / erected UNMANNED inside a vending machine', 13.5, '#333')
tx(30, ny+70, '· Çok adımlı klasik kilitli pizza kutusu UYGUN DEĞİL / classic multi-step lock-corner pizza box is NOT suitable', 13.5, '#333')
tx(W-30, ny+70, 'AUTOKITCH · kutu_talep_semasi_v1', 11, '#999', anchor='end')

svg = '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d"><rect width="%d" height="%d" fill="#ffffff"/>%s</svg>' % (W,H,W,H,W,H,''.join(parts))
out = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\kutu_talep_semasi_v1.svg"
io.open(out,'w',encoding='utf-8').write(svg)
print('ok', out)
