# -*- coding: utf-8 -*-
# v46 -> v47: TOPPING kap simgesi v26 (Picnic tipi: daire duvar R 6,5 + boğaz + yalak, POM helezon Ø7, göbek + çubuk tarak) ·
# ⑧ v26 kap, ⑦ 15,4 kg, robot ≈ 12 kap/hafta, başlık v47. Yerleşim/ölçüler aynı (kap dışı 14×68, kat 27).
import io, math
NL = chr(10)
SRC = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\_uretec\teknik_cizim46.py"
OUT = r"C:\Users\Kemal\Desktop\Kemal\WEBSİTE\AUTOKITCH\arastirma\_uretec\teknik_cizim47.py"
t = io.open(SRC, encoding='utf-8').read()
def rep(o, n, c=1):
    global t
    assert t.count(o) == c, 'A(%d): %s' % (t.count(o), o[:80])
    t = t.replace(o, n)

# ---- kap simgesi: v25 (55° eğim, spiral) -> v26 (Picnic tipi) ----
old_start = "# TOPPING v25 kabi (on gorunus): 14x24 + altta 2 kizak 3x2 + L raf cizgisi"
old_end = NL + "xs=[X0+px(sum(w for _,w in M[:i])) for i in range(6)]"
s = t.index(old_start); e = t.index(old_end)
new_fn = '''# TOPPING v26 kabi (on gorunus, Picnic tipi): dis 14x24 + altta 2 kizak 3x2 + L raf; ic: daire duvar R 6,5 (gobek z 14) + bogaz 7,6 + yalak R 3,8, helezon O7, gobek + 4 cubuk tarak
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
    for dx_ in (30,110): rc(x+px(dx_-15),y+px(240),px(30),px(20),.7,0,col,dsh,'#d0d7de' if not bos else '#f7f6f2')   # kızaklar
    if rail: ln(x-px(6),y+px(262),x+px(146),y+px(262),1.3,'#555')                                # L raf
    tx(x+px(70),y+px(26),nm,fs,'middle','bold',col)
    if alt: tx(x+px(70),y+px(36),alt,4.4,'middle','','#333')
'''
t = t[:s] + new_fn + t[e:]

# ---- metinler ----
rep('tx(X0,Y0-94,"AUTOKITCH — HAT v46 · TÜM İSTASYONLAR SON VERSİYON (5 Eyl 2026) — STORE v4 (+ v5 öneri: −18 kaset katı) · PRESS v8 · TOPPING v25 (kap 14×68×24 · çatal · L raf · kap arkaya dayalı) · OVEN tank+pompa · PACK 116",15,"start","bold")',
    'tx(X0,Y0-94,"AUTOKITCH — HAT v47 · TÜM İSTASYONLAR SON VERSİYON (5 Eyl 2026) — STORE v4 (+ v5 öneri: −18 kaset katı) · PRESS v8 · TOPPING v25 yerleşim + v26 KAP (Picnic tipi: daire duvar · POM helezon · çubuk tarak · şeffaf PC) · OVEN tank+pompa · PACK 116",15,"start","bold")')
rep('Robot: tek kol, 16–20 kg sınıfı (en ağır yük: kıyma kabı 8,6 + kap 4,6 + çatal 2,0 = 15,2 kg — ⑦ açık)', 'Robot: tek kol, 16–20 kg sınıfı (en ağır yük: kıyma kabı 8,4 + kap 5,0 + çatal 2,0 = 15,4 kg — ⑦ açık)')
rep('⑦ kol yükü 15,2 kg + menzil', '⑦ kol yükü 15,4 kg + menzil')
rep(' ("⑦ KOL YÜKÜ YENİDEN AÇIK: kap boş ≈ 4,6 kg (PE 6 mm 2,9 + helezon 1,2 + tarak 0,5) + çatal 2,0 → kıyma 15,2 kg · sucuk 15,0 · kaşar 13,8",',
    ' ("⑦ KOL YÜKÜ YENİDEN AÇIK: kap boş ≈ 5,0 kg (PC 5 mm 3,3 + POM helezon 0,7 + tarak 1,0) + çatal 2,0 → kıyma 15,4 kg · sucuk 14,7 · kaşar 12,8",')
rep(' ("⑧ ✓ TOPPING v25: TEK kap 14×68×24 (PE 6 mm, 17,5 L, simetrik, 16 kap tek kalıp) · 3 kat × 2 · kap ARKAYA DAYALI (ara mil yok)","→ altta 2 kızak + kabinde 2 L raf; robot ÇATALLA önden alır (gir 50 → kaldır 0,5 → çek 70); ALT: soğutma dipte 20 + 2 sıra raf; evaporatör sol kanal","#1d7a4f"),',
    ' ("⑧ ✓ TOPPING v25 yerleşim + v26 KAP (Picnic tipi): dış 14×68×24 aynı · iç: daire duvar R 6,5 (tarak süpürmesiyle eş merkezli) + boğaz 7,6 + yalak · POM milli helezon Ø70 hatve 50 + topuz → yaylı soket · göbek + 4 çubuk tarak · şeffaf PC 5 mm","→ 14,0 L kullanılabilir: kaşar 5,8 kg 1,3 gün (2 poz. 2,6) · kıyma 8,4 kg 2,9 gün · sucuk 7,7 kg 6,4 gün → robot ≈ 12 kap/hafta · kap başına 2 soket (helezon z 3,8 + tarak z 14) ya da tek motor + kayış — AÇIK · 3 kat × 2 · kap ARKAYA DAYALI · 2 kızak + 2 L raf · ÇATAL","#1d7a4f"),')
