# -*- coding: utf-8 -*-
# ist1_store2 -> ist1_store3: on gorunuste icerikler KESIK cizgiyle (toplar, kutular, siseler, kasetler) + icecek pitch 130 / 1L 320
import io
NL = chr(10)
t = io.open('ist1_store2.py', encoding='utf-8').read()
def rep(o, n, c=1):
    global t
    assert t.count(o) == c, 'A(%d): %s' % (t.count(o), o[:80])
    t = t.replace(o, n)
rep("İSTASYON 1 — STORE · DETAY v2 (gerçek kalınlıklar · 61 cm çekmece modülleri · alt buzluk 6 çekmeceye bölündü · robot erişimi)",
    "İSTASYON 1 — STORE · DETAY v3 (v2 + ön görünüşte içerikler kesik çizgiyle · içecek çekmecesi 13 (dik kutu 12,3) · 1 L çekmecesi 32)")
# icecek cekmeceleri 130 pitch, 1L 320 + icerikler kesik
old = """for k in range(4):
    y = Y0+px(Y3+5)+k*px(105)
    front(xl,y,wcol,px(95),'#111',PU,'İÇECEK %d — 7 kanal' % (k+1),'kutu 24 · tatlı 3 · yedek 1')
front(xl,Y0+px(Y3+5)+4*px(105),wcol,px(410),'#111',PU,'1 L ÇEKMECESİ — 5 kanal × 8','şişe dik, ~40')
for r in range(8):
    y = Y0+px(Y3+5)+r*px(105)
    front(xr,y,wcol,px(95),'#111',PU,'TAZE %d — 1 tepsi 20 top' % (r+1),'')"""
new = """D = '3,3'
for k in range(4):
    y = Y0+px(Y3+5)+k*px(130)
    front(xl,y,wcol,px(120),'#111',PU,'','')
    for i in range(7):                                                        # dik kutular (on sira) — kesik
        rc(xl+px(22)+i*px(82),y+px(4),px(66),px(112),.9,3,'#777',D)
        el(xl+px(22)+i*px(82)+px(33),y+px(8),px(33),px(6),.7,'#777',D)
    tx(xl+wcol/2,y+px(60)+3,'İÇECEK %d — 7 kanal · dik kutu 12,3' % (k+1),7,'middle','bold','#111')
y1L = Y0+px(Y3+5)+4*px(130)
front(xl,y1L,wcol,px(310),'#111',PU,'','')
for i in range(5):                                                            # 1 L siseler — kesik
    bx = xl+px(50)+i*px(110)
    rc(bx,y1L+px(60),px(85),px(245),.9,6,'#777',D); rc(bx+px(28),y1L+px(12),px(29),px(48),.9,2,'#777',D)
tx(xl+wcol/2,y1L+px(160),'1 L ÇEKMECESİ — 5 kanal × 8 (şişe dik, 27-30 cm)',7,'middle','bold','#111')
for r in range(8):
    y = Y0+px(Y3+5)+r*px(105)
    front(xr,y,wcol,px(95),'#111',PU,'','')
    ln(xr+px(30),y+px(50),xr+wcol-px(30),y+px(50),.9,'#777',D)                # tepsi ust yuzu — kesik
    for i in range(4):                                                        # on sira 4 top — kesik
        el(xr+px(95)+i*px(140),y+px(38),px(45),px(28),.9,'#777',D)
    tx(xr+wcol/2,y+px(80),'TAZE %d — 1 tepsi 20 top' % (r+1),6.5,'middle','bold','#111')"""
rep(old, new)
rep("not_(X0+px(1027),Y0+px(Y3+5)+8*px(105)+10,'8 × 20 = 160 (2 gün) · pitch 10,5: kutu 1,5 + tepsi 3 + top 4,5 + boşluk 1,5',fs=7.5)",
    "not_(X0+px(1027),Y0+px(Y3+5)+8*px(105)+10,'8 × 20 = 160 (2 gün) · pitch 10,5 · sol: 4 × 13 + 32 = 84 ✓',fs=7.5)")
