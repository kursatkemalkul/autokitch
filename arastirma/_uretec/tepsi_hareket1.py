# -*- coding: utf-8 -*-
# TEPSI HAREKET ANALIZI v1 — ust gorunum, olcekli (mm): kabin 70x42 (arka duvar ustte, on acik, koridor altta)
# MEVCUT (kulplu tepsi + bilekten 360 donus) neden carpar + 3 alternatif
import io, math

E = []
def ln(x1,y1,x2,y2,w=1.4,c='#111',dash=None):
    d = ' stroke-dasharray="%s"' % dash if dash else ''
    E.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%s"%s/>' % (x1,y1,x2,y2,c,w,d))
def rc(x,y,w_,h,sw=1.4,rx=0,c='#111',dash=None,fill='none'):
    d = ' stroke-dasharray="%s"' % dash if dash else ''
    E.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%s" fill="%s" stroke="%s" stroke-width="%s"%s/>' % (x,y,w_,h,rx,fill,c,sw,d))
def ci(cx,cy,r,sw=1.4,c='#111',dash=None,fill='none'):
    d = ' stroke-dasharray="%s"' % dash if dash else ''
    E.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" stroke="%s" stroke-width="%s"%s/>' % (cx,cy,r,fill,c,sw,d))
def tx(x,y,s,fs=11,a='middle',w='',col='#111'):
    fw = ' font-weight="%s"' % w if w else ''
    E.append('<text x="%.1f" y="%.1f" text-anchor="%s" font-size="%s" fill="%s" font-family="Arial"%s>%s</text>' % (x,y,a,fs,col,fw,s))
def arr(x1,y1,x2,y2,w=1.6,c='#1d7a4f'):
    ln(x1,y1,x2,y2,w,c)
    a = math.atan2(y2-y1,x2-x1)
    for da in (2.6,-2.6):
        ln(x2,y2,x2-8*math.cos(a+da),y2-8*math.sin(a+da),w,c)

W, H = 1560, 1300
tx(40,44,'TEPSİ HAREKET ANALİZİ v1 — üstten, ölçekli · kabin 70×42 (arka duvar üstte, ön AÇIK, altta robot koridoru) · pide Ø28 · tepsi Ø34 · kulp 12',17,'start','bold')
tx(40,68,'Soru: çıkış pidenin EN DIŞINA malzeme koyarken tepsi duvara çarpıyor mu? Kural: ağız pide üstünde yarıçap r noktasına dökecekse tepsi merkezi ağızdan r uzakta olmalı (r = 0…14 cm); yön SERBEST (tepsi döndürülebiliyorsa). Tepsi merkezi yan duvarlardan ≥17, arka duvardan ≥17 cm.',10.5,'start','','#555')

S = 0.5
def panel(px0, py0, title, tag, tagc):
    tx(px0, py0-14, title, 12.5, 'start', 'bold')
    tx(px0+350, py0-14, tag, 12, 'end', 'bold', tagc)
    # koridor
    rc(px0, py0+420*S, 700*S, 300*S, 0.8, 0, '#bbb', '4,3', '#f7f7f7')
    tx(px0+350*S, py0+700*S, 'ROBOT KORİDORU (duvar yok)', 8, 'middle', '', '#999')
    # kabin: arka duvar + yan duvarlar kalin, on kenar kesik
    rc(px0, py0, 700*S, 420*S, 1, 0, '#ddd', None, '#fff')
    ln(px0, py0, px0+700*S, py0, 4)
    ln(px0, py0, px0, py0+420*S, 4); ln(px0+700*S, py0, px0+700*S, py0+420*S, 4)
    ln(px0, py0+420*S, px0+700*S, py0+420*S, 1.2, '#111', '6,4')
    tx(px0+350*S, py0-3, 'arka duvar', 7.5, 'middle', '', '#888')
    tx(px0-6, py0+210*S, 'PRESS', 7.5, 'end', '', '#888'); tx(px0+700*S+6, py0+210*S, 'OVEN', 7.5, 'start', '', '#888')
    tx(px0+350*S, py0+420*S+11, 'ön kenar (açık)', 7.5, 'middle', '', '#888')
