# -*- coding: utf-8 -*-
# v39 -> v40: PRESS ust bolge = yatay tepsi rafi + pence yuvasi; PACK kesim yandan (bicak yatay, onden ince); KONTROL 6 cozuldu
import io
NL = chr(10)
t = io.open('teknik_cizim39.py', encoding='utf-8').read()
def rep(o, n, c=1):
    global t
    assert t.count(o) == c, 'A(%d): %s' % (t.count(o), o[:80])
    t = t.replace(o, n)

# ---- PRESS ust bolge
s = t.index("# ust bolge: sol uc yuvalari / sag cop")
e = t.index("# ================= 3 TOPPING")
blk = [
"# ust bolge: sol TEPSI RAFI YATAY + PENCE (0-365) / sag COP (365-700)",
"xB=b0+px(365); ln(xB,Y0+px(50),xB,Y0+px(880),1.1,'#111','6,5')",
"rc(b0+px(25),Y0+px(70),px(325),px(180),1.3,3); tx(b0+px(187),Y0+px(110),'PENÇE YUVASI',8,'middle','bold')",
"rc(b0+px(140),Y0+px(130),px(95),px(35),1.1,2); ln(b0+px(155),Y0+px(165),b0+px(168),Y0+px(230),1.2); ln(b0+px(220),Y0+px(165),b0+px(207),Y0+px(230),1.2)",
"tx(b0+px(187),Y0+px(300),'TEPSİ RAFI — 8 YATAY yuva',8,'middle','bold','#1a49b8')",
"for i in range(8):",
"    yy_=Y0+px(330+i*50)",
"    rc(b0+px(28),yy_-px(6),px(18),px(12),1,1); rc(b0+px(328),yy_-px(6),px(18),px(12),1,1)",
"    el(b0+px(187),yy_,px(160),px(9),1.3,'#1a49b8')",
"    rc(b0+px(175),yy_-px(5),px(24),px(10),.8,1,'#1a49b8',None,'#dfe7fb')",
"not_(b0+px(187),Y0+px(760),'kulp ÖNE (robota) · kilit üstten · pitch 5',fs=7)",
"not_(b0+px(187),Y0+px(800),'BEYİN en uzun soğuyanı verir · gün sonu eleman yıkar',fs=6.8)",
"tx(b0+px(187),Y0+px(845),'⑥ ✓ tepsi havuzu burada: 34 + kulp 12 = 46 &lt; derinlik 84',6.5,'middle','bold','#1d7a4f')",
"tx(b0+px(532),Y0+px(115),'ÇÖP',9.5,'middle','bold')",
"ln(b0+px(392),Y0+px(160),b0+px(452),Y0+px(330),1.6); ln(b0+px(672),Y0+px(160),b0+px(612),Y0+px(330),1.6); ln(b0+px(392),Y0+px(160),b0+px(672),Y0+px(160),1.6)",
"not_(b0+px(532),Y0+px(142),'huni — bırak-geç',fs=7.5)",
"rc(b0+px(422),Y0+px(380),px(220),px(470),1.6,4)",
"tx(b0+px(532),Y0+px(600),'KOVA 30 L',9.5,'middle','bold')",
"not_(b0+px(532),Y0+px(660),'motorsuz · eleman HER GÜN',fs=7.5)",
"not_(bm,Y0+px(880)+8,'kabin 70 — sol 36 tepsi rafı + pençe · sağ 34 çöp (v5)',fs=7.5)",
"",
]
t = t[:s] + NL.join(blk) + NL + t[e:]

# ---- PACK: kesim yandan
s = t.index("# ================= 5 PACK")
e = t.index("# ================= UST GORUNUM")
blk = [
"# ================= 5 PACK (bicak yildizi YATAY -> onden ince plaka; kesim bolgesi 41 cm) =================",
"e0,e1=xs[4],xs[5]; em=(e0+e1)/2",
"rc(em-px(60),Y0+px(60),px(120),px(90),1.4,3); ln(em,Y0+px(150),em,Y0+px(250),2.6)",
"rc(em-px(150),Y0+px(250),px(300),px(14),1.6,2)",
"for i in range(7): ln(em-px(135)+i*px(45),Y0+px(264),em-px(135)+i*px(45),Y0+px(298),1.2)",
"rc(em-px(200),Y0+px(330),px(400),px(35),1.4,3,'#777',None,'#eee')",
"tray(em,Y0+px(332),kulp=True)",
"rc(em-px(190),Y0+px(400),px(380),px(70),1.2,2,'#8a6a3a',None,'#fbf3e6'); tx(em,Y0+px(445),'AÇIK KUTU 32×32 — tepsi eğilir, pide kayar',6.5,'middle','','#8a6a3a')",
"not_(em,Y0+px(48),'24V piston · bıçak yıldızı YATAY (önden ince plaka) · iz yeter',fs=7.5)",
"not_(em,Y0+px(316),'kesim yuvası — tepsi oturur, kilit takılı',fs=7)",
"nk(em,Y0+px(385),'④ bıçak Ø28 (tepsi iç 32)',6.5)",
"for r in range(24):",
"    for kx in (e0+8, e0+8+px(320)+4): rc(kx,Y0+px(520)+r*px(45),px(320),px(45),1.05)",
"rc(e0+8,Y0+px(1620),px(320)*2+4,px(220),1.4)",
"for i in range(4): ln(e0+16,Y0+px(1660)+i*px(40),e0+196,Y0+px(1660)+i*px(40),.8)",
"not_(em,Y0+px(505),'katlanmış kutu 2×2×24 = 96 — ELEMAN katlar (ıslak mendil içinde)',fs=7.5)",
"not_(em,Y0+px(1835),'açık deste ≈50',fs=7.5)",
"",
]
t = t[:s] + NL.join(blk) + NL + t[e:]

