# -*- coding: utf-8 -*-
# TEPSI HAREKET ANALIZI v2 — TEPSI DONMEZ (Kemal): kol tepsiyi sabit yonde tutar, yatay duzlemde oteler (yorunge/spiral).
# Kural: tepsi merkezi C, agiz O etrafinda 14 cm yaricapli TAM daire cizebilmeli -> C-diski (r14) izinli bolgede kalmali.
# Izinli bolge (kabin 70x84, tepsi O34, kulp one): x 17-53, y >= 17 (on acik). => agizlar x 31-39, y >= 31.
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
def oy(x1,x2,y,cm):
    ln(x1,y,x2,y,1,'#b3452b'); ln(x1,y-5,x1,y+5,1,'#b3452b'); ln(x2,y-5,x2,y+5,1,'#b3452b')
    tx((x1+x2)/2,y-6,cm,10.5,'middle','bold','#b3452b')
def ox(x,y1,y2,cm):
    ln(x,y1,x,y2,1,'#b3452b'); ln(x-5,y1,x+5,y1,1,'#b3452b'); ln(x-5,y2,x+5,y2,1,'#b3452b')
    E.append('<text x="%.1f" y="%.1f" text-anchor="middle" font-size="10" font-weight="bold" fill="#b3452b" font-family="Arial" transform="rotate(-90 %.1f %.1f)">%s</text>' % (x-9,(y1+y2)/2,x-9,(y1+y2)/2,cm))

W, H = 1560, 1180
tx(40,44,'TEPSİ HAREKET ANALİZİ v2 — TEPSİ DÖNMEZ: kol tepsiyi sabit yönde tutar, yatay düzlemde öteler (yörünge / spiral) · kabin 70×84 · tepsi Ø34 · kulp öne',17,'start','bold')
tx(40,68,'Hesap: ağız O sabit; pidenin (r, açı) noktasını ağzın altına getirmek için tepsi merkezi C = O − P olmalı → C, ağzın etrafında 14 cm yarıçaplı TAM DAİRE çizmeli. C izinli bölge: x 17-53 (yan duvar 17), y ≥ 17 (arka duvar; ön açık) → ağız x 31-39, y ≥ 31.',10.5,'start','','#555')

# ================= UST GORUNUM 1:1 (1 px = 1 mm) =================
S = 1.0
X0, Y0 = 80, 120
def P(x,y): return (X0+x*S, Y0+y*S)
# kabin + koridor
rc(X0, Y0+840, 700, 200, .8, 0, '#bbb', '4,3', '#f7f7f7'); tx(X0+350, Y0+960, 'ROBOT KORİDORU (ön açık — tepsi öne taşabilir)', 9, 'middle', '', '#999')
rc(X0, Y0, 700, 840, 1, 0, '#ddd', None, '#fff')
ln(X0,Y0,X0+700,Y0,4); ln(X0,Y0,X0,Y0+840,4); ln(X0+700,Y0,X0+700,Y0+840,4); ln(X0,Y0+840,X0+700,Y0+840,1.2,'#111','6,4')
tx(X0+350, Y0-6, 'arka duvar', 8, 'middle', '', '#888'); tx(X0-8, Y0+420, 'PRESS', 8, 'end', '', '#888'); tx(X0+708, Y0+420, 'OVEN', 8, 'start', '', '#888')
# kasetler — on sira duz, arka sira kesik
def kas(x,y,w,h,ad,alt,front=True):
    c = '#111' if front else '#999'
    rc(X0+x+2, Y0+y+2, w-4, h-4, 1.2 if front else 1, 3, c, None if front else '4,3', '#f4f1ea' if front else '#fafafa')
    tx(X0+x+w/2, Y0+y+h/2-2, ad, 9 if front else 8, 'middle', 'bold', c)
    tx(X0+x+w/2, Y0+y+h/2+11, alt, 7.5, 'middle', '', c)