def kaset(px0,py0,x,y,w,h,ad,alt='',c='#555'):
    rc(px0+x*S+1.5, py0+y*S+1.5, w*S-3, h*S-3, 1, 2, c, None, '#f4f1ea')
    tx(px0+(x+w/2)*S, py0+(y+h/2)*S-1, ad, 8, 'middle', 'bold', '#444')
    if alt: tx(px0+(x+w/2)*S, py0+(y+h/2)*S+10, alt, 7, 'middle', '', '#777')
def outlet(px0,py0,x,y,ad,r=18):
    ci(px0+x*S, py0+y*S, r*S, 1.6, '#b3452b', None, '#fde3dc')
    ci(px0+x*S, py0+y*S, 1.8, 1, '#b3452b', None, '#b3452b')
    tx(px0+x*S, py0+y*S-r*S-3, ad, 7, 'middle', 'bold', '#b3452b')
def tray(px0,py0,cx,cy,kulp=True,ring=False,c='#1a49b8',dash=None,label=''):
    ci(px0+cx*S, py0+cy*S, 170*S, 1.6, c, dash, 'rgba(26,73,184,0.06)')
    ci(px0+cx*S, py0+cy*S, 140*S, 0.8, '#8a6a3a', '3,3')
    if ring: ci(px0+cx*S, py0+cy*S, 200*S, 1.2, c, '5,3')
    if kulp:
        rc(px0+(cx-15)*S, py0+(cy+170)*S, 30*S, 120*S, 1.4, 2, c)
        rc(px0+(cx-22)*S, py0+(cy+250)*S, 44*S, 40*S, 1.4, 2, c, None, '#dfe7fb')
    ci(px0+cx*S, py0+cy*S, 2, 1, c, None, c)
    if label: tx(px0+cx*S, py0+cy*S+4, label, 7.5, 'middle', 'bold', c)
def zone(px0,py0,x1,y1,x2,y2,ad,top=True):
    rc(px0+x1*S, py0+y1*S, (x2-x1)*S, (y2-y1)*S, 1.2, 0, '#1d7a4f', '5,3', 'rgba(29,122,79,0.08)')
    tx(px0+(x1+x2)/2*S, (py0+y1*S-3) if top else (py0+y2*S-4), ad, 7, 'middle', 'bold', '#1d7a4f')
def note(x, y, lines, lh=15.5):
    for s_, c_ in lines:
        if s_: tx(x, y, s_, 9.8, 'start', 'bold' if s_.endswith(':') else '', c_)
        y += lh
G, Rd, Bl, Gr = '#1d7a4f', '#b3452b', '#1a49b8', '#555'

# ================= PANEL 1 — MEVCUT =================
P1x, P1y = 60, 118
panel(P1x, P1y, '1 · MEVCUT (v8): kulplu tepsi, bilek 360°', 'ÇARPAR ✗', Rd)
kaset(P1x,P1y,0,0,350,420,'KAŞAR','35×42'); kaset(P1x,P1y,350,0,170,210,'KAVURMA'); kaset(P1x,P1y,520,0,170,210,'KUŞBAŞI'); kaset(P1x,P1y,350,210,350,210,'SUCUK','35×21')
for x,y,ad in ((200,210,'kaşar'),(400,175,'kav'),(470,300,'sucuk'),(520,175,'kuş')): outlet(P1x,P1y,x,y,ad)
tray(P1x,P1y,520,175,kulp=True,label='r=0')
ci(P1x+520*S, P1y+175*S, 290*S, 1.4, Rd, '6,4')       # kulp+kilit tarama dairesi
tx(P1x+520*S, P1y+(175+290)*S+12, 'kulp+kilit taraması R29 (360° için)', 7.5, 'middle', 'bold', Rd)
tx(P1x+700*S+4, P1y+175*S+24, '✗ sağ duvar', 8, 'start', 'bold', Rd)
tx(P1x+520*S+40, P1y+8, '✗ arka duvar', 8, 'start', 'bold', Rd)
zone(P1x,P1y,290,290,410,420,'360° için merkez bölgesi: x 29-41 · y ≥29 → 1 çıkış sığar')
note(P1x+370, P1y+8, [
 ('NEDEN ÇARPAR:','#b3452b'),
 ('· Tepsiyi merkezinden 360° döndürmek = kulp ve','#333'),
 ('  kilit R29 daire tarar → yan/arka duvar + komşu ağız','#333'),
 ('· Daha kötüsü: kulbu tutan KOL da tepsinin etrafında','#333'),
 ('  dolanmalı (dirsek arka duvara girer) — kol tepsiyi','#333'),
 ('  kenardan tutunca en fazla ±90° çevirebilir','#333'),
 ('· 360° için merkez bölgesi 12×13 cm → 4 çıkış sığmaz','#333'),
 ('· Blender\'daki çarpma tam bu: sağ uç çıkış (52,17,5)','#666'),
 ('  için kulp sağa/arkaya dönünce duvara girer','#666'),
 ('','#333'),
 ('SONUÇ: kenardan tutulan tepsi 70 cm kabin İÇİNDE','#b3452b'),
 ('tam tur atamaz — ya dönüş kabinin DIŞINDA olacak,','#b3452b'),
 ('ya tepsi kendi içinde dönecek (alt. 2), ya ±90° ile','#b3452b'),
 ('yetinilecek (alt. 3).','#b3452b'),
])