# ---- UST GORUNUM: PRESS tepsi rafi (36 x 46, sol on) + pence
rep("rc(bm-px(320),YT2+px(20),px(640),px(800),1.6)",
    "rc(bm-px(320),YT2+px(20),px(640),px(800),1.6)" + NL +
    "rc(b0+px(25),YT2+px(380),px(340),px(460),1.2,2,'#1a49b8','5,4'); tx(b0+px(195),YT2+px(600),'tepsi rafı 36×46 (üst)',7,'middle','','#1a49b8')")
rep("not_(bm,YT2+px(890),\"PZP-400 64×80 · üst plaka Ø29 · tepsi Ø34 (mavi)\")",
    "not_(bm,YT2+px(890),\"PZP-400 64×80 · üst plaka Ø29 · üstte tepsi rafı (kesik)\")")
rep("not_(em,YT2+px(890),\"kesim yuvası (tepsi) önde · şarjör 2×2 arkada (kesik)\")",
    "not_(em,YT2+px(890),\"kesim yuvası (tepsi) önde · bıçak yatay · şarjör 2×2 arkada (kesik)\")")

# ---- KONTROL kutusu
rep(' ("⑥ Tepsi havuzu (8-10) + kirli/temiz raf: yeri yok","→ PRESS uç yuvası 2-3 + SERVICE? — Kemal ile ayrıca","#b3452b"),',
    ' ("⑥ Tepsi havuzu ✓ ÇÖZÜLDÜ: PRESS\'te 8 YATAY yuva (v5) — dikey cep sığmıyordu (46 > 33)","→ 8 = fırında 2 + kolda 1 + soğuyan 5; BEYİN saat damgasıyla en soğuğu verir; gün sonu yıkama","#1d7a4f"),')
rep(' ("④ PACK bıçak Ø30 – tepsi iç Ø32: 1 cm pay az","→ bıçak yıldızı Ø28 (pide Ø28 tam) + yuva pimleri","#b3452b"),',
    ' ("④ PACK bıçak Ø30 – tepsi iç Ø32: 1 cm pay az · kesim önden İNCE (yatay yıldız) — bölge 73 → 41 cm","→ bıçak yıldızı Ø28 + yuva pimleri; kazanılan yer şarjöre (80 → 96 kutu)","#9a6b1f"),')
# ---- baslik
rep('tx(X0,Y0-94,"AUTOKITCH — HAT v39 · TÜM İSTASYONLAR SON VERSİYON (4 Eyl 2026) — STORE v38 · PRESS v4 + tepsi · TOPPING v8 · OVEN tepsiyle · PACK kesim yuvası · robot TEPSİ ucu v1",15,"start","bold")',
    'tx(X0,Y0-94,"AUTOKITCH — HAT v40 · TÜM İSTASYONLAR SON VERSİYON (4 Eyl 2026) — STORE v38 · PRESS v5 (yatay tepsi rafı) · TOPPING v8 · OVEN tepsiyle · PACK kesim yandan · robot TEPSİ ucu v1",15,"start","bold")')
rep('tx(X0,Y0-54,"Ölçüler cm. Açık kararlar: ③ dozaj hareketi (saçak / C-tutucu) · ⑥ tepsi havuzu · ① STORE 5. raf + soğutma üstte turu · ② fırın kavitesi 50",10.5,"start","","#b3452b")',
    'tx(X0,Y0-54,"Ölçüler cm. Açık kararlar: ③ dozaj hareketi (saçak / C-tutucu) · ① STORE 5. raf (1L çekmecesi sağa) · ② fırın kavitesi 50 / kulp 6 — ⑥ tepsi rafı ÇÖZÜLDÜ (PRESS v5)",10.5,"start","","#b3452b")')
rep('hat_on_gorunus_teknik_v39.svg', 'hat_on_gorunus_teknik_v40.svg')
io.open('teknik_cizim40.py', 'w', encoding='utf-8', newline='\n').write(t)
print('v40 uretici ok')