kas(0,420,350,420,'KAŞAR A','35×42 · çalışan')
kas(0,0,350,420,'KAŞAR B','35×42 · sıradaki',False)
kas(350,630,350,210,'SUCUK','35×21 · çalışan')
kas(350,0,350,210,'SUCUK yedek','35×21 · sıradaki',False)
kas(350,210,170,210,'KAVURMA','17×21 · çalışan')
kas(350,420,170,210,'KUŞBAŞI','17×21 · çalışan')
kas(520,210,170,210,'sır. KAV','donmuş gelir',False)
kas(520,420,170,210,'sır. KUŞ','1 gün çözülür',False)
# izinli C bolgesi (yesil)
rc(X0+170, Y0+170, 360, 870, 1.4, 0, '#1d7a4f', '6,4', 'rgba(29,122,79,0.06)')
tx(X0+350, Y0+185, 'TEPSİ MERKEZİ İZİNLİ BÖLGE: x 17-53 · y ≥ 17', 8.5, 'middle', 'bold', '#1d7a4f')
# agiz bandi
rc(X0+310, Y0+310, 80, 530, 1, 0, '#b3452b', '3,3', 'rgba(179,69,43,0.05)')
tx(X0+350, Y0+300, 'AĞIZ BANDI x 31-39', 7.5, 'middle', 'bold', '#b3452b')
# agizlar + C-diskleri
OUT = [(350,340,'C','kavurma'),(350,460,'D','kuşbaşı'),(350,580,'A','kaşar'),(350,700,'B','sucuk')]
for ox_,oy_,ad,nm in OUT:
    ci(X0+ox_, Y0+oy_, 140, 1.1, '#1d7a4f', '5,4')
    ci(X0+ox_, Y0+oy_, 20, 1.6, '#b3452b', None, '#fde3dc'); tx(X0+ox_, Y0+oy_+4, ad, 8, 'middle', 'bold', '#b3452b')
    tx(X0+ox_+28, Y0+oy_+4, nm+' (35, %d)' % (oy_/10), 7.5, 'start', '', '#b3452b')
tx(X0+350, Y0+832, 'yeşil daireler = her ağız için C-diski (r 14) — hepsi izinli bölgede ✓', 8, 'middle', 'bold', '#1d7a4f')
# tepsi uc konumlar (agiz A icin): C = O - P
def tray(cx,cy,c='#1a49b8',dash='5,4',lab=''):
    ci(X0+cx, Y0+cy, 170, 1.3, c, dash, 'rgba(26,73,184,0.05)')
    ci(X0+cx, Y0+cy, 140, .7, '#8a6a3a', '2,3')
    rc(X0+cx-15, Y0+cy+170, 30, 120, 1.2, 2, c, dash)   # kulp ONE (+y)
    rc(X0+cx-22, Y0+cy+250, 44, 40, 1.2, 2, c, dash, '#dfe7fb')
    ci(X0+cx, Y0+cy, 2.5, 1, c, None, c)
    if lab: tx(X0+cx, Y0+cy-8, lab, 7.5, 'middle', 'bold', c)
tray(350,440,lab='C=(35,44): A pidenin ÖN kenarına')
tray(210,580,lab='C=(21,58): sağ kenar')
tray(350,720,'#1a49b8','2,3','C=(35,72): arka kenar')
# spiral (agiz A etrafinda, C yolu): r 0 -> 140, 4.7 tur
pth = ''
N = 470
for k in range(N+1):
    a = k/100.0*2*math.pi; r = 140*k/N
    x = X0+350 + r*math.cos(a); y = Y0+580 + r*math.sin(a)
    pth += ('M' if k==0 else 'L') + '%.1f %.1f ' % (x,y)
E.append('<path d="%s" fill="none" stroke="#1a49b8" stroke-width="1.4"/>' % pth)
arr(X0+350+140*math.cos(0.1), Y0+580+140*math.sin(0.1), X0+350+140*math.cos(0.3), Y0+580+140*math.sin(0.3), 1.6, '#1a49b8')
tx(X0+350, Y0+575-150, 'mavi: C\'nin spiral yolu (A ağzı) — 4,7 tur · hatve 3 cm', 7.5, 'middle', 'bold', '#1a49b8')
# olculer
oy(X0, X0+350, Y0-30, '35'); oy(X0+350, X0+700, Y0-30, '35')
ox(X0-30, Y0, Y0+420, '42'); ox(X0-30, Y0+420, Y0+840, '42')
ox(X0+740, Y0+170, Y0+840, 'C bölgesi 67');