# ================= PANEL 2 — ALT 1: ON SACAK =================
P2x, P2y = 830, 118
panel(P2x, P2y, '2 · ALT 1 — ÖN SAÇAK: dozaj koridorda', 'ÖNERİ ✓', G)
kaset(P2x,P2y,0,0,300,420,'KAŞAR','30×42'); kaset(P2x,P2y,300,0,160,420,'SUCUK','16×42'); kaset(P2x,P2y,460,0,120,420,'KAV.','12×42'); kaset(P2x,P2y,580,0,120,420,'KUŞ.','12×42')
rc(P2x, P2y+420*S, 700*S, 100*S, 1.2, 0, '#111', None, '#eee')
tx(P2x+350*S, P2y+470*S+3, 'SAÇAK 10 cm — 4 ağız altında', 7.5, 'middle', 'bold', '#444')
for x,ad in ((175,'kaşar'),(380,'sucuk'),(520,'kav'),(640,'kuş')): outlet(P2x,P2y,x,470,ad)
# koni oklari (kaset merkezinden agiza)
for (kx,ky),(ox,oy) in (((150,210),(175,470)),((380,210),(380,470)),((520,210),(520,470)),((640,210),(640,470))):
    arr(P2x+kx*S, P2y+ky*S+8, P2x+ox*S, P2y+oy*S-12, 1, '#999')
tray(P2x,P2y,175,470,kulp=True,label='kaşar r=0')
tray(P2x,P2y,500,470,kulp=True,dash='4,3',label='kuş r=14 (sola)')
tx(P2x+700*S+4, P2y+300*S, '✓', 9, 'start', 'bold', G); tx(P2x-8, P2y+300*S, '✓', 9, 'end', 'bold', G)
note(P2x+370, P2y+8, [
 ('NASIL ÇALIŞIR:','#1d7a4f'),
 ('· 4 çark ağzı kabinin ÖN yüzündeki 10 cm saçağın','#333'),
 ('  altında (y 47); tepsi hep KORİDORDA, yan duvar yok','#333'),
 ('· Kol tepsiyi kenardan tutar, ±90° çevirir + öteler:','#333'),
 ('  her yarıçap için iki 180° yay → pide tamamen dolar','#333'),
 ('· Kabin altına yalnız tepsinin arkası girer (y 30-42):','#333'),
 ('  kenar çıkışlar "iç tarafa" ötelenir (kaşar sağa, kuş sola)','#333'),
 ('· Kilit/kulp hiç kabin altına girmez → ağız-kilit sorunu yok','#333'),
 ('DEĞİŞEN:','#b3452b'),
 ('· Kaset katı 4 ŞERİT (hepsi ön kenara değer): kaşar 30×42','#333'),
 ('  · sucuk 16×42 · kavurma 12×42 · kuşbaşı 12×42; tek','#333'),
 ('  yükseklik 30 (kaşar 38 L ✓, sucuk 20 L ✓, küçükler 15 L)','#666'),
 ('· Her koni kendi şeridinde öne eğimli (≤21 cm, ≥48°)','#333'),
 ('· Kabin altı 26 cm boşluk GEREKMEZ → geçiş rafına gider','#333'),
 ('· Tepsi, kilit, kulp, istasyonlar: AYNEN (motor yok)','#1d7a4f'),
])