# donmus hamur + kasetler — kesik icerik
old2 = """for k in range(2):
    y = Y0+px(1225)+k*px(105)
    front(xl2,y,wcol2,px(95),Bl,'#dfe7fb','DONMUŞ %d — 20 top' % (k+1),'')
    front(xr2,y,wcol2,px(95),Bl,'#dfe7fb','DONMUŞ %d — 20 top' % (k+3),'')
front(xl2,Y0+px(1440),wcol2,px(300),Bl,'#dfe7fb','KASET: KAVURMA ×2','17×21×25 · −18 · boş yer +1')
front(xr2,Y0+px(1440),wcol2,px(300),Bl,'#dfe7fb','KASET: KUŞBAŞI ×2','17×21×25 · −18 · boş yer +1')"""
new2 = """for k in range(2):
    y = Y0+px(1225)+k*px(105)
    for xx_,nm in ((xl2,k+1),(xr2,k+3)):
        front(xx_,y,wcol2,px(95),Bl,'#dfe7fb','','')
        ln(xx_+px(30),y+px(50),xx_+wcol2-px(30),y+px(50),.9,Bl,D)
        for i in range(4): el(xx_+px(92)+i*px(140),y+px(38),px(45),px(28),.9,Bl,D)
        tx(xx_+wcol2/2,y+px(80),'DONMUŞ %d — 20 top' % nm,6.5,'middle','bold',Bl)
for xx_,nm in ((xl2,'KAVURMA'),(xr2,'KUŞBAŞI')):
    front(xx_,Y0+px(1440),wcol2,px(300),Bl,'#dfe7fb','','')
    for i in range(2):
        rc(xx_+px(40)+i*px(185),Y0+px(1470),px(170),px(250),1,2,Bl,D)
        rc(xx_+px(40)+i*px(185)+px(150),Y0+px(1530),px(14),px(70),.9,1,Bl,D)
    rc(xx_+px(410),Y0+px(1470),px(170),px(250),.8,2,'#999',D); tx(xx_+px(495),Y0+px(1600),'boş +1',6,'middle','','#999')
    tx(xx_+wcol2/2,Y0+px(1745),'KASET: %s ×2 · 17×21×25 · −18' % nm,6.5,'middle','bold',Bl)"""
rep(old2, new2)
rep("tx(X0+px(700),Y0+px(1758),'−18 °C bandı — 4 hamur çekmecesi = 80 top (1 gün) + 2 kaset çekmecesi · çekmece önü 60 izoleli',7.5,'middle','bold',Bl)",
    "tx(X0+px(700),Y0+px(1762),'−18 °C bandı — 4 hamur çekmecesi = 80 top (1 gün) + 2 kaset çekmecesi · çekmece önü 60 izoleli · kesik = içerik',7,'middle','bold',Bl)")
# notlar: içecek pitch
rep(" ('· Pitch 105: 8 taze = 84 cm; dikey bütçe tutuyor','','#333'),",
    " ('· Pitch: taze 10,5 × 8 = 84 · içecek 13 × 4 (dik','','#333'),\n ('  kutu 12,3) + 1 L 32 = 84 ✓ (v2 hatası düzeldi)','','#333'),")
rep("tx(DX,cy+40,'DİKEY: 20 + 220 + 60 + 8×105 + 80 + 2×105 + 290 + 80 = 1800 → 50 mm pay → 185 + ayak 12 = 197 ✓',9,'start','bold',G)",
    "tx(DX,cy+40,'DİKEY: 20 + 220 + 60 + 8×105 (sol: 4×130 + 320) + 80 + 2×105 + 290 + 80 = 1800 → 50 pay → 185 + ayak 12 = 197 ✓',9,'start','bold',G)")
rep("'AUTOKITCH · ist1_store_detay_v2'", "'AUTOKITCH · ist1_store_detay_v3'")
rep("ist1_store_detay_v2.svg", "ist1_store_detay_v3.svg")
io.open('ist1_store3.py', 'w', encoding='utf-8', newline='\n').write(t)
print('store3 ok')