# ================= NOTLAR =================
NX, NY = 900, 120
tx(NX, NY, 'KURAL (tepsi dönmez → yalnız öteleme):', 13, 'start', 'bold')
note = [
 ('· Pide noktası P (yarıçap r ≤ 14, açı β) ağzın altına gelsin:','#333'),
 ('  tepsi merkezi C = O − P → C, O etrafında r yarıçaplı daire çizer','#333'),
 ('· Tam kaplama = C-diski (r 14) izinli bölgede: x 17-53, y ≥ 17','#333'),
 ('  → ağız x ∈ [31, 39], y ≥ 31. Kabin ortası hattı = x 35.','#1d7a4f'),
 ('· 4 ağız ORTA HATTA, derinlikte 12 cm arayla:','#1d7a4f'),
 ('  C kavurma (35,34) · D kuşbaşı (35,46) · A kaşar (35,58) · B sucuk (35,70)','#1d7a4f'),
 ('· En öndeki ağız (B, y 70): C y 56-84 → tepsi öne 17 cm taşar (ön açık ✓)','#333'),
 ('· En arkadaki (C, y 34): C y 20-48 → arka duvara 3 cm pay ✓','#333'),
 ('· Yanlar: C x 21-49 → duvara 4 cm pay ✓ (kulp hep öne, sallanmaz)','#333'),
 ('','#333'),
 ('KASET KATI (70×84 tam dolu) — her koni kendi ağzına:','#333'),
 ('· kaşar A 35×42 (sol ön) → A: 18 cm yatay / 21 düşey → 49°','#333'),
 ('· sucuk 35×21 (sağ ön) → B: 18 cm → 49°','#333'),
 ('· kavurma 17×21 (orta arka) → C: 9 cm · kuşbaşı (orta ön) → D: 10 cm','#333'),
 ('· arka sıra sıradaki: kaşar B · sucuk yedek · 2 küçük (donmuş gelir, çözülür)','#666'),
 ('· ağızlar orta hatta = iki kaset sütununun birleşim çizgisi (x 35)','#666'),
 ('','#333'),
 ('HAREKET (kol, bilek sabit):','#333'),
 ('· Spiral: r 0 → 14, hatve 3 cm (kaşar şerit genişliği) → 4,7 tur','#333'),
 ('  yol ≈ π·n·r_maks ≈ 207 cm; 15 cm/s → ~14 sn (kaşar 4 cep boyunca)','#333'),
 ('· Sucuk: halka r 10 + r 5, cep cep (8-10 küp) → ~6 sn','#333'),
 ('· Kavurma/kuşbaşı: serpme spirali r 3 → 13, ~8 sn','#333'),
 ('· Toplam dozaj ~30 sn/pide (kaşarlı ~14) — bütçeye uyar','#333'),
 ('· Robotun bu hareketinin adı: "dairesel öteleme" (orbital move) —','#666'),
 ('  UR/Fanuc\'ta MoveC/MoveP ile standart, bilek açısı sabit','#666'),
 ('','#333'),
 ('KİLİT / AĞIZ ÇAKIŞMASI:','#b3452b'),
 ('· Kilit tepesi tepsi tabanından 8,5 cm; ağızlar 11 cm → 2,5 cm pay,','#b3452b'),
 ('  kilit komşu ağızların altından geçer ✓ · düşme 6,5 cm','#b3452b'),
 ('· Boşluk 14 cm yeterli (tepsi 3 + pide 1,5 + kilit 4 + pay + ağız 3)','#666'),
 ('','#333'),
 ('DEĞİŞEN: v42\'deki 2×2 küme (±90° varsayımı) → TEK HAT (öteleme).','#9a6b1f'),
 ('Kaset yerleşimi buna göre v11.','#9a6b1f'),
]
yy = NY+22
for s_,c_ in note:
    if s_: tx(NX, yy, s_, 10.2, 'start', 'bold' if s_.endswith(':') else '', c_)
    yy += 17

tx(W-24, H-14, 'AUTOKITCH · tepsi_hareket_analizi_v2', 10, 'end', '', '#999')
svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" width="%d" height="%d"><rect width="%d" height="%d" fill="#ffffff"/>%s</svg>' % (W,H,W,H,W,H,''.join(E))
OUT_ = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\8_ROBOT\tepsi_hareket_analizi_v2.svg"
io.open(OUT_,'w',encoding='utf-8').write(svg)
print('yazildi:', OUT_)