# ================= PANEL 3 — ALT 2: C-TUTUCU + DONER DISK =================
P3x, P3y = 60, 600
panel(P3x, P3y, '3 · ALT 2 — C-TUTUCU: disk elde kendi içinde döner', 'OLUR ✓', G)
kaset(P3x,P3y,0,0,350,420,'KAŞAR','35×42'); kaset(P3x,P3y,350,0,170,210,'KAVURMA'); kaset(P3x,P3y,520,0,170,210,'KUŞBAŞI'); kaset(P3x,P3y,350,210,350,210,'SUCUK','35×21')
for x,y,ad in ((210,210,'kaşar'),(400,200,'kav'),(470,300,'sucuk'),(500,200,'kuş')): outlet(P3x,P3y,x,y,ad)
tray(P3x,P3y,500,200,kulp=False,ring=True,label='kuş r=0')
tray(P3x,P3y,210,350,kulp=False,ring=True,dash='4,3',label='kaşar r=14')
# C-tutucu kol: on tarafta motor kutusu
rc(P3x+(500-40)*S, P3y+(200+200)*S, 80*S, 50*S, 1.4, 2, Bl, None, '#dfe7fb'); tx(P3x+500*S, P3y+(200+232)*S, 'M', 8, 'middle', 'bold', Bl)
zone(P3x,P3y,200,200,500,420,'merkez bölgesi x 20-50 · y ≥20 (halka +3)',top=False)
note(P3x+370, P3y+8, [
 ('NASIL ÇALIŞIR:','#1d7a4f'),
 ('· Tepsi = bordürlü DİSK, kulp yok; robotun ucu C-halka','#333'),
 ('  (3 V-makara, biri NEMA17 ile tahrikli): disk halkada','#333'),
 ('  kendi merkezinde SINIRSIZ döner → gerçek spiral','#333'),
 ('· Halka dönmez → tarama = disk + 3 cm; kabin içinde her','#333'),
 ('  yere girer, kol önden tutar, ağız-kilit çakışması yok','#333'),
 ('· v8 kaset katı AYNEN; çıkışlar 1-3 cm içe: (21,21)','#333'),
 ('  (40,20) (47,30) (50,20) — koni kaymaları ≤5 cm','#333'),
 ('· Fırın/press/kesim: disk halkadan sıyrılıp düz oturur','#333'),
 ('  (halka önü açık C) — istasyonlarda değişiklik yok','#333'),
 ('BEDELİ:','#b3452b'),
 ('· TOPPING tabla motoru gitmedi, robotun ELİNE taşındı','#333'),
 ('  (1 step motor + kayış, uç değiştiricide)','#666'),
 ('· Makaralar 350 °C jantı tutar → çelik makara, motor uzakta','#333'),
 ('· Kabin altı 26 cm boşluk kalır; uç 1,5 kg ağırlaşır','#333'),
])

# ================= PANEL 4 — ALT 3: MERKEZ KUME =================
P4x, P4y = 830, 600
panel(P4x, P4y, '4 · ALT 3 — MERKEZ KÜME: ±90° + öteleme', 'SIKIŞIK ◐', '#9a6b1f')
kaset(P4x,P4y,0,0,350,420,'KAŞAR','35×42'); kaset(P4x,P4y,350,0,350,210,'SUCUK (arka)','35×21'); kaset(P4x,P4y,350,210,170,210,'KAVURMA'); kaset(P4x,P4y,520,210,170,210,'KUŞBAŞI')
for x,y,ad in ((280,320,'kaşar'),(380,320,'sucuk'),(330,400,'kav'),(430,400,'kuş')): outlet(P4x,P4y,x,y,ad,16)
for (kx,ky),(ox,oy) in (((175,210),(280,320)),((525,105),(380,320)),((435,315),(330,400)),((605,315),(430,400))):
    arr(P4x+kx*S, P4y+ky*S+8, P4x+ox*S, P4y+oy*S-10, 1, '#999')