rep('kap değişimleri gece, haftada 9-10 + STORE→ALT 4"', 'kap değişimleri gece, haftada ≈ 12 + STORE→ALT 4"')
rep('"→ haftalık: robot 9–10 kap değişimi (kaşar 4–5 · kıyma 2 · kuşbaşı 2 · sucuk 1) + 4 STORE→ALT taşıma (gece) · eleman haftada 1 (5 kaşar + 1 sucuk + 2+2 donmuş, 10 boş alır) · uç değiştirici PRESS alt yuvaları"',
    '"→ haftalık (v26 kap): robot ≈ 12 kap değişimi (kaşar 5 · kıyma 3 · kuşbaşı 2 · sucuk 2) + 4 STORE→ALT taşıma (gece) · eleman haftada 1 (5 kaşar + 2 sucuk + 3+2 donmuş, boşları alır) · uç değiştirici PRESS alt yuvaları"')
rep('"→ harçlar KAVRULMUŞ/SOTE vakumlu (çiğ olmaz) · v25 açıkları: tırnak-cep hizası (pim + kamera) · −18 raf buzlanması · klape contaları · soğutma grubu ≤ 20 boy"',
    '"→ harçlar KAVRULMUŞ/SOTE vakumlu (çiğ olmaz) · açıklar: tırnak-cep hizası (pim + kamera) · −18 raf buzlanması · klape contaları · soğutma grubu ≤ 20 boy · v26: yayıcı plaka mı spiral süpürme mi · gramaj prototipi (123 cm³/dev) · PC çizilme"')
rep('tx(kx,ky,"KONTROL — istasyonlar arası uyum (5 Eyl 2026, HAT v46)",12,"start","bold","#b3452b")', 'tx(kx,ky,"KONTROL — istasyonlar arası uyum (5 Eyl 2026, HAT v47)",12,"start","bold","#b3452b")')
rep("notew(cm2,YT2+px(1050),'kat 1 planı · kap 68 arka duvara dayalı, ara mil yok · ağız ön uçta y 76, merkez x 27/43 · süpürme R 27 = tepsi 16 + spiral 11 · kesikli = kızak cepleri (çatal) · 10+68+2+4 = 84',c1-c0-20,6.5)",
    "notew(cm2,YT2+px(1050),'kat 1 planı · kap 68 arka duvara dayalı, ara mil yok · ağız ön uçta y 63 (6×6,5), merkez x 27/43 · süpürme R 27 = tepsi 16 + spiral 11 · kesikli = kızak cepleri (çatal) · 10+68+2+4 = 84',c1-c0-20,6.5)")
rep("    ln(c0+px(xk+70),YT2+px(120),c0+px(xk+70),YT2+px(760),1.4,'#1d7a4f')" + NL + "    ci(c0+px(xk+70),YT2+px(760),px(22),1.4,'#1d7a4f',None,'#fff'); ci(c0+px(xk+70),YT2+px(760),px(270),1,'#1d7a4f','5,3')",
    "    ln(c0+px(xk+70),YT2+px(105),c0+px(xk+70),YT2+px(705),1.4,'#1d7a4f')" + NL + "    rc(c0+px(xk+40),YT2+px(700),px(60),px(65),1.2,1,'#1d7a4f',None,'#eaf6ee'); ci(c0+px(xk+70),YT2+px(732),px(270),1,'#1d7a4f','5,3')")
rep("rc(kx-10,ky-18,KW,px(1800),1.4,6,'#b3452b',None,'#fff8f5')", "rc(kx-10,ky-18,KW,px(1930),1.4,6,'#b3452b',None,'#fff8f5')")
rep('W=int(X0+px(T)+px(2200)); H=int(YT2+px(1860))', 'W=int(X0+px(T)+px(2200)); H=int(YT2+px(1990))')
rep('hat_on_gorunus_teknik_v46.svg', 'hat_on_gorunus_teknik_v47.svg')
rep('"""HAT v46 —', '"""HAT v47 (v46 + TOPPING kap simgesi v26 Picnic tipi, ⑦ 15,4, ⑧ v26, robot ≈ 12 kap/hafta) — v46:')
io.open(OUT, 'w', encoding='utf-8', newline='\n').write(t)
print('teknik_cizim47.py yazildi')
