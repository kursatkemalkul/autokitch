# -*- coding: utf-8 -*-
# KUTU ISTASYONU — istek krokisi v3
# Kemal: istif hacmi doldurmasin (duzen adamin isi), gercek die-cut blank krokisi,
# genislik 70-120 esnek, "katlama yontemi size ait", tum olculer degisebilir.
import io

S = 0.3
def px(mm): return mm*S
W, H = 1060, 800
parts = []
def ln(x1,y1,x2,y2,w=2,c='#1a1a1a',dash=None):
    d = ' stroke-dasharray="%s"' % dash if dash else ''
    parts.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%.1f"%s/>' % (x1,y1,x2,y2,c,w,d))
def rc(x,y,w,h,sw=2,c='#1a1a1a',fill='none',dash=None):
    d = ' stroke-dasharray="%s"' % dash if dash else ''
    parts.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" stroke="%s" stroke-width="%.1f" fill="%s"%s/>' % (x,y,w,h,c,sw,fill,d))
def tx(x,y,s,size=14,c='#1a1a1a',w='normal',anchor='start'):
    parts.append('<text x="%.1f" y="%.1f" font-family="Arial" font-size="%.1f" fill="%s" font-weight="%s" text-anchor="%s">%s</text>' % (x,y,size,c,w,anchor,s))
def oy(x,y1,y2,label,side='r'):
    ln(x,y1,x,y2,1.2,'#b3452b'); ln(x-5,y1,x+5,y1,1.2,'#b3452b'); ln(x-5,y2,x+5,y2,1.2,'#b3452b')
    if side=='r': tx(x+8,(y1+y2)/2+4,label,12.5,'#b3452b','bold')
    else: tx(x-8,(y1+y2)/2+4,label,12.5,'#b3452b','bold','end')
def ox(y,x1,x2,label):
    ln(x1,y,x2,y,1.2,'#b3452b'); ln(x1,y-5,x1,y+5,1.2,'#b3452b'); ln(x2,y-5,x2,y+5,1.2,'#b3452b')
    tx((x1+x2)/2,y+16,label,12.5,'#b3452b','bold',anchor='middle')

# Baslik
tx(30,36,'KUTU İSTASYONU — İSTEK KROKİSİ v3',21,'#1a1a1a','bold')
tx(30,58,'Pizza kutuları istifli İÇİNDE duracak + komutla tek tek katlayacak bir sistem. Katlama yöntemi ve iç yerleşim SİZE AİT. / Boxes stored flat inside + folds one on command. Method and layout are up to you.',11,'#666')
ln(30,70,W-30,70,1,'#999')

# --- SOL: hacim ---
X0, Y0 = 90, 120
GW, GH, AYAK = px(900), px(1850), px(120)
rc(X0, Y0, GW, GH, 2.6)
for ax in (X0+8, X0+GW-16):
    rc(ax, Y0+GH, 8, AYAK, 1.8)
ln(X0, Y0+GH, X0+GW, Y0+GH, 2.6)

# ic: alt bolgede iki sematik deste (hacmi doldurmaz)
def deste(dx, dy, dw, n):
    for i in range(n):
        y = dy - i*6
        ln(dx, y, dx+dw, y, 1.5, '#8a6a3a')
    rc(dx-5, dy-n*6-2, dw+10, n*6+10, 1.2, '#999', dash='4,3')
db = Y0+GH-px(180)
deste(X0+px(60), db, px(340), 34)
deste(X0+px(480), db, px(340), 34)
tx(X0+GW/2, db+26, '≈ 560 açık kutu İÇİNDE istiflenecek', 12, '#333', 'normal', 'middle')
tx(X0+GW/2, db+42, '(istif düzeni size ait — çizim temsilîdir)', 11, '#666', 'normal', 'middle')

# ust bolge: cozum size ait
tx(X0+GW/2, Y0+px(500), 'KATLAMA SİSTEMİ', 15, '#1d7a4f', 'bold', 'middle')
tx(X0+GW/2, Y0+px(500)+22, 'yöntem + iç yerleşim', 12.5, '#1d7a4f', 'normal', 'middle')
tx(X0+GW/2, Y0+px(500)+42, 'SİZE AİT', 13, '#1d7a4f', 'bold', 'middle')
tx(X0+GW/2, Y0+px(500)+64, 'biz sadece katlanmış kutuyu alacağız', 11.5, '#7aa88c', 'normal', 'middle')

# olculer
ox(Y0+GH+AYAK+26, X0, X0+GW, 'genişlik 70-120 cm arası (esnek)')
oy(X0-52, Y0, Y0+GH+AYAK, '≈200', side='l')
tx(X0, Y0+GH+AYAK+64, 'Derinlik ≈ 85 cm · TÜM ÖLÇÜLER YAKLAŞIKTIR, DEĞİŞEBİLİR', 12, '#666')