tray(P4x,P4y,180,320,kulp=True,label='kaşar r=10 (sola)')
tray(P4x,P4y,430,260,kulp=True,dash='4,3',label='kuş r=14 (arkaya)')
zone(P4x,P4y,270,310,430,420,'ağız bölgesi x 27-43 · y 31-42',top=False)
note(P4x+370, P4y+8, [
 ('NASIL ÇALIŞIR:','#9a6b1f'),
 ('· Kemal\'in tepsisi/kilidi AYNEN; kol ±90° çevirir + XY','#333'),
 ('  öteler; 4 ağız kabinin ÖN-ORTA bölgesinde kümelenir','#333'),
 ('  (aralık 10 cm) — böylece öteleme duvara varmaz','#333'),
 ('· Pidenin ön dilimi için tepsi ağzın ARKASINA ötelenir','#333'),
 ('  (y ≥17) → ağızlar y ≥31 olmalı (ön banda)','#333'),
 ('· Kilit kabin altına girer → ağızlar kilidin ÜSTÜNDEN','#333'),
 ('  geçmeli: düşme 8 cm (saçılma artar, hassasiyet düşer)','#333'),
 ('DEĞİŞEN / RİSK:','#b3452b'),
 ('· Kaset yer değişimi: kavurma+kuşbaşı ÖNE, sucuk ARKAYA','#333'),
 ('· Koniler 5-25 cm yatay taşır; sucuk 25 cm → 43° ✗','#333'),
 ('  (çark katı 23→30 cm ile 52°)','#666'),
 ('· 4 rotor 10 cm aralıkla dip dibe: kaşar rotoru Ø12 sığmaz','#333'),
 ('  → kaşar Ø8 çift cep (pilot)','#666'),
 ('· En az yeni parça, en çok uzlaşma','#333'),
])

# ================= KARSILASTIRMA =================
TY = 1000
tx(60, TY, 'KARŞILAŞTIRMA', 12.5, 'start', 'bold')
cols = [60, 330, 660, 990, 1320]
heads = ['', '1 · MEVCUT', '2 · ÖN SAÇAK (öneri)', '3 · C-TUTUCU', '4 · MERKEZ KÜME']
rows = [
 ('Tepsi + kilit + kulp', 'aynen', 'AYNEN', 'kulp yok, bordürlü disk', 'AYNEN'),
 ('Robot ucunda motor', 'yok', 'yok', '1 step motor (halka)', 'yok'),
 ('Dönüş', '360° istenir — OLMAZ', '±90° + öteleme (yaylar)', 'sınırsız (spiral)', '±90° + öteleme'),
 ('Duvara çarpma', 'ÇARPAR', 'yok — tepsi koridorda', 'yok — x 20-50, y ≥20', 'yok — ağızlar ortada'),
 ('Kaset katı', 'v8', '4 şerit (v9) + tek yük. 30', 'v8 aynen', 'kavurma/kuşbaşı öne, sucuk arkaya'),
 ('Koniler', 'kısa', 'öne eğimli ≤21 cm', '≤5 cm kayma', '5-25 cm, sucuk sınırda'),
 ('Kabin', '26 cm boşluk', 'boşluk kalkar, +10 cm saçak', '26 cm boşluk kalır', '26 cm boşluk + ağız 8 cm yüksek'),
 ('İstasyonlar', '—', 'değişmez', 'değişmez', 'değişmez'),
 ('Karar', '✗', '✓ en temiz: motor yok, tepsi aynen', '✓ spiral en iyi, uç ağırlaşır', '◐ sığar ama sıkışık'),
]
y = TY+22
for k,h in enumerate(heads):
    tx(cols[k], y, h, 9.5, 'start', 'bold', ['#333',Rd,G,G,'#9a6b1f'][k])
y += 8
for r_ in rows:
    y += 20
    ln(60, y-14, 1520, y-14, 0.5, '#ddd')
    for k,cell in enumerate(r_):
        col = '#333' if k else '#111'
        if k == 1 and ('OLMAZ' in cell or 'ÇARPAR' in cell or cell == '✗'): col = Rd
        if cell.startswith('✓'): col = G
        if cell.startswith('◐'): col = '#9a6b1f'
        tx(cols[k], y, cell, 9.5, 'start', 'bold' if k == 0 else '', col)

tx(W-24, H-14, 'AUTOKITCH · tepsi_hareket_analizi_v1', 10, 'end', '', '#999')
svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d"><rect width="%d" height="%d" fill="#ffffff"/>%s</svg>' % (W,H,W,H,W,H,''.join(E))
OUT = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\8_ROBOT\tepsi_hareket_analizi_v1.svg"
io.open(OUT,'w',encoding='utf-8').write(svg)
print('yazildi:', OUT)