# --- SAG: gercek acilmis blank (die-cut) krokisi ---
NX = 620
tx(NX, 108, 'KUTU — AÇILMIŞ HÂLİ (die-cut):', 15, '#1a1a1a', 'bold')
f = 4.4  # px/cm
bx, by = NX+14, 132
def dln(x1,y1,x2,y2,dash=None,w=1.6,c='#1a1a1a'):
    ln(bx+x1*f, by+y1*f, bx+x2*f, by+y2*f, w, c, dash)
# ana serit konturu (y 4.5..36.5, x 0..77.5)
dln(0,4.5,0,36.5); dln(77.5,4.5,77.5,36.5)
dln(0,4.5,4.5,4.5); dln(0,36.5,4.5,36.5)
dln(36.5,4.5,41,4.5); dln(36.5,36.5,41,36.5)
dln(73,4.5,77.5,4.5); dln(73,36.5,77.5,36.5)
# taban yan kanatlari (ust/alt)
dln(4.5,0,36.5,0); dln(4.5,0,4.5,4.5); dln(36.5,0,36.5,4.5)
dln(4.5,41,36.5,41); dln(4.5,36.5,4.5,41); dln(36.5,36.5,36.5,41)
# kapak yan kanatlari (biraz iceride)
dln(42,0.8,72,0.8); dln(42,0.8,42,4.5); dln(72,0.8,72,4.5)
dln(42,40.2,72,40.2); dln(42,36.5,42,40.2); dln(72,36.5,72,40.2)
# kapak on kenari ust/alt konturu
dln(41,4.5,42,4.5); dln(41,36.5,42,36.5)
dln(72,4.5,73,4.5); dln(72,36.5,73,36.5)
# on kilit dili (solda kucuk cikinti)
dln(0,12,-2,13); dln(-2,13,-2,28); dln(-2,28,0,29)
# pilyaj (katlama) kesik cizgileri
for xx in (4.5, 36.5, 41, 73):
    dln(xx,4.5,xx,36.5,dash='5,4',w=1,c='#999')
dln(4.5,4.5,36.5,4.5,dash='5,4',w=1,c='#999')
dln(4.5,36.5,36.5,36.5,dash='5,4',w=1,c='#999')
dln(42,4.5,72,4.5,dash='5,4',w=1,c='#999')
dln(42,36.5,72,36.5,dash='5,4',w=1,c='#999')
# etiketler
tx(bx+20.5*f, by+21.5*f, 'TABAN', 12, '#8a6a3a', 'bold', 'middle')
tx(bx+57*f, by+21.5*f, 'KAPAK', 12, '#8a6a3a', 'bold', 'middle')
tx(bx+20.5*f, by-6, 'yan kanatlar', 10, '#999', 'normal', 'middle')
# olcu oklari
ox(by+41*f+18, bx, bx+77.5*f, '≈ 78 cm')
oy(bx+77.5*f+16, by, by+41*f, '≈ 41')
tx(NX+14, by+41*f+52, 'ORTA BOY kutu: katlanınca ≈ 32 × 32 × 4,5 cm · karton kalınlığı ≈ 3 mm', 12, '#333')
tx(NX+14, by+41*f+70, 'KUTU DEĞİŞEBİLİR — önereceğiniz kutuya/ölçüye uyarız', 12, '#1d7a4f', 'bold')

# --- SAG ALT: istek ozeti ---
ny_ = by+41*f+108
tx(NX, ny_, 'İSTEK / REQUEST:', 15, '#1a1a1a', 'bold')
notlar = [
 ('· Haftalık ~560 kutu (günde ~80 · tepe saatte ~12)', '#1a1a1a', 12.5, 'normal'),
 ('· Kutular açık hâlde sistemin İÇİNDE istifli duracak', '#1a1a1a', 12.5, 'normal'),
 ('· Komut gelince (24V sinyal / PLC) TEK kutu katlayacak', '#1a1a1a', 12.5, 'bold'),
 ('· KATLAMA YÖNTEMİ SİZE AİT — çıktı: katlanmış kutu', '#1a1a1a', 12.5, 'bold'),
 ('· Sürekli çalışmaz — sanayi tipi büyük makine aramıyoruz', '#1a1a1a', 12.5, 'normal'),
 ('· Tüm ölçüler yaklaşık — öneriniz değerlidir', '#555', 12, 'normal'),
]
yy = ny_+26
for s, c, sz, w_ in notlar:
    tx(NX, yy, s, sz, c, w_)
    yy += 22
tx(NX, yy+12, 'EN: ~560 flat blanks/week stored inside; on command it folds ONE box;', 10.5, '#888')
tx(NX, yy+27, 'folding method is up to you — we only need the folded box; not continuous.', 10.5, '#888')

tx(W-30, H-16, 'AUTOKITCH · kutu_istasyonu_teknik_v3', 11, '#999', anchor='end')

svg = '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d"><rect width="%d" height="%d" fill="#ffffff"/>%s</svg>' % (W,H,W,H,W,H,''.join(parts))
out = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\kutu_istasyonu_teknik_v3.svg"
io.open(out,'w',encoding='utf-8').write(svg)
print('ok', out)
